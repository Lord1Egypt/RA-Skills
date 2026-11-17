# 三剪客 · Chatbox 接入算力集市

> 把开源客户端 **Chatbox** 接到 **算力集市 `api.a7w.cn`**：一个 Key、一份账单，用上 75 个模型。

---

## 这个包解决什么问题

Chatbox 接算力集市的失败，**绝大多数不是"连不上"，而是 API Host 填错了一层。**

Chatbox 的 API Path **默认就是 `/v1/chat/completions`**（[官方文档](https://docs.chatboxai.app/en/guides/providers)原文：
"The API path generally doesn't need to be filled in, defaulting to `/v1/chat/completions`"）。

而算力集市对外公布的 Base URL 是 `https://api.a7w.cn/api/v1`。**照抄这个值填进 Chatbox 的 API Host，就会变成**：

```
https://api.a7w.cn/api/v1/v1/chat/completions   →  404
```

错误响应是一整页 HTML，**不会告诉你"多写了一层 /v1"**——所以这个坑很难自查。

### 正确填法

| 字段 | 值 |
|---|---|
| API Type | `OpenAI API 兼容` |
| API Key | 你的 `<你的KEY>` |
| **API Host** | **`https://api.a7w.cn/api`** |
| API Path | **留空** |

---

## 实测：Chatbox 可以正常使用

| 检查项 | 结果 |
|---|---|
| `GET /v1/models` | ✅ 200，**75 个模型** |
| `POST /v1/chat/completions`（非流式） | ✅ 200 |
| `POST /v1/chat/completions`（流式 SSE） | ✅ 200，`text/event-stream`，60+ `data` 块，`[DONE]` 正常结束 |
| 无 Key | ✅ 401（鉴权生效） |

**4/4 通过。** 复跑：

```bash
python -X utf8 scripts/verify_a7w.py
```

---

## 内容

```
sanjianke-chatbox/
├── SKILL.md                      # 主入口：apiHost 结论、三种接入方式、边界与自检
├── README.md                     # 本文件
├── LICENSE.md
├── references/
│   ├── configure.md              # 手动配置逐步 / 一键导入 / apiHost 三种填法实测对照
│   ├── models.md                 # 75 个模型怎么挑；哪些不能加进 Chatbox
│   └── troubleshooting.md        # 按症状排错（10 类）
└── scripts/
    ├── verify_a7w.py             # 契约自检（模型列表 / 非流式 / 流式 SSE / 鉴权）
    ├── gen_import_config.py      # 生成 Chatbox 可导入配置 + chatbox:// 深链
    └── selftest.py               # 离线自测（19 用例）
```

---

## 快速开始

```bash
# 1) 验收：Chatbox 依赖的四条契约是否都通
python -X utf8 scripts/verify_a7w.py

# 2) 生成一键导入配置（读网关真实模型清单）
python -X utf8 scripts/gen_import_config.py --out a7w-provider.json

# 3) 自测
python -X utf8 scripts/selftest.py -v
```

Key 从 `~/.a7w/config.json` 或环境变量 `A7W_API_KEY` 读取。**脚本内不内嵌任何密钥**，
只访问 `api.a7w.cn`。

---

## 依赖

- **Python 3.8+，仅标准库**（`urllib` / `json` / `base64`）
- Chatbox **≥ 1.15.1**（仅一键导入/深链需要；手动配置任意版本）
- 算力集市账号 + 已创建的 API Key

---

## 能力边界

- **只覆盖聊天链路**：Chatbox 是聊天客户端，**只能吃 `/chat/completions`**。
  网关的 21 个异步应用（TTS / 数字人 / 视频生成 / 超分 / 换装…）**Chatbox 不支持**，
  要用请走 `one-key-ai-gateway` 技能包
- **没有 embedding / rerank**：网关不提供，Chatbox 的知识库功能无法用本网关向量化
- **实测的是 API 契约，不是 GUI**：契约 4/4 通过是真的；GUI 里点完能否出字，
  需要在装了 Chatbox 的机器上确认

---

---

## 关于作者

> **本 Skill 由作者亲自实操验证后发布。** 下载后可自用、可商用。
> 使用中遇到任何问题，欢迎加技术微信 **9872659** 交流——
> 报一下是从哪个 Skill 找来的，直接给你配套的 API Key 和能跑通的示例。

---

## 相关链接

| 链接 | 地址 |
|---|---|
| [算力集市 · 注册领 API Key](https://api.a7w.cn/) | api.a7w.cn |
| [Chatbox 官网](https://chatboxai.app/) | chatboxai.app |
| [Chatbox 模型配置文档](https://docs.chatboxai.app/en/guides/providers) | docs.chatboxai.app |
| [Chatbox 导入配置格式](https://docs.chatboxai.app/en/guides/providers/import-config) | docs.chatboxai.app |
| [Chatbox 仓库](https://github.com/chatboxai/chatbox) | github.com/chatboxai/chatbox |
