# Shopify Admin Pro workflows

Each playbook: read first, summarize in plain language, label the evidence (API / screen / inferred), write only
with approval for that specific change, then verify. Commands use the `shopify` helper from SKILL.md.

Status: playbook 1 was run on a live store (an 18-product apparel store with 0 orders). The write playbooks
(5-9) and the order-based playbooks (2-4) have not been exercised on a live store yet. The `mutate` guards were
tested against a stubbed network.

## 1. Pre-opening store audit (read, tested live)
Produce one report: Verdict, Fix first (ordered), The Ugly (blocks opening), The Bad, The Good, What was not
covered, How it was checked. Tag every finding [API], [Screen], [Public] or [Inferred]. Never bypass a store password.
1. Basics: shop plan, currency, timezone, domain and SSL, ship-to countries, `scopes`.
2. Catalog: counts by status; variants; duplicate titles and SKUs; zero or missing prices; missing SEO, alt text,
   category, barcode, country of origin, HS code; unit costs and margin on ACTIVE products.
3. Shipping: every delivery profile, its variant count and zones. Flag any ACTIVE product whose profile has no
   Rest-of-World zone, since it cannot ship outside the listed countries. Flag unused profiles.
4. Channels: which products are published on which channel.
5. Online store: live theme and unpublished themes, pages, menus (Shop link? policy links?), URL redirects whose
   target does not exist, policies (placeholders like `[Your Email]`, conflicting wording).
6. Discounts, gift cards, markets: active codes with no end date, test gift cards.
7. Customers: counts and consent states (`--redact-pii`).
8. Public checks: HTTP status, redirects, HTTPS, response time of the storefront or password page.
9. Not coverable by API: payment provider live/test mode, tax, checkout settings, 2FA and users, notification
   sender, order routing. Say these were not verified unless someone read the admin screens.
10. Not coverable at all without the owner: rendered storefront behind a password, test checkout, confirmation
    emails, vendor order flow, pixel firing. List them under "What was not covered".

## 2. Daily ops brief (read, untested with orders)
1. Orders since start of period: `paginate --path orders` with `created_at:>=<date>`; compute count, gross sales,
   AOV, paid vs pending, refunded total (`totalRefundedSet`).
2. Unfulfilled backlog: `fulfillment_status:unfulfilled financial_status:paid`; flag any older than the store's
   shipping promise (ask the user once).
3. Low stock on items that sold: collect line-item product/variant IDs from step 1, query `inventoryLevels`, flag
   `available <= threshold` (default 5, ask).
4. Optional trend via ShopifyQL (`SINCE -7d`, `-30d`) if `read_reports` is granted.
5. Output: 5-8 lines: headline numbers, 3 things needing action, 1 opportunity. No customer names or emails unless asked.

## 3. Low-stock / reorder report (read, untested)
`bulk-query` all variants with `inventoryQuantity` and `inventoryItem.unitCost`, then sort by sales velocity divided
by stock if order history is available, else by quantity ascending. Deliver a table: SKU, title, on hand, committed, location.

## 4. Store health audit (read, partly tested)
`scopes` (are write scopes granted that are not used?), draft and archived product counts, products with no
inventory tracking or zero price, active discounts without an end date. Present findings ranked by risk.

## 5. Refund a customer (money, write, untested)
1. Find the order by `name:#1234` (or email): show items, paid amount, existing refunds, fulfillment state.
2. Ask what to refund (items / shipping / custom amount) and whether to restock and notify.
3. `suggestedRefund`: show amount, currency and gateway.
4. The user says yes to that amount: `mutate ... --confirm --confirm-high-risk refundCreate`.
5. Verify: re-read `totalRefundedSet` and report the new total. If `userErrors` or exit code 3, nothing was refunded: say so.

## 6. Fulfill an order with tracking (write, untested)
1. Read `fulfillmentOrders` for the order; confirm line items and remaining quantities.
2. Get carrier and tracking number from the user (never invent). Ask whether to notify the customer.
3. Preview `fulfillmentCreate`, get approval, then `--confirm`. Verify `fulfillment.status`.

## 7. Bulk catalog update: prices, tags, status (write, untested)
1. `bulk-query` the affected set and save the JSONL.
2. Build the change list as a table: id, field, old to new. Show the count, 10 samples and the min/max of new
   values (this catches 10x errors).
3. Get approval for the whole batch once, then apply in chunks of 50 or fewer (one `mutate` each;
   `productVariantsBulkUpdate` takes many variants per call). Stop on the first non-empty `userErrors` and report.
4. Save the old-to-new table next to the audit log so the change can be reverted.
5. Never use delete as a cleanup shortcut; archive instead.

## 8. Create products from a spreadsheet (write, untested)
Create everything as `DRAFT`. Show the user the first 3 created (handles and admin links). They publish; the skill
changes status to `ACTIVE` only on explicit request per batch.

## 9. Fix audit findings (write, untested)
Take findings from playbook 1 and propose each fix as its own preview: add a Rest-of-World zone, fix a template
placeholder in a policy, delete a dead redirect, add SEO titles and alt text, set an end date on a discount.
Group low-risk edits (SEO, alt text) into one reviewed batch. Treat shipping, policy, theme and discount changes
as individual approvals.

## 10. Abandoned-checkout recovery list (read)
Read `abandonedCheckouts` (last N days), compute value and top items, output a ranked list with `--redact-pii`.
Sending recovery emails is out of scope unless the user supplies the channel and copy and approves the send.
