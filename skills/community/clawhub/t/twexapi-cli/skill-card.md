## Description:

Use this skill when the task should be done through the twexapi command-line client, including installing the CLI, configuring app or profile auth, previewing requests, and calling twexapi endpoints through convenience commands or raw paths.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yeahjjyy](https://clawhub.ai/user/yeahjjyy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to install and run the twexapi CLI, configure API keys or Twitter/X session profiles, preview requests, and call supported Twexapi endpoints through convenience commands or raw paths.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The CLI stores Twexapi API keys and Twitter/X session material locally in plaintext.

Mitigation: Use isolated config directories on shared machines or CI, keep config directories private, and avoid saving long-lived profiles where unnecessary.

Risk: The CLI can send authenticated write requests on behalf of a configured profile.

Mitigation: Use --dry-run before write actions and execute real requests only after the user clearly confirms the intended action.

Risk: The auth cookie flow places auth_token material in a request path, which can expose secrets in logs or traces.

Mitigation: Avoid logging raw command lines or request paths that contain auth_token values and treat related traces as sensitive.

Risk: Custom base URLs and generic full-URL requests can direct authenticated requests outside the expected Twexapi service boundary.

Mitigation: Do not use untrusted --base-url values and avoid generic full-URL requests when credentials are configured.

## Reference(s):

- [Twexapi dashboard](https://twexapi.io/dashboard)
- [ClawHub skill page](https://clawhub.ai/yeahjjyy/skills/twexapi-cli)

## Skill Output:

**Output Type(s):** [shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON command output when requests are executed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill may guide authenticated CLI requests and dry-run previews; responses depend on Twexapi endpoints and local credentials.]

## Skill Version(s):

0.1.1 (source: package.json and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
