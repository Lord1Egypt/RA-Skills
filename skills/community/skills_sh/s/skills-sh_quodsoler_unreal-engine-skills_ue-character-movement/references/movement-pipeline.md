# Movement Pipeline

Detailed breakdown of CMC's internal movement execution, floor detection, and root motion replication.

---

## Phys* Function Flow

```
TickComponent(DeltaTime)
  |
  v
PerformMovement(DeltaTime)           [main entry point, protected]
  |
  +-- ControlledCharacterMove()       [applies input acceleration]
  |
  v
StartNewPhysics(DeltaTime, Iterations)
  |
  +-- switch (MovementMode)
  |     |
  |     +-- MOVE_Walking   --> PhysWalking(dt, iter)
  |     +-- MOVE_NavWalking --> PhysNavWalking(dt, iter)
  |     +-- MOVE_Falling    --> PhysFalling(dt, iter)
  |     +-- MOVE_Swimming   --> PhysSwimming(dt, iter)
  |     +-- MOVE_Flying     --> PhysFlying(dt, iter)
  |     +-- MOVE_Custom     --> PhysCustom(dt, iter)
  |
  v
[Inside each Phys* function:]
  CalcVelocity(dt, Friction, bFluid, BrakingDecel)
    |
    v
  SafeMoveUpdatedComponent(Delta, Rotation, bSweep, Hit)
    |
    +-- MoveUpdatedComponent()        [actual primitive move]
    +-- ResolvePenetration()          [if overlapping after move]
```

Each `Phys*` function may iterate multiple times within a single tick (up to `MaxSimulationIterations`) when sub-stepping is required, for example when a sweep hit blocks movement partway through the delta.

---

## Floor Detection Chain

```
FindFloor(CapsuleLocation, OutFloorResult, bCanUseCached, DownwardSweepResult)
  |
  v
ComputeFloorDist(CapsuleLocation, LineDistance, SweepDistance, OutResult, SweepRadius, DownwardSweepResult)
  |
  +-- 1. Capsule sweep downward (SweepDistance)
  |       - Uses capsule shape slightly smaller than actual (SweepRadius)
  |       - Tests bBlockingHit and surface angle vs WalkableFloorZ
  |
  +-- 2. Line trace downward (LineDistance)
  |       - From capsule center to below capsule bottom
  |       - Validates the sweep result at the exact contact point
  |       - Catches edges where the sweep capsule might miss
  |
  v
FFindFloorResult populated:
  bBlockingHit   = sweep found something
  bWalkableFloor = surface normal Z >= WalkableFloorZ
  bLineTrace     = result came from line trace fallback
  FloorDist      = distance from capsule bottom to floor (sweep)
  LineDist       = distance from line trace
  HitResult      = full FHitResult
```

`IsWalkableFloor()` returns `true` only when both `bBlockingHit` and `bWalkableFloor` are set. A blocking hit on a steep surface (above `WalkableFloorAngle`) returns `bBlockingHit = true` but `bWalkableFloor = false`.

---

## Step-Up Logic

When `PhysWalking` encounters a blocking hit during `SafeMoveUpdatedComponent`, it attempts a step-up if the obstacle height is within `MaxStepHeight`:

```
1. Hit blocking surface during horizontal move
2. Check obstacle height <= MaxStepHeight
3. Move capsule UP by MaxStepHeight
4. Move capsule FORWARD by remaining Delta
5. Move capsule DOWN to find new floor
6. If new floor is walkable:
     - Accept the step-up position
     - Continue walking
7. If no walkable floor found or obstacle too tall:
     - Revert to pre-step-up position
     - Slide along the wall or transition to falling
```

Step-up only triggers during walking mode. Characters in `MOVE_Falling` do not step up -- they slide along surfaces.

---

## PhysWalking Flow

```
PhysWalking(deltaTime, Iterations)
  |
  +-- CalcVelocity(dt, GroundFriction, false, BrakingDecelerationWalking)
  |
  +-- MoveAlongFloor(Velocity * dt, Hit)
  |     |
  |     +-- SafeMoveUpdatedComponent(Delta, Rotation, true, Hit)
  |     +-- If blocked: attempt SlideAlongSurface or StepUp
  |
  +-- FindFloor(NewLocation, FloorResult, false)
  |     |
  |     +-- If walkable floor found: maintain MOVE_Walking
  |     +-- If floor lost: SetMovementMode(MOVE_Falling)
  |     +-- If floor too steep: slide down or fall
  |
  +-- AdjustFloorHeight()
        |
        +-- Snap capsule to floor within tolerance
        +-- Prevents floating or sinking between frames
```

The `Iterations` parameter limits how many sub-steps occur if the character hits multiple surfaces in one frame. Each slide or step-up consumes an iteration.

---

## PhysFalling Flow

```
PhysFalling(deltaTime, Iterations)
  |
  +-- GetFallingLateralAcceleration()
  |     +-- Applies AirControl to lateral input
  |     +-- Scaled by GetAirControl() (0-1 range)
  |
  +-- CalcVelocity(dt, FallingLateralFriction, false, BrakingDecelerationFalling)
  |
  +-- Apply gravity: Velocity.Z += GetGravityZ() * dt
  |
  +-- SafeMoveUpdatedComponent(Velocity * dt, Rotation, true, Hit)
  |     |
  |     +-- If hit floor:
  |     |     +-- ProcessLanded(Hit)
  |     |     +-- FindFloor check
  |     |     +-- If walkable: SetMovementMode(MOVE_Walking)
  |     |     +-- ACharacter::Landed(Hit) called
  |     |
  |     +-- If hit wall:
  |           +-- HandleImpact(Hit)
  |           +-- SlideAlongSurface(Delta, 1-Hit.Time, Hit.Normal, Hit)
  |
  +-- If no hit: continue falling next frame
```

Air control: `AirControl` (0-1) scales the player's lateral input while falling. At 0, the character follows a pure ballistic arc. At 1, the character has full lateral control in air (feels unrealistic but common in platformers).

---

## Root Motion Replication

Root motion from `FRootMotionSource` replicates through the CMC's network prediction system.

```
[Server]
  ApplyRootMotionSource(Source)
    |
    +-- Source added to CurrentRootMotion.RootMotionSources
    +-- Each tick: accumulated into FRootMotionMovementParams
    +-- Applied during PerformMovement before physics
    +-- Included in server move response

[Client - Autonomous Proxy]
  Receives source via replication
    |
    +-- Applies locally for prediction
    +-- Corrections handled through normal FSavedMove replay
    +-- Source duration tracked independently

[Client - Simulated Proxy]
  Receives replicated movement result
    |
    +-- Smoothing applied via NetworkSmoothingMode
    +-- Root motion baked into final position/velocity
```

Key points:
- Root motion sources with `Duration < 0` run infinitely until explicitly removed with `RemoveRootMotionSource(InstanceName)`
- `AccumulateMode::Override` replaces velocity from other sources at the same or lower priority
- `AccumulateMode::Additive` stacks on top of existing velocity
- Animation root motion (`FRootMotionMovementParams` from `UAnimMontage`) takes a separate path: it is extracted from `UAnimInstance` each tick in `TickComponent`, accumulated in `RootMotionParams`, then applied in `PerformMovement`. This path is distinct from `FRootMotionSource` and is handled by the animation system, not the source list.
- Both paths merge in `PerformMovement` where the final delta is applied
