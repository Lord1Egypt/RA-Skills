# Operations & CX (OpenClaw Optimized)

This reference defines high-performance operations and customer experience workflows for AI agents in the OpenClaw environment, focusing on efficiency, quality, and proactive management.

## 1. Ticket Triage & Response

### The Autonomous Support Agent
- **Triage**: Automatically categorize incoming tickets (Bug, How-to, Feature Request, Billing, Security) using `read` on the ticket content.
- **Priority**: Assign priority (P1-P4) based on impact and breadth using the Triage Matrix.
- **Drafting**: Use `subagent spawn` with the "CX Specialist" persona to draft empathetic, direct, and specific responses using the **Response Structure**:
  1. Acknowledgment
  2. Core Message
  3. Next Steps
  4. Closing

---

## 2. Escalation Management

### Structured Escalation Workflow
- **Trigger**: Confirmed bug, SLA at risk, or high-value customer churn risk.
- **Action**: Generate an `ESCALATION_[ID].md` for Engineering or Product.
- **Requirements**: Must include **Reproduction Steps** (Start State, Specific Steps, Expected vs. Actual, Evidence).

---

## 3. Knowledge Base (KB) Management

### KB Hygiene & Expansion
- **Article Generation**: After every resolved P1/P2 ticket, the agent should propose a new KB article or update an existing one.
- **Templates**: Use standard formats for **How-to**, **Troubleshooting**, **FAQ**, and **Known Issue** articles.
- **Maintenance**: Use `heartbeat` to run a monthly "Stale Content Check" on the `kb/` directory.

---

## 4. Project & Portfolio Management

### Portfolio Health Monitoring
- **Health Dimensions**: Track Timeline, Budget, Scope, Quality, and Risk.
- **RAG Status**: Automatically update the `PORTFOLIO_STATUS.md` with Green/Amber/Red indicators.
- **Prioritization**: Use `exec` with Python to run WSJF or RICE models on the project portfolio.

---

## 5. File & Document Organization

### Workspace Optimization
- **Cleanup**: Use `exec` to find and move stale files (not accessed in 30 days) to an `archive/` folder.
- **Naming**: Enforce strict naming conventions: `[YYYY-MM-DD]_[Type]_[Description].[ext]`.
- **Invoices**: Use `read` and `write` to extract data from invoice files and append to a `FINANCE_TRACKER.csv`.

---

## 6. Operational Quality Assurance

### The "Iron Law" of Verification
Before completing any operational task, the agent must:
1. **Verify**: Run a final `read` or `exec` check to ensure the output matches the request.
2. **Document**: Record the action in the session log or a specific `LOG.md`.

---
*Derived from Perplexity Super-Skills & Claude Code. Optimized for OpenClaw by Ryder.*
