## Description: <br>
Tracks Eastmoney watchlist announcements with three-stage filtering, optional LLM classification and summaries, and a local web dashboard. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[54lynnn](https://clawhub.ai/user/54lynnn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to monitor selected Eastmoney stock groups, filter announcements, summarize high-value items, and review results through a digest or dashboard. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles Eastmoney session cookies and optional LLM API keys. <br>
Mitigation: Use a dedicated low-privilege Eastmoney session where possible, and protect cookie.txt and .env like passwords. <br>
Risk: Watchlist and announcement data may be sent to the configured LLM endpoint. <br>
Mitigation: Confirm the LLM base_url matches the intended API-key provider before enabling LLM classification or summaries. <br>
Risk: The setup script can add recurring jobs. <br>
Mitigation: Review setup.sh before running it and only install cron jobs when scheduled execution is intended. <br>
Risk: The dashboard can expose local announcement data on a shared network if broadly bound. <br>
Mitigation: Bind the dashboard to localhost or otherwise restrict access when running on shared machines. <br>


## Reference(s): <br>
- [System Architecture](references/architecture.md) <br>
- [Announcement Classification](references/classification.md) <br>
- [Token Cost Analysis](references/token-cost.md) <br>
- [Text Cleaning Rules](references/text-cleaning.md) <br>
- [Eastmoney Watchlist](https://quote.eastmoney.com/zixuan/lite.html) <br>
- [CNInfo Announcement Query](https://www.cninfo.com.cn/new/hisAnnouncement/query) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Plain text digest, Markdown guidance, shell commands, configuration snippets, and a local HTML dashboard] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Digest output uses DIGEST_TOTAL or DIGEST_EMPTY markers; dashboard runs locally on a configurable PORT.] <br>

## Skill Version(s): <br>
2.1.0 (source: server release metadata; artifact frontmatter reports 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
