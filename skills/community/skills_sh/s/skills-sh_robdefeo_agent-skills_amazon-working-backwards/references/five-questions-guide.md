# The 5 Questions — Deep Guide

## Table of Contents

1. [Question 1: Who is the customer?](#q1)
2. [Question 2: What is the customer problem or opportunity?](#q2)
3. [Question 3: What is the most important customer benefit?](#q3)
4. [Question 4: How do we know what the customer needs or wants?](#q4)
5. [Question 5: What does the customer experience look like?](#q5)
6. [Verification checklist](#verification)

---

## Q1: Who is the customer? {#q1}

### What a strong answer looks like

- Name a **specific** persona, not a broad category. "Engineering managers at Series B+ startups with 10-50 engineers" beats "developers."
- If there are multiple customer segments, identify the **primary** customer — the one whose problem you solve first.
- Include relevant context: role, company size, industry, technical sophistication, budget authority.

### Common pitfalls

- **Too broad**: "Everyone" or "businesses" — no product is for everyone.
- **Confusing buyer and user**: The person who pays may differ from the person who uses. Name both if relevant, but clarify who is primary.
- **Internal-only framing**: "Our sales team" is valid for internal tools, but clarify that it is an internal customer.

### Probing questions to strengthen

- "If you could only sell to ONE type of customer for the first year, who would it be?"
- "What is this customer doing today to solve the problem?"
- "Why is this customer underserved by existing solutions?"

---

## Q2: What is the customer problem or opportunity? {#q2}

### What a strong answer looks like

- State the problem **from the customer's perspective**, not the builder's.
- Quantify the pain: time wasted, money lost, error rates, missed opportunities.
- Explain why the problem exists NOW — what changed (market shift, regulation, technology)?

### Common pitfalls

- **Solution masquerading as problem**: "The customer needs a dashboard" is a solution. The problem is "The customer cannot see which campaigns are underperforming until the monthly report."
- **Trivial problem**: If the customer wouldn't pay money or change behavior to solve it, it's not worth building.
- **Builder's problem, not customer's**: "We need more revenue" is YOUR problem, not the customer's.

### Probing questions to strengthen

- "What happens if the customer does nothing? How bad does it get?"
- "How much time/money does this problem cost the customer per week/month/year?"
- "Can you describe a specific moment when a real customer experienced this pain?"

---

## Q3: What is the most important customer benefit? {#q3}

### What a strong answer looks like

- ONE benefit, stated clearly. Not a feature list.
- Framed as an outcome: "Reduce time-to-deploy from 2 hours to 5 minutes" rather than "Automated CI/CD pipeline."
- The benefit must directly address the problem from Q2.
- Quantify where possible (time saved, error reduction, revenue gained).

### Common pitfalls

- **Feature list instead of benefit**: "Supports SSO, RBAC, and audit logs" — these are features. The benefit is "Meets enterprise security requirements out of the box so customers don't need a 3-month compliance project."
- **Multiple benefits**: If you can't pick one, you haven't identified the core value.
- **Benefit doesn't map to problem**: If Q2 says "customers lose deals due to slow proposals" but Q3 says "beautiful formatting," there's a disconnect.

### Probing questions to strengthen

- "If the customer could only get ONE thing from this, what would make them stay?"
- "How would you measure whether this benefit was delivered?"
- "Would the customer describe the benefit the same way you do?"

---

## Q4: How do we know what the customer needs or wants? {#q4}

### What a strong answer looks like

- Cite **specific evidence**: customer interviews, support tickets, usage data, market research, competitor analysis, survey results.
- Distinguish between what customers SAY they want and what they DO (revealed vs. stated preferences).
- Include both qualitative and quantitative signals when available.

### Common pitfalls

- **"We just know"**: Intuition without validation is a red flag at Amazon.
- **Only anecdotal**: "One customer told me..." — how representative is that?
- **Circular reasoning**: "We know they need it because we're building it."
- **Outdated evidence**: Research from 2 years ago may not reflect current needs.

### Probing questions to strengthen

- "How many customers have you spoken to about this? What did they say?"
- "What data do you have that supports this? Usage metrics? Support volume?"
- "What would DISPROVE this hypothesis? Have you looked for that evidence?"

---

## Q5: What does the customer experience look like? {#q5}

### What a strong answer looks like

- Walk through the experience **step by step** as the customer would live it.
- Start from the moment the customer discovers or encounters the product.
- Be concrete: name the screens, the actions, the outcomes at each step.
- Describe the "before and after" — how the experience compares to what the customer does today.

### Common pitfalls

- **Architecture description, not experience**: "The service uses a microservices architecture with event-driven..." — the customer does not care.
- **Happy path only**: What happens when something goes wrong? How does the customer recover?
- **Too abstract**: "The customer has a seamless experience" says nothing. Describe what they SEE and DO.

### Probing questions to strengthen

- "Walk me through a typical Tuesday for this customer — when do they first interact with this?"
- "What is the very first thing the customer does? What do they see?"
- "What would make the customer say 'wow' vs. 'meh'?"

---

## Verification Checklist {#verification}

Use this checklist to verify a complete set of 5Q answers:

### Coherence
- [ ] Q3 (benefit) directly solves Q2 (problem)
- [ ] Q5 (experience) delivers Q3 (benefit) to Q1 (customer)
- [ ] Q4 (evidence) supports Q2 (problem) and Q3 (benefit)

### Specificity
- [ ] Q1 names a specific persona, not a broad category
- [ ] Q2 quantifies the pain or opportunity
- [ ] Q3 states ONE measurable benefit
- [ ] Q4 cites concrete evidence sources
- [ ] Q5 describes step-by-step actions, not abstractions

### Customer obsession
- [ ] Every answer is written from the customer's perspective
- [ ] No solution-first thinking (problem before solution)
- [ ] The experience (Q5) would genuinely delight the customer

### Intellectual honesty
- [ ] Q4 evidence is current and representative
- [ ] Assumptions are called out as assumptions
- [ ] Known risks or gaps are acknowledged
