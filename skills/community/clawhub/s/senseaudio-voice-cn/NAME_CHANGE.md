# 📝 技能更名说明

> **时间**: 2026-03-14  
> **原名**: senseaudio-tts  
> **新名**: senseaudio-voice

---

## 🎯 更名原因

**senseaudio-tts** 这个名字不准确，因为该技能实际上包含：
- ✅ **TTS** (Text-to-Speech) - 语音合成
- ✅ **ASR** (Automatic Speech Recognition) - 语音识别

原名只体现了 TTS 功能，忽略了 ASR 能力。

---

## ✨ 新名称优势

### senseaudio-voice

| 优势 | 说明 |
|------|------|
| **准确** | voice 体现完整语音能力（输入 + 输出） |
| **简洁** | 一个词概括所有语音功能 |
| **易记** | 简单好记，用户友好 |
| **扩展** | 未来添加其他语音功能也适用 |

---

## 📋 更新范围

### 技能内部
- ✅ SKILL.md - 技能名称和描述
- ✅ scripts/tts.py - 路径注释
- ✅ scripts/setup.sh - 安装脚本
- ✅ scripts/asr.py - ASR 脚本

### kids-points 引用
- ✅ skill.json - 依赖声明
- ✅ README.md - 使用说明
- ✅ DEPENDENCIES.md - 依赖文档
- ✅ SKILL.md - 技能说明
- ✅ META_SKILL.md - 元技能文档
- ✅ scripts/handler.js - 代码引用
- ✅ scripts/send-daily-report.sh - 定时任务

### 其他文档
- ✅ MEMORY.md - 工作区记忆
- ✅ NAME_CHANGE.md - 更名说明（本文档）

---

## 🔧 迁移指南

### 已安装用户

```bash
# 1. 删除旧技能
clawhub uninstall senseaudio-tts

# 2. 安装新技能
clawhub install senseaudio-voice

# 3. 验证安装
ls ~/.openclaw/agents/kids-study/workspace/skills/senseaudio-voice/
```

### 新用户

```bash
# 直接安装新技能
clawhub install senseaudio-voice
```

---

## 📊 功能对比

| 功能 | senseaudio-tts | senseaudio-voice |
|------|----------------|------------------|
| **TTS** | ✅ | ✅ |
| **ASR** | ✅ | ✅ |
| **名称准确性** | ⚠️ 不完整 | ✅ 完整 |
| **用户理解** | ⚠️ 可能误解 | ✅ 清晰明了 |

---

## 🎯 技能定位

### senseaudio-voice

**完整语音交互技能**，提供：

1. **TTS 语音合成**
   - 文字转语音
   - 多声音支持（童声、男声、女声）
   - WAV/MP3格式
   - 智能播放

2. **ASR 语音识别**
   - 语音转文字
   - 高精度识别
   - 多格式支持（OGG/WAV/MP3/M4A）
   - 深度理解模型

---

## 📝 版本说明

- **v2.0.0** - 更名为 senseaudio-voice
- **v1.x.x** - 原 senseaudio-tts 版本

---

## ✅ 检查清单

- [x] 技能目录重命名
- [x] SKILL.md 更新
- [x] 脚本文件更新
- [x] kids-points 引用更新
- [x] 文档引用更新
- [x] 配置文件更新
- [x] 创建更名说明文档

---

**更名完成！** 🎉

_senseaudio-voice - 完整语音交互能力_ 🎤
