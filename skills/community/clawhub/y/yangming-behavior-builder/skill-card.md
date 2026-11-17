## Description:

阳明先生 is an AI agent skill-creation engine that researches a person's observable behavior, execution patterns, and outcomes to generate a behavior-perspective skill with friction-diagnosis guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kingsunzhang2026-oss](https://clawhub.ai/user/kingsunzhang2026-oss)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to analyze public or user-provided behavior evidence, extract behavior models and execution traits, and generate a reusable behavior-perspective skill. The generated skill can support self-calibration through knowledge-action friction diagnosis and practical improvement guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can over-activate when user intent resembles its broad trigger phrases.

Mitigation: Confirm the requested target person, purpose, scope, and whether a new or updated skill is needed before running the full workflow.

Risk: Generated persona-style outputs can be mistaken for statements from real people.

Mitigation: Label outputs as AI-generated behavioral interpretations and avoid presenting them as the target person's actual advice or endorsement.

Risk: Behavior narratives and diagnosis logs may contain sensitive personal, workplace, financial, or medical details.

Mitigation: Use only trusted workspaces, redact private details, and disable or avoid retained logs for sensitive scenarios.

Risk: Agent-driven research and local file creation can introduce inaccurate or misleading guidance into generated skills.

Mitigation: Review source quality, generated files, diagnostic scripts, and security scan results before installing or sharing generated skills.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kingsunzhang2026-oss/skills/yangming-behavior-builder)
- [README](README.md)
- [Friction diagnosis script](scripts/friction_diagnosis.py)
- [Andrew Ng behavior example skill](references/andrew-ng-behavior/SKILL.md)
- [Karpathy behavior example skill](references/karpathy-behavior/SKILL.md)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown skill files, Python scripts, diagnostic reports, and concise guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated skills may create local research, source, script, and log files; execution logs can retain user behavior narratives.]

## Skill Version(s):

1.2.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
