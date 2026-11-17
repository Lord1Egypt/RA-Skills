## Description:

幸福开瓶器 is a Chinese-language wellbeing companion that turns daily mood, relationship, gift, travel, and monthly-review prompts into three ranked micro-action suggestions while maintaining local user profiles.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hardycg](https://clawhub.ai/user/hardycg)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this Chinese-language wellbeing assistant for personalized daily happiness suggestions, low-mood micro-actions, relationship and gift ideas, and monthly happiness summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can quietly retain sensitive local profiles about the user and people they mention, including emotional, relationship, family, location, and financial inferences.

Mitigation: Install only with informed user consent, add visible save prompts and view/delete controls, use private file permissions, and define retention limits for local profile files.

Risk: Wellbeing suggestions for low-mood scenarios may be mistaken for professional mental health support.

Mitigation: Keep responses limited to low-effort micro-actions, preserve the red/yellow/green intervention boundaries, and route high-risk language to appropriate support resources.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/hardycg/skills/xingfukaipingqi)
- [Profile Schema](references/profile-schema.md)
- [Suggestion Engine](references/suggestion-engine.md)
- [Tone Adaptation](references/tone-adaptation.md)
- [Monthly Summary](references/monthly-summary.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Chinese-language Markdown or plain text guidance with optional shell command snippets and JSON profile summaries.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local profile data when available; no network service is required by the bundled Python helper.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter, package.json, release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
