---
name: trades-builder
license: MIT
compatibility: Works with any AI coding assistant that supports the Agent Skills specification. Requires a running Customware SPA instance to consume the generated config.
metadata:
  author: ryan-price
  version: "1.4"
description: >
  Trades Operations vertical skill for the Customware SPA. Defines the section
  layout, config schema, and mapping rules for transforming a DOMAIN.md into a
  trades operations tool. Use this skill when the Builder Agent classifies a
  customer's domain as construction, field service, or trades project tracking.
  Trigger signals: estimates, job specs, scope items, square footage, field scheduling,
  subtrade payments, trade invoices, customer invoices, project stages, crew tracking.
---

# Trades Operations Skill

## What This Skill Does

This skill defines how to build a **trades operations tool** — the estimate-to-payment workflow that construction trades and field service businesses run daily.

It is NOT a generic project management tool (Jira/Asana). It is NOT a CPQ tool (no product configuration). It is a workflow tracker specifically shaped for businesses that:
- Create estimates based on measured scope items (square footage, linear feet, units)
- Schedule and assign field work to crews or subtrades
- Track progress by scope item and location
- Pay subtrades based on completed measured work
- Invoice customers and collect payment

**Common verticals:** drywall, roofing, HVAC, plumbing, electrical, painting, flooring, concrete, landscaping, general contracting.

The builder reads this skill, reads the DOMAIN.md for the specific trade and terminology, and generates a working prototype that uses the customer's actual scope items, pricing, and workflow stages.

## When to Use This Skill

Use this skill when the transcript or DOMAIN.md contains these signals:

| Signal | Examples |
|---|---|
| **Scope items with measurements** | square footage, linear feet, board feet, units per area |
| **Field scheduling** | crew assignment, job calendar, field work planning |
| **Subtrade payments** | paying subs, trade payments, per-sqft pay rates |
| **Estimate-to-invoice workflow** | estimate → schedule → work → invoice cycle |
| **Trade-specific scopes** | insulation, drywall, taping, roofing, framing, plumbing rough-in |
| **Location-based specs** | different specs per floor, per room, per zone |
| **Dual invoicing** | trade invoices (outgoing to subs) AND customer invoices (incoming from clients) |

**Do NOT use this skill for:**
- Product configuration with dependencies → use cpq-builder
- Inventory and stock management → use erp-builder (future)
- Generic CRM or contact management → use crm-builder

---

## Template Contract

Before you start building, understand what the template gives you and what this skill adds. This is the contract:

**The template (`app/layouts/MainLayout.tsx`) ships with:**
- `SidebarProvider`, `Sidebar`, `SidebarContent`, `SidebarInset`, `SidebarTrigger` — already wired
- `SidebarContent` is **empty** — this is your landing zone
- One brand slot in the header (logo placeholder + company name)
- `ModeToggle` and user menu in the header's right cluster

**This skill fills:**
- `SidebarContent` — with the vertical stepper and saved projects (see Layout Pattern below)
- The brand slot in the header — with the client's logo and company name from DOMAIN.md
- The header's right cluster — adds a role switcher `DropdownMenu` before the existing user menu
- The `<Outlet />` in `<main>` — via route components for each of the five sections

**This skill does NOT:**
- Add a second `Sidebar` component. There is one sidebar.
- Put a brand tile inside `SidebarContent`. Brand lives in the header only.
- Rewire `SidebarProvider` or replace the collapsible behavior. Use what's there.
- Put the stepper as horizontal tabs in the main content area. The stepper is a vertical list inside `SidebarContent`.

If you find yourself wanting to restructure `MainLayout.tsx`, stop — the answer is almost always to fill `SidebarContent` instead.

---

## Section Definitions

The trades-builder tool has **FIVE sections**. These are fixed — they come from this skill, not from the business process described in the transcript.

### Section 1: Estimate

**What it does:** Capture the project details and build the scope-based estimate.

**Project details (editable inline):**
- Project name — inline editable text (click to edit, save on blur)
- Customer name — inline editable text
- Address — inline editable text
- Estimate number — auto-generated, read-only
- Lead source — `Select` dropdown if DOMAIN.md defines sources, otherwise free text
- Estimator notes — `Textarea`, always editable

**Scope items table (the core of this section):**
This table is the most important element in the app. Each row represents a scope of work with measured quantities.

| Column | Type | Editable | Notes |
|---|---|---|---|
| Scope | `Select` dropdown | Yes | Options from DOMAIN.md: insulation, drywall, taping, sanding, cleaning, priming, etc. |
| Location | Text input | Yes | e.g., "Main floor living room," "Basement suite" |
| Spec/Type | Text input or `Select` | Yes | e.g., "Type X," "Moisture resistant," "R-20 batt," "Level 4 finish" |
| Sq ft | Number input | Yes | Square footage for this scope at this location |
| Rate | Number input | Yes | Dollar rate per sqft (CAD) |
| Line total | Calculated | No | Sqft × Rate, auto-calculated |
| Actions | Delete button | — | Trash icon to remove the row |

- **"Add row" button** below the table to add more scope items
- **Multiple rows per scope type** — e.g., two drywall rows for different locations with different types
- **Auto-calculated footer:** Subtotal, Tax (GST 5%), Total — updates on every cell change
- **All cells are directly editable** — click a cell, type, blur to save. See frontend-design skill for inline editing pattern.

**Data from DOMAIN.md to use:**
- Entity Registry → Job Specification sub-items become the Scope dropdown options
- Business Rules → unit of measure (sqft, lft), tax type and rate, payment terms
- Terminology Glossary → exact scope names (not generic labels)

### Section 2: Schedule

**What it does:** Plan field work assignments and sequence.

**Fields (editable):**
- Assigned roles/people — `Select` dropdowns from DOMAIN.md Stakeholder Map, NOT free text
- Scope sequence — reorderable list showing which scope items happen in what order
- Start date — date picker, editable
- Target completion date — date picker, editable
- Field crew notes — `Textarea`, editable

**If DOMAIN.md mentions scheduling tools** (e.g., "Bold for scheduling"), reference them in the section description: "Use Bold to line up the field crew."

### Section 3: In Progress

**What it does:** Track work completion per scope item and location.

**Display:**
- Table populated from Estimate's scope items — same rows, now being tracked for completion

| Column | Type | Editable | Notes |
|---|---|---|---|
| Scope | Text | No | From Estimate |
| Location | Text | No | From Estimate |
| Sq ft | Number | No | From Estimate |
| Status | `Select` dropdown | Yes | Not Started / In Progress / Completed |

- Status changes save immediately to localStorage
- "Mark all completed" button for bulk update
- Progress indicator: "3 of 5 scope items completed"

### Section 4: Close Out

**What it does:** Handle the dual payment flow — pay subtrades and invoice the customer.

**Display — two invoice sections side by side:**

**Trade Invoice section:**
- Subtrade payment amount — auto-calculated from completed scope items (sqft × rate)
- Status: `Select` dropdown — Ready to pay / Paid
- Payment date — date picker, editable when status is Paid
- Reference to Bold if mentioned in DOMAIN.md

**Customer Invoice section:**
- Invoice amount — subtotal + tax from Estimate
- Status: `Select` dropdown — Ready to send / Sent / Paid
- Invoice date — date picker, editable
- Reference to Arvest if mentioned in DOMAIN.md

- "Close out job" action button that marks the project as Completed
- Both invoice statuses must be saved to localStorage

**If DOMAIN.md mentions invoicing tools**, reference them in the section headers: "Trade invoice (Bold)" and "Customer invoice (Arvest)."

### Section 5: Job Summary

**What it does:** Read-only summary of the completed project — the final output view.

**Layout (top to bottom):**
1. **Company header** — brand logo from domain.md Brand Logos section (use the logo URL or path provided) + company name + placeholder address ("123 Main St, City, Province, Postal Code — update in settings")
2. **Project metadata** — project name, customer, address, estimate number, dates, assigned to. Two-column grid of label/value pairs.
3. **Scope summary table** — all scope items with scope type, location, spec/type, sqft, rate, line total. Clean `Table` with right-aligned numeric columns.
4. **Totals block** — subtotal, tax (GST 5%), total. Total is large and bold.
5. **Payment status** — trade invoice status badge + customer invoice status badge, side by side.
6. **Terms** — payment terms (Net 30), currency (CAD).

**This view is entirely read-only.** No edit controls, no inputs, no dropdowns. Users click back to Estimate or Schedule in the stepper to make changes. The Job Summary is the output, not the workspace.

## Layout Pattern

The trades-builder tool uses a **three-panel layout** with **FIVE sections** (not four). The builder MUST follow this layout.

### Left sidebar (always visible, collapsible)

The template ships `SidebarProvider`, `Sidebar`, `SidebarContent`, and `SidebarTrigger` already wired in `app/layouts/MainLayout.tsx`. `SidebarContent` is empty — that's the slot this skill fills. Do not re-wire the sidebar, do not add a second `Sidebar` component, and do not put a brand tile inside it. Brand identity lives in the header only (see Template Contract above).

**Sidebar heading:** Use a contextual label like "Workflow" or "Project workflow" — not the company name. The heading describes what the navigation IS.

| Component | Content |
|---|---|
| **Stepper** | A VERTICAL list of ALL FIVE sections inside `SidebarContent`: (1) Estimate, (2) Schedule, (3) In Progress, (4) Close Out, (5) Job Summary. Each step shows: step number, label, subtitle from section description, and completion state. **Vertical stepper in the sidebar — NOT horizontal tabs in the main content area.** |
| **Saved projects** | List of projects stored in localStorage. Each shows name + customer + status badge (Estimated / Scheduled / In Progress / Completed). Pin this section to the bottom of the sidebar so it's always visible without scrolling. Double-click a project name to rename inline. |

**CRITICAL: Stepper labels come from THIS SKILL, not from DOMAIN.md.** The DOMAIN.md state model may list `estimated, scheduled, in progress, completed` — those are the project's STATUS values for badges. The stepper LABELS are the skill's section names: **Estimate, Schedule, In Progress, Close Out, Job Summary.** These are different things. The stepper has 5 steps. The domain has 4 statuses. Do not use the domain status list as stepper labels — you'll get 4 steps instead of 5 and lose Close Out and Job Summary.

### Main content (center — changes per section)

**Only the active section renders.** Do NOT stack all sections on one scrolling page. Do NOT combine multiple sections into one panel (e.g., "Schedule / In Progress / Close Out" as one section is WRONG — each is its own panel). Do NOT use horizontal tabs. Each stepper step shows its corresponding panel at FULL WIDTH of the main content area. All other panels are hidden.

Implementation: use a `currentStep` state variable (0–4). Render only the panel that matches `currentStep`.

```tsx
// ALL FIVE panels, conditional rendering
{currentStep === 0 && <EstimatePanel />}
{currentStep === 1 && <SchedulePanel />}
{currentStep === 2 && <InProgressPanel />}
{currentStep === 3 && <CloseOutPanel />}
{currentStep === 4 && <JobSummaryPanel />}
```

| Section | What renders |
|---|---|
| **Estimate** | Project details form + scope items table with add/remove rows, quantities, rates, auto-calculated totals. "Save estimate" and "Continue to Schedule" buttons. |
| **Schedule** | Role/crew assignment dropdowns (from DOMAIN.md), scope sequence, date fields, field notes. "Continue to In Progress" button. |
| **In Progress** | Location-based scope tracking table with status per row. "Mark completed" button. |
| **Close Out** | Trade invoice section + customer invoice section, side by side. "Close out job" button. |
| **Job Summary** | Read-only formatted project summary with company header, scope table, totals, payment status. |

### Right sidebar (always visible)

| Component | Content |
|---|---|
| **Project summary** | Live-updating sidebar summary: current stage, estimate number, payment terms, subtotal, tax, total. Updates when scope items change. |
| **Workflow notes** | Business rules from DOMAIN.md displayed as contextual guidance. Reference BR-IDs. |
| **Actions** | Back, Continue, and Delete project buttons. Primary action uses brand accent color. |

### RBAC behavior

- Seed localStorage with roles from DOMAIN.md User Roles or Stakeholder Map.
- Role switcher is a **single `DropdownMenu` dropdown in the header bar** — not separate buttons. Shows active role name and badge.
- **Approval gating**: If DOMAIN.md says only certain roles can close out or approve, disable those buttons for other roles.
- **Role-specific views**: If roles handle specific stages (e.g., estimator handles Estimate, project manager handles Schedule), show relevant context when that role is active.

### Price visibility

- Show prices on the Estimate panel — unit rates, line totals, subtotal, tax, total.
- Show running totals in the right sidebar Project Summary.
- Use the currency, tax type, and tax rate from DOMAIN.md.
- Format prices with the currency code (e.g., "$3,900.40 CAD" or "$3,900.40" with "CAD" shown in the summary).

### shadcn/ui component mapping

Treat cards as an exception, not the default layout primitive. Inline content into the page body whenever possible. Use cards only when something truly needs emphasis, separation, repetition, or dialog/detail framing. Do not build card-heavy dashboards, cards inside cards, or generic grids of floating panels.

| Trades-ops Element | shadcn Component | Usage Notes |
|---|---|---|
| Project details form | `Input`, `Label`, `Select` | Project name, customer, address. Stack label above input. |
| Scope items table | `Table`, `TableHeader`, `TableRow`, `TableCell` | Add/remove rows. Right-align numeric columns. |
| Scope item status | `Badge` | Not Started = outline, In Progress = blue, Completed = green. |
| Project status badges | `Badge` | Estimated = amber, Scheduled = blue, In Progress = blue, Completed = green. |
| Role badges | `Badge` | Staff = outline, Approver = default. |
| Assignment dropdowns | `Select`, `SelectContent`, `SelectItem` | Populate from DOMAIN.md stakeholder names. NOT free text inputs. |
| Invoice status sections | Inline sections with `Separator`, `Badge`, `Select`, `Input` | Trade invoice + customer invoice side by side. Use cards only if the invoices need stronger separation. |
| Action buttons | `Button` | Primary: brand accent, "Continue." Secondary: outline, "Back." Destructive: "Delete project." |
| Stepper navigation | Custom vertical list | Inside `SidebarContent`. Step number in circle, label, subtitle, completion checkmark. Use `cn()` for states. |
| Role switcher | `DropdownMenu` | Single dropdown trigger in header. |
| Project summary sidebar | Inline stacked label/value rows | Labels muted, values bold. Total row large and prominent. |
| Workflow notes | Compact muted note block | Reference material with BR-IDs. |
| Date fields | `Input` with `type="date"` | Start date, target completion. |
| Notes/textarea | `Textarea` | Estimator notes, field crew notes. |
| Confirmation dialogs | `AlertDialog` | Delete project, close out job. |
| Toast notifications | `Sonner` / `toast()` | After save, mark complete, close out. |

## Deterministic Mapping Rules

### Entity → Scope Item Mapping

When the Knowledge Agent extracts entities from the transcript, map them to the trades-builder structure:

| DOMAIN.md entity | Maps to | In section |
|---|---|---|
| Project / Job | Project record (top-level) | All sections |
| Estimate | Estimate data (prices, terms) | Estimate panel |
| Job Specification / Scope | Scope items table rows | Estimate + In Progress |
| Invoice | Customer invoice section | Close Out |
| Trade Invoice | Trade invoice section | Close Out |
| Subtrade Payment | Payment status on trade invoice | Close Out |
| Field Schedule | Schedule data | Schedule panel |

### Business Rule → Validation Mapping

| DOMAIN.md rule pattern | Implementation |
|---|---|
| "tracked by square footage" | Scope items table uses sqft as quantity column |
| "paid per square footage" | Trade invoice amount = sum of (sqft × rate) for completed scope items |
| "different [type] per location" | Scope items table includes Location column, multiple rows per scope type |
| "stages: estimated, scheduled, in progress, completed" | Stepper stages match exactly |
| "manually entered" | Project creation form, no import flow |
| "GST/HST at X%" | Tax line in estimate and invoice, tax type as label |
| "Net 30/45" | Payment terms shown in summary and invoice |
| "only [role] can [action]" | RBAC gate on the relevant button |

### Integration → Reference Mapping

If DOMAIN.md lists integration points (e.g., Bold, Arvest, QuickBooks), reference them in section descriptions and workflow notes — but do NOT build integration UI. The prototype is localStorage-only. Integration comes in the full build.

## Reference Files

This skill expects these files to exist:

| File | Purpose |
|---|---|
| `DOMAIN.md` or `.tasks/domain.md` | Business terminology, entities, rules, roles, brand data |

The builder should read `DOMAIN.md` or `.tasks/domain.md` before writing any code.
