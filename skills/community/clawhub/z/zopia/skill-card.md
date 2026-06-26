## Description: <br>
Zopia helps an agent create and manage AI video and image projects on the Zopia platform by configuring projects, sending user prompts, polling progress, downloading generated media, and rendering final episodes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lambdua](https://clawhub.ai/user/lambdua) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill through an agent to create Zopia video or image projects, configure style and model settings, submit creative prompts, track generation progress, download generated assets, and render final MP4 episodes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, project names, generated project data, and account credentials are sent to the configured Zopia service. <br>
Mitigation: Install only when that data sharing is acceptable, treat ZOPIA_ACCESS_KEY as an account credential, and verify ZOPIA_BASE_URL before use. <br>
Risk: The skill downloads generated media files into a local output directory. <br>
Mitigation: Run downloads in a directory where generated media is expected and review downloaded files before reuse or redistribution. <br>
Risk: Episode deletion is irreversible. <br>
Mitigation: Double-check episode IDs before using the delete action. <br>


## Reference(s): <br>
- [Zopia platform](https://zopia.ai) <br>
- [ClawHub skill page](https://clawhub.ai/lambdua/zopia) <br>
- [Skill README](artifact/README.md) <br>
- [Skill instructions](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, JSON, Files, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands, JSON script output, and downloaded image or video files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ZOPIA_ACCESS_KEY and may use ZOPIA_BASE_URL to call the configured Zopia API endpoint.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence, created 2026-04-25) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
