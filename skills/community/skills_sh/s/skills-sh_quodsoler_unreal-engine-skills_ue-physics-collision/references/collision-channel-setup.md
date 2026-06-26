# Collision Channel Setup Reference

Reference for configuring custom collision channels, object types, and collision profiles in Unreal Engine 5 projects using the Chaos physics backend.

---

## Channel Slots Available

UE reserves the first 14 channels for built-in engine use. Projects have 18 custom slots:

| Enum                   | INI Key           | Typical Use             |
|------------------------|-------------------|-------------------------|
| `ECC_GameTraceChannel1`  | `TraceTypeQuery1` | Custom trace channel 1  |
| `ECC_GameTraceChannel2`  | `TraceTypeQuery2` | Custom trace channel 2  |
| ...through...          | ...               | ...                     |
| `ECC_GameTraceChannel18` | `TraceTypeQuery18`| Custom trace channel 18 |

The same slots serve as object type channels when `bTraceType=False`.

---

## DefaultEngine.ini Configuration

All custom channels and profiles go in `Config/DefaultEngine.ini` under `[/Script/Engine.CollisionProfile]`.

### Declaring a Custom Trace Channel

```ini
[/Script/Engine.CollisionProfile]
+DefaultChannelResponses=(Channel=ECC_GameTraceChannel1,DefaultResponse=ECR_Ignore,bTraceType=True,bStaticObject=False,Name="Weapon")
+DefaultChannelResponses=(Channel=ECC_GameTraceChannel2,DefaultResponse=ECR_Ignore,bTraceType=True,bStaticObject=False,Name="Interaction")
```

- `bTraceType=True` — this is a trace channel (used in `LineTraceSingleByChannel`, `SweepSingleByChannel`)
- `DefaultResponse` — response all components have unless overridden

### Declaring a Custom Object Type Channel

```ini
+DefaultChannelResponses=(Channel=ECC_GameTraceChannel3,DefaultResponse=ECR_Block,bTraceType=False,bStaticObject=False,Name="Interactable")
+DefaultChannelResponses=(Channel=ECC_GameTraceChannel4,DefaultResponse=ECR_Block,bTraceType=False,bStaticObject=True,Name="HazardZone")
```

- `bTraceType=False` — object channel (what an object IS, not what a trace uses)
- `bStaticObject=True` — object is non-moving (WorldStatic category behavior)

### Declaring Custom Profiles

```ini
; Weapon/projectile — blocks WorldStatic, WorldDynamic, Pawn; ignores triggers
+Profiles=(Name="Projectile",CollisionEnabled=QueryAndPhysics,ObjectTypeName="WorldDynamic",CustomResponses=(\
    (Channel="WorldStatic",Response=ECR_Block),\
    (Channel="WorldDynamic",Response=ECR_Block),\
    (Channel="Pawn",Response=ECR_Block),\
    (Channel="PhysicsBody",Response=ECR_Block),\
    (Channel="Weapon",Response=ECR_Ignore),\
    (Channel="Interaction",Response=ECR_Ignore)))

; Trigger volume — overlaps pawns, ignores everything else
+Profiles=(Name="TriggerPawn",CollisionEnabled=QueryOnly,ObjectTypeName="WorldDynamic",CustomResponses=(\
    (Channel="Pawn",Response=ECR_Overlap),\
    (Channel="WorldStatic",Response=ECR_Ignore),\
    (Channel="WorldDynamic",Response=ECR_Ignore),\
    (Channel="PhysicsBody",Response=ECR_Ignore)))

; Interactable object — visible to interaction traces, blocks world
+Profiles=(Name="Interactable",CollisionEnabled=QueryAndPhysics,ObjectTypeName="Interactable",CustomResponses=(\
    (Channel="WorldStatic",Response=ECR_Block),\
    (Channel="WorldDynamic",Response=ECR_Block),\
    (Channel="Pawn",Response=ECR_Block),\
    (Channel="Interaction",Response=ECR_Block),\
    (Channel="Weapon",Response=ECR_Ignore),\
    (Channel="Visibility",Response=ECR_Block)))
```

---

## Common Profile Setups

### Shooter Game — Standard Channels

```ini
; Weapon trace — hits everything physical, ignores other weapon traces
+DefaultChannelResponses=(Channel=ECC_GameTraceChannel1,DefaultResponse=ECR_Block,bTraceType=True,bStaticObject=False,Name="Weapon")

; Interaction trace — used by player to find interactable objects
+DefaultChannelResponses=(Channel=ECC_GameTraceChannel2,DefaultResponse=ECR_Ignore,bTraceType=True,bStaticObject=False,Name="Interaction")

; Interactable object type
+DefaultChannelResponses=(Channel=ECC_GameTraceChannel3,DefaultResponse=ECR_Block,bTraceType=False,bStaticObject=False,Name="Interactable")

; Damage volume object type
+DefaultChannelResponses=(Channel=ECC_GameTraceChannel4,DefaultResponse=ECR_Ignore,bTraceType=False,bStaticObject=False,Name="DamageVolume")
```

### Corresponding Profiles

```ini
; Player character — responds to weapon hits, can interact
+Profiles=(Name="PlayerPawn",CollisionEnabled=QueryAndPhysics,ObjectTypeName="Pawn",CustomResponses=(\
    (Channel="WorldStatic",Response=ECR_Block),\
    (Channel="WorldDynamic",Response=ECR_Block),\
    (Channel="Weapon",Response=ECR_Block),\
    (Channel="Interaction",Response=ECR_Block),\
    (Channel="Interactable",Response=ECR_Ignore),\
    (Channel="DamageVolume",Response=ECR_Overlap)))

; Pickup item — not hit by weapons, visible to interaction traces
+Profiles=(Name="Pickup",CollisionEnabled=QueryOnly,ObjectTypeName="Interactable",CustomResponses=(\
    (Channel="Pawn",Response=ECR_Overlap),\
    (Channel="WorldStatic",Response=ECR_Block),\
    (Channel="Weapon",Response=ECR_Ignore),\
    (Channel="Interaction",Response=ECR_Block),\
    (Channel="Visibility",Response=ECR_Block)))

; NPC enemy — blocks weapons and pawns
+Profiles=(Name="EnemyPawn",CollisionEnabled=QueryAndPhysics,ObjectTypeName="Pawn",CustomResponses=(\
    (Channel="WorldStatic",Response=ECR_Block),\
    (Channel="WorldDynamic",Response=ECR_Block),\
    (Channel="Pawn",Response=ECR_Block),\
    (Channel="Weapon",Response=ECR_Block),\
    (Channel="Interaction",Response=ECR_Ignore),\
    (Channel="Camera",Response=ECR_Ignore)))
```

---

## Applying Profiles in C++

```cpp
// Apply a named profile — sets ObjectType, CollisionEnabled, and all channel responses at once
MyMesh->SetCollisionProfileName(TEXT("PlayerPawn"));
MyMesh->SetCollisionProfileName(TEXT("Projectile"));
MyMesh->SetCollisionProfileName(TEXT("NoCollision"));

// Get the current profile name
FName ProfileName = MyMesh->GetCollisionProfileName();

// Override individual channel responses after setting a profile
MyMesh->SetCollisionResponseToChannel(ECC_Camera, ECR_Ignore);
```

---

## Referencing Custom Channels in C++

Custom trace channels map to `ETraceTypeQuery` for Blueprint functions and `ECollisionChannel` for C++ world queries.

```cpp
// Use the generated enum values — confirmed by checking Project Settings > Collision
// ECC_GameTraceChannel1 = "Weapon" (in our setup)
// ECC_GameTraceChannel2 = "Interaction"

FHitResult Hit;
FCollisionQueryParams Params;
Params.AddIgnoredActor(this);

// Weapon trace — using ECC directly
GetWorld()->LineTraceSingleByChannel(Hit, Start, End, ECC_GameTraceChannel1, Params);

// Interaction trace
GetWorld()->LineTraceSingleByChannel(Hit, Start, End, ECC_GameTraceChannel2, Params);

// Interaction trace by object type (finds Interactable objects)
FCollisionObjectQueryParams ObjectParams;
ObjectParams.AddObjectTypesToQuery(ECC_GameTraceChannel3); // Interactable type
GetWorld()->LineTraceSingleByObjectType(Hit, Start, End, ObjectParams, Params);
```

---

## ECollisionEnabled Quick Reference

| Value              | Query (Traces) | Physics (Forces/Sweep) | Typical Use                     |
|--------------------|---------------|------------------------|---------------------------------|
| `NoCollision`      | No            | No                     | Ghost/invisible actors          |
| `QueryOnly`        | Yes           | No                     | Trigger volumes, sensors        |
| `PhysicsOnly`      | No            | Yes                    | Invisible physics blockers      |
| `QueryAndPhysics`  | Yes           | Yes                    | Most gameplay objects           |
| `ProbeOnly`        | Probe only    | No                     | Contact data only (no query hits, no physics forces) |

---

## Physics Settings (Project Settings > Physics)

These values live in `Config/DefaultEngine.ini` under `[/Script/Engine.PhysicsSettings]` and map to `UPhysicsSettingsCore`:

```ini
[/Script/Engine.PhysicsSettings]
DefaultGravityZ=-980.000000
BounceThresholdVelocity=200.000000
FrictionCombineMode=Average
RestitutionCombineMode=Average
MaxAngularVelocity=3600.000000
MaxDepenetrationVelocity=0.000000
ContactOffsetMultiplier=0.020000
MinContactOffset=2.000000
MaxContactOffset=8.000000
bSimulateSkeletalMeshOnDedicatedServer=True
DefaultShapeComplexity=CTF_UseDefault
```

`DefaultShapeComplexity` accepts: `CTF_UseDefault`, `CTF_UseSimpleAndComplex`, `CTF_UseSimpleAsComplex`, `CTF_UseComplexAsSimple`.

---

## Collision Setup Checklist

When collision is not working as expected, verify in order:

1. **Both components have collision enabled** — `GetCollisionEnabled() != NoCollision`
2. **Response matrix is symmetric** — if A blocks B, B must block A for events
3. **Profile vs manual responses** — `SetCollisionProfileName` resets all manual responses; set per-channel overrides after the profile call
4. **Overlap events flag** — `bGenerateOverlapEvents` must be `true` on BOTH components for overlap events
5. **Hit events flag** — `bNotifyRigidBodyCollision` must be `true` for `OnComponentHit` to fire
6. **Physics enabled** — `bSimulatePhysics = true` required for physics-driven hits (`NormalImpulse` will be non-zero)
7. **Channel type** — trace channels vs object type channels use different query functions; mixing them gives no results
8. **Query layer** — `QueryOnly` components are invisible to physics-only queries and vice versa
