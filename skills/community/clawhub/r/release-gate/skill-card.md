## Description:

Guides agents through role-based sign-off and decision logging before irreversible or customer-facing changes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ferrentinomj-dev](https://clawhub.ai/user/ferrentinomj-dev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and release coordinators use this skill to collect explicit role-based checklist approvals, block unresolved changes, and record release decisions before deployments or other hard-to-reverse actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A checklist alone cannot prevent an agent from bypassing the release gate.

Mitigation: Use a project-specific gate and require explicit sign-off before high-impact actions.

Risk: A failed log write can leave a release decision unrecorded.

Mitigation: Verify that the log entry was written before proceeding.

## Reference(s):

- [Release Gate on ClawHub](https://clawhub.ai/ferrentinomj-dev/skills/release-gate)
- [OWASP Secure Coding Practices Quick Reference Guide](https://owasp.org/www-project-secure-coding-practices-quick-reference-guide/)
- [The Twelve-Factor App](https://12factor.net/)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code]

**Output Format:** [Markdown checklists and Python examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can append approval or block decisions to a specified log file.]

## Skill Version(s):

1.2.0 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
