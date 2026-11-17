## Description:

Monitor Steam game prices and alert when a game hits historical low or a user target price.

This skill is ready for commercial/non-commercial use.

## Publisher:

[g-zoe](https://clawhub.ai/user/g-zoe)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to keep a local watchlist of Steam games, check current Steam prices, and receive command-line alerts when a watched game is discounted or reaches a target price.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Historical-low alerts may not match the advertised behavior because the security review says the code may alert on any discount rather than a true historical low.

Mitigation: Treat alerts as discount or target-price notifications unless historical-low behavior is fixed or documented clearly.

Risk: Price checks use China-region Steam pricing in CNY, which may not match a user's expected Steam region or currency.

Mitigation: Confirm the target region and currency before relying on alerts for purchasing decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/g-zoe/skills/steam-lowest-price-skill)
- [CheapShark games API](https://www.cheapshark.com/api/1.0/games)
- [Steam Store appdetails API](https://store.steampowered.com/api/appdetails)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration]

**Output Format:** [Plain text alerts and Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Maintains local JSON watchlist and state files; price checks use China-region Steam pricing in CNY.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
