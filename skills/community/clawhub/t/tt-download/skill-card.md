## Description: <br>
Resolves signed MP4 video URLs from Oceanengine material-center video_player pages and can optionally download the stream to a local file. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[suiside](https://clawhub.ai/user/suiside) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill when they need to extract or save the real signed video URL behind an Oceanengine material-center video_player link. It is intended for trusted Oceanengine material-center links, not for general-purpose video downloading. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill launches a local headless browser and performs network requests to resolve Oceanengine video URLs. <br>
Mitigation: Review before installation and use it only with trusted Oceanengine material-center links. <br>
Risk: The downloader can write MP4 output to the local filesystem. <br>
Mitigation: Ask for explicit user confirmation before downloading and choose an intentional output path. <br>
Risk: The browser command uses --no-sandbox, which can increase exposure on sensitive machines. <br>
Mitigation: Run in an isolated browser profile or controlled environment, and consider removing --no-sandbox when the local platform supports it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/suiside/tt-download) <br>
- [OpenClaw documentation](https://docs.openclaw.ai/) <br>
- [Usage contract](references/usage.json) <br>
- [Chrome path reference](references/chrome-paths.json) <br>
- [Troubleshooting guide](references/troubleshooting.md) <br>
- [Google Chrome](https://www.google.com/chrome/) <br>
- [Microsoft Edge](https://www.microsoft.com/edge) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, files, guidance] <br>
**Output Format:** [Plain text URL on stdout, optional MP4 file output, and progress or error guidance on stderr] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python 3 and a local Chromium-based browser; uses network access and local file writes when downloading.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
