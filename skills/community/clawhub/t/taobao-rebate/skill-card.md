## Description:

淘宝返利 routes Chinese rebate requests across authorization guidance, platform-link rebate conversion, product search, balance lookup, and withdrawal confirmation for Taobao, JD, and Pinduoduo shopping flows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[skyfile](https://clawhub.ai/user/skyfile)

### License/Terms of Use:

MIT-0

## Use Case:

External shoppers using ClawHub can ask in Chinese for rebate instructions, submit Taobao, JD, or Pinduoduo product links, search for products, check rebate account balances, and confirm withdrawals through the rebate service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can use WeChat/OpenID identifiers, shopping links or queries, and rebate account state with remote rebate service endpoints.

Mitigation: Install only if the publisher and service endpoints are trusted, and review privacy expectations for local account identifiers and shopping data before use.

Risk: The skill can submit withdrawal requests after a confirmation step.

Mitigation: Require explicit user confirmation, verify withdrawal amount and balance before submission, and monitor rebate account activity after use.

Risk: The skill requires verbatim return of script stdout, so remote service messages and generated rebate details may be shown without assistant-side reinterpretation.

Mitigation: Review service responses and treat rebate links, arrival text, and account messages as service-provided results rather than independently verified claims.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/skyfile/skills/taobao-rebate)
- [Publisher profile](https://clawhub.ai/user/skyfile)
- [Skill definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown or JSON emitted by Node.js CLI scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Verbatim script stdout may include product results, rebate links, coupon links, account balances, withdrawal status, and user guidance.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
