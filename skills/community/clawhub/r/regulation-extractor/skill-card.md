## Description:

Extracts structured articles from construction-regulation PDFs, cleans OCR and formatting noise, writes JSON for review, and can sync the resulting records to Feishu Bitable.

This skill is ready for commercial/non-commercial use.

## Publisher:

[youfeijun123](https://clawhub.ai/user/youfeijun123)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations teams use this skill to convert Chinese construction-regulation PDFs into article-level JSON, run cleaning and quality checks, and optionally load reviewed records into Feishu Bitable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Feishu sync path can send extracted document text to Feishu and may expose Feishu secrets through command-line arguments.

Mitigation: Run sync only after confirming the documents may be shared with the target Feishu workspace; prefer local review first, avoid passing secrets in shared shells or CI logs, and use the documented dry-run mode before writing.

Risk: Cleaning scripts overwrite local JSON outputs in place.

Mitigation: Keep backups or work on copied JSON outputs before running cleaning, deep-cleaning, or quality-repair steps.

Risk: The Bitable sync script can delete duplicate records when delete-dupes is enabled.

Mitigation: Export or review existing Bitable records before enabling duplicate deletion, and avoid the delete option until the target table and deduplication behavior have been verified.

Risk: OCR and rule-based splitting can leave recognition errors, residual page or chapter noise, or imperfect long-article splits.

Mitigation: Manually review records marked as OCR errors, inspect long split articles, and run the quality check before using the data for retrieval or compliance workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/youfeijun123/skills/regulation-extractor)
- [Feishu Bitable schema reference](references/bitable-schema.md)
- [OCR error pattern reference](references/ocr-patterns.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands; scripts produce JSON article files, quality reports, and optional Feishu Bitable API writes.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Python scripts mutate local JSON outputs in place during cleaning and can make authenticated Feishu API calls when sync is invoked.]

## Skill Version(s):

3.0.0 (source: server release evidence and skill heading)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
