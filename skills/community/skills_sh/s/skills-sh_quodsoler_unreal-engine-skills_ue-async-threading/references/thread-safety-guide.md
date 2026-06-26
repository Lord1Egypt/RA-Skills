# Thread Safety Guide

Patterns and rules for safe cross-thread data access in Unreal Engine.

---

## UObject Access Rules

UObjects are managed by the garbage collector, which runs on the game thread. Any access from another thread risks reading a dangling pointer or corrupting GC bookkeeping.

**What counts as "access":** Reading any UPROPERTY, calling any UFUNCTION, calling `GetWorld()`, `GetOwner()`, `GetComponentByClass()`, iterating component arrays, spawning or destroying actors, modifying transform -- all of these are game-thread-only operations.

**Why it seems to work sometimes:** GC only runs at specific points in the frame. A background thread that finishes quickly may never collide with GC. But under load, longer GC pauses, or different hardware timing, the race condition triggers -- producing crashes that are nearly impossible to reproduce in development.

---

## TWeakObjectPtr for Cross-Thread UObject References

Never capture raw `UObject*` in lambdas dispatched to other threads or deferred to future game-thread ticks. The object may be garbage collected before execution.

```cpp
// Capture weak pointer BEFORE dispatching
TWeakObjectPtr<AMyActor> WeakActor(MyActor);

UE::Tasks::Launch(UE_SOURCE_LOCATION, [WeakActor]()
{
    float Result = ExpensiveCompute();

    // Dispatch result back to game thread with safety check
    AsyncTask(ENamedThreads::GameThread, [WeakActor, Result]()
    {
        if (AMyActor* Actor = WeakActor.Get())
        {
            Actor->ApplyComputedResult(Result);
        }
        // If Get() returns nullptr, actor was GC'd — silently skip
    });
});
```

**Rule:** Create the `TWeakObjectPtr` on the game thread, then copy it into lambdas. `TWeakObjectPtr::Get()` is safe to call from the game thread to check validity.

---

## TSharedPtr Thread Safety Modes

`TSharedPtr<T>` defaults to `ESPMode::NotThreadSafe` -- the reference count uses non-atomic operations. Sharing across threads causes data races on the refcount itself.

```cpp
// WRONG — default ESPMode is not thread-safe
TSharedPtr<FComputeBuffer> Buffer = MakeShared<FComputeBuffer>();

// RIGHT — atomic refcount for cross-thread sharing
TSharedPtr<FComputeBuffer, ESPMode::ThreadSafe> Buffer =
    MakeShared<FComputeBuffer, ESPMode::ThreadSafe>();

// The data INSIDE the buffer still needs its own synchronization
// ESPMode::ThreadSafe only protects the pointer/refcount operations
```

**Key distinction:** `ESPMode::ThreadSafe` makes the *pointer operations* (copy, destroy, reset) thread-safe. It does NOT protect the pointed-to data. You still need locks or atomics for the actual data if mutated concurrently.

---

## FCriticalSection + FScopeLock Pattern

Use `FCriticalSection` (recursive mutex) when multiple threads read and write shared non-UObject data.

```cpp
class FThreadSafeAccumulator
{
public:
    void AddSample(float Value)
    {
        FScopeLock Lock(&CriticalSection);  // acquires on construction
        Samples.Add(Value);
        Total += Value;
    }   // releases when Lock goes out of scope

    float GetAverage() const
    {
        FScopeLock Lock(&CriticalSection);
        return Samples.Num() > 0 ? Total / Samples.Num() : 0.0f;
    }

private:
    mutable FCriticalSection CriticalSection;
    TArray<float> Samples;
    float Total = 0.0f;
};
```

**Always use `FScopeLock`** -- never call `Lock()` / `Unlock()` manually. Manual lock/unlock risks missing the unlock path on early returns or exceptions.

---

## FRWLock for Read-Heavy Scenarios

When reads vastly outnumber writes, `FRWLock` allows concurrent readers while writers get exclusive access. Significant performance win over `FCriticalSection` in read-heavy workloads.

```cpp
class FThreadSafeCache
{
public:
    FVector LookupPosition(FName Key) const
    {
        FReadScopeLock ReadLock(RWLock);  // multiple readers allowed
        const FVector* Found = PositionCache.Find(Key);
        return Found ? *Found : FVector::ZeroVector;
    }

    void UpdatePosition(FName Key, FVector NewPos)
    {
        FWriteScopeLock WriteLock(RWLock);  // exclusive access
        PositionCache.Add(Key, NewPos);
    }

private:
    mutable FRWLock RWLock;
    TMap<FName, FVector> PositionCache;
};
```

**Critical:** `FRWLock` is NOT recursive. Do not acquire a read lock while holding a read lock, and do not acquire a write lock while holding a read lock. Both cause deadlocks on some platforms.

---

## std::atomic Patterns

`FThreadSafeCounter` and `FThreadSafeBool` are deprecated in engine source comments. Use `std::atomic` directly.

```cpp
class FBackgroundProcessor
{
public:
    void RequestStop() { bShouldStop.store(true, std::memory_order_relaxed); }
    bool IsStopped() const { return bShouldStop.load(std::memory_order_relaxed); }

    int32 GetProcessedCount() const { return ProcessedCount.load(std::memory_order_relaxed); }
    void IncrementProcessed() { ProcessedCount.fetch_add(1, std::memory_order_relaxed); }

private:
    std::atomic<bool> bShouldStop{false};
    std::atomic<int32> ProcessedCount{0};
};
```

**Memory ordering:** `std::memory_order_relaxed` is sufficient for simple flags and counters where you do not need happens-before guarantees with other data. Use `std::memory_order_acquire` / `std::memory_order_release` when the atomic guards visibility of other non-atomic writes.

---

## Double-Buffering Pattern

For transferring bulk data from a background thread to the game thread without locks during the hot path. The background thread writes to one buffer while the game thread reads from the other.

```cpp
class FDoubleBufferedData
{
public:
    // Background thread writes to back buffer
    void WriteBackBuffer(TArray<FVector>&& NewData)
    {
        FScopeLock Lock(&SwapLock);
        BackBuffer = MoveTemp(NewData);
        bSwapPending.store(true, std::memory_order_release);
    }

    // Game thread swaps and reads — call once per tick
    const TArray<FVector>& SwapAndRead()
    {
        if (bSwapPending.load(std::memory_order_acquire))
        {
            FScopeLock Lock(&SwapLock);
            Swap(FrontBuffer, BackBuffer);
            bSwapPending.store(false, std::memory_order_relaxed);
        }
        return FrontBuffer;  // lock-free read on game thread
    }

private:
    TArray<FVector> FrontBuffer;  // game thread reads
    TArray<FVector> BackBuffer;   // background thread writes
    FCriticalSection SwapLock;    // only held during swap
    std::atomic<bool> bSwapPending{false};
};
```

The lock is only contended during the brief swap operation. The game thread reads the front buffer without any synchronization for the rest of the frame.

---

## Lock Ordering Rules

When multiple locks must be held simultaneously, always acquire them in a consistent global order. Inconsistent ordering between threads causes deadlocks.

**Rules:**
1. **Define a total order** for all locks in your system (e.g., by subsystem, then by allocation order).
2. **Always acquire in ascending order.** If thread A holds Lock1 and needs Lock2, Lock2 must have a higher order than Lock1.
3. **Never hold a lock while calling unknown code** (callbacks, delegates, virtual functions). The callee may try to acquire a lock with a lower order.
4. **Prefer lock-free patterns** (`TQueue`, `std::atomic`, double-buffering) when they fit. No locks means no deadlocks.
5. **Keep critical sections short.** Do expensive computation outside the lock, then lock briefly to commit results.

```cpp
// WRONG — inconsistent order causes deadlock
// Thread 1: Lock(A) -> Lock(B)
// Thread 2: Lock(B) -> Lock(A)

// RIGHT — consistent order
// Thread 1: Lock(A) -> Lock(B)
// Thread 2: Lock(A) -> Lock(B)
```

When in doubt, restructure to use a single lock or a lock-free queue. Two locks that must be held simultaneously usually indicate a design that can be simplified.
