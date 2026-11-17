## Description:

Regex Master helps agents generate, explain, test, validate, replace, and extract text with regular expressions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kaiyuelv](https://clawhub.ai/user/kaiyuelv)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to construct regular expressions from natural-language descriptions, explain existing patterns, test matches, extract repeated data, and reuse common regex templates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Untrusted or very expensive regular expressions can cause regex denial-of-service behavior.

Mitigation: Avoid exposing test, extract, or replace methods directly to untrusted users unless regex timeouts, input length limits, or process isolation are added.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kaiyuelv/skills/regex-master)
- [artifact/README.md](artifact/README.md)
- [artifact/SKILL.md](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [Markdown and text containing regex patterns, Python examples, match results, and explanations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return Python dictionaries or lists for test, validation, extraction, and template lookup results.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
