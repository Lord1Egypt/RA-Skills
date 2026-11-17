## Description:

Launch a NovitaClaw (OpenClaw) sandbox, install a specified skill, and generate an installation and security audit report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[freecodewu](https://clawhub.ai/user/freecodewu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to test community skills in an isolated sandbox before installing them locally and to generate an installation and security audit report for review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unsafe installation patterns and sandbox commands may execute unreviewed remote installation code.

Mitigation: Install only in a disposable, least-privilege environment and independently verify remote installer scripts before running them.

Risk: The scanner may collect unrelated skill files or produce advisory results that miss context.

Mitigation: Run the audit in a clean sandbox containing only the target skill and treat reports as review input rather than a definitive security decision.

Risk: Novita API credentials are required for sandbox access.

Mitigation: Use a scoped Novita API key and avoid exposing credentials in shared terminals, logs, or long-lived sandbox sessions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/freecodewu/skills/skill-auditor-in-sandbox)
- [Project Homepage](https://github.com/freecodewu/skill-auditor-in-sandbox)
- [NovitaClaw Documentation](https://novita.ai/docs/guides/novitaclaw)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, guidance]

**Output Format:** [Markdown report with inline shell commands and JSON outputs from helper scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Novita API key, the novitaclaw CLI, Node.js, and sandbox access.]

## Skill Version(s):

1.0.3 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
