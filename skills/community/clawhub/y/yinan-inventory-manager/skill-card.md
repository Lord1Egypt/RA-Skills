## Description:

E-commerce inventory management for Taobao, Douyin, and other platforms, including stock tracking, multi-store sync, supplier management, reorder alerts, and sales forecasting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yinanping-cpu](https://clawhub.ai/user/yinanping-cpu)

### License/Terms of Use:


## Use Case:

E-commerce sellers and operations teams use this skill to check stock reports, simulate inventory synchronization, configure low-stock alerts, and reason about supplier and reorder workflows across storefronts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release overstates live Taobao and Douyin capabilities while the bundled script uses sample inventory data.

Mitigation: Validate real platform integrations, credentials handling, and SKU mapping before relying on sync or reporting results.

Risk: Inventory sync actions can create incorrect stock levels if conflict rules or store targets are misconfigured.

Mitigation: Use dry-run review, scoped SKU tests, and explicit conflict-resolution settings before applying updates to production stores.

Risk: Alerting workflows may expose business or contact information if notification channels are not documented and protected.

Mitigation: Define privacy handling for email or WeChat alerts and avoid storing secrets or personal contact data in skill files.

## Reference(s):

- [Taobao Seller Center](https://myseller.taobao.com/home.htm/QnworkbenchHome/)
- [Douyin Merchant Center](https://fxg.jinritemai.com/ffa/mshop/homepage/index?channel=zhaoshang)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and CSV or JSON-style operational outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate local CSV stock reports when the bundled script is executed with an output path.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
