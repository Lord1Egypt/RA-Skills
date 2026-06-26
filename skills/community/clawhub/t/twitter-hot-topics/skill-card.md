## Description: <br>
每小时监控 Twitter/X 上中国、加密货币、国际、美国和特朗普相关热点，提取 TOP 10 话题并生成中文推文草稿和发布建议。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yanghui-88](https://clawhub.ai/user/yanghui-88) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Social media operators, creators, and marketing teams use this skill to monitor current Twitter/X topics and draft Chinese posts or threads with publishing guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Recurring Twitter/X monitoring can run broad automatic trend searches without clear user control. <br>
Mitigation: Configure any hourly schedule explicitly before use and confirm how to stop or disable recurring execution. <br>
Risk: Generated trend claims and draft posts may be inaccurate, outdated, or misleading. <br>
Mitigation: Fact-check all trend claims against current sources before publishing, especially for political and market-sensitive topics. <br>
Risk: Style-imitation drafts may imply affiliation with named creators if published without care. <br>
Mitigation: Use the style guidance as inspiration only and avoid presenting drafts as written, approved, or endorsed by the referenced creators. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yanghui-88/twitter-hot-topics) <br>
- [X algorithm rules reference](artifact/references/algorithm-rules.md) <br>
- [Chinese creator style guide](artifact/references/kol-style-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown report with a ranked topic table, tweet drafts, and a publishing checklist] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generates TOP 10 hotspot rankings and two Chinese draft variants per topic; users should fact-check before posting.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
