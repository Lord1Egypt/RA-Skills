## Description: <br>
Tracks Eastmoney self-selected stock announcements, filters low-value notices, uses optional LLM classification and summaries, and can present results through an agent digest or local web dashboard. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[54lynnn](https://clawhub.ai/user/54lynnn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Investors, analysts, and agents use this skill to monitor selected A-share and Hong Kong stock announcements, prioritize higher-value disclosures, and produce concise summaries or a dashboard view for review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles live account cookies and .env API keys. <br>
Mitigation: Treat cookie.txt and .env as secrets, keep them out of commits, and restrict local file permissions. <br>
Risk: Announcement data may be sent to configurable external LLM or webhook endpoints. <br>
Mitigation: Enable LLM and webhook features only when sending the selected announcement data to those endpoints is acceptable. <br>
Risk: Automatic scheduling can repeatedly run network and notification workflows. <br>
Mitigation: Review and confirm cron entries manually before enabling scheduled runs. <br>
Risk: The dashboard exposes announcement data through a local web service. <br>
Mitigation: Bind the dashboard to localhost unless intentional network exposure has been reviewed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/54lynnn/skills/stock-tracker) <br>
- [System architecture](references/architecture.md) <br>
- [Announcement classification system](references/classification.md) <br>
- [Text cleaning rules](references/text-cleaning.md) <br>
- [Token cost analysis](references/token-cost.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Plain-text digest output, Markdown-style summaries, shell command guidance, configuration instructions, and optional dashboard CSV export.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can run scheduled agent digests or launch a local Flask dashboard for interactive review.] <br>

## Skill Version(s): <br>
2.2.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
