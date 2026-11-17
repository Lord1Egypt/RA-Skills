## Description:

Helps Xiaohongshu creators and operators turn note topics or draft content into ten platform-focused title options grouped by likely click, save, comment, and overall fit.

This skill is ready for commercial/non-commercial use.

## Publisher:

[miromiraclemiro-ux](https://clawhub.ai/user/miromiraclemiro-ux)

### License/Terms of Use:

MIT-0

## Use Case:

External content creators, Xiaohongshu bloggers, and social media operations teams use this skill to generate concise Chinese title candidates for Xiaohongshu notes, including recommended title types, posting-time suggestions, tags, and usage tips.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes memory-style personalization notes for creator niche, target audience, title style, and feedback.

Mitigation: Review the host agent's memory settings before use and persist only user-approved, non-sensitive preferences.

Risk: The skill declares file read and write tools even though normal title generation can be completed from chat input.

Mitigation: Avoid granting file read/write access unless the user explicitly wants the skill to work with local draft files.

Risk: Overbroad routing may call the skill for adjacent content-marketing requests where it is not the best fit.

Mitigation: Use it for Chinese Xiaohongshu title assistance and route other platform, resume, or general chat tasks to more appropriate skills.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/miromiraclemiro-ux/skills/xhs-title-pro)

## Skill Output:

**Output Type(s):** [Markdown, Guidance, Text]

**Output Format:** [Markdown text with categorized title lists, recommendations, tags, and brief usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces ten title candidates per request and may personalize suggestions from the user's content domain, target audience, and stated style preferences.]

## Skill Version(s):

2.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
