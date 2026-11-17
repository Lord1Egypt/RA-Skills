## Description:

Manage YouTube video captions by listing, inserting, updating, downloading, or deleting caption tracks with the yutu CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[openwaygate](https://clawhub.ai/user/openwaygate)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, creators, and operations teams use this skill to manage YouTube caption tracks from an agent workflow after configuring Google OAuth credentials and the yutu CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: OAuth client secrets and cached YouTube tokens can expose account access if committed or shared.

Mitigation: Keep client_secret.json and youtube.token.json out of repositories and shared folders, restrict file permissions, and use the documented YUTU_CREDENTIAL and YUTU_CACHE_TOKEN paths carefully.

Risk: Caption update and delete commands can alter or remove YouTube caption tracks.

Mitigation: Verify video IDs and caption IDs before running update or delete commands, especially when acting on behalf of a content owner.

Risk: The skill depends on the third-party yutu CLI for YouTube API operations.

Mitigation: Install yutu only from a trusted source and review the CLI source or package provenance before use in sensitive environments.

## Reference(s):

- [Caption Delete](references/caption-delete.md)
- [Caption Download](references/caption-download.md)
- [Caption Insert](references/caption-insert.md)
- [Caption List](references/caption-list.md)
- [Caption Update](references/caption-update.md)
- [Yutu Setup Guide](references/setup.md)
- [yutu CLI](https://github.com/eat-pray-ai/yutu)
- [yutu releases](https://github.com/eat-pray-ai/yutu/releases/latest)
- [YouTube Data API v3](https://console.cloud.google.com/apis/api/youtube.googleapis.com/overview)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands may read or modify YouTube caption resources through OAuth-authorized yutu CLI calls.]

## Skill Version(s):

0.10.7-dev (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
