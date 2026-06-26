## Description: <br>
Monitor journals precisely via ISSN lookup to track new PubMed papers with bilingual titles and detailed metadata. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chenghan66](https://clawhub.ai/user/chenghan66) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, clinicians, and literature-monitoring teams use this skill to check specified journals for recent PubMed articles, retrieve PMID, year, author, title, and abstract metadata, and produce bilingual English and Chinese title output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: PubMed search terms are sent to NCBI through Biopython Entrez calls. <br>
Mitigation: Avoid submitting sensitive or confidential journal-monitoring terms, and review organizational policy before use. <br>
Risk: The monitoring script uses an embedded Entrez contact email. <br>
Mitigation: Replace the hardcoded email with an approved configured contact address before regular use. <br>
Risk: Large result sets can trigger creation of a local Desktop report. <br>
Mitigation: Ask for user consent before writing reports locally and confirm the intended output location. <br>
Risk: The skill installs and depends on Biopython. <br>
Mitigation: Install dependencies from trusted package sources in an isolated environment. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown summaries with bilingual article entries, JSON from the monitoring script, shell commands for dependency setup, and optional local report files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and Biopython; may send PubMed search terms to NCBI and create a Desktop report for large result sets.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
