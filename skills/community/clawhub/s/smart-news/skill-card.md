## Description:

Smart News helps agents call the Crypto News Analyzer HTTP API for async analysis jobs, semantic search, datasource management, intelligence operations, and health checks from OpenClaw.

This skill is ready for commercial/non-commercial use.

## Publisher:

[laceletho](https://clawhub.ai/user/laceletho)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and operators use Smart News to authenticate to the Crypto News Analyzer API, run crypto-news analysis and semantic search jobs, manage news and intelligence datasources, and maintain intelligence topics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An agent using this skill can call an authenticated external API with a bearer token.

Mitigation: Install only when the operator intends to grant that API access, and configure API_KEY only in the intended runtime environment.

Risk: Delete, archive, prompt-edit, topic-confirm, merge, and datasource association endpoints can change stored API state.

Mitigation: Require explicit operator confirmation before using state-changing or lifecycle-changing endpoints.

Risk: Telegram and V2EX datasources may collect or process third-party channel or forum content.

Mitigation: Configure only sources the operator is authorized to collect and process.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/laceletho/skills/smart-news)
- [Crypto News Analyzer API](https://news.tradao.xyz)
- [Analyze Workflow Reference](references/analyze-workflow.md)
- [Semantic Search Reference](references/semantic-search.md)
- [Datasource Management Reference](references/datasource-management.md)
- [Intelligence Query Reference](references/intelligence-query.md)
- [Operations and Maintenance Reference](references/operations-and-maintenance.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown guidance with JSON and bash/curl examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a configured bearer token in API_KEY; API responses may include JSON job metadata and Markdown reports.]

## Skill Version(s):

0.4.6 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
