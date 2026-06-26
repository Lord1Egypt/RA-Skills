## Description: <br>
Combines public web search and academic search into one intelligent AISA search mode for balanced retrieval across current web coverage and scholarly depth. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bibaofeng](https://clawhub.ai/user/bibaofeng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, developers, and agents use this skill to run blended web and academic searches through AISA when they need both broad public-web coverage and scholarly depth. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries, URLs, and extracted page content are sent to the remote AISA API. <br>
Mitigation: Use the skill only with information suitable for AISA, and do not submit secrets, private documents, authenticated pages, localhost URLs, or internal network URLs. <br>
Risk: The skill requires an AISA_API_KEY credential. <br>
Mitigation: Use a dedicated or rotatable key, keep it out of prompts and logs, and monitor usage. <br>
Risk: Search results and generated summaries can be incomplete or misleading. <br>
Mitigation: Review returned URLs, citations, and source content before relying on the results for decisions. <br>


## Reference(s): <br>
- [AISA](https://aisa.one) <br>
- [AISA API endpoint](https://api.aisa.one/apis/v1) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Terminal text with result titles, URLs, snippets, citations, usage details, and optional summaries.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AISA_API_KEY and network access to AISA API endpoints.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
