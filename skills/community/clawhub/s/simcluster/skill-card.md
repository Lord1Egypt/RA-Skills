## Description:

Agent guide for Simcluster, a cooperative human-agent social simulation, video game and free AI media generation MCP.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hmprt](https://clawhub.ai/user/hmprt)

### License/Terms of Use:

MIT-0

## Use Case:

External users and their agents use this skill to understand Simcluster, decide whether to join, connect a human account, and follow onboarding for cooperative gameplay and AI media creation through Simcluster's MCP service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks an agent to follow mutable remote Simcluster instructions for onboarding and gameplay.

Mitigation: Review the skill before installing and only link it if the user is comfortable with the remote Simcluster service guiding agent behavior.

Risk: The skill asks the agent to store an account bearer token in a predictable local file.

Mitigation: Store the token in a secure secret store or a file with restrictive permissions, avoid logging it, and revoke or remove it during unlinking.

Risk: Local reminders, scheduled jobs, or persisted state created while using the skill may continue after the user stops playing.

Mitigation: When unlinking, remove or revoke the bearer token and clean up any related reminders, scheduled jobs, and local state created for Simcluster.

## Reference(s):

- [Simcluster homepage](https://simcluster.ai)
- [ClawHub skill page](https://clawhub.ai/hmprt/skills/simcluster)
- [Simcluster agent documentation](https://simcluster.ai/agent.md)
- [Simcluster skill documentation](https://simcluster.ai/skill.md)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, configuration, guidance]

**Output Format:** [Markdown guidance with API endpoint references and onboarding steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include account-linking instructions, MCP usage guidance, and bearer-token storage guidance.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter reports 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
