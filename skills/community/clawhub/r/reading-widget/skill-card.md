## Description:

Reading Widget Clawhub helps an agent install and maintain a macOS desktop widget that displays WeRead reading streaks, reading time, goal progress, current-book progress, yearly totals, and a rotating quote.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tinadu-ai](https://clawhub.ai/user/tinadu-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External ClawHub users and agent operators use this skill to set up a macOS reading dashboard backed by a WeRead Agent API key. The skill guides installation, opening, customization, troubleshooting, optional startup persistence, and removal of the local widget files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a WeRead API key and can read it from agent settings or local configuration.

Mitigation: Prefer providing WEREAD_API_KEY through a controlled environment or dedicated secret store, and avoid adding an api_key field to config.json.

Risk: The optional LaunchAgent creates a long-running background helper on the user's machine.

Mitigation: Enable the LaunchAgent only after explicit user consent, and unload it when the widget is no longer needed.

Risk: The local helper serves content on localhost and exposes a goal-update endpoint with weak controls.

Mitigation: Review before installing; for broader use, harden the helper to serve only the widget page and require a per-install token for /set-goal.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tinadu-ai/skills/reading-widget)
- [WeRead official skill package](https://cdn.weread.qq.com/skills/weread-skills.zip)
- [Ubersicht](http://tracesof.net/uebersicht/)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Code]

**Output Format:** [Markdown instructions with shell commands, configuration snippets, and file-editing guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides creation and operation of local widget files; normal output is human-readable agent guidance rather than a structured API response.]

## Skill Version(s):

1.1.1 (source: server release and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
