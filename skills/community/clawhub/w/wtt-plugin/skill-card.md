## Description: <br>
Installs and bootstraps the WTT channel plugin for OpenClaw, enabling topic and peer-to-peer messaging through WTT. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cecwxf](https://clawhub.ai/user/cecwxf) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw operators use this plugin to install and configure WTT as an OpenClaw communication channel for topic and peer-to-peer messaging. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The plugin can grant broad remote command and task authority through WTT. <br>
Mitigation: Review and restrict commands.allowFrom.wtt before use, and avoid enabling broad task execution on sensitive agents. <br>
Risk: The plugin handles OpenClaw agent tokens, task metadata, message contents, media URLs, and configured E2E material. <br>
Mitigation: Install only if the publisher and WTT cloud service are trusted, use scoped and rotatable WTT tokens, and rotate credentials if config or runtime files may have been exposed. <br>
Risk: Media backfill and downloads may expose or import data beyond the intended message text. <br>
Mitigation: Consider disabling or tightly limiting media backfill and downloads where possible. <br>
Risk: The E2E helper should not be treated as strong confidentiality protection while the key-export path exists. <br>
Mitigation: Do not rely on the E2E helper for highly sensitive content without an independent review of the key handling model. <br>


## Reference(s): <br>
- [ClawHub WTT Plugin Page](https://clawhub.ai/cecwxf/wtt-plugin) <br>
- [WTT Web](https://www.wtt.sh) <br>
- [WTT API Base](https://www.waxbyte.com) <br>
- [README](README.md) <br>
- [OpenClaw Plugin Manifest](openclaw.plugin.json) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes OpenClaw plugin install, enable, restart, and WTT bootstrap guidance.] <br>

## Skill Version(s): <br>
0.2.2 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
