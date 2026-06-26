## Description: <br>
Collect latest technology and AI news from RSS feeds AND the TLDR.tech AI newsletter, merge them into a unified daily digest, and send via email. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[juniarto-samsudin](https://clawhub.ai/user/juniarto-samsudin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and operators use this skill to gather current technology and AI stories, merge RSS and TLDR.tech AI newsletter items, and send a daily HTML bulletin to configured recipients. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send outbound email from the user's SMTP account to hard-coded recipients. <br>
Mitigation: Review and edit EMAIL_ADDRESSES before setting SMTP_EMAIL and SMTP_PASSWORD or running the skill. <br>
Risk: The cron example can create recurring outbound email delivery. <br>
Mitigation: Enable the cron job only when recurring bulletin delivery is intended. <br>
Risk: RSS article text and feed content may be sent to a fixed HTTP Ollama summarizer endpoint. <br>
Mitigation: Use only a trusted summarizer endpoint for this workflow or adjust the script before processing sensitive content. <br>
Risk: Digest content is written to /tmp/openclaw-debug.log. <br>
Mitigation: Treat the log as containing bulletin content until logging is reduced, redirected, or access-controlled. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/juniarto-samsudin/tech-news-bulletin) <br>
- [Publisher profile](https://clawhub.ai/user/juniarto-samsudin) <br>
- [TLDR.tech AI newsletter](https://tldr.tech/ai/) <br>
- [TechCrunch RSS feed](https://techcrunch.com/feed/) <br>
- [WIRED AI RSS feed](https://www.wired.com/feed/tag/ai/latest/rss) <br>


## Skill Output: <br>
**Output Type(s):** [Text, HTML, Shell commands, Configuration] <br>
**Output Format:** [HTML email digest with Markdown setup and run instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Fetches RSS and TLDR.tech AI items, deduplicates articles, summarizes RSS articles when the configured Ollama endpoint is available, and sends the digest through SMTP.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
