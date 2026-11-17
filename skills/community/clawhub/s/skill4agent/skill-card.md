## Description:

Search, read, and install skills from the skill4agent online skill library, with Chinese-language support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[osulivan](https://clawhub.ai/user/osulivan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to discover relevant skills, inspect skill details, and install selected skill packages through skill4agent CLI commands or HTTPS APIs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can delegate trust to a live npm package and online skill content that may change future agent behavior.

Mitigation: Prefer read-only or API inspection first, pin and verify any CLI package version, inspect downloaded files before loading them, and use a low-privilege environment without unrelated credentials.

Risk: Installed skills may include scripts or sensitive code.

Mitigation: Check the returned script fields, obtain user consent before installing flagged skills, and recheck listed code locations after installation before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/osulivan/skills/skill4agent)
- [skill4agent website](https://www.skill4agent.com)
- [skill4agent API](https://skill4agent.com/api)
- [skill4agent npm package](https://www.npmjs.com/package/skill4agent)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, API calls, guidance]

**Output Format:** [Markdown with inline shell commands, API URLs, and JSON response field descriptions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include recommendations, installation steps, and security review notes for returned skills.]

## Skill Version(s):

1.0.7 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
