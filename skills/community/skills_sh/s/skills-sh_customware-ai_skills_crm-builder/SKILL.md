---
name: crm-builder
license: MIT
compatibility: Works with any AI coding assistant that supports the Agent Skills specification. Requires a running Customware SPA instance to consume the generated config.
metadata:
  author: ryan-price
  version: "1.1"
description: >
  Customer Relationship Management (CRM) vertical skill for the Customware SPA. Defines the
  section layout, entity views, and mapping rules for transforming a DOMAIN.md into a CRM tool.
  Use this skill when the Builder Agent classifies a customer's domain as contact management,
  sales pipeline, deal tracking, or customer relationship workflows.
  Trigger signals: contacts, leads, deals, pipeline, follow-ups, opportunities, accounts,
  customer data everywhere, can't track who talked to whom, sales process, referrals.
---

# CRM Builder Skill

## What This Skill Does

This skill defines how to build a **CRM tool** — a system for managing contacts, companies, deals, and the relationships between them.

CRM is structurally different from CPQ and trades-builder:
- **CPQ / Trades** = one record moves through sequential stages (stepper navigation)
- **CRM** = multiple entity types with relationships between them (entity navigation)

The left sidebar uses a **navigator pattern** (Contacts, Companies, Deals, Pipeline, Activities) — NOT a stepper. Users switch between entity views, not sequential stages.

**Common verticals:** sales teams, consulting firms, agencies, professional services, real estate, recruiting, B2B services, any business that tracks relationships and deals.

The builder reads this skill, reads the DOMAIN.md for the specific business terminology and pipeline stages, and generates a working prototype with the customer's actual entities, fields, and workflow.

## When to Use This Skill

Use this skill when the transcript or DOMAIN.md contains these signals:

| Signal | Examples |
|---|---|
| **Contact/people tracking** | "customer data is everywhere," "can't find who we talked to," "contacts in spreadsheets" |
| **Sales pipeline** | "deals," "opportunities," "pipeline," "stages," "won/lost" |
| **Follow-up tracking** | "follow-ups fall through the cracks," "no one knows who called last" |
| **Relationship management** | "referrals," "who knows who," "account management" |
| **Lead management** | "leads from website," "inbound inquiries," "lead source tracking" |

**Do NOT use this skill for:**
- Product configuration with pricing → use cpq-builder
- Construction/trades project tracking → use trades-builder
- Inventory and stock management → use erp-builder (future)

---

## Template Contract

Before you start building, understand what the template gives you and what this skill adds. This is the contract:

**The template (`app/layouts/MainLayout.tsx`) ships with:**
- `SidebarProvider`, `Sidebar`, `SidebarContent`, `SidebarInset`, `SidebarTrigger` — already wired
- `SidebarContent` is **empty** — this is your landing zone
- One brand slot in the header (logo placeholder + company name)
- `ModeToggle` and user menu in the header's right cluster

**This skill fills:**
- `SidebarContent` — with entity navigation (Pipeline, Contacts, Companies, Deals, Activities), quick filters, and recent records (see Layout Pattern below)
- The brand slot in the header — with the client's logo and company name from DOMAIN.md
- The header's right cluster — adds a role switcher `DropdownMenu` before the existing user menu, plus a global search input if there's room
- The `<Outlet />` in `<main>` — via route components for each entity view (Pipeline is default)

**This skill does NOT:**
- Add a second `Sidebar` component. There is one sidebar.
- Put a brand tile inside `SidebarContent`. Brand lives in the header only.
- Rewire `SidebarProvider` or replace the collapsible behavior. Use what's there.
- Build a stepper. CRM uses entity navigation — parallel views, not sequential stages.
- Collapse the detail view into a popover or modal by default. List/detail is a full-page pattern (list view → click → detail view in the main content area).

If you find yourself wanting to restructure `MainLayout.tsx`, stop — the answer is almost always to fill `SidebarContent` instead.

---

## Section Definitions

The CRM tool has **FIVE sections**. Unlike CPQ/trades-builder, these are NOT sequential stages — they are parallel entity views. Users navigate between them freely.

### Section 1: Pipeline

**What it does:** Visual board view of deals moving through stages.

**Display:**
- Kanban-style columns, one per pipeline stage from DOMAIN.md
- If DOMAIN.md does not define stages, use: Lead → Qualified → Proposal → Negotiation → Closed Won / Closed Lost
- Each deal item shows: deal name, company, value, assigned to, days in stage
- Drag-and-drop between columns (or click to move stage)
- "Add deal" button on each column
- Filter by assigned person, date range, or deal value

**If no pipeline stages exist in DOMAIN.md**, use the defaults above. The customer refines them after seeing the prototype.

### Section 2: Contacts

**What it does:** List/detail view of people.

**List view:**
- Table or lightweight list of contacts
- Columns: name, email, phone, company, last activity, tags
- Search and filter
- "Add contact" button

**Detail view (clicking a contact):**
- Contact detail: name, email, phone, company (linked), role/title, source, notes
- Activity timeline below: calls, emails, meetings, notes — most recent first
- Linked deals: list of deals associated with this contact
- "Log activity" button: quick-add a call, email, meeting, or note with date and description

**Fields from DOMAIN.md:**
- Entity Registry → Contact entity fields become the contact detail fields
- Terminology Glossary → exact field names and labels
- If DOMAIN.md doesn't define contact fields, use: name, email, phone, company, role, source, notes

### Section 3: Companies

**What it does:** List/detail view of organizations.

**List view:**
- Table of companies
- Columns: company name, industry, contacts count, deals count, total deal value
- Search and filter
- "Add company" button

**Detail view (clicking a company):**
- Company detail: name, industry, size, website, address, notes
- Contacts tab: list of people linked to this company
- Deals tab: list of deals linked to this company
- Activity timeline: aggregated from all contacts at this company

**Fields from DOMAIN.md:**
- Entity Registry → Company/Account entity fields
- If not defined: name, industry, size, website, address, notes

### Section 4: Deals

**What it does:** List/detail view of deals/opportunities.

**List view:**
- Table of deals
- Columns: deal name, company, contact, value, stage (badge), close date, assigned to
- Sort by value, stage, close date
- Filter by stage, assigned person
- "Add deal" button

**Detail view (clicking a deal):**
- Deal detail: name, value, stage (selectable dropdown), expected close date, probability, assigned to
- Linked contact and company (clickable links)
- Activity timeline specific to this deal
- Notes section
- "Mark as Won" / "Mark as Lost" action buttons when in final stages

**Stage progression:**
- Deal stage is a `Select` dropdown populated from DOMAIN.md pipeline stages
- Changing the stage updates the Pipeline board view automatically
- Won/Lost are terminal stages — show win/loss reason field when selected

### Section 5: Activities

**What it does:** Chronological feed of all activities across the CRM.

**Display:**
- Timeline/feed view, most recent first
- Each activity shows: type icon (call/email/meeting/note), description, linked contact, linked deal, date, logged by
- Filter by activity type, date range, person
- "Log activity" button at top

**Activity types:** Call, Email, Meeting, Note, Task. Use icons to distinguish.
- If DOMAIN.md defines different activity types, use those instead.

## Layout Pattern

The CRM tool uses a **two-panel layout** (left sidebar + main content) by default. A right sidebar appears contextually when viewing a record detail.

**This is NOT a stepper layout.** The left sidebar is entity navigation, not sequential stages.

### Left sidebar (always visible, collapsible)

The template ships `SidebarProvider`, `Sidebar`, `SidebarContent`, and `SidebarTrigger` already wired in `app/layouts/MainLayout.tsx`. `SidebarContent` is empty — that's the slot this skill fills with entity navigation. Do not re-wire the sidebar, do not add a second `Sidebar` component, and do not put a brand tile inside it. Brand identity lives in the header only (see Template Contract above).

**Sidebar heading:** Use a contextual label like "CRM" or the business name + "CRM" — not a workflow description. If the business name is short, "[Business] CRM" reads naturally; if it's long, just "CRM" is fine. The heading describes what the navigation IS.

| Component | Content |
|---|---|
| **Entity navigation** | A VERTICAL nav list inside `SidebarContent` with the five sections: Pipeline, Contacts, Companies, Deals, Activities. Each nav item shows: icon, label, and record count badge. Clicking navigates to that entity's view. **This is a navigator, NOT a stepper** — no step numbers, no completion states, no sequential flow. |
| **Quick filters** | Below the nav, show saved filters or views if the user creates them. E.g., "My deals," "Hot leads," "This week's follow-ups." |
| **Recent records** | Below filters, show the 3-5 most recently accessed records (any entity type) for quick navigation. Each shows name and entity type badge. Pin this section near the bottom of the sidebar so it's always visible without scrolling. |

### Main content (center — changes per section)

**The active section renders based on the selected nav item.** Only one section visible at a time.

```tsx
{activeSection === "pipeline" && <PipelineView />}
{activeSection === "contacts" && <ContactsView />}
{activeSection === "companies" && <CompaniesView />}
{activeSection === "deals" && <DealsView />}
{activeSection === "activities" && <ActivitiesView />}
```

**List/detail pattern within each section:**
- Default: list view, table, or lightweight board depending on the entity.
- Click a record: detail view with full-width sections, activity timeline, linked records
- "Back to list" button or breadcrumb to return
- This is a standard Salesforce/HubSpot pattern

### Right sidebar (contextual — appears on detail views)

When viewing a record detail (contact, company, or deal), a right sidebar can show:
- **Quick summary** — key fields at a glance
- **Linked records** — related contacts, deals, or companies
- **Upcoming activities** — next scheduled call/meeting

This sidebar is optional for the prototype. If the main content area has enough space, the detail view can be single-panel. Add the right sidebar only if the record detail benefits from simultaneous context.

### RBAC behavior

- Seed localStorage with roles from DOMAIN.md User Roles or Stakeholder Map.
- Role switcher is a **single `DropdownMenu` dropdown in the header bar**.
- **Assignment filtering**: When a role is active, optionally filter pipeline and deal views to show only records assigned to that person.
- **Activity attribution**: Activities logged should be attributed to the active role.
- CRM typically has fewer hard permission gates than CPQ — most users can see everything but own their assigned records.

### Price/value visibility

- Show deal values on Pipeline items, Deal list, and Deal detail.
- Show total pipeline value per stage at the top of the Pipeline view.
- Use the currency from DOMAIN.md.
- Format: "$25,000" or "$25,000 CAD" depending on DOMAIN.md.

### shadcn/ui component mapping

Treat cards as an exception, not the default layout primitive. Inline content into the page body whenever possible. Use cards only when something truly needs emphasis, separation, repetition, or dialog/detail framing. Do not build card-heavy dashboards, cards inside cards, or generic grids of floating panels.

| CRM Element | shadcn Component | Usage Notes |
|---|---|---|
| Entity nav items | `Button variant="ghost"` in vertical stack | Inside `SidebarContent`. Active item gets accent background. Icon + label + count badge. |
| Pipeline columns | Column sections, `ScrollArea` if many deals | Column header shows stage name + deal count + total value. Use cards only if items need strong separation. |
| Deal items (pipeline) | Compact clickable rows or subtle item blocks | Deal name, company, value, assigned avatar. |
| Contact/Company list | `Table` | Sortable columns, search input above. |
| Record detail | Full-width sections with `Separator` | Keep details inline in the main page body. |
| Activity timeline | Custom list with icons | Each item: type icon, description, date, linked record. Use `Avatar` for person. |
| Stage badges | `Badge` | Color-coded by stage: lead=gray, qualified=blue, proposal=amber, negotiation=purple, won=green, lost=red. |
| Deal value | `text-lg font-semibold` | Prominent on pipeline items and detail views. |
| Assignment dropdowns | `Select` | Populated from DOMAIN.md stakeholder names. NOT free text. |
| Activity type selector | `Select` or `RadioGroup` | Call, Email, Meeting, Note, Task. |
| Search inputs | `Input` with search icon | At top of every list view. |
| Action buttons | `Button` | Primary: "Add contact," "Log activity." Destructive: "Delete," "Mark as Lost." |
| Linked record chips | `Badge variant="outline"` | Clickable — navigates to the linked record. |
| Quick add forms | `Dialog` or inline form | Modal for adding a contact/deal quickly without leaving the current view. |
| Empty states | Inline empty block with centered text + action | "No contacts yet. Add your first contact." |
| Confirmation dialogs | `AlertDialog` | Delete record, mark deal as lost. |
| Toast notifications | `Sonner` / `toast()` | After create, update, delete, log activity. |

## Deterministic Mapping Rules

### Entity → CRM Record Mapping

| DOMAIN.md entity pattern | Maps to | In section |
|---|---|---|
| Contact / Person / Lead / Customer | Contact record | Contacts |
| Company / Account / Organization / Business | Company record | Companies |
| Deal / Opportunity / Sale / Prospect | Deal record | Deals + Pipeline |
| Activity / Call / Meeting / Email / Note | Activity entry | Activities + record timelines |
| Pipeline / Stage / Status | Pipeline stage columns | Pipeline |
| Referral / Source / Lead source | Source field on Contact or Deal | Contact/Deal detail |

### Relationship Mapping

| DOMAIN.md relationship | Implementation |
|---|---|
| Contact belongs to Company | Contact has a Company field (Select dropdown). Company detail shows linked contacts. |
| Deal has a Contact | Deal has a Contact field (Select dropdown). Contact detail shows linked deals. |
| Deal has a Company | Deal has a Company field (auto-populated from contact's company, editable). |
| Activity tied to Contact/Deal | Activity has Contact and Deal fields (Select dropdowns). |

### Business Rule → Behavior Mapping

| DOMAIN.md rule pattern | Implementation |
|---|---|
| "pipeline stages: X, Y, Z" | Pipeline columns use those exact names |
| "only [role] can close deals" | RBAC gate on "Mark as Won/Lost" buttons |
| "follow up within X days" | Show overdue badge on contacts/deals without recent activity |
| "deals over $X need approval" | Show approval requirement note on high-value deals |
| "referral source tracking" | Source field on contacts with defined dropdown values |
| Currency/tax/terms | Display on deal values and any invoicing views |

### Pipeline Stage Defaults

If DOMAIN.md does not define pipeline stages, use these:

| Stage | Color | Meaning |
|---|---|---|
| Lead | Gray | New unqualified inquiry |
| Qualified | Blue | Confirmed as a real opportunity |
| Proposal | Amber | Proposal or quote sent |
| Negotiation | Purple | In discussion, terms being worked out |
| Closed Won | Green | Deal signed, revenue booked |
| Closed Lost | Red | Deal did not close |

These defaults can be overridden by DOMAIN.md state models.

## Key UX Patterns from Real CRMs

These patterns are drawn from Salesforce, HubSpot, Pipedrive, and Freshsales. Follow them for a prototype that feels familiar to CRM users:

### 1. Everything links to everything
Contacts link to companies. Deals link to contacts and companies. Activities link to contacts and deals. Every linked name is clickable — clicking navigates to that record's detail view.

### 2. Activity timeline is the heartbeat
Every record (contact, company, deal) shows an activity timeline. The most recent interaction matters most. "When did we last talk to this person?" should be answerable at a glance.

### 3. Pipeline is the home screen
The Pipeline board view is the default landing page. Sales teams live here. Total pipeline value per stage is visible at the top.

### 4. Quick-add is everywhere
"Log a call" and "Add a deal" should be accessible from any view — either via a floating action button or a persistent "Quick add" in the header. Users shouldn't have to navigate away to log an interaction.

### 5. Search is global
One search bar that finds contacts, companies, and deals by name. Results grouped by entity type.

### 6. Empty states guide action
When a section has no records, show a helpful empty state: "No deals yet. Add your first deal to start tracking your pipeline." Include a primary action button.

## Reference Files

This skill expects these files to exist:

| File | Purpose |
|---|---|
| `DOMAIN.md` or `.tasks/domain.md` | Business terminology, entities, pipeline stages, roles, brand data |

The builder should read `DOMAIN.md` or `.tasks/domain.md` before writing any code.
