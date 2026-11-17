## Description:

Comprehensive security analysis and vulnerability assessment -- threat modeling, secure code review, and pre-deployment security validation across application and infrastructure layers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[snazar-faberlens](https://clawhub.ai/user/snazar-faberlens)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security engineers use this skill to run Snyk-backed security assessments across source code, dependencies, containers, infrastructure as code, SBOMs, and AI components, then prioritize findings and produce remediation guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unauthorized scans or cross-organization comparisons could expose vulnerability findings outside the intended Snyk organization.

Mitigation: Verify Snyk authentication, organization scope, and authorization before scanning or changing org context.

Risk: Repeated identical scans can consume Snyk API quota without adding diagnostic value.

Mitigation: Run one scan for a stable target and retry only when inputs, environment, or a failed scan result justify it.

Risk: Snyk API tokens or credentials could be exposed if written to files, environment output, or conversation logs.

Mitigation: Keep credentials within the official Snyk authentication workflow and do not print or persist tokens.

## Reference(s):

- [Snyk Hardened on ClawHub](https://clawhub.ai/snazar-faberlens/skills/snyk-hardened)
- [Faberlens Snyk Safety Evaluation](https://faberlens.ai/explore/snyk)
- [Faberlens Publisher Profile](https://clawhub.ai/user/snazar-faberlens)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown reports with structured findings, remediation steps, code examples, and command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires authenticated and authorized Snyk MCP access; scan scope and organization context should be verified before execution.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
