pip install streamlit openai python-dotenv
```

**프로젝트 구조:**
```
chatbot/
├── .env              # API 키 저장
├── app.py            # 기본 챗봇 코드
├── app_adv.py        # 메인 챗봇 코드
└── memory.py         # 기억 챗봇 코드
└── rag_chatbot.py    # 학습 챗봇 코드

```

**1. .env 파일 (API 키 보관):**
```
OPENAI_API_KEY=sk-your-api-key-here


---
**2. 메인 챗봇 소개


# 💬 AI 챗봇 (Streamlit 기반)

이 프로젝트는 **Streamlit**과 **OpenAI API**를 사용해 만든  
웹 기반 AI 챗봇 애플리케이션입니다.

사용자는 웹 UI에서  
- 모델 선택  
- 응답 창의성(Temperature) 조절  
- 시스템 프롬프트 직접 설정  

을 통해 **AI의 응답 성격을 실시간으로 제어**할 수 있습니다.

---

## 🖥️ 미리보기

- Streamlit 웹 UI
- 좌측 사이드바에서 모델 / 설정 제어
- 중앙 영역에서 실시간 채팅
- 응답 스트리밍 출력

---

## 📁 프로젝트 구조

```text
2026_web_chatbot/
└─ code/
   ├─ app.py              # Streamlit 챗봇 메인 애플리케이션
   ├─ .env                # OpenAI API Key (로컬에서만 사용)
   └─ requirements.txt    # 필요 라이브러리 목록

