# 配色系统

## 怎么上色（最重要）

上色步骤：

1. **找出图中有几个分组**（层级、分支、类别、阶段...）
2. **为每个分组选一种不同颜色**（从色板中选 2-4 种颜色）
3. **分组背景**用浅色填充 + 低透明度 -- 告诉读者"这块是一个整体"
4. **分组内节点**用白色填充 + 该分组的深色 border_color -- 告诉读者"这些属于这个分组"

具体映射（经典色板）：

| 分组 | 背景 fill_color | 背景 border_color | 节点 border_color |
|------|----------------|-------------------|-------------------|
| 第 1 组 | #F0F4FC（浅蓝） | #5178C6 | #5178C6 |
| 第 2 组 | #EAE2FE（浅紫） | #8569CB | #8569CB |
| 第 3 组 | #DFF5E5（浅绿） | #509863 | #509863 |
| 第 4 组 | #FEF1CE（浅黄） | #D4B45B | #D4B45B |
| 第 5 组 | #FEE3E2（浅红） | #D25D5A | #D25D5A |
| 内部节点 | #FFFFFF | 跟随所属分组 | -- |

**各类图表怎么上色**：
- 架构图有 3 层 -- 每层一种颜色，层背景浅色填充（opacity <= 25），层内节点白色 + 深色边框
- 对比表有 3 列 -- 每列表头一种颜色，该列数据单元格用同色边框
- 组织架构有 4 个部门 -- 每个部门一种颜色，子部门白色 + 同色边框
- 流程图 -- 起止节点一种颜色，判断节点一种颜色，步骤节点白色

> 用户配色优先。用户指定了色值/风格时以用户为准。用户只给 1-2 个色值时，推导完整色板：主色 -> 浅底 -> 深边框 -> 灰调连线色。
> 用户未指定配色时，必须从下方色板表中选取颜色，不要自创色值。

---

## 结构规则

### 分组 -- 不同层/分组必须用不同颜色

选 2-4 种颜色，每种代表一个分组。同组节点视觉完全一致（fill_color、border_color 相同）。

### 分层 -- 外重内轻

- 外层（大分区背景）：浅色填充，fill_opacity <= 25
- 内层（具体节点）：白色填充（opacity=100） + 分组色边框

### 清晰

- 所有节点有边框（border_style=solid, border_width=medium）
- 间距不粘连（同层 >= 30px，有连线 >= 60px）
- 文字清晰可读（font_size >= 14）
- 连线用灰色（色板连线色），不抢节点注意力

### 统一参数

| 参数 | 值 | 为什么 |
|------|---|--------|
| border_width | `medium` | 让边框清晰可见 |
| border_style | `solid` | 统一的边框风格 |
| fill_opacity（节点） | 100 | 实心填充 |
| fill_opacity（背景） | <= 25 | 不遮挡上层 |
| font_size（正文） | >= 14 | 可读 |
| font_size（标题） | >= 24 | 醒目 |
| font_size（辅助） | >= 13 | 不费眼 |

---

## 色板选择指南

| 色板 | 适用场景 | 关键词 |
|------|---------|-------|
| 经典 | 通用图表、说明文档 | 默认、通用 |
| 商务 | 汇报、企业架构、正式文档 | 专业、正式、给老板看 |
| 科技 | 技术架构、DevOps、监控 | 技术、炫酷、暗色 |
| 清新 | 流程图、用户旅程、教程 | 清新、自然、轻松 |
| 极简 | 论文配图、学术报告 | 学术、极简、黑白 |

未指定时默认使用"经典"色板。

---

## 预设色板

每套色板定义 7 个角色的颜色。连线色是色板的一部分。

### 经典（默认）

| 角色 | fill_color | border_color | text font_color |
|------|-----------|-------------|-----------------|
| 分区背景 | #F0F4FC | #5178C6 | #1F2329 |
| 第 2 分组 | #EAE2FE | #8569CB | #1F2329 |
| 第 3 分组 | #DFF5E5 | #509863 | #1F2329 |
| 第 4 分组 | #FEF1CE | #D4B45B | #1F2329 |
| 第 5 分组 | #FEE3E2 | #D25D5A | #1F2329 |
| 内容节点 | #FFFFFF | 跟随分组 | #1F2329 |
| 强调/表头 | #1F2329 | #1F2329 | #FFFFFF |
| 连线 | -- | #BBBFC4 | -- |

### 商务

| 角色 | fill_color | border_color | text font_color |
|------|-----------|-------------|-----------------|
| 分区背景 | #EDF2F7 | #4A6FA5 | #1A202C |
| 第 2 分组 | #D4E0ED | #4A6FA5 | #1A202C |
| 第 3 分组 | #E8EDF3 | #5A7B9A | #1A202C |
| 第 4 分组 | #F0F0F0 | #8895A7 | #1A202C |
| 内容节点 | #FFFFFF | #718BAE | #1A202C |
| 强调/表头 | #2D4A7A | #2D4A7A | #FFFFFF |
| 连线 | -- | #718BAE | -- |

### 科技（暗色）

| 角色 | fill_color | border_color | text font_color |
|------|-----------|-------------|-----------------|
| 画布/分区背景 | #0F172A | #1E293B | #E2E8F0 |
| 第 2 分组 | #1E293B | #3B82F6 | #E2E8F0 |
| 第 3 分组 | #1E293B | #8B5CF6 | #E2E8F0 |
| 第 4 分组 | #1E293B | #10B981 | #E2E8F0 |
| 内容节点 | #1E293B | #334155 | #E2E8F0 |
| 强调 | #2563EB | #3B82F6 | #FFFFFF |
| 连线 | -- | #475569 | -- |

### 清新

| 角色 | fill_color | border_color | text font_color |
|------|-----------|-------------|-----------------|
| 分区背景 | #F0FDF4 | #86EFAC | #14532D |
| 第 2 分组 | #DCFCE7 | #4ADE80 | #14532D |
| 第 3 分组 | #ECFDF5 | #6EE7B7 | #14532D |
| 第 4 分组 | #F0FDFA | #5EEAD4 | #134E4A |
| 内容节点 | #FFFFFF | #86EFAC | #14532D |
| 强调 | #16A34A | #16A34A | #FFFFFF |
| 连线 | -- | #86EFAC | -- |

### 极简

| 角色 | fill_color | border_color | text font_color |
|------|-----------|-------------|-----------------|
| 分区背景 | #F8F9FA | #DEE2E6 | #212529 |
| 第 2 分组 | #E9ECEF | #ADB5BD | #212529 |
| 第 3 分组 | #F1F3F5 | #868E96 | #212529 |
| 第 4 分组 | #F8F9FA | #ADB5BD | #212529 |
| 内容节点 | #FFFFFF | #CED4DA | #212529 |
| 强调/表头 | #495057 | #495057 | #FFFFFF |
| 连线 | -- | #ADB5BD | -- |

---

## 各元素怎么画

> 以下示例使用经典色板。选了其他色板时替换对应颜色，结构不变。

### 图表标题

大号深色文字，居中。用 composite_shape + 无边框无填充模拟纯文本。

```json
{"style": {"fill_opacity": 0, "border_style": "none"},
 "text": {"font_size": 24, "font_weight": "bold", "horizontal_align": "center"}}
```

### 分区背景

浅色填充 + 低透明度 + 对应深色边框。内部放白色节点。

```json
{"style": {"fill_color": "#F0F4FC", "fill_opacity": 25,
           "border_style": "solid", "border_color": "#5178C6", "border_width": "narrow", "border_opacity": 40},
 "z_index": 0}
```

### 分区标签

独立文本节点，深色文字。通过 composite_shape 模拟。

```json
{"style": {"fill_opacity": 0, "border_style": "none"},
 "text": {"font_size": 18, "font_weight": "bold", "horizontal_align": "left"}}
```

### 内容节点

白色填充，边框颜色跟随所属分组。

```json
{"style": {"fill_color": "#FFFFFF", "fill_opacity": 100,
           "border_style": "solid", "border_color": "#5178C6", "border_width": "medium", "border_opacity": 100},
 "z_index": 10}
```

白色节点的 border_color 取决于所属分组：
```
蓝色分组: border_color="#5178C6"
紫色分组: border_color="#8569CB"
绿色分组: border_color="#509863"
独立节点: border_color="#DEE0E3"
```

### 表头

深色填充 + 白色文字。

```json
{"style": {"fill_color": "#1F2329", "fill_opacity": 100,
           "border_style": "solid", "border_color": "#1F2329", "border_width": "medium", "border_opacity": 100},
 "text": {"font_size": 15, "font_weight": "bold", "horizontal_align": "center"},
 "z_index": 10}
```

### 连线

使用色板中的连线色，不用彩色。

```json
{"style": {"border_color": "#BBBFC4", "border_opacity": 100,
           "border_style": "solid", "border_width": "narrow"},
 "z_index": 50}
```

### 辅助说明

灰色小字，弱化不抢注意力。

```json
{"text": {"font_size": 13, "font_weight": "regular"},
 "style": {"fill_opacity": 0, "border_style": "none"}}
```

---

## 常见错误

错误：每个节点一种颜色 -> 读者分不清分组
正确：同组节点视觉一致（相同 fill_color + border_color）

错误：内外层都用重色 -> 读者不知道先看哪里
正确：外层浅色（opacity <= 25），内层白色实心

错误：连线用和节点一样的彩色 -> 抢注意力
正确：连线统一用色板连线色（经典色板 #BBBFC4）

错误：节点没边框 -> 和背景融为一体
正确：所有节点 border_style=solid, border_width=medium

错误：全图黑白灰，没有颜色区分 -> 无法识别分组
正确：不同分组用色板中不同颜色
