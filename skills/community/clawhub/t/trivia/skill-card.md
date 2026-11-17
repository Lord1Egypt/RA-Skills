## Description:

Host trivia rounds with question banks, scoring, and boards. Use when running quizzes, checking answers, analyzing scores, generating rounds.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ckchzh](https://clawhub.ai/user/ckchzh)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use this skill to run local trivia-related command workflows, record activity, inspect recent entries, search logs, and export stored data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review identifies this release as a generic local activity logger packaged as a trivia skill, so users may store text that the tool can later surface.

Mitigation: Install only when a local plaintext activity log is intended; avoid entering secrets, API keys, personal data, private answer keys, or sensitive business content.

Risk: Activity is stored locally in plaintext under ~/.local/share/trivia.

Mitigation: Review and clean the local data directory after use, and tighten file permissions before storing anything important.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ckchzh/skills/trivia)
- [BytesAgain Homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Plain text and Markdown with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates and reads local plaintext activity logs under ~/.local/share/trivia.]

## Skill Version(s):

2.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
