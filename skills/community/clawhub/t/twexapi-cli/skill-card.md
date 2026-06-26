## Description: <br>
Use this skill when the task should be done through the twexapi command-line client, including installing the CLI, configuring app or profile auth, previewing requests, and calling twexapi endpoints through convenience commands or raw paths. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yeahjjyy](https://clawhub.ai/user/yeahjjyy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to install, configure, preview, and run twexapi CLI requests for supported X/Twitter account, tweet, search, follower, list, and profile workflows. It is especially useful when the task should use the published CLI and its dry-run behavior instead of reimplementing request construction. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Saved app and profile configuration can contain API keys, cookies, auth_token values, or ct0 values in local JSON config. <br>
Mitigation: Use an isolated --config-dir or TWEXAPI_CONFIG_DIR, avoid shared machines and CI for long-lived credentials, and do not echo raw credentials in logs or prompts. <br>
Risk: Write actions can post, like, follow, unfollow, or create lists through configured social-account credentials. <br>
Mitigation: Use --dry-run before write commands and execute real write requests only after the user clearly confirms the action. <br>
Risk: The generic raw path form can send saved credentials with unexpected request targets if misused. <br>
Mitigation: Prefer convenience commands and avoid full external URLs while credentials are configured. <br>
Risk: The auth cookie workflow places auth_token material in a request path, which can be exposed through logs or traces. <br>
Mitigation: Treat command traces, terminal history, and network logs as sensitive when using auth cookie, and prefer credential isolation for testing. <br>


## Reference(s): <br>
- [Twexapi dashboard](https://twexapi.io/dashboard) <br>
- [ClawHub release page](https://clawhub.ai/yeahjjyy/twexapi-cli) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide dry-run previews, credential configuration, and twexapi command selection.] <br>

## Skill Version(s): <br>
0.1.1 (source: package.json and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
