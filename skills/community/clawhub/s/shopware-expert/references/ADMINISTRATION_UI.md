# ADMINISTRATION UI

Compiled excerpts from the Shopware Developer Documentation snapshot. Prefer live docs at [developer.shopware.com](https://developer.shopware.com/) when in doubt.

---

## Administration
**Source:** [guides/plugins/apps/administration.md](https://developer.shopware.com/docs/v6.6/guides/plugins/apps/administration.md)  
# Administration

You can't extend the Shopware Administration by means of freely overriding and extending Administration components, all js files you provide in the `Resources/administration` namespace will be ignored. Instead, you have more defined extension points and can extend the Administration by other means: You are able to [add your own modules](add-custom-modules), [custom fields](../custom-data/custom-fields) or [action buttons](add-custom-action-button) via manifest file.

Starting with version 6.4.2.0 you can also extend Shopware's CMS module by [adding custom CMS blocks](../content/cms/add-custom-cms-blocks).

---

---

## Add CMS Element
**Source:** [guides/plugins/apps/administration/add-cms-element-via-admin-sdk.md](https://developer.shopware.com/docs/v6.6/guides/plugins/apps/administration/add-cms-element-via-admin-sdk.md)  
*(Body truncated in this bundle; follow the link for the rest.)*

# Add CMS Element

## Overview

This article will teach you how to create a new CMS element via the Meteor Admin SDK. The plugin in this example will be named `SwagBasicAppCmsElementExample`, similar to the other guides.

## Prerequisites

* Knowledge on the creation of [Plugins](/docs/guides/plugins/plugins/plugin-base-guide) or [Apps](/docs/guides/plugins/apps/app-base-guide)
* Knowledge on the [creation of custom admin components](/docs/guides/plugins/plugins/administration/add-custom-component#creating-a-custom-component)
* Understanding the [Meteor Admin SDK](/resources/admin-extension-sdk/getting-started/installation)

::: info
This example uses TypeScript, which is recommended, but not required for developing Shopware.
:::

## Creating your custom element

Similar to [Creating a new custom element via plugin](/docs/guides/plugins/plugins/content/cms/add-cms-element#creating-your-custom-element), this article describes creating a new custom element via app.
Creating a new element requires Meteor Admin SDK.

Consider the same scenario to allow a shop manager configure a link to display the Dailymotion video. That is exactly what you are going to build.

### Target structure

You can decide what approach to use when creating apps since everything here is loaded via iFrame. However, Shopware's best practice is a full Vue.js approach.

When our extension is finished, you will get the following file structure:

```bash
// <plugin root>/src/Resources/app/administration/src
├── base
│   └── mainCommands.ts
├── main.ts
├── viewRenderer.ts
└── views
    └── swag-dailymotion
        ├── swag-dailymotion-config.ts
        ├── swag-dailymotion-element.ts
        └── swag-dailymotion-preview.ts
```

## Initial loading of components

Everything starts in the `main.ts` file:

```javascript
// Prior to 6.7
import 'regenerator-runtime/runtime';
import { location } from '@shopware-ag/meteor-admin-sdk';

// Only execute extensionSDK commands when
// it is inside an iFrame
if (location.isIframe()) {
    if (location.is(location.MAIN_HIDDEN)) {
        // Execute the base commands
        import('./base/mainCommands');
    } else {
        // Render different views
        import('./viewRenderer');
    }
}
```

```javascript
// 6.7 and above (inside meteor-app folder)
import 'regenerator-runtime/runtime';
import { location } from '@shopware-ag/meteor-admin-sdk';

if (location.is(location.MAIN_HIDDEN)) {
    // Execute the base commands
    import('./base/mainCommands');
} else {
    // Render different views
    import('./viewRenderer');
}
```

This is the main file, which is executed first and functions as the entry point.

Use `if(location.is(location.MAIN_HIDDEN))` to **load the main commands**, which are defined in the `mainCommands.ts` file. This will only be used to load logic, but not templates into the Administration.

Lastly, the `else` case will be responsible for specific loading of views via `viewRenderer.ts`. This is where the view templates will be loaded.

### Loading all required templates

Now, create the `viewRenderer.ts` file, which includes the three mandatory files needed for a CMS element as below:

* `swag-dailymotion-config.ts`, which will handle the content of the CMS element configuration
* `swag-dailymotion-element.ts`, which represents the actual target element in the CMS
* `swag-dailymotion-preview.ts`, which is responsible for the preview, when selecting the CMS element in its selection screen

Observe that every file is named according to the component and prefixed with `swag-dailymotion`, (vendor prefix) to ensure no other developer accidentally chooses the same name.

Let us see how the component loading via `viewRenderer.ts` looks like:

```javascript
import Vue from 'vue';
import { location } from '@shopware-ag/meteor-admin-sdk';

// watch for height changes
location.startAutoResizer();

// start app views
const app = new Vue({
    el: '#app',
    data() {
        return { location };
    },
    components: {
        'SwagDailymotionElement':
            () => import('./views/swag-dailymotion/swag-dailymotion-element'),
        'SwagDailymotionConfig':
            () => import('./views/swag-dailymotion/swag-dailymotion-config'),
        'SwagDailymotionPreview':
            () => import('./views/swag-dailymotion/swag-dailymotion-preview'),
    },
    template: `
        <SwagDailymotionElement
            v-if="location.is('swag-dailymotion-element')"
        ></SwagDailymotionElement>
        <SwagDailymotionConfig
            v-else-if="location.is('swag-dailymotion-config')"
        ></SwagDailymotionConfig>
        <SwagDailymotionPreview
            v-else-if="location.is('swag-dailymotion-preview')"
        ></SwagDailymotionPreview>
    `,
});
```

Really straightforward, isn't it? As you probably know from Vue.js's Options API, you just need to load, register and use the Vue.js component to make them work.

What's especially interesting here is the use of the `location` object. This is a main concept of the Meteor Admin SDK, where Shopware provides dedicated `locationIds` to offer you places to inject your templates into. For further information on that, it is recommend to take a look at the documentation of the [Meteor Admin SDK](/resources/admin-extension-sdk/concepts/locations) to learn more about its concepts.

In your case, we will get your own **auto-generated** `locationIds`, depending on the name of your CMS element and suffixes, such as `-element`, `-config`, and `-preview`.

Those will be available after **registering the component**, which we will do in the following chapter.

## Registering a new element

For this topic we head to `mainCommands.ts`, since the registration of CMS elements is something to be done in a global scope.

```javascript
import { cms } from '@shopware-ag/meteor-admin-sdk';

const CMS_ELEMENT_NAME = 'swag-dailymotion';
const CONSTANTS = {
    CMS_ELEMENT_NAME,
    PUBLISHING_KEY: `${CMS_ELEMENT_NAME}__config-element`,
};

void cms.registerCmsElement({
    name: CONSTANTS.CMS_ELEMENT_NAME,
    label: 'Dailymotion video',
    defaultConfig: {
        dailyUrl: {
            source: 'static',
            value: '',
        },
    },
});

export default CONSTANTS;
```

At first, you import the Meteor Admin SDK's cms object, used for `cms.registerCmsElement` to register a new element.

That is all about what is required to register your CMS element. As a best practice, it is recommended to create a **constant** for the CMS element name and the publishing key. This makes it easier to maintain and keep track of changes. The publishing key can be predefined since the name must be a combination of CMS element name and the `__config-element` suffix as shown above.

## Templates and communication with the Administration

The last files are the components inside our `views` folder. Just like you know it from typical CMS element loading, we will create a folder with the full component name, containing 3 files as shown below:

```bash
// <plugin root>/src/Resources/app/administration/src
views
└── swag-dailymotion
    ├── swag-dailymotion-config.ts
    ├── swag-dailymotion-element.ts
    └── swag-dailymotion-preview.ts
```

You can vary the structure of `swag-dailymotion`'s contents and create folders for each of the three. However, let us keep it simple with single file components.

### The config file

Let's go through each of the files to talk about it's contents, starting with `swag-dailymotion-config.ts`:

```javascript
import Vue from 'vue'
import { data } from "@shopware-ag/meteor-admin-sdk";
import CONSTANTS from "../../base/mainCommands";

export default Vue.extend({
    template: `
        <div>
          <h2>
            Config!
          </h2>
          Video-Code: <input v-model="dailyUrl" type="text"/><br/>
        </div>
    `,

    data(): Object {
        return {
            element: null
        }
    },

    computed: {
        dailyUrl: {
            get(): string {
                return this.element?.config?.dailyUrl?.value || '';
            },

            set(value: string): void {
                this.element.config.dailyUrl.value = value;

                data.update({
                    id: CONSTANTS.PUBLISHING_KEY,
                    data: this.element,
                });
            }
        }
    },

    created() {
        this.createdComponent();
    },

    methods: {
        async createdComponent() {
            this.element = await data.get({ id: CONSTANTS.PUBLISHING_KEY });
        }
    }
});
```

This file is the config component used to define every type of configuration for the CMS element. Most of the code will be common for experienced Shopware 6 developers, so here are some important highlights:

* Import `data` from the Meteor Admin SDK, which is required for data handling between this app and Shopware
* The `element` variable contains the typical CMS element object and is also used to manage the element configuration you want to edit
* The `publishingKey` is used to tell the Meteor Admin SDK in Shopware what piece of information you want to fetch. In this case, you need the `element` data

So, now you need a simple input field to get a `dailyUrl` for the Dailymotion video to be displayed. For that, first fetch the element via `data.get()` as seen in `createdComponent` and then link it to the computed property `dailyUrl` with getters and setters to mutate it. Using `data.update({ id, data })` you provide the publishing key `id` as a target and `data` for the data you want to save in Shopware.

With these small additions to typical CMS element behavior, you have already done with the config modal.

![Dailymotion config modal](../../../../assets/add-cms-element-via-admin-sdk-config.png)

### The element file

Now let's have a look at the result of `swag-dailymotion-element.ts`:

```javascript
import Vue from 'vue'
import { data } from "@shopware-ag/meteor-admin-sdk";
import CONSTANTS from "../../base/mainCommands";

export default Vue.extend({
    template: `
        <div>
            <h2>
              Element!
            </h2>
            <div class="sw-cms-el-dailymotion">
                <div class="sw-cms-el-dailymotion-iframe-wrapper">
                    <iframe
                        frameborder="0"
                        type="text/html"
                        width="100%"
                        height="100%"
                        :src="dailyUrl">
                    </iframe>
                </div>
            </div>
        </div>
    `,

    data(): { element: object|null } {
        return {
            element: null
        }
    },

    computed: {
        dailyUrl(): string {
            return `https://www.dailymotion.com/embed/video/${this.element?.config?.dailyUrl?.value || ''}`;
        }
    },

    created() {
        this.createdComponent();
    },

    methods: {
        async createdComponent() {
            this.element = await data.get({ id: CONSTANTS.PUBLISHING_KEY });
            data.subscribe(CONSTANTS.PUBLISHING_KEY, this.elementSubscriber);
        },

        elementSubscriber(response: { data: unknown, id: string }): void {
            this.element = response.data;
        }
    }
});
```

Here, you have the main rendering logic for the Administration's CMS element. This file shows what your element will look like when it's done. So besides a template and the computed `dailyUrl`, used to correctly load the Dailymotion video player, the only interesting part is the `createdComponent` method.

It initially fetches the `element` data, as you've already seen it in the config file. After that, using `data.subscribe(id, method)` it subscribes to the publishing key, which will update the element data automatically if something changes. It doesn't matter if the changes originate from our config modal outside Shopware or from somewhere else inside Shopware.

![Dailymotion CMS element](../../../../assets/add-cms-element-via-admin-sdk-element.

… **Truncated.** Full document: https://developer.shopware.com/docs/v6.6/guides/plugins/apps/administration/add-cms-element-via-admin-sdk.md


---

## Add custom action button
**Source:** [guides/plugins/apps/administration/add-custom-action-button.md](https://developer.shopware.com/docs/v6.6/guides/plugins/apps/administration/add-custom-action-button.md)  
# Add custom action button

:::info
This guide will show you how to add custom action buttons to the Shopware Administration using your manifest file. This works for simple applications; however, if you want to write more advanced applications, the [Meteor Admin SDK](/resources/admin-extension-sdk/) is recommended. It has many more features and is more flexible.

For further details and guidance on custom action buttons, refer to the documentation provided on the Meteor Admin SDK's [action button](/resources/admin-extension-sdk/api-reference/ui/actionButton) section.
:::

One extension possibility in the Administration is the ability to add custom action buttons to the smartbar. For now, you can add them in the smartbar of detail and list views:

![Custom action buttons in the Administration](../../../../assets/custom-buttons.png)

To get those buttons, you start in the `admin` section of your manifest file. There you can define `<action-button>` elements in order to add your button, as seen as below:

::: code-group

```xml [manifest.xml]
<?xml version="1.0" encoding="UTF-8"?>
<manifest xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://raw.githubusercontent.com/shopware/shopware/trunk/src/Core/Framework/App/Manifest/Schema/manifest-2.0.xsd">
    <meta>
        ...
    </meta>
    <admin>
        <action-button action="setPromotion" entity="promotion" view="detail" url="https://example.com/promotion/set-promotion">
            <label>set Promotion</label>
        </action-button>
        <action-button action="deletePromotion" entity="promotion" view="detail" url="https://example.com/promotion/delete-promotion">
            <label>delete Promotion</label>
        </action-button>
        <action-button action="restockProduct" entity="product" view="list" url="https://example.com/restock">
            <label>restock</label>
        </action-button>
    </admin>
</manifest>
```

:::

For a complete reference of the structure of the manifest file take a look at the [Manifest reference](../../../../resources/references/app-reference/manifest-reference).

An action button must have the following attributes:

* `action`: Unique identifier for the action, can be set freely.
* `entity`: Here you define which entity you're working on.
* `view`: `detail`or `list`;  to set the view the button should be added to. Currently, you can choose between detail and listing view.

When the user clicks on the action button your app receives a request similar to the one generated by a [webhook](../app-base-guide#webhooks).
The main difference is that it contains the name of the entity and an array of ids that the user selected (or an array containing only a single id if the action button was executed on a detail page).

A sample payload may look like the following:

```json
{
  "source":{
    "url":"http:\/\/localhost:8000",
    "appVersion":"1.0.0",
    "shopId":"F0nWInXj5Xyr"
  },
  "data":{
    "ids":[
      "2132f284f71f437c9da71863d408882f"
    ],
    "entity":"product",
    "action":"restockProduct"
  },
  "meta":{
    "timestamp":1592403610,
    "reference":"9e968471797b4f29be3e3cf09f52d8da",
    "language":"2fbb5fe2e29a4d70aa5854ce7ce3e20b"
  }
}
```

```php
// injected or build by yourself
$shopResolver = new ShopResolver($repository);
$contextResolver = new ContextResolver();

$shop = $shopResolver->resolveShop($serverRequest);
$actionButton = $contextResolver->assembleActionButton($serverRequest, $shop);
```

```php
use Shopware\App\SDK\Context\ActionButton\ActionButtonAction;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\HttpKernel\Attribute\AsController;
use Symfony\Component\Routing\Attribute\Route;
use Psr\Http\Message\ResponseInterface;

#[AsController]
class ActionButtonController {
    #[Route('/action/product/detail')]
    public function handle(ActionButtonAction $button): ResponseInterface
    {
        // handle button
        
        return ActionButtonResponse::notification('success', 'Success message');
    }
}
```

::: info
Starting from Shopware version 6.4.1.0, the current shopware version will be sent as a `sw-version` header.
:::

Again you can verify the authenticity of the incoming request, like with [webhooks](../app-base-guide#webhooks), by checking the `shopware-shop-signature` it too contains the SHA256 HMAC of the request body, that is signed with the secret your app assigned the shop during the [registration](../app-base-guide#setup).

## Providing feedback in the Administration

::: info
This feature was added in Shopware 6.4.3.0, previous versions will ignore the response content.
:::

::: info
Starting from Shopware version 6.4.8.0, the requests of the [tab](#opening-a-new-tab-for-the-user) and [custom modal](#open-a-custom-modal) have the following additional query parameters:

* `shop-id`
* `shop-url`
* `timestamp`
* `sw-context-language`
* `sw-user-language`
* `shopware-shop-signature`

You **must** make sure to verify the authenticity of the incoming request by checking the `shopware-shop-signature`, which is a hash of the request's query part, signed with the shop's secret key.
:::

If you want to trigger an action inside the Administration upon completing the action, the app should return a response with a valid body and the header `shopware-app-signature` containing the SHA256 HMAC of the whole response body signed with the app secret.
If you do not need to trigger any actions, a response with an empty body is also always valid.

### Opening a new tab for the user

Examples response body:
To open a new tab in the user browser you can use the `openNewTab` action type. You need to pass the url that should be opened as the `redirectUrl` property inside the payload.

```txt
Content-Type: application/json

{
  "actionType": "openNewTab",
  "payload": {
    "redirectUrl": "http://google.com"
  }
}
```

```php
use Shopware\App\SDK\Response\ActionButtonResponse;

ActionButtonResponse::openNewTab('https://www.shopware.com');
```

### Show a notification to the user

To send a notification, you can use the `notification` action type. You need to pass the `status` property and the content of the notification as `message` property inside the payload.

```json
{
  "actionType": "notification",
  "payload": {
    "status": "success",
    "message": "This is the successful message"
  }
}
```

```php
use Shopware\App\SDK\Response\ActionButtonResponse;

ActionButtonResponse::notification('success', 'foo');
```

### Reload the current page

To reload the data in the user's current page you can use the `reload` action type with an empty payload.

```json
{
  "actionType": "reload",
  "payload": {}
}
```

```php
use Shopware\App\SDK\Response\ActionButtonResponse;

ActionButtonResponse::reload();
```

### Open a custom modal

To open a modal with the embedded link in the iframe, you can use the `openModal` action type. You need to pass the url that should be opened as the `iframeUrl` property and the `size` property inside the payload.

```json
{
  "actionType": "openModal",
  "payload": {
    "iframeUrl": "http://google.com",
    "size": "medium",
    "expand": true
  }
}
```

```php
use Shopware\App\SDK\Response\ActionButtonResponse;

ActionButtonResponse::modal('https://shopware.com', size: 'medium', expand: true)
```

### General structure

* `actionType`: The type of action the app want to be triggered, including `notification`, `reload`, `openNewTab`, `openModal`
* `payload`: The needed data to perform the action.
  * `redirectUrl`: The url to open new tab
  * `iframeUrl`: The embedded link in modal iframe
  * `status`: Notification status, including `success`, `error`, `info`, `warning`
  * `message`: The content of the notification
  * `size`: The size of the modal in `openModal` type, including `small`, `medium`, `large`, `fullscreen`, default `medium`
  * `expand`: The expansion of the modal in `openModal` type, including `true`, `false`, default `false`

## Using Custom Endpoints as target

It is also possible to use [custom endpoints](../app-scripts/custom-endpoints) as target for action buttons.

::: info
This feature was added in Shopware 6.4.10.0, previous versions don't support relative target urls for action buttons.
:::

To use custom endpoints as the target url for action buttons you can define the target url as a relative url in your apps manifest.xml:

::: code-group

```xml [manifest.xml]
<?xml version="1.0" encoding="UTF-8"?>
<manifest xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://raw.githubusercontent.com/shopware/shopware/trunk/src/Core/Framework/App/Manifest/Schema/manifest-2.0.xsd">
    <meta>
        ...
    </meta>
    <admin>
      <action-button action="test-button" entity="product" view="list" url="/api/script/action-button">
        <label>test-api-endpoint</label>
      </action-button>
    </admin>
</manifest>
```

:::

And then add the corresponding app script that should be executed when the user clicks the action button.

```twig
// Resources/scripts/api-action-button/action-button-script.twig
{% set ids = hook.request.ids %}

{% set response = services.response.json({
    "actionType": "notification",
    "payload": {
        "status": "success",
        "message": "You selected " ~ ids|length ~ " products."
    }
}) %}

{% do hook.setResponse(response) %}
```

As you can see it is possible to provide a [`JsonResponse`](../../../../resources/references/app-reference/script-reference/custom-endpoint-script-services-reference#json) to give [feedback to the user in the administration](#providing-feedback-in-the-administration).

---

---

## Add custom module
**Source:** [guides/plugins/apps/administration/add-custom-modules.md](https://developer.shopware.com/docs/v6.6/guides/plugins/apps/administration/add-custom-modules.md)  
# Add custom module

:::info
This guide will show you how to add custom modules to the Shopware Administration using your manifest file. This works for simple applications; however, if you want to write more advanced applications, the [Meteor Admin SDK](/resources/admin-extension-sdk/) is recommended. It has many more features and is more flexible.

For further details and guidance on custom modules, refer to the documentation provided on the Meteor Admin SDK's [custom modules](/resources/admin-extension-sdk/api-reference/ui/mainModule) section.
:::

## Prerequisites

You should be familiar with the concept of Apps, especially their registration flow as well as signing and verifying requests and responses between Shopware and the App backend server, as that is required to authenticate the requests coming from the shops and showing the correct content in your modules.

## Overview

In your app, you are able to add your own modules to the Administration. Your custom modules are loaded as iframes which are embedded in the Shopware Administration and within this iframe, your website will be loaded and shown.

Creating custom modules takes place at the `<admin>` section of your `manifest.xml`. Take a look at the [Manifest Reference](../../../../resources/references/app-reference/manifest-reference) You can add any amount of custom modules by adding new `<module>` elements to your manifest.

To configure your module, you can set it up with with some additional attributes.

* `name` (required): The technical name of the module. This is the name your module is referenced with.
* `parent` (required): The Administration navigation id of the menu item that serves as the parent menu item.
* `source` (optional): The URL to your app servers endpoint from which the module is served from. This can be omitted if you want to define a menu item that should serve as a parent menu item for other app modules.
* `parent` (optional): The Administration navigation id from the menu item that serves as the parent menu item. If omitted your module will be listed under the "My apps" menu entry. **This field will be required in future versions as we are going to remove the "My Apps" menu item**
* `position` (optional): A numeric index that sets the position of your menu entry regarding to it's siblings.

Additionally you can define `label` elements inside of your `module` element, to set up how your module will be displayed in the admin menu.

::: code-group

```xml [manifest.xml]
<?xml version="1.0" encoding="UTF-8"?>
<manifest xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://raw.githubusercontent.com/shopware/shopware/trunk/src/Core/Framework/App/Manifest/Schema/manifest-2.0.xsd">
    <meta>
        ...
    </meta>
    <admin>
        <module name="exampleModule"
                source="https://example.com/promotion/view/promotion-module"
                parent="sw-marketing"
                position="50"
        >
            <label>Example module</label>
            <label lang="de-DE">Beispiel Modul</label>
        </module>
    </admin>
</manifest>
```

:::

For a complete reference of the structure of the manifest file, take a look at the [Manifest reference](../../../../resources/references/app-reference/manifest-reference).

If the user opens the module in the Administration your app will receive a request to the URL defined in the `source` attribute of your `module` element. Your app can determine the shop that has opened the module through query parameters added to the url:

* `shop-id`: The unique identifier of the shop, where the app was installed
* `shop-url`: The URL of the shop, this can later be used to access the Shopware API
* `timestamp`: The Unix timestamp when the request was created
* `shopware-shop-signature`: SHA256 HMAC of the rest of the query string, signed with the `shop-secret`

A sample request may look like this:

```text
https://example.com/promotion/view/promotion-config?shop-id=HKTOOpH9nUQ2&shop-url=http%3A%2F%2Fmy.shop.com&timestamp=1592406102&shopware-shop-signature=3621fffa80187f6d43ce6cb25760340ab9ba2ea2f601e6a78a002e601579f415
```

In this case the `shopware-shop-signature` parameter contains an SHA256 HMAC of the rest of the query string, signed again with the secret your app assigned the shop during the [registration](../app-base-guide#setup). The signature can be used to verify the authenticity of the request.

```php
// injected or build by yourself
$shopResolver = new ShopResolver($repository);
$contextResolver = new ContextResolver();

$shop = $shopResolver->resolveShop($serverRequest);
$module = $contextResolver->assembleModule($serverRequest, $shop);
```

```php
use Shopware\App\SDK\Context\Module\ModuleAction;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\HttpKernel\Attribute\AsController;
use Symfony\Component\Routing\Attribute\Route;

#[AsController]
class ModuleController {
    #[Route('/module')]
    public function show(ModuleAction $module): Response
    {
        // handle payment
        
        return $this->render('....');
    }
}
```

## Leave loading state

Because your module is displayed as an iframe in the Administration, Shopware can not easily tell when your module has finished loading. Therefore, your new module will display a loading spinner to signalize your iframe is loading. To leave the loading state, your iframe needs to give a notification when the loading process is done.

```javascript
function sendReadyState() {
    window.parent.postMessage('sw-app-loaded', '*');
}
```

This has to be done as soon as everything is loaded so that the loading spinner disappears. If your view is not fully loaded after 5 seconds, it will be aborted.

## Structure your modules

With Shopware 6.4.0.0 we added a third level in the admin menu structure. This change was made to give you as a developer the opportunity to group your Administration modules if needed.

When you define a module, it gets automatically loaded by the Administration. Additionally the Administration creates a menu entry for your module. You can reference this menu entry and set it as the parent menu entry for your other modules.

The navigation id of your modules always uses the pattern `app-<appName>-<moduleName>`. So, within your manifest you can add a reference to modules that you just created:

::: code-group

```xml [manifest.xml]
<?xml version="1.0" encoding="UTF-8"?>
<manifest xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://raw.githubusercontent.com/shopware/shopware/trunk/src/Core/Framework/App/Manifest/Schema/manifest-2.0.xsd">
    <meta>
        <name>myApp</app>
        ...
    </meta>
    <admin>
        <module name="myModules"
                source="https://example.com/promotion/view/promotion-module"
                parent="sw-catalogue"
                position="50"
        >
            <label>My apps modules</label>
            <label lang="de-DE">Module meiner app</label>
        </module>

        <module name="someModule"
                source="https://example.com/promotion/view/promotion-module"
                parent="app-myApp-myModules"
                position="1"
        >
            <label>Module underneath "My apps modules"</label>
            <label lang="de-DE">Modul unterhalb von "Module meiner app"</label>
        </module>
    </admin>
</manifest>
```

:::

Modules that are used as a parent for other modules do not need the `source` attribute to be set, although they can.

## Add main module to your app

With Shopware 6.4.0.0 You can define a main module for your app. This "special" module will be opened from the list of your installed apps as well as from the app detail page if you bought it from the Shopware store.

Your main module can be defined by adding a `main-module` element within your `administration` section of your manifest file. It's only required attribute is the `source` attribute.

To avoid mixing other modules with your main module, we decided to separate the main module from modules with navigation entries. You can still use the same URL on both, a module that is available through the menu and your main module.

::: code-group

```xml [manifest.xml]
<?xml version="1.0" encoding="UTF-8"?>
<manifest xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://raw.githubusercontent.com/shopware/shopware/trunk/src/Core/Framework/App/Manifest/Schema/manifest-2.0.xsd">
    <meta>
        <name>myApp</app>
        ...
    </meta>
    <admin>
        <module name="normalModule"
                source="https://example.com/main"
                parent="sw-catalogue"
                position="50"
        >
            <label>Module in admin menu</label>
            <label lang="de-DE">Modul im Adminmenü</label>
        </module>

        <!-- You can use the same url to open your module from the app store -->
        <main-module source="https://example.com/main"/>
    </admin>
</manifest>
```

:::

This feature is not compatible with themes as they will always open the theme config by default.

## Admin design compatibility

As your module page is integrated as an iframe you are not able to use the stylesheet and javascript out of the box.
Having the stylesheets that are used in the Administration can be beneficial for the app module to seamlessly integrate into the Administration.
You can use the shop version that is passed as `sw-version` within the request query to determine what stylesheets you want to load.
The compiled Administration stylesheets for each version can be found within the tagged releases of the `shopware/administration` package within the `Resources/public/static` folder.
Combining this information enables your app to look exactly like the Administration, although it is encapsulated within an iframe.

---

---

## Adding translations for apps
**Source:** [guides/plugins/apps/administration/adding-snippets.md](https://developer.shopware.com/docs/v6.6/guides/plugins/apps/administration/adding-snippets.md)  
# Adding translations for apps

Adding snippets to the administration works the same way for plugins and apps. The only difference is the file structure and that apps are not allowed to override existing snippet keys. The only thing to do, therefore, is to create new files in the following directory: `<app root>/Resources/app/administration/snippet`
Additionally, you need JSON file for each language you want to support, using its specific language locale, e.g. `de-DE.json`, `en-GB.json`.

Since everything else works the same, please refer to our [Adding translations for plugins](../../plugins/administration/adding-snippets) guide for more information.

---

---

## Meteor Admin SDK
**Source:** [guides/plugins/apps/administration/meteor-admin-sdk.md](https://developer.shopware.com/docs/v6.6/guides/plugins/apps/administration/meteor-admin-sdk.md)  
# Meteor Admin SDK

The [Meteor Admin SDK](https://github.com/shopware/meteor/tree/main/packages/admin-sdk) is an NPM library for Shopware 6 apps and plugins that need an easy way to extend or customize the administration.

To write advanced apps, its recommended that you use the [Meteor Admin SDK](https://github.com/shopware/meteor/tree/main/packages/admin-sdk). It contains helper functions to communicate with the Administration, execute actions, subscribe to data or extend the user interface. It has many more features and is more flexible.

* 🏗  **Works with Shopware 6 Apps and Plugins:** You can use the SDK for your plugins or apps. API usage is identical.
* 🎢  **Shallow learning curve:** You don't need to have extensive knowledge about the internals of the Shopware 6 Administration. Our SDK hides the complicated stuff behind a beautiful API.
* 🧰  **Many extension capabilities:** Includes throwing notifications, accessing context information, extending the current UI and more. The feature set of the SDK will gradually be extended, providing more possibilities and flexibility for your ideas and solutions.
* 🪨  **A stable API with great backwards compatibility:** Don't fear Shopware updates anymore. Breaking changes in this SDK are an exception. If you use the SDK, your apps and plugins will stay stable for a longer time, without any need for code maintenance.
* 🧭  **Type safety:** The whole SDK is written in TypeScript which provides great autocompletion support and more safety for your apps and plugins.
* 💙  **Developer experience:** Have a great development experience right from the start. And it will become better and better in the future.
* 🪶  **Lightweight:** The whole library is completely tree-shakable and dependency-free. Every functionality can be imported granularly to keep your bundle as small and fast as possible.

Go to [Installation](/resources/admin-extension-sdk/getting-started/installation/) to get started. Or check out the [quick start guide](/resources/admin-extension-sdk/#quick-start).

---

---

## Administration
**Source:** [guides/plugins/plugins/administration.md](https://developer.shopware.com/docs/v6.6/guides/plugins/plugins/administration.md)  
# Administration

Shopware allows to extend the functionality of the Shopware administration panel, providing additional features and customization options for managing the e-commerce platform. The plugin allows businesses to tailor the administration interface to their specific needs, adding custom sections, modules, services, or functionalities to streamline their workflow and enhance the user experience. The administration plugin offers flexibility in configuring dashboards, menu structures, permissions, and settings, empowering businesses to create a customized and efficient administration experience that aligns with their unique requirements.

---

---

## Adding permissions
**Source:** [guides/plugins/plugins/administration/add-acl-rules.md](https://developer.shopware.com/docs/v6.5/guides/plugins/plugins/administration/add-acl-rules.md)  
*(Body truncated in this bundle; follow the link for the rest.)*

# Adding permissions

## Overview

This guide will teach you how to add Access Control Lists to the Shopware 6 Administration. Access Control Lists or ACL in Shopware ensure that you can create individual roles. These roles have finely granular rights, which every shop operator can set up for themselves. They can be assigned to users.

As an example, let's take a look at a role called 'Editor'. We would assign this role rights to edit products, categories and manufacturers. Now, every user who is a 'Editor' would be able to see and edit the specific areas which are defined in the role.

This documentation chapter will cover the following topics:

* What is an admin privilege
* How to register new admin privileges for your plugin
* How to protect your plugin routes
* How to protect your menu entries
* How to add admin snippets for your privileges
* How you can check in your module at any place if the user has the required rights

Note: ACL Rules in the Administration can be circumnavigated by making direct API calls to your backend.

## Prerequisites

All you need for this guide is a running Shopware 6 instance and full access to both the files and a running plugin. A basic understanding of the [vue router](https://router.vuejs.org/) is also required. Of course you'll have to understand JavaScript, but that's a prerequisite for Shopware as a whole and will not be taught as part of this documentation.

## Admin privileges

Admin privileges are higher-level permissions that are always determined by an explicit identifier. This is made up of a 'key' and the 'role', connected by a dot: `.`.

A distinction is made here between normal `permissions` and `additional_permissions`. Let's start with the normal permissions.

### Normal permissions

![Permissions GUI](../../../../assets/permissions-gui.png)

`permissions`:

* Key: `product`
* Role: `viewer`
* Identifier (Key + Role): `product.viewer`

The key describes the higher-level admin privilege. For normal `permissions` this is usually the module name, `product` in this case. Other keys could be for example `manufacturer`, `shopping_experiences` or `customers`. The key is used to group the admin privileges, as seen in the picture above.

The role indicates which authorization is given for the key. So four predefined roles are available for the normal `permissions`:

* `viewer`: The viewer is allowed to view entities
* `editor`: The editor is allowed to edit entities
* `creator`: The Creator is allowed to create new entities
* `deleter`: The Deleter is allowed to delete entities

It is important to note that these combinations are not API permissions. They are only intended to enable, disable, deactivate or hide certain elements in the Administration.

For each admin privilege, the needed entity privileges need to be assigned. Depending on the admin privileges, these can be much more complex. This means that for example if a user should be allowed to view reviews, then they also have to be allowed to view customers, products and sales channels.

### Additional permissions

In addition to the normal `permissions`, which represent CRUD functionality, there are also `additional_permissions`. These are intended for all functions that cannot be represented by CRUD.

![Additional permissions GUI](../../../../assets/additionalPermissions-gui.png)

The `additional_permissions` have their own card below the normal permissions grid. An example for `additional_permissions` would be: "clearing the cache". This is an individual action without CRUD functionalities. The key is still used for grouping. Therefore the role can be individual and does not have to follow the scheme.

`additional_permissions`:

* Key: `system`
* Role: `clear_cache`
* Identifier (Key + Role): `system.clear_cache`

## Register admin privilege

The privilege service is used to handle privileges in the Administration. Those privileges will then be displayed in the Users & Permissions module under the roles.

Privileges can be added or extended with the Method `addPrivilegeMappingEntry` of the privilege service:

| Property | Description |
| :--- | :--- |
| category | Where the privilege should be visible in the `permissions` grid or in the `additional_permissions` |
| parent | For nesting and gaining a better overview, you can add a parent key. If the privilege does not have a parent then use `null`. |
| key | All privileges with the same key will be grouped together. For normal `permissions` each role will be in the same row. |
| roles | When category is `permissions`: Use `viewer`, `editor`, `creator` and `deleter`. |
|  | When category is `additional_permissions`: Use a custom key because the additional permissions don´t enforce a structure. |

Each role in roles:

| Property | Description |
| :--- | :--- |
| privileges | You need to add all API permissions here which are required for an working admin privilege. The structure is `entity_name:operation`, e.g. 'product:read'. |
| dependencies | In some cases it is necessary to automatically check another role. To do this, you need to add the identifier, e.g. `product.viewer`. |

Here's an example how this can look like for the review functionality in the Administration:

```javascript
Shopware.Service('privileges')
    .addPrivilegeMappingEntry({
        category: 'permissions',
        parent: 'catalogues',
        key: 'review',
        roles: {
            viewer: {
                privileges: [
                    'product_review:read',
                    'customer:read',
                    'product:read',
                    'sales_channel:read'
                ],
                dependencies: []
            },
            editor: {
                privileges: [
                    'product_review:update'
                ],
                dependencies: [
                    'review.viewer'
                ]
            },
            creator: {
                privileges: [
                    'product_review:create'
                ],
                dependencies: [
                    'review.viewer',
                    'review.editor'
                ]
            },
            deleter: {
                privileges: [
                    'product_review:delete'
                ],
                dependencies: [
                    'review.viewer'
                ]
            }
        }
    });
```

### Adding new, normal permissions

You could use the service at any point in your code. However, it's important that it will be called before the user goes to the roles detail page. For convenience, we recommend this pattern:

```text
- <plugin root>/src/Resources/app/administration/src/<your-component>/
    - acl
        - index.js -> contains permission
    - ...
    - index.js -> import './acl'
```

Now you can use the method `addPrivilegeMappingEntry` to add a new entry:

To add a new mapping for your custom key use the following approach:

```javascript
// <plugin root>/src/Resources/app/administration/src/<your-component>/acl/index.js

Shopware.Service('privileges').addPrivilegeMappingEntry({
    category: 'permissions',
    parent: null,
    key: 'your_key',
    roles: {
        viewer: {
            privileges: [],
            dependencies: []
        },
        editor: {
            privileges: [],
            dependencies: []
        },
        creator: {
            privileges: [],
            dependencies: []
        },
        deleter: {
            privileges: [],
            dependencies: []
        }
    }
});
```

### Extending existing normal permissions

Adding privileges to an existing key can be done like this:

```javascript
// <plugin root>/src/Resources/app/administration/src/acl-override/index.js

Shopware.Service('privileges').addPrivilegeMappingEntry({
    category: 'permissions',
    parent: null,
    key: 'product',
    roles: {
        viewer: {
            privileges: ['plugin:read']
        },
        editor: {
            privileges: ['plugin:update']
        },
        newrole: {
            privileges: ['plugin:write']
        }
    }
});
```

Note: This file has to be imported in the `main.js` file which has to be placed in the `<plugin root>/src/Resources/app/administration/src` directory in order to be automatically found by Shopware 6.

### Register additional permissions

To add privileges to the card `additional_permissions` you need to set `additional_permissions` in the property category. The main difference to normal permissions is that you can choose every role key you want.

Here's an example for `additional_permissions`:

```javascript
Shopware.Service('privileges').addPrivilegeMappingEntry({
    category: 'additional_permissions',
    parent: null,
    key: 'system',
    roles: {
        clear_cache: {
            privileges: ['system:clear:cache'],
            dependencies: []
        }
    }
});
```

Here, the key is `system` to group the permission together with other system specific permissions. However, you can feel free to add your own names here.

## Get permissions from other privilege mappings

In case you have many dependencies which are the same as in other modules, you can import them here. This can be useful if you have components in your module which have complex privileges. Some examples can be found in the rule builder or the media module. You can get these privileges with the method `getPrivileges` of the service.

See this example here:

```javascript
Shopware.Service('privileges').addPrivilegeMappingEntry({
    category: 'permissions',
    parent: null,
    key: 'product',
    roles: {
        viewer: {
            privileges: [
                'product.read',
                Shopware.Service('privileges').getPrivileges('rule.viewer')
            ],
            dependencies: []
        }
    }
})
```

Now all users with the privilege `product.viewer` automatically have access to all privileges from the `rule.viewer`.

Important: The user still has no access to the module itself in the Administration. This means that the example above doesn't give a user access to the `rule` module.

## Protect your plugin routes

It's easy to protect your routes for users without the appropriate privileges. Just add `privilege` to the `meta` property in your route:

```javascript
Module.register('your-plugin-module', {
    routes: {
        detail: {
            component: 'your-plugin-detail',
            path: 'your-plugin',
            meta: {
                privilege: 'your_key.your_role' // e.g. 'product.viewer'
            }
        }    
    }
});
```

## Protect your plugin menu entries

Similar to the routes, you can to add the property `privilege` to your navigation settings to hide it:

```javascript
Module.register('your-plugin-module', {
    navigation: [{
        id: 'your-plugin',
        ...,
        privilege: 'your_key.your_role' // e.g. product.viewer
    }]
});
```

or in the settings item:

```javascript
Module.register('your-plugin-module', {
    settingsItem: [{
        group: 'system',
        to: 'sw.your.plugin.detail',
        privilege: 'your_key.your_role' // e.g. product.viewer
    }]
});
```

## Add snippets for your privileges

To create translations for the labels of the permissions you need to add snippet translations. The path is created automatically for you:

For group titles:

```text
sw.privileges.${category}.${key}.label
// e.g. sw.privileges.permissions.product.label
// e.g. sw.privileges.additional_permissions.system.label
```

For specific roles (only needed in `additional_permissions`):

```text
sw.privileges.${category}.${key}.${role_key} 
// e.g. sw.privileges.additional_permissions.system.clear_cache
```

Just add the snippets to your snippets file:

```json
{
  "sw-privileges": {
    "permissions": {
      "review": {
        "label": "Reviews"
      }
    },
    "additional_permissions": {
      "system": {
        "label": "System",
        "clear_cache": "Clear cache"
      }
    }
  }
}
```

## Use the privi

… **Truncated.** Full document: https://developer.shopware.com/docs/v6.5/guides/plugins/plugins/administration/add-acl-rules.md


---

## Add custom component
**Source:** [guides/plugins/plugins/administration/add-custom-component.md](https://developer.shopware.com/docs/v6.5/guides/plugins/plugins/administration/add-custom-component.md)  
# Add custom component

## Overview

Since the Shopware 6 Administration is using [VueJS](https://vuejs.org/) as its framework, it also supports creating custom components. This guide will teach you how to register your own custom component with your plugin.

In this example, you will create a component that will print a 'Hello world!' everywhere it's being used.

## Prerequisites

This guide **does not** explain how to create a new plugin for Shopware 6. Head over to our Plugin base guide to learn how to create a plugin at first:

If you want to work with entities in your custom component or page, it might be useful to take a look at how to create a custom entity guide first:

Especially if you want to add a new page for an own module, you should consider looking at the process on how to add a custom module first.

This way, you're able to start building your own module in the right order.

### Injecting into the Administration

Same as with all custom extensions of the Administration, the main entry point to extend the Administration via plugin is the `main.js` file. It has to be placed into a `<plugin root>/src/Resources/app/administration/src` directory in order to be found by Shopware 6.

## Creating a custom component

### Path to the component

Usually there's one question you have to ask yourself first: Will your new component be used as a `page` for your plugin's custom route, or is this going to be a component to be used by several other components, such as an element that prints 'Hello world' everywhere it's used? In order to properly structure your plugin's code and to be similar to the core structure, you have to answer this question first. If it's going to be used as page for a module, it should be placed here: `<plugin-root>/src/Resources/app/administration/src/module/<your module's name>/page/<your component name>`

Otherwise, if it's going to be a general component to be used by other components, the following will be the proper path. For this example, this component scenario is used. `<plugin-root>/src/Resources/app/administration/src/component/<name of your plugin>/<name of your component>`

::: info
Using this path is **not** a hard requirement, but rather a recommendation. This way, third party developers having a glance at your code will get used to it real quick, because you stuck to Shopware 6's core conventions.
:::

Since the latter example is being used, this is the path being created in the plugin now: `<plugin-root>/src/Resources/app/administration/src/component/custom-component/hello-world`

### Import your custom component via main.js file

In the directory mentioned above, create a new file `index.js`. We will get you covered with more information about it later. Now import your custom component using your plugin's `main.js` file:

You can use the `Shopware.Component.register` method to register your component. This method expects a name and a function that will import your component. By using a dynamic import here, your component will be loaded asynchronously when it's being used.

```javascript
// <plugin root>/src/Resources/app/administration/src
Shopware.Component.register('hello-world', () => import('./component/custom-component/hello-world'));
```

To import your component synchronously, you need to import it directly in the `main.js` file. The component registration
will be done in the `index.js` file of your component.

```javascript
// <plugin root>/src/Resources/app/administration/src
import './component/custom-component/hello-world';
```

### Index.js as main entry point for this component

Head back to the `index.js` file, this one will be the most important for your component.

The structure of this file depends on the type of your component. If it loads synchronously, you need to register your component directly in this file. If it loads asynchronously, you can just export the component and register it in the `main.js` file.

```javascript
export default Shopware.Component.wrapComponentConfig({
    // Configuration here
});
```

```javascript
// <plugin-root>/src/Resources/app/administration/src/component/custom-component/hello-world
Shopware.Component.register('hello-world', {
    // Configuration here
});
```

A component's template is being defined by using the `template` property. For this short example, the template will be defined inline. An example for a bigger template will also be provided later on this page.

```javascript
// <plugin-root>/src/Resources/app/administration/src/component/custom-component/hello-world
export default Shopware.Component.wrapComponentConfig('hello-world', {
    template: '<h2>Hello world!</h2>'
});
```

That's it. You can now use your component like this `<hello-world></hello-world>` in any other template in the Administration.

### Long template example

It's quite uncommon to have such a small template example and you don't want to define huge templates inside a javascript file. For this case, just create a new template file in your component's directory, which should be named after your component. For this example `hello-world.html.twig` is used.

Now simply import this file in your component's JS file and use the variable for your property.

```javascript
// <plugin-root>/src/Resources/app/administration/src/component/custom-component/hello-world.html.twig
import template from 'hello-world.html.twig';

export default Shopware.Component.wrapComponentConfig('hello-world', {
    template: template
});
```

In the core code, you will find another syntax for the same result though:

```javascript
// <plugin-root>/src/Resources/app/administration/src/component/custom-component/hello-world.html.twig
import template from 'hello-world.html.twig';

export default Shopware.Component.wrapComponentConfig('hello-world', {
    template
});
```

This is a [shorthand](https://eslint.org/docs/latest/rules/object-shorthand), which can only be used if the variable is named exactly like the property.

## Next steps

You've now added a custom component, including a little template. However, there's more to discover here.

* [More about templates](writing-templates)
* [Add some styling to your component](add-custom-styles)
* [Use shortcuts for your component](add-shortcuts)

Furthermore, what about [customizing other components](customizing-components), instead of creating new ones?

---

---

## Add custom input field to existing component
**Source:** [guides/plugins/plugins/administration/add-custom-field.md](https://developer.shopware.com/docs/v6.5/guides/plugins/plugins/administration/add-custom-field.md)  
# Add custom input field to existing component

## Overview

If you were wondering how to add a new input field to an existing module in the Administration via plugin, then you've found the right guide to cover that subject. In the following examples, you'll add a new input field to the product's detail page, to display and configure some other product data not being handled by default.

## Prerequisites

This guide **does not** explain how you can create a new plugin for Shopware 6. Head over to our plugin base guide to learn how to create a plugin at first:

## Injecting into the Administration

The main entry point to customize the Administration via plugin is the `main.js` file. It has to be placed into a `<plugin root>/src/Resources/app/administration/src` directory in order to be automatically found by Shopware 6.

Your `main.js` file then needs to override the [Vue component](https://vuejs.org/v2/guide/components.html) using the `override` method of our `ComponentFactory`.

The first parameter matches the component to override, the second parameter has to be an object containing the actually overridden properties , e.g. the new twig template extension for this component.

```javascript
// <plugin root>/src/Resources/app/administration/src/main.js
import template from './extension/sw-product-settings-form/sw-product-settings-form.html.twig';

Shopware.Component.override('sw-product-settings-form', {
    template
});
```

In this case, the `sw-product-settings-form` component is overridden, which reflects the settings form on the product detail page. As mentioned above, the second parameter has to be an object, which includes the actual template extension.

## Adding the custom template

Time to create the referenced twig template for your plugin now.

::: info
We're dealing with a [TwigJS](https://github.com/twigjs/twig.js/wiki) template here.
:::

Create a file called `sw-product-settings-form.html.twig` in the following directory: `<plugin root>/src/Resources/app/administration/src/extension/sw-product-settings-form`

::: info
The path starting from 'src' is fully customizable, yet we recommend choosing a pattern like this one.
:::

```twig
// <plugin root>/src/Resources/app/administration/src/extension/sw-product-settings-form/sw-product-settings-form.html.twig
{% block sw_product_settings_form_content %}
    {% parent %}

    <sw-container columns="repeat(auto-fit, minmax(250px, 1fr))" gap="0px 30px">
        <sw-text-field label="Manufacturer ID" v-model="product.manufacturerId" disabled></sw-text-field>
    </sw-container>
{% endblock %}
```

Basically the twig block `sw_product_settings_form_content` is overridden here. Make sure to have a look at the [Twig documentation about the template inheritance](https://twig.symfony.com/doc/3.x/templates.html#template-inheritance), to understand how blocks in Twig work.

This block contains the whole settings form of the product detail page. In order to add a new input field to it, you need to override the block, call the block's original content (otherwise we'd replace the whole form), and then add your custom input field to it. Also, the input field is "disabled", since it should be readable only. This should result in a new input field with the label 'Manufacturer ID', which then contains the ID of the actually chosen manufacturer.

## Loading the JS files

As mentioned above, Shopware 6 is looking for a `main.js` file in your plugin. Its contents get minified into a new file named after your plugin and will be moved to the `public` directory of Shopware 6 root directory. Given this plugin would be named "AdministrationNewField", the minified javascript code for this example would be located under `<plugin root>/src/Resources/public/administration/js/administration-new-field.js`, once you run the command following command in your shopware root directory:

```bash
./bin/build-administration.sh
```

```bash
composer run build:js:admin
```

::: info
Your plugin has to be activated for this to work.
:::

Make sure to also include that file when publishing your plugin! A copy of this file will then be put into the directory `<shopware root>/public/bundles/administration/newfield/administration/js/administration-new-field.js`.

Your minified javascript file will now be loaded in production environments.

---

---

## Add custom module
**Source:** [guides/plugins/plugins/administration/add-custom-module.md](https://developer.shopware.com/docs/v6.5/guides/plugins/plugins/administration/add-custom-module.md)  
*(Body truncated in this bundle; follow the link for the rest.)*

# Add custom module

In the `Administration` core code, each module is defined in a directory called `module`.
Inside the `module` directory lies the list of several modules, each having their own directory named after the module itself.

## Prerequisites

This guide **does not** explain how to create a new plugin for Shopware 6.
Head over to our Plugin base guide to learn how to create a plugin at first:

## Creating the index.js file

The first step is creating a new directory `<plugin root>/src/Resources/app/administration/src/module/swag-example`, so you can store your own modules files in there.
Right afterwards, create a new file called `index.js` in there. Consider it to be the main file for your custom module.

::: warning
This is necessary, because Shopware 6 is automatically requiring an `index.js` file for each module.
:::

Your custom module directory isn't known to Shopware 6 yet.
The entry point of your plugin is the `main.js` file.
That's the file you need to change now, so that it loads your new module.
For this, simply add the following line to your `main.js` file:

```javascript
// <plugin root>/src/Resources/app/administration/src/main.js
import './module/swag-example';
```

Now your module's `index.js` will be executed.

## Registering the module

Your `index.js` is still empty now, so let's get going to actually create a new module.
This is technically done by calling the method `registerModule` method of our [ModuleFactory](https://github.com/shopware/shopware/blob/trunk/src/Administration/Resources/app/administration/src/core/factory/module.factory.ts), but you're not going to use this directly.

Instead, you're using the `Shopware.Module.register()` method, but why is that?

`Shopware` is a [global object](the-shopware-object) created for third party developers.
It is mainly the bridge between the Shopware Administration and our plugin.
The `Module` object comes with a `register` helper method to easily register your module.
The method needs two parameters to be set, the first one being the module's name, the second being a javascript object, which contains your module's configuration.

```javascript
// <plugin root>/src/Resources/app/administration/src/module/swag-example/index.js
Shopware.Module.register('swag-example', {
    // configuration here
});
```

## Configuring the module

In this file, you can configure a couple of things, e.g. the color of your module.
Each module needs a primary color, which will be used on specific accents and locations throughout your module.
To name a few, it's the color of the main icon of the module, the tag in the global search input and the accent color of the smart bar.

In this example `#ff3d58` is used as a color, which is a soft red.
Also, each module has their own icon. You can see here [here](https://component-library.shopware.com/icons/) which icons are available in Shopware 6 by default.
In our case here, let's say we use the icon `default-shopping-paper-bag-product`, which will also be used for the module.

::: danger
This is not the icon being used for a menu entry! The icon for that needs to be configured separately.
Please refer to the [Add a menu entry](add-menu-entry) guide for more information on this topic.
:::

In addition, you're able to configure a title here, which will be used for the actual browser title.
Just add a string for the key `title`.
This will be the default title for your module, you can edit this for each component later on.

The `description` is last basic information you should set here, which will be shown as an empty-state.
That means the description will be shown e.g. when you integrated a list component, but your list is empty as of now.
In that case, your module's description will be displayed instead.

Another important aspect are the routes which your module is going to use, such as e.g. `swag-example-list` for the list of your module, `swag-example-detail` for the detail page and `swag-example-create` for creating a new entry.
Those routes are configured as an object in a property named `routes`. We will cover that in the next paragraph.

## Setting up menu entry and routes

The next steps are covered in their own guides. The first one would be adding a menu entry, so please take a look at the guide regarding:

The second one refers to setting up custom routes, its guide can be found in the guide on adding custom routes:

## Set up additional meta info

If you have been following that guide, then you should have got a menu entry then.
The related routes are also set up already and linked to components, which will be created in the next main step.
There's a few more things we need to change in the configurations though that you should add to your module, such as a unique `name` and a `type`.
For reference, see this example:

```javascript
// <plugin root>/src/Resources/app/administration/src/module/swag-example/index.js
Shopware.Module.register('swag-example', {
    type: 'plugin',
    name: 'Example',
    title: 'swag-example.general.mainMenuItemGeneral',
    description: 'sw-property.general.descriptionTextModule',
    color: '#ff3d58',
    icon: 'default-shopping-paper-bag-product',
...
```

The `name` should be a technical unique one, the `type` would be 'plugin' here. When it comes to this `type`, there are basically two options in Shopware: `core` and `plugin`.
So every third-party module should use `plugin`.
To give a little context: Looking at `module.factory` inside `registerModule` the plugin type is the only case which is being checked and has some different behaviour.
So it is more a convention and not a real validation which throws an error when `type` is divergent to these options.

## Implementing snippets

You've already set a label for your module's menu entry.
Yet, by default the `Administration` expects the value in there to be a [Vuei18n](https://kazupon.github.io/vue-i18n/started.html#html) variable, a translation key that is.
It's looking for a translation key `example` now and since you did not provide any translations at all yet, it can't find any translation for it and will just print the key of a snippet.
Sounds like it's time to implement translation snippets as well, right?

This is done by providing a new object to your module configuration, `snippets` this time.
This object contains another object for each language you want to support.
In this example `de-DE` and of course `en-GB` will be supported.

Each language then contains a nested object of translations, so let's have a look at an example:

```json
{
    "swag-example": {
        "nested": {
            "value": "example"
        },
        "foo": "bar"
    }
}
```

In this example you would have access to two translations by the following paths: `swag-example.nested.value` to get the value 'example' and `swag-example.foo` to get the value 'bar'.
You can nest those objects as much as you want. Please note that each path is prefixed by the extension name.

Since those translation objects become rather large, you should store them into separate files.
For this purpose, create a new directory `snippet` in your module's directory and in there two new files: `de-DE.json` and `en-GB.json`

Then, when each file contains your translations as an object, you only have to import them into your module again.

```javascript
// <plugin root>/src/Resources/app/administration/src/module/swag-example/index.js
[...]

import deDE from './snippet/de-DE';
import enGB from './snippet/en-GB';

Shopware.Module.register('swag-example', {
    ...
    snippets: {
        'de-DE': deDE,
        'en-GB': enGB
    },
});
```

Let's also create the first translation, which is for your menu's label.
It's key should be something like this: `swag-example.general.mainMenuItemGeneral`

Thus open the `snippet/en-GB.json` file and create the new object in there.
The structure here is the same as in the first example, just formatted as json file.
Afterwards, use this path in your menu entry's `label` property.

To translate the `description` or the `title`, add those to your snippet file as well and edit the values in your module's `description` and `title`.
The title will be the same as the main menu entry by default.

This should be your snippet file now:

```json
{
    "swag-example": {
        "general": {
            "mainMenuItemGeneral": "My custom module",
            "descriptionTextModule": "Manage this custom module here"
        }
    }
}
```

## Build the Administration

As mentioned above, Shopware 6 is looking for a `main.js` file in your plugin.
Its contents get minified into a new file named after your plugin and will be moved to the `public` directory of Shopware 6 root directory.
Given this plugin would be named "AdministrationNewModule", the bundled and minified javascript code for this example would be located under `<plugin root>/src/Resources/public/administration/js/administration-new-module.js`, once you run the command following command in your shopware root directory:

```bash
./bin/build-administration.sh
```

```bash
composer run build:js:admin
```

::: info
Your plugin has to be activated for this to work.
:::

Make sure to also include that file when publishing your plugin!
A copy of this file will then be put into the directory `<shopware root>/public/bundles/administration/administrationnewmodule/administration/js/administration-new-module.js`.

Your minified javascript file will now be loaded in production environments.

## Special: Case Settings

### Link your module into settings

If you think about creating a module concerning settings, you might want to link your module in the `settings` section of the Administration.
You can add the `settingsItem` option to the module configuration as seen below:

```javascript
// <plugin root>/src/Resources/app/administration/src/module/swag-example/index.js
import './page/swag-plugin-list';
import './page/swag-plugin-detail';
Shopware.Module.register('swag-plugin', {
    ...
    settingsItem: [{
        group: 'plugin',
        to: 'swag.plugin.list',
        icon: 'default-object-rocket',
        name: 'swag-example.general.mainMenuItemGeneral'
    }]
});
```

The `group` property targets to the group section, the item will be displayed in 'shop', 'system' and 'plugins' sections.
The `to` gets the link path of the route. The `icon` contains the icon name which will be display.

### Add custom settings card

You can even provide custom setting cards that are either placed in shop, system or plugin tab.
This can be achieved by adding the key settingsItem to your module object:

```javascript
settingsItem: [{ // this can be a single object if no collection is needed
    to: 'custom.module.overview', // route to anything
    group: 'system', // either system, shop or plugins
    icon: 'default-object-lab-flask',
    iconComponent: YourCustomIconRenderingComponent, // optional, this overrides icon attribute
    id: '', // optional, fallback is taken from module
    name: '', // optional, fallback is taken from module
    label: '', // optional, fallback is taken from module
}]
```

## Example for the final module

Here's your final module:

```javascript
// <plugin root>/src/Resources/app/administration/src/module/swag-example/index.js
import './page/swag-example-list';
import './page/swag-example-detail';
import './page/swag-example-create';
import deDE from './snippet/de-DE';
import enGB from './snippet/en-GB';

Shopware.Module.register('swag-example', {
    type: 'plugin',
    name: 'Example',
    title: 'swag-example.general.mainMenuItemGeneral',
    description: 'sw-property.general.descriptionTextModule',
    color: '#ff3d58',
    icon: 'default-shopping-paper-bag-product',

    snippets: {
        'de-DE': deDE,
        'en-GB': enGB
    },

    routes: {
        list: {
            component: 'swag-example-list',
            path: 'list'
        },
        detail: {
            component: 'swag-example-detail',
            path: 'detail/:id'

… **Truncated.** Full document: https://developer.shopware.com/docs/v6.5/guides/plugins/plugins/administration/add-custom-module.md


---

## Add custom route
**Source:** [guides/plugins/plugins/administration/add-custom-route.md](https://developer.shopware.com/docs/v6.5/guides/plugins/plugins/administration/add-custom-route.md)  
# Add custom route

Routes in the Shopware 6 Administration are essentially the same as in any other [Vue Router](https://router.vuejs.org). This guide will teach you the basics of creating your very first route from scratch.

## Prerequisites

All you need for this guide is a running Shopware 6 instance and full access to both the files and preferably a registered module. Of course you'll have to understand JavaScript, but that's a prerequisite for Shopware as a whole and will not be taught as part of this documentation.

## Configuring the route

So lets start with configuring our own route. In order to add routes to a module you simply add the `routes` property, which expects an object containing multiple route configuration objects. Each route configuration object needs to have a `name`, which is set using the configuration object's key. Furthermore, we need to set a component and a path: A route points to a [component](https://vuejs.org/v2/guide/components.html) using the key `component`, which targets the component to be shown when this route is requested. The key `path` represents the actual path, that's going to be used for this route. Do not get confused just because it is equal to the route name in the first route.

Now, our route should look like this:

```javascript
// routes: {
//     nameOfTheRoute: {
//         component: 'example',
//         path: 'actualPathInTheBrowser'
//     }
// }
routes: {
    overview: {
        component: 'sw-product-list',
        path: 'overview'
    },
},
```

Routes can be matched by name and path. This configuration results in this route's full name being `custom.module.overview` and the URL being `/overview` relative to the Administration's default URL. Usually you want to render your custom component here, which is explained [here](add-custom-component). But that is not all! Routes can have parameters, to then be handed to the components being rendered and much more. Learn more about what the Vue Router can do in its official [Documentation](https://router.vuejs.org/guide/essentials/dynamic-matching.html#reacting-to-params-changes).

## Meta data and dynamic parameters

Let's extend this example:

```javascript
Shopware.Module.register('swag-example', {
    color: '#ff3d58',
    icon: 'default-shopping-paper-bag-product',
    title: 'My custom module',
    description: 'Manage your custom module here.',

    routes: {
        overview: {
            component: 'swag-example-list',
            path: 'overview'
        },
        // This is our second route
        detail: {
            component: 'sw-example-detail',
            path: 'detail/:id',
            meta: {
                parentPath: 'swag.example.list'
            }
        }
    },
});
```

This second route, `detail`, comes with a dynamic parameter as part of the route. When you want to open a detail page of an example, the route also has to contain the ID of the example, in the `path` of `detail`:

```javascript
path: 'detail/:id'
```

Furthermore, the `detail` route comes with another new configuration, which is called `meta`. As the name suggests, you can use this object to apply more meta information for your route. In this case the `parentPath` is filled. Its purpose is to link the path of the actual parent route. In the Administration, this results in a "back" button on the top left of your module when being on the detail page. This button will then link back to the list route and the icon defined earlier will also be used for this button.

You might want to have a closer look at the `parentPath` value though. Its route follows this pattern: `<bundle-name>.<name of the route>`

See in this example:

```javascript
...
   meta: {
       parentPath: 'swag.example.list'
   }
...
```

The `bundle-name` is separated by dots instead of dashes here though. The second part is the **name** of the route, the key of the route configuration that is. Thus the path to the `list` route is `swag.example.list`. The same applies for the `create` route.

## More interesting topics

* [Adding a custom service](add-custom-service)
* [Customizing a module](customizing-modules)
* [Adding permissions](add-acl-rules)

---

---

## Adding Services
**Source:** [guides/plugins/plugins/administration/add-custom-service.md](https://developer.shopware.com/docs/v6.5/guides/plugins/plugins/administration/add-custom-service.md)  
# Adding Services

## Overview

This guide will teach you how to add a service to the Shopware 6 Administration, using [BottleJS](https://github.com/young-steveo/bottlejs).

This documentation chapter will cover the following topics:

* What is an Administration service?
* How to register a new Administration service for your plugin

## Prerequisites

All you need for this guide is a running Shopware 6 instance and full access to both the files and a running plugin. Of course you'll have to understand JavaScript, but that's a prerequisite for Shopware as a whole and will not be taught as part of this documentation.

## Register a new service

For this example, we want to use the following service. It's supposed to get random jokes. It is placed in `<administration root>/services/joke.service.js` and looks like the example seen below:

```javascript
export default class JokeService {
    constructor(httpClient) {
        this.httpClient = httpClient;
    }

    joke() {
        return this.httpClient
            .get('https://v2.jokeapi.dev/joke/Programming?blacklistFlags=nsfw,religious,political')
            .then(response => response.data)
    }
}
```

For now this service class is not available in the injection container. To fix this, a new script is placed at `<administration root>/init/joke-service.init.js` and imported in the `main.js` file of our plugin:

```javascript
import JokeService from '../services/joke.service'

Shopware.Service().register('joker', (container) => {
    const initContainer = Shopware.Application.getContainer('init');
    return new JokeService(initContainer.httpClient);
});
```

## Service injection

A service is typically injected into a vue component and can simply be referenced in the `inject` property:

```javascript
Shopware.Component.register('swag-basic-example', {
    inject: ['joker'],

    created() {
        this.joker.joke().then(joke => console.log(joke))
    }
});
```

To avoid collision with other properties like computed fields or data fields there is an option to rename the service property using an object:

```javascript
Shopware.Component.register('swag-basic-example', {
    inject: {
        jokeService: 'joker'
    },

    created() {
        this.jokeService.joke().then(joke => console.log(joke))
    }
});
```

## Adding a middleware

BottleJS also allows us to add middleware to our services.

This code sample is based on the example in the [BottleJS documentation](https://github.com/young-steveo/bottlejs#middlewarename-func). For this we need to change our previously used service, as seen below:

```javascript
class JokeService {
    constructor(httpClient) {
        this.httpClient = httpClient;
        this.isActive = false;
    }

    joke() {
        return this.httpClient
            .get(`https://v2.jokeapi.dev/joke/Programming?blacklistFlags=nsfw,religious,political`)
            .then(response => response.data)
    }
}
```

Now that we've added an `isActive` flag, we can react to it in our middleware and throw an exception if the service is not active.

```javascript
Shopware.Application.addServiceProviderMiddleware('joker', (service, next) => {
    if(!service.isActive) {
        return next(new Error('Service is inActive'));
    }

    next();
});

Shopware.Service().register('joker', (container) => {
    const initContainer = Shopware.Application.getContainer('init');
    return new JokeService(initContainer.httpClient);
});
```

## Decorating a service

Service decoration can be us in a variety of ways. Services can be initialized right after their creation and single methods can get an altered behavior. Like in the service registration, a script that is part of the `main.js` is needed.

::: warning
Decorators are just simple functions, which intercept a service in the provider phase. This means that a service can only be decorated in the timeframe between it being created and it being accessed for the first time.
:::

If you need to alter a service method return value or add an additional parameter you can also do this using decoration. For this example a `funny` attribute is added to the requested jokes by the previously registered `JokeService`:

```javascript
Shopware.Application.addServiceProviderDecorator('joker', joker => {
    const decoratedMethod = joker.joke;

    joker.joke = function () {
        return decoratedMethod.call(joker).then(joke => ({
            ...joke,
            funny: joke.id % 2 === 0
        }))
    };

    return joker;
});
```

## Next steps

Now that we have created a service, you might want to create or customize a Administration component:

* [Creating a new administration component](add-custom-component)
* [Extending an existing administration component](customizing-components)

---

---

## Add custom styles
**Source:** [guides/plugins/plugins/administration/add-custom-styles.md](https://developer.shopware.com/docs/v6.5/guides/plugins/plugins/administration/add-custom-styles.md)  
# Add custom styles

## Overview

All components contain own templates and some style. Of course, you may want to use your custom styles in your component or module. In this guide, we got you covered on how to add those custom styles to your components.

## Prerequisites

However, this guide does not explain how to create a custom component, so head over to the official guide about creating a custom component to learn this first.

In addition, you need to have a basic knowledge of CSS and SCSS in order to use custom styles. This is though considered a basic requirement and won't be taught in this guide.

### Example: Custom cms block

We will base our guide on an example: Let's use a custom component printing out "Hello world!". So first of all, create a new directory for your`sw-hello-world`. As said before, more information about that topic, such as where to create this directory, can be found in [Add a custom component](add-custom-component).

In your component's directory, create a new `index.js` file and register your custom component `sw-hello-world`:

```javascript
Shopware.Component.register('sw-hello-world', {
    template
});
```

Just like most components, it has a custom template. First we create the template file named `sw-hello-world.html.twig`:

This template now has to define the basic structure of your component. In this simple case, you only need a parent container and two sub-elements, whatever those are.

```html
{% block example_block %}
    <div class="sw-hello-world">
        <p>Hello world!</p>
    </div>
{% endblock %}
```

You've got a parent `div` containing the content of your template, an abstract with the text "Hello world!" in this case. Next up, you need to import that template in your `index.js` file of your component:

```javascript
// Import for your template
import template from './sw-hello-world.html.twig';

Shopware.Component.register('sw-sw-hello-world', {
    template
});
```

## Add custom styles to your component

Your component should come with a custom `.scss` file, which you need to create now. Don't forget to import it in your `index.js` file, if not done yet:

```javascript
import template from './sw-hello-world.html.twig';

// Import for your custom styles
import './sw-hello-world.scss';

Shopware.Component.register('sw-sw-hello-world', {
    template
});
```

In there, simply use a grid to display your elements next to each other. You set a CSS class for your block, which is named after the component. In there, you can set your styles as you need. To mention an example, we want the text in the `div` with the class `sw-hello-world` to have a blue color:

```css
.sw-hello-world {
    color: blue;
}
```

That's it for this component! This way, you're able to add your own styles to your component now.

### Import variables

Because of [Sass](https://sass-lang.com/) usage, you are able to import external variables and use them in your classes. Below you see an example which uses Shopware's SCSS variables to color the text of the component in shopware's shade of blue.

```css
/* Import statement */
@import "~scss/variables";

.sw-hello-world {
  /* Usage of variable */
  color: $color-shopware-brand-500;
}
```

## More interesting topics

* [Writing templates](writing-templates)
* [Add shortcuts](https://github.com/shopware/docs/tree/575c2fa12ef272dc25744975e2f1e4d44721f0f1/guides/plugins/plugins/administration/add-shortcuts.md)

---

---

## Adding error handling
**Source:** [guides/plugins/plugins/administration/add-error-handling.md](https://developer.shopware.com/docs/v6.5/guides/plugins/plugins/administration/add-error-handling.md)  
# Adding error handling



## Overview

The Shopware 6 Administration stores API errors in the [Vuex store](https://vuex.vuejs.org/). There they are centrally accessible to your components, with a flat data structure looking like this:

```text
(state)
 |- entityNameA
    |- id1
        |- property1
        |- property2
        ...
    |- id2
        |- property1
        |- property2
        ...
 |- entityNameB
   ...
```

In this guide you will learn how to access this error store directly or via one of the provided helper functions. 

## Read errors from the store

 Errors can be read from the store by calling the getter method `getApiErrorFromPath`. 

```javascript
function getApiErrorFromPath (state) => (entityName, id, path)
```

 In there, the parameter `path` is an `array` representing the nested property names of your entity.

Also we provide a wrapper which can also handle nested fields in object notation, being much easier to use for scalar fields: 

```javascript
function getApiError(state) => (entity, field)
```

 For example, an empty product name would result in an error with the path `product.name`, instead of having the array `['product', 'name']` present.

In your Vue component, use computed properties to avoid flooding your templates with store calls. 

```javascript
computed: {
    propertyError() {
        return this.$store.getters.getApiError(myEntity, 'myFieldName');
    },
    nestedpropertyError() {
        return this.$store.getters.getApiError(myEntity, 'myFieldName.nested');
    }
}
```

Those computed properties can then be used in your templates the familiar way:

```html
<div>
    <sw-field ... :error="propertyError"></sw-field>
</div>
```



### The mapErrors Service

 Like every Vuex mapping, fetching the errors from the store may be very repetitive and error-prone. Because of this we provide you an Vuex like mapper function: 

```javascript
mapPropertyErrors(subject, properties)
```

 Here, the `subject` parameter is the entity name (not the entity itself) and `properties` is an array of the properties you want to map. You can spread its result to create computed properties in your component. The functions returned by the mapper are named like a camelCase representation of your input, suffixed with `Error`.

This is an example from the `sw-product-basic-form` component: 

```javascript
const { mapPropertyErrors } = Shopware.Component.getComponentHelper();

Component.register('sw-product-basic-form', {
    computed: {
        ...mapPropertyErrors('product', [
            'name',
            'description',
            'productNumber',
            'manufacturerId',
            'active',
            'markAsTopseller'
        ])
    }
})
```

Which then are bound to the inputs like this:

```html
<sw-field type="text" v-model="product.name" :error="productNameError">
```



### Error configuration for pages

 When working with nested views, you need a way to tell the user that an error occurred on another view, e.g in another `tab`. For this you can write a config for your `sw-page` component which looks like seen below: 

```json
{
  "sw.product.detail.base": {
    "product": [
      "taxId",
      "price",
      "stock",
      "manufacturerId",
      "name"
    ]
  },
  "sw.product.detail.cross.selling": {
    "product_cross_selling": [
      "name",
      "type",
      "position"
    ]
  }
}
```

 This can then directly imported and used in the `mapPageError` computed property:

```javascript
import errorConfiguration from './error.cfg.json';

const { mapPageErrors } = Shopware.Component.getComponentHelper();

Shopware.Component.register('sw-product-detail', {
    computed: {
        ...mapPageErrors(errorConfiguration),
    }
}
```

This makes it possible to indicate if one or more errors exists, in another view or a tab:

```html
<sw-tabs
    :hasError="swProductDetailBaseError">
</sw-tabs>
```

---

---

## Add filter
**Source:** [guides/plugins/plugins/administration/add-filter.md](https://developer.shopware.com/docs/v6.5/guides/plugins/plugins/administration/add-filter.md)  
# Add filter

## Overview

In this guide you'll learn, how to create a filter for the Shopware Administration. A filter is just a little helper for formatting text. In this example, we create a filter that converts text into uppercase and adds an underscore at the beginning and end.

## Prerequisites

This guide requires you to already have a basic plugin running. If you don't know how to do this in the first place, have a look at our [Plugin base guide](../plugin-base-guide).

## Creating the filter

First we create a new file in the directory `<plugin root>/src/Resources/app/administration/src/app/filter`. In this case we name our filter `example`, so our file will be named `example.filter.js`.

Here's an example how your filter could look like:

```javascript
// <plugin root>/src/Resources/app/administration/src/app/filter/example.filter.js
const { Filter } = Shopware;

Filter.register('example', (value) => {
    if (!value) {
        return '';
    }

    return `_${value.toLocaleUpperCase()}_`;
});
```

As you can see, it's very simple. We use `Filter` from the `Shopware` object where we can register our filter with the method `register`. The first argument we pass is the name of our filter, which is `example`. The second argument is a function with which we format our text.

If you want to use multiple arguments in your filter function, it could look like this:

```javascript
Filter.register('example', (value, secondValue, thirdValue) => {
    ...
});
```

Last, import the filter into your plugin's `main.js` file.

## Next steps

Now that you know how to create a filter for the Administration, we want to use it in our code. For this head over to our [using filter](using-filter) guide.

---

---

## Add menu entry
**Source:** [guides/plugins/plugins/administration/add-menu-entry.md](https://developer.shopware.com/docs/v6.5/guides/plugins/plugins/administration/add-menu-entry.md)  
# Add menu entry

## Overview

When it comes to the module configuration, the menu entry is one of the most important things to set up. It serves to open your module.

## Prerequisites

This guide **does not** explain how to create a new plugin for Shopware 6. Head over to our Plugin base guide to learn how to create a plugin at first:

Especially if you want to add a new page for an own module, you should consider to look at the process on how to add a custom module first.

## Creating a simple menu entry

This menu entry can be defined in your module configuration. Remember, your module configuration looks as seen below:

```javascript
// <plugin root>/src/Resources/app/administration/src/module/swag-example/index.js
Shopware.Module.register('swag-plugin', {
    // configuration here
});
```

In order to create your own menu entry, you need to use the `navigation` key: It takes an array of objects, each one configuring a route connected to your module.

So let's define a menu entry using the `navigation` key in your module configuration. It takes an array of objects, each one configuring a route connected to your module:

```javascript
// <plugin root>/src/Resources/app/administration/src/module/swag-example/index.js
navigation: [{
    label: 'CustomModule',
    color: '#ff3d58',
    path: 'swag.custommodule.list',
    icon: 'default-shopping-paper-bag-product',
    position: 100
}]
```

As you see, you are able to configure several things in there:

| Configuration | Description |
| :--- | :--- |
| label | The label to be shown with this menu entry. |
| color | This  is the theme color of the module. This color may differ from the module's color itself. |
| path | Which one of your configured routes shall be used when clicking this menu entry? The path is composed of the module id and the path name. Dashes become dots, for example module 'swag-example' and path 'index' become 'swag.example.index'. |
| icon | Also you can set a separate icon, which can make sense e.g. when having multiple menu entries for a single module, such as a special icon for 'Create bundle'. This example does not have this and it's only going to have a single menu entry, so use the icon from the main module here. |
| position | The position of the menu entry. The higher the value, the more likely it is that your menu entry appears in the bottom. |

Of course there's more to be configured here, but more's not necessary for this example.

## Menu entry in category

Due to UX reasons, we're not supporting plugin modules to add new menu entries on the first level of the main menu. Please use the "parent" property inside your navigation object to define the category where you want your menu entry will be appended to. Your navigation entry will also have to have an `id` to show up in the rendered navigation:

```javascript
// <plugin root>/src/Resources/app/administration/src/module/swag-example/index.js
navigation: [{
    id: 'swag-custommodule-list',
    label: 'CustomModule',
    color: '#ff3d58',
    path: 'swag.custommodule.list',
    icon: 'default-shopping-paper-bag-product',
    parent: 'sw-catalogue',
    position: 100
}]
```

You can find the parent id at the `index.js` file in each module folder. You can see the property `navigation` in the `Module.register` method. The id here can be used as the parent key.

## Nesting menu entries

The parent can be on any level because the menu supports infinite depth nesting. For example, if `sw-manufacturer` were taken as the `parent`, the menu item would be present on the third level. So what's important here is that the configured parent defines where the menu entry will take place.

::: info
If you're planning to publish your plugin to the Shopware Store keep in mind we're rejecting plugins which have created their own menu entry on the first level.
:::

---

---

## Adding Mixins
**Source:** [guides/plugins/plugins/administration/add-mixins.md](https://developer.shopware.com/docs/v6.5/guides/plugins/plugins/administration/add-mixins.md)  
# Adding Mixins

## Overview

This documentation chapter will cover how to add a new Administration mixin for your plugin. In general, mixins behave the same as they do in Vue normally, differing only in the registration and the way mixins are included in a component. If you want an overview over the shopware provided mixins look at them here: [Using Mixins](using-mixins).

## Prerequisites

All you need for this guide is a running Shopware 6 instance and full access to both the files and a running plugin. Of course you'll have to understand JavaScript, but that's a prerequisite for Shopware as a whole and will not be taught as part of this documentation. As stated before mixins in Shopware are basically the same as in Vue, so you should have read their [documentation](https://vuejs.org/v2/guide/mixins.html) on them first.

## Register a new Mixin

For this example, we'll just use the example mixin from the [VueJS documentation](https://vuejs.org/v2/guide/mixins.html) and adjust it to be used in Shopware.

Mixins in Shopware have to be registered in the mixin registry via the `Mixin.register` function to be available everywhere in the Administration.

Converting the Vue mixin to be used in Shopware looks like the example seen below:

```javascript
// <administration root>/mixins/swag-basic-example.js
// get the Mixin property of the shopware object
const { Mixin } = Shopware;

// give the mixin a name and feed it into the register function as the second argument
Mixin.register('swag-basic-mixin', {
    created: function () {
        this.hello()
    },
    methods: {
        hello: function () {
            console.log('hello from mixin!')
        }
    }
});
```

## Importing the Mixin in the Plugin

Now that we have registered the mixin, we need to import it *before importing our components* in the `main.js` file.

```javascript
// <administration root>/src/main.js
import '<administration root>/mixins/swag-basic-example.js'
    
// importing components...
```

## Using the Mixin

After registering our mixin under a name, we can get it from the registry with the `Mixin.getByName` function and inject it into our component as seen below.

```javascript
// <administration root>/components/swag-basic-example/index.js
const { Component, Mixin } = Shopware;

Component.register('swag-basic-example', {

    mixins: [
        Mixin.getByName('swag-basic-mixin')
    ],
});
```

This can also be done with Shopware provided mixins, learn more about them here: [Using Mixins](using-mixins)

## More interesting topics

* [Adding filters](add-filter)
* [Using utils](using-utils)

---

---

## Add tab to existing module
**Source:** [guides/plugins/plugins/administration/add-new-tab.md](https://developer.shopware.com/docs/v6.5/guides/plugins/plugins/administration/add-new-tab.md)  
# Add tab to existing module

## Overview

You want to create a new tab in the Administration? This guide gets you covered on this subject. A realistic example would be adding a new association for an entity, which you want to configure on a separate tab on the entity detail page.

## Prerequisites

This guide requires you to already have a basic plugin running. If you don't know how to do this in the first place, have a look at our plugin base guide:

In the course of this guide, you need to create a custom route. If you want to learn on how to create a custom component, please refer to the guide on it:

Also, we will use a small, custom component to fill our custom tab. In order to get used to that, it might come in handy to read the corresponding guide first:

::: info

### Please remember

The main entry point to customize the Administration via plugin is the `main.js` file. It has to be placed into a `<plugin root>/src/Resources/app/administration/src` directory in order to be found by Shopware 6. So please use the file accordingly and refer to the [plugin base guide](../plugin-base-guide) for more details.
:::

## Creating a custom tab

### Find the block to extend

For this guide, we'll think about the following example: The product detail page is extended by a new tab, which then only contains a 'Hello world!'. In order to refer to this example, let's have a look at the twig code of the product detail page found here:

Let's imagine your first goal is to create a new tab on the product detail page. Having a look at the template, you might find the block `sw_product_detail_content_tabs`, which seems to contain all available tabs. It starts by creating a new `<sw-tabs>` element to contain all the tabs available. Here you can see excerpt of this block:

```twig
// platform/src/Administration/Resources/app/administration/src/module/sw-product/page/sw-product-detail/sw-product-detail.html.twig
{% block sw_product_detail_content_tabs %}
    <sw-tabs class="sw-product-detail-page__tabs" v-if="productId">
        {% block sw_product_detail_content_tabs_general %}
            <sw-tabs-item
                class="sw-product-detail__tab-general"
                :route="{ name: 'sw.product.detail.base', params: { id: $route.params.id } }"
                :hasError="swProductDetailBaseError"
                :title="$tc('sw-product.detail.tabGeneral')">
                {{ $tc('sw-product.detail.tabGeneral') }}
            </sw-tabs-item>
        {% endblock %}

        ...

        {% block sw_product_detail_content_tabs_reviews %}
            <sw-tabs-item
                class="sw-product-detail__tab-reviews"
                :route="{ name: 'sw.product.detail.reviews', params: { id: $route.params.id } }"
                :title="$tc('sw-product.detail.tabReviews')">
                {{ $tc('sw-product.detail.tabReviews') }}
            </sw-tabs-item>
        {% endblock %}
    </sw-tabs>
{% endblock %}
```

Unfortunately, you cannot use the block mentioned above, because then your new tab wouldn't be inside the `<sw-tabs>` element. Instead, you can choose the last available block inside the element, which is `sw_product_detail_content_tabs_reviews` at this moment.

### Create custom tab

Knowing the block you have to override in your plugin, you can now start doing exactly this: Add your custom tab by overriding this block called `sw_product_detail_content_tabs_reviews`.

::: danger
However, please keep in mind that "overriding" doesn't mean we want to replace the block completely with our new one. We want to add our tab, thus only extending the template. This will have some implications on our implementation.
:::

First, please re-create the directory structure from the core code in your plugin. In this case, you'll have to create a directory structure like the following: `<plugin root>/src/Resources/app/administration/src/page/sw-product-detail`

In there you create a new file `index.js`, which then contains the following code:

```javascript
// <plugin root>/src/Resources/app/administration/src/page/sw-product-detail/index.js
import template from './sw-product-detail.html.twig';

// Override your template here, using the actual template from the core
Shopware.Component.override('sw-product-detail', {
    template
});
```

All this file is doing is to basically override the `sw-product-detail` component with a new template. The new template does not exist yet though, so create a new file `sw-product-detail.html.twig` in the same directory as your `index.js` file. It then has to use the block we figured out earlier and override it by adding a new tab element:

```twig
// <plugin root>/src/Resources/app/administration/src/page/sw-product-detail/sw-product-detail.html.twig
{% block sw_product_detail_content_tabs_reviews %}

    {# This parent is very important as you don't want to override the review tab completely #}
    {% parent %}

{% endblock %}
```

::: warning
The block gets overridden and immediately the parent block is called, since you do not want to replace the 'Review' tab, you want to add a new tab instead.
:::

After that, we'll create the actual `sw-tabs-item` element, which, as the name suggests, represents a new tab item. We want this tab to have a custom route, so we're also adding this route directly. Don't worry, we'll explain this custom route in a bit. The product detail page's route contain the product's ID, which you also want to have in your custom tab: So make sure to also pass the ID in, like shown in the example above.

```twig
// <plugin root>/src/Resources/app/administration/src/page/sw-product-detail/sw-product-detail.html.twig
{% block sw_product_detail_content_tabs_reviews %}

    {% parent %}

    <!-- We'll define a custom route here, an explanation will follow later -->
    <sw-tabs-item :route="{ name: 'sw.product.detail.custom', params: { id: $route.params.id } }" title="Custom">
        Custom
    </sw-tabs-item>
{% endblock %}
```

The [route](add-custom-route) being used here has the name `sw.product.detail.custom`, this will become important again later on.

### Loading the new tab

You've now created a new tab, but your new template is not yet loaded. Remember, that the main entry point for custom javascript for the Administration is the your plugin's `main.js` file. And that's also the file you need to adjust now, so it loads your `sw-product-detail` override.

This is an example of what your `main.js` should look like in order to load your override:

```javascript
import './page/sw-product-detail';
```

::: info
Don't forget to rebuild the Administration after applying changes to your `main.js`.

```bash
./bin/build-administration.sh
```

```bash
composer run build:js:admin
```

## Registering the tab's new route

Your new tab should now already show up on the product detail page, but clicking it should always result in an error. It's basically pointing to a new route, which you never defined yet.

Next step would be the following: Create a new route and map it to your own component. This is done by registering a new dummy module, which then overrides the method `routeMiddleware` of a module. It gets called for each and every route that is called in the Administration. Once the `sw.product.detail` route is called, you want to add your new child route to it.

You can add those changes to your `main.js` file, which could then look like this:

```javascript
// <plugin root>/src/Resources/app/administration/src/main.js
import './page/sw-product-detail';
import './view/sw-product-detail-custom';

// Here you create your new route, refer to the mentioned guide for more information
Shopware.Module.register('sw-new-tab-custom', {
    routeMiddleware(next, currentRoute) {
        const customRouteName = 'sw.product.detail.custom';
    
        if (
            currentRoute.name === 'sw.product.detail' 
            && currentRoute.children.every((currentRoute) => currentRoute.name !== customRouteName)
        ) {
            currentRoute.children.push({
                name: customRouteName,
                path: '/sw/product/detail/:id/custom',
                component: 'sw-product-detail-custom',
                meta: {
                    parentPath: 'sw.product.index'
                }
            });
        }
        next(currentRoute);
    }
});
```

As already mentioned, you need to create a dummy module in order to override the `routeMiddleware` method. In there, you're listening for the current route, that got called. If the current route matches `sw.product.detail`, you want to add your new child route to it, and that's what's done here.

::: warning
Your child route defines the routes name, so make sure to use the name you're already defined earlier!
:::

The path should be identical to the default ones, which look like this: `/sw/product/detail/:id/base` Just replace the `base` here with `custom` or anything you like.

It then points to a component, which represents the routes actual content - so you'll have to create [a new component](add-custom-component) in the next step. Note the new import that's already part of this example: `view/sw-product-detail-custom`

## Creating your new component

As shown in the previous example, your custom component is expected to be in a directory `view/sw-product-detail-custom`, so create this directory in your plugin now. The directory structure inside of your Administration directory should then look like this:

```text
administration
├── src
│   └──page
│       └── sw-product-detail
│           ├── index.js
│           └── sw-product-detail.html.twig
|   └──view
│       └── sw-product-detail-custom
│           ├── index.js        
└── main.js
```

Since a component always gets initiated by a file called `index.js`, create such a new file in the `sw-product-detail-custom` directory:

```javascript
// <plugin root>/src/Resources/app/administration/src/view/sw-product-detail-custom/index.js
import template from './sw-product-detail-custom.html.twig';

Shopware.Component.register('sw-product-detail-custom', {
    template,

    metaInfo() {
        return {
            title: 'Custom'
        };
    },
});
```

This file mainly registers a new component with a custom title and a custom template. Once more, the referenced template is still missing, so make sure to create the file `sw-product-detail-custom.html.twig` next to your `index.js` file.

Here's what this new template could look like:

```html
// <plugin root>/src/Resources/app/administration/src/view/sw-product-detail-custom/sw-product-detail-custom.html.twig
<sw-card title="Custom">
    Hello world!
</sw-card>
```

It simply creates a new card with a title, which only contains a 'Hello world!' string. And that's it - your tab should now be fully functional.

---

---

## Add rule assignment configuration
**Source:** [guides/plugins/plugins/administration/add-rule-assignment-configuration.md](https://developer.shopware.com/docs/v6.5/guides/plugins/plugins/administration/add-rule-assignment-configuration.md)  
# Add rule assignment configuration

::: info
The rule assignment configuration is available from Shopware Version 6.4.8.0
:::

## Overview

You want to create a custom card in the rule assignment, where you can add or delete assignments? This guide gets you covered on this topic. Based on an example of the configuration of the `Dynamic Access` plugin, you will see how to write your configuration.

![](../../../../assets/add-rule-assignment-configuration-0.png)

## Prerequisites

This guide **does not** explain how to create a new plugin for Shopware 6.
Head over to our Plugin base guide to learn how to create a plugin at first:

## Creating the index.js file

The first step is creating a new directory like so `<plugin root>/src/Resources/app/administration/src/module/sw-settings-rule/extension/sw-settings-rule-detail-assignments`.
Right afterwards, create a new file called `index.js` in there.

Your custom module directory isn't known to Shopware 6 yet.
The entry point of your plugin is the `main.js` file.
That's the file you need to change now, so that it loads your extended component.
For this, simply add the following line to your `main.js` file:

```javascript
// <plugin root>/src/Resources/app/administration/src/main.js
import './module/sw-settings-rule/extension/sw-settings-rule-detail-assignments';
```

Now your module's `index.js` will be executed.

## Override the component

Your `index.js` is still empty now, so let's override the `sw-settings-rule-detail-assignments` component.
This is technically done by calling the method `override` method of our [ComponentFactory](https://github.com/shopware/shopware/blob/trunk/src/Administration/Resources/app/administration/src/core/factory/async-component.factory.ts), which is available through our third party wrapper.
This method expects a name, and a configuration for the component you want to override.

```javascript
// <plugin root>/src/Resources/app/administration/src/module/sw-settings-rule/extension/sw-settings-rule-detail-assignments/index.js
Component.override('sw-settings-rule-detail-assignments', {
    // override configuration here
});
```

## Overriding the computed

Now your plugin is overriding the `sw-settings-rule-detail-assignments` component, but currently this has no effect.
In the `associationEntitiesConfig` computed property the configuration of the rule assignment is built and returned to the method which initiates the component.
Because of this, you have to override this computed property, get the computed property of the original component, add your own configuration of the rule assignment and return the whole configuration array.

```javascript
// <plugin root>/src/Resources/app/administration/src/module/sw-settings-rule/extension/sw-settings-rule-detail-assignments/index.js
Component.override('sw-settings-rule-detail-assignments', {
    computed: {
        associationEntitiesConfig() {
            const associationEntitiesConfig = this.$super('associationEntitiesConfig');
            associationEntitiesConfig.push(/* insert your configuration here */);
            return associationEntitiesConfig;
        },
    }
});
```

## Adding the configuration

The configuration of the rule assignment is passed as an object and offers a wide range of options.
Just have a look onto one example configuration item of the `Dynamic Access` plugin:

```javascript
// Example of a configuration item
getRuleAssignmentConfig()
{
    return [
        {
            id: 'swagDynamicAccessProducts',
            notAssignedDataTotal: 0,
            entityName: 'product',
            label: 'swag-dynamic-access.sw-settings-rule.detail.associations.productVisibility',
            criteria: () => {
                const criteria = new Criteria();
                criteria.setLimit(this.associationLimit);
                criteria.addFilter(Criteria.equals('swagDynamicAccessRules.id', this.rule.id));
                criteria.addAssociation('options.group');
                criteria.addAssociation('swagDynamicAccessRules');

                return criteria;
            },
            api: () => {
                const api = Object.assign({}, Context.api);
                api.inheritance = true;

                return api;
            },
            detailRoute: 'sw.product.detail.base',
            gridColumns: [
                {
                    property: 'name',
                    label: 'Name',
                    rawData: true,
                    sortable: true,
                    routerLink: 'sw.product.detail.prices',
                    allowEdit: false,
                },
            ],
            deleteContext: {
                type: 'many-to-many',
                entity: 'product',
                column: 'extensions.swagDynamicAccessRules',
            },
            addContext: {
                type: 'many-to-many',
                entity: 'swag_dynamic_access_product_rule',
                column: 'productId',
                searchColumn: 'name',
                criteria: () => {
                    const criteria = new Criteria();
                    criteria.addFilter(
                            Criteria.not('AND', [Criteria.equals('swagDynamicAccessRules.id', this.rule.id)]),
                    );
                    criteria.addAssociation('options.group');

                    return criteria;
                },
                gridColumns: [
                    {
                        property: 'name',
                        label: 'Name',
                        rawData: true,
                        sortable: true,
                        allowEdit: false,
                    },
                    // ...
                ],
            },
        },
    ];
}
```

Let's go through the most important entries, how to configure your rule assignment:

| Option | Description |
| :--- | :--- |
| id | Required identifier for the assignment, which is arbitrary but unique |
| entityName, criteria, api | Required for data loading of the assignment |
| gridColumns | To define the columns, which are shown in your assignment card. Have a look into the [data grid component](using-the-data-grid-component) for more information. |

### Provide to delete an assignment

If you want to provide to delete an assignment, you have to define the `deleteContext`. There are two types of the `deleteContext`.
The first one is the `one-to-many` type, which link to a column of the assignment entity like this:

```js
// Example of a one-to-many deleteContext
deleteContext: {
    type: 'one-to-many',
    entity: 'cms_block',
    column: 'extensions.swagCmsExtensionsBlockRule.visibilityRuleId',
},
```

The other type is `many-to-many`, which has to link to the `ManyToManyAssociationField` of the extension like this:

```js
// Example of a many-to-many deleteContext
deleteContext: {
    type: 'many-to-many',
    entity: 'category',
    column: 'extensions.swagDynamicAccessRules',
},
```

### Provide to add an assignment

If you want to provide to add an assignment, you have to define the `addContext`. This context has the same two types as the `deleteContext` (see above),
but the `addContext` has more options to fill out, because an add assignment modal has to be configured:

```js
// Example of a one-to-many addContext
addContext: {
    type: 'one-to-many',
    entity: 'shipping_method',
    column: 'availabilityRuleId',
    searchColumn: 'name',
    criteria: () => {
        const criteria = new Criteria();
        criteria.addFilter(Criteria.not(
            'AND',
            [Criteria.equals('availabilityRuleId', ruleId)],
        ));

        return criteria;
    },
    gridColumns: [
        {
            property: 'name',
            label: 'Name',
            rawData: true,
            sortable: true,
            allowEdit: false,
        },
        {
            property: 'description',
            label: 'Description',
            rawData: true,
            sortable: true,
            allowEdit: false,
        },
        {
            property: 'taxType',
            label: 'Tax calculation',
            rawData: true,
            sortable: true,
            allowEdit: false,
        },
        {
            property: 'active',
            label: 'Active',
            rawData: true,
            sortable: true,
            allowEdit: false,
        },
    ],
},
```

The `addContext` needs a definition of the `gridColumns`, the `entity` and the `criteria`, like in the general configuration.
Also, the context needs the `column` of the assignment and the `searchColumn` of the assigned entity.

A context of the `many-to-many` type would look like this:

```js
// Example of a many-to-many addContext
addContext: {
    type: 'many-to-many',
    entity: 'swag_dynamic_access_category_rule',
    column: 'categoryId',
    searchColumn: 'name',
    association: 'swagDynamicAccessRules',
    criteria: () => {
        const criteria = new Criteria();
        criteria.addFilter(Criteria.equals('parentId', null));

        return criteria;
    },
    gridColumns: [
        // Definition of columns
    ],
},
```

Beside the properties of a `one-to-many` type you have to define the `association` with the name of the `ManyToManyAssociationField`.

## Further reading

For more other information, refer to [Add custom rules](../framework/rule/add-custom-rules).

---

---

## Adding Shortcuts
**Source:** [guides/plugins/plugins/administration/add-shortcuts.md](https://developer.shopware.com/docs/v6.5/guides/plugins/plugins/administration/add-shortcuts.md)  
# Adding Shortcuts

## Overview

Shortcuts in Shopware 6 are defined on a Component basis. This guide will show you how to add your own ones.

## Prerequisites

All you need for this guide is a running Shopware 6 instance and full access to both the files and preferably a registered module and custom component.
Of course you'll have to understand JavaScript, but that's a prerequisite for Shopware as a whole and will not be taught as part of this documentation.

## Configuring the Shortcuts

The following code sample will show you how to register shortcuts in your components with help of the `shortcuts` attribute.

```javascript
// <plugin root>/src/Resources/app/administration/src/module/swag-example/index.js
const { Component } = Shopware;

Component.register('swag-basic-example', {
    
    shortcuts: {
        'SYSTEMKEY+S': {
            active() {
                return this.acl.can('product.editor');
            },
            method: 'myEditProductFunction'
        },
        ESCAPE: 'myCancelEditProductFunction'
    },

   
    methods: {
        myEditProductFunction() {
            console.log("myEditProductFunction")
        },
        myCancelEditProductFunction() {
            console.log("myCancelEditProductFunction")
        }
    }
});
```

The first keyboard shortcut reacts to the key combination of `SYSTEMKEY+S`, only if the user has the privilege `product.editor`, with the invocation of the component method with the name `myEditProductFunction`.
The second keyboard shortcut defines that, upon the `ESCAPE` key being pressed, the function with the name `myCancelEditProductFunction` should be invoked.

The before mentioned `SYSTEMKEY` is `CTRL` on macOS and `ALT` on Windows, other system-keys like `CTRL` on Windows or `⌥` on macOS are not supported.

Since ACL is used in the first keyboard shortcut you might want to learn more about ACL and how to add your own ACL rules [here](./add-acl-rules).

## More interesting topics

* [Writing templates](./writing-templates)
* [Adding styles](./add-custom-styles)

---

---

## Using Directives
**Source:** [guides/plugins/plugins/administration/adding-directives.md](https://developer.shopware.com/docs/v6.5/guides/plugins/plugins/administration/adding-directives.md)  
# Using Directives

## Overview

Directives in the Shopware 6 Administration are essentially the same as in any other Vue application. This guide will teach you how to register your directives on a global and on a local scope.

Learn more about Vue Directives in their documentation:

## Prerequisites

All you need for this guide is a running Shopware 6 instance and full access to both the files and preferably a registered module. Of course you'll have to understand JavaScript, but that's a prerequisite for Shopware as a whole and will not be taught as part of this documentation.

## Registering a directives globally

Directives can be registered globally via the [Shopware Objects](the-shopware-object) `register` helper function as seen below:

```javascript
// <plugin-root>/src/Resources/app/administration/app/src/directive/focus.js
const { Directive } = Shopware;

Directive.register('focus', {
    // when the bound element is inserted into the DOM...
    inserted: function (el) {
        // Focus the element
        el.focus();
    }
});
```

As you might have seen, this is the exact same example as in the [Vue documentation](https://vuejs.org/v2/guide/custom-directive.html). Now, the only thing that's left is importing this file in your `main.js`. Then you can use it in the same way as you would do a normal Vue directive.

## Registering a directives locally

Registering directives locally is exactly the same as you're familiar with in Vue. The code snippet below registers the example from the [Vue documentation](https://vuejs.org/v2/guide/custom-directive.html) locally to the `swag-basic-example` component.

```javascript
// <plugin-root>/src/Resources/app/administration/app/src/component/swag-basic-example/index.js
Shopware.Component.register('swag-basic-example', {

    directives: {
        focus: {
            // When the bound element is inserted into the DOM...
            inserted: function (el) {
                // Focus the element
                el.focus();
            }
        }
    }

});
```

As mentioned before, directives can be used as in any other Vue application, after they are registered:

```html
// <plugin-root>/src/Resources/app/administration/app/src/component/swag-basic-example/swag-basic-example.html.twig
<input type="text" v-focus="">
```

::: warning
Make sure the directive you are trying to access is actually in your components scope, either by registering the directive globally or locally to a component.
:::

---

---

## Adding responsive behavior
**Source:** [guides/plugins/plugins/administration/adding-responsive-behavior.md](https://developer.shopware.com/docs/v6.5/guides/plugins/plugins/administration/adding-responsive-behavior.md)  
# Adding responsive behavior

## Overview

The Shopware 6 Administration provides two ways of adding classes to elements based on their size, the device helper and the `v-responsive` directive. Alternatively you can use `css` media queries to make your plugin responsive. Learn how to use `css` here:

## DeviceHelper

The DeviceHelper provides methods to get device and browser information like the current viewport size. The helper methods can be accessed with `this.$device` in every Vue component, since it is bound to the Vue prototype.

It makes it possible to run functions to react to `onResize` events with adding classes or removing them. The example below shows you how to use the `$device.onResize` helper.

```javascript
const listener = function (ev) {
    // do something on resize with the event, like adding or removing classes to elements   
};

const scope = this;
const component = 'sw-basic-example';

this.$device.onResize({ listener, scope, component });
```

The code snippet before could be placed in the `mounted` [Vue lifecycle](https://vuejs.org/v2/guide/instance.html#Lifecycle-Diagram) hook to register those listeners automatically. Then you can automatically remove the listeners in the `onDestroy` hook

```javascript
this.$device.removeResizeListener(component);
```

It also provides many helper functions e.g. to get the screen dimensions. Although there are many more as seen below:

| Function | Description |
| :--- | :--- |
| `this.$device.getViewportWidth();` | Gets the viewport width |
| `this.$device.getViewportHeight();` | Gets the viewport height |
| `this.$device.getDevicePixelRatio();` | Gets the device pixel ratio |
| `this.$device.getScreenWidth();` | Gets the screen width |
| `this.$device.getScreenHeight();` | Gets screen height |
| `this.$device.getScreenOrientation();` | Gets the screen orientation |

## v-responsive directive

The `v-responsive` directive can be used to dynamically apply classes based on an element's dimensions.

```html
<input v-responsive="{ 'is--compact': el => el.width <= 1620, timeout: 200 }">
```

Let's do a small explanation of this directive:

* Apply class (in this case: `is--compact`) when the width of the element is smaller than 1620px.
* `timeout`: Sets the duration on how much the throttle should wait.

---

---

## Adding snippets
**Source:** [guides/plugins/plugins/administration/adding-snippets.md](https://developer.shopware.com/docs/v6.5/guides/plugins/plugins/administration/adding-snippets.md)  
# Adding snippets

## Overview

By default Shopware 6 uses the [Vue I18n](https://kazupon.github.io/vue-i18n/started.html#html) plugin in the `Administration` to deal with translation.

## Creating snippet files

Normally you use snippets in your custom module. To keep things organized, create a new directory named `snippet` inside module directory `<plugin root>/src/Resources/app/administration/src/module/<your-module>/snippet`. For each language you want to support, you need a JSON file inside it, e.g., `de-DE.json`, `en-GB.json`.

::: info
Providing snippets for apps works the same as in plugins but it has a more simplistic file structure. Also, unlike plugins, App-Snippets **are not allowed** to override existing snippet keys. So, use the following path for vendor-prefixed app snippet files: `<app root>/Resources/app/administration/snippet`
:::

Each language then receives a nested object of translations, so let's have a look at an example `snippet/en-GB.json`:

```json
{
    "swag-example": {
        "nested": {
            "value": "example",
            "examplePluralization": "1 Product | {n} Products"
        },
        "foo": "bar"
    }
}
```

In this example you would have access the two translations by the following paths: `swag-example.nested.value` to get the value 'example' and `swag-example.foo` to get the value 'bar'. You can nest those objects as much as you want.

By default, Shopware 6 will collect those files automatically when your plugin is activated.

::: info
When you do not build a module and therefore do not fit into the suggested directory structure, you can still place the translation files anywhere in `<plugin root>/src/Resources/app/administration/`.
:::

## Using the snippets in JavaScript

Since snippets are automatically registered in the scope of your module, you can use them directly:

```javascript
Component.register('my-custom-page', {
    ...

    methods: {
        createdComponent() {
            // call the $tc helper function provided by Vue I18n 
            const myCustomText = this.$tc('swag-example.general.myCustomText');

            console.log(myCustomText);
        }
    }
    ...
});
```

## Using the snippets in templates

The same `$tc` helper function can be used in the templates to access translations.

```twig
{% block my_custom_block %}
    <p>
       {{ $tc('swag-example.general.myCustomText') }}
    </p>
{% endblock %}
```

Another feature of `$tc` is pluralization. Use a `|` in snippets to provide translations depending on the number. The first part shows singular expression, while the second takes care of plural cases.
Let's have a look at this example of `"examplePluralization": "One Product | {n} Products"` with the following implementation:

```twig
{% block my_custom_block %}
    <p>
       {{ $tc('swag-example.nested.examplePluralization', products.length) }}
    </p>
{% endblock %}
```

If you provide `1` as the second parameter to `$tc()`, the text `One Product` would be rendered. For any other value greater than 1, the number itself is shown — for example, `4 Products`.

## More interesting topics

* [Learning about the global Shopware object](the-shopware-object)
* [Learning about the VueX state](https://github.com/shopware/docs/tree/575c2fa12ef272dc25744975e2f1e4d44721f0f1/guides/plugins/plugins/administration/using-vuex-state.md)

---

---

