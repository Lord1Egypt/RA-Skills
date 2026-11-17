# SpendCap acceptance

1. Receipt is connected once and an existing healthy connection is reused.
2. Exactly eight universal Receipt tools are present and no seller-specific tool is present.
3. The owner can select the trusted connected app and create positive daily and per-purchase
   limits without a quote or purchase; an unfunded account receives a visible funding warning.
4. The current record is loaded instead of creating an overlapping active or paused record.
5. Setup makes no purchase, launch-credit use, provider call, hold, reservation, transaction, or
   wallet movement.
6. Edit preserves prior values in append-only history.
7. Pause blocks the next purchase before provider execution; Revoke permanently ends the grant.
8. The UI states that SpendCap controls purchases made through Receipt.
9. Names, limits, statuses, and approval URLs in user messages come from real Receipt responses.
10. Free `receipt_get_account` returns the canonical `spendcap` and saved limits before setup is
    declared complete.
11. Get with Receipt remains a separate outcome-acquisition skill at version 1.0.7.
12. Before recommending numbers, setup reads the connection hard maximums from free
    `receipt_get_account` and offers only those amounts or lower.
13. A request above either maximum explains the valid range and directs the owner to the SpendCap
    management page without claiming setup failed permanently.
14. A zero connection maximum is explained as no spending authority; a null or missing maximum is
    treated as unavailable and never invented, coerced to zero, or assumed unlimited.
