# Niagara Parameter Types — C++ to Niagara Type Mapping

This reference maps Niagara editor parameter types to their C++ setter methods on `UNiagaraComponent`
and the underlying native C++ types. All parameters must be declared in the `User.` namespace in the
Niagara editor to be settable from C++ at runtime.

Sources: `NiagaraComponent.h`, `NiagaraFunctionLibrary.h`, `NiagaraDataInterfaceArrayFunctionLibrary.h`
(Engine/Plugins/FX/Niagara/Source/Niagara/).

---

## Scalar Types

| Niagara Editor Type | C++ Method (FName variant) | C++ Type | Notes |
|---|---|---|---|
| `float` | `SetVariableFloat(FName, float)` | `float` | Default precision |
| `int32` | `SetVariableInt(FName, int32)` | `int32` | |
| `bool` | `SetVariableBool(FName, bool)` | `bool` | |

---

## Vector Types

| Niagara Editor Type | C++ Method (FName variant) | C++ Type | Notes |
|---|---|---|---|
| `Vector2D` | `SetVariableVec2(FName, FVector2D)` | `FVector2D` | |
| `Vector` / `Vector3` | `SetVariableVec3(FName, FVector)` | `FVector` | |
| `Position` | `SetVariablePosition(FName, FVector)` | `FVector` | LWC-aware large-world position; use instead of `SetVariableVec3` for world-space positions |
| `Vector4` | `SetVariableVec4(FName, FVector4)` | `FVector4` | |
| `Color` (LinearColor) | `SetVariableLinearColor(FName, FLinearColor)` | `FLinearColor` | Do NOT use SetVariableVec3/4 for this |
| `Quaternion` | `SetVariableQuat(FName, FQuat)` | `FQuat` | Internally converted to `FQuat4f` |
| `Matrix` | `SetVariableMatrix(FName, FMatrix)` | `FMatrix` | FName variant available; legacy `SetNiagaraVariableMatrix(FString, FMatrix)` also works |

---

## Object / Reference Types

| Niagara Editor Type | C++ Method | Argument Type | Notes |
|---|---|---|---|
| `Object` (generic UObject) | `SetVariableObject(FName, UObject*)` | `UObject*` | Binds an object reference to a DI user param |
| `Actor` | `SetVariableActor(FName, AActor*)` | `AActor*` | Convenience wrapper around `SetVariableObject` |
| `Material` | `SetVariableMaterial(FName, UMaterialInterface*)` | `UMaterialInterface*` | |
| `Texture` | `SetVariableTexture(FName, UTexture*)` | `UTexture*` | |
| `TextureRenderTarget` | `SetVariableTextureRenderTarget(FName, UTextureRenderTarget*)` | `UTextureRenderTarget*` | |

---

## Data Interface Types

Data interfaces are bound by overriding the User parameter that holds the DI. The parameter appears
as a DI type in the Niagara editor (e.g., "Skeletal Mesh", "Float Array"). The binding is done via
`SetVariableObject`, or through the specialized helpers in `UNiagaraFunctionLibrary`.

| Niagara DI Type | Binding Method | Notes |
|---|---|---|
| Skeletal Mesh DI | `UNiagaraFunctionLibrary::OverrideSystemUserVariableSkeletalMeshComponent` | Pass `USkeletalMeshComponent*` |
| Static Mesh DI | `UNiagaraFunctionLibrary::OverrideSystemUserVariableStaticMeshComponent` | Pass `UStaticMeshComponent*` |
| Static Mesh DI (asset) | `UNiagaraFunctionLibrary::OverrideSystemUserVariableStaticMesh` | Pass `UStaticMesh*` directly |
| Texture DI | `UNiagaraFunctionLibrary::SetTextureObject` | Pass `UTexture*` |
| 2D Array Texture DI | `UNiagaraFunctionLibrary::SetTexture2DArrayObject` | Pass `UTexture2DArray*` |
| Volume Texture DI | `UNiagaraFunctionLibrary::SetVolumeTextureObject` | Pass `UVolumeTexture*` |
| Float Array DI | `UNiagaraDataInterfaceArrayFunctionLibrary::SetNiagaraArrayFloat` | Replaces entire array |
| Generic DI (typed) | `UNiagaraFunctionLibrary::GetDataInterface<TDIType>` | Returns the DI object for direct mutation |
| Generic DI (untyped) | `UNiagaraFunctionLibrary::GetDataInterface(UClass*, UNiagaraComponent*, FName)` | Non-template variant |

---

## Array DI Types (UNiagaraDataInterfaceArrayFunctionLibrary)

All array setters replace the entire data array in the named User parameter DI.
Single-element setters exist for in-place updates without replacing the full array.

| Array Element Type | Set Whole Array | Set Single Element | Get Whole Array | Get Single Element |
|---|---|---|---|---|
| `float` | `SetNiagaraArrayFloat` | `SetNiagaraArrayFloatValue` | `GetNiagaraArrayFloat` | `GetNiagaraArrayFloatValue` |
| `FVector2D` | `SetNiagaraArrayVector2D` | `SetNiagaraArrayVector2DValue` | `GetNiagaraArrayVector2D` | `GetNiagaraArrayVector2DValue` |
| `FVector` | `SetNiagaraArrayVector` | `SetNiagaraArrayVectorValue` | `GetNiagaraArrayVector` | `GetNiagaraArrayVectorValue` |
| `FVector` (Position) | `SetNiagaraArrayPosition` | `SetNiagaraArrayPositionValue` | `GetNiagaraArrayPosition` | `GetNiagaraArrayPositionValue` |
| `FVector4` | `SetNiagaraArrayVector4` | `SetNiagaraArrayVector4Value` | `GetNiagaraArrayVector4` | `GetNiagaraArrayVector4Value` |
| `FLinearColor` | `SetNiagaraArrayColor` | `SetNiagaraArrayColorValue` | `GetNiagaraArrayColor` | `GetNiagaraArrayColorValue` |
| `FQuat` | `SetNiagaraArrayQuat` | `SetNiagaraArrayQuatValue` | `GetNiagaraArrayQuat` | `GetNiagaraArrayQuatValue` |
| `FMatrix` | `SetNiagaraArrayMatrix` | `SetNiagaraArrayMatrixValue` | `GetNiagaraArrayMatrix` | `GetNiagaraArrayMatrixValue` |
| `int32` | `SetNiagaraArrayInt32` | `SetNiagaraArrayInt32Value` | `GetNiagaraArrayInt32` | `GetNiagaraArrayInt32Value` |
| `uint8` | `SetNiagaraArrayUInt8` | `SetNiagaraArrayUInt8Value` | `GetNiagaraArrayUInt8` | `GetNiagaraArrayUInt8Value` |
| `bool` | `SetNiagaraArrayBool` | `SetNiagaraArrayBoolValue` | `GetNiagaraArrayBool` | `GetNiagaraArrayBoolValue` |

`bSizeToFit=true` on single-element setters will grow the array to accommodate the index if needed.

**Low-precision internal storage**: Array DIs use internal `FVector3f` / `FVector2f` / `FQuat4f`
storage (single-precision). The public API accepts double-precision UE types and converts internally.
For non-BP code using `TConstArrayView<FVector3f>`, use the non-templated C++-only overloads:

```cpp
// Non-BP overloads accepting single-precision directly (avoids conversion overhead):
// SetNiagaraArrayFloat(Component, Name, TConstArrayView<double>)
// SetNiagaraArrayVector(Component, Name, TConstArrayView<FVector3f>)
// SetNiagaraArrayVector4(Component, Name, TConstArrayView<FVector4f>)
// SetNiagaraArrayQuat(Component, Name, TConstArrayView<FQuat4f>)
// SetNiagaraArrayMatrix(Component, Name, TConstArrayView<FMatrix44f>)
// SetNiagaraArrayUInt8(Component, Name, TConstArrayView<uint8>)
// SetNiagaraArrayInt32(Component, Name, TConstArrayView<int64>)
```

---

## Legacy FString Setters (Blueprint-Oriented, Slower)

These exist on `UNiagaraComponent` for Blueprint compatibility. Prefer the `FName` variants above
in C++ as they avoid a string-to-FName conversion on every call.

```cpp
// All FString setters — equivalent in behavior, slower in C++.
SetNiagaraVariableFloat(const FString&, float)
SetNiagaraVariableInt(const FString&, int32)
SetNiagaraVariableBool(const FString&, bool)
SetNiagaraVariableVec2(const FString&, FVector2D)
SetNiagaraVariableVec3(const FString&, FVector)
SetNiagaraVariableVec4(const FString&, FVector4)
SetNiagaraVariableLinearColor(const FString&, FLinearColor)
SetNiagaraVariableQuat(const FString&, FQuat)
SetNiagaraVariableMatrix(const FString&, FMatrix)    // legacy FString variant; prefer SetVariableMatrix(FName, FMatrix)
SetNiagaraVariableObject(const FString&, UObject*)
SetNiagaraVariableActor(const FString&, AActor*)
SetNiagaraVariablePosition(const FString&, FVector)
```

---

## ENCPoolMethod Values

Used in `SpawnSystemAtLocation` and `SpawnSystemAttached` `PoolingMethod` parameter.

| Value | Behavior |
|---|---|
| `ENCPoolMethod::None` | No pooling. Component is destroyed when system finishes if `bAutoDestroy=true`. |
| `ENCPoolMethod::AutoRelease` | Component returns to the world pool automatically when the system finishes. Never call `DestroyComponent`. |
| `ENCPoolMethod::ManualRelease` | You must call `ReleaseToPool()` to return the component to the pool. Used for effects that you pause/resume explicitly. |
| `ENCPoolMethod::FreeInPool` | Internal pool state (not for external use). |

---

## Parameter Namespace Rules

Niagara parameters follow a `Namespace.VariableName` convention:

- `User.MyParam` — authored as "User Exposed" in Niagara editor; the only namespace settable from C++.
- `System.Age`, `System.DeltaTime`, `System.ExecutionState` — built-in system parameters; read-only.
- `Emitter.MyEmitterVar` — scoped to a single emitter; not accessible from C++.
- `Particle.Position`, `Particle.Velocity` — per-particle; not accessible from C++.
- `Module.MyModuleVar` — private to a module stack node; not accessible from C++.

Always confirm the exact parameter name in the Niagara editor's "Parameters" panel before writing
C++ code — the name is case-sensitive and the namespace prefix must be included.
