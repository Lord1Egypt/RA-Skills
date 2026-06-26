## Description: <br>
Manage a stock and crypto watchlist with target and stop alerts using live AISA price checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aisadocs](https://clawhub.ai/user/aisadocs) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to add, remove, list, and check stock or crypto watchlist entries with target, stop, and signal-change alerts. It relies on an AISA API key for live price and signal checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Watchlist ticker symbols are sent to the configured AISA-compatible API during live checks. <br>
Mitigation: Install only if this data sharing is acceptable, use a limited AISA API key, and avoid untrusted AISA_BASE_URL overrides. <br>
Risk: Generated market signals or prices may be incomplete, stale, or unsuitable for trading decisions. <br>
Mitigation: Verify market data and trading signals with reliable sources before acting on them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aisadocs/stock-watchlist-aisa-api) <br>
- [Publisher profile](https://clawhub.ai/user/aisadocs) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, JSON] <br>
**Output Format:** [Command-line text output with local JSON watchlist state] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and AISA_API_KEY; CLAWDBOT_STATE_DIR, AISA_BASE_URL, and AISA_MODEL can alter runtime behavior.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, target metadata, and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
