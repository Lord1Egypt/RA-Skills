## Description: <br>
小红书短视频运营增长助手适合内容创作者、运营、品牌方、电商在用户提供了小红书笔记链接时使用，帮助基于输入材料生成情绪和舆情视图、用户画像和意图分析、优化与转化建议。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[allinherog-star](https://clawhub.ai/user/allinherog-star) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content creators, operations teams, brands, and ecommerce users use this skill to analyze Xiaohongshu note or short-video comments after providing a Xiaohongshu link. It returns sentiment and public-opinion views, user profile and intent analysis, and practical content optimization or conversion suggestions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Xiaohongshu links, parsed content details, and comment-analysis task data are sent to ai-skills.ai using the user's API key. <br>
Mitigation: Submit only content that is approved for external processing, and avoid private, regulated, or unauthorized business or customer content unless that processing is acceptable. <br>
Risk: The skill requires a sensitive API credential to run. <br>
Mitigation: Store AISKILLS_API_KEY securely, avoid committing it to source control, and rotate it if exposure is suspected. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/allinherog-star/xhs-sentiment-dashboard) <br>
- [Form schema](references/form-schema.json) <br>
- [Skill metadata](references/skill.json) <br>
- [AI Skills](https://ai-skills.ai) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Analysis, Guidance] <br>
**Output Format:** [JSON task result with sentiment summary, labeled comments, user insights, and operation advice] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns an asynchronous comment-analysis task result after polling reaches a terminal status.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
