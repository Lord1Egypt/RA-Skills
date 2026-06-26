## Description: <br>
Retrieves Chinese finance news, A-share market updates, macroeconomic developments, market hotspots, finance articles, and listed-company announcements through the public Shenlan News API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qxsclass](https://clawhub.ai/user/qxsclass) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to look up current Chinese financial news, market sentiment, trending finance articles, and listed-company announcements. It is useful for time-sensitive finance questions and topic search across Shenlan News content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Finance-news searches and query terms are sent to shenlannews.com. <br>
Mitigation: Use the skill only where outbound requests to the declared Shenlan News domain are acceptable, and restrict network egress in stricter environments. <br>
Risk: The skill may use Bash to run the provided Python API helper. <br>
Mitigation: Review helper commands before execution and keep use limited to the disclosed read-only API calls. <br>


## Reference(s): <br>
- [Shenlan News](https://www.shenlannews.com) <br>
- [API Reference](references/api-reference.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/qxsclass/shenlannews) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, shell commands, guidance] <br>
**Output Format:** [Markdown summaries with optional JSON results from API helper commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses public Shenlan News endpoints and may include article links, dispatch timestamps, AI summaries, sentiment fields, and announcement references.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
