# Shopify docs: Custom Data

> Generated from Shopify official LLM documentation snapshot (maintainer export). Prefer live docs at [shopify.dev](https://shopify.dev/) for API versions and current behaviour.

---
## Custom data

### Custom data

Shopify comes with many built-in data models like products, customers, and orders. Yet often while building for the varied and diverse needs of merchants you'll need a way to customize the data in Shopify:

* Metafields to extend Shopify's resources with custom fields
* Metaobjects to create entirely new resources by making new custom objects

#### Metafields

[Metafields](https://shopify.dev/docs/apps/build/custom-data#what-are-metafields) are a flexible way to store additional details about existing Shopify resources, like products, orders, and many more. These custom fields can be almost anything, such as related products, release dates, internal approval status, or part numbers. Metafields power experiences across Shopify. In the Shopify admin, they enable features like customer segmentation, smart collections, and product taxonomy. For customers, they enhance the shopping experience through product recommendations, product swatches, and customized checkouts using Shopify Functions.

##### Unstructured metafields

Metafields serve as the foundation for extending Shopify's data model. At their core, metafields are key-value pairs that can be added to specific resources in Shopify:

* **Identifier**: Composed of both namespace (drives ownership) and key.
* **Value**: The raw value stored.
* **Type**: How value is interpreted.

The type on an unstructured metafield can vary on an instance-by-instance basis. To ensure consistency, you need a metafield definition.

**Example**
You work with a snowboard merchant who needs to store care instructions for each product. Starting simple, you add a custom.care\_guide metafield to a product by using the `productUpdate` mutation:

```
mutation {
  metafieldDefinitionCreate(definition: {
    name: "Care Guide",
    namespace: "custom",
    key: "care_guide",
    description: "How to care for the product.",
    type: "single_line_text_field",
    ownerType: PRODUCT,
    access: {
      storefront: PUBLIC_READ,
    },
  }) {
    createdDefinition {
      name
      namespace
      key
      type
      access
    }
  }
}
```

##### Structured metafields

Metafields covered by a metafield definition, or structured metafields, have consistent types amongst other optional configurations:

* Data validation
* Permissions
* Optional features
* Conditional usage

**Example**
In this example, you'll add a definition to your snowboard merchant to ensure all products have a `custom.care_guide metafield` with a type of `single_line_text_field` that is also accessible to storefronts:

```
mutation {
  metafieldDefinitionCreate(definition: {
    name: "Care Guide",
    namespace: "custom",
    key: "care_guide",
    description: "How to care for the product.",
    type: "single_line_text_field",
    ownerType: PRODUCT,
    access: {
      storefront: PUBLIC_READ,
    },
  }) {
    createdDefinition {
      name
      namespace
      key
      type
      access
    }
  }
}
```

#### Metaobjects

[Metaobjects](https://shopify.dev/docs/apps/build/custom-data#what-are-metaobjects) are a powerful way to create and reuse custom data structures beyond Shopify's standard resources. They exist independently and can be referenced by metafields to connect with standard resources like products, orders, and customers.

Key terms related to metaobjects:

* **Definition**: The structure outlining the fields and properties for your metaobjects.
* **Entry**: An instance of the associated definition.

Metaobject definitions, beyond defining the fields, also offer control over:

* Permissions, such as storefront visibility.
* Optional features, such as translatable fields.

**Example**
Suppose a merchant wants a `Feature` resource in Shopify. You can represent that with a new metaobject definition:

```
mutation {
  metaobjectDefinitionCreate(definition: {
    type: "$app:feature",
    access: {
      admin: MERCHANT_READ_WRITE,
      storefront: PUBLIC_READ,
    },
    capabilities: {
      translatable: { enabled: true },
    },
    displayNameKey: "title",
    fieldDefinitions: [
      { key: "title", name: "Highlight Title", type: "single_line_text_field", required: true },
      { key: "description", name: "Description", type: "multi_line_text_field", required: true },
      { key: "creative", name: "Creative", type: "file_reference" },
    ]
  }) {
    metaobjectDefinition {
      id
      type
      fieldDefinitions {
        key
        name
        type
      }
    }
  }
}
```

The merchant's products have a set of key features, so you'll also need to create a product metafield definition that references the `Feature` metaobject definition you just created:

```
mutation {
  metafieldDefinitionCreate(definition: {
    name: "Key features",
    key: "key_features",
    description: "Key features of the product.",
    type: "list.metaobject_reference",
    ownerType: PRODUCT,
    access: {
      storefront: PUBLIC_READ,
    },
    validation: {
      metaobjectDefinitionId: "gid://shopify/MetaobjectDefinition/1",
    },
  }) {
    createdDefinition {
      namespace
      key
      type
    }
  }
}
```

With those in place, you can create `Feature` entries and reference as many as you want in a product's `key_features` metafield. These entries can be reused across products, making it easy to manage and update.

