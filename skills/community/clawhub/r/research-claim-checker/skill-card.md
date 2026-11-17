## Description:

Research Claim Checker helps review research or analysis claims against supplied evidence and identify gaps in the evidence chain.

This skill is ready for commercial/non-commercial use.

## Publisher:

[52yuanchangxing](https://clawhub.ai/user/52yuanchangxing)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, analysts, reviewers, and developers use this skill to turn supplied analysis drafts, claims, and evidence summaries into a structured claim-support review with evidence gaps, needed follow-up evidence, revision suggestions, and confidence judgments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The output can look like an evidence-verification result even though the skill works from the user's supplied materials and is not a final truth determination.

Mitigation: Use the report as a structured review draft, confirm source material independently, and avoid treating it as a replacement for peer review.

Risk: The local helper reads the input path and may write an output report when requested.

Mitigation: Review inputs for sensitive information before use and direct output to an intended local path.

Risk: Dormant audit modes exist beyond the default structured claim-review workflow.

Mitigation: Document or remove unused audit modes before relying on the skill in stricter deployment environments.

## Reference(s):

- [ClawHub skill release page](https://clawhub.ai/52yuanchangxing/skills/research-claim-checker)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Structured Markdown or JSON report, with optional local shell command usage when execution is available]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local input only; requires python3 for the bundled script and has no additional third-party dependencies.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
