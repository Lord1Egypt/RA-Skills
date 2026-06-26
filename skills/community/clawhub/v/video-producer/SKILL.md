---
name: video-producer
description: 短视频一键生成技能 v2.2。调用video-director进行画面规划，然后生成AI素材、TTS配音、视频渲染，输出完整MP4。
version: 2.2.0
tags: [video, production, tts, image-generation, automation, storyboard]
---

# Video Producer - 短视频一键生成技能 v2.2

## 核心能力

1. **画面规划** - 调用video-director生成分镜表（含素材路径）
2. **AI素材生成** - 根据文案关键词智能匹配素材
3. **TTS配音** - 每场景独立配音
4. **视频渲染** - Remotion + AI素材动画
5. **音视频合成** - 最终MP4输出

---

## 技能协作

本技能与 **video-director** 协作完成视频生成：

```
用户输入
   ↓
video-producer (协调者)
   ↓
调用 video-director (画面规划专家)
   ↓
生成分镜表 (JSON格式)
   ↓
video-producer 继续执行
   ↓
AI生图 → TTS配音 → 视频渲染 → 合成输出
```

### 协作优势

- **职责分离**：video-director专注画面设计，video-producer专注执行
- **独立使用**：video-director可单独用于画面规划
- **灵活调整**：用户可手动修改分镜表后再生成视频
- **易于维护**：设计规则和执行逻辑分离更新

---

## 画面设计方案格式

```markdown
# 「主题」画面设计方案

**总时长：** 10秒

| 场景 | 时间 | 类型 | 口播 | 素材 |
|:----:|------|------|------|------|
| 0 | 0-2s | 开场 | 主题... | 科技背景 |
| 1 | 2-7s | 核心观点 | 口播... | AI, 工作 |

---

## 场景1：标题

**时间：** 2s - 7s (5秒)
**口播：** 完整口播文案

### 画面设计

```
[背景] 科技背景 - fadeIn 0-30帧
[Emoji] 🤖 - popIn 15-30帧
[文字] "主标题" - fadeSlideUp 30-70帧
```

### 素材清单

| 元素 | 类型 | Prompt | 尺寸 | 保存路径 |
|------|------|--------|------|----------|
| 科技背景 | 背景 | 抽象科技背景... | 9:16 | s00_科技背景.png |
| AI | 素材 | AI机器人头像... | 1:1 | s01_AI.png |
```

---

## 名词 → 素材 映射表

| 关键词 | 素材描述 |
|--------|---------|
| AI/机器人 | 逼真的AI机器人头像 |
| 数据/录入 | 数据流动画 |
| 设计/创意 | 设计师工作场景 |
| 程序员/代码 | 编程工作场景 |
| 赚钱/收入 | 金币增长图表 |
| 时间/倒计时 | 沙漏时钟 |
| 技能/升级 | 技能树图标 |
| 取代/替代 | 人类vsAI对比图 |
| 裁员 | 空荡办公室 |
| 实习生 | 年轻人使用AI |

---

## 工作流

```
Step 1: 生成画面设计方案
        ↓
Step 2: AI生成素材 (按filename保存)
        ↓
Step 3: TTS配音
        ↓
Step 4: 生成视频代码 (按filename引用素材)
        ↓
Step 5: 渲染 + 合并
```

---

## 输出文件

```
test-video/
├── storyboard.md      # 画面设计方案（含素材路径）
├── materials/         # AI素材
│   ├── s00_科技背景.png
│   ├── s01_AI.png
│   └── ...
├── audio/            # TTS配音
├── src/Video.js     # 视频代码
└── out/final.mp4    # 最终视频
```

---

## 素材路径使用

生成的视频代码会自动引用素材路径：

```javascript
import img0_科技背景 from 'materials/s00_科技背景.png';
import img1_AI from 'materials/s01_AI.png';

// 在场景中使用
<img src={img0_科技背景} style={{ position: 'absolute', ... }} />
```

---

## 使用方式

```bash
node produce.js "视频主题" '[{"text":"口播","emoji":"💡","title":"标题"}]'
```

---

## v2.1.1 更新 (修复)

### Bug 修复
- TTS生成添加重试逻辑（最多3次）
- 添加文件验证：确保音频文件大小>1KB
- 添加缺失文件检查和警告

### 修复的问题
- 场景1音频(s1.mp3)缺失导致只有一句配音
- TTS失败时静默继续的问题

