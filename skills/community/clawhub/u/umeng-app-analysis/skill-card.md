## Description:

Queries Umeng+ Open API data for mobile app analytics, including app lists, summary metrics, active and new users, launches, retention, session duration, channel and version breakdowns, and custom event analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leowing](https://clawhub.ai/user/leowing)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analytics engineers use this skill to fetch Umeng+ mobile app metrics and user behavior data from authenticated Open API endpoints. It supports operational analysis of app performance, channels, versions, retention, usage duration, and custom events.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires Umeng analytics credentials for authenticated API access.

Mitigation: Run it in an isolated environment, provide credentials only at runtime, and use least-privilege Umeng credentials.

Risk: The package contains broader authenticated SDK wrappers than the documented commands, including account-changing capabilities.

Mitigation: Review commands before execution and require explicit approval before account-changing API use such as creating apps or events.

Risk: Dependency and API behavior may affect the integrity of analytics results or command execution.

Mitigation: Pin dependencies, review JSON responses before using them in decisions, and handle API error objects explicitly.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/leowing/skills/umeng-app-analysis)
- [Commands Reference](references/commands.md)
- [SDK README](sdk/README.md)
- [Umeng Open API Signature Documentation](https://open.1688.com/api/sysSignature.htm)
- [Umeng App Daily Data API](https://open.1688.com/api/api.htm?ns=com.umeng.uapp&n=umeng.uapp.getDailyData&v=1&cat=default)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Shell commands, Configuration instructions, Guidance]

**Output Format:** [JSON responses and Markdown guidance with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires UMENG_API_KEY and UMENG_API_SECURITY environment variables; failed calls return a JSON error object.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
