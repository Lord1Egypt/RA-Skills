# Migration and Teardown — Moving a Live Server, and Stopping the Bill

Read when moving to another provider, replacing a server in place, or shutting one down. Two halves: the cutover, which is mostly a DNS operation, and the teardown, which is where the money is lost.

**Before planning a cutover**, read `~/Clawic/data/servers/servers.md` (what exists and what it costs), `## Hosts` in `memory.md` (what each box serves, its snapshot policy, its PTR), `## Exposure` (rules to recreate on the new host), and `~/Clawic/data/domains/domains.md` (registrar, DNS host, and current TTL — the TTL sets the cutover window).

**Contents:** [Decide Whether to Move at All](#decide-whether-to-move-at-all) · [The Two Migration Shapes](#the-two-migration-shapes) · [Cutover Choreography](#cutover-choreography) · [Moving the Data](#moving-the-data) · [Databases](#databases) · [What Gets Forgotten](#what-gets-forgotten) · [Rollback](#rollback) · [Teardown](#teardown) · [Leaving a Provider Entirely](#leaving-a-provider-entirely)

## Decide Whether to Move at All

Migration costs a day of attention and carries real risk. Good reasons: a price difference that compounds meaningfully at this fleet size, a jurisdiction requirement, chronic reliability or steal-time problems, or a capability the current provider does not have. Bad reasons: a slightly better plan page, and a bad week.

Price the move honestly before deciding: the egress to get the data out, the hours, the risk window, and the new provider's real monthly total including add-ons (`choosing.md`). A saving of a few units of currency per month rarely repays a day of work plus an outage risk.

## The Two Migration Shapes

| | Image / snapshot transfer | Rebuild and restore |
|---|---|---|
| How | Export a disk image, import at the destination | Provision fresh from the user-data file, restore data |
| Speed | Faster when it works | Slower first time, then repeatable |
| Fidelity | Carries everything, including the accumulated mess and any compromise | Carries only what you listed |
| Provider support | Patchy, and formats and hardware differ | Universal |
| Side effect | None | You discover what was never written down |
| Use when | The box is a pet with undocumented state and you accept the mess | Almost always |

**Rebuild and restore is the default.** It exercises the provisioning file and the backups, which is the same drill you owe yourself quarterly anyway (`backups.md`). If a rebuild is not possible because nobody knows what is on the box, that finding is more important than the migration.

## Cutover Choreography

The order exists because DNS caches ignore your schedule.

1. **Days ahead: lower the TTL** on every record that will change, to a few minutes. This is the only step that cannot be rushed — you must wait out the *old* TTL for the new one to be in effect everywhere. Update the row in `~/Clawic/data/domains/domains.md`.
2. **Build the destination completely** and test it by name, using a local hosts-file override so you exercise the real hostname and the real certificate without touching public DNS.
3. **Freeze or plan for writes.** Any write that lands on the old server after the data sync is lost. Either a short read-only window, or an application-level rule for reconciling the overlap. Choose deliberately; "it will be fine" is where data goes missing.
4. **Final data sync**, incremental on top of the earlier bulk copy, so the last step is minutes rather than hours.
5. **Switch.** DNS record to the new address, or — within one provider — move the floating address, which is instant and needs no TTL wait (`networking.md`).
6. **Watch both machines.** The old one still receives traffic for the length of the old TTL and from resolvers that ignore it. Logs on the old box tell you when the tail has finished.
7. **Keep the old server running, untouched, for at least 24-72 hours.** It is the rollback (below) and it is cheap insurance.
8. **Raise the TTL back** and update the domain row.
9. **Then** teardown.

Certificates: issue them on the new host *before* the cutover where the issuance method allows it, or the switch produces a certificate warning for every visitor during the gap. Anything that validates over HTTP needs the traffic to be arriving already, which means issuing after the switch and accepting a short window — plan which of the two you are doing.

## Moving the Data

- **Bulk copy first, days early; incremental sync at cutover.** A file-level sync tool that only transfers differences turns a multi-hour copy into a two-minute one.
- Preserve ownership, permissions, and timestamps. A restore where every file belongs to root is a subtle, half-working application.
- **Transfer over the private network if both machines share one**; it is free and fast. Across providers it is public egress and it is metered on the sending side (`costs.md`).
- Large datasets sometimes move faster via object storage than directly, because both ends can parallelise and a failure resumes instead of restarting.
- Verify by count and size after the copy, not by watching it finish. A transfer interrupted at 98% looks complete in the terminal scrollback.

## Databases

- Never file-copy a running database. Dump, transfer, load — or set up replication from old to new and promote the new one at cutover, which reduces the write freeze to seconds.
- **Match or exceed the major version** at the destination. A dump from a newer major version will not load into an older one, and this is discovered at the worst moment.
- Load times are dominated by index rebuilds. Time it on a scratch copy beforehand: this number decides the length of your write freeze and it is routinely underestimated by a factor of several.
- Character set and collation differences between versions can change sort order and unique-constraint behaviour. Check before, not after.
- Re-run the application's own health checks after the load. A database that loads without error can still be missing sequences, extensions, or grants.

## What Gets Forgotten

The list that turns a clean cutover into a week of small outages. Walk it explicitly:

- **Cron jobs and timers** — on the old box, not in the repository.
- **Firewall rules at both layers**, from `## Exposure` (`firewall.md`).
- **The provider firewall's group or tag membership** — the new machine is not automatically in it.
- **Reverse DNS**, set at the provider, needed by mail (`email.md`).
- **Addresses allow-listed by third parties** — a payment provider, an API, a partner's firewall, a database that only accepts your old address. These take days to change and belong at the top of the plan.
- **Certificates and their renewal mechanism**, including whatever proves domain control.
- **Secrets and environment files** — never in the backup if the backup was correct, so they must be moved deliberately from the user's secret store.
- **Log shipping, monitoring agents, and uptime checks** pointing at the old host.
- **Backup jobs** — configured on the old box, and now backing up a machine you are about to destroy.
- **SSH known-hosts entries and any key allow-list** on machines that connect to this one.
- **The private network address** and anything that references it.
- **Documentation and runbooks** naming the old host (`artifacts/`).

## Rollback

- The rollback is the old server, still running, still unmodified. This is the entire reason for step 7.
- Rolling back means pointing DNS back and waiting out the TTL — which is why the TTL stays low until you are confident.
- **Rollback stops being possible the moment the new server accepts writes you have not mirrored back.** Know where that point is, state it out loud before the cutover, and treat it as the real decision point.
- Define the abort criteria before starting: what error rate, what missing functionality, what elapsed time causes you to go back rather than push forward at 2am.

## Teardown

Destroying the instance does not stop the billing. Walk the list, then verify on the invoice next cycle:

| Item | Why it lingers |
|---|---|
| Reserved / floating addresses | Bill while reserved, attached or not (`networking.md`) |
| Block volumes | Detaching does not delete; an orphaned volume bills forever |
| Snapshots and backup add-on | Per GB of disk size, indefinitely; the add-on may need cancelling separately from the server |
| Load balancers, managed databases, object storage buckets | Created alongside, destroyed separately |
| Private networks and firewall objects | Usually free, but they clutter and confuse the next audit |
| DNS records pointing at the dead address | An address handed to the next customer now receives your traffic — a real and underrated exposure |
| Monitoring and uptime checks | Bill per check and page someone at 3am about a server that no longer exists |
| The final snapshot you kept "just in case" | Set a date to delete it, or it is permanent |

Before destroying: take a final snapshot, keep it for a defined period, and put its deletion date in `## Due` so it is actually deleted. Then verify the next invoice actually dropped — this is the step that catches everything the list missed.

## Leaving a Provider Entirely

- Get all data out first and verify it, including anything in their object storage, their managed databases, and their backup add-on.
- Export any configuration you would otherwise re-derive: firewall rules, DNS zones if they host them, load balancer configuration.
- **Close the account rather than leaving it empty**, once nothing remains — an open account with a stored payment method and no 2FA discipline is a liability (`security.md`).
- Cancel the subscription row in `~/Clawic/data/finances/subscriptions.md` and confirm the final invoice is zero.
- Some providers keep data for a retention period after deletion; if that matters, ask for confirmation of deletion in writing.

---

**Write it down.** A migration produces four writes, all in the same turn as the work: the cutover plan and its lessons to `~/Clawic/data/vps/artifacts/cutover-<year>-<from>-<to>.md` with its `## Boxes` line; the new host's row in `~/Clawic/data/servers/servers.md` and the **deletion** of the old one, plus its `## Hosts` row; the events in `~/Clawic/data/vps/changes/<year>.md`, one line for the cutover and one for the teardown with `Reversible? no`; and the updated `Points at` and TTL in `~/Clawic/data/domains/domains.md`. If the provider account is closed, delete its row from `## Provider Accounts` and from `~/Clawic/data/finances/subscriptions.md`, noting the closure date. An inventory that only grows stops being an inventory.
