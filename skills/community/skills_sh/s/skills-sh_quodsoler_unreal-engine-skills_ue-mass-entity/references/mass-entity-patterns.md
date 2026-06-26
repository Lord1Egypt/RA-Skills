# Mass Entity Patterns

Code templates for Mass Entity framework. All signatures source-verified from UE headers.

---

## Custom Fragment and Tag Definitions

```cpp
#include "MassEntityTypes.h"

// Per-entity mutable fragment
USTRUCT()
struct FHealthFragment : public FMassFragment
{
    GENERATED_BODY()
    UPROPERTY(EditAnywhere)
    float Current = 100.f;
    UPROPERTY(EditAnywhere)
    float Max = 100.f;
};

// Zero-size tag (no data members allowed)
USTRUCT()
struct FPoisonedTag : public FMassTag
{
    GENERATED_BODY()
};

// Shared fragment — one instance per archetype, mutable
USTRUCT()
struct FSquadSharedFragment : public FMassSharedFragment
{
    GENERATED_BODY()
    UPROPERTY(EditAnywhere)
    int32 SquadID = 0;
    UPROPERTY(EditAnywhere)
    FLinearColor SquadColor = FLinearColor::White;
};

// Const shared fragment — immutable after archetype creation
USTRUCT()
struct FMeshConfigFragment : public FMassConstSharedFragment
{
    GENERATED_BODY()
    UPROPERTY(EditAnywhere)
    TSoftObjectPtr<UStaticMesh> Mesh;
    UPROPERTY(EditAnywhere)
    float LODDistance = 5000.f;
};

// Chunk fragment — per memory chunk, not per entity
USTRUCT()
struct FChunkLODFragment : public FMassChunkFragment
{
    GENERATED_BODY()
    int32 CurrentLOD = 0;
};
```

---

## UMassProcessor Subclass Template

```cpp
// MyMovementProcessor.h
#pragma once
#include "MassProcessor.h"
#include "MyMovementProcessor.generated.h"

UCLASS()
class UMyMovementProcessor : public UMassProcessor
{
    GENERATED_BODY()
public:
    UMyMovementProcessor();
protected:
    virtual void ConfigureQueries(const TSharedRef<FMassEntityManager>& EntityManager) override;
    virtual void Execute(FMassEntityManager& EntityManager,
                         FMassExecutionContext& Context) override;
private:
    FMassEntityQuery MovementQuery;
};

// MyMovementProcessor.cpp
#include "MyMovementProcessor.h"
#include "MassCommonFragments.h"
#include "MassMovementFragments.h"

UMyMovementProcessor::UMyMovementProcessor()
{
    ProcessingPhase = EMassProcessingPhase::PrePhysics;
    ExecutionFlags = static_cast<int32>(
        EProcessorExecutionFlags::Server |
        EProcessorExecutionFlags::Standalone);
    ExecutionOrder.ExecuteInGroup = UE::Mass::ProcessorGroupNames::Movement;
    bRequiresGameThreadExecution = false;
}

void UMyMovementProcessor::ConfigureQueries(const TSharedRef<FMassEntityManager>& EntityManager)
{
    MovementQuery.AddRequirement<FTransformFragment>(
        EMassFragmentAccess::ReadWrite, EMassFragmentPresence::All);
    MovementQuery.AddRequirement<FMassVelocityFragment>(
        EMassFragmentAccess::ReadOnly, EMassFragmentPresence::All);
    MovementQuery.AddTagRequirement<FDeadTag>(EMassFragmentPresence::None);
    RegisterQuery(MovementQuery);
}

void UMyMovementProcessor::Execute(FMassEntityManager& EntityManager,
                                   FMassExecutionContext& Context)
{
    MovementQuery.ForEachEntityChunk(Context,
        [](FMassExecutionContext& Context)
    {
        const int32 Num = Context.GetNumEntities();
        TArrayView<FTransformFragment> Transforms =
            Context.GetMutableFragmentView<FTransformFragment>();
        TConstArrayView<FMassVelocityFragment> Velocities =
            Context.GetFragmentView<FMassVelocityFragment>();
        const float DT = Context.GetDeltaTimeSeconds();

        for (int32 i = 0; i < Num; ++i)
        {
            Transforms[i].GetMutableTransform().AddToTranslation(
                Velocities[i].Value * DT);
        }
    });
}
```

---

## Observer Processor Template

```cpp
// HealthAddedObserver.h
#pragma once
#include "MassObserverProcessor.h"
#include "HealthAddedObserver.generated.h"

UCLASS()
class UHealthAddedObserver : public UMassObserverProcessor
{
    GENERATED_BODY()
public:
    UHealthAddedObserver()
    {
        ObservedType = FHealthFragment::StaticStruct();
        ObservedOperations = EMassObservedOperationFlags::AddElement;
    }
protected:
    virtual void ConfigureQueries(const TSharedRef<FMassEntityManager>& EntityManager) override;
    virtual void Execute(FMassEntityManager& EntityManager,
                         FMassExecutionContext& Context) override;
private:
    FMassEntityQuery ObserverQuery;
};

// HealthAddedObserver.cpp
void UHealthAddedObserver::ConfigureQueries(const TSharedRef<FMassEntityManager>& EntityManager)
{
    ObserverQuery.AddRequirement<FHealthFragment>(
        EMassFragmentAccess::ReadWrite, EMassFragmentPresence::All);
    ObserverQuery.AddRequirement<FTransformFragment>(
        EMassFragmentAccess::ReadOnly, EMassFragmentPresence::All);
    RegisterQuery(ObserverQuery);
}

void UHealthAddedObserver::Execute(FMassEntityManager& EntityManager,
                                   FMassExecutionContext& Context)
{
    ObserverQuery.ForEachEntityChunk(Context,
        [](FMassExecutionContext& Context)
    {
        TArrayView<FHealthFragment> Healths =
            Context.GetMutableFragmentView<FHealthFragment>();
        for (int32 i = 0; i < Context.GetNumEntities(); ++i)
        {
            // Initialize health on fragment addition
            Healths[i].Current = Healths[i].Max;
        }
    });
}
```

---

## FMassEntityView Usage

```cpp
void ApplyDamage(FMassEntityManager& EntityManager,
                 FMassEntityHandle Target, float Damage)
{
    if (!EntityManager.IsEntityValid(Target))
    {
        return;
    }

    FMassEntityView View(EntityManager, Target);

    if (View.GetFragmentDataPtr<FHealthFragment>() == nullptr)
    {
        return;
    }

    FHealthFragment& Health = View.GetFragmentData<FHealthFragment>();
    Health.Current = FMath::Max(0.f, Health.Current - Damage);

    // Check tag presence
    if (!View.HasTag<FDeadTag>() && Health.Current <= 0.f)
    {
        // Add tag outside processor — direct mutation is safe here
        EntityManager.AddTagToEntity(Target, FDeadTag::StaticStruct());
    }
}
```

**Important:** Never store `FMassEntityView` across frames. Create a fresh view each time.

---

## Deferred Command Patterns

Use inside `ForEachEntityChunk` -- never mutate entities directly during iteration:

```cpp
Query.ForEachEntityChunk(Context,
    [](FMassExecutionContext& Context)
{
    auto Entities = Context.GetEntities();
    auto Healths = Context.GetFragmentView<FHealthFragment>();

    for (int32 i = 0; i < Context.GetNumEntities(); ++i)
    {
        if (Healths[i].Current <= 0.f)
        {
            // Tag for death processing
            Context.Defer().AddTag<FDeadTag>(Entities[i]);

            // Remove fragment
            Context.Defer().RemoveFragment<FHealthFragment>(Entities[i]);

            // Swap tags atomically
            Context.Defer().SwapTags<FAliveTag, FDeadTag>(Entities[i]);

            // Add fragment with initial data using FMassCommandAddFragmentInstances<T>
            // Template args are the fragment types; call Add(Entity, FragmentValue) pattern
            Context.Defer().PushCommand<FMassCommandAddFragmentInstances<FHealthFragment>>(
                Entities[i], FHealthFragment{});
        }
    }
});
```

**Execution order:** Create -> Add -> Remove -> ChangeComposition -> Set -> Destroy

---

## Custom Trait Template

```cpp
// MyHealthTrait.h
#pragma once
#include "MassEntityTraitBase.h"
#include "MyHealthTrait.generated.h"

UCLASS(meta = (DisplayName = "Health"))
class UMyHealthTrait : public UMassEntityTraitBase
{
    GENERATED_BODY()
public:
    UPROPERTY(EditAnywhere, Category = Health)
    float DefaultHealth = 100.f;

    UPROPERTY(EditAnywhere, Category = Health)
    float DefaultMaxHealth = 100.f;

protected:
    virtual void BuildTemplate(
        FMassEntityTemplateBuildContext& BuildContext,
        const UWorld& World) const override
    {
        // Add fragment and set initial values using AddFragment_GetRef
        FHealthFragment& HealthDefaults = BuildContext.AddFragment_GetRef<FHealthFragment>();
        HealthDefaults.Current = DefaultHealth;
        HealthDefaults.Max = DefaultMaxHealth;

        // Add a tag
        BuildContext.AddTag<FAliveTag>();
    }
};
```

Assign traits to `UMassEntityConfigAsset` in the editor. `AMassSpawner` references the config asset and controls spawn count and spatial distribution.

---

## ISM Representation Setup

Representation uses `UMassVisualizationTrait` on entity config assets. The trait adds `FMassRepresentationFragment` (per-entity) and `FMassRepresentationParameters` (const shared) to the archetype.

Key configuration on the trait:
- Static mesh assignment per LOD significance range
- LOD distance thresholds (`EMassLOD::High/Medium/Low/Off`)
- Actor classes for `EMassRepresentationType::HighResSpawnedActor` and `LowResSpawnedActor` (close-up detail)

Force game-thread execution for processors touching ISM:

```cpp
// In your processor's shared fragment traits specialization:
template<>
struct TMassSharedFragmentTraits<FMyVisualizationFragment>
{
    static constexpr bool GameThreadOnly = true;
};
```

`UMassRepresentationSubsystem` manages ISM component pools and handles LOD transitions between `StaticMeshInstance`, `HighResSpawnedActor`, and `LowResSpawnedActor` representation types.
