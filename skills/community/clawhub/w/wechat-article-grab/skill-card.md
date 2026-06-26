## Description: <br>
Fetches, searches, compares, and summarizes WeChat public account articles from shared article links, account names, or trending keywords. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[one2agi](https://clawhub.ai/user/one2agi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to retrieve WeChat article text, list recent account articles, query trending articles by keyword, compare account performance, and prepare article summaries or analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use a WeChat session cookie, which should be treated as an account credential. <br>
Mitigation: Remove bundled cookie values, restrict file permissions on skill.env, rotate or delete cookies after use, and install only when this credential access is acceptable. <br>
Risk: Some searches use external aggregation services and may return incomplete, delayed, or third-party article metrics. <br>
Mitigation: Verify important results against the original article or trusted sources before relying on trend, statistics, or account-comparison output. <br>
Risk: The security scan flags insecure TLS/SNI-bypass network behavior that users should review before sensitive use. <br>
Mitigation: Review the network code, run the skill in a restricted environment, and avoid using it for sensitive workflows unless the behavior is acceptable. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown or plain text with article links, summaries, metrics, comparisons, and command examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include fetched article content, interaction metrics, account comparisons, keyword trend results, and follow-up search guidance.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
