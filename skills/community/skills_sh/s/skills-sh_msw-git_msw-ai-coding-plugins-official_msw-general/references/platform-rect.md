# Platform: RectTile (Top-Down) — `TileMapMode = 1`

**When to read this file**: When the `.map` you're working with has `MapComponent.TileMapMode` = **`1` (RectTile)**, or when working on top-down RPG / maze / board game / dungeon crawler / Bomberman-style / RTS-style / farming simulation.

> This file was split from [`platform.md`](platform.md) as a **RectTile-specific guide**. Rules common to all map types (8 core, coordinate system, RUID, spawn, ID, .config) remain in [`platform.md`](platform.md). Other map types: [`platform-maple.md`](platform-maple.md) / [`platform-sideview.md`](platform-sideview.md).

---

## 1. Map Type at a Glance

| Item | Value |
|---|---|
| TileMapMode | `1` |
| Enum name | `RectTile` |
| View | Top-down |
| Body component | **`KinematicbodyComponent`** |
| Map component | `RectTileMapComponent` |
| Gravity | **None** |
| Terrain | Square tile grid |
| Movement axes | **Free 4-directional** |
| Collision | Tile collision (Movable property) |
| Representative genres | Top-down RPG, Bomberman, dungeon crawler |

---

## 2. Physics System

**No gravity**. Free 4-directional movement. Tile-based collision.

- **Movement speed**: `KinematicbodyComponent.SpeedFactor` (separate X / Y multiplier)
- **Jump**: Optional (`EnableJump = true` is visual-only jump — no actual height change)
- **Shadow**: `EnableShadow` shows shadow during jump

### Engine defaults (`KinematicbodyComponent`)

A freshly-added `KinematicbodyComponent` already has movement-enabling defaults. The most common "my entity is mysteriously slow / can't move / has no shadow" issues come from **overwriting** these defaults with zero / false, not from forgetting to set them.

| Property | Default | Notes |
|---|---|---|
| `SpeedFactor` | `Vector2(1, 1)` | Per-axis multiplier. `(0, 0)` means cannot move at all; `(1, 0)` locks Y. |
| `EnableTileCollision` | `true` | Set `false` only when an entity must pass through walls (projectiles, ghosts). |
| `EnableJump` | `true` | Visual-only jump — does not change height. |
| `JumpSpeed` | `6.3` | Upward velocity at jump start. |
| `JumpDrag` | `20` | Downward acceleration during fall. |
| `EnableShadow` | `true` | Shadow under the entity. |
| `ShadowColor` | `Color(0.3, 0.3, 0.3, 0.8)` | RGBA. |
| `ShadowOffset` | `Vector2(0, 0)` | Local offset in tiles. |
| `ShadowSize` | `Vector2(0.7, 0.3)` | Width × height in tiles. |
| `ShadowScalingRatio` | `0.5` | How much the shadow shrinks as the entity rises. |
| `ApplyClimbableRotation` | `true` | Rotate sprite on climbable tiles. |

> `KinematicbodyComponent.Acceleration` is **deprecated** — do not rely on it for new code. Use `SpeedFactor` plus `MoveVelocity` for tuning.

```lua
-- KinematicbodyComponent key properties
local kb = self.Entity.KinematicbodyComponent
kb.SpeedFactor = Vector2(3, 3)     -- movement speed multiplier
kb.EnableJump = true                -- enable jump (visual only)
kb.JumpSpeed = 5                    -- jump speed
kb.JumpDrag = 3                     -- fall speed
kb.EnableTileCollision = true       -- enable tile collision
kb.EnableShadow = true              -- show shadow
kb.ShadowSize = Vector2(0.5, 0.2)   -- shadow size
```

---

## 3. Terrain & Collision

- **`RectTileMapComponent`**: Square tile grid.
- Per-tile **Movable property**: passable/blocked setting (in tile editor).
- `EnableTileCollision`: collision detection toggle.
- Coordinate conversion: `ToCellPosition(worldPos)` ↔ `ToWorldPosition(cellPos)`
- **The entity carrying `RectTileMapComponent` has its `TransformComponent` locked** at a fixed origin — direct `Position` / `EulerAngles` / `Scale` writes are silently rejected with `[LWA-3047]`. Game-side anchors (grid origin, spawn points, waypoints) must align to the locked origin and use `ToWorldPosition(cellPos)` to convert tile↔world. See [entity.md "Tile-map entity transform is locked"](entity.md#tile-map-entity-transform-is-locked).

```lua
-- World coordinates → tile coordinates
local tilemap = self.Entity.CurrentMap:GetFirstChildComponentByTypeName("RectTileMapComponent")
local cellPos = tilemap:ToCellPosition(self.Entity.TransformComponent.WorldPosition)
local tileInfo = tilemap:GetTile(cellPos)

if tileInfo ~= nil then
    log("Current tile: " .. tileInfo.Name)
end
```

---

## 4. Events

| Event | Triggered when |
|---|---|
| `RectTileEnterEvent` | Entering a tile |
| `RectTileLeaveEvent` | Leaving a tile |
| `RectTileCollisionBeginEvent` | Contact with non-passable tile begins |
| `RectTileCollisionEndEvent` | Contact with non-passable tile ends |
| `KinematicbodyJumpEvent` | Jump state change |

---

## 5. Monster / NPC Development

**Requirements**:
1. Monster `.model` must include **`KinematicbodyComponent`**.
2. **No gravity** → no fall handling needed.
3. Free 4-directional movement.
4. `SpeedFactor = (0,0)` means cannot move.

```lua
-- RectTile monster basic patrol pattern (top-down)
@Component
script MonsterPatrol extends Component

@Sync
property int32 patrolIndex = 0

property table patrolPoints = {
    Vector2(1, 0), Vector2(0, 1), Vector2(-1, 0), Vector2(0, -1)
}

[server only]
void OnUpdate(number delta)
{
    local kb = self.Entity.KinematicbodyComponent
    if kb == nil then return end

    local dir = self.patrolPoints[(self.patrolIndex % #self.patrolPoints) + 1]
    kb.MoveVelocity = dir
}

end
```

---

## 6. Special Features

- **Per-tile speed changes**: Adjust speed when entering specific tiles via `RectTileEnterEvent`.
- **Dynamic tile placement**: Modify the map at runtime with `SetTile()`, `RemoveTile()`, `BoxFill()`.
- **Tile name-based logic**: Distinguish tile types via `tileInfo.Name`.

---

## 7. MovementComponent — InputSpeed Conversion

**In RectTile**: `direction * InputSpeed / 1.2f` — divided by 1.2 for migration compatibility.

| TileMapMode | Actual speed | Notes |
|---|---|---|
| MapleTile | `InputSpeed` passed directly to Rigidbody | — |
| **RectTile (this file)** | `direction * InputSpeed / 1.2f` | Migration compatibility |
| SideViewRectTile | `direction.x * InputSpeed * 1.5f`, Y preserved | Similar to Rigidbody |

The same `InputSpeed = 3` feels slightly slower than MapleTile.

```lua
local movement = self.Entity.MovementComponent
movement.InputSpeed = 3
movement:MoveToDirection(Vector2(1, 0), delta)
movement:Stop()
-- Jump is visual-only — no actual height change
```

---

## 7. Troubleshooting (RectTile Only)

| Symptom | Cause | Fix |
|---|---|---|
| Entity doesn't move (no error) | Body is not `KinematicbodyComponent` | Body swap |
| Log `[LEA-3004] MissingComponent : Entity is missing 'KinematicbodyComponent'.` | Dynamic entity missing `KinematicbodyComponent` | Add `KinematicbodyComponent` to model/entity's `@components` |
| Monster disappears off-map | Leftover gravity code (from another map type) | Remove gravity code in RectTile |
| Can't jump over walls | RectTile jump is **visual-only** (no height change) | Change tile's Movable property |
| Passes through walls | Tile Movable not set or `EnableTileCollision = false` | Set Movable in tile editor, `EnableTileCollision = true` |
| Only some of 4 directions work | `SpeedFactor` X or Y is 0 | Set both to positive values |

> Full symptom dictionary: [`troubleshooting.md`](troubleshooting.md).

---

## 8. Checklist

### Common

- [ ] Read `MapComponent.TileMapMode` as a number directly from `.map` and confirm it is 1
- [ ] Player.model Body is `KinematicbodyComponent` active (DefaultPlayer handles this automatically)
- [ ] Monster/NPC `.model` includes `KinematicbodyComponent`
- [ ] `SpriteRendererComponent.SpriteRUID` is set
- [ ] Spawn calls pass map entity as `parent`

### RectTile Specific

- [ ] **No gravity code present** (unnecessary)
- [ ] `KinematicbodyComponent.SpeedFactor` ≠ `(0, 0)`
- [ ] `EnableTileCollision = true` (when wall/obstacle collision is needed)
- [ ] Tile Movable properties set as intended (tile editor)

---

## 9. Cross-references

- [`platform.md`](platform.md) — 8 core, TileMapMode↔Body mapping table, coordinate system, RUID, spawn, ID
- [`platform-maple.md`](platform-maple.md) / [`platform-sideview.md`](platform-sideview.md) — Other map types
- [`troubleshooting.md`](troubleshooting.md) — Unified symptom dictionary
- [`tile.md`](tile.md) — Tile painting (Movable property editing, etc.)
- [`entity.md`](entity.md) — Entity placement / Map Work Preflight
