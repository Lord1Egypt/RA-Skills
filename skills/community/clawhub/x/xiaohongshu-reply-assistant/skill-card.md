## Description: <br>
小红书智能回复助手 analyzes Xiaohongshu comments for sentiment and intent, then drafts personalized reply suggestions and batch-processing guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiaoliuzhuan](https://clawhub.ai/user/xiaoliuzhuan) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Content creators, brand operators, MCN agencies, and developers use this skill to analyze Xiaohongshu comments, generate reply suggestions, manage comment history, and optionally monitor notes through Xiaohongshu API access. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Account-connected monitoring can require Xiaohongshu session credentials or tokens. <br>
Mitigation: Use offline drafting when possible, and do not provide web_session cookies or xsec_token values unless the implementation has been reviewed and its data handling is understood. <br>
Risk: The release references install scripts and API integration files that are not present in the reviewed artifact. <br>
Mitigation: Review any fetched or external scripts before execution, and avoid running install.sh or referenced integration code from another source without inspection. <br>
Risk: Generated replies may be inaccurate, inappropriate, or noncompliant with platform rules. <br>
Mitigation: Review reply suggestions manually before posting and follow Xiaohongshu platform rules, privacy expectations, and applicable laws. <br>


## Reference(s): <br>
- [Skill page](https://clawhub.ai/xiaoliuzhuan/xiaohongshu-reply-assistant) <br>
- [xiaohongshu-mcp](https://github.com/xpzouying/xiaohongshu-mcp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python and shell command examples, plus structured reply suggestions and reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include sentiment labels, intent categories, reply templates, batch reports, and configuration notes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
