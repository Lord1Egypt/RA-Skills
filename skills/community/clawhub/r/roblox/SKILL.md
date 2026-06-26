---
name: Roblox
description: Avoid common Roblox mistakes — server/client security, DataStore pitfalls, memory leaks, and replication gotchas.
metadata: {"clawdbot":{"emoji":"🎲","os":["linux","darwin","win32"]}}
---

## Server vs Client
- Server scripts in ServerScriptService — never trust client data
- LocalScripts in StarterPlayerScripts or StarterGui — client-only
- RemoteEvent for fire-and-forget — RemoteFunction when server needs to return value
- ALWAYS validate on server — client can send anything, exploiters will

## Security
- Never trust client input — validate everything server-side
- Server-side sanity checks — is player allowed? Is value reasonable?
- FilteringEnabled is always on — but doesn't protect your RemoteEvents
- Don't expose admin commands via RemoteEvents — check permissions server-side

## DataStore
- `:GetAsync()` and `:SetAsync()` can fail — wrap in pcall, retry with backoff
- Rate limits: 60 + numPlayers × 10 requests/minute — queue writes, batch when possible
- `:UpdateAsync()` for read-modify-write — prevents race conditions
- Session locking — prevent data loss on rejoin, use `:UpdateAsync()` with check
- Test with Studio API access enabled — Settings → Security → API Services

## Memory Leaks
- Connections not disconnected — store and `:Disconnect()` when done
- `:Destroy()` instances when removed — sets Parent to nil and disconnects events
- Player leaving without cleanup — `Players.PlayerRemoving` to clean up
- Tables holding references — nil out references you don't need

## Character Handling
- Character may not exist at PlayerAdded — use `player.CharacterAdded:Wait()` or event
- Character respawns = new character — reconnect events on CharacterAdded
- `Humanoid.Died` fires on death — for death handling logic
- `LoadCharacter()` to force respawn — but prefer natural respawn usually

## Replication
- ServerStorage: server-only — clients can't see
- ReplicatedStorage: both see — shared modules and assets
- ReplicatedFirst: loads first on client — loading screens
- Workspace replicates to clients — but server is authority

## Services Pattern
- `game:GetService("ServiceName")` — don't index directly, fails in different contexts
- Cache service references — `local Players = game:GetService("Players")`
- Common: Players, ReplicatedStorage, ServerStorage, RunService, DataStoreService

## RunService
- `Heartbeat` after physics — most gameplay logic
- `RenderStepped` client only, before render — camera, visual updates
- `Stepped` before physics — physics manipulation
- Avoid heavy computation every frame — spread over multiple frames

## Common Mistakes
- `wait()` deprecated — use `task.wait()` for reliable timing
- `spawn()` deprecated — use `task.spawn()` or `task.defer()`
- Module require returns cached — same table across requires, changes shared
- `:Clone()` doesn't fire events — manually fire if needed
- Part collisions with CanCollide false — still fire Touched, use CanTouch
