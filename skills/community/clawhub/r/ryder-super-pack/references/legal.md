# Legal (OpenClaw Optimized)

This reference defines high-performance legal operations for AI agents in the OpenClaw environment, prioritizing risk management and structured communication.

## 1. Contract Review & NDA Triage

### The Ryder Review Protocol
1. **Classification**: Use `read` to ingest the contract. Classify as **GREEN** (Standard), **YELLOW** (Negotiate), or **RED** (Escalate).
2. **Clause Check**: Systematically check for:
   - **Limitation of Liability**: Are caps mutual and reasonable?
   - **Indemnification**: Are there overbroad carveouts?
   - **Data Protection**: Is a DPA (Data Processing Agreement) included?
3. **Redline Generation**: Create a `REDLINES_[CONTRACT].md` with:
   - **Current Language**: The original text.
   - **Proposed Change**: The optimized Ryder version.
   - **Rationale**: Why this change is necessary.

---

## 2. Compliance & Privacy (GPDR/CCPA)

### Automated DSR (Data Subject Request) Handling
- **Intake**: Monitor for DSRs via `heartbeat` or manual trigger.
- **Verification**: Use `web_search` to verify regulatory deadlines (e.g., 72 hours for GDPR breach).
- **Fulfillment**: 
  1. **Search**: Use `grep` or `memory_search` to find all personal data related to the requester in the workspace.
  2. **Package**: Use `write` to create a `DSR_RESPONSE_[ID].md`.
  3. **Log**: Update a `COMPLIANCE_LOG.md` with the request status.

---

## 3. Risk Assessment & Escalation

### Severity × Likelihood Matrix
Before any major action (e.g., a new integration or public post), the agent should run a risk assessment:
- **Severity (1-5)**: Financial, operational, and reputational impact.
- **Likelihood (1-5)**: Probability of occurrence.
- **Output**: A `RISK_ASSESSMENT.md` with a clear "Go/No-Go" recommendation.

---

## 4. Legal Writing & Communications

### Canned Responses (Ryder Style)
- **Litigation Holds**: Use `write` to generate a `LEGAL_HOLD_[MATTER].md` for distribution.
- **NDA Transmittals**: Use the "Legal Ops" persona via `subagent spawn` to draft professional, firm, yet polite cover letters for standard NDAs.
- **Subpoena Intake**: Automatically flag any incoming subpoena for immediate human review.

---

## 5. Meeting Briefings & Action Tracking

### The "Counsel's Brief"
- **Pre-Meeting**: Use `web_search` and `read` to summarize the background of all external participants.
- **Post-Meeting**: Use `write` to create a `MEETING_MINUTES.md` with a clear "Action Items" table (Owner, Deadline, Status).

---
*Derived from Perplexity Super-Skills & Claude Code. Optimized for OpenClaw by Ryder.*
