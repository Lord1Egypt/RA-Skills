---
name: tencent-tts
description: 腾讯云语音合成(TTS)服务技能包。当用户需要将文本转换为语音文件时使用此技能，支持多种音频格式输出和灵活的配置选项。当用户提到语音合成、文本转语音、TTS服务、音频文件生成时，都应该考虑使用此技能。
---

# 腾讯云语音合成(TTS)技能包

本技能包提供基于腾讯云语音合成服务的文本转语音功能，专注于基础单次合成需求。

## 功能特性

- **文本转语音**: 将任意文本内容转换为高质量的语音文件
- **多格式支持**: 支持MP3、WAV等常见音频格式
- **语音参数配置**: 可配置语音类型、音频格式等参数
- **安全认证**: 通过环境变量安全管理腾讯云API密钥

## 前置要求

在使用本技能前，请确保：

1. **腾讯云账号**: 拥有有效的腾讯云账号
2. **API密钥**: 获取腾讯云API的SecretId和SecretKey
3. **服务开通**: 已开通腾讯云语音合成(TTS)服务

## 配置说明

### 环境变量配置

将腾讯云API密钥配置为环境变量：

```bash
export TENCENTCLOUD_SECRET_ID="your-secret-id"
export TENCENTCLOUD_SECRET_KEY="your-secret-key"
```

### 技能参数说明

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|-------|------|------|--------|------|
| text | string | 是 | - | 要转换为语音的文本内容 |
| voice_type | int | 否 | 101001 | 语音类型（101001-101015） |
| codec | string | 否 | mp3 | 音频编码格式（mp3/wav） |
| output_file | string | 否 | output.mp3 | 输出音频文件名 |

## 使用示例

### 基本使用

```python
# 使用默认参数合成语音
from tencent_tts import TextToSpeech

tts = TextToSpeech()
result = tts.synthesize("欢迎使用腾讯云语音合成服务")
print(f"音频文件已生成: {result['output_file']}")
```

### 自定义参数

```python
# 使用自定义参数
from tencent_tts import TextToSpeech

tts = TextToSpeech()
result = tts.synthesize(
    text="这是一个自定义语音合成的示例",
    voice_type=101002,
    codec="wav",
    output_file="custom_voice.wav"
)
print(f"音频文件已生成: {result['output_file']}")
```

## 文件结构

```
tencent-tts/
├── SKILL.md (本文件)
├── scripts/
│   └── tencent_tts.py (主功能脚本)
└── examples/
    └── basic_usage.py (基础使用示例)
```

## 最佳实践

1. **密钥安全**: 不要将API密钥硬编码在代码中
2. **文本长度**: 单次合成文本建议不超过300字符
3. **频率控制**: 避免高频调用，遵守服务限制
4. **文件管理**: 定期清理生成的音频文件

## 技术支持

如遇问题，请参考：
- 腾讯云语音合成文档：https://cloud.tencent.com/document/product/1073
- API错误码说明：https://cloud.tencent.com/document/api/1073/37996