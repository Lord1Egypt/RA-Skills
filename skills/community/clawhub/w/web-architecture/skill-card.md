## Description:

Multi-agent orchestration for complex TypeScript/Next.js/Convex projects. Phased builds, functional verification, the full playbook for delegating to sub-agents without chaos.

This skill is ready for commercial/non-commercial use.

## Publisher:

[michaelmonetized](https://clawhub.ai/user/michaelmonetized)

### License/Terms of Use:


## Use Case:

Developers and engineering leads use this skill to coordinate multi-agent builds for TypeScript, Next.js, and Convex applications with phased sequencing, contracts, file ownership, and functional QA checkpoints.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled project guidance can lead agents to implement session replay and error analytics that expose user data without enough privacy controls.

Mitigation: Before using the skill in automated builds, revise telemetry guidance to disable or tightly mask session replay, avoid sending email or full domain objects to Sentry or PostHog, and add consent, opt-out, retention, and redaction requirements.

Risk: Automated generation workflows may run with unpinned tools or access to production secrets.

Mitigation: Pin CLI and dependency versions, run generators in a restricted environment, and keep production secrets out of the execution environment.

## Reference(s):

- [Web Architecture skill page](https://clawhub.ai/michaelmonetized/skills/web-architecture)
- [SKILL.md](artifact/SKILL.md)
- [TECH-REQ.md](artifact/TECH-REQ.md)
- [CODING-STANDARDS.md](artifact/CODING-STANDARDS.md)
- [CONTRACTS-TEMPLATE.md](artifact/CONTRACTS-TEMPLATE.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with checklists, templates, and inline TypeScript and shell examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
