## Description:

Analyze a Twitter/X account's posting style and generate authentic posts that match their voice.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gravyxbt](https://clawhub.ai/user/gravyxbt)

### License/Terms of Use:


## Use Case:

Developers, social media operators, and authorized account owners use this skill to analyze public or provided X post samples, build a voice profile, and draft X posts that match an account's observed style.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can imitate arbitrary X accounts without built-in consent checks.

Mitigation: Use it only for the user's own account or accounts whose owner has authorized voice matching, and review drafts before posting.

Risk: Generated posts may mislead audiences if presented as authentic account-owner speech.

Mitigation: Treat generated posts as drafts and label or disclose AI assistance where appropriate.

Risk: Voice profiles, sample posts, generated prompts, and generated drafts may be saved locally or printed in terminal output.

Mitigation: Avoid processing sensitive or private account data and review local output files and terminal logs before sharing the workspace.

## Reference(s):

- [X Post Types & Frameworks](references/post-types.md)
- [ClawHub skill page](https://clawhub.ai/gravyxbt/skills/x-voice-match)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, JSON voice profiles, and JSON-style generated post drafts with confidence scores and reasoning]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write local JSON profile or post files when output paths are provided.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
