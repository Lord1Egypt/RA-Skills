# Asset Loading Patterns

Reference guide for async loading, `FStreamableManager`, load grouping, and handle lifecycle in Unreal Engine 5.

---

## FStreamableManager Access

`FStreamableManager` is a member of `UAssetManager`. Do not create your own instances in game code — share the one owned by the Asset Manager.

```cpp
// Preferred access (UE5):
FStreamableManager& SM = UAssetManager::GetStreamableManager();
// Equivalent to: UAssetManager::Get().StreamableManager
```

Module dependency required in `Build.cs`:
```csharp
PublicDependencyModuleNames.AddRange(new string[] { "Engine", "AssetManager" });
```

---

## Pattern 1: Single Asset, Callback on Completion

```cpp
// Header
TSharedPtr<FStreamableHandle> LoadHandle;

UPROPERTY(EditDefaultsOnly)
TSoftObjectPtr<UStaticMesh> WeaponMeshSoft;

// Load
void AMyCharacter::BeginLoadWeaponMesh()
{
    FStreamableManager& SM = UAssetManager::GetStreamableManager();

    LoadHandle = SM.RequestAsyncLoad(
        WeaponMeshSoft.ToSoftObjectPath(),
        FStreamableDelegate::CreateUObject(this, &AMyCharacter::OnWeaponMeshReady));
}

void AMyCharacter::OnWeaponMeshReady()
{
    // At callback time, IsValid() returns true if successfully loaded.
    if (WeaponMeshSoft.IsValid())
    {
        WeaponMeshComp->SetStaticMesh(WeaponMeshSoft.Get());
    }
    // Handle can now be released; assets stay in memory while referenced by component.
    LoadHandle.Reset();
}
```

---

## Pattern 2: Multiple Assets, Single Callback

Load a batch and receive one callback when all are ready.

```cpp
void UMyLoadSystem::LoadUIAssets(const TArray<TSoftObjectPtr<UTexture2D>>& IconRefs)
{
    TArray<FSoftObjectPath> Paths;
    Paths.Reserve(IconRefs.Num());
    for (const TSoftObjectPtr<UTexture2D>& Ref : IconRefs)
    {
        if (!Ref.IsNull())
        {
            Paths.Add(Ref.ToSoftObjectPath());
        }
    }

    if (Paths.IsEmpty()) { return; }

    FStreamableManager& SM = UAssetManager::GetStreamableManager();
    UILoadHandle = SM.RequestAsyncLoad(
        Paths,
        FStreamableDelegate::CreateUObject(this, &UMyLoadSystem::OnUIAssetsLoaded));
}

void UMyLoadSystem::OnUIAssetsLoaded()
{
    // Retrieve loaded assets from handle.
    TArray<UTexture2D*> LoadedIcons;
    UILoadHandle->GetLoadedAssets(LoadedIcons);

    for (UTexture2D* Icon : LoadedIcons)
    {
        if (Icon) { /* bind to widget */ }
    }
}
```

---

## Pattern 3: High Priority / Synchronous Fallback

For assets needed immediately (e.g., during level transition):

```cpp
// Option A: RequestSyncLoad — blocks until done.
// Use only for small assets or during loading screens.
TSharedPtr<FStreamableHandle> Handle = SM.RequestSyncLoad(
    AssetPath,
    false,                                              // bManageActiveHandle
    TEXT("LevelTransition sync load"));

UObject* Asset = Handle->GetLoadedAsset();

// Option B: WaitUntilComplete on an already-started async load.
if (LoadHandle.IsValid() && LoadHandle->IsLoadingInProgress())
{
    LoadHandle->WaitUntilComplete(5.f); // Timeout seconds; 0 = wait forever.
}
```

---

## Pattern 4: Lambda Callback with Captured State

```cpp
FPrimaryAssetId AssetId(TEXT("WeaponDefinition"), TEXT("DA_Rifle"));

TSharedPtr<FStreamableHandle> Handle = UAssetManager::Get().LoadPrimaryAsset(
    AssetId,
    TArray<FName>{ TEXT("Game") },
    FStreamableDelegate::CreateLambda([this, AssetId]()
    {
        UWeaponDefinition* Def =
            UAssetManager::Get().GetPrimaryAssetObject<UWeaponDefinition>(AssetId);
        if (Def && IsValid(this))
        {
            EquipWeapon(Def);
        }
    }));
```

Important: Lambdas capturing `this` are not safe if the object is destroyed before the callback fires. Use `CreateUObject` (which checks object validity) or guard with `IsValid(this)`.

---

## Pattern 5: Progress Tracking

```cpp
void UMyLoadingScreen::StartLoadWithProgress(const TArray<FSoftObjectPath>& Assets)
{
    FStreamableManager& SM = UAssetManager::GetStreamableManager();

    LoadHandle = SM.RequestAsyncLoad(
        Assets,
        FStreamableDelegate::CreateUObject(this, &UMyLoadingScreen::OnLoadComplete));
}

// Poll from Tick or a timer.
void UMyLoadingScreen::Tick(float DeltaTime)
{
    if (LoadHandle.IsValid() && LoadHandle->IsLoadingInProgress())
    {
        float Progress = LoadHandle->GetLoadProgress(); // 0.0 to 1.0
        ProgressBar->SetPercent(Progress);
    }
}

void UMyLoadingScreen::OnLoadComplete()
{
    ProgressBar->SetPercent(1.f);
    LoadHandle.Reset();
    HideLoadingScreen();
}
```

---

## Pattern 6: Load Grouping with Asset Manager Bundles

Bundle state transitions are the recommended way to manage groups of related assets across gameplay states.

```cpp
UAssetManager& AM = UAssetManager::Get();

// Get all weapon IDs.
TArray<FPrimaryAssetId> WeaponIds;
AM.GetPrimaryAssetIdList(FPrimaryAssetType(TEXT("WeaponDefinition")), WeaponIds);

// On entering the main menu: load UI bundle only.
AM.LoadPrimaryAssets(WeaponIds, { TEXT("UI") });

// On entering gameplay: add Game bundle, keep UI or remove it.
AM.ChangeBundleStateForPrimaryAssets(
    WeaponIds,
    { TEXT("Game") },   // AddBundles
    { TEXT("UI") },     // RemoveBundles
    false,              // bRemoveAllBundles
    FStreamableDelegate::CreateLambda([]() { /* gameplay ready */ }));

// On leaving gameplay: unload Game bundle, keep UI.
AM.ChangeBundleStateForMatchingPrimaryAssets(
    { TEXT("UI") },     // NewBundles
    { TEXT("Game") });  // OldBundles (removes these)
```

---

## Handle Lifecycle Rules

| State | Meaning |
|---|---|
| `IsLoadingInProgress()` | Async load still running |
| `HasLoadCompleted()` | All assets loaded (callback may not have fired yet if deferred) |
| `WasCanceled()` | `CancelHandle()` was called; completion callback not invoked |
| `HasError()` | One or more assets failed to load |

**Ownership rules:**
- `TSharedPtr<FStreamableHandle>` keeps assets pinned while alive.
- Letting the `TSharedPtr` go out of scope calls `ReleaseHandle()` implicitly.
- `ReleaseHandle()` is deferred if called before the completion callback fires; callback still runs.
- `CancelHandle()` cancels immediately — completion callback is NOT called; cancel callback is called if bound.

```cpp
// Cancellation with a cancel callback.
Handle->BindCancelDelegate(FStreamableDelegate::CreateLambda([]()
{
    UE_LOG(LogTemp, Warning, TEXT("Load was canceled."));
}));
Handle->CancelHandle();
```

---

## Combined / Merged Handles

When multiple independent loads should be tracked as one unit:

```cpp
TSharedPtr<FStreamableHandle> HandleA = SM.RequestAsyncLoad(PathA, {});
TSharedPtr<FStreamableHandle> HandleB = SM.RequestAsyncLoad(PathB, {});

// Combine into a single tracking handle. CreateCombinedHandle is on FStreamableManager.
TSharedPtr<FStreamableHandle> Merged = SM.CreateCombinedHandle({ HandleA, HandleB });

Merged->BindCompleteDelegate(FStreamableDelegate::CreateLambda([]()
{
    // Both A and B are loaded.
}));
```

---

## Priority Constants

From `Engine/StreamableManager.h` (namespace `UE::StreamableManager::Private`):

```cpp
constexpr TAsyncLoadPriority DefaultAsyncLoadPriority = 0;
constexpr TAsyncLoadPriority AsyncLoadHighPriority     = 100;
```

Pass priority to `RequestAsyncLoad`:
```cpp
SM.RequestAsyncLoad(
    Paths, Delegate,
    UE::StreamableManager::Private::AsyncLoadHighPriority);
```

---

## Anti-Patterns

### Releasing Handle Before Using Loaded Assets

```cpp
// BAD: assets may be GC'd immediately after Reset().
SM.RequestAsyncLoad(Path, [this]() {
    LoadHandle.Reset(); // released inside callback
    UStaticMesh* Mesh = MeshSoft.Get(); // nullptr — already GC'd
});

// GOOD: only reset after assigning to a hard reference.
SM.RequestAsyncLoad(Path, [this]() {
    MeshComp->SetStaticMesh(MeshSoft.Get()); // component holds the ref
    LoadHandle.Reset();                      // safe to release now
});
```

### Calling LoadSynchronous in Tick

```cpp
// BAD: stalls every frame if asset not cached.
void AMyActor::Tick(float DeltaTime)
{
    UStaticMesh* Mesh = MeshSoft.LoadSynchronous(); // blocks rendering
}

// GOOD: start async load once, use result only after callback.
```

### Ignoring Load Errors

```cpp
// Always check after callback:
if (Handle->HasError())
{
    UE_LOG(LogTemp, Error, TEXT("One or more assets failed to load."));
}
```
