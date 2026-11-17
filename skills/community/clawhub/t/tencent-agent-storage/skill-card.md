## Description:

Tencent Agent Storage lets an agent upload, list, search, rename, move, and share files in a user's Tencent Agent Storage cloud drive.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shawnminh](https://clawhub.ai/user/shawnminh)

### License/Terms of Use:

MIT-0

## Use Case:

External users and their agents use this skill to manage personal cloud-drive files, upload generated artifacts, and provide time-limited download or preview links across devices.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Administrative Tencent storage tokens can be exposed or overused if shared broadly.

Mitigation: Use a dedicated Tencent storage token with the least privilege available, keep credential files private, and never display access-token based URLs to users.

Risk: Broad activation language can lead to unintended uploads of local files or directories.

Mitigation: Require the user to identify the exact file or directory before upload, and confirm before uploading sensitive or unexpected content.

Risk: Setup guidance includes curl-to-sudo and global npm installation paths.

Mitigation: Prefer reviewed local installation with pinned dependencies, and avoid piping remote setup scripts into privileged package installation.

Risk: A modified endpoint could direct storage operations away from the intended Tencent service.

Mitigation: Keep smh_basePath fixed to the legitimate Tencent endpoint unless the publisher and deployment owner explicitly approve a different endpoint.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shawnminh/skills/tencent-agent-storage)
- [Publisher profile](https://clawhub.ai/user/shawnminh)
- [Tencent Agent Storage API endpoint](https://api.tencentsmh.cn)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON command results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Successful uploads return complete, time-limited downloadUrl links; search is limited to filename matching.]

## Skill Version(s):

1.0.17 (source: server release metadata; artifact frontmatter says 1.0.11)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
