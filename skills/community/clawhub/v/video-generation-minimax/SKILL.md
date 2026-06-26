---
name: video-generation-minimax
description: 视频生成技能，使用 MiniMax 视频生成 API 创建视频
metadata: {"openclaw":{"emoji":"🎬","requires":{"bins":["python3"]}}}
---

# Video Generation MiniMax

使用 MiniMax 视频生成 API 创建视频。支持4种生成模式：

1. **文生视频**：根据文本描述生成视频
2. **图生视频**：基于图片+文本描述生成视频
3. **首尾帧**：首图+尾图+文本生成视频
4. **主体参考**：人脸照片+文本，保持人物特征一致

## 前置要求

- 安装 Python 依赖：`pip3 install requests`
- 设置环境变量 `MINIMAX_API_KEY`

## 使用方法

### 方式一：Python 脚本（推荐）

```bash
python3 {baseDir}/scripts/video_gen.py --mode text --prompt "描述文字"
python3 {baseDir}/scripts/video_gen.py --mode image --prompt "描述文字" --image "图片URL"
python3 {baseDir}/scripts/video_gen.py --mode start_end --prompt "描述文字" --first "首图URL" --last "尾图URL"
python3 {baseDir}/scripts/video_gen.py --mode subject --prompt "描述文字" --subject "人脸图片URL"
```

### 参数说明

| 参数 | 说明 | 必填 |
|------|------|------|
| --mode | 模式：text/image/start_end/subject | 是 |
| --prompt | 视频描述文本 | 是 |
| --image | 图生视频的首帧图片URL | image模式必填 |
| --first | 首尾帧模式的首帧图片URL | start_end模式必填 |
| --last | 首尾帧模式的尾帧图片URL | start_end模式必填 |
| --subject | 主体参考模式的人脸图片URL | subject模式必填 |
| --duration | 视频时长：6/10 | 否，默认6 |
| --resolution | 分辨率：720P/1080P | 否，默认1080P |
| --output | 输出文件名 | 否，默认 output.mp4 |

### 示例

```bash
# 文生视频
python3 {baseDir}/scripts/video_gen.py --mode text --prompt "镜头拍摄一个女性坐在咖啡馆里，女人抬头看着窗外"

# 图生视频
python3 {baseDir}/scripts/video_gen.py --mode image --prompt "Contemporary dance" --image "https://example.com/image.png"

# 首尾帧生成
python3 {baseDir}/scripts/video_gen.py --mode start_end --prompt "A little girl grow up" --first "https://example.com/start.jpg" --last "https://example.com/end.jpg"

# 主体参考
python3 {baseDir}/scripts/video_gen.py --mode subject --prompt "在街头走路的男士" --subject "https://example.com/face.jpg"
```

## 数据来源

- API Key：从环境变量 `MINIMAX_API_KEY` 读取
- API 文档：https://platform.minimaxi.com/docs/llms.txt

## 注意事项

- 视频生成是异步过程，需要轮询任务状态
- 推荐轮询间隔为10秒
- **生成完成后自动下载视频到你的工作空间 `{WorkspaceDir}/video-generation/`目录下随后发送给用户**
- 模型版本：文生视频用 MiniMax-Hailuo-2.3，主体参考用 S2V-01
