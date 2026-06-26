---
name: phaser-best-practices
description: Builds and refactors Phaser 3 browser games. Use for creating a new Phaser project, adding scenes, entities, physics, UI, tilemaps, animations, input, audio, camera, or for fixing Phaser-specific bugs and performance problems.
compatibility: Intended for Phaser 3 JavaScript or TypeScript projects. New-project scaffolding assumes Node.js/npm or an existing browser bundler.
metadata:
  phaser-major: "3"
  skill-type: "framework"
---

# Building Phaser Games

## When to use this skill

Use this skill when the user wants to:

- create a new Phaser 3 game or prototype
- add or refactor scenes, entities, UI, physics, tilemaps, input, audio, or cameras
- debug Phaser-specific behavior such as scene restarts, blurry pixel art, collider bugs, asset loading problems, or animation issues
- improve architecture, maintainability, or runtime performance in a Phaser project

Do not use this skill for non-Phaser engines unless the user explicitly wants Phaser-style patterns adapted elsewhere.

## How to operate

### 1. Triage the request

Classify the task before writing code:

- **New project**: scaffolding, folder layout, game config, first scenes
- **Feature work**: add gameplay, UI, audio, transitions, tilemaps, enemies, pickups
- **Bug fix**: isolate scene lifecycle, asset, physics, input, camera, or rendering failure
- **Optimization**: profile bottlenecks, pooling, culling, throttling, asset strategy
- **Art / asset pipeline**: spritesheet measurements, animation setup, nine-slice / three-slice UI, tilemap integration

### 2. Inspect first, then decide

When a repository already exists, inspect before proposing structure changes:

- package.json, bundler config, tsconfig/jsconfig
- Phaser version and whether the codebase is JS or TS
- game bootstrap, scene list, physics config, scale config
- asset folders and naming conventions
- current state-sharing approach (scene data, registry, services, globals)
- whether the project is pixel art, HD art, desktop-first, mobile-first, or mixed input

Prefer adapting to the existing codebase over replacing it with boilerplate.

### 3. Default technical choices

Use these defaults unless the task clearly calls for something else:

- Prefer the official **Vite + TypeScript** style setup for new projects
- Prefer **Arcade Physics** for platformers, shooters, top-down action, simple pickups, and lightweight collision logic
- Use **Matter Physics** only when the game needs rotation-driven collisions, compound bodies, constraints, stacking stability, or more realistic simulation
- Organize code around **Scenes first**, then entities / systems inside scenes
- Keep input **scene-owned**; entities should consume input state, not attach their own listeners
- Use **global animations** when multiple sprites share the same animation data
- Preload **startup-critical** assets up front; load level-specific assets later when it improves startup time
- Use built-in **NineSlice / ThreeSlice** for scalable UI art when the texture layout supports it; only fall back to custom compositing when transparent padding or discontinuous art breaks built-in slicing
- Use **FIT** scaling for most games, **RESIZE** for editor-like or UI-heavy layouts, and **NONE** only when manually controlling canvas sizing
- For pixel art, enable **pixelArt** mode, favor integer scaling where possible, and avoid sub-pixel camera movement

### 4. Output expectations

For **new games**, provide:

- the recommended folder structure
- a game config
- scene list and responsibilities
- starter code that runs
- notes on why each architectural choice fits the requested genre

For **feature work or bug fixes**, provide:

- minimal targeted edits
- root cause explanation
- the patch
- validation steps the user can run immediately

For **architecture advice**, provide:

- the smallest structure that solves the current problem
- one recommended path, not a menu of equally-weighted options
- explicit tradeoffs when the choice is important (for example Arcade vs Matter)

## Non-negotiable implementation rules

- Respect the project's existing JS vs TS choice unless the user asks to migrate
- Centralize scene keys, asset keys, collision categories, and balance constants
- Keep `update()` orchestration-focused; push detailed logic into entities or systems
- Register cleanup for scene shutdown / destroy when you attach listeners, timers, tweens, or long-lived references
- Avoid creating new objects inside hot `update()` loops unless profiling proves it is harmless
- Do not make every object interactive or physics-enabled by default
- Do not assume spritesheet frame dimensions; inspect and verify them
- Do not tell the user to use Matter when Arcade already solves the problem cleanly
- Do not preload the entire game into one Boot scene just because it is convenient

## Recommended delivery workflow

### New Phaser project

1. Pick the architecture size:
   - **Small / jam game**: 2-4 scenes, lightweight service modules
   - **Mid-size game**: scenes + entities + systems + constants
   - **Large content-heavy game**: data-driven content, scene services, dedicated state layer
2. Define the base config: renderer, scale mode, physics, pixel-art settings
3. Create startup scenes first: Boot, Menu, Game, UI; add Pause / GameOver only if required
4. Add one vertical slice that proves the core loop works
5. Add reference-driven systems next: audio, saveable state, enemy spawning, tilemaps, UI polish

### Adding or refactoring a feature

1. Locate the owning scene and affected systems
2. Identify the smallest correct insertion point
3. Reuse existing helpers, constants, managers, and pools
4. Add cleanup and validation steps with the change
5. Preserve scene restart safety

### Debugging

1. Reproduce the issue from the code and config
2. Identify whether the fault is:
   - lifecycle / restart
   - asset dimensions or loader config
   - physics body setup or collider order
   - scale / camera / pixel rounding
   - stale listeners, timers, or pooled object state
3. Patch the root cause, not just the symptom
4. Provide a quick repro or verification checklist

## Reference map

Read only the files relevant to the task:

- **Setup / bootstrap / config**: [references/setup-and-build.md](references/setup-and-build.md)
- **Scenes / shared state / architecture**: [references/scenes-state-architecture.md](references/scenes-state-architecture.md)
- **Physics / entities / pooling**: [references/physics-and-entities.md](references/physics-and-entities.md)
- **Assets / animations / UI panels**: [references/assets-animation-ui.md](references/assets-animation-ui.md)
- **Tilemaps / camera / input / audio**: [references/tilemaps-camera-input-audio.md](references/tilemaps-camera-input-audio.md)
- **Performance / debugging / cleanup**: [references/performance-debugging.md](references/performance-debugging.md)
- **Code review / architecture checklist**: [references/review-checklist.md](references/review-checklist.md)

## Concrete examples

### Example: "Create a Phaser top-down shooter"

Use this skill. Default to:

- Vite + TypeScript structure
- Arcade Physics
- Boot, Menu, Game, UI scenes
- scene-owned input mapping
- pooled bullets
- global animations
- camera follow and world bounds
- asset keys / scene keys in constants

Then deliver runnable starter code plus the first playable loop.

### Example: "My pixel art looks blurry on mobile"

Use this skill. Inspect:

- `pixelArt` and `roundPixels` settings
- camera follow rounding
- scale mode and zoom strategy
- CSS around the canvas container
- whether art is being scaled non-integer

Then patch the smallest set of config and camera settings required.

### Example: "Paper UI panels show weird side bars"

Use this skill. Inspect the source texture first. Then:

- try built-in ThreeSlice / NineSlice if the art is a true 3-slice or 9-slice layout
- if frames contain large transparent padding or discontinuous art, use trimmed or composited fallback slices
- document the measured frame sizes, spacing, margins, and any overlap used

## Common traps

Avoid these unless the user explicitly wants them:

- one giant `GameScene` that owns menus, HUD, gameplay, pause, and transitions
- state stored on `window`, random module globals, or ad hoc singleton soup
- entity-owned keyboard listeners
- scene restart bugs caused by forgotten shutdown cleanup
- loading every future asset in the first scene
- manual nine-slice composition when built-in NineSlice already fits the asset
- over-engineering with ECS for tiny games that only need a few entity classes

## Final check before responding

Make sure the answer:

- matches the user's genre, platform, and art style
- uses Phaser 3 APIs, not Phaser 4 RC APIs
- chooses a physics system deliberately
- keeps SKILL.md-level advice concise and moves detail into references
- includes validation steps when code is produced
