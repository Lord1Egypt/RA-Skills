## Description: <br>
TikTok account search tool that lets an agent search creator accounts by keyword, rank results by follower count, show profile details, and suggest related keywords when no accounts are found. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[redfox-data](https://clawhub.ai/user/redfox-data) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, marketers, content creators, brands, MCNs, and cross-border e-commerce teams use this skill to discover TikTok creator accounts by niche, compare follower counts, and collect profile links for outreach, research, or competitive analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends a RedFox API key to the RedFox API while TLS certificate and hostname verification are disabled in the helper script. <br>
Mitigation: Review before installing, use only a RedFox API key that can be rotated or revoked, avoid sensitive searches, and restore normal TLS certificate verification before broader deployment. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/redfox-data/skills/tiktok-account-search) <br>
- [RedFox Hub API Key Settings](https://redfox.hk/settings/api-keys?source=clawhub) <br>
- [RedFox Hub](https://redfox.hk?source=github) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, API Calls, Guidance] <br>
**Output Format:** [Markdown tables and guidance with JSON returned by the helper script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search output includes account nickname, TikTok ID, follower count, bio summary, verification status, region, profile URL, page number, next-page flag, total count, and pagination cursor.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
