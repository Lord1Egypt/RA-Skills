## Description: <br>
Store, search, and chat with a personal knowledge base using the SuperMemory API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[clawdbot51-oss](https://clawhub.ai/user/clawdbot51-oss) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to save notes or other memory content to SuperMemory, search stored memories, and ask chat-style questions over the returned results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A live-looking API key appears in the setup documentation. <br>
Mitigation: Do not use the embedded key; configure SUPERMEMORY_API_KEY with the user's own key through a secure environment variable and rotate any exposed credential. <br>
Risk: The skill can send user-provided memory content to a remote SuperMemory service. <br>
Mitigation: Do not store passwords, tokens, regulated personal data, or confidential business information as memories; confirm SuperMemory retention and deletion behavior before use. <br>


## Reference(s): <br>
- [ClawHub Supermemory release](https://clawhub.ai/clawdbot51-oss/supermemory) <br>
- [SuperMemory documents API endpoint](https://api.supermemory.ai/v3/documents) <br>
- [SuperMemory search API endpoint](https://api.supermemory.ai/v3/search) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Configuration guidance] <br>
**Output Format:** [Terminal text and JSON responses from shell scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SUPERMEMORY_API_KEY and network access to the SuperMemory API.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
