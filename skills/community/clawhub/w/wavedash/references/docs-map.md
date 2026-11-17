# Wavedash Docs Map

Official docs are canonical. Use the rendered URL for humans and append `.md`
when an agent needs raw page text.

Markdown form: `https://docs.wavedash.com/<slug>.md`

## Start and concepts

- Quickstart: https://docs.wavedash.com/getting-started/quickstart
- Introduction: https://docs.wavedash.com/getting-started/introduction
- Concepts: https://docs.wavedash.com/getting-started/concepts
- All docs for LLMs: https://docs.wavedash.com/llms.txt
- Full docs text: https://docs.wavedash.com/llms-full.txt

## SDK

- SDK overview: https://docs.wavedash.com/sdk/overview
- SDK setup: https://docs.wavedash.com/sdk/setup
- Players: https://docs.wavedash.com/sdk/players
- Achievements and stats: https://docs.wavedash.com/sdk/achievements
- Leaderboards: https://docs.wavedash.com/sdk/leaderboards
- Cloud saves: https://docs.wavedash.com/sdk/cloud-saves
- User-generated content: https://docs.wavedash.com/sdk/ugc
- Fullscreen: https://docs.wavedash.com/sdk/fullscreen
- Audio: https://docs.wavedash.com/sdk/audio
- Functions reference: https://docs.wavedash.com/sdk/functions
- Events reference: https://docs.wavedash.com/sdk/events
- Types reference: https://docs.wavedash.com/sdk/types

## Multiplayer

- Multiplayer overview: https://docs.wavedash.com/multiplayer
- Lobbies: https://docs.wavedash.com/multiplayer/lobbies
- Networking: https://docs.wavedash.com/multiplayer/networking

## CLI and local development

- CLI overview: https://docs.wavedash.com/cli
- Installation: https://docs.wavedash.com/cli/installation
- Authentication: https://docs.wavedash.com/cli/authentication
- Configuration: https://docs.wavedash.com/cli/configuration
- Commands: https://docs.wavedash.com/cli/commands

Common local workflow:

```bash
wavedash auth status
wavedash init
wavedash dev
wavedash build push
wavedash publish <BUILD_ID>
```

Common automation flags:

```bash
--json --no-color --no-update-check
```

## Publishing

- Upload a build: https://docs.wavedash.com/publishing/upload
- Publish a build: https://docs.wavedash.com/publishing/publish
- Metadata: https://docs.wavedash.com/publishing/metadata
- Pricing: https://docs.wavedash.com/publishing/pricing
- Content guidelines: https://docs.wavedash.com/publishing/content-guidelines

## Game quality

- Best practices: https://docs.wavedash.com/tutorials/best-practices
- Shader stutter: https://docs.wavedash.com/tutorials/shader-stutter
- CI/CD: https://docs.wavedash.com/tutorials/ci-cd

## Engine guides

Start at https://docs.wavedash.com/engines, then select the project engine.
Available guides include Godot, Unity, Unreal, Phaser, Three.js, PixiJS,
Babylon.js, PlayCanvas, Construct, Cocos, ct.js, Excalibur, Flame, GameMaker,
GB Studio, GDevelop, Heaps, KAPLAY, LittleJS, Love2D, melonJS, MonoGame,
PICO-8, Ren'Py, RPG Maker, Ruffle, JSDOS, Defold, Bevy, Ebiten, KNI, raylib,
React, Solar2D, Stride, Rust, JavaScript, TypeScript, Python, C, C++, C#, Lua,
Go, Haxe, Swift, Zig, and custom web builds.
