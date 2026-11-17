## Description:

Fast 10-iteration security spot-check for pre-deployment or daily checks covering secrets, OWASP basics, authentication, rate limiting, and containers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dorukardahan](https://clawhub.ai/user/dorukardahan)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to run a quick security spot-check before deployment, during daily hygiene reviews, or after verifying a specific fix.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads project files while performing security spot-checks.

Mitigation: Use it only in workspaces where project-file inspection by the agent is acceptable.

Risk: Pattern-match findings may include false positives or inconclusive results.

Mitigation: Manually review findings marked PATTERN_MATCH or NEEDS_REVIEW before acting on them.

Risk: The skill writes `.ralph-report.md` and may rename an existing report in the workspace.

Mitigation: Run it from the intended workspace and check for an existing report before execution.

## Reference(s):

- [Severity and Triage Reference](references/severity-guide.md)
- [ClawHub Skill Page](https://clawhub.ai/dorukardahan/skills/ralph-quick)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance, Files]

**Output Format:** [Per-iteration text findings and a Markdown report file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces 10 checks by default and writes the final report to .ralph-report.md.]

## Skill Version(s):

3.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
