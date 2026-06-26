## Description: <br>
Monitors Vercel-hosted deployments with health checks, cache freshness verification, and Vercel API validation so teams can confirm releases succeeded. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivanpruss](https://clawhub.ai/user/ivanpruss) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operations engineers use this skill to monitor web applications they own after Vercel deployments, validate homepage and API health, and prepare scheduled watchdog checks with alerting through the agent platform. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: URL validation may be weaker than described, especially if arbitrary URLs are supplied to the agent. <br>
Mitigation: Review or patch URL validation before installation, and only monitor URLs you own or are authorized to monitor. <br>
Risk: A Vercel token is required for API-backed deployment monitoring. <br>
Mitigation: Use a least-privilege Vercel token and provide it through VERCEL_TOKEN or another controlled secret path. <br>
Risk: Scheduled or background monitoring can create repeated network checks and notifications. <br>
Mitigation: Configure cron or sub-agent jobs deliberately with a clear schedule, target URLs, and notification channel. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ivanpruss/vercel-deployment-watchdog) <br>
- [Vercel API Base URL](https://api.vercel.com) <br>
- [Vercel Account Tokens](https://vercel.com/account/tokens) <br>
- [curl](https://curl.se/) <br>
- [jq](https://stedolan.github.io/jq/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with bash commands and optional JSON script output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Scripts require curl and jq, use VERCEL_TOKEN for Vercel API access, and may write watchdog state to a local JSON file.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
