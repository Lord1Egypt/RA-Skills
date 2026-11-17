## Description:

Searches Knowledge Planet for a keyword, switches to joined-group topic results sorted by newest, and returns structured search results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[barryyjj](https://clawhub.ai/user/barryyjj)

### License/Terms of Use:

MIT-0

## Use Case:

Agents use this skill to answer user requests that require searching joined Knowledge Planet communities for recent topic posts matching specific keywords.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Searches may return private or paid content from Knowledge Planet communities available through the logged-in browser profile.

Mitigation: Use narrow keywords or current-group search when broad cross-community retrieval is not appropriate.

Risk: The skill depends on an active logged-in browser session for Knowledge Planet.

Mitigation: If the session has expired or redirects to login, pause and ask the user to restore the browser login before retrying.

## Reference(s):

- [Zsxq Search on ClawHub](https://clawhub.ai/barryyjj/skills/zsxq-search)
- [Knowledge Planet web app](https://wx.zsxq.com)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown or plain text search-result summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search results are summarized without exposing intermediate browser-navigation steps.]

## Skill Version(s):

1.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
