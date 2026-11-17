## Description:

文献搜索工具 helps agents search scholarly literature, retrieve article details and full text by PMCID, manage references, analyze literature relationships, evaluate journal quality, and summarize results for academic research workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cainingnk](https://clawhub.ai/user/cainingnk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and AI-assistant builders use this skill to route literature-search requests to XiaoBenYang-backed tools for article metadata, full text retrieval, references, citation relationships, and journal-quality signals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores the XiaoBenYang API key in a local plaintext .env file.

Mitigation: Use a disposable or narrowly scoped key, keep .env out of source control and backups, and rotate the key if it may have been exposed.

Risk: Literature queries and requested article identifiers are sent to an external API service.

Mitigation: Avoid submitting sensitive unpublished research queries unless the user is comfortable sharing them with that service.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cainingnk/skills/xby-article)
- [XiaoBenYang API key page](https://xiaobenyang.com)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, guidance]

**Output Format:** [Markdown summaries and guidance derived from structured JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can return article metadata, full-text sections, reference lists, citation relationships, and journal quality metrics; full-text retrieval requires PMCID values.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
