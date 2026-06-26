# Threading Patterns Reference

Complete code templates for UE async and threading patterns. Each template is production-ready with proper lifecycle management and error handling.

---

## FRunnable Subclass Template

Full dedicated-thread pattern with cooperative shutdown via `std::atomic<bool>`.

```cpp
#include "HAL/Runnable.h"
#include "HAL/RunnableThread.h"
#include "HAL/PlatformProcess.h"
#include <atomic>

class FMyBackgroundWorker : public FRunnable
{
public:
    FMyBackgroundWorker() = default;

    // Start the thread — call from game thread
    void StartThread()
    {
        Thread = FRunnableThread::Create(
            this,
            TEXT("MyBackgroundWorker"),
            0,                    // StackSize (0 = platform default)
            TPri_BelowNormal,    // lower than game thread
            FPlatformAffinity::GetPoolThreadMask()
        );
    }

    // Request shutdown and wait — call from game thread
    ~FMyBackgroundWorker()
    {
        if (Thread)
        {
            Thread->Kill(true);  // calls Stop(), then blocks until Run() exits
            delete Thread;
            Thread = nullptr;
        }
    }

    // --- FRunnable interface ---

    bool Init() override
    {
        // Runs on NEW thread before Run() starts
        // Return false to abort thread creation
        return true;
    }

    uint32 Run() override
    {
        // Runs on the NEW thread
        while (!bShouldStop.load(std::memory_order_relaxed))
        {
            // --- Do your work here ---
            ProcessNextWorkItem();

            // Yield to prevent CPU spin when no work available
            FPlatformProcess::Sleep(0.001f);
        }
        return 0;
    }

    void Stop() override
    {
        // Called from OUTSIDE the thread (by Kill or directly)
        // Must be thread-safe — only set the atomic flag
        bShouldStop.store(true, std::memory_order_relaxed);
    }

    void Exit() override
    {
        // Runs on the worker thread AFTER Run() returns
        // Clean up thread-local resources here
    }

private:
    std::atomic<bool> bShouldStop{false};
    FRunnableThread* Thread = nullptr;

    void ProcessNextWorkItem()
    {
        // Your actual work implementation
    }
};
```

---

## FNonAbandonableTask + FAsyncTask Template

Thread pool work unit pattern. The `friend` declaration lets `FAsyncTask` construct the inner task.

```cpp
#include "Async/AsyncWork.h"

class FChunkProcessTask : public FNonAbandonableTask
{
    friend class FAsyncTask<FChunkProcessTask>;

public:
    // Results accessible after completion
    TArray<FVector> ProcessedVertices;

private:
    // Constructor — args forwarded from FAsyncTask constructor
    FChunkProcessTask(TArray<FVector> InRawVertices, float InScale)
        : RawVertices(MoveTemp(InRawVertices))
        , Scale(InScale)
    {}

    void DoWork()
    {
        ProcessedVertices.Reserve(RawVertices.Num());
        for (const FVector& V : RawVertices)
        {
            ProcessedVertices.Add(V * Scale);
        }
    }

    FORCEINLINE TStatId GetStatId() const
    {
        RETURN_QUICK_DECLARE_CYCLE_STAT(FChunkProcessTask, STATGROUP_ThreadPoolAsyncTasks);
    }

    TArray<FVector> RawVertices;
    float Scale;
};

// --- Usage: reusable task ---
auto* Task = new FAsyncTask<FChunkProcessTask>(MoveTemp(Vertices), 2.0f);
Task->StartBackgroundTask();          // dispatch to GThreadPool
// ... do other game thread work ...
Task->EnsureCompletion();             // block until done
TArray<FVector> Result = MoveTemp(Task->GetTask().ProcessedVertices);
delete Task;

// --- Usage: fire-and-forget ---
(new FAutoDeleteAsyncTask<FChunkProcessTask>(MoveTemp(Vertices), 2.0f))
    ->StartBackgroundTask();
// Task auto-deletes when DoWork completes — no result retrieval possible
```

---

## TGraphTask Template with Prerequisites

Custom TaskGraph task with dependency chaining.

```cpp
#include "Async/TaskGraphInterfaces.h"

class FComputeNavTask
{
public:
    FComputeNavTask(TArray<FVector>& InOutPath) : Path(InOutPath) {}

    static ESubsequentsMode::Type GetSubsequentsMode()
    {
        return ESubsequentsMode::TrackSubsequents;
    }

    ENamedThreads::Type GetDesiredThread()
    {
        return ENamedThreads::AnyThread;
    }

    TStatId GetStatId() const
    {
        RETURN_QUICK_DECLARE_CYCLE_STAT(FComputeNavTask, STATGROUP_TaskGraphTasks);
    }

    void DoTask(ENamedThreads::Type CurrentThread, const FGraphEventRef& MyCompletionGraphEvent)
    {
        // Compute path — runs on worker thread
        for (FVector& Point : Path)
        {
            Point = SmoothPoint(Point);
        }
    }

private:
    TArray<FVector>& Path;
};

// --- Dispatch with prerequisites ---
FGraphEventArray NoPrereqs;
FGraphEventRef StepA = TGraphTask<FComputeNavTask>::CreateTask(&NoPrereqs)
    .ConstructAndDispatchWhenReady(PathData);

FGraphEventArray StepAPrereq;
StepAPrereq.Add(StepA);
FGraphEventRef StepB = TGraphTask<FApplyNavTask>::CreateTask(&StepAPrereq)
    .ConstructAndDispatchWhenReady(PathData);

// Wait for final step on game thread
FTaskGraphInterface::Get().WaitUntilTaskCompletes(StepB, ENamedThreads::GameThread);
```

---

## UE::Tasks::Launch with Prerequisites

Modern preferred API (UE 5.0+).

```cpp
#include "Tasks/Task.h"

// Step 1: compute positions
UE::Tasks::TTask<TArray<FVector>> PosTask = UE::Tasks::Launch(
    UE_SOURCE_LOCATION,
    []() -> TArray<FVector>
    {
        TArray<FVector> Positions;
        // ... expensive computation ...
        return Positions;
    }
);

// Step 2: depends on step 1
UE::Tasks::TTask<TArray<FVector>> SmoothTask = UE::Tasks::Launch(
    UE_SOURCE_LOCATION,
    [&PosTask]() -> TArray<FVector>
    {
        TArray<FVector> Raw = PosTask.GetResult();
        // ... smooth positions ...
        return Raw;
    },
    UE::Tasks::Prerequisites(PosTask)
);

// Retrieve on game thread (blocks until chain completes)
TArray<FVector> Final = SmoothTask.GetResult();

// Non-blocking check
if (SmoothTask.IsCompleted()) { /* safe to GetResult without blocking */ }

// Timed wait
if (SmoothTask.Wait(FTimespan::FromMilliseconds(5.0)))
{
    // completed within timeout
}
```

---

## ParallelFor Variants

```cpp
#include "Async/ParallelFor.h"

// Basic — all iterations equal cost
ParallelFor(Meshes.Num(), [&Meshes](int32 Index)
{
    ProcessMesh(Meshes[Index]);
});

// With MinBatchSize — avoids thread overhead for small counts
ParallelFor(TEXT("MeshProcess"), Meshes.Num(), 128,
    [&Meshes](int32 Index) { ProcessMesh(Meshes[Index]); }
);

// With flags — variable-cost iterations at background priority
ParallelFor(Meshes.Num(), [&Meshes](int32 Index)
{
    ProcessMesh(Meshes[Index]);
}, EParallelForFlags::Unbalanced | EParallelForFlags::BackgroundPriority);

// With per-thread context — avoids per-iteration allocation
TArray<FMyThreadContext> OutContexts;
ParallelForWithTaskContext(TEXT("GenNormals"), OutContexts, Meshes.Num(), 64,
    [&Meshes](FMyThreadContext& Ctx, int32 Index)
    {
        // Ctx is unique per worker thread — use as scratch buffer
        Ctx.TempBuffer.Reset();
        ComputeNormals(Meshes[Index], Ctx.TempBuffer);
    }
);
```

---

## Async() with EAsyncExecution Modes

```cpp
#include "Async/Async.h"

// ThreadPool — most common for CPU work
TFuture<int32> F1 = Async(EAsyncExecution::ThreadPool,
    []() { return HeavyCompute(); });

// TaskGraphMainThread — runs on game thread next tick
TFuture<void> F2 = Async(EAsyncExecution::TaskGraphMainThread,
    []() { /* safe for UObject access */ });

// Thread — dedicated thread for blocking I/O
TFuture<TArray<uint8>> F3 = Async(EAsyncExecution::Thread,
    []() { return FFileHelper::LoadFileToArray(...); });

// Convenience wrappers
TFuture<int32> F4 = AsyncPool(GThreadPool,
    []() { return Compute(); });
TFuture<void> F5 = AsyncThread(
    []() { BlockingIOWork(); },
    0,             // StackSize (0 = default)
    TPri_Normal);
```

---

## TPromise/TFuture Producer-Consumer

Decouples the code that produces a value from the code that consumes it.

```cpp
#include "Async/Future.h"
#include "Async/Async.h"

// Create promise/future pair
TPromise<FAnalyticsResult> Promise;
TFuture<FAnalyticsResult> Future = Promise.GetFuture(); // call exactly once

// Producer — moves promise into background work
Async(EAsyncExecution::ThreadPool, [P = MoveTemp(Promise)]() mutable
{
    FAnalyticsResult Result;
    Result.PlayerCount = GatherPlayerMetrics();
    Result.FrameStats = GatherFrameMetrics();
    P.SetValue(MoveTemp(Result)); // or P.EmplaceValue(args...)
});

// Consumer — chain continuation or block
Future.Then([](TFuture<FAnalyticsResult> F)
{
    FAnalyticsResult R = F.Get(); // Get() does NOT invalidate
    UE_LOG(LogGame, Log, TEXT("Players: %d"), R.PlayerCount);
});

// Or block directly on game thread (use sparingly)
FAnalyticsResult R = Future.Get();
```
