---
name: seedtts2
description: 豆包语音合成 2.0，支持情绪控制、多音色、语音指令。34 种音色可选，含 JARVIS 同款男声。
version: 1.0.0
author: JARVIS
license: MIT
tags:
  - tts
  - voice
  - speech
  - 语音合成
  - 豆包
---

# 豆包 SeedTTS 2.0 Skill

> 火山引擎豆包语音合成 2.0，支持 34 种音色、情绪控制、语音指令。

---

## 🎯 功能特性

- ✅ **34 种音色** - 中文/英文、男声/女声、通用/角色扮演
- ✅ **情绪控制** - 支持语音标签，如 `[温柔地] 你好呀`
- ✅ **多格式输出** - MP3/WAV，24kHz 高采样率
- ✅ **批量生成** - 一次调用生成多个音频
- ✅ **命令行工具** - 一行命令生成语音
- ✅ **Python SDK** - 简化调用，自动配置

---

## 📦 安装

```bash
clawhub install seedtts2
```

---

## 🔧 配置

### 1. 获取火山引擎凭证

1. 登录 [火山引擎控制台](https://console.volcengine.com/speech)
2. 进入「语音合成」→「应用管理」
3. 创建应用或选择已有应用
4. 获取 **APP ID** 和 **Access Token**

### 2. 配置凭证

**方式一：环境变量**（推荐）

```bash
export VOLCANO_APP_ID="你的 APP ID"
export VOLCANO_ACCESS_TOKEN="你的 Access Token"
export VOLCANO_RESOURCE_ID="seed-tts-2.0"  # 可选，默认值
```

**方式二：OpenClaw 配置**

在 `~/.openclaw/openclaw.json` 中添加：

```json
{
  "skills": {
    "entries": {
      "seedtts2": {
        "env": {
          "VOLCANO_APP_ID": "你的 APP ID",
          "VOLCANO_ACCESS_TOKEN": "你的 Access Token"
        }
      }
    }
  }
}
```

---

## 🚀 使用方法

### 命令行

```bash
# 基础用法
seedtts2 "你好，这是测试"

# 指定输出文件
seedtts2 "你好" -o test.mp3

# 指定音色
seedtts2 "你好" -s zh_male_ruyayichen_uranus_bigtts

# 合成后播放
seedtts2 "你好" -p

# 列出可用音色
seedtts2 --list
```

### Python SDK

```python
from tts_client import SeedTTS2

# 初始化（自动从环境变量读取配置）
tts = SeedTTS2()

# 基础合成
tts.say("你好，这是测试")

# 指定音色（JARVIS 官方音色）
tts.say("你好", speaker="zh_male_ruyayichen_uranus_bigtts")

# 保存到指定文件
tts.say("你好", output="test.mp3")

# 合成并播放
tts.say_and_play("你好")

# 批量生成
tts.batch_generate([
    {"text": "第一句", "speaker": "zh_male_ruyayichen_uranus_bigtts"},
    {"text": "第二句", "speaker": "zh_female_vv_uranus_bigtts"},
], output_dir="./output")
```

### 快捷函数

```python
from tts_client import say, say_and_play, batch_generate

# 一句话生成
say("你好")

# 生成并播放
say_and_play("你好")

# 批量生成
batch_generate(["第一句", "第二句"], output_dir="./output")
```

---

## 🎵 音色列表

### 推荐音色

| 音色 | Voice Type | 场景 |
|------|-----------|------|
| **儒雅逸辰 2.0** | `zh_male_ruyayichen_uranus_bigtts` | JARVIS 官方，成熟稳重 |
| **Vivi 2.0** | `zh_female_vv_uranus_bigtts` | 表现力强，情感丰富 |
| **甜美小源 2.0** | `zh_female_tianmeixiaoyuan_uranus_bigtts` | 甜美温柔，情感陪伴 |
| **云舟** | `zh_male_m191_uranus_bigtts` | 沉稳大气 |
| **Tim** | `en_male_tim_uranus_bigtts` | 标准美式英语 |
| **Dacey** | `en_female_dacey_uranus_bigtts` | 标准英式英语 |

### 完整音色库

运行以下命令查看完整音色列表：

```bash
seedtts2 --list
```

或参考文档：[seedtts2-voice-library.md](docs/seedtts2-voice-library.md)

---

## 🎭 语音指令

支持在文本中使用语音标签控制情绪和语气：

```text
【格式】[表情/心理/肢体动作] 台词

【示例】
[温柔地] 你好呀
[开心地] 太好啦！
[严肃地] 请注意，这是重要通知
[旁白，语调平静] 故事从这里开始
```

---

## 📁 目录结构

```
seedtts2/
├── SKILL.md              # 本文件
├── bin/
│   └── seedtts2          # 命令行工具
├── examples/
│   ├── basic_usage.py    # 基础示例
│   ├── batch_generate.py # 批量生成
│   └── emotion_control.py # 情绪控制
├── docs/
│   ├── voice-library.md  # 完整音色库
│   └── troubleshooting.md # 故障排查
└── tts_client.py         # Python SDK
```

---

## ⚠️ 故障排查

### 问题 1：缺少必要配置

**错误信息**：
```
ValueError: 缺少必要配置：APP_ID, ACCESS_TOKEN
```

**解决方案**：
- 检查环境变量是否设置：`echo $VOLCANO_APP_ID`
- 或检查 `openclaw.json` 配置是否正确

### 问题 2：认证失败（401）

**错误信息**：
```
请求失败：{"message": "Unauthorized"}
```

**解决方案**：
- 检查 Access Token 是否正确
- 确认 Token 格式为 `Bearer; {token}`（注意空格）
- 在火山引擎控制台确认应用状态

### 问题 3：音色不可用（403）

**错误信息**：
```
请求失败：{"message": "Forbidden"}
```

**解决方案**：
- 该音色可能需要单独开通
- 登录火山引擎控制台 → 「音色管理」
- 确认音色状态为"已开通"

### 问题 4：音频无法播放

**解决方案**：
- macOS：使用 `afplay` 播放
- Linux：安装 `aplay`（alsa-utils 包）
- Windows：使用默认播放器

---

## 📚 相关文档

- [部署手册](docs/volcano-tts2-deployment-guide.md) - 完整配置指南
- [音色库](docs/seedtts2-voice-library.md) - 34 种音色详情
- [复盘报告](docs/tts2-debug-retrospective.md) - 经验教训总结

---

## 🙏 致谢

- 火山引擎豆包团队提供强大的语音合成 API
- OpenClaw 社区提供 Skill 开发框架

---

## 📄 许可证

MIT License

---

**维护者**: JARVIS  
**最后更新**: 2026-03-24  
**版本**: 1.0.0
