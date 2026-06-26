## Description: <br>
Generates Xiaohongshu post copy, publishing schedules, trend-informed variants, and matching cover prompts for teams operating Xiaohongshu accounts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[daniel-yu-gold](https://clawhub.ai/user/daniel-yu-gold) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Marketing and social content operators use this skill to generate Xiaohongshu copy, organize account-by-date content schedules, and create companion cover concepts. It is intended for teams that need repeatable content operations across multiple Xiaohongshu accounts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can delete and rewrite Feishu scheduling records, which could overwrite existing campaign data if the target project, table, date range, or account range is wrong. <br>
Mitigation: Before allowing writes, require the agent to show the target project and table, date and account range, records that would be deleted, and replacement rows; use least-privilege Feishu access. <br>
Risk: Cover-generation guidance includes prompts to avoid similarity checks, which could encourage attempts to bypass originality or content review controls. <br>
Mitigation: Review generated cover prompts and assets for originality, rights, and platform compliance, and avoid prompts intended to bypass originality or similarity checks. <br>
Risk: Generated Xiaohongshu copy may include platform-sensitive terms or promotional claims that create moderation or compliance risk. <br>
Mitigation: Apply the bundled sensitive-word and product-reference rules before publishing, and require human review for regulated claims, pricing language, and contact-channel guidance. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/daniel-yu-gold/xhs-bahamo-copywriter) <br>
- [产品引用规则](references/产品引用.md) <br>
- [小红书敏感词清单](references/敏感词.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Configuration, Guidance] <br>
**Output Format:** [Markdown and structured text for post copy, scheduling instructions, cover-generation prompts, and Feishu table updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose or perform Feishu table record updates when the agent has the required workspace access.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
