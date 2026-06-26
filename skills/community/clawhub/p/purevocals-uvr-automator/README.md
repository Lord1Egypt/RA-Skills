# **🎙️ PureVocals UVR Automator**

**高性能本地干声提取工具** 基于 **UVR (Ultimate Vocal Remover)** 核心算法，利用 audio-separator 实现自动化的人声与伴奏分离。专为 OpenClaw 开发，支持智能 GPU 加速检测，能够从单音频或整个目录中提取极度干净的人声（Vocals）。

## **✨ 核心特性**

* **🎤 极致干声提取**：采用 Kim\_Vocal\_2 等顶级 UVR 模型，提取结果几乎无伴奏残留。  
* **⚡ 智能硬件加速**：自动检测环境。有 GPU 时自动调用 CUDA 加速，无 GPU 时平滑切换至 CPU 模式。  
* **📂 批量与结构保持**：支持处理整个文件夹，并完美保留原始目录层级结构。  
* **🧪 预览模式 (Sample Mode)**：支持 \--sample\_mode 参数，仅处理音频前 30 秒，方便快速测试模型效果。  
* **🛠️ 自动化环境管理**：内置 venv 自动创建与依赖隔离，免去繁琐的库安装过程。  
* **🧹 智能维护**：自动清理临时文件，日志滚动更新（仅保留最近 3 天），保持系统整洁。

## **📥 推荐模型说明**

脚本支持自动下载模型。如遇网络问题，可手动下载并放入 models/ 目录：

| 模型文件名 | 推荐场景 | 特点 |
| :---- | :---- | :---- |
| **Kim\_Vocal\_2.onnx** | **首选推荐** | 速度极快，且干声提取效果极其干净。 |
| **UVR\_MDXNET\_KARA\_2.onnx** | 批量/快速处理 | 极致的推理速度，适合大规模音频预处理。 |
| **6\_HP-Karaoke-UVR.pth** | 高质量卡拉OK | 针对卡拉OK场景优化的经典高质量模型。 |

## **🚀 快速开始**

### **方式一：作为 OpenClaw Skill (推荐)**

1. 将文件夹放入 \~/.openclaw/skills/purevocals-uvr-automator/。  
2. 在对话框中告诉 Agent：“帮我把 F:/Music 里的歌提取一下干声”。

### **方式二：独立命令行使用**

\# 1\. 基础用法：处理整个目录  
python scripts/purevocals.py "F:/InputAudio" "F:/OutputVocals"

\# 2\. 指定高性能模型 \+ 处理单个文件  
python scripts/purevocals.py "F:/test.mp3" "F:/Output" \--model "6\_HP-Karaoke-UVR.pth"

\# 3\. 快速预览模式（仅处理前30秒）  
python scripts/purevocals.py "F:/Input" "F:/Output" \--sample\_mode

## **⚙️ 参数对照表**

| 参数名 | 说明 | 默认值 |
| :---- | :---- | :---- |
| input | **【必填】** 输入音频文件或目录路径。 | \- |
| output\_dir | **【必填】** 提取后的干声存放路径。 | \- |
| \--model | 使用的模型文件名。 | Kim\_Vocal\_2.onnx |
| \--sample\_mode | 开启后仅处理音频前 30 秒，用于效果预览。 | False |
| \--aggression | VR 算法强度（1-100）。 | 10 |
| \--window\_size | VR 窗口大小（常见 320, 512, 1024）。 | 320 |

### **在 OpenClaw 聊天中**

你可以直接对你的 Agent 说：

“帮我把"F:\命理学-音频\猴哥说易\月支月令如何看一个人事业！.mp3"这首歌的伴奏去掉，只留干声”

“批量把"F:\命理学-音频"文件夹里的所有 mp3 提取纯人声，保存到"F:\命理学-音频-干声"目录，模型使用"6_HP-Karaoke-UVR.pth"”

“做翻唱需要干净的清唱素材，请处理"F:\命理学-音频" 目录”

“卡拉OK 模式分离"F:\命理学-音频"这几个音频的人声”