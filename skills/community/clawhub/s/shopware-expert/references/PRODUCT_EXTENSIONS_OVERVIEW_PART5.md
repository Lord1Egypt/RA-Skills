# PRODUCT EXTENSIONS OVERVIEW

Compiled excerpts from the Shopware Developer Documentation snapshot. Prefer live docs at [developer.shopware.com](https://developer.shopware.com/) when in doubt.

---

## Mixed subscription checkout
**Source:** [products/extensions/subscriptions/guides/mixed-checkout.md](https://developer.shopware.com/docs/products/extensions/subscriptions/guides/mixed-checkout.md)  
# Mixed subscription checkout

::: info
Available since Shopware version 6.7.4.0
:::

This guide describes how the so-called `mixed carts` for subscriptions work and how extensions should integrate with it.
Mixed carts let customers buy subscription products and one‑time products during a single checkout while keeping subscription calculation isolated and predictable.

Please familiarize yourself with the [concept](../concept.md) first before continuing here.

## Overview

Subscription line items are ordinary product line items in the main cart, but they carry subscription plan and interval IDs in their payload.
During cart calculation, line items containing subscription plan and interval IDs in their payload are collected and grouped by plan and interval.
For each group a derived *managed* subscription context and a *managed* subscription cart are created and calculated using the subscription cart calculation path.
These represent the context and content of the upcoming generated subscription.

Managed subscription contexts and carts are persisted in the database as well.
They are linked back to the main context by the `subscription_cart` database table.

## Retrieving information

You can access the managed carts through the cart extension named `subscriptionManagedCarts`, which maps keys in the form `<plan-id>-<interval-id>` to their corresponding [managed cart](../concept.md#subscription-cart).
The sales channel context extension named `subscriptionManagedContexts` provides the same mapping for [managed sales channel contexts](../concept.md#subscription-context).
The intended way of retrieving plan and interval IDs is to split the composite ID out of this mapping.

When an order is placed from a mixed cart, the order will contain an `initialSubscriptions` extension that includes all created subscriptions.
As any subsequent orders are generated per subscription, the orders will contain a `subscriptionId` / `subscription` extension instead.

```json
{ // main sales channel context
  "token": "<main-context-token>",
  "extensions": {
    "subscriptionManagedContexts": {
      "<plan-id>-<interval-a-id>": {}, // subscription sales channel context
      "<plan-id>-<interval-b-id>": {   // subscription sales channel context
        "token": "<subscription-context-token>",
        "extensions": {
          "subscription": {
            "mainToken": "<main-context-token>",
            "subscriptionToken": "<subscription-context-token>",
            "managed": true,
            "plan": {},     // subscription plan entity
            "interval": {}, // subscription interval entity
          }
        }
      }
    }
  }
}
```

```json
{ // main cart
  "token": "<main-context-token>",
  "extensions": {
    "subscriptionManagedCarts": {
      "<plan-id>-<interval-a-id>": {}, // subscription cart
      "<plan-id>-<interval-b-id>": {   // subscription cart
        "token": "<subscription-context-token>",
        "lineItems": [
          { // subscription line item
            "label": "Product A",
            "payload": {
              "subscriptionPlan": "<plan-id>",
              "subscriptionInterval": "<interval-id>",
            }
          }
        ]
      }
    }
  }
}
```

## Manipulate mixed cart

With subscription mixed carts, you manipulate the main cart as [you are used to](../../../../guides/plugins/plugins/checkout/cart/).
This is different from the [separate checkout](./separate-checkout.md#manipulate-subscription-cart), where you manipulate a separate subscription cart directly, e.g. by subscription scoped cart processors or separate Store API routes.
Therefore, to support mixed carts, your cart collectors and processors should process both subscription carts and regular carts, so they need to be tagged with `subscription.cart.collector` (or `subscription.cart.processor`) as well as `shopware.cart.collector` (or `shopware.cart.processor`).
If you need to differentiate between main and subscription cart calculations, check the sales channel context for the [subscription extension](../concept.md#subscription-context).
If you need to differentiate between a mixed and a separate subscription cart calculation, check `salesChannelContext.extensions.subscription.isManaged`.

The cart processor `Shopware\Commercial\Subscription\Checkout\Cart\Discount\SubscriptionDiscountProcessor` is a good example how to add line items to mixed carts.

:::warning
We discourage the use of subscription collectors and processors for adding new line items **only** to subscription carts.
Instead, always make sure to add line items to the main cart as well.
This is because it's potentially confusing for customers, and handling line items in subscription carts missing in the main cart is more difficult.
Instead, follow [the steps described below](#adding-subscription-line-items) to add additional line items.

If you still want to add line items to subscription carts only, please add a subscriber to the `SubscriptionOrderLineItemRestoredEvent` event to correctly show the line item in Shopware's after order process.
:::

### Adding subscription line items

To add a line item to a subscription cart, the relevant subscription plan and interval IDs must be added.

The following methods are available to do so via the **Store-API**:

* Add `lineItem.subscriptionPlan` and `lineItem.subscriptionInterval` IDs to a line item
* Add `lineItem.subscriptionPlan` and `lineItem.subscriptionInterval-<plan-id>` IDs to a line item (useful when submitting HTML forms)
* Add `lineItem.payload.subscriptionPlan` and `lineItem.payload.subscriptionInterval` IDs to a line item's payload

Information added through the first two methods will be remapped to the line item's payload, as shown in the last method.

To do so via the **backend**, like in cart collectors or processors, the following methods are available:

* Add `lineItem.payload.subscriptionPlan` and `lineItem.payload.subscriptionInterval` IDs to a line items payload

```php
// retrieve plan and interval IDs in subscription collectors and processors 
$subscriptionPlanId = $salesChannelContext->getExtension('subscription')->getPlan()->getId();
$subscriptionIntervalId = $salesChannelContext->getExtension('subscription')->getInterval()->getId();

// generating a composite ID to avoid
// merging into existing line items of the same product
$lineItemId = sprintf('%s-%s-%s', '<product-id>', '<subscription-plan-id>', '<subscription-interval-id>');

$lineItem = new LineItem($lineItemId, LineItem::PRODUCT_LINE_ITEM_TYPE, '<product-id>');
$lineItem->setQuantity(1);
$lineItem->setPayloadValue('subscriptionPlan', $planId);
$lineItem->setPayloadValue('subscriptionInterval', $intervalId);
// ...

$cart->add($lineItem);
```

```html
<form
  id="productDetailPageSubscriptionBuyProductForm"
  action="/checkout/line-item/add"
  method="post"
>
  <input
    type="hidden"
    name="lineItems[<product-id>][id]"
    value="<product-id>"
  >

  <input
    type="radio"
    name="lineItems[<product-id>][subscriptionPlan]"
    value="<subscription-plan-id>"
  >

  <select name="lineItems[<product-id>][subscriptionInterval-<subscription-plan-id>]">
    <option value="<subscription-interval-id>">Weekly interval</option>
    <option value="<subscription-interval-id>">Monthly interval</option>
    <option value="<subscription-interval-id>">Yearly interval</option>
  </select>
</form>
```

```sh
curl -XPOST '/store-api/checkout/cart/line-item' -d '{
    "lineItems": [{
      "id": <product-id>,
      "subscriptionPlan": <subscription-plan-id>,
      "subscriptionInterval": <subscription-interval-id>
      ...
    }]
  }'
```

## Events

A mixed cart will fire all events like usual.
Additionally, any event fired during the subscription cart calculation will be prefixed with `subscription.` like it is the case in the [separate checkout](./separate-checkout.md#events).

:::info
Note that unlike the separate checkout, only the normal `CheckoutOrderPlacedEvent` but no `'subscription.' . CheckoutOrderPlacedEvent` (or similar) will be fired, as the subscription carts are not placed as separate orders.
:::

## Mixed carts in the Storefront

To change the following Storefront pages if a mixed cart is present, the template scope `mixed-subscription` must be added to the page's Twig templates and subsequent Twig templates used:

* `frontend.checkout.cart.page` / `@Storefront/storefront/page/checkout/cart/index.html.twig`
* `frontend.checkout.confirm.page` / `@Storefront/storefront/page/checkout/confirm/index.html.twig`
* `frontend.checkout.register.page` / `@Storefront/storefront/page/checkout/address/index.html.twig`
* `frontend.account.edit-order.page` / `@Storefront/storefront/page/account/order/index.html.twig`
* `frontend.account.login.page` / `@Storefront/storefront/page/account/register/index.html.twig`
* `frontend.account.register.page` / `@Storefront/storefront/page/account/register/index.html.twig`
* `frontend.cart.offcanvas` / `@Storefront/storefront/component/checkout/offcanvas-cart.html.twig`

Further information can be found in the [dedicated guide here](./template-scoping.md).
The list can be changed through the `subscription.routes.mixed-storefront-scope` Symfony container parameter.

Besides the scope change in Twig templates, the following additional information is available in Twig templates:

* The global `context` will have the `subscriptionManagedContexts` extension available. See [here](#retrieving-information)
* `page.cart` will have the `subscriptionManagedCarts` extension available. See [here](#retrieving-information)
* `page.order` will have the `initialSubscriptions` extension available, containing the collection

---

---

## Request scoping
**Source:** [products/extensions/subscriptions/guides/request-scoping.md](https://developer.shopware.com/docs/v6.6/products/extensions/subscriptions/guides/request-scoping.md)  
# Request scoping

When you are in a subscription checkout, you are using a separate cart and context. In Storefront, there is an additional URL parameter (`subscriptionToken`) that gets resolved. In headless, there are two header parameters that need to be set namely `sw-subscription-plan` and `sw-subscription-interval`.

Below is an example of the context set on a subscription cart in the Storefront:

```xml
    <route id="frontend.subscription.checkout.cart.page"
           path="/subscription/checkout/cart/{subscriptionToken}"
           methods="GET"
           controller="subscription.storefront.controller.checkout::cartPage">
        <default key="_noStore">true</default>
        <default key="_routeScope"><list><string>storefront</string></list></default>
        <default key="_subscriptionCart">true</default>
        <default key="_subscriptionContext">true</default>
        <default key="_controllerName">checkout</default>
        <default key="_controllerAction">cartpage</default>
        <default key="_templateScopes">subscription</default>
        <option key="seo">false</option>
    </route>
```

And, here is an example of the headers set on a subscription cart using headless:

```bash
curl -XPOST /
    -H 'sw-subscription-plan: planId' /
    -H 'sw-subscription-interval: intervalId' /
    -d 'your body' /
    '/store-api/subscription/{subscriptionId}/activate'
```

These context definitions can be found in `Subscription/Resources/app/config/routes/storefront.xml` or `Subscription/Resources/app/config/routes/store-api.xml`.

---

---

## Separate subscription checkout
**Source:** [products/extensions/subscriptions/guides/separate-checkout.md](https://developer.shopware.com/docs/products/extensions/subscriptions/guides/separate-checkout.md)  
# Separate subscription checkout

This guide describes how buying a subscription via the separate checkout flow works and how extensions should integrate with it.
The **separated subscription checkout** allows customers to purchase subscription products via an isolated checkout process and dedicated cart.
This process is best described as an *express checkout* for subscription products.

Please familiarize yourself with the [concept](../concept.md) first before continuing here.

## Overview

Subscription line items are added to a new subscription cart containing **only** the subscription product.
The checkout process will start right away, and the customer will not be able to add any additional products.
If a customer leaves the subscription checkout, they can only return to it via their browser history or by starting a new checkout with their desired product.
The main cart and the original sales channel context will be left untouched.

## Retrieving information

In a separated subscription checkout a [subscription cart](../concept.md#subscription-cart) and [subscription context](../concept.md#subscription-context) and replaces the main cart and sales channel context.
Additional information about the subscription can be retrieved from the subscription context via it's `subscription` extension.

When an order is placed from a subscription cart, the order will contain an `subscriptionId` / `subscription` extension that references the created subscription as well as an `initialSubscriptions` extension like a [mixed order](./mixed-checkout.md#retrieving-information).
Any subsequent orders generated will only contain the `subscriptionId` / `subscription` extension.

```json
{   // subscription sales channel context
  "token": "<subscription-context-token>",
  "extensions": {
    "subscription": {
      "mainToken": "<main-context-token>",
      "subscriptionToken": "<subscription-context-token>",
      "managed": true,
      "plan": {},     // subscription plan entity
      "interval": {}, // subscription interval entity
    }
  }
}
```

```json
{   // subscription cart
  "token": "<subscription-context-token>",
  "lineItems": [
    { // subscription line item
      "label": "Product A",
      "payload": { // Only since 6.7.4.0
        "subscriptionPlan": "<plan-id>",
        "subscriptionInterval": "<interval-id>",
      }
    }
  ]
}
```

## Manipulate subscription cart

The [subscription cart](../concept.md#subscription-cart) is calculated with the subscription cart calculator.
To add cart collectors or processors to the calculation process, they have to be tagged with `subscription.cart.collector` and `subscription.cart.processor` respectively.
If you need to differentiate between a separate and mixed subscription cart calculation, check `salesChannelContext.extensions.subscription.isManaged`.

The cart processor `Shopware\Commercial\Subscription\Checkout\Cart\Discount\SubscriptionDiscountProcessor` can serve as example how to add line items to subscription carts. But note that the processor supports [mixed carts](./mixed-checkout.md) too.

### Adding subscription line items

To add a line item to a subscription cart, the relevant subscription plan and interval IDs must be added.

The following methods are available to do so via the **Store-API**, remember to use the subscription endpoints including necessary headers:

* Add `subscription-plan-option` and `subscription-plan-option-<subscription-plan-id>-interval` IDs besides `lineItems`.

Information added through the first two methods will be remapped to the line item's payload, as shown in the last method.

To do so via the **backend**, like in cart collectors or processors, the following methods are available:

* Add `lineItem.payload.subscriptionPlan` and `lineItem.payload.subscriptionInterval` IDs to a line items payload

```php
// retrieve plan and interval IDs in subscription collectors and processors 
$subscriptionPlanId = $salesChannelContext->getExtension('subscription')->getPlan()->getId();
$subscriptionIntervalId = $salesChannelContext->getExtension('subscription')->getInterval()->getId();

// generating a composite ID to avoid
// merging into existing line items of the same product
$lineItemId = sprintf('%s-%s-%s', '<product-id>', '<subscription-plan-id>', '<subscription-interval-id>');

$lineItem = new LineItem($lineItemId, LineItem::PRODUCT_LINE_ITEM_TYPE, '<product-id>');
$lineItem->setQuantity(1);
$lineItem->setPayloadValue('subscriptionPlan', $planId);
$lineItem->setPayloadValue('subscriptionInterval', $intervalId);
// ...

$cart->add($lineItem);
```

```html
<form
  id="productDetailPageSubscriptionBuyProductForm"
  action="/checkout/line-item/add"
  method="post"
>
  <input
    type="hidden"
    name="lineItems[<product-id>][id]"
    value="<product-id>"
  >

  <input
    type="radio"
    name="subscription-plan-option"
    value="<subscription-plan-id>"
  >

  <select name="subscription-plan-option-<subscription-plan-id>-interval">
    <option value="<subscription-interval-id>">Weekly interval</option>
    <option value="<subscription-interval-id>">Monthly interval</option>
    <option value="<subscription-interval-id>">Yearly interval</option>
  </select>
</form>
```

Store-API requests need the subscription headers to be set, see [Request scoping](#request-scoping).

The only exception is adding a line item:

```sh
curl -XPOST '/store-api/subscription/checkout/cart/line-item' -d '{
    "lineItems": [{
      "id": <product-id>,
      ...
    }],
    "subscription-plan-option": <subscription-plan-id>,
    "subscription-plan-option-<subscription-plan-id>-interval": <subscription-interval-id>
  }'
```

## Events

Most of the events triggered within subscription checkout are prefixed with `subscription.`.
These events are identical to normal checkout events.
If you wish to use these events, you need to subscribe to them.
A list of known prefixed events can be found in `Subscription/Framework/Event/SubscriptionEventRegistry.php`

```php
// Normal Event Listener
class MyEventSubscriber implements EventSubscriberInterface
{
    public static function getSubscribedEvents(): array
    {
        return [CheckoutOrderPlacedCriteriaEvent::class => 'onOrderPlacedCriteria'];
    }

    public function onOrderPlacedCriteria(CheckoutOrderPlacedCriteriaEvent $event): void
    {
        // Your event handler logic
    }
}

// Subscription Event Listener
class MyEventSubscriber implements EventSubscriberInterface
{
    public static function getSubscribedEvents(): array
    {
        return ['subscription.' . CheckoutOrderPlacedCriteriaEvent::class => 'onOrderPlacedCriteria'];
    }

    public function onOrderPlacedCriteria(CheckoutOrderPlacedCriteriaEvent $event): void
    {
        // Your event handler logic
    }
}
```

## Request scoping

In Storefront, there is an additional URL parameter (`subscriptionToken`) that gets resolved.
In headless, there are two header parameters that need to be set namely `sw-subscription-plan` and `sw-subscription-interval`.

Below is an example of the context set on a subscription cart in the Storefront:

```xml
<route id="frontend.subscription.checkout.cart.page"
        path="/subscription/checkout/cart/{subscriptionToken}"
        methods="GET"
        controller="subscription.storefront.controller.checkout::cartPage">
    <default key="_noStore">true</default>
    <default key="_routeScope"><list><string>storefront</string></list></default>
    <default key="_subscriptionCart">true</default>
    <default key="_subscriptionContext">true</default>
    <default key="_controllerName">checkout</default>
    <default key="_controllerAction">cartpage</default>
    <default key="_templateScopes">subscription</default>
    <option key="seo">false</option>
</route>
```

And, here is an example of the headers set on a subscription cart using headless:

```sh
curl -XPOST '/store-api/subscription/checkout/cart/line-item' /
    -H 'sw-subscription-plan: <subscription-plan-id>' /
    -H 'sw-subscription-interval: <subscription-interval-id>' /
    -d '{
      "lineItems": [{
        "id": <product-id>,
        "subscriptionPlan": <subscription-plan-id>,
        "subscriptionInterval": <subscription-interval-id>
        ...
      }]
    }'
```

These context definitions can be found in `Subscription/Resources/app/config/routes/storefront.xml` or `Subscription/Resources/app/config/routes/store-api.xml`.

## Subscription carts in the Storefront

To change Storefront pages while a customer is a subscription checkout process, the template scope `subscription` must be added to the page's Twig templates and subsequent Twig templates used.
This affects at least the following pages:

* `frontend.checkout.cart.page` / `@Storefront/storefront/page/checkout/cart/index.html.twig`
* `frontend.checkout.confirm.page` / `@Storefront/storefront/page/checkout/confirm/index.html.twig`
* `frontend.checkout.register.page` / `@Storefront/storefront/page/checkout/address/index.html.twig`
* `frontend.account.edit-order.page` / `@Storefront/storefront/page/account/order/index.html.twig`
* `frontend.account.login.page` / `@Storefront/storefront/page/account/register/index.html.twig`
* `frontend.account.register.page` / `@Storefront/storefront/page/account/register/index.html.twig`

Further information can be found in the [dedicated guide here](./template-scoping.md).

---

---

## Template scoping
**Source:** [products/extensions/subscriptions/guides/template-scoping.md](https://developer.shopware.com/docs/v6.6/products/extensions/subscriptions/guides/template-scoping.md)  
# Template scoping

In a subscription context, it's important to ensure that certain template adjustments, which are applicable to the standard storefront, are not automatically applied. This precaution helps in maintaining a clear distinction between the regular checkout process and the subscription checkout process. For instance, elements or buttons that facilitate immediate purchases or third-party payment options, like PayPal Express, should not be visible during the subscription checkout to avoid confusion.

To achieve this separation, templates used within the subscription context should explicitly define their scope. Below is an example of extending a template in the default and subscription context:

```twig
{% sw_extends {
    template: '@Storefront/storefront/base.html.twig',
    scopes: ['default', 'subscription']
} %}
```

---

---

## Guided Shopping Overview
**Source:** [products/guided-shopping.md](https://developer.shopware.com/docs/v6.4/products/guided-shopping.md)  
# Guided Shopping Overview

Guided Shopping is the state-of-the-art new feature that seamlessly integrates into your Shopware system landscape and co-operates with your existing ecommerce infrastructure.

You can create interactive live video events for your customers straight from your Shopware website without having to switch between a presentation tool, video conferencing system, and store system. It is one sophisticated solution to highlight your products, engage your customers and reinforce brand loyalty.

![ ](../../.gitbook/assets/products-guidedShopping.png)

::: warning
Guided Shopping is a commercial extension and is not available as open source.
:::

## Prerequisites

Review the below minimum operating requirements before you install the Guided Shopping feature:

* Instance of [Shopware 6](../../guides/installation/legacy/from-scratch) (version 6.4.18.0 and above).

::: warning
The compliant Node.js version for PWA setup is v14.0.0 to v16.0.0.
:::

* Instance of [Shopware PWA](https://github.com/vuestorefront/shopware-pwa)(version 1.2.0 and above).
* Install and activate [PWA plugin](https://github.com/shopware/SwagShopwarePwa)(version 0.3.3 and above) in Shopware 6 instance.
* Install [Mercure package](https://packagist.org/packages/symfony/mercure#v0.5.3)(version 0.5.3) in Shopware 6 instance.

```bash
# To install Mercure 0.5.3, use the following command
composer require symfony/mercure ^0.5.3
```

* Install Mercure service with the below available options:
  * [Self-hosted installation](./selfHostedMercureInstallation).
  * [Cloud service](https://mercure.rocks/). Refer to the [basic configuration of Mercure hub](./installation#basic-configuration-of-mercure-hub) section.
* An account in [daily.co](http://daily.co/). Refer to the [set up an account](./installation#set-up-an-account) section.

---

---

## Checklist
**Source:** [products/guided-shopping/checklist.md](https://developer.shopware.com/docs/v6.4/products/guided-shopping/checklist.md)  
# Checklist

## Requirements

::: info
💡 This checklist does not cover project specific configurations like cms pages, specific presentations, etc. The only intention of the checklist is to provide a fully working plugin at every step and make it ready to use in terms of administration and end-user experience.
:::

### Shopware fundamentals

* Shopware 6 is available on the web over HTTPS.
* PWA plugin for Shopware 6 is installed.
* Shopware PWA is generated and available as a public URL over HTTPS.

### External services

* [Mercure.rocks](http://Mercure.rocks) service is available on the web over HTTPS with the required settings.
* [Daily.co](http://Daily.co) service is available on the web with default settings.

### Plugin Setup

![ ](../../.gitbook/assets/products-guidedShopping-checklist.png)

* The plugin is installed with no errors and is available in the “Marketing” section.

* The plugin is set up with settings based on the configuration of external services.

### Refresh Shopware PWA

* An instance of Shopware PWA is rebuilt using `yarn build` and redeployed.

Now it is time to set up the presentations and prepare the appointments in order to start using the Guided Shopping.

---

---

## Guided Shopping Installation
**Source:** [products/guided-shopping/installation.md](https://developer.shopware.com/docs/v6.4/products/guided-shopping/installation.md)  
# Guided Shopping Installation

## Install and use the Guided Shopping feature

To install and use the Guided Shopping feature, follow the below steps:

### Get the plugin

1. Clone or download the [guided-shopping repository](https://gitlab.com/shopware/shopware/shopware-6/services/swagguidedshopping).
2. Extract the plugin, including the outer folder `SwagGuidedShopping`, to `platform/custom/plugins` directory of Shopware repository.
3. Make sure the plugin has a PHP package structure containing `composer.json` file, `src/` folder, and so on.
4. Prepare a zip file containing the plugin as in the following structure:

```bash
# SwagGuidedShopping.zip

**SwagGuidedShopping**/
├── bin
├── composer.json
├── composer.lock
├── makefile
├── phpstan.neon
├── phpunit.xml
├── README.md
├── src
└── tests
```

### Install the plugin

You can install the plugin via the admin panel or terminal server.

#### Admin panel

1. Log in to the admin panel.

2. Go to Extensions > My extensions

   ![ ](../../.gitbook/assets/products-guidedShopping-extensionsMenu.png)

3. Click on the “Upload extension” button and choose the zip file containing the plugin from your device.

   ![ ](../../.gitbook/assets/products-guidedShopping-uploadExtension.png)

4. Once it is uploaded and listed, click “Install”.

   ![ ](../../.gitbook/assets/products-guidedShopping-swagExtensionInstall.png)

5. On successful installation, activate the plugin by clicking on the switch button on the left.

#### Terminal server

1. Log in to a server.
2. Zip the plugin and place it in `<shopware-root-dir>/custom/plugins` directory.
3. Extract the zip file from `<shopware-root-dir>/custom/plugins` directory.
4. Run the below Symfony commands:

```bash
# refresh the list of available plugins
bin/console plugin:refresh
# find the plugin **name** (first column on the list). In this case, it is "**SwagGuidedShopping"**
bin/console plugin:install **SwagGuidedShopping** --activate
# clear the cache afterwards
bin/console cache:clear

# Now it is ready to use
```

### Basic configuration of Mercure Hub

Except for the self-hosted service, we recommend using any cloud-based service.

::: info
💡 We tested the service provided by [StackHero](https://www.stackhero.io/en/services/Mercure-Hub/pricing). Depending on the expected traffic, you can easily switch between the plans. For a small demo among a few people at the same time, the “Hobby” plan is sufficient.
:::

Detailed below is the minimum configuration needed for a working stack apart from project specific CMS configurations.

* **Set up CORS allowed origins** - In our case, it would be the domain where the Shopware PWA is hosted and available. For instance: `https://shopware-pwa-gs.herokuapp.com`(frontend).

* **Set up publish allowed origins** - The domains which request the Mercure service must be added to *publish allowed origins* else it gets rejected. For instance (HTTP protocol must not be included): `shopware-pwa-gs.herokuapp.com` (frontend) and `pwa-demo-api.shopware.com`(backend - API).

* **Set up the publisher (JWT) key** - Set whatever you want.

* **Set up the subscriber (JWT) key** - Set whatever you want.

* **Other settings** - Take a look at the below sample Mercure configuration on StackHero (Default settings is recommended).

![ ](../../.gitbook/assets/products-guidedShopping-mercureConfig.png)

### Daily service access

Daily service is responsible for streaming a video between the attendees. It is necessary to have an account to avail its services.

#### Set up an account

1. Go to the [Daily dashboard](https://dashboard.daily.co/).
2. Visit the “developers” section on the left.
3. Get the **API KEY**.

### Configure the plugin

Once the plugin is installed, the services are up and running and have all the required credentials, then the next thing to do is to configure the Guided Shopping plugin itself.

To do so,

1. Navigate to the admin panel where the Guided Shopping plugin is installed.
2. Click the menu and select configure option to configure the below two sections:

   * **Video (daily.co)**

     * You can leave the **API Base URL** as it is `https://api.daily.co/v1/` if not necessary.
     * Insert your **API KEY**.

   ![ ](../../.gitbook/assets/products-guidedShopping-videoConfig.png)

   * **Mercure**

     * Replace *Mercure Hub Url* and *Mercure Hub Public Url* with your domain’s URL where the Mercure service is working and accessible from your stack. For instance, for the URL `https://fcoxpx.stackhero-network.com`, it would be `https://fcoxpx.stackhero-network.com/.well-known/mercure`.
     * Input the secret tokens that were set up in your Mercure service configuration.

   ![ ](../../.gitbook/assets/products-guidedShopping-mercureConfigExample.png)

Daily and Mercure are two external services that are crucial for working with the Guided Shopping plugin.

### Install the plugin into PWA

1. Make sure you have the `guided-shopping` repository.

2. Generate a [PWA project](https://shopware-pwa-docs.vuestorefront.io/)

3. Link the guided-shopping plugin to PWA using the below command:

   ```text
   ln -s <your-path-to-guidedShoppingRepo>/src/Resources/app/pwa <your-path-to-shopware-pwa-repo>/sw-plugins/guided-shopping
   ```

4. Navigate to the folder `pwa` > `sw-plugins` and open `local-plugins.json` file to add `"guided-shopping": true`.

5. Edit `PWA_PATH` in makefile in guided-shopping folder with your current pwa folder path.

6. Install additional dependencies using the below command:

   ```text
   make install-pwa
   ```

7. Update `jest.config.ts` with the following example file:

   ```js
   module.exports = {
     preset: "ts-jest",
     testEnvironment: "jsdom",
     moduleNameMapper: {
       "^@/(.*)$": "<rootDir>/$1",
       "^~/(.*)$": "<rootDir>/$1",
       "^vue$": "vue/dist/vue.common.js",
     },
     verbose: true,
     testMatch: [
       "<rootDir>/sw-plugins/guided-shopping/**/__tests__/**/*.spec.{js,ts}",
     ],
     moduleFileExtensions: ["ts", "tsx", "js", "json"],
     transform: {
       "^.+\\.js$": "babel-jest",
       "^.+\\.ts$": "ts-jest",
       ".*\\.(vue)$": "vue-jest",
     },
     coverageDirectory: "coverage",
     coverageReporters: ["html", "lcov", "text", "cobertura"],
     collectCoverage: true,
     watchPathIgnorePatterns: ["/node_modules/", "/dist/", "/.git/"],
     modulePathIgnorePatterns: [".yalc"],
     roots: [
       "<rootDir>/sw-plugins",
     ],
     coveragePathIgnorePatterns: [
       '/node_modules/',
       '/.nuxt/',
       '/.shopware-pwa/'
     ],
     transformIgnorePatterns: [
       "/node_modules/(?!@shopware-pwa)"
     ],
     collectCoverageFrom: [
       "sw-plugins/guided-shopping/logic/**/*.{js,ts}",
     ],
   }
   ```

8. Open `tsconfig.json` file to add `@types/jest` into `compilerOptions.types` array and save it.

### Rebuild Shopware PWA

In order to synchronize the installed `SwagGuidedShopping` plugin in the backend, the Shopware PWA must be rebuilt (recompiled) after the plugins are downloaded. Follow the below steps:

1. Check credentials in the `.env` file (ADMIN\_USER and ADMIN\_PASSWORD).

::: info
💡 Alternatively, you can invoke the `plugins` command manually using:
`npx @shopware-pwa/cli@canary plugins --user YOUR_ADMIN_USERNAME --password=YOUR_SECRET_PASS`
Now, the application is ready for the rebuild process.

```
Note that the admin credentials are required to connect to the installed plugin library through an Admin API.
```

:::

1. Run the build command.

   ```bash
   # being in the root directory of your Shopware PWA project:
   yarn build
   # under the hood, plugins synchronization will be processed at the same time
   ```

2. Re-deploy Shopware PWA.

With this, the PWA will contain the Guided Shopping plugin and be ready to use.

Now let us rehearse the steps before deployment by going through the [Checklist](./checklist).

---

---

## Sample Mercure Configuration on StackHero
**Source:** [products/guided-shopping/sampleMercureConfig.md](https://developer.shopware.com/docs/v6.4/products/guided-shopping/sampleMercureConfig.md)  
# Sample Mercure Configuration on StackHero

![Mercure configuration](../../.gitbook/assets/products-guidedShopping-mercureConfig.png)

---

---

## Self-hosted Mercure Installation for Guided Shopping
**Source:** [products/guided-shopping/selfHostedMercureInstallation.md](https://developer.shopware.com/docs/v6.4/products/guided-shopping/selfHostedMercureInstallation.md)  
# Self-hosted Mercure Installation for Guided Shopping

## Mercure general settings

| Name | Variable | Description |
| ---- | -------- | ----------- |
| Publisher JWT Key  | publisher\_jwt      | The JWT key used for authenticating publishers |
| Subscriber JWT Key | subscriber\_jwt     | The JWT key used for authenticating subscribers|
| CORS Origin        | cors\_origins       | List of domains allowed to connect to the Mercure hub as value of the cors\_origins. For other cases, check [troubleshoot cors errors](https://mercure.rocks/docs/hub/troubleshooting#cors-issues) |
| UI                 | ui                 | Enable the UI and expose the demo |
| Demo               | demo               | Enable the UI but do not expose the demo |
| Anonymous          | anonymous          | Allow subscribers with no valid JWT to connect |

## Mercure installation

There are two recommended ways of Mercure installations:

### 1. Docker

If you host Mercure yourself, the easiest way is to do it via docker. The image can be found at [dunglas/mercure](https://hub.docker.com/r/dunglas/mercure).

#### Configure Mercure docker

The docker image allows you to use the following *env* variables to configure Mercure.

::: warning
Use different publisher and subscriber keys for security reasons.
:::

```txt
- MERCURE_PUBLISHER_JWT_KEY: your-256-bit-publisher-key
- MERCURE_SUBSCRIBER_JWT_KEY: your-256-bit-subscriber-key
- MERCURE_EXTRA_DIRECTIVES: |-  
   cors_origins "https://my-pwa-shop.com https://en.my-pwa-shop.com"  
   anonymous 0  
   ui 1
```

You can also configure it like the self-installed version via the Caddyfile.

```txt
// Sample Caddyfile
{
    # Debug mode (disable it in production!)
    debug
    # HTTP/3 support
}
:80
log
route {
    redir / /.well-known/mercure/ui/
    encode gzip
    mercure {
        # Enable the demo endpoint (disable it in production!)
        demo
        # Publisher JWT key
        publisher_jwt MySecret
        # Subscriber JWT key
        subscriber_jwt MySecret
        # CORS
        cors_origins http://localhost:3000 http://localhost:8080 http://shopware.test http://7779-91-90-160-158.ngrok.io
        publish_origins localhost:3000 localhost:8080 shopware.test 7779-91-90-160-158.ngrok.io
        # Allow anonymous subscribers (double-check that it's what you want)
        anonymous
        # Enable the subscription API (double-check that it's what you want)
        subscriptions
    }
    respond "Not Found" 404
}
```

### 2. Self-installation

The [installation guide](https://mercure.rocks/docs/hub/install) explains all steps that are required for installing the Mercure.

#### Production configuration

```txt
mercure {
...  
publisher_jwt my-publisher-key HS256  
subscriber_jwt my-subscriber-key HS256  
cors_origins "https://my-pwa-shop.com https://en.my-pwa-shop.com"  
demo 0  
ui 0  
...
}
```

---

---

## Introduction to PaaS
**Source:** [products/paas.md](https://developer.shopware.com/docs/v6.6/products/paas.md)  
# Introduction to PaaS

While both [Shopware PaaS Native](./shopware) and [Shopware PaaS](./shopware-paas) offer cloud-based environments for development, they differ in specialization and flexibility:

* **Shopware PaaS**: A generic PaaS provider, [Shopware PaaS](./shopware-paas) supports various applications and multiple cloud providers, giving developers the flexibility to define their infrastructure as code. However, this requires customers to manage more aspects of infrastructure and setup.

* **Shopware PaaS Native**: Optimized solely for Shopware, this platform provides a tightly integrated and controlled environment on AWS. This focus ensures higher stability, with Shopware managing all underlying configurations, enabling developers to concentrate on application development.

By using [Shopware PaaS Native](./shopware), teams benefit from a unified, robust platform that simplifies the development lifecycle, enhances performance, and enables faster innovation.

---

---

## Build and Deploy
**Source:** [products/paas/build-deploy.md](https://developer.shopware.com/docs/v6.5/products/paas/build-deploy.md)  
# Build and Deploy

Now that we have set up the repository, we are ready to push changes to your PaaS environment.

The key concept is that your PaaS project is a git repository. Every time you push to that repository, a new version of your store will be created from the source code and deployed. Different environments (e.g., dev-previews, staging, and production) are mapped by corresponding branches.

## Push main branch

To push your latest changes, run the following commands from your terminal:

```bash{3}
git add .
git commit -m "Applied new configuration"
git push -u shopware main
```

First, we stage all changes and then add them as a new commit. Then, we push them to our `shopware` origin (remember, the one for our PaaS environment) on the `main` branch.

This will trigger a new build with a subsequent deploy consisting of the following steps:

| Build | Deploy |
| --- | --- |
| Configuration validation | Hold app requests |
| Build container image | Unmount live containers |
| Installing dependencies | Mount file systems |
| Run [build hook](./setup-template#build-hook) | Run [deploy hook](./setup-template#deploy-hook) |
| Building app image | Serve requests |

After both steps have been executed successfully (you will get extensive logging about the process), you will be able to see the deployed store on a link presented at the end of the deployment.

## First deployment

The first time the site is deployed, Shopware's command line installer will run and initialize Shopware. It will not run again unless the `install.lock` file is removed. **Do not remove that file unless you want the installer to run on the next deploy.**

The installer will create an administrator account with the default credentials.

| username | password |
|---|---|
| `admin` | `shopware` |

Make sure to change this password immediately in your Administration account settings. Not doing so is a security risk.

### Manual steps

After the first deploy, some steps must be done manually before the environment is entirely up and running.

#### JWT keys

The JWT keys, used for the Administration authentication, need to be generated for your project. The keys will be stored securely in the Shopware Paas environment variable storage and should not be committed to the Git repository or be available on the file system.

To generate the keys and add them to the storage, run the following command:

```bash
shopware ssh --app=app "bin/console system:generate-jwt-secret --use-env" |\
grep -E "^JWT_(PUBLIC|PRIVATE)_KEY=" |\
while read line ; do \
shopware variable:create --sensitive 1 --level project --name env:$(echo $line | cut -d "=" -f 1) --value $(echo $line | cut -d "=" -f 2-); \
done
```

Run this command from your project directory so the `shopware` command knows which project to update.

The command connects to the application server to generate the JWT keys. It then sets the `JWT_PUBLIC_KEY` and `JWT_PRIVATE_KEY` as private environment variables.

Finally, execute the `shopware redeploy` command to proceed with the build-and-deploy process.

##### Shopware config

By default, Shopware looks for the JWT keys on the file system. The configuration must be updated to use the keys in the environment variables.

If you use the Shopware Flex Paas template, [the configuration](https://github.com/shopware/recipes/blob/main/shopware/paas-meta/6.4/config/packages/paas.yaml) will be applied automatically.

```yaml
 shopware:
   api:
     jwt_key:
       private_key_path: '%env(base64:JWT_PRIVATE_KEY)%'
       public_key_path: '%env(base64:JWT_PUBLIC_KEY)%'  
```

#### Theme assets

It is a known issue that after the first deployment, theme assets are not compiled during the deployment. For that reason, your store will look unstyled. The [Theme Build](./theme-build) section explains how to resolve that issue.

## Composer authentication

You must authenticate yourself to install extensions from the Shopware store via composer. In your local development environment, this is possible by creating an `auth.json` file that contains your auth token. However, this file shouldn't be committed to the repository.

The following command adds your authentication token to the secure environment variable storage of Shopware Paas. This variable (contains the content which would otherwise be in `auth.json`) will be available during the build step and be automatically picked up by the composer.

```bash
shopware variable:create --level project --name env:COMPOSER_AUTH --json true --visible-runtime false --sensitive true --visible-build true --value '{"bearer": {"packages.shopware.com": "%place your key here%"}}'
```

Make sure to replace `%place your key here%` with your actual token. You can find your token by clicking 'Install with Composer' in your Shopware Account.

## Extending Shopware - plugins and apps

The PaaS recipe uses the [Composer plugin loader](../../guides/hosting/installation-updates/cluster-setup#composer-plugin-loader).

## Manually trigger rebuilds

Sometimes, you might want to trigger a rebuild and deploy of your environment without pushing new code to your project. To do this for your main environment, create a `REBUILD_DATE` environment variable. This triggers a build right away to propagate the variable.

```bash
shopware variable:create --environment main --level environment --prefix env --name REBUILD_DATE --value "$(date)" --visible-build true
```

To force a rebuild at any time, update the variable with a new value:

```bash
shopware variable:update --environment main --value "$(date)" "env:REBUILD_DATE"
```

This forces your application to be built even if no code has changed.

---

---

## CLI Setup
**Source:** [products/paas/cli-setup.md](https://developer.shopware.com/docs/v6.5/products/paas/cli-setup.md)  
# CLI Setup

The CLI is your tool to connect with your PaaS environment, push changes, trigger deployments, etc.

## Download and install

To install PaaS CLI, run the following command:

```sh
curl -sfS https://cli.shopware.com/installer | php
```

When you run the CLI for the first time, it will ask you to log in via your browser.

You can also generate an SSH key manually and add it in the **My profile > SSH Keys** section of your [PaaS Console](https://console.shopware.com/).

::: info
**Set up SSH keys**

If you are unsure of how to create SSH keys, please follow [this tutorial](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent) provided by GitHub.
:::

## Authenticate

Next, you need to authenticate your CLI. This can be done through your browser. Just run the following command and follow the instructions:

```sh
shopware
```

---

---

## Elasticsearch
**Source:** [products/paas/elasticsearch.md](https://developer.shopware.com/docs/v6.5/products/paas/elasticsearch.md)  
# Elasticsearch

Perform the following steps to activate Elasticsearch in your environment.

## Enable service

Add (or uncomment) the Elasticsearch service configuration.

```yaml
// .platform/services.yaml
elasticsearch:
   type: opensearch:1.2
   disk: 256
```

## Add relationship

Add (or uncomment) the relationship for the app configuration.

```yaml
// .platform.app.yaml
relationships:
    elasticsearch: "elasticsearch:opensearch"
```

## Configure instance

Follow the setup and indexing steps to prepare your instance as described in the [setup Elasticsearch](../../guides/hosting/infrastructure/elasticsearch/elasticsearch-setup#prepare-shopware-for-elasticsearch).

After that, the following environment variables are provided by the Composer package \`shopware/paas-meta:

* `SHOPWARE_ES_HOSTS`

## Enable Elasticsearch

Ultimately, activate Elasticsearch by setting the environment variable `SHOPWARE_ES_ENABLED` to `1`. You can either do that by uncommenting the corresponding line in `platformsh-env.php` or setting it in the [variables](./setup-template#variables) section of the app configuration.

---

---

## Fastly
**Source:** [products/paas/fastly.md](https://developer.shopware.com/docs/v6.5/products/paas/fastly.md)  
# Fastly

Fastly allows Shopware to store the HTTP Cache at the nearest edge server to the end customer. This saves a lot of resources as the cached responses don't reach the actual application, and it decreases the response time drastically worldwide. Another benefit is that the Redis cache is not used anymore and will have less cache items.

## Setup

::: info
Fastly is supported in Shopware versions 6.4.11 or newer.
:::

1. Make sure `FASTLY_API_TOKEN` and `FASTLY_SERVICE_ID` are set in the environment or contact the support when they are missing.
2. Install the Fastly Composer package using `composer req fastly`.
3. Disable caching in the `.platform/routes.yaml`.
4. Push the new config and Fastly gets enabled.

---

---

## RabbitMQ
**Source:** [products/paas/rabbitmq.md](https://developer.shopware.com/docs/v6.5/products/paas/rabbitmq.md)  
# RabbitMQ

RabbitMQ is enabled by default in the template. This service is optional but recommended. It can be disabled and replaced by an SQL-backed queue.

## Disable service

Comment out the RabbitMQ service configuration.

```yaml
// .platform/services.yaml
#rabbitmq:
#   type: rabbitmq:3.8
#   disk: 1024
```

## Remove relationship

Comment out the relationship for the app configuration.

```yaml
// .platform.app.yaml
#relationships:
#   rabbitmqqueue: "rabbitmq:rabbitmq"
```

## Push changes

Push the changes to your git repository and wait for the deployment to finish.

---

---

## Repository
**Source:** [products/paas/repository.md](https://developer.shopware.com/docs/v6.5/products/paas/repository.md)  
# Repository

The source code of your project will reside in a git-based VCS repository. You can start with a plain project. However, we suggest starting with a new Composer create-project. You will learn more about the setup template in the [Setup Template](setup-template) section.

::: info
This guide explains the repository setup using **GitHub**. You can also integrate Bitbucket or GitLab-based version control environments with Shopware PaaS. Refer to [Source Integrations](https://docs.platform.sh/integrations/source.html) for more information.
:::

## Create a Shopware project

Firstly, create a new project with `composer create-project shopware/production <folder-name>` using the [Symfony Flex](../../guides/installation/template.md) template.

This will create a brand new Shopware 6 project in the given folder. Now, change it into the newly created project and require the PaaS configuration with `composer req paas`.

Secondly, create a new Git repository and push it to your favourite Git hosting service.

### Updating the PaaS template recipe

You can update the recipe to the latest version using the `composer recipes:update` [command](https://symfony.com/blog/fast-smart-flex-recipe-upgrades-with-recipes-update).

However, the template may receive breaking changes. For example, when making certain changes to file mounts (like using a "service mount" instead of a "local mount"), there is no way to migrate your existing data into the updated mount automatically. Due to this, we always recommend manually checking all changes in the `recipes:update` command provided for the PaaS package, as some updates to the `.platform-yaml` files might need extra manual actions. Every PaaS recipe update should be deemed a **breaking** update and thus be validated before applying it to your project.

## Add PaaS remote

Lastly, add a second remote, which allows us to push code towards the PaaS environment and trigger a deployment.

We first need the project ID, so we display all projects using

```bash{7}
$ shopware projects

Your projects are:
+---------------+-----------+------------------+--------------+
| ID            | Title     | Region           | Organization |
+---------------+-----------+------------------+--------------+
| 7xasjkyld189e | paas-env  | <region-domain>  | shopware     |
+---------------+-----------+------------------+--------------+

Get a project by running: platform get [id]
List a projects environments by running: platform environments -p [id]
```

To add the project remote to your local repository, just run

```bash
shopware project:set-remote 7xasjkyld189e # Replace with your project ID
```

## Conclusion

Now your repository is configured - you should have two remotes

```sh
$ git remote -v

origin	git@github.com:<project-repository>.git (fetch)
origin	git@github.com:<project-repository>.git (push)
shopware	<paas-url>.git (fetch)
shopware	<paas-url>.git (push)
```

| Remote     | Function          | Description                                                             |
|------------|-------------------|-------------------------------------------------------------------------|
| `origin`   | Project Code      | This remote contains all your project specific source code              |
| `shopware` | PaaS Environment  | Changes pushed to this remote will be synced with your PaaS environment |

## Migrating from the old template to the new template

If you have already used the [Shopware PaaS old template](https://github.com/shopware/paas), please follow the guide to [migrate it to the new structure](../../guides/installation/template#how-to-migrate-from-production-template-to-symfony-flex).

The following tasks have to be done additionally to the flex migration:

* The root `.platform.app.yml` has been moved to `.platform/applications.yaml`
* The following services has been renamed:
  * `queuerabbit` to `rabbitmq`
  * `searchelastic` to `opensearch`

As the services are renamed, a completely new service will be created. Here are three possible options available:

* Rename the services back again
* Start with a new service and re-index Elasticsearch
* [Perform the transitional upgrade of two services in parallel for some time](https://docs.platform.sh/add-services/opensearch.html#upgrading)

---

---

## Setup Template
**Source:** [products/paas/setup-template.md](https://developer.shopware.com/docs/v6.5/products/paas/setup-template.md)  
# Setup Template

The setup template is installed automatically using Symfony Flex when requiring the `paas` package as described in the [Repository](repository). It contains build and deployment logic for Shopware PaaS as well as configuration for the underlying infrastructure and services. In this chapter, we will have a look at these customizations.

Below is an overview of the files and directories added by the PaaS meta-package:

```text
./
├─ .platform/
│  ├─ applications.yaml
│  ├─ routes.yaml
│  ├─ services.yaml
├─ bin/
│  ├─ prestart_cacheclear.sh
├─ config/
│  ├─ packages/
│  │  ├─ paas.yaml
├─ files/
│  ├─ theme-config/
```

## [.platform/applications.yaml](https://github.com/shopware/recipes/blob/main/shopware/paas-meta/6.4/.platform/applications.yaml)

This file contains Shopware PaaS specific configuration and can be customized as needed for your individual project.

### name

It is the name of your app. It is used in commands like:

```bash
shopware ssh -A app 'bin/console theme:dump'
```

Unless there is a specific need for it, leave it as `app`.

### type

This section contains the base image used for your build process. This is also where you configure the PHP version used in your PaaS environment.

### variables

This section contains configuration for environment variables or server settings. General store settings and configurations are set here. Here you can inject custom environment variables or enable feature flags.

Variables in the `env` section are automatically injected as environment variables. If a variable is also set in your .env file, the variables set in the `applications.yaml` file will overwrite these.

### hooks

Lifecycle hooks are custom scripts that are called during your build and deploy processes. See more on the [deployment process](./build-deploy#push-main-branch).

#### build hook

This script is called during the build process and builds your application's assets (composer dependencies, javascript- and css- assets of Shopware core and extensions) and disables the UI installer. You can customize this script if you need. During the execution, you may perform write operations on the file system, which are prohibited in the proceeding steps unless the corresponding directory is [mounted](#mounts).

You do not have access to any of the services (like the database or Redis) configured, as the application is not running yet. You should ensure to perform as much of your entire building procedure during the build step, as web traffic is blocked during the execution of the deploy step.

#### deploy hook

::: warning
The environment will be cut off from web traffic during the execution of the deploy hook. The shorter this script is, the shorter the downtime will be.
:::

This script is called during the deployment process. Theme configuration is copied, the install scripts are executed and secrets are generated.

* Copy theme configuration
* Run database migrations
* Set sales channel domains for non-production environments
* Clear cache

If this is the first deployment, the following operations are performed:

* Setup script is executed
* Theme is set
* Secrets are generated
* `install.lock` file is created

You can also customize this script, however, make sure to keep operations to a minimum, as your store will not be exposed to web traffic during the execution. Connections made during the meantime will be queued in a suspended state and not necessarily fail but will take longer than usual (i.e., until the deployment has finished).

#### post\_deploy

Analogous to the two preceding hooks, the post\_deploy hook provides an entry point for custom scripts. However, this hook is executed after the application container accepts connections.

### relationships

This section defines the mapping between services created in the [services.yaml](https://github.com/shopware/recipes/blob/main/shopware/paas-meta/6.4/.platform/services.yaml) and the application itself.

### mounts

By default, the entire storage of your application is read-only. Mounts define directories that are writable after the build is complete. They aren’t available during the build.

Every mount has one of two types: `local` or `service`.
A local mount is unique to the service that is accessing it. For example `/var/cache` is a good local mount because the Symfony cache should not be shared between different app servers.
A service mount references to another service (of the type `network-storage`). These mounts are shared between other services and between the different app servers. For example the `/public/media` folder is a good shared mount because the [workers](#workers) that consume the Messenger queue should be able to read and write to the media directory.

### web

The public root of your application `public/index.php` is configured so the server knows where to route dynamic requests.

### workers

Workers are copies of your application instance after the [build hook](#build-hook) has been executed. They are usually configured with a start command. By default, there are two configured workers - one for message queues and one for scheduled tasks.

## [.platform / routes.yaml](https://github.com/shopware/recipes/blob/main/shopware/paas-meta/6.4/.platform/routes.yaml)

This file configures incoming HTTP requests routed to the `app` instance.

## [.platform / services.yaml](https://github.com/shopware/recipes/blob/main/shopware/paas-meta/6.4/.platform/services.yaml)

This file contains services that are used by the `app` instances. Depending on your setup, uncomment or add services that you need, and they will be created and scaled automatically.

In our template there are 4 different services enabled by default:

* `db`
* `cacheredis`
* `rabbitmq`
* `fileshare`

## [files / theme-config](https://github.com/shopware/recipes/tree/main/shopware/paas-meta/6.4/files/theme-config)

We suggest checking in your theme configuration to version control in this directory. Read more on the concept of [builds without database](../../guides/hosting/installation-updates/deployments/build-w-o-db) as described in [Theme Build](./theme-build).

---

---

## Shopware PaaS
**Source:** [products/paas/shopware-paas.md](https://developer.shopware.com/docs/v6.6/products/paas/shopware-paas.md)  
# Shopware PaaS

::: info
Shopware PaaS is available at request for Shopware merchants. Please approach the [Shopware Sales](https://www.shopware.com/en/#contact-sales) to get more information on Shopware PaaS
:::

Shopware PaaS is a platform-as-a-service to host, deploy and scale for your individual Shopware project.
It comes with full flexibility and code ownership of a self-hosted Shopware project, but takes away the complexity of building custom infrastructure, build and testing pipelines, or deployment automation.

Get started by installing the PaaS CLI on your local development machine.

## Getting started with Shopware PaaS - How to deploy your first project

::: info
Prerequisites:

* Having a Shopware PaaS account (Select Register now on the authentication form when accessing <https://console.shopware.com>)
* Having the project\_id of an empty project created on Shopware PaaS
* Having the Shopware PaaS CLI installed, see <https://developer.shopware.com/docs/products/paas/cli-setup.html>
* Having PHP ext-amqp installed (PaaS uses RabbitMQ instead of the regular DB to manage messages)
  :::

Steps:

1.) Create a local Shopware project on your laptop

```sh
composer create-project shopware/production demo --no-interaction --ignore-platform-reqs
```

2.) Enter the folder newly created

```sh
cd /demo
```

3.) Install the PaaS composer package

```sh
composer req paas
```

4.) Initialize your local Git repository

```sh
git init
```

5.) Add all the existing files to Git

```sh
git add .
```

6.) Create your first commit

```sh
git commit -am "initial commit"
```

7.) Configure the PaaS CLI with your project\_id

```sh
shopware project:set-remote PROJECT_ID
```

Where PROJECT\_ID is the project\_id of your empty project.

8.) Push the code to Shopware PaaS

```sh
git push shopware
```

## Step-by-step guide

The sub-pages describe a more detailed step-by-step guide that you can follow to set up your PaaS project.

First, make sure your [PaaS CLI is set up correctly](cli-setup).
Once your PaaS CLI is up and running, it is time to [set up your project repository](repository).

When your repository is set up correctly, you are ready to [push and deploy your project](build-deploy) to the PaaS environment.

You can look into setting up [Elasticsearch](elasticsearch), [RabbitMQ](rabbitmq) and/or [Fastly](fastly) to further enhance the performance of your PaaS project.

Finally, do not forget each PaaS project comes with [Blackfire](blackfire) which will help you to monitor the response time and investigate performance issues of your project.

---

---

## Blackfire Continuous Observability Solution
**Source:** [products/paas/shopware-paas/blackfire.md](https://developer.shopware.com/docs/v6.6/products/paas/shopware-paas/blackfire.md)  
# Blackfire Continuous Observability Solution

Blackfire is bundled with every Enterprise Shopware PaaS project without any additional fees.\
All the people invited to the project can access Blackfire, and all environments can be monitored.

The APM will show you when, where, and why performance issues happen.

Here are the main Blackfire features:

* Monitoring (Live metrics from your app): identify slow transactions, background jobs, services or third-party calls
* Deterministic Profiling (Deep, runtime code analysis): get function-call level metrics and spot root causes of bottlenecks
* Continuous Profiling (Combines profiling and monitoring with minimal overhead): easily identify hotspots, optimize resource usage, and compare timeframes to visually identify the flaky parts of your application
* Testing (Performance budget control): verify code behavior and performance
* Alerting (Warnings upon abnormal behaviors)
* Recommendations (Actionable insights and expert advice): benefit from unique, cutting-edge issue detection with documented resolution recommendations
* CI/CD integration (Automated testing and regression prevention): add Blackfire to any testing pipeline and existing tests, or start from scratch with our Open-Source crawler, tester, and scraper

## Access

You'll find the link to access Blackfire on the Shopware PaaS Console at the environment level.
Once you click on the link, you'll be redirected to the Platform.sh authentication portal.

If this is your first authentication, please use your usual Shopware PaaS email and follow the "reset password" workflow so you can set your Platform.sh password.

## Onboarding Guide

We encourage you to look at our [self-onboarding guide](https://docs.blackfire.io/onboarding/index). It includes extensive documentation and videos to help use and understand Blackfire.

## Deterministic Profiling

We recommend you install the [Firefox Blackfire extension](https://addons.mozilla.org/en-US/firefox/addon/blackfire/) or the [Chrome Blackfire extension](https://chromewebstore.google.com/detail/blackfire-profiler/miefikpgahefdbcgoiicnmpbeeomffld?hl=en) so you can trigger profiles of targeted transactions or group of transactions.

![Blackfire profile](../../../assets/blackfire-profile.png)

---

---

## Build and Deploy
**Source:** [products/paas/shopware-paas/build-deploy.md](https://developer.shopware.com/docs/v6.6/products/paas/shopware-paas/build-deploy.md)  
# Build and Deploy

Now that we have set up the repository, we are ready to push changes to your PaaS environment.

The key concept is that your PaaS project is a git repository. Every time you push to that repository, a new version of your store will be created from the source code and deployed. Different environments (e.g., dev-previews, staging, and production) are mapped by corresponding branches.

## Push main branch

To push your latest changes, run the following commands from your terminal:

```bash{3}
git add .
git commit -m "Applied new configuration"
git push -u shopware main
```

First, we stage all changes and then add them as a new commit. Then, we push them to our `shopware` origin (remember, the one for our PaaS environment) on the `main` branch.

This will trigger a new build with a subsequent deploy consisting of the following steps:

| Build                                         | Deploy                                          |
|-----------------------------------------------|-------------------------------------------------|
| Configuration validation                      | Hold app requests                               |
| Build container image                         | Unmount live containers                         |
| Installing dependencies                       | Mount file systems                              |
| Run [build hook](./setup-template#build-hook) | Run [deploy hook](./setup-template#deploy-hook) |
| Building app image                            | Serve requests                                  |

After both steps have been executed successfully (you will get extensive logging about the process), you will be able to see the deployed store on a link presented at the end of the deployment.

## First deployment

The first time the site is deployed, Shopware's command line installer will run and initialize Shopware. It will not run again unless the `install.lock` file is removed. **Do not remove that file unless you want the installer to run on the next deploy.**

The installer will create an administrator account with the default credentials.

| username | password   |
|----------|------------|
| `admin`  | `shopware` |

Make sure to change this password immediately in your Administration account settings. Not doing so is a security risk.

## Composer authentication

You must authenticate yourself to install extensions from the Shopware store via composer. In your local development environment, this is possible by creating an `auth.json` file that contains your auth token. However, this file shouldn't be committed to the repository.

The following command adds your authentication token to the secure environment variable storage of Shopware Paas. This variable (contains the content which would otherwise be in `auth.json`) will be available during the build step and be automatically picked up by the composer.

```bash
shopware variable:create --level project --name env:COMPOSER_AUTH --json true --visible-runtime false --sensitive true --visible-build true --value '{"bearer": {"packages.shopware.com": "%place your key here%"}}'
```

Make sure to replace `%place your key here%` with your actual token. You can find your token by clicking 'Install with Composer' in your Shopware Account.

## Extending Shopware - plugins and apps

The PaaS recipe uses the [Composer plugin loader](../../../guides/hosting/installation-updates/cluster-setup#composer-plugin-loader).

## Manually trigger rebuilds

Sometimes, you might want to trigger a rebuild and deploy of your environment without pushing new code to your project. To do this for your main environment, create a `REBUILD_DATE` environment variable. This triggers a build right away to propagate the variable.

```bash
shopware variable:create --environment main --level environment --prefix env --name REBUILD_DATE --value "$(date)" --visible-build true
```

To force a rebuild at any time, update the variable with a new value:

```bash
shopware variable:update --environment main --value "$(date)" "env:REBUILD_DATE"
```

This forces your application to be built even if no code has changed.

---

---

## PaaS CLI Setup
**Source:** [products/paas/shopware-paas/cli-setup.md](https://developer.shopware.com/docs/v6.6/products/paas/shopware-paas/cli-setup.md)  
# PaaS CLI Setup

The PaaS CLI is your tool to connect with your PaaS environment, push changes, trigger deployments, etc.

## Download and install

To install PaaS CLI, run the following command:

```sh
curl -sfS https://cli.shopware.com/installer | php
```

When you run the PaaS CLI for the first time, it will ask you to log in via your browser.

You can also generate an SSH key manually and add it in the **My profile > SSH Keys** section of your [PaaS Console](https://console.shopware.com/).

::: info
**Set up SSH keys**

If you are unsure of how to create SSH keys, please follow [this tutorial](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent) provided by GitHub.
:::

## Authenticate

Next, you need to authenticate your PaaS CLI. This can be done through your browser. Just run the following command and follow the instructions:

```sh
shopware
```

---

---

## Blackfire Continuous Profiling of Nuxt.js
**Source:** [products/paas/shopware-paas/composable-frontends/blackfire.md](https://developer.shopware.com/docs/products/paas/shopware-paas/composable-frontends/blackfire.md)  
# Blackfire Continuous Profiling of Nuxt.js

It's possible to enable [Blackfire Continuous Profiling](https://www.blackfire.io/continuous-profiler/) on a frontend based on Nuxt.js.

1. Install the Blackfire Node.js Lib: `npm install @blackfireio/node-tracing`
2. Add the environment variable `BLACKFIRE_ENABLE=1`
3. Add `./server/plugins/blackfire.ts`:

```ts
// server/plugins/blackfire.ts
export default defineNitroPlugin(async () => {
  if (process.env.BLACKFIRE_ENABLE !== '1') return;

  try {
    // Works in ESM: dynamically import and handle both default/named exports
    const mod = await import('@blackfireio/node-tracing');
    const Blackfire: any = (mod as any).default || mod;

    Blackfire.start({
      appName:
        process.env.BLACKFIRE_APP_NAME || 'shopware-frontend',
      // durationMillis: 45000,
      // cpuProfileRate: 100,
      // labels: { service: 'frontend', framework: 'nuxt3' },
    });

    console.info('[blackfire] node-tracing started');
  } catch (e) {
    console.error('[blackfire] failed to start node-tracing', e);
  }
});
```

---

---

## Composable-Frontends Performance
**Source:** [products/paas/shopware-paas/composable-frontends/performance.md](https://developer.shopware.com/docs/products/paas/shopware-paas/composable-frontends/performance.md)  
# Composable-Frontends Performance

## Shopware Backend caching

The current versions of Shopware rely heavily on `POST` requests for `/store-api/`.\
`POST` requests are by design not cacheable, so Fastly simply passes them to the backend cluster without even trying to cache them.

A temporary [plugin](https://github.com/shopwareLabs/SwagStoreApiCache) has been developed.  With this workaround, Fastly can cache some of the `/store-api/` `POST` requests.

This plugin includes new Fastly snippets that must be used instead of the usual ones.

The plugin includes [a few routes](https://github.com/shopwareLabs/SwagStoreApiCache/blob/trunk/src/Listener/StoreAPIResponseListener.php#L57) which will become automatically cacheable.

If you need to cache additional routes, it can be done via the admin config: `SwagStoreAPICache.config.additionalCacheableRoutes`.

As usual, ensure [soft-purges](https://developer.shopware.com/docs/guides/hosting/infrastructure/reverse-http-cache.html#fastly-soft-purge) are enabled.

Please note that we're actively working on moving the `store-api` requests from `POST` to `GET` to make them cacheable, so the use of this plugin would no longer be required.\
More details in the [Epic](https://github.com/shopware/shopware/issues/7783).

## Composable Frontend caching

To get the best performance, Frontend caching must be enabled.

There are a few steps to get there:

1. Configure a Fastly service on top of each Frontend. It can be one Fastly service per Frontend, or it can be a single Fastly service with multiple domains and hosts configured.

2. Update `nuxt.config.ts` so `routesRules`, using Incremental Static Regeneration (`ISR`), have the required cache headers.
   Example:

```ts
'/': {
      		isr: 60 * 60 * 24,
      		headers: {
        		'cache-control': 'public, s-maxage=3600, stale-while-revalidate=1800'
      		}
    	},
'/**': {
      		isr: 60 * 60 * 24,
      		headers: {
        		'cache-control': 'public, s-maxage=3600, stale-while-revalidate=1800'
      		}
    	},
```

`s-maxage` and `stale-while-revalidate` can be adjusted.\
`s-maxage` represents how long in seconds the content will be cached on Fastly.\
`stale-while-revalidate` represents how long a stale page (aka an expired page) can be kept and served, so when a client requests this page, the stale object is served while a request to update it is done in the background, so the next client will have an updated version of the page.

::: Note

The cache invalidation process is only on the Fastly Backend service.
The Shopware instance is not "aware" of the Frontend instance. It cannot trigger cache invalidation. Items will remain in cache for the `s-maxage` duration.

:::

## Get rid of the OPTIONS requests (CORS)

When using a different domain for backend requests, browsers are forced to send `OPTIONS` requests. Those requests, also named `preflight` requests, are due to `CORS` checks. Every time the browser needs to send a request to the backend, it must first confirm it's authorized to do so.

`OPTIONS` requests are by default not cacheable as the responses may vary depending on the request's headers.
There is a possibility to include an `Access-Control-Max-Age` header in the `OPTIONS` responses, so it forces the browser to cache the answer for a longer period than the default 5 seconds.

But the recommended action is to remove those `CORS` checks completely.
To do so, all the requests to the Shopware backend must be sent on the same domain as the Frontend, so the browser only sees one single domain.

For this, the Frontend Fastly service can be configured to serve both the Frontend and the Backend requests.

The config is pretty simple. With the additional host, the logic is only four lines of code:

```vcl
if (req.url.path ~ "^/store-api/") { 
  set req.http.host = "backend.mydomain.com"; 
  set req.backend = F_Backend__Shopware_instance_; 
  return (pass);
}
```

The `return (pass)` is very important. We must not add a cache layer on the Frontend Fastly service to avoid invalidation issues. The Backend Fastly service remains the one responsible for caching.

## Optimize the Fastly Backend hit-ratio

Once an item has been set into the cart, a new cookie named `sw-cache-hash` is sent.
The default VCL hash snippet includes the content of this cookie in the hash (aka the cache key).
It means that the first backend request that was cached will no longer be cached when requested once an item has been added to the cart.

If rules based pricing is not used in the Shopware instance, the following section can be commented out in the VCL hash snippet:

```vcl
# Consider Shopware http cache cookies
#if (req.http.cookie:sw-cache-hash) {
#	set req.hash += req.http.cookie:sw-cache-hash;
#} elseif (req.http.cookie:sw-currency) {
#	set req.hash += req.http.cookie:sw-currency;
#}
```

## Check the results using the Developer Tools

Once everything is configured, check for the `Age` header to confirm the responses are cached.

---

---

## Elasticsearch
**Source:** [products/paas/shopware-paas/elasticsearch.md](https://developer.shopware.com/docs/v6.6/products/paas/shopware-paas/elasticsearch.md)  
# Elasticsearch

Perform the following steps to activate Elasticsearch in your environment.

## Enable service

Add (or uncomment) the Elasticsearch service configuration.

```yaml
// .platform/services.yaml
elasticsearch:
   type: opensearch:2
   disk: 256
```

## Add relationship

Add (or uncomment) the relationship for the app configuration.

```yaml
// .platform.app.yaml
relationships:
    elasticsearch: "elasticsearch:opensearch"
```

## Configure instance

Follow the setup and indexing steps to prepare your instance as described in the [setup Elasticsearch](../../../guides/hosting/infrastructure/elasticsearch/elasticsearch-setup#prepare-shopware-for-elasticsearch).

After that, the following environment variables are provided by the Composer package \`shopware/paas-meta:

* `SHOPWARE_ES_HOSTS`

## Enable Elasticsearch

Ultimately, activate Elasticsearch by setting the environment variable `SHOPWARE_ES_ENABLED` to `1`. You can either do that by uncommenting the corresponding line in `platformsh-env.php` or setting it in the [variables](./setup-template#variables) section of the app configuration.

---

---

## Fastly
**Source:** [products/paas/shopware-paas/fastly.md](https://developer.shopware.com/docs/v6.6/products/paas/shopware-paas/fastly.md)  
# Fastly

Fastly allows Shopware to store the HTTP Cache at the nearest edge server to the end customer. This saves a lot of resources as the cached responses don't reach the actual application, and it decreases the response time drastically worldwide. Another benefit is that the Redis cache is not used anymore and will have less cache items.

## Setup

::: info
Fastly is supported in Shopware versions 6.4.11 or newer.
:::

1. Make sure `FASTLY_API_TOKEN` and `FASTLY_SERVICE_ID` are set in the environment or contact the support when they are missing.
2. Install the Fastly Composer package using `composer req fastly`.
3. Disable caching in the `.platform/routes.yaml`.
4. Push the new config and Fastly gets enabled.

---

---

## RabbitMQ
**Source:** [products/paas/shopware-paas/rabbitmq.md](https://developer.shopware.com/docs/v6.6/products/paas/shopware-paas/rabbitmq.md)  
# RabbitMQ

RabbitMQ is enabled by default in the template. This service is optional but recommended. It can be disabled and replaced by an SQL-backed queue.

## Disable service

Comment out the RabbitMQ service configuration.

```yaml
// .platform/services.yaml
#rabbitmq:
#   type: rabbitmq:3.8
#   disk: 1024
```

## Remove relationship

Comment out the relationship for the app configuration.

```yaml
// .platform.app.yaml
#relationships:
#   rabbitmqqueue: "rabbitmq:rabbitmq"
```

## Push changes

Push the changes to your git repository and wait for the deployment to finish.

---

---

## Repository
**Source:** [products/paas/shopware-paas/repository.md](https://developer.shopware.com/docs/v6.6/products/paas/shopware-paas/repository.md)  
# Repository

The source code of your project will reside in a git-based VCS repository. You can start with a plain project. However, we suggest starting with a new Composer create-project. You will learn more about the setup template in the [Setup Template](setup-template) section.

::: info
This guide explains the repository setup using **GitHub**. You can also integrate Bitbucket or GitLab-based version control environments with Shopware PaaS. Refer to [Source Integrations](https://docs.platform.sh/integrations/source.html) for more information.
:::

## Create a Shopware project

Firstly, create a new project with `composer create-project shopware/production <folder-name>` using the [Symfony Flex](../../../guides/installation/template.md) template.

This will create a brand new Shopware 6 project in the given folder. Now, change it into the newly created project and require the PaaS configuration with `composer req paas`.

Secondly, create a new Git repository and push it to your favourite Git hosting service.

### Updating the PaaS template recipe

You can update the recipe to the latest version using the `composer recipes:update` [command](https://symfony.com/blog/fast-smart-flex-recipe-upgrades-with-recipes-update).

However, the template may receive breaking changes. For example, when making certain changes to file mounts (like using a "service mount" instead of a "local mount"), there is no way to migrate your existing data into the updated mount automatically. Due to this, we always recommend manually checking all changes in the `recipes:update` command provided for the PaaS package, as some updates to the `.platform-yaml` files might need extra manual actions. Every PaaS recipe update should be deemed a **breaking** update and thus be validated before applying it to your project.

## Add PaaS remote

Lastly, add a second remote, which allows us to push code towards the PaaS environment and trigger a deployment.

We first need the project ID, so we display all projects using

```bash{7}
$ shopware projects

Your projects are:
+---------------+-----------+------------------+--------------+
| ID            | Title     | Region           | Organization |
+---------------+-----------+------------------+--------------+
| 7xasjkyld189e | paas-env  | <region-domain>  | shopware     |
+---------------+-----------+------------------+--------------+

Get a project by running: platform get [id]
List a projects environments by running: platform environments -p [id]
```

To add the project remote to your local repository, just run

```bash
shopware project:set-remote 7xasjkyld189e # Replace with your project ID
```

## Conclusion

Now your repository is configured - you should have two remotes

```sh
$ git remote -v

origin	git@github.com:<project-repository>.git (fetch)
origin	git@github.com:<project-repository>.git (push)
shopware	<paas-url>.git (fetch)
shopware	<paas-url>.git (push)
```

| Remote     | Function          | Description                                                             |
|------------|-------------------|-------------------------------------------------------------------------|
| `origin`   | Project Code      | This remote contains all your project specific source code              |
| `shopware` | PaaS Environment  | Changes pushed to this remote will be synced with your PaaS environment |

## Migrating from the old template to the new template

If you have already used the [Shopware PaaS old template](https://github.com/shopware/paas), please follow the guide to [migrate it to the new structure](../../../guides/installation/template#how-to-migrate-from-production-template-to-symfony-flex).

The following tasks have to be done additionally to the flex migration:

* The root `.platform.app.yml` has been moved to `.platform/applications.yaml`
* The following services has been renamed:
  * `queuerabbit` to `rabbitmq`
  * `searchelastic` to `opensearch`

As the services are renamed, a completely new service will be created. Here are three possible options available:

* Rename the services back again
* Start with a new service and re-index Elasticsearch
* [Perform the transitional upgrade of two services in parallel for some time](https://docs.platform.sh/add-services/opensearch.html#upgrading)

---

---

## Setup Template
**Source:** [products/paas/shopware-paas/setup-template.md](https://developer.shopware.com/docs/v6.6/products/paas/shopware-paas/setup-template.md)  
# Setup Template

The setup template is installed automatically using Symfony Flex when requiring the `paas` package as described in the [Repository](repository). It contains build and deployment logic for Shopware PaaS as well as configuration for the underlying infrastructure and services. In this chapter, we will have a look at these customizations.

Below is an overview of the files and directories added by the PaaS meta-package:

```text
./
├─ .platform/
│  ├─ applications.yaml
│  ├─ routes.yaml
│  ├─ services.yaml
├─ bin/
│  ├─ prestart_cacheclear.sh
├─ config/
│  ├─ packages/
│  │  ├─ paas.yaml
├─ files/
│  ├─ theme-config/
```

## [.platform/applications.yaml](https://github.com/shopware/recipes/blob/main/shopware/paas-meta/6.4/.platform/applications.yaml)

This file contains Shopware PaaS specific configuration and can be customized as needed for your individual project.

### name

It is the name of your app. It is used in commands like:

```bash
shopware ssh -A app 'bin/console theme:dump'
```

Unless there is a specific need for it, leave it as `app`.

### type

This section contains the base image used for your build process. This is also where you configure the PHP version used in your PaaS environment.

### variables

This section contains configuration for environment variables or server settings. General store settings and configurations are set here. Here you can inject custom environment variables or enable feature flags.

Variables in the `env` section are automatically injected as environment variables. If a variable is also set in your .env file, the variables set in the `applications.yaml` file will overwrite these.

### hooks

Lifecycle hooks are custom scripts that are called during your build and deploy processes. See more on the [deployment process](./build-deploy#push-main-branch).

#### build hook

This script is called during the build process and builds your application's assets (composer dependencies, javascript- and css- assets of Shopware core and extensions) and disables the UI installer. You can customize this script if you need. During the execution, you may perform write operations on the file system, which are prohibited in the proceeding steps unless the corresponding directory is [mounted](#mounts).

You do not have access to any of the services (like the database or Redis) configured, as the application is not running yet. You should ensure to perform as much of your entire building procedure during the build step, as web traffic is blocked during the execution of the deploy step.

#### deploy hook

::: warning
The environment will be cut off from web traffic during the execution of the deploy hook. The shorter this script is, the shorter the downtime will be.
:::

This script is called during the deployment process. Theme configuration is copied, the install scripts are executed and secrets are generated.

* Copy theme configuration
* Run database migrations
* Set sales channel domains for non-production environments
* Clear cache

If this is the first deployment, the following operations are performed:

* Setup script is executed
* Theme is set
* Secrets are generated
* `install.lock` file is created

You can also customize this script, however, make sure to keep operations to a minimum, as your store will not be exposed to web traffic during the execution. Connections made during the meantime will be queued in a suspended state and not necessarily fail but will take longer than usual (i.e., until the deployment has finished).

#### post\_deploy

Analogous to the two preceding hooks, the post\_deploy hook provides an entry point for custom scripts. However, this hook is executed after the application container accepts connections.

### relationships

This section defines the mapping between services created in the [services.yaml](https://github.com/shopware/recipes/blob/main/shopware/paas-meta/6.4/.platform/services.yaml) and the application itself.

### mounts

By default, the entire storage of your application is read-only. Mounts define directories that are writable after the build is complete. They aren’t available during the build.

Every mount has one of two types: `local` or `service`.
A local mount is unique to the service that is accessing it. For example `/var/cache` is a good local mount because the Symfony cache should not be shared between different app servers.
A service mount references to another service (of the type `network-storage`). These mounts are shared between other services and between the different app servers. For example the `/public/media` folder is a good shared mount because the [workers](#workers) that consume the Messenger queue should be able to read and write to the media directory.

### web

The public root of your application `public/index.php` is configured so the server knows where to route dynamic requests.

### workers

Workers are copies of your application instance after the [build hook](#build-hook) has been executed. They are usually configured with a start command. By default, there are two configured workers - one for message queues and one for scheduled tasks.

## [.platform / routes.yaml](https://github.com/shopware/recipes/blob/main/shopware/paas-meta/6.4/.platform/routes.yaml)

This file configures incoming HTTP requests routed to the `app` instance.

## [.platform / services.yaml](https://github.com/shopware/recipes/blob/main/shopware/paas-meta/6.4/.platform/services.yaml)

This file contains services that are used by the `app` instances. Depending on your setup, uncomment or add services that you need, and they will be created and scaled automatically.

In our template there are 4 different services enabled by default:

* `db`
* `cacheredis`
* `rabbitmq`
* `fileshare`

## [files / theme-config](https://github.com/shopware/recipes/tree/main/shopware/paas-meta/6.4/files/theme-config)

We suggest checking in your theme configuration to version control in this directory. Read more on the concept of [builds without database](../../../guides/hosting/installation-updates/deployments/build-w-o-db) as described in [Theme Build](./theme-build).

---

---

## Introduction to Shopware PaaS Native
**Source:** [products/paas/shopware.md](https://developer.shopware.com/docs/v6.6/products/paas/shopware.md)  
# Introduction to Shopware PaaS Native

**Shopware PaaS Native (Platform-as-a-Service)** is a fully managed, cloud-native environment dedicated to hosting and developing Shopware applications. Built with an opinionated infrastructure, Shopware PaaS Native enables developers to focus on custom development without the overhead of managing scalability or infrastructure. This platform is optimized for efficiency, scalability, and rapid iteration, helping developers streamline Shopware project workflows.

## Key technical features

* **Kubernetes and AWS-Powered Infrastructure:** Shopware PaaS Native is built on a Kubernetes-based architecture running on AWS. This setup provides managed resources—such as servers, storage, networking, and databases—optimized to scale automatically based on application demands, ensuring high availability and stability without manual intervention.

* **Developer-Centric Tools and Workflows:** The platform includes preconfigured tools and standardized workflows specifically designed for Shopware development. These tools enable seamless integration with CLI, APIs, and other familiar development resources, streamlining deployment, testing, and monitoring processes.

* **Efficient Build and Deployment Pipelines:** Developers benefit from a ready-to-use environment optimized for continuous integration and deployment (CI/CD), reducing the need to manage complex infrastructure configurations. This setup accelerates development lifecycles and minimizes error rates.

## Shopware PaaS Native Architecture

The architecture of Shopware PaaS Native includes two primary layers:

1. **Infrastructure Layer:** A robust, cloud-based foundation powered by Kubernetes and AWS. Resources are configured to scale based on project needs, ensuring high availability and stability.

2. **Platform Layer:** A preconfigured environment with integrated best practices and tools, streamlining the development and deployment of Shopware applications. This layer accelerates workflows and reduces operational complexity by providing a consistent and managed setup.

## Comparison with Self-Hosted and SaaS Models

| **Model**                         | **Self-Hosted**                      | **Shopware PaaS Native**                                  | **SaaS**                                          |
|-----------------------------------|--------------------------------------|----------------------------------------------------|---------------------------------------------------|
| **Infrastructure Responsibility** | Fully managed by the customer        | Managed by Shopware (customer manages application) | Fully managed by Shopware                         |
| **Control Over Customization**    | Complete control                     | High control with opinionated best practices       | Limited; customization possible only through apps |
| **Setup and Maintenance Effort**  | High                                 | Moderate, with most infrastructure tasks automated | Low                                               |
| **Ideal Use Case**                | Full control, advanced custom setups | Balance of control and managed scalability         | Ease of use with minimal setup                    |

---

---

## Prerequisites
**Source:** [products/paas/shopware/CLI.md](https://developer.shopware.com/docs/v6.6/products/paas/shopware/CLI.md)  
The Shopware PaaS Native CLI allows you to manage shops and resources within the PaaS cloud in a simple way.

## Prerequisites

To access Shopware PaaS Native resources via the CLI, you must first have an account. Shopware uses AWS Cognito as its identity provider. At present, users must be invited to our identity platform before they can access any resources.

Once your organization is successfully onboarded to the Shopware Business Platform (SBP) and users added to Shopware PaaS Native, the initial user is assigned the admin role. This admin user can then assign roles to the rest of the organization.

For details on managing users, refer to our [Account Management Commands Guide](./commands/account.md).

## Installation

Visit the [releases page for the sw-paas](https://github.com/shopware/paas-cli/releases) GitHub project and find the appropriate archive for your operating system and architecture. Download the archive and retrieve it to your home directory.

:::info
To make this as easy as possible, we will be adding the binaries to some package managers soon.
:::

## Authentication

After successful installation, you will need to authenticate to enable authorized access to other CLI functionalities.

The `auth` command opens a browser window where you log in to your Shopware PaaS Native account. After successful login, the authentication token is retrieved and saved in the `XDG` state directory, which depends on your system.

```sh
sw-paas auth
```

To view your user-id and roles in the PaaS system, execute:

```sh
sw-paas account whoami
```

Visit [the account command](./account) walkthrough for more information on how to manage your account and provision machine tokens for CI/CD pipelines.

## Authorization

To access resources in our paas system, you need to have specific roles inside the organization. To add somebody to a role in your organization you need to have **Account Admin** role in your organization.

Check for the role:

```sh
sw-paas account whoami
```

If you are already `Account Admin`, and you would like to add more users.

On the cli use this command to get the user-id:

```sh
sw-paas account whoami --output json
# or if you have jq installed
sw-paas account whoami --output json | jq ".sub"
```

Add the user to your organization and select a new role:

```sh
sw-paas account user add --sub "<user-id of the new user>"
```

### Report an issue

Should you spot a bug, please report it in our [issue tracker](https://github.com/shopware/paas-cli/issues).

---

---

## Account
**Source:** [products/paas/shopware/CLI/account.md](https://developer.shopware.com/docs/v6.6/products/paas/shopware/CLI/account.md)  
# Account

The `account` command gives you access to account-level operations such as context management, token handling, user-role mapping, and role identification. An **account** represents your access to resources within our backend environment.

## Usage

```sh
sw-paas account [command]
```

## Commands

### Account Context

The `context` command lets you define and manipulate a *context file*, allowing the CLI to skip repetitive prompts for `organization-id` and `project-id`. The default context file is saved as `context-production.yaml` and stored alongside the main config file. Below is the location of where these files are stored.

|                 | Unix                   | MacOS                                      | Windows        |
|-----------------|------------------------|--------------------------------------------|----------------|
| XDG\_CONFIG\_HOME | ~/.config/sw-paas      | ~/Library/Application Support/sw-paas | %LOCALAPPDATA% |
| XDG\_STATE\_HOME  | ~/.local/state/sw-paas | ~/Library/Application Support/sw-paas | %LOCALAPPDATA% |

**Usage:**

```sh
sw-paas account context [command]
```

**Available Subcommands:**

* `set`: Define or update your current context.
* `show`: Display the currently active context values.
* `delete`: Remove the saved context.

**Examples:**

```sh
# Set a new context for organization and project
sw-paas account context set --organization-id org-123 --project-id proj-456

# Set a new context for organization skipping project
sw-paas account context set --organization-id org-123 --skip-project-id

# View the current context
sw-paas account context show

# Delete the current context file
sw-paas account context delete
```

### Authentication Tokens

The `token` command manages personal access tokens for secure API and CLI usage. Tokens can be created, listed, and revoked.

**Usage:**

```sh
sw-paas account token [command]
```

**Available Subcommands:**

* `create`: Generate a new access token.
* `list`: View all your active tokens.
* `revoke`: Remove a specific token.

**Examples:**

```sh
# Create a new token
sw-paas account token create --name "ci-token"

# List all active tokens
sw-paas account token list

# Revoke a token by ID
sw-paas account token revoke --token-id abcd-1234
```

### Users and Roles

Use the `user` command to map users to specific roles within the organization. Only users with sufficient privileges (e.g., admin) can modify roles.

**Usage:**

```sh
sw-paas account user [command]
```

**Available Subcommands:**

* `add`: Add a user to the organization with a specific role.
* `remove`: Remove a user from a role.

If you already have the `project-admin` role and wish to add additional users to your organization, they can share their **user ID (sub-id)** with you. You can instruct them to retrieve it using the following command:

```sh
sw-paas account whoami --output json
```

Or, if they have `jq` installed for easier parsing:

```sh
sw-paas account whoami --output json | jq ".sub"
```

Once you receive their `sub` (subject ID), you can proceed to add them to your organization with the appropriate role.

**Available Roles:**

* `read-only`: Gets access to projects and applications. Only actions allowed are `get` and `list`.
* `developer`: Gets access to projects and applications. All actions are allowed.
* `account-admin`: Gets access to projects and applications. All actions are allowed.
* `project-admin`: Gets access to account management. Actions for managing Users are allowed.

**Examples:**

```sh
# Add a new user as a developer
sw-paas account user add --sub adbs-123 --organization-id abc-123 --role developer

# Remove a user from the developer role
sw-paas account user remove --sub adbs-123 --organization-id abc-123 --role developer
```

### **whoami** – Show Your Identity and Roles

Use the `whoami` command to display your identity, including your User ID(Sub ID), email, and associated policies within the account.

**Usage:**

```sh
sw-paas account whoami
```

This is especially helpful for confirming which roles and permissions are currently active in a given account.

## **Tips**

* Always set a context to reduce repetitive prompts across commands.
* Token management is essential for CI/CD and script-based access. You can use this in environments such as Github Action, CircleCI, GitLab CI, Travis CI etc.
* Use `whoami` to verify access if permission errors occur.

---

---

## Applications
**Source:** [products/paas/shopware/CLI/applications.md](https://developer.shopware.com/docs/v6.6/products/paas/shopware/CLI/applications.md)  
# Applications

The `application` command manages deployments in Shopware PaaS Native. Each application represents a deployment of your codebase within a project. Projects can contain multiple applications (e.g., for staging, production).

## Usage

```sh
sw-paas application [command]
```

## Commands

### Creating an Application

Deploy a new application to a project.

**Usage:**

```sh
sw-paas application create [flags]
```

**Flags:**

* `--project-id`: ID of the target project. If not provided, the CLI will try to fetch it from the repository.
* `--name`: Name of the application. If not provided, the CLI will prompt for it.
* `--commit-sha`: Commit SHA to deploy. If not provided, the CLI will prompt for it.
* `--help`: Display help for the command.

**Example:**

```sh
sw-paas application create --project-id "proj-1" --name "my-app" --commit-sha "abcdef123456"
```

### Updating an Application

Update an existing application with a new commit SHA.

**Usage:**

```sh
sw-paas application update [flags]
```

**Flags:**

* `--project-id`: ID of the project.
* `--application-id`: ID of the application.
* `--commit-sha`: Commit SHA to deploy.
* `--help`: Display help for the command.

**Example:**

```sh
sw-paas application update --project-id "proj-1" --application-id "app-1" --commit-sha "abcdef123456"
```

### Listing Applications

List all applications associated with a specific project.

**Usage:**

```sh
sw-paas application list [flags]
```

**Flags:**

* `--project-id`: ID of the project.
* `--help`: Display help for the command.

**Example:**

```sh
sw-paas application list --project-id "proj-1"
```

### Checking Applications

Check the status of applications.

**Usage:**

```sh
sw-paas application check [flags]
```

**Flags:**

* `--project-id`: ID of the project.
* `--application-id`: ID of the application.
* `--help`: Display help for the command.

## Build Commands

### Listing Builds

List all builds for a specific application.

**Usage:**

```sh
sw-paas application build list [flags]
```

**Flags:**

* `--application-id`: ID of the application.
* `--organization-id`: ID of the organization.
* `--project-id`: ID of the project.
* `--help`: Display help for the command.

**Example:**

```sh
sw-paas application build list --organization-id "org-1" --project-id "proj-1" --application-id "app-1"
```

### Viewing Build Logs

Display logs of a specific build.

**Usage:**

```sh
sw-paas application build logs [flags]
```

**Flags:**

* `--application-id`: ID of the application.
* `--application-build-id`: ID of the build.
* `--organization-id`: ID of the organization.
* `--project-id`: ID of the project.
* `--help`: Display help for the command.

**Example:**

```sh
sw-paas application build logs --organization-id "org-1" --project-id "proj-1" --application-id "app-1" --application-build-id "build-1"
```

### Starting a Build

Trigger a new build for the specified application.

**Usage:**

```sh
sw-paas application build start [flags]
```

**Flags:**

* `--application-id`: ID of the application.
* `--organization-id`: ID of the organization.
* `--project-id`: ID of the project.
* `--help`: Display help for the command.

**Example:**

```sh
sw-paas application build start --organization-id "org-1" --project-id "proj-1" --application-id "app-1"
```

### Deleting an Application

Delete an existing application from a project.

**Usage:**

```sh
sw-paas application delete [flags]
```

**Flags:**

* `--application-id`: ID of the application to be deleted (required).
* `--project-id`: ID of the project (optional, fetched if omitted).
* `--help`: Display help for the command.

**Example:**

```sh
sw-paas application delete --application-id "app-1" --project-id "proj-1"
```

---

---

## Managing Commands
**Source:** [products/paas/shopware/CLI/command.md](https://developer.shopware.com/docs/v6.6/products/paas/shopware/CLI/command.md)  
# Managing Commands

The `command` command allows you to create and manage commands that are executed in dedicated containers. This is particularly useful for CI/CD environments or when you need to run commands asynchronously without waiting for their completion.

## Usage

```sh
sw-paas command [command]
```

:::info
The default execution directory is `/var/www/html`
The container has a time-to-live (TTL) of 1 hour, so your command must complete within that timeframe.
:::

## Description

Unlike the `exec` command which provides an interactive shell session, the `command` command executes your commands in dedicated containers that are spun up specifically for that purpose. This approach is better suited for:

* CI/CD environments
* Asynchronous command execution
* Automated processes
* Situations where you don't need to wait for command completion

Here is [a list of Shopware console commands](https://docs.shopware.com/en/shopware-6-en/tutorials-and-faq/shopware-cli).

## Available Commands

### `command create`

Create a new command that will be executed in a dedicated container.

```sh
sw-paas command create [flags]
```

### `command get`

Get detailed information about a specific command.

```sh
sw-paas command get [flags]
```

### `command list`

List all available commands.

```sh
sw-paas command list [flags]
```

### `command output`

Get the output of a specific command.

```sh
sw-paas command output [flags]
```

:::info
See this [FAQ section](./../faq) for the main difference between `exec` and `command`
:::

## Examples

1. Create a new command:

   ```sh
   sw-paas command create --project-id my-project --application-id my-app --script "bin/console cache:clear"
   ```

2. List all commands:

   ```sh
   sw-paas command list
   ```

3. Get command output:

   ```sh
   sw-paas command output --command-id abc123
   ```

## Notes

* Commands are executed in isolated containers, ensuring clean environments for each execution
* You can track command execution status and retrieve output even after the command has completed
* This approach is more suitable for automated processes than interactive debugging

---

---

## Executing Commands
**Source:** [products/paas/shopware/CLI/exec.md](https://developer.shopware.com/docs/v6.6/products/paas/shopware/CLI/exec.md)  
# Executing Commands

The `exec` command allows you to execute commands in a remote terminal session for your applications. This is useful for running commands directly on your application's environment, such as debugging, maintenance, or running one-off commands. Here is [a list of Shopware console commands](https://docs.shopware.com/en/shopware-6-en/tutorials-and-faq/shopware-cli).

## Usage

```sh
sw-paas exec [flags]
```

## Description

The `exec` command provides two main functionalities:

1. List existing terminal sessions
2. Start a new terminal session.

By default, the command will show existing sessions if there are any or start a new session if no existing sessions are found.

:::info
See this [FAQ section](./../faq) for the main difference between `exec` and `command`
:::

## Flags

* `--application-id string`: The ID of the application you want to execute commands in
* `--new`: Force creation of a new terminal session
* `--organization-id string`: The ID of the organization
* `--project-id string`: The ID of the project
* `-h, --help`: Show help for the exec command

## Examples

1. List existing terminal sessions:

   ```sh
   sw-paas exec
   ```

2. Force creation of a new terminal session:

   ```sh
   sw-paas exec --new
   ```

3. Execute commands in a specific application:

   ```sh
   sw-paas exec --project-id my-project --application-id my-app
   ```

## Notes

* When using the command without any flags, it will automatically handle the session management based on existing sessions
* The `--new` flag is useful when you want to ensure you're starting a fresh session
* Make sure to provide the necessary IDs (application, project, organization) when working with specific resources
* To exit the remote shell, type `exit` and press Enter
* You can reuse existing terminal sessions instead of creating new ones each time, which can be more efficient for ongoing work

---

---

## Open
**Source:** [products/paas/shopware/CLI/open.md](https://developer.shopware.com/docs/v6.6/products/paas/shopware/CLI/open.md)  
# Open

The `open` command lets you access critical service interfaces and internal tools within Shopware PaaS Native. This command is essential for quickly navigating to application endpoints such as the Admin, Storefront, Grafana dashboard, or opening service tunnels for debugging and direct access.

## Usage

```sh
sw-paas open [command]
```

:::info
To avoid repeatedly specifying `organization-id` and `application-id`, either use the `context` command to set them persistently, or run the CLI in interactive mode for guided input.
:::

## Commands

### Admin Panel Access

Use this command to retrieve the Admin URL and credentials required for logging into the Shopware Admin interface.

**Usage:**

```sh
sw-paas open admin [flags]
```

**Flags:**

* `--organization-id`: ID of the organization
* `--application-id`: ID of the application

**Example:**

```sh
sw-paas open admin --organization-id abc123 --application-id abc123
```

### Storefront URL Access

Use this command to retrieve the URL of the Shopware Storefront application.

**Usage:**

```sh
sw-paas open storefront [flags]
```

**Flags:**

* `--organization-id`: ID of the organization
* `--application-id`: ID of the application

**Example:**

```sh
sw-paas open storefront --organization-id abc123 --application-id abc123
```

### Monitoring Dashboard

Access the Grafana dashboard with this command to visualize and monitor application metrics.

**Usage:**

```sh
sw-paas open grafana [flags]
```

**Flags:**

* `--organization-id`: ID of the organization
* `--application-id`: ID of the application

**Example:**

```sh
sw-paas open grafana --organization-id abc123 --application-id abc123
```

### Open a Tunnel to a Service

This command establishes a local port tunnel to one of the internal services. It is useful for debugging or interacting directly with backend components. The current supported services are: `database`, `valkey-app`, `valkey-worker`.

**Usage:**

```sh
sw-paas open service [flags]
```

**Flags:**

* `--service`: Name of the service to connect to.
* `--organization-id`: ID of the organization
* `--application-id`: ID of the application

**Example:**

```sh
sw-paas open service --service database --organization-id abc123 --application-id abc123
```

---

---

## Organization
**Source:** [products/paas/shopware/CLI/organizations.md](https://developer.shopware.com/docs/v6.6/products/paas/shopware/CLI/organizations.md)  
# Organization

The `organization` command allows you to manage organizations, which serve as the top-level container representing a company or entity in Shopware PaaS Native. Each organization can contain multiple projects. Admin users within an organization can manage user access through the `account` commands.

## Usage

```sh
sw-paas organization [command]
```

**Aliases:**
`organization`, `org`

## Commands

### Creating an Organization

Use this command to create a new organization. Only users with appropriate permissions can perform this action.

**Usage:**

:::info
It's recommended to choose a clear and distinct name for your organization, as it will be visible across your teams and projects.
:::

```sh
sw-paas organization create --name "Awesome GmbH"
```

### Retrieving an Organization

Fetch details of a specific organization using its unique identifier.

**Usage:**

```sh
sw-paas organization get --organization-id org-123
```

**Flags:**

* `--organization-id`: ID of the organization to retrieve.

### Listing All Organizations

Displays a list of all organizations you are a part of, including relevant metadata such as ID and name.

**Usage:**

```sh
sw-paas organization list
```

---

---

## Project
**Source:** [products/paas/shopware/CLI/project.md](https://developer.shopware.com/docs/v6.6/products/paas/shopware/CLI/project.md)  
# Project

The project command enables you to manage and organize projects within Shopware PaaS Native. A project is a logical entity that encapsulates your application environments such as staging and production and is linked to a specific codebase repository.

Each project supports multiple application instances and shares infrastructure settings within the same organization.

Projects serve as the foundational unit for deployments. They define the application code source (Git repository), the project type and associated resources.

## Usage

```sh
sw-paas project [command]
```

:::info
To avoid repeatedly specifying `organization-id`, either use the `context` command to set them persistently, or run the CLI in interactive mode for guided input.
:::

## Commands

### Creating a New Project

Initialize a new project in your organization by specifying its name, repository, and type. To enable secure code fetching from private repositories during deployments, Shopware PaaS Native uses SSH deploy keys. [Here is a guide](./repository.md) on how you can configure deploy keys.

**Usage:**

```sh
sw-paas project create [flags]
```

**Flags:**

* `--name`: The name of the project.
* `--repository`: The repository URL associated with the project.
* `--type`: The type of the project (`shopware`, `blackbox`).

**Example:**

```sh
sw-paas project create --name "myproject" --repository "https://github.com/example/repo.git" --type shopware
```

This example creates a Shopware project named `myproject` linked to the specified Git repository.

### List All Projects

Displays all projects associated with your user or organization, along with key metadata such as project name, type, and repository.

**Usage:**

```sh
sw-paas project list
```

---

---

## Setting Up Repository Access via Deploy Keys
**Source:** [products/paas/shopware/CLI/repository.md](https://developer.shopware.com/docs/v6.6/products/paas/shopware/CLI/repository.md)  
## Setting Up Repository Access via Deploy Keys

To enable Shopware PaaS Native to access your private Git repository, you must configure an **SSH deploy key**. This key allows the platform to securely clone your code during deployments.

Regardless of whether you use the CLI or set things up manually, you must **add the public SSH key to your repository**.

### Option 1: Automated Setup via PaaS CLI

For a quicker setup, you can use the PaaS CLI to automatically generate and register the key:

```sh
sw-paas vault create --type ssh
```

By default, this command stores the key at the **organization level**, making it available to all projects within the org. To limit the key to a specific project, use the `--project` flag:

```sh
sw-paas vault create --type ssh --project <project-id>
```

After running the command, copy the generated public key and add it to your Git repository's **Deploy keys** section (see instructions below).

### Option 2: Manual Setup

If you prefer full control over the SSH key creation process, follow these steps:

#### 1. Generate a Passwordless SSH Key Pair

Run the following command to generate an RSA key pair in PEM format:

```bash
ssh-keygen -t rsa -b 4096 -m PEM -f ./sw-paas
```

:::info
Alternative algorithms like **ED25519** and **ECDSA** are also supported, provided the key is **passwordless** and the **private key is in PEM format**.
:::

#### 2. Add the Public Key to Your Repository

Open the file `sw-paas.pub`, copy its contents, and add it as a **read-only deploy key** in your Git repository:

* **GitHub**: Go to your repository `Settings` → `Deploy keys`
* **GitLab**/**Bitbucket**: Look for the equivalent "Deploy keys" section in your repository settings
  Be sure to enable **read-only access**.

#### 3. Store the Private Key in the Vault

Once the public key is added to your repo, store the corresponding private key in the Shopware PaaS Native Vault:

```bash
cat sw-paas | sw-paas vault create --type ssh --password-stdin
```

You can store the key at either:

* **Organization level**: Shared across all projects.
* **Project level**: Dedicated to a single project (takes precedence over the org-level key).

:::warning
Only one SSH key can be stored per level (organization or project). You may name the key freely, but keep in mind that a project-level key **overrides** an organization-level one during deployments.
:::

---

---

## Vault
**Source:** [products/paas/shopware/CLI/vault.md](https://developer.shopware.com/docs/v6.6/products/paas/shopware/CLI/vault.md)  
# Vault

The `vault` command manages secrets in Shopware PaaS Native. Secrets are encrypted pieces of sensitive data such as API keys, credentials, or SSH private keys. These secrets are securely stored and only accessible to users with the required permissions.

## Usage

```sh
sw-paas vault [command]
```

## Commands

### Creating a New Secret

Use this command to create and securely store a new secret.

**Usage:**

```sh
sw-paas vault create [flags]
```

**Flags:**

* `--key`: Key name for the secret.
* `--organization-id`: ID of the organization.
* `--project-id`: ID of the project.
* `--application-id`: ID of the application.
* `--value`: Value of the secret (used for all types except `ssh`).
* `--password-stdin`: Read the secret value from stdin (only valid when type is `ssh`).
* `--type`: Type of secret. Accepted values: `env`, `buildenv`, `ssh`.
* `--help`: Display help for the command.

**Type of secret and scope of use**
`env`: Available at runtime in the environment.
`buildenv`: Used during build processes.
`ssh`: SSH keys for secure connections.

**Examples:**

Create a standard environment secret:

```sh
sw-paas vault create --organization-id "org-123" --project-id "proj-456" --application-id "app-789" --key "API_KEY" --value "my-api-key" --type env
```

Create an SSH secret from stdin:

```sh
cat private.pem | sw-paas vault create --key "SSH_KEY" --type ssh --password-stdin
```

### Deleting a Secret

Use this command to delete an existing secret.

**Usage:**

```sh
sw-paas vault delete --secret-id [id]
```

**Flags:**

* `--secret-id`: ID of the secret to delete.
* `--help`: Display help for the command.

**Example:**

```sh
sw-paas vault delete --secret-id "secret-abc123"
```

This example deletes the secret identified by `secret-abc123`.

***

### Listing Available Secrets

Use this command to list all secrets associated with a specific scope.

**Usage:**

```sh
sw-paas vault list [flags]
```

**Flags:**

* `--organization-id`: ID of the organization.
* `--project-id`: ID of the project.
* `--application-id`: ID of the application.
* `--with-metadata`: Include metadata such as project name.
* `--help`: Display help for the command.

**Example:**

```sh
sw-paas vault list --organization-id "org-123" --project-id "proj-456"
```

This command lists all secrets for the specified project. Secrets scoped to applications within the project are also included.

---

---

## Watch
**Source:** [products/paas/shopware/CLI/watch.md](https://developer.shopware.com/docs/v6.6/products/paas/shopware/CLI/watch.md)  
# Watch

The `watch` command allows you to monitor events related to a specific project in Shopware PaaS Native. It listens for real-time events associated with the project and its applications. You can specify the project ID, application IDs, and event types to filter the events you want to observe.

## Usage

```sh
sw-paas watch [flags]
```

## Flags

* `--project-id`: The ID of the project whose events you want to watch. If not provided, the command attempts to infer the project from the Git repository's remote URL.
* `--application-ids`: A list of application IDs whose events you want to monitor. If not provided, it watches all applications associated with the project.
* `--event-types`: A list of event types to filter (e.g., deployment events, application events). You can choose specific event types to subscribe to. By default, it listens to all events.

## Examples

Watch all events of a project:

```sh
  sw-paas watch --project-id abc123
```

Watch specific application events in a project:

```sh
  sw-paas watch --project-id abc123 --application-ids app1,app2
```

Watch specific event types:

```sh
  sw-paas watch --project-id abc123 --event-types "EVENT_TYPE_DEPLOYMENT_STARTED,EVENT_TYPE_DEPLOYMENT_FINISHED"
```

The `--event-types` flag allows you to filter the event types to watch for. The available event types are fetched from Shopware PaaS Native and are sorted for easy selection.

### Project ID and application IDs

* **`--project-id`**: The ID of the project is required to subscribe to its events. If the flag is not set, the command attempts to infer the project ID from the current Git remote (assuming a linked repository).
* **`--application-ids`**: You can optionally filter the events by specifying application IDs within the project. If omitted, it subscribes to all application events in the project.

### Event subscription

Once the `watch` command is triggered, it establishes a connection to the Shopware PaaS Native event stream and listens for the specified events. The events are printed out in real time to the terminal.

---

---

## CDN
**Source:** [products/paas/shopware/cdn.md](https://developer.shopware.com/docs/products/paas/shopware/cdn.md)  
# CDN

This section provides comprehensive information about Content Delivery Network (CDN) solutions for Shopware PaaS Native, with a focus on Fastly integration and optimization strategies.

## Fastly CDN

Fastly serves as the primary CDN solution for Shopware PaaS Native, delivering edge caching capabilities that significantly enhance your shop's performance and user experience. By storing HTTP cache at the nearest edge server to your customers, Fastly reduces response times globally while minimizing resource consumption on your application servers.

### Key Benefits

* **Global Performance**: Cached responses are served from edge locations worldwide, drastically reducing latency
* **Resource Optimization**: Reduces load on your application servers by serving cached content from the edge
* **Redis Cache Relief**: Minimizes Redis cache usage by handling HTTP cache at the CDN level
* **Automatic Scaling**: Seamlessly handles traffic spikes without impacting your application performance

### Integration

Fastly is fully integrated into Shopware PaaS Native. The integration includes:

* Pre-configured VCL snippets for optimal Shopware performance
* Automatic cache invalidation mechanisms
* Soft purge capabilities to maintain performance during cache updates
* Deployment helper integration for seamless VCL snippet management

### Configuration

Fastly is automatically configured and enabled by default in Shopware PaaS Native environments. No additional Shopware configuration is required - the PaaS platform handles all Fastly setup, VCL snippets, and cache management automatically.

#### Custom Domain DNS Configuration

To configure your custom domain with the Fastly CDN, you must configure a DNS record. Depending of the type of your record, the DNS configuration is different.

If you have multiple custom domains, you need to create a record per domain.

**None APEX record**

Configure a `CNAME` record with your custom domain's DNS to point to:

```dns
cdn.shopware.shop
```

**APEX record**

Configure a `A` with your custom domain's DNS to point to:

```dns
151.101.3.52
151.101.67.52
151.101.131.52
151.101.195.52
```

This configuration ensures that all traffic to your custom domain is routed through the Fastly CDN for optimal performance and caching.

#### Managing Custom Domains

Custom domain management is handled through the `sw-paas` CLI domain command. You can attach multiple domains to a single shop. Following domain creation, you must update the application using `sw-paas application update`. You may use the same commit to trigger a deployment. This process will be automated in future releases.

Subsequently, you can configure the domain within Shopware and associate it with a storefront. Status update functionality is currently under development.

---

---

## Frequently Asked Questions
**Source:** [products/paas/shopware/faq.md](https://developer.shopware.com/docs/v6.6/products/paas/shopware/faq.md)  
## Frequently Asked Questions

### Can I roll back my deployment if I lose my git history?

For now, no rollback is possible when you do a force push and lose your git history

### Is it possible to write to the local filesystem?

No, all containers are stateless, and local file writes are discouraged. Persistent storage must use S3 buckets or other external storage solutions.

### How can I connect my already deployed application to a new branch?

The application that you create is linked to a commit SHA and not to a branch. You can change the existing application commit SHA by running `sw-paas application update`. What matters is the commit configured for a given application.

### Why can't I manage extensions in the Shopware Administration?

Plugin management via the Administration interface is not supported in PaaS because the platform runs in a high-availability (HA) and clustered environment. In such setups, local changes aren't feasible, as all instances must remain identical and stateless. To ensure consistency across all deployments, plugins must be installed or updated via Composer, as part of the project’s codebase. You need to install or update extensions [via Composer](./../../../guides/hosting/installation-updates/extension-managment.html#installing-extensions-with-composer).

### Can I run different applications like Node.js?

No, currently PaaS is limited to Shopware projects.

### How are secrets managed in PaaS?

Secrets are stored in the PaaS secret store and can be applied at the organization, project, or application level. They are encrypted in the database and decrypted only when accessed via the CLI.

### Can I access the database directly?

Yes. Follow the guide on [open command](./CLI/open).

### Can I customize the infrastructure (e.g., change web server configurations)?

No, the infrastructure is opinionated and pre-configured. Customizations at the server level are not allowed.

### Are CDN or database configurations customizable?

No, PaaS uses Fastly as the CDN and provides a fixed database configuration at the moment. Customizations to these resources are currently under development.

### Can I host my custom applications?

Custom applications and decoupled storefront hosting will be evaluated based on customer needs but are not currently supported.

### What is the difference between `exec` and `command` ?

1. **Container Management**:

   * `exec`: Uses an existing container and provides an interactive shell
   * `command`: Spins up a new container specifically for the command execution

2. **Execution Mode**:

   * `exec`: Interactive and synchronous
   * `command`: Non-interactive and can be asynchronous

3. **Use Cases**:
   * `exec`: Best for debugging, maintenance, and interactive work
   * `command`: Best for automation, CI/CD, and scheduled tasks

### Can I connect to my PaaS instance via SSH

Yes, you can connect to your PaaS instance — but not via traditional SSH. Instead, we provide a remote terminal session through the `sw-paas exec` command. This command allows you to execute shell commands inside your PaaS environment remotely, effectively giving you SSH-like access for troubleshooting, deployments, or interactive sessions. You can find the detailed guide on how to use `sw-paas exec` in the [documentation here](../shopware/CLI/exec).

### Where can I see the status of my PaaS application update?

You can see the status of your PaaS application by running `sw-paas application list`. This command shows the current status of your application, including whether the update was successful or if it's still in progress. See more in the [documentation here](../shopware/CLI/applications). To monitor all real-time events associated with the project and its applications run `sw-paas watch` this provides a live stream of events and is especially useful for tracking the progress of an ongoing update. [Learn more here](../shopware/CLI/watch).

---

---

## Fundamentals
**Source:** [products/paas/shopware/fundamentals.md](https://developer.shopware.com/docs/products/paas/shopware/fundamentals.md)  
# Fundamentals

This section will introduce the fundamental pieces of Shopware PaaS Native.

---

---

## Account
**Source:** [products/paas/shopware/fundamentals/account.md](https://developer.shopware.com/docs/products/paas/shopware/fundamentals/account.md)  
# Account

An account represents your access to resources within the Shopware PaaS Native backend environment which includes context management, token handling, and role identification.

## Roles

To find what resources you have access to via the CLI:

```sh
sw-paas account whoami
```

## Context

To avoid repetitive prompts for `organization-id` and `project-id`, you can set a context and the CLI will automatically use these values without asking.

Setting your context streamlines your workflow by eliminating the need to specify these parameters with every command.

```sh
sw-paas account context set
```

The context is saved as `context-production.yaml` and stored alongside the main configuration file in the following locations:

|                 | Unix                   | macOS                                      | Windows        |
|-----------------|------------------------|--------------------------------------------|----------------|
| XDG\_CONFIG\_HOME | ~/.config/sw-paas      | ~/Library/Application Support/sw-paas | %LOCALAPPDATA% |
| XDG\_STATE\_HOME  | ~/.local/state/sw-paas | ~/Library/Application Support/sw-paas | %LOCALAPPDATA% |

## Authentication Tokens

The `token` command manages personal access tokens, enabling secure authentication for both API and CLI operations without exposing your main account credentials. Personal access tokens are especially useful for automating workflows, such as authenticating in CI/CD pipelines or integrating with external systems.

### Creating a Token

Generate a new access token:

```sh
sw-paas account token create --name "ci-token"
```

### Using a Token

To use a token you have multiple options:

```sh
token=<your-token-here>
sw-paas --token $token account whoami
sw-paas --token "<your-token-here>" account whoami

# Set it for the current terminal session
export SW_PAAS_TOKEN=<your-token-here>
sw-paas account whoami
```

### Revoking a Token

Remove a specific token by ID:

```sh
sw-paas account token revoke --token-id abcd-1234
```

---

---

## Applications
**Source:** [products/paas/shopware/fundamentals/applications.md](https://developer.shopware.com/docs/products/paas/shopware/fundamentals/applications.md)  
# Applications

Shopware PaaS Native supports multiple applications within a project, such as environments for production, staging, or temporary feature testing.

Each application has its own compute resources, infrastructure, and deployment configuration, so you can tailor each environment to its specific needs.

For instance, you might allocate smaller, hibernating compute instances for staging while reserving larger, always-on resources for production.

## Creating an Application

Create a new application to a project:

```sh
sw-paas application create
```

## Build your application

To trigger a new build for the application via CLI, use the following command:

```sh
sw-paas application build start
```

This command initiates the build process, packaging your application and preparing it for deployment. While the build is running, you can monitor its progress and view real-time output by following the logs:

```sh
sw-paas application build logs
```

## Update your application

To update your application, you need to run the following command and provide the commit SHA:

```sh
sw-paas application update
```

This command initiates the build process, waits until it's done, and runs the deployment for you.

## Deploy a specific build of your application

To create a deployment with a specific build, use the following command:

```sh
sw-paas application deploy create
```

It will let you choose which build you want to deploy.
This is very handy, since you can choose any successful build to deploy: the latest one to bring your change live, or a previous one to fix an issue that arose.

## Deployments management

To list all past deployments:

```sh
sw-paas application deploy list
```

To get details about a given deployment:

```sh
sw-paas application deploy get
```

## Plugin Management

Plugin management is done [via Composer](../../../../guides/hosting/installation-updates/extension-managment#installing-extensions-with-composer) because the platform runs in a high-availability and clustered environment.

In such setups, local changes aren't feasible, as all instances must remain identical and stateless. This ensures consistency across all deployments.

### Using Privately Hosted Packages

To pull privately hosted Composer packages, you need to provide authentication credentials. Create a `COMPOSER_AUTH` secret using the CLI:

```sh
sw-paas vault create
```

Follow the prompts to enter your Composer authentication JSON as a `buildenv`. This secret will be used during builds to access private repositories.

## Executing Commands

Shopware PaaS Native provides two primary ways to run commands in your application environments via CLI: `exec` and `command`.

### `exec` Command

The `exec` command allows you to execute commands in a remote terminal session for your applications. This is useful for running commands directly on your application's environment, such as debugging, maintenance, or running one-off commands interactively.

```sh
sw-paas exec --new
```

This opens an interactive shell session inside your application's container.

#### Note

Please check the [known issues](../known-issues.md) regarding network considerations when running this command.

### `command` Command

The `command` command lets you create and manage commands that are executed in dedicated containers. This is particularly useful for CI/CD environments, asynchronous command execution, automated processes, or situations where you don't need to wait for command completion.

Unlike `exec`, which provides an interactive shell, `command` runs your specified command in a new, isolated container and does not require you to wait for its completion.

The default execution directory is `/var/www/html` and the container has a time-to-live (TTL) of 1 hour, so your command must complete within that timeframe.

```sh
sw-paas command create
```

For a complete list of available commands, refer to the [Shopware console commands documentation](https://docs.shopware.com/en/shopware-6-en/tutorials-and-faq/shopware-cli).

## Domain Management

### Shopware Domain

When you deploy an application for the first time, it automatically receives a complimentary `shopware.shop` domain. This allows you to access and test your application right away, even before setting up a custom domain.

The assigned domain is generated based on your application's name and unique identifier.

### Custom Domain

You can configure custom domains for your applications using the `sw-paas` CLI domain command. This allows you to attach multiple domains to a single application and route traffic through the Fastly CDN for optimal performance.

#### Creating Custom Domains

To create a custom domain for your application:

```sh
sw-paas domain create
```

Follow the prompts to specify your domain name and application. You can attach multiple domains to a single application.

#### DNS Configuration

After creating a custom domain, you must configure your DNS settings to point to the PaaS CDN endpoint:

**Configure your custom domain's DNS to point to:**

```dns
cdn.shopware.shop
```

This configuration ensures that all traffic to your custom domain is routed through the Fastly CDN for optimal performance and caching.

#### Application Deployment

Following domain creation, you must redeploy your application. You can do it by using:

```sh
sw-paas application deploy create
```

#### Shopware Configuration

Subsequently, you can configure the domain within Shopware and associate it with a storefront. Status update functionality is currently under development and should be considered a beta feature.

For more detailed information about CDN configuration and best practices, refer to the [CDN documentation](../cdn/index.md).

---

---

## Setting environment variables
**Source:** [products/paas/shopware/fundamentals/environment-variables.md](https://developer.shopware.com/docs/products/paas/shopware/fundamentals/environment-variables.md)  
# Setting environment variables

This page explains how to configure environment variables in Shopware PaaS Native.

Please only use this to configure non-sensitive environment variables. For sensitive variables, please use [secrets](./secrets.md). There is a detailed guide [here](../guides/secrets-vault-guide.md).

## Configure environment variables

Environment variables are defined in the `application.yaml` file, in the following array `app.environment_variables`.

Environment variables need to be scoped, they can be configured either for `RUN` or `BUILD`

| Scope      | Description                                           |
|------------|-------------------------------------------------------|
| `RUN`      | The value is passed to Shopware application (runtime) |
| `BUILD`    | Build-time environment variables                      |

Once the `application.yaml` is updated as usual, run the following:

```sh
sw-paas application update
```

## Configure an environment variable for runtime

Update the `application.yaml` file like this:

```yaml
app:
  environment_variables:
    - name: MY_RUNTIME_VARIABLE
      value: my-value
      scope: RUN
```

## Configure an environment variable for build-time

Update the `application.yaml` file like this:

```yaml
app:
  environment_variables:
    - name: MY_BUILDTIME_VARIABLE
      value: my-value
      scope: BUILD
```

## Complete example

Here is a full example of environment variables. They can be used for both build-time and runtime, and you can have multiple variables with the same name but different scopes.

```yaml
app:
  # ... Other application settings
  environment_variables:
    - name: MY_BUILDTIME_VARIABLE
      value: bar
      scope: BUILD
    - name: MY_RUNTIME_VARIABLE
      value: foo
      scope: RUN
    - name: MY_VARIABLE_WITH_THE_SAME_NAME
      value: my-value
      scope: RUN
    - name: MY_VARIABLE_WITH_THE_SAME_NAME
      value: my-value
      scope: BUILD
```

---

---

