## Description: <br>
Uno CLI lets an agent search for external tools, inspect schemas, authenticate with Uno, and call selected tools through a command-line client. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lxyd-ai](https://clawhub.ai/user/lxyd-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill when an agent needs real-time data or actions from external services through a search, inspect, authenticate, and call workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent broad authenticated access to external tools and services. <br>
Mitigation: Install only when the publisher and clawdtools.uno are trusted, and require explicit user confirmation before calls that spend credits, change keys, publish content, or modify third-party data. <br>
Risk: Credentials such as UNO_API_KEY, login output, and ~/.uno/credentials.json can grant access to the Uno account. <br>
Mitigation: Treat all credential material as secret, prefer a dedicated low-privilege account or API key, and avoid exposing credential values in logs or chat. <br>
Risk: The API base URL can be changed with a flag or environment variable. <br>
Mitigation: Verify the configured API base URL before authentication or tool calls, especially when using UNO_API_URL or --base-url. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lxyd-ai/uno-cli) <br>
- [Uno homepage](https://clawdtools.uno) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON command outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python 3.8+, Uno authentication, and access to https://clawdtools.uno unless the API base URL is explicitly overridden.] <br>

## Skill Version(s): <br>
1.1.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
