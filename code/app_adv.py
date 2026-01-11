import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os

# 환경변수 로드
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 페이지 설정
st.set_page_config(
    page_title="AI 챗봇",
    page_icon="💬",
    layout="wide"
)

st.title("💬 AI 챗봇")

# 사이드바 설정
with st.sidebar:
    st.header("⚙️ 설정")
    
    # 모델 선택
    model = st.selectbox(
        "모델 선택",
        ["gpt-4o", "gpt-4o-mini", "gpt-3.5-turbo"],
        index=1
    )
    
    # 온도 설정
    temperature = st.slider(
        "창의성 (Temperature)",
        min_value=0.0,
        max_value=2.0,
        value=0.7,
        step=0.1,
        help="낮을수록 일관적, 높을수록 창의적"
    )
    
    # 시스템 프롬프트
    st.subheader("시스템 프롬프트")
    system_prompt = st.text_area(
        "AI의 역할과 성격을 정의하세요",
        value="당신은 친절하고 도움이 되는 AI 어시스턴트입니다. 사용자의 질문에 명확하고 정확하게 답변해주세요.",
        height=150
    )
    
    st.divider()
    
    # 대화 초기화 버튼
    if st.button("🗑️ 대화 초기화", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    
    st.divider()
    
    # 통계 표시
    if "messages" in st.session_state:
        msg_count = len([m for m in st.session_state.messages if m["role"] == "user"])
        st.metric("대화 횟수", msg_count)

# 세션 상태 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []

# 기존 대화 표시
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 사용자 입력
if prompt := st.chat_input("메시지를 입력하세요..."):
    # 사용자 메시지 저장 및 표시
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # AI 응답 생성 (스트리밍)
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        # 시스템 프롬프트 포함한 메시지 구성
        messages_with_system = [
            {"role": "system", "content": system_prompt}
        ] + st.session_state.messages
        
        # 스트리밍 응답
        try:
            stream = client.chat.completions.create(
                model=model,
                messages=messages_with_system,
                temperature=temperature,
                stream=True
            )
            
            for chunk in stream:
                if chunk.choices[0].delta.content is not None:
                    full_response += chunk.choices[0].delta.content
                    message_placeholder.markdown(full_response + "▌")
            
            message_placeholder.markdown(full_response)
            
        except Exception as e:
            st.error(f"오류 발생: {str(e)}")
            full_response = "죄송합니다. 응답을 생성하는 중 오류가 발생했습니다."
            message_placeholder.markdown(full_response)
    
    # AI 응답 저장
    st.session_state.messages.append({"role": "assistant", "content": full_response})