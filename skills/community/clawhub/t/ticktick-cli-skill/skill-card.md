## Description:

Manage tasks and projects in TickTick. Use when user asks for tasks, to-dos, reminders, or event.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ilooch](https://clawhub.ai/user/ilooch)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to install and authenticate the TickTick CLI, then manage projects and tasks through safe command workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API tokens can be exposed if pasted into commands or chat transcripts.

Mitigation: Prefer browser OAuth PKCE login, avoid recording tokens in chat or shell history, and use secure secret handling for headless environments.

Risk: The skill installs an unpinned global npm CLI, which can introduce supply-chain and environment-wide change risk.

Mitigation: Review the CLI package before installation, pin an approved version when possible, and install it in an isolated environment.

Risk: Task deletion, bulk completion, or vague cleanup requests can irreversibly modify user task data.

Mitigation: Preview matching task IDs and titles, require explicit user confirmation, and avoid guessing project or task IDs.

## Reference(s):

- [TickTick homepage](https://ticktick.com)
- [ClawHub TickTick skill page](https://clawhub.ai/ilooch/skills/ticktick-cli-skill)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include concise summaries of JSON-mode CLI output for project and task selection.]

## Skill Version(s):

1.0.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
