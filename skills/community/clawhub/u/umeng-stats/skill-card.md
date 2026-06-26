## Description: <br>
Queries Umeng (友盟) U-APM crash and error statistics and U-App analytics for configured apps, including crash, ANR, error trend, affected user, daily active user, new user, launch, total user, and all-app summary data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fengerzh](https://clawhub.ai/user/fengerzh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, product owners, and operations teams use this skill to query authorized Umeng app stability and usage metrics across configured mobile and service apps. It is intended for app health checks, crash and ANR review, and daily analytics summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release packages sensitive Umeng API credentials for multiple apps. <br>
Mitigation: Install only if authorized to access those apps, treat the bundled secret as exposed, rotate or replace it, and move credentials into a private user-controlled secret or config location. <br>
Risk: The query script relies on a hard-coded local credential path. <br>
Mitigation: Fix the config path or make it user-configurable before relying on the skill in another environment. <br>
Risk: The skill can retrieve operational app analytics and stability data. <br>
Mitigation: Limit use to approved Umeng accounts and avoid sharing query outputs outside the authorized team. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/fengerzh/umeng-stats) <br>
- [Umeng Open API Gateway](https://gateway.open.umeng.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration guidance] <br>
**Output Format:** [Plain text summaries or raw JSON from a Python CLI, often presented with shell command snippets.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires authorized Umeng credentials and configured app identifiers; crash queries support a 90-day maximum date range and a documented 5 calls/second API rate limit.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, released 2026-04-16) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
