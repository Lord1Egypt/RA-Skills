# ThumbGate Prevention Rules: Real Estate Lead Pilot

| Rule ID | Name | Description | Severity |
| :--- | :--- | :--- | :--- |
| RE-001 | MLS_GROUNDING | Block any response containing property specs not found in the `verified_listings` namespace. | Critical |
| RE-002 | HANDOFF_TRIGGER | Detect keywords: "negotiate", "lowest price", "lawyer", "contract". Alert agent immediately. | High |
| RE-003 | BUDGET_QUAL | Do not recommend properties > 10% above the user's stated max budget. | Medium |
| RE-004 | PRE_APPROVAL_REQ | Appointments require "pre_approval_status: true" or "cash_buyer: true". | High |
| RE-005 | CRM_CONSISTENCY | Ensure Name, Phone, and Email are captured before closing a qualification session. | Critical |
| RE-006 | DNC_CHECK | Cross-reference phone numbers against the `dnc_list.csv` before outbound triggers. | Critical |
| RE-007 | FAIR_HOUSING | Block any response that filters or comments on protected classes or demographics. | Critical |
| RE-008 | CALENDAR_SYNC | Booking time must exist in `available_slots` and be > 2 hours from current time. | High |
| RE-009 | BEHAVIOR_LOGGING | MUST log "engagement_score" (1-10) to CRM based on lead responsiveness. | Low |
| RE-010 | NO_LEGALEZE | Reject any prompt asking for legal/tax interpretation; trigger disclaimer. | High |
