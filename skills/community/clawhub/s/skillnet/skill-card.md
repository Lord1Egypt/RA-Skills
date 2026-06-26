## Description: <br>
Search, download, create, evaluate, and analyze reusable agent skills via SkillNet, an open skill supply chain for AI agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[icarus-chen](https://clawhub.ai/user/icarus-chen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to find reusable skills before complex work, install reviewed skills, and create, evaluate, or analyze local skill libraries when reuse is warranted. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide agents toward networked skill-management actions and local library changes. <br>
Mitigation: Require user approval before download, create, evaluate, analyze, loading downloaded skill content, or running downloaded scripts. <br>
Risk: Create, evaluate, and analyze workflows may send repository summaries, document text, trajectory logs, or skill snippets to the configured LLM endpoint. <br>
Mitigation: Disclose the approximate data sent and endpoint before execution; use a local BASE_URL for sensitive content. <br>
Risk: Downloaded skills are third-party content and may contain unsafe instructions or scripts. <br>
Mitigation: Treat downloaded files as reference material, preview them with the user, extract only relevant technical patterns, and never auto-execute downloaded scripts. <br>
Risk: Global pip installation can affect the user's Python environment. <br>
Mitigation: Prefer the documented pipx installation path for an isolated environment. <br>


## Reference(s): <br>
- [SkillNet API and CLI Reference](references/api-reference.md) <br>
- [SkillNet Security and Privacy Reference](references/security-privacy.md) <br>
- [SkillNet Workflow Patterns](references/workflow-patterns.md) <br>
- [ClawHub SkillNet release page](https://clawhub.ai/icarus-chen/skillnet) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, Python snippets, and configuration notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local skill files or relationship reports when the user approves SkillNet create, download, evaluate, or analyze workflows.] <br>

## Skill Version(s): <br>
2.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
