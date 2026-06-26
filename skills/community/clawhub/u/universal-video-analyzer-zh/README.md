# 🎬 多模态视频分析器 (doubao-video-analyzer)

使用多模态大模型自动分析视频内容，支持画面识别和语音转文字，生成结构化中文报告。支持豆包、智谱、通义千问等多种模型，用户自行配置 API Key。

## ✨ 功能特点

- **双轨分析**：同时提取视频关键帧画面 + 语音转文字，融合生成完整内容总结
- **模型无关**：通过环境变量配置，支持任意兼容 OpenAI 格式的多模态模型 API
- **结构化输出**：自动识别场景、人物、核心信息、视频亮点等维度
- **国内友好**：支持豆包、智谱、通义千问等国内模型，无需翻墙
- **零门槛使用**：在微信中直接发送视频，自动触发分析，无需手动输入命令
- **容错完善**：ffmpeg 错误检查、API 超时保护、跨平台路径兼容

## 📦 安装

### 1. 克隆仓库
```bash
git clone https://github.com/lantianbaicai/doubao-video-analyzer.git
cd doubao-video-analyzer
```

### 2. 安装依赖
```bash
# PyTorch（CPU 版即可，有 GPU 可参考 PyTorch 官网安装 CUDA 版）
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

# 其他依赖
pip install requests openai-whisper

# 可选：支持 .env 文件管理配置
pip install python-dotenv
```

### 3. 安装 ffmpeg
- **Windows**: `winget install Gyan.FFmpeg` 或从 [ffmpeg.org](https://ffmpeg.org/download.html) 下载
- **macOS**: `brew install ffmpeg`
- **Linux**: `sudo apt install ffmpeg`

## ⚙️ 配置

### 方式一：临时环境变量（当前终端有效）
```bash
# Windows PowerShell
$env:VIDEO_ANALYZER_API_KEY="你的API密钥"
$env:VIDEO_ANALYZER_MODEL="doubao-seed-2-0-pro-260215"

# Linux/macOS
export VIDEO_ANALYZER_API_KEY="你的API密钥"
export VIDEO_ANALYZER_MODEL="doubao-seed-2-0-pro-260215"
```

### 方式二：永久环境变量（推荐）
**Windows（管理员 PowerShell）**：
```powershell
[Environment]::SetEnvironmentVariable("VIDEO_ANALYZER_API_KEY", "你的API密钥", "User")
[Environment]::SetEnvironmentVariable("VIDEO_ANALYZER_MODEL", "doubao-seed-2-0-pro-260215", "User")
[Environment]::SetEnvironmentVariable("VIDEO_ANALYZER_BASE_URL", "https://ark.cn-beijing.volces.com/api/v3", "User")
```
设置后重启终端即可生效。

**Linux/macOS**：追加到 `~/.bashrc` 或 `~/.zshrc`
```bash
echo 'export VIDEO_ANALYZER_API_KEY="你的API密钥"' >> ~/.bashrc
echo 'export VIDEO_ANALYZER_MODEL="doubao-seed-2-0-pro-260215"' >> ~/.bashrc
source ~/.bashrc
```

### 方式三：.env 文件（最方便）
在技能目录下创建 `.env` 文件：
```
VIDEO_ANALYZER_API_KEY=你的API密钥
VIDEO_ANALYZER_MODEL=doubao-seed-2-0-pro-260215
VIDEO_ANALYZER_BASE_URL=https://ark.cn-beijing.volces.com/api/v3
```

## 🚀 支持的多模态模型

| 模型提供商 | MODEL 值 | BASE_URL | API Key 申请 |
|-----------|---------|----------|-------------|
| 豆包 | `doubao-seed-2-0-pro-260215` | `https://ark.cn-beijing.volces.com/api/v3` | [火山引擎](https://www.volcengine.com/) |
| 智谱 GLM-4V | `glm-4v-plus` | `https://open.bigmodel.cn/api/paas/v4` | [智谱AI](https://open.bigmodel.cn/) |
| 通义千问 VL | `qwen-vl-plus` | `https://dashscope.aliyuncs.com/compatible-mode/v1` | [阿里云](https://dashscope.console.aliyun.com/) |

> 所有模型均兼容 OpenAI `/chat/completions` 接口格式

## 📖 使用方法

### 方式一：OpenClaw 技能（推荐）
1. 将技能文件夹放入 OpenClaw 的 `skills` 目录
2. **在微信中直接发送视频文件**，自动触发分析并返回结果

### 方式二：命令行
```bash
python doubao_video_analyzer.py "视频文件路径.mp4"
```

## 📊 分析示例

### 输入
发送一个产品介绍视频

### 输出
```
### 视频主题、内容
这是一个科技类产品介绍视频，展示GitHub开源项目InkOS...

### 核心信息、关键要点
1. 项目精准定位：面向内容创作者的AI写作工作台
2. 核心功能细节：内置5套创作模板、多模态生成...

### 视频对应项目的核心优势
1. 产品定位差异明显，面向商业级全流程创作
2. 信息透明度高，直接从开源页面真实展示
```

## 🔧 故障排查

| 问题 | 解决方案 |
|------|---------|
| `ffmpeg: command not found` | 安装 ffmpeg 并加入系统 PATH |
| `❌ 请设置环境变量 VIDEO_ANALYZER_API_KEY` | 按上文配置环境变量或创建 `.env` 文件 |
| `❌ 视频文件不存在` | 检查路径是否正确，路径含空格请用引号包裹 |
| `API 请求超时` | 检查网络或模型响应速度，大视频可能需要更长时间 |
| `ModuleNotFoundError: No module named 'torch'` | 安装 PyTorch：`pip install torch` |
| 分析结果不准确 | 尝试切换其他模型（智谱/通义），或调整 prompt |

## 📝 技能文件结构

```
doubao-video-analyzer/
├── doubao_video_analyzer.py   # 主分析脚本
├── SKILL.md                   # OpenClaw 技能定义
├── README.md                  # 本文档
├── references/
│   └── config_example.md      # 多模型配置示例
└── .env.example               # 环境变量模板（复制为 .env 使用）
```

## 💡 高级用法

### 批量分析视频
```python
import os
import subprocess

video_dir = "待分析视频/"
for video in os.listdir(video_dir):
    if video.endswith('.mp4'):
        subprocess.run(["python", "doubao_video_analyzer.py", os.path.join(video_dir, video)])
```

### 自定义分析维度
修改脚本中的 prompt 部分，可以调整输出格式，例如：
- 只分析画面内容
- 只提取语音文字
- 按营销/技术/教育等角度分析

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！如果你有更好的分析 prompt 或者支持更多模型的方案，非常欢迎贡献。

## 📄 许可证

MIT License

## 🎯 核心使用场景

**最简单的方式**：在微信中直接发送视频文件给配置了 OpenClaw 的账号，即可自动分析视频内容并返回结构化报告。

## 💬 反馈与支持

如有问题或建议，欢迎通过以下方式联系：
- GitHub Issues
- 微信：[你的微信号]
