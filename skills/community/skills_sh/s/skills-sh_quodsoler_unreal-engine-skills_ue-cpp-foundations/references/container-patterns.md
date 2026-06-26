# Container Patterns Reference

Detailed patterns, performance notes, and advanced usage for TArray, TMap, TSet, TOptional, TVariant, and related UE containers.

---

## TArray

`TArray<T, AllocatorType>` is defined in `Engine/Source/Runtime/Core/Public/Containers/Array.h`. It stores elements in a contiguous block of memory and is the default container for ordered sequences.

### Core Operations

```cpp
TArray<int32> Numbers;

// Construction
TArray<int32> FromInit = { 1, 2, 3, 4, 5 };
TArray<int32> Copy     = FromInit;
TArray<int32> Moved    = MoveTemp(FromInit);  // Move — FromInit is empty after

// Capacity management
Numbers.Reserve(64);          // Pre-allocate without changing Num()
Numbers.SetNum(10);           // Resize, default-initializes new elements
Numbers.SetNumZeroed(10);     // Resize, zero-initializes new elements
Numbers.SetNumUninitialized(10); // Resize without initialization (POD only)
Numbers.Shrink();             // Release excess capacity
Numbers.Empty();              // Clear all elements, free allocation
Numbers.Reset();              // Clear all elements, keep capacity (no reallocation)
Numbers.Empty(64);            // Clear + hint future capacity

// Element count
int32 Count  = Numbers.Num();
bool  bEmpty = Numbers.IsEmpty();
int32 MaxCap = Numbers.Max();       // Current allocation capacity
```

### Adding Elements

```cpp
TArray<FString> Names;

// Add — copies or moves
Names.Add(TEXT("Alpha"));
Names.Add(FString(TEXT("Beta")));    // Move from rvalue

// Emplace — constructs in-place (avoids copy/move overhead for complex types)
Names.Emplace(TEXT("Gamma"));

// AddUnique — O(n) search before add; use TSet if uniqueness is the main goal
Names.AddUnique(TEXT("Alpha"));  // No-op: already present

// Insert at index (shifts all subsequent elements)
Names.Insert(TEXT("First"), 0);

// Append
TArray<FString> Extra = { TEXT("X"), TEXT("Y") };
Names.Append(Extra);
Names.Append({ TEXT("P"), TEXT("Q") });  // Initializer list

// Push/Pop (stack semantics)
Names.Push(TEXT("Top"));
FString Top = Names.Pop();       // Removes and returns last element
```

### Removal

```cpp
TArray<int32> V = { 1, 2, 3, 2, 4, 2 };

// Remove — removes all occurrences; order-preserving; O(n)
int32 Removed = V.Remove(2);    // Removed == 3

// RemoveSwap — removes all; swaps with last; O(1) per removal but destroys order
V.RemoveSwap(3);

// RemoveAt — by index; order-preserving; O(n)
V.RemoveAt(0);

// RemoveAtSwap — by index; swaps with last; O(1); destroys order
V.RemoveAtSwap(0);

// RemoveSingle — removes only the first occurrence
V.RemoveSingle(4);

// RemoveAll — removes all matching a predicate
V.RemoveAll([](int32 N) { return N % 2 == 0; });

// RemoveAllSwap — same but unordered (faster)
V.RemoveAllSwap([](int32 N) { return N < 0; });

// Pop — removes the last element
if (V.Num() > 0)
{
    int32 Last = V.Pop();
}
```

### Search & Query

```cpp
TArray<FString> Names = { TEXT("Alpha"), TEXT("Beta"), TEXT("Gamma") };

// Find — returns INDEX_NONE if not found
int32 Idx = Names.Find(TEXT("Beta"));       // 1
int32 Rev = Names.FindLast(TEXT("Beta"));    // 1 (from end)

// Contains — bool
bool bHas = Names.Contains(TEXT("Delta"));  // false

// FindByPredicate — returns pointer to first match or nullptr
FString* Match = Names.FindByPredicate([](const FString& S)
{
    return S.StartsWith(TEXT("G"));
});
// Use as: if (Match) { ... }

// IndexOfByPredicate — returns index or INDEX_NONE
int32 GIdx = Names.IndexOfByPredicate([](const FString& S)
{
    return S.Contains(TEXT("amm"));
});

// ContainsByPredicate
bool bAnyLong = Names.ContainsByPredicate([](const FString& S)
{
    return S.Len() > 4;
});

// FilterByPredicate — returns a new TArray
TArray<FString> Long = Names.FilterByPredicate([](const FString& S)
{
    return S.Len() > 4;
});

// IsValidIndex
bool bValid = Names.IsValidIndex(5);  // false
```

### Sorting

```cpp
TArray<int32> Numbers = { 5, 3, 1, 4, 2 };

// Sort with operator< (modifies in-place)
Numbers.Sort();

// Sort with predicate
Numbers.Sort([](int32 A, int32 B) { return A > B; });  // Descending

// StableSort — preserves relative order of equal elements
Numbers.StableSort([](int32 A, int32 B) { return A < B; });

// Sort array of pointers/objects by a member
TArray<FWeaponStats*> Weapons;
Weapons.Sort([](const FWeaponStats* A, const FWeaponStats* B)
{
    return A->BaseDamage > B->BaseDamage;
});

// HeapSort (O(n log n), not stable, slightly faster than Sort)
Numbers.HeapSort();
```

### Iteration Patterns

```cpp
TArray<AActor*> Actors;

// Ranged-for (do NOT add/remove during iteration)
for (AActor* Actor : Actors)
{
    if (IsValid(Actor)) { Actor->Destroy(); }
}

// Indexed (safe for removal when iterating backwards)
for (int32 i = Actors.Num() - 1; i >= 0; --i)
{
    if (!IsValid(Actors[i]))
    {
        Actors.RemoveAtSwap(i);
    }
}

// Iterator with inline removal
for (auto It = Actors.CreateIterator(); It; ++It)
{
    if (!IsValid(*It))
    {
        It.RemoveCurrent();
    }
}

// Const iterator
for (auto It = Actors.CreateConstIterator(); It; ++It)
{
    UE_LOG(LogTemp, Log, TEXT("%s"), *(*It)->GetName());
}
```

### Memory & Performance Notes

- `Add` / `Emplace` are O(1) amortized; worst-case O(n) when reallocation occurs.
- `Remove` / `RemoveAt` are O(n) — they shift elements. Use `RemoveSwap` / `RemoveAtSwap` for O(1) when order does not matter.
- `Reserve` before filling large arrays eliminates reallocation churn.
- Use `Emplace` over `Add` for non-trivial types to avoid an extra copy.
- `SetNumUninitialized` is the fastest way to resize for POD bulk-fill patterns.
- Avoid `Contains` / `Find` in hot paths on large arrays — O(n). Use `TSet` or `TMap` instead.

### Fixed-Size Inline Allocation

```cpp
// TArray with inline storage for up to N elements (avoids heap for small arrays)
TArray<int32, TInlineAllocator<8>> SmallList;
SmallList.Add(1);  // Stored inline; no heap alloc if <= 8 elements

// Fixed max size (compile-time assertion on overflow)
TArray<int32, TFixedAllocator<16>> FixedList;
```

---

## TMap

`TMap<K, V>` is a hash map backed by a sparse array. Average O(1) lookup, insertion, and removal. Defined in `Engine/Source/Runtime/Core/Public/Containers/Map.h`.

### Core Operations

```cpp
TMap<FName, float> WeaponDamage;

// Add — overwrites if key exists
WeaponDamage.Add(FName("Rifle"), 35.f);
WeaponDamage.Add(FName("Shotgun"), 80.f);

// Emplace — constructs value in-place
WeaponDamage.Emplace(FName("Pistol"), 20.f);

// FindOrAdd — returns ref to existing or newly-default-inserted value
float& RifleRef = WeaponDamage.FindOrAdd(FName("Rifle"));  // Returns 35.f ref
float& SniperRef = WeaponDamage.FindOrAdd(FName("Sniper")); // Inserts 0.f, returns ref
SniperRef = 120.f;

// Find — returns pointer; nullptr if absent
float* DamagePtr = WeaponDamage.Find(FName("Rifle"));
if (DamagePtr)
{
    *DamagePtr *= 1.5f;  // Modify in-place
}

// FindRef — returns value copy (or default if absent) — no way to distinguish "absent" from "zero"
float GrenadeDmg = WeaponDamage.FindRef(FName("Grenade"));  // 0.f (not found)

// Contains
bool bHasRifle = WeaponDamage.Contains(FName("Rifle"));  // true

// Remove
int32 NumRemoved = WeaponDamage.Remove(FName("Pistol"));  // 1

// Num / IsEmpty
int32 Count = WeaponDamage.Num();
bool  bEmpty = WeaponDamage.IsEmpty();
```

### Iteration

```cpp
TMap<FName, int32> ItemCounts;

// Iterate all pairs
for (const TPair<FName, int32>& Pair : ItemCounts)
{
    UE_LOG(LogTemp, Log, TEXT("%s = %d"), *Pair.Key.ToString(), Pair.Value);
}

// Structured bindings (C++17)
for (auto& [Key, Value] : ItemCounts)
{
    Value += 10;
}

// Keys only
TArray<FName> Keys;
ItemCounts.GetKeys(Keys);

// Values only
TArray<int32> Values;
ItemCounts.GenerateValueArray(Values);

// Key-value arrays
TArray<FName> OutKeys;
TArray<int32> OutValues;
ItemCounts.GenerateKeyArray(OutKeys);
ItemCounts.GenerateValueArray(OutValues);

// Iterator with removal
for (auto It = ItemCounts.CreateIterator(); It; ++It)
{
    if (It.Value() <= 0)
    {
        It.RemoveCurrent();
    }
}
```

### Memory & Performance Notes

- TMap uses a hash table with open addressing on a sparse array. Iteration visits only live pairs (no gaps for the user).
- Keys must implement `GetTypeHash()` and `operator==`. FName, FString, int32, FGuid, etc. are supported out of the box.
- `Reserve` before bulk-adding: `WeaponDamage.Reserve(64)`.
- `TMap::Empty(Slack)` clears and reserves `Slack` slots.
- For read-heavy maps that rarely change, prefer building once then querying.
- `TMultiMap<K, V>` allows duplicate keys — access with `MultiFind()`.

### Custom Key Hashing

```cpp
// For custom struct keys, provide GetTypeHash and operator==
struct FItemKey
{
    FName Category;
    int32 Tier;

    bool operator==(const FItemKey& Other) const
    {
        return Category == Other.Category && Tier == Other.Tier;
    }
};

inline uint32 GetTypeHash(const FItemKey& Key)
{
    return HashCombine(GetTypeHash(Key.Category), GetTypeHash(Key.Tier));
}

TMap<FItemKey, float> ItemValues;
```

---

## TSet

`TSet<T>` is a hash set — unique elements, O(1) average operations. Backed by the same sparse array as TMap (without values).

### Core Operations

```cpp
TSet<FName> Tags;

// Add
Tags.Add(FName("Flying"));
Tags.Add(FName("Aquatic"));
Tags.Add(FName("Flying"));  // No-op — already present

// Contains
bool bFlying = Tags.Contains(FName("Flying"));  // true

// Remove
Tags.Remove(FName("Aquatic"));

// Num / IsEmpty
int32 Count = Tags.Num();

// Reserve
Tags.Reserve(32);
```

### Set Operations

```cpp
TSet<FName> A = { FName("Fire"), FName("Ice"), FName("Wind") };
TSet<FName> B = { FName("Ice"), FName("Wind"), FName("Earth") };

TSet<FName> Intersection = A.Intersect(B);  // { Ice, Wind }
TSet<FName> Union        = A.Union(B);      // { Fire, Ice, Wind, Earth }
TSet<FName> Difference   = A.Difference(B); // { Fire }

bool bSubset = B.Includes(A);  // false (A has Fire which B doesn't)
```

### Iteration

```cpp
TSet<FName> Tags;

for (const FName& Tag : Tags)
{
    UE_LOG(LogTemp, Log, TEXT("Tag: %s"), *Tag.ToString());
}

// Iterator with removal
for (auto It = Tags.CreateIterator(); It; ++It)
{
    if (It->IsNone())
    {
        It.RemoveCurrent();
    }
}
```

---

## TOptional

`TOptional<T>` represents a value that may or may not be present. Avoids sentinel values like `-1` or `nullptr`.

```cpp
TOptional<int32> MaybeLevel;

// Check and access
if (MaybeLevel.IsSet())
{
    int32 Level = MaybeLevel.GetValue();  // Asserts if not set
}

// Safe access with default
int32 Level = MaybeLevel.Get(1);  // Returns 1 if not set

// Set
MaybeLevel = 5;

// Reset (clear)
MaybeLevel.Reset();

// IsSet shorthand in conditions
if (MaybeLevel.IsSet() && MaybeLevel.GetValue() > 10)
{
    // ...
}

// Return from function
TOptional<FVector> FindSpawnPoint(const FString& ZoneName)
{
    if (ZoneName.IsEmpty()) return {};  // NullOpt
    return FVector(100.f, 200.f, 0.f);
}

if (TOptional<FVector> Pt = FindSpawnPoint(TEXT("Start")))
{
    SpawnAt(Pt.GetValue());
}
```

---

## TVariant

`TVariant<T1, T2, ...>` is a type-safe discriminated union (like `std::variant`).

```cpp
#include "Misc/TVariant.h"

TVariant<int32, float, FString> Val;

// Set
Val.Set<int32>(42);
Val.Set<FString>(TEXT("Hello"));

// Check active type
if (Val.IsType<FString>())
{
    FString& S = Val.Get<FString>();
}

// Visit pattern — UE5 provides Visit() via TVariantHelper
Visit([](auto& V) { /* handle each type */ }, Val);
```

---

## Sparse Arrays & Indirect Arrays

### TSparseArray

Used internally by TSet and TMap. Elements can have "holes" (removed indices remain allocated but invalid). Access by `FSetElementId`.

```cpp
// Rarely used directly — prefer TSet/TMap
TSparseArray<FMyStruct> SparseData;
FSparseArrayAllocationInfo AllocInfo = SparseData.AddUninitialized();
new (AllocInfo.Pointer) FMyStruct();
```

### TIndirectArray

Holds heap-allocated objects; owns and deletes them on removal.

```cpp
TIndirectArray<FMyNonCopyable> Objects;
Objects.Add(new FMyNonCopyable());
// Objects deletes all entries on destruction
```

---

## UPROPERTY-Compatible Container Rules

When containers are UPROPERTY members:

- `TArray<UPROPERTY-type>` — fully supported, GC-tracked element pointers
- `TMap<UPROPERTY-type, UPROPERTY-type>` — supported
- `TSet<UPROPERTY-type>` — supported
- **Keys in TMap UPROPERTY must be value types** (no UObject* keys)
- `TArray<TArray<T>>` — **not supported** as UPROPERTY (use a wrapper struct)
- Containers of raw pointers **without UPROPERTY** are invisible to GC

```cpp
// Correct: TArray of TObjectPtr for UE5 GC-tracked arrays
UPROPERTY()
TArray<TObjectPtr<UMyObject>> ManagedObjects;

// Correct: TMap with value-type key and UObject ptr value
UPROPERTY()
TMap<FName, TObjectPtr<UDataAsset>> AssetRegistry;

// WRONG: nested TArray as UPROPERTY
UPROPERTY()
TArray<TArray<int32>> Matrix;  // Compile error

// WORKAROUND: wrap inner array
USTRUCT(BlueprintType)
struct FIntRow { GENERATED_BODY() UPROPERTY() TArray<int32> Values; };

UPROPERTY()
TArray<FIntRow> Matrix;
```

---

## Performance Comparison

| Operation | TArray | TMap | TSet |
|-----------|--------|------|------|
| Add | O(1) amortized | O(1) amortized | O(1) amortized |
| Find/Contains | O(n) | O(1) avg | O(1) avg |
| Remove by value | O(n) | O(1) avg | O(1) avg |
| Remove by index | O(n) (shift) | — | — |
| Iteration | O(n), cache-friendly | O(n), sparse | O(n), sparse |
| Sorted iteration | Sort first: O(n log n) | No | No |
| Memory | Compact contiguous | Sparse + hash table | Sparse + hash table |

**Guidelines:**
- Use `TArray` when: ordered, index-based access, frequent iteration, small N.
- Use `TMap` when: key-based lookup, O(1) find matters, order irrelevant.
- Use `TSet` when: uniqueness enforced, fast membership test, no associated value needed.
- Consider `TArray` + `Sort` + binary search for read-heavy sorted lookups.
