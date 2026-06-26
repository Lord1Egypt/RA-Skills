## Description: <br>
WHOOP CLI with health insights, trends analysis, and data fetching for sleep, recovery, HRV, strain, workouts, and related profile data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[koala73](https://clawhub.ai/user/koala73) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and WHOOP users use this skill to authenticate with the WHOOP API, fetch personal health and fitness metrics, and produce JSON or human-readable summaries, trends, and recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access sensitive WHOOP health and profile data. <br>
Mitigation: Use it only with trusted accounts and avoid sharing terminal output, logs, or generated JSON that may contain personal health information. <br>
Risk: WHOOP client secrets and OAuth tokens can grant continued access if exposed. <br>
Mitigation: Protect WHOOP_CLIENT_SECRET, keep .env files out of source control, restrict token file permissions, and run whoopskill auth logout or revoke the WHOOP app when access is no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/koala73/whoopskill) <br>
- [Publisher profile](https://clawhub.ai/user/koala73) <br>
- [npm package](https://www.npmjs.com/package/whoopskill) <br>
- [WHOOP Developer Portal](https://developer.whoop.com) <br>
- [README](README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [JSON by default, with optional human-readable CLI text for summaries, trends, insights, and fetched WHOOP records.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js, WHOOP API credentials, and OAuth authentication; output may contain sensitive personal health and profile data.] <br>

## Skill Version(s): <br>
1.1.0 (source: package.json and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
