## Description:

Runs a broad, long-running security audit across OWASP, secrets, infrastructure, supply chain, compliance, and business-logic checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dorukardahan](https://clawhub.ai/user/dorukardahan)

### License/Terms of Use:


## Use Case:

Developers and security engineers use this skill before major releases, compliance preparation, or incident investigation to guide a structured deep security review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks the agent to inspect sensitive project configuration, secrets metadata, git history, remotes, and infrastructure files.

Mitigation: Run it only in an approved workspace, require secret redaction in reports, and restrict access to repositories and environment files that are necessary for the audit.

Risk: The skill can make automatic report file changes during a long-running audit.

Mitigation: Set an explicit report path before starting and preserve any existing .ralph-report.md before allowing updates.

Risk: Network, runtime, or penetration-test activity could affect systems outside the intended review scope.

Mitigation: Require explicit approval and a defined scope before any network calls, runtime execution, or penetration-test simulation.

## Reference(s):

- [Severity and triage guidance](references/severity-guide.md)
- [Expert persona descriptions](references/personas.md)
- [Ralph Ultra Security Audit on ClawHub](https://clawhub.ai/dorukardahan/skills/ralph-ultra)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown security audit progress entries and final report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May update .ralph-report.md every 50 iterations and is designed for long-running reviews.]

## Skill Version(s):

3.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
