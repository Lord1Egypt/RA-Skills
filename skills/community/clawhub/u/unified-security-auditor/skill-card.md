## Description:

Unified application security skill for Coding Agent systems like OpenCode, used when reviewing or writing code that touches authentication, authorization, user input, payments, database access, secrets, deployment, dependencies, or AI/agent workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[selimerunkut](https://clawhub.ai/user/selimerunkut)

### License/Terms of Use:

CC-BY-SA-4.0

## Use Case:

Developers and engineers use this skill to review codebases and implementation plans for application security issues, especially in authentication, authorization, secrets handling, dependency risk, deployment hardening, CI/CD automation, and AI/agent workflows. It supports both proactive secure coding guidance and structured audit reports organized by severity.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can generate audit reports as Markdown files in the active repository, which may surprise users if the destination is not agreed in advance.

Mitigation: Invoke the skill explicitly and confirm the target folder or report path before asking it to write an audit report.

Risk: Security findings and remediation advice may be incomplete or context-sensitive even when the skill reports no embedded execution or hidden data movement.

Mitigation: Review findings, proposed fixes, and severity ratings before relying on them for production security decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/selimerunkut/skills/unified-security-auditor)
- [claude-code-owasp](https://github.com/agamm/claude-code-owasp)
- [trailofbits/skills](https://github.com/trailofbits/skills)
- [vibe-security-skill](https://github.com/raroque/vibe-security-skill)
- [VibeSec-Skill](https://github.com/BehiSecc/VibeSec-Skill)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown findings, prioritized summaries, remediation guidance, code diffs, and secure implementation notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate dated Markdown audit reports when explicitly requested; findings are organized by severity.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
