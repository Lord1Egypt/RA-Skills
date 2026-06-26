## Description: <br>
Guide for using wjx-cli (Wenjuanxing CLI) to create surveys, query responses, and analyze data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[orzwq](https://clawhub.ai/user/orzwq) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to help an agent install and use wjx-cli for Wenjuanxing survey creation, response retrieval, local analytics, and contact or account management. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can let an agent use a Wenjuanxing API key for broad account and data-changing actions. <br>
Mitigation: Use the least-privileged API key available, avoid exposing secrets in chat where possible, and require explicit confirmation before exports, response submission or import, score changes, SSO link generation, contact or account changes, response clearing, or survey deletion. <br>
Risk: The setup flow may rely on global npm installation, sudo, or pipe-to-shell Node.js installation commands. <br>
Mitigation: Review the source before installation and prefer user-scoped or reviewed installation paths when possible. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/orzwq/wjx-cli-use) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/orzwq) <br>
- [Survey command reference](references/survey-commands.md) <br>
- [Response command reference](references/response-commands.md) <br>
- [Contact and account command reference](references/contacts-commands.md) <br>
- [Analytics command reference](references/analytics-commands.md) <br>
- [Question type reference](references/question-types.md) <br>
- [DSL syntax reference](references/dsl-syntax.md) <br>
- [Node.js installation reference](references/install-nodejs.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, code, markdown] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSONL examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use Wenjuanxing API credentials and may produce or execute wjx-cli commands for account and survey operations.] <br>

## Skill Version(s): <br>
0.3.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
