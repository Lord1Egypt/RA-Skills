## Description: <br>
Extract structured data from construction specifications, including CSI sections, requirements, submittals, and product data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[datadrivenconstruction](https://clawhub.ai/user/datadrivenconstruction) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Construction project managers, estimators, procurement teams, and developers use this skill to turn user-provided specification documents into structured section summaries, submittal logs, product schedules, and referenced-standard lists. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads construction specification files explicitly provided by the user, which may contain private project information. <br>
Mitigation: Provide only the intended specification files or paths, avoid unrelated private documents, and review outputs before sharing. <br>
Risk: Extracted sections, submittals, products, or standards may be incomplete or need professional review before operational use. <br>
Mitigation: Validate extracted tables and reports against the original specifications before using them for estimating, procurement, or compliance decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/datadrivenconstruction/specification-extractor) <br>
- [Data Driven Construction homepage](https://datadrivenconstruction.io) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown tables and reports, Python code snippets, and optional CSV, Excel, or JSON exports.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user-provided project data or file paths; Python 3 and pdfplumber are needed for PDF extraction.] <br>

## Skill Version(s): <br>
2.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
