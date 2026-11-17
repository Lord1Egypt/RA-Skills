## Description:

sn-deepresearch-cli helps an agent prepare, install, configure, and launch SenseNova-Skills-DeepResearch workflows for multi-source research, fact checking, competitive analysis, due diligence, and report generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sensenova-skills](https://clawhub.ai/user/sensenova-skills)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and analysts use this skill to run SenseNova-Skills-DeepResearch for industry and market research, competitive analysis, policy or technical research, business due diligence, trend analysis, fact checking, and report delivery. The skill guides the agent through environment checks, installation or upgrade, harness preparation, parameter confirmation, launch, progress monitoring, and result handoff.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Global npm installation or upgrade can modify a user's environment and install mutable packages.

Mitigation: Before installing, confirm trust in the npm package and publisher; prefer a pinned version or isolated environment when possible.

Risk: Broad networked research workflows may send research context through the selected harness, search sources, and local configuration.

Mitigation: Avoid sensitive private research unless the user is comfortable with the selected harness, search sources, and local configuration changes.

Risk: OpenClaw permission changes can expand local workspace write access and tool capabilities.

Mitigation: Review requested permission changes carefully and scope them to the current agent and workspace.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sensenova-skills/skills/sn-deepresearch-cli)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration guidance]

**Output Format:** [Markdown guidance with shell command blocks and configuration checks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May ask for user confirmation before installing global npm packages, changing harness configuration, granting OpenClaw workspace permissions, or launching long-running research.]

## Skill Version(s):

2026.9.12 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
