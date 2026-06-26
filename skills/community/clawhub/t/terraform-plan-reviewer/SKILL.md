---
name: terraform-plan-reviewer
description: Review terraform plan output for risk before apply. Detects destructive changes (force replace and destroy on stateful resources), drift from real state, missing imports, secrets leaked into outputs or state, IAM permission widening, public-internet exposure on storage and security groups, and provider-specific footguns across AWS, GCP, and Azure. Produces a P0/P1/P2 severity matrix, applies gating rules (block, require-approval, allow), and writes a PR-comment-style review with line citations and suggested fixes. Use when asked to review a terraform plan, gate a CI apply, audit a Terragrunt run, check infrastructure changes for risk, or set up a plan-review GitHub Action. Triggers on "terraform plan", "tf plan", "terragrunt", "tofu plan", "infrastructure as code", "iac review", "plan output", "destroy", "force replace", "iam widening", "drift", "tfstate", "atlantis", "spacelift", "env0".
metadata:
  tags: ["terraform", "tofu", "terragrunt", "iac", "infrastructure", "aws", "gcp", "azure", "devops", "platform-engineering", "security", "ci-cd", "code-review"]
---

# Terraform Plan Reviewer

Review `terraform plan` (or `tofu plan`, or a Terragrunt run-all) and decide whether the apply is safe. Categorizes every change by destructiveness, drift, secret exposure, IAM blast radius, and provider-specific risk. Returns a PR-comment-style review with severity grades, gating decision, and line-cited suggested fixes. Acts as a senior platform engineer who has approved thousands of applies and reverted the bad ones.

## Usage

Invoke this skill before any non-trivial `terraform apply`, in CI as a gate on PRs, or as a manual second opinion on an environment-affecting change.

**Basic invocation:**
> Review this terraform plan: [paste plan output]
> Gate this PR — should we apply or block?
> Audit my Terragrunt run-all output for drift

**With context:**
> Here's the plan and the previous state file — flag any IAM widening
> We're about to apply this to prod — what's the blast radius?
> Generate a GitHub Action that runs this review on every PR

The agent produces a graded review (P0/P1/P2 findings), a single apply gating decision (BLOCK / APPROVE-WITH-CONDITIONS / APPROVE), and per-finding suggested fixes with line numbers from the plan.

## How It Works

### Step 1: Parse The Plan

The agent normalizes input from any of:

- Human-readable `terraform plan` output (most common)
- JSON plan: `terraform show -json plan.out` (preferred — unambiguous)
- Terragrunt aggregated `run-all plan` output
- OpenTofu `tofu plan` (treated identically to terraform)

JSON form is preferred. When only text is available, the agent extracts:

```
+ create        = N resources
~ update        = N resources
-/+ replace     = N resources    (destroy then create)
+/- replace     = N resources    (create then destroy — usually safer)
-  destroy      = N resources
<= read         = N data sources
```

The agent also captures **resource addresses** (`module.x.aws_iam_role.y`), **change reasons** (`# forces replacement`), and any **drift markers** (`# (config refers to values not yet known)`, `Note: Objects have changed outside of Terraform`).

### Step 2: Severity Matrix

Every change in the plan gets exactly one severity. The matrix is the contract:

| Severity | Meaning | CI Default |
|----------|---------|------------|
| **P0 — Block** | Apply will cause data loss, outage, security breach, or unauthorized access. | Hard block. Human override required. |
| **P1 — Require Approval** | High risk; reasonable in some contexts but needs second pair of eyes. | Require named reviewer + comment justification. |
| **P2 — Advisory** | Low risk; flagged for awareness. | Allow apply; record in review. |
| **OK** | Standard, low-risk change. | No flag. |

### Step 3: Detection Rules

The agent runs every change through a layered ruleset. A single change may fire multiple rules; the highest severity wins.

**D — Destructive change rules:**

```
D1.  destroy on aws_db_instance, aws_rds_cluster, gcp_sql_database_instance,
     azurerm_mssql_database, azurerm_postgresql_server                     → P0
D2.  destroy on aws_s3_bucket, gcs_bucket, azurerm_storage_account
     when not empty (force_destroy=false)                                  → P0
D3.  destroy on stateful workloads (statefulset, persistent volume,
     elasticache, redis, kafka, mq broker)                                 → P0
D4.  -/+ replace on a database, cache, queue, or persistent disk           → P0
D5.  -/+ replace on a load balancer with active traffic                    → P1
D6.  -/+ replace on an IAM role / service account                          → P1
     (breaks every principal that assumes it)
D7.  destroy on a route53 / cloud DNS zone                                 → P0
D8.  destroy on a KMS key, cmek, key vault key                             → P0
     (data encrypted with it becomes unrecoverable)
D9.  destroy + recreate on a network resource carrying production traffic
     (vpc, subnet, vpc peering, transit gateway, vpn)                      → P0
D10. lifecycle.prevent_destroy=true bypassed by a destroy                  → P0
```

**S — Secret / output leak rules:**

```
S1.  output without `sensitive = true` containing a value matching
     password|secret|token|key|credential|api[_-]?key                      → P1
S2.  resource attribute set from a hardcoded string matching the
     secret regex (in plan diff, not just var)                             → P0
S3.  user_data / cloud-init / startup script contains a credential
     string visible in plan diff                                           → P0
S4.  tfvars/state file referenced from a public S3 bucket / public
     storage container / public repo                                       → P0
S5.  KMS / KeyVault key policy widens decrypt to "*"                       → P0
```

**I — IAM widening rules:**

```
I1.  Action: "*" or Resource: "*" on a new policy statement              → P0
I2.  Wildcard service principal in trust policy
     (Principal: {"AWS": "*"} or sts:AssumeRoleWithSAML to *)              → P0
I3.  iam:PassRole with Resource:"*" and no condition on iam:PassedToService→ P0
I4.  s3:* / dynamodb:* / kms:* added to a previously scoped policy        → P1
I5.  AdministratorAccess / Owner / Editor role assignment to a user
     that previously had a narrower role                                   → P1
I6.  GCP roles/iam.serviceAccountUser added without resource restriction → P1
I7.  Azure RoleAssignment scope = subscription or management-group        → P1
I8.  Conditions removed from an existing IAM policy (less restriction)    → P1
I9.  MFA condition removed from an assume-role trust policy               → P0
```

**N — Public exposure rules:**

```
N1.  S3 bucket public-access-block disabled OR ACL set to public-read    → P0
N2.  RDS / Cloud SQL / Azure SQL publicly_accessible = true               → P0
N3.  Security group ingress 0.0.0.0/0 on port not in {80, 443}            → P0
N4.  GCS bucket IAM grants `allUsers` or `allAuthenticatedUsers`          → P0
N5.  Azure Storage account public_network_access = "Enabled"             → P1
N6.  ELB / ALB scheme = internet-facing on a service that previously was
     internal                                                              → P1
N7.  Cloud Functions / Lambda invocation policy adds Principal: "*"      → P0
N8.  GKE / EKS / AKS cluster endpoint becomes public                     → P0
N9.  VPC subnet route added to internet gateway with 0.0.0.0/0            → P1
```

**X — Drift & state rules:**

```
X1.  Plan shows changes you didn't intend (drift) — values "changed
     outside of Terraform"                                                  → P1
X2.  Resource referenced in code but absent from state (needs import)    → P1
X3.  Resource in state with no matching code (needs `terraform state rm`
     or restore to code)                                                    → P1
X4.  Provider version pinning loosened (~> to >=)                         → P1
X5.  Backend config changed (state moves region/bucket/account)          → P0
X6.  count or for_each shifts re-index a list, causing mass replacement  → P0
```

**P — Provider-specific footguns (AWS):**

```
PA1. aws_launch_configuration deprecated → P2 (use launch_template)
PA2. aws_security_group rule moved into inline vs aws_security_group_rule
     resource without explicit replace = silent rule loss                 → P1
PA3. aws_lb_target_group port change forces recreate                     → P1
PA4. aws_eks_cluster version downgrade attempted                         → P0
PA5. aws_db_instance allocated_storage decreased                         → P0
PA6. aws_iam_role assume_role_policy replaced (vs updated)               → P1
PA7. aws_acm_certificate replaced when an LB still references the old   → P0
```

**P — Provider-specific footguns (GCP):**

```
PG1. google_sql_database_instance deletion_protection=false             → P1
PG2. google_compute_instance metadata_startup_script changed (replaces) → P1
PG3. google_project_iam_member vs _binding mixed (binding wipes others) → P0
PG4. google_kms_crypto_key with skip_initial_version_creation=true and
     destroy_scheduled_duration<7d                                         → P0
PG5. google_container_cluster master_auth changes force in-place        → P1
```

**P — Provider-specific footguns (Azure):**

```
PZ1. azurerm_resource_group destroy (cascades all child resources)      → P0
PZ2. azurerm_key_vault soft_delete_enabled toggled off                 → P0
PZ3. azurerm_storage_account replication type change forces destroy    → P0
PZ4. azurerm_role_assignment with scope at subscription level          → P1
PZ5. azurerm_virtual_machine deprecated (use _linux/_windows variant)  → P2
```

### Step 4: Apply Gating

The agent renders a single decision based on the highest-severity finding:

```
ANY P0           → BLOCK (do not apply)
ANY P1, no P0    → APPROVE_WITH_CONDITIONS (named reviewer + justification)
P2 only          → APPROVE (with advisory comments)
no findings      → APPROVE (clean plan)
```

Conditions on **APPROVE_WITH_CONDITIONS** include: a specific named reviewer, a deploy window restriction (no Friday afternoons), a maintenance-window flag, paired apply (two engineers on call), or a pre-apply backup snapshot.

### Step 5: Drift Detection

Drift is the silent killer of IaC. The agent surfaces three categories:

| Category | Marker | Action |
|----------|--------|--------|
| **Config drift** | "changed outside of Terraform" | Flag P1; suggest `terraform refresh` then re-plan; or import the manual change as code |
| **State drift** | resource missing from state but in code | Flag P1; provide `terraform import` command |
| **Code drift** | resource in state, removed from code | Flag P1; suggest `terraform state rm` if intentional, otherwise restore the resource block |

The agent generates the import command with the address and the cloud-side resource id whenever the cloud-side id can be inferred from the plan.

### Step 6: Comment-Style Review Output

The output mimics a senior reviewer's PR comment, formatted for direct paste into GitHub / GitLab / Bitbucket:

```markdown
## Terraform Plan Review

**Decision:** BLOCK

**Findings:** 2 × P0, 1 × P1, 3 × P2

---

### P0 — Destroying production RDS
`aws_db_instance.payments_prod` is being destroyed. This is a
`stateful + production` resource. Apply will lose all data not
captured in a manual snapshot.

```diff
-resource "aws_db_instance" "payments_prod" {
-  identifier = "payments-prod"
-  ...
-}
```

**Fix options**
1. Add `lifecycle { prevent_destroy = true }` and re-plan; investigate
   why the resource block was removed from code.
2. If the destruction is intentional (decommission), confirm a final
   snapshot exists: `aws rds describe-db-snapshots --db-instance-identifier payments-prod`.
3. If the resource was renamed, run `terraform state mv` instead of
   destroy + create.

---

### P0 — IAM wildcard introduced
`aws_iam_policy.deploy` adds `"Action": "*"` on `"Resource": "*"`.
This grants the role full account access.

```diff
+      Action   = "*"
+      Resource = "*"
```

**Fix:** scope to the specific actions the deploy job actually needs.

---

### P1 — Secret in output
Output `db_password` lacks `sensitive = true`. Plan will print the
value to logs.

**Fix:**
```hcl
output "db_password" {
  value     = aws_db_instance.x.password
  sensitive = true
}
```

---

### P2 — Provider version loosened
`hashicorp/aws` constraint moved from `~> 5.40` to `>= 5.0`. Future
plans may pull a major version. Pin tightly.

---

### Summary
Apply is **blocked** until the two P0 findings are addressed.
Recommended sequencing:
1. Restore `aws_db_instance.payments_prod` block, or land a
   decommission RFC with snapshot evidence.
2. Replace the wildcard IAM policy with a scoped policy.
3. Re-run plan and request review.
```

### Step 7: CI Integration

The agent emits a ready-to-commit GitHub Action / GitLab CI job:

```yaml
# .github/workflows/terraform-plan-review.yml
name: Terraform Plan Review
on:
  pull_request:
    paths: ['terraform/**', '**.tf', '**.tfvars']

jobs:
  plan-review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: hashicorp/setup-terraform@v3
        with: { terraform_version: 1.7.5 }
      - run: terraform -chdir=terraform init -backend=false
      - id: plan
        run: |
          terraform -chdir=terraform plan -out=plan.out -no-color
          terraform -chdir=terraform show -json plan.out > plan.json
      - id: review
        uses: ./.github/actions/tf-plan-review
        with:
          plan-json: terraform/plan.json
          gating: strict       # block | strict | advisory
      - if: steps.review.outputs.decision == 'BLOCK'
        run: |
          echo "::error::Plan review blocked the apply"
          exit 1
      - uses: actions/github-script@v7
        with:
          script: |
            github.rest.issues.createComment({
              owner: context.repo.owner,
              repo:  context.repo.repo,
              issue_number: context.issue.number,
              body: require('fs').readFileSync('review.md','utf8')
            });
```

For Atlantis, Spacelift, env0, and Terraform Cloud — the agent emits the equivalent webhook / pre-apply hook config.

### Step 8: Cloud-Specific Risk Lenses

The agent reads each plan with cloud-aware eyes:

**AWS lens:**

- IAM trust-policy changes carry the highest blast radius
- KMS key policy widening can grant cross-account decrypt — always P0
- Security group changes need *effective rules diff*, not just resource diff (a removed rule from one SG may be re-added in an inline rule on another)
- Route53 zone changes are slow to revert; mistakes propagate via DNS TTL

**GCP lens:**

- `google_project_iam_binding` overwrites *all* members on a role — P0 if mixed with `_member` resources for the same role
- KMS key versions in `STATE_PENDING_DELETE` cannot be recovered after `destroy_scheduled_duration` — minimum 7 days
- Cloud SQL `deletion_protection` should be true in prod; a plan toggling it off is P1

**Azure lens:**

- Resource group destroys cascade silently — every child resource is gone
- Key Vault `soft_delete_enabled` and `purge_protection_enabled` interact; turning off either is P0
- Storage Account `account_replication_type` change forces destroy + create
- Role assignments at subscription scope are the equivalent of AWS account-level Admin — P1 minimum

### Step 9: Backup & Pre-Apply Checklist

For any plan with P1+ findings, the agent emits a pre-apply checklist:

```
[ ] State backed up (s3 cp / gsutil cp / az storage blob copy)
[ ] Manual DB snapshot taken for any stateful resource being touched
[ ] Maintenance window confirmed with stakeholders
[ ] On-call paged or notified
[ ] Rollback plan documented in PR description
[ ] Apply executed by named engineer (not bot)
[ ] Post-apply: drift re-checked within 30 min
[ ] Post-apply: smoke tests run against affected services
```

For P0 plans the checklist is moot — the gating is BLOCK and the plan is rejected.

### Step 10: Output Modes

The agent supports four output modes for different integration points:

| Mode | Format | Where It Plugs In |
|------|--------|-------------------|
| **review-comment** | Markdown PR comment with diffs + fixes | GitHub/GitLab PR |
| **gating-decision** | JSON `{decision, p0:[], p1:[], p2:[]}` | CI scripts |
| **slack-summary** | One-screen Slack post with deep links | Deploy channel |
| **runbook** | Markdown checklist + commands | Pre-apply prep |

## Worked Examples

### Example 1: Production Plan — Block

**Input (excerpt):**

```
# aws_db_instance.payments_prod will be destroyed
- resource "aws_db_instance" "payments_prod" {
-     identifier = "payments-prod"
-     engine     = "postgres"
-     ...
- }

# aws_iam_role_policy.deploy will be updated in-place
~ resource "aws_iam_role_policy" "deploy" {
~     policy = jsonencode(
~       {
~         Statement = [
~           {
~             Action   = "*"
~             Resource = "*"
~           },
~         ]
~       },
~     )
}

# aws_db_instance.payments_prod will be created
+ resource "aws_db_instance" "payments_prod" {
+     identifier = "payments-prod"
+     ...
+ }
```

Wait — same identifier, destroy then create? That's a `-/+` masquerading as separate destroy + create blocks because the resource address moved between modules. **Rule D4 fires (P0)**.

**Decision:** BLOCK
**P0:** D4 (DB recreate), I1 (IAM wildcard)

### Example 2: Drift With Import Suggestion

**Input:**

```
Note: Objects have changed outside of Terraform

  # aws_security_group.web has changed
  ~ resource "aws_security_group" "web" {
        id          = "sg-0a1b2c3d"
      ~ ingress     = [
          + {
              + cidr_blocks = ["192.168.10.0/24"]
              + from_port   = 22
              + to_port     = 22
              + protocol    = "tcp"
            },
          ...
        ]
    }

# aws_security_group_rule.ssh will be created
+ resource "aws_security_group_rule" "ssh" {
+     from_port   = 22
+     to_port     = 22
+     protocol    = "tcp"
+     cidr_blocks = ["10.0.0.0/8"]
+ }
```

**Findings:**
- X1 (P1): drift — someone added a 192.168.10.0/24 SSH rule outside Terraform
- X2 (P1): the new code adds a 10.0.0.0/8 rule, which conflicts with the manually-added one and will not remove it

**Suggested fixes:**
1. Import the manual rule first: `terraform import aws_security_group_rule.adhoc_ssh sg-0a1b2c3d_ingress_tcp_22_22_192.168.10.0/24`
2. Decide whether to keep both rules or consolidate
3. Re-plan and re-review

**Decision:** APPROVE_WITH_CONDITIONS — apply will succeed but state will remain inconsistent until the import is done.

### Example 3: Clean Plan

**Input (excerpt):**

```
# aws_lambda_function.x will be updated in-place
~ environment {
~     variables = {
~         LOG_LEVEL = "info" -> "debug"
    }
}
```

**Decision:** APPROVE
**Findings:** none
**Comment:** "Plan is clean. Single in-place env var update on a Lambda. No P-level findings. Apply approved."

## Output

The agent produces:

- **Severity-graded review** — every change classified P0/P1/P2/OK with rule citations
- **Single gating decision** — BLOCK / APPROVE_WITH_CONDITIONS / APPROVE
- **PR-comment markdown** — paste-ready into the PR thread
- **Suggested fixes** — code diffs and commands per finding
- **Pre-apply checklist** — for P1+ plans
- **Drift triage** — import / state-mv / state-rm commands per drift entry
- **CI workflow** — ready-to-commit YAML for GitHub Actions / GitLab CI / Atlantis
- **Slack summary** — one-screen status for the deploy channel
- **Cloud-specific notes** — AWS / GCP / Azure footguns relevant to this plan

## Common Scenarios

### "We use Terragrunt run-all — there's 40 modules"
The agent processes each module's plan independently, then aggregates: per-module decision plus a cross-module dependency check (e.g. module A destroys a KMS key that module B's plan still references). Cross-module references that fail produce an additional P0.

### "The plan shows no changes but production is different"
Drift outside Terraform. The agent runs through `terraform plan -refresh-only` mentally and flags X1 across the board. Fix: refresh-only apply, then audit which fields were touched and bring them under code or back to declared state.

### "Should we apply during business hours?"
Depends on findings. Clean P2-only plans: yes. P1 plans involving load balancers, DNS, or stateful resources: schedule for low-traffic windows. P0: never (and gate blocks anyway).

### "How do we handle plans with no JSON, only text?"
The agent's text parser handles standard plan output. JSON gives 100% accuracy on resource addresses and change reasons; text gives ~95% — the gap is mostly in nested module addresses and dynamic blocks.

### "Atlantis already gates — why use this?"
Atlantis enforces *who can apply*, not *whether the plan is safe*. This skill is the safety review; Atlantis is the policy enforcement. They stack.

## Tips for Best Results

- Provide the JSON plan (`terraform show -json plan.out`) when possible — disambiguates module addresses and change reasons
- Share the previous state file (or its summary) when reviewing drift — distinguishes "drift since last apply" from "first-time import"
- State the environment (prod / staging / dev) before review — gating thresholds shift; a P1 in prod may be a P2 in dev
- Mention any in-flight infra changes outside this PR — concurrent applies can produce false-positive drift
- Specify the cloud (AWS / GCP / Azure) explicitly — provider-detection is reliable but ambiguous for multi-cloud plans
- Indicate the apply executor (CI bot vs human, Atlantis vs Terraform Cloud vs spacelift) — gating recommendations adapt

## When NOT To Use

- **Pre-merge code review of HCL** without an actual `plan` — use `tflint` / `tfsec` / `checkov` for static analysis; this skill needs the rendered plan to grade destructiveness
- **Ad-hoc CLI applies on a laptop** without state in version control — fix the workflow first; reviewing a plan from an unknown state is reviewing fiction
- **Plans against an empty state** (initial bootstrap) — every resource is a `+ create`; the destruction matrix doesn't apply, run a separate bootstrap-review skill
- **Pulumi / CDKTF / CDK plans** — output format differs; this skill is HCL/JSON-plan specific. Use a CDK-specific reviewer
- **Helm / Kustomize / kubectl-apply** — Kubernetes-native deploys have a different risk model; use a k8s-manifest reviewer
- **Drift-detection-only runs** without intent to apply — those need a different output (drift report), not a gating decision
