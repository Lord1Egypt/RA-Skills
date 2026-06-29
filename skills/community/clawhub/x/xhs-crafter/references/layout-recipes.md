# Layout Recipes

> 3:4 (1080×1440) card layout recipes for xhs-crafter.
> Content density rule: on 1080×1440 cards, content must cover **≥75%** of canvas height.

---

## Editorial Magazine × E-ink Recipes

### M01 — Cover

| Field | Value |
|-------|-------|
| **Name** | Magazine Issue Cover |
| **Best for** | 封面页、主题开篇、系列首卡 |
| **Structure** | 顶部 issue 行 → 大号衬线标题 2-4 行 → 大图 35-55% → 底部 issue 条 3-5 要点 |

```html
<div class="card frame m01-cover">
  <div class="issue-row">Vol.03 · 2026 春</div>
  <h1 class="title-serif">如何构建<br>可持续的<br>知识体系</h1>
  <div class="image-well">
    <img src="…" style="object-fit:cover;object-position:center 50%">
  </div>
  <div class="issue-strip">
    <span>方法论</span><span>工具链</span><span>实践案例</span><span>复盘模板</span>
  </div>
</div>
```

---

### M02 — Field Note Photo

| Field | Value |
|-------|-------|
| **Name** | Field Note Photo |
| **Best for** | 照片主导页、田野记录、场景展示 |
| **Structure** | 大图 60-70% → field-note 标题 → 地点/日期元数据 |

```html
<div class="card frame m02-field-note">
  <div class="image-well">
    <img src="…" style="object-fit:cover;object-position:center 50%">
  </div>
  <div class="field-note">
    <h2 class="title-serif">山间工坊</h2>
    <p class="meta">📍 杭州 · 2026.04</p>
  </div>
</div>
```

---

### M03 — Feature Essay

| Field | Value |
|-------|-------|
| **Name** | Feature Essay |
| **Best for** | 长文节选、深度分析、编辑式排版 |
| **Structure** | 编辑式标题 → 窄文字列 + 宽图井交替 |

```html
<div class="card frame m03-essay">
  <header class="editorial-header">
    <span class="overline">深度</span>
    <h2 class="title-serif">设计的隐秩序</h2>
  </header>
  <div class="essay-body">
    <div class="text-column">
      <p>好的设计不是添加，而是减去多余……</p>
    </div>
    <div class="image-well">
      <img src="…" style="object-fit:cover;object-position:center 50%">
    </div>
  </div>
</div>
```

---

### M04 — Checklist / Numbered List

| Field | Value |
|-------|-------|
| **Name** | Checklist / Numbered List |
| **Best for** | 清单、步骤摘要、要点罗列 |
| **Structure** | 编辑式标题 → 编号条目（可选图标） → 配图 |

```html
<div class="card frame m04-checklist">
  <header class="editorial-header">
    <span class="overline">清单</span>
    <h2 class="title-serif">出发前检查</h2>
  </header>
  <ol class="checklist-items">
    <li><span class="nb">01</span> 确认护照有效期</li>
    <li><span class="nb">02</span> 预订住宿</li>
    <li><span class="nb">03</span> 购买旅行保险</li>
    <li><span class="nb">04</span> 打包随身物品</li>
  </ol>
  <div class="image-well">
    <img src="…" style="object-fit:cover;object-position:center 55%">
  </div>
</div>
```

---

### M05 — Pull Quote / Takeaway

| Field | Value |
|-------|-------|
| **Name** | Pull Quote / Takeaway |
| **Best for** | 金句、核心观点、关键洞察 |
| **Structure** | 大号衬线引文 → 来源/上下文行 |

```html
<div class="card frame m05-pull-quote">
  <blockquote class="pull-quote">
    <p class="title-serif">"简洁是复杂的终极形式。"</p>
  </blockquote>
  <div class="source-row">
    <span class="source">— 达芬奇</span>
    <span class="context">文艺复兴笔记</span>
  </div>
</div>
```

---

### M06 — Comparison

| Field | Value |
|-------|-------|
| **Name** | Comparison |
| **Best for** | 对比分析、二选一、前后对照 |
| **Structure** | 双栏张力布局 → 简洁标签 → 视觉锚点 |

```html
<div class="card frame m06-comparison">
  <h2 class="title-serif">选择</h2>
  <div class="compare-columns">
    <div class="col left">
      <div class="image-well"><img src="…" style="object-fit:cover;object-position:center 50%"></div>
      <span class="label">方案 A</span>
      <p>轻量、快速</p>
    </div>
    <div class="col right">
      <div class="image-well"><img src="…" style="object-fit:cover;object-position:center 50%"></div>
      <span class="label">方案 B</span>
      <p>稳健、全面</p>
    </div>
  </div>
</div>
```

---

### M07 — Field Ledger

| Field | Value |
|-------|-------|
| **Name** | Field Ledger |
| **Best for** | 表格式信息、属性清单、规格对比 |
| **Structure** | 编辑式标题 → 账本行（标题列 + 备注列） |

```html
<div class="card frame m07-ledger">
  <header class="editorial-header">
    <span class="overline">规格</span>
    <h2 class="title-serif">材料清单</h2>
  </header>
  <div class="ledger-rows">
    <div class="row"><span class="title-col">木材</span><span class="note-col">白橡木 · 2m</span></div>
    <div class="row"><span class="title-col">五金</span><span class="note-col">黄铜铰链 ×4</span></div>
    <div class="row"><span class="title-col">涂料</span><span class="note-col">哑光清漆</span></div>
    <div class="row"><span class="title-col">胶水</span><span class="note-col">木工白胶 500ml</span></div>
  </div>
</div>
```

---

### M08 — Pipeline Vertical

| Field | Value |
|-------|-------|
| **Name** | Pipeline Vertical |
| **Best for** | 流程步骤、工作流、阶段展示 |
| **Structure** | 垂直步骤管道 → step-nb + step-title + step-desc |

```html
<div class="card frame m08-pipeline">
  <h2 class="title-serif">制作流程</h2>
  <div class="pipeline-steps">
    <div class="step">
      <span class="step-nb">01</span>
      <div class="step-content">
        <span class="step-title">选材</span>
        <span class="step-desc">挑选纹理均匀的白橡木</span>
      </div>
    </div>
    <div class="step">
      <span class="step-nb">02</span>
      <div class="step-content">
        <span class="step-title">切割</span>
        <span class="step-desc">按图纸精确下料</span>
      </div>
    </div>
    <div class="step">
      <span class="step-nb">03</span>
      <div class="step-content">
        <span class="step-title">组装</span>
        <span class="step-desc">榫卯结构拼接</span>
      </div>
    </div>
    <div class="step">
      <span class="step-nb">04</span>
      <div class="step-content">
        <span class="step-title">打磨</span>
        <span class="step-desc">从 80 目到 400 目逐级打磨</span>
      </div>
    </div>
  </div>
</div>
```

---

### M09 — Marginalia Essay

| Field | Value |
|-------|-------|
| **Name** | Marginalia Essay |
| **Best for** | 学术随笔、注释式阅读、深度笔记 |
| **Structure** | 主栏 + 旁注栏 → 衬线正文 |

```html
<div class="card frame m09-marginalia">
  <div class="main-column">
    <h2 class="title-serif">论手艺的消逝</h2>
    <p class="body-serif">手艺不仅是一种技能，更是一种与材料对话的方式。当机器取代了手，我们失去的不只是效率……</p>
  </div>
  <aside class="marginalia">
    <p class="note">手艺 (craft) 源自古英语 cræft，意为力量与技巧</p>
    <p class="note">参见 Richard Sennett《匠人》</p>
  </aside>
</div>
```

---

### M10 — Atmosphere Thesis

| Field | Value |
|-------|-------|
| **Name** | Atmosphere Thesis |
| **Best for** | 氛围感宣言、品牌主张、情绪页 |
| **Structure** | 大字陈述 + 氛围背景图 → 极少文字 |

```html
<div class="card frame m10-atmosphere">
  <div class="atmosphere-bg">
    <img src="…" style="object-fit:cover;object-position:center 50%">
  </div>
  <div class="thesis-overlay">
    <h1 class="title-serif">少即是多</h1>
    <p class="subtitle">Less, but better.</p>
  </div>
</div>
```

---

### M11 — Photo Grid

| Field | Value |
|-------|-------|
| **Name** | Photo Grid |
| **Best for** | 多图展示、作品集、场景合集 |
| **Structure** | 2×2 或 3×2 照片网格 + 说明文字 |

```html
<div class="card frame m11-photo-grid">
  <h2 class="title-serif">空间记录</h2>
  <div class="photo-grid cols-2x2">
    <figure><img src="…" style="object-fit:cover;object-position:center 50%"><figcaption>客厅</figcaption></figure>
    <figure><img src="…" style="object-fit:cover;object-position:center 50%"><figcaption>书房</figcaption></figure>
    <figure><img src="…" style="object-fit:cover;object-position:center 50%"><figcaption>厨房</figcaption></figure>
    <figure><img src="…" style="object-fit:cover;object-position:center 50%"><figcaption>阳台</figcaption></figure>
  </div>
</div>
```

---

### M12 — Data Cards

| Field | Value |
|-------|-------|
| **Name** | Data Cards |
| **Best for** | 数据展示、KPI 概览、统计摘要 |
| **Structure** | 2×2 或 2×3 数据卡片 → 数字 + 标签 |

```html
<div class="card frame m12-data-cards">
  <h2 class="title-serif">年度数据</h2>
  <div class="data-grid cols-2x2">
    <div class="data-card"><span class="number">128</span><span class="label">项目完成</span></div>
    <div class="data-card"><span class="number">4.9</span><span class="label">客户评分</span></div>
    <div class="data-card"><span class="number">36</span><span class="label">团队成员</span></div>
    <div class="data-card"><span class="number">99%</span><span class="label">按时交付</span></div>
  </div>
</div>
```

---

### M13 — Timeline Vertical

| Field | Value |
|-------|-------|
| **Name** | Timeline Vertical |
| **Best for** | 时间线、发展历程、里程碑 |
| **Structure** | 垂直时间轴 → 节点 + 日期 + 描述 |

```html
<div class="card frame m13-timeline">
  <h2 class="title-serif">发展历程</h2>
  <div class="timeline-nodes">
    <div class="node">
      <span class="dot"></span>
      <div class="node-content">
        <span class="date">2023</span>
        <span class="desc">项目启动</span>
      </div>
    </div>
    <div class="node">
      <span class="dot"></span>
      <div class="node-content">
        <span class="date">2024</span>
        <span class="desc">首版发布</span>
      </div>
    </div>
    <div class="node">
      <span class="dot"></span>
      <div class="node-content">
        <span class="date">2025</span>
        <span class="desc">用户突破 10 万</span>
      </div>
    </div>
    <div class="node">
      <span class="dot"></span>
      <div class="node-content">
        <span class="date">2026</span>
        <span class="desc">全球化运营</span>
      </div>
    </div>
  </div>
</div>
```

---

### M14 — Before / After

| Field | Value |
|-------|-------|
| **Name** | Before / After |
| **Best for** | 改造对比、效果展示、优化前后 |
| **Structure** | 分割对比 → 中间分隔线 |

```html
<div class="card frame m14-before-after">
  <h2 class="title-serif">改造前后</h2>
  <div class="split-compare">
    <div class="half before">
      <img src="…" style="object-fit:cover;object-position:center 50%">
      <span class="label">Before</span>
    </div>
    <div class="divider"></div>
    <div class="half after">
      <img src="…" style="object-fit:cover;object-position:center 50%">
      <span class="label">After</span>
    </div>
  </div>
</div>
```

---

### M15 — Full-Bleed Image

| Field | Value |
|-------|-------|
| **Name** | Full-Bleed Image |
| **Best for** | 视觉冲击页、作品展示、氛围图 |
| **Structure** | 图片覆盖 80%+ → 文字叠加安全区 |

```html
<div class="card frame m15-full-bleed">
  <div class="full-image">
    <img src="…" style="object-fit:cover;object-position:center 50%">
  </div>
  <div class="text-safe-zone">
    <h2 class="title-serif">光与影</h2>
    <p class="caption">建筑摄影系列 · 第三章</p>
  </div>
</div>
```

---

### M16 — Closing / CTA

| Field | Value |
|-------|-------|
| **Name** | Closing / CTA |
| **Best for** | 结尾页、行动号召、关注引导 |
| **Structure** | 结语陈述 → CTA 按钮/链接 → 页脚 |

```html
<div class="card frame m16-closing">
  <div class="closing-content">
    <h2 class="title-serif">感谢阅读</h2>
    <p class="body">如果这篇文章对你有帮助，欢迎关注获取更多内容。</p>
    <a class="cta-button" href="#">关注我</a>
  </div>
  <footer class="card-footer">
    <span>@作者名</span>
    <span>Vol.03 · 2026</span>
  </footer>
</div>
```

---

## Swiss International Recipes

### S01 — Index Cover

| Field | Value |
|-------|-------|
| **Name** | Index Cover |
| **Best for** | 索引封面、目录页、系列开篇 |
| **Structure** | 大号无衬线标题 weight 200 → 强调元素 → 类目标签 |

```html
<div class="card frame s01-index">
  <h1 class="title-sans weight-200">知识<br>管理<br>手册</h1>
  <div class="accent-element"></div>
  <div class="category-labels">
    <span>工具</span><span>方法</span><span>实践</span>
  </div>
</div>
```

---

### S02 — Vertical Timeline + KPI

| Field | Value |
|-------|-------|
| **Name** | Vertical Timeline + KPI |
| **Best for** | 时间线 + 关键指标、发展历程 + 数据 |
| **Structure** | 时间轴节点 → KPI 数字 |

```html
<div class="card frame s02-timeline-kpi">
  <div class="timeline-column">
    <div class="node"><span class="dot"></span><span class="date">Q1</span><span class="desc">上线</span></div>
    <div class="node"><span class="dot"></span><span class="date">Q2</span><span class="desc">增长</span></div>
    <div class="node"><span class="dot"></span><span class="date">Q3</span><span class="desc">扩展</span></div>
    <div class="node"><span class="dot"></span><span class="date">Q4</span><span class="desc">盈利</span></div>
  </div>
  <div class="kpi-column">
    <div class="kpi"><span class="number">10K</span><span class="label">用户</span></div>
    <div class="kpi"><span class="number">¥2M</span><span class="label">营收</span></div>
    <div class="kpi"><span class="number">98%</span><span class="label">留存</span></div>
  </div>
</div>
```

---

### S03 — Split Statement

| Field | Value |
|-------|-------|
| **Name** | Split Statement |
| **Best for** | 观点 + 论据、主张 + 证据 |
| **Structure** | 左右分栏 → 陈述 + 证据 |

```html
<div class="card frame s03-split-statement">
  <div class="left-statement">
    <h2 class="title-sans">设计即沟通</h2>
    <p>每一个像素都在传递信息。</p>
  </div>
  <div class="right-evidence">
    <div class="evidence-item"><span class="number">73%</span><span class="label">用户首先注意视觉</span></div>
    <div class="evidence-item"><span class="number">2.6s</span><span class="label">平均首屏停留</span></div>
    <div class="evidence-item"><span class="number">4.2×</span><span class="label">好设计提升转化</span></div>
  </div>
</div>
```

---

### S04 — Six Cells

| Field | Value |
|-------|-------|
| **Name** | Six Cells |
| **Best for** | 矩阵展示、功能罗列、分类概览 |
| **Structure** | 2×3 或 3×2 卡片填充矩阵 |

```html
<div class="card frame s04-six-cells">
  <h2 class="title-sans">核心能力</h2>
  <div class="cell-grid cols-2x3">
    <div class="cell"><span class="icon">📝</span><span class="label">写作</span></div>
    <div class="cell"><span class="icon">🎨</span><span class="label">设计</span></div>
    <div class="cell"><span class="icon">📊</span><span class="label">数据</span></div>
    <div class="cell"><span class="icon">🔧</span><span class="label">工程</span></div>
    <div class="cell"><span class="icon">📈</span><span class="label">增长</span></div>
    <div class="cell"><span class="icon">🤝</span><span class="label">协作</span></div>
  </div>
</div>
```

---

### S05 — Three Layers

| Field | Value |
|-------|-------|
| **Name** | Three Layers |
| **Best for** | 架构图、层级关系、系统分层 |
| **Structure** | 三层架构图 |

```html
<div class="card frame s05-three-layers">
  <h2 class="title-sans">系统架构</h2>
  <div class="layers">
    <div class="layer top"><span class="layer-name">表现层</span><span class="layer-desc">UI / 交互</span></div>
    <div class="layer mid"><span class="layer-name">逻辑层</span><span class="layer-desc">业务 / API</span></div>
    <div class="layer bot"><span class="layer-name">数据层</span><span class="layer-desc">存储 / 缓存</span></div>
  </div>
</div>
```

---

### S06 — KPI Tower

| Field | Value |
|-------|-------|
| **Name** | KPI Tower |
| **Best for** | 关键指标展示、数据对比、仪表盘 |
| **Structure** | 4 个 KPI 柱状条 → 不同高度 |

```html
<div class="card frame s06-kpi-tower">
  <h2 class="title-sans">季度表现</h2>
  <div class="tower-bars">
    <div class="bar" style="height:45%"><span class="number">45%</span><span class="label">Q1</span></div>
    <div class="bar" style="height:62%"><span class="number">62%</span><span class="label">Q2</span></div>
    <div class="bar" style="height:78%"><span class="number">78%</span><span class="label">Q3</span></div>
    <div class="bar" style="height:95%"><span class="number">95%</span><span class="label">Q4</span></div>
  </div>
</div>
```

---

### S07 — H-Bar Chart

| Field | Value |
|-------|-------|
| **Name** | H-Bar Chart |
| **Best for** | 排名、对比、水平柱状图 |
| **Structure** | 5-10 条水平柱 → 排名展示 |

```html
<div class="card frame s07-hbar">
  <h2 class="title-sans">语言流行度</h2>
  <div class="hbar-rows">
    <div class="hbar-row"><span class="label">Python</span><div class="bar" style="width:92%"></div><span class="value">92</span></div>
    <div class="hbar-row"><span class="label">JavaScript</span><div class="bar" style="width:87%"></div><span class="value">87</span></div>
    <div class="hbar-row"><span class="label">TypeScript</span><div class="bar" style="width:74%"></div><span class="value">74</span></div>
    <div class="hbar-row"><span class="label">Rust</span><div class="bar" style="width:58%"></div><span class="value">58</span></div>
    <div class="hbar-row"><span class="label">Go</span><div class="bar" style="width:51%"></div><span class="value">51</span></div>
  </div>
</div>
```

---

### S08 — Duo Compare

| Field | Value |
|-------|-------|
| **Name** | Duo Compare |
| **Best for** | 前后对比、方案对比、双栏对照 |
| **Structure** | 前后/左右对比 → 中间竖线分隔 |

```html
<div class="card frame s08-duo-compare">
  <h2 class="title-sans">优化效果</h2>
  <div class="duo-columns">
    <div class="duo-col before">
      <span class="label">优化前</span>
      <span class="number">3.2s</span>
      <span class="desc">加载时间</span>
    </div>
    <div class="vertical-rule"></div>
    <div class="duo-col after">
      <span class="label">优化后</span>
      <span class="number">0.8s</span>
      <span class="desc">加载时间</span>
    </div>
  </div>
</div>
```

---

### S09 — Dot Matrix Statement

| Field | Value |
|-------|-------|
| **Name** | Dot Matrix Statement |
| **Best for** | 宣言、主张、品牌声明 |
| **Structure** | 大字陈述 + 点阵背景 |

```html
<div class="card frame s09-dot-matrix">
  <div class="dot-matrix-bg"></div>
  <div class="statement">
    <h1 class="title-sans">做减法</h1>
    <p>去掉一切不必要的，留下真正重要的。</p>
  </div>
</div>
```

---

### S10 — Split Closing

| Field | Value |
|-------|-------|
| **Name** | Split Closing |
| **Best for** | 结尾页、分栏收束、CTA |
| **Structure** | 分栏收尾布局 |

```html
<div class="card frame s10-split-closing">
  <div class="left-close">
    <h2 class="title-sans">下期见</h2>
    <p>每周更新，持续精进。</p>
  </div>
  <div class="right-close">
    <a class="cta-button" href="#">关注</a>
    <a class="cta-link" href="#">往期回顾 →</a>
  </div>
</div>
```

---

### S11 — Horizontal Timeline

| Field | Value |
|-------|-------|
| **Name** | Horizontal Timeline |
| **Best for** | 水平流程、步骤展示、阶段推进 |
| **Structure** | 4-7 步水平流程 → 节点 + 连线 |

```html
<div class="card frame s11-h-timeline">
  <h2 class="title-sans">项目阶段</h2>
  <div class="h-timeline">
    <div class="step"><span class="dot"></span><span class="label">调研</span></div>
    <div class="connector"></div>
    <div class="step"><span class="dot"></span><span class="label">设计</span></div>
    <div class="connector"></div>
    <div class="step"><span class="dot"></span><span class="label">开发</span></div>
    <div class="connector"></div>
    <div class="step"><span class="dot"></span><span class="label">测试</span></div>
    <div class="connector"></div>
    <div class="step"><span class="dot"></span><span class="label">发布</span></div>
  </div>
</div>
```

---

### S12 — Manifesto + Accent Banner

| Field | Value |
|-------|-------|
| **Name** | Manifesto + Accent Banner |
| **Best for** | 宣言页、品牌主张、信条展示 |
| **Structure** | 宣言文字 + 强调色横幅 |

```html
<div class="card frame s12-manifesto">
  <div class="manifesto-text">
    <p class="title-sans">我们相信</p>
    <p>好的工具应该让人更自由，而非更忙碌。</p>
    <p>好的设计应该减少选择，而非增加焦虑。</p>
    <p>好的产品应该安静地工作，而非喧哗地存在。</p>
  </div>
  <div class="accent-banner">
    <span>Less, but better.</span>
  </div>
</div>
```
