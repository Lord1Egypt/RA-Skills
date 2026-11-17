# Debugging — Plan and Apply Errors, Symptom to Cause

Work symptom-first. Each chain is ordered by probability and every step is a check, not a guess.

## The Universal First Three

1. **Read the address, not just the message.** Terraform prints `file:line` and the full resource address (`module.net.aws_subnet.this["b"]`). The module path tells you who wrote the block — often not the file you just edited.
2. **`terraform validate`** (needs `init`, no credentials). Passes → the config is type-correct and the problem lives in state, the provider, or the cloud. Fails → you have a config bug and no API call has happened yet.
3. **`TF_LOG=DEBUG TF_LOG_PATH=tf.log terraform plan`**, then grep for the resource address or the API action. `TF_LOG_PROVIDER=TRACE TF_LOG_CORE=WARN` isolates the provider from core. The log contains request and response bodies — treat the file as a credential and delete it.

## Permanent Diff (the plan never converges)

1. Name the attribute. `terraform state show <addr>` versus the real object: which side is wrong?
2. Find the writer. Autoscaler, console operator, another pipeline, a platform agent, or the provider's own defaulting. `terraform apply -refresh-only` then a fresh plan tells you whether the value comes back on its own.
3. Suspect normalization before suspecting a human: providers canonicalize case, JSON key order, ARN vs bare name, empty string vs null, and policy document whitespace. Write the config in the canonical form the API returns — `jsonencode()` on policy documents removes an entire class of these.
4. Ordering-only diffs on a list mean the API returns a set. If the provider offers a set-typed alternative argument, use it; otherwise sort the config to match.
5. Only then `ignore_changes = [that_exact_attribute]`, with a comment naming the writer. Never `all` (`lifecycle.md`).
6. Still churning after a clean apply → the "inconsistent result" family below.

## "Invalid for_each argument" / "Invalid count argument"

The message: *the "for_each" value depends on resource attributes that cannot be determined until apply*.

- The rule: **keys** must be known at plan time; values may be unknown. `for_each = var.subnets` is fine. `for_each = toset(aws_subnet.this[*].id)` is not.
- Fix hierarchy:
  1. Key on the input that produced the resources — you almost always already have that map. Reference the unknown attribute inside the body: `for_each = var.subnets` then `subnet_id = aws_subnet.this[each.key].id`.
  2. Move the unknown into a value: `for_each = { for k, v in var.zones : k => { az = v, id = aws_subnet.this[k].id } }`.
  3. Two-phase apply with `-target` on the producing resource, then a full plan. Last resort, and it leaves a partially applied graph.
- `depends_on` does not help — it changes ordering, not knowability.
- `count` fails the same way when the *number* is unknown: `count = length(data.x.y.ids)` where the data source resolves at apply. `length(var.list)` is always known.
- A sensitive value cannot be a key either: the error names sensitivity, not unknownness. Wrap with `nonsensitive()` only if the key itself is genuinely not a secret.

## "Error: Cycle: ..."

- The error lists every node in the loop. The usual shape is two resources referencing each other inline — the canonical example is two security groups each allowing the other.
- Fix: pull the edge out into a standalone rule/attachment/association resource so the graph becomes A → rule ← B instead of A ↔ B.
- `create_before_destroy` also manufactures cycles: it propagates to everything the resource depends on, and meets a `depends_on` pointing the other way. Removing an unnecessary `depends_on` usually breaks the loop.
- Visual: `terraform graph -type=plan | dot -Tsvg > graph.svg`. Faster in practice: grep the cycle members from the error and open only those blocks.

## "Provider produced inconsistent final plan" / "...inconsistent result after apply"

Always a provider bug — core caught the provider returning a value it did not promise at plan.

1. Upgrade the provider to the newest patch of your major; most of these are fixed within a release or two.
2. Search the provider's issue tracker for the attribute name in the error, not for the error text.
3. Pin the last known-good version with a comment linking the issue.
4. Interim workaround: drop the attribute from config and let the provider default it, or `ignore_changes` on that attribute.

## Authentication and Permission Errors

- Timing tells you the layer: data sources fail at plan, resources at apply. A plan that fails on credentials never reached your config.
- Multi-provider configs: `terraform providers` prints the resolved provider tree per module — confirm the alias you think you passed actually reached the resource (`providers.md`).
- "AccessDenied" on one resource type only = an IAM gap, not a Terraform problem; the log line shows the exact API action to add.
- Short-lived credentials expiring mid-apply leaves a half-applied change. Re-authenticate and re-plan; the plan is now the truth.

## Apply Failed Partway

- Terraform persists state after each resource completes. Created objects are in state even though the apply errored. **The next plan is the source of truth** — run it before touching anything.
- Provider crashed between the API call and the state write → the object exists in the cloud but not in state. Plan wants to create it, apply fails with "already exists". Adopt it with an `import` block (`refactoring.md`).
- Failure mid-replace leaves a tainted or deposed object; those are recovery playbooks, routed from SKILL.md Quick Reference.
- Never re-run a failed apply with `-refresh=false`: you would plan against a state that predates the damage.

## "Saved plan is stale"

Someone applied between your plan and your apply. There is no flag that makes the old plan safe — re-plan, re-review, re-apply. If this happens routinely, two pipelines share one state without a concurrency group (`ci.md`).

## Init and Backend Errors

- **"Backend initialization required"** after changing the backend block. Two different answers: `init -migrate-state` copies the existing state into the new backend; `init -reconfigure` forgets the old backend and starts empty. Choosing `-reconfigure` by reflex against a fresh bucket gives you an empty state and a plan that wants to create your entire estate — stop, do not apply, and re-point at the old backend.
- **"Inconsistent dependency lock file"**: config requires a provider the lock does not record. `terraform init -upgrade` locally, then commit the lock. In CI use `init -lockfile=readonly` so this fails loudly instead of silently rewriting the lock (`providers.md`).
- **"Error acquiring the state lock"**: read the ID, Who, Created, and Operation fields printed with it before doing anything (`recovery.md`).

## Timeouts and Slow Applies

- "timeout while waiting for state to become available" is the cloud's clock, not Terraform's. Raise it where the resource declares a `timeouts` block (`timeouts { create = "60m" }`); resources that do not declare one reject the block outright.
- The same resource type timing out repeatedly is capacity or quota, not configuration.
- Slow but progressing is a different problem — `performance.md`.

## When You Are Truly Stuck

Reduce to the smallest reproducing case: an empty directory, a local backend, one resource, the same provider version. Reproduces → provider or core bug worth filing, with that directory attached. Does not reproduce → the fault is in your state, your module wiring, or a variable you have not printed yet (`terraform console` evaluates expressions against real state without running a plan).
