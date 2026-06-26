## Description: <br>
Download PDFs from PubMed Central (PMC) and Europe PMC for open-access academic papers using a PMC ID, PubMed URL, PMID, or DOI, with single and batch download modes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xuyuan0805](https://clawhub.ai/user/xuyuan0805) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, researchers, and academic workflow users can use this skill to download open-access PubMed Central PDFs from identifiers or lists of identifiers. It is useful for collecting papers from PMC and Europe PMC into a local output directory. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Custom filenames or output paths could overwrite files outside the intended download location. <br>
Mitigation: Use the default downloads folder or a dedicated output directory, and avoid absolute paths or parent-directory segments in --filename. <br>
Risk: Article identifiers may be sent to NCBI and Europe PMC during lookup and download. <br>
Mitigation: Use only identifiers that are appropriate to share with those external services. <br>
Risk: The helper script depends on the Python requests package and network downloads. <br>
Mitigation: Install and run the skill only in a Python environment you trust. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xuyuan0805/xy-pubmed-pdf-downloader) <br>
- [NCBI PMC ID Converter API](https://www.ncbi.nlm.nih.gov/pmc/utils/idconv/v1.0/) <br>
- [NCBI PMC ID Converter articles API](https://pmc.ncbi.nlm.nih.gov/tools/idconv/api/v1/articles/) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, code, files, guidance] <br>
**Output Format:** [Markdown guidance with shell commands; downloaded PDF files are written by the helper script.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The script supports a single identifier, a batch file, output directory selection, custom filenames, and PDF validation before keeping downloaded files.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
