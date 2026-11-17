## Description:

云启智联AI服务 helps agents submit bank receipts, bank statements, invoices, and general documents to Yunqi Zhilian's OCR service, retrieve asynchronous parsing results, and generate local accounting voucher drafts with confidence and review guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hinejon](https://clawhub.ai/user/hinejon)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, finance operators, and accounting agents use this skill to parse financial documents, review extracted OCR data, query asynchronous task status, and draft accounting vouchers for human review. It is intended for documents the user is authorized to process through Yunqi Zhilian's external service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive financial files may be sent to Yunqi Zhilian's external OCR service.

Mitigation: Use the skill only with financial files the user is authorized to process through that service.

Risk: Generated HTML and JSON previews may contain financial data and may be unsafe to open for untrusted documents until HTML escaping issues are fixed.

Mitigation: Treat generated previews as sensitive records and avoid opening previews from untrusted documents.

Risk: API keys can be exposed when passed directly on command lines in shared systems.

Mitigation: Prefer the skill's configuration flow or environment variable support instead of placing API keys in shell history.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hinejon/skills/yqzl-ai-service)
- [Yunqi Zhilian website](https://www.yunqi-zhilian.com/)
- [Yunqi Zhilian AI service experience page](https://www.yunqi-zhilian.com/AIService/experience/page)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, JSON, HTML files]

**Output Format:** [Markdown guidance with inline shell commands, JSON API results, and generated local HTML or JSON preview files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated previews and voucher files can contain sensitive financial records.]

## Skill Version(s):

1.2.5 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
