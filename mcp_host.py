import asyncio
from contextlib import AsyncExitStack
from dotenv import load_dotenv

from mcp import ClientSession
from mcp.client.stdio import stdio_client, StdioServerParameters

from langchain_openai import ChatOpenAI
from langchain_mcp_adapters.tools import load_mcp_tools
from langchain.agents import create_agent

load_dotenv()


async def run():
    async with AsyncExitStack() as stack:
        # 1. MCP Server 연결
        params = StdioServerParameters(
            command="python",
            args=["mcp_server.py"]
        )

        read, write = await stack.enter_async_context(
            stdio_client(params)
        )

        session = await stack.enter_async_context(
            ClientSession(read, write)
        )
        await session.initialize()

        # 2. MCP Tool 로드
        tools = await load_mcp_tools(session)

        # 3. LLM 준비
        llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0
        )

        # 4. Agent 생성
        agent = create_agent(llm, tools)

        # # 5. 사용자 질문
        # user_question = """
        # train_result.json 파일을 요약해서
        # Notion에 기록해줘.
        # 제목은 '모델 실험 결과 - step 500'으로 해줘.
        # """

        # result = await agent.ainvoke({
        #     "messages": [
        #         ("user", user_question)
        #     ]
        # })

        #2차 실습 : 파일 결과 속 값을 이용해 페이지 생성하기
        user_question = """
            train_result.json 파일을 읽고 다음을 수행해줘:

            1. 파일에서 global_step 값을 찾아서 확인해
            2. 파일 내용을 요약해서 Notion에 기록해줘
            3. Notion 페이지 제목은 '모델 실험 결과 - step {global_step 값}'으로 설정해줘
            (예: global_step이 500이면 '모델 실험 결과 - step 500')
            4. epoch 값도 함께 추출해서 나에게 알려줘
            """

        result = await agent.ainvoke({
                "messages": [
                    ("user", user_question)
                ]
            })

        print(result)


if __name__ == "__main__":
    asyncio.run(run())