# Platform: SideViewRectTile (Side-View on Tile Grid) — `TileMapMode = 2`

**When to read this file**: When the `.map` you're working with has `MapComponent.TileMapMode` = **`2` (SideViewRectTile)**, or when working on tile-based side-scrolling platformer / Mario-style pixel action / side-view puzzle (square-tile side-view).

> This file was split from [`platform.md`](platform.md) as a **SideViewRectTile-specific guide**. Rules common to all map types (8 core, coordinate system, RUID, spawn, ID, .config) remain in [`platform.md`](platform.md). Other map types: [`platform-maple.md`](platform-maple.md) / [`platform-rect.md`](platform-rect.md).

---

## 1. Map Type at a Glance

| Item | Value |
|---|---|
| TileMapMode | `2` |
| Enum name | `SideViewRectTile` |
| View | Side-view (side-scrolling) |
| Body component | **`SideviewbodyComponent`** |
| Map component | `RectTileMapComponent` |
| Gravity | **Yes (built-in, no Gravity property)** |
| Terrain | Square tile grid |
| Movement axes | Left/right + jump (Y = gravity) |
| Collision | Tile collision (Collision property) |
| Representative genres | Side-view action, tile-based platformer |

**Key difference**: RectTile's tile grid system + MapleTile's side-view gravity. **A hybrid of both modes.** Walks on square tiles with gravity instead of Foothold line segments.

---

## 2. Physics System

Combines RectTile's tile grid + side-view gravity.

- **Gravity**: Engine built-in (no separate `Gravity` property — fall speed is adjusted via `JumpDrag`).
- **Movement**: Left/right + jump.
- **Jump**: `JumpSpeed` (jump velocity), `JumpDrag` (fall speed).
- **Down-jump**: `EnableDownJump`, `DownJumpSpeed`.

```lua
-- SideviewbodyComponent key properties
local svb = self.Entity.SideviewbodyComponent
svb.JumpSpeed = 5         -- jump speed (higher = jumps higher)
svb.JumpDrag = 3          -- fall speed (higher = falls faster)
svb.EnableDownJump = true -- enable down-jump
svb.DownJumpSpeed = 3.3   -- down-jump rebound speed
```

---

## 3. Terrain & Collision

- Uses **`RectTileMapComponent`** (same tile system as RectTile).
- Concept of standing on tiles + falling due to gravity.
- `IsOnGround()`: Whether standing on a tile.
- `GetUnderfootTile()`: Info about the tile currently under feet.

```lua
-- Check underfoot tile
local svb = self.Entity.SideviewbodyComponent
local tileInfo = svb:GetUnderfootTile()
if tileInfo ~= nil then
    log("Underfoot tile: " .. tileInfo.Name)
end
```

---

## 4. Events

| Event | Triggered when |
|---|---|
| `RectTileEnterEvent` | Entering a tile |
| `RectTileLeaveEvent` | Leaving a tile |
| `RectTileCollisionBeginEvent` | Collision tile contact begins (**used for wall detection**) |
| `RectTileCollisionEndEvent` | Collision tile contact ends |

---

## 5. Monster / NPC Development

**Requirements**:
1. Monster `.model` must include **`SideviewbodyComponent`**.
2. **Gravity is automatic** → must spawn on top of tiles to avoid falling.
3. Left/right movement only (no top-down movement).
4. Movement driven by `MoveVelocity`.

```lua
-- SideViewRectTile monster basic patrol pattern
@Component
script MonsterWalk extends Component

@Sync
property boolean movingRight = true

[server only]
void OnUpdate(number delta)
{
    local svb = self.Entity.SideviewbodyComponent
    if svb == nil then return end

    -- Only move while on the ground
    if svb:IsOnGround() == false then return end

    -- Set movement direction
    local dir = 1
    if self.movingRight == false then dir = -1 end
    svb.MoveVelocity = Vector2(dir, 0)
}

-- Reverse direction on wall collision (no PredictFootholdEnd, so use collision events)
[self]
HandleRectTileCollisionBeginEvent(RectTileCollisionBeginEvent event)
{
    local normal = event.Normal
    if normal == Vector2.left or normal == Vector2.right then
        self.movingRight = not self.movingRight
    end
}

end
```

---

## 6. Special Features

- **Wall detection**: Identify wall direction via `RectTileCollisionBeginEvent`'s `Normal` vector.
- **Custom movement**: Drive `MoveVelocity` directly → implement slippery floors, acceleration/deceleration.
- **Dynamic tiles**: Runtime tile manipulation available, same as RectTile.

---

## 7. MovementComponent — InputSpeed Conversion

**In SideViewRectTile**: `direction.x * InputSpeed * 1.5f`, Y preserves existing velocity (to avoid breaking gravity).

| TileMapMode | Actual speed | Notes |
|---|---|---|
| MapleTile | `InputSpeed` passed directly to Rigidbody | — |
| RectTile | `direction * InputSpeed / 1.2f` | Migration compatibility |
| **SideViewRectTile (this file)** | `direction.x * InputSpeed * 1.5f`, Y preserved | Correction similar to Rigidbody |

The same `InputSpeed = 3` feels faster than RectTile (×1.5 acceleration).

```lua
local movement = self.Entity.MovementComponent
movement.InputSpeed = 3
movement.JumpForce = 1.5
movement:Jump()
movement:DownJump()
```

---

## 7. Troubleshooting (SideViewRectTile Only)

| Symptom | Cause | Fix |
|---|---|---|
| Entity doesn't move (no error) | Body is not `SideviewbodyComponent` | Body swap |
| Log `[LEA-3004] MissingComponent : Entity is missing 'SideviewbodyComponent'.` | Dynamic entity missing `SideviewbodyComponent` | Add `SideviewbodyComponent` to model/entity's `@components` |
| Floating in mid-air | Using `KinematicbodyComponent` (brought RectTile model as-is) | Switch to `SideviewbodyComponent` |
| Tile collision broken | Using `RigidbodyComponent` (brought MapleTile model as-is) | Switch to `SideviewbodyComponent` |
| Error when calling `PredictFootholdEnd` | Not a Foothold system (MapleTile-only) | Use `RectTileCollisionBeginEvent` Normal for wall detection |
| Monster gets stuck in wall | No wall detection logic | Use `RectTileCollisionBeginEvent + Normal` |
| Down-jump doesn't work | `EnableDownJump = false` | Set `EnableDownJump = true` |
| Falls too fast / too slow | Inappropriate `JumpDrag` | Adjust `JumpDrag` |

> Full symptom dictionary: [`troubleshooting.md`](troubleshooting.md).

---

## 8. Checklist

### Common

- [ ] Read `MapComponent.TileMapMode` as a number directly from `.map` and confirm it is 2
- [ ] Player.model Body is `SideviewbodyComponent` active (DefaultPlayer handles this automatically)
- [ ] Monster/NPC `.model` includes `SideviewbodyComponent`
- [ ] `SpriteRendererComponent.SpriteRUID` is set
- [ ] Spawn calls pass map entity as `parent`

### SideViewRectTile Specific

- [ ] Confirmed using `SideviewbodyComponent` (not `Rigidbody` / `Kinematicbody`)
- [ ] Spawn is on top of tiles (will fall due to gravity)
- [ ] Wall collision handling (`RectTileCollisionBeginEvent + Normal`)
- [ ] `EnableDownJump = true` set if down-jump is needed

---

## 9. Cross-references

- [`platform.md`](platform.md) — 8 core, TileMapMode↔Body mapping table, coordinate system, RUID, spawn, ID
- [`platform-maple.md`](platform-maple.md) / [`platform-rect.md`](platform-rect.md) — Other map types
- [`troubleshooting.md`](troubleshooting.md) — Unified symptom dictionary
- [`tile.md`](tile.md) — Tile painting (Collision property editing, etc.)
- [`entity.md`](entity.md) — Entity placement / Map Work Preflight
