## Description:

Skill Evolver Pro analyzes skill usage data, identifies improvement opportunities, generates optimization plans, and supports resumable evolution workflows with state tracking and local persistence.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pagoda111king](https://clawhub.ai/user/pagoda111king)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill maintainers use this skill to evaluate agent skill performance, review usage and feedback patterns, generate prioritized optimization plans, and resume multi-stage skill evolution work after interruptions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local storage paths can be influenced by skill names and may escape intended data folders.

Mitigation: Use only trusted skill names, validate and normalize path segments before execution, and keep the configured data directory isolated from sensitive files.

Risk: The skill stores local usage, error, feedback, state, and history data.

Mitigation: Avoid storing secrets or sensitive user data in evolution inputs, and review retention and backup practices for the data directory.

Risk: Generated optimization plans and deployment steps may be incorrect or unsuitable for a target skill.

Mitigation: Review generated plans, code changes, and deployment recommendations before applying them to production skills.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/pagoda111king/skills/skill-evolver-pro)
- [Skill Evolver Documentation](https://docs.cloud-shrimp.com/skill-evolver)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with JavaScript examples, JSON-like reports, and implementation recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write local evolution logs, version history, and resumable state files when its JavaScript persistence components are used.]

## Skill Version(s):

0.3.0 (source: server release metadata and artifact documentation, released 2026-04-13)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
