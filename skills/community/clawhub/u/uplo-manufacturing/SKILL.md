---
name: uplo-manufacturing
description: AI-powered manufacturing knowledge management. Search work orders, quality inspections, production schedules, and equipment maintenance records with structured extraction.
---

# UPLO Manufacturing

Connects your AI assistant to the structured knowledge layer built from your plant floor documentation — work orders, inspection reports, preventive maintenance schedules, CAPA records, production batch logs, and equipment manuals. When a machine goes down at 2am or a customer reports a defect, you need answers from your own data, not a web search.

## Session Start

Pull your manufacturing context first. This loads your role (maintenance engineer, quality manager, production supervisor), active production priorities, and any open quality holds or equipment issues.

```
use_mcp_tool: get_identity_context
use_mcp_tool: search_knowledge query="open quality holds production line stoppages equipment downtime alerts"
```

Check directives if you need to understand current throughput targets or quality improvement initiatives:

```
use_mcp_tool: get_directives
```

## When to Use

- Investigating a non-conformance: what were the process parameters for batch #4471 on Line 3?
- Finding the torque specification and calibration schedule for the CNC mill in Cell B
- Pulling the FMEA (Failure Mode and Effects Analysis) for the new product introduction
- Checking if a specific raw material lot passed incoming inspection before it hit the floor
- Reviewing OEE trends for a production line to justify a capital expenditure request
- Locating the lockout/tagout procedure for the hydraulic press before a maintenance window
- Determining which shifts had the highest scrap rate last month and what corrective actions were taken

## Example Workflows

### Root Cause Analysis for Customer Complaint

A customer received parts with dimensional non-conformances. You need to trace back through your process.

```
use_mcp_tool: search_knowledge query="part number 7842-A dimensional inspection results CMM data last 90 days"
use_mcp_tool: search_with_context query="work order production batch part 7842-A process parameters tool wear records"
use_mcp_tool: search_knowledge query="CAPA corrective actions dimensional tolerance issues machining"
```

The structured extraction links inspection data back to specific work orders, machine settings, and operator certifications — giving you a complete traceability chain for your 8D report.

### Preventive Maintenance Planning

You're building next quarter's PM schedule and need to consolidate equipment data.

```
use_mcp_tool: search_knowledge query="preventive maintenance schedules all production equipment Q2 upcoming"
use_mcp_tool: search_knowledge query="equipment breakdown history unplanned downtime root causes 2025"
use_mcp_tool: export_org_context
```

Cross-reference PM intervals against actual failure data to shift from calendar-based to condition-based maintenance where the data supports it.

## Key Tools for Manufacturing

**search_knowledge** — Query across work orders, inspection records, PM logs, and SOPs simultaneously. The structured extraction means you get typed fields (part numbers, batch IDs, measurement values) not just raw text. Example: `"SPC control chart data injection mold press 12 cavity pressure"`

**search_with_context** — Follows the relationships between documents. A work order connects to the BOM, which connects to incoming material certs, which connect to supplier audits. Example: `"material traceability lot number RM-2025-0892 from receiving through finished goods"`

**report_knowledge_gap** — Found a machine with no documented setup procedure? A process with no control plan? Flag it. This feeds back into your quality system and ensures gaps get closed. Example: report that the new laser welder has no documented process validation (IQ/OQ/PQ).

**propose_update** — When an SOP is wrong or a spec has changed, propose the correction directly. It enters the review queue for the document owner. Example: update the anodizing bath concentration range after a process optimization study.

**flag_outdated** — Critical for manufacturing where revision control is everything. Mark superseded drawings, expired calibration certs, or obsolete work instructions before someone on the floor uses the wrong version.

## Tips

- Search by part number, work order number, or equipment asset ID for the most precise results — the extraction engine indexes these as structured fields, not just text tokens.
- Manufacturing data is deeply interconnected. If a simple `search_knowledge` doesn't give you the full picture, switch to `search_with_context` to traverse the relationships (part -> BOM -> supplier -> cert -> inspection).
- Always check document revision levels in results. If you spot an outdated revision, flag it immediately — in manufacturing, the wrong revision can mean scrapped parts or a safety incident.
- When logging conversations about quality issues, include the NCR or CAPA number — it makes the audit trail searchable when regulators or customers ask about corrective actions taken.
