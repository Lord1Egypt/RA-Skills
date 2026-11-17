## Description:

Rule Extractor extracts avoid and prefer rules from failure or success traces and learning notes, then formats them as prompt text, JSON, or Markdown.

This skill is ready for commercial/non-commercial use.

## Publisher:

[paudyyin](https://clawhub.ai/user/paudyyin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to turn traces and learning notes into avoid/prefer rules for review, documentation, and optional prompt integration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local Markdown headings and trace-derived patterns can become future system-prompt instructions without enough review.

Mitigation: Use only traces and learning files you control, and require human or trusted policy approval before generated prompt text is used in high-privilege agent sessions.

## Reference(s):

- [Rule Categories](references/rule_categories.md)

## Skill Output:

**Output Type(s):** [Text, JSON, Markdown, Guidance]

**Output Format:** [System prompt text, JSON array, or Markdown rule table]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Rules can include category, description, confidence, and source count.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
