# Infrastructure as Code Checklist

Review checklist for Terraform, CloudFormation, Pulumi, and other IaC files.
The review skill checks these during layer 4 (IaC).

Customize for your organization's specific policies.

## Terraform

### Resource Tags (commonly enforced via SCP or policy)
- [ ] All taggable resources have required tags
- [ ] Tag values match allowed values (if enforced)
- [ ] `default_tags` block in provider to avoid repetition

### Provider Configuration
- [ ] Provider version pinned with `~> X.Y` (not exact or unbounded)
- [ ] `required_version` set for Terraform itself
- [ ] `allowed_account_ids` set to prevent accidental cross-account applies

### State Management
- [ ] Remote backend configured (S3, GCS, Azure Blob, etc.)
- [ ] State encryption enabled
- [ ] State key is unique — no collision with other modules
- [ ] State locking configured (DynamoDB for S3, etc.)

### Security
- [ ] No hardcoded secrets, account IDs, or API keys
- [ ] IAM policies follow least privilege — no `*` on actions or resources
- [ ] No IAM users — use roles (if policy requires)
- [ ] Secrets stored in Secrets Manager / Parameter Store, not variables
- [ ] Security groups are not open to `0.0.0.0/0` unless explicitly justified

### Region / Network
- [ ] Resources deployed to allowed regions only
- [ ] No VPC creation if shared VPCs are required
- [ ] Subnet and AZ selection is correct

### Structure
- [ ] `moved` blocks used for renames (not destroy/recreate)
- [ ] `for_each` preferred over `count` for collections that may change
- [ ] Variables have `description` and `type`
- [ ] Outputs have `description`
- [ ] HCL data sources preferred over `jsonencode` (e.g., `aws_iam_policy_document` over inline JSON)
  - `jsonencode` should be a last resort when no native data source exists
  - Native data sources validate at plan time, are easier to read, and are composable

### Naming
- [ ] Resource names follow team conventions
- [ ] S3 buckets follow naming prefix requirements (if any)
- [ ] Module names match the resource they manage

## CloudFormation

- [ ] Parameters have `AllowedValues` where applicable
- [ ] No hardcoded AMI IDs — use SSM parameters or mappings
- [ ] DeletionPolicy set on stateful resources (RDS, S3, DynamoDB)
- [ ] Stack tags applied
- [ ] Outputs exported only when needed (avoid namespace collisions)

## Azure (ARM / Bicep)

- [ ] Required tags on all resources (resource group tags don't auto-inherit)
- [ ] Resource locks on stateful resources (storage accounts, databases)
- [ ] NSG rules follow least-privilege — no `*` on source/destination
- [ ] Managed identities preferred over service principals with secrets
- [ ] Key Vault used for secrets, not parameters or variables
- [ ] Resource names follow naming convention (`<prefix>-<app>-<env>-<resource>`)
- [ ] Correct subscription and resource group targeting
- [ ] API versions pinned (not `latest`)

## GCP (Terraform / Deployment Manager)

- [ ] Labels applied to all resources (GCP equivalent of tags)
- [ ] Firewall rules follow least-privilege — no `0.0.0.0/0` ingress unless justified
- [ ] Service accounts follow least-privilege — no `roles/editor` or `roles/owner`
- [ ] Secrets in Secret Manager, not environment variables or config files
- [ ] Correct project targeting — verify `project` attribute on resources
- [ ] Regions/zones match deployment requirements
- [ ] Uniform bucket-level access on GCS buckets (not ACLs)

## General IaC

- [ ] Changes have been `plan`/`preview` validated
- [ ] Destructive changes (destroy, replace) are intentional and called out
- [ ] Cross-environment impact considered (does this affect prod?)
