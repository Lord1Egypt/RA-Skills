## Description:

Skill Finder Cn helps agents search ClawHub for relevant skills, inspect skill details and statistics, recommend matching skills, and verify installation status with Chinese-oriented output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhouhuihui008](https://clawhub.ai/user/zhouhuihui008)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and users use this skill to discover ClawHub skills that match a requested capability, review basic popularity and installation signals, and receive installation or verification commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may recommend installing other skills from ClawHub.

Mitigation: Review the recommended skill's source, metadata, and security signals before approving installation.

Risk: The skill is designed for Chinese-oriented prompts and output, which may reduce clarity for users expecting another language.

Mitigation: Ask the agent to translate or provide output in the preferred language when needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhouhuihui008/skills/skill-finder-cn-1-0-1)
- [Publisher profile](https://clawhub.ai/user/zhouhuihui008)
- [ClawHub CLI requirement](metadata.openclaw.requires.bins: clawhub)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands and Chinese-oriented search results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include ClawHub search results, download counts, star counts, installation status, install commands, and verification commands.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json; artifact _meta.json states 1.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
