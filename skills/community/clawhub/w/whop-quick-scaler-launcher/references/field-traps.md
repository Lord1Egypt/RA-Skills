# Whop field traps

By Major · Unofficial

Use this reference when preparing a store, diagnosing an unexpected setting or handing work to an authorized operator. It is independent guidance, not an official Whop product. An agent with account access runs these checks before and after every approved change; a chat-only assistant explains them.

Documentation checked: 2026-09-29, Europe/Paris. Field observations describe failures encountered in earlier workflows. They are reasons to verify a setting, not guarantees that every current account or CLI version behaves that way. Each entry separates the observed failure from the public documentation that supports a check.

## Before troubleshooting

Keep the approved offer and current live state intact. Record the intended business, existing product, pricing option, canonical checkout and authorized change in the operator's private record. Do not paste account identifiers, credentials or customer records into a public bot. If ownership is ambiguous, stop before changing anything.

A new offer being prepared for review should remain hidden and closed to enrollment. For an existing live offer, preserve availability unless the owner explicitly approves closing it. Hiding an existing offer while retaining direct purchases is a different request.

## FT01. An operation targets the wrong business

Symptom: A new resource appears in a different business, or a product with a familiar title cannot be found in the intended account.

Cause: The operator relied on the display name or active CLI business. A field workflow observed a creation flag failing to route the object as expected. This is not a claim that current account-scoping flags always fail.

Countermeasure:
1. Inspect the signed-in identity and selected business before any authorized write. List existing products before creating another.
2. Prefer explicit account scope where the current command supports it. Verify the target object's owning account, not just its title.
3. Read the returned object and its owner immediately after the write, including automatically created companion resources.
4. If routing differs, stop dependent work. Report the mismatch; do not automatically delete, recreate or migrate resources.
5. If switching the active business was unavoidable, record its previous value, avoid concurrent operators using that session, then restore and verify it.

Verification: The owner of each target object matches the intended business, and the existing draft was reused where applicable.

Evidence: Field observation; selected-business defaults and explicit account scope are documented in [Whop CLI](https://docs.whop.com/cli/overview.md). The documentation does not establish the observed routing defect for every version.

## FT02. Authentication disappears between sessions

Symptom: Sign-in appears successful, but the next process cannot authenticate.

Cause: A field workflow used a session-bound credential store. Other possibilities include an expired session, a different CLI profile or insufficient permissions; a missing resource alone does not diagnose authentication loss.

Countermeasure:
1. Pause pending operations and preserve completed work. Do not repeatedly recreate resources after a sign-in failure.
2. Check the current CLI authentication status and profile in the same environment that will run the operation.
3. Have the owner complete the official secure sign-in flow. Keep authorization links intact and out of public logs; wait for completion rather than treating an opened browser as success.
4. In the affected field setup, `WHOP_CLI_SECRET_STORE=file` addressed session-store loss. Treat it as a version-dependent operator workaround: verify support locally, protect the credential file from shared access and backups, and do not print its contents. It is not confirmed by the public pages cited here.
5. Start a fresh process and perform a harmless scoped read before resuming the first unfinished step.

Verification: The fresh process reads the intended business under the intended identity. No password, key, authorization code or session cookie was copied into chat.

Evidence: Field observation for credential persistence; [Agent Mode](https://docs.whop.com/cli/agent-mode.md) and [Whop CLI](https://docs.whop.com/cli/overview.md) for supported sign-in guidance. The advisory bot never initiates sign-in.

## FT03. A CLI test changes production

Symptom: A supposedly harmless rehearsal creates a live resource or starts a consequential operation.

Cause: A developer assumes the CLI has a sandbox or dry-run mode. Whop explicitly documents that it does not.

Countermeasure:
1. Draft copy and proposed changes locally. Label local simulations as simulations.
2. Require approval for the exact account operation, even if it is described as a test.
3. If integration testing needs a sandbox, use the separately documented sandbox only after checking support for the exact feature. Do not point an unsupported CLI command at it and assume isolation.
4. Check the current sandbox limitations before planning a checkout or app test. The reviewed documentation says the sandbox is not yet available for Whop Elements and excludes apps, messaging and payouts; it limits supported payment methods as well.
5. Keep live payment, signup, invitation, waitlist approval and publication tests behind separate approval gates.

Verification: The test record names the actual environment and the operations allowed there. A local preview is never reported as a tested payment flow.

Evidence: [Agent Mode](https://docs.whop.com/cli/agent-mode.md) and [Test in the Sandbox](https://docs.whop.com/developer/guides/sandbox.md), checked on the date above. Whop having an API sandbox does not give the CLI a test mode.

## FT04. A requested public address never changes

Symptom: The command returns successfully, but the product or business address still uses its previous route.

Cause: A field workflow observed an ignored route option. A label, title, requested slug and actual public URL are separate values.

Countermeasure:
1. Read the exact resource and its returned public address before and after an authorized change.
2. Inspect the current command schema. Do not keep retrying an unsupported field or construct a URL from the title.
3. If the CLI does not expose a working route setting, use the appropriate dashboard control after confirming the owner wants the address changed. If it is absent, ask Whop support rather than inventing a menu path.
4. Check the actual destination and any old links the owner needs to preserve. Treat a custom domain as a separate configuration task.

Verification: The returned address opens the intended seller and offer. Any redirect from an old shared address was tested separately.

Evidence: Field observation, not a verified universal CLI defect. [Whop CLI](https://docs.whop.com/cli/overview.md) describes command help and schemas; it does not guarantee a particular route-editing flag.

## FT05. Headline validation or an idempotency replay blocks a correction

Symptom: A headline is rejected, or a corrected request keeps returning the earlier error.

Cause: The headline exceeds its field limit, or a previously used idempotency key is reused for a different request.

Countermeasure:
1. Validate against the current resource schema before writing. The reviewed Product API limits the headline to 80 characters. Source: [Update Product](https://docs.whop.com/api-reference/beta/products/update-product.md), checked 2026-09-29.
2. Preserve the approved meaning when shortening copy. Keep unresolved claims out of the headline.
3. If the response was lost or timed out, inspect current state before retrying. Reuse the same idempotency key only for the exact same operation within the documented retention period.
4. A changed payload is a new operation and needs a new key. A cached validation failure will not be repaired by resending that key.
5. An uncertain outcome is a reason to reconcile state, not to issue a fresh key and risk a duplicate.

Verification: The saved headline matches the approved text, and reconciliation finds only the intended resource.

Evidence: [Update Product](https://docs.whop.com/api-reference/beta/products/update-product.md) and [Idempotent Requests](https://docs.whop.com/developer/api/idempotency.md). Do not assume every HTTP method supports the same idempotency behavior.

## FT06. The image upload succeeds but the product still shows the old image

Symptom: A file record exists or an update reports success, yet the gallery is unchanged or blank.

Cause: Creating the file record did not transfer its bytes, processing is incomplete, the wrong attachment field was used, or the updated file was never attached to the product. A field workflow observed an older image flag behaving as a no-op.

Countermeasure:
1. For an authorized public marketing image, create the file record with public visibility. Never use this route for a paid download or private document.
2. Send the actual bytes to the returned upload destination with the exact returned headers. Preserve the file reference for a safe resume.
3. Read the processing state until it is ready; stop on failure. Do not confuse a created record with completed storage.
4. Snapshot the ordered gallery. Attach the returned file reference through the current gallery field, preserving every image outside the approved replacement. The reviewed API describes the gallery update as replacement of the collection.
5. Make an image-only change. Do not alter pricing, access or listing state while fixing a cover.

Verification: Read the product again, inspect its exact attached asset, download it and check decoded dimensions and pixels. Inspect the buyer page as a separate check; a different compressed file hash alone does not prove different imagery.

Evidence: [Upload Files](https://docs.whop.com/developer/guides/upload-files.md) and [Update Product](https://docs.whop.com/api-reference/beta/products/update-product.md). Public file URLs can remain accessible; hiding a product is not a way to revoke a leaked file.

## FT07. A post-purchase offer creates a redirect loop

Symptom: After accepting or skipping an additional offer, the buyer returns to the same offer instead of reaching delivery.

Cause: A broad product redirect is reused across purchase steps, or a generic payment link replaces the checkout configuration that owns the intended redirect.

Countermeasure:
1. Draw the actual path before changing it: primary checkout, optional offer page, optional additional checkout, final delivery page.
2. Give each purchase step its own approved checkout configuration and destination. Keep the additional purchase optional and preserve access to the original purchase when it is skipped.
3. Bind each button to the returned canonical checkout URL, retaining required routing parameters. Do not substitute the pricing option's generic URL.
4. Read back each checkout's product association, price, currency and redirect. Check the path for self-links and cycles.
5. Inspect both accept and skip destinations without buying. A real post-payment test requires separate authorization.

Verification: The configuration forms a finite path to delivery. Report redirect configuration and executed post-payment behavior separately.

Evidence: Field observation for the loop; per-checkout redirect configuration is documented in [Create a Checkout Configuration](https://docs.whop.com/api-reference/beta/checkout-configurations/create-a-checkout-configuration.md) and [Create a Checkout Link](https://docs.whop.com/manage-your-business/payment-processing/create-checkout-link.md).

## FT08. An old tutorial promises an order-bump checkbox

Symptom: The operator searches for a native checkbox that is absent from the current checkout settings.

Cause: A field workflow could no longer find the native control described by an earlier tutorial. The reviewed public pages do not establish that it has been removed from every account forever.

Countermeasure:
1. Check the current checkout controls and official documentation for the intended account. Do not spend the session following an obsolete tutorial.
2. Until a supported native control is verified, propose an optional post-purchase offer using the bounded path in FT07.
3. Explain that a separate offer is an additional purchase step, not the same checkout experience as a checkbox.
4. If a third-party app is being considered, review its permissions, costs, data access and purchase behavior first. Do not install it or hand it production credentials just to test the idea.

Verification: The recommendation names the observed capability and the remaining uncertainty. No native order bump is advertised without evidence.

Evidence: Field observation. [Create a Checkout Link](https://docs.whop.com/manage-your-business/payment-processing/create-checkout-link.md) supports checkout configuration choices, but absence of a checkbox from that page is not proof of permanent platform-wide removal.

## FT09. A crossed-out price is saved but not displayed

Symptom: The stored pricing data suggests a discount, but the buyer page does not display it, or a cleared value reappears.

Cause: Display controls and charge amounts are different settings. A field workflow required a dashboard discount-display control, while a CLI value did not affect the page and could not be cleared as expected.

Countermeasure:
1. Preserve the approved amount and currency. Inspect the charge separately from the visual comparison price.
2. Look for the current discount-display control in the dashboard's growth settings. The historical menu location is a lead, not a guaranteed current label.
3. Check the current schema before clearing a value; do not invent a null-reset behavior. If the control cannot be found or reset, report it as unresolved.
4. Use a crossed-out price only when the comparison basis is genuine and approved. Do not manufacture a former price to make the offer appear discounted.
5. Reopen the product page and checkout in a fresh session after an authorized change.

Verification: The buyer sees the intended comparison and the correct payable amount. A promotional display must not silently change billing terms.

Evidence: Field observation for the display control and clearing behavior. [Manage Products](https://docs.whop.com/manage-your-business/products/manage-products.md) documents pricing edits, not a universal CLI discount-display guarantee.

## FT10. The PDF exists, but the buyer cannot get the right file

Symptom: The seller can open a PDF, but a buyer sees no download, an outdated edition or an unrelated product's content.

Cause: Storage, app installation, product access and the file inside the app were treated as one step. An administrator's access masked a missing buyer entitlement.

Countermeasure:
1. Identify the approved file, edition and language before upload. Keep paid content out of public product galleries.
2. Use an appropriate product-restricted delivery app. The field workflow used Content; current documentation also lists Files for ebooks and digital assets.
3. Confirm that the delivery app is included in the intended product and excluded from unrelated free products. Inspect its internal content permissions too.
4. Use the dashboard's product preview for a first check. Then, under a separately approved test, sign in as a buyer distinct from the seller administrator.
5. Download and open the file from that buyer's access area. Check title, language, contents and version against the approved original. Test denial for a buyer without that product.

Verification: The entitled buyer receives the correct file, while an unrelated buyer cannot access it. An upload receipt, installed app or administrator preview alone is insufficient.

Evidence: [Consumer Apps](https://docs.whop.com/whop-apps/consumer-apps.md), [Manage Products](https://docs.whop.com/manage-your-business/products/manage-products.md) and [Upload Files](https://docs.whop.com/developer/guides/upload-files.md). The bot can prepare this checklist; it cannot verify private buyer access itself.

## FT11. A stale editor overwrites a newer change

Symptom: A corrected price, description or image unexpectedly reverts after someone saves an old browser tab.

Cause: The editor retained an earlier form state while another operator or API changed the same resource.

Countermeasure:
1. Agree which operator or interface owns the edit. Close stale forms without saving before changing the resource through another interface.
2. Take a fresh before-state immediately before an authorized update.
3. Send only supported, intended changes. Inspect replacement-style arrays and objects and preserve approved values where the API requires a full replacement.
4. If another edit occurred, stop and reconcile the latest state instead of blindly applying the old snapshot.
5. Reopen the editor from the newly saved resource, then compare protected commercial and access fields.

Verification: The intended change remains saved and unrelated fields match the latest approved state.

Evidence: Field observation for stale forms; [Update Product](https://docs.whop.com/api-reference/beta/products/update-product.md) explicitly describes gallery replacement. Do not infer that every update field has identical merge behavior.

## FT12. Unreviewed defaults change economics or collect unnecessary data

Symptom: Affiliate commissions, phone collection or a member-count display appear although the owner did not choose them.

Cause: Defaults or inherited settings were accepted without inspection. A field observation does not establish a universal default rate or configuration.

Countermeasure:
1. Review product affiliate settings and any overrides, including their scope and when a commission applies. Have the owner approve the actual economics.
2. Inspect the checkout's requested fields. Remove unnecessary seller-configurable collection only after approval; do not promise that required payment-method fields can be disabled.
3. Review member-count visibility and the basis of any social proof. Never populate an invented count.
4. Verify amount, currency, billing interval, initial charge, access duration, renewal behavior and localization independently. If an exact charge currency is promised, inspect adaptive pricing rather than changing the offer to match a surprising symbol.
5. Treat a waitlist as a distinct flow. The dashboard guide describes payment details and a possible charge on approval. Do not call it a card-free interest form without checking the actual journey, including approval behavior.

Verification: The settings match explicit owner decisions, the checkout collects only the intended information plus unavoidable payment requirements, and no supposed free-interest flow can silently authorize a later payment.

Evidence: [Affiliates](https://docs.whop.com/developer/guides/affiliates.md), [Create a Checkout Link](https://docs.whop.com/manage-your-business/payment-processing/create-checkout-link.md), [Create a Waitlist](https://docs.whop.com/manage-your-business/products/create-waitlist.md) and [Adaptive Pricing](https://docs.whop.com/payments-and-billing/fees/adaptive-pricing.md). No historical affiliate percentage is presented as a current default.

## FT13. A successful page response is mistaken for publication

Symptom: A link responds successfully, but it shows a generic page, the wrong offer, a closed checkout or no discoverable listing.

Cause: HTTP success, rendered content, sales availability, search discovery and Marketplace review were collapsed into one status.

Countermeasure:
1. Open the exact returned URL in a fresh anonymous desktop session and a narrow mobile view. Check seller, title, included access, amount, currency and billing wording.
2. Read product visibility, pricing-option visibility, effective purchase availability and Marketplace status separately.
3. Check the actual card or listing where discovery is claimed. A sitemap can corroborate a site's public route; it does not prove checkout readiness, Marketplace approval or search-engine indexing.
4. For a closed preparation, inspect the direct checkout and confirm that enrollment is unavailable. Hidden listing status alone is insufficient.
5. For an authorized open checkout, wait for the actual secure payment controls to finish loading. A blank loading frame is not evidence of a broken payment flow or a successful one.
6. Keep payment and delivery marked untested until their authorized end-to-end checks have really occurred.

Verification: Each claimed surface shows the intended offer. Use the state receipt below instead of a blanket statement that the product is published.

Evidence: Field observation for misleading success responses. [Create a Checkout Link](https://docs.whop.com/manage-your-business/payment-processing/create-checkout-link.md) explicitly says a link omitted from the store can still work when shared directly.

## FT14. A payment inspection becomes a real purchase

Symptom: An inspection charges a saved payment method, creates a membership or triggers fulfillment.

Cause: The operator presses the final payment control in a production buyer session, assuming another confirmation will appear.

Countermeasure:
1. Inspect public pages in a fresh context without stored payment methods. This reduces accidental-payment risk but does not make submitting a checkout harmless.
2. During passive QA, stop before any action that pays, enrolls, approves a waitlist entry or grants access.
3. Plan a separate payment test with the owner's approval for the exact offer, amount, currency, buyer identity and environment. Identify who will submit the payment and how the resulting membership will be handled.
4. Let the authorized buyer enter payment credentials directly in Whop's secure flow. Never collect them in a bot conversation.
5. Keep the seller administrator and test buyer separate. If a purchase succeeds and sign-in remains unfinished, resume that purchase instead of buying again.
6. Do not automatically refund, cancel or delete the result; those are separate consequential actions that need authorization.

Verification: Passive QA records that no purchase was submitted. An approved payment test has real transaction, access and delivery evidence, with any untested stage left explicit.

Evidence: Field observation; production risk is documented in [Agent Mode](https://docs.whop.com/cli/agent-mode.md). [Test in the Sandbox](https://docs.whop.com/developer/guides/sandbox.md) explains the separate supported testing environment and its limitations.

## Copyable change brief

Keep this record private with the authorized operator. An assistant can help draft it without receiving private identifiers or credentials.

```text
Owner-approved objective:
Intended business confirmed by the operator:
Existing offer to reuse:
Exact change requested:
Fields and live behavior to preserve:
Current visibility and availability:
Target visibility and availability:
Canonical checkout confirmed by the operator:
Buyer-facing amount, currency and billing terms:
Delivery scope and approved file version:
Unresolved commercial or legal decisions:
Approval required before the operation:
Readback and buyer checks to perform:
Recovery if the operation stops midway:
```

For parallel work, assign a single editor per resource and an independent checker. Preserve completed stages when authentication fails. Before copying a draft or template, review inherited links, access, images and conditions; a previous approval does not validate the new offer.

## Copyable verification receipt

```text
Evidence date and method:
Business and offer matched: verified / unverified
Approved content saved: verified / unverified
Product visibility: visible / hidden / unknown
Pricing option visibility: visible / hidden / unknown
Direct checkout availability: open / closed / unknown
Displayed amount, currency and cadence: verified / unverified
Marketplace status: not submitted / pending / public / unknown
Gallery asset: verified / unverified
Redirect configuration: verified / unverified
Real payment submitted: yes / no
Post-payment redirect executed: verified / untested
Buyer access and correct download: verified / untested
Unrelated-buyer access denied: verified / untested
Remaining blocker and next owner action:
```

When an advisory bot has only a user's account of events, label the receipt user-reported. It must not promote that account into independently verified evidence.
