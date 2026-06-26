# Session note: max-turns must not be raised; split tasks and use fixed validation scripts

## Context

The user corrected the proposed mitigation for repeated Claude Code `error_max_turns` interruptions and long-running tasks. The user explicitly required:

1. Do not adjust/increase `max-turns`.
2. Split all tasks into the smallest practical units.
3. Use fixed validation scripts.
4. Do not enable the proposed "禁止重新探索" / no-re-exploration rule for now.
5. Apply the other recommendations, especially avoiding long-running tasks; the previous final task exceeded 50 minutes and must not repeat.
6. Keep the Claude interactive session / tmux option for multi-step coordination, but use it to supervise a sequence of small tasks, not to create one large long-running task.
7. Stability is more important than speed: do not use concurrency for xz01 template execution unless the user explicitly re-enables it.

## Durable workflow rules

- Keep Claude Code `--max-turns` at the current/default task-appropriate value; do not solve interruptions by increasing it.
- Main must split work into minimum independent units. A dev task should normally address exactly one page, one component, or one defect class.
- Do not bundle development, broad exploration, screenshots, AI visual analysis, packaging, and rule review into one dev task.
- Dev tasks should be time-boxed. If a task risks running long, split it before dispatch. Prefer small `terminal(... timeout=...)` limits over one long 50+ minute run.
- For a batch of many related small fixes, use Claude interactive session / tmux as a supervised workbench to preserve context and avoid repeated startup/resume overhead. Each tmux prompt must still be a minimum-unit task with a clear stop point; do not let tmux become a 50+ minute monolithic run.
- Do not run xz01 work concurrently. Use a single serial queue: one dev task, then one test task, then one rule review, then proceed to the next item. tmux may be used as a single dev session container, not as multiple parallel dev sessions.
- Validation must use deterministic fixed scripts where possible instead of making each test agent invent new shell snippets.
- The proposed "禁止重新探索" rule is explicitly not active for now. Do not add it to prompts as a hard rule unless the user later enables it.

## Fixed validation scripts

Created under:

```text
/root/.hermes/workspace/xz01-factory/tools/
```

Scripts:

```text
xz01-backend-baseline-check.sh   # verify PHP/backend/controller/config baseline
xz01-theme-diff-check.sh         # verify live theme and generated theme are identical
xz01-runtime-clear.sh            # clear runtime and verify empty
xz01-quick-http-gate.py          # quick HTTP/content gate for core PC/mobile URLs
```

Use these in test/rule validation before writing ad-hoc checks.

## Dispatch template

For each dev task:

```text
You are xz01 dev. Fix only: <single defect>.
Allowed paths: /www/wwwroot/www.900az.com/public/themes/default/** and generated counterpart only.
Forbidden: application/**/*.php, config/**/*.php, route/**/*.php, thinkphp/**/*.php, vendor/**/*.php.
Do not package. Do not screenshot. Do not run broad regression.
After edit: sync generated, clear runtime, run fixed baseline/diff checks, and give a short self-check.
```

Then test runs fixed scripts plus targeted screenshot/AI visual review.