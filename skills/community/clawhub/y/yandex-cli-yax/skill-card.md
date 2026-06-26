## Description: <br>
CLI tool for Yandex Disk, Calendar, and Mail via Yandex OAuth API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smvlx](https://clawhub.ai/user/smvlx) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and automation users use this skill to authenticate with Yandex OAuth, inspect and transfer Yandex Disk files, list calendars, and create calendar events from a Node.js command-line workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The OAuth token may carry mail-sending authority even though mail functionality is only informational. <br>
Mitigation: Create a dedicated Yandex OAuth app, grant only the scopes needed for the intended workflow, and omit mail:smtp unless mail-sending authority is intentionally required. <br>
Risk: Saved Yandex credentials and tokens can expose account access if the local configuration files are mishandled. <br>
Mitigation: Protect ~/.openclaw/yax.env and ~/.openclaw/yax-token.json and avoid sharing logs or archives that include those files. <br>
Risk: Disk upload and download commands can overwrite user-selected local or remote paths. <br>
Mitigation: Review local and remote path arguments before running file transfer commands, especially in automated workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/smvlx/yandex-cli-yax) <br>
- [Project homepage](https://github.com/smvlx/openclaw-ru-skills) <br>
- [Yandex OAuth app setup](https://oauth.yandex.ru/client/new) <br>
- [Yandex OAuth verification code redirect](https://oauth.yandex.ru/verification_code) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and CLI usage examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local configuration and token files under ~/.openclaw.] <br>

## Skill Version(s): <br>
1.1.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
