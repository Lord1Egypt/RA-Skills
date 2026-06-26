---
name: uplo-knowledge-management
description: AI-powered knowledge management intelligence. Search taxonomies, content curation records, expertise directories, and communities of practice with structured extraction.
---

# UPLO Knowledge Management — Organizational Learning & Expertise Intelligence

This is the meta-skill: knowledge management about knowledge management. Your organization's KM infrastructure — taxonomies, controlled vocabularies, expertise directories, community of practice charters, content lifecycle policies, lessons learned repositories, and knowledge audit results — is indexed in UPLO. Use this skill to understand, maintain, and improve how your organization captures, organizes, and shares what it knows.

## Session Start

```
get_identity_context
```

As a KM practitioner, you likely have broad read access across the organization. But KM strategy documents, knowledge audit findings, and expertise gap analyses may be restricted if they reveal competitive intelligence vulnerabilities.

## Example Workflows

### Knowledge Audit for a Business Unit

The Product Engineering division has experienced 40% turnover in the past year. The KM team needs to assess what institutional knowledge is at risk.

```
search_with_context query="subject matter experts and knowledge domain owners within Product Engineering and their documented areas of expertise"
```

```
search_knowledge query="knowledge transfer and documentation requirements in the offboarding process"
```

```
search_knowledge query="lessons learned and after-action review submissions from Product Engineering in the past 18 months"
```

Cross-reference the expertise directory with the departure list to identify critical knowledge areas that lost their primary expert without a documented successor.

### Taxonomy Governance Review

The enterprise taxonomy has grown organically and several business units are requesting new terms that may overlap with existing ones. The KM team needs to rationalize.

```
search_knowledge query="enterprise taxonomy governance policy including term proposal process and review committee membership"
```

```
search_with_context query="controlled vocabulary terms related to 'customer engagement' across all business units and their usage frequency"
```

```
search_knowledge query="taxonomy change log and approved term additions from the past 12 months"
```

## When to Use

- A KM analyst needs to find which communities of practice are active, dormant, or recently dissolved and why
- Someone asks whether the organization has a knowledge retention strategy for employees approaching retirement eligibility
- The CKO wants a dashboard view of content freshness across all knowledge repositories — what percentage of articles were reviewed in the past year
- A department head asks how to set up a new community of practice and what governance structure is required
- The IT team is evaluating a new collaboration platform and needs to understand current knowledge sharing patterns and tool adoption metrics
- An executive asks for evidence that the KM program is delivering measurable value — ROI metrics, reuse rates, time-to-competency improvements
- A content steward wants to know the disposition rules for records that have passed their retention period

## Key Tools for Knowledge Management

**search_with_context** — KM questions are inherently cross-cutting. A query like `query="which knowledge domains have no designated owner and what content exists in those domains"` requires traversing the expertise directory, domain taxonomy, and content inventory simultaneously. This is your primary tool.

**search_knowledge** — Use for specific KM artifacts: `query="community of practice charter template and facilitation guidelines"` or `query="content lifecycle policy including review frequency and archival criteria"`. KM frameworks tend to be well-documented, so direct searches work when you know what you are looking for.

**export_org_context** — The KM team's best friend. The full organizational context export reveals the state of institutional knowledge: which areas are well-documented, which have gaps, how knowledge flows between teams. Use this for annual KM program assessments.

**report_knowledge_gap** — This is the tool KM practitioners should use most aggressively. Every gap you report feeds back into the organizational twin's health score: `topic="machine learning model deployment procedures" description="Data Science team deploys 12 models to production but no standardized deployment documentation exists; knowledge is held by 2 senior engineers"`

**flag_outdated** — Content staleness is the KM team's eternal battle. When you encounter documents past their review date or referencing defunct organizational structures, flag them: `entry_id="..." reason="Article references the Digital Innovation Lab which was absorbed into Product Engineering in the Q2 2025 reorg; content owner and review cycle need reassignment"`

**propose_update** — KM practitioners are uniquely positioned to propose content improvements. When you find a knowledge article that is partially correct but needs updating, use the formal proposal mechanism to route the correction to the content owner.

## Tips

- KM is about connections, not just content. The most valuable KM queries are the ones that reveal relationships: who knows what, which teams share knowledge, where expertise is concentrated vs. distributed. Default to `search_with_context` over `search_knowledge` when exploring organizational capability.
- Distinguish between explicit knowledge (documented) and tacit knowledge (expertise held by individuals). When a search returns no documentation for a topic, check the expertise directory — the knowledge may exist in someone's head but not on paper. Report this as a knowledge gap with a recommendation to capture it.
- Content freshness is a leading indicator of KM health. When you surface documents, always note their last review date. A perfectly accurate article that has not been reviewed in 3 years signals a governance failure even if the content is still correct.
- Communities of practice are social structures, not just document collections. When advising on CoP health, look beyond content output to membership activity, event frequency, and cross-functional participation. A CoP with great documentation but no active discussion is a library, not a community.
