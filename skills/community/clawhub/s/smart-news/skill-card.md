## Description: <br>
Use when calling the Crypto News Analyzer HTTP API for async analysis jobs, semantic search, datasource management, intelligence operations, or health checks from OpenClaw. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[laceletho](https://clawhub.ai/user/laceletho) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to guide OpenClaw agents through authenticated crypto news analysis, semantic search, datasource management, intelligence topic workflows, and service health checks against the Smart News HTTP API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a bearer API key and can use it to call a crypto news service. <br>
Mitigation: Configure only the intended API key, prefer a scoped key where available, and do not send unauthenticated requests. <br>
Risk: Datasource deletion, topic archiving, and topic-datasource association changes can modify server-side resources. <br>
Mitigation: Review destructive or association-changing requests before execution and confirm the target datasource or topic identifiers. <br>
Risk: Telegram, V2EX, and REST datasource collection may ingest sensitive or deployment-specific content. <br>
Mitigation: Confirm each datasource is appropriate for the deployment and keep datasource credentials in environment-managed secrets. <br>


## Reference(s): <br>
- [Smart News ClawHub Page](https://clawhub.ai/laceletho/smart-news) <br>
- [Laceletho Publisher Profile](https://clawhub.ai/user/laceletho) <br>
- [Analyze Workflow Reference](references/analyze-workflow.md) <br>
- [Semantic Search Reference](references/semantic-search.md) <br>
- [Datasource Management Reference](references/datasource-management.md) <br>
- [Intelligence Query Reference](references/intelligence-query.md) <br>
- [Operations and Maintenance Reference](references/operations-and-maintenance.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with JSON and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include authenticated HTTP request patterns, polling steps, response interpretation, and configuration guidance.] <br>

## Skill Version(s): <br>
0.4.6 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
