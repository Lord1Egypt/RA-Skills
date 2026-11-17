# Customer support

Use this module to investigate a Whop purchase problem and prepare a reply. It covers failed payments, missing access, refunds, duplicate payments, and questions before purchase. It does not authorize sending messages, retrying charges, changing access, or moving money.

The investigation checklists are recommended operating practices. Whop-specific navigation is sourced below and was checked on 2026-09-29. Confirm the current interface and the exact account before using a procedure.

## Rules for every case

- Start in an authorized, private support channel. Verify the customer through the platform's supported process before disclosing purchase details or changing access. Do not reveal whether another account has a purchase.
- Retrieve existing case and purchase information before asking the customer to repeat it. If necessary, request only the product, purchase date, and receipt reference through the private channel.
- Never request passwords, full card numbers, security codes, sign-in codes, recovery codes, or bank credentials. The customer enters sensitive information directly into Whop or their bank's secure interface.
- If a screenshot is needed, ask for the relevant error or transaction only, with unrelated purchases, balances, contact details, and payment details redacted. Do not request a full bank statement.
- Distinguish payment, subscription, access, refund, and dispute states. A bank entry, receipt, or customer report is useful evidence, but does not establish every state.
- Draft first. A human approves the exact recipient, final message, attachments, and timing before every send. Refunds, charge retries, cancellations, access changes, and other mutations need separate approval of their effects.
- Read the exact resource back after an approved action. Do not report "refunded," "canceled," "paid," or "fixed" from a button click or a success toast alone.
- Do not promise a refund policy, grace period, response deadline, or delivery benefit that the seller has not approved. Record a next-update time only when the responsible person can meet it.

### Case record

Keep this record private. Bracketed fields are instructions, not sample customer data.

```text
Issue: [failed payment / missing access / refund / duplicate / before purchase]
Verified customer and business: [restricted reference]
Product and offer terms at purchase: [verified facts or unknown]
Payment: [state, amount, currency, time, and source]
Subscription and entitlement: [current states or unknown]
Refund or dispute already open: [state or none found after checking]
Customer's requested outcome: [their request]
Evidence and gaps: [what was checked; what remains unverified]
Proposed action: [one bounded action or read-only investigation]
Human approval: [message approval and any separate financial approval]
Next update: [agreed time and responsible role]
Closure evidence: [exact result; buyer confirmation if needed]
```

## Failed payment

### Investigate before suggesting another attempt

1. Determine whether this is an initial purchase or a subscription renewal. Check the exact payment, its latest attempt, and any successful payment for the same intended purchase.
2. Read the payment and subscription states. If the outcome is pending or uncertain, do not ask for another purchase. Check for an existing charge before a retry.
3. Use the actual decline information when available. Never invent insufficient funds, fraud, or a bank restriction as the cause. Keep sensitive risk information out of an unnecessary customer-facing explanation.
4. For a failed renewal, check the current recovery state and the seller's access-while-past-due settings. Do not promise uninterrupted access or a particular retry schedule from memory.
5. Direct the customer to [membership settings](https://whop.com/@me/settings/memberships), select the affected membership, and choose **Update Payment Method**. The customer supplies billing details there. Explain that payment recovery can charge the saved method; do not create a new subscription to repair the old one.
6. If a manual retry is appropriate, obtain approval for the exact payment and amount, confirm the customer's intent to complete that payment, and check whether another attempt is already in progress. Read the outcome before any further retry.
7. After a successful payment, verify the entitlement and the buyer-visible access separately.

Whop documents renewal recovery and the customer update flow in [Failed subscription payments](https://docs.whop.com/payments-and-billing/payment-issues/troubleshoot-failed-payments). An initial checkout failure does not necessarily follow the renewal process. If the customer needs another attempt, use the original verified offer and secure checkout only after checking that the intended purchase did not already succeed.

### Reply: failed renewal confirmed

Use only after checking that the renewal has not succeeded elsewhere.

```text
The renewal payment for [product] has not completed.

Open https://whop.com/@me/settings/memberships, select the affected membership, and choose Update Payment Method. Enter any payment details directly in Whop, not in this conversation. Whop may retry the outstanding renewal as part of payment recovery.

Please do not start a new subscription for the same product. If the payment succeeds but access is still unavailable, send the error text through this support thread so we can check the access stage.
```

### Reply: outcome still uncertain

```text
I cannot yet confirm the outcome of the payment for [product]. Please do not submit another payment while we check the existing attempt.

[Specific missing item, only if needed: purchase date or receipt reference.] Please keep card details and sign-in codes out of this conversation.

The next update is due by [confirmed time and timezone].
```

Avoid repeated retries, promises that the bank will approve a card, and a new checkout that charges the customer again.

## Access not received

### Locate the failing stage

1. Match the intended purchase to the correct Whop business and customer. Confirm payment status and the purchased offer's actual access terms.
2. Ask the customer to find their Whop order confirmation and sign in using the same address that received it. Never ask them to send the sign-in code to support.
3. Check that the membership grants the intended product, is in an eligible state, and has not expired, been refunded, or been canceled in a way that ends access.
4. Check the product's delivery configuration. A paid product may lack the intended content attachment, or the customer may still need to claim access in an attached app. Installation of an app is not proof of correct product access.
5. Use the buyer's account or an explicitly authorized buyer test. Administrator access can make a broken customer flow look functional.
6. If a correction is needed, obtain approval for the exact entitlement or delivery change. Do not grant access to unrelated paid products or ask the customer to buy again.
7. Verify the affected experience. For a download, check the actual file; for a community, verify buyer entry; for a service, verify the promised booking or delivery route. A stored redirect alone proves none of these.

The receipt-based recovery flow is documented under [Find a missing purchase](https://docs.whop.com/memberships-and-access/cancellations-and-refunds/request-a-refund#find-a-missing-purchase).

### Reply: help the buyer find the purchase

```text
Please find the Whop order confirmation for [product] and select its Access button. Sign in to Whop using the same address that received the receipt, even if you normally use another account.

Enter any sign-in code only on Whop. Please do not send it here, and do not buy the product again.

If access is still missing, send the page's error text through this private support thread. A screenshot is optional; hide unrelated purchases and personal or payment details.
```

### Reply: entitlement corrected, buyer check still needed

Use only after the exact entitlement correction has been read back.

```text
The access setting for [product] has been corrected on the purchase account.

Please sign in to that account and open [verified access page]. I have verified the saved access setting; please confirm whether you can now [open the course / download the file / enter the community].

If it still fails, reply with the error text. No additional purchase is needed.
```

Do not mark this case fully resolved if only the administrator's view works. Record buyer access as unverified until an authorized buyer check or the customer's confirmation establishes it.

## Refund request

### Prepare a decision without promising one

1. Find the exact payment, amount, currency, earlier refunds, and any open claim or dispute. Check whether Whop has already handled a refund automatically, including a financing-related case, before initiating anything.
2. Review the offer and refund terms that applied at purchase, the customer's stated issue, and the evidence. Escalate questions about consumer rights or disputed terms to a responsible human; a seller policy does not remove statutory rights.
3. Record whether the request concerns a full refund, partial refund, future renewal cancellation, or several separate actions. Refunding a payment and canceling future billing must each be checked; do not assume one implies the other.
4. Obtain human approval for the exact payment, amount, currency, reason, and any access or subscription consequence. If funds or permissions are insufficient, escalate; do not fund the account or change payout settings yourself.
5. Before an approved refund, re-read the payment and claim to avoid racing an automatic refund or another operator. In Whop, the documented merchant routes include **Dashboard > Payments** and **Dashboard > Resolution Center**. Accepting a claim can process a refund; it is not just an acknowledgment.
6. After execution, read the refund and payment back. Distinguish pending, succeeded, failed, and any partial amount. Check the subscription and entitlement separately. Resume an uncertain operation from its saved reference instead of issuing another refund.
7. Tell the customer only what that evidence establishes. Processing in Whop is distinct from the money appearing at their bank.

Sources: [Refunds](https://docs.whop.com/manage-your-business/manage-payments/issuing-refunds), [Resolution Center](https://docs.whop.com/payments/resolution-center), and [Refund payment](https://docs.whop.com/api-reference/payments/refund-payment).

Whop's refund guide, checked on 2026-09-29, gives a typical bank or payment-method arrival time of 3-7 business days after processing. This is a public estimate, not a guaranteed deadline. Recheck the guide and actual refund state before quoting it; the templates below avoid turning it into a promise.

### Reply: request received

```text
I have received your refund request for [product]. The next step is to check the payment and the terms that applied to your purchase. No refund is confirmed yet.

[Ask one necessary question, or remove this line if the case already has enough information.]

You can also open your Whop profile, select Orders, find the payment under Billing history, and use the three-dot menu to select Request Refund. If you already have a case, keep the discussion in that case rather than starting another request.

The next update is due by [confirmed time and timezone].
```

The customer navigation above comes from [Request a refund](https://docs.whop.com/memberships-and-access/cancellations-and-refunds/request-a-refund). If that option is unavailable, inspect eligibility and ask official Whop support for the supported route. Do not invent an alternative policy or ask for bank details to send money elsewhere.

### Reply: refund succeeded in Whop

Use only after success, amount, currency, and consequences are verified. For a pending refund, explicitly say it is pending instead.

```text
Whop confirms that the [full / partial] refund of [amount and currency] for [product] was processed on [date].

The time for it to appear in your account depends on your bank or payment method. This confirms processing in Whop, not receipt by your bank.

Future billing: [verified subscription state].
Access: [verified entitlement state and effective date, if relevant].
```

For a denial or contested claim, have the human review the facts and applicable rights before replying. State the specific reason and the available Whop review route. Never pressure the customer to withdraw a dispute or give up rights as a condition of receiving support.

## Suspected duplicate payment

### Reconcile before refunding or canceling

1. Ask the customer not to submit another payment. Read all relevant attempts for the intended purchase.
2. Compare the payments' customer, product, billing period, timestamp, amount, currency, and status. Deduplicate records by their private payment references, not amount alone.
3. Distinguish a settled payment from a pending authorization, a failed attempt, an installment, a renewal, and a separate purchase. Matching bank amounts do not prove a duplicate charge.
4. If only a bank-side entry is visible, request a redacted view of the relevant entry or ask the customer to check its pending/posted status with their bank. Do not guarantee when a hold will disappear.
5. If a duplicate is confirmed, obtain approval for the exact corrective action. Check which membership and entitlement each payment controls so the legitimate purchase remains usable.
6. Re-read the corrective refund and the remaining payment, subscription, and access. Do not cancel the entire subscription to solve an extra payment unless that separate action is also approved.

These are reconciliation safeguards, not a claim that every payment method handles duplicate-looking entries in the same way. Use the verified refund flow above when a refund is appropriate.

### Reply: investigation

```text
Please do not make another payment for [product] while we check the entries.

We need to distinguish a second completed payment from a pending authorization or another billing event. [Ask only for the missing purchase date or receipt reference.]

If we need a screenshot, please show only the relevant entries and hide card details, balances, and unrelated transactions. We will confirm what the records show before proposing a correction.
```

### Reply: duplicate correction verified

```text
We confirmed a duplicate payment for [product]. Whop shows that the extra payment of [amount and currency] was refunded on [date]. Your intended purchase remains [verified payment state], and its access is [verified access state].

Bank or payment-method posting time can vary. Future billing remains [verified subscription state].
```

Do not use this confirmation for a pending refund or an unresolved entitlement. Replace it with the actual current state.

## Questions before purchase

### Answer from the current offer

Check the seller's approved product page, the exact checkout, and the delivery terms. Separate inclusions, access duration, payment schedule, renewal, cancellation, refund conditions, support scope, and buyer eligibility. Display currency and merchant settlement currency can differ; describe what this buyer will be charged, using the current checkout.

A payment option advertised by Whop generally is not proof it is enabled or available for this seller and buyer. A coaching session, personal feedback, community, certificate, or ongoing support is included only if the approved offer says so. Do not invent availability, outcomes, testimonials, discounts, or a response-time promise.

### Reply: verified offer summary

```text
[Product] includes [verified inclusions]. It does not include [important verified exclusions].

Payment: [verified amount, currency, taxes or fees as shown, and billing schedule].
Renewal: [one-time purchase or verified recurring terms].
Access: [duration, start conditions, and actual delivery steps].
Support: [approved scope and channel].
Cancellation and refunds: [accurate summary and verified policy link].

You can review the current checkout before deciding: [verified checkout link].
```

Remove fields that do not apply rather than inventing answers. If a material term is unknown, do not send a purchase recommendation. Use this holding reply after human review:

```text
I need to confirm [specific missing term] before recommending this purchase. The current information does not establish it, so please do not rely on that benefit yet.

The next update is due by [confirmed time and timezone].
```

## Escalation and closure

Escalate suspected account takeover, an unrecognized charge, a disputed identity, conflicting payment records, inaccessible account data, or a legal complaint to the responsible human and official Whop support as appropriate. Do not bypass a security control or infer that a denial of access means no purchase exists. For an unrecognized charge, tell the customer to secure the affected account and contact their bank through its trusted channel.

Before the human approves a final reply:

- [ ] Customer, business, product, and intended payment have been matched privately.
- [ ] Claims in the reply match current evidence, not a proposed action.
- [ ] All bracketed instructions have been replaced or removed.
- [ ] Existing retries, refunds, claims, and other operators have been checked.
- [ ] No credentials, unnecessary personal data, or unrelated account details appear.
- [ ] Any financial or access change has separate approval and exact readback.
- [ ] The reply distinguishes processing from bank receipt and saved access from buyer access.
- [ ] A remaining gap has a responsible owner and a realistic next update.

Close the case when its agreed outcome is verified. If the customer has not confirmed access or the refund is still pending, record that boundary and follow the seller's approved follow-up process instead of marking an unsupported success.

## Sources

Official documentation checked on 2026-09-29:

- [Failed subscription payments](https://docs.whop.com/payments-and-billing/payment-issues/troubleshoot-failed-payments): renewal recovery, access-while-past-due settings, and payment-method updates.
- [Request a refund](https://docs.whop.com/memberships-and-access/cancellations-and-refunds/request-a-refund): customer refund navigation and locating a purchase through its receipt.
- [Refunds](https://docs.whop.com/manage-your-business/manage-payments/issuing-refunds): merchant refund routes, automatic handling, and typical posting estimate.
- [Resolution Center](https://docs.whop.com/payments/resolution-center): claims, responses, platform decisions, and appeals. Check the case's actual deadline and current rules.
- [Refund payment](https://docs.whop.com/api-reference/payments/refund-payment): payment refund operation and returned payment data.
