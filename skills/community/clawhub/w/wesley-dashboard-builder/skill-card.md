## Description: <br>
Creates live dashboards, complete websites, and social-proof pages for Wesley-Agent with self-contained HTML, CSS, and JavaScript output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[georges91560](https://clawhub.ai/user/georges91560) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to generate mobile-first Wesley dashboard pages, live signal views, trading performance screens, and deployment guidance for VPS and Cloudflare-hosted sharing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill includes deployment workflows for live VPS, Docker, public tunnel, Telegram, and persistence operations. <br>
Mitigation: Use only on controlled Wesley infrastructure, replace hard-coded hosts and domains, avoid root access, and require explicit approval before SSH, Docker, Cloudflare, or Telegram actions. <br>
Risk: Generated dashboards may expose live portfolio or signal data through public sharing links. <br>
Mitigation: Publish only intentionally public data, restrict CORS to known origins, and add authentication when dashboards expose non-public information. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/georges91560/wesley-dashboard-builder) <br>
- [Telegram Bot API](https://api.telegram.org) <br>
- [Chart.js CDN](https://cdn.jsdelivr.net/npm/chart.js) <br>
- [Google Fonts](https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Syne:wght@400;600;800&display=swap) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline HTML, CSS, JavaScript, shell commands, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces self-contained frontend files and deployment instructions; optional Telegram integration requires TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
