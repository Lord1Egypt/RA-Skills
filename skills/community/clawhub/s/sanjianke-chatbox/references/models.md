# 模型选择：75 个模型里哪些能加进 Chatbox

> 数据来源：`GET https://api.a7w.cn/api/v1/models`，2026-09-25 实测。

---

## 一、先分清：能加的 / 不能加的

| 类型 | 数量 | 调用方式 | 能加进 Chatbox？ |
|---|---|---|---|
| **文本** | **58** | `call_type=1` 同步 | ✅ **能** |
| 图片生成 | 12 | `call_type=2` 异步 | ❌ 不能 |
| 视频生成 | 5 | `call_type=2` 异步 | ❌ 不能 |

**为什么图片/视频模型不能加**：Chatbox 是聊天客户端，只会打
`/v1/chat/completions` 并期待同步返回 `choices`。而网关的图片/视频模型走的是
`POST /api/v1/apps/{app}/{code}` → 返回 `task_id` → 轮询，**协议形态完全不同**。
把它们填进模型列表，表现是调用报错或长时间无响应。

> 生成器（`gen_import_config.py`）已自动只挑 `type_code=text 且 call_type≠2` 的模型。

---

## 二、58 个文本模型怎么挑

### 通用对话 / 日常

| 模型 ID | 适用 |
|---|---|
| `DeepSeek-V4-Flash` | 快、便宜，日常首选 |
| `DeepSeek-V4-Pro` | 复杂推理、长文 |
| `Qwen3.6-Plus` | 综合能力强 |
| `Qwen3.6-Flash` | 轻量快速 |
| `GLM-5.2` / `GLM-5.1` | 中文场景 |
| `Kimi-K2.6` / `kimi-k3` | 长上下文 |
| `gpt-5.6-sol` / `gpt-5.5` | 国际模型对照 |

### 写代码

| 模型 ID | 说明 |
|---|---|
| `Qwen3-Coder-Next` | 代码主力 |
| `Qwen3-Coder-30B-A3B-Instruct` | 轻量代码 |
| `Kimi-K2.7-Code` | 代码专用 |
| `KAT-Dev` | 开发场景 |

### 支持视觉（能传图）

实测仅 **4 个**：

```
qwen3.6-plus
PaddleOCR-VL-1.5
Qwen3-VL-30B-A3B-Instruct
ERNIE-4.5-Turbo-VL
```

在 Chatbox 里要给这些模型**勾上 `vision` 能力**，否则它不会把图片发给模型。

### 支持深度推理

实测仅 **2 个**：

```
qwen3.6-plus
ERNIE-5.0-Thinking
```

在 Chatbox 里**勾上 `reasoning`**。

> ⚠️ **推理模型会把 token 先花在思维链上**。实测 `DeepSeek-V4-Flash` 在
> `max_tokens=8` 时 `content` 返回 `null`（`finish_reason=length`），加到 200 才正常。
> 如果你在 Chatbox 里把最大输出调得很小，推理模型可能"什么都不输出"。

### 垂类专业模型

`Fin-R1`、`DianJin-R1-32B`（金融）、`LegalOne-8B`（法律）、
`Sinong1.0-32B`（农学）——按业务场景挑。

---

## 三、模型名必须用真名

网关的模型 ID **区分大小写**，且同一厂商可能有多个近似条目。例如：

- `Qwen3.6-Plus`（大写开头）与 `qwen3.6-plus`（小写）**是两条不同记录**
- 厂商字段（`vendor_name`）有标注串味（`veo3.1` 系落在 `xAI` 分组等），
  **不要用厂商字段做匹配，一律用 `model_code`**

**取真名的唯一正确方式**：

```bash
# 用 one-key-ai-gateway 技能包的客户端
python -X utf8 ..\one-key-ai-gateway\scripts\client.py models

# 或直接打接口
GET https://api.a7w.cn/api/v1/models
```

---

## 四、Chatbox 里怎么配能力

在 Chatbox 的模型条目上：

| 网关字段 | Chatbox 勾选 |
|---|---|
| `supports_vision: 1` | ✅ `vision`（视觉） |
| `supports_reasoning: 1` | ✅ `reasoning`（推理） |
| 都为 0 | 都不勾（当普通文本模型） |

不勾的后果：能力对不上时 Chatbox 不会按对应方式调用——比如某模型支持视觉但你没勾，
它就不会把图片传过去。

`gen_import_config.py` 生成配置时会**自动映射这两个字段**，所以一键导入通常不用手改。

---

## 五、模型清单会变

- 实测 **75 个**（58 文本 / 12 图片 / 5 视频）
- 官网口径写 **87+**，宣传页写 89+
- 模型上下架频繁

**要准数就现场打 `GET /v1/models`**，不要用任何文档里的快照数字做判断依据。

---

## 六、没有的能力（容易踩空）

| 缺什么 | 影响 |
|---|---|
| **embedding 模型** | Chatbox 的知识库/向量化功能无法用本网关 |
| **rerank 模型** | 同上 |

网关 75 个模型里**没有 embedding、没有 rerank**。如果你要用 Chatbox 的知识库功能，
需要另配本地 embedding（如 bge-m3）。
