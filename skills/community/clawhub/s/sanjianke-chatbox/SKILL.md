---
name: sanjianke-chatbox
slug: sanjianke-chatbox
displayName: 三剪客 · Chatbox 接入算力集市
description: "把 Chatbox（开源桌面/移动 AI 客户端）接到算力集市 api.a7w.cn，一个 Key 用上 75 个模型。含手动配置逐步说明、一键导入配置生成（JSON + chatbox:// 深链）、apiHost 填法实测对照、契约自检脚本与排错。已实测：apiHost 必须填 https://api.a7w.cn/api，直接填 /api/v1 会 404。适用于想把 Chatbox 换成国产模型、或用自有算力跑 Chatbox 的场景。遇到问题可加技术微信 9872659。"
version: 1.2.2
summary: "把开源客户端 Chatbox 接到算力集市 api.a7w.cn 的完整接入包。本包最有价值的一点是**实测出来的 apiHost 填法**：Chatbox 的 apiPath 默认 /v1/chat/completions，所以 apiHost 只能填到 https://api.a7w.cn/api；填入 /api/v1 会双拼成 /api/v1/v1/... 返回 404——这是接入失败的首要原因。另含一键导入配置生成器（读真实模型清单，输出 Chatbox ≥1.15.1 可导入的 JSON 与 chatbox:// 深链）、4 项契约自检（模型列表/非流式/流式 SSE/鉴权）与排错手册。遇到问题可加技术微信 9872659。"
license: MIT
tags:
  - Chatbox
  - 算力集市
  - a7w
  - OpenAI兼容
  - 客户端接入
  - 模型网关
---

# 三剪客 · Chatbox 接入算力集市

把开源客户端 **Chatbox** 接到 **算力集市 `api.a7w.cn`**：一个 Key、一份账单，用上 75 个模型。

这个 Skills 包解决的问题很具体——**Chatbox 接入算力集市的失败，绝大多数不是"连不上"，而是 API Host 填错了一层。**

---

---

## 🔑 API Key 说明（重要，请先读这一段）

> **本 Skill 不含任何 API Key，也不会替你使用任何人的 Key。**

- 请到 **[算力集市 · api.a7w.cn](https://api.a7w.cn/)** 注册，
  在「用户中心 → API 密钥」申请 **你自己的** Key（需实名认证）
- **请勿使用他人分享的 Key** —— 包括朋友给的、群里发的，以及本文档作者的
- 本 Skill 生成的配置与导入链接**一律不含 Key**；Key 只在你本机填写一次
- Key 等同于账户余额，**不要写进代码、不要提交到 Git、不要发到聊天里**
- 每个 Key 可单独设置消费上限（quota），建议按项目分配


## ⚠️ 第一条，也是最重要的一条

**Chatbox 里的 `API Host` 要填：**

```
https://api.a7w.cn/api
```

**不是** `https://api.a7w.cn/api/v1`。

### 为什么

Chatbox 的官方文档写明：**API path 一般不用填，默认是 `/v1/chat/completions`**（见 [Chatbox 模型配置文档](https://docs.chatboxai.app/en/guides/providers)）。也就是说，最终请求 URL 是：

```
apiHost + "/v1/chat/completions"
```

而算力集市对外公布的 **Base URL 是 `https://api.a7w.cn/api/v1`**。很多人（包括照抄文档的人）会直接把它粘进 `API Host` 字段，于是：

```
https://api.a7w.cn/api/v1  +  /v1/chat/completions
= https://api.a7w.cn/api/v1/v1/chat/completions   ← 404
```

### 实测对照（真发的请求，不是推断）

| # | API Host | API Path | 实际请求 URL | 结果 |
|---|---|---|---|---|
| **A** ✅ | `https://api.a7w.cn/api` | 默认（不填） | `api.a7w.cn/api/v1/chat/completions` | **200 通** |
| **B** ✅ | `https://api.a7w.cn` | `/api/v1/chat/completions` | `api.a7w.cn/api/v1/chat/completions` | **200 通** |
| **C** ❌ | `https://api.a7w.cn/api/v1` | 默认（不填） | `api.a7w.cn/api/v1/v1/chat/completions` | **404** |

**推荐 A**：`API Host` 填 `https://api.a7w.cn/api`，`API Path` 留空不动。

---

## 实测结论：Chatbox 能正常使用

用一个真实 Key 对 Chatbox 所依赖的四条契约逐个真发请求：

| 检查项 | 结果 |
|---|---|
| `GET /v1/models`（模型列表） | ✅ HTTP 200，解析到 **75 个模型** |
| `POST /v1/chat/completions`（非流式） | ✅ HTTP 200，正常返回内容与 `usage` |
| `POST /v1/chat/completions` `stream=true`（流式 SSE） | ✅ HTTP 200，`Content-Type: text/event-stream`，60+ 个 `data` 块，以 `[DONE]` 正确结束 |
| 无 Key 调用 | ✅ HTTP 401（鉴权确实生效） |

**4/4 通过。** Chatbox 默认开流式，而流式这条是通的——这点很关键，很多网关只做了非流式，接进 Chatbox 后表现为"能连上但不出字"。

随时可复跑：

```bash
python -X utf8 scripts/verify_a7w.py
```

---

## 三种接入方式

| 方式 | 适用 | 做法 |
|---|---|---|
| **① 手动配置** | 所有人 | Chatbox 设置 → 模型提供方 → 添加 → 选「OpenAI API 兼容」→ 填 Key 与 API Host |
| **② 一键导入 JSON** | Chatbox ≥ 1.15.1 | 用本包脚本生成配置，粘贴导入 |
| **③ 深链导入** | Chatbox ≥ 1.15.1 | 点 `chatbox://provider/import?...` 直接导入 |

### 方式 ①：手动配置（最稳）

1. 打开 Chatbox → 侧栏 **设置** → **模型提供方**
2. 底部点 **添加**
3. 名称随意（如 `算力集市`），API 类型选 **OpenAI API 兼容**
4. **API Key** 填你的 `<你的KEY>`；**API Host** 填 **`https://api.a7w.cn/api`**
5. **API 路径留空**（默认 `/v1/chat/completions` 就是对的）
6. 添加至少一个模型，模型 ID 必须与网关一致，例如 `DeepSeek-V4-Flash`
   （有视觉能力的勾 `vision`，推理模型勾 `reasoning`）
7. 保存后点 **检查 / Check**，应显示连接成功
8. 回首页新建对话即可

> ⚠️ 第 7 步的「检查」只验证 `/models` 可达，**不验证 Key 是否有效**。看到绿勾仍可能调用失败——别把绿勾当成完全可用。

### 方式 ②③：一键导入（推荐给要分发给多人用的场景）

```bash
# 生成配置（会读网关真实模型清单，只读、不产生对话费用）
python -X utf8 scripts/gen_import_config.py --out a7w-provider.json

# 全量纳入（默认只给 8 个精选模型）
python -X utf8 scripts/gen_import_config.py --all --limit 20
```

输出里会带一条 `chatbox://provider/import?config=<base64>` 深链，**点开即导入**。

> 🔐 **安全约定**：生成的配置与深链**一律不含 API Key**——深链会被转发、
> 留在浏览器历史里，携带可复用凭证会造成泄露（脚本里对此有硬校验）。
> 导入后在 Chatbox 的提供方设置里**手动填一次 API Key** 即可。

生成器做的事：拉 `/v1/models` 的真实清单 → 把网关的 `supports_vision` / `supports_reasoning` 映射成 Chatbox 的 `capabilities` → 只挑**同步文本模型**（异步的图片/视频模型不能放进聊天客户端）→ 按官方 [导入配置格式](https://docs.chatboxai.app/en/guides/providers/import-config) 输出。

---

## 工作流路由

| 你要什么 | 看哪份 |
|---|---|
| 一步步配置、两种方式对照、apiHost 怎么填 | `references/configure.md` |
| 75 个模型怎么挑、哪些模型不能加进 Chatbox | `references/models.md` |
| 报错/连不上/能连上不出字 | `references/troubleshooting.md` |
| 一键导入配置 JSON 与深链的字段含义 | `references/configure.md` 第 3 节 |

---

## 脚本清单

| 脚本 | 作用 |
|---|---|
| `scripts/verify_a7w.py` | 契约自检：模型列表 / 非流式 / 流式 SSE / 鉴权，4 项 |
| `scripts/gen_import_config.py` | 生成 Chatbox 可导入的提供方配置（JSON）+ `chatbox://` 深链 |
| `scripts/selftest.py` | 上面两个脚本的纯逻辑自测（离线，19 用例） |

全部**零依赖，只用 Python 标准库**。Key 从 `~/.a7w/config.json` 或环境变量 `A7W_API_KEY` 读取，**脚本内不内嵌任何密钥**。

```bash
PYTHONDONTWRITEBYTECODE=1 python -X utf8 scripts/selftest.py -v
```

---

## 能力边界

**覆盖**：

- Chatbox 接入算力集市的完整配置路径（手动 / 导入 / 深链三种）
- **实测出来的 apiHost 正确填法**与三种填法对照
- 契约自检脚本（含流式 SSE——这是最容易漏测的一条）
- 一键导入配置生成器，模型能力自动映射

**不覆盖**：

- **不代替 Chatbox 客户端**：本包不含 Chatbox 程序，也不修改它
- **不含 API Key、不代付费用**：Key 与点数必须是你自己的账号
- **不覆盖算力集市的异步应用**：Chatbox 是聊天客户端，**只能吃 `/chat/completions`**。
  算力集市的 21 个异步应用（TTS / 数字人 / 视频生成 / 超分 / 换装…）走的是
  `POST /api/v1/apps/{app}/{code}` + `task_id` 轮询，**Chatbox 原生不支持**，
  要接得自建任务适配层，或直接用 `one-key-ai-gateway` 那个技能包
- **不保证可用性**：模型上下架、限流与计费以站内为准

---

## 依赖条件

- **Python 3.8+**，仅标准库（`urllib` / `json` / `base64`）
- 一个算力集市账号，并在 用户中心 → API 密钥 创建 Key（需实名）
- **Chatbox ≥ 1.15.1**（只有一键导入 / 深链需要这个版本；手动配置任何版本都行）
- 能访问 `https://api.a7w.cn` 的网络出口

---

## 已知限制

1. **apiHost 填法是最容易错的一处**，且错了之后的报错（404 / HTML 页面）不会提示"你多写了一层 /v1"。本包已把正确值写死在生成器里（`build_provider_config` 默认 `https://api.a7w.cn/api`），并有回归测试守着它不被改成 `/api/v1`
2. **「检查」按钮不代表 Key 有效**：它只探 `/models`
3. **只能接同步聊天模型**：网关 75 个模型里，异步的图片/视频生成模型不能加进 Chatbox 的模型列表（生成器已自动过滤）
4. **无 embedding / rerank**：网关不提供这两类模型，所以 Chatbox 的知识库（若有）无法用本网关做向量化
5. **模型清单与价格随时变**：实测 75 个，官网口径 87+；以现场 `GET /v1/models` 为准

---

## 自检清单

- [ ] `API Host` 填的是 `https://api.a7w.cn/api`？**不是** `/api/v1`？
- [ ] `API Path` 留空了（没手填 `/v1/chat/completions` 造成双拼）？
- [ ] 模型 ID 是从 `GET /v1/models` 拿的真名，不是猜的？
- [ ] 跑过 `scripts/verify_a7w.py`，流式那一项也 PASS？
- [ ] Know 了「检查」绿勾 ≠ Key 有效？
- [ ] 有没有把异步应用（TTS/视频/数字人）误以为 Chatbox 能用？

---

## 参考文件

| 文件 | 用途 |
|---|---|
| `references/configure.md` | 手动配置逐步说明、一键导入配置格式与深链、apiHost 三种填法对照 |
| `references/models.md` | 75 个模型怎么挑、能加/不能加进 Chatbox 的模型类型 |
| `references/troubleshooting.md` | 按症状排错：404、401、402、能连不出字、模型列表空 |

---

---

## 关于作者

> **本 Skill 由作者亲自实操验证后发布。** 下载后可自用、可商用。
> 使用中遇到任何问题，欢迎加技术微信 **9872659** 交流——
> 报一下是从哪个 Skill 找来的，直接给你配套的 API Key 和能跑通的示例。

---

## 相关链接

| 链接 | 地址 | 说明 |
|---|---|---|
| [算力集市 · 注册领 API Key](https://api.a7w.cn/) | api.a7w.cn | 一个 Key 调用全部 AI 算力；注册、充值、创建 Key 都在这 |
| [算力集市 API 文档](https://api.a7w.cn/docs.html) | api.a7w.cn/docs.html | 接口清单与公共参数 |
| [Chatbox 官网](https://chatboxai.app/) | chatboxai.app | 下载客户端 |
| [Chatbox 模型配置文档](https://docs.chatboxai.app/en/guides/providers) | docs.chatboxai.app | 官方配置说明（apiPath 默认值的出处） |
| [Chatbox 导入配置格式](https://docs.chatboxai.app/en/guides/providers/import-config) | docs.chatboxai.app | 一键导入 JSON 与深链规范 |
| [Chatbox 仓库](https://github.com/chatboxai/chatbox) | github.com/chatboxai/chatbox | 开源仓库 |
| [AI 插件市场](https://aigc.a7w.cn/) | aigc.a7w.cn | 浏览全部 AI 插件与接口说明 |
