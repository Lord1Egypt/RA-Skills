## Description:

超能文献（Suppr）学术文献检索 API。当用户需要检索学术论文、查找 PubMed 文献、搜索研究资料时激活。

This skill is ready for commercial/non-commercial use.

## Publisher:

[zjg678](https://clawhub.ai/user/zjg678)

### License/Terms of Use:

MIT-0

## Use Case:

External users and research-focused agents use this skill to search PubMed literature with natural-language queries and request article metadata such as DOI, PMID, abstracts, publication details, citation counts, and impact factors.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries and Suppr API keys are sent to the hosted Suppr literature search service.

Mitigation: Use the skill only when that provider relationship fits the user's data-handling requirements, and avoid sending sensitive unpublished research questions or private data.

Risk: The skill depends on an external academic search API and may be affected by provider availability, authentication, or rate limits.

Mitigation: Confirm API credentials and handle non-zero API response codes, missing results, or rate-limit failures before relying on returned literature metadata.

## Reference(s):

- [Suppr API documentation](https://openapi.suppr.wilddata.cn/introduction.html)
- [Suppr homepage](https://suppr.wilddata.cn)
- [ClawHub skill page](https://clawhub.ai/zjg678/skills/suppr-academic-search-skills)

## Skill Output:

**Output Type(s):** [guidance, shell commands, API calls, markdown, JSON]

**Output Format:** [Markdown guidance with JSON examples and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides authenticated requests to the hosted Suppr semantic literature search API and describes returned article metadata.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
