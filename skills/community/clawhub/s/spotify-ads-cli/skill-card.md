## Description:

Spotify Ads data analysis and reporting via spotify-ads-cli.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bin-huang](https://clawhub.ai/user/bin-huang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and marketing operations teams use this skill to query Spotify Ads accounts, retrieve performance reports, inspect campaign hierarchy, explore targeting and audiences, and plan bids through the spotify-ads-cli.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Spotify Ads OAuth tokens can expose advertising account data if overscoped, pasted into chat, or stored insecurely.

Mitigation: Use a least-privilege Spotify Ads token, keep token values out of chat, and prefer the documented environment variable or credentials file path.

Risk: The CSV report workflow creates an asynchronous report job, which is state-changing despite the skill describing the CLI as read-only.

Mitigation: Require explicit user confirmation before creating CSV report jobs or downloading generated report files.

Risk: Installing an unpinned global CLI package can change behavior over time.

Mitigation: Use a controlled or pinned installation of spotify-ads-cli before relying on command output for reporting.

## Reference(s):

- [spotify-ads-cli documentation](https://github.com/Bin-Huang/spotify-ads-cli)
- [Spotify Ads API documentation](https://developer.spotify.com/documentation/ads-api)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct the agent to run spotify-ads-cli commands that return pretty-printed or compact JSON.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
