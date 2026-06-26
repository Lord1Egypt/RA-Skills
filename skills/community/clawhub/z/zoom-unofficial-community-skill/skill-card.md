## Description: <br>
A Python CLI for interacting with Zoom's REST API that manages meetings, recordings, team chat, AI meeting summaries, live meeting monitoring, and RTMS control. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tanchunsiong](https://clawhub.ai/user/tanchunsiong) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators use this skill to let agents manage Zoom meetings, recordings, summaries, chat, users, phone logs, and RTMS controls through Zoom's REST API after configuring OAuth credentials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can perform sensitive Zoom account actions, including delete, send-message, RTMS, and download commands. <br>
Mitigation: Use the minimum required Zoom scopes and require explicit user confirmation before executing sensitive commands. <br>
Risk: OAuth credentials and tokens can expose Zoom account access if mishandled. <br>
Mitigation: Protect the .env file, avoid committing credentials, and prefer a virtual environment for dependencies. <br>
Risk: The token cache uses a predictable temporary file path. <br>
Mitigation: Change the token cache to a private user directory with 0600 permissions before use. <br>


## Reference(s): <br>
- [Zoom Authentication Setup](references/AUTH.md) <br>
- [Zoom Marketplace](https://marketplace.zoom.us/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with inline shell commands and CLI-produced text, JSON, media, transcript, and markdown files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Zoom OAuth credentials and selected scopes; some commands may download recordings, transcripts, or summaries.] <br>

## Skill Version(s): <br>
0.0.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
