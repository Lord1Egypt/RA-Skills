---
name: Smart Model Router
description: Optimize Your API Costs - Route tasks to cost-effective models via TokenRouter. Dynamically builds model tiers from live pricing, classifies tasks into 6 categories (supporting English & Chinese), and orchestrates multi-agent workflows with adaptive fallback.
---

## Pre-flight Check: PaleBlueDot AI TokenRouter Provider Configuration

**This skill requires a PaleBlueDot AI TokenRouter provider to be configured. Before using ANY feature, the agent MUST perform the following check-and-setup flow.**

### Phase 1: Check Existing Provider

1. Read the configuration file at `~/.openclaw/openclaw.json`.
2. Look under `models.providers` for any provider whose `baseUrl` **contains** `https://open.palebluedot.ai` (partial match is sufficient).
3. **If found** → Skip to **Phase 3** (the provider is already configured).
4. **If NOT found** → Proceed to **Phase 2**.

### Phase 2: Guide User & Write Configuration

When no TokenRouter provider is detected, the agent should:

1. **Inform the user** that TokenRouter is not configured and prompt them to register:

   > TokenRouter provider not configured. To use this skill, you need a PaleBlueDot AI TokenRouter account.
   > Please visit **https://www.palebluedot.ai** to register and log in, then go to the **TokenRouter** section to get your configuration (base URL and API key).
   > Once you have the information, please provide it to me and I will complete the configuration for you.

2. **Wait for the user** to provide the following information:
   - **Base URL** (e.g., `https://open.palebluedot.ai/v1`)
   - **API Key** (the user's real API key from PaleBlueDot AI)
   - *(Optional)* **Provider name** (defaults to `tokenrouter` if not specified)

3. **Agent writes the configuration** by running the `setup` command:
   ```
   setup --name <provider_name> --base-url <baseUrl> --api-key <apiKey>
   ```
   This writes the provider into `~/.openclaw/openclaw.json` under `models.providers` with a backup of the original config.

4. **Do NOT use placeholder API keys.** The agent must only write the actual credentials provided by the user.

### Phase 3: Re-verify & Auto-Sync Models

After the provider is confirmed (either pre-existing or just written in Phase 2), the agent MUST:

1. **Re-verify** the provider configuration by running:
   ```
   check
   ```
   This confirms the provider with `baseUrl` containing `https://open.palebluedot.ai` is properly saved in the config.

2. **If verification fails**, inform the user and go back to Phase 2.

3. **If verification succeeds**, automatically sync models by running:
   ```
   sync
   ```
   This will:
   - Fetch all available models from the TokenRouter API.
   - Add all model names to the TokenRouter provider's `models` array.
   - Add all models to the `models.allowed` list.
   - All models will be routed through the configured TokenRouter provider.
   - Display the synced model list to the user.

4. **Confirm completion** to the user:
   > TokenRouter configuration complete. {N} models have been synced and added to your allow list. All models are routed through the TokenRouter provider. You can now use `list` to view pricing or start planning tasks.

---

## Automatic Pre-Planning Sync

**Before executing any `plan` command, the system will automatically:**

1. **Verify TokenRouter Provider**: Checks if a provider whose `baseUrl` contains `https://open.palebluedot.ai` exists in `models.providers`. **If not found, the agent enters the Phase 2 setup flow** described above.
2. **Auto-Sync Models**: Fetches the latest model list and updates the provider's `models` array and the `models.allowed` list.
3. **Set Default Model**: If no default model is set, picks the first available model from the synced list.

This ensures that the plan command always has access to the most up-to-date model information, and all models are routed through the user's TokenRouter provider.

---

## Dynamic Model Tier System

Model tiers are **not hardcoded**. On every `plan` invocation, the system:

1. Fetches the live price list from TokenRouter API.
2. Filters to well-known models (GPT, Claude, Gemini, DeepSeek, Llama, Qwen, Grok).
3. Computes each model's output price.
4. Sorts by price descending and splits into **3 equal buckets** (high / mid / low).
5. Picks the **median-priced model** from each bucket to avoid outliers.

| Tier | Role | Selection Rule |
|------|------|---------------|
| **tier1** (high) | Architect / Reasoning | Median of top-third by price |
| **tier2** (mid) | Coder / Drafter | Median of middle-third by price |
| **tier3** (low) | Reviewer / Quick tasks | Median of bottom-third by price |

If the API is unreachable or fewer than 3 known models are available, the system falls back to hardcoded defaults (claude-opus-4.6 / gpt-4o-mini / deepseek-v3.2).

---

## 6-Category Task Classification Engine

The `plan` command uses an enhanced classifier that supports **both Chinese and English** keywords. Tasks are scored against 6 categories; the highest-scoring category wins.

### Categories & Routing Pipelines

#### 1. Coding
**Keywords**: code, program, script, debug, function, api, database, app, test, bug, deploy, refactor, 代码, 编程, 脚本, 程序, 调试, 测试, 开发, 接口, 部署, 重构, 修复, 函数, 算法, 数据库, 前端, 后端, 全栈, 爬虫, 框架, 模块 ...

| Phase | Tier | Purpose | Artifact |
|-------|------|---------|----------|
| 1. Design | tier1 | Architecture | SPEC.md |
| 2. Code | tier2 | Implementation | code files |
| 3. Review | tier3 | Security check | AUDIT.md |

#### 2. Analysis
**Keywords**: analyze, compare, evaluate, research, report, data, statistics, 分析, 对比, 评估, 研究, 调研, 报告, 数据, 统计, 洞察, 指标, 复盘 ...

| Phase | Tier | Purpose | Artifact |
|-------|------|---------|----------|
| 1. Research | tier1 | Deep reasoning | RESEARCH.md |
| 2. Synthesize | tier2 | Summarization | REPORT.md |
| 3. Fact-check | tier3 | Verification | REVIEW.md |

#### 3. Writing
**Keywords**: write, article, blog, content, story, email, essay, documentation, 写作, 文章, 博客, 内容, 故事, 邮件, 文案, 文档, 稿件, 撰写, 起草 ...

| Phase | Tier | Purpose | Artifact |
|-------|------|---------|----------|
| 1. Outline | tier1 | Structure & strategy | OUTLINE.md |
| 2. Draft | tier2 | Content generation | DRAFT.md |
| 3. Polish | tier3 | Proofreading | RESULT.md |

#### 4. Creative
**Keywords**: creative, brainstorm, idea, design, logo, prototype, 创意, 头脑风暴, 点子, 设计, 艺术, 原型, 线框图, 灵感, 构思 ...

| Phase | Tier | Purpose | Artifact |
|-------|------|---------|----------|
| 1. Ideate | tier1 | Creative thinking | IDEAS.md |
| 2. Execute | tier2 | Production | RESULT.md |

#### 5. Translation
**Keywords**: translate, localize, interpretation, 翻译, 本地化, 国际化, 多语言, 中译英, 英译中 ...

| Phase | Tier | Purpose | Artifact |
|-------|------|---------|----------|
| 1. Translate | tier2 | Language conversion | TRANSLATION.md |
| 2. Review | tier3 | Quality check | RESULT.md |

#### 6. Simple
**Keywords**: simple, quick, summarize, list, count, define, explain, 简单, 快速, 总结, 列出, 计数, 查询, 定义, 解释, 概括 ...

| Phase | Tier | Purpose | Artifact |
|-------|------|---------|----------|
| 1. Execute | tier3 | Direct completion | RESULT.md |

### Cost Savings by Category

| Category | Phases | Tiers Used | Typical Savings |
|----------|--------|------------|-----------------|
| **Coding** | 3 | tier1 + tier2 + tier3 | ~54% |
| **Analysis** | 3 | tier1 + tier2 + tier3 | ~54% |
| **Writing** | 3 | tier1 + tier2 + tier3 | ~54% |
| **Creative** | 2 | tier1 + tier2 | ~33% |
| **Translation** | 2 | tier2 + tier3 | ~81% |
| **Simple** | 1 | tier3 only | ~95% |

---

## Multi-Agent Routing Guidance

When the user's task is complex (e.g., building an application, designing a system, multi-step workflows), **proactively suggest** multi-agent routing:

1. **Identify complexity** — If the task involves multiple phases, recommend running `plan`.
2. **Show the pricing** — Run `list` to display the full price list.
3. **Run the planner** — Run `plan "<task>"` to show the recommended routing with projected savings.
4. **Offer to enable models** — Ask the user if they want to enable the recommended models as fallbacks.

**Example prompt to user:**
> Your task involves multiple phases. Let me run the planner to find the optimal routing:
> ```
> build a REST API with authentication / 帮我构建一个REST API的鉴权功能
> ```
> The planner will automatically pick the best models for each phase based on current pricing and show projected savings.

---

## Quick Start

```
# Step 1: Check if TokenRouter is configured
check

# Step 2: If not configured, set it up (agent does this with user-provided credentials)
setup --name tokenrouter --base-url https://open.palebluedot.ai/v1 --api-key sk-xxx...

# Step 3: Verify and sync all models
check
sync

# List all models with real-time pricing
list / 列出TokenRouter的模型价格列表

# Get routing recommendations for a task (Chinese or English)
# NOTE: This will automatically sync models before planning
write a Python script
帮我开发一个用户管理后端接口
analyze and compare the data reports of three competing products
把这段中译英

# Enable a model by index or name
enable 1
enable openai/gpt-4o-mini

# Generate execution plan for host agent to dispatch sub-agents
build a todo app
```

---

## Core Functions

### 1. `check` - Verify Provider Configuration
```
check / 检查TokenRouter配置
```
Verifies that a TokenRouter provider (baseUrl containing `https://open.palebluedot.ai`) exists in the config. Displays provider details if found, or guides the user to set up if not.

### 2. `setup` - Write Provider Configuration
```
setup --name tokenrouter --base-url https://open.palebluedot.ai/v1 --api-key <key>
```
Writes the TokenRouter provider into `~/.openclaw/openclaw.json` (with automatic backup). The agent uses this command after the user provides their credentials from PaleBlueDot AI. **The agent must never use placeholder API keys** — only real credentials provided by the user.

### 3. `sync` - Fetch & Sync All Models
```
sync / 同步TokenRouter模型
```
Fetches all available models from the TokenRouter API, adds them to the provider's `models` array and the `models.allowed` list. All models are routed through the configured TokenRouter provider. This is automatically called before `plan`.

### 4. `list` - Real-Time Model Pricing
```
list / 列出模型的价格列表
```
Fetches current TokenRouter pricing and displays all available models with input/output/cache prices.

### 5. `plan` - Smart Task Routing
```
plan "<task description>" / 计划 "<任务描述>"
plan "<task description>" --execute / 计划 "<任务描述>" 并执行
```
Classifies the task, builds a multi-phase pipeline, assigns dynamic model tiers, and shows projected savings. Automatically syncs models before planning. Add `--execute` (or `-x`) to generate a structured JSON execution plan (`swarm_plan.json`) that the host agent uses to dispatch sub-agents via the internal `sessions_spawn` API.

**How `--execute` works:**

The `--execute` flag does NOT call sub-agents directly via CLI. Instead, it outputs a JSON plan to `~/.openclaw/workspace/swarm_plan.json` and to stdout. The host agent (OpenClaw) reads this plan and dispatches sub-agents internally using `sessions_spawn`. Each step in the plan contains:
- `model`: which model to use for this phase
- `system_prompt`: the role prompt for the sub-agent
- `task_prompt`: the task instruction
- `expected_artifact`: the file the sub-agent should produce
- `max_retries` and `timeout_seconds`: retry and timeout policy

Steps must be executed sequentially — each step's artifact is context for the next.

### 6. `enable` - Auto-Configuration
```
enable 1                    # Enable model by index
enable openai/gpt-4o-mini   # Enable by name
启用 1
启用 openai/gpt-4o-mini
```
Writes the model directly into `~/.openclaw/openclaw.json` (with automatic backup).

---

## Adaptive Stability Fallback

The system tracks historical model performance via `swarm_memory.json` and `swarm_insights.json`:

- **Tier selection**: If a tier2/tier3 model's historical success rate drops below **50%**, it is automatically replaced by the tier1 model for that phase during plan generation.
- **Retry policy**: The generated execution plan specifies `max_retries: 2` per step. The host agent should inject the error context into the retry prompt when re-dispatching a failed step.
- **Logging**: The host agent should append execution results to `swarm_memory.json`. Run `consolidate_memory.py` to generate performance insights for future adaptation.

---

## Advanced Usage

### Custom Routing Rules

You can override the dynamic tier selection for specific categories by creating `~/.openclaw/model-routing.json`. Each category maps to an **ordered list of model IDs**, one per phase (matching the pipeline order). An optional `"fallback"` model is used for any phase without an explicit override.

```json
// ~/.openclaw/model-routing.json
{
  "coding": [
    "anthropic/claude-opus-4.6",
    "openai/gpt-4o-mini",
    "deepseek/deepseek-v3.2"
  ],
  "analysis": [
    "google/gemini-3-pro-preview",
    "anthropic/claude-sonnet-4.6",
    "deepseek/deepseek-v3.2"
  ],
  "writing": [
    "anthropic/claude-opus-4.6",
    "openai/gpt-4o",
    "openai/gpt-4o-mini"
  ],
  "creative": [
    "anthropic/claude-opus-4.6",
    "openai/gpt-4o"
  ],
  "translation": [
    "openai/gpt-4o",
    "deepseek/deepseek-v3.2"
  ],
  "simple": [
    "deepseek/deepseek-v3.2"
  ],
  "fallback": "openai/gpt-4o-mini"
}
```

**How it works:**
- The list index corresponds to the phase order in each category's pipeline (e.g., for coding: index 0 = Design, 1 = Code, 2 = Review).
- If a category is not listed, the default dynamic tier selection applies.
- If the list is shorter than the number of phases, remaining phases use `"fallback"` (if set) or the default tier.
- If the file does not exist, the system uses fully dynamic tier selection.
