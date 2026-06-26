## Description: <br>
Collects recent public X/Twitter posts from a specified account and produces a bilingual report with links, screenshots, engagement metrics, and topic analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pinotao](https://clawhub.ai/user/pinotao) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Analysts, operators, and content teams use this skill to collect and summarize public X/Twitter activity for a named handle over a requested time range, typically the past 24 hours. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a browser profile to view X/Twitter and collect public posts, links, metrics, and screenshots. <br>
Mitigation: Use explicit public handles and time ranges, avoid private or sensitive targets, and confirm the collection scope before running. <br>
Risk: Generated reports and screenshots can retain social media content locally. <br>
Mitigation: Store outputs only where appropriate and periodically delete reports or screenshots that are no longer needed. <br>
Risk: X/Twitter login state, account visibility, deleted posts, and loading limits can affect report completeness. <br>
Mitigation: Treat reports as best-effort snapshots and verify important findings against the live public account. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/pinotao/x-twitter-collector) <br>
- [README.md](README.md) <br>
- [SKILL.md](SKILL.md) <br>
- [template.md](template.md) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, text, files, guidance] <br>
**Output Format:** [Markdown report with tables, bilingual text, tweet links, engagement metrics, and screenshot file references.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May save local screenshots and reports; default collection window is 24 hours and targets public accounts.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
