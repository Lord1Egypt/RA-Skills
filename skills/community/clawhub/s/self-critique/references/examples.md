# Self-Critique - Detailed Examples

## Example 1: Architecture Decision

**Task:** "Choose database for new microservice"

**Initial Analysis:**
```markdown
We should use PostgreSQL for the new service.

Pros:
- Reliable
- Good querying
- Team knows it

Cons:
- None really

Recommendation: Use PostgreSQL.
```

**Self-Critique:**
```markdown
CRITIQUE PERSONA: "Experienced architect who has been burned by bad decisions"

## Criteria
- [ ] All viable options considered
- [ ] Trade-offs quantified
- [ ] Scalability addressed
- [ ] Team skills factored
- [ ] Migration path considered
- [ ] Cost implications
- [ ] Operational overhead
- [ ] Decision reversibility

## Findings

### CRITICAL
1. **Only one option considered** (PostgreSQL)
   - MongoDB, DynamoDB, Cassandra not evaluated
   - Service has high write volume, relational might not be best
   - FIX: Evaluate 3+ options

2. **No scalability analysis**
   - Expected: 10K writes/second in year 1
   - PostgreSQL single-node limits?
   - FIX: Include capacity planning

3. **"None really" for cons is lazy**
   - PostgreSQL has real limitations
   - FIX: Honest trade-off analysis

### MODERATE
4. **No cost comparison**
   - Managed PostgreSQL vs self-hosted?
   - FIX: Include TCO estimate

5. **Migration from existing system?**
   - Current service uses MySQL
   - Dual-write period needed?
   - FIX: Migration plan section

### POSITIVE
✓ Team familiarity is valid consideration
✓ Recommendation is clear (even if premature)

## Summary
Analysis is superficial. Need:
- Evaluate alternatives
- Quantify trade-offs
- Address scalability
- Include migration plan

## Revised Analysis
```markdown
## Options Evaluated

### Option 1: PostgreSQL (Managed)
**Pros:**
- Team expertise (3 engineers with 5+ years each)
- ACID compliance for data integrity
- Rich querying (JSONB for flexibility)

**Cons:**
- Vertical scaling limits ~10K writes/sec
- Failover complexity
- $2,000/month for managed instance

**Verdict:** Good for complex queries, write volume concern

---

### Option 2: MongoDB (Atlas)
**Pros:**
- Horizontal scaling (sharding)
- Flexible schema (service still evolving)
- Native JSON (matches API format)

**Cons:**
- Team learning curve (1 engineer has experience)
- Eventual consistency for some operations
- $1,500/month for similar performance

**Verdict:** Good for write volume, querying limitations

---

### Option 3: DynamoDB
**Pros:**
- Serverless scaling
- Pay per use (low traffic = low cost)
- Managed entirely

**Cons:**
- Query limitations (no joins)
- AWS lock-in
- Complex pricing model
- Team has minimal experience

**Verdict:** Good scaling, operational risk

## Trade-off Analysis

| Criteria | PostgreSQL | MongoDB | DynamoDB |
|----------|-----------|---------|----------|
| Write throughput | 6/10 | 9/10 | 10/10 |
| Query flexibility | 10/10 | 6/10 | 5/10 |
| Team expertise | 10/10 | 4/10 | 2/10 |
| Operational burden | 5/10 | 7/10 | 9/10 |
| Cost (est.) | $2K/mo | $1.5K/mo | $800-3K/mo |

## Scalability Analysis

Current: 1K writes/sec
Year 1: 10K writes/sec
Year 3: 50K writes/sec

- PostgreSQL: Single-node limit ~15K/sec. Would need read replicas + partitioning by year 2.
- MongoDB: Sharding handles 50K+ with proper indexing
- DynamoDB: Scales automatically

## Recommendation

**Primary: MongoDB**
- Handles write volume growth
- Flexible schema (service evolving)
- Lower cost than PostgreSQL at scale
- Can add PostgreSQL later for analytics if needed

**Migration Plan:**
1. Dual-write to MongoDB (2 weeks)
2. Backfill historical data (1 week)
3. Switch reads to MongoDB (1 day)
4. Monitor for 1 week
5. Remove MySQL writes
6. Decommission MySQL (month 3)

**Risk Mitigation:**
- Train 2 engineers on MongoDB before migration
- Keep MySQL as backup for 1 month
- Automated rollback script ready

**Confidence:** High (7/10)
```
```

---

## Example 2: Bug Report Response

**Task:** "Respond to customer bug report"

**Initial Draft:**
```
Hi,

Thanks for the report. We fixed the bug.
It should work now.

Let us know if you have issues.

Thanks,
Support Team
```

**Self-Critique:**
```markdown
CRITIQUE PERSONA: "Frustrated customer who just reported a critical bug"

## Criteria
- [ ] Acknowledges impact on customer
- [ ] Explains what went wrong
- [ ] Specific about fix
- [ ] Timeline clear
- [ ] Prevention mentioned
- [ ] Professional tone
- [ ] Next steps clear

## Findings

### CRITICAL
1. **No apology for impact**
   - Customer's business was affected
   - "Thanks for the report" is dismissive
   - FIX: Acknowledge severity and apologize

2. **"The bug" - which bug?**
   - Not specific, seems like template
   - FIX: Reference specific issue

3. **"Should work now" - uncertainty**
   - Did you test it?
   - FIX: Confirm verification

### MODERATE
4. **No explanation of root cause**
   - Customer wondering if it'll happen again
   - FIX: Brief technical explanation

5. **No compensation mentioned**
   - SLA breach? Credit due?
   - FIX: Address if applicable

### MINOR
6. **"Support Team" impersonal**
   - FIX: Actual name

## Summary
Response feels robotic and dismissive. Needs empathy, specificity, and assurance.

## Revised Response
```
Hi Sarah,

I sincerely apologize for the disruption this caused your team yesterday. 
I know having the export fail right before your client deadline was 
stressful, and that's not the experience we want to provide.

**What happened:**
Our database migration (completed March 15) introduced a regression in 
the CSV export module. Large datasets (>10,000 rows) were triggering a 
timeout due to an inefficient query. This affected your account and 12 
others.

**What we fixed:**
- Optimized the export query (now 10x faster)
- Added pagination for large exports
- Deployed fix at 3:30pm PT today
- Tested with your specific dataset (87,000 rows) - export now completes 
  in 12 seconds

**To prevent recurrence:**
We've added automated tests for exports with >50K rows and monitoring 
alerts if export time exceeds 30 seconds.

**Next steps:**
1. Please try your export again and confirm it works
2. I've applied a $200 service credit to your account for this incident
3. I'll follow up in 24 hours to ensure everything is smooth

If you hit any other issues, reply directly to this email or call me at 
(555) 123-4567.

Again, I'm sorry for the trouble.

Best,
Michael Chen
Senior Support Engineer
```
```

---

## Example 3: Code Review Self-Critique

**Task:** "Review your own PR before requesting review"

**Code Being Committed:**
```python
def get_user_data(user_id):
    """Get user data."""
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM users WHERE id = {user_id}")
    result = cur.fetchone()
    cur.close()
    conn.close()
    return result
```

**Self-Critique:**
```markdown
CRITIQUE PERSONA: "Senior engineer reviewing junior's code"

## Criteria
- [ ] SQL injection safe
- [ ] Connection handling robust
- [ ] Error handling complete
- [ ] Return type clear
- [ ] Documentation adequate
- [ ] Tests exist
- [ ] Performance considered

## Findings

### CRITICAL
1. **SQL Injection vulnerability**
   - `f"...{user_id}"` is unsafe
   - Attacker could pass `user_id = "1; DROP TABLE users;--"`
   - FIX: Use parameterized query

2. **Connection not using pool**
   - Creating new connection per call
   - High latency under load
   - FIX: Use connection pool

3. **No error handling**
   - Database down = unhandled exception
   - FIX: Try/except with proper logging

4. **SELECT * is bad practice**
   - Returns unnecessary columns
   - Schema changes break consumers
   - FIX: Explicit column list

### MODERATE
5. **Missing type hints**
   - FIX: Add return type: `-> Optional[User]`

6. **Docstring too vague**
   - "Get user data" - which data?
   - FIX: Document return format, exceptions

7. **Connection not context manager**
   - If exception, connection might not close
   - FIX: Use `with` statement

### MINOR
8. **No caching**
   - User data rarely changes
   - FIX: Add cache (if appropriate)

## Revised Code
```python
from typing import Optional
import logging
from psycopg2 import sql
from psycopg2.pool import SimpleConnectionPool

# Module-level connection pool
_db_pool = None

def init_db_pool(min_conn=1, max_conn=10):
    global _db_pool
    _db_pool = SimpleConnectionPool(min_conn, max_conn, DB_URL)

def get_user_data(user_id: int) -> Optional[dict]:
    """
    Get user data by ID.
    
    Args:
        user_id: The user ID to look up
        
    Returns:
        Dict with user data or None if not found
        
    Raises:
        DatabaseError: If database query fails
    """
    if _db_pool is None:
        init_db_pool()
    
    conn = None
    try:
        conn = _db_pool.getconn()
        with conn.cursor() as cur:
            cur.execute(
                sql.SQL("SELECT id, email, name, created_at FROM users WHERE id = %s"),
                (user_id,)
            )
            row = cur.fetchone()
            
            if row is None:
                return None
                
            return {
                'id': row[0],
                'email': row[1],
                'name': row[2],
                'created_at': row[3]
            }
    except psycopg2.Error as e:
        logging.error(f"Database error fetching user {user_id}: {e}")
        raise DatabaseError(f"Failed to fetch user {user_id}") from e
    finally:
        if conn:
            _db_pool.putconn(conn)
```

## Self-Reflection
Caught 4 critical security/robustness issues. Original code was dangerous to ship.
```

---

## Example 4: Documentation

**Task:** "Document API endpoint"

**Initial Draft:**
```markdown
## POST /api/users

Creates a user.

Parameters:
- email: string
- name: string

Returns user object.
```

**Self-Critique:**
```markdown
CRITIQUE PERSONA: "New developer trying to use this API"

## Criteria
- [ ] Clear what endpoint does
- [ ] All parameters documented
- [ ] Required vs optional clear
- [ ] Validation rules stated
- [ ] Example request provided
- [ ] Example response provided
- [ ] Error cases documented
- [ ] Auth requirements clear
- [ ] Rate limits mentioned

## Findings

### CRITICAL
1. **No authentication mentioned**
   - Is this public? Token required?
   - FIX: Add auth section

2. **Missing required vs optional**
   - Both parameters required?
   - FIX: Mark required fields

3. **No validation rules**
   - Email format? Name length?
   - FIX: Document constraints

4. **No error examples**
   - What if email exists?
   - What if invalid format?
   - FIX: Error response section

### MODERATE
5. **No example request**
   - FIX: Include curl example

6. **No example response**
   - What does "user object" mean?
   - FIX: Show JSON response

7. **No rate limiting**
   - Throttling? Limits?
   - FIX: Add rate limit header

### MINOR
8. **"Creates a user" too vague**
   - What happens? Email sent? Active immediately?
   - FIX: Describe full behavior

## Revised Documentation
```markdown
## POST /api/users

Create a new user account. User will receive email verification before 
account is activated.

### Authentication
Requires API key in header: `Authorization: Bearer {token}`

### Rate Limiting
10 requests per minute per IP

### Request Body

| Field | Type | Required | Description | Validation |
|-------|------|----------|-------------|------------|
| email | string | Yes | User's email | Valid email format, unique |
| name | string | Yes | User's full name | 2-100 characters |
| role | string | No | User role | "admin", "user" (default: "user") |

### Example Request
```bash
curl -X POST https://api.example.com/api/users \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "name": "John Doe",
    "role": "user"
  }'
```

### Success Response (201 Created)
```json
{
  "id": "usr_123456",
  "email": "user@example.com",
  "name": "John Doe",
  "role": "user",
  "status": "pending_verification",
  "created_at": "2024-03-15T10:30:00Z",
  "verification_email_sent": true
}
```

### Error Responses

**400 Bad Request - Validation Error**
```json
{
  "error": "validation_error",
  "message": "Invalid input data",
  "details": {
    "email": ["Invalid email format"],
    "name": ["Name must be at least 2 characters"]
  }
}
```

**409 Conflict - Email Exists**
```json
{
  "error": "conflict",
  "message": "Email already registered"
}
```

**429 Too Many Requests**
```json
{
  "error": "rate_limit",
  "message": "Rate limit exceeded. Retry in 60 seconds."
}
```

### Notes
- User status will be `pending_verification` until email confirmed
- Verification email expires in 24 hours
- Duplicate email returns 409 (not 200)
```
```

---

## Example 5: Decision Explanation

**Task:** "Explain why we chose Solution B over Solution A"

**Initial Explanation:**
```
We chose Solution B because it's better.

Solution A had some issues.
Solution B is faster.
```

**Self-Critique:**
```markdown
CRITIQUE PERSONA: "Stakeholder who advocated for Solution A"

## Criteria
- [ ] Acknowledges Solution A fairly
- [ ] Specific technical reasons for B
- [ ] Trade-offs honestly stated
- [ ] No dismissive language
- [ ] Data/evidence cited
- [ ] Future implications considered
- [ ] Respectful tone

## Findings

### CRITICAL
1. **"Better" is subjective and dismissive**
   - Sounds like bias, not analysis
   - FIX: Specific technical criteria

2. **"Some issues" - vague dismissal**
   - Should acknowledge valid points
   - FIX: Fair comparison

3. **"Faster" - how much? Why?**
   - No data
   - FIX: Benchmark numbers

4. **No trade-offs mentioned**
   - Solution B must have downsides
   - FIX: Honest trade-off analysis

### MODERATE
5. **Who was involved in decision?**
   - FIX: Reference decision process

6. **Reversible if wrong?**
   - FIX: Risk mitigation

## Revised Explanation
```
After evaluating both options, we selected Solution B. Here's the 
analysis:

## Both Solutions Have Merits

**Solution A (microservices)** has real strengths:
- Team expertise in this architecture
- Independent scaling of services
- Technology flexibility per service

We seriously considered it and prototyped for 2 weeks.

## Why Solution B (modular monolith) Was Selected

### Performance Data
- Solution A: 450ms p99 latency (service hops add overhead)
- Solution B: 120ms p99 latency
- Our use case: 80% of requests need data from 3+ services, making 
  microservice overhead significant

### Complexity Trade-off
- Solution A: 15 services to deploy, monitor, debug
- Solution B: 1 deployable unit, modular boundaries maintained
- Team size (4 engineers) favors simpler ops

### Time to Market
- Solution A: Estimated 4 months (ops overhead)
- Solution B: Estimated 2.5 months
- Business priority: Launch in Q2

## Acknowledging Trade-offs

**What we lose with Solution B:**
- Independent service scaling (mitigation: horizontal scaling of 
  monolith works for our load)
- Technology diversity per module (mitigation: standardized stack 
  acceptable for our needs)

**Risk mitigation:**
- Module boundaries clearly defined for future extraction
- If we need microservices later, well-defined modules make migration 
  easier
- Decision reversible: can extract services in future if needed

## Conclusion

Solution B meets our performance requirements with lower operational 
complexity given team size. The 6-week time savings is critical for Q2 
launch.

This was a team decision (4 engineers + architect) after 2-week 
prototype evaluation.
```
```

---

## Quick Reference: Critique Personas

Choose a persona based on what you're reviewing:

| Output Type | Persona | Focus |
|-------------|---------|-------|
| Code | Security engineer | Injection, auth, secrets |
| Code | Future maintainer | Clarity, documentation |
| Code | Performance engineer | Efficiency, scaling |
| Writing | Target audience | Understanding, relevance |
| Writing | Skeptical reader | Logic, evidence |
| Analysis | Peer reviewer | Methodology, rigor |
| Decision | Stakeholder | Fairness, trade-offs |

---

## Checklist Summary

Before shipping any output, ask:

- [ ] Have I waited 5+ minutes since creating it?
- [ ] Did I review against specific criteria?
- [ ] Did I classify issues by severity?
- [ ] Did I suggest specific fixes?
- [ ] Did I actually make the fixes?
- [ ] Would I be proud if my name was on this?

If no: critique again.
