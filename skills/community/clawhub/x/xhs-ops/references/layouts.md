# 小红书配图布局体系

配图由两个维度决定：**风格**（怎么画）× **布局**（怎么排）。风格见 `illustration-prompts.md`，本文定义布局。

---

## 画布规范

### 推荐比例

| 名称 | 比例 | 尺寸 | 说明 |
|------|------|------|------|
| 竖版 3:4 | 3:4 | 1680×2240 | **首选**，小红书最高流量比例 |
| 竖版 9:16 | 9:16 | 1440×2560 | 更高竖版，适合长列表 |
| 方版 | 1:1 | 1920×1920 | 次选，适合对比图 |

### 安全区（⚠️ 必读）

小红书移动端 UI 会遮挡图片以下区域，**关键信息必须避开**：

```
┌─────────────────────────────┐
│                 [❤️ 📌 💬]  │  ← 右上角：点赞/收藏/评论按钮
│                             │
│                             │
│      ✓ 安全内容区域          │
│                             │
│                             │
│  [笔记标题 + 用户头像栏]     │  ← 底部 10%：标题栏遮挡
│                   [@水印]   │  ← 右下角：平台水印
└─────────────────────────────┘
```

| 避让区 | 位置 | 说明 |
|--------|------|------|
| 底部 10% | 最下方 | 标题栏覆盖，不放关键文字/数据 |
| 右上角 | 右上 15% | 互动按钮区 |
| 右下角 | 右下 10% | 水印位置 |

**所有配图 prompt 末尾追加**：
> Leave the bottom 10% of the image clean — no critical text or key visual elements — for mobile platform UI overlay. Avoid placing important content in the top-right corner.

---

## 布局类型

### 密度型布局

| 布局 | 信息密度 | 留白 | 信息点/图 | 最佳场景 |
|------|---------|------|----------|---------|
| `sparse` | 低 | 60-70% | 1-2 | 封面、金句、重磅声明 |
| `balanced` | 中 | 40-50% | 3-4 | 标准内容、教程、故事 |
| `dense` | 高 | 20-30% | 5-8 | 知识卡、干货速查、清单 |

### 结构型布局

| 布局 | 结构 | 条目数 | 最佳场景 |
|------|------|-------|---------|
| `list` | 垂直列举 | 4-7 条 | 排行榜、清单、步骤指南 |
| `comparison` | 左右对比 | 2 组 | before/after、优劣对比、产品PK |
| `flow` | 节点+箭头 | 3-6 步 | 流程、时间线、工作流 |
| `mindmap` | 中心放射 | 4-8 分支 | 概念图、知识脉络、话题总览 |
| `quadrant` | 四宫格/2×2 | 4 区块 | SWOT分析、优先级矩阵、分类对比 |

---

## 布局详细定义

### sparse（稀疏/冲击型）

```
结构：单一焦点居中，四周大量留白
视觉：对称构图，一个核心元素+大字标题
文字：主标题 ≤ 8 字，副标题可选，无正文段落
```

**Prompt 关键词**：
> Centered single focal point, abundant whitespace on all sides, symmetrical composition, one dominant visual element, large bold title text.

**典型用法**：封面图、金句卡、开篇声明、结尾CTA

---

### balanced（均衡型）

```
结构：标题居上（约20%），内容区均匀分布（约60%），底部留白（约20%）
视觉：清晰的视觉层次，3-4个并列或上下排列的要点
文字：标题 + 3-4 条要点（每条 5-10 字）+ 可选小图标
```

**Prompt 关键词**：
> Top-weighted title, evenly distributed content sections below, clear visual hierarchy, 3-4 key points with icons, moderate whitespace.

**典型用法**：标准内容页、教程讲解、经验分享

---

### dense（密集/知识卡型）

```
结构：紧凑网格，多区块有明确边界，标题+多个子分区
视觉：高信息密度但有组织，每个区块独立成组
文字：标题 + 5-8 个要点/数据项，允许较小字号，关键词高亮
```

**Prompt 关键词**：
> Organized grid structure, clear section boundaries, compact but readable spacing, multiple content blocks with headers, highlighted keywords, high information density.

**典型用法**：知识卡片、干货速查表、工具推荐合集

---

### list（列表/排行型）

```
结构：垂直排列 4-7 个条目，每条有序号/图标+标题+简述
视觉：左对齐，清晰的序号层级，一致的条目格式
文字：每条 = 序号 + 标题（3-5字）+ 一句描述
```

**Prompt 关键词**：
> Vertical enumeration with clear numbering, left-aligned items, consistent item format, visual hierarchy through number/bullet styling.

**典型用法**：Top N 排行、避坑清单、必备工具

---

### comparison（对比型）

```
结构：左右对称分屏，中间有分隔线/vs标记
视觉：左右配色差异明显（如绿vs红、亮vs暗），对比强烈
文字：顶部标题 + 左右各 3-4 条对应要点
```

**Prompt 关键词**：
> Split vertically into left and right halves with clear divider, symmetrical layout, contrasting colors for each side, corresponding comparison points.

**典型用法**：before/after、传统vs新方法、产品A vs 产品B

---

### flow（流程型）

```
结构：从上到下（或从左到右）的连接节点，箭头串联
视觉：3-6 个步骤节点，每个节点内有编号+简述，箭头连接
文字：每步 = 编号 + 标题（3-5字）+ 可选简述
```

**Prompt 关键词**：
> Top-to-bottom (or left-to-right) flow with connected nodes, directional arrows between steps, numbered stages, clear progression indicators.

**典型用法**：操作教程、工作流展示、决策路径

---

### mindmap（脑图/放射型）

```
结构：中心主题节点，向外放射 4-8 个分支，支持子分支
视觉：有机曲线连接，层级通过大小/颜色区分
文字：中心 = 主题（3-5字），分支 = 子主题（2-4字），叶节点 = 关键词
```

**Prompt 关键词**：
> Central topic node with radial branches outward, organic curved connections, hierarchical sub-branches, each branch with a distinct color from the palette.

**典型用法**：概念图、知识脉络、头脑风暴结果、话题全景

---

### quadrant（四象限型）

```
结构：2×2 网格，每个象限独立内容区，中心可选标记交叉轴
视觉：四个象限用不同色块区分，轴标签清晰
文字：每象限 = 类型标签（2-3字）+ 2-4 条内容
```

**Prompt 关键词**：
> Four-quadrant grid (2×2), clear axis labels at center cross, each quadrant with distinct background color, organized content within each section.

**典型用法**：SWOT 分析、优先级矩阵（紧急/重要）、四象限分类、对比归类

---

## 按位置推荐布局

| 位置 | 图片序号 | 推荐布局 | 原因 |
|------|---------|---------|------|
| Cover（封面） | 第 1 张 | `sparse` | 最大视觉冲击，清晰标题 |
| Setup（铺垫） | 第 2 张 | `balanced` | 建立上下文，不过载 |
| Core（核心） | 第 3 到 N-1 张 | `balanced` / `dense` / `list` | 根据信息密度选择 |
| Payoff（收获） | 倒数第 2 张 | `balanced` / `list` | 可执行的行动建议 |
| Ending（结尾） | 最后 1 张 | `sparse` | 干净的 CTA + 互动引导 |

---

## Prompt 中引用布局

在风格 prompt 块之后、内容描述之前，插入布局指令：

```
## 布局
[从上方对应布局的 Prompt 关键词中复制]

## 内容
[具体要展示的信息]
```
