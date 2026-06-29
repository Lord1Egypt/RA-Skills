# Account Factory Workflow

Use this guidebook to create standardized accounts inside the Landing Zone and optionally apply baselines after account creation.

## Core Principles

- The main workflow is always account creation. Baseline is an optional enhancement, not a prerequisite.
- Stepwise pause mode is enabled by default. Do not chain account creation, baseline selection or creation, and baseline apply into one uninterrupted long run.
- Account creation must determine OU placement, finance relationship, and tags. Baseline handles only standard configuration after the account exists.
- Baseline execution prefers Terraform first and uses `ve` CLI only when supplementation is necessary.
- Any `ve` CLI supplementation must follow the real parameter contract of the action. Do not assume every action supports the same `--body` shape.
- When multiple baselines are used together, merge them in the user-selected order. Later selections override earlier ones.

## Checklist Conventions

If tasklists or checklists are available, account factory should be represented inside the unified six-step `volcengine-landing-zone` checklist with `06-account-factory` as the entry.

- When skipped steps can remain visible, prefer to keep the full six-step structure and mark the first five steps as skipped.
- If showing skipped steps is not a good fit, create at least one clearly named entry called `06-account-factory`.
- After entering account factory, it is recommended to create a three-step sub-checklist: `Build Account Baseline`, `Create Account`, and `Apply Baseline`.
- Keep the three-step structure even when this run does not need a baseline. Mark the related steps as skipped instead of deleting them.

## Runtime Directories

> See the `Path Anchors` section in `SKILL.md`: `./skills/...` resolves to `${SKILL_ROOT}/...`, and `./volcengine-landing-zone-workspace/...` resolves to `${WORKSPACE_ROOT}/...`.

- Runtime root: `${WORKSPACE_ROOT}/` (that is, `./volcengine-landing-zone-workspace/`)
- Blueprint source directory: `./skills/volcengine-landing-zone/assets/blueprints/` (see G3: built-in blueprints are read-only)
- Execution copy directory: `./volcengine-landing-zone-workspace/blueprints/` (real execution runs here under G3)
- Baseline directory: `./volcengine-landing-zone-workspace/account-factory/baseline/`
- Baseline runtime-state directory: `./volcengine-landing-zone-workspace/account-factory/runs/`
- Customer custom Terraform directory: `./volcengine-landing-zone-workspace/account-factory/custom-terraform/`
- Baseline schema: `skills/volcengine-landing-zone/references/account-factory/baseline.schema.json`

## Preflight Focus

The general rules come from [../preflight-checks.md](../preflight-checks.md). This path focuses on confirming:

- Current credentials are valid and the Terraform Provider can read the Volcengine authentication available in the current process.
- The minimum input for account creation is complete.
- Baseline-related directories can be created automatically.
- If a baseline must be applied, the target `*.baseline.json` exists and conforms to `baseline.schema.json`.
- If `terraform plan` reports `Either (AccessKey and SecretKey) or Profile must be provided`, go back to preflight and repair provider authentication injection instead of asking the user to hand-edit files.

## Standard Flow

The default rhythm is: explain before execution -> summarize results after execution -> confirm again before the next task.
`Create account` and `apply baseline` are each their own task. Each triggers G2, and write actions inside the task run continuously without per-write prompts. Authorization does not carry across tasks because of G6.

### 1. First-Round Minimum Input

Collect only the required input for account creation in the first round:

- `account_name`
- `show_name`
- `target_ou_id`
- `account_tags`

Delay the following until they are truly needed:

- `financial_relation_type`
- `financial_relation_auth_list_str`
- `admin_email`
- `network_account_id`
- `transit_router_id`

### 2. Confirmation Before Creation

Before real creation, show the account summary to the user and ask only for the still-missing variables that are truly required to continue.

- If the finance relationship is not yet clear, then ask for `financial_relation_type` and, when required, `financial_relation_auth_list_str`.
- If `financial_relation_account_alias` is not specified, it may default to `account_name`. When the default alias conflicts, the blueprint automatically retries once by appending the account ID suffix. If the user explicitly provided an alias and it conflicts, stop and ask the user to rename it.
- When the network baseline is enabled, require explicit values for `workload_vpc_cidr`, `workload_subnet_cidr_az_a`, and `workload_subnet_cidr_az_b`. Do not auto-fill fallback CIDRs.
- Describe baseline briefly in business language and make its optional nature clear. Do not expand internal implementation details at this stage.

Then ask the user to choose:

- create the account only
- create the account and select an existing baseline
- create the account and create a baseline now

Then stop under G2/G6 and wait for explicit confirmation for the `create account` task.

### 3. Select or Create a Baseline

When selecting an existing baseline:

- scan `account-factory/baseline/`
- list only `*.baseline.json`
- support multi-select

When creating a baseline on the spot:

- the currently supported built-in module is `network-cross-account-connectivity`
- explain first that this module connects a workload account into the enterprise shared network
- ask whether customer custom Terraform modules should also be included
- generate baseline JSON from `baseline.schema.json`
- ask the user to confirm the baseline name, file name, variables, and module summary
- when the file name conflicts, ask the user to rename it

After selection or creation is complete, summarize in user-facing language what was selected or created and what will run next, then wait for confirmation to continue.

### 4. Create the Account

- Run `terraform init`, variable preparation, and `terraform plan -parallelism=1 -out=tfplan` in the background.
- Under G2, confirmation for this task covers the account creation itself plus its follow-up CLI write actions. Do not interrupt for each individual internal write.
- After confirmation, run `terraform apply -parallelism=1 tfplan`.
- If the account has already been created successfully but post-create CLI steps such as finance relationship or tags fail, treat it as partial success. Do not delete the account and do not rebuild from scratch.
- For those failures, inspect the current state first, then backfill the failed `null_resource` steps through another `plan/apply`.

Read-after-write validation and CLI conventions:

- After finance relationship creation, validate with `ve billing ListFinancialRelation`.
- After account tags are written, validate with `ve organization ListTagResources`.
- Even if `CreateFinancialRelation` returns a duplicate or already-exists style result, do not treat it as success without read-after-write validation.
- Finance relationship actions currently use `--body`.
- Tag-related actions currently use numbered `.1/.2` style parameters instead of a JSON body.
- The `CreateFinancialRelation` body should be organized with `SubAccountID`, `Relation`, optional `AuthListStr`, and optional `AccountAlias`. Follow `--help` for the exact field names.
- Treat `AccountAlias` conflicts as alias uniqueness issues, not as an `already exists so skip it` case.

After account creation completes, follow G2/G6: output the result summary first, then ask whether to continue with baseline. Do not automatically enter the next step just because the user previously selected a baseline path.

### 5. Apply the Baseline

- The agent reads the selected `*.baseline.json` files directly, merges them in order, and lets later selections override earlier ones.
- Identify the final enabled modules and variables first, then normalize them into the runtime payload.
- The current built-in module is `network-cross-account-connectivity`. Ask for missing minimum variables only when that module is actually enabled.
- When cross-account network connectivity is enabled, check the cross-account `AssumeRole` prerequisite only once right before entering that module. If the current login comes from the primary account, stop and ask the user to switch to an IAM sub-user with `STSAssumeRoleAccess`.
- Before entering that module, ensure the target workload account already has `ServiceRoleForTransitRouter`. Prefer running `ve iam CreateServiceLinkedRole --ServiceName transitrouter`, and treat `RoleAlreadyExists` as already authorized.
- Customer custom Terraform modules should preferably use paths relative to the runtime root, such as `account-factory/custom-terraform/<name>`.
- In the background, run `terraform plan/apply -parallelism=1` inside the workspace execution copy at `account-factory/baseline-apply/`, passing `workspace_root` explicitly.
- Show only a concise impact summary to the user. Do not expand configuration shaping, script generation, or extension-module preparation details.
- G2 applies to this task: one confirmation covers the current baseline apply and internal writes run continuously.

After baseline apply completes, follow G6: output the result summary and any manual follow-up items first, then explain whether to continue with further account configuration or start the next account-factory run.

## Result Output

Final output follows the unified result summary format in [../interaction-contract.md](../interaction-contract.md) and must include at least:

- basic information of the new account
- which baselines were used
- which baseline segments were applied automatically
- which items still require manual handling
- the recommended next step
