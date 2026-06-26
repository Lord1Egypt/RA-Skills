## Description: <br>
ZeeLin小红书自动化内容运营技能：从热文抓取、热梗生成、产品结合到发布文案，支持短视频选题策划、爆款文案生成、账号定位和内容日历规划。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kelcey2023](https://clawhub.ai/user/kelcey2023) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators, marketers, and content operators use this skill to plan Xiaohongshu and short-form social content, generate topic hooks and scripts, and optionally automate posting into a logged-in Xiaohongshu creator account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can publish live posts from a logged-in Xiaohongshu creator account without a clear final approval step. <br>
Mitigation: Review generated content manually, use draft-only controls such as XHS_NO_PUBLISH where available, and do not run auto-publish scripts unless the post is ready to go live. <br>
Risk: Running the automation against a regular browser profile can affect a real creator account. <br>
Mitigation: Use a dedicated browser profile or test account when installing or evaluating the skill. <br>


## Reference(s): <br>
- [Auto Content Ops Skill Documentation](references/auto-content-ops-skill-完整文档.md) <br>
- [Methodology](references/methodology.md) <br>
- [Xiaohongshu Creator Center](https://creator.xiaohongshu.com) <br>
- [ClawHub skill page](https://clawhub.ai/kelcey2023/zeelin-xiaohongshu-autopost) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/kelcey2023) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, code, configuration, guidance] <br>
**Output Format:** [Markdown content plans and publishing guidance, with shell commands or script-driven actions when posting is requested.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May interact with a logged-in Xiaohongshu creator browser session; use draft-only controls such as XHS_NO_PUBLISH where available before live publishing.] <br>

## Skill Version(s): <br>
1.0.100 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
