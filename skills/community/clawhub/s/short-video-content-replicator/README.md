# Short Video Content Replicator

**一键端到端短视频内容复制工作流** —— 专为 ClawHub / OpenClaw 设计的复合 Skill

输入一个抖音或 Bilibili 视频链接（或本地视频文件夹），自动按严格顺序完成 **6 步处理**，输出高质量干净干声 + 纠错后的带标点文本，适合快速复刻、二次创作、内容批量加工或 TTS 训练素材准备。

---

## ✨ 核心功能

- **一键复制**：从视频链接到最终文字，只需一条命令
- **严格 6 步工作流**：
  1. `link-resolver-engine` —— 下载最高画质视频（支持抖音/B站）
  2. `mp4-to-mp3-extractor` —— 批量提取 MP3 音频
  3. `purevocals-uvr-automator` —— 提取超干净干声（VR Architecture）
  4. `turbo-whisper-local-stt` —— 本地高速 Whisper 转录（large-v3-ct2，中文优先）
  5. `llm-text-correct` —— 中文文本纠错（pycorrector + MacBERT）
  6. `funasr-punctuation-restore` —— FunASR 标点符号恢复
- 支持**断点续跑**（从任意步骤开始）
- 支持**自定义输出目录**
- 完全本地化运行（隐私安全，支持 GPU 加速）

---

### **在 OpenClaw 聊天中**

你可以直接对你的 Agent 说：

帮我复制这个抖音视频的内容：https://v.douyin.com/M4M5uqTWCRE/

把这个B站短视频转成带标点的文字https://b23.tv/Os94Q14，输出到 "F:/test" 文件夹。

一键端到端处理这个视频

/short-video-content-replicator https://b23.tv/Os94Q14

## 📋 工作流示意图

```mermaid
flowchart TD
    A[视频URL 或 本地视频目录] --> B[Step 1: link-resolver-engine<br>下载视频]
    B --> C[Step 2: mp4-to-mp3-extractor<br>提取 MP3]
    C --> D[Step 3: purevocals-uvr-automator<br>人声分离 → 干净干声.wav]
    D --> E[Step 4: turbo-whisper-local-stt<br>转录为 .txt]
    E --> F[Step 5: llm-text-correct<br>文本纠错]
    F --> G[Step 6: funasr-punctuation-restore<br>标点恢复 → 最终文本]
    G --> H[输出目录: videos / mp3 / vocals / transcripts / corrected / final]