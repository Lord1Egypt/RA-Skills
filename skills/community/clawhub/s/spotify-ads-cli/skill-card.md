## Description: <br>
Spotify Ads CLI helps agents analyze Spotify Ads performance, reports, targeting, audiences, assets, pixels, and datasets through spotify-ads-cli commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bin-huang](https://clawhub.ai/user/bin-huang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and advertising operators use this skill to inspect Spotify Ads accounts, pull aggregate or insight reports, explore targeting and audiences, and prepare CSV reporting workflows through the Spotify Ads CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill describes the CLI as read-only while documenting commands that create remote CSV report jobs and suggesting audience or asset management workflows. <br>
Mitigation: Require explicit user confirmation before creating CSV reports or running commands that may affect audiences or assets. <br>
Risk: The skill requires Spotify Ads OAuth access and may expose account reporting data if used with overly broad credentials. <br>
Mitigation: Use only Spotify Ads accounts where reporting access is approved, and verify the selected business, account, date range, and credential source before running commands. <br>


## Reference(s): <br>
- [spotify-ads-cli documentation](https://github.com/Bin-Huang/spotify-ads-cli) <br>
- [Spotify Ads API documentation](https://developer.spotify.com/documentation/ads-api) <br>
- [ClawHub skill page](https://clawhub.ai/bin-huang/spotify-ads-cli) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance, markdown] <br>
**Output Format:** [Markdown with inline shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Spotify OAuth access token with Ads API access.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
