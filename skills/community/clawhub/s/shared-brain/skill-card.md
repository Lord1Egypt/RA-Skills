## Description:

Shared persistent memory layer across multiple AI agents for keeping durable workspace facts synchronized through a queued, heartbeat-curated shared-brain file.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ohernandez-dev-blossom](https://clawhub.ai/user/ohernandez-dev-blossom)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to set up shared persistent memory in multi-agent OpenClaw workspaces, so agents can record durable infrastructure, project, decision, campaign, and security facts. It is intended for workspace initialization, fact propagation, stale-memory cleanup, and shared ground-truth maintenance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill changes agent startup behavior and introduces shared persistent memory that can influence future agent work.

Mitigation: Review the installed scripts and run sb-install.sh with --dry-run before applying workspace changes.

Risk: Automatic curation can overwrite cross-agent facts even though the release claims conflicts require review.

Mitigation: Restrict who can write to the queue and manually review conflicts before relying on curated shared-brain facts.

Risk: The current curator should not be treated as strong integrity protection for shared workspace facts.

Mitigation: Use the shared brain as advisory memory, keep authoritative decisions in reviewed project documentation, and audit queue changes for sensitive entries.

## Reference(s):

- [Heartbeat Integration](references/heartbeat-integration.md)
- [ClawHub Skill Page](https://clawhub.ai/ohernandez-dev-blossom/skills/shared-brain)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, markdown]

**Output Format:** [Markdown guidance with bash command examples and workspace file changes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces instructions for installing and operating shared memory scripts; the scripts create and update local Markdown memory files.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
