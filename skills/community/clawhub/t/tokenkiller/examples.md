## Example 1: Large Repository Issue Localization (Throttled Version)

**User**: `A button click has no response, help me find the cause`

**TokenKiller Behavior:**

- First produce L0: Locate and fix the cause of button click not triggering
- Constraints L1: No API changes; minimal modifications; buildable after fix
- Tool strategy: First `Grep` search "button text/component name" → then read hit segment
- Only read hit segment context, don't read through entire repository
- After fix, run `npm run build`

**Output (Example):**

- **Conclusion**: onClick was overridden / event was stopPropagation'd causing non-trigger
- **Evidence**: `src/components/X.tsx:L88-L102`
- **Changes**: Adjusted event binding and added regression verification
- **Next Step**: Add 1 minimal unit test or manual verification checklist

## Example 2: Long Log Troubleshooting (Throttled Version)

**User**: `Build failed, logs are huge`

**TokenKiller Behavior:**

- Only take: error line, stack top 20 lines, reproduction command, related config filenames
- Don't take: full logs
- First list 3 hypotheses → verify one by one (only append necessary evidence each time)

## Example 3: Code Refactoring (Dynamic Budget)

**User**: `Refactor the authentication module to use dependency injection`

**TokenKiller Behavior:**

- **Complexity Assessment**: Complex (cross-module refactor, needs exploration)
- **Budget**: ≤10 tool calls, ≤200 lines output
- L0: Refactor auth module to use DI pattern
- L1: Maintain backward compatibility; minimal file changes; tests pass

**Execution:**

1. `Grep` for "auth" related files → identify core files
2. Read only function signatures and dependencies (L2 evidence)
3. Implement changes incrementally

**Budget Warning Example:**

```
[TokenKiller] Budget running low, current progress 8/10, remaining work: add unit tests
```

**Output (Example):**

- **Conclusion**: Auth module now uses DI container
- **Evidence**: `src/auth/AuthService.ts:L15-L45`, `src/auth/index.ts:L1-L10`
- **Changes**: Extracted interfaces; registered in DI container
- **Next Step**: Add integration tests for new DI setup

## Example 4: Test Verification (Cost Ordering)

**User**: `Verify the payment flow works correctly`

**TokenKiller Behavior:**

- L0: Verify payment flow end-to-end
- L1: No production changes; document failures only

**Verification Order (Cheap → Expensive):**

1. **TypeScript check** (`tsc --noEmit`) — cheapest, catches type errors
2. **Lint** (`eslint`) — catches style/pattern issues
3. **Build** (`npm run build`) — validates compilation
4. **Unit tests** (`jest --testPathPattern=payment`) — focused tests only
5. **E2E** (only if all above pass)

**Output (Example):**

- **Conclusion**: Payment flow verification complete
- **Evidence**: `tsc` passed; `jest payment.test.ts` 12/12 passed
- **Changes**: None required
- **Next Step**: Monitor production metrics

## Example 5: L3 Pull Scenarios

### Scenario A: Code Modification Needs Exact Format

**Context**: Need to modify a function but indentation matters.

**Decision**: L2 insufficient → Pull L3 for target function only.

```
L2 Evidence: src/utils/parser.ts:L45 (contains parseFunction)
↓ Attempt to modify with L2 only
↓ Fail: Cannot match exact indentation
↓ Pull L3: Read lines 40-60 (target function scope)
✓ Success: Make precise edit
```

### Scenario B: Error Analysis Needs Full Stack

**Context**: Error message truncated, need full context.

**Decision**: Pull L3 for complete stack trace.

```
L2 Evidence: "TypeError at line 102"
↓ Attempt to diagnose
↓ Fail: Need more context
↓ Pull L3: Full error log (filtered for relevant frames)
✓ Success: Identify root cause
```

### Scenario C: Config Dependencies

**Context**: Nested config with cross-references.

**Decision**: Pull L3 for config block.

```
L2 Evidence: config.json references "dbConfig"
↓ Attempt to trace
↓ Fail: dbConfig defined elsewhere in same file
↓ Pull L3: Read config block containing both references
✓ Success: Understand dependency chain
```

## Example 6: Multi-Skill Collaboration

**User**: `Extract this PDF invoice data and summarize the costs`

**Collaboration Flow:**

```
[User Request] → [pdf skill processes PDF] → [TokenKiller constrains output]
```

**Behavior:**

1. **pdf skill** activates first (functional priority)
2. **TokenKiller** applies during output generation:
   - Budget: Medium complexity (≤6 tools)
   - Output: Structured summary, not raw text dump
   - L2 evidence only (file names, key values, not full content)

**Output (Example):**

- **Conclusion**: Invoice contains 5 line items, total $12,450
- **Evidence**: `invoice.pdf` (pages 1-2), extracted line items in table format
- **Changes**: None
- **Next Step**: Export to CSV if needed

**Conflict Resolution:**

- User explicitly asks for full text → User priority, TokenKiller yields
- No explicit request → TokenKiller applies summary format

## Anti-Patterns: Easy Ways to Burn Tokens (Avoid)

- Reading through entire project structure at the start, reading all config files
- Copy-pasting entire build logs
- Repeatedly pasting/explaining the same information
- Reading >500 line files in full without sectioning
- Outputting complete file contents instead of diffs
- Listing entire directory trees instead of target paths