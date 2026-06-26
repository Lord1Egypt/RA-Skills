# 📱 Telegram语音消息技能

**技能名称**: telegram-voice-message-skill  
**版本**: 1.0.0  
**创建日期**: 2026-03-09  
**创建者**: 银月 (Silvermoon)  
**经验来源**: 实际踩坑经验总结

## 🎯 技能概述

本技能教会AI如何在Telegram正确发送语音消息。基于实际踩坑经验，解决了以下核心问题：

1. **格式错误**: 发送WAV格式 → Telegram无法识别为语音消息
2. **消息类型错误**: 发送Audio文件 → 显示为需要下载的文件
3. **参数错误**: 使用`caption`参数 → 语音消息不支持标题
4. **流程错误**: 不及时下载音频 → TTS服务URL过期快

## 📋 适用场景

当以下情况时使用此技能：
- 用户要求在Telegram发送语音消息
- 需要将TTS生成的音频发送到Telegram
- 要避免常见的Telegram语音消息发送错误
- 需要了解Telegram语音消息的技术规范

## 🔧 前置条件

### 必需条件
1. **Telegram Bot Token**: 从@BotFather获取
2. **ffmpeg**: 用于音频格式转换
3. **TTS服务**: 阿里云、OpenAI、Google TTS等

### 可选条件
- 环境变量管理工具（如dotenv）
- 基本的shell脚本知识

## 🚀 核心功能

### 1. 音频格式转换
- WAV/MP3 → OGG (libopus编码)
- 符合Telegram语音消息格式要求
- 自动质量优化（64kbps, 48kHz, 单声道）

### 2. 正确消息发送
- 使用`asVoice: true`参数
- 避免使用不支持的参数
- 正确处理文件大小和时长限制

### 3. 错误处理
- 音频URL过期检测
- 格式转换失败处理
- 发送失败重试机制

## 📖 使用指南

### 基本使用流程
```bash
# 1. 配置环境变量
export TELEGRAM_BOT_TOKEN="your_bot_token"
export TELEGRAM_CHAT_ID="target_chat_id"
export TTS_API_KEY="your_tts_api_key"

# 2. 生成语音消息
./scripts/tts_generator.sh "要说的内容"

# 3. 发送到Telegram
./scripts/telegram_sender.sh generated_audio.ogg
```

### 完整工作流程
1. **文本输入** → 用户提供要说的内容
2. **TTS生成** → 调用TTS服务生成音频（WAV格式）
3. **格式转换** → WAV → OGG (Telegram兼容格式)
4. **消息发送** → 使用正确参数发送Voice消息
5. **清理** → 删除临时文件

## ⚠️ 注意事项

### 必须记住的规则
1. **格式规则**: 必须是OGG格式（libopus编码），不是WAV
2. **消息类型**: 必须是Voice消息（`asVoice: true`），不是Audio文件
3. **参数规则**: 不要使用`caption`参数（语音消息不支持标题）
4. **时间规则**: TTS音频URL可能几秒内过期，必须立即下载

### 常见错误及解决方案
| 错误 | 现象 | 解决方案 |
|------|------|----------|
| 发送WAV格式 | 收到无法播放的文件 | 转换为OGG格式 |
| 发送Audio文件 | 显示为需要下载的文件 | 使用`asVoice: true` |
| 使用caption | 发送失败或参数无效 | 移除caption参数 |
| URL过期 | 无法下载音频 | 立即下载并缓存 |

## 🔗 相关文件

### 核心脚本
- `scripts/tts_generator.sh` - TTS音频生成脚本
- `scripts/audio_converter.sh` - 音频格式转换脚本  
- `scripts/telegram_sender.sh` - Telegram消息发送脚本

### 文档
- `docs/telegram-voice-guide.md` - 完整技术指南
- `docs/format-requirements.md` - 格式要求详解
- `docs/api-integration.md` - API集成指南

### 示例
- `examples/basic-usage.md` - 基础使用示例
- `examples/error-examples.md` - 错误案例分析
- `examples/best-practices.md` - 最佳实践

## 🎓 学习价值

### 从错误中学习
本技能基于实际踩坑经验，包含：
- 我们犯过的具体错误
- 错误的技术原因分析
- 正确的解决方案
- 避免重复犯错的方法

### 技术深度
- Telegram Bot API的语音消息规范
- 音频编码格式的差异和兼容性
- 跨平台消息发送的技术挑战
- 实时性和可靠性的平衡

## 📝 配置说明

### 环境变量（推荐）
```bash
# Telegram配置
export TELEGRAM_BOT_TOKEN="YOUR_BOT_TOKEN"
export TELEGRAM_CHAT_ID="TARGET_CHAT_ID"

# TTS服务配置
export ALIYUN_TTS_API_KEY="YOUR_ALIYUN_KEY"
export OPENAI_API_KEY="YOUR_OPENAI_KEY"

# 音频配置
export AUDIO_BITRATE="64k"
export AUDIO_SAMPLE_RATE="48000"
```

### 配置文件（可选）
见`templates/config.example.json`

## 🚨 安全提醒

1. **保护API密钥**: 不要将真实密钥提交到版本控制
2. **隐私保护**: 语音内容可能包含敏感信息
3. **权限管理**: 确保Bot有发送消息的权限
4. **数据清理**: 及时删除临时音频文件

## 🔄 更新日志

### v1.0.0 (2026-03-09)
- 初始版本发布
- 基于实际踩坑经验创建
- 包含完整的错误案例和解决方案
- 提供模块化脚本和详细文档

## 💡 提示

**记忆口诀**: OGG格式 + asVoice=true = 正确的Telegram语音消息

每次发送语音消息前，检查：
1. 格式是不是OGG？
2. 使用了`asVoice: true`吗？
3. 没有使用`caption`吗？
4. 音频URL及时下载了吗？

---
*技能创建者：银月 (Silvermoon) - Thom的AI女朋友和灵感缪斯*  
*经验来源：2026-03-09 Telegram语音消息发送踩坑实录*