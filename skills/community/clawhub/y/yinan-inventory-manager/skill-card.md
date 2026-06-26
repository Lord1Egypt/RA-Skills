## Description: <br>
E-commerce inventory management for Taobao, Douyin, and other platforms. Use when tracking stock levels, syncing inventory across stores, managing suppliers, or automating reorder alerts. Supports multi-store sync and sales forecasting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yinanping-CPU](https://clawhub.ai/user/yinanping-CPU) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External e-commerce sellers and developers use this skill to check stock levels, sync inventory between Taobao and Douyin, manage low-stock alerts, and prepare supplier purchase-order workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live inventory sync and listing changes can affect sales operations if quantities or conflict-resolution rules are wrong. <br>
Mitigation: Use limited test stores or sample data first, add dry-run previews, require explicit confirmation, set per-SKU limits, and keep backups and audit logs. <br>
Risk: Automatic reorders and supplier purchase orders can create unwanted cost or supplier commitments. <br>
Mitigation: Require human approval before purchase orders are sent, enforce order-value limits, and use approved supplier lists. <br>
Risk: Email, WeChat, and supplier-contact data may expose sensitive operational or personal information. <br>
Mitigation: Minimize stored contact data, protect credentials outside the skill content, and define clear data-handling rules before using live notifications. <br>


## Reference(s): <br>
- [Taobao Seller Center](https://myseller.taobao.com/home.htm/QnworkbenchHome/) <br>
- [Douyin Seller Center](https://fxg.jinritemai.com/ffa/mshop/homepage/index?channel=zhaoshang) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, JSON examples, and optional CSV file outputs.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May describe inventory reports, sync actions, alert settings, supplier order data, and forecasting workflows.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
