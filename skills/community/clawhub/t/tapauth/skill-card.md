## Description: <br>
OAuth token provider for OpenClaw agents that helps configure scoped OAuth tokens and user-entered secrets through TapAuth and OpenClaw SecretRef entries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[schwartzdev](https://clawhub.ai/user/schwartzdev) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use TapAuth when an OpenClaw agent needs delegated OAuth access or a fixed user-supplied secret without placing credentials directly in shell commands or configuration files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: TapAuth brokers access to OAuth grants, manual secrets, and a local grant cache that should be treated as sensitive. <br>
Mitigation: Install only when that credential-brokering behavior is acceptable, keep TAPAUTH_HOME in a private directory, and revoke or delete cached grants when access is no longer needed. <br>
Risk: Approving broad provider scopes can expose more account access than the task requires. <br>
Mitigation: Approve the minimum scopes needed and avoid broad scopes such as GitHub repo, Vercel full integration access, or Apify full_api_access unless they are required. <br>


## Reference(s): <br>
- [TapAuth documentation](https://tapauth.ai/docs) <br>
- [TapAuth website](https://tapauth.ai) <br>
- [ClawHub TapAuth skill page](https://clawhub.ai/schwartzdev/skills/tapauth) <br>
- [OpenClaw Integration](references/openclaw.md) <br>
- [Google Workspace via TapAuth](references/google.md) <br>
- [GitHub via TapAuth](references/github.md) <br>
- [Gmail via TapAuth](references/gmail.md) <br>
- [Slack OAuth Provider](references/slack.md) <br>
- [Vercel via TapAuth](references/vercel.md) <br>
- [Agent Skills Spec](https://agentskills.io) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and bash; designed for OpenClaw exec secrets provider configuration.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release metadata, CHANGELOG.md, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
