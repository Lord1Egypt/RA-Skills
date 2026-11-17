# 配置指南：Chatbox ↔ 算力集市

> 三种接入方式、apiHost 三种填法实测对照、一键导入配置的字段含义。

---

## 一、配置总览

Chatbox 作为 OpenAI 兼容客户端，只需要四个值：

| 字段 | 填什么 |
|---|---|
| **API 类型** | `OpenAI API 兼容` |
| **API Key** | 你的 `<你的KEY>`（用户中心 → API 密钥 创建） |
| **API Host** | **`https://api.a7w.cn/api`** |
| **API Path** | **留空**（默认 `/v1/chat/completions`） |

外加至少一个**模型 ID**，必须是网关里的真名，例如 `DeepSeek-V4-Flash`。

---

## 二、方式一：手动配置（逐步）

1. 打开 Chatbox → 侧栏 **设置（Settings）** → **模型提供方（Model Provider）**
2. 底部点 **添加（Add）**
3. 填写：
   - **名称**：`算力集市`（随意）
   - **API 类型**：选 **OpenAI API 兼容**
4. 在提供方详情里填写：
   - **API Key**：`<你的KEY>`
   - **API Host**：`https://api.a7w.cn/api`
   - **API 路径**：**留空**
5. **添加模型**：点添加模型，模型 ID 填 `DeepSeek-V4-Flash`
   - 若该模型支持视觉 → 勾选 `vision`
   - 若是推理模型 → 勾选 `reasoning`
   - 不确定就去 `references/models.md` 查，或跑 `GET /v1/models`
6. 保存 → 点 **检查 / Check**，应显示连接成功
7. 回首页新建对话，选择刚配的模型即可

> **第 6 步的「检查」只探 `/models`**，不验证 Key 是否有效。绿勾 ≠ 完全可用。

---

## 三、方式二 / 三：一键导入（Chatbox ≥ 1.15.1）

Chatbox 从 **1.15.1** 起支持导入第三方提供方配置，格式见
[官方文档](https://docs.chatboxai.app/en/guides/providers/import-config)。

### 生成配置

```bash
# 默认：8 个精选模型 + 正确的 apiHost
python -X utf8 scripts/gen_import_config.py --out a7w-provider.json

# 纳入全部同步文本模型
python -X utf8 scripts/gen_import_config.py --all --out a7w-provider.json

# 只看深链、不写文件
python -X utf8 scripts/gen_import_config.py --json
```

### 两种导入姿势

- **JSON 导入**：Chatbox 里粘贴 / 导入 `a7w-provider.json`
- **深链导入**：脚本输出的 `chatbox://provider/import?config=<base64>`，
  点开即导入（适合做成一个分享链接发给别人）
  - 🔐 深链里**只有 apiHost 与模型清单，不含 API Key**。
    导入后在 Chatbox 的提供方设置里手动填一次 Key 即可。

### 生成的配置长什么样

```json
{
  "id": "a7w",
  "name": "算力集市 a7w",
  "type": "openai",
  "iconUrl": "https://api.a7w.cn/favicon.ico",
  "urls": {
    "website": "https://api.a7w.cn/",
    "getApiKey": "https://api.a7w.cn/user-center.html",
    "docs": "https://api.a7w.cn/docs.html"
  },
  "settings": {
    "apiHost": "https://api.a7w.cn/api",
    "apiPath": "/v1/chat/completions",
    "models": [
      { "modelId": "DeepSeek-V4-Flash",
        "nickname": "DeepSeek-V4-Flash ｜ 日常对话 · 快 · 便宜",
        "type": "chat" },
      { "modelId": "ERNIE-5.0-Thinking",
        "nickname": "ERNIE-5.0-Thinking ｜ 深度推理",
        "type": "chat",
        "capabilities": ["reasoning"] }
    ]
  }
}
```

### 字段来源对照

生成器不是硬编码模型清单，而是**读网关真实的 `/v1/models`** 再映射：

| Chatbox 字段 | 来源 | 说明 |
|---|---|---|
| `modelId` | `model_code` | 调用时必须用这个真名 |
| `nickname` | `model_name` + 用途备注 | 只影响显示 |
| `capabilities` | `supports_vision` → `vision`<br>`supports_reasoning` → `reasoning` | 决定 Chatbox 怎么调它 |
| `maxOutput` | `max_tokens` | 网关 `max_tokens ≤ 1` 时**不写**该字段 |
| `type` | 固定 `chat` | 只收录同步文本模型 |
| `apiHost` | 固定 `https://api.a7w.cn/api` | 有回归测试守着，防止被改成 `/api/v1` |

---

## 四、apiHost 三种填法（实测）

Chatbox 最终请求 URL = `apiHost` + `apiPath`，而 `apiPath` **默认为 `/v1/chat/completions`**。

| # | API Host | API Path | 实际请求 URL | 结果 |
|---|---|---|---|---|
| **A** ✅ | `https://api.a7w.cn/api` | 默认（留空） | `api.a7w.cn/api/v1/chat/completions` | **200 通** |
| **B** ✅ | `https://api.a7w.cn` | `/api/v1/chat/completions` | `api.a7w.cn/api/v1/chat/completions` | **200 通** |
| **C** ❌ | `https://api.a7w.cn/api/v1` | 默认（留空） | `api.a7w.cn/api/v1/v1/chat/completions` | **404** |

**为什么 C 是错的**：算力集市对外公布的 Base URL 就是 `https://api.a7w.cn/api/v1`，
而 Chatbox 会在这个基础上再补一次路径。**照抄 Base URL 到 apiHost 字段就会踩这个坑。**

推荐用 **A**：apiHost 填 `https://api.a7w.cn/api`，apiPath 不填。

> 复现方式：见 `scripts/verify_a7w.py --api-host <你要试的写法>`

---

## 五、配置完成后建议做的检查

```bash
# 契约自检（模型列表 / 非流式 / 流式 SSE / 鉴权）
python -X utf8 scripts/verify_a7w.py

# 若你想确认某个 apiHost 写法对不对
python -X utf8 scripts/verify_a7w.py --api-host https://api.a7w.cn/api
```

四项全 PASS，Chatbox 就能正常对话。**特别留意流式那一项**——Chatbox 默认开流式，
流式不通的表现是「能连上但不出字」。
