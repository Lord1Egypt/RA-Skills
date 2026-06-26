## Description: <br>
Generates WeChat public-account article drafts by monitoring AI and technology trends, filtering candidate topics, and creating review-ready Markdown drafts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gdp6539](https://clawhub.ai/user/gdp6539) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Content creators, social media operators, and marketing teams use this skill to monitor public trend sources and generate WeChat article drafts for human review. Treat it as a draft-generation workflow, not as a complete live WeChat publisher. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release implies live WeChat auto-publishing and requests WeChat credentials, while security evidence says publishing is not implemented. <br>
Mitigation: Use the skill for draft generation only, leave autoPublish disabled, and do not add WeChat app secrets until publishing behavior is implemented and reviewed. <br>
Risk: The skill makes outbound requests to public trend sources and DashScope for article generation. <br>
Mitigation: Run it only where those network calls are expected, configure DASHSCOPE_API_KEY through a local environment file, and keep any .env file out of version control. <br>
Risk: Generated drafts and scraped trend summaries can be inaccurate, stale, or unsuitable for publication. <br>
Mitigation: Manually review generated drafts, verify important claims against sources, and check content rights before publication. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gdp6539/wechat-auto-publisher) <br>
- [Alibaba Cloud Bailian console](https://bailian.console.aliyun.com/) <br>
- [DashScope OpenAI-compatible endpoint](https://dashscope.aliyuncs.com/compatible-mode/v1) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown article drafts, JSON topic data, and console status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated drafts are intended for manual review; auto-publishing should remain disabled unless a reviewed publishing implementation is added.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
