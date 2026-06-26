# Tuya Account Linking and Device Ownership

Use this guide when device control depends on user-bound accounts and homes.

## App Model Matters

Tuya documents different account behavior by app type:

- Custom Development app:
  - Supports real app accounts linked to Tuya cloud project context.
  - Typical for production mobile app + cloud control flows.

- SaaS Development app:
  - Uses virtual account behavior for testing and service workflows.
  - May not represent full real-user app-account binding behavior.

Do not assume device ownership APIs behave the same across these models.

## User Permission Package Requirements

Before user-scoped device operations, verify:

- Project has user permission package configured.
- App account and cloud project are mapped correctly.
- Data center alignment is consistent across app and OpenAPI host.

## Recommended Linking Flow

1. Confirm app model and region.
2. Confirm user account synchronization status.
3. Query user device list from user-scoped APIs.
4. Validate each target device is visible in both discovery and control paths.
5. Only then build command execution plans.

## Consistency Checks

- Device appears in user list but command endpoint fails -> check permission scope and project authorization.
- Device appears in cloud list but not app user list -> check app-account linkage.
- Home/room metadata missing -> reconcile user binding before automation setup.

## What to Store Locally

Keep concise, non-secret notes in `~/tuya/environments.md`:
- app model in use
- region and endpoint mapping
- user-linking assumptions validated
- known account-specific restrictions
