# Material Parameter Reference

Common material parameter patterns, performance notes, and API quick-reference for C++ UE development.

---

## API Quick Reference

### UMaterialInstanceDynamic (MaterialInstanceDynamic.h)

| Method | Signature | Notes |
|--------|-----------|-------|
| `Create` | `static UMaterialInstanceDynamic* Create(UMaterialInterface* ParentMaterial, UObject* InOuter, FName Name = NAME_None)` | Preferred factory; always cache result |
| `SetScalarParameterValue` | `void SetScalarParameterValue(FName ParameterName, float Value)` | Parameter names are case-sensitive |
| `SetVectorParameterValue` | `void SetVectorParameterValue(FName ParameterName, FLinearColor Value)` | Pass FLinearColor explicitly; no implicit conversion from FVector |
| `SetTextureParameterValue` | `void SetTextureParameterValue(FName ParameterName, UTexture* Value)` | Accepts any UTexture subclass including render targets |
| `SetDoubleVectorParameterValue` | `void SetDoubleVectorParameterValue(FName ParameterName, FVector4 Value)` | For double-precision world position use |
| `InitializeScalarParameterAndGetIndex` | `bool InitializeScalarParameterAndGetIndex(const FName& Name, float Value, int32& OutIndex)` | Call once; use index in tight loops |
| `SetScalarParameterByIndex` | `bool SetScalarParameterByIndex(int32 ParameterIndex, float Value)` | Fast path; index must come from same MID |
| `InitializeVectorParameterAndGetIndex` | `bool InitializeVectorParameterAndGetIndex(const FName& Name, const FLinearColor& Value, int32& OutIndex)` | Same pattern as scalar index API |
| `SetVectorParameterByIndex` | `bool SetVectorParameterByIndex(int32 ParameterIndex, const FLinearColor& Value)` | Fast path for vectors |
| `K2_GetScalarParameterValue` | `float K2_GetScalarParameterValue(FName ParameterName)` | Returns current scalar value |
| `K2_GetVectorParameterValue` | `FLinearColor K2_GetVectorParameterValue(FName ParameterName)` | Returns current vector value |
| `K2_GetTextureParameterValue` | `UTexture* K2_GetTextureParameterValue(FName ParameterName)` | Returns current texture value |
| `ClearParameterValues` | `void ClearParameterValues()` | Removes all overrides; falls back to parent |
| `CopyParameterOverrides` | `void CopyParameterOverrides(UMaterialInstance* MaterialInstance)` | Copies all overrides from another instance |
| `CopyMaterialUniformParameters` | `void CopyMaterialUniformParameters(UMaterialInterface* Source)` | Faster than K2_Copy; skips static params |
| `K2_InterpolateMaterialInstanceParams` | `void K2_InterpolateMaterialInstanceParams(UMaterialInstance* A, UMaterialInstance* B, float Alpha)` | Output = lerp(A, B, Alpha) |
| `SetNaniteOverride` | `void SetNaniteOverride(UMaterialInterface* InMaterial)` | UE5 — assign Nanite-compatible material |

### UMaterialParameterCollectionInstance (MaterialParameterCollectionInstance.h)

| Method | Signature | Notes |
|--------|-----------|-------|
| `SetScalarParameterValue` | `bool SetScalarParameterValue(FName ParameterName, float ParameterValue)` | Returns false if name not found |
| `SetVectorParameterValue` | `bool SetVectorParameterValue(FName ParameterName, const FLinearColor& ParameterValue)` | Pass FLinearColor explicitly; no implicit conversion from FVector |
| `GetScalarParameterValue` | `bool GetScalarParameterValue(FName ParameterName, float& OutParameterValue) const` | |
| `GetVectorParameterValue` | `bool GetVectorParameterValue(FName ParameterName, FLinearColor& OutParameterValue) const` | |
| `ForceReturnToDefaultValues` | `void ForceReturnToDefaultValues()` | Resets all overrides to collection defaults |

Obtain the instance via:
```cpp
UMaterialParameterCollectionInstance* Inst = GetWorld()->GetParameterCollectionInstance(CollectionAsset);
```

### UPrimitiveComponent — Material Slot API (PrimitiveComponent.h)

| Method | Signature | Notes |
|--------|-----------|-------|
| `GetMaterial` | `UMaterialInterface* GetMaterial(int32 ElementIndex) const` | Returns current material for slot |
| `SetMaterial` | `void SetMaterial(int32 ElementIndex, UMaterialInterface* Material)` | Replaces static material; does not create MID |
| `SetMaterialByName` | `void SetMaterialByName(FName MaterialSlotName, UMaterialInterface* Material)` | Slot name lookup version |
| `GetMaterialIndex` | `int32 GetMaterialIndex(FName MaterialSlotName) const` | Resolve slot name to index |
| `GetMaterialSlotNames` | `TArray<FName> GetMaterialSlotNames() const` | All slot names on the component |
| `CreateDynamicMaterialInstance` | `UMaterialInstanceDynamic* CreateDynamicMaterialInstance(int32 ElementIndex, UMaterialInterface* SourceMaterial = nullptr, FName OptionalName = NAME_None)` | Creates MID and assigns to slot |

---

## Parameter Type Mapping

| Material Parameter Type | C++ Setter | C++ Type |
|------------------------|-----------|----------|
| Scalar Parameter | `SetScalarParameterValue` | `float` |
| Vector Parameter | `SetVectorParameterValue` | `FLinearColor` (pass FLinearColor explicitly; no implicit conversion from FVector) |
| Texture Parameter | `SetTextureParameterValue` | `UTexture*` |
| Runtime Virtual Texture | `SetRuntimeVirtualTextureParameterValue` | `URuntimeVirtualTexture*` |
| Sparse Volume Texture | `SetSparseVolumeTextureParameterValue` | `USparseVolumeTexture*` |
| Texture Collection | `SetTextureCollectionParameterValue` | `UTextureCollection*` |

Static parameters (Static Bool, Static Switch, Static Component Mask) cannot be changed at runtime on a MID. Create a `UMaterialInstanceConstant` in the editor for different static permutations and use MIDs on top for dynamic parameters.

---

## Performance Guidelines

### MID Parameter Update Cost

Parameter updates are low-cost individually. The overhead is:
1. Name hash lookup (`FName` hashing — fast)
2. Dirty flag on the uniform buffer
3. GPU uniform buffer upload on the next render (batched, not per-parameter)

For very high parameter counts (50+ parameters changed per frame per instance), use the index-based API to skip name lookup:

```cpp
// One-time initialization
int32 AlphaIdx = -1;
int32 ColorIdx = -1;
MyMID->InitializeScalarParameterAndGetIndex(TEXT("Alpha"), 1.0f, AlphaIdx);
MyMID->InitializeVectorParameterAndGetIndex(TEXT("TintColor"), FLinearColor::White, ColorIdx);

// Per-frame update — no FName hash lookup
MyMID->SetScalarParameterByIndex(AlphaIdx, NewAlpha);
MyMID->SetVectorParameterByIndex(ColorIdx, NewColor);
```

### MPC vs MID — When to Use Which

| Scenario | MPC | MID |
|----------|-----|-----|
| Global time-of-day color / intensity | Yes | No |
| Weather parameters (rain, fog) | Yes | No |
| Per-actor color / damage state | No | Yes |
| Per-instance texture swap | No | Yes |
| Drive 100+ materials at once | Yes | No (100 MID updates) |
| Layered material parameter override | No | Yes |

### Render Target Format Selection

Choose the smallest format that meets precision needs:

| Use Case | Recommended Format | Memory (512x512) |
|----------|--------------------|-----------------|
| LDR color (UI, minimap) | `RTF_RGBA8` | 1 MB |
| HDR scene color | `RTF_RGBA16f` | 2 MB |
| Depth data / single channel | `RTF_R16f` | 0.5 MB |
| Float computation | `RTF_RGBA32f` | 4 MB |

`RTF_RGBA32f` costs 4x more memory and bandwidth than `RTF_RGBA16f`. Avoid unless data requires full 32-bit precision.

### Scene Capture Performance

`USceneCaptureComponent2D` renders a full scene pass. Cost is proportional to:
- Render target resolution
- Capture source (`SCS_FinalColorLDR` is more expensive than `SCS_BaseColor`)
- Geometry in the captured view
- Post-process applied to capture

Optimization options:
```cpp
// Disable capture every frame; call manually when needed
SceneCapture->bCaptureEveryFrame = false;
SceneCapture->CaptureScene(); // trigger manually

// Exclude expensive show flags
SceneCapture->ShowFlags.SetAtmosphere(false);
SceneCapture->ShowFlags.SetFog(false);
SceneCapture->ShowFlags.SetBloom(false);
SceneCapture->ShowFlags.SetMotionBlur(false);
SceneCapture->ShowFlags.SetContactShadows(false);

// Hide specific actors from capture
SceneCapture->HiddenActors.Add(PlayerActor);

// Use a low-resolution render target for distant/offscreen views
```

---

## Common Material Parameter Names by Domain

These are conventions, not enforced by the engine. Match whatever names the material artist has used.

### PBR Base Parameters

| Parameter Name | Type | Typical Range | Purpose |
|----------------|------|--------------|---------|
| `BaseColor` | Vector | — | Albedo color |
| `Roughness` | Scalar | 0.0–1.0 | Surface roughness |
| `Metallic` | Scalar | 0.0 or 1.0 | Metallic surface flag |
| `Emissive` | Vector | — | Emissive color (HDR) |
| `EmissiveIntensity` | Scalar | 0–100+ | Emissive brightness multiplier |
| `Opacity` | Scalar | 0.0–1.0 | Translucency opacity |
| `Normal` | Texture | — | Normal map override |

### Damage / Destruction State

| Parameter Name | Type | Purpose |
|----------------|------|---------|
| `DamageAmount` | Scalar | 0 = pristine, 1 = fully damaged |
| `DamageMask` | Texture | Grayscale damage region mask |
| `BurnAmount` | Scalar | Char/burn intensity |

### Environmental / Weather

| Parameter Name | Type | Purpose |
|----------------|------|---------|
| `RainWetness` | Scalar (MPC) | Surface wetness from rain |
| `SnowAmount` | Scalar (MPC) | Snow coverage amount |
| `WindStrength` | Scalar (MPC) | Foliage wind intensity |
| `TimeOfDay` | Scalar (MPC) | 0.0–24.0 hour |

### UI / HUD Materials

| Parameter Name | Type | Purpose |
|----------------|------|---------|
| `HealthPercent` | Scalar | 0.0–1.0 health fraction |
| `FillAmount` | Scalar | Progress bar fill |
| `TintColor` | Vector | Icon or panel tint |
| `MaskTexture` | Texture | Custom shape mask |

---

## Debugging Parameter Issues

### Parameter Name Verification

Parameter names are stored as `FName` — case-sensitive exact match required. If `SetScalarParameterValue` has no visible effect:

1. Open the material in the Material Editor; confirm the exact `ParameterName` field value.
2. Check if the parameter is inside a Material Function — use `SetScalarParameterValueByInfo` with `FMaterialParameterInfo` for layer-based access.
3. Verify the MID's parent is the correct material (not already a MID of another MID pointing to the wrong base).

### MID Not Taking Effect on Mesh

If `CreateDynamicMaterialInstance` returns a valid pointer but visual changes are not visible:

- Confirm `UPROPERTY()` on the cached pointer — if missing, the MID may have been GC'd.
- Confirm the element index matches the correct material slot (`GetMaterialSlotNames()` to list them).
- On skeletal meshes, verify the LOD 0 slot is being targeted; some materials are per-LOD.

### MPC Parameter Not Updating Shaders

- Verify the collection asset reference in the component matches the collection asset the material references.
- Parameter names in the collection are `FName` — case-sensitive.
- Changes via `SetScalarParameterValue` on `UMaterialParameterCollectionInstance` queue a uniform buffer update; they are applied before the next frame render.
