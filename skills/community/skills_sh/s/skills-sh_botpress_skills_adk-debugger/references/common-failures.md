# Common Failure Patterns

Each pattern follows: **Symptom → How to Check → Root Cause → Fix**.

Use `--format json` on diagnostic CLI commands that support it for structured, parseable output.

---

## 1. Project Won't Validate

**Symptom:** `adk check --format json` reports errors before you even run the bot.

**How to check:**

```bash
adk check --format json
```

**Common causes:**

- Missing or invalid `agent.config.ts` fields
- Schema mismatch between action/tool input and output definitions
- Invalid entity names (too long or contains invalid characters)
- Missing dependency (integration not added with `adk integrations add`)
- Import from wrong source (e.g., importing from `@botpress/sdk` instead of `@botpress/runtime`)
- Invalid table schema definitions

**Fix:** Read the `adk check` output — it reports the exact file, field, and error. Fix each reported issue and re-run.

**Note:** It does not run full TypeScript type-checking, formatting or linting; that is project specific.

---

## 2. Bot Not Responding

**Symptom:** You send a message but get no reply.

**How to check:**

```bash
# Is the dev server running?
adk logs --format json

# Any startup errors?
adk logs error --format json

# Try sending a test message
adk chat --single "Hello" --format json
```

**Common causes:**

| Cause                      | How to Verify                                                                                                                                                                                |
| -------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| No dev bot created         | Check that `agent.local.json` has `devId` (set automatically on the first `adk dev` run, or manually via `adk link --local`). If missing, run `adk dev` at least once to create the dev bot. |
| Integration not configured | Check Dev Console at localhost:3001 — look for unconfigured integrations                                                                                                                     |

**Fix:** Work through the checklist top to bottom. Most "bot not responding" issues are missing config or a stopped dev server.

---

## 3. Tool Call Errors

**Symptom:** The bot tries to use a tool but it fails, or returns unexpected results.

**How to check:**

```bash
adk traces --format json
```

Look for `tool_call` spans with `success: false`. Some tools could be workflows or actions wrapped as tools: follow the money and find the real source.

**Common causes:**

| Cause                      | Trace Evidence                                        |
| -------------------------- | ----------------------------------------------------- |
| Handler throws an error    | `error` field has the exception message               |
| Input schema mismatch      | `error` mentions validation or type error             |
| Integration auth expired   | `error` mentions 401, unauthorized, or token expired  |
| Missing integration config | `error` mentions missing configuration or credentials |

**Fix:**

- **Handler error:** Read the error message, fix the handler code
- **Schema mismatch:** Compare `input` in the trace against the tool's input schema definition
- **Auth expired:** Reconfigure the integration in the Dev Console (localhost:3001) which must be done interactively
- **Missing config:** Run `adk integrations info <integration> --format json` to see required config, then configure in Dev Console which must also be done interactively

---

## 4. Workflow Stuck

**Symptom:** A workflow starts but never completes, or a step doesn't execute.

**How to check:**

```bash
adk traces --format json
```

Look for workflow-related traces that start but have no completion.

**Common causes:**

- **Step not resuming:** The workflow is waiting for a step that depends on an external event or trigger that hasn't fired
- **`step.sleep()` still waiting:** A sleep step hasn't expired yet — check the duration
- **Missing trigger to continue:** A multi-step workflow needs a trigger (e.g., user message, webhook) to resume after a pause
- **Error in step handler:** A step threw an error silently — check for `code_execution_exception` spans
- **State lost:** Workflow state wasn't persisted correctly between steps

**Fix:** Identify which step the workflow is stuck on, then check that step's handler, triggers, and dependencies.

---

## 5. Integration Failures

**Symptom:** Integration actions fail, events don't fire, or channels don't work.

**How to check:**

```bash
# Check logs for integration errors
adk logs error --format json

# Check traces for failed integration calls
adk traces --format json
```

Also check the Dev Console at localhost:3001 for integration status.

**Common causes:**

| Cause                             | How to Identify                                                     |
| --------------------------------- | ------------------------------------------------------------------- |
| Auth expired or missing           | Error mentions 401, unauthorized, or token                          |
| Rate limited                      | Error mentions 429 or rate limit                                    |
| Wrong config values               | Integration actions fail with config-related errors                 |
| Events not registered in dev mode | Events work in production but not locally — re-run `adk dev`        |
| Channel routing misconfigured     | Messages arrive but aren't routed to the right conversation handler |

**Fix:**

- **Auth:** Reconfigure the integration in Dev Console
- **Rate limits:** Add retry logic or reduce request frequency
- **Config:** Run `adk integrations info <integration> --format json` to verify required fields, update in Dev Console
- **Events in dev:** Restart `adk dev` — event registration sometimes needs a fresh start

---

## 6. Build and Deploy Errors

**Symptom:** `adk deploy` or `adk build` fails.

**How to check:**

```bash
# Always validate offline first
adk check --format json
```

**Common causes:**

- **Import from wrong source:** Using `@botpress/sdk` where `@botpress/runtime` is needed (or vice versa)
- **Schema mismatch:** Action/tool input or output schema doesn't match the handler's actual types
- **Missing dependency:** Integration referenced in code but not added with `adk integrations add`
- **Type errors in generated code:** Usually caused by stale generated types — run `adk build` or re-run `adk dev` to regenerate

**Fix:** Start with `adk check --format json` — it catches most issues offline. For type errors, try deleting `.adk/` and running `adk build` or re-running `adk dev` to regenerate.

---

## 7. Code Execution Exceptions

**Symptom:** The LLMz sandbox throws an error during code execution.

**How to check:**

```bash
adk traces --format json
```

Look for spans with type `code_execution_exception`.

**Key fields:**

- `message` — the error message
- `stackTrace` — full stack trace pointing to the failing line

**Common causes:**

- Undefined variable or function in the generated code
- Async operation that wasn't awaited
- Tool output shape doesn't match what the LLM expected
- Runtime exception in user-defined code called from the sandbox

**Fix:** Read the stack trace. Correlate the line numbers with the generated code or your source. Fix the underlying issue — often a tool's output schema or a missing null check.

---

## 8. Config Confusion: agent.json vs agent.local.json

**Symptom:** Bot connects to the wrong workspace, wrong bot ID, or `adk dev`/`adk chat`/`adk deploy` commands fail unexpectedly.

### How the files work

| File               | Purpose                                                    | Git Status | Created By                                                   |
| ------------------ | ---------------------------------------------------------- | ---------- | ------------------------------------------------------------ |
| `agent.json`       | Primary config: `botId`, `workspaceId`, `apiUrl`           | Committed  | `adk link`                                                   |
| `agent.local.json` | Local overrides: `botId`, `workspaceId`, `apiUrl`, `devId` | Gitignored | `adk dev` or `adk link --local` (sets `devId`), manual edits |

**`agent.local.json` fields take precedence over `agent.json` fields.** If both files define `botId`, the local one wins.

### Common issues

| Issue                                    | Cause                                           | Fix                                                    |
| ---------------------------------------- | ----------------------------------------------- | ------------------------------------------------------ |
| Wrong bot ID used                        | `agent.local.json` overrides `agent.json` botId | Check both files, remove or update the local override  |
| `adk chat` fails with "no devId"         | `adk dev` hasn't been run yet (devId not set)   | Run `adk dev` at least once to create the dev bot      |
| Different behavior on teammate's machine | They have different `agent.local.json`          | Expected — local overrides are per-developer           |
| Deploy targets wrong bot                 | `agent.json` has wrong botId                    | Update `agent.json` via `adk link` or `adk config:set` |

### Checking your config

```bash
# See what's in agent.json
cat agent.json

# See local overrides (if any)
cat agent.local.json
```
