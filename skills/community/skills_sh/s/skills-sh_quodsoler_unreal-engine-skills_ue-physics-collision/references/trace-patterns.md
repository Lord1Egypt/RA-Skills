# Trace Patterns Reference

Common trace query patterns for gameplay mechanics in Unreal Engine 5. All patterns use the C++ world query API (`UWorld::LineTraceSingleByChannel` etc.) with `FCollisionQueryParams`. For Blueprint-callable wrappers with built-in debug drawing, see `UKismetSystemLibrary`.

---

## Pattern 1: Hitscan Weapon

Single line trace from camera or muzzle, returning the first blocking hit. Reports impact point, surface normal, hit actor, and physical surface type for decal/sound selection.

```cpp
// MyWeaponComponent.h
UFUNCTION()
void FireHitscan(const FVector& MuzzleLocation, const FVector& AimDirection, float Range);

// MyWeaponComponent.cpp
void UMyWeaponComponent::FireHitscan(const FVector& MuzzleLocation,
                                      const FVector& AimDirection,
                                      float Range)
{
    const FVector TraceStart = MuzzleLocation;
    const FVector TraceEnd   = MuzzleLocation + AimDirection * Range;

    FCollisionQueryParams Params;
    Params.TraceTag          = TEXT("WeaponTrace");
    Params.bTraceComplex     = false;              // simple hull — sufficient for shooting
    Params.bReturnPhysicalMaterial = true;         // needed for surface type
    Params.AddIgnoredActor(GetOwner());            // don't hit self

    FHitResult Hit;
    const bool bHit = GetWorld()->LineTraceSingleByChannel(
        Hit,
        TraceStart,
        TraceEnd,
        ECC_GameTraceChannel1, // "Weapon" channel
        Params
    );

    if (bHit)
    {
        // Impact data
        const FVector  ImpactPoint  = Hit.ImpactPoint;
        const FVector  ImpactNormal = Hit.ImpactNormal;
        AActor*        HitActor     = Hit.GetActor();

        // Surface type for decal / sound selection
        EPhysicalSurface Surface = SurfaceType_Default;
        if (UPhysicalMaterial* PhysMat = Hit.PhysMaterial.Get())
        {
            Surface = UPhysicalMaterial::DetermineSurfaceType(PhysMat);
        }

        // Apply damage
        if (HitActor)
        {
            FPointDamageEvent DamageEvent(DamageAmount, Hit, AimDirection, DamageTypeClass);
            HitActor->TakeDamage(DamageAmount, DamageEvent, GetOwner()->GetInstigatorController(), GetOwner());
        }
    }

    // Debug draw (editor/development only)
#if ENABLE_DRAW_DEBUG
    DrawDebugLine(GetWorld(), TraceStart, bHit ? Hit.ImpactPoint : TraceEnd,
                  FColor::Red, false, 1.f, 0, 1.f);
    if (bHit) DrawDebugSphere(GetWorld(), Hit.ImpactPoint, 5.f, 8, FColor::Green, false, 1.f);
#endif
}
```

---

## Pattern 2: Melee Attack — Sphere Sweep

Sweeps a sphere along an arc for melee hit detection. Captures multiple targets in one call with `SweepMultiByChannel`. Avoids hitting the same actor twice.

```cpp
void UMeleeComponent::PerformMeleeSwing(const FVector& SwingStart,
                                         const FVector& SwingEnd,
                                         float AttackRadius)
{
    FCollisionShape Sphere = FCollisionShape::MakeSphere(AttackRadius);

    FCollisionQueryParams Params;
    Params.bTraceComplex = false;
    Params.AddIgnoredActor(GetOwner());

    TArray<FHitResult> Hits;
    const bool bAnyHit = GetWorld()->SweepMultiByChannel(
        Hits,
        SwingStart,
        SwingEnd,
        FQuat::Identity,
        ECC_Pawn,        // "Pawn" channel — hits characters and pawns
        Sphere,
        Params
    );

    // Deduplicate actors (sweep may return multiple hits per actor)
    TSet<AActor*> DamagedActors;
    for (const FHitResult& Hit : Hits)
    {
        AActor* HitActor = Hit.GetActor();
        if (HitActor && !DamagedActors.Contains(HitActor))
        {
            DamagedActors.Add(HitActor);
            HitActor->TakeDamage(MeleeDamage,
                                  FDamageEvent(),
                                  GetOwner()->GetInstigatorController(),
                                  GetOwner());
        }
    }

#if ENABLE_DRAW_DEBUG
    DrawDebugSphere(GetWorld(), SwingEnd, AttackRadius, 12, FColor::Orange, false, 0.5f);
#endif
}
```

---

## Pattern 3: Interaction / Use — Line Trace from Camera

Player looks at an object and presses interact. Uses a trace channel dedicated to interaction so non-interactable geometry is filtered automatically by the Interactable object type's channel response.

```cpp
// In PlayerController or Character

void AMyCharacter::TryInteract()
{
    APlayerController* PC = Cast<APlayerController>(GetController());
    if (!PC) return;

    FVector CameraLocation;
    FRotator CameraRotation;
    PC->GetPlayerViewPoint(CameraLocation, CameraRotation);

    const FVector TraceStart = CameraLocation;
    const FVector TraceEnd   = CameraLocation + CameraRotation.Vector() * InteractRange;

    FCollisionQueryParams Params;
    Params.AddIgnoredActor(this);

    FHitResult Hit;
    // Use object type query to find only Interactable objects
    FCollisionObjectQueryParams ObjectParams;
    ObjectParams.AddObjectTypesToQuery(ECC_GameTraceChannel3); // "Interactable" type

    const bool bHit = GetWorld()->LineTraceSingleByObjectType(
        Hit, TraceStart, TraceEnd, ObjectParams, Params
    );

    if (bHit)
    {
        if (AActor* HitActor = Hit.GetActor())
        {
            if (HitActor->GetClass()->ImplementsInterface(UInteractableInterface::StaticClass()))
            {
                IInteractableInterface::Execute_Interact(HitActor, this);
            }
        }
    }
}
```

---

## Pattern 4: Ground Detection / IsGrounded

Character or physics object checks whether it is on the ground. Uses a short downward line trace against WorldStatic and WorldDynamic. Common for jump/fall logic without relying on `CharacterMovementComponent`.

```cpp
bool UMyMovementComponent::IsGrounded() const
{
    const FVector Start = GetOwner()->GetActorLocation();
    const FVector End   = Start + FVector::DownVector * (GroundCheckDistance + CapsuleHalfHeight);

    FCollisionQueryParams Params;
    Params.bTraceComplex = false;
    Params.AddIgnoredActor(GetOwner());

    FHitResult Hit;
    const bool bHit = GetWorld()->LineTraceSingleByChannel(
        Hit,
        Start,
        End,
        ECC_Visibility,
        Params
    );

    return bHit && Hit.bBlockingHit;
}

// Slope normal — for movement alignment or sliding
FVector UMyMovementComponent::GetGroundNormal() const
{
    FHitResult Hit;
    const FVector Start = GetOwner()->GetActorLocation();
    const FVector End   = Start - FVector::UpVector * (GroundCheckDistance + CapsuleHalfHeight);

    FCollisionQueryParams Params;
    Params.bTraceComplex = false;
    Params.AddIgnoredActor(GetOwner());

    if (GetWorld()->LineTraceSingleByChannel(Hit, Start, End, ECC_Visibility, Params))
    {
        return Hit.ImpactNormal;
    }
    return FVector::UpVector;
}
```

---

## Pattern 5: Explosion Area-of-Effect — Sphere Overlap

Instant radial check at detonation point. Finds all Pawns and PhysicsBodies within radius. Applies damage with falloff.

```cpp
void AExplosiveActor::Detonate(const FVector& ExplosionCenter, float Radius, float MaxDamage)
{
    FCollisionShape Sphere = FCollisionShape::MakeSphere(Radius);

    FCollisionObjectQueryParams ObjectParams;
    ObjectParams.AddObjectTypesToQuery(ECC_Pawn);
    ObjectParams.AddObjectTypesToQuery(ECC_PhysicsBody);
    ObjectParams.AddObjectTypesToQuery(ECC_WorldDynamic);

    FCollisionQueryParams Params;
    Params.AddIgnoredActor(this);

    TArray<FOverlapResult> Overlaps;
    GetWorld()->OverlapMultiByObjectType(
        Overlaps,
        ExplosionCenter,
        FQuat::Identity,
        ObjectParams,
        Sphere,
        Params
    );

    TSet<AActor*> DamagedActors;
    for (const FOverlapResult& Result : Overlaps)
    {
        AActor* Actor = Result.GetActor();
        if (!Actor || DamagedActors.Contains(Actor)) continue;
        DamagedActors.Add(Actor);

        // Line of sight check — don't damage through walls
        FHitResult LOSHit;
        FCollisionQueryParams LOSParams;
        LOSParams.AddIgnoredActor(this);
        LOSParams.AddIgnoredActor(Actor);

        const FVector ActorCenter = Actor->GetActorLocation();
        const bool bBlocked = GetWorld()->LineTraceSingleByChannel(
            LOSHit, ExplosionCenter, ActorCenter, ECC_Visibility, LOSParams
        );
        if (bBlocked) continue; // wall between explosion and target

        // Damage falloff (linear)
        const float Distance  = FVector::Dist(ExplosionCenter, ActorCenter);
        const float Falloff   = FMath::Clamp(1.f - (Distance / Radius), 0.f, 1.f);
        const float Damage    = MaxDamage * Falloff;

        FRadialDamageEvent DmgEvent;
        DmgEvent.Params    = FRadialDamageParams(MaxDamage, 0.f, Radius, Radius, 1.f);
        DmgEvent.Origin    = ExplosionCenter;
        // FOverlapResult has no ToHitResult() — build FHitResult manually
        FHitResult ComponentHit(Result.GetActor(), Result.GetComponent(), ActorCenter, FVector::ZeroVector);
        DmgEvent.ComponentHits.Add(ComponentHit);

        Actor->TakeDamage(Damage, DmgEvent, GetInstigatorController(), this);

        // Radial impulse on physics bodies
        if (UPrimitiveComponent* PrimComp = Result.GetComponent())
        {
            if (PrimComp->IsSimulatingPhysics())
            {
                PrimComp->AddRadialImpulse(ExplosionCenter, Radius, ImpulseStrength,
                                            RIF_Linear, false);
            }
        }
    }

#if ENABLE_DRAW_DEBUG
    DrawDebugSphere(GetWorld(), ExplosionCenter, Radius, 16, FColor::Orange, false, 2.f);
#endif
}
```

---

## Pattern 6: Camera Line-of-Sight Check

Test whether a target actor is visible from the camera position, blocked by world geometry. Common for AI perception fallback or UI visibility indicators.

```cpp
bool AMyAIController::HasLineOfSightTo(AActor* Target) const
{
    if (!Target) return false;

    APawn* ControlledPawn = GetPawn();
    if (!ControlledPawn) return false;

    const FVector EyeLocation = ControlledPawn->GetPawnViewLocation();
    const FVector TargetLocation = Target->GetActorLocation();

    FCollisionQueryParams Params;
    Params.bTraceComplex  = false;
    Params.AddIgnoredActor(ControlledPawn);
    Params.AddIgnoredActor(Target);

    FHitResult Hit;
    const bool bBlocked = GetWorld()->LineTraceSingleByChannel(
        Hit,
        EyeLocation,
        TargetLocation,
        ECC_Visibility,
        Params
    );

    return !bBlocked; // no blocking hit means clear line of sight
}
```

---

## Pattern 7: Capsule Sweep for Character Movement Check

Before moving a character or vehicle to a new position, sweep a capsule to detect blocking geometry. Returns the first blocking hit to adjust the path.

```cpp
bool UMyMovementComponent::CanMoveToLocation(const FVector& TargetLocation) const
{
    const FVector CurrentLocation = GetOwner()->GetActorLocation();

    // Capsule matching the character's collision: radius 34, half-height 88 (standard UE character)
    FCollisionShape Capsule = FCollisionShape::MakeCapsule(34.f, 88.f);

    FCollisionQueryParams Params;
    Params.bTraceComplex  = false;
    Params.AddIgnoredActor(GetOwner());

    FHitResult Hit;
    const bool bHit = GetWorld()->SweepSingleByChannel(
        Hit,
        CurrentLocation,
        TargetLocation,
        FQuat::Identity,
        ECC_Pawn,
        Capsule,
        Params
    );

    if (bHit)
    {
        // Hit.Distance tells us how far we can actually move
        // Hit.ImpactNormal tells us the blocking surface orientation
        return false;
    }

    return true;
}
```

---

## Pattern 8: Async Trace for High-Frequency Sensors

For sensors that fire every frame on many actors (AI perception, grass interaction, liquid detection), synchronous traces stall the game thread. Use async traces queued this frame and read next frame.

```cpp
// .h
FTraceHandle PendingTraceHandle;
bool         bHasPendingTrace = false;

// .cpp — in Tick or timer callback

void UMySensorComponent::TickComponent(float DeltaTime, ELevelTick TickType,
                                        FActorComponentTickFunction* TickFunc)
{
    Super::TickComponent(DeltaTime, TickType, TickFunc);

    // Read result from last frame's trace
    if (bHasPendingTrace)
    {
        FTraceDatum Datum;
        if (GetWorld()->QueryTraceData(PendingTraceHandle, Datum))
        {
            bHasPendingTrace = false;
            if (Datum.OutHits.Num() > 0 && Datum.OutHits[0].bBlockingHit)
            {
                OnSensorHit(Datum.OutHits[0]);
            }
        }
    }

    // Queue this frame's trace (result readable next frame)
    if (!bHasPendingTrace)
    {
        FCollisionQueryParams Params;
        Params.AddIgnoredActor(GetOwner());

        const FVector Start = GetComponentLocation();
        const FVector End   = Start + GetForwardVector() * SensorRange;

        PendingTraceHandle = GetWorld()->AsyncLineTraceByChannel(
            EAsyncTraceType::Single,
            Start,
            End,
            ECC_Visibility,
            Params
        );
        bHasPendingTrace = true;
    }
}
```

---

## FCollisionQueryParams Quick Reference

```cpp
FCollisionQueryParams Params(
    TEXT("TraceName"),    // tag for profiling / debug drawing
    false,                // bTraceComplex — true for per-poly, false for simple hull
    GetOwner()            // actor to ignore (optional convenience constructor arg)
);

Params.bReturnPhysicalMaterial = true;  // populate Hit.PhysMaterial (slight cost)
Params.bReturnFaceIndex        = false; // populate Hit.FaceIndex (expensive, rarely needed)
Params.bFindInitialOverlaps    = true;  // report overlapping hits at Start position
Params.MobilityType = EQueryMobilityType::Any; // Any, Static, Dynamic

// Ignore specific actors or components
Params.AddIgnoredActor(SomeActor);
Params.AddIgnoredActors(ArrayOfActors);
Params.AddIgnoredComponent(SomeComponent);
```

---

## FCollisionShape Quick Reference

All shapes from `CollisionShape.h`:

```cpp
// Line — default, no volume (same as calling LineTrace functions directly)
FCollisionShape Line; // default constructor

// Sphere
FCollisionShape Sphere = FCollisionShape::MakeSphere(50.f); // radius in cm

// Box (axis-aligned, rotated by the Rotation parameter in sweep calls)
FCollisionShape Box = FCollisionShape::MakeBox(FVector(50.f, 30.f, 80.f)); // half-extents

// Capsule — HalfHeight includes the sphere radius at each end
FCollisionShape Capsule = FCollisionShape::MakeCapsule(34.f, 88.f);
// Capsule shaft half-length = HalfHeight - Radius = 88 - 34 = 54 cm

// Shape introspection
bool bSphere  = Sphere.IsSphere();
float Radius  = Sphere.GetSphereRadius();
float CHH     = Capsule.GetCapsuleHalfHeight();         // full half-height
float CAxisHL = Capsule.GetCapsuleAxisHalfLength();     // shaft only (HalfHeight - Radius)
FVector Ext   = Box.GetBox();                           // returns half-extents as FVector
```

---

## EDrawDebugTrace Reference (UKismetSystemLibrary)

```cpp
EDrawDebugTrace::None         // No debug drawing
EDrawDebugTrace::ForOneFrame  // Draw for one frame only
EDrawDebugTrace::ForDuration  // Draw for specified duration (DrawTime parameter)
EDrawDebugTrace::Persistent   // Draw until explicitly cleared
```

---

## Trace Performance Guidelines

| Technique | CPU cost | Use case |
|-----------|----------|----------|
| `LineTraceSingleByChannel` | Low | Shooting, interaction, simple AOS |
| `LineTraceMultiByChannel` | Medium | Penetration, multi-target beams |
| `SweepSingleByChannel` | Medium | Movement, precise melee |
| `SweepMultiByChannel` | Medium–High | Melee arc, projectile sweeping |
| `OverlapMultiByObjectType` | Medium | AoE, proximity detection |
| Complex collision (`bTraceComplex=true`) | High (4–10x) | Only when triangle accuracy needed |
| Async trace | Low (deferred) | Sensors, AI, effects polling >5 actors per frame |

**General rules:**
- Never run complex collision traces every tick for more than a handful of actors.
- Prefer `SweepSingle` over `SweepMulti` when only the first hit matters.
- Use `OverlapMultiByObjectType` for AoE — it is cheaper than multi-sweep for static positions.
- Group traces using `AsyncLineTraceByChannel` for sensors and background detection.
- Throttle non-critical traces with timers (5–10 Hz is sufficient for most AI awareness checks).
