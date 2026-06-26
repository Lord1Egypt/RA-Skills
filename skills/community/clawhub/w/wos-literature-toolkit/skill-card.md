## Description: <br>
WOS Literature Toolkit helps agents launch a web interface to search Web of Science, export literature metadata to Excel, and coordinate PDF downloads through configured academic and open-access sources. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[grizzlyccc](https://clawhub.ai/user/grizzlyccc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, librarians, and agents supporting literature reviews use this skill to run WOS searches, collect metadata exports, and coordinate batch PDF retrieval from one web interface. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Browser automation may use persistent institutional WOS session cookies. <br>
Mitigation: Confirm the user intends to use WOS automation, review where cookies are stored, and delete saved cookies when institutional access should no longer persist. <br>
Risk: Paper metadata and DOI queries may be sent to third-party PDF retrieval sources. <br>
Mitigation: Confirm acceptable download sources with the user before batch retrieval and prefer scoped WOS-only or open-access requests when required. <br>
Risk: Bulk crawling or downloading may exceed site, publisher, or institutional policies. <br>
Mitigation: Require explicit user confirmation for crawl scope and output location before starting unattended crawling or bulk downloads. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/grizzlyccc/wos-literature-toolkit) <br>
- [Publisher profile](https://clawhub.ai/user/grizzlyccc) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with inline shell commands and web UI workflow steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create Excel metadata exports and PDF files in a user-selected output directory.] <br>

## Skill Version(s): <br>
1.1.2 (source: server release metadata; artifact frontmatter reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
