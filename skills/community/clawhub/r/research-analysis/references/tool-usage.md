# 工具使用指南

## 一、天眼查企业信息查询（MCP 工具）

### 概述
天眼查 MCP 连接器提供企业工商信息、股权结构、融资历程、知识产权、风险信息等企业数据查询能力。

### 前置条件
- 用户需在 WorkBuddy 的「连接器管理」中启用 `tyc-mcp`（天眼查）连接器
- 查看连接状态：连接器名称为 `tyc-mcp 天眼查`

### 可用工具
天眼查 MCP 连接后，以下工具可用（通过 `mcp__tyc-mcp__` 前缀调用）：

| 工具 | 用途 | 关键参数 |
|------|------|---------|
| 企业基本信息查询 | 查询企业工商注册信息 | 企业名称/统一社会信用代码 |
| 股东信息查询 | 查询企业股东及持股比例 | 企业ID |
| 对外投资查询 | 查询企业对外投资情况 | 企业ID |
| 融资历程查询 | 查询企业融资轮次和金额 | 企业ID |
| 知识产权查询 | 查询专利、商标、软著 | 企业ID |
| 行政处罚查询 | 查询企业行政处罚记录 | 企业ID |
| 司法风险查询 | 查询企业诉讼/法院公告 | 企业ID |
| 经营异常查询 | 查询企业经营异常名录 | 企业ID |

### 使用流程
1. **确认连接状态**：首次使用时检查天眼查 MCP 是否已连接
2. **查询企业基本信息**：用企业名称查询，获取企业ID
3. **按需查询详细数据**：用企业ID查询股东、融资、知识产权等
4. **结构化整理**：将查询结果整理为表格或结构化文本
5. **融入分析报告**：将企业信息融入竞品分析或行业研究

### 未连接时的降级方案
- 提示用户：「天眼查连接器未连接，建议在连接器管理中启用以获取更详细的企业信息」
- 使用 WebSearch 搜索天眼查公开页面作为替代
- 使用 WebFetch 抓取天眼查公开页面内容

---

## 二、七麦数据查询

### 概述
七麦数据（qimai.cn）是国内领先的移动应用数据分析平台，提供 App 下载量、排名、评分、版本迭代、ASO关键词等数据。

### 可查询数据
| 数据维度 | 分析价值 | 获取方式 |
|---------|---------|---------|
| 下载量及趋势 | 判断产品增长态势 | 七麦数据公开页面 |
| App Store/安卓排名 | 品类排名变化反映竞争格局 | 七麦数据排名页 |
| 版本更新历史 | 产品迭代节奏、研发投入 | 七麦数据版本页 |
| 评论评分趋势 | 用户满意度变化 | 七麦数据评论页 |
| 关键词覆盖/ASO | 获客策略、搜索优化 | 七麦数据ASO页 |
| 预估收入(iOS) | 商业化能力 | 七麦数据收入预估 |

### 数据获取方式

#### 方式1：Web 搜索 + WebFetch
```
1. WebSearch 搜索："七麦数据 [App名称] 下载量"
2. 找到七麦数据页面 URL
3. WebFetch 获取页面内容
4. 提取关键数据
```

#### 方式2：用户提供数据
- 用户提供七麦数据导出的 Excel/CSV 文件
- 用户提供七麦数据页面截图
- 用户提供七麦数据 API 返回的 JSON 数据

#### 方式3：App Store 公开数据
```
1. WebSearch 搜索 "[App名称] App Store"
2. WebFetch 获取 App Store 页面
3. 提取评分、评论数、最近更新等信息
```

### 数据分析要点
1. **下载量趋势**：观察月环比、季环比变化，判断增长/衰退
2. **排名波动**：关注品类排名变化，对比竞品排名走势
3. **版本频率**：高频更新=研发活跃，低频更新=可能资源不足
4. **评论分析**：差评关键词提取，识别用户痛点
5. **ASO关键词**：分析竞品覆盖的关键词，找差异化获客机会

---

## 三、VisActor 图表生成

### 概述
VisActor 是字节跳动开源的可视化解决方案体系，包含：
- **VChart**：通用图表库（折线、柱状、饼图、散点等）
- **VTable**：高性能数据表格（支持大数据量、透视表）
- **VGrammar**：可视化语法（高度自定义）
- **VStory**：可视化叙事（数据故事讲述）

### CDN 引用
```html
<!-- VChart -->
<script src="https://unpkg.com/@visactor/vchart/build/index.min.js"></script>

<!-- VTable -->
<script src="https://unpkg.com/@visactor/vtable/build/index.min.js"></script>
```

### 常用图表代码模板

#### 折线图（趋势分析）
```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <script src="https://unpkg.com/@visactor/vchart/build/index.min.js"></script>
  <style>
    #chart { width: 800px; height: 450px; }
  </style>
</head>
<body>
  <div id="chart"></div>
  <script>
    const spec = {
      type: 'line',
      data: [{
        id: 'data',
        values: [
          { month: '1月', value: 120 },
          { month: '2月', value: 150 },
          { month: '3月', value: 180 },
          { month: '4月', value: 165 },
          { month: '5月', value: 210 },
          { month: '6月', value: 250 }
        ]
      }],
      xField: 'month',
      yField: 'value',
      title: { text: '月度增长趋势' },
      axes: [
        { orient: 'bottom', title: '月份' },
        { orient: 'left', title: '数值' }
      ]
    };
    const chart = new VChart.default(spec, { dom: 'chart' });
    chart.renderAsync();
  </script>
</body>
</html>
```

#### 柱状图（对比分析）
```html
<script>
  const spec = {
    type: 'bar',
    data: [{
      id: 'data',
      values: [
        { product: '产品A', marketShare: 35 },
        { product: '产品B', marketShare: 28 },
        { product: '产品C', marketShare: 20 },
        { product: '产品D', marketShare: 17 }
      ]
    }],
    xField: 'product',
    yField: 'marketShare',
    title: { text: '市场份额对比' },
    label: { visible: true }
  };
  const chart = new VChart.default(spec, { dom: 'chart' });
  chart.renderAsync();
</script>
```

#### 饼图（占比分析）
```html
<script>
  const spec = {
    type: 'pie',
    data: [{
      id: 'data',
      values: [
        { type: '搜索引擎', value: 45 },
        { type: '社交媒体', value: 25 },
        { type: '直接访问', value: 20 },
        { type: '其他', value: 10 }
      ]
    }],
    valueField: 'value',
    categoryField: 'type',
    title: { text: '获客渠道分布' },
    label: { visible: true }
  };
  const chart = new VChart.default(spec, { dom: 'chart' });
  chart.renderAsync();
</script>
```

#### 漏斗图（转化分析）
```html
<script>
  const spec = {
    type: 'funnel',
    data: [{
      id: 'data',
      values: [
        { stage: '曝光', value: 1000000 },
        { stage: '点击', value: 50000 },
        { stage: '访问', value: 45000 },
        { stage: '注册', value: 13500 },
        { stage: '购买', value: 2700 }
      ]
    }],
    categoryField: 'stage',
    valueField: 'value',
    title: { text: '用户转化漏斗' }
  };
  const chart = new VChart.default(spec, { dom: 'chart' });
  chart.renderAsync();
</script>
```

### 图表生成规范
1. **标题即结论**：图表标题写结论而非数据描述
2. **标注数据来源**：在图表下方或说明中标注数据来源
3. **配色专业**：使用统一色板，中国股市涨红跌绿
4. **交互友好**：默认启用 tooltip 悬浮提示
5. **响应式**：设置合理的图表宽高
6. **中文优先**：根据用户语言设置图表语言

### 替代方案
如果 VisActor 不可用，可使用以下替代方案：
- **Chart.js**：轻量级，CDN 引用方便
- **ECharts**：功能全面，中文生态好
- **D3.js**：高度自定义，适合复杂可视化

---

## 四、Web 搜索与信息整合

### 搜索策略
| 搜索目标 | 推荐搜索词 | 筛选方法 |
|---------|-----------|---------|
| 行业报告 | "[行业名] 行业报告 2024" | 优先权威机构（艾瑞、QuestMobile、IDC等） |
| 公司财报 | "[公司名] 财报/年报" | 优先官方投资者关系页面 |
| 新闻资讯 | "[公司名/行业] 最新动态" | 优先近3个月的信息 |
| 政策法规 | "[行业名] 政策/监管" | 优先政府官网 |
| 竞品动态 | "[竞品名] 融资/产品/人事" | 多源交叉验证 |

### 信息整合规范
1. **多源验证**：关键数据至少2个独立来源验证
2. **标注来源**：每个数据点标注来源和日期
3. **区分事实与观点**：客观数据与分析师观点分开标注
4. **时效性检查**：优先使用最近6个月的数据
5. **置信度标注**：对数据可信度标注（高/中/低）

### 常用数据源
| 数据类型 | 推荐来源 |
|---------|---------|
| 互联网行业数据 | 艾瑞咨询、QuestMobile、极光大数据 |
| 企业融资数据 | 天眼查、IT桔子、Crunchbase |
| App市场数据 | 七麦数据、SensorTower、App Annie |
| 电商数据 | 星图数据、魔镜市场情报 |
| 宏观经济 | 国家统计局、世界银行、IMF |
| 上市公司财报 | 巨潮资讯网、Wind、东方财富 |
| 社交媒体数据 | 新榜、微指数、微博数据中心 |
