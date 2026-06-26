---
name: react-loop
description: Solve complex problems by interleaving reasoning with actions. Based on the ReAct research, this skill alternates between thinking (reasoning about the situation) and acting (using tools or taking steps), then observing results to inform next steps. Use for multi-step problems requiring tool use, information gathering, or situations where the path forward only becomes clear through exploration. Critical for research, debugging, data analysis, and tool-heavy workflows.
---

# ReAct Loop - Reason, Act, Observe

**ReAct Loop** implements the **ReAct** (Reason + Act) paradigm for solving complex problems through iterative exploration.

The core insight: **Alternating between reasoning and action produces better results than either alone**—reasoning guides which actions to take, and observations from actions inform better reasoning.

## The Analogy: Detective Investigation

| Just Thinking | Just Acting | ReAct Loop |
|--------------|-------------|------------|
| Theorize without evidence | Randomly collect evidence | Form hypothesis → Test → Update |
| Miss key clues | Waste time on irrelevant leads | Systematic, evidence-driven |
| Paralysis by analysis | Spray and pray | Balanced exploration |

## When to Use ReAct Loop

**Perfect for:**
- 🔍 **Research questions** (gather info from multiple sources)
- 🐛 **Debugging** (hypothesize cause → test → observe)
- 📊 **Data exploration** (query → analyze → decide next query)
- 🌐 **Web/API tasks** (fetch data → process → fetch more)
- 🛠️ **Tool-using workflows** (sequence of tool calls needed)
- 🧩 **Problems where you "don't know what you don't know"**

**Skip for:**
- ✅ Direct questions with known answers
- 📝 Single-step tasks ("write a summary")
- 🎯 Problems with clear predetermined steps

## The ReAct Pattern

```
┌─────────────────────────────────────────────────────────┐
│  LOOP: Repeat until solved or max iterations reached   │
│                                                          │
│  Step 1: REASON (Thought)                               │
│  "Based on what I know, I need to..."                   │
│           ↓                                              │
│  Step 2: ACT (Action)                                   │
│  [Use tool, run query, fetch data, execute code]        │
│           ↓                                              │
│  Step 3: OBSERVE (Observation)                          │
│  [Result, output, data, error]                          │
│           ↓                                              │
│  Return to Step 1 with new information                │
└─────────────────────────────────────────────────────────┘
```

## The Workflow

### Step 1: Initial Reasoning

**Assess what you know and what you need:**

```
THOUGHT 1: 
I need to find why the API is slow. I know:
- Latency increased on March 15
- It's the /search endpoint specifically
- Database CPU is normal

What I don't know:
- Is it the search algorithm or data layer?
- What changed on March 15?
- Is it all queries or specific ones?

Next action: Check git log for March 15 changes to search endpoint
```

### Step 2: Take Action

**Execute the decided action:**

```
ACTION 1:
Run: git log --since="2024-03-14" --until="2024-03-16" --oneline -- api/search/
```

### Step 3: Observe Results

**Record what happened:**

```
OBSERVATION 1:
abc1234 Add fuzzy matching to search

def5678 Update search ranking algorithm

ghi9012 Increase search result limit from 10 to 100
```

### Step 4: Iterate - Next Reasoning

**Update understanding, decide next step:**

```
THOUGHT 2:
Three changes on March 15:
1. Fuzzy matching added
2. Ranking algorithm changed  
3. Result limit increased 10x

The result limit increase (10→100) is suspicious—could cause:
- More database queries
- More serialization
- More network transfer

I should check if the latency correlates with result size.

Next action: Query logs for response size vs latency correlation
```

### Step 5: Next Action

```
ACTION 2:
Run: analyze_logs --endpoint=/search --metric=response_size --since=2024-03-14
```

### Step 6: Next Observation

```
OBSERVATION 2:
Average response size: 
- March 14: 45KB
- March 15: 420KB
- March 16: 415KB

Latency correlation with response size: r=0.89 (strong)
```

### Step 7: Continue Iterating...

```
THOUGHT 3:
Strong correlation found! Response size increased 10x, latency spiked.
The result limit change (ghi9012) is likely the culprit.

But I should verify the fuzzy matching isn't also slow.
Let me check query execution time for search with and without fuzzy matching.

ACTION 3:
Run: benchmark_search --fuzzy=on --fuzzy=off --iterations=100

OBSERVATION 3:
Without fuzzy: 45ms avg
With fuzzy: 52ms avg (15% increase)

Not significant compared to response size impact.
```

### Step 8: Conclude

```
THOUGHT 4:
Root cause identified: Increasing result limit from 10 to 100 items 
caused 10x response size increase, which correlates strongly with 
latency increase.

Recommendation: 
1. Revert result limit to 10 (quick fix)
2. Implement pagination for clients who need more results (proper fix)

FINAL ANSWER: The latency spike was caused by commit ghi9012 which 
increased search result limit from 10 to 100. This increased response 
size 10x. Revert or implement pagination.
```

## ReAct Format

Standard format for tracking:

```markdown
## ReAct Session: [Task Description]

### Iteration 1

**Thought 1:**
[Reasoning about current state and what to do next]

**Action 1:**
[Specific action taken]

**Observation 1:**
[Result of action]

---

### Iteration 2

**Thought 2:**
[Updated reasoning based on observation 1]

**Action 2:**
[Next action]

**Observation 2:**
[Result]

---

[Continue until solved...]

### Final Answer
[Conclusion based on accumulated observations]
```

## Common Action Types

### Information Gathering

```
ACTION: Search web for "Python async best practices 2024"
ACTION: Query database: SELECT * FROM users WHERE last_login > NOW() - INTERVAL '7 days'
ACTION: Read file: src/auth/middleware.py
ACTION: Fetch API: GET https://api.github.com/repos/owner/repo/issues
```

### Execution

```
ACTION: Run Python script to analyze log file
ACTION: Execute SQL migration
ACTION: Run tests: pytest tests/test_feature.py -v
ACTION: Deploy to staging
```

### Calculation/Processing

```
ACTION: Calculate correlation between variables X and Y
ACTION: Transform data: normalize column values
ACTION: Aggregate: sum revenue by month
```

### Communication

```
ACTION: Send email to team with findings
ACTION: Post message to Slack channel
ACTION: Create GitHub issue
```

## Best Practices

### 1. Thoughts Should Guide Actions

❌ **Bad:** Action without reasoning
```
ACTION: Check logs
```

✅ **Good:** Reasoning explains why
```
THOUGHT: The error happens intermittently. Let me check if it's 
correlated with specific times or traffic patterns.

ACTION: Query error logs grouped by hour for past 7 days
```

### 2. Be Specific in Actions

❌ **Vague:**
```
ACTION: Look into the database
```

✅ **Specific:**
```
ACTION: Run: SELECT COUNT(*) FROM orders WHERE status = 'pending' 
AND created_at < NOW() - INTERVAL '1 day'
```

### 3. Record Full Observations

❌ **Partial:**
```
OBSERVATION: Some errors found
```

✅ **Complete:**
```
OBSERVATION: 23 errors in past 24 hours, all from IP 203.0.113.42,
all occurring between 02:00-04:00 UTC, all with message 
"Connection timeout"
```

### 4. Update Understanding Each Iteration

```
THOUGHT 1: Suspect database issue
[Action, Observation]

THOUGHT 2: Database is healthy. Error is network-related. 
Suspect DNS resolution.
[Next action]
```

### 5. Know When to Stop

**Stop when:**
- ✅ Question is answered
- ✅ Problem is solved
- ✅ Sufficient information gathered
- ❌ Not making progress (stuck in loop)
- ❌ Hitting iteration limits

**If stuck:** Try different angle, ask for help, or escalate.

## Examples

### Example 1: Research Task

**Task:** "What's the best approach for real-time notifications in a React app?"

```markdown
## ReAct Session: Research React real-time notifications

### Iteration 1

**Thought 1:**
I need to understand current options for real-time notifications in React.
Common approaches: WebSockets, Server-Sent Events (SSE), polling.
Let me search for current best practices.

**Action 1:**
Search web: "React real-time notifications best practices 2024"

**Observation 1:**
Results mention:
- WebSockets (Socket.io) - bidirectional, good for chat
- SSE - unidirectional, simpler, auto-reconnect
- Long polling - fallback, less efficient
- Web Push API - for offline notifications

### Iteration 2

**Thought 2:**
Multiple options exist. Decision depends on:
1. Do we need bidirectional communication?
2. Do we need offline notifications?
3. Browser support requirements?

Let me check if we need bidirectional (can client send to server?)

**Action 2:**
Check requirements doc: "Does client need to send real-time data to server?"

**Observation 2:**
Requirements: "User actions should update in real-time for other users"
This implies bidirectional: client sends action → server broadcasts to others

### Iteration 3

**Thought 3:**
Bidirectional requirement suggests WebSockets. But let me verify SSE 
couldn't work with separate HTTP endpoints for client-to-server.

**Action 3:**
Search: "WebSockets vs SSE for notifications bidirectional"

**Observation 3:**
- SSE: Client→Server via HTTP POST, Server→Client via SSE
- WebSockets: Both directions over same connection
- Hybrid approach: SSE for broadcast, HTTP for client actions

Trade-offs:
- WebSockets: More complex, firewall issues, but single connection
- SSE+HTTP: Simpler, better HTTP infrastructure support

### Iteration 4

**Thought 4:**
Need to check if infrastructure handles WebSockets. Also need offline 
notifications which requires Service Workers + Web Push.

**Action 4:**
Check: "Does current infrastructure support WebSockets?"

**Observation 4:**
Infrastructure: Load balancer (Nginx) supports WebSocket upgrade.
Current stack: Node.js with Socket.io already used for chat feature.

### Iteration 5

**Thought 5:**
We already use Socket.io for chat, so WebSocket infrastructure exists.
For notifications, we can:
1. Extend existing Socket.io for in-app notifications
2. Add Web Push API for offline notifications

This reuses existing infrastructure.

**Action 5:**
Search: "Socket.io vs Web Push API for React notifications"

**Observation 5:**
Best practice: Use Socket.io for in-app (real-time when app open),
Web Push for when app closed/offline. They're complementary.

### Final Answer

Recommended approach:
1. **In-app real-time:** Extend existing Socket.io infrastructure
   - Reuses current chat setup
   - Handles reconnection, fallbacks automatically
   
2. **Offline notifications:** Implement Web Push API
   - Requires Service Worker
   - Browser notification permission
   - Works even when app closed

Implementation order:
1. Phase 1: Socket.io for in-app (2 weeks)
2. Phase 2: Web Push for offline (add 1 week)

Rationale: Infrastructure already supports WebSockets, requirement 
is bidirectional, hybrid approach gives best UX.
```

### Example 2: Debugging

**Task:** "Fix failing CI build"

```markdown
## ReAct Session: Debug CI build failure

### Iteration 1

**Thought 1:**
Build started failing yesterday. Need to identify what's failing and why.
Let me check the latest build logs.

**Action 1:**
Check: Last CI build logs (GitHub Actions)

**Observation 1:**
Build fails at "Run tests" step:
```
Error: Cannot find module '../config/database'
Require stack:
- /app/tests/setup.js
```

### Iteration 2

**Thought 2:**
Test setup can't find database config. This could be:
1. File was deleted/moved
2. Path changed in test
3. Config not generated in CI environment

Let me check if the file exists in repo.

**Action 2:**
Check: Does config/database.js exist in repository?

**Observation 2:**
File exists: config/database.js
But error shows it's looking for '../config/database' from tests/setup.js

Path resolution issue. Let me check directory structure.

### Iteration 3

**Thought 3:**
Path is '../config/database' from tests/setup.js.
This should resolve to config/database.js if tests/ is sibling to config/.

Let me check actual directory structure.

**Action 3:**
Run: find . -name "setup.js" -o -name "database.js" | head -20

**Observation 3:**
```
./src/config/database.js
./tests/setup.js
```

Ah! config is under src/, not at root. Path should be '../src/config/database'

### Iteration 4

**Thought 4:**
Path in test is wrong. But why did it work before?
Either:
1. File was moved recently
2. Test was changed
3. Working directory changed

Let me check git history.

**Action 4:**
Run: git log --oneline -10 -- tests/setup.js src/config/

**Observation 4:**
```
abc1234 Move config to src/ (yesterday)
def5678 Update test dependencies
```

Config was moved yesterday, test path not updated.

### Iteration 5

**Thought 5:**
Root cause identified: Commit abc1234 moved config to src/ but didn't 
update tests/setup.js require path.

Fix: Update require path from '../config/database' to '../src/config/database'

**Action 5:**
Edit: tests/setup.js - change require path

**Observation 5:**
Fixed line 3: `const dbConfig = require('../src/config/database')`

### Iteration 6

**Thought 6:**
Fix applied. Let me verify by running tests locally.

**Action 6:**
Run: npm test

**Observation 6:**
Tests pass locally.

### Final Answer

**Root cause:** Config directory moved to src/ in commit abc1234, but 
tests/setup.js still referenced old path.

**Fix:** Updated require path in tests/setup.js from '../config/database' 
to '../src/config/database'

**Prevention:** Add CI check for broken requires, or use path aliases.
```

### Example 3: Data Analysis

**Task:** "Why did conversion rate drop last week?"

```markdown
## ReAct Session: Analyze conversion rate drop

### Iteration 1

**Thought 1:**
Conversion rate dropped last week. Need to understand:
1. When exactly did it drop?
2. Is it specific to traffic source, device, or user segment?
3. What changed around that time?

Let me start with overall trend.

**Action 1:**
Query: Conversion rate by day for past 14 days

**Observation 1:**
- Week of Feb 1-7: 3.2% avg
- Week of Feb 8-14: 3.1% avg
- Week of Feb 15-21: 2.1% avg ⬅️ Drop here
- Feb 22+: 2.0% avg

Drop started Feb 15, sustained since.

### Iteration 2

**Thought 2:**
Drop started Feb 15. Let me check what changed that day:
- New deployment?
- Marketing campaign started?
- External event?

**Action 2:**
Check: Deployments on Feb 15

**Observation 2:**
Deploy at 10:00 AM: "New checkout flow, A/B test enabled"
Deploy at 2:00 PM: "Hotfix: Fix validation error"

Two deployments that day. The checkout flow change is suspicious.

### Iteration 3

**Thought 3:**
Checkout flow changed Feb 15. Let me check if conversion drop 
correlates with the new flow specifically.

**Action 3:**
Query: Conversion rate by A/B test variant

**Observation 3:**
- Control (old flow): 3.2% conversion
- Variant B (new flow): 1.8% conversion

New flow has much lower conversion. A/B test should have caught this.

### Iteration 4

**Thought 4:**
Why was this deployed if A/B test showed lower conversion? 
Maybe it wasn't significant in the test, or test was misconfigured.

Let me check A/B test results.

**Action 4:**
Check: A/B test configuration and results

**Observation 4:**
A/B test configured:
- Duration: 7 days
- Sample: 10% of traffic
- Result: "No significant difference" (p=0.12)

But the 10% sample might have been too small to detect the drop.

### Iteration 5

**Thought 5:**
Test said "no significant difference" but full rollout shows 40% drop.
Let me check if the test was properly configured—maybe traffic wasn't 
randomized, or checkout isn't where the drop is happening.

**Action 5:**
Query: Funnel analysis for new vs old checkout flow

**Observation 5:**
Old flow funnel:
- Visit checkout: 100%
- Enter shipping: 85%
- Enter payment: 70%
- Complete: 32%

New flow funnel:
- Visit checkout: 100%
- Enter shipping: 75% ⬅️ Big drop
- Enter payment: 60%
- Complete: 18%

Drop is at shipping info step. Something about new shipping form.

### Iteration 6

**Thought 6:**
Drop is at shipping info step. Let me check what changed in the 
shipping form specifically.

**Action 6:**
Check: UI changes to shipping form (Feb 15 deploy)

**Observation 6:**
From PR diff:
- Added "Phone number" field (required)
- Changed "ZIP code" from text to number input
- Added address validation

Phone number is required? Let me check error rates.

### Iteration 7

**Thought 7:**
New required phone number field. This could be causing users to 
abandon if they don't want to provide it, or if it's not clear why 
it's needed.

Let me check abandonment at shipping step.

**Action 7:**
Query: Cart abandonment rate at shipping step

**Observation 7:**
Before Feb 15: 15% abandonment at shipping
After Feb 15: 25% abandonment at shipping

10 percentage point increase in abandonment.

### Iteration 8

**Thought 8:**
Phone number requirement is likely causing abandonment. But let me 
verify by checking if users who complete shipping have lower conversion 
to purchase (which would indicate payment step issues).

**Action 8:**
Query: Conversion rate from shipping complete to purchase

**Observation 8:**
- Old flow: 37% of users who enter shipping complete purchase
- New flow: 24% of users who enter shipping complete purchase

Also lower! So two issues:
1. More abandonment at shipping (phone requirement)
2. Lower conversion among those who continue (payment step?)

### Final Answer

**Conversion dropped 40% due to two issues in Feb 15 checkout redesign:**

1. **10% more abandonment at shipping step**
   - Root cause: New required phone number field
   - Users reluctant to provide or confused why needed

2. **13% lower conversion after shipping**
   - Root cause: ZIP code changed to number input
   - International users with letters can't enter (e.g., UK: "SW1A 1AA")
   - Validation errors cause drop-off

**Recommendations:**
1. Revert to old checkout flow immediately
2. Redesign: Make phone optional, fix ZIP validation
3. Increase A/B test sample size for future changes
4. Monitor funnel step-by-step, not just final conversion
```

## Integration with Other Skills

**ReAct + Plan First:**
- Plan First: Create initial plan
- ReAct Loop: Execute each step with reasoning-observation cycles

**ReAct + Self-Critique:**
- ReAct Loop: Execute and observe
- Self-Critique: Review if reasoning path is sound

**ReAct + Team Code:**
- ReAct Loop: Manager uses to coordinate (reason → delegate → observe)
- Team Code: Multiple agents working in parallel

## Anti-Patterns to Avoid

### 1. Actions Without Reasoning

❌ **Bad:**
```
ACTION: Check logs
ACTION: Run query
```

✅ **Good:**
```
THOUGHT: Error is intermittent. Let me check if it correlates with time.
ACTION: Query error logs by hour
```

### 2. Ignoring Observations

❌ **Bad:**
```
OBSERVATION: Error rate is 0%
THOUGHT: Must be database issue
```

✅ **Good:**
```
OBSERVATION: Error rate is 0%
THOUGHT: If error rate is 0%, this isn't a widespread issue. 
Let me check if it's specific to one user or one scenario.
```

### 3. Getting Stuck in Loops

❌ **Bad:**
```
THOUGHT 1: Check database
[Action, Observation: DB healthy]

THOUGHT 2: Maybe database is slow?
[Same action again]
```

✅ **Good:**
```
THOUGHT 1: Check database
[Action, Observation: DB healthy]

THOUGHT 2: Database is healthy. Issue must be elsewhere. 
Let me check application layer.
```

### 4. Stopping Too Early

❌ **Bad:**
```
Found one possible cause. Done.
```

✅ **Good:**
```
Found likely cause. Let me verify:
1. Does it explain all symptoms?
2. Is there evidence to support it?
3. Are there alternative explanations?

[Verify, then conclude]
```

## Quick Start Template

```markdown
## ReAct Session: [Task]

### Iteration 1

**Thought 1:**
[What I know, what I need, what to do first]

**Action 1:**
[Specific action]

**Observation 1:**
[Result]

---

### Iteration 2

**Thought 2:**
[Updated understanding, next step]

**Action 2:**
[Next action]

**Observation 2:**
[Result]

---

[Continue...]

### Final Answer
[Conclusion]
```

## References

- Research: "ReAct: Synergizing Reasoning and Acting in Language Models" (Yao et al., 2022)
- Related: Chain-of-Thought, ToolFormer, WebGPT
- See [references/examples.md](references/examples.md) for detailed examples
