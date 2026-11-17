# xtaste · 一次记住你的品味

**Remember your taste once — every AI after that knows it.**

Take a 5-minute quiz once. After that, when you react to the AI's work with a lasting preference — "too busy", "I like this one", "keep it shorter" — it writes that down. One-off requests ("red this time, it's a holiday campaign") are not recorded. The next time it designs a page, writes copy or names something, it already knows your taste.

## What it covers

29 dimensions across six domains, plus concrete **anchors** (works and styles you love or hate):

- 视觉设计 visual design — light/dark, density, ornament, depth, colour, shape, type, motion, tone
- 文案表达 writing — length, conclusion-first, tone, format, jargon, hedging
- 命名 naming — length, language, literal vs. evocative
- 代码风格 code — abstraction, comments, dependencies, paradigm
- 做事方式 way of working — ask vs. just do it, scope, one pick vs. options, risk
- 产品取舍 product — focused vs. complete, classic vs. trendy, gamification

## How it learns

- **Single-variable quiz**: the two options in each visual question differ in exactly one parameter, so the answer measures one thing. Sides are randomised. 3 questions repeat with sides swapped, and inconsistent answers lower the weight of the whole quiz.
- **Weighted signals**: what you say outright > corrections > picks between variants > quiz > passive hints. Older signals fade. Contradictions are flagged, never silently overwritten.
- **Scenes**: "dense for dashboards, airy for landing pages" is kept as two separate preferences, so they don't cancel out.
- **Measured accuracy**: before recording each reaction, xtaste saves what the profile predicted. `xtaste stats` reports the hit rate.

## Install

```bash
python3 scripts/xtaste.py install          # preview
python3 scripts/xtaste.py install --apply  # link for Claude Code / Codex and open the quiz
```

Requires `python3` (standard library only). Chinese and English, picked from your system language automatically (`XTASTE_LANG=zh|en` to force; the quiz page also has a 中/EN switch).

## Privacy

Everything stays in `~/.xtaste/` on your machine, with no network calls. The quiz server listens only on `127.0.0.1`, accepts only same-origin requests with a per-session token (DNS-rebinding safe), and exits when you submit. `xtaste pause` stops recording. `xtaste forget <id>` stops a signal from counting, but its original line stays in the append-only log. Deleting `~/.xtaste` erases everything. `install --apply --no-onboard` turns the quiz prompt off for good.

License: MIT-0
