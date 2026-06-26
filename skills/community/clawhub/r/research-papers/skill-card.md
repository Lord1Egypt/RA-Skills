## Description: <br>
Searches academic papers with OpenAlex for paper discovery, DOI lookup, citation-chain inspection, open-access PDF discovery or download, and Markdown literature review generation, with defaults tailored to neuroimaging and neurodegenerative disease classification. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zjuncher](https://clawhub.ai/user/zjuncher) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, researchers, and developers use this skill to find, rank, summarize, and review academic literature, especially for dynamic brain network modeling, fMRI neuroimaging, graph neural networks, and neurodegenerative disease classification. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends search terms, DOI lookups, and related research queries to OpenAlex and Unpaywall and stores cache or output files locally. <br>
Mitigation: Avoid sensitive unpublished research terms when using external APIs, review generated files before sharing, and clear local cache or output directories when needed. <br>
Risk: The optional QQBot handoff can run a separate staging script and transfer generated review files outside the core research workflow. <br>
Mitigation: Use QQBot handoff only when the separate tooling and destination are trusted, and verify the staging script path before enabling the option. <br>
Risk: Paper summaries, citation counts, open-access links, and literature-review synthesis may be incomplete or stale because they depend on third-party scholarly indexes. <br>
Mitigation: Verify important papers, metadata, citations, and access rights against primary sources before relying on the review. <br>


## Reference(s): <br>
- [OpenAlex API](https://api.openalex.org) <br>
- [Unpaywall API](https://api.unpaywall.org/v2) <br>
- [DOI Resolver](https://doi.org/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, files, guidance] <br>
**Output Format:** [Plain text or JSON search results, Markdown literature reviews, and shell commands for running the bundled research script.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can write Markdown review files and locally cache API responses and generated outputs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
