# HTML Report Format

Architectural review 会被渲染成一个 self-contained HTML file，放在 OS temp directory。Tailwind 和 Mermaid 都来自 CDNs。Mermaid 能稳定处理 graph-shaped diagrams；手写 divs 和 inline SVG 更适合 editorial visuals（mass diagrams、cross-sections）。两者混用，不要所有东西都依赖 Mermaid，否则看起来会很 generic。

## Scaffold

```html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <title>Architecture review — {{repo name}}</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script type="module">
      import mermaid from "https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs";
      mermaid.initialize({ startOnLoad: true, theme: "neutral", securityLevel: "loose" });
    </script>
    <style>
      /* small custom layer for things Tailwind doesn't cover cleanly:
         dashed seam lines, hand-drawn-feeling arrow heads, etc. */
      .seam { stroke-dasharray: 4 4; }
      .leak { stroke: #dc2626; }
      .deep { background: linear-gradient(135deg, #0f172a, #1e293b); }
    </style>
  </head>
  <body class="bg-stone-50 text-slate-900 font-sans">
    <main class="max-w-5xl mx-auto px-6 py-12 space-y-12">
      <header>...</header>
      <section id="candidates" class="space-y-10">...</section>
      <section id="top-recommendation">...</section>
    </main>
  </body>
</html>
```

## Header

Repo name、date，以及紧凑 legend：solid box = module，dashed line = seam，red arrow = leakage，thick dark box = deep module。不要 introduction paragraph，直接进入 candidates。

## Candidate card

Diagrams 承担主要信息量。Prose 要稀疏、直白，并直接使用 glossary terms（[LANGUAGE.md](LANGUAGE.md)），不要铺垫。

每个 candidate 是一个 `<article>`：

- **Title** — 简短，命名 deepening（例如 “Collapse the Order intake pipeline”）。
- **Badge row** — recommendation strength（`Strong` = emerald，`Worth exploring` = amber，`Speculative` = slate），再加一个 dependency category tag（`in-process`、`local-substitutable`、`ports & adapters`、`mock`）。
- **Files** — monospaced list，`font-mono text-sm`。
- **Before / After diagram** — 核心内容。两列并排。见下面的 patterns。
- **Problem** — 一句话。痛点是什么。
- **Solution** — 一句话。改变什么。
- **Wins** — bullets，每条不超过 6 个词。例如 “Tests hit one interface”、“Pricing logic stops leaking”、“Delete 4 shallow wrappers”。
- **ADR callout**（如果适用）— amber-tinted box 里的一行。

不要写成段落解释。如果 diagram 需要一段文字才能看懂，就重画 diagram。

## Diagram patterns

选择适合 candidate 的 pattern。混合使用。不要让每个 diagram 长得一样，变化本身就是重点。

### Mermaid graph（dependencies / call flow 的主力）

当重点是 “X calls Y calls Z, and look at the mess” 时，使用 Mermaid `flowchart` 或 `graph`。外面包一个 Tailwind-styled card，避免像是直接空降。用 classDef 把 leakage edges 标红，把 deep module 标成深色。Sequence diagrams 很适合 “before: 6 round-trips; after: 1.”

```html
<div class="rounded-lg border border-slate-200 bg-white p-4">
  <pre class="mermaid">
    flowchart LR
      A[OrderHandler] --> B[OrderValidator]
      B --> C[OrderRepo]
      C -.leak.-> D[PricingClient]
      classDef leak stroke:#dc2626,stroke-width:2px;
      class C,D leak
  </pre>
</div>
```

### Hand-built boxes-and-arrows（当 Mermaid layout 跟你作对时）

Modules 用带 border 和 label 的 `<div>` 表示。Arrows 用 inline SVG `<line>` 或 `<path>`，absolute 定位在 relative container 上。当你希望 “after” diagram 像一个 thick-bordered deep module，内部结构被 greyed-out 显示时，用这个；Mermaid 很难渲染出正确的 weight。

### Cross-section（适合 layered shallowness）

堆叠 horizontal bands（`h-12 border-l-4`）来展示一次 call 穿过的 layers。Before：6 个薄 layer，每个几乎什么都不做。After：1 个 thick band，标注 consolidated responsibility。

### Mass diagram（适合 “interface as wide as implementation”）

每个 module 用两个 rectangles：一个表示 interface surface area，一个表示 implementation。Before：interface rectangle 几乎和 implementation rectangle 一样高（shallow）。After：interface rectangle 很短，implementation rectangle 很高（deep）。

### Call-graph collapse

Before：把 function calls tree 渲染成 nested boxes。After：把同一棵 tree 折叠成一个 box，并把现在内部化的 calls 以 faded 状态显示在里面。

## Style guidance

- Lean editorial，不要 corporate-dashboard。留足 whitespace。Headings 可选 serif（`font-serif` 和 stone/slate 很搭）。
- Colour sparingly：一个 accent（emerald 或 indigo），red 用于 leakage，amber 用于 warnings。
- Diagrams 保持约 320px 高，这样 before/after 可以舒适并排，不需要滚动。
- Diagram 内部 module labels 使用 `text-xs uppercase tracking-wider`，应该读起来像 schematic，而不是 UI。
- 唯一 scripts 是 Tailwind CDN 和 Mermaid ESM import。除此之外 report 是 static，不要 app code，不要 Mermaid 自身渲染之外的 interactivity。

## Top recommendation section

一个更大的 card。Candidate name，一句话说明为什么，anchor link 到它的 card。仅此而已。

## Tone

Plain English，concise，但 architectural nouns 和 verbs 必须直接来自 [LANGUAGE.md](LANGUAGE.md)。简洁不是漂移的借口。

**Use exactly:** module, interface, implementation, depth, deep, shallow, seam, adapter, leverage, locality.

**Never substitute:** component, service, unit (for module) · API, signature (for interface) · boundary (for seam) · layer, wrapper (for module, when you mean module).

**Phrasings that fit the style:**

- "Order intake module is shallow — interface nearly matches the implementation."
- "Pricing leaks across the seam."
- "Deepen: one interface, one place to test."
- "Two adapters justify the seam: HTTP in prod, in-memory in tests."

**Wins bullets** 要用 glossary terms 命名收益：_"locality: bugs concentrate in one module"_、_"leverage: one interface, N call sites"_、_"interface shrinks; implementation absorbs the wrappers"_。不要写 _"easier to maintain"_ 或 _"cleaner code"_，这些词不在 glossary 中，不能直接获得位置。

不要 hedging，不要 throat-clearing，不要 “it's worth noting that…”。如果一个 sentence 可以变成 bullet，就改成 bullet。如果一个 bullet 可以删，就删。如果一个 term 不在 [LANGUAGE.md](LANGUAGE.md) 里，先找一个已经存在的 term，再考虑发明新词。
