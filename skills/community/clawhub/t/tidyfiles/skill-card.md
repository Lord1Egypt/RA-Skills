## Description:

Tidyfiles is a Bash command-line logbook for recording file-organization activities, reviewing recent entries, searching saved notes, and exporting logs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xueyetianya](https://clawhub.ai/user/xueyetianya)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use this skill as a local command-line logbook for file-organization notes, checks, reports, searches, and exports. It should not be relied on to move, sort, or organize files automatically.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may assume the skill organizes files, while the security summary identifies it as a local activity logger packaged as a file-organizing tool.

Mitigation: Use it only as a logbook for file-organization notes, and verify any actual file movement, sorting, or cleanup through separate tools.

Risk: Saved entries and exports may retain sensitive file paths, tokens, secrets, or confidential business details.

Mitigation: Avoid entering sensitive details, and review ~/.local/share/tidyfiles for retained logs and exports before sharing or disposing of the environment.

Risk: The security guidance calls for clearer consent and retention controls, harder file permissions, and fixes to search/export handling.

Mitigation: Review before installing, inspect generated files and permissions, and require the publisher to align the description and harden storage behavior before broad deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xueyetianya/skills/tidyfiles)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and terminal text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create plain-text logs and JSON, CSV, or TXT exports under ~/.local/share/tidyfiles.]

## Skill Version(s):

2.0.0 (source: release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
