# Screenshot to Code — one screenshot, one honest component

Free agent skill. Give your agent a UI screenshot and get back **one** React + Tailwind
component that uses your design tokens, plus a demo page and a `NOTES.md` of what the
image genuinely could not tell it.

## The problem

Pasting a screenshot into a chat gets you code that looks right and behaves wrong:

- it ignores your design tokens and hardcodes colors
- it invents copy that was never in the image
- it silently guesses the parts it could not see (hover, focus, exact spacing)

This skill makes the guesswork explicit. The vision pass produces a typed spec first, the
coding pass works from that spec, and the checks fail on the usual cheats.

## How it works

1. **One vision call** turns the image into a structured spec: component name, regions,
   every visible string, token mapping, breakpoints, and unknowns.
2. **One cheap code call** turns the spec into three files: the component, a demo page,
   and `NOTES.md`.
3. **Checks** reject external image URLs, token colors hardcoded as hex, missing
   demo/notes, and multiple exports.

Two model calls per screenshot. Everything mechanical (prompt building, JSON parsing,
file writing, token parsing, constraint checks) is deterministic.

## What is enforced

- one component per screenshot, one default export
- no invented copy; `?` stays `?`
- no external image URLs, web fonts or icon packages
- no hardcoded hex for colors covered by tokens
- breakpoints only if the spec mentions them
- `NOTES.md` always lists the vision pass's unknowns

## Install

```
npx skills add WinSoftLabs30/screenshot-to-code-skill
```

On ClawHub (OpenClaw): `openclaw skills install @winsoftlabs30/screenshot-to-code`, or
`clawhub install @winsoftlabs30/screenshot-to-code`.

Or copy `SKILL.md` into:

- **OpenCode** — `.opencode/skills/screenshot-to-code/` or
  `~/.config/opencode/skills/screenshot-to-code/`
- **Claude Code** — `.claude/skills/screenshot-to-code/`
- **Other agents** — any that read `SKILL.md` and can attach an image

No build step and no dependencies. Any Node version works for this manual edition.

## Use

Ask your agent:

> Turn this screenshot into a component: `C:\shots\pricing.png`, tokens at `src/tokens.css`.

It asks for the image path, the tokens (optional) and a component name, then follows the
flow: spec first, code second, checks last.

## Manual edition

This repository is the workflow and the checks. The paid edition adds seven dependency-free
scripts that do the mechanical part:

| Script | What it does |
| --- | --- |
| `describe.ts` | builds the vision prompt and validates/parses the spec JSON |
| `generate.ts` | builds the code prompt, accepts JSON or FILE blocks, writes the three files |
| `check.ts` | fails on external URLs, token hex, missing demo/notes; warns on unused tokens |
| `tokens.ts` | parses `tokens.css` and simple Tailwind color maps |
| `image.ts` | reads PNG/JPEG/WebP headers for size, without dependencies |
| `spec.ts` | the typed spec schema plus validation |
| `cli.ts` | a single entry point for all of it |

Backed by **41 tests** and a recorded-response demo, so the whole pipeline runs without a
model call.

## Honest limits

- No pixel diff and no automatic visual loop. This is a first pass, not pixel fidelity.
- One component per screenshot; a full page takes several runs.
- Tailwind is assumed. Plain CSS output is not supported.
- Token extraction is regex-based: simple configs yes, computed colors no.
- Model quality varies; rerun the code pass for a different take.
- Icons become placeholders when their meaning is not visible.
- `NOTES.md` is the vision model's self-report plus your notes, not verified truth.
- The manual edition leans on the agent; the paid scripts make every run identical.

## License

MIT-0 — see [LICENSE](LICENSE). Use it, modify it, redistribute it, no attribution
needed. (ClawHub requires MIT-0, so both free channels use one license.)
