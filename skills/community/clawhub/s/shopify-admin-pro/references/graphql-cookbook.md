# Shopify GraphQL cookbook (reads and guarded writes)

Shapes below are from the Admin GraphQL API; fields and inputs drift between versions. If a call errors on an
unknown field or argument, introspect that type for the resolved version (SKILL.md rule 8) instead of retrying
blindly. Use `gid://shopify/<Type>/<id>` IDs everywhere. `paginate` needs `$cursor` and
`pageInfo { hasNextPage endCursor }`.

Status:
- Part 1 (reads) was run against a live store (an 18-product store with 0 orders) with the scopes in
  `safety-and-scopes.md` and returned without errors. Order, fulfillment-order and abandoned-checkout queries were
  not exercised against real rows.
- Part 2 (writes) has NOT been executed against a live store. Its shapes were checked against the live schema of
  API 2026-10 by introspection: every mutation name, argument, input field and payload field used below exists
  (this caught two stale shapes, now fixed). That proves the shapes are valid, not that a write behaves as
  expected. The `mutate` guards were tested against a stubbed network only. Introspect the input type for your
  API version, preview, get approval, then confirm.

# Part 1: Reads

## Products
```graphql
# paginate --path products
query($cursor: String) {
  products(first: 100, after: $cursor, query: "status:active") {
    pageInfo { hasNextPage endCursor }
    nodes { id title handle status vendor totalInventory
            seo { title description }
            category { name }
            variants(first: 20) { nodes { id sku price barcode inventoryItem { id unitCost { amount } } } } }
  }
}
```
Catalog-hygiene checks to run on the result: missing SEO title/description, empty image alt text, missing category,
missing barcode, zero price, duplicate SKUs, drafts with duplicate titles.

## Orders
```graphql
query($cursor: String) {
  orders(first: 100, after: $cursor,
         query: "created_at:>=2026-10-01 financial_status:paid fulfillment_status:unfulfilled") {
    pageInfo { hasNextPage endCursor }
    nodes { id name createdAt displayFinancialStatus displayFulfillmentStatus
            totalPriceSet { shopMoney { amount currencyCode } }
            totalRefundedSet { shopMoney { amount currencyCode } } }
  }
}
```
Filter syntax is Shopify search syntax. Add `customer { id email }` only when needed, with `--redact-pii`.

## Customers (PII, use --redact-pii)
```graphql
query { customers(first: 20) { nodes { id numberOfOrders amountSpent { amount currencyCode }
  defaultEmailAddress { marketingState } } } }
```

## Inventory and locations
```graphql
query { locations(first: 10) { nodes { id name isActive isFulfillmentService } } }
query($id: ID!) { inventoryItem(id: $id) { id sku inventoryLevels(first: 10) {
  nodes { location { name } quantities(names: ["available","on_hand","committed"]) { name quantity } } } } }
```

## Fulfillment
```graphql
query($id: ID!) { order(id: $id) { fulfillmentOrders(first: 10) { nodes { id status
  lineItems(first: 20) { nodes { id remainingQuantity lineItem { title } } } } } } }
```

## Shipping (delivery profiles and zones)
```graphql
query { deliveryProfiles(first: 20) { nodes { id name
  profileItems(first: 1) { pageInfo { hasNextPage } }
  profileLocationGroups { locationGroupZones(first: 25) { nodes {
    zone { name countries { code { countryCode restOfWorld } } }
    methodDefinitions(first: 10) { nodes { name active
      rateProvider { ... on DeliveryRateDefinition { price { amount currencyCode } } } } } } } } } } }
```
This query is large on stores with many profiles; trim it. A profile with no zone that has `restOfWorld: true`
cannot ship to countries outside its listed zones.

## Publication (which channels show a product)
```graphql
query { publications(first: 10) { nodes { id name } } }
query($pid: ID!) { products(first: 50) { nodes { id title publishedOnPublication(publicationId: $pid) } } }
```
`publishedOnCurrentPublication` fails for apps without a publication; use `publishedOnPublication` with ids from `publications`.

## Discounts, gift cards, markets
```graphql
query { discountNodes(first: 50) { nodes { id discount { __typename
  ... on DiscountCodeBasic { title status endsAt }
  ... on DiscountAutomaticBasic { title status endsAt } } } } }
query { giftCards(first: 25) { nodes { id enabled expiresOn initialValue { amount currencyCode } } } }
query { markets(first: 20) { nodes { id name enabled } } }
```
Flag active discounts with no `endsAt`.

## Online store: themes, pages, menus, redirects, policies
```graphql
query { themes(first: 20) { nodes { id name role } } }
query { pages(first: 20) { nodes { id title handle } } }
query { menus(first: 10) { nodes { id handle title items { title url } } } }
query { urlRedirects(first: 100) { nodes { id path target } } }
query { shop { shopPolicies { type title body updatedAt } } }
```
Compare redirect targets with existing collections and pages to find dead redirects. Search policy `body` for
template placeholders such as `[Your Email]`.

## Analytics (ShopifyQL, needs `read_reports`)
```graphql
query { shopifyqlQuery(query: "FROM sales SHOW total_sales GROUP BY day SINCE -7d ORDER BY day") {
  tableData { columns { name dataType } rows } parseErrors } }
```
Return shape has changed across versions; introspect if it errors.

## Abandoned checkouts
`abandonedCheckouts(first: 50, query: "created_at:>=...")` is a recovery list (PII). Report counts and value; do not contact customers.

## Bulk reads (whole catalog / all orders)
Put the query in a `.graphql` file (connections written without `first`; nest at most two levels):
```graphql
{ products { edges { node { id title status variants { edges { node { id sku price } } } } } } }
```
`shopify bulk-query --file q.graphql --out ~/.openclaw/workspace/tmp/products.jsonl` gives JSONL, one object per
line, children carry `__parentId`. The output path must be new. Download URLs expire; the file is saved mode 600
and should be deleted when done if it holds PII.

# Part 2: Writes (all untested live; each goes through `mutate`)

Every write: read the target first, run `mutate` without `--confirm` to preview, state the effect in plain words,
get a yes for that specific change, then re-run with `--confirm` (plus `--confirm-high-risk <names>` where the
preview demands it). Then re-read the object and report what is now true. Exit code 3 means `userErrors`: nothing
was applied. Every mutation should select `userErrors { field message }`.

Each example is one operation, saved in a `.graphql` file or passed with `--query`, with variables via `--vars` or
`--vars-file`. Needed scopes are in brackets.

## Products and variants [write_products]
Create as DRAFT first:
```graphql
mutation($product: ProductCreateInput!) {
  productCreate(product: $product) { product { id title handle status } userErrors { field message } }
}
```
`{"product": {"title": "Example tee", "status": "DRAFT", "vendor": "Example", "tags": ["new"]}}`

Update title, SEO, status or tags (the id goes inside the input):
```graphql
mutation($product: ProductUpdateInput!) {
  productUpdate(product: $product) { product { id title status seo { title description } tags } userErrors { field message } }
}
```
`{"product": {"id": "gid://shopify/Product/1", "seo": {"title": "...", "description": "..."}}}`

Add tags without replacing existing ones:
```graphql
mutation($id: ID!, $tags: [String!]!) { tagsAdd(id: $id, tags: $tags) { node { id } userErrors { field message } } }
```

Change variant prices or barcodes in bulk (many variants per call, one product per call):
```graphql
mutation($productId: ID!, $variants: [ProductVariantsBulkInput!]!) {
  productVariantsBulkUpdate(productId: $productId, variants: $variants) {
    productVariants { id sku price } userErrors { field message } }
}
```
Archive instead of delete: `productUpdate` with `"status": "ARCHIVED"`. `productDelete` is high-risk and rarely reversible.

## Collections [write_products]
`collectionAddProducts` does not exist in API 2026-10. Add or remove a product's collections through the product
(manual collections only):
```graphql
mutation($product: ProductUpdateInput!) {
  productUpdate(product: $product) { product { id collections(first: 10) { nodes { id title } } } userErrors { field message } }
}
```
`{"product": {"id": "gid://shopify/Product/1", "collectionsToJoin": ["gid://shopify/Collection/1"]}}`
Use `collectionsToLeave` to remove. `collectionCreate`, `collectionUpdate` and `collectionReorderProducts` also exist.

## Inventory [write_inventory]
Relative change, with the read of `available` before and after:
```graphql
mutation($input: InventoryAdjustQuantitiesInput!) {
  inventoryAdjustQuantities(input: $input) { inventoryAdjustmentGroup { reason changes { name delta } } userErrors { field message } }
}
```
`{"input": {"name": "available", "reason": "correction", "changes": [{"inventoryItemId": "gid://shopify/InventoryItem/1", "locationId": "gid://shopify/Location/1", "delta": 5}]}}`
Check the allowed `reason` values for the API version by introspection.

## Order notes and tags [write_orders]
```graphql
mutation($input: OrderInput!) { orderUpdate(input: $input) { order { id note tags } userErrors { field message } } }
```
`{"input": {"id": "gid://shopify/Order/1", "note": "Packed by hand", "tags": ["priority"]}}`
`tags` replaces the list; read the current tags and send the full new list, or use `tagsAdd`.

## Fulfill with tracking [write_orders, plus the matching write_*_fulfillment_orders scope]
Read `fulfillmentOrders` first (Part 1). Carrier and number come from the user, never invented. Ask whether the
customer is notified.
```graphql
mutation($fulfillment: FulfillmentInput!) {
  fulfillmentCreate(fulfillment: $fulfillment) { fulfillment { id status trackingInfo { number company url } } userErrors { field message } }
}
```
`{"fulfillment": {"notifyCustomer": false, "trackingInfo": {"number": "...", "company": "..."}, "lineItemsByFulfillmentOrder": [{"fulfillmentOrderId": "gid://shopify/FulfillmentOrder/1"}]}}`

## Refunds [write_orders] (money, high-risk)
Calculate first, then quote the amount and currency back to the user:
```graphql
query($id: ID!) { order(id: $id) { id name
  suggestedRefund(suggestFullRefund: true) { amountSet { shopMoney { amount currencyCode } } } } }
```
`suggestedRefund` also takes `refundLineItems` (`{lineItemId, quantity}` objects), `shippingAmount`, `refundShipping`,
`refundDuties` and `refundMethodAllocation`. Introspect `SuggestedRefund` for its return fields. Then:
```graphql
mutation($input: RefundInput!) { refundCreate(input: $input) { refund { id totalRefundedSet { shopMoney { amount currencyCode } } } userErrors { field message } } }
```
Run with `--confirm --confirm-high-risk refundCreate` only after the user confirms that exact amount. Verify by
re-reading `totalRefundedSet`.

## Cancel an order [write_orders] (high-risk)
```graphql
mutation($orderId: ID!, $reason: OrderCancelReason!, $restock: Boolean!, $refundMethod: OrderCancelRefundMethodInput, $notifyCustomer: Boolean, $staffNote: String) {
  orderCancel(orderId: $orderId, reason: $reason, restock: $restock, refundMethod: $refundMethod, notifyCustomer: $notifyCustomer, staffNote: $staffNote) {
    job { id done } orderCancelUserErrors { field message } }
}
```
`reason` is one of CUSTOMER, DECLINED, FRAUD, INVENTORY, STAFF, OTHER. `refundMethod` is
`{"originalPaymentMethodsRefund": true}` or `{"storeCreditRefund": {...}}`; omit it for no refund. It returns a
background job, and its errors come back as `orderCancelUserErrors`, not `userErrors`. The helper's exit-3 check
matches any key ending in `UserErrors`, so these are caught too. The cancel itself runs in the background: re-read the
order afterward to confirm it is cancelled.

## Discounts [write_discounts]
Always with an end date:
```graphql
mutation($basicCodeDiscount: DiscountCodeBasicInput!) {
  discountCodeBasicCreate(basicCodeDiscount: $basicCodeDiscount) { codeDiscountNode { id } userErrors { field message } }
}
```
Fill `title`, `code`, `startsAt`, `endsAt`, `customerGets`, `context` and any `minimumRequirement` from the introspected input type.
To end an existing code, set `endsAt` with the matching update mutation; deactivate and delete are high-risk.

## Customers [write_customers] (PII)
```graphql
mutation($input: CustomerInput!) { customerUpdate(input: $input) { customer { id tags } userErrors { field message } } }
```
Change only what the user named. Never mass-edit marketing consent.

## Redirects, menus, pages [write_online_store_navigation, write_content, write_online_store_pages]
```graphql
mutation($urlRedirect: UrlRedirectInput!) { urlRedirectCreate(urlRedirect: $urlRedirect) { urlRedirect { id path target } userErrors { field message } } }
mutation($id: ID!) { urlRedirectDelete(id: $id) { deletedUrlRedirectId userErrors { field message } } }
mutation($page: PageCreateInput!) { pageCreate(page: $page) { page { id title handle } userErrors { field message } } }
mutation($id: ID!, $title: String!, $items: [MenuItemUpdateInput!]!) { menuUpdate(id: $id, title: $title, items: $items) { menu { id } userErrors { field message } } }
```
`menuUpdate` replaces the whole item list: read the menu first and send every item. `urlRedirectDelete` is high-risk.

## Policies and themes [write_legal_policies / write_themes] (high-risk)
```graphql
mutation($shopPolicy: ShopPolicyInput!) { shopPolicyUpdate(shopPolicy: $shopPolicy) { shopPolicy { id type updatedAt } userErrors { field message } } }
mutation($id: ID!) { themePublish(id: $id) { theme { id role } userErrors { field message } } }
```
Both need `--confirm-high-risk` with the exact mutation name. Policy text is legal content: show the full before and
after text and have the owner approve the wording. Publishing a theme changes what customers see immediately.
Scope handles in brackets were checked against Shopify's access-scope documentation; `menuUpdate`'s scope was not
listed there explicitly (navigation scope is documented for redirects). Confirm what the app actually holds with
`shopify scopes`.
