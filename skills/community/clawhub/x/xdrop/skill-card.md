## Description:

Xdrop helps an agent upload local files or directories to an Xdrop server and download encrypted Xdrop share links from the terminal.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xixu-me](https://clawhub.ai/user/xixu-me)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use Xdrop to automate encrypted file-transfer workflows with an Xdrop server, including upload, share-link generation, and local decryption/download from full share links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The downloader trusts Xdrop server responses enough to create review-worthy network and overwrite risks.

Mitigation: Use trusted Xdrop servers and share links, and choose a fresh output directory that other local users or processes cannot pre-populate.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xixu-me/skills/xdrop)
- [Publisher profile](https://clawhub.ai/user/xixu-me)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, JSON, files, guidance]

**Output Format:** [Markdown guidance with inline shell commands and optional JSON script outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uploads return share links or JSON metadata; downloads save files to a local output directory.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
