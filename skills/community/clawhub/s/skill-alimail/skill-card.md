## Description: <br>
Provides AliMail API access for querying mailbox users, retrieving message details, and searching mail with KQL. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vber](https://clawhub.ai/user/vber) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Administrators and support engineers use this skill to inspect authorized AliMail tenant user profiles and mailbox records for operational troubleshooting, compliance review, or message lookup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read sensitive AliMail user and mailbox data. <br>
Mitigation: Install only for authorized AliMail tenant administration and use the minimum read-only permissions needed. <br>
Risk: ALMAIL_SECRET exposure could allow unauthorized access through the configured AliMail app. <br>
Mitigation: Protect and rotate ALMAIL_SECRET and avoid storing it in prompts, logs, or committed files. <br>
Risk: Full message bodies may contain sensitive or regulated content. <br>
Mitigation: Avoid retrieving or logging full message bodies unless there is a clear business need. <br>
Risk: The npm SDK dependency affects the security posture of runtime API calls. <br>
Mitigation: Pin or review the alimail-node-sdk version before deployment. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/vber/skill-alimail) <br>
- [AliMail API reference](references/alimail-api.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON API results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ALMAIL_APP_ID and ALMAIL_SECRET for OAuth2 client credentials.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
