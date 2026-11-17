## Description:

Read, explain, and evaluate a software repository or GitHub project in an engineering-oriented way for codebase understanding, architecture analysis, adoption review, onboarding notes, and risk-oriented engineering summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[9penny](https://clawhub.ai/user/9penny)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to quickly understand unfamiliar repositories, map stack and module boundaries, trace important execution paths, and judge maintainability or adoption risk. It supports quick-read, architecture, and takeover-review modes, with a lightweight public GitHub health layer when project adoption signals matter.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Repository analysis can be misleading when the requested scope, output mode, or target repository is ambiguous.

Mitigation: Clarify the repository scope and preferred output language when the request could be interpreted in multiple ways.

Risk: The skill may inspect local repository files and optionally public GitHub health signals when adoption context is requested.

Mitigation: Review the repository scope before use and avoid pointing it at directories containing unrelated sensitive material.

## Reference(s):

- [Repo Analysis Skill](artifact/SKILL.md)
- [Repo Analysis Output Templates](artifact/references/output-template.md)
- [Signals for Repo Analysis](artifact/references/signals.md)
- [Lightweight GitHub Health Layer](artifact/references/github-health.md)
- [Adapted Notes from Surveyed Skills](artifact/references/adapted-notes.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown engineering summary with evidence labels and optional command or code references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Output depth varies by requested mode: quick read, architecture analysis, or takeover review.]

## Skill Version(s):

0.4.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
