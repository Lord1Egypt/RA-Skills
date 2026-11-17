# Shopify GraphQL cookbook (read-only)

Shapes below are from the Admin GraphQL API; fields drift between versions. If a call errors on an unknown
field or argument, introspect that type for the resolved version (SKILL.md rule 2) instead of retrying blindly.
Use `gid://shopify/<Type>/<id>` IDs everywhere. Everything here is a read. `paginate` needs `$cursor` and
`pageInfo { hasNextPage endCursor }`.

Every query in this file was run against a live store (an 18-product store with 0 orders) with the scopes in
`safety-and-scopes.md` and returned without errors. Order, fulfillment-order and abandoned-checkout queries
were not exercised against real rows (the store has no orders).

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
query { menus(first: 10) { nodes { handle title items { title url } } } }
query { urlRedirects(first: 100) { nodes { path target } } }
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
