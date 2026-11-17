## Description:

Helps agents search, read, and install skills from the skill4agent online skill library, with Chinese-language support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[osulivan](https://clawhub.ai/user/osulivan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to discover relevant online skills, inspect skill details, and install selected skills through the skill4agent CLI or HTTPS API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mutable npm execution and remote downloads can change behavior between reviews.

Mitigation: Use a pinned, reviewed skill4agent CLI version and inspect downloaded skills before activation.

Risk: Installer workflows may be run in projects or shells that expose sensitive credentials.

Mitigation: Run search, read, and install commands from a low-privilege environment without sensitive credentials or private project files.

Risk: The skill depends on the skill4agent online service and downloaded third-party skill content.

Mitigation: Review returned skill metadata, script safety fields, and downloaded files before recommending or activating an installed skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/osulivan/skills/skill4agent-cn)
- [Publisher profile](https://clawhub.ai/user/osulivan)
- [skill4agent website](https://www.skill4agent.com)
- [skill4agent npm package](https://www.npmjs.com/package/skill4agent)
- [skill4agent API](https://skill4agent.com/api)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and API URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference JSON responses from skill4agent search/read APIs; installation can create local skill files when executed.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
