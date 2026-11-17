# Runtime Contract

Use this contract for paged reading reports and single-screen presentations generated from the bundled template.

## Supported Core

The current core supports:

- Fixed 16:9 canvas scaled inside the browser viewport
- Hash-addressable pages
- Reading and single-screen presentation modes
- Per-page reveal progress retained while moving between pages
- Separate step navigation and whole-page navigation
- Click-to-advance in presentation mode
- Whole-page previous/next buttons
- Fullscreen entry and exit
- Page number
- Auto-hiding controls
- Source evidence modal
- Lightweight report text/image editing with unified undo/redo
- Session-scoped refresh recovery and export to a newly named HTML
- Offline local assets and portable packaging

Do not promise dual-screen presenter view, embedded speaker notes, free element movement, layout rebuilding, interactive chart authoring, animation editing, cross-page morphing, durable version history, or browser ZIP export from this core. Read `content-editor.md` before authoring or testing editable content.

## DOM Contract

Keep these hooks when generating or redesigning a deck:

```html
<main class="deck" id="deck" data-mode="presentation" data-taohtml-step-contract="fragment-v1">
  <section class="slide active" data-title="...">
    <div class="fragment" data-step="1">...</div>
    <div class="fragment" data-step="1">...</div>
    <div class="fragment" data-step="2">...</div>
  </section>
</main>
```

- `.deck`: runtime root and current `data-mode`.
- `.slide`: one paged scene; DOM order is page order.
- `.slide.active`: the one visible page.
- `.fragment`: an element controlled by a presentation step.
- `data-step`: optional positive step number. Elements sharing a number change together. Fragments without it are numbered in DOM order for backward compatibility.
- `.fragment.visible`: a step already revealed in presentation mode.
- `data-taohtml-step-contract="fragment-v1"`: the current single controlled-presentation-step contract. QA normalizes `.fragment` plus `data-step` into per-page `data-taohtml-step` values through this named contract. A future equivalent state-node system must declare a new contract and update Runtime and QA together; it must not bypass the zero-step gate with an unrelated selector.
- `data-step-index` on each slide: current numeric presentation state, available to page-specific CSS.
- `data-taohtml-interactive`: mark a custom chart, attachment viewer, or other interactive subtree whose clicks must remain local instead of advancing the report.
- `#pageIndicator`: current page and total pages.
- `#prev` / `#next`: whole-page navigation controls.
- `#modeToggle`: reading/presentation switch.
- `#fullscreenToggle`: fullscreen control.
- `#editToggle`: enter/leave the bundled content editor.
- `data-taohtml-edit-lock`: exclude a system, fixed-brand, or other non-report subtree from editing.

Page-specific design may add classes and data attributes, but must not remove these hooks.

## Input Contract

### Presentation mode

- `ArrowRight`, Space, or a blank-page click advances one fragment; after the last fragment, it moves to the next page.
- `ArrowLeft` reverses exactly one fragment. At the initial state it is a no-op and must never perform whole-page navigation.
- `PageDown` moves to the next page immediately without completing remaining fragments.
- `PageUp` moves to the previous page immediately.
- `#prev` and `#next` always move by one whole page.
- Returning to a page restores its prior fragment stage.

### Reading mode

- Every fragment is visibly complete.
- `ArrowRight`, `ArrowLeft`, Space, `PageDown`, `PageUp`, blank-page click, and navigation buttons move by whole page.
- Switching from reading to presentation resets the current page to its first presentation state.

Only an unconsumed primary-button click on report whitespace is a blank-page click. Links, buttons, attachments, source viewers, forms and their controls, editable content, dialogs, menus, media, embedded documents, SVG/canvas charts, semantic interactive roles, and `[data-taohtml-interactive]` subtrees consume their own clicks rather than advancing the report. An open modal blocks report navigation regardless of its clicked descendant.

### Edit mode

- `setEditing(true)` preserves `mode`, page index, and every stored stage while exposing all fragments for editing.
- Page-step keys, blank-page advance, reveal transitions, and report animations pause. Previous/next page buttons remain available for moving through the same edit session.
- System controls and locked subtrees never become content targets.
- `setMode`, `nextStep`, and `previousStep` do nothing until `setEditing(false)` restores normal Runtime behavior.

### Controls and fullscreen

- The auto-hide policy applies while presentation mode is fullscreen. `#prev`, `#next`, and the top-right more control are hidden immediately on entry; `#pageIndicator` remains visible. Outside this state, controls remain visible.
- Only a trusted `mousemove` that represents actual pointer movement may reveal hidden controls. The Runtime must ignore browser-generated pointer-coordinate relayout events during a short post-entry fullscreen stabilization window before accepting mouse movement. Keyboard or presenter-remote keys, blank-page clicks, `pointerdown`, `fullscreenchange`, mode changes, and Runtime navigation calls must not reveal or flash them.
- After mouse movement reveals the controls, about two seconds of pointer inactivity hides them again.
- Opening the more menu, entering edit mode, or actively interacting with the controls keeps them visible and suspends hiding. Closing the menu, leaving edit mode, or ending control interaction rearms the two-second hide timer when the auto-hide policy still applies.
- Entering or exiting fullscreen closes the more menu and sets its toggle to `aria-expanded="false"`. Fullscreen changes synchronize the correct hidden or visible state without treating the event as pointer activity.
- If an implementation hides the cursor with the controls, the same trusted `mousemove` must restore it. Cursor hiding is optional.

## Public API

Expose `window.TaoHtmlRuntime` with:

```text
getState()
setMode("reading" | "presentation")
showPage(index)
nextStep()
previousStep()
nextPage()
previousPage()
toggleFullscreen()
setEditing(true | false)
```

`getState()` returns a copy containing `mode`, zero-based `index`, the per-page `stages` array, and boolean `editing`. Runtime changes dispatch `taohtml:statechange` on `window` with the same state snapshot in `event.detail`.

The `editing` field and `setEditing()` method are additive. Existing consumers may continue reading only `mode`, `index`, and `stages`; their meaning and types do not change. Event consumers must ignore unknown future snapshot fields. Editor consumers must not mutate `event.detail` and must use `setEditing()` instead of replacing the core Runtime or synthesizing navigation state.

Optional future modules must use this API and event rather than replacing core navigation.

## Performance Rules

- Do no work while the presenter is idle except the control-hide timer.
- Animate with `transform` and `opacity` when possible.
- Do not start hidden-page animations or media.
- Keep large media and full fonts out of the single file when they make loading or interaction visibly slow.
- Add optional modules only when the confirmed brief requires them.

## QA Contract

Before delivery, verify:

- A deck whose initial mode is presentation has at least one controlled presentation step across the report. Reading mode may validly contain zero steps.
- Reading mode exposes all current-page fragments.
- Presentation mode starts with unrevealed fragments.
- Step and whole-page keys have different behavior.
- Elements that share `data-step` change together.
- Whole-page jumps work before all fragments are revealed.
- `ArrowLeft` at stage 0 leaves both page index and all stored stages unchanged; `PageUp` remains the explicit previous-page input.
- Returning to a page restores its stage.
- Hash routes and page numbers match the active page.
- Links, attachments, charts/interactive regions, forms, editable content, dialogs, menus, and media do not advance steps or pages.
- Controls and fullscreen actions do not advance the report. Presentation fullscreen remains hidden after the post-entry stabilization window; keyboard, blank-click, `pointerdown`, browser coordinate relayout, and `fullscreenchange` do not reveal controls; the first real mouse movement after stabilization does; idle time hides them again; menus, edit mode, and active control interaction pin them visible; the page number stays visible throughout.
- Direct HTML, Report IR Compiler output, and all built-in visual systems retain the same bundled Runtime script and behavior; themes may style controls but must not fork navigation or visibility state.
- Edit mode pauses keyboard/blank-click/reveal advance, keeps page buttons usable, locks system UI, and restores the pre-edit Runtime state on exit.
- Text, image replacement, and crop focus share Ctrl/Cmd undo and redo; refresh recovery and export/reopen pass `content-editor.md`.
- Asset, console, and visible-bound checks pass at the target viewport.
- Every active slide's rendered rectangle covers the deck canvas within the QA tolerance at each target viewport.
- Independent visible text labels, including HTML text and SVG `<text>`, do not intersect and retain the small QA safety gap. SVG labels and positioned/transformed HTML labels remain strict; a shallow HTML Range font-metric overlap is excluded only when both static, independently untransformed layout boxes are actually separate, and that exclusion is recorded in QA JSON. Exempt an intentional overlay only on the exact text owner with `data-qa-ignore-text-collision="reason"`; the report must list every opt-out.
