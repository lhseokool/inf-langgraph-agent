# LangGraph를 활용한 LLM Agent 개발

- 강의 목차 중 코드 작성을 하지 않는 회차는 포함되지 않았습니다

## 목차

### 2. LangGraph 기초
- 2.1 LangChain vs LangGraph (feat. LangGraph 개념 설명)
- 2.2 간단한 Retrieval 에이전트 (feat. PDF 전처리 꿀팁)
- 2.3 공식문서 따라하며 실패하는 Agentic RAG
- 2.4 생성된 답변을 여러번 검증하는 Self-RAG
- 2.5 웹 검색을 지원하는 Corrective RAG
- 2.6 SubGraph: LangGraph Agent를 Node로 활용하는 방법
- 2.7 병렬 처리를 통한 효율 개선 (feat. 프롬프트 엔지니어링)
- 2.8 Multi-Agent 시스템과 RouteLLM

### 3. 도구(Tool) 활용과 고급 기능
- 3.1 Workflow vs "찐" Agent (코드 없는 이론설명)
- 3.2 LangChain에서 도구(tool) 활용 방법
- 3.3 LangGraph에서 도구(tool) 활용 방법
- 3.4 LangGraph 내장 도구(tool)를 활용해서 만드는 Agent
- 3.5 Agent의 히스토리를 관리하는 방법
- 3.6 human-in-the-loop: 사람이 Agent와 소통하는 방법
- 3.7 "찐" Multi-Agent System (feat. create_react_agent)

## 시작하기

1. 저장소 클론:

```bash
git clone https://github.com/jasonkang14/inflearn-langgraph-agent
```

2. 필요한 패키지 설치:
```bash
pip install -r requirements.txt
```

3. 노트북 실행 옵션:
- CURSOR:
    ```bash
    cursor run (강의에서는 cursor .)
    ```
- VSCode:
    ```bash
    code .
    ```
- Jupyter Notebook:
    ```bash
    jupyter notebook
    ```

## 요구사항

- Python 3.11+
- 기타 필요한 패키지는 각 노트북 파일에 명시되어 있습니다

## 라이선스

MIT 라이선스로 배포됩니다.
