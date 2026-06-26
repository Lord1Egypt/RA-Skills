# Memory Organization

How to structure MEMORY.md for effective knowledge retrieval.

## Organization Principles

### 1. Topic-Based Structure

Group by **domain** or **technology**, not chronologically.

✅ Good:
```markdown
## React Patterns
## GraphQL Patterns
## Database Patterns
```

❌ Bad:
```markdown
## February 2025 Learnings
## January 2025 Learnings
```

### 2. Problem-Solution Format

Lead with the **problem** so you can find it when facing the same issue.

✅ Good:
```markdown
### Infinite Re-render Loop

**Problem:** Component re-renders infinitely
**Cause:** New object created in dependency array
**Solution:** Use useMemo
```

❌ Bad:
```markdown
### useMemo Hook

You should use useMemo when...
```

### 3. Searchable Titles

Use **specific**, **searchable** terms.

✅ Good:
```markdown
### Apollo Cache Not Updating After Mutation
### CORS Errors with Cookies
### N+1 Query Problem in GraphQL
```

❌ Bad:
```markdown
### Cache Issue
### API Problem
### Query Optimization
```

### 4. Flat Hierarchy

Keep structure **maximum 2 levels deep** for quick scanning.

✅ Good:
```markdown
## React Patterns
### Context Re-renders
### Infinite Loops
### State Updates
```

❌ Bad:
```markdown
## Frontend
### React
#### Hooks
##### Performance
###### Memoization
```

## Organization Patterns

### By Technology/Framework

```markdown
# MEMORY.md

## React

### Context Re-renders
### Component Memoization
### useEffect Dependencies

## GraphQL

### Apollo Cache Normalization
### N+1 Queries
### Batching with DataLoader

## TypeScript

### Generic Type Constraints
### Discriminated Unions
### Type Guards

## Database

### Query Optimization
### Index Design
### Connection Pooling
```

**When to use:** Full-stack projects, multiple technologies

### By Problem Domain

```markdown
# MEMORY.md

## Performance

### Frontend Performance
- React re-renders
- Bundle size optimization
- Lazy loading

### Backend Performance
- Database query optimization
- Caching strategies
- API response times

## Security

### Authentication
- JWT best practices
- Session management

### Authorization
- Role-based access
- Permission checks

## Data Management

### State Management
### Data Fetching
### Caching
```

**When to use:** Large projects, cross-cutting concerns

### By Activity Type

```markdown
# MEMORY.md

## Common Solutions

### Debugging
- Memory leaks
- Race conditions
- Network issues

### Patterns
- Authentication flows
- Error handling
- Data validation

## Mistakes to Avoid

### Performance
### Security
### Architecture
```

**When to use:** Teaching/mentoring focus

## Template Structures

### Minimal Template

```markdown
# MEMORY.md

## [Technology/Domain]

### [Problem]

**Solution:**

**Context:**
```

### Detailed Template

```markdown
# MEMORY.md

## [Technology/Domain]

### [Problem Title]

**Problem:** [Description]
**Symptoms:** [How it manifests]
**Cause:** [Root cause]
**Solution:** [How to fix]
**Code:** [Example]
**Prevention:** [How to avoid]
**References:** [Links, docs]
```

### Pattern-Based Template

```markdown
# MEMORY.md

## [Domain] Patterns

### [Pattern Name]

**Use when:** [Conditions]
**Problem solved:** [What it addresses]
**Implementation:**
[Code/steps]
**Trade-offs:** [Pros/cons]
**Alternatives:** [Other approaches]
```

## Section Types

### Patterns & Best Practices

```markdown
## React Patterns

### Server Components Pattern

**Use when:** Need SEO + fast initial render
**Benefits:** RSC hydration, reduced JS bundle
**Trade-offs:** Can't use hooks, interactive = client component
```

### Common Solutions

```markdown
## Common Solutions

### Debugging Memory Leaks

**Tool:** Chrome DevTools Memory Profiler
**Steps:**
1. Take heap snapshot
2. Perform action
3. Take second snapshot
4. Compare snapshots
5. Look for "Detached" DOM nodes
```

### Mistakes to Avoid

```markdown
## Mistakes to Avoid

### ❌ Storing Derived State

**Don't:**
```js
const [total, setTotal] = useState(0)
const [items, setItems] = useState([])

// Derived state can get out of sync
useEffect(() => {
  setTotal(items.reduce((sum, item) => sum + item.price, 0))
}, [items])
```

**Do:**
```js
const [items, setItems] = useState([])
const total = items.reduce((sum, item) => sum + item.price, 0)
```
```

### Useful References

```markdown
## Useful References

### GraphQL
- [Apollo Client Docs](https://apollographql.com/docs/react)
- [GraphQL Best Practices](https://graphql.org/learn/best-practices)

### React
- [React Beta Docs](https://react.dev)
- [Patterns.dev](https://patterns.dev)
```

## Maintenance Strategies

### Table of Contents

For MEMORY.md > 500 lines, add TOC at top:

```markdown
# MEMORY.md

## Table of Contents

- [React](#react)
  - [Context Re-renders](#context-re-renders)
  - [Infinite Loops](#infinite-loops)
- [GraphQL](#graphql)
  - [Apollo Cache](#apollo-cache)
  - [N+1 Queries](#n1-queries)
- [Database](#database)
  - [Query Optimization](#query-optimization)

---

## React

### Context Re-renders

...
```

### Splitting Large Files

When MEMORY.md > 1000 lines, split by domain:

```
workspace/
├── MEMORY.md (index + most common patterns)
├── memory/
│   ├── 2025-02-15.md (daily logs)
│   └── domains/
│       ├── react.md
│       ├── graphql.md
│       ├── database.md
│       └── security.md
```

Update MEMORY.md to reference domain files:

```markdown
# MEMORY.md

## Quick Reference

[Most common 10-15 patterns here]

## Domain Knowledge

For detailed patterns, see:
- [React Patterns](memory/domains/react.md)
- [GraphQL Patterns](memory/domains/graphql.md)
- [Database Patterns](memory/domains/database.md)
- [Security Patterns](memory/domains/security.md)
```

### Regular Cleanup

**Monthly:**
1. Remove outdated entries
2. Consolidate duplicate patterns
3. Update code examples
4. Check links still work
5. Reorganize if structure is hard to navigate

### Version Control

**Track MEMORY.md in git:**
```bash
git add MEMORY.md memory/
git commit -m "Memory: Add Apollo cache normalization pattern"
```

**Benefits:**
- History of what you've learned
- Rollback if needed
- Sync across machines

## Search Strategies

### Using grep

```bash
# Find pattern in MEMORY.md
grep -i "apollo" workspace/MEMORY.md

# Search with context
grep -C 3 -i "cache" workspace/MEMORY.md
```

### Using memory scripts

```bash
# Search all memory files
python scripts/search_memory.py --workspace ~/.openclaw/workspace --query "CORS"

# Recent entries only
python scripts/search_memory.py --workspace ~/.openclaw/workspace --query "CORS" --days 30
```

### Editor Search

Most editors support full-text search:
- VS Code: `Cmd+Shift+F`
- Vim: `:grep`
- Emacs: `M-x grep`

## Example Organizations

### Solo Developer

```markdown
# MEMORY.md

## Patterns
[Common patterns across all work]

## Gotchas
[Mistakes and how to avoid them]

## Shortcuts
[Time-saving techniques]

## Resources
[Useful links and docs]
```

**Why:** Simple, all knowledge in one place, easy to search

### Team/Shared Workspace

```markdown
# MEMORY.md

## Architecture Decisions
[ADRs and rationale]

## Patterns
[Approved patterns to follow]

## Code Standards
[Team conventions]

## Onboarding
[New team member guide]

## Troubleshooting
[Common issues and fixes]
```

**Why:** Team-focused, standardization, consistency

### Learning/Experimentation

```markdown
# MEMORY.md

## TIL (Today I Learned)
[Quick discoveries]

## Deep Dives
[Detailed explorations]

## Experiments
[What I tried and results]

## Questions
[Open questions to investigate]
```

**Why:** Learning-focused, captures exploration journey
