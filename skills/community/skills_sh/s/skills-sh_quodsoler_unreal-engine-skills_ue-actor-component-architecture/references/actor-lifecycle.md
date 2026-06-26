# Actor Lifecycle Reference

Full event ordering for `AActor` from spawn through destruction, with component events interleaved, network notes, and what is safe to do at each stage.

Source of truth: `Engine/Source/Runtime/Engine/Classes/GameFramework/Actor.h` — the class-level Doxygen block starting at line 222 documents the authoritative order of initialization virtual functions.

---

## Complete Lifecycle Diagram

```
  SPAWN / LEVEL LOAD
  ──────────────────────────────────────────────────────────────────────────
  AActor::AActor()
    Called on the Class Default Object (CDO) and on every instance.
    World = nullptr. No other actors are accessible.
    ┌─ CreateDefaultSubobject<T>()           OK: creates owned components
    ├─ SetRootComponent()                    OK: sets hierarchy root
    ├─ PrimaryActorTick.*                    OK: configure tick
    └─ Default UPROPERTY values              OK

  [Statically placed actors only — loaded from level file]
  UObject::PostLoad()
    Normal UObject serialization. Called in editor and during gameplay for
    map-placed actors. NOT called for freshly spawned actors.

  UActorComponent::OnComponentCreated()
    Called for native (C++) components when the actor is spawned in editor
    or gameplay. Not called for components loaded from a saved level.

  AActor::PreRegisterAllComponents()
    For actors that have a native root component. Components are about to
    be registered with the world scene.

  UActorComponent::RegisterComponent()       [once per component]
    Creates the physical and visual representation of each component
    in the world (render proxy, physics body). May be spread across frames
    for large levels.

  AActor::PostRegisterAllComponents()
    All components are now registered. Called in editor and gameplay.
    Last function called in all initialization paths.

  [Spawned actors only — NOT level-placed]
  AActor::PostActorCreated()
    Called right before construction (UserConstructionScript / OnConstruction).
    Not called for level-placed actors.

  AActor::UserConstructionScript()
    Blueprint construction script executes here.

  AActor::OnConstruction()
    C++ hook called at end of ExecuteConstruction (after Blueprint CS).
    All Blueprint-created components are fully created and registered at
    this point. In gameplay, only called for spawned actors.
    Can be re-run in editor when Blueprint is recompiled.

  ──────────────────────────────────────────────────────────────────────────
  GAMEPLAY INITIALIZATION  (not in editor CDO pass)
  ──────────────────────────────────────────────────────────────────────────
  AActor::PreInitializeComponents()
    Called before InitializeComponent on any component. Override to do
    pre-init setup that doesn't belong in the constructor.

  UActorComponent::Activate()                [if bAutoActivate == true]
    Component self-activates during the init sequence.

  UActorComponent::InitializeComponent()     [if bWantsInitializeComponent == true]
    Called once per gameplay session per component. Override to do
    one-time setup that requires the world to exist.

  AActor::PostInitializeComponents()
    All components have been initialized. World exists. Other actors that
    were in the level at load time are accessible.
    ┌─ Safe: bind delegates to own components
    ├─ Safe: read/write component state
    ├─ Safe: access GetWorld()
    └─ NOT safe: assume BeginPlay-dependent state in other actors

  ──────────────────────────────────────────────────────────────────────────
  PLAY  (level has started ticking)
  ──────────────────────────────────────────────────────────────────────────
  AActor::BeginPlay()
    ├─ UActorComponent::BeginPlay()          [each component, in order]
    │    Begins play for each registered, initialized component.
    │    Component BeginPlay runs BEFORE Actor BeginPlay completes
    │    if called from within AActor::BeginPlay via Super chain.
    └─ Full game state is accessible here

  AActor::Tick(float DeltaTime)              [every frame, if bCanEverTick]
    ├─ UActorComponent::TickComponent()      [each ticking component]
    └─ Tick groups control ordering (see tick group table below)

  ──────────────────────────────────────────────────────────────────────────
  TERMINATION
  ──────────────────────────────────────────────────────────────────────────
  AActor::EndPlay(EEndPlayReason::Type)
    ├─ UActorComponent::EndPlay()            [each component]
    └─ UActorComponent::UninitializeComponent()

  AActor::Destroyed()
    Called when the actor is being deleted. Avoid complex logic here.
    The actor is about to be handed to the garbage collector.

  [GC pass — memory freed]
```

---

## EEndPlayReason Values

Declared in `Engine/EngineTypes.h`:

```cpp
namespace EEndPlayReason
{
    enum Type : int
    {
        Destroyed,          // Actor::Destroy() was called explicitly
        LevelTransition,    // A level transition (map change) is occurring
        EndPlayInEditor,    // PIE session ended in the editor
        RemovedFromWorld,   // Level streaming unloaded the actor's sublevel
        Quit,               // The game application is shutting down
    };
}
```

### Decision matrix for EndPlay cleanup

| EndPlayReason | Play effects? | Save state? | Release resources? |
|---|---|---|---|
| `Destroyed` | Yes (optional) | If persistent | Yes |
| `LevelTransition` | No | If needed | Yes |
| `EndPlayInEditor` | No | No | Yes |
| `RemovedFromWorld` | No | If needed | Yes |
| `Quit` | No | If needed | Yes |

Always clear timers in EndPlay regardless of reason:

```cpp
void AMyActor::EndPlay(const EEndPlayReason::Type EndPlayReason)
{
    GetWorld()->GetTimerManager().ClearAllTimersForObject(this);
    Super::EndPlay(EndPlayReason); // Required
}
```

---

## Tick Group Ordering

Tick groups are defined in `Engine/Source/Runtime/Engine/Classes/Engine/EngineBaseTypes.h`:

```
Frame start
  │
  ├─ TG_PrePhysics       (default for actors and components)
  │    Input processing, movement requests, AI decisions
  │
  ├─ TG_StartPhysics     (internal — physics simulation begins)
  │
  ├─ TG_DuringPhysics    (async; runs while physics is simulating)
  │    Read-only queries on physics state from previous frame
  │
  ├─ TG_EndPhysics       (physics simulation completes)
  │    First point where this frame's physics results are readable
  │
  ├─ TG_PostPhysics      (after physics settles)
  │    Spring arm, camera follow, IK solvers, cloth, ragdoll read
  │
  └─ TG_PostUpdateWork   (last tick group)
       Final state queries, rendering preparation
Frame end
```

Setting the tick group:

```cpp
AMyActor::AMyActor()
{
    PrimaryActorTick.bCanEverTick = true;
    PrimaryActorTick.TickGroup = TG_PostPhysics;
}

UMyComponent::UMyComponent()
{
    PrimaryComponentTick.bCanEverTick = true;
    PrimaryComponentTick.TickGroup = TG_PostPhysics;
}
```

---

## Network Lifecycle Differences

For replicated actors, the lifecycle deviates from the single-player sequence.

### Server (authority)

The server runs the complete lifecycle described above. `BeginPlay` is called normally.

### Client (simulated proxy)

1. Actor data is received from the server over the network.
2. The actor is created locally by the net driver.
3. **`PostNetReceive`** is called after properties are received.
4. **`OnRep_*` functions** are called for `UPROPERTY(ReplicatedUsing=...)` fields.
5. **`BeginPlay` is called**, but timing is determined by the network — it may be delayed compared to the server, and happens after the actor's initial replicated state is applied.

Key consequence: never assume that `BeginPlay` on the client sees the same initial property values as the server's `BeginPlay`. The server may have changed properties after initial spawn before the client even received the actor.

### Replicated actor spawn sequence (client side)

```
Net driver receives actor channel data
  → UActorComponent::OnComponentCreated() [native components]
  → AActor::PostActorCreated()
  → AActor::PostInitializeComponents()
  → PostNetReceive() / OnRep_* calls for initial property batch
  → AActor::BeginPlay()
```

### Child actors in multiplayer

`UChildActorComponent` actors have their `BeginPlay` delayed until after their parent actor's `BeginPlay` in some cases. Do not assume a child actor is BegunPlay when the parent is in `PostInitializeComponents`.

---

## Deferred Spawn Sequence

`SpawnActorDeferred` pauses the lifecycle between construction and initialization, giving you a window to configure the actor before `BeginPlay` fires.

```
SpawnActorDeferred<T>() called
  → AActor::AActor()                  Constructor runs
  → CreateDefaultSubobject calls      Components created
  → AActor::PostActorCreated()        Normal post-construction hook

  [Actor exists but is NOT initialized — BeginPlay has NOT fired]
  [Window: set properties on the actor here]

Actor->FinishSpawning(Transform)
  → AActor::OnConstruction()
  → AActor::PreInitializeComponents()
  → UActorComponent::InitializeComponent()
  → AActor::PostInitializeComponents()
  → AActor::BeginPlay()               Now fires
```

This pattern is essential when:
- The actor's `BeginPlay` reads configuration data that must be set before it runs
- You are spawning from a DataAsset or configuration object
- You need to prevent BeginPlay side effects (spawning sub-actors, playing audio) until fully configured

---

## Component Lifecycle Within an Actor

Each `UActorComponent` has its own parallel lifecycle that mirrors the actor's:

```
UActorComponent constructed (via CreateDefaultSubobject or NewObject)
  → OnComponentCreated()          [first time, not on level-placed actors]
  → RegisterComponent()           [gets world presence]
  → OnRegister()                  [scene is set; before render/physics state]
  → CreateRenderState_Concurrent() [render proxy created]
  → OnCreatePhysicsState()        [physics body created]
  → InitializeComponent()         [if bWantsInitializeComponent]
  → Activate()                    [if bAutoActivate]
  → BeginPlay()

  → TickComponent()               [every frame if ticking]

  → EndPlay()
  → UninitializeComponent()
  → OnUnregister()
  → DestroyRenderState_Concurrent()
  → OnDestroyPhysicsState()
  → DestroyComponent()            [marks for GC]
```

`bHasBegunPlay`, `bHasBeenInitialized`, `bHasBeenCreated` are the runtime flags you can check on a `UActorComponent` instance to know where it is in this sequence.

---

## What Is Safe At Each Stage

| Stage | GetWorld() | Other Actors | Own Components | Game State |
|---|---|---|---|---|
| Constructor | No (nullptr on CDO) | No | Create only | No |
| PostLoad | Yes (editor/runtime) | No | Read only | No |
| OnComponentCreated | No | No | Yes | No |
| RegisterComponent | No | No | Yes | No |
| PostActorCreated | Yes | Limited | Yes | No |
| OnConstruction | Yes | Limited | Yes | No |
| PreInitializeComponents | Yes | Yes | Yes | Partial |
| PostInitializeComponents | Yes | Yes | Yes | Partial |
| BeginPlay | Yes | Yes | Yes | Yes |
| Tick | Yes | Yes | Yes | Yes |
| EndPlay | Yes | Carefully | Yes | Shutting down |
| Destroyed | Yes | No | Partial | No |
