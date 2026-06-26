## Description: <br>
Intelligent web scraper that fetches URLs and returns clean Markdown content. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[CodeHourra](https://clawhub.ai/user/CodeHourra) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to extract readable Markdown from web pages through a layered fetch strategy. It is suited for public web content where the user accepts the per-fetch charge and external service handling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can charge 0.001 USDT through a third-party billing service before each fetch. <br>
Mitigation: Use only when the pricing and billed SkillPay user ID are understood, and prefer platform-managed billing or stronger publisher documentation before deployment. <br>
Risk: URLs, search queries, and page content may be sent to external scraping and conversion services. <br>
Mitigation: Avoid private, authenticated, internal, or token-containing links, and use the skill only for content that may be shared with those services. <br>
Risk: Embedded billing credentials and stealth scraping behavior increase operational and trust risk. <br>
Mitigation: Review the skill before installing, restrict use to permitted sites, and require clear publisher documentation for billing and scraping behavior. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/CodeHourra/web-scraper-pro) <br>
- [SkillPay](https://skillpay.me) <br>
- [markdown.new](https://markdown.new/) <br>
- [defuddle.md](https://defuddle.md/) <br>
- [Jina Reader](https://r.jina.ai/) <br>
- [Scrapling](https://github.com/D4Vinci/Scrapling) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Text, Guidance] <br>
**Output Format:** [Markdown content with fetch status and payment guidance when applicable] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include source URL, source service, character count, and top-up guidance if payment is required.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata; artifact frontmatter reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
