# Platform: MapleTile (Side-View Platformer) — `TileMapMode = 0`

**When to read this file**: When the `.map` you're working with has `MapComponent.TileMapMode` = **`0` (MapleTile)**, or when working on MapleStory-style side-scrolling action (jump / ladder / free-position platforms).

> This file was split from [`platform.md`](platform.md) as a **MapleTile-specific guide**. Rules common to all map types (8 core, coordinate system, RUID, spawn, ID, .config) remain in [`platform.md`](platform.md). Other map types: [`platform-rect.md`](platform-rect.md) / [`platform-sideview.md`](platform-sideview.md).

---

## 1. Map Type at a Glance

| Item | Value |
|---|---|
| TileMapMode | `0` |
| Enum name | `MapleTile` |
| View | Side-view (side-scrolling) |
| Body component | **`RigidbodyComponent`** |
| Map component | `TileMapComponent` + `FootholdComponent` |
| Gravity | **Yes (built-in, adjustable)** |
| Terrain | **Foothold (line segments)** — non-grid free placement |
| Movement axes | Left/right + jump (Y = gravity) |
| Collision | Foothold collision |
| Representative genres | MapleStory-style platformer |

---

## 2. Grid / Physics / Properties

### Grid Size

`TileMapComponent.GridSize` is **fixed at `(0.45, 0.3)`** (`static readonly`). Cannot be changed.

### Physics System

MapleStory's unique **Foothold-based** physics.

- **Gravity**: `RigidbodyComponent.Gravity` (has default, adjustable)
- **Walking on platforms**: `WalkSpeed`, `WalkAcceleration`, `WalkDrag`
- **Air movement**: `AirAccelerationX`, `AirDecelerationX`, `FallSpeedMaxX/Y`
- **Jump**: `WalkJump` (height), `JumpBias` (hang time)
- **Mass**: `Mass` (acceleration/deceleration responsiveness)

```lua
-- RigidbodyComponent key properties example setup
local rb = self.Entity.RigidbodyComponent
rb.Gravity = 30          -- gravity strength
rb.WalkSpeed = 3         -- max movement speed
rb.WalkJump = 6          -- jump height
rb.WalkAcceleration = 10 -- movement acceleration
rb.WalkDrag = 1          -- movement friction
rb.Mass = 1              -- mass
```

---

## 3. Foothold System (Terrain & Collision)

- **`FootholdComponent`**: Manages all footholds on the map. Interacts with `RigidbodyComponent`.
- Footholds are **line segments (StartPoint ~ EndPoint)**.
- Walking only happens on footholds — **falls due to gravity** without one.
- `DownJump()`: Jump downward (fall through foothold)
- `IsOnGround()`: Check if standing on a foothold
- `GetCurrentFoothold()`: Get current foothold info under feet
- `PredictFootholdEnd(distance, isForward)`: Predict distance to foothold end

```lua
-- Check if on a foothold
if self.Entity.RigidbodyComponent:IsOnGround() then
    -- Logic that only runs while on a foothold
end

-- Foothold end detection (AI monster)
if self.Entity.RigidbodyComponent:PredictFootholdEnd(1, true) then
    -- Within 1 unit of right edge → reverse direction
end
```

---

## 4. Events

| Event | Triggered when |
|---|---|
| `FootholdEnterEvent` | Landing on a foothold |
| `FootholdLeaveEvent` | Leaving a foothold |
| `FootholdCollisionEvent` | Colliding with a foothold |
| `RigidbodyAttachEvent` | Attached via `AttachTo` |
| `RigidbodyDetachEvent` | Detached via `Detach` |

---

## 5. Monster / NPC Development

**Requirements**:
1. Monster `.model` must include **`RigidbodyComponent`**.
2. `Gravity = 0` means **floating in mid-air** → always set to positive.
3. `WalkSpeed = 0` means **cannot move**.
4. Spawn Y must be above a foothold (below foothold = infinite fall).

```lua
-- MapleTile monster basic patrol pattern
@Component
script MonsterAI extends Component

property boolean movingRight = true

[server only]
void OnUpdate(number delta)
{
    local rb = self.Entity.RigidbodyComponent
    if rb == nil then return end

    -- Only move while on a foothold
    if rb:IsOnGround() == false then return end

    -- Detect foothold end → reverse direction
    if rb:PredictFootholdEnd(0.5, self.movingRight) then
        self.movingRight = not self.movingRight
    end

    -- Set movement direction
    local dir = 1
    if self.movingRight == false then dir = -1 end
    rb.MoveVelocity = Vector2(dir, 0)
}

end
```

---

## 6. Special Features

- **KinematicMove mode**: Setting `RigidbodyComponent.KinematicMove = true` switches to top-down movement mode (moves top-down style on a MapleTile map).
- **AttachTo / Detach**: Attach to another entity (moving platforms, etc.).
- **AddForce / SetForce**: Apply physics-based forces (knockback, push).

---

## 7. MovementComponent — InputSpeed Conversion

`MovementComponent` is a high-level wrapper usable with all Body types.
**In MapleTile**: `InputSpeed` is passed directly to Rigidbody.

| TileMapMode | Actual speed | Notes |
|---|---|---|
| **MapleTile (this file)** | `InputSpeed` passed directly to Rigidbody | — |
| RectTile | `direction * InputSpeed / 1.2f` | 1.2 divisor for migration compatibility |
| SideViewRectTile | `direction.x * InputSpeed * 1.5f`, Y preserved | Correction similar to Rigidbody |

- `InputSpeed` default: `1.0` (`MovementComponent`'s `[MODProperty]`, `@Sync`)
- The same `InputSpeed = 3` feels different across map types.

```lua
local movement = self.Entity.MovementComponent
movement.InputSpeed = 3
movement.JumpForce = 1.5
movement:Jump()
movement:DownJump()
movement:MoveToDirection(Vector2(1, 0), delta)
movement:Stop()
```

`PlayerControllerComponent` handles input → action mapping and internally uses `MovementComponent`. Default key mapping: arrows (movement), Alt/Space (jump), down+jump (down-jump). For custom movement, set `PlayerControllerComponent.Enable = false` then control the Body directly.

---

## 7. Troubleshooting (MapleTile Only)

| Symptom | Cause | Fix |
|---|---|---|
| Entity doesn't move (no error) | Body is not `RigidbodyComponent` | Body swap |
| Log `[LEA-3004] MissingComponent : Entity is missing 'RigidbodyComponent'.` | Dynamic entity missing `RigidbodyComponent` | Add `RigidbodyComponent` to model/entity's `@components` |
| Monster floating in mid-air | `Gravity = 0` | Set `Gravity` to positive |
| Monster falls off platform edge | No foothold-end handling | Reverse direction with `PredictFootholdEnd` |
| Monster disappears off-screen | Spawn Y is below foothold | Move spawn Y above foothold |
| Jump can't reach platform | `WalkJump` is less than foothold gap | Increase `WalkJump` |

> Full symptom dictionary: [`troubleshooting.md`](troubleshooting.md). Recommended to compare there when confused with other map types.

---

## 8. Checklist

### Common (All Map Types)

- [ ] Read `MapComponent.TileMapMode` as a number directly from `.map` and confirm it is 0
- [ ] Player.model Body is `RigidbodyComponent` active (DefaultPlayer handles this automatically)
- [ ] Monster/NPC `.model` includes `RigidbodyComponent`
- [ ] `SpriteRendererComponent.SpriteRUID` is set
- [ ] Spawn calls pass map entity as `parent` (`self.Entity.CurrentMap`)

### MapleTile Specific

- [ ] `RigidbodyComponent.Gravity` > 0 (if not using default)
- [ ] Monster spawn Y is above foothold
- [ ] Foothold-end handling logic (`PredictFootholdEnd` or `IsolatedMove`)
- [ ] `WalkJump` provides sufficient jump height for foothold gaps

---

## 9. Cross-references

- [`platform.md`](platform.md) — 8 core, TileMapMode↔Body mapping table, coordinate system, RUID, spawn, ID
- [`platform-rect.md`](platform-rect.md) / [`platform-sideview.md`](platform-sideview.md) — Other map types
- [`troubleshooting.md`](troubleshooting.md) — Unified symptom dictionary
- [`tile.md`](tile.md) — Tile painting (FootholdComponent editing, etc.)
- [`entity.md`](entity.md) — Entity placement / Map Work Preflight
