## Description: <br>
Generate, schedule, and publish tweets in your voice using AI. Browse viral content, manage preferences, and track billing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jmoon90](https://clawhub.ai/user/jmoon90) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to draft, review, schedule, and publish X/Twitter posts through the XReply MCP server, while also checking voice profile status, preferences, billing, quota, and subscription-gated features. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can draft, schedule, publish, delete, and auto-retweet public X/Twitter posts. <br>
Mitigation: Review the exact post text, account, schedule, and reversibility before invoking publish, schedule, delete, or auto-retweet tools. <br>
Risk: The XREPLY_TOKEN grants authenticated access to the user's XReply account and may expire or be exposed if handled carelessly. <br>
Mitigation: Store XREPLY_TOKEN only in a secret or configuration mechanism, avoid pasting it into chats or logs, and rotate it if exposed. <br>
Risk: Generation and discovery features may consume quota or require Pro/BYOK subscription access. <br>
Mitigation: Check billing status before batch generation or subscription-gated tools, and reduce batch size when quota is insufficient. <br>


## Reference(s): <br>
- [XReply website](https://xreplyai.com) <br>
- [ClawHub skill page](https://clawhub.ai/jmoon90/xreply) <br>
- [Publisher profile](https://clawhub.ai/user/jmoon90) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with mcporter and npx command examples for MCP tool calls.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires mcporter or npx plus an XREPLY_TOKEN secret for authenticated XReply MCP calls.] <br>

## Skill Version(s): <br>
0.1.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
