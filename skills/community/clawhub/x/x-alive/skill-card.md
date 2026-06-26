## Description: <br>
X Alive helps AI agents operate an authentic X/Twitter presence through organic engagement, trend awareness, deduplication, and safety guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kitakitsune0x](https://clawhub.ai/user/kitakitsune0x) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External developers and agent operators use this skill to configure an AI agent's X/Twitter identity, engagement loop, posting behavior, mention handling, and safety escalation practices. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent to post and engage publicly on an X/Twitter account. <br>
Mitigation: Use a dedicated low-privilege X app or token where possible, keep token files private, and require human approval for reputationally sensitive or irreversible actions. <br>
Risk: Regular background loops can drift into forced posting, repetitive engagement, or account-like automation that feels inauthentic. <br>
Mitigation: Run loops as check-and-maybe-engage workflows, apply the deduplication rule before posting, and choose silence when nothing relevant is worth saying. <br>
Risk: Token, ticker, contract-address, scam, or financial mentions can create reputational and compliance risk. <br>
Mitigation: Ignore or privately escalate crypto and financial mentions, and require explicit human approval before any public response. <br>
Risk: Mentions and DMs can expose the agent to spam, impersonation, harassment, or attempts to extract private information. <br>
Mitigation: Default to ignoring DMs and obvious spam, never share private or infrastructure details, and escalate impersonation, threats, money, or legal issues to a human operator. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kitakitsune0x/x-alive) <br>
- [X Developer Platform](https://developer.x.com) <br>
- [xurl CLI](https://github.com/xdevplatform/xurl) <br>
- [x-research skill](https://github.com/rohunvora/x-research-skill) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Agent behavior guidance for X/Twitter posting, replies, monitoring loops, and safety escalation.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
