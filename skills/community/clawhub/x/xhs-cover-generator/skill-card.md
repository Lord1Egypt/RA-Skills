## Description: <br>
AI cover design assistant for Xiaohongshu creators that queries recent popular-note data, analyzes cover patterns, and produces actionable cover concepts and image-generation prompts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[if530770](https://clawhub.ai/user/if530770) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators, brand operators, agencies, and MCN teams use this skill to turn a Xiaohongshu topic or draft into a data-informed cover analysis, visual direction, and practical cover-generation prompt. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends search keywords to a third-party trend API. <br>
Mitigation: Avoid submitting confidential topics or customer-sensitive planning terms, and review the API endpoint before normal use. <br>
Risk: Reports may include public creator/profile links and raw remote XHS or CDN image URLs. <br>
Mitigation: Review generated reports before sharing and remove creator, profile, or media links when redistribution is not appropriate. <br>
Risk: The security evidence notes disabled HTTPS certificate verification, so returned data could be intercepted or tampered with. <br>
Mitigation: Review and patch the network request behavior before routine use, or run only in a constrained environment where this risk is acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/if530770/xhs-cover-generator) <br>
- [Core workflow](references/core_workflow.md) <br>
- [Xiaohongshu trend data format](references/xhs_trend_data_format.md) <br>
- [Third-party trend API endpoint](https://onetotenvip.com/skill/cozeSkill/getXhsCozeSkillData) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown reports with image links, tables, design recommendations, generation prompts, and optional JSON data.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include remote Xiaohongshu/CDN image URLs, creator or profile links, interaction metrics, and optional debug or output files.] <br>

## Skill Version(s): <br>
1.0.2 (source: server evidence release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
