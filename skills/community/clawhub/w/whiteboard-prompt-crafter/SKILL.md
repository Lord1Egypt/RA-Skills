---
name: whiteboard-prompt-crafter
version: 1.0.0
description: >
  将用户的简短关键词扩展为精美的白板插图提示词，并调用 image_synthesize 生成图片。
  触发场景：用户说"生成白板图"、"做个白板插图"、"这种风格的图怎么做"、
  "帮我画一个XX的白板图"，或上传参考图要求生成类似风格。
  核心特点：生成的图片只有白板本身，无背景，白板占满画面。
---

# 白板插图提示词生成器

## 工作流

1. 理解用户意图 → 提取主题、步骤、关键词
2. 构建结构化英文提示词（核心改进：无背景白板）
3. 调用 image_synthesize 生成图片
4. 发给用户图片 + 提示词文本

## 白板风格核心提示词模板

```
[CLOSE-UP WHITEBOARD - NO BACKGROUND]
Close-up of a whiteboard, tilted slightly. [FRAME DETAILS] visible at edges.
White whiteboard surface fills the entire frame.
Hand-drawn style text and icons on white surface, realistic marker strokes with slight ink bleed.

[TITLE SECTION]
Top: large blue handwritten title '[中文标题]'
Below title: thick black wavy divider line

[MAIN CONTENT - 根据用户内容填入]

[ACCESSORIES]
Bottom right corner: small eraser and [N] markers (blue, black, red) lying on whiteboard surface

[CROPPING - 必须加入]
Clean white surface, no background visible, tight crop, flat laid on table or wall-mounted.
Realistic marker texture, slight shadow under accessories.
```

## 框架细节（FRAME DETAILS）

| 场景 | 提示词片段 |
|------|---------|
| 完整金属框 | Silver-grey metallic frame visible at edges |
| 简约无边 | Frameless whiteboard, clean white border only |
| 墙壁挂式 | Whiteboard mounted directly on wall, no tray |
| 桌上平放 | Whiteboard laid flat on wooden desk, slight top-down angle |

## 构图类型模板

### 类型A：卡片网格型（冥想/习惯/好处类）

```text
[数量]x2 grid layout of benefit cards, each with hand-drawn icon and Chinese text label:
Row 1: [图标] '[关键词1]' | [图标] '[关键词2]' | [图标] '[关键词3]'
Row 2: [图标] '[关键词4]' | [图标] '[关键词5]' | [图标] '[关键词6]'

Cards connected by dotted arrows to central [主题图标/mascot/figure]

Bottom left: yellow sticky note '[便利贴提示]'
Bottom right: bold red handwritten text '[底部强调金句/数据]'
```

### 类型B：时间线型（24小时/阶段类）

```text
Timeline shows [N] steps connected by black arrows:
- [时间] [步骤中文] - [图标英文描述]
- [时间] [步骤中文] - [图标英文描述]
[依此类推...]

Bottom: bold red handwritten Chinese text: '[底部金句]'
```

### 类型C：泳道流程型（多角色/泳道类）

```text
[N] horizontal swim lanes:
Lane [N] label in red marker: [泳道名]
  → [步骤N]: [图标] [中文描述]
[虚线箭头连接跨泳道步骤]

Bottom: blue sticky note '[关键结论]'
```

### 类型D：人物弧线型（成长/路径类）

```text
Horizontal curved path from left to right with [N] waypoints:

Waypoint [N] ([阶段名]):
  [图标] - [中文描述]
  [装饰: speech bubble / arrow / star annotation]

Final destination: [终极目标图标] '[终极目标中文]'

Bottom: red marker key lesson: '[一句话核心领悟]'
```

## 图标映射（常用）

| 含义 | 英文图标描述 |
|------|------------|
| 冥想/禅定 | stick figure sitting cross-legged with closed eyes, aura circles |
| 大脑/思维 | brain with calm wave pattern |
| 心脏/健康 | heart with pulse line |
| 专注/上升 | upward trending arrow |
| 精力/电池 | battery with charge indicator |
| 盾牌/自控 | shield icon |
| 创意/灯泡 | glowing lightbulb |
| 焦虑/压力 | tangled knot unraveling |
| 睡眠/夜晚 | crescent moon with stars |
| 读书/学习 | open book icon |
| 运动/跑步 | running stick figure |
| 团队/协作 | two stick figures high-fiving |
| 目标/Flag | flag on pole |
| 增长/数据 | bar chart with upward trend |
| 检查/完成 | bold checkmark in green circle |

## 马克笔颜色语义

| 颜色 | 用途 | 提示词关键词 |
|------|------|----------|
| 蓝色 | 标题 | blue handwritten, large blue marker |
| 黑色 | 正文/箭头 | black marker, black handwritten |
| 红色 | 强调/警示 | bold red handwritten, red marker |
| 黄色 | 便利贴 | yellow sticky note |
| 绿色 | 完成/正向 | green checkmark, green marker |

## 调用格式

```python
image_synthesize(
  requests=[{
    "prompt": "完整英文提示词（见上方模板组装）",
    "output_file": "/workspace/[用户主题].png",
    "aspect_ratio": "16:9",   # 16:9 横版 / 9:16 竖版
    "resolution": "2K"        # 1K / 2K / 4K
  }]
)
```

## 输出规则

- 文件路径：`/workspace/[英文主题]_whiteboard.png`
- 生成后用 `message` tool 发给用户（channel=feishu）
- 同时附上**完整英文提示词**供用户保存复用
- 中文内容建议后期用 Canva/PS 叠加精准文字，AI 生成的中文仅供参考

## 参考资源

- 完整模板库：`references/prompt-library.md`
- 图标对照表（扩展版）：`references/icon-guide.md`
