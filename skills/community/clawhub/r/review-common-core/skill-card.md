## Description:

Provides shared review frameworks, checklists, fact-check categories, and JSON validators for review-oriented agent skills; it is used by other skills rather than run standalone.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mayf3](https://clawhub.ai/user/mayf3)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content-review skill authors use this shared core to reuse consistent editorial review principles, segment annotation guidance, holistic review checks, fact-check risk categories, and completion checklists across review workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Validator scripts can print checklist content to a terminal, which may be unsafe if the input JSON contains terminal-control characters.

Mitigation: Run validators only on trusted checklist JSON, or sanitize/capture terminal output in a safer viewer before review.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mayf3/skills/review-common-core)
- [Review Principles](references/review-principles.md)
- [Segment Annotation Framework](references/segment-annotation-framework.md)
- [Holistic Review Framework](references/holistic-review-framework.md)
- [Sensitivity Checklist](references/sensitivity-checklist.md)
- [Fact-Check Framework](references/fact-check-framework.md)
- [Dual-Host Dialogue Guide](references/dual-host-dialogue-guide.md)
- [Review Checker](references/review-checker.md)
- [Theme Consistency Checklist](references/theme-consistency-checklist.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance, JSON checklist structures, and terminal validation reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The bundled validator scripts read local checklist JSON and return pass/fail reports.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
