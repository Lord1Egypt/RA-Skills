## Description:

Combines cognitive-memory, memory-tiering, context-compactor, and memory-on-demand into a unified, auto-compacting memory system with semantic recall.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tech-immortales-design](https://clawhub.ai/user/tech-immortales-design)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to coordinate memory compaction, tiered storage, semantic recall, and token-aware context handling in OpenClaw environments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic persistent memory may retain conversation-derived information for long periods.

Mitigation: Review retention settings before enabling the skill and confirm that the underlying memory skills support review and deletion.

Risk: Secrets or highly sensitive personal data could be stored if they appear in memory-managed conversations.

Mitigation: Avoid storing secrets or highly sensitive personal data unless the deployment environment has appropriate controls and deletion workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tech-immortales-design/skills/superlative-memory-manager)

## Skill Output:

**Output Type(s):** [guidance, configuration, shell commands]

**Output Format:** [Markdown with JSON configuration and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces memory-management guidance for an agent; persistent storage behavior depends on the required underlying memory skills.]

## Skill Version(s):

1.0.0 (source: evidence.release.version and openclaw.plugin.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
