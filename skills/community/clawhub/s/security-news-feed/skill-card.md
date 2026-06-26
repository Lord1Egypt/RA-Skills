## Description: <br>
Collects Korean security news from multiple sources, summarizes it with an LLM, and publishes the results to Notion with optional Tistory blog publishing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rebugui](https://clawhub.ai/user/rebugui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and security operators use this skill to monitor Korean security news, filter security-relevant articles, summarize them, and route the results into a Notion database or an optional Tistory blog. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can run unattended and publish externally using configured credentials. <br>
Mitigation: Use dedicated low-privilege credentials, a dedicated Notion database, and keep optional Tistory publishing disabled unless it is intentionally required. <br>
Risk: Article content may be sent to z.ai/GLM for summarization and analysis. <br>
Mitigation: Confirm the data-sharing posture is acceptable before enabling LLM summarization in production workflows. <br>
Risk: Notion archiving and file-upload behavior may change stored workspace content. <br>
Mitigation: Review or disable the 90-day Notion archiving and automatic file-upload behavior before scheduled use. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/rebugui/security-news-feed) <br>
- [Publisher profile](https://clawhub.ai/user/rebugui) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with command examples, configuration snippets, and generated article summaries.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces summarized news entries, detailed analysis, tags, source URLs, and publishing instructions for Notion and optional Tistory workflows.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence; artifact frontmatter reports 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
