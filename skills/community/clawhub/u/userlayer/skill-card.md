## Description: <br>
Use this skill when the user wants a UserLayer report for an App Store or Google Play app, including full analysis, polling, and follow-up questions grounded in real reviews. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[houyongsheng](https://clawhub.ai/user/houyongsheng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, product teams, and market researchers use this skill to analyze App Store or Google Play reviews, surface pain points, user segments, and market opportunities, and ask follow-up questions grounded in cited reviews. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a paid UserLayer API credential and documented per-analysis or query costs can accrue. <br>
Mitigation: Use a scoped API key, confirm the requested analysis size before increasing max_reviews, and monitor reported usage and cost fields. <br>
Risk: Changing LAUNCHBASE_API_URL can route credentials and requests to an alternate API host. <br>
Mitigation: Leave LAUNCHBASE_API_URL unset unless the alternate endpoint is specifically trusted. <br>


## Reference(s): <br>
- [UserLayer ClawHub release](https://clawhub.ai/houyongsheng/userlayer) <br>
- [Default UserLayer API host](https://lb-api.workflowhunt.com) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Analysis, JSON, Guidance] <br>
**Output Format:** [JSON responses with analysis results, status payloads, usage data, and cited sources] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires API_KEY; LAUNCHBASE_API_URL can override the default host.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
