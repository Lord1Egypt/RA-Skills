## Description:

Rewrites AI-written text to sound more natural while aiming to preserve its meaning, facts, and voice.

This skill is ready for commercial/non-commercial use.

## Publisher:

[abcqq1234567](https://clawhub.ai/user/abcqq1234567)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use it to polish AI-drafted essays, posts, fiction, marketing copy, and work documents through a cloud text-processing service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad polishing and ChatGPT-related triggers may activate the skill unexpectedly.

Mitigation: Review the skill's trigger rules and invoke it only when the user requests text processing.

Risk: Submitted text is sent to a cloud service, and host runtime network permissions were not confirmed.

Mitigation: Avoid submitting sensitive personal information and confirm network access is acceptable for the intended use.

Risk: A personal API key is stored in plaintext when the user explicitly saves it.

Mitigation: Save a personal key only when needed, keep the local config file protected, and clear the key when it is no longer required.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/abcqq1234567/skills/text-humanizer-pro)
- [Humanizer API](https://1257655569-3o00dbw8fr.ap-singapore.tencentscf.com/v1/chat/completions)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [Rewritten natural-language text with an optional quality report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Preserves the input language and aims to retain the original meaning, facts, and voice.]

## Skill Version(s):

1.7.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
