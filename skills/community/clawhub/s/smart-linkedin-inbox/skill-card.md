## Description: <br>
LinkedIn inbox manager and conversation assistant powered by Linxa for searching, filtering, reading, and managing LinkedIn conversations and lead follow-up. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vdybenko](https://clawhub.ai/user/vdybenko) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users use this skill to review LinkedIn inbox activity, search and filter conversations, read message threads, generate next actions, add lead comments, and mark conversations as read through Linxa. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access LinkedIn inbox and lead data through Linxa. <br>
Mitigation: Install only if you trust Linxa with that data, keep the LINXA_TOKEN scoped to the intended account, and revoke or rotate the token when access is no longer needed. <br>
Risk: The skill can make persistent changes by adding lead comments and marking conversations as read. <br>
Mitigation: Require explicit confirmation before state-changing requests, showing the exact lead, conversation, comment text, or read-state change. <br>
Risk: Broad activation for LinkedIn messaging tasks may expose more inbox context than the user intended. <br>
Mitigation: Ask the user to narrow searches or confirm the conversation before fetching full threads or taking action. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/vdybenko/smart-linkedin-inbox) <br>
- [Linxa API OpenAPI specification](artifact/openapi.yaml) <br>
- [Linxa MCP setup](https://app.uselinxa.com/setup-mcp) <br>
- [Linxa Chrome Extension](https://chromewebstore.google.com/detail/ai-smart-inbox-for-linked/ggkdnjblijkchfmgapnbhbhnphacmabm) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with authenticated API calls, JSON API responses, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a LINXA_TOKEN bearer token and user-selected conversation or profile identifiers for scoped requests.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
