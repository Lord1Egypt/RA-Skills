# Upgrades — CLI Versions, Provider Majors, And OpenTofu

Two independent axes: the CLI version, and each provider's version. **Never move both in the same PR** — when the plan changes, you need to know which one did it.

## Upgrading The CLI

- State is upgraded on first write by the newer CLI, and older CLIs then refuse it: *"state snapshot was created by Terraform vX, which is newer than current"*. One person applying from a new binary locks everyone else out until they upgrade.
- Bump `required_version` in the same PR as the upgrade. The failure mode becomes a clear message instead of a confusing parse error on a block the old CLI does not know.
- Order: CI first (every change flows through it), then laptops, then the documentation everyone copies from.
- There is no supported downgrade after a state write. The recovery is restoring the previous state version, which is a data loss window.
- Read the release notes for state format changes specifically; feature additions are safe to ignore until you use them (`SKILL.md` Version Floors).

## Upgrading A Provider Major

1. **Read the provider's upgrade guide.** Grep the codebase for every renamed or removed argument it names.
2. Bump in **one low-risk stack**. `terraform init -upgrade`, then plan.
3. Sort the diff into three classes:
   - **(a) Real changes** you have to accept or adjust.
   - **(b) Nothing** — the provider's state upgrader handled a rename internally. This is the majority in a well-run major.
   - **(c) Resource splits**: one resource became several. The plan will offer to *remove* the settings, because they now live in resources that do not exist in your config yet. **This is import work, not an approval.** The canonical example is the AWS provider's 4.x series splitting `aws_s3_bucket`'s inline arguments (ACL, versioning, logging, lifecycle, server-side encryption) into separate resources.
4. Zero-diff, or an explained diff per line, before moving to the next stack.
5. Commit the regenerated lock file with every platform (`providers.md`).

Class (c) is the whole risk of a provider major. If the upgrade guide has a "the following resource is now several resources" section, budget a day, not an afternoon.

## Deprecation Warnings Are The Schedule

Warnings in plan output tell you what the next major removes. Grep CI logs for `Warning:` and fix them while they are warnings — that is the entire difference between a boring major upgrade and a week of surprises. `-compact-warnings` makes them readable; it does not make them optional.

## Upgrading Modules

- One module per PR, planned in every environment. Bundling three module bumps means bisecting an unexpected destroy by hand.
- A module that renames internal resources without shipping `moved` blocks turns a version bump into a destroy. Read the CHANGELOG, and diff the source if it does not have one (`modules.md`).
- Registry modules can pull in provider constraints of their own. A module upgrade that suddenly requires a newer provider is a two-axis change — split it.

## Terraform ↔ OpenTofu

- OpenTofu forked from the Terraform 1.6 line after the license change to BUSL. The `tofu` binary reads existing state, parses the same HCL, and is a drop-in for most codebases.
- Divergence grows with every release on both sides: OpenTofu added native state encryption, and each project has shipped features the other has not. Version floors above 1.6 **do not transfer** — check `tofu version` against OpenTofu's own changelog before using a newer block.
- Registry namespaces differ; `terraform state replace-provider` rewrites the recorded provider addresses (`refactoring.md`).
- Treat a switch as a one-way door for the team, not per-repo. Mixed binaries against one state is how you get a state written by a version half the team cannot read.

Migration checklist:

```bash
terraform state pull > pre-switch-$(date +%s).tfstate   # keep it offline
terraform show -json > before.json                       # baseline
tofu init                                                # against a COPY of the state first
tofu show -json > after.json
diff <(jq -S . before.json) <(jq -S . after.json)        # expect no semantic difference
```

Then switch CI, then laptops, then delete the old binary from the runner image so nobody drifts back.

## The Rhythm That Prevents All Of This

- Patch upgrades on a schedule (monthly is enough for most teams) so the diff is always small.
- Majors deliberately, one stack at a time, with the upgrade guide open.
- A stack nobody has planned in six months is not stable, it is unknown — the scheduled drift job (`ci.md`) is what keeps that from being true.
