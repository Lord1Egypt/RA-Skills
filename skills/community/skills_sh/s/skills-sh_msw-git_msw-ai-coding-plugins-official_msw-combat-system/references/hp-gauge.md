# HP gauge — PixelRendererComponent + Lazy Init

> All `PixelRendererComponent` methods are `@ExecSpace("ClientOnly")` — the buffer init and per-pixel writes must run on the client.

---

## Why PixelRendererComponent

Alternative ways to attach a health bar to a dynamically spawned entity, and their failure cases:

| Approach | Issue |
|----------|-------|
| Add a child entity to the `.model`'s Children JSON | File-format errors possible; load fails when a PixelRenderer is included |
| Spawn a separate child via `SpawnByModelId` | Only the first spawn succeeds; subsequent failure cases exist |
| `SpriteRendererComponent` + a solid-color sprite | A solid-color rectangle RUID is not provided by default — requires a separate upload |
| **Include `PixelRendererComponent` directly in the model's Components** | **Most stable** — as a native component, it can be included in `.model` |

`PixelRendererComponent` is a native component — it can be included in `.model` directly, without the missing-`.codeblock` silent-drop risk that custom scripts have.

---

## Flow

```
Server: HP/MaxHP change (@Sync)
  └→ Client: OnSyncProperty("HP"/"MaxHP") detected
       └→ UpdateHealthBar() — paint via SetPixel
Client OnUpdate: check PixelRenderer readiness → InitHealthBar() (lazy init)
```

---

## Step 1: Add PixelRendererComponent to the model

Add the following component to the `.model`:

| Component | Key value |
|-----------|-----------|
| `MOD.Core.PixelRendererComponent` | If `SortingLayer` is the default (`"Default"`), map layers are not reflected → adjust to `"MapLayer0"` in the Maker editor or set at runtime in script (below) |

Setting SortingLayer at runtime:
```lua
-- Inside InitHealthBar
pixel.SortingLayer = "MapLayer0"
pixel.OrderInLayer = 10    -- Higher than the monster SpriteRenderer (OrderInLayer=2)
```

---

## Step 2: Script — @Sync HP/MaxHP + full HP gauge template

```lua
@Component
script MonsterAI extends Component

    @Sync
    property number HP = 100

    @Sync
    property number MaxHP = 100

    -- Client: initialize the pixel buffer (Lazy Init)
    -- Why Lazy Init: for dynamically spawned entities the PixelRendererComponent
    -- may not be ready on the client at OnBeginPlay time
    @ExecSpace("ClientOnly")
    method void InitHealthBar()
        local pixel = self.Entity.PixelRendererComponent
        if pixel == nil then return end
        -- 16×3: 16 px wide (HP steps), 3 px tall (thickness)
        -- SetPixel coordinate system: bottom-left (1,1) origin
        pixel:ResetWithColor(16, 3, Color(0, 1, 0, 1))
        pixel.SortingLayer = "MapLayer0"
        pixel.OrderInLayer = 10
        self._T.hpBarPixel   = pixel
        self._T.hpBarInited  = true
        self:UpdateHealthBar()
    end

    -- Client: paint pixels based on HP ratio
    @ExecSpace("ClientOnly")
    method void UpdateHealthBar()
        if not self._T.hpBarInited then return end
        local pixel = self._T.hpBarPixel
        if pixel == nil then return end

        local ratio = 0
        if self.MaxHP > 0 then
            ratio = math.max(0, self.HP / self.MaxHP)
        end
        local fillWidth = math.max(0, math.floor(ratio * 16))

        -- Color thresholds: >60% → green, 31~60% → yellow, 0~30% → red
        local barColor
        if ratio <= 0.3 then
            barColor = Color(1, 0, 0, 1)
        elseif ratio <= 0.6 then
            barColor = Color(1, 1, 0, 1)
        else
            barColor = Color(0, 1, 0, 1)
        end

        for x = 1, 16 do
            for y = 1, 3 do
                if x <= fillWidth then
                    pixel:SetPixel(x, y, barColor)
                else
                    pixel:SetPixel(x, y, Color(0.2, 0.2, 0.2, 0.8))
                end
            end
        end
    end

    -- @Sync property change detection → refresh the bar
    @ExecSpace("ClientOnly")
    method void OnSyncProperty(string name, any value)
        if name == "HP" or name == "MaxHP" then
            self:UpdateHealthBar()
        end
    end

    -- OnUpdate: no @ExecSpace → runs on both server and client
    -- Branch via IsClient()/IsServer() (health bar on client, combat logic on server)
    method void OnUpdate(number delta)
        if self:IsClient() then
            if self._T.hpBarInited == nil then self._T.hpBarInited = false end
            if not self._T.hpBarInited then
                self:InitHealthBar()
            end
        end

        if not self:IsServer() then return end
        -- Server-only logic (AI, death handling, etc.)
    end

    @EventSender("Self")
    @ExecSpace("ServerOnly")
    handler HandleHitEvent(HitEvent event)
        self.HP -= event.TotalDamage
        if self.HP <= 0 then
            self.HP = 0
            self.Entity.StateComponent:ChangeState("DEAD")
            -- Death handling is in a separate DeadEvent handler
        end
    end

    method void OnEndPlay()
        self.Entity:DisconnectEvent(HitEvent, self.HandleHitEvent)
    end

end
```

---

## PixelRendererComponent API summary

```
-- Buffer init
@ExecSpace("ClientOnly") ResetWithColor(int32 width, int32 height, Color color)
@ExecSpace("ClientOnly") ResetWithColors(int32 width, int32 height, table<Color> pixels)

-- Pixel read/write  coordinates: bottom-left (1,1)
@ExecSpace("ClientOnly") SetPixel(int32 x, int32 y, Color color)
@ExecSpace("ClientOnly") GetPixel(int32 x, int32 y) → Color
@ExecSpace("ClientOnly") SetPixels(table<Color> pixels)   -- Width*Height in size
@ExecSpace("ClientOnly") GetPixels() → table<Color>

-- Fill all
@ExecSpace("ClientOnly") FillColor(Color color)
@ExecSpace("ClientOnly") SetAlpha(float alpha)

-- Properties
property int32  OrderInLayer = 0
property string SortingLayer = "Default"   -- For map entities, change to "MapLayer0"
property int32  Width  = 16   (read-only: set via ResetWithColor)
property int32  Height = 16
```

Recommended size: **16×N (N=2~4)**. Performance degrades above 16×16.

`Width` / `Height` are **logical pixels** of the texture grid, not screen pixels — the on-screen size scales with the entity's `TransformComponent.Scale`. Keep the logical grid small (`16×3`) and grow it visually through scale (e.g. `Scale = (4, 4, 1)`) instead of enlarging the grid.

---

## Setting MaxHP on spawn

Include `MonsterAI` in the `.model` in advance (after Maker Refresh) → after spawn, only initialize HP/MaxHP via the handle:

```lua
@ExecSpace("ServerOnly")
method void SpawnMonster(Vector3 pos)
    local parent = self.Entity.CurrentMap
    local entity = _SpawnService:SpawnByModelId(
        "monster_1_model", "monster_1", pos, parent  -- 1st arg: the .model's EntryKey, case-insensitive
    )
    local ai = entity.MonsterAI
    if ai ~= nil then
        ai.HP    = 100
        ai.MaxHP = 100
    end
end
```

---

## Constraints

| Item | Rule |
|------|------|
| PixelRenderer methods | **ClientOnly** — error if called from the server |
| Lazy Init | Use **repeated check in OnUpdate** instead of OnBeginPlay — guarantees the client readiness timing of dynamically spawned entities |
| `@Sync` required | If HP/MaxHP are not set, the client health bar will not update |
| `OnUpdate` @ExecSpace | **Unspecified** — handle via IsClient()/IsServer() branches internally |
| Render position | Drawn overlapping the entity's TransformComponent position. Cannot offset to display above the monster separately (child entities are unstable) |
| Recommended resolution | 16×16 or less. The health bar is `16×3` |
