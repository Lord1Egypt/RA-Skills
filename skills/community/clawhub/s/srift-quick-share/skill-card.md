## Description:

Creates temporary download links for local files and folders through SRIFT, with optional end-to-end encryption.

This skill is ready for commercial/non-commercial use.

## Publisher:

[srivardhan113](https://clawhub.ai/user/srivardhan113)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and their users share selected local files or folders with recipients through temporary download links, optionally encrypting the transfer.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sharing an unintended local file or folder exposes it to anyone with the download link while sharing is active.

Mitigation: Confirm the selected paths and recipient before sharing; use --once, --ttl, or --max-downloads to limit link exposure.

Risk: Sensitive content shared without encryption may be exposed during transfer.

Mitigation: Use --encrypt for confidential files.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/srivardhan113/skills/srift-quick-share)
- [SRIFT agent manual](https://srift.app/AGENTS.md)
- [SRIFT API contract](https://srift.app/openapi.json)

## Skill Output:

**Output Type(s):** [Text]

**Output Format:** [Download URL with brief sharing guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Link works while the sender's sharing process is running; optional encryption, single-download, expiry, and download limits.]

## Skill Version(s):

4.4.0 (source: skill frontmatter and ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
