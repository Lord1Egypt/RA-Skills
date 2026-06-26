## Description: <br>
Query AI-generated trading signals from vibetrading-datahub. Signals are produced by autonomous agents analyzing whale activity, news, funding rates, and technical indicators. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liuhaonan00](https://clawhub.ai/user/liuhaonan00) <br>

### License/Terms of Use: <br>
ISC <br>


## Use Case: <br>
External users and developers use this skill to query public VibeTrading crypto market signal endpoints for latest, symbol-specific, or signal-type-specific analysis. The results support market monitoring and independent review, not automated trade execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Trading signals may be incomplete, stale, or misleading if used without independent validation. <br>
Mitigation: Treat returned signals as informational, verify them against other data sources, and apply appropriate risk management before making trading decisions. <br>
Risk: The skill runs npm dependencies and makes outbound HTTPS requests to vibetrading.dev. <br>
Mitigation: Install only in environments where those dependencies and outbound requests are acceptable, and review dependency updates before deployment. <br>
Risk: Scheduled checks can create recurring market monitoring that users may not intend. <br>
Mitigation: Enable cron or OpenClaw scheduling only when recurring checks are intentional and frequency limits are understood. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/liuhaonan00/vibetrading-global-signals) <br>
- [VibeTrading API base](https://vibetrading.dev/api/v1) <br>
- [README](README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Console text with summarized signal analysis and markdown excerpts from JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires outbound HTTPS requests to vibetrading.dev and local Node.js dependencies; no API token is documented as required.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact package.json and CHANGELOG report 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
