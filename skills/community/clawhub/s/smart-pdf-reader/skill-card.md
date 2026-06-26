## Description: <br>
Smart PDF Reader helps agents extract and summarize PDF content, including scanned and complex documents, through the mineru-open-api CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[veeicwgy](https://clawhub.ai/user/veeicwgy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and document-review users use this skill to read, extract, and summarize content from PDFs, including scanned files, academic papers, reports, legal documents, and multilingual documents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill relies on a third-party CLI/API that may process PDF contents outside the agent environment. <br>
Mitigation: Verify the mineru-open-api package and source before installing, and avoid confidential PDFs unless MinerU privacy and retention practices are acceptable. <br>
Risk: Extracted document content may be saved locally in output directories. <br>
Mitigation: Prefer stdout mode for quick reads, choose output directories deliberately, and clean saved extracts when they are no longer needed. <br>


## Reference(s): <br>
- [Smart PDF Reader on ClawHub](https://clawhub.ai/veeicwgy/smart-pdf-reader) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown text extracted from PDFs, optional saved output files, and concise summaries or guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call mineru-open-api and may save extracted document content to a chosen or generated output directory.] <br>

## Skill Version(s): <br>
0.2.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
