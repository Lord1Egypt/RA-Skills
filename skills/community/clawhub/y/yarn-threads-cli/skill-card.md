## Description: <br>
Interact with Threads by Meta through yarn-threads-cli to read feeds, likes, saved posts, threads, profiles, and search results, and to post, reply, or quote after authentication. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jeizzon](https://clawhub.ai/user/jeizzon) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, operators, and social-media automation users use this skill to ask an agent for Threads CLI commands, authentication guidance, feed/profile lookup, and publishing actions. It is useful when the agent should access Threads data or prepare explicit post, reply, or quote commands through the user's authenticated browser profile or session tokens. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The underlying CLI can use Threads browser sessions or manual cookies, exposing account access if session IDs, CSRF tokens, or user IDs are shared insecurely. <br>
Mitigation: Treat session values like passwords, avoid placing them in visible command lines or chats, and prefer browser-profile authentication when appropriate. <br>
Risk: Posting, replying, or quoting can publish from the user's Threads account. <br>
Mitigation: Require explicit user confirmation before any publish command is run, including the exact text and target thread when applicable. <br>


## Reference(s): <br>
- [yarn-threads Command Reference](references/commands.md) <br>
- [yarn-threads-cli documentation](https://github.com/jeizzon/yarn-threads-cli) <br>
- [ClawHub skill page](https://clawhub.ai/jeizzon/yarn-threads-cli) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline CLI commands, flags, and short examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include JSON-output recommendations for downstream parsing when the CLI supports --json or --json-full.] <br>

## Skill Version(s): <br>
0.1.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
