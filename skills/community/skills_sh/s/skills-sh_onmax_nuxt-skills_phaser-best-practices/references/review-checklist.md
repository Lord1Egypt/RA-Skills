# Review Checklist

## Contents

- Activation checklist
- Architecture checklist
- Code generation checklist
- Bug-fix checklist
- Performance checklist
- Asset-pipeline checklist
- Final-response checklist

## Activation checklist

Use the Phaser skill when the task is about:

- Phaser 3 scenes, game config, scaling, cameras, or scene lifecycle
- sprites, atlases, animations, or asset loading
- Arcade or Matter physics
- tilemaps / Tiled integration
- browser-game input, audio, HUD, pause menus, or scene transitions
- Phaser-specific debugging or performance issues

Do not reach for this skill just because the project is a web app with a canvas.

## Architecture checklist

Before proposing structure, verify:

- Is this a new game, a prototype, a mid-size game, or a content-heavy production?
- Does the current codebase already have an architecture worth preserving?
- Is a dedicated UI scene warranted?
- Does the user actually need Matter, or is Arcade enough?
- Should shared state live in scene data, registry, or a dedicated service?

If the answer is "small prototype", do not prescribe a large architecture.

## Code generation checklist

When generating code:

- keep file changes minimal
- preserve the existing language style (JS or TS)
- centralize keys / constants instead of scattering raw strings
- ensure lifecycle-safe cleanup for listeners and timers
- keep `update()` readable
- avoid speculative abstractions the user did not ask for
- include enough code for the feature to run, not just fragments
- include validation steps

## Bug-fix checklist

When fixing a Phaser bug, ask:

- is this a lifecycle problem?
- is the scene restarting safely?
- are loader keys or asset dimensions wrong?
- are bodies the wrong size or offset?
- is the camera or scale config causing the symptom?
- is stale pooled-object state leaking across spawns?
- are duplicate listeners accumulating?

Patch the root cause and explain why it happened.

## Performance checklist

Before claiming a performance fix:

- confirm the likely bottleneck category
- reduce active bodies / collisions before micro-tuning
- pool only what is frequently recycled
- remove per-frame allocations where practical
- verify that cleanup happens on shutdown
- test representative counts, not tiny toy counts
- remove or gate debug visuals when done

## Asset-pipeline checklist

Before writing loader config:

- inspect the real source image
- verify frame size, spacing, and margin
- decide whether the asset is better as an image, spritesheet, or atlas
- prefer built-in NineSlice / ThreeSlice when the art supports it
- use custom composition only when the art truly demands it

## Final-response checklist

Before responding to the user, ensure the answer:

- reflects the requested genre, platform, and art style
- uses Phaser 3 APIs and terminology
- recommends a physics system deliberately
- keeps the architecture proportional to the job
- includes concrete next steps or validation steps
- avoids unnecessary boilerplate
