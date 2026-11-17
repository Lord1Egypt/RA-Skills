## Description:

Grades how AI-generated or poorly architected a codebase appears, producing a Slop Percentage, tier ranking, cited findings, fix-it prompts, JSON artifacts, and a local HTML report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aidan945](https://clawhub.ai/user/aidan945)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to run a fast codebase quality scan, combine deterministic repository metrics with a sampled review pass, and generate cited findings plus fix-it prompts for follow-up refactoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can perform repo-wide local code analysis and generate files without a separate consent gate.

Mitigation: Confirm the intended target repository before running it, use a disposable checkout for sensitive or unfamiliar code, and review generated files before sharing them.

Risk: The generated HTML report has a script-injection risk from untrusted repository data.

Mitigation: Avoid running it on untrusted repositories until report data embedding is fixed, or open the report cautiously in an isolated environment.

Risk: The workflow may start a temporary localhost report server.

Mitigation: Stop the local server when finished and avoid exposing the generated report beyond the local machine.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aidan945/skills/slop-check)
- [HEURISTICS.md](artifact/references/HEURISTICS.md)
- [SCORING.md](artifact/references/SCORING.md)
- [REPORT-SCHEMA.md](artifact/references/REPORT-SCHEMA.md)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, HTML, shell commands, guidance]

**Output Format:** [Chat verdict plus JSON metrics and report data, a self-contained HTML report, and Markdown fix-it prompts.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node 18+. The workflow can write .slop-check/metrics.json, .slop-check/slop-map.json, .slop-check/report-data.json, and slop-report.html, and can serve the report on localhost.]

## Skill Version(s):

1.2.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
