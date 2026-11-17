## Description:

Quicknote is a terminal note-taking and productivity helper for capturing local notes, searching entries, and exporting saved content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ckchzh](https://clawhub.ai/user/ckchzh)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use Quicknote as a local terminal productivity helper for quickly recording notes, plans, reminders, and searchable activity snippets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores private productivity entries persistently in local plaintext.

Mitigation: Avoid highly sensitive content unless storage permissions, deletion behavior, and retention controls are reviewed and accepted.

Risk: The artifact does not reliably match advertised pin, delete, list, and markdown export behavior.

Mitigation: Validate the installed commands against the artifact before relying on those workflows.

## Reference(s):

- [Quicknote ClawHub listing](https://clawhub.ai/ckchzh/skills/quicknote)
- [BytesAgain feedback](https://bytesagain.com/feedback)

## Skill Output:

**Output Type(s):** [text, shell commands, files, configuration]

**Output Format:** [Terminal text with local JSON, CSV, or TXT export files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores persistent local plaintext logs under ~/.local/share/quicknote.]

## Skill Version(s):

1.0.4 (source: ClawHub release metadata; artifact frontmatter and script report 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
