## Description:

Monitors configured stock symbols and sends alerts through email and optional Sonos voice announcements when price movement or price thresholds are triggered.

This skill is for research and development only.

## Publisher:

[terrycarter1985](https://clawhub.ai/user/terrycarter1985)

### License/Terms of Use:

Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International

## Use Case:

External users and developers use this skill to monitor a configured stock watchlist and receive threshold-based alerts through console output, email, or local Sonos voice announcements.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Malformed alert values in the local configuration can lead to command execution in the alert script.

Mitigation: Use only a trusted, locally controlled config file and validate symbols, prices, percentages, and polling intervals before running the skill.

Risk: SMTP credentials may be exposed through command-line arguments when email alerts are enabled.

Mitigation: Prefer a dedicated app-specific SMTP password and avoid treating the skill as low risk until credential handling is fixed.

Risk: Watched symbols and alerts may be sent to external services or local Sonos devices.

Mitigation: Use a dedicated Alpha Vantage key and enable only notification channels approved for the portfolio data being monitored.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/terrycarter1985/skills/stock-price-alert)
- [Stock Price Alert README](artifact/README.md)
- [Stock Price Alert skill documentation](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, shell commands, JSON configuration, and plain text alert output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and jq; optional notifications use SMTP settings and a local Sonos CLI.]

## Skill Version(s):

3.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
