## Description: <br>
Advanced Shodan API interactions including search, scan, alerts, and DNS. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dmcmurrin4617](https://clawhub.ai/user/dmcmurrin4617) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and security practitioners use this skill to run Shodan searches, host lookups, DNS lookups, account queries, scans, alert management, exploit search, and realtime stream commands through an AI agent. It is intended for authorized security research and asset monitoring with a configured Shodan API key. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can trigger Shodan active scans and persistent account changes such as alert creation. <br>
Mitigation: Require manual approval before scan, alert creation, exploit search, or realtime stream commands, and limit use to authorized assets. <br>
Risk: Shodan API credentials are required and may grant account-level access. <br>
Mitigation: Store the API key outside prompts and files, use environment or Shodan CLI configuration controls, and rotate the key if exposure is suspected. <br>
Risk: Queries, targets, and monitoring requests are sent to Shodan. <br>
Mitigation: Assume submitted targets leave the local environment and avoid sending data unless the user is authorized to assess it. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/dmcmurrin4617/shodan-skill) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/dmcmurrin4617) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, API calls, Configuration guidance] <br>
**Output Format:** [Markdown guidance with shell commands; the bundled script returns JSON responses.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3, pip, the shodan Python package, and a Shodan API key configured through SHODAN_API_KEY or the Shodan CLI configuration.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
