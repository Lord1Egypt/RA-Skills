## Description: <br>
Autonomous AI agent that tips Rumble.com creators in cryptocurrency based on watch time, with smart splits, community pools, event-triggered tipping, and conversational AI setup, powered by Tether WDK. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Dev-me4](https://clawhub.ai/user/Dev-me4) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this agent to configure browser-based cryptocurrency tipping rules for Rumble creators, including watch-time tips, split payments, community pools, event-triggered tips, wallet checks, budget controls, and transaction history queries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Autonomous crypto tipping can execute irreversible payments using persistent wallet authority. <br>
Mitigation: Review before installing, use a separate low-balance wallet, avoid importing a primary seed phrase, and confirm comfort with irreversible transfers based on browser activity and configured rules. <br>
Risk: Configured rules may spend more than intended if autonomous mode, watch-time triggers, or event triggers are enabled too broadly. <br>
Mitigation: Set strict daily and per-tip caps and keep autonomous mode off unless needed. <br>


## Reference(s): <br>
- [RumbleTipAI ClawHub release](https://clawhub.ai/Dev-me4/rumble-autotip) <br>
- [Publisher profile](https://clawhub.ai/user/Dev-me4) <br>
- [Project homepage](https://github.com/kalxe/rumble-ai-extension) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with natural-language commands, parameter lists, setup guidance, and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference required environment variable OPENAI_API_KEY and Node packages for Tether WDK wallet support.] <br>

## Skill Version(s): <br>
2.0.1 (source: server release evidence; artifact frontmatter reports 2.1.0 and artifact skill.json reports 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
