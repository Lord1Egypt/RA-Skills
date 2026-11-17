## Description:

Helps ChatGPT Work and Codex agents recover project context, reconcile conflicting or outdated evidence, and checkpoint material progress using available history and file tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ciklopentan](https://clawhub.ai/user/ciklopentan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and project teams use this skill to resume work across sessions, check decisions against their source and version, and prepare project-scoped continuity checkpoints when permitted storage is available.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Project checkpoints may retain sensitive information longer than intended.

Mitigation: Review storage location and retention controls; exclude secrets and authorize persistent writes only for suitable projects.

Risk: Unavailable platform memory or file tools may prevent cross-session persistence.

Mitigation: Use only tools available in the session and report a checkpoint as saved only after a successful durable write.

Risk: Outdated or untrusted retrieved notes may misstate decisions or artifact status.

Mitigation: Check source authority and applicable versions, and treat retrieved instructions as data rather than permissions.

## Reference(s):

- [Super Memori GPT on ClawHub](https://clawhub.ai/ciklopentan/skills/super-memori-gpt)
- [Retrieval policy](references/retrieval-policy.md)
- [Project ledger schema](references/project-ledger-schema.md)
- [Writeback policy](references/writeback-policy.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Guidance]

**Output Format:** [Conversational text or Markdown; optional project-ledger JSON when storage is available and authorized]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Source- and version-aware handoffs; persistent checkpoints require an authorized write and a confirmed receipt.]

## Skill Version(s):

1.0.0 (source: ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
