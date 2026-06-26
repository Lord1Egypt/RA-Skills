## Description: <br>
SocialEpoch WhatsApp SCRM API 智能助手 helps agents manage WhatsApp SCRM accounts, send single or bulk messages, query agents and task status, configure callbacks, and manage auto-receive workflows through SocialEpoch APIs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liuguangchuan](https://clawhub.ai/user/liuguangchuan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External business, marketing, and customer-support operators use this skill to automate WhatsApp SCRM messaging, account queries, callbacks, task tracking, and customer communication workflows through SocialEpoch. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires sensitive SocialEpoch credentials and can send or bulk-send WhatsApp and customer data through the service. <br>
Mitigation: Use scoped API keys, keep credentials out of shared logs, review recipients and message content, and use consent-based messaging only. <br>
Risk: The security scan reports that the skill changes local OpenClaw configuration, installs Python packages, downloads and runs a native client, and manages local processes. <br>
Mitigation: Install only when the publisher is trusted, verify the downloaded client through an out-of-band trusted source, and run the skill in a controlled environment. <br>
Risk: Callback and auto-receive workflows can route message and status data to configured URLs. <br>
Mitigation: Review callback URLs before enabling them, restrict access to receiving endpoints, and test with non-sensitive data first. <br>


## Reference(s): <br>
- [SocialEpoch WhatsApp SCRM Open API documentation](https://doc.socialepoch.com/wa-scrm-open-api-doc/) <br>
- [ClawHub skill listing](https://clawhub.ai/liuguangchuan/socialepoch-wa-scrm) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, configuration, api calls, guidance] <br>
**Output Format:** [Structured JSON responses with concise command and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands may require SocialEpoch tenant credentials and can open a local dashboard or manage the receive client.] <br>

## Skill Version(s): <br>
2.3.3 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
