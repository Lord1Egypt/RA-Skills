# Video Note Maker - 视频转笔记工具

## 📁 文件结构

### 技能目录
```
video-note-maker/
├── video_note_maker.py   # 主程序
├── SKILL.md              # 技能说明文档
├── README.md             # 本文档
├── config.json           # 配置文件
└── scripts/
    ├── extract_audio.sh  # 提取音频脚本
    ├── split_audio.sh    # 分割音频脚本
    └── transcribe.py     # Whisper 转写脚本
```

### 输出目录结构（处理视频时自动创建）
```
原视频目录/
├── video1.mp4
├── video2.mp4
├── tmp/                   # 临时文件（按视频创建子文件夹）
│   ├── video1/
│   │   ├── audio.wav
│   │   ├── segment_000.wav
│   │   └── ...
│   └── video2/
│       └── ...
└── done/                  # 最终笔记目录
    ├── video1.md
    └── video2.md
```

---

## 🚀 快速开始

### 1. 安装依赖

```bash
# Ubuntu/Debian
sudo apt-get install ffmpeg

# Python 依赖
pip3 install openai-whisper

# 验证安装
ffmpeg -version
python3 -c "import whisper; print(whisper.__version__)"
```

### 2. 运行命令

```bash
# 单个视频
python video_note_maker.py /path/to/video.mp4

# 整个目录
python video_note_maker.py /path/to/videos/

# 自定义输出目录
python video_note_maker.py /path/to/videos/ --output /path/to/notes/
```

### 3. 查看结果

笔记会保存在 `notes/` 目录下，每个视频一个 Markdown 文件。

---

## ⚙️ 配置说明

编辑 `config.json` 修改参数：

```json
{
  "whisper_model": "small",
  "language": "zh",
  "segment_duration": 900,
  "audio_quality": {
    "sample_rate": 44100,
    "channels": 2,
    "format": "pcm_s16le"
  },
  "temp_dir": "tmp",
  "output_dir": "notes"
}
```

---

## 📊 处理流程

1. **扫描视频** - 查找所有视频文件
2. **提取音频** - 使用 ffmpeg 提取 WAV 格式
3. **分割音频** - 按 15 分钟一段分割
4. **逐段转写** - Whisper Small 模型转写
5. **拼接文字** - 按顺序合并所有段落
6. **大模型整理** - 生成结构化笔记（待接入）
7. **清理临时文件** - 删除中间文件

---

## 💡 使用建议

- **视频时长**：推荐 15-60 分钟
- **模型选择**：small 平衡速度和准确率
- **分割时长**：默认 15 分钟，可根据需要调整
- **大模型**：当前为示例输出，建议接入实际 API

---

## 📝 示例

```bash
# 处理 HCIP 视频
python video_note_maker.py /home/fangjinan/视频/HCIP/
```

输出目录结构：
```
HCIP/
├── 1 - OSPF 基础.mp4
├── 2 - OSPF 邻居建立.mp4
├── tmp/                   # 临时文件（按视频创建子文件夹）
│   ├── 1 - OSPF 基础/
│   │   ├── audio.wav
│   │   ├── segment_000.wav
│   │   └── segment_001.wav
│   └── 2 - OSPF 邻居建立/
│       └── ...
└── done/                  # 最终笔记
    ├── 1 - OSPF 基础.md
    └── 2 - OSPF 邻居建立.md
```

自定义输出目录：
```bash
python video_note_maker.py /home/fangjinan/视频/HCIP/ --output /home/fangjinan/视频/笔记/
```

---

## 🔧 故障排除

### 1. ffmpeg 未找到
```bash
sudo apt-get install ffmpeg
```

### 2. whisper 导入失败
```bash
pip3 install openai-whisper
```

### 3. 视频格式不支持
- 支持格式：mp4, mov, avi, mkv, flv, wmv
- 不支持：需要转换为上述格式

### 4. 内存不足
- 减少 `segment_duration` 分割时长
- 使用更小的模型（tiny/base）

---

## 📮 问题反馈

如有问题，请检查：
1. ffmpeg 和 whisper 是否正确安装
2. 视频文件路径是否正确
3. 输出目录是否有写入权限
4. 临时磁盘空间是否充足

---

**作者：** 虾妹  
**版本：** 1.0.0  
**更新日期：** 2026-04-09
