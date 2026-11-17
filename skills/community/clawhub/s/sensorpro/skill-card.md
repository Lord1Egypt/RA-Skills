## Description:

Manage your Sensorpro email marketing account in OpenClaw.

This skill is ready for commercial/non-commercial use.

## Publisher:

[forcequit](https://clawhub.ai/user/forcequit)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to configure an agent for Sensorpro email marketing account tasks, including contact management, campaign metrics, relay email, imports, and account administration through the Sensorpro REST API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The agent may send email or create broadcasts to real recipients.

Mitigation: Require explicit human approval before sending relay email, creating broadcasts, or otherwise contacting real recipients.

Risk: The agent may delete contacts, invoke ForgetMe, or change contact status in a live marketing account.

Mitigation: Require approval for destructive contact actions and prefer a dedicated least-privilege API user where Sensorpro supports it.

Risk: Sensorpro credentials and API keys can grant account access if exposed.

Mitigation: Keep credentials out of repositories, store them in the runtime environment, and rotate keys if they are exposed.

Risk: Account-user or sub-organization changes can alter account administration.

Mitigation: Require explicit approval before changing account users or creating sub-organizations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/forcequit/skills/sensorpro)
- [Skill homepage](https://github.com/forcequit/openclaw-sensorpro)
- [Sensorpro API home](https://sensorpro.net/api/)
- [Sensorpro contacts API](https://sensorpro.net/api/contacts.html)
- [Sensorpro campaigns and metrics API](https://sensorpro.net/api/campaigns.html)
- [Sensorpro relay email API](https://sensorpro.net/api/sendemail.html)
- [Sensorpro imports API](https://www.sensorpro.net/api/imports.html)
- [Sensorpro account API](https://sensorpro.net/api/account.html)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with shell command examples and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses Sensorpro credentials and API tokens supplied through environment variables.]

## Skill Version(s):

0.2.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
