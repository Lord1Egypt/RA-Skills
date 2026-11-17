## Description:

Create user-facing App Store release notes by collecting and summarizing all user-impacting changes since the last git tag (or a specified ref).

This skill is ready for commercial/non-commercial use.

## Publisher:

[quincygunter](https://clawhub.ai/user/quincygunter)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and release managers use this skill to turn git history into concise, user-facing App Store release notes that emphasize visible changes and omit internal work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads git commit history and touched file names from the target repository.

Mitigation: Use it only in repositories where exposing commit subjects and changed paths to the agent is acceptable.

Risk: The helper script has a limited shell-quoting weakness around revision arguments.

Mitigation: Pass ordinary trusted tags or commit refs, and quote or validate revision arguments before using the script in automated release workflows.

Risk: Generated release notes may include ambiguous or internal changes if the git history is unclear.

Mitigation: Review each bullet against the selected git range and ask for clarification when a change is not clearly user-visible.

## Reference(s):

- [App Store Release Notes Guidelines](references/release-notes-guidelines.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown bullet list with optional shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Release notes are expected to be concise, user-facing bullets tied to changes in the selected git range.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
