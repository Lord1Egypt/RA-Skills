## Description: <br>
Extracts structured articles from construction regulation PDFs, cleans text and OCR artifacts, produces reviewable JSON, and can sync records to Feishu Bitable. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[youfeijun123](https://clawhub.ai/user/youfeijun123) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineering teams, and operations staff use this skill to extract article-level text from Chinese construction regulation PDFs, clean OCR and formatting issues, and prepare JSON records for human review or Feishu Bitable synchronization. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send extracted document content to Feishu Bitable using command-line application credentials. <br>
Mitigation: Use a least-privilege Feishu application, avoid exposing long-lived secrets in shell history or shared logs, and confirm the destination table before syncing. <br>
Risk: The sync workflow can create records and delete duplicate Bitable records when delete-dupes behavior is enabled. <br>
Mitigation: Run dry-run checks first, review records marked for synchronization or deletion, and use backups or staging tables for large updates. <br>
Risk: OCR output and long-article splitting may produce inaccurate text or imperfect boundaries. <br>
Mitigation: Human-review entries marked as OCR errors, inspect split long articles, and validate extracted regulation text before relying on it downstream. <br>
Risk: The quality-check script was flagged because it scans a hard-coded local path instead of the intended directory. <br>
Mitigation: Fix or avoid the quality-check script until it accepts the user-provided target directory. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/youfeijun123/regulation-extractor) <br>
- [Bitable schema reference](references/bitable-schema.md) <br>
- [OCR patterns reference](references/ocr-patterns.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, JSON] <br>
**Output Format:** [Markdown guidance with shell commands and JSON file outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated JSON contains article records, quality labels, chapter metadata, page references, and summary reports for human review or Feishu Bitable synchronization.] <br>

## Skill Version(s): <br>
3.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
