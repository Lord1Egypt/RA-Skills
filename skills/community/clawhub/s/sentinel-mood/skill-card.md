## Description:

Analyze the sentiment and emotional tone of text using NLTK and VADER. Use this to gauge user mood, detect urgency, or analyze content tone.

This skill is ready for commercial/non-commercial use.

## Publisher:

[numbpill3d](https://clawhub.ai/user/numbpill3d)

### License/Terms of Use:

MIT

## Use Case:

Developers and external agents use this skill to score the sentiment and emotional tone of short-form or conversational text, such as user messages, social posts, and content snippets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may install or fetch NLTK/VADER dependency data if the VADER lexicon is missing.

Mitigation: Preinstall and verify the NLTK package and vader_lexicon resource in locked-down or offline environments before enabling the skill.

## Reference(s):

- [Sentinel Mood on ClawHub](https://clawhub.ai/numbpill3d/skills/sentinel-mood)
- [Publisher profile](https://clawhub.ai/user/numbpill3d)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, guidance]

**Output Format:** [JSON sentiment scores with positive, negative, neutral, and compound values]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns an error object when no text is provided or sentiment analysis fails.]

## Skill Version(s):

1.0.0 (source: package.json and ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
