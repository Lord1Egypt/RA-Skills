## Description: <br>
Track TikTok ad activity and monitor advertiser changes using PipiAds tools for TikTok ad discovery and Facebook-based monitoring workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fanyanggod](https://clawhub.ai/user/fanyanggod) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Marketing analysts, ecommerce operators, and growth teams use this skill to research TikTok ad creatives, inspect advertisers, and set up PipiAds monitoring workflows for changes over time. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on a third-party npm package and a PipiAds/Pipispy service account. <br>
Mitigation: Verify trust in the pipiads-mcp-server package and the PipiAds/Pipispy account relationship before installing or configuring credentials. <br>
Risk: Global npm installation can affect the local agent environment. <br>
Mitigation: Install without elevated privileges in a controlled environment and review package provenance before use. <br>
Risk: Searches and monitor tasks consume PipiAds account credits and may affect billing. <br>
Mitigation: Use narrow searches, review monitor task scope before creation, and monitor API credit or billing usage. <br>


## Reference(s): <br>
- [PipiAds homepage](https://www.pipiads.com) <br>
- [Pipispy API key and billing](https://www.pipispy.com/) <br>
- [ClawHub skill page](https://clawhub.ai/fanyanggod/tiktok-ad-tracker-monitor) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, API calls] <br>
**Output Format:** [Markdown setup and workflow guidance with MCP tool names and shell command configuration.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires PIPIADS_API_KEY and the pipiads-mcp-server npm package.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
