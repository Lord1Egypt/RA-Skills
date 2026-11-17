## Description:

Fetch personalized daily horoscope forecasts from zodiac-today.com API based on natal chart calculations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dowands](https://clawhub.ai/user/dowands)

### License/Terms of Use:


## Use Case:

External users use this skill to fetch personalized daily horoscope guidance, lucky colors and numbers, and planning suggestions based on a stored birth-chart profile.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks for sensitive personal data including email, birth date, and birth city.

Mitigation: Collect this information only with explicit user consent, send it only to zodiac-today.com, and avoid logging or sharing it in public contexts.

Risk: The setup flow permits an agent to retrieve email verification codes automatically if mailbox access is available.

Mitigation: Keep verification human-in-the-loop: users should read and enter verification codes manually instead of granting mailbox or IMAP access.

Risk: Horoscope output may be mistaken for reliable advice for consequential decisions.

Mitigation: Present results as entertainment or reflection and avoid using them as the basis for financial, employment, health, safety, or legal decisions.

## Reference(s):

- [Zodiac Today API Reference](references/api.md)
- [Zodiac Today Dashboard](https://zodiac-today.com/en/dashboard)
- [Zodiac Horoscope ClawHub Release](https://clawhub.ai/dowands/skills/zodiac-horoscope)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with optional inline shell commands and API response summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Zodiac Today API key and profile ID; horoscope guidance should be treated as entertainment or reflection.]

## Skill Version(s):

1.3.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
