## Description:

Integrates with the QinSi Wangcut API so an agent can create AI video-editing tasks, check task status and details, and download completed videos.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huangjt](https://clawhub.ai/user/huangjt)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to connect an agent to a configured Wangcut account, create short-form video-editing tasks from scripts, monitor completion, inspect task metadata, and download generated videos.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Wangcut account credentials may be entered in chat and stored in a persistent config.ini file.

Mitigation: Prefer manual configuration in a private location, restrict file permissions, avoid committing or sharing config.ini, and rotate the password if exposure is possible.

Risk: Changing the configured API base URL could send credentials and task data to an untrusted endpoint.

Mitigation: Keep the default Wangcut HTTPS API URL unless the custom endpoint is fully trusted and reviewed.

Risk: Generated videos and downloaded task outputs may contain user-provided content or sensitive media.

Mitigation: Store downloads in an appropriate local directory, avoid committing downloads, and review generated media before sharing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/huangjt/skills/wangcut)
- [秦丝旺剪官网](https://cloud.qinsilk.com)
- [OpenClaw Skills documentation](https://docs.openclaw.ai/tools/skills)
- [Installation guide](artifact/docs/INSTALL.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files]

**Output Format:** [Markdown responses with Python or shell snippets, configuration values, task IDs, task summaries, URLs, and local video file paths.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update config.ini and may download generated MP4 files to a local downloads directory.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
