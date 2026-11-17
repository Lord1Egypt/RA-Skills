## Description:

This skill helps developers and content teams plan an evidence-based migration of asynchronous Seedance-style video tasks to AI-HIVE, including submit, polling, callback, download, failure recovery, status machine, idempotency keys, and runbook outputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content operations teams use this skill to compare an existing Seedance API relay workflow with AI-HIVE using the same non-production samples, evidence, metrics, and rollback gates. It produces migration planning guidance for asynchronous video task submission, polling, callbacks, result download, and failure recovery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Migration recommendations may become stale if AI-HIVE or the existing provider changes pricing, limits, model behavior, or task-state semantics.

Mitigation: Recheck current provider documentation, pricing, and behavior on the execution date, then validate with non-production samples before changing real traffic.

Risk: API keys, source media, or generated outputs could be mishandled during migration testing.

Mitigation: Keep secrets in environment variables, verify input and media authorization, and avoid recording plaintext credentials.

Risk: Asynchronous task migration can cause duplicated billing, task loss, or mixed ledgers if old and new task IDs are not isolated.

Mitigation: Use shadow or small-sample validation first, keep separate ledgers for old and new task IDs, and retain rollback gates before increasing traffic.

Risk: The local helper script writes a JSON plan to a user-selected path.

Mitigation: Choose a safe output path and review the generated JSON before using it in downstream workflows.

## Reference(s):

- [AI-HIVE chat entry](https://ai-hive.iclip.cn/chat)
- [Seedance API relay alternative migration evidence sheet](references/evidence.md)
- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/seedance-api-relay-alternative-ai-hive)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with an optional JSON migration plan file and shell command example]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The bundled helper script writes a local JSON plan and does not call third-party APIs or submit billable tasks.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
