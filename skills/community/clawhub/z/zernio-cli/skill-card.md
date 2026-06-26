## Description: <br>
Schedule and manage social media posts across 14 platforms from the CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mikipalet](https://clawhub.ai/user/mikipalet) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and AI agents use this skill to authenticate with Zernio, manage profiles and connected social accounts, create or schedule posts, upload media, and retrieve analytics from the command line. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The CLI can act on connected Zernio social accounts, including publishing, retrying, uploading media, and deleting posts or profiles. <br>
Mitigation: Use it only with accounts where this authority is acceptable, and require explicit agent confirmation before actions that publish, retry, upload, or delete content. <br>
Risk: API keys may be exposed if pasted into shared terminals, logs, transcripts, or unprotected config files. <br>
Mitigation: Prefer browser login or protected environment secrets, avoid sharing real keys in transcripts, and protect ~/.zernio/config.json. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/mikipalet/zernio-cli) <br>
- [Zernio Documentation](https://docs.zernio.com) <br>
- [Zernio Homepage](https://zernio.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON command output expectations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands return compact JSON by default and support pretty-printed JSON with --pretty.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
