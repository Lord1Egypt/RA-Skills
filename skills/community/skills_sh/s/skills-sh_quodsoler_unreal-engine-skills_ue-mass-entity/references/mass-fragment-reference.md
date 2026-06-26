# Mass Fragment Reference

Built-in fragment types, shared fragments, and trait classes from the Mass Entity framework. All types verified from UE source headers.

---

## Per-Entity Fragments

| Fragment | Header | Key Fields | Purpose |
|----------|--------|------------|---------|
| `FTransformFragment` | `MassCommonFragments.h` | `FTransform Transform` | Entity world transform (location, rotation, scale) |
| `FMassVelocityFragment` | `MassMovementFragments.h` | `FVector Value` | Linear velocity vector |
| `FMassForceFragment` | `MassMovementFragments.h` | `FVector Value` | Applied force vector (consumed by velocity processor) |
| `FAgentRadiusFragment` | `MassCommonFragments.h` | `float Radius` | Agent collision/avoidance radius |
| `FMassMoveTargetFragment` | `MassNavigationFragments.h` | `FVector Center`, `float DesiredSpeed`, `FMassMovementAction Action` | Navigation move target with speed and action |
| `FMassRepresentationFragment` | `MassRepresentationFragments.h` | `EMassRepresentationType CurrentRepresentation`, `EMassRepresentationType PrevRepresentation` | Current and previous visual representation state |
| `FMassRepresentationLODFragment` | `MassRepresentationFragments.h` | `TEnumAsByte<EMassLOD::Type> LOD`, `TEnumAsByte<EMassLOD::Type> PrevLOD`, `EMassVisibility Visibility`, `float LODSignificance` | Per-entity LOD level and visibility state |

### FTransformFragment

The most common fragment. Stores a full `FTransform` with location, rotation, and scale. Access with `GetTransform()` (const) and `GetMutableTransform()` (mutable).

### FMassVelocityFragment / FMassForceFragment

Both store an `FVector Value` field. Forces are consumed by the velocity integration processor each frame. Velocity is then consumed by movement processors that update `FTransformFragment`.

### FMassMoveTargetFragment

Used by navigation and crowd systems. Contains the desired move target position, speed, and a movement action enum indicating the current navigation intent (move, stand, animate).

---

## Chunk Fragments

Chunk fragments (`FMassChunkFragment`) store per-memory-chunk data shared across all entities in a chunk. `FMassRepresentationLODFragment` is NOT a chunk fragment — it is a per-entity `FMassFragment` (see Per-Entity Fragments above). Use `AddChunkFragment<T>()` in `BuildContext` only for types that inherit `FMassChunkFragment`.

---

## Shared Fragments (Per-Archetype)

| Fragment | Type | Header | Key Fields |
|----------|------|--------|------------|
| `FMassRepresentationParameters` | Const Shared | `MassRepresentationFragments.h` | `EMassRepresentationType LODRepresentation[EMassLOD::Max]`, `float NotVisibleUpdateRate`, `bKeepLowResActors` |
| `FMassMovementParameters` | Const Shared | `MassMovementFragments.h` | `float MaxSpeed`, `float MaxAcceleration`, `float DefaultDesiredSpeed` |

### FMassRepresentationParameters

Immutable const shared fragment configuring visual representation for an archetype. Defines `LODRepresentation[EMassLOD::Max]` which maps each LOD level to an `EMassRepresentationType` (e.g. `StaticMeshInstance`, `HighResSpawnedActor`, `LowResSpawnedActor`, or `None`). Also controls update rate for non-visible entities and actor retention behavior. Set via `UMassVisualizationTrait`.

### FMassMovementParameters

Immutable const shared fragment defining movement constraints for an archetype. Contains `MaxSpeed`, `MaxAcceleration`, `DefaultDesiredSpeed`, and movement style configurations. No `MaxDeceleration` field exists — deceleration is handled implicitly via force/velocity integration. Used by movement processors to generate desired velocities.

---

## Trait Classes

Traits are `UMassEntityTraitBase` subclasses that add fragments to entity templates during `BuildTemplate()`.

| Trait | Header | Fragments Added | Purpose |
|-------|--------|----------------|---------|
| `UMassAssortedFragmentsTrait` | `MassEntityConfigAsset.h` | User-specified list | Add arbitrary fragments/tags via editor list |
| `UMassVisualizationTrait` | `MassVisualizationTrait.h` | `FMassRepresentationFragment`, `FMassRepresentationParameters` | ISM visualization setup with LOD |
| `UMassReplicationTrait` | `MassReplicationTrait.h` | Replication fragments | Network replication support |

### UMassAssortedFragmentsTrait

The simplest trait. Exposes an editable list of fragment `UScriptStruct` types in the editor. Each listed type is added to the entity archetype. Use for adding custom fragments without writing a custom trait class.

### UMassVisualizationTrait

Configures ISM-based rendering. Adds both the per-entity `FMassRepresentationFragment` and the const shared `FMassRepresentationParameters`. Configure mesh assets via `StaticMeshInstanceDesc` and LOD distances via `LODParams` directly on the trait in the entity config editor. Note: this class is soft-deprecated; prefer `UMassMovableVisualizationTrait` or `UMassStationaryVisualizationTrait` for new work.

### UMassReplicationTrait

Enables Mass entity replication for multiplayer. Adds the necessary replication fragments and registers entities with the Mass replication system. Requires the MassReplication plugin module.

---

## MassCrowd Fragments

| Type | Kind | Purpose |
|------|------|---------|
| `FMassCrowdTag` | Tag | Marks entity as part of the crowd system |
| `FMassCrowdLaneTrackingFragment` | Fragment | Tracks current ZoneGraph lane and position along it |

### MassCrowd Integration

Entities tagged with `FMassCrowdTag` are processed by `UMassCrowdSubsystem`. The lane tracking fragment maintains the entity's current lane ID, distance along the lane, and lane-relative offset.

ZoneGraph lanes define navigation paths as connected directed graphs. The crowd system handles:
- Lane assignment and transitions
- Density-based speed modulation
- Waiting slot allocation at intersections
- Avoidance between crowd agents

`UMassCrowdSubsystem` is thread-safe (`TMassExternalSubsystemTraits<UMassCrowdSubsystem>::GameThreadOnly = false`) and can be accessed from parallel processors via `AddSubsystemRequirement`.

---

## EMassRepresentationType Values

| Value | Description |
|-------|-------------|
| `StaticMeshInstance` | Instanced static mesh (most efficient, distant) |
| `HighResSpawnedActor` | Full actor spawned for high LOD (close-up, full gameplay) |
| `LowResSpawnedActor` | Reduced actor for low-res LOD |
| `None` | No visual representation |

## EMassLOD Values

| Value | Typical Usage |
|-------|--------------|
| `High` | Close to camera, actor representation |
| `Medium` | Mid-range, full ISM detail |
| `Low` | Far range, simplified ISM |
| `Off` | Beyond render distance, simulation only |

LOD transitions are managed by the representation system. Entities promoted to `HighResSpawnedActor` at high LOD significance gain full gameplay capabilities (collision, animation, interaction). When demoted back to `StaticMeshInstance` at lower LODs, the actor is returned to a pool.
