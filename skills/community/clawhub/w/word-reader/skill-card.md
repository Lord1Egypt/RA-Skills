## Description: <br>
Reads Word documents in .docx and .doc formats and extracts text, tables, metadata, and image information. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xtfnhcyjpgf](https://clawhub.ai/user/xtfnhcyjpgf) <br>

### License/Terms of Use: <br>
MIT License <br>


## Use Case: <br>
Developers and document-processing users use this skill to inspect Word files, extract document content, convert content to text, JSON, or Markdown, and batch-process directories of Word documents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The installer may install Python packages or optional system packages, including commands that can require elevated privileges. <br>
Mitigation: Install dependencies in a virtual environment or managed machine image, and avoid running installer steps with elevated privileges unless the package sources are trusted. <br>
Risk: The skill reads document contents and metadata and can save extracted results locally. <br>
Mitigation: Process only documents whose contents and metadata are appropriate to expose to the agent and store in the selected output location. <br>


## Reference(s): <br>
- [python-docx documentation](https://python-docx.readthedocs.io/) <br>
- [ClawHub skill page](https://clawhub.ai/xtfnhcyjpgf/word-reader) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, files] <br>
**Output Format:** [Plain text, JSON, or Markdown, with optional file output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can process a single Word file or batch-process a directory; .doc support depends on optional antiword installation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
