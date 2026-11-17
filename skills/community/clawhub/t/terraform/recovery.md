# Recovery — After The Damage

Every playbook here starts the same way: **stop the pipeline** so a second run cannot make it worse, then find out what is actually true before changing anything.

## Stuck State Lock

Precondition: you have proven the holder is dead.

1. Read the five fields the error prints: ID, Who, Created, Operation, Path. `Created` five minutes ago with `Operation: apply` is a live apply — wait.
2. Confirm with the source: the CI job page (finished, cancelled, or still running) or the colleague named in `Who`.
3. `terraform force-unlock <LOCK_ID>` — the ID from the error, never a guessed one.
4. Then run `plan` and read it before anything else. If the holder died mid-apply, see the next playbook.

Force-unlocking a **running** apply gives you two writers and a state that describes neither reality. There is no clean recovery from that; there is only reconstruction.

## Apply Interrupted (Ctrl-C, runner killed, credentials expired)

- Terraform persists state after each resource completes, so the state is usually intact but partial.
- First move is `terraform plan`. It tells you exactly what exists and what is missing — you do not have to guess.
- If the lock is still held by the dead job, unlock first (above), then plan.
- Do not re-run with `-refresh=false`: you would be planning against a state that predates the damage.
- Objects created by the API but never written to state show up as "already exists" errors on the next apply. Adopt them with an `import` block (`refactoring.md`).

## State Corrupted Or Pushed Wrong

Bucket object versioning is the undo. Nothing else is.

```bash
# download the previous version out of band, then:
jq '.serial, .lineage, (.resources | length)' candidate.tfstate
terraform state push candidate.tfstate
terraform plan          # must be zero-diff against reality
```

- A lower serial or a different lineage will be rejected; `-force` overrides both. Use it only when you are certain which snapshot describes reality, and keep the rejected one.
- Verify by resource count and by spot-checking two or three IDs against the cloud before you trust it.

## State Lost Entirely, No Versioning

Rebuild by import. This is a project, not a command.

1. Inventory the real objects from the cloud provider's own tooling — that inventory is now your source of truth.
2. Write `import` blocks for each. Where the config is gone too, `plan -generate-config-out=gen.tf` drafts it (`refactoring.md`).
3. Iterate to zero diff, one resource group at a time.
4. Budget hours per dozen resources, more for anything with compound import IDs.

This is the reason versioning on the state bucket is not optional.

## `state rm` On The Wrong Resource

The object is alive and unmanaged; nothing is broken yet.

- Best: restore the previous state version (above) — one operation, no ambiguity.
- Otherwise: `import` it back at exactly the same address. Get the address from your PR or from the backup you took before the surgery.
- Never "fix" it by letting the next apply create a replacement. That leaves a live orphan billing forever next to its new twin.

## An Unintended Destroy Applied

Terraform has no undo.

1. Stop the pipeline before a second apply removes more.
2. Recover the **data** first: snapshots, point-in-time restore, backups. Recreating the resource is the easy half.
3. Re-apply to recreate the resource, then restore the data into it.
4. Write down the "forces replacement" attribute or the plan line that caused it — that is the postmortem, and it usually points at a `for_each` key change or a module upgrade without `moved` blocks.

## Tainted And Deposed Objects

- **Tainted**: an apply failed partway through creating the object. The next apply replaces it. If the object is actually fine, `terraform untaint <addr>`. To force a replacement deliberately, `terraform apply -replace=<addr>` is the modern form of `taint`.
- **Deposed**: a `create_before_destroy` apply created the new object and failed before destroying the old one. `terraform state list` shows the address with `(deposed <id>)`. A normal apply usually destroys it. If it does not, confirm the object is gone in the cloud, then:

```bash
terraform state rm 'aws_instance.web (deposed abc12345)'
```

Leaving a deposed object unresolved means paying for a resource nothing references.

## The Same Object Managed By Two States

Two pipelines will fight over it forever, each reverting the other.

1. Decide which state owns it (usually the one whose blast radius it belongs to).
2. In the loser, delete the resource block and add a `removed` block with `destroy = false`. Apply.
3. Verify the winner's plan is zero-diff.

## Secret Leaked Into State Or Logs

Rotate first, clean second — the full order is in `secrets.md`. The state-specific part: old versions in the bucket still hold the value, so treat every principal with historical read access as having seen it.

## Emergency Change With A Broken Pipeline

When production is down and CI cannot deploy:

1. Use a machine with the correct role, not personal credentials.
2. `terraform plan -target=<addr> -out=tfplan`, read it, `apply tfplan`.
3. Immediately run a **full** plan and reconcile whatever the targeted apply skipped.
4. Open the PR that makes the change permanent the same day, describing exactly what was applied out of band.

Steps 3 and 4 are the ones people skip, and they are the reason the next incident starts with a surprise diff.
