"""
AI 客户端 —— 支持多模型供应商，通过 .env 切换。

支持的供应商:
  - deepseek  : DeepSeek API (国内直连，便宜，推荐)
  - anthropic : Anthropic Claude API
  - openai    : OpenAI 兼容接口 (可接入任何 OpenAI 兼容服务)

切换方式: .env 中设置 AI_PROVIDER=deepseek
"""

import os
import json
import httpx
from skill_loader import build_system_prompt


# ============================================================
# Provider 检测
# ============================================================

def _provider() -> str:
    return os.environ.get("AI_PROVIDER", "deepseek").lower()


def _model() -> str:
    defaults = {
        "deepseek": "deepseek-chat",
        "anthropic": "claude-sonnet-4-6",
        "openai": "gpt-4o",
    }
    return os.environ.get("AI_MODEL", defaults.get(_provider(), "deepseek-chat"))


# ============================================================
# DeepSeek
# ============================================================

async def _chat_deepseek(messages: list[dict], system_prompt: str) -> str:
    api_key = os.environ.get("DEEPSEEK_API_KEY", "")
    base_url = os.environ.get("DEEPSEEK_BASE_URL", "https://api.deepseek.com")

    full_messages = [{"role": "system", "content": system_prompt}]
    full_messages.extend(messages)

    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.post(
            f"{base_url}/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": _model(),
                "messages": full_messages,
                "max_tokens": 4096,
                "temperature": 0.7,
            },
        )
        data = resp.json()
        return data["choices"][0]["message"]["content"]


# ============================================================
# Anthropic Claude
# ============================================================

async def _chat_anthropic(messages: list[dict], system_prompt: str) -> str:
    import anthropic

    api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    client = anthropic.Anthropic(api_key=api_key)

    # Anthropic 的 system 是独立参数
    anthropic_messages = []
    for m in messages:
        role = m["role"]
        if role == "system":
            continue
        anthropic_messages.append({"role": role, "content": m["content"]})

    response = client.messages.create(
        model=_model(),
        max_tokens=4096,
        system=system_prompt,
        messages=anthropic_messages,
        temperature=0.7,
    )
    return response.content[0].text


# ============================================================
# OpenAI 兼容 (也可用于其他兼容服务如 硅基流动、通义千问 等)
# ============================================================

async def _chat_openai(messages: list[dict], system_prompt: str) -> str:
    api_key = os.environ.get("OPENAI_API_KEY", "")
    base_url = os.environ.get("OPENAI_BASE_URL", "https://api.openai.com")

    full_messages = [{"role": "system", "content": system_prompt}]
    full_messages.extend(messages)

    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.post(
            f"{base_url}/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": _model(),
                "messages": full_messages,
                "max_tokens": 4096,
                "temperature": 0.7,
            },
        )
        data = resp.json()
        return data["choices"][0]["message"]["content"]


# ============================================================
# 统一入口
# ============================================================

_CHAT_FN = {
    "deepseek": _chat_deepseek,
    "anthropic": _chat_anthropic,
    "openai": _chat_openai,
}


async def chat(user_message: str, conversation_history: list[dict] | None = None) -> str:
    """
    处理用户消息，返回 AI 客服回复。

    Args:
        user_message: 当前用户消息
        conversation_history: [{"role": "user"|"assistant", "content": "..."}]
    """
    prov = _provider()
    chat_fn = _CHAT_FN.get(prov)
    if chat_fn is None:
        raise ValueError(f"不支持的 AI_PROVIDER: {prov}，可选: {', '.join(_CHAT_FN.keys())}")

    system_prompt = build_system_prompt()

    messages = []
    if conversation_history:
        messages.extend(conversation_history[-20:])
    messages.append({"role": "user", "content": user_message})

    return await chat_fn(messages, system_prompt)


async def chat_simple(user_message: str) -> str:
    """无历史对话的简单调用"""
    return await chat(user_message)


# ============================================================
# 多角色协同机器人 System Prompts
# ============================================================
# 工作流：用户 → 审查Bot(调度) → 前端Bot+后端Bot(执行) → 审查Bot(检查) → 用户
# 所有机器人在同一个飞书群里，对话历史按 chat_id 共享，互相可见。

ROLE_PROMPTS = {
    "reviewer": """你是「审查Bot」——本群协同开发团队的**任务调度中心和质检官**。

## 工作流程（严格遵守）
用户 @你 提交需求后，你按以下流程执行：

### 第一步：分析任务
- 理解用户需求，判断需要前端还是后端参与
- 如果只需要一端（纯前端或纯后端），只派发该端
- 如果需要两端配合，同时派发

### 第二步：派发任务
用以下格式回复（前端Bot和后端Bot会收到并自动响应）：

```
📋 任务分解：

@前端Bot
任务：[具体的前端任务描述，包含技术要求]
要求：[验收标准]

@后端Bot
任务：[具体的后端任务描述，包含接口要求]
要求：[验收标准]

@用户 请等待，完成后我会统一审查汇报。
```

### 第三步：等待执行
- 等待前端Bot 和后端Bot 完成并 @你
- 如果超过合理时间没有回复，可以追问进度

### 第四步：审查验收
收到完成通知后：
1. 查看前端和后端的输出代码
2. 逐项审查：逻辑、安全、性能、规范
3. 检查前后端接口是否对齐
4. 发现问题 → @对应Bot 要求修正（回到第三步）
5. 审查通过 → 进入第五步

### 第五步：汇报用户
审查通过后，@用户 汇报：

```
📋 项目交付报告

✅ 前端（@前端Bot）：[完成内容概述]
✅ 后端（@后端Bot）：[完成内容概述]

🔍 审查结论：[通过/有问题已修复]

📌 注意事项：[上线前需要注意的点]
```

## 审查标准
- 代码：逻辑正确性、安全性（OWASP top 10）、性能、可维护性
- API 设计：RESTful 规范、鉴权、限流、幂等、错误码
- 前后端对齐：接口路径、入参、出参、错误码格式一致

## 禁止事项
- 不要自己去写前端或后端代码，只做调度和审查
- 不要在两端都未完成时就开始汇报用户""",

    "frontend": """你是「前端Bot」——本群协同开发团队的**前端执行者**。

## 工作流程（严格遵守）

### 收到任务时
收到审查Bot 或用户派发的任务后：
1. 确认理解需求，如果不清楚就追问
2. 查看对话历史中审查Bot 的@后端Bot 任务，了解后端接口设计
3. 写出完整可运行的前端代码

### 任务完成时
代码完成后，必须在结尾 @审查Bot 报告：

```
@审查Bot 前端任务完成。
产出：[简述完成了什么]
接口依赖：[需要后端提供的 API 格式]
请检查。
```

### 收到修改要求时
如果审查Bot 提出修改意见：
1. 逐条处理修改意见
2. 修改完成后重新 @审查Bot 报告

## 技术栈
React 19 / Vue 3 / Next.js / TypeScript / Tailwind CSS / Vite

## 输出格式
- 完整组件代码（含 imports、类型定义、样式）
- 复杂交互标注关键逻辑
- 涉及 API 调用时，明确写出期望的接口契约

## 禁止事项
- 完成后不要 @用户，只 @审查Bot（由审查Bot 统一汇报）
- 不要写后端代码""",

    "backend": """你是「后端Bot」——本群协同开发团队的**后端执行者**。

## 工作流程（严格遵守）

### 收到任务时
收到审查Bot 或用户派发的任务后：
1. 确认理解需求，如果不清楚就追问
2. 查看对话历史中审查Bot 的@前端Bot 任务，了解前端期望的接口格式
3. 先设计 API 接口，再写实现代码

### 任务完成时
代码完成后，必须在结尾 @审查Bot 报告：

```
@审查Bot 后端任务完成。
产出：[简述完成了什么]
接口清单：[列出 API 的路径和方法]
请检查。
```

### 收到修改要求时
如果审查Bot 提出修改意见：
1. 逐条处理修改意见
2. 修改完成后重新 @审查Bot 报告

## 技术栈
Go / Python / Node.js / PostgreSQL / Redis / Docker

## 输出格式
- 先给接口设计（路径/方法/入参/出参/错误码）
- 再给核心逻辑代码
- 最后给 curl 测试示例

## 禁止事项
- 完成后不要 @用户，只 @审查Bot（由审查Bot 统一汇报）
- 不要写前端代码""",
}


def get_role_prompt(role: str) -> str:
    """获取指定角色的 system prompt"""
    return ROLE_PROMPTS.get(role, build_system_prompt())


async def chat_with_role(user_message: str, role: str, conversation_history: list[dict] | None = None) -> str:
    """以特定角色处理用户消息"""
    prov = _provider()
    chat_fn = _CHAT_FN.get(prov)
    if chat_fn is None:
        raise ValueError(f"不支持的 AI_PROVIDER: {prov}，可选: {', '.join(_CHAT_FN.keys())}")

    system_prompt = get_role_prompt(role)

    messages = []
    if conversation_history:
        messages.extend(conversation_history[-20:])
    messages.append({"role": "user", "content": user_message})

    return await chat_fn(messages, system_prompt)


# ============================================================
# 对话记忆（内存版，生产环境建议换 Redis）
# ============================================================

class ConversationStore:

    def __init__(self, max_size: int = 1000):
        self._store: dict[str, list[dict]] = {}
        self._max_size = max_size

    def get(self, session_id: str) -> list[dict]:
        return self._store.get(session_id, [])

    def add(self, session_id: str, role: str, content: str):
        if session_id not in self._store:
            self._store[session_id] = []
        self._store[session_id].append({"role": role, "content": content})
        if len(self._store[session_id]) > 40:
            self._store[session_id] = self._store[session_id][-40:]
        if len(self._store) > self._max_size:
            oldest = next(iter(self._store))
            del self._store[oldest]


conversations = ConversationStore()
