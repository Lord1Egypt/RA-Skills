## Description: <br>
Fix garbled text in PDF/SVG vector graphics caused by font encoding issues, making files editable in AI tools. Supports batch processing and JSON export for manual correction. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aipoch-ai](https://clawhub.ai/user/aipoch-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, designers, and document-processing teams use this skill to inspect PDF or SVG files with garbled vector text, identify repair candidates, and produce structured repair reports or editable JSON for manual correction. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review notes that the skill can report repaired PDF/SVG output paths even when those files were not actually written. <br>
Mitigation: Run it on copies of documents and verify that any expected output files exist and open correctly before relying on the result. <br>
Risk: JSON exports and repair reports may include extracted text from source documents. <br>
Mitigation: Treat exported JSON and reports as sensitive document data and store or share them only under the same controls as the original files. <br>
Risk: Runtime dependencies should be confirmed before use in an agent environment. <br>
Mitigation: Pin or verify Python dependencies before running the skill, and test the CLI on non-sensitive sample files first. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, JSON, guidance] <br>
**Output Format:** [Markdown repair report with CLI commands and optional JSON export] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports repaired, skipped, and unresolved text blocks with confidence values; verify any claimed PDF/SVG output files before relying on them.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
