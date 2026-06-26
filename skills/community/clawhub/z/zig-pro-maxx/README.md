<p align="center">
  <img src="assets/banner.svg" alt="zig-pro-maxx banner" width="100%">
</p>

<div align=center>

> Agent skill that enforces strict Zig 0.16.0 API compliance.
> Drop it in any repo; any agentskills-compatible agent will load it automatically.
</div>

---

## Structure

```
zig-pro-maxx/
├── SKILL.md                         ← entry point (agentskills format)
├── references/
|    ├── zig-0_16-breaking-changes.md
|    ├── allocators.md
|    ├── build-system.md
|    ├── code-discipline.md
|    ├── common-mistakes.md
|    ├── std-collections.md          ← ArrayList + HashMap (new)
|    ├── std-debug.md
|    ├── std-fmt.md                  ← bufPrint, allocPrint, parseInt (new)
|    ├── std-io.md
|    └── testing.md
└── examples/
     └── hello_from_cli_args.zig
```

## What it enforces

- `DebugAllocator` not `GeneralPurposeAllocator`
- `std.Io` (capital I) not `std.io`
- `std.ArrayList` is unmanaged in 0.16.0 — allocator passed per call
- No `async` / `await` — removed in 0.16.0
- No variable shadowing — compile error in 0.16.0
- Explicit `try` / `catch` on every fallible call
- `errdefer` over `defer` for conditional cleanup
- `bufPrint` over `allocPrint` in hot paths
- Correct format specifiers (compile-time enforced)

## Usage

Compatible with **Claude Code** and any agent that reads the agentskills format.

```sh
claude --skill zig-pro-maxx/SKILL.md
```

---

MIT

---

## Author

**Soumyajit Bala**

*Systems engineer. I build automation infrastructure, AI pipelines, and local-first tools.*

soumyajit@zelkyr.dev | https://github.com/debuggerdragon311

**Need a custom automation pipeline, AI integration, or data extraction system built?**
Reach out at [soumyajit@zelkyr.dev](mailto:soumyajit@zelkyr.dev)
