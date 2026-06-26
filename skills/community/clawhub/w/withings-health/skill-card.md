## Description: <br>
Fetches health data from the Withings API including weight, body composition, activity, and sleep data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hisxo](https://clawhub.ai/user/hisxo) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to retrieve personal Withings measurements such as weight, body composition, daily activity, and sleep history for health tracking workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill accesses sensitive Withings health data and stores OAuth account tokens locally. <br>
Mitigation: Install only when this access is acceptable; keep WITHINGS_CLIENT_SECRET, .env, and tokens.json private, and revoke the Withings authorization and delete tokens.json when the skill is no longer used. <br>


## Reference(s): <br>
- [Withings Developer Portal](https://developer.withings.com/) <br>
- [ClawHub Skill Page](https://clawhub.ai/hisxo/withings-health) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, API Calls, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js plus WITHINGS_CLIENT_ID and WITHINGS_CLIENT_SECRET environment variables; data availability depends on the connected Withings devices and account permissions.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
