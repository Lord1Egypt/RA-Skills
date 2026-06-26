---
name: improve-codebase-architecture
description: 根据 CONTEXT.md 中的 domain language 和 docs/adr/ 中的 decisions，寻找 codebase 的 deepening opportunities。Use when the user wants to improve architecture, find refactoring opportunities, consolidate tightly-coupled modules, or make a codebase more testable and AI-navigable.
---

# Improve Codebase Architecture

暴露 architecture friction，并提出 **deepening opportunities**，也就是把 shallow modules 变成 deep modules 的 refactors。目标是 testability 和 AI-navigability。

## Glossary

在每个建议中精确使用这些术语。语言一致性就是重点，不要漂移到 “component”、“service”、“API” 或 “boundary”。完整定义见 [LANGUAGE.md](LANGUAGE.md)。

- **Module** — 任何有 interface 和 implementation 的东西（function、class、package、slice）。
- **Interface** — caller 为正确使用 module 必须知道的一切：types、invariants、error modes、ordering、config。不只是 type signature。
- **Implementation** — 内部代码。
- **Depth** — interface 上的 leverage：小 interface 后面有大量 behaviour。**Deep** = 高 leverage。**Shallow** = interface 几乎和 implementation 一样复杂。
- **Seam** — interface 所在的位置；可以不原地编辑就改变 behaviour 的地方。（用这个词，不用 “boundary”。）
- **Adapter** — 在 seam 处满足 interface 的具体东西。
- **Leverage** — callers 从 depth 获得的东西。
- **Locality** — maintainers 从 depth 获得的东西：change、bugs、knowledge 集中在一个地方。

关键原则（完整列表见 [LANGUAGE.md](LANGUAGE.md)）：

- **Deletion test**：想象删除这个 module。如果复杂性消失，它只是 pass-through。如果复杂性在 N 个 callers 中重新出现，它就在发挥价值。
- **The interface is the test surface.**
- **One adapter = hypothetical seam. Two adapters = real seam.**

这个 skill 会参考项目的 domain model。Domain language 为好的 seams 命名；ADRs 记录 skill 不应重新争论的决策。

## Process

### 1. Explore

先读取项目的 domain glossary 和你将触碰区域的任何 ADR。

然后使用 Agent tool 和 `subagent_type=Explore` 遍历 codebase。不要死套启发式规则；自然探索并记录你感到 friction 的地方：

- 理解一个概念是否需要在许多小 modules 之间来回跳？
- 哪些 modules 是 **shallow**，interface 几乎和 implementation 一样复杂？
- 哪些 pure functions 只是为了 testability 被抽出，但真正 bug 藏在调用方式里（没有 **locality**）？
- 哪些 tightly-coupled modules 会跨 seams 泄漏？
- codebase 哪些部分未测试，或很难通过当前 interface 测试？

对任何疑似 shallow 的东西应用 **deletion test**：删除它会集中复杂性，还是只是移动复杂性？“会集中”就是你要找的信号。

### 2. Present candidates as an HTML report

写一个 self-contained HTML file 到 OS temp directory，避免任何内容落进 repo。Temp dir 从 `$TMPDIR` 解析，fallback 到 `/tmp`（Windows 上用 `%TEMP%`），并写入 `<tmpdir>/architecture-review-<timestamp>.html`，确保每次运行都有新文件。为用户打开它：Linux 用 `xdg-open <path>`，macOS 用 `open <path>`，Windows 用 `start <path>`，并告诉用户绝对路径。

Report 使用 **Tailwind via CDN** 做 layout 和 styling，使用 **Mermaid via CDN** 处理适合 graph/flow/sequence 的 diagrams。Mermaid 要和手写 CSS/SVG visual 混用：关系是 graph-shaped（call graphs、dependencies、sequences）时用 Mermaid；想要更 editorial 的效果（mass diagrams、cross-sections、collapse animations）时用 hand-built divs/SVG。每个 candidate 都要有一个 **before/after visualisation**。要视觉化。

每个 candidate 仍使用之前的模板，但渲染成 card：

- **Files** — 涉及哪些 files/modules
- **Problem** — 当前 architecture 为什么造成 friction
- **Solution** — 用普通语言说明会改变什么
- **Benefits** — 用 locality 和 leverage 解释，并说明 tests 会如何改善
- **Before / After diagram** — side-by-side，自定义绘制，说明 shallowness 和 deepening
- **Recommendation strength** — `Strong`、`Worth exploring`、`Speculative` 之一，渲染成 badge

Report 最后加一个 **Top recommendation** section：你会先处理哪个 candidate，以及原因。

**domain 词汇使用 CONTEXT.md，architecture 词汇使用 [LANGUAGE.md](LANGUAGE.md)。** 如果 `CONTEXT.md` 定义了 “Order”，就说 “Order intake module”，不要说 “FooBarHandler”，也不要说 “Order service”。

**ADR conflicts**：如果 candidate 与现有 ADR 冲突，只有当 friction 真实到值得重开 ADR 时才提出。在 card 中明确标记（例如一个 warning callout：_"contradicts ADR-0007 — but worth reopening because…"_）。不要列出 ADR 理论上禁止的每个 refactor。

完整 HTML scaffold、diagram patterns 和 styling guidance 见 [HTML-REPORT.md](HTML-REPORT.md)。

不要还没问用户就提出 interfaces。文件写好后，问用户：“你想探索哪一个？”

### 3. Grilling loop

用户选中 candidate 后，进入 grilling conversation。和他们走完整个 design tree：constraints、dependencies、deepened module 的形状、seam 后面是什么、哪些 tests 能经受变化。

决策成形时内联产生 side effects：

- **用 `CONTEXT.md` 中没有的概念命名 deepened module？** 把 term 加到 `CONTEXT.md`，纪律同 `/grill-with-docs`（见 [CONTEXT-FORMAT.md](../grill-with-docs/CONTEXT-FORMAT.md)）。文件不存在就懒创建。
- **对话中收紧了模糊 term？** 立刻更新 `CONTEXT.md`。
- **用户用有分量的理由拒绝 candidate？** 提议 ADR，表述为：_"要我把这记录成 ADR，避免未来 architecture reviews 再次建议它吗？"_ 只有当未来 explorer 真的需要这个理由来避免重复建议时才提议；短期理由（“现在不值得”）和显而易见的理由跳过。见 [ADR-FORMAT.md](../grill-with-docs/ADR-FORMAT.md)。
- **想探索 deepened module 的替代 interfaces？** 见 [INTERFACE-DESIGN.md](INTERFACE-DESIGN.md)。
