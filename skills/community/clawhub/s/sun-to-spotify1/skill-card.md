## Description: <br>
Generate Sun audio and stream episodes to Spotify as a podcast. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sunbot001](https://clawhub.ai/user/sunbot001) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to turn a supplied prompt into a Sun-generated audio experience and publish completed episodes to Spotify as a podcast. It supports CLI-first operation with an HTTP API fallback when the CLI is unavailable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create Spotify shows and upload generated episodes without a separate approval step. <br>
Mitigation: Require explicit review of the show title, cover image, generated audio, and target Spotify show before any upload command runs. <br>
Risk: The workflow uses Sun and Spotify credentials, including personal API tokens and OAuth authorization. <br>
Mitigation: Use isolated credential storage, avoid logging secrets, prefer uv or pipx installation, and revoke tokens that are no longer needed. <br>
Risk: The curl installer executes a remote install script. <br>
Mitigation: Prefer uv or pipx installation when possible, or review the installer before running it. <br>


## Reference(s): <br>
- [Sun to Spotify skill page](https://clawhub.ai/sunbot001/sun-to-spotify1) <br>
- [Sun CLI Usage](artifact/cli-usage.md) <br>
- [Sun Public HTTP API](artifact/http-api.md) <br>
- [Sun CLI installer](https://sunapp-ai.github.io/sun-to-spotify/install.sh) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, JSON examples, and operational checklists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Sun authentication, a personal Sun API token, Spotify authorization through save-to-spotify, and user-supplied audio prompt details.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
