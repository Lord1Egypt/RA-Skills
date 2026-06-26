## Description: <br>
Fetches health data from the Withings API for multiple family members, including weight, body composition, activity, and sleep. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[odrobnik](https://clawhub.ai/user/odrobnik) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to authenticate family members' Withings accounts and retrieve weight, body composition, activity, and sleep data for health-history questions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Withings health data and OAuth tokens are sensitive personal data. <br>
Mitigation: Install only for accounts whose owners have authorized access, keep the local skill directory and token files private, and delete token files or revoke Withings app access when access is no longer needed. <br>
Risk: Body-composition history can expose broad historical health information. <br>
Mitigation: Use explicit limits for body-composition history when broad historical output is not needed. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/odrobnik/withings-family) <br>
- [Withings Developer Portal](https://developer.withings.com/) <br>
- [Withings OAuth authorization endpoint](https://account.withings.com/oauth2_user/authorize2) <br>
- [Withings OAuth token endpoint](https://wbsapi.withings.net/v2/oauth2) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON CLI output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns Withings account data only after OAuth authorization; activity and sleep commands accept day-count limits, and body composition can be limited or requested in full.] <br>

## Skill Version(s): <br>
1.1.2 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
