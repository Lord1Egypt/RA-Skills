# Error Resolution Decision Tree

This decision tree provides a structured, step-by-step process for handling errors encountered during any phase. Each step produces a diagnostic output that informs the next step. Following this tree ensures errors are captured completely, classified accurately, and resolved at the root cause rather than the symptom.

## Why a Decision Tree Exists

When an error occurs, the immediate impulse is to fix the visible symptom. This approach fails when the symptom is caused by a deeper issue — fixing the symptom masks the problem, which resurfaces later in a different form. The decision tree enforces a diagnostic sequence: capture first, classify second, diagnose third, fix fourth, verify fifth. This sequence prevents premature fixes and ensures the full error context is available at every decision point.

---

## STEP 1: Capture the Error

When any error is detected, stop all work and complete these actions before attempting a fix.

**Actions:**
1. Record the exact error message — paste it verbatim, do not summarize.
2. Record the stack trace if one is available.
3. Check `/home/z/my-project/dev.log` for additional context — read the file directly to inspect recent errors and server output.
4. Record what the agent was doing when the error occurred (which phase, which Traceability ID, which command).
5. Open the incident report template (`procedure/templates/incident-report.md`) and fill in the "Error Capture" section.

**Output:** A completed Error Capture section in the incident report.

**Decision:** Proceed to STEP 1.5.

---

## STEP 1.5: Denial Delta Analysis

Before classifying the error, check if it's a **denial-type error** — an error message that explicitly names a missing capability, permission, or resource. If so, perform a systematic comparison between what was denied and what is currently configured. The difference IS the fix.

**Why this step exists:** Without delta analysis, agents pattern-match symptoms to assumed solutions, guess at fixes, and burn debug cycles. A 10-second field-by-field comparison can prevent hours of trial-and-error.

### When to Apply

Apply delta analysis when the error message fits this pattern:

> "X was denied because Y is missing/not granted/not configured"

Common indicators:
- `denied`, `EPERM`, `EACCES`, `Permission denied`
- `not allowed`, `forbidden`, `unauthorized`
- `missing`, `not found` (in policy/config context)
- `ERROR 1142` (database), `DENIED` (AppArmor), `avc: denied` (SELinux)

If the error does NOT fit this pattern (e.g., `TypeError`, `SyntaxError`, crash), skip to STEP 2.

### How to Perform Delta Analysis

1. **Extract denied fields** from the error message:
   - What capability/permission/resource was denied?
   - Who is the source (user, process, domain, role)?
   - What is the target (file, directory, service, table)?
   - What class/type/category is involved?

2. **Find the corresponding configuration** that controls this capability:
   - Search the config file, policy file, or permission system that grants or denies this capability
   - Use the source + target + class fields to locate the specific rule

3. **Compute the delta** — compare what was denied vs what is configured:
   ```
   Denied:     { permission_A, permission_B }
   Config has: { permission_A, permission_C }
   Delta:      { permission_B }  ← THIS IS THE FIX
   ```

4. **Act on the delta**:
   - **Delta is non-empty** → The fix is to add the missing capability to the existing config. This is a **Bug** (incomplete configuration), NOT a Wrong Approach. Skip Pivot protocol. Go directly to STEP 3 with the specific missing item.
   - **Delta is empty** (all denied capabilities ARE in the config) → The config exists but isn't being applied. This is a **deployment issue** (stale cache, precompiled policy, wrong config loaded, etc.). Proceed to STEP 2 for normal classification.

### Domain Examples

| Domain | Error Pattern | Config Source | Delta = Fix |
|--------|--------------|---------------|-------------|
| SELinux | `avc: denied { create }` | CIL allow rules, `sesearch` | Missing permission in allow rule |
| Linux capabilities | `EPERM` on syscall | `capsh --print`, Docker `--cap-add` | Missing capability |
| File permissions (DAC) | `Permission denied` | `ls -l`, `stat`, ACL | Missing rwx bit or ACL entry |
| Firewall | Connection refused/timeout | `iptables -L -n`, `ufw status` | Missing ACCEPT rule |
| AppArmor | `DENIED` in audit log | AppArmor profile | Missing rule in profile |
| Database grants | `ERROR 1142: SELECT denied` | `SHOW GRANTS FOR user` | Missing GRANT statement |
| IAM (AWS/GCP) | `AccessDenied` | IAM policy JSON | Missing action in policy statement |
| CORS | `blocked by CORS policy` | Server CORS headers config | Missing origin/header/method |
| Kubernetes RBAC | `forbidden: User cannot X` | Role/ClusterRole YAML | Missing verb in rule |

### Example (SELinux)

```
Error: avc: denied { create } for comm="rsc" scontext=u:r:rsc:s0 tcontext=u:object_r:adb_data_file:s0 tclass=dir

Step 1: Extract
  Denied:     { create }
  Source:     rsc
  Target:     adb_data_file
  Class:      dir

Step 2: Find rule
  grep "allow.*rsc.*adb_data_file" vendor_sepolicy.cil
  → (allow rsc adb_data_file_30_0 (dir (search write add_name)))

Step 3: Delta
  Denied:     { create }
  Rule has:   { search, write, add_name }
  Delta:      { create }  ← MISSING

Step 4: Delta non-empty → Bug (incomplete rule). Fix: add 'create' to dir permissions.
  Skip Pivot. Go to STEP 3.
```

**Cost**: 10-30 seconds. **Benefit**: prevents guessing, false pivots, and multi-hour debug sessions.

**Output:** Either (a) a specific missing capability to add (go to STEP 3), or (b) confirmation that config is correct but not applied (go to STEP 2).

**Decision:** If delta found → STEP 3 (Recovery Actions with specific fix). If delta empty or N/A → STEP 2 (Classify).

---

## STEP 2: Classify the Error

Use the error message and context to classify the error into one of the categories below. The classification determines the diagnostic path.

### Classification Table

| Category | Indicators | Reference |
|----------|-----------|-----------|
| **Wrong Approach** | Fix requires rewriting 50%+ of implementation, same error recurs after 2 fix attempts, required feature doesn't exist in chosen library/framework | See Pivot Assessment below |
| **Compilation / Syntax** | `SyntaxError`, `Unexpected token`, `cannot find module`, build fails | `knowledge/universal/conventions.md` (import rules, file extensions) |
| **Type** | TypeScript error (`TSxxxx`), `Type 'X' is not assignable to type 'Y'`, type mismatch | `knowledge/universal/conventions.md` (type constraints, `unknown` vs `any`) |
| **Runtime** | `TypeError`, `ReferenceError`, `Cannot read properties of undefined`, function crashes | `knowledge/universal/error-patterns.md` (runtime error patterns) |
| **Network / Gateway** | `ECONNREFUSED`, `fetch failed`, `502 Bad Gateway`, CORS error, WebSocket failure | `knowledge/universal/error-patterns.md` (network/gateway section), `knowledge/universal/architecture.md` (service communication), `knowledge/platform/zai-sandbox.md` (gateway routing) |
| **Database / Prisma** | Prisma error, `Unique constraint failed`, `PrismaClient not generated`, query error | `knowledge/universal/error-patterns.md` (database section) |
| **Git / Version Control** | `push rejected`, `fetch failed`, `merge conflict`, `diverged branches`, `non-fast-forward`, `detached HEAD` | This section (see Git diagnostic path below) |
| **AI / SDK** | SDK invocation failure, rate limit, timeout, model error, image generation failure, `z-ai-web-dev-sdk` runtime error | See AI/SDK diagnostic path below |
| **Other** | Error does not match any category above | Isolate minimal reproduction (see below) |

### Pivot Assessment (Wrong Approach)

Before following any diagnostic path, determine if the error is a **Bug** or an **Wrong Approach**. This classification changes the entire recovery path.

**Pivot Assessment criteria**:

| Signal | Type | Explanation |
|--------|------|-------------|
| Fix requires rewriting 50%+ of implementation | Wrong Approach | The fundamental design is wrong — patching won't help |
| Same error recurs after 2 fix attempts | Wrong Approach | Fixing symptoms, not root cause — escalation needed |
| Fix requires changing data model / API contract | Wrong Approach | Architecture assumption was invalid |
| Required library/framework feature doesn't exist | Wrong Approach | SADC miss — the chosen approach is infeasible |
| Simple typo, wrong variable, missing null check | Bug | Normal implementation error — proceed to diagnostic path |
| Type mismatch, import error, lint violation | Bug | Normal implementation error — proceed to diagnostic path |

**If Wrong Approach is detected**:

1. **Stop fixing immediately** — do not attempt a third fix attempt on the same approach.
2. **Check Scope fallback** — the implementation plan's Fallback Approach field should have a concrete alternative.
3. **Evaluate the fallback** — is it still viable given what was learned from the failure?
4. **Present pivot to user** — explain what failed, why the fallback is better, and what changes.
5. **Re-enter PLAN** — create a new implementation plan using the fallback (or a new approach if fallback is not viable).
6. **Output new Scope** — update the Scope with the new approach.
7. **Re-implement and re-verify** — full cycle from PLAN through DELIVER.
8. **Record Pivot in delivery report** — the Pivot field documents the approach change for audit trail.

### Pivot Backlog Meta-Review (after 3+ back-to-back pivots)

If this is the **3rd or more** back-to-back pivot on the same task (each triggered by a different error), STOP and perform a meta-review before attempting another pivot:

1. **Stop** — do not attempt a 4th pivot yet.
2. **Tally all pivots** with their trigger errors:
   - Pivot 1: <trigger>
   - Pivot 2: <trigger>
   - Pivot 3: <trigger>
3. **Identify meta-pattern** — which pattern best describes the cascade?
   - **Skipped delta analysis** — pivots happened without comparing denied vs configured capabilities (STEP 1.5 was skipped). Ask: "did you compare what was denied against the actual config?"
   - **Documentation lies** — target system doesn't behave per its documentation
   - **Toolchain drift** — local toolchain doesn't match target environment
   - **Symptom cascade** — each pivot fixes a symptom of a deeper, unaddressed issue
   - **Environment mismatch** — sandbox/local doesn't match production constraints
   - **Wrong abstraction level** — pivoting at code level, but the issue is architectural
4. **Re-enter SPECIFY** (not PLAN) — the problem specification itself may be wrong. The meta-pattern suggests the original approach was built on incorrect assumptions.
5. **Surface to user**: "I've pivoted 3 times, each on a different error. The pattern suggests [meta-pattern]. Should we reconsider [higher-level change]?"

**Rationale**: 3+ pivots on different errors is a signal that the overall approach is wrong, not that individual fixes are failing. Continuing to pivot at the same level wastes time. Stepping back to SPECIFY allows re-examining assumptions, not just swapping implementations.

**Output**: Classification as Bug or Wrong Approach. If Wrong Approach, proceed to pivot flow instead of diagnostic path. If 3+ pivots, perform meta-review above.

**Decision**: If Bug → proceed to appropriate diagnostic path below. If Wrong Approach → pivot flow above. If 3+ pivots → meta-review → re-enter SPECIFY.

### Diagnostic Paths by Category

**Compilation / Syntax:**
1. Check file extensions — `.js` files cannot contain JSX; rename to `.tsx`.
2. Check import paths for correct casing (Linux is case-sensitive).
3. Check for missing exports — verify the imported symbol is actually exported from the source file.
4. Check for missing barrel exports — new files may not be added to `index.ts`.

**Type:**
1. Read the exact TypeScript error code and message.
2. Replace any `any` types with proper types or `unknown` with type guards.
3. Check function return types — are they declared and correct?
4. Check optional chaining — is a nullable value being accessed without `?.` or null check?

**Runtime:**
1. Identify the line and column from the stack trace.
2. Check for `undefined` or `null` access — add optional chaining or null checks.
3. Check for missing function arguments or wrong argument order.
4. Check for array/object access with out-of-bounds or missing keys.
5. If the error is intermittent, look for race conditions or timing dependencies.

**Network / Gateway:**
1. Check if the URL uses an absolute `localhost` address — change to relative path with `?XTransformPort=`. Reference `knowledge/universal/architecture.md` for the service communication model and `knowledge/platform/zai-sandbox.md` for gateway routing rules.
2. Check if the target service is running — verify the mini-service or dev server is active.
3. Check for port conflicts — ensure no two services use the same port.
4. Check for CORS errors — these almost always indicate an absolute URL where a relative one is needed.
5. If using `z-ai-web-dev-sdk`, confirm it is only in server-side code, never in client components.

**Database / Prisma:**
1. If schema was changed, run `bun run db:push` to regenerate the client.
2. For unique constraint violations, use `upsert` or check existence with `findFirst` before inserting.
3. Check that query conditions match the schema field names exactly.
4. Verify the Prisma client import path is correct.

**Git / Version Control:**

> **Critical rule**: Never run `git pull`, `git rebase`, `git reset`, `git push --force`, or any destructive git operation without first running `git fetch` and inspecting the state. If remote has diverged from local, **stop and ask the user** — do not attempt automatic resolution. The infrastructure may block git operations, and cascading git commands can leave the agent completely paralyzed.

1. **On `git push` rejected (remote has diverged):**
   a. Run `git fetch origin` to see what changed on the remote.
   b. Run `git log HEAD..origin/<branch> --oneline` (use the current branch name) to inspect the divergent commits.
   c. Present the situation to the user: "Remote has N commits ahead of local. [Summarize what changed]. How would you like to proceed?"
   d. **Do NOT** run `git pull`, `git rebase`, or `git merge` without explicit user instruction.
   e. If the user asks you to resolve it, follow their specific instruction. If they say "rebase", confirm before executing.
2. **On merge conflict during any operation:**
   a. Do NOT run `git rebase --abort`, `git merge --abort`, or `git reset --hard` without user approval.
   b. Present the conflicting files to the user and ask how to resolve each conflict.
   c. If git commands are being blocked by infrastructure, inform the user immediately — do not attempt alternative commands.
3. **On `git push --force` consideration:**
   a. Force push is almost never appropriate in collaborative repositories.
   b. If the user requests it, warn them about the consequences (overwriting remote history).
   c. Do not suggest force push as a resolution option unless the user explicitly asks for it.
4. **On git operations being blocked by infrastructure:**
   a. Stop all git operations immediately.
   b. Inform the user that the infrastructure is blocking git commands and that manual intervention is required.
   c. Do NOT attempt alternative escalation commands (`rm -rf .git`, `git checkout --theirs`, etc.).
5. **On stale-data analysis detected (during or after verification):**
   a. Run `git fetch origin && git log HEAD..origin/<branch> --oneline` to identify missed commits.
   b. Run `git pull` (or `git checkout <branch>` after fetch) to synchronize.
   c. Re-read all affected files from the updated working tree.
   d. Re-perform the analysis on the current files.
   e. If the analysis output was already delivered to the user, issue a correction immediately with the updated findings.
   f. Return to VERIFY phase and complete a new verification report reflecting the corrected state.

**AI / SDK:**
1. If `z-ai-web-dev-sdk` error occurs in client-side code — the SDK must only run in server-side code (API routes, server actions). Move the invocation to a server-side endpoint.
2. For rate limiting or timeout errors — add retry logic with exponential backoff, or simplify the request (shorter prompt, fewer tokens).
3. For image generation failures — verify the `size` parameter is one of the supported values (1024x1024, 768x1344, 864x1152, etc.). Check that the output path is valid.
4. For web search failures — check network connectivity; the search function requires internet access through the platform gateway.
5. If the SDK environment is unavailable — stop and inform the user. The SDK requires specific platform environment variables that may not be present in all contexts.

**Other:**
1. Isolate a minimal reproduction — reduce the failing code to the smallest possible case that still produces the error.
2. Check if the error is reproducible or intermittent.
3. If reproducible, add logging or defensive checks to narrow down the failure point.
4. If the error remains unclear after isolation, present the minimal reproduction and full context to the user and ask for guidance.

**Output:** Error classification and the result of the diagnostic path. Fill in the "Root Cause Analysis" section of the incident report.

**Decision:** Proceed to STEP 3.

---

## STEP 3: Identify Recovery Actions

Based on the root cause, list all actions needed to fix the error.

**Actions:**
1. List each action required to resolve the root cause.
2. For each action, evaluate whether it has side effects. Side effects include:
   - File deletion or renaming
   - Git history changes (rebase, reset, force push)
   - Data loss (database records, configuration values)
   - Configuration changes that affect other parts of the system
   - Installing or removing shared dependencies
   - Changes to behavior in unrelated components
3. If ANY action has side effects, user approval is required before proceeding. Present the proposed actions and their side effects to the user.
4. If NO actions have side effects, the fix may be applied without asking.

**Output:** A list of recovery actions with side-effect assessments. Fill in the "Proposed Fix" section of the incident report.

**Decision:** If user approval is required, wait for confirmation. If not, proceed to STEP 4.

---

## STEP 4: Apply the Fix

Execute the planned fix with precision.

**Actions:**
1. Apply the fix that addresses the root cause — not the symptom.
2. If the fix involves code changes, annotate the changed code with the incident context (e.g., a comment referencing the error and the reason for the fix).
3. Verify the fix does not introduce new errors by running the same command or operation that originally failed.
4. Fill in the "Resolution" section of the incident report with what was actually done.

**Output:** Fix applied and confirmed to resolve the original error. Completed Resolution section.

**Decision:** Proceed to STEP 5.

---

## STEP 5: Return to VERIFY Phase

After applying a fix, full verification is required to confirm nothing else was broken.

**Actions:**
1. Return to the VERIFY phase (even if the error occurred during IMPLEMENT).
2. Complete the full verification report (`procedure/templates/verification-report.md`):
   - Run all automated checks (lint, type check, tests).
   - Verify all Traceability IDs, including those affected by the fix.
   - Re-test all edge cases.
3. Do not skip any verification items. A fix that resolves one issue but breaks another is not a successful fix.
4. If the verification report shows all items passing, proceed to DELIVER.
5. If the verification report shows new failures, return to STEP 1 with the new error.

**Output:** Completed verification report confirming the fix is sound.

**Decision:** If all checks pass, transition to DELIVER. If new failures appear, loop back to STEP 1.

---

## Quick Reference: Return Phase Decision

| Error During | Root Cause Is | Classification | Return To |
|-------------|---------------|---------------|----------|
| SPECIFY | Incomplete requirements | — | SPECIFY (update spec) |
| PLAN | Specification gap or wrong approach | — | SPECIFY or PLAN |
| IMPLEMENT | Code defect | Bug | VERIFY (re-verify after fix) |
| IMPLEMENT | Fundamental design wrong | Wrong Approach | PLAN (pivot with fallback or new approach) |
| IMPLEMENT | Specification gap | Wrong Approach | SPECIFY (update spec, re-plan) |
| VERIFY | Code defect not caught by self-review | Bug | IMPLEMENT (fix, then VERIFY) |
| VERIFY | Specification gap | Wrong Approach | SPECIFY (update spec, re-plan, re-implement) |

When uncertain, return to SPECIFY. It is safer to re-confirm requirements than to fix code against a misunderstood specification.
