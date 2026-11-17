## Description:

SharpAgent Engineering Lifecycle is a 6-phase engineering pipeline for Spec, Plan, Build, Verify, Review, and Ship workflows, embedding five-factor review, calibration, content safety, and anti-rationalization practices for structured development.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yezhaowang888-stack](https://clawhub.ai/user/yezhaowang888-stack)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering agents use this skill to run a structured software lifecycle from requirements and planning through implementation, verification, review, and release documentation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow may cause agents to create or update planning, review, verification, and release documents that affect a project record.

Mitigation: Review generated documents and require evidence such as passing tests, build output, or runtime checks before accepting lifecycle progress.

Risk: Applying the full lifecycle to very small changes may add unnecessary process overhead.

Mitigation: Use the skill's fast-track guidance for tiny or single-line changes while still completing build, verify, review, and ship checks.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yezhaowang888-stack/skills/sharpagent-engineering-lifecycle)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with optional code, shell command, configuration, planning, review, verification, and release artifacts.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs vary by lifecycle phase and may include specs, task plans, tests, verification reports, review notes, release notes, and retrospectives.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
