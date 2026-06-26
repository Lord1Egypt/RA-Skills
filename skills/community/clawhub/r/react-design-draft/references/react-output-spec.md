# React 4-Piece Output Specification

## Overview

Every design draft outputs exactly 4 types of files. No more, no less.

```
project/
├── design-tokens.css    ← Design system (single source of truth)
├── data.js              ← All display data (structured)
├── components/
│   ├── Header.jsx       ← One component per file
│   ├── Card.jsx
│   ├── ComparisonBlock.jsx
│   └── ...              ← As many as needed
└── App.jsx              ← Composition root
```

## File 1: design-tokens.css

**Purpose**: Single source of truth for all visual values. Change once, update everywhere.

**Required variable groups**:

```css
:root {
  /* === Color Palette === */
  --color-bg-primary: #FAFAF8;
  --color-bg-secondary: #F0EDE6;
  --color-bg-card: #FFFFFF;
  --color-text-primary: #1A1A1A;
  --color-text-secondary: #666666;
  --color-text-muted: #999999;
  --color-accent-1: #3B82F6;
  --color-accent-2: #10B981;
  --color-accent-3: #F59E0B;
  --color-accent-4: #EF4444;
  --color-border: #E5E5E5;

  /* === Typography === */
  --font-display: 'Playfair Display', serif;
  --font-body: 'Source Sans 3', sans-serif;
  --font-mono: 'JetBrains Mono', monospace;
  --text-hero: 48px;
  --text-h1: 32px;
  --text-h2: 24px;
  --text-h3: 20px;
  --text-body: 16px;
  --text-small: 14px;
  --text-caption: 12px;
  --leading-tight: 1.2;
  --leading-normal: 1.5;
  --leading-relaxed: 1.7;

  /* === Spacing (4px scale) === */
  --space-1: 4px;
  --space-2: 8px;
  --space-3: 12px;
  --space-4: 16px;
  --space-6: 24px;
  --space-8: 32px;
  --space-12: 48px;
  --space-16: 64px;

  /* === Shape === */
  --radius-sm: 4px;
  --radius-md: 8px;
  --radius-lg: 12px;
  --radius-xl: 16px;
  --radius-full: 9999px;

  /* === Shadow === */
  --shadow-sm: 0 1px 2px rgba(0,0,0,0.05);
  --shadow-md: 0 4px 6px rgba(0,0,0,0.07);
  --shadow-lg: 0 10px 15px rgba(0,0,0,0.1);

  /* === Transition === */
  --transition-fast: 150ms ease;
  --transition-normal: 250ms ease;
  --transition-slow: 350ms ease;
}
```

**Rules**:
- All values must reference CSS variables, never hardcode in components
- Color palette must have at least: bg-primary, bg-secondary, bg-card, text-primary, text-secondary, text-muted, 2-4 accents, border
- Fonts: 1 display + 1 body + 1 mono (never Inter/Roboto/Arial/system-ui)
- Spacing must follow the 4px scale

## File 2: data.js

**Purpose**: All display data in one place. Components import from here.

**Structure**:

```javascript
// data.js

export const siteConfig = {
  title: "Page Title",
  subtitle: "Page subtitle or tagline",
  theme: "infographic-poster", // matches aesthetic direction
};

export const sections = [
  {
    id: "section-1",
    type: "enumeration", // enumeration / comparison / process / data / hierarchy / timeline
    title: "Section Title",
    items: [
      {
        id: "item-1",
        index: 1,
        title: "Item Title",
        description: "Item description text",
        accent: "accent-1", // references CSS variable
        // type-specific fields:
        htmlDesc: "HTML approach description",
        reactDesc: "React approach description",
      },
    ],
  },
];

export const comparisons = [
  {
    id: "comp-1",
    sideA: { label: "HTML", points: ["..."], icon: "📄" },
    sideB: { label: "React", points: ["..."], icon: "⚛️" },
  },
];
```

**Rules**:
- Every data item must have `id` and `title`
- Use arrays for lists, objects for single items
- Reference accent colors by variable name (e.g., `"accent-1"`), not hex values
- No HTML/JSX in data — only plain text and structured values
- Export each data group as a named export

## File 3: components/*.jsx

**Purpose**: One file per component. Each component is self-contained.

**Component template**:

```jsx
// components/Card.jsx
import { sections } from '../data';

export function Card({ item }) {
  return (
    <article className="card">
      <span className="card__badge">{item.index}</span>
      <h3 className="card__title">{item.title}</h3>
      <p className="card__desc">{item.description}</p>
    </article>
  );
}
```

**Rules**:
- Each component in its own file
- Component name = PascalCase = filename
- Import data from `../data.js`, never hardcode
- Use BEM-style class naming: `block__element--modifier`
- All visual values reference CSS variables via `var(--token-name)`
- Props: receive data items, not the entire data array
- Keep components focused: one visual concern per component
- Add `aria-label` to icon-only elements
- Use semantic HTML: `<article>`, `<section>`, `<nav>`, `<header>`, `<footer>`

**Common component types**:

| Component | Props | Used When |
|-----------|-------|-----------|
| `Header` | siteConfig | Always (page title area) |
| `Card` | item | Enumeration items |
| `ComparisonBlock` | comparison | Comparison sections |
| `StepCard` | step, index | Process steps |
| `StatCard` | metric | Data/KPI display |
| `TreeNode` | node | Hierarchy display |
| `TimelineNode` | event | Timeline events |
| `Footer` | siteConfig | Always (page footer) |

## File 4: App.jsx

**Purpose**: Composition root. Defines the component tree and page layout.

**Template**:

```jsx
// App.jsx
import './design-tokens.css';
import { siteConfig, sections } from './data';
import { Header } from './components/Header';
import { Card } from './components/Card';
import { Footer } from './components/Footer';

export default function App() {
  return (
    <div className="app">
      <Header config={siteConfig} />
      <main className="app__content">
        {sections.map(section => (
          <section key={section.id} className="app__section">
            <h2 className="app__section-title">{section.title}</h2>
            <div className="app__grid">
              {section.items.map(item => (
                <Card key={item.id} item={item} />
              ))}
            </div>
          </section>
        ))}
      </main>
      <Footer config={siteConfig} />
    </div>
  );
}
```

**Rules**:
- Import and compose all components
- Import `design-tokens.css` at the top
- Import all data from `data.js`
- Layout CSS lives in App.jsx (grid, page structure)
- Component-specific CSS lives in each component file
- Use `.map()` to render lists, always with `key={item.id}`
- Add layout comments: `/* === Grid Layout === */`

## Output Format

Present each file as a code block with filename header:

````markdown
### design-tokens.css

```css
:root { ... }
```

### data.js

```javascript
export const siteConfig = { ... };
```

### components/Header.jsx

```jsx
import { siteConfig } from '../data';
...
```

### App.jsx

```jsx
import './design-tokens.css';
...
```
````

## Adaptive Font Size Rules (自适应字号)

Font sizes must adapt to content length, not stay fixed. A title that overflows its container is worse than a slightly smaller title that fits.

### Title Length → Size Mapping

| Title Length | Chinese chars | Size (640px canvas) | Weight | Line Clamp |
|-------------|--------------|---------------------|--------|-----------|
| Short (1-6 chars) | ≤6 | 56-72px | 200-400 | 1 line |
| Medium (7-14 chars) | 7-14 | 40-52px | 300-500 | 1-2 lines |
| Long (15-24 chars) | 15-24 | 28-36px | 400-500 | 2 lines |
| Extended (25+ chars) | 25+ | 22-28px | 500 | 2-3 lines |

### Dynamic Adjustment Rules

1. **Never overflow**: If text overflows its container at the planned size, reduce size by one tier first, then add `line-clamp` as fallback
2. **Minimum readable size**: On 640px canvas, minimum body text = 14px, minimum caption = 10px
3. **Number emphasis**: Data numbers in metric cards always use the largest size tier regardless of length (e.g., "$186.74亿" at 48px even though it's 9 chars)
4. **CJK line-break**: Chinese text breaks at any character boundary. Do NOT rely on space-based word-break
5. **Line-height scales with size**: Display (1.1-1.2), Body (1.5-1.6), Caption (1.3-1.4)

### Implementation in React

```jsx
// Utility: adaptive title size
function getTitleStyle(text, baseSize = 56) {
  const len = text.length;
  if (len <= 6) return { fontSize: baseSize, fontWeight: 300, lineHeight: 1.15 };
  if (len <= 14) return { fontSize: baseSize * 0.72, fontWeight: 400, lineHeight: 1.2 };
  if (len <= 24) return { fontSize: baseSize * 0.52, fontWeight: 500, lineHeight: 1.3 };
  return { fontSize: baseSize * 0.4, fontWeight: 500, lineHeight: 1.4, WebkitLineClamp: 3 };
}
```

## Component Granularity Rules

**Why**: React design drafts must be editable at the component level. Monolithic components defeat this purpose.

**Rules**:
- Each component ≤ 80 lines of JSX
- If a component contains a distinct visual concern (comparison, chart, step list, question list), extract it as a separate component
- Example: `Card.jsx` should NOT contain an inline comparison block — extract `ComparisonBlock.jsx`
- Example: `Card.jsx` should NOT contain inline step rendering — extract `StepList.jsx`

**Extraction triggers** (when to split):

| Pattern | Extract as | Why |
|---------|-----------|-----|
| Comparison UI inside a card | `ComparisonBlock.jsx` | User may want to move it outside the card |
| Step/numbered list inside a card | `StepList.jsx` | User may want to restyle steps independently |
| Question list inside a card | `QuestionList.jsx` | User may want to reuse questions elsewhere |
| Chart/visualization inside a card | `ChartBlock.jsx` | User may want to swap chart type |
| Agent/role badges inside a card | `AgentRow.jsx` | User may want to add/remove agents |

## Interactive Edit Guide (Post-Generation)

After every generation, output this guide. It maps user intent → file → edit action.

### Edit Matrix

| User Says | File to Edit | What Changes | Scope |
|-----------|-------------|-------------|-------|
| "换个配色" / "换个风格" | `design-tokens.css` | Replace color/font/spacing variables | Global |
| "改第N个卡片的标题" | `data.js` | `items[N-1].title = "..."` | Single item |
| "改第N个卡片的描述" | `data.js` | `items[N-1].description = "..."` | Single item |
| "删掉第N个卡片" | `data.js` | Remove `items[N-1]` from array | Single item |
| "添加一个新卡片" | `data.js` | Push new object to `items` array | Single item |
| "调整卡片顺序" | `data.js` | Reorder `items` array | All items |
| "从2列改成3列" | `App.jsx` | Change `grid-template-columns` | Layout |
| "把Header移到底部" | `App.jsx` | Move `<Header />` after `<main>` | Hierarchy |
| "把对比块提取出来" | `App.jsx` + new `ComparisonBlock.jsx` | Extract inline JSX to component | Restructure |
| "加一个总结组件" | New `SummaryCard.jsx` + `data.js` + `App.jsx` | Add component + data + import | Add feature |
| "卡片间距大一点" | `design-tokens.css` | Increase `--grid-gap` value | Global |
| "标题字号大一点" | `design-tokens.css` | Increase `--text-hero` value | Global |
| "换成暗色方案" | `design-tokens.css` | Replace all color variables with dark palette | Global |

### Agent Platform Edit Workflow

In TRAE/WorkBuddy/龙虾等 Agent 平台中，React 设计稿的交互编辑优势体现为：

```
1. 用户说 "把第3个卡片标题改成XXX"
2. Agent 读取 data.js，定位 items[2].title
3. Agent 只修改 data.js 中的那一行
4. Agent 用 git diff 确认变更范围
5. 用户预览，满意则继续，不满意则回退
```

**vs 图片设计稿的流程**：

```
1. 用户说 "把第3个卡片标题改成XXX"
2. 必须重新生成整张图片
3. 其他卡片可能因为 AI 随机性而改变
4. 无法 diff，无法回退
5. 无法增量修改
```

**关键优势**：
- **定向修改**：只改一个文件的一行，不影响其他组件
- **可回退**：git checkout 即可恢复
- **可 diff**：精确知道改了什么
- **可增量**：添加/删除/重排都是单行操作
- **可重构**：组件层级调整只需改 App.jsx 的 import 和 JSX 结构

## File Structure Summary

Always include a file tree at the beginning of the output:

```
📁 project/
├── 📄 design-tokens.css  ← 改配色/字体/间距
├── 📄 data.js            ← 改文字/数据/顺序
├── 📁 components/
│   ├── 📄 Header.jsx     ← 改标题区
│   ├── 📄 Card.jsx       ← 改卡片样式
│   └── 📄 ComparisonBlock.jsx ← 改对比块
└── 📄 App.jsx            ← 改布局/层级
```
