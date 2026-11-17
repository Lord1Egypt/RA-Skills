## Description:

Rename the current chat to match its focus. Use only when the user invokes /rename-chat. Optional text after the command steers the title.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eohmig](https://clawhub.ai/user/eohmig)

### License/Terms of Use:

MIT-0

## Use Case:

People using Cursor invoke this slash-only skill to rename the current chat with a concise topic title based on the chat focus and optional hint text.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill renames the current chat immediately after explicit /rename-chat invocation without a confirmation prompt.

Mitigation: Review the command and optional hint before invoking when exact title wording matters.

## Reference(s):


## Skill Output:

**Output Type(s):** [API Calls, Text]

**Output Format:** [Single chat rename action, with plain text only if the rename tool is unavailable or fails]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generates a 3-5 word sentence-case title with a 200-character maximum]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
