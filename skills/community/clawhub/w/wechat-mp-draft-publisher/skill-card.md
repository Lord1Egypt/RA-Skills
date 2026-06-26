## Description: <br>
Publish WeChat Official Account draft articles through a packaged CLI executable that wraps WeChat API calls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mesus](https://clawhub.ai/user/mesus) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to create WeChat Official Account draft articles from local content and image files. It guides the agent through the required getAuth, image upload, cover upload, and addDraft sequence. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can download and run an executable from a GitHub release or direct URL. <br>
Mitigation: Prefer a locally audited binary supplied with --bin or MP_WECHAT_CLI_BIN, and avoid direct URL or latest-release auto-download modes unless the executable has been independently reviewed. <br>
Risk: Normal JSON output includes a WeChat access token. <br>
Mitigation: Treat command output as sensitive, do not paste it into shared logs or tickets, and redact access_token before sharing results. <br>
Risk: GITHUB_TOKEN may be used during release download paths. <br>
Mitigation: Unset GITHUB_TOKEN before using download mode unless authenticated GitHub API access is explicitly required. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mesus/wechat-mp-draft-publisher) <br>
- [CLI Contract](references/cli-contract.md) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, JSON, guidance] <br>
**Output Format:** [Markdown guidance with bash command examples and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires local WeChat credentials, prepared article assets, and an audited mp-weixin-skill executable.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
