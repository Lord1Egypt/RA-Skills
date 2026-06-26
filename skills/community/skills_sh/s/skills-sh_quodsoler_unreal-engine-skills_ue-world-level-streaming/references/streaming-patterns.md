# Level Streaming Configuration Patterns

Reference patterns for common game types. Choose the pattern that matches your project's world structure and adapt the specifics to your scale and multiplayer requirements.

---

## Pattern 1: Open World with World Partition (UE5)

**Best for:** Large continuous worlds — survival games, open-world RPGs, exploration games.

### Configuration

Enable World Partition on the persistent level. Every actor is managed by the WP grid. Sub-levels are not used.

Streaming radius is configured per-partition in the World Partition editor UI (`LoadingRange` on `URuntimePartition`). World Partition streaming is enabled per-world in the editor, not via ini.

### Data Layers for Dynamic Content

```cpp
// Assign actors to data layers in editor (details panel: Data Layers).
// At runtime, activate/deactivate via UDataLayerManager (UE 5.3+).
// NOTE: UDataLayerSubsystem is deprecated since UE 5.3 — use UDataLayerManager instead.

// Example: interior content (caves, buildings) only loads when player is near
#include "WorldPartition/DataLayer/DataLayerManager.h"
UDataLayerManager* DLMgr = UDataLayerManager::GetDataLayerManager(GetWorld());

// SetDataLayerRuntimeState takes UDataLayerAsset* (asset reference set up in editor)
UDataLayerAsset* InteriorLayerAsset = /* UPROPERTY asset reference */;

// Activate — loads and makes visible
DLMgr->SetDataLayerRuntimeState(InteriorLayerAsset, EDataLayerRuntimeState::Activated);

// Pre-load without making visible (background warm)
DLMgr->SetDataLayerRuntimeState(InteriorLayerAsset, EDataLayerRuntimeState::Loaded);

// Unload completely
DLMgr->SetDataLayerRuntimeState(InteriorLayerAsset, EDataLayerRuntimeState::Unloaded);
```

### Streaming Radius per Player (Multiplayer)

World Partition automatically uses each player controller as a streaming source. Each controller can have a different runtime cell size. Override `IWorldPartitionStreamingSourceProvider` for non-player streaming sources (e.g., AI directors, cinematic cameras).

### HLOD Setup

1. Open World Partition editor panel.
2. Add HLOD layers: one per LOD tier (e.g., far, medium).
3. Set cell size to match grid (e.g., 128m cells = 12800 units).
4. Build HLODs before shipping: **Build -> Build World Partition HLODs**.

### Anti-Patterns for This Setup

- Do not use streaming volumes — they have no effect in World Partition.
- Do not add actors to persistent level outside of World Partition (they will always be loaded).
- Do not use `UGameplayStatics::LoadStreamLevel` — there are no named sub-levels to target.

---

## Pattern 2: Hub-and-Spoke with Manual Sub-Level Streaming

**Best for:** Games with discrete zones (MMO zones, dungeon crawlers, hub worlds with portal travel).

### Persistent Level

The persistent level contains: GameMode, GameState, player spawn points, UI actors, and global managers. It never unloads during a session.

### Sub-Levels Setup

Each zone is a separate `.umap` added to the persistent level's streaming list in the editor. Zones are loaded on demand.

```cpp
// MyZoneManager.h — UWorldSubsystem for zone state tracking
UCLASS()
class UMyZoneManager : public UWorldSubsystem
{
    GENERATED_BODY()

public:
    void LoadZone(FName ZoneLevelName);
    void UnloadZone(FName ZoneLevelName);
    bool IsZoneLoaded(FName ZoneLevelName) const;

private:
    TSet<FName> LoadedZones;

    UFUNCTION()
    void OnZoneLoaded() { /* update LoadedZones */ }
};
```

```cpp
// MyZoneManager.cpp
void UMyZoneManager::LoadZone(FName ZoneLevelName)
{
    FLatentActionInfo LatentInfo;
    LatentInfo.CallbackTarget = this;
    LatentInfo.ExecutionFunction = FName("OnZoneLoaded");
    LatentInfo.Linkage = 0;
    LatentInfo.UUID = GetTypeHash(ZoneLevelName);

    UGameplayStatics::LoadStreamLevel(this, ZoneLevelName, true, false, LatentInfo);
}

void UMyZoneManager::UnloadZone(FName ZoneLevelName)
{
    FLatentActionInfo LatentInfo;
    LatentInfo.CallbackTarget = this;
    LatentInfo.ExecutionFunction = FName("OnZoneUnloaded");
    LatentInfo.Linkage = 0;
    LatentInfo.UUID = GetTypeHash(ZoneLevelName) + 1;

    UGameplayStatics::UnloadStreamLevel(this, ZoneLevelName, LatentInfo, false);
    LoadedZones.Remove(ZoneLevelName);
}
```

### Pre-Loading Adjacent Zones

Load neighbor zones into `LoadedNotVisible` state so they are in memory before the player arrives:

```cpp
void UMyZoneManager::PreloadAdjacentZone(FName ZoneLevelName)
{
    const TArray<ULevelStreaming*>& Levels = GetWorld()->GetStreamingLevels();
    for (ULevelStreaming* Level : Levels)
    {
        if (Level->GetWorldAssetPackageFName() == ZoneLevelName)
        {
            Level->SetShouldBeLoaded(true);
            Level->SetShouldBeVisible(false); // Load but keep invisible
            // Changes are picked up by the streaming system each frame automatically
            return;
        }
    }
}
```

### Loading Screen Handoff

Before loading screen dismiss, wait for the target zone to reach `LoadedVisible`:

```cpp
void UMyHUD::WaitForZoneVisible(FName ZoneLevelName)
{
    GetWorld()->GetTimerManager().SetTimer(
        PollTimerHandle,
        [this, ZoneLevelName]()
        {
            for (ULevelStreaming* Level : GetWorld()->GetStreamingLevels())
            {
                if (Level->GetWorldAssetPackageFName() == ZoneLevelName &&
                    Level->GetLevelStreamingState() == ELevelStreamingState::LoadedVisible)
                {
                    DismissLoadingScreen();
                    GetWorld()->GetTimerManager().ClearTimer(PollTimerHandle);
                    return;
                }
            }
        },
        0.1f,   // poll every 100ms
        true    // looping
    );
}
```

---

## Pattern 3: Procedural / Instanced Level Streaming

**Best for:** Roguelikes, procedural dungeons, instanced arenas, modular buildings loaded at runtime.

### Core Pattern: ULevelStreamingDynamic

```cpp
// ProcDungeonGenerator.h
UCLASS()
class AProcDungeonGenerator : public AActor
{
    GENERATED_BODY()

public:
    // Room template level to instance (set in editor)
    UPROPERTY(EditDefaultsOnly)
    TSoftObjectPtr<UWorld> RoomTemplate;

    void SpawnRoom(FTransform RoomTransform, FString InstanceName);
    void DespawnRoom(FString InstanceName);

private:
    UPROPERTY()
    TMap<FString, TObjectPtr<ULevelStreamingDynamic>> SpawnedRooms;

    UFUNCTION()
    void OnRoomVisible();
};
```

```cpp
// ProcDungeonGenerator.cpp
void AProcDungeonGenerator::SpawnRoom(FTransform RoomTransform, FString InstanceName)
{
    ULevelStreamingDynamic::FLoadLevelInstanceParams Params(
        GetWorld(),
        RoomTemplate.GetLongPackageName(),
        RoomTransform
    );
    Params.OptionalLevelNameOverride = &InstanceName; // Deterministic name for net sync
    Params.bInitiallyVisible = true;

    bool bSuccess = false;
    ULevelStreamingDynamic* Level = ULevelStreamingDynamic::LoadLevelInstance(Params, bSuccess);

    if (bSuccess && Level)
    {
        Level->OnLevelShown.AddDynamic(this, &AProcDungeonGenerator::OnRoomVisible);
        SpawnedRooms.Add(InstanceName, Level);
    }
}

void AProcDungeonGenerator::DespawnRoom(FString InstanceName)
{
    if (ULevelStreamingDynamic** Level = SpawnedRooms.Find(InstanceName))
    {
        (*Level)->SetShouldBeLoaded(false);
        (*Level)->SetShouldBeVisible(false);
        (*Level)->SetIsRequestingUnloadAndRemoval(true);
        SpawnedRooms.Remove(InstanceName);
    }
}
```

### Multiplayer: Replicating Instance Names

The server spawns room instances with deterministic names (e.g., "Room_0001", "Room_0002"). It replicates these names to clients via a replicated array on GameState. Clients call `LoadLevelInstance` with the same `OptionalLevelNameOverride`. The names must match exactly — without this, clients and server reference different package names and streaming breaks.

```cpp
// MyGameState.h
UPROPERTY(ReplicatedUsing=OnRep_SpawnedRooms)
TArray<FString> SpawnedRoomNames;

UFUNCTION()
void OnRep_SpawnedRooms();

// MyGameState.cpp — client side
void AMyGameState::OnRep_SpawnedRooms()
{
    for (const FString& RoomName : SpawnedRoomNames)
    {
        // Load each room with the replicated name as the override
        // so the package name matches what the server has
        DungeonGenerator->SpawnRoom(GetRoomTransform(RoomName), RoomName);
    }
}
```

---

## Pattern 4: Linear Level Sequence (Chapter / Act Structure)

**Best for:** Narrative games, linear action games with distinct chapters or missions.

### Approach

Each chapter is a separate `.umap`. A small persistent level holds global actors. Travel between chapters uses seamless travel (multiplayer) or `OpenLevel` (single-player).

### Single-Player: OpenLevel with GameInstance State

```cpp
// Save chapter progress to GameInstance before traveling
void AMyGameMode::TravelToChapter(FName ChapterMapName)
{
    UMyGameInstance* GI = GetGameInstance<UMyGameInstance>();
    if (GI)
    {
        GI->LastCompletedChapter = CurrentChapter;
        GI->PlayerInventory = CollectPlayerInventory();
    }

    UGameplayStatics::OpenLevel(this, ChapterMapName, true);
}
```

### Multiplayer: Seamless Travel

```ini
; DefaultEngine.ini
[/Script/Engine.GameMapsSettings]
TransitionMap=/Game/Maps/Transition_Loading
```

```cpp
// MyGameMode.h
uint32 bUseSeamlessTravel : 1; // set to 1 in constructor

// MyGameMode.cpp
void AMyGameMode::TravelToChapter(const FString& ChapterURL)
{
    // Server initiates; clients follow automatically
    GetWorld()->ServerTravel(ChapterURL);
}

void AMyGameMode::GetSeamlessTravelActorList(bool bToTransition, TArray<AActor*>& ActorList)
{
    Super::GetSeamlessTravelActorList(bToTransition, ActorList);

    if (!bToTransition)
    {
        // Carry GameState into the destination
        ActorList.Add(GameState);
    }
}

void AMyGameMode::HandleSeamlessTravelPlayer(AController*& C)
{
    Super::HandleSeamlessTravelPlayer(C);
    // Restore character state from GameInstance or GameState
    RestorePlayerState(C);
}
```

---

## Pattern 5: Streaming Volume–Driven Interior Loading

**Best for:** Open world games with buildings or interiors that stream in as the player approaches.

### Setup

1. Create a sub-level per interior (e.g., `L_Building_Interior_01`).
2. Place an `ALevelStreamingVolume` in the persistent level surrounding the building exterior.
3. Set `StreamingUsage = SVB_LoadingAndVisibility` on the volume.
4. Assign the sub-level to the volume via the streaming level's `EditorStreamingVolumes` array (set in editor Details panel or via Levels panel).
5. Set `MinTimeBetweenVolumeUnloadRequests = 5.0` seconds on the sub-level to prevent unload flicker when the player stands near the volume boundary.

### Disabling Volume Control at Runtime (Cutscene or Boss Arena)

```cpp
void AMyBossRoomTrigger::BeginPlay()
{
    Super::BeginPlay();
    // Find the streaming level and disable volume-based streaming
    for (ULevelStreaming* Level : GetWorld()->GetStreamingLevels())
    {
        if (Level->GetWorldAssetPackageFName() == FName("/Game/Levels/L_BossArena"))
        {
            // Disable volume control — we'll manage load state from code
            Level->bDisableDistanceStreaming = true;
            return;
        }
    }
}

void AMyBossRoomTrigger::NotifyActorBeginOverlap(AActor* OtherActor)
{
    if (OtherActor->IsA<APlayerCharacter>())
    {
        // Manually load and show
        for (ULevelStreaming* Level : GetWorld()->GetStreamingLevels())
        {
            if (Level->GetWorldAssetPackageFName() == FName("/Game/Levels/L_BossArena"))
            {
                Level->SetShouldBeLoaded(true);
                Level->SetShouldBeVisible(true);
                // Changes are picked up by the streaming system each frame automatically
            }
        }
    }
}
```

---

## Dedicated Server Streaming Considerations

On a dedicated server, there is no rendering pipeline. Streaming must be entirely logic-driven.

- **World Partition**: streaming sources on the server must be explicit. Player controller positions are used by default if `APlayerController` is registered as a source.
- **Sub-levels**: call `SetShouldBeLoaded` and `SetShouldBeVisible` explicitly. Volume-based streaming is disabled (no camera player controller overlap in server-only mode without clients).
- **Avoid `bShouldBlockOnLoad`** on the server unless behind a map-change sequence — blocking the server stalls all clients.

```cpp
// Server-side: manually drive zone loading based on player positions
// Inherits UTickableWorldSubsystem (UWorldSubsystem has no Tick)
void UServerZoneSubsystem::Tick(float DeltaTime)
{
    if (GetWorld()->GetNetMode() != NM_DedicatedServer) return;

    for (APlayerController* PC : TActorRange<APlayerController>(GetWorld()))
    {
        FVector PlayerPos = PC->GetPawn() ? PC->GetPawn()->GetActorLocation() : FVector::ZeroVector;
        FName TargetZone = DetermineZoneForPosition(PlayerPos);
        if (!LoadedZones.Contains(TargetZone))
        {
            LoadZone(TargetZone);
        }
    }
}
```

---

## Performance Benchmarks and Budget Guidelines

| Scenario | Recommended Cell/Zone Size | Max Simultaneous Loaded Levels |
|---|---|---|
| Open world (WP) | 128m–256m cells | N/A (grid-based) |
| Hub-and-spoke zones | Per zone (no fixed size) | 2–3 (current + neighbors) |
| Procedural rooms | Per room (10m–50m) | 10–30 depending on actor counts |
| Interior streaming | Per building | 3–5 around player |

**Actor counts per cell (World Partition):** Keep under 1000 dynamic actors per cell. Static meshes are merged by HLOD and do not count against this limit in distant cells.

**Loading budget per frame:** Level streaming operations are spread across frames. `bShouldBlockOnLoad` forces all operations into a single frame — only acceptable during loading screens. Async loading typically completes in 0.5–5 seconds depending on level size and disk speed.
