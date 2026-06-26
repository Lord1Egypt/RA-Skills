# Advanced Workflow Guide / 高手玩法 / 上級ワークフローガイド

## Table of Contents

1. [Master Prompt Template](#master-prompt-template)
2. [Reference Input Strategy](#reference-input-strategy)
3. [Iteration Techniques](#iteration-techniques)
4. [Design-to-Code Handoff](#design-to-code-handoff)

## Master Prompt Template

Use this template when starting a new project. Fill in all fields for best results / 新项目启动时使用此模板，填入所有字段获得最佳效果:

```
做一个 [产品类型]
目标用户：[用户画像]
使用场景：[使用情境]
核心功能：
- [功能1]
- [功能2]
页面结构：
- [页面1]
- [页面2]
设计风格：[风格描述]
参考：
- [参考1，如 Stripe]
- [参考2，如 Notion]
输出：
1. 低保真结构
2. 3种布局方案
```

**Example / 示例:**
```
做一个 B2B SaaS 后台
目标用户：运营人员，非技术背景
使用场景：日常数据监控 + 客户管理
核心功能：
- 数据看板（实时指标）
- 客户列表（筛选+操作）
- 任务分配
页面结构：
- Dashboard（首页）
- Customer List
- Customer Detail
设计风格：简洁冷静，专业可信
参考：
- Stripe Dashboard
- Linear
输出：
1. Wireframe（低保真）
2. 3种 Dashboard 布局方案（信息优先 / 操作优先 / 极简）
```

## Reference Input Strategy

XDesign is strongest when fed reference material. Always encourage users to provide input / XDesign 在有参考输入时最强。始终鼓励用户提供输入:

**Accepted inputs / 接受的输入:**
- **Brand name (fastest)** → load pre-extracted DESIGN.md from catalog. See [design-system-catalog.md](design-system-catalog.md) for full list.
- Website URLs → extract layout patterns, color systems, typography
- Screenshots → inherit visual style, component language
- Figma exports → pixel-accurate recreation
- PPT files → extract slide layouts, brand colors
- Code repositories → lift exact design tokens, component patterns
- Hand-drawn sketches / napkin files → interpret structure and intent
- Brand assets (logos, style guides) → auto-extract design system

### DESIGN.md Fast Path

When user names a brand (e.g., "像 Stripe", "Linear 风格", "make it look like Notion"):

1. Check [design-system-catalog.md](design-system-catalog.md) for the brand index
2. Read the corresponding `assets/design-md/<brand>/DESIGN.md`
3. Apply the design tokens (colors, typography, components, shadows) directly as the design system foundation
4. Skip manual brand material extraction — proceed to design phase immediately

When user describes a style without naming a brand:
- "暗黑开发者风格" → Linear, Supabase, or Resend
- "温暖友好" → Claude, Notion, or Airbnb
- "专业金融" → Stripe
- "极简高端" → Apple, Tesla, or Vercel
- Refer to the "Style-to-Brand Mapping" table in [design-system-catalog.md](design-system-catalog.md)

**Pro tip / 高手技巧:**
Give it a brand name → get pixel-accurate design system without screenshots or manual extraction.

给一个品牌名 → 直接获得完整设计令牌，无需截图或手动提取。

## Iteration Techniques

Three iteration modes / 三种迭代模式:

### 1. Conversational / 对话修改
Best for directional changes / 方向性调整:
- "按钮太重了，轻一点"
- "整体风格偏冷，加暖色"
- "信息层级不对，数据应该是主角"

### 2. Canvas Annotation / 画布批注
Best for specific element changes / 具体元素修改:
- Click element → "这里改成卡片布局"
- Drag element → adjust spacing/position
- Select text → change copy

### 3. Slider/Tweak Adjustment / 滑杆调整
Best for parameter tuning / 参数微调:
- Spacing scale
- Color palette
- Font size/weight
- Layout density

## Design-to-Code Handoff

When user says "把这个转成 React 组件" or "hand off to development":

1. Invoke **Handoff to Claude Code** sub-skill
2. Output structured component code with:
   - Props interface
   - Style tokens extracted from design
   - Responsive breakpoints
   - Accessibility attributes
3. This bridges design → development in one flow

**设计 → 开发一体化。** 一句话从设计稿转成可开发代码。

## Multilingual Design / 多语言设计

When producing designs for multilingual audiences, follow these rules:

**Text direction & layout:**
- Always confirm target languages before starting
- CJK text: line height 1.6-1.8, font stacks (`"Noto Sans SC", "PingFang SC", "Microsoft YaHei", sans-serif` for Chinese; `"Noto Sans JP", "Hiragino Sans", "Yu Gothic", sans-serif` for Japanese)
- RTL languages (Arabic, Hebrew): `dir="rtl"`, mirror layout asymmetries
- Text expansion: English→Chinese ~60-80%, English→German ~130%, English→Japanese ~80-100%

**Localization:**
- Text in variables, not hardcoded
- `lang` attribute on `<html>`
- `Intl.DateTimeFormat` / `Intl.NumberFormat` for locale formatting
- CJK slides more compact; German/French need more space

---

# Design Workflow Engine — Core Loop

> Extracted from main SKILL.md to keep the entry file under 500 lines.
> Read this when a project requires more than a single-pass design.

## Core Loop: PPAF

XDesign operates as a continuous PPAF (Perception → Planning → Action → Feedback) loop, not a linear pipeline. Each design iteration cycles through all four phases; skipping a phase produces worse designs, not faster ones.

### 1. Perception — Read the world

Gather ALL available context before acting. Concurrent reads are cheap; sequential reads are slow.

- Read the user request, attached files, design system files, existing codebase
- Call file-exploration tools in parallel where possible
- If context is insufficient, ask questions (see Asking Questions below)

### 2. Planning — Decide what to do

A plan that lives only in the agent's head is a plan that drifts. Make it concrete:

- Write a todo list for complex tasks
- Decide the output type (prototype, deck, landing page, etc.)
- Choose the starter component and technical approach
- Identify which existing resources to reuse

### 3. Action — Execute the plan

Build the design artifact. The junior-designer voice — assumptions + context + reasoning — is intentional. It signals to the user that the agent is thinking, not just generating.

- Create folder structure, copy resources, write HTML
- Begin with assumptions + context + design reasoning; add placeholders; show early
- Follow the Design Process phases (Design System First → Wireframe → Build)

### 4. Feedback — Verify and learn

After each action, verify before proceeding. Verification is cheap; rebuilds are expensive.

- Call `done` to surface the file and check for console errors
- If errors appear, diagnose the root cause; don't just patch symptoms
- If clean, fork a verifier agent for background quality check
- Reflect: did this action achieve the planned goal? If not, loop back to Planning

If stuck on the same issue for 3+ iterations, escalate to the user rather than retrying endlessly. Endless retries usually mean the plan was wrong, not the implementation.

## Design Process

### Phase 1: Design System First

Establishing the visual foundation is the single highest-leverage move in this workflow. Skipping it means every subsequent page invents its own visual language.

1. Ask the user for brand materials (logo, existing PPT, website URL, screenshots)
2. Extract or create a design system from those materials
3. Only then start designing pages

**DESIGN.md fast path** — when the user names a brand ("Stripe-style", "Linear style", "像 Notion"):

1. Check `references/design-system-catalog.md` for the brand index and style-to-brand mapping
2. Read `assets/design-md/<brand>/DESIGN.md` for the full design system
3. Apply those tokens as the foundation; skip manual extraction
4. Proceed directly to Phase 2

This covers 58 curated brands across AI, developer tools, fintech, automotive, design, and more.

The design system is a **contract** — it defines the binding rules for color, typography, spacing, and component language. All subsequent designs must honor this contract.

### Phase 2: Wireframe Before Hi-Fi

Endless visual tweaks are a symptom of skipping the wireframe phase. Confirm structure first; polish later.

1. **Wireframe first** — low-fidelity structure, confirm layout and information hierarchy with the user
2. **Then upgrade** — apply the visual system, refine interactions

### Phase 3: Build & Iterate

Output is a single HTML document. Pick the format by exploration type:

- **Purely visual** (color, type, static layout) → `design_canvas.jsx` starter
- **Interactions, flows, many-option situations** → hi-fi clickable prototype with Tweaks

Build process:

1. Copy ALL relevant components, read ALL relevant examples; ask the user if you can't find them
2. Begin HTML with assumptions + context + design reasoning; add placeholders; show early
3. Write React components, embed in HTML; show ASAP
4. Check, verify, iterate

Good designs start from existing context — ask the user to import a codebase, find a UI kit, or provide screenshots. Mocking from scratch is a last resort and produces mediocre results.

Prefer code over screenshots — better at recreating or editing interfaces when the source is code.

## Structured Requirements

XDesign thrives on structured requirements, not loose keywords. When user input is vague, extract or ask for these dimensions:

- **Product type** — B2B SaaS, consumer app, marketing site, internal tool, etc.
- **Target users** — role, tech-savviness, context of use
- **Core functions** — what must the design accomplish
- **Page structure** — key screens or sections
- **Visual direction** — style references, mood, brand constraints
- **Output format** — prototype, deck, landing page, design system

For the complete prompt template, see "Master Prompt Template" above.

## Project Naming

Descriptive names act as implicit context — they anchor subsequent design decisions and produce more consistent output.

- ❌ "project1", "untitled", "new project"
- ✅ "AI Recruitment Platform", "Stripe-style Dashboard", "Q4 Investor Deck"

If the system supports setting a project name, always set it to something descriptive.

## Asking Questions

Use the question tool when starting something new or when the ask is ambiguous. One focused round is usually right; multiple rounds cause fatigue.

**When to ask:**
- New project with ambiguous requirements → ask extensively
- Attached PRD but unclear audience/tone → ask about specifics
- Food delivery app prototype → ask a TON of questions

**When NOT to ask:**
- "Make a deck with this PRD for Eng All Hands, 10 minutes" → enough info provided
- "Turn this screenshot into an interactive prototype" → ask only if behavior is unclear from images
- "Recreate the composer UI from this codebase" → no questions needed
- Small tweaks, follow-ups, or the user gave everything needed → skip

When asking, include:
- Starting point confirmation (UI kit, design system, codebase). If none exists, ask for one.
- Whether they want variations, and for which aspects
- Whether they want divergent visuals, interactions, or ideas
- What tweaks they'd like to explore
- At least 4 other problem-specific questions
- At least 10 questions total for new projects

## Design Reasoning

When the user asks "why this layout?" or "explain your design choices", provide clear thinking:

- **Information hierarchy** — what's primary, secondary, tertiary
- **Layout rationale** — why this grid, spacing, visual weight
- **Color choices** — how the palette supports brand or mood
- **Interaction logic** — why elements behave the way they do
- **Trade-offs** — what was prioritized and what was sacrificed

This makes XDesign a design mentor, not just a production tool.

## Tweaks

Tweaks are in-design toggle controls — sliders, color pickers, layout switches. They let the user explore without re-prompting.

Toggle Tweaks from the toolbar. Title panel **"Tweaks"**. Keep small — floating bottom-right or inline handles. Hide when off.

Register the listener BEFORE announcing availability:

```js
window.addEventListener('message', (e) => { ... });
window.parent.postMessage({type: '__edit_mode_available'}, '*');
```

Persist defaults with a marker comment so the agent can find and update them later:

```js
const TWEAK_DEFAULTS = /*EDITMODE-BEGIN*/{...}/*EDITMODE-END*/;
```

Add a couple of tweaks by default even if the user didn't ask — exposing interesting possibilities is part of the value.

## Design Variations

When the user wants "options", give 3+ distinct approaches across several dimensions. Mix conventional and novel. Start basic, get more creative.

**Multi-variation strategy:**
- Never say "tweak it again". Instead, generate 3 distinct approaches:
  - **Information-first** — content density, data clarity
  - **Conversion-first** — CTA prominence, flow optimization
  - **Minimal** — maximum whitespace, essential-only elements
- Let the user mix and match across variations

When the user asks for changes, add as TWEAKS to the original file — one file with toggleable versions beats multiple files that drift.

## Verification

1. Run the Quality Self-Check (see `mode-2-prototype.md`)
2. `done` with the HTML path → opens in the user's tab, returns console errors
3. Fix errors: diagnose root cause, not symptoms. `done` again.
4. Once clean → `fork_verifier_agent`. Silent on pass.
5. Don't screenshot before `done`.

Mid-task: `fork_verifier_agent({task: "..."})`.

## Built-in Sub-Skills

| Skill Name | When to Use |
|---|---|
| Animated video | Timeline-based motion design |
| Interactive prototype | Working app with real interactions |
| Make a deck | Slide presentation in HTML |
| Make tweakable | Add in-design tweak controls |
| Frontend design | Aesthetic direction outside brand system |
| Wireframe | Explore ideas with wireframes/storyboards |
| Export as PPTX (editable) | Native text & shapes, editable in PowerPoint |
| Export as PPTX (screenshots) | Flat images, pixel-perfect |
| Create design system | Creating design systems or UI kits |
| Save as PDF | Print-ready PDF export |
| Save as standalone HTML | Single self-contained offline file |
| Send to Canva | Export as editable Canva design |
| Handoff to Claude Code | Developer handoff package |
