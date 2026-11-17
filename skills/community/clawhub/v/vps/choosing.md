# Choosing a Provider, a Region, and a Plan

Prices and allowances move; the **ratios and the decision order are stable**. Verify the current number on the provider's page before anyone spends money. Every threshold here scales with `monthly_budget`, and `data_residency` filters the shortlist before price is considered.

**Before recommending anything**, read `~/Clawic/data/servers/servers.md` and `## Hosts` in `~/Clawic/data/vps/memory.md`: the user may already run the exact plan being discussed, and the cheapest new server is often an existing one with capacity.

**Contents:** [Decision Order](#decision-order) · [Size From the Binding Constraint](#size-from-the-binding-constraint) · [vCPU Is the Least Useful Number](#vcpu-is-the-least-useful-number) · [ARM Before x86](#arm-before-x86) · [Region](#region) · [The Comparison That Actually Matters](#the-comparison-that-actually-matters) · [Managed Versus Self-Run](#managed-versus-self-run) · [Trial and Exit](#trial-and-exit)

## Decision Order

Wrong order is why comparisons stall on specs. Run it top to bottom and stop as soon as a step eliminates everyone but one:

1. **Jurisdiction and residency.** A contractual requirement kills options no price can revive. Check where the legal entity is, not only where the datacenter is — a US-owned company operating an EU datacenter is a different answer to the same question.
2. **Region and latency to the users.** Distance is the one property you cannot buy your way out of later.
3. **The binding constraint**, usually RAM. See below.
4. **Egress allowance**, then the overage rate. This is where the real difference between providers lives.
5. **Address and add-on charges** — IPv4, backup add-on, snapshot storage.
6. **Plan price.** Last, because by this point there are two candidates and the price gap is usually smaller than the egress gap.
7. **Operational fit** — do they already have an account, and have they ever recovered a box there?

## Size From the Binding Constraint

- **RAM binds first for almost every web workload.** Application runtime plus database plus page cache. Undersized RAM does not slow down gracefully; the OOM killer removes a process and the site returns 502.
- Rule of thumb for a single-box web app: application processes × their steady resident size + database working set + 25% headroom + swap. A small dynamic site with a database sits comfortably in 2-4 GB; anything running a JVM, an Elasticsearch node, or a bundler in CI wants 8 GB before it wants more cores.
- **Disk binds second, and it is a one-way door.** Growth cannot be undone on essentially every provider. Size for roughly 18 months of data plus the space logs and images will take, then leave the rest on object storage. See `resizing.md`.
- **CPU binds last**, and when it does, it usually binds as *latency variance* on a shared plan rather than as raw throughput.
- **Bandwidth binds invisibly**: it does not slow anything down, it just appears on the invoice.

## vCPU Is the Least Useful Number

- A shared vCPU is a scheduling claim, not a core. Two providers' "2 vCPU" plans can differ by more than 2× in delivered throughput, and by much more in consistency.
- **Steal time is the honest metric.** Sustained steal above ~5% means the hypervisor is handing your slice elsewhere; that is a noisy-neighbour problem, and the fix is to move the instance or to pay for dedicated vCPU, never to add software.
- **Shared is correct for almost everything**: web servers, databases under moderate load, background workers. Dedicated vCPU is for sustained compute — video encoding, builds that run for hours, anything where p99 latency is contractual.
- Published benchmark scores of a plan family tell you about that provider's *typical* node, not about the node you will get.

## ARM Before x86

- Where both exist, ARM plans are commonly cheaper for the same RAM and perform equivalently or better for interpreted web workloads, which are memory- and IO-bound rather than instruction-bound.
- **Check compatibility before recommending**, in this order: container base images for the stack, any binary-distributed dependency (database extensions, headless browsers, proprietary agents, some ML wheels), and the CI runner that will build the images. One dependency without an `arm64` build converts the saving into an emulation penalty.
- Emulating x86 on ARM is a fallback for one small component, never a plan.
- `cpu_arch: either` means present both and let the compatibility check decide; `arm64` means run the check first and say what it found.

## Region

- Place by user latency, not by datacenter reputation. Round-trip time roughly tracks distance; a continent away is a noticeable delay on any request that makes several sequential calls.
- One region until you have a measured reason for two. Multi-region multiplies operational surface — configuration drift, data sync, and a much harder debugging story — and buys nothing for a single-database application.
- Regions inside one provider are usually priced alike but **not** always: some locations carry a surcharge, and included traffic allowances can differ between locations of the same provider.
- Private networking works only between machines in the same location. Plan the fleet's location before the second box, not after.

## The Comparison That Actually Matters

Build this table for the two finalists rather than comparing plan pages:

| Line | A | B |
|---|---|---|
| Plan price, monthly, with currency | | |
| RAM, disk, vCPU type (shared/dedicated) and architecture | | |
| Included egress, and the overage rate per unit | | |
| IPv4 charge, attached and unattached | | |
| Snapshot storage rate, and backup add-on as a % of plan price | | |
| Expected monthly total at *this* workload | | |
| Recovery path: console, rescue mode, API | | |
| Exit cost: how the data leaves, and what that egress costs | | |

The last two rows are what turns a spreadsheet into a decision. A provider you cannot recover a box on is cheaper only until the first outage.

## Managed Versus Self-Run

- A managed database or managed Kubernetes typically costs several times the equivalent VPS resources. That premium buys backups, failover, and patching — real work, correctly priced if you would otherwise do it badly.
- The honest test: would this component's failure at 3am wake someone who knows how to fix it? If no, managed is cheaper than the outage. If yes, self-run on a VPS is a legitimate saving.
- Mixed is normal and often optimal: application on a VPS, the database managed, object storage for anything large.

## Trial and Exit

- Prefer hourly billing for anything experimental: you can create, measure, and destroy inside a day for a rounding error, which beats any benchmark article.
- Check the refund and trial rules **before** prepaying anything annual — many budget hosts refund nothing after a short window.
- Promotional first-month pricing is not a price. Compare renewal rates.
- Verify the exit path at signup: is there an image or snapshot export, and what does moving the data out cost? A provider whose data only leaves over metered egress has priced your migration in advance.

---

**Write the outcome.** When a provider or plan is chosen, save the decision to `~/Clawic/data/vps/artifacts/provider-decision-<scope>.md` — the choice, the rejected option and its real cost, the accepted downsides, and what would make you revisit — and add its `## Boxes` line to `memory.md` in the same turn. Deriving this comparison takes an afternoon; nobody should pay for it twice. When a server is actually created from the decision, its row goes to `~/Clawic/data/servers/servers.md` and its VPS-only attributes to `## Hosts` (`provisioning.md`).
