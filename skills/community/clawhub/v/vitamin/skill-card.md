## Description:

Track vitamin and supplement intake with goals and reminders. Use when logging supplements, setting nutrition goals, reviewing history, or scheduling doses.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bytesagain-lab](https://clawhub.ai/user/bytesagain-lab)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to manage a local terminal-based supplement log, including intake records, goals, reminders, activity history, search, status checks, and exports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Supplement and wellness entries are stored as plaintext logs under ~/.local/share/vitamin.

Mitigation: Avoid recording sensitive medical details, restrict local directory permissions where appropriate, and clear the directory when the data is no longer needed.

Risk: The export command is reported as unreliable because of a duplicate command bug.

Mitigation: Treat exported JSON, CSV, or text files as untrusted until manually checked, and verify export behavior before relying on backups.

## Reference(s):

- [Vitamin on ClawHub](https://clawhub.ai/bytesagain-lab/skills/vitamin)
- [bytesagain-lab ClawHub Profile](https://clawhub.ai/user/bytesagain-lab)
- [BytesAgain Homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [Shell commands, Text, Files]

**Output Format:** [Terminal text output and local JSON, CSV, or plain text export files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores entries locally under ~/.local/share/vitamin.]

## Skill Version(s):

2.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
