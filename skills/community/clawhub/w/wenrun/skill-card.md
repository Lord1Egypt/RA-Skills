## Description:

WenRun analyzes Chinese writing for template-like AI text patterns and provides naturalness scores, issue locations, and improvement suggestions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wwumit](https://clawhub.ai/user/wwumit)

### License/Terms of Use:

MIT-0

## Use Case:

External users, writers, editors, and developers use this skill to check Chinese articles, reports, social posts, and local files for AI-like wording before publication or upload. It returns naturalness scores and localized findings that guide manual revision.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The analysis is heuristic and may produce false positives or miss AI-generated text.

Mitigation: Treat scores and findings as review aids, not proof; have a human review final wording and publication decisions.

Risk: Broad trigger terms may invoke the skill during ordinary writing requests.

Mitigation: Use it when the user explicitly asks for Chinese AI-style detection, naturalness scoring, or polishing guidance.

Risk: File analysis reads the local file path supplied by the user.

Mitigation: Review the target path before execution and avoid pointing it at unrelated or sensitive files.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/wwumit/skills/wenrun)
- [README](artifact/README.md)
- [Chinese AI Text Feature Patterns](artifact/features/ai-patterns.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown or terminal text with optional JSON analyzer output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local file analysis reads the file path supplied by the user; no network output is indicated by the evidence.]

## Skill Version(s):

1.1.1 (source: server release metadata; artifact frontmatter and package.json report 1.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
