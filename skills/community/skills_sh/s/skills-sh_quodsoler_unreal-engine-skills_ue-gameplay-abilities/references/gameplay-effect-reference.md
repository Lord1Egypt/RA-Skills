# GameplayEffect Reference

Configuration guide for `UGameplayEffect`: duration policies, modifier types, stacking rules,
execution calculations, periodic effects, and conditional effects.

Source: `GameplayEffect.h` (UE5.3+, modular GE component architecture)

---

## Duration Policies (`EGameplayEffectDurationType`)

| Value | Behavior |
|-------|----------|
| `Instant` | Executes once, modifies base value permanently, never enters the active container |
| `HasDuration` | Active for a set time, then removed; modifies current value temporarily |
| `Infinite` | Active until `RemoveActiveGameplayEffect` is called; use for passive bonuses |

Instant effects call `PostGameplayEffectExecute` on the AttributeSet; duration/infinite effects
do not (they work through aggregators on the current value).

---

## Modifier Operations (`EGameplayModOp`)

The modifier equation is evaluated in this order across all active modifiers:
```
Final = ((BaseValue + AddBase) * MultiplyAdditive / DivideAdditive * MultiplyCompound) + AddFinal
```

| Op | Enum | Effect |
|----|------|--------|
| `Additive` | `EGameplayModOp::Additive` | Adds to the attribute (+10 hp) |
| `Multiplicative` | `EGameplayModOp::Multiplicative` | Multiplies (1.25x damage) |
| `Division` | `EGameplayModOp::Division` | Divides; applied as additive in denominator |
| `Override` | `EGameplayModOp::Override` | Replaces the attribute value entirely |

---

## Magnitude Calculation Types (`EGameplayEffectMagnitudeCalculation`)

### ScalableFloat (most common)
A constant or level-scaled float. Supply a `FScalableFloat` backed optionally by a CurveTable:

```
Modifier: Health
Operation: Additive
Magnitude Type: ScalableFloat
Scalable Float Magnitude: -50.0  (or reference a CurveTable row for level scaling)
```

### AttributeBased
Derives magnitude from another attribute. Formula:
```
(Coefficient * (PreMultiplyAdditive + [Attribute Value])) + PostMultiplyAdditive
```

```
Magnitude Type: AttributeBased
Backing Attribute: SourceObject.AttackPower  (capture from Source or Target)
Attribute Calculation Type: AttributeMagnitude  (final evaluated value)
Coefficient: 1.0
```

`EAttributeBasedFloatCalculationType` options:
- `AttributeMagnitude`: Final current value (includes active modifiers)
- `AttributeBaseValue`: Permanent base value only
- `AttributeBonusMagnitude`: Final - Base (modifier contribution only)

### CustomCalculationClass
Runs a `UGameplayModMagnitudeCalculation` subclass for arbitrary logic:

```cpp
UCLASS()
class UMyDamageMagnitudeCalc : public UGameplayModMagnitudeCalculation
{
    GENERATED_BODY()
public:
    UMyDamageMagnitudeCalc();

    virtual float CalculateBaseMagnitude_Implementation(
        const FGameplayEffectSpec& Spec) const override;

private:
    // Declare captures in constructor
    FGameplayEffectAttributeCaptureDefinition AttackPowerDef;
};

UMyDamageMagnitudeCalc::UMyDamageMagnitudeCalc()
{
    // Capture AttackPower from Source at execution time (not snapshot)
    AttackPowerDef = FGameplayEffectAttributeCaptureDefinition(
        UMyAttackSet::GetAttackPowerAttribute(),
        EGameplayEffectAttributeCaptureSource::Source,
        false /*bSnapshot*/);
    RelevantAttributesToCapture.Add(AttackPowerDef);
}

float UMyDamageMagnitudeCalc::CalculateBaseMagnitude_Implementation(
    const FGameplayEffectSpec& Spec) const
{
    FAggregatorEvaluateParameters EvalParams;
    EvalParams.SourceTags = Spec.CapturedSourceTags.GetAggregatedTags();
    EvalParams.TargetTags = Spec.CapturedTargetTags.GetAggregatedTags();

    float AttackPower = 0.f;
    GetCapturedAttributeMagnitude(AttackPowerDef, Spec, EvalParams, AttackPower);
    return AttackPower * 1.5f; // Example: 150% of attack power
}
```

### SetByCaller
The caller sets the magnitude at spec creation time using a tag as the key.

In the GE asset:
```
Magnitude Type: SetByCaller
DataTag: SetByCaller.Damage
```

In ability/code:
```cpp
FGameplayEffectSpecHandle SpecHandle = MakeOutgoingGameplayEffectSpec(DamageEffectClass, Level);
SpecHandle.Data->SetSetByCallerMagnitude(
    FGameplayTag::RequestGameplayTag("SetByCaller.Damage"), 75.f);
ApplyGameplayEffectSpecToTarget(Handle, ActorInfo, ActivationInfo, SpecHandle, TargetASC);
```

---

## Execution Calculations (`UGameplayEffectExecutionCalculation`)

Executions are for complex damage formulas that modify multiple attributes at once.
They run on instant GEs and fire `PostGameplayEffectExecute` on the AttributeSet.

```cpp
UCLASS()
class UMyDamageExecution : public UGameplayEffectExecutionCalculation
{
    GENERATED_BODY()
public:
    UMyDamageExecution();

    virtual void Execute_Implementation(
        const FGameplayEffectCustomExecutionParameters& ExecutionParams,
        FGameplayEffectCustomExecutionOutput& OutExecutionOutput) const override;

private:
    FGameplayEffectAttributeCaptureDefinition AttackPowerDef;
    FGameplayEffectAttributeCaptureDefinition ArmorDef;
};

UMyDamageExecution::UMyDamageExecution()
{
    AttackPowerDef = FGameplayEffectAttributeCaptureDefinition(
        UMyAttackSet::GetAttackPowerAttribute(),
        EGameplayEffectAttributeCaptureSource::Source,
        true /*bSnapshot*/);

    ArmorDef = FGameplayEffectAttributeCaptureDefinition(
        UMyDefenseSet::GetArmorAttribute(),
        EGameplayEffectAttributeCaptureSource::Target,
        false);

    RelevantAttributesToCapture.Add(AttackPowerDef);
    RelevantAttributesToCapture.Add(ArmorDef);
}

void UMyDamageExecution::Execute_Implementation(
    const FGameplayEffectCustomExecutionParameters& ExecutionParams,
    FGameplayEffectCustomExecutionOutput& OutExecutionOutput) const
{
    const FGameplayEffectSpec& Spec = ExecutionParams.GetOwningSpec();

    FAggregatorEvaluateParameters EvalParams;
    EvalParams.SourceTags = Spec.CapturedSourceTags.GetAggregatedTags();
    EvalParams.TargetTags = Spec.CapturedTargetTags.GetAggregatedTags();

    float AttackPower = 0.f;
    ExecutionParams.AttemptCalculateCapturedAttributeMagnitude(
        AttackPowerDef, EvalParams, AttackPower);

    float Armor = 0.f;
    ExecutionParams.AttemptCalculateCapturedAttributeMagnitude(
        ArmorDef, EvalParams, Armor);

    // Example formula: damage = (attack * 2) - armor, min 1
    float Damage = FMath::Max(1.f, (AttackPower * 2.f) - Armor);

    // Output modifier: subtract from Health on target
    OutExecutionOutput.AddOutputModifier(FGameplayModifierEvaluatedData(
        UMyHealthSet::GetHealthAttribute(),
        EGameplayModOp::Additive,
        -Damage));
}
```

In the GE asset, add this class to `Executions` array (replaces individual Modifiers for complex
calculations).

---

## Stacking

### Stacking Type (`EGameplayEffectStackingType`)

| Value | Behavior |
|-------|----------|
| `None` | No stacking; each application is a separate active effect |
| `AggregateBySource` | One stack group per source ASC applying the effect |
| `AggregateByTarget` | One stack group regardless of source; all sources share one stack |

### Stack Limit

Set `StackLimitCount` in the GE asset. A value of 0 means unlimited.

### Duration Policy While Stacking (`EGameplayEffectStackingDurationPolicy`)

| Value | Behavior |
|-------|----------|
| `RefreshOnSuccessfulApplication` | Duration resets on each successful stack add |
| `NeverRefresh` | Duration is set at first application, never extended |
| `ExtendDuration` | Each new stack adds the spec's full duration to remaining time |

### Expiration Policy (`EGameplayEffectStackingExpirationPolicy`)

| Value | Behavior |
|-------|----------|
| `ClearEntireStack` | All stacks removed when the effect expires |
| `RemoveSingleStackAndRefreshDuration` | Decrement by 1 and restart duration |
| `RefreshDuration` | Duration refreshes (effectively infinite until manually removed) |

### Reading Stack Count at Runtime

```cpp
// By active handle:
int32 StackCount = AbilitySystemComponent->GetCurrentStackCount(ActiveHandle);

// By query:
FGameplayEffectQuery Query = FGameplayEffectQuery::MakeQuery_MatchAllOwningTags(
    FGameplayTagContainer(PoisonEffectTag));
int32 TotalStacks = AbilitySystemComponent->GetAggregatedStackCount(Query);

// Update SetByCaller on active stacking effect:
AbilitySystemComponent->UpdateActiveGameplayEffectSetByCallerMagnitude(
    ActiveHandle,
    FGameplayTag::RequestGameplayTag("SetByCaller.StackDamage"),
    NewDamageValue);
```

---

## Periodic Effects (Damage Over Time)

Set in the GE asset:
```
Duration Policy: HasDuration
Duration Magnitude: 10.0  (total duration in seconds)
Period: 1.0               (execute every 1 second)
Execute Periodic Effect on Application: true/false
```

`EGameplayEffectStackingPeriodPolicy` controls what happens to the period timer on stack add:
- `ResetOnSuccessfulApplication`: Timer resets to full period on each stack
- `NeverReset`: Timer continues uninterrupted

Period callbacks on the ASC:
```cpp
// Called on server when a periodic GE executes on self:
AbilitySystemComponent->OnPeriodicGameplayEffectExecuteDelegateOnSelf.AddUObject(
    this, &AMyCharacter::OnPeriodicEffectExecuted);
```

---

## Conditional Effects (`FConditionalGameplayEffect`)

Apply secondary effects only when a primary execution succeeds:

```cpp
// In GE asset, set up Executions[0].ConditionalGameplayEffects:
FConditionalGameplayEffect ConditionalEntry;
ConditionalEntry.EffectClass = UMyBurnEffect::StaticClass();
ConditionalEntry.RequiredSourceTags.AddTag(
    FGameplayTag::RequestGameplayTag("Ability.FireType")); // Source must have this tag
```

The conditional effect is applied to the same target as the parent execution.

---

## Immunity

Block specific GEs from applying using the `UImmunityGameplayEffectComponent` (UE 5.3+).
In the GE asset, add this component and configure its tag query to match incoming GE source tags.

`GrantedApplicationImmunityTags` (deprecated since UE 5.3) was the legacy property for this.
New code should use `UImmunityGameplayEffectComponent` in the GE component list instead.

When an ASC has this GE active, any incoming GE matching the immunity query is blocked.
The `OnImmunityBlockGameplayEffectDelegate` fires on the ASC when a block occurs:

```cpp
AbilitySystemComponent->OnImmunityBlockGameplayEffectDelegate.AddUObject(
    this, &AMyCharacter::OnImmunityBlockGE);

void AMyCharacter::OnImmunityBlockGE(
    const FGameplayEffectSpec& BlockedSpec,
    const FActiveGameplayEffect* ImmunityEffect)
{
    // Log or trigger "immune" visual feedback
}
```

---

## Querying Active Effects

```cpp
// Get all active effect handles matching a query:
FGameplayEffectQuery Query;
Query.EffectTagQuery = FGameplayTagQuery::MakeQuery_MatchAnyTags(
    FGameplayTagContainer(FGameplayTag::RequestGameplayTag("Effect.Type.Buff")));

TArray<FActiveGameplayEffectHandle> Handles =
    AbilitySystemComponent->GetActiveEffects(Query);

// Get time remaining:
TArray<float> Remaining = AbilitySystemComponent->GetActiveEffectsTimeRemaining(Query);

// Remove all matching:
AbilitySystemComponent->RemoveActiveEffects(Query);

// Remove those with specific granted tags:
AbilitySystemComponent->RemoveActiveEffectsWithGrantedTags(
    FGameplayTagContainer(FGameplayTag::RequestGameplayTag("Buff.Speed")));

// Remove those with specific applied source tags:
AbilitySystemComponent->RemoveActiveEffectsWithSourceTags(
    FGameplayTagContainer(FGameplayTag::RequestGameplayTag("Effect.Poison")));
```

---

## Effect Application Callbacks

```cpp
// Any GE applied to self (server-side):
AbilitySystemComponent->OnGameplayEffectAppliedDelegateToSelf.AddUObject(
    this, &AMyCharacter::OnEffectApplied);

void AMyCharacter::OnEffectApplied(
    UAbilitySystemComponent* Source,
    const FGameplayEffectSpec& Spec,
    FActiveGameplayEffectHandle Handle)
{
    // React to any applied effect
    // Use Spec.Def->DurationPolicy to determine if instant/duration/infinite
    UE_LOG(LogTemp, Log, TEXT("Effect applied: %s"), *GetNameSafe(Spec.Def));
}

// Duration-based GE added (client + server):
AbilitySystemComponent->OnActiveGameplayEffectAddedDelegateToSelf.AddUObject(
    this, &AMyCharacter::OnActiveEffectAdded);

// GE removed — subscribe per active effect handle after applying:
FOnActiveGameplayEffectRemoved_Info* RemovalDelegate =
    AbilitySystemComponent->OnGameplayEffectRemoved_InfoDelegate(ActiveHandle);
if (RemovalDelegate)
{
    RemovalDelegate->AddUObject(this, &AMyCharacter::OnEffectRemoved);
}

void AMyCharacter::OnEffectRemoved(const FGameplayEffectRemovalInfo& RemovalInfo)
{
    // RemovalInfo.ActiveEffect holds the effect that was removed
    // RemovalInfo.bPrematureRemoval is true if removed before natural expiry
}
```

---

## UE5.3+ Modular GE Components

Since UE 5.3, `UGameplayEffect` uses `UGameplayEffectComponents` instead of monolithic
properties for many behaviors. Legacy properties still work (the system auto-upgrades via
`PostCDOCompiled`), but new GEs should prefer the component approach in the editor.

Key components include:
- `UAdditionalEffectsGameplayEffectComponent` — conditional and chained GEs
- `UBlockAbilityTagsGameplayEffectComponent` — block abilities while active
- `UTargetTagsGameplayEffectComponent` — grant tags to the target actor while active
- `UImmunityGameplayEffectComponent` — immunity to incoming GEs
- `UTargetTagRequirementsGameplayEffectComponent` — required/ignored tags on target for application/continuation

These replace what was previously set directly on `UGameplayEffect` properties. When
reading older code, map properties like `GrantedTags`, `InhibitionTags`, and
`ApplicationTagRequirements` to their respective component equivalents.
