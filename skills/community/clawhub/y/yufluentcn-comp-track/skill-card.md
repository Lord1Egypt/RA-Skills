## Description:

Yufluent Comp Track compares manually provided competitor listing copy across titles, bullets, descriptions, and keywords, then returns differentiation suggestions and opportunity areas through the Yufluent cloud harness.

This skill is ready for commercial/non-commercial use.

## Publisher:

[metahuan](https://clawhub.ai/user/metahuan)

### License/Terms of Use:

MIT-0

## Use Case:

External ecommerce sellers, operators, and agents use this skill to compare manually supplied competitor listing copy for Amazon, Shopify, or TikTok. It helps identify positioning gaps, keyword opportunities, and concrete listing improvements without scraping platform product pages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local file paths supplied as listing inputs can cause those file contents to be uploaded for cloud analysis.

Mitigation: Review each file before passing its path and only submit content intended for the Yufluent service.

Risk: A configurable TOKENAPI_BASE_URL can receive the TOKENAPI_KEY and submitted listing content.

Mitigation: Use a trusted HTTPS endpoint, avoid untrusted local or third-party endpoints, and keep TOKENAPI_KEY secret.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/metahuan/skills/yufluentcn-comp-track)
- [Yufluent homepage](https://claw.changzhiai.com)
- [Yufluent OpenClaw](https://claw.changzhiai.com/app/openclaw)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown or plain text report returned from cloud skill execution]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires TOKENAPI_KEY; TOKENAPI_BASE_URL is optional and should point to a trusted service endpoint.]

## Skill Version(s):

1.1.2 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
