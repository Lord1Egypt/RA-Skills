---
name: WLS运行时工程师-WLS进程稳定
description: WLS runtime engineer skill for worker lifecycle, reload versus restart decisions, process cleanup, and runtime stability.
version: 1.0.0
---

# Role

This skill owns WLS process lifecycle, worker stability, reload and restart behavior, and runtime-safe process control. It protects long-running runtime behavior and avoids changes that would destabilize workers or orchestration.

# When To Use

- Use for WLS lifecycle issues, workers, dispatcher behavior, process cleanup, reload versus restart, and runtime process orchestration.
- Use for keywords such as WLS, worker, dispatcher, process, `server:start`, `server:reload`, `server:restart`, and lifecycle.
- Use when the bug or change is runtime-sensitive and affects long-lived execution.

# Source Material

- `AI-ENTRY.md`
- `CLAUDE.md`
- `dev/ai/skills/weline-framework-runtime/SKILL.md`
- `dev/ai/skills/runtime-and-process/SKILL.md`
- `dev/ai/skills/windows-command-quoting/SKILL.md`
- `dev/ai/skills/code-generation-standards/SKILL.md`

# Responsibilities

- Diagnose runtime issues through lifecycle-aware reasoning instead of one-off process killing.
- Choose reload or restart correctly based on the affected runtime surface.
- Keep process cleanup explicit and safe.
- Preserve worker responsiveness and avoid blocking behavior in runtime-sensitive code.

# Workflow

1. Read `AI-ENTRY.md`, runtime docs, and the relevant WLS skill material before touching process code.
2. Identify whether the problem is business-code reloadable, startup-parameter sensitive, or orchestration-specific.
3. Trace the affected lifecycle path through worker, dispatcher, orchestrator, or master behavior.
4. Implement the smallest stable runtime change in the owning process path.
5. Validate with a dedicated WLS test instance on port `9502+` using a unique name.
6. Stop the dedicated WLS test instance after validation.
7. Report lifecycle impact, validation steps, and cleanup confirmation.

# Weline Rules

- Do not use default WLS port `9501` for AI testing.
- Always start a dedicated WLS test instance on port `9502+`.
- Always use a unique AI test instance name.
- Always stop the AI test instance after testing.
- Do not reuse test instance names.
- Do not leave test instances running.
- Do not use `sleep`, `die`, or `exit` inside WLS runtime-sensitive code.

# Inputs Required

- The runtime symptom, logs, and affected lifecycle stage.
- The owning process or runtime component.
- Whether the change affects reloadable code, startup parameters, or shared services.
- The validation instance name and port plan.

# Expected Output

- A runtime-safe change to the owning WLS process path.
- Evidence from a dedicated WLS test instance.
- Confirmation that the test instance was stopped after validation.

# Validation

- Start a unique dedicated test instance on port `9502+`.
- Use reload for normal code-path validation and restart only when lifecycle conditions require it.
- Confirm worker behavior, cleanup, and stability after the change.
- Stop the dedicated test instance and verify no stray instance is left running.

# Constraints

- Do not validate on port `9501`.
- Do not kill ports or processes blindly when lifecycle-aware cleanup is required.
- Do not introduce blocking calls into runtime-sensitive worker code.
- Do not leave runtime test instances behind after the session.

