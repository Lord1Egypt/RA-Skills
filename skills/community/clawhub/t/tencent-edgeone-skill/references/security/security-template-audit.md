# security-template-audit

Audit EdgeOne security policy template coverage, output template-to-bound-resource mappings, and find domains without any bound templates — suitable for security audit scenarios.

## APIs Involved

| Action | Description |
|---|---|
| `DescribeWebSecurityTemplates` | Query all security policy templates under the zone |
| `DescribeWebSecurityTemplate` | Query detailed configuration of a single template |
| `DescribeSecurityTemplateBindings` | Query the binding relationship between templates and domains |

> **Command usage**: This document only lists API names and process guidelines.
> Before execution, consult the API documentation via `../api/api-discovery.md` to confirm the complete parameters and response descriptions.

## Prerequisites

1. All Tencent Cloud API calls are executed via `tccli` — confirm login authentication is complete before execution.

2. You need to obtain the ZoneId first — see `../api/zone-discovery.md`.

## Execution Flow

**Trigger**: User says "which domains don't have a security template", "help me check template coverage", "are there any domains that missed binding a security policy", "help me audit security templates", "which domains have no security protection", "what's the template binding status", "help me check security templates", "are there domains without bound templates".

Call the following APIs in order to progressively build the template-binding resource mapping:

### Step 1: Get All Security Policy Templates

Call the `DescribeWebSecurityTemplates` API, record each template's `TemplateId` and `TemplateName` as input for subsequent queries.

### Step 2: Get Detailed Configuration for Each Template

Call the `DescribeWebSecurityTemplate` API, focusing on the following fields for subsequent status labeling:
- Whether the template is enabled (overall toggle status)
- Whether each protection module (WAF, CC, Bot, etc.) has rule configurations

### Step 3: Query Domain Binding Relationships for Each Template

Call the `DescribeSecurityTemplateBindings` API, collect the list of domains bound to each template, and aggregate into a global "covered domains set".

### Step 4: Get the Complete Domain List for the Zone

To identify uncovered domains, you need the complete domain list under the zone — call the `DescribeZoneRelatedDomains` API.

> If this API is unavailable or returns empty, try finding other APIs to get the domain list (such as `DescribeAccelerationDomains`) via `../api/api-discovery.md`.

### Step 5: Cross-Compare to Identify Uncovered Domains

Compute the difference between the "covered domains set" (aggregated from Step 3) and the complete zone domain list to produce the list of domains not bound to any template.

> ⚠️ **Note**: If the complete domain list cannot be obtained, explicitly state "currently can only output known coverage based on template binding relationships — cannot confirm whether there are missing domains" — do not make assumptions.

## Output Format

> **Language note**: Adapt the report language to match the user's language. The template below is an example — output should be in the same language the user is using.

```markdown
## Security Template Coverage Audit Report

**Zone**: example.com (ZoneId: zone-xxx)
**Audit Date**: YYYY-MM-DD
**Data Sources**: `DescribeWebSecurityTemplates` / `DescribeWebSecurityTemplate` / `DescribeSecurityTemplateBindings`

### Template-Binding Resource Mapping

| Template Name | Template ID | Bound Domains Count | Bound Domain List | Template Status |
|---|---|---|---|---|
| Production Template | template-xxx | 3 | a.com, b.com, c.com | ✅ Normal |
| Test Template | template-yyy | 0 | — (no domains bound) | ⚠️ Empty template |

### Coverage Summary

- Total templates: N
- Templates with bound domains: N / Empty templates (no domains bound): N
- Total covered domains: N
- **Uncovered domains: N**

### Uncovered Domain List

> The following domains are not bound to any security policy template and have a protection gap:

- example.com
- test.example.com
- staging.example.com

(If the complete domain list is unavailable, note here: "Data is incomplete, showing known coverage only")

### Recommended Actions

- Uncovered domains: Evaluate and bind an appropriate security template
- Empty templates: Confirm whether they are reserved templates; consider cleanup if unused
```

> **Read-only disclaimer**: This skill only performs query operations and does not perform any binding or modification. To bind templates, use the console or call the appropriate write APIs — confirm the impact scope before operating.
