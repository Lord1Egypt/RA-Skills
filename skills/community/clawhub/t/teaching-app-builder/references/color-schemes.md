# 专业配色方案

6 套为教学场景设计的配色，刻意避开「白底紫渐变」这类 AI 套路色，每套都有明确的语境归属。

## 设计约定（重要）

**所有方案共用同一套变量名**，切换配色只改值不改名，HTML/JS 里对颜色的引用永远稳定。选定一套后，把它的 `:root` 块整段贴进 `<style>` 即可。

变量语义：

| 变量 | 含义 | 变量 | 含义 |
|---|---|---|---|
| `--bg` | 页面底色 | `--primary` | 主色（导航/按钮/强调标题） |
| `--surface` | 卡片/面板底 | `--primary-weak` | 主色淡背景（高亮块、选中态底） |
| `--surface-2` | 更深/更浅一档的面 | `--accent` | 点缀色（与主色对比，少量用） |
| `--fg` | 正文文字 | `--success` `--warning` `--danger` | 语义色 |
| `--fg-muted` | 次要文字 | `--chart-1..6` | 图表定性色板 |
| `--border` | 描边/分隔线 | | |

**配色使用纪律**（决定专业感的关键，比选哪套更重要）：
- **60-30-10**：60% 中性面（bg/surface）、30% 文字、10% 主色+点缀。主色和 accent 是「盐」，大面积铺就廉价了。
- 正文永远用 `--fg`，不要给大段文字上彩色。
- accent 只用在「最该被一眼看到」的一个东西上（当前步骤、关键结论、唯一 CTA）。
- 暗色方案下，纯白 `#fff` 文字太刺眼，用 `--fg`（略带灰/蓝）。亮色方案下别用纯黑，用 `--fg`（深灰）。
- 大色块之间留白和描边比额外加颜色更能提升质感。

## 共享排版变量（任选配色都先贴这段）

```css
:root {
  /* 字体栈：纯系统字体，不依赖外网，中英文混排都好看 */
  --font-sans: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC',
               'Hiragino Sans GB', 'Microsoft YaHei', 'Source Han Sans SC', sans-serif;
  --font-serif: Georgia, 'Times New Roman', 'Songti SC', 'STSong', 'SimSun', serif;
  --font-mono: 'SF Mono', 'JetBrains Mono', 'Cascadia Code', Consolas, 'Courier New', monospace;
  /* 间距尺度 */
  --space-1: 4px; --space-2: 8px; --space-3: 12px; --space-4: 16px;
  --space-5: 24px; --space-6: 32px; --space-8: 48px;
  /* 圆角 / 阴影 */
  --radius: 10px; --radius-sm: 6px; --radius-lg: 16px;
  --shadow: 0 1px 3px rgba(0,0,0,.08), 0 6px 24px rgba(0,0,0,.06);
  --shadow-lg: 0 8px 40px rgba(0,0,0,.12);
  --maxw: 1080px; /* 内容主区最大宽度，长文教学别铺满屏 */
}
```
> 暗色方案的阴影更弱、靠 border 区分层级；可把 `--shadow` 改为 `0 1px 2px rgba(0,0,0,.4)`。

---

## 1. 深空蓝 Midnight Scholar（暗色）

**适合**：理工、数据科学、物理、工程、算法可视化、任何「严肃 + 科技感」的内容。耐看不刺眼，长时间盯着舒服。

```css
:root {
  --bg: #0b1120;        --surface: #141d33;   --surface-2: #1c2742;
  --fg: #e6edf7;        --fg-muted: #93a4c0;  --border: #263149;
  --primary: #4f9dff;   --primary-weak: rgba(79,157,255,.12);
  --accent: #22d3ee;
  --success: #34d399;   --warning: #fbbf24;   --danger: #f87171;
  --chart-1:#4f9dff; --chart-2:#22d3ee; --chart-3:#a78bfa;
  --chart-4:#fbbf24; --chart-5:#f472b6; --chart-6:#34d399;
  --shadow: 0 1px 2px rgba(0,0,0,.5), 0 8px 30px rgba(0,0,0,.35);
}
```

## 2. 学术纸张 Academic Paper（亮色）

**适合**：人文、社科、文献研读、概念讲解、阅读密集型。米白纸感 + 墨蓝 + 赭金，像一本印制讲究的教科书。配 `--font-serif` 标题尤其有气质。

```css
:root {
  --bg: #faf7f0;        --surface: #ffffff;   --surface-2: #f3eee3;
  --fg: #23282d;        --fg-muted: #6b7280;  --border: #e6dfd1;
  --primary: #1f4e79;   --primary-weak: rgba(31,78,121,.08);
  --accent: #b45309;
  --success: #15803d;   --warning: #b45309;   --danger: #b91c1c;
  --chart-1:#1f4e79; --chart-2:#b45309; --chart-3:#6b8e6b;
  --chart-4:#8d6e97; --chart-5:#c97b56; --chart-6:#4a7a8c;
}
```

## 3. 清新薄荷 Fresh Mint（亮色）

**适合**：K12、科普、生物医学、自然科学、面向年轻学习者。teal 主色干净友好，暖橙做点缀提精神。

```css
:root {
  --bg: #f4fbf8;        --surface: #ffffff;   --surface-2: #e7f5ef;
  --fg: #15302b;        --fg-muted: #5e7a73;  --border: #d4ece4;
  --primary: #0d9488;   --primary-weak: rgba(13,148,136,.10);
  --accent: #f59e0b;
  --success: #16a34a;   --warning: #f59e0b;   --danger: #e11d48;
  --chart-1:#0d9488; --chart-2:#34a0a4; --chart-3:#76c893;
  --chart-4:#f59e0b; --chart-5:#ef767a; --chart-6:#577590;
}
```

## 4. 暖阳赭橙 Warm Ochre（亮色）

**适合**：历史、文学、语言、艺术、传统文化。赤陶 + 麦黄的暖调，配少量青做冷暖平衡，温润有人情味。

```css
:root {
  --bg: #fdf6ea;        --surface: #fffbf4;   --surface-2: #f7ead6;
  --fg: #382c22;        --fg-muted: #8a7560;  --border: #ecdcc4;
  --primary: #c2410c;   --primary-weak: rgba(194,65,12,.09);
  --accent: #0e7490;
  --success: #4d7c0f;   --warning: #ca8a04;   --danger: #9f1239;
  --chart-1:#c2410c; --chart-2:#ca8a04; --chart-3:#4d7c0f;
  --chart-4:#0e7490; --chart-5:#9f1239; --chart-6:#7c4a2d;
}
```

## 5. 靛青商务 Indigo Pro（亮色）

**适合**：商务、管理、经济、金融、职业培训、企业内训。靛蓝 + 石板灰，干净克制、可信，最「安全」的通用专业感。

```css
:root {
  --bg: #f8fafc;        --surface: #ffffff;   --surface-2: #eef2f7;
  --fg: #1e293b;        --fg-muted: #64748b;  --border: #e2e8f0;
  --primary: #4338ca;   --primary-weak: rgba(67,56,202,.08);
  --accent: #0891b2;
  --success: #059669;   --warning: #d97706;   --danger: #dc2626;
  --chart-1:#4338ca; --chart-2:#0891b2; --chart-3:#7c3aed;
  --chart-4:#db2777; --chart-5:#ea580c; --chart-6:#16a34a;
}
```

## 6. 暗夜霓虹 Neon Dark（暗色）

**适合**：计算机、网络安全、前沿科技、黑客松、需要「酷 / 吸睛」的演示。品红 + 青绿霓虹，注意克制——霓虹色只点在交互高亮上，铺多了廉价。

```css
:root {
  --bg: #0a0a12;        --surface: #15151f;   --surface-2: #1e1e2e;
  --fg: #e8e8f2;        --fg-muted: #8a8aa3;  --border: #2b2b3d;
  --primary: #d946ef;   --primary-weak: rgba(217,70,239,.12);
  --accent: #2dd4bf;
  --success: #4ade80;   --warning: #facc15;   --danger: #fb7185;
  --chart-1:#d946ef; --chart-2:#2dd4bf; --chart-3:#818cf8;
  --chart-4:#facc15; --chart-5:#fb7185; --chart-6:#38bdf8;
}
```

---

## 让图表库吃这套变量

CSS 变量不能直接写进 Chart.js/ECharts 的配置（它们要具体色值字符串），用 JS 把变量读出来：

```js
const css = getComputedStyle(document.documentElement);
const C = n => css.getPropertyValue(`--chart-${n}`).trim();
const palette = [C(1), C(2), C(3), C(4), C(5), C(6)];
const fg = css.getPropertyValue('--fg').trim();
const grid = css.getPropertyValue('--border').trim();

// Chart.js：全局默认色，省得每个 dataset 单独配
Chart.defaults.color = fg;
Chart.defaults.borderColor = grid;
// dataset 用 backgroundColor: palette
```

- **Mermaid**：用 `mermaid.initialize({ theme:'base', themeVariables:{ primaryColor:'…', lineColor:'…', textColor:'…' }})`，把这几个关键变量填成本方案的色值，图就和页面一致了。暗色方案可直接 `theme:'dark'` 起步再微调。
- **ECharts**：在 `option` 里设 `color: palette`，`textStyle.color: fg`，坐标轴 `axisLine`/`splitLine` 用 `--border`。
- **KaTeX 公式**：默认继承文字色，暗色方案下自动是浅色，无需额外处理。

## 配深浅切换（可选）

若要一个明暗切换按钮，把两套 `:root` 分别挂在 `:root` 和 `:root[data-theme="dark"]` 上，按钮切 `document.documentElement.dataset.theme`。一般教学 app 选定一套即可，不必都做。
