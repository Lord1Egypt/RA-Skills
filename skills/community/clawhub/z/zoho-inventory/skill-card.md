## Description: <br>
Zoho Inventory API integration with managed OAuth for managing items, sales orders, invoices, purchase orders, bills, contacts, and shipments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[byungkyu](https://clawhub.ai/user/byungkyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to inspect and manage Zoho Inventory records through Maton's managed OAuth gateway. It supports inventory, customer, vendor, order, invoice, bill, shipment, and connection-management workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access and modify sensitive Zoho Inventory business records through Maton. <br>
Mitigation: Install only when Maton and the connected Zoho Inventory account are trusted, and use the least-privileged Zoho account available. <br>
Risk: The MATON_API_KEY grants access to the Maton gateway and connected Zoho Inventory resources. <br>
Mitigation: Keep MATON_API_KEY secret and avoid exposing it in logs, shared shell history, or committed files. <br>
Risk: Write, delete, status change, invoice email, payment, credit, bill, order, shipment, or connection-management actions can change operational or financial records. <br>
Mitigation: Require explicit user confirmation before executing those actions, including the target resource and intended effect. <br>
Risk: Multiple active Maton connections can route a request to the wrong Zoho Inventory account. <br>
Mitigation: Specify the intended Maton-Connection header whenever multiple connections exist. <br>


## Reference(s): <br>
- [Zoho Inventory Skill on ClawHub](https://clawhub.ai/byungkyu/zoho-inventory) <br>
- [Maton](https://maton.ai) <br>
- [Maton Settings](https://maton.ai/settings) <br>
- [Zoho Inventory API v1 Introduction](https://www.zoho.com/inventory/api/v1/introduction/) <br>
- [Zoho Inventory Items API](https://www.zoho.com/inventory/api/v1/items/) <br>
- [Zoho Inventory Contacts API](https://www.zoho.com/inventory/api/v1/contacts/) <br>
- [Zoho Inventory Sales Orders API](https://www.zoho.com/inventory/api/v1/salesorders/) <br>
- [Zoho Inventory Invoices API](https://www.zoho.com/inventory/api/v1/invoices/) <br>
- [Zoho Inventory Purchase Orders API](https://www.zoho.com/inventory/api/v1/purchaseorders/) <br>
- [Zoho Inventory Bills API](https://www.zoho.com/inventory/api/v1/bills/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline Python, curl, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access, MATON_API_KEY, and an active Zoho Inventory connection through Maton.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
