# Vendor Onboarding Workflow — VendorGate System
**Framework:** VendorGate System
**Price:** FREE
**Category:** Productivity / Vendor Management
**Tags:** vendor management, onboarding, procurement, ops, compliance
**last_validated:** 2026-03-03

---

## What This Is

The VendorGate System is a complete vendor onboarding operating system for mid-market ops teams. It replaces ad-hoc email chains and scattered spreadsheets with a structured, repeatable intake-to-activation workflow that any team can execute from day one.

**Problem it solves:** Most organizations lose 3-5 hours per new vendor onboarding to back-and-forth emails, missing documents, and unclear approval ownership. VendorGate closes the gate until all requirements are met — then opens it on command.

**Output:** A fully onboarded vendor with all documents collected, all approvals signed off, and a welcome communication sent — with a complete audit trail.

---

## The VendorGate Framework

VendorGate operates across **5 sequential gates**. A vendor cannot advance to the next gate until the current gate is cleared. Each gate has a defined owner, checklist, and exit condition.

```
GATE 1: Intake & Qualification
        ↓ (Pass/Fail)
GATE 2: Document Collection
        ↓ (Complete/Incomplete)
GATE 3: Internal Approval Routing
        ↓ (Approved/Rejected/Conditional)
GATE 4: System Setup & Access
        ↓ (Configured/Pending)
GATE 5: Welcome & Activation
        ↓
    VENDOR ACTIVE ✓
```

---

## GATE 1: Intake & Qualification

**Owner:** Procurement / Ops
**Timeline:** Day 1
**Exit Condition:** Vendor passes basic qualification criteria

### 1.1 — Vendor Intake Form Fields

Collect the following at intake (use a form tool: Typeform, JotForm, Google Form, or intake email template):

**Company Information**
- Legal entity name
- DBA name (if applicable)
- State of incorporation / country of origin
- Business address (physical + mailing)
- EIN / Tax ID number
- Website URL
- Year founded
- Number of employees (range: 1-10 / 11-50 / 51-200 / 200+)

**Primary Contact**
- Name, title, email, phone
- Accounts payable contact (if different)
- Emergency / escalation contact

**Services / Products**
- Category of service or product (dropdown: Technology / Professional Services / Facilities / Marketing / Logistics / Other)
- Description of what they'll be providing
- Estimated annual spend (range)
- Contract start date (anticipated)

**Certifications & Compliance (initial self-report)**
- Is your business licensed to operate in [our state]? (Y/N)
- Do you carry general liability insurance? (Y/N) If yes, coverage amount?
- Do you carry workers' compensation? (Y/N)
- Are you minority/women/veteran-owned? (Y/N — for reporting purposes)
- Do you have any active litigation against your business? (Y/N)

### 1.2 — Qualification Decision Matrix

Score the intake responses using the following logic:

| Factor | Disqualifying Condition |
|--------|------------------------|
| EIN / Tax ID | Missing or invalid → cannot proceed |
| Business license | "No" for regulated service categories → hold |
| Active litigation | "Yes" → flag for legal review before advancing |
| Insurance self-report | "No" for GL → flag for Gate 2 follow-up |
| Estimated spend > $50K | Requires executive approval added to Gate 3 |

**Gate 1 Exit:** All non-flagged fields complete + disqualifying conditions resolved (or escalated). Log decision in vendor tracker with timestamp.

---

## GATE 2: Document Collection

**Owner:** Ops / Vendor (vendor submits, ops verifies)
**Timeline:** Days 2-5
**Exit Condition:** All required documents received, not expired, legible

### 2.1 — Document Checklist by Vendor Category

**All Vendors (Universal)**
- [ ] W-9 (US vendors) or W-8BEN (international)
- [ ] Certificate of Insurance (COI) — see COI skill for full requirements
- [ ] Signed NDA / Confidentiality Agreement (use your standard template)
- [ ] Business license or equivalent registration

**Technology / SaaS Vendors (additional)**
- [ ] SOC 2 Type II report (or equivalent security certification)
- [ ] Data Processing Agreement (DPA) — required if handling any personal data
- [ ] Subprocessor list (if applicable)
- [ ] Penetration test summary (if accessing internal systems)

**Professional Services (additional)**
- [ ] E&O / Professional Liability proof of coverage
- [ ] Proof of relevant professional licenses / certifications
- [ ] References (minimum 2 client contacts)

**Facilities / Contractors (additional)**
- [ ] Contractor's license (state-specific)
- [ ] Workers' Compensation certificate
- [ ] Equipment / tool insurance (if applicable)
- [ ] OSHA compliance certification (if applicable)

**Logistics / Shipping (additional)**
- [ ] Cargo insurance certificate
- [ ] DOT number (if motor carrier)
- [ ] Operating authority / MC number

### 2.2 — Document Review Standards

For each document received:

1. **Verify authenticity** — Is it on letterhead? Signed? From a recognized insurer/authority?
2. **Check expiration** — No document should expire within 60 days of receipt. If expiring soon, request renewal before completing Gate 2.
3. **Confirm coverage/scope** — Does it cover the work being contracted? (e.g., tech vendor COI must list "technology services")
4. **Log receipt** — Date received, document type, expiration date, reviewer initials

### 2.3 — Missing Document Follow-Up Protocol

**Day 0:** Send initial document request (use Template A below)
**Day 3:** If incomplete — send reminder (use Template B below)
**Day 7:** If still incomplete — escalate to vendor's senior contact
**Day 10:** If no response — pause onboarding, notify internal requestor

#### Template A — Initial Document Request
```
Subject: [Your Company] Vendor Onboarding — Documents Required

Hi [Contact Name],

Thank you for your interest in partnering with [Your Company]. To complete your onboarding, we need the following documents by [DATE — 5 business days]:

[List required documents from checklist above]

Please send to: [ops email or portal link]

Questions? Reply to this email or call [contact].

Best,
[Your Name]
[Your Company] Operations
```

#### Template B — Follow-Up Reminder
```
Subject: Action Required: Outstanding Documents for [Vendor Name] Onboarding

Hi [Contact Name],

We're still waiting on the following documents to complete your onboarding:

[List missing items with checkboxes]

We need these by [DATE] to keep your start date on track. If there's a delay, please let us know so we can plan accordingly.

[Your Name]
```

---

## GATE 3: Internal Approval Routing

**Owner:** Ops (routing) + Department Heads (approvals)
**Timeline:** Days 5-8
**Exit Condition:** All required approvals received

### 3.1 — Approval Routing Matrix

| Spend Tier | Required Approvers |
|------------|-------------------|
| Under $10K/year | Department head only |
| $10K-$50K/year | Department head + Finance |
| $50K-$100K/year | Department head + Finance + COO/VP Ops |
| Over $100K/year | All above + CEO/Executive team |
| Any vendor with data access | All above + IT/Security sign-off |
| Any vendor with legal exposure | All above + Legal/Counsel review |

### 3.2 — Approval Package (what each approver receives)

Send each approver a package containing:
1. **Vendor Summary Sheet** (1 page): vendor name, service category, estimated spend, contract term, key contacts
2. **Gate 1 Intake Summary**: qualification responses
3. **Gate 2 Document Status**: confirmation all docs received + any flags
4. **Risk Flags** (if any): litigation, expiring coverage, missing certs
5. **Requestor's Business Case**: why we need this vendor (brief — 3-5 sentences)
6. **Approval Action Requested**: Approve / Reject / Approve with Conditions

### 3.3 — Approval Conditions

If an approver approves with conditions:
- Document the condition in the vendor record
- Set a calendar reminder to verify the condition is met within 30 days
- Do NOT pause onboarding for minor conditions — note and track

If rejected:
- Document reason
- Notify internal requestor with reason
- Pause onboarding
- If vendor resubmits with corrections, restart at Gate 2

### 3.4 — Approval Turnaround SLA

Approvers have **3 business days** to respond. If no response:
- Day 4: Ops sends a nudge ("Quick approval needed for [Vendor]")
- Day 6: Ops escalates to approver's supervisor
- Day 8: Decision defaults to "hold" — document and notify requestor

---

## GATE 4: System Setup & Access

**Owner:** IT / Ops
**Timeline:** Days 8-10
**Exit Condition:** Vendor configured in all required systems

### 4.1 — System Setup Checklist

**Finance / Accounting**
- [ ] Vendor added to accounting system (QuickBooks, NetSuite, etc.)
- [ ] Payment terms set (Net 30, Net 60, etc.)
- [ ] ACH banking info collected (via secure form — never email)
- [ ] W-9 / tax document filed in accounting system
- [ ] Vendor contact assigned to PO workflow

**Procurement / Contracts**
- [ ] Signed contract uploaded to contract management system (or shared drive folder)
- [ ] Contract start date, end date, renewal date logged
- [ ] Reminder set for 90 days before contract end
- [ ] Contract assigned an internal owner

**Operations / Project Management**
- [ ] Vendor added to relevant project boards (if applicable)
- [ ] Scope of work documented and linked to vendor record
- [ ] Performance review schedule set (quarterly or annually per contract value)

**IT / Security (if vendor has system access)**
- [ ] Access permissions defined per least-privilege principle
- [ ] SSO / 2FA configured if accessing internal tools
- [ ] Vendor's security questionnaire responses filed
- [ ] Access provisioned with expiration date tied to contract end

**Compliance Record**
- [ ] COI expiration date entered in compliance tracker
- [ ] Business license expiration entered
- [ ] Next compliance review date set

---

## GATE 5: Welcome & Activation

**Owner:** Ops / Department Head
**Timeline:** Day 10-12
**Exit Condition:** Vendor confirmed active and relationship initiated

### 5.1 — Welcome Communication

Send a welcome email to the vendor's primary contact upon activation:

#### Template C — Vendor Welcome Email
```
Subject: Welcome to the [Your Company] Vendor Network

Hi [Contact Name],

Congratulations — you've completed our vendor onboarding process and are now an approved vendor for [Your Company]. We're looking forward to working with you.

Here's what to expect:

**Your key contacts at [Your Company]:**
- Day-to-day: [Name], [Title] — [email]
- Invoicing / Payments: [Name], [Title] — [email]
- Escalations: [Name], [Title] — [email]

**How to submit invoices:**
[Payment process — email to AP, portal link, etc.]

**Payment terms:** Net [X] days from invoice approval

**Your contract start date:** [DATE]

**Quarterly check-ins:** We conduct brief performance reviews with our key vendors each quarter. You'll hear from [Name] to schedule your first one.

If you have questions, reply to this email or contact [Name] directly.

Welcome aboard.

[Your Name]
[Title]
[Your Company]
```

### 5.2 — Internal Activation Notice

Notify the internal requestor and relevant team members:

```
Subject: ✅ [Vendor Name] — Onboarding Complete

[Vendor Name] has completed our vendor onboarding process and is now active in our system.

Key details:
- Service: [What they're providing]
- Contract start: [DATE]
- Contract end: [DATE]
- Internal owner: [Name]
- Payment terms: Net [X]
- Next compliance review: [DATE]

All documents are on file. Questions → [ops contact].
```

---

## Vendor Tracker Setup

### Required Fields in Your Vendor Master List

Create a tracker (spreadsheet or your vendor management tool) with these columns:

| Field | Type | Notes |
|-------|------|-------|
| Vendor ID | Auto-generated | e.g., VEN-001 |
| Vendor Name | Text | Legal entity name |
| DBA | Text | If applicable |
| Category | Dropdown | Technology / Services / Facilities / etc. |
| Status | Dropdown | Intake / Gate 2 / Gate 3 / Gate 4 / Active / Inactive / Terminated |
| Internal Owner | Text | Who manages this relationship |
| Contract Start | Date | |
| Contract End | Date | |
| Renewal Alert Date | Date | 90 days before end |
| Estimated Annual Spend | Currency | |
| W-9 on file | Y/N | |
| COI on file | Y/N | |
| COI Expiration | Date | Alert 60 days before |
| Business License Expiration | Date | Alert 60 days before |
| Last Performance Review | Date | |
| Next Performance Review | Date | |
| Risk Tier | Dropdown | Green / Yellow / Red |
| Notes | Text | |

### Tracker Automation (if using spreadsheet)

Set up conditional formatting:
- **Red highlight:** COI Expiration or License Expiration within 30 days
- **Yellow highlight:** Expiration within 60 days
- **Orange highlight:** Status = Gate 2 or Gate 3 for more than 7 days (stalled onboarding)

---

## VendorGate Implementation Checklist (First 30 Days)

Use this to stand up VendorGate in your organization:

**Week 1: Foundation**
- [ ] Customize intake form with your company fields
- [ ] Identify your approval routing matrix (fill in the spend tiers)
- [ ] Create vendor tracker (copy the field list above into your tool)
- [ ] Set up document collection folder structure (shared drive or vendor portal)
- [ ] Customize all email templates with your branding

**Week 2: Process**
- [ ] Run a test onboarding with one current vendor to validate the flow
- [ ] Identify gaps and update checklists
- [ ] Brief your team on the 5-gate process and their responsibilities
- [ ] Define who owns each gate

**Week 3: Automation**
- [ ] Set up expiration alerts (calendar reminders or spreadsheet alerts)
- [ ] Connect to your accounting system if possible
- [ ] Create a shared "Vendor Onboarding" email alias for document submission

**Week 4: Launch**
- [ ] Begin using VendorGate for all new vendors
- [ ] Review your backlog of existing vendors — identify any compliance gaps
- [ ] Schedule first quarterly vendor review for your top 5 vendors

---

## Expected Outputs

After running a vendor through VendorGate, you should have:
1. ✅ Complete vendor intake record (all fields populated)
2. ✅ All required documents collected, verified, and filed
3. ✅ All required approvals documented with timestamps
4. ✅ Vendor configured in accounting, contracts, and relevant systems
5. ✅ Welcome communication sent and confirmed received
6. ✅ Compliance calendar reminders set for document renewals
7. ✅ Vendor tracker updated with active status and all key dates

**Time to onboard (target):** 10-12 business days for a standard vendor
**Time to onboard (expedited):** 5-7 business days with dedicated ops focus

---

*VendorGate System — Part of the Vendor & Compliance Operations Pack by Remy Claw*
*More at remyclaw.com | @Remy_Claw on X*
