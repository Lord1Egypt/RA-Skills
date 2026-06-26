# PCG Node Reference

PCG nodes are categorized by their `EPCGSettingsType` enum value. Each node is a `UPCGSettings` subclass paired with a `FPCGElement` (or `IPCGElement`) that performs the actual work. Nodes connect through typed pins carrying `UPCGData`-derived objects.

---

## Data Flow Model

```
[Actor/Landscape/Spline Input] --> [Sampler] --> [Filter/Density] --> [Spawner] --> [Output]
                                        |
                                  [UPCGPointData]
                                  TArray<FPCGPoint>
                                  Each point has:
                                    FTransform Transform
                                    float      Density   (0..1)
                                    FVector    BoundsMin
                                    FVector    BoundsMax
                                    FVector4   Color
                                    int32      Seed
                                    int64      MetadataEntry
                                    float      Steepness
```

Data flows between nodes as `FPCGTaggedData` entries in an `FPCGDataCollection`. Each entry carries:
- `Data` — pointer to `UPCGData` subclass
- `Pin` — `FName` matching the target pin label
- `Tags` — `TSet<FString>` for filtering

---

## Standard Pin Labels

| Label constant | String value | Usage |
|---|---|---|
| `PCGPinConstants::DefaultInputLabel` | `"In"` | Default input pin |
| `PCGPinConstants::DefaultOutputLabel` | `"Out"` | Default output pin |
| `PCGPinConstants::DefaultParamsLabel` | `"Overrides"` | Overridable parameter input (was `"Params"` before 5.6) |

---

## Node Categories and Settings Types

### InputOutput (`EPCGSettingsType::InputOutput`)

**Get Actor Data** (`UPCGDataFromActorSettings`)
- Collects spatial data from actors tagged with a PCG tag.
- Produces: `UPCGSpatialData` (volume, surface, spline depending on actor components).
- Key fields: `ActorSelector` (tag, class, or explicit reference), `bParseActor`.

**Get Landscape Data** (`UPCGLandscapeData`)
- Wraps landscape heightfield as a surface for sampling.
- Produces: `UPCGLandscapeData`.

**Get Spline Data** (`UPCGSplineData`)
- Wraps `USplineComponent` as PCG spline data.
- Can be used as a surface boundary or point source.
- Produces: `UPCGSplineData`, `UPCGSplineInteriorSurfaceData`.

---

### Sampler (`EPCGSettingsType::Sampler`)

**Surface Sampler** (`UPCGSurfaceSamplerSettings`)
- Scatters points on a surface (landscape, mesh, spline-bounded area).
- Key fields:
  - `PointsPerSquaredMeter` — density of scatter
  - `PointExtents` — bounding box half-size per point
  - `Looseness` — boundary tolerance (0 = strict inside)
  - `bApplyDensityToPoints` — use surface density to reject points
  - `Seed` — deterministic seed for scatter
- Produces: `UPCGPointData`

**Spline Sampler** (`UPCGSplineSamplerSettings`)
- Generates points along a spline or inside a spline boundary.
- `Mode`: `Edge` (along spline), `Interior` (inside closed spline).
- `Dimension`: `OnSpline` (1D), `OnHorizontalSurface` (2D), `OnVolume` (3D).
- Key fields: `NumSegments`, `SubdivisionCount`, `Fill` mode.
- Produces: `UPCGPointData`

**Volume Sampler** (`UPCGVolumeSamplerSettings`)
- Samples points in 3D space within a volume.
- Key fields: `VoxelSize`.
- Produces: `UPCGPointData`

**Point Grid** (`UPCGCreatePointsGridSettings`)
- Creates a regular grid of points.
- Key fields: `CellSize`, `NumCells`, `Center`.
- Produces: `UPCGPointData`

**Point Sphere** (`UPCGCreatePointsSphereSettings`)
- Creates points on or inside a sphere.
- Key fields: `NumPoints`, `Radius`, `bFillSphere`.
- Produces: `UPCGPointData`

---

### Filter (`EPCGSettingsType::Filter`)

**Density Filter** (`UPCGDensityFilterSettings`)
- Removes points below a density threshold with optional random culling.
- Key fields: `LowerBound`, `UpperBound`, `bInvertFilter`, `Seed`.

**Attribute Filter** (`UPCGAttributeFilterSettings`)
- Filters points by metadata attribute comparison.
- Key fields: `TargetAttribute`, `Operator` (`==`, `!=`, `<`, `>`, `<=`, `>=`), `ConstantValue` or `OtherAttributeSource`.

**Bounds Check** (`UPCGCullPointsOutsideActorBoundsSettings`)
- Removes points outside the owning actor's bounding box.
- No required configuration beyond the node itself.

**Point Filter** (generic `UPCGFilterByAttributeSettings`)
- Keeps or removes points based on arbitrary attribute predicate.

---

### Density (`EPCGSettingsType::Density`)

**Density Noise** (`UPCGAttributeNoiseSettings` applied to density)
- Modulates point density using Perlin noise or other noise modes.
- Key fields: `NoiseMode` (`Perlin`, `Value`, etc.), `Frequency`, `Seed`, `InvertSourceDensity`.

**Density Remap** (`UPCGAttributeRemapSettings`)
- Remaps a numeric attribute from one range to another.
- Key fields: `SourceAttribute`, `InRange`, `OutRange`, `ClampOutput`.

**Blur** (`UPCGBlurSettings`)
- Blurs point attributes by averaging neighbor values.
- Key fields: `Iterations`, `KernelSize`.

---

### Spawner (`EPCGSettingsType::Spawner`)

**Static Mesh Spawner** (`UPCGStaticMeshSpawnerSettings`)
- Takes `UPCGPointData` and spawns `UHierarchicalInstancedStaticMeshComponent` instances.
- Key fields:
  - `MeshEntries` — weighted list of `FSoftObjectPath` mesh assets
  - `bOverrideDescriptors` — override ISM component properties per mesh
  - `InstancePackingMode` — `StaticMesh`, `Actor`, or `ISM`
- Uses `FPCGProceduralISMComponentDescriptor` (USTRUCT) for per-mesh ISM settings.

**Actor Spawner** (`UPCGSpawnActorSettings`)
- Spawns `AActor` subclasses at point positions.
- Key fields: `TemplateActor`, `SpawnMode` (bOverlapExisting, etc.), `PostSpawnFunction`.

**Create Spline** (`UPCGCreateSplineSettings`)
- Creates a `USplineComponent` from input point positions.
- Key fields: `bCreateFromInputPositions`, `SplineType`.

---

### Metadata (`EPCGSettingsType::Metadata`)

**Create Attribute** (`UPCGCreateAttributeSettings`)
- Adds a named metadata attribute to all points.
- Key fields: `OutputAttributeName`, `Type` (Float, Int, Vector, etc.), `DefaultValue`.

**Copy Attributes** (`UPCGCopyAttributesSettings`)
- Copies one or more attributes from source data to output.
- Key fields: `SourceAttributeNames`, `DestinationAttributeNames`.

**Attribute Noise** (`UPCGAttributeNoiseSettings`)
- Applies noise to any float/vector attribute.
- Key fields: `TargetAttribute`, `NoiseMode`, `Frequency`, `Amplitude`, `Seed`.

**Attribute Remap** (`UPCGAttributeRemapSettings`)
- Remaps attribute values between ranges with optional curves.

**Attribute Cast** (`UPCGAttributeCastSettings`)
- Casts attribute type (e.g., float to int, FVector to FVector2D).

**Break Transform** (`UPCGMetadataBreakTransformSettings`)
- Decomposes `FTransform` attribute into Translation, Rotation, Scale attributes.

**Make Transform** (`UPCGMetadataMakeTransformSettings`)
- Composes Translation, Rotation, Scale attributes into `FTransform`.

**Math Operations** (`UPCGMetadataMathsOpElementSettings`)
- Float/vector math: Add, Subtract, Multiply, Divide, Min, Max, Abs, Clamp, etc.
- Key fields: `Operation`, `InputA`, `InputB` (attributes or constants).

---

### ControlFlow (`EPCGSettingsType::ControlFlow`)

**Branch** (`UPCGBranchSettings`)
- Routes data to one of two output pins based on a bool attribute or parameter.
- Pins: `In`, `OutTrue`, `OutFalse`.

**Switch** (`UPCGSwitchSettings`)
- Routes data to N output pins based on an int or enum attribute.

**Boolean Select** (`UPCGBooleanSelectSettings`)
- Selects between two data inputs based on a bool parameter.

**Wait** (`UPCGWaitSettings`)
- Waits for upstream tasks to complete before forwarding data.
- Used to enforce ordering in asynchronous graphs.

**Quality Branch** (`UPCGQualityBranchSettings`)
- Branches based on current scalability/quality level.

---

### Subgraph (`EPCGSettingsType::Subgraph`)

**Subgraph** (`UPCGSubgraphSettings`)
- Executes a nested `UPCGGraph` as a subgraph node.
- Key fields: `SubgraphGraph` (asset reference), parameter overrides via `FPCGOverrideInstancedPropertyBag`.
- Subgraph pins match the subgraph's own input/output node pins.

---

### PointOps (`EPCGSettingsType::PointOps`)

**Copy Points** (`UPCGCopyPointsSettings`)
- Copies points from one dataset to positions defined by another (source into target).
- Key fields: `CopyMode` (FixedRotation, InheritRotation, etc.).

**Combine Points** (`UPCGCombinePointsSettings`)
- Merges two point datasets into one output.

**Collapse** (`UPCGCollapseSettings`)
- Merges nearby points into single representatives.
- Key fields: `CollapseRadius`.

**Attract** (`UPCGAttractSettings`)
- Displaces points toward or away from attractor points.
- Key fields: `Weight`, `Radius`, `FalloffType`.

**Bounds Modifier** (`UPCGBoundsModifierSettings`)
- Adjusts `BoundsMin`/`BoundsMax` per point.
- Key fields: `BoundsMode` (Set, Add, Scale), `Bounds`.

**Apply Scale to Bounds** (`UPCGApplyScaleToBoundsSettings`)
- Applies point scale to its bounds for accurate spatial queries.

---

### Grammar (`EPCGSettingsType::Generic` — Grammar namespace)

**Spline to Segment** (`UPCGSplineToSegmentSettings`)
- Converts a spline into discrete linear segments (points at control points).

**Subdivide Spline** (`UPCGSubdivideSplineSettings`)
- Inserts additional control points along a spline at regular intervals.

**Subdivide Segment** (`UPCGSubdivideSegmentSettings`)
- Subdivides linear segments into smaller sub-segments.

**Select Grammar** (`UPCGSelectGrammarSettings`)
- Applies L-system–style grammar rules to select/transform points.

**Duplicate Cross Sections** (`UPCGDuplicateCrossSectionsSettings`)
- Duplicates points at cross-section intervals along a spline.

---

### Blueprint Custom Nodes (`EPCGSettingsType::Blueprint`)

Derive from `UPCGBlueprintBaseElement`. Key configuration:

```cpp
UPROPERTY(BlueprintReadWrite, EditDefaultsOnly, Category = "Settings|Input & Output")
TArray<FPCGPinProperties> CustomInputPins;

UPROPERTY(BlueprintReadWrite, EditDefaultsOnly, Category = "Settings|Input & Output")
TArray<FPCGPinProperties> CustomOutputPins;

UPROPERTY(BlueprintReadWrite, EditDefaultsOnly, Category = Settings)
bool bIsCacheable = false;       // false if node creates actors/components

UPROPERTY(BlueprintReadWrite, EditDefaultsOnly, Category = Settings)
bool bRequiresGameThread = true; // true for actor spawn, component add
```

The `Execute` function signature:
```cpp
UFUNCTION(BlueprintNativeEvent, BlueprintCallable, Category = "PCG|Execution")
void Execute(const FPCGDataCollection& Input, FPCGDataCollection& Output);
```

---

## Graph Parameter System

Graph-level parameters (`FInstancedPropertyBag UserParameters` on `UPCGGraph`) allow exposing typed parameters to instances and Blueprints.

```cpp
// Read a parameter by name (typed template)
TValueOrError<float, EPropertyBagResult> Result =
    Graph->GetGraphParameter<float>(TEXT("SpawnRadius"));
if (Result.HasValue())
{
    float Radius = Result.GetValue();
}

// Write a parameter
Graph->SetGraphParameter<float>(TEXT("SpawnRadius"), 250.f);

// For instances, overrides are tracked per-property:
GraphInstance->UpdatePropertyOverride(Property, /*bMarkAsOverridden=*/true);
GraphInstance->ResetPropertyToDefault(Property);
bool bOverridden = GraphInstance->IsPropertyOverridden(Property);
```

Parameter change events (`EPCGGraphParameterEvent`):
`GraphChanged`, `GraphPostLoad`, `Added`, `RemovedUnused`, `RemovedUsed`, `PropertyMoved`, `PropertyRenamed`, `PropertyTypeModified`, `ValueModifiedLocally`, `ValueModifiedByParent`, `MultiplePropertiesAdded`, `UndoRedo`, `CategoryChanged`.

---

## PCGComponent Generation Modes

From `EPCGComponentGenerationTrigger`:

| Value | Behavior |
|---|---|
| `GenerateOnLoad` | Generates once when component registers (BeginPlay or editor load) |
| `GenerateOnDemand` | Only generates when `Generate()` or `GenerateLocal()` called explicitly |
| `GenerateAtRuntime` | Managed by `UPCGSubsystem` runtime scheduler; budget-limited per frame |

Input source (`EPCGComponentInput`):
- `Actor` — uses the owning actor's bounds and components
- `Landscape` — uses the landscape as the primary spatial input
- `Other` — custom `UPCGData` provided programmatically

Dirty flags (`EPCGComponentDirtyFlag`): `Actor`, `Landscape`, `Input`, `Data`, `All`.
Call `NotifyPropertiesChangedFromBlueprint()` to mark dirty and trigger conditional regeneration.

---

## Hierarchical Generation (HiGen)

Enable on `UPCGGraph`:
```cpp
bool bUseHierarchicalGeneration = true;
EPCGHiGenGrid HiGenGridSize = EPCGHiGenGrid::Grid256; // default grid cell size
uint32 HiGenExponential = 0; // shifts grid sizes up by this exponent
bool bUse2DGrid = true;      // 2D grid (XY plane) vs 3D volumetric
```

Grid sizes available: `Grid16`, `Grid32`, `Grid64`, `Grid128`, `Grid256`, `Grid512`, `Grid1024`, `Grid2048`, `GridUnbounded`.

Nodes run at the minimum of all incoming data grid sizes. Use `Get Grid Size` nodes to force execution at a specific resolution.

---

## ISM Descriptor (PCG Spawner)

`FPCGProceduralISMComponentDescriptor` (USTRUCT from `Components/PCGProceduralISMComponentDescriptor.h`) controls per-mesh ISM properties when spawned by the Static Mesh Spawner node:

Key settings mirrored from `UInstancedStaticMeshComponent`:
- `StaticMesh` — mesh asset
- `OverrideMaterials` — material slots
- `InstanceStartCullDistance` / `InstanceEndCullDistance`
- `InstanceLODDistanceScale`
- `bUseGpuLodSelection`
- `NumCustomDataFloats` — per-instance float channels
- Collision preset, body instance settings

---

## Compute (GPU) Nodes

PCG supports GPU-accelerated nodes via `UPCGComputeKernel` (UE 5.4+). These nodes implement `EPCGSettingsType::GPU` and execute HLSL kernels on the GPU point buffer. Useful for mass transforms, noise sampling, or attribute operations at millions of points.

Key classes: `UPCGComputeKernel`, `UPCGComputeSource`, `FPCGDataBinding`, `FPCGDataDescription`.

GPU nodes are identified by returning `EPCGSettingsType::GPU` from `GetType()` (override in your settings class) and must reference a `UPCGComputeKernel`-derived kernel asset with matching data binding descriptors.

---

## Determinism Checklist

For reproducible procedural results:
1. Set a fixed `Seed` on the `UPCGComponent` (or use actor position as seed input).
2. Use `GetSeedWithContext` in custom Blueprint nodes rather than `FMath::Rand`.
3. Ensure custom nodes set `bIsCacheable = true` when outputs depend only on inputs + seed.
4. For multiplayer: use `Generate(bForce)` (NetMulticast) not `GenerateLocal`.
5. Sort input point arrays before processing — order from `GetActorPCGData` is not guaranteed to be stable across platforms.
