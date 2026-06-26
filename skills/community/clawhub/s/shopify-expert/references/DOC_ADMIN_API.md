# Shopify docs: Admin Api

> Generated from Shopify official LLM documentation snapshot (maintainer export). Prefer live docs at [shopify.dev](https://shopify.dev/) for API versions and current behaviour.

---
## Admin API

### Admin API

The [GraphQL Admin API](https://shopify.dev/docs/api/admin-graphql) lets you build apps and integrations that extend and enhance the Shopify admin. You can query and manage resources like products, customers, orders, inventory, fulfillment, and more. Because it’s GraphQL, it provides a more flexible, efficient, and controlled way to query and manipulate data than traditional REST APIs. For more on how to work with GraphQL, see [About GraphQL](https://shopify.dev/docs/apps/build/graphql).

The Admin GraphQL endpoint URL depends on your shop name and the API version:

```
https://{shop-name}.myshopify.com/admin/api/2025-01/graphql.json
```

#### Authentication

Authentication requires both access tokens and specific access scopes depending what resource you need to access.

- All GraphQL Admin API queries require a valid Shopify access token.
- Public and custom apps created in the Partner Dashboard generate tokens using OAuth, and custom apps made in the Shopify admin are authenticated in the Shopify admin.
- Include your token as a `X-Shopify-Access-Token` header on all API queries.
- Your app will need the correct [access scopes](https://shopify.dev/api/usage/access-scopes).

#### Example queries

Get shop information:

```
query { shop { id name email domain createdAt updatedAt } }
```

Get products:

```
query { products(first: 10) { edges { node { id title description variants(first: 5) { edges { node { id price sku } } } } } } }
```

Get orders:

```
query { orders(first: 10) { edges { node { id name totalPrice createdAt lineItems(first: 5) { edges { node { title quantity } } } } } } }
```

Get customers:

```
query { customers(first: 10) { edges { node { id firstName lastName email ordersCount } } } }
```

#### Example mutations

Create a product:

```
mutation { productCreate(input: { title: "New Product" bodyHtml: "Good Product" vendor: "Vendor Name" productType: "Type" tags: "tag1, tag2" variants: [{ price: "19.99" sku: "SKU123" }] }) { product { id title } userErrors { field message } } }
```

Update a product:

```
mutation { productUpdate(input: { id: "gid://shopify/Product/1234567890" title: "Updated Product Title" }) { product { id title } userErrors { field message } } }
```

Delete a product:

```
mutation { productDelete(id: "gid://shopify/Product/1234567890") { deletedProductId userErrors { field message } } }
```

#### Best practices

* **Paginate results**: Use first, last, after, and before for pagination in queries.
* **Error handling**: Always check for userErrors in mutations to handle any issues that may arise.
* **Rate limiting**: Be aware of rate limits (typically 2 requests per second) and implement retries or exponential backoff if necessary.
* **Use fragments**: For commonly used fields across multiple queries, consider defining fragments to keep your queries DRY.

