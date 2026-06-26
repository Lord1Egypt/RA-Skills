# GAS Setup Patterns

Initialization sequences and ownership patterns for `UAbilitySystemComponent`.

---

## Pattern 1: ASC on PlayerState (Multiplayer Recommended)

The ASC lives on `APlayerState`. The PlayerState persists across respawns (Pawn does not), so
ability grants, active effects, and cooldowns survive death and respawn. The Pawn/Character acts
as the avatar (the physical representation).

### PlayerState

```cpp
// MyPlayerState.h
#pragma once
#include "GameFramework/PlayerState.h"
#include "AbilitySystemInterface.h"
#include "MyPlayerState.generated.h"

class UAbilitySystemComponent;
class UMyHealthSet;

UCLASS()
class AMyPlayerState : public APlayerState, public IAbilitySystemInterface
{
    GENERATED_BODY()
public:
    AMyPlayerState();

    virtual UAbilitySystemComponent* GetAbilitySystemComponent() const override;

    UMyHealthSet* GetHealthSet() const { return HealthSet; }

protected:
    // ASC lives here; created as default subobject
    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "GAS")
    TObjectPtr<UAbilitySystemComponent> AbilitySystemComponent;

    // AttributeSet created as subobject of ASC's outer (PlayerState)
    UPROPERTY()
    TObjectPtr<UMyHealthSet> HealthSet;
};
```

```cpp
// MyPlayerState.cpp
#include "MyPlayerState.h"
#include "AbilitySystemComponent.h"
#include "Attributes/MyHealthSet.h"

AMyPlayerState::AMyPlayerState()
{
    AbilitySystemComponent = CreateDefaultSubobject<UAbilitySystemComponent>(TEXT("ASC"));

    // Mixed: owner/autonomous proxy gets full GE info; simulated proxies get minimal
    AbilitySystemComponent->SetIsReplicated(true);
    AbilitySystemComponent->SetReplicationMode(EGameplayEffectReplicationMode::Mixed);

    // AttributeSet is a subobject of the PlayerState; ASC auto-discovers it
    HealthSet = CreateDefaultSubobject<UMyHealthSet>(TEXT("HealthSet"));

    // PlayerState replication required
    NetUpdateFrequency = 100.f;
}

UAbilitySystemComponent* AMyPlayerState::GetAbilitySystemComponent() const
{
    return AbilitySystemComponent;
}
```

### Character (Avatar)

```cpp
// MyCharacter.h
#pragma once
#include "GameFramework/Character.h"
#include "AbilitySystemInterface.h"
#include "MyCharacter.generated.h"

UCLASS()
class AMyCharacter : public ACharacter, public IAbilitySystemInterface
{
    GENERATED_BODY()
public:
    // Delegates to PlayerState's ASC
    virtual UAbilitySystemComponent* GetAbilitySystemComponent() const override;

    // Server: Called when controller possesses this pawn
    virtual void PossessedBy(AController* NewController) override;

    // Client: Called when PlayerState replicates
    virtual void OnRep_PlayerState() override;

private:
    void InitGAS();
    void GiveDefaultAbilities(); // Server only
};
```

```cpp
// MyCharacter.cpp
#include "MyCharacter.h"
#include "MyPlayerState.h"
#include "AbilitySystemComponent.h"

UAbilitySystemComponent* AMyCharacter::GetAbilitySystemComponent() const
{
    const AMyPlayerState* PS = GetPlayerState<AMyPlayerState>();
    return PS ? PS->GetAbilitySystemComponent() : nullptr;
}

void AMyCharacter::PossessedBy(AController* NewController)
{
    Super::PossessedBy(NewController);
    InitGAS();
    GiveDefaultAbilities(); // Authority only, safe here
}

void AMyCharacter::OnRep_PlayerState()
{
    Super::OnRep_PlayerState();
    InitGAS(); // Client side initialization
}

void AMyCharacter::InitGAS()
{
    AMyPlayerState* PS = GetPlayerState<AMyPlayerState>();
    if (!PS) return;

    UAbilitySystemComponent* ASC = PS->GetAbilitySystemComponent();
    if (!ASC) return;

    // OwnerActor = who logically owns the ASC (PlayerState)
    // AvatarActor = the physical actor in the world (Character)
    ASC->InitAbilityActorInfo(PS, this);
}

void AMyCharacter::GiveDefaultAbilities()
{
    if (!HasAuthority()) return;

    UAbilitySystemComponent* ASC = GetAbilitySystemComponent();
    if (!ASC) return;

    // Grant abilities from a data-driven list
    for (const TSubclassOf<UGameplayAbility>& AbilityClass : DefaultAbilities)
    {
        FGameplayAbilitySpec Spec(AbilityClass, 1 /*Level*/);
        ASC->GiveAbility(Spec);
    }
}
```

### Respawn Handling

When the Pawn is destroyed and respawned, the new Pawn must re-init its actor info:

```cpp
void AMyGameMode::RespawnPlayer(AController* Controller)
{
    // Destroy old pawn, spawn new one at respawn location
    APawn* OldPawn = Controller->GetPawn();
    if (OldPawn) OldPawn->Destroy();

    AMyCharacter* NewPawn = GetWorld()->SpawnActor<AMyCharacter>(
        CharacterClass, RespawnTransform);
    Controller->Possess(NewPawn);
    // PossessedBy fires → InitGAS → InitAbilityActorInfo with old PlayerState ASC
    // Active effects and cooldowns on the ASC survive the respawn
}
```

---

## Pattern 2: ASC on Character (Single-Player / AI)

Simpler setup. The ASC and AttributeSet both live on the Pawn. Use for AI actors or
single-player games where persistence across respawns is not needed.

```cpp
// MyAICharacter.h
#pragma once
#include "GameFramework/Character.h"
#include "AbilitySystemInterface.h"
#include "MyAICharacter.generated.h"

UCLASS()
class AMyAICharacter : public ACharacter, public IAbilitySystemInterface
{
    GENERATED_BODY()
public:
    AMyAICharacter();

    virtual UAbilitySystemComponent* GetAbilitySystemComponent() const override;
    virtual void BeginPlay() override;

protected:
    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "GAS")
    TObjectPtr<UAbilitySystemComponent> AbilitySystemComponent;

    UPROPERTY()
    TObjectPtr<UMyHealthSet> HealthSet;
};
```

```cpp
// MyAICharacter.cpp
#include "MyAICharacter.h"
#include "AbilitySystemComponent.h"
#include "Attributes/MyHealthSet.h"

AMyAICharacter::AMyAICharacter()
{
    AbilitySystemComponent = CreateDefaultSubobject<UAbilitySystemComponent>(TEXT("ASC"));
    AbilitySystemComponent->SetIsReplicated(true);
    // Minimal: AI does not need full GE replication on simulated proxies
    AbilitySystemComponent->SetReplicationMode(EGameplayEffectReplicationMode::Minimal);

    HealthSet = CreateDefaultSubobject<UMyHealthSet>(TEXT("HealthSet"));
}

UAbilitySystemComponent* AMyAICharacter::GetAbilitySystemComponent() const
{
    return AbilitySystemComponent;
}

void AMyAICharacter::BeginPlay()
{
    Super::BeginPlay();
    // For ASC on Pawn, OwnerActor == AvatarActor == this
    AbilitySystemComponent->InitAbilityActorInfo(this, this);

    if (HasAuthority())
    {
        // Grant AI abilities
        for (const TSubclassOf<UGameplayAbility>& AbilityClass : DefaultAbilities)
        {
            AbilitySystemComponent->GiveAbility(FGameplayAbilitySpec(AbilityClass, 1));
        }
    }
}
```

---

## Attribute Initialization from CurveTable

GAS supports initializing attributes from a `UCurveTable` for data-driven level scaling.
Row format: `[GroupName].[AttributeSetName].[AttributeName]`

Example rows:
```
Default.MyHealthSet.Health    | 100 | 150 | 200 | ...  (per level)
Default.MyHealthSet.MaxHealth | 100 | 150 | 200 | ...
Hero1.MyHealthSet.Health      |  80 | 120 | 160 | ...
```

```cpp
// Call after InitAbilityActorInfo, on server only:
UAbilitySystemGlobals::Get().GetAttributeSetInitter()->InitAttributeSetDefaults(
    AbilitySystemComponent,
    FName("Default"), // GroupName matches CurveTable row prefix
    PlayerLevel,
    true /*bInitialInit*/);
```

---

## Ability Spec Handle Tracking

Store handles to remove or modify abilities later:

```cpp
// In a component or character header:
UPROPERTY()
TArray<FGameplayAbilitySpecHandle> GrantedAbilityHandles;

// Granting:
FGameplayAbilitySpecHandle Handle = AbilitySystemComponent->GiveAbility(
    FGameplayAbilitySpec(UMyAbility::StaticClass(), 1));
GrantedAbilityHandles.Add(Handle);

// Removing a specific ability:
AbilitySystemComponent->ClearAbility(GrantedAbilityHandles[0]);

// Removing all granted abilities:
for (const FGameplayAbilitySpecHandle& H : GrantedAbilityHandles)
{
    AbilitySystemComponent->ClearAbility(H);
}
GrantedAbilityHandles.Empty();
```

---

## Tag Event Registration

Listen for gameplay tag additions/removals on the ASC:

```cpp
void AMyCharacter::InitGAS()
{
    // ... init actor info ...

    // Register delegate for stunned state:
    AbilitySystemComponent->RegisterGameplayTagEvent(
        FGameplayTag::RequestGameplayTag("State.Stunned"),
        EGameplayTagEventType::NewOrRemoved)
        .AddUObject(this, &AMyCharacter::OnStunnedTagChanged);
}

void AMyCharacter::OnStunnedTagChanged(const FGameplayTag Tag, int32 NewCount)
{
    if (NewCount > 0)
    {
        // Stunned: disable movement, play stun animation
    }
    else
    {
        // No longer stunned: re-enable movement
    }
}
```

---

## Attribute Value Delegates

React to attribute changes (e.g., update UI health bar):

```cpp
void UMyHealthWidget::BindToASC(UAbilitySystemComponent* ASC)
{
    if (!ASC) return;

    HealthChangedDelegateHandle = ASC->GetGameplayAttributeValueChangeDelegate(
        UMyHealthSet::GetHealthAttribute())
        .AddUObject(this, &UMyHealthWidget::OnHealthChanged);
}

void UMyHealthWidget::OnHealthChanged(const FOnAttributeChangeData& Data)
{
    UpdateHealthBar(Data.NewValue);
}

void UMyHealthWidget::UnbindFromASC(UAbilitySystemComponent* ASC)
{
    if (!ASC) return;
    ASC->GetGameplayAttributeValueChangeDelegate(UMyHealthSet::GetHealthAttribute())
        .Remove(HealthChangedDelegateHandle);
}
```

---

## Replication Mode Summary

| Mode | GE Replication | Tag Replication | Use Case |
|------|----------------|-----------------|----------|
| `Minimal` | None to simulated | Minimal tags only | AI, non-player actors |
| `Mixed` | Full to owner/autonomous, minimal to simulated | Full | Player-controlled characters |
| `Full` | Full to everyone | Full | Single-player or small games |

**Critical:** `Mixed` mode requires the ASC owner to be the PlayerState (or any actor
not the Pawn). If the ASC is on the Pawn with `Mixed` mode, tag replication to simulated
proxies will not work correctly. Use `Full` if ASC must be on the Pawn in multiplayer.
