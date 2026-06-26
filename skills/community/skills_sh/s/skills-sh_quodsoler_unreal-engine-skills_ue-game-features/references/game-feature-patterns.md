# Game Feature Patterns Reference

Complete code templates for Game Feature plugin setup, custom actions, and component injection.

---

## GameFeature .uplugin Template

```json
{
    "FileVersion": 3,
    "Version": 1,
    "VersionName": "1.0",
    "FriendlyName": "My Feature",
    "Description": "Adds my gameplay feature",
    "Category": "Game Features",
    "CreatedBy": "",
    "CreatedByURL": "",
    "DocsURL": "",
    "MarketplaceURL": "",
    "CanContainContent": true,
    "Installed": false,
    "ExplicitlyLoaded": true,
    "Type": "GameFeature",
    "BuiltInInitialFeatureState": "Active",
    "Plugins": [
        { "Name": "GameFeatures", "Enabled": true },
        { "Name": "ModularGameplay", "Enabled": true }
    ]
}
```

`BuiltInInitialFeatureState` options: `"Installed"` (on disk, not registered), `"Registered"` (registered with Asset Manager, activated by code), `"Active"` (fully active on startup).

---

## Custom UGameFeatureAction Subclass

```cpp
// MyGameFeatureAction_SpawnManagers.h
#pragma once
#include "GameFeatureAction.h"
#include "GameFeaturesSubsystem.h"
#include "MyGameFeatureAction_SpawnManagers.generated.h"

UCLASS(MinimalAPI, meta = (DisplayName = "Spawn Managers"))
class UMyGameFeatureAction_SpawnManagers : public UGameFeatureAction
{
    GENERATED_BODY()

public:
    virtual void OnGameFeatureActivating(FGameFeatureActivatingContext& Context) override;
    virtual void OnGameFeatureDeactivating(FGameFeatureDeactivatingContext& Context) override;

private:
    void AddToWorld(const FWorldContext& WorldContext);
    void HandleGameInstanceStart(UGameInstance* GameInstance);

    // Per-world tracking for PIE support
    TMap<FObjectKey, TArray<TWeakObjectPtr<AActor>>> SpawnedActorsPerWorld;

    UPROPERTY(EditAnywhere, Category = "Spawn")
    TSubclassOf<AActor> ManagerClass;
};
```

```cpp
// MyGameFeatureAction_SpawnManagers.cpp
#include "MyGameFeatureAction_SpawnManagers.h"
#include "Engine/GameInstance.h"
#include "Engine/World.h"

void UMyGameFeatureAction_SpawnManagers::OnGameFeatureActivating(
    FGameFeatureActivatingContext& Context)
{
    // Handle worlds already running (hot-activation)
    for (const FWorldContext& WorldContext : GEngine->GetWorldContexts())
    {
        if (Context.ShouldApplyToWorldContext(WorldContext))
        {
            AddToWorld(WorldContext);
        }
    }
    // Handle worlds created after activation (new PIE sessions, travel)
    FWorldDelegates::OnStartGameInstance.AddUObject(
        this, &UMyGameFeatureAction_SpawnManagers::HandleGameInstanceStart);
}

void UMyGameFeatureAction_SpawnManagers::OnGameFeatureDeactivating(
    FGameFeatureDeactivatingContext& Context)
{
    FWorldDelegates::OnStartGameInstance.RemoveAll(this);

    for (auto& [WorldKey, ActorArray] : SpawnedActorsPerWorld)
    {
        for (TWeakObjectPtr<AActor>& ActorPtr : ActorArray)
        {
            if (AActor* Actor = ActorPtr.Get())
            {
                Actor->Destroy();
            }
        }
    }
    SpawnedActorsPerWorld.Empty();
}

void UMyGameFeatureAction_SpawnManagers::AddToWorld(const FWorldContext& WorldContext)
{
    UWorld* World = WorldContext.World();
    if (!World || !World->IsGameWorld() || !ManagerClass)
    {
        return;
    }

    FActorSpawnParameters SpawnParams;
    SpawnParams.SpawnCollisionHandlingOverride = ESpawnActorCollisionHandlingMethod::AlwaysSpawn;
    AActor* Spawned = World->SpawnActor<AActor>(ManagerClass, FTransform::Identity, SpawnParams);
    if (Spawned)
    {
        SpawnedActorsPerWorld.FindOrAdd(FObjectKey(World)).Add(Spawned);
    }
}

void UMyGameFeatureAction_SpawnManagers::HandleGameInstanceStart(UGameInstance* GameInstance)
{
    if (UWorld* World = GameInstance->GetWorld())
    {
        for (const FWorldContext& WC : GEngine->GetWorldContexts())
        {
            if (WC.World() == World) { AddToWorld(WC); break; }
        }
    }
}
```

**Key pattern:** Iterate `GEngine->GetWorldContexts()` and check `Context.ShouldApplyToWorldContext()` to support PIE with multiple worlds. Store per-world state with `FObjectKey` as map key.

---

## Actor Receiver Setup

```cpp
// MyModularCharacter.h — registers for component injection
#include "GameFrameworkComponentManager.h"

void AMyModularCharacter::BeginPlay()
{
    Super::BeginPlay();
    UGameFrameworkComponentManager::AddGameFrameworkComponentReceiver(this);
}

void AMyModularCharacter::EndPlay(const EEndPlayReason::Type EndPlayReason)
{
    UGameFrameworkComponentManager::RemoveGameFrameworkComponentReceiver(this);
    Super::EndPlay(EndPlayReason);
}
```

Call `RemoveGameFrameworkComponentReceiver` before `Super::EndPlay` to ensure cleanup occurs while the actor is still valid.

---

## Extension Handler Registration

```cpp
// In a custom UGameFeatureAction or subsystem
void UMyAction::OnGameFeatureActivating(FGameFeatureActivatingContext& Context)
{
    UGameFrameworkComponentManager* CompMgr =
        UGameInstance::GetSubsystem<UGameFrameworkComponentManager>(
            /* get game instance from world context */);

    ExtensionHandle = CompMgr->AddExtensionHandler(
        TSoftClassPtr<AActor>(AMyCharacter::StaticClass()),
        FExtensionHandlerDelegate::CreateUObject(
            this, &UMyAction::OnActorExtension));
}

void UMyAction::OnActorExtension(AActor* Actor, FName EventName)
{
    if (EventName == UGameFrameworkComponentManager::NAME_ReceiverAdded)
    {
        // Actor just registered — configure initial state
    }
    else if (EventName == UGameFrameworkComponentManager::NAME_GameActorReady)
    {
        // All init states complete — safe to use all components
    }
    else if (EventName == UGameFrameworkComponentManager::NAME_ReceiverRemoved)
    {
        // Actor unregistering — clean up references
    }
}

void UMyAction::OnGameFeatureDeactivating(FGameFeatureDeactivatingContext& Context)
{
    // RAII: dropping the handle removes the extension
    ExtensionHandle.Reset();
}

// Member variable — RAII handle
TSharedPtr<FComponentRequestHandle> ExtensionHandle;
```

---

## FComponentRequestHandle RAII Lifecycle

```cpp
// Store handles as member variables for lifetime management
// Note: TSharedPtr is not supported by UE reflection — no UPROPERTY() here
TArray<TSharedPtr<FComponentRequestHandle>> ComponentRequests;

void UMyAction::OnGameFeatureActivating(FGameFeatureActivatingContext& Context)
{
    UGameFrameworkComponentManager* CompMgr = /* ... */;

    // Each request returns a shared handle — RAII removes on destruction
    ComponentRequests.Add(CompMgr->AddComponentRequest(
        TSoftClassPtr<AActor>(AMyCharacter::StaticClass()),
        UMyHealthComponent::StaticClass(),
        EGameFrameworkAddComponentFlags::AddUnique));

    ComponentRequests.Add(CompMgr->AddComponentRequest(
        TSoftClassPtr<AActor>(AMyCharacter::StaticClass()),
        UMyInventoryComponent::StaticClass(),
        EGameFrameworkAddComponentFlags::AddUnique));
}

void UMyAction::OnGameFeatureDeactivating(FGameFeatureDeactivatingContext& Context)
{
    // Empty the array — shared pointers destruct — components removed automatically
    ComponentRequests.Empty();
}
```

---

## Custom Action with Async Deactivation

```cpp
UCLASS(MinimalAPI, meta = (DisplayName = "Save Progress On Deactivate"))
class UMyAction_SaveProgress : public UGameFeatureAction
{
    GENERATED_BODY()
public:
    virtual void OnGameFeatureDeactivating(
        FGameFeatureDeactivatingContext& Context) override
    {
        // Pause deactivation — returns FSimpleDelegate that MUST be invoked
        FSimpleDelegate Resume = Context.PauseDeactivationUntilComplete(
            TEXT("SaveProgress"));

        // Start async save
        UGameplayStatics::AsyncSaveGameToSlot(
            SaveGameObject, TEXT("AutoSave"), 0,
            FAsyncSaveGameToSlotDelegate::CreateLambda(
                [Resume](const FString&, const int32, bool bSuccess)
                {
                    UE_LOG(LogTemp, Log, TEXT("Save %s"),
                        bSuccess ? TEXT("succeeded") : TEXT("failed"));
                    Resume.ExecuteIfBound();  // Resume deactivation
                }));
    }

private:
    UPROPERTY()
    TObjectPtr<USaveGame> SaveGameObject;
};
```

**Critical:** Always invoke the resume delegate, even on error paths. If the async operation can fail silently (timeout, crash), wrap with a safety timer.

---

## Project Policies Subclass

```cpp
UCLASS()
class UMyProjectPolicies : public UGameFeaturesProjectPolicies
{
    GENERATED_BODY()
public:
    virtual bool IsPluginAllowed(const FString& PluginURL, FString* OutReason) const override
    {
        // Block specific features in shipping builds
        if (PluginURL.Contains(TEXT("DebugTools")))
        {
            if (OutReason) { *OutReason = TEXT("Debug tools disabled in shipping"); }
            return false;
        }
        return true;
    }

    virtual void GetGameFeatureLoadingMode(
        bool& bLoadClientData, bool& bLoadServerData) const override
    {
        bLoadClientData = !IsRunningDedicatedServer();
        bLoadServerData = true;
    }
};
```

Register in `DefaultGame.ini`:
```ini
[/Script/GameFeatures.GameFeaturesSubsystemSettings]
GameFeaturesManagerClassName=/Script/MyProject.UMyProjectPolicies
```
