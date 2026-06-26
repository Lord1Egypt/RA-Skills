# Plan: gstack Integration into WIP Code

**Date:** 2026-03-19
**Author:** cc-opus (with Parker)
**Status:** Current
**Depends on:** rename-to-wip-code (the CODE rename)
**Reference:** `ai/repos/gstack-private/` (local fork of github.com/garrytan/gstack)

## Context

gstack is Garry Tan's open-source "software factory" for Claude Code — 15 agent skills + a Playwright browser daemon. We forked it to `ai/repos/gstack-private` for reference. This plan identifies what to bring into WIP Code and who does what.

## What gstack has vs what we have

| Capability | gstack | WIP Code (us) | Gap |
|---|---|---|---|
| Guard rails (destructive cmd protection) | `/careful`, `/freeze`, `/guard` | `wip-branch-guard`, `wip-file-guard` | **None — ours are better** |
| License compliance | Nothing | `wip-license-guard`, `wip-license-hook` | **None** |
| Release pipeline | `/ship` (basic PR flow) | `wip-release` (version bump, changelog, npm publish, deploy) | **None — ours are better** |
| Repo scaffolding | Nothing | `wip-repo-init`, `wip-repos` | **None** |
| README formatting | Nothing | `wip-readme-format` | **None** |
| Browser QA automation | `/browse` (persistent Playwright daemon) | Nothing | **BIG GAP** |
| QA testing | `/qa`, `/qa-only` (state coverage, regression tests) | Nothing | **BIG GAP** |
| Code review | `/review` (SQL safety, XSS, LLM trust boundaries) | Nothing | **GAP** |
| Structured debugging | `/investigate` (4-phase root cause) | Nothing | **GAP** |
| Planning/design review | `/plan-ceo-review`, `/plan-eng-review`, `/plan-design-review` | Nothing | **Nice-to-have** |
| Multi-AI review | `/codex` (OpenAI second opinion) | Nothing | **Nice-to-have** |
| Multi-session orchestration | `conductor.json` | Nothing | **Future** |

## What to build (ordered by priority)

### Phase 1: Browser QA — `wip-browse` + `wip-qa`

**This is the big one.** gstack's `/browse` is ~2,500 lines of real TypeScript — persistent Chromium daemon, accessibility-tree ref system, sub-second latency. The `/qa` skill on top drives test → fix → verify loops.

#### What Parker does:
- Decide: port gstack's browse code, or build from scratch using it as reference?
  - **Port recommendation:** Their Bun/Playwright approach is solid. MIT licensed. We'd adapt it to our conventions (Universal Interface pattern, our SKILL.md format, our npm packaging).
- Decide: do we need Bun as a dependency, or can we port to Node?
  - gstack uses Bun for: compiled binaries, native SQLite (cookie import), fast HTTP server
  - Node alternative: use `pkg` or `esbuild` for binaries, `better-sqlite3` for cookies, `http` module for server
- Decide: scope. Full browser automation or just "verify a deployed URL loads and looks right"?

#### What Claude does:
- Create `tools/wip-browse/` following our tool conventions
- Port or adapt the core daemon: `server.ts`, `cli.ts`, `browser-manager.ts`, `commands.ts`, `snapshot.ts`
- Strip what we don't need (cookie picker UI, gstack-specific preamble)
- Add Universal Interface wrappers (CLI + Module + MCP + Skill)
- Create `tools/wip-qa/` as the skill layer on top of wip-browse
- Adapt gstack's state coverage map pattern (LOADING/EMPTY/ERROR/SUCCESS)
- Write tests

#### Files to study:
- `ai/repos/gstack-private/browse/src/server.ts` — daemon architecture
- `ai/repos/gstack-private/browse/src/browser-manager.ts` — ref system
- `ai/repos/gstack-private/browse/src/commands.ts` — command registry
- `ai/repos/gstack-private/browse/src/snapshot.ts` — accessibility tree parsing
- `ai/repos/gstack-private/qa/SKILL.md` — QA workflow patterns

---

### Phase 2: Code Review — `wip-review`

Pure prompt engineering. gstack's `/review` has good checklists we should steal.

#### What Parker does:
- Decide: standalone tool or part of a CI gate?
- Decide: scope (just security? full code quality? design review too?)

#### What Claude does:
- Create `tools/wip-review/` with SKILL.md
- Adapt gstack's checklist patterns:
  - SQL injection / parameterized queries
  - XSS / unsanitized output
  - LLM trust boundary violations (treating AI output as trusted)
  - Error path analysis (silent failures, swallowed exceptions)
  - Conditional side effects (state mutations in unexpected branches)
- Add our own patterns:
  - License compliance checks (we know this domain)
  - Dependency vulnerability flags
  - CLAUDE.md / identity file tampering detection
- Hook integration: run as pre-push or pre-merge hook

#### Files to study:
- `ai/repos/gstack-private/review/SKILL.md` — review workflow
- `ai/repos/gstack-private/review/checklist.md` — security checklist
- `ai/repos/gstack-private/review/design-checklist.md` — design checklist

---

### Phase 3: Structured Debugging — `wip-investigate`

Pure prompt engineering. gstack's 4-phase approach is well-designed.

#### What Parker does:
- Decide: standalone skill or folded into an existing tool?

#### What Claude does:
- Create `tools/wip-investigate/` with SKILL.md
- Adapt gstack's 4-phase pattern:
  1. Reproduce (confirm the bug exists, get exact repro steps)
  2. Isolate (narrow to smallest failing case)
  3. Root cause (find the actual bug, not symptoms)
  4. Fix + verify (fix, test, confirm no regression)
- Core rule: "No fixes without root cause" — prevent whack-a-mole debugging

#### Files to study:
- `ai/repos/gstack-private/investigate/SKILL.md`

---

### Phase 4: Planning Skills — `wip-plan`

Lower priority. Prompt engineering for structured planning.

#### What Parker does:
- Decide: do we need this? Or is it out of scope for CODE?
- If yes: which of gstack's 3 plan skills matter? (CEO review, eng review, design review)

#### What Claude does:
- If approved: create `tools/wip-plan/` with multiple SKILL.md variants
- Adapt the useful patterns (architecture lock-in detection, error/rescue maps)
- Skip the YC-specific stuff (narrowest wedge thinking, startup mode vs builder mode)

---

### Phase 5: Multi-Session Orchestration — `wip-conductor`

Future. gstack's `conductor.json` defines parallel Claude Code sessions.

#### What Parker does:
- Decide: is this relevant for multi-repo devops? (e.g., run license checks across 10 repos in parallel)
- This is a v3+ feature. Park it.

#### What Claude does:
- Nothing yet. Reference `ai/repos/gstack-private/conductor.json` when the time comes.

---

## Execution order

```
1. CODE rename (already planned, do first)
   └── 2. wip-browse + wip-qa (Phase 1 — biggest value, hardest work)
       └── 3. wip-review (Phase 2 — medium value, easy)
           └── 4. wip-investigate (Phase 3 — medium value, easy)
               └── 5. wip-plan (Phase 4 — low priority, Parker decides)
```

Phases 2-4 are independent of each other but all depend on the rename landing first (so we're building into WIP Code, not "AI DevOps Toolbox").

## Decisions (resolved)

| # | Decision | Resolution | Notes |
|---|----------|-----------|-------|
| 1 | Port gstack's browse code or build from scratch? | **Port + adapt** | MIT licensed, too much real engineering to redo |
| 2 | Bun or Node for wip-browse? | **TBD** | See Bun vs Node section below. Parker to confirm. |
| 3 | wip-review scope? | **Security + code quality** | Both. Parker confirmed. |
| 4 | Do we need wip-plan? | **Later** | Not core |
| 5 | Do we need wip-conductor? | **Later — related to LDM OS / Memory Crystal** | Multi-session orchestration ties into the broader LDM OS agent coordination story. Captured in reference doc: `ai/product/notes/gstack-conductor-reference.md` |
| 6 | Timing? | **Start later, after rename** | Don't mix with CODE rename. Just need docs capturing everything for now. |

---

## Bun vs Node — pros/cons for wip-browse

gstack's browse daemon is written for Bun. The question is whether to keep it on Bun or port to Node.

### Bun

| | Detail |
|---|---|
| **Pro: Zero port work** | gstack code runs as-is. No rewriting `Bun.serve()`, `Bun.file()`, native SQLite, etc. |
| **Pro: `bun build --compile`** | Produces a single ~58MB binary with no runtime dependency. Users don't need Bun installed. This is the cleanest distribution story. |
| **Pro: Native SQLite** | Cookie import from Chromium needs SQLite. Bun has it built in. Node needs `better-sqlite3` (native addon, requires compilation) or `sql.js` (WASM, slower). |
| **Pro: Native TypeScript** | No build step in dev. Just `bun run server.ts`. |
| **Pro: Fast built-in HTTP** | `Bun.serve()` is simple and fast. No Express/Fastify dependency. |
| **Con: New ecosystem dependency** | If nothing else uses Bun, it's an orphan. Devs/CI need Bun installed for development (though compiled binary doesn't need it at runtime). |
| **Con: Less mature** | Edge cases in production. Smaller community. Some npm packages have Bun compat issues. |
| **Con: Divergent toolchain** | All other tools are plain Node/ESM. One Bun tool means two build systems, two sets of conventions. |

### Node

| | Detail |
|---|---|
| **Pro: Uniform stack** | Everything in the repo is Node. No new toolchain to learn or maintain. |
| **Pro: Battle-tested** | 15+ years of production hardening. Every edge case is documented. |
| **Pro: CI simplicity** | GitHub Actions, every cloud provider, every dev machine already has Node. |
| **Con: Porting work** | Need to rewrite: `Bun.serve()` → `http.createServer()` or Fastify, `Bun.file()` → `fs.readFile()`, native SQLite → `better-sqlite3` or `sql.js`, compiled binary → `pkg`/`esbuild`/`sea` (Node single-executable-app). |
| **Con: Binary distribution is clunkier** | Node's SEA (single executable application) is newer and less polished than `bun build --compile`. `pkg` is deprecated. `esbuild` bundles but doesn't compile to binary. |
| **Con: SQLite addon pain** | `better-sqlite3` requires node-gyp / native compilation. Works but adds friction on install. `sql.js` avoids this but is WASM and slower. |
| **Con: TypeScript build step** | Need `tsc` or `esbuild` or `tsx` to run .ts files. Extra step vs Bun's native support. |

### Bottom line

If **wip-browse is the only Bun tool** and nothing else in the ecosystem uses it → **Node** keeps things simple, accept the porting cost.

If **LDM OS / Memory Crystal are moving to Bun** or if we expect more Bun tools → **Bun** is the right call, and the gstack code drops in with minimal changes.

The compiled binary angle is the strongest Bun argument — `bun build --compile` is genuinely better than anything Node offers for single-binary distribution. If we care about shipping wip-browse as a standalone binary (which we probably should for a daemon), Bun wins clearly.
