## Description: <br>
Automatically scans document reference lists and checks citations against retraction data sources. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aipoch-ai](https://clawhub.ai/user/aipoch-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, reviewers, editors, and research-support teams use this skill to scan manuscripts, bibliographies, PDFs, BibTeX, plaintext, or URLs for citations that may be retracted, corrected, or subject to concern. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Reference checks require outbound lookups to services such as Crossref, PubMed, and Open Retractions. <br>
Mitigation: Use only with documents and bibliographies that may be shared with those services, and avoid confidential manuscripts, sensitive bibliographies, signed URLs, or internal URLs without stronger privacy controls. <br>
Risk: Untrusted PDFs and the declared PyPDF2 dependency can introduce parsing and dependency risk. <br>
Mitigation: Run the skill in a constrained environment for untrusted PDFs and prefer pinning or replacing the PyPDF2 dependency before broad use. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/aipoch-ai/retraction-watcher) <br>
- [Publisher Profile](https://clawhub.ai/user/aipoch-ai) <br>
- [Audit Reference](references/audit-reference.md) <br>
- [Retraction Watch](https://retractionwatch.com/) <br>
- [Crossref API](https://api.crossref.org/) <br>
- [PubMed E-utilities](https://www.ncbi.nlm.nih.gov/home/develop/api/) <br>
- [Open Retractions](https://openretractions.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown report with status categories, citation findings, assumptions, risks, and recommended actions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include detailed or summary reporting depending on the requested workflow.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
