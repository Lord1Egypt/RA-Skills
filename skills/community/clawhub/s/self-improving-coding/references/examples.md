# Entry Examples

Concrete examples of well-formatted coding entries with all fields.

## Learning: Anti-Pattern (Mutable Default Argument)

```markdown
## [LRN-20250415-001] anti_pattern

**Logged**: 2025-04-15T10:30:00Z
**Priority**: high
**Status**: pending
**Area**: logic

### Summary
Mutable default argument in Python causes shared state across function calls

### Details
Function `def add_item(name, items=[])` uses a mutable list as default argument.
In Python, default arguments are evaluated once at function definition, not at each
call. This means all callers share the same list object, causing items to accumulate
across calls unexpectedly.

### Code Example

**Before (problematic):**
\`\`\`python
def add_item(name, items=[]):
    items.append(name)
    return items

add_item("a")  # ['a']
add_item("b")  # ['a', 'b'] — unexpected!
\`\`\`

**After (correct):**
\`\`\`python
def add_item(name, items=None):
    if items is None:
        items = []
    items.append(name)
    return items
\`\`\`

### Suggested Action
Enable Ruff rule B006 (mutable-argument-default) to catch this at lint time.
Refactor all existing occurrences to use `None` sentinel pattern.

### Metadata
- Source: code_review
- Language: python
- Related Files: src/utils/collections.py
- Tags: python, mutable, default-argument, shared-state
- Pattern-Key: anti_pattern.mutable_default

---
```

## Learning: Idiom Gap (List Comprehension vs map/filter)

```markdown
## [LRN-20250415-002] idiom_gap

**Logged**: 2025-04-15T14:00:00Z
**Priority**: low
**Status**: pending
**Area**: syntax

### Summary
Using map/filter with lambda instead of list comprehension in Python

### Details
Code uses `list(map(lambda x: x * 2, filter(lambda x: x > 0, numbers)))` where
a list comprehension `[x * 2 for x in numbers if x > 0]` is more Pythonic,
more readable, and slightly faster due to avoiding function call overhead.

### Code Example

**Before (non-idiomatic):**
\`\`\`python
result = list(map(lambda x: x * 2, filter(lambda x: x > 0, numbers)))
\`\`\`

**After (idiomatic):**
\`\`\`python
result = [x * 2 for x in numbers if x > 0]
\`\`\`

### Suggested Action
Prefer list/dict/set comprehensions over map/filter with lambdas in Python.
Reserve map/filter for cases where the function already exists (e.g., `map(str, items)`).

### Metadata
- Source: code_review
- Language: python
- Related Files: src/data/transform.py
- Tags: python, comprehension, idiom, readability

---
```

## Learning: Debugging Insight (Race Condition in Async Code)

```markdown
## [LRN-20250416-001] debugging_insight

**Logged**: 2025-04-16T09:15:00Z
**Priority**: critical
**Status**: resolved
**Area**: logic

### Summary
Race condition in async code caused by shared mutable state between coroutines

### Details
Two coroutines both read and write to a shared `dict` tracking user sessions.
Under load, coroutine A reads the dict, coroutine B modifies it, then coroutine A
writes back stale data — overwriting B's changes. The bug was intermittent and
only appeared under concurrent load.

**Diagnosis steps:**
1. Added `asyncio.current_task().get_name()` to log statements at dict access points
2. Observed interleaved reads/writes from different tasks
3. Identified the unprotected critical section
4. Wrapped access with `asyncio.Lock()`

### Code Example

**Before (race condition):**
\`\`\`python
sessions = {}

async def update_session(user_id, data):
    current = sessions.get(user_id, {})
    current.update(data)
    await some_async_io()  # yields control — another coroutine can modify sessions
    sessions[user_id] = current  # overwrites changes made during await
\`\`\`

**After (thread-safe):**
\`\`\`python
sessions = {}
_lock = asyncio.Lock()

async def update_session(user_id, data):
    async with _lock:
        current = sessions.get(user_id, {})
        current.update(data)
        sessions[user_id] = current
    await some_async_io()  # IO outside the lock
\`\`\`

### Suggested Action
Any shared mutable state accessed across `await` boundaries requires synchronization.
Add to debug playbook: when seeing intermittent data inconsistency in async code,
check for unprotected shared state around await points.

### Metadata
- Source: runtime_exception
- Language: python
- Related Files: src/services/session_manager.py
- Tags: async, race-condition, asyncio, concurrency, lock
- Pattern-Key: debugging.async_race_condition

### Resolution
- **Resolved**: 2025-04-16T11:30:00Z
- **Commit/PR**: #87
- **Notes**: Added asyncio.Lock and wrote concurrent test to reproduce

---
```

## Bug Pattern: Off-by-One in Pagination Logic

```markdown
## [BUG-20250415-001] pagination_off_by_one

**Logged**: 2025-04-15T16:00:00Z
**Priority**: high
**Status**: pending
**Area**: logic

### Summary
Pagination returns duplicate items at page boundaries due to off-by-one in offset calculation

### Error Output
\`\`\`
AssertionError: Expected 20 unique items across 2 pages, got 19 unique (1 duplicate)
  at test_pagination_no_duplicates (tests/api/test_pagination.py:45)
\`\`\`

### Root Cause
Offset calculation uses `offset = page * page_size` instead of `offset = (page - 1) * page_size`.
With 1-indexed pages, page 1 skips the first `page_size` items, and the last item of
page N overlaps with the first item of page N+1.

\`\`\`python
# Bug: page 1 → offset=10, skips first 10 items
offset = page * page_size
\`\`\`

### Fix
\`\`\`python
offset = (page - 1) * page_size
\`\`\`

### Prevention
- Add boundary test: assert no duplicates across consecutive pages
- Add test: page 1 starts at item 0
- Consider using cursor-based pagination to avoid offset bugs entirely

### Context
- Trigger: test_failure
- Language: python
- Framework: fastapi
- Input: page=1, page_size=10 returns items starting at index 10 instead of 0

### Metadata
- Reproducible: yes
- Related Files: src/api/routes/items.py, tests/api/test_pagination.py
- Tags: pagination, off-by-one, boundary, api

---
```

## Bug Pattern: Null Reference in Optional Chaining

```markdown
## [BUG-20250416-002] null_optional_chain

**Logged**: 2025-04-16T14:30:00Z
**Priority**: high
**Status**: pending
**Area**: error_handling

### Summary
Optional chaining used for read but not for method call, causing TypeError at runtime

### Error Output
\`\`\`
TypeError: Cannot read properties of undefined (reading 'map')
    at UserList (src/components/UserList.tsx:23)
\`\`\`

### Root Cause
Code uses `user?.addresses` (optional chaining for property access) but then calls
`.map()` directly on the result without checking if the chain resolved to undefined.

\`\`\`typescript
// Bug: addresses is undefined when user is null, .map() throws
const formatted = user?.addresses.map(a => a.street);
\`\`\`

### Fix
\`\`\`typescript
const formatted = user?.addresses?.map(a => a.street) ?? [];
\`\`\`

### Prevention
- Enable TypeScript strict mode (`strictNullChecks: true`)
- Use ESLint rule `@typescript-eslint/no-unsafe-call`
- Always pair optional chaining with nullish coalescing for method calls

### Context
- Trigger: runtime
- Language: typescript
- Framework: react
- Input: user object is null when API returns 404

### Metadata
- Reproducible: yes
- Related Files: src/components/UserList.tsx
- Tags: typescript, optional-chaining, null, undefined, react

---
```

## Feature Request: Auto-Fix for Common Lint Violations

```markdown
## [FEAT-20250415-001] auto_fix_lint

**Logged**: 2025-04-15T17:00:00Z
**Priority**: medium
**Status**: pending
**Area**: tooling

### Requested Capability
Automatic fix for the 10 most common lint violations in the codebase, triggered
on file save or as a pre-commit hook.

### User Context
Developer spends 5-10 minutes per PR fixing lint issues that have well-known
auto-fixes (import sorting, trailing whitespace, missing semicolons, unused imports).
These should be handled automatically.

### Complexity Estimate
simple

### Suggested Implementation
1. Configure Ruff with `fix = true` for safe auto-fixes
2. Add ESLint `--fix` to pre-commit hook
3. Configure VS Code / Cursor to format on save with the project formatter
4. Create a `lint:fix` npm/make script for batch fixes:
   \`\`\`json
   {
     "scripts": {
       "lint:fix": "eslint --fix . && ruff check --fix ."
     }
   }
   \`\`\`

### Metadata
- Frequency: recurring
- Related Features: pre-commit hooks, editor format-on-save

---
```

## Learning: Promoted to Style Guide

```markdown
## [LRN-20250410-003] anti_pattern

**Logged**: 2025-04-10T11:00:00Z
**Priority**: high
**Status**: promoted
**Promoted**: style guide (CODING_STANDARDS.md)
**Area**: error_handling

### Summary
Bare except clauses hide bugs — always catch specific exceptions

### Details
Found 7 instances of bare `except:` or `except Exception:` in the codebase.
These swallow unexpected errors (KeyboardInterrupt, SystemExit, TypeError from
bugs) making debugging extremely difficult. In one case, a TypeError from a
refactoring error was silently swallowed for 3 weeks.

### Code Example

**Before (anti-pattern):**
\`\`\`python
try:
    result = process(data)
except:
    result = default_value
\`\`\`

**After (specific):**
\`\`\`python
try:
    result = process(data)
except (ValueError, KeyError) as e:
    logger.warning("Processing failed for %s: %s", data.id, e)
    result = default_value
\`\`\`

### Suggested Action
Added to style guide: "Always catch specific exceptions. Never use bare except."
Enabled Ruff rule E722 (bare-except) and B001 (ambiguous-except).

### Metadata
- Source: code_review
- Language: python
- Related Files: src/services/*.py
- Tags: exceptions, error-handling, bare-except, debugging
- Pattern-Key: anti_pattern.bare_except
- Recurrence-Count: 7
- First-Seen: 2025-03-20
- Last-Seen: 2025-04-10

---
```

## Learning: Promoted to Skill

```markdown
## [LRN-20250412-001] debugging_insight

**Logged**: 2025-04-12T15:00:00Z
**Priority**: high
**Status**: promoted_to_skill
**Skill-Path**: skills/async-race-conditions
**Area**: logic

### Summary
Systematic approach to diagnosing race conditions in async Python code

### Details
Developed a repeatable diagnosis workflow after encountering 4 separate race
condition bugs in async code over 2 months. The pattern is always the same:
shared mutable state accessed across await boundaries without synchronization.

### Suggested Action
Follow the debug playbook:
1. Identify shared mutable state (dicts, lists, object attributes)
2. Find await points between read and write of shared state
3. Add task-name logging at access points
4. Wrap critical sections with asyncio.Lock()
5. Write concurrent test to verify fix

### Metadata
- Source: runtime_exception
- Language: python
- Related Files: multiple services
- Tags: async, race-condition, debugging, playbook
- See Also: LRN-20250416-001, BUG-20250320-002, BUG-20250401-005

---
```
