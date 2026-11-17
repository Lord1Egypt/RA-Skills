## Description:

X Media Parser parses X/Twitter post URLs and returns direct download links and metadata for images, videos, GIFs, and mixed media posts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ingress007](https://clawhub.ai/user/ingress007)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to inspect X/Twitter post URLs and produce machine-readable media download information without requiring an X login or API key. It can also guide optional handoff to Aria2 for downloads when the downloader script has been reviewed and configured.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional Aria2 downloader can control an Aria2 RPC service using hardcoded private-network settings and a hardcoded RPC secret.

Mitigation: Do not run the downloader until the RPC endpoint, secret, download directory, temporary-file handling, and URL validation have been audited and changed; rotate the exposed Aria2 token if it has ever been used.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ingress007/skills/x-media-parser)
- [Publisher profile](https://clawhub.ai/user/ingress007)
- [vxtwitter API endpoint used by the skill](https://api.vxtwitter.com/Twitter/status/{tweetId})

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [JSON responses and Markdown guidance with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns media type, title, direct URL, video URLs, image URLs, thumbnails, duration, and resolution when available.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
