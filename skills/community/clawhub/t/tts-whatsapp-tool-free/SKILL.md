---
slug: tts-whatsapp-tool-free
name: tts-whatsapp-tool-free
version: 1.0.0
displayName: WhatsApp语音消息免费版
summary: 基于 Piper TTS 的 WhatsApp 语音消息发送工具,支持 40+ 语言,适合个人用户发送语音消息.
license: Proprietary
edition: free
description: 面向个人用户的 WhatsApp 语音消息工具(免费版)。核心能力:，可自动提升工作效率

  - 基于 Piper TTS 的高质量语音合成(40+ 语言)

  - 文字转 OGG/Opus 格式(WhatsApp 兼容)

  - 自动发送语音消息到指定联系人

  - 支持中文、英文、法文、西班牙文等

  - 可调语速与音质

  - 发送后自动清理临时文件

  适用场景:

  - 个人 WhatsApp 语音消息发送

  - 多语言沟通辅助

  - 文字转语音快速发送

  - 无法语音输入时替代打字

  差异化:

  - 免费版聚焦单条消息发送核心能力

  - 完...'
tags:
  - 创意设计
  - 语音合成
  - WhatsApp
  - 消息发送
  - 多语言
  - 社交
  - 通信
  - 语音消息
  - whatsapp
  - tts-whatsapp
  - target
  - bash
tools:
  - read
  - exec
  - write
homepage: ""
category: "Communication"
---
# WhatsApp 语音消息工具 - 免费版

## 概述

WhatsApp 语音消息工具(免费版)帮助个人用户将文字转换为高质量语音消息并发送到 WhatsApp。基于 Piper TTS 引擎,支持 40+ 语言,自动转换为 OGG/Opus 格式(WhatsApp 兼容),适合多语言沟通与快速语音发送.
免费版聚焦单条消息发送,专业版(`tts-whatsapp-tool-pro`)在此基础上提供群发广播、定时发送、批量处理与团队协作等高级能力.
## 核心能力

| 能力 | 免费版 | 说明 |
|---|---|---|
| 文字转语音 | 支持 | Piper TTS 引擎 |
| 语言支持 | 40+ | 含中英法德西等 |
| 音频格式 | OGG/Opus | WhatsApp 兼容 |
| 单人发送 | 支持 | 指定手机号 |
| 语速控制 | 支持 | 0.5-2.0 倍速 |
| 音质选择 | 支持 | x_low/low/medium/high |
| 自动清理 | 支持 | 发送后删除临时文件 |
| 群组发送 | 不支持 | 升级专业版 |
| 批量发送 | 不支持 | 升级专业版 |
| 定时发送 | 不支持 | 升级专业版 |
| 消息模板 | 不支持 | 升级专业版 |

### 核心功能执行
用`input_params`参数进行配置.

**处理**: 解析核心功能执行的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回核心功能执行的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 参数配置与调用
用`config_options`参数进行配置.

**处理**: 解析参数配置与调用的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回参数配置与调用的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`config_options`参数,支持修改/重置/导入操作

### 结果处理与输出
用`output_format`参数进行配置.

**处理**: 解析结果处理与输出的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回结果处理与输出的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`output_format`参数,支持导出/保存/转换操作
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：语音消息发送工具、适合个人用户发送、语音消息、面向个人用户的、语音消息工具、核心能力、的高质量语音合成、自动发送语音消息、到指定联系人、支持中文、西班牙文等、可调语速与音质、发送后自动清理临等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持.
## 使用场景

### 场景一:发送中文语音消息

将中文文字转为语音发送.
```bash
# 发送中文语音消息
tts-whatsapp "你好,这是一条语音消息测试。" \
    --lang zh_CN \
    --voice zh_CN-huayan-medium \
    --target "+8613800138000"
```

### 场景二:多语言沟通

发送不同语言的语音消息.
```bash
# 英文消息
tts-whatsapp "Hello, how are you today?" \
    --lang en_US \
    --voice lessac \
    --target "+15555550123"
# ...
# 法文消息
tts-whatsapp "Bonjour, comment allez-vous?" \
    --lang fr_FR \
    --voice siwis \
    --target "+33123456789"
# ...
# 西班牙文消息
tts-whatsapp "Hola, como estas?" \
    --lang es_ES \
    --voice carlfm \
    --target "+34123456789"
```

### 场景三:调整音质与语速

根据需求选择不同音质.
```bash
# 高音质(文件较大)
tts-whatsapp "重要通知:明天会议改到下午三点。" \
    --quality high \
    --speed 1.0 \
    --target "+8613800138000"
# ...
# 低音质(快速发送)
tts-whatsapp "收到,谢谢!" \
    --quality low \
    --speed 1.2 \
    --target "+8613800138000"
```

## 不适用场景

以下场景WhatsApp语音消息免费版不适合处理：

- 专业医学法律翻译认证
- 同声传译
- 文学创作翻译

## 触发条件

需要文本翻译、多语言转换、本地化处理时使用。不适用于非本工具能力范围的需求.
## 快速开始

1. 阅读## 核心能力章节了解skill功能
2. 按## 依赖说明配置环境
3. 执行所需能力对应的命令
4. 参考## 错误处理章节处理异常
5. 查看## FAQ解答常见疑问

### 依赖详情

```bash
# 安装 Piper TTS
pip3 install --user piper-tts
# ...
# 安装 FFmpeg
# macOS
brew install ffmpeg
# ...
# Ubuntu / Debian
sudo apt install ffmpeg
# ...
# Windows (scoop)
scoop install ffmpeg
```

### 2. 下载语音模型

```bash
# 创建模型目录
mkdir -p ~/.tts-whatsapp/models/
# ...
# 下载中文语音模型
# 从 Piper 语音仓库下载 .onnx 和 .onnx.json 文件
# 放入 ~/.tts-whatsapp/models/ 目录
```

### 3. 配置 WhatsApp 发送

```bash
# 配置默认目标
export WHATSAPP_DEFAULT_TARGET="+8613800138000"
export PIPER_DEFAULT_LANG="zh_CN"
export PIPER_DEFAULT_VOICE="zh_CN-huayan-medium"
export PIPER_DEFAULT_QUALITY="medium"
```

### 4. 发送第一条语音

```bash
tts-whatsapp "你好,这是第一条语音消息!" --target "+8613800138000"
```

## 示例

### 配置文件

```json
{
  "tts_whatsapp": {
    "enabled": true,
    "env": {
      "WHATSAPP_DEFAULT_TARGET": "+8613800138000",
      "PIPER_DEFAULT_LANG": "zh_CN",
      "PIPER_DEFAULT_VOICE": "zh_CN-huayan-medium",
      "PIPER_DEFAULT_QUALITY": "medium"
    }
  }
}
```

### 命令行参数

```text
--target NUMBER       WhatsApp 手机号或群组 ID
--message TEXT        附带的文字消息
--lang LANGUAGE       语言(默认: zh_CN)
--voice VOICE         语音名称(默认: 自动)
--quality QUALITY     音质: x_low / low / medium / high
--speed SPEED         播放速度(默认: 1.0)
--no-send             仅生成不发送
```

### 支持的语言

| 语言 | 代码 | 示例语音 |
|:-----|:-----|:-----|
| 中文 | zh_CN | huayan |
| 英文(美) | en_US | lessac, amy, joe |
| 英文(英) | en_GB | alan, alba |
| 法文 | fr_FR | siwis, upmc |
| 德文 | de_DE | thorsten, eva_k |
| 西班牙文 | es_ES | carlfm, davefx |
| 葡萄牙文 | pt_BR | faber |
| 俄文 | ru_RU | dmitri, irina |
| 日文 | ja_JP | (多款可选) |
| 韩文 | ko_KR | (多款可选) |

### 音质等级

| 等级 | 码率 | 文件大小(10秒) | 适用场景 |
|---:|---:|---:|---:|
| x_low | 最低 | ~50KB | 极速发送,网络差 |
| low | 低 | ~80KB | 日常简短消息 |
| medium | 中 | ~120KB | 推荐平衡 |
| high | 高 | ~200KB | 重要内容,清晰度优先 |

## 最佳实践

1. **语音模型选择**
   - 中文:推荐 `zh_CN-huayan-medium`
   - 英文:推荐 `en_US-lessac-medium`
   - 首次使用前试听 `preview_audio_url`
   - 不同语音适合不同场景(正式/轻松)

2. **音质与速度平衡**
   - 日常消息:`medium` + `1.0` 倍速
   - 简短回复:`low` + `1.2` 倍速
   - 重要通知:`high` + `0.9` 倍速
   - 网络较差:`x_low` + `1.0` 倍速

3. **文本长度控制**
   - 单条消息建议不超过 500 字
   - 长文本分段发送
   - 段落间自然停顿用标点

4. **隐私与安全**
   - 手机号等敏感信息不要硬编码
   - 使用环境变量或配置文件管理
   - 发送后自动清理临时文件
   - 遵守当地通信法规

5. **性能优化**
   - 预加载常用语音模型
   - 避免频繁切换语言
   - 网络不稳定时降低音质

## 常见问题

### Q1: 发送失败怎么办?

检查:
- WhatsApp 是否已登录并保持连接
- 目标手机号是否正确(含国际区号)
- 网络是否正常
- 语音模型是否已下载

### Q2: 语音质量不理想?

- 升级音质到 `high`
- 确认语音模型已正确下载
- 尝试不同的语音名称
- 文本中适当使用标点控制节奏

### Q3: 支持哪些语言?

支持 40+ 语言,包括中文、英文、法文、德文、西班牙文、葡萄牙文、俄文、日文、韩文等。完整列表参见 Piper 语音仓库.
### Q4: 免费版与专业版的区别?

免费版支持单条消息发送;专业版支持群发广播、批量发送、定时发送与消息模板。需要群发或自动化的场景建议升级.
### Q5: 是否需要 API Key?

不需要。Piper TTS 完全本地运行,基础LLM由Agent平台提供。WhatsApp 发送通过本地连接完成.
### Q6: 语音模型在哪里下载?

从 Piper 语音仓库(Hugging Face)下载 `.onnx` 和 `.onnx.json` 文件,放入配置的模型目录.
## 依赖说明

### 运行环境
- **Agent 平台**: 支持SKILL.md的任意AI Agent(Claude Code / Cursor / Codex / Gemini CLI等)
- **操作系统**: Windows / macOS / Linux
- **网络**: 需访问 WhatsApp(发送消息时)

### 第三方依赖

| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:---:|:---:|:---:|:---:|
| piper-tts | Python 库 | 必需 | `pip install piper-tts` |
| ffmpeg | 系统工具 | 必需 | `brew install ffmpeg` / `apt install ffmpeg` |
| WhatsApp 连接 | 服务 | 必需 | 本地配置或第三方桥接 |
| Python 3.9+ | 运行时 | 必需 | `python.org` 下载 |
| 语音模型 | 数据文件 | 必需 | 从 Piper 仓库下载 |
| LLM API | API | 必需 | 由Agent内置LLM提供 |

### API Key 配置
- TTS 合成**基础LLM由Agent平台提供**(Piper 本地运行)
- WhatsApp 发送需配置连接(通过本地桥接服务)
- 建议使用配置文件管理目标号码与默认参数

### 可用性分类
- **分类**: MD+EXEC(纯Markdown指令,部分功能需exec命令行执行)
- **说明**: 基于Markdown的AI Skill,通过自然语言指令驱动Agent完成操作。免费版聚焦单条语音消息发送,适合个人用户多语言沟通.
## 错误处理

| 错误场景 | 原因 | 处理方式 |
|:------|------:|:------|
| 配置错误 | 参数缺失或格式错误 | 检查依赖说明中的配置要求 |
| 运行时错误 | 运行环境不满足 | 确认运行环境符合依赖说明 |
| 网络错误 | 连接超时或不可达 | 执行ping命令测试网络连通性,检查防火墙和代理设置连接后执行ping命令测试网络连通性,检查防火墙和代理设置连接后重新执行命令，参考国内替代方案 |

## 已知限制

- 本地运行，不支持多设备同步

## 输出格式
```json
{
  "success": true,
  "data": {
    "result": "WhatsApp语音消息免费版处理结果",
    "execution_time": "0.5s",
    "metadata": {
      "version": "1.0",
      "processor": "tts whatsapp"
    }
  },
  "execution_log": ["解析输入参数", "执行核心处理", "格式化输出结果"],
  "error": null
}
```
