## Description:

Structured debugging with four techniques: Log Injection, Screenshot Analysis, Manual Trace, and Test-Driven Fix.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nakedoshadow](https://clawhub.ai/user/nakedoshadow)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to triage runtime errors, UI defects, regressions, unclear test failures, and performance issues, then select a structured debugging technique to investigate, fix, verify, and clean up.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Some JavaScript test commands can download and run unverified tools from a package registry.

Mitigation: Use trusted repositories or sandboxes, and prefer local-only runner commands such as npm exec --no-install or direct node_modules binaries.

Risk: Project test suites execute repository code.

Mitigation: Run tests only in trusted repositories or within a sandboxed environment.

Risk: Log Injection temporarily modifies source files and can leave debug artifacts behind.

Mitigation: Perform the cleanup pass described by the skill and verify injected logs or debug markers are removed before completion.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/nakedoshadow/skills/shadows-bug-hunter)
- [Publisher Homepage](https://clawhub.ai/NakedoShadow)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Guidance]

**Output Format:** [Markdown bug report with root cause, fix details, file references, and verification checklist]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include proposed or applied code changes and local test commands depending on host agent capabilities.]

## Skill Version(s):

1.1.0 (source: release evidence and artifact/SKILL.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
