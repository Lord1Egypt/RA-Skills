# **🚀 faster-whisper-local-stt**

**高性能本地音频转文本工具** 基于 **Faster-Whisper**（支持 large-v3 / turbo 等模型），专为 OpenClaw Skill 开发，同时也完美支持独立命令行（CLI）使用。支持单文件与**整个目录批量转录**，自动保留目录结构，支持输出 .txt 或结构化 .json 文件。

## **✨ 核心特性**

* **🎯 场景全覆盖**：支持单文件极速转录与目录批量处理（自动递归遍历子文件夹）。  
* **📦 模型自动化**：自动下载模型（如 \--model large-v3 首次运行自动从 Hugging Face 下载，并永久本地缓存）。  
* **📂 目录结构保持**：批量处理时完全保留原目录层级（输入/子文件夹/音频.wav → 输出/子文件夹/音频.txt）。  
* **📝 灵活输出格式**：  
  * \--output txt → 提取纯文本内容，适合阅读。  
  * \--output json → 严格格式 {"success": true, "text": "..."}，适合程序对接。  
* **⚡ 极致性能优化**：内置中文优先优化、VAD 静音检测与长音频智能分段。支持 GPU（int8\_float16）加速与 CPU 运行，运行完毕自动释放显存。  
* **🛡️ 隐私与安全**：完全本地离线运行（模型下载后无需联网），数据绝对安全。  
* **🧩 OpenClaw 原生集成**：无缝对接 env\_manager / ensure\_package / config，Agent 可直接调用。

## **📥 常用模型下载**

脚本支持通过 \--model 参数自动从 Hugging Face 下载。如果环境无法联网，请手动下载后通过 \--model\_path 指定目录。

| 模型规模 | 推荐场景 | Hugging Face 下载地址 |
| :---- | :---- | :---- |
| **Base** | 低配设备 / 追求极速 | [wangminrui2022/faster-whisper-base-ct2](https://huggingface.co/wangminrui2022/faster-whisper-base-ct2) |
| **Large-v3** | 高精度需求 / 会议转录 | [wangminrui2022/faster-whisper-large-v3-ct2](https://huggingface.co/wangminrui2022/faster-whisper-large-v3-ct2) |
| **Turbo** | 性能与精度的平衡点 | [deepdml/faster-whisper-large-v3-turbo-ct2](https://huggingface.co/deepdml/faster-whisper-large-v3-turbo-ct2) |

## **📁 项目结构**

faster-whisper-local-stt/  
├── scripts/  
│   └── transcribe.py          \# 主脚本（已集成所有核心功能）  
├── models/                    \# 自动下载的本地模型存放目录  
├── SKILL.md                   \# OpenClaw Skill Agent 提示词元数据  
├── requirements.txt           \# 依赖清单  
└── README.md                  \# 项目文档

## **🚀 快速安装**

### **方式一：作为 OpenClaw Skill（推荐）**

1. 将整个文件夹放入 OpenClaw 的技能目录：\~/.openclaw/skills/faster-whisper-local-stt/  
2. Agent 首次调用时会自动安装所需的依赖包并配置环境。

### **方式二：作为独立工具使用**

git clone \[https://github.com/wangminrui2022/faster-whisper-local-stt.git\](https://github.com/wangminrui2022/faster-whisper-local-stt.git)  
cd faster-whisper-local-stt  
pip install \-r requirements.txt

## **💻 使用指南**

执行以下命令前，请确保已进入项目根目录。

### **1\. 单文件转录**

处理单个音频，默认自动检测语言。

\# 使用简洁别名自动下载/加载模型  
python scripts/transcribe.py \--audio\_path "F:/TestOutput/test.wav" \--model large-v3-ct2

\# 使用完整的 HuggingFace 仓库名  
python scripts/transcribe.py \--audio\_path "F:/TestOutput/test.wav" \--model wangminrui2022/faster-whisper-large-v3-ct2

\# 使用已下载到本地的绝对路径模型（完全断网可用）  
python scripts/transcribe.py \--audio\_path "F:/TestOutput/test.wav" \--model\_path "D:/faster-whisper-large-v3-ct2"

\# 指定输出为纯文本格式  
python scripts/transcribe.py \--audio\_path "F:/TestOutput/test.wav" \--model large-v3-ct2 \--output text

\# 指定每句换行显示  
python scripts/transcribe.py \--audio\_path "F:/TestOutput/test.wav" \--model large-v3-ct2 \--output text \--separator "\n"

### **2\. 批量目录转录**

当 \--audio\_path 指向一个文件夹时，程序会自动找出所有音频文件并批量转录。

\# 默认输出：自动在源目录同级创建 \`原目录名\_transcripts\` 文件夹保存结果  
python scripts/transcribe.py \--audio\_path "F:/TestOutput" \--model large-v3-ct2

\# 自定义输出：通过 \--output\_dir 指定保存路径，内部会保持源文件的子目录结构  
python scripts/transcribe.py \--audio\_path "F:/TestOutput" \--output\_dir "F:/TestOutput/transcripts" \--model\_path "D:/models/large-v3-turbo"

## **⚙️ 核心参数对照表**

| 参数名 | 说明 | 示例 |
| :---- | :---- | :---- |
| \--audio\_path | **【必填】** 音频文件路径，或包含音频的文件夹路径。 | "F:/TestOutput/test.wav" |
| \--model | 模型名称或 HuggingFace 仓库名（首次需联网下载）。 | large-v3-ct2 |
| \--model\_path | 本地模型绝对路径（与 \--model 二选一，优先使用此项）。 | "D:/model-path" |
| \--output\_dir | 批量处理时指定结果存放路径，单文件处理时通常无需填写。 | "F:/TestOutput/transcripts" |
| \--output | 输出格式。可选 txt (纯文本) 或 json (结构化数据)。默认输出完整元数据。 | txt |
| \--separator | 句子间隔和换行符。可以使用"\n"为句子换行显示，默认句子用空格间隔。 | "\n" |

### **在 OpenClaw 聊天中**

你可以直接对你的 Agent 说：

帮我把这个音频转成文字 F:\命理学-音频-干声\猴哥说易\月支月令如何看一个人事业！_20260329_200421.wav，使用换行符号"\n"，保存到 F:\测试音频

语音转文本，这个文件夹 F:\命理学-音频-干声-切片，添加换行符"\n"，保存到 F:\命理学-音频-干声-切片-文本

转录会议录音 F:\命理学-音频-干声\猴哥说易\月支月令如何看一个人事业！_20260329_200421.wav 输出成 json

