# Shopify Audit Pro workflows (read-only)

Each playbook: read first, summarize in plain language, label the evidence (API / screen / inferred), and
hand the user the exact change to make in Shopify admin. Commands use the `shopify` helper from SKILL.md.

Status: playbook 1 was run on a live store (an 18-product apparel store with 0 orders). Playbooks 2-4 have not
been exercised on a store with order history yet.

## 1. Pre-opening store audit (tested live)
Produce one report: Verdict, Fix first (ordered), The Ugly (blocks opening), The Bad, The Good, What was not
covered, How it was checked. Tag every finding [API], [Screen], [Public] or [Inferred]. Never bypass a store password.
Use `report-template.md` for the skeleton and the launch-readiness checklist.
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

## 2. Daily ops brief (untested on a live store with orders)
1. Orders since start of period: `paginate --path orders` with `created_at:>=<date>`; compute count, gross sales,
   AOV, paid vs pending, refunded total (`totalRefundedSet`).
2. Unfulfilled backlog: `fulfillment_status:unfulfilled financial_status:paid`; flag any older than the store's
   shipping promise (ask the user once).
3. Low stock on items that sold: collect line-item product/variant IDs from step 1, query `inventoryLevels`, flag
   `available <= threshold` (default 5, ask).
4. Optional trend via ShopifyQL (`SINCE -7d`, `-30d`) if `read_reports` is granted.
5. Output: 5-8 lines: headline numbers, 3 things needing action, 1 opportunity. No customer names or emails unless asked.

## 3. Low-stock / reorder report (untested)
`bulk-query` all variants with `inventoryQuantity` and `inventoryItem.unitCost`, then sort by sales velocity divided
by stock if order history is available, else by quantity ascending. Deliver a table: SKU, title, on hand, committed, location.

## 4. Store health audit (partly tested)
`scopes` (only `read_*` handles?), draft and archived product counts, products with no inventory tracking or zero
price, active discounts without an end date. Present findings ranked by risk.
