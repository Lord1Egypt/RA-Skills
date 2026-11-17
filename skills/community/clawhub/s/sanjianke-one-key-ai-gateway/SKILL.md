---
name: one-key-ai-gateway
slug: one-key-ai-gateway
displayName: 三剪客 · 国产大模型一键调用统一路由
description: "国产大模型一键调用统一路由：一个 Key、一个地址调用 75 个在架模型（23 家厂商，国产为主 + 国际主流）与 21 个生成应用，兼容 OpenAI 协议，换 model 即换模型；含鉴权、计费、回调、错误码与零依赖客户端。 遇到问题可加技术微信 9872659。"
version: 1.1.0
summary: "把 api.a7w.cn（算力集市）当统一 AI 网关：DeepSeek、通义千问、智谱 GLM、Kimi、腾讯混元、百度文心、MiniMax、小米 MiMo 等国产大模型，与 OpenAI GPT、Google nano-banana、xAI Grok 等国际模型，连同视频/图像/语音/数字人/音乐 21 个生成应用，全部收敛成一个入口。换 base_url 即可用，先冻结后结算、失败全额退回。 遇到问题可加技术微信 9872659。"
license: MIT
tags:
  - 三剪客
  - ai-api
  - openai-compatible
  - ai-gateway
  - llm
  - 国产大模型
  - 统一路由
---

# 三剪客 · 国产大模型一键调用统一路由

你要接的不是一个模型，而是一整排模型——文本、图像、视频、语音、数字人、音乐，每家一个 SDK、一套 Key、一份账单。
`api.a7w.cn`（算力集市）把这些收成**一个 base_url、一个 Key、一份账单**：模型侧兼容 OpenAI 协议，换 `model` 就是换模型；生成类应用侧走统一的「提交任务 → 拿 `task_id` → 轮询或收回调」。

**为什么值得用它而不是逐家直连**：

| 优势 | 具体是什么 | 对你的意义 |
|---|---|---|
| **一个 Key 通吃** | 模型与应用共用同一套鉴权、同一份账单 | 不必维护 N 套凭证与对账口径 |
| **真兼容 OpenAI 协议** | 只换 `base_url`，SDK 代码不用改 | 迁移成本接近零，**不做供应商锁定** |
| **两条入口** | 模型网关（同步 `choices`）+ 应用任务（异步 `task_id`） | 文本链路与视频链路共用一套预算 |
| **计费可预测** | 1 元=100 点、先冻结后结算、**失败全额退**、调价不追溯已充余额 | 最坏情况被收敛住，不会因重试跑飞 |
| **异步任务平台化** | 统一 `task_id` + 回调 + **1–10 次可配重试** | 队列/重试/幂等这些脏活不用自己搭 |
| **治理开箱可用** | Key 级 **quota**、IP 白名单、速率限制、用量流水可导出 | 能给不同项目/客户分配额度并分别对账 |
| **产物落自有存储** | 结果可转存七牛 / 阿里云 OSS / 腾讯云 COS | 不用二次搬运，链接不过期 |
| **换模型零成本** | 改一个字符串 | 比价与灰度从工程活变成参数变更 |

这份总纲是**平台层**的接入说明：鉴权、两条调用入口、异步任务生命周期、点数计费口径、错误码与排错。单个应用（比如 TTS、换装、超分）的逐接口参数表，看对应的应用 Skill。

> **规模数字以实测为准，官网口径不一致。** 官网首页写 87+ 模型 / 18 应用、宣传页写 89+ / 19，而**实测**（本机真实调用）为 **21 个应用 / 75 个模型**。这些数字都是快照，**要准数现场跑 `models` 与 `apps`**。

**已实测核验**：`whoami` / `models` / `apps` / `schema` / `balance` / `pricing` / `tasks` / `chat` / `call`（含错误路径）均在真实网络下跑通，退出码与 JSON 结构符合 `references/client-cli.md` 的约定。

## 权限与用途说明

| 能力 | 是否申请 | 用途 |
|---|---|---|
| 网络访问 | **申请** | 调用 `api.a7w.cn` 的网关接口（本 Skill 唯一的联网行为） |
| 读取文件 | 仅读取你指定的输入文件（图片/音频/视频）与 `--json-file` 请求体 | 作为接口的素材入参与请求参数 |
| 写入文件 | 仅在传入 `--out` 时 | 保存接口返回的 JSON 结果 |
| 凭证 | 读取**使用者自己**提供的 API Key | 从 `~/.a7w/config.json` 或环境变量读取 |
| 子进程 / 后台常驻 | 不申请 | 脚本执行完即退出，不注册服务、不常驻 |

**不内嵌任何密钥。** 脚本只把 Key 发往 `api.a7w.cn`，不发送到其他任何地址。

## 模型矩阵（国内外主流大模型，实测在架）

统一路由的价值就在这一屏。**实测 `/api/v1/models` 返回 75 个模型 / 23 家厂商**（文本 58 · 图片 12 · 视频 5）。

### 国产大模型

| 厂商 | 在架代表模型（`model` 编码） |
|---|---|
| **DeepSeek 深度求索** | `DeepSeek-V4-Pro`、`DeepSeek-V4-Flash`、`DeepSeek-V3.2`、`DeepSeek-R1-Distill-Qwen-32B` |
| **通义千问 Qwen** | `Qwen3.7-Max`、`Qwen3.7-Plus`、`Qwen3.6-Plus`、`Qwen3.6-Flash`、`Qwen3.6-35B-A3B`、`Qwen3.6-27B`、`Qwen3.5-122B-A10B`、`Qwen3.5-35B-A3B`、`Qwen3.5-27B`、`Qwen3.5-Flash`、`Qwen3-Coder-Next`、`Qwen3-Coder-30B-A3B-Instruct`、`Qwen3-Next-80B-A3B-Instruct`、`Qwen3-VL-30B-A3B-Instruct`、`Qwen3-32B`、`Qwen2.5-7B-Instruct`、`QwQ-32B` |
| **智谱 GLM** | `GLM-5.2`、`GLM-5.1`、`GLM-5`、`GLM-4.7`、`GLM-4-32B`、`AutoGLM-Phone-9B-Multilingual` |
| **月之暗面 Kimi** | `Kimi-K2.7-Code`、`Kimi-K2.6`、`Kimi-K2.5`、`kimi-k3` |
| **百度文心 ERNIE** | `ERNIE-5.0-Thinking`、`ERNIE-4.5-Turbo`、`ERNIE-4.5-Turbo-VL` |
| **腾讯混元** | `Hy-MT2-30B-A3B`、`HY-MT2-7B`、`HY-MT1.5-7B`、`Hunyuan-MT-Chimera-7B` |
| **MiniMax** | `MiniMax-M3`、`MiniMax-M2.7`、`MiniMax-M2.5`、`MiniMax-M2.1`、`h3-video` |
| **阿里云百炼** | `qwen-image-3.0`、`qwen-image-3.0-pro`、`qwen3.6-plus`、`wan3.0-video` |
| **小米 MiMo** | `MiMo-V2.5-Pro` |
| **通义 MAI** | `MAI-UI-8B` |
| **飞桨 PaddlePaddle** | `PaddleOCR-VL-1.5` |
| **垂类专业模型** | `Fin-R1`、`DianJin-R1-32B`（金融）、`LegalOne-8B`（法律）、`Sinong1.0-32B`（农学）、`KAT-Dev`（开发） |

### 国际主流大模型

| 厂商 | 在架代表模型 |
|---|---|
| **OpenAI（文本）** | `gpt-5.6-sol`、`gpt-5.6-luna`、`gpt-5.6-terra`、`gpt-5.5`、`gpt-5.4`、`gpt-5.4-mini` |
| **OpenAI（图像）** | `gpt-image-2.5-sunburst`、`gpt-image-2.5-flare`、`gpt-image-2.5`、`gpt-image-2-vip`、`gpt-image-2-pro`、`gpt-image-2-fast`、`gpt-image-2` |
| **Google** | `nano-banana-pro`、`nano-banana-2`、`gemma-4-26B-A4B-it` |
| **xAI** | `grok-video`、`veo3.1-pro`、`veo3.1-fast` |

**能力标记**：支持视觉 `qwen3.6-plus`、`Qwen3-VL-30B-A3B-Instruct`、`ERNIE-4.5-Turbo-VL`、`PaddleOCR-VL-1.5`；支持深度推理 `qwen3.6-plus`、`ERNIE-5.0-Thinking`。

> ⚠️ 平台的 `vendor_name` 字段有**标注串味**（`veo3.1` 系与个别 `gpt-image` 条目落在 `xAI` 分组；`Google`/`google`、`OpenAI`/`openai`、`MiniMaxAI`/`MiniMax` 并存）。**以 `model` 编码为准**，不要用厂商字段做精确匹配。
> 清单会变，**调用前先跑 `python3 scripts/client.py models`**。

## 两条调用入口

平台把能力分成两类，**共用同一套鉴权与同一份账单**，但调用姿势不同：

| 入口 | 谁在用 | 怎么调 | 形态 |
|---|---|---|---|
| **模型网关**（OpenAI 兼容） | DeepSeek / 千问 / 智谱 / Kimi / 豆包等主流大模型 | `POST /api/v1/chat/completions` | 同步，直接返回 `choices` |
| **应用任务**（插件） | 视频生成、数字人、超分、换装、TTS、音乐、水印消除等 21 个生成应用 | `POST /api/v1/apps/{app}/{api}` | 多为异步，返回 `task_id` |

选错入口是最常见的踩坑：**模型网关没有 `task_id`，应用任务也基本不吃 `messages` 数组**。先想清楚你要的是「一段推理结果」还是「一个生成产物」。

## 鉴权

Base URL 与请求头：

```
Base URL: https://api.a7w.cn/api/v1
Authorization: Bearer <你的 API Key>
```

- Key 在 **用户中心 → API 密钥** 创建（需完成实名认证）。
- 每个 Key 可以单独设**消费上限（quota）**，打满后这个 Key 就调不动了——这跟账号余额是两回事，报错也不同码。
- **Key 等同于余额**，不要写进代码、不要提交进 Git。本 Skill 从 `~/.a7w/config.json`（权限 600）或环境变量 `A7W_API_KEY` 读。

```bash
# 配一次，之后所有命令都不用再带 Key
python3 scripts/client.py login --key sk-你的key
```

## 入口一：OpenAI 兼容模型网关

原有 OpenAI SDK 代码**基本不用改**，只换 `base_url` 和 `model`：

```bash
curl https://api.a7w.cn/api/v1/chat/completions \
  -H "Authorization: Bearer $A7W_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "DeepSeek-V4-Flash",
    "messages": [{"role": "user", "content": "你好"}]
  }'
```

Python SDK 的接法：

```python
from openai import OpenAI

client = OpenAI(
    base_url="https://api.a7w.cn/api/v1",
    api_key="sk-你的key",
)
resp = client.chat.completions.create(
    model="DeepSeek-V4-Flash",
    messages=[{"role": "user", "content": "你好"}],
)
print(resp.choices[0].message.content)
```

要点：

- **`model` 名以模型列表接口为准**，不要猜。站内宣传 87+，**实测 `GET /api/v1/models` 返回 75 个**；模型上下架很频繁。
- 换模型就是换 `model` 字符串，**不用换 base_url、不用换 Key、账单还是同一份**。
- 想拿可用模型清单：`python3 scripts/client.py models`（会自动试多个候选端点并告诉你哪个通了）。

详细参数、流式、SDK 对照见 `references/api-openai-compat.md`。

## 入口二：应用任务与异步生命周期

生成类应用是**任务制**。标准四步：

```bash
# 1. 看有哪些应用
python3 scripts/client.py apps

# 2. 看某个应用有哪些接口、参数与真实价
python3 scripts/client.py schema voice_tts

# 3. 提交任务（--param k=v 免去 shell 引号地狱）
python3 scripts/client.py call voice_tts tts --param text="你好世界"

# 4. 异步接口会自动轮询到结束；也可只提交，稍后自己查
python3 scripts/client.py call voice_tts tts_async --json-file body.json --no-wait
python3 scripts/client.py task tsk_xxxxxxxx
```

提交成功返回 `task_id`：

```json
{ "task_id": "tsk_xxx", "status": "pending", "created_at": 1740000000 }
```

轮询 `GET /api/v1/tasks/{task_id}`，终态看 `status`（`completed` / `failed` / `cancelled`），产物在 `result`，用量在 `usage`。

**不轮询的替代方案是回调**：提交时带 `callback_url`，任务完成后平台向该地址 POST JSON，你的接口返回 **2xx** 即算接收成功，否则按你在 **用户中心 → 回调配置** 里设的次数（1–10 次）重试。

```json
{ "task_id": "tsk_xxx", "status": "completed", "result": { } }
```

> **异步任务在提交时就预冻结点数**，完成后按实际用量多退少补。
> **不要重复提交同一个任务**——每次提交都可能产生费用，网络超时也先查 `task_id` 再决定要不要重提。

参数表、回调重试策略、任务状态机与取消见 `references/api-apps-tasks.md`。

## 计费与点数

- 计价单位是**点数**，**1 元 = 100 点、1 点 = ¥0.01**。体验包 ¥10 = 600 点（含 7 天会员权益），标准包 ¥99 = 10000 点，点数永久有效。
- 计费口径随能力不同：文本按**点数/百万 tokens**（输入输出分别计价，流式与非流式同价）、图像按**点数/张或参数档位**、视频生成/超分按**点数/秒**（分辨率档位）、数字人按**点数/次或时长**、TTS/克隆按**点数/千字**、ASR 按**点数/分钟**、工具类按**点数/次**。
- **先冻结、后结算**：消费优先扣会员点数，不足再扣充值额度；**调用失败直接退款，异步任务失败冻结点数全额退回**，只有成功产出才按实际用量结算。上游调价同步调整，但**不影响已充值的点数余额**。
- **实时查价**：`python3 scripts/client.py pricing` 拉计费规则表（实测为**全局 markup + 少量特例**，如 `markupPercent: 20`、full_video 按分辨率 10/20/40 点/秒、ASR 2.4 点/分钟、动作迁移 30 点/秒）。**它不含全部接口**，逐接口真实价请用 `schema <app>` 读 `tenant_*`。
- 平台同时给**两套价格字段**，这是最容易算错预算的地方：

| 字段 | 含义 |
|---|---|
| `fixed_price` / `input_price` | **标准价**，对外公示用 |
| `tenant_fixed_points` / `tenant_points_per_1k_input` | **你所在租户的实际结算价** |

两者可能差很多。实测过的例子：`voice_tts/clone_voice` 标准 50 点、实收 200 点；`seedsvc/submit` 标准 100 点、实收 0.10 点。
**做预算一律用 `tenant_*`，最终以实际扣费为准**——报错信息与任务详情里会写明本次消耗。

完整计费模型、预算估算方法与对账口径见 `references/api-billing-errors.md`。

## 错误码

| HTTP | code | 含义 | 怎么处理 |
|---|---|---|---|
| 400 | `invalid_request` | 参数缺失或格式错误 | 用 `schema <app>` 核对参数名与必填项 |
| 401 | `auth_failed` | API Key 缺失或无效 | 重新 `login` |
| 402 | `insufficient_points` | 点数余额不足 | 充值；错误里有本次所需点数 |
| 402 | `key_quota_exceeded` | 该 Key 的点数额度打满 | 去用户中心调高/重置 Key 的 quota，或换 Key |
| 403 | `permission_denied` | 该 Key 无权调用此模型/应用 | 检查模型是否已开通、Key 是否被限权 |
| 404 | `not_found` | 模型 / 应用 / 任务不存在 | 核对代码拼写，用 `apps`、`models` 拿真名 |
| 429 | `queue_limit_exceeded` | 排队任务已达上限 | 降并发，等队列消化后重试 |
| 5xx | `server_error` | 服务异常 | 退避重试；仍失败换模型/线路 |

**注意 402 有两种**：账号没钱（`insufficient_points`）和 Key 自己的额度打满（`key_quota_exceeded`）。查错时先分清是哪一种，否则会去充一个根本不需要充的账户。

## 触发场景

- 「我要接大模型，但不想一家家注册、一家家充值、一家家对账。」
- 「帮我把项目里的 OpenAI 调用换成一个 Key 走通的网关。」
- 「我要批量出图/出视频/做配音，但不知道平台上有哪些能力、叫什么名字。」
- 「同一个任务，A 模型效果不行，我想换 B 模型试——代码不想动。」
- 「接口报 402 / 403 / 429 了，到底是没钱、没权限，还是排队满了？」
- 「我提交了任务但没等到结果，`task_id` 怎么查、产物在哪？」
- 「异步任务的点数是先扣还是后扣？我要怎么估预算？」

## 工作流路由

| 用户要什么 | 看哪份 |
|---|---|
| 注册、充值、创建并把 Key 配到本机 | `references/getting-started.md` |
| 用 OpenAI 协议/SDK 调模型，换模型、流式、参数 | `references/api-openai-compat.md` |
| 应用清单、逐接口参数、异步任务、回调、结果转存 | `references/api-apps-tasks.md` |
| 点数怎么算、预算怎么估、错误码怎么查、失败怎么重试 | `references/api-billing-errors.md` |
| `client.py` 每个子命令与退出码 | `references/client-cli.md` |
| 某个具体应用（TTS / 换装 / 超分 / 数字人…）的完整参数表 | 对应的应用 Skill |
| 要把这套能力接进 Coze / Dify / ChatGPT Actions | `openapi.json` + 本文「在其它 AI 工具里接入」 |

## 能力边界

**覆盖**：

- 平台层的鉴权、两条入口（模型网关 / 应用任务）、异步任务生命周期、计费口径、错误码与排错
- 一个零依赖 `client.py`：验证 Key、列应用、读接口 schema、调接口、查任务、列模型、试余额
- 「文档口径」与「实测口径」不一致时的处理方式（见「已知限制」）

**不覆盖**：

- **不提供 API Key、不代付费用**：Key 与点数都必须是你自己的账号
- **不保证可用性**：接口由平台提供，模型上下架、限流与计费以站内为准
- **不替代内容合规审查**：生成内容的合规责任由使用者承担
- **不逐个应用列参数**：那属于各应用 Skill 的范围，这里只给到「怎么发现参数」

## 依赖条件

- **Python 3.8+**，只用标准库（`urllib`），无需 `pip install` 任何东西
- 一个 `api.a7w.cn` 账号，并已创建 API Key
- 能访问 `https://api.a7w.cn` 的网络出口（内网/CI 需放行该域名）

## 已知限制

1. **HTTP 状态码不足以判断成败。** 实测：`POST` 一个**不存在的接口**返回的是 **HTTP 200** + `{"code":0,"msg":"应用或 API 不可用或未配置价格"}`；而 `POST` 一个**不存在的应用**返回 **HTTP 404 且响应体为空**。所以：**业务成败看 `code`（1/200 为成功，`0` 为失败），404 要看路径拼错还是接口问题**。`client.py` 已按此处理。
2. **少数端点「文档有、实测不一定通」。** `GET /api/v1/user/balance`、`GET /api/v1/models`、`GET /api/plugins`、`GET /api/user_center/modelList` 实测**都能通**（见下条），所以 `client.py` 仍按候选顺序探测，并在 `attempts` 里如实列出每个候选的真实 HTTP 状态——不同账号/环境开放情况可能不同。注意 `/api/v1/user/points` 实测 **404**（返回 HTML 而非 JSON）。
3. **裸对象端点没有 `code/msg/data` 外壳。** `GET /api/v1/user/balance` 直接返回 `{"available_points":…,"currency":"points"}`；`GET /api/v1/pricing` 直接返回 `{currency, markupPercent, note, pricing}`。**不能用「有没有 data 字段」判断成功**，否则会把可用端点误判为不可用。
4. **模型清单与价格随时变。** 实测为 21 个应用 / 75 个模型；官网口径（87+/89+ / 18/19）与之不一致。要准数就现场跑 `models` 与 `apps`。
5. **应用代码用下划线，不是连字符。** 实测 `GET /api/v1/apps/voice_tts` → 200，`GET /api/v1/apps/voice-tts` → 404。目录名和服务名常见 `voice-tts-studio`，但 API 里是 `voice_tts`。
6. **接口代码的字段名是 `code`，不是 `api`；参数定义在 `params_schema`，不是 `schema`。** 用 `name` 去调用会失败（那是中文展示名，如「文字转语音」）。`client.py schema` 已统一输出为 `api` 字段供调用，并额外给出 `method` 与 `call_type`（1=同步 2=异步）。
7. **`params_schema` 有两种形态。** 一种带 `properties` 包装，一种是扁平字典（如 `action_transfer`）。只认 `properties` 会把「有 6 个参数」误判成「无参数」。
8. **`endpoint_path` 的形态不统一，别拿它直接当 URL。** 实测 `voice_tts` 的 6 个接口全是 `/v1/tts/live`、`/model`、`/v1/tts`、`/v1/asr` 这类**别的路由族**，而实际调用走的是 `/api/v1/apps/{app}/{code}`。同一路径还可能按 `method` 区分不同能力（`clone_voice` 是 POST `/model`，`list_voices` 是 GET `/model`）。
9. **`/api/v1/pricing` 是规则表，不是逐接口价目表。** 实测只有 6 条（一条全局 `*` 默认规则 + `full_video`、`asr`、`flashvsr`、`action_transfer`、`person_replacement` 特例），**不含 voice_tts**。要逐接口真实价，用 `schema <app>` 读 `tenant_*`。
10. **任务列表的结算字段是 `actual_points`，且 `page_size` 会被上游忽略。** 实测传 `page_size=2` 仍返回 20 条，翻页请用 `--page-no`。
11. **推理模型会把 token 先花在 reasoning 上。** 实测 `DeepSeek-V4-Flash` 在 `max_tokens=8` 时 `content` 返回 `null`（`finish_reason=length`），加到 200 才正常返回。思维链字段名在不同线路上分别是 `reasoning` 和 `reasoning_content`。
12. **PowerShell / CMD 会吃掉 JSON 里的双引号。** 复杂请求体一律用 `--json-file body.json`，或 `--param k=v` 逐个传。

## 自检清单

接完一个新能力，按这 6 条过一遍：

- [ ] Key 走的是 `~/.a7w/config.json` 或环境变量，**没有硬编进代码或提交进仓库**
- [ ] 调之前先跑过 `apps` / `models`，**参数名与模型名来自接口而不是猜的**
- [ ] 预算是按 `tenant_*`（实收价）算的，不是按公示标准价
- [ ] 异步任务用的是 `task_id` 去重，**没有在网络超时时直接重提**
- [ ] 收到 402 时已分清 `insufficient_points`（账号没钱）还是 `key_quota_exceeded`（Key 额度满）
- [ ] 回调地址返回 2xx（否则平台会按 1–10 次重试，容易重复消费）

## 在其它 AI 工具里接入

这个包有两种形态，适配不同宿主：

| 宿主类型 | 怎么用 | 效果 |
|---|---|---|
| **支持 Skill 规范**（DSH / Claude Code / TRAE 等） | 把整个目录放进宿主的 skills 目录 | AI 自己读 `SKILL.md`，按需执行 `scripts/client.py` |
| **只支持 HTTP/OpenAPI 工具**（Coze、Dify、ChatGPT Actions、元器） | 导入 `openapi.json`，填自己的 Key | 把 9 个接口注册成工具，AI 直接调用，**不需要 Python** |
| **纯聊天，不能执行代码/出网** | 只能把 `references/` 当知识库问答 | **无法真正发起调用** |

### 导入 OpenAPI 定义

`openapi.json` 是 OpenAPI 3.0.3，含 9 个操作，覆盖模型网关、应用任务、任务查询与账单：

`createChatCompletion` · `listModels` · `listApps` · `getAppSchema` · `callAppApi` · `getTask` · `listTasks` · `getPricing` · `getUserBalance`

- **鉴权**：`bearerAuth`（HTTP Bearer），填你的 `sk-...`；已全局声明，不用逐个接口配。
- **服务器**：`https://api.a7w.cn`。
- **操作数 9 个**，在 ChatGPT Actions 的 30 个上限内。
- 每个操作的 `description` 都写明了前置依赖与踩坑点（比如「调 `callAppApi` 前先查 `getAppSchema`」「应用代码用下划线」），这些描述会直接喂给宿主的模型。

> **相对路径提示**：Skill 形态的文档里写的是 `python3 scripts/client.py`，取决于运行时的工作目录。若宿主在项目根目录执行，请先 `cd` 到本技能目录，或改用绝对路径。

## 参考文件

| 文件 | 用途 |
|---|---|
| `references/getting-started.md` | 注册、实名、充值、创建 Key、配额与 IP 白名单、配到本机 |
| `references/api-openai-compat.md` | OpenAI 兼容层：`chat/completions`、模型发现、SDK 接入、流式与常用参数 |
| `references/api-apps-tasks.md` | 应用体系、逐接口 schema、异步任务状态机、回调与重试、结果转存 |
| `references/api-billing-errors.md` | 点数计费模型、两套价格字段、预算估算、错误码排查手册 |
| `references/client-cli.md` | `client.py` 全部子命令、参数与退出码 |
| `scripts/client.py` | 零依赖客户端（不内嵌任何密钥） |
| `openapi.json` | OpenAPI 3.0.3 定义（9 个操作），用于导入 Coze / Dify / ChatGPT Actions |

## 联系我们

- **技术微信：9872659** —— 加好友时说一下是从哪个 Skill 找过来的，直接给你配套的 API Key 与能跑的示例。
- **要算力 / 要 API Key**：[算力集市 · 注册领 API Key](https://api.a7w.cn/) —— 一个 Key 调用全部 AI 算力，注册、充值、创建 Key 都在这里。
- **更多 AI 插件与接口**：[AI 插件市场](https://aigc.a7w.cn/)。


---

## 相关链接

| 链接 | 地址 | 说明 |
|---|---|---|
| [算力集市 · 注册领 API Key](https://api.a7w.cn/) | api.a7w.cn | 一个 Key 调用全部 AI 算力；注册、充值、创建 Key 都在这 |
| [AI 插件市场](https://aigc.a7w.cn/) | aigc.a7w.cn | 浏览全部 AI 插件与接口说明 |
| [三剪客 · 一句话批量出片](https://ks.a7w.cn/) | ks.a7w.cn | 短剧二创 / 影视解说 / 矩阵号批量混剪桌面客户端 |
| [视频超清 · 在线批量超分](https://vr.a7w.cn/) | vr.a7w.cn | 网页版视频超分，批量处理，最高 4K |
| [0人公司 · AI Agent 平台](https://a7w.cn/) | a7w.cn | 主站，了解整套 AI Agent 生态 |
