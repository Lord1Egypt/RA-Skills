# EQS Reference

Environment Query System (EQS) generator and test configurations for common AI spatial reasoning tasks.

---

## Architecture Overview

```
UEnvQuery (Data Asset)
  └── Options (array of UEnvQueryOption)
        ├── Generator — produces candidate items (locations or actors)
        └── Tests (array) — filter and score items
              ├── Filter: Discard items that fail the condition
              └── Score: Weight items by test result
```

Key classes:
- `UEnvQuery` — the query asset (inherits `UDataAsset`)
- `UEnvQueryManager` — subsystem that executes queries
- `FEnvQueryResult` — results: `GetItemAsLocation(0)`, `GetItemAsActor(0)`, `GetRawStatusDesc()`
- `UEnvQueryContext_Querier` — built-in context: the AI pawn running the query
- `UEnvQueryContext_Item` — built-in context: each candidate item (used in item-relative tests)

---

## Generators

### SimpleGrid (Point Grid)

Generates a uniform grid of points on the NavMesh around a center context.

| Property | Type | Description |
|----------|------|-------------|
| `GridHalfSize` | Float | Half extent of the grid (cm). 500 = 10x10 at 100cm spacing |
| `SpaceBetween` | Float | Spacing between points (cm) |
| `GenerateAroundActor` | Context | Usually `EnvQueryContext_Querier` |
| `ProjectDown` | Float | How far down to project onto NavMesh |

Practical settings for cover search (nearby): `GridHalfSize=800, SpaceBetween=150`
Practical settings for patrol (wide area): `GridHalfSize=2000, SpaceBetween=300`

### Ring (DonutAroundActor)

Generates points on a ring/annulus around a context at a specified radius range.

| Property | Type | Description |
|----------|------|-------------|
| `Center` | Context | Center of ring (e.g., `EnvQueryContext_Querier`) |
| `Radius` | Float | Ring radius (cm) |
| `ItemSpacing` | Float | Angular spacing between ring points |
| `ArcDirection` | Direction | Optional: restrict to a forward arc |

Use for: **flanking positions** (ring around enemy), **retreat points** (ring around self, facing away from enemy).

### PathingGrid (Points on NavMesh reachable from context)

Extends SimpleGrid by only keeping points reachable via NavMesh from the querier. More expensive but guarantees navigability.

| Property | Type | Description |
|----------|------|-------------|
| `GenerateAroundActor` | Context | Usually `EnvQueryContext_Querier` |
| `MaxDistance` | Float | NavMesh distance budget |
| `SpaceBetween` | Float | Grid spacing |
| `ScanRangeMultiplier` | Float | Multiplies scan range for path exploration |

### ActorsOfClass

Generates candidate actors of a given class (e.g., `APatrolPoint`, `APickup`).

| Property | Type | Description |
|----------|------|-------------|
| `SearchedActorClass` | Class | Actor class to find |
| `SearchCenter` | Context | Center of search radius |
| `SearchRadius` | Float | Radius to find actors in |

Use for: **patrol waypoints**, **interact targets**, **pickup locations**.

### Composite Generator

Combines results from multiple generators into one candidate set. Each sub-generator runs independently; results are merged.

---

## Tests

Each test has a **Test Purpose**: `Filter` (discard), `Score` (weight), or `FilterAndScore`.

### Distance Test

Scores/filters by distance between item and a context.

| Property | Type | Use |
|----------|------|-----|
| `DistanceTo` | Context | Usually `EnvQueryContext_Querier` or enemy context |
| `TestMode` | Enum | PathLength (NavMesh), Straight3D, Straight2D, Z |
| `ScoringEquation` | Enum | Constant, Linear, Square, InverseLinear |
| `ScoringFactor` | Float | Multiplier on the score |

**Find nearest actor**: Score=InverseLinear, ScoringFactor=1.0
**Find farthest (flee)**: Score=Linear, ScoringFactor=1.0
**Filter within range**: Purpose=Filter, FloatValueMin=100, FloatValueMax=2000

### Trace Test

Checks line-of-sight between item and a context. Can be used to find covered positions (no LoS to enemy) or exposed positions (has LoS to enemy).

| Property | Type | Use |
|----------|------|-----|
| `TraceFrom` | Context | Usually enemy actor context |
| `TraceChannel` | Enum | Visibility, Camera, or custom |
| `BoolMatch` | Bool | `true` = requires LoS; `false` = requires NO LoS (cover) |
| `TraceMode` | Enum | Navigation, Geometry, ByChannel |

**Cover query**: `BoolMatch=false` (item must NOT be visible from enemy)
**Sniper position query**: `BoolMatch=true` (item must have LoS to enemy)

### Dot Product Test

Scores items by the dot product of two directions. Useful for angular relationship checks.

| Property | Type | Use |
|----------|------|-----|
| `LineFrom` | Context | Origin of direction line |
| `LineTo` | Context | End of direction line |
| `TestAgainst` | Direction | Direction to test against |
| `bAbsoluteValue` | Bool | Use absolute dot product |

**Prefer items behind the querier**: `LineFrom=Enemy, LineTo=Querier, TestAgainst=ItemToLine`
**Flanking (perpendicular)**: Set scoring to penalize high dot products

### Overlap Test

Filters items that have overlapping geometry of a given class or channel.

| Property | Type | Use |
|----------|------|-----|
| `OverlapData` | Shape | Box, Sphere, or Capsule |
| `OverlapChannel` | Channel | Collision channel to check |
| `bOnlyBlockingHits` | Bool | Filter based on blocking overlaps |

Use for: checking clearance at candidate positions (e.g., "is there room to stand here?").

### Pathfinding Length Test

Scores items by how long the NavMesh path from the querier is. Different from straight-line distance.

| Property | Type | Use |
|----------|------|-----|
| `Context` | Context | Path destination context |
| `ScoringEquation` | Enum | Linear (prefer shorter paths) or InverseLinear |
| `PathFromContext` | Bool | If true, path goes from context to item |

Use for: **patrol point selection** (prefer reachable points without huge path detours), **cover with fast exit route**.

### GameplayTagsTest

Filters/scores items based on GameplayTags on the item actor.

| Property | Type | Use |
|----------|------|-----|
| `TagsToMatch` | FGameplayTagContainer | Required tags |
| `TagMatchType` | Enum | HasAll, HasAny |
| `bMustPass` | Bool | True = filter out non-matching |

---

## Common Query Configurations

### 1. Find Nearest Cover

Goal: AI hides from enemy, selecting the closest covered position.

```
Generator: SimpleGrid
  GridHalfSize = 800
  SpaceBetween = 150
  GenerateAround = EnvQueryContext_Querier

Test 1: Trace (Filter)
  TraceFrom = EnemyContext
  BoolMatch = false          ← item must NOT be visible from enemy
  TraceChannel = Visibility

Test 2: Distance (Score)
  DistanceTo = EnvQueryContext_Querier
  TestMode = Straight2D
  ScoringEquation = InverseLinear   ← prefer closer cover
  ScoringFactor = 1.0

Test 3: Pathfinding Length (Filter + Score)
  Purpose = FilterAndScore
  FloatValueMax = 3000       ← discard unreachable points
  ScoringEquation = InverseLinear
```

### 2. Find Flee Point (Retreat from Enemy)

Goal: AI moves far from enemy while staying navigable.

```
Generator: PathingGrid
  MaxDistance = 2000
  SpaceBetween = 300
  GenerateAround = EnvQueryContext_Querier

Test 1: Distance from Enemy (Score)
  DistanceTo = EnemyContext
  ScoringEquation = Linear      ← higher score = farther from enemy
  ScoringFactor = 1.0

Test 2: Trace from Enemy (Score — optional soft preference)
  TraceFrom = EnemyContext
  BoolMatch = false
  Purpose = Score               ← bonus score for hidden positions
  ScoringFactor = 0.5

Test 3: Distance from Self (Filter)
  DistanceTo = EnvQueryContext_Querier
  Purpose = Filter
  FloatValueMin = 400           ← don't pick a spot right next to self
```

### 3. Find Flanking Position

Goal: AI reaches a position perpendicular to the enemy, neither directly behind nor in front.

```
Generator: Ring
  Center = EnemyContext
  Radius = 600
  ItemSpacing = 45              ← 8 points around enemy

Test 1: Dot Product (Score — penalize direct front/back)
  LineFrom = EnemyContext (enemy forward)
  LineTo = Item position
  bAbsoluteValue = true
  ScoringEquation = InverseLinear   ← low dot = perpendicular = high score

Test 2: Trace to Enemy from Item (Filter)
  TraceFrom = EnemyContext
  BoolMatch = true              ← flanking position must have LoS to attack from
  TraceChannel = Visibility

Test 3: Pathfinding Length (Filter)
  FloatValueMax = 2500          ← must be reachable
```

### 4. Find Patrol Waypoint

Goal: Select a patrol destination that is not the current location, ideally exploring unvisited areas.

```
Generator: ActorsOfClass
  SearchedActorClass = APatrolPoint
  SearchCenter = EnvQueryContext_Querier
  SearchRadius = 5000

Test 1: Distance (Filter + Score)
  DistanceTo = EnvQueryContext_Querier
  Purpose = FilterAndScore
  FloatValueMin = 100           ← not current location
  FloatValueMax = 4000
  ScoringEquation = Linear      ← prefer farther points for exploration

Test 2: GameplayTags (Filter — optional)
  TagsToMatch = PatrolPoint.Active
  bMustPass = true
```

### 5. Find Attack Position (Ranged AI)

Goal: AI positions itself at ideal attack range, with LoS, not too close.

```
Generator: Ring
  Center = EnvQueryContext_Querier
  Radius = [AttackRangeMin..AttackRangeMax]   ← can use two rings merged with Composite
  ItemSpacing = 30

Test 1: Distance from Enemy (Filter)
  DistanceTo = EnemyContext
  Purpose = Filter
  FloatValueMin = AttackRangeMin
  FloatValueMax = AttackRangeMax

Test 2: Trace to Enemy (Filter — must have LoS)
  TraceFrom = EnemyContext
  BoolMatch = true
  TraceChannel = Visibility

Test 3: Distance from Self (Score — minimize movement)
  DistanceTo = EnvQueryContext_Querier
  ScoringEquation = InverseLinear
  ScoringFactor = 0.3           ← lower weight: prefer standing still if already in range
```

---

## Custom EQS Context (C++)

A custom context resolves to a specific actor or location, used in tests:

```cpp
#include "EnvironmentQuery/EnvQueryContext.h"
#include "EnvironmentQuery/Items/EnvQueryItemType_Actor.h"

UCLASS()
class UEnvQueryContext_Enemy : public UEnvQueryContext
{
    GENERATED_BODY()
public:
    virtual void ProvideContext(
        FEnvQueryInstance& QueryInstance,
        FEnvQueryContextData& ContextData) const override
    {
        AAIController* Controller = Cast<AAIController>(
            Cast<APawn>(QueryInstance.Owner.Get())->GetController());
        if (!Controller) { return; }

        UBlackboardComponent* BB = Controller->GetBlackboardComponent();
        if (!BB) { return; }

        AActor* Enemy = Cast<AActor>(BB->GetValueAsObject(TEXT("TargetActor")));
        if (IsValid(Enemy))
        {
            UEnvQueryItemType_Actor::SetContextHelper(ContextData, Enemy);
        }
    }
};
```

Blueprint context (simpler): Subclass `UEnvQueryContext_BlueprintBase` and implement `ProvideActorsSet` or `ProvideSingleLocation`.

---

## Running EQS Queries from C++

### Direct call (one-shot)

```cpp
#include "EnvironmentQuery/EnvQueryManager.h"

UPROPERTY(EditDefaultsOnly)
TObjectPtr<UEnvQuery> CoverQuery;

void AMyAIController::FindCover()
{
    FEnvQueryRequest Request(CoverQuery, this);
    // Optional named float params (set via DataProvider in the asset):
    // Request.SetFloatParam(TEXT("SearchRadius"), 1200.f);

    Request.Execute(EEnvQueryRunMode::SingleResult,
        FQueryFinishedSignature::CreateUObject(
            this, &AMyAIController::OnCoverQueryDone));
}

void AMyAIController::OnCoverQueryDone(TSharedPtr<FEnvQueryResult> Result)
{
    if (!Result.IsValid() || !Result->IsSuccessful()) { return; }

    // Location result
    FVector Location = Result->GetItemAsLocation(0);
    GetBlackboardComponent()->SetValueAsVector(TEXT("CoverLocation"), Location);

    // Actor result (if generator produces actors)
    // AActor* Actor = Result->GetItemAsActor(0);

    // Multiple results (when RunMode = AllMatching)
    // for (int32 i = 0; i < Result->Items.Num(); ++i)
    // {
    //     FVector Loc = Result->GetItemAsLocation(i);
    //     float Score = Result->Items[i].Score;
    // }
}
```

### Via BT Task (BTTask_RunEQSQuery)

Configure in-editor:
1. Add `BTTask_RunEQSQuery` node to Behavior Tree
2. Set `EQSRequest.QueryTemplate` = your `UEnvQuery` asset
3. Set `BlackboardKey` = target BB key (Vector for locations, Object for actors)
4. `EQSRequest.RunMode` = `SingleResult` for most cases
5. `bUpdateBBOnFail = false` to avoid clearing BB on failure

The task stores `FBTEnvQueryTaskMemory` (containing `RequestID`) in NodeMemory to manage the async query lifecycle and abort correctly.

### Via BT Service (periodic queries)

```cpp
// BTService_RunEQS — built-in service that runs an EQS query on interval
// Found in: BehaviorTree/Services/BTService_RunEQS.h
// Configure: QueryTemplate, BlackboardKey, RunMode, Interval
// This is equivalent to using a service that calls Request.Execute() in TickNode
```

---

## EQS Debugging

Enable EQS debug visualization:

```
Console: ai.debug.eqs 1
Console: DisplayAll EQS
Gameplay Debugger: ' key → select AI → press 4 (EQS panel)
```

In C++, `UEQSTestingPawn` (`EnvironmentQuery/EQSTestingPawn.h`) can be placed in the level to preview query results in-editor without running the game.

---

## Performance Notes

| Concern | Mitigation |
|---------|-----------|
| Large grid (many candidates) | Reduce `GridHalfSize` or increase `SpaceBetween`. Use `SingleResult` mode. |
| Frequent queries | Use BT Service with `Interval >= 0.5s`. Cache result in BB rather than re-running each tick. |
| Expensive Trace tests | Limit trace count via early filter tests before trace (e.g., distance filter first). |
| PathfindingLength test | Avoid on every frame; path queries are CPU-intensive. Run at 1-2s intervals max. |
| Many concurrent AI | Use `UEnvQueryManager`'s built-in query throttling (max parallel queries per frame set in Project Settings > AI > EQS). |
| AllMatching mode | Only use when you need a ranked list; `SingleResult` is significantly cheaper. |
