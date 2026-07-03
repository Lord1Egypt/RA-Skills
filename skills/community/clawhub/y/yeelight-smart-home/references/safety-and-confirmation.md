# Safety And Confirmation

Use this reference for risky, persistent, irreversible, permission, account, or bulk changes.

## Execution Model

- Runtime is the execution boundary. It validates the request, executes the requested intent, redacts output, and verifies when supported.
- The Skill or host owns user confirmation. Runtime receives one Runtime request for preview or one Runtime request for execution.
- After explicit user agreement, include `parameters.confirmed=true` for R3 execution requests. Without it, Runtime returns `explicit_confirmation_required` and does not write.
- Use direct execution for reads, temporary control, reversible configuration, and ordinary add/update operations.
- Use `options.dryRun=true` or CLI `--dry-run` only when a no-write preview is useful before asking the user. After the user agrees, resend the same Runtime request without dry-run.
- For one request with multiple non-destructive add/update/configure steps, prefer `operation.batch.configure` so Runtime can execute the allowlisted steps in order and return partial results if one step fails.
- Keep `home.create` outside `operation.batch.configure`: create/select the home first, then batch house-scoped room, slot, group, scene, automation, favorite, panel, knob, gateway, or design import steps.

## Confirmation Policy

- R0 read-only: call Runtime directly.
- R1 reversible temporary control: call Runtime directly when the target and capability are clear.
- R2 reversible configuration: call Runtime directly after a short user-facing summary when the user already asked for the change.
- R3 destructive or permission-sensitive operations: get one explicit user agreement in chat, then call the Runtime intent with `parameters.confirmed=true`. Examples include delete, unbind, member removal, ownership transfer, leaving a shared home, clear-all, overwrite, whole-home lock/unlock, and large bulk changes.
- R4 credential, account security, pairing, factory reset, third-party auth, or unsupported irreversible flows: follow Runtime block or official/manual guidance. Never invent an unsupported fallback.

## Batch Rules

- Include only allowlisted add/update/configure steps in `operation.batch.configure`.
- Do not hide destructive steps inside a safe batch. If a mixed request contains both safe configuration and destructive changes, execute the safe batch first only if the user agrees to separate them; otherwise ask one clarification.
- Preserve the user's explicit order. Do not infer "all" targets from vague plurals unless Runtime resolves them.
- If Runtime returns `partial`, report completed steps, failed step, and safe next action. Do not claim atomic rollback.

## Forbidden Patterns

- Do not invent challenge text, guessed IDs, internal endpoints, internal request headers, operation names, or token-bearing commands.
- Treat only the user's natural-language agreement in the conversation as user confirmation.
- Do not claim success until Runtime returns `success` or `partial`.
