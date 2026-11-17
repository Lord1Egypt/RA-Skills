# State — Backends, Locking, and Environment Layout

State is not a cache. It holds the only link between a resource address in your code and the real object's ID, plus values the API will never return again (generated passwords, one-time tokens). Losing it does not lose the infrastructure — it loses your ability to manage it.

## Backend Choice

| Backend | Locking | Undo | Notes |
|---|---|---|---|
| S3 | Native via `use_lockfile = true` (terraform >=1.10) — a `.tflock` object beside the state | Bucket object versioning | DynamoDB table no longer required on current versions; keep it only for older CLIs in the same bucket |
| GCS | Built in | Object versioning | Enable versioning explicitly; it is not on by default |
| azurerm | Blob lease | Blob versioning / soft delete | Lease survives a killed process until it expires |
| Managed platform (HCP/TFC and equivalents) | Built in, with audit | Versioned state history in the UI | Also solves credential custody; costs a vendor dependency |
| `http` | Depends entirely on the server | Depends on the server | Verify the implementation actually locks before trusting it |
| `local` | File lock only | Whatever your laptop backup is | Throwaway experiments only |

Every remote backend needs three things enabled on day one: **locking, versioning, and encryption at rest**, plus an access policy where the pipeline role can write and almost nobody can read.

## The Backend Block Cannot Take Variables

No variables, no locals, no interpolation — the backend is resolved before anything else exists. The supported pattern is partial configuration:

```hcl
terraform { backend "s3" {} }        # empty block, everything passed at init
```

```bash
terraform init -backend-config=env/prod.s3.tfbackend -input=false
```

One root module then serves every environment without CLI workspaces. Keep one `.tfbackend` file per environment next to the code, and the credentials for each in a different role.

## Environment Layout

| Layout | Use when | Cost |
|---|---|---|
| Directory (or repo) per environment, separate backend key and separate cloud role | Default | Duplicated backend and provider blocks |
| CLI workspaces | Short-lived parallel copies of the *same* stack — a per-PR sandbox, a spike | One backend, one credential set, and the active workspace is invisible CLI state |
| Separate accounts/projects per environment | Blast-radius or compliance separation is a requirement | Cross-environment changes need one PR per environment |
| else | Directory per environment | — |

CLI workspaces are a fine tool used for what they are: they share the backend and the credentials, so they cannot separate production from anything. With S3 they key state at `env:/<workspace>/<key>` — useful to know when you go looking for a workspace's state object.

## Splitting State by Blast Radius

Split along "what changes together", not along the org chart: network, data, application tiers. Signals to split, in order of how often they decide it:

- Unrelated teams queue behind one lock.
- Plans you stop watching (~3 min+, typically 300-500 resources in one state).
- One stack's failure blocks an unrelated stack's release.
- Different blast radius: a state that can delete a database should not also hold a feature flag.

One state = one lock = one apply unit. That is the whole cost model.

## Cross-State References

- `terraform_remote_state` exposes only root outputs *in config*, but the reader needs read access to the **entire** state file — every secret in it included. That is the reason to avoid it, not performance.
- Preferred: the producing stack writes values to a parameter store or secret manager; consumers read them via a data source, scoped per key by IAM.
- Either way you have created an ordering dependency between two pipelines that nothing enforces. Write it down in both repos, and make the consumer fail loudly (`precondition` on the data source) rather than plan with a stale value.

## Locking Mechanics

- The lock error prints ID, Who, Created, Operation, and Path. Those five fields decide whether you are looking at a live apply or a dead job.
- `-lock-timeout=5m` makes a queued CI job wait instead of failing. Set it once via `TF_CLI_ARGS_plan` / `TF_CLI_ARGS_apply`.
- `-lock=false` is for read-only inspection of a state you know nobody is writing. It is also a lie that the next person believes; never in a pipeline.
- `force-unlock` is a recovery action with preconditions, routed from SKILL.md Quick Reference.

## Moving State Between Backends

```bash
terraform state pull > backup-$(date +%s).tfstate          # always first
terraform state list | wc -l                                # record the count
# edit the backend block / swap the .tfbackend file
terraform init -migrate-state
terraform state list | wc -l                                # must match
terraform plan                                              # must be zero-diff
```

A mismatched count or a non-empty plan means the migration copied the wrong state — stop before applying anything.

## Splitting One State Into Two

Two paths. Prefer the first.

1. **Declarative (reviewable, replayable):** add `removed` blocks with `destroy = false` in the source root and `import` blocks in the destination root. Apply the source removal first, then the destination import. Between the two applies the objects are unmanaged and still running — that is safe; being managed twice is not.
2. **Surgical (local files only):** `terraform state mv -state=src.tfstate -state-out=dst.tfstate <addr>` works on pulled files, not on remote backends. Pull both, move, push both, then plan both to zero diff. Use when the addresses are too broken for `import` to express.

## Serial, Lineage, and Push Safety

- Every write increments `serial`; `lineage` is a UUID identifying the state's ancestry.
- `terraform state push` refuses a state with a lower serial or a different lineage. `-force` overrides both checks and is almost always the wrong answer — the exception is a deliberate restore where you know which snapshot describes reality.
- Quick triage of any state file you are holding: `jq '.serial, .lineage, (.resources | length)' file.tfstate`.

## State Hygiene

- Gitignore `*.tfstate*` and `.terraform/`. Commit `.terraform.lock.hcl`.
- Do not put large blobs in resources that store their content in state (file contents, certificates, rendered documents): every plan pulls and every apply pushes the whole file.
- Secrets in state are unavoidable, not acceptable by default — the containment measures are in `secrets.md`.
- Audit who can read the state bucket the same way you audit who can read production credentials, because it is the same list.
