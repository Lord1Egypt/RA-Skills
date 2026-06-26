## Description: <br>
Aggregates trending public news from multiple platforms, categorizes topics, scores heat, detects newly appearing items, summarizes trends, and can support scheduled delivery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[19x19btr](https://clawhub.ai/user/19x19btr) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and OpenClaw operators use this skill to collect public trending-news results, group them by category, compare heat scores, and produce scheduled or on-demand news digests. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Scheduled delivery can send digests to the wrong channel or recipient if push settings are misconfigured. <br>
Mitigation: Verify the push channel, recipient, and schedule before enabling automation, and test delivery manually first. <br>
Risk: Trending-news collection depends on public web search results and can include stale links, incomplete coverage, or classification errors. <br>
Mitigation: Treat the digest as a monitoring aid, review linked sources before acting on information, and adjust category keywords when results are inaccurate. <br>
Risk: Automated searches and delivery may be affected by rate limits or host compatibility. <br>
Mitigation: Use a reasonable schedule and run the skill on an up-to-date OpenClaw version that satisfies the documented minimum host requirement. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/19x19btr/trending-news-aggregator) <br>
- [Publisher profile](https://clawhub.ai/user/19x19btr) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Configuration, Guidance] <br>
**Output Format:** [Markdown-style news digest with categorized items, heat scores, new-item markers, links, and a trend summary] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include scheduled push configuration guidance when delivery channels are enabled.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence release, package.json, CHANGELOG) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
