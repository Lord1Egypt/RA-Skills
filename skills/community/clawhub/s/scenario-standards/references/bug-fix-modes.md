# Bug Fix Mode Reference

Detailed diagnostic protocols for each bug type. Load the matching mode when its bug type activates.

---

## Regression Mode (Bisect)

Activate when: 以前是好的, used to work, 之前是好的, broke after update, 上一次提交还是对的, 回归

### Flow

1. **Protect the worktree first**: run `git status --short --branch -uall`. If the worktree is dirty, do NOT bisect in the current checkout. Create a detached worktree: `git worktree add --detach /tmp/bisect-<bug-name> <last-good-tag>` and run bisect there. Remove the worktree when done.

2. **Diff before bisect**: `git diff <last-good-tag>..HEAD -- <suspect-path>`. Read the delta first. The regression is usually visible in the diff at a fraction of a bisect's cost. Fall through to bisect only when the diff is too large or the culprit is not obvious.

3. **Bisect protocol** (when diff is insufficient):
   - Define a non-interactive pass/fail command upfront (script or one-liner).
   - `git bisect start HEAD <last-good-tag>`
   - `git bisect run <test-command>`
   - After it names the culprit: read that commit's diff down to the specific line.
   - `git bisect reset` before removing the temporary worktree.

4. **Read only the guilty commit**: after bisect finishes, read the culprit commit's diff. Cite the exact commit hash and line in the root cause report.

---

## Intermittent Bug Mode

Activate when: 时好时坏, 偶尔, 不稳定, intermittent, 有时候, 概率性, 随机, race condition

### Flow

1. **Reproduce reliably before diagnosing**. If reliable repro is genuinely impossible, state this explicitly and proceed with runtime instrumentation only. Do not claim "probably the same issue" without evidence.

2. **Targeted logging**: every log statement must be a yes/no question that rules a hypothesis in or out.
   - "If this prints X before Y, hypothesis A survives; otherwise A is dead."
   - A log that cannot rule a hypothesis in or out is noise. Delete it.

3. **Place logs at boundaries**: handler entry/exit, cache hit/miss, state setter, async callback entry, external API result. These are the boundaries where timing diverges.

4. **For race conditions**: capture event identity (timestamp, counter, request ID), monotonic ordering, and thread/queue identity. Log the order of arrival, not just the final state.

5. **If adding a log changes the behavior**: that is itself evidence of a timing, lifecycle, or concurrency problem. Do not ignore it.

6. **Instrument first, not after failure**: the moment your hypothesis involves "this callback fires before/after that one" or "this state should be X when Y runs", add the log immediately as part of forming the hypothesis, before writing any fix.

---

## Performance Mode

Activate when: 慢, slow, 卡顿, lag, 内存, memory, 卡死, not responding, beachball

### Flow

1. **Measure baseline first**: wall-clock time, profile sample, memory footprint. The specific tool depends on the runtime:
   - Browser: Performance tab, Memory tab, Lighthouse
   - Node.js: `--inspect`, clinic.js, 0x
   - Python: cProfile, py-spy, memory_profiler
   - Go: pprof, trace
   - Native: Instruments (macOS), perf (Linux)

2. **Fix, then re-measure and report before/after numbers**. "Feels faster" is not evidence.

3. **For native app freezes**: collect while frozen:
   - `sample <process>` (macOS) for stack traces
   - Recent app logs
   - CPU and memory footprint
   - Thread count and whether the main thread is blocked, spinning, or allocating
   - Common traps: path walks on the main thread, synchronous icon loading, first-paint hydrating full app state before showing UI

4. **Performance complaints need numbers, not impressions**. Report: wall-clock time (ms), operation count, memory (MB), before and after.

---

## Rendering / UI Mode

Activate when: 显示有问题, 样式不对, looks wrong, visual bug, 渲染错误, layout broken, PDF output wrong

### Flow

1. **Static analysis first**: trace paint layers, stacking contexts, and layer order in DevTools (or equivalent tooling). Understand what the compositor is doing before adding visual debug overlays or console.log.

2. **Only add instrumentation after static analysis fails**. Logs cannot capture what the compositor does.

3. **For PDF/print rendering**:
   - Check font loading (web fonts, custom fonts, font-display)
   - Check page overflow (content wider than page)
   - Check print-specific CSS rules (@media print, @page)
   - For WeasyPrint: check rendering quirks doc

4. **Runtime evidence requirement**: compile-only or build-only is not sufficient. You MUST open the app/page/artifact and verify the visible result. State which viewport sizes and states were checked.

5. **Distinguish from `/ui` aesthetic polish**: if the issue is purely subjective ("ugly", "不清晰"), route to `/ui`. If it is rendering, state, timing, or a regression, stay in this mode.

---

## Default Mode

Activate when: all other bugs not matching the specialized types above.

Standard flow: reproduce obtain error output classify in the table read relevant code form hypothesis fix blast verify. Follow the full Hard Constraints list from the main SKILL.md.
