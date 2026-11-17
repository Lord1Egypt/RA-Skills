## Description:

Turbine provides shell commands for recording, listing, searching, removing, exporting, and configuring local turbine-related entries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bytesagain1](https://clawhub.ai/user/bytesagain1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators can use this skill to manage local turbine records from a command-line workflow, including status checks, data entry, search, export, statistics, and configuration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may surprise users who expect only a calculator because it stores local records, mutates configuration, deletes entries, and writes export files.

Mitigation: Install it only when local record management is desired, set TURBINE_DIR to a controlled workspace, and review remove, export, and config operations before use.

Risk: The security evidence reports shell input-handling bugs that could be dangerous when command arguments come from an agent or another user.

Mitigation: Do not pass untrusted arguments to the shell script; review the script before installation and run it in a constrained environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bytesagain1/skills/turbine)
- [Publisher profile](https://clawhub.ai/user/bytesagain1)
- [Publisher homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration]

**Output Format:** [Plain text command output and JSONL or CSV export files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses TURBINE_DIR when set; otherwise stores local data under ~/.turbine/.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
