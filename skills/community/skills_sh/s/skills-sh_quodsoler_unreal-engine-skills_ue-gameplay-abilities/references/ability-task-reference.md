# Ability Task Reference

Common built-in `UAbilityTask` subclasses and how to create custom tasks.
Ability tasks extend ability execution across multiple frames using internal latent logic.

All tasks must be called from within `ActivateAbility` (or from within other tasks).
Tasks broadcast results via dynamic delegates. When the task completes, call `EndAbility`
if the ability is meant to end at that point.

---

## How Ability Tasks Work

1. Create the task via a static factory function (never call `new` directly).
2. Bind delegates for each outcome (OnCompleted, OnInterrupted, etc.).
3. Call `ReadyForActivation()` to start the task.
4. The task runs asynchronously; the ability remains active but yields.
5. In delegate callbacks, perform follow-up logic and call `EndAbility` when done.

```cpp
// Typical task usage in ActivateAbility:
void UMyAbility::ActivateAbility(...)
{
    if (!CommitAbility(Handle, ActorInfo, ActivationInfo))
    {
        EndAbility(Handle, ActorInfo, ActivationInfo, true, true);
        return;
    }

    UAbilityTask_PlayMontageAndWait* Task =
        UAbilityTask_PlayMontageAndWait::CreatePlayMontageAndWaitProxy(
            this, NAME_None, AttackMontage, 1.f);

    Task->OnCompleted.AddDynamic(this, &UMyAbility::OnMontageCompleted);
    Task->OnInterrupted.AddDynamic(this, &UMyAbility::OnMontageInterrupted);
    Task->OnCancelled.AddDynamic(this, &UMyAbility::OnMontageCancelled);
    Task->ReadyForActivation();
}

void UMyAbility::OnMontageCompleted()
{
    EndAbility(CurrentSpecHandle, CurrentActorInfo, CurrentActivationInfo, true, false);
}

void UMyAbility::OnMontageInterrupted()
{
    EndAbility(CurrentSpecHandle, CurrentActorInfo, CurrentActivationInfo, true, true);
}
```

---

## UAbilityTask_PlayMontageAndWait

Plays an `AnimMontage` on the avatar actor's skeletal mesh and waits for it to finish.

```cpp
#include "Abilities/Tasks/AbilityTask_PlayMontageAndWait.h"

UAbilityTask_PlayMontageAndWait* Task =
    UAbilityTask_PlayMontageAndWait::CreatePlayMontageAndWaitProxy(
        this,              // OwningAbility
        NAME_None,         // Task instance name (NAME_None = auto)
        AttackMontage,     // UAnimMontage* to play
        1.f,               // Rate
        NAME_None,         // StartSection (NAME_None = start from beginning)
        false,             // bStopWhenAbilityEnds
        1.f);              // AnimRootMotionTranslationScale

Task->OnCompleted.AddDynamic(this, &UMyAbility::OnMontageCompleted);
Task->OnBlendOut.AddDynamic(this, &UMyAbility::OnMontageBlendOut);
Task->OnInterrupted.AddDynamic(this, &UMyAbility::OnMontageInterrupted);
Task->OnCancelled.AddDynamic(this, &UMyAbility::OnMontageCancelled);
Task->ReadyForActivation();
```

Delegates:
- `OnCompleted`: Montage finished playing
- `OnBlendOut`: Montage started blending out
- `OnInterrupted`: Montage was interrupted by another montage
- `OnCancelled`: Task was cancelled (EndAbility called while running)

---

## UAbilityTask_WaitGameplayEvent

Waits for a `FGameplayEventData` to be sent via `HandleGameplayEvent` on the ASC.
Common use: waiting for an animation notify to trigger (e.g., `Event.Montage.Attack.Hit`).

```cpp
#include "Abilities/Tasks/AbilityTask_WaitGameplayEvent.h"

FGameplayTag EventTag = FGameplayTag::RequestGameplayTag("Event.Montage.Attack.Hit");

UAbilityTask_WaitGameplayEvent* Task =
    UAbilityTask_WaitGameplayEvent::WaitGameplayEvent(
        this,
        EventTag,
        nullptr,  // OptionalExternalTarget (null = use self ASC)
        true,     // TriggerOnce (false = keep listening)
        true);    // OnlyMatchExact

Task->EventReceived.AddDynamic(this, &UMyAbility::OnAttackHitEvent);
Task->ReadyForActivation();
```

Sending the event (e.g., from an `AnimNotify`):
```cpp
// In AnimNotify or character code:
FGameplayEventData EventData;
EventData.Instigator = GetOwner();
UAbilitySystemBlueprintLibrary::SendGameplayEventToActor(
    GetOwner(),
    FGameplayTag::RequestGameplayTag("Event.Montage.Attack.Hit"),
    EventData);
```

Delegate: `EventReceived(FGameplayEventData Payload)`

---

## UAbilityTask_WaitDelay

Waits for a fixed duration and then fires a callback. Equivalent to a GAS-aware timer.

```cpp
#include "Abilities/Tasks/AbilityTask_WaitDelay.h"

UAbilityTask_WaitDelay* Task =
    UAbilityTask_WaitDelay::WaitDelay(this, 2.f); // 2 second delay

Task->OnFinish.AddDynamic(this, &UMyAbility::OnDelayFinished);
Task->ReadyForActivation();
```

Delegate: `OnFinish()`

---

## UAbilityTask_WaitTargetData

Spawns a `AGameplayAbilityTargetActor` to gather targeting information (line trace,
sphere trace, actor selection, etc.) and returns `FGameplayAbilityTargetDataHandle`.

```cpp
#include "Abilities/Tasks/AbilityTask_WaitTargetData.h"
#include "Abilities/GameplayAbilityTargetActor_SingleLineTrace.h"

UAbilityTask_WaitTargetData* Task =
    UAbilityTask_WaitTargetData::WaitTargetData(
        this,
        NAME_None,
        EGameplayTargetingConfirmation::Instant, // Instant, UserConfirmed, Custom, etc.
        AGameplayAbilityTargetActor_SingleLineTrace::StaticClass());

Task->ValidData.AddDynamic(this, &UMyAbility::OnValidTargetData);
Task->Cancelled.AddDynamic(this, &UMyAbility::OnTargetCancelled);
Task->ReadyForActivation();
```

Targeting confirmation modes:
| Mode | Behavior |
|------|----------|
| `Instant` | Confirms immediately upon spawn |
| `UserConfirmed` | Waits for `SendGameplayEvent` with confirm tag |
| `Custom` | Custom confirmation logic in the TargetActor |
| `CustomMulti` | Confirms multiple targets over time |

Delegate `ValidData(FGameplayAbilityTargetDataHandle Data)`:
```cpp
void UMyAbility::OnValidTargetData(const FGameplayAbilityTargetDataHandle& Data)
{
    // Apply effect to targets
    FGameplayEffectSpecHandle SpecHandle = MakeOutgoingGameplayEffectSpec(DamageEffect, Level);
    ApplyGameplayEffectSpecToTarget(CurrentSpecHandle, CurrentActorInfo,
        CurrentActivationInfo, SpecHandle, Data);
    EndAbility(CurrentSpecHandle, CurrentActorInfo, CurrentActivationInfo, true, false);
}
```

---

## UAbilityTask_WaitAttributeChange

Waits for an attribute to cross a threshold or change at all.

```cpp
#include "Abilities/Tasks/AbilityTask_WaitAttributeChange.h"

UAbilityTask_WaitAttributeChange* Task =
    UAbilityTask_WaitAttributeChange::WaitForAttributeChange(
        this,
        UMyHealthSet::GetHealthAttribute(),
        FGameplayTag(),    // WithTag: optional, only trigger if ASC has this tag
        FGameplayTag(),    // WithoutTag: only trigger if ASC lacks this tag
        true);             // TriggerOnce

Task->OnChange.AddDynamic(this, &UMyAbility::OnHealthChanged);
Task->ReadyForActivation();
```

Delegate: `OnChange()`

For threshold-based (separate class — `UAbilityTask_WaitAttributeChangeThreshold`):
```cpp
#include "Abilities/Tasks/AbilityTask_WaitAttributeChangeThreshold.h"

UAbilityTask_WaitAttributeChangeThreshold* Task =
    UAbilityTask_WaitAttributeChangeThreshold::WaitForAttributeChangeThreshold(
        this,
        UMyHealthSet::GetHealthAttribute(),
        EWaitAttributeChangeComparison::LessThan,
        0.3f,    // Compare against: below 30%
        false,   // bTriggerOnce
        nullptr);

Task->OnChange.AddDynamic(this, &UMyAbility::OnHealthBelowThreshold);
Task->ReadyForActivation();
```

Delegate: `OnChange(bool bMatchesComparison, float CurrentValue)`

---

## UAbilityTask_WaitGameplayEffectApplied

Fires when a GameplayEffect matching specified tag requirements is applied to a target.

```cpp
#include "Abilities/Tasks/AbilityTask_WaitGameplayEffectApplied.h"

FGameplayTargetDataFilterHandle FilterHandle;
FGameplayTagRequirements SourceTagReqs;
FGameplayTagRequirements TargetTagReqs;
FGameplayTagRequirements AssetTagReqs;    // Tags the GE asset itself must have
FGameplayTagRequirements GrantedTagReqs; // Tags the GE grants to the target

UAbilityTask_WaitGameplayEffectApplied_Self* Task =
    UAbilityTask_WaitGameplayEffectApplied_Self::WaitGameplayEffectAppliedToSelf(
        this,
        FilterHandle,
        SourceTagReqs,
        TargetTagReqs,
        AssetTagReqs,
        GrantedTagReqs,
        false /*TriggerOnce*/,
        nullptr /*OptionalExternalOwner*/,
        false /*ListenForPeriodicEffect*/);

Task->OnApplied.AddDynamic(this, &UMyAbility::OnEffectApplied);
Task->ReadyForActivation();
```

---

## Creating a Custom Ability Task

```cpp
// MyAbilityTask_WaitInputRelease.h
#pragma once
#include "Abilities/Tasks/AbilityTask.h"
#include "MyAbilityTask_WaitInputRelease.generated.h"

DECLARE_DYNAMIC_MULTICAST_DELEGATE(FOnInputReleased);

UCLASS()
class UMyAbilityTask_WaitInputRelease : public UAbilityTask
{
    GENERATED_BODY()
public:
    // Factory function: always use a static factory, never construct directly
    UFUNCTION(BlueprintCallable, Category = "Ability|Tasks",
        meta = (HidePin = "OwningAbility", DefaultToSelf = "OwningAbility",
                BlueprintInternalUseOnly = "true"))
    static UMyAbilityTask_WaitInputRelease* WaitInputRelease(
        UGameplayAbility* OwningAbility,
        bool bTestAlreadyReleased = false);

    UPROPERTY(BlueprintAssignable)
    FOnInputReleased OnReleased;

    virtual void Activate() override;
    virtual void TickTask(float DeltaTime) override;
    virtual void OnDestroy(bool bInOwnerFinished) override;

private:
    bool bStartedAlreadyReleased = false;
};
```

```cpp
// MyAbilityTask_WaitInputRelease.cpp
#include "MyAbilityTask_WaitInputRelease.h"
#include "AbilitySystemComponent.h"

UMyAbilityTask_WaitInputRelease* UMyAbilityTask_WaitInputRelease::WaitInputRelease(
    UGameplayAbility* OwningAbility,
    bool bTestAlreadyReleased)
{
    UMyAbilityTask_WaitInputRelease* Task =
        NewAbilityTask<UMyAbilityTask_WaitInputRelease>(OwningAbility);
    Task->bStartedAlreadyReleased = bTestAlreadyReleased;
    return Task;
}

void UMyAbilityTask_WaitInputRelease::Activate()
{
    // Enable ticking so we can poll input state
    bTickingTask = true;
}

void UMyAbilityTask_WaitInputRelease::TickTask(float DeltaTime)
{
    // GetAbilitySpecHandle and AbilitySystemComponent come from UAbilityTask base
    if (AbilitySystemComponent.IsValid())
    {
        const FGameplayAbilitySpec* Spec =
            AbilitySystemComponent->FindAbilitySpecFromHandle(GetAbilitySpecHandle());
        if (Spec && !Spec->InputPressed)
        {
            if (ShouldBroadcastAbilityTaskDelegates())
            {
                OnReleased.Broadcast();
            }
            EndTask();
        }
    }
}

void UMyAbilityTask_WaitInputRelease::OnDestroy(bool bInOwnerFinished)
{
    Super::OnDestroy(bInOwnerFinished);
}
```

Usage in an ability:
```cpp
UMyAbilityTask_WaitInputRelease* Task =
    UMyAbilityTask_WaitInputRelease::WaitInputRelease(this);
Task->OnReleased.AddDynamic(this, &UMyChargeAbility::OnInputReleased);
Task->ReadyForActivation();
```

---

## Task Lifecycle Notes

- Tasks are automatically cleaned up when `EndAbility` or `CancelAbility` is called.
- Call `EndTask()` inside the task when done; do not call `delete`.
- `ShouldBroadcastAbilityTaskDelegates()` guards against broadcasting after the ability ends.
- `bTickingTask = true` must be set in `Activate()` to enable `TickTask`. Default is false.
- `NewAbilityTask<T>()` is the correct factory; never use `NewObject<T>()` for tasks.

---

## Task Execution Flow

```
ActivateAbility()
    └── Task::WaitXxx() (static factory)
    └── Bind delegates
    └── Task::ReadyForActivation()
            └── Task::Activate() [task starts its internal logic]
                    └── (async frames pass)
                    └── Event fires → delegate broadcast
                            └── Ability callback runs gameplay logic
                            └── EndAbility() called
                                    └── Task::OnDestroy() cleanup
```

---

## Common Task Mistakes

**Not calling ReadyForActivation:** The task is created but never starts. Always call this after
binding delegates.

**Binding delegates after ReadyForActivation:** Some tasks fire synchronously in `Activate()`
(e.g., `WaitDelay` with 0 duration). Bind delegates before calling `ReadyForActivation`.

**Calling EndAbility inside a task without ending the task first:** The task will linger.
Let `EndAbility` clean it up, or call `EndTask()` explicitly if the task should stop without
ending the ability.

**Broadcasting delegates after ability ends:** Always check `ShouldBroadcastAbilityTaskDelegates()`
before broadcasting inside `TickTask` or callback functions to avoid operating on a cleaned-up
ability.

**Tick-heavy tasks in non-instanced abilities:** If `InstancingPolicy` is `NonInstanced`, the
CDO runs the ability. Ticking tasks on a CDO can produce shared state issues. Use
`InstancedPerActor` or `InstancedPerExecution` when using ticking tasks.
