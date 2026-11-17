## Description:

Calls the Li Xiaowen Yijing API to cast or interpret hexagrams and returns either Markdown with images or terminal-friendly ASCII rendering.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liquanyu123](https://clawhub.ai/user/liquanyu123)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to ask Yijing/I Ching divination questions, provide context, and receive a structured reading. The agent also helps configure API_KEY and RENDER_STYLE before calling the service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User divination prompts are sent to wenmutang.top, which may expose personal or sensitive context.

Mitigation: Do not include unnecessary personal, medical, financial, employer-confidential, or third-party details in prompts.

Risk: The artifact describes editing API_KEY into SKILL.md, which can expose credentials if the file is shared or committed.

Mitigation: Configure the API key through an environment variable or managed secret instead of storing it in SKILL.md.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/liquanyu123/skills/yijing-suangua)
- [Skill homepage](https://github.com/liquanyu123/yijing-suangua)
- [Wenmutang API endpoint](https://wenmutang.top/api/skill/chat)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown by default, with optional terminal ASCII hexagram and rating blocks when RENDER_STYLE is set to 艺术字]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires API_KEY and RENDER_STYLE configuration; API responses may include image links and hexagram metadata.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
