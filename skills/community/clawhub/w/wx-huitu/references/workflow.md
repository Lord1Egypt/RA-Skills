# wx-huitu 核心工作流

> 版本: 2.0 | 输出格式: HTML → Puppeteer 截图 → PNG 交付
> 触发词: `文章绘图` / `绘图图表` / `画个图表` / `数据图` / `做个图` / `画图`

## Core Principles

1. **Think first, plot second** — 先剖析数据形态和论证意图，再选图型
2. **主动拦截不当选择** — 发现问题先说再给替代，不默默照做
3. **色盲安全默认** — Okabe-Ito 配色 + 冗余编码
4. **一图一论点** — 一张图表只承载一个核心论证目标

## 执行流程

```
输入（文章/数据描述/CSV）
  ↓
Step 1: 数据剖析（静默）
  ↓
Step 2: 图型推荐 ← 确认点（必须）
  ↓
Step 3: 风格 + 生成 HTML
  ↓
Step 4: 截图交付 + 云盘同步
```

---

## Step 1: 数据剖析（静默）

### 三轴分析

对每个提取到的数据单元，分析三个维度：

**轴1: 变量类型**

| 组合 | 数据结构 |
|------|---------|
| 1×连续 | 看分布 |
| 1×分类 | 看占比 |
| 1×分类 + 1×连续 | 看组间比较 |
| 2×连续 | 看关系 |
| 1×时间 + 1×连续 | 看趋势 |
| 多个连续 | 看相关 |
| 二维矩阵 | 看模式 |
| 嵌套分组 | 看层次 |

**轴2: 论证意图**

**这是最容易被忽略的一轴。** 同样数据，论证目标不同，图就不同。

- **比较** — "A 比 B 高/低/不同" → bar-chart / h-bar-chart
- **趋势** — "随时间/条件变化" → line-chart
- **占比** — "总和被分成几份" → donut-chart / treemap
- **关系** — "X 越大 Y 越大" → scatter-plot / bubble-chart
- **流程** — "A→B→C 顺序步骤" → flow-chart / swimlane-chart
- **层级** — "上下级/嵌套结构" → tree-chart / layered-diagram
- **重叠** — "集合之间有交集" → venn-diagram
- **累积** — "正负贡献叠加" → waterfall-chart

**轴3: 数据形态**

- 数据点数量（2-5 / 6-12 / 13+）
- 类别数量（2-5 / 6-8 / 9+）
- 是否有分组
- 是否有异常值
- 是否跨量级

### 从文章提取数据单元

| 提取信号 | 寻找什么 | 论证意图 |
|---------|---------|---------|
| 数值比较 | "A占X%，B占Y%" | 比较 |
| 时间变化 | "从X增长到Y"/"逐年/逐月" | 趋势 |
| 占比构成 | "其中X占Y%"/"分为三部分" | 占比 |
| 变量关系 | "X越高Y越"/"正相关/负相关" | 关系 |
| 顺序步骤 | "第一步→第二步"/"Phase1→2" | 流程 |
| 层级结构 | "包含"/"下属"/"分为N类" | 层级 |
| 集合重叠 | "同时属于"/"交集" | 重叠 |
| 累积变化 | "贡献了X"/"减少了Y" | 累积 |

### 提取规则

- 数据单元须有 ≥2个数据点 或 清晰逻辑结构
- 孤立单个数字不可视化（如"48天"单独→不做图）
- 两个单元来源段落重叠时，合并
- 无数据/结构的叙述段落不可视化

---

## Step 2: 图型推荐（确认点 — 必须）

### 推荐格式

```
📊 图表推荐：共 N 张

┌──────────────────────────────────────────────────┐
│ #1 [图型emoji] [图型名称]                          │
│ 论证意图: [比较/趋势/占比/...]                      │
│ 推荐理由: [基于三轴分析的具体理由]                    │
│ 备选: [备选图型1] / [备选图型2]                     │
│                                                    │
│ #2 ...                                             │
└──────────────────────────────────────────────────┘

💡 我的建议:
- [主动给出合并/拆分/调整建议]
- [指出哪张信息密度最高]
```

### 图型Emoji映射

| 图型 | Emoji | 图型 | Emoji |
|------|-------|------|-------|
| bar-chart | 📊 | horizontal-bar-chart | 📏 |
| line-chart | 📈 | donut-chart | 🍩 |
| scatter-plot | 🔵 | bubble-chart | 🫧 |
| flow-chart | 🔀 | swimlane-chart | 🏊 |
| tree-chart | 🌳 | layered-diagram | 🧱 |
| venn-diagram | ⭕ | waterfall-chart | 📉 |
| treemap | 🗺️ | quadrant-chart | ✛ |
| data-billboard | 🔢 | candlestick-chart | 🕯️ |
| state-machine | ⚙️ | | |

### 拦截规则执行

发现用户需求触发拦截时，**先说明问题再给替代方案**：

```
拦截示例：
你要的"3个类别画饼图"会触发 I2（7以下类别虽可画饼图，
但横向柱状图在长度比较上比角度比较更直观）。
我建议改成 **横向柱状图**：长度差异一目了然。
要按原方案画，还是改？
```

尊重用户最终决定，但**留下明确的劝阻记录**。

### 用户覆盖选项

- "确认" → 按推荐执行
- "第N张换成[图型]" → 更换
- "加上[描述]" → 添加
- "合并第M和第N张" → 合并
- "去掉第N张" → 移除

---

## Step 3: 风格 + 生成 HTML

### 1问定风格

```
🎨 主题色偏好？
  A. 克制风（单品牌色+暖灰层级）— 默认
  B. 品牌DNA（自动检测文章来源色）
  C. 高端财经：
     C1. 麦肯锡（深蓝+青绿+暖灰白，克制严谨）
     C2. 经济学人（红+深蓝+米白，英式鲜明）
     C3. 财新（财新蓝+冷灰白，中式精炼）
  D. 指定色系：______
```

> 高端财经配色详见 [`design-tokens.md`](design-tokens.md) 第2节。核心原则：低饱和度、高灰度占比、单色系为主+1个强调色、大面积留白。

### 尺寸体系（三画幅）

| 画幅 | 基准尺寸 | 弹性区间 | 适用图型 |
|------|---------|---------|---------|
| **宽幅** | 640×400 | 360-480px | line-chart, flow-chart, grouped-bar, area-chart |
| **标准** | 640×480 | 420-600px | bar-chart, h-bar-chart, layered-diagram, waterfall-chart, stacked-bar, comparison-table, data-billboard, tree-chart, treemap, swimlane-chart |
| **方版** | 640×640 | 560-720px | donut-chart, quadrant-chart, venn-diagram, scatter-plot, bubble-chart, state-machine |

> 画幅详细映射和弹性规则见 [`design-tokens.md`](design-tokens.md) 第5节。

### HTML 生成规则

1. **内联CSS** — 每个 HTML 文件包含完整样式
2. **`<img>`标签背景** — 照片背景用 `<img>` + 绝对定位，不用 CSS background-image
3. **固定宽高** — `html,body{width:Wpx;height:Hpx;overflow:hidden;margin:0;padding:0}`
4. **overflow:hidden** — 确保截图尺寸精确
5. **Google Fonts @import** — 放在 `<style>` 顶部
6. **命名规范** — `{NN}-{type}.html`

### 输出目录

```
[article-name]-charts/
├── 01-bar-comparison.html
├── 02-line-trend.html
├── 03-donut-share.html
└── screenshot.js
```

### HTML模板骨架

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@200;300;400;500;600;700&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@200;300;400;500;700&display=swap');
:root {
  --ink: #0a0a0a;
  --paper: #fafaf8;
  --accent: #002FA7;
  --muted: #737373;
  --rule: #d4d4d2;
  --surface: #ffffff;
  --surface-2: #f2f2f0;
  --good: #1aaf6c;
  --bad: #e0445a;
  --warn: #f5a524;
  --font-body: 'Noto Sans SC', sans-serif;
  --font-data: 'Inter', 'Noto Sans SC', sans-serif;
  --chart-1: #E69F00;
  --chart-2: #56B4E9;
  --chart-3: #009E73;
  --chart-4: #D55E00;
}
* { margin: 0; padding: 0; box-sizing: border-box; }
.num { font-family: var(--font-data); font-feature-settings: 'tnum' on; letter-spacing: -0.02em; }
html, body { width: 640px; overflow: hidden; font-family: var(--font-body); background: var(--paper); color: var(--ink); }
</style>
</head>
<body>
<!-- 图表内容 -->
</body>
</html>
```

---

## Step 4: 截图交付 + 云盘同步

### Puppeteer-core + 系统Chrome

Chrome路径检测（Windows，按顺序）：
1. 注册表：`HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\chrome.exe`
2. Playwright：`$env:LOCALAPPDATA\ms-playwright\chromium-*\chrome-win64\chrome.exe`
3. 默认：`C:\Program Files\Google\Chrome\Application\chrome.exe`

### 截图参数

| 格式 | Viewport | deviceScaleFactor | 输出 |
|------|----------|-------------------|------|
| 横版 | 640×auto | 2 | PNG |
| 方版 | 640×640 | 2 | PNG |

### screenshot.js

```javascript
const puppeteer = require('puppeteer-core');
const fs = require('fs');
const path = require('path');

function detectChromePath() {
  const { execSync } = require('child_process');
  try {
    const reg = execSync(
      'reg query "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\App Paths\\chrome.exe" /ve',
      { encoding: 'utf-8' }
    );
    const m = reg.match(/REG_SZ\s+(.+)/);
    if (m && fs.existsSync(m[1].trim())) return m[1].trim();
  } catch (_) {}
  const playwrightDir = path.join(process.env.LOCALAPPDATA || '', 'ms-playwright');
  if (fs.existsSync(playwrightDir)) {
    const dirs = fs.readdirSync(playwrightDir).filter(d => d.startsWith('chromium-')).sort().reverse();
    for (const d of dirs) {
      const p = path.join(playwrightDir, d, 'chrome-win64', 'chrome.exe');
      if (fs.existsSync(p)) return p;
    }
  }
  const defaultPath = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';
  if (fs.existsSync(defaultPath)) return defaultPath;
  throw new Error('未找到 Chrome');
}

const TYPE_CONFIG = {
  square: { width: 640, height: 640, fullPage: false },
  default: { width: 640, height: 800, fullPage: true },
};

function isSquare(name) {
  const squareTypes = ['donut','quadrant','venn','treemap','scatter','bubble','billboard'];
  return squareTypes.some(t => name.includes(t));
}

(async () => {
  const chromePath = detectChromePath();
  console.log('Chrome:', chromePath);
  const browser = await puppeteer.launch({
    headless: 'new', executablePath: chromePath,
    args: ['--no-sandbox','--disable-setuid-sandbox','--disable-gpu']
  });
  const scriptDir = __dirname;
  const desktop = path.join(require('os').homedir(), 'Desktop');
  const articleName = path.basename(scriptDir).replace(/-charts$/, '');
  const outputDir = path.join(desktop, articleName + '图表');
  if (!fs.existsSync(outputDir)) fs.mkdirSync(outputDir, { recursive: true });
  const htmlFiles = fs.readdirSync(scriptDir).filter(f => f.endsWith('.html')).sort();
  console.log(`Found ${htmlFiles.length} HTML files`);
  for (const file of htmlFiles) {
    const filePath = path.join(scriptDir, file);
    const sq = isSquare(file);
    const config = sq ? TYPE_CONFIG.square : TYPE_CONFIG.default;
    const pngName = file.replace('.html', '.png');
    const pngPath = path.join(outputDir, pngName);
    console.log(`  ${file} -> ${pngName} (${sq ? '640x640' : '640xauto'})`);
    const page = await browser.newPage();
    await page.setViewport({ width: config.width, height: config.height, deviceScaleFactor: 2 });
    await page.goto('file:///' + filePath.replace(/\\/g, '/'), { waitUntil: 'networkidle0', timeout: 30000 });
    await page.evaluate(() => document.fonts.ready);
    await new Promise(r => setTimeout(r, 3000));
    const opts = { path: pngPath, type: 'png' };
    if (config.fullPage) { opts.fullPage = true; }
    else { opts.clip = { x: 0, y: 0, width: config.width, height: config.height }; }
    await page.screenshot(opts);
    await page.close();
  }
  await browser.close();
  console.log(`Done! Output: ${outputDir}`);
  const { execSync } = require('child_process');
  try { execSync('explorer.exe "' + outputDir + '"'); } catch(e) {}
})();
```

### 交付流程

1. **截图**: 运行 screenshot.js
2. **本地验证**: PNG > 10KB / 中文字符正确 / 标签无裁切
3. **飞书云盘同步**: `lark-cli drive +create-folder` → `lark-cli drive +upload` 逐张上传

### 视觉自检清单

- [ ] 数值标签无裁切
- [ ] 图例不压数据
- [ ] 颜色在灰度下可区分
- [ ] 轴标签可读（640px画布上≥12px）
- [ ] 数据来源已标注
