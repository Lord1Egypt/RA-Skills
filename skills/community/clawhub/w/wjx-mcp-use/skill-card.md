## Description: <br>
Guides agents using wjx-mcp-server MCP tools to create, manage, analyze, and administer Wenjuanxing surveys, forms, polls, exams, contacts, SSO links, and response data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[orzwq](https://clawhub.ai/user/orzwq) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to guide an agent through Wenjuanxing survey administration workflows, including creating surveys, querying and exporting responses, analyzing metrics, managing contacts, and generating SSO or survey links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent operating a real Wenjuanxing account with sensitive credentials. <br>
Mitigation: Install only for intended account administration, use least-privileged credentials, and avoid sharing API keys or passwords in chat. <br>
Risk: The documented workflows include deletion, exports, admin changes, response clearing, and SSO link generation. <br>
Mitigation: Require explicit user confirmation with the exact target before irreversible or account-affecting actions. <br>
Risk: Survey responses and participant data may contain sensitive information. <br>
Mitigation: Avoid exposing participant data or SSO URLs in chat and limit exports to authorized users and necessary fields. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/orzwq/wjx-mcp-use) <br>
- [DSL and question types](references/dsl-and-types.md) <br>
- [Survey tools](references/tools-survey.md) <br>
- [Response tools](references/tools-response.md) <br>
- [Other tools](references/tools-other.md) <br>
- [Troubleshooting](references/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Configuration instructions, Shell commands] <br>
**Output Format:** [Markdown guidance with inline commands and structured tool-use recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include natural-language instructions, survey JSON guidance, configuration steps, and safety confirmations for account-affecting actions.] <br>

## Skill Version(s): <br>
0.3.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
