## Description:

Read and write messages on a Vestaboard using the Vestaboard Cloud API and optional legacy read-write endpoint.

This skill is ready for commercial/non-commercial use.

## Publisher:

[seidprojects](https://clawhub.ai/user/seidprojects)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators use this skill to preview, read, and update Vestaboard messages, including short status text and simple 6 x 22 color layouts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Write commands can immediately change a physical Vestaboard display.

Mitigation: Preview messages first and run write commands only from trusted workflows with intentional operator approval.

Risk: Credentials can be sent to a configurable API endpoint.

Mitigation: Keep Vestaboard tokens private and leave VESTABOARD_API_BASE unset unless the endpoint is fully trusted.

Risk: The write-layout command can upload arbitrary local JSON files.

Mitigation: Use known layout files from the skill directory until path and layout validation are added.

## Reference(s):

- [Vestaboard Character Codes](https://docs.vestaboard.com/docs/characterCodes/)
- [Character Codes Reference](references/character-codes.md)
- [Formatting Notes](references/formatting.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, JSON]

**Output Format:** [Markdown guidance with inline shell commands and JSON board payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Messages are constrained to the Vestaboard 6 x 22 grid; text is uppercased, word-wrapped, and truncated on overflow.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
