# Providers — Pinning, The Lock File, and Multi-Account Configs

## Declaring and Constraining

```hcl
terraform {
  required_version = ">= 1.7"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.1"
    }
  }
}
```

Constraint semantics, worked:

| Constraint | Allows | Blocks |
|---|---|---|
| `~> 5.1` | 5.1.0 through any 5.x | 6.0.0 |
| `~> 5.1.0` | 5.1.0 through 5.1.x | 5.2.0 |
| `>= 5.0, < 6.0` | the same as `~> 5.0`, written explicitly | 6.0.0 |
| `5.1.2` | exactly that build | everything else |

Pessimistic minor (`~> 5.1`) plus a committed lock file is the working default: the constraint states intent, the lock states reality. Exact pins in `required_providers` are for the case where you also own a scheduled upgrade job — otherwise they rot.

**Constraints belong in the root and in modules; the lock file exists only in the root.** A module's constraint narrows the range, it does not select the version.

## `.terraform.lock.hcl`

- Records the selected version plus content hashes per platform. **Commit it.** It is the difference between "CI builds what I reviewed" and "CI builds today's release".
- `terraform init` adds newly required providers; `terraform init -upgrade` re-selects within the constraints and rewrites the lock.
- A colleague or runner on a different OS/architecture hits "provider ... does not have a package available" or a checksum mismatch, because your lock only carries your platform's hashes. Fix once, for everyone:

```bash
terraform providers lock \
  -platform=linux_amd64 \
  -platform=darwin_arm64
```

Those two are the `lock_platforms` default (CI runner plus Apple Silicon laptop). Add one `-platform` flag per extra target your team or runners use — `-platform=linux_arm64` for Graviton runners, `-platform=windows_amd64` for a Windows workstation — and keep the flags and `lock_platforms` in `~/Clawic/data/terraform/config.yaml` identical, since the Output Gates check that list.

- CI gate: `terraform init -lockfile=readonly` fails when the lock would have to change. That turns "someone bumped a provider by accident" from a silent diff into a red build.
- "Inconsistent dependency lock file" means the config requires something the lock does not record — run `init -upgrade` locally and commit, never work around it in CI.

## Aliases: Two Regions, Two Accounts, One Config

```hcl
provider "aws" {
  region = "eu-west-1"
}

provider "aws" {
  alias  = "us"
  region = "us-east-1"
}

resource "aws_s3_bucket" "replica" {
  provider = aws.us
  # ...
}

module "edge" {
  source    = "./modules/cdn"
  providers = { aws = aws.us }
}
```

- The unaliased provider is inherited by child modules automatically; aliased ones must be passed in the `providers` map or the module silently uses the default.
- `terraform providers` prints the resolved provider tree per module — the fastest way to confirm which credentials a resource will actually use.
- Cross-account: one alias per account, each with its own `assume_role`. The starting credentials must be allowed to assume every role in the config. Switching profiles between applies instead of using aliases means a plan and its apply can hit different accounts.
- **Removing a provider block while resources still reference it** fails with "Provider configuration not present", usually during a destroy. Keep the block until the last resource using it is gone.

## Provider-Level Defaults

- Defaults set on the provider (AWS `default_tags`, and equivalents elsewhere) apply to everything it creates. They are the cheapest way to enforce a tagging policy — and a source of confusing diffs when a resource also sets the same tag inline.
- Retry and timeout settings on the provider apply fleet-wide; tune them there rather than per resource.

## Installation Plumbing

- `TF_PLUGIN_CACHE_DIR=~/.terraform.d/plugin-cache` makes every workspace share one copy of each provider. Without it, each `.terraform` directory holds its own copy, and the large cloud providers are hundreds of megabytes each — this is most of the disk and most of the `init` time on a laptop with a dozen stacks.
- Airgapped or regulated CI: `provider_installation { filesystem_mirror }` or `network_mirror` in the CLI config, populated by `terraform providers mirror ./dir`.
- `dev_overrides` points a provider at a local build for development. It skips the lock file and prints a warning on every command — leaving it configured is how you spend an afternoon debugging a plan that ignores your version constraint.

## Third-Party And Community Providers

- `source = "namespace/name"` — the **namespace is the trust boundary**. A typo'd or lookalike namespace is a supply-chain event that runs code on your CI with your cloud credentials.
- Verify the namespace once, then let the lock file's hashes hold it. Review the diff whenever the lock changes for a third-party provider.
- Provider-defined functions (terraform >=1.8) are called as `provider::name::function(...)`. They make the module unusable on older CLIs, so raise `required_version` in the same PR.

## When A Provider Is The Problem

Symptoms that are the provider, not you: "Provider produced inconsistent final plan", an attribute that diffs after every apply, a crash with a stack trace, or an API field the resource simply does not expose. Upgrade to the newest patch of the current major first — then pin, comment, and file (`debug.md`).
