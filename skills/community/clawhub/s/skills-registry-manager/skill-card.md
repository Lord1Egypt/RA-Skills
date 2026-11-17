## Description:

Manages and installs Claude Code skills from local and subscribed registries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gavinyao](https://clawhub.ai/user/gavinyao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to list, subscribe to, and install Claude Code skills from registry YAML files. It supports local, git, and npx installation sources with dependency handling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Registry files can direct the agent to fetch mutable remote registries or install skills through npx, git, or local copy.

Mitigation: Review every registry URL and skill source before use, and prefer pinned, trusted versions or commits.

Risk: Installing entries from untrusted registries can change local or global agent behavior.

Mitigation: Prefer project-local installs for evaluation and avoid entries whose final source cannot be validated.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gavinyao/skills/skills-registry-manager)
- [Claude Code documentation](https://docs.anthropic.com/en/docs/claude-code)
- [Default awesome-skills registry](https://raw.githubusercontent.com/gavinyao/awesome-skills/main/registry.yaml)
- [registry.yaml](artifact/registry.yaml)
- [registry.example.yaml](artifact/registry.example.yaml)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown tables, prompts, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose local or global skill installation actions based on registry entries.]

## Skill Version(s):

1.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
