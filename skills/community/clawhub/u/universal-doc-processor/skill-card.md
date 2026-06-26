## Description: <br>
Processes uploaded documents across common formats, retains parsed files for multi-turn work, and waits for a clear user task before analyzing, editing, extracting, translating, or converting content. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cyril-ruidong](https://clawhub.ai/user/cyril-ruidong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to receive uploaded documents, keep them available during a session, ask for missing task details, and produce document analysis, edits, extraction, translation, conversion guidance, or processed files on demand. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Uploaded documents may be parsed and retained during multi-turn work, potentially until the stated 72-hour inactivity cleanup. <br>
Mitigation: Use the skill only in environments with acceptable upload controls and a clear deletion or reset process; avoid highly sensitive documents unless those controls are in place. <br>
Risk: Document processing can produce incorrect summaries, edits, translations, or extracted data. <br>
Mitigation: Review generated outputs before relying on them, especially for business, legal, financial, medical, or compliance-sensitive documents. <br>


## Reference(s): <br>
- [Universal Doc Processor on ClawHub](https://clawhub.ai/cyril-ruidong/universal-doc-processor) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Guidance] <br>
**Output Format:** [Plain text or Markdown messages, with processed document files when the task requires file output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May retain uploaded document content for multi-turn tasks until session cleanup.] <br>

## Skill Version(s): <br>
2.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
