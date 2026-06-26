## Description: <br>
Searches Web of Science, extracts paper metadata, and helps download open-access PDFs for environmental psychology and related literature reviews. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ziyi-z-z](https://clawhub.ai/user/ziyi-z-z) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, students, and literature-review authors with valid Web of Science access use this skill to build search queries, parse exported records, identify open-access versions, and organize downloaded paper metadata and files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends paper DOIs to Unpaywall and may download PDFs to a local directory. <br>
Mitigation: Use it only when DOI lookup through Unpaywall is acceptable and choose an output directory suitable for downloaded academic files. <br>
Risk: Web of Science and publisher content may be subject to institutional access terms, copyright restrictions, and download limits. <br>
Mitigation: Run it only within the user's authorized Web of Science access and follow institutional, publisher, and copyright rules for downloaded or manually retrieved papers. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ziyi-z-z/wos-paper-downloader) <br>
- [Web of Science Advanced Search Guide](references/wos_search_guide.md) <br>
- [DOI Resolver and Open Access Detection](references/doi_resolver.md) <br>
- [Unpaywall API](https://api.unpaywall.org/v2/{doi}?email={your_email}) <br>
- [Web of Science](https://www.webofscience.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Files, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with command examples plus local CSV, JSON, TXT, and PDF files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes results to a local output directory, including metadata.csv, papers.json, download_list.txt, and open-access PDF files when available.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
