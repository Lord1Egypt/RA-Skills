# Code pack
Layer 1 (always): build, type check, lint, unit tests (new behavior needs a test that fails without the change), dependency/security scan.
Layer 1 for web apps: drive key paths with Playwright (wait for networkidle, inspect DOM, then act); assert no console errors; save screenshots as evidence. Write big accessibility snapshots to files instead of putting them in context.
Fix loop: feed structured failures (file, line, message) back; max 3 retries.
Judge dimensions (one subagent each): correctness and edge cases; error handling; security; tests actually assert behavior (not just that code runs); simplification opportunities; project conventions (CLAUDE.md / AGENTS.md).
Score confidence and severity separately; report only confidence >= 80 for PR comments.

Behavioral probes (when tests are weak or missing): write throwaway checks against the spec, not the implementation — boundaries (exactly n, n±1), limits/caps after long idle, time going backwards (inject a fake clock), invalid arguments, concurrency. A probe that fails is a blocker with its printed output as evidence. Also check the existing tests: an assertion-free or `is not None` test counts as no test.
