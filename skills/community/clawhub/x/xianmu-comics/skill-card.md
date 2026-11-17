## Description:

Helps readers discover Chinese picture-story books, view and hear their pages, chat with characters, and access full books through the XianMu service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[miaokingsoft](https://clawhub.ai/user/miaokingsoft)

### License/Terms of Use:

MIT-0

## Use Case:

Readers use the skill to find and preview Chinese lianhuanhua, hear narration, converse with story characters, and request paid access to complete books.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Login codes and API keys could be exposed when shared in chat or stored insecurely.

Mitigation: Create the API key on the website, keep it in a trusted secret store, and do not paste one-time codes or full keys into chat.

Risk: Unlocks, character chats, quota resets, or account purchases can spend money or points or change account state.

Mitigation: Explain the cost and effect, then require explicit user confirmation before each charge or account-changing action.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/miaokingsoft/skills/xianmu-comics)
- [Server-resolved source at release](https://github.com/miaokingsoft/xianmu-comics-mcp/tree/main/xianmu-comics)
- [XianMu integration documentation](https://www.wwzu.com/mcp-docs.php)
- [XianMu pricing](https://www.wwzu.com/mcp-billing.php)
- [Tool reference](artifact/references/tools.md)
- [Reading and account workflows](artifact/references/workflows.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Conversational text with book links, page images, audio links, and purchase guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Full-book content and some interactions depend on account access, usage limits, or payment.]

## Skill Version(s):

0.1.0 (source: ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
