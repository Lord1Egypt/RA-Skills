# 生产流程详解

## 完整 Pipeline

```
[输入] 小说原文
    │
    ▼
[阶段1] 故事线 (storyline.md)
    │  需要: models.text
    ▼
[阶段2] 大纲 (outline/outline-*.md)
    │  需要: models.text
    ▼
[阶段3] 资产提取 (assets/*.md, assets/data.json)
    │  需要: models.text
    ▼
[阶段4] 风格样张 (assets/style-sample.jpg)
    │  需要: models.image
    │  关键: 用户确认后才继续
    ▼
[阶段5] 资产生成 (assets/images/*)
    │  需要: models.image
    ▼
[阶段6] 剧本 (script/script-*.md)
    │  需要: models.text
    ▼
[阶段7] 分镜 (storyboard/storyboard-*.md)
    │  需要: models.text
    ▼
[阶段8] 分镜图 (storyboard/images/*)
    │  需要: models.image
    │  引用: style-sample.jpg, assets/images/*
    ▼
[阶段9] 视频 (video/ep*-*.mp4)
    │  需要: models.video
    ▼
[阶段10] 音频/字幕 (audio/*, subtitle/*.srt)
    │  需要: models.audio
    ▼
[阶段11] 后期合成 (final/episode*.mp4)
    │  需要: ffmpeg
    ▼
[输出] 成片
```

## 各阶段说明

### 阶段1: 故事线

**输入**: 小说原文
**输出**: `storyline.md`

包含:
- 主题定位
- 主线剧情
- 主要人物关系
- 情感基调

### 阶段2: 大纲

**输入**: 故事线
**输出**: `outline/outline-{ep}.md`

每集包含:
- 标题（8字内，含情绪爆点）
- 章节范围
- 核心矛盾
- 剧情主干（100-300字）
- 开场镜头
- 剧情节点 [起, 承, 转, 合]
- 情绪曲线
- 视觉重点
- 结尾悬念
- 经典台词
- 角色/场景/道具列表

### 阶段3: 资产提取

**输入**: 大纲
**输出**:
- `assets/characters.md`
- `assets/scenes.md`
- `assets/props.md`
- `assets/data.json`

提取三类资产，输出人工阅读版（Markdown）和程序兼容版（JSON）。

### 阶段4: 风格样张（关键质量控制点）

**输入**: `project.json` 中的 `artStyle`
**输出**: `assets/style-sample.jpg`

这是整个项目的视觉锚点。用户必须确认风格样张后，才能进入批量生成阶段。

### 阶段5: 资产生成

**输入**: `assets/data.json`
**输出**: `assets/images/*`

为每个角色生成四视图参考图（正面、侧面、背面、特写），为场景和道具生成单张参考图。

**角色一致性机制**:
- 使用相同 seed 生成四视图
- 记录 seed 到 `project.json`
- 后续生成复用 seed 和参考图

### 阶段6: 剧本

**输入**: 大纲
**输出**: `script/script-{ep}.md`

包含场景、对白、动作指示、音效等。

### 阶段7: 分镜

**输入**: 剧本
**输出**: `storyboard/storyboard-{ep}.md`

包含镜头描述、AI 生成提示词、出场角色、场景、运镜方式、建议时长。

### 阶段8: 分镜图

**输入**:
- 分镜文档
- 资产参考图
- 风格样张

**输出**: 宫格图 + 拆分后的单张镜头图

**强制引用**:
- 风格样张（确保风格统一）
- 角色参考图（确保角色一致）

### 阶段9: 视频

**输入**: 分镜图
**输出**: 视频片段

根据分镜中的时长和运镜参数调用视频 API。

### 阶段10: 音频/字幕

**输入**: 剧本
**输出**: 音频文件 + SRT 字幕

- 按角色分配音色
- 字粒度时间戳合并为句子级字幕

### 阶段11: 后期合成

**输入**:
- 视频片段
- 音频（可选）
- 字幕（可选）

**输出**: 最终成片

- 按片段拼接视频
- 混音（BGM + 配音 + 音效）
- 字幕烧录

## 质量控制节点

| 阶段 | 检查项 |
|------|--------|
| 大纲完成后 | 角色/场景/道具名称一致性 |
| 风格样张后 | 用户确认风格 |
| 分镜图生成后 | 黑图/异常图检测 |
| 视频生成后 | 片段完整性检查 |
| 最终成片前 | 全量一致性校验 |
