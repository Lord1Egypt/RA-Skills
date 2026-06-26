## Description: <br>
Routes user requests to likely agent skills using BM25, bilingual embedding retrieval, reciprocal-rank fusion, rejection rules, and optional multi-skill chain planning. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[awoo129](https://clawhub.ai/user/awoo129) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to select the most relevant skill from a large mixed-language skill library, reject pure information queries, and propose multi-skill workflows when a request spans several capabilities. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The router may recommend multi-skill plans or fallback commands that are too broad for the user request. <br>
Mitigation: Review the suggested skill, chain steps, and fallback path before execution, and require an explicit human selection when the recommendation is ambiguous. <br>
Risk: Fallback actions can involve email, downloads, browser automation, account APIs, or credential-backed services. <br>
Mitigation: Require explicit confirmation before those actions and run the skill where environment variables and credentials are controlled. <br>
Risk: The first run may download an embedding model and the fallback layer may use local or external model providers. <br>
Mitigation: Use approved model mirrors or cached models, and control network access for model downloads and fallback model endpoints. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/awoo129/yan-skill-router) <br>
- [Project Homepage](https://github.com/awoo129/wangyan) <br>
- [Rejection Word Lists](references/noise-words.md) <br>
- [Translation Bridge Map](references/zh2en-map.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text routing recommendations with markdown-style candidate blocks, rejection messages, and optional chain plans.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include top-k skill rankings, relevance scores, query-profile metadata, step dependencies, fallback guidance, and command snippets for downstream tools.] <br>

## Skill Version(s): <br>
2.1.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
