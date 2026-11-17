## Description:

Automatically uses installed skills by maintaining trigger mappings that tell an agent when to invoke each skill.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kapslap](https://clawhub.ai/user/kapslap)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to define trigger tables that map observable user contexts to installed skills, so agents can choose relevant skills without repeated manual prompts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can make future skill selection persistent and automatic, reducing explicit user control over when skills run.

Mitigation: Install only when persistent workspace-level automation is intended, and review each proposed trigger before adding it to permanent rules.

Risk: Automatic triggers for powerful skills could later route agents toward skills that write files, use credentials, contact accounts, publish, deploy, or delete data without enough deliberation.

Mitigation: Avoid auto-use triggers for skills with write, credential, account, publishing, deployment, or deletion capabilities unless they still require explicit approval at execution time.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kapslap/skills/skill-auto-use)

## Skill Output:

**Output Type(s):** [guidance, markdown, configuration]

**Output Format:** [Markdown prose with trigger-table examples and workspace rule guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces persistent trigger-table and skill-use guidance; no direct tool execution is required by the skill itself.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
