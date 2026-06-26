# ADMIN EXTENSION SDK

Compiled excerpts from the Shopware Developer Documentation snapshot. Prefer live docs at [developer.shopware.com](https://developer.shopware.com/) when in doubt.

---

## Introduction
**Source:** [resources/admin-extension-sdk.md](https://developer.shopware.com/resources/admin-extension-sdk.md)  
# Introduction

The Meteor Admin SDK is an NPM library for Shopware 6 apps and plugins that need an easy way of extending or customizing the Administration.

It contains helper functions to communicate with the Administration, execute actions, subscribe to data or extend the user interface.

* 🏗  **Works with Shopware 6 Apps and Plugins:** you can use the SDK for your plugins or apps. API usage is identical.
* 🎢  **Shallow learning curve:** you don't need to have extensive knowledge about the internals of the Shopware 6 Administration. Our SDK hides the complicated stuff behind a beautiful API.
* 🧰  **Many extension capabilities:** from throwing notifications, accessing context information or extending the current UI. The feature set of the SDK will gradually be extended, providing more possibilities and flexibility for your ideas and solutions.
* 🪨  **A stable API with great backwards compatibility:** don't fear Shopware updates anymore. Breaking changes in this SDK are an exception. If you use the SDK, your apps and plugins will stay stable for a longer time, without any need for code maintenance.
* 🧭  **Type safety:** the whole SDK is written in TypeScript which provides great autocompletion support and more safety for your apps and plugins.
* 💙  **Developer experience:** have a great development experience right from the start. And it will become better and better in the future.
* 🪶  **Lightweight:** the whole library is completely tree-shakable and dependency-free. Every functionality can be imported granularly to keep your bundle as small and fast as possible.

Go to [Installation](./getting-started/installation.md) to get started. Or check out the quick start guide:

## Quick start

Understand the Shopware Extension SDK by learning how to throw a notification.

Requirements for this quick start guide are:

* [Shopware 6 self-hosted instance](https://developer.shopware.com/docs/guides/installation) or a [Shopware 6 cloud instance](https://www.shopware.com/en/shopware-cloud/)
* [clean Shopware 6 Plugin or App](https://developer.shopware.com/docs/guides/plugins/overview) which is activated

### App

1. Create an HTML file with following content:

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
</head>
<body>
  <script src="https://unpkg.com/@shopware-ag/meteor-admin-sdk/cdn"></script>

  <script>
    sw.notification.dispatch({
      title: 'My first notification',
      message: 'This was really easy to do'
    })
  </script>
</body>
</html>
```

2. Add the link to the webpage and to the [manifest.xml](https://developer.shopware.com/docs/guides/plugins/apps/app-base-guide#manifest-file) of your app. For local files you can use [ngrok](https://ngrok.com/) to create a public URL for your HTML file.

3. Visit the Administration. After you have logged in you should see the notification from your app.

Congratulation 🎉 You just created your first interaction with the Administration via the Meteor Admin SDK.

### Plugin

**Notice:** Plugins will only be working on self-hosted instances. You can't use a Shopware 6 cloud instance for plugins.

1. Create a new `index.html` file to your new plugin in the following path: `custom/plugins/yourPlugin/src/Resources/app/administration/index.html`. The HTML file should have the following content:

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
</head>
<body>
  <script src="https://unpkg.com/@shopware-ag/meteor-admin-sdk/cdn"></script>

  <script>
    sw.notification.dispatch({
      title: 'My first notification',
      message: 'This was really easy to do'
    })
  </script>
</body>
</html>
```

2. Start the Shopware 6 Administration watcher using the following command:

```bash
$ bin/watch-administration.sh
```

After all files have been compiled, a new browser window should open, in which you should see the Administration. After logging in, you should see the notification from your plugin.

Congratulations 🎉 You just created your first interaction with the Administration via the Meteor Admin SDK.

---

---

## admin-sdk-docs
**Source:** [resources/admin-extension-sdk/CHANGELOG.md](https://developer.shopware.com/resources/admin-extension-sdk/CHANGELOG.md)  
# admin-sdk-docs

## 1.0.0

### Major Changes

* 0e794ae: Add `uiMediaModalOpen` method
  Add `media` option for parameter `entity`, `view` option for parameter `view` of actionButton method

---

---

## resources/admin-extension-sdk/api-reference.md
**Source:** [resources/admin-extension-sdk/api-reference.md](https://developer.shopware.com/resources/admin-extension-sdk/api-reference.md)  
---

---

## Base options
**Source:** [resources/admin-extension-sdk/api-reference/base-options.md](https://developer.shopware.com/resources/admin-extension-sdk/api-reference/base-options.md)  
# Base options

There are options that exist for every message type in the SDK. You'll find a list with all of them below.

| Name         | Required | Default        | Availability        | Description                                                                                     |
| :----------- | :------- | :------------- | :------------------ | :---------------------------------------------------------------------------------------------- |
| `privileges` | false    |                | >= Shopware 6.6.3.0 | The privileges that will be checked before executing the message in the Shopware Administration |

## Example privileges

```typescript
import * as sw from '@shopware-ag/meteor-admin-sdk';

// This notification will only be displayed if the user has `product:read` permissions.
sw.notification.dispatch({
    message: 'Your product report is ready',
    privileges: [
        'product:read',
    ],
});
```

---

---

## resources/admin-extension-sdk/api-reference/cms.md
**Source:** [resources/admin-extension-sdk/api-reference/cms.md](https://developer.shopware.com/resources/admin-extension-sdk/api-reference/cms.md)  
---

---

## Register CMS block
**Source:** [resources/admin-extension-sdk/api-reference/cms/registerCmsBlock.md](https://developer.shopware.com/resources/admin-extension-sdk/api-reference/cms/registerCmsBlock.md)  
# Register CMS block

> Available since Shopware v6.6.1.0

With `cms.registerCmsBlock` you can register CMS blocks to use in the Shopping Experiences Module.

![Register a CMS block in your Shopping Experiences Module via App](../assets/register-cms-block-example.png)

#### Usage:

```ts
cms.registerCmsBlock({
    name: 'dailymotion-dual-block',
    label: 'ex.cms.dailymotion.block.label',
    slots: [
        { element: 'dailymotionElement' },
        { element: 'dailymotionElement' },
    ],
    // optional properties
    category: 'video',
    previewImage: 'https://placehold.co/350x200',
    slotLayout: {
        grid: 'auto / auto auto'
    },
});
```

#### Parameters

| Name           | Required | Description                                                                                                                                                                                                                                                                                             |
| :------------- | :------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `name`         | true     | The name of the cms block - Should have vendor prefix. It can be used in the Storefront for overriding the default layout.                                                                                                                                                                              |
| `label`        | true     | The label, which is visible when selecting the cms element - Use snippet keys here                                                                                                                                                                                                                      |
| `slots`        | true     | Array containing the slots. The content of the array are objects with the property "element" which refers to a real CMS element (can also be your own custom CMS elements).                                                                                                                             |
| `category `    | false    | The category of the CMS block. This is used to group the CMS blocks in the Shopping Experiences Module. You can use existing ones or create your own category. Then you need to provide a snippet for the category following this pattern: `apps.sw-cms.detail.label.blockCategory.${yourCategoryName}` |
| `previewImage` | false    | The URL of the preview image. This image is shown in the Shopping Experiences Module when selecting the CMS block.                                                                                                                                                                                      |
| `slotLayout`   | false    | The layout of the slots. This is used to define the grid layout of the slots. You can use the [CSS grid shorthand syntax](https://developer.mozilla.org/en-US/docs/Web/CSS/grid) here.                                                                                                                  |

## Storefront usage

The CMS block will render automatically in the Storefront without any additional work. It renders the block as a CSS grid with the slots as grid items and the grid shorthand syntax you provided in the `slotLayout` property.

If you want you can override the default layout by creating a new template file in your app. The file should be named `cms-block-app-renderer.html.twig` and should be placed in the `<your-app>/Resources/views/storefront/block` directory of your app folder. More details on how to customize the Storefront in your App can be found in this documentation: https://developer.shopware.com/docs/guides/plugins/apps/storefront/customize-templates.html

Inside this file you need to define the block layout and the slots. The block which needs to be created follows this naming pattern: `block_app_renderer_${yourBlockName}`. The `${yourBlockName}` is the name of the block you registered with `cms.registerCmsBlock` except that you need to replace the hyphens with underscores.

If you want to have multiple different templates for multiple different CMS blocks you can add new Twig blocks for each CMS block
in the same file.

Example:

```html
{% sw_extends '@Storefront/storefront/block/cms-block-app-renderer.html.twig' %}

{% block block_app_renderer_dailymotion_dual_block %}
    <div>
        <h1>Your custom implementation</h1>

        {# Render each slot content #}
        {% for slot in block.slots %}
            {% set element = block.slots.getSlot(slot.slot) %}

            <div>
                {% sw_include '@Storefront/storefront/element/cms-element-' ~ element.type ~ '.html.twig' ignore missing %}
            </div>
        {% endfor %}
    </div>
{% endblock %}
```

---

---

## Register CMS element
**Source:** [resources/admin-extension-sdk/api-reference/cms/registerCmsElement.md](https://developer.shopware.com/resources/admin-extension-sdk/api-reference/cms/registerCmsElement.md)  
# Register CMS element

> Available since Shopware v6.4.17.0

With `cms.registerCmsElement` you can register CMS elements to use in the Shopping Experiences Module.
More information on how to develop CMS elements can be found in these guides for [plugins](https://developer.shopware.com/docs/guides/plugins/plugins/content/cms/add-cms-element) and [apps](https://developer.shopware.com/docs/guides/plugins/apps/administration/add-cms-element-via-admin-sdk.html).

![Register a CMS element in your Shopping Experiences Module via App](../assets/register-cms-element-example.png)

#### Usage:

```ts
void cms.registerCmsElement({
    name: 'dailymotionElement',
    label: 'Dailymotion Video',
    defaultConfig: {
        dailyUrl: {
            source: 'static',
            value: '',
        },
    },
});
```

#### Parameters

| Name            | Required | Description                                                                                              |
|:----------------|:---------|:---------------------------------------------------------------------------------------------------------|
| `name`          | true     | The name of the cms element, which will also be used to generate locationIds - Should have vendor prefix |
| `label`         | true     | The label, which is visible when selecting the cms element - Use snippet keys here!                      |
| `defaultConfig` | true     | Object containing the defaultConfig; same like in plugin development.                                    |

---

---

## resources/admin-extension-sdk/api-reference/composables.md
**Source:** [resources/admin-extension-sdk/api-reference/composables.md](https://developer.shopware.com/resources/admin-extension-sdk/api-reference/composables.md)  
---

---

## resources/admin-extension-sdk/api-reference/composables/getRepository.md
**Source:** [resources/admin-extension-sdk/api-reference/composables/getRepository.md](https://developer.shopware.com/resources/admin-extension-sdk/api-reference/composables/getRepository.md)  
---

---

## useRepository
**Source:** [resources/admin-extension-sdk/api-reference/composables/useRepository.md](https://developer.shopware.com/resources/admin-extension-sdk/api-reference/composables/useRepository.md)  
# useRepository

The `composables.useRepository` function is a reactive wrapper around the `getRepository` function. It creates a repository instance that automatically updates when its dependencies change. This is particularly useful when you need a repository that responds to reactive data changes in your Vue components.

Unlike `getRepository`, which returns a static repository instance, `useRepository` accepts reactive references (refs) or values as parameters and returns a computed repository that updates when those parameters change.

#### Usage:

```ts
// Inside a Vue component setup
import { ref } from 'vue';
import { composables } from '@shopware-ag/meteor-admin-sdk';
const { useRepository } = composables;

// With a reactive entity name
const entityName = ref('product');
const productRepository = useRepository(entityName);

// The repository updates automatically if entityName changes
entityName.value = 'category';
// Now productRepository.value references a category repository

// With a reactive repository factory
const myFactory = ref(customRepositoryFactory);
const repository = useRepository('product', myFactory);

// Search for products
const products = await repository.value.search(criteria);
```

## Dynamic Repository Creation

The main advantage of `useRepository` is that it automatically recreates the repository when its inputs change:

1. If the entity name changes, a new repository for the different entity type is created
2. If the repository factory changes, a new repository using the different factory is created

This reactivity is implemented using Vue's computed properties, ensuring that the repository is only recreated when necessary.

#### Parameters

| Name                | Required | Description                                                     |
|:--------------------|:---------|:----------------------------------------------------------------|
| `entityNameRef`     | true     | The name of the entity type as a ref or static value            |
| `repositoryFactory` | false    | Optional repository factory as a ref or static value            |

#### Return Value

A computed ref containing a repository that updates when its dependencies change. The repository provides the same methods as described in the `getRepository` documentation, but you need to access them through the `.value` property of the computed ref.

## Relationship with getRepository

Under the hood, `useRepository` calls `getRepository` whenever its dependencies change. This means:

* It uses the same repository factory resolution logic as `getRepository`
* It provides the same repository interface and functionality
* It adds reactivity, automatically updating when inputs change

```ts
// Example implementation (simplified)
import { computed } from 'vue';
import { getRepository } from './getRepository';

export function useRepository(entityNameRef, factoryRef) {
  return computed(() => {
    const entityName = unref(entityNameRef);
    const factory = unref(factoryRef);
    
    return getRepository(entityName, factory);
  });
}
```

This pattern follows Vue's composition API conventions, where composables prefixed with "use" typically provide reactive wrappers around non-reactive functionality.

---

---

## useSharedState
**Source:** [resources/admin-extension-sdk/api-reference/composables/useSharedState.md](https://developer.shopware.com/resources/admin-extension-sdk/api-reference/composables/useSharedState.md)  
# useSharedState

The `composables.useSharedState` function allows you to create globally accessible state in your app. The state defined within this composable has a unique key, and any other part of the app that uses the same composable with the same key will access the same data.

The shared state is reactive, meaning that when you update the data in one place, all other places that access the same shared state will be automatically updated as well. This feature is particularly useful when you need to pass data to different locations, such as modals or locations outside the current iFrame. The shared state is also saved locally to the user's machine using IndexedDB, ensuring persistence even after refreshes or when the user is using multiple tabs.

The value stored within the shared state can be any data type that can be serialized to JSON. Additionally, we have added support for Entities and EntityCollections.

![useShardState demo](../assets/useSharedState-demo.gif)

#### Usage:

```ts
// Inside a Vue component setup
import { composables } from '@shopware-ag/meteor-admin-sdk';
const { useSharedState } = composables;

const mySharedStateValue = useSharedState('myUniqueKeyForTheSharedState', 'myInitialDataValue');
```

#### Parameters

| Name           | Required | Description                                                               |
| :------------- | :------- | :------------------------------------------------------------------------ |
| `key`          | true     | The unique key used to share the state across different places            |
| `initial data` | true     | The initial data value used when no data exists in the local shared state |

---

---

## Context
**Source:** [resources/admin-extension-sdk/api-reference/context.md](https://developer.shopware.com/resources/admin-extension-sdk/api-reference/context.md)  
# Context

## Language

### Get current language

#### Usage:

```ts
const language = await sw.context.getLanguage();
```

#### Parameters

No parameters needed.

#### Return value:

```ts
Promise<{
  languageId: string,
  systemLanguageId: string
}>
```

#### Example value:

```ts
{
  languageId: '2fbb5fe2e29a4d70aa5854ce7ce3e20b',
  systemLanguageId: '2fbb5fe2e29a4d70aa5854ce7ce3e20b'
}
```

### Subscribe on language changes

#### Usage:

```ts
sw.context.subscribeLanguage(({ languageId, systemLanguageId }) => {
  // do something with the callback data
});
```

#### Parameters

| Name | Description |
| :------ | :------ |
| `callbackMethod` | Called every-time the language changes |

#### Callback value:

```ts
{
  languageId: string,
  systemLanguageId: string
}
```

#### Example callback value:

```ts
{
  languageId: '2fbb5fe2e29a4d70aa5854ce7ce3e20b',
  systemLanguageId: '2fbb5fe2e29a4d70aa5854ce7ce3e20b'
}
```

## Environment

### Get current environment

#### Usage:

```ts
const environment = await sw.context.getEnvironment();
```

#### Parameters

No parameters needed.

#### Return value:

```ts
Promise<'development' | 'production' | 'testing'>
```

#### Example value:

```ts
'development'
```

## Locale

### Get current locale

#### Usage:

```ts
const locale = await sw.context.getLocale();
```

#### Parameters

No parameters needed.

#### Return value:

```ts
Promise<{
  locale: string,
  fallbackLocale: string
}>
```

#### Example value:

```ts
{
  locale: 'de-DE',
  fallbackLocale: 'en-GB'
}
```

### Subscribe on locale changes

#### Usage:

```ts
sw.context.subscribeLocale(({ locale, fallbackLocale }) => {
  // do something with the callback data
});
```

#### Parameters

| Name | Description |
| :------ | :------ |
| `callbackMethod` | Called every-time the locale changes |

#### Callback value:

```ts
{
  locale: string,
  fallbackLocale: string
}
```

#### Example callback value:

```ts
{
  locale: 'de-DE',
  fallbackLocale: 'en-GB'
}
```

## Currency

### Get current currency

#### Usage:

```ts
const currency = await sw.context.getCurrency();
```

#### Parameters

No parameters needed.

#### Return value:

```ts
Promise<{
  systemCurrencyId: string,
  systemCurrencyISOCode: string
}>
```

#### Example value:

```ts
{
  systemCurrencyId: 'b7d2554b0ce847cd82f3ac9bd1c0dfca',
  systemCurrencyISOCode: 'EUR'
}
```

## Shopware version

### Get current Shopware version

#### Usage:

```ts
const shopwareVersion = await sw.context.getShopwareVersion();
```

#### Parameters

No parameters needed.

#### Return value:

```ts
string
```

#### Example value:

```ts
'6.4.0.0'
```

### Compare current Shopware version with a given version

In many cases you have to make sure that the shop you are communicating with has a certain Shopware version. For this purpose the Meteor Admin SDK provides the `context.compareIsShopwareVersion` function.

The function always treats the current Shopware version of a shop as the left hand operator of the comparison. That means a call like `context.compareIsShopwareVersion('>=', '7.0.0')` can be read as "*Compare: is Shopware version equal or greater than 7.0.0*"

#### Usage:

```ts
const isRightVersion = await sw.context.compareShopwareVersion('>=', '7.0.0')
```

#### Parameters

| Name         | Description                                                                                                       |
|:-------------|:------------------------------------------------------------------------------------------------------------------|
| `comparator` | The operator to compare. Possible values: `'='` `'!='` `'>'` `'<'` `'<='` `'>='`|
| `version`    | The string with the version to compare

The function supports both, Shopware's four-digit version number and semver versions. The following calls are equivalent:

```ts
await sw.context.compareShopwareVersion('>=', '6.6.4.0');

await sw.context.compareShopwareVersion('>=', '6.4.0');
```

#### Return value:

```ts
boolean
```

#### Example value:

```ts
true
```

## App information

### Get app information

> The privileges property will be available with Shopware v6.7.1.0 and higher

#### Usage:

```ts
const { name, version, type, privileges } = await sw.context.getAppInformation();
```

#### Parameters

No parameters needed.

#### Return value:

```ts
Promise<{ name: string ; version: string ; type: 'app' | 'plugin', privileges: privileges }>
```

#### Example value:

```ts
{
  name: 'my-extension',
  version: '1.2.3',
  type: 'app'
  privileges: {
    read: [ 'product', 'customer' ],
    write: [ 'product' ],
    additional: [ 'system.cache_clear' ]
  }
}
```

## User information

### Get user information

:::caution
Do not use this feature yet. It is not implemented in a Shopware release yet.
:::

#### Usage:

```ts
const userInformation = await sw.context.getUserInformation();
```

#### Parameters

No parameters needed.

#### Return value:

```ts
Promise<{
  aclRoles: Array<{
    name: string,
    type: string,
    id: string,
    privileges: Array<string>,
  }>,
  active: boolean,
  admin: boolean,
  avatarId: string,
  email: string,
  firstName: string,
  id: string,
  lastName: string,
  localeId: string,
  title: string,
  type: string,
  username: string,
}>
```

#### Example value:

```ts
{
    "aclRoles": [],
    "active": true,
    "admin": true,
    "avatarId": "",
    "email": "info@shopware.com",
    "firstName": "",
    "id": "e2a77f4c718d407591b4826222aa3546",
    "lastName": "admin",
    "localeId": "35bbb8c4305c47ec88b13ab30c0c5c5a",
    "title": "",
    "type": "user",
    "username": "admin"
}
```

## User Timezone

### Get user timezone

:::caution
This feature will be available with Shopware ^6.6.2.0
:::

This feature allows you to get the timezone of the user.

#### Usage:

```ts
const userTimezone = await sw.context.getUserTimezone();
```

#### Parameters

No parameters needed.

#### Return value:

```ts
Promise<string>
```

This function returns a Promise that resolves to a string representing the user's timezone.

## Module information

### Get module information

Get information about all registered modules. These modules are created by adding new menu items, setting items, etc.

The ID can be used to change the current route to the module.

#### Usage:

```ts
const { modules } = await sw.context.getModuleInformation();

sw.window.routerPush({
  name: 'sw.extension.sdk.index',
  params: {
    id: modules[0].id // get the ID of the wanted module
  }
})
```

#### Parameters

No parameters needed.

#### Return value:

```ts
Promise<{
  modules: Array<{
    displaySearchBar: boolean,
    heading: string,
    id: string,
    locationId: string
  }>
}>
```

#### Example value:

```ts
{
  modules: [
    {
      displaySearchBar: true,
      heading: 'My module',
      id: 'sd5aasfsdfas',
      locationId: 'my-location-id'
    }
  ]
}
```

## ShopId

### Get the shopId

> Available since Shopware v6.7.1.0

Get the shop's shop-id used by Shopware's app system

#### Usage

```ts
const shopId = await sw.context.getShopId();
```

#### Parameters

no parameters needed

#### Return value:

```ts
Promise<string>
```

## Check app's privileges

> Available since Shopware 6.7.1.0

This lets you check if a specific privilege is granted for your app

#### Usage

```ts
const isAllowed: boolean = await sw.context.can('product:read');
```

#### Parameters

No parameters needed.

#### Return value

```ts
boolean
```

---

---

## resources/admin-extension-sdk/api-reference/data.md
**Source:** [resources/admin-extension-sdk/api-reference/data.md](https://developer.shopware.com/resources/admin-extension-sdk/api-reference/data.md)  
---

---

## Get
**Source:** [resources/admin-extension-sdk/api-reference/data/get.md](https://developer.shopware.com/resources/admin-extension-sdk/api-reference/data/get.md)  
# Get

With `data.get` you can receive datasets from the Shopware administration.
More information on how to find the unique identifiers can be found in [this guide](../../internals/datahandling.md).

Compared to data.subscribe, data.get only gives you the current state of the data. If the data is not available yet,
such as when opening a page, you won't receive any data. In these cases, it's better to subscribe to data changes instead.

#### Usage:

```ts
data.get({
    id: 'sw-product-detail__product',
    selectors: ['name', 'manufacturer.name'],
}).then((product) => {
    console.log(product);
});
```

#### Output:

```json
{
  "name": "Ergonomic Copper Mr. Frenzy",
  "manufacturer": {
    "name": "Turcotte, Rempel and Padberg"
  }
}
```

#### Parameters

| Name      | Required | Description                                                                                                          |
| :-------- | :------- |:---------------------------------------------------------------------------------------------------------------------|
| `options` | true     | Containing the unique `id` and optional `selectors`. Read more about selectors [here](../../concepts/selectors.md) |

---

---

## Repository
**Source:** [resources/admin-extension-sdk/api-reference/data/repository.md](https://developer.shopware.com/resources/admin-extension-sdk/api-reference/data/repository.md)  
# Repository

The data handling of the SDK allows you to fetch and write nearly everything in the database. The behavior matches the data handling in the main administration. The only difference is the implementation details because the data handling don't request the server directly. It communicates with the admin which handles the requests, changesets, saving and more.

The data handling implements the repository pattern. You can create a repository for an entity simply like this:

```ts
sw.data.repository('your_entity_name')
```

With this repository you can search for data, save it, delete it, create it or check for changes.

### Permissions

For every action on the repository, your app will need the matching permissions.
Permissions are set in the app manifest file and are grouped by action.
For actions you can choose between `create`, `read`, `update` and `delete`.
Remember everytime you adjust the permissions in your manifest you need to increase the app version and update it.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<manifest
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:noNamespaceSchemaLocation="https://raw.githubusercontent.com/shopware/platform/trunk/src/Core/Framework/App/Manifest/Schema/manifest-1.0.xsd">

    <!-- ... -->

    <permissions>
        <create>product</create>
        <read>product</read>
        <update>product</update>
        <delete>product</delete>
    </permissions>
</manifest>

```

### Criteria

For requesting data you need to create a Criteria class which contains all information for the request:

```ts
const criteria = new sw.data.Classes.Criteria();

criteria.setPage(1);
criteria.setLimit(10);
criteria.setTerm('foo');
criteria.setIds(['some-id', 'some-id']); // Allows to provide a list of ids which are used as a filter

/**
    * Configures the total value of a search result.
    * 0 - no total count will be selected. Should be used if no pagination required (fastest)
    * 1 - exact total count will be selected. Should be used if an exact pagination is required (slow)
    * 2 - fetches limit * 5 + 1. Should be used if pagination can work with "next page exists" (fast)
*/
criteria.setTotalCountMode(2);

criteria.addFilter(
    Criteria.equals('product.active', true)
);

criteria.addSorting(
    Criteria.sort('product.name', 'DESC')
);

criteria.addAggregation(
    Criteria.avg('average_price', 'product.price')
);

criteria.getAssociation('categories')
    .addSorting(Criteria.sort('category.name', 'ASC'));
```

### Search

Sends a search request for the repository entity.

#### Usage:

```ts
const exampleRepository = sw.data.repository('your_entity');

const yourEntities = await exampleRepository.search(yourCriteria);
```

#### Parameters:

| Name       | Required | Default | Description                                    |
| :--------- | :------- | :------ | :--------------------------------------------- |
| `criteria` | true     |         | Your criteria object                           |
| `context`  | false    | {}      | Change the [request context](#request-context) |

#### Return value:

The return value is a EntityCollection which contains all entities matching the criteria.

### Get

Short hand to fetch a single entity from the server

#### Usage:

```ts
const exampleRepository = sw.data.repository('your_entity');

const yourEntity = await exampleRepository.get('theEntityId');
```

#### Parameters:

| Name       | Required | Default | Description                                    |
| :--------- | :------- | :------ | :--------------------------------------------- |
| `id`       | true     |         | The id of the entity                           |
| `context`  | false    | {}      | Change the [request context](#request-context) |
| `criteria` | true     |         | Your criteria object                           |

#### Return value:

The return value is the entity result when a matching entity was found.

### Save

Detects all entity changes and send the changes to the server.
If the entity is marked as new, the repository will send a POST create. Updates will be send as PATCH request.
Deleted associations will be send as additional request

#### Usage:

```ts
const exampleRepository = sw.data.repository('your_entity');

await exampleRepository.save(yourEntityObject);
```

#### Parameters:

| Name      | Required | Default | Description                                    |
| :-------- | :------- | :------ | :--------------------------------------------- |
| `entity`  | true     |         | The entity object                              |
| `context` | false    | {}      | Change the [request context](#request-context) |

#### Return value:

This method does not have a return value. It just returns a Promise which is resolved when it was saved successfully.

### Clone

Clones an existing entity

#### Usage:

```ts
const exampleRepository = sw.data.repository('your_entity');

const clonedEntityId = await exampleRepository.clone('theEntityIdToClone');
```

#### Parameters:

| Name       | Required | Default | Description                                    |
| :--------- | :------- | :------ | :--------------------------------------------- |
| `entityId` | true     |         | The entity id which should be cloned           |
| `context`  | false    | {}      | Change the [request context](#request-context) |

#### Return value:

This method returns the id of the cloned entity.

### Has changes

Detects if the entity or the relations has remaining changes which are not synchronized with the server

#### Usage:

```ts
const exampleRepository = sw.data.repository('your_entity');

const hasChanges = await exampleRepository.hasChanges(yourEntityObject);
```

#### Parameters:

| Name     | Required | Default | Description       |
| :------- | :------- | :------ | :---------------- |
| `entity` | true     |         | The entity object |

#### Return value:

This method returns a boolean value. If the entity has changes then it returns `true`. Otherwise it returns `false`.

### Save all

Detects changes of all provided entities and send the changes to the server

#### Usage:

```ts
const exampleRepository = sw.data.repository('your_entity');

await exampleRepository.saveAll(yourEntityCollection);
```

#### Parameters:

| Name       | Required | Default | Description                                    |
| :--------- | :------- | :------ | :--------------------------------------------- |
| `entities` | true     |         | Your entity collection which should be saved   |
| `context`  | false    | {}      | Change the [request context](#request-context) |

#### Return value:

This method does not have a return value. It just returns a Promise which is resolved when it was saved successfully.

### Delete

Sends a delete request for the provided id.

#### Usage:

```ts
const exampleRepository = sw.data.repository('your_entity');

await exampleRepository.delete('yourEntityId');
```

#### Parameters:

| Name       | Required | Default | Description                                    |
| :--------- | :------- | :------ | :--------------------------------------------- |
| `entityId` | true     |         | The id of the entity which should be deleted   |
| `context`  | false    | {}      | Change the [request context](#request-context) |

#### Return value:

This method does not have a return value. It just returns a Promise which is resolved when it was deleted successfully.

### Create

Creates a new entity for the local schema. To Many association are initialed with a collection with the corresponding remote api route. This entity is not saved to the database yet.

#### Usage:

```ts
const exampleRepository = sw.data.repository('your_entity');

const yourNewEntity = await exampleRepository.create();
```

#### Parameters:

| Name       | Required | Default | Description                                    |
| :--------- | :------- | :------ | :--------------------------------------------- |
| `context`  | false    | {}      | Change the [request context](#request-context) |
| `id` | false     |         | You can provide a id of the new entity if wanted   |

#### Return value:

This method returns the newly created entity.

### Request Context

You can optionally change the context of the request. It will be merged together with the base API context.

```ts
const exampleContext = {
    // Load also inherited data (example from parent product in variant)
    inheritance: true,
    // Change the language context of the entity to change data in different languages
    languageId: 'theLanguageId',
    // If you are working with versioned entities you can change the current live version id
    liveVersionId: 'yourLiveVersionId'
}
```

---

---

## Subscribe
**Source:** [resources/admin-extension-sdk/api-reference/data/subscribe.md](https://developer.shopware.com/resources/admin-extension-sdk/api-reference/data/subscribe.md)  
# Subscribe

With `data.subscribe` you can subscribe to dataset changes. The callback will be called every time, the dataset with the matching id is changed.
More information on how to find the unique identifiers can be found in [this guide](../../internals/datahandling.md).

#### Usage:

```ts
data.subscribe(
    'sw-product-detail__product',
    ({id, data}) => {
        console.log(data);
    },
    {
        selectors: ['name', 'manufacturer.name']
    },
);
```

#### Output:

```json
{
  "name": "Ergonomic Copper Mr. Frenzy",
  "manufacturer": {
    "name": "Turcotte, Rempel and Padberg"
  }
}
```

#### Parameters

| Name        | Required | Description                                                                                           |
| :---------- | :------- |:------------------------------------------------------------------------------------------------------|
| `id`        | true     | The unique id of the dataset you want to receive                                                      |
| `callback`  | true     | A callback function which will be called every time the Shopware Administration publishes the dataset |
| `options` | false    | Allows to specify `selectors`. Read more about selectors [here](../../concepts/selectors.md)                                       |

---

---

## Update
**Source:** [resources/admin-extension-sdk/api-reference/data/update.md](https://developer.shopware.com/resources/admin-extension-sdk/api-reference/data/update.md)  
# Update

With `data.update` you can update datasets from the Shopware administration.
More information on how to find the unique identifiers can be found in [this guide](../../internals/datahandling.md).

#### Usage:

```ts
data.update({
    id: 'sw-product-detail__product',
    data: {
        name: 'My updated name',
    },
}).then(() => {
    console.log('success');
});
```

#### Parameters

| Name      | Required | Description                                        |
| :-------- | :------- | :------------------------------------------------- |
| `options` | true     | An object containing the id and the data to update |

---

---

## resources/admin-extension-sdk/api-reference/in-app-purchases.md
**Source:** [resources/admin-extension-sdk/api-reference/in-app-purchases.md](https://developer.shopware.com/resources/admin-extension-sdk/api-reference/in-app-purchases.md)  
---

---

## In-App Purchase Flow
**Source:** [resources/admin-extension-sdk/api-reference/in-app-purchases/in-app-purchases.md](https://developer.shopware.com/resources/admin-extension-sdk/api-reference/in-app-purchases/in-app-purchases.md)  
# In-App Purchase Flow

> Available since Shopware v6.6.9.0

In-App purchases allow you to create different functionality based on purchases the user has made in your app. This guide will show you how to start the in-app purchase flow.

### Opening modal with details of feature

To open a modal with the details of the feature you want to purchase, you can use the following code:

```ts
sw.iap.purchase({
    identifier: 'your-in-app-purchase-id',
});
```

This will create a modal in admin which takes the user through the checkout flow in which the app will be purchased or subscribed to.

Once the purchase has been completed, the amount will be added to the bill of the merchant, and the feature will be unlocked.

---

---

## Location
**Source:** [resources/admin-extension-sdk/api-reference/location.md](https://developer.shopware.com/resources/admin-extension-sdk/api-reference/location.md)  
# Location

## Prerequisites

We recommend you read the [concept](../concepts/locations.md) of locations first.

## Location checks

### Check the current location id

Check if the current location matches the given location Id.

#### Usage:

```ts
if (sw.location.is('my-location-id')) {
    // Render view for location
}
```

#### Parameters:

| Name         | Required | Default | Description              |
| :----------- | :------- | :------ | :----------------------- |
| `locationId` | true     |         | The location Id to check |

#### Return value:

Returns a boolean. It is `true` if the location Id matches the current location.

### Get the current location id

Get the name of the current location ID

#### Usage:

```ts
const currentLocation = sw.location.get()
```

#### Return value:

Returns a string with the name of the current location.

### Check if current location is inside iFrame

Useful for hybrid extensions which are using plugin and Extension SDK functionalities together (Shopware 6.6 and lower). You can use this
check to separate code which should be executed inside the Extension SDK context and the plugin context.

#### Usage:

```ts
if (location.isIframe()) {
    // Execute the code which uses the meteor-admin-sdk context
    import('./extension-code');
} else {
    // Execute the plugin code
    import('./plugin-code');
}
```

## iFrame Heights

#### Parameters:

No parameters needed.

#### Return value:

Returns a boolean. If it is executed inside a iFrame it returns `true`.

### Update the height of the location iFrame

You can update the height of the iFrame with this method.

#### Usage:

```ts
sw.location.updateHeight(750);
```

#### Parameters:

| Name            | Required | Default        | Description                                                                                                    |
| :-------------- | :------- | :------------- | :------------------------------------------------------------------------------------------------------------- |
| `iFrame height` | false    | Auto generated | The height of the iFrame. If no value is provided it will be automatically calculated from the current height. |

#### Return value:

This method does not have a return value.

### Start auto resizing of the iFrame height

This methods starts the auto resizer of the iFrame height.

![Auto resizing example](../concepts/assets/auto-resizer.gif)

#### Usage:

```ts
sw.location.startAutoResizer();
```

#### Parameters:

No parameters needed.

#### Return value:

This method does not have a return value.

### Stop auto resizing of the iFrame height

This methods stops the auto resizer of the iFrame height.

#### Usage:

```ts
sw.location.stopAutoResizer();
```

#### Parameters:

No parameters needed.

#### Return value:

This method does not have a return value.

## URL changes inside your app

:::caution
Do not use this feature yet. It is not implemented in a Shopware release yet.
:::

Important: You can track and emit your URL changes only inside your own main module or settings page.

### Update URL

Send the current URL of your iFrame to the administration. When the user reloads the whole page your iFrame will get the
last page you sent to the administration.

#### Usage:

```ts
const currentUrl = window.location.href;

sw.location.updateUrl(new URL(currentUrl))
```

#### Parameters:

| Name            | Required | Default | Description                           |
| :-------------- | :------- | :------ | :------------------------------------ |
| First parameter | true     |         | An URL object which contains your URL |

### Start automatic URL updates

To avoid manually sending URL changes you can use this helper methods. It sends automatically changes in your URL to the
administration.

#### Usage:

```ts
sw.location.startAutoUrlUpdater();
```

### Stop automatic URL updates

If you had started an automatic URL updater before then you can stop it by calling this method.

#### Usage:

```ts
sw.location.stopAutoUrlUpdater();
```

---

---

## Notification
**Source:** [resources/admin-extension-sdk/api-reference/notification.md](https://developer.shopware.com/resources/admin-extension-sdk/api-reference/notification.md)  
# Notification

### Dispatch a notification

![notification example](./assets/notification-example.jpg)

#### Usage:

```ts
function alertYes() {
  alert('Yes');
}

sw.notification.dispatch({
    title: 'Your title',
    message: 'Your message',
    variant: 'success',
    appearance: 'notification',
    growl: true,
    actions: [
        {
            label: 'Yes',
            method: alertYes
        },
        {
            label: 'No',
            method: () => {
                alert('No')
            }
        },
        {
            label: 'Cancel',
            route: 'https://www.shopware.com',
            disabled: false,
        }
    ]
})
```

#### Parameters:

| Name         | Required | Default        | Description                                                                                                                                                                                                     |
|:-------------|:---------|:---------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `title`      | true     |                | Defines a notification's **title**.                                                                                                                                                                             |
| `message`    | true     |                | Defines a notification's main expression or message to the user.                                                                                                                                                |
| `variant`    | false    | `info`         | Defines the notification type. Available `variant` types are `success`, `info`, `warning` and `error`.                                                                                                          |
| `appearance` | false    | `notification` | Changes the style of a notification. Use `system` for technical notifications thrown by the application. Otherwise keep the default value `notification`.                                                       |
| `growl`      | false    | `true`         | Displays a notification that is overlaying any module. Use `false` to display the notification in the notification center (bell symbol) only.                                                                   |
| `actions`    | false    | `[]`           | Adds clickable buttons to the notification. Each button with a `label` can trigger a `method` or open a `route` (internal route or external link). Buttons can also be disabled using the attribute `disabled`. |

#### Return value:

Returns a promise without data.

---

---

## Toast
**Source:** [resources/admin-extension-sdk/api-reference/toast.md](https://developer.shopware.com/resources/admin-extension-sdk/api-reference/toast.md)  
# Toast

## Availability

This feature will be available with Shopware 6.6.2.0.

### Dispatch a toast

![toast example](./assets/toast-example.png)

#### Usage:

```ts
function alertYes() {
  alert('Yes');
}

sw.toast.dispatch({
    msg: 'Your message',
    dismissible: true,
    type: 'positive',
    action: {
        label: 'action',
        callback: alertYes
    },
})
```

#### Parameters:

| Name          | Required | Default | Description                                                                                                    |
|:--------------|:---------|:--------|:---------------------------------------------------------------------------------------------------------------|
| `msg`         | true     |         | Defines a toast's main expression or message to the user.                                                      |
| `type`        | true     |         | Defines the toast type. Available `types` are `positive`, `informal` and `critical`.                           |
| `icon      `  | false    | None    | A icon that should be displayed in front of your message.                                                      |
| `dismissible` | false    | `false` | Specifies if the toast can be manually dismmissed.                                                             |
| `action`      | false    | None    | Adds a clickable button to the toast. The button receives a label and a callback wichs is called once clicked. |

#### Return value:

Returns a promise without data.

---

---

## resources/admin-extension-sdk/api-reference/ui.md
**Source:** [resources/admin-extension-sdk/api-reference/ui.md](https://developer.shopware.com/resources/admin-extension-sdk/api-reference/ui.md)  
---

---

## Action button
**Source:** [resources/admin-extension-sdk/api-reference/ui/actionButton.md](https://developer.shopware.com/resources/admin-extension-sdk/api-reference/ui/actionButton.md)  
# Action button

#### Usage:

```ts
import { location, ui } from '@shopware-ag/meteor-admin-sdk';

if (location.is(sw.location.MAIN_HIDDEN)) {
    ui.actionButton.add({
        action: 'your-app_customer-detail-action',
        entity: 'customer',
        view: 'detail',
        label: 'Test action',
        callback: (entity, entityIds) => {
            // TODO: do something
        },
    });
}
```

#### Parameters

| Name                 | Required | Description                                                                                                |
| :------------------- | :------- | :--------------------------------------------------------------------------------------------------------- |
| `action`             | true     | A unique name of your action                                                                               |
| `entity`             | true     | The entity this action is for possible values: `product`, `order`, `category`, `promotion`, `customer` or `media`. Value `media` is available in Shopware version 6.7.1   |
| `view`               | true     | Determines if the action button appears on the listing or detail page, possible values: `detail`,`list` or item. View `item` is only used for entity `media` and in version 6.7.1 |
| `label`              | true     | The label of your action button                                                                            |
| `meteorIcon`         | false    | Meteor icon before label, will be available in Shopware version 6.7.4.0 . Check icon name on https://developer.shopware.com/resources/meteor-icon-kit/ |
| `fileTypes`          | false    | Media file types you want the action button to be displayed for. Will be available in Shopware version 6.7.6.                                          |
| `callback`           | true     | The callback function where you receive the entity and the entityIds for further processing                |

### Calling app actions

As an app developer you may want to receive the information of the callback function server side.
The following example will render the same action button as the above example but once it gets clicked you will receive a POST request to your app server.
**This will only work for apps. Plugin developers need to use a api client directly in there callback.**.

```ts
import { location, ui } from '@shopware-ag/meteor-admin-sdk';

if (location.is(sw.location.MAIN_HIDDEN)) {
    ui.actionButton.add({
        action: 'your-app_customer-detail-action',
        entity: 'customer',
        view: 'detail',
        label: 'Test action',
        callback: (entity /* "customer" */, entityIds /* ["..."] */) => {
            app.webhook.actionExecute({
                url: 'http://your-app.com/customer-detail-action',
                entityIds,
                entity,
            })
        },
    });
}
```

#### Example

* Add action button in customer detail page

![Action button example](./assets/add-action-button-example.png)

```ts
ui.actionButton.add({
    action: 'your-app_customer-detail-action',
    entity: 'customer',
    view: 'detail',
    meteorIcon: 'regular-analytics',
    label: 'Test action',
    callback: (entity /* "customer" */, entityIds /* ["..."] */) => {
        app.webhook.actionExecute({
            url: 'http://your-app.com/customer-detail-action',
            entityIds,
            entity,
        })
    },
});
```

* Add action button in media item

![Action button media example](./assets/add-action-button-media-example.png)

```ts
ui.actionButton.add({
    action: 'test-media-button',
    entity: 'media',
    view: 'item',
    meteorIcon: 'regular-tools-alt',
    label: 'Open in Image editor',
    callback: (entity /* "media" */, entityIds /* ["..."] */) => {
        // TODO: Navigate to image editor app
    },
});
```

---

---

## Component Section
**Source:** [resources/admin-extension-sdk/api-reference/ui/component-section.md](https://developer.shopware.com/resources/admin-extension-sdk/api-reference/ui/component-section.md)  
# Component Section

## Add

Add a new component to a component section.

### General usage

#### Usage:

```ts
import { ui } from '@shopware-ag/meteor-admin-sdk';

ui.componentSection.add({
    component: 'the-component', // Choose the component which you want to render at the component section
    positionId: 'the-position-id-of-the-component-section', // Select the positionId where you want to render the component
    props: {
        ... // The properties are depending on the component
    }
})
```

#### Parameters

| Name        | Required | Default | Description                                    |
| :---------- | :------- | :------ | :--------------------------------------------- |
| `component` | true     |         | Choose the component which you want to render. |

#### Return value:

This method does not have a return value.

## Available components

### Card

#### Properties:

| Name         | Required | Default | Description                        |
|:-------------|:---------|:--------|:-----------------------------------|
| `title`      | false    |         | The main title of the card         |
| `subtitle`   | false    |         | The subtitle of the card           |
| `locationId` | true     |         | The locationId for the custom view |
| `tabs`       | false    |         | Render different content with tabs |

#### Usage:

```js
import { ui } from '@shopware-ag/meteor-admin-sdk';

ui.componentSection.add({
    component: 'card',
    positionId: 'sw-product-properties__before',
    props: {
        title: 'Hello from plugin',
        subtitle: 'I am before the properties card',
        locationId: 'my-awesome-app-card-before'
    }
})
```

#### Example

![Card component example](./assets/example-card.png)

#### With tabs:

```js
import { ui } from '@shopware-ag/meteor-admin-sdk';

ui.componentSection.add({
    component: 'card',
    positionId: 'sw-product-properties__before',
    props: {
        title: 'Hello from plugin',
        subtitle: 'I am before the properties card',
        locationId: 'my-awesome-app-card-before',
        // Render tabs and custom tab content with the provided location id
        tabs: [
            {
                name: 'example-tab-1',
                label: 'First tab',
                locationId: 'example-tab-1'
            },
            {
                name: 'example-tab',
                label: 'Second tab',
                locationId: 'example-tab-2'
            }
        ],
    }
})
```

#### Example

![Card component with tabs example](./assets/example-card-with-tabs.png)

---

---

## Main module
**Source:** [resources/admin-extension-sdk/api-reference/ui/mainModule.md](https://developer.shopware.com/resources/admin-extension-sdk/api-reference/ui/mainModule.md)  
# Main module

### Add main module

Add a main module to your extension. The content of the main module is determined by your `locationId`.
A specific view or a set of actions can be triggered based on the `locationId`.

#### Usage:

```ts
ui.mainModule.addMainModule({
    heading: 'My App',
    locationId: 'main-location-id',
});
```

#### Parameters

| Name                    | Required | Default | Description                            |
| :---------------------- | :------- | :------ | :------------------------------------- |
| `heading`               | true     |         | The heading displayed in your module   |
| `locationId`            | true     |         | The Id for the content of the module   |
| `displaySearchBar`      | false    | true    | Toggles the sw-page search bar on/off  |
| `displayLanguageSwitch` | false    | false   | Toggles sw-page language switch on/off |

#### Example

![Main module example](./assets/add-main-module-example.png)

```ts
import { location, ui } from '@shopware-ag/meteor-admin-sdk';

// General commands
if (location.is(location.MAIN_HIDDEN)) {
    // Add the main module
    ui.mainModule.addMainModule({
        heading: 'My App',
        locationId: 'main-location-id',
    });

  // If you want to provide some buttons for the smart bar of your main module
  ui.mainModule.addSmartbarButton({
      locationId: 'main-location-id', // locationId of your main module
      buttonId: 'test-button', // The button id
      label: 'Click me', // The button label
      variant: 'primary', // The button variant
      onClickCallback: () => {}
  });

    ui.mainModule.hideSmartBar({
        locationId: 'main-location-id',
    });
}

// Render your custom view
if (location.is('main-location-id')) {
    document.body.innerHTML = '<h1 style="text-align: center">Hello from your main module</h1>';
}
```

### Add smart bar button to main module

Add a button to the smart bar of your main module. The button can be used to trigger actions, e.g. saving, cancel, etc. The location ID needs to be defined and have the same value as the `locationId` of the main module.

#### Usage:

```ts
ui.mainModule.addSmartbarButton({
    locationId: 'main-location-id', // locationId of your main module
    buttonId: 'test-button', // The button id
    label: 'Click me', // The button label
    variant: 'primary', // The button variant
    onClickCallback: () => {}
});
```

#### Parameters

| Name              | Required | Default   | Description                                                                                                         |
| :---------------- | :------- | :-------- | :------------------------------------------------------------------------------------------------------------------ |
| `locationId`      | true     |           | The locationId of the module you want to display the smart bar button                                               |
| `buttonId`        | true     |           | The id of the button                                                                                                |
| `label`           | true     |           | The label of the button                                                                                             |
| `variant`         | false    | `primary` | Set the variant of the button. Possible values: `primary`, `ghost`, `danger`, `ghost-danger`, `contrast`, `context` |
| `onClickCallback` | true     |           | Callback function which will be called once the button is clicked                                                   |
| `disabled`        | false    | false     | Toggle disabled state of the button                                                                                 |

### Hide smart bar

Turn the smart bar off as needed.

#### Usage:

```ts
ui.mainModule.hideSmartBar({
    locationId: 'main-location-id',
});
```

#### Parameters

| Name         | Required | Default   | Description                                                                                                                                    | Available at Shopware |
| :----------- | :------- | :-------- | :--------------------------------------------------------------------------------------------------------------------------------------------- | :---------------------|
| `locationId` | true     |           | The locationId of the module you want to hide the smart bar                                                                                    | v6.6.7.0               |

---

---

## Media modal
**Source:** [resources/admin-extension-sdk/api-reference/ui/mediaModal.md](https://developer.shopware.com/resources/admin-extension-sdk/api-reference/ui/mediaModal.md)  
# Media modal

This method allows an app to interact with the Administration's media modal, which includes the Media modal and the Save media modal.

Functionality of each modal:

* The Media modal is used for selecting existing media from the media library or uploading new media. This functionality has been available since version 6.7.1.

* The Save media modal is used to choose a specific location to save the media, and this feature will be implemented in version 6.7.5.

## Media modal

### Open modal

Open media modal in the current view.

#### Usage:

```ts
ui.mediaModal.open({
  initialFolderId: "initialFolderId",
  allowMultiSelect: false,
  fileAccept: "image/png",
  selectors: ["fileName", "id", "url"],
  callback: ({ fileName, id, url }) => {},
});
```

#### Parameters

All parameters are similar to `sw-media-modal-v2` component's props

| Name               | Required | Default                   | Description                                                                          |
| :----------------- | :------- | :------------------------ | :----------------------------------------------------------------------------------- |
| `initialFolderId`  | false    | null                      | Initial folder id where the media modal will open                                    |
| `entityContext`    | false    | null                      | The entity name that upload image will be stored in that entity folder in Upload tab |
| `allowMultiSelect` | false    | true                      | Define single or multiple selection                                                  |
| `defaultTab`       | false    | library                   | Defines which tab should be opened by default                                        |
| `fileAccept`       | false    | image/\*                  | Define the file types which are allowed to be uploaded in Upload tab                 |
| `selectors`        | false    | \['fileName', 'id', 'url'] | Selected properties which should be returned in callback function                    |
| `callback`         | true     |                           | Callback function which will be called once the media item is selected.              |

#### Example

![Menu item example](./assets/media-modal.png)

```ts
ui.mediaModal.open({
  initialFolderId: "productMediaFolderId",
  allowMultiSelect: false,
  selectors: ["fileName", "id", "url"],
  callback: ({ fileName, id, url }) => {},
});
```

## Save media modal

### Open save media modal

Open save media modal in the current view.

#### Usage:

```ts
ui.mediaModal.openSaveMedia({
  initialFolderId: "initialFolderId",
  initialFileName: "New Image",
  fileType: "png",
  callback: ({ fileName, folderId, mediaId }) => {},
});
```

#### Parameters

All parameters are similar to `sw-media-save-modal` component's props

| Name               | Required | Default                   | Description                                                                          |
| :----------------- | :------- | :------------------------ | :----------------------------------------------------------------------------------- |
| `initialFolderId`  | false    | null                      | Initial folder id where the media modal will open                                    |
| `initialFileName`  | false    | null                      | Initial file name of media to set as initial value of file name input                                    |
| `fileType`  | false    | null                      | File extension of media to display on file name input's suffix                                    |
| `callback`         | true     |                           | This callback function is triggered when the "Save media" button is clicked. It returns the updated file name and the folderId where the media is stored.              |

#### Example

![Menu item example](./assets/save-media-modal.png)

```ts
ui.mediaModal.openSaveMedia({
  initialFileName: "images",
  fileType: "png",
  callback: ({ fileName, folderId, mediaId }) => {},
});
```

---

---

## Menu
**Source:** [resources/admin-extension-sdk/api-reference/ui/menu.md](https://developer.shopware.com/resources/admin-extension-sdk/api-reference/ui/menu.md)  
# Menu

### Toggle menu

> Available since Shopware v6.6.2.0

The Admin SDK allows you to manipulate the Admin menu of your application. One of the features it provides is the ability to toggle the Admin menu. This is done using the `collapseMenu` and `expandMenu` methods.

#### Usage:

```ts
ui.menu.collapseMenu(); // To collapse the Admin menu;

ui.menu.expandMenu(); // To expand the Admin menu;
```

### Add menu item

Add a new menu item to the Shopware admin menu. The content of the menu item module is determined by your `locationId`.
A specific view or a set of actions can be triggered based on the `locationId`.

#### Usage:

```ts
ui.menu.addMenuItem({
    label: 'Test item',
    locationId: 'your-location-id',
    displaySearchBar: true,
    displaySmartBar: true,
    parent: 'sw-catalogue',
})
```

#### Parameters

| Name                 | Required | Default        | Description                                                   |
| :------------------- | :------- | :------------- | :------------------------------------------------------------ |
| `label`              | true     |                | The label of the tab bar item                                 |
| `locationId`         | true     |                | The id for the content of the menu item module                |
| `displaySearchBar`   | false    | true           | Toggles the sw-page search bar on/off                         |
| `displaySmartBar`    | false    | true           | Toggles the sw-page smart bar on/off                          |
| `parent`             | false    | 'sw-extension' | Determines under which main menu entry your item is displayed |
| `position`           | false    | 110            | Determines the position of your menu item                     |

#### Example

![Menu item example](./assets/add-menu-item-example.png)

```ts
import { location, ui } from '@shopware-ag/meteor-admin-sdk';

// General commands
if (location.is(sw.location.MAIN_HIDDEN)) {
    // Add the menu item to the catalogue module
    ui.menu.addMenuItem({
        label: 'Test item',
        displaySearchBar: true,
        displaySmartBar: true,
        locationId: 'your-location-id',
        parent: 'sw-catalogue',
    });
}

// Render your custom view
if (location.is('your-location-id')) {
    document.body.innerHTML = '<h1 style="text-align: center">Hello from your menu item</h1>';
}
```

---

---

## Modals
**Source:** [resources/admin-extension-sdk/api-reference/ui/modals.md](https://developer.shopware.com/resources/admin-extension-sdk/api-reference/ui/modals.md)  
# Modals

A modal can be displayed in front of all other elements. To return to the main content the user must engage
with the modal by completing an action or by closing it. It should be mainly opened when the user interacts with something.
We recommend that no modal gets opened without context. As an example, it would be bad practice if the user gets logged
in and directly see some modals (e.g. changelogs of extensions) which all need to be closed manually.

### Open modal

Open a new modal in the current view. The content of the modal is determined by your `locationId` or by using plain text with `textContent`.

#### Usage:

```ts
ui.modal.open({
    title: 'Your modal title',
    // Use locationId for rendering custom content inside modal
    locationId: 'your-location-id',
    // Use textContent when no locationId is needed
    textContent: 'Do you really want to dispatch a notification?',
    variant: 'large',
    showHeader: true,
    showFooter: false,
    closable: true,
    buttons: [
        {
            label: 'Dispatch notification',
            method: () => {
                notification.dispatch({
                    message: 'Hello from the modal',
                    title: 'Modal example'
                })
            }
        },
        {
            label: 'Close modal',
            variant: 'primary',
            method: () => {
                ui.modal.close({
                    locationId: 'your-location-id'
                })
            }
        }
    ],
})
```

#### Parameters

| Name          | Required | Default   | Description                                                                                    | Available at Shopware |
|:--------------|:---------|:----------|:-----------------------------------------------------------------------------------------------|:----------------------|
| `title`       | true     |           | The title of the modal                                                                         |                       |
| `locationId`  | false    |           | The id for the content of the modal. If not provided it will render the `textContent`          |                       |
| `textContent` | false    |           | The plain text content of the modal. Will only be rendered if no `locationId` is given         | v.6.7.1               |
| `variant`     | false    | 'default' | Determine the size of the modal. Possible values are 'default', 'small', 'large' and 'full'    |                       |
| `showHeader`  | false    | true      | Enable the header in the modal which contains the title                                        |                       |
| `showFooter`  | false    | true      | Enable the modal footer                                                                        | v6.5.8                |
| `closable`    | false    | true      | If this is set to `false` then the modal can only be closed programmatically                   |                       |
| `buttons`     | false    | \[]        | This array contains button configurations which will render buttons in the footer of the modal |                       |

#### Example

![Menu item example](./assets/modal-example.png)

```ts
ui.modal.open({
    title: 'Hello from the plugin',
    locationId: 'my-awesome-app-hello-world-modal',
    buttons: [
        {
            label: 'Dispatch notification',
            method: () => {
                notification.dispatch({
                    message: 'Hello from the modal',
                    title: 'Modal plugin'
                })
            }
        },
        {
            label: 'Close modal',
            variant: 'primary',
            method: () => {
                ui.modal.close({
                    locationId: 'my-awesome-app-hello-world-modal'
                })
            }
        }
    ]
})
```

### Update modal

> Available since Shopware 6.7.1.0

Updates an existing modal with the given `locationId`. This can be used to modify the modal's properties after it has been opened, such as changing the title, buttons, or visibility of header/footer from inside the modal.

#### Usage:

```ts
ui.modal.update({
    locationId: 'your-location-id',
    title: 'Updated modal title',
    showHeader: true,
    showFooter: true,
    closable: true,
    buttons: [
        {
            label: 'New button',
            method: () => {
                // Your method here
            }
        }
    ]
})
```

#### Parameters

| Name         | Required | Default | Description                                                                                    |
|:-------------|:---------|:--------|:-----------------------------------------------------------------------------------------------|
| `locationId` | true     |         | The id of the modal which should be updated                                                    |
| `title`      | false    |         | The new title of the modal                                                                     |
| `showHeader` | false    |         | Enable or disable the header in the modal                                                      |
| `showFooter` | false    |         | Enable or disable the modal footer                                                             |
| `closable`   | false    |         | If set to `false` then the modal can only be closed programmatically                           |
| `buttons`    | false    |         | Array of button configurations which will render buttons in the footer of the modal            |

### Close modal

Closes an opened modal. You need use the correct `locationId` of the modal which should get closed. If you don't provide a `locationId` the last modal without a `locationId` gets closed.

#### Usage:

```ts
ui.modal.close({ locationId: 'your-location-id' })
```

#### Parameters

| Name         | Required | Default | Description                                                                                                               |
|:-------------|:---------|:--------|:--------------------------------------------------------------------------------------------------------------------------|
| `locationId` | false    |         | The locationId of the modal which should get closed. If not provided, the last modal without a locationId will be closed. |

---

---

## resources/admin-extension-sdk/api-reference/ui/module.md
**Source:** [resources/admin-extension-sdk/api-reference/ui/module.md](https://developer.shopware.com/resources/admin-extension-sdk/api-reference/ui/module.md)  
---

---

## Payment Overview Cards
**Source:** [resources/admin-extension-sdk/api-reference/ui/module/paymentOverviewCard.md](https://developer.shopware.com/resources/admin-extension-sdk/api-reference/ui/module/paymentOverviewCard.md)  
# Payment Overview Cards

### Add a custom payment method overview card in settings

Starting with Shopware 6.4.14.0, you can render a custom card in the new payment method overview.
With that, you can replace the default card, where you can toggle the active state of a payment method, with your own component.
This allows you, for example, to require an onboarding to your payment provider before activating the payment method.

### Parameters

| Name                    | Required | Default        | Description                                                                                                                         |
|:------------------------|:---------| :------------- |:------------------------------------------------------------------------------------------------------------------------------------|
| `positionId`            | true     |                | The position id that is created in the payment overview, where you can add a component section to                                   |
| `paymentMethodHandlers` | true     |                | A list of formatted payment method handlers, which are handled by your component and where the default card should not be rendered. |
| `component`             | false    |                | The component name of you custom payment overview card. Only useful, if you have a plugin with a registered component               |

### Extension example

```ts
import { ui } from '@shopware-ag/meteor-admin-sdk';

if (sw.location.is(sw.location.MAIN_HIDDEN)) {
  // create the position
  ui.module.payment.overviewCard.add({
    positionId: 'my-custom-payment-overview-position',
    paymentMethodHandlers: [
      'handler_my_custom_payment_method_one',
      'handler_my_custom_payment_method_two', 
      // ...
    ],
  });
    
  // add your component to that position
  ui.componentSection.add({
    component: 'card',
    positionId: 'my-custom-payment-overview-position',
    props: {
      title: 'My payment provider',
      subtitle: 'We have all the methods that exist',
      locationId: 'my-custom-payment-overview-position-before'
    }
  })
}

// render your view to that location
if (sw.location.is('my-custom-payment-overview-position-before')) {
  // your content here
}
```

### Custom plugin component example

```ts
import { ui } from '@shopware-ag/meteor-admin-sdk';

// register a custom component
Component.register('my-custom-payment-overview-card', {
  template: ``,// your template here
  props: {
    paymentMethods: {
      type: Array,
      required: true,
    },
  },
  methods: {
    async changePaymentMethodActive(paymentMethod) {
      paymentMethod.active = !paymentMethod.active;

      this.$emit('set-payment-active', paymentMethod);
    },
  },
});

// add that component to the payment overview
ui.module.payment.overviewCard.add({
  component: 'my-custom-payment-overview-card',
  positionId: 'my-custom-payment-overview-position',
  paymentMethodHandlers: [
    'handler_my_custom_payment_method_one',
    'handler_my_custom_payment_method_two',
    // ...
  ],
});
```

---

---

## Settings Item
**Source:** [resources/admin-extension-sdk/api-reference/ui/settingsItem.md](https://developer.shopware.com/resources/admin-extension-sdk/api-reference/ui/settingsItem.md)  
# Settings Item

### Add settings item

Add a new settings item to the Shopware settings. The content of the settings item module is determined by your `locationId`.
A specific view or a set of actions can be triggered based on the `locationId`.

#### Usage:

```ts
ui.settings.addSettingsItem({
    label: 'App Settings',
    locationId: 'settings-location-id',
    icon: 'regular-AR',
    displaySearchBar: true,
    displaySmartBar: false,
    tab: 'plugins',
});
```

#### Parameters

| Name                 | Required | Default        | Description                                                   |
| :------------------- | :------- | :------------- | :------------------------------------------------------------ |
| `label`              | true     |                | The label of the tab bar item                                 |
| `locationId`         | true     |                | The id for the content of the settings item module            |
| `icon`               | true     |                | The icon to display in your settings item                     |
| `displaySearchBar`   | false    | true           | Toggles the sw-page search bar on/off                         |
| `displaySmartBar`    | false    | true           | Toggles the sw-page smart bar on/off                          |
| `tab`                | false    | 'plugins'      | Determines in which tab your settings item will be displayed  |

### Getting the right icon

Assuming that your editor supports TypeScript, you should get auto-completion for valid `icon` values.
In case that doesn't work take a look at the list [here](https://github.com/shopware/meteor-admin-sdk/blob/trunk/src/icons.ts).

#### Example

![Settings item example](./assets/add-settings-item-example.png)

```ts
import { location, ui } from '@shopware-ag/meteor-admin-sdk';

// General commands
if (location.is(location.MAIN_HIDDEN)) {
    // Add the settings item to the plugins tab
    ui.settings.addSettingsItem({
        label: 'App Settings',
        locationId: 'settings-location-id',
        icon: 'regular-AR',
        displaySearchBar: true,
        tab: 'plugins',
    });
}

// Render your custom view
if (location.is('settings-location-id')) {
    document.body.innerHTML = '<h1 style="text-align: center">Hello from your settings item</h1>';
}
```

---

---

## Sidebars
**Source:** [resources/admin-extension-sdk/api-reference/ui/sidebars.md](https://developer.shopware.com/resources/admin-extension-sdk/api-reference/ui/sidebars.md)  
# Sidebars

A sidebar provides a contextual panel that displays at the right edge of the Administration window. Unlike modals, sidebars allow users to view and interact with additional content or functionality without losing context of the main interface. Sidebars should be opened in response to user interaction rather than appearing automatically. As a best practice, avoid opening sidebars without clear user context - for example, automatically displaying extension changelog sidebars immediately after login creates a poor user experience by requiring manual dismissal of each one.

### Add a sidebar

Add a new sidebar. The content of the sidebar is determined by your `locationId`.

#### Usage:

```ts
sw.ui.sidebar.add({
    title: 'Awesome Chat Bot',
    locationId: 'sidebar-chat-bot',
    icon: 'regular-sparkles',
});
```

#### Parameters

| Name | Required | Description | Available at Shopware |
| :----------- | :------- | :--------------------------------------------------------------------------------------------------------------------------------------------- | :---------------------|
| `title` | true | The title of the sidebar | 6.7 |
| `locationId` | true | The id for the content of the sidebar | 6.7 |
| `icon` | true | The icon to display in the sidebar. You can use any icon from the Shopware icon library | 6.7 |
| `resizable` | false | Enables horizontal resizing of the sidebar | 6.7.2.0 |

#### Example

![Menu item example](../assets/sidebar-example.png)

### Close a sidebar

Close an existing sidebar programmatically.

#### Usage:

```ts
sw.ui.sidebar.close({
    locationId: 'sidebar-chat-bot',
});
```

#### Parameters

| Name | Required | Description | Available at Shopware |
| :----------- | :------- | :--------------------------------------------------------------------------------------------------------------------------------------------- | :---------------------|
| `locationId` | true | The id of the sidebar to close | 6.7 |

### Remove a sidebar

Remove a sidebar completely from the DOM.

#### Usage:

```ts
sw.ui.sidebar.remove({
    locationId: 'sidebar-chat-bot',
});
```

#### Parameters

| Name | Required | Description | Available at Shopware |
| :----------- | :------- | :--------------------------------------------------------------------------------------------------------------------------------------------- | :---------------------|
| `locationId` | true | The id of the sidebar to remove | 6.7 |

---

---

## Tabs
**Source:** [resources/admin-extension-sdk/api-reference/ui/tabs.md](https://developer.shopware.com/resources/admin-extension-sdk/api-reference/ui/tabs.md)  
# Tabs

### Add tab item

Add a new tab item to an existing tab bar. The content of the the new tab item
contains a component section. This works with tab bar's which have routing and
also static tab bars. If the tab bar has routing then the route for the tab item
will be generated automatically.

#### Usage:

```ts
import { ui } from '@shopware-ag/meteor-admin-sdk';

ui.tabs('sw-product-detail' /* The positionId of the tab bar*/).addTabItem({
    label: 'Example tab',
    componentSectionId: 'example-product-detail-tab-content'
})
```

#### Parameters

| Name                 | Required | Default | Description                                             |
| :------------------- | :------- | :------ | :------------------------------------------------------ |
| `label`              | true     |         | The label of the tab bar item                           |
| `componentSectionId` | true     |         | The Id for for the component section in the tab content |

#### Example

![Tab item example](./assets/add-tab-item-example.png)

```ts
import { ui, location } from '@shopware-ag/meteor-admin-sdk';

// For general commands
if (location.is(location.MAIN_HIDDEN)) {
    // Add tab bar item
    ui.tabs('sw-product-detail').addTabItem({
        label: 'Example',
        componentSectionId: 'my-awesome-app-example-product-view'
    })

    // Add component to the new created section
    ui.componentSection.add({
        component: 'card',
        positionId: 'my-awesome-app-example-product-view',
        props: {
            title: 'Hello in the new tab',
            locationId: 'my-example-product-view-tab-card'
        }
    })
}

// Render custom view of the component
if (location.is('my-example-product-view-tab-card')) {
    document.body.innerHTML = '
        <h1>Hello in the example card</h1>
        <button onClick="sw.notification.dispatch({ title: 'Foo', message: 'bar' })">
            Throw notification
        </button>
    ';
}
```

---

---

## Window
**Source:** [resources/admin-extension-sdk/api-reference/window.md](https://developer.shopware.com/resources/admin-extension-sdk/api-reference/window.md)  
# Window

### Redirect to another URL

#### Usage:

```ts
sw.window.redirect({
    url: 'https://www.shopware.com,
    newTab: true
})
```

#### Parameters:

| Name | Required | Default | Description |
| :------ | :------ | :------ | :------ |
| `url` | true | | The title of the notification |
| `newTab` | false | false | The message of the notification |

#### Return value:

Returns a promise without data.

### Push to another page

For redirecting to other pages in the admin.

#### Usage:

The usage matches the Vue Router push capabilities. Here are two examples how to use it for redirecting to your own modules:

```ts
sw.window.routerPush({
    name: 'sw.extension.sdk.index',
    params: {
        id: 'the_id_of_the_module' // can be get with context.getModuleInformation
    }
})
```

```ts
sw.window.routerPush({
    path: `/extension/${the_id_of_the_module}` // id can be get with context.getModuleInformation
})
```

#### Parameters:

| Name | Required | Default | Description |
| :------ | :------ | :------ | :------ |
| `name` | false | undefined | The name of the route |
| `path` | false | undefined | The path of the route |
| `params` | false | undefined | Additional params for the new route |
| `replace` | false | false | Should not change the browser history |

#### Return value:

Returns a promise without data.

### Reload page

Useful for development. You can trigger a page reload on file changes.

#### Usage:

```ts
sw.window.reload()
```

#### Parameters:

No parameters required.

#### Return value:

Returns a promise without data.

### Get an unique identifier for the window

> Available since Shopware v6.7.1.0

When it comes to session handling it can be useful to have a unique identifier for your window.

### Usage:

```ts
sw.window.getId() 
```

### Parameters

No parameters required

### Return value:

A `string` representing an unique identifier for the current window

### Example

In this example we check if the `sessionStorage` contains data from a former window. This can happen if a user uses the *Duplicate Tab* feature of some browsers.

```ts
const windowId = sw.window.getId();
const storedWindowId = globalThis.sessionStorage.getItem('window-id');

if (windowId !== storedWindowId) {
    globalThis.sessionStorage.clear();
    globalThis.sessionStorage.setItem('window-id', windowId);
}

```

### Get the view router path

> Available since Shopware v6.7.3.0

You can get the view router full path.

#### Usage:

```ts
sw.window.getPath()
```

#### Parameters:

No parameters required.

#### Return value:

A `string` with the full path, or empty if router not found.

---

---

## resources/admin-extension-sdk/concepts.md
**Source:** [resources/admin-extension-sdk/concepts.md](https://developer.shopware.com/resources/admin-extension-sdk/concepts.md)  
---

---

## Component sections
**Source:** [resources/admin-extension-sdk/concepts/component-sections.md](https://developer.shopware.com/resources/admin-extension-sdk/concepts/component-sections.md)  
# Component sections

In most cases extension developers will directly use the extension capabilities of the UI components (e.g. adding tab items, adding button to grid, ...). This will cover most needs of many extensions. But in cases where a extension need special solutions which aren't feasible with the given extension they can use a feature named `Component Sections`. These are sections where any extension developer can inject components.

These components are prebuilt (like cards) and contain in most cases custom [location](./locations.md) where the extension has the full freedom to render anything.

### Example:

```js
if (location.is(location.MAIN_HIDDEN)) {
    sw.ui.componentSection.add({
        // Choose a position id where you want to render a custom component
        positionId: 'sw-manufacturer-card-custom-fields__before',
        // The Component Sections provides different components out of the box
        component: 'card', 
        // Props are depending on the type of component
        props: {
            title: 'Hello from plugin',
            subtitle: 'I am before the properties card',
            // Some components can render a custom view. In this case the extension can render custom content in the card.
            locationId: 'my-app-card-before-properties'
        }
  })
}

// Render the custom UI when the iFrame location matches your defined location
if (sw.location.is('my-app-card-before-properties')) {
    document.body.innerHTML = '<h1>Hello World before</h1>';
    document.body.style.background = 'blue';
}
```

![Component Sections screenshot example](./assets/component-sections-example.png)

If you want to render tabs inside the `card` component section, we provide a way to do so:

```js
if (sw.location.is(sw.location.MAIN_HIDDEN)) {
  // Choose a position id where you want to render a custom component
  sw.ui.componentSection.add({
      // The Component Sections provides different components out of the box
      component: 'card', 
      // Props are depending on the type of component
      props: {
          title: 'Hello from plugin',
          subtitle: 'I am before the properties card',
          // Render tabs and custom tab content with the provided location id
          tabs: [
              {
                  name: 'example-tab-1',
                  label: 'First tab', 
                  locationId: 'example-tab-1'
              },
              {
                  name: 'example-tab',
                  label: 'Second tab',
                  locationId: 'example-tab-2'
              }
          ],
      }
  })
}

// Render the custom UI for different tab with the location id
if (sw.location.is('example-tab-1')) {
  document.body.innerHTML = '<h1>My first tab</h1>';
  document.body.style.background = 'blue';
}

if (sw.location.is('example-tab-2')) {
  document.body.innerHTML = '<h1>My second tab</h1>';
  document.body.style.background = 'yellow';
}
```

![Component Sections screenshot example](./assets/component-sections-with-tabs-example.png)

---

---

## Locations
**Source:** [resources/admin-extension-sdk/concepts/locations.md](https://developer.shopware.com/resources/admin-extension-sdk/concepts/locations.md)  
# Locations

Extensions can render custom views via iFrames. To support multiple views in different places every `location` of the iFrame gets a unique ID. These can be defined by the extension developer itself.

*Example:*

A extension wants to render a custom iFrame in a card in the dashboard. The `location` of the iFrame has then a specific `locationId` like `sw-dashboard-example-app-dashboard-card`. The app can also render another iFrames which also get `locationId`s. In our example it is a iFrame in a custom modal: `example-app-example-modal-content`.

The extension want to render different views depending on the `location` of the iFrame. So the extension developer can render the correct view depending on the `locationId`:

```js
// Add the ui extensions when your extension is loaded in the hidden iFrame
if (sw.location.is(sw.location.MAIN_HIDDEN)) {
  ui.componentSection.add({
      component: 'card',
      positionId: 'sw-product-properties__before',
      props: {
          title: 'Hello from plugin',
          subtitle: 'I am before the properties card',
          /**
           *  The locationId:
           **/
          locationId: 'my-app-card-before-properties'
      }
  })
}

// Render the custom UI when the iFrame location matches your defined location
if (sw.location.is('my-app-card-before-properties')) {
    document.body.innerHTML = '<h1>I am the in the location "my-app-card-before-properties"</h1>';
}
```

## Base location

Every extension gets rendered in a hidden iFrame. In this iFrame the extension can execute different commands to extend
the administration and add custom locations to different extension points. To check if the script will be executed in this
location you can use the predefined constant:

```js
import { location } from '@shopware-ag/meteor-admin-sdk';

if (location.is(location.MAIN_HIDDEN)) {
  // Do the stuff in the hidden iFrame
}
```

## Change height of location iFrame

The iFrame height is by default fixed. You can update the height with the location helper:

```js
location.updateHeight(750); // change iFrame height to 750px
```

If you use a parameter then the height will automatically be calculated so that your whole view gets rendered. In most cases
you don't want to update the height manually. To watch for height changes you can use the auto resizer. It updates the iFrame
height everytime the height of the view changes:

```js
// watch for height changes and update the iFrame
location.startAutoResizer();
```

![Auto Resizer example](./assets/auto-resizer.gif)

## Avoiding scrollbars

If you render custom locations it is useful to disable the scroll behavior in your view. Otherwise scrollbars are visible
which aren't needed in most cases. To avoid this you can add the css property `overflow: hidden;` to the `body` element.

## For existing plugin migrations: render Vue components instead of iFrames

In some cases you just want to use specific features from the SDK and some features from the existing plugin system which works with Twig and Component overriding. In this case you can do some things with the SDK but render components from the Shopware Component Factory instead of iFrames.

To do this you need to register the component in the existing plugin system:

```js
Shopware.Component.register('your-component-name', {
  // your component
})
```

Now if you want to render the component in a location you need to add the name of the component to the current location. This can be done with the `sdkLocation` store:

```js
Shopware.State.commit('sdkLocation/addLocation', {
    locationId: 'your-location-id',
    componentName: 'your-component-name'
})
```

With this feature you can create mix the usage of the SDK and the existing plugin system. A complete example could be looking like this. It creates a new tab item in the product detail page, renders a card with the componentSection renderer and inside the card it renders the location. But instead of the traditional location it renders a Vue component which was registered in the Shopware Component Factory.

```js
// in a normal plugin js file without a HTML file
import { ui, location } from '@shopware-ag/meteor-admin-sdk';

if (!location.isIframe()) {
  const myLocationId = 'my-example-location-id';

  // Create a new tab entry
  ui.tabs('sw-product-detail').addTabItem({
      label: 'Example tab',
      componentSectionId: 'example-product-detail-tab-content'
  })

  // Add a new card to the tab content which renders a location
  ui.componentSection.add({
      component: 'card',
      positionId: 'example-product-detail-tab-content',
      props: {
          title: 'Component section example',
          locationId: myLocationId
      }
  })

  // Register your component which should be rendered inside the location
  Shopware.Component.register('your-component-name', {
    // your component
  })

  // Add the component name to the specific location
  Shopware.State.commit('sdkLocation/addLocation', {
      locationId: myLocationId,
      componentName: 'your-component-name'
  })
}
```

---

---

## Positions
**Source:** [resources/admin-extension-sdk/concepts/positions.md](https://developer.shopware.com/resources/admin-extension-sdk/concepts/positions.md)  
# Positions

Extension developer can extend existing areas or create new areas in the administration. It is so flexible that there are way to many Id's to remember. To identify the positions which the developer want to extend we need a unique ID for every position. These Id's are the `positionId`s.

### Example:

A extension wants to add a new tab item to a tab-bar. In the administration are
many tab-bars available. So the developer needs to choose the correct `positionId` to tell the admin which tab-bar should be extended. In this example the developer adds a new tab item to the tab-bar in the product detail page.

```js
sw.ui.tabs('sw-product-detail').addTabItem({ ... })
```

### Vue Devtools Plugin for finding the PositionId's

It is impossible to create a list of all potential position Id's. And they would be hard to manage. To solve this problem the SDK provides a custom plugin for the Vue Devtools. It makes identifying the position Id's very easy.

Just open the plugin in the Devtools (It is available directly when you open the Administration). Then you can see all positions at the current administration view which are available for extending. If you click at one position Id you get more information about it. Like the property in the meteor-admin-sdk so that you directly know what functionality this position has.

In summary: the Devtool plugin provides a visual way to see which parts can be extended and what are the positionIDs for the extension position. You can find a detailed guide in the tooling section of this documentation: [Vue Devtools](../tooling/vue-devtools.md)

---

---

## Selectors
**Source:** [resources/admin-extension-sdk/concepts/selectors.md](https://developer.shopware.com/resources/admin-extension-sdk/concepts/selectors.md)  
# Selectors

Selectors are a powerful tool to reduce the payload and minimize the needed privileges.
They are used in `data.subscribe` and `data.get`. Selectors are an array of strings. Each string represents a path to a property in the dataset.

### Example:

Imagine this payload:

```json
{
    "name": "My Product",
    "manufacturer": {
        "name": "My Manufacturer"
    },
    "price": 100,
    "variants": [
        {
            "name": "First Variant",
            "price": 110
        },
        // contains more variants
    ],
    // contains more properties
}
```

If you are only interested in the names of the product and manufacturer, you can use the following selectors:

```javascript
data.get({
    id: 'sw-product-detail__product',
    selectors: ['name', 'manufacturer.name'],
}).then((product) => {
    console.log(product); // prints { name: "My Product", manufacturer: { name: "My Manufacturer" } }
});
```

### Combining selectors

Again for the above payload, if you are interested in multiple properties of the manufacturer, you can use the following selectors:

```javascript
data.get({
    id: 'sw-product-detail__product',
    selectors: ['manufacturer.id', 'manufacturer.name'],
}).then((product) => {
    console.log(product); // prints { manufacturer: { id: '065e71ab94d778a980008e8c3e890270', name: "My Manufacturer" }
});
```

### Arrays

If you are interested in a specific variant, you can use the following selectors:

```javascript
data.get({
    id: 'sw-product-detail__product',
    selectors: ['variants.[0].name'],
}).then((product) => {
    console.log(product); // prints { variants: [ { name: "First Variant" } ] }
});
```

If you are interested in all variants, you can use wildcards. A wildcard is the asterix symbol (`*`)

```javascript
data.get({
    id: 'sw-product-detail__product',
    selectors: ['variants.*.name'],
}).then((product) => {
    console.log(product); // prints { variants: [ { name: "First Variant" }, // same structure for all entries ] }
});
```

---

---

## FAQ
**Source:** [resources/admin-extension-sdk/faq.md](https://developer.shopware.com/resources/admin-extension-sdk/faq.md)  
# FAQ

## Can I use the same domain with subfolders for multiple apps?

No, for technical reasons, it is not possible to use the same domain with subfolders to host multiple apps. Each app must have its own separate domain.
The preferred solution is to use subdomains for each app. For example, you can use subdomains like "app-one.your-company.com", "app-two.your-company.com", and so on. Using subdomains allows you to have separate domains for each app, which avoids the technical limitations associated with using subfolders.

## How can I use components that resemble the original components in the administration?

While it is not possible to use the exact same components in the Shopware administration, there is a component library called Meteor Component Library that offers similar components. The Shopware administration components are not native Vue components because they have extension capabilities, Twig templates, and other features that cannot be directly used. However, by utilizing the Meteor Component Library, you can achieve a native look and feel for your app that seamlessly integrates with the original Shopware administration.

To access the Meteor Component Library, visit the following link: https://github.com/shopware/meteor-component-library

## How can I use snippets to translate my app?

You can manage all texts rendered within your [locations](../concepts/locations.md) with a translation plugin of your choice. If you're utilizing Vue.js as your frontend framework, you can use the i18n plugin. Additionally, to ensure consistency between your app and the Shopware Administration, you can synchronize language changes by [subscribing to them through the context API](../api-reference/context.md#subscribe-on-language-changes).

For text elements in native Shopware Administration components, such as titles within [component sections](../concepts/component-sections.md), you can employ snippet files within your app. This is supported since the Shopware Version 6.6. Here's a how to accomplish this:

1. **Create Snippet Files:** Begin by generating a snippet file for each supported language within your app. These files should reside in the `Resources/app/administration/snippet` directory. Naming conventions follow the language code format, for instance, `en-GB.json` for English language support. The file structure mirrors that of administration snippets. However it is not impossible to overwrite Shopware Administration snippets.

```json
// <app root>/Resources/app/administration/snippet/en-GB.json
{
    "my-app-name": {
        "example-card": {
            "title": "My app",
            "subtitle": "This is my app"
        }
    }
}
```

2. **Integrate Snippets:** Utilize these snippets within your app by referencing their paths directly in your code. For example:

```js
sw.ui.componentSection('sw-manufacturer-card-custom-fields__before').add({
    component: 'card', 
    props: {
        title: 'my-app-name.example-card.title',
        subtitle: 'my-app-name.example-card.subtitle',
        locationId: 'my-app-card-before-properties'
    }
})
```

---

---

## resources/admin-extension-sdk/getting-started.md
**Source:** [resources/admin-extension-sdk/getting-started.md](https://developer.shopware.com/resources/admin-extension-sdk/getting-started.md)  
---

---

## Vue dev tools
**Source:** [resources/admin-extension-sdk/getting-started/devTools.md](https://developer.shopware.com/resources/admin-extension-sdk/getting-started/devTools.md)  
# Vue dev tools

## Prerequisites

We assume that you got the [Vue dev tools](https://devtools.vuejs.org/) installed for your browser.
The extension is available for Chrome, Firefox, Edge and as a standalone app.

## Development setup

Furthermore you should have [Shopware](https://github.com/shopware/platform) setup.
To make use of the Extension API plugin for the Vue dev tools start the watcher of the administration:

```bash
$ composer run watch:admin
```

## Vue dev tool plugin

Once you logged into your administration, open up the development tools of your browser and choose the Vue tab.
Inside the Vue tab choose the Shopware Extension API plugin.

![Devtools plugin](./assets/devtools-plugin.png)

## Usage

The plugin will show you all extension points for the current page you visit.
Once you select an extension point it will highlight the corresponding area in the viewport and give detailed information how to extend the highlighted property.

![Devtools usage](./assets/devtools-usage.png)

---

---

## Installation
**Source:** [resources/admin-extension-sdk/getting-started/installation.md](https://developer.shopware.com/resources/admin-extension-sdk/getting-started/installation.md)  
# Installation

## Prerequisites:

You need to have an working [app](https://developer.shopware.com/docs/guides/plugins/apps/app-base-guide) or [plugin](https://developer.shopware.com/docs/guides/plugins/plugins/plugin-base-guide) installed on your Shopware 6 instance.

## Prepare your app or plugin

### App:

You need to create a HTML page with an JS file for your app. This page needs to be served by your app-server as it needs to be accesible via URL.
For development purposes you can use [App server sdk](https://github.com/shopware/app-sdk-js).

Once you got the registration/ handshake working you need to add the `<base-app-url>` field to the `<admin>` section of the [manifest](https://developer.shopware.com/docs/guides/plugins/apps/app-base-guide#manifest-file) file. This field should contain the public URL of your app. Let's assume your app HTML page is served under `http://localhost/my-example-app.html`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<manifest xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://raw.githubusercontent.com/shopware/platform/trunk/src/Core/Framework/App/Manifest/Schema/manifest-1.0.xsd">
    <meta>
        <name>MyExampleApp</name>
        <!-- App meta data... -->
    </meta>

    <setup>
        <registrationUrl>http://link-to-your-local-app-server/register</registrationUrl>
        <secret>S3cr3tf0re$t</secret>
    </setup>

    <admin>
        <!-- Insert your app page URL here -->
        <base-app-url>http://localhost/my-example-app.html</base-app-url>
    </admin>
</manifest>
```

In your new HTML file you need inject a JS file. This file can use the Meteor Admin SDK via CDN or if you want to use a build tools then you
can use the NPM package.

### Plugin:

**Notice:** Plugins will work on self-hosted instances only. You won't be able to use a Shopware 6 cloud instance with plugins.

#### For Shopware 6.7 and higher:

Create the folder `custom/plugins/yourPlugin/src/Resources/app/meteor-app`. This is the base path for all new files
for your extension.

Create a new base `index.html` file. This file will be automatically injected as a hidden iFrame to the administration
when the plugin is activated. Then you need to create a JavaScript file in the subfolder `src/main.js` and
add it to your `index.html`:

```html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <link rel="icon" type="image/svg+xml" href="/vite.svg" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Your extension</title>
  </head>
  <body>
    <div id="app"></div>
    <script type="module" src="/src/main.js"></script>
  </body>
</html>
```

Then you initialize a new Node project with `npm init --yes` and install the SDK via NPM
with `npm i --save @shopware-ag/meteor-admin-sdk`.

If you want to have a custom Vite configuration you can install Vite with `npm i --save vite` and
create a `vite.config.js` file in the `meteor-app` folder with your custom configuration.

This should result in a folder structure like this:

```plaintext
custom/plugins/yourPlugin/src/Resources/app/meteor-app
├── index.html
├── vite.config.js (optional)
├── package.json
├── package-lock.json
├── src
│   ├── main.js
```

#### For Shopware 6.6 and lower:

Open the path `custom/plugins/yourPlugin/src/Resources/app/administration`. This is the base path for all new admin files.

Create a new base `index.html` file. This file will be automatically injected to the administration when the plugin is
activated. Then you need to create a JavaScript file in the subfolder `src/main.js`. This file will be automatically
injected into the created HTML file.

For plugins the best way is to install the SDK via NPM. But first you need to initialize a new NPM project in your plugin folder with
`npm init --yes`.

This should result in a folder structure like this:

```plaintext
custom/plugins/yourPlugin/src/Resources/app/administration
├── index.html
├── package.json
├── package-lock.json
├── src
│   ├── main.js
```

## Installing the SDK:

The preferred way of using the library is with a NPM package. This guarantees the smallest bundle size for your apps and plugins, since this way only necessary functions are bundled together.

The CDN method is easy to use and fast to implement. It is best used for quick prototyping or if you don't want to work with building tools.

### Using NPM (require bundling):

Install it to your `package.json`

```
npm i --save @shopware-ag/meteor-admin-sdk
```

and import it into your app or plugin:

```js
// import everything as one big object
import * as sw from '@shopware-ag/meteor-admin-sdk';

// or import only needed functionality scope
import { notification }  from '@shopware-ag/meteor-admin-sdk';

// or the direct method (here with an alias)
import { dispatch as dispatchNotification } from '@shopware-ag/meteor-admin-sdk/es/notification'

```

### Using CDN:

Import the source from the CDN

```js
// use the latest version available
<script src="https://unpkg.com/@shopware-ag/meteor-admin-sdk/cdn"></script>

// use a fix version (example here: 1.2.3)
<script src="https://unpkg.com/@shopware-ag/meteor-admin-sdk@1.2.3/cdn"></script>
```

and access it with the global variable `sw`.

```js
sw.notification.dispatch({
  title: 'My first notification',
  message: 'This was really easy to do'
})
```

## Adding types for Entities (TS only)

The data management inside the SDK supports complete TypeScript support. This allows complete type safety when getting
entities, editing or saving them.

For adding the types you need to create a global type definition file like `global.d.ts`. Inside this file you can
add the types for the entities by extending the global namespace.

### Using auto-generated types from Shopware

This is the easiest solution. Just install the correct type definition for the matching shopware version:

`npm install @shopware-ag/entity-schema-types@5.0.0`

The version number should match the Shopware version number without the `6.` in the beginning. Examples:

`Shopware 6.5.0.0` → `@shopware-ag/entity-schema-types@5.0.0`
`Shopware 6.5.1.2` → `@shopware-ag/entity-schema-types@5.1.2`
`Shopware 6.6.3.1` → `@shopware-ag/entity-schema-types@6.3.1`

```ts
// global.d.ts
import '@shopware-ag/entity-schema-types';
```

### Using "any" fallback

This is the easiest solution. You set the type to `any` for every entity. The downside of this is the missing type safety.

```ts
// global.d.ts
declare namespace EntitySchema {
    interface Entities {
        [entityName: string]: any;
    }
}
```

### Using custom types

This is the safest solution. You define for every needed entity every property and association. The downside of this is
that it takes time to write the definitions.

```ts
// global.d.ts
declare namespace EntitySchema {
    interface Entities {
        // using product_manufacturer as an example
        product_manufacturer: product_manufacturer;
        // in this case 'media', 'product' and 'product_manufacturer_translation' is also needed
        ...
    }

    interface product_manufacturer {
        id: string;
        versionId: string;
        mediaId?: string;
        link?: string;
        name: string;
        description?: string;
        customFields?: unknown;
        /* 
        * Entity and EntityCollection is defined in the namespace and can directly be used.
        * The value in the generic (here 'media', 'product' and 'product_manufacturer_translation') need
        * also to be defined in this file.
        */ 
        media?: Entity<'media'>;
        products?: EntityCollection<'product'>;
        translations: EntityCollection<'product_manufacturer_translation'>;
        createdAt: string;
        updatedAt?: string;
        translated?: {name?: string, description?: string, customFields?: unknown};
    }

    // 'media', 'product' and 'product_manufacturer_translation' also needs to be added
    ...
}
```

---

---

## Usage
**Source:** [resources/admin-extension-sdk/getting-started/usage.md](https://developer.shopware.com/resources/admin-extension-sdk/getting-started/usage.md)  
# Usage

After [installing](./installation) the Meteor Admin SDK successfully you can use it in your apps and plugins.

## Adding functionality to new apps or plugins

You can use the SDK features directly in your JS file. Just import the specific feature (NPM method) or use the method in the
`sw` object (CDN method). You can find all features in the API reference documentation.

### NPM example:

```js
// import notification toolkit from the SDK
import { notification }  from '@shopware-ag/meteor-admin-sdk';

// dispatch a new notification
notification.dispatch({
  title: 'My first notification',
  message: 'This was really easy to do'
})
```

### CDN example:

```js
// access the "notification" toolkit in the global "sw" object and dispatch a new notification
sw.notification.dispatch({
  title: 'My first notification',
  message: 'This was really easy to do'
})
```

## Adding functionality to existing plugins

Shopware 6 has a rich plugin extension system for the Admin based on Twig and the concepts of component overriding and component extending. These
concepts are very powerful, but may also come with a steep learning curve. That's why you can migrate gradually to the new Meteor Admin SDK, if you want.
Both approaches can work together. This way you can start by converting only parts of your plugins at first and then gradually converting more and more of your plugins as new features are added to the SDK.
This approach is also going to help with simplifying your plugins and preparing them for long term usage.

#### Example:

```js
// Use existing extension capabilties
Shopware.Component.override('sw-dashboard-index', {
    methods: {
        async createdComponent() {
          // Can also use Meteor Admin SDK features
          await sw.notification.dispatch({
            title: 'Hello from the plugin',
            message: 'I am combining the existing approach with the new SDK approach',
          })

          this.$super('createdComponent');
        }
    }
});
```

### Using locations with normal Vue components without iFrame rendering

**This feature is not yet released in Shopware.
It's only available with the development enviroment or `dev-trunk` version of Shopware.**

It is useful when you want to migrate partially from the twig plugin system to the SDK extension system that you use both systems together. To make this happen you can render normal Vue components in the Shopware administration for the locations instead of your iFrame view.

To do this you need to register the component in the existing plugin system:

```js
Shopware.Component.register('your-component-name', {
  // your component
})
```

Now if you want to render the component in a location you need to add the name of the component to the current location. This can be done with the `sdkLocation` store:

```js
Shopware.State.commit('sdkLocation/addLocation', {
    locationId: 'your-location-id',
    componentName: 'your-component-name'
})
```

With this feature you can create mix the usage of the SDK and the existing plugin system. A complete example could be looking like this. It creates a new tab item in the product detail page, renders a card with the componentSection renderer and inside the card it renders the location. But instead of the traditional location it renders a Vue component which was registered in the Shopware Component Factory.

```js
// in a normal plugin js file without a HTML file
import { ui, location } from '@shopware-ag/meteor-admin-sdk';

if (!location.isIframe()) {
  const myLocationId = 'my-example-location-id';

  // Create a new tab entry
  ui.tabs('sw-product-detail').addTabItem({
      label: 'Example tab',
      componentSectionId: 'example-product-detail-tab-content'
  })

  // Add a new card to the tab content which renders a location
  ui.componentSection.add({
      component: 'card',
      positionId: 'example-product-detail-tab-content',
      props: {
          title: 'Component section example',
          locationId: myLocationId
      }
  })

  // Register your component which should be rendered inside the location
  Shopware.Component.register('your-component-name', {
    // your component
  })

  // Add the component name to the specific location
  Shopware.State.commit('sdkLocation/addLocation', {
      locationId: myLocationId,
      componentName: 'your-component-name'
  })
}
```

---

---

## resources/admin-extension-sdk/internals.md
**Source:** [resources/admin-extension-sdk/internals.md](https://developer.shopware.com/resources/admin-extension-sdk/internals.md)  
---

---

## Datahandling
**Source:** [resources/admin-extension-sdk/internals/datahandling.md](https://developer.shopware.com/resources/admin-extension-sdk/internals/datahandling.md)  
# Datahandling

This guide elaborates how the data handling works between extensions and the Shopware administration.

## What are datasets?

Datasets consist of a unique identifier, an `id` and some `data` which could be anything from a single value to a whole entity.
The id gives some insight on what to expect as the value. For example `sw-product-detail__product` contains the product of the product detail page.

## How to find available datasets

You can explore all available datasets with the Vue Devtool extension we provide with the Shopware administration.

* Open the Vue DevTools in the Shopware Administration
* Change to the Shopware Extension API inspector

In this inspector you will see all published datasets if there are any in the current view.

#### Example

![Action button example](./assets/devtool-example.png)

---

---

## How it works
**Source:** [resources/admin-extension-sdk/internals/how-it-works.md](https://developer.shopware.com/resources/admin-extension-sdk/internals/how-it-works.md)  
# How it works

The Meteor Admin SDK provides wrapper methods for a better development experience. It abstracts and hides the more
complex logic behind a simple API. This makes it easier for app and plugin developers to create their solutions and focus
on their business instead of caring about the technical details.

## Admin communication

Technically speaking, apps and plugins are communicating with the Administration via the [postMessage API](https://developer.mozilla.org/en-US/docs/Web/API/Window/postMessage). It is a secure communication channel between different windows. In most cases it will be used to communicate
from an iFrame to the main window or the other way around.

The Extension SDK works in the same way, but it uses a hybrid approach. Every method is callable within an iFrame and also
from the same window. This allows apps (within iFrames) and plugins (in the same window) to use the same API.

![postMessage communication](./assets/post-message-communication.png)

Normally the postMessage API is very limited and not easy to use. You merely can send string values from one window to
another. This isn't very handy during the development process. To provide a smoother experience, we wrote some helper methods that
make working with the postMessage API a breeze.

The helper methods can be found in the `channel` file. It holds different methods for easier communication. The most important ones are `send` and `handle`. They are responsible for sending and handling data.

Here is an example to give you a better understanding of how that works.

### Example workflow

Let's imagine that an app or plugin calls the `context.getLanguage` method from the Extension SDK:

```js
// from app/plugin
const language = await sw.context.getLanguage();
```

But what is happening in the background? The method is a wrapper for the `send` method in the `channel`. When you use it, it will call `send` with a predefined type:

```js
// from app/plugin
send('contextLanguage', {});
```

Each message has a unique type. The types are hidden from plugin and app developers and are only responsible for the underlying handling. Knowing the unique type we can tell what type of request there is in the Administration and what response it expects.

The `send` method is producing magic in the background now. It creates a data object with following properties:

```js
{
  _type: 'contextLanguage',
  _data: {},
  _callbackId: 'aRand0mGeneratedUniqueId'
}
```

The `_type` property is there to recognize the request type. The `_data` property is custom data that will be added by the app or plugin. E.g. the title, message or any more information available for a notification. The `_callbackId` is needed for the Administration to send back the data including an ID, so that the sender is able to recognize it and use the included data.

This object will be sent as a stringified JSON object to the Administration window via the postMessage API.

Now let's have a look at what needs to happen on the side of the Administration.

```js
// at Administration
handle('contextLanguage', () => {
    return {
        languageId: Shopware.Context.api.languageId,
        systemLanguageId: Shopware.Context.api.systemLanguageId,
    };
});
```

It uses the `handle` method, which is also a helper method of the `channel`. You see now, that the type matches the sender type. And in the second argument it provides a method that returns the data.

This method reacts to every `contextLanguage` request and sends the data values back to the source of the request. It also creates an object that includes meta information which in turn are needed for the original `send` window:

```js
{
  _type: 'contextLanguage',
  _response: { languageId: '1a2b3c...', systemLanguageId: '9f8g7h...', },
  _callbackId: 'aRand0mGeneratedUniqueId'
}
```

The source that will send the request is adding a new event listener before sending the message. This event listener listens to all incoming messages and if any of these messages matches the type and the callback ID of the message sent, it will handle the data.

In our case it will in return get a stringified object that includes the language information. These will be parsed and returned to the first method call:

```js
// from app/plugin
const language = await sw.context.getLanguage();

// language = { languageId: '1a2b3c...', systemLanguageId: '9f8g7h...', }
```

And this is basically it! The app or plugin has now got the data from the Administration. It all just looks like a simple call, but there is a lot going on in the background.

## Sending methods

In normal cases you can't add methods to JSON objects which will get stringified. But in our case we are convinced it would make the many developers' lives much easier if they can also use their own methods in the calls.

To handle these edge-cases we are converting the methods to information objects like this:

```js
{
  __type__: '__function__',
  id: 'theUniqueFunctionId' // will be generated uniquely
}
```

The method will be saved in a `methodRegistry` where the unique ID can be used as an identifier.

The receiver of the object converts this object back to a method that triggers the original method. This can't be done directly, because we do not have direct access to the method. To solve this problem, we send a special postMessage call to the original source. This call contains all arguments of the method called and its unique ID:

```js
send('__function__', {
  args: args,
  id: id,
})
```

The sender gets the message back and executes the method with the matching ID and the given arguments. The return value will then be sent back to the converted method in the receiver.

This complex logic is also abstracted. To use it, just add methods to
the data. They will then be converted and handled automatically.

---

---

## resources/admin-extension-sdk/tooling.md
**Source:** [resources/admin-extension-sdk/tooling.md](https://developer.shopware.com/resources/admin-extension-sdk/tooling.md)  
---

---

## Vue Devtools
**Source:** [resources/admin-extension-sdk/tooling/vue-devtools.md](https://developer.shopware.com/resources/admin-extension-sdk/tooling/vue-devtools.md)  
# Vue Devtools

The administration has many extension capabilties. Many of them are components with an unique positionId. It can be
difficult to find out their id to extend them. You need to manually look in the core source code to find out the id.

The better way is using the Vue devtools plugin. It is preinstalled in every Shopware administration so that you can
find out the ids in an interactive and visual way.

## Prerequisites:

You need to have the Vue Devtools installed. The plugin API for the Vue Devtools is only available in the versions 6+ (Currently only in the [beta channel](https://chrome.google.com/webstore/detail/vuejs-devtools/ljjemllljcmogpfapbkkighbhhppjdbg). You can install both parallel.). If you are using an older version then this plugin will not work.

After installing the browser extensions you should be able to open the devtools in the development/watch mode of the administration. To check if the admin plugin works you can go to the settings and check if the Shopware Admin plugin is installed and enabled:

![Vue Devtools plugin settings](./assets/devtools-plugin-settings.png)

![Vue Devtools plugin settings list](./assets/devtools-plugin-settings-list.png)

## Finding extension capabilites

Navigate to the page which you want to extend. In our example we go to the product detail page in the tab specifications.

Now you can open the plugin in the top dropdown menu:

![Vue Devtools plugin tab Shopware extension](./assets/devtools-plugin-tab-shopware-extension.png)

You should see a list on the left side where all extension capabilities are listed. If you click on any of them you will directly see them highlighted in the administration.

![Vue Devtools plugin extension point selection](./assets/devtools-plugin-extension-point-selection.png)

In the inspector of the devtools you will see more information about the extension point. You can see the `Property` value which you can look in the API Reference documentation. Then you know how to use your selected extension point and which capabilities are available. And in most cases you need the `positionId` which is also shown in the inspector. The positionId is a unique identifer so that you extend not every area but only your selected one.

---

---

