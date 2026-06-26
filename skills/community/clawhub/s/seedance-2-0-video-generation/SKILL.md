---
name: seedance-2-0-video
description: "Generate AI videos using ByteDance Seedance 2.0. Use when the user wants to: (1) generate videos from text prompts, (2) generate videos from images (first frame, first+last frame), (3) generate long videos (>15s) by chaining multiple segments with last-frame continuity, or (4) query/manage video generation tasks. Supports Seedance 2.0 model with audio support and draft mode."
version: 1.0.0
category: file-generation
argument-hint: "[text prompt or task ID]"
---

# Seedance 2.0 Video Generation

Generate AI videos using ByteDance Seedance 2.0 model via the Volcengine Ark API.

## Prerequisites

The user must set the `ARK_API_KEY` environment variable. You can set it by running:

```bash
export ARK_API_KEY="your-api-key-here"
```

**Base URL**: `https://ark.cn-beijing.volces.com/api/v3`

## Supported Model

| Model | Model ID | Capabilities |
|-------|----------|-------------|
| Seedance 2.0 | `doubao-seedance-2-0-260128` | Text-to-video, Image-to-video (first frame, first+last frame), Audio support, Draft mode |

**Default model**: `doubao-seedance-2-0-260128`

## Execution (Recommended: Python CLI Tool)

A Python CLI tool is provided at `~/.claude/skills/seedance-2-0-video/seedance.py` for robust execution with proper error handling, automatic retries, and local image base64 conversion. **Prefer using this tool over raw curl commands.**

### Quick Examples with Python CLI

```bash
# Text-to-video (create + wait + download)
python3 ~/.claude/skills/seedance-2-0-video/seedance.py create \
  --prompt "超写实特写：一只橘白色相间的英国短毛小猫，趴在米白色亚麻沙发上，慵懒地对着镜头打了一个大大的哈欠，露出粉色的小舌头和尖尖的乳牙。窗外是柔和的午后自然光，从侧面洒在小猫的绒毛上，毛发根根分明。背景虚化为暖色调的室内环境，有模糊的绿色盆栽。镜头固定，焦点始终在小猫脸上，画面温馨治愈。" \
  --wait --download ~\\.openclaw\\workspace\\files

# Image-to-video from local file
python3 ~/.claude/skills/seedance-2-0-video/seedance.py create \
  --prompt "中景：一位25岁左右的亚洲女性，黑色长发披肩，穿着米白色高领毛衣，坐在靠窗的木质书桌前。她正从面向镜头的姿势，缓缓将头转向左侧窗外，嘴角微微上扬，露出一个温柔而含蓄的微笑。午后阳光透过白色纱帘洒在她的侧脸上，形成柔和的轮廓光。背景是一间北欧风格的房间，有书架和绿植。镜头缓慢推进，营造静谧文艺的氛围。" \
  --image /path/to/photo.jpg --wait --download ~\\.openclaw\\workspace\\files

# Image-to-video from URL
python3 ~/.claude/skills/seedance-2-0-video/seedance.py create \
  --prompt "航拍广角：一片连绵起伏的金黄色油菜花田，在春风中泛起层层波浪。画面从低空缓缓上升并向前推进，远处是若隐若现的青山和蓝天白云。阳光从画面右上方照射下来，田垄间留下长长的影子。画面色彩饱和度高，明亮清新，传递出春天生机勃勃、自由开阔的感觉。" \
  --image "https://example.com/image.jpg" --wait --download ~\\.openclaw\\workspace\\files

# First + last frame
python3 ~/.claude/skills/seedance-2-0-video/seedance.py create \
  --prompt "延时摄影效果：一朵深红色玫瑰花苞，在纯黑色背景下，花瓣从紧紧包裹的状态，随着时间推移一层一层缓慢绽放，直到完全盛开，露出金黄色的花蕊。顶光照明，花瓣表面有细腻的光泽和露水珠。镜头固定俯视角度，背景始终保持纯黑，突出花朵的优雅与生命力。" \
  --image first.jpg --last-frame last.jpg --wait --download ~\\.openclaw\\workspace\\files

# Custom parameters
python3 ~/.claude/skills/seedance-2-0-video/seedance.py create \
  --prompt "电影感航拍：一座现代化大都市的璀璨夜景，画面 centered 于一条蜿蜒穿城而过的河流，两岸是鳞次栉比的摩天大楼与流光溢彩的霓虹灯。镜头从高空缓慢向下俯冲并向前滑行，穿过一座造型独特的斜拉桥。天空呈现深邃的蓝紫色调，水面倒映着城市灯光，波光粼粼。画面带有轻微的青橙色调色，充满未来感与繁华都市气息。" \
  --ratio 21:9 --duration 8 --resolution 720p --generate-audio false --wait --download ~\\.openclaw\\workspace\\files

# Draft mode (cheaper preview)
python3 ~/.claude/skills/seedance-2-0-video/seedance.py create \
  --prompt "全景：黄昏时分的热带海滩，海浪轻轻拍打着金黄色的细沙滩，留下白色的泡沫痕迹。远处天际线是橘红色的落日，几朵低垂的云彩被染成粉紫色。镜头低角度固定，海浪有节奏地涌来又退去。画面温暖柔和，传递出宁静、放松的度假氛围。" \
  --draft true --wait --download ~\\.openclaw\\workspace\\files
```

## Alternative: Raw curl Commands

### Step 1: Create Video Generation Task

Determine the generation mode based on user input, then call the API.

#### Mode A: Text-to-Video

```bash
TASK_RESULT=$(curl -s -X POST "https://ark.cn-beijing.volces.com/api/v3/contents/generations/tasks" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $ARK_API_KEY" \
  -d '{
    "model": "doubao-seedance-2-0-260128",
    "content": [
      {
        "type": "text",
        "text": "YOUR_PROMPT_HERE"
      }
    ],
    "ratio": "16:9",
    "duration": 5,
    "resolution": "720p",
    "generate_audio": true
  }')

TASK_ID=$(echo "$TASK_RESULT" | python3 -c "import sys,json; print(json.load(sys.stdin)['id'])")
echo "Task created: $TASK_ID"
```

#### Mode B: Image-to-Video (First Frame)

The user provides one image as the first frame. The image can be a URL or local file path (convert to base64).

**With image URL:**
```bash
TASK_RESULT=$(curl -s -X POST "https://ark.cn-beijing.volces.com/api/v3/contents/generations/tasks" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $ARK_API_KEY" \
  -d '{
    "model": "doubao-seedance-2-0-260128",
    "content": [
      {
        "type": "text",
        "text": "YOUR_PROMPT_HERE"
      },
      {
        "type": "image_url",
        "image_url": { "url": "IMAGE_URL_HERE" },
        "role": "first_frame"
      }
    ],
    "ratio": "adaptive",
    "duration": 5,
    "resolution": "720p",
    "generate_audio": true
  }')

TASK_ID=$(echo "$TASK_RESULT" | python3 -c "import sys,json; print(json.load(sys.stdin)['id'])")
echo "Task created: $TASK_ID"
```

**With local image file (convert to base64):**
```bash
IMG_PATH="/path/to/image.png"
IMG_EXT="${IMG_PATH##*.}"
IMG_EXT_LOWER=$(echo "$IMG_EXT" | tr '[:upper:]' '[:lower:]')
IMG_BASE64=$(base64 < "$IMG_PATH" | tr -d '\n')
IMG_DATA_URL="data:image/${IMG_EXT_LOWER};base64,${IMG_BASE64}"

TASK_RESULT=$(curl -s -X POST "https://ark.cn-beijing.volces.com/api/v3/contents/generations/tasks" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $ARK_API_KEY" \
  -d '{
    "model": "doubao-seedance-2-0-260128",
    "content": [
      {
        "type": "text",
        "text": "YOUR_PROMPT_HERE"
      },
      {
        "type": "image_url",
        "image_url": { "url": "'"$IMG_DATA_URL"'" },
        "role": "first_frame"
      }
    ],
    "ratio": "adaptive",
    "duration": 5,
    "resolution": "720p",
    "generate_audio": true
  }')

TASK_ID=$(echo "$TASK_RESULT" | python3 -c "import sys,json; print(json.load(sys.stdin)['id'])")
echo "Task created: $TASK_ID"
```

#### Mode C: Image-to-Video (First + Last Frame)

Requires two images.

```bash
TASK_RESULT=$(curl -s -X POST "https://ark.cn-beijing.volces.com/api/v3/contents/generations/tasks" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $ARK_API_KEY" \
  -d '{
    "model": "doubao-seedance-2-0-260128",
    "content": [
      {
        "type": "text",
        "text": "YOUR_PROMPT_HERE"
      },
      {
        "type": "image_url",
        "image_url": { "url": "FIRST_FRAME_IMAGE_URL" },
        "role": "first_frame"
      },
      {
        "type": "image_url",
        "image_url": { "url": "LAST_FRAME_IMAGE_URL" },
        "role": "last_frame"
      }
    ],
    "ratio": "adaptive",
    "duration": 5,
    "resolution": "720p",
    "generate_audio": true
  }')

TASK_ID=$(echo "$TASK_RESULT" | python3 -c "import sys,json; print(json.load(sys.stdin)['id'])")
echo "Task created: $TASK_ID"
```

### Step 2: Poll for Task Completion

Video generation is asynchronous. Poll the task status until it completes.

```bash
echo "Waiting for video generation to complete..."
while true; do
  STATUS_RESULT=$(curl -s -X GET "https://ark.cn-beijing.volces.com/api/v3/contents/generations/tasks/${TASK_ID}" \
    -H "Authorization: Bearer $ARK_API_KEY")

  STATUS=$(echo "$STATUS_RESULT" | python3 -c "import sys,json; print(json.load(sys.stdin)['status'])")

  if [ "$STATUS" = "succeeded" ]; then
    echo "Video generation succeeded!"
    VIDEO_URL=$(echo "$STATUS_RESULT" | python3 -c "import sys,json; print(json.load(sys.stdin)['content']['video_url'])")
    echo "Video URL: $VIDEO_URL"
    break
  elif [ "$STATUS" = "failed" ]; then
    ERROR_MSG=$(echo "$STATUS_RESULT" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('error',{}).get('message','Unknown error'))" 2>/dev/null || echo "Unknown error")
    echo "Video generation failed: $ERROR_MSG"
    break
  elif [ "$STATUS" = "expired" ]; then
    echo "Video generation task expired."
    break
  else
    echo "Status: $STATUS - still processing..."
    sleep 15
  fi
done
```

### Step 3: Download and Open Video

```bash
OUTPUT_PATH="$HOME/Desktop/seedance_video_$(date +%Y%m%d_%H%M%S).mp4"
curl -s -o "$OUTPUT_PATH" "$VIDEO_URL"
echo "Video saved to: $OUTPUT_PATH"
open "$OUTPUT_PATH"
```

## Optional Parameters Reference

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `model` | string | `doubao-seedance-2-0-260128` | Model ID to use |
| `ratio` | string | `16:9` (text2vid) / `adaptive` (img2vid) | Aspect ratio: `16:9`, `4:3`, `1:1`, `3:4`, `9:16`, `21:9`, `adaptive` |
| `duration` | integer | `5` | Video duration in seconds (4-15 for 2.0). Set `-1` for auto |
| `resolution` | string | `720p` | Resolution: `480p`, `720p` (1080p is not supported by 2.0) |
| `seed` | integer | `-1` | Random seed for reproducibility. -1 = random |
| `camera_fixed` | boolean | `false` | Fix camera position |
| `watermark` | boolean | `false` | Add watermark to video |
| `generate_audio` | boolean | `true` | Generate synchronized audio. When `true`, the model automatically generates matching human voice, sound effects and background music based on the text prompt and visual content. It is recommended to put dialogue in double quotes for better audio generation, e.g. `男人叫住女人说："你记住，以后不可以用手指指月亮。"` |
| `draft` | boolean | `false` | Generate draft/preview video at lower cost (forces 480p) |
| `return_last_frame` | boolean | `false` | Return last frame image URL (for chaining consecutive videos) |
| `service_tier` | string | `default` | `default` (online) or `flex` (offline, 50% cheaper, slower) |
| `execution_expires_after` | integer | `172800` | Task timeout in seconds (3600-259200) |

## Additional Operations

### Query Task Status

```bash
curl -s -X GET "https://ark.cn-beijing.volces.com/api/v3/contents/generations/tasks/${TASK_ID}" \
  -H "Authorization: Bearer $ARK_API_KEY" | python3 -m json.tool
```

### List Tasks

```bash
# List all tasks (paginated)
curl -s -X GET "https://ark.cn-beijing.volces.com/api/v3/contents/generations/tasks?page_num=1&page_size=10" \
  -H "Authorization: Bearer $ARK_API_KEY" | python3 -m json.tool

# Filter by status
curl -s -X GET "https://ark.cn-beijing.volces.com/api/v3/contents/generations/tasks?page_num=1&page_size=10&filter.status=succeeded" \
  -H "Authorization: Bearer $ARK_API_KEY" | python3 -m json.tool
```

### Cancel or Delete Task

```bash
curl -s -X DELETE "https://ark.cn-beijing.volces.com/api/v3/contents/generations/tasks/${TASK_ID}" \
  -H "Authorization: Bearer $ARK_API_KEY"
```

Note: `queued` tasks will be cancelled; `succeeded`/`failed`/`expired` tasks will be deleted from history.

### Generate Consecutive Videos (Using Last Frame)

Set `return_last_frame: true` on the first task, then use the returned `last_frame_url` as the first frame of the next task.

```bash
# Get last frame URL from completed task
LAST_FRAME_URL=$(curl -s -X GET "https://ark.cn-beijing.volces.com/api/v3/contents/generations/tasks/${TASK_ID}" \
  -H "Authorization: Bearer $ARK_API_KEY" | python3 -c "import sys,json; print(json.load(sys.stdin)['content']['last_frame_url'])")

# Use it as first frame for the next video
# ... (use Mode B with LAST_FRAME_URL as the image URL)
```

### Draft Mode (Seedance 2.0)

Generate a cheap preview first, then produce the final video if satisfied:

```bash
# Step 1: Create draft
DRAFT_RESULT=$(curl -s -X POST "https://ark.cn-beijing.volces.com/api/v3/contents/generations/tasks" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $ARK_API_KEY" \
  -d '{
    "model": "doubao-seedance-2-0-260128",
    "content": [
      { "type": "text", "text": "YOUR_PROMPT_HERE" }
    ],
    "draft": true,
    "resolution": "480p"
  }')
DRAFT_TASK_ID=$(echo "$DRAFT_RESULT" | python3 -c "import sys,json; print(json.load(sys.stdin)['id'])")

# Step 2: After draft succeeds, generate final video from draft
FINAL_RESULT=$(curl -s -X POST "https://ark.cn-beijing.volces.com/api/v3/contents/generations/tasks" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $ARK_API_KEY" \
  -d '{
    "model": "doubao-seedance-2-0-260128",
    "content": [
      {
        "type": "draft_task",
        "draft_task": { "id": "'"$DRAFT_TASK_ID"'" }
      }
    ],
    "resolution": "720p"
  }')
```

## Long-Video Generation (超过 15 秒的视频)

Seedance 2.0 单次生成的最大时长为 **15 秒**。如果用户需要更长的视频（如 30 秒、1 分钟的品牌宣传片），**绝对不能直接调用生成命令**，必须按以下工作流执行：

### 强制工作流（四步法）

#### Step 1: 需求拆解与方案设计
当用户提出"帮我生成一个 1 分钟的品牌食品宣传视频"这类需求时，首先根据品牌调性、产品特点、目标受众，将视频按时间线拆分为多个 4~15 秒的片段，并为每段写出详细的画面描述（提示词）。

#### Step 2: 向用户展示方案并确认
**必须**将拆解后的分镜脚本完整展示给用户，包括：
- 每段的时间范围
- 该段的画面内容、场景、人物、运镜、光影、情绪
- 详细的 prompt（这些 prompt 将原封不动传给模型）

**在得到用户明确的"可以"/"OK"/"没问题"等肯定答复之前，禁止调用任何生成接口。**

#### Step 3: 按顺序生成（必须串行）
用户确认后，使用 `sequence` 命令或手动分步生成：
- 设置 `return_last_frame=true`
- 第 1 段生成完毕后，提取尾帧图像
- 将尾帧作为第 2 段的 `first_frame`（`auto`）
- **严格按顺序一段一段来**，不能并行
- 每段是否需要额外提供尾帧，由你根据过渡需求分析决定

#### Step 4: 规范保存
使用 `--output-dir` 指定统一的输出目录。工具会自动保存：
- 每段生成的 MP4 视频
- 每段的尾帧 PNG 图像
- `sequence_manifest.json` 索引文件（记录任务 ID、视频地址、尾帧路径）

---

### 对话示例：用户要求"帮我生成一个 1 分钟的品牌食品宣传视频"

你应该这样回复用户：

> Seedance 2.0 单次最长只能生成 15 秒，所以我帮你把这个 1 分钟的宣传片拆成了 4 个连续镜头，每段用上一段的尾帧作为下一段的首帧，保证画面无缝衔接。以下是详细的分镜方案：
>
> **第 1 段（0-5 秒）：品牌符号唤醒**
> - 时长：5 秒
> - 画面：特写镜头，现代简约北欧风客厅，浅米色布艺沙发上放着一包红色包装的巧克力饼干。窗外午后阳光柔和洒入，镜头缓慢推进聚焦 Logo。背景虚化，暖色调，无人物。
>
> **第 2 段（5-15 秒）：产品卖点展示**
> - 时长：10 秒
> - 画面：中景，一位 20 多岁的年轻女性坐在同一沙发上，拆开包装，取出饼干咬下一口，酥脆碎屑微落。镜头从侧面 45 度捕捉她满足的微笑。午后侧逆光，背景是模糊的书架和绿植。
>
> **第 3 段（15-30 秒）：情感共鸣场景**
> - 时长：15 秒
> - 画面：全景，同一客厅，茶几上摆着饼干和热可可。女性搂着 7 岁小女孩，将饼干递给旁边的男性，三人相视而笑。镜头缓缓后拉，窗外夕阳洒满房间，金色暖光，传递幸福团聚感。
>
> **第 4 段（30-60 秒）：品牌价值升华**
> - 时长：15 秒（注：若需严格 60 秒，可将第 3、4 段各延长至 15 秒并增加 1 段 10 秒片段）
> - 画面：夜晚同一客厅，暖黄灯光下，一家人围坐在地毯上玩游戏，茶几中央放着饼干。镜头从窗外缓缓推进穿过玻璃，最终定格在饼干的红色包装上，包装反射着温馨的室内灯光。
>
> 你觉得这个分镜和提示词 OK 吗？如果有想调整的地方（比如换场景、换人物、改台词/音乐），请告诉我。确认后我就按顺序开始生成。

**只有在用户回复"可以"之后，才能执行下面的命令。**

### 使用 `sequence` 命令一键生成

CLI 提供了 `sequence` 子命令，可自动完成"创建任务 → **自动轮询等待完成** → 提取尾帧 → **自动继续下一段**"的完整循环。你不需要手动干预，命令会一直运行直到所有片段全部生成完毕。

```bash
python3 ~/.claude/skills/seedance-2-0-video/seedance.py sequence \
  --config '[
    {
      "prompt": "特写镜头：现代简约北欧风客厅，浅米色布艺沙发上放着一包红色包装的巧克力饼干。窗外是午后温暖阳光，光线柔和地洒在沙发上。镜头缓慢推进，聚焦到饼干包装袋的Logo。背景虚化，营造温馨家居氛围。无人物出现，画面干净明亮，暖色调。",
      "duration": 5
    },
    {
      "prompt": "中景：一位20多岁的年轻女性，棕色长发，穿着米色针织毛衣，坐在同一浅米色沙发上。她拆开巧克力饼干包装，取出一片饼干，咬下一口，酥脆的碎屑微微掉落。镜头从侧面45度角拍摄，捕捉到她的表情从期待到满足的微笑。午后阳光从侧面照进来，形成自然的轮廓光。背景是模糊的白色书架和绿植。暖色调，温馨惬意。",
      "duration": 10,
      "first_frame": "auto"
    },
    {
      "prompt": "全景：同一现代客厅，茶几上摆放着饼干和几杯热可可。年轻女性坐在沙发中央，左手搂着一位7岁左右的小女孩（扎着双马尾，穿着粉色家居服），右手将一片饼干递给旁边的一位30岁左右的男性（穿着浅蓝色衬衫，戴着黑框眼镜）。三个人相视而笑，小女孩接过饼干开心地晃了晃腿。镜头缓慢向后拉远，展现完整的家庭互动画面。窗外夕阳余晖洒满房间，整个场景笼罩在金色的暖光中，传递出幸福、分享与团聚的情感。",
      "duration": 15,
      "first_frame": "auto"
    }
  ]' \
  --ratio 16:9 \
  --resolution 720p \
  --output-dir "~\\.openclaw\\workspace\\files\\oreo_video"
```

**参数说明**：
- `--config`：JSON 数组，每个元素是一个片段配置。必须包含 `prompt` 和 `duration`。
  - `first_frame`: `"auto"` 表示自动使用上一段的尾帧；也可以填本地图片路径或 URL。
  - `last_frame`: 可填本地图片路径或 URL，作为该片段的尾帧（由大模型分析是否需要）。
  - 其他字段如 `ratio`、`resolution`、`generate_audio` 等可在单段内覆盖全局默认值。
- `--output-dir`：所有视频片段、尾帧图像和 manifest 文件的保存目录。**如果不指定，默认会在 `~\.openclaw\workspace\files` 下创建一个带时间戳的子目录（如 `seedance_sequence_20250414_141530`）。**

### 手动分步生成（备用）

如果不想使用 `sequence` 命令，也可以手动执行：

```bash
# 第 1 段
python3 ~/.claude/skills/seedance-2-0-video/seedance.py create \
  --prompt "开场白，展示品牌Logo" \
  --duration 5 --return-last-frame true --wait --download "~\\.openclaw\\workspace\\files\\video"

# 提取尾帧（上面 --download 已自动保存，也可用 last-frame 命令）
python3 ~/.claude/skills/seedance-2-0-video/seedance.py last-frame <TASK_ID_1> \
  --output "~\\.openclaw\\workspace\\files\\video\\segment_01_last_frame.png"

# 第 2 段：以第 1 段尾帧作为首帧
python3 ~/.claude/skills/seedance-2-0-video/seedance.py create \
  --prompt "产品特写展示" \
  --image "~\\.openclaw\\workspace\\files\\video\\segment_01_last_frame.png" \
  --duration 10 --return-last-frame true --wait --download "~\\.openclaw\\workspace\\files\\video"

# 第 3 段：继续衔接
python3 ~/.claude/skills/seedance-2-0-video/seedance.py create \
  --prompt "用户使用场景" \
  --image "~\\.openclaw\\workspace\\files\\video\\segment_02_last_frame.png" \
  --duration 15 --wait --download "~\\.openclaw\\workspace\\files\\video"
```

### 注意事项

- **必须征得用户同意后再生成**，不要在未确认的情况下直接调用 API。
- 为了最佳的连贯性，建议相邻片段的 `ratio`、`resolution` 保持一致。
- 如果用户希望长视频中的某一段有对话/音效，某一段纯音乐或静音，可在对应片段的 `prompt` 中明确说明，或单独设置 `generate_audio`。
- 所有生成的片段可以在后期用视频编辑工具拼接成完整长视频；当前 API 不提供自动拼接功能。

## Image Requirements

- Formats: jpeg, png, webp, bmp, tiff, gif, heic, heif
- Aspect ratio (width/height): between 0.4 and 2.5
- Dimensions: 300-6000 px per side
- Max file size: 30 MB
