## Description:

Visual troubleshooting and screen-aware user guidance for screenshots, terminal output, app settings, installer failures, and confusing web/app flows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[m-lwatcher](https://clawhub.ai/user/m-lwatcher)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to interpret screenshots, terminal errors, app settings, installer failures, and confusing web or app flows, then receive one to three concrete next actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may lead an agent to inspect screenshots, browser state, local files, or command output when directly relevant to troubleshooting.

Mitigation: Avoid sharing sensitive screens or logs unless needed, and ask before destructive, privacy-sensitive, or irreversible actions.

Risk: Blurry, partial, or cropped screenshots can make the guidance uncertain.

Mitigation: State what is visible, what cannot be confirmed, and request the single most useful missing detail before giving high-confidence instructions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/m-lwatcher/skills/quirky-help)
- [Response Patterns](artifact/references/response-patterns.md)
- [Triage Guide](artifact/references/triage.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown or concise plain text with optional inline commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Action-first troubleshooting guidance, typically limited to the visible issue, likely cause, and one to three next actions.]

## Skill Version(s):

1.0.0 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
