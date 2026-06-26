## Description: <br>
SlonAide helps agents query, search, and summarize AiDeNote recording notes, including transcripts, AI summaries, tags, folders, and optional remote OpenClaw bridge setup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ajingmiao](https://clawhub.ai/user/ajingmiao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and end users connect OpenClaw to SlonAide or AiDeNote accounts to retrieve recording-note lists, view note details, search notes, and summarize recent recordings. Users who need mobile remote access can optionally install and check a local AiDeNote OpenClaw bridge on macOS or Windows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The optional remote bridge downloads and runs installer scripts, creates login persistence, and can access the user's SlonAide API key and local OpenClaw connection. <br>
Mitigation: Install the bridge only when remote AiDeNote access is needed, review or verify installer sources first, understand the created auto-start service, and run it only on machines where exposing those credentials and the local OpenClaw connection is acceptable. <br>
Risk: The skill requires sensitive API credentials for note access. <br>
Mitigation: Use a dedicated SlonAide API key, store it through OpenClaw configuration, rotate it if exposed, and avoid sharing full transcript or note output in contexts where private recordings should not be disclosed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ajingmiao/slonaide) <br>
- [AiDeNote Web App](https://h5.aidenote.cn/) <br>
- [SlonAide Web App](https://h5.slonaide.cn/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown-style text with structured note summaries, API status messages, shell commands, and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include truncated transcript text, AI summaries, note metadata, bridge status, and installation results.] <br>

## Skill Version(s): <br>
3.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
