# MSW Entity — `.map` Placement & Runtime

**Domain rules** for entity instances inside `.map` files — which mode (`TileMapMode`) places things where, how coordinates / footholds / camera / RUID interact, the `modelId` vs inline decision, runtime lifecycle. `.model` template authoring is split out into [model.md](model.md).

> **The actual call protocol for `.map` mutation (MapBuilder API, snapshot workflow, coverage gaps, `.map` / `.model` cross-flow) lives in [builder-protocol.md §1](builder-protocol.md). Re-read builder-protocol.md every turn that touches `.map`; this document supplies the domain context (why the calls look that way) and is read alongside it.**

The legacy Maker RPC (curl) API has been removed. `.map` inspection and mutation go through `scripts/map/msw_map_builder.cjs` (= `MapBuilder`), followed by **msw-maker-mcp** verification tools.

---

## File / Tool Overview

| Area | Path | Role |
|------|------|------|
| Map | `./map/*.map` | Map root, footholds, tiles, **all placed entities** |
| User models | `./RootDesk/MyDesk/Models/{Category}/*.model` (typed subfolder, e.g. `Models/Monsters/`) | Custom `.model` templates ([model.md](model.md) — never save directly under `MyDesk/` or `Models/`) |
| System models | `./Global/*.model` | Engine default templates (monster presets, Player, etc.) — read-only; copy into `MyDesk/Models/{Category}/` to customize |
| UI | `./ui/*.ui` | UI-only entities and widgets ([`msw-ui-system`](../../msw-ui-system/SKILL.md)) |

> **Placing a monster** — read [monster.md](monster.md) first. The two verified working canonicals each have 11 components (`Soldier.model` for Pattern A — script-driven SpriteRUID; `MonsterCanonical.model` for Pattern B — `AIChaseComponent` + ActionSheet pipeline). `ActionSheet` keys are lowercase. `IsLegacy: false` is mandatory on `HitComponent` for both patterns; on `StateComponent` (and on `AIChaseComponent` if present) only for Pattern B — Pattern A leaves `StateComponent.IsLegacy` at the default. Mixing inline `@components` with `modelId` overrides on a system monster model produces `LEA-3046 InternalError` at runtime; bake the values into a dedicated `.model` instead.

> MCP tools are self-documenting when connected. If the user asks about MCP setup, share this link: https://maplestoryworlds-creators.nexon.com/ko/docs?postId=1368

---

## Scope Concept (file-edit workflow)

1. **Scope of "what shows up in the list"**
   - The editor **hierarchy** and the builder entity list for `./map/{mapname}.map` only contain entities belonging to **that map instance**.
   - When listing entities by opening a file, the **currently edited map file is the scope**. Placements in other maps live in other `.map` files.

2. **Scope of ID / path-based access**
   - In runtime Lua, you can reference an entity in any map via a **global path** like **`_EntityService:GetEntityByPath("/maps/map01/Monster01")`**.
   - Entity **`id` (UUID)** is also stored in the map file, and scripts can track it by the same ID (assuming the map is loaded).

**Practical implication**: "What's in this map?" → search `./map/{this}.map`. "Find this entity across the whole world" → grep all `.map` files.

---

## Component vs Logic

> See `msw-scripting` §3 for type comparison, declaration syntax, and decision criteria. Behavior attached to an entity → Component; global singleton manager → Logic.

---

## StateComponent vs StateAnimationComponent

### StateComponent

- **Role**: game-logic state machine (e.g. `Walk`, `Jump`, `Dead`, `Attack`).
- **May not play animation directly** — manages only state names and transition conditions.
- Controlled from scripts via `CurrentStateName`, `ChangeState()`, etc.
- The **DefaultPlayer** family uses `StateComponent` + `AvatarStateAnimationComponent`.

### StateAnimationComponent

- **Role**: visual state / action playback based on **sprite / action sheet** (`ActionSheet`).
- In monster / object models, handles the **action name ↔ sprite sequence** mapping.
- A common pattern is `actionSheet` etc. in `.model` `Properties` linking to `StateAnimationComponent`.

**Difference**: **StateComponent = logical state**; **StateAnimationComponent = sprite animation data**. In a model that has both, keep names and transition timing aligned.

---

## TouchReceiveComponent vs ButtonComponent

> See `msw-scripting` §10 for world input (TouchReceiveComponent + TouchEvent) vs UI input (ButtonComponent + ButtonClickEvent). Swapping them silently drops all input. Do not attach UI components to map entities.

---

## Entity.CurrentMap (strongly recommended)

At runtime, when spawning, parenting, or searching within the same map, use **`self.Entity.CurrentMap`** or an already-acquired map entity.

```lua
local map = self.Entity.CurrentMap
_SpawnService:SpawnByModelId("myenemy", "Enemy_1", position, map)
```

- **`SpawnService` parent must not be nil** — yields LWA-3019 warnings and undefined behavior.
- Unless a special case requires another parent (such as out-of-map common), **always pass the map entity**.
- For file-only edits, reflect the spawn position in `.map`'s `TransformComponent.Position`.

---

## RUID (Resource Unique ID)

- MSW resources (sprites, tilesets, sounds) are identified by **RUID strings**.
- An empty **`SpriteRendererComponent.SpriteRUID`** means **the entity is invisible** (with no error).
- In `.model` `Values` or `.map` `@components`, use either a string or `{ "DataId": "hex..." }` form — **match the existing pattern in the same map / model**.

**Asset search**: use the `msw-search` skill or `_ResourceService` API. Replace temporary placeholders with real assets before release ([platform.md](platform.md)).

---

## MapBuilder — call protocol lives in builder-protocol.md

`.map` snapshot workflow (get → edit → set), the API table, placement / patch / rename / remove / component CRUD / tile / foothold inspection, coverage gaps, Map Mode Rules, `false`-return handling — **every detail of MapBuilder invocation is consolidated in the single entry point [builder-protocol.md §1](builder-protocol.md).** Read it just before any `.map` work.

This document carries the **why** behind those calls — Scope, RUID, the meaning of the TileMapMode-to-Body mapping, the `modelId` vs inline decision rule, placement coordinates / footholds / camera visibility, runtime verification, and the constraint checklist.

Domain-side summary rules:

- `.map` `Entities` arrays are very large. **Direct raw JSON editing is reserved for builder coverage-gap areas only** — minimal scope plus `refresh` + logs verification.
- Patch values through world-unit vectors (`pos: [x, y, z]`), color helpers, and component override objects. Do not hand-write raw component JSON except as a builder argument for a single-component payload.

---

## TileMapMode ↔ Movement Components

`MapComponent.TileMapMode` on the map root determines the **entire movement / gravity / collision stack**. If an entity's Body-family component does not match the map, **it will not move** (with no error) — and the engine will log one of the `[LEA-3004] MissingComponent` messages ([platform.md §4](platform.md)).

### Map Work Preflight (mandatory before any map task)

Before touching a map in any way (entity placement, spawn, movement scripts, applying models, tile edits, etc.), always confirm the following two items **in order**:

1. **Identify which map you are working on and where it lives** (e.g. the `./map/{mapname}.map` path and its root entity).
2. **Use `MapBuilder.read(...).getTileMapMode()` to read `MapComponent.TileMapMode` as a number**, and keep the value in mind:
   - `0` → **MapleTile** (side-view + Foothold; Body = `RigidbodyComponent`)
   - `1` → **RectTile** (top-down grid; Body = `KinematicbodyComponent`)
   - `2` → **SideViewRectTile** (side-view tile grid; Body = `SideviewbodyComponent`)

**Do not proceed with model / entity / script work while the `TileMapMode` value is unknown or unclear.** The three modes differ completely in Body component, events, gravity, and collision. A mismatch is not a compile-time error — it surfaces as a runtime `[LEA-3004] MissingComponent` log **or** as a silent failure where the entity simply refuses to move with no error at all.

### Recommending the mode (when starting a new map or when the current mode is wrong for the user's goal)

For **new map authoring** — or whenever the current map's `TileMapMode` clearly does not fit the gameplay the user described — **explicitly recommend the appropriate `TileMapMode` before doing any further entity / model / script work** (do not silently proceed with whatever is already on disk).

Use this decision matrix:

| User's intended game / gameplay | Recommend | Why |
|---|---|---|
| MapleStory-style side-scrolling action · jump · ladder · freely placed footholds (platformer) | **`0` MapleTile** | Side-view + gravity + freely placed Foothold line segments |
| Top-down RPG · maze · board game · dungeon crawler · Bomberman-style · farming sim | **`1` RectTile** | Top-down 4-directional free move, no gravity, square-tile grid |
| Tile-based side-scrolling platformer · Mario-style pixel action · side-view puzzle | **`2` SideViewRectTile** | Side-view + gravity **on a tile grid** (not free footholds) |

If the user has not yet told you what kind of game they want, **ask one short question first** (e.g. "Is it top-down, or side-scrolling (jump/ladder)? Is it based on freely placed footholds, or a square tile grid?") and only then recommend.

### Changing `TileMapMode` — user action in Maker, not an AI file edit

The AI must **never** write a new value into `MapComponent.TileMapMode` directly in the `.map` JSON. Mode switching swaps tile components, rebuilds footholds, and converts tile-data formats — Maker handles all of that internally.

Guide the user to switch the mode in the Maker editor as follows:

1. Open the Maker editor's **Hierarchy** window.
2. **Right-click the target map entity** in the Hierarchy.
3. Choose the **"Switch ..." option that matches the target mode** (Switch TileMap / RectTileMap / SideViewRectTileMap) from the context menu.
4. After the user reports the switch is complete, call MCP **`refresh`**, then re-read `MapComponent.TileMapMode` to confirm and re-check every dynamic entity's Body component against the new mode.

> AI role on mode changes: **recommend mode → wait for the user to right-click-switch in the Maker Hierarchy → refresh → fix Body components / scripts that no longer match**. Do not flip `TileMapMode` from a file edit.

> Mapping table / check protocol / transition limits: [platform.md §4](platform.md). `LEA-3004` and other silent-failure symptoms (won't move / won't render / floating in mid-air / stuck in a wall …): [troubleshooting.md](troubleshooting.md). Per-map-type code patterns: [platform-maple.md](platform-maple.md) / [platform-rect.md](platform-rect.md) / [platform-sideview.md](platform-sideview.md). Tile painting itself: [tile.md](tile.md).

---

## Two-Step Map Editing Workflow (create → place)

1. **Create** — define the `.model` under `RootDesk/MyDesk/Models/{Category}/{Name}.model` (typed subfolder; details in [model.md §1, §2.2](model.md)).
2. **Place**
   - `MapBuilder.read(...)` → `map.placeModel(...)` → `map.write(...)`. Concrete call sequence, API tables, and option details live in [builder-protocol.md §1 + §4](builder-protocol.md).
   - `placeModel()` returns the placed root entity id string, not the builder. Do not chain `.write()` after it.
   - **`modelId` form (default — required for ≥2 instances)**: `placeModel()` mirrors model components and applies per-instance overrides.
   - **Inline form**: use `sprite()` / `empty()` only for truly one-off map-local entities.
   - `refresh`.

### `modelId` vs Inline — Decision Rule

| Situation | Form |
|---|---|
| Same composition placed **≥2 times** in this map | **`modelId`** (always — author a `.model` first if none exists) |
| Same composition reused in **another map** | **`modelId`** |
| Will be spawned at runtime via `SpawnByModelId` | **`modelId`** (required) |
| Truly one-off composition that will never recur | inline `@components` is acceptable |

> When in doubt, choose `modelId`. Five inline copies of "the same monster" silently drift apart over edits (one gets `IsLegacy: true`, another loses `SortingLayer`); the model anchors the canonical values and a single edit propagates.

---

## Handling Entity Instances in `.map`

### Common fields (must match)

- **`id`**: UUID v4 (with hyphens). Generate fresh for new entities.
- **`path`**: `/maps/{mapname}/{entityname}` — parent-child hierarchy is the path prefix.
- **`componentNames`**: comma-joined `@type` values of `@components`, **kept in sync**.
- **`jsonString.path`**: same as the outer `path`.
- **`pathConstraints`**: root `//`, child `///`.
- **`displayOrder`**: avoid overlap among siblings.

### modelId entities

Use `MapBuilder.placeModel()` — it creates the model-instance metadata, keeps component names in sync, mirrors model components, and applies per-instance `TransformComponent.Position` and `componentOverrides`. For the call signature and option details, see [builder-protocol.md §1.4 + §4](builder-protocol.md).

### Adding a new map to the world

- You may need to add `map://{mapId}` to `entries` in `Global/SectorConfig.config`.

---

## Tile-map entity transform is locked

The map's tile-grid container — the entity carrying `TileMapComponent` (MapleTile) or `RectTileMapComponent` (RectTile / SideViewRectTile) — has its `TransformComponent` **locked by the tile-map component itself**. Writes to `TransformComponent.Position` / `EulerAngles` / `Scale` are **silently rejected** with a `LWA-3047 NativeIssue_UnableToChange` warning. The engine keeps this entity at a fixed origin (`(0, 0, z)`, or a half-cell offset for odd-grid RectTile maps) so that tile coordinates and world coordinates stay in a known relationship.

**This applies regardless of whether the entity was placed with `modelId` or as an inline `@components` block** — the lock comes from the tile-map component, not from how the entity was authored. Moving the entity in `.map` JSON appears to take, but `refresh` reverts it to `(0, 0, z)`; runtime `Position = ...` writes produce no visible movement and log `[LWA-3047]`.

**Workaround**: do not try to move the tile-map entity. Anchor your game's coordinate system to the locked origin instead — keep gameplay anchors (grid origin, spawn points, path waypoints) in tile coordinates and convert via the tile-map component's helpers (e.g. `RectTileMapComponent:ToWorldPosition(cellPos)` — see [`platform-rect.md`](platform-rect.md) §3).

Symptoms when the rule is ignored:

- A `Position` written into `.map` JSON reverts to `(0, 0, z)` after Maker `refresh`.
- Runtime `TransformComponent.Position = ...` writes have no observable effect; `logs` shows `[LWA-3047] UnableToChange`.
- Adding a custom child entity to the tile-map entity works, but the child's effective world position is still measured relative to the locked parent at `(0, 0)`.

This is **by design** — the tile-map entity is the canonical reference frame for tile↔world conversion. Decorations, spawn anchors, or overlays that need to be elsewhere should live as **siblings under the map root, not as children of the tile-map entity**.

---

## Placement Coordinate Rules

### Y (MapleTile + footholds)

- Align character / foothold-based entities to the **top of the foothold**.
- The **`y`** of each foothold's `StartPoint`/`EndPoint` in `FootholdComponent` is the platform height.
- A small offset (+0.01 to 0.05) may be needed depending on sprite anchor / collider offset — verify with `play` + `screenshot`.

### Horizontal Spacing (multiple monsters / objects in a row)

- **Always use the `modelId` form** for repeated entities (see "Two-Step Map Editing Workflow → Decision Rule" above). The N instances should share one `.model` and differ only in `TransformComponent.Position`.
- Space along X **without overlap** based on each entity's **bound width** (`TiledSize`, `BoxSize`).
- Even spacing: `x_i = x0 + i * (width + gap)`.
- On the same foothold, share **the same Y** and only shift X.

### RectTile / SideViewRectTile

- **Grid-based** placement — verify the conversion between `RectTileMapComponent` tile coordinates and world coordinates ([tile.md](tile.md)).
- On RectTile (no gravity), assume **Kinematicbody** and move on the XY plane.

### Camera Visible Area

- See the rough visible-world-unit table in [platform.md §5](platform.md) for PC / mobile — verify the **start position is on-screen**.

---

## RPC → File-Based Replacement Table

| Old (RPC) | Current equivalent |
|----------------|-----------|
| Create entity | Author `.model` under `RootDesk/MyDesk/Models/{Category}/` + place it with `MapBuilder.placeModel()` |
| Delete entity | `MapBuilder.remove()` |
| Change property | `MapBuilder.patchComponent()` for map instances or ModelBuilder values for templates |
| Add/remove component | `MapBuilder.upsertComponent()` / `removeComponent()` for one-off map-local instance changes |
| Register/edit/delete model | CRUD `.model` files under `RootDesk/MyDesk/` (`refresh`) |
| List entities | `MapBuilder.snapshot()` / `listEntities()` |

---

## Runtime Verification

For **runtime state** that's hard to know from files alone, use `logs` and `log()` in play mode.

### Flow

1. Add `log()` in `.mlua` for the value to inspect
2. `refresh` → `play` → collect via `logs`
3. `stop` → edit files → repeat

### When you don't know an API

1. **`.d.mlua`** — search `Environment/NativeScripts/` for `EntityService`, `SpawnService` signatures
2. **`msw-search`** — API details, implementation guide

After work, `**stop**` to return to edit mode.

---

## Constraint Rules Checklist

### Files / Editor / MCP

1. **Run `refresh` after file changes** (not allowed during play — `stop` first).
2. **Use `MapBuilder` first for `.map` work** — direct raw JSON edits are only for explicitly unsupported gaps, and must be minimal plus verified.
3. **Do not modify `Environment/*.d.mlua`** — API definitions are read-only.
4. **Do not create or edit `.codeblock` manually** — Maker `refresh` generates it from `.mlua`.
5. **Take `screenshot` only when the user explicitly asks or when identifying coordinates for input simulation.**

### Physics / Movement / Map

6. **TileMapMode ↔ Body components** must match.
7. On **MapleTile**, placement Y is **foothold-based**; assumes gravity / Rigidbody.
8. On **RectTile**, do not expect vertical foothold physics — assumes Kinematicbody.
9. When inspecting or changing foothold data, use `MapBuilder` APIs so Id / Length / OwnerId consistency is centralized.

### Render / Resource

10. **If a visual is needed, do not leave `SpriteRUID` empty.**
11. **RUIDs must be project-registered resources** — arbitrary strings are missing at runtime.
12. **Match the form of TileSetRUID / sprite DataRef** to existing maps.

### Entity / Spawn / Hierarchy

13. **Keep `id` / `path` / `componentNames` / `jsonString.path` consistent in `.map`.**
14. **`SpawnService` parent must not be nil** — pass a map entity such as `self.Entity.CurrentMap`.
15. **When referencing `modelId`**, `origin.entry_id` = `modelId`, and `origin.root_entity_id` = the entity's own outer `id` (top-level instance).
16. **Use `MapBuilder.placeModel()` for `modelId` instances** — it mirrors model components and keeps `componentNames` in sync. Empty component names or partial component arrays silently remove components at runtime.
17. Child entities must have a **`path` that is a prefix of the parent**.

### Input / UI Boundary

18. **TouchReceive (world) vs Button (UI)** — do not confuse input layers.
19. Keep the responsibilities of UI-only groups (the `ui` hierarchy) and map entities separated.

### State / Animation

20. Do not confuse the roles of **StateComponent (logic)** vs **StateAnimationComponent (sprite action)**.
21. Action-name strings must **match** across code, action sheet, and animation data.

### Verification Loop

22. **`refresh` → `logs`** → **`play` → `logs` → `stop`**.
23. On intermediate failure, **stop the following steps** — fix the cause and retry.

---

## Related Skills / Docs

| Doc | Purpose |
|-------------|------|
| [builder-protocol.md §1](builder-protocol.md) | **`.map` call protocol — MapBuilder API, snapshot workflow, coverage gaps, `false`-return handling** (read every turn that touches `.map`) |
| [builder-protocol.md §4](builder-protocol.md) | `.model` author → `.map` placement → `refresh` cross-flow |
| [model.md](model.md) | `.model` template authoring domain (when / catalog / component combinations) |
| [tile.md](tile.md) | Tile maps / tilesets |
| [`msw-ui-system`](../../msw-ui-system/SKILL.md) | UI authoring |
| [platform.md](platform.md) (core) | TileMapMode ↔ Body mapping, spawn, RUID, coordinates, `.directory`, ID, `.config` (common to all map types) |
| [platform-maple.md](platform-maple.md) / [platform-rect.md](platform-rect.md) / [platform-sideview.md](platform-sideview.md) | Per-map-type physics / events / patterns / checklists |
| [troubleshooting.md](troubleshooting.md) | Symptom → cause → fix (`LEA-3004`, "won't move", "won't render" …) |
| `msw-defaultplayer` | Player model / Values / components |
| `msw-scripting` | Component / Logic, properties, lifecycle |
| `msw-search` | RUID / asset / doc search |

Core principle of entity work: **"models are templates, maps are instances, builder-protocol.md is the single call manual, MCP is for verification."**
