# Incident Management: Severity, Response & Post-Mortem

Read this when triaging or coordinating a production incident, or defining the severity and response-time policy. Moved verbatim from `SKILL.md`.

## Manage Incidents

The agent follows the DETECT -> TRIAGE -> RESPOND -> RESOLVE -> REVIEW process:

**Severity levels:**

| Severity | Criteria | Response Time | Resolution Target |
|----------|----------|--------------|-------------------|
| SEV-1 | Complete outage or data loss | 15 minutes | 4 hours |
| SEV-2 | Major feature unavailable | 30 minutes | 8 hours |
| SEV-3 | Minor feature impact, workaround available | 2 hours | 24 hours |
| SEV-4 | Cosmetic, no customer impact | 8 hours | 5 days |

**Incident workflow:**
1. **Detect** -- Alert fires, monitoring triggers, user reports
2. **Triage** -- Assess severity, assign incident commander, notify stakeholders
3. **Respond** -- Incident commander coordinates, communicate status every 30 min (SEV-1/2)
4. **Resolve** -- Deploy fix, verify restoration, confirm with monitoring
5. **Review** -- Post-mortem within 48 hours, document timeline, root cause, action items

**Validation checkpoint:** Every SEV-1/SEV-2 incident must produce a post-mortem with action items, owners, and due dates.
