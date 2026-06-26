# Locomotion Setup Reference

This guide covers the end-to-end setup for character locomotion using UE5's
animation system: AnimInstance properties, blend spaces, state machines, and
layered blending.

Source headers referenced:
- `Engine/Source/Runtime/Engine/Classes/Animation/AnimInstance.h`
- `Engine/Source/Runtime/Engine/Classes/Animation/BlendSpace.h`
- `Engine/Source/Runtime/Engine/Classes/Animation/BlendSpace1D.h`
- `Engine/Source/Runtime/Engine/Classes/Animation/AimOffsetBlendSpace.h`

---

## AnimInstance: Locomotion Properties

```cpp
// LocomotionAnimInstance.h
#pragma once
#include "Animation/AnimInstance.h"
#include "LocomotionAnimInstance.generated.h"

UCLASS()
class MYGAME_API ULocomotionAnimInstance : public UAnimInstance
{
    GENERATED_BODY()

public:
    virtual void NativeInitializeAnimation() override;
    virtual void NativeUpdateAnimation(float DeltaSeconds) override;

protected:
    // Cached references (game thread only)
    UPROPERTY(Transient)
    TObjectPtr<ACharacter> OwningCharacter;

    UPROPERTY(Transient)
    TObjectPtr<UCharacterMovementComponent> MovementComp;

    // --- Properties read by the AnimGraph ---

    // Ground speed (XY plane), drives blend space Y axis
    UPROPERTY(Transient, BlueprintReadOnly, Category="Locomotion")
    float GroundSpeed = 0.f;

    // Movement direction relative to actor facing (-180 to 180), drives X axis
    UPROPERTY(Transient, BlueprintReadOnly, Category="Locomotion")
    float Direction = 0.f;

    // True when CharacterMovement reports IsFalling()
    UPROPERTY(Transient, BlueprintReadOnly, Category="Locomotion")
    bool bIsInAir = false;

    // True when velocity is near zero
    UPROPERTY(Transient, BlueprintReadOnly, Category="Locomotion")
    bool bIsIdle = true;

    // True when crouching
    UPROPERTY(Transient, BlueprintReadOnly, Category="Locomotion")
    bool bIsCrouching = false;

    // Acceleration magnitude, for start/stop transitions
    UPROPERTY(Transient, BlueprintReadOnly, Category="Locomotion")
    float Acceleration = 0.f;

    // For aim offset
    UPROPERTY(Transient, BlueprintReadOnly, Category="AimOffset")
    float AimYaw = 0.f;

    UPROPERTY(Transient, BlueprintReadOnly, Category="AimOffset")
    float AimPitch = 0.f;

    // Lean amount for banking in turns
    UPROPERTY(Transient, BlueprintReadOnly, Category="Locomotion")
    float LeanAmount = 0.f;

private:
    // Previous yaw for lean calculation
    float PreviousActorYaw = 0.f;
    float LeanVelocity = 0.f;
};
```

```cpp
// LocomotionAnimInstance.cpp
#include "LocomotionAnimInstance.h"
#include "GameFramework/Character.h"
#include "GameFramework/CharacterMovementComponent.h"
#include "Kismet/KismetMathLibrary.h"

static constexpr float IdleSpeedThreshold = 10.f;
static constexpr float LeanInterpSpeed    = 4.f;
static constexpr float LeanMaxAngle       = 30.f;

void ULocomotionAnimInstance::NativeInitializeAnimation()
{
    Super::NativeInitializeAnimation();

    OwningCharacter = Cast<ACharacter>(TryGetPawnOwner());
    if (OwningCharacter)
    {
        MovementComp = OwningCharacter->GetCharacterMovement();
        PreviousActorYaw = OwningCharacter->GetActorRotation().Yaw;
    }
}

void ULocomotionAnimInstance::NativeUpdateAnimation(float DeltaSeconds)
{
    Super::NativeUpdateAnimation(DeltaSeconds);

    if (!OwningCharacter || !MovementComp || DeltaSeconds <= 0.f) return;

    const FVector Velocity = MovementComp->Velocity;
    GroundSpeed  = Velocity.Size2D();
    bIsInAir     = MovementComp->IsFalling();
    bIsCrouching = MovementComp->IsCrouching();
    bIsIdle      = GroundSpeed < IdleSpeedThreshold && !bIsInAir;
    Acceleration = MovementComp->GetCurrentAcceleration().Size2D();

    // Direction: angle between velocity and actor facing
    if (GroundSpeed > IdleSpeedThreshold)
    {
        const FRotator ActorRot    = OwningCharacter->GetActorRotation();
        const FRotator VelocityRot = Velocity.ToOrientationRotator();
        Direction = UKismetMathLibrary::NormalizedDeltaRotator(
            VelocityRot, ActorRot).Yaw;
    }

    // Aim offset (yaw/pitch delta from actor to control rotation)
    const FRotator AimRot   = OwningCharacter->GetBaseAimRotation();
    const FRotator ActorRot = OwningCharacter->GetActorRotation();
    const FRotator AimDelta = UKismetMathLibrary::NormalizedDeltaRotator(
        AimRot, ActorRot);
    AimYaw   = FMath::Clamp(AimDelta.Yaw,   -90.f, 90.f);
    AimPitch = FMath::Clamp(AimDelta.Pitch, -90.f, 90.f);

    // Lean: angular velocity of actor yaw, smoothed with interp
    const float CurrentYaw   = OwningCharacter->GetActorRotation().Yaw;
    const float YawDeltaRate = UKismetMathLibrary::NormalizedDeltaRotator(
        FRotator(0.f, CurrentYaw, 0.f),
        FRotator(0.f, PreviousActorYaw, 0.f)).Yaw / DeltaSeconds;
    PreviousActorYaw = CurrentYaw;

    const float TargetLean = FMath::Clamp(YawDeltaRate / LeanMaxAngle, -1.f, 1.f);
    LeanAmount = FMath::FInterpTo(LeanAmount, TargetLean,
        DeltaSeconds, LeanInterpSpeed);
}
```

---

## Blend Space Setup

### 1D Blend Space — Walk/Run

**Asset**: `BS_GroundLocomotion1D` (type: `BlendSpace1D`)

| Axis  | Name    | Min | Max | Grid Points |
|-------|---------|-----|-----|-------------|
| X     | Speed   | 0   | 600 | 3           |

Samples:
| Speed | Animation       |
|-------|-----------------|
| 0     | Idle            |
| 200   | Walk_Fwd        |
| 600   | Run_Fwd         |

Interpolation (from `FInterpolationParameter`):
```
InterpolationTime = 0.15
InterpolationType = SpringDamper
DampingRatio      = 1.0
MaxSpeed          = 0.0  (unclamped)
```

In the AnimGraph, a **Blend Space 1D Player** node:
- Asset: `BS_GroundLocomotion1D`
- X pin: bound to `GroundSpeed` from the AnimInstance

---

### 2D Blend Space — Directional Locomotion

**Asset**: `BS_GroundLocomotion2D` (type: `BlendSpace`)

| Axis | Name      | Min  | Max | Grid Points |
|------|-----------|------|-----|-------------|
| X    | Direction | -180 | 180 | 5           |
| Y    | Speed     | 0    | 600 | 3           |

Sample layout (Direction x Speed):

```
Direction\Speed |  0 (Idle) | 200 (Walk) | 600 (Run)
----------------+-----------+------------+-----------
     0 (Fwd)    | Idle      | Walk_Fwd   | Run_Fwd
    90 (Right)  | Idle      | Walk_Right | Run_Right
   -90 (Left)   | Idle      | Walk_Left  | Run_Left
   180 (Bwd)    | Idle      | Walk_Bwd   | Run_Bwd
```

Idle is the same animation at all direction values and Speed=0; it is defined
at four direction points so the blend falls back to it cleanly.

Interpolation per axis:
```
X (Direction): InterpolationTime=0.10, InterpolationType=SpringDamper
Y (Speed):     InterpolationTime=0.15, InterpolationType=SpringDamper
```

In the AnimGraph, a **Blend Space Player** node:
- Asset: `BS_GroundLocomotion2D`
- X pin: `Direction`
- Y pin: `GroundSpeed`

---

### Aim Offset — Upper Body Aiming

**Asset**: `AO_Rifle` (type: `AimOffset`)

| Axis  | Name  | Min | Max |
|-------|-------|-----|-----|
| X     | Yaw   | -90 |  90 |
| Y     | Pitch | -90 |  90 |

Samples (5 poses, all additive relative to reference pose):

| Yaw | Pitch | Animation             |
|-----|-------|-----------------------|
| 0   | 0     | AO_Rifle_Center       |
| 90  | 0     | AO_Rifle_Right        |
| -90 | 0     | AO_Rifle_Left         |
| 0   | 90    | AO_Rifle_Up           |
| 0   | -90   | AO_Rifle_Down         |

In the AnimGraph:
- Place **Aim Offset** node after the base locomotion result
- X pin: `AimYaw`, Y pin: `AimPitch`
- This node applies an additive pose on top of the base pose

---

## State Machine Setup — Locomotion State Machine

**State Machine Name**: `LocomotionSM`

### States

```
[Entry] --> [Idle] --> [Walk/Run] --> [Idle]
                 \--> [Jump Start] --> [In Air] --> [Land] --> [Idle]
                 \--> [Crouch Idle] --> [Crouch Walk] --> [Crouch Idle]
```

### State Definitions

**Idle**
- Animation: Idle loop sequence or the 1D/2D blend space at Speed=0
- Transition to Walk/Run: `GroundSpeed > 10 && !bIsInAir`
- Transition to Jump Start: `bIsInAir`
- Transition to Crouch Idle: `bIsCrouching`

**Walk/Run**
- Animation: `BS_GroundLocomotion1D` or `BS_GroundLocomotion2D`
- Transition to Idle: `GroundSpeed <= 10 && !bIsInAir`
- Transition to Jump Start: `bIsInAir`

**Jump Start**
- Animation: `JumpStart` (plays once)
- Automatic transition to In Air when animation finishes:
  `TimeRemaining(ratio) < 0.1`

**In Air**
- Animation: `InAir` loop (often a blend between apex and falling poses)
- Transition to Land: `!bIsInAir`

**Land**
- Animation: `Land` (plays once)
- Automatic transition to Idle or Walk/Run when complete

**Crouch Idle**
- Animation: `CrouchIdle` loop
- Transition to Crouch Walk: `GroundSpeed > 3`
- Transition to Idle (stand): `!bIsCrouching`

**Crouch Walk**
- Animation: `BS_CrouchLocomotion1D` (separate blend space for crouch walk)
- Transition to Crouch Idle: `GroundSpeed <= 3`
- Transition to Idle: `!bIsCrouching`

### Transition Cross-Fade Settings

| From        | To          | Duration | Blend Curve  |
|-------------|-------------|----------|--------------|
| Idle        | Walk/Run    | 0.15s    | Cubic In-Out |
| Walk/Run    | Idle        | 0.20s    | Cubic In-Out |
| Walk/Run    | Jump Start  | 0.10s    | Linear       |
| In Air      | Land        | 0.05s    | Linear       |
| Land        | Idle        | 0.20s    | Cubic In-Out |
| Idle        | Crouch Idle | 0.15s    | Linear       |
| Crouch Idle | Idle        | 0.15s    | Linear       |

Use **Automatic Rule Based on Sequence Player** for states with a single
play-once animation (Jump Start, Land) to auto-transition when the animation
nears completion.

---

## AnimGraph Structure

```
[Output Pose]
    |
[Layered Blend Per Bone]  <-- upper body slot for montages
    |              |
[LocomotionSM]  [Slot 'UpperBody']
    |
[Aim Offset]        <-- aim yaw/pitch additive
    |
[Locomotion Blend Space Player]
```

### Full AnimGraph Node Order (Bottom to Top)

1. **Blend Space Player** (`BS_GroundLocomotion2D`) — base movement pose
2. **Aim Offset** (`AO_Rifle`) — additive aim layer on top of base
3. **State Machine** (`LocomotionSM`) — wraps steps 1 & 2 inside states
4. **Slot 'UpperBody'** — montage poses blend into upper body here
5. **Layered Blend Per Bone** — blends upper body slot over the state machine
   - Blend Poses 0: State Machine output (lower body + full)
   - Blend Poses 1: UpperBody slot
   - Layer Setup: `spine_01`, Depth=0, BlendDepth=1, MeshPoseBlendFactor=1
6. **Output Pose**

---

## Layered Blend Per Bone — Upper/Lower Split

To play attack montages on the upper body while keeping lower body locomotion:

In the AnimGraph:
1. Add a **Slot** node named `UpperBody` (create the slot in Skeleton settings).
2. Add a **Layered Blend Per Bone** node.
3. Connect the State Machine output to **Base Pose**.
4. Connect the `UpperBody` slot output to **Blend Poses 0**.
5. In the **Layer Setup** array, add entry:
   - Bone Name: `spine_01`
   - Blend Depth: `-1` (blend from the specified bone downward to root is
     unaffected; upward is fully blended)
   - Mesh Pose Blend Factor: 1.0
   - Inverse: unchecked (positive bones = upper body = get slot blend)

The montage must target the `UpperBody` slot. In C++:

```cpp
// Play on UpperBody slot only
AnimInst->Montage_Play(AttackMontage);
// AttackMontage must have its anim tracks assigned to the 'UpperBody' slot
// in the montage editor (SlotAnimTracks[0].SlotName = "UpperBody")
```

---

## Native State Machine Bindings

Bind C++ logic to state transitions without Blueprint:

```cpp
// In ULocomotionAnimInstance::NativeInitializeAnimation()

// Transition rule
AddNativeTransitionBinding(
    FName("LocomotionSM"),
    FName("Idle"),
    FName("Walk/Run"),
    FCanTakeTransition::CreateUObject(
        this, &ULocomotionAnimInstance::CanStartMoving),
    FName("IdleToMoving")
);

// State entry notification
AddNativeStateEntryBinding(
    FName("LocomotionSM"),
    FName("Land"),
    FOnGraphStateChanged::CreateUObject(
        this, &ULocomotionAnimInstance::OnLandStateEntered)
);
```

```cpp
bool ULocomotionAnimInstance::CanStartMoving() const
{
    return GroundSpeed > IdleSpeedThreshold && !bIsInAir;
}

void ULocomotionAnimInstance::OnLandStateEntered(
    const FAnimNode_StateMachine& SM,
    int32 PrevState,
    int32 NextState)
{
    // Play landing camera shake, rumble, etc.
    if (OwningCharacter)
    {
        // UGameplayStatics::PlayWorldCameraShake(...);
    }
}
```

---

## Modular Locomotion via Linked Anim Layers

For projects with multiple locomotion modes (ground, swimming, climbing,
zero-gravity), use the linked anim layer pattern instead of a monolithic state
machine.

### Interface Definition

Create `ULocomotionLayerInterface` (AnimLayerInterface Blueprint asset)
with a single layer function: `LocomotionLayer`.

### Main AnimInstance

The main `ABP_Character` has a **Linked Anim Layer** node targeting
`ULocomotionLayerInterface::LocomotionLayer`. Its output feeds directly into
the **Output Pose** (after any additive overlays).

### Layer Implementations

```cpp
// GroundLocomotionLayer.h — implements LocomotionLayerInterface
UCLASS()
class MYGAME_API UGroundLocomotionLayer : public UAnimInstance
{
    GENERATED_BODY()
    // ...same locomotion properties as above...
};

// ClimbingLocomotionLayer.h
UCLASS()
class MYGAME_API UClimbingLocomotionLayer : public UAnimInstance
{
    GENERATED_BODY()
    // Separate state machine / sequences for climbing
};
```

### Swapping at Runtime

```cpp
void AMyCharacter::EnterClimbing()
{
    if (UAnimInstance* AnimInst = GetMesh()->GetAnimInstance())
    {
        AnimInst->LinkAnimClassLayers(UClimbingLocomotionLayer::StaticClass());
    }
}

void AMyCharacter::ExitClimbing()
{
    if (UAnimInstance* AnimInst = GetMesh()->GetAnimInstance())
    {
        AnimInst->LinkAnimClassLayers(UGroundLocomotionLayer::StaticClass());
        // Or pass nullptr to reset all layers to defaults:
        // AnimInst->LinkAnimClassLayers(nullptr);
    }
}
```

The transition is automatically inertially blended when an **Inertialization**
node is placed in the main AnimGraph.

---

## Inertial Blending for Smooth Layer Transitions

Add an **Inertialization** node in the main AnimGraph between the linked layer
output and the Output Pose. When `LinkAnimClassLayers` is called, the system
will inertialize the transition using the blend duration configured on the
`FAnimNode_LinkedAnimGraph` node (`PendingBlendInDuration` /
`PendingBlendOutDuration`).

To request inertialization from C++:

```cpp
// Request a 0.2s inertialized blend for all slots in the "DefaultGroup"
AnimInst->RequestSlotGroupInertialization(FName("DefaultGroup"), 0.2f);
```

---

## Root Motion Configuration

| Mode                        | Description                                              |
|-----------------------------|----------------------------------------------------------|
| `NoRootMotionExtraction`    | Root bone moves normally; no extraction to component     |
| `IgnoreRootMotion`          | Root motion is extracted and discarded (root stays put)  |
| `RootMotionFromMontagesOnly`| Only montage root motion drives component movement       |
| `RootMotionFromEverything`  | All animations contribute root motion to component       |

For typical third-person games with CharacterMovementComponent:
```cpp
// In Character BP defaults or constructor:
GetMesh()->GetAnimInstance()->RootMotionMode =
    ERootMotionMode::RootMotionFromMontagesOnly;
```

In the `AnimInstance` class default:
```cpp
// Set in class constructor or CDO:
RootMotionMode = ERootMotionMode::RootMotionFromMontagesOnly;
```

For multiplayer, pair `RootMotionFromMontagesOnly` with GAS montage replication
so the server's `CharacterMovementComponent` processes root motion authoritatively.

---

## Common Locomotion Pitfalls

**Direction flips when speed is near zero**
- Only update `Direction` when `GroundSpeed > threshold`. Keep the last valid
  direction when the character is decelerating to idle, preventing the blend
  space from snapping.

**Blend space snapping on direction change**
- Use `SpringDamper` interpolation on the Direction axis with
  `InterpolationTime = 0.08–0.12`. Too low = snappy, too high = sluggish turns.

**Aim offset fighting the state machine**
- Ensure the Aim Offset node is placed inside the locomotion state (not outside
  the state machine), or apply it as an additive overlay after the state machine
  output, so it blends correctly during transitions.

**Crouch/stand transition pops**
- Ensure crouch and stand blend spaces share samples at Speed=0. The blend space
  sampler interpolates between them; if the idle samples differ significantly,
  use a short cross-fade on the Idle->Crouch Idle transition (0.15s+).

**Upper body slot not blending**
- Verify the montage's slot track is named exactly `UpperBody` (case-sensitive)
  and the Layered Blend Per Bone node references the same slot name. Mismatches
  result in the montage playing on the wrong slot or not blending at all.

**State machine transition not firing from C++**
- `AddNativeTransitionBinding` must be called in `NativeInitializeAnimation`,
  not in `BeginPlay` or later. The binding is registered against the compiled
  state machine before the AnimGraph evaluates.
