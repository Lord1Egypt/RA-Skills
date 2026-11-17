## Description:

Reverse each line of text character by character for text analysis, palindrome checks, and data format conversion.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dinghaibin](https://clawhub.ai/user/dinghaibin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to reverse text for lightweight inspection, palindrome checks, and simple text transformation workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The current script reverses the full input stream rather than each line independently, which can change line order or newline placement for line-oriented data.

Mitigation: Use it only where whole-stream reversal is acceptable, or review and update the script before relying on line-oriented conversion.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dinghaibin/skills/rev-tool)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text and Markdown guidance with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Current implementation processes stdin as one complete text stream.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
