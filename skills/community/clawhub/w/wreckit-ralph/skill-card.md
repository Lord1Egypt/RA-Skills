## Description:

Reckit helps agents verify code changes by running code-quality, type-checking, mutation-testing, security, regression, performance, and proof-bundle workflows before shipping.

This skill is ready for commercial/non-commercial use.

## Publisher:

[christiancattaneo](https://clawhub.ai/user/christiancattaneo)

### License/Terms of Use:


## Use Case:

Developers and engineering teams use Reckit to build, rebuild, fix, or audit software with verification gates and a generated proof bundle that records Ship, Caution, or Blocked results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security verdict is suspicious because the skill asks users to weaken sandbox protections.

Mitigation: Run it only in a disposable, sandboxed workspace and do not follow sandbox-bypass or inherit-all environment guidance.

Risk: The skill may execute project commands and mutation-testing workflows against the target repository.

Mitigation: Avoid repositories with secrets or production data and review planned commands before execution.

Risk: Generated .wreckit proof artifacts may contain project details or sensitive output.

Mitigation: Review generated .wreckit files before sharing or publishing them.

Risk: The dashboard has reported XSS and CORS issues.

Mitigation: Do not run the dashboard on sensitive projects until those issues are fixed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/christiancattaneo/skills/wreckit-ralph)
- [Verification Framework](references/verification-framework.md)
- [Corroboration Gate](references/gates/corroboration.md)
- [Proof Bundle Gate](references/gates/proof-bundle.md)
- [Swarm Orchestrator](references/swarm/orchestrator.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, JSON reports, generated configuration, and proof-bundle files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate .wreckit proof artifacts and dashboard data in the target project.]

## Skill Version(s):

2.4.0 (source: server evidence release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
