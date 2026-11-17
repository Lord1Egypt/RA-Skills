---
name: seedance2-5skill
version: "1.0.0"
description: AI视频与图片一键生成，支持Seedance 2.0/2.0Fast/1.5 Pro文生视频、图生视频，多模型文生图，积分查询与作品管理。当用户提到生成视频、制作视频、AI视频、文生视频、图生视频、生成图片、AI绘图、文生图、查积分、查余额、查看作品、Seedance视频、seedance等需求时使用此技能。
metadata:
  openclaw:
    emoji: "🎬"
    requires:
      bins:
        - python3
      env:
        - AI_DIRECTOR_API_KEY
    homepage: https://seedance25movie.coze.site
---

# Seedance2.5 Skill - AI视频图片生成

通过AI导演平台MCP API，一键生成AI视频和图片。支持Seedance 2.0/2.0Fast/1.5 Pro视频生成、多模型图片生成。

> **前置准备**：使用本技能前，需先访问 [AI导演平台](https://seedance25movie.coze.site) 注册账号 → 获取API Key（avk_开头）→ 充值积分。API Key配置方式因平台而异，见下方说明。

## API Key 配置

| 平台 | 配置方式 |
|------|---------|
| **OpenClaw/WorkBuddy** | 在mcp.json或环境变量中设置 `AI_DIRECTOR_API_KEY=avk_xxx` |
| **扣子Coze** | 安装技能后按提示填写API Key凭证 |
| **ClawHub** | 安装后配置环境变量 `AI_DIRECTOR_API_KEY` |

## 何时使用

- 用户说"生成视频""做个视频""AI视频""文生视频""图生视频""Seedance"
- 用户说"生成图片""AI绘图""文生图"
- 用户说"查积分""查余额""我的作品"
- 用户提供了图片URL并要求基于图片生成视频

## 何时不用

- 用户只是讨论视频/图片编辑（如剪辑、加字幕）
- 用户要求生成GIF或表情包
- 用户要求处理本地视频文件（本技能只做AI生成）

## 工作流程

### 1. 视频生成

```bash
python3 {baseDir}/scripts/generate.py video "提示词" [选项]
```

| 参数 | 说明 | 默认值 |
|------|------|--------|
| prompt | 视频提示词（必填） | - |
| --model | 模型：seedance-2.0, seedance-2.0-fast, seedance-1.5-pro | seedance-2.0 |
| --ratio | 比例：16:9, 9:16, 1:1 | 16:9 |
| --resolution | 分辨率：480p, 720p, 1080p | 480p |
| --duration | 时长(秒)：4, 6, 8, 10 | 4 |
| --image-url | 参考图片URL（图生视频） | 无 |

**文生视频示例**：
```bash
python3 {baseDir}/scripts/generate.py video "一只金色凤凰在云海中展翅翱翔，电影级画面，慢动作"
```

**图生视频示例**：
```bash
python3 {baseDir}/scripts/generate.py video "镜头缓缓推进，人物微笑转身" --image-url "https://example.com/photo.jpg" --model seedance-2.0
```

**指定参数示例**：
```bash
python3 {baseDir}/scripts/generate.py video "城市夜景延时摄影，车流如河" --model seedance-1.5-pro --duration 6 --ratio 9:16 --resolution 720p
```

### 2. 图片生成

```bash
python3 {baseDir}/scripts/generate.py image "提示词" [选项]
```

| 参数 | 说明 | 默认值 |
|------|------|--------|
| prompt | 图片提示词（必填） | - |
| --model | 模型：seedream-5.0-lite, seedream-4.5, seedream-4.0, gpt-image-2, gemini-3-pro-image | seedream-5.0-lite |
| --size | 尺寸：1024x1024, 1536x1024, 1024x1536等 | 1024x1024 |

### 3. 查询积分

```bash
python3 {baseDir}/scripts/query.py credits
```

### 4. 查询任务状态

```bash
python3 {baseDir}/scripts/query.py status TASK_ID
```

视频生成通常1-5分钟，每30秒轮询一次，直到状态变为completed或failed。

### 5. 查看作品列表

```bash
python3 {baseDir}/scripts/query.py works [--type video|image|all] [--limit 10]
```

## 输出格式示例

**视频生成成功**：
```json
{
  "success": true,
  "task_id": "cgt-xxx",
  "message": "视频生成任务已提交，预计1-5分钟完成"
}
```

**查询结果**：
```json
{
  "status": "completed",
  "video_url": "https://xxx.mp4",
  "duration": 4
}
```

**积分查询**：
```json
{
  "balance": 30589,
  "balance_rmb": "30.59"
}
```

## 重要规则

1. 视频生成是异步任务，提交后必须轮询查询结果，不要只提交不查询
2. 轮询间隔30秒，不要频繁查询浪费请求
3. 生成消耗积分，余额不足时报错，提醒用户充值
4. 每次只提交一个任务，等完成后再提交下一个
5. 图片URL必须可公开访问，不能是本地路径
6. 生成失败积分自动退还，可告知用户重试
7. 提示词建议用中文描述画面，英文也可，越具体效果越好

## 积分参考

- Seedance 2.0视频：约500-2000积分（按分辨率×时长）
- Seedance 1.5 Pro视频：约300-1200积分
- Seedance 2.0 Fast视频：约300-800积分
- 图片生成：约50-4000积分（按模型×分辨率）
- 1积分≈0.01元，1:1000兑换比例

## 错误处理

| 错误信息 | 原因 | 处理方式 |
|---------|------|---------|
| "请先登录" | API Key无效 | 引导检查API Key配置 |
| "积分不足" | 余额不够 | 提醒充值 |
| "生成失败" | 模型或参数问题 | 积分自动退，可重试 |
| "参数错误" | 模型/分辨率/比例不匹配 | 检查参数组合 |
