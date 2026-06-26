# Sure API Playbooks

## Playbook 1: Monthly Spend Summary

1. List accounts.
2. List transactions for relevant period.
3. Group by category and month.
4. Return:
- total spend
- top categories
- largest single expense

## Playbook 2: Fix Transaction Category

1. Retrieve transaction by id.
2. Retrieve categories and confirm target category id.
3. Patch transaction with new `category_id`.
4. Retrieve transaction again and confirm field update.

## Playbook 3: Create and Tag Expense

1. Create transaction with required fields.
2. Retrieve available tags.
3. Patch transaction with `tag_ids` if needed.
4. Re-read transaction and return final state.

## Playbook 4: Import CSV Transactions

1. Validate account id exists.
2. Build import payload using CSV content and column mapping.
3. Create import.
4. Retrieve import status by id.
5. If failures occur, return column mapping hints and date format corrections.

## Playbook 5: External Assistant Validation

> **Opt-in only:** This playbook runs only when the user explicitly requests external-assistant validation. Do not execute it during normal API usage.

1. Confirm Sure instance is running.
2. Confirm chat endpoint works with API key.
3. Only if the user has opted into external-assistant mode, verify these env vars are set (do not prompt for them otherwise):
   - `MCP_API_TOKEN`
   - `MCP_USER_EMAIL`
   - `EXTERNAL_ASSISTANT_URL`
   - `EXTERNAL_ASSISTANT_TOKEN`
4. Validate chat message flow and retry endpoint.
