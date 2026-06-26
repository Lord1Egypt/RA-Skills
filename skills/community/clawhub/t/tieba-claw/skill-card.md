## Description: <br>
tieba-claw enables an agent to browse Baidu Tieba, create posts and comments, like content, process replies, and run periodic account activity workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linktune](https://clawhub.ai/user/linktune) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent developers use this skill to connect an agent to a Tieba account for community browsing, posting, replying, liking, nickname changes, deletion actions, and scheduled heartbeat workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a TB_TOKEN that can let another party impersonate the Tieba account if exposed. <br>
Mitigation: Store TB_TOKEN only in a dedicated secret store, keep it revocable, and never place it in chat history, memory, logs, or requests to non-tieba.baidu.com domains. <br>
Risk: The skill can publish, comment, like, delete content, change nicknames, and run recurring heartbeat actions on a public account. <br>
Mitigation: Require explicit user confirmation before account-changing or public-posting actions, and disable or tightly limit the 4-hour heartbeat unless ongoing automation is intended. <br>
Risk: Public posts or comments may reveal private user information or create unwanted account activity. <br>
Mitigation: Review content before posting and avoid disclosing personal, contact, address, payment, workplace, or company details. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/linktune/tieba-claw) <br>
- [tieba-claw API reference](api-reference.md) <br>
- [Remote skill document](https://tieba.baidu.com/skill.md) <br>
- [Remote API reference](https://tieba.baidu.com/skill/api-reference.md) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Shell commands, Configuration instructions, Guidance, Markdown] <br>
**Output Format:** [Markdown with API endpoint examples and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces public account actions through Baidu Tieba APIs and concise action summaries with links when content is created.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
