# Component Types Reference

Complete reference for UE's built-in component types with inheritance hierarchy, capabilities, use cases, and creation patterns. All component classes live under `Engine/Source/Runtime/Engine/Classes/Components/` unless otherwise noted.

---

## Inheritance Hierarchy

```
UObject
  └── UActorComponent                 Logic-only; no transform
        └── USceneComponent           Adds transform + attachment
              └── UPrimitiveComponent Adds collision + rendering + physics
                    ├── UMeshComponent
                    │     ├── UStaticMeshComponent
                    │     ├── USkeletalMeshComponent
                    │     ├── UInstancedStaticMeshComponent
                    │     └── UProceduralMeshComponent
                    ├── UShapeComponent
                    │     ├── UCapsuleComponent
                    │     ├── UBoxComponent
                    │     └── USphereComponent
                    └── ULightComponentBase
                          ├── UPointLightComponent
                          ├── USpotLightComponent
                          └── UDirectionalLightComponent
```

---

## Layer 1: UActorComponent

**Header**: `Components/ActorComponent.h`

**What it is**: The base class for all components. Has no transform, no position in the world. Pure behavior and data.

**Key properties from source**:
```cpp
// Tick function — must set bCanEverTick = true to use
struct FActorComponentTickFunction PrimaryComponentTick;

// Whether the component activates itself during initialization
uint8 bAutoActivate : 1;

// Whether InitializeComponent() is called during startup
uint8 bWantsInitializeComponent : 1;

// Component can replicate — owner actor must also replicate
uint8 bReplicates : 1;

// Tags for grouping, accessible from Blueprint
TArray<FName> ComponentTags;
```

**Key virtual functions to override**:
```cpp
virtual void InitializeComponent();     // One-time setup; requires bWantsInitializeComponent=true
virtual void BeginPlay();               // Game starts
virtual void EndPlay(EEndPlayReason);   // Cleanup
virtual void TickComponent(float DeltaTime, ELevelTick, FActorComponentTickFunction*);
virtual void Activate(bool bReset);     // Custom activation logic
virtual void Deactivate();
virtual bool ShouldActivate() const;    // Return false to block activation
virtual void OnRegister();              // Component registered with world
virtual void OnUnregister();            // Component unregistered
```

**When to use**:
- Health/stamina/mana tracking
- Inventory and item management
- Status effect systems
- Buff/debuff application
- AI blackboard bridging
- Ability management (alternative to GAS for simple cases)
- Save game data aggregation per actor

**Creation pattern**:
```cpp
// Constructor
HealthComponent = CreateDefaultSubobject<UHealthComponent>(TEXT("Health"));

// Runtime
UHealthComponent* HC = NewObject<UHealthComponent>(this, UHealthComponent::StaticClass());
HC->RegisterComponent();
```

---

## Layer 2: USceneComponent

**Header**: `Components/SceneComponent.h`

**What it is**: A `UActorComponent` that has a `FTransform` (`RelativeLocation`, `RelativeRotation`, `RelativeScale3D`). Can attach to and from other `USceneComponent`s, building a hierarchical transform tree.

**Key properties from source**:
```cpp
// Transform (private — use accessors)
FVector RelativeLocation;
FRotator RelativeRotation;
FVector RelativeScale3D;

// Attachment parent
TObjectPtr<USceneComponent> AttachParent;
FName AttachSocketName;

// Children
TArray<TObjectPtr<USceneComponent>> AttachChildren;

// Mobility — only safe to set in constructor
TEnumAsByte<EComponentMobility::Type> Mobility;
// EComponentMobility::Static   — baked lighting, no runtime movement
// EComponentMobility::Stationary — baked shadows, can change intensity/color
// EComponentMobility::Movable  — fully dynamic, moves at runtime

// Visibility
uint8 bVisible : 1;
uint8 bHiddenInGame : 1;

// Absolute flags (ignore parent transform for that axis)
uint8 bAbsoluteLocation : 1;
uint8 bAbsoluteRotation : 1;
uint8 bAbsoluteScale : 1;
```

**Key transform API**:
```cpp
// Position
void SetRelativeLocation(FVector);
void SetWorldLocation(FVector);
FVector GetRelativeLocation() const;
FVector GetComponentLocation() const;   // World space

// Rotation
void SetRelativeRotation(FRotator);
void SetWorldRotation(FRotator);
FRotator GetRelativeRotation() const;
FRotator GetComponentRotation() const;  // World space

// Full transform
void SetRelativeTransform(const FTransform&);
void SetWorldTransform(const FTransform&);
FTransform GetRelativeTransform() const;
FTransform GetComponentTransform() const; // = ComponentToWorld

// Movement with sweep (collision-aware)
bool MoveComponent(const FVector& Delta, const FQuat& NewRotation, bool bSweep,
    FHitResult* Hit, EMoveComponentFlags Flags, ETeleportType Teleport);
```

**Attachment API**:
```cpp
// Constructor-time parent declaration (no world required)
Child->SetupAttachment(Parent);
Child->SetupAttachment(Parent, SocketName);

// Runtime attachment with transform rules
Child->AttachToComponent(Parent, FAttachmentTransformRules::KeepRelativeTransform);
Child->AttachToComponent(Parent, FAttachmentTransformRules::KeepWorldTransform);
Child->AttachToComponent(Parent, FAttachmentTransformRules::SnapToTargetNotIncludingScale, SocketName);

// Detach
Child->DetachFromComponent(FDetachmentTransformRules::KeepWorldTransform);
Child->DetachFromComponent(FDetachmentTransformRules::KeepRelativeTransform);
```

**`FAttachmentTransformRules` options**:

| Rule | Location | Rotation | Scale | Typical use |
|---|---|---|---|---|
| `KeepRelativeTransform` | Relative | Relative | Relative | Default — preserves local offset |
| `KeepWorldTransform` | World | World | World | Actor already positioned correctly |
| `SnapToTargetIncludingScale` | Target | Target | Target | Hard snap to socket, match scale |
| `SnapToTargetNotIncludingScale` | Target | Target | Self | Hard snap to socket, own scale |

**When to use `USceneComponent` directly**:
- Pivot point / offset node: attach children to a scene component to shift their origin without a visible mesh
- Spawn location markers (invisible reference points)
- Grouping components that should move together under one transform

```cpp
// Common pattern: scene component as a group pivot
GroupPivot = CreateDefaultSubobject<USceneComponent>(TEXT("GroupPivot"));
GroupPivot->SetupAttachment(RootComponent);

MeshA->SetupAttachment(GroupPivot);
MeshB->SetupAttachment(GroupPivot);
// Rotate GroupPivot to rotate both meshes together
```

---

## Layer 3: UPrimitiveComponent

**Header**: `Components/PrimitiveComponent.h`

**What it is**: Extends `USceneComponent` with:
- Collision geometry (collision response channels, query/physics collision)
- Render proxy (submitted to the renderer each frame)
- Physics simulation (rigid body, constraints)
- Overlap/hit events

**Key collision API**:
```cpp
void SetCollisionEnabled(ECollisionEnabled::Type);
// ECollisionEnabled::NoCollision
// ECollisionEnabled::QueryOnly      — overlaps and line traces, no physics
// ECollisionEnabled::PhysicsOnly    — physics push/pull, no queries
// ECollisionEnabled::QueryAndPhysics

void SetCollisionObjectType(ECollisionChannel);
void SetCollisionResponseToChannel(ECollisionChannel, ECollisionResponse);
void SetCollisionResponseToAllChannels(ECollisionResponse);
void SetCollisionProfileName(FName ProfileName);

// Overlap events
void SetGenerateOverlapEvents(bool);
FComponentBeginOverlapSignature OnComponentBeginOverlap;
FComponentEndOverlapSignature OnComponentEndOverlap;

// Hit events (blocking collision)
FComponentHitSignature OnComponentHit;
```

**Physics simulation**:
```cpp
void SetSimulatePhysics(bool bSimulate);
void SetEnableGravity(bool bGravityEnabled);
void AddForce(FVector Force, FName BoneName = NAME_None, bool bAccelChange = false);
void AddImpulse(FVector Impulse, FName BoneName = NAME_None, bool bVelChange = false);
void SetPhysicsLinearVelocity(FVector NewVel, bool bAddToCurrent = false);
FVector GetPhysicsLinearVelocity(FName BoneName = NAME_None);
```

---

## Mesh Components

### UStaticMeshComponent

**Header**: `Components/StaticMeshComponent.h`

A rendered mesh with pre-baked lighting. The mesh geometry does not deform. The workhorse for environment art — buildings, props, weapons, projectiles.

```cpp
UStaticMeshComponent* Mesh = CreateDefaultSubobject<UStaticMeshComponent>(TEXT("Mesh"));
SetRootComponent(Mesh);

// Set mesh from C++ (usually set via Blueprint or Details panel)
static ConstructorHelpers::FObjectFinder<UStaticMesh> MeshAsset(
    TEXT("/Game/Meshes/MyMesh"));
if (MeshAsset.Succeeded())
{
    Mesh->SetStaticMesh(MeshAsset.Object);
}

// Runtime mesh swap
Mesh->SetStaticMesh(NewMeshAsset);

// Material override
Mesh->SetMaterial(0, MaterialInstance);

// Mobility — set in constructor for performance
Mesh->SetMobility(EComponentMobility::Movable);
```

### USkeletalMeshComponent

**Header**: `Components/SkeletalMeshComponent.h`

A mesh with a skeleton (bone hierarchy) that drives deformation. Required for characters, creatures, and anything that needs animation. Supports AnimBP, montages, sockets, morph targets.

```cpp
USkeletalMeshComponent* CharMesh = CreateDefaultSubobject<USkeletalMeshComponent>(TEXT("CharMesh"));
CharMesh->SetupAttachment(RootComponent);

// Play animation montage
CharMesh->GetAnimInstance()->Montage_Play(AttackMontage);

// Get socket transform (for attaching weapons, spawning VFX)
FTransform SocketTransform = CharMesh->GetSocketTransform(TEXT("WeaponSocket"));

// Bone manipulation at runtime — SetBoneLocationByName is on UPoseableMeshComponent,
// not USkeletalMeshComponent. For driven bone transforms, use UPoseableMeshComponent:
// PoseableMesh->SetBoneLocationByName(TEXT("spine_01"), NewLocation, EBoneSpaces::WorldSpace);
```

### UInstancedStaticMeshComponent (ISMC)

**Header**: `Components/InstancedStaticMeshComponent.h`

Renders many instances of the same static mesh in a single draw call using GPU instancing. Essential for foliage, crowds, spawned duplicates (e.g. bullet casings on the ground).

```cpp
UInstancedStaticMeshComponent* ISMC = CreateDefaultSubobject<UInstancedStaticMeshComponent>(TEXT("ISMC"));
ISMC->SetStaticMesh(TreeMesh);

// Add instances
for (int32 i = 0; i < 1000; i++)
{
    FTransform InstanceTransform = GetRandomTransform();
    ISMC->AddInstance(InstanceTransform);
}

// Update a specific instance
ISMC->UpdateInstanceTransform(InstanceIndex, NewTransform, /*bWorldSpace=*/true);

// Remove instance
ISMC->RemoveInstance(InstanceIndex);
```

---

## Shape / Collision Components

These are invisible collision volumes used for overlap detection, trigger zones, and character collision. They have no visual representation in-game.

### UCapsuleComponent

**Header**: `Components/CapsuleComponent.h`

The standard root component for `ACharacter`. The vertical capsule shape is ideal for characters because it slides over small bumps and provides stable physics interaction.

```cpp
// ACharacter already creates this as its root — you rarely create it manually
// Access via ACharacter::GetCapsuleComponent()

UCapsuleComponent* Capsule = CreateDefaultSubobject<UCapsuleComponent>(TEXT("Capsule"));
SetRootComponent(Capsule);
Capsule->InitCapsuleSize(42.f, 96.f); // Radius, HalfHeight

// Collision profile
Capsule->SetCollisionProfileName(TEXT("Pawn"));
```

### UBoxComponent

**Header**: `Components/BoxComponent.h`

An axis-aligned box. Common for trigger zones, room boundaries, button hitboxes, and rectangular objects.

```cpp
UBoxComponent* TriggerBox = CreateDefaultSubobject<UBoxComponent>(TEXT("TriggerZone"));
TriggerBox->SetupAttachment(RootComponent);
TriggerBox->SetBoxExtent(FVector(200.f, 200.f, 100.f)); // Half extents
TriggerBox->SetCollisionProfileName(TEXT("Trigger"));
TriggerBox->OnComponentBeginOverlap.AddDynamic(this, &AMyActor::OnOverlapBegin);
```

### USphereComponent

**Header**: `Components/SphereComponent.h`

A sphere. Common for explosion radius checks, audio area triggers, and simple interactable zones.

```cpp
USphereComponent* DetectionRadius = CreateDefaultSubobject<USphereComponent>(TEXT("Detection"));
DetectionRadius->SetupAttachment(RootComponent);
DetectionRadius->SetSphereRadius(500.f);
DetectionRadius->SetCollisionProfileName(TEXT("Trigger"));
```

---

## Camera and View Components

### USpringArmComponent

**Header**: `GameFramework/SpringArmComponent.h`

Implements a "boom" arm with collision-aware retraction. Positions the camera behind a character with automatic obstruction avoidance. The standard third-person camera rig.

```cpp
SpringArmComp = CreateDefaultSubobject<USpringArmComponent>(TEXT("SpringArm"));
SpringArmComp->SetupAttachment(RootComponent);
SpringArmComp->TargetArmLength = 400.f;          // Boom length in cm
SpringArmComp->bUsePawnControlRotation = true;    // Rotate with controller yaw
SpringArmComp->bEnableCameraLag = true;           // Smooth follow
SpringArmComp->CameraLagSpeed = 8.f;

// Socket name for camera attachment
// SpringArmComp has a built-in socket: USpringArmComponent::SocketName
```

### UCameraComponent

**Header**: `Camera/CameraComponent.h`

Defines a camera view. When the owning actor is the ViewTarget, this component supplies the `FMinimalViewInfo` used for rendering.

```cpp
CameraComp = CreateDefaultSubobject<UCameraComponent>(TEXT("Camera"));
CameraComp->SetupAttachment(SpringArmComp, USpringArmComponent::SocketName);
CameraComp->bUsePawnControlRotation = false; // Spring arm handles it

// Field of view
CameraComp->FieldOfView = 90.f;

// Cinematic settings
CameraComp->PostProcessSettings.bOverride_DepthOfFieldFstop = true;
CameraComp->PostProcessSettings.DepthOfFieldFstop = 1.4f;
```

---

## Special Components

### UArrowComponent

**Header**: `Components/ArrowComponent.h`

Editor-only visualization arrow. Marks spawn points, projectile directions, patrol waypoints, and any directional reference that needs to be visible in the editor viewport but not in-game.

```cpp
ArrowComp = CreateDefaultSubobject<UArrowComponent>(TEXT("Arrow"));
ArrowComp->SetupAttachment(RootComponent);
ArrowComp->ArrowColor = FColor::Yellow;
ArrowComp->ArrowSize = 2.f;
ArrowComp->bHiddenInGame = true; // Not visible during play — editor only
```

### UChildActorComponent

**Header**: `Components/ChildActorComponent.h`

Embeds another actor inside this actor's component tree. The child actor lives at the component's world transform and moves with it. Useful for modular actors (building blocks, vehicle parts) and Blueprint actor graphs.

```cpp
UChildActorComponent* ChildActorComp = CreateDefaultSubobject<UChildActorComponent>(TEXT("ChildActor"));
ChildActorComp->SetupAttachment(RootComponent);
ChildActorComp->SetChildActorClass(AMyChildActor::StaticClass());

// Access the child actor at runtime (after BeginPlay)
AMyChildActor* Child = Cast<AMyChildActor>(ChildActorComp->GetChildActor());
```

**Warning**: Child actor BeginPlay is called after the parent's `PostInitializeComponents` but the exact timing relative to the parent's `BeginPlay` depends on whether the parent was spawned or level-placed. Always access child actors in or after `BeginPlay`, never in `PostInitializeComponents`.

### UWidgetComponent

**Header**: `Components/WidgetComponent.h` (UMG module)

Renders a `UUserWidget` as a 3D object in the world. Used for 3D UI on characters (health bars over enemies), interactive surfaces, and world-space HUDs.

```cpp
// Module dependency: add "UMG" to PublicDependencyModuleNames in .Build.cs

UWidgetComponent* HealthBarWidget = CreateDefaultSubobject<UWidgetComponent>(TEXT("HealthBar"));
HealthBarWidget->SetupAttachment(RootComponent);
HealthBarWidget->SetWidgetClass(UHealthBarWidget::StaticClass());
HealthBarWidget->SetDrawSize(FVector2D(200.f, 50.f));
HealthBarWidget->SetDrawAtDesiredSize(false);

// At runtime — get the widget instance and cast to your widget class
UHealthBarWidget* Widget = Cast<UHealthBarWidget>(HealthBarWidget->GetWidget());
if (Widget)
{
    Widget->SetHealthPercent(0.75f);
}
```

---

## Audio and Effects Components

### UAudioComponent

**Header**: `Components/AudioComponent.h`

Plays a sound (USoundBase, USoundCue, USoundWave) at the component's world location with 3D spatialization.

```cpp
UAudioComponent* AudioComp = CreateDefaultSubobject<UAudioComponent>(TEXT("Audio"));
AudioComp->SetupAttachment(RootComponent);
AudioComp->SetSound(IdleLoopSound);
AudioComp->bAutoActivate = false; // Don't play on spawn

// Runtime control
AudioComp->Play();
AudioComp->Stop();
AudioComp->FadeIn(2.0f);          // 2-second fade in
AudioComp->FadeOut(1.0f, 0.f);   // 1-second fade to silence then stop
AudioComp->SetVolumeMultiplier(0.5f);
AudioComp->SetPitchMultiplier(1.2f);
```

### UNiagaraComponent

**Header**: `NiagaraComponent.h` (Niagara module)

Instances a Niagara particle system at the component's location. Use for persistent effects (fire, smoke, shields) that live on the actor.

```cpp
// Module dependency: add "Niagara" to PublicDependencyModuleNames

UNiagaraComponent* FireFX = CreateDefaultSubobject<UNiagaraComponent>(TEXT("FireEffect"));
FireFX->SetupAttachment(RootComponent);
FireFX->SetAsset(FireNiagaraSystem);
FireFX->bAutoActivate = false;

// Runtime
FireFX->Activate();
FireFX->Deactivate();
FireFX->SetVariableFloat(TEXT("EmitterRate"), 100.f);
FireFX->SetVariableLinearColor(TEXT("FlameColor"), FLinearColor::Red);
```

---

## Physics and Simulation

### UPhysicsConstraintComponent

**Header**: `PhysicsEngine/PhysicsConstraintComponent.h`

A joint constraint between two physics bodies or between a body and the world. Used for hinges (doors, flaps), ball sockets (ragdoll joints), prismatic sliders (elevators), and breakable constraints.

```cpp
UPhysicsConstraintComponent* HingeConstraint = CreateDefaultSubobject<UPhysicsConstraintComponent>(TEXT("HingeConstraint"));
HingeConstraint->SetupAttachment(RootComponent);

// Constrain two bodies
HingeConstraint->SetConstrainedComponents(BodyA, NAME_None, BodyB, NAME_None);

// Configure as a hinge (rotation about X, locked Y/Z)
HingeConstraint->SetAngularSwing1Limit(ACM_Locked, 0.f);
HingeConstraint->SetAngularSwing2Limit(ACM_Locked, 0.f);
HingeConstraint->SetAngularTwistLimit(ACM_Free, 0.f);
```

---

## Component Decision Guide

| Need | Component |
|---|---|
| Logic only, no position | `UActorComponent` |
| Position anchor, no visuals | `USceneComponent` |
| Static environment mesh | `UStaticMeshComponent` |
| Animated character/creature | `USkeletalMeshComponent` |
| Thousands of same mesh | `UInstancedStaticMeshComponent` |
| Character collision root | `UCapsuleComponent` |
| Trigger zone (rectangular) | `UBoxComponent` |
| Trigger zone (radial) | `USphereComponent` |
| Third-person camera | `USpringArmComponent` + `UCameraComponent` |
| World-space UI | `UWidgetComponent` |
| Persistent particle effect | `UNiagaraComponent` |
| Spatial audio | `UAudioComponent` |
| Nested actor | `UChildActorComponent` |
| Editor-only direction marker | `UArrowComponent` |
| Physics joint | `UPhysicsConstraintComponent` |

---

## Finding Components at Runtime

```cpp
// Get a component by class — returns first match
UHealthComponent* Health = Actor->FindComponentByClass<UHealthComponent>();

// Get all components of a class
TArray<UStaticMeshComponent*> AllMeshes;
Actor->GetComponents<UStaticMeshComponent>(AllMeshes);

// Inline array variant (avoids heap allocation for small counts)
TInlineComponentArray<UPrimitiveComponent*> Primitives;
Actor->GetComponents(Primitives);

// By name
UActorComponent* Named = Actor->GetDefaultSubobjectByName(TEXT("HealthComponent"));

// Blueprint component query
Actor->FindComponentByInterface(UInteractable::StaticClass());
```

---

## Component Mobility and Performance

`EComponentMobility` must be set in the constructor. It cannot be changed at runtime for static lighting to be valid.

```cpp
// Static — fully baked lighting; cannot move at runtime
Mesh->SetMobility(EComponentMobility::Static);

// Stationary — baked shadows; can change color/intensity
Mesh->SetMobility(EComponentMobility::Stationary);

// Movable — dynamic lighting; can translate/rotate at runtime
Mesh->SetMobility(EComponentMobility::Movable);
```

Performance implication: `Movable` components cast dynamic shadows (expensive). Use `Static` for anything that never moves. Use `Movable` only when the component actually needs to translate, rotate, or scale at runtime.
