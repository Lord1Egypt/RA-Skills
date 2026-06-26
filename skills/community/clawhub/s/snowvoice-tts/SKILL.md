---
name: snowvoice-tts
version: 1.0.2
description: >
  本地中文语音合成工具，基于 Qwen3-TTS。当用户需要将文字转换为语音、克隆声音、
  设计新音色或生成对话配音时触发。支持自然语言直接调用 snowvoice CLI 生成音频。
  Keywords: TTS, 语音合成, 文字转语音, 声音克隆, 音色设计, 配音, snowvoice, 语音生成.
url: https://github.com/webkubor/snowvoice-studio
---

# SnowVoice TTS

本地中文语音合成 Skill，基于 [SnowVoice Studio (Qwen3-TTS)](https://github.com/webkubor/snowvoice-studio)。

## 触发条件

- "把这段话转成语音" / "用小烛的声音说你好"
- "克隆这个声音" / "设计一个温柔的女声"
- "生成一段配音" / "帮我朗读这段文字"

## 环境初始化

**首次使用前，必须确保 SnowVoice Studio 已安装。** Agent 应自动检测并引导安装。

### 检查环境
```bash
python3 scripts/init.py status
```

### 一键安装（推荐）
```bash
python3 scripts/init.py setup
```
这会自动完成：git clone → venv 创建 → 依赖安装 → 模型下载（约 3GB）

### 分步安装
```bash
python3 scripts/init.py install          # 仅安装软件
python3 scripts/init.py download-model Base-1.7B          # 下载克隆模型
python3 scripts/init.py download-model VoiceDesign-1.7B   # 下载设计模型
```

### 安装路径
默认安装到 `~/.snowvoice-studio`。如果开发者路径 `~/Desktop/personal/tts` 存在也会被识别。

## 执行流程

1. **检查环境**：确认 snowvoice 可用（自动发现路径）
2. **识别意图**：判断克隆/设计/列表
3. **提取参数**：文字内容 + 音色（自然语言解析）
4. **构建并执行命令**：`python -m cli.app clone/design <args>`（在 snowvoice 项目目录下）
5. **返回结果**：音频文件完整路径

## 核心命令

### 克隆（最常用）
```bash
# 在 snowvoice 项目目录下执行
python -m cli.app clone <persona_key> "要合成的文字"
python -m cli.app clone <persona_key> "文字" --tone "温柔" --emotion "Happy"
```

### 音色设计
```bash
python -m cli.app design <voice_name> "建模短句" --tone "描述"
```

### 音色列表
```bash
python -m cli.app voice list
```

## 音色速查

| 简称 | persona_key | 说明 |
|------|-------------|------|
| 顾栖月 | gu_qiyue | 默认音色 |
| 小烛 | candy | 小烛原版 |
| 小烛傲娇 | candy_cool | 傲娇大小姐 |
| 小烛腹黑 | candy_mischievous | 腹黑小恶魔 |
| 王爷沉稳 | 王爷-儒武沉稳 | 儒武风格 |
| 王爷冷峻 | 王爷-冷峻锋压 | 冷峻风格 |
| 星栀 | 星栀-暧昧撩人 | AI女友 |
| 夜棠 | 夜棠-午夜耳语 | AI女友 |
| 朝朝 | 朝朝-元气阳光 | AI女友 |
| 宁观尘 | ning_guanchen | 男声 |
| 江湖老人 | jianghu_laoren | 老年男声 |
| 搞笑男 | zhou_xingchi | 港式无厘头 |

完整列表运行 `snowvoice voice list` 查看。自然语言映射见 `scripts/tts_skill.py` 的 PERSONA_MAP。

## 注意事项

1. **首次使用必须初始化**：`python3 scripts/init.py setup`
2. **模型下载约 3GB**：首次可能需要 10-30 分钟
3. **仅支持 macOS Apple Silicon**（MPS 加速）
4. **执行超时**：合成一条语音约 10-30 秒，已设 5 分钟超时
5. **输出路径**：默认在 snowvoice 项目的 `out/` 目录
