# Failure Recovery Workflow

This file handles the `Failure Recovery` main path and applies to:

- `landing-zone-setup`
- `account-factory account create`
- `account-factory baseline apply`

## Core Principles

- By default, repair only the failed portion. Do not require a full rerun of the entire chain.
- Reconcile the current state first, then decide whether to backfill, retry, or stop.
- For cases such as `ConcurrentException`, partially landed resources, or inconsistent state, prefer a `partial success` interpretation instead of immediately calling the entire run a failure.
- Any real write action during recovery triggers G2. Present the impact summary first and get confirmation.
- Report only confirmed completed items, real blockers, and recommended next steps to the user. Do not expand internal troubleshooting details.

## Standard Flow

### 1. Identify the Failure Scope

- First determine whether the failure occurred in `landing-zone-setup`, `account-factory account create`, or `account-factory baseline apply`.
- Reuse the latest available workspace, plan files, output files, and read-only inspection results whenever possible.
- If the user only describes an error symptom, fill in the minimum context first: failed path, failed phase, latest error message, and whether any resources have already landed.

### 2. Reconcile the Current State in the Background

- For Terraform paths, first reread the current state, outputs, and latest plan context from the existing workspace.
- For steps supplemented by `ve` CLI actions, first use read-only APIs to confirm whether the resource has already been created, bound, or written successfully.
- If partial success is possible, do not rerun a same-name create action immediately. Confirm the current state first.

### 3. Decide the Recovery Strategy

- If the issue is only a missing prerequisite such as credentials, permissions, unwritable directories, or an unopened service, stop write actions first and tell the user to fix that prerequisite.
- If resources have partially landed, prefer incremental repair of incomplete items. Do not delete existing resources by default.
- If the current state has clearly drifted from the intended state, regenerate a plan before deciding whether to continue the repair.
- If the issue is a naming conflict, uniqueness conflict, or cross-account authorization problem, treat it as its own blocker instead of calling the entire blueprint failed.

### 4. Regenerate the Recovery Plan

- When needed, rerun `terraform plan`, `terraform plan -refresh-only`, or equivalent read-only checks to confirm what actions are still truly needed.
- Show the user only the post-recovery impact summary. Do not narrate internal refreshes, state extraction, or script reassembly line by line.
- If the recovery plan still contains real write actions, G2 applies: present the impact summary, get confirmation, then continue.

### 5. Output the Recovery Conclusion

- Final output must follow the result summary format from `interaction-contract.md`.
- Clearly distinguish which items were already complete, which items were repaired successfully in this run, and which items still require manual handling.
- If recovery completes and the main flow can continue, explicitly tell the user which path they can return to next.

## Common Recovery Scenarios

- **Concurrency conflicts**: reconcile the current state first, then replan. Do not immediately rerun apply.
- **Partial success**: split completed items out of the failed list and repair only what remains.
- **Missing prerequisites**: tell the user to repair the prerequisite first, then re-enter through the recovery path.
- **Enterprise organization creation hits `NoPermissionOnVerificationError`**: recognize this as missing enterprise real-name verification rather than a normal IAM permission gap. Guide the user to `https://console.volcengine.com/user/authentication/detail/` first, then retry from the `DescribeOrganization` or `CreateOrganization` branch.
- **Insufficient cross-account authorization**: recognize it as a permission problem, stop further writes, and do not misclassify it as a networking or logging blueprint failure.
- **Leftover temporary log profile from `04-log`**: if the previous run was interrupted in `04-log`, a temporary log profile may still exist and the original default profile may not have been restored. During recovery, detect and clean up the dangling temporary profile first, confirm that the default profile is restored, and only then re-enter `04-log` to avoid a dirty login state.
- **Tag, finance relationship, or organization read-only checks disagree with expectations**: trust the read-only API result first and confirm whether any backfill is still needed.
