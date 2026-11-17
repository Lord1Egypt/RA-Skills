## Description:

A paid Chinese chat-native system-novel launcher that previews 爽文 scenarios, creates an Alipay unlock flow, verifies entitlement, and returns or installs the paid Skill package after payment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hengruizzzz](https://clawhub.ai/user/hengruizzzz)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to browse and purchase Chinese system-novel power fantasy scenarios, beginning with the paid 末世囤货：空间折叠 package. Operators use it to route users through payment, entitlement verification, and paid Skill package delivery without exposing paid scenario prompts before unlock.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A remotely returned paid Skill package may be installed without enough verification or explicit install consent.

Mitigation: Before installing, require explicit user consent and verify the package identity, source, publisher, version, digest or signature, and requested permissions against trusted release metadata.

Risk: Entitlement could be granted incorrectly if payment status relies on a user's claim or stale local state.

Mitigation: Unlock only after merchant-side order status or payment MCP results confirm payment; if state is lost, query the merchant backend rather than unlocking from memory.

Risk: Payment URLs and QR codes can be short-lived sensitive links.

Mitigation: Preserve cashier URLs exactly for the payment flow, avoid unnecessary exposure, and recreate expired links through the merchant payment surface.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/hengruizzzz/skills/shuangwen-simulator-v1)
- [Alipay Paid Access](artifact/references/alipay-paid-access.md)
- [Paid Scenario Notice](artifact/references/apocalypse-space-folding.md)
- [Public Scenario Catalog Preview](artifact/references/scenario-catalog-preview.md)
- [System Archetypes](artifact/references/system-archetypes.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration, Guidance]

**Output Format:** [Markdown and chat text with inline configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Alipay cashier URLs, paid package identifiers, entitlement status, and install instructions after payment verification.]

## Skill Version(s):

1.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
