# Replication Patterns

Common patterns for replicating game state in Unreal Engine multiplayer projects.
Each pattern includes the header declarations, implementation, and client callback.

---

## Pattern 1: Health with OnRep Callback

The most common pattern. Health is authoritative on the server. Clients receive the
updated value and react via `OnRep_Health` (update HUD, play hurt effects).

```cpp
// AMyCharacter.h
UPROPERTY(ReplicatedUsing = OnRep_Health)
float Health;

UPROPERTY(ReplicatedUsing = OnRep_MaxHealth)
float MaxHealth;

UFUNCTION()
void OnRep_Health(float PreviousHealth);

UFUNCTION()
void OnRep_MaxHealth(float PreviousMaxHealth);

// Server RPC — clients request damage (usually called by server game logic instead)
UFUNCTION(Server, Reliable, WithValidation)
void ServerApplyHealing(float Amount);
```

```cpp
// AMyCharacter.cpp
#include "Net/UnrealNetwork.h"

void AMyCharacter::GetLifetimeReplicatedProps(
    TArray<FLifetimeProperty>& OutLifetimeProps) const
{
    Super::GetLifetimeReplicatedProps(OutLifetimeProps);
    DOREPLIFETIME(AMyCharacter, Health);
    DOREPLIFETIME(AMyCharacter, MaxHealth);
}

void AMyCharacter::OnRep_Health(float PreviousHealth)
{
    // Called on clients only — update UI and effects
    OnHealthChanged.Broadcast(PreviousHealth, Health);
    if (Health < PreviousHealth)
    {
        PlayHurtMontage();
    }
}

void AMyCharacter::OnRep_MaxHealth(float PreviousMaxHealth)
{
    OnMaxHealthChanged.Broadcast(PreviousMaxHealth, MaxHealth);
}

// Called by game logic on server only
void AMyCharacter::ApplyDamage_Authority(float Damage)
{
    if (!HasAuthority()) return;
    Health = FMath::Clamp(Health - Damage, 0.f, MaxHealth);
    if (Health <= 0.f)
    {
        Die_Authority();
    }
}

void AMyCharacter::ServerApplyHealing_Implementation(float Amount)
{
    // Validate amount is positive and actor is alive
    Health = FMath::Clamp(Health + Amount, 0.f, MaxHealth);
}

bool AMyCharacter::ServerApplyHealing_Validate(float Amount)
{
    return Amount > 0.f && Amount <= 500.f; // reject absurd values
}
```

---

## Pattern 2: Team Data (Owner-Only Private + All-Clients Public)

Split information based on who needs it. Score is public; private currency is owner-only.

```cpp
// AMyPlayerState.h  (PlayerState replicates to all clients)
UPROPERTY(ReplicatedUsing = OnRep_TeamId)
int32 TeamId;

UPROPERTY(Replicated)
int32 Score;

UPROPERTY(Replicated)
int32 Kills;

// Private to owning player only
UPROPERTY(ReplicatedUsing = OnRep_Currency)
int32 Currency;
```

```cpp
// AMyPlayerState.cpp
void AMyPlayerState::GetLifetimeReplicatedProps(
    TArray<FLifetimeProperty>& OutLifetimeProps) const
{
    Super::GetLifetimeReplicatedProps(OutLifetimeProps);

    DOREPLIFETIME(AMyPlayerState, TeamId);
    DOREPLIFETIME(AMyPlayerState, Score);
    DOREPLIFETIME(AMyPlayerState, Kills);

    // Only the owning client receives their own currency
    DOREPLIFETIME_CONDITION(AMyPlayerState, Currency, COND_OwnerOnly);
}

void AMyPlayerState::OnRep_TeamId()
{
    // Update team color, nameplate, etc. on all clients
    OnTeamChanged.Broadcast(TeamId);
}

void AMyPlayerState::OnRep_Currency()
{
    // Update shop UI — only fires on the owning client
    OnCurrencyChanged.Broadcast(Currency);
}
```

---

## Pattern 3: Inventory Using FFastArraySerializer

Efficient replicated inventory — only changed items are sent over the network,
not the entire array.

```cpp
// InventoryTypes.h
USTRUCT(BlueprintType)
struct FInventoryItem : public FFastArraySerializerItem
{
    GENERATED_BODY()

    UPROPERTY()
    int32 ItemId = 0;

    UPROPERTY()
    int32 Quantity = 0;

    UPROPERTY()
    float Durability = 1.0f;

    void PreReplicatedRemove(const struct FInventoryList& InArraySerializer);
    void PostReplicatedAdd(const struct FInventoryList& InArraySerializer);
    void PostReplicatedChange(const struct FInventoryList& InArraySerializer);
};

USTRUCT()
struct FInventoryList : public FFastArraySerializer
{
    GENERATED_BODY()

    UPROPERTY()
    TArray<FInventoryItem> Items;

    bool NetDeltaSerialize(FNetDeltaSerializeInfo& DeltaParms)
    {
        return FFastArraySerializer::FastArrayDeltaSerialize<FInventoryItem, FInventoryList>(
            Items, DeltaParms, *this);
    }
};

template<>
struct TStructOpsTypeTraits<FInventoryList>
    : public TStructOpsTypeTraitsBase2<FInventoryList>
{
    enum { WithNetDeltaSerializer = true };
};
```

```cpp
// UMyInventoryComponent.h
UCLASS()
class UMyInventoryComponent : public UActorComponent
{
    GENERATED_BODY()

public:
    virtual void GetLifetimeReplicatedProps(
        TArray<FLifetimeProperty>& OutLifetimeProps) const override;

    // Only the owning player sees their own inventory
    UPROPERTY(ReplicatedUsing = OnRep_Inventory)
    FInventoryList Inventory;

    UFUNCTION()
    void OnRep_Inventory();

    // Server-side mutation
    void AddItem_Authority(int32 ItemId, int32 Quantity);
    void RemoveItem_Authority(int32 ItemId, int32 Quantity);
};
```

```cpp
// UMyInventoryComponent.cpp
void UMyInventoryComponent::GetLifetimeReplicatedProps(
    TArray<FLifetimeProperty>& OutLifetimeProps) const
{
    Super::GetLifetimeReplicatedProps(OutLifetimeProps);
    DOREPLIFETIME_CONDITION(UMyInventoryComponent, Inventory, COND_OwnerOnly);
}

void UMyInventoryComponent::AddItem_Authority(int32 ItemId, int32 Quantity)
{
    if (!GetOwner()->HasAuthority()) return;

    // Find existing stack
    for (FInventoryItem& Item : Inventory.Items)
    {
        if (Item.ItemId == ItemId)
        {
            Item.Quantity += Quantity;
            Inventory.MarkItemDirty(Item); // tell FastArray this item changed
            return;
        }
    }

    // Add new stack
    FInventoryItem& NewItem = Inventory.Items.AddDefaulted_GetRef();
    NewItem.ItemId = ItemId;
    NewItem.Quantity = Quantity;
    Inventory.MarkItemDirty(NewItem);
}

// Callbacks on client
void FInventoryItem::PostReplicatedAdd(const FInventoryList& InArraySerializer)
{
    // New item appeared in inventory — update UI
}

void FInventoryItem::PostReplicatedChange(const FInventoryList& InArraySerializer)
{
    // Existing item quantity or durability changed — update slot UI
}

void FInventoryItem::PreReplicatedRemove(const FInventoryList& InArraySerializer)
{
    // Item is about to be removed — clear UI slot
}
```

---

## Pattern 4: Ability State (InitialOnly + Runtime Flags)

Ability unlocks are set once; cooldowns and charges update dynamically.

```cpp
// UMyAbilityComponent.h
// Which abilities are unlocked — sent once at spawn, never changes
UPROPERTY(Replicated)
TArray<int32> UnlockedAbilityIds;

// Current cooldown end times per ability slot
UPROPERTY(ReplicatedUsing = OnRep_Cooldowns)
TArray<float> CooldownEndTimes;

// Active ability flags bitmask
UPROPERTY(ReplicatedUsing = OnRep_ActiveFlags)
uint8 ActiveAbilityFlags;

UFUNCTION()
void OnRep_Cooldowns();

UFUNCTION()
void OnRep_ActiveFlags(uint8 PreviousFlags);
```

```cpp
// UMyAbilityComponent.cpp
void UMyAbilityComponent::GetLifetimeReplicatedProps(
    TArray<FLifetimeProperty>& OutLifetimeProps) const
{
    Super::GetLifetimeReplicatedProps(OutLifetimeProps);

    // Unlocked abilities: all clients see which abilities a player has
    DOREPLIFETIME_CONDITION(UMyAbilityComponent, UnlockedAbilityIds, COND_InitialOnly);

    // Cooldowns: only the owning client needs exact cooldown timers
    DOREPLIFETIME_CONDITION(UMyAbilityComponent, CooldownEndTimes, COND_OwnerOnly);

    // Active flags: all clients see which abilities are currently active (for animation)
    DOREPLIFETIME(UMyAbilityComponent, ActiveAbilityFlags);
}

void UMyAbilityComponent::OnRep_Cooldowns()
{
    // Refresh cooldown bar UI for owning player only
}

void UMyAbilityComponent::OnRep_ActiveFlags(uint8 PreviousFlags)
{
    // Determine which bits changed and trigger corresponding animations/effects
    uint8 ChangedBits = ActiveAbilityFlags ^ PreviousFlags;
    for (int32 i = 0; i < 8; ++i)
    {
        if (ChangedBits & (1 << i))
        {
            bool bNowActive = (ActiveAbilityFlags & (1 << i)) != 0;
            OnAbilityActivationChanged.Broadcast(i, bNowActive);
        }
    }
}
```

---

## Pattern 5: Replicated Object Subobject (UE 5.1+ API)

A `UObject` subobject with its own replicated properties, registered via the modern API.

```cpp
// UMyQuestData.h
UCLASS()
class UMyQuestData : public UObject
{
    GENERATED_BODY()

public:
    virtual void GetLifetimeReplicatedProps(
        TArray<FLifetimeProperty>& OutLifetimeProps) const override;

    virtual bool IsSupportedForNetworking() const override { return true; }

    UPROPERTY(Replicated)
    int32 QuestId;

    UPROPERTY(Replicated)
    int32 Progress;

    UPROPERTY(Replicated)
    bool bCompleted;
};
```

```cpp
// AMyPlayerController.cpp — register the subobject during BeginPlay on server
void AMyPlayerController::BeginPlay()
{
    Super::BeginPlay();
    if (HasAuthority())
    {
        ActiveQuest = NewObject<UMyQuestData>(this);
        ActiveQuest->QuestId = 42;
        // Register with COND_OwnerOnly so only this player's client receives it
        AddReplicatedSubObject(ActiveQuest, COND_OwnerOnly);
    }
}

void AMyPlayerController::EndPlay(const EEndPlayReason::Type EndPlayReason)
{
    if (HasAuthority() && ActiveQuest)
    {
        RemoveReplicatedSubObject(ActiveQuest);
    }
    Super::EndPlay(EndPlayReason);
}
```

```cpp
// UMyQuestData.cpp
void UMyQuestData::GetLifetimeReplicatedProps(
    TArray<FLifetimeProperty>& OutLifetimeProps) const
{
    Super::GetLifetimeReplicatedProps(OutLifetimeProps);
    DOREPLIFETIME(UMyQuestData, QuestId);
    DOREPLIFETIME(UMyQuestData, Progress);
    DOREPLIFETIME(UMyQuestData, bCompleted);
}
```

---

## Pattern 6: Replicated Actor Movement (FRepMovement)

For actors that move but do not use `UCharacterMovementComponent`, replicate movement
via `bReplicateMovement` and the built-in `FRepMovement` struct.

```cpp
// AMyVehicle.h
AMyVehicle()
{
    bReplicates = true;
    SetReplicateMovement(true); // enables FRepMovement replication via OnRep_ReplicatedMovement
    SetNetUpdateFrequency(50.f);
    NetPriority = 2.5f;
}

// Override to apply custom interpolation when movement data arrives on simulated proxies
virtual void OnRep_ReplicatedMovement() override;
```

```cpp
// AMyVehicle.cpp
void AMyVehicle::OnRep_ReplicatedMovement()
{
    Super::OnRep_ReplicatedMovement(); // applies FRepMovement to root component

    // Additional logic: apply physics state, snap wheels, etc.
    SyncWheelPositions();
}
```

For physics-simulated actors, set `bRepPhysics = true` on the `FRepMovement` to
include linear and angular velocity, allowing clients to simulate physics correctly.

---

## Pattern 7: Custom Relevancy Override

Override `IsNetRelevantFor` to implement game-specific relevancy (team-based, zone-based, etc.).

```cpp
// AMyActor.h
virtual bool IsNetRelevantFor(
    const AActor* RealViewer,
    const AActor* ViewTarget,
    const FVector& SrcLocation) const override;
```

```cpp
// AMyActor.cpp — only replicate to players on the same team
bool AMyActor::IsNetRelevantFor(
    const AActor* RealViewer,
    const AActor* ViewTarget,
    const FVector& SrcLocation) const
{
    // Always relevant to owner
    if (RealViewer == GetOwner()) return true;

    // Check team
    const AMyPlayerController* PC = Cast<AMyPlayerController>(RealViewer);
    if (PC && PC->GetTeamId() == TeamId)
    {
        // Also respect distance — call default distance check
        return Super::IsNetRelevantFor(RealViewer, ViewTarget, SrcLocation);
    }

    return false;
}
```

---

## Pattern 8: Dormancy for Rarely-Updated Actors

Actors like pickups and map objectives update infrequently. Use dormancy to skip
replication checks when nothing changes.

```cpp
// AMyPickup.h
AMyPickup()
{
    bReplicates = true;
    NetDormancy = DORM_DormantAll; // start dormant
    SetNetUpdateFrequency(1.f);
}

void PickupCollected(ACharacter* Collector);
```

```cpp
// AMyPickup.cpp
void AMyPickup::PickupCollected(ACharacter* Collector)
{
    if (!HasAuthority()) return;

    bPickedUp = true;
    SetActorHiddenInGame(true);
    SetActorEnableCollision(false);

    // Wake up for one replication update to push bPickedUp to clients, then re-dormant
    FlushNetDormancy();

    // Schedule respawn
    GetWorldTimerManager().SetTimer(
        RespawnTimer, this, &AMyPickup::Respawn_Authority, RespawnTime, false);
}

void AMyPickup::Respawn_Authority()
{
    bPickedUp = false;
    SetActorHiddenInGame(false);
    SetActorEnableCollision(true);
    FlushNetDormancy(); // push respawn state, then return to dormant
}
```

---

## Bandwidth Estimation Guide

| Data Type                       | Approximate Bits per Update |
|---------------------------------|-----------------------------|
| `bool` (replicated)             | 1 bit + overhead (~8 bits)  |
| `uint8`                         | 8 bits                      |
| `int32`                         | 32 bits                     |
| `float`                         | 32 bits                     |
| `FVector` (full precision)      | 96 bits                     |
| `FVector_NetQuantize`           | ~30-48 bits                 |
| `FVector_NetQuantize10`         | ~30-48 bits (1/10 cm)       |
| `FRotator` (full)               | 96 bits                     |
| `FRotator` compressed           | ~24 bits                    |
| `FRepMovement`                  | ~100-200 bits               |
| RPC call overhead               | ~80-120 bits + params       |

Use `FVector_NetQuantize` variants for world positions and directions to halve
bandwidth compared to raw `FVector`. The precision tiers are:

- `FVector_NetQuantize` — 1 cm precision
- `FVector_NetQuantize10` — 0.1 cm precision
- `FVector_NetQuantize100` — 0.01 cm precision
- `FVector_NetQuantizeNormal` — unit vector, ~16 bits
