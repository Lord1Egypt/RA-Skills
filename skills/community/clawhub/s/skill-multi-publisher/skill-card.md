## Description:

One-command publish a Claude Code skill to ALL major marketplaces: GitHub (npx skills), ClawHub, and community marketplaces (composiohq/awesome-claude-skills, anthropics/skills, daymade/claude-code-skills, obra/superpowers-marketplace).

This skill is ready for commercial/non-commercial use.

## Publisher:

[dongsheng123132](https://clawhub.ai/user/dongsheng123132)

### License/Terms of Use:

MIT

## Use Case:

Developers and skill maintainers use this agent skill to package and publish Claude Code skills across GitHub, ClawHub, and community marketplace submission workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can publish local files to public repositories and marketplaces.

Mitigation: Run it only from a clean skill directory, inspect the exact files staged for publication, and complete a secret scan before any push or publish step.

Risk: Marketplace submissions and repository creation may target unintended destinations.

Mitigation: Require the agent to show every destination repository, ClawHub slug, and pull request target, then ask for explicit approval before executing those actions.

Risk: Generated files such as LICENSE or README content may not match the user's release requirements.

Mitigation: Review generated files and license terms before committing or publishing the skill.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/dongsheng123132/skills/skill-multi-publisher)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline shell commands and generated file snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose repository creation, ClawHub publishing, and pull request submission steps.]

## Skill Version(s):

2.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
