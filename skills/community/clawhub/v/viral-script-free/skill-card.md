## Description:

输入一份口播逐字稿，输出结构地图、开场钩子判定、留存节奏诊断、口语度评分、CTA 强度，并列出按严重度分级的问题清单；免费版展示体检总览、结构地图与前 3 条问题。

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, marketers, and content teams use this skill to run an offline, rule-based check of Chinese spoken short-video scripts before recording or publishing. It helps identify missing structure, weak openings, pacing issues, written-language phrasing, and CTA weakness without sending transcript data over the network.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The declared Write permission is broader than the inspected runtime behavior needs.

Mitigation: Review requested tool permissions before installation and run the skill with only the file access needed for the input JSON; the inspected runtime reads a transcript JSON and writes the report to standard output.

Risk: Users may treat the mechanical script diagnosis as a guarantee of virality, platform approval, legal compliance, or sales performance.

Mitigation: Present results as structure and expression checks only, and direct users to platform rules, legal review, or domain specialists for compliance and commercial claims.

Risk: The rule set is focused on Chinese spoken short-video scripts and China-oriented platforms.

Mitigation: Use it only for matching Chinese-language spoken-script workflows, and warn users that non-script materials or other platform contexts may make the diagnostic output unreliable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/viral-script-free)
- [钩子判定口径](artifact/references/hook-patterns.md)
- [平台口径参考](artifact/references/platform-rules.md)

## Skill Output:

**Output Type(s):** [text, JSON, guidance]

**Output Format:** [Console text report or JSON diagnostic summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Free tier limits issue details to the first 3 findings and withholds positions, rule bases, rewrite advice, golden-line candidates, and remix blueprint details.]

## Skill Version(s):

1.0.28 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
