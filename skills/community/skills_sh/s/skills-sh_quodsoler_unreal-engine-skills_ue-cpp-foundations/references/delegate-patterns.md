# Delegate Patterns Reference

Complete reference for Unreal Engine's delegate system: declaration macros, binding methods, and invocation patterns. Source: `Engine/Source/Runtime/Core/Public/Delegates/DelegateCombinations.h` and `Delegate.h`.

---

## Delegate Type Overview

| Type | Macro Family | Bindings | Serializable | Blueprint | Use Case |
|------|-------------|----------|--------------|-----------|----------|
| Single static | `DECLARE_DELEGATE` | 1 | No | No | Internal single-owner callbacks |
| Multicast static | `DECLARE_MULTICAST_DELEGATE` | N | No | No | Internal multi-listener events |
| Thread-safe multicast | `DECLARE_TS_MULTICAST_DELEGATE` | N | No | No | Cross-thread event broadcasting |
| Dynamic single | `DECLARE_DYNAMIC_DELEGATE` | 1 | Yes | Yes | Blueprint-assignable single callback |
| Dynamic multicast | `DECLARE_DYNAMIC_MULTICAST_DELEGATE` | N | Yes | Yes | Blueprint-bindable events (most common for gameplay) |
| Return-value single | `DECLARE_DELEGATE_RetVal` | 1 | No | No | Query callbacks with a return value |

---

## Declaration Macros

All delegate type declarations go at **file scope** (outside classes), except `DECLARE_DYNAMIC_*` which should also be at file scope before the UCLASS that uses them.

### Single Delegate (No Parameters)

```cpp
DECLARE_DELEGATE(FOnGamePaused);
```

### Single Delegate with Parameters

```cpp
// One parameter
DECLARE_DELEGATE_OneParam(FOnItemCollected, AActor* /* Item */);

// Two parameters
DECLARE_DELEGATE_TwoParams(FOnDamageDealt, AActor* /* Target */, float /* Amount */);

// Three parameters
DECLARE_DELEGATE_ThreeParams(FOnAbilityUsed, FName /* AbilityID */, int32 /* Level */, float /* Cooldown */);

// Up to nine parameters supported
DECLARE_DELEGATE_FourParams(FOnWeaponFired, FVector /* Origin */, FVector /* Direction */, float /* Damage */, AActor* /* Shooter */);
```

### Single Delegate with Return Value

```cpp
DECLARE_DELEGATE_RetVal(bool, FOnShouldSpawn);
DECLARE_DELEGATE_RetVal_OneParam(float, FOnCalculateDamage, float /* BaseDamage */);
DECLARE_DELEGATE_RetVal_TwoParams(AActor*, FOnSelectTarget, FVector /* Origin */, float /* Range */);
```

### Multicast Delegate

```cpp
DECLARE_MULTICAST_DELEGATE(FOnLevelLoaded);
DECLARE_MULTICAST_DELEGATE_OneParam(FOnActorSpawned, AActor* /* SpawnedActor */);
DECLARE_MULTICAST_DELEGATE_TwoParams(FOnHealthChanged, float /* Current */, float /* Max */);
DECLARE_MULTICAST_DELEGATE_ThreeParams(FOnGameEvent, FName /* EventID */, UObject* /* Instigator */, const FString& /* Payload */);
```

### Thread-Safe Multicast

```cpp
// Use when broadcasting from non-game threads
DECLARE_TS_MULTICAST_DELEGATE_OneParam(FOnAsyncDataReady, const TArray<uint8>& /* Data */);
```

### Dynamic Single Delegate

```cpp
// Saveable, can be assigned in Blueprint
// Param names are required (used as Blueprint pin labels)
DECLARE_DYNAMIC_DELEGATE(FOnSimpleEvent);
DECLARE_DYNAMIC_DELEGATE_OneParam(FOnActorDestroyed, AActor*, DestroyedActor);
DECLARE_DYNAMIC_DELEGATE_TwoParams(FOnTransformChanged, FVector, NewLocation, FRotator, NewRotation);

// With return value
DECLARE_DYNAMIC_DELEGATE_RetVal(bool, FOnValidationCheck);
DECLARE_DYNAMIC_DELEGATE_RetVal_OneParam(float, FOnGetModifiedDamage, float, BaseDamage);
```

### Dynamic Multicast Delegate

```cpp
// Most common for UPROPERTY(BlueprintAssignable) events
DECLARE_DYNAMIC_MULTICAST_DELEGATE(FOnGameStarted);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnScoreChanged, int32, NewScore);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_TwoParams(FOnPlayerDied, APlayerController*, PlayerController, AActor*, KillerActor);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_ThreeParams(
    FOnAbilityActivated,
    FName,          AbilityID,
    int32,          Level,
    APlayerState*,  PlayerState);

// Four params
DECLARE_DYNAMIC_MULTICAST_DELEGATE_FourParams(
    FOnHitResult,
    FVector,    HitLocation,
    FVector,    HitNormal,
    float,      Damage,
    AActor*,    HitActor);
```

---

## Declaring in a UCLASS

```cpp
// Forward-declare or include delegate declarations before the class

DECLARE_DYNAMIC_MULTICAST_DELEGATE_TwoParams(FOnHealthChanged, float, CurrentHealth, float, MaxHealth);
DECLARE_MULTICAST_DELEGATE_OneParam(FOnDeathNative, AActor* /* DeadActor */);

UCLASS(Blueprintable)
class MYGAME_API AMyCharacter : public ACharacter
{
    GENERATED_BODY()

public:
    // BlueprintAssignable — Blueprint can bind to this in event graph
    UPROPERTY(BlueprintAssignable, Category="Events")
    FOnHealthChanged OnHealthChanged;

    // BlueprintCallable on a delegate property — Blueprint can call Broadcast
    UPROPERTY(BlueprintAssignable, BlueprintCallable, Category="Events")
    FOnHealthChanged OnHealthChangedCallable;

    // Native-only multicast (no UPROPERTY needed, but no GC protection either)
    FOnDeathNative OnDeathNative;
};
```

---

## Binding Methods

### Single Static Delegate Binding

```cpp
FOnItemCollected Delegate;

// Bind to a UObject member function (safe: auto-unbinds on UObject destruction)
Delegate.BindUObject(this, &AMyCharacter::HandleItemCollected);

// Bind to a raw C++ pointer (unsafe: does NOT unbind automatically)
Delegate.BindRaw(RawPtr, &FMyHelper::HandleItem);

// Bind to a static function (no instance)
Delegate.BindStatic(&UMyLibrary::StaticHandleItem);

// Bind to a TSharedPtr owner (safe: weak-ref checked on invocation)
Delegate.BindSP(SharedOwner, &FMyOwner::Handle);

// Bind to a lambda
Delegate.BindLambda([this](AActor* Item)
{
    UE_LOG(LogMyGame, Log, TEXT("Collected: %s"), *Item->GetName());
});

// Bind with extra payload parameters (up to 4 bound "payload" vars)
float ScoreBonus = 1.5f;
Delegate.BindUObject(this, &AMyCharacter::HandleItemWithBonus, ScoreBonus);

// Check binding state
if (Delegate.IsBound())
{
    Delegate.Execute(SomeActor);
}

// ExecuteIfBound — no-op if not bound (use for optional callbacks)
Delegate.ExecuteIfBound(SomeActor);

// Unbind
Delegate.Unbind();
```

### Multicast Static Delegate Binding

```cpp
FOnHealthChanged HealthDelegate;

// Add binding — returns a handle for later removal
FDelegateHandle Handle = HealthDelegate.AddUObject(this, &AMyHUD::OnHealthChanged);

// Lambda binding
FDelegateHandle LambdaHandle = HealthDelegate.AddLambda([](float Current, float Max)
{
    // Update UI
});

// Raw pointer binding
FDelegateHandle RawHandle = HealthDelegate.AddRaw(RawPtr, &FMyClass::Handle);

// SP binding
FDelegateHandle SpHandle = HealthDelegate.AddSP(SharedOwner, &FMyClass::Handle);

// Broadcast — calls all bound functions
HealthDelegate.Broadcast(75.f, 100.f);

// Remove by handle (precise)
HealthDelegate.Remove(Handle);
HealthDelegate.Remove(LambdaHandle);

// Remove by UObject — removes all bindings from that object
HealthDelegate.RemoveAll(this);

// Check if any bindings exist
bool bHasListeners = HealthDelegate.IsBound();
```

### Dynamic Single Delegate Binding

```cpp
FOnActorDestroyed Delegate;

// Bind to a UFUNCTION on a UObject (the function MUST be a UFUNCTION)
Delegate.BindDynamic(this, &AMyCharacter::HandleActorDestroyed);

// Check
bool bBound = Delegate.IsBound();

// Execute
Delegate.ExecuteIfBound(SomeActor);

// Unbind
Delegate.Unbind();
```

### Dynamic Multicast Delegate Binding

```cpp
// In UCLASS that declares OnHealthChanged:
OnHealthChanged.AddDynamic(this, &AMyHUD::HandleHealthChanged);

// Remove specific binding
OnHealthChanged.RemoveDynamic(this, &AMyHUD::HandleHealthChanged);

// Remove all bindings from an object
OnHealthChanged.RemoveAll(this);

// Broadcast
OnHealthChanged.Broadcast(NewHealth, MaxHealth);

// Check
bool bHasBindings = OnHealthChanged.IsBound();
```

---

## Complete Example: Full Delegate Workflow

### Component-based health with events

```cpp
// HealthComponent.h

DECLARE_DYNAMIC_MULTICAST_DELEGATE_TwoParams(FOnHealthChangedSignature, float, CurrentHealth, float, MaxHealth);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnDeathSignature, AActor*, KillerActor);
DECLARE_MULTICAST_DELEGATE_OneParam(FOnHealthChangedNative, float /* NewHealthFraction */);

UCLASS(ClassGroup=Combat, meta=(BlueprintSpawnableComponent))
class MYGAME_API UHealthComponent : public UActorComponent
{
    GENERATED_BODY()

public:
    // Blueprint-assignable events
    UPROPERTY(BlueprintAssignable, Category="Health")
    FOnHealthChangedSignature OnHealthChanged;

    UPROPERTY(BlueprintAssignable, Category="Health")
    FOnDeathSignature OnDeath;

    // Native-only event for C++ subsystems (faster, no reflection overhead)
    FOnHealthChangedNative OnHealthChangedNative;

    UFUNCTION(BlueprintCallable, Category="Health")
    void ApplyDamage(float DamageAmount, AActor* DamageInstigator);

    UFUNCTION(BlueprintPure, Category="Health")
    float GetHealthFraction() const { return CurrentHealth / MaxHealth; }

private:
    UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category="Health",
              meta=(AllowPrivateAccess="true", ClampMin="1.0"))
    float MaxHealth = 100.f;

    UPROPERTY(Transient)
    float CurrentHealth;

    virtual void BeginPlay() override;
};
```

```cpp
// HealthComponent.cpp

void UHealthComponent::BeginPlay()
{
    Super::BeginPlay();
    CurrentHealth = MaxHealth;
}

void UHealthComponent::ApplyDamage(float DamageAmount, AActor* DamageInstigator)
{
    if (CurrentHealth <= 0.f) return;

    CurrentHealth = FMath::Clamp(CurrentHealth - DamageAmount, 0.f, MaxHealth);

    // Fire both native and dynamic events
    OnHealthChanged.Broadcast(CurrentHealth, MaxHealth);
    OnHealthChangedNative.Broadcast(CurrentHealth / MaxHealth);

    if (CurrentHealth <= 0.f)
    {
        OnDeath.Broadcast(DamageInstigator);
    }
}
```

```cpp
// MyCharacter.cpp — binding to the component's delegates

void AMyCharacter::BeginPlay()
{
    Super::BeginPlay();

    UHealthComponent* HC = FindComponentByClass<UHealthComponent>();
    if (HC)
    {
        // Dynamic: Blueprint can also bind this in its event graph
        HC->OnHealthChanged.AddDynamic(this, &AMyCharacter::HandleHealthChanged);
        HC->OnDeath.AddDynamic(this, &AMyCharacter::HandleDeath);

        // Native: C++ subsystem listens too
        HC->OnHealthChangedNative.AddUObject(this, &AMyCharacter::HandleHealthChangedNative);
    }
}

void AMyCharacter::EndPlay(const EEndPlayReason::Type EndPlayReason)
{
    UHealthComponent* HC = FindComponentByClass<UHealthComponent>();
    if (HC)
    {
        HC->OnHealthChanged.RemoveDynamic(this, &AMyCharacter::HandleHealthChanged);
        HC->OnDeath.RemoveDynamic(this, &AMyCharacter::HandleDeath);
        HC->OnHealthChangedNative.RemoveAll(this);
    }
    Super::EndPlay(EndPlayReason);
}

void AMyCharacter::HandleHealthChanged(float CurrentHealth, float MaxHealth)
{
    UE_LOG(LogMyGame, Log, TEXT("[%s] Health: %.1f / %.1f"), *GetName(), CurrentHealth, MaxHealth);
}

void AMyCharacter::HandleDeath(AActor* KillerActor)
{
    UE_LOG(LogMyGame, Warning, TEXT("[%s] Died. Killer: %s"), *GetName(),
           KillerActor ? *KillerActor->GetName() : TEXT("Unknown"));
}

void AMyCharacter::HandleHealthChangedNative(float HealthFraction)
{
    // Update UI or animation state without Blueprint overhead
}
```

---

## Binding Method Quick Reference

| Method | Owner Safety | Auto-Unbind | Use With |
|--------|-------------|-------------|----------|
| `BindUObject` / `AddUObject` | Yes (weak ref) | On UObject destroy | UObject-derived classes |
| `BindSP` / `AddSP` | Yes (weak ptr) | On TSharedPtr destruction | Non-UObject with TSharedPtr |
| `BindRaw` / `AddRaw` | No | Never | Raw pointers (manual unbind required) |
| `BindStatic` / `AddStatic` | N/A | Never | Global/static functions |
| `BindLambda` / `AddLambda` | No (capture manually) | Never | Short-lived, inline callbacks |
| `BindDynamic` / `AddDynamic` | Yes (UFUNCTION) | On UObject destroy | Dynamic delegates only |

> **Safety rule:** Always `RemoveAll(this)` in `EndPlay` or destructor when using `AddLambda` or `AddRaw` to avoid calling into destroyed objects.

---

## Common Mistakes

**Calling Execute() on an unbound delegate:**
```cpp
// BAD — asserts in Debug if not bound
PickupDelegate.Execute(SomeActor);

// GOOD
PickupDelegate.ExecuteIfBound(SomeActor);
// Or:
if (PickupDelegate.IsBound()) { PickupDelegate.Execute(SomeActor); }
```

**Binding lambda to multicast without storing the handle:**
```cpp
// BAD — cannot be removed later
OnHealthChanged.AddLambda([this](float C, float M) { ... });

// GOOD — store the handle
FDelegateHandle Handle = OnHealthChanged.AddLambda([this](float C, float M) { ... });
// Later:
OnHealthChanged.Remove(Handle);
```

**Using AddDynamic with a non-UFUNCTION:**
```cpp
// BAD — compile error or undefined behavior
OnHealthChanged.AddDynamic(this, &AMyCharacter::NonUFunction);

// GOOD — the function must have UFUNCTION()
UFUNCTION()
void HandleHealthChanged(float Current, float Max);
```

**Forgetting to RemoveDynamic in EndPlay:**
```cpp
// BAD — dangling binding, crash when broadcast fires after object destruction
void AMyActor::BeginPlay()
{
    Super::BeginPlay();
    OtherActor->OnEvent.AddDynamic(this, &AMyActor::HandleEvent);
    // Never removed!
}

// GOOD
void AMyActor::EndPlay(const EEndPlayReason::Type EndPlayReason)
{
    if (IsValid(OtherActor))
    {
        OtherActor->OnEvent.RemoveDynamic(this, &AMyActor::HandleEvent);
    }
    Super::EndPlay(EndPlayReason);
}
```

**Dynamic multicast delegate not in UPROPERTY:**
```cpp
// BAD — not serialized; Blueprint bindings lost between sessions
FOnScoreChanged OnScoreChanged;

// GOOD
UPROPERTY(BlueprintAssignable, Category="Events")
FOnScoreChanged OnScoreChanged;
```

---

## Return-Value Delegate Pattern

Single static delegates support return values. Multicast and dynamic delegates do not (which binding's return value would you use?).

```cpp
DECLARE_DELEGATE_RetVal_OneParam(bool, FOnValidatePickup, AActor* /* Item */);

FOnValidatePickup ValidationDelegate;

ValidationDelegate.BindLambda([](AActor* Item) -> bool
{
    return IsValid(Item) && Item->ActorHasTag(FName("Pickup"));
});

if (ValidationDelegate.IsBound())
{
    bool bValid = ValidationDelegate.Execute(PotentialPickup);
    if (bValid) { CollectItem(PotentialPickup); }
}
```

---

## Payload Parameters (Bound Extras)

Single delegate bind methods accept up to 4 "payload" values that are forwarded after the delegate's declared parameters.

```cpp
DECLARE_DELEGATE_OneParam(FOnItemPickedUp, AActor* /* Item */);

float BonusMultiplier = 1.5f;
FName PickupSound = FName("SFX_Pickup");

// BonusMultiplier and PickupSound are captured at bind time
FOnItemPickedUp Delegate;
Delegate.BindUObject(this, &AMyCharacter::HandlePickupWithExtras, BonusMultiplier, PickupSound);

// The bound function signature must match declared params + payload params
void AMyCharacter::HandlePickupWithExtras(AActor* Item, float Bonus, FName Sound)
{
    // Bonus == 1.5f, Sound == "SFX_Pickup"
}
```
