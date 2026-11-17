## Description:

Self-reflection skill that helps an agent record mistakes, lessons, feature requests, reusable snippets, and daily memory in local Markdown files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lanlan314](https://clawhub.ai/user/lanlan314)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and developers use this skill to keep structured self-review records after completed tasks, user-corrected errors, repeated mistakes, newly learned practices, and feature requests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persist conversation-derived notes and daily memory as local Markdown files.

Mitigation: Install only when local reflection storage is desired, and review generated memory and reflection files for sensitive content.

Risk: The optional scheduling setup can install a recurring macOS task.

Mitigation: Review or disable scheduling before use, and avoid running --setup unless recurring execution is intentional.

Risk: Scheduled scripts can write logs under /tmp.

Mitigation: Consider changing log paths to a private user-owned log directory before enabling scheduled runs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lanlan314/skills/self-reflection-lan)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown files with text guidance and optional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes local memory and reflection files; optional setup can configure recurring local execution.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
