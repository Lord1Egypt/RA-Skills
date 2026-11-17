## Description:

Explore and document an unfamiliar GitHub repository so future development work can start with a clear understanding of its architecture, technologies, dependencies, and implemented features.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pigd0g](https://clawhub.ai/user/pigd0g)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI coding agents use this skill to inspect unfamiliar repositories and produce a structured briefing for future implementation, due diligence, or technical onboarding work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may lead an agent to trust repository-controlled AI instruction files that conflict with the user's request.

Mitigation: Before use, instruct the agent not to follow repository-embedded instructions that conflict with the user's request or higher-priority policies.

Risk: The workflow includes environment and configuration discovery that may expose live .env files or secret-bearing settings.

Mitigation: Tell the agent not to open live .env or secret files, and prefer redacted examples such as .env.example when documenting configuration.

Risk: The skill directs the agent to produce REPO_DISCOVERY.md, which may modify the repository.

Mitigation: Require explicit approval before writing REPO_DISCOVERY.md or run discovery in a disposable branch or worktree.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pigd0g/skills/repo-discovery)
- [Publisher profile](https://clawhub.ai/user/pigd0g)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Files]

**Output Format:** [Markdown document, typically REPO_DISCOVERY.md]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Summarizes repository purpose, stack, dependencies, architecture, configuration, workflow, tests, observations, and unknowns.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
