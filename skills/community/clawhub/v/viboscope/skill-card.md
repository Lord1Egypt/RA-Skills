## Description:

Viboscope helps agents find compatible cofounders, project partners, groups, friends, or other contacts through psychological compatibility matching.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivankoriako](https://clawhub.ai/user/ivankoriako)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to build a psychological matching profile, search for compatible people, manage conversations, and update profile or subscription settings through Viboscope.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles sensitive psychological and relationship data and may upload profile details to Viboscope.

Mitigation: Require explicit user consent before any profile upload, show the exact profile content that will be sent, and keep private psychological scores out of user-to-user messages.

Risk: The skill may inspect workspace files and git information while building a profile.

Mitigation: Ask before scanning local files, limit scans to relevant workspace content, and show findings for user approval before using them.

Risk: API keys stored near project files can be exposed through logs, shell history, or version control.

Mitigation: Store credentials outside version-controlled files where possible, use restrictive file permissions, avoid echoing keys, and redact headers or raw requests in errors.

Risk: Remote update commands and account actions such as messaging, deletion, or profile uploads can have user-visible consequences.

Mitigation: Independently verify remote update URLs and require manual approval before sending messages, deleting data, sharing contact details, or changing account state.

## Reference(s):

- [Viboscope ClawHub skill page](https://clawhub.ai/ivankoriako/skills/viboscope)
- [Viboscope API base](https://viboscope.com/api/v1)
- [Viboscope hosted skill artifact](https://viboscope.com/api/v1/skill)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, JSON request examples, and configuration file updates.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local data files for API keys, profiles, prompts, and questionnaire responses when the host agent has filesystem access.]

## Skill Version(s):

4.0.0 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
