# Experience System Reference

The experience system pattern (pioneered by Lyra) composes game modes from multiple Game Feature
plugins at runtime. Instead of a monolithic `AGameMode` subclass per game type, you define
lightweight data assets that list which features to activate.

---

## Experience Definition Asset

```cpp
// UExperienceDefinition — a primary data asset listing features to compose
#pragma once
#include "Engine/DataAsset.h"
#include "ExperienceDefinition.generated.h"

UCLASS()
class UExperienceDefinition : public UPrimaryDataAsset
{
    GENERATED_BODY()
public:
    // Game Feature plugins to activate for this experience
    UPROPERTY(EditDefaultsOnly, Category = "Experience")
    TArray<FString> GameFeaturesToEnable;

    // Actions to execute directly (without a full Game Feature plugin)
    UPROPERTY(EditDefaultsOnly, Instanced, Category = "Experience")
    TArray<TObjectPtr<UGameFeatureAction>> Actions;

    // Default pawn data for this experience
    UPROPERTY(EditDefaultsOnly, Category = "Experience")
    TObjectPtr<UPawnData> DefaultPawnData;

    virtual FPrimaryAssetId GetPrimaryAssetId() const override
    {
        return FPrimaryAssetId(FPrimaryAssetType("Experience"),
            GetFName());
    }
};
```

Example experience assets:
- **B_Deathmatch**: Enables `ShooterCore` + `DeathmatchRules`
- **B_ControlPoint**: Enables `ShooterCore` + `ControlPointRules`
- **B_FrontEnd**: Enables `FrontEndUI` only (no gameplay features)

Each experience shares common features (e.g., `ShooterCore` for weapons, health, HUD) and
adds mode-specific rules as separate Game Feature plugins.

---

## Experience Manager Component

A `UGameStateComponent` on `AGameStateBase` orchestrates experience loading:

```cpp
#pragma once
#include "Components/GameStateComponent.h"
#include "ExperienceManagerComponent.generated.h"

DECLARE_MULTICAST_DELEGATE_OneParam(FOnExperienceLoaded, const UExperienceDefinition*);

UCLASS()
class UExperienceManagerComponent : public UGameStateComponent
{
    GENERATED_BODY()
public:
    // Call from GameMode::InitGame to start loading
    void SetCurrentExperience(FPrimaryAssetId ExperienceId);

    // Check if experience is fully loaded and active
    bool IsExperienceLoaded() const { return bExperienceLoaded; }

    // Bind to get notified when experience is ready — fires immediately if already loaded
    void CallOrRegister_OnExperienceLoaded(FOnExperienceLoaded::FDelegate&& Delegate);

    const UExperienceDefinition* GetCurrentExperience() const { return CurrentExperience; }

    FOnExperienceLoaded OnExperienceLoaded;

private:
    void OnExperienceLoadComplete();
    void OnGameFeaturePluginLoadComplete(const UE::GameFeatures::FResult& Result);

    UPROPERTY()
    TObjectPtr<const UExperienceDefinition> CurrentExperience;

    int32 NumGameFeaturePluginsLoading = 0;
    bool bExperienceLoaded = false;
};
```

---

## Experience Loading Flow

```cpp
// 1. GameMode selects and starts loading the experience
void AMyGameMode::InitGame(const FString& MapName, const FString& Options,
    FString& ErrorMessage)
{
    Super::InitGame(MapName, Options, ErrorMessage);

    // Determine experience from map, URL options, or default
    FPrimaryAssetId ExperienceId = FPrimaryAssetId(
        FPrimaryAssetType("Experience"), FName("B_Deathmatch"));

    // Get the experience manager on GameState
    UExperienceManagerComponent* ExpMgr =
        GameState->FindComponentByClass<UExperienceManagerComponent>();
    ExpMgr->SetCurrentExperience(ExperienceId);
}

// 2. ExperienceManagerComponent loads the definition, then activates features
void UExperienceManagerComponent::SetCurrentExperience(FPrimaryAssetId ExperienceId)
{
    // Async load the experience data asset
    UAssetManager::Get().LoadPrimaryAsset(ExperienceId,
        TArray<FName>(),
        FStreamableDelegate::CreateUObject(this,
            &UExperienceManagerComponent::OnExperienceLoadComplete));
}

void UExperienceManagerComponent::OnExperienceLoadComplete()
{
    // Asset loaded — now activate each Game Feature plugin
    CurrentExperience = Cast<UExperienceDefinition>(
        UAssetManager::Get().GetPrimaryAssetObject(ExperienceId));

    UGameFeaturesSubsystem& GFS = UGameFeaturesSubsystem::Get();
    NumGameFeaturePluginsLoading = CurrentExperience->GameFeaturesToEnable.Num();

    for (const FString& PluginURL : CurrentExperience->GameFeaturesToEnable)
    {
        GFS.LoadAndActivateGameFeaturePlugin(PluginURL,
            FGameFeaturePluginLoadComplete::CreateUObject(
                this, &UExperienceManagerComponent::OnGameFeaturePluginLoadComplete));
    }

    // If no plugins to load, mark ready immediately
    if (NumGameFeaturePluginsLoading == 0)
    {
        bExperienceLoaded = true;
        OnExperienceLoaded.Broadcast(CurrentExperience);
    }
}

void UExperienceManagerComponent::OnGameFeaturePluginLoadComplete(
    const UE::GameFeatures::FResult& Result)
{
    NumGameFeaturePluginsLoading--;
    if (NumGameFeaturePluginsLoading == 0)
    {
        bExperienceLoaded = true;
        OnExperienceLoaded.Broadcast(CurrentExperience);
    }
}

// 3. CallOrRegister pattern — fires immediately if already loaded
void UExperienceManagerComponent::CallOrRegister_OnExperienceLoaded(
    FOnExperienceLoaded::FDelegate&& Delegate)
{
    if (bExperienceLoaded)
    {
        Delegate.Execute(CurrentExperience);
    }
    else
    {
        OnExperienceLoaded.Add(MoveTemp(Delegate));
    }
}
```

---

## Consuming the Experience

Systems that depend on the experience being ready use `CallOrRegister_OnExperienceLoaded`
instead of assuming features are available at `BeginPlay`:

```cpp
void UMyPawnComponent::BeginPlay()
{
    Super::BeginPlay();

    AGameStateBase* GS = GetWorld()->GetGameState<AGameStateBase>();
    if (UExperienceManagerComponent* ExpMgr =
        GS->FindComponentByClass<UExperienceManagerComponent>())
    {
        ExpMgr->CallOrRegister_OnExperienceLoaded(
            FOnExperienceLoaded::FDelegate::CreateUObject(
                this, &UMyPawnComponent::OnExperienceReady));
    }
}

void UMyPawnComponent::OnExperienceReady(const UExperienceDefinition* Experience)
{
    // All features active — safe to look up injected components, configure abilities, etc.
    // Experience->DefaultPawnData contains pawn configuration for this mode
}
```

---

## Feature Composition Example

A Deathmatch experience composed from modular features:

```
B_Deathmatch (UExperienceDefinition)
├── GameFeaturesToEnable:
│   ├── "ShooterCore"        → Health, weapons, HUD, hit detection
│   ├── "DeathmatchRules"    → Score tracking, kill feed, respawn timer
│   └── "TeamSystem"         → Team assignment, team colors, team HUD
├── Actions:
│   └── AddComponents: DeathmatchScoreComponent → AGameState
└── DefaultPawnData: BP_ShooterCharacter
```

Switching to Control Point mode replaces `DeathmatchRules` with `ControlPointRules` while
keeping `ShooterCore` and `TeamSystem`. This avoids duplicating shared gameplay code and
allows features to be developed and tested independently.
