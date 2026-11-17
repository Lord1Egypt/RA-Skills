## Description:

Skill Quality Checker evaluates installed OpenClaw skills across five quality dimensions and produces scoring reports with improvement suggestions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shaozhengmao](https://clawhub.ai/user/shaozhengmao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill maintainers use this skill to scan one or more local OpenClaw skills, review heuristic quality scores, and prioritize improvements before release or manual review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The checker reads local skill files from the selected scan path.

Mitigation: Review the --scan-dir or --skill path before running and point it only at skill directories intended for inspection.

Risk: Using --output can create or overwrite a report file at the provided path.

Mitigation: Use --output only for report locations intended to be created or overwritten, or omit it to print results to the terminal.

Risk: Static heuristic scores can miss context that a human reviewer would catch.

Mitigation: Treat the report as a screening aid and perform manual review before deployment or publication decisions.

## Reference(s):

- [Scoring Criteria](references/scoring-criteria.md)
- [ClawHub Skill Page](https://clawhub.ai/shaozhengmao/skills/skill-quality-checker)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, guidance]

**Output Format:** [Markdown or JSON report, with optional terminal output or file output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses Python standard library static analysis; reports are heuristic and should not replace human review.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
