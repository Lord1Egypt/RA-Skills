## Description:

Thesaurus is advertised for synonym and related-word lookup, but the shipped artifact primarily records local command activity and exports or searches those logs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bytesagain3](https://clawhub.ai/user/bytesagain3)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can invoke the command-line skill to record thesaurus-related activity, inspect recent entries, search local logs, and export stored history. Review carefully before installation because server security evidence says the release does not provide a real thesaurus as shipped.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release is advertised as a thesaurus, but server security evidence says the included script is mostly a generic local activity and history tracker.

Mitigation: Review the script before installing and do not rely on it for synonym or antonym lookup unless the shipped behavior is acceptable.

Risk: User inputs may be written to local logs under ~/.local/share/thesaurus.

Mitigation: Avoid entering sensitive text or private prompts unless local activity logging is intended and acceptable.

Risk: Server security guidance notes unclear and partly broken export or status behavior.

Mitigation: Test export and status commands with non-sensitive sample data before depending on generated files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bytesagain3/skills/thesaurus)
- [Publisher profile](https://clawhub.ai/user/bytesagain3)
- [BytesAgain homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Plain text command output with optional JSON, CSV, or text export files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes local activity logs under ~/.local/share/thesaurus when commands are invoked.]

## Skill Version(s):

2.0.1 (source: server release evidence and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
