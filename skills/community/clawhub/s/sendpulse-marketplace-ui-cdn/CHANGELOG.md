# Changelog — sendpulse-marketplace-ui-cdn

All notable changes to the SendPulse Marketplace UI kit (CDN route). Format follows
[Keep a Changelog](https://keepachangelog.com/); versioning follows
[SemVer](https://semver.org/) — MAJOR for a rewrite of the rules or structure, MINOR for new
guidance or reference files, PATCH for corrections to existing facts.

## [1.1.0] — 2026-08-27

### Added

- `adapters/` — installing this skill in tools that are not Claude Code, mirroring the layout the
  other SendPulse skills use. `adapters/README.md` states plainly what survives on each platform:
  everything, where the assistant has a shell; Steps 0–5 plus a manual checklist, in a chat window.
- `adapters/chatgpt/instructions.md` — the condensed, self-contained form of the skill for a Custom
  GPT, a ChatGPT Project or a Gemini gem. It names no file paths in its own flow and is 7.9k
  characters, inside the *Instructions* field's 8000-character limit with little headroom.
- `adapters/chatgpt/pocket-guide.md` — the second tier for those tools: the icon rules, the palette,
  the sixteen gaps as a symptom table, and the pre-delivery checklist, which is the manual form of
  the three checkers. Step 7 and the delivery checklist in `SKILL.md` now point at it for anyone
  working without a shell.
- `adapters/gemini/GEMINI.md` and `adapters/cursor/sendpulse-marketplace-ui.mdc` — repo-level rule
  files for gemini-cli and Cursor, both of which keep the full reference folder and its checkers.

### Changed

- *Scope* now says what degrades without a filesystem or a shell, instead of leaving a chat-window
  reader to infer it.
- Step 1 and Step 4 lead with the rule and follow with the argument, rather than the reverse. The
  intro, the 28-custom-properties paragraph and the `var()`-naming paragraph now do the same: the
  instruction is the bold lead-in, the reasoning follows it.
- No rule in `SKILL.md` is left as a pointer alone. The intro states the two rules it used to
  delegate to Step 2 and Step 4, and Step 4's width-cap bullet names the wrapper and the 364px value
  instead of deferring to *Controls do not stretch*. Step numbers remain, as locators for the detail.
- The Step 0 file table carries a `Use` column — COPY, READ, LOOKUP or SHELL per file — so how a
  file is meant to be used is a keyword rather than something to infer from the *When* column.
- Step 1 and Step 6 now state the no-filesystem path, as Step 7 and the delivery checklist already
  did: `tokens.css` is reproducible from `adapters/chatgpt/instructions.md`, and the sixteen-gap
  index from `adapters/chatgpt/pocket-guide.md`.

### Fixed

- Step 7 listed the `verify.mjs` checks twice, the second time as "the other fourteen" where the
  paragraph above it and the Step 0 table both say nineteen. The stale duplicate is removed.

Nothing in the Claude Code path changed: no reference file moved or changed content, and the
`adapters/` files are never loaded on it.

## [1.0.0] — 2026-08-25

### Added

- Initial release. Named `sendpulse-marketplace-ui-cdn` after its delivery route: this skill covers
  the prebuilt bundle linked from the CDN, and an app that instead receives the design system
  through its own LESS build is a different route with a different class list, covered by a
  separate skill. The route is in the name so there is no unmarked one that reads as the default.
- `SKILL.md`: the class vocabulary of `sp-marketplace-app-ui.min.css` — wiring the CDN stylesheet,
  the custom properties the bundle reads but never defines, layout and spacing inside the host
  iframe, light/dark theming (`?theme=dark`, `ma-dark`), the structural gaps the bundle leaves, and
  the checks to run before calling a screen done.
- `references/gaps.md`: sixteen classes that exist, look like they should work, and don't — one
  section per class with an index at the top, so the class you are fighting is greppable by name.
  Every cause re-measured in Chrome against the live build before release; the `.input-group`
  entry's explanation was wrong and is corrected (the table rules are present — Chrome refuses
  `display:table-cell` on `<input>`/`<select>`, and the bundle floats both children at 100%).
- Step 4: the frame size is stated per context — 796px is the marketplace *settings* frame, while a
  widget window is another size — which is the reason the app declares no width of its own rather
  than a detail beside it.
- Step 5: the `?theme=` / `?lang=` / `?access=` contract and the `ma-dark` / `ma-light` class on
  `<html>` verified against shipped integrations, including that all three params are re-attached to
  the post-login redirect. No shipped integration offers a theme switcher.
- Step 7 covers changing a screen that already exists, not only building a new one: declaring the
  prefixes a repo already uses, not declaring one the bundle owns, and fixing what you touch rather
  than what you find. Measured against four shipped integrations (15–29 prefixes each).
- `check-classes.sh` and `verify.mjs`: `--app-prefix` is now repeatable and accepts a comma-separated
  list. One prefix suits a new app; an existing one has many, and the single-value flag made the
  checkers unusable there (166 findings on one repo, with no way to narrow them).
- `references/verify.mjs`: executed end to end against every shipped page in both themes, plus a
  deliberately broken control page to prove each assertion fires. Three defects found and fixed —
  the dark pass disabled the only stylesheet of a single-theme app (cascading false positives);
  the `.input-group` check tested the parent's `display`, which is `table` even when the layout is
  broken (false negative); and the body-background check could not see the gap it names, a body
  left `#fff` in the dark build.
- References: component catalogue (`components.md`), a correct `<head>` baseline
  (`starter.html`), the light palette as lookup (`tokens.md`), the 28 undefined custom properties
  (`tokens.css`), the structural gaps as copy-paste CSS (`bundle-fixes.css`), a kitchen-sink page,
  grep-able `classes.txt` (1411) and `icons.txt` (536).
- `examples/settings-screen.html`: one whole integration screen, composed — the panel as the
  layout, per-control width caps beside full-width mapping rows, the two glyphs restraint allows,
  and the host-driven theme switch. `kitchen-sink.html` shows the components; this shows a screen.
- `examples/amazon-connections-screen.html`: the other screen shape — a plan-gated list of
  connected marketplaces: the `paid` family with the badge inset, separated `.list-group` cards
  with the connected state on the left border, a row kebab with the eight lines of JS the
  CSS-only bundle leaves to you, and a text-first empty state.
- Checkers: `check-build.sh` (the wiring: the bundle linked from the CDN rather than self-hosted,
  `tokens.css` and `bundle-fixes.css` present and linked in order, app CSS last, one theme build
  live at a time, `ma-dark` on the root, and every `var()` name checked against the 28 that exist),
  `check-classes.sh` (no toolchain, greps templates for classes the bundle does not define),
  `verify.mjs` (the same check against the rendered DOM plus 19 more, in Playwright), `refresh.sh`
  (re-derives both lists from the live CDN and prints what drifted).
- Runtime assertions for the Step 6 gaps a rendered page can be measured for: a status dot that comes
  out grey inside a `.list-group-item`, an `.avatar` off its baseline in a dropdown, a `.modal` shown
  with no backdrop / `modal-open` / `.in`, a `.settings-toggle-radius` overlapping its own label, and
  the four classes that are styled but inert (`.accordion`, `.tab-content`, `.bootstrap-select`,
  `.settings-toggle-btn-sm`). Each was verified firing against a purpose-built broken page and silent
  on `kitchen-sink.html`.
- A scope note at the top of `SKILL.md`: the wiring steps cover the CDN stylesheet, and an app that
  already receives the design system through its own build pipeline is left alone. The skill is
  self-contained — it names no other skill as a prerequisite.
- A staleness rule: re-run `refresh.sh` before trusting any count, class list or token value once
  the verification date is more than three months old.
