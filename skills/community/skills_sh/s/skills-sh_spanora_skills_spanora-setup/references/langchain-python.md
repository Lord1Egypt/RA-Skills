# Pattern E: LangChain / LangGraph (Python)

Instrument LangChain and LangGraph Python applications using standard OpenTelemetry auto-instrumentation — **no Spanora SDK required**. The [`opentelemetry-instrumentation-langchain`](https://pypi.org/project/opentelemetry-instrumentation-langchain/) package automatically captures every LLM call, chain invocation, and tool execution.

## Install Dependencies

```bash
pip install langchain langchain-openai langgraph \
  opentelemetry-sdk \
  opentelemetry-exporter-otlp \
  opentelemetry-instrumentation-langchain
```

If the project uses `uv`:

```bash
uv add langchain langchain-openai langgraph \
  opentelemetry-sdk \
  opentelemetry-exporter-otlp \
  opentelemetry-instrumentation-langchain
```

If the project uses `.env` files, also install `python-dotenv`:

```bash
pip install python-dotenv
```

## OTEL Setup

Create this once at application startup — **before** any LangChain imports that trigger calls:

```python
import os
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.instrumentation.langchain import LangchainInstrumentor

resource = Resource.create({
    "service.name": "my-langchain-app",
    "gen_ai.agent.name": "my-agent",
})

provider = TracerProvider(resource=resource)
provider.add_span_processor(BatchSpanProcessor(OTLPSpanExporter(
    endpoint=os.environ.get("SPANORA_ENDPOINT", "https://spanora.ai/api/v1/traces"),
    headers={"Authorization": f"Bearer {os.environ['SPANORA_API_KEY']}"},
)))
trace.set_tracer_provider(provider)

# Auto-instrument LangChain — call AFTER setting the provider
LangchainInstrumentor().instrument()
```

**Important:** `TracerProvider` must be set **before** calling `LangchainInstrumentor().instrument()`.

## Text Generation (Chain Invocation)

```python
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

llm = ChatOpenAI(model="gpt-4o-mini")
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant."),
    ("human", "{input}"),
])
chain = prompt | llm

result = chain.invoke(
    {"input": "What is the capital of France?"},
    config={"metadata": {"user_id": "usr_123", "org_id": "org_acme"}},
)
print(result.content)
```

All LLM calls, prompts, tokens, and chain structure are captured automatically.

## Streaming

```python
llm = ChatOpenAI(model="gpt-4o-mini", streaming=True)
chain = prompt | llm

for chunk in chain.stream(
    {"input": "Write a haiku about observability."},
    config={"metadata": {"user_id": "usr_123", "org_id": "org_acme"}},
):
    print(chunk.content, end="", flush=True)
```

## Tool Calls (ReAct Agent)

Tools decorated with `@tool` are auto-instrumented — tool spans appear in the trace with name, input, and output:

```python
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain.agents import create_agent

@tool
def get_weather(city: str) -> str:
    """Get the current weather for a given city."""
    return f"72F and sunny in {city}"

@tool
def search_web(query: str) -> str:
    """Search the web for information."""
    return f"Results for: {query}"

llm = ChatOpenAI(model="gpt-4o-mini")
agent = create_agent(llm, [get_weather, search_web])

result = agent.invoke(
    {"messages": [{"role": "user", "content": "What's the weather in Paris?"}]},
    config={"metadata": {"user_id": "usr_123", "org_id": "org_acme"}},
)
print(result["messages"][-1].content)
```

## Multi-Turn Conversation

```python
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

llm = ChatOpenAI(model="gpt-4o-mini")
metadata = {"user_id": "usr_123", "org_id": "org_acme"}

messages = [HumanMessage(content="My name is Alice. I live in Tokyo.")]

# Each invoke is traced as a separate LLM span
response = llm.invoke(messages, config={"metadata": metadata})
messages.append(response)

messages.append(HumanMessage(content="What city do I live in?"))
response = llm.invoke(messages, config={"metadata": metadata})
messages.append(response)

messages.append(HumanMessage(content="What's my name?"))
response = llm.invoke(messages, config={"metadata": metadata})
```

## User and Org Context

Pass `user_id` and `org_id` via LangChain's `config.metadata` on any runnable (chains, agents, LLMs, tools). The metadata propagates to all child spans:

```python
result = chain.invoke(
    {"input": "How do I reset my password?"},
    config={
        "metadata": {
            "user_id": "usr_abc123",
            "org_id": "org_acme",
        }
    },
)
```

## Shutdown

For **scripts and CLIs**, flush remaining spans before exit:

```python
provider.shutdown()
```

For **long-running servers** (FastAPI, Flask, etc.), the `BatchSpanProcessor` flushes automatically — explicit shutdown is not required.

## Environment Variables

```
SPANORA_API_KEY=ak_your_api_key
SPANORA_ENDPOINT=https://spanora.ai/api/v1/traces
OPENAI_API_KEY=sk-...
```

The endpoint must end with `/api/v1/traces`. The API key is passed as a `Bearer` token in the `Authorization` header.

## What Gets Captured Automatically

The `LangchainInstrumentor` captures:
- **LLM calls**: model, provider, prompt input/output, token counts
- **Tool executions**: tool name, input arguments, output, status
- **Chain structure**: nested spans showing the execution flow
- **Agent reasoning**: multi-step agent loops with tool calls and follow-ups

No manual wrapping or SDK calls needed — just configure OTEL once and use LangChain normally.

## Troubleshooting

- **Traces not appearing?** Verify the API key has `Bearer ` prefix in the auth header, and the endpoint URL ends with `/api/v1/traces`
- **Missing prompt content?** Ensure `TRACELOOP_TRACE_CONTENT` is not set to `false`
- **Missing tokens/cost?** Token counts come from the LLM provider response. Cost is auto-calculated by Spanora from model + tokens
