## Description:

Provides guidance for querying Chinese company information from Tianyancha, Qichacha, Aiqicha, and public company-registration sources.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guohongbin-git](https://clawhub.ai/user/guohongbin-git)

### License/Terms of Use:


## Use Case:

External users and developers use this skill for due diligence, business-partner checks, market research, and company-risk lookup against Chinese business-information services.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API tokens for third-party company-data services could be exposed in shared prompts, logs, or command history.

Mitigation: Keep provider tokens out of shared logs and prompts, and use secret-management practices when adapting the sample API calls.

Risk: Provider data access may be paid, governed by third-party legal terms, or not updated in real time.

Mitigation: Review provider fees, terms, and data freshness before relying on results for due diligence or business decisions.

Risk: Installing the optional Python SDK can introduce supply-chain risk.

Mitigation: Install optional dependencies only in an isolated environment with a pinned trusted version.

## Reference(s):

- [Tianyancha Open API search endpoint](https://open.api.tianyancha.com/services/open/search/2.0?keyword=%E8%85%BE%E8%AE%AF)
- [Qichacha enterprise lookup endpoint](https://api.qichacha.com/ECIV4/GetEnterpriseByName?keyword=%E8%85%BE%E8%AE%AF)
- [Aiqicha](https://aiqicha.baidu.com/)
- [National Enterprise Credit Information Publicity System](http://www.gsxt.gov.cn/)
- [ClawHub skill page](https://clawhub.ai/guohongbin-git/skills/tianyancha-cn)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Code]

**Output Format:** [Markdown with inline bash and Python code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require third-party API tokens, paid provider access, and compliance review before use.]

## Skill Version(s):

1.0.0 (source: package.json and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
