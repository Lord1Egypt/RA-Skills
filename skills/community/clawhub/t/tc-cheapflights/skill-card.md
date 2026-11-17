## Description:

Queries and monitors discounted flight prices from third-party travel sources, parses Chinese natural-language route/date requests, and can send Feishu price-drop notifications.

This skill is for research and development only.

## Publisher:

[qi812560784](https://clawhub.ai/user/qi812560784)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use this skill to query China-focused flight prices, create route or flight price monitors, and receive price-drop alerts through a configured Feishu webhook.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: The skill can present fabricated, mock, or fallback flight prices as usable fare results.

Mitigation: Require outputs to distinguish live-source results from mock or fallback data, keep mock data disabled for real use, and verify fares directly with the travel provider before purchase.

Risk: Monitoring and price-drop notification behavior may be overstated or unverified.

Mitigation: Test subscription creation, scheduled checks, threshold handling, and Feishu delivery before relying on the skill for real alerts.

Risk: Feishu notifications can disclose route, date, and price information to the configured webhook destination.

Mitigation: Configure Feishu webhooks only for trusted channels and avoid sending sensitive travel plans to shared or untrusted rooms.

Risk: Installation writes persistent local skill files and dependencies with limited safeguards.

Mitigation: Review the skill before installing, use a virtual environment with pinned dependencies, and install into a scoped EasyClaw/OpenClaw profile.

## Reference(s):

- [API documentation](artifact/references/api_documentation.md)
- [City and airport codes](artifact/references/city_airport_codes.md)
- [Natural language examples](artifact/references/natural_language_examples.md)
- [ClawHub skill page](https://clawhub.ai/qi812560784/skills/tc-cheapflights)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown or plain text responses with optional Python and shell snippets plus JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include parsed route/date parameters, flight listings, price analysis, subscription status, notification setup guidance, and local configuration paths.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
