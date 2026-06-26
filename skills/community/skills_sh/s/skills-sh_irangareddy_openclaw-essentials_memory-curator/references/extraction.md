# Knowledge Extraction Guide

How to identify and extract valuable patterns from daily logs into MEMORY.md.

## Extraction Signals

### Repetition (3+ occurrences)

**Pattern:**
```
2025-01-15: Spent 30min debugging Apollo cache - forgot to include __typename
2025-01-22: Apollo cache issue again - missing __typename field
2025-02-03: Reminded team: Apollo requires __typename for cache normalization
```

**Extract to MEMORY.md:**
```markdown
## GraphQL Patterns

### Apollo Cache Normalization

**Problem:** Cache not updating after mutations
**Solution:** Ensure all queries include `__typename` field
**Why:** Apollo uses `__typename` + `id` to normalize cache
**Prevention:** Configure Apollo to auto-add `__typename` in queries
```

### High-Cost Learning (>1 hour to solve)

**Pattern:**
```
2025-02-10: [09:00-12:30] Debugging React re-render loop
- Tried React.memo - didn't help
- Suspected context - found it!
- Problem: Creating new object in context provider value prop
- Solution: useMemo for context value
```

**Extract to MEMORY.md:**
```markdown
## React Performance

### Context Re-render Loops

**Symptom:** Infinite re-renders, browser hangs
**Root cause:** New object/array created on every render in context value
**Solution:**
```js
// ❌ Bad - creates new object every render
<Context.Provider value={{ user, settings }}>

// ✅ Good - memoized value
const value = useMemo(() => ({ user, settings }), [user, settings])
<Context.Provider value={value}>
```
**Time saved:** 3+ hours of debugging
```

### Non-Obvious Solutions

**Pattern:**
```
2025-02-05: File uploads failing randomly
- Headers looked correct
- Server receiving empty body
- Found issue: Axios was stringifying FormData
- Solution: Don't set Content-Type header - browser does it
```

**Extract to MEMORY.md:**
```markdown
## HTTP / APIs

### File Upload with FormData

**Gotcha:** Manually setting `Content-Type: multipart/form-data` breaks uploads
**Why:** Browser needs to add boundary parameter
**Solution:** Let browser set Content-Type automatically

❌ Don't:
```js
headers: { 'Content-Type': 'multipart/form-data' }
```

✅ Do:
```js
// Omit Content-Type - browser handles it
await axios.post('/upload', formData)
```
```

### Successful Patterns Worth Reusing

**Pattern:**
```
2025-02-12: Built feature flag system
- Used LaunchDarkly SDK
- SSR + client hydration pattern worked well
- Flags evaluated server-side, passed to client
- Zero flicker on page load
```

**Extract to MEMORY.md:**
```markdown
## Architecture Patterns

### Feature Flags with SSR

**Approach:** Evaluate flags server-side, pass to client

**Benefits:**
- No flicker/flash of wrong variant
- SEO sees correct variant
- Faster initial render

**Implementation:**
1. Evaluate flags in `getServerSideProps`
2. Pass flags to client via props
3. Initialize client SDK with server flags
4. Client SDK subscribes to updates

**Code:**
```js
// Server
export async function getServerSideProps(context) {
  const flags = await ldClient.allFlagsState(context.user)
  return { props: { flags } }
}

// Client
<LDProvider flags={props.flags}>
  <App />
</LDProvider>
```
```

## Extraction Workflow

### Weekly Review (Recommended)

**Every Friday/Sunday:**

1. **Read last 7 days of logs**
   ```bash
   python search_memory.py --workspace ~/.openclaw/workspace --recent 7
   ```

2. **Look for patterns:**
   - Repeated issues
   - Time-consuming problems
   - Valuable discoveries
   - Decisions worth remembering

3. **Extract to MEMORY.md:**
   - Add new sections or update existing ones
   - Remove outdated information
   - Consolidate related entries

4. **Update daily log with extraction note:**
   ```markdown
   ## 2025-02-14

   - [18:00] Weekly review: Extracted 3 patterns to MEMORY.md
     - Apollo cache normalization
     - React context re-renders
     - Feature flags SSR pattern
   ```

### Monthly Consolidation

**Once a month:**

1. **Review MEMORY.md structure:**
   - Are categories still relevant?
   - Is information easy to find?
   - Any duplicate entries?

2. **Archive old daily logs:**
   ```bash
   # Optional: Move logs older than 90 days to archive
   mkdir -p memory/archive/2025-Q1
   mv memory/2025-01-*.md memory/archive/2025-Q1/
   ```

3. **Update index/table of contents** in MEMORY.md

## Extraction Criteria

### ✅ Extract When:

- Pattern appears **3+ times**
- Solution took **>1 hour** to find
- Solution is **non-obvious**
- Will save **significant time** in future
- Applies to **multiple projects**
- Mistake was **costly** to debug
- Pattern is **generalizable**

### ❌ Don't Extract:

- One-off fixes
- Project-specific hacks
- Obvious solutions
- Rapidly changing APIs
- Tool version-specific workarounds
- Personal preferences (unless team-wide)

## Extraction Quality

### Good Extraction

```markdown
## Database Patterns

### Avoiding N+1 Queries

**Problem:** Loading user posts generates N queries (one per user)
**Solution:** Use DataLoader for batching

**Example:**
```js
const userLoader = new DataLoader(async (ids) => {
  return await User.findAll({ where: { id: ids } })
})

// Batches multiple user requests into single query
const users = await Promise.all(ids.map(id => userLoader.load(id)))
```

**When to use:** GraphQL resolvers, nested data fetching
**Libraries:** dataloader (Node.js), aiodataloader (Python)
```

**Why it's good:**
- Clear problem statement
- Concrete solution
- Code example
- Context for when to use
- Language-specific libraries

### Bad Extraction

```markdown
## Stuff I Learned

- DataLoader is good for databases
- Use it when you have performance issues
```

**Why it's bad:**
- Vague problem
- No context
- No code example
- No actionable guidance

## Tools for Extraction

### Search for Patterns

```bash
# Find all entries about a topic
python search_memory.py --workspace ~/.openclaw/workspace --query "Apollo"

# Review recent work
python search_memory.py --workspace ~/.openclaw/workspace --recent 14
```

### Extract Session

```bash
# Generate session summary with learnings template
python extract_session.py \
  --session ~/.openclaw/agents/main/sessions/abc123.jsonl \
  --output session-summary.md

# Review summary, copy key learnings to MEMORY.md
```

## Example Extraction Process

**1. Find pattern in logs:**

```bash
$ python search_memory.py --workspace ~/.openclaw/workspace --query "CORS"

Found matches in 3 file(s):

📄 2025-02-05.md
Line 23:
>>> - [14:30] CORS error - forgot to add credentials: 'include'

📄 2025-02-12.md
Line 15:
>>> - [10:15] CORS issue again - client needs withCredentials

📄 2025-02-18.md
Line 32:
>>> - [16:00] Helped teammate with CORS + cookies
```

**2. Extract to MEMORY.md:**

```markdown
## HTTP / APIs

### CORS with Cookies

**Problem:** Cookies not sent with CORS requests
**Solution:** Enable credentials on both client and server

**Client (fetch):**
```js
fetch(url, { credentials: 'include' })
```

**Client (axios):**
```js
axios.get(url, { withCredentials: true })
```

**Server:**
```js
res.header('Access-Control-Allow-Credentials', 'true')
res.header('Access-Control-Allow-Origin', 'https://specific-domain.com') // Not '*'
```

**Gotcha:** `Allow-Origin` cannot be `*` when using credentials

**Repeated:** 3 times in Feb 2025
```

**3. Note extraction in daily log:**

```markdown
## 2025-02-18

- [18:30] Weekly review: Extracted CORS + cookies pattern to MEMORY.md (appeared 3x this month)
```
