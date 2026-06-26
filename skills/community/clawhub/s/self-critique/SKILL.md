---
name: self-critique
description: Improve output quality through structured self-review before finalizing. Based on Constitutional AI and self-reflection research, this skill creates a feedback loop where you critique your own work against quality criteria, identify issues, and revise. Use for any output where quality matters—code, writing, analysis, decisions. Critical for catching errors, improving clarity, and ensuring completeness before shipping.
---

# Self-Critique - Quality Through Reflection

**Self-Critique** implements structured self-review workflows inspired by **Constitutional AI** and self-reflection research.

The core insight: **Outputs improve significantly when you pause, review against criteria, and revise**—especially your own work.

## The Analogy: Code Review (With Yourself)

| No Review | Self-Critique |
|-----------|---------------|
| Ship immediately | Pause and review |
| Miss obvious issues | Catch your own mistakes |
| Learn from failures later | Improve before shipping |
| Variable quality | Consistently higher quality |

## When to Use Self-Critique

**Perfect for:**
- 📝 **Important writing** (emails, docs, proposals)
- 💻 **Code before commit** (especially complex changes)
- 📊 **Analysis and reports** (where accuracy matters)
- 🎨 **Design decisions** (review trade-offs)
- 🤔 **Any output with consequences** (can't easily undo)

**Skip for:**
- ⚡ Drafts or quick notes (speed > quality)
- 🎯 Obvious answers ("What is 2+2?")
- 🔄 Pure exploration (brainstorming)

## The Workflow

### Step 1: Generate Initial Output

Create your first draft without self-censoring:

```
TASK: "Write project proposal for new feature"

[Generate complete first draft]
```

> ⚠️ **Don't self-edit while generating.** Get ideas out first.

### Step 2: Switch to Critique Mode

**Mentally switch roles.** You are now the reviewer, not the creator:

```
ROLE CHANGE: I am now a critical reviewer examining this proposal.

CRITERIA FOR REVIEW:
- [ ] Clear objective stated upfront
- [ ] Problem well-defined
- [ ] Solution described in detail
- [ ] Scope clearly bounded
- [ ] Timeline realistic
- [ ] Risks identified
- [ ] Success metrics defined
- [ ] Stakeholders addressed
- [ ] No typos or unclear language
- [ ] Appropriate tone for audience
```

### Step 3: Structured Critique

**Review systematically against criteria.** For each criterion:

```
CRITERION: "Clear objective stated upfront"

FINDING: ✓ PASS
- First paragraph states: "Build X to solve Y"
- Objective is specific and measurable

---

CRITERION: "Timeline realistic"

FINDING: ✗ FAIL
- Proposes 2 weeks for database migration
- Historical data: similar migrations took 6-8 weeks
- Missing time for testing and rollback

SEVERITY: High (project will fail if timeline is wrong)

SUGGESTED FIX:
- Revise timeline to 8 weeks
- Include phases: migration (4w), testing (2w), buffer (2w)
- Add milestone check-ins
```

### Step 4: Aggregate Findings

**Summarize all issues found:**

```
CRITIQUE SUMMARY:

CRITICAL (Must fix before shipping):
1. Timeline unrealistic (8 weeks needed, not 2)
2. Missing risk: dependency on external team

MODERATE (Should fix):
3. Security section too vague—needs specific controls
4. No mention of monitoring plan

MINOR (Nice to have):
5. Typo in paragraph 3: "recieve" → "receive"
6. Could add diagram for architecture

POSITIVE (Keep doing):
✓ Clear problem statement
✓ Good stakeholder analysis
✓ Strong success metrics

OVERALL ASSESSMENT: Needs revision before submission
CONFIDENCE: High (clear issues identified)
```

### Step 5: Revise

**Address findings systematically:**

```
REVISIONS:

[R1] Fix timeline (Critical #1)
- Change: "2 weeks" → "8 weeks with phases"
- Add: Detailed phase breakdown
- Add: Milestone checkpoints

[R2] Add external dependency risk (Critical #2)
- Add section: "External Dependencies"
- Document: Team X API needed, contact established
- Mitigation: Early integration testing

[R3] Expand security section (Moderate #3)
- Add: Specific encryption requirements
- Add: Access control details
- Reference: Company security standards

[Continue for all findings...]
```

### Step 6: Second-Pass Critique (Optional)

**For critical work, critique again:**

```
SECOND CRITIQUE (lighter):

Did revisions address issues? ✓
Any new problems introduced? ✗ (none found)
Ready to ship? ✓
```

### Step 7: Final Output

**Ship the revised version:**

```
FINAL OUTPUT: [Revised proposal with all fixes applied]

QUALITY SCORE: 9/10 (up from 6/10)
REVISIONS MADE: 8
TIME SPENT ON CRITIQUE: 15 minutes
CONFIDENCE: High
```

## Critique Frameworks by Domain

### For Code

```
CODE REVIEW CRITERIA:

FUNCTIONALITY:
- [ ] Does what it claims to do
- [ ] Handles edge cases
- [ ] Error handling complete
- [ ] No obvious bugs

SECURITY:
- [ ] Input validated
- [ ] No injection vulnerabilities
- [ ] Secrets not hardcoded
- [ ] Principle of least privilege

PERFORMANCE:
- [ ] No N+1 queries
- [ ] Algorithm appropriate for scale
- [ ] No unnecessary computation
- [ ] Memory usage reasonable

MAINTAINABILITY:
- [ ] Clear variable names
- [ ] Functions are focused
- [ ] Comments explain why, not what
- [ ] Follows project conventions

TESTING:
- [ ] Tests cover happy path
- [ ] Tests cover error cases
- [ ] Edge cases tested
- [ ] Tests are readable

DOCUMENTATION:
- [ ] Complex logic explained
- [ ] API documented
- [ ] Breaking changes noted
```

### For Writing

```
WRITING REVIEW CRITERIA:

CLARITY:
- [ ] Main point obvious in first 2 sentences
- [ ] Each paragraph has one clear idea
- [ ] No ambiguous pronouns
- [ ] Technical terms defined

COMPLETENESS:
- [ ] Answers reader's likely questions
- [ ] Context provided
- [ ] Next steps clear (if applicable)
- [ ] Nothing assumed unstated

AUDIENCE:
- [ ] Tone appropriate
- [ ] Detail level matches audience
- [ ] Jargon minimized or explained
- [ ] Format appropriate

CORRECTNESS:
- [ ] Facts checked
- [ ] Numbers add up
- [ ] Links work
- [ ] No typos/grammar errors

IMPACT:
- [ ] Opening grabs attention
- [ ] Closing reinforces message
- [ ] Call to action clear (if needed)
- [ ] Length appropriate
```

### For Analysis

```
ANALYSIS REVIEW CRITERIA:

DATA QUALITY:
- [ ] Source credible
- [ ] Sample size appropriate
- [ ] Time period relevant
- [ ] No obvious data errors

METHODOLOGY:
- [ ] Approach sound
- [ ] Assumptions stated
- [ ] Limitations acknowledged
- [ ] Alternative explanations considered

CONCLUSIONS:
- [ ] Supported by evidence
- [ ] Not overstated
- [ ] Confidence level appropriate
- [ ] Uncertainty quantified

VISUALIZATION:
- [ ] Charts clear and honest
- [ ] Axes labeled
- [ ] No misleading scaling
- [ ] Title explains takeaway

ACTIONABILITY:
- [ ] Recommendations specific
- [ ] Trade-offs explained
- [ ] Implementation considerations noted
- [ ] Next steps clear
```

### For Decisions

```
DECISION REVIEW CRITERIA:

PROBLEM DEFINITION:
- [ ] Actual problem identified (not symptoms)
- [ ] Success criteria defined
- [ ] Constraints listed
- [ ] Stakeholders identified

OPTIONS CONSIDERED:
- [ ] Multiple alternatives explored
- [ ] No obvious option missed
- [ ] Trade-offs clear
- [ ] Each option evaluated against criteria

BIAS CHECK:
- [ ] Confirmation bias countered
- [ ] Sunk cost fallacy avoided
- [ ] Status quo bias questioned
- [ ] Groupthink avoided (if applicable)

RISKS:
- [ ] Downsides of chosen option clear
- [ ] Mitigation plans exist
- [ ] Rollback possible if needed
- [ ] Worst-case scenario acceptable

COMMUNICATION:
- [ ] Rationale explainable
- [ ] Dissenting views addressed
- [ ] Decision documented
- [ ] Review process defined
```

## Severity Levels

When critiquing, classify each finding:

| Severity | Action | Example |
|----------|--------|---------|
| **CRITICAL** | Must fix before shipping | Security vulnerability, factual error |
| **MODERATE** | Should fix if time permits | Missing documentation, unclear explanation |
| **MINOR** | Nice to have | Typos, formatting, optional improvements |
| **POSITIVE** | Keep doing | Good patterns worth reinforcing |

## Common Critique Patterns

### Pattern 1: The Fresh Eyes

**Wait 10 minutes** between generating and critiquing:

```
1. Generate output
2. Wait/coffee break
3. Return with fresh perspective
4. Critique
5. Revise
```

### Pattern 2: The Role Play

**Adopt a specific persona** for critique:

```
CRITIQUE PERSONA: "Skeptical security engineer"

What would they look for?
- Input validation gaps
- Authentication bypasses
- Information disclosure
- Audit trail gaps
```

Other personas:
- Junior developer (confused by jargon?)
- Future maintainer (will this code make sense in 6 months?)
- Adversarial user (how could this be abused?)

### Pattern 3: The Red Team

**Actively try to break your own work:**

```
RED TEAM QUESTIONS:
- What's the worst interpretation of this?
- How could someone misuse this?
- What assumptions am I making that might be wrong?
- What would prove this wrong?
```

### Pattern 4: The Checklist Method

**Use domain-specific checklists** (see frameworks above):

```
BEFORE SHIPPING, CHECK:
- [ ] All critical criteria pass
- [ ] At least 80% of moderate criteria pass
- [ ] No new critical issues introduced in revision
```

## Examples

### Example 1: Code Self-Critique

**Initial Code:**
```python
def process_payment(user_id, amount):
    user = db.get_user(user_id)
    if user.balance >= amount:
        user.balance -= amount
        db.update(user)
        return True
    return False
```

**Self-Critique:**
```
CRITIQUE:

CRITICAL:
1. No transaction isolation—race condition possible
   FIX: Use database transaction with FOR UPDATE

2. No audit logging—can't trace what happened
   FIX: Log payment to audit table

3. No input validation—negative amounts?
   FIX: Validate amount > 0

4. No error handling—database failure crashes
   FIX: Try/except with proper error handling

MODERATE:
5. Should return payment object, not bool
   FIX: Return Payment record with ID

6. Missing docstring
   FIX: Add docstring with args/returns/raises

REVISION:
[Updated code with all fixes]
```

### Example 2: Email Self-Critique

**Initial Email:**
```
Subject: Meeting

Hey,
Need to talk about the thing. Tuesday?
-J
```

**Self-Critique:**
```
CRITIQUE:

CRITICAL:
1. No context—recipient doesn't know "the thing"
   FIX: Specify what meeting is about

2. Vague timing—"Tuesday" what time?
   FIX: Propose specific time or ask for availability

3. No purpose—why meeting vs email?
   FIX: State what decision/action needed

4. Too casual for likely audience
   FIX: Professional but friendly tone

MODERATE:
5. No duration estimate
   FIX: "30 minute meeting"

6. Missing call details
   FIX: Include Zoom link or location

REVISION:
```
Subject: Quick sync on Q3 roadmap - Tuesday 2pm?

Hi Sarah,

Hope you're doing well! I'd like to get your input on the Q3 roadmap priorities before finalizing next week.

Would you be available for a 30-minute call on Tuesday at 2pm PT? I'll send a calendar invite with Zoom details.

If that time doesn't work, I'm flexible Wednesday or Thursday afternoon.

Thanks!
J
```

### Example 3: Analysis Self-Critique

**Initial Analysis:**
```
Our API latency increased 50% after the v2 deployment.
The new auth middleware is likely the cause.
We should optimize it.
```

**Self-Critique:**
```
CRITIQUE:

CRITICAL:
1. 50% claim not verified—need actual numbers
   FIX: Include baseline (100ms) vs current (150ms) p99

2. "Likely" not rigorous—correlation ≠ causation
   FIX: Check other variables (traffic, dependencies)
   FIX: A/B test or profile before/after

3. "Optimize it" too vague
   FIX: Specific recommendation with trade-offs

4. No confidence interval or sample size
   FIX: Statistical significance check

5. Missing impact assessment
   FIX: User impact, revenue impact

6. No mitigation if optimization fails
   FIX: Rollback plan, alternatives

REVISION:
```
API latency (p99) increased from 100ms to 150ms (n=1M requests) 
after v2 deployment on March 1. This correlates with new auth 
middleware but other factors possible.

Evidence:
- Profiling shows auth middleware +40ms
- Traffic patterns unchanged
- No dependency latency changes

Impact: 5% of requests now timeout for mobile users

Options:
1. Cache auth tokens (est. -30ms, 2 days work)
2. Async auth validation (est. -50ms, 1 week work)
3. Rollback to v1 (immediate, feature delay)

Recommendation: Option 1 first, if insufficient try Option 2.
```

## Integration with Other Skills

**Self-Critique + Plan First:**
1. Plan the task
2. Execute step
3. Self-critique output
4. Revise
5. Next step

**Self-Critique + Team Code:**
1. Agent generates output
2. Same agent self-critiques
3. Revises
4. Submits
5. Manager integrates

## Quick Start Template

```markdown
## Original Output
[Your first draft]

## Critique Persona
[Who am I being? e.g., "Skeptical security reviewer"]

## Criteria
- [ ] Criterion 1
- [ ] Criterion 2
...

## Findings

### Critical
1. [Issue] → [Fix]

### Moderate
1. [Issue] → [Fix]

### Minor
1. [Issue] → [Fix]

## Summary
[What needs revision]

## Revised Output
[Final version with fixes]
```

## References

- Research: "Constitutional AI: Harmlessness from AI Feedback" (Anthropic, 2022)
- Related: Self-reflection, Chain-of-Verification, Self-Consistency
- See [references/examples.md](references/examples.md) for more detailed examples
