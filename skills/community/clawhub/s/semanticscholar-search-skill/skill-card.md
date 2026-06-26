## Description: <br>
Searches Semantic Scholar for academic papers, paper details, author profiles, citations, and references with console or JSON output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[JackKuo666](https://clawhub.ai/user/JackKuo666) <br>

### License/Terms of Use: <br>
MIT License <br>


## Use Case: <br>
Researchers, students, and developers use this skill to search academic literature, inspect paper and author metadata, and gather citation or reference data through the Semantic Scholar API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Research queries, paper identifiers, and author identifiers are sent to Semantic Scholar. <br>
Mitigation: Avoid sensitive or confidential queries and review organizational data-sharing requirements before use. <br>
Risk: Third-party dependencies and installation commands can introduce normal supply-chain risk. <br>
Mitigation: Install in an isolated environment, prefer package-manager based installation, and pin dependencies when deploying. <br>
Risk: The optional output path can overwrite an existing file. <br>
Mitigation: Use a dedicated output directory and review file paths before running commands with --output. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/JackKuo666/semanticscholar-search-skill) <br>
- [Semantic Scholar](https://www.semanticscholar.org/) <br>
- [Semantic Scholar API Key](https://www.semanticscholar.org/product/api#api-key) <br>
- [semanticscholar PyPI package](https://pypi.org/project/semanticscholar/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Files, Shell commands] <br>
**Output Format:** [Console text or JSON, with optional JSON export files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Optional Semantic Scholar API key can be used for higher rate limits.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
