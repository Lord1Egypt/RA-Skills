---
name: qwb-cli
description: >-
  企微瓣 (Qiweiban) AI 平台 CLI 工具。提供语音合成、声音克隆、数字人视频生成、AI 对话、图片生成、瓣值管理等能力。
  当用户需要"生成语音"、"合成语音"、"克隆声音"、"生成数字人视频"、"文字转语音"、"AI对话"、"生成图片"、
  "文生图"、"图生图"、"查看瓣值"、"查消费记录"时触发。也适用于用户提到"企微瓣"、"qwb"、"qiweiban"时。
metadata:
  requires:
    bins: ["qwb"]
  cliHelp: "qwb --help"
---

# 企微瓣 CLI 技能 (qwb-cli)

> `qwb` 是企微瓣平台的命令行工具，所有操作通过执行 `qwb` 命令完成。
> 安装：`npm install -g qwb-cli`
> 输出默认为 JSON 格式（AI 友好），加 `--format table` 可切换为人类友好表格。

---

## 前置条件：认证

所有业务接口（除 auth 外）都需要先登录。

```bash
# 密码登录
qwb auth login -p <手机号> -w <密码>

# 验证码登录
qwb auth send-code -p <手机号>
qwb auth login -p <手机号> -c <验证码>

# 查看登录状态
qwb auth status

# 查看/设置配置（如 API 地址）
qwb auth config                           # 查看
qwb auth config --api-url <url>           # 设置 API 地址

# 退出
qwb auth logout
```

Token 存储在 `~/.qwb/credentials.json`，默认有效期 30 天。

---

## 命令概览

| 领域 | 命令前缀 | 能力 |
|------|----------|------|
| 认证 | `qwb auth` | 登录、登出、配置管理 |
| 用户 | `qwb user` | 查看/更新用户资料 |
| 语音合成 | `qwb voice` | MiniMax TTS、音色列表、作品管理 |
| 声音克隆 | `qwb clone` | 上传音频、创建/管理克隆声音 |
| 数字人 | `qwb dh` | 列表、创建、视频生成（纯文本/音频） |
| 瓣值 | `qwb petals` | 余额概览、批次、消费历史 |
| AI 对话 | `qwb ai` | 多模型对话 |
| 阿里百炼 | `qwb ds` | 通义千问对话、CosyVoice TTS、音色克隆 |
| 图像 | `qwb image` | AI 图片生成（文生图/图生图）、去背景 |

---

## 语音合成 (qwb voice)

### 获取系统音色列表

```bash
qwb voice voices
```

返回所有可用系统音色，包含 ID、名称、性别、语言、风格、标签。

### 语音合成

```bash
# 最简用法（使用默认音色）
qwb voice synthesize -t "你好，欢迎使用企微瓣"

# 指定系统音色
qwb voice synthesize -t "你好" --voice-id <音色ID>

# 使用克隆声音
qwb voice synthesize -t "你好" --clone-id <克隆声音ID>

# 完整参数
qwb voice synthesize -t "文本内容" \
  --voice-id <id>         `# 系统音色 ID（不传用默认）` \
  --speed 1.0             `# 语速 0.5-2.0` \
  --volume 1.0            `# 音量 0.1-2.0` \
  --pitch 0               `# 音调 -1.0~1.0` \
  --emotion auto          `# 情感: auto/happy/sad/angry/calm/fluent` \
  --format mp3            `# 格式: mp3/wav/pcm` \
  --title "作品标题" \
  --subtitle              `# 生成字幕`
```

**返回**：`jobId`、`audioUrl`（或 `audioExternalUrl`）、时长、文件大小、消耗瓣值、剩余瓣值。

### 作品管理

```bash
qwb voice works                   # 作品列表（分页：--page, --limit）
qwb voice work <id>               # 作品详情
qwb voice delete <id>             # 删除作品
```

---

## 声音克隆 (qwb clone)

```bash
qwb clone list                    # 克隆声音列表（--page, --page-size, --status）
qwb clone upload --file <path>    # 上传音频文件
qwb clone create \
  --name "我的声音" \
  --voice-id <唯一ID> \
  --audio-id <upload返回的资源ID> \
  --description "描述" \
  --demo-text "试听文本"
qwb clone delete <id>             # 软删除
qwb clone restore <id>            # 恢复
```

---

## 数字人 (qwb dh)

### 查看数字人

```bash
qwb dh list                       # 所有可用数字人（含系统预设）
qwb dh my                         # 我的克隆数字人（--page, --page-size, --search）
qwb dh status <id>                # 查询创建状态
```

### 创建数字人

```bash
# 本地视频文件（自动上传到 OSS）
qwb dh create \
  --video ./my-video.mp4 \
  --name "数字人名称" \
  --gender male \
  --description "描述" \
  --wait                          # 等待创建完成（轮询状态）

# 远程 URL
qwb dh create \
  --video https://oss.example.com/video.mp4 \
  --name "数字人名称" \
  --gender female
```

### 生成数字人视频

```bash
# 最简用法（自动选择数字人 + 自动使用默认声音）
qwb dh video-create --script "你好，欢迎使用企微瓣"

# 指定数字人
qwb dh video-create --dh-id <id> --script "你好，欢迎使用企微瓣"

# 使用自定义音频（忽略 TTS）
qwb dh video-create --script "对口型文本" --audio-url <音频URL>

# 完整参数
qwb dh video-create \
  --script "脚本文本"             `# 必填` \
  --dh-id <id>                   `# 可选，不传自动选择第一个可用的` \
  --audio-url <url>              `# 可选，提供后用音频模式` \
  --speed 1                      `# TTS 语速 0.5-2` \
  --duration 30                  `# 音频时长（秒，预估消费用）` \
  --width 1080 --height 1920     `# 视频尺寸` \
  --bg-color "#EDEDED"           `# 背景颜色` \
  --wait                         `# 等待生成完成（轮询状态）`
```

**逻辑**：
- 不传 `--dh-id` → CLI 自动调用 `dh list` 获取第一个 READY 状态的数字人
- 不传 `--audio-url` → 使用 `text` 模式（数字人默认声音 TTS）
- 传了 `--audio-url` → 使用 `audio` 模式

### 查询视频状态

```bash
qwb dh video-status <jobId>       # 返回 status、videoUrl、duration、errorMessage
```

---

## 瓣值管理 (qwb petals)

```bash
qwb petals overview               # 余额概览
qwb petals batches                # 批次列表
qwb petals history                # 消费历史（--page, --limit, --type）
```

---

## AI 对话 (qwb ai)

```bash
qwb ai models                    # 获取可用模型列表

qwb ai chat -i "你好"            # 默认模型对话

qwb ai chat -i "你好" \
  --model-id <id> \
  --system-prompt "你是一个助手" \
  --temperature 0.7 \
  --max-tokens 2048 \
  --stream                       # 流式输出
```

---

## 阿里百炼 DashScope (qwb ds)

### 对话

```bash
qwb ds token                     # 获取临时 Token
qwb ds models                    # 模型列表

qwb ds chat -i "你好" \
  --model qwen-plus \            # qwen-turbo/qwen-plus/qwen-max/qwen-long
  --system-prompt "你是助手" \
  --temperature 1.0 \
  --max-tokens 2048 \
  --search                       # 启用联网搜索
```

### CosyVoice 语音合成

```bash
qwb ds voices                    # 预设音色列表

qwb ds tts -t "你好" \
  --voice longxiaochun_v2 \      # 音色 ID
  --format mp3 \
  --sample-rate 22050 \
  --volume 50 \
  --rate 1 --pitch 1
```

### 克隆音色管理

```bash
qwb ds clone-create --name "音色名" --audio-url <url> --text "训练文本"
qwb ds clone-list                # 克隆音色列表
qwb ds clone-detail <voiceId>    # 音色详情
qwb ds clone-update <voiceId> --name "新名称"
qwb ds clone-delete <voiceId>
```

---

## 图像处理 (qwb image)

### AI 图片生成

```bash
# 文生图
qwb image generate "一只可爱的橘猫在阳光下打哈欠"

# 指定尺寸和输出
qwb image generate "星际穿越风格壁纸" -s 3k -o wallpaper.png

# 图生图（单张参考）
qwb image generate "将背景换成海边" -i https://example.com/photo.jpg

# 图生图（多张参考）
qwb image generate "将图1的服装换为图2的服装" -i img1.jpg -i img2.jpg

# 选项
#   -s, --size <size>      尺寸: 2k(默认)/3k/WIDTHxHEIGHT
#   -i, --image <urls...>  参考图片 URL（支持多张）
#   --no-watermark          不添加水印
#   -o, --output <path>    保存到本地文件
```

### 图像去背景

```bash
qwb image remove-bg --image-url <url>
```

---

## 用户信息 (qwb user)

```bash
qwb user profile                  # 查看当前用户信息
qwb user update --nickname "新昵称" --avatar <url>
```

---

## 核心规则

### 输出格式
- **默认 JSON**（AI Agent 友好，机器解析）
- `--format table`：人类友好的表格
- `--format quiet`：最少输出（脚本/管道用）
- `--pretty`：格式化 JSON

### 错误处理
- 退出码：0 = 成功，1 = 业务错误，2 = 认证错误，3 = 网络错误
- 错误输出到 stderr，正常结果到 stdout
- 捕获到退出码 2 时，提示用户重新登录

### 异步任务模式
数字人创建和视频生成是异步任务：
1. 提交后返回 `jobId`
2. 加 `--wait` 自动轮询直到完成/失败
3. 不加 `--wait` 则需手动通过 `dh status <id>` 或 `dh video-status <jobId>` 查询

---

## 典型工作流

### 快速生成语音
```bash
qwb voice synthesize -t "欢迎使用企微瓣，这是一段测试语音"
```
无需指定音色，使用系统默认。返回音频 URL 和瓣值消耗。

### 快速生成数字人视频
```bash
qwb dh video-create --script "大家好，欢迎来到我们的产品发布会" --wait
```
自动选择系统数字人 → TTS 合成 → 生成视频 → 等待完成返回视频 URL。

### AI 图片创作
```bash
qwb image generate "赛博朋克城市夜景，霓虹灯闪烁" -s 3k -o cyber_city.png
```
文生图并保存到本地。

### 查看消费情况
```bash
qwb petals overview && qwb petals history --limit 5
```

### 克隆声音后合成
```bash
# 1. 上传音频
qwb clone upload --file my_voice.wav
# 2. 创建克隆（用返回的 audioId）
qwb clone create --name "我的声音" --voice-id my-voice-001 --audio-id <audioId>
# 3. 用克隆声音合成
qwb voice synthesize -t "这是用我的克隆声音说的话" --clone-id <cloneId>
```
