## Description: <br>
Track autonomous driving and Robotaxi sector intelligence with Pony.ai, Waymo, Tesla Robotaxi, and Baidu Apollo as core targets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yangzhe1991](https://clawhub.ai/user/yangzhe1991) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and analysts use this skill to generate twice-daily Chinese-language briefings on robotaxi and autonomous-driving sector developments, with source URLs, delta extraction against recent reports, and competitive context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Report history older than 24 hours may be deleted from OpenClaw memory by the skill's cleanup step. <br>
Mitigation: Keep separate copies of reports when long-term audit, comparison, or compliance history is required. <br>
Risk: Briefing quality depends on public news, RSS, Reddit, and web-search availability during the reporting window. <br>
Mitigation: Use the skill's source status reporting and fallback channels, and treat source outages or empty fetches as coverage limitations. <br>
Risk: Robotaxi, market, regulatory, and financial claims can mislead readers if sources are stale, redirected, or weak. <br>
Mitigation: Require resolved final URLs and cross-verification for financial data, stock-price context, permits, and other high-impact claims. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yangzhe1991/robotaxi-briefing) <br>
- [TechCrunch RSS feed](https://techcrunch.com/feed/) <br>
- [The Verge RSS feed](https://www.theverge.com/rss/index.xml) <br>
- [Wired RSS feed](https://www.wired.com/feed/rss) <br>
- [Ars Technica RSS feed](https://arstechnica.com/feed/) <br>
- [Reuters technology feed](https://www.reutersagency.com/feed/?taxonomy=best-sectors&post_type=best&best-sectors=tech) <br>
- [Reddit SelfDrivingCars feed](https://www.reddit.com/r/SelfDrivingCars/new.json?limit=15) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Analysis, Shell commands, Files] <br>
**Output Format:** [Chinese-language Markdown briefing with bare source URLs and a saved local report file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Briefings are constrained to a 24-hour news window, compare against saved reports from the previous 24 hours, and avoid long tables for Feishu readability.] <br>

## Skill Version(s): <br>
6.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
