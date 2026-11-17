## Description:

Provides AliMail API access for querying enterprise mailbox user information, retrieving message details, and searching messages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vber](https://clawhub.ai/user/vber)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and workspace administrators use this skill to run AliMail SDK scripts that inspect enterprise mailbox users, retrieve individual messages, and search mail with KQL when they have authorized credentials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles organization mailbox data and can print user profile data or full email content to the terminal.

Mitigation: Run it only with an authorized AliMail application, restrict access to users with a business need, and treat terminal output and logs as sensitive.

Risk: Credentialed API access may be over-privileged if read-write scopes are granted for read-oriented scripts.

Mitigation: Grant least-privilege read-only scopes where possible and avoid read-write scopes unless a specific workflow requires them.

Risk: The skill installs and executes the alimail-node-sdk npm dependency.

Mitigation: Pin and review the npm dependency before installation and before accepting updates.

## Reference(s):

- [AliMail API Reference](references/alimail-api.md)
- [AliMail API Endpoint](https://alimail-cn.aliyuncs.com)
- [ClawHub Skill Page](https://clawhub.ai/vber/skills/skill-alimail)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown summaries with shell commands and JSON API results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires ALMAIL_APP_ID and ALMAIL_SECRET; script output may include user profile data and full email content.]

## Skill Version(s):

0.1.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
