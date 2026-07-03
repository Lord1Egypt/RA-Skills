# Stripe Direct Connection Schema

This generated reference belongs to the adjacent `SKILL.md`. Use it for exact action names, action slugs, parameter summaries, sample parameters, and generated JSON parameter schemas.

Product slug: `stripe-direct-connection`

x402 availability: not enabled for this product.

## `cancel_subscription`

Action slug: `cancel-subscription`

Price: `5` credits

This tool will cancel a subscription in Stripe. It takes the following arguments: - subscription (str, required): The ID of the subscription to cancel.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `subscription` | `string` | no | The ID of the subscription to cancel. |

Sample parameters:

```json
{
  "subscription": "example subscription"
}
```

Generated JSON parameter schema:

```json
{
  "subscription": {
    "description": "The ID of the subscription to cancel.",
    "required": false,
    "type": "string"
  }
}
```

## `create_coupon`

Action slug: `create-coupon`

Price: `5` credits

This tool will create a coupon in Stripe. It takes several arguments: - name (str): The name of the coupon. Only use one of percent_off or amount_off, not both: - percent_off (number, optional): The percentage discount to apply (between 0 and 100). - amount_off (number, optional): The amount to subtract from an invoice (in currency minor units, e.g. cents for USD and yen for JPY). Optional arguments for duration. Use if specific duration is desired, otherwise default to 'once'. - duration (str, optional): How long the discount will last ('once', 'repeating', or 'forever'). Defaults to 'once'. - duration_in_months (number, optional): The number of months the discount will last if duration is repeating.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `amount_off` | `number` | no | A positive integer representing the amount to subtract from an invoice total (required if percent_off is not passed) |
| `currency` | `string` | no | Three-letter ISO code for the currency of the amount_off parameter (required if amount_off is passed). Infer based on the amount_off. For example, if a coupon is $2 off, set currency to be USD. |
| `duration` | `string` | no | How long the discount will last. Defaults to "once" |
| `duration_in_months` | `number` | no | The number of months the discount will last if duration is repeating |
| `name` | `string` | no | Name of the coupon displayed to customers on invoices or receipts |
| `percent_off` | `number` | no | A positive float larger than 0, and smaller or equal to 100, that represents the discount the coupon will apply (required if amount_off is not passed) |

Sample parameters:

```json
{
  "amount_off": 1,
  "currency": "USD",
  "duration": "once",
  "duration_in_months": 1,
  "name": "example name",
  "percent_off": 1
}
```

Generated JSON parameter schema:

```json
{
  "amount_off": {
    "description": "A positive integer representing the amount to subtract from an invoice total (required if percent_off is not passed)",
    "required": false,
    "type": "number"
  },
  "currency": {
    "default": "USD",
    "description": "Three-letter ISO code for the currency of the amount_off parameter (required if amount_off is passed). Infer based on the amount_off. For example, if a coupon is $2 off, set currency to be USD.",
    "required": false,
    "type": "string"
  },
  "duration": {
    "default": "once",
    "description": "How long the discount will last. Defaults to \"once\"",
    "enum": [
      "forever",
      "once",
      "repeating"
    ],
    "required": false,
    "type": "string"
  },
  "duration_in_months": {
    "description": "The number of months the discount will last if duration is repeating",
    "required": false,
    "type": "number"
  },
  "name": {
    "description": "Name of the coupon displayed to customers on invoices or receipts",
    "required": false,
    "type": "string"
  },
  "percent_off": {
    "description": "A positive float larger than 0, and smaller or equal to 100, that represents the discount the coupon will apply (required if amount_off is not passed)",
    "required": false,
    "type": "number"
  }
}
```

## `create_customer`

Action slug: `create-customer`

Price: `5` credits

This tool will create a customer in Stripe. It takes two arguments: - name (str): The name of the customer. - email (str, optional): The email of the customer.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `email` | `string` | no | The email of the customer |
| `name` | `string` | no | The name of the customer |

Sample parameters:

```json
{
  "email": "user@example.com",
  "name": "example name"
}
```

Generated JSON parameter schema:

```json
{
  "email": {
    "description": "The email of the customer",
    "format": "email",
    "required": false,
    "type": "string"
  },
  "name": {
    "description": "The name of the customer",
    "required": false,
    "type": "string"
  }
}
```

## `create_invoice`

Action slug: `create-invoice`

Price: `5` credits

This tool will create an invoice in Stripe. It takes two arguments: - customer (str): The ID of the customer to create the invoice for. - days_until_due (int, optional): The number of days until the invoice is due.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `customer` | `string` | no | The ID of the customer to create the invoice for. |
| `days_until_due` | `number` | no | The number of days until the invoice is due. |

Sample parameters:

```json
{
  "customer": "example customer",
  "days_until_due": 1
}
```

Generated JSON parameter schema:

```json
{
  "customer": {
    "description": "The ID of the customer to create the invoice for.",
    "required": false,
    "type": "string"
  },
  "days_until_due": {
    "description": "The number of days until the invoice is due.",
    "required": false,
    "type": "number"
  }
}
```

## `create_invoice_item`

Action slug: `create-invoice-item`

Price: `5` credits

This tool will create an invoice item in Stripe. It takes three arguments: - customer (str): The ID of the customer to create the invoice item for. - price (str): The ID of the price to create the invoice item for. - invoice (str): The ID of the invoice to create the invoice item for.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `customer` | `string` | no | The ID of the customer to create the invoice item for. |
| `invoice` | `string` | no | The ID of the invoice to create the item for. |
| `price` | `string` | no | The ID of the price for the item. |

Sample parameters:

```json
{
  "customer": "example customer",
  "invoice": "example invoice",
  "price": "example price"
}
```

Generated JSON parameter schema:

```json
{
  "customer": {
    "description": "The ID of the customer to create the invoice item for.",
    "required": false,
    "type": "string"
  },
  "invoice": {
    "description": "The ID of the invoice to create the item for.",
    "required": false,
    "type": "string"
  },
  "price": {
    "description": "The ID of the price for the item.",
    "required": false,
    "type": "string"
  }
}
```

## `create_payment_link`

Action slug: `create-payment-link`

Price: `5` credits

This tool will create a payment link in Stripe. It takes two arguments: - price (str): The ID of the price to create the payment link for. - quantity (int): The quantity of the product to include in the payment link.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `price` | `string` | no | The ID of the price to create the payment link for. |
| `quantity` | `number` | no | The quantity of the product to include. |

Sample parameters:

```json
{
  "price": "example price",
  "quantity": 1
}
```

Generated JSON parameter schema:

```json
{
  "price": {
    "description": "The ID of the price to create the payment link for.",
    "required": false,
    "type": "string"
  },
  "quantity": {
    "description": "The quantity of the product to include.",
    "required": false,
    "type": "number"
  }
}
```

## `create_price`

Action slug: `create-price`

Price: `5` credits

This tool will create a price in Stripe. If a product has not already been specified, a product should be created first. It takes three arguments: - product (str): The ID of the product to create the price for. - unit_amount (int): The unit amount of the price in currency minor units, e.g. cents for USD and yen for JPY. - currency (str): The currency of the price.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `currency` | `string` | no | The currency of the price. |
| `product` | `string` | no | The ID of the product to create the price for. |
| `recurring` | `object` | yes | The recurring components of a price such as its interval. |
| `unit_amount` | `number` | no | The unit amount of the price in cents. |

Sample parameters:

```json
{
  "currency": "example currency",
  "product": "example product",
  "recurring": {
    "interval": "day",
    "interval_count": 1
  },
  "unit_amount": 1
}
```

Generated JSON parameter schema:

```json
{
  "currency": {
    "description": "The currency of the price.",
    "required": false,
    "type": "string"
  },
  "product": {
    "description": "The ID of the product to create the price for.",
    "required": false,
    "type": "string"
  },
  "recurring": {
    "additionalProperties": false,
    "description": "The recurring components of a price such as its interval.",
    "properties": {
      "interval": {
        "description": "Specifies billing frequency. Either day, week, month or year.",
        "enum": [
          "day",
          "month",
          "week",
          "year"
        ],
        "required": false,
        "type": "string"
      },
      "interval_count": {
        "description": "The number of intervals between subscription billings. For example, interval=month and interval_count=3 bills every 3 months. Maximum of three years interval allowed (3 years, 36 months, or 156 weeks).",
        "required": false,
        "type": "integer"
      }
    },
    "required": true,
    "type": "object"
  },
  "unit_amount": {
    "description": "The unit amount of the price in cents.",
    "required": false,
    "type": "number"
  }
}
```

## `create_product`

Action slug: `create-product`

Price: `5` credits

This tool will create a product in Stripe. It takes two arguments: - name (str): The name of the product. - description (str, optional): The description of the product.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `description` | `string` | no | The description of the product. |
| `name` | `string` | no | The name of the product. |

Sample parameters:

```json
{
  "description": "example description",
  "name": "example name"
}
```

Generated JSON parameter schema:

```json
{
  "description": {
    "description": "The description of the product.",
    "required": false,
    "type": "string"
  },
  "name": {
    "description": "The name of the product.",
    "required": false,
    "type": "string"
  }
}
```

## `create_refund`

Action slug: `create-refund`

Price: `5` credits

This tool will refund a payment intent in Stripe. It takes three arguments: - payment_intent (str): The ID of the payment intent to refund. - amount (int, optional): The amount to refund in currency minor units, e.g. cents for USD and yen for JPY. - reason (str, optional): The reason for the refund. Options: "duplicate", "fraudulent", "requested_by_customer".

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `amount` | `integer` | no | The amount to refund in cents. |
| `payment_intent` | `string` | no | The ID of the PaymentIntent to refund. |
| `reason` | `string` | no | The reason for the refund. |

Sample parameters:

```json
{
  "amount": 1,
  "payment_intent": "example payment intent",
  "reason": "duplicate"
}
```

Generated JSON parameter schema:

```json
{
  "amount": {
    "description": "The amount to refund in cents.",
    "required": false,
    "type": "integer"
  },
  "payment_intent": {
    "description": "The ID of the PaymentIntent to refund.",
    "required": false,
    "type": "string"
  },
  "reason": {
    "description": "The reason for the refund.",
    "enum": [
      "duplicate",
      "fraudulent",
      "requested_by_customer"
    ],
    "required": false,
    "type": "string"
  }
}
```

## `fetch_stripe_resources`

Action slug: `fetch-stripe-resources`

Price: `5` credits

Retrieve Stripe object details by ID. IMPORTANT: Only call this tool after search_stripe_resources is called to get specific object IDs. Do not use this tool to discover or search for objects. This tool fetches the object information from Stripe including all available fields. It is only able to fetch the following resources (prefixes): - Payment Intents (pi_) - Charges (ch_) - Invoices (in_) - Prices (price_) - Products (prod_) - Subscriptions (sub_) - Customers (cus_) It takes one argument: - id (str): The unique identifier for the Stripe object (e.g. cus_123, pi_123). Note that any amount returned is in currency minor units, e.g. cents for USD and yen for JPY.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `id` | `string` | no | The unique identifier for the Stripe object (e.g. cus_123, pi_123). |

Sample parameters:

```json
{
  "id": "example id"
}
```

Generated JSON parameter schema:

```json
{
  "id": {
    "description": "The unique identifier for the Stripe object (e.g. cus_123, pi_123).",
    "required": false,
    "type": "string"
  }
}
```

## `finalize_invoice`

Action slug: `finalize-invoice`

Price: `5` credits

This tool will finalize an invoice in Stripe. It takes one argument: - invoice (str): The ID of the invoice to finalize.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `invoice` | `string` | no | The ID of the invoice to finalize. |

Sample parameters:

```json
{
  "invoice": "example invoice"
}
```

Generated JSON parameter schema:

```json
{
  "invoice": {
    "description": "The ID of the invoice to finalize.",
    "required": false,
    "type": "string"
  }
}
```

## `get_stripe_account_info`

Action slug: `get-stripe-account-info`

Price: `5` credits

This will get the account info for the logged in Stripe account.

Parameters:

This action does not require parameters.

Sample parameters:

```json
{}
```

Generated JSON parameter schema:

```json
{}
```

## `list_coupons`

Action slug: `list-coupons`

Price: `5` credits

This tool will fetch a list of Coupons from Stripe. It takes one optional argument: - limit (int, optional): The number of coupons to return.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `limit` | `integer` | no | A limit on the number of objects to be returned. Limit can range between 1 and 100. |

Sample parameters:

```json
{
  "limit": 1
}
```

Generated JSON parameter schema:

```json
{
  "limit": {
    "description": "A limit on the number of objects to be returned. Limit can range between 1 and 100.",
    "maximum": 100,
    "minimum": 1,
    "required": false,
    "type": "integer"
  }
}
```

## `list_customers`

Action slug: `list-customers`

Price: `5` credits

This tool will fetch a list of Customers from Stripe. It takes two arguments: - limit (int, optional): The number of customers to return. - email (str, optional): A case-sensitive filter on the list based on the customer's email field.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `email` | `string` | no | A case-sensitive filter on the list based on the customer's email field. The value must be a string. |
| `limit` | `integer` | no | A limit on the number of objects to be returned. Limit can range between 1 and 100. |

Sample parameters:

```json
{
  "email": "user@example.com",
  "limit": 1
}
```

Generated JSON parameter schema:

```json
{
  "email": {
    "description": "A case-sensitive filter on the list based on the customer's email field. The value must be a string.",
    "required": false,
    "type": "string"
  },
  "limit": {
    "description": "A limit on the number of objects to be returned. Limit can range between 1 and 100.",
    "maximum": 100,
    "minimum": 1,
    "required": false,
    "type": "integer"
  }
}
```

## `list_disputes`

Action slug: `list-disputes`

Price: `5` credits

This tool will fetch a list of disputes in Stripe. It takes the following arguments: - charge (string, optional): Only return disputes associated to the charge specified by this charge ID. - payment_intent (string, optional): Only return disputes associated to the PaymentIntent specified by this PaymentIntent ID.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `charge` | `string` | no | Only return disputes associated to the charge specified by this charge ID. |
| `limit` | `integer` | no | A limit on the number of objects to be returned. Limit can range between 1 and 100, and the default is 10. |
| `payment_intent` | `string` | no | Only return disputes associated to the PaymentIntent specified by this PaymentIntent ID. |

Sample parameters:

```json
{
  "charge": "example charge",
  "limit": 10,
  "payment_intent": "example payment intent"
}
```

Generated JSON parameter schema:

```json
{
  "charge": {
    "description": "Only return disputes associated to the charge specified by this charge ID.",
    "required": false,
    "type": "string"
  },
  "limit": {
    "default": 10,
    "description": "A limit on the number of objects to be returned. Limit can range between 1 and 100, and the default is 10.",
    "maximum": 100,
    "minimum": 1,
    "required": false,
    "type": "integer"
  },
  "payment_intent": {
    "description": "Only return disputes associated to the PaymentIntent specified by this PaymentIntent ID.",
    "required": false,
    "type": "string"
  }
}
```

## `list_invoices`

Action slug: `list-invoices`

Price: `5` credits

This tool will fetch a list of Invoices from Stripe. It takes two arguments: - customer (str, optional): The ID of the customer to list invoices for. - limit (int, optional): The number of invoices to return.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `customer` | `string` | no | The ID of the customer to list invoices for. |
| `limit` | `integer` | no | A limit on the number of objects to be returned. Limit can range between 1 and 100, and the default is 10. |

Sample parameters:

```json
{
  "customer": "example customer",
  "limit": 1
}
```

Generated JSON parameter schema:

```json
{
  "customer": {
    "description": "The ID of the customer to list invoices for.",
    "required": false,
    "type": "string"
  },
  "limit": {
    "description": "A limit on the number of objects to be returned. Limit can range between 1 and 100, and the default is 10.",
    "maximum": 100,
    "minimum": 1,
    "required": false,
    "type": "integer"
  }
}
```

## `list_payment_intents`

Action slug: `list-payment-intents`

Price: `5` credits

This tool will list payment intents in Stripe. It takes two arguments: - customer (str, optional): The ID of the customer to list payment intents for. - limit (int, optional): The number of payment intents to return. Note that the payment intent amount returned is in currency minor units, e.g. cents for USD and yen for JPY.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `customer` | `string` | no | The ID of the customer to list payment intents for. |
| `limit` | `integer` | no | A limit on the number of objects to be returned. Limit can range between 1 and 100. |

Sample parameters:

```json
{
  "customer": "example customer",
  "limit": 1
}
```

Generated JSON parameter schema:

```json
{
  "customer": {
    "description": "The ID of the customer to list payment intents for.",
    "required": false,
    "type": "string"
  },
  "limit": {
    "description": "A limit on the number of objects to be returned. Limit can range between 1 and 100.",
    "maximum": 100,
    "minimum": 1,
    "required": false,
    "type": "integer"
  }
}
```

## `list_prices`

Action slug: `list-prices`

Price: `5` credits

This tool will fetch a list of Prices from Stripe. It takes two arguments. - product (str, optional): The ID of the product to list prices for. - limit (int, optional): The number of prices to return. Note that the price unit_amount returned is in currency minor units, e.g. cents for USD and yen for JPY.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `limit` | `integer` | no | A limit on the number of objects to be returned. Limit can range between 1 and 100, and the default is 10. |
| `product` | `string` | no | The ID of the product to list prices for. |

Sample parameters:

```json
{
  "limit": 1,
  "product": "example product"
}
```

Generated JSON parameter schema:

```json
{
  "limit": {
    "description": "A limit on the number of objects to be returned. Limit can range between 1 and 100, and the default is 10.",
    "maximum": 100,
    "minimum": 1,
    "required": false,
    "type": "integer"
  },
  "product": {
    "description": "The ID of the product to list prices for.",
    "required": false,
    "type": "string"
  }
}
```

## `list_products`

Action slug: `list-products`

Price: `5` credits

This tool will fetch a list of Products from Stripe. It takes one optional argument: - limit (int, optional): The number of products to return.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `limit` | `integer` | no | A limit on the number of objects to be returned. Limit can range between 1 and 100, and the default is 10. |

Sample parameters:

```json
{
  "limit": 1
}
```

Generated JSON parameter schema:

```json
{
  "limit": {
    "description": "A limit on the number of objects to be returned. Limit can range between 1 and 100, and the default is 10.",
    "maximum": 100,
    "minimum": 1,
    "required": false,
    "type": "integer"
  }
}
```

## `list_subscriptions`

Action slug: `list-subscriptions`

Price: `5` credits

This tool will list all subscriptions in Stripe. It takes four arguments: - customer (str, optional): The ID of the customer to list subscriptions for. - price (str, optional): The ID of the price to list subscriptions for. - status (str, optional): The status of the subscriptions to list. - limit (int, optional): The number of subscriptions to return.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `customer` | `string` | no | The ID of the customer to list subscriptions for. |
| `limit` | `integer` | no | A limit on the number of objects to be returned. Limit can range between 1 and 100. |
| `price` | `string` | no | The ID of the price to list subscriptions for. |
| `status` | `string` | no | The status of the subscriptions to retrieve. |

Sample parameters:

```json
{
  "customer": "example customer",
  "limit": 1,
  "price": "example price",
  "status": "active"
}
```

Generated JSON parameter schema:

```json
{
  "customer": {
    "description": "The ID of the customer to list subscriptions for.",
    "required": false,
    "type": "string"
  },
  "limit": {
    "description": "A limit on the number of objects to be returned. Limit can range between 1 and 100.",
    "maximum": 100,
    "minimum": 1,
    "required": false,
    "type": "integer"
  },
  "price": {
    "description": "The ID of the price to list subscriptions for.",
    "required": false,
    "type": "string"
  },
  "status": {
    "description": "The status of the subscriptions to retrieve.",
    "enum": [
      "active",
      "all",
      "canceled",
      "incomplete",
      "incomplete_expired",
      "past_due",
      "trialing",
      "unpaid"
    ],
    "required": false,
    "type": "string"
  }
}
```

## `retrieve_balance`

Action slug: `retrieve-balance`

Price: `5` credits

This tool will retrieve the balance from Stripe. It takes no input.

Parameters:

This action does not require parameters.

Sample parameters:

```json
{}
```

Generated JSON parameter schema:

```json
{}
```

## `search_stripe_documentation`

Action slug: `search-stripe-documentation`

Price: `5` credits

Search the Stripe documentation for the given question and language. It takes two arguments: - question (str): The user question to search an answer for in the Stripe documentation. - language (str, optional): The programming language to search for in the the documentation.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `language` | `string` | no | The programming language to search for in the the documentation. |
| `question` | `string` | no | The user question about integrating with Stripe will be used to search the documentation. |
| `search_only_api_ref` | `boolean` | no | When set to true, search only in the Stripe API reference documentation instead of the full documentation set. Use true when users need specific API implementation details, code examples, or parameter references. Use false (default) for conceptual explanations, best practices, integration guides, or troubleshooting help. |

Sample parameters:

```json
{
  "language": "dotnet",
  "question": "example question",
  "search_only_api_ref": true
}
```

Generated JSON parameter schema:

```json
{
  "language": {
    "description": "The programming language to search for in the the documentation.",
    "enum": [
      "dotnet",
      "go",
      "java",
      "node",
      "php",
      "ruby",
      "python",
      "curl"
    ],
    "required": false,
    "type": "string"
  },
  "question": {
    "description": "The user question about integrating with Stripe will be used to search the documentation.",
    "required": false,
    "type": "string"
  },
  "search_only_api_ref": {
    "description": "When set to true, search only in the Stripe API reference documentation instead of the full documentation set. Use true when users need specific API implementation details, code examples, or parameter references. Use false (default) for conceptual explanations, best practices, integration guides, or troubleshooting help.",
    "required": false,
    "type": "boolean"
  }
}
```

## `search_stripe_resources`

Action slug: `search-stripe-resources`

Price: `5` credits

This tool can be used to search for specific Stripe resources using a custom Stripe query syntax. It is only able to search for the following resources: customers, payment_intents, charges, invoices, prices, products, subscriptions. It returns a maximum of 100 results. IMPORTANT: For most use cases, prefer using the specific `list_` tools (e.g., `list_customers`, `list_payment_intents`) when you know the resource type you need. Only use this search tool when you need to: - Search across multiple resource types simultaneously - Search by field values that aren't supported by list tools - Use complex query syntax that isn't supported by list tools It takes one argument: - query (str): The query consisting of the Stripe resource to query for and the query clause in Stripe's custom query syntax to query metadata for. Note that any amount returned is in currency minor units, e.g. cents for USD and yen for JPY.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `query` | `string` | no | This query string should be formatted as 'resource:query_clause', where 'resource' is one of (customers, payment_intents, charges, invoices, prices, products, subscriptions), and 'query_clause' is the actual query in Stripe's custom query syntax to query metadata for that resource. For example, for the query: customers:email:"jenny.rosen@example.com" resource: `customers` query_clause: `email:"jenny.rosen@example.com"` A query clause consists of a field, operator, and value. ## Query Fields for customers * created * email * metadata * name * phone ## Query Fields for payment_intents * amount * created * currency * customer * metadata * status ## Query Fields for charges * amount * billing_details.address.postal_code * created * currency * customer * disputed * metadata * payment_method_details.{{SOURCE}}.last4 * payment_method_details.{{SOURCE}}.exp_month * payment_method_details.{{SOURCE}}.exp_year * payment_method_details.{{SOURCE}}.brand * payment_method_details.{{SOURCE}}.fingerprint * refunded * status ## Query Fields for invoices * created * currency * customer * last_finalization_error_code * last_finalization_error_type * metadata * number * receipt_number * status * subscription * total ## Query Fields for prices * active * currency * lookup_key * metadata * product * type ## Query Fields for products * active * description * metadata * name * shippable * url ## Query Fields for subscriptions * created * metadata * status * canceled_at ## Search Operators The following table lists the syntax that you can use to construct a query: \| Syntax \| Usage \| Description \| When to Use \| Examples \| \|--------\|-------\|-------------\|-------------\|----------\| \| `:` \| `field:value` \| Exact match operator (case insensitive) \| **ONLY when you know the exact complete value** \| `currency:"eur"` returns records where the currency is exactly "EUR" \| \| `~` \| `field~value` \| Substring match operator (minimum 3 characters) \| **ALWAYS use for domain searches, partial names, email parts** \| `email~"foo.com"` returns emails containing "foo.com" \| \| `AND`, `and` \| `field:value1 AND field:value2` \| Returns records that match both clauses \| Combining multiple conditions \| `status:"active" AND amount:500` \| \| `OR`, `or` \| `field:value1 OR field:value2` \| Returns records that match either clause \| Alternative conditions \| `currency:"usd" OR currency:"eur"` \| \| `-` \| `-field:value` \| Returns records that don't match the clause \| Excluding specific values \| `-currency:"jpy"` returns records not in JPY \| \| `NULL`, `null` \| `field:null` \| Checks for field presence (empty/null values) \| Finding empty fields \| `url:null` returns records where URL field is empty \| \| `>`, `<`, `>=`, `<=`, `=` \| `field>value`, `field<value`, etc. \| Numeric comparison operators \| Amount ranges, dates \| `amount>="10"` returns records with amount >= 10 \| \| `` \| `" """` \| Escape quotes within quotes \| When quotes are in the search value \| `description:"the story called "The Sky and the Sea.""` \| ## Query Rules * You can combine up to 10 query clauses in a search by separating them with a space or using AND/OR keywords (case insensitive) * You cannot combine AND and OR in the same query * No parentheses are supported for operator precedence * By default, the API combines clauses with AND logic * You must use quotation marks around string values (optional for numeric values) * You can escape quotes inside quotes with a backslash (\) ## Examples Input: Look up charges matching a custom metadata value. Output: charges:metadata['order_id']:'1234567890' Input: Look up charges matching the last 4 digits of the card used for the payment. Output: charges:payment_method_details.card.last4:4242 Input: Look up customers matching an email. Output: customers:email:'jenny.rosen@example.com' Input: Look up PaymentIntents not in the USD currency. Output: payment_intents:-currency:'usd' Input: Filter invoice objects with a total greater than 1000. Output: invoices:total>1000 Input: Filter payments with a amount over $100. Reasoning: Stripe "amount" field is in cents, so we use 1000 instead of 100 Output: payment_intents:amount>1000 Input: Look up charges matching a combination of metadata and currency. Output: charges:metadata['key']:'value' AND currency:'usd' Input: Search for customers with email containing "john". Output: customers:email~"john" Input: Find products where the description field is empty. Output: products:description:null Input: Search for payments with amounts greater than or equal to 5000. Output: payment_intents:amount>=5000 Input: Search for products with description with escaped quotes. Output: products:description:"The story called "The Sky and the Sea"." |

Sample parameters:

```json
{
  "query": "example search query"
}
```

Generated JSON parameter schema:

```json
{
  "query": {
    "description": "This query string should be formatted as 'resource:query_clause', where 'resource' is one of (customers, payment_intents, charges, invoices, prices, products, subscriptions), and 'query_clause' is the actual query in Stripe's custom query syntax to query metadata for that resource.\n\nFor example, for the query: customers:email:\"jenny.rosen@example.com\"\nresource: `customers`\nquery_clause: `email:\"jenny.rosen@example.com\"`\n\nA query clause consists of a field, operator, and value.\n\n## Query Fields for customers\n* created\n* email\n* metadata\n* name\n* phone\n\n## Query Fields for payment_intents\n* amount\n* created\n* currency\n* customer\n* metadata\n* status\n\n## Query Fields for charges\n* amount\n* billing_details.address.postal_code\n* created\n* currency\n* customer\n* disputed\n* metadata\n* payment_method_details.{{SOURCE}}.last4\n* payment_method_details.{{SOURCE}}.exp_month\n* payment_method_details.{{SOURCE}}.exp_year\n* payment_method_details.{{SOURCE}}.brand\n* payment_method_details.{{SOURCE}}.fingerprint\n* refunded\n* status\n\n## Query Fields for invoices\n* created\n* currency\n* customer\n* last_finalization_error_code\n* last_finalization_error_type\n* metadata\n* number\n* receipt_number\n* status\n* subscription\n* total\n\n## Query Fields for prices\n* active\n* currency\n* lookup_key\n* metadata\n* product\n* type\n\n## Query Fields for products\n* active\n* description\n* metadata\n* name\n* shippable\n* url\n\n## Query Fields for subscriptions\n* created\n* metadata\n* status\n* canceled_at\n\n## Search Operators\nThe following table lists the syntax that you can use to construct a query:\n\n| Syntax | Usage | Description | When to Use | Examples |\n|--------|-------|-------------|-------------|----------|\n| `:` | `field:value` | Exact match operator (case insensitive) | **ONLY when you know the exact complete value** | `currency:\"eur\"` returns records where the currency is exactly \"EUR\" |\n| `~` | `field~value` | Substring match operator (minimum 3 characters) | **ALWAYS use for domain searches, partial names, email parts** | `email~\"foo.com\"` returns emails containing \"foo.com\" |\n| `AND`, `and` | `field:value1 AND field:value2` | Returns records that match both clauses | Combining multiple conditions | `status:\"active\" AND amount:500` |\n| `OR`, `or` | `field:value1 OR field:value2` | Returns records that match either clause | Alternative conditions | `currency:\"usd\" OR currency:\"eur\"` |\n| `-` | `-field:value` | Returns records that don't match the clause | Excluding specific values | `-currency:\"jpy\"` returns records not in JPY |\n| `NULL`, `null` | `field:null` | Checks for field presence (empty/null values) | Finding empty fields | `url:null` returns records where URL field is empty |\n| `>`, `<`, `>=`, `<=`, `=` | `field>value`, `field<value`, etc. | Numeric comparison operators | Amount ranges, dates | `amount>=\"10\"` returns records with amount >= 10 |\n| `` | `\" \"\"\"` | Escape quotes within quotes | When quotes are in the search value | `description:\"the story called \"The Sky and the Sea.\"\"` |\n\n## Query Rules\n* You can combine up to 10 query clauses in a search by separating them with a space or using AND/OR keywords (case insensitive)\n* You cannot combine AND and OR in the same query\n* No parentheses are supported for operator precedence\n* By default, the API combines clauses with AND logic\n* You must use quotation marks around string values (optional for numeric values)\n* You can escape quotes inside quotes with a backslash (\\)\n\n## Examples\n\nInput: Look up charges matching a custom metadata value.\nOutput: charges:metadata['order_id']:'1234567890'\n\nInput: Look up charges matching the last 4 digits of the card used for the payment.\nOutput: charges:payment_method_details.card.last4:4242\n\nInput: Look up customers matching an email.\nOutput: customers:email:'jenny.rosen@example.com'\n\nInput: Look up PaymentIntents not in the USD currency.\nOutput: payment_intents:-currency:'usd'\n\nInput: Filter invoice objects with a total greater than 1000.\nOutput: invoices:total>1000\n\nInput: Filter payments with a amount over $100.\nReasoning: Stripe \"amount\" field is in cents, so we use 1000 instead of 100\nOutput: payment_intents:amount>1000\n\nInput: Look up charges matching a combination of metadata and currency.\nOutput: charges:metadata['key']:'value' AND currency:'usd'\n\nInput: Search for customers with email containing \"john\".\nOutput: customers:email~\"john\"\n\nInput: Find products where the description field is empty.\nOutput: products:description:null\n\nInput: Search for payments with amounts greater than or equal to 5000.\nOutput: payment_intents:amount>=5000\n\nInput: Search for products with description with escaped quotes.\nOutput: products:description:\"The story called \"The Sky and the Sea\".\"\n",
    "required": false,
    "type": "string"
  }
}
```

## `send_stripe_mcp_feedback`

Action slug: `send-stripe-mcp-feedback`

Price: `5` credits

Submit feedback from user or agent about Stripe's MCP server tools. Valid: "the search tool returned irrelevant results", "I wish there was a tool for X" Invalid: Stripe API complaints, AI model issues, IDE/environment problems - Only call when feedback clearly targets MCP tools. - If feedback is about one specific tool, include its name in tool_name. - If feedback is from user, quote their exact message and set source to "user". - If a tool didn't follow your expectations as an agent, set source to "agent".

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `context` | `string` | no | What the user was trying to accomplish. |
| `quote` | `string` | no | User's exact message containing feedback. Max 1000 chars. |
| `sentiment` | `string` | no | positive, negative, or neutral |
| `source` | `string` | no | user or agent |
| `tool_name` | `string` | no | The name of the tool the user is giving feedback about. Include if confident that feedback is about a specific tool. |

Sample parameters:

```json
{
  "context": "example context",
  "quote": "example quote",
  "sentiment": "positive",
  "source": "user",
  "tool_name": "example tool name"
}
```

Generated JSON parameter schema:

```json
{
  "context": {
    "description": "What the user was trying to accomplish.",
    "required": false,
    "type": "string"
  },
  "quote": {
    "description": "User's exact message containing feedback. Max 1000 chars.",
    "required": false,
    "type": "string"
  },
  "sentiment": {
    "description": "positive, negative, or neutral",
    "enum": [
      "positive",
      "negative",
      "neutral"
    ],
    "required": false,
    "type": "string"
  },
  "source": {
    "description": "user or agent",
    "enum": [
      "user",
      "agent"
    ],
    "required": false,
    "type": "string"
  },
  "tool_name": {
    "description": "The name of the tool the user is giving feedback about. Include if confident that feedback is about a specific tool.",
    "required": false,
    "type": "string"
  }
}
```

## `stripe_integration_recommender`

Action slug: `stripe-integration-recommender`

Price: `5` credits

Guides users through Stripe integration planning via interactive Q&A. Analyzes payment requirements and recommends the appropriate Stripe products (Checkout, Elements, Billing, Connect, etc.) with step-by-step implementation guidance. WHEN TO USE: Call this tool when the user expresses: - Payment keywords: "payments", "checkout", "billing", "subscriptions", "invoices" - Commercial intent: "sell", "monetize", "charge users", "e-commerce" - Stripe mention: User references "Stripe" directly IMPORTANT BEHAVIOR: - You may call this tool with partial information—the tool will ask clarifying questions. Do not wait until you have complete requirements. - Once a plan is in progress, stay in the Q&A flow until completion. If the user asks for clarification or advice (e.g., "what's best for me?"), answer them, then continue with the plan. Only exit early if the user explicitly requests it or the tool returns an unrecoverable error. - When the tool returns type="question", present the question to the user exactly as provided. PARAMETERS: - plan_id (optional): Required for continuing/updating. Omit when starting new plan. - answer (required): For new plans, provide summary. For existing plans, provide user response. Accepts option selections ('Option 1'), natural language, clarifying questions, or 'UNKNOWN'. - notes (optional): Technical context you've observed (e.g., "Python/Flask backend", "user wants minimal code to go live quickly", "already has Stripe SDK installed"). Returns JSON: - type="question": Plan in progress. Contains `question` to present to user and `plan_id` to include in next call. - type="summary": plan_id, status, summary (blueprints, prerequisites, sample_code) - type="error": status, error (code, message, user_visible, agent_guidance) WORKFLOW: - New plan: Call without plan_id + answer → Present question EXACTLY → Get answer → Call with plan_id + answer → Repeat - Continue plan: Present question EXACTLY → Analyze code → Formulate answer → Get approval → Call with plan_id + answer + notes → Repeat LIMITATIONS: - Generates integration guidance only; does not execute code or create Stripe resources. - Cannot modify completed or expired plans—start a new plan instead.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `answer` | `string` | no | For new plans (no plan_id): 2-3 sentence summary including (1) business name and payment model, (2) tech stack with frontend AND backend (use 'UNKNOWN' for unknown components), (3) payment requirements (use 'UNKNOWN' if not specified). For existing plans: User's verbatim response. Accepts option selections ('Option 1'), natural language, clarifying questions, or 'UNKNOWN'. |
| `notes` | `string` | no | Optional agent-discovered context from codebase analysis (e.g., 'Found Stripe SDK v12.0.0', 'Existing webhook at /api/stripe'). Helps backend provide accurate recommendations. |
| `plan_id` | `string` | no | Plan identifier in format lplan_[alphanumeric] from previous response. Required for continuing existing plan. Omit when starting new plan. |

Sample parameters:

```json
{
  "answer": "example answer",
  "notes": "example notes",
  "plan_id": "example plan id"
}
```

Generated JSON parameter schema:

```json
{
  "answer": {
    "description": "For new plans (no plan_id): 2-3 sentence summary including (1) business name and payment model, (2) tech stack with frontend AND backend (use 'UNKNOWN' for unknown components), (3) payment requirements (use 'UNKNOWN' if not specified). For existing plans: User's verbatim response. Accepts option selections ('Option 1'), natural language, clarifying questions, or 'UNKNOWN'.",
    "required": false,
    "type": "string"
  },
  "notes": {
    "description": "Optional agent-discovered context from codebase analysis (e.g., 'Found Stripe SDK v12.0.0', 'Existing webhook at /api/stripe'). Helps backend provide accurate recommendations.",
    "required": false,
    "type": "string"
  },
  "plan_id": {
    "description": "Plan identifier in format lplan_[alphanumeric] from previous response. Required for continuing existing plan. Omit when starting new plan.",
    "pattern": "^lplan_[a-zA-Z0-9]+$",
    "required": false,
    "type": "string"
  }
}
```

## `update_dispute`

Action slug: `update-dispute`

Price: `5` credits

When you receive a dispute, contacting your customer is always the best first step. If that doesn't work, you can submit evidence to help resolve the dispute in your favor. This tool helps. It takes the following arguments: - dispute (string): The ID of the dispute to update - evidence (object, optional): Evidence to upload for the dispute. - cancellation_policy_disclosure (string) - cancellation_rebuttal (string) - duplicate_charge_explanation (string) - uncategorized_text (string, optional): Any additional evidence or statements. - submit (boolean, optional): Whether to immediately submit evidence to the bank. If false, evidence is staged on the dispute.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `dispute` | `string` | no | The ID of the dispute to update |
| `evidence` | `object` | no | Evidence to upload, to respond to a dispute. Updating any field in the hash will submit all fields in the hash for review. |
| `submit` | `boolean` | no | Whether to immediately submit evidence to the bank. If false, evidence is staged on the dispute. |

Sample parameters:

```json
{
  "dispute": "example dispute",
  "evidence": {
    "cancellation_policy_disclosure": "example cancellation policy disclosure",
    "duplicate_charge_explanation": "example duplicate charge explanation",
    "uncategorized_text": "example uncategorized text"
  },
  "submit": true
}
```

Generated JSON parameter schema:

```json
{
  "dispute": {
    "description": "The ID of the dispute to update",
    "required": false,
    "type": "string"
  },
  "evidence": {
    "additionalProperties": false,
    "description": "Evidence to upload, to respond to a dispute. Updating any field in the hash will submit all fields in the hash for review.",
    "properties": {
      "cancellation_policy_disclosure": {
        "description": "An explanation of how and when the customer was shown your refund policy prior to purchase.",
        "required": false,
        "type": "string"
      },
      "duplicate_charge_explanation": {
        "description": "An explanation of the difference between the disputed charge versus the prior charge that appears to be a duplicate.",
        "required": false,
        "type": "string"
      },
      "uncategorized_text": {
        "description": "Any additional evidence or statements.",
        "required": false,
        "type": "string"
      }
    },
    "required": false,
    "type": "object"
  },
  "submit": {
    "description": "Whether to immediately submit evidence to the bank. If false, evidence is staged on the dispute.",
    "required": false,
    "type": "boolean"
  }
}
```

## `update_subscription`

Action slug: `update-subscription`

Price: `5` credits

This tool will update an existing subscription in Stripe. If changing an existing subscription item, the existing subscription item has to be set to deleted and the new one has to be added. It takes the following arguments: - subscription (str, required): The ID of the subscription to update. - proration_behavior (str, optional): Determines how to handle prorations when the subscription items change. Options: 'create_prorations', 'none', 'always_invoice', 'none_implicit'. - items (array, optional): A list of subscription items to update, add, or remove. Each item can have the following properties: - id (str, optional): The ID of the subscription item to modify. - price (str, optional): The ID of the price to switch to. - quantity (int, optional): The quantity of the plan to subscribe to. - deleted (bool, optional): Whether to delete this item.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `items` | `array` | no | A list of subscription items to update, add, or remove. |
| `proration_behavior` | `string` | no | Determines how to handle prorations when the subscription items change. |
| `subscription` | `string` | no | The ID of the subscription to update. |

Sample parameters:

```json
{
  "items": [
    {
      "deleted": true,
      "id": "example id",
      "price": "example price",
      "quantity": 1
    }
  ],
  "proration_behavior": "always_invoice",
  "subscription": "example subscription"
}
```

Generated JSON parameter schema:

```json
{
  "items": {
    "description": "A list of subscription items to update, add, or remove.",
    "items": {
      "additionalProperties": false,
      "properties": {
        "deleted": {
          "description": "Whether to delete this item.",
          "type": "boolean"
        },
        "id": {
          "description": "The ID of the subscription item to modify.",
          "type": "string"
        },
        "price": {
          "description": "The ID of the price to switch to.",
          "type": "string"
        },
        "quantity": {
          "description": "The quantity of the plan to subscribe to.",
          "type": "number"
        }
      },
      "type": "object"
    },
    "required": false,
    "type": "array"
  },
  "proration_behavior": {
    "description": "Determines how to handle prorations when the subscription items change.",
    "enum": [
      "always_invoice",
      "create_prorations",
      "none",
      "none_implicit"
    ],
    "required": false,
    "type": "string"
  },
  "subscription": {
    "description": "The ID of the subscription to update.",
    "required": false,
    "type": "string"
  }
}
```
