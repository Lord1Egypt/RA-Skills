# Support Script Quality Checklist

Run every script (and the library as a whole) through this before approval and rollout. Aim for all boxes checked; any unchecked box is a fix-before-ship item.

## Coverage
- [ ] Top 15-25 inquiry types from the ticket audit each have a script.
- [ ] The highest-volume scenarios (WISMO, returns, damaged item) are covered first.
- [ ] Each scenario has both a standard (A) and high-empathy (B) variant.
- [ ] Each scenario has a short chat variant and a fuller email variant.
- [ ] Edge cases that recur (delivered-but-missing, double charge) are included.
- [ ] No duplicate scripts covering the same trigger differently.

## Brand Voice
- [ ] Tone matches the library's voice summary (register, warmth, formality).
- [ ] Emoji usage follows the rule (none on complaints/refunds; within the per-message cap).
- [ ] No corporate-legalese and no off-brand slang.
- [ ] Reads like a person wrote it, not a form letter.
- [ ] Contraction and sign-off style are consistent across scripts.

## Accuracy & Policy
- [ ] No promise exceeds the agent's actual authority (refunds, reships, dates).
- [ ] Timeframes are realistic and match carrier/processor windows.
- [ ] Platform-specific guardrails are correct (Shopify vs. Shopee vs. TikTok Shop).
- [ ] No steering customers to pay or talk off-platform on marketplaces.
- [ ] Return window, conditions, and who-pays-shipping are stated correctly.
- [ ] Sensitive claims (injury/safety/allergy) avoid admitting fault and escalate.
- [ ] Compensation offers stay within the pre-approved, capped ladder.

## Personalization
- [ ] Every script uses `{{customer_name}}`.
- [ ] Every script references at least one order-specific detail (order ID, item, ETA).
- [ ] All placeholders use consistent `{{snake_case}}` tokens.
- [ ] Every placeholder appears in the variable glossary.
- [ ] Must-verify fields (ETA, tracking, amount) are flagged before sending.
- [ ] No literal `{{ }}` token can be sent by accident (final swap step exists).

## Empathy
- [ ] Complaints open by acknowledging the specific problem and feeling.
- [ ] Ownership is taken where the issue is the brand's fault.
- [ ] No non-apologies ("sorry you feel that way", "sorry for any inconvenience").
- [ ] The customer is never blamed or made to feel at fault.
- [ ] Tone energy is dialled down on money/safety/complaint scenarios.

## Escalation
- [ ] Each script states when to escalate and to whom.
- [ ] Hard triggers are defined (safety/injury, chargeback, legal/press, value over threshold, 3rd contact).
- [ ] Escalation handoff includes what info to pass along.
- [ ] Agents have a clear default for "I'm not sure" (escalate, don't improvise).

## Clarity & Next Step
- [ ] Each reply states exactly what happens next and by when.
- [ ] Each reply invites a response or confirms the conversation is resolved.
- [ ] No script forces an unnecessary follow-up message.
- [ ] Chat variants lead with the answer, not preamble.

## Localization
- [ ] Localized versions read naturally, not word-for-word translated.
- [ ] A native speaker reviewed each non-English set.
- [ ] Politeness/formality matches market norms (e.g. Shopee SEA courtesy).
- [ ] Date, currency, name order, and honorifics are correct per locale.
- [ ] Placeholders survive translation intact.

## Maintenance
- [ ] Library has an owner and a version/date.
- [ ] Maintenance log is in place and started.
- [ ] A monthly review is scheduled.
- [ ] A trigger exists to audit scripts on any product/price/policy change.
- [ ] Unused or outdated scripts are flagged for retirement.
