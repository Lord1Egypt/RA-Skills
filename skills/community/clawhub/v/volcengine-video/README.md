# 火山引擎视频生成技能 (VolcEngine Video Generation)

这个技能封装了火山引擎的AI视频生成API，支持文本到视频的生成以及任务状态查询。

## 功能

1. **视频生成** - 根据文本提示生成AI视频
2. **任务查询** - 轮训已提交任务的状态和获取视频URL

## 使用方法

### 1. 配置API密钥

将你的火山引擎API密钥保存到配置文件：
```json
{
  "access_key": "你的访问密钥",
  "secret_key": "你的秘密密钥"
}
```

配置文件路径：`E:\OpenClaw_workspace\skills\volcengine-video\config.json`

### 2. 触发技能

- **生成视频**: "用火山引擎生成一个[描述]的视频，[帧数]帧"
  - 示例: "用火山引擎生成一个小猫游泳的视频，241帧"
  
- **查询任务**: "查询火山引擎任务[任务ID]的状态"
  - 示例: "查询火山引擎任务12754421025266709930的状态"

### 3. 脚本说明

- `scripts/volcengine_video.py` - 视频生成脚本
- `scripts/query_task.py` - 任务状态查询脚本

## API详情

- 使用火山引擎CVSync2AsyncSubmitTask接口进行视频生成
- 使用火山引擎CVSync2AsyncGetResult接口查询任务状态
- 支持自定义提示词(prompt)、帧数(frames)等参数
- 自动处理V4签名认证

## 返回结果

- **视频生成**: 返回任务ID，用于后续查询
- **任务查询**: 返回任务状态(done/processing)和视频URL(如果已完成)