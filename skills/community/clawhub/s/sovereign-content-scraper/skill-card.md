## Description: <br>
Monitors configured social channels daily to identify trending topics, viral content, and new content ideas within a user's niche, delivering structured reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ryudi84](https://clawhub.ai/user/ryudi84) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Content creators, marketers, and agents use this skill to monitor configured X/Twitter, Reddit, RSS, and YouTube sources for trends and produce daily content planning reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill fetches public or API-backed content from user-configured sources, which may include untrusted links or misleading trend signals. <br>
Mitigation: Review sources.json before use and validate important trends against source links before acting on the report. <br>
Risk: Optional Twitter API access may expose credentials if broad or shared tokens are used. <br>
Mitigation: Use scoped API credentials and rotate or revoke them if the configuration is shared or no longer needed. <br>
Risk: Daily scheduled runs and notifications may publish trend summaries or source links to an inappropriate channel. <br>
Mitigation: Confirm that the 6 AM schedule is desired and choose a notification channel suitable for the report contents. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ryudi84/sovereign-content-scraper) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Structured JSON report with trend topics, content ideas, viral formats, source evidence, and optional notification guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Saves reports to data/trend-report-{date}.json and depends on a user-provided sources.json configuration; Twitter API credentials are optional.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
