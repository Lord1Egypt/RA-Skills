## Description:

Generate public one-shot or time-limited download links for files using a local Express server exposed via Cloudflare Tunnel.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hitman86r](https://clawhub.ai/user/hitman86r)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to create one-shot or time-limited public links for files when a recipient needs access without VPN or cloud storage.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Public download links can expose a file to anyone who obtains the URL.

Mitigation: Confirm the exact file before sharing, use short TTLs, and do not place sensitive files in the shared directory unless disclosure is intended.

Risk: Weak or mishandled SHARE_SECRET values can expose protected link generation and status endpoints.

Mitigation: Use a strong SHARE_SECRET, pass it in request headers, and avoid query-string secrets.

Risk: Filename-collision and TTL-validation issues could expose or substitute shared files.

Mitigation: Fix filename-collision and TTL-validation behavior before relying on the skill for important files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hitman86r/skills/share-onetime-link)
- [Publisher profile](https://clawhub.ai/user/hitman86r)
- [Cloudflare Zero Trust dashboard](https://one.dash.cloudflare.com)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with shell commands and generated URL text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Copies selected files into the configured shared directory and returns tokenized links with TTL and one-download behavior.]

## Skill Version(s):

1.2.0 (source: server release metadata and scripts/package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
