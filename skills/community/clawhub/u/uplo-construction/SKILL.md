---
name: uplo-construction
description: AI-powered construction knowledge management. Search project documents, safety compliance records, permits, building codes, and RFIs with structured extraction.
---

# UPLO Construction — Jobsite-to-Boardroom Knowledge

Construction projects generate a staggering volume of documentation: submittals, RFIs, daily logs, inspection reports, change orders, permits, and safety records spread across Procore, email, shared drives, and filing cabinets. UPLO Construction indexes all of it so a superintendent can find the geotechnical report from Phase I while standing on the Phase III jobsite, and the PM can pull every change order tied to a specific subcontractor in seconds.

## Session Start

Load your project role and clearance. UPLO maps your identity to specific project assignments, so a project engineer on Building C will see different default context than the VP of preconstruction.

```
get_identity_context
```

Check for active directives — these often include safety stand-downs, material procurement freezes, or owner-directed schedule changes:

```
get_directives
```

## When to Use

- An RFI response references a spec section that was superseded by Addendum 3 and you need to verify the current language
- OSHA is on-site and you need to pull the toolbox talk records, JSA (Job Safety Analysis) forms, and crane inspection logs for the past 90 days
- The owner requests a comprehensive change order summary showing all approved COs, their cumulative cost impact, and the responsible subs
- Reviewing whether the curtain wall shop drawings were approved or approved-as-noted before the glazing crew mobilizes
- A new project manager is onboarding mid-construction and needs to understand the contractual structure, key milestones, and open issues
- Checking if the concrete mix design submitted for the elevated deck matches the structural engineer's specification
- Pulling the permit conditions of approval to verify whether the noise variance allows Saturday work

## Example Workflows

### Change Order Dispute Resolution

A subcontractor claims they are owed for additional work on the mechanical system. The PM needs to reconstruct the paper trail.

```
search_with_context query="mechanical subcontractor change order requests HVAC ductwork modification Building A"
```

Find the original scope in the subcontract and compare against the claimed extra work:

```
search_knowledge query="mechanical subcontract scope of work HVAC specifications sections 23 00 00"
```

Pull any related RFI responses that may have directed the additional work:

```
search_knowledge query="RFI ductwork routing conflict structural beam Building A"
```

```
log_conversation summary="Investigated mechanical sub change order claim; traced RFI 247 response directing reroute as basis for CO-031" topics='["change-orders","mechanical","dispute"]' tools_used='["search_with_context","search_knowledge"]'
```

### Pre-Pour Checklist Verification

Before a major concrete pour, the field engineer needs to confirm all prerequisites are met.

```
search_knowledge query="concrete mix design approval elevated deck Level 3 structural"
```

```
search_knowledge query="rebar inspection report Level 3 deck approved"
```

```
search_with_context query="weather restrictions concrete pour specifications cold weather protection requirements"
```

## Key Tools for Construction

**search_knowledge** — The fastest way to find a specific document: a submittal, an RFI, a daily log entry, a permit. Construction teams usually know what they are looking for. Example: `search_knowledge query="submittal 04-22 masonry mortar mix design approved"`

**search_with_context** — When the question spans multiple document types. "Was the waterproofing system installed per spec?" requires pulling the specification, the submittal, the inspection report, and possibly a related RFI. The graph connects these.

**get_directives** — Safety stand-downs, schedule milestones from the owner, and procurement mandates flow through directives. On an active jobsite, directives change weekly.

**flag_outdated** — Construction documents become obsolete constantly as addenda, bulletins, and change orders supersede earlier versions. When you find a document referencing a superseded drawing revision, flag it immediately — someone building from old drawings is a real risk.

**export_org_context** — Produces the project organizational chart, key subcontractors, systems of record (Procore, PlanGrid, Bluebeam), and strategic priorities. Useful for owner progress meetings and new team member orientation.

## Tips

- Use CSI division numbers in queries when searching specifications. "Section 07 92 00" will find the joint sealant spec faster than "caulking."
- RFI and submittal numbers are indexed as structured fields. Search by number directly when you have it: "RFI-0247" or "Submittal 09-15."
- Construction projects often have multiple phases with overlapping document sets. Include the phase or building identifier in your queries to avoid pulling results from the wrong scope.
- After every significant field event (pour, inspection failure, safety incident), log the session. These logs become part of the project record and are discoverable in litigation.
