## Description:

Provides agent procedures for calling the SimpleERP HTTP API with curl, curl.exe, or PowerShell across products, inventory, warehouses, orders, invoices, payments, returns, master data, reports, and admin endpoints.

This skill is ready for commercial/non-commercial use.

## Publisher:

[icystssi-lang](https://clawhub.ai/user/icystssi-lang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to inspect and operate a SimpleERP backend through documented HTTP endpoints, including reads, writes, reports, and administrative workflows. It is intended for localhost or explicitly trusted SimpleERP API origins with appropriate API-key permissions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send API keys and make persistent ERP or admin changes, including against a user-specified HTTP host.

Mitigation: Use only localhost or an explicitly trusted HTTPS origin, avoid broad or admin API keys, and review write, delete, and admin actions before execution.

Risk: API-key creation or rotation responses can expose sensitive key material.

Mitigation: Treat API-key creation and rotation output as sensitive and store raw keys securely.

## Reference(s):

- [SimpleERP ClawHub listing](https://clawhub.ai/icystssi-lang/skills/simpleerp)
- [SimpleERP API skill instructions](SKILL.md)
- [SimpleERP API endpoint reference](references/ENDPOINTS.md)
- [Master data endpoints](references/master-data-endpoints.md)
- [Products, price lists, and related master data](references/products-and-pricing.md)
- [Inventory and deliveries](references/inventory-and-deliveries.md)
- [Sales and purchasing documents](references/documents-sales-purchasing.md)
- [Returns and memos](references/returns-and-memos.md)
- [Admin and permissions](references/admin-and-permissions.md)
- [End-to-end workflow examples](references/workflows.md)
- [Report curl examples](references/reports.md)
- [List query filters](references/query-filters.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, API calls, Configuration]

**Output Format:** [Markdown guidance with curl and PowerShell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use x-api-key credentials supplied by the user or SIMPLEERP_API_KEY; GET /api/health can run without authentication.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
