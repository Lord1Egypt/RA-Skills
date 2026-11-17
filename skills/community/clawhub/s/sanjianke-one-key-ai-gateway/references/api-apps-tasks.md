# 应用任务：清单、参数、异步生命周期

「应用」（也叫插件）是生成类能力的载体：出图、换装、超分、配音、数字人、音乐、混剪。
模型网关给的是**一段推理结果**，应用给的是**一个生成产物**——这是两条不同的路。

## 1. 应用清单

```bash
python3 scripts/client.py apps --brief        # 只要代码与名称
python3 scripts/client.py apps                # 完整字段
```

接口：`GET /api/v1/apps`。实测该端点可用；客户端仍保留 `GET /api/plugins` 作为回退候选（实测也返回 200，但只有 13 条、结构不同），并在 `endpoint` 字段告诉你实际用了哪个。

站内宣传口径为 18~19 个应用，但**实测 `GET /api/v1/apps` 返回 21 个**。以下为实测全量清单（代码 → 平台名称）：

| 应用代码 | 平台名称 |
|---|---|
| `voice_tts` | 语音TTS |
| `music_generation` | 音乐生成 |
| `music_search` | 音乐搜索 |
| `seedsvc` | 音色修改、AI翻唱 |
| `mmaudio` | 音效生成、视频配音 |
| `full_video` | 全能视频生成 |
| `wan` | Wan 视频生成 |
| `seedance` | Seedance 2.0 |
| `grok_video` | Grok 视频生成 |
| `happy_horse` | Happy Horse |
| `flashvsr` | 视频超分 |
| `smart_clip` | 智能剪辑 |
| `image_human` | 全驱动数字人 |
| `pic_lipsync` | 图片数字人 |
| `lipsync` | 数字人对口型 |
| `dressing_diffusion` | AI换装 |
| `person_replacement` | 人物替换 |
| `action_transfer` | 动作迁移 |
| `nano_banana` | nano-banana |
| `watermark_removal` | 水印消除 |
| `file_qa` | 文件问答 |

> ⚠️ **应用代码用下划线，不是连字符。** 仓库目录名、Skill 名常见 `voice-tts-studio`，但 API 里的代码是 `voice_tts`。实测 `GET /api/v1/apps/voice-tts` 返回 **404**，`/api/v1/apps/voice_tts` 返回 200。

## 2. 读一个应用的接口与参数

```bash
python3 scripts/client.py schema voice_tts
```

接口：`GET /api/v1/apps/{app}`

返回里每个接口都带这几样，**把它们当成唯一事实来源**：

| 真实字段 | 含义 |
|---|---|
| `code` | **接口代码**，如 `tts`、`submit`、`create`——调用时用它 |
| `name` | 中文展示名（如「文字转语音（Live·异步）」）——**不要拿它去调用** |
| `method` | HTTP 方法，`POST` 或 `GET` |
| `call_type` | `1` = 同步，`2` = 异步 |
| `endpoint_path` | 该接口在平台内的真实路径（**形态不统一，见 3.2**） |
| `params_schema` | **参数定义**（注意不是 `schema`） |
| `tenant_fixed_points` | **你的实际按次结算价**（点数） |
| `tenant_points_per_1k_input` / `tenant_points_per_1k_output` | **你的实际按千字 / 千 token 结算价**（点数） |
| `fixed_price` / `input_price` | 公示标准价 |

> **两个最容易踩的字段名**：接口代码是 `code`（不是 `api`）；参数定义是 `params_schema`（不是 `schema`）。
> 实测 `voice_tts` 的 6 个接口：`tts_live`(异步) / `clone_voice`(同步) / `tts`(同步) / `tts_async`(异步) / `stt`(同步) / `list_voices`(GET)。

客户端的 `schema` 子命令把这些整理成一份 `apis` 数组（统一把接口代码输出为 `api` 字段，附带 `method`、`call_type`、参数与价格），省得你手翻原始 JSON。

## 3. 三个真实存在的坑

### 3.1 `params_schema` 有两种形态

```jsonc
// 形态 A：带 properties 包装
{ "type": "object", "properties": { "text": {...}, "model": {...} }, "required": ["text"] }

// 形态 B：扁平字典（例如 action_transfer）
{ "text": {...}, "model": {...} }
```

**只认 `properties` 的通用解析器会把形态 B 判成「这个接口没有参数」。**
本 Skill 的 `schema` 子命令两种都认：先找 `properties`，找不到就把除元数据键之外的顶层键当作参数。

### 3.2 `endpoint_path` 的形态不统一（最容易踩）

实测发现同一个字段至少有这几种形态：

| 形态 | 真实例子 | 说明 |
|---|---|---|
| 另一套路由族 | `/v1/tts`、`/v1/tts/live`、`/v1/asr`、`/model`（voice_tts 全部 6 个都属此类） | 不在 `apps/{app}` 之下 |
| 相对路径 | `/flashvsr/submit`、`/seedsvc/submit`、`/action_transfer/submit` | 需要自己拼到应用前缀后面 |
| 绝对路径 | `/api/v1/apps/grok_video/submit` | 已经是完整路径，**再拼一次就错** |
| 带占位符 | `/v1/tasks/{task_id}` | 路径里含变量 |

而**实际可用的调用方式**是 `POST /api/v1/apps/{应用代码}/{接口代码}`——按「应用代码 + `code` 字段」拼，与 `endpoint_path` 无关。所以：

> **把 `endpoint_path` 当参考信息，不要当 URL 用。** 调用路径统一按 `apps/{app}/{code}` 拼；`endpoint_path` 用来说明上游实际打到哪里。
> 另外同一个 `endpoint_path` 可能按 `method` 区分不同能力：`clone_voice` 是 `POST /model`，`list_voices` 是 `GET /model`。

### 3.3 接口代码基本是简单单词，但要看 `code` 而不是 `name`

实测 21 个应用的接口代码都是 `tts`、`submit`、`query`、`create`、`remove`、`search` 这类简单单词，**没有占位符**。
真正会出错的是**拿 `name`（中文展示名）去调用**——那一定失败。

## 4. 提交任务

```bash
# 方式一：--param（推荐，免 shell 引号问题）
python3 scripts/client.py call voice_tts tts --param text="你好世界"

# 方式二：--json-file（复杂嵌套参数用这个，最稳）
python3 scripts/client.py call smart_clip realman_broadcast --json-file body.json

# 方式三：--json（PowerShell/CMD 会吃掉内部双引号，慎用）
python3 scripts/client.py call voice_tts tts --json '{"text":"你好"}'
```

对应的 HTTP：

```bash
curl -sS -X POST "https://api.a7w.cn/api/v1/apps/voice_tts/tts" \
  -H "Authorization: Bearer $A7W_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"text":"你好世界"}'
```

响应固定带 `code` / `msg` / `data` 外壳（`code` 为 `1` 或 `200` 表示成功）：

```json
{ "code": 1, "msg": "ok",
  "data": { "task_id": "tsk_xxx", "status": "pending", "created_at": 1740000000 } }
```

> ⚠️ **`code` 为 `0` 表示失败，且 HTTP 状态码仍是 200。** 实测：
> - `POST /api/v1/apps/voice_tts/__不存在的接口__` → **HTTP 200** + `{"code":0,"msg":"应用或 API 不可用或未配置价格","data":null}`
> - `POST /api/v1/apps/__不存在的应用__/submit` → **HTTP 404 且响应体为空**
>
> 所以：**不要只看 HTTP 状态码判断成败**，务必检查 `code`（`1`/`200` 为成功，`0` 为失败）。

**如果 `data` 里没有 `task_id`，说明这是个同步接口**，结果已经在 `data` 里了。客户端的 `call` 会自动区分这两种情况并标注 `mode: sync` / `mode: async`。

## 5. 异步生命周期

```
提交 → pending → processing → completed
                        └──→ failed / cancelled
```

查询任务：

```
GET /api/v1/tasks/{task_id}
```

```bash
python3 scripts/client.py task tsk_xxxxxxxx
```

任务详情里关注四个字段：

| 字段 | 说明 |
|---|---|
| `status` | `pending` / `processing` / `completed` / `failed` / `cancelled` |
| `result` | 产物。视频常见 `result.data.videoUrl`，音频常见音频 URL |
| `actual_points` | **结算点数**（任务列表里的真实字段名；不要找 `usage.points_cost`） |
| `error` | 失败原因，通常是上游处理失败（`error.message`） |

实测任务条目的字段为：`task_id`、`model_code`、`channel_code`、`type_code`、`call_type`、`status`、`actual_points`、`response_time_ms`、`completed_at`、`created_at`。
其中 `model_code` 对应用任务形如 `voice_tts/tts`（应用代码/接口代码），对模型调用则是模型名。

> 实测真实消耗参考：`DeepSeek-V4-Flash` 一次普通问答约 **0.74~0.99 点**；极小的调用（`max_tokens=8`）为 **0.00 点**。

列出最近任务（用于估算消耗）：

```bash
python3 scripts/client.py tasks --page-size 50
```

对应 `GET /api/v1/tasks?page_no=1&page_size=50`。

> ⚠️ **实测 `page_size` 会被上游忽略**：传 `page_size=2` 仍返回默认 20 条。翻页请用 `--page-no`，客户端会在 `note` 里提示这一点。

### 5.1 轮询与超时

- 客户端 `call` 默认**轮询到终态**再返回，间隔 6 秒，上限 30 分钟（`--interval` / `--timeout` 可调）。
- 只想提交不等结果：`--no-wait`，拿到 `task_id` 就走。
- 轮询超时**不等于任务失败**——任务可能还在跑，用 `task <task_id>` 继续查（客户端会明确提示，退出码 7）。

### 5.2 幂等：不要重复提交

> **异步任务在提交时就预冻结点数。** 网络超时、进程被杀、你以为失败了——都可能只是「响应没收到」，而任务已经创建并冻结了钱。
>
> **规则：提交前先落盘记录意图，超时后先按 `task_id` 或任务列表确认，再决定是否重提。** 同一个任务重复提交会重复计费。

## 6. 回调（替代轮询）

提交时带 `callback_url` 即可不轮询：

```json
{ "text": "你好世界", "callback_url": "https://your-domain.com/a7w/hook" }
```

任务完成后平台向该地址 **POST**：

```json
{ "task_id": "tsk_xxx", "status": "completed", "result": { } }
```

接入要求：

1. 你的接口**必须返回 2xx** 才算接收成功。
2. 非 2xx 会触发重试，次数在 **用户中心 → 回调配置** 设置，范围 **1–10 次**。
3. 回调是「至少一次」语义 → **消费端必须幂等**（按 `task_id` 去重），否则重试会让你重复登记同一笔产物。
4. 回调地址要公网可达；内网地址收不到。

## 7. 结果转存到自己的对象存储

任务产物（图片/视频/音频）可以落到你自己的存储，避免链接过期：

在 **用户中心 → 结果转存** 配置 `provider / bucket / accessKey / secretKey / region / domain`，支持七牛、阿里云 OSS、腾讯云 COS；调用时在请求体里传 `storage` 对象即可。

> 转存凭证同理是密钥，不要写进代码或提交进仓库。

## 8. 一个完整的端到端例子

```bash
# 1) 先看参数与真实价
python3 scripts/client.py schema flashvsr

# 2) 写请求体（复杂参数一律走文件）
cat > body.json <<'JSON'
{ "video_url": "https://example.com/in.mp4",
  "callback_url": "https://your-domain.com/a7w/hook" }
JSON

# 3) 提交并等到完成（异步接口自动轮询）
python3 scripts/client.py call flashvsr submit --json-file body.json

# 4) 只提交不等结果的话
python3 scripts/client.py call flashvsr submit --json-file body.json --no-wait
python3 scripts/client.py task tsk_xxxxxxxx
```

## 9. 排错顺序

1. **HTTP 200 但 `code:0`** → 接口或应用不可用。最常见原因：用了 `name`（中文展示名）而不是 `code`（接口代码）。
2. **HTTP 404 且响应体为空** → 应用代码拼错（用了连字符？）。先跑 `apps --brief` 拿真名。
3. **400 `invalid_request`** → 参数名/必填项不对，用 `schema <app>` 对齐；注意 `params_schema` 的两种形态。
4. **402** → 先分清 `insufficient_points`（账号没钱）与 `key_quota_exceeded`（Key 额度满）。
5. **403 `permission_denied`** → 这个 Key 没开该应用的权限。
6. **429 `queue_limit_exceeded`** → 排队任务达上限，降并发、等队列消化。
7. **任务 `failed`** → 看 `error.message`；多为素材不合规/格式不支持，换素材重试。
