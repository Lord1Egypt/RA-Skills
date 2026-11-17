## Description:

Manages stock and cryptocurrency watchlists with AISA live price checks, target prices, stop-loss alerts, and signal-change checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aisadocs](https://clawhub.ai/user/aisadocs)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to add, remove, list, and check watched stock or cryptocurrency symbols, including target-price, stop-loss, and signal-change alerts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: AISA_BASE_URL can redirect the AISA API key and watched tickers to a replacement endpoint.

Mitigation: Keep AISA_BASE_URL unset unless the replacement endpoint is intentionally configured and trusted.

Risk: The generated local watchlist can reveal private tickers or alert levels.

Mitigation: Keep the .clawdbot watchlist file out of commits and use a private CLAWDBOT_STATE_DIR when needed.

Risk: The release security verdict is suspicious and calls for review before installation.

Mitigation: Install and run the skill only in a controlled environment after reviewing the release security guidance.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aisadocs/skills/stock-watchlist-zh)
- [AISA API endpoint](https://api.aisa.one/v1)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with command examples, configuration notes, and summarized watchlist status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update a local JSON watchlist file under .clawdbot unless CLAWDBOT_STATE_DIR is set.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
