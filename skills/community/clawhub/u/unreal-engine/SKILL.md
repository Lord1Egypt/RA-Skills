---
name: Unreal Engine
description: Avoid common Unreal mistakes — garbage collection, UPROPERTY macros, replication authority, and asset reference pitfalls.
metadata: {"clawdbot":{"emoji":"🎯","os":["linux","darwin","win32"]}}
---

## Garbage Collection
- Raw pointers to UObjects get garbage collected — use `UPROPERTY()` to prevent
- `UPROPERTY()` marks for GC tracking — without it, pointer becomes dangling
- `TWeakObjectPtr` for optional references — doesn't prevent collection, check `IsValid()`
- `NewObject<T>()` for UObjects — never raw `new`, GC won't track it

## UPROPERTY and UFUNCTION
- `UPROPERTY()` required for Blueprint access — and for GC tracking
- `UFUNCTION()` for Blueprint callable/events — also required for replication
- `EditAnywhere` vs `VisibleAnywhere` — edit allows changes, visible is read-only
- `BlueprintReadWrite` vs `BlueprintReadOnly` — controls Blueprint access level

## Actor Lifecycle
- `BeginPlay` after all components initialized — safe to access components
- Constructor runs on CDO (Class Default Object) — don't spawn actors or access world
- `PostInitializeComponents` before BeginPlay — for component setup
- `EndPlay` for cleanup — called on destroy and level transition

## Tick Performance
- Disable tick when not needed — `PrimaryActorTick.bCanEverTick = false`
- Use timers instead of tick + counter — `GetWorldTimerManager().SetTimer()`
- Tick groups for ordering — `PrePhysics`, `DuringPhysics`, `PostPhysics`
- Blueprint tick expensive — move hot logic to C++

## Replication
- Server is authority — clients request, server validates and replicates
- `UPROPERTY(Replicated)` for variable sync — implement `GetLifetimeReplicatedProps`
- `UFUNCTION(Server)` for client-to-server RPC — must be `Reliable` or `Unreliable`
- `HasAuthority()` to check if server — before executing authoritative logic
- `Role` and `RemoteRole` for network role checks — `ROLE_Authority` is server

## Asset References
- Hard references load with parent — bloats memory, use for always-needed
- Soft references (`TSoftObjectPtr`) load on demand — for optional or large assets
- `LoadSynchronous()` or `AsyncLoad` for soft refs — don't access until loaded
- Blueprint class references: `TSubclassOf<T>` — type-safe class selection

## Memory and Pointers
- `TSharedPtr` for non-UObjects — reference counted, auto-deletes
- `TUniquePtr` for exclusive ownership — can't copy, moves only
- `MakeShared<T>()` for creation — single allocation for object and control block
- Never mix raw `new/delete` with smart pointers — choose one pattern

## Common Mistakes
- Accessing null actor in Blueprint — use `IsValid()` node before access
- PIE (Play In Editor) vs packaged build differ — test shipping build
- Hot reload corrupts Blueprints — close editor, build, reopen
- `GetWorld()` null in constructor — world doesn't exist yet, use BeginPlay
- Spawning in constructor crashes — defer to BeginPlay or later
- `FString` for display, `FName` for identifiers — FName is hashed, faster comparison
