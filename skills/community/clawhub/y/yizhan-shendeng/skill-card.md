## Description:

Turns books and other long-form material into actionable, reusable agent skills through extraction, source verification, and testing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qianyu6a](https://clawhub.ai/user/qianyu6a)

### License/Terms of Use:

MIT-0

## Use Case:

Writers, researchers, and developers use this skill to turn method-oriented books, transcripts, and long documents into callable skill packages rather than summaries. It screens source material, checks extracted claims against the source, and tests the resulting skills.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The long-running workflow writes many local files and can consume substantial compute or paid-model capacity.

Mitigation: Approve the working directory and a time or spending budget before starting; review progress before continuing large batches.

Risk: Account-balance checks and optional cross-channel notifications may access account or messaging services.

Mitigation: Confirm whether balance checks and notifications are permitted, and specify the intended channel before enabling them.

Risk: Optional installation or archival can move generated skills or source material beyond the working directory.

Mitigation: Leave installation and library archival disabled unless their destinations and contents have been reviewed.

## Reference(s):

- [Skill construction template](references/skill-template.md)
- [Quote verification guide](references/quote-verification.md)
- [Batch extraction playbook](references/batch-extraction-playbook.md)
- [Blind-test prompts template](references/test-prompts-template.md)

## Skill Output:

**Output Type(s):** [Markdown, Files, Guidance]

**Output Format:** [Markdown skill packages with source excerpts, test prompts, and progress records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes intermediate and final files to a working directory; installation is optional.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
