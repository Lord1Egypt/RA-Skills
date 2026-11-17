# Bug Fix Gotchas

Accumulated from real failure patterns. Each entry records what happened and the rule that prevents it.

| What happened | Rule |
|---------------|------|
| Patched the wrong file (client pane instead of local, wrong handler, wrong module) | Trace the execution path backward before touching any file. Read the call chain from symptom to entry point. |
| Reproduced locally but failed in CI | Align the environment first (runtime version, env vars, timezone, locale), then chase the code. Two rounds of environment divergence without repair is the stop signal. |
| Stack trace points deep into a library | Walk back 3 frames into your own code. The bug is almost always at the boundary where your code calls the library, not inside the dependency. |
| Changed the code but the output stayed wrong | Confirm the runtime is not reading stale cache, persisted output, snapshot with a TTL, or build artifact that was not regenerated. Changing generated-then-persisted data requires invalidating or version-bumping the old cache in the same change. |
| Build passed but UI still looked wrong | Move up the runtime evidence ladder. Compile-only is not enough for UI, visual, rendering, or generated-artifact bugs. Open the real surface. |
| Fix matched the reporter's setup but regressed the default experience | State whether the fix changes the default behavior for all users or only the reporter's configuration. Prefer fixing the default path. |
| Blamed the symptom, not the cause | If the same error appears in multiple places, the root cause is the shared dependency or data source, not each call site individually. |
| Tracked a name/path that was renamed in a rename refactor | Before diagnosing, verify file paths and function names exist by grep. A stale reference in your reasoning is worse than no reference. |
| Broke after toggling theme/mode/locale, fine after restart | The state rebuild path is broken, not the initial load. Trace the toggle's recompute or invalidation route first. Do not tune styles pixel by pixel while the state path is broken. |
| Relied on function name, file name, or comment to understand behavior without reading the code | Only the code is authoritative. Function names, file names, and comments may be misleading, outdated, or describe intentions that were never implemented. Read the code. |
| Stacked patches onto a disproven hypothesis | Same symptom after a fix means the hypothesis was wrong. Re-read the execution path from scratch. Do not add another patch. |
| Fixed a single instance and declared the bug done | The same pattern often hides in N other places. Extract the pattern signature and grep the entire repo. One local fix with no blast scan leaves N-1 bugs in the tree. |
| Treated a convincing explainer or comment as ground truth | Comments describe intent, not behavior. A comment that says "this handles the edge case" is not proof it handles the edge case. Verify with code, not prose. |
| Reproduced from the app launcher, user hit the bug from file association / deep link | Reproduce using the exact entry point the user described. App-internal init differs from cold-launch-with-file init; state may not be ready when the document arrives via a different code path. |
| Reporter reproduces, local machine is fine, patched blind | Produce one copy-paste diagnostic command first (single command, silent collection, one output file). Diagnose from the returned evidence, then fix. Two rounds of blind patches without a probe is the stop signal. |
