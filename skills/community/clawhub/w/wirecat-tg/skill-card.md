## Description:

Helps an account owner search their Telegram history and, when asked, read or send messages through the tg command-line skill.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wirecat](https://clawhub.ai/user/wirecat)

### License/Terms of Use:

MIT-0

## Use Case:

AI agents use this skill on behalf of an account owner to search Telegram history and answer questions with message locators. They can also inspect chats or perform account actions when the owner explicitly asks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan marked the skill suspicious, citing broad access and account-changing capabilities beyond its stated purpose and weak approval safeguards; the scan was partial and confidence was medium.

Mitigation: Consider the scanner's do-not-install recommendation. Before use, review whether the reported capabilities are needed and whether Telegram access and write approvals meet expectations; a partial scan cannot establish that all behavior is safe.

## Reference(s):

- [Setup and CLI contract](https://github.com/WireCatLabs/tg-cli/blob/main/docs/cli-contract.md)
- [Search guide](https://github.com/WireCatLabs/tg-cli/blob/main/docs/search.md)
- [Topic search guide](https://github.com/WireCatLabs/tg-cli/blob/main/docs/topic-search.md)
- [Query language guide](https://github.com/WireCatLabs/tg-cli/blob/main/docs/query-language.md)
- [Rankings guide](https://github.com/WireCatLabs/tg-cli/blob/main/docs/rankings.md)
- [Messages reference](artifact/references/messages.md)
- [History reference](artifact/references/history.md)
- [People reference](artifact/references/people.md)
- [Tasks reference](artifact/references/tasks.md)
- [Files reference](artifact/references/files.md)
- [Stats reference](artifact/references/stats.md)
- [MCP and bots reference](artifact/references/mcp-and-bots.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Text or Markdown answers; JSON command output when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Answers may cite Telegram messages by locator. Command output may be partial and includes status and coverage fields.]

## Skill Version(s):

1.0.7 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
