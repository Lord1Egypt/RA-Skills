## Description:

Perform a thorough client-side and browser-facing security assessment of a target web application.

This skill is ready for commercial/non-commercial use.

## Publisher:

[enderphan94](https://clawhub.ai/user/enderphan94)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security reviewers use this skill to perform authorized, non-destructive client-side assessments of web applications and produce a structured Markdown report of browser-facing risks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Client-side security testing can create real assessment risk if scope and authorization are unclear.

Mitigation: Use only for authorized targets, define the target origin and included subdomains before testing, and keep testing passive or low-risk unless active scanning is explicitly approved.

Risk: The artifact includes optional active tools such as nuclei and runtime validation steps that may be noisy.

Mitigation: Confirm authenticated testing and active scanner approval before running noisy checks, and keep request volume moderate.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/enderphan94/skills/web-front-scanner)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown security report with command notes and structured findings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Final report is expected as client_side_pentest_report.md.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
