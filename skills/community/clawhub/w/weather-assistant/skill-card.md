## Description: <br>
Weather Assistant helps users query city weather, manage city configuration, and optionally send scheduled daily weather updates to WeChat with a quote. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jerryaction](https://clawhub.ai/user/jerryaction) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to fetch weather from configured cities, update city settings, and set up a daily WeChat weather announcement with concise clothing advice and an optional quote. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Incorrect WeChat target or account settings could send scheduled weather updates to the wrong destination. <br>
Mitigation: Configure the WeChat OpenID and account carefully before enabling delivery. <br>
Risk: Scheduled weather messages may continue after they are no longer wanted. <br>
Mitigation: Remove or disable the cron job when automatic messages are no longer needed. <br>
Risk: The local quote file used in daily messages could contain private text. <br>
Mitigation: Keep the quote file free of private or sensitive content. <br>
Risk: City configuration edits can remove or corrupt configured locations. <br>
Mitigation: Review proposed configuration changes before applying them and keep at least one city configured. <br>
Risk: Weather lookup depends on wttr.in and may be slow, unavailable, or not support a specific local query. <br>
Mitigation: Use supported city query names and add a timeout or retry strategy for scheduled runs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jerryaction/weather-assistant) <br>
- [Skill README](README.md) <br>
- [Skill definition](SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Conversational Markdown and plain text weather announcements, with JSON configuration snippets and shell commands when setup or manual triggering is needed.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read city configuration and a local quote file, query wttr.in, and produce scheduled WeChat announcement content through OpenClaw delivery.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
