# APP SYSTEM

Compiled excerpts from the Shopware Developer Documentation snapshot. Prefer live docs at [developer.shopware.com](https://developer.shopware.com/) when in doubt.

---

## Starter Guide - Read and Write Data
**Source:** [guides/plugins/apps/starter/product-translator.md](https://developer.shopware.com/docs/v6.6/guides/plugins/apps/starter/product-translator.md)  
*(Body truncated in this bundle; follow the link for the rest.)*

# Starter Guide - Read and Write Data

This guide will show you how to set up an app server with our [app bundle](https://github.com/shopware/app-bundle-symfony).
You will learn how to read and write data to the Shopware Admin API using an example of fetching dynamic translations for products when they are updated.

## Prerequisites

* Basic CLI usage (creating files, directories, running commands)
* Installed [shopware-cli](../../../../products/cli/) tools
* Installed [symfony-cli](https://symfony.com/download)
* A running MariaDB or MySQL accessible to your development machine

## Setting up the app template

First, we need to create a new Symfony project using Symfony-CLI

```sh
symfony new translator-app
```

The app template contains a basic Symfony application.

Now we need to install the Shopware App Bundle with Composer:

```sh
composer require shopware/app-bundle
```

::: warning
Make sure that you agree to second interaction of the bundle recipe. It will add your routing, register the bundle, and more. If you do not agree to it, you will have to
create those manually (check files [here](https://github.com/symfony/recipes-contrib/tree/main/shopware/app-bundle/1.0))
:::

```shell
-  WARNING  shopware/app-bundle (>=1.0): From github.com/symfony/recipes-contrib:main
   The recipe for this package comes from the "contrib" repository, which is open to community contributions.
   Review the recipe at https://github.com/symfony/recipes-contrib/tree/main/shopware/app-bundle/1.0

    Do you want to execute this recipe?
    [y] Yes
    [n] No
    [a] Yes for all packages, only for the current installation session
    [p] Yes permanently, never ask again for this project
    (defaults to n): n
```

Modify the `SHOPWARE_APP_NAME` and `SHOPWARE_APP_SECRET` in the env to your app name`./.env` to ensure you can install the app in a store later.
Also, configure the `DATABASE_URL` to point to your database:

```sh
// .env
....

###> shopware/app-bundle ###
SHOPWARE_APP_NAME=TestApp
SHOPWARE_APP_SECRET=TestSecret
###< shopware/app-bundle ###
```

You can now start the application with `symfony server:start -v`.

For now, your app server is currently only available locally.

::: info
When you are using a local Shopware environment, you can skip to the [next chapter](#creating-the-manifest)
:::

We need to expose your local app server to the internet. The easiest way to achieve that is using a tunneling service like [ngrok](https://ngrok.com/).

The setup is as simple as calling the following command (after installing ngrok)

```sh
ngrok http 8000
```

This will expose your Symfony server on a public URL, so the cloud store can communicate with your app.

## Creating the manifest

The `manifest.xml` is the main interface definition between stores and your app server.
It contains all the required information about your app.
Let's start by filling in all the meta-information:

```xml
// release/manifest.xml
<?xml version="1.0" encoding="UTF-8" ?>
<manifest xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://raw.githubusercontent.com/shopware/shopware/trunk/src/Core/Framework/App/Manifest/Schema/manifest-2.0.xsd">
    <meta>
        <name>product-translator</name>
        <label>Product translator</label>
        <description>App to translate product descriptions</description>
        <author>shopware AG</author>
        <copyright>(c) by shopware AG</copyright>
        <version>0.1.0</version>
        <license>MIT</license>
    </meta>
   </manifest>
```

::: warning
Take care to use the same `<name>` as in the `.env` file. Otherwise, stores can't install the app.
:::

### Setup hook

Next, we will define the `<setup>` part of the manifest. This part describes how the store will connect itself with the app server.

```xml
// release/manifest.xml
<?xml version="1.0" encoding="UTF-8" ?>
<manifest xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://raw.githubusercontent.com/shopware/shopware/trunk/src/Core/Framework/App/Manifest/Schema/manifest-2.0.xsd">
    <meta>
    <!-- ... -->
    </meta>
    <setup>
        <registrationUrl>http://localhost:8000/app/lifecycle/register</registrationUrl>
        <secret>TestSecret</secret>
    </setup>
</manifest>
```

The `<registraionUrl>` is already implemented by the app template and is always `/app/lifecycle/register`, unless you modify `config/routes/shopware_app.yaml`.
The `<secret>` element is only present in development versions of the app. In production, the extension store will provide the secret to authenticate your app buyers.

### Permissions

The manifest needs permissions as this app will read product descriptions and translate them:

```xml
// release/manifest.xml
<?xml version="1.0" encoding="UTF-8" ?>
<manifest xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://raw.githubusercontent.com/shopware/shopware/trunk/src/Core/Framework/App/Manifest/Schema/manifest-2.0.xsd">
    <meta>
    <!-- ... -->
    </meta>
    <setup>
    <!-- ... -->
    </setup>
    <permissions>
        <read>product</read>
        <read>product_translation</read>
        <read>language</read>
        <read>locale</read>
        <update>product</update>
        <update>product_translation</update>
        <create>product_translation</create>
    </permissions>
</manifest>
```

### Webhooks

Finally, your app needs to be notified every time a product description is modified.
The app system provides webhooks to subscribe your app server to any changes in the data
in its shops:

```xml
// release/manifest.xml
<?xml version="1.0" encoding="UTF-8" ?>
<manifest xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://raw.githubusercontent.com/shopware/shopware/trunk/src/Core/Framework/App/Manifest/Schema/manifest-2.0.xsd">
    <meta>
    <!-- ... -->
    </meta>
    <setup>
    <!-- ... -->
    </setup>
    <permissions>
    <!-- ... -->
    </permissions>
    <webhooks>
        <webhook name="appActivated" url="http://localhost:8000/app/lifecycle/activate" event="app.activated"/>
        <webhook name="appDeactivated" url="http://localhost:8000/app/lifecycle/deactivate" event="app.deactivated"/>
        <webhook name="appDeleted" url="http://localhost:8000/app/lifecycle/delete" event="app.deleted"/>
        <webhook name="productWritten" url="http://localhost:8000/app/webhook" event="product.written"/>
    </webhooks>
</manifest>
```

::: info
The timeout for the requests against the app server is 5 seconds.
:::

The App Bundle provides these four webhooks, so the Bundle does the complete lifecycle and handling of Webhooks for you.

## Handling shop events

To get started, let's write a simple [Symfony event listener](https://symfony.com/doc/current/event_dispatcher.html#creating-an-event-listener):

```php
// src/EventListener/ProductWrittenWebhookListener.php
#[AsEventListener(event: 'webhook.product.written')]
class ProductWrittenWebhookListener
{
    public function __construct(private readonly ClientFactory $clientFactory, private readonly LoggerInterface $logger)
    {
    }

    public function __invoke(WebhookAction $action): void
    {
    }
}
```

### Creating a shop client

The Bundle verifies for you the Request and provides you the Webhook parsed together with the Shop it has requested it.
With the Shop, we can create a pre-authenticated PSR-18 Client to communicate with the Shop.
In this example, we will use the SimpleHttpClient which simples the usage of the PSR-18 Client.

```php
// src/EventListener/ProductWrittenWebhookListener.php
    public function __invoke(WebhookAction $action): void
    {
        $client = $this->clientFactory->createSimpleClient($action->shop);
    }
```

Now we can inspect the event payload:

```php
// src/EventListener/ProductWrittenWebhookListener.php
    public function __invoke(WebhookAction $action): void
    {
        //...

        $updatedFields = $action->payload[0]['updatedFields'];
        $id = $action->payload[0]['primaryKey'];

        if (!in_array('description', $updatedFields)) {
            return;
        }
    }
```

### Fetching data from the shop

All `$entity.written` events contain a list of fields that a written event has changed.
The code above uses this information to determine if someone changed the description of a product.
If the change does not affect the description, the listener early returns because there is nothing else to do with this event.

Now that it is certain that someone changed the description of the product, we fetch the description through the API of the shop:

```php
// src/EventListener/ProductWrittenWebhookListener.php
    public function __invoke(WebhookAction $action): void
    {
        //...
        $response = $client->post(
            sprintf('%s/api/search/product', $action->shop->getShopUrl()),
            [
                'ids' => [$id],
                'associations' => [
                    'translations' => [
                        'associations' => [
                            'language' => [
                                'associations' => [
                                    'locale' => []
                                ]
                            ],
                        ]
                    ],
                ]
            ]
        );
        
        if (!$response->ok()) {
            $this->logger->error('Could not fetch product', ['response' => $response->json()]);
            return;
        }
    }
```

The request contains a criteria that fetches the product for which we received the event `'ids' => [$id]` and all translations and their associated languages `'associations' => 'language'`. Now we can retrieve the English description from the API response:

```php
// src/EventListener/ProductWrittenWebhookListener.php
    public function __invoke(WebhookAction $action): void
    {
        //...
        $product = $response->json()['data'][0];
        $description = '';
        $name = '';
        foreach ($product['translations'] as $translation) {
            if ($translation['language']['locale']['code'] === 'en-GB') {
                $description = $translation['description'];
                $name = $translation['name'];
            }
        }
    }
```

::: info
A common gotcha with `entity.written` webhooks is that they trigger themselves when you're performing write operations. Updating the description triggers another `entity.written` event. This again calls the webhook, which updates the description, and so on.
:::

Because our goal is to write a French translation of the product, the app needs to take care to avoid endless loops.
To determine if the app has already written a translation once, it saves a hash of the original description.
We will get to the generation of the hash later, but we need to check it first:

```php
// src/EventListener/ProductWrittenWebhookListener.php
    public function __invoke(WebhookAction $action): void
    {
        //...
        $lastHash = $product['customFields']['translator-last-translation-hash'] ?? '';
        if (md5($description) === $lastHash) {
            return;
        }
    }
```

### Writing a translated description

Now that the app can be sure, the description has not been translated before it can write the new description like so:

```php
// src/EventListener/ProductWrittenWebhookListener.php
    public function __invoke(WebhookAction $action): void
    {
        //...
        $response = $client->patch(sprintf('%s/api/product/%s', $action->shop->getShopUrl(), $id), [
            'translations' => [
                'en-GB' => [
                    'name' => $name,
                    'description' => $this->translate($description)
                ],
            ],
            'customFields' => [
                'translator-last-translation-hash' => md5($description)
            ]
        ]);

        if (!$response->ok()) {

… **Truncated.** Full document: https://developer.shopware.com/docs/v6.6/guides/plugins/apps/starter/product-translator.md


---

## Starter Guide - Create an Admin Extension
**Source:** [guides/plugins/apps/starter/starter-admin-extension.md](https://developer.shopware.com/docs/v6.6/guides/plugins/apps/starter/starter-admin-extension.md)  
# Starter Guide - Create an Admin Extension

In this guide, you will learn how to set up an extension for the Administration UI.

![An admin notification](../../../../assets/extension-api-notification.png)

## Prerequisites

In order to follow this guide, make sure you are familiar with and meet the following requirements:

* Basic CLI usage (creating files, directories, running commands)
* Installed [shopware-cli](../../../../products/cli/) tools
* We will use the following libraries/software
  * npm
  * live-server (small local development live-reloading server)

## Create the app wrapper

First of all, we need to create the app "wrapper", the so-called app manifest. It is just a single XML file with some basic configuration.

### Create manifest file

First of all, we create the manifest file in a new directory. We'll call that our "project directory".

```text
SimpleNotification/
├─ manifest.xml
```

::: info
When you are using a self-hosted Shopware version, you can also create the project directory in the `custom/apps` directory of your Shopware installation. However, the descriptions in this guide apply to both Shopware cloud and self-hosted stores.
:::

Next, we will put our basic configuration into the file we just created.

::: code-group

```xml [manifest.xml]
<?xml version="1.0" encoding="UTF-8"?>
<manifest xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://raw.githubusercontent.com/shopware/shopware/trunk/src/Core/Framework/App/Manifest/Schema/manifest-2.0.xsd">
    <meta>
        <name>SimpleNotification</name>
        <label>Hi Developer App</label>
        <description>This app shows a notification in the admin panel</description>
        <author>shopware AG</author>
        <copyright>(c) shopware AG</copyright>
        <version>1.0.0</version>
        <license>MIT</license>
    </meta>
</manifest>
```

:::

## Set up communication between Shopware and the app

Next, we need to set up an entry point, so Shopware and your app can communicate. The entry point is a static `.html` file, which includes the Extension SDK script and defines our extension.

![Communication between the admin panel and your entry point](../../../../assets/extension-api-communication.png)

The file will be rendered as a hidden iFrame within your admin panel. Using `postMessage` requests, the iFrame and your admin panel can communicate and exchange data.

Let's create an `index.html` file in a directory called `src`.

```text
SimpleNotification/
├─ src/
│  ├─ index.html
├─ manifest.xml
```

```html
// src/index.html
<!doctype html>
<html>
    <head>
        <script src="https://unpkg.com/@shopware-ag/meteor-admin-sdk/cdn"></script>
    </head>
    <script>
        sw.notification.dispatch({
            title: 'Hi there',
            message: 'Looks like someone sent you a message'
        });
    </script>
</html>
```

This file contains the basic setup for our app to display the notification:

* The HTML is rendered in a hidden iFrame when the Administration panel is loaded.
* The Meteor Admin SDK script is loaded through a CDN and exposed as the `sw` object.
* We use the `notification.dispatch` SDK method to display a simple notification with a title and a message.

### Start the local development server

Next, we need to start the live server, so you don't always have to reload the page manually.

```bash
npm install -g live-server
live-server src
```

Now the file should be available on <http://127.0.0.1:8080>.

### Add the entry point link to your manifest

The final step of the setup is to configure your app to use that file as an entry point.

To do that, we have to add an `admin` section to our `manifest.xml` file and pass it into the `base-app-url` tag:

::: code-group

```xml [manifest.xml]
<?xml version="1.0" encoding="UTF-8"?>
<manifest xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://raw.githubusercontent.com/shopware/shopware/trunk/src/Core/Framework/App/Manifest/Schema/manifest-2.0.xsd">
    <meta>
        <!-- ... -->
    </meta>
  <setup>
    <registrationUrl>http://127.0.0.1:8000/app/lifecycle/register</registrationUrl>
    <secret>TestSecret</secret>
  </setup>
    <admin>
        <base-app-url>http://127.0.0.1:8080</base-app-url>
    </admin>
</manifest>
```

:::

Since the URL to your entry point is only available locally, you will only be able to see changes on your own machine. If you want to share it, for development purposes, you need to host the entry point file somewhere or use services to expose local files as public URLs, such as [ngrok](https://ngrok.com/).

For production usage, you should host the entry point file on a public CDN or a static site hosting.

## Install the app

In this last step, we will install the app using the Shopware CLI tools.

::: info
If this is your first time using the Shopware CLI, you have to [install](../../../../products/cli/installation) it first. Next, configure it using the `shopware-cli project config init` command.
:::

```bash
shopware-cli project extension upload SimpleNotification --activate --increase-version
```

This command will create a zip file from the specified extension directory and upload it to your configured store.
The `--increase-version` parameter increases the version specified in the `manifest.xml` file. This flag is required so Shopware picks up changes made to the `manifest.xml` since the last installation.
When the app is successfully installed, you will see the notification pop up once you open the Shopware admin panel - congratulations!

## Where to continue

This example showed end-to-end how to create a local dev environment and connect it with your Shopware Store. There is a lot more to learn and try out, so why not move on with one of those topics:

* Did you know, you can add [new sections](/resources/admin-extension-sdk/api-reference/ui/component-section) to the UI or even [entire modules](/resources/admin-extension-sdk/api-reference/ui/mainModule)?
* The Meteor Admin SDK also offers [TypeScript support](/resources/admin-extension-sdk/getting-started/installation#using-npm-require-bundling) (including autocompletion)
* Don't want to extend the admin panel? Have a look at [App Scripts](/docs/guides/plugins/apps/app-scripts/index.md)

---

---

## Storefront
**Source:** [guides/plugins/apps/storefront.md](https://developer.shopware.com/docs/v6.6/guides/plugins/apps/storefront.md)  
# Storefront

You can modify the whole appearance of the Storefront within your app. This includes [customizing templates](../../apps/storefront/customize-templates), [adding custom Javascript](../../plugins/storefront/add-custom-javascript) and [custom styling](../../plugins/storefront/add-custom-styling).

As the Shopware server will build the Storefront, you don't have to set up any external servers for this. All you have to do is include your modifications (in form of `.html.twig`, `.js` or `.scss` files) inside the `Resources` folder of your app. The base folder structure of your app may look like this:

```text
└── DemoApp
    ├── Resources
    │   ├── app
    │   │   └── storefront
    │   │       └── src
    │   │           ├── scss
    │   │           │   └── base.scss
    │   │           └── main.js
    │   ├── views
    │   │   └── storefront
    │   │       └── ...
    │   └── public
    │       └── ... // public assets go here
    └── manifest.xml
```

## Custom Assets in Apps

::: info
Note that this feature was introduced in Shopware 6.4.8.0, and is not supported in previous versions.
:::

You may want to include custom assets inside your app, like custom fonts, etc.
Therefore, place the assets you need in the `/Resources/public` folder. All files inside this folder are available over the [asset-system](../../plugins/storefront/add-custom-assets#adding-custom-assets-to-your-plugin).

## Custom Template Priority

::: info
Note that this feature was introduced in Shopware 6.4.12.0, and is not supported in previous versions.
:::

You may want your templates loaded before or after other extensions. To do so, you can define a `template-load-priority` inside your `manifest.xml`. The default value to this is 0, with positive numbers your template will be loaded earlier, and with negative numbers later.

::: code-group

```xml [manifest.xml]
<?xml version="1.0" encoding="UTF-8"?>
<manifest xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"  xsi:noNamespaceSchemaLocation="https://raw.githubusercontent.com/shopware/shopware/trunk/src/Core/Framework/App/Manifest/Schema/manifest-2.0.xsd">
    <meta>
        ....
    </meta>
    <storefront>
        <template-load-priority>100</template-load-priority>
    </storefront>    
</manifest>
```

:::

---

---

## Apps as themes
**Source:** [guides/plugins/apps/storefront/apps-as-themes.md](https://developer.shopware.com/docs/v6.6/guides/plugins/apps/storefront/apps-as-themes.md)  
# Apps as themes

It is absolutely possible to ship whole [themes](../../themes/) inside an app. All you have to do is include your theme configuration (in the form of a [theme.json](../../../plugins/themes/theme-configuration) file) inside your app's Resources folder.\
So the folder structure of a theme may look like this:

```text
└── DemoTheme
      └── Resources
            └── ...
            └── theme.json
      └── manifest.xml
```

## Themes vs. "ordinary" apps

If your app provides a `theme.json` file, it is considered to be a theme. All the changes you make to the Storefront's appearance inside your theme will be visible only if your theme is assigned to the Storefront. In contrast, if you don't provide a `theme.json` file, your app is an "ordinary" app. The changes will be applied to all sales channels automatically, as long as your app is active.

## Migrating existing themes

If you have already created Shopware 6 themes via plugins, it is effortless to migrate them to the app system. Don't worry, you don't have to do all the work twice. Instead of providing a `composer.json` and plugin base class, provide a `manifest.xml` file with the metadata for your app. After you have created a new folder for your app and added the `manifest.xml`, you can copy the `YourThemePlugin/src/Resources` folder from your plugin to the `YourThemeApp/Resources` folder inside your app. It should not be necessary to change anything inside your template or Javascript code.

---

---

## Add cookies to the consent manager
**Source:** [guides/plugins/apps/storefront/cookies-with-apps.md](https://developer.shopware.com/docs/v6.6/guides/plugins/apps/storefront/cookies-with-apps.md)  
# Add cookies to the consent manager

## Prerequisites

You should be familiar with the concept of apps.

## Create a single cookie

To add new cookies to the cookie consent manager, you can add a `cookies` section to your `manifest.xml`. Inside this section, you can add new `cookie` elements, as shown in the following example. Note that you don't need a `setup` section in your `manifest.xml` since extending the Storefront doesn't need a registration nor an own server to run.

::: code-group

```xml [manifest.xml]
<?xml version="1.0" encoding="UTF-8"?>
<manifest xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://raw.githubusercontent.com/shopware/shopware/trunk/src/Core/Framework/App/Manifest/Schema/manifest-2.0.xsd">
    <meta>
        <name>ExampleAppWithCookies</name>
        <version>1.0.0</version>
        <!-- other meta data goes here -->
    </meta>
    <cookies>
        <cookie>
            <cookie>my-cookie</cookie>
            <snippet-name>example-app-with-cookies.my-cookie.name</snippet-name>
            <snippet-description>example-app-with-cookies.my-cookie.description</snippet-description>
            <value>a static value for the cookie</value>
            <expiration>1</expiration>
        </cookie>
    </cookies>
</manifest>
```

:::

Cookie elements can be configured by adding the following child elements:

* `cookie` (required): The technical name of the cookie. The value is used to store the cookie in the customer's cookie jar.
* `snippet-name` (required): A string that represents the label of the cookie in the cookie consent manager. To provide translations this should be the key of a Storefront snippet.
* `value` (optional): A fixed value that is set as the cookie's value when the customer accepts your cookie. **If unset, the cookie will not be updated (set active or inactive) by Shopware, but passed to the update event.**
* `expiration` (optional): Cookie lifetime in days. **If unset, the cookie expires with the session.**
* `snippet-description` (optional): A string that represents the description of the cookie in the cookie consent manager. To provide translations, this should be the key of a Storefront snippet.

For a complete reference of the structure of the manifest file, take a look at the [Manifest reference](../../../../resources/references/app-reference/manifest-reference).

## Create a cookie group

When adding multiple cookies through your app it may become handy to group them. This makes it possible for the customer to accept all of your cookies at once and additionally enhances the readability of the cookie consent manager.

To add a cookie group, you can add a `groups` section within your `cookies` section in your `manifest.xml`. In the following example, we use the cookie that we created in the previous section but display it in a cookie group:

::: code-group

```xml [manifest.xml]
<?xml version="1.0" encoding="UTF-8"?>
<manifest xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://raw.githubusercontent.com/shopware/shopware/trunk/src/Core/Framework/App/Manifest/Schema/manifest-2.0.xsd">
    <meta>
        <name>ExampleAppWithCookies</name>
        <version>1.0.0</version>
        <!-- other meta data goes here -->
    </meta>
    <cookies>
        <group>
            <snippet-name>example-app-with-cookies.cookie-group.name</snippet-name>
            <snippet-description>example-app-with-cookies.cookie-group.description</snippet-description>
            <entries>
                <cookie>
                    <cookie>my-cookie</cookie>
                    <snippet-name>example-app-with-cookies.my-cookie.name</snippet-name>
                    <snippet-description>example-app-with-cookies.my-cookie.description</snippet-description>
                    <value>a static value for the cookie</value>
                    <expiration>1</expiration>
                </cookie>
            </entries>
        </group>
    </cookies>
</manifest>
```

:::

A `group` element consists of three child elements to configure the cookie group. Here is a description of all of them:

* `snippet-name` (required): A string that represents the label of the cookie group in the cookie consent manager. To provide translations this should be the key of a Storefront snippet.
* `entries` (required): Contains the grouped cookies. It is a collection of `cookie` elements described in the previous section.
* `snippet-description` (optional): A string that represents the description of the cookie group in the cookie consent manager. To provide translations this should be the key of a Storefront snippet.

For a complete reference of the structure of the manifest file, take a look at the [Manifest reference](../../../../resources/references/app-reference/manifest-reference).

## Snippet handling

As already mentioned in the previous sections, both the `cookie` and the `group` elements can contain `snippet-name` and `snippet-description` child elements. Although their values can be strings that will be displayed in the Storefront, the preferred way to set up cookie names and descriptions is to provide Storefront snippets. It gives you and the shop owner the possibility to add translations for your cookie's name and description.

If you are not familiar with setting up Storefront snippets, please refer to our snippet guide.

## Reacting to cookie consent changes

As described in the previous section, `cookie` elements without a `value` element will not be set automatically. Instead, you have to react to cookie consent changes within your JavaScript. Find out how to [respond to cookie consent changes](../../../plugins/plugins/storefront/reacting-to-cookie-consent-changes).

---

---

## Customize Templates
**Source:** [guides/plugins/apps/storefront/customize-templates.md](https://developer.shopware.com/docs/v6.6/guides/plugins/apps/storefront/customize-templates.md)  
# Customize Templates

## Overview

This guide will cover customizing Storefront templates using an app.

## Prerequisites

Before you begin, make sure you have:

* A basic understanding of [Shopware app development](../app-base-guide).
* Familiarity with the [Twig template](https://twig.symfony.com/) is beneficial.

## Getting started

This guide assumes you have already set up your Shopware app. If not, refer to the [app base guide](../app-base-guide) for the initial setup.

The following sections give you a very short example of how you can extend a storefront block. For simplicity's sake, only the page logo is replaced with a 'Hello world!' text.

### Setting up app's view directory

First of all, in your app's root, register your app's own view path, which basically represents a path in which Shopware 6 is looking for template-files. By default, Shopware 6 is looking for a directory called `views` in your app's `Resources` directory, so the path could look like this: `<app root>/Resources/views`

### Locating the template

As mentioned earlier, this guide is only trying to replace the 'demo' logo with a 'Hello world!' text. In order to find the proper template, you can simply search for the term 'logo' inside the `<shopware root>/src/Storefront` directory. This will eventually lead you to [this file](https://github.com/shopware/shopware/blob/v6.3.4.1/src/Storefront/Resources/views/storefront/layout/header/logo.html.twig).

::: info
There's a plugin out there called [FroshDevelopmentHelper](https://github.com/FriendsOfShopware/FroshDevelopmentHelper), that adds hints about template blocks and includes into the rendered HTML. This way, it's easier to actually find the proper template.
:::

### Overriding the template

Now that you have found the proper template for the logo, you can override it.

Overriding this file now requires you to copy the exact same directory structure starting from the `views` directory for your custom file. In this case, the file `logo.html.twig` is located in a directory called `storefront/layout/header`, so make sure to remember this path.

Finally, you have to set up the following directory path in your app: `<app root>/Resources/views/storefront/layout/header`. Next, create a new file called `logo.html.twig`, just like the original file. Once more to understand what's going on here: In the Storefront code, the path to the logo file looks like this: `Storefront/Resources/views/storefront/layout/header/logo.html.twig`. Now have a look at the path being used in your app: `<app root>/Resources/views/storefront/layout/header/logo.html.twig`

Starting from the `views` directory, the path is **exactly the same**, and that's the important part for your custom template to be loaded automatically.

### Customizing the template

First extend from the original file, to override its blocks. Now fill your custom `logo.html.twig` file.

Put this line at the very beginning of your file:

```twig
{% sw_extends '@Storefront/storefront/layout/header/logo.html.twig' %}
```

This is simply extending the `logo.html.twig` file from the Storefront bundle. If you would leave the file like that, it wouldn't change anything, as you are currently just extending from the original file with no overrides.

To replace the logo with some custom text, take a look at the block called `layout_header_logo_link` in the original file. Its contents create an anchor tag, which is not necessary for our case anymore, so this seems to be a great block to override.

To override it now, just add the very same block into your custom file and replace its contents:

```twig
{% sw_extends '@Storefront/storefront/layout/header/logo.html.twig' %}

{% block layout_header_logo_link %}
    <h2>Hello world!</h2>
{% endblock %}
```

If you wanted to append your text to the logo instead of replacing it, you could add a line like this to your override: {{ parent() }}

And that's it, you are done. However, you might have to clear the cache and refresh your storefront to see your changes in action. This can be done by using the following command:

```bash
./bin/console cache:clear
```

::: info
Also remember to not only activate your app but also to assign your theme to the correct sales channel by clicking on it in the sidebar, going to the tab Theme and selecting your theme.
:::

### Finding variables

Of course, this example is very simplified and does not use any variables, even though you most likely want to do that. Using variables is exactly the same as in [Twig](https://twig.symfony.com/doc/3.x/templates.html#variables) in general, so this won't be explained here in detail. However, this is how you use a variable: {{ variableName }}

But how do you know which variables are available to use? For this, you can just dump all available variables:

```twig
{{ dump() }}
```

This `dump()` call will print out all variables available on this page.

::: info
Once again, the plugin called [FroshDevelopmentHelper](https://github.com/FriendsOfShopware/FroshDevelopmentHelper) adds all available page data to the Twig tab in the profiler, when opening a request and its details. This might help here as well.
:::

---

---

## Tax provider
**Source:** [guides/plugins/apps/tax-provider.md](https://developer.shopware.com/docs/v6.6/guides/plugins/apps/tax-provider.md)  
# Tax provider

Tax calculations differ from country to country. Especially in the US, the sales tax calculation can be tedious, as the laws and regulations differ from state to state, country-wise, or even based on cities. Therefore, most shops use a third-party service (so-called tax provider) to calculate sales taxes.

With version 6.5.0.0, Shopware allows apps to integrate custom tax calculations, which could include an automatic tax calculation with a tax provider. An app has to provide an endpoint, which is called during the checkout to provide new tax rates. The requests and responses of all of your endpoints will be signed and featured as JSON content.

## Prerequisites

You should be familiar with the concept of Apps, their registration flow as well as signing and verifying requests and responses between Shopware and the App backend server.

Your app server must be also accessible for the Shopware server.
You can use a tunneling service like [ngrok](https://ngrok.com/) for development.

## Manifest configuration

To indicate to Shopware that your app uses a custom tax calculation, you must provide one or more `tax-provider` properties inside a `tax` parent property of your app's `manifest.xml`.

Below, you can see an example definition of a working tax provider.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<manifest xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://raw.githubusercontent.com/shopware/shopware/trunk/src/Core/Framework/App/Manifest/Schema/manifest-3.0.xsd">
    <meta>
        <!-- The name of the app should not change. Otherwise all payment methods are created as duplicates. -->
        <name>PaymentApp</name>
        <!-- ... -->
    </meta>
    <tax>
        <tax-provider>
            <!-- Unique identifier of the tax provider -->
            <identifier>myCustomTaxProvider</identifier>
            <!-- Display name of the tax provider -->
            <name>My custom tax provider</name>
            <!-- Priority of the tax provider - can be changed in the administration as well -->
            <priority>1</priority>
            <!-- Url of your implementation - is called during checkout to provide taxes -->
            <process-url>https://tax-provider.app/provide-taxes</process-url>
        </tax-provider>
    </tax>
</manifest>

```

After successful installation of your app, the tax provider will already be used during checkout to provide taxes. You should also see the new tax provider showing up in the administration in `Settings > Tax`.

## Tax provider endpoint

During checkout, Shopware checks for any active tax providers - sorted by priority - and will call the `processUrl` to provide taxes one-by-one, until one of endpoint successfully provides taxes for the current cart.

::: warning
**Connection timeouts**

The Shopware shop will wait for a response for 5 seconds. Be sure, that your tax provider implementation responds in time, otherwise Shopware will time out and drop the connection.
:::

In response, you can adjust the taxes of the entire cart, the entire delivery, or each item in the cart.

Request content is JSON

```json
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
  }
}
```

You can find an example payload [here](https://github.com/shopware/app-php-sdk/blob/main/tests/Context/_fixtures/tax.json)

and your response should look like this:

```json
{
  // optional: Overwrite the tax of an line item
  "lineItemTaxes": {
    "unique-identifier-of-lineitem": [
      {"tax":19,"taxRate":23,"price":19}
    ]
  },
  // optional: Overwrite the tax of an delivery
  "deliveryTaxes": {
    "unique-identifier-of-delivery-position": [
      {"tax":19,"taxRate":23,"price":19}
    ]
  },
  // optional: Overwrite the tax of the entire cart
  "cartPriceTaxes": [
    {"tax":19,"taxRate":23,"price":19}
  ]
}
```

```php
use Psr\Http\Message\RequestInterface;
use Psr\Http\Message\ResponseInterface;
use Shopware\App\SDK\Shop\ShopResolver;
use Shopware\App\SDK\Context\ContextResolver;

function taxController(RequestInterface $request): ResponseInterface
{
    // injected or build by yourself
    $shopResolver = new ShopResolver($repository);
    $contextResolver = new ContextResolver();
    $signer = new ResponseSigner();
    
    $shop = $shopResolver->resolveShop($serverRequest);
    $taxInfo = $contextResolver->assembleTaxProvider($serverRequest, $shop);
    
    $builder = new TaxProviderResponseBuilder();

    // optional: Add tax for each line item
    foreach ($taxInfo->cart->getLineItems() as $item) {
        $taxRate = 50;

        $price = $item->getPrice()->getTotalPrice() * $taxRate / 100;

        $builder->addLineItemTax($item->getUniqueIdentifier(), new CalculatedTax(
            tax: $price,
            taxRate: $taxRate,
            price: $item->getPrice()->getTotalPrice()
        ));
    }

    // optional: Add tax for each delivery
    foreach ($taxProviderContext->cart->getDeliveries() as $item) {
        foreach ($item->getPositions() as $position) {
            $builder->addDeliveryTax($position->getIdentifier(), new CalculatedTax(
                tax: 10,
                taxRate: 50,
                price: 100
            ));
        }
    }

    // optional: Add tax to the entire cart
    $builder->addCartTax(new CalculatedTax(
        tax: 20,
        taxRate: 50,
        price: 100
    ));
    
    return $signer->signResponse($builder->build(), $shop);
}
```

```php
use Shopware\App\SDK\Context\TaxProvider\TaxProviderAction;
use Shopware\App\SDK\TaxProvider\TaxProviderResponseBuilder;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\HttpKernel\Attribute\AsController;
use Symfony\Component\Routing\Attribute\Route;
use Psr\Http\Message\ResponseInterface;

#[AsController]
class TaxController {
    #[Route('/tax.process')]
    public function handle(TaxProviderAction $taxInfo): ResponseInterface
    {
        $builder = new TaxProviderResponseBuilder();

        // optional: Add tax for each line item
        foreach ($taxInfo->cart->getLineItems() as $item) {
            $taxRate = 50;
    
            $price = $item->getPrice()->getTotalPrice() * $taxRate / 100;
    
            $builder->addLineItemTax($item->getUniqueIdentifier(), new CalculatedTax(
                tax: $price,
                taxRate: $taxRate,
                price: $item->getPrice()->getTotalPrice()
            ));
        }
    
        // optional: Add tax for each delivery
        foreach ($taxProviderContext->cart->getDeliveries() as $item) {
            foreach ($item->getPositions() as $position) {
                $builder->addDeliveryTax($position->getIdentifier(), new CalculatedTax(
                    tax: 10,
                    taxRate: 50,
                    price: 100
                ));
            }
        }
    
        // optional: Add tax to the entire cart
        $builder->addCartTax(new CalculatedTax(
            tax: 20,
            taxRate: 50,
            price: 100
        ));
        
        return $builder->build();
    }
}
```

If you wish to use a tax provider, you will probably have to provide the whole cart for the tax provider to correctly calculate taxes during checkout and you will probably get sums of the specific tax rates, which you can respond to Shopware via `cartPriceTaxes`. If given, Shopware does not recalculate the tax sums and will use those given by your tax provider.

---

---

## Webhook
**Source:** [guides/plugins/apps/webhook.md](https://developer.shopware.com/docs/v6.6/guides/plugins/apps/webhook.md)  
# Webhook

With webhooks, you can subscribe to events occurring in Shopware. Whenever such an event occurs, a `POST` request will be sent to the URL specified for this particular event.

## Prerequisites

You should be familiar with the concept of Apps, especially their registration flow as well as signing and verifying requests and responses between Shopware and the App backend server, as that is required to authenticate the webhooks coming from the shops and showing the correct content in your modules.

## Webhook configuration

To use webhooks in your app, you need to implement a `<webhooks>` element in your manifest file as shown below:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<manifest xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://raw.githubusercontent.com/shopware/shopware/trunk/src/Core/Framework/App/Manifest/Schema/manifest-3.0.xsd">
    <meta>
        ...
    </meta>
    <webhooks>
        <webhook name="product-changed" url="https://example.com/event/product-changed" event="product.written"/>
    </webhooks>
</manifest>

```

This example illustrates how to define a webhook with the name `product-changed` and the URL `https://example.com/event/product-changed`, which will be triggered if the event `product.written` is fired. So every time a product is changed, your custom logic will get executed. Further down, you will find a list of the most important events you can hook into.

An event contains as much data as is needed to react to that event. The data is sent as JSON in the request body:

```json
{
  "data":{
    "payload":[
      {
        "entity":"product",
        "operation":"delete",
        "primaryKey":"7b04ebe416db4ebc93de4d791325e1d9",
        "updatedFields":[
        ]
      }
    ],
    "event":"product.written"
  },
  "source":{
    "url":"http:\/\/localhost:8000",
    "appVersion":"0.0.1",
    "shopId":"dgrH7nLU6tlE",
    "eventId": "7b04ebe416db4ebc93de4d791325e1d9"
  },
  "timestamp": 123123123
}
```

```php
use Psr\Http\Message\RequestInterface;
use Psr\Http\Message\ResponseInterface;
use Shopware\App\SDK\Shop\ShopResolver;
use Shopware\App\SDK\Context\ContextResolver;

function webhookController(RequestInterface $request): ResponseInterface
{
    // injected or build by yourself
    $shopResolver = new ShopResolver($repository);
    $contextResolver = new ContextResolver();
    
    $shop = $shopResolver->resolveShop($serverRequest);
    $webhook = $contextResolver->assembleWebhook($serverRequest, $shop);
    
    // do something with the parsed webhook
}
```

```php
use Shopware\App\SDK\Context\Webhook\WebhookAction;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\HttpKernel\Attribute\AsController;
use Symfony\Component\Routing\Attribute\Route;

#[AsController]
class WebhookController {
    #[Route('/webhook/product.created')]
    public function handle(WebhookAction $webhook): Response
    {
        // handle webhook action
        
        return new Response(null, 204);
    }
}
```

The `source` property contains all necessary information about the Shopware instance that sent the request:

* `url` is the URL under which your app can reach the Shopware instance and its API.
* `appVersion` is the version of the app that is installed.
* `shopId` is the id by which you can identify the Shopware instance.
* `eventId` is a unique identifier of the event. This id will not change if sending of the webhook is retried, etc. **Since 6.4.11.0**.

The next property, `data` contains the name of the event so that a single endpoint can handle several different events. `data` also contains the event data in the `payload` property. Due to the asynchronous nature of these webhooks, the `payload` for `entity.written` events does not contain complete entities as these might become outdated. Instead, the entity in the payload is characterized by its id, stored under `primaryKey`, so the app can fetch additional data through the shop API. This also has the advantage of giving the app explicit control over the associations that get fetched instead of relying on the associations determined by the event. Other events, in contrast, contain the entity data that defines the event but keep in mind that the event might not contain all associations.

The next property, `timestamp` is the time at which the webhook was handled. This can be used to prevent replay attacks, as an attacker cannot change the timestamp without making the signature invalid. If the timestamp is too old, your app should reject the request. This property is only available from 6.4.1.0 onwards

::: info
Starting from Shopware version 6.4.1.0, the current Shopware version will be sent as a `sw-version` header.
Starting from Shopware version 6.4.5.0, the current language id of the shopware context will be sent as a  `sw-context-language` header, and the locale of the user or locale of the context language is available under the `sw-user-language` header.
:::

You can verify the authenticity of the incoming request by checking the `shopware-shop-signature` every request should have a SHA256 HMAC of the request body that is signed with the secret your app assigned the shop during the [registration](app-base-guide#setup). The mechanism to verify the request is exactly the same as the one used for the [confirmation request](app-base-guide#confirmation-request).

You can use a variety of events to react to changes in Shopware that way. See that table [Webhook-Events-Reference](../../../resources/references/app-reference/webhook-events-reference) for an overview.

## Webhooks for live version only

::: info
This feature has been introduced with Shopware version 6.5.7.0
:::

There might be cases when you only want to call the webhook when an entry is written to the database with live version ID (`Shopware\Core\Defaults::LIVE_VERSION`). For example when orders are created, you want to filter out drafts and only call your webhook when an order is actually placed. See more on versioning entities [here](../plugins/framework/data-handling/versioning-entities.md).

You can achieve this by adding the option `onlyLiveVersion` to your webhook definition in the manifest file:

```xml
<webhook name="order-created" url="https://example.com/event/order-created" event="order.written" onlyLiveVersion="true"/>
```

By default, this option is set to `false` and the webhook will be called for every version of the entity.

This option is only checked for instances of `HookableEntityWrittenEvent`. For other events, the option is ignored.

If this option is enabled the payload of your webhook will also be filtered to only contain entries that have live version id.

---

---

