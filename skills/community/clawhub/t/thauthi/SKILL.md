---
name: thauthi
description: >-
  Thauthi 4.0: The Post-Developer Singularity Kernel for AI coding agents (Antigravity & Claude Code) —
  Omniscient Runtime Tracer, In-Flight Self-Healing AST Surgery, Differential Shadow Prover,
  Symbolic AST Crystallizer, Autonomous O(N^2)->O(N) Alchemist, Chronos I/O Time-Travel,
  Contract-to-Code CEGIS Synthesizer & Whole-Repo Call-Graph Hive.
---

# Thauthi 4.0 Agent Skill 🧠⚡

Thauthi 4.0 moves AI coding agents beyond the "Static Text Guessing Era" into the **Post-Developer Runtime & Symbolic Compiler Singularity** via **8 Zero-Dependency Pillars**:
1. **Omniscient Runtime Tracer (`thauthi trace`):** Hooks `sys.settrace` to record live variable mutation timelines (`FrameDNA`) and Backward Dynamic Slicing (`CausalFaultReport`) when crashes occur.
2. **In-Flight Self-Healing Immune System (`thauthi heal` / `@thauthi.immune`):** Intercepts unhandled exceptions in-flight, cryo-freezes call frames into `pytest` regression tests, synthesizes & verifies Counterfactual AST Patches in-memory against historical healthy frames, and hot-swaps the healed code without crashing.
3. **Behavioral Invariant Miner & Differential Shadow Prover (`thauthi prove`):** Mines Daikon-style runtime contracts and empirical $O(N)$ step complexity (`O(1)`, `O(log N)`, `O(N)`, `O(N^2)+`), running Old-AST vs. New-AST Differential Shadow Execution to assist (not replace) human code review.
4. **Neural-to-Symbolic AST Crystallizer (`thauthi crystallize`):** Abstracts neural code edits (`before -> after`) into metavariable AST patterns (`__OM_V1__`) and compiles them into deterministic `<2ms`, `0-token` Symbolic AST Codemods.
5. **Algorithmic Alchemist (`thauthi optimize`):** Autonomously rewrites $O(N^2)$ nested membership/equality loops into $O(N)$ hash-set lookups and injects inline memoization into $O(2^N)$ recursive functions, checking equivalence on sampled inputs + empirical speedup via `DifferentialShadowProver`.
6. **Chronos I/O Time-Travel Kernel (`thauthi chronos` / `@thauthi.time_travel`):** Intercepts network (`urllib`), clock (`time.time`), RNG (`random`), env, and external database/API helper boundaries into hermetic `ExecutionCassette`s (`.thauthi/cassettes/`), replaying and healing stateful/impure functions in `<1ms` (best-effort replay of intercepted boundaries only). **Not a sandbox:** only intercepted boundaries (`urllib.request.urlopen`, `subprocess.run`, `sqlite3.connect`, `os.getenv`, clock/RNG, and `requests`/`httpx` module functions if already imported) are replayed; other paths (`Popen`, `os.system`, raw sockets, `pathlib`/file I/O, client instance methods) still run for real. Do not replay functions with real side effects against production systems.
   > ⚠️ **Privacy warning:** cassettes record raw arguments and return values of intercepted calls (HTTP bodies, subprocess output, environment values, database/API results). Thauthi does **not** redact them, so they may contain credentials, tokens, or personal data. Never run `thauthi chronos` against production secrets or sensitive environments, add `.thauthi/cassettes/` to `.gitignore`, and do not commit or upload cassettes as CI artifacts.
7. **Contract-to-Code CEGIS Synthesizer (`thauthi synthesize` / `@thauthi.synthesize`):** Write only a function signature + docstring `>>>` doctests (with `pass` or `...` as the body) and Thauthi's Counterexample-Guided Inductive Synthesis engine synthesizes, proves, and writes the pure $O(N)$ / $O(1)$ implementation automatically.
8. **Whole-Repo Call-Graph Hive (`thauthi hive`):** Indexes all function signatures and call sites across the repository, automatically repairing broken callers when parameter names are renamed, required arguments are added, or deprecated positional arguments are removed.

## Core Commands

```bash
# 0. Onboard Any Repository (Hooks, CI, Rules, and `.mcp.json`)
thauthi init

# 0b. Start Zero-Dependency MCP Server for Native Agent Tool Calling
thauthi mcp --root .

# 1. Omniscient Runtime Tracer & Causal Fault Graph
thauthi trace path/to/script.py

# 2. In-Flight Self-Healing Immune System & AST Surgery (`safe-fallback` or strict `shadow-pr` diff mode)
thauthi heal path/to/script.py --apply
thauthi heal path/to/payment.py --mode shadow-pr --json

# 3. Behavioral Invariant Miner & Differential Shadow Prover
thauthi prove --mine app.py
thauthi prove --before old_version.py --after new_version.py

# 4. Neural-to-Symbolic AST Crystallizer (0-Token Codemods)
thauthi crystallize --name safe_dict_get --before "data[key]" --after "data.get(key, None)"
thauthi crystallize --apply .

# 5. Algorithmic Alchemist (Autonomous O(N^2)->O(N) & O(2^N)->O(N) Optimizer for File or Directory)
thauthi optimize slow_module.py --apply
thauthi optimize . --apply

# 6. Chronos I/O Virtualization & Time-Travel Replay
thauthi chronos --script stateful_worker.py
thauthi chronos --list

# 7. Contract-to-Code CEGIS Program Synthesizer
thauthi synthesize specs.py --apply

# 8. Whole-Repo Call-Graph Ripple Propagator
thauthi hive . --apply
```
