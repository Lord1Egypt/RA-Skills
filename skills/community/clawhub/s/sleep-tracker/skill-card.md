## Description:

Sleep Tracker helps agents run a local CLI for sleep and wellness logging, sleep analysis, schedule planning, environment checks, nap guidance, and improvement tips.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bytesagain-lab](https://clawhub.ai/user/bytesagain-lab)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use this skill to log sleep or wellness entries, review recent history and streaks, calculate sleep schedules, analyze sleep duration, and get general sleep hygiene guidance from local shell commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sleep journal entries can contain personal sleep or health notes, and one artifact script stores journal data in a shared temporary file.

Mitigation: Use the skill only after review, avoid shared machines for personal entries, and prefer storage in a private per-user directory with restrictive permissions.

Risk: The security summary says the documentation does not clearly match the artifact behavior.

Mitigation: Confirm which script and commands are intended before installation or execution, especially before logging or exporting personal data.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/bytesagain-lab/skills/sleep-tracker)
- [Publisher Profile](https://clawhub.ai/user/bytesagain-lab)
- [BytesAgain Homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text CLI output with optional shell redirection]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include locally recorded sleep or wellness notes when the user logs or exports data.]

## Skill Version(s):

2.0.1 (source: server release metadata; artifact frontmatter and scripts report 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
