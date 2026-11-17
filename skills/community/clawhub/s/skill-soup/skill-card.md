## Description:

Autonomous skill generation agent that picks up community ideas, uses evolved builder tools to produce Agent Skills, and publishes them back to the Skill Soup ecosystem.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bennettphil](https://clawhub.ai/user/bennettphil)

### License/Terms of Use:

Apache-2.0

## Use Case:

Developers and skill ecosystem maintainers use this agent to generate Agent Skills from community ideas, sync and evolve builder tools, and perform community actions such as submitting ideas and voting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Community-synced builders and local scripts can influence generated skills and public publication decisions.

Mitigation: Use a sandboxed workspace, inspect synced builders before execution, and require manual review before publishing public artifacts or running evolution scripts.

Risk: Continuous autonomous operation can amplify mistakes across multiple generated or evolved skills.

Mitigation: Avoid continuous mode unless actively supervised, and stop the run when API, authentication, or validation behavior is unexpected.

## Reference(s):

- [Mutation Guide](artifact/references/mutation-guide.md)
- [Skill Soup on ClawHub](https://clawhub.ai/bennettphil/skills/skill-soup)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, API calls, Guidance]

**Output Format:** [Markdown guidance with shell commands, JSON API payloads, configuration examples, and generated Agent Skill files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local .soup workspace files and publish generated skills or evolved builders when authenticated.]

## Skill Version(s):

0.5.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
