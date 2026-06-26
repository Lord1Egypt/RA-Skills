## Description: <br>
输入研究主题，自动采集 Reddit 讨论，提炼爆款角度，产出 X 推文、小红书笔记、公众号文章三平台成品。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Wbule](https://clawhub.ai/user/Wbule) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Content creators, marketers, researchers, and developers use this skill to research public Reddit discussions for a topic, identify content angles, and generate draft content for X, Xiaohongshu, and WeChat. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill makes outbound requests to Reddit and may use Reddit API credentials from the local environment. <br>
Mitigation: Use only approved Reddit API credentials and review network access expectations before running the collection steps. <br>
Risk: The workflow stores Reddit-derived data and generated drafts under runs/<slug>. <br>
Mitigation: Avoid sensitive private research topics unless local storage of collected material and drafts is acceptable. <br>
Risk: Generated social and article drafts may contain inaccurate or misleading interpretations of Reddit discussions. <br>
Mitigation: Review generated content and source tables before publishing or reusing the drafts. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Wbule/reddit-topic-insight) <br>
- [10 article types](reference/article-types.md) <br>
- [X tweet template](reference/x-tweet-template.md) <br>
- [Xiaohongshu note template](reference/xiaohongshu-template.md) <br>
- [WeChat article template](reference/wechat-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Files, Shell commands, Configuration] <br>
**Output Format:** [Markdown reports and JSON intermediate files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local run artifacts under runs/<slug>, including Reddit post data, angle plans, per-angle drafts, and a merged content.md report.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
