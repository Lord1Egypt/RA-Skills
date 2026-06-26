# Property Specifiers Reference

Complete reference for UPROPERTY(), UFUNCTION(), UCLASS(), USTRUCT(), and UENUM() specifiers in Unreal Engine 5.

---

## UPROPERTY() Specifiers

### Editor Visibility & Editability

| Specifier | Editable | Location |
|-----------|----------|----------|
| `EditAnywhere` | Yes | Instance + archetype Details panels |
| `EditDefaultsOnly` | Yes | Archetype (CDO) Details only, not instance |
| `EditInstanceOnly` | Yes | Instance Details only, not archetype |
| `VisibleAnywhere` | No (read-only) | Instance + archetype Details |
| `VisibleDefaultsOnly` | No | Archetype Details only |
| `VisibleInstanceOnly` | No | Instance Details only |
| `NoEditInline` | Suppresses | Hides inline object editor |

**None of the above** means the property does not appear in the Details panel at all.

### Blueprint Access

| Specifier | Read | Write |
|-----------|------|-------|
| `BlueprintReadWrite` | Yes | Yes |
| `BlueprintReadOnly` | Yes | No |
| `BlueprintGetter=FuncName` | Custom getter | No (use with BlueprintReadOnly) |
| `BlueprintSetter=FuncName` | No | Custom setter |

> BlueprintReadWrite cannot be combined with EditAnywhere without a Category. Always add `Category="..."`.

### Replication

| Specifier | Effect |
|-----------|--------|
| `Replicated` | Replicates to clients; must implement `GetLifetimeReplicatedProps` |
| `ReplicatedUsing=FuncName` | Replicates + calls named function on client when value changes (RepNotify) |
| `NotReplicated` | Explicitly marks as not replicated (for structs inheriting replicated struct) |

All replicated properties require `GetLifetimeReplicatedProps` override:
```cpp
void AMyActor::GetLifetimeReplicatedProps(TArray<FLifetimeProperty>& OutLifetimeProps) const
{
    Super::GetLifetimeReplicatedProps(OutLifetimeProps);
    DOREPLIFETIME(AMyActor, Health);
    DOREPLIFETIME_CONDITION(AMyActor, bIsAiming, COND_SkipOwner);
    DOREPLIFETIME_CONDITION(AMyActor, PersonalScore, COND_OwnerOnly);
}
```

**Replication Conditions (COND_*):**

| Condition | When Replicated |
|-----------|-----------------|
| `COND_None` | Always (default) |
| `COND_InitialOnly` | Only on initial send |
| `COND_OwnerOnly` | To owning client only |
| `COND_SkipOwner` | To all except owner |
| `COND_SimulatedOnly` | To simulated proxies only |
| `COND_AutonomousOnly` | To autonomous proxy only |
| `COND_InitialOrOwner` | Initial send or to owner |
| `COND_Custom` | Controlled by `SetCustomIsActiveOverride` |

### Serialization

| Specifier | Effect |
|-----------|--------|
| `Transient` | Not serialized; reset to default on load |
| `DuplicateTransient` | Not copied when object is duplicated |
| `TextExportTransient` | Excluded from text export |
| `NonTransactional` | Not recorded in undo/redo transaction |
| `SaveGame` | Included when using `UGameplayStatics::SaveGameToSlot` |
| `SkipSerialization` | Omit from serialization entirely |

### Delegates & Events

| Specifier | Effect |
|-----------|--------|
| `BlueprintAssignable` | Blueprint can bind to this multicast delegate |
| `BlueprintCallable` | Blueprint can call `Broadcast()` on this delegate |
| `BlueprintAuthorityOnly` | Only authority can bind/call |

### Meta Specifiers

Meta goes inside `meta=(...)` after the main specifiers:

```cpp
UPROPERTY(EditAnywhere, BlueprintReadWrite, Category="Stats",
    meta=(
        ClampMin="0.0",
        ClampMax="100.0",
        UIMin="0.0",
        UIMax="100.0",
        ToolTip="Character health, clamped to [0, 100]",
        DisplayName="Health Points",
        EditCondition="bHealthEnabled",
        EditConditionHides,
        AllowPrivateAccess="true"
    ))
float Health;
```

| Meta Key | Effect |
|----------|--------|
| `ClampMin` / `ClampMax` | Hard clamps on numeric input |
| `UIMin` / `UIMax` | Slider range without hard clamp |
| `ToolTip` | Tooltip shown in Details panel |
| `DisplayName` | Override displayed property name |
| `Category` | Can also be set in meta for finer control |
| `EditCondition` | Boolean property that enables editing |
| `EditConditionHides` | Hides property (instead of graying out) when condition is false |
| `InlineEditConditionToggle` | Adds a checkbox next to another property for EditCondition |
| `AllowPrivateAccess` | Allows Blueprint access to private C++ property |
| `Units="cm"` | Shows unit label in editor |
| `MakeStructureDefaultValue` | Default value for struct members |
| `MustImplement` | For TSubclassOf<>, limits to classes implementing given interface |
| `MetaClass` | Restricts UClass* pickers to a specific base class |
| `RequiredAssetDataTags` | Filters asset picker by asset tags |
| `AssetBundles` | Controls bundle membership for soft references |
| `NoResetToDefault` | Hides "Reset to Default" arrow in Details |
| `NoClear` | Prevents setting object reference to null |
| `ShowOnlyInnerProperties` | Inline struct properties without a group header |
| `HideInDetailPanel` | Hidden in Details but still accessible in Blueprint |

---

## UFUNCTION() Specifiers

### Blueprint Interaction

| Specifier | Effect |
|-----------|--------|
| `BlueprintCallable` | Exposed as a Blueprint node with execution pin |
| `BlueprintPure` | No execution pin; no side effects implied |
| `BlueprintNativeEvent` | C++ provides `_Implementation`; Blueprint can override |
| `BlueprintImplementableEvent` | Blueprint must implement; C++ just declares |
| `BlueprintAuthorityOnly` | Only callable from authority in Blueprint |
| `BlueprintCosmetic` | Only callable on clients (cosmetic-only) |

**BlueprintNativeEvent pattern:**
```cpp
// .h
UFUNCTION(BlueprintNativeEvent, Category="Events")
FVector GetSpawnLocation();
virtual FVector GetSpawnLocation_Implementation();

// .cpp — always provide the _Implementation
FVector AMyActor::GetSpawnLocation_Implementation()
{
    return GetActorLocation() + FVector(0.f, 0.f, 200.f);
}
```

### Networking RPCs

| Specifier | Execution Site | Direction |
|-----------|---------------|-----------|
| `Server` | Runs on server | Client → Server |
| `Client` | Runs on owning client | Server → Client |
| `NetMulticast` | Runs on all (server + clients) | Server → All |
| `Reliable` | Guaranteed delivery (ordered) | — |
| `Unreliable` | Best effort, no ordering | — |
| `WithValidation` | Requires `_Validate` function | — |

```cpp
// Client RPC: runs on the owning client
UFUNCTION(Client, Reliable)
void ClientShowKillFeed(const FString& KillerName, const FString& VictimName);
void ClientShowKillFeed_Implementation(const FString& KillerName, const FString& VictimName);

// Server RPC with validation
UFUNCTION(Server, Reliable, WithValidation)
void ServerRequestInteract(AActor* Target);
void ServerRequestInteract_Implementation(AActor* Target);
bool ServerRequestInteract_Validate(AActor* Target) { return IsValid(Target); }

// NetMulticast: no validation allowed
UFUNCTION(NetMulticast, Unreliable)
void MulticastSpawnBloodDecal(FVector Location, FRotator Rotation);
void MulticastSpawnBloodDecal_Implementation(FVector Location, FRotator Rotation);
```

### Other Function Specifiers

| Specifier | Effect |
|-----------|--------|
| `Exec` | Can be called from in-game console |
| `CallInEditor` | Adds a button in the Details panel to call the function |
| `Category="..."` | Groups the node in the Blueprint palette |
| `DisplayName="..."` | Override function display name in Blueprint |
| `meta=(DeprecatedFunction)` | Marks function as deprecated |
| `meta=(CompactNodeTitle="Name")` | Compact node title in Blueprint |
| `meta=(Keywords="search terms")` | Blueprint search keywords |
| `meta=(AdvancedDisplay="Param1,Param2")` | Hides params behind Advanced disclosure |
| `meta=(DefaultToSelf="Target")` | Pins this param to Self by default |
| `meta=(HidePin="Target")` | Hides a parameter pin in Blueprint |
| `meta=(ExpandEnumAsExecs="Result")` | Creates one exec pin per enum value |
| `meta=(Latent, LatentInfo="LatentInfo")` | Marks as async latent action |

---

## UCLASS() Specifiers

| Specifier | Effect |
|-----------|--------|
| `Blueprintable` | Blueprint can subclass |
| `BlueprintType` | Usable as Blueprint variable |
| `NotBlueprintable` | Blocks subclassing even if parent allows it |
| `Abstract` | Cannot be instantiated directly |
| `Config=<Name>` | Loads Config properties from `Default<Name>.ini` |
| `DefaultConfig` | Saves config to `Default<Name>.ini` instead of user ini |
| `Transient` | Not serialized to disk |
| `Deprecated` | Marks class deprecated; instances still load |
| `CollapseCategories` | All properties put in root category |
| `DontCollapseCategories` | Overrides parent `CollapseCategories` |
| `HideCategories=(Cat1,Cat2)` | Hides listed categories in Details |
| `ShowCategories=(Cat1)` | Un-hides categories hidden by parent |
| `HideDropdown` | Not shown in class picker dropdowns |
| `Meta=(ChildCanTick)` | Blueprint subclasses can tick |
| `MinimalAPI` | Exports only type metadata, not all symbols |
| `Within=<ClassName>` | Instance outer must be of given class |
| `CustomConstructor` | Generated constructor not auto-created |
| `EditInlineNew` | Can be created inline in Details panel |
| `DefaultToInstanced` | ObjectProperty with this class is instanced by default |
| `Intrinsic` | Class built into the engine binary |

---

## USTRUCT() Specifiers

| Specifier | Effect |
|-----------|--------|
| `BlueprintType` | Usable as Blueprint variable |
| `Atomic` | Always serialized as a unit (no partial deltas) |
| `NoExport` | No automatic UScriptStruct created; manually generated |
| `HasNoOpConstructor` | Has a no-op constructor (optimization hint) |
| `IsAlwaysAccessible` | struct data accessible even without RTTI |

**UE5 note:** Always use `GENERATED_BODY()` inside structs. `GENERATED_USTRUCT_BODY()` is deprecated.

---

## UENUM() Specifiers

| Specifier | Effect |
|-----------|--------|
| `BlueprintType` | Usable in Blueprint |

**UMETA per-value specifiers:**

| Meta Key | Effect |
|----------|--------|
| `DisplayName="Label"` | Override name shown in Blueprint/editor |
| `Hidden` | Hide this value from Blueprint picker |
| `ToolTip="text"` | Tooltip in editor |

```cpp
UENUM(BlueprintType)
enum class EGamePhase : uint8
{
    PreGame    UMETA(DisplayName="Pre-Game"),
    InGame     UMETA(DisplayName="In Game"),
    PostGame   UMETA(DisplayName="Post-Game"),
    MAX        UMETA(Hidden)   // sentinel; hidden from pickers
};
```

Enums used in replication must be `uint8` and fit in 8 bits. For larger enums use `TEnumAsByte<EMyEnum>` (UE4) or keep as `uint8`-backed enum class (UE5).

---

## UINTERFACE() & IInterface

```cpp
// .h
UINTERFACE(MinimalAPI, Blueprintable)
class UDamageable : public UInterface
{
    GENERATED_BODY()
};

class MYGAME_API IDamageable
{
    GENERATED_BODY()
public:
    UFUNCTION(BlueprintCallable, BlueprintNativeEvent, Category="Combat")
    void TakeDamage(float Amount, AActor* Instigator);
};

// Implementing class
UCLASS()
class AMyCharacter : public ACharacter, public IDamageable
{
    GENERATED_BODY()
public:
    virtual void TakeDamage_Implementation(float Amount, AActor* Instigator) override;
};

// Checking/casting via interface
if (SomeActor->Implements<UDamageable>())
{
    IDamageable::Execute_TakeDamage(SomeActor, 25.f, this);
}
```
