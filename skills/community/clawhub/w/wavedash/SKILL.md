---
name: wavedash
description: Use when building, integrating, testing, uploading, publishing, or preparing a browser game for Wavedash, including CLI setup, Wavedash SDK features, multiplayer, achievements, leaderboards, cloud saves, player identity, user-generated content, store metadata, pricing, and content guidelines.
---

# Wavedash

Use this skill to get a game from local project to tested, uploaded, and
publishable on Wavedash. Official docs are canonical; this skill routes the
agent to the right docs and highlights traps agents commonly miss.

## Always do this

1. Identify whether the user is starting from an existing game or from zero. If
   no game exists yet, create a small browser-playable game first.
2. Identify the engine/framework, build command, output directory, and requested
   Wavedash features.
3. Read the relevant reference file before changing code or giving detailed
   instructions. Do not invent SDK methods, event names, constants, CLI flags,
   pricing rules, or content-policy exceptions.
4. Prefer the CLI for local testing and scripted upload/publish workflows.
5. Publish only when the user explicitly asks to make a build live.
6. Use `WAVEDASH_TOKEN` and `--json --no-color --no-update-check` in CI,
   cloud-agent, or other headless automation contexts.

## Routing

| User task | Read first |
| --- | --- |
| Start a new game from zero, scaffold a browser game, choose a framework | `references/project-start.md` |
| Install CLI, authenticate, initialize, test locally, upload, publish | `references/cli.md` |
| Add or fix SDK calls, player identity, load lifecycle, events | `references/sdk.md` |
| Add multiplayer, lobbies, networking | `references/sdk.md` |
| Add achievements, stats, leaderboards, cloud saves, UGC | `references/sdk.md` |
| Prepare store page, metadata, pricing, content policy, launch checklist | `references/publishing.md` |
| Fix launch-quality issues like shader stutter, Escape key, audio, memory | `references/game-quality.md` |
| Determine engine-specific build/export steps | `references/engines.md` |
| Need all docs URLs or raw Markdown links | `references/docs-map.md` |

## Critical rules

- Every Wavedash game must call `Wavedash.init()` or the engine binding
  equivalent; otherwise the game can stay hidden behind the loading screen.
- A new game must produce static browser files with an `index.html`; Wavedash is
  not a server runtime for native binaries or backend services.
- Test with `wavedash dev` when possible, then smoke-test the uploaded build on
  Wavedash after upload.
- Do not use Escape as the only pause/menu key; browsers reserve it for
  fullscreen and pointer-lock exit.
- Warm up shaders/materials before gameplay to avoid first-use stutter.
- Do not present crypto, NFT, real-money gambling, malware, hateful, sexual, or
  otherwise disallowed content as acceptable for Wavedash.
- Never commit API keys, tokens, private user data, or generated credentials.
