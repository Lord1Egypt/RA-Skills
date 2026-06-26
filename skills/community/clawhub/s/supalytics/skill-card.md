## Description: <br>
Query web analytics data using the Supalytics CLI for pageviews, visitors, top pages, traffic sources, referrers, countries, revenue metrics, conversions, funnels, events, and realtime visitors. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yogesharc](https://clawhub.ai/user/yogesharc) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External developers and site operators use this skill to query Supalytics web analytics, inspect traffic and revenue metrics, manage sites, and produce CLI queries for reporting or troubleshooting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Setup instructions include remote installation and admin-level symlink commands. <br>
Mitigation: Review installation commands before execution, prefer a user-local PATH setup, and avoid running remote install scripts blindly. <br>
Risk: The skill can guide site create, update, default, and remove operations through the Supalytics CLI. <br>
Mitigation: Only run administrative site commands after the user explicitly requests the change and confirms the target site. <br>
Risk: OAuth login requires browser interaction and may expose a verification URL during agent-assisted authentication. <br>
Mitigation: Present the verification URL only to the intended user and poll the background login session without storing credentials in the skill. <br>


## Reference(s): <br>
- [Supalytics](https://supalytics.co) <br>
- [Bun runtime](https://bun.sh) <br>
- [ClawHub release page](https://clawhub.ai/yogesharc/supalytics) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and optional JSON-oriented CLI examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Supalytics CLI commands, setup guidance, filters, metric and dimension choices, troubleshooting steps, and JSON output guidance.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
