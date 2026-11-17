# Disputes — Chargebacks, Evidence, and Keeping the Rate Down

**Before answering any dispute**, read `disputes/<year>.md` and any evidence packet in `artifacts/` that `## Boxes` names — what won last time for this reason code is worth more than a fresh draft. At the monthly review, read `## Volume & Fees` too: the rate is disputes over transactions, and both numbers live there.

**Contents:** [What a Dispute Actually Is](#what-a-dispute-actually-is) · [The Only Date That Counts](#the-only-date-that-counts) · [Fight, Refund, or Accept](#fight-refund-or-accept) · [Evidence by Reason Code](#evidence-by-reason-code) · [Building an Evidence Packet](#building-an-evidence-packet) · [Early Fraud Warnings](#early-fraud-warnings) · [The Dispute Rate and Network Programs](#the-dispute-rate-and-network-programs) · [Prevention, in Order of Return](#prevention-in-order-of-return) · [Inquiries and Retrieval Requests](#inquiries-and-retrieval-requests)

## What a Dispute Actually Is

The cardholder complained to their bank, and the bank pulled the money back. It is not a support ticket and it is not a refund: the funds and a per-dispute fee are withdrawn from your balance immediately, and the fee stays gone whether you win or lose.

You are not arguing with the customer. You are submitting evidence to the issuing bank, which decides on documents, not on being right. The customer never reads what you write.

Consequences that follow directly:
- Winning restores the disputed amount, not the fee.
- The economics of fighting are `amount × win_probability` against the effort — for a small subscription charge, the honest answer is often that fighting does not pay, and that the real work is preventing the next one.
- A dispute you could have prevented with a clearer statement descriptor cost you the amount, the fee, and a tick on the ratio the networks watch.

## The Only Date That Counts

The deadline is on the dispute object (`evidence_details.due_by`). Not the email, not "usually two weeks" — the field. Submitting one minute late is a forfeit with the evidence sitting in a draft.

- The window is short, often a couple of weeks, and it is set by the network, not by Stripe.
- Evidence can be submitted once. There is no revision after submission, so a partial packet sent early is worse than a complete one sent on the last day.
- Put the due date in your own tracker the moment `charge.dispute.created` arrives — the whole reason `disputes/<year>.md` records `Due by` at filing time and not at close.
- Subscribe to `charge.dispute.created`, `charge.dispute.updated` and `charge.dispute.closed`. A dispute discovered by reading the Dashboard is a dispute discovered late.

## Fight, Refund, or Accept

| Situation | Do |
|---|---|
| You have delivery or usage evidence and the amount is worth the effort | Fight, with the full packet |
| The customer is right — you did fail to deliver, or the cancellation was mishandled | Accept. Losing deliberately costs the same and saves hours |
| An early fraud warning arrived and no dispute has been filed yet | Refund immediately: the refund can prevent the dispute and its fee |
| The dispute is already filed | **Do not refund now.** Refunding a disputed charge can pay twice and does not stop the dispute |
| Duplicate charge that is genuinely yours | Refund the duplicate the moment you find it, before the customer's bank does it for them |
| Rate is approaching a network threshold | Every dispute matters regardless of amount — the ratio is now the asset you are defending |

## Evidence by Reason Code

The reason code tells you what the issuer needs to see. Sending everything you have for every code is the most common way to lose.

| Reason | What the issuer wants |
|---|---|
| `fraudulent` | Proof the cardholder authorized it: AVS and CVC results, 3DS authentication, device and IP matching prior legitimate use, delivery to the billing address, account activity from the same customer before and after |
| `product_not_received` | Proof of delivery: tracking with a delivery confirmation to the billing address, or for digital goods, access logs with timestamps and IPs |
| `product_unacceptable` | The specification, the terms accepted at purchase, photographs, and your handling of the complaint |
| `subscription_canceled` | The cancellation policy shown at signup, the timestamped acceptance, the absence of a cancellation request, and usage after the alleged cancellation |
| `duplicate` | The two charges are different orders: both order records with distinct items or dates, or the refund receipt if one truly was duplicate |
| `unrecognized` | Statement descriptor, the customer's own account details, purchase confirmation email, and usage history that the cardholder will recognize |
| `credit_not_processed` | The refund receipt with its date, or the policy stating why no refund was due |
| `general` | Everything relevant, tightly organized — this code carries no hint |

Usage logs are the underrated evidence for subscriptions: a login two days after the supposed cancellation ends most `subscription_canceled` arguments.

## Building an Evidence Packet

- **One narrative, in order.** Who the customer is, what they bought, when, what proves they received it, and what proves they knew the terms. The reviewer spends minutes, not hours.
- **Documents over prose.** Screenshots of the terms as they appeared at purchase, the confirmation email with headers, the delivery confirmation, the access log. An assertion with no artifact is not evidence.
- **Match the fields.** The API has dedicated evidence fields (customer name, email, purchase IP, receipt, service documentation, delivery tracking, refund policy and its acceptance date). Fill the specific fields rather than dumping everything into the uncategorized text.
- **Redact before uploading.** No full card numbers, no other customers' data, no secrets. This applies doubly to anything you also save locally.
- **Save the packet that wins.** Store it as `artifacts/evidence-packet-<reason>.md` with the fields in order and what each one proves — the next dispute of that type is then a fill-in exercise instead of an afternoon.
- Submitting evidence marks the dispute under review; outcomes commonly take weeks and are decided by the issuer.

## Early Fraud Warnings

- Networks flag transactions the issuer believes are fraudulent *before* a dispute is filed. It is the cheapest signal in this file.
- Refunding on an early fraud warning generally prevents the dispute — you lose the sale, keep the fee, and keep the ratio clean.
- Automate it for low-value transactions: warning arrives, refund issues, access revokes. Human review is for amounts where losing the sale hurts more than a possible dispute.
- An account seeing repeated warnings from one pattern — same BIN range, same country, same product — needs a Radar rule, not more refunds (`advanced.md`).

## The Dispute Rate and Network Programs

- Rate = disputes ÷ transactions in a period, and the card networks run monitoring programs when it stays high — thresholds are in the region of 0.9% for Visa and 1.5% for Mastercard with a floor of around 100 disputes per month. Verify the current numbers with the network; the direction is what matters here.
- Consequences escalate: monitoring, then per-dispute penalties, then remediation plans, and in the worst case losing the ability to accept cards. A processor cannot exempt you from a network program.
- Compute it monthly from `disputes/<year>.md` against `## Volume & Fees`, and treat 0.5% as the internal alarm rather than waiting for the network's number.
- A single bad month matters less than a trend. Two consecutive rising months is the moment to change something, not the moment to write better evidence.

## Prevention, in Order of Return

1. **Statement descriptor the customer recognizes.** A large share of disputes are `unrecognized` — someone who does not know who charged them. Around 22 characters including the prefix, and it should be the brand they bought from, not the legal entity.
2. **Immediate, clear receipt** with the descriptor printed on it, so the customer can match it later.
3. **Cancellation that works in one click**, in the product and in the Billing Portal. Making cancellation hard converts voluntary churn into disputes, which cost more than the churn.
4. **Renewal notice before the charge** on annual plans and after trials. "I forgot I had this" is a dispute waiting for the statement.
5. **3DS on the segments with fraud**, which shifts liability on those transactions (`sca-3ds.md`).
6. **Radar rules for the patterns you actually see**, blocking a narrow shape rather than a whole country.
7. **Fast, generous refunds** where the amount is small. A refund costs the sale; a dispute costs the sale, the fee, and the ratio.
8. **Support reachable before the bank is.** A visible contact route is measurably cheaper than the alternative.

## Inquiries and Retrieval Requests

Some networks send an inquiry or retrieval request first: the issuer asks for information without pulling funds. Treat it as a full dispute with a shorter fuse — a good answer here ends the matter without a dispute, a fee, or a mark on the ratio. Ignoring it converts it into a chargeback automatically.

---

**Two writes per dispute** to `~/Clawic/data/stripe-api-integration/disputes/<year>.md`: one when `charge.dispute.created` arrives (date, amount with currency, reason, `Due by`), one when it closes (evidence sent, outcome). The monthly rate is computed from that file, so a dispute nobody recorded is a rate nobody can defend. When a packet wins, save it as `artifacts/evidence-packet-<reason>.md` and add its `## Boxes` line in the same turn.
