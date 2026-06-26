## Description: <br>
Reddit Spy browses, reads, and analyzes subreddit posts and comments using Reddit API, Tor/proxy, browser, and archive fallback layers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hioliver933](https://clawhub.ai/user/hioliver933) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and analysts use this skill to gather read-only intelligence from public Reddit communities, compare subreddit activity, inspect posts and comments, search keywords, and profile posting patterns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security evidence flags stealth scraping, Tor/proxy routing, credentials, and persistent session state as behaviors requiring review. <br>
Mitigation: Install only when those behaviors are intended, review or disable Tor/proxy/browser fallback behavior, and clear ~/.openclaw/.reddit-spy-cache after use. <br>
Risk: Optional Reddit OAuth credentials and proxy URLs may expose account or infrastructure secrets if overprivileged or reused. <br>
Mitigation: Use a throwaway or least-privilege Reddit account, avoid entering sensitive credentials, and scope proxy credentials to this use case. <br>
Risk: User and subreddit analysis can create privacy or compliance concerns when directed at private individuals or sensitive communities. <br>
Mitigation: Use the skill only with a legitimate basis, review collected outputs before sharing, and avoid targeting private individuals without appropriate authorization. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/hioliver933/reddit-spy) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, guidance] <br>
**Output Format:** [JSON written to stdout, with operational logs written to stderr] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs can include subreddit metrics, post and comment data, content pattern analysis, keyword search results, user posting patterns, health-check results, and recommendations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
