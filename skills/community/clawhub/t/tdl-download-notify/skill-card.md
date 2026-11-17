## Description:

Downloads Telegram resources with tdl and sends ServerChan WeChat notifications with file names, sizes, timing, and success or failure status.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tang2606](https://clawhub.ai/user/tang2606)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to download a Telegram message resource with tdl and receive a WeChat notification when the download succeeds or fails.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence reports a hardcoded ServerChan key that can send Telegram download details, filenames, file sizes, local output paths, timestamps, and failure output to a fixed external channel.

Mitigation: Review before installation, replace the embedded SendKey with user-controlled secret configuration, and minimize notification payloads before production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tang2606/skills/tdl-download-notify)
- [TDL documentation](https://github.com/iyear/tdl)
- [ServerChan website](https://sct.ftqq.com/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown notifications and JSON command-line result output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the tdl binary, Telegram login state, Python requests, and ServerChan notification access.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
