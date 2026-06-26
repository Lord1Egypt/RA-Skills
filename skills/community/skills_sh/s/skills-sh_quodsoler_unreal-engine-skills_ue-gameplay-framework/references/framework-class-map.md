# Gameplay Framework Class Map

Reference table showing where each class lives, who owns it, what it stores, and
the exact lifecycle hook order. Cross-reference with SKILL.md for code examples.

---

## Authority and Presence Matrix

| Class | Dedicated Server | Listen Server (Host) | Listen Server (Remote Client) | Standalone |
|---|---|---|---|---|
| AGameModeBase / AGameMode | YES (authority) | YES (authority) | NO — null | YES (authority) |
| AGameStateBase / AGameState | YES | YES | YES (replicated) | YES |
| APlayerController (local player) | N/A | YES (server+client role) | YES (own only) | YES |
| APlayerController (remote player) | YES (all players) | YES (all players) | NO — not present | N/A |
| APlayerState (all players) | YES (all) | YES (all) | YES (all, replicated) | YES |
| APawn / ACharacter (possessed by local) | YES (auth) | YES (auth+local) | YES (local proxy) | YES |
| APawn / ACharacter (possessed by remote) | YES (auth) | YES (auth) | YES (simulated proxy) | N/A |
| UGameInstance | YES | YES | YES | YES |
| AHUD | NO | YES (host player only) | YES (own only) | YES |
| APlayerCameraManager | NO | YES (host player only) | YES (own only) | YES |

**Key:** "YES (auth)" = exists with `ROLE_Authority`. "YES (simulated proxy)" = exists with `ROLE_SimulatedProxy`, position interpolated from server updates.

---

## Class Ownership Chain

```
UGameInstance  [persists across all level loads]
  |
  +-- UWorld
        |
        +-- AGameMode           [server only]
        |     |
        |     +-- AGameState    [server + all clients]
        |           |
        |           +-- PlayerArray[]  --> APlayerState per player
        |
        +-- APlayerController   [server: all; client: own only]
              |
              +-- APlayerState  [server + all clients]
              |
              +-- AHUD          [local client only]
              |
              +-- APlayerCameraManager  [local client only]
              |
              +-- (possesses) --> APawn / ACharacter
                                    |
                                    +-- UCharacterMovementComponent
                                    +-- UCapsuleComponent  (root)
                                    +-- USkeletalMeshComponent
```

---

## Responsibility Summary

| Class | Primary Responsibility | Do NOT put here |
|---|---|---|
| AGameModeBase | Game rules, join approval, player spawn points, match initialization | Any data clients need to read |
| AGameMode | AGameModeBase + match state machine (WaitingToStart, InProgress, etc.) | Per-player data |
| AGameStateBase | Global replicated state: server clock, player array, has match started | Server-only logic |
| AGameState | AGameStateBase + match elapsed time | Client-only UI state |
| APlayerController | Input, camera, HUD management, possess/unpossess, client↔server RPC bridge | Cross-session data (may be replaced during seamless travel if PC class changes) |
| APlayerState | Replicated per-player data: name, score, team, ping | Input processing, UI |
| APawn | Minimal possessable actor, custom movement | Anything requiring capsule/mesh/built-in movement |
| ACharacter | Humanoid movement with capsule, skeletal mesh, and CMC prediction | Game rules, scoring |
| UGameInstance | Cross-level persistence: sessions, save game refs, analytics | Per-match state |
| AHUD | Local-only 2D overlay rendering | Any replicated data |

---

## Player Join Sequence (Server Side)

```
1. PreLogin(Options, Address, UniqueId, ErrorMessage)
      Set ErrorMessage != "" to reject.

2. Login(NewPlayer, RemoteRole, Portal, Options, UniqueId, ErrorMessage)
      Creates APlayerController via SpawnPlayerController().
      Creates APlayerState, assigns UniqueId and name.
      Returns new PC (or null on failure).

3. PostLogin(NewPlayer)
      First point where server-to-client RPCs are safe.
      GameState->PlayerArray is populated.
      Override to assign teams, send initial data.

4. HandleStartingNewPlayer(NewPlayer)
      Calls RestartPlayer() if not spectator.

5. RestartPlayer(NewPlayer)
      Calls FindPlayerStart() -> ChoosePlayerStart()
      Calls SpawnDefaultPawnFor()
      Calls NewPlayer->Possess(Pawn)
```

---

## Player Logout Sequence

```
1. Logout(Exiting)            -- GameMode notified (server only)
2. GameState->RemovePlayerState(PS)  -- PlayerArray updated
3. PlayerController destroyed
4. PlayerState destroyed (after ReplicationTimeout or immediately if non-seamless)
```

---

## Seamless Travel Actor Survival

When `bUseSeamlessTravel = true`, the travel happens in two legs:
- **Leg 1:** Current map → Transition map
- **Leg 2:** Transition map → Destination map

`GetSeamlessTravelActorList` is called for BOTH legs.

| Object | Survives Seamless Travel | Notes |
|---|---|---|
| UGameInstance | YES | Never dies |
| APlayerController | YES (transferred) | Engine handles this automatically |
| APlayerState | YES (transferred with PC) | Engine handles this automatically |
| AGameMode | NO | New one spawned in destination map |
| AGameState | NO | New one spawned in destination map |
| APawn / ACharacter | NO (by default) | Destroyed; new one spawned by RestartPlayer |
| Custom actors | Optional | Add in GetSeamlessTravelActorList() |

---

## Movement Mode Reference (UCharacterMovementComponent)

| EMovementMode | Description | Typical Use |
|---|---|---|
| MOVE_None | No movement processed | Ragdoll, dead state |
| MOVE_Walking | On ground, uses NavMesh | Default walking/running |
| MOVE_NavWalking | On NavMesh surface (AI) | AI characters on nav mesh |
| MOVE_Falling | In air, gravity applied | After jump, falling off ledge |
| MOVE_Swimming | In fluid volume | Water traversal |
| MOVE_Flying | No gravity, full air control | Spectator, flying character |
| MOVE_Custom | User-defined (CustomMovementMode byte) | Wall running, zero-G, grapple |

---

## Key Properties Quick Reference

### AGameModeBase Classes

```cpp
TSubclassOf<APawn>              DefaultPawnClass;
TSubclassOf<AGameStateBase>     GameStateClass;
TSubclassOf<APlayerController>  PlayerControllerClass;
TSubclassOf<APlayerState>       PlayerStateClass;
TSubclassOf<AHUD>               HUDClass;
TSubclassOf<ASpectatorPawn>     SpectatorClass;
TSubclassOf<AGameSession>       GameSessionClass;
uint32                          bUseSeamlessTravel : 1;
uint32                          bStartPlayersAsSpectators : 1;
uint32                          bPauseable : 1;
```

### AGameStateBase Replicated Properties

```cpp
TSubclassOf<AGameModeBase>   GameModeClass;       // ReplicatedUsing=OnRep_GameModeClass
TSubclassOf<ASpectatorPawn>  SpectatorClass;      // ReplicatedUsing=OnRep_SpectatorClass
TArray<APlayerState*>        PlayerArray;         // Always relevant
bool                         bReplicatedHasBegunPlay; // ReplicatedUsing=OnRep_ReplicatedHasBegunPlay
double                       ReplicatedWorldTimeSecondsDouble; // server clock sync
```

### APlayerController Notable Members

```cpp
TObjectPtr<APawn>                 AcknowledgedPawn;        // server-confirmed possession
TObjectPtr<APlayerCameraManager>  PlayerCameraManager;
TObjectPtr<AHUD>                  MyHUD;
TObjectPtr<UPlayerInput>          PlayerInput;             // only valid locally
uint32                            bShowMouseCursor : 1;
uint32                            bEnableClickEvents : 1;
uint32                            bEnableStreamingSource : 1;
uint16                            SeamlessTravelCount;
```

### ACharacter Notable Members

```cpp
// Components (access via getters)
USkeletalMeshComponent*        GetMesh()
UCharacterMovementComponent*   GetCharacterMovement()
UCapsuleComponent*             GetCapsuleComponent()

// Replicated state
uint8   bIsCrouched : 1;       // ReplicatedUsing=OnRep_IsCrouched
uint8   bProxyIsJumpForceApplied : 1;
float   JumpMaxHoldTime;       // Replicated — variable jump height
int32   JumpMaxCount;          // Replicated — multi-jump count
int32   JumpCurrentCount;      // current jump count this airtime
uint8   ReplicatedMovementMode; // Replicated — movement mode for simulated proxies
```

---

## NetMode Cheat Sheet

```cpp
GetNetMode() == NM_Standalone      // single player, no network
GetNetMode() == NM_DedicatedServer // server process, no local player
GetNetMode() == NM_ListenServer    // server + local player (host)
GetNetMode() == NM_Client          // remote client

HasAuthority()  // true on server (NM_Standalone, NM_DedicatedServer, NM_ListenServer)
IsLocalController()  // true if this PlayerController belongs to the local machine's player
IsLocallyControlled()  // true on Pawn if its controller is a local player
```

---

## Class Selection Decision Tree

```
Need to store game-wide rules or control who can join?
  --> AGameMode (server-only, authoritative)

Need global data visible to ALL clients (scores, match timer)?
  --> AGameState (replicated everywhere)

Need per-player data visible to ALL clients (kills, team, name)?
  --> APlayerState (always relevant, replicated everywhere)

Need to handle input, camera, or UI for ONE player?
  --> APlayerController (exists on server + owning client only)

Need a player body that walks/jumps/crouches with built-in prediction?
  --> ACharacter (with UCharacterMovementComponent)

Need a custom vehicle, drone, or non-humanoid body?
  --> APawn (with a custom UPawnMovementComponent or manual physics)

Need data that survives level transitions?
  --> UGameInstance (singleton per process, never destroyed)
```
