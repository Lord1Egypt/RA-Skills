# State Tree Mass Entity Integration

How State Trees integrate with Mass Entity for processing thousands of entities efficiently. For core Mass Entity architecture, see `ue-mass-entity`.

**Build.cs modules**: `StateTreeModule`, `GameplayStateTreeModule`, `MassEntity`, `MassAIBehavior`

---

## UMassStateTreeSchema

`UMassStateTreeSchema` constrains a `UStateTree` asset to only allow Mass-compatible node types:
- `FMassStateTreeTaskBase` (not `FStateTreeTaskBase`)
- `FMassStateTreeConditionBase` (not `FStateTreeConditionBase`)
- `FMassStateTreeEvaluatorBase` (not `FStateTreeEvaluatorBase`)

Select this schema when creating a `UStateTree` intended for Mass Entity processing. Regular State Tree nodes will not appear in the editor dropdown.

---

## Mass-Specific Node Base Classes

### FMassStateTreeTaskBase

Extends `FStateTreeTaskBase` with Mass fragment dependency declarations:

```cpp
USTRUCT(meta=(DisplayName="My Mass Task"))
struct FMyMassTask : public FMassStateTreeTaskBase
{
    GENERATED_BODY()
    typedef FMyMassTaskInstanceData FInstanceDataType;

    // Declare which fragments this task reads/writes
    // The processor uses these to build its execution requirements
    virtual void GetDependencies(UE::MassBehavior::FStateTreeDependencyBuilder& Builder) const override
    {
        Builder.AddReadWrite<FTransformFragment>();
        Builder.AddReadOnly<FMassVelocityFragment>();
    }

    virtual EStateTreeRunStatus EnterState(FStateTreeExecutionContext& Context,
        const FStateTreeTransitionResult& Transition) const override
    {
        // Access entity via FMassStateTreeExecutionContext
        const FMassStateTreeExecutionContext& MassContext =
            static_cast<const FMassStateTreeExecutionContext&>(Context);
        FMassEntityHandle Entity = MassContext.GetEntity();
        // Use entity with Mass subsystem APIs...
        return EStateTreeRunStatus::Running;
    }
};
```

### FMassStateTreeConditionBase

Same pattern — extends `FStateTreeConditionBase`, adds `GetDependencies()`:

```cpp
USTRUCT(meta=(DisplayName="My Mass Condition"))
struct FMyMassCondition : public FMassStateTreeConditionBase
{
    GENERATED_BODY()

    virtual void GetDependencies(UE::MassBehavior::FStateTreeDependencyBuilder& Builder) const override
    {
        Builder.AddReadOnly<FMassHealthFragment>();
    }

    virtual bool TestCondition(FStateTreeExecutionContext& Context) const override
    {
        const auto& MassCtx = static_cast<const FMassStateTreeExecutionContext&>(Context);
        // Check fragment data on the entity...
        return true;
    }
};
```

### FMassStateTreeEvaluatorBase

Extends `FStateTreeEvaluatorBase` with the same `GetDependencies(UE::MassBehavior::FStateTreeDependencyBuilder& Builder) const` override for fragment access.

---

## Entity Configuration

### UMassStateTreeTrait

Add `UMassStateTreeTrait` to a `UMassEntityConfigAsset` to assign a State Tree to entities of that archetype:

```cpp
// In Mass Entity Config asset (data-driven):
// Add StateTree Trait → assign UStateTree asset with UMassStateTreeSchema
```

The trait adds required fragments to the archetype:
- `FMassStateTreeInstanceFragment` — per-entity instance data handle
- `FMassStateTreeSharedFragment` — shared tree reference (one per archetype)

### Fragments

| Fragment | Scope | Contains |
|----------|-------|----------|
| `FMassStateTreeInstanceFragment` | Per-entity | Handle to pooled `FStateTreeInstanceData` |
| `FMassStateTreeSharedFragment` | Per-archetype (shared) | `FStateTreeReference` to the `UStateTree` asset |

---

## UMassStateTreeSubsystem

Manages pooled State Tree instance data for Mass entities. Pooling avoids per-entity allocation overhead.

```cpp
// Allocate instance data for an entity
FMassStateTreeInstanceHandle Handle =
    MassStateTreeSubsystem->AllocateInstanceData(StateTree);

// Access instance data for execution
FStateTreeInstanceData* Data = MassStateTreeSubsystem->GetInstanceData(Handle);

// Free when entity is destroyed
MassStateTreeSubsystem->FreeInstanceData(Handle);
```

The subsystem handles allocation/deallocation automatically through the trait lifecycle. Manual calls are only needed for custom processors.

---

## FMassStateTreeExecutionContext

Wraps `FStateTreeExecutionContext` with entity access:

```cpp
// 4-param constructor (UE 5.5+): Owner, StateTree, InstanceData, MassExecutionContext
FMassStateTreeExecutionContext MassContext(
    Owner, *StateTree, InstanceData, MassExecContext);

MassContext.SetEntity(EntityHandle);    // set current entity before Tick
FMassEntityHandle Entity = MassContext.GetEntity();  // access in tasks
```

`MassExecContext` is the `FMassExecutionContext&` available inside a Mass processor's `Execute()` method. The old 6-param form `(Owner, *StateTree, InstanceData, EntityManager, SignalSubsystem, MassExecContext)` is deprecated since UE 5.6.

The processor calls `SetEntity()` before ticking each entity's tree, making the entity handle available to all tasks and conditions via the context.

---

## UMassStateTreeProcessor

Evaluates State Trees for all entities with `FMassStateTreeInstanceFragment`. Created dynamically — one processor per unique set of fragment requirements (hashed from all tasks' `GetDependencies()`).

The processor:
1. Queries entities with matching fragments
2. For each entity: constructs `FMassStateTreeExecutionContext`, calls `SetEntity()`, ticks the tree
3. Handles transition signals and state changes

Fragment requirements declared in `GetDependencies()` from all tasks in the tree are merged into the processor's query, so a tree with tasks reading `FTransformFragment` and `FMassVelocityFragment` will produce a processor that requires both.

---

## Mass Signals

Mass signals coordinate State Tree execution with other Mass processors:

| Signal | Purpose |
|--------|---------|
| `StateTreeActivate` | Activates a dormant State Tree on an entity |
| `NewStateTreeTaskRequired` | Signals that the current task needs re-evaluation |
| `DelayedTransitionWakeup` | Wakes an entity for a delayed transition check |

Send signals via `UMassSignalSubsystem`:
```cpp
SignalSubsystem.SignalEntity(Entity, UE::Mass::Signals::StateTreeActivate);
```

---

## Performance Notes

- **Keep tasks minimal:** Each entity ticks its tree every frame. Expensive operations (pathfinding, overlap queries) should be throttled with intervals or event-driven rather than per-tick.
- **Fragment access matters:** `GetDependencies()` determines processor parallelism. Minimize `ReadWrite` fragments; prefer `ReadOnly` to allow concurrent execution with other processors.
- **Pool instance data:** Always use `UMassStateTreeSubsystem` for allocation. Direct `FStateTreeInstanceData` construction per entity defeats the pooling optimization.
- **Shallow trees:** `FStateTreeActiveStates::MaxStates = 8` is the depth limit. Mass trees should be especially shallow (2-3 levels) since depth adds per-entity overhead.
- **Profile early:** Use `stat MassEntity` and Unreal Insights to identify expensive State Tree tasks. A single heavy task across 10,000 entities multiplies its cost dramatically.
- **Batch signals:** Prefer `SignalEntities()` (plural) over individual `SignalEntity()` calls when signaling multiple entities to reduce subsystem overhead.
