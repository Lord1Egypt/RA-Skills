# Spend policy and ride approval

The server is authoritative. Limits use USDC and rolling windows: the last 24 hours, 7 days and 30 days. Keep existing receipt/tip accounting; do not substitute calendar periods or completed-ride-only sums. Per-ride caps do not apply to tips.

## Basic ride flow

1. Search and let the user choose a vehicle. Call `ride-request` with the selected ride JSON. Before creating a RideRequest, the server checks the validated USDC fare against per-ride and rolling limits. A pre-creation `POLICY_EXCEEDED` includes the blocking axis, cap, attempted and spent amounts; it has no rideRequestId. No request or approval record has been created.
2. Read `amb policy --wallet WALLET`, explain the blocking limits and ask for **approve this ride once**, **raise limits**, or **stop**. Choose before issuing a link.
3. Keep the original ride JSON. If its search expired (3 minutes) while the user decided, `approval-request` searches the same trip once and issues the link with the fresh quote; when quote_refreshed is true, show the returned price and price_currency as the current fare before the user approves. If the product or currency disappears, stop. For one-time approval, issue a link for this trip; policy stays unchanged. For a raise, request the link using the same ride JSON and signed search quote. The server proposes spent plus twice the fare for exceeded rolling limits (twice the fare for per-ride); other limits remain unchanged. Explain the returned current/proposed amounts. The link is an editable form: the user can choose a final amount between the displayed minimum and maximum. The minimum is fixed at link issuance: max(current limit, spent plus fare). Unchanged fields are not written. Respect server maxima and use exact USDC arithmetic.
4. The link request stores the owner, wallet and trip details with no RideRequest ID. Present the link, then poll. Direct human approval is the default; user-authorized agent assistance is allowed. The initial ride instruction does not authorize automatic approval. Link creation/viewing does not apply a decision.
5. After APPROVED or APPLIED, call `ride-request` with the same ride JSON plus `approval_id`. If the local search cache is missing or expired (3 minutes), the command searches the same trip once and submits the fresh quote with the same approval_id. It keeps the chosen product, currency, wallet, route and rider; if the product or currency disappears, stop. When quote_refreshed is true, show the returned current fare before payment. Do not create another approval solely because the quote price changed. The server validates the trip against the approval; a raise rechecks policy and is not a one-time exception.
6. The server creates the actual RideRequest and links it to the approval within the existing creation transaction. Only now does the existing payment waiting period start. Preserve the returned request_id, then follow existing `ride-pay-prepare`, signing and confirmation under the user's payment authorization.

```bash
amb policy --wallet WALLET
amb approval-request 'RIDE_JSON_FROM_THE_DENIED_CALL' once
amb approval-request 'RIDE_JSON_FROM_THE_DENIED_CALL' raise
amb approval-status APPROVAL_ID WALLET
amb approval-wait APPROVAL_ID WALLET [--timeout SECONDS]
amb approval-cancel APPROVAL_ID WALLET
# Add "approval_id":"APPROVAL_ID" to the original ride JSON, then:
amb ride-request 'RIDE_JSON_WITH_APPROVAL_ID'
amb ride-pay-prepare REQUEST_ID WALLET
```

`RIDE_JSON_FROM_THE_DENIED_CALL` is a placeholder for the same JSON object accepted by `ride-request`, including wallet_address, search_id, product_code, region, pay_currency, locations and rider. It is not a RideRequest ID. `approval-wait` polls every two seconds for up to 90 seconds by default (`--timeout` 1-600) so it fits host tool timeouts, and retries network errors, timeouts and HTTP 5xx within that window. If it returns PENDING, run it again while PENDING; the server reports EXPIRED from its own `expiresAt`. It never creates a ride, signs or pays. Keep the approval ID. A successful creation links a request ID; subsequent status guidance uses that existing request. Approval links are capabilities: do not put them in shared logs or telemetry.

## Stop conditions and scope

- `CANCELLED`, `EXPIRED`, or a non-payable RideRequest: stop. Do not automatically create another request, approval or link. Approval cancellation does not itself cancel the RideRequest; use the existing ride cancellation command if the user wants to cancel the ride.
- If an applied raise still leaves a blocker, explain the remaining limit and stop; do not loop by creating replacement requests.
- A status or link request failure is not approval. If an approval ID is known, check it. Do not automatically repeat link issuance or silently switch action after an ambiguous response. Lost response recovery is a separate decision.
- `POLICY_WALLET_MISMATCH`: verify the selected wallet/authentication; never switch wallets to bypass a limit.
- `POLICY_UNAVAILABLE`: explain that the server could not check the policy. Never assume permission to pay.
- `POLICY_HARDMAX_EXCEEDED`: leave policy unchanged and explain the maximum.
- Payment submission failure or an ambiguous result belongs to existing payment recovery. Approval does not establish whether crypto settled.
- The 3-minute cache lifetime is a local lookup rule, not a TADA price guarantee. Recovery happens only before request creation: in `approval-request`, and in `ride-request` with an approval_id. No approval/request deadline is renewed. The refreshed fare is used when creating the request and receipt, before payment preparation and signing. After-payment failures follow the existing payment recovery policy.
- A payment-stage POLICY_EXCEEDED on an already-created request is a remaining blocker: report it and stop. The creation-time approval command does not issue exceptions for existing requests.

TADA Mini and member/card rides do not enter this agent approval flow. A valid one-time approval is usable only for its original request and wallet before expiry; it does not change limits for the next ride. A policy raise affects later requests too.

Standalone `amb policy set --daily 80` remains available for explicitly requested policy management. Do not use it to bypass the link step in an over-limit ride flow. For tips, preserve the existing policy-management/payment flow; ride approval does not cover tips.

Example: “This ride is 20 USDC. Your 24-hour limit is 50 USDC and you have spent 40 USDC. Would you like to approve only this ride, raise your limit, or stop?” If the user chooses higher limits: “I can propose 80 USDC for the last 24 hours (40 spent + twice this 20 USDC fare), keeping your weekly and monthly limits unchanged. The link lets you edit the amount, with a minimum of 60 USDC, before approving.” Substitute only observed values.
