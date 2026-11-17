## Description:

Optimizes Chinese Midjourney image prompts by filtering sensitive wording, applying style enhancements, and returning ready-to-use English prompts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tianheihei002](https://clawhub.ai/user/tianheihei002)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use this skill to turn Chinese image descriptions into English Midjourney prompts while applying the bundled wording substitutions and style suffix.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Silent prompt rewriting can remove or change parts of the user's request.

Mitigation: Review the final generated prompt before submitting it, especially when exact wording or user intent must be preserved.

Risk: The skill is oriented toward identifying wording that avoids Midjourney moderation filters.

Mitigation: Use it only for acceptable prompt cleanup and apply the destination platform's content and safety policies before use.

## Reference(s):

- [Sensitive Words Reference](references/sensitive-words.md)
- [ClawHub Skill Page](https://clawhub.ai/tianheihei002/skills/yq-mj-prompt-optimizer)

## Skill Output:

**Output Type(s):** [text, guidance]

**Output Format:** [Plain text English Midjourney prompt]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Applies wording substitutions silently and appends a standard Midjourney style and exclusion suffix.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
