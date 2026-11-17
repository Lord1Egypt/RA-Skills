## Description:

每日唐诗推送。每天从全唐诗数据集中随机选取一首唐诗，生成包含深度赏析和作者介绍的结构化推送内容。触发词：每日唐诗、唐诗推送、唐诗赏析、今日唐诗。

This skill is ready for commercial/non-commercial use.

## Publisher:

[cantoneyes](https://clawhub.ai/user/cantoneyes)

### License/Terms of Use:

MIT-0

## Use Case:

External users and teams use this skill to schedule a daily Chinese poetry message that selects a poem, drafts a structured appreciation, and sends it to Feishu.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends scheduled Chinese-language poetry content to Feishu.

Mitigation: Confirm the Feishu destination, delivery schedule, and recipient consent before enabling the release.

Risk: The bundled poem dataset has quality caveats reported by security evidence, including a mismatched poem count and at least one non-Tang poem.

Mitigation: Review and correct the dataset before relying on the skill for curated or educational poetry distribution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cantoneyes/skills/tang-poem-daily)
- [Publisher profile](https://clawhub.ai/user/cantoneyes)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [JSON poem selection followed by a structured plain-text Feishu message]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Daily deterministic poem selection based on the current date; intended delivery channel is Feishu.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
