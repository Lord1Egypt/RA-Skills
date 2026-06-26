## Description: <br>
超能文献（Suppr）学术文献检索 API。当用户需要检索学术论文、查找 PubMed 文献、搜索研究资料时激活。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zjg678](https://clawhub.ai/user/zjg678) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, students, and agents use this skill to search PubMed-backed academic literature with natural-language queries and retrieve paper metadata such as DOI, PMID, abstracts, citation counts, journal details, and impact factors. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Research queries and requested metadata are sent to Suppr's third-party API. <br>
Mitigation: Use a dedicated Suppr API key and avoid submitting confidential research queries unless the service's data handling is acceptable. <br>
Risk: Literature search results or AI-selected matches may be incomplete or not suitable as final evidence. <br>
Mitigation: Verify important papers, identifiers, citations, and abstracts against primary publication sources before relying on them. <br>
Risk: The artifact discloses a 60 requests per minute rate limit. <br>
Mitigation: Throttle automated searches and handle API errors or fewer-than-requested results gracefully. <br>


## Reference(s): <br>
- [Suppr API documentation](https://openapi.suppr.wilddata.cn/introduction.html) <br>
- [Suppr API base endpoint](https://api.suppr.wilddata.cn) <br>
- [ClawHub skill page](https://clawhub.ai/zjg678/suppr-academic-search-skills) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, JSON, API Calls] <br>
**Output Format:** [Markdown with HTTP request examples and JSON response fields] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Suppr API key; search results depend on the Suppr API and PubMed-backed retrieval.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
