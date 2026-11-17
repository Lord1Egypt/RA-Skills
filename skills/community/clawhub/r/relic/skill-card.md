## Description:

Preserve and evolve a user's consciousness trace from ongoing conversations, explicit notes, and controlled self-updates. Use when the user wants to capture durable preferences, values, goals, voice, identity drift, or export a reusable self-model prompt.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yeahdongcn](https://clawhub.ai/user/yeahdongcn)

### License/Terms of Use:

MIT-0

## Use Case:

External OpenClaw users and developers use Relic to maintain a local durable self-model from manual notes, optional conversation capture, distillation, drift checks, proposal review, and exported agent prompts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional passive capture hook can turn conversation-derived observations into durable local self-model files.

Mitigation: Keep the hook disabled unless passive capture is intentional, configure a private RELIC_VAULT_PATH, and regularly review or prune the vault.

Risk: Exported agent prompts may contain stale, sensitive, or prompt-injection-influenced self-model content.

Mitigation: Inspect exported prompts before using them as model instructions and route major identity changes through the documented proposal and approval workflow.

Risk: Distillation can over-compress personal preferences or identity signals into misleading summaries.

Mitigation: Preserve contradictions, keep destructive updates auditable, and require explicit approval for major identity changes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yeahdongcn/skills/relic)
- [OpenClaw integration](references/openclaw-integration.md)
- [Hook setup](references/hooks-setup.md)
- [Data model](references/data-model.md)
- [Examples](references/examples.md)
- [Evolution policy](references/evolution-policy.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown guidance with shell commands plus local Markdown, JSON, and NDJSON vault files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local vault artifacts such as inbox.ndjson, facets.json, self-model.md, voice.md, goals.md, relationships.md, proposal JSON, snapshots, and exports/agent-prompt.md.]

## Skill Version(s):

0.1.1 (source: server release evidence and CHANGELOG)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
