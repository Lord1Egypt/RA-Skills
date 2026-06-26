## Description: <br>
Use when generating a complete WeChat article from a topic, with optional source research, evidence tracking, illustration, HTML conversion, and draft-box publishing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhylq](https://clawhub.ai/user/zhylq) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators, operators, and developers use this skill to turn a topic or reference URLs into a traceable WeChat article, with optional illustrations, WeChat-styled HTML, and a draft-box upload for review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow can upload generated drafts to a real WeChat account when draft publishing is enabled and credentials are configured. <br>
Mitigation: Set post_to_wechat to false unless draft upload is intended, protect .env secrets and Chrome profile directories, and review generated HTML before upload. <br>
Risk: Optional illustration upload can place generated images on public CDN hosting. <br>
Mitigation: Keep illustration_upload false unless public hosting is acceptable and review generated images before using them in a draft. <br>
Risk: Generated articles may include incorrect or unsupported claims if source collection is weak. <br>
Mitigation: Review the evidence pool, cited sources, and review report before relying on or publishing the article. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhylq/zhy-wechat-writing) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, HTML, Guidance] <br>
**Output Format:** [Markdown articles, evidence and review files, optional WeChat HTML, optional illustration assets, and execution summaries.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes outputs under articles/<slug>/ and may save a WeChat draft when publishing is enabled.] <br>

## Skill Version(s): <br>
0.1.0 (source: ClawHub release metadata; artifact SKILL.md reports 3.6.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
