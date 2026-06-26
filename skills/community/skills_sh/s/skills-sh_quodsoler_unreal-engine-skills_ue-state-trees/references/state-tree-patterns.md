# State Tree Patterns

Complete code templates for custom State Tree nodes. All signatures are source-verified from UE headers.

---

## Custom Task Template

```cpp
// MyTimedTask.h
#pragma once
#include "StateTreeTaskBase.h"
#include "StateTreeExecutionContext.h"
#include "StateTreeLinker.h"
#include "MyTimedTask.generated.h"

USTRUCT()
struct FMyTimedTaskInstanceData
{
    GENERATED_BODY()

    UPROPERTY()
    float ElapsedTime = 0.f;

    UPROPERTY()
    bool bHasTriggered = false;
};

USTRUCT(meta=(DisplayName="My Timed Task"))
struct FMyTimedTask : public FStateTreeTaskBase
{
    GENERATED_BODY()

    // Required — framework uses this to allocate per-instance storage
    typedef FMyTimedTaskInstanceData FInstanceDataType;

    // Configuration (set in editor, shared across all instances)
    UPROPERTY(EditAnywhere, Category = "Parameter")
    float TriggerDelay = 3.0f;

    UPROPERTY(EditAnywhere, Category = "Parameter")
    FGameplayTag EventToSend;

    virtual EStateTreeRunStatus EnterState(FStateTreeExecutionContext& Context,
        const FStateTreeTransitionResult& Transition) const override
    {
        FInstanceDataType& Data = Context.GetInstanceData(*this);
        Data.ElapsedTime = 0.f;
        Data.bHasTriggered = false;
        return EStateTreeRunStatus::Running;
    }

    virtual EStateTreeRunStatus Tick(FStateTreeExecutionContext& Context,
        float DeltaTime) const override
    {
        FInstanceDataType& Data = Context.GetInstanceData(*this);
        Data.ElapsedTime += DeltaTime;

        if (!Data.bHasTriggered && Data.ElapsedTime >= TriggerDelay)
        {
            Data.bHasTriggered = true;
            Context.SendEvent(EventToSend, FConstStructView(), TEXT("MyTimedTask"));
            return EStateTreeRunStatus::Succeeded;
        }
        return EStateTreeRunStatus::Running;
    }

    virtual void ExitState(FStateTreeExecutionContext& Context,
        const FStateTreeTransitionResult& Transition) const override
    {
        // Cleanup if needed (stop audio, cancel async ops, etc.)
    }
};
```

### Task with External Data

```cpp
USTRUCT(meta=(DisplayName="Move To Target"))
struct FMoveToTargetTask : public FStateTreeTaskBase
{
    GENERATED_BODY()
    typedef FMoveToTargetInstanceData FInstanceDataType;

    // External data — linked at setup, accessed at runtime
    TStateTreeExternalDataHandle<FStateTreeActorContext,
        EStateTreeExternalDataRequirement::Required> ActorHandle;

    UPROPERTY(EditAnywhere)
    float AcceptanceRadius = 100.f;

    // Bindable input — editor can bind this to evaluator output
    UPROPERTY(EditAnywhere, Category = "Input")
    FVector TargetLocation = FVector::ZeroVector;

    virtual bool Link(FStateTreeLinker& Linker) override
    {
        Linker.LinkExternalData(ActorHandle);
        return true;
    }

    virtual EStateTreeRunStatus EnterState(FStateTreeExecutionContext& Context,
        const FStateTreeTransitionResult& Transition) const override
    {
        auto& ActorCtx = Context.GetExternalData(ActorHandle);
        AActor* Actor = ActorCtx.GetActor();
        if (!Actor) return EStateTreeRunStatus::Failed;

        // Start movement...
        return EStateTreeRunStatus::Running;
    }

    virtual EStateTreeRunStatus Tick(FStateTreeExecutionContext& Context,
        float DeltaTime) const override
    {
        auto& ActorCtx = Context.GetExternalData(ActorHandle);
        AActor* Actor = ActorCtx.GetActor();
        if (!Actor) return EStateTreeRunStatus::Failed;

        float Dist = FVector::Dist(Actor->GetActorLocation(), TargetLocation);
        return Dist <= AcceptanceRadius
            ? EStateTreeRunStatus::Succeeded : EStateTreeRunStatus::Running;
    }
};
```

---

## Custom Condition Template

```cpp
USTRUCT()
struct FHealthCheckConditionInstanceData
{
    GENERATED_BODY()

    // Bindable — connect to evaluator or context data in editor
    UPROPERTY(EditAnywhere, Category = "Input")
    float CurrentHealth = 100.f;
};

USTRUCT(meta=(DisplayName="Health Below Threshold"))
struct FHealthBelowThresholdCondition : public FStateTreeConditionBase
{
    GENERATED_BODY()
    typedef FHealthCheckConditionInstanceData FInstanceDataType;

    UPROPERTY(EditAnywhere, Category = "Parameter")
    float Threshold = 25.f;

    // TestCondition must be a PURE FUNCTION — no side effects
    // May be called multiple times per frame during transition evaluation
    virtual bool TestCondition(FStateTreeExecutionContext& Context) const override
    {
        const FInstanceDataType& Data = Context.GetInstanceData(*this);
        return Data.CurrentHealth < Threshold;
    }
};
```

---

## Evaluator Template

Evaluators run every tick before transitions. Use them to inject world data into the tree via property bindings.

```cpp
USTRUCT()
struct FNearestEnemyEvaluatorInstanceData
{
    GENERATED_BODY()

    // Output — bind task/condition inputs to these in the editor
    UPROPERTY(EditAnywhere, Category = "Output")
    TObjectPtr<AActor> NearestEnemy = nullptr;

    UPROPERTY(EditAnywhere, Category = "Output")
    float DistanceToNearest = MAX_FLT;

    // Internal cache
    float TimeSinceLastQuery = 0.f;
};

USTRUCT(meta=(DisplayName="Nearest Enemy Evaluator"))
struct FNearestEnemyEvaluator : public FStateTreeEvaluatorBase
{
    GENERATED_BODY()
    typedef FNearestEnemyEvaluatorInstanceData FInstanceDataType;

    UPROPERTY(EditAnywhere, Category = "Parameter")
    float QueryInterval = 0.5f;  // Don't query every frame

    TStateTreeExternalDataHandle<FStateTreeActorContext,
        EStateTreeExternalDataRequirement::Required> ActorHandle;

    virtual bool Link(FStateTreeLinker& Linker) override
    {
        Linker.LinkExternalData(ActorHandle);
        return true;
    }

    virtual void TreeStart(FStateTreeExecutionContext& Context) const override
    {
        FInstanceDataType& Data = Context.GetInstanceData(*this);
        Data.NearestEnemy = nullptr;
        Data.DistanceToNearest = MAX_FLT;
        Data.TimeSinceLastQuery = QueryInterval;  // Force immediate first query
    }

    virtual void Tick(FStateTreeExecutionContext& Context, float DeltaTime) const override
    {
        FInstanceDataType& Data = Context.GetInstanceData(*this);
        Data.TimeSinceLastQuery += DeltaTime;

        if (Data.TimeSinceLastQuery < QueryInterval) return;
        Data.TimeSinceLastQuery = 0.f;

        auto& ActorCtx = Context.GetExternalData(ActorHandle);
        AActor* Owner = ActorCtx.GetActor();
        if (!Owner) return;

        // Perform query (overlap, EQS, etc.)
        // Update Data.NearestEnemy and Data.DistanceToNearest
    }

    virtual void TreeStop(FStateTreeExecutionContext& Context) const override
    {
        FInstanceDataType& Data = Context.GetInstanceData(*this);
        Data.NearestEnemy = nullptr;
    }
};
```

---

## FStateTreeReference Setup

Use `FStateTreeReference` for linked assets and runtime parameter overrides:

```cpp
// In your component or controller
UPROPERTY(EditAnywhere, Category = "StateTree")
FStateTreeReference StateTreeRef;

void SetupStateTree(UStateTree* TreeAsset, float CustomAggroRange)
{
    StateTreeRef.SetStateTree(TreeAsset);
    StateTreeRef.SyncParameters();  // sync defaults from asset
    StateTreeRef.GetParameters().SetValueFloat(TEXT("AggroRange"), CustomAggroRange);

    StateTreeComp->SetStateTreeReference(StateTreeRef);
}

// Runtime variant swapping via FStateTreeReferenceOverrides
UPROPERTY(EditAnywhere)
FStateTreeReferenceOverrides TreeOverrides;

void SwitchToCombatVariant(FStateTreeReference& CombatRef)
{
    TreeOverrides.AddOverride(
        FGameplayTag::RequestGameplayTag("Variant.Combat"), CombatRef);
}
```

---

## Event Patterns

### Sending Events from External Systems

```cpp
// From perception callback
void AMyAIController::OnTargetPerceived(AActor* Target)
{
    FMyPerceptionPayload Payload;
    Payload.PerceivedActor = Target;
    Payload.ThreatLevel = CalculateThreat(Target);

    StateTreeComp->SendStateTreeEvent(
        FGameplayTag::RequestGameplayTag("AI.TargetPerceived"),
        FConstStructView::Make(Payload),
        TEXT("Perception"));
}
```

### Consuming Events in Tasks

```cpp
virtual EStateTreeRunStatus EnterState(FStateTreeExecutionContext& Context,
    const FStateTreeTransitionResult& Transition) const override
{
    // Iterate events pending in the queue; ConsumeEvent(Event) removes a specific event
    Context.ForEachEvent([&](const FStateTreeSharedEvent& SharedEvent)
    {
        const FStateTreeEvent& Event = *SharedEvent;
        if (Event.Tag == MyExpectedTag)
        {
            // Process payload from the triggering event
            Context.ConsumeEvent(SharedEvent);  // void — does not return bool
        }
        return EStateTreeLoopEvents::Continue;
    });
    return EStateTreeRunStatus::Running;
}
```

---

## Transition Design Patterns

### Event-Driven (decoupled, reactive)
Use `OnEvent` trigger with a GameplayTag. Best for external stimuli (perception, damage, game events). Set `bConsumeEventOnSelect = true` to prevent double-handling.

### Tick-Based with Conditions (polled)
Use `OnTick` trigger with conditions gating the transition. Best for continuous checks (distance thresholds, timer expiry). Keep conditions lightweight since they evaluate every frame.

### Completion-Based (sequential)
Use `OnStateCompleted` / `OnStateSucceeded` / `OnStateFailed` triggers. Best for linear state sequences where the next state depends on the previous state's outcome. Use `NextState` target for sequential flows.

### Priority Escalation
Set `Critical` priority on interrupt transitions (damage, death) so they override normal transitions regardless of state depth. Lower priorities for optional transitions (idle variations).
