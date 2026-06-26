## Description: <br>
Cross-reference restaurant recommendations from Xiaohongshu and Dianping to validate restaurant quality and consistency for location-based dining and local-life queries. <br>

This skill is for research and development only. <br>

## Publisher: <br>
[zhongrenfei1-hub](https://clawhub.ai/user/zhongrenfei1-hub) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and agents use this skill to compare restaurants or local-life venues across Dianping ratings and Xiaohongshu user posts, then produce ranked recommendations with confidence and consistency signals. It is most appropriate for personal research workflows that can tolerate scraping limitations, saved browser sessions, and manual review of low-confidence matches. <br>

### Deployment Geography for Use: <br>
China <br>

## Known Risks and Mitigations: <br>
Risk: The skill saves logged-in Dianping and Xiaohongshu browser sessions locally. <br>
Mitigation: Use separate accounts where practical, avoid shared machines, and delete ~/.local/share/restaurant-crosscheck/sessions after use. <br>
Risk: The skill scrapes sites that may restrict automation and may trigger access blocks or terms-of-service issues. <br>
Mitigation: Review platform terms before use, keep usage to permitted personal research workflows, and prefer official or licensed data access for commercial use. <br>
Risk: Setup and scraping scripts run local code and browser automation. <br>
Mitigation: Inspect setup.sh and scripts before execution, install in a virtual environment, and run with least-privileged local accounts. <br>
Risk: Restaurant matches and sentiment scores may be inaccurate because they rely on fuzzy matching, scraped data availability, and keyword heuristics. <br>
Mitigation: Treat low-confidence or inconsistent results as candidates for manual review before making decisions. <br>


## Reference(s): <br>
- [Data Schema Documentation](references/data_schema.md) <br>
- [Sentiment Analysis for Xiaohongshu Posts](references/sentiment_analysis.md) <br>
- [API and Data Source Limitations](references/api_limitations.md) <br>
- [Dianping](https://www.dianping.com) <br>
- [Xiaohongshu](https://www.xiaohongshu.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown-like ranked recommendations with platform comparison details, confidence scores, consistency labels, warnings, and setup or configuration commands when needed.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Recommendation quality depends on current platform access, saved login sessions, scraping success, fuzzy matching, engagement heuristics, and sentiment keyword coverage.] <br>

## Skill Version(s): <br>
2.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
