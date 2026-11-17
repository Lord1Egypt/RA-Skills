# Refactoring Live Infrastructure Without Recreating It

The acceptance test for every refactor — rename, module extraction, import, split — is a no-op plan: `0 to add, 0 to change, 0 to destroy` before the PR merges. Any other result means the refactor changes infrastructure.

- Not sure which construct the change needs → Which Block Do I Need
- Renaming, or moving a resource into or out of a module → `moved` Blocks · Extracting A Module From Inline Resources
- Switching `count` to `for_each` without recreating anything → `count` → `for_each`, Worked
- Adopting an object that already exists in the cloud → `import` Blocks
- Dropping a resource from Terraform while it keeps running → `removed` Blocks
- The address is too broken for any block, or the move crosses states → When Surgery Is Still The Answer · Provider Address Changes

## Which Block Do I Need

| What you want | Block | Constraint |
|---|---|---|
| Rename in code, same resource type | `moved` | Same type only; `moved` cannot cross types |
| Move a resource into or out of a module | `moved` | The address includes the full module path |
| Rename or re-key a module call | `moved` | Moving `module.a` (un-indexed) moves all of its instances |
| Migrate `count` → `for_each` | One `moved` per index | `aws_x.y[0]` → `aws_x.y["blue"]` |
| Adopt an object that already exists in the cloud | `import` | Needs config for it; `-generate-config-out` writes a draft |
| Stop managing, keep the object alive | `removed` block with `destroy = false` | Delete the resource block in the same commit |
| Stop managing and delete the object | Delete the block; it becomes a normal destroy | Read the destroy count first |
| Move a resource to a different state | `removed` in the source, then `import` in the destination | Source applies first (`state.md`) |
| Change the resource *type* (provider split one resource into several) | `removed` + `import` | Or the provider's documented migration path (`upgrades.md`) |
| Fix an address too broken to express declaratively | `state mv` / `state rm` on a pulled backup | Out-of-band; document it in the PR that follows |

## `moved` Blocks

```hcl
moved {
  from = aws_instance.web
  to   = module.compute.aws_instance.web
}
```

- Keep the block until **every** environment and every collaborator has applied it. Deleting it early against a state that never saw it is a destroy plus a create.
- Chains resolve in one pass: `A → B` and `B → C` in the same file lands everything at C.
- `moved` is state-only. It never calls the cloud, so a zero-diff plan is a complete proof that you got the addresses right.
- Removing the blocks later is a separate, boring PR. Do it — a file of historical `moved` blocks is a map of decisions nobody can safely delete a year later.

## Extracting A Module From Inline Resources

1. Write the module and call it, leaving the original resource blocks in place for one commit only if you need to diff attributes.
2. Delete the originals, add one `moved` per resource: `from = aws_subnet.this["a"]`, `to = module.net.aws_subnet.this["a"]`.
3. Plan. A create/destroy pair in the output means one address is wrong — compare against `terraform state list`, which is the only authoritative list of the old addresses.
4. Apply everywhere, then remove the blocks.

## `count` → `for_each`, Worked

```bash
terraform state list | grep aws_instance.web
# aws_instance.web[0]
# aws_instance.web[1]
```

```hcl
moved {
  from = aws_instance.web[0]
  to   = aws_instance.web["blue"]
}
moved {
  from = aws_instance.web[1]
  to   = aws_instance.web["green"]
}
```

The index→key mapping comes from the *current* state, not from the order in your variable file. Get it wrong and Terraform re-creates both machines while reporting a perfectly reasonable-looking plan.

## `import` Blocks

```hcl
import {
  to = aws_s3_bucket.logs
  id = "acme-prod-logs"
}
```

- The `id` format is per resource type and documented at the bottom of that resource's page — some take an ARN, some a name, some a compound `region/name` string. A wrong format fails with "Cannot import non-existent remote object" even when the object plainly exists.
- `terraform plan -generate-config-out=gen.tf` writes a draft for everything being imported. It refuses to overwrite an existing file, so iterate into a new name.
- **The generated config is a draft, not an answer.** Every attribute is inlined including defaults and read-only fields; leaving read-only attributes in makes the next plan try to set them. Rewrite it to your conventions, then verify zero diff.
- Bulk import (terraform >=1.7) takes `for_each`:

```hcl
import {
  for_each = { logs = "acme-prod-logs", assets = "acme-prod-assets" }
  to       = aws_s3_bucket.this[each.key]
  id       = each.value
}
```

- "Resource already managed by Terraform" means the address is taken — you are importing something you already have, usually under a different address.
- After the import applies, the blocks are no-ops. Remove them in the follow-up PR with the `moved` blocks.

## `removed` Blocks

```hcl
removed {
  from = aws_iam_user.legacy
  lifecycle {
    destroy = false
  }
}
```

- This is the reviewable form of `state rm`: the intent ships in the diff and replays in every environment.
- The resource block must be gone from config in the same commit; `removed` and a live `resource` block for the same address conflict.
- `destroy = true` in a `removed` block is just a destroy with extra steps — use it only when you also want the object gone and the block deleted in one motion.

## When Surgery Is Still The Answer

`state mv` and `state rm` survive for cross-state work on pulled files, and for addresses so broken that no block can name them. Rules:

- `terraform state pull > backup-$(date +%s).tfstate` first, every time.
- Single-quote every address — brackets and double quotes are shell metacharacters:
  ```bash
  terraform state mv 'aws_instance.web[0]' 'module.compute.aws_instance.web["blue"]'
  terraform state rm 'module.legacy'          # removes the module and everything in it
  ```
- `state rm` on a module address drops every resource inside it. Print `terraform state list | grep '^module.legacy'` and count before you run it.
- Write what you did into the PR description. An out-of-band change nobody can find is the reason the next engineer distrusts the state.

## Provider Address Changes

`terraform state replace-provider registry.terraform.io/-/aws registry.terraform.io/hashicorp/aws` rewrites the provider recorded against every resource. Needed after very old state formats and after switching registry namespaces (including a Terraform ↔ OpenTofu move). It touches state only; run a zero-diff plan after.
