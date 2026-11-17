## Description:

Queries VisPatrol alarm records on Windows, retrieves matching snapshots, and helps an agent produce alarm reports after explicit approval to read local vpup.json runtime configuration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[baymax1957](https://clawhub.ai/user/baymax1957)

### License/Terms of Use:

MIT-0

## Use Case:

Operations staff and developers use this skill on trusted Windows VisPatrol hosts to answer alarm-history questions, filter by time, alarm type, device, or alarm ID, and produce concise reports with associated snapshot images.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads and decrypts a local VisPatrol session token from vpup.json.

Mitigation: Install only on trusted Windows VisPatrol hosts and require explicit approval before each run that reads vpup.json or uses its token.

Risk: Snapshot downloads can forward the session token while retrieving image data.

Mitigation: Restrict snapshot downloads to the configured VisPatrol media-service origin and avoid forwarding tokens to arbitrary URLs or nonlocal HTTP services.

Risk: Downloaded snapshot images may persist on disk after reports are generated.

Mitigation: Use a controlled snapshot output directory and define a cleanup policy for saved snapshot images.

Risk: The security verdict is suspicious because token handling and snapshot URL validation need review before broad use.

Mitigation: Require script-enforced per-run approval, pin dependencies, and review the token and snapshot handling before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/baymax1957/skills/vispatrol-alram-query)
- [Artifact security boundary](artifact/SECURITY.md)
- [Artifact skill documentation](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Files, Guidance]

**Output Format:** [Markdown or plain text alarm reports with optional JSON results and local snapshot image file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Windows-only; may save snapshot images to a configured local directory after approved vpup.json access.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
