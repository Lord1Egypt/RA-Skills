# Conversational / Chat UI Audit

Use this module when auditing a chat, agent, or workspace-style interface. These components have their own recurring failure patterns beyond general layout/state bugs.

## 1. Message bubbles

- [ ] Bubble width is adaptive to content, not fixed — a one-word reply shouldn't render in a bubble the same width as a paragraph, but a long response also shouldn't overflow or force horizontal scroll. Typical pattern: `max-width` (e.g. 70–80% of the chat column) with `width: fit-content`, not a fixed width.
- [ ] User messages and assistant messages are visually distinguishable at a glance (alignment, color, or avatar — ideally more than one signal, not color alone per accessibility baseline) without needing to read the "You"/"Assistant" label to tell them apart.
- [ ] Long messages don't break the layout — check specifically with a message containing a very long unbroken string (a URL, a long code identifier) to confirm `overflow-wrap`/`word-break` is applied, not just normal prose.
- [ ] Consecutive messages from the same sender have appropriate spacing/grouping (visually distinct from a new turn) rather than every message looking like an isolated, equally-spaced block regardless of context.
- [ ] Timestamp/metadata (if shown) doesn't compete visually with the message content — typically smaller, muted-color text, not the same weight as the message itself.

## 2. Markdown rendering fidelity

This is a common gap: a message pipeline that renders plain text correctly but falls back to showing raw syntax for anything beyond basic bold/italic.

- [ ] **Tables** render as actual HTML tables (`<table>`), not literal pipe-and-dash text (`| Column | Column |` / `|---|---|` shown verbatim). Verify the markdown parser in use (e.g. `react-markdown`, `marked`, `markdown-it`) has GFM (GitHub Flavored Markdown) table support enabled — this is frequently an opt-in plugin (e.g. `remark-gfm` for `react-markdown`), not default behavior, and its absence is the most common reason tables show as raw text.
- [ ] **Lists** (ordered, unordered, nested) render with actual list styling and indentation, not as plain text with dashes/numbers.
- [ ] **Headings, blockquotes, links** render with distinct styling, and links open appropriately (typically a new tab for external links, with `rel="noopener noreferrer"`).
- [ ] **Inline code** (single backticks) is visually distinct (monospace, subtle background) from block code.

## 3. Code blocks

- [ ] Rendered in a monospace font with a distinct background/border from surrounding prose — this is the "field pendeteksi code" component: a fenced code block, not the same paragraph styling as regular text.
- [ ] **Syntax highlighting** is applied based on the declared language (the ```` ```language ```` hint), not rendered as flat unstyled monospace text.
- [ ] **Copy-to-clipboard button** is present, visible on hover (or always visible on touch devices, since hover doesn't exist there), and gives feedback on click (e.g. icon swaps to a checkmark briefly) — a copy button with no click feedback leaves the user unsure whether it worked.
- [ ] The language label (e.g. "TypeScript", "bash") is shown, typically in the code block's header bar alongside the copy button.
- [ ] Long lines either wrap or scroll horizontally within the block *without* breaking the surrounding page layout — a code block should never force the whole page to scroll horizontally.
- [ ] Code blocks that arrive via streaming render progressively without visibly "flashing" unstyled-then-styled, if avoidable — a minor polish item, not a correctness blocker.

## 4. Chat input control

A "basic" input control typically means a bare `<textarea>` with a send button and nothing else. Compare against what a production-grade input control needs:

- [ ] **Auto-resizing**: the input grows with content (up to a reasonable max height, then scrolls internally) rather than staying single-line or having a fixed height that clips longer drafts.
- [ ] **Submit behavior**: Enter sends, Shift+Enter inserts a newline (the near-universal convention for chat inputs) — verify this explicitly, since a plain `<textarea>` defaults to Enter always inserting a newline.
- [ ] **Send button states**: disabled/inert when the input is empty or while a response is streaming (prevents double-submission), with a visually distinct "stop generating" affordance during streaming rather than the send button just doing nothing when clicked.
- [ ] **Attachment/action affordances** (if the product needs them): a way to attach files/images, positioned so it doesn't crowd the text entry area — typically a small icon button to one side, not competing for the same click target as sending.
- [ ] **Focus state**: the input container shows a clear focus treatment (border/ring) consistent with the rest of the design system's focus tokens, not just the browser default outline.
- [ ] **Placeholder text** is helpful and non-generic ("Message [assistant name]..." rather than a bare "Type here"), and disappears immediately on focus/typing.
- [ ] **Loading/streaming state** of the assistant's response is visible near the input or message list (a subtle indicator that generation is in progress) so the user isn't left wondering whether their message was received.

## 5. Self-check

- [ ] A message containing a markdown table renders as a real table, verified by testing with actual table markdown, not assumed from the library's marketing claims.
- [ ] A message containing a fenced code block has visible syntax highlighting and a working copy button, verified by actually triggering the copy and confirming clipboard content (or at minimum confirming the click handler fires and gives visual feedback).
- [ ] The input control's Enter/Shift+Enter behavior is explicitly implemented, not left to `<textarea>` defaults.
- [ ] Message bubbles were checked with both a very short message and a very long one, not just default placeholder text.
