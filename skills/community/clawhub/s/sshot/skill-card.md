## Description:

Take full screen screenshot using PowerShell.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alenzhu72](https://clawhub.ai/user/alenzhu72)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to trigger a full-screen screenshot on a configured Windows node and receive the captured screenshot file path.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill captures the entire visible screen, which may include private messages, documents, passwords, or dashboards.

Mitigation: Use it only in trusted environments and add an explicit confirmation step before captures.

Risk: The skill runs an unaudited PowerShell script with execution-policy bypass on a hard-coded Windows node.

Mitigation: Verify or package the referenced script, remove the execution-policy bypass where possible, and restrict who can modify the script path.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/alenzhu72/skills/sshot)
- [Publisher profile](https://clawhub.ai/user/alenzhu72)

## Skill Output:

**Output Type(s):** [Shell commands, Files, Text]

**Output Format:** [Text output containing a screenshot file path]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs on Windows and captures the full screen through a configured PowerShell script.]

## Skill Version(s):

1.0.0 (source: release evidence and artifact meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
