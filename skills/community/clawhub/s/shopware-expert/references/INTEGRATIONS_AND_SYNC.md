# INTEGRATIONS AND SYNC

Compiled excerpts from the Shopware Developer Documentation snapshot. Prefer live docs at [developer.shopware.com](https://developer.shopware.com/) when in doubt.

---

## Integrations/API
**Source:** [guides/integrations-api.md](https://developer.shopware.com/docs/v6.6/guides/integrations-api.md)  
# Integrations/API

Generally, Shopware provides two APIs that serve two aspects of integrations with our platform. Both APIs are based on HTTP and though they serve different use cases, they share some underlying concepts. We recommend understanding these concepts before diving deeper into either of the APIs.

## Customer-facing interactions - Store API

Frontend applications usually provide interfaces for users (customers). These applications usually don't expose sensitive data and have two layers of users - anonymous and authenticated i.e., unregistered and registered. Payloads are usually small, performance and availability are critical.

## Backend-facing integrations - Admin API

These integrations are characterized by the exchange of structured data, synchronizations, imports, exports and notifications. Performance is also important in terms of high data loads rather than fast response times. Consistency, error handling, and transaction-safety are critical.

Shopware's Store and Admin APIs offer essential technical resources for you to interact with and customize the platform's core functions, enabling tailored solutions and seamless integration.

---

---

## General Concepts
**Source:** [guides/integrations-api/general-concepts.md](https://developer.shopware.com/docs/v6.6/guides/integrations-api/general-concepts.md)  
# General Concepts

Even though the Admin API and the Store API serve very different purposes, they have some commonalities handy to be aware of.

## Querying data

For the Admin API these apply to the `/search` endpoint, whilst for the Store API they apply to almost every endpoint that returns a list of records.

It starts with a very simple underlying concept, which encapsulates your entire search description in one generic object, referred to as the **search criteria**.

There are some additional instructions that can be specified using **request headers**.

## Documentation

Here you find a common approach regarding the way that Shopware provides endpoint references for its APIs:

## API Versioning

Starting with Shopware version 6.4.0.0, we decided to change our API versioning strategy. The following article will cover what has been done and changed, how it used to be and how the version strategy looks like now.

These topics provide essential foundations for effective API development and usage in Shopware.

---

---

## API Versioning
**Source:** [guides/integrations-api/general-concepts/api-versioning.md](https://developer.shopware.com/docs/v6.6/guides/integrations-api/general-concepts/api-versioning.md)  
# API Versioning

## Overview

Starting with Shopware version 6.4.0.0, we decided to change our API versioning strategy. This article will cover what has been done and changed, how it used to be, and what the version strategy looks like now.

### Versioning prior to 6.4.0.0

Prior to Shopware 6.4.0.0, the API version was mainly found in the routes themselves.

`/api/v3/example-route`

By using the version, one could ensure that his application keeps on working because we are not going to introduce breaking changes within a version. Yet, versions had to be removed every now and then, which would then still break the application.

More on this can be found in our guide [ADR regarding the API version removal](https://github.com/shopware/shopware/blob/trunk/adr/2020-12-02-removing-api-version.md) section.

### Versioning starting with 6.3.5.0

With Shopware 6.4.0.0, we removed the API version from the routes.

**Old**:

`/api/v3/example-route`

**New**:

`/api/example-route`

The version inside the route will keep working with Shopware 6.3.\*, but it will be removed with the next major Shopware version, 6.4.0.

### Deprecations

Deprecations are now added with patch and minor releases but only removed with a major release. This has always been the case for the Core and is now adapted to the API.

Also, deprecated fields and routes are now shown in the Swagger documentation. Have a look at the FAQ beneath to learn how to open Swagger. Have a look for the `@deprecated` annotation on routes or the `Deprecated` flag on entity fields to see which fields or routes are deprecated in the code.

### Route and field availability

The Swagger API reference now includes the necessary information about the route and field availability. For routes, this can look like this:

![Availability route](../../../assets/availability-route.png)

Note the availability information.

Same for fields, here is an example of how it would look like:

![Availability field](../../../assets/availability-field.png)

### API expectations

API expectations can be used as a request header to define the necessary conditions for the server side. Example conditions could be the Shopware version, the existence of plugins, or the version of a plugin. There are some examples:

```text
GET /api/test
sw-expect-packages: shopware/core:~6.4
```

This would expect that at least Shopware with version 6.4 is installed.

```text
GET /api/test
sw-expect-packages: shopware/core:~6.4,swag/paypal:*
```

This would expect that the Shopware version is at least 6.4 and PayPal is installed in any version.

If the conditions are not met, the backend will answer with a *417 Expectation Failed* error.

## FAQ

### I ensure that my application will keep on working by using the version in the route. What now?

Yes, this was necessary for the previous versioning strategy since breaks were also introduced with Shopware minor releases. The new versioning strategy comes with the benefit that breaks are only introduced with major releases, which were always breaking anyway. Thus, one route will keep working for you until the next major release.

### How do I get the currently used version via the API?

You can read the currently used version in the API as well. Starting with Shopware 6.3.5.0, you can use this route to fetch the current version: `GET /api/_info/version`

Prior to that, the version was readable using the following route: `GET /api/v2/_info/config`

### How do I open up the Swagger page?

Simply navigate to the following URL in your shop: `/api/_info/swagger.html`

---

---

## Generated Reference
**Source:** [guides/integrations-api/general-concepts/generated-reference.md](https://developer.shopware.com/docs/v6.6/guides/integrations-api/general-concepts/generated-reference.md)  
# Generated Reference

Shopware generates schemas for both HTTP APIs that can be interpreted by API client libraries and documentation tools, such as [Swagger.io](https://swagger.io/).

These schemas are generated using PHP annotations based on the [swagger-php](https://github.com/zircote/swagger-php) library. When building API extensions, you can also leverage these annotations to let Shopware generate standardized endpoint documentation for your custom endpoints on-the-fly.

::: warning
Due to security restrictions, your **`APP_ENV`** environment variable has to be set to **`dev`** to access any of the specifications described below.
:::

## Swagger UI

The easiest way to access the generated schema is Swagger UI. [Swagger UI](https://swagger.io/tools/swagger-ui/) is a small library that takes an OpenAPI specification and renders it into a more accessible user interface. Shopware already ships with these user interfaces. They are accessible at the following endpoint relative to their respective base path:

```text
/(api|store-api)/_info/swagger.html
```

::: info
The above path is relative and contains `api` (Admin API) and `store-api` seperated by a pipe. Please choose the appropriate option.
:::

::: warning
The Swagger UI is deprecated and can freeze your browser when loading all schemas. We recommend using the Stoplight (see below) instead.
:::

## Stoplight

The easiest way to access the generated schema is Stoplight. [Stoplight](https://docs.stoplight.io/) is a collaborative platform equipping your team with tooling across the API lifecycle that helps them build quality APIs efficiently. Shopware already ships with these user interfaces. They are accessible at the following endpoint relative to their respective base path:

```text
/(api|store-api)/_info/stoplightio.html
```

::: info
The above path is relative and contains `api` (Admin API) and `store-api` seperated by a pipe. Please choose the appropriate option.
:::

You will find a list of all generic endpoints (entity endpoints like product, category, etc.) for the **Admin API** here `api/_info/stoplightio.html?type=jsonapi#/` or access it via the top navigation bar.

## OpenAPI schema

If you don't want to bother with the UI but just fetch the schema definition instead, use the following endpoint:

```text
/(api|store-api)/_info/openapi3.json
```

## Entity schema

If you would like to access the schema definitions of all available entities instead of an endpoint reference, use one of the corresponding schema endpoints instead:

```text
/(api|store-api)/_info/open-api-schema.json
```

---

---

## Partial Data Loading
**Source:** [guides/integrations-api/general-concepts/partial-data-loading.md](https://developer.shopware.com/docs/v6.6/guides/integrations-api/general-concepts/partial-data-loading.md)  
# Partial Data Loading

`Partial data loading` allows you to select specific fields of an entity to be returned by the API. This can be useful if you only need a few fields of an entity and don't want to load the whole entity. This can reduce the response size and improve the performance of your application.

## Partial data loading vs Includes

`Partial data loading` is different from the [includes](./search-criteria.md#includes-apialias) feature. The `includes` works as post-output processing, so the complete entity or data is loaded in the backend side and then filtered, while `partial data loading` works already on database level. This means that the database only loads the requested fields and not the whole entity.

### Usage

```http
POST /api/search/currency
Authorization: Bearer YOUR_ACCESS_TOKEN
Content-Type: application/json
Accept: application/json

{
    "fields": [
        "name"
    ]
}
```

```json
// response
{
  "total": 1,
  "data": [
    {
      "extensions": [],
      "_uniqueIdentifier": "018cda3ac909712496bccc065acf0ff4",
      "translated": {
        "name": "US-Dollar"
      },
      "id": "018cda3ac909712496bccc065acf0ff4",
      "name": "US-Dollar",
      "isSystemDefault": false,
      "apiAlias": "currency"
    }
  ],
  "aggregations": []
}
```

Fields can also reference fields of associations like in this example the assigned salesChannel names of the currency. The API adds the necessary associations automatically.

```http
POST /api/search/currency
Authorization: Bearer YOUR_ACCESS_TOKEN
Content-Type: application/json
Accept: application/json

{
    "fields": [
        "name",
        "salesChannels.name"
    ]
}
```

```json
// response
{
  "total": 1,
  "data": [
    {
      "extensions": [],
      "_uniqueIdentifier": "018cda3ac909712496bccc065acf0ff4",
      "translated": {
        "name": "US-Dollar"
      },
      "id": "018cda3ac909712496bccc065acf0ff4",
      "name": "US-Dollar",
      "salesChannels": [
        {
          "extensions": [],
          "_uniqueIdentifier": "018cda3af56670d6a3fa515a85967bd2",
          "translated": {
            "name": "Storefront"
          },
          "id": "018cda3af56670d6a3fa515a85967bd2",
          "name": "Storefront",
          "apiAlias": "sales_channel"
        }
      ],
      "isSystemDefault": false,
      "apiAlias": "currency"
    }
  ],
  "aggregations": []
}
```

## Default fields

Some fields are always loaded like the `id` or join relevant fields like foreign keys, these are necessary for the API to work correctly and can't be removed.

## Runtime fields

Some fields in the API are generated at runtime like `isSystemDefault` of the currency. These fields are loaded by default when the referenced data is available, otherwise they can be requested in the `fields` parameter to force the API to load them.

For custom entity definitions with runtime flag, the referenced fields need to be specified inside the constructor. See an example from the core:

```php
protected function defineFields(): FieldCollection
{
    return new FieldCollection([
        (new IdField('id', 'id'))->addFlags(new ApiAware(), new PrimaryKey(), new Required()),
        (new StringField('path', 'path'))->addFlags(new ApiAware()),

        // When this field is requested, we need the data of path field to generate the url
        (new StringField('url', 'url'))->addFlags(new ApiAware(), new Runtime(['path'])),
    ]);
}
```

## Limitations

The current limitation of the `partial data loading` is that it only works on the Entity level. Any custom responses like a product detail page or CMS in the Store API can't be used with this feature, as the Store API needs the whole entity to generate the response. If you need a small response, we recommend using the [includes](./search-criteria.md#includes-apialias) feature of the Search API.

---

---

## Request Headers
**Source:** [guides/integrations-api/general-concepts/request-headers.md](https://developer.shopware.com/docs/v6.6/guides/integrations-api/general-concepts/request-headers.md)  
# Request Headers

## sw-language-id

By default, the API delivers the entities via the system language. This can be changed by specifying a language id using the `sw-language-id` header.

```bash
POST /api/search/product
--header 'sw-language-id: be01bd336c204f20ab86eab45bbdbe45'
```

::: info
Shopware only populates a translatable field if there is an explicit translation for that field. Instead, the `translated` object always contains values, if necessary fallbacks.

**Example:** You instruct Shopware to fetch the french translation of a product using the `sw-language-id` header, but there's no french translation for the products name. The resulting field `product.name` will be `null`. When you're building applications, always use `product.translated.[value]`to access translated values, to make sure you will always get a valid translation or fallback value.
:::

## sw-version-id

Shopware 6 allows developers to create multiple versions of an entity. This has been used, for example, for orders. This allows relations, like documents, to pin a specific state of the entity it relates to. However, the API initially only delivers the data of the most recent record. To tell the API that a specific version should be returned, the header `sw-version-id` must be sent along with the request.

```bash
POST /api/search/order
--header 'sw-version-id: 0fa91ce3e96a4bc2be4bd9ce752c3425'
```

## sw-inheritance

Shopware 6 allows developers to define inheritance (parent-child) relationships between entities of the same type. This has been used, for example, for products and their variants. Certain fields of a variant can therefore inherit the data from the parent product or define (i.e. override) them themselves. However, the API initially only delivers the data of its own record, without considering parent-child inheritance. To tell the API that the inheritance should be considered, the header `sw-inheritance` must be sent along with the request.

```bash
POST /api/search/product
--header 'sw-inheritance: 1'
```

## sw-skip-trigger-flow

Flows are an essential part of Shopware and are triggered by events like the creation of a customer. When migrating from another e-commerce platform to shopware, you might import hundreds of thousands of customers via the sync API. In that case, you don't want to trigger the `send email on customer creation` flow. To avoid this behavior, you can pass the `sw-skip-trigger-flow` header.

```bash
POST /api/_action/sync
--header 'sw-skip-trigger-flow: 1'
```

## sw-access-token

Any request to the Store API needs an Authentication with a `sw-access-token`. Refer to [Authentication & Authorization](https://shopware.stoplight.io/docs/store-api/8e1d78252fa6f-authentication-and-authorisation) section of Store API for more details on this.

## sw-context-token

The `sw-context-token` is used to recognize your customers in the context of the Store API. Refer to [Authentication & Authorization](https://shopware.stoplight.io/docs/store-api/8e1d78252fa6f-authentication-and-authorisation) section of Store API for more details on this.

## sw-currency-id

When calling the API, a client can include the `sw-currency-id` header to indicate the currency in which it wants to receive prices. For example, if the header is set to "USD," the API might respond with prices converted to U.S. dollars. This header is associated with the currency settings in the admin panel. It allows clients to dynamically switch between different currencies based on their preferences.

```bash
POST /api/search/order
--header 'sw-currency-id: 1987f5c352434028802556e065cd5b1e'
```

## sw-include-seo-urls

This header indicates whether SEO-friendly URLs for products or categories should be included in the API response. If an API request is made and the `sw-include-seo-urls` header is set, the API response will include all the configured SEO URLs for the specified product. This can provide additional information to the client about the various SEO-friendly paths associated with the product, allowing for better SEO management or customization.

```bash
POST /api/search/product
--header 'sw-include-seo-urls: 1'
```

## sw-app-integration-id

The `sw-app-integration-id` enables seamless connection and data exchange between different software components. This header is required for correct permission checks performed by the backend when fetching or manipulating data. It overrides the default behavior and uses the privileges provided by the app. This is used in the Meteor Admin SDK for the [Repository Data Handling](/resources/admin-extension-sdk/api-reference/data/repository). But the developer itself doesn’t need to care about it because it is handled automatically by the admin.

---

---

## Search Criteria
**Source:** [guides/integrations-api/general-concepts/search-criteria.md](https://developer.shopware.com/docs/v6.6/guides/integrations-api/general-concepts/search-criteria.md)  
*(Body truncated in this bundle; follow the link for the rest.)*

# Search Criteria

## Overview

Generally, we refer to the endpoints that use `POST` method and receive the criteria as a JSON object as **search criteria**. It takes the same arguments as a [DAL criteria](../../plugins/plugins/framework/data-handling/reading-data#filtering). Some endpoints expect more parameters than specified here. However, these differ from one endpoint to another, so we don't specify them here.

A typical **search criteria** looks like this:

```json
{
  "limit": 10,
  "associations": {
    "manufacturer": {},
    "propertyIds": {},
    "cover": {},
    "options": {
      "associations": {
        "productOptions": {},
        "group": {}
      }
    }
  },
  "includes": {
    "product": [
      "calculatedPrice",
      "cover",
      "id",
      "translated",
      "seoUrls",
      "manufacturer",
      "propertyIds",
      "options"
    ],
    "product_media": [
      "media"
    ],
    "media": [
      "thumbnails",
      "width",
      "height",
      "url"
    ],
    "calculated_price": [
      "unitPrice",
      "quantity"
    ]
  }
}
```

In the following, we will go through different parameters that criteria can be assembled from.

| Parameter | Usage |
| :--- | :--- |
| `associations` | Allows to load additional data to the standard data of an entity |
| `includes` | Restricts the output to the defined fields |
| `ids` | Limits the search to a list of Ids |
| `total-count-mode` | Defines whether a total must be determined |
| `page` | Defines at which page the search result should start |
| `limit` | Defines the number of entries to be determined |
| `filter` | Allows you to filter the result and aggregations |
| `post-filter` | Allows you to filter the result but not the aggregations |
| `query` | Enables you to determine a ranking for the search result |
| `term` | Enables you to determine a ranking for the search result |
| `sort` | Defines the sorting of the search result |
| `aggregations` | Specify aggregations to be computed on-the-fly |
| `grouping` | Lets you group records by fields |

## Parameters

### `associations`

The `associations` parameter allows you to load additional data to the minimal data set of an entity without sending an extra request similar to a SQL Join. The parameter's key is the association's property name in the entity. You can pass nested criteria just for that association, e.g., to perform a sort to or apply filters within the association.

```json
{
    "associations": {
        "products": {
            "limit": 5,
            "filter": [
                { "type": "equals", "field": "active", "value": true }
            ],
            "sort": [
                { "field": "name", "order": "ASC" }    
            ]
        }
    }
}
```

### `includes (apiAlias)`

The `includes` parameter allows you to restrict the returned fields.

* Transfer only what you need reduces response payload.
* Easier to consume for client applications.
* When debugging, the response is smaller, and you can concentrate on the essential fields.

```json
{
    "includes": {
        "product": ["id", "name"]
    }
}

// Response
{
    "total": 120,
    "data": [
        {
            "name": "Synergistic Rubber Fish Soda",
            "id": "012cd563cf8e4f0384eed93b5201cc98",
            "apiAlias": "product"
        },
        {
            "name": "Mediocre Plastic Ticket Lift",
            "id": "075fb241b769444bb72431f797fd5776",
            "apiAlias": "product"
        }
  ]
}
```

::: info
All response types come with a `apiAlias` field which you can use to identify the type in your includes field. If you only want a categories id, add: `"category": ["id"]`. For entities, this is the entity name: `product`, `product_manufacturer`, `order_line_item`, ... For other non-entity types like a listing result or a line item, check the full response. This pattern applies not only to simple fields but also to associations.
:::

### `ids`

If you want to perform a simple lookup using just the ids of records, you can pass a list of those using the `ids` field:

```json
{
    "ids": [
        "012cd563cf8e4f0384eed93b5201cc98", 
        "075fb241b769444bb72431f797fd5776",
        "090fcc2099794771935acf814e3fdb24"
    ]
}
```

### `total-count-mode`

The `total-count-mode` parameter can be used to define whether the total for the total number of hits should be determined for the search query. This parameter supports the following values:

* `0 [default]` - No total is determined.
  * Advantage: This is the most performing mode because MySQL Server does not need to run the `SQL_CALC_FOUND_ROWS` in the background.
  * Purpose: Should be used if pagination is not required.
* `1` - An exact total is determined.
  * Purpose: Should be used if a pagination with the exact page number has to be displayed.
  * Disadvantage: Performance intensive. Here you have to work with `SQL_CALC_FOUND_ROWS`.
* `2` - It is determined whether there is a next page.
  * Advantage: Good performance, same as `0`.
  * Purpose: Can be used well for infinite scrolling because, with infinite scrolling, the information is enough to know if there is a next page to load.

```json
{
    "total-count-mode": 1
}
```

### `page & limit`

The `page` and `limit` parameters can be used to control pagination. The `page` parameter is 1-indexed.

```json
{
    "page": 1,
    "limit": 5
}
```

### `filter`

The `filter` parameter allows you to filter the result and aggregations using many filters and parameters. The filter types are equivalent to the filters available for the DAL.

::: info
When you are filtering for nested values - for example, you are filtering orders by their transaction state (`order.transactions.stateMachineState`) - make sure to fetch those in your `associations` field before.
:::

```json
{
  "associations": {
    "transactions": {
      "associations": {
        "stateMachineState": {}
      }
    }
  },
  "filter": [
    {
      "type": "multi",
      "operator": "and",
      "queries": [
        {
          "type": "multi",
          "operator": "or",
          "queries": [
            {
              "type": "equals",
              "field": "transactions.stateMachineState.technicalName",
              "value": "paid"
            },
            {
              "type": "equals",
              "field": "transactions.stateMachineState.technicalName",
              "value": "open"
            }
          ]
        },
        {
          "type": "equals",
          "field": "customFields.exportedFlag",
          "value": null
        }
      ]
    }
  ]
}
```

### `post-filter`

Work the same as `filter`; however, they don't apply to aggregations. This is great when you want to work with aggregations to display facets for filter navigation but already filter results based on filters without making an additional request.

### `query`

Use this parameter to create a weighted search query that returns a `_score` for each found entity. Any filter type can be used for the `query`. A `score` has to be defined for each query. The sum of the matching queries then results in the total `_score` value.

```json
{
    "query": [
        {
            "score": 500,
            "query": { "type": "contains", "field": "name", "value": "Bronze"}
        },
        { 
            "score": 500,
            "query": { "type": "equals", "field": "active", "value": true }
        },
        {
            "score": 100,
            "query": {
                "type": "equals",
                "field": "manufacturerId",
                "value": "db3c17b1e572432eb4a4c881b6f9d68f"
            }
        }
    ]
}
```

The resulting score is appended to every resulting record in the `extensions.search` field:

```json
{
    "total": 5,
    "data": [
        {
            "manufacturerId": "db3c17b1e572432eb4a4c881b6f9d68f",
            "name": "Awesome Bronze Krill Kream",
            "extensions": {
                "search": {
                    "_score": "1100"
                }
            },
            "id": "0acc3aa5c45a492c9a2adb8844cb7adc",
            "apiAlias": "product"
        },
        {
            "manufacturerId": "d0c0daa910d94b3c8b03c2bef6acb9b8",
            "name": "Synergistic Bronze New Tab",
            "extensions": {
                "search": {
                    "_score": "1000"
                }
            },
            "id": "72858576ac634f209b7ad61db15b7cc3",
            "apiAlias": "product"
        },
        {
            "manufacturerId": "3b5f9d51803849c68bb72360debd3da0",
            "name": "Fantastic Paper Zamox",
            "extensions": {
                "search": {
                    "_score": "500"
                }
            },
            "id": "18d2b4225ea34b17a6099108da159e7f",
            "apiAlias": "product"
        }
    ]
}
```

### `term`

Using the `term` parameter, the server performs a text search on all records based on their data model and weighting as defined in the entity definition using the `SearchRanking` flag.

::: info
Don't use `term` parameters together with `query` parameters.
:::

```json
{
    "term": "Awesome Bronze"
}
```

The results are formatted the same as for the `query` parameter above.

## `sort`

The `sort` parameter allows controlling the sorting of the result. Several sorts can be transferred at the same time.

* The `field` parameter defines the field to be used for sorting.
* The `order` parameter defines the sort direction.
* The parameter `naturalSorting` allows using a [Natural Sorting Algorithm](https://en.wikipedia.org/wiki/Natural_sort_order)
* The parameter `type` allows using divergent sorting behavior. Valid values are:
  * `count`: Sort by the count of associations via the given field. SQL representation: `ORDER BY COUNT({field}) {order}`

```json
{
    "limit": 5,
    "sort": [
        { "field": "name", "order": "ASC", "naturalSorting": true },
        { "field": "active", "order": "DESC" },
        { "field": "products.id", "order": "DESC", "type": "count" }
  ]
}
```

### `count` sorting behavior

For demonstration purposes, see the following request payload that additionally includes a `count` aggregation.

::: info
This `count` type was introduced with Shopware 6.4.12.0 and is not available in prior versions.
:::

```json
{
  "limit": 3,
  "includes": {
    "product": ["id"]
  },
  "sort": [
    { "field": "categories.id", "order": "DESC", "type": "count" }
  ],
  "aggregations": [
    {  
        "name": "product-id",
        "type": "terms",
        "field": "id",
        "limit": 3,
        "sort": { "field": "_count", "order": "DESC" },
        "aggregation": {  
            "name": "category-count",
            "type": "count",
            "field": "product.categories.id"
        }
    }
  ]
}
```

In response, the order of the `product` elements is now equal to the order of the aggregated buckets:

```json
{
    "total": 3,
    "aggregations": {
        "product-id": {
            "buckets": [
                {
                    "key": "f977f6a845a54b0381cbaf322f53b63e",
                    "count": 5
                },
                {
                    "key": "8d0ee52433df44b78a6f7827180049d9",
                    "count": 4
                },
                {
                    "key": "003a9df163474b28bc8a000243549547",
                    "count": 3
                }
            ]
        }
    },
    "elements": [
        { "id": "f977f6a845a54b0381cbaf322f53b63e" },
        { "id": "8d0ee52433df44b78a6f7827180049d9" },
        { "id": "003a9df163474b28bc8a000243549547" }
    ]
}
```

## `aggregations`

The `aggregations` parameter can determine metadata for a search query. There are different types of aggregations that are listed in the reference documentation. A simple example is the determination of the average price from a product search query.

* Purpose: Calculation of statistics and metrics.
* Purpose: Determination of possible filters.

The aggregation types

… **Truncated.** Full document: https://developer.shopware.com/docs/v6.6/guides/integrations-api/general-concepts/search-criteria.md


---

