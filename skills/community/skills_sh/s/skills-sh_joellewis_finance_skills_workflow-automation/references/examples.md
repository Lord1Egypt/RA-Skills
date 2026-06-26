# Workflow Automation — Worked Examples

## Contents

1. [Example 1: Designing an Approval Workflow for High-Value Account Transfers](#example-1-designing-an-approval-workflow-for-high-value-account-transfers) — approval matrix by transfer type, value, and risk; state machine; timeout escalation
2. [Example 2: Building SLA Monitoring for Account Maintenance Requests](#example-2-building-sla-monitoring-for-account-maintenance-requests) — SLA targets per maintenance type, aging thresholds, advisor visibility
3. [Example 3: Implementing Escalation Rules for Aging Corporate Action Elections](#example-3-implementing-escalation-rules-for-aging-corporate-action-elections) — Day -10 to Day 0 escalation timeline, response-rate alerts, post-event review

## Example 1: Designing an Approval Workflow for High-Value Account Transfers

**Scenario:** A mid-size broker-dealer processes approximately 300 account transfers per month. Management has identified that high-value transfers (over $500,000) lack a consistent approval process — some receive supervisory review, others do not, depending on which analyst processes them. The compliance department has flagged this as a FINRA Rule 3110 supervisory concern. The firm needs a structured approval workflow for all account transfers, with additional controls for high-value and high-risk transfers.

**Design Considerations:**
- FINRA Rule 11870 imposes strict timelines (3 business days for validation, 6 total for completion), so the approval workflow cannot add significant delay.
- The firm processes three transfer types: full ACAT, partial ACAT, and non-ACAT (journals, wire transfers, DTC deliveries).
- Transfer risk varies by type, dollar value, and circumstances (e.g., transfers to third-party accounts, transfers from elderly clients, transfers initiated shortly after an advisor change).
- The firm has 12 operations analysts, 3 team leads, and an operations manager. Compliance has one dedicated surveillance analyst for operations reviews.

**Analysis:**

Define the approval matrix:

| Transfer Type | Value / Risk | Approvals Required | SLA Impact |
|---|---|---|---|
| Full ACAT (standard) | Under $500K | Operations analyst (self-review) + automated supervisory log | No added delay |
| Full ACAT (high-value) | $500K - $2M | Operations analyst + team lead review | Add 4 hours max |
| Full ACAT (very high value) | Over $2M | Operations analyst + team lead + operations manager | Add 8 hours max |
| Transfer to third-party account | Any value | Operations analyst + team lead + compliance review | Add 1 business day max |
| Transfer from client age 65+ | Over $100K | Operations analyst + team lead (senior investor protection review) | Add 4 hours max |
| Non-ACAT wire transfer | Over $50K | Operations analyst + team lead + verbal callback confirmation | Add 2 hours max |

Model the workflow as a state machine with states: Received, Validated, Pending Approval (Tier 1), Pending Approval (Tier 2), Pending Approval (Tier 3), Approved, Submitted to ACATS/Custodian, In Progress, Completed, Rejected. Guard conditions on each transition enforce the approval matrix — the system evaluates transfer value, transfer type, client age, and destination account ownership to determine which approval tiers are required.

Implement timeout escalation on each approval tier. If a Tier 1 approval (team lead) is not acted upon within 2 hours, send a reminder. If not acted upon within 4 hours, escalate to the operations manager for either direct approval or reassignment. These timeouts are calibrated to keep the total approval cycle within the FINRA Rule 11870 timelines.

For the compliance review tier (transfers to third-party accounts), the compliance analyst receives a structured review package: client identity verification, relationship between the client and the third-party recipient, source of the transfer instruction (client-initiated vs. advisor-initiated), and any recent account activity that may indicate exploitation or unauthorized transactions. The compliance review SLA is 1 business day, with escalation to the Chief Compliance Officer if the deadline is approaching.

The audit trail captures every approval decision: approver identity, timestamp, decision (approve/reject/request more information), and any comments or justification. This audit trail is the firm's evidence of supervisory review for FINRA Rule 3110 examination purposes.

## Example 2: Building SLA Monitoring for Account Maintenance Requests

**Scenario:** An RIA with $6 billion in AUM processes approximately 800 account maintenance requests per month, including name changes, address updates, beneficiary changes, account re-registrations, and fee schedule adjustments. The firm has no formal SLA tracking — requests are managed through a shared email inbox and a spreadsheet. Advisors frequently complain that requests "disappear" or take too long. The head of operations wants to implement SLA monitoring with real-time visibility for both operations staff and advisors.

**Design Considerations:**
- The firm uses Salesforce as its CRM and wants to leverage Salesforce's workflow capabilities rather than introducing a new platform.
- Different maintenance types have different complexity and urgency. A simple address change should complete in 1 business day. A trust re-registration may require 5-7 business days due to document collection and custodian processing.
- The firm custodies with two custodians (Schwab and Fidelity), and each custodian has different processing times and submission methods for maintenance requests.
- Advisors need visibility into request status without calling the operations team.

**Analysis:**

Step 1 — Define SLA targets per maintenance type:

| Maintenance Type | SLA Target | Rationale |
|---|---|---|
| Address change | 1 business day | Simple, no documentation required beyond client confirmation |
| Name change (marriage, divorce) | 3 business days | Requires supporting documents (marriage certificate, court order) and custodian processing |
| Beneficiary change | 2 business days | Requires signed beneficiary designation form; advisor review recommended |
| Account re-registration (individual to trust) | 5 business days | Requires trust documentation, custodian re-titling, cost basis continuity verification |
| Fee schedule adjustment | 2 business days | Requires advisor approval, billing system update, and confirmation |
| Account closure | 3 business days | Requires asset disposition (transfer or liquidation) and custodian close-out |

Step 2 — Build the workflow in Salesforce. Create a custom object (or use Salesforce Case) for maintenance requests. Each request captures: request type, requesting advisor, client account, date received, SLA deadline (auto-calculated from request type), assigned analyst, current status (Received, In Progress, Pending Documentation, Submitted to Custodian, Completed, Cancelled), and custodian.

Implement routing rules: requests are auto-assigned to the next available analyst using workload-based assignment. Complex request types (re-registrations, closures) are routed to senior analysts with the appropriate skill tag.

Step 3 — Implement SLA monitoring. Salesforce Process Builder (or Flow) evaluates each open request against its SLA deadline on a scheduled basis (every hour during business hours). The aging thresholds:
- Green: more than 50% of SLA remaining.
- Yellow: 20-50% of SLA remaining. The assigned analyst sees a yellow indicator on their dashboard.
- Red: less than 20% of SLA remaining. The team lead receives an automated notification.
- Breached: SLA exceeded. The operations manager receives a breach notification. The request is flagged for root cause documentation.

Step 4 — Advisor visibility. Build a Salesforce Experience Cloud portal (or a custom Lightning component accessible to advisors) that displays: all open requests for the advisor's clients, current status and assigned analyst, SLA deadline and color-coded aging indicator, and a comment thread for advisor-operations communication. This eliminates the need for advisors to email or call operations for status updates.

Step 5 — Management reporting. A weekly SLA dashboard displays: total requests received and completed, SLA compliance rate by maintenance type, average cycle time by maintenance type, breach count and root causes, and analyst-level throughput. The operations manager reviews the dashboard in the weekly team meeting and assigns process improvement actions for any maintenance type with SLA compliance below 90%.

## Example 3: Implementing Escalation Rules for Aging Corporate Action Elections

**Scenario:** A broker-dealer processes voluntary corporate action elections for approximately 4,000 client accounts. The firm has experienced two incidents in the past year where election deadlines were missed, resulting in clients receiving the default election on tender offers instead of their instructed election. In both cases, the root cause was a combination of late client notification and insufficient escalation when elections were not returned in time. The COO has mandated a formal escalation framework for corporate action elections.

**Design Considerations:**
- The election deadline chain runs: DTC deadline (hard deadline), custodian deadline (1 business day before DTC), firm internal deadline (2 business days before custodian), client notification (at least 5 business days before firm internal deadline).
- Election types vary in complexity: simple tender offers (tender or do not tender), mandatory with choice (cash or stock), complex events (Dutch auctions, exchange offers with multiple alternatives).
- The firm has 8 corporate actions analysts, a corporate actions manager, and a senior operations VP who oversees all processing.
- Some clients (particularly institutional accounts) require internal committee approval before submitting elections, adding time to the response cycle.

**Analysis:**

Define the escalation timeline working backward from the DTC deadline. Assume a typical tender offer with a DTC deadline of Day 0 (expressed as business days before the DTC deadline):

| Day (Before DTC Deadline) | Action | Owner |
|---|---|---|
| Day -10 | Event announced, validated, and set up in system. Client notification generated. | Corporate actions analyst |
| Day -9 | Notification sent to all affected clients and advisors via email and portal. | Automated |
| Day -5 | First follow-up to clients/advisors who have not responded. Yellow status assigned. | Automated notification, analyst monitors |
| Day -4 | Second follow-up with direct call to advisor for accounts above $100K in affected position. Team lead notified of non-responses. | Analyst (calls), automated (team lead alert) |
| Day -3 | Firm internal deadline. All received elections aggregated for submission. Non-respondents receive default election unless override is approved. | Corporate actions analyst + team lead review |
| Day -2.5 | Escalation to corporate actions manager for any account where the advisor disputes the default and requests a late election. Manager decides whether to attempt late submission. | Corporate actions manager |
| Day -2 | Elections submitted to custodian. | Corporate actions analyst |
| Day -1 | Custodian deadline. Confirm custodian has accepted the firm's election submission. Escalate to manager immediately if custodian rejects or flags any issues. | Corporate actions analyst + manager (if issues) |
| Day 0 | DTC deadline. Verify final settlement. Any issues escalated to senior VP. | Corporate actions manager + senior VP (if issues) |

Implement monitoring controls:
- A daily corporate actions dashboard shows all open voluntary events, the number of accounts requiring election, the response rate, and the days remaining until each deadline.
- Automated alerts fire at each escalation milestone. If the response rate is below 70% at Day -5, the team lead is alerted. If below 85% at Day -4, the corporate actions manager is alerted. If below 95% at Day -3 (firm internal deadline), the manager and senior VP are alerted.
- For institutional accounts requiring committee approval, the escalation timeline starts earlier — notification at Day -12 instead of Day -10 — to accommodate the approval process.

Post-event review: after each voluntary corporate action settles, the team logs the response rate, any elections that missed the internal deadline, whether late submissions were attempted and accepted, and any client impact from default elections. This data feeds a monthly review that identifies patterns (specific advisors who consistently respond late, event types that require longer lead times, clients who need proactive outreach) and drives process improvements.

Audit trail requirements: every notification, follow-up, escalation, and election submission is logged with timestamps and responsible parties. If a client later disputes that they received the default election, the firm can produce the complete communication and escalation history demonstrating that the client was notified, reminded, and escalated through the defined process. This audit trail satisfies FINRA Rule 3110 supervisory obligations and provides examination-ready documentation.

