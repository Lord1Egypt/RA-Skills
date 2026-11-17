## Description:

Download PDFs from PubMed Central (PMC) and Europe PMC using PMC ID, PubMed URL, PMID, or DOI, with support for single and batch downloads.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xuyuan0805](https://clawhub.ai/user/xuyuan0805)

### License/Terms of Use:


## Use Case:

Developers, researchers, and agents use this skill to download open-access academic paper PDFs from PubMed Central or Europe PMC from supported publication identifiers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A crafted filename can write outside the intended download directory or overwrite an existing PDF.

Mitigation: Use only simple basename filenames without slashes or `..`, choose a dedicated output folder, and prevent accidental overwrites before running the downloader.

Risk: Untrusted text could choose unsafe `--filename` or `--output` values.

Mitigation: Keep identifier, filename, and output-directory choices under trusted operator control, especially in automated or batch runs.

Risk: Unpinned dependencies can change downloader behavior over time.

Mitigation: Run in a dedicated virtual environment and pin required dependencies before deployment.

## Reference(s):

- [NCBI PMCID Converter API](https://pmc.ncbi.nlm.nih.gov/tools/idconv/api/v1/articles/)
- [NCBI ID Converter API](https://www.ncbi.nlm.nih.gov/pmc/utils/idconv/v1.0/)
- [ClawHub Skill Page](https://clawhub.ai/xuyuan0805/skills/xy-pubmed-pdf-downloader)

## Skill Output:

**Output Type(s):** [text, shell commands, files, guidance]

**Output Format:** [Markdown guidance with inline shell commands and downloaded PDF files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates PDF files in the selected output directory and prints download status or error messages.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
