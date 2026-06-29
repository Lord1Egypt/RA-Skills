## Description: <br>
Design profile-based agent teams from skills, workflows, prompts, tools, or briefs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[c-narcissus](https://clawhub.ai/user/c-narcissus) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use Skill2Team to convert complex skills, workflows, prompts, tools, scripts, SOPs, or briefs into compact profile-based agent team designs and, when requested, Codex package artifacts. It supports design and package workflows with explicit architecture maps, orchestration maps, quality gates, human-interaction preservation, and runtime handoff guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated package-end registration prompts or helper scripts may change Codex agent configuration. <br>
Mitigation: Inspect generated manifests and .codex/config.toml changes before registration, then run smoke tests before treating a generated team as runnable. <br>
Risk: Generated team packages can accidentally include secrets, private files, or unintended local resources. <br>
Mitigation: Review local-resource manifests and generated package contents before sharing or deploying artifacts. <br>
Risk: Agent-team proposals may contain incorrect or misleading design guidance. <br>
Mitigation: Use the skill's design/package quality gates and independent review before deployment. <br>


## Reference(s): <br>
- [Skill2Team ClawHub Skill Page](https://clawhub.ai/c-narcissus/skills/skill2team) <br>
- [Agent Architecture and Workflow Method](references/agent-architecture-and-workflow-method.md) <br>
- [Workflow-Aligned Orchestration](references/workflow-aligned-orchestration.md) <br>
- [Package Workflow](references/package-workflow.md) <br>
- [Output Contracts](references/output-contracts.md) <br>
- [Team Usage Guide](references/team-usage-guide.md) <br>
- [Risk Governance](references/risk-governance.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown, JSON, TOML, prompt templates, and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce Codex package artifacts, manifests, configuration snippets, design archives, quality gates, and follow-up prompts depending on the selected delivery path.] <br>

## Skill Version(s): <br>
1.9.2 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
