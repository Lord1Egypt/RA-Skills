# Profiling Commands & Unreal Insights

Reference for stat commands, Unreal Insights capture, custom profiling markers, CSV telemetry, and performance analysis workflow.

---

## Built-in Stat Commands

All `stat` commands are typed into the in-game console (`~`) or passed via `-ExecCmds` on the command line.

### Frame & CPU

| Command | Description |
|---|---|
| `stat fps` | Frame rate and frame time overlay |
| `stat unit` | Game, Draw, GPU, Frame times in ms |
| `stat unitgraph` | Rolling graph of unit timings |
| `stat game` | Game thread breakdown: Tick, Actors, Components |
| `stat engine` | Engine-level counters |
| `stat tasks` | Async task system occupancy |
| `stat threads` | Per-thread CPU times |
| `stat slate` | Slate UI widget tick cost |
| `stat scenerendering` | Scene rendering draw calls and primitives |
| `stat initviews` | Visibility / frustum culling cost |

### Memory

| Command | Description |
|---|---|
| `stat memory` | High-level memory categories |
| `stat memoryplatform` | OS-level virtual / physical memory |
| `stat streaming` | Texture and mesh streaming stats |
| `stat streamingdetails` | Per-resource streaming detail |
| `memreport` | Full memory dump to `Saved/Profiling/MemReports/` |
| `memreport -full` | Extended dump including asset registry |
| `obj list class=Texture2D` | Count and size of all loaded Texture2D objects |
| `obj list class=StaticMesh sortby=size` | Mesh objects sorted by memory |

### GPU

| Command | Description |
|---|---|
| `stat gpu` | Per-pass GPU time overlay (requires GPU timing support) |
| `ProfileGPU` | Single-frame GPU capture, opens in RenderDoc-style viewer |
| `r.ProfileGPU.Pattern *` | Set capture pattern (default `*` = everything) |
| `r.GPUBusyWait 1` | Force busy-wait timing for more accurate GPU stats |

### Networking

| Command | Description |
|---|---|
| `stat net` | Network channel counts, saturation, packet loss |
| `stat netdetailed` | Per-actor replication bandwidth |
| `net.Stats 1` | Enable network stats overlay |

---

## Capturing Stats to File

### .uestats Capture (Legacy)

```
# In-game console
stat startfile          # starts recording to Saved/Profiling/
stat stopfile           # stops and writes the .uestats file

# Open in: UnrealEditor > Window > Session Frontend > Profiler tab
# Or use deprecated StatsViewer commandlet
```

### Command-Line Automated Capture

```bash
# Capture for 10 seconds then exit
UnrealEditor-Cmd MyGame -game \
    -ExecCmds="stat startfile, delay 10, stat stopfile, quit" \
    -log
```

---

## Unreal Insights

Unreal Insights replaces the legacy profiler for CPU, GPU, memory, and network trace analysis.

### Starting a Trace

```bash
# Attach Insights at launch (preferred for full coverage)
UnrealEditor MyGame \
    -trace=cpu,gpu,frame,memory,loadtime,log,bookmark \
    -tracehost=127.0.0.1         # send to local Insights recorder
    # or -tracefile=MyCapture.utrace   to write directly to disk

# Insight trace channels
#   cpu        — CPU thread events and named events
#   gpu        — GPU pass timings (requires RHI support)
#   frame      — per-frame markers
#   memory     — LLM allocation tracking
#   loadtime   — asset and package load timings
#   log        — UE_LOG lines embedded in timeline
#   bookmark   — UE_TRACE_BOOKMARK calls
#   task       — Task Graph tasks
#   rhicommands — RHI command list
```

### Runtime Console Commands

```
# Start trace mid-session
Trace.Start cpu,frame,gpu

# Stop trace
Trace.Stop

# Bookmark (appears as vertical line in Insights timeline)
Trace.Bookmark "LevelLoaded"
```

### Opening Insights

```bash
# Launch the standalone Insights app
Engine/Binaries/Win64/UnrealInsights.exe

# Open a .utrace file directly
UnrealInsights.exe MyCapture.utrace
```

Key Insights views:

- **Timing Insights** — CPU/GPU flame chart, thread rows
- **Memory Insights** — allocation timeline, LLM categories
- **Asset Loading** — package load waterfall
- **Networking** — connection bandwidth and packet timeline

---

## Custom Profiling Markers

### SCOPE_CYCLE_COUNTER

Links to the stat system (visible in `stat MyGame` overlay and Insights).

```cpp
// In a .cpp file — one DECLARE per stat, referenced anywhere in the module
DECLARE_STATS_GROUP(TEXT("MyGame"), STATGROUP_MyGame, STATCAT_Advanced);
DECLARE_CYCLE_STAT(TEXT("InventoryTick"),  STAT_InventoryTick,  STATGROUP_MyGame);
DECLARE_CYCLE_STAT(TEXT("PathFinder"),     STAT_PathFinder,     STATGROUP_MyGame);
DECLARE_CYCLE_STAT(TEXT("AbilityResolve"), STAT_AbilityResolve, STATGROUP_MyGame);

// Usage
void UInventoryComponent::TickComponent(float DeltaTime, ...)
{
    SCOPE_CYCLE_COUNTER(STAT_InventoryTick);
    // ...
}
```

### SCOPED_NAMED_EVENT

Shows as a colored block in Insights without stat overhead.

```cpp
#include "HAL/PlatformMisc.h"

void UMySystem::ProcessBatch()
{
    SCOPED_NAMED_EVENT(MySystem_ProcessBatch, FColor::Orange);
    for (auto& Item : Batch)
    {
        SCOPED_NAMED_EVENT_TEXT("ItemProcess", FColor::Yellow);
        Process(Item);
    }
}
```

### UE_TRACE_BOOKMARK

Places a labelled vertical marker in the Insights timeline.

```cpp
#include "ProfilingDebugging/TraceAuxiliary.h"  // or use Trace.Bookmark in console

UE_TRACE_BOOKMARK(TEXT("WaveStarted_%d"), WaveNumber);
```

---

## CSV Profiling

CSV profiling writes lightweight, always-on telemetry to `Saved/Profiling/CSVStats/`. Enable with `-csvstatfile` or the auto-started profiler.

```cpp
#include "ProfilingDebugging/CsvProfiler.h"

// Declare category once per module
CSV_DEFINE_CATEGORY(MyGame, true);   // true = enabled by default

// Timing stat in a function (duration captured each frame)
void UMySystem::Tick(float DeltaTime)
{
    CSV_SCOPED_TIMING_STAT(MyGame, SystemTick);
    // ...
}

// Custom scalar value
void UMySystem::PostSpawn()
{
    CSV_CUSTOM_STAT(MyGame, ActiveEnemies, ActiveEnemyCount, ECsvCustomStatOp::Set);
    CSV_CUSTOM_STAT(MyGame, DamageDealt,   FrameDamage,      ECsvCustomStatOp::Accumulate);
}

// Named event (segment in CSV timeline)
CSV_EVENT(MyGame, TEXT("LevelLoaded"));
```

### Launching with CSV Capture

```bash
UnrealEditor-Cmd MyGame -game \
    -csvstatfile=MySession.csv \
    -csvCaptureFrames=1000 \     # capture 1000 frames then stop
    -log
```

Open `.csv` output with Python / Excel or the **PerfReportTool** (`Engine/Extras/PerfReportTool/`).

---

## LLM (Low-Level Memory Tracker)

LLM categorises allocations for memory profiling in Insights.

```cpp
#include "HAL/LowLevelMemTracker.h"

// Push/pop a custom LLM scope
LLM_SCOPE(ELLMTag::EngineMisc);                    // built-in tag
LLM_SCOPE_BYTAG(MyGame_Inventory);                 // custom tag (declared separately)

// Declare a custom LLM tag (in a cpp, once)
LLM_DEFINE_TAG(MyGame_Inventory, TEXT("MyGame/Inventory"), TEXT("MyGame"));

// Use in allocations
{
    LLM_SCOPE_BYTAG(MyGame_Inventory);
    InventoryData = new FInventoryData();
}
```

Activate LLM at launch:

```bash
UnrealEditor MyGame -LLM -trace=memory -tracehost=127.0.0.1
```

---

## Performance Analysis Workflow

### 1. Identify the Bottleneck

```
stat unit          # Is Frame time dominated by Game, Draw, or GPU?
stat fps           # Confirm frame rate
```

- **Game > 33ms** → CPU game thread (tick, AI, physics logic)
- **Draw > 33ms** → Render thread (draw calls, visibility)
- **GPU > 33ms** → GPU fill rate, overdraw, shader complexity

### 2. Drill Down on CPU

```
stat game          # Which game-thread category?
stat engine        # Is it engine overhead?
stat tasks         # Async task contention?
```

Then capture with Insights (`-trace=cpu,frame`) and look at the flame chart.

### 3. Drill Down on GPU

```
stat gpu           # Per-pass timings
ProfileGPU         # Single-frame breakdown
r.ProfileGPU.Pattern BasePass    # isolate specific pass
```

### 4. Memory Pressure

```
stat memory
memreport -full
obj list class=Texture2D sortby=size
```

Insights memory view shows allocation spikes over time.

### 5. Reproduce and Baseline

Always capture a baseline before any optimization. Use CSV profiling for production telemetry:

```bash
# Baseline run
UnrealEditor-Cmd MyGame -game -csvstatfile=Baseline.csv -csvCaptureFrames=600

# After optimization
UnrealEditor-Cmd MyGame -game -csvstatfile=Optimized.csv -csvCaptureFrames=600

# Diff with PerfReportTool or a Python script
```

---

## GPU Profiling with RenderDoc

```bash
# Launch with RenderDoc capture support
UnrealEditor MyGame -AttachRenderDoc

# In-game console
renderdoc.CaptureFrame    # capture next frame
```

Or attach RenderDoc externally and use **F12** to capture. Open `.rdc` in the RenderDoc UI for draw-call-level inspection.

---

## Profiling on Device (Mobile / Console)

```bash
# iOS / Android — tunnel Insights over USB
UnrealInsights.exe -RecorderAddress=127.0.0.1:1980

# On device launch with
-trace=cpu,frame -tracehost=<HOST_IP>

# Console-specific profiling tools (e.g. PlayStation Razor / Xbox PIX)
# integrate via platform-specific plugin; SCOPE_CYCLE_COUNTER feeds into them automatically
```

---

## Quick Reference: Command-Line Profiling Flags

| Flag | Effect |
|---|---|
| `-trace=cpu,gpu,frame,memory,log` | Enable trace channels for Insights |
| `-tracehost=127.0.0.1` | Send trace to local Insights recorder |
| `-tracefile=Output.utrace` | Write trace directly to file |
| `-LLM` | Enable Low-Level Memory Tracker |
| `-csvstatfile=Out.csv` | Start CSV profiling |
| `-csvCaptureFrames=N` | Stop CSV after N frames |
| `-statnamedevents` | Include stat names in profiler named events |
| `-ExecCmds="stat startfile"` | Begin stats file capture on startup |
