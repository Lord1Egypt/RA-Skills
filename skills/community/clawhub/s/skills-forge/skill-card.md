## Description:

Detect repeated capability gaps, convert recurring user needs into candidate skills, scaffold new OpenClaw-compatible skills, and validate them before installation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sheepxux](https://clawhub.ai/user/sheepxux)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use Skill Forge to turn recurring failures, feature requests, and repeatable workflows into reviewed skill candidates. It helps detect opportunities, scaffold skills, validate quality, evaluate candidates, and route installation or evolution through approval gates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Update and uninstall flows have safety gaps that could persist unsafe instructions or delete the wrong files.

Mitigation: Use the skill only in a controlled workspace, prefer plan-only mode, and review generated or evolved skill folders before approval.

Risk: Scheduled or Telegram-approved mutations can change installed skills when the local install manifest or feedback source is not trusted.

Mitigation: Do not enable scheduled or Telegram-approved mutations unless the install manifest and feedback source are trusted.

Risk: Generic environment discovery can expose unrelated secrets to approval or reporting flows.

Mitigation: Use a dedicated Telegram environment file that contains only Telegram values.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/sheepxux/skills/skills-forge)
- [Forge Console](references/forge-console.md)
- [Milestone Architecture](references/milestone-architecture.md)
- [Detection Heuristics](references/heuristics.md)
- [Skill Quality Rubric](references/skill-quality-rubric.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with command examples and JSON or text output from bundled scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Plan-only by default; install, uninstall, scheduled, and Telegram-approved mutation paths require explicit review and approval.]

## Skill Version(s):

1.4.0 (source: server release evidence and SKILL.md current version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
