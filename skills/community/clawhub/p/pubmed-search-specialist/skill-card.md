## Description: <br>
Builds complex Boolean query strings for precise PubMed/MEDLINE retrieval, including MeSH term mapping, advanced filters, citation searching, systematic review strategies, and clinical query optimization. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aipoch-ai](https://clawhub.ai/user/aipoch-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, clinicians, evidence review teams, and developers use this skill to build reproducible PubMed/MEDLINE Boolean search strategies with MeSH mapping, PICO-style concept decomposition, filters, and syntax validation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Language, date, human-only, or age filters can bias literature retrieval when they are added without a protocol reason. <br>
Mitigation: Apply filters only when the user request or review protocol explicitly justifies them, and document the rationale in the search strategy. <br>
Risk: Suggested MeSH terms may be incomplete or stale for current PubMed indexing. <br>
Mitigation: Verify MeSH terms against current NLM/PubMed sources before relying on the generated search. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/aipoch-ai/pubmed-search-specialist) <br>
- [MeSH Structure Guide](references/mesh-structure.md) <br>
- [Boolean Query Examples](references/boolean-examples.md) <br>
- [MeSH Browser](https://meshb.nlm.nih.gov/) <br>
- [NCBI MeSH](https://www.ncbi.nlm.nih.gov/mesh) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown or plain text search strategies, with optional JSON output from the packaged CLI] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces copy-paste-ready PubMed query strings, line-by-line search plans, MeSH suggestions, and validation feedback.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
