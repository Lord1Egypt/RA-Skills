# Shopify docs: Webhooks

> Generated from Shopify official LLM documentation snapshot (maintainer export). Prefer live docs at [shopify.dev](https://shopify.dev/) for API versions and current behaviour.

---
## Webhooks

### Webhooks

The default and recommended way to configure [webhooks](https://shopify.dev/docs/api/webhooks?reference=toml) is using `shopify.app.toml` configuration file. This will ensure that every shop on which your app is installed will provide your app with the same set of events.

You can use the following syntax for subscribing to webhooks where the URI is an endpoint that you provide. This could be an HTTP endpoint, Google Cloud PubSub endpoint, or an AWS Eventbridge endpoint.

```
[[webhooks.subscriptions]]
topics = ["orders/create"]
uri = "https://webhook.site/webhooks/o/app/orders-create"
```

If you wish to use the same URI for all webhooks just put multiple topics into the topics array. If you wish to have different endpoints depending on the topic then you should have multiple `[[webhooks.subscriptions]]` sections in your TOML. Here’s what multiple subscriptions each with a different endpoint would look like:

```
[[webhooks.subscriptions]]
topics = ["orders/create"]
uri = "https://webhook.site/webhooks/app/orders-create"

```

```
[[webhooks.subscriptions]]
topics = ["products/create"]
uri = "https://webhook.site/webhooks/p/app/orders-create"

```

You can use the GraphQL mutations for registering webhooks when you require different events per shop. For example, if you have features in your app that merchants must upgrade to enable then you might want to only receive events that are necessary when merchants upgrade. Here’s a GraphQL mutation to register a webhook on a single shop:

```
mutation WebhookSubscriptionCreate($topic: WebhookSubscriptionTopic!, $webhookSubscription: WebhookSubscriptionInput!) {
  webhookSubscriptionCreate(topic: $topic, webhookSubscription: $webhookSubscription) {
    webhookSubscription {
      id
      topic
      apiVersion {
        handle
      }
      format
      createdAt
    }
    userErrors {
      field
      message
    }
  }
}
```

And that GraphQL takes the following as variable inputs:

```
{
  "topic": "ORDERS_CREATE",
  "webhookSubscription": {
    "uri": "https://webhook.site/webhooks/app/orders-create",
    "format": "JSON"
  }
}
```

For that GraphQL to work your app must be authenticated and have a shop token that it can use to call that mutation on that specific shop.

