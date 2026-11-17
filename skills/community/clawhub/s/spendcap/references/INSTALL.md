# Install SpendCap

1. Run `bash "{baseDir}/scripts/bootstrap-receipt.sh"`.
2. If the script reports `RECEIPT_CONNECTION_REUSED`, do not start another authorization flow.
3. Otherwise show the exact Receipt authorization URL and wait for the owner to approve it.
4. Complete the localhost callback with the printed clipboard-helper command.
5. Verify that the Receipt connection exposes exactly eight universal tools.
6. Call free `receipt_get_account`, explain the returned connection daily and per-purchase maximums,
   and never recommend a value above either maximum.
7. Open the attributed owner page printed by the script and ask the owner to select the connected
   app, choose those limits or lower, and create or confirm its SpendCap.
8. Read the saved canonical SpendCap, status, and limits back from `receipt_get_account` before
   stating that SpendCap is active.

Do not browse the seller catalogue, request a quote, use launch credit, call `receipt_purchase`,
create a hold or reservation, or make any provider call as part of setup.
