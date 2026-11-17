## Description:

Web Scraper Pro fetches user-provided URLs through multiple web-to-Markdown services and returns clean Markdown content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[codehourra](https://clawhub.ai/user/codehourra)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to fetch webpages and convert extracted content into Markdown for reading, summarization, or downstream analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Off-platform crypto billing uses a hardcoded SkillPay API key.

Mitigation: Remove hardcoded credentials, disclose the payment provider and cost before use, and require explicit user consent before billing.

Risk: The scraper may fetch confidential, tokenized, internal, or private-network URLs.

Mitigation: Restrict use to public URLs and block private-network and metadata address ranges before any request.

Risk: Stealth anti-bot scraping can bypass site controls or terms.

Mitigation: Disable stealth bypass behavior by default and require policy review and user authorization for any site-specific scraping.

Risk: Unpinned scraping dependencies may change behavior or supply-chain risk over time.

Mitigation: Pin and review dependencies before installation or execution.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/codehourra/skills/web-scraper-pro)
- [Publisher Profile](https://clawhub.ai/user/codehourra)
- [SkillPay](https://skillpay.me)
- [markdown.new](https://markdown.new/)
- [defuddle.md](https://defuddle.md/)
- [Jina Reader](https://r.jina.ai/)
- [Scrapling](https://github.com/D4Vinci/Scrapling)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with Python and shell command snippets; fetched page content is returned as Markdown.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Charges 0.001 USDT per fetch through SkillPay; long fetched content may be truncated around 50000 characters.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
