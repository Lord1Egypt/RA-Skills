# xiaomi-tts-chapters

将章节文件（支持 .md 和 .txt）批量转换为有声小说音频，使用小米MiMo TTS API。

## 功能特点

- 批量处理章节文件（支持 Markdown 和纯文本）
- 长文本自动分段处理
- 支持多种音色和语音风格
- 断点续传（跳过已存在的文件）
- 输出MP3格式音频

## 前置条件

- Python 3.8+
- ffmpeg（用于音频合并）
- 小米MiMo API密钥

## 安装

```bash
pip install -r scripts/requirements.txt
brew install ffmpeg  # macOS
```

## 使用

```bash
# 使用run.sh（自动处理虚拟环境）
./scripts/run.sh -a YOUR_API_KEY -c /path/to/chapters

# 直接使用Python
python scripts/synthesize.py --api-key YOUR_KEY --chapters-dir /path/to/chapters
```

### 参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--api-key` | API密钥（必需） | - |
| `--chapters-dir` | 章节目录（必需） | - |
| `--output-dir` | 输出目录 | `.` |
| `--voice` | 音色 | `mimo_default` |
| `--style` | 风格标签 | 无 |
| `--start` / `--end` | 章节范围 | 全部 |

### 音色

- `mimo_default` - 默认音色
- `default_zh` - 中文女声
- `default_en` - 英文女声

### 风格

情绪：`开心`、`悲伤`、`生气`、`温柔`
方言：`东北话`、`四川话`、`河南话`、`粤语`

## 项目结构

```
├── SKILL.md              # OpenCode技能定义
└── scripts/
    ├── base_tts.py       # TTS基类（通用逻辑）
    ├── mimo_tts.py       # 小米MiMo TTS实现
    ├── synthesize.py     # 主程序入口
    ├── run.sh            # 快速启动脚本
    └── requirements.txt  # Python依赖
```

### 扩展新TTS厂商

继承 `BaseTTS` 基类，实现 `_synthesize_segment` 方法即可：

```python
from base_tts import BaseTTS

class NewTTS(BaseTTS):
    def _synthesize_segment(self, text, output_path, style=None):
        # 实现具体的TTS API调用
        pass
```

## 支持的文件格式

- `.md` - Markdown 格式（自动清理标记，提取纯文本）
- `.txt` - 纯文本格式（直接使用原文）

文件按数字前缀排序（如 `01-初遇.md`、`02-重逢.txt`）。

## 作为OpenCode Skill使用

将本项目复制到 `~/.opencode/skills/` 目录即可作为技能使用。

触发词：`生成有声小说`、`把小说转成音频`、`TTS合成`、`文字转语音`

## 许可证

MIT
