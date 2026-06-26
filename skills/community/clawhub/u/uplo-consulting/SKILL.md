---
name: uplo-consulting
description: AI-powered consulting knowledge management. Search engagement records, methodology frameworks, deliverable templates, and best practices with structured extraction.
---

# UPLO Consulting — Firm Knowledge at Your Fingertips

Consulting firms are knowledge businesses that routinely forget what they know. The partner who led the airline digital transformation last year is on a different engagement; the associate who built the market sizing model left six months ago; the methodology deck from the supply chain practice sits in someone's OneDrive. UPLO Consulting captures engagement artifacts, methodology IP, proposal content, and lessons learned so the firm's collective intelligence is accessible to every team, on every engagement, without playing "who do I ask?"

## Session Start

Fetch your identity to establish your practice area, seniority level, and current engagement assignments:

```
get_identity_context
```

Review firm-wide directives — these typically include utilization targets, proposal approval thresholds, and client confidentiality mandates:

```
get_directives
```

## When to Use

- Staffing a new engagement and need to find consultants who have delivered similar work (industry, capability, geography)
- Building a proposal and looking for relevant case studies, win rates for similar pursuits, and reusable methodology sections
- Starting a workstream and want to see how a previous team structured a similar analysis (e.g., total cost of ownership model for a manufacturing client)
- Preparing a client steering committee deck and need the firm's standard framework for presenting transformation roadmaps
- Conducting a lessons-learned review and want to surface patterns across multiple completed engagements
- Looking for the firm's published point of view on a topic (e.g., AI in financial services) to reference in a client workshop
- Checking what deliverables were produced on a past engagement before scoping a follow-on

## Example Workflows

### Proposal Development

A principal is pursuing a healthcare payer operational improvement engagement and needs to build the proposal over a weekend.

```
search_with_context query="healthcare payer operations improvement engagement case studies outcomes"
```

Find reusable methodology content from the operations practice:

```
search_knowledge query="operational excellence methodology framework Lean Six Sigma consulting deliverables"
```

Pull the firm's current strategic priorities to align the proposal narrative:

```
get_directives
```

Identify consultants with relevant experience for the proposed team:

```
search_knowledge query="healthcare payer experience consultants managed care claims processing"
```

### Engagement Kickoff Knowledge Transfer

A manager is starting on a new engagement and the previous phase was led by a different team. They need to get up to speed.

```
export_org_context
```

```
search_with_context query="client ABC Phase 1 findings current state assessment key recommendations"
```

```
search_knowledge query="client ABC stakeholder map decision makers change readiness assessment"
```

```
log_conversation summary="Onboarded to client ABC Phase 2; reviewed Phase 1 findings, stakeholder map, and org context" topics='["engagement-onboarding","client-ABC","knowledge-transfer"]' tools_used='["export_org_context","search_with_context","search_knowledge"]'
```

## Key Tools for Consulting

**search_with_context** — Consulting questions are inherently cross-cutting. "What did we learn from similar engagements?" requires connecting engagement records with client industries, methodologies used, and outcomes achieved. The graph traversal assembles this narrative. Example: `search_with_context query="retail supply chain transformation engagements outcomes cost savings"`

**search_knowledge** — When you need a specific artifact: a deliverable template, a framework diagram source, a pricing model, or a named methodology. Example: `search_knowledge query="zero-based budgeting methodology template"`

**export_org_context** — Produces the firm's practice structure, leadership, key systems (CRM, time tracking, knowledge management), and strategic priorities. Indispensable for new hire orientation and cross-practice collaboration.

**get_directives** — Firm directives govern proposal approval thresholds, travel policies, rate cards, and client confidentiality walls. Check before making commitments to clients.

**report_knowledge_gap** — If a pursuit team cannot find case studies for a new capability area, that is a strategic signal. Flagging the gap helps the practice development team prioritize IP creation.

## Tips

- Client names may be anonymized in the knowledge base due to confidentiality agreements. Search by industry, engagement type, and capability rather than relying solely on client names.
- Methodology frameworks are often versioned. Include "latest" or "v3" qualifiers if the firm maintains multiple generations of a methodology to avoid pulling deprecated content.
- When building proposals, combine `search_with_context` (for case studies and outcomes) with `search_knowledge` (for specific deliverable examples) — they serve complementary retrieval patterns.
- Always log proposal development sessions. Win/loss analysis relies on understanding what knowledge was available to the pursuit team at the time of proposal submission.
