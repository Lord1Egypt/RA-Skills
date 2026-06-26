---
name: hair-cam-anno
description: 安防摄像头视频 VL 模型微调数据集标注工具。用于从安防摄像头视频中提取关键帧、分析视频内容、生成结构化标注（含环境/人物/行为/风险描述），并输出符合 dataset.jsonl 格式的微调训练数据。Use when 用户需要对安防摄像头视频进行数据标注、生成 VL 模型训练数据集、处理 /root/hair-cam 目录下的视频数据，或提及 "hair-cam"、"数据标注"、"视频标注"、"VL模型微调"。
---

# hair-cam-anno — 安防摄像头视频标注

对安防摄像头拍摄的视频进行帧提取、视觉分析、结构化标注，输出 `dataset.jsonl` 格式的 VL 模型微调数据集。

## 工作流程

### 第1步：提取视频帧

```bash
python3 <skill>/scripts/extract_frames.py \
  --data-dir <视频目录> \
  --output-dir <帧输出目录> \
  --fps 0.5 \
  --max-frames 4
```

- 从每个视频均匀提取 4 帧（每2秒一帧）
- 生成 `manifest.json` 记录每个视频的元信息和帧路径

### 第2步：逐视频分析标注

对每个视频：

1. **查看提取的帧**：用 `read` 工具读取帧图片（支持 jpg/png）
2. **从文件名推断信息**：文件名包含关键信息（如 `海尔摄像头-1男1女-坐-2` → 品牌=海尔摄像头, 1男1女, 行为=坐）
3. **生成标注 JSON**：根据帧画面内容 + 文件名信息，生成结构化标注

标注 JSON 结构：

```json
{
  "title": "场景标题",
  "subtitle": "场景副标题",
  "description": "详细描述（≥50字，含环境、人物外貌、行为姿态）",
  "labels": ["system_suggest_X", ...],
  "risk": {
    "level": "none|low|medium|high",
    "description": "风险描述"
  },
  "simple_description": "简练描述（≤20汉字）"
}
```

### 第3步：汇总生成 dataset.jsonl

1. 将所有标注结果收集到 `annotations.json`，格式：
```json
[
  {"video": "文件名.mp4", "annotation": { ...标注JSON... }},
  ...
]
```

2. 运行构建脚本：
```bash
python3 <skill>/scripts/build_jsonl.py \
  --annotations annotations.json \
  --video-dir <视频目录> \
  --output dataset.jsonl
```

3. 脚本会自动验证标注数据并生成 `dataset.jsonl`

## 关键参考

- **System prompt 模板**: `references/system-prompt.md`
- **标签范围**: `references/labels-reference.md`

## 标签选择规则

- 根据视频实际内容选择匹配标签
- 可多选，但不要选不匹配的标签
- 如果视频中有危险行为（儿童攀爬窗户、摔倒等），risk.level 应为 medium 或 high
- 文件名中的信息（人数、行为）必须与标注一致
