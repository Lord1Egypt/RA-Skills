---
name: minimax-video
description: MiniMax 视频生成技能。集成文生视频、图生视频、首尾帧生成视频功能。触发场景：(1) 用户请求生成视频，(2) 用户提供描述创建视频，(3) 用户上传图片生成视频，(4) 用户提供首尾帧图片生成过渡视频，(5) 用户想要查询视频生成任务状态。支持运镜指令：[左移], [右移], [左摇], [右摇], [推进], [拉远], [上升], [下降], [上摇], [下摇], [变焦推近], [变焦拉远], [晃动], [跟随], [固定]。
---

# MiniMax 视频生成技能

## 功能概览

| 功能 | API 端点 | 模型 | 说明 |
|------|----------|------|------|
| 文生视频 | `/v1/video_generation` | `T2V-01`, `T2V-01-Director`, `MiniMax-Hailuo-2.3`, `MiniMax-Hailuo-02` | 从文本生成视频 |
| 图生视频 | `/v1/video_generation` | `I2V-01`, `I2V-01-Director`, `I2V-01-live`, `MiniMax-Hailuo-2.3`, `MiniMax-Hailuo-2.3-Fast`, `MiniMax-Hailuo-02` | 从图片生成视频 |
| 首尾帧生成 | `/v1/video_generation` | `MiniMax-Hailuo-02` | 前后两张图生成过渡视频 |
| 查询状态 | `/v1/query/video_generation` | - | 查询任务进度 |

## 工作流程

```
1. 提交任务 → 获取 task_id
2. 轮询状态 → 显示进度 (Preparing → Queueing → Processing → Success/Fail)
3. 自动下载 → 保存到本地（URL有效期短，需立即保存）
```

## 快速开始

### 文生视频

```python
import requests
import os

API_KEY = os.getenv("MINIMAX_API_KEY")

response = requests.post(
    "https://api.minimaxi.com/v1/video_generation",
    headers={
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    },
    json={
        "model": "MiniMax-Hailuo-2.3",
        "prompt": "一只猫在草地上玩耍 [左摇,上升]",
        "duration": 6,
        "resolution": "1080P"
    }
)

task_id = response.json()["task_id"]

# 查询状态
status_resp = requests.get(
    f"https://api.minimaxi.com/v1/query/video_generation?task_id={task_id}",
    headers={"Authorization": f"Bearer {API_KEY}"}
)
status = status_resp.json()["status"]

# 下载视频
if status == "Success":
    file_id = status_resp.json()["file_id"]
    
    # 获取下载链接（有效期1小时，需立即下载）
    file_resp = requests.get(
        f"https://api.minimaxi.com/v1/files/retrieve?file_id={file_id}",
        headers={"Authorization": f"Bearer {API_KEY}"}
    )
    download_url = file_resp.json()["file"]["download_url"]
    
    # 保存到本地
    save_dir = "~/.openclaw/workspace/assets/videos"
    os.makedirs(save_dir, exist_ok=True)
    save_path = os.path.join(save_dir, f"video_{task_id}.mp4")
    
    video_resp = requests.get(download_url, timeout=120)
    with open(save_path, 'wb') as f:
        f.write(video_resp.content)
```

### 图生视频

```python
import base64

with open("start_image.jpg", "rb") as f:
    img_base64 = base64.b64encode(f.read()).decode()

response = requests.post(
    "https://api.minimaxi.com/v1/video_generation",
    headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"},
    json={
        "model": "MiniMax-Hailuo-2.3",
        "first_frame_image": f"data:image/jpeg;base64,{img_base64}",
        "prompt": "人物转身离开 [右移]",
        "duration": 6,
        "resolution": "1080P"
    }
)
```

### 首尾帧生成视频

```python
response = requests.post(
    "https://api.minimaxi.com/v1/video_generation",
    headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"},
    json={
        "model": "MiniMax-Hailuo-02",
        "first_frame_image": "https://example.com/start.jpg",
        "last_frame_image": "https://example.com/end.jpg",
        "prompt": "小女孩成长",
        "duration": 6,
        "resolution": "1080P"
    }
)
```

## 支持的模型

### 文生视频模型

| 模型 | 分辨率 | 时长 | 说明 |
|------|--------|------|------|
| `MiniMax-Hailuo-2.3` | 768P, 1080P | 6s, 10s | 高质量（推荐） |
| `MiniMax-Hailuo-02` | 512P, 768P, 1080P | 6s, 10s | 快速稳定 |
| `T2V-01-Director` | 720P | 6s | 导演模式 |
| `T2V-01` | 720P | 6s | 基础模型 |

### 图生视频模型

| 模型 | 分辨率 | 时长 | 说明 |
|------|--------|------|------|
| `MiniMax-Hailuo-2.3` | 768P, 1080P | 6s, 10s | 高质量（推荐） |
| `MiniMax-Hailuo-2.3-Fast` | 768P, 1080P | 6s, 10s | 快速 |
| `MiniMax-Hailuo-02` | 512P, 768P, 1080P | 6s, 10s | 快速稳定 |
| `I2V-01-Director` | 720P | 6s | 导演模式 |
| `I2V-01-live` | 720P | 6s | 真实感 |
| `I2V-01` | 720P | 6s | 基础模型 |

## 运镜指令

支持 15 种运镜指令，可在 prompt 中使用 `[指令]` 语法：

| 类别 | 指令 |
|------|------|
| 左右移 | `[左移]`, `[右移]` |
| 左右摇 | `[左摇]`, `[右摇]` |
| 推拉 | `[推进]`, `[拉远]` |
| 升降 | `[上升]`, `[下降]` |
| 上下摇 | `[上摇]`, `[下摇]` |
| 变焦 | `[变焦推近]`, `[变焦拉远]` |
| 其他 | `[晃动]`, `[跟随]`, `[固定]` |

### 使用规则

- **组合运镜**：同一组 `[]` 内多个指令同时生效，如 `[左摇,上升]`，建议不超过 3 个
- **顺序运镜**：前后出现的指令依次生效，如 `...[推进], 然后...[拉远]`

## 输入图片要求

| 项目 | 要求 |
|------|------|
| 格式 | JPG, JPEG, PNG, WebP |
| 大小 | 小于 20MB |
| 尺寸 | 短边 > 300px，长宽比 2:5 ~ 5:2 |

## 任务状态

| 状态 | 说明 |
|------|------|
| `Preparing` | 准备中 |
| `Queueing` | 队列中 |
| `Processing` | 生成中 |
| `Success` | 成功（可用 file_id 下载） |
| `Fail` | 失败 |

## 输出目录

生成的视频保存在：`~/.openclaw/workspace/assets/videos/`

**注意**：下载链接有效期仅 1 小时，生成后立即保存到本地。

## 错误码

| 错误码 | 说明 |
|--------|------|
| 0 | 成功 |
| 1002 | 触发限流 |
| 1004 | 鉴权失败 |
| 1008 | 余额不足 |
| 1026 | 描述涉及敏感内容 |
| 1027 | 生成视频涉及敏感内容 |
| 2013 | 参数异常 |
| 2049 | 无效 API Key |

## 脚本工具

- `scripts/generate_video.py` - 文生视频 + 图生视频（自动保存本地，显示进度）

### 命令行用法

```bash
# 文生视频
python generate_video.py "一只猫在草地上玩耍" --model MiniMax-Hailuo-2.3 --duration 6 --resolution 1080P

# 图生视频
python generate_video.py "人物转身" --model MiniMax-Hailuo-2.3 --first-image path/to/image.jpg

# 首尾帧生成
python generate_video.py "小女孩成长" --model MiniMax-Hailuo-02 --first-image start.jpg --last-image end.jpg

# 查询任务状态
python generate_video.py --query --task-id 123456789
```

## API 参考

详细文档见 [references/video-api.md](references/video-api.md)。
