# Commands — Terraform

The incident toolkit: what you reach for under pressure, not the basics. On OpenTofu, substitute `tofu` — every flag below is identical.

## Plan And Read

```bash
terraform plan -out=tfplan
terraform show tfplan                    # re-render a saved plan, human form
terraform apply tfplan                   # the only apply that matches what you reviewed
terraform plan -detailed-exitcode        # 0 no changes · 1 error · 2 changes present
terraform plan -refresh-only             # what changed in the cloud, without proposing config changes
```

```bash
# every non-no-op change, as addresses and actions
terraform show -json tfplan \
  | jq -r '.resource_changes[] | select(.change.actions != ["no-op"]) | "\(.change.actions|join(",")) \(.address)"'

# the destroy gate
terraform show -json tfplan \
  | jq '[.resource_changes[] | select(.change.actions | index("delete"))] | length'
```

## State Inspection

```bash
terraform state list                     # every managed address
terraform state list | wc -l             # the number to compare after a migration
terraform state show 'module.net.aws_subnet.this["a"]'
terraform state pull > backup-$(date +%s).tfstate
jq '.serial, .lineage, (.resources | length)' backup-*.tfstate
```

Single-quote every address: `[`, `]`, and `"` are shell metacharacters.

## Surgery (only after a `state pull` backup)

```bash
terraform state mv 'aws_instance.web[0]' 'module.compute.aws_instance.web["blue"]'
terraform state rm 'aws_iam_user.legacy'                 # stops managing; the object keeps running
terraform state rm 'aws_instance.web (deposed abc12345)'
terraform state push backup-1770000000.tfstate
terraform state replace-provider registry.terraform.io/-/aws registry.terraform.io/hashicorp/aws
terraform force-unlock <LOCK_ID>                         # preconditions in recovery.md
```

## Init, Backends, Providers

```bash
terraform init -upgrade                                  # re-select within constraints, rewrite the lock
terraform init -migrate-state                            # copy state into the new backend
terraform init -reconfigure                              # forget the old backend, do NOT copy
terraform init -backend-config=env/prod.s3.tfbackend -input=false
terraform init -lockfile=readonly                        # CI gate: fail if the lock would change
terraform providers                                      # resolved provider tree, per module
terraform providers lock -platform=linux_amd64 -platform=darwin_arm64
terraform providers mirror ./mirror                      # populate an airgapped mirror
```

## Drift And Targeted Repair

```bash
terraform apply -refresh-only                            # accept reality into state
terraform apply -replace='aws_instance.web'              # recreate one resource (replaces `taint`)
terraform untaint 'aws_instance.web'
terraform plan -target='module.net' -out=tfplan          # emergencies only; full plan afterwards
```

## Answer Questions Without Running A Plan

```bash
terraform console                        # evaluate expressions against real state
terraform output -json
terraform output -raw db_endpoint
terraform graph -type=plan | dot -Tsvg > graph.svg
terraform fmt -check -recursive
terraform validate
terraform test                           # .tftest.hcl files (>=1.6)
```

## Environment Variables

```bash
TF_LOG=DEBUG TF_LOG_PATH=tf.log          # request/response bodies — treat the file as a secret
TF_LOG_PROVIDER=TRACE TF_LOG_CORE=WARN   # isolate the provider from core
TF_IN_AUTOMATION=1 TF_INPUT=0            # CI: no hints, no prompts
TF_VAR_db_password=...                   # a variable from the environment
TF_PLUGIN_CACHE_DIR=~/.terraform.d/plugin-cache
TF_CLI_ARGS_plan="-lock-timeout=5m"      # applies to every `plan` invocation
TF_WORKSPACE=staging                     # selects a CLI workspace non-interactively
```

## Two Habits Worth The Keystrokes

- `terraform plan -out=tfplan` even when you are "just looking" — the file is free and it is the only artifact you can apply honestly.
- `terraform state pull > backup-$(date +%s).tfstate` before any command containing the word `state`. It has never once been wasted effort.
