## Description:

Generates Xiaohongshu marketing copy, posting schedules, hotspot-analysis material, and matching cover-generation prompts for content operations teams.

This skill is ready for commercial/non-commercial use.

## Publisher:

[daniel-yu-gold](https://clawhub.ai/user/daniel-yu-gold)

### License/Terms of Use:

MIT-0

## Use Case:

External content operators and marketing teams use this skill to generate Xiaohongshu post drafts, multi-account publishing schedules, product-reference fields, sensitive-word checks, and cover-generation prompts for campaign operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can delete conflicting Feishu schedule rows before writing replacements.

Mitigation: Limit Feishu access to the intended Xiaohongshu project tables and require a preview or explicit confirmation before overwriting or deleting schedule rows.

Risk: Cover-generation guidance includes wording aimed at avoiding duplicate-detection checks.

Mitigation: Revise cover prompts to require original, licensed visuals and remove duplicate-evasion intent before operational use.

Risk: Generated copy may include Xiaohongshu-sensitive wording if project inputs conflict with the sensitive-word rules.

Mitigation: Review generated drafts against the included sensitive-word list before posting or scheduling publication.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/daniel-yu-gold/skills/xhs-bahamo-copywriter)
- [小红书敏感词清单](references/敏感词.md)
- [产品引用规则](references/产品引用.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Guidance]

**Output Format:** [Chinese marketing copy, schedule entries, sensitive-word guidance, and cover-generation prompts in Markdown or table form.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write or replace connected Feishu schedule rows when used with the intended project tables; cover outputs may be saved as image files under /tmp/xhs-cover/.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
