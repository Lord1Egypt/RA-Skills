## Description: <br>
Xiaohongshu Hot Daily fetches public Xiaohongshu Explore trending notes with a browser, categorizes them by topic, prints a ranked daily summary, and can export JSON reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qq853632587](https://clawhub.ai/user/qq853632587) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content operators, analysts, and automation agents use this skill to collect a daily snapshot of public Xiaohongshu trending notes, categorize topics, and export summaries for editorial planning or lightweight trend monitoring. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Browser fetch failures can produce simulated fallback results that resemble a normal report. <br>
Mitigation: Run the skill manually first, check stderr for the simulated-data message, and label or verify the data source before using exported reports for decisions. <br>
Risk: The skill opens a public Xiaohongshu page with agent-browser/Chromium. <br>
Mitigation: Use it only in environments where browser access to public webpages is acceptable, and follow site terms and local data-use policy. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/qq853632587/xiaohongshu-hot-daily) <br>
- [Xiaohongshu Explore](https://www.xiaohongshu.com/explore) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration] <br>
**Output Format:** [Console text with optional JSON report files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include ranked note titles, authors, like counts, categories, source URLs, timestamps, and an optional summary.] <br>

## Skill Version(s): <br>
3.1.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
