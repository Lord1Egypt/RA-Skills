## Description: <br>
百科虾 is a Feishu-backed company knowledge-base Q&A skill for answering employee questions about company policies, benefits, processes, organization, onboarding, and related internal topics without inventing answers or searching the web. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[beyondbright](https://clawhub.ai/user/beyondbright) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees use this skill to ask company-specific questions and receive answers grounded in the synced Feishu wiki. Administrators use its commands to synchronize wiki content, check sync status, and configure the agent workspace. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send Feishu messages and upload arbitrary local file paths referenced by MEDIA or IMG markers. <br>
Mitigation: Install only in an isolated agent workspace, restrict who can run sync and send-message.js, and limit media uploads to approved cache directories before broad deployment. <br>
Risk: Feishu credentials and synced cache content may expose internal company data if reused outside the intended bot and wiki. <br>
Mitigation: Scope Feishu credentials to the intended bot and wiki, review wiki_list.json before use, and treat cached content as internal company data. <br>
Risk: send-message.js may fall back to the first available Feishu account if the intended account is not explicitly selected. <br>
Mitigation: Require the intended Feishu account explicitly for deployment and verify OPENCLAW_AGENT_NAME or agent-specific configuration. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/beyondbright/walter-baikexia) <br>
- [Configured Feishu wiki: 蜗牛大百科](https://campsnail.feishu.cn/wiki/VGRRw7s4BiStank4GnpczxnGn44) <br>
- [Feishu Open APIs](https://open.feishu.cn/open-apis) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration guidance] <br>
**Output Format:** [Markdown or plain text responses with optional Feishu mention and media markers, plus inline shell commands for setup and synchronization.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Responses should be grounded in cache/content.json; message sending may use Feishu API calls for mentions and media.] <br>

## Skill Version(s): <br>
2.2.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
