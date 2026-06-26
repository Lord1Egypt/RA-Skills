# Behavior Tree Patterns

Common, reusable Behavior Tree structures for UE AI. Each pattern shows the tree topology, required Blackboard keys, and key C++ touchpoints from the AIModule source.

---

## Blackboard Keys (Common Set)

Define these in your `UBlackboardData` asset as a baseline. Extend per-character:

| Key Name | Type | Description |
|----------|------|-------------|
| `TargetActor` | Object (AActor) | Current enemy/target |
| `LastKnownLocation` | Vector | Last confirmed target location |
| `PatrolLocation` | Vector | Current patrol waypoint |
| `HomeLocation` | Vector | Spawn/home position |
| `InvestigateLocation` | Vector | Sound/sight disturbance location |
| `CoverLocation` | Vector | EQS-found cover position |
| `IsAlerted` | Bool | Has AI been alerted |
| `IsInCombat` | Bool | Actively fighting |
| `AttackCooldown` | Bool | Tag cooldown sentinel (used with BTDecorator_TagCooldown) |
| `StateFloat` | Float | Generic float (health %, threat score, etc.) |

---

## Pattern 1: Patrol / Chase / Attack

Classic three-phase NPC AI. The root Selector tries Combat first (highest priority), then Alerted search, then idle patrol.

```
Root [Selector]
├── [Sequence] "Combat" — BTDecorator_Blackboard(TargetActor, IsSet, AbortBoth)
│   ├── [Service] UpdateTarget (0.3s interval — re-scores nearest hostile)
│   ├── BTTask_MoveTo (TargetActor key, AcceptRadius=150)
│   └── BTTask_RunEQSQuery (AttackPositionQuery → CoverLocation)
│       └── [Sequence] "Attack Sequence"
│           ├── BTTask_RotateToFaceBBEntry (TargetActor)
│           └── MyBTTask_FireWeapon
│               └── BTDecorator_Cooldown (2.0s, AbortSelf)
│
├── [Sequence] "Investigate" — BTDecorator_Blackboard(InvestigateLocation, IsSet, AbortBoth)
│   ├── BTTask_MoveTo (InvestigateLocation, AcceptRadius=100)
│   ├── BTTask_Wait (2.0s)
│   └── MyBTTask_ClearInvestigateLocation
│
└── [Sequence] "Patrol"
    ├── [Service] PickNextPatrolPoint (5.0s interval, calls EQS or patrol spline)
    ├── BTTask_MoveTo (PatrolLocation, AcceptRadius=50)
    └── BTTask_Wait (WaitBlackboardTime key="PatrolWait")
```

### Perception Wiring

`OnTargetPerceptionUpdated` on the AIController:

```cpp
void AEnemyAIController::OnTargetPerceptionUpdated(AActor* Actor, FAIStimulus Stimulus)
{
    UBlackboardComponent* BB = GetBlackboardComponent();

    if (Stimulus.WasSuccessfullySensed())
    {
        if (Stimulus.Type == UAISense::GetSenseID<UAISense_Sight>())
        {
            BB->SetValueAsObject(TEXT("TargetActor"), Actor);
            BB->SetValueAsVector(TEXT("LastKnownLocation"), Stimulus.StimulusLocation);
        }
        else if (Stimulus.Type == UAISense::GetSenseID<UAISense_Hearing>())
        {
            // Only set investigate location if we don't already have a visual target
            if (!BB->GetValueAsObject(TEXT("TargetActor")))
            {
                BB->SetValueAsVector(TEXT("InvestigateLocation"), Stimulus.StimulusLocation);
            }
        }
    }
    else
    {
        // Lost sight — remember last known location
        BB->SetValueAsVector(TEXT("LastKnownLocation"), Stimulus.StimulusLocation);
        // Do NOT clear TargetActor — let the search phase handle it
    }
}
```

---

## Pattern 2: Combat with Cover and Repositioning

AI actively seeks cover, attacks from cover, repositions when suppressed.

```
Root [Selector]
├── [Sequence] "Take Cover" — BTDecorator_Blackboard(IsInCombat, IsSet, AbortBoth)
│   ├── [Service] RunEQSCoverService (1.0s — updates CoverLocation)
│   ├── BTTask_MoveTo (CoverLocation, AcceptRadius=80)
│   └── [Selector] "Attack or Wait"
│       ├── [Sequence] "Peek and Shoot"
│       │   ├── BTDecorator_Blackboard(TargetActor, IsSet)
│       │   ├── BTTask_RotateToFaceBBEntry (TargetActor)
│       │   └── MyBTTask_FireWeapon
│       │       └── BTDecorator_Cooldown (1.5s)
│       └── BTTask_Wait (1.0s)  ← suppress-wait when no LoS
│
└── [Sequence] "Find Enemy"
    ├── BTTask_RunEQSQuery (LastKnownLocationSearch)
    ├── BTTask_MoveTo (PatrolLocation, AcceptRadius=100)
    └── BTTask_Wait (3.0s)
```

### Cover Query Service (C++)

```cpp
// BTService_FindCover.cpp
void UBTService_FindCover::TickNode(
    UBehaviorTreeComponent& OwnerComp, uint8* NodeMemory, float DeltaSeconds)
{
    AAIController* Controller = OwnerComp.GetAIOwner();
    UBlackboardComponent* BB = OwnerComp.GetBlackboardComponent();

    if (!CoverQuery) { return; }

    FEnvQueryRequest Request(CoverQuery, Controller);
    Request.Execute(EEnvQueryRunMode::RandomBest25Pct,
        FQueryFinishedSignature::CreateWeakLambda(Controller,
        [BB](TSharedPtr<FEnvQueryResult> Result)
        {
            if (Result.IsValid() && Result->IsSuccessful())
            {
                BB->SetValueAsVector(TEXT("CoverLocation"), Result->GetItemAsLocation(0));
            }
        }));
}
```

---

## Pattern 3: Flee (Health Threshold Trigger)

AI retreats when health drops below a threshold, uses EQS to find a safe escape point.

```
Root [Selector]
├── [Sequence] "Flee" — MyBTDecorator_HealthBelow(30%, AbortBoth)
│   ├── BTTask_RunEQSQuery (FleePointQuery → PatrolLocation)
│   │    ← FleePointQuery: DonutGenerator(self, minR=500, maxR=2000)
│   │       + Trace test (not visible from TargetActor location)
│   │       + Pathfinding test (reachable)
│   ├── BTTask_MoveTo (PatrolLocation, AcceptRadius=100, AllowPartialPath=true)
│   └── BTTask_Wait (5.0s)  ← catch breath before re-evaluating
│
└── [Sequence] "Normal Combat" (same as Pattern 1 combat branch)
```

### Health Threshold Decorator (C++)

```cpp
// BTDecorator_HealthBelow.h
UCLASS()
class UBTDecorator_HealthBelow : public UBTDecorator
{
    GENERATED_BODY()
public:
    UBTDecorator_HealthBelow() { bAllowAbortLowerPri = true; bAllowAbortChildNodes = true; }

    UPROPERTY(EditAnywhere, Category = "Condition", meta = (ClampMin = 0, ClampMax = 1))
    float HealthThresholdNormalized = 0.3f;

protected:
    virtual bool CalculateRawConditionValue(
        UBehaviorTreeComponent& OwnerComp, uint8* NodeMemory) const override
    {
        APawn* Pawn = OwnerComp.GetAIOwner()->GetPawn();
        IMyHealthInterface* HealthInterface = Cast<IMyHealthInterface>(Pawn);
        if (!HealthInterface) { return false; }
        return HealthInterface->GetNormalizedHealth() < HealthThresholdNormalized;
    }
};
```

---

## Pattern 4: Investigate Sound / Disturbance

AI pauses current activity, moves to sound source, looks around, then resumes.

```
Root [Selector]
├── [Sequence] "Investigate" — BTDecorator_Blackboard(InvestigateLocation, IsSet, AbortBoth)
│   ├── BTTask_MoveTo (InvestigateLocation, AcceptRadius=100)
│   ├── MyBTTask_LookAround (rotates pawn 360° over 3s)
│   │   └── BTDecorator_TimeLimit (5.0s) ← abort if takes too long
│   └── MyBTTask_ClearBBKey (InvestigateLocation)
│        ← clears BB so decorator deactivates and lower priority resumes
│
├── [Sequence] "Combat" (as before)
│
└── [Sequence] "Patrol" (as before)
```

### LookAround Task (C++)

```cpp
// BTTask_LookAround.cpp
EBTNodeResult::Type UBTTask_LookAround::ExecuteTask(
    UBehaviorTreeComponent& OwnerComp, uint8* NodeMemory)
{
    auto* Mem = CastInstanceNodeMemory<FBTLookAroundMemory>(NodeMemory);
    Mem->ElapsedTime = 0.f;
    Mem->StartYaw = OwnerComp.GetAIOwner()->GetPawn()->GetActorRotation().Yaw;
    return EBTNodeResult::InProgress;
}

void UBTTask_LookAround::TickTask(
    UBehaviorTreeComponent& OwnerComp, uint8* NodeMemory, float DeltaSeconds)
{
    auto* Mem = CastInstanceNodeMemory<FBTLookAroundMemory>(NodeMemory);
    Mem->ElapsedTime += DeltaSeconds;

    float NewYaw = Mem->StartYaw + (Mem->ElapsedTime / LookDuration) * 360.f;
    OwnerComp.GetAIOwner()->SetFocalPoint(
        OwnerComp.GetAIOwner()->GetPawn()->GetActorLocation() +
        FRotator(0.f, NewYaw, 0.f).Vector() * 500.f);

    if (Mem->ElapsedTime >= LookDuration)
    {
        OwnerComp.GetAIOwner()->ClearFocus(EAIFocusPriority::Gameplay);
        FinishLatentTask(OwnerComp, EBTNodeResult::Succeeded);
    }
}
```

---

## Pattern 5: Patrol Along Spline

Looping patrol along a spline, with stop duration at each point.

```
Root [Sequence]
└── [Sequence + BTDecorator_Loop(NumLoops=0)] "Patrol Loop"
    ├── MyBTTask_GetNextSplinePoint (writes PatrolLocation + PatrolWaitTime)
    ├── BTTask_MoveTo (PatrolLocation, AcceptRadius=50)
    └── BTTask_WaitBlackboardTime (BlackboardKey=PatrolWaitTime)
```

### GetNextSplinePoint Task (C++)

```cpp
EBTNodeResult::Type UBTTask_GetNextSplinePoint::ExecuteTask(
    UBehaviorTreeComponent& OwnerComp, uint8* NodeMemory)
{
    UBlackboardComponent* BB = OwnerComp.GetBlackboardComponent();
    AAIController* Controller = OwnerComp.GetAIOwner();

    if (!IsValid(PatrolSplineActor)) { return EBTNodeResult::Failed; }

    USplineComponent* Spline = PatrolSplineActor->FindComponentByClass<USplineComponent>();
    if (!Spline) { return EBTNodeResult::Failed; }

    int32 NumPoints = Spline->GetNumberOfSplinePoints();
    int32 CurrentIdx = BB->GetValueAsInt(TEXT("PatrolIndex"));
    int32 NextIdx = (CurrentIdx + 1) % NumPoints;

    BB->SetValueAsInt(TEXT("PatrolIndex"), NextIdx);
    BB->SetValueAsVector(TEXT("PatrolLocation"),
        Spline->GetLocationAtSplinePoint(NextIdx, ESplineCoordinateSpace::World));
    BB->SetValueAsFloat(TEXT("PatrolWaitTime"), WaitTimeAtPoint);

    return EBTNodeResult::Succeeded;
}
```

---

## Pattern 6: Squad AI with Shared Blackboard

Multiple AI agents share awareness via instance-synced blackboard keys.

**Setup**: Mark `TargetActor` and `AlertLevel` as "Instance Synced" in `UBlackboardData`.

When any squad member's AI controller updates these keys, `UAISystem` propagates the change to all blackboards sharing the same asset (see `UBlackboardComponent::SetValue` template for the sync loop).

```cpp
// Squad leader sets target → all squad members receive it
void ASquadLeaderAIController::OnTargetPerceptionUpdated(AActor* Actor, FAIStimulus Stimulus)
{
    if (Stimulus.WasSuccessfullySensed())
    {
        // Setting a synced key broadcasts to all squad members sharing this BB asset
        GetBlackboardComponent()->SetValueAsObject(TEXT("TargetActor"), Actor);
        GetBlackboardComponent()->SetValueAsFloat(TEXT("AlertLevel"), 1.0f);
    }
}
```

The BT on each squad member reacts independently to the shared `TargetActor` key via `BTDecorator_Blackboard`.

---

## Pattern 7: Message-Driven Task (WaitForMessage)

Used when a task needs to wait for an external event (animation notify, ability end, timer) rather than polling.

```cpp
EBTNodeResult::Type UBTTask_PlayMontage::ExecuteTask(
    UBehaviorTreeComponent& OwnerComp, uint8* NodeMemory)
{
    ACharacter* Character = Cast<ACharacter>(OwnerComp.GetAIOwner()->GetPawn());
    if (!Character || !MontageToPlay) { return EBTNodeResult::Failed; }

    // Register to receive a specific message name
    WaitForMessage(OwnerComp, TEXT("MontageCompleted"));
    WaitForMessage(OwnerComp, TEXT("MontageFailed"));

    // Start the montage
    Character->GetMesh()->GetAnimInstance()->Montage_Play(MontageToPlay);

    return EBTNodeResult::InProgress;
}

void UBTTask_PlayMontage::OnMessage(
    UBehaviorTreeComponent& OwnerComp, uint8* NodeMemory,
    FName Message, int32 RequestID, bool bSuccess)
{
    StopWaitingForMessages(OwnerComp);
    FinishLatentTask(OwnerComp,
        (Message == TEXT("MontageCompleted")) ? EBTNodeResult::Succeeded : EBTNodeResult::Failed);
}

// Sender side (e.g., AnimNotify or ability):
// UAIBlueprintHelperLibrary::SendAIMessage(Pawn, TEXT("MontageCompleted"), nullptr, true);
// Or from C++:
// UBehaviorTreeComponent* BTComp = Cast<UBehaviorTreeComponent>(Controller->GetBrainComponent());
// if (BTComp) { BTComp->HandleMessage(FAIMessage(TEXT("MontageCompleted"), nullptr, true)); }
```

---

## Node Memory Pattern

For tasks that store per-instance runtime data (not shared across AI using the same tree asset):

```cpp
struct FBTMyTaskMemory
{
    FAIRequestID MoveRequestID;
    float ElapsedTime = 0.f;
    TWeakObjectPtr<UMyComponent> CachedComp;
};

UCLASS()
class UBTTask_MyTask : public UBTTaskNode
{
    // ...
    virtual uint16 GetInstanceMemorySize() const override
    {
        return sizeof(FBTMyTaskMemory);
    }
};

// In ExecuteTask:
FBTMyTaskMemory* Mem = CastInstanceNodeMemory<FBTMyTaskMemory>(NodeMemory);
new(Mem) FBTMyTaskMemory(); // placement-new to initialize
Mem->ElapsedTime = 0.f;
```

---

## Decorator Abort Modes

| FlowAbortMode | Behavior |
|---------------|----------|
| `None` | Decorator never aborts running tasks |
| `Self` | Aborts tasks within its own subtree if condition changes |
| `LowerPriority` | Aborts lower-priority branches when condition becomes true |
| `Both` | Combination of Self and LowerPriority |

Most reactive decorators (Blackboard, CanSeeTarget) should use `Both` so the tree re-evaluates when the condition changes in either direction.

Set via:
```cpp
FlowAbortMode = EBTFlowAbortMode::Both;
bAllowAbortLowerPri = true;
bAllowAbortChildNodes = true;
```

Then call `ConditionalFlowAbort` from external event handlers to trigger re-evaluation:
```cpp
// In perception callback or timer:
ConditionalFlowAbort(OwnerComp, EBTDecoratorAbortRequest::ConditionResultChanged);
```
