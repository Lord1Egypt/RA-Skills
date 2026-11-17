## Description:

Download files from the web via HTTP/HTTPS/FTP with resume support, recursive mirroring, rate limiting, and progress feedback.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dinghaibin](https://clawhub.ai/user/dinghaibin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to retrieve web-accessible files for batch downloads, website mirroring, and automated data acquisition workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The downloader can read from unexpected URL schemes or overwrite writable files.

Mitigation: Use only trusted URLs and explicit output paths, and avoid automated or unattended use until allowed schemes and destination handling are bounded.

Risk: Command-line headers can expose secrets through shell history, logs, or process listings.

Mitigation: Do not pass real secrets in command-line headers; use short-lived test credentials or a safer secret-handling path.

Risk: Some documented downloader capabilities may be less complete than described.

Mitigation: Verify required behavior in a controlled test before relying on the skill for production automation.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/dinghaibin/skills/wget-tool)
- [Publisher Profile](https://clawhub.ai/user/dinghaibin)

## Skill Output:

**Output Type(s):** [Shell commands, Files, Guidance]

**Output Format:** [Markdown with shell command snippets and downloaded files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write files to a specified output path or a URL-derived filename; review destination handling before unattended use.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
