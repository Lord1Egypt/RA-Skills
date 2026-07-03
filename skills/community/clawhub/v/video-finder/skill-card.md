## Description: <br>
Helps users search for, filter, recommend, and download adult videos using saved preferences, site reachability checks, proxy configuration, and yt-dlp. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiaoka520](https://clawhub.ai/user/xiaoka520) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to locate adult videos matching stated preferences, review filtered results, choose a target item, and download it to a selected local directory. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persistently store highly sensitive adult-content preferences, download history, feedback, and proxy credentials. <br>
Mitigation: Install only if this storage is acceptable; prefer session-only proxy use and regularly review or delete files under ~/.openclaw/skills/video-finder/. <br>
Risk: Ambiguous requests may trigger an adult-content search and download workflow. <br>
Mitigation: Avoid ambiguous invocations unless the workflow is explicitly intended, and require user confirmation before download. <br>
Risk: Stored proxy credentials may expose access details if local files are mishandled. <br>
Mitigation: Do not echo proxy secrets in chat, logs, or examples, and avoid persisting credentials unless necessary. <br>


## Reference(s): <br>
- [Source repository](https://github.com/xiaoka520/video-finder) <br>
- [ClawHub skill page](https://clawhub.ai/xiaoka520/skills/video-finder) <br>
- [Publisher profile](https://clawhub.ai/user/xiaoka520) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include search results, download commands, progress updates, local preference and proxy file guidance, and history entries.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
