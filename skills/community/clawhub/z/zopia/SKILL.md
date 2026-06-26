---
name: zopia-skill
description: Zopia AI 视频创作技能 - 通过 Zopia 平台的 AI Agent 进行视频/图片创作。覆盖场景包括：AI 视频生成（文生视频、图生视频）、AI 图片生成（角色设定图、分镜关键帧）、剧本创作（对话/旁白/场景描述）、角色设计、分镜设计、多集连续剧制作。当用户提到 zopia、视频创作、短剧制作、分镜、角色设计、AI 视频生成时应触发。关键判断：只要用户的请求涉及通过 AI 进行系统化的视频创作流程（剧本→角色→分镜→视频），都必须触发此技能。
user-invocable: true
metadata:
  {
    "openclaw":
      {
        "emoji": "🎬",
        "requires":
          {
            "bins": ["python3"],
            "env": ["ZOPIA_ACCESS_KEY"]
          },
        "primaryEnv": "ZOPIA_ACCESS_KEY"
      }
  }
---

# Zopia AI 视频创作

Zopia 是一个项目制的 AI 视频创作平台。每个项目包含完整的创作流水线：**剧本 → 角色 → 分镜 → 视频**，由后端 AI Agent 自动驱动。你通过脚本管理项目、传达用户意图、追踪进度、获取成果。

## 环境配置

```bash
export ZOPIA_ACCESS_KEY="zopia-xxxxxxxxxxxx"   # 必需，30天有效
export ZOPIA_BASE_URL="https://zopia.ai"  # 可选
```

仅使用 Python 标准库，无需额外安装。

## 核心概念

| 概念 | 说明 |
|------|------|
| **Project (Base)** | 创作项目，包含设置、剧集、所有资产。创建时自动生成首集 |
| **Episode** | 剧集，同一项目下可创建多集，每集有独立的剧本/角色/分镜 |
| **Session** | 一次 Agent 对话。异步执行，通过轮询获取进展 |
| **Workspace** | 项目的实时工作区快照，包含角色(entities)、分镜(storyboard)、各媒体的生成状态 |

## 脚本速查

| 脚本 | 用途 | 关键参数 |
|------|------|---------|
| `create_project.py` | 创建项目 | `[名称]` |
| `save_settings.py` | 项目设置 | `--base-id` `--style` `--aspect-ratio` `--video-model` `--storyboard-image-model` `--entity-image-model` ... |
| `send_message.py` | 发送创作指令（异步） | `--base-id` `--episode-id` `消息` |
| `query_session.py` | 查询进展 | `SESSION_ID` `--poll` `--after-seq N` |
| `download_results.py` | 下载媒体资源 | `SESSION_ID` `--output-dir` `--type image\|video` |
| `get_balance.py` | 余额查询 | — |
| `list_projects.py` | 列出项目 | `--page` `--page-size` |
| `manage_episodes.py` | 剧集管理 | `list\|create\|delete` |
| `render_episode.py` | 合成最终视频 | `trigger\|status` `--base-id` `--episode-id` `--poll` |

## 项目设置参考

创建项目后，必须配置基础设置（locale / aspect_ratio / style）才能开始创作。

```bash
python3 {baseDir}/scripts/save_settings.py --base-id BASE_ID \
  --locale zh-CN --aspect-ratio 16:9 --style realistic_3d_cg
```

### 风格

| ID | 说明 |
|----|------|
| `anime_japanese_korean` | 日韩动漫 |
| `realistic_3d_cg` | 3D CG 写实 🔥 |
| `pixar_3d_cartoon` | Pixar 3D 卡通 |
| `photorealistic_real_human` | 真人写实 |
| `3D_CG_Animation` | 3D CG 动画 🔥 |
| `anime_chibi` | Q版可爱 |
| `anime_shinkai` | 新海诚 |
| `anime_ghibli` | 吉卜力 |
| `stylized_pixel` | 像素艺术 |

别名支持：`realistic` → `realistic_3d_cg`，`ghibli` → `anime_ghibli`，`shinkai` → `anime_shinkai`，`pixel` → `stylized_pixel`

### 视频模型 × 生成方式

不同模型支持不同的生成方式（generation_method），不匹配会报错。

| 模型 ID | 名称 | 支持的方式 | 默认 |
|---------|------|-----------|------|
| `generate_video_by_seedance_20` | Seedance 2.0 Pro ⭐ | n_grid, video_ref, multi_ref, multi_ref_v2 | video_ref |
| `generate_video_by_seedance_20_fast` | Seedance 2.0 Fast | n_grid, video_ref, multi_ref, multi_ref_v2 | video_ref |
| `generate_video_by_kling_o3` | Kling O3 | start_frame, n_grid, multi_ref, multi_ref_v2 | n_grid |
| `generate_video_by_kling_v3_0` | Kling V3.0 | start_frame, n_grid | n_grid |
| `generate_video_by_pixverse_c1` | PixVerse C1 | start_frame, multi_ref | start_frame |
| `generate_video_by_hailuo_02` | Hailuo 2.3 | start_frame | start_frame |
| `generate_video_by_wan26_i2v` | Wan 2.6 | start_frame | start_frame |
| `generate_video_by_wan26_i2v_flash` | Wan 2.6 Flash | start_frame | start_frame |
| `generate_video_by_viduq2_pro` | Vidu Q2 Pro | start_frame | start_frame |
| `generate_video_by_viduq3_pro` | Vidu Q3 Pro | start_frame | start_frame |
| `generate_video_by_viduq3` | Vidu Q3 | n_grid, multi_ref, multi_ref_v2 | n_grid |
| `generate_video_by_seedance_15` | Seedance 1.5 Pro | start_frame | start_frame |

### 图片模型

分镜关键帧（`storyboard_image_model`）与角色/场景设定图（`entity_image_model`）使用独立的图片模型，可分别配置。

| 模型 ID | 名称 | 默认场景 |
|---------|------|---------|
| `generate_image_by_nano_banana_2` | Nano Banana 2 | storyboard 默认 |
| `generate_image_by_doubao_seedream_4` | Doubao Seedream 4 | entity 默认 |
| `generate_image_by_nano_banana` | Nano Banana | — |
| `generate_image_by_gpt_image_2` ⭐ | GPT Image 2 | — |

不传则后端使用默认值。传非法 ID 后端会返回 `invalid_storyboard_image_model` / `invalid_entity_image_model` 400 错误，并在响应的 `allowed_values` 字段给出当前可用列表。

### 其他设置

| 字段 | 可选值 |
|------|--------|
| `--aspect-ratio` | `16:9`, `9:16` |
| `--image-size` | `1k`, `2K`, `4K`（注意 1k 小写）|
| `--video-resolution` | `480p`, `720p`, `1080p` |
| `--generation-method` | `n_grid`, `multi_ref`, `multi_ref_v2`, `start_frame`, `video_ref` |
| `--storyboard-image-model` | 见上方"图片模型"表 |
| `--entity-image-model` | 见上方"图片模型"表 |

---

## 典型场景

理解这些场景，才能正确组合脚本完成用户需求。

### 场景 1：用户给出创作需求，从零开始（最常见）

```
1. get_balance.py                          → 确认余额 ≥ 10
2. create_project.py "赛博朋克短剧"        → 拿到 baseId, episodeId
3. save_settings.py --base-id B \
     --locale zh-CN --aspect-ratio 16:9 \
     --style anime_japanese_korean         → 配置项目
4. send_message.py --base-id B \
     --episode-id E "用户的原始描述"        → 拿到 session_id
5. query_session.py S --poll               → 自动轮询直到完成
6. download_results.py S \
     --output-dir ./赛博朋克短剧 \
     --prefix storyboard                   → 自动下载到本地
```

生成完成后**自动执行下载**，不需要用户额外请求。下载目录和前缀根据任务语义自动命名（如分镜用 `storyboard`，角色设定用 `character`，最终视频用 `video` 等）。

**展示时机：** 生成过程中只告知进度（"角色图生成中..."、"分镜关键帧 5/8 完成"），**不要提前给出项目链接**。全部完成后，同时给出：**本地文件列表** + **项目链接**（`{ZOPIA_BASE_URL}/base/{baseId}?session_id={sessionId}`，用户可在浏览器中查看和编辑完整项目）。优先使用脚本输出中的 `projectUrl` 字段。

### 场景 2：在已有会话中追加新需求（如"再改一下角色造型"）

```
1. send_message.py --base-id B --episode-id E \
     --session-id S "用户的新指令"          → 复用已有会话
2. 轮询 → 下载 → 展示
```

使用同一个 `session_id` 可保持上下文连续。

### 场景 3：在已有项目中继续创作

```
1. list_projects.py                         → 让用户选择项目
2. manage_episodes.py list --base-id B      → 查看剧集列表
3. send_message.py --base-id B \
     --episode-id E "新的创作指令"           → 新建会话
4. 轮询 → 下载 → 展示
```

### 场景 4：多集连续剧制作

一个项目(Project)可以包含多个剧集(Episode)。每集有独立的剧本、角色表、分镜表，但共享项目级设置（风格、画幅、模型）。

**创作流程：**

```
1. create_project.py "我的连续剧"              → 拿到 baseId, episodeId (自动创建第一集)
2. save_settings.py --base-id B ...            → 配置项目（所有剧集共享）

── 第一集 ──
3. send_message.py --base-id B \
     --episode-id EP1 "第一集：主角进入废墟..."  → 创作第一集
4. 轮询 → 下载

── 第二集 ──
5. manage_episodes.py create --base-id B       → 拿到新 episodeId (EP2)
6. send_message.py --base-id B \
     --episode-id EP2 "第二集：发现地下实验室..." → 创作第二集
7. 轮询 → 下载

── 更多剧集：重复步骤 5-7 ──
```

**多集注意事项：**
- 每集有独立的角色和分镜，不会互相干扰
- 如果后续剧集需要沿用前集角色形象，在消息中说明即可（如"延续第一集的角色设定"），后端 Agent 会处理
- 创建新剧集前，建议先确认当前剧集已完成（`status: "completed"`）
- 可以随时用 `manage_episodes.py list --base-id B` 查看所有剧集状态
- 删除剧集是不可逆操作，会清除该集所有内容

### 场景 5：将分镜视频合成为最终 MP4

所有分镜视频生成完毕后，可一键触发云端渲染，将所有片段按时间轴顺序合成为完整 MP4 文件。

```
1. render_episode.py trigger \
     --base-id B --episode-id E            → 拿到 render_id，渲染开始（异步）
2. render_episode.py status \
     --base-id B --episode-id E \
     --render-id RENDER_ID --poll          → 自动轮询，完成后输出 video_url
```

**触发时机：** 用户明确要求「导出视频」「合成 MP4」「生成完整视频」时才触发。分镜视频生成阶段不要触发。

**渲染前提：** storyboard 中至少有一个分镜有 video_urls（即已完成视频生成），否则渲染内容为空。

**完成标志：** `status: "completed"` 且返回 `video_url`（S3 直链，可直接下载或分享）。

**轮询说明：** 渲染由 Remotion Lambda 执行，通常需要 1–5 分钟，`--poll` 参数每 8 秒检查一次进度（`progress` 字段 0→1），超时上限 10 分钟。

---

## 读懂 workspace 进度

`query_session.py` 返回的 `workspace` 是项目的实时快照，用来判断创作走到哪一步了：

```json
{
  "status": "running",
  "workspace": {
    "entities": [{"name": "角色A", "images_status": "done", "image_urls": [...]}],
    "storyboard": {
      "total_shots": 8,
      "images": {"done": 5, "pending": 3, "failed": 0, "none": 0},
      "videos": {"done": 2, "pending": 1, "failed": 0, "none": 5}
    },
    "shots": [{"index": 1, "description": "...", "image_urls": [...], "video_urls": [...]}]
  }
}
```

**怎么读：**

- `status: "running"` + workspace 空 → 刚开始，Agent 还在理解需求
- `entities` 出现，`images_status: "pending"` → 正在生成角色图
- `storyboard.images.pending > 0` → 正在生成分镜关键帧
- `storyboard.videos.pending > 0` → 正在生成视频片段
- `status: "completed"` → 全部完成，检查有无 failed 项

**轮询策略：**
- **间隔**：每 8 秒查询一次
- **增量拉取**：首次 `--after-seq 0`，后续传上次拿到的最大 seq 值
- **完成判断**：`status` 变为 `completed`（全部完成）或 `idle`
- **超时**：连续 3 分钟无新进展，告知用户「生成时间较长」并给出项目链接供自行查看，停止轮询
- **错误重试**：单次查询失败可重试 1 次；连续 3 次失败则停止并告知用户
- **自动轮询**：使用 `--poll` 参数可自动执行上述策略，无需手动循环

---

## 你的角色

Zopia 后端有完整的 AI 创作 Agent（对模型能力、prompt 工程、创作流程远比用户侧专业），你负责的是**项目管理和需求传达**。

**你要做的三件事：**
1. **配置** — 根据用户意图创建项目，选择合适的风格、模型、画幅
2. **传话** — 把用户的原始需求原封不动发给后端 Agent
3. **取件** — 追踪进度，在关键节点通知用户，完成后自动下载结果并展示

**不要做的事：**
- 不替用户扩写、润色、翻译创作描述（用户说"帮我推演分镜"，就直接传这句话，不要自己先写个分镜表再逐条发）
- 不自行拆分任务（用户说"生成8个分镜图"，发一条消息给后端，后端自己拆解）
- 不在消息中添加自己编的描述词（如"超写实风格，电影级光影，8K分辨率"）

**正确：**
```
用户说：「帮我做一个赛博朋克风格的短剧，讲一个机器人在废墟中寻找最后一朵花」

→ create_project.py "赛博朋克短剧"
→ save_settings.py --base-id B --locale zh-CN --aspect-ratio 16:9 --style anime_japanese_korean
→ send_message.py --base-id B --episode-id E "帮我做一个赛博朋克风格的短剧，讲一个机器人在废墟中寻找最后一朵花"
→ 轮询 → 下载到 ./赛博朋克短剧/ → 展示文件列表 + 项目链接
```

**错误：**
```
❌ 先自己写了个详细的 5 场剧本和分镜描述
❌ 把自己编的内容逐条发给后端
❌ 在用户描述后面追加 "cinematic lighting, 8K, ultra detailed"
```

---

## 错误码速查

| 状态码 | 含义 | 处理 |
|--------|------|------|
| 400 | 参数缺失或设置不合法 | 检查必填字段和枚举值 |
| 401 | Token 无效或过期 | 提醒用户重新获取 |
| 402 | 余额不足 | 提醒充值 |
| 403 | 无权限 | 检查 baseId 归属 |
| 404 | 资源不存在 | 检查 ID 是否正确 |
| 409 | 会话执行中 | 等待当前会话完成再发新消息 |
