# Multi-Tenancy — Isolation, Noisy Neighbours and Tenant Lifecycle

Scope: the tenancy decisions a SaaS business lives with — isolation model, tenant identity, per-tenant operations, residency, offboarding. Cloud infrastructure itself is `aws` and `k8s`; per-tenant cost is `margins.md`.

**Before answering an isolation, residency or single-tenant request**, read `## Commitments` in `~/Clawic/data/saas/memory.md` (or `commitments.md`) for residency and isolation promises already made, and any tenancy decision in `artifacts/`. Isolation promises are irreversible in practice: they constrain every future architecture decision, so the record of what has already been promised is a hard input.

## The Three Models

| Model | Isolation | Cost per tenant | Operational load | Sell it when |
|---|---|---|---|---|
| Pool (shared everything, tenant column) | Logical only | Lowest | One deployment, one upgrade | Default for everything below enterprise |
| Bridge (shared compute, tenant-per-schema or per-database) | Data separated, compute shared | Moderate | One deployment, N migrations | Enterprise data-separation requirement, or a noisy-neighbour problem at the data layer |
| Silo (dedicated stack per tenant) | Full | Highest | N deployments, N upgrades, N on-call surfaces | Contractual isolation, residency you cannot meet otherwise, or regulated workloads |

- **Default to pool** and move individual tenants up the ladder rather than moving everyone. A mixed estate is normal and correct; a company that siloes everyone because one buyer asked has multiplied its operational cost by its customer count.
- **Price the silo to cover the operational tax explicitly** — deployment, upgrade, monitoring, on-call, and the version skew that follows. A silo sold at pooled prices converts every new enterprise customer into a permanent tax on engineering.
- **Version skew is the hidden cost of silo.** Without a written policy — a maximum number of versions behind, with a forced-upgrade window — the estate diverges until every fix has to be backported to a dozen variants.
- Bridge is the most underused option: it satisfies most "our data must be separate" requirements without the operational cost of silo, because compute and deployment stay shared.

## Tenant Identity Discipline

The bugs that end companies in this domain are cross-tenant data leaks, and they come from a tenant id that is optional somewhere.

- **Tenant id on every row, every request, every log line, every background job, every event.** Optional anywhere means missing eventually.
- **Enforce at the lowest layer available**, not in application code: row-level security in the database, or a repository layer that physically cannot construct an unscoped query. A convention that every query must include the tenant filter is a convention that will be broken by a new hire in month two.
- **Deny by default in tests.** A test suite that runs as a superuser proves nothing about isolation; run integration tests as the tenant-scoped role.
- **Background jobs and scheduled work carry the tenant explicitly** — never inferred from the last request or from ambient state. Cross-tenant leaks disproportionately originate in async paths.
- **Admin and impersonation paths are the exception that must be audited.** Every support impersonation is logged with who, which tenant, when and why, and it is visible to the customer in their audit log if they have one (`enterprise.md`).
- **Cross-tenant queries exist** — analytics, billing, admin. Isolate them in a separately reviewed module with a name that makes their danger obvious, rather than allowing an unscoped query anywhere in the general codebase.

## Noisy Neighbours

Pooled tenancy means one customer's behaviour is another's latency.

| Symptom | Usual cause | Control |
|---|---|---|
| Latency spikes correlated with one tenant | An unbounded query or import from a large account | Per-tenant query timeouts and result-size limits |
| Queue starvation | One tenant enqueues a bulk job of a million items | Per-tenant concurrency caps and fair scheduling, not a single FIFO queue |
| Connection exhaustion | One tenant's traffic burst | Per-tenant rate limits at the edge, with limits sized per plan |
| Storage or index bloat | One tenant with orders of magnitude more data | Detect the outlier early; that tenant is a bridge or silo candidate |
| Cost spike with no revenue change | The same outlier | The margin analysis finds it first (`margins.md`) |

Instrument every one of these per tenant. Aggregate dashboards hide exactly the distribution that matters, and the outlier tenant is usually visible weeks before it causes an incident.

## Provisioning and Offboarding

Both directions must be a single automated operation. Manual tenant creation guarantees drift; manual deletion guarantees a compliance problem.

**Provisioning**: tenant record, isolated storage or schema, default entitlements from the plan (`entitlements.md`), admin user, audit-log stream, monitoring and cost tags, and the sample data that makes the first session productive (`trials.md`).

**Offboarding**, which almost nobody builds until forced:

- **Export before deletion**, in a documented machine-readable format, available self-serve. Data portability is a GDPR right and, independently, the thing that makes buyers comfortable signing (`compliance.md`).
- **Deletion is a defined, timed process**: soft-delete with a stated retention window, then hard delete across primary storage, replicas, search indexes, caches, object storage, analytics warehouse and backups-per-policy. Enumerate every store; the forgotten one is always the search index or the warehouse.
- **Backups are the honest exception**: state the backup retention period in the DPA rather than claiming instant erasure you cannot perform.
- **Deletion produces a certificate** — what was deleted, when, from where. Enterprise buyers ask for it and it costs nothing to generate if the process is automated.

## Residency and Regions

- Residency is a commitment with an architecture behind it: data at rest, backups, logs, analytics, support tooling and any subprocessor must all respect it. Teams routinely satisfy the first and fail on logs or the warehouse.
- **Sell residency as an enterprise-tier capability with its own price**, because it multiplies deployment and operational surface exactly like silo tenancy does.
- Every residency promise is a row in `## Commitments`, and every region added is a subprocessor and DPA update (`compliance.md`).
- Region migration for an existing tenant is a project, not a setting: plan it as an export, import, verify and cut-over with downtime stated in advance.

## Tenant-Aware Operations

- **Migrations run per tenant in bridge and silo**, which means a migration runner with progress, resumability and per-tenant failure isolation. One failed tenant must not block the other 400.
- **Feature flags are tenant-scoped**, so a rollout is a percentage of tenants rather than a percentage of requests — a request-scoped rollout gives a single customer an inconsistent product.
- **Per-tenant observability**: error rate, latency and cost filterable by tenant, or "is it just them?" cannot be answered during an incident.
- **Status and incident scope** stated per region or tenant group where the architecture allows. Telling every customer that everything is down when one shard is affected costs credits and trust unnecessarily (`incidents/<year>.md`).

**After any tenancy decision, isolation grant or residency promise**, write the decision with its alternatives and numbers to `artifacts/<kebab-name>.md` with its `## Boxes` line, and the customer-specific promise — isolation level, region, deletion window — to `## Commitments` with its expiry, in the same turn (`memory-template.md`). Tenancy is the decision most often re-argued and least often documented, and reversing it after the fact is a migration project per customer.
