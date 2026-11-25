# Optional polish

Offer these only after the look is applied. Everything here is optional; the design skill works fully without any of it. Ask before installing anything. Installing changes the student's Claude Code, and a restart or reload is needed afterwards. Each project is third party; point to its page and let the student decide.

Command status: checked against each project's README on 2026-10-16 unless marked unverified. READMEs change, so if a command fails, check the project page.

## Baseline: frontend-design (official, free)

An Anthropic plugin that nudges Claude toward distinctive, careful screens instead of generic ones. Good to have while building features.

```
claude plugin marketplace add anthropics/claude-plugins-official
claude plugin install frontend-design@claude-plugins-official
```

Or inside Claude Code: `/plugin install frontend-design@claude-plugins-official`. Restart Claude Code afterwards.

Unverified: the official README confirms the `/plugin install <name>@claude-plugins-official` form, but its page does not list the plugin names. The name `frontend-design` should show up under `/plugin` then Discover. If it does not, tell the student and skip it. In some versions the official marketplace is already added, so the first command may say "already added", which is fine.

The Shipyard look always wins: if frontend-design suggests colours or fonts, keep the app's tokens and let the script change the look.

## After the first real build: Impeccable (free)

A design review and polish tool (Apache-2.0, impeccable.style, github.com/pbakaus/impeccable). Best used on one page at a time, with the page open in front of Claude. Warning to say out loud: it can use a lot of the Claude Pro allowance, so run it on one page, not the whole app.

Install, either way (verified in its README):
```
/plugin marketplace add pbakaus/impeccable
```
then open `/plugin` and install Impeccable from the list. Or, from the app folder:
```
npx impeccable install
```
(it asks where to install; `npx impeccable update` refreshes it; needs Node. Add `--providers=claude --scope=project` to skip the questions.) Reload Claude Code afterwards. The first time, run `/impeccable init`.

Useful commands: `/impeccable critique` (review of hierarchy and clarity), `/impeccable audit` (technical quality), `/impeccable polish` (final pass). Typing `/impeccable` alone lists the rest. It also installs hooks that run when files are edited; mention that.

Unverified: the README lists the plugin simply as Impeccable, with no separate package name.

After any Impeccable change, run `npm run check:design` again. It often adds hard-coded colours or gradients that the check will catch.

## Advanced: UI UX Pro Max (big style library)

A large library of styles and palettes (MIT, github.com/nextlevelbuilder/ui-ux-pro-max-skill). Needs Python 3 (`python3 --version`). Do not install Python for the student: tell them to install it from python.org and ask first. Verified commands:
```
/plugin marketplace add nextlevelbuilder/ui-ux-pro-max-skill
/plugin install ui-ux-pro-max@ui-ux-pro-max-skill
```
Or the project's own CLI: `npm install -g ui-ux-pro-max-cli` then, in the app folder, `uipro init --ai claude` (`npx ui-ux-pro-max-cli init --ai claude` if the global install gives a permissions error). Without Python 3 it will not work, so skip it. Treat anything it suggests as input for a look file, and still apply it with `apply-design.mjs`. Add `--global` to `uipro init` only if the student wants it in every project.

## Not recommended for beginners (skipped on purpose)

- Figma MCP: the free plan allows only a handful of requests a month.
- v0 and Google Stitch: need separate accounts and sign-ins.
- 21st.dev: needs an API key.

## Accessibility the eye misses (checked by verify and Lighthouse)

- Icon-only buttons and links, and the logo link when its text is hidden on phones, need `aria-label`.
- Every pack, light and dark, keeps body text at 4.5:1 contrast and large text and icons at 3:1. Check muted text and accent-on-surface pairs in both modes.
- Animate only `transform` and `opacity` (Lighthouse "non-composited-animations"); respect `prefers-reduced-motion`.
- Tap targets at least 48px with 8px between them.
- Before calling a look done: `verify.mjs <appDir> --only hygiene,lighthouse` on the deployed preview.
