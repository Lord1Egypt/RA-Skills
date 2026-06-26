# APP SYSTEM

Compiled excerpts from the Shopware Developer Documentation snapshot. Prefer live docs at [developer.shopware.com](https://developer.shopware.com/) when in doubt.

---

## Add custom flow actions
**Source:** [guides/plugins/apps/flow-builder/add-custom-flow-actions-from-app-system.md](https://developer.shopware.com/docs/v6.6/guides/plugins/apps/flow-builder/add-custom-flow-actions-from-app-system.md)  
# Add custom flow actions

::: info
Custom flow actions in Shopware Apps are available starting with Shopware 6.4.10.0 and are not supported in previous versions.
:::

Besides the default actions, developers can add custom, predefined, and configurable web hook actions to the flow builder.

![Custom flow action in Administration](../../../../assets/flow-builder-app-action-preview.png)

After reading, you will be able to

* Create the basic setup of an app
* Create custom actions for the flow builder
* Use custom actions to interact with third-party services

## Prerequisites

Please make sure you already have a working Shopware 6 store running (either cloud or self-hosted). Prior knowledge about the Flow Builder feature of Shopware 6 is useful.

Please see the [Flow Builder Concept](../../../../concepts/framework/flow-concept) for more information.

## Create the app wrapper

To get started with your app, create an `apps` folder inside the `custom` folder of your Shopware dev installation. In there, create another directory for your application and provide a `manifest.xml` file, following the structure below:

```text
└── custom
    ├── apps
    │   └── FlowBuilderActionApp
    │       └── Resources
    │           └── flow-action.xml
    │           └── app-icon.png
    │           └── slack-icon.png
    │       └── manifest.xml
    └── plugins
```

::: info
From 6.5.2.0, you can define the flow action in `flow.xml`. The `flow-action.xml` will be removed from 6.6.0.0.
:::

| File name | Description |
| :--- | :--- |
| FlowBuilderActionApp | Your app's technical name |
| app-icon.png | The app's icon |
| slack-icon.png | Your action icon will be defined for each action in the `flow-action.xml` file. (optional, icons will default to a fallback) |
| flow-action.xml | Place to define your new actions |
| manifest.xml | Base information about your app |

### Manifest file

The manifest file is the central point of your app. It defines the interface between your app and the Shopware instance. It provides all the information concerning your app, as seen in the minimal version below:

::: code-group

```xml [manifest.xml]
<?xml version="1.0" encoding="UTF-8"?>
<manifest xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://raw.githubusercontent.com/shopware/shopware/trunk/src/Core/Framework/App/Manifest/Schema/manifest-2.0.xsd">
    <meta>
        <name>FlowBuilderActionApp</name>
        <label>Flow Builder Action App</label>
        <label lang="de-DE">Flow Builder Aktions-App</label>
        <description>This is the example description for app</description>
        <description lang="de-DE">Dies ist die Beispielbeschreibung für app</description>
        <author>shopware AG</author>
        <copyright>(c) shopware AG</copyright>
        <version>4.14.0</version>
        <icon>Resources/app-icon.png</icon>
        <license>MIT</license>
    </meta>
</manifest>
```

:::

::: warning
The name of your app that you provide in the manifest file needs to match the folder name of your app.
:::

## Define the flow action

To create a flow action, you need to define a `<flow-action>` block within a file called `flow-action.xml`. Each `<flow-action>` represents one action and you can define an arbitrary number of actions.

```xml
// Resources/flow-action.xml
<flow-actions xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://raw.githubusercontent.com/shopware/shopware/trunk/src/Core/Framework/App/Flow/Schema/flow-1.0.xsd">
    <flow-action>
        ... # The first action
    </flow-action>
    <flow-action>
        ... # The second action
    </flow-action>
    <flow-action>
        ... # The third action
    </flow-action>
    ...
</flow-actions>
```

From 6.5.2.0, to create a flow action, you must define a `<flow-actions>` block within a file called `flow.xml`. Each `<flow-action>` in `<flow-actions>` represents one action, and you can define an arbitrary number of actions.

```xml
<flow-extensions xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://raw.githubusercontent.com/shopware/shopware/trunk/src/Core/Framework/App/Flow/Schema/flow-1.0.xsd">
    <flow-actions>
        <flow-action>
            ... # The first action
        </flow-action>
        <flow-action>
            ... # The second action
        </flow-action>
        <flow-action>
            ... # The third action
        </flow-action>
    </flow-actions>
    ...
</flow-extensions>
```

A single flow action would look like this:

```xml
<flow-action>
    <meta>
        <name>slackmessage</name>
        <label>Send slack message</label>
        <label lang="de-DE">Slack-Nachricht senden</label>
        <badge>Slack</badge>
        <description>Slack send message description</description>
        <description lang="de-DE">Dies ist die Beispielbeschreibung für app</description>
        <url>https://hooks.slack.com/services/{id}</url>
        <sw-icon>default-communication-speech-bubbles</sw-icon>
        <icon>slack.png</icon>
        <requirements>orderAware</requirements>
        <requirements>customerAware</requirements>
    </meta>
    ...
</flow-action>
```

| Key | Required | Description |
| :--- | :--- | :--- |
| name | yes | The technical name of your action, unique for all actions |
| label | yes | A name to be shown for your action in the actions list or action modal title |
| badge | no | An attached badge shown behind the label in the action modal title |
| description | yes | Detailed information for your action |
| sw-icon | no | An icon component name from the [icon library](https://component-library.shopware.com/icons/) |
| icon | no | Alternatively, a path to your action icon. In the case you define both `<sw-icon>` and `<icon>`, the `<icon>` will be take precedence in this case. |
| requirements | yes | Available action triggers, read more below |
| url | yes | External webhook location. Shopware will call this URL when the action is executed |

**requirements**

Requirements will decide for which trigger events your action is available.
Example: The `checkout.order.placed` has an `orderAware` requirements - indicating that your action is allow to use be used in the `checkout.order.placed` event. It is defined using `<requirements>orderAware</requirements>` in your app action definition.

For each value when you define, it'll represent one of the `aware` interfaces from the `core`.

To fulfill the requirements, refer to a subset of action triggers aware:

| Value | Interface |
| :--- | :--- |
| customerAware | Shopware\Core\Framework\Event\CustomerAware |
| customerGroupAware | Shopware\Core\Framework\Event\CustomerGroupAware |
| delayAware | Shopware\Core\Framework\Event\DelayAware |
| mailAware | Shopware\Core\Framework\Event\MailAware |
| orderAware | Shopware\Core\Framework\Event\OrderAware |
| salesChannelAware | Shopware\Core\Framework\Event\SalesChannelAware |
| userAware | Shopware\Core\Framework\Event\UserAware |

### Header parameters

```xml
<flow-action>
    <meta>
        ...
    </meta>
    <headers>
        <parameter type="string" name="content-type" value="application/json"/>
    </headers>
    ...
</flow-action>
```

| Key | Description |
| :--- | :--- |
| type | Parameter type - currently only `string` supported |
| name | The header key |
| value | The header value |

### Parameters

```xml
<flow-action>
    <meta>
        ...
    </meta>
    <headers>
        ...
    </headers>
    <parameters>
        <parameter type="string" name="text" value="{{ message }} \n Order Number: {{ order.orderNumber }}"/>
    </parameters>
    ...
</flow-action>
```

Define the `parameter` for the URL body based on your URL webhook services.

| Key | Description |
| :--- | :--- |
| type | Type of parameter, only support `string` type. |
| name | The body key for your URL. |
| value | The content message for your URL; free to design your content message here. |
| {{ message }} | The variable from your `<input-field>` defined in `flow-action.xml`. |
| {{ order.orderNumber }} | For each trigger event, the action will have the variables suitable. [Read more variables here](../../../../resources/references/app-reference/flow-action-reference). |

With the parameters configured like described above, an exemplary call of your Webhook Action could look like this:

```text
    POST https://hooks.slack.com/services/{id} {
        headers:
            content-type: application/json
        body:
            text: {{ message }} \n Order Number: {{ order.orderNumber }}
    }
```

### Action configuration

You can make your flow action configurable in the Administration by adding input fields. Based on your configuration - similar to the [app configurations](../../plugins/plugin-fundamentals/add-plugin-configuration) - you can later on use these configuration values within flow parameters.

```xml
<flow-action>
    <meta>
        ...
    </meta>
    <headers>
        ...
    </headers>
    <parameters>
        ...
    </parameters>
    <config>
        <input-field type="text">
            <name>message</name>
            <label>Message</label>
            <label lang="de-DE">Gegenstand</label>
            <place-holder>Placeholder</place-holder>
            <place-holder lang="de-DE">Platzhalter</place-holder>
            <required>true</required>
            <helpText>Help Text</helpText>
            <helpText lang="de-DE">Hilfstext</helpText>
        </input-field>
    </config>
</flow-action>
```

Available input field attributes:

| Key | Required |
| :--- | :--- |
| name | Yes |
| label | Yes |
| place-holder | No |
| required | No |
| helpText | No |

You assemble your configuration from a variety of input fields.

::: info
To get more information on how to create configuration forms, see [Plugin Configurations](../../plugins/plugin-fundamentals/add-plugin-configuration#the-different-types-of-input-field).
:::

| Type | Shopware component |
| :--- | :--- |
| text | `<sw-text-field/>` |
| textarea | `<sw-textarea-field/>` |
| text-editor | `<sw-text-editor/>` |
| url | `<sw-url-field/>` |
| password | `<sw-password-field/>` |
| int | `<sw-number-field/>` |
| float | `<sw-number-field/>`  |
| bool | `<sw-switch-field/>`  |
| checkbox | `<sw-checkbox-field/>`  |
| datetime | `<sw-datepicker/>`  |
| date | `<sw-datepicker/>` |
| time | `<sw-datepicker/>` |
| colorpicker | `<sw-colorpicker/>` |
| single-select | `<sw-single-select/>` |
| multi-select | `<sw-multi-select/>` |

## Install the App

The app can now be installed by running the following command:

```bash
bin/console app:install --activate FlowBuilderActionApp
```

## Further steps

* [Flow action example configuration](../../../../resources/references/app-reference/flow-action-reference) page
* [Schema definition for flow actions (GitHub)](https://github.com/shopware/shopware/blob/trunk/src/Core/Framework/App/Flow/Schema/flow-1.0.xsd)\`

---

---

## Add custom flow trigger
**Source:** [guides/plugins/apps/flow-builder/add-custom-flow-triggers-from-app-system.md](https://developer.shopware.com/docs/v6.6/guides/plugins/apps/flow-builder/add-custom-flow-triggers-from-app-system.md)  
# Add custom flow trigger

::: info
The Shopware app custom flow triggers are only accessible from 6.5.3.0 and later versions.
:::

In addition to the default triggers, you have the option to incorporate custom, pre-defined, and adjustable triggers into the flow builder.

![Custom flow trigger in Administration](../../../../assets/flow-builder-custom-trigger-preview.png)

After reading, you will be able to :

* Create the basic setup of an app.
* Create custom triggers for the flow builder.
* Use an API to interact with custom triggers.

## Prerequisites

Please ensure you have a working Shopware 6 store (either cloud or self-hosted). Prior knowledge about the Flow Builder feature of Shopware 6 is useful.

Please see the [Flow Builder Concept](../../../../concepts/framework/flow-concept) for more information.

## Create the app wrapper

To get started with your app, create an `apps` folder inside the `custom` folder of your Shopware dev installation. Next, create another directory inside for your application and provide a `manifest.xml` file following the structure below:

```text
└── custom
    ├── apps
    │   └── FlowBuilderTriggerApp
    │       └── Resources
    │           └── app
    │               └── administration
    │                   └── snippet
    │                       └── de-DE.json
    │                       └── en-GB.json
    │           └── flow.xml
    │       └── manifest.xml
    └── plugins
```

| File name             | Description                                        |
|:----------------------|:---------------------------------------------------|
| FlowBuilderTriggerApp | Your app's technical name                          |
| flow.xml              | Place to define your new triggers                  |
| de-DE.json            | Snippet to translate your trigger name for Deutsch |
| en-GB.json            | Snippet to translate your trigger name for English |
| manifest.xml          | Base information about your app                    |

### Manifest file

The manifest file is the central point of your app. It defines the interface between your app and the Shopware instance. It provides all the information concerning your app, as seen in the minimal version below:

::: code-group

```xml [manifest.xml]
<?xml version="1.0" encoding="UTF-8"?>
<manifest xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://raw.githubusercontent.com/shopware/shopware/trunk/src/Core/Framework/App/Manifest/Schema/manifest-2.0.xsd">
    <meta>
        <name>FlowBuilderTriggerApp</name>
        <label>Flow Builder Trigger App</label>
        <label lang="de-DE">Flow Builder Abzug-App</label>
        <description>This is the example description for app</description>
        <description lang="de-DE">Dies ist die Beispielbeschreibung für app</description>
        <author>shopware AG</author>
        <copyright>(c) shopware AG</copyright>
        <version>4.14.0</version>
        <icon>Resources/app-icon.png</icon>
        <license>MIT</license>
    </meta>
</manifest>
```

:::

::: warning
The name of your app that you provide in the manifest file needs to match the folder name of your app.
:::

## Define the flow trigger

To create a flow trigger, you need to define a `<flow-event>` block within a file called `flow.xml`. Each `<flow-event>` represents one trigger, and you can define an arbitrary number of events.

::: code-group

```xml [Resources/flow.xml]
<flow-extensions xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://raw.githubusercontent.com/shopware/shopware/trunk/src/Core/Framework/App/Flow/Schema/flow-1.0.xsd">
    <flow-events>
        <flow-event>
            ... # The first trigger
        </flow-event>
        <flow-event>
            ... # The second trigger
        </flow-event>
    </flow-events>
    ...
</flow-extensions>
```

:::

A single flow trigger would look like this:

```xml
<flow-event>
    <name>swag.before.open_the_doors</name>
    <aware>orderAware</aware>
</flow-event>
```

| Key          | Required | Description                                                 |
|:-------------|:---------|:------------------------------------------------------------|
| name         | yes      | The technical name of your trigger, unique for all actions. |
| aware        | no       | Filter actions for your trigger, read more below.           |

**aware**

The `aware` will decide which actions are available for your trigger.

***Example***

If you define the `orderAware` in your trigger config `<aware>orderAware</aware>`, the actions related to the Order will be available when the trigger is selected.

* action.add.order.tag,
* action.remove.order.tag,
* action.generate.document,
* action.grant.download.access,
* action.set.order.state,
* action.add.order.affiliate.and.campaign.code,
* action.set.order.custom.field,
* action.stop.flow

If you define the `customerAware` in your trigger config `<aware>orderAware</aware>`, the actions related to Customer will be available when the trigger is selected.

* action.add.customer.tag
* action.remove.customer.tag
* action.change.customer.group
* action.change.customer.status
* action.set.customer.custom.field
* action.add.customer.affiliate.and.campaign.code
* action.stop.flow

Each value defined, it represents one of the `aware` interfaces from the `core`.

To fulfill the `aware`, refer to a subset of action triggers aware:

| Value              | Interface                                        |
|:-------------------|:-------------------------------------------------|
| customerAware      | Shopware\Core\Framework\Event\CustomerAware      |
| customerGroupAware | Shopware\Core\Framework\Event\CustomerGroupAware |
| delayAware         | Shopware\Core\Framework\Event\DelayAware         |
| mailAware          | Shopware\Core\Framework\Event\MailAware          |
| orderAware         | Shopware\Core\Framework\Event\OrderAware         |
| salesChannelAware  | Shopware\Core\Framework\Event\SalesChannelAware  |
| userAware          | Shopware\Core\Framework\Event\UserAware          |

Please refer to the [Schema definition for flow events (GitHub)](https://github.com/shopware/shopware/blob/trunk/src/Core/Framework/App/Flow/Schema/flow-1.0.xsd) for more information.

## Trigger API

We provided an API with the endpoint `POST: /api/_action/trigger-event/{eventName}` to dispatch the custom trigger when you call the API.
The app calls the API to trigger the custom event and can provide the data. The API will create a CustomAppEvent object and dispatch it with the data provided.
The data given will be saved through `StorableFlow`. This can be utilized for actions or email templates.

Here is an example to define data from the API:

```json
    {
        "customerId": "d20e4d60e35e4afdb795c767eee08fec",
        "salesChannelId": "55cb094fd1794d489c63975a6b4b5b90",
        "shopName": "Shopware's Shop",
        "url": "https://shopware.com" 
    }
```

Flow actions can retrieve the data from FlowStorer.

```php
    $salesChanelId = $flow->getData(MailAware::SALES_CHANNEL_ID));
    $customer = $flow->getData(CustomerAware::CUSTOMER_ID));
```

Or we can use the data when defining the email template.

```html
    <h3>Welcome to {{ shopName }}</h3>
    <h1>Visit us at: {{ url }} </h1>
```

Please see the [StorableFlow Concept](../../../../resources/references/adr/2022-07-21-adding-the-storable-flow-to-implement-delay-action-in-flow-builder) for more information.

## Snippet for translation

You can define snippets to translate your custom trigger to show the trigger tree and flow list. Refer to the [Adding snippets](../../plugins/administration/adding-snippets) guide for more information.

Snippet keys should be defined based on your trigger name defined at `<name>` in your `flow.xml`.

| Fixed key            | Description                                                          |
|:---------------------|:---------------------------------------------------------------------|
| sw-flow-custom-event | All the keys related to the custom trigger will be defined inside    |
| event-tree           | All the keys used to trigger the tree will be defined inside         |
| flow-list            | All the keys used to flow list will be defined inside                |

***Example***

```xml
// Resources/flow.xml
<flow-extensions xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://raw.githubusercontent.com/shopware/shopware/trunk/src/Core/Framework/App/Flow/Schema/flow-1.0.xsd">
    <flow-events>
        <flow-event>
            <name>swag.before.open_the_doors</name>
            ...
        </flow-event>
    </flow-events>
</flow-extensions>
```

```javascript
// custom/apps/FlowBuilderTriggerApp/Resources/app/administration/snippet/en-GB.json
{
  "sw-flow-custom-event": {
    "event-tree": {
      "swag": "Swag",
      "before": "Before",
      "openTheDoors": "Open the doors"
    },
    "flow-list": {
      "swag_before_open_the_doors": "Before open the doors"
    }
  }
}
```

## Install the App

The app can now be installed by running the following command:

```bash
bin/console app:install --activate FlowBuilderTriggerApp
```

---

---

## Checkout Gateway
**Source:** [guides/plugins/apps/gateways/checkout/checkout-gateway.md](https://developer.shopware.com/docs/v6.6/guides/plugins/apps/gateways/checkout/checkout-gateway.md)  
# Checkout Gateway

## Context

As of Shopware version 6.6.3.0, the Checkout Gateway was introduced.

The Checkout Gateway aims to allow a streamlined implementation for making informed decisions during the checkout process, based on both the cart contents and the current sales channel context.
In particular, the app system benefits from this solution, enabling seamless communication and decision-making on the app server during the checkout.

While this documentation focuses on the app integration of the Checkout Gateway, the design is intended to allow a custom replacement solution via the plugin system."

## Prerequisites

You should be familiar with the concept of Apps, their registration flow as well as signing and verifying requests and responses between Shopware and the App backend server.

Your app server must be also accessible for the Shopware server.
You can use a tunneling service like [ngrok](https://ngrok.com/) for development.

## Manifest configuration

To indicate to Shopware that your app uses the checkout gateway, you must provide a `checkout` property inside a `gateways` parent property of your app's `manifest.xml`.

Below, you can see an example definition of a working checkout gateway configuration.

::: code-group

```xml [manifest.xml]
<?xml version="1.0" encoding="UTF-8"?>
<manifest>
    <!-- ... -->

    <gateways>
        <checkout>https://my-app.server.com/checkout/gateway</checkout>
    </gateways>
</manifest>
```

:::

After successful installation of your app, the checkout gateway will already be used during checkout.

## Checkout gateway endpoint

During checkout, Shopware checks for any active checkout gateways and will call the `checkout` url.
The app server will receive the current `SalesChannelContext`, `Cart`, and available payment and shipping methods as part of the payload.

::: warning
**Connection timeouts**

The Shopware shop will wait for a response for 5 seconds.
Be sure that your checkout gateway implementation on your app server responds in time, otherwise Shopware will time out and drop the connection.
:::

Your app server can then respond with a list of commands to manipulate the cart, payment methods, shipping methods, or add cart errors.

You can find a reference of all currently available commands [here](./command-reference.md).

Let's assume that your payment method is not available for carts with a total price above 1000€.

Request content is JSON

```json5
{
  "source": {
    "url": "http:\/\/localhost:8000",
    "shopId": "hRCw2xo1EDZnLco4",
    "appVersion": "1.0.0"
  },
  "cart": {
    //...
  },
  "salesChannelContext": {
    //...
  },
  "availablePaymentMethods": [
    "payment-method-technical-name-1",
    "payment-method-technical-name-2",
    // ...
  ],
  "availableShippingMethods": [
    "shipping-method-technical-name-1",
    "shipping-method-technical-name-2",
    // ...
  ]
}
```

And your response could look like this:

```json5
{
  "commands": [
    {
      "command": "remove-payment-method",
      "payload": {
        "paymentMethodTechnicalName": "payment-myApp-payment-method"
      }
    },
    {
      "command": "add-cart-error",
      "payload": {
        "message": "Payment method 'My App Payment Method' is not available for carts > 1000€.",
        "blocking": false,
        "level": 10,
      }
    }
  ]
}
```

With version `3.0.0`, support for the checkout gateway has been added to the `app-php-sdk`.
The SDK will handle the communication with the Shopware shop and provide you with a convenient way to handle the incoming payload and respond with the necessary commands.

```php
<?php declare(strict_types=1);

use Psr\Http\Message\RequestInterface;
use Psr\Http\Message\ResponseInterface;
use Shopware\App\SDK\Context\Cart\Error;
use Shopware\App\SDK\Context\ContextResolver;
use Shopware\App\SDK\Framework\Collection;
use Shopware\App\SDK\Gateway\Checkout\CheckoutGatewayCommand;
use Shopware\App\SDK\Gateway\Checkout\Command\AddCartErrorCommand;
use Shopware\App\SDK\Gateway\Checkout\Command\RemovePaymentMethodCommand;
use Shopware\App\SDK\Response\GatewayResponse;
use Shopware\App\SDK\Shop\ShopResolver;

function gatewayController(RequestInterface $request): ResponseInterface
{
    // injected or build by yourself
    $shopResolver = new ShopResolver($repository);
    $contextResolver = new ContextResolver();
    $signer = new ResponseSigner();
    
    $shop = $shopResolver->resolveShop($request);
    
    /** @var Shopware\App\SDK\Context\Gateway\Checkout\CheckoutGatewayAction $action */
    $action = $contextResolver->assembleCheckoutGatewayRequest($request, $shop);

    /** @var Collection<Shopware\App\SDK\Gateway\Checkout\CheckoutGatewayCommand> $commands */
    $commands = new Collection();

    if ($action->paymentMethods->has('payment-myApp-payment-method')) {
        if ($action->cart->getPrice()->getTotalPrice() > 1000) {
            $commands->add(new RemovePaymentMethodCommand('payment-myApp-payment-method'));
            $commands->add(new AddCartErrorCommand('Payment method \'My App Payment Method\' is not available for carts > 1000€.', false, Error::LEVEL_WARNING));
        }
    }

    $response = GatewayResponse::createCheckoutGatewayResponse($commands);

    return $signer->sign($response);
}
```

```php
<?php declare(strict_types=1);

namespace App\Controller;

use Shopware\App\SDK\Context\Cart\Error;
use Shopware\App\SDK\Context\Gateway\Checkout\CheckoutGatewayAction;
use Shopware\App\SDK\Framework\Collection;
use Shopware\App\SDK\Gateway\Checkout\CheckoutGatewayCommand;
use Shopware\App\SDK\Gateway\Checkout\Command\AddCartErrorCommand;
use Shopware\App\SDK\Response\GatewayResponse;
use Symfony\Bridge\PsrHttpMessage\HttpFoundationFactoryInterface;
use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\Routing\Attribute\Route;

#[Route('/api/gateway', name: 'api.gateway.')]
class GatewayController extends AbstractController
{
    public function __construct(
        private readonly HttpFoundationFactoryInterface $httpFoundationFactory
    ) {
    }

    #[Route('/checkout', name: 'checkout', methods: ['POST'])]
    public function checkout(CheckoutGatewayAction $action): Response
    {
        /** @var Collection<CheckoutGatewayCommand> $commands */
        $commands = new Collection();

        if ($action->paymentMethods->has('payment-myApp-payment-method')) {
            if ($action->cart->getPrice()->getTotalPrice() > 1000) {
                $commands->add(new RemovePaymentMethodCommand('payment-myApp-payment-method'));
                $commands->add(new AddCartErrorCommand('Payment method \'My App Payment Method\' is not available for carts > 1000€.', false, Error::LEVEL_WARNING));
            }
        }

        $response = GatewayResponse::createCheckoutGatewayResponse($commands);

        return $this->httpFoundationFactory->createResponse($response);
    }
}
```

## Event

Plugins can listen to the `Shopware\Core\Checkout\Gateway\Command\Event\CheckoutGatewayCommandsCollectedEvent`.
This event is dispatched after the Checkout Gateway has collected all commands from all app servers.
It allows plugins to manipulate the commands before they are executed, based on the same payload the app servers retrieved.

---

---

## Checkout Gateway Command Reference
**Source:** [guides/plugins/apps/gateways/checkout/command-reference.md](https://developer.shopware.com/docs/v6.6/guides/plugins/apps/gateways/checkout/command-reference.md)  
# Checkout Gateway Command Reference

| Command                  | Description                                                                                                                                                  | Payload                                                        | Since   |
|:-------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------|:---------------------------------------------------------------|:--------|
| `remove-payment-method`  | Removes a payment method from the available payment methods.                                                                                                 | `{"paymentMethodTechnicalName": "string"}`                     | 6.6.3.0 |
| `remove-shipping-method` | Removes a shipping method from the available shipping methods.                                                                                               | `{"shippingMethodTechnicalName": "string"}`                    | 6.6.3.0 |
| `add-cart-error`         | Adds an error to the cart. The level decides the severity of the cart error flash message. Blocking decides, whether to block the checkout for the customer. | `{"message": "string", "level": "int", "blocking": "boolean"}` | 6.6.3.0 |

---

---

## Context Gateway Command Reference
**Source:** [guides/plugins/apps/gateways/context/command-reference.md](https://developer.shopware.com/docs/guides/plugins/apps/gateways/context/command-reference.md)  
# Context Gateway Command Reference

## Available commands

| Command                            | Description                                                                                           | Payload                                                 | Since   |
|:-----------------------------------|:------------------------------------------------------------------------------------------------------|:--------------------------------------------------------|:--------|
| `context_add-customer-message`     | Adds an error message to be displayed to the customer in the Storefront via FlashBag messages.        | `{"message": "string"}`                                 | 6.7.1.0 |
| `context_change-billing-address`   | Changes the billing address of a customer to the specified address ID.                                | `{"addressId": "string"}`                               | 6.7.1.0 |
| `context_change-shipping-address`  | Changes the shipping address of a customer to the specified address ID.                               | `{"addressId": "string"}`                               | 6.7.1.0 |
| `context_change-currency`          | Changes the active currency for a customer to the currency with the specified ISO 4217 currency code. | `{"iso": "string"}`                                     | 6.7.1.0 |
| `context_change-language`          | Changes the active language for a customer to the language with the specified BCP 47 language tag.    | `{"iso": "string"}`                                     | 6.7.1.0 |
| `context_change-payment-method`    | Changes the active payment method for a customer to the method with the specified technical name.     | `{"technicalName": "string"}`                           | 6.7.1.0 |
| `context_change-shipping-method`   | Changes the active shipping method for a customer to the method with the specified technical name.    | `{"technicalName": "string"}`                           | 6.7.1.0 |
| `context_change-shipping-location` | Changes the active shipping location for a customer to the specified country / country state.         | `{"countryIso": "string", "countryStateIso": "string"}` | 6.7.1.0 |
| `context_login-customer`           | Logs in an existing customer with the specified email.                                                | `{"customerEmail": "string"}`                           | 6.7.1.0 |
| `context_register-customer`        | Register a new customer with the specified data and log them in.                                      | `{"data": "object (s. RegisterCustomerCommand)"}`       | 6.7.1.0 |

## Available data for RegisterCustomerCommand

These properties are available to set in the custom `data` object of the `context_register-customer` command.

| Field                    | Type   | Required                  | Description                                                                                                                   |
|:-------------------------|:-------|:--------------------------|-------------------------------------------------------------------------------------------------------------------------------|
| `title`                  | string |                           | The title of the customer, e.g. "Mr." or "Mrs."                                                                               |
| `accountType`            | string |                           | The type of account, either "private" or "business"                                                                           |
| `firstName`              | string | Yes                       | The first name of the customer                                                                                                |
| `lastName`               | string | Yes                       | The last name of the customer                                                                                                 |
| `email`                  | string | Yes                       | The email address of the customer                                                                                             |
| `salutationId`           | string |                           | The ID of the salutation to use for the customer                                                                              |
| `guest`                  | bool   |                           | Whether the customer is a guest (default: true)                                                                               |
| `storefrontUrl`          | string | Yes                       | The storefront URL of the sales channel (You find available domains in the sales channel context -> sales channel -> domains) |
| `requestedGroupId`       | string |                           | The ID of the customer group to assign to the customer                                                                        |
| `affiliateCode`          | string |                           | The affiliate code to assign to the customer                                                                                  |
| `campaignCode`           | string |                           | The campaign code to assign to the customer                                                                                   |
| `birthdayDay`            | int    |                           | The day of the customer's birthday                                                                                            |
| `birthdayMonth`          | int    |                           | The month of the customer's birthday                                                                                          |
| `birthdayYear`           | int    |                           | The year of the customer's birthday                                                                                           |
| `password`               | string | (for non-guest customers) | The password for the customer (plain text, will be hashed by the shop before stored)                                              |
| `billingAddress`         | object | Yes                       | The billing address of the customer, s. `AddressResponseStruct` for available fields                                          |
| `shippingAddress`        | object |                           | The shipping address of the customer, s. `AddressResponseStruct` for available fields                                         |
| `vatIds`                 | array  |                           | An array of VAT IDs for the customer                                                                                          |
| `acceptedDataProtection` | bool   |                           | Whether the customer has accepted the data protection policy (default: false)                                                 |

### AddressResponseStruct

This structure is used for the `billingAddress` and `shippingAddress` fields in the `RegisterCustomerCommand`.

| Field                    | Type   | Required | Description                                           |
|:-------------------------|:-------|:---------|:------------------------------------------------------|
| `title`                  | string |          | The title of the address, e.g. "Mr." or "Mrs."        |
| `firstName`              | string | Yes      | The first name of the address owner                   |
| `lastName`               | string | Yes      | The last name of the address owner                    |
| `salutationId`           | string |          | The ID of the salutation to use for the address owner |
| `street`                 | string | Yes      | The street of the address                             |
| `zipcode`                | string | Yes      | The ZIP code of the address                           |
| `city`                   | string | Yes      | The city of the address                               |
| `company`                | string |          | The company name for the address                      |
| `department`             | string |          | The department name for the address                   |
| `countryStateId`         | string |          | The ID of the country state for the address           |
| `countryId`              | string | Yes      | The ID of the country for the address                 |
| `additionalAddressLine1` | string |          | Additional address line 1                             |
| `additionalAddressLine2` | string |          | Additional address line 2                             |
| `phoneNumber`            | string |          | The phone number for the address                      |

---

---

## Context Gateway
**Source:** [guides/plugins/apps/gateways/context/context-gateway.md](https://developer.shopware.com/docs/guides/plugins/apps/gateways/context/context-gateway.md)  
# Context Gateway

::: danger
**Security and privacy**

With the Context Gateway, Shopware allows your app to manipulate the customer context, which includes sensitive information like customer addresses, payment methods, and more.
It is your responsibility to ensure that the commands are valid and do not compromise the security or privacy of customers.

Due to the powerful nature of this feature, it should only be used if your app server is properly secured and the commands it sends are fully trusted and validated.

:::

## Context

As of Shopware version 6.7.1.0, the Context Gateway has been introduced.

The Context Gateway is a powerful feature that enables apps to securely access and interact with the customer context — based on the current cart and sales channel — allowing for more informed decision-making on the app server.
This enhancement empowers app developers to dynamically tailor the shopping experience by manipulating the customer context.

It serves as the bridge between your app’s JavaScript and your app server.

## Prerequisites

You should be familiar with the concept of Apps, their registration flow as well as signing and verifying requests and responses between Shopware and the App backend server.

Your app server must also be accessible to the Shopware server.
You can use a tunneling service like [ngrok](https://ngrok.com/) for development.

## Manifest configuration

To indicate to Shopware that your app uses the context gateway, you must provide a `context` property inside a `gateways` parent property of your app's `manifest.xml`.

Below, you can see an example definition of a working checkout gateway configuration.

::: code-group

```xml [manifest.xml]
<?xml version="1.0" encoding="UTF-8"?>
<manifest>
    <!-- ... -->

    <gateways>
        <!-- ... -->
        <context>https://my-app.server.com/context/gateway</context>
    </gateways>
</manifest>
```

:::

After the successful installation of your app, the context gateway is ready to be called by Shopware.

## Context Gateway Endpoint

To trigger the context gateway, your integration can call the additional Store API route: `store-api.context.gateway`.
This endpoint will forward the request to your app server’s context gateway endpoint, which must be [configured in your app's manifest](#manifest-configuration).

To allow the shop to identify your app, the request must include the `appName`, which is defined in your [app’s `manifest.xml`](../../app-base-guide.md#manifest-file).

Your app server will receive the following payload:

* The request source, including:
  * The URL of the Shopware shop
  * The Shop ID
  * The app version
  * Any active [in-app purchase](../../in-app-purchases).
* The current `SalesChannelContext`
* The current `Cart`
* Any custom data you include in the request body

::: info

Communication between Shopware and your app server is secured via the [app signature verification mechanism](../../app-signature-verification), ensuring that only your app server can respond to context gateway requests.

:::

### Storefront Integration

To trigger the context gateway from the Storefront, use the `frontend.gateway.context` endpoint. This route is automatically registered by Shopware.

You can include any custom data in the request body - Shopware will forward this data to your app server.

To simplify this integration, Shopware provides the `ContextGatewayClient` service.
This JavaScript client is intended for use within your app and handles communication with the context gateway endpoint.
It returns a response containing:

* A (new) context token
* An optional redirect URL

Here is an example JavaScript plugin that triggers the context gateway when a button is clicked in the Storefront:

::: code-group

```javascript [context-gateway.js]
import Plugin from 'src/plugin-system/plugin.class';
import ContextGatewayClient from 'src/service/context-gateway-client.service';

export default class MyPlugin extends Plugin {
  init() {
    this._registerEvents();
  }

  _registerEvents() {
    this.el.addEventListener('click', this._onClick.bind(this));
  }

  async _onClick() {
    // create client with your app name
    const gatewayClient = new ContextGatewayClient('myAppName');

    // call the gateway with optional custom data
    const tokenResponse = await gatewayClient.call({ some: 'data', someMore: 'data' });

    // either: you can work with the new token or redirect URL
    // this means you have to handle the navigation yourself, e.g. reloading the page or redirecting to the URL
    const token = tokenResponse.token;
    const redirectUrl = tokenResponse.redirectUrl;

    // or: if you want shopware to handle the navigation automatically, even supplying an optional custom target path is possible
    await gatewayClient.navigate(tokenResponse, '/custom/target/path');
  }
}
```

:::

::: info
**Navigation `customTarget` Behavior**

The `customTarget` parameter allows you to optionally control the redirect path used by the `navigate` method.

* If `customTarget` is an **absolute path** (starts with `/`), it completely replaces the path portion of the `redirectUrl`.
  This can be used to override sales channel sub-paths in the `redirectUrl`.
  *Example:* `https://example.com/en` → `https://example.com/custom/target/path`

* If `customTarget` is a **relative path**, it is appended to the existing path of the `redirectUrl`.

* If `customTarget` is `null`, the behavior depends on whether a `redirectUrl` is present:
  * If present: the `redirectUrl` is used as-is.
  * If not: the current page is reloaded to apply context changes.

Trailing slashes are automatically removed to ensure clean and consistent URLs.
:::

### App server response

::: warning
**Connection timeouts**

The Shopware shop will wait for a response for 5 seconds.
Be sure that your context gateway implementation on your app server responds in time, otherwise Shopware will time out and drop the connection.
:::

Your app server can respond with a list of commands to modify the current sales channel context.
These commands can be used to perform actions such as:

* Changing aspects of the customer context, like:
  * Changing the active currency
  * Changing the active language and more
* Registering a new customer
* Logging in an existing customer

You can find a complete reference of all available commands in the [command reference](./command-reference.md).

For example, you might want to update the context to a different currency and language if the current currency is not GBP.

Request content is JSON

```json5
{
  "source": {
    "url": "http:\/\/localhost:8000",
    "shopId": "hRCw2xo1EDZnLco4",
    "appVersion": "1.0.0"
  },
  "cart": {
    //...
  },
  "salesChannelContext": {
    //...
  },
  "data": {
    "your": "custom data",
    "appears": "here"
  }
}
```

And your response could look like this:

```json5
{
  "commands": [
    {
      "command": "context_change-currency",
      "payload": {
        "iso": "GBP"
      }
    },
    {
      "command": "context_change-language",
      "payload": {
        "iso": "en-GB",
      }
    }
  ]
}
```

With version `4.1.0`, support for the context gateway has been added to the `app-php-sdk`.
The SDK will handle the communication with the Shopware shop and provide you with a convenient way to handle the incoming payload and respond with the necessary commands.

```php
<?php declare(strict_types=1);

use Psr\Http\Message\RequestInterface;
use Psr\Http\Message\ResponseInterface;
use Shopware\App\SDK\Context\Cart\Error;
use Shopware\App\SDK\Context\ContextResolver;
use Shopware\App\SDK\Framework\Collection;
use Shopware\App\SDK\Gateway\Context\ContextGatewayCommand;
use Shopware\App\SDK\Gateway\Context\Command\ChangeCurrencyCommand;
use Shopware\App\SDK\Gateway\Context\Command\ChangeLanguageCommand;
use Shopware\App\SDK\Response\GatewayResponse;
use Shopware\App\SDK\Shop\ShopResolver;

function gatewayController(RequestInterface $request): ResponseInterface
{
    // injected or build by yourself
    $shopResolver = new ShopResolver($repository);
    $contextResolver = new ContextResolver();
    $signer = new ResponseSigner();

    $shop = $shopResolver->resolveShop($request);

    /** @var Shopware\App\SDK\Context\Gateway\Context\ContextGatewayAction $action */
    $action = $contextResolver->assembleContextGatewayRequest($request, $shop);

    /** @var Collection<Shopware\App\SDK\Gateway\Context\ContextGatewayCommand> $commands */
    $commands = new Collection();

    if ($action->getSalesChannelContext()->getCurrency()->getIsoCode() !== 'GBP') {
        $commands->add(new ChangeCurrencyCommand('GBP'));
        $commands->add(new ChangeLanguageCommand('en-GB'));
    }

    $response = GatewayResponse::createContextGatewayResponse($commands);

    return $signer->sign($response);
}
```

```php
<?php declare(strict_types=1);

namespace App\Controller;

use Shopware\App\SDK\Context\Cart\Error;
use Shopware\App\SDK\Context\Gateway\Context\ContextGatewayAction;
use Shopware\App\SDK\Framework\Collection;
use Shopware\App\SDK\Gateway\Context\Command\ChangeCurrencyCommand;
use Shopware\App\SDK\Gateway\Context\Command\ChangeLanguageCommand;
use Shopware\App\SDK\Response\GatewayResponse;
use Symfony\Bridge\PsrHttpMessage\HttpFoundationFactoryInterface;
use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\Routing\Attribute\Route;

#[Route('/api/gateway', name: 'api.gateway.')]
class GatewayController extends AbstractController
{
    public function __construct(
        private readonly HttpFoundationFactoryInterface $httpFoundationFactory
    ) {
    }

    #[Route('/context', name: 'context', methods: ['POST'])]
    public function context(ContextGatewayAction $action): Response
    {
        /** @var Collection<ContextGatewayCommand> $commands */
        $commands = new Collection();

        if ($action->getSalesChannelContext()->getCurrency()->getIsoCode() !== 'GBP') {
            $commands->add(new ChangeCurrencyCommand('GBP'));
            $commands->add(new ChangeLanguageCommand('en-GB'));
        }

        $response = GatewayResponse::createContextGatewayResponse($commands);

        return $this->httpFoundationFactory->createResponse($response);
    }
}
```

### Command Validation

Shopware performs basic validation on the commands returned by your app server to ensure they are reasonable to execute.

The following checks are enforced:

* The command must be recognized as valid, e.g. `context_change-currency`. See the full list of available [commands](./command-reference.md#available-commands).
* The payload must be valid for the respective command type.
* Only **one command per type** is allowed. For example, you cannot include two `context_change-currency` commands in a single response.
* A maximum of **one `context_register-customer` or `context_login-customer`** command is allowed per response.

## Event

Plugins can listen to the `Shopware\Core\Framework\Gateway\Context\Command\Event\ContextGatewayCommandsCollectedEvent`.
This event is dispatched after all commands have been collected from the app server and allow plugins to modify or add commands based on the same payload the app received.

## Special Considerations

* The `context_login-customer` command allows your app to log in a customer **without requiring their password**.
  Use this feature with caution to uphold the shop’s security and privacy standards.

* The `context_register-customer` command will create a new customer account and **automatically log them in**.
  Make sure to validate the provided data before issuing this command.
  See the [RegisterCustomerCommand reference](./command-reference.md#available-data-for-registercustomercommand) for the list of accepted fields.

In both cases, your app must ensure that the customer has **explicitly consented** to be registered or logged in.

---

---

## In-App Purchase Gateway
**Source:** [guides/plugins/apps/gateways/in-app-purchase/in-app-purchase-gateway.md](https://developer.shopware.com/docs/v6.6/guides/plugins/apps/gateways/in-app-purchase/in-app-purchase-gateway.md)  
# In-App Purchase Gateway

## Context

::: info
In-App Purchase is available since Shopware version 6.6.9.0
:::

In-App Purchase Gateway was introduced to enhance flexibility in managing In-App Purchases.

The gateway enables app servers to restrict specific In-App Purchases based on advanced decision-making processes handled on the app server side.

::: info
**Current Limitations:**\
At present, the In-App Purchase Gateway supports only restricting the checkout process for new In-App Purchases.\
**Plans:**\
We aim to expand its functionality to include filtering entire lists of In-App Purchases before they are displayed to users.
:::

## Prerequisites

You should be familiar with the concept of Apps, their registration flow as well as signing and verifying requests and responses between Shopware and the App backend server.

Your app server must be also accessible for the Shopware server.
You can use a tunneling service like [ngrok](https://ngrok.com/) for development.

## Manifest Configuration

To indicate that your app leverages the In-App Purchase Gateway, include the `inAppPurchase` property within the `gateways` property in your app's `manifest.xml`.

Below is an example of a properly configured manifest snippet for enabling the checkout gateway:

```xml [manifest.xml]
<?xml version="1.0" encoding="UTF-8"?>
<manifest>
    <!-- ... -->

    <gateways>
        <inAppPurchases>https://my-app.server.com/inAppPurchases/gateway</inAppPurchases>
    </gateways>
</manifest>
```

After successful installation of your app, the In-App Purchases gateway will already be used.

## In-App Purchases gateway endpoint

During checkout of an In-App Purchase, Shopware checks for any active In-App Purchases gateways and will call the `inAppPurchases` url.
The app server will receive a list containing the single only In-App Purchase the user wants to buy as part of the payload.

::: warning
**Connection timeouts**

The Shopware shop will wait for a response for 5 seconds.
Be sure that your In-App Purchases gateway implementation on your app server responds in time,
otherwise Shopware will time out and drop the connection.
:::

Request content is JSON

```json5
{
  "source": {
    "url": "http:\/\/localhost:8000",
    "shopId": "hRCw2xo1EDZnLco4",
    "appVersion": "1.0.0",
    "inAppPurchases": "eyJWTEncodedTokenOfActiveInAppPurchases"
  },
  "purchases": [
    "my-in-app-purchase-bronze",
    "my-in-app-purchase-silver",
    "my-in-app-purchase-gold",
  ],
}
```

Respond with the In-App Purchases you want the user to be allowed to buy by simply responding with the purchase identifier in the `purchases` array.
During checkout, respond with an empty array to disallow the user from buying the In-App Purchase.

```json5
{
  "purchases": [
    "my-in-app-purchase-bronze",
    "my-in-app-purchase-silver",
    // disallow the user from buying the gold in-app purchase by removing it from the response
  ]
}
```

With version `4.0.0`, support for the In-App Purchases gateway has been added to the `app-php-sdk`.
The SDK will handle the communication with the Shopware shop and provide you with a convenient way to handle the incoming payload and respond with the necessary purchases.

```php

use Psr\Http\Message\RequestInterface;
use Psr\Http\Message\ResponseInterface;
use Shopware\App\SDK\Authentication\ResponseSigner;
use Shopware\App\SDK\Context\Cart\Error;
use Shopware\App\SDK\Context\ContextResolver;
use Shopware\App\SDK\Context\InAppPurchase\InAppPurchaseProvider;
use Shopware\App\SDK\Framework\Collection;
use Shopware\App\SDK\HttpClient\ClientFactory;
use Shopware\App\SDK\Response\InAppPurchaseResponse;
use Shopware\App\SDK\Shop\ShopResolver;

function inAppPurchasesController(): ResponseInterface {
    // injected or build by yourself
    $shopResolver = new ShopResolver($repository);
    $signer = new ResponseSigner();
    
    $shop = $shopResolver->resolveShop($request);

    $inAppPurchaseProvider = new InAppPurchaseProvider(new SBPStoreKeyFetcher(
        (new ClientFactory())->createClient($shop)
    ));
    
    $contextResolver = new ContextResolver($inAppPurchaseProvider);
    
    /** @var Shopware\App\SDK\Context\Gateway\InAppFeatures\FilterAction $action */
    $action = $contextResolver->assembleInAppPurchasesFilterRequest($request, $shop);
    
    /** @var Shopware\App\SDK\Framework\Collection $purchases */
    $purchases = $action->getPurchases();
    
    // filter the purchases based on your business logic
    $purchases->remove('my-in-app-purchase-gold');
    
    $response = InAppPurchasesResponse::filter($purchases);
    
    return $signer->sign($response);
}
```

```php
<?php declare(strict_types=1);

namespace App\Controller;

use Shopware\App\SDK\Context\Cart\Error;
use Shopware\App\SDK\Context\Gateway\InAppFeatures\FilterAction;
use Shopware\App\SDK\Framework\Collection;
use Shopware\App\SDK\Gateway\Checkout\CheckoutGatewayCommand;
use Shopware\App\SDK\Gateway\Checkout\Command\AddCartErrorCommand;
use Shopware\App\SDK\Response\GatewayResponse;
use Symfony\Bridge\PsrHttpMessage\HttpFoundationFactoryInterface;
use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\Routing\Attribute\Route;

#[Route('/api/gateway', name: 'api.gateway.')]
class GatewayController extends AbstractController
{
    public function __construct(
        private readonly HttpFoundationFactoryInterface $httpFoundationFactory
    ) {
    }

    #[Route('/inAppPurchases', name: 'in-app-purchases', methods: ['POST'])]
    public function inAppPurchases(FilterAction $action): Response
    {
        // the user already has the best premium purchase
        // disallow him from buying the less premium ones
        if ($action->source->inAppPurchases->has('my-in-app-purchase-gold')) {
            $action->purchases->remove('my-in-app-purchase-bronze');
            $action->purchases->remove('my-in-app-purchase-silver');
        }

        $response = GatewayResponse::createCheckoutGatewayResponse($commands);

        return $this->httpFoundationFactory->createResponse($response);
    }
}
```

## Event

Plugins can listen to the `Shopware\Core\Framework\App\InAppPurchases\Event\InAppPurchasesGatewayEvent`.
This event is dispatched after the In-App Purchases Gateway has received the app server response.
It allows plugins to manipulate the available In-App Purchases, based on the same payload the app servers retrieved.

---

---

## Hosting your App
**Source:** [guides/plugins/apps/hosting-guide.md](https://developer.shopware.com/docs/v6.4/guides/plugins/apps/hosting-guide.md)  
# Hosting your App

When you plan to build an app, there will come a point when you have to consider which kinds of server infrastructure you will need. This article is a starting point, so you can investigate further and make an informed decision.

## Does your app need hosting

Not all apps need hosting. If your app requires a server depends on the kinds of functionalities that it uses.

* **Features that require a server**
  * [Custom Modules](../administration/add-custom-modules)
  * [Action Buttons](../administration/add-custom-action-button)
  * [Webhooks](../app-base-guide#webhooks)
  * [Payment Processing](../payment)
* **Features that work without a server**
  * [Themes](../storefront/apps-as-themes)
  * [Template changes](../storefront/)
  * [CMS Blocks](../content/cms/add-custom-cms-blocks)
  * [App configuration](../configuration)

## Hosting options

Modern server providers offer several ways to host web based applications. Booking such a hosting is often tied to different tiers of resources available to you. These are generally measured in units like the amount of virtual CPUs and gigabytes of RAM and billing intervals are per millisecond, hour or month. Here are the most common options starting with the most labor-intensive.

### Dedicated server

A dedicated server is a classic way to host performance critical applications. With this model, you rent one or several pieces of hardware from your provider. This is cheaper if your order compute and memory resources in bulk. But this model also has the drawback of high management overhead. With a dedicated server, you are responsible for the operating system and software upgrades, as well as backups.

### Infrastructure as a Service

So-called IaaS providers provide a solid layer of abstraction over dedicated hosting solutions. With an IaaS model, you are no longer forced to rent physical pieces of hardware but rather virtual machines with configurable amounts of computing power and memory. Another improvement is the availability of so-called managed services, like databases, object storage, and queues. These services allow you to off-load maintenance, backups, and availability to the cloud provider so that you can concentrate on using these services.

Be aware that even though IaaS solutions massively reduce the amount of application management, it still requires you to keep an overview of your servers and services and how they are networked together.

### Platform as a Service

The next step in abstraction is the PaaS providers. They allow you to declare the resources you need in a few configuration files. Once the config is set up, they take care of getting your code up and running on their infrastructure. They not only provide managed services like databases for you, they also help with deploying your application and creating several environments for production, staging, and testing use. Many PaaS providers use git to integrate directly with development workflows. This is also in contrast to IaaS providers where it is your
responsibility to provide deployables.

### Serverless

Serverless services, also called function as a service, provide the most elastic way to scale your application. A serverless solution treats your application code as a function that is called with some input parameters. In the case of a web application, the "function" takes a HTTP request and returns a response that is then passed to the client.

This is reflected by the way serverless solutions often directly take source code and then take care of distributing it. This makes serverless applications very scalable due to the fact that the service provider takes care to boot a runtime for your code and as many parallel runtimes as are necessary to handle large loads. This approach abstracts away any notion of reserved resources, billing is handled by the millisecond, hence the name serverless.

This makes this approach the easiest to get started quickly, at least in theory. Keep in mind that in real world applications, things like databases even as managed services, are still often modeled as reserved resources. Also, it is necessary to take care of a dedicated entry point to map incoming requests to the function as a service model.

This is where tools like ["Serverless Framework"](https://serverless.com/) come into play to help you. It allows you to manage the lifecycle of your serverless application in many languages and on all big FaaS providers. It is optimized to be used with continuous integration, allowing for automated deployments.

## Pricing

To give you an example of the potential costs of hosting an app we have provided the following example calculation:

Let's assume your app is a PHP application on platform.sh, and it generates a revenue of 5$ per user per month. This means that with 50 users, that app makes 205$ a month. A standard plan on platform.sh costs 50$ a month and provides 0.96 vCPU and 0.8 GB of RAM. According to the [symfony benchmark](http://www.phpbenchmarks.com/en/benchmark/symfony/5.0) a REST API built with Symfony can handle about 6000req/s on a machine with 32 GB RAM and 32GB of RAM. So considering a real world application is between 5 and 10 times slower than the benchmark, it leaves the standard plan to handle roughly between 50-100req/s or about one request per user every second.

Keep in mind, though, that this example is a very theoretical calculation. How much computational power your app needs is specific to the kinds of work it does and its tech stack. But we hope it provides some orientation.

---

---

## Platform.sh Deployment
**Source:** [guides/plugins/apps/hosting-guide/platform-sh-deployment.md](https://developer.shopware.com/docs/v6.4/guides/plugins/apps/hosting-guide/platform-sh-deployment.md)  
# Platform.sh Deployment

## Overview

[Platform.sh](https://platform.sh) is a powerful hosting provider for your infrastructure that's quite easy to use.

Keep in mind, though, that this is **not** the only way to go for apps. You can, of course, use different services, providers or host everything on a dedicated machine. This guide explains to you how to get started for hosting an app on Platform.sh.

Know more about hosting from the [hosting guide](../hosting-guide/index.md) and from the [official documentation](https://docs.platform.sh/).

## Getting started

To deploy your app on [Platform.sh](https://platform.sh), just follow those instructions:

* [Source Integrations](https://docs.platform.sh/integrations/source.html)
* [Private Git repository](https://docs.platform.sh/development/private-repository.html)
* [Using the Platform.sh CLI](https://docs.platform.sh/development/cli.html)

## Most important steps

1. Configure your [Source Integrations](https://docs.platform.sh/integrations/source.html) (Optional, but highly recommended!)
2. Install the [Platform.sh CLI](https://docs.platform.sh/development/cli.html)
3. [Authenticate](https://docs.platform.sh/development/cli.html#authentication) using your Platform.sh account
4. Create required config files. Also, if you create a new project, Platform.sh shows you a checklist where you can generate the code for these files
   * [routes.yaml](https://docs.platform.sh/configuration/routes.html)
   * [services.yaml](https://docs.platform.sh/configuration/services.html)
   * [.platform.app.yaml](https://docs.platform.sh/configuration/app.html)
5. Push your changes to your Git Repo
6. After it's been deployed, migrate the database by connecting via [SSH to your project](#ssh-into-your-project) and running the command `vendor/bin/doctrine-migrations migrations:migrate`
7. That's it!

Your project should now be running at <https://console.platform.sh>, and you can start developing your own app!

## Good to know

### Automatic TLS certificates based on Branch / Pull Request

[Platform.sh](https://platform.sh) automatically creates a URL and TLS certificate using [Let's Encrypt](https://letsencrypt.org/) based on your [routes.yaml](https://docs.platform.sh/configuration/routes.html) file for every active environment.

You should be aware that the URL will be built in a specific way. If your branch name gets too long, [Let's Encrypt](https://letsencrypt.org/) won't be able to generate a certificate.

To avoid this, you should configure your [Source Integrations](https://docs.platform.sh/integrations/source.html) to use the name of your **Pull Request** instead of the **Branch Name**.

**Read more about this topic from  [doc.platform.sh](https://docs.platform.sh/configuration/routes/https.html#lets-encrypt-limits-errors-and-branch-names).**

### Hook commands

You can place commands like the database migration mentioned above inside your `.platform.app.yaml` under [hooks](https://docs.platform.sh/configuration/app/build.html#hooks).
This way your commands will be executed every time it deploys a new build *(e.g. if your branch gets updated)*.

Your file could than look like this *(with the default [AppTemplate](https://github.com/shopware/AppTemplate))*:

```yaml
// .platform.app.yaml
hooks:
    build: |
        set -e
        php bin/console assets:install --no-debug
    deploy: |
        set -e
        php bin/console cache:clear
        php bin/console doctrine:migrations:migrate --no-interaction
```

By default, PHP images already run a `composer install` command, so we don't need that in our hooks.
Learn more about that [here](https://docs.platform.sh/languages/php.html#build-flavor).

## Useful Platform.sh commands

In order to use the following commands you need to have the [Platform.sh CLI](https://docs.platform.sh/development/cli.html) installed.

### List all Platform.sh CLI commands

```bash
platform list
```

### Set Platform.sh as new remote host

This step is needed if you want to get more information about the project using the [Platform.sh CLI](https://docs.platform.sh/development/cli.html).

Refer to this documentation on [Create environment](https://docs.platform.sh/gettingstarted/introduction/own-code/create-project.html)

```bash
platform project:set-remote <Project ID>
```

### Push single branch to Platform.sh and activate it

Refer to this documentation on [Create environment](https://docs.platform.sh/gettingstarted/developing/dev-environments/create-environment.html)

```bash
# Push to Platform.sh
git push -u platform <Branch Name>

# Activate branch
platform environment:activate <Branch Name>
```

### Get available URLs for the current project

Refer to this [Documentation](https://docs.platform.sh/development/access-site.html#visiting-the-site-on-the-web)

```bash
platform url 
```

### SSH into your project

Refer to this documentation on [SSH](https://docs.platform.sh/development/ssh.html)

```bash
platform ssh
```

### Connect to the database using SSH tunneling

Refer to this documentation on [SSH Tunneling](https://docs.platform.sh/development/local/tethered.html#ssh-tunneling)

```bash
# List all possible commands
platform tunnel:list

# Open tunnel for all services
platform tunnel:open

# Connect to the remote database normally, as if it were local.
mysql --host=127.0.0.1 --port=30001 --user='user' --password='' --database='main'
```

### Accessing log files

Refer to this documentation on [logs](https://docs.platform.sh/development/logs.html)

```bash
platform log --help
```

---

---

## In-App Purchases
**Source:** [guides/plugins/apps/in-app-purchase.md](https://developer.shopware.com/docs/v6.6/guides/plugins/apps/in-app-purchase.md)  
# In-App Purchases

::: info
In-App Purchase is available since Shopware version 6.6.9.0
:::

In-App Purchases are a way to lock certain features behind a paywall within the same extension.
This is useful for developers who want to offer a free version of their extension with limited features and a paid version with more features.

## Retrieve In-App Purchases on your app server

Whenever Shopware sends you a request, you'll receive a JWT as a query parameter or in the request body,
depending on whether the request is a GET or POST.
This JWT is signed by our internal systems, ensuring that you, as the app developer, can verify its authenticity and confirm it hasn't been tampered with.

You can use the `shopware/app-php-sdk` for plain PHP or the `shopware/app-bundle` for Symfony to validate and decode the JWT.
An example for plain PHP is available [here](https://github.com/shopware/app-php-sdk/blob/main/examples/index.php).
For Symfony applications, use the appropriate action argument for your route.

### Admin

You will also receive In-App Purchases with the initial `sw-main-hidden` admin request.
To make them accessible, inject them into your JavaScript application.

Here is an example of retrieving active In-App Purchases in an example `admin.html.twig` using the `shopware/app-bundle`:

```php
#[Route(path: '/app/admin', name: 'admin')]
public function admin(ModuleAction $action): Response {
    return $this->render('admin.html.twig', [
        'inAppPurchases' => $action->inAppPurchases->all(),
    ]);
}
```

```html
<!DOCTYPE html>
<html>
    <head>
        <script>
            try {
                window.inAppPurchases = JSON.parse('{{ inAppPurchases | json_encode | raw }}');
            } catch (e) {
                window.inAppPurchases = [];
                console.error('Unable to decode In-App Purchases', e);
            }
        </script>

        <!-- ... -->
    </head>

    <!-- ... -->
</html>
```

Alternatively you can extract the query parameter from `document.location` on the initial `sw-main-hidden` request,
store it and ask your app-server do properly decode it for you.

## Trigger a purchase of an In-App Purchases

The checkout process itself is provided by Shopware, you only have to trigger it with an identifier of the In-App Purchase.
To do so, create a button and make use of the [Meteor Admin SDK](https://github.com/shopware/meteor/tree/main/packages/admin-sdk):

```vue
<template>
    <!-- ... -->
    <p>
        If you buy this you'll get an incredible useful feature: ...
    </p>
    <mt-button @click="onClick">
        Buy
    </mt-button>
    <!-- ... -->
</template>

<script setup>
import * as sw from '@shopware/meteor-admin-sdk';

function onClick() {
    sw.iap.purchase({ identifier: 'my-iap-identifier' });
}
</script>
```

Alternatively, you can trigger a checkout manually by sending a properly formatted
[post message](https://developer.mozilla.org/en-US/docs/Web/API/Window/postMessage) with an In-App purchase identifier to the Admin.

---

---

## In-App Purchases
**Source:** [guides/plugins/apps/in-app-purchases.md](https://developer.shopware.com/docs/guides/plugins/apps/in-app-purchases.md)  
# In-App Purchases

::: info
In-App Purchase is available since Shopware version 6.6.9.0
:::

In-App Purchases are a way to lock certain features behind a paywall within the same extension.
This is useful for developers who want to offer a free version of their extension with limited features and a paid version with more features.

## Allow users to buy an In-App Purchase

In order to enable others to purchase your In-App Purchase, you must request a checkout for it via the `sw.iap.purchase()` function of the [Meteor Admin SDK](https://github.com/shopware/meteor/tree/main/packages/admin-sdk).
The checkout process itself is provided by Shopware.
As this is purely functional, it is your responsibility to provide a button and hide it if the IAP cannot be purchased more than once.

```vue
<template>
    <!-- ... -->
    <p>
        If you buy this you'll get an incredible useful feature: ...
    </p>
    <mt-button @click="onClick">
        Buy
    </mt-button>
    <!-- ... -->
</template>

<script setup>
import * as sw from '@shopware/meteor-admin-sdk';

function onClick() {
    sw.iap.purchase({ identifier: 'my-iap-identifier' });
}
</script>
```

Alternatively, you can trigger a checkout manually by sending a properly formatted
[post message](https://developer.mozilla.org/en-US/docs/Web/API/Window/postMessage) with an In-App purchase identifier to the Admin.

## Check active In-App Purchases

Whenever Shopware sends you a request, you'll receive a [JWT](../../../concepts/framework/in-app-purchases.md#token) as a query parameter `in-app-purchases` or in the request body as `inAppPurchases` as part of the `source`, depending on whether the request is a GET or POST. The claims of the JWT will contain all bought In-App Purchases.

### Symfony or PHP app servers

You can use the `shopware/app-php-sdk` for plain PHP or the `shopware/app-bundle` for Symfony to validate and decode the JWT.
An example for plain PHP is available [here](https://github.com/shopware/app-php-sdk/blob/main/examples/index.php).
For Symfony applications, use the appropriate action argument for your route.

#### Admin

You will also receive In-App Purchases with the initial `sw-main-hidden` admin request.
To make them accessible, inject them into your JavaScript application.

Here is an example of retrieving active In-App Purchases in an example `admin.html.twig` using the `shopware/app-bundle`:

```php
#[Route(path: '/app/admin', name: 'admin')]
public function admin(ModuleAction $action): Response {
    return $this->render('admin.html.twig', [
        'inAppPurchases' => $action->inAppPurchases->all(),
    ]);
}
```

```html
<!DOCTYPE html>
<html>
    <head>
        <script>
            try {
                window.inAppPurchases = JSON.parse('{{ inAppPurchases | json_encode | raw }}');
            } catch (e) {
                window.inAppPurchases = {};
                console.error('Unable to decode In-App Purchases', e);
            }
        </script>

        <!-- ... -->
    </head>

    <!-- ... -->
</html>
```

### Non-PHP app servers

To validate In-App Purchase tokens on non-PHP app servers, use a JWT/JOSE library appropriate for your language.
These tokens are signed JSON Web Tokens (JWT) and include the list of purchased features in their claims. To ensure the token’s authenticity,
you must verify its signature using Shopware’s public keys, available as a JWKS (JSON Web Key Set) at `https://api.shopware.com/inappfeatures/jwks`.

Most modern JWT libraries support loading JWKS endpoints directly. After successful verification, you can extract and use the claims to enable or restrict features based on the user’s purchases.

Example (Node.js with `jose`):

```js
import { jwtVerify, createRemoteJWKSet } from 'jose';

const JWKS = createRemoteJWKSet(new URL('https://api.shopware.com/inappfeatures/jwks'));

const { payload } = await jwtVerify(token, JWKS);
console.log(payload); // Contains list of purchased IAP identifiers
```

## Event

Apps are also able to manipulate the available In-App Purchases as described in

---

---

## Local development
**Source:** [guides/plugins/apps/local-development.md](https://developer.shopware.com/docs/v6.4/guides/plugins/apps/local-development.md)  
# Local development

This guide will walk you through the process of adding your app-server to your local Shopware development setup. We assume that you have already set this up. If not, please take a look at the [installation guide](../../../../guides/installation).

---

---

## App development with docker
**Source:** [guides/plugins/apps/local-development/app-development-with-docker.md](https://developer.shopware.com/docs/v6.4/guides/plugins/apps/local-development/app-development-with-docker.md)  
# App development with docker

## Overview

This guide will walk you through the process of combining Shopware and your app in one setup.

## File Structure

At first, you need to clone the app template from [GitHub](https://github.com/shopwareLabs/AppTemplate) and create a `manifest.xml` for your app. Or take a glance at our fully working example based on this template: [appExample](https://github.com/shopwareLabs/AppExample).\
For further information about the `manifest.xml` have a look at our \[PLACEHOLDER-LINK: manifest-documentation].\
The easiest way to create a `manifest.xml` is with our `bin/console app:create-manifest` command.

Your file structure should look as follows:

```text
...
│
├──development
│  ├──custom
│  │  └───apps
│  │      └───yourAppName
│  │          └───manifest.xml
│  │
│  ├──platform
│  └──...
│
└──shopwareAppTemplate
...
```

## Combining both in one docker setup

Once your Shopware development setup is ready to go you need to add your app to it. This is done by adding the services to your `development/docker-compose.yml`.\
At first, you need to add two networks. One for your app system and another one for combining the app system with Shopware.

This is done by adding the networks `appSystem` and `development` to your existing ones:

```yaml
// 
networks:
    shopware:
    appSystem:
    development:
```

The `appSystem`-network is only for your app server and the app database.\
The `development`-network is used to combine your app server with the Shopware server.

### Adding the app server

Now you need to define the `services` in your `development/docker-compose.yml`. First insert the following to add your app server.

```yaml
// development/docker-compose.yml
services:
[...]
  example_app_server:
    image: shopware/development:local
    volumes:
      - "../shopwareAppTemplate:/app"
      - "~/.composer:/.composer"
    environment:
      CONTAINER_UID: 1000
      APPLICATION_UID: 1000
      APPLICATION_GID: 1000
    ports:
      - "127.0.0.1:7777:8000"
    networks:
      appSystem:
      development:
        aliases:
          - example
```

This adds a new container to your docker setup running your app server's code. The new container is available inside the networks `appSystem` and `development`.\
In the `development`-network your app server has the alias `example`. This will be the url which your Shopware server needs to communicate with. This is also the url which you should use in your `manifest.xml` except for iframes.\
`volumes` represents the relative path to your app.\
`ports` exposes port `8000` to `127.0.0.1:7777` to us so that we can visit `127.0.0.1:7777` or `localhost:7777` to directly connect to your app server. This will come in handy when we register our own modules to use iframes.

### Adding the app database

The next step is to also add your mysql server to your docker setup. This is as easy as it was for your app server.\
Simply add this to your `development/docker-compose.yml`.

```yaml
// development/docker-compose.yml
services:
[...]
  example_mysql:
    build: dev-ops/docker/containers/mysql
    environment:
      MYSQL_ROOT_PASSWORD: root
      MYSQL_USER: app
      MYSQL_PASSWORD: app
    ports:
      - "5506:3306"
    volumes:
      - ./dev-ops/docker/_volumes/mysql-example:/mysql-data
    networks:
      appSystem:
        aliases:
          - appmysql
```

As you already know you connect your mysql server to the same network as your app server and give it the alias `appmysql`. Furthermore, you can now connect to your database on port `5506` from outside of the docker container.\
Last but not least we define the credentials for the mysql server and you are done with setting up the database container.

### Combining both in one network

Now you need to add your Shopware server to your `development`-network and give him an alias as follows:

```yaml
// development/docker-composer.yml
services:
[...]
  app_server:
    image: shopware/development:latest
    networks:
      shopware:
        aliases:
          - docker.vm
      development:
        aliases:
          - shopware
    extra_hosts:
      - "docker.vm:127.0.0.1"
    volumes:
      - ~/.composer:/.composer
    tmpfs:
      - /tmp:mode=1777
```

Now your app server can communicate with the Shopware server and your app's database.

## Access your app server via ssh

To easily access a terminal on your app server, you need to create this script `development/dev-ops/docker/actions/ssh-app-server.sh`.

```sh
// development/dev-ops/docker/actions/ssh-app-server.shell script
#!/usr/bin/env bash
TTY: docker exec -i --env COLUMNS=`tput cols` --env LINES=`tput lines` -u __USERKEY__ -t __EXAMPLE_APP_SERVER_ID__ bash
```

This script can be executed from your `development` folder with `./psh.phar docker:ssh-app-server`. Keep in mind that this is only possible when the app server has been started with `./psh.phar docker:start` from your development folder.

To make sure this script actually knows the ID of your app server which is running in the docker container, you need to define the `EXAMPLE_APP_SERVER_ID` in the `development/.psh.yaml.override`.\
Your `development/.psh.yaml.override` should look like this:

```yaml
// development/.psh.yaml.override
# ...
dynamic:
 #  ...
  EXAMPLE_APP_SERVER_ID: docker-compose ps -q example_app_server
 #  ...
# ...
```

## Initialising the app server

To initialise the app server and the app database you need to open a terminal on the app server and run `composer install --no-interaction`.\
Next you need to change your `shopwareAppTemplate/.env` and set the `DATABASE_URL` to `mysql://app:app@appmysql:3306/main`.\
This url should look familiar to you because you just configured each part of it in the `development/docker-compose.yml`.

The next steps should be done in the terminal of your app server.\
Now you can set up the database by executing `bin/console doctrine:database:create`. This will create your database with the name `main`.\
Then execute the migrations with `bin/console doctrine:migrations:migrate --no-interaction`. Now your database is ready.

## Registration

This last step assumes that you already have a valid `manifest.xml` in the correct folder. In order to check this, make sure your `manifest` is in `development/custom/apps/yourAppName/manifest.xml`.\
Then access your local Shopware instance with `./psh.phar docker:ssh` and execute the check with `bin/console app:validate`. This will tell you if you provided a valid `manifest.xml`.

For the sake of simplicity you need to change the `APP_URL` of your Shopware instance to match the network-alias you gave it.\
This is done in your `development/.psh.yaml.override` which should look like this:

```yaml
// development/.psh.yaml.override
# ...
const:
  # ...
  APP_URL: "http://shopware"
  # ...
# ...
```

To make sure your `APP_URL` changed you need to rerun `./psh.phar docker:ssh`. Now your `APP_URL` changed and you can register your app via `bin/console app:refresh --activate`. This can also be done by `bin/console app:install --activate yourAppName`.

**Note:** Like with plugins, apps get installed as inactive. You can activate them by passing the `--activate` flag to the `app:install` command or by executing `app:activate`.

## Working with iframes

Due to the fact that the aliases for your app server only work inside the docker container, you need to change it in the `manifest.xml`. In contrast to every other action, like webhooks or action buttons, iframes need to be accessible from outside the docker container.\
For this purpose iframes are the only thing in your `manifest.xml` where you need to set the source to `http://localhost:7777` as defined in the `development/docker-compose.yml`.

---

---

## App development with platform.sh
**Source:** [guides/plugins/apps/local-development/app-development-with-platform-sh.md](https://developer.shopware.com/docs/v6.4/guides/plugins/apps/local-development/app-development-with-platform-sh.md)  
# App development with platform.sh

## Overview

This guide will walk you through the process of developing your app on Platform.sh with your local Shopware setup.

## Forwarding requests

In order to register your local Shopware instance to your app on Platform.sh you need to be able to connect from Platform.sh to your client.\
To do so, you need to forward the request from your app to your local Shopware instance. This can be done with port forwarding. This means that every request which is addressed to `localhost:8000` on your app will be forwarded to your defined port to your client.\
But why would the app send requests to localhost? This happens when your app wants to communicate with your local Shopware instance which should run on `localhost:8000`. Then your app will send each request to `localhost:8000` which then should get forwarded to your client to the port where Shopware is running on.

## How does this work in practice?

To accomplish this, just copy the command from Platform.sh which can be found in the top right corner and paste it into your terminal. This should look something like this `ssh abcde12345-master-12345--app@ssh.de-2-platform.sh`.\
To make the authentication much easier we recommend installing the [Platform.sh cli](https://docs.platform.sh/development/cli.html) and log in into your project.

To redirect the requests you need to add the option `-R` with a few parameters to the copied Platform.sh command.\
First you define the port on the remote server which needs to be forwarded. In our case this is port `8000`. The second parameter is the destination on your client. This will be your local Shopware instance which is running on `localhost:8000`.\
If you put everything together this should look something like this `ssh -R 8000:localhost:8000 abcde12345-master-12345--app@ssh.de-2-platform.sh`. The last thing you have to do is to change all URLs in your `manifest.xml` to point to your Platform.sh URL and you are done.\
For further information have a look at [remote forwarding](https://www.ssh.com/ssh/tunneling/example).

## Switching between Platform.sh and local development

The best way to switch from Platform.sh to your local setup and vice versa is to have two `manifest.xml` files.\
Create the first one for your Platform.sh setup with `bin/console app:create-manifest APP_NAME=PlatformshSetup APP_URL_CLIENT=https://your-client-url.platform.sh APP_URL_BACKEND=https://your-backend-url.platform.sh` and the other one for your local setup with\
`bin/console app:create-manifest APP_NAME=LocalSetup APP_URL_CLIENT=http://localhost/your-local-client-url APP_URL_BACKEND=http://localhost/your-local-backend-url` Then place them in `development/custom/apps/your-app-name/manifest.xml` and you are good to go.

Once you switch to local development you have to make sure to change your `APP_URL` of your Shopware instance in your `development/.psh.yaml.override` back to `http://localhost:8000`. This can be done as follows:

```yaml
const:
  APP_URL: "http://localhost:8000"
```

And vice versa change it to `http://shopware` for development with Platform.sh.\
After changing your `APP_URL` you need to execute `bin/console app:url-change:resolve`. More about this \[PLACEHOLDER-LINK: app-url-change documentation].

---

---

## Payment
**Source:** [guides/plugins/apps/payment.md](https://developer.shopware.com/docs/v6.6/guides/plugins/apps/payment.md)  
*(Body truncated in this bundle; follow the link for the rest.)*

# Payment

Starting with version `6.4.1.0`, Shopware also provides functionality for your app to be able to integrate payment providers.
You can choose between just a simple request for approval in the background (synchronous payment) and the customer being forwarded to a provider for payment (asynchronous payment).
You provide one or two endpoints, one for starting the payment and providing a redirect URL and one for finalization to check for the resulting status of the payment.
The requests and responses of all of your endpoints will be signed and feature JSON content.

## Prerequisites

You should be familiar with the concept of Apps, their registration flow as well as signing and verifying requests and responses between Shopware and the App backend server.

Your app server must be also accessible for the Shopware server.
You can use a tunneling service like [ngrok](https://ngrok.com/) for development.

## Manifest configuration

If your app should provide one or multiple payment methods, you need to define these in your manifest.
The created payment methods in Shopware will be identified by the name of your app and the identifier you define per payment method.
You should therefore not change the identifier after release, otherwise new payment methods will be created.

You may choose between a synchronous and an asynchronous payment method.
These two types are differentiated by defining a `finalize-url` or not.
If no `finalize-url` is defined, the internal Shopware payment handler will default to a synchronous payment.
If you do not want or need any communication during the payment process with your app, you can also choose not to provide a `pay-url`, then the payment will remain on open on checkout.

Below, you can see different definitions of payment methods.

Depending on the URLs you provide, Shopware knows which kind of payment flow your payment method supports.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<manifest xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://raw.githubusercontent.com/shopware/shopware/trunk/src/Core/Framework/App/Manifest/Schema/manifest-3.0.xsd">
    <meta>
        <!-- The name of the app should not change. Otherwise, all payment methods are created as duplicates. -->
        <name>PaymentApp</name>
        <!-- ... -->
    </meta>

    <payments>
        <payment-method>
            <!-- The identifier of the payment method should not change. Otherwise, a separate method is created. -->
            <identifier>asynchronousPayment</identifier>
            <name>Asynchronous payment</name>
            <name lang="de-DE">Asynchrone Zahlung</name>
            <description>This payment method requires forwarding to payment provider.</description>
            <description lang="de-DE">Diese Zahlungsmethode erfordert eine Weiterleitung zu einem Zahlungsanbieter.</description>
            <pay-url>https://payment.app/async/pay</pay-url>
            <finalize-url>https://payment.app/async/finalize</finalize-url>
            <!-- This optional path to this icon must be relative to the manifest.xml -->
            <icon>Resources/paymentLogo.png</icon>
        </payment-method>

        <payment-method>
            <!-- The identifier of the payment method should not change. Otherwise, a separate method is created. -->
            <identifier>synchronousPayment</identifier>
            <name>Synchronous payment</name>
            <name lang="de-DE">Synchrone Zahlung</name>
            <description>This payment method does everything in one request.</description>
            <description lang="de-DE">Diese Zahlungsmethode arbeitet in einem Request.</description>
            <!-- This URL is optional for synchronous payments (see below). -->
            <pay-url>https://payment.app/sync/pay</pay-url>
        </payment-method>

        <payment-method>
            <!-- The identifier of the payment method should not change. Otherwise, a separate method is created. -->
            <identifier>simpleSynchronousPayment</identifier>
            <name>Simple Synchronous payment</name>
            <name lang="de-DE">Einfache synchrone Zahlung</name>
            <description>This payment will not do anything and stay on 'open' after order.</description>
            <description lang="de-DE">Diese Zahlungsmethode wird die Transaktion auf 'offen' belassen.</description>
            <!-- No URL is provided. -->
        </payment-method>

        <payment-method>
            <!-- The identifier of the payment method should not change. Otherwise, a separate method is created. -->
            <identifier>preparedPayment</identifier>
            <name>Payment, that offers everything</name>
            <name lang="de-DE">Eine Zahlungsart, die alles kann</name>
            <validate-url>https://payment.app/validate</validate-url>
            <pay-url>https://payment.app/pay</pay-url>
            <!-- This optional path to this icon must be relative to the manifest.xml -->
            <icon>Resources/paymentLogo.png</icon>
        </payment-method>

        <payment-method>
            <!-- The identifier of the payment method should not change. Otherwise, a separate method is created. -->
            <identifier>refundPayment</identifier>
            <name>Refund payments</name>
            <name lang="de-DE">Einfache Erstattungen</name>
            <refund-url>https://payment.app/refund</refund-url>
            <!-- This optional path to this icon must be relative to the manifest.xml -->
            <icon>Resources/paymentLogo.png</icon>
        </payment-method>

        <payment-method>
            <!-- The identifier of the payment method should not change. Otherwise, a separate method is created. -->
            <identifier>recurringPayment</identifier>
            <name>Recurring payments</name>
            <name lang="de-DE">Einfache wiederkehrende Zahlungen</name>
            <recurring-url>https://payment.app/recurring</recurring-url>
            <!-- This optional path to this icon must be relative to the manifest.xml -->
            <icon>Resources/paymentLogo.png</icon>
        </payment-method>
    </payments>
</manifest>

```

## Synchronous payments

There are different types of payments.
Synchronous payment is the simplest of all and does not need any additional interaction with the customer.
If you have defined a `pay-url`, you can choose to be informed about and possibly process the payment or not.
If you do not need to communicate with your app, you can stop reading here and the transaction will stay open.
But if you do define a `pay-url`, you can respond to the request with a different transaction status like authorize, paid, or failed.
This is useful if you want to add a payment provider that only needs the information if the customer has already provided it in the checkout process or not.
For example, a simple credit check for payment upon invoice.
Below you can see an example of a simple answer from your app to mark a payment as authorized.

Request content is JSON

```json
{
  "source": {
    "url": "http:\/\/localhost:8000",
    "shopId": "hRCw2xo1EDZnLco4",
    "appVersion": "1.0.0"
  },
  "orderTransaction": {
    //...
  },
  "order": {
    //...
  }
}
```

Refer to an example on [payment payload](https://github.com/shopware/app-php-sdk/blob/main/tests/Context/_fixtures/payment.json) and the response should look like this:

```json
{
  "status": "authorize"
}
```

Refer to possible [status values](#all-possible-payment-states).
Failing states can also have a `message` property with the reason, which will be logged and could be seen as information for the merchant.

```json
{
  "status": "authorize",
  "message": "The customer failed to pass the credit check."
}
```

```php
use Psr\Http\Message\RequestInterface;
use Psr\Http\Message\ResponseInterface;
use Shopware\App\SDK\Shop\ShopResolver;
use Shopware\App\SDK\Context\ContextResolver;
use Shopware\App\SDK\Response\PaymentResponse;

function myController(RequestInterface $request): ResponseInterface
{
    // injected or build by yourself
    $shopResolver = new ShopResolver($repository);
    $contextResolver = new ContextResolver();
    $signer = new ResponseSigner();
    
    $shop = $shopResolver->resolveShop($serverRequest);
    $payment = $contextResolver->assemblePaymentPay($serverRequest, $shop);
    
    // implement your logic here based on the information provided in $payment
    
    // check PaymentResponse class for all available payment states
    return $signer->signResponse(PaymentResponse::paid(), $shop);
}
```

```php
use Shopware\App\SDK\Context\Payment\PaymentPayAction;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\HttpKernel\Attribute\AsController;
use Symfony\Component\Routing\Attribute\Route;
use Shopware\App\SDK\Response\PaymentResponse;
use Psr\Http\Message\ResponseInterface;

#[AsController]
class PaymentController {
    #[Route('/payment/pay')]
    public function handle(PaymentPayAction $payment): ResponseInterface
    {
        // handle payment
        
        return PaymentResponse::paid();
    }
}
```

## Asynchronous payments

Asynchronous payments are more complicated than synchronous payments.
They require interaction with the customer and a redirect to the payment provider, such as PayPal or Stripe.

Here is how it works:

* Shopware sends the first pay `POST` request to start the payment with the payment provider.
  The request includes all necessary data such as the `order`, `orderTransaction`, and a `returnUrl`,
  where the customer should be redirected once the payment process with the payment provider has been finished.
* Your app server returns a response with a `redirectUrl` to the payment provider.
* The browser will be redirected to this URL and processes his order,
  and the payment provider will redirect the customer back to the `returnUrl` provided in the first request.
* Shopware sends a second `POST` request to the `finalize-url` with the `orderTransaction` and all the query parameters passed by the payment provider to Shopware.
* Your app server responds with a `status` and a `message` if necessary, like in the synchronous payment.

Request content is JSON

```json
{
  "source": {
    "url": "http:\/\/localhost:8000",
    "shopId": "hRCw2xo1EDZnLco4",
    "appVersion": "1.0.0"
  },
  "orderTransaction": {
    //...
  },
  "order": {
    //...
  },
  "returnUrl": "https://shop.com/checkout/...."
}
```

You can find an example refund payload [here](https://github.com/shopware/app-php-sdk/blob/main/tests/Context/_fixtures/payment.json)

and your response should look like this:

```json
{
  "redirectUrl": "https://payment.app/customer/gotoPaymentProvider"
}
```

```php
use Psr\Http\Message\RequestInterface;
use Psr\Http\Message\ResponseInterface;
use Shopware\App\SDK\Shop\ShopResolver;
use Shopware\App\SDK\Context\ContextResolver;
use Shopware\App\SDK\Response\PaymentResponse;

function pay(RequestInterface $request): ResponseInterface
{
    // injected or build by yourself
    $shopResolver = new ShopResolver($repository);
    $contextResolver = new ContextResolver();
    $signer = new ResponseSigner();
    
    $shop = $shopResolver->resolveShop($serverRequest);
    $payment = $contextResolver->assemblePaymentPay($serverRequest, $shop);
    
    // Implement your logic here based on the information provided in $payment. 
    // Payment providers should redirect the customer to $payment->returnUrl once the payment process has been finished.
    
    return $signer->signResponse(PaymentResponse::redirect($paymentProviderRediectUrl), $shop);
}
```

```php
use Shopware\App\SDK\Context\Payment\PaymentPayAction;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\HttpKernel\Attribute\AsController;
use Symfony\Component\Routing\Attribute\Route;
use Shopware\App\SDK\Response\PaymentResponse;
use Psr\Http\Message\ResponseInterface;

#[AsController]
class PaymentCont

… **Truncated.** Full document: https://developer.shopware.com/docs/v6.6/guides/plugins/apps/payment.md


---

## Rule Builder
**Source:** [guides/plugins/apps/rule-builder.md](https://developer.shopware.com/docs/v6.6/guides/plugins/apps/rule-builder.md)  
# Rule Builder

Shopware allows you to enhance the capabilities of the rule builder by adding custom rules from an app. By creating a custom app and defining your own rules, you can incorporate specific conditions and actions based on your business requirements. This empowers you to create dynamic and personalized customer experiences, such as customized promotions, targeted discounts, or advanced product recommendations.

Starting with version 6.4.12.0, apps are able to [add custom rule conditions](./add-custom-rule-conditions) for use in the [Rule Builder](../../../../concepts/framework/rules).

---

---

## Add custom rule conditions
**Source:** [guides/plugins/apps/rule-builder/add-custom-rule-conditions.md](https://developer.shopware.com/docs/v6.6/guides/plugins/apps/rule-builder/add-custom-rule-conditions.md)  
# Add custom rule conditions

## Overview

In this guide, you'll learn how to make your app introduce custom conditions for use in the [Rule Builder](../../../../concepts/framework/rules). Custom conditions can be defined with fields to be rendered in the Administration and with their own logic, using the same approach as [App Scripts](../app-scripts/).

::: info
Note that app rule conditions were introduced in Shopware 6.4.12.0, and are not supported in previous versions.
:::

## Prerequisites

If you're not familiar with the app system, please take a look at the concept first.

You should also be familiar with the general concept of the Rule Builder.

For the attached logic of your custom conditions, you'll use [twig files](https://twig.symfony.com/). Please refer to the App Scripts guide for a general introduction.

## Definition

App Rule Conditions are defined in the `manifest.xml` file of your app:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<manifest xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://raw.githubusercontent.com/shopware/shopware/trunk/src/Core/Framework/App/Manifest/Schema/manifest-3.0.xsd">
    <meta>
        <!-- ... -->
    </meta>
    <rule-conditions>
        <rule-condition>
            <!-- The identifier of the rule condition must be unique should not change. Otherwise a separate rule condition is created and uses of the old one are lost. -->
            <identifier>my_custom_condition</identifier>
            <!-- Translatable, a name of your rule condition -->
            <name>Custom condition</name>
            <name lang="de-DE">Eigene Bedingung</name>
            <!-- A thematic group the condition should be assigned too, available groups are: general, customer, cart, item, promotion, misc -->
            <group>misc</group>
            <!-- The *.twig file that contains the corresponding script for the condition. It must be placed in the directory Resources/scripts/rule-conditions starting from your app's root directory -->
            <script>custom-condition.twig</script>
            <!-- Define the fields you want the user to fill out for use as data within your condition -->
            <constraints>
                <!-- the element type, defines the type of the field -->
                <!-- the elements available here are the same as for custom fields -->
                <single-select name="operator">
                    <placeholder>Choose an operator...</placeholder>
                    <placeholder lang="de-DE">Bitte Operatoren wählen</placeholder>
                    <options>
                        <option value="=">
                            <name>Is equal to</name>
                            <name lang="de-DE">Ist gleich</name>
                        </option>
                        <option value="!=">
                            <name>Is not equal to</name>
                            <name lang="de-DE">Ist nicht gleich</name>
                        </option>
                    </options>
                    <required>true</required>
                </single-select>
                <text name="firstName">
                    <placeholder>Enter first name</placeholder>
                    <placeholder lang="de-DE">Bitte Vornamen eingeben</placeholder>
                    <required>true</required>
                </text>
            </constraints>
        </rule-condition>
    </rule-conditions>
</manifest>

```

For a complete reference of the structure of the manifest file, take a look at the [Manifest reference](../../../../resources/references/app-reference/manifest-reference).

The following fields are required:

* `identifier`: A technical name for the condition that should be unique within the scope of the app. The name is being used to identify existing conditions when updating the app, so it should not be changed.
* `name`: A descriptive and translatable name for the condition. The name will be shown within the Rule Builder's selection of conditions in the Administration.
* `script`: The file name and extension of the file that contains the script for the condition. All scripts for rule conditions must be placed inside `Resources/scripts/rule-conditions` within the root directory of the app.

### Constraints

Constraints are optional and may be used to define fields, whose purpose is to provide data for use within the condition's script.

Constraints are a collection of [custom fields](../custom-data/), which allows you to provide a variety of different fields for setting parameters within the administration. Fields may be marked as `required`. The `name` attribute of the field is also the variable the field's value will be exposed as within the condition's script. So it is advisable to use a variable-friendly name and to use unique names within the confines of a single condition.

The above example will add the condition shown below for selection in the Administration:

![App Rule Condition](../../../../assets/app-rule-condition.png)

## Scripts

The corresponding scripts to the defined conditions within `manifest.xml` need to be placed at a specific directory of your app:

```text
└── DemoApp
    ├── Resources
    │   └── scripts                         // all scripts are stored in this folder
    │       ├── rule-conditions             // reserved for scripts of rule conditions
    │       │   └── custom-condition.twig   // the file name may be freely chosen but must be identical to the corresponding `script` element within `rule-conditions` of `manifest.xml`
    │       └── ...
    └── manifest.xml
```

Scripts for rule conditions are [twig files](https://twig.symfony.com/) that are executed in a sandboxed environment. They offer the same extended syntax and debugging options as [App Scripts](../app-scripts/).

Within the script you will have access to the `scope` variable which is an instance of `RuleScope` as described in the [Rule Builder concept](../../../../concepts/framework/rules). The scope instance provides you with the current `SalesChannelContext` and, given the right scope, the current cart. Further available variables depend on the existence of constraints within the definition of your conditions.

A script *must* return a boolean value, stating whether the condition is true or false. Anything but a boolean returned as value may lead to unexpected behavior.

### Compare helper

To keep condition scripts smaller we provide a `compare` helper function which can be used for the most common comparisons of two values.

The function takes three arguments:

```text
compare(operator, value, comparable)
```

The `operator` *must* be one of the following string values: `=`, `!=`, `>`, `>=`, `<`, `<=`, `empty`

If either one or both of `value` and `comparable` are an array, then only `=` and `!=` should be used as operator. It will then compare whether there is at least one occurrence of the value within the other array and return `true` if that is the case. As an example `value` might be an ID, `comparable` an array of IDs and you could use the function to match whether the ID is included in that array.

### Example

```twig
// Resources/scripts/rule-conditions/custom-condition.twig
{% if scope.salesChannelContext.customer is not defined %}
    {% return false %}
{% endif %}

{% return compare(operator, scope.salesChannelContext.customer.firstName, firstName) %}
```

In the example above, we first check whether we can retrieve the current customer from the instance of `RuleScope` and return `false` otherwise.

We then use the variables `operator` and `firstName`, provided by the constraints of the condition, to evaluate whether the first name in question matches the first name of the current customer. To do so, we make use of the `compare` helper function.

### Line item condition example

```html
// manifest.xml
<!-- ... -->
<rule-condition>
    <identifier>line_item_condition</identifier>
    <name>Custom product multi select</name>
    <group>item</group>
    <script>line-item-condition.twig</script>
    <constraints>
        <single-select name="operator">
            <placeholder>Choose an operator...</placeholder>
            <options>
                <option value="=">
                    <name>Is equal to</name>
                </option>
                <option value="!=">
                    <name>Is not equal to</name>
                </option>
            </options>
            <required>true</required>
        </single-select>
        <multi-entity-select name="productIds">
            <placeholder>Choose products...</placeholder>
            <entity>product</entity>
            <required>true</required>
        </multi-entity-select>
    </constraints>
</rule-condition>
<!-- ... -->
```

```twig
// Resources/scripts/rule-conditions/line-item-condition.twig
{% if scope.lineItem is defined %}
    {% return compare(operator, lineItem.referenceId, productIds) %}
{% endif %}

{% if scope.cart is not defined %}
    {% return false %}
{% endif %}

{% for lineItem in scope.cart.lineItems.getFlat() %}
    {% if compare(operator, lineItem.referenceId, productIds) %}
        {% return true %}
    {% endif %}
{% endfor %}

{% return false %}
```

In this example we first check if the current scope is `LineItemScope` and refers to a specific line item. If so, we compare that specific line item. Otherwise we check if the scope has a cart and return false if it doesn't. We have a multi select for product selection in the Administration which provides an array of product IDs in the script. We iterate the current cart's line items to check if the product is included and return `true` if that is the case.

### Date condition example

```html
// manifest.xml
<!-- ... -->
<rule-condition>
    <identifier>date_condition</identifier>
    <name>Custom date condition</name>
    <group>misc</group>
    <script>date-condition.twig</script>
</rule-condition>
<!-- ... -->
```

```twig
// Resources/scripts/rule-conditions/date-condition.twig
{% return compare('=', scope.getCurrentTime()|date_modify('first day of this month')|date_modify('second wednesday of this month')|date('Y-m-d'), scope.getCurrentTime()|date('Y-m-d')) %}
```

For this example, we don't have to define constraints. We retrieve the current date from the scope, calling `getCurrentTime`. We modify the date to set it to the first day of the month, then modify it again to set it to the second wednesday from that point in time. We then compare that date against the current date for a condition that matches only on the second wednesday of each month.

---

---

## Shipping methods
**Source:** [guides/plugins/apps/shipping-methods.md](https://developer.shopware.com/docs/v6.6/guides/plugins/apps/shipping-methods.md)  
# Shipping methods

Starting with version 6.5.7.0 as **experimental feature**. Shopware has introduced experimental functionality for adding shipping methods via the App Manifest to a shop. **The entire functionality and API are subject to change during the development process.**

## Prerequisites

You should be familiar with the concept of Apps, their registration flow as well as signing and verifying requests and responses between Shopware and the App backend server.

Your app server must be also accessible for the Shopware server.

## Manifest configuration

### Basic configuration

The following example represents the most minimal configuration for a shipping method.

**Important!**

Ensure that the `<identifier>` of your shipping method remains unchanged, as Shopware will deactivate or delete shipping methods that do no longer appear in the manifest during app updates.

::: code-group

```xml [manifest.xml]

<?xml version="1.0" encoding="UTF-8" ?>
<manifest xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
          xsi:noNamespaceSchemaLocation="https://raw.githubusercontent.com/shopware/shopware/trunk/src/Core/Framework/App/Manifest/Schema/manifest-2.0.xsd">
    <meta>
        <!-- Make sure that the name of your app does not change anymore, otherwise there will be duplicates of your shipping methods -->
        <name>NameOfYourShippingMethodApp</name>
        <!-- ... -->
    </meta>

    <shipping-methods>

        <shipping-method>
            <!-- The identifier should not change after the first release -->
            <identifier>NameOfYourFirstShippingMethod</identifier>
            <name>First shipping method</name>

            <delivery-time>
                <!-- Requires a new generated UUID for your new delivery time -->
                <id>c8864e36a4d84bd4a16cc31b5953431b</id>
                <name>From 2 to 4 days</name>
                <min>2</min>
                <max>4</max>
                <unit>day</unit>
            </delivery-time>
        </shipping-method>

    </shipping-methods>
</manifest>
```

:::

### Delivery Time

The app manufacturer should initially display the standard delivery time to the shop manager, who can subsequently adjust it as needed. The delivery time requires some configurations.

#### Id

The ID should only be generated initially and should remain unchanged thereafter. Changing it will result in the creation of a new one.

::: info
Please note that you should not modify the ID of the shipping time.
:::

#### Name

The name should describe the delivery time simply, briefly and comprehensibly.

#### Min / Max

The min and max values depend on the unit. Assuming the unit is days, in our example, the delivery time has a range from 2 to 4 days.

#### Unit

The following values are possible units

* hour
* day
* week
* month
* year

::: code-group

```xml [manifest.xml]

<?xml version="1.0" encoding="UTF-8" ?>
<manifest xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
          xsi:noNamespaceSchemaLocation="https://raw.githubusercontent.com/shopware/shopware/trunk/src/Core/Framework/App/Manifest/Schema/manifest-2.0.xsd">
    
    ...

    <shipping-methods>

        <shipping-method>
            <identifier>NameOfYourFirstShippingMethod</identifier>
            <name>First shipping method</name>
            ...
            <delivery-time>
                <id>c8864e36a4d84bd4a16cc31b5953431b</id>
                <name>From 2 to 4 days</name>
                <min>2</min>
                <max>4</max>
                <unit>day</unit>
            </delivery-time>
            ...
        </shipping-method>

    </shipping-methods>
</manifest>
```

:::

### Extended configuration

The functionality offers more than one identifier name. The following examples represent all possible configurations.

* Translation of fields that are visible to the customer and requires a translation
* Shipping method description
* Shipping method icon
* Shipping method active (expects true or false). Default value is `false`

::: code-group

```xml [manifest.xml]

<?xml version="1.0" encoding="UTF-8" ?>
<manifest xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
          xsi:noNamespaceSchemaLocation="https://raw.githubusercontent.com/shopware/shopware/trunk/src/Core/Framework/App/Manifest/Schema/manifest-2.0.xsd">

    ...

    <shipping-methods>

        <shipping-method>
            <!-- Identifier should not change after the first release -->
            <identifier>NameOfYourFirstShippingMethod</identifier>
            <name>First shipping method</name>
            <name lang="de-DE">Erste Versandmethode</name>
            <delivery-time>
                <!-- Remember to remove the dashes from generated UUID -->
                <id>c8864e36a4d84bd4a16cc31b5953431b</id>
                <name>From 2 to 4 days</name>
                <min>2</min>
                <max>4</max>
                <unit>day</unit>
            </delivery-time>
            <!-- The following configurations are optional -->
            <description>This is a simple description</description>
            <description lang="de-DE">Das ist eine einfache Beschreibung</description>
            <icon>icon.png</icon>
            <active>true</active>
            <tracking-url>https://www.yourtrackingurl.com</tracking-url>
            <position>2</position>
        </shipping-method>

    </shipping-methods>
</manifest>
```

:::

### Description

You can initially add a description for the customer.

::: info
Please note that the manifest cannot modify the description once you install the app, as the merchant can change it.
:::

::: code-group

```xml [manifest.xml]

<?xml version="1.0" encoding="UTF-8" ?>
<manifest xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
          xsi:noNamespaceSchemaLocation="https://raw.githubusercontent.com/shopware/shopware/trunk/src/Core/Framework/App/Manifest/Schema/manifest-2.0.xsd">
    
    ...

    <shipping-methods>

        <shipping-method>
            <identifier>NameOfYourFirstShippingMethod</identifier>
            <name>First shipping method</name>
            ...
            <description>This is a simple description</description>
            <description lang="de-DE">Das ist eine einfache Beschreibung</description>
            <description lang="fr-FR">C'est une description simple</description>
            ...
        </shipping-method>

    </shipping-methods>
</manifest>
```

:::

### Icon

You can initially add a shipping method icon. You must specify the path to this icon as relative to the manifest.xml file. For example, you have the following directory structure:

```text
YourAppDirectory/
├── assets/
│   └── icons/
│       └── yourIcon.png
└── manifest.xml
```

The path should be: `assets/icons/yourIcon.png`

::: info
Please note that the manifest cannot modify the icon once you install the app, as the merchant can change it.
:::

::: code-group

```xml [manifest.xml]

<?xml version="1.0" encoding="UTF-8" ?>
<manifest xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
          xsi:noNamespaceSchemaLocation="https://raw.githubusercontent.com/shopware/shopware/trunk/src/Core/Framework/App/Manifest/Schema/manifest-2.0.xsd">
    
    ...

    <shipping-methods>

        <shipping-method>
            <identifier>NameOfYourFirstShippingMethod</identifier>
            <name>First shipping method</name>
            ...
            <icon>assets/icons/yourIcon.png</icon>
            ...
        </shipping-method>

    </shipping-methods>
</manifest>
```

:::

### Active

You can activate the shipping method by default. Possible values for active are `true` or `false`

* true: Activates the shipping method
* false: Deactivates the shipping method. Alternatively, you can leave out active

::: code-group

```xml [manifest.xml]

<?xml version="1.0" encoding="UTF-8" ?>
<manifest xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
          xsi:noNamespaceSchemaLocation="https://raw.githubusercontent.com/shopware/shopware/trunk/src/Core/Framework/App/Manifest/Schema/manifest-2.0.xsd">
    
    ...

    <shipping-methods>

        <shipping-method>
            <identifier>NameOfYourFirstShippingMethod</identifier>
            <name>First shipping method</name>
            ...
            <active>true</active>
            ...
        </shipping-method>

    </shipping-methods>
</manifest>
```

:::

### Tracking url

It is possible to add a tracking URL for customers to monitor the delivery status.

::: code-group

```xml [manifest.xml]

<?xml version="1.0" encoding="UTF-8" ?>
<manifest xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
          xsi:noNamespaceSchemaLocation="https://raw.githubusercontent.com/shopware/shopware/trunk/src/Core/Framework/App/Manifest/Schema/manifest-2.0.xsd">
    
    ...

    <shipping-methods>

        <shipping-method>
            <identifier>NameOfYourFirstShippingMethod</identifier>
            <name>First shipping method</name>
            ...
            <tracking-url>https://www.yourtrackingurl.com</tracking-url>
            ...
        </shipping-method>

    </shipping-methods>
</manifest>
```

:::

### Position

Here, you can set the display order of the shipping methods in the checkout. If you omit the tag, the position of the shipping method is 1 by default.

::: code-group

```xml [manifest.xml]

<?xml version="1.0" encoding="UTF-8" ?>
<manifest xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
          xsi:noNamespaceSchemaLocation="https://raw.githubusercontent.com/shopware/shopware/trunk/src/Core/Framework/App/Manifest/Schema/manifest-2.0.xsd">

    ...

    <shipping-methods>

        <shipping-method>
            <identifier>NameOfYourFirstShippingMethod</identifier>
            <name>First shipping method</name>
            ...
            <position>2</position>
            ...
        </shipping-method>

    </shipping-methods>
</manifest>
```

:::

---

---

## App Starter Guides
**Source:** [guides/plugins/apps/starter.md](https://developer.shopware.com/docs/v6.6/guides/plugins/apps/starter.md)  
# App Starter Guides

The app starter guide provides a comprehensive approach to extending the platform's functionality. The following section guides you on creating custom API endpoints with App scripts, reading and writing data to/from Shopware, and creating custom admin extensions.

---

---

## Starter Guide - Add an API Endpoint
**Source:** [guides/plugins/apps/starter/add-api-endpoint.md](https://developer.shopware.com/docs/v6.6/guides/plugins/apps/starter/add-api-endpoint.md)  
# Starter Guide - Add an API Endpoint

::: info
Note that this guide relies on [App scripts](../app-scripts/), introduced from Shopware 6.4.8.0 version.
:::

This guide shows how you can add a custom API endpoint that delivers dynamic data starting from zero.

After reading, you will be able to:

* Create the basic setup of an app.
* Execute app scripts and use them to model custom logic.
* Fetch, filter, and aggregate data from Shopware.
* Consume HTTP parameters and create responses.

## Prerequisites

* A Shopware cloud store
* Basic CLI usage (creating files, directories, running commands)
* Installed and configured [shopware-cli](../../../../products/cli/) tools
* General knowledge of [Twig Syntax](https://twig.symfony.com/)
* A text editor

## Create the app wrapper

We need to create the app "wrapper", the so-called app manifest within a new directory. Let's call that the project directory:

```text
MyApiExtension/
├─ manifest.xml
```

::: info
When using a self-hosted Shopware version, you can also create the project directory in the `custom/apps` directory of your Shopware installation. However, the descriptions in this guide apply to both Shopware cloud and self-hosted stores.
:::

Next, we will put our basic configuration into the file we just created.

::: code-group

```xml [manifest.xml]
<?xml version="1.0" encoding="UTF-8"?>
<manifest xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://raw.githubusercontent.com/shopware/shopware/trunk/src/Core/Framework/App/Manifest/Schema/manifest-2.0.xsd">
    <meta>
        <name>MyApiExtension</name>
        <label>Topsellers API</label>
        <description>This app adds a Topseller API endpoint</description>
        <author>shopware AG</author>
        <copyright>(c) shopware AG</copyright>
        <version>1.0.0</version>
        <license>MIT</license>
    </meta>
    <permissions>
        <read>order</read>
        <read>order_line_item</read>
        <read>product</read>
    </permissions>
</manifest>
```

:::

Besides some metadata, like a name, description, or version, this file contains permissions that the app requires.
We will need them later on when performing searches.

## Create the script

We will define our new API endpoint in a script file based on [App Scripts](./../app-scripts/).
There are specific directory conventions that we have to follow to register a new API endpoint script.
The prefix for our API endpoint is one of the following and cannot be changed:

| API        | API consumers / callers      | Prefix                |
|------------|------------------------------|-----------------------|
| Store API  | Customer-facing integrations | `/store-api/script/`  |
| Admin API  | Backend integrations         | `/api/script/`        |
| Storefront | Default Storefront           | `/storefront/script/` |

::: info
You might wonder why the Storefront shows up in that table. In Storefront endpoints, you can render not only JSON but also twig templates.
But use them with care - whenever you create a Storefront endpoint, your app will not be compatible with headless consumers.

Learn more about the different endpoints in [custom endpoints](../app-scripts/custom-endpoints)
:::

### Directory structure

In this example, we're going to create a Store API endpoint. We want to provide logic that returns the top-selling products for a specific category.
So let's use the following endpoint naming:

`/store-api/script/swag/topseller`

You see that we have added a custom subdirectory `swag` in the route.
This is a good practice because we can prevent naming collisions between different apps.
Slashes (or subdirectories) in the endpoint path are represented by a hyphen in the name of the directory that contains the script.

```text
MyApiExtension/
├─ Resources/
│  ├─ scripts/
│  │  ├─ store-api-swag-topseller/ <-- /store-api/script/swag/topseller
│  │  │  ├─ topseller-script.twig
├─ manifest.xml
```

This directory naming causes Shopware to expose the script on two routes:

* `/store-api/script/swag/topseller` and
* `/store-api/script/swag-topseller`

### Add custom logic and install

Let's start with a simple script to see it in action:

```twig
// Resources/scripts/store-api-swag-topseller/topseller-script.twig
{% block response %}
    {% set response = services.response.json({ test: 'This is my API endpoint' }) %}
    {% do hook.setResponse(response) %}
{% endblock %}
```

Next we will install the App using the Shopware CLI.

::: info
If this is your first time using the Shopware CLI, you have to [install](../../../../products/cli/installation) it first. Next, configure it using the `shopware-cli project config init` command.
:::

Run this command from the root of the project directory.

```shell
shopware-cli project extension upload . --activate
```

This command will create a zip file from the specified extension directory (the one you are in), upload it to your configured store and activate it.

### Call the endpoint

You can call the endpoint using this curl command.

::: info
Follow this guide for more information on using the Store API : [Store API Authentication & Authorization](https://shopware.stoplight.io/docs/store-api/ZG9jOjEwODA3NjQx-authentication-and-authorisation)
:::

```shell
curl --request GET \
  --url http://<your-store-url>/store-api/script/swag/topseller \
  --header 'sw-access-key: insert-your-access-key'
```

which should return something like:

```json
{"apiAlias":"store_api_swag_topseller_response","test":"This is my API endpoint"}
```

However, instead of using curl, we recommend using visual clients to test the API - such as [Postman](https://www.postman.com/downloads/) or [Insomnia](https://insomnia.rest/download).

## Fill in the logic

For now, our script is not really doing anything. Let's change that.

```twig
// Resources/scripts/store-api-swag-topseller/topseller-script.twig
{% block response %}

    {% set categoryId = hook.request.categoryId %}

    {% set criteria = {
        aggregations: [
            {
                name: "categoryFilter",
                type: "filter",
                filter: [{
                    type: "equals",
                    field: "order.lineItems.product.categoryIds",
                    value: categoryId
                }],
                aggregation: {
                    name: "orderedProducts",
                    type: "terms",
                    field: "order.lineItems.productId",
                    aggregation: {
                        name: "quantityItemsOrdered",
                        type : "sum",
                        field: "order.lineItems.quantity"
                    }
                }
            }
        ]
    } %}

    {% set orderAggregations = services.repository.aggregate('order', criteria) %}

    {% set response = services.response.json(orderAggregations.first.jsonSerialize) %}

    {% do hook.setResponse(response) %}

{% endblock %}
```

What happened here?

We wrap everything in a block named `response`. That way, we will get access to useful objects and services, so we can build a response.

### Search criteria and fetching results

We start by reading the requested category id using `hook.request.categoryId`. In general, we can access post body parameters using `hook.request.*`.

In the following lines, we define a search criteria. The criteria contain a description of the data we want to fetch:

1. First, we filter out all products not inside the category that was requested, using a filter aggregation.
2. The following lines contain two further nested aggregations:
   1. The first one groups all products from all orders using their id.
   2. The second one sums up the number of ordered items in each order.

Ultimately, it gives a result of all products that have been ordered and the total ordered.

::: info
To learn more about the structure of search criteria, follow the link below:

[Search Criteria](./../../../integrations-api/general-concepts/search-criteria)
:::

We now send a request to the database to retrieve the result using:

```twig
{% set orderAggregations = services.repository.aggregate('order', criteria) %}
```

### Building the response

In the final step, we build the response. We use the `services.response.json()` method to convert the serialized json representation of our aggregation into a json response object named `response`.

```twig
{% set response = services.response.json(orderAggregations.first.jsonSerialize) %}
```

Finally, we just set the response of the hook to the result from above:

```twig
{% do hook.setResponse(response) %}
```

It is important to do all this within the `response` block of the twig script. Otherwise, you will get errors when calling the script.

### Installing the plugin

Next, we re-install our plugin using the same command as before:

```shell
shopware-cli project extension upload . --activate
```

::: warning
Remember, if you made changes to the `manifest.xml` file in the meantime, also pass the `--increase-version` parameter, else Shopware will not pick up the changes:

```shell
shopware-cli project extension upload . --activate --increase-version
```

:::

We can now call our endpoint again:

```shell
curl --request GET \
  --url http://<your-store-url>/store-api/script/swag/topseller \
  --header 'sw-access-key: insert-your-access-key'
```

and receive a different result:

```json
{
  "apiAlias": "store_api_swag_topseller_response",
  "buckets": [
    {
      "key": "0060b9b2b3804244bf8ba98cdad50234",
      "count": 3,
      "quantityItemsOrdered": {
        "extensions": [],
        "sum": 15
      },
      "apiAlias": "aggregation_bucket"
    },
    {
      "key": "a65d918f883c47778a65b73548f456ea",
      "count": 2,
      "quantityItemsOrdered": {
        "extensions": [],
        "sum": 3
      },
      "apiAlias": "aggregation_bucket"
    },
    {
      "key": "6b67935063c84bde8e9d86f25a47c69d",
      "count": 3,
      "quantityItemsOrdered": {
        "extensions": [],
        "sum": 8
      },
      "apiAlias": "aggregation_bucket"
    }
  ]
}
```

## Wrap-Up

This tutorial covered the basics of app development using app scripts and some filtering and aggregation logic.

In a proper app, you should consider the following points:

* Input parameter validation
* Format and limit the result
* Define an API contract (endpoint structure) first and build after that
* The search result does not show actual top sellers but just the quantity of products ordered

## Where to continue

* More on adding [custom endpoints](../app-scripts/custom-endpoints)
* See how you can use [Twig functions](../app-scripts/#extended-syntax) in app scripts
* Working with [DAL Aggregations](./../../../../resources/references/core-reference/dal-reference/aggregations-reference)

---

---

