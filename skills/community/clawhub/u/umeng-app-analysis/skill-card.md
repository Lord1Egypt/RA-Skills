## Description: <br>
Umeng App Analysis helps agents query Umeng Open API data for mobile app statistics, including app lists, summary metrics, active and new users, launches, retention, session duration, channel or version breakdowns, and custom event analytics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leowing](https://clawhub.ai/user/leowing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators with Umeng API credentials use this skill to retrieve mobile app analytics through documented CLI commands and inspect the returned JSON for reporting or troubleshooting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires Umeng API credentials that may expose analytics data or account actions. <br>
Mitigation: Use least-privilege Umeng credentials, avoid broad production credentials, and provide secrets only through the documented environment variables. <br>
Risk: The artifact includes write or admin-capable API wrappers beyond ordinary analytics querying. <br>
Mitigation: Limit agent use to the documented CLI commands and require review before any create, edit, or back-report action is run. <br>
Risk: Incorrect app keys, date ranges, channels, versions, or event identifiers can return misleading analytics or trigger unintended API calls. <br>
Mitigation: Validate command parameters against the documented command reference before execution and review returned JSON before using it for decisions. <br>


## Reference(s): <br>
- [Command Reference](references/commands.md) <br>
- [Umeng Open API Signature Documentation](https://open.1688.com/api/sysSignature.htm) <br>
- [ClawHub Skill Page](https://clawhub.ai/leowing/umeng-app-analysis) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Shell commands, Guidance] <br>
**Output Format:** [JSON from CLI execution with Markdown command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires UMENG_API_KEY and UMENG_API_SECURITY environment variables; failed API calls return a JSON error object and exit with status 1.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
