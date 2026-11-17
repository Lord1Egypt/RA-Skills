## Description:

ToolDeck helps agents save and retrieve user-confirmed tool or service URLs by extracting details, categorizing entries, and storing them in a personal database.

This skill is ready for commercial/non-commercial use.

## Publisher:

[almohalhel1408](https://clawhub.ai/user/almohalhel1408)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent operators use ToolDeck to remember public tools or services they explicitly ask an agent to save, then retrieve saved entries by category, search, or full listing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may fetch and store information from URLs, which can expose private, authenticated, paywalled, intranet, or token-bearing pages if used carelessly.

Mitigation: Use it only for public URLs that the user explicitly asks to save; skip authenticated, paywalled, CAPTCHA-protected, robots.txt-disallowed, private, intranet, personal-data, or token-bearing URLs.

Risk: Saved URL records can retain sensitive query parameters or unnecessary tracking data.

Mitigation: Strip OAuth tokens, API keys, session IDs, and tracking parameters such as utm_* or fbclid before saving.

Risk: Automatically saved or suggested entries could surprise users or add unwanted data to the personal database.

Mitigation: Confirm intent before scraping, save only after user confirmation, and provide tool suggestions only when explicitly requested.

## Reference(s):

- [ToolDeck database schema and seed data](references/database.json)

## Skill Output:

**Output Type(s):** [text, JSON, guidance]

**Output Format:** [Plain text or Markdown responses with JSON-compatible database records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires explicit user intent and confirmation before saving entries.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
