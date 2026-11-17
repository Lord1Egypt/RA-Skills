## Description:

Translation assistant capability.

This skill is ready for commercial/non-commercial use.

## Publisher:

[534422530](https://clawhub.ai/user/534422530)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to trigger translation-assistant guidance when requests mention translation, such as translating a phrase or asking how to translate text.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may activate outside translation requests because the security evidence flags poor scoping and unrelated triggers.

Mitigation: Narrow activation phrases to explicit translation requests before normal use.

Risk: The artifact contains unrelated Home Assistant and plugin-installation content.

Mitigation: Remove unrelated Home Assistant material and re-scan the skill before deployment.

Risk: The artifact refers to local executor files that are not included in the release.

Mitigation: Verify required executor dependencies in the target agent environment before installation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/534422530/skills/translation-assistant)
- [Publisher profile](https://clawhub.ai/user/534422530)

## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [Markdown with optional inline code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include bilingual English and Chinese usage guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
