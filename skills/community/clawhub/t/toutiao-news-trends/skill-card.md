## Description: <br>
Fetches Toutiao hot-board news trends across Chinese news topics and returns titles, popularity scores, cleaned links, covers, labels, aggregation IDs, and category tags. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wuchubuzai2018](https://clawhub.ai/user/wuchubuzai2018) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to retrieve current Toutiao trending-news entries for monitoring, summarization, or downstream Chinese news workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Scraped news results may be incomplete, stale, or non-authoritative. <br>
Mitigation: Review returned items before using them in decisions or publications, and cross-check important facts against authoritative sources. <br>
Risk: Toutiao's public web endpoint or response fields may change or access may be rate-limited. <br>
Mitigation: Handle errors and missing fields gracefully, use conservative request rates, and confirm that the scraping posture is acceptable for the intended environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wuchubuzai2018/toutiao-news-trends) <br>
- [Toutiao hot-board endpoint](https://www.toutiao.com/hot-event/hot-board/) <br>
- [Toutiao website](https://www.toutiao.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Code, API Calls, Files] <br>
**Output Format:** [JSON emitted by a Node.js command-line script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns up to 200 ranked items with title, popularity, link, cover, label, clusterId, and categories fields.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
