## Description:

This skill helps agents extract full WeChat article content and metadata from keyword searches using the BrowserAct API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ccmagia2-gif](https://clawhub.ai/user/ccmagia2-gif)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and agents use this skill to search WeChat articles by keyword and optional publication date, then retrieve article URLs, dates, authors, images, titles, and body content for monitoring, media research, trend tracking, knowledge base building, or competitor analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms and date filters are sent to the BrowserAct API.

Mitigation: Use the skill only for non-sensitive WeChat research unless the user accepts sharing those inputs with BrowserAct.

Risk: The skill requires a BrowserAct API key and the security guidance warns against sharing it in chat.

Mitigation: Configure BROWSERACT_API_KEY through a protected environment variable or secret manager, and rotate any key that was previously pasted into a conversation.

Risk: The security verdict is suspicious because the skill lacks enough user-facing scoping around third-party API use.

Mitigation: Review the skill before installing or running it, and confirm that the user understands what data will be sent to BrowserAct.

## Reference(s):

- [BrowserAct Console](https://www.browseract.com/reception/integrations)
- [BrowserAct Workflow API endpoint](https://api.browseract.com/v2/workflow)
- [ClawHub skill page](https://clawhub.ai/ccmagia2-gif/skills/wechat-article-search-api-skill)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and text or JSON-like API results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python and BROWSERACT_API_KEY; article search terms and date filters are sent to BrowserAct.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
