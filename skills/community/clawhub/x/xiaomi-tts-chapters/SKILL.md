---
name: xiaomi-tts-chapters
description: 将章节文件（支持 .md 和 .txt）转换为有声小说音频，使用小米MiMo TTS API。支持批量处理、长文本自动分段、多种音色和风格。当用户要求"生成有声小说"、"把小说转成音频"、"TTS合成"、"文字转语音"、"章节转音频"时触发。
---

# 小米TTS有声小说合成

将小说章节文件（支持 .md 和 .txt 格式）批量转换为MP3音频文件。

## 前置条件

1. 安装依赖：`pip install openai>=1.0.0`
2. 安装ffmpeg（用于音频合并）：`brew install ffmpeg`
3. 获取小米MiMo API密钥：访问 [小米MiMo Token Plan](https://mimo.mi.com/token-plan)

## 快速使用

```bash
# 设置环境变量（推荐）
export MIMO_API_KEY="your_api_key"

# 合成单个章节
python scripts/synthesize.py --chapters-dir /path/to/chapters

# 使用run.sh（自动处理虚拟环境）
./scripts/run.sh -c /path/to/chapters

# 也可以直接指定API密钥
python scripts/synthesize.py --api-key YOUR_KEY --chapters-dir /path/to/chapters
```

## API密钥获取

API密钥按以下优先级查找：
1. 命令行参数 `--api-key` 或 `-a`
2. 环境变量 `MIMO_API_KEY`
3. 交互式提示用户输入

获取密钥：访问 [小米MiMo Token Plan](https://mimo.mi.com/token-plan)

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--api-key` | API密钥（可选，优先级最高） | 环境变量或交互输入 |
| `--chapters-dir` | 章节目录（必需） | - |
| `--output-dir` | 输出目录 | `.` |
| `--voice` | 音色 | `mimo_default` |
| `--style` | 风格标签 | 无 |
| `--start` / `--end` | 章节范围 | 全部 |
| `--delay` | 请求间隔秒数 | `1.0` |

## 可用音色

| 音色 | voice参数 | 说明 |
|------|-----------|------|
| MiMo默认 | `mimo_default` | 默认音色 |
| 冰糖 | `冰糖` | 中文女声 |
| 茉莉 | `茉莉` | 中文女声 |
| 苏打 | `苏打` | 中文女声 |
| 白桦 | `白桦` | 中文女声 |
| Mia | `Mia` | 英文女声 |
| Chloe | `Chloe` | 英文女声 |
| Milo | `Milo` | 英文男声 |
| Dean | `Dean` | 英文男声 |

## 可用风格

情绪：`开心`、`悲伤`、`生气`、`温柔`
语速：`变快`、`变慢`
方言：`东北话`、`四川话`、`河南话`、`粤语`
特殊：`唱歌`、`悄悄话`、`夹子音`

## 工作流程

1. 扫描章节目录中的 `.md` 和 `.txt` 文件，按数字前缀排序
2. 清理格式：`.md` 文件自动去除 Markdown 标记，`.txt` 文件直接使用原文
3. 长文本自动分段（每段约2000 tokens）
4. 逐段调用TTS API合成
5. 使用ffmpeg合并分段音频
6. 输出 `{章节名}.mp3` 文件

## 注意事项

- 已存在的音频文件会自动跳过（断点续传）
- 单次合成建议不超过500字，长章节自动处理
- API可能产生费用，请查看官方定价
