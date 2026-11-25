---
name: voooai
description: >
  VoooAI creative platform — three modes: Image Generation, Video Generation, and Director Mode
  (script → characters → storyboard → film; for short dramas, ads, MV, long-form video with
  character consistency). Relay the user's request verbatim to the backend; the platform's AI
  handles all creative decisions. Image/Video: submit task → poll → download. Director:
  conversational SSE session across 4 stages → export workflow → execute → download.
  Upload reference files (image/video/audio) as generation inputs.
  Requires VOOOAI_ACCESS_KEY AND a PAID membership (free VIP0 keys are rejected with MEMBERSHIP_REQUIRED).
  Use when: users request any image, video, or multi-shot narrative content creation or editing.
version: 2.0.2
author: VoooAI Team
license: MIT-0
user-invocable: true
permissions:
  env: [VOOOAI_ACCESS_KEY, VOOOAI_BASE_URL, VOOOAI_LOCALE]
  network: ["https://voooai.com"]
  file_read: ["user-selected reference media", ".voooai_director_session.json"]
  file_write: ["--output-dir downloads", ".voooai_director_session.json"]
metadata:
  {
    "openclaw": {
      "emoji": "🎬",
      "requires": {
        "env": ["VOOOAI_ACCESS_KEY"],
        "bins": ["python3"]
      },
      "primaryEnv": "VOOOAI_ACCESS_KEY",
      "envVars": [
        {"name": "VOOOAI_ACCESS_KEY", "required": true, "description": "Paid-member AccessKey (vooai_ prefix)."},
        {"name": "VOOOAI_BASE_URL", "required": false, "description": "Optional API base URL; HTTPS required for non-loopback hosts."},
        {"name": "VOOOAI_LOCALE", "required": false, "description": "Optional error-message language: zh (default) or en."}
      ],
      "homepage": "https://voooai.com",
      "tags": [
        "ai-director",
        "video-directing",
        "long-form-video",
        "ai-movie",
        "movie-generation",
        "ai-series",
        "episodic",
        "character-consistency",
        "script-to-storyboard",
        "shot-list",
        "storyboard",
        "short-drama",
        "webtoon",
        "manga",
        "image-generation",
        "video-generation",
        "music-generation",
        "text-to-image",
        "text-to-video",
        "image-to-image",
        "image-to-video",
        "video-to-video",
        "audio-to-video",
        "image-edit",
        "video-edit",
        "style-transfer",
        "digital-human",
        "talking-head",
        "marketing-video",
        "ai-animation",
        "batch-generation",
        "agent-to-agent",
        "multimedia",
        "workflow-automation",
        "ai-creative"
      ]
    }
  }
---

# VoooAI — AI 创作平台（图片 / 视频 / 编导）

VoooAI 是一个多媒体 AI 创作平台。Agent 的角色是**搬运工（relay）**——把用户请求原文转发给后端，
由平台 AI 完成全部创作决策（引擎选型、提示词工程、多镜头编排、角色一致性等）。

> **不要**自己改写提示词、拆解任务或手工构造工作流 JSON——只负责转发、查询、取回结果。

---

## 0. 模式选择引导（最重要·置顶）

平台当前提供**三种缺省创作模式**。接到需求时，先判断属于哪一种；**需求模糊时，先向用户复述这三选一，不要自己猜**：

| 模式 | 适用场景 | 入口脚本 |
|------|----------|----------|
| **① 图片生成** | 单张图 / 一组图、海报、概念图、封面、图生图、风格转换 | `image_generate.py` |
| **② 视频生成** | 单个视频片段、文生视频、图生视频、参考视频/音频驱动 | `video_generate.py` |
| **③ 编导模式** | 短剧 / 广告 / MV、多镜头叙事、需角色一致性、长视频、剧本→分镜→成片全流程 | `director_start.py` 等 |

**选型规则：**
- 只要一张/一批静态图 → **图片生成**
- 只要一个视频片段（无多镜头叙事） → **视频生成**
- 涉及剧情、多镜头、角色贯穿一致、剧本/分镜/成片流水线、长视频或短剧 → **编导模式**

> 🚧 **nl2workflow（自然语言一键工作流）正在维护中，暂不可用**——详见 [§12](#12-nl2workflow-维护中暂不可用)。请一律使用上述三模式。

---

## 1. 鉴权与前置要求

### VOOOAI_ACCESS_KEY
- **来源**：用户 VoooAI 账户页 https://voooai.com
- **格式**：`vooai_` 前缀 + 40 位随机字母数字（共 46 字符）
- **存储**：环境变量 `export VOOOAI_ACCESS_KEY="vooai_..."`（Windows PowerShell：`$env:VOOOAI_ACCESS_KEY="vooai_..."`），**切勿硬编码进源码**
- **可选** `VOOOAI_BASE_URL`：默认 `https://voooai.com`

### ⚠️ 需付费会员（硬门槛）
**免费用户（VIP0）无法通过 AccessKey 调用任何 API**，后端会返回 `MEMBERSHIP_REQUIRED`（HTTP 403）。
遇到该错误时，提示用户到 https://voooai.com/subscription 升级付费会员后重试。

### 允许的操作（AccessKey 授权范围）
- ✅ 能力发现（`check_capabilities.py`）
- ✅ 文件上传（`upload_file.py`）
- ✅ 图片生成 / 视频生成（`image_generate.py` / `video_generate.py`）
- ✅ 编导模式全流程（`director_*.py`）
- ✅ 任务查询/下载（`get_task.py` / `download_results.py`）
- ✅ 工作流执行（`execute_workflow.py` / `execute_single_node.py` / `get_status.py`）

### 禁止的操作（明确拒绝清单）
若用户请求以下操作，告知其直接访问 https://voooai.com：
- ❌ 用户注册 / 登录 / 鉴权管理
- ❌ 订阅 / 支付 / 计费管理
- ❌ 账户设置 / 资料修改
- ❌ 数据分析 / 使用统计
- ❌ 管理后台 / 系统配置
- ❌ 首页 / 仪表盘功能
- ❌ 绕过脚本直接调用底层 API（安全风险）

**内容安全（明确拒绝清单）**
- ❌ 制作深度伪造（deepfake）或未经同意的人脸/声音模仿
- ❌ 未经明确同意冒充真实人物
- ❌ 生成政治虚假信息或选举干预内容

> 数字人 / 口播等能力仅用于合法创作（营销主播、教育主持、虚构角色）。用户须依适用法规标注 AI 生成内容。

---

## 2. 通用脚本

所有脚本位于 `{baseDir}/scripts/`，需环境变量 `VOOOAI_ACCESS_KEY`。
> `{baseDir}` = 本 skill 的安装目录。Claude Code / OpenClaw 会在运行时告知该目录；
> 在 Cursor / 其他编辑器中，用仓库相对路径 `backend/agent-integration/openclaw/scripts/`。
> 调用统一用 `python3`（Windows 若无 `python3` 别名则用 `python`）。

### check_capabilities.py — 能力与积分发现
```bash
python3 {baseDir}/scripts/check_capabilities.py --summary   # 积分/引擎数/技能数摘要
python3 {baseDir}/scripts/check_capabilities.py             # 完整能力（含 engine_constraints、cost_guide）
```

### upload_file.py — 上传参考文件（COS 三步上传）
```bash
python3 {baseDir}/scripts/upload_file.py /path/to/file.png
```
- 支持：jpg/png/webp/gif/svg/bmp、mp4/mov/avi/mkv/webm、mp3/wav/flac/m4a/ogg
- 大小上限：图片 10MB / 视频 200MB / 音频 15MB
- 特性：MD5 去重（已存在则跳过上传）、自动分类
- 输出：`{file_url, file_id, file_type, ...}`——`file_url`/`file_id` 可作为参考素材传给生成脚本

> 🔒 **隐私提示**：上传会把本地参考文件发送到 VoooAI 服务器（离开本地环境）。上传前务必向用户说明去向并获得同意；不要上传敏感个人或第三方版权素材。

---

## 3. 模式一：图片生成

**脚本**：`image_generate.py` → `POST /api/create-task`（`task_type=image`）→ 轮询 `/api/tasks/<id>` → 下载。

```bash
# 文生图（最简）
python3 {baseDir}/scripts/image_generate.py "一只戴眼镜的橘猫，写实风格"

# 指定比例/画质并下载到本地
python3 {baseDir}/scripts/image_generate.py "赛博朋克城市夜景" --aspect-ratio 16:9 --quality high --output-dir ./out

# 图生图（先上传参考图，拿到 file_url 后传入）
python3 {baseDir}/scripts/upload_file.py ./ref.png
python3 {baseDir}/scripts/image_generate.py "把这张草图变成写实图" --reference-image-ids <file_url>

# 仅提交不等待
python3 {baseDir}/scripts/image_generate.py "产品海报" --no-wait
```

**常用参数**：`--aspect-ratio` `--resolution-tier` `--quality`(low/medium/high) `--engine-type`(留空=Auto) `--reference-image-ids` `--negative-prompt` `--output-dir` `--prefix` `--no-wait` `--dry-run`

> 📐 **尺寸语义（实测 2026-11-16）**：决定实际像素的是 `--aspect-ratio` / `--resolution-tier` / `--quality`。`--image-size`（如 `1024x1024`）仅为**向后兼容字段**，GPT Image 2 等引擎会忽略它——实测传 `--image-size 1024x1024` 仍产出 **2880×2880 PNG**。需要精确像素或指定格式（例如 SEO 配图要求 1024×1024 webp q65）时，请在下载后自行缩放/转码，不要依赖 `--image-size`。

**执行流程**：`（可选）upload_file → image_generate（提交即扣积分，先向用户确认）→ 自动轮询 → 下载`

**输出**：`{success, task_id, status, media:[{type,url}], result_urls[], points_deducted, remaining_points, downloaded_files[]}`

> ⚠️ **提交即扣积分**。调用前务必先向用户说明预估成本并获确认（见 [§8](#8-用户交互准则)）。

---

## 4. 模式二：视频生成

**脚本**：`video_generate.py` → `POST /api/create-task`（`task_type=video`）→ 轮询 `/api/tasks/<id>` → 下载。

```bash
# 文生视频
python3 {baseDir}/scripts/video_generate.py "一只机器人在跳舞，霓虹灯背景"

# 图生视频（先上传首帧图）
python3 {baseDir}/scripts/upload_file.py ./first.png
python3 {baseDir}/scripts/video_generate.py "让这张图动起来" --reference-image-ids <file_url>

# 指定时长/比例并下载（视频较慢，默认轮询超时 600s）
python3 {baseDir}/scripts/video_generate.py "咖啡产品广告" --video-duration 8 --video-aspect-ratio 16:9 --output-dir ./out

# 仅提交不等待，稍后轮询
python3 {baseDir}/scripts/video_generate.py "海浪拍打礁石" --no-wait
python3 {baseDir}/scripts/get_task.py <task_id> --poll --timeout 600
```

**常用参数**：`--video-duration` `--video-size`(480p/720p/1080p) `--video-aspect-ratio` `--video-engine-type`(留空=Auto) `--generation-type`(TEXT/FIRST&LAST/REFERENCE) `--reference-image-ids` `--reference-video-ids` `--reference-audio-ids` `--output-dir` `--no-wait` `--dry-run`

**输出**：同图片生成，`media` 中 `type=video`。

> ⚠️ 视频成本通常高于图片，**提交即扣积分**，调用前务必向用户确认。

---

## 5. 模式三：编导模式（长视频 / 短剧 / 角色一致性）

编导模式是一个**有状态、多轮对话、SSE 流式**的创作环境，分 4 个阶段渐进产出：
**Stage 1 剧本 → Stage 2 角色与元素 → Stage 3 分镜 → Stage 4 工作流/成片**。
后端 AI 在对话中自动执行编排动作（加角色、加分镜、生成引用图等）并逐阶段推进。

### 生命周期与脚本

```bash
# ① 启动会话（SSE）：传入创意描述，返回 session_id，AI 驱动 Stage 1
python3 {baseDir}/scripts/director_start.py "一部关于侦探的短剧，黑色电影风格"
#   默认 --no-auto-generate（逐阶段确认，防自动烧积分）；会话状态存入 .voooai_director_session.json

# ② 对话推进（SSE）：持续指导 AI，自动产出角色/分镜并前进阶段
python3 {baseDir}/scripts/director_chat.py "把主角设定为一名退休警探，增加一个反派"
python3 {baseDir}/scripts/director_chat.py "确认当前阶段，进入下一步"

# ③ 查看状态与各阶段产出
python3 {baseDir}/scripts/director_status.py            # current_stage / stage_statuses / 摘要
python3 {baseDir}/scripts/director_status.py --full     # 完整阶段数据（剧本/角色/分镜）

# ④（可选）阶段控制
python3 {baseDir}/scripts/director_navigate.py --stage 3              # 确认 Stage 3 完成并推进（确定性，不耗 LLM 积分）
python3 {baseDir}/scripts/director_confirm.py --proposal-id <mp_xxx>  # 确认 AI 提出的修改提案（proposal_id 来自 chat 回复）

# ⑤ 出片（两条路，二选一）
# 路 A（推荐·复用执行链）：导出工作流 → node-builder 执行 → 下载
python3 {baseDir}/scripts/director_export.py --execute --output-dir ./out
# 路 B（逐分镜直接出视频）：
python3 {baseDir}/scripts/director_execute_video.py --storyboard-id <sb_id>
```

- 所有 `director_*.py` 缺省从 `.voooai_director_session.json` 读取 `session_id`；多会话时用 `--session-id` 显式指定。
- `director_start.py` / `director_chat.py` 消费 SSE 流（`token`/`action`/`summary`/`required_config`/`done`），脚本会聚合为一次性 JSON 输出。

### 首次创作必答题：`required_config`（全局配置确认）

会话**首次进入剧本创作**且全局必填配置尚未确认时，后端守门流程会**拦截本轮 task 执行**，改为下发 `required_config` 事件。此时：

- `reply` 为空、`current_stage` 不推进 —— **属预期，不是失败**，不要重试或改写消息重发；
- 但本轮守门 LLM **已计费**（实测扣 1 分），所以必须一次把配置问全，避免反复空转；
- 脚本输出会带 `needs_config: true`、`required_config.questions[]`、`required_config.original_message` 与 `hint`。

`questions[]` 字段语义（**文案与回传值必须分清**）：

| 字段 | 含义 |
|------|------|
| `question_id` | 回传 `config` 对象的**键**（如 `aspect_ratio`） |
| `question` | 后端按会话语种（`director_start.py --locale`）**已本地化的问题文案**，直接展示给用户 |
| `quick_options[].label` | 已本地化的**选项文案**，直接展示 |
| `quick_options[].value` | **真正要回传的值**，不要用 label 当值 |

**处理流程（四步，不可跳）：**

1. 把 `questions` 的问题与选项**原样呈现给用户拍板**。画面比例 / 分辨率 / 时长 / 对白语言属创作决策，**Agent 不得代选**（成本差异可达数十倍）。
2. 用用户选定值组装回传指令，`original_message` **必须取** `required_config.original_message`（后端据此重走守门流程，丢了它就丢了原始创作意图）：
   ```
   [REQUIRED_CONFIG]{"config":{"<question_id>":"<value>", ...},"original_message":"<原消息>"}
   ```
3. 用 `director_chat.py` 把上面整串**作为 content 原样传入**（前缀 `[REQUIRED_CONFIG]` 不可省、不可改写、不可加引号包裹）：
   ```bash
   python3 {baseDir}/scripts/director_chat.py '[REQUIRED_CONFIG]{"config":{"aspect_ratio":"16:9","resolution":"480p","duration_seconds":30,"dialogue_language":"zh","draft_mode":"true"},"original_message":"请给出这个短片的剧本大纲"}' --timeout 600
   ```
4. 回传成功后后端会校验并落盘配置、重走守门并**真正生成剧本**：输出含 `actions[].type=stage_update`、`current_stage=1`、`stage_statuses={"1":"pending_confirmation"}`，随后按正常逐阶段确认流程推进。

> ⚠️ **字段以实际下发为准**：上例键名只是常见项，不同版本/阶段必填项可能不同，一律按 `questions[].question_id` 组装，不要硬编码清单。
> `draft_mode=true` 时后端会**权威锁定** `resolution=480p`（草稿档省积分），此时不要再传高分辨率。
>
> 🪟 **Windows/PowerShell 陷阱**：content 内含大量 JSON 双引号，直接内联传参易被 shell 切碎或挂在续行提示符上。建议把指令写入临时文件后读取，或用 `subprocess` **列表传参**（由 Python 负责转义）。
>
> 📙 实测记录（2026-11-16 本地环境）：未处理 `required_config` 时表现为「chat 已扣积分却只回空 reply」；按上述流程回传后 Stage 1 剧本生成成功（扣 5 分，产出剧本/角色/关系与 `creative_directives` 落盘）。

### 出片路径说明
- **路 A（export-workflow → execute）**：`director_export.py` 调 `GET /api/director/v2/<sid>/export-workflow` 得到 `{nodes, edges}`，脚本自动把 ReactFlow `edges` 归一化为 node-builder `connections`，再交给 `execute_workflow.py` 执行、`get_status.py` 轮询、`download_results.py` 下载。加 `--execute` 可一条龙。
  **前置**：必须已完成 **Stage 3 分镜设计**，否则后端返回 HTTP 400 `Stage 3 storyboard data is empty`（属业务拦截，不是脚本故障）；此时先推进阶段，不要反复重试导出。
- **路 B（execute_storyboard_video）**：`director_execute_video.py` 调 `POST /api/director/v2/<sid>/execute_storyboard_video` 逐分镜生成视频，结果经任务系统回写，用 `get_task.py` 查询下载。

> ⚠️ 编导模式涉及多轮 LLM 与多次生成，积分消耗较高。`director_start.py` 默认 `auto_generate=false`，
> 需逐阶段由用户确认后再推进/出片，符合「Agent 绝不代替用户做耗积分决策」原则。

---

## 6. 任务查询与结果下载

### get_task.py — 图片/视频任务查询·下载·取消
```bash
python3 {baseDir}/scripts/get_task.py <task_id> --poll                    # 轮询直到完成
python3 {baseDir}/scripts/get_task.py <task_id> --poll --output-dir ./out # 轮询并下载
python3 {baseDir}/scripts/get_task.py <task_id> --cancel                  # 取消任务
```
任务结果按媒体类型分字段：`task.image_url` / `video_url` / `audio_url`。

### download_results.py — node-builder 执行结果下载（编导出片路 A / 工作流执行）
```bash
python3 {baseDir}/scripts/download_results.py <execution_id> --output-dir ./out
python3 {baseDir}/scripts/download_results.py --urls https://a.com/1.png  # 直接下载指定 URL
```

### get_status.py / execute_workflow.py / execute_single_node.py — 工作流执行（编导出片路 A 复用）
```bash
python3 {baseDir}/scripts/execute_workflow.py workflow.json               # 执行工作流
python3 {baseDir}/scripts/get_status.py <execution_id> --poll             # 轮询执行状态
python3 {baseDir}/scripts/execute_single_node.py workflow.json --node-id <id>  # 重试单节点
```

---

## 7. 典型端到端流程

### 场景 1：一张海报（图片生成）
```bash
python3 {baseDir}/scripts/check_capabilities.py --summary      # 看积分
python3 {baseDir}/scripts/image_generate.py "极简风格咖啡品牌海报，暖色调" --aspect-ratio 3:4 --output-dir ./out
```

### 场景 2：图生视频（上传 + 视频生成）
```bash
python3 {baseDir}/scripts/upload_file.py ./product.png         # → file_url
python3 {baseDir}/scripts/video_generate.py "让产品缓慢旋转，柔和打光" --reference-image-ids <file_url> --output-dir ./out
```

### 场景 3：一部短剧（编导模式，路 A 出片）
```bash
python3 {baseDir}/scripts/director_start.py "30 秒悬疑短剧：深夜便利店的一场对峙"
python3 {baseDir}/scripts/director_chat.py "确认剧本，进入角色设计"
python3 {baseDir}/scripts/director_chat.py "确认角色，生成分镜"
python3 {baseDir}/scripts/director_status.py                    # 核对分镜
python3 {baseDir}/scripts/director_export.py --execute --output-dir ./out/drama
```

---

## 8. 用户交互准则

### 积分确认（关键）
图片/视频**提交即扣积分**，编导模式多轮消耗更高。因此：
1. 生成前**必须**向用户说明预估成本（可用 `check_capabilities.py` 查余额）
2. **必须**等待用户确认后再提交
3. 存在积分不足风险时**绝不**自动提交

```
Agent：「这张图预计消耗约 N 积分，你当前余额 M。是否继续？(yes/no)」
User ：「yes」
Agent：[再提交]
```

### 模式选择
需求模糊时，先向用户复述[三模式](#0-模式选择引导最重要置顶)让其选择，不要自行猜测模式或填充创作细节。

### 多方案
后端返回多个方案/选项时，全部呈现给用户并附清晰说明，由用户选择，不要自动选。

### 失败后决策
执行失败时清晰呈现原因，提供选项（重试 / 调整参数 / 换引擎 / 放弃），由用户决定。

### 核心原则
**Agent 绝不代替用户做任何消耗积分的决策。**

---

## 9. 失败处理与重试

### 诊断
1. 图片/视频：`get_task.py <task_id>` 看 `status` 与 `error_message`
2. 工作流：`get_status.py <execution_id>` 看 `failed_nodes` 与 `node_statuses`
3. 编导：`director_status.py` 看各阶段状态

### 重试策略
| 策略 | 适用 | 命令 |
|------|------|------|
| 任务重提交 | 图片/视频任务失败 | 重新运行 `image_generate.py` / `video_generate.py` |
| 单节点重试 | 工作流某节点失败 | `execute_single_node.py --node-id <failed>` |
| 参数调整 | 引擎拒绝参数 | `execute_workflow.py --set-param node_id.key=value` |
| 编导局部重生成 | 某分镜/角色不满意 | `director_chat.py "重做第 N 个分镜"` |

### 常见错误
| 错误码 | 原因 | 处理 |
|--------|------|------|
| `MEMBERSHIP_REQUIRED` | 免费 VIP0 用 AccessKey | 到 voooai.com/subscription 升级付费会员 |
| `INSUFFICIENT_POINTS` | 积分不足 | 到 voooai.com/subscription 充值 |
| `DUPLICATE_REQUEST` / 429 | 请求过频/并发限制 | 稍后重试 |
| `ENGINE_TIMEOUT` | 引擎超时 | 重试或换引擎 |
| `CONTENT_BLOCKED` / `CONTENT_MODERATION_FAILED` | 内容安全过滤 | 修改描述以符合规范 |
| `ENGINE_UNAVAILABLE` | 引擎临时不可用 | 稍后重试或用替代引擎 |

### 已知限制
- 状态同步可能滞后——轮询需有耐心（图片默认超时 300s，视频 600s）
- 编导模式复杂短剧可能耗时数分钟
- 超时后提示用户到 https://voooai.com 查看结果

---

## 10. 输出格式

**check_capabilities.py**：`{success, trust_level, points_balance, membership_level, points_warning, engines, skills, engine_constraints, constraints}`

**image_generate.py / video_generate.py**：`{success, task_id, status, media:[{type,url}], result_urls[], points_deducted, remaining_points, downloaded_files[]}`

**get_task.py**：`{success, task_id, status, media[], result_urls[]}`

**director_start.py**：`{success, session_id, tab_id, current_stage, reply}`

**director_chat.py**：`{success, session_id, reply, actions[], current_stage, stage_statuses}`

**director_status.py**：`{success, session_id, current_stage, stage_statuses, stage_data}`

**director_export.py**：`{success, session_id, workflow:{nodes,connections}, execution_id?, ...}`

**execute_workflow.py**：`{success, execution_id, status, message}`

**get_status.py**：`{success, execution_id, status, progress, result_urls[]}`（status: pending|running|completed|failed）

**download_results.py**：`{success, output_dir, downloaded_files[], total_count}`

**upload_file.py**：`{file_url, file_id, file_type, file_name, file_size_bytes, status}`

---

## 11. 核心原则

### Agent 是搬运工（relay）
- **原文转发**用户描述给平台，**绝不**改写、扩写、润色或翻译用户提示词
- **绝不**自己拆解任务（"做 5 集"作为一个请求整体发出）
- **绝不**手工构造工作流 JSON——编导模式用 `director_*`，图片/视频用 `image_generate`/`video_generate`

### 信任后端
平台 AI（编导 Agent / 引擎评分服务）负责：任务拆解与规划、引擎/模型选择、提示词工程、多镜头与角色一致性编排。

### 积分意识
- 生成前**总是**说明预估成本、**总是**获取用户确认、**绝不**自动提交耗积分操作

### 隐私意识
- 上传参考素材前**总是**告知用户文件将离开本地、上传至 VoooAI 服务器并获确认；**绝不**擅自上传敏感或第三方版权文件

### 范围意识
- **仅**操作创作相关功能；**绝不**触碰首页/计费/管理后台/账户设置；越界请求引导至 voooai.com

---

## 12. nl2workflow（🚧 维护中·暂不可用）

自然语言一键工作流（`/api/agent/nl2workflow/*`）链路已较长时间未维护，存在参考媒体被丢弃、
方案契约漂移等已知问题，**当前不对外开放**。相关脚本已归档至源码仓的 _deprecated 目录，不随本包分发。

**请一律使用三模式**（图片生成 / 视频生成 / 编导模式）。待后端 nl2workflow 重新迭代修复后再恢复启用。

---

## 13. 跨编辑器使用说明（Cursor / Claude Code / 任意 AI editor）

本 skill 采用「一份脚本 + 多份宿主适配」结构，便于不同 AI 编辑器直接读取使用：

| 宿主 | 读取入口 | 说明 |
|------|----------|------|
| OpenClaw / ClawHub | 本技能说明文件（frontmatter metadata.openclaw） | 原生 Agent Skills 包；本包仅含本文件与 scripts/ |
| Claude Code | 本技能说明文件（frontmatter name + description） | 将本目录复制到 .claude/skills/voooai/ 或插件目录 |
| 其他编辑器 / MCP 宿主 | 源码仓 https://github.com/hkljjkl/voooai_agent_skill | 通用 AGENTS.md、Cursor Rules、MCP 封装见源码仓，不随本包分发 |

**统一约定**：所有宿主都调用本包 scripts/ 下的同一套 Python 脚本，
仅需设置 VOOOAI_ACCESS_KEY（付费会员）。脚本输出统一为 JSON，便于各编辑器解析。

---

## 14. 轮询策略

- **图片任务**：间隔 5s，默认超时 300s
- **视频任务**：间隔 5s，默认超时 600s
- **工作流执行**：间隔 10s，默认超时 300s（`get_status.py --poll`）
- **完成**：`status: completed` → 取 `media`/`result_urls`/`outputs`
- **失败**：`status: failed` → 看 `error_message`
- **超时后**：提示用户到 https://voooai.com 查看

---

**Website**: https://voooai.com | **Support**: support@voooai.com
