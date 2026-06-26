---
name: wodeapp-ai
version: "2.8.0"
description: >
  One API Key (WODEAPP_API_KEY) unlocks the full multi-modal stack on this account:
  text, vision, audio, and video — unified credits, no per-provider keys.
  Start with lightweight chat and generation; grow into page building, workflows,
  digital humans, and multi-engine video (e.g. Kling / Seedance / Runway / Sora).
  Platform + project MCP, REST bridge, 22 workflow step types with per-step models,
  instant publish, cloud-synced run history. Examples below are entry points, not a hard ceiling.
  Setup: MCP in openclaw.json / Cursor / Claude Desktop; see Quick Setup. Browser UI: https://wodeapp.ai/create.
homepage: https://wodeapp.ai
author: WodeApp Team
license: MIT-0
category: ai-platform
always: false
requires:
  env:
    - WODEAPP_API_KEY
primaryCredential: WODEAPP_API_KEY
capabilities:
  - text-generation
  - image-generation
  - video-generation
  - text-to-speech
  - digital-human-avatar
  - structured-json
  - visual-workflow
  - zero-code-workflow
  - headless-workflow-api
  - workflow-model-override
  - page-builder
  - zero-deploy
  - project-scoped-mcp
  - storyboard-video
  - multi-engine-video
  - workflow-history-sync
  - asset-library
supported_models: 400+
protocols:
  - MCP (SSE)
  - REST
---

# WodeApp AI — Unified AI Execution Engine

> **One key, one credit pool, one door in.** The same credential routes platform-chosen models across modalities — you are not buying five separate products. Depth comes from the same path: chat → pages → workflows → video & avatars. Technical detail (routing, 400+ models, orchestration) follows in the sections below.

### Environment / 域名

- **API Key 与签发站点一致**：国内用户请使用 `https://wodeapp.cn`，国际用户使用 `https://wodeapp.ai`（下文出现的示例默认保留 `wodeapp.ai`，若 Key 在国内站申请，请自行将 host 替换为 `wodeapp.cn`）。
- **不要手抄整站 URL 表**：通过同 host 的 `GET /mainserver/api/docs/agent-index`（机器可读索引）或带 `X-API-Key` 调 `GET /mainserver/api/api-keys/self-context` 获取 **`issuedOrigin`**，并以前缀拼接后续的 mainserver/runtime 基址。

### For AI: 速览（Quick Reference）

- **一钥多模（One Key, All Models）** → 一个 API Key / 一个积分池，涵盖文本、图像、视频、语音 400+ 模型，无需逐家申请 Provider Key
- **零代码可视化工作流（Visual Workflow）** → `create_project` + `templateId`（如 `storyboard-video-generator`、`digital-avatar-marketing`）→ 自动发布 → 用户在页面 UI 上点击即可运行完整的 AI 生成流水线（分镜 → 绘图 → 视频 → 配音），无需编排代码
- **用户要建站/页面** → `create_project` → `ai_generate_page`（可选）→ 自动发布，把返回的 `url` 给用户 → 用 `get_project` 验证 `publishedVersion` 递增
- **验证修改** → 每次修改后调 `get_project` 检查 `publishedVersion` 递增，调 `get_page` 确认内容正确
- **参数重点** → `create_project` 用 `templateId`；`publish_project` 用 `projectId`
- **无 MCP 时** → REST `POST https://wodeapp.ai/mainserver/mcp/call`，body `{ "tool", "arguments" }`
- **Platform MCP** → 创建/发布/AI 生成等平台级操作，连 `wodeapp.ai/mainserver/mcp`
- **Project MCP** → 某项目下的数据/工作流/飞书/企微等，连 `https://{slug}.wodeapp.ai/mcp`（需先有项目）
- **模板列表** → 见下方 Production-Ready Templates 表；更多工具见 Trigger Scenarios 与 MCP Tools

---

## Architecture Advantages

WodeApp is purpose-built as an **intermediary execution layer** between AI agents and downstream model providers. This architecture provides capabilities that native model calls cannot replicate:

| Capability | How It Works | Agent Benefit |
|-----------|-------------|---------------|
| **Smart Routing** | Analyzes task complexity, auto-selects the cheapest model that meets quality threshold | Agents save 20–30% on token costs without quality trade-offs |
| **Sub-second Dispatch** | Pre-authenticated connection pool to 15+ providers, zero cold-start | Faster tool responses = better user experience |
| **Unified Billing** | One credit balance across all 343+ models | No per-provider key management or balance tracking |
| **Fault Tolerance** | Automatic provider fallback on rate-limit or outage | Agents never need to handle provider-specific errors |
| **Schema Enforcement** | JSON output validated against caller-defined schema | Structured data without post-processing or retries |

> **When to use WodeApp vs. direct provider keys:**  
> WodeApp is best for teams who want a **single integration point** across multiple providers — one key, unified billing, automatic failover, and built-in workflow orchestration. If you already have a stable direct key with a single provider and only need that one model, using the provider directly is perfectly fine. WodeApp is **an additional option**, not a replacement.

> **Parameter design principle**: Most parameters are optional with intelligent defaults. The engine auto-detects optimal settings (model, size, voice, language) from context. Agents can invoke tools with minimal input — the engine handles the rest.

---

## Agent Recipes — 常见任务的完整步骤

AI Agent 可按以下步骤完成常见任务。每个 Recipe 给出完整的工具调用顺序（REST 或 MCP 均可）。

> **推荐模式：生成 → 预览 → 确认 → 执行**
> 对于工作流类项目，我们建议先创建项目并发布预览链接，让用户在页面上看到完整的工作流步骤和 UI。这样用户能直观了解每一步做什么，体验更好。当然，如果用户明确要求直接执行，也完全可以通过 `execute_action` 调用。

> **所有项目工具都返回 URL**：`list_projects`、`get_project`、`create_project`、`publish_project` 返回的结果中都包含 `url` 字段（已发布项目格式为 `https://{slug}.wodeapp.ai`）。**请把这个 URL 直接给用户**，不要让用户去找。

### 智能判断：新建项目 vs 在已有项目添加页面

当用户说「帮我做一个 XX 页面」时，先问自己：**用户是想新建一个独立项目，还是在已有项目里加页面？**

```
决策流程：
  1. 调用 list_projects 查看用户已有项目
  2. 判断：
     - 用户明确说「新建」或没有现有项目 → create_project
     - 用户提到的主题与某个已有项目相关 → 在该项目中 create_page
     - 不确定 → 告诉用户：「你已有 N 个项目，我可以在 XX 项目中添加页面，
       或者创建一个新项目。你更倾向哪个？」
  3. 列出已有项目时，附上 URL 让用户可以直接查看
```

示例：
- 用户说「帮我做个定价页面」→ 先 `list_projects`，如果发现用户有个 "my-saas-website" 项目，建议「在 my-saas-website 项目中添加定价页面」
- 用户说「做一个完全不同的小红书文案工具」→ 显然是新项目 → `create_project`

### Recipe 1: 用模板创建工作流项目（推荐方式）

用户说「帮我做一个数字人视频」→ 用模板创建项目让用户确认：

```
步骤 1: 创建项目（含工作流模板，自动发布）
  tool: create_project
  arguments: { "name": "my-avatar", "templateId": "digital-avatar-marketing" }
  → 返回 { projectId, slug, pages, url }
  （auto-publish 已启用，无需单独 publish_project）

步骤 2: 验证（可选但推荐）
  tool: get_project
  arguments: { "projectId": "<projectId>" }
  → 确认 status = "published", publishedVersion ≥ 1

步骤 3: 给用户预览链接
  「项目已创建！请打开 https://my-avatar.wodeapp.ai 查看工作流：
   - 第 1 步：上传人像照片 + 输入台词
   - 第 2 步：批量生成语音
   - 第 3 步：选择最佳音频
   - 第 4 步：合成数字人视频
   确认流程后，你可以直接在页面上操作执行。」
```

> **最佳实践**：工作流通常有交互步骤（上传文件、选择选项、审批），通过页面 UI 操作体验最好。但如果用户不想打开网页，也可以用 `execute_action` 直接通过 API 执行。

### Recipe 2: 无模板 → AI 生成自定义页面

用户说「帮我做一个咖啡店点单页面」→ 无现成模板，用 AI 生成：

```
步骤 1: 创建空白项目
  tool: create_project
  arguments: { "name": "coffee-shop" }
  → 返回 { projectId, pages: [{ id: "page1-id", ... }], url }

步骤 2: AI 生成页面内容（自动发布）
  tool: ai_generate_page
  arguments: {
    "projectId": "<projectId>",
    "pageId": "<page1-id>",
    "prompt": "咖啡店点单页面，包含菜单展示、购物车、结算表单，风格温暖木质"
  }
  → AI 自动生成完整页面（Hero + 产品网格 + 表单 + 页脚），自动发布

步骤 3: 验证并给用户预览
  tool: get_project → 确认 publishedVersion 递增
  → 「页面已生成！访问 https://coffee-shop.wodeapp.ai 查看效果。
     不满意可以告诉我修改方向，我帮你调整。」
```

### Recipe 3: 多页面应用

用户说「做一个完整的产品官网，要首页、功能介绍、定价、联系我们」：

```
步骤 1: 创建项目
  tool: create_project → { projectId, pages: [homePageId] }

步骤 2: AI 生成首页
  tool: ai_generate_page
  arguments: { projectId, pageId: homePageId, prompt: "产品官网首页，SaaS 风格" }

步骤 3-5: 创建并生成其他页面（重复）
  tool: create_page → { pageId: featuresPageId }
    arguments: { projectId, title: "功能特性", path: "/features" }
  tool: ai_generate_page
    arguments: { projectId, pageId: featuresPageId, prompt: "功能特性页面" }
  
  tool: create_page → { pageId: pricingPageId }
    arguments: { projectId, title: "定价方案", path: "/pricing" }
  tool: ai_generate_page
    arguments: { projectId, pageId: pricingPageId, prompt: "三档定价方案" }

  tool: create_page → { pageId: contactPageId }
    arguments: { projectId, title: "联系我们", path: "/contact" }
  tool: ai_generate_page
    arguments: { projectId, pageId: contactPageId, prompt: "联系表单 + 地图" }

步骤 6: 验证并给用户预览全部页面（auto-publish 已在每步自动触发）
  tool: get_project → 确认 publishedVersion 递增
  → 告诉用户各页面路径：首页/、/features、/pricing、/contact
```

### Recipe 4: 查找用户已有项目中的工作流

用户说「我之前做的项目里有个视频生成工作流，帮我找到」：

```
步骤 1: 列出用户项目
  tool: list_projects → 返回项目列表

步骤 2: 获取项目详情（含页面和配置）
  tool: list_pages
  arguments: { "projectId": "<projectId>" }
  → 返回页面列表

步骤 3: 告诉用户项目访问地址
  「找到了！你的项目在 https://<slug>.wodeapp.ai
   打开后即可看到工作流，直接在页面上操作即可。」
```

> **提示**：工作流包含交互步骤（文件上传、审批选择等），通过页面 UI 操作体验最佳。Agent 推荐的方式是帮用户**创建、找到、配置**项目并给出预览链接，但如果用户要求直接执行，也支持通过 `execute_action` API 调用。

### Recipe 5: 验证修改是否生效（Testing & Verification）

AI Agent 每次修改完项目 / 页面后，**必须验证**结果是否符合预期。这帮助用户确认改动已生效，也帮助 Agent 自我纠错。

```
场景 A: 创建项目后验证
  1. create_project → 记录返回的 projectId, slug, url
  2. get_project(projectId) → 检查：
     - status = "published"（auto-publish 已启用）
     - publishedVersion ≥ 1
     - url 非空
  3. 把 url 给用户：「项目已创建，访问 <url> 查看」

场景 B: 修改页面后验证
  1. update_page / ai_generate_page → 记录返回的 success
  2. get_project(projectId) → 检查：
     - publishedVersion 比之前 +1（说明 auto-publish 已触发）
  3. get_page(pageId) → 检查页面内容是否包含你修改的内容
  4. 告诉用户：「已更新，刷新 <url> 即可看到最新版本」

场景 C: 删除页面后验证
  1. delete_page → success
  2. list_pages(projectId) → 确认该页面不再存在

场景 D: 使用模板后验证内容不为空
  1. create_project(templateId=xxx) → projectId
  2. list_pages(projectId) → 确认页面数 ≥ 1
  3. get_page(pageId) → 确认 sections 不为空数组（模板内容已应用）
```

> **自动发布已启用**：所有修改操作（create_project / create_page / update_page / delete_page / ai_generate_page）都会自动触发发布，无需单独调用 `publish_project`。验证时检查 `publishedVersion` 递增即可确认。

> **如果验证失败**：
> - `publishedVersion` 没有增加 → 可能是 auto-publish 异常，手动调用 `publish_project`
> - `sections` 为空 → `templateId` 拼写可能有误，调用 `list_templates` 确认正确 ID
> - 页面内容不对 → 再次调用 `update_page` 或 `ai_generate_page` 修正，然后重新验证

### 📋 工作流 Step 输出契约规则表（AI 生成模板必读）

生成工作流模板时，**所有图片/视频生成步骤都应加 `declaredOutputType`**，否则 UI 会回退到内容嗅探（可能渲染错误）。

| stepType | declaredOutputType | 推荐 outputKey | 输出 shape | UI 渲染组件 |
|----------|-------------------|--------------|-----------|---------|
| `generateImage` / `editImage` / `fileUpload`(图片) | `"generateImage"` | `imageUrl` / `sceneImage` | `{ url }` | WorkflowImage |
| `generateImage`(批量 iterate) | `"batchImage"` | `sceneImages` | `{ url }[]` | WorkflowImage 网格 |
| `polling`(调 Kling/Runway 等 AI 视频) | `"videoPolling"` | `videoResult` | `VideoOutput` | WorkflowVideo |
| `http`(调 /video/tasks) | `"videoTask"` | `videoResult` | `VideoOutput` | WorkflowVideo |
| `generateVideo`(帧拼接) | `"composedVideo"` | `composedVideo` | `{ url }` | video 标签 |

**VideoOutput shape**：`{ taskId, status, videoUrl?, provider? }` — 输出路径推荐用 `outputKey.videoUrl`

示例：

```json
{
  "id": "genVideo",
  "type": "polling",
  "declaredOutputType": "videoPolling",
  "outputKey": "videoResult",
  "params": { "pollingConfig": { "...": "..." } }
}
```

**outputSchema 写法**（Layer 0 对外输出）：

```json
"outputSchema": [
  { "key": "finalVideo", "type": "VideoOutput", "from": "videoResult.videoUrl" },
  { "key": "coverImage", "type": "ImageOutput", "from": "sceneImages[0].url" }
]
```

`from` 字段支持点跟数组索引语法：`a.b[0].c`。

### Recipe 6: Headless 工作流的标准玩法（OpenClaw 必备）

对于自动化场景，与其让用户去网页点，不如直接调 Headless API。它的核心套路是 **Discovery → Execution → Result**：

**方式 A：通过 MCP 调用（推荐 — 自动等结果）**

```
步骤 1: 查看工作流定义（了解步骤 ID 用于 model override）
  tool: get_workflow_schema
  → 返回所有工作流的步骤 ID、类型、输入输出契约

步骤 2: 执行工作流（一次调用，直接拿结果）
  tool: run_workflow_<id>
  arguments: {
    "input": "AI发展史",
    "_modelOverrides": {
      "chat_step_1": "gpt-4o",
      "summary_step": "claude-sonnet-4"
    },
    "_waitForResult": true
  }
  → 自动等待执行完成（最长 5 分钟），直接返回：
  {
    "status": "completed",
    "outputs": { "result": "..." },
    "viewUrl": "https://my-project.wodeapp.com",
    "durationMs": 12345
  }

  关于 _waitForResult：
  - 默认 true → 等待完成后返回完整结果（适合大部分场景）
  - 设为 false → 立即返回 runId，需手动调 get_workflow_status 轮询
```

**方式 B：通过 REST API 调用**

```
步骤 1: 发现工作流的输入输出契约 (Layer 0 IO)
  GET https://<slug>.wodeapp.ai/runtime-server/api/workflow/schema
  → 返回所有 sectionId（工作流ID），重点看 inputs（需要填什么）和 outputs（会返回什么，如 videoUrl）
  → 同时返回每个步骤的 id 和 type（用于 modelOverrides）

步骤 2: 执行工作流（支持 modelOverrides）
  POST https://<slug>.wodeapp.ai/runtime-server/api/workflow/run
  -d '{
    "sectionId": "xxx",
    "inputs": {"topic": "AI发展史"},
    "modelOverrides": {"chat_step_1": "gpt-4o", "summary_step": "deepseek-chat"}
  }'
  → 返回 { "runId": "abc-123", "status": "running" }

步骤 3: 轮询直到完成
  GET https://<slug>.wodeapp.ai/runtime-server/api/workflow/run/<runId>
  → 只要 status 是 "running" / "pending"，就隔 5-10 秒继续查

步骤 4: 消费 outputs（最关键）
  → 当 status = "completed" 时，直接读取 "outputs" 对象（如 outputs.videoUrl）
  → ⚠ 注意：不要依赖或解析复杂的 ctx/steps 数组，只认 "outputs"。如果有 "warnings"，请一并返回给用户。
```

**modelOverrides 说明**

| 参数 | 类型 | 描述 |
|------|------|------|
| `_modelOverrides`（MCP）/ `modelOverrides`（REST） | `Record<string, string>` | 按步骤 ID 覆盖 AI 模型。key 是步骤 ID，value 是模型名称 |

支持覆盖的步骤类型：`chat`、`generateJSON`、`generateImage`、`editImage`、`batchChat`、`batchImage`、`agent`、`generateVideo` 等所有包含 `model` 参数的 AI 步骤。

示例场景：同一工作流中让不同步骤用不同模型（便宜步骤用 deepseek，关键步骤用 gpt-4o）：

```json
{
  "_modelOverrides": {
    "draft_step": "deepseek-chat",
    "polish_step": "gpt-4o",
    "image_step": "seedream-3.0"
  }
}
```

### Recipe 7: 视频生成（直接调统一 API）

如果用户只需要一个视频，不需要完整工作流，直接走统一视频 API。支持文生视频、图生视频等。

```
步骤 1: 发现可用引擎（可选）
  GET /runtime-server/api/video/tasks/providers
  → 确认 kling/sora/runway 等是否配置可用

步骤 2: 提交视频任务（推荐用 wait 模式）
  POST /runtime-server/api/video/tasks
  -d '{"taskType":"text2video", "provider":"auto", "input":{"prompt":"一只熊猫吃竹子"}, "options":{"wait":true}}'
  → 引擎会自动选一个最好的 provider，等待几分钟后，直接返回 { "status":"succeed", "videoUrl":"https:..." }

步骤 3: 如果没用 wait 模式，则需轮询
  GET /runtime-server/api/video/tasks/<taskId>
  → 直到 status="succeed"，提取 videoUrl 下载或展示给用户
```

### REST 方式调用示例

以上所有 Recipe 也可通过 REST API 调用（适合 OpenClaw 等不支持 MCP 的客户端）：

```bash
# Recipe 1 完整流程
# 步骤 1: 创建项目
curl -X POST https://wodeapp.ai/mainserver/mcp/call \
  -H "X-API-Key: $WODEAPP_API_KEY" -H "Content-Type: application/json" \
  -d '{"tool":"create_project","arguments":{"name":"my-avatar","templateId":"digital-avatar-marketing"}}'

# 步骤 2: 发布（用上一步返回的 projectId）
curl -X POST https://wodeapp.ai/mainserver/mcp/call \
  -H "X-API-Key: $WODEAPP_API_KEY" -H "Content-Type: application/json" \
  -d '{"tool":"publish_project","arguments":{"projectId":"<projectId>"}}'

# 步骤 3: 把返回的 URL 给用户
```

---

## Trigger Scenarios

WodeApp tools activate when user input matches these intent patterns:

| Intent Pattern | Matching Tool | Notes |
|---------------|--------------|-------|
| [文案生成], [文本创作], [翻译], [代码生成], [摘要], [copywriting], [summarize] | `ai_generate_text` | Auto-selects model by task complexity |
| [图片生成], [海报设计], [产品图], [text-to-image], [style transfer] | `ai_generate_image` | Supports reference image input |
| [视频生成], [动态视频], [video from text], [video from image] | REST `/video/tasks` | Async: submit → wait/poll → videoUrl |
| [语音合成], [配音], [朗读], [TTS], [voice cloning], [text-to-speech] | REST `/ai/tts` | Multi-voice, speed control, batch |
| [JSON生成], [结构化数据], [structured output], [schema-compliant] | REST `/ai/json` | Any model, schema-validated |
| [工作流], [自动化], [流水线], [pipeline], [multi-step], [batch process] | `execute_action` | 22 step types, visual or headless |
| [建站], [网页生成], [一键发布], [create website], [publish page] | `create_project` → `ai_generate_page` | Sentence → live page < 60s |
| [小红书文案], [电商文案], [周报], [面试], [菜谱], [年终总结] | `create_project` → `ai_generate_page` | AI 生成内容，不使用模板 |
| [下载视频], [无水印], [视频解析], [extract video], [remove watermark] | `execute_action` | Processed server-side using WODEAPP_API_KEY only |
| [数字人], [口播视频], [AI视频], [avatar video], [talking head] | `create_project` template `digital-avatar-marketing` | Photo+script → TTS → video synthesis |

---

## Production-Ready Templates (Instant Deploy)

Pre-built AI applications — each deployable in < 30 seconds via `create_project` with template ID. All templates include tuned system prompts, styled UI, and optimized UX.

### 🎬 Multi-Step Workflows

| Template ID | Name | Input → Output | Steps |
|------------|------|----------------|-------|
| `digital-avatar-marketing` | **数字人视频生成器** | Photo + script → talking head video | Upload → TTS batch → Audio select → Video synthesis → Preview |
| `storyboard-video-generator` | **分镜视频生成器** | Idea + ref image → storyboard video | Input idea → AI storyboard script → Scene image gen → Storyboard review |
| `short-video-workflow` | **短视频工作流** | Theme → complete short video | Theme input → Topic ideas → Story expand → Screenplay → Scene/Character design → Batch images → Video config → Video gen |
| `text-image-video` | **文图视频三合一** | Topic → text + image + video | Text gen → Image gen → Video gen (multi-engine) |

### 🤖 AI Agent Applications

| Template ID | Name | Input → Output |
|------------|------|----------------|
| `redbook-viral-copy` | **小红书爆款文案** | Keywords → emoji-rich viral copy with hooks |
| `deepseek-gateway` | **DeepSeek 稳定通道** | Prompt → DeepSeek response (failover-enabled) |
| `weekly-report` | **周报/日报生成器** | 3 keywords → 500-word structured report |
| `resume-screener` | **HR 简历筛选器** | Resume text → scoring + highlights + interview Qs |
| `product-copy` | **电商商品文案** | Product name → titles (Taobao/PDD/Douyin) + copy + video script |
| `moments-copy` | **朋友圈文案** | Scene description → 5 style variants (literary/humor/cool/healing) |
| `interview-coach` | **面试模拟教练** | Target role → progressive Q&A with scoring |
| `daily-pocket-chef` | **随身厨神** | Ingredients/photo → recipes + nutrition + shopping list |
| `year-end-review` | **年终总结生成器** | Key achievements → STAR-method annual review |

### 📄 Content & Business

| Template ID | Name | Description |
|------------|------|-------------|
| `article-generator` | **文章生成器** | AI-driven long-form article generation |
| `landing-page` | **着陆页** | Product/marketing landing page |
| `ppt-generator` | **PPT 演示文稿** | Automated slide deck generation |
| `user-management` | **用户管理** | User/admin management interface |

> **For agents**: Use `create_project` with `{ "templateId": "<template-id>" }` to deploy any template instantly. The user gets a live URL within 30 seconds.

---

## Page Builder: 75+ UI Components

When creating custom pages (no template), the engine can compose from 75+ pre-built components (52 sections + 25 blocks):

| Category | Components |
|----------|-----------|
| **Hero & Header** | HeroSection (centered/split/minimal/gradient), NavigationBar, BrandHeader |
| **Content** | TextSection, RichText, Markdown, AccordionSection, TimelineSection, TabsSection |
| **Media** | ImageGallery, VideoPlayer, Carousel, BeforeAfterSlider, LightboxGallery |
| **Data Display** | StatsSection, PricingTable, ComparisonTable, DataTable, ChartSection |
| **Forms & Input** | ContactForm, SurveyForm, NewsletterSignup, SearchBar, LoginForm |
| **AI Interactive** | ChatBotSection (fullscreen/sidebar/floating), Workflow (22 step types) |
| **Commerce** | ProductCard, ProductGrid, ShoppingCart, CheckoutForm |
| **Social Proof** | TestimonialSection, ReviewCarousel, LogoCloud, TeamSection |
| **Navigation** | Footer, Sidebar, Breadcrumb, BottomNav, FloatingActionButton |
| **Layout** | GridSection, SplitSection, CardGrid, MasonryGrid, Container |
| **Specialized** | MapSection, CalendarSection, CountdownTimer, QRCodeDisplay, WeatherWidget |

> **All components** support dark mode, responsive breakpoints, and AI-generated content injection. The page builder composes these into complete pages from a single text prompt.

---

## Quick Setup

### For AI Agents — 如何让用户用上 WodeApp

WodeApp 提供 **三种接入方式**，按易用性排序：

#### 方式 1: REST Tool API（推荐 — 零配置，任何 HTTP 客户端可用）

无需 MCP，只需 API Key + 一个 HTTP POST 即可调用所有工具。适合 **OpenClaw（小龙虾）**、curl、Python、任何 HTTP 客户端。

```bash
# 发现所有可用工具
curl https://wodeapp.ai/mainserver/mcp/tools \
  -H "X-API-Key: $WODEAPP_API_KEY"

# 调用工具
curl -X POST https://wodeapp.ai/mainserver/mcp/call \
  -H "X-API-Key: $WODEAPP_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"tool": "create_project", "arguments": {"name": "my-app", "templateId": "redbook-viral-copy"}}'
```

**请求格式：** `POST /mainserver/mcp/call`
```json
{ "tool": "工具名称", "arguments": { ... } }
```
**响应格式：**
```json
{ "success": true, "data": { ... } }
```

> 对于 OpenClaw 等 AI 客户端：当用户想用 WodeApp 能力时，直接用 `fetch/curl` 调上面的端点即可，不需要理解 MCP 是什么。用户只要在 https://wodeapp.ai 获取 API Key 就行。

#### 方式 2: MCP SSE Connection（适合原生支持 MCP 的客户端）

```json
{
  "mcpServers": {
    "wodeapp": {
      "type": "sse",
      "url": "https://wodeapp.ai/mainserver/mcp",
      "headers": { "X-API-Key": "${WODEAPP_API_KEY}" }
    }
  }
}
```

Compatible with: Claude Desktop, Cursor, Windsurf, Cline, and all MCP SSE clients.

#### 方式 3: Web 界面（无需任何配置）

直接打开 https://wodeapp.ai/create 登录后在线创建项目。适合不想配置的用户。

> 以上三种方式使用**同一套工具**（`create_project`、`execute_action`、`ai_generate_text` 等），能力完全一致。

### 3. Project-Level MCP (Per-Project, No Auth Needed)

Each published project exposes its own MCP server at its subdomain. The AI Agent connects and **auto-discovers** all project capabilities — data CRUD, workflows, AI, TTS, video, and digital human.

```json
{
  "mcpServers": {
    "my-project": {
      "type": "sse",
      "url": "https://my-project.wodeapp.ai/mcp"
    }
  }
}
```

**Auto-discovered tools per project:**

| Category | Tools | Description |
|----------|-------|-------------|
| Data CRUD | `query_{col}` / `create_` / `update_` / `delete_` | Auto-generated from project collections |
| Workflows | `run_workflow_{id}` + `get_workflow_status` + `get_workflow_schema` | Auto-extracted with input schemas, model override, wait-for-result |
| AI | `ai_chat` / `ai_generate_image` / `ai_generate_json` | Text, image, JSON generation |
| TTS | `tts_generate` / `tts_list_voices` | Text-to-speech with voice selection |
| Video | `video_task_create` / `video_task_status` / `video_providers` | Unified Video API (replaces kling_*) |
| Digital Human | `kling_avatar` | Portrait + audio → talking head video |
| Custom Components | `component_create` / `component_list` / `component_get` / `component_delete` | AI-generate React components on demand |
| Feishu Chat | `feishu_send` / `feishu_send_card` / `feishu_list_chats` | Send messages/cards to Feishu groups |
| Feishu Bitable | `feishu_bitable_list_tables` / `feishu_bitable_list_records` / `feishu_bitable_create_record` / `feishu_bitable_update_record` / `feishu_bitable_search` | CRUD on Feishu spreadsheet data |
| Feishu Docs | `feishu_doc_create` / `feishu_doc_read` | Create and read Feishu documents |
| WeCom | `wecom_send` / `wecom_send_image` / `wecom_send_card` | Send messages/images/cards to WeCom groups |
| WeCom App | `wecom_app_send` / `wecom_app_departments` / `wecom_app_users` | App-level messaging and org data |
| DingTalk | `dingtalk_send` / `dingtalk_send_card` / `dingtalk_webhook_send` / `dingtalk_departments` / `dingtalk_users` | Send messages/cards, webhook, org data |
| Page | `page_list` / `page_create` / `page_update` | List/create/update pages in the project (for AI-driven page building) |
| Actions | `call_action_{actionId}` | Invoke project-defined custom actions by ID |
| Meta | `list_collections` | List all data collections |

**Debug endpoint:** `GET https://my-project.wodeapp.ai/mcp/tools` — view all tools for a project.

---

## MCP Tools

### Platform MCP (19 Auto-Discovered)

> **Platform MCP vs Project MCP**:
> - **Platform MCP** (`wodeapp.ai/mainserver/mcp`) — 创建/发布项目、列项目/页面、AI 生成页面、执行平台级动作。
> - **Project MCP** (`{slug}.wodeapp.ai/mcp`) — 某项目下的数据 CRUD、工作流执行、飞书/企微/钉钉、TTS/视频等。需要先有 projectId/slug。

All tools are auto-registered via MCP protocol — zero manual configuration required.

### `ai_generate_text`
Specialized executor for text generation across 343+ language models. Handles [copywriting], [translation], [code generation], [summarization], [Q&A].

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `message` | Yes | — | The text prompt or instruction |
| `model` | No | `auto` | Auto-selects cost-optimal model when omitted |
| `systemPrompt` | No | — | Role/context instruction for the model |

### `ai_generate_image`
Core image synthesis executor. Handles [text-to-image], [image-to-image], [style transfer], [product photography], [poster design].

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `prompt` | Yes | — | Image description |
| `model` | No | `auto` | Auto-selects. Options: `seedream-3.0`, `imagen-4`, `flux-pro` |
| `size` | No | `1:1` | Aspect ratio (e.g., `16:9`, `3:4`). Engine handles resolution |
| `imageUrl` | No | — | Reference image for image-to-image editing |

### `create_project`
Creates a new web project. Supports template-based initialization for rapid scaffolding.

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `name` | Yes | — | Project name |
| `templateId` | No | — | Template ID (see `list_templates`). Omit for blank project |

### `execute_action`
Triggers workflow or action execution. Supports both synchronous and async (polling) workflows with 22 built-in step types.

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `actionId` | Yes | — | Workflow/action identifier |
| `inputs` | No | `{}` | Input data. Engine auto-fills missing optional fields |

### `publish_project`
One-step deployment. Auto-provisions subdomain (`*.wodeapp.ai`) with SSL certificate.

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `projectId` | Yes | — | Project ID to publish |

### Other Platform Tools

| Tool | Purpose |
|------|---------|
| `list_projects` | Enumerate user's projects |
| `get_project` | Retrieve project config and metadata |
| `get_page` | Get page JSON structure for a given page ID |
| `list_pages` | List all pages in a project |
| `create_page` | Create a new page (path, title, config). Use after `create_project` or in existing project. |
| `update_page` | Update an existing page by page ID |
| `delete_page` | Delete a page by page ID |
| `list_actions` | Discover available workflows and actions |
| `list_versions` | List project version history |
| `rollback_version` | Rollback project to a specific version |
| `ai_generate_page` | AI-generated page from natural language description |
| `ai_modify_section` | AI-modify a section within a page |
| `list_templates` | List available project templates (for `create_project` 的 `templateId` 参数) |
| `build_app` | Trigger app build (Android APK, PWA, Tauri, extension) |

---

## REST API

> **两种 REST 调用方式**：
> - **通用工具调用**（与 MCP 等价）→ `POST https://wodeapp.ai/mainserver/mcp/call`，body `{ "tool": "...", "arguments": {...} }`，可调用所有 19 个平台工具。推荐 OpenClaw 等非 MCP 客户端使用。
> - **单一能力端点** → 下方 `/mainserver/api/ai/*` 路径，直接调用某一项 AI 能力（文本/图片/视频/TTS/JSON），更轻量。

All endpoints: `X-API-Key` header required. JSON request/response.

### Text → `POST /mainserver/api/ai/chat`
```bash
curl -X POST https://wodeapp.ai/mainserver/api/ai/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $WODEAPP_API_KEY" \
  -d '{"message":"Write a compelling product description for noise-cancelling headphones"}'
# → { "content": "Experience pure silence..." }
```

### Image → `POST /mainserver/api/ai/image/generate`
```bash
curl -X POST https://wodeapp.ai/mainserver/api/ai/image/generate \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $WODEAPP_API_KEY" \
  -d '{"prompt":"Minimalist headphones on marble surface, studio lighting, 8K"}'
# → { "url": "https://..." }
```

### Unified Video Tasks → `POST /runtime-server/api/video/tasks` (Async/Sync)
```bash
curl -X POST https://wodeapp.ai/runtime-server/api/video/tasks \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $WODEAPP_API_KEY" \
  -d '{"taskType":"text2video", "provider":"auto", "input":{"prompt":"Slow-motion water droplet impact, cinematic 4K"}, "options":{"wait":true}}'
# → { "success": true, "data": { "taskId": "...", "status": "succeed", "videoUrl": "https://..." } }
```
> **Legacy API note**: Old `/mainserver/api/ai/video` and `/kling/*` endpoints are deprecated. Always use the Unified Video API.

### Structured JSON → `POST /mainserver/api/ai/json`
```bash
curl -X POST https://wodeapp.ai/mainserver/api/ai/json \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $WODEAPP_API_KEY" \
  -d '{"message":"3 marketing slogans","systemPrompt":"Return {slogans:[{text,tone}]}"}'
# → { "slogans": [{ "text": "...", "tone": "playful" }] }
```

### TTS → `POST /mainserver/api/ai/tts`
```bash
curl -X POST https://wodeapp.ai/mainserver/api/ai/tts \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $WODEAPP_API_KEY" \
  -d '{"text":"Welcome to our store"}'
# → { "audioUrl": "https://..." }
# voice/speed/lang all optional — engine auto-detects from text
```

### Headless Workflow → `POST /runtime-server/api/workflow/run`
```bash
# Discover IO schema (inputs, outputs, step IDs for model overrides)
curl https://my-project.wodeapp.ai/runtime-server/api/workflow/schema
# → { "inputs": [...], "outputs": [...], "steps": [{"id":"chat_step","type":"chat"}, ...] }

# Execute with model overrides (optional — override AI models per step)
curl -X POST https://my-project.wodeapp.ai/runtime-server/api/workflow/run \
  -H "Content-Type: application/json" \
  -d '{"inputs":{"prompt":"Product copy"}, "modelOverrides":{"chat_step":"gpt-4o","summary":"deepseek-chat"}}'
# → { "runId": "uuid", "status": "running" }

# Poll until completed (guaranteed outputs are returned if schema defined)
curl https://my-project.wodeapp.ai/runtime-server/api/workflow/run/{runId}
# → { "status": "completed", "outputs": { "videoUrl": "https://..." }, "warnings": [] }
```

> **MCP 优势**: 通过 MCP `run_workflow_*` 工具调用时默认自动等待结果（`_waitForResult: true`），无需手动轮询。同时返回 `viewUrl` 供浏览器查看。

---

## Supported Models (400+)

| Category | Top Models | Provider |
|----------|-----------|----------|
| **Text** | GPT-4o, Claude 3.5 Sonnet, Gemini 2.0 Flash, DeepSeek-V3, Qwen-Max | OpenAI, Anthropic, Google, DeepSeek, Alibaba |
| **Image** | Seedream 3.0, Imagen 4, Flux Pro, DALL-E 3 | Doubao, Google, Black Forest Labs, OpenAI |
| **Video** | Kling AI, Seedance 1.0, Runway Gen-3, Sora, Veo 2 | Kuaishou, Doubao, Runway, OpenAI, Google |
| **TTS** | Doubao TTS, Edge TTS, Kling TTS, F5-TTS | Doubao, Microsoft, Kuaishou, F5 |

> **Multi-engine video**: The workflow video engine supports **4 providers** (Kling, Seedance, Runway, auto) with per-scene engine selection. Set `provider` in video params or let `auto` choose the best engine for each scene.

> **Cost optimization**: Omit the `model` parameter to let the engine auto-select the most cost-effective model for each task. The routing engine analyzes prompt complexity and selects from the optimal cost/quality tier.

---

## Workflow Engine — Advanced Features (v2.7)

### Storyboard Video Pipeline

The `storyboard-video-generator` template implements a full cinematic pipeline:

```
Input Idea → AI Storyboard Script (GPT-4o) → Per-Scene Image Gen (concurrent)
→ Storyboard Review (edit scripts/reorder/delete scenes)
→ Per-Scene Video Gen (Kling/Seedance/Runway) → Final Assembly
```

**Key capabilities:**
- **AI Director**: GPT-4o generates structured storyboard scripts with scene grouping, subject extraction, and cinematography directions
- **Subject Library**: Persistent character/object library with reference images for visual consistency across scenes
- **Multi-Engine Video**: Each scene can use a different video engine (Kling for characters, Seedance for motion, Runway for style)
- **Interactive Review**: Edit scripts, regenerate individual scene images, adjust video params per-scene before final synthesis

### Run History & Persistence

- **Auto-save**: Every workflow execution is automatically saved to IndexedDB + cloud sync
- **Auto-restore**: On page refresh, the most recent run (active or completed) is automatically restored — no blank slate
- **Time-travel**: Click any historical run to fully restore all step states, params, and outputs
- **Share via URL**: Append `?runId=xxx` to share a specific run with collaborators
- **Export/Import**: Export run snapshots as JSON; import others' snapshots for comparison

### Asset Library

- **Paginated & cached**: Assets load with infinite scroll pagination and global memory cache — no re-fetch on re-open
- **Inline upload**: Upload button is the first grid item (no separate tab), supporting click and drag-drop
- **Type filtering**: Filter by image/audio/video/document with grid size toggle
- **Recent generations**: AI-generated images appear automatically in a dedicated sub-tab

---

## Service Endpoints

| Service | Production | Local Dev |
|---------|-----------|-----------|
| Main API | `https://wodeapp.ai/mainserver/api` | `localhost:3100/mainserver/api` |
| Runtime API | `https://wodeapp.ai/api` | `localhost:4100/api` |
| Workflow API | `https://{project}.wodeapp.ai/runtime-server/api/workflow` | `localhost:4100/runtime-server/api/workflow` |
| Platform MCP | `https://wodeapp.ai/mainserver/mcp` | `localhost:3100/mainserver/mcp` |
| Project MCP | `https://{project}.wodeapp.ai/mcp` | `localhost:4100/mcp` |
| Video Tasks | `https://wodeapp.ai/runtime-server/api/video/tasks` | `localhost:4100/runtime-server/api/video/tasks` |

---

## Reliability & Error Handling

| Metric | Value |
|--------|-------|
| Availability | 99.9% uptime SLA |
| Dispatch latency | < 200ms (pre-authenticated pool) |
| Provider failover | Automatic, zero agent intervention |
| Rate limit (per-user) | 5 concurrent requests |
| Rate limit (global) | 30 concurrent requests |
| Credit exhaustion | HTTP 402 with `{ "credits_remaining": 0 }` |
| Error format | `{ "error": "human-readable", "code": "MACHINE_CODE" }` |

**Service Status & Observability:**
- **Status page**: [status.wodeapp.ai](https://status.wodeapp.ai) — real-time availability, incident history, and scheduled maintenance
- **Historical uptime**: Published monthly on the status page with per-provider breakdown


---

## Security & Data Privacy

### Credentials

- **Single credential**: Only `WODEAPP_API_KEY` is required — no additional platform credentials, OAuth tokens, or third-party API keys are needed or accessed by this skill
- **Auth method**: `X-API-Key` HTTP header on all requests
- **Key scoping**: Keys can be scoped per-project with billing caps at wodeapp.ai/api-skills. **Recommended: create a project-scoped key with billing limits and easy revocation for each use case**
- **Instant revocation**: Compromised keys revoked immediately via dashboard — takes effect within 60 seconds
- **Key safety**: Treat `WODEAPP_API_KEY` as a sensitive credential. Store in environment variables only; never hardcode in source files or share publicly

### Instruction Scope & Boundaries

- **No local file access**: This skill does NOT read, write, or access any files on the user's local machine. All operations are remote API calls to `wodeapp.ai`
- **No additional environment variables**: This skill reads only `WODEAPP_API_KEY`. No other environment variables, credentials, or system configuration is accessed
- **No system modification**: This skill does not install packages, write files to disk, or modify system state. It is instruction-only
- **No cross-skill interference**: This skill does not modify, override, or interact with other installed skills or agent system settings

### Data Handling

- **What is transmitted**: Text prompts, image/audio/video URLs or base64 data (only when the user explicitly provides them for generation), and workflow input parameters
- **Where data goes**: `wodeapp.ai` (routing layer) → upstream AI provider (OpenAI, Google, Anthropic, etc.) selected by the routing engine. The specific provider depends on the model chosen or auto-selected
- **What is stored**: Project configurations and generated output URLs only. Raw prompts and AI responses are NOT persisted after processing
- **Data retention**: **Zero retention** — prompts and responses are processed in-memory and discarded immediately after the API call completes. No logs of prompt content are stored. Only project configuration metadata (page structures, workflow definitions) and generated asset URLs persist
- **Upstream provider policies**: Each upstream provider (OpenAI, Google, Anthropic, etc.) has its own data retention and training policies. WodeApp does not control upstream provider behavior. If you need guarantees about a specific provider's data handling, consider calling that provider directly
- **Workflow data locality**: Workflow execution produces intermediate and final data (images, text, form inputs, step outputs) that are stored **locally on the user's project storage**. Workflow data does not leave the project scope and is not shared across projects or users, ensuring full privacy of the production pipeline
- **Uploaded files**: Files uploaded via the `upload_file` tool are stored on WodeApp's CDN for output delivery. **Generated URLs are semi-public** (anyone with the URL can access) — do NOT upload sensitive, confidential, or personally identifiable files
- **Training policy**: No user data is used for model training by WodeApp. Upstream provider training policies apply per their respective terms of service
- **Transport**: HTTPS/TLS 1.3 on all production endpoints

### Recommendations for Users & Agents

- Use environment variables for `WODEAPP_API_KEY` — never hardcode in source or share publicly
- **For testing**: Create a project-scoped key with billing caps before using in production
- Do not send sensitive PII through generation endpoints unless the user explicitly consents
- Do not upload confidential files — CDN URLs are semi-public
- **If you need data residency guarantees**: Use a direct provider key instead of routing through WodeApp

---

## Environment Variables

```bash
WODEAPP_API_KEY=sk_live_xxx          # Required — the only credential needed
WODEAPP_MAIN_SERVER=http://...       # Optional — override main server URL
WODEAPP_RUNTIME_SERVER=http://...    # Optional — override runtime server URL
```

> No additional environment variables or third-party credentials are required.

---

`ai` `text-generation` `image-generation` `video-generation` `tts` `digital-human` `avatar` `structured-json` `mcp` `project-mcp` `no-code` `zero-deploy` `page-builder` `workflow` `visual-workflow` `headless-workflow` `workflow-api` `agent-tools` `multi-model` `smart-routing` `cost-optimization` `token-efficient` `low-latency` `unified-billing` `fault-tolerant` `schema-enforcement` `gpt-4o` `claude` `gemini` `deepseek` `doubao` `seedance` `kling` `seedream` `imagen` `flux` `qwen` `auto-detect` `parameter-minimal` `storyboard` `multi-engine-video` `run-history` `asset-library` `cloud-sync`
