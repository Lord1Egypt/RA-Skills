# Anim Notify Reference

Source headers:
- `Engine/Source/Runtime/Engine/Classes/Animation/AnimNotifies/AnimNotify.h`
- `Engine/Source/Runtime/Engine/Classes/Animation/AnimNotifies/AnimNotifyState.h`

---

## Class Hierarchy

```
UObject
  ├── UAnimNotify              (point-in-time event)
  └── UAnimNotifyState         (duration event: Begin / Tick / End)
```

### UAnimNotify — Key Virtual Methods

```cpp
// UE5 signature (always override this one; UE4 signature is deprecated)
virtual void Notify(
    USkeletalMeshComponent* MeshComp,
    UAnimSequenceBase* Animation,
    const FAnimNotifyEventReference& EventReference);

// Fires synchronously during Montage_Advance (only when bIsNativeBranchingPoint = true)
virtual void BranchingPointNotify(FBranchingPointNotifyPayload& BranchingPointPayload);

// Display name shown in the editor timeline
virtual FString GetNotifyName_Implementation() const;
```

### UAnimNotifyState — Key Virtual Methods

```cpp
// UE5 signatures
virtual void NotifyBegin(USkeletalMeshComponent* MeshComp,
    UAnimSequenceBase* Animation, float TotalDuration,
    const FAnimNotifyEventReference& EventReference);

virtual void NotifyTick(USkeletalMeshComponent* MeshComp,
    UAnimSequenceBase* Animation, float FrameDeltaTime,
    const FAnimNotifyEventReference& EventReference);

virtual void NotifyEnd(USkeletalMeshComponent* MeshComp,
    UAnimSequenceBase* Animation,
    const FAnimNotifyEventReference& EventReference);

// Branching point variants (synchronous during Montage_Advance)
virtual void BranchingPointNotifyBegin(FBranchingPointNotifyPayload& Payload);
virtual void BranchingPointNotifyTick(FBranchingPointNotifyPayload& Payload, float DeltaTime);
virtual void BranchingPointNotifyEnd(FBranchingPointNotifyPayload& Payload);
```

---

## Built-In Notifies (Engine-Provided)

### UAnimNotify_PlaySound

**Header**: `AnimNotify_PlaySound.h`

Plays a `USoundBase` at a socket location when the notify fires.

Key properties:
```cpp
UPROPERTY(EditAnywhere, BlueprintReadWrite, Category="AnimNotify")
TObjectPtr<USoundBase> Sound;

UPROPERTY(EditAnywhere, BlueprintReadWrite, Category="AnimNotify")
float VolumeMultiplier = 1.f;

UPROPERTY(EditAnywhere, BlueprintReadWrite, Category="AnimNotify")
float PitchMultiplier = 1.f;

UPROPERTY(EditAnywhere, BlueprintReadWrite, Category="AnimNotify")
uint32 bFollow : 1;   // if true, sound component follows the socket

UPROPERTY(EditAnywhere, BlueprintReadWrite, Category="AnimNotify",
    meta=(EditCondition="bFollow"))
FName AttachName;     // socket or bone to attach to
```

Use for: footsteps, impacts, voice barks, weapon sounds.

---

### UAnimNotify_PlayParticleEffect

**Header**: `AnimNotify_PlayParticleEffect.h`

Spawns a `UParticleSystem` at a socket location.

Key properties:
```cpp
UPROPERTY(EditAnywhere, BlueprintReadWrite, Category="AnimNotify")
TObjectPtr<UParticleSystem> PSTemplate;

UPROPERTY(EditAnywhere, BlueprintReadWrite, Category="AnimNotify")
FName SocketName;

UPROPERTY(EditAnywhere, BlueprintReadWrite, Category="AnimNotify")
FVector LocationOffset;

UPROPERTY(EditAnywhere, BlueprintReadWrite, Category="AnimNotify")
FRotator RotationOffset;

UPROPERTY(EditAnywhere, BlueprintReadWrite, Category="AnimNotify")
bool bAttached;   // false = spawned at socket, not parented
```

Use for: muzzle flashes, hit sparks, ability cast effects.

---

### UAnimNotifyState_TimedParticleEffect

**Header**: `AnimNotifyState_TimedParticleEffect.h`

Activates a looping `UParticleSystem` for the duration of the notify state.
Deactivates (or destroys) on end.

Key properties:
```cpp
UPROPERTY(EditAnywhere, Category=ParticleSystem)
TObjectPtr<UParticleSystem> PSTemplate;

UPROPERTY(EditAnywhere, Category=ParticleSystem)
FName SocketName;

UPROPERTY(EditAnywhere, Category=ParticleSystem)
FVector LocationOffset;

UPROPERTY(EditAnywhere, Category=ParticleSystem)
FRotator RotationOffset;

UPROPERTY(EditAnywhere, Category=ParticleSystem,
    meta=(DisplayName="Destroy Immediately"))
bool bDestroyAtEnd;  // false = allow particles to complete their cycle
```

Use for: weapon trails, aura effects, charged attack indicators.

---

### UAnimNotifyState_DisableRootMotion

**Header**: `AnimNotifyState_DisableRootMotion.h`

Suppresses root motion extraction for the duration of the notify state.
Internally calls `PushDisableRootMotion()` on `FAnimMontageInstance` and
`PopDisableRootMotion()` at end.

Use for: ragdoll transitions, ability phases where motion is physics-driven.

---

### UAnimNotifyState_Trail

**Header**: `AnimNotifyState_Trail.h`

Spawns and manages a particle trail between two sockets. Used for sword trails,
cape effects, etc.

---

## Custom Notify Patterns

### Pattern 1 — Footstep with Surface Detection

```cpp
// FootstepNotify.h
#pragma once
#include "Animation/AnimNotifies/AnimNotify.h"
#include "FootstepNotify.generated.h"

UCLASS(meta=(DisplayName="Footstep"))
class MYGAME_API UFootstepNotify : public UAnimNotify
{
    GENERATED_BODY()

public:
    UFootstepNotify()
    {
        bIsNativeBranchingPoint = false; // queued, not synchronous
    }

    virtual void Notify(
        USkeletalMeshComponent* MeshComp,
        UAnimSequenceBase* Animation,
        const FAnimNotifyEventReference& EventReference) override;

    virtual FString GetNotifyName_Implementation() const override
    {
        return FString::Printf(TEXT("Footstep_%s"), *FootSocket.ToString());
    }

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category="Footstep")
    FName FootSocket = FName("foot_l");

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category="Footstep")
    float TraceDistance = 75.f;
};
```

```cpp
// FootstepNotify.cpp
#include "FootstepNotify.h"
#include "Components/SkeletalMeshComponent.h"
#include "PhysicalMaterials/PhysicalMaterial.h"
#include "Kismet/GameplayStatics.h"

void UFootstepNotify::Notify(
    USkeletalMeshComponent* MeshComp,
    UAnimSequenceBase* Animation,
    const FAnimNotifyEventReference& EventReference)
{
    Super::Notify(MeshComp, Animation, EventReference);

    if (!MeshComp || !MeshComp->GetWorld()) return;

    const FVector SocketLoc = MeshComp->GetSocketLocation(FootSocket);
    const FVector TraceStart = SocketLoc + FVector(0.f, 0.f, 20.f);
    const FVector TraceEnd   = SocketLoc - FVector(0.f, 0.f, TraceDistance);

    FHitResult Hit;
    FCollisionQueryParams Params(SCENE_QUERY_STAT(FootstepTrace), true);
    Params.AddIgnoredActor(MeshComp->GetOwner());
    Params.bReturnPhysicalMaterial = true;

    if (MeshComp->GetWorld()->LineTraceSingleByChannel(
            Hit, TraceStart, TraceEnd, ECC_Visibility, Params))
    {
        EPhysicalSurface Surface = UGameplayStatics::GetSurfaceType(Hit);
        // Dispatch footstep event to a surface manager or audio system
        // e.g. UFootstepSubsystem::Get(World)->PlayFootstep(Surface, Hit.ImpactPoint);
    }
}
```

---

### Pattern 2 — Weapon Collision Window (NotifyState)

```cpp
// WeaponCollisionNotifyState.h
#pragma once
#include "Animation/AnimNotifies/AnimNotifyState.h"
#include "WeaponCollisionNotifyState.generated.h"

UCLASS(meta=(DisplayName="Weapon Collision Window"))
class MYGAME_API UWeaponCollisionNotifyState : public UAnimNotifyState
{
    GENERATED_BODY()

public:
    virtual void NotifyBegin(
        USkeletalMeshComponent* MeshComp,
        UAnimSequenceBase* Animation,
        float TotalDuration,
        const FAnimNotifyEventReference& EventReference) override;

    virtual void NotifyEnd(
        USkeletalMeshComponent* MeshComp,
        UAnimSequenceBase* Animation,
        const FAnimNotifyEventReference& EventReference) override;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category="Weapon")
    FName WeaponComponentTag = FName("PrimaryWeapon");
};
```

```cpp
// WeaponCollisionNotifyState.cpp
#include "WeaponCollisionNotifyState.h"
#include "Components/SkeletalMeshComponent.h"
#include "GameFramework/Actor.h"

void UWeaponCollisionNotifyState::NotifyBegin(
    USkeletalMeshComponent* MeshComp,
    UAnimSequenceBase* Animation,
    float TotalDuration,
    const FAnimNotifyEventReference& EventReference)
{
    Super::NotifyBegin(MeshComp, Animation, TotalDuration, EventReference);

    if (!MeshComp) return;
    AActor* Owner = MeshComp->GetOwner();
    if (!Owner) return;

    // Enable weapon collision via interface or component lookup
    // IWeaponInterface::Execute_EnableCollision(WeaponActor);
}

void UWeaponCollisionNotifyState::NotifyEnd(
    USkeletalMeshComponent* MeshComp,
    UAnimSequenceBase* Animation,
    const FAnimNotifyEventReference& EventReference)
{
    Super::NotifyEnd(MeshComp, Animation, EventReference);

    if (!MeshComp) return;
    AActor* Owner = MeshComp->GetOwner();
    if (!Owner) return;

    // Disable weapon collision
}
```

---

### Pattern 3 — BranchingPoint Notify (Synchronous, Montage)

Use when you need to jump sections or stop a montage at a precise frame:

```cpp
// ComboBranchNotify.h
#pragma once
#include "Animation/AnimNotifies/AnimNotify.h"
#include "ComboBranchNotify.generated.h"

UCLASS(meta=(DisplayName="Combo Branch Point"))
class MYGAME_API UComboBranchNotify : public UAnimNotify
{
    GENERATED_BODY()

public:
    UComboBranchNotify()
    {
        // Marks this notify as always synchronous on montages
        bIsNativeBranchingPoint = true;
    }

    virtual void BranchingPointNotify(
        FBranchingPointNotifyPayload& BranchingPointPayload) override;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category="Combo")
    FName NextSection = FName("ComboEnd");
};
```

```cpp
// ComboBranchNotify.cpp
#include "ComboBranchNotify.h"
#include "Animation/AnimMontage.h"
#include "Animation/AnimInstance.h"
#include "Components/SkeletalMeshComponent.h"

void UComboBranchNotify::BranchingPointNotify(
    FBranchingPointNotifyPayload& Payload)
{
    Super::BranchingPointNotify(Payload);

    if (!Payload.SkelMeshComponent) return;

    UAnimInstance* AnimInst =
        Payload.SkelMeshComponent->GetAnimInstance();
    if (!AnimInst) return;

    // Redirect the montage timeline to a different section synchronously
    AnimInst->Montage_JumpToSection(NextSection);
}
```

---

### Pattern 4 — Named Notify + AnimInstance Delegate

For gameplay events (enabling abilities, triggering GAS effects) tied to
animation timing, use a **PlayMontageNotify** Blueprint node or the
`FPlayMontageAnimNotifyDelegate`:

```cpp
// From AnimInstance.h:
// DECLARE_DYNAMIC_MULTICAST_DELEGATE_TwoParams(FPlayMontageAnimNotifyDelegate,
//     FName, NotifyName, const FBranchingPointNotifyPayload&, BranchingPointPayload);

// Bind in C++ to receive named notify events:
void UMyAbilityComponent::BindMontageNotifies(UAnimInstance* AnimInst)
{
    AnimInst->OnPlayMontageNotifyBegin.AddDynamic(
        this, &UMyAbilityComponent::HandleNotifyBegin);
    AnimInst->OnPlayMontageNotifyEnd.AddDynamic(
        this, &UMyAbilityComponent::HandleNotifyEnd);
}

void UMyAbilityComponent::HandleNotifyBegin(
    FName NotifyName,
    const FBranchingPointNotifyPayload& Payload)
{
    if (NotifyName == FName("EnableHitbox"))
    {
        ActivateHitDetection();
    }
    else if (NotifyName == FName("ApplyGameplayEffect"))
    {
        ApplyDamageEffect();
    }
}

void UMyAbilityComponent::HandleNotifyEnd(
    FName NotifyName,
    const FBranchingPointNotifyPayload& Payload)
{
    if (NotifyName == FName("EnableHitbox"))
    {
        DeactivateHitDetection();
    }
}
```

---

## Tick Type Summary

| Tick Type       | Synchronous? | Use Case                                      |
|-----------------|-------------|-----------------------------------------------|
| Queued          | No          | VFX, SFX, gameplay events (safe, no re-entry) |
| BranchingPoint  | Yes         | Montage section jumps, precise loop control   |

Set in the montage editor per-notify, or via `bIsNativeBranchingPoint = true`
in the C++ constructor for native notifies.

---

## Notify Firing on Linked Instances

By default, notifies fire only on the AnimInstance that owns the animation.
To propagate across linked layers:

```cpp
// Main instance receives notifies from linked layers
AnimInst->SetReceiveNotifiesFromLinkedInstances(true);

// Linked layer propagates its notifies to the main instance
AnimInst->SetPropagateNotifiesToLinkedInstances(true);
```

Also controllable per-node in the `FAnimNode_LinkedAnimGraph` properties:
```cpp
// AnimNode_LinkedAnimGraph.h
uint8 bReceiveNotifiesFromLinkedInstances : 1;
uint8 bPropagateNotifiesToLinkedInstances : 1;
```

---

## Receiving Montage Notify Events Outside AnimInstance

To react to named montage notifies from code outside the `AnimInstance`, bind to the
`OnPlayMontageNotifyBegin` and `OnPlayMontageNotifyEnd` delegates exposed on
`UAnimInstance`:

```cpp
// In your owning actor / component — called after obtaining the AnimInstance.
AnimInst->OnPlayMontageNotifyBegin.AddDynamic(
    this, &AMyCharacter::HandleMontageNotifyBegin);

AnimInst->OnPlayMontageNotifyEnd.AddDynamic(
    this, &AMyCharacter::HandleMontageNotifyEnd);

// Callback signature (must be UFUNCTION):
UFUNCTION()
void HandleMontageNotifyBegin(FName NotifyName,
    const FBranchingPointNotifyPayload& Payload)
{
    if (NotifyName == FName("WeaponCollisionEnable"))
    {
        EnableWeaponCollision();
    }
}

UFUNCTION()
void HandleMontageNotifyEnd(FName NotifyName,
    const FBranchingPointNotifyPayload& Payload)
{
    if (NotifyName == FName("WeaponCollisionEnable"))
    {
        DisableWeaponCollision();
    }
}
```

These delegates fire for every branching-point or standard notify on any montage
playing on the instance, so always filter by `NotifyName`. Unbind with
`RemoveDynamic` when the listener is destroyed.
