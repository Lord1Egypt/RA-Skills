# Save System Architecture

Complete patterns for production save systems: slot management, save metadata, async pipelines, multi-user handling, and corruption recovery.

---

## Architecture Overview

A production save system has three layers:

```
┌─────────────────────────────────────────────────────────┐
│  Game Code (GameMode, PlayerController, Subsystems)     │
│  -- calls SaveManager --                                │
├─────────────────────────────────────────────────────────┤
│  Save Manager (UGameInstanceSubsystem)                  │
│  -- slot routing, async coordination, migration --      │
├─────────────────────────────────────────────────────────┤
│  UGameplayStatics / ISaveGameSystem                     │
│  -- platform-agnostic file I/O --                       │
└─────────────────────────────────────────────────────────┘
```

The save manager lives on the `UGameInstance` as a `UGameInstanceSubsystem` so it persists across level transitions and map loads.

---

## 1. Save Metadata (Slot List)

Store a lightweight metadata object in a fixed slot so the UI can display save slot info (timestamp, player name, level, screenshot thumbnail path) without loading the full save payload.

```cpp
// SaveMetadata.h
#pragma once
#include "CoreMinimal.h"
#include "GameFramework/SaveGame.h"
#include "SaveMetadata.generated.h"

USTRUCT(BlueprintType)
struct FSaveSlotInfo
{
    GENERATED_BODY()

    UPROPERTY(SaveGame, BlueprintReadOnly)
    int32 SlotIndex = -1;

    UPROPERTY(SaveGame, BlueprintReadOnly)
    FString PlayerDisplayName;

    UPROPERTY(SaveGame, BlueprintReadOnly)
    FString MapName;

    UPROPERTY(SaveGame, BlueprintReadOnly)
    int32 PlayerLevel = 0;

    UPROPERTY(SaveGame, BlueprintReadOnly)
    FDateTime LastSaveTime;

    UPROPERTY(SaveGame, BlueprintReadOnly)
    float TotalPlayTimeSeconds = 0.f;

    UPROPERTY(SaveGame, BlueprintReadOnly)
    bool bIsValid = false;

    // Path to a thumbnail screenshot stored in Saved/Screenshots/
    UPROPERTY(SaveGame, BlueprintReadOnly)
    FString ThumbnailPath;
};

UCLASS()
class MYGAME_API USaveMetadataBank : public USaveGame
{
    GENERATED_BODY()

public:
    static constexpr int32 MaxSlots = 10;
    static const FString SlotName;     // "SaveMetadataBank"
    static constexpr int32 UserIndex = 0;

    UPROPERTY(SaveGame)
    TArray<FSaveSlotInfo> Slots;

    // Initialize with empty slots
    void Init()
    {
        Slots.SetNum(MaxSlots);
        for (int32 i = 0; i < MaxSlots; ++i)
        {
            Slots[i].SlotIndex = i;
            Slots[i].bIsValid  = false;
        }
    }

    const FSaveSlotInfo* GetSlot(int32 Index) const
    {
        if (Slots.IsValidIndex(Index)) { return &Slots[Index]; }
        return nullptr;
    }

    void UpdateSlot(int32 Index, const FSaveSlotInfo& Info)
    {
        if (Slots.IsValidIndex(Index))
        {
            Slots[Index] = Info;
            Slots[Index].SlotIndex = Index;
            Slots[Index].bIsValid  = true;
        }
    }

    void ClearSlot(int32 Index)
    {
        if (Slots.IsValidIndex(Index))
        {
            Slots[Index] = FSaveSlotInfo();
            Slots[Index].SlotIndex = Index;
        }
    }
};

const FString USaveMetadataBank::SlotName = TEXT("SaveMetadataBank");
```

---

## 2. Save Manager Subsystem

```cpp
// SaveManager.h
#pragma once
#include "CoreMinimal.h"
#include "Subsystems/GameInstanceSubsystem.h"
#include "SaveMetadata.h"
#include "MyGameSaveGame.h"
#include "SaveManager.generated.h"

DECLARE_DYNAMIC_MULTICAST_DELEGATE_TwoParams(FOnSaveComplete, int32, SlotIndex, bool, bSuccess);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_TwoParams(FOnLoadComplete, int32, SlotIndex, bool, bSuccess);

UCLASS()
class MYGAME_API USaveManager : public UGameInstanceSubsystem
{
    GENERATED_BODY()

public:
    // USubsystem interface
    virtual void Initialize(FSubsystemCollectionBase& Collection) override;
    virtual void Deinitialize() override;

    // -- Public API --

    /** Load the metadata bank (slot list). Call once at game startup. */
    UFUNCTION(BlueprintCallable, Category = "Save")
    void LoadMetadataBank();

    /** Get info for all slots without loading save payloads. */
    UFUNCTION(BlueprintCallable, Category = "Save")
    TArray<FSaveSlotInfo> GetAllSlotInfo() const;

    /** Async save to a slot. Fires OnSaveComplete when done. */
    UFUNCTION(BlueprintCallable, Category = "Save")
    void AsyncSaveToSlot(int32 SlotIndex);

    /** Async load from a slot. Fires OnLoadComplete when done. */
    UFUNCTION(BlueprintCallable, Category = "Save")
    void AsyncLoadFromSlot(int32 SlotIndex);

    /** Synchronous load — blocks game thread. Use only during initial boot. */
    UFUNCTION(BlueprintCallable, Category = "Save")
    bool SyncLoadFromSlot(int32 SlotIndex);

    /** Delete a save slot and clear its metadata entry. */
    UFUNCTION(BlueprintCallable, Category = "Save")
    void DeleteSlot(int32 SlotIndex);

    /** True if an async save is currently in flight. */
    UFUNCTION(BlueprintCallable, Category = "Save")
    bool IsSaveInProgress() const { return bSaveInProgress; }

    /** The currently active save data (loaded slot). */
    UFUNCTION(BlueprintCallable, Category = "Save")
    UMyGameSaveGame* GetCurrentSave() const { return CurrentSave; }

    // -- Events --
    UPROPERTY(BlueprintAssignable, Category = "Save")
    FOnSaveComplete OnSaveComplete;

    UPROPERTY(BlueprintAssignable, Category = "Save")
    FOnLoadComplete OnLoadComplete;

    // -- Auto-Save --
    UFUNCTION(BlueprintCallable, Category = "Save")
    void StartAutoSave(int32 SlotIndex, float IntervalSeconds = 300.f);

    UFUNCTION(BlueprintCallable, Category = "Save")
    void StopAutoSave();

private:
    static FString MakeSlotName(int32 SlotIndex);
    void PopulateSaveData(UMyGameSaveGame* Save);
    void ApplySaveData(UMyGameSaveGame* Save);
    void SaveMetadataBank();
    FSaveSlotInfo BuildSlotInfo(int32 SlotIndex, const UMyGameSaveGame* Save) const;

    // Callbacks
    UFUNCTION()
    void OnAsyncSaveComplete(const FString& SlotName, int32 UserIndex, bool bSuccess);
    UFUNCTION()
    void OnAsyncLoadComplete(const FString& SlotName, int32 UserIndex, USaveGame* SaveGame);

    UPROPERTY()
    USaveMetadataBank* MetadataBank = nullptr;

    UPROPERTY()
    UMyGameSaveGame* CurrentSave = nullptr;

    int32 ActiveSlotIndex = -1;
    bool  bSaveInProgress = false;

    FTimerHandle AutoSaveTimerHandle;
    int32 AutoSaveSlotIndex = 0;
};
```

```cpp
// SaveManager.cpp
#include "SaveManager.h"
#include "Kismet/GameplayStatics.h"
#include "Engine/World.h"
#include "TimerManager.h"

void USaveManager::Initialize(FSubsystemCollectionBase& Collection)
{
    Super::Initialize(Collection);
    LoadMetadataBank();
}

void USaveManager::Deinitialize()
{
    StopAutoSave();
    Super::Deinitialize();
}

FString USaveManager::MakeSlotName(int32 SlotIndex)
{
    return FString::Printf(TEXT("GameSave_%02d"), SlotIndex);
}

void USaveManager::LoadMetadataBank()
{
    if (UGameplayStatics::DoesSaveGameExist(USaveMetadataBank::SlotName,
                                            USaveMetadataBank::UserIndex))
    {
        MetadataBank = Cast<USaveMetadataBank>(
            UGameplayStatics::LoadGameFromSlot(
                USaveMetadataBank::SlotName, USaveMetadataBank::UserIndex));
    }

    if (!MetadataBank)
    {
        MetadataBank = Cast<USaveMetadataBank>(
            UGameplayStatics::CreateSaveGameObject(USaveMetadataBank::StaticClass()));
        MetadataBank->Init();
    }
}

TArray<FSaveSlotInfo> USaveManager::GetAllSlotInfo() const
{
    if (MetadataBank)
    {
        return MetadataBank->Slots;
    }
    return {};
}

void USaveManager::AsyncSaveToSlot(int32 SlotIndex)
{
    if (bSaveInProgress)
    {
        UE_LOG(LogTemp, Warning, TEXT("SaveManager: Save already in progress, ignoring request."));
        return;
    }

    if (!CurrentSave)
    {
        CurrentSave = Cast<UMyGameSaveGame>(
            UGameplayStatics::CreateSaveGameObject(UMyGameSaveGame::StaticClass()));
    }

    PopulateSaveData(CurrentSave);
    ActiveSlotIndex = SlotIndex;
    bSaveInProgress = true;

    FAsyncSaveGameToSlotDelegate Delegate;
    Delegate.BindUObject(this, &USaveManager::OnAsyncSaveComplete);
    UGameplayStatics::AsyncSaveGameToSlot(
        CurrentSave, MakeSlotName(SlotIndex), USaveMetadataBank::UserIndex, Delegate);
}

void USaveManager::OnAsyncSaveComplete(
    const FString& SlotName, int32 UserIndex, bool bSuccess)
{
    bSaveInProgress = false;

    if (bSuccess && MetadataBank)
    {
        FSaveSlotInfo Info = BuildSlotInfo(ActiveSlotIndex, CurrentSave);
        MetadataBank->UpdateSlot(ActiveSlotIndex, Info);
        SaveMetadataBank();
    }

    OnSaveComplete.Broadcast(ActiveSlotIndex, bSuccess);

    if (!bSuccess)
    {
        UE_LOG(LogTemp, Error, TEXT("SaveManager: Async save failed for slot %d"), ActiveSlotIndex);
    }
}

void USaveManager::AsyncLoadFromSlot(int32 SlotIndex)
{
    ActiveSlotIndex = SlotIndex;

    FAsyncLoadGameFromSlotDelegate Delegate;
    Delegate.BindUObject(this, &USaveManager::OnAsyncLoadComplete);
    UGameplayStatics::AsyncLoadGameFromSlot(
        MakeSlotName(SlotIndex), USaveMetadataBank::UserIndex, Delegate);
}

void USaveManager::OnAsyncLoadComplete(
    const FString& SlotName, int32 UserIndex, USaveGame* SaveGame)
{
    CurrentSave = Cast<UMyGameSaveGame>(SaveGame);

    if (!CurrentSave)
    {
        UE_LOG(LogTemp, Warning,
               TEXT("SaveManager: Load failed or no file for slot %d; using fresh save."),
               ActiveSlotIndex);
        CurrentSave = Cast<UMyGameSaveGame>(
            UGameplayStatics::CreateSaveGameObject(UMyGameSaveGame::StaticClass()));
    }

    RunMigrations(CurrentSave);
    ApplySaveData(CurrentSave);

    OnLoadComplete.Broadcast(ActiveSlotIndex, SaveGame != nullptr);
}

bool USaveManager::SyncLoadFromSlot(int32 SlotIndex)
{
    // Use only at startup before the first frame renders
    USaveGame* Loaded = UGameplayStatics::LoadGameFromSlot(
        MakeSlotName(SlotIndex), USaveMetadataBank::UserIndex);

    CurrentSave = Cast<UMyGameSaveGame>(Loaded);
    if (!CurrentSave)
    {
        CurrentSave = Cast<UMyGameSaveGame>(
            UGameplayStatics::CreateSaveGameObject(UMyGameSaveGame::StaticClass()));
        return false;
    }

    RunMigrations(CurrentSave);
    ApplySaveData(CurrentSave);
    ActiveSlotIndex = SlotIndex;
    return true;
}

void USaveManager::DeleteSlot(int32 SlotIndex)
{
    UGameplayStatics::DeleteGameInSlot(MakeSlotName(SlotIndex), USaveMetadataBank::UserIndex);

    if (MetadataBank)
    {
        MetadataBank->ClearSlot(SlotIndex);
        SaveMetadataBank();
    }
}

void USaveManager::SaveMetadataBank()
{
    UGameplayStatics::SaveGameToSlot(
        MetadataBank, USaveMetadataBank::SlotName, USaveMetadataBank::UserIndex);
}

FSaveSlotInfo USaveManager::BuildSlotInfo(int32 SlotIndex, const UMyGameSaveGame* Save) const
{
    FSaveSlotInfo Info;
    Info.SlotIndex   = SlotIndex;
    Info.bIsValid    = true;
    Info.LastSaveTime = FDateTime::Now();

    if (Save)
    {
        Info.PlayerDisplayName    = Save->PlayerDisplayName;
        Info.PlayerLevel          = Save->PlayerLevel;
        Info.TotalPlayTimeSeconds = Save->TotalPlayTimeSeconds;
        // MapName from world:
        if (UWorld* World = GetGameInstance() ? GetGameInstance()->GetWorld() : nullptr)
        {
            Info.MapName = World->GetMapName();
        }
    }

    return Info;
}

void USaveManager::StartAutoSave(int32 SlotIndex, float IntervalSeconds)
{
    AutoSaveSlotIndex = SlotIndex;
    if (UWorld* World = GetGameInstance()->GetWorld())
    {
        World->GetTimerManager().SetTimer(
            AutoSaveTimerHandle,
            FTimerDelegate::CreateUObject(this, &USaveManager::AsyncSaveToSlot, SlotIndex),
            IntervalSeconds,
            /*bLoop=*/true);
    }
}

void USaveManager::StopAutoSave()
{
    if (UWorld* World = GetGameInstance() ? GetGameInstance()->GetWorld() : nullptr)
    {
        World->GetTimerManager().ClearTimer(AutoSaveTimerHandle);
    }
}
```

---

## 3. Migration Pipeline

Centralize all migration logic so it runs consistently on every load path (sync and async):

```cpp
// Add to SaveManager or to UMyGameSaveGame

// Version constants
namespace ESaveVersion
{
    enum Type : int32
    {
        Initial               = 0,
        AddedInventory        = 1,
        AddedAbilitySaveData  = 2,
        AddedPlayTime         = 3,
        SoftRefForWeapon      = 4,

        VersionPlusOne,
        Latest = VersionPlusOne - 1
    };
}

void USaveManager::RunMigrations(UMyGameSaveGame* Save)
{
    if (!Save) { return; }

    const int32 LoadedVersion = Save->SaveVersion;

    if (LoadedVersion == ESaveVersion::Latest)
    {
        return; // Already up to date, fast path
    }

    UE_LOG(LogTemp, Log, TEXT("Migrating save from version %d to %d"),
           LoadedVersion, (int32)ESaveVersion::Latest);

    if (LoadedVersion < ESaveVersion::AddedInventory)
    {
        // No inventory existed; leave InventoryItems empty (already default)
    }

    if (LoadedVersion < ESaveVersion::AddedAbilitySaveData)
    {
        // Ability data didn't exist; initialize defaults
        Save->SavedAbilities.Reset();
    }

    if (LoadedVersion < ESaveVersion::AddedPlayTime)
    {
        // Can't recover old play time; set to 0
        Save->TotalPlayTimeSeconds = 0.f;
    }

    if (LoadedVersion < ESaveVersion::SoftRefForWeapon)
    {
        // Old save used a FName; new format uses FSoftObjectPath.
        // If OldWeaponID_Deprecated was populated, convert it.
        // Save->LastEquippedWeaponPath = ResolveWeaponIDToPath(Save->OldWeaponID_Deprecated);
    }

    // Stamp new version
    Save->SaveVersion = ESaveVersion::Latest;
}
```

---

## 4. Binary Blob Pattern (FArchive Inside USaveGame)

For complex subsystem data that warrants manual layout control, store it as `TArray<uint8>` inside the `USaveGame` and serialize/deserialize with `FMemoryWriter`/`FMemoryReader`:

```cpp
// In UMyGameSaveGame:
UPROPERTY(SaveGame)
TArray<uint8> QuestSystemBlob;  // Manually serialized binary payload

// In your quest subsystem:
bool UQuestSubsystem::SerializeToBlob(TArray<uint8>& OutBlob) const
{
    FMemoryWriter Writer(OutBlob, /*bIsPersistent=*/true);

    int32 BlobVersion = 2;
    Writer << BlobVersion;

    int32 NumActiveQuests = ActiveQuests.Num();
    Writer << NumActiveQuests;

    for (const FQuestState& Quest : ActiveQuests)
    {
        FName QID = Quest.QuestID;
        int32 Stage = Quest.CurrentStage;
        Writer << QID;
        Writer << Stage;
    }

    return !Writer.IsError();
}

bool UQuestSubsystem::DeserializeFromBlob(const TArray<uint8>& Blob)
{
    if (Blob.IsEmpty()) { return true; } // No quest data saved yet

    FMemoryReader Reader(Blob, /*bIsPersistent=*/true);

    int32 BlobVersion = 0;
    Reader << BlobVersion;

    if (BlobVersion < 1 || Reader.IsError())
    {
        UE_LOG(LogTemp, Error, TEXT("QuestSubsystem: Invalid blob version %d"), BlobVersion);
        return false;
    }

    int32 NumQuests = 0;
    Reader << NumQuests;

    ActiveQuests.Empty(NumQuests);

    for (int32 i = 0; i < NumQuests; ++i)
    {
        FName QID;
        int32 Stage;
        Reader << QID;
        Reader << Stage;

        if (Reader.IsError()) { return false; }

        FQuestState& Q = ActiveQuests.AddDefaulted_GetRef();
        Q.QuestID      = QID;
        Q.CurrentStage = Stage;
    }

    return !Reader.IsError();
}
```

---

## 5. Multi-User (Local Multiplayer) Pattern

Each local player gets their own save slot. Use `ULocalPlayerSaveGame` and pass the `ULocalPlayer` or `APlayerController`.

```cpp
// In your player controller or local player subsystem:
void AMyPlayerController::SavePlayerData()
{
    if (!LocalPlayerSave)
    {
        UE_LOG(LogTemp, Warning, TEXT("No local player save — was it loaded?"));
        return;
    }

    // Populate
    LocalPlayerSave->AbilityLevels.Empty();
    for (auto& [AbilityName, Level] : AbilityComponent->GetAllLevels())
    {
        LocalPlayerSave->AbilityLevels.Add(AbilityName, Level);
    }

    // Async save — hooks HandlePostSave for result
    LocalPlayerSave->AsyncSaveGameToSlotForLocalPlayer();
}

void AMyPlayerController::LoadPlayerData()
{
    // Async load or create a fresh save if none exists
    bool bScheduled = ULocalPlayerSaveGame::AsyncLoadOrCreateSaveGameForLocalPlayer(
        UMyLocalPlayerSave::StaticClass(),
        this, // APlayerController* LocalPlayerController
        TEXT("PlayerData"),
        FOnLocalPlayerSaveGameLoadedNative::CreateUObject(
            this, &AMyPlayerController::OnPlayerDataLoaded));

    if (!bScheduled)
    {
        UE_LOG(LogTemp, Error, TEXT("Failed to schedule async load for local player save."));
    }
}

void AMyPlayerController::OnPlayerDataLoaded(ULocalPlayerSaveGame* SaveGame)
{
    LocalPlayerSave = Cast<UMyLocalPlayerSave>(SaveGame);
    if (!LocalPlayerSave)
    {
        UE_LOG(LogTemp, Error, TEXT("LocalPlayerSave cast failed after load."));
        return;
    }

    // Apply
    for (auto& [AbilityName, Level] : LocalPlayerSave->AbilityLevels)
    {
        AbilityComponent->SetAbilityLevel(AbilityName, Level);
    }
}
```

For the save slot name per player, derive it from the player index or platform user ID so each user has isolated data:

```cpp
FString GetPlayerSlotName(const APlayerController* PC)
{
    if (!PC) { return TEXT("PlayerData_0"); }
    if (const ULocalPlayer* LP = PC->GetLocalPlayer())
    {
        return FString::Printf(TEXT("PlayerData_%d"), LP->GetControllerId());
    }
    return TEXT("PlayerData_0");
}
```

---

## 6. Platform Considerations

| Platform | Key Difference |
|---|---|
| PC / Mac | `UGameplayStatics` writes to `Saved/SaveGames/`. No user index required in most cases. |
| Console (PS5, Xbox) | User index maps to a controller/account. Always use `GetPlatformUserIndex()` from `ULocalPlayerSaveGame`. |
| Mobile (iOS, Android) | Save path is app-specific sandbox; `UGameplayStatics` handles it. Watch for size limits. |
| PIE | Saves go to the project's `Saved/SaveGames/`. Clean between test runs with `DeleteGameInSlot`. |

To get the platform user index correctly:

```cpp
int32 GetUserIndex(const APlayerController* PC)
{
    if (const ULocalPlayer* LP = PC ? PC->GetLocalPlayer() : nullptr)
    {
        return LP->GetPlatformUserIndex(); // returns int32 directly
    }
    return 0;
}
```

---

## 7. Save File Path Reference (Debug Only)

Never rely on these paths in shipping code. They are useful for wiping saves in automation tests or editor utilities:

```cpp
FString GetSaveGamePath(const FString& SlotName, int32 UserIndex)
{
    // Only valid on PC / development. Do not use in shipping builds.
    ISaveGameSystem* SaveSystem = IPlatformFeaturesModule::Get().GetSaveGameSystem();
    // ISaveGameSystem does not expose paths directly; use FPaths for debug only:
    return FPaths::ProjectSavedDir()
        / TEXT("SaveGames")
        / FString::Printf(TEXT("%s.sav"), *SlotName);
}
```

---

## 8. Save System Registration in GameInstance

Register the save manager and trigger initial metadata load in `UGameInstance::Init()`:

```cpp
// MyGameInstance.cpp
void UMyGameInstance::Init()
{
    Super::Init();
    // Subsystem is created automatically; access it via GetSubsystem<>
    // No manual construction needed.
}

// In any game code:
USaveManager* SM = GetGameInstance()->GetSubsystem<USaveManager>();
SM->AsyncSaveToSlot(0);
```

Because `USaveManager` is a `UGameInstanceSubsystem`, UE creates it automatically when the `GameInstance` initializes. `Initialize()` on the subsystem fires before the first level loads, making it the correct place to load the metadata bank.
