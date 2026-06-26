## Description: <br>
小红书议题报告生成工具。当用户说"小红书上关于XXX的议题，生成报告"或类似表达时触发。自动搜索小红书热帖 + 头部媒体资讯 + Twitter/X 推文，三源交叉验证去重，生成结构化舆情报告。如已配置飞书则发布到飞书文档，否则直接输出报告。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[minmengxhw-cpu](https://clawhub.ai/user/minmengxhw-cpu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and analysts use this skill to generate structured public-topic reports that combine Xiaohongshu posts, media coverage, and Twitter/X discussion with cross-source deduplication and verification notes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated reports may include misleading or stale claims from public social and media sources. <br>
Mitigation: Review source labels, cross-source verification notes, and disputed items before relying on or sharing the report. <br>
Risk: Optional Feishu publishing can send generated documents or links to unintended locations if credentials or destinations are misconfigured. <br>
Mitigation: Use a least-privileged Feishu app and confirm the intended document or group destination before enabling publishing. <br>
Risk: Browser sessions can expose content the user has intentionally logged in to access. <br>
Mitigation: Keep browser sessions limited to public or intentionally included content, and avoid private or restricted pages. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Structured Markdown report or Feishu document link when Feishu publishing is configured] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May degrade to fewer public sources or direct chat output when optional tools or Feishu credentials are unavailable.] <br>

## Skill Version(s): <br>
1.4.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
