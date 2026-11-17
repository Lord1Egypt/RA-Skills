# Secrets — What State Exposes and How To Contain It

The one fact everything else follows from: **Terraform writes every attribute it manages into state in plaintext**, including generated passwords, private keys, and anything a data source read. `sensitive = true` is output hygiene, not a security control.

## The Four Places A Secret Leaks

| Surface | What it contains | Containment |
|---|---|---|
| The state file | Every attribute of every managed resource, in clear | Encrypt at rest, restrict read access to the pipeline role, enable versioning knowing old versions keep old secrets |
| The saved plan (`tfplan` and its JSON) | New values in clear, including passwords about to be set | Treat the artifact like a credential; never attach it to a public PR comment — post the human summary instead |
| `TF_LOG` output | Full request and response bodies | Write to a path you delete; never into a CI log that ships to a log aggregator |
| Git | `.tfvars`, a variable default, a heredoc policy with a token in it | Gitignore `*.tfvars`, pre-commit secret scanning, and remember history is forever |

## Getting Secrets In

- `TF_VAR_<name>` environment variables sourced from the CI secret store. The value still lands in state if a resource stores it — that is expected; the point is that it is not in the repo.
- Secret-manager data sources read at plan time; the value lands in state too. Acceptable when everyone who can read the state is already allowed to read that secret.
- `-var-file` pointing outside the repository for laptop runs.
- Never a committed `.tfvars`, never a variable `default`, never a value pasted into a `locals`.

## Keeping Secrets Out Of State Entirely

- **Ephemeral values and resources** (terraform >=1.10): variables, locals, and resources marked ephemeral exist only during the run. They are never written to state or to the plan file — the right vehicle for a short-lived token used to configure something else.
- **Write-only arguments** (terraform >=1.11): resource arguments the provider accepts and never persists (password fields on supporting resources). They pair with a companion version argument you bump to trigger a rotation, since the provider has nothing to compare against.
- **Let the cloud generate it.** Managed-secret features (a database that creates and stores its own master password in the platform's secret manager) mean Terraform never sees the value at all. Prefer this over `random_password`, which stores the result in state by definition.
- OpenTofu offers native state encryption as an alternative containment layer; Terraform relies on the backend's encryption (`upgrades.md`).

## Marking And Retrieving

```hcl
variable "api_token" {
  type      = string
  sensitive = true
}

output "db_endpoint" {
  value     = aws_db_instance.this.address
  sensitive = false
}
```

- A non-sensitive output derived from a sensitive value errors at plan. That is the system working — mark the output, or use `nonsensitive()` only when the sensitivity was inherited rather than real.
- Retrieve with `terraform output -raw <name>`; piping it anywhere that logs is the same leak as before.
- Sensitivity propagates through expressions, so one sensitive input can make a whole merged map sensitive — and a sensitive map cannot be used as `for_each` keys (`expressions.md`).

## After An Exposure

Order matters:

1. **Rotate the credential first.** Everything else is cleanup.
2. Remove the value from the current config and state (usually by rotating the underlying resource, not by editing state).
3. Accept that **old state versions still hold it**. Bucket versioning that saved you last month is now retaining the secret; assume anyone who had read access has it.
4. Audit the read access list for the state backend, the CI artifact store, and the log aggregator — those are the three copies.
5. If the value reached git, rotation is the only remediation. History rewriting does not reach forks and clones.

## Access Control Checklist

- State backend: pipeline role can read/write; humans read only via a break-glass path that is audited.
- No `terraform_remote_state` across a trust boundary — it grants read of the whole state file, secrets included (`state.md`).
- Plan artifacts expire on a schedule and are not world-readable in the CI UI.
- Provider credentials come from OIDC federation per environment, not from long-lived keys in CI secrets (`ci.md`).
- Nothing in this skill's configuration is a secret: `config.yaml` holds preferences, credentials come from the environment.
