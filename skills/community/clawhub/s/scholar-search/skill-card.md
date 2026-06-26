## Description: <br>
Unified academic search across arXiv and Semantic Scholar. Supports topic search, latest preprints, paper/author lookup, citation analysis, and structured output from core endpoints. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xxxxxxxxxxxxxxxxxxx20gex](https://clawhub.ai/user/xxxxxxxxxxxxxxxxxxx20gex) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and research assistants use this skill to search arXiv and Semantic Scholar, retrieve paper and author metadata, inspect citation networks, and produce structured literature-search summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The helper script can store a Semantic Scholar API key in scripts/.env and overwrite an existing value. <br>
Mitigation: Prefer setting S2_API_KEY through the shell or a secret manager; if scripts/.env is used, keep it out of version control and rotate the key if it is exposed. <br>


## Reference(s): <br>
- [arXiv API reference](references/arxiv-api-reference.md) <br>
- [Semantic Scholar API reference](references/semantic-scholar-api-reference.md) <br>
- [arXiv Legacy API User Manual](https://info.arxiv.org/help/api/user-manual.html) <br>
- [Semantic Scholar Paper Data API](https://api.semanticscholar.org/api-docs/#tag/Paper-Data) <br>
- [Semantic Scholar Author Data API](https://api.semanticscholar.org/api-docs/#tag/Author-Data) <br>
- [Semantic Scholar Graph API Swagger](https://api.semanticscholar.org/graph/v1/swagger.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and structured paper metadata] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include external paper metadata, links, abstracts, citation counts, author details, and API error messages returned by arXiv or Semantic Scholar.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
