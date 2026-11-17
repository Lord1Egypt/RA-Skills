## Description:

Automate setup, configuration, execution, monitoring, and troubleshooting of AutoResearchClaw, a 23-stage autonomous research pipeline for generating conference-grade papers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[othmanadi](https://clawhub.ai/user/othmanadi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and technical users use this skill to set up, configure, run, monitor, resume, and troubleshoot AutoResearchClaw research-paper generation workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles LLM API credentials during configuration.

Mitigation: Use environment-variable names instead of raw API keys and do not paste secrets into chat.

Risk: The workflow can run long autonomous research actions and may skip approval gates by default.

Mitigation: Disable auto-approve for first runs and review proposed research directions, experiments, and final output before continuing.

Risk: Sandbox or SSH experiment modes may execute generated experiment code.

Mitigation: Use a dedicated virtual environment and avoid sandbox or SSH modes until generated experiment code and configuration files have been reviewed.

Risk: Dependency installation and upstream package behavior can change over time.

Mitigation: Review before installing and prefer a pinned package version or commit.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/othmanadi/skills/researchclaw-2)
- [Server-resolved GitHub Import](https://github.com/OthmanAdi/researchclaw-skill/tree/main/skills/researchclaw)
- [AutoResearchClaw Upstream](https://github.com/aiming-lab/AutoResearchClaw)
- [Pipeline Stages Reference](references/pipeline-stages.md)
- [Configuration Reference](references/config-reference.md)
- [Troubleshooting Guide](references/troubleshooting.md)
- [Chinese README](references/README-CN.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, generated configuration files, validation reports, and troubleshooting summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write config.yaml, log files, and pipeline artifacts when the user approves the relevant workflow steps.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
