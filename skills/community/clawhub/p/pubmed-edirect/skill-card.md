## Description: <br>
Search and retrieve literature from PubMed using NCBI's EDirect command-line tools. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[killgfat](https://clawhub.ai/user/killgfat) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users, developers, and researchers use this skill to search PubMed and related NCBI databases, retrieve abstracts or structured records, and build repeatable literature-review or publication-analysis command workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Manual installation requires downloading and running command-line tooling outside the agent. <br>
Mitigation: Download EDirect only from the official NCBI source, review the installer before execution, and avoid running installation commands as root. <br>
Risk: NCBI API keys or email addresses may be stored in shell configuration. <br>
Mitigation: Treat NCBI_API_KEY and NCBI_EMAIL as sensitive local configuration and avoid exposing them in shared logs, prompts, or repositories. <br>
Risk: Examples and bundled scripts contact NCBI and can create or overwrite local output files. <br>
Mitigation: Run commands in a dedicated workspace, review output paths before execution, and set conservative request delays to respect service limits. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/killgfat/pubmed-edirect) <br>
- [NCBI EDirect Documentation](https://www.ncbi.nlm.nih.gov/books/NBK179288/) <br>
- [NCBI EDirect Installer](https://ftp.ncbi.nlm.nih.gov/entrez/entrezdirect/install-edirect.sh) <br>
- [NCBI Home](https://www.ncbi.nlm.nih.gov/) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, Code] <br>
**Output Format:** [Markdown with inline bash commands and shell-script examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May generate local text or CSV files when users run the provided scripts.] <br>

## Skill Version(s): <br>
0.4.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
