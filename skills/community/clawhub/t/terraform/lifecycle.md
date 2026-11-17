# Lifecycle — Replacement, Protection, And Ignored Drift

The `lifecycle` block is where Terraform's declarative model gets its escape hatches. Each one buys something and charges for it later.

## `create_before_destroy`

```hcl
lifecycle {
  create_before_destroy = true
}
```

- **It is infectious.** Opting in on one resource forces the same ordering onto everything that resource depends on. Expect it to spread through the graph, and expect the spread to be the surprise, not the flag.
- **Unique names collide.** With CBD, the old and new objects exist at the same time — a fixed name on an IAM role, security group, or load balancer produces "already exists" at apply. Use `name_prefix`, or a `random_id` suffix with `keepers` (`expressions.md`).
- It can manufacture cycles when it meets a `depends_on` pointing the other way (`debug.md`).
- A CBD apply that creates the new object and fails before destroying the old one leaves a **deposed** object in state. Recovery is routed from SKILL.md Quick Reference.
- Worth it for anything fronted by a load balancer or referenced by a running fleet. Not worth it for a resource whose replacement is instant and unreferenced.

## `prevent_destroy`

```hcl
lifecycle {
  prevent_destroy = true
}
```

- It fails the plan with "Instance cannot be destroyed" — a genuinely useful guard against a stray `-target` or a bad `for_each` key.
- **It only guards while the block exists.** Deleting the resource block deletes the guard with it, and the plan proceeds to destroy. So it protects against accidents inside the config, not against removing the config.
- It also blocks a legitimate replacement: any change that forces replacement fails the plan until you remove the flag, apply, and put it back.
- Real deletion protection lives **outside** Terraform: an IAM deny on the delete action, or the provider's own deletion-protection attribute (which Terraform must then clear in a separate apply before the destroy — that two-step is the feature working).

## `ignore_changes`

```hcl
lifecycle {
  # the autoscaler owns this; see INFRA-482
  ignore_changes = [desired_count]
}
```

- Takes a **static list of attribute names** — no variables, no expressions, no computed lists.
- The attribute becomes permanently unmanaged: your config can say anything and Terraform will never correct it. That is the point and the danger.
- `ignore_changes = all` freezes the whole resource. Every future edit becomes a silent no-op, including the security fix someone assumes shipped.
- Always comment who writes the value. Without it, the next engineer inherits archaeology and eventually deletes the line to "clean up".
- Reach for it **third**, after identifying the writer and after checking for provider normalization (`debug.md`).

## `replace_triggered_by`

```hcl
lifecycle {
  replace_triggered_by = [aws_launch_template.this.latest_version]
}
```

- Forces replacement when a referenced resource or attribute changes — the clean fix for objects that must rotate together but have no direct dependency the provider understands.
- Takes resource or attribute references only, not arbitrary expressions. To trigger on a computed value, put the value in a `terraform_data` resource (terraform >=1.4) and reference that:

```hcl
resource "terraform_data" "config_version" {
  input = filesha256("${path.module}/app.conf")
}
```

- This is the supported replacement for the old "null_resource with triggers" idiom, and unlike a provisioner it is tracked in state.

## `precondition` And `postcondition`

They live inside `lifecycle` too (terraform >=1.2), but they are input validation rather than lifecycle control — assertions, thresholds, and where each one belongs are in `expressions.md`.

## Deleting Things On Purpose

Teardown fails for different reasons than creation, and always at the worst time:

- Provider-level deletion protection blocks the destroy until a prior apply clears the flag.
- Resources that retain data on delete (snapshots, final backups) leave names occupied, so the next create in that account collides.
- Dependencies destroy in reverse order, and anything created outside Terraform inside a managed container (an object written into a managed bucket, a record added to a managed zone) blocks its parent's deletion with an error the plan could not predict.
- `prevent_destroy` anywhere in the graph fails the whole plan, not just that resource.

Run one full create-then-destroy cycle in a sandbox before declaring a stack finished (`testing.md`). A stack nobody has ever destroyed usually cannot be.
