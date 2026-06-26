## Description: <br>
Provides procedures for calling the SimpleERP HTTP API with curl or PowerShell across products, inventory, warehouses, orders, invoices, payments, returns, master data, reports, and admin operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[icystssi-lang](https://clawhub.ai/user/icystssi-lang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and business-system administrators use this skill to have an agent inspect or operate a SimpleERP HTTP API instance through authenticated API calls. It supports read workflows, reports, and requested create, update, delete, inventory, order, permission, and API-key operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can direct an agent to change live ERP business, inventory, and admin data. <br>
Mitigation: Use a test instance or least-privilege API key and manually review create, update, delete, inventory, order, permission, and API-key operations before execution. <br>
Risk: Authenticated requests may target the wrong SimpleERP host or production environment. <br>
Mitigation: Confirm the base URL before authenticated requests and avoid production admin keys unless the user explicitly requires them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/icystssi-lang/simpleerp) <br>
- [SimpleERP API Endpoint Reference](references/ENDPOINTS.md) <br>
- [Admin and permissions](references/admin-and-permissions.md) <br>
- [Master data endpoints](references/master-data-endpoints.md) <br>
- [Products and pricing](references/products-and-pricing.md) <br>
- [Inventory and deliveries](references/inventory-and-deliveries.md) <br>
- [Documents, sales, and purchasing](references/documents-sales-purchasing.md) <br>
- [Returns and memos](references/returns-and-memos.md) <br>
- [Reports](references/reports.md) <br>
- [Query filters](references/query-filters.md) <br>
- [Workflows](references/workflows.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, markdown] <br>
**Output Format:** [Markdown with inline shell, curl, and PowerShell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May execute authenticated HTTP requests against the configured SimpleERP base URL when the user asks for API operations.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
