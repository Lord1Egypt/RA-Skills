# Entry Examples

Concrete examples of well-formatted support entries with all fields.

## Learning: Misdiagnosis of Network Issue

```markdown
## [LRN-20250415-001] misdiagnosis

**Logged**: 2025-04-15T10:30:00Z
**Priority**: high
**Status**: pending
**Area**: diagnosis

### Summary
502 Bad Gateway errors misdiagnosed as server-side when root cause was customer's WAF blocking API callbacks

### Details
Three separate agents investigated 502 errors reported by customers on webhook
delivery. Each spent 2+ hours checking our infrastructure (load balancers, API
gateway, upstream services) before discovering the customer's Web Application
Firewall was blocking outbound requests from our IP ranges. No KB article
existed for this common scenario.

### Resolution Steps

**What happened:**
Agent checked our server logs, restarted API gateway, and escalated to
infrastructure team. Infrastructure confirmed all systems healthy. After
2.5 hours, agent asked customer about their firewall — root cause found.

**What should have happened:**
After confirming our infrastructure is healthy (5-minute check), immediately
ask about customer's network configuration: WAF rules, firewall whitelist,
proxy settings.

### Suggested Action
Create KB article: "502 Bad Gateway on Webhooks — Check Customer WAF First".
Add to triage checklist: for 502 errors on callbacks, always check customer
network config before investigating our infrastructure.

### Metadata
- Source: repeat_ticket
- Channel: email
- Product Area: integrations
- Customer Tier: professional
- Related Tickets: TKT-44821, TKT-44956, TKT-45102
- Tags: 502, webhook, WAF, firewall, misdiagnosis
- Pattern-Key: misdiagnosis.502_customer_waf
- Recurrence-Count: 3
- First-Seen: 2025-03-20
- Last-Seen: 2025-04-15

---
```

## Ticket Issue: SLA Breach on P1 Ticket

```markdown
## [TKT-20250416-001] sla_breach_p1_database

**Logged**: 2025-04-16T09:15:00Z
**Priority**: critical
**Status**: pending
**Area**: escalation

### Summary
P1 SLA breached because database deadlock ticket was escalated to general engineering instead of DBA on-call

### Ticket Timeline
| Time | Event |
|------|-------|
| T+0h | Enterprise customer reports complete application freeze |
| T+15m | First response sent (within SLA) |
| T+30m | Agent diagnoses database connection pool exhaustion |
| T+45m | Escalated to general engineering team |
| T+2h | General engineering cannot reproduce; re-routes to DBA team |
| T+3h | DBA identifies deadlock on high-contention table |
| T+3.5h | Deadlock resolved, application restored |
| T+4h | Ticket closed — **P1 resolution SLA (2h) breached** |

### Root Cause
Escalation went to the general engineering queue instead of directly to the
DBA on-call. The 1.5-hour routing delay caused the P1 SLA breach. The agent
correctly diagnosed database issues but did not know the DBA team has a
separate escalation path.

### Correct Approach
For database-related P1 tickets (connection pool, deadlock, replication lag):
escalate directly to DBA on-call via PagerDuty, not general engineering.

### Customer Impact
- SLA Status: breached (resolution — 3.5h vs 2h target)
- CSAT Impact: significant (customer mentioned "unacceptable downtime")
- Reopened: no
- Escalated: yes (general engineering → DBA team)

### Prevention
Update escalation matrix: database issues (keywords: deadlock, connection pool,
replication, slow query) → DBA on-call directly. Add to agent training material.

### Context
- Trigger: sla_breach
- Channel: portal
- Product Area: infrastructure
- Customer Tier: enterprise

### Metadata
- Related Tickets: TKT-44500
- Related Files: runbooks/database-escalation.md
- See Also: TKT-20250320-003

---
```

## Learning: Knowledge Gap on New Feature

```markdown
## [LRN-20250417-001] knowledge_gap

**Logged**: 2025-04-17T14:00:00Z
**Priority**: medium
**Status**: pending
**Area**: documentation

### Summary
No KB article exists for the new bulk import API released two weeks ago; four agents researched from scratch

### Details
The bulk import API (v2.3) was released on April 3rd. Since then, four different
agents have received tickets about rate limits, file format requirements, and
error codes for this endpoint. Each agent had to read the engineering docs and
API changelog to answer customer questions, averaging 45 minutes per ticket for
what should be a 10-minute resolution with a KB article.

### Resolution Steps

**What happened:**
Each agent independently searched KB, found nothing, then consulted internal
Slack channels and API docs. Customers waited 4-6 hours for responses.

**What should have happened:**
A KB article should have been created as part of the feature release process,
covering: supported file formats, rate limits, error codes, and example requests.

### Suggested Action
Create KB article for bulk import API. Add to feature release checklist:
"Support KB article created and reviewed before GA."

### Metadata
- Source: kb_search_miss
- Channel: email
- Product Area: api
- Customer Tier: professional
- Related Tickets: TKT-45200, TKT-45215, TKT-45230, TKT-45248
- Tags: knowledge-gap, bulk-import, api, documentation, release-process

---
```

## Ticket Issue: Repeat Ticket for Password Reset

```markdown
## [TKT-20250418-001] repeat_password_reset

**Logged**: 2025-04-18T11:00:00Z
**Priority**: medium
**Status**: pending
**Area**: resolution

### Summary
Same customer opened 3 tickets in 2 weeks for password reset failures; root cause was cached SAML certificate not addressed on first ticket

### Ticket Timeline
| Time | Event |
|------|-------|
| Apr 4 | Ticket #1: Customer cannot log in via SSO. Agent resets password manually. |
| Apr 10 | Ticket #2: Same customer, same issue. Different agent resets password again. |
| Apr 18 | Ticket #3: Customer frustrated ("This is the third time"). Agent investigates deeper. |
| Apr 18 +2h | Root cause found: customer's IdP has expired SAML certificate cached in our system. |
| Apr 18 +3h | SAML certificate refreshed in admin panel. Issue permanently resolved. |

### Root Cause
First two agents treated the symptom (reset password) instead of investigating
why SSO login kept failing. The expired SAML certificate was the actual root cause
and should have been checked on the first ticket.

### Correct Approach
For SSO login failures, check SAML certificate validity and IdP configuration
before resorting to password reset. Password reset is a workaround, not a fix.

### Customer Impact
- SLA Status: met (each individual ticket)
- CSAT Impact: significant (customer used phrase "unacceptable recurring issue")
- Reopened: no (new tickets each time)
- Escalated: no

### Prevention
Add to SSO troubleshooting tree: "Check SAML certificate expiry before
password reset. If cert expired, guide customer to refresh via IdP admin."
Flag repeat tickets from same customer for agent attention.

### Context
- Trigger: repeat_ticket
- Channel: portal
- Product Area: auth
- Customer Tier: enterprise

### Metadata
- Related Tickets: TKT-44300, TKT-44580, TKT-45100
- See Also: LRN-20250410-002

---
```

## Learning: Escalation Failure

```markdown
## [LRN-20250419-001] escalation_gap

**Logged**: 2025-04-19T16:30:00Z
**Priority**: high
**Status**: pending
**Area**: escalation

### Summary
Critical billing integration bug escalated to API team instead of billing team; 8-hour delay in resolution

### Details
Customer reported double-charges on their account. Agent correctly identified
it as a billing API issue but escalated to the general API team. The API team
investigated for 6 hours before realising it was a Stripe webhook processing
bug owned by the billing team. After re-routing, billing team fixed it in
30 minutes.

### Resolution Steps

**What happened:**
Agent saw "API" in the error and routed to API team. No escalation matrix
entry distinguishes billing API issues from general API issues.

**What should have happened:**
Any ticket involving payments, charges, invoices, or refunds should route to
the billing team regardless of which API endpoint is involved.

### Suggested Action
Update escalation matrix: tickets with keywords (charge, invoice, payment,
refund, subscription, billing) → Billing team, not general API team.

### Metadata
- Source: escalation_failure
- Channel: chat
- Product Area: billing
- Customer Tier: professional
- Related Tickets: TKT-45300
- Tags: escalation, billing, routing, double-charge, stripe
- Pattern-Key: escalation.billing_vs_api

---
```

## Feature Request: Auto-Categorization for Ticket Triage

```markdown
## [FEAT-20250420-001] auto_categorize_tickets

**Logged**: 2025-04-20T09:00:00Z
**Priority**: medium
**Status**: pending
**Area**: triage

### Requested Capability
Automatic ticket categorization based on subject line and first message content,
reducing manual triage time and improving routing accuracy.

### User Context
Agents spend 3-5 minutes per ticket on initial triage (reading, categorizing,
assigning priority, routing). With 200+ tickets/day, that's 10-17 hours of
agent time on triage alone. Misrouting causes an average 2-hour delay in resolution.

### Complexity Estimate
complex

### Suggested Implementation
1. Train classifier on historical ticket data (subject + body → category + priority)
2. Integrate with Zendesk/Intercom API to auto-set fields on ticket creation
3. Display confidence score; auto-assign above 90%, flag for human review below
4. Keywords → team routing map for high-confidence escalation paths
5. Feedback loop: agents correct misclassifications to improve model

### Metadata
- Frequency: recurring
- Related Features: SLA timer automation, escalation matrix

---
```

## Learning: Promoted to KB Article

```markdown
## [LRN-20250410-003] knowledge_gap

**Logged**: 2025-04-10T11:00:00Z
**Priority**: high
**Status**: promoted
**Promoted**: KB article (support.example.com/articles/rate-limit-troubleshooting)
**Area**: documentation

### Summary
No documentation for API rate limit error codes; 12 tickets in one week asking about 429 responses

### Details
After API rate limiting was tightened in v2.2, 12 customers opened tickets
about 429 Too Many Requests errors. No KB article explained the new limits,
how to check current usage, or how to request a limit increase. Each agent
spent 20-30 minutes composing a custom response.

### Suggested Action
KB article created covering: rate limit tiers by plan, how to check current
usage via dashboard, how to read X-RateLimit headers, and how to request
an increase. Canned response template also created for quick replies.

### Metadata
- Source: kb_search_miss
- Channel: email
- Product Area: api
- Related Tickets: TKT-44100 through TKT-44112
- Tags: rate-limit, 429, api, documentation, knowledge-gap
- Recurrence-Count: 12
- First-Seen: 2025-04-03
- Last-Seen: 2025-04-10

---
```

## Learning: Promoted to Skill

```markdown
## [LRN-20250412-001] misdiagnosis

**Logged**: 2025-04-12T15:00:00Z
**Priority**: high
**Status**: promoted_to_skill
**Skill-Path**: skills/502-gateway-diagnosis
**Area**: diagnosis

### Summary
Systematic approach to diagnosing 502 Bad Gateway errors on customer webhook endpoints

### Details
Developed a repeatable diagnostic workflow after encountering 6 separate
misdiagnoses of 502 errors over 2 months. The pattern is consistent:
agents investigate our infrastructure first when the root cause is almost
always on the customer's side (WAF, firewall, SSL, DNS).

### Suggested Action
Follow the diagnostic workflow:
1. Confirm our services are healthy (status page, internal monitoring)
2. Check webhook delivery logs for the specific endpoint
3. Ask customer about WAF/firewall rules, IP whitelisting
4. Check customer's SSL certificate chain
5. Verify DNS resolution for the endpoint from our infrastructure

### Metadata
- Source: repeat_ticket
- Channel: email
- Product Area: integrations
- Related Tickets: multiple
- Tags: 502, webhook, diagnosis, misdiagnosis, playbook
- See Also: LRN-20250415-001, TKT-20250320-002, TKT-20250401-005

---
```
