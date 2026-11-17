---
name: solo-build
slug: solo-build
displayName: "Build"
version: 1.0.1
summary: "用TDD工作流执行实施"
description: 用TDD工作流执行实施计划任务,自动提交与阶段门禁。提供专业的能力支持,适用于多种工作场景。内置错误恢复与降级机制,跨格式适配,适配多源数据。 功能涵盖:。Use when 需要项目管理、任务规划、进度跟踪、团队协作时使用。不适用于实际人员绩效评估。适用于独立开发者、企业团队和自动化工作流场景。支持中文交互，无需复杂配置即开即用。 功能涵盖: solo。
license: "MIT"
tools:
  - read
  - exec
tags:
  - task
  - plan
  - project
  - docs
  - files
category: "Productivity"
pricing_tier: "L2-标准级"

---

> **功能说明**: 本技能涵盖 专业的能力支持、提交与阶段门禁 等核心能力。

> **功能说明**: 本技能涵盖 中文交互、化工作流场景 等核心能力。

This skill is self-contained — follow the task loop, TDD rules, and completion flow below instead of delegating to external build/execution skills (superpowers, etc.).

Execute tasks from an implementation plan. Finds `plan.md` (in `docs/plan/`), picks the next unchecked task, implements it with TDD workflow, commits, and updates progress.

## When to use
After `/plan` has created a track with `spec.md` + `plan.md`. This is the execution engine.

Pipeline: `/plan` → **`/build`** → `/deploy` → `/review`

## 协议 Tools (use if available)
* `session_search(query)` — find how similar problems were solved before
* `project_code_search(query, project)` — find reusable code across projects
* `codegraph_query(query)` — check file dependencies, imports, callers

If 协议 tools are not available, fall back to Glob + Grep + Read.

## Pre-flight Checks
> 详细内容已移至 `references/detail.md`

## Track Selection
### If `$ARGUMENTS` contains a track ID:
* Validate: `{plan_root}/{argument}/plan.md` exists (check `docs/plan/`).
* If not found: search `docs/plan/*/plan.md` for partial matches, suggest corrections.

### If `$ARGUMENTS` contains `--task X.Y`:
* Jump directly to that task in the active track.

### If no argument:
1. Search for `plan.md` files in `docs/plan/`.
2. Read each `plan.md`, find tracks with uncompleted tasks.
3. If multiple, ask via AskUserQuestion.
4. If zero tracks: "No plans found. Run `/plan` first."

## Context Loading
### Step 1 — Architecture overview (if 协议 available)
```text
codegraph_explain(project="{project name}")
```

Returns: stack, languages, directory layers, key patterns, top dependencies, hub files — one call instead of exploring the tree manually.

### Step 2 — Essential docs (parallel reads)
1. `docs/plan/{trackId}/plan.md` — task list (REQUIRED)
2. `docs/plan/{trackId}/spec.md` — acceptance criteria (REQUIRED)
3. `docs/workflow.md` — TDD policy, commit strategy (if exists)
4. `.md` — architecture, Do/Don't
5. `.solo/pipelines/progress.md` — running docs from previous iterations (if exists, pipeline-specific). Contains what was done in prior pipeline sessions: stages completed, commit SHAs, last output lines. **Use this to avoid repeating completed work.**

**Do NOT read source code files at this stage.** Only docs. Source files are loaded per-task in the execution loop (step 3 below).

## Resumption
If a task is marked `[~]` in plan.md:

```text
Resuming: {track title}
Last task: Task {X.Y}: {description} [in progress]

1. Continue from where we left off
2. Restart current task
3. Show progress summary first
```

Ask via AskUserQuestion, then proceed.

## Task Execution Loop
**Makefile convention:** If `Makefile` exists in project root, **always prefer `make` targets** over raw commands. Use `make test` instead of `pnpm test`, `make lint` instead of `pnpm lint`, `make build` instead of `pnpm build`, etc. Run `make help` (or read Makefile) to discover available targets. If a `make integration` or similar target exists, use it for integration testing after pipeline-related tasks.

**IMPORTANT — All-done check:** Before entering the loop, scan plan.md for ANY `- [ ]` or `- [~]` tasks. If ALL tasks are `[x]` — skip the loop entirely and jump to **Completion** section below to run final verification and output `<solo:done/>`.

For each incomplete task in plan.md (marked `[ ]`), in order:

### 1. Find Next Task
Parse plan.md for first line matching `- [ ] Task X.Y:` (or `- [~] Task X.Y:` if resuming).

### 2. Start Task
* Update plan.md: `[ ]` → `[~]` for current task.
* Announce: **"Starting Task X.Y: {description}"**

### 3. Research (smart, before coding)
**Do NOT grep the entire project or read all source files.** Load only what this specific task needs.

**If 协议 available (preferred):**

1. `project_code_search(query="{task keywords}", project="{name}")` — find relevant code in the project. Read only the top 2-3 results.
2. `session_search("{task keywords}")` — check if you solved this before.
3. `codegraph_query("MATCH (f:File {project: '{name}'})-[:IMPORTS]->(dep) WHERE f.path CONTAINS '{module}' RETURN dep.path")` — check imports/dependencies of files you'll modify.

**If 协议 unavailable (fallback):**

1. Read ONLY the files explicitly mentioned in the task description (file paths).
2. Glob for the specific module directory the task targets (e.g., `src/auth/**/*.ts`), not the entire project.
3. If the task doesn't mention files, use Grep with a narrow pattern on `src/` or `app/` — never `**/*`.

**Never do:** `Grep "keyword" .` across the whole project. This dumps hundreds of lines into context for no reason. Be surgical.

### Python-Specific Quality Tools

### JS/TS-Specific Quality Tools

### iOS/Android-Specific Quality Tools
When the project uses a mobile stack:

**iOS (Swift):**

```bash
swiftlint lint --strict
swift-format format --in-place --recursive Sources/
```

**Android (Kotlin):**

```bash
./gradlew detekt
./gradlew ktlintCheck
```

Both use **lefthook** for pre-commit hooks (language-agnostic, no Node.js required).

### 4. TDD Workflow (if TDD enabled in workflow.md)
**Red — write failing test:**

* Create/update test file for the task functionality.
* Run tests to confirm they fail.

**Green — implement:**

* Write minimum code to make the test pass.
* Run tests to confirm pass.

**Refactor:**

* Clean up while tests stay green.
* Run tests one final time.

### 5. Non-TDD Workflow (if TDD is "none" or "moderate" and task is simple)
* Implement the task directly.
* Run existing tests to check nothing broke.
* For "moderate": write tests for business logic and API routes, skip for UI/config.

### 5.5. Integration Testing (CLI-First)
If the task touches core business logic (pipeline, algorithms, agent tools), run `make integration` (or the integration command from `docs/workflow.md`). The CLI exercises the same code paths as the UI without requiring a browser. If `make integration` fails, fix before committing.

### 5.6. Visual Verification (if browser/simulator/emulator available)

### 6. Complete Task

### 7. Phase Completion Check

## Error Handling
### Test Failure
```text
Tests failing after Task X.Y:
  {failure details}

1. Attempt to fix
2. Rollback task changes (git checkout)
3. Pause for manual intervention
```

Ask via AskUserQuestion. Do NOT automatically continue past failures.

## Track Completion
When all phases and tasks are `[x]`:

### 1. Final Verification
* **Run local build** — must pass before deploy:
  + Next.js: `pnpm build`
  + Python: `uv build` or `uv run python -m py_compile src/**/*.py`
  + Astro: `pnpm build`
  + Cloudflare: `pnpm build`
  + iOS: `xcodebuild -scheme {Name} -sdk iphonesimulator build`
  + Android: `./gradlew assembleDebug`
* Run full test suite.
* Run linter + type-checker.
* **Visual smoke test** (if tools available):
  + Web: start dev server, navigate to main page, check console for errors, take screenshot
  + iOS: build + install on simulator, launch, take screenshot, check logs
  + Android: build APK + install on emulator, launch, take screenshot, check logcat
  + Skip if tools unavailable — not a blocker for completion
* Check acceptance criteria from spec.md.

### 2. Update plan.md header
Change `**Status:** [ ] Not Started` → `**Status:** [x] Complete` at the top of plan.md.

### 3. Signal completion
Output pipeline signal ONLY if pipeline state directory (`.solo/states/`) exists:

```text
<solo:done/>
```

**Do NOT repeat the signal tag elsewhere in the response.** One occurrence only.

### 4. Summary
> 详细代码示例已移至 `references/detail.md`

## Reverting Work

## Progress Tracking (TodoWrite)
At the start of a build session, create a task list from plan.md so progress is visible:

1. **On session start:** Read plan.md, find all incomplete tasks (`[ ]` and `[~]`).
2. **Create TaskCreate** for each phase with its tasks as description.
3. **TaskUpdate** as you work: `in_progress` when starting a task, `completed` when done.
4. This gives the user (and pipeline) real-time visibility into progress.

## Rationalizations Catalog
These thoughts mean STOP — you're about to cut corners:

| Thought | Reality |
| --- | --- |
| "This is too simple to test" | Simple code breaks too. Write the test. |
| "I'll add tests later" | Tests written after pass immediately — they prove nothing. |
| "I already tested it manually" | Manual tests don't persist. Automated tests do. |
| "The test framework isn't set up" | Set it up. That's part of the task. |
| "This is just a config change" | Config changes break builds. Verify. |
| "I'm confident this works" | Confidence without evidence is guessing. Run the command. |
| "Let me just try changing X" | Stop. Investigate root cause first. |
| "Tests are passing, ship it" | Tests passing ≠ acceptance criteria met. Check spec.md. |
| "I'll fix the lint later" | Fix it now. Tech debt compounds. |
| "It works on my machine" | Run the build. Verify in the actual environment. |

## Critical Rules
1. **Run phase checkpoints** — verify tests + linter pass before moving to next phase.
2. **STOP on failure** — do not continue past test failures or errors.
3. **Keep plan.md updated** — task status must reflect actual progress at all times.
4. **Commit after each task** — atomic commits with conventional format.
5. **Research before coding** — 30 seconds of search saves 30 minutes of reimplementation.
6. **One task at a time** — finish current task before starting next.
7. **Keep test output concise** — when running tests, pipe through `head -50` or use `--reporter=dot` / `-q` flag. Thousands of test lines pollute context. Only show failures in detail.
8. **Verify before claiming done** — run the actual command, read the full output, confirm success BEFORE marking a task complete. Never say "should work now".

## Common Issues
### "No plans found"
**Cause:** No `plan.md` exists in `docs/plan/`.
**Fix:** Run `/plan "your feature"` first to create a track.

### Tests failing after task
**Cause:** Implementation broke existing functionality.
**Fix:** Use the error handling flow — attempt fix, rollback if needed, pause for user input. Never skip failing tests.

### Phase checkpoint failed
**Cause:** Tests or linter failed at phase boundary.
**Fix:** Fix failures before proceeding. Re-run verification for that phase.

## 依赖与配置
### 运行环境
- **Agent平台**: 支持SKILL.md的任意AI Agent( Code / Cursor / Codex /  CLI等)
- **操作系统**: Windows / macOS / Linux

### 依赖说明
| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:-------|:-----|:---------|:---------|
| LLM API | API | 必需 | 由Agent内置LLM提供 |

### API Key 配置
- 本Skill基于Markdown指令,无需额外API Key(除内容中明确标注的外部API)

### 可用性分类
- **分类**: MD+execute(纯Markdown指令,部分功能需要exec命令行执行能力)
- **说明**: 基于Markdown的AI Skill,通过自然语言指令驱动Agent执行任务

## 功能能力
```text
codegraph_explain(project="{project name}")
```

## 部署指引
1. 确认运行环境满足依赖说明中的要求
2. 在AI Agent对话中调用本技能,提供必要的输入参数
3. 检查输出结果,根据需要进行后续处理

> 详细的输入输出格式请参考下方章节说明。

## 典型场景
| 场景 | 输入 | 输出 |
|------|------|------|
| 基础使用 | 用户请求 | 处理结果 |

**不适用于**：需要人工判断的复杂决策场景

## 示例
### 示例1：基础用法
```
# 请参考上方使用说明进行配置和调用
result = "ready"
```

## 疑问整理
### Q1: 如何开始使用Build？
A: 请先阅读使用流程章节，确认环境满足依赖说明中的要求。

### Q2: 遇到错误怎么办？
A: 请参考错误处理章节，按照表格中的处理方式操作。

### Q3: Build有什么限制？
A: 请参考已知限制章节了解具体限制。

## 注意事项
- 需要LLM支持，无LLM环境无法使用
- 复杂场景可能需要人工辅助判断
- 性能取决于底层模型能力
