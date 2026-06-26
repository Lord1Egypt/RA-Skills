# DataStorage — Cost, Limits, and Safe Usage Guide

> **⚠️ IMPORTANT — This document is directly tied to billing.**
> DataStorage calls consume **Credit**, and worlds that exceed their Credit budget may have future requests **blocked**.
> Even today, exceeding the threshold is recorded in the **critical report** (for published worlds). When generating code,
> AI **must** follow the rules below to prevent excessive storage usage.

---

## 0. 90-Second Summary — 5 Rules You Must Follow

1. **Never call DataStorage functions inside `OnUpdate`, every frame, or short-interval timers (<1s).** Saves and reads must be **event-driven** only.
2. **Compare against the cache before writing.** If the value has not changed, do not call `SetAsync`/`SetAndWait`.
3. **For multiple keys, always use `Batch*`.** Running `SetAsync` inside a `for` loop consumes Credit linearly.
4. **Design for value strings ≤ 4,000 bytes.** Going over 4,000 bytes consumes **proportionally more Credit**.
5. **Use `Transact*` only when atomicity is truly required.** It costs **2× the Credit** of Batch.

---

## 1. Hard Limits (immediate error if exceeded)

| Field | Limit (UTF-8 bytes) |
|------|--------------------|
| DataStorage name | 1 ~ 64 |
| Key | 1 ~ 100 |
| Tag | 0 ~ 64 |
| Version | 0 ~ 64 |
| `Update*` value | 0 ~ 50,000 |
| `Set*` value | 0 ~ 300,000 |

> Actually using the per-Set maximum (300KB) burns **75+ Credits** in a single call. Do not store anywhere near the limit.

---

## 2. Credit Model — What AI Must Understand

Credit accumulates and is consumed **per FunctionGroup**, summed across **all instances** of the world.

| FunctionGroup | Granted/min | Max accumulation | Cost per request |
|---|---|---|---|
| **Set** / **Get** | `100 + (concurrent_users × 10)` | grant × 2 | **1 per 4,000 bytes** |
| **Delete** | `50 + (concurrent_users × 2)` | grant × 2 | **1 per 4,000 bytes** |
| **List** / **List DataStorage** / **Delete DataStorage** | `10 + (concurrent_users × 2)` | grant × 2 | 1 |
| **List Sorted** | `50 + (concurrent_users × 2)` | grant × 2 | 1 |
| **None** (local handles such as `GetGlobalDataStorage`) | — | — | 0 |

### Credit by byte size (Set/Get/Delete)

```
0 ~ 4,000 bytes   → 1 credit
4,001 ~ 8,000     → 2 credit
8,001 ~ 12,000    → 3 credit
... (rounded up in 4,000-byte chunks)
```

Key/Tag/Version sizes have **no effect** on Credit. Only the value size is counted.

### Special Rules

- **Reading a non-existent key still consumes Credit** → do not blindly query when existence is unknown.
- **Batch family**: the first 25 entries are charged immediately at call time; the rest are charged when `MoveToNextPageAndWait()` is invoked.
- **Transact family**: **2× the Credit** of Batch. Use only when atomicity is required. Up to 20 keys per call.
- **`MoveToNextPageAndWait()` after `LoadNextPageAndWait()`**: pages already loaded do not consume additional Credit.

---

## 3. Anti-Patterns — Do Not Generate

### ❌ Saving every frame / on a short repeating timer

```lua
-- Forbidden: OnUpdate runs every frame (typically 30~60Hz). Credit is exhausted instantly.
method void OnUpdate(number dt)
    self.storage:SetAsync("Hp", tostring(self.Hp), nil)
end

-- Forbidden: short-interval repeating timers are equivalent
_TimerService:SetTimerRepeat(function()
    self.storage:SetAsync("Pos", tostring(self.Entity.TransformComponent.WorldPosition), nil)
end, 0.1)
```

### ❌ Per-element Set/Get inside a loop

```lua
-- Forbidden: 10 saves = 10 Credits + 10 network requests
for i, item in ipairs(items) do
    self.storage:SetAsync(item.Key, item.Value, nil)
end
```

→ **Replace with**: `BatchSetAndWait` / `BatchSetAsync` (handled in a single request, Credit per request scales with bytes).

### ❌ Saving an unchanged value every time

```lua
-- Forbidden: identical values still consume Credit.
method void OnHit()
    self.storage:SetAsync("LastHit", os.time(), nil)
end
```

→ **Replace with**: save only when the value changes, or **batch up changes on a periodic flush (debounce)**.

### ❌ Storing an entire table as one giant string

```lua
-- Caution: a 50KB result from TableToString costs 13 Credits in a single Set.
local bigStr = _UtilLogic:TableToString(self.EntireInventory)  -- assume 50KB
self.storage:SetAsync("Inventory", bigStr, nil)
```

→ **Replace with**: **split rarely-changing data and frequently-changing data into separate keys**, or save only the diff.

### ❌ Calling DataStorage from the client

`_DataStorageService:Get*DataStorage` is **Server Only**. Calls from client space will not execute.
→ Use **only inside methods marked `@ExecSpace("ServerOnly")`**.

---

## 4. Recommended Patterns

### 4.1 Read once, then serve from in-memory cache

```lua
@ExecSpace("ServerOnly")
method void OnBeginPlay()
    self.storage = _DataStorageService:GetGlobalDataStorage("PlayerStats")
    local errorCode, raw = self.storage:GetAndWait(self.UserId)
    self.cache = (errorCode == 0 and raw) and _UtilLogic:StringToTable(raw) or {}
end

@ExecSpace("ServerOnly")
method void GetStat(string key)
    return self.cache[key]  -- no DB roundtrip
end
```

### 4.2 Writes use a dirty flag + debounce

```lua
-- Mark dirty only on actual change, and flush on a fixed cadence
@ExecSpace("ServerOnly")
method void SetStat(string key, any value)
    if self.cache[key] == value then return end  -- no change → no save
    self.cache[key] = value
    self.dirty = true
end

@ExecSpace("ServerOnly")
method void OnBeginPlay()
    -- Flush example: every 30 seconds, or only on logout / important events
    self.flushTimer = _TimerService:SetTimerRepeat(function()
        if not self.dirty then return end
        self.dirty = false
        self.storage:SetAsync(self.UserId, _UtilLogic:TableToString(self.cache), nil)
    end, 30.0)
end

@ExecSpace("ServerOnly")
method void OnEndPlay()
    if self.flushTimer then _TimerService:ClearTimer(self.flushTimer) end
    if self.dirty then
        self.storage:SetAndWait(self.UserId, _UtilLogic:TableToString(self.cache))
    end
end
```

### 4.3 Use Batch for multiple keys

```lua
@ExecSpace("ServerOnly")
method void SaveAll()
    local kv = {}
    for k, v in pairs(self.cache) do kv[k] = tostring(v) end
    local errorCode, successKeys = self.storage:BatchSetAndWait(kv)
    if errorCode ~= 0 then
        log_warning("BatchSet partial failure, success key count: " .. tostring(#successKeys))
    end
end
```

### 4.4 Use Increase for SortableDataStorage counters

```lua
-- Forbidden pattern: Get → +1 → Set (2× Credit + race condition). Use Increase for atomic update.
local errorCode, newScore = self.ranking:IncreaseAndWait(userId, delta)
```

### 4.5 Pick the right storage for the job

| Storage | Scope | Type | Use Case |
|---|---|---|---|
| `GlobalDataStorage` | World | string | World-wide settings/state |
| `UserDataStorage` | User | string | Inventory, progression |
| `CreatorDataStorage` | Creator (shared across worlds) | string | Creator-wide values |
| `SortableDataStorage` | World | int | Rankings, cumulative scores |

**Rule**: User data must live in `UserDataStorage`. Do not dump `user_<id>_xxx` keys into Global.

---

## 5. AndWait vs Async — Which to Choose

| Suffix | Behavior | When to Use |
|---|---|---|
| `~AndWait` | Synchronous, blocks the script until completion | Initial load (OnBeginPlay), logout save — moments where **blocking is acceptable** |
| `~Async` + callback | Asynchronous, result handled in callback | In-game live saves. Prevents frame drops |

> Credit cost is **the same**. Only the **performance characteristics** differ.

---

## 6. Error Code Handling (Do Not Ignore)

Every DataStorage call returns `errorCode` as its first value. **Always check it.**

| Code | Name | Action |
|---|---|---|
| 0 | Ok | Normal |
| 1000004 | TimedOut | Retry with backoff or fold into the next flush |
| 1000005 | **ResourceExhausted** | **Credit exceeded.** Reduce call frequency immediately. Log an alert. |
| 1000006 | PartialFailure | Batch had partial failure — retry only the failed keys |
| 1000002 | NotFound | First-time access (assign default value) |
| Other | InternalError/Unknown | Log and retry, or give up |

If `ResourceExhausted` ever appears, treat the offending function as a **cost bug** and redesign its call path.

---

## 7. Pre-Generation Checklist (Answer Before Writing Code)

Before adding a DataStorage call to a script, you **must be able to answer all of the following**:

- [ ] Is the method holding this call marked `@ExecSpace("ServerOnly")`?
- [ ] Does this call avoid frames and short timers? (Is it event-driven?)
- [ ] Is the same call repeated inside a loop? If so, can it become a `Batch*`?
- [ ] What is the maximum byte size of the value? If over 4KB, can it be split?
- [ ] Does it save only when the value actually changed? (dirty check)
- [ ] Is `errorCode` branched on? Especially `ResourceExhausted`.
- [ ] Is user data being placed in Global by mistake? (Verify UserDataStorage is used.)
- [ ] If `Transact*` is used, is atomicity actually required? (Otherwise, use Batch.)

---

## 8. References

- API signatures: `./Environment/NativeScripts/Service/DataStorageService.d.mlua`, `./Environment/NativeScripts/Component/GlobalDataStorage.d.mlua`, etc.
