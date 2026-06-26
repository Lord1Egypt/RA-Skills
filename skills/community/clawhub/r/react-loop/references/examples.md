# ReAct Loop - Detailed Examples

## Example 1: Multi-Step API Integration

**Task:** "Integrate Stripe payment and handle all edge cases"

```markdown
## ReAct Session: Stripe payment integration

### Iteration 1

**Thought 1:**
I need to integrate Stripe for payments. I know the basic flow:
1. Create payment intent on server
2. Client confirms payment
3. Webhook confirms success

But I need to understand:
- What API version to use?
- How to handle failed payments?
- What webhooks to listen for?
- How to handle idempotency?

Let me start by checking Stripe docs for the recommended approach.

**Action 1:**
Search: "Stripe payment intent integration best practices 2024"

**Observation 1:**
Stripe recommends:
- Payment Intents API (not legacy Charges)
- Server-side payment intent creation
- Client-side confirmation with Elements
- Webhook payment_intent.succeeded for fulfillment
- Idempotency key for retry safety

### Iteration 2

**Thought 2:**
Good, Payment Intents is the modern approach. Now I need to:
1. Set up Stripe SDK
2. Create endpoint to create payment intent
3. Add webhook handler
4. Handle various failure cases

Let me check what specific webhook events I need.

**Action 2:**
Search: "Stripe payment intent webhook events required"

**Observation 2:**
Required events:
- payment_intent.succeeded - payment complete
- payment_intent.payment_failed - payment failed
- payment_intent.canceled - user canceled
- payment_intent.requires_action - 3D Secure needed

Also need to handle:
- Insufficient funds
- Card declined
- Expired card

### Iteration 3

**Thought 3:**
I have the events. Now let me understand the flow better. I should 
check if there are specific error codes I need to handle.

**Action 3:**
Search: "Stripe card decline error codes complete list"

**Observation 3:**
Common decline codes:
- insufficient_funds
- card_declined (generic)
- expired_card
- incorrect_cvc
- processing_error
- issuer_not_available

Each needs different user messaging.

### Iteration 4

**Thought 4:**
Now I have enough to start implementing. Let me create the server-side 
endpoint first.

**Action 4:**
Write code: Create /api/create-payment-intent endpoint

**Observation 4:**
Code created:
```python
@app.route('/api/create-payment-intent', methods=['POST'])
def create_payment():
    try:
        data = request.get_json()
        intent = stripe.PaymentIntent.create(
            amount=data['amount'],
            currency='usd',
            automatic_payment_methods={'enabled': True},
            idempotency_key=data.get('idempotency_key')
        )
        return jsonify(client_secret=intent.client_secret)
    except stripe.error.StripeError as e:
        return jsonify(error=str(e)), 400
```

### Iteration 5

**Thought 5:**
Basic endpoint created. Now I need webhook handler. This is critical 
for production - can't rely on client-side confirmation alone.

**Action 5:**
Write code: Webhook handler for payment_intent.succeeded

**Observation 5:**
Webhook handler created with signature verification.

But I realize I need to handle webhook retries safely - should be 
idempotent.

### Iteration 6

**Thought 6:**
Webhook needs to be idempotent - if Stripe retries, I shouldn't 
fulfill the order twice. Let me check how to implement this.

**Action 6:**
Search: "Stripe webhook idempotency prevent duplicate fulfillment"

**Observation 6:**
Best practice:
- Store payment_intent.id with order
- Check if already processed before fulfilling
- Return 200 even if already processed (so Stripe stops retrying)

### Iteration 7

**Thought 7:**
Need to update webhook to check for existing order. Let me also add 
proper error handling for the different decline codes.

**Action 7:**
Update code: Add idempotency check and decline code handling

**Observation 7:**
Updated webhook:
```python
@app.route('/webhook', methods=['POST'])
def webhook():
    event = stripe.Webhook.construct_event(
        payload, sig_header, webhook_secret
    )
    
    if event['type'] == 'payment_intent.succeeded':
        intent = event['data']['object']
        
        # Idempotency check
        if Order.exists(payment_intent_id=intent['id']):
            return '', 200  # Already processed
        
        # Create order
        Order.create_from_payment_intent(intent)
    
    return '', 200
```

### Iteration 8

**Thought 8:**
Core integration done. Let me verify by checking test mode behavior 
and ensure I handle the client-side properly too.

**Action 8:**
Test: Create test payment intent and verify webhook received

**Observation 8:**
Test successful:
- Payment intent created
- Webhook received
- Order created
- Idempotency working (retry didn't create duplicate)

### Iteration 9

**Thought 9:**
Server-side working. Now need client-side error handling to show 
appropriate messages for different decline codes.

**Action 9:**
Write code: Client-side error message mapping

**Observation 9:**
Client code created with error mapping:
```javascript
const errorMessages = {
  'insufficient_funds': 'Your card has insufficient funds.',
  'expired_card': 'Your card has expired.',
  'incorrect_cvc': 'Your card security code is incorrect.',
  'card_declined': 'Your card was declined.',
  'default': 'Payment failed. Please try again.'
};
```

### Final Answer

Stripe integration complete with:

1. **Server-side:**
   - Payment intent creation endpoint
   - Webhook handler with signature verification
   - Idempotent fulfillment (prevents duplicates)
   - Proper error handling

2. **Client-side:**
   - Payment confirmation with Elements
   - Error message mapping for decline codes
   - Loading states

3. **Edge cases handled:**
   - Webhook retries (idempotent)
   - Card declines (specific messages)
   - Network failures (retry with idempotency key)
   - 3D Secure (automatically handled by Stripe.js)

4. **Security:**
   - Webhook signature verification
   - Client secret only, not raw card data
   - HTTPS required

Testing: Use Stripe test cards for different scenarios.
```

---

## Example 2: Research and Synthesis

**Task:** "Should we migrate from REST to GraphQL?"

```markdown
## ReAct Session: Evaluate GraphQL migration

### Iteration 1

**Thought 1:**
Need to evaluate if GraphQL migration makes sense. Current state:
- REST API with 50 endpoints
- Mobile and web clients
- Some performance issues with over-fetching

Need to research:
- When is GraphQL worth it?
- Migration cost estimate
- Performance benefits
- Team learning curve

**Action 1:**
Search: "GraphQL vs REST when to migrate case studies"

**Observation 1:**
Key findings:
- GraphQL shines with multiple clients needing different data
- Over-fetching/under-fetching is main pain point it solves
- Migration cost is high (months, not weeks)
- Team needs training on new paradigm
- Tooling is more complex

### Iteration 2

**Thought 2:**
We have multiple clients (web, mobile) and over-fetching issues. 
Let me check our current API usage to quantify the problem.

**Action 2:**
Query: API response sizes by endpoint for mobile client

**Observation 2:**
Mobile client:
- /api/user: Returns 50 fields, uses 5 (90% waste)
- /api/dashboard: Returns 100KB, uses 20KB (80% waste)
- Multiple round trips to compose dashboard view

Clear over-fetching problem.

### Iteration 3

**Thought 3:**
Over-fetching confirmed. But what's the actual user impact? Let me 
check if this causes performance issues.

**Action 3:**
Query: Mobile app load times and user complaints

**Observation 3:**
- Dashboard load: 4.2 seconds average
- User complaints: "app is slow" increased 40% in past 6 months
- Data transfer: 2MB per session (expensive on mobile data)

Pain point is real.

### Iteration 4

**Thought 4:**
Problem is real, but migration is expensive. Let me look for 
alternatives. Could we solve this without full GraphQL migration?

**Action 4:**
Search: "REST over-fetching solutions without GraphQL"

**Observation 4:**
Alternatives:
- BFF pattern (Backend for Frontend)
- Query parameters to select fields (?fields=name,email)
- Request batching
- Partial response (Google API style)

These are lighter weight but less flexible.

### Iteration 5

**Thought 5:**
Alternatives exist but GraphQL is more comprehensive. Let me estimate 
migration cost more precisely.

**Action 5:**
Calculate: Rough effort estimate for GraphQL migration

**Observation 5:**
Estimate:
- Schema design: 2 weeks
- Resolver implementation: 6 weeks
- Client migration: 8 weeks
- Testing/bug fixes: 4 weeks
- Total: 20 weeks (5 months)

Plus ongoing: more complex caching, monitoring, tooling.

### Iteration 6

**Thought 6:**
5 months is significant. Let me check if there are specific GraphQL 
features we actually need vs just solving over-fetching.

**Action 6:**
List: Which GraphQL features would we use?

**Observation 6:**
Features we need:
- ✅ Query specific fields (solves over-fetching)
- ✅ Nested queries (reduce round trips)
- ✅ Single endpoint (simpler client code)

Features we don't need:
- ❌ Mutations (our REST mutations work fine)
- ❌ Subscriptions (no real-time features needed)
- ❌ Fragments (not complex enough)

### Iteration 7

**Thought 7:**
We only need ~30% of GraphQL features. Let me check if a BFF pattern 
would give us 80% of benefits for 20% of effort.

**Action 7:**
Search: "BFF pattern vs GraphQL mobile optimization"

**Observation 7:**
BFF findings:
- Can optimize specifically for mobile needs
- Keeps REST for other clients
- 2-3 weeks effort vs 5 months
- Easier to maintain
- Less complexity

Trade-off: Web client still has over-fetching.

### Iteration 8

**Thought 8:**
BFF is much cheaper but only solves mobile. Let me check current 
web client impact.

**Action 8:**
Query: Web client API usage and performance

**Observation 8:**
Web client:
- Better network conditions (less impact)
- Uses Next.js with caching
- Load time: 1.8 seconds (acceptable)
- Data waste: 40% (less than mobile)

Web is less urgent.

### Iteration 9

**Thought 9:**
Interesting. Mobile is the pain point, web is okay. BFF for mobile 
might be the pragmatic choice. But let me verify team capacity.

**Action 9:**
Check: Team availability and current priorities

**Observation 9:**
- Team: 3 backend engineers
- Current sprint: Committed to feature work
- No bandwidth for 5-month migration
- Could spare 1 engineer for 3 weeks

### Final Answer

**Recommendation: Implement BFF for mobile, defer full GraphQL migration**

**Rationale:**

1. **Problem identified:** Mobile has severe over-fetching (80% waste)
2. **Impact quantified:** 4.2s load time, user complaints up 40%
3. **GraphQL cost too high:** 5 months, team can't afford now
4. **BFF alternative:** Solves mobile problem in 3 weeks with 1 engineer
5. **Web acceptable:** Less urgent, can revisit later

**Implementation:**
- Phase 1: Mobile BFF (3 weeks)
- Phase 2: Monitor impact
- Phase 3: Re-evaluate GraphQL for web in 6 months

**Success metrics:**
- Mobile load time: 4.2s → 2s
- Data transfer: -50%
- User complaints: trend down
```

---

## Example 3: Debugging Complex Issue

**Task:** "Memory leak in production Node.js app"

```markdown
## ReAct Session: Debug Node.js memory leak

### Iteration 1

**Thought 1:**
Production app has memory leak. Symptoms:
- Memory grows over time
- Eventually crashes with OOM
- Restart temporarily fixes

Need to:
1. Confirm it's actually a leak (vs high baseline)
2. Find what's leaking
3. Find root cause
4. Fix and verify

Let me start with memory metrics.

**Action 1:**
Check: Memory usage graphs for past 7 days

**Observation 1:**
- March 1: 512MB baseline
- March 7: 1.2GB (crashed)
- Pattern: Steady growth, not spikes
- Restarts: Every 2-3 days now (was weekly)

Confirmed leak - memory not stabilizing.

### Iteration 2

**Thought 2:**
Steady growth suggests accumulated objects. Need heap snapshot to 
see what's growing. Let me check if we can capture heap dump.

**Action 2:**
Check: Can we enable heap dumps in production?

**Observation 2:**
Yes, can enable --heapsnapshot-near-heap-limit flag.
But need to be careful - snapshots are large (hundreds of MB).

Let me try local reproduction first.

### Iteration 3

**Thought 3:**
Try to reproduce locally. Need to understand what triggers the leak.
Let me check recent code changes around when leak started.

**Action 3:**
Check: Git commits around March 1 (when growth started)

**Observation 3:**
Commits March 1-3:
- "Add image processing for thumbnails"
- "Update file upload handling"
- "Add caching for user sessions"

Image processing is suspicious - might not be releasing buffers.

### Iteration 4

**Thought 4:**
Image processing added March 1. Let me check the implementation 
for memory issues.

**Action 4:**
Review code: Image thumbnail processing

**Observation 4:**
```javascript
async function createThumbnail(imagePath) {
  const buffer = fs.readFileSync(imagePath);  // 🚨 Sync!
  const processed = await sharp(buffer)
    .resize(200, 200)
    .toBuffer();
  return processed;
}
```

Issues found:
1. readFileSync - blocking, but also buffer never released?
2. No try/catch - if sharp fails, buffer might not GC?

But this shouldn't cause accumulation unless called repeatedly.

### Iteration 5

**Thought 5:**
Code has issues but not obvious leak. Let me check how often this 
is called and if there's a caching issue.

**Action 5:**
Check: Image processing endpoint usage

**Observation 5:**
- Endpoint called 50,000 times/day
- Each call processes image
- No caching of processed images
- Images range 1-10MB

Wait - if we're processing 50K images/day and keeping references...

### Iteration 6

**Thought 6:**
Let me check if there's a cache or event listener holding references.
Check the user session caching commit too.

**Action 6:**
Review code: User session caching (other March 1 commit)

**Observation 6:**
```javascript
const sessionCache = new Map();

function cacheSession(userId, session) {
  sessionCache.set(userId, session);
  // ❌ No TTL, no cleanup
}
```

Cache grows forever. This is likely the leak.

### Iteration 7

**Thought 7:**
Found it! Session cache has no cleanup. Each user session added 
stays forever. Let me verify this is the main issue.

**Action 7:**
Query: Number of unique user sessions in cache

**Observation 7:**
Session cache size: 180,000 entries
Each session object: ~5KB estimated
Total: ~900MB

This matches the memory growth pattern!

### Iteration 8

**Thought 8:**
Session cache is the leak. Now I need to:
1. Confirm by checking if growth correlates with user count
2. Fix by adding TTL/cleanup
3. Test fix
4. Deploy

Let me check correlation.

**Action 8:**
Query: Daily active users vs memory growth

**Observation 8:**
Correlation coefficient: 0.94 (very strong)
Each new DAU adds ~5KB to memory
Memory = 500MB + (DAU * 5KB)

Confirmed: Session cache is the leak.

### Iteration 9

**Thought 9:**
Root cause confirmed. Now fix. Options:
1. Add TTL to cache entries
2. Use LRU cache with max size
3. Switch to Redis

Redis is best long-term but TTL is quick fix. Let's do TTL now.

**Action 9:**
Fix code: Add TTL to session cache

**Observation 9:**
```javascript
const sessionCache = new Map();
const TTL = 24 * 60 * 60 * 1000; // 24 hours

function cacheSession(userId, session) {
  sessionCache.set(userId, {
    data: session,
    timestamp: Date.now()
  });
}

// Cleanup old entries periodically
setInterval(() => {
  const now = Date.now();
  for (const [key, value] of sessionCache) {
    if (now - value.timestamp > TTL) {
      sessionCache.delete(key);
    }
  }
}, 60 * 60 * 1000); // hourly cleanup
```

### Iteration 10

**Thought 10:**
Fix implemented. Let me test locally to verify memory stabilizes.

**Action 10:**
Test: Simulate user sessions, verify memory doesn't grow unbounded

**Observation 10:**
Test results:
- 0-1000 sessions: Memory grows to 50MB
- 1000-5000 sessions: Memory stable at 55MB (old sessions cleaned)
- 5000-10000 sessions: Memory stable at 58MB

Fix verified - memory stabilizes.

### Final Answer

**Root Cause:**
Session cache added March 3 has no TTL or cleanup. Each user session 
stored indefinitely. With 180K active users, cache consumed 900MB.

**Fix:**
Added 24-hour TTL with hourly cleanup. Memory now stabilizes.

**Deployment Plan:**
1. Deploy fix (blue-green deployment)
2. Monitor memory for 24 hours
3. If stable, remove old heap dump flags
4. Schedule Redis migration for long-term solution

**Prevention:**
- Code review checklist: "Does cache have cleanup?"
- Lint rule: Flag unbounded Maps used as caches
- Monitoring alert: Memory growth > 20%/day
```

---

## Example 4: Data Investigation

**Task:** "Why did conversion rate drop on Tuesdays?"

```markdown
## ReAct Session: Investigate Tuesday conversion drop

### Iteration 1

**Thought 1:**
Report says conversion rate drops specifically on Tuesdays. Need to:
1. Verify this is real (not noise)
2. Find what's different about Tuesdays
3. Identify root cause
4. Propose fix

Let me start by checking the data.

**Action 1:**
Query: Conversion rate by day of week (past 90 days)

**Observation 1:**
Day of week | Conversion
Mon | 3.1%
Tue | 2.4% ⬅️ Lower
Wed | 3.0%
Thu | 3.2%
Fri | 3.3%
Sat | 2.8%
Sun | 2.9%

Tuesday is 23% lower than average. Pattern is consistent.

### Iteration 2

**Thought 2:**
Confirmed - Tuesday is consistently lower. What could be different 
about Tuesdays? Let me check traffic sources.

**Action 2:**
Query: Conversion by day and traffic source

**Observation 2:**
All sources lower on Tuesday:
- Organic: 3.2% → 2.5%
- Paid: 3.0% → 2.3%
- Email: 4.1% → 3.2%

Not source-specific. Something about the product experience on Tuesdays?

### Iteration 3

**Thought 3:**
All sources affected. Could be:
1. Site performance issues on Tuesdays?
2. Tuesday-specific content/promotions?
3. User behavior differences?
4. Technical issues (deploys, maintenance)?

Let me check site performance.

**Action 3:**
Query: Page load times by day of week

**Observation 3:**
Page load times:
Mon: 1.2s
Tue: 2.8s ⬅️ Slower
Wed: 1.3s

Tuesday is 2x slower! This explains conversion drop.

### Iteration 4

**Thought 4:**
Tuesday has 2x slower page load. What's causing this? Let me check 
what happens on Tuesdays specifically.

**Action 4:**
Check: Scheduled jobs, cron tasks, reports on Tuesdays

**Observation 4:**
Tuesday schedule:
- 02:00: Database backup
- 06:00: Weekly analytics report generation
- 09:00: Full-text search index rebuild
- 14:00: Marketing email send (2M emails)

Multiple heavy jobs on Tuesdays!

### Iteration 5

**Thought 5:**
Heavy Tuesday schedule likely causing resource contention. Let me check 
database performance during these times.

**Action 5:**
Query: Database CPU and query latency on Tuesdays

**Observation 5:**
Tuesday 09:00-12:00:
- DB CPU: 95% (vs 40% other days)
- Query latency: 450ms avg (vs 80ms other days)
- Search queries timing out

Full-text index rebuild is crushing the database.

### Iteration 6

**Thought 6:**
Index rebuild during business hours (9am) is causing performance 
degradation. This is scheduled poorly. Let me verify by checking 
if conversion drop matches the timing.

**Action 6:**
Query: Hourly conversion rate on Tuesdays

**Observation 6:**
Tuesday conversion by hour:
- 00-06: 3.1% (normal)
- 06-09: 2.9% (slight drop)
- 09-12: 1.8% ⬅️ Severe drop
- 12-14: 2.5% (recovering)
- 14-18: 2.3% (email send impact)

Drop exactly matches index rebuild window (09:00-12:00).

### Iteration 7

**Thought 7:**
Found it! Index rebuild 9am-12pm on Tuesdays causing site slowdown, 
which causes conversion drop. Solution: Move to off-hours.

But wait - why was this scheduled for Tuesday 9am? Let me check if 
there's a reason.

**Action 7:**
Check: Who scheduled this and why?

**Observation 7:**
Index rebuild scheduled by previous team. Comment: "Tuesday morning 
so results are fresh for the week"

Historical reason, not technical requirement.

### Iteration 8

**Thought 8:**
No technical reason for Tuesday 9am. Can move to off-hours. But I 
should also check the marketing email impact at 2pm.

**Action 8:**
Query: Site performance during Tuesday 2pm email send

**Observation 8:**
Tuesday 14:00:
- Traffic spike: 10x normal
- Server CPU: 90%
- Some users get 503 errors

Email blast overwhelming servers.

### Iteration 9

**Thought 9:**
Two issues:
1. Index rebuild 9am (solvable: move to night)
2. Email spike 2pm (need rate limiting or scaling)

Let me propose solutions for both.

**Action 9:**
Research: Best practices for handling traffic spikes

**Observation 9:**
Solutions:
1. Schedule index rebuild for 3am (low traffic)
2. Add auto-scaling for email blast days
3. Queue marketing emails with rate limiting
4. CDN caching improvements

### Final Answer

**Root Causes of Tuesday Conversion Drop:**

1. **Primary: Full-text index rebuild (9am-12pm)**
   - Causes database CPU to spike to 95%
   - Query latency increases 5x
   - Conversion drops to 1.8% during this window

2. **Secondary: Marketing email blast (2pm)**
   - 10x traffic spike
   - Server overload, some 503 errors
   - Additional conversion impact

**Recommendations:**

**Immediate (this week):**
- Move index rebuild to Tuesday 3am
- Expected impact: +0.8% conversion on Tuesdays

**Short-term (next sprint):**
- Implement auto-scaling before marketing emails
- Add rate limiting to email sends
- Expected impact: +0.3% conversion

**Total expected improvement:** Tuesday conversion 2.4% → 3.2% 
(+33% improvement, ~$50K/month revenue impact)

**Monitoring:**
- Alert if Tuesday conversion < 2.8%
- Dashboard: Conversion by hour on Tuesdays
```

---

## Common ReAct Patterns

### Pattern 1: Hypothesis-Driven Investigation

```
THOUGHT: I suspect X is causing Y
ACTION: Test if X correlates with Y
OBSERVATION: [Results]
THOUGHT: Confirmed/not confirmed. Next hypothesis...
```

### Pattern 2: Information Gathering

```
THOUGHT: I need to understand X
ACTION: Search/read/query about X
OBSERVATION: [Information]
THOUGHT: Now I know X. Next, understand Y...
```

### Pattern 3: Divide and Conquer

```
THOUGHT: Problem has multiple aspects
ACTION: Test aspect A
OBSERVATION: [A is/isn't the issue]
THOUGHT: Aspect A ruled out. Test aspect B...
```

### Pattern 4: Drill Down

```
THOUGHT: Found high-level issue
ACTION: Get more specific data
OBSERVATION: [Narrowed location]
THOUGHT: Drill deeper into specific area...
```

---

## When to Stop

**Stop when:**
- ✅ Question is definitively answered
- ✅ Root cause identified with evidence
- ✅ Solution verified
- ❌ Going in circles (same thoughts/actions)
- ❃ Making no progress after 3+ iterations
- ❌ Hitting time limits

**If stuck:** Change angle, ask for help, or escalate.
