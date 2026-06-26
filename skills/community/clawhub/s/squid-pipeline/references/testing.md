# Testing Reference

## YAML Test File Format

Create `pipeline.test.yaml` alongside `pipeline.yaml`:

```yaml
pipeline: ./pipeline.yaml          # REQUIRED — relative to test file

tests:
  - name: "test name"              # REQUIRED
    mode: sandbox                   # sandbox (default) | integration
    args: { key: value }           # pipeline args
    env: { KEY: value }            # env overrides
    mocks:
      run:
        stepId:
          output: { key: value }   # mock output
          stdout: "raw text"       # raw stdout (optional)
          status: completed        # completed (default) | failed
          error: "message"         # error when status: failed
      spawn:
        stepId:
          output: { key: value }
          status: accepted         # accepted (default) | error
          error: "message"
    gates:
      stepId: true                 # true = approve, false = reject
    assert:                         # REQUIRED
      status: completed            # completed | failed | halted | cancelled
      output: { key: value }      # pipeline final output (exact match)
      steps:
        stepId: completed          # status shorthand
        stepId: { status: completed }       # status object
        stepId: { output: { k: v } }        # exact output match
        stepId: { outputContains: "text" }  # substring match
        stepId: { outputPath: field.nested, equals: value }  # nested field
```

## Test Modes

| Mode | `run` steps | `spawn` steps | `gate` steps | Use case |
|------|------------|---------------|--------------|----------|
| **sandbox** | Mocked (nothing runs) | Mocked | Mock decisions | Unit test logic, conditions, data flow |
| **integration** | Execute for real (unless mocked) | Mocked | Mock decisions | Test actual shell scripts |

## Execution Modes (all)

| Mode | run | spawn | gate | How |
|------|-----|-------|------|-----|
| `run` | Execute | Real agent | Halt | `squid run pipeline.yaml` |
| `dry-run` | Skip | Skip | Skip | `squid run --dry-run` |
| `test` | Execute | Mocked | Auto-approve | `squid run --test` |
| `sandbox` | Mocked | Mocked | Mocked | `squid test` (YAML tests) |
| `integration` | Execute | Mocked | Mocked | `squid test` (YAML tests) |

## Mocking Details

**Sandbox mode**: all `run` steps return `{ sandbox: true }` unless explicitly mocked.

**Integration mode**: `run` steps execute for real UNLESS you mock them. Mock specific dangerous commands while letting safe ones run.

**Spawn**: always mocked in both modes. Unmocked spawns return `{ mocked: true }`.

**Gates**: unmocked gates auto-approve. Set `gates: { stepId: false }` to reject.

## CLI

```bash
squid test                          # auto-discovers *.test.yaml
squid test deploy.test.yaml         # specific file
```

## TypeScript API

```typescript
import { createTestRunner } from "squid/testing";
import { parseFile } from "squid";

const result = await createTestRunner()
  .mockSpawn("agent", { output: { score: 95 } })
  .approveGate("gate")
  .rejectGate("dangerous")
  .overrideStep("external", { status: "completed", output: { ok: true } })
  .withArgs({ env: "test" })
  .withEnv({ API_KEY: "test" })
  .run(parseFile("pipeline.yaml"));

// Assertions
result.assertStepCompleted("deploy");
result.assertStepSkipped("rollback");
const review = result.getStepResult("reviewer");
expect(review?.output).toEqual({ score: 95 });
expect(result.capturedSteps.map(c => c.step.id)).toEqual(["build", "test", "deploy"]);
```

## Example: Multi-Agent Pipeline Test

```yaml
pipeline: ./multi-agent.yaml
tests:
  - name: "full happy path"
    mode: sandbox
    args: { feature: "auth", repo: /workspace }
    mocks:
      spawn:
        architect: { output: { plan: "JWT auth", files: ["auth.ts"] } }
        coder: { output: { files: ["src/auth.ts"] } }
        reviewer: { output: { criticalIssues: 0, summary: "LGTM" } }
      run:
        tests: { output: { passed: true } }
    gates:
      plan-review: true
      deploy: true
    assert:
      status: completed
      steps:
        architect: completed
        coder: completed
        reviewer: completed

  - name: "plan rejected stops everything"
    mode: sandbox
    mocks:
      spawn:
        architect: { output: { plan: "bad plan" } }
    gates:
      plan-review: false
    assert:
      status: completed
      steps:
        coder: skipped
```

## Tips

1. Start with **sandbox** — test logic first, then add integration tests
2. Test **happy path** first — all spawns succeed, all gates approved
3. Test **rejection paths** — reject gates, verify conditional skips
4. Test **error handling** — mock steps as `status: failed`, verify branch routing
5. Test **restart loops** — mock improving scores across iterations
6. Mock only what's needed — unmocked steps have sensible defaults
7. Keep test files next to pipelines — `deploy.yaml` + `deploy.test.yaml`
