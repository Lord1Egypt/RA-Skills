## Description:

Detect AI-generated writing patterns in developer text, including docs, docstrings, commit messages, PR descriptions, and code comments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anderskev](https://clawhub.ai/user/anderskev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering reviewers use this skill to scan repository text for AI-like writing patterns and receive evidence-backed rewrite guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad scans can inspect repository text such as docs, comments, docstrings, commit messages, and PR bodies.

Mitigation: Run the skill against a specific path or category when broad coverage is not intended, and use --all only for whole-codebase scans.

Risk: Rewrite suggestions can change tone or meaning if applied without review.

Mitigation: Review each finding and suggestion before applying edits, especially items marked as needing review.

Risk: The skill writes a local .beagle/ai-writing-review.json report.

Mitigation: Check the report contents before sharing repository artifacts outside the review workflow.

## Reference(s):

- [Content Patterns](references/content-patterns.md)
- [Vocabulary Patterns](references/vocabulary-patterns.md)
- [Formatting Patterns](references/formatting-patterns.md)
- [Communication Patterns](references/communication-patterns.md)
- [Filler Patterns](references/filler-patterns.md)
- [Code Documentation Patterns](references/code-docs-patterns.md)
- [ClawHub Skill Page](https://clawhub.ai/anderskev/skills/review-ai-writing)
- [Publisher Profile](https://clawhub.ai/user/anderskev)

## Skill Output:

**Output Type(s):** [Analysis, Files, Markdown, Shell commands, Guidance]

**Output Format:** [JSON report file plus Markdown summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes .beagle/ai-writing-review.json with findings, categories, source locations, suggestions, risk levels, and fix safety.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
