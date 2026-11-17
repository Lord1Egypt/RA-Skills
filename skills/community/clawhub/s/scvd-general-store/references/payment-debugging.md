# Payment diagnosis

Start with the existing request, response/error, chosen network, transaction
identifier if known, and the original idempotency key. These are evidence;
never ask for wallet secrets or a new signed payment to investigate an error.
A timeout or HTTP error alone does not prove that money moved or did not move.

1. If an `order_id` exists, read `GET https://scvd.store/api/order/{order_id}`
   or the connected `check_order` tool. Verify an existing artifact for free.
2. If the response disappeared, use free wallet-proven recovery:
   `POST https://scvd.store/api/claims/challenge`, then the authorized wallet
   signs the challenge locally, then `POST https://scvd.store/api/claims`.
   The challenge is SIWX (CAIP-122); a bare wallet address is not proof.
   It returns open orders and instant-purchase certificates with verify URLs.
3. Preserve the original request and `Idempotency-Key`; do not rotate either
   as an error-recovery tactic or make a new payment to find out what happened.
   See [purchases](purchases.md) for retry windows, wallet binding and refunds.
4. For a malformed quote or client selection issue, use free `preflight_endpoint`
   or `check_before_you_pay`, or their HTTPS endpoints in
   [inspection](inspection.md). Neither sends payment to the target.
5. If the user needs a new signed observation of settlement, consult
   `settlement_attestation` in the fresh menu. Reconciliation distinguishes
   a declared authorization ceiling from one actually observed on chain.
   These are paid products and require a separate spending decision.

Choose the chain explicitly from the item's input contract: identical EVM
transaction-hash shapes do not distinguish Base, Polygon or another EVM chain.
Inspection-network support and checkout-network support are different lists;
current quotes say which networks can pay. Report unresolved settlement or
delivery as unknown. The keeper pays refunds manually; recovery is not a
promise of an automatic refund.
