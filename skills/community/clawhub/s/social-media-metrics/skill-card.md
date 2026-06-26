## Description: <br>
Fetch follower counts and social media metrics from profile URLs or nicknames across platforms including Bilibili, YouTube, TikTok, Instagram, Douyin, Kuaishou, Xiaohongshu, Toutiao, Baijiahao, WeChat Video, Haokan, and iQiyi. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[guoming0000](https://clawhub.ai/user/guoming0000) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to look up follower counts and related public social media metrics from a supported profile URL or account nickname. It helps agents retrieve metrics and present the JSON result in a concise user-facing summary. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Browser scraping and anti-detection automation can trigger platform anti-bot controls or account-risk consequences. <br>
Mitigation: Install only if this behavior is acceptable for the use case, and prefer low-risk or dedicated accounts for platforms that require authentication. <br>
Risk: The skill can retain reusable logged-in browser sessions in a local Playwright CDP profile. <br>
Mitigation: Keep the profile private and delete ~/.playwright_cdp_profile when retained cookies are no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/guoming0000/social-media-metrics) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Text, Shell commands] <br>
**Output Format:** [JSON metrics from the helper script, with concise text or Markdown summaries from the agent] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns platform, username, uid, URL, metrics such as followers, fetch timestamp, success status, and error details when retrieval fails.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
