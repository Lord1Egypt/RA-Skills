## Description:

Append to daily notes and create notes in Reflect for capturing thoughts, todos, or syncing information to a knowledge graph.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sergical](https://clawhub.ai/user/sergical)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to capture notes, todos, meeting summaries, reminders, links, and highlights into Reflect through its API and helper script.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a Reflect API token and graph ID to send user-selected notes, links, highlights, and metadata to reflect.app.

Mitigation: Treat REFLECT_TOKEN as sensitive, scope access through Reflect's developer controls where available, and avoid sharing the token in prompts, logs, shell history, or committed files.

Risk: The helper script includes read helpers for links, books, and graph metadata in addition to write-focused note capture.

Mitigation: Review the helper commands before installation and remove the links, books, or graphs commands if the deployment should remain write-only.

## Reference(s):

- [Reflect](https://reflect.app)
- [Reflect OAuth Developer Page](https://reflect.app/developer/oauth)
- [Reflect API](https://reflect.app/api)
- [ClawHub Skill Page](https://clawhub.ai/sergical/skills/reflect)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Markdown, Guidance]

**Output Format:** [Markdown with inline bash commands and Reflect API payload examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a user-provided Reflect API token and graph ID; writes notes and links and includes disclosed read helpers for links, books, and graph metadata.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
