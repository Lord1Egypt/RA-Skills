## Description:

Uses Playwright to connect to a user's logged-in Chrome browser and compose and publish posts on X (Twitter).

This skill is ready for commercial/non-commercial use.

## Publisher:

[1067873313](https://clawhub.ai/user/1067873313)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to let an agent post requested content to X through a logged-in local Chrome session. It is useful for assisted social posting workflows where the user controls the browser account and invocation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires broad access to a logged-in Chrome session.

Mitigation: Use only a dedicated Chrome profile or disposable account, keep the CDP port bound to localhost, and close the debugging-enabled browser immediately after use.

Risk: The skill includes tweet-reading capability beyond simple posting.

Mitigation: Review the code before installing and invoke the skill only for explicit user-requested posting or account-checking tasks.

Risk: Dependencies are not pinned by a lockfile in the artifact.

Mitigation: Pin dependencies and add a lockfile before trusting the skill in a real account workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/1067873313/skills/x-twitter-poster)
- [Publisher profile](https://clawhub.ai/user/1067873313)
- [Artifact README](artifact/README.md)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JavaScript and shell command examples; runtime calls return JSON-like status objects.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses CDP_URL and X_USERNAME configuration and operates through the user's active Chrome and X session.]

## Skill Version(s):

0.1.3 (source: server release metadata; artifact/package.json lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
