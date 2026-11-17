## Description:

Check and control a Wyze smart lock, including status, lock, and unlock, through an unofficial Wyze API client.

This skill is ready for commercial/non-commercial use.

## Publisher:

[noelportugal](https://clawhub.ai/user/noelportugal)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to check Wyze lock status, lock a named Wyze smart lock, or unlock a named Wyze smart lock after explicit confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unlock commands can open a physical door and are not safely enforced at the command boundary.

Mitigation: Require a specific lock name, restate the target lock, and obtain explicit confirmation before invoking unlock.

Risk: The skill needs Wyze credentials and cached tokens that can control the lock.

Mitigation: Install only in trusted environments, protect the Wyze environment file and token directory, and limit access to agents authorized to control the lock.

Risk: Shared or untrusted conversations can create ambiguous or unauthorized unlock requests.

Mitigation: Refuse vague unlock requests and confirm out of band before unlocking from shared channels.

Risk: The skill uses an unofficial Wyze client and Wyze API behavior may change.

Mitigation: Monitor command results, pin dependencies where practical, and review updates before relying on the skill for routine access control.

## Reference(s):

- [ClawHub Wyze Lock release](https://clawhub.ai/noelportugal/skills/wyze-lock)
- [wyze-node npm package](https://www.npmjs.com/package/wyze-node)
- [Wyze Developer API key console](https://developer-api-console.wyze.com/#/apikey/view)
- [wyze-node GitHub project](https://github.com/noelportugal/wyze-node)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Markdown guidance with shell command examples and plain-text CLI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js, Wyze API credentials, and a cached Wyze login token.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
