# SVG 可视化设计规范

## 设计系统

### 色彩方案

```
主色（强调/标题）:    #6C5CE7  紫色
正面（改进/优势）:    #00B894  绿色
负面（问题/瓶颈）:    #E17055  橙红
中性（说明文字）:     #636E72  灰色
背景浅色:            #F8F9FA  浅灰
背景白色:            #FFFFFF  纯白
辅助浅紫:            #DFE6E9  浅灰蓝
高亮背景:            #FFEAA7  浅黄（用于聚焦）
```

### 字体规范

```xml
<!-- 标题 -->
<text font-size="18" font-weight="bold" font-family="system-ui, -apple-system, sans-serif">

<!-- 副标题 -->
<text font-size="15" font-weight="600" font-family="system-ui, -apple-system, sans-serif">

<!-- 正文 -->
<text font-size="13" font-family="system-ui, -apple-system, sans-serif">

<!-- 标注/注释 -->
<text font-size="11" font-family="system-ui, -apple-system, sans-serif" fill="#636E72">
```

### 图形元素

```xml
<!-- 标准矩形（圆角） -->
<rect rx="8" ry="8" stroke-width="2" />

<!-- 强调矩形 -->
<rect rx="8" ry="8" stroke="#6C5CE7" stroke-width="2" fill="#f0efff" />

<!-- 问题矩形 -->
<rect rx="8" ry="8" stroke="#E17055" stroke-width="2" fill="#fff5f3" />

<!-- 方案矩形 -->
<rect rx="8" ry="8" stroke="#00B894" stroke-width="2" fill="#f0fff4" />

<!-- 连接箭头 -->
<marker id="arrowhead" markerWidth="10" markerHeight="7" refX="10" refY="3.5" orient="auto">
  <polygon points="0 0, 10 3.5, 0 7" fill="#636E72"/>
</marker>
<line marker-end="url(#arrowhead)" stroke="#636E72" stroke-width="2"/>

<!-- 虚线（表示可选/弱关联） -->
<line stroke-dasharray="5,5" stroke="#636E72" stroke-width="1.5"/>
```

### 阴影滤镜

```xml
<defs>
  <filter id="shadow" x="-5%" y="-5%" width="110%" height="110%">
    <feDropShadow dx="0" dy="2" stdDeviation="3" flood-opacity="0.1"/>
  </filter>
</defs>
<!-- 使用: filter="url(#shadow)" -->
```

## 图示类型模板

### 1. 架构对比图（左右分栏）

```xml
<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <!-- 标题 -->
  <text x="400" y="30" text-anchor="middle" font-size="18" font-weight="bold">{标题}</text>

  <!-- 左侧：旧方案 -->
  <rect x="20" y="50" width="370" height="330" rx="12" fill="#fff5f3" stroke="#E17055" stroke-width="2"/>
  <text x="205" y="75" text-anchor="middle" font-size="15" font-weight="600" fill="#E17055">旧方案</text>
  <!-- 内容区域 -->

  <!-- 右侧：新方案 -->
  <rect x="410" y="50" width="370" height="330" rx="12" fill="#f0fff4" stroke="#00B894" stroke-width="2"/>
  <text x="595" y="75" text-anchor="middle" font-size="15" font-weight="600" fill="#00B894">新方案</text>
  <!-- 内容区域 -->

  <!-- VS 分隔 -->
  <circle cx="400" cy="215" r="20" fill="#6C5CE7"/>
  <text x="400" y="221" text-anchor="middle" font-size="13" fill="white" font-weight="bold">VS</text>
</svg>
```

### 2. 流程图（从上到下或从左到右）

```xml
<svg viewBox="0 0 800 300" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrow" markerWidth="10" markerHeight="7" refX="10" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#6C5CE7"/>
    </marker>
  </defs>

  <!-- 步骤节点 -->
  <rect x="50" y="120" width="140" height="60" rx="8" fill="#f0efff" stroke="#6C5CE7" stroke-width="2"/>
  <text x="120" y="155" text-anchor="middle" font-size="13">步骤 1</text>

  <!-- 箭头连接 -->
  <line x1="190" y1="150" x2="250" y2="150" stroke="#6C5CE7" stroke-width="2" marker-end="url(#arrow)"/>

  <!-- 下一步骤... -->
</svg>
```

### 3. 层级结构图

```xml
<svg viewBox="0 0 800 350" xmlns="http://www.w3.org/2000/svg">
  <!-- 多层矩形从上到下叠加，用渐变色表示层级 -->
  <!-- 顶层（快/小） -->
  <rect x="250" y="40" width="300" height="60" rx="8" fill="#6C5CE7"/>
  <text x="400" y="75" text-anchor="middle" fill="white" font-size="14">Level 1 (Fast)</text>

  <!-- 中层 -->
  <rect x="150" y="120" width="500" height="70" rx="8" fill="#74b9ff"/>
  <text x="400" y="160" text-anchor="middle" fill="white" font-size="14">Level 2</text>

  <!-- 底层（慢/大） -->
  <rect x="50" y="210" width="700" height="80" rx="8" fill="#dfe6e9"/>
  <text x="400" y="255" text-anchor="middle" fill="#2d3436" font-size="14">Level 3 (Slow)</text>
</svg>
```

### 4. 趋势/性能对比图

```xml
<svg viewBox="0 0 800 350" xmlns="http://www.w3.org/2000/svg">
  <!-- 坐标轴 -->
  <line x1="80" y1="280" x2="750" y2="280" stroke="#2d3436" stroke-width="2"/>
  <line x1="80" y1="280" x2="80" y2="40" stroke="#2d3436" stroke-width="2"/>

  <!-- X轴标签 -->
  <text x="415" y="310" text-anchor="middle" font-size="13">X Axis</text>

  <!-- Y轴标签 -->
  <text x="30" y="160" text-anchor="middle" font-size="13" transform="rotate(-90,30,160)">Y Axis</text>

  <!-- 曲线A（标准方案） -->
  <polyline points="100,250 200,200 300,140 400,100 500,70 600,50" fill="none" stroke="#E17055" stroke-width="3"/>

  <!-- 曲线B（新方案） -->
  <polyline points="100,260 200,245 300,235 400,228 500,222 600,218" fill="none" stroke="#00B894" stroke-width="3"/>

  <!-- 图例 -->
  <rect x="550" y="40" width="15" height="15" fill="#E17055"/>
  <text x="570" y="52" font-size="12">标准方案</text>
  <rect x="550" y="62" width="15" height="15" fill="#00B894"/>
  <text x="570" y="74" font-size="12">新方案</text>
</svg>
```

### 5. 全景/矩阵图

```xml
<svg viewBox="0 0 800 500" xmlns="http://www.w3.org/2000/svg">
  <!-- 中心标题 -->
  <text x="400" y="30" text-anchor="middle" font-size="18" font-weight="bold">{全景标题}</text>

  <!-- 分类区块（网格布局） -->
  <!-- 每个卡片：120x80 或 150x90 -->
  <rect x="50" y="60" width="150" height="80" rx="8" fill="#f0efff" stroke="#6C5CE7"/>
  <text x="125" y="95" text-anchor="middle" font-size="12" font-weight="600">分类A</text>
  <text x="125" y="115" text-anchor="middle" font-size="11" fill="#636E72">说明</text>

  <!-- 连接线到中心或其他节点 -->
</svg>
```

### 6. 时间线图

```xml
<svg viewBox="0 0 800 200" xmlns="http://www.w3.org/2000/svg">
  <!-- 主轴线 -->
  <line x1="50" y1="100" x2="750" y2="100" stroke="#dfe6e9" stroke-width="4"/>

  <!-- 时间节点 -->
  <circle cx="150" cy="100" r="12" fill="#6C5CE7"/>
  <text x="150" y="80" text-anchor="middle" font-size="12" font-weight="600">v1</text>
  <text x="150" y="130" text-anchor="middle" font-size="11" fill="#636E72">2022.06</text>
  <text x="150" y="148" text-anchor="middle" font-size="10" fill="#636E72">关键改进</text>

  <!-- 更多节点... -->
</svg>
```

## 内联到 HTML 的方式

```html
<div class="svg-figure">
  <svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
    <!-- SVG 内容 -->
  </svg>
  <p class="figure-caption">图 1：{图示说明}</p>
</div>
```

对应 CSS:
```css
.svg-figure {
  margin: 2rem 0;
  text-align: center;
}
.svg-figure svg {
  max-width: 100%;
  height: auto;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.06);
}
.figure-caption {
  margin-top: 0.8rem;
  font-size: 0.9rem;
  color: #636E72;
  font-style: italic;
}
```
