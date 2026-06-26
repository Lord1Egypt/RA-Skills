# 三位一体报告模板：战略 + 策略 + 指标（餐饮行业版）

---

## 报告结构总览

```
[品牌名称] 餐饮商业模式全景报告
生成时间：YYYY-MM-DD

━━━━━━━━━━━━━━━━━━━━━━━━━━━━
第一部分：商业模式全景（战略层）
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1.1 品牌概况与所属业态
1.2 商业模式画布解析（9要素·餐饮版）
1.3 商业模式类型识别（经营模式+收入模型）
1.4 价值主张核心分析（口味/环境/服务/性价比）
1.5 竞争壁垒与护城河
1.6 竞争格局映射（竞品对比矩阵）
1.7 风险矩阵

━━━━━━━━━━━━━━━━━━━━━━━━━━━━
第二部分：近期战略动向（策略层）
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
2.1 近3-6个月重大新闻摘要（联网检索）
2.2 战略选择分析（扩张/深化/转型/出海/收缩）
2.3 营销与渠道策略近期动作
2.4 商业模式演化方向研判

━━━━━━━━━━━━━━━━━━━━━━━━━━━━
第三部分：核心指标体系（指标层）
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
3.1 北极星指标（定义 + 当前数据）
3.2 二级驱动指标（3-5个 + 数据）
3.3 三级过程指标（若干 + 数据）
3.4 指标趋势解读

━━━━━━━━━━━━━━━━━━━━━━━━━━━━
第四部分：餐饮经营专项分析
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
4.1 单位经济模型（单店P&L+投资回报）
4.2 成本结构健康度（四费分析）
4.3 门店效率分析（坪效/人效/翻台率）
4.4 供应链与标准化水平
4.5 数字化成熟度评估

━━━━━━━━━━━━━━━━━━━━━━━━━━━━
第五部分：扩展分析（按需生成）
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
5.1 组织能力诊断（人才梯队/培训/激励/管理幅度）
5.2 区域分布分析（城市层级/区域渗透/战略路径）
5.3 消费者洞察（画像/趋势/场景偏好）
5.4 出海分析（若有海外布局）
5.5 技术与AI应用评估
5.6 ESG与可持续性

━━━━━━━━━━━━━━━━━━━━━━━━━━━━
综合研判：战略-策略-指标三位一体解读
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## HTML 报告格式规范

### 配色（暖色餐饮主题）
- 背景：`#faf8f5`
- 卡片背景：`#ffffff`
- 标题色：`#1a1a1a`
- 强调色：`#c0392b`（暖红色，餐饮感强）
- 辅助强调：`#e67e22`（暖橙色）
- 次要文字：`#666666`
- 边框/分割线：`#e8e0d8`
- 指标高亮：`#fff5f5`（浅红底）
- 正向趋势：`#27ae60`（绿色）
- 负向趋势：`#e74c3c`（红色）

### 字体
```css
font-family: 'PingFang SC', 'Noto Sans SC', 'Microsoft YaHei', sans-serif;
```

### 布局结构
```html
<div class="report-container">
  <!-- 封面卡片：品牌名、业态、门店规模、报告日期 -->
  <div class="cover-card">...</div>
  
  <!-- 五个主要部分，每部分独立卡片 -->
  <div class="section-card" id="part1">战略层</div>
  <div class="section-card" id="part2">策略层</div>
  <div class="section-card" id="part3">指标层</div>
  <div class="section-card" id="part4">餐饮专项</div>
  <div class="section-card" id="part5">扩展分析（按需）</div>
  
  <!-- 综合研判 -->
  <div class="summary-card">三位一体综合解读</div>
</div>
```

### 指标展示组件
```html
<!-- 北极星指标 - 突出展示 -->
<div class="nsm-block">
  <span class="nsm-label">⭐ 北极星指标</span>
  <span class="nsm-name">翻台率 × 客单价</span>
  <span class="nsm-value">3.8次/天 × ¥105 = ¥399/桌/天</span>
  <span class="nsm-trend">↑ 12% YoY</span>
</div>

<!-- 成本四费健康度仪表盘 -->
<div class="cost-dashboard">
  <div class="cost-item">
    <span class="cost-label">食材成本率</span>
    <span class="cost-value">36.2%</span>
    <span class="cost-status healthy">✅ 健康（≤38%）</span>
  </div>
  <div class="cost-item">
    <span class="cost-label">人力成本率</span>
    <span class="cost-value">23.8%</span>
    <span class="cost-status healthy">✅ 健康（≤25%）</span>
  </div>
  <div class="cost-item">
    <span class="cost-label">租金成本率</span>
    <span class="cost-value">11.5%</span>
    <span class="cost-status healthy">✅ 健康（≤12%）</span>
  </div>
  <div class="cost-item">
    <span class="cost-label">四费合计</span>
    <span class="cost-value">78.5%</span>
    <span class="cost-status warning">⚠️ 偏高（目标≤75%）</span>
  </div>
</div>

<!-- 二级/三级指标 - 表格形式 -->
<table class="metrics-table">
  <thead><tr><th>指标</th><th>当前值</th><th>趋势</th><th>行业基准</th><th>来源</th></tr></thead>
  <tbody>...</tbody>
</table>
```

### 商业模式画布可视化（餐饮版）
用 HTML 表格近似还原9格画布布局：
```
┌──────────────────────────────────────────────────────────────┐
│ 重要伙伴      │ 关键业务      │ 价值主张      │ 客户关系      │ 客户细分      │
│ ·食材供应商   │ ·采购/品控    │ ·口味/品质    │ ·会员体系     │ ·堂食顾客     │
│ ·外卖平台     │ ·菜品研发     │ ·环境/服务    │ ·私域社群     │ ·外卖顾客     │
│ ·中央厨房     │ ·门店运营     │ ·性价比       │ ·点评互动     │ ·加盟商       │
│               ├───────────────┤ ·便捷/快速    ├───────────────┤ ·企业/团餐    │
│               │ 核心资源      │               │ 渠道通路      │               │
│               │ ·品牌/口碑    │               │ ·门店/外卖    │               │
│               │ ·供应链/SOP   │               │ ·小程序/抖音  │               │
├──────────────┴───────────────┴───────────────┴───────────────┴───────────────┤
│     成本结构（食材+人力+租金+能耗）          │       收入来源（堂食+外卖+加盟+零售）  │
└──────────────────────────────────────────────────────────────────────────────┘
```

### 竞品对比组件（新增）
```html
<!-- 竞品矩阵表格 -->
<table class="competitor-table">
  <thead>
    <tr><th>品牌</th><th>门店数</th><th>客单价</th><th>翻台率</th><th>经营模式</th><th>核心差异</th></tr>
  </thead>
  <tbody>
    <tr class="highlight-row"><td>目标品牌</td><td>1,383</td><td>¥105</td><td>3.9</td><td>直营+加盟</td><td>极致服务</td></tr>
    <tr><td>竞品A</td><td>...</td><td>...</td><td>...</td><td>...</td><td>...</td></tr>
    <tr><td>竞品B</td><td>...</td><td>...</td><td>...</td><td>...</td><td>...</td></tr>
  </tbody>
</table>
```

### 风险矩阵组件（新增）
```html
<div class="risk-matrix">
  <div class="risk-item risk-high">
    <span class="risk-label">🔴 高风险</span>
    <span class="risk-name">人力成本刚性上升</span>
    <span class="risk-desc">概率：高 | 影响：高 | 现有防控：灵活用工+自动化</span>
  </div>
  <div class="risk-item risk-medium">
    <span class="risk-label">🟡 中风险</span>
    <span class="risk-name">子品牌品控挑战</span>
    <span class="risk-desc">概率：中 | 影响：中 | 现有防控：蜀海供应链统一管理</span>
  </div>
</div>
```

### 单店经济模型组件（新增）
```html
<div class="unit-economics">
  <h4>💰 单店经济模型</h4>
  <table>
    <tr><td>月营收</td><td class="value">¥30万</td></tr>
    <tr><td>- 食材成本（38%）</td><td>¥11.4万</td></tr>
    <tr><td>- 人力成本（25%）</td><td>¥7.5万</td></tr>
    <tr><td>- 租金（10%）</td><td>¥3.0万</td></tr>
    <tr><td>- 其他（12%）</td><td>¥3.6万</td></tr>
    <tr class="profit-row"><td>= 门店利润（15%）</td><td class="value">¥4.5万</td></tr>
    <tr><td>投资回报周期</td><td>18个月</td></tr>
  </table>
</div>
```

### 门店效率对比组件（餐饮专属）
```html
<!-- 效率三角对比 -->
<div class="efficiency-triangle">
  <div class="metric-card">
    <h4>🍽️ 翻台率</h4>
    <span class="value">3.8次/天</span>
    <span class="benchmark">行业基准：3.2次</span>
  </div>
  <div class="metric-card">
    <h4>📐 坪效</h4>
    <span class="value">¥2,800/㎡/月</span>
    <span class="benchmark">行业基准：¥2,200</span>
  </div>
  <div class="metric-card">
    <h4>👤 人效</h4>
    <span class="value">¥6.5万/人/月</span>
    <span class="benchmark">行业基准：¥5.6万</span>
  </div>
</div>
```

---

## 报告写作规范

### 风格要求
- 去 AI 化：避免"值得注意的是"、"需要指出"等模板语
- 具体数据优先：尽量用数字替代形容词
- 场景化表达：用具体经营场景说明抽象策略
- 简洁段落：每段不超过4句，快速传递关键信息

### 新闻整合规范
- 每条新闻来源标注（来源：36氪/界面新闻/餐饮老板内参/Bloomberg/官方PR）
- 时间标注（如：2025年3月）
- 与商业模式的关联解读（这个动作对应商业模式画布中哪个模块的变化？）

### 指标缺失处理
- 明确标注"数据未公开"
- 提供行业基准值作为参考（如：行业平均翻台率 2.1次/天）
- 不捏造数据，不模糊表述

### 餐饮行业数据特殊处理
- 区分"同店数据"和"总体数据"（含新店）
- 注意季节性：春节/五一/国庆/暑假为旺季
- 外卖数据需扣除平台佣金后计算实际收入
- 加盟品牌需区分"总部口径"和"门店口径"

---

## 综合研判写作框架

三位一体解读 = **战略一致性** + **策略执行质量** + **指标印证**

```
[战略] 该品牌核心战略是XXX，商业模式本质是XXX模式（直营/加盟/供应链型）。
[策略] 近期动作（新闻A、新闻B）表明品牌正在XXX方向加速/调整/收缩。
[指标] 这一策略已在XXX指标上体现：[数据]，同比/环比XXX。
[成本] 四费合计XXX%，[健康/偏高/风险]，其中XXX成本是主要压力/亮点。
[竞争] 在XXX赛道中，该品牌处于[领先/追赶/差异化]位置，与竞品A/B的核心差异在于XXX。
[风险] 前3大风险：① XXX（概率X/影响X）② XXX ③ XXX。
[组织] 组织能力[匹配/存在瓶颈]战略目标，关键约束在于XXX。
[出海] （若有）海外布局处于XXX阶段，核心挑战是XXX。
[ESG] ESG总体处于[初级/进阶/领先]水平，主要亮点/短板在XXX。
[研判] 战略与近期动作[一致/存在分歧]。主要风险点在于XXX，关键机遇在于XXX。
```

---

## 数据置信度标签组件

报告中每个核心数字必须标注数据置信度：

```html
<!-- 数据置信度CSS -->
<style>
  .conf { font-size: 0.75em; padding: 2px 6px; border-radius: 4px; margin-left: 4px; vertical-align: middle; }
  .conf-high { background: #e8f5e9; color: #2e7d32; }
  .conf-mid { background: #fff3e0; color: #e65100; }
  .conf-low { background: #fce4ec; color: #c62828; }
</style>

<!-- 使用示例 -->
<td>翻台率 3.8次/天 <span class="conf conf-high">确·2024年报</span></td>
<td>门店数 ~4,200家 <span class="conf conf-mid">推·窄门餐眼</span></td>
<td>食材成本率 ~35% <span class="conf conf-low">估·行业基准</span></td>
```

---

## 组织能力诊断组件

```html
<div class="org-capability">
  <h4>👥 组织能力诊断</h4>
  <table>
    <thead><tr><th>维度</th><th>现状</th><th>评级</th><th>关键发现</th></tr></thead>
    <tbody>
      <tr><td>人才梯队</td><td>店长储备率120%</td><td class="rating-good">✅ 成熟</td><td>师徒制体系成熟</td></tr>
      <tr><td>培训体系</td><td>内部大学+线上平台</td><td class="rating-good">✅ 成熟</td><td>培训覆盖率95%</td></tr>
      <tr><td>激励机制</td><td>合伙人制+利润分红</td><td class="rating-excellent">🌟 卓越</td><td>行业标杆</td></tr>
      <tr><td>管理幅度</td><td>1:10（区域经理:门店）</td><td class="rating-good">✅ 成熟</td><td>数字化赋能中</td></tr>
    </tbody>
  </table>
</div>
```

---

## 区域分布分析组件

```html
<div class="regional-analysis">
  <h4>🗺️ 区域分布分析</h4>
  <table>
    <thead><tr><th>城市层级</th><th>门店数</th><th>占比</th><th>SSSG</th><th>利润率</th><th>渗透空间</th></tr></thead>
    <tbody>
      <tr><td>一线城市</td><td>350</td><td>26%</td><td>+2.1%</td><td>12%</td><td>趋于饱和</td></tr>
      <tr><td>新一线城市</td><td>420</td><td>31%</td><td>+5.8%</td><td>15%</td><td>仍有空间</td></tr>
      <tr><td>二线城市</td><td>380</td><td>28%</td><td>+8.2%</td><td>16%</td><td>增长引擎</td></tr>
      <tr><td>三线及以下</td><td>200</td><td>15%</td><td>+12%</td><td>14%</td><td>待验证</td></tr>
    </tbody>
  </table>
</div>
```

---

## 出海分析组件（按需）

```html
<div class="overseas-analysis">
  <h4>🌏 出海分析</h4>
  <table>
    <thead><tr><th>目标市场</th><th>门店数</th><th>进入时间</th><th>经营模式</th><th>本地化程度</th><th>盈利状态</th></tr></thead>
    <tbody>
      <tr><td>东南亚</td><td>120</td><td>2018年</td><td>直营+合作</td><td>中</td><td>盈利</td></tr>
      <tr><td>日本</td><td>15</td><td>2020年</td><td>直营</td><td>高</td><td>盈亏平衡</td></tr>
    </tbody>
  </table>
</div>
```

---

## ESG评估组件（按需）

```html
<div class="esg-assessment">
  <h4>🌱 ESG与可持续性评估</h4>
  <div class="esg-grid">
    <div class="esg-card esg-e">
      <h5>🌍 环境 (E)</h5>
      <span class="esg-rating">进阶</span>
      <ul><li>食材损耗跟踪系统 ✅</li><li>可降解包装试点 ✅</li><li>碳排放核算 ❌</li></ul>
    </div>
    <div class="esg-card esg-s">
      <h5>🤝 社会 (S)</h5>
      <span class="esg-rating">领先</span>
      <ul><li>员工持股计划 ✅</li><li>食安全链路可追溯 ✅</li><li>供应商审核制度 ✅</li></ul>
    </div>
    <div class="esg-card esg-g">
      <h5>⚖️ 治理 (G)</h5>
      <span class="esg-rating">进阶</span>
      <ul><li>独立董事制度 ✅</li><li>ESG报告 ❌</li><li>职业化管理团队 ✅</li></ul>
    </div>
  </div>
</div>
```

---

## PDF 输出规范

除 HTML 报告外，同时生成 PDF 版本，便于正式分享和打印。

### PDF 生成方式

使用 Puppeteer 或浏览器 `window.print()` 从 HTML 转换 PDF：

```html
<!-- 在 HTML 报告 <head> 中加入打印样式 -->
<style>
  @media print {
    body { background: white; }
    .report-container { max-width: 100%; box-shadow: none; }
    .section-card { break-inside: avoid; box-shadow: none; border: 1px solid #ddd; }
    .cover-card { break-after: page; }
    .nsm-block { break-inside: avoid; }
    table { break-inside: avoid; }
    .no-print { display: none; }
  }
  
  @page {
    size: A4;
    margin: 15mm 12mm;
  }
</style>

<!-- 报告底部加入"导出PDF"按钮（仅屏幕显示） -->
<div class="no-print" style="text-align:center; margin:32px 0;">
  <button onclick="window.print()" style="
    padding: 12px 32px;
    background: #c0392b;
    color: white;
    border: none;
    border-radius: 8px;
    font-size: 16px;
    cursor: pointer;
  ">📄 导出 PDF</button>
</div>
```

### PDF 布局要点

- **封面页**：品牌名+业态+报告日期+门店规模概览，独占一页
- **分页规则**：每个主要 section（战略/策略/指标/专项/扩展）尽量从新页开始
- **避免截断**：表格、卡片组件使用 `break-inside: avoid` 防止被分页截断
- **页眉页脚**：页眉显示品牌名+报告类型，页脚显示页码和生成日期
- **字体大小**：PDF版正文用 `11pt`，标题用 `16pt`，小字注释用 `9pt`
