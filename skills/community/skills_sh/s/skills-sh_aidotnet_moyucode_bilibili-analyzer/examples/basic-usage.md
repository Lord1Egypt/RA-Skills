# 基本使用示例

## 快速开始

```bash
cd skills/tools/bilibili-analyzer/scripts
python main.py "https://www.bilibili.com/video/BV1xx411c7mD"
```

## 常用场景

### 1. 分析教程视频（提取更多帧）

```bash
python main.py "https://www.bilibili.com/video/BV1xx411c7mD" \
    -i 15 \
    -m 100 \
    -f text,objects
```

### 2. 快速预览长视频

```bash
python main.py "https://www.bilibili.com/video/BV1xx411c7mD" \
    -i 120 \
    -m 20 \
    --no-scene-detection
```

### 3. 分析人物访谈

```bash
python main.py "https://www.bilibili.com/video/BV1xx411c7mD" \
    -i 30 \
    -f faces,text,scene
```

### 4. 高并行分析（快速完成）

```bash
python main.py "https://www.bilibili.com/video/BV1xx411c7mD" \
    -w 8 \
    -m 30
```

### 5. 指定输出目录

```bash
python main.py "https://www.bilibili.com/video/BV1xx411c7mD" \
    -o ./my-video-reports
```

### 6. 使用短链接

```bash
python main.py "https://b23.tv/xxxxx"
```

### 7. 详细日志模式（调试用）

```bash
python main.py "https://www.bilibili.com/video/BV1xx411c7mD" -v
```

### 8. 静默模式（只显示错误）

```bash
python main.py "https://www.bilibili.com/video/BV1xx411c7mD" -q
```

## 输出示例

分析完成后，输出目录结构：

```
./bilibili/视频标题/
├── report.md          # Markdown分析报告
├── frames/            # 关键帧图片
│   ├── frame_001_00-00-00.jpg
│   ├── frame_002_00-00-30.jpg
│   └── ...
├── analysis.log       # 执行日志
└── checkpoints/       # 检查点数据
```
