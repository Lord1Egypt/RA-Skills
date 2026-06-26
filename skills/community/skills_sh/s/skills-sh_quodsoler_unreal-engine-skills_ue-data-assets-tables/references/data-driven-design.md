# Data-Driven Design in Unreal Engine

Patterns for structuring game data using `UDataAsset`, `UPrimaryDataAsset`, and `UDataTable` so designers control gameplay values without C++ changes.

---

## Core Principle

Data-driven design separates **what** (values, configurations, relationships) from **how** (C++ logic). C++ defines the schema; designers populate instances in the editor or spreadsheets.

| Layer | Owner | Tool |
|---|---|---|
| Data schema | Programmer | C++ `USTRUCT` / `UCLASS` |
| Data values | Designer | Data Asset editor, CSV/JSON |
| Data loading | Programmer | Asset Manager, soft refs |
| Data consumption | Programmer | `FindRow`, `GetPrimaryAssetObject` |

---

## Pattern A: Item / Ability Definitions (UPrimaryDataAsset)

Best when each item has unique properties, may need Blueprint extension, and should integrate with the Asset Manager for selective loading.

### Schema

```cpp
// ItemDefinition.h
#pragma once
#include "Engine/DataAsset.h"
#include "GameplayTagContainer.h"
#include "ItemDefinition.generated.h"

UENUM(BlueprintType)
enum class EItemRarity : uint8
{
    Common,
    Uncommon,
    Rare,
    Legendary
};

UCLASS(BlueprintType)
class MYGAME_API UItemDefinition : public UPrimaryDataAsset
{
    GENERATED_BODY()
public:
    // Identity
    UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Item")
    FText DisplayName;

    UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Item")
    FText Description;

    UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Item")
    EItemRarity Rarity = EItemRarity::Common;

    UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Item",
              AssetRegistrySearchable)
    FGameplayTagContainer ItemTags;

    // Stats
    UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Stats")
    float BaseDamage = 0.f;

    UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Stats")
    int32 MaxStack = 1;

    // UI bundle: loaded in inventory screen.
    UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Art",
              meta = (AssetBundles = "UI"))
    TSoftObjectPtr<UTexture2D> Icon;

    // Game bundle: loaded in the world.
    UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Art",
              meta = (AssetBundles = "Game"))
    TSoftObjectPtr<UStaticMesh> WorldMesh;

    UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Spawning",
              meta = (AssetBundles = "Game"))
    TSoftClassPtr<AActor> DroppedActorClass;
};
```

### DefaultGame.ini Registration

```ini
[/Script/Engine.AssetManagerSettings]
+PrimaryAssetTypesToScan=(
    PrimaryAssetType="ItemDefinition",
    AssetBaseClass=/Script/MyGame.ItemDefinition,
    bHasBlueprintClasses=False,
    bIsEditorOnly=False,
    Directories=((Path="/Game/Data/Items")),
    Rules=(Priority=1,ChunkId=-1,bApplyRecursively=True,CookRule=AlwaysCook))
```

### Discovery and Loading

```cpp
// Get all item IDs (no assets loaded yet).
TArray<FPrimaryAssetId> AllItemIds;
UAssetManager::Get().GetPrimaryAssetIdList(
    FPrimaryAssetType(TEXT("ItemDefinition")), AllItemIds);

// Filter by tag using Asset Registry (no load).
IAssetRegistry& AR = IAssetRegistry::GetChecked();
TArray<FAssetData> MeleeAssets;
AR.GetAssetsByClass(
    FTopLevelAssetPath(TEXT("/Script/MyGame"), TEXT("ItemDefinition")),
    MeleeAssets, true);

// Load UI bundle for inventory.
UAssetManager::Get().LoadPrimaryAssetsWithType(
    FPrimaryAssetType(TEXT("ItemDefinition")),
    { TEXT("UI") });

// After callback: retrieve a specific item.
FPrimaryAssetId SwordId(TEXT("ItemDefinition"), TEXT("DA_Sword"));
UItemDefinition* Sword =
    UAssetManager::Get().GetPrimaryAssetObject<UItemDefinition>(SwordId);
```

---

## Pattern B: Stat Tables (UDataTable)

Best for large, flat, designer-authored datasets where all rows share the same shape: XP curves, damage falloff, NPC dialogue, loot drop weights.

### Row Struct

```cpp
// XPTableRow.h
#pragma once
#include "Engine/DataTable.h"
#include "XPTableRow.generated.h"

USTRUCT(BlueprintType)
struct FXPTableRow : public FTableRowBase
{
    GENERATED_BODY()

    /** Player level. Also used as the row name in the DataTable. */
    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    int32 Level = 1;

    /** XP required to reach this level from the previous one. */
    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    int32 XPRequired = 0;

    /** Stat multiplier applied at this level. */
    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    float StatMultiplier = 1.f;

    // Validate row after import.
    virtual void OnPostDataImport(const UDataTable* InDataTable,
                                  const FName InRowName,
                                  TArray<FString>& OutCollectedImportProblems) override
    {
        if (XPRequired < 0)
        {
            OutCollectedImportProblems.Add(
                FString::Printf(TEXT("Row '%s': XPRequired cannot be negative."),
                                *InRowName.ToString()));
        }
    }
};
```

### CSV Format

```csv
---,Level,XPRequired,StatMultiplier
Level_1,1,0,1.0
Level_2,2,100,1.05
Level_3,3,250,1.10
Level_4,4,500,1.15
```

The first column (`---` or `Name`) is the row name. Import via: DataTable asset > Import > select CSV.

### Runtime Lookup

```cpp
// Stored as a hard reference because it is small and always needed.
UPROPERTY(EditDefaultsOnly, Category = "Data")
TObjectPtr<UDataTable> XPTable;

FXPTableRow* ULevelingComponent::GetRowForLevel(int32 Level) const
{
    if (!XPTable) { return nullptr; }
    FName RowName = FName(*FString::Printf(TEXT("Level_%d"), Level));
    return XPTable->FindRow<FXPTableRow>(RowName, TEXT("GetRowForLevel"));
}

int32 ULevelingComponent::GetXPToNextLevel(int32 CurrentLevel) const
{
    const FXPTableRow* Row = GetRowForLevel(CurrentLevel + 1);
    return Row ? Row->XPRequired : 0;
}
```

---

## Pattern C: Config Objects (UDataAsset — Not Primary)

Use plain `UDataAsset` (not Primary) for global configuration that is always loaded with the referencing class, is not addressable by ID, and does not need Asset Manager integration.

```cpp
// GameBalanceConfig.h
#pragma once
#include "Engine/DataAsset.h"
#include "GameBalanceConfig.generated.h"

UCLASS(BlueprintType)
class MYGAME_API UGameBalanceConfig : public UDataAsset
{
    GENERATED_BODY()
public:
    UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Economy")
    int32 StartingGold = 100;

    UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Economy")
    float SellPriceMultiplier = 0.5f;

    UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Combat")
    float GlobalDamageScale = 1.f;

    UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Combat")
    float CritMultiplier = 2.f;
};
```

Reference from GameMode or GameInstance with a hard `TObjectPtr`:

```cpp
UPROPERTY(EditDefaultsOnly, Category = "Config")
TObjectPtr<UGameBalanceConfig> BalanceConfig;
```

---

## Pattern D: Hybrid — DataAsset with DataTable Reference

An item definition holds a soft reference to a DataTable for per-tier stat scaling, while the DataAsset handles identity and art.

```cpp
UCLASS(BlueprintType)
class MYGAME_API UWeaponDefinition : public UPrimaryDataAsset
{
    GENERATED_BODY()
public:
    UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Weapon")
    FText WeaponName;

    // Reference to a scaling table — loaded on demand.
    UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Stats",
              meta = (AssetBundles = "Game"))
    TSoftObjectPtr<UDataTable> ScalingTable;

    float GetDamageAtTier(int32 Tier) const
    {
        // ScalingTable must already be loaded (via bundle).
        UDataTable* Table = ScalingTable.Get();
        if (!Table) { return 0.f; }

        FName RowName = FName(*FString::Printf(TEXT("Tier_%d"), Tier));
        const FWeaponScalingRow* Row =
            Table->FindRow<FWeaponScalingRow>(RowName, TEXT("GetDamageAtTier"));
        return Row ? Row->Damage : 0.f;
    }
};
```

---

## Pattern E: Subsystem as Data Gateway

A `UGameInstanceSubsystem` caches loaded data assets after initial scan, providing a central access point that avoids repeated Asset Manager calls throughout the codebase.

```cpp
// ItemSubsystem.h
#pragma once
#include "Subsystems/GameInstanceSubsystem.h"
#include "ItemSubsystem.generated.h"

UCLASS()
class MYGAME_API UItemSubsystem : public UGameInstanceSubsystem
{
    GENERATED_BODY()
public:
    virtual void Initialize(FSubsystemCollectionBase& Collection) override;

    UItemDefinition* GetItemById(const FPrimaryAssetId& Id) const;
    TArray<UItemDefinition*> GetItemsByTag(FGameplayTag Tag) const;

private:
    void OnItemsLoaded();

    TMap<FPrimaryAssetId, TObjectPtr<UItemDefinition>> ItemCache;
    TSharedPtr<FStreamableHandle> LoadHandle;
};
```

```cpp
// ItemSubsystem.cpp
void UItemSubsystem::Initialize(FSubsystemCollectionBase& Collection)
{
    Super::Initialize(Collection);

    UAssetManager& AM = UAssetManager::Get();
    TArray<FPrimaryAssetId> ItemIds;
    AM.GetPrimaryAssetIdList(FPrimaryAssetType(TEXT("ItemDefinition")), ItemIds);

    LoadHandle = AM.LoadPrimaryAssets(
        ItemIds,
        { TEXT("UI") },
        FStreamableDelegate::CreateUObject(this, &UItemSubsystem::OnItemsLoaded));
}

void UItemSubsystem::OnItemsLoaded()
{
    UAssetManager& AM = UAssetManager::Get();
    TArray<UObject*> LoadedObjects;
    AM.GetPrimaryAssetObjectList(FPrimaryAssetType(TEXT("ItemDefinition")), LoadedObjects);

    for (UObject* Obj : LoadedObjects)
    {
        if (UItemDefinition* Item = Cast<UItemDefinition>(Obj))
        {
            ItemCache.Add(Item->GetPrimaryAssetId(), Item);
        }
    }
}

UItemDefinition* UItemSubsystem::GetItemById(const FPrimaryAssetId& Id) const
{
    const TObjectPtr<UItemDefinition>* Found = ItemCache.Find(Id);
    return Found ? Found->Get() : nullptr;
}

TArray<UItemDefinition*> UItemSubsystem::GetItemsByTag(FGameplayTag Tag) const
{
    TArray<UItemDefinition*> Results;
    for (const auto& Pair : ItemCache)
    {
        if (Pair.Value && Pair.Value->ItemTags.HasTag(Tag))
        {
            Results.Add(Pair.Value);
        }
    }
    return Results;
}
```

---

## When to Use Each Approach

| Scenario | Recommended Approach |
|---|---|
| Per-item configs, ~10–500 items, designers use editor | `UPrimaryDataAsset` + Asset Manager |
| Large flat tables, designers use Excel/Sheets | `UDataTable` + CSV import |
| Global game settings, always in memory | `UDataAsset` (plain), hard reference |
| Server-only data (drop rates, economy) | `UDataTable` with `bStripFromClientBuilds=true` |
| Items with stat scaling per tier | Hybrid: PrimaryDataAsset + soft ref to DataTable |
| Runtime-generated content | `UDataTable::AddRow`, or dynamic `FPrimaryAssetId` via `AddDynamicAsset` |
| Querying without loading | `IAssetRegistry::GetAssetsByClass` + `FAssetData` |

---

## Designer Workflow Checklist

1. **C++ schema merged**: Row struct or DataAsset class is compiled and visible in the editor.
2. **Asset registered**: `DefaultGame.ini` has the correct `PrimaryAssetTypesToScan` entry (for PrimaryDataAssets).
3. **Editor asset created**: Data Asset instances or DataTable created in Content Browser under the scanned path.
4. **Data populated**: Fields filled in the editor or CSV imported.
5. **Cook verified**: Launch a development cook and confirm assets appear in the cooked output. Check for "Asset not in cook" warnings in the log.
6. **Bundle states tested**: Verify UI bundle loads in menus and Game bundle loads during gameplay without performance spikes.
