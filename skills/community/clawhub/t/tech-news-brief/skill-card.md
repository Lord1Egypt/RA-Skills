## Description: <br>
Organizes Chinese and foreign technology news into source drafts, Chinese summaries, and DOCX files that follow the "xx班" reporting format, completing discovery through email delivery in one session. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[scienlot](https://clawhub.ai/user/scienlot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and analysts use this agent skill to find recent AI, large-model, semiconductor, and frontier-technology news, filter it by recency and strategic relevance, generate concise Chinese reporting drafts, convert them to DOCX, and send the packaged report by email. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires SMTP credentials and can send generated report archives by email. <br>
Mitigation: Use app-specific SMTP credentials, keep .env files private, avoid command-line passwords, and confirm the SMTP recipient before sending. <br>
Risk: The generated ZIP archive may contain local MD and DOCX reports selected by the agent workflow. <br>
Mitigation: Review the ZIP contents before email delivery and send only to the intended SMTP_TO recipient. <br>
Risk: The reporting guide emphasizes a China-strategy brief posture that may not fit neutral reporting needs. <br>
Mitigation: Adjust the writing guide before use when neutral or different editorial framing is required. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/scienlot/tech-news-brief) <br>
- [Recommended news sources](artifact/references/sources.md) <br>
- [Summary writing guide](artifact/references/writing-guide.md) <br>
- [README](artifact/README.md) <br>
- [Firecrawl scrape API](https://api.firecrawl.dev/v2/scrape) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown reports, DOCX files, ZIP archives, email delivery status, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates dated local report directories and can package selected report files for SMTP delivery.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
