## Description:

通过联网搜索整理主题资料，并生成可按比例裁剪的知乎风格深度回答网页。

This skill is ready for commercial/non-commercial use.

## Publisher:

[timerate-966](https://clawhub.ai/user/timerate-966)

### License/Terms of Use:

MIT-0

## Use Case:

研究者、学习者和内容创作者可围绕一个主题检索资料，并整理成可裁剪的知乎风格知识专题页、教程或行业研究网页。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Security evidence flags broad permission changes and access to files beyond the stated research and webpage-generation purpose.

Mitigation: Review requested permissions and constrain file access before running the skill.

Risk: Research topics may include information the user does not want sent to external search services.

Mitigation: Avoid submitting sensitive topics or details to external search services.

Risk: Security review coverage is partial and does not establish that all referenced or runtime behavior was assessed.

Mitigation: Review referenced resources and runtime behavior; do not treat the partial scan as a complete assessment.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/timerate-966/skills/zhihu-research-page-skill)
- [Publisher profile](https://clawhub.ai/user/timerate-966)

## Skill Output:

**Output Type(s):** [HTML, Files, Research summaries]

**Output Format:** [Single-file HTML webpage with styled sections and linked sources]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Output size and search volume scale with the requested percentage. A full version may take about 100 minutes and consume many tokens; the skill recommends trying a 2% version first.]

## Skill Version(s):

22.0.2 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
