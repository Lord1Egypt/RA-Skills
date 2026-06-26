## Description: <br>
PubMed citation verifier that detects AI-fabricated PMID references with fuzzy matching against PubMed metadata. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[docsor1212](https://clawhub.ai/user/docsor1212) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, medical writers, evidence-based medicine teams, and developers use this skill to batch-verify PMID citations, detect invalid or mismatched references, and produce reports for human review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Private drafts or citation-derived search terms may be sent to PubMed or Crossref when verification, DOI checks, or suggestions are enabled. <br>
Mitigation: Review the selected source path before running, avoid suggestion or DOI checks for sensitive drafts when appropriate, and sanitize citation text before external lookups. <br>
Risk: PubMed metadata may be stored in a local SQLite cache. <br>
Mitigation: Use --no-cache for sensitive projects or clear the local cache after verification. <br>


## Reference(s): <br>
- [PubMed E-utilities API Quick Reference](references/api_examples.md) <br>
- [ClawHub Pubmed Verifier release](https://clawhub.ai/docsor1212/pubmed-verifier) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, code, guidance, files] <br>
**Output Format:** [Markdown guidance with CLI commands and optional HTML, JSON, or text report files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May query PubMed and Crossref, may cache PubMed metadata locally, and can generate reports for citation review.] <br>

## Skill Version(s): <br>
2.1.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
