## Description: <br>
Multi-platform sentiment monitoring and analysis for products, brands, and topics across Chinese and English social platforms, producing structured reports with product mentions, pricing complaints, comparison analysis, and actionable insights. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Danielwangyy](https://clawhub.ai/user/Danielwangyy) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, analysts, and market intelligence teams use this skill to collect social-media discussion for products, brands, or competitors and turn it into sentiment, pain-point, pricing, and comparison reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses authenticated social sessions and live browser automation for social-media collection. <br>
Mitigation: Review before installing, use a dedicated social account and isolated browser profile, and run collection only for platforms you explicitly intend to monitor. <br>
Risk: The workflow depends on MediaCrawler and can make persistent changes to that crawler's configuration. <br>
Mitigation: Inspect or pin the MediaCrawler dependency and review configuration changes before running collection. <br>
Risk: Generated reports and stdout may retain scraped comments and location metadata from social platforms. <br>
Mitigation: Sanitize keywords and review, redact, and handle generated outputs as retained social-media content. <br>


## Reference(s): <br>
- [Sentiment Report Template](references/report-template.md) <br>
- [MediaCrawler](https://github.com/NanmiCoder/MediaCrawler) <br>
- [ClawHub Skill Page](https://clawhub.ai/Danielwangyy/sentiment-radar) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports, JSON analysis output, and shell-command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports may include retained social-media content, engagement metrics, product mentions, pricing complaints, comparison excerpts, and location metadata when present in collected comments.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
