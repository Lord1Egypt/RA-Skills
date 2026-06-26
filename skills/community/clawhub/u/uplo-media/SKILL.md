---
name: uplo-media
description: AI-powered media knowledge management. Search content production records, licensing agreements, distribution data, and audience analytics with structured extraction.
---

# UPLO Media

The media industry runs on rights, deadlines, and relationships — and the documentation behind all three is scattered across deal memos, distribution agreements, production bibles, ratings reports, and talent contracts. This skill gives your AI assistant structured access to that knowledge so you can answer questions about content rights windows, production budgets, talent availability, and audience performance without hunting through file shares.

## When to Use

- Checking whether your distribution rights for a title cover SVOD in Southeast Asia or only linear broadcast
- Finding the talent hold dates and options for a recurring cast member before greenlighting Season 3
- Pulling audience retention curves and completion rates for a series to inform renewal decisions
- Locating the music licensing terms for a track used in Episode 4 before you can clear international distribution
- Reviewing production insurance certificates and bond requirements for an upcoming shoot
- Comparing CPMs and fill rates across ad-supported content in your portfolio
- Answering "which titles in our library have rights expiring in the next 6 months?"

## Session Start

Orient yourself by loading your identity context and checking what content priorities leadership has set — slate decisions, acquisition targets, and distribution strategy all flow from directives.

```
use_mcp_tool: get_identity_context
use_mcp_tool: get_directives
use_mcp_tool: search_knowledge query="content slate priorities greenlight decisions upcoming productions"
```

## Example Workflows

### Rights Availability Check for International Sales

Your distribution team received an inquiry from a European broadcaster about licensing a title.

```
use_mcp_tool: search_with_context query="distribution rights windows Territory Europe title 'Northern Edge' holdbacks exclusivity"
use_mcp_tool: search_knowledge query="Northern Edge existing license agreements international territories"
use_mcp_tool: search_knowledge query="Northern Edge audience performance ratings demographics international comparable"
```

The context search connects the title's rights chain — original production agreement, domestic distribution deal, and any existing international licenses — so you can see exactly what's available and what's encumbered.

### Production Budget Reconciliation

You're closing out a production and need to reconcile actuals against the approved budget.

```
use_mcp_tool: search_knowledge query="Project Lighthouse production budget approved cost report actuals variance"
use_mcp_tool: search_knowledge query="Project Lighthouse vendor invoices post-production VFX sound mix"
use_mcp_tool: export_org_context
```

Pull the structured budget data alongside vendor payment records. The org context shows which production executives and line producers own the sign-off chain.

## Key Tools for Media

**search_with_context** — Essential for rights management. A single title has interconnected agreements (production, domestic, international, music, talent) and you need to see how they relate. Example: `"rights chain for 'After Midnight' including music sync licenses and talent residual obligations"`

**search_knowledge** — Fast lookup across your content library metadata, production records, and audience data. Example: `"audience demographics 18-49 rating performance unscripted content Q4 2025"`

**get_directives** — Surfaces the creative and business strategy that should inform content decisions: genre priorities, budget envelopes, platform strategy, and audience targets. Critical context before recommending acquisitions or renewals.

**propose_update** — When deal terms change (renegotiated license fee, extended rights window, revised delivery date), propose the update so the structured record stays current. Example: update the avail date for LATAM territories after a holdback extension.

**report_knowledge_gap** — Flag missing documentation before it becomes a problem. No signed chain-of-title for a library title? No E&O insurance certificate for an acquisition? Report it now.

## Example Queries That Work Well

Rather than generic searches, use the terminology your deals and production teams actually use:

- `"above-the-line costs pilot episode budget top sheet"`
- `"SAG-AFTRA scale payments series regular options"`
- `"deliverables list technical specifications OTT platform"`
- `"residual payment schedule backend participation profit definition"`
- `"clearance report music visual third-party IP episode 7"`

## Tips

- Rights data is time-sensitive. Always check the `valid_through` or expiration fields in results — a rights window that expired last month will still appear in search but shouldn't inform a sales pitch.
- Use `log_conversation` after any rights negotiation discussion. Media deals involve many informal agreements that eventually need to be papered, and having a searchable log prevents "I thought we agreed to..." disputes.
- When searching for audience data, include the measurement source (Nielsen, platform analytics, Comscore) since the same title can have very different numbers depending on methodology.
- Production documents use inconsistent naming. Search by project code name AND official title — many productions change names between development and release.
