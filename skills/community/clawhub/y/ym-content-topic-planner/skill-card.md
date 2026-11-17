## Description:

Plans a content calendar from account positioning and existing content, with topic deduplication, series organization, per-post goals, and hooks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liuyuming0823](https://clawhub.ai/user/liuyuming0823)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, content strategists, and agents use this skill to plan what to publish next, avoid repeating previously covered angles, organize posts into series, and produce a structured Markdown schedule.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill activates for broad content-planning phrases and responds mainly in Chinese.

Mitigation: Confirm the target workspace expects Chinese content-planning behavior and adjust routing or locale expectations before deployment.

Risk: The skill cannot verify deduplication when the user does not provide prior content history.

Mitigation: Require users to provide historical titles when deduplication matters, and preserve the skill's documented 'not checked' labeling when history is missing.

Risk: The skill does not fetch real-time platform trends and does not guarantee traffic or follower growth.

Mitigation: Have users provide current trend inputs when needed and review plans as editorial guidance rather than performance predictions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/liuyuming0823/skills/ym-content-topic-planner)
- [Server-resolved GitHub provenance](https://github.com/liuyuming0823/ym-content-topic-planner)
- [Deduplication rules](references/dedup-rules.md)
- [Topic plan template](templates/topic-plan-template.md)

## Skill Output:

**Output Type(s):** [Markdown, Guidance]

**Output Format:** [Markdown with planning tables, topic candidates, hooks, goals, deduplication notes, and assumptions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Text-only; primarily Chinese; no code execution, network access, credential handling, persistence, or hidden behavior reported by security evidence.]

## Skill Version(s):

0.1.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
