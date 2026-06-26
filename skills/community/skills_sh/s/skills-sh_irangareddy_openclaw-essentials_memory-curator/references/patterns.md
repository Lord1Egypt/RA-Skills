# Memory Logging Patterns

Guidance on what to log in different scenarios.

## Daily Logging

### Feature Development

Log:
- Feature scope and requirements
- Key implementation decisions (why approach X over Y)
- APIs/libraries integrated
- Edge cases handled
- Tests written
- Related issues/PRs

Don't log:
- Every file changed (git history has this)
- Routine commits
- Obvious implementation details

### Bug Fixes

Log:
- Bug symptoms and reproduction steps
- Root cause analysis
- Solution approach
- Why other approaches didn't work
- Prevention strategy

### Research & Learning

Log:
- Research question
- Sources consulted
- Key findings
- Decisions made based on research
- Related resources

### Debugging Sessions

Log:
- Initial symptoms
- Debugging approach
- Dead ends explored
- Final solution
- Time spent (if significant)

### Architecture Decisions

Log:
- Problem being solved
- Options considered
- Trade-offs analyzed
- Decision made and rationale
- Stakeholders involved
- Expected impact

### Meetings & Discussions

Log:
- Key decisions
- Action items assigned
- Open questions
- Context needed later

## Session Preservation

### Before `/new` or `/reset`

Save:
- Current task state (what's in progress)
- Decisions made this session
- Context that will be lost
- Open questions
- Next steps

### After Major Work

Save:
- What was accomplished
- Key learnings
- Patterns discovered
- Problems encountered
- Solutions that worked

### Failed Attempts

Log:
- What was tried
- Why it failed
- What was learned
- Alternative approaches to try

## Knowledge Extraction

### When to Extract to MEMORY.md

Extract when:
- Same pattern appears 3+ times
- Solution was non-obvious
- Mistake was costly to debug
- Approach saved significant time
- Information will be useful across projects

Don't extract:
- One-off solutions
- Project-specific details (keep in daily logs)
- Obvious information
- Rapidly changing APIs/tools

## Categorization

### By Work Type

- **Development**: Feature work, refactoring
- **Debugging**: Bug fixes, performance issues
- **Research**: Learning, investigation
- **Planning**: Architecture, design decisions
- **Operations**: Deployments, incidents

### By Domain

- **Frontend**: UI, components, styling
- **Backend**: APIs, database, services
- **Infrastructure**: DevOps, CI/CD, hosting
- **Tooling**: Build tools, CLI, automation
- **Testing**: Test strategies, frameworks

## Log Entry Format

### Timestamp Entries

```markdown
- [14:30] Implemented user authentication with JWT
- [15:45] Fixed race condition in payment processing
```

### Structured Entries

```markdown
## Feature: User Profile Dashboard

**Decision:** Use GraphQL for data fetching
**Rationale:** Reduces over-fetching, better type safety
**Alternative considered:** REST with multiple endpoints
**Trade-off:** Added GraphQL server complexity

**Implementation:**
- Apollo Client on frontend
- Apollo Server with resolvers
- DataLoader for batching

**Testing:**
- Unit tests for resolvers
- Integration tests for queries
- E2E tests for critical flows
```

### Quick Notes

```markdown
- Discovered: Apollo cache normalization requires `id` field
- TIL: React.memo doesn't prevent re-renders from context changes
- Remember: Run `pnpm install` after pulling main branch changes
```

## Memory Organization

### Daily Logs (`memory/YYYY-MM-DD.md`)

- Chronological entries
- Activity-focused
- Includes timestamps
- Raw notes and observations

### MEMORY.md

- Topic-organized
- Pattern-focused
- Extracted knowledge
- Timeless insights

### When to Use Which

**Daily logs** for:
- "What did I do on [date]?"
- "When did I implement X?"
- Session history
- Activity tracking

**MEMORY.md** for:
- "How do I solve X?"
- "What's the pattern for Y?"
- Best practices
- Common solutions
