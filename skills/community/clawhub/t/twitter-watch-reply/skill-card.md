## Description: <br>
Twitter Watch Reply monitors configured X/Twitter accounts through the 6551 interface, identifies new tweets, drafts reply candidates, and supports a semi-automatic browser-based reply workflow after user confirmation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yugulugulu](https://clawhub.ai/user/yugulugulu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to monitor selected X/Twitter accounts, prepare concise AI-assisted reply drafts, and avoid duplicate handling with local watch state. It is intended for semi-automatic social engagement where a user confirms the reply before posting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Twitter/X token for 6551 API access. <br>
Mitigation: Provide the token only through the runtime environment, do not hard-code it, and avoid sharing it in chats or committed files. <br>
Risk: Watch state and pending tweet data are stored in the workspace. <br>
Mitigation: Use an appropriate workspace or custom data directory and review stored state before sharing the workspace. <br>
Risk: Optional notifications can forward tweet content and reply candidates to a configured chat channel. <br>
Mitigation: Keep notifications disabled unless intentionally configured, and verify the target channel, thread, and recipient before enabling. <br>
Risk: Reply drafts could be posted from a logged-in browser session if the workflow is advanced without review. <br>
Mitigation: Keep the documented semi-automatic flow and require explicit user confirmation before browser-based posting. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/yugulugulu/twitter-watch-reply) <br>
- [README](README.md) <br>
- [Configuration example](references/config-example.json) <br>
- [Host adapter reference](references/host-adapter.md) <br>
- [Reply generation guide](references/reply-generation.md) <br>
- [6551 token setup](https://6551.io/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON alert payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces draft replies and notification payloads for review; posting and outbound notifications require user or host confirmation.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
