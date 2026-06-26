## Description: <br>
Audit and port AI agent skills, Claude Code skills/plugins, Codex skills/plugins, Gemini CLI skills/extensions, slash commands, agents, hooks, policies, MCP-backed plugins, and similar skill repositories across target agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yand](https://clawhub.ai/user/yand) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to inspect agent-skill repositories, assess portability and security posture, and stage compatible target-agent layouts when porting is requested. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Untrusted source skills or plugins may contain unsafe scripts, install behavior, credential requirements, or target-specific automation. <br>
Mitigation: Use audit-only mode first, review the generated report, and approve remote cloning, source script execution, package installation, or global agent-directory writes only when those actions are intended. <br>
Risk: Ported output can misrepresent unsupported lifecycle hooks, MCP setup, app connectors, credentials, or agent-specific orchestration as fully portable behavior. <br>
Mitigation: Keep dependency-bound and unsupported behavior in the compatibility report or dependency notes, and require manual setup for credentials, MCP servers, app connectors, provisioning, regulated review, and final installation. <br>


## Reference(s): <br>
- [Skill Port ClawHub Release](https://clawhub.ai/yand/skill-port) <br>
- [Project Homepage](https://github.com/yand/skill-port) <br>
- [Ecosystem Porting](references/ecosystem-porting.md) <br>
- [Location Policy](references/locations.md) <br>
- [Portability Model](references/portability-model.md) <br>
- [Report Schema](references/report-schema.md) <br>
- [Security Review](references/security.md) <br>
- [Claude Source Porting](references/source-claude.md) <br>
- [Codex Source Porting](references/source-codex.md) <br>
- [Gemini Source Porting](references/source-gemini.md) <br>
- [Claude Target Porting](references/target-claude.md) <br>
- [Codex Target Porting](references/target-codex.md) <br>
- [Gemini Target Porting](references/target-gemini.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown summaries, JSON reports, staged files, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Audit-only mode produces reports without creating ported files; port mode stages target-agent layouts under explicit output paths.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
