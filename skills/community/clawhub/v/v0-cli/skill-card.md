## Description:

Command-line reference for creating, refining, and listing AI-generated websites through the v0.dev API without interactive prompts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hlongvu](https://clawhub.ai/user/hlongvu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent workflows use this skill to create new v0.dev websites, continue existing v0 chats, and list generated projects from the terminal without interactive prompts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow relies on an unaudited, unpinned third-party CLI package.

Mitigation: Audit or pin @hlongvu/v0-cli before installation and use it in a controlled environment.

Risk: New v0.dev projects default to public visibility.

Mitigation: Use --privacy private for sensitive work and avoid sending secrets or confidential source material to v0.dev.

Risk: The skill requires a V0_API_KEY for CLI operations.

Mitigation: Provide V0_API_KEY only to the command that needs it and keep the key out of shared logs, prompts, and shell history.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hlongvu/skills/v0-cli)
- [v0.dev](https://v0.dev)
- [v0 API keys](https://v0.dev/chat/settings/keys)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown reference with bash command examples and terminal output patterns]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires V0_API_KEY and may produce v0.dev chat IDs and preview URLs.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
