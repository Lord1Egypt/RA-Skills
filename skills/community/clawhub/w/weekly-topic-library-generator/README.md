# Weekly Topic Library Generator

A weekly research skill for AI video people who know how to generate, but stall on *what* to generate.

It looks at public short-video trend write-ups from the last seven days, pulls the non-copyright bits (hook, structure, camera, visual keywords), and turns each one into a prompt pack you can paste into a text-to-video tool.

It does not download other people's videos. It does not clone a specific clip. Grades are a filter so you can sort the list — they are not a forecast.

## Install

Copy the `weekly-topic-library-generator` folder into your agent's skills directory:

- Claude Code: `~/.claude/skills/`
- Codex: `~/.codex/skills/`
- Cursor: `~/.cursor/skills/`

Then say: generate this week's topic library.

## What you get

Two files: Markdown for reading, JSON if you want to import the rows elsewhere. Each kept topic has a teardown, a prompt pack, a grade, and a risk line (copyright / platform AI label / deepfake-adjacent faces).

## What you need

An agent that can search the public web. No API key is bundled. No hosted feed.

## Rights

Outputs are AIGC starting points. Label generated video as AI-generated on the platform you post to. Do not use a real person's likeness or a protected character in the prompts.

## Full version

This repo is the free lite skill: the core 5-step workflow (collect → teardown → prompt pack → grade → ship).

The full version on Agensi adds:

- The complete 3-dimensional scoring system (replicability × spread-odds × compliance) with S/A/B tier thresholds
- Ready-made Markdown + JSON output templates
- Marketing-copy support for each topic (out of scope in this free version)
- A repeatable weekly consistency workflow with risk-flag conventions

Get it on Agensi: `<AGENSI_SKILL_URL>` — $5.99 one-time, includes future updates.

## More from the same creator

- [ZeroUploadPDF](https://www.zerouploadpdf.dev) — private PDF upload and sharing
- [NoteSpark](https://notespark.dev) — AI note-taking
- [TokSpark](https://tokspark.dev) — content research for AI video

⭐ Star this repo if it saved you time — it helps other creators find it.

## License

[CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/). Commercial use is allowed. Credit the source and keep derivatives under the same license.

## Version

0.1.0 — 2026-08-19. Public lite skill (core workflow only).
