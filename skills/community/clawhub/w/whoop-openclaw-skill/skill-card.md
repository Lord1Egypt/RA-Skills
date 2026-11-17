## Description:

Fetches and analyzes Whoop recovery, strain, sleep, HRV, workout, and profile data through OAuth-authenticated Whoop API calls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vraj1512](https://clawhub.ai/user/vraj1512)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to connect a Whoop account, retrieve personal recovery, sleep, strain, HRV, and workout metrics, and generate daily briefings or trend-based training and recovery guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests access to sensitive Whoop health data and stores OAuth access and refresh tokens locally.

Mitigation: Use a local redirect flow or trusted secret store, restrict token and config file permissions, and revoke Whoop authorization if a token or authorization code is exposed.

Risk: The OAuth redirect page can display and copy authorization codes or tokens, and the artifact suggests sending them through chat apps.

Mitigation: Do not send authorization codes, client secrets, access tokens, or refresh tokens through chat apps; exchange and store them only in a trusted local environment.

Risk: The skill can generate training and recovery recommendations from personal metrics.

Mitigation: Treat generated recommendations as wellness guidance and review them against personal context before acting on them.

## Reference(s):

- [Whoop API Reference](references/whoop-api.md)
- [OAuth Pages for Whoop Integration](references/oauth-pages/README.md)
- [Whoop Developer Docs](https://developer.whoop.com/)
- [Whoop Developer App Settings](https://app.whoop.com/settings/developer)
- [ClawHub Skill Page](https://clawhub.ai/vraj1512/skills/whoop-openclaw-skill)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, JSON configuration examples, and optional JSON API summaries.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May run local Python scripts and make Whoop API requests after the user completes OAuth setup.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
