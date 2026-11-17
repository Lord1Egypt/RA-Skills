# VibePolish Technical Design

## Product Boundary

VibePolish is a runtime-only WYSIWYG retoucher for arbitrary single-file HTML demos. It targets vibe-coded HTML where contract-first normalization is usually unavailable.

It is not a semantic normalizer. It does not promise full hidden-state discovery, source refactoring, component extraction, branch editing, snapshot rebase, or conflict resolution.

The product promise is narrower:

- Freeze a browser-rendered moment.
- Resolve what the user visually selected.
- Offer safe edit controls for that selection.
- Apply edits directly to the rendered page.
- Export enough patch information for either baked HTML output or AI-assisted source modification.

Supported states are states the user can reach or stabilize in the browser:

- current visible page
- hover/dropdown/popover
- modal/drawer
- focus-like UI
- active/current/open/selected-like class or attribute states when mechanically discoverable inside a group
- timer/RAF/CSS-animation driven demo moments

Unsupported as a core V1 flow:

- hidden business-state discovery
- semantic state classification
- multi-branch snapshot editing
- editing old snapshots out of order
- snapshot rebase or merge conflict resolution
- preview panes
- source-code cleanup or maintainable component generation

## Engineering Migration Guardrail

During the React/Vite engineering migration, `src/core/legacy-runtime.ts` is a frozen migration layer.

Allowed changes:

- mechanical moves that preserve behavior
- generated-output sync after an approved source change
- test-mode plumbing that does not affect normal user behavior
- comments or documentation that clarify migration boundaries

Not allowed as incidental engineering work:

- changing selection, scope, routing, CSS writing, freeze, snapshot, or export behavior
- changing AI Patch semantics or selector strategy
- adding product features inside `legacy-runtime.ts`
- fixing product bugs as part of a structural refactor without a separate task and verification plan

Any product behavior change must be handled as its own task with explicit intent, focused diff, and browser/runtime verification. Engineering refactors should prove behavior equivalence before and after the change.

### Shell Layer Before CDP

The final safe engineering cleanup before CDP is limited to shell-layer code:

- React panel ViewModel and command contracts.
- Export/download/feedback wrappers.
- Read-only test bridge packaging.
- Pure shared helpers for text formatting, CSS property formatting, and geometry math.

These helpers may be shared by the current DOM runtime and a future CDP runtime. They must not know selection, scope, routing, CSS priority, pseudo states, or runtime `dt-*` implementation classes.

CDP-sensitive behavior remains inside the frozen runtime until CDP probing proves the replacement shape:

- freeze, virtual time, snapshot, hover lock, and interaction shield
- visual selection and visual layer resolution
- scope/range/group/state detection
- style routing and CSS write priority
- hover/default/active selector strategy
- patch/export semantic entry points

Do not split those areas into DOM-specific modules merely for aesthetics. Doing so would freeze current DOM assumptions before CDP has been validated.

### CDP Runtime Probe

`src/core/cdp-runtime-probe.mjs` is the first CDP-facing runtime probe. It lives next to `legacy-runtime.ts` so future migration work can compare the current DOM runtime with CDP facts without changing product behavior.

The runnable host is `tools/cdp-runtime-probe.mjs`:

```bash
npm run probe:cdp -- --selector ".drm-topic-tab:not(.active)" --property background-color --pseudo hover
```

The probe is read-only. It can inspect computed style, matched CSS rules, likely winning declarations, source ranges, stylesheet ids, and forced pseudo-state snapshots. It must not write styles, drive editor edits, or replace runtime behavior until CDP read results are understood.

The current capability matrix is documented in `docs/CDP_RUNTIME_PROBE_REPORT.md`. The key validated constraint is that CDP should be bound to the current selected node/backend node, because a plain selector may match hidden equivalents before the visible object the user is editing.

`npm run probe:cdp:binding` validates that constraint against the current wrapper: a naked selector can resolve to a different hidden/sibling element, while a temporary `data-vibepolish-cdp-probe-id` attached to the editor's selected anchor lets CDP inspect the actual node. That attribute is test/probe plumbing only and must be stripped from exported HTML.

`npm run probe:cdp:selection` is the current-selection diagnostic loop. It opens real wrappers, selects targets through visible editor UI, binds CDP to the selected anchor/route, and records winner declarations for representative default, hover, active, table, and history-card cases. This is still read-only; it must not change product selection, routing, or write behavior.

## Source And Artifact Boundary

The VibePolish skill package has three layers:

- Source: `src/`, `templates/`, `tools/`, and `scripts/`.
- Ignored local build cache: `dist/`.
- Committed standalone Node distribution: `standalone/`.
- Committed Codex live generated mirror: `skills/vibepolish`.

`standalone/` is the direct Node entry for users who do not use the skill layer. It contains `README.md`, `wrap-html.mjs`, and `assets/`.

`skills/vibepolish` is a thin agent skill wrapper over the standalone distribution. It is intentionally overwritten by `npm run build:skill` so Codex can immediately use the latest generated skill for local E2E. Files in that directory must not be edited by hand; edit the source layer and rebuild instead.

`dist/` is ignored by git. After `npm run build:skill`, local `dist/vibepolish` and committed `skills/vibepolish` should match for key skill files.

Codex E2E flow:

```bash
npm run build
npm run build:skill
# Codex uses skills/vibepolish for E2E.
```

## Runtime Architecture

The editor is generated by wrapping a source HTML file with:

- an iframe that renders the source demo
- a parent-side control panel
- an injected runtime script
- runtime CSS patches for selection, freeze, scope, and edits

The source HTML structure is not rewritten for normalization. Runtime classes such as `dt-scope-*`, `dt-edit-*`, `dt-force-hover`, and `dt-hover-edit-*` are editor implementation details, not source component names.

Editor shell TODO:

- Refactor the sidebar and iframe wrapper architecture so the demo stage, editor panel, overlays, and floating UI have clearer ownership boundaries.
- Evaluate replacing or supplementing the fixed sidebar with a floating-window style editor shell.
- The wrapper should make room for future desktop-like interactions without making the iframe coordinate model fragile.
- Add a polished product floating entry point for opening/activating the editor.
- The entry should use VP/LD element design language and feel like a designed product affordance, not a raw debug button.

## Three-Layer Hit Model

The editor separates three questions that used to be conflated:

1. What did the user visually select?
2. Where should a specific property actually be written?
3. Should a specific control be shown or enabled for this selection?

### Visual Selection

Visual selection answers: "What object did the user visually select?"

It is used for:

- solid selection outline
- object ladder
- range ladder anchor
- copy selection payload object identity
- selector display or anchor selector generation when needed internally

Suggested structure:

```js
{
  anchor: Element,
  raw: Element,
  layers: {
    background: Element | undefined,
    border: Element | undefined,
    radius: Element | undefined,
    shadow: Element | undefined,
    padding: Element | undefined,
    content: Element | undefined
  },
  textLeaves: Element[],
  roles: string[],
  confidence: number,
  reason: string
}
```

Rules:

- Start from the raw hit element under the pointer.
- Walk only the ancestor chain, usually capped to 5-6 levels.
- Do not search arbitrary siblings to build an object.
- Media elements such as `img`, `svg`, `video`, and `canvas` are self objects by default.
- Controls such as `button`, `a`, `input`, `textarea`, and `select` are control visual objects by default.
- Text leaves remain selectable as text objects.
- Meaningless wrappers may be merged into a visual object when they contribute background, border, radius, shadow, padding, or layout.
- Page-level containers, `html`, `body`, and near-fullscreen shells are ignored as visual objects unless the raw hit really is that shell.
- If confidence is low, fall back to the raw DOM element and expose fewer controls.

Visual contribution is mechanical:

- non-transparent `background-color`
- visible border width and non-transparent border color
- `box-shadow` other than `none`
- positive `border-radius`
- positive padding
- flex/grid layout with multiple visible children
- visible text leaves inside the bounded object

### Property Route

Property route answers: "For this property, which DOM nodes should receive the edit?"

It consumes the visual selection. It is not a separate user-facing concept.

Examples:

- `backgroundColor` writes to `layers.background` when available.
- `borderColor` writes to `layers.border`, with a safe fallback to the surface/control/media anchor.
- `borderRadius` writes to the radius layer.
- `boxShadow` will write to the shadow/surface layer when a dedicated control exists.
- `padding` writes to the padding/content layer.
- `color`, `fontSize`, `fontFamily`, and `fontWeight` write to visible text leaves.
- `textContent` writes only to a single text leaf.

Text style properties share the same target principle: they route to `textLeaves`, not to the surface anchor. Their enabled state may differ because each property independently checks whether current computed values are consistent across the target set.

### Safe Write Target

A safe write target means: after the editor writes CSS to a DOM node, the result should match what the user visually intended, and the edit should not unexpectedly spill into unrelated UI.

It is not only about whether the browser accepts the CSS. The browser may accept a declaration that is useless, written to the wrong layer, or too broad.

Safe write has two requirements:

1. Correct layer

   The target node must be the layer that actually controls the property.

   Examples:

   - text color can safely write to text leaves
   - card background should write to the background/surface layer, not to a text `span`
   - border color should write to the border layer or a known surface fallback
   - `text-align` should write to a block/text container, not blindly to an inline text leaf

2. Correct blast radius

   The target node must stay within the user's selected visual object and selected range.

   Writing to an ancestor is only safe when that ancestor is still part of the visual object. If the ancestor also controls unrelated icons, actions, or sibling content, the route should be considered risky or disabled.

This is why "the source has a computed value" is not enough to show a control. For example, a selected text leaf may inherit `text-align: center`, but without a reliable text-container route the editor should hide or disable `text-align`. In contrast, `borderColor` can be enabled with a surface fallback only when the editor can guarantee the edit will become visible, including adding `border-style: solid` and `border-width: 1px` if needed.

### CSS Patch Selector Plan

Default visual-style edits should not write inline styles. Inline styles often override hover, active, focus, open, or other state rules, so they make WYSIWYG state editing too destructive.

For normal style edits, V1 uses runtime CSS class patches:

```css
.stable-class.dt-edit-1 {
  color: ...;
}
```

The selector plan is deliberately finite:

- Prefer a stable source class on the actual write target: `.source-class.dt-edit-*`.
- If the target is `td` or `th` and the nearest table has a stable class, use `.table-class td.dt-edit-*` or `.table-class th.dt-edit-*`.
- If no stable class exists, fall back to `tag.dt-edit-*`.
- Do not use repeated class specificity such as `.dt-edit-1.dt-edit-1.dt-edit-1`.
- Do not use `!important` for default-state edits.
- Do not auto-escalate through an unbounded selector search.

This handles common source rules such as `.dr-table td { color: ... }` while keeping the generated patch understandable and exportable.

State-specific edits still use the state-aware scoped selector shape described in State Editing. Hover may use `!important` only for the runtime hover-lock patch because it must keep the frozen editing view visible; export still records the state condition separately.

Patch priority rewrite TODO:

The current hover/active/default write path still contains a risky temporary state-token heuristic. It may recognize active/current/open-like classes with a regular expression and synthesize selectors such as `.active` or `:not(.active)`. This keeps current demos editable, but it is not the desired long-term model because it depends on class naming rather than pure WYSIWYG cascade behavior.

- Treat `dt-edit-*` / `dt-scope-*` classes as range filters, not as specificity boosters.
- Prefer selectors such as `tag:where(.dt-edit-*)` or `source-class:where(.dt-edit-*)` so tool classes do not increase priority.
- Start from low-priority candidates and escalate only when computed-style validation proves the edit did not apply.
- When the selected range contains multiple current computed values for the edited property, avoid escalating into a selector that overwrites the visible higher-priority state.
- Keep hover and active/default state writes on the same selector-planning model instead of maintaining separate ad hoc priority rules.
- If no candidate can make the selected value visible without overwriting currently visible state variants, show an honest write-failure indicator rather than forcing `!important` or semantic state guesses.

### Style Application Validation

After a style patch is written, the editor must read computed style from the actual applied targets and compare it with the expected normalized value.

Validation applies to normal CSS class patch and inline fallback writes. It should be conservative:

- Empty/clear values do not require strict computed validation.
- Color values compare normalized colors.
- Font weight compares normalized numeric weights.
- Font size, width, padding, and radius compare computed numeric values with a small tolerance.
- Font family comparison normalizes quotes and whitespace.

If validation succeeds, clear any previous failure for that control.

If validation fails:

- Keep the attempted patch visible in patch history.
- Mark the edit as not effectively applied.
- Show a red circular exclamation badge next to the affected control label.
- Use the badge hover/title text to explain that the page's original CSS still wins and suggest exporting an AI patch to modify source CSS.

The editor should not silently add `!important` or keep increasing selector specificity after failure. A visible honest failure is preferable to a hidden destructive override.

### Property Capability

Property capability answers: "Should this edit control be shown, enabled, disabled, or hidden?"

The UI should not blindly render controls just because a route exists. A route tells where an edit could go; capability decides whether offering that edit is useful and safe.

Suggested structure:

```js
{
  key: string,
  prop: string,
  group: 'content' | 'typography' | 'appearance' | 'size' | 'insetSpacing' | 'position',
  groupCapability: object,
  show: boolean,
  enabled: boolean,
  targets: Element[],
  route: object,
  reason: string
}
```

Capability is grouped by shared target responsibility and write prerequisites:

- `content`: text content
- `typography`: font family, font size, line height, letter spacing, and text color
- `appearance`: background color, border color, and border radius
- `size`: width and height
- `insetSpacing`: the four padding sides
- `position`: horizontal and vertical offsets

The editor does not assign a semantic identity such as text, card, or surface before computing capability. It derives mechanical traits from the selected depth target, builds each capability group once, and lets member properties reuse that result. A member may still be disabled by its own value-consistency or declaration constraint, but it must not recalculate selection targets or classification.

Capability should consider:

- whether the group's mechanical responsibility fits the current selection
- whether there is a safe write target
- whether multiple targets currently have consistent computed values
- whether a missing explicit value can be given a reasonable default and still visibly take effect
- whether the edit has a high risk of damaging unrelated layout or markup

Layout capabilities need an extra gate because a visual box is not always a safe layout responsibility layer:

- table cells (`td`, `th`, or `display: table-cell`) should not enable width, height, or position nudges by default; padding follows the dedicated table-scope rules
- table objects may enable width and height, but should not route padding controls to descendant `th`/`td`; cell padding is table density, not table object whitespace
- plain inline elements may enable the appearance group, but should not enable size, inset spacing, or position controls because they do not have a stable independent layout box
- direct text leaves should not enable size, inset spacing, or position controls
- stable boxes may enable the appropriate mechanical groups when the route is safe
- in debug/dev mode, unsuitable controls should remain visible but disabled with a clear reason, rather than being hidden

Pipeline:

```text
depthTarget -> mechanicalTraits -> capabilityGroups -> member constraints -> render controls
```

This separation keeps selection, routing, and UI availability from collapsing into one brittle heuristic.

## Selection And Grouping

Selection has two independent axes:

- object ladder: which visual object is being edited
- range ladder: how many similar objects the edit affects

The object ladder moves between stable visual objects near the raw hit. It is for "this text leaf", "this control", "this card", or "this wrapper-surface" style changes.

The range ladder changes the set of same-kind members affected by the current object. Range does not change the object identity itself.

Same-kind inference is handled by `GroupEngine`, which consumes a visual selection rather than a raw DOM element. It should not rely on business class names or semantic labels.

## Range Ladder

Current V1 range ladder has five levels:

1. Current
2. Same parent
3. Same slot
4. Same area kind
5. Cross-area kind

Range and state are orthogonal:

- range decides which same-kind objects are affected
- state decides under which visible/current state the edit applies

For tables, the intended ladder is:

```text
td -> same row td -> same column td -> all td in this table -> td in similar tables
```

For non-table same-slot:

- Use stable part slots only.
- Do not replay pure `nth-child` paths as a general solution.
- A repeated map-rendered list usually benefits more from same parent or same area than from many nested same-slot variants.

`pattern-area` and cross-region matching must be conservative:

- avoid generic `div` expansion
- avoid visually similar but unrelated regions
- require bounded area evidence
- prefer stable class and structure patterns
- use score thresholds and keep rejection evidence for debugging

## State Editing

State editing is based on the frozen visible moment. The editor does not create a semantic state model.

Current state sources:

- default visible state
- hover state captured by delayed snapshot
- mechanically discovered class/attribute diff inside the selected group

### Hover

Hover is captured by delayed snapshot and hover-chain lock:

- delayed snapshot waits for user-input silence
- after settle, the currently visible hover chain can be locked with `.dt-force-hover`
- hover patches use pseudo condition output
- export records `stateCondition`

Runtime editing can emit rules like:

```css
.dt-scope-1.dt-force-hover,
.dt-scope-1:hover {
  background-color: #c03030 !important;
}
```

`.dt-force-hover` keeps the frozen editing view visible. `:hover` represents the real browser interaction for export or baked output.

### Class / Attribute State

Active/current/open/selected-like states are not recognized by name. They are mechanically found as clear diffs inside a group.

The selected object may have a token that similar default objects do not have:

- stable class token
- stable attribute token
- attribute value token

When confidence is high, the token is recorded as `selectedDiffSelector` and used as a scoped state condition. This allows editing the visible `.active` shape without hard-coding the word `active`.

The scoped patch shape is preferred:

```css
.dt-scope-1.some-diff-token {
  background-color: ...;
}
```

`dt-scope-*` means "the selected range for this edit", not a source component. The diff token means "the current visible state condition", not a semantic label.

If confidence is low, fall back to direct target patching and record the limitation.

### Export State Requirements

Patch export must include:

- `applyMode`
- `cssSelector`
- `scopeClass`
- `scopeTargets`
- `stateCondition`
- `suggestedImplementation`
- actual applied targets

This is required because a selector alone cannot express object + range + state.

## Freeze Strategy

Freeze preserves the rendered moment without normalizing source state.

Clock freeze:

- Inject a timer prelude before source scripts run.
- Control `setTimeout`, `setInterval`, and `requestAnimationFrame`.
- Freeze `Date.now()`, `performance.now()`, and RAF timestamps so resume continues from the frozen time instead of jumping to real elapsed time.
- Pause CSS animation with `animation-play-state: paused`.

Interaction freeze:

- After a snapshot, a parent-side transparent shield blocks new demo input.
- The browser pointer no longer enters the iframe document, so it cannot create new hover, click, focus, wheel, drag, or form-input state.
- The editor can still select by temporarily hit-testing through the shield at the pointer coordinate, then restoring the shield.
- The iframe viewport is locked to the frozen pixel size during the draft. Shell resize does not reflow the frozen demo.

Ordinary snapshot:

- freezes clock and interaction immediately
- does not lock stale hover
- captures the current non-hover/default visible state

Presentation pause TODO:

- Consider adding a pause-only mode for pure demo/presentation use, separate from snapshot editing.
- This mode should pause the demo without creating an editable draft.
- Evaluate whether the floating entry button should expose this pause/resume affordance directly.
- The interaction should avoid confusing "pause for presentation" with "snapshot for editing".

Delayed snapshot:

- uses user-input silence as settle condition
- only after settle does it lock the hover chain
- is the path for hover, tooltip, dropdown, and floating UI states

Current settle behavior:

- `SETTLE_IDLE_MS` is 600ms
- pointer, mouse, touch, key, wheel, scroll, and resize activity reset the timer
- iframe document scroll is listened in capture phase
- iframe window resize resets the timer
- wheel/trackpad inertial scroll continues to postpone the snapshot
- cancel, mode switch, ordinary snapshot, apply, refresh, and cancel clear the settle timer and armed state

Delayed snapshot timing TODO:

- Make the settle delay user-adjustable so demos with long hover animations, delayed dropdowns, or async visual reveals can wait longer before freezing.
- Show a circular progress indicator near the pointer while delayed snapshot is armed.
- The ring should visualize the current idle countdown and reset back to zero whenever user input, scroll, or resize activity resets the settle timer.
- This progress UI should make clear that the product currently waits for input silence, not full visual stability.

## Snapshot Model

Snapshots are reset points on one linear editing line.

- There is one active draft at most.
- Clicking snapshot or delayed snapshot creates the active editable draft.
- The active draft is frozen by default.
- Apply records the current draft as the next history item and resumes browsing.
- Cancel discards the draft and resumes browsing.
- Historical tabs show patch details and are not edited out of order.
- Rollback means reset to an earlier point by discarding later edits.
- There is no branch, rebase, or conflict resolution in V1.

Tabs are horizontal sticky-note tabs titled by index only.

Selection/scope switching TODO:

- V1 editing model should remain one snapshot, one active selection.
- If the user has already edited the current selection and then tries to switch object or scope, the editor should warn, intercept, or require an explicit decision.
- The prompt should explain that switching scope after edits may change the meaning of the draft because the patch was authored for the previous selected object/range.
- Possible actions to evaluate: apply current draft first, cancel current draft, or discard edits and switch selection.
- This should prevent an accidental mental-model break where a single draft silently mixes edits for different objects or ranges.

Undo/export safety TODO:

- Add single-step `Ctrl+Z` undo for edits inside the active draft.
- Keep snapshot-level rollback as a separate operation from single-step undo.
- Define how `Ctrl+Z`, cancel draft, apply draft, and rollback interact so users can recover both small mistakes and whole snapshot-level changes.
- Before export, intercept if there is an unapplied draft.
- Evaluate whether export should prompt the user to apply/cancel the draft, or default to applying the latest draft before export.
- If unapplied draft state should survive refresh/reopen, this may require persistence for draft metadata and pending edits.

## Property Controls

Controls are grouped by capability, not by raw CSS property implementation.

Current V1 control set:

Content:

- `textContent`
- `fontFamily`
- `fontSize`
- `fontWeight`
- `lineHeight`
- `letterSpacing`
- `color`

Appearance:

- `backgroundColor`
- `borderColor`
- `borderRadius`

Layout:

- `padding`
- `paddingX`
- `paddingY`
- `width`
- `height`

Position:

- `translateX`
- `translateY`

Normal mode should show enabled controls only.

When `DEBUG_SHOW_ALL_CONTROLS = true`, render the whole V1 set. Unavailable controls stay visible with strikethrough styling and a reason. Debug mode is a code variable, not a UI switch.

Editing panel interaction TODO:

- Improve editing-panel visual polish, spacing, alignment, and control grouping.
- Revisit input interaction patterns for colors, numeric values, units, sliders, selects, copy actions, and disabled states.
- Make default values, applied values, failed writes, and derived values visually clear without adding noisy explanatory UI.
- Keep controls compact enough for repeated editing while preserving readable labels and predictable focus behavior.

### Content Controls

Content ordering:

```text
textContent -> fontFamily -> fontSize / fontWeight -> lineHeight -> letterSpacing -> color
```

Reasoning:

- edit the content itself first
- choose the font family before sizing
- tune size and weight together
- tune reading rhythm after size
- tune letter spacing only after the base type shape is clear
- adjust color last

`textContent`:

- only enabled for a single editable text leaf
- disabled for mixed or complex text
- complex text should show a subtitle hint near the edit title, not a large blocking banner
- never apply `textContent` to a complex container, because it destroys child markup, icons, and inline structure

`fontFamily` candidates:

```text
current selection computed font-family
+ visible page text computed font-family values, deduplicated
+ sans-serif / serif / monospace
```

Constraints:

- no arbitrary font input
- no external font loading
- no `@font-face` modification
- write to text leaves
- require consistent current `fontFamily` across multiple text leaves before enabling
- show long font stacks with truncation and full value on hover/title

`fontSize`:

- special-case range control
- supports `px`, `rem`, and `%`
- slider range is generated around the current computed px value
- unit switching converts from the current px value and does not call `applyStyle`
- only dragging the slider or editing the numeric input applies style
- other range controls keep fixed ranges for now; do not prematurely abstract a generic range config

`fontWeight`:

- belongs in the font-size row because users tune size and weight together
- current implementation uses a weight dropdown rather than a binary B button, because `500`, `700`, and `900` can be visually and semantically different
- candidate values are the standard numeric weights from light to black
- write to text leaves
- require consistent current `fontWeight` across multiple text leaves before enabling

`lineHeight`:

- write to text leaves
- UI uses a unitless multiplier range
- range is `1.0-2.4`
- computed `normal` should be displayed as an effective multiplier based on computed line-height divided by computed font-size
- require consistent current `lineHeight` across multiple text leaves before enabling
- validation compares computed line-height after write

`letterSpacing`:

- write to text leaves
- UI uses px range
- range is `-2px` to `12px`
- computed `normal` should be displayed as `0px`
- require consistent current `letterSpacing` across multiple text leaves before enabling
- validation compares computed letter-spacing after write
- this is most useful for titles, labels, buttons, and short text; avoid over-recommending it for long prose in normal mode

`color`:

- write to text leaves
- require consistent current text color across multiple text leaves before enabling

### Appearance Controls

`backgroundColor`:

- route to the background layer when available
- share the appearance group's targets and classification with border color and border radius

`borderColor`:

- route to the border layer when available
- share the appearance group's targets and classification
- when no existing border layer exists, fallback may target background/surface/control/media anchor
- if the target has no visible border, applying border color must also create a visible border:

```css
border-style: solid;
border-width: 1px;
```

This is the rule of thumb for default values: if a control is visible and enabled, the edit must visibly take effect.

`borderRadius`:

- route to radius layer when available
- otherwise use a safe surface/control/media target
- share the appearance group's targets and classification
- UI uses a dynamic px-only slider, numeric input, and static `px` label
- slider maximum is based on the current target box: `ceil(min(width, height) / 2)`
- if the current computed radius is larger than that visual maximum, include the current value in the range so opening the panel does not clamp existing styles
- do not expose `%` or `rem` in V1; percentage radius can create ellipse behavior that is not a simple WYSIWYG "roundness" control

### Layout Controls

Layout controls are presented as a compact box-model editor instead of independent rows.

The UI has two parts:

- a small engineering-drawing style diagram
- width is shown as a compact engineering-style text dimension, such as `|<--- 宽度 122px --->|`; do not add extra side ticks that duplicate the `|` markers
- height is shown with a vertical dimension line on the right side, with small end caps aligned to the top and bottom of the edited box
- padding labels are shown directly in the diagram as `上留白`, `下留白`, `左留白`, and `右留白`
- every diagram label also shows the current value
- width, top padding, and bottom padding are shown on one line when there is enough horizontal space
- left padding, right padding, and height use a line break so labels remain readable in the narrow sidebar

The inputs below the diagram use a two-column grid:

- row 1: `宽:` and `高:`
- row 2: `左:` and `右:`
- row 3: `上:` and `下:`

A short vertical divider separates the two columns. This keeps width, height, and four-sided padding visible without making the panel tall.

`paddingLeft` / `paddingRight` / `paddingTop` / `paddingBottom`:

- route to the padding/content layer
- UI uses short labels and numeric inputs
- unit is fixed to `px` in V1
- each side writes only its matching CSS property
- higher risk than pure color edits because it can change layout and wrapping
- disabled for table cells and plain inline elements by default
- disabled for table objects by default; do not treat descendant cell padding as table padding
- the older `padding`, `paddingX`, and `paddingY` controls are considered legacy runtime helpers and should not be the default UI

`width`:

- route to the selected visual object's stable box target
- supports `px`, `%`, and `rem`
- uses the same custom unit menu style as font size
- unit switching converts from the current computed px width and does not call `applyStyle`
- `%` conversion uses the parent box width as the base
- `rem` conversion uses the root font size as the base
- appears in the box-model editor beside height
- should avoid near-page containers and low-confidence wrappers
- disabled for table cells and plain inline elements by default

`height`:

- route to the selected visual object's stable box target
- UI uses a numeric input in the box-model editor
- unit is fixed to `px` in V1
- should not be recommended for pure text leaf selections
- must be treated as higher risk than width because it can clip or create overflow
- disabled for table cells and plain inline elements by default

### Layout Side Effects

Layout edits have side effects. The editor should not treat every computed value the same way after a layout-affecting write.

V1 uses three categories:

1. Default-value controls

   `width` and `height` behave like color defaults:

   - before the user explicitly edits them, they display the current computed value in default-value styling
   - while they are still default values, layout side effects may refresh them from the current rendered box
   - default width and height are read from the rendered box (`getBoundingClientRect`) before falling back to computed CSS values, because text metrics, wrapping, font changes, and layout can change the visible box without changing the authored `width` or `height` property
   - after the user edits one, that control becomes configured and should not be overwritten by later side-effect sync
   - changing width can refresh height only if height is still in default-value state
   - changing height should not rewrite width if width has already been configured

2. Pure derived display values

   These are not user configuration values and may always be recalculated:

   - box-model diagram width and height labels
   - `borderRadius` slider max, which depends on the current box size
   - selection and group overlay rectangles
   - unit conversions for width (`px`, `%`, `rem`)
   - position nudge rect validation results

3. Stable configuration values

   These should not be resynced merely because layout changed:

   - colors and border colors
   - font family and font weight
   - line height and letter spacing
   - padding values themselves
   - text content
   - group/range ladder counts

Layout-affecting write sources in V1:

- `width`
- `height`
- `paddingLeft` / `paddingRight` / `paddingTop` / `paddingBottom`
- legacy `padding` / `paddingX` / `paddingY`
- `fontSize`
- `lineHeight`
- `letterSpacing`
- `fontFamily`
- `fontWeight`
- `textContent`

After a layout-affecting write, the runtime should schedule a post-layout side-effect sync for derived values and default-value width/height controls. This applies to every write mode: inline style, generated CSS class, and hover/state CSS class. The currently edited input should be skipped during that sync so typing is not interrupted.

`borderRadius` max is also a derived display value. It is recomputed from `ceil(min(rendered width, rendered height) / 2)`. If a font edit only increases width while height remains the smaller side, the radius range may correctly stay unchanged.

### Position Controls

Position controls are visual intent controls, not final source implementation requirements.

`translateX` / `translateY`:

- route to the selected visual object's anchor
- UI uses px sliders and numeric inputs
- runtime uses a layout-first write strategy:
  - try `left` / `top` when the selected object already has a positioned layout that can safely move
  - otherwise try `margin-left` / `margin-top` for normal flow objects when all selected targets share the same base value
  - validate the result with `getBoundingClientRect()` and require the visual delta to match the requested nudge
  - if layout-first writes do not move the object, fall back to transform using editor CSS variables
- the input value is an absolute visual offset from the un-nudged baseline, not an incremental move from the current rendered position
- before applying a new horizontal or vertical nudge, clear prior editor-generated nudge rules on the same axis, measure the baseline rect, then apply the new offset
- setting the value back to `0` must remove the visual nudge and restore the baseline position
- horizontal and vertical transform fallback nudges must compose without overwriting each other
- export should describe the intent as moving the object horizontally or vertically by N px
- AI source modification may implement the intent with margin, gap, parent layout, alignment, or transform
- do not treat these controls as a substitute for true alignment or spacing controls
- disabled for table cells, text leaves, and plain inline elements by default

## Color And Numeric Inputs

Color controls use:

- swatch
- direct CSS text input
- copy button for the current value
- popover color picker with alpha support
- transparent / clear behavior
- separate default-value marker

Default is input state, not a button. Display values such as `rgb(...) (默认)` when the current value is computed/default and no override has been applied. Clear the marker when the user edits.

The copy button copies the actual CSS value. For default-value display it copies the stored computed value, not the UI suffix. For example, `rgb(26, 35, 50) (默认)` copies `rgb(26, 35, 50)`.

Numeric controls use:

- slider
- exact value input
- unit selector where the property benefits from unit switching

`borderRadius` is an exception: it uses px only. Its range is dynamic and stops at the practical visual limit for a round/capsule shape. Elliptical percentage radii are out of V1 scope and should be treated as an advanced/source-edit case.

Invalid CSS values should be ignored and not recorded in patch history. A style edit must be accepted by the browser before the patch is considered applied.

## Copy Selection Payload

"Copy selection" does not copy a single CSS selector. It copies the object + range + state payload.

Suggested structure:

```js
{
  source: string,
  anchor: string,
  raw: string,
  object: {
    index: number,
    total: number,
    label: string,
    selector: string,
    roles: string[],
    confidence: number,
    reason: string
  },
  range: {
    index: number,
    total: number,
    label: string,
    mode: string,
    count: number,
    members: string[]
  },
  state: {
    label: string,
    source: string,
    selector: string,
    frozenSelector: string,
    token: string,
    value: string,
    confidence: number
  }
}
```

Notes:

- `selector` is anchor positioning information.
- It does not represent the final affected range.
- AI source modification should consume the whole payload.
- Patch, undo, and export must record actual applied targets, not only the anchor selector.

## UI Structure

Selection section:

- title: `选区`
- right action: `复制`
- subtitle: state hint, such as hover or current-state notice
- object ladder
- range ladder

Edit section:

- title: `编辑`
- subtitle: text-not-editable hint when relevant
- light groups: `内容`, `外观`, `布局`
- debug unavailable controls stay visible with strikethrough and reason

Layout notes:

- Multi-line labels and copy payload values should not make row actions look vertically centered against a tall text block.
- Rows should have a minimum height; labels and actions align near the top with fixed margin.
- The selection outline is offset outward so it does not cover the selected object's own border.
- Do not show internal `元素`, `角色`, or raw selector rows in normal UI. Keep those as source data for copy/export/debug.
- Hidden/restore display remains an operation area at the bottom, not part of the main grouped control set.

## Export Strategy

V1 exports the current working result.

Supported export forms:

- download the current single HTML or project archive with live edits baked into rendered DOM/CSS
- copy a concise, human-readable structured prompt that describes source, target count, locator hint, pseudo state, and requested values
- in project mode, apply the same validated document and stylesheet overrides directly to the original project root

The copied prompt must not expose raw Patch JSON. It should preserve enough structure for a person or AI agent to understand the intended targets and changes without forcing the mechanical selector implementation on the source code.

Internal patch/debug records should include:

- source file
- edit kind and value
- object/range/state payload
- actual targets
- before values
- applied selector or scope class
- applied/effective result
- failure reason when computed validation fails
- computed values after write
- expected normalized values
- suggested source implementation

Direct source apply reuses the same cleaned document and stylesheet snapshots used by export. Project mode validates relative paths, rejects conflicting updates, and rolls back already-written files if a later write fails. Single HTML mode atomically replaces the source file selected when the runtime starts; browser requests cannot choose another filesystem path.

Optional future export:

- editable HTML including runtime and linear history

## Future Controls

Do not add these controls only because the computed style exists. They need explicit route and capability design first.

`text-align`:

- This is a valuable future content control, but it is intentionally excluded from the current V1 set.
- User-facing group: Content.
- Suggested UI position: after `fontSize / fontWeight`, before `color`.
- Suggested UI: icon segmented buttons for left, center, and right. Do not add justify in the first version.
- Route kind: `text-container`, not `textLeaves`.
- Route requirement: from the selected text/text object, find the nearest effective block text container inside the current visual selection boundary.
- Do not show it only because the selected text has inherited or computed `text-align`.
- Enable only when the route target is a safe write target: correct text container layer, not a page shell, not an overly broad card/container, and not an inline text leaf.
- For group scope, every member must resolve to the same relative text-container layer.
- Multi-target current `text-align` values must be consistent.
- If the container mixes independent zones such as title, body, icon area, and action buttons, disable or hide the control until a narrower object is selected.
- Flex/grid alignment is a different feature. If the user visually wants item alignment, do not fake it with `text-align`.

`line-height`:

- affects multi-line rhythm and container height
- often invisible on single-line text

`box-shadow`:

- needs a dedicated control
- cannot be represented as a simple percentage range

`border-width` / `border-style`:

- related to `borderColor`
- useful, but adds coupled border editing complexity

`height`, `gap`, `margin`, `align`, `direction`:

- layout edits with high blast radius
- should come after stronger route/capability rules

`icon color`:

- SVG/icon handling must distinguish currentColor icons from complex media SVG

## Legacy Notes

Keep these names documented so future work does not accidentally revive old fallback behavior as product logic.

- `findRepeatedClassGroup`: old class fallback. It is not part of the active range ladder.
- `findVisualFingerprintGroup`: old visual fingerprint fallback. It can over-collect and should not drive new range modes.
- `relativeElementPath` / `elementFromRelativePath`: old `nth-child` same-position helper. It has been replaced by table slot and stable part slot logic.
- `collectCandidates` global pool: historical compatibility support only. It should not drive new range modes.

If any of these helpers remain in code, they should be commented as legacy and guarded from influencing the default ladder.

## Why There Is No Semantic Probe

The old normalizer needed a probe because it claimed to compile a source demo into a semantic state model. That required validating selector reality, rewrite maps, state host granularity, non-editable state exclusions, and dynamic template coverage.

VibePolish makes a narrower claim: a browser-rendered state can be frozen, selected, edited, and exported. Verification should therefore be runtime-based:

- use Chrome
- interact like a user
- inspect screenshots
- verify live edits
- reopen exported HTML

For large demo pages, verification should prefer the visible user path: click the editor controls, hit-test the iframe by real coordinates, fill the right panel, and then confirm with live DOM facts, trace, patch JSON, and exported HTML. Locator-only verification is a convenience, not the product contract.

No probe should attempt to prove source-state semantics, because the product does not promise them.

Runtime test policy:

- `npm run test:runtime-pw` is the active runtime behavior test entry.
- The old CDP runtime runner has been removed. It allowed too many non-user-path shortcuts and could hide product interaction problems.
- Runtime tests may read product export contracts from bridge: `selectionPayload()`, `aiPatchPayload()`, `currentHtml()`.
- Runtime tests may read product computed state from bridge: `ready()`, `meta()`, `capabilities()`, `editCount()`, `settleIdleMs()`.
- The bridge must not expose write shortcuts or user-path bypasses: no `setObjectIndex()`, `setScopeIndex()`, `applyStyle()`, `applyText()`, `selectBySelector()`, `selectByCandidate()`, `enumerateCandidates()`, or `resetDraft()`.
- This follows layered testing: case tests may trust thicker product calculations that are already shown by the editor, while visible UI interaction still validates the user path for editing and applying changes.
- Runtime behavior cases should not use highlight overlays or right-panel wording as primary assertions. Use bridge state/export contracts for product-computed facts, then use real DOM/computed style for visible results. Keep thin UI mapping checks in dedicated smoke cases.
- Tests should validate with `getComputedStyle()`, `getBoundingClientRect()`, DOM text, selector hit counts, injected CSS rules, exported HTML, and AI Patch payloads.
- Playwright trace is the preferred human-review artifact; headed CDP window orchestration is no longer part of the maintained test path.

Runtime test TODOs:

- Keep case tags and `estimatedDurationMs` close to the Playwright case definitions.
- Use observed per-case duration to override first-run `estimatedDurationMs` for future scheduling.
- Optionally record lightweight run-level environment data such as CPU count, load average, free memory, browser launch duration, timeout count, and total run duration.
- Add an explicit `--workers=auto` mode that chooses worker count from local history and lightweight environment data. Do not make this adaptive mode the default until it has proven stable.

## Engineering Refactor Flow

This is the preferred order for the next engineering migration steps. The goal is to reduce review noise and protect runtime behavior while gradually moving from the legacy runtime toward a clearer React/Vite project structure.

1. Keep `build:skill` syncing the live generated skill mirror.

   This is intentional so Codex E2E always uses the latest generated `skills/vibepolish` mirror after a build.

2. Guard generated mirror consistency and runtime behavior.

   Engineering tests check generated markers, dist/live mirror equality, the frozen runtime boundary, and the read-only bridge. Playwright runtime cases cover the golden behavior paths.

3. Keep Playwright runtime tests as the active runtime behavior suite.

   Runtime behavior cases should use visible UI for edits, bridge/computed state for product facts, and real DOM/computed style for results.

4. Close naming inconsistencies.

   Use `vibepolish` as the single product, skill, and artifact name. Do not generate parallel `freeze-editor-*` asset aliases.

5. Isolate generated artifacts.

   Keep `standalone/` committed as the directly usable Node distribution, keep `skills/vibepolish` committed as the directly usable agent skill wrapper, ignore `dist/` as local build cache, and decide generated wrapper fixture policy separately.

6. Extract read-only tools first.

   Move low-risk helpers such as selector generation, geometry, and formatting before touching behavior modules.

7. Extract core behavior modules last.

   Selection, scope, routing, CSS writer, freeze, and export should be moved only after the build/sync boundary, engineering tests, and runtime equivalence checks are in place.

## Source Directory Structure

The source tree is organized by responsibility, not by where code happened to come from during the legacy migration.

```text
src/
  app/
    bootstrap.tsx       app startup, wrapper inputs, test mode, beforeunload, React mount
  ui/
    Panel.tsx           editor panel shell
    PanelRuntimeContext.tsx  React context bridge for PanelViewModel + dispatch
    components/         panel sections, steppers, edit controls, popovers, and patch panels
    controls/           reusable editor controls
    styles/             editor UI CSS and tokens
    feedback.ts         status, toast, clipboard feedback
  core/
    legacy-runtime.ts   current DOM runtime implementation and migration baseline
    apply.ts            apply-side helpers; current CSS/text write pipeline remains in legacy runtime
    export.ts           export cleanup and AI Patch compact payload helpers
    state.ts            editor state helpers plus serializable PanelViewModel, commands, and runtime store contract
    properties.ts       property definitions, grouping, and capability display model
    test-bridge.ts      read-only test bridge textarea packaging
  shared/
    css.ts              generic CSS string helpers
    dom.ts              generic DOM read helpers
    format.ts           generic formatting/escaping helpers
    geometry.ts         generic rect/geometry helpers
```

Directory rules:

- `src/app` owns startup and environment wiring: reading wrapper-provided HTML, reading source name, detecting `dt-test`, mounting React, and installing dirty-page protection. Do not put selection, scope, CSS source, or write strategy here.
- `src/ui` owns editor interface code: panel components, controls, styles, status/toast/copy feedback, and the React context bridge. UI code may display product state but should not decide style routes, selector priority, or export payload semantics.
- `src/core` owns product/runtime behavior. During migration, `legacy-runtime.ts` remains the behavior-frozen DOM runtime baseline. New files in `core` should be introduced only when their boundary is stable and covered by engineering/runtime tests.
- `src/core/state.ts` is the React migration boundary for the right panel. Core keeps the source of truth, publishes a serializable ViewModel, and accepts typed commands; React consumes only `viewModel + dispatch`.
- React owns the right panel DOM, edit-control events, and initial edit-control values: capture controls, snapshot tab strip, selection stepper, edit controls, color popover, patch details, and footer actions. The DOM runtime still owns product behavior and executes typed `PanelCommand` edit actions; the React commit hook is limited to small DOM side effects such as textarea sizing and global menu/popover close listeners. It must not render right-panel HTML strings, bind per-control input/click handlers, or initialize the panel by scanning the sidebar DOM with `syncControls()`.
- `src/core/properties.ts`, `src/core/export.ts`, `src/core/apply.ts`, and `src/core/test-bridge.ts` are extracted stable boundaries. They may be reused by the DOM runtime and a future CDP runtime, but they must not start owning selection, scope, CSS source, hover/active state, or write-priority decisions. In particular, `apply.ts` currently owns only apply-side layout effect helpers; the real text/CSS write pipeline remains behavior-frozen in `legacy-runtime.ts`.
- `src/shared` owns generic utilities with no VibePolish product meaning. Shared helpers must be deterministic and side-effect-light.
- Do not introduce a universal DOM/CDP adapter. The current direction is to keep the DOM runtime as the baseline and later explore CDP as a separate runtime/host implementation.
- CDP-sensitive behavior should stay out of incidental refactors: CSS source, specificity, hover/active/pseudo state, write priority, patch application, freeze/time control, and export payload semantics.

Generated and distribution directories:

```text
dist/                  ignored local build cache
standalone/            committed directly usable Node distribution
skills/vibepolish/     committed generated live skill mirror for Codex E2E
templates/             source templates used to regenerate standalone and skill artifacts
tests/                 engineering and Playwright runtime tests
```

`build:skill` intentionally syncs `skills/vibepolish/` so Codex E2E uses the latest generated skill. Hand-edit source files and templates, not generated mirror files, unless the task is explicitly about the generated artifact.

## TODO Index

- Patch Priority Rewrite: replace temporary state-token specificity heuristics with a low-priority selector plan plus computed validation.
- Delayed Snapshot Timing: make delay configurable and show pointer-side circular countdown/reset feedback.
- Playwright Runtime Tests: add local runtime history, observed-duration scheduling, lightweight environment data, and explicit `--workers=auto`.
- CDP Backend: introduce an optional Chrome DevTools Protocol backend for deeper browser facts and CSS source information.
- Selection/Scope Switching Guard: warn or intercept when a user edits one selection and then tries to change object or range inside the same draft.
- Editing Panel Polish: improve editing area visual style, control alignment, input interactions, and value-state clarity.
- Editor Shell Refactor: revisit sidebar, iframe wrapper, overlays, and possible floating-window editor layout.
- Product Floating Entry: add a polished VP/LD-style floating entry point for opening or activating the editor.
- Undo And Snapshot Rollback: support single-step `Ctrl+Z` separately from snapshot-level rollback.
- Export Draft Safety: intercept export with unapplied drafts or define default apply-before-export behavior, possibly backed by persistence.
- Presentation Pause: add a pause-only demo mode and evaluate exposing it from the floating entry button.
