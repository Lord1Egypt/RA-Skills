## Description: <br>
Let OpenClaw capture reusable workflows as managed skill candidates, support review or revision, and evolve safely through manual, assisted, or autonomous modes inside the current workspace. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[haocheng0126](https://clawhub.ai/user/haocheng0126) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and teams use this skill to let OpenClaw identify reusable workspace workflows, draft managed skill candidates, and route them through review, approval, publish, or rollback flows. It is aimed at review-first skill evolution with manual, assisted, and autonomous modes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Autonomous mode can change learned skills without per-change approval. <br>
Mitigation: Start in manual mode and enable assisted or autonomous mode only after confirming that low-risk auto-promotion boundaries match the workspace's expectations. <br>
Risk: Managed skill candidates may accidentally capture sensitive project details from the current workspace. <br>
Mitigation: Review candidate diffs before publishing and avoid letting the skill encode secrets, private file contents, or sensitive project context into reusable instructions. <br>
Risk: The optional TrustLoop plugin changes lifecycle behavior by adding a native managed-skill tool. <br>
Mitigation: Review the plugin separately before installation and before relying on plugin-backed publish, rollback, or mode-change operations. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/haocheng0126/trustloop-skill-evolver) <br>
- [README](README.md) <br>
- [Evolution Rules](references/evolution-rules.md) <br>
- [Review Policy](references/review-policy.md) <br>
- [Managed Skill Tool Interface](references/skill-manage-managed-tool.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline commands, generated skill drafts, candidate records, registry entries, and audit records] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Workspace-local state is written under .skill-evolver and published managed skills are constrained to skills/learned-* paths.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
