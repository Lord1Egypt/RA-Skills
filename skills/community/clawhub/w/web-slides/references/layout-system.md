# Layout System

## Rule

不要为每一页重新发明版式。优先从固定布局原型中组装整套 deck。

## Core Layouts

### `cover`

用途：

- 封面
- 开场标题
- 发布会开幕页

特征：

- 一句话主标题
- 一句副标题或价值陈述
- 品牌标识或演讲者信息
- 背景氛围最强

### `agenda`

用途：

- 目录
- 章节导览

特征：

- 3-6 个条目
- 当前章节高亮
- 结构明确，避免装饰过重

### `section-break`

用途：

- 章节切换
- 节奏重置

特征：

- 大标题
- 小段引导语
- 视觉上比内容页更有仪式感

### `insight`

用途：

- 单页表达一个核心观点
- 适合高管汇报和路演

特征：

- 1 个结论标题
- 2-4 个支持要点
- 可附 1 个强调数字

### `two-column`

用途：

- 图文并列
- 左右论证
- 要点 + 说明

特征：

- 左右内容权重清晰
- 不要两边都塞满字

### `metrics`

用途：

- KPI
- 核心数字
- 成长指标

特征：

- 1 个主指标 + 2-4 个副指标
- 数字最大、说明最短
- 适合移动端卡片堆叠

### `chart-focus`

用途：

- 图表结论页
- 数据洞察页

特征：

- 图表只服务于结论
- 同页必须有一句结论总结
- 避免满屏网格与复杂图例

### `timeline`

用途：

- 路线图
- 项目阶段
- 事件演进

特征：

- 3-6 个节点
- 当前或关键节点最强
- 移动端改为纵向时间线

### `comparison`

用途：

- 方案对比
- 前后对比
- 竞品对比

特征：

- 维度不超过 4
- 视觉上要让优选项更突出

### `quote`

用途：

- 客户证言
- 金句
- 观点强调

特征：

- 大引语
- 小署名
- 装饰弱于内容

### `closing`

用途：

- 总结
- Q&A
- 联系方式

特征：

- 以一句强收束为主
- 可附二维码/链接/联系方式

## Recommended Deck Recipes

### 标准商务汇报

`cover` → `agenda` → `section-break` → `insight` × 3 → `comparison` → `metrics` → `closing`

### 融资路演

`cover` → `insight` → `problem-solution`（用 `two-column`）→ `market`（用 `metrics`）→ `traction`（用 `chart-focus`）→ `roadmap`（用 `timeline`）→ `closing`

### 技术分享

`cover` → `agenda` → `section-break` → `insight` → `two-column` → `timeline` → `chart-focus` → `closing`

### 发布会

`cover` → `section-break` → `insight` → `two-column` → `metrics` → `quote` → `closing`

## Combination Rule

12 套主题都应支持以上布局原型。这样主题和布局可组合，形成高丰富度，但仍保持统一输出质量。
