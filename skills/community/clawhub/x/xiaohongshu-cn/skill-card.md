## Description: <br>
小红书分析 - 热门笔记发现、关键词监控、趋势分析（Instagram 中国版） <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[guohongbin-git](https://clawhub.ai/user/guohongbin-git) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to guide Xiaohongshu trend research, keyword monitoring, and creator or brand analysis with manual web review or carefully reviewed third-party tools. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill discusses third-party scraping and packet-capture approaches for a platform without a public API. <br>
Mitigation: Review linked tools separately, pin a known-safe commit when possible, run them in a sandbox or disposable environment, and keep collection low-rate and compliant with platform rules. <br>
Risk: Packet capture or reverse engineering can create legal, privacy, account, and credential exposure. <br>
Mitigation: Avoid those techniques unless the operator understands and accepts the risks, and do not expose credentials or personal data during analysis. <br>


## Reference(s): <br>
- [Xiaohongshu Explore](https://www.xiaohongshu.com/explore) <br>
- [Xiaohongshu Search](https://www.xiaohongshu.com/search_result) <br>
- [XiaohongshuSpider](https://github.com/Big-Buffer/XiaohongshuSpider) <br>
- [xiaohongshu-spider](https://github.com/63can/xiaohongshu-spider) <br>
- [Nanji](https://www.nanji.com/) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands] <br>
**Output Format:** [Markdown guidance with reference links and example shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance may point to third-party crawler tooling that should be reviewed before use.] <br>

## Skill Version(s): <br>
1.0.0 (source: package.json and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
