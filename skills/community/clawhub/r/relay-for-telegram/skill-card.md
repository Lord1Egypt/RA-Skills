## Description: <br>
Relay for Telegram lets agents search, summarize, extract action items, and recall information from a user's synced Telegram messages, chats, DMs, groups, and channels. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[RelayIntel](https://clawhub.ai/user/RelayIntel) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use Relay for Telegram to search, summarize, and extract structured information from the user's previously synced Telegram chats, DMs, groups, and channels. The skill is intended for Telegram-related recall, catch-up, and communication analysis tasks after the user configures RELAY_API_KEY. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can expose private Telegram message history through broad model invocation. <br>
Mitigation: Install only if the user trusts Relay with synced Telegram data, keep RELAY_API_KEY private, and consider setting disable-model-invocation to true so access occurs only on explicit requests. <br>
Risk: The artifact presents the API as read-only while documenting billing and referral account actions. <br>
Mitigation: Review billing and referral requests before use, and prefer read-only search, chat listing, and message retrieval operations unless the user explicitly approves account changes. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/RelayIntel/relay-for-telegram) <br>
- [Relay for Telegram homepage](https://relayfortelegram.com) <br>
- [Relay Agent API base](https://relayfortelegram.com/api/v1) <br>
- [Relay skill source](https://relayfortelegram.com/skill.md) <br>
- [Relay agent guide](https://relayfortelegram.com/agents.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance, API calls] <br>
**Output Format:** [Markdown guidance with shell commands, REST API examples, and optional JSON summaries.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires RELAY_API_KEY; accesses previously synced Telegram data through Relay's API.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
