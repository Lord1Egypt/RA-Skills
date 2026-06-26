# VoxCPM中文视频配音

> **唯一使用VoxCPM开源模型的中文配音技能**

## 快速开始

```bash
# 1. 安装依赖
pip install torch openai-whisper soundfile scipy librosa requests

# 2. 克隆VoxCPM
git clone https://github.com/modelscope/VoxCPM.git

# 3. 配置
cp config.example.json config.json
# 编辑config.json，填入API密钥和路径

# 4. 运行
python scripts/dubbing.py your_video.mp4
```

## 特性

- 🎯 **VoxCPM独家** - 唯一集成VoxCPM的中文配音技能
- ✅ **生产验证** - 已在B站成功发布4个视频
- 🔄 **断点续传** - 中断后可继续
- 🔍 **硬字幕检测** - AI自动检测并覆盖
- 🎵 **智能BGM** - 自动循环、淡入淡出

## 文档

详见 [SKILL.md](./SKILL.md)

## 许可证

MIT License