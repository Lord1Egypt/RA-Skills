# 排错：按症状定位

> 先跑一次自检，多数问题它直接告诉你答案：
> ```bash
> python -X utf8 scripts/verify_a7w.py
> ```

---

## 症状 1：点「检查」报连接失败 / 404

**最常见原因：API Host 多写了一层 `/v1`。**

| 你填的 API Host | 实际请求 | 结果 |
|---|---|---|
| `https://api.a7w.cn/api/v1` | `.../api/v1/v1/chat/completions` | ❌ 404 |
| `https://api.a7w.cn/api` | `.../api/v1/chat/completions` | ✅ 200 |

**改法**：把 API Host 改成 `https://api.a7w.cn/api`，API Path 留空。

> 注意 404 返回的是一整页 HTML，不会告诉你"多了一层 /v1"。所以这个坑很难自查出来。

---

## 症状 2：404，且返回 HTML 页面

网关对**不存在的路径**返回 HTML 404，对**存在但缺参数**返回 JSON。
所以：

- 返回 **HTML** → 路径不对（apiHost/apiPath 拼错了）
- 返回 **JSON**（如 `{"code":0,"msg":"model参数不能为空"}`）→ 路径对，是参数问题

```bash
# 确认你的 apiHost 写法
python -X utf8 scripts/verify_a7w.py --api-host <你填的那个>
```

---

## 症状 3：401 / 鉴权失败

| 检查项 | 说明 |
|---|---|
| Key 是否正确复制 | 注意首尾空格 |
| Key 是否已启用 | 用户中心 → API 密钥 |
| 账号是否实名 | 未实名无法创建可用 Key |
| Key 是否被 IP 白名单限制 | 若设了白名单，本机出口 IP 要在里面 |

401 也说明**鉴权是生效的**（这是好事，说明网络通、路径对）。

---

## 症状 4：402 点数不足

**402 有两种，要先分清**：

| code | 含义 | 处理 |
|---|---|---|
| `insufficient_points` | **账号余额不足** | 充值 |
| `key_quota_exceeded` | **这个 Key 自己的额度打满了** | 去用户中心调高/重置该 Key 的 quota，或换个 Key |

分不清就会去充一个根本不需要充的账户——**账号有钱但 Key 额度满了，也会报 402**。

---

## 症状 5：能连上，但对话不出字

**流式（SSE）不通。** Chatbox 默认开流式，若网关只支持非流式，
表现正是"连接成功、发出去没反应"。

本网关**流式是通的**（实测 `Content-Type: text/event-stream`，60+ 个 `data` 块，
以 `[DONE]` 结束）。所以先确认：

```bash
python -X utf8 scripts/verify_a7w.py     # 看第 3 项「流式」是否 PASS
```

若第 3 项 PASS 但 GUI 仍不出字，检查中间是否有**代理/公司网关**截断了 SSE
（有些反代会缓冲 `text/event-stream`）。

---

## 症状 6：模型下拉是空的

Chatbox 靠 `GET /v1/models` 填充模型列表。

1. 确认 API Host 能通（症状 1）
2. 确认该 Key 有权访问模型列表
3. **手动添加模型**兜底：模型 ID 直接填 `DeepSeek-V4-Flash`

实测 `GET /v1/models` 返回 **75 个模型**，若你拿到 0 个，是路径或权限问题，不是没模型。

---

## 症状 7：模型加了但调用报「模型不存在」

**模型名不是真名。** 网关模型 ID 区分大小写，且存在近似条目：

- `Qwen3.6-Plus` ≠ `qwen3.6-plus`（两条不同记录）

**解决**：从 `GET /v1/models` 复制 `model_code` 字段，不要手打。

```bash
python -X utf8 ..\one-key-ai-gateway\scripts\client.py models
```

---

## 症状 8：推理模型「什么都不输出」

推理模型会把 token 先花在**思维链**上，思维链占满了 `max_tokens` 就没内容可输出。

实测：`DeepSeek-V4-Flash` 在 `max_tokens=8` 时 `content` 返回 `null`，
`finish_reason=length`；加到 200 就正常。

**解决**：把 Chatbox 里该模型的**最大输出调大**（≥ 200，建议 1000+）。

---

## 症状 9：想把 TTS / 数字人 / 视频生成也接进 Chatbox

**做不到，别在这上面耗时间。**

Chatbox 只会打 `/v1/chat/completions`；而网关的 21 个生成应用走的是
`POST /api/v1/apps/{app}/{code}` → `task_id` → 轮询，是**另一套异步协议**，
Chatbox 原生不支持。

要用这些能力，走 `one-key-ai-gateway` 技能包（它覆盖两条入口）。

---

## 症状 10：知识库 / 向量化用不了

**网关没有 embedding、没有 rerank 模型**（75 个模型里一个都没有）。

Chatbox 若要用知识库，需要另配本地 embedding（如 bge-m3）。

---

## 快速对照表

| 现象 | 最可能的原因 | 一句话解决 |
|---|---|---|
| 检查失败 / 404 HTML | apiHost 带了 `/v1` | 改成 `https://api.a7w.cn/api` |
| 404 | 路径拼错 | 跑 `verify_a7w.py --api-host` 验 |
| 401 | Key 错/未实名/白名单 | 换 Key 或查用户中心 |
| 402 | 余额不足 **或** Key 额度满 | 先分清是哪种 |
| 能连不出字 | 流式被截断 | 看自检第 3 项 |
| 模型列表空 | 路径或权限 | 手动填 `DeepSeek-V4-Flash` |
| 模型不存在 | 名字不是真名 | 从 `/v1/models` 复制 |
| 推理模型无输出 | `max_tokens` 太小 | 调到 1000+ |
| 想接 TTS/视频 | 协议完全不同 | 用 `one-key-ai-gateway` |
| 知识库用不了 | 无 embedding | 另配本地 bge-m3 |
