## Description: <br>
Creates a new OpenClaw agent and configures a Feishu bot account, routing, workspace identity files, optional skill installation, Feishu tools, and gateway restart. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[beyondbright](https://clawhub.ai/user/beyondbright) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to provision OpenClaw agents that are connected to Feishu bots, including account setup, route binding, workspace files, optional skill installation, and gateway restart steps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persist Feishu app credentials in OpenClaw configuration. <br>
Mitigation: Use a least-privilege Feishu app and run the skill only in environments where storing that app secret in OpenClaw configuration is acceptable. <br>
Risk: The skill modifies OpenClaw configuration, enables Feishu tools, and restarts the OpenClaw gateway. <br>
Mitigation: Back up openclaw.json, review the proposed configuration changes, and run the workflow during an acceptable maintenance window. <br>
Risk: The skill may copy an existing MEMORY.md into the new agent workspace. <br>
Mitigation: Review any existing MEMORY.md before allowing it to be copied into a newly created agent. <br>
Risk: An optional requested skill may be installed into the new agent workspace. <br>
Mitigation: Review and trust any optional skill before requesting installation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/beyondbright/walter-agent-factory) <br>
- [Publisher profile](https://clawhub.ai/user/beyondbright) <br>
- [Feishu tenant access token API](https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with Bash and PowerShell code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes required input parameters, setup steps, platform-specific scripts, and error-handling guidance.] <br>

## Skill Version(s): <br>
2.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
