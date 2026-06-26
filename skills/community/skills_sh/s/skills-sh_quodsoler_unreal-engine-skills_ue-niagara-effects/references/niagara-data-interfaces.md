# Niagara Data Interfaces — Built-In Reference

Data interfaces (DIs) extend Niagara scripts with external data sources that cannot be represented
as simple scalar/vector parameters. Each DI is a `UObject` subclass derived from
`UNiagaraDataInterface` (`NiagaraDataInterface.h`) or, for the base type, from
`UNiagaraDataInterfaceBase` (`NiagaraCore/NiagaraDataInterfaceBase.h`).

DIs appear in the Niagara editor as `User.*` parameters of DI type and are bound at runtime from
C++ using `UNiagaraFunctionLibrary` helpers or `SetVariableObject`. All DI classes listed here are
found under `Engine/Plugins/FX/Niagara/Source/Niagara/`.

---

## Mesh DIs

### UNiagaraDataInterfaceSkeletalMesh
**Header**: `Classes/NiagaraDataInterfaceSkeletalMesh.h`
**Module**: `Niagara`
**Sim target**: CPU + GPU (partial)

Samples positions, normals, UV coordinates, and bone transforms from a live
`USkeletalMeshComponent`. The mesh is skinned at the moment of sampling — particles can follow
bones or spawn from surface regions.

**Runtime binding from C++**:
```cpp
// Preferred: bind by component reference.
UNiagaraFunctionLibrary::OverrideSystemUserVariableSkeletalMeshComponent(
    NiagaraComp, TEXT("User.SourceMesh"), SkeletalMeshComp
);

// Restrict to specific bones (destructive modification of DI instance data).
UNiagaraFunctionLibrary::SetSkeletalMeshDataInterfaceFilteredBones(
    NiagaraComp, TEXT("User.SourceMesh"), { FName("spine_01"), FName("head") }
);

// Restrict to sampling regions defined in the SkeletalMesh asset's LOD settings.
UNiagaraFunctionLibrary::SetSkeletalMeshDataInterfaceSamplingRegions(
    NiagaraComp, TEXT("User.SourceMesh"), { FName("UpperBody") }
);

// Restrict to named sockets only.
UNiagaraFunctionLibrary::SetSkeletalMeshDataInterfaceFilteredSockets(
    NiagaraComp, TEXT("User.SourceMesh"), { FName("foot_l_socket") }
);

// Direct access for advanced mutation.
UNiagaraDataInterfaceSkeletalMesh* SkelDI =
    UNiagaraFunctionLibrary::GetDataInterface<UNiagaraDataInterfaceSkeletalMesh>(
        NiagaraComp, FName("User.SourceMesh")
    );
```

**Key properties** (set in Niagara editor or via direct DI mutation):
- `SourceMode` — `Default`, `Source`, `AttachParent`, `DefaultMesh`, `MeshParameterBinding`
- `SoftSourceActor` — soft actor reference; the DI resolves its `USkeletalMeshComponent`
- `FilteredBones`, `FilteredSockets`, `SamplingRegions` — sampling restrictions
- `bRequireCurrentFrameData` — whether to wait for skinning to complete this frame

**Notes**:
- Requires `bAllowCPUAccess` on the `USkeletalMesh` asset for CPU sampling.
- Pre-skinned vertex positions (`bUsesPreSkinnedVerts`) require `bCacheSampledData` on the
  mesh's LOD settings.
- Not all functions work on GPU sim; check Niagara editor warnings.

---

### UNiagaraDataInterfaceStaticMesh
**Header**: `Internal/DataInterface/NiagaraDataInterfaceStaticMesh.h`
**Module**: `Niagara`
**Sim target**: CPU + GPU (partial)

Samples vertex positions, normals, UV coordinates, and socket transforms from a static mesh.
Supports per-section filtering and instanced static mesh instance selection.

**Runtime binding from C++**:
```cpp
// Bind by component.
UNiagaraFunctionLibrary::OverrideSystemUserVariableStaticMeshComponent(
    NiagaraComp, TEXT("User.ScatterMesh"), StaticMeshComp
);

// Bind by raw asset.
UNiagaraFunctionLibrary::OverrideSystemUserVariableStaticMesh(
    NiagaraComp, TEXT("User.ScatterMesh"), MyStaticMesh
);

// Set which ISM instance to read from.
UNiagaraDataInterfaceStaticMesh::SetNiagaraStaticMeshDIInstanceIndex(
    NiagaraComp, FName("User.ScatterMesh"), InstanceIndex
);
```

**Key properties**:
- `SourceMode` — `ENDIStaticMesh_SourceMode::Default/Source/AttachParent/DefaultMeshOnly/MeshParameterBinding`
- `DefaultMesh` — fallback `UStaticMesh*` used when no runtime override is bound
- `SectionFilter.AllowedMaterialSlots` — restricts triangle sampling to specific material slots
- `LODIndex` — which LOD to sample; negative index counts back from highest LOD
- `bCaptureTransformsPerFrame` — update mesh-to-world transform each tick (default true)
- `bAllowSamplingFromStreamingLODs` — allows sampling from streaming LODs

**Notes**:
- Requires `bAllowCPUAccess` on the static mesh asset for CPU sampling.
- Set `bAllowSamplingFromStreamingLODs=false` on mobile to avoid streaming stalls.

---

## Curve DIs

All curve DIs derive from `UNiagaraDataInterfaceCurveBase` and provide a `SampleCurve(time)` function
to Niagara scripts. Internally they build a LUT (look-up table) at load time for GPU sampling.

### UNiagaraDataInterfaceCurve
**Header**: `Classes/NiagaraDataInterfaceCurve.h`
**Niagara type**: "Curve for Floats"
**Output**: `float`

```cpp
// Mutate keys at runtime (rebuilds LUT).
UNiagaraDataInterfaceCurve* CurveDI =
    UNiagaraFunctionLibrary::GetDataInterface<UNiagaraDataInterfaceCurve>(
        NiagaraComp, FName("User.SpeedCurve")
    );
if (CurveDI)
{
    CurveDI->Curve.Reset();
    CurveDI->Curve.AddKey(0.f, 0.f);
    CurveDI->Curve.AddKey(0.5f, 1.f);
    CurveDI->Curve.AddKey(1.f, 0.f);
    // UNiagaraDataInterface derives from UObject, not UActorComponent —
    // MarkRenderStateDirty() does not exist on this hierarchy.
    // UpdateLUT() rebuilds the GPU look-up table (WITH_EDITORONLY_DATA only).
#if WITH_EDITORONLY_DATA
    CurveDI->UpdateLUT();
#endif
}
```

### UNiagaraDataInterfaceVectorCurve
**Header**: `Classes/NiagaraDataInterfaceVectorCurve.h`
**Niagara type**: "Curve for Vectors"
**Output**: `FVector` (XYZ channels via three `FRichCurve`)

```cpp
UNiagaraDataInterfaceVectorCurve* VecCurveDI =
    UNiagaraFunctionLibrary::GetDataInterface<UNiagaraDataInterfaceVectorCurve>(
        NiagaraComp, FName("User.VelocityCurve")
    );
// Properties: XCurve, YCurve, ZCurve (each FRichCurve).
```

### UNiagaraDataInterfaceColorCurve
**Header**: `Classes/NiagaraDataInterfaceColorCurve.h`
**Niagara type**: "Curve for Colors"
**Output**: `FLinearColor` (RGBA channels via four `FRichCurve`)

### UNiagaraDataInterfaceVector2DCurve
**Header**: `Classes/NiagaraDataInterfaceVector2DCurve.h`
**Niagara type**: "Curve for Vector 2Ds"
**Output**: `FVector2D`

### UNiagaraDataInterfaceVector4Curve
**Header**: `Classes/NiagaraDataInterfaceVector4Curve.h`
**Niagara type**: "Curve for Vector 4s"
**Output**: `FVector4`

---

## Array DIs

Array DIs hold a `TArray` of typed data that Niagara scripts index into at runtime. They are the
primary mechanism for pushing per-frame C++ arrays into GPU/CPU simulations.

All array DIs derive from `UNiagaraDataInterfaceArray` (`Classes/NiagaraDataInterfaceArray.h`).

| DI Class | Element Type | Header |
|---|---|---|
| `UNiagaraDataInterfaceArrayFloat` | `float` | `Classes/NiagaraDataInterfaceArrayFloat.h` |
| `UNiagaraDataInterfaceArrayFloat2` | `FVector2f` (internal) / `FVector2D` (API) | same |
| `UNiagaraDataInterfaceArrayFloat3` | `FVector3f` (internal) / `FVector` (API) | same |
| `UNiagaraDataInterfaceArrayFloat4` | `FVector4f` (internal) / `FVector4` (API) | same |
| `UNiagaraDataInterfaceArrayPosition` | `FNiagaraPosition` | same |
| `UNiagaraDataInterfaceArrayColor` | `FLinearColor` | same |
| `UNiagaraDataInterfaceArrayQuat` | `FQuat4f` (internal) / `FQuat` (API) | same |
| `UNiagaraDataInterfaceArrayMatrix` | `FMatrix44f` (internal) / `FMatrix` (API) | same |
| `UNiagaraDataInterfaceArrayInt32` | `int32` | `Classes/NiagaraDataInterfaceArrayInt.h` |

**Runtime population from C++** (see also `niagara-parameter-types.md` for full method list):
```cpp
#include "NiagaraDataInterfaceArrayFunctionLibrary.h"

TArray<FVector> PositionArray = BuildPositions();
UNiagaraDataInterfaceArrayFunctionLibrary::SetNiagaraArrayVector(
    NiagaraComp, FName("User.SpawnPositions"), PositionArray
);
```

**Direct property access** (avoids function library overhead for large arrays):
```cpp
UNiagaraDataInterfaceArrayFloat* FloatArrayDI =
    UNiagaraFunctionLibrary::GetDataInterface<UNiagaraDataInterfaceArrayFloat>(
        NiagaraComp, FName("User.HeatData")
    );
if (FloatArrayDI)
{
    FloatArrayDI->FloatData = MoveTemp(NewFloatData);
    // UNiagaraDataInterface derives from UObject, not UActorComponent —
    // MarkRenderStateDirty() does not exist on this hierarchy.
    // The engine re-uploads array data automatically on the next simulation tick.
}
```

---

## Texture DIs

### UNiagaraDataInterfaceTexture
**Header**: `Classes/NiagaraDataInterfaceTexture.h`
**Sim target**: CPU + GPU

Samples from a `UTexture2D` or `UTextureRenderTarget2D`. Provides `SampleTexture2D(UV)`.

```cpp
UNiagaraFunctionLibrary::SetTextureObject(NiagaraComp, TEXT("User.FlowTexture"), MyTexture2D);
// or via SetVariableTexture:
NiagaraComp->SetVariableTexture(FName("User.FlowTexture"), MyTexture);
```

### UNiagaraDataInterface2DArrayTexture
**Header**: `Classes/NiagaraDataInterface2DArrayTexture.h`
**Sim target**: GPU only

Samples from a `UTexture2DArray`.

```cpp
UNiagaraFunctionLibrary::SetTexture2DArrayObject(NiagaraComp, TEXT("User.TexArray"), MyTexArray);
```

### UNiagaraDataInterfaceVolumeTexture
**Header**: `Classes/NiagaraDataInterfaceVolumeTexture.h`
**Sim target**: GPU only

Samples from a `UVolumeTexture`.

```cpp
UNiagaraFunctionLibrary::SetVolumeTextureObject(NiagaraComp, TEXT("User.DensityVol"), MyVolumeTexture);
```

### UNiagaraDataInterfaceCubeTexture
**Header**: `Classes/NiagaraDataInterfaceCubeTexture.h`
**Sim target**: GPU only

Samples from a `UTextureCube`.

### UNiagaraDataInterfaceRenderTarget2D
**Header**: `Classes/NiagaraDataInterfaceRenderTarget2D.h`
**Sim target**: GPU (read/write)

Read-write GPU render target. Used for simulation caching and fluid-like effects.

---

## Noise DIs

### UNiagaraDataInterfaceCurlNoise
**Header**: `Classes/NiagaraDataInterfaceCurlNoise.h`
**Sim target**: CPU + GPU

Provides 3D curl noise for divergence-free velocity fields. No runtime parameters — configure
`ModificationMode` and `NoiseStrength` in the Niagara editor.

---

## Simulation / Grid DIs

### UNiagaraDataInterfaceGrid2DCollection
**Header**: `Classes/NiagaraDataInterfaceGrid2DCollection.h`
**Sim target**: GPU only

2D grid of simulation data (textures). Used for fluid simulation and cellular automata effects.
Requires GPU sim mode. Not configurable from C++ directly — set up in Niagara editor.

### UNiagaraDataInterfaceGrid3DCollection
**Header**: `Classes/NiagaraDataInterfaceGrid3DCollection.h`
**Sim target**: GPU only

3D volumetric grid. Used for Niagara Fluids and volumetric simulations.

### UNiagaraDataInterfaceNeighborGrid3D
**Header**: `Classes/NiagaraDataInterfaceNeighborGrid3D.h`
**Sim target**: GPU only

Spatial hash grid for neighbor queries between particles.

---

## Collision DIs

### UNiagaraDataInterfaceCollisionQuery
**Header**: `Classes/NiagaraDataInterfaceCollisionQuery.h`
**Sim target**: CPU (sync) + GPU (async via HWRT)

Allows Niagara particles to perform physics collision traces. CPU mode executes synchronous line
traces; GPU mode uses hardware ray tracing (HWRT) when available.

For GPU HWRT, manage collision groups from C++:
```cpp
// Assign a collision group to a primitive so GPU particles can filter against it.
UNiagaraFunctionLibrary::SetComponentNiagaraGPURayTracedCollisionGroup(
    this, MyPrimitiveComp, CollisionGroupIndex
);

// Acquire a free collision group index.
int32 GroupIdx = UNiagaraFunctionLibrary::AcquireNiagaraGPURayTracedCollisionGroup(this);
// ... assign and use ...
UNiagaraFunctionLibrary::ReleaseNiagaraGPURayTracedCollisionGroup(this, GroupIdx);
```

### UNiagaraDataInterfaceAsyncGpuTrace
**Header**: `Classes/NiagaraDataInterfaceAsyncGpuTrace.h`
**Sim target**: GPU only (HWRT)

Asynchronous GPU-side ray traces. Results are available in the following frame.

---

## Audio DIs

### UNiagaraDataInterfaceAudio
**Header**: `Classes/NiagaraDataInterfaceAudio.h`

Abstract base for audio-driven data interfaces.

### UNiagaraDataInterfaceAudioOscilloscope
**Header**: `Classes/NiagaraDataInterfaceAudioOscilloscope.h`

Samples audio waveform (time-domain) data into the particle simulation.

### UNiagaraDataInterfaceAudioSpectrum
**Header**: `Classes/NiagaraDataInterfaceAudioSpectrum.h`

Samples FFT frequency spectrum data. Drive particle effects from audio amplitude.

### UNiagaraDataInterfaceAudioPlayer
**Header**: `Classes/NiagaraDataInterfaceAudioPlayer.h`

Triggers audio events from within a Niagara simulation (e.g., play a sound per particle spawn).

---

## Physics DIs

### UNiagaraDataInterfacePhysicsAsset
**Header**: `Public/NiagaraDataInterfacePhysicsAsset.h`

Exposes physics asset body transforms for collision or constraint effects.

### UNiagaraDataInterfaceRigidMeshCollisionQuery
**Header**: `Public/NiagaraDataInterfaceRigidMeshCollisionQuery.h`

Provides signed-distance-field (SDF)-based collision queries against rigid body meshes.

---

## Camera DI

### UNiagaraDataInterfaceCamera
**Header**: `Classes/NiagaraDataInterfaceCamera.h`
**Sim target**: CPU + GPU (partial)

Exposes camera position, rotation, field of view, and depth buffer data to the simulation.
On GPU, depth buffer sampling is available when a scene depth texture is accessible.

---

## Spline DI

### UNiagaraDataInterfaceSpline
**Header**: `Classes/NiagaraDataInterfaceSpline.h`
**Sim target**: CPU

Samples positions, tangents, and curvature along a `USplineComponent`. Particles can follow
or distribute along splines.

---

## Particle Read DI

### UNiagaraDataInterfaceParticleRead
**Header**: `Classes/NiagaraDataInterfaceParticleRead.h`
**Sim target**: CPU

Allows one emitter to read particle attributes from another emitter within the same system.
Useful for spawning secondary effects at the positions of particles in a primary emitter.

---

## Data Channel DIs (UE 5.4+)

### UNiagaraDataInterfaceDataChannelRead / Write
**Headers**: `Internal/DataInterface/NiagaraDataInterfaceDataChannelRead.h` and `...Write.h`

Data Channels allow multiple Niagara systems to share data across system boundaries at runtime,
without direct C++ coupling. Writers push data into a named channel; readers consume it.

---

## Export DI

### UNiagaraDataInterfaceExport
**Header**: `Classes/NiagaraDataInterfaceExport.h`
**Sim target**: CPU

Allows Niagara to export particle attributes back to C++ via an interface callback. Implement
`INiagaraParticleCallbackHandler` on your UObject to receive per-particle data:

```cpp
// Your class must implement INiagaraParticleCallbackHandler.
#include "NiagaraDataInterfaceExport.h"

class UMyParticleCallbackHandler : public UObject, public INiagaraParticleCallbackHandler
{
    GENERATED_BODY()
public:
    virtual void ReceiveParticleData(
        const TArray<FBasicParticleData>& Data,
        UNiagaraSystem* NiagaraSystem,
        const FVector& SimulationPositionOffset) override;
};
```

---

## Landscape DI

### UNiagaraDataInterfaceLandscape
**Header**: `Classes/NiagaraDataInterfaceLandscape.h`
**Sim target**: CPU

Samples height, normal, and material weight data from an `ALandscape` actor.

---

## Occlusion DI

### UNiagaraDataInterfaceOcclusion
**Header**: `Classes/NiagaraDataInterfaceOcclusion.h`

Queries occlusion state from the renderer's occlusion query results.

---

## Actor / Component DI

### UNiagaraDataInterfaceActorComponent
**Header**: `Internal/DataInterface/NiagaraDataInterfaceActorComponent.h`

Exposes an actor's component transforms and velocity to Niagara scripts. Useful for binding
a target actor's transform without requiring a full skeletal or static mesh DI.

---

## Material / MPC DIs

### NiagaraDataInterfaceMaterialInstanceDynamic
**Header**: `Private/NiagaraDataInterfaceMaterialInstanceDynamic.h`

Allows Niagara to read scalar and vector parameters from a `UMaterialInstanceDynamic`.

### NiagaraDataInterfaceMaterialParameterCollection
**Header**: `Private/NiagaraDataInterfaceMaterialParameterCollection.h`

Reads values from a `UMaterialParameterCollection` asset.

---

## Choosing a DI

| Use Case | Recommended DI |
|---|---|
| Spawn particles on a character mesh | `UNiagaraDataInterfaceSkeletalMesh` |
| Scatter particles on a static prop | `UNiagaraDataInterfaceStaticMesh` |
| Drive emitter rate with an animation curve | `UNiagaraDataInterfaceCurve` |
| Push a gameplay position list (e.g., AI waypoints) | `UNiagaraDataInterfaceArrayFloat3` (Vector Array) |
| Particles collide with world geometry | `UNiagaraDataInterfaceCollisionQuery` |
| Audio-reactive effects | `UNiagaraDataInterfaceAudioSpectrum` |
| Particles follow a spline path | `UNiagaraDataInterfaceSpline` |
| Camera-relative VFX (e.g., lens flares) | `UNiagaraDataInterfaceCamera` |
| Export particle positions to C++ for gameplay | `UNiagaraDataInterfaceExport` |
| Share data between two independent VFX systems | `UNiagaraDataInterfaceDataChannelRead/Write` |
| Volumetric / fluid simulation | `UNiagaraDataInterfaceGrid3DCollection` |
