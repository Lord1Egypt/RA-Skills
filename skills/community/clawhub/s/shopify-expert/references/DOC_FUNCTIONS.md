# Shopify docs: Functions

> Generated from Shopify official LLM documentation snapshot (maintainer export). Prefer live docs at [shopify.dev](https://shopify.dev/) for API versions and current behaviour.

---
## Functions

### Functions

[Shopify Functions](https://shopify.dev/docs/api/customer-account-ui-extensions/2025-01/extension-targets-overview) allow developers to customize the backend logic that powers parts of Shopify. They can be used to generate custom discounts, shipping, pickup points and more. Building Shopify Functions is similar to embedded programming - there is a focus on low latency execution and thus there are constraints on execution time.

#### How Functions work

Function extension targets inject code into the backend logic of Shopify. The key parts of a function are:

* **Function input**: The function input is a JSON object which is the result of a GraphQL input query you define. Input queries allow you to select the specific data you need for your function, such as cart line product data or metafields.
* **Function logic**: The function logic is written in any language that can compile a WebAssembly module which meets function requirements. Function templates and client libraries are available for Rust and JavaScript.
* **Function output**: The function output is a JSON document that describes the operations you'd like Shopify to carry out.

GraphQL schemas provided by Shopify specify the targets, available inputs, and expected outputs for a Functions API.

#### Example: Build a Product Discount function
In this example we build a Shopify Function that applies a 20% discount to the first item in the cart

First we create an input query to get the first item in the cart
```
query Input {
  cart {
    lines {
      id
    }
  }
}
```

Then we write a Function in Rust to apply the 20% discount to the cart item
```
use shopify_function::prelude::*;
use shopify_function::Result;
use crate::run::run::output::*;

#[shopify_function_target(query_path = "src/run.graphql", schema_path = "schema.graphql")]
fn run(input: input::ResponseData) -> Result<FunctionRunResult> {
    let mut discounts = vec![];
    let percentage = 20.0;

    // Check if there are any lines in the cart
    if let Some(first_line) = input.cart.lines.first() {
        discounts.push(Discount {
            value: Value::Percentage(Percentage {
                value: Decimal(percentage),
            }),
            targets: vec![Target::CartLine(CartLineTarget {
                id: first_line.id.clone(),
                quantity: None,
            })],
            message: Some(format!("{}% off first item", percentage)),
        });
    }

    Ok(FunctionRunResult {
        discounts,
        discount_application_strategy: DiscountApplicationStrategy::FIRST,
    })
}
```

#### Example: Build a Payment Customization Function
In this example we remove a payment method if the cart total exceeds a certain amount.

Define the input query to fetch the cart total and available payment methods:
```
query Input {
  cart {
    cost {
      totalAmount {
        amount
      }
    }
  }
  paymentMethods {
    id
    name
  }
}
```

This returns the following JSON output
```
{
  "cart": {
    "cost": {
      "totalAmount": {
        "amount": 200.0
      }
    }
  },
  "paymentMethods": [
    {
      "id": "gid://shopify/PaymentCustomizationPaymentMethod/1",
      "name": "Cash on Delivery"
    },
    {
      "id": "gid://shopify/PaymentCustomizationPaymentMethod/2",
      "name": "Credit Card"
    }
  ]
}
```

Then we write a Function in Rust to hide the Cash on Delivery payment method if the value is greater than $100
```
use shopify_function::prelude::*;
use shopify_function::Result;

#[shopify_function_target(query_path = "src/run.graphql", schema_path = "schema.graphql")]
fn run(input: input::ResponseData) -> Result<output::FunctionRunResult> {
    let no_changes = output::FunctionRunResult { operations: vec![] };

    // Get the cart total from the function input, and return early if it's below 100
    let cart_total: f64 = input.cart.cost.total_amount.amount.into();
    if cart_total < 100.0 {
        // You can use debug logs in your function
        log!("Cart total is not high enough, no need to hide the payment method.");
        return Ok(no_changes);
    }

    // Find the payment method to hide, and create a hide output operation from it
    // (this will be None if not found)
    let operations = input
        .payment_methods
        .iter()
        .find(|&method| method.name.contains(&"Cash on Delivery".to_string()))
        .map(|method| {
            vec![output::Operation::Hide(output::HideOperation {
                payment_method_id: method.id.to_string(),
            })]
        })
        .unwrap_or_default();

    // The shopify_function crate serializes your function result
    Ok(output::FunctionRunResult { operations })
}
```

#### Example: Build a Delivery Option Customization Function
In this example we add a "May be delayed due to weather conditions" message to the delivery options, if the delivery address is in North Carolina.

Define the input query to fetch the provinceCode and delivery options:
```
query Input {
  cart {
    deliveryGroups {
      deliveryAddress {
        provinceCode
      }
      deliveryOptions {
        handle
        title
      }
    }
  }
}
```

This returns the following JSON output
```
{
  "cart": {
    "deliveryGroups": [
      {
        "deliveryAddress": {
          "provinceCode": "NC"
        }
        "deliveryOptions": [
            {
              "handle": "shopify-Standard-21.90",
              "title": "Standard"
            },
            {
              "handle": "shopify-Express-31.90",
              "title": "Express"
            },
        ]
      }
    ]
  }
}
```

Then we write a Function in Rust to append the message if the delivery address is in North Carolina
```
use shopify_function::prelude::*;
use shopify_function::Result;

#[shopify_function_target(query_path = "src/run.graphql", schema_path = "schema.graphql")]
fn run(input: input::ResponseData) -> Result<output::FunctionRunResult> {
    // The message we wish to add to the delivery option
    let message = "May be delayed due to weather conditions";

    let to_rename = input
        .cart
        .delivery_groups
        .iter()
        // Filter for delivery groups with a shipping address containing the affected state or province
        .filter(|group| {
            let state_province = group
                .delivery_address
                .as_ref()
                .and_then(|address| address.province_code.as_ref());
            match state_province {
                Some(code) => code == "NC",
                None => false,
            }
        })
        // Collect the delivery options from these groups
        .flat_map(|group| &group.delivery_options)
        // Construct a rename operation for each, adding the message to the option title
        .map(|option| output::RenameOperation {
            delivery_option_handle: option.handle.to_string(),
            title: match &option.title {
                Some(title) => format!("{} - {}", title, message),
                None => message.to_string(),
            },
        })
        // Wrap with an Operation
        .map(output::Operation::Rename)
        .collect();

    // The shopify_function crate serializes your function result
    Ok(output::FunctionRunResult {
        operations: to_rename,
    })
}
```

#### Available Function APIs

* **Delivery Customization API**: Rename, reorder, and sort the delivery options available to buyers during checkout.
  * **Use cases**: Hide delivery options for certain products or customers; reorder delivery options according to user preference; hide delivery options for PO Box addresses; add messaging to delivery option titles
  * **Extension target**: `purchase.delivery-customization.run`
* **Order Discount API**: Create a new type of discount that's applied to all merchandise in the cart.
  * **Use cases**: Money off the order subtotal; money off products on an order; tiered discount by spend.
  * **Extension target**: `purchase.order-discount.run`
* **Product Discount API**: Create a new type of discount that's applied to a particular product or product variant in the cart.
  * **Use cases**: Money off a product; money off a product variant; money off a cart line; buy a specific quantity of a product; buy a specific amount of a product, get a second amount at a discount.
  * **Extension target**: `purchase.product-discount.run`
* **Shipping Discount API**: Create a new type of discount that's applied to one or more shipping rates at checkout.
  * **Use cases**: Free shipping; a discount on shipping; a discount on specific shipping rates.
  * **Extension target**: `purchase.shipping-discount.run`
* **Payment Customization API**: Rename, reorder, and sort the payment methods available to buyers during checkout.
  * **Use cases**: Hide payment methods for carts with totals above or below a given value; reorder payment methods according to user preference; hide payment methods based on customer tag or country; hide and disable gift cards based on cart contents, country and more.
  * **Extension target**: `purchase.payment-customization.run`
* **Cart Transform API**: Expand cart line items and update the presentation of cart line items.
  * **Extension target**: `purchase.cart-transform.run`
* **Cart and Checkout Validation API**: Provide your own validation of a cart and checkout.
  * **Use cases**: Use tokengating or require a customer membership at checkout; verify the age or id of a customer when they proceed through checkout; provide b2b product minimums, maximums, and multiples; provide b2b location order minimums, maximums, or credit limits; specify quantity limits in a flash sale.
  * **Extension target**: `purchase.validation.run`
* **Fulfillment Constraints API**: Provide your own logic for how Shopify should fulfill and allocate an order.
  * **Use cases**: Ensure that n cart line items are fulfilled from the same location; ensure that n cart line items are fulfilled from any of the locations in a list.
  * **Extension target**: `purchase.fulfillment-constraint-rule.run`
* **Local Pickup Delivery Option Generator API**: Generate custom local pickup options available to buyers during checkout.
  * **Use cases**: Generate local pickup options based on custom rules:
  * **Extension target**: `purchase.local-pickup-delivery-option-generator.run`
* **Pickup Point Delivery Option Generator API**: Generate custom pickup point options available to buyers during checkout.
  * **Use cases**: Generate pickup points based on custom rules
  * **Extension target**: `purchase.pickup-point-delivery-option-generator.run`

