# Scenario Library

The most common ecommerce CS scenarios, grouped by category. For each: the **trigger**, the customer's **underlying emotion**, the **key info to include**, and a **script seed** (a one-line starting point — expand into A/B variants in your library). Adapt names, windows, and amounts to your brand.

## Order Status

**1. WISMO — "Where is my order?"**
Trigger: order shipped, no recent tracking movement, or buyer impatient. Emotion: anxious / impatient. Include: order ID, live `{{tracking_link}}`, current status, realistic `{{eta_date}}`, what to do if it misses ETA. Seed: "Your order `{{order_id}}` is on its way — here's live tracking and it's due by `{{eta_date}}`."

**2. Order not yet shipped (still processing)**
Trigger: buyer asks why no tracking yet within handling window. Emotion: worried it's stuck. Include: handling-time window, ship-by date, reassurance it's normal. Seed: "Good news — `{{order_id}}` is being packed now and ships by `{{ship_by_date}}`; tracking lands the same day."

**3. Tracking shows delivered but customer didn't receive it**
Trigger: carrier marked delivered, buyer has nothing. Emotion: alarmed / suspicious. Include: ask to check with neighbours/household and safe spots, 24-48h carrier-scan note, next step if still missing (claim/reship). Seed: "Let's track this down — carriers sometimes mark early; can you check `{{safe_spots}}`? If it's still missing by `{{check_date}}` I'll open a claim and sort a replacement."

## Shipping / Delivery

**4. Delivery delayed past estimate**
Trigger: ETA passed, parcel in transit. Emotion: frustrated. Include: honest acknowledgement, updated ETA, no false promises, goodwill option if eligible. Seed: "You're right, `{{order_id}}` is running behind — it's now expected `{{new_eta}}`. I'm watching it daily and will flag the carrier if it stalls."

**5. Address change / wrong address after ordering**
Trigger: buyer wants to correct address. Emotion: anxious it's too late. Include: whether it has shipped, what's possible (edit vs. intercept vs. reship), deadline. Seed: "I can update the address on `{{order_id}}` if it hasn't shipped — what's the correct one? If it's already out, here's our reroute option."

**6. Customs / duties or international delay**
Trigger: cross-border parcel held or duty charged. Emotion: confused / annoyed by surprise fee. Include: who pays duties, where it is, expected clearance time. Seed: "`{{order_id}}` is clearing customs in `{{destination}}`; this can add `{{customs_window}}`. Duties are set by local customs and aren't something we control, but here's exactly what to expect."

## Returns / Refunds

**7. How do I return this?**
Trigger: buyer wants to return an eligible item. Emotion: neutral, wants it easy. Include: eligibility window, condition rules, label/process, refund timing. Seed: "Happy to help — here's your return for `{{order_id}}`: label at `{{return_label_link}}`, refund of `{{amount}}` once it scans, within `{{refund_window}}`."

**8. Refund status — "Where's my refund?"**
Trigger: refund issued, not yet visible. Emotion: distrustful. Include: date issued, amount, bank/platform processing window, reference. Seed: "Your `{{amount}}` refund on `{{order_id}}` went out `{{refund_date}}` — banks take `{{refund_window}}` to post it. Reference: `{{ref}}`."

**9. Outside return window**
Trigger: buyer requests return past policy window. Emotion: hopeful / defensive. Include: the policy, any goodwill exception and its limit, alternative (store credit). Seed: "Our window is `{{return_window}}`, so this one's just past — but I'd like to help: I can offer `{{goodwill_option}}` as a one-time exception."

**10. Refund vs. exchange decision**
Trigger: buyer unsure whether to refund or swap. Emotion: indecisive. Include: pros of each, speed, stock. Seed: "Either works for `{{order_id}}` — a refund of `{{amount}}` lands in `{{refund_window}}`, or I can ship a swap today and reserve your size."

## Product Issues / Defects

**11. Item arrived damaged / broken in transit**
Trigger: photos of damage. Emotion: disappointed. Include: own it, free replacement or refund, no return needed for low-value, packing improvement note. Seed: "That's on us — I've arranged a free replacement for `{{order_id}}`, no need to return the damaged one."

**12. Item defective / not working**
Trigger: product fault, not transit damage. Emotion: let down. Include: quick triage questions, warranty coverage, replace/repair/refund path. Seed: "That shouldn't happen — a couple of quick questions to pin it down, then I'll get you a replacement under our `{{warranty_period}}` warranty."

**13. Wrong item / missing item received**
Trigger: order picked or packed incorrectly. Emotion: annoyed at the hassle. Include: apology, immediate correct-item ship, keep/return note for the wrong one. Seed: "Apologies for the mix-up on `{{order_id}}` — the correct `{{product_name}}` ships today; please keep the wrong item, it's on us."

**14. Scent / colour / quality not as expected**
Trigger: product fine but didn't match expectation. Emotion: mild buyer's remorse. Include: empathy without admitting defect, return/credit option, guidance to a better fit. Seed: "Sorry `{{product_name}}` wasn't quite what you pictured — I can set up a return, or suggest an option closer to what you're after."

## Sizing / Fit

**15. Pre-sale sizing advice**
Trigger: buyer asks which size before ordering. Emotion: cautious, wants to avoid a return. Include: fit (true/runs small/large), their measurements, recommended size, size chart. Seed: "For your stats I'd go `{{recommended_size}}` — it runs `{{fit_note}}`; full chart here: `{{size_chart_link}}`."

**16. Exchange for different size**
Trigger: bought, doesn't fit. Emotion: slightly frustrated but loyal. Include: exchange process, condition (unworn/tags), hold option, timing. Seed: "Happy to swap to `{{new_size}}` — prepaid label here, and I can hold your size so it doesn't sell out."

## Promo / Discount Problems

**17. Discount code won't apply**
Trigger: code rejected at checkout. Emotion: irritated, feels cheated. Include: code conditions (min spend, exclusions, expiry), manual fix offer. Seed: "Let's fix that — `{{promo_code}}` needs `{{min_spend}}` and excludes `{{excluded_items}}`; send a screenshot and I'll apply it manually."

**18. Price dropped right after I bought / price-match**
Trigger: buyer saw a lower price post-purchase. Emotion: regretful / wants fairness. Include: policy on post-purchase adjustments, window, what you can offer. Seed: "I hear you — our price-adjustment window is `{{adjust_window}}`, so I can credit you the `{{difference}}` on `{{order_id}}`."

**19. Promo expired / missed the sale**
Trigger: buyer asks to honour a past promo. Emotion: hopeful. Include: the promo ended, any current alternative, no precedent-setting. Seed: "That sale wrapped `{{end_date}}`, but here's what's live now: `{{current_offer}}`."

## Cancellations

**20. Cancel order before shipping**
Trigger: buyer wants to cancel. Emotion: decisive, sometimes impatient. Include: whether it's shipped, cancel + refund confirmation, or intercept option. Seed: "Done — `{{order_id}}` is cancelled and your `{{amount}}` refund is on its way, posting in `{{refund_window}}`."

**21. Cancel after shipping**
Trigger: cancel request once dispatched. Emotion: anxious it's too late. Include: can't cancel in transit, refuse-delivery or return path, refund timing. Seed: "It's already shipped, so I can't pull it back — but here's the easy route: `{{return_or_refuse_option}}`, fully refunded once it's back."

## Account / Payment

**22. Double charge / unexpected charge**
Trigger: buyer sees two charges or an unfamiliar one. Emotion: alarmed. Include: explain pending-auth vs. capture, verify, refund duplicate if real. Seed: "Let's check this — one of those is likely a pending authorization that drops off in `{{auth_window}}`; if it's a true double charge I'll refund it today."

**23. Payment failed / order didn't go through**
Trigger: checkout error, buyer unsure if charged. Emotion: confused / frustrated. Include: confirm no order created, common causes, retry guidance, hold item if possible. Seed: "No order was created and you weren't charged — let's get you checked out; if your card keeps declining try `{{alt_method}}` and I'll hold your cart."

## Negative Review Recovery

**24. Negative public review / low rating**
Trigger: 1-3 star review or public complaint. Emotion: feels unheard, possibly venting. Include: public empathy + ownership, move to private to resolve, concrete fix, invite to update review only after resolving. Seed: "I'm sorry this fell short, `{{customer_name}}` — that's not our standard. I've sent you a DM/email to make it right on `{{order_id}}`."

## Pre-sale Questions

**25. Product / stock / availability question**
Trigger: buyer asks specs, materials, restock, or compatibility before buying. Emotion: interested, deciding. Include: accurate answer, link to details, restock date or notify option, gentle nudge to buy. Seed: "Great question — `{{product_name}}` is `{{key_spec}}`; it's `{{stock_status}}`, and I can notify you the moment `{{restock_item}}` is back."
