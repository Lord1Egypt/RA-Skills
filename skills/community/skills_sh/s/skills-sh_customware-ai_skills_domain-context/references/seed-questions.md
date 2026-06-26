# Seed Questions for Domain Bootstrapping

Use these when a project has no DOMAIN.md yet. Ask the user these questions to build the first version.
You don't need to ask all of them — use judgment based on what the user has already shared.

---

## Round 1 — The Big Picture (always ask)

1. **What does this application do in one sentence?**
   *(e.g., "It helps our rental company track equipment, customers, and service jobs.")*

2. **Who are the main types of people who use it?**
   *(e.g., "Office staff, field technicians, and managers.")*

3. **What are the 3-5 most important "things" in your system — the core objects your business tracks?**
   *(e.g., "Generators, Customers, Rental Agreements, Service Tickets, Invoices.")*

---

## Round 2 — Terminology (ask if they have internal jargon)

4. **Are there any terms your team uses that outsiders might not understand?**
   *(e.g., "We call overdue rentals 'stranded units' and our pricing tiers 'run rates'.")*

5. **Are any of those core objects called something specific internally vs. what a generic system might call them?**
   *(e.g., "We call customers 'accounts', and a rental agreement is always called a 'ticket'.")*

---

## Round 3 — Key Flows (ask to understand how the system behaves)

6. **Walk me through the most common thing a user does in this system, step by step.**
   *(This becomes your first entry in the Flow Catalog.)*

7. **What's the lifecycle of your most important entity — how does it get created, used, and closed?**
   *(e.g., "A Generator gets added to inventory, assigned to a Rental, returned, serviced, then re-deployed.")*

---

## Round 4 — Rules and Constraints (ask when building logic)

8. **Are there any hard rules that the system must enforce?**
   *(e.g., "A generator can't be rented if it's in maintenance status." or "Invoices must be approved before payment.")*

9. **Are there any things that seem obvious to your staff but might not be obvious to someone new?**
   *(e.g., "All prices are in USD except for the Quebec clients which are always CAD.")*

---

## Round 5 — External Connections (ask when building integrations)

10. **Does this system connect to any other software your company uses?**
    *(e.g., QuickBooks, Salesforce, a custom ERP, a GPS system, etc.)*

---

## Tips for Using These Questions

- Don't ask all 10 at once. Ask Round 1, build a draft, then ask follow-ups.
- If the user gives a long free-form answer, extract entities, terms, and rules from it and propose them.
- After asking, generate a draft DOMAIN.md and say: *"Here's what I understood — does this look right?"*
- Mark anything you're unsure about with `[NEEDS CONFIRMATION]` in the draft.

