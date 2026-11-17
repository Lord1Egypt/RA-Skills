## Description:

Aligns columns in plain text tables using specified or auto-detected delimiters for improved readability and consistent spacing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[albionaiinc-del](https://clawhub.ai/user/albionaiinc-del)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, data analysts, and operators use this skill to turn delimiter-separated text, logs, and CSV-like rows into aligned plain-text columns for easier reading and review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Documented command names differ between the usage text and the script examples, which can cause invocation failures after installation.

Mitigation: Confirm the installed entry point before use, or invoke the Python script directly with the intended delimiter and padding arguments.

Risk: The server security guidance notes that the pipe example may not work without a code fix.

Mitigation: Prefer file input for release validation, or test standard-input handling before relying on piped workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/albionaiinc-del/skills/txt-col-align)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text or Markdown with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces aligned plain-text columns from local file or standard-input data; no network output or persistent behavior is indicated.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
