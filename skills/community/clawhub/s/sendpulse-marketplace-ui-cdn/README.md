# SendPulse Marketplace UI kit — `sendpulse-marketplace-ui-cdn`

An AI skill that teaches an assistant (Claude Code/Desktop, Cursor, ChatGPT, …) to build SendPulse
integration UI out of the shared design system as served from the CDN —
**`sp-marketplace-app-ui.min.css`**: the class vocabulary behind SendPulse-styled buttons, forms,
panels, alerts, labels, badges, modals, side panels, dropdowns, tables, `sp_icons`, colour tokens,
layout utilities and the light and dark themes.

It's a plain folder — `SKILL.md` (instructions), `examples/` (whole screens) and `references/`
(on-demand docs, baselines and checkers). No installation, no dependencies of its own.

> **Scope is the CDN stylesheet.** The skill is complete and standalone: it needs no other skill
> installed, and it names none as a prerequisite. If an app already receives the design system some
> other way — through its own build pipeline rather than the CDN `<link>` — its wiring is set up
> already and the skill says so rather than fighting it; the class vocabulary, icons, layout and
> restraint rules apply either way.

## What it gives your AI assistant

- **The vocabulary, not invention** — every element built from a class the bundle actually defines,
  in any framework or none: the same classes produce the same screen in Angular, React, Vue or
  plain HTML.
- **Correct wiring** — the CDN link and where the app's own CSS goes relative to it, and why
  vendoring a copy breaks both design tracking and the bundle's root-relative `url(/img/…)`.
- **The bundle's gaps, filled** — the 28 custom properties it reads and never defines, and the
  structural holes it leaves, both as copy-paste files rather than prose.
- **Theming discipline** — `?theme=dark` from the host, `ma-dark`, and app CSS that survives both.
- **Grep-able truth** — 1411 classes and 536 icon names as flat lists, so a name gets checked
  instead of guessed.
- **Checkers** — the repo's wiring, templates against the class list, and the rendered DOM against
  20 rules.

## Structure

```
SKILL.md                        # core playbook (entry point for the AI)
examples/
  settings-screen.html          # a whole form-shaped screen, composed — start here
  amazon-connections-*.html     # the other shape: plan-gated list, cards, row kebab + its JS
adapters/                       # installing this skill outside Claude Code
  README.md                     # what survives on each platform, and how to install it there
  chatgpt/instructions.md       # the condensed, self-contained skill — fits the 8000-char field
  chatgpt/pocket-guide.md       # icons, palette, the gaps, the manual pre-delivery checklist
  gemini/GEMINI.md · cursor/*.mdc
references/
  components.md                 # component catalogue: every load-bearing class + its markup
  gaps.md                       # sixteen classes that look like they work and don't — one per class
  starter.html                  # correct <head> for a standalone integration — copy, don't retype
  tokens.md                     # the light palette as lookup — for when no semantic class covers it
  tokens.css                    # the 28 custom properties the bundle reads and never defines
  bundle-fixes.css              # the structural gaps the bundle leaves, as copy-paste CSS
  kitchen-sink.html             # every load-bearing component rendered correctly
  classes.txt · icons.txt       # 1411 classes, 536 sp_icons names — grep-able lookup
  check-build.sh                # wiring: the CDN link, tokens.css, bundle-fixes.css, load order
  check-classes.sh              # greps templates for classes the bundle doesn't define. No Node
  verify.mjs                    # the same check against the rendered DOM, +19 more, in Playwright
  refresh.sh                    # re-derives both lists from the live CDN and prints what drifted
VERSION · CHANGELOG.md · LICENSE
```

Open `examples/settings-screen.html` in a browser first — add `?theme=dark` for the dark build — to
see what a finished integration screen looks like; `examples/amazon-connections-screen.html` is
the list-shaped counterpart. `references/kitchen-sink.html` is the same vocabulary spread out
component by component, and it doubles as the control for the checkers.

## Install

**Claude Code / Claude Desktop** (the skill lives in the `sendpulse-skills` monorepo — clone once,
then copy or symlink the skill folder):

```bash
git clone https://github.com/sendpulse/sendpulse-skills

# User-level (all your projects):
cp -R sendpulse-skills/sendpulse-marketplace-ui-cdn ~/.claude/skills/
# Or project-level (committed, shared with everyone who clones the repo):
cp -R sendpulse-skills/sendpulse-marketplace-ui-cdn .claude/skills/
```

A symlink instead of `cp -R` means a plain `git pull` updates the skill in place. The folder name
must stay `sendpulse-marketplace-ui-cdn`. It loads automatically — just ask for a screen ("build
the settings screen for this integration") and the skill triggers on its description.

**Claude.ai / Claude Desktop upload:** zip the folder, then *Settings → Capabilities → Skills →
Upload skill*.

**Cursor / ChatGPT / Gemini / other LLMs:** see [`adapters/README.md`](adapters/README.md) — it
ships a rule file for Cursor and gemini-cli (both keep the full folder and its checkers), and a
condensed, self-contained instruction block plus a pocket guide for ChatGPT and Gemini gems, where
there is no filesystem. The scripts only work where the assistant can run commands; in a chat
window the pocket guide's checklist stands in for them.

## Using the checkers in your app repo

Both scripts read `classes.txt` from beside themselves, so they run from anywhere. But `verify.mjs`
resolves `playwright` from the **working directory** — run it from the repo that installed
playwright. Easiest is to copy the folder in:

```bash
cp -R sendpulse-marketplace-ui-cdn/references tools/sp-ui

# no toolchain needed
tools/sp-ui/check-classes.sh --app-prefix app- $(find src -name '*.html')
# an existing repo, several prefixes:
tools/sp-ui/check-classes.sh --app-prefix 'rz-,settings-,wsr__' $(find resources -name '*.html')

# the rendered page, both themes
npm i -D playwright && npx playwright install chrome
node tools/sp-ui/verify.mjs http://localhost:4200 --app-prefix app-
```

`--app-prefix` declares your own classes so they aren't reported as invented ones. It is
**repeatable and accepts a comma-separated list** — a new app needs one prefix, an existing one
usually has many, and listing them is how you get from a wall of findings to the few that are
actually wrong. Never declare a prefix the bundle already owns (`color-`, `gap-`, `btn-`, …):
that hides real findings — `color-muted` is not a class, `color-muted-link` is.

## Requirements on the SendPulse side

Nothing but network access to the CDN. The stylesheet is public.

## Staying current

Every claim in `SKILL.md` is derived from the live CDN and dated. `classes.txt` and `icons.txt` are
the parts that go stale when the design system ships a change, so don't trust the date — re-derive
them:

```bash
references/refresh.sh            # exits 0 if nothing drifted
references/refresh.sh --write    # and update the lists
```

A line saying a class *disappeared* is the one to act on: grep `SKILL.md`, `components.md` and
`kitchen-sink.html` for it, because something in there still recommends it.

## Contributing & versioning

Semantic versioning; the current version lives in `VERSION` and in the `SKILL.md` frontmatter (keep
them in sync). Log changes in [CHANGELOG.md](CHANGELOG.md). When the live bundle and this skill
disagree, the bundle wins — fix the skill and note it in the changelog.

## License

MIT — see [LICENSE](LICENSE).
