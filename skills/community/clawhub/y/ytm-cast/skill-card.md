## Description: <br>
Download music from YouTube/YouTube Music and stream to Chromecast via Home Assistant with a CLI toolset, web server integration, configuration wizard, and playback controls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AidanTheBandit](https://clawhub.ai/user/AidanTheBandit) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and technically comfortable home media users use this skill to download local audio or video files from YouTube sources and cast them to Chromecast devices through Home Assistant. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores a Home Assistant long-lived access token in a local configuration file. <br>
Mitigation: Use a dedicated or least-privilege token where possible, keep ~/.youtube-music-cast/config.sh private, and revoke the token if it is exposed. <br>
Risk: The skill uses a local media server to make downloaded files available for casting. <br>
Mitigation: Run the media server only on trusted networks and stop it when it is not needed. <br>
Risk: The skill depends on referenced local scripts and external command-line tools. <br>
Mitigation: Install only when the source is trusted and review the scripts before running download, server, or casting commands. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/AidanTheBandit/ytm-cast) <br>
- [Artifact repository metadata](https://github.com/clawdbot/skills/tree/main/youtube-music-cast) <br>
- [Artifact homepage metadata](https://github.com/clawdbot/skills) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include commands that rely on local tools, Home Assistant configuration, and a local media server.] <br>

## Skill Version(s): <br>
6.0.0 (source: release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
