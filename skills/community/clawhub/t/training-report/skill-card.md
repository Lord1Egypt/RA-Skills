## Description:

Produces structured training and workshop reports by interviewing the trainer, drafting a canonical Markdown report, and generating a final .docx after approval.

This skill is ready for commercial/non-commercial use.

## Publisher:

[samber](https://clawhub.ai/user/samber)

### License/Terms of Use:

MIT-0

## Use Case:

Trainers, learning and development teams, consultants, and managers use this skill to document training sessions, workshops, onboarding events, participant observations, recommendations, annexes, and follow-up actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Training reports may include named participant observations, survey summaries, annexes, and trainer contact details.

Mitigation: Collect and include personal or sensitive information only when authorized, use diplomatic group-level wording when appropriate, and review the report before sharing.

Risk: The workflow overwrites a single canonical Markdown draft during iteration.

Mitigation: Keep a separate copy when draft history is required and review the current Markdown before generating the Word document.

Risk: The final .docx is a derivative generated after approval and may need regeneration if content changes.

Mitigation: Approve the Markdown source first, then regenerate the .docx from the updated Markdown instead of editing the Word file directly.

## Reference(s):

- [Training Report Skill Page](https://clawhub.ai/samber/skills/training-report)
- [Publisher Profile](https://clawhub.ai/user/samber)
- [Project Homepage from ClawHub Metadata](https://github.com/samber/cc-skills)
- [Tone of Voice Reference](artifact/references/tone-of-voice.md)
- [Markdown Draft Reference](artifact/references/markdown-draft.md)
- [DOCX Generation Reference](artifact/references/docx-generation.md)

## Skill Output:

**Output Type(s):** [text, markdown, files, guidance]

**Output Format:** [Markdown draft plus final .docx file after user approval]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The Markdown draft is the canonical editable artifact; the .docx is generated once after approval.]

## Skill Version(s):

1.0.1 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
