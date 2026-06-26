# ADMINISTRATION UI

Compiled excerpts from the Shopware Developer Documentation snapshot. Prefer live docs at [developer.shopware.com](https://developer.shopware.com/) when in doubt.

---

## Add rule assignment configuration
**Source:** [guides/plugins/plugins/administration/advanced-configuration/add-rule-assignment-configuration.md](https://developer.shopware.com/docs/v6.6/guides/plugins/plugins/administration/advanced-configuration/add-rule-assignment-configuration.md)  
# Add rule assignment configuration

::: info
The rule assignment configuration is available from Shopware Version 6.4.8.0
:::

## Overview

You want to create a custom card in the rule assignment, where you can add or delete assignments? This guide gets you covered on this topic. Based on an example of the configuration of the `Dynamic Access` plugin, you will see how to write your configuration.

![Rule config](../../../../../assets/add-rule-assignment-configuration-0.png)

## Prerequisites

This guide **does not** explain how to create a new plugin for Shopware 6.
Head over to our Plugin base guide to learn how to create a plugin at first:

## Creating the index.js file

The first step is creating a new directory like so `<plugin root>/src/Resources/app/administration/src/module/sw-settings-rule/extension/sw-settings-rule-detail-assignments`.
Right afterward, create a new file called `index.js` in there.

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

| Option                    | Description                                                                                                                                                                                    |
|:--------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| id                        | Required identifier for the assignment, which is arbitrary but unique                                                                                                                          |
| entityName, criteria, api | Required for data loading of the assignment                                                                                                                                                    |
| gridColumns               | To define the columns, which are shown in your assignment card. Have a look into the [data grid component](../data-handling-processing/using-the-data-grid-component.md) for more information. |

### Provide to delete an assignment

If you want to provide to delete an assignment, you have to define the `deleteContext`. There are two types of the `deleteContext`.
The first one is the `one-to-many` type, which link to a column of the assignment entity like this:

```javascript
// Example of a one-to-many deleteContext
deleteContext: {
    type: 'one-to-many',
    entity: 'cms_block',
    column: 'extensions.swagCmsExtensionsBlockRule.visibilityRuleId',
},
```

The other type is `many-to-many`, which has to link to the `ManyToManyAssociationField` of the extension like this:

```javascript
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

```javascript
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

```javascript
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

For more other information, refer to [Add custom rules](../../framework/rule/add-custom-rules.md).

---

---

## Adding Shortcuts
**Source:** [guides/plugins/plugins/administration/advanced-configuration/add-shortcuts.md](https://developer.shopware.com/docs/v6.6/guides/plugins/plugins/administration/advanced-configuration/add-shortcuts.md)  
# Adding Shortcuts

## Overview

Shortcuts in Shopware 6 are defined on a Component basis. This guide will show you how to add your own ones.

## Prerequisites

All you need for this guide is a running Shopware 6 instance and full access to both the files and preferably a registered module and custom component.
Of course, you'll have to understand JavaScript, but that's a prerequisite for Shopware as a whole and will not be taught as part of this documentation.

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

Since ACL is used in the first keyboard shortcut, you might want to learn more about ACL and how to add your own ACL rules [here](../permissions-error-handling/add-acl-rules.md).

## More interesting topics

* [Writing templates](../templates-styling/writing-templates.md)
* [Adding styles](../templates-styling/add-custom-styles.md)

---

---

## Extending Webpack
**Source:** [guides/plugins/plugins/administration/advanced-configuration/extending-webpack.md](https://developer.shopware.com/docs/v6.6/guides/plugins/plugins/administration/advanced-configuration/extending-webpack.md)  
# Extending Webpack

## Overview

The Shopware 6 Administration uses [Webpack](https://webpack.js.org/) as a static module bundler. Normally you don't need to change the Webpack configuration, but if you need to here is how to do it.

## Extending the Webpack configuration

The Webpack configuration can be extended by creating the file `<plugin root>/src/Resources/app/administration/build/webpack.config.js` and exporting a function from it. This will return a [webpack configuration object](https://webpack.js.org/configuration/), as seen below:

```javascript
// <plugin root>/src/Resources/app/administration/build/webpack.config.js
const path = require('path');

module.exports = () => {
    return {
        resolve: {
            alias: {
                SwagBasicExample: path.join(__dirname, '..', 'src')
            }
        }
    };
};
```

This way, the configuration is automatically loaded and then merged with the Shopware provided webpack configuration. Configurations of plugins are **not** merged into each other. Merging is done with the [webpackMerge](https://github.com/survivejs/webpack-merge) library.

---

---

## Modify dynamic product groups blacklist
**Source:** [guides/plugins/plugins/administration/advanced-configuration/modify-blacklist-for-dynamic-product-groups.md](https://developer.shopware.com/docs/v6.6/guides/plugins/plugins/administration/advanced-configuration/modify-blacklist-for-dynamic-product-groups.md)  
# Modify dynamic product groups blacklist

## Overview

The module "Dynamic product groups" includes a condition builder to properly configure your dynamic product groups.
You might have noticed though, that this condition builder does not show all available properties,
since some of them are blacklisted in the code, such as e.g. `createdAt`.

In this guide you'll get two quick examples on how to either add new properties to this blacklist or even remove
properties from the blacklist, so they're actually shown in the Administration and thus can be used.

## Prerequisites

This guide **will not** explain in detail how to override an existing component.
For this guide you'll have to extend the component [sw-product-stream-field-select](https://github.com/shopware/shopware/blob/v6.3.4.1/src/Administration/Resources/app/administration/src/module/sw-product-stream/component/sw-product-stream-field-select/index.js) though, since it's the one [actually checking for the properties in the computed property options](https://github.com/shopware/shopware/blob/v6.3.4.1/src/Administration/Resources/app/administration/src/module/sw-product-stream/component/sw-product-stream-field-select/index.js#L41).

An example on how to override a component can be found [here](../module-component-management/customizing-components.md).

## Adding properties to blacklist

As already mentioned in the prerequisites, the check for properties in the blacklist is done in the computed property `options`.
Therefore you'll have to make sure your modifications are done **before** the check happens.

```javascript
// <plugin-root>/src/Resources/app/administration/app/src/component/sw-product-stream-field-select/index.js
const { Component } = Shopware;

Component.override('sw-product-stream-field-select', {
    computed: {
        options() {
            this.conditionDataProviderService.addToGeneralBlacklist(['deliveryTimeId']);
            return this.$super('options');
        }
    }
});
```

This example will simply add the property `deliveryTimeId` to the blacklist, so it's not configurable using the Administration anymore.
There are also nested properties, so called 'entity properties', which are selectable once you've chosen a property such as `Categories`.
Those entity properties can also be added to the blacklist by using the method `addToEntityBlacklist` instead:

```javascript
// <plugin-root>/src/Resources/app/administration/app/src/component/sw-product-stream-field-select/index.js
const { Component } = Shopware;

Component.override('sw-product-stream-field-select', {
    computed: {
        options() {
            this.conditionDataProviderService.addToEntityBlacklist('category', ['breadcrumb']);
            return this.$super('options');
        }
    }
});
```

This example would forbid the usage of `breadcrumb` from the `category` entity.

## Removing properties from the blacklist

Most likely you'd want to do the opposite and enable properties by removing entries from the blacklist.
This can be done exactly like adding properties to the blacklist:

* Remove a property from the "general blacklist", which is the first dropdown
* Remove from the "entity blacklist" which contains the properties of the previously selected entity.

```javascript
// <plugin-root>/src/Resources/app/administration/app/src/component/sw-product-stream-field-select/index.js
const { Component } = Shopware;

Component.override('sw-product-stream-field-select', {
    computed: {
        options() {
            this.conditionDataProviderService.removeFromGeneralBlacklist(['createdAt']);
            this.conditionDataProviderService.removeFromEntityBlacklist('category', ['path']);
            return this.$super('options');
        }
    }
});
```

This example enables both the general `createdAt` property, as well as the category property `path`.

---

---

## Customizing components
**Source:** [guides/plugins/plugins/administration/customizing-components.md](https://developer.shopware.com/docs/v6.5/guides/plugins/plugins/administration/customizing-components.md)  
# Customizing components

The Shopware 6 Administration allows you to override twig blocks to change its content.
This guide will teach you the basics of overriding parts of the Administration.

## Prerequisites

All you need for this guide is a running Shopware 6 instance, the files and preferably a registered module.
Of course, you'll have to understand JavaScript and have a basic familiarity with TwigJS, the templating engine, used in the Administration.
However, that's a prerequisite for Shopware as a whole and will not be taught as part of this documentation.

## Finding the block to override

In this guide we want to change the heading of the Shopware 6 dashboard to be `Welcome to a customized Administration` instead of `Welcome to Shopware 6`.
To do this we first need to find an appropriate twig block to override.
We don't want to replace too much but also to not override too little of the Administration.
In this case we only want to override the headline and not links or anything else on the page.
Looking at the twig markup for the dashboard [here](https://github.com/shopware/shopware/blob/trunk/src/Administration/Resources/app/administration/src/module/sw-dashboard/page/sw-dashboard-index/sw-dashboard-index.html.twig),
suggests that we only need to override the Twig block with the name `sw_dashboard_index_content_intro_content_headline` to achieve our goal.

## Preparing the override

Now that we know where to place our override, we need to decide what to override it with.
In this very simple example it suffices to create a twig file, declare a block with the name we previously found and to insert our new header into the block.

```text
<!-- <plugin root>/src/Resources/app/administration/src/sw-dashboard-index-override/sw-dashboard-index.html.twig -->
{% block sw_dashboard_index_content_intro_content_headline %}
    <h1>
        Welcome to a customized component
    </h1>
{% endblock %}
```

This overrides the entire Twig block with our new markup.
However, if we want to retain the original content of the Twig block and just add our markup to the existing one, we can do that by including a {% parent %} somewhere in the Twig block.
Learn more about the capabilities of twig.js [here](https://github.com/twigjs/twig.js/wiki).

As you might have noticed the heading we just replaced had a `{ $tc() }` [string interpolation](https://vuejs.org/v2/guide/syntax.html#Text) which is used to make it multilingual.
Learn more about internationalization in the Shopware 6 Administration and about adding your own snippets to the Administration [here](adding-snippets).

## Applying the override

Registering the override of the Vue component is done by using the override method of our ComponentFactory.
This could be done in any `.js` file, which then has to be later imported, but we'll place it in `<plugin root>/src/Resources/app/administration/src/sw-dashboard-index-override/index.js`.

```javascript
import template from './sw-dashboard-index.html.twig';

Shopware.Component.override('sw-dashboard-index', {
    template
});
```

The first parameter matches the component to override, the second parameter has to be an object containing the actually overridden properties , e.g. the new twig template extension for this component.

## Loading the JavaScript File

The main entry point to customize the Administration via a plugin is the `main.js` file.
It has to be placed into the `<plugin root>/src/Resources/app/administration/src` directory in order to be automatically found by Shopware 6.

The only thing now left to just add an import for our of previously created `./sw-dashboard-index-override/index.js` in the `main.js`:

```javascript
import './sw-dashboard-index-override/';
```

## More interesting topics

* [Customizing templates](writing-templates)
* [Customizing via custom styles](add-custom-styles)
* [Using base components](using-base-components)

---

---

## Customize modules
**Source:** [guides/plugins/plugins/administration/customizing-modules.md](https://developer.shopware.com/docs/v6.5/guides/plugins/plugins/administration/customizing-modules.md)  
# Customize modules

## Overview

In the `Administration` core code, each module is defined in a directory called `module`. A `module` is an encapsulated unit which implements a whole feature. For example there are modules for customers, orders, settings, etc.

## Prerequisites

All you need for this guide is a running Shopware 6 instance. Of course, you'll have to understand JavaScript and have a basic familiarity with TwigJS, the templating engine, used in the Administration. However, that's a prerequisite for Shopware as a whole and will not be taught as part of this documentation.

## Customizing a module

Module settings like `color`, `icon`, `navigation` are fixed by design and cannot be changed.

A guide for customizing components, which are already defined in existing modules, can be found here - [Customizing components](customizing-components).

However, modules themselves cannot be directly overridden.

At some point you need to add or change the routes of a module. For example when you want to add a tab to the page.

This is done by creating a new module and implementing a `routeMiddleware`. You can add those changes to your `main.js` file, which could then look like this:

```javascript
// <plugin root>/src/Resources/app/administration/src/main.js
Shopware.Module.register('my-new-custom-route', {
    routeMiddleware(next, currentRoute) {
        if (currentRoute.name === 'sw.product.detail') {
            currentRoute.children.push({
                name: 'sw.product.detail.custom',
                path: '/sw/product/detail/:id/custom',
                component: 'sw-product-detail-custom',
                meta: {
                    parentPath: "sw.product.index"
                }
            });
        }
        next(currentRoute);
    }
});
```

In this example we register a new module which uses the `routeMiddleWare` to scan the routes while the `Vue router` is being set up. If we find the route `sw.product.detail` we just add another child route by pushing it to the `currentRoute.children`.

You can find a detailed example in the [Add tab to existing module](add-new-tab) guide.

## More interesting topics

* [Customizing components](customizing-components)
* [Adding a route](add-custom-route)

---

---

## Handling media
**Source:** [guides/plugins/plugins/administration/data-handling-processing/handling-media.md](https://developer.shopware.com/docs/v6.6/guides/plugins/plugins/administration/data-handling-processing/handling-media.md)  
# Handling media

## Overview

The Shopware 6 Administration provides many components to work with, when it comes to handle media. For example, imagine you want to provide an opportunity to upload files.
This guide will show you how to use the most important of them.

## The media upload component

The Shopware 6 Administration media upload component makes it relatively easy to upload media of various kinds such as images, videos and audio files.
This is done through the `sw-media-upload-v2` component as seen below:

```html
<div>
    <sw-media-upload-v2
        uploadTag="my-upload-tag"
        :allowMultiSelect="false"
        variant="regular"
        :autoUpload="true"
        label="My image-upload">
    </sw-media-upload-v2>
</div>
```

As you can see in the code sample below, the `sw-media-upload-v2` is pretty configurable through properties.
To get an overview of all the options, here is a list:

| Property           | Function                                                                                                                        |
|--------------------|---------------------------------------------------------------------------------------------------------------------------------|
| `source`           | The source that will be used for the internal `sw-media-preview-v2` if the component is not used in the `allowMultiSelect` mode |
| `variant`          | This can be used to choose between the `regular` and the `compact` variants                                                     |
| `uploadTag`        | This is used to coordinate with the `sw-upload-listener` component                                                              |
| `allowMultiSelect` | Sets whether multiple files can be uploaded at once                                                                             |
| `label`            | The text that is displayed in the header                                                                                        |
| `defaultFolder`    | The path where the file will be put                                                                                             |
| `targetFolderId`   | The `targetFolderId` that will be used as a backup to the `defaultFolder`                                                       |
| `helpText`         | Sets the `helpText` displayed in the header of the component                                                                    |
| `fileAccept`       | Sets what the underlying `<input>`, accepts standard is `image/*`                                                                 |
| `disabled`         | Disables the whole component                                                                                                    |

## Keeping track of uploads

As seen below, the `sw-upload-listener` component can be used in conjunction with an `sw-media-upload-v2` component.

```html
<div>
    <sw-media-upload-v2
        uploadTag="my-upload-tag"
        :allowMultiSelect="false"
        variant="regular"
        label="My image-upload">
    </sw-media-upload-v2>
    <sw-upload-listener
        @media-upload-finish="onUploadFinish" 
        uploadTag="my-upload-tag">
    </sw-upload-listener>
</div>
```

Notice that the `uploadTag` needs to be the same in the `sw-media-upload-v2` and the `sw-upload-listener` for them to communicate properly.
Beyond the `media-upload-finish` event there are a few more events:

| Event                 | Description                                        |
|-----------------------|----------------------------------------------------|
| `media-upload-add`    | This event is triggered when an upload is added    |
| `media-upload-finish` | This event is triggered when an upload finishes    |
| `media-upload-fail`   | This event is triggered on an upload failing       |
| `media-upload-cancel` | This event is triggered when an upload is canceled |

## Previewing Media

Media can be previewed with the `sw-media-preview-v2` component as seen below:

```html
<sw-media-preview-v2
    :source="some-id">
</sw-media-preview-v2>
```

As previously mentioned this component is already embedded within the `sw-media-upload-v2`.
However, using it as a separate component you get access to the following configuration options:

| Property         | Function                                                                      |
|------------------|-------------------------------------------------------------------------------|
| `source`         | The `id` or alternately the path to the media to be previewed                 |
| `showControls`   | Controls whether media such as videos or audio shows controls                 |
| `autoplay`       | Controls whether media such as videos or audio auto-plays                     |
| `hideTooltip`    | Hides the the filename tooltip of the media in at the bottom of the component |
| `mediaIsPrivate` | If set to true displays various lock symbols                                  |

---

---

## Add custom data to the search
**Source:** [guides/plugins/plugins/administration/data-handling-processing/search-custom-data.md](https://developer.shopware.com/docs/v6.6/guides/plugins/plugins/administration/data-handling-processing/search-custom-data.md)  
# Add custom data to the search

## Overview

When developing a customization that has a frequently visited entity listing, you're able to make use of an interesting opportunity: You can enable the user to take a shortcut finding his desired entry using the global search.

There are two different ways how the global search works:

* Global search without type specification
* Typed global search

They only differ in the API they use and get displayed in a slightly different way.

::: warning
Think twice about adding this shortcut because if every plugin adds their own search tag, it gets cluttered.
:::

## Prerequisites

For this guide, it's necessary to have a running Shopware 6 instance and full access to both the files and a running plugin. See our plugin page guide to learn how to create your own plugins.

In addition, you need a custom entity to add to the search to begin with. Head over to the following guide to learn how to achieve that:

## Support custom entity via search API

To support an entity in the untyped global search, the entity has to be defined in one of the Administration Modules.

Add the `entity` and `defaultSearchConfiguration` values to your module to make it available to the search bar component.

```javascript
Shopware.Module.register('swag-plugin', {
    entity: 'swag_example',
    defaultSearchConfiguration: {
        _searchable: true,
        name: {
            _searchable: true,
            _score: 500,
        },
        description: {
            name: {
                _searchable: true,
                _score: 500,
            },
        },
    },
});
```

## Support in the Administration UI

### Add search tag

The search tag displays the entity type used in the typed search and is a clickable button to switch from the untyped to the typed search. To add the tag, a service decorator is used to add a type to the `searchTypeService`:

```javascript
const { Application } = Shopware;

Application.addServiceProviderDecorator('searchTypeService', searchTypeService => {
    searchTypeService.upsertType('foo_bar', {
        entityName: 'foo_bar',
        placeholderSnippet: 'foo-bar.general.placeholderSearchBar',
        listingRoute: 'foo.bar.index',
        hideOnGlobalSearchBar: false,
    });

    return searchTypeService;
});
```

Let's take a closer look at how this decorator is used:

* The key and `entityName` is used as the same to change also existing types.
* This service can be overridden with an own implementation for customization.
* The `placeholderSnippet` is a translation key that is shown when no search term is entered.
* The `listingRoute` is used to show a link to continue the search in the module-specific listing view.
* The `hideOnGlobalSearchBar` is used to determine whether the entity should be searched when searching globally untyped.

### Add the search result item

By default, the search bar does not know how to display the result items, so a current search request will not show any result. In order to declare a search result view the `sw-search-bar-item` template has to be altered as seen below, starting with the template:

```twig
// <plugin root>/src/Resources/app/administration/src/app/component/structure/sw-search-bar-item/sw-search-bar-item.html.twig
{% block sw_search_bar_item_cms_page %}
    {% parent %}

    <router-link v-else-if="type === 'foo_bar'"
                 v-bind:to="{ name: 'foo.bar.detail', params: { id: item.id } }"
                 ref="routerLink"
                 class="sw-search-bar-item__link">
        {% block sw_search_bar_item_foo_bar_label %}
            <span class="sw-search-bar-item__label">
                <sw-highlight-text v-bind:searchTerm="searchTerm"
                                   v-bind:text="item.name">
                </sw-highlight-text>
            </span>
        {% endblock %}
    </router-link>
{% endblock %}
```

Here you see the changes in the `index.js` file:

```javascript
// <plugin root>/src/Resources/app/administration/src/main.js

Shopware.Component.override('sw-search-bar-item', () => import('./app/component/structure/sw-search-bar-item'));
```

```javascript
// <plugin root>/src/Resources/app/administration/src/app/component/structure/sw-search-bar-item/index.js
import template from './sw-search-bar-item.html.twig';

export default {
    template
};
```

The `sw_search_bar_item_cms_page` block is used as it is the last block, but it is not important which shopware type is extended as long as the vue else-if structure is kept working.

### Add custom show more results link

By default, the search bar tries to resolve to the registered listing route. If your entity can be searched externally you can edit the `sw-search-more-results` or `sw-search` components as well:

```twig
// <plugin root>/src/Resources/app/administration/src/app/component/structure/sw-search-more-results/sw-search-more-results.html.twig
{% block sw_search_more_results %}
    <template v-if="result.entity === 'foo_bar'">
        There are so many hits.
        <a :href="'https://my.erp.localhost/?q=' + searchTerm"
           class="sw-search-bar-item__link"
           target="_blank">
             Look it directly up
        </a>
        in the ERP instead.
    </template>
    <template v-else>
        {% parent %}
    </template>
{% endblock %}
```

See for the changes in the `index.js` file below:

```javascript
// <plugin root>/src/Resources/app/administration/src/main.js

Shopware.Component.override('sw-search-more-results', () => import('./app/component/structure/sw-search-more-results'));
```

```javascript
// <plugin root>/src/Resources/app/administration/src/app/component/structure/sw-search-more-results/index.js
import template from './sw-search-more-results.html.twig';

export default {
    template
};
```

### Potential pitfalls

In case of a tag with a technical name with a missing translation, proceed like this:

```json
{
    "global": {
        "entities": {
            "my_entity": "My entity | My entities"
        }
    }
}
```

To change the color of the tag, or the icon in the untyped global search, a module has to be registered with an entity reference in the module:

```javascript
Shopware.Module.register('any-name', {
    color: '#ff0000',
    icon: 'default-basic-shape-triangle',
    entity: 'my_entity',
})
```

---

---

## The Shopware object
**Source:** [guides/plugins/plugins/administration/data-handling-processing/the-shopware-object.md](https://developer.shopware.com/docs/v6.6/guides/plugins/plugins/administration/data-handling-processing/the-shopware-object.md)  
# The Shopware object

## Overview

The global `Shopware` object is the bridge between the Shopware Administration and your plugin as third party code. It provides utility functions to interface to the rest of the Administration.

::: warning
Don't try to access other parts of the Administration directly, always use the `Shopware` object.
:::

It is bound to a window object in order to be accessible everywhere and can therefore be inspected with the browser console in the developer tools. To take a look at it, open the `Administration` in your browser and run this in the dev-tools console:

```javascript
// run this command in the dev-tools of your browser
console.log(Shopware);
```

There are lots of things bound to this object. So here is a short overview of the most commonly used parts.

## Component

The `Component` property of the global `Shopware` contains the component registry, which is responsible for handling the VueJS components. If you want to write your own components you have to register them with the `Component.register()` method. Those components are small reusable building blocks which you can use to implement your features.

```javascript
const { Component } = Shopware;

Component.register('sw-dashboard-index', {
    template,
});
```

Learn more about them here: [Creating administration component](../module-component-management/add-custom-component.md)

## Module

The `Module` property of the global `Shopware` contains the module registry. A `Module` is an encapsulated unit of routes and pages, which implements a whole feature. For example there are modules for customers, orders, settings, etc.

```javascript
const { Module } = Shopware;

Module.register('your-module', {});
```

Learn more about them here: [Creating administration module](../module-component-management/add-custom-module.md)

## A more general overview

We now have discussed the most commonly used parts of the `Shopware` object, but there is much more to discover. Take a look at all these options in a brief overview below:

| Property   | Description                                                                                 |
| :--------- | :------------------------------------------------------------------------------------------ |
| ApiService | Registry which holds services to fetch data from the api                                    |
| Component  | A registry for VueJS `components`                                                           |
| Context    | A set of contexts for the `app` and the `api`                                               |
| Defaults   | A collection of default values                                                              |
| Directive  | A registry for [VueJS `directives`](https://vuejs.org/v2/guide/custom-directive.html)       |
| Filter     | A registry for [VueJS template `filters`](https://vuejs.org/v2/guide/filters.html)          |
| Helper     | A collection of helpers, e.g. the `DeviceHelper` where you can listen on the `resize` event |
| Locale     | A registry for `locales`                                                                    |
| Mixin      | A registry for `mixins`                                                                     |
| Module     | A registry for `modules`                                                                    |
| Plugin     | An interface to add `promise`based hooks to run when the Administration launches            |
| Service    | A helper to get quick access to service, e.g. `Shopware.Service('snippetService')`          |
| Shortcut   | A registry for keyboard shortcuts                                                           |
| State      | A wrapper for the [VueX](https://vuex.vuejs.org/) store to manage state                     |
| Utils      | A collection of utility methods like `createId`                                             |

## TypeScript declarations

::: info
TypeScript declarations are available from Shopware Version 6.4.4.0
:::

The Shopware Administration is written in pure JavaScript. To provide you with the benefits of TypeScript and the best possible developer experience while working in JavaScript files we're providing TypeScript declaration files within the Administration. These files are helping you to understand how the Shopware object works and what arguments you have to provide for example when you're creating a new module or registering a new component.

![TypeScript declarations example](../../../../../assets/typescript-declaration-shopware-module.gif)

In the example above you can see how the TypeScript declarations are helping you to register a module. It automatically marks your code and points out what is missing.

## Next steps

As you might have noticed, the `Shopware` object can be used in a lot of cases. Besides registering components and modules, here are some guides about [adding filters](../services-utilities/add-filter.md), about [adding mixins](../mixins-directives/add-mixins.md) and about [using our utils](../services-utilities/using-utils.md) - all by using the Shopware object.

---

---

## Using custom fields
**Source:** [guides/plugins/plugins/administration/data-handling-processing/using-custom-fields.md](https://developer.shopware.com/docs/v6.6/guides/plugins/plugins/administration/data-handling-processing/using-custom-fields.md)  
# Using custom fields

## Prerequisites

All you need for this guide is a running Shopware 6 instance, the files and preferably a registered module in your own plugin. Don't know how to create an own plugin yet? Head over to the following guide:

In order to craft your module, you will need to create lots on own components. If you're not sure about how to do that, take a look at the corresponding guide:

In addition, of course you need an entity with custom fields to be able to add those custom fields to your module to begin with. Here you can learn how to add your custom fields:

## Using custom fields in your module

In Shopware, we provide an own component called `sw-custom-field-set-renderer` for your template, being tailored specifically to display custom field sets.

As a consequence, you're able to use this component to display your custom fields. See here:

```html
// <plugin-root>/src/Resources/app/administration/app/src/component/swag-basic-example/swag-basic-example.html.twig
<sw-card title="Custom fields">
    <sw-custom-field-set-renderer
        :entity="customEntity"
        showCustomFieldSetSelection
        :sets="sets">
    </sw-custom-field-set-renderer>
</sw-card>
```

For further details on the `sw-custom-field-set-renderer` component, feel free to refer to its page in our component library:

The next step is loading your custom fields. First things first, create a variable for your custom fields in `data`:

```javascript
// <plugin-root>/src/Resources/app/administration/app/src/component/swag-basic-example/index.js
    data() {
        return {
            ...
            customFieldSets: null
        };
    }
```

Afterwards, you can start to integrate the custom field data into your component. Therefore, you need to create a `customFieldSetRepository` first as `computed` property. In this context, it may come in handy to already set the `customFieldSetCriteria`. Both steps can be seen in the example below:

```javascript
// <plugin-root>/src/Resources/app/administration/app/src/component/swag-basic-example/index.js
computed: {
    // Using the repository to work with customFields
    customFieldSetRepository() {
        return this.repositoryFactory.create('custom_field_set');
    },

    // sets the criteria used for your custom field set
    customFieldSetCriteria() {
        const criteria = new Criteria();

        // restrict the customFieldSets to be associated with products
        criteria.addFilter(Criteria.equals('relations.entityName', 'product'));

        // sort the customFields based on customFieldPosition
        criteria
            .getAssociation('customFields')
            .addSorting(Criteria.sort('config.customFieldPosition', 'ASC', true));

        return criteria;
    }
}
```

Now you can access your custom fields, e.g. within a `method`. In order to achieve that, you can use the `search` method as you're used to working with repositories:

```javascript
    // this will fetch the customFieldSets
    this.customFieldSetRepository.search(this.customFieldSetCriteria, Shopware.Context.api)
        .then((customFieldSets) => {
            this.customFieldSets = customFieldSets;
        });
```

---

---

## Using the data handling
**Source:** [guides/plugins/plugins/administration/data-handling-processing/using-data-handling.md](https://developer.shopware.com/docs/v6.6/guides/plugins/plugins/administration/data-handling-processing/using-data-handling.md)  
*(Body truncated in this bundle; follow the link for the rest.)*

# Using the data handling

The Shopware 6 Administration allows you to fetch and write nearly everything in the database. This guide will teach you the basics of the data handling.

## Prerequisites

All you need for this guide is a running Shopware 6 instance and full access to both the files, as well as the command line and preferably registered module. Of course you'll have to understand JavaScript, but that's a prerequisite for Shopware as a whole and will not be taught as part of this documentation.

Considering that the data handling in the Administration is remotely operating the Data Abstraction Layer its highly encouraged to read the articles [Reading data with the DAL](../../../../../guides/plugins/plugins/framework/data-handling/reading-data.md) and [Writing data with the DAL](../../../../../guides/plugins/plugins/framework/data-handling/writing-data.md).

## Relevant classes

`Repository`: Allows to send requests to the server - used for all CRUD operations `Entity`: Object for a single storage record `EntityCollection`: Enable object-oriented access to a collection of entities `SearchResult`: Contains all information available through a search request `RepositoryFactory`: Allows to create a repository for an entity `Context`: Contains the global state of the Administration (language, version, auth, ...) `Criteria`: Contains all information for a search request (filter, sorting, pagination, ...)

## The repository service

Accessing the Shopware API in the Administration is done by using the repository service, which can be injected with a [bottleJs](https://github.com/young-steveo/bottlejs) dependency injection container. In the Shopware Administration, there's a wrapper that makes `bottleJs` work with the [inject / provide](https://vuejs.org/v2/api/#provide-inject) from [`Vue`](https://vuejs.org/). In short: You can use the `inject` key in your component configuration to fetch services from the `bottleJs` DI container, such as the `repositoryFactory`, that you will need in order to get a repository for a single entity.

Add those lines to your component configuration:

```javascript
inject: [
    'repositoryFactory'
],
```

This way the `repositoryFactory` object is accessible in your component. The `create` function can be used to create a repository for a single entity, like in this example:

```javascript
const productRepository = this.repositoryFactory.create('product')
```

Note: You can also change some options in the repository, with the third parameter:

```javascript
Component.register('swag-basic-example', {
    inject: ['repositoryFactory'],

    template,

    data: function () {
        return {
            repository: undefined
        }
    },

    created() {
        const options = {
            version: 1 // default is the latest api version
        };

        this.repository = this.repositoryFactory.create('product', null, options);
    }
});
```

Note: The version 1 used in the options is just an example, how to select a version. Then again the default would be the newest version. There are no other options.

## Working with the criteria class

To fetch data from the server, the repository has a `search` function. Each repository function requires the API `context` and `criteria` class, which contains all functionality of the core criteria class. If you want to see all the options take a look at the file [src/Administration/Resources/app/administration/src/core/data/criteria.data.ts](https://github.com/shopware/meteor/blob/main/packages/admin-sdk/src/data/Criteria.ts).

```javascript
const { Criteria } = Shopware.Data;
Shopware.Component.register('swag-basic-example', {
    inject: ['repositoryFactory'],

    template,

    data: function () {
        return {
            result: undefined
        }
    },

    computed: {
        productRepository() {
            // create a repository for the `product` entity
            return this.repositoryFactory.create('product');
        },
    },

    created() {
        const criteria = new Criteria();

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

        this.productRepository.create('product');

        this.productRepository
            .search(criteria, Shopware.Context.api)
            .then(result => {
                this.result = result;
            });
    }
});
```

## How to fetch a single entity

Since the context of an edit or update form is usually a single root entity, the data handling diverges here from the Data Abstraction Layer and provides loading of a single resource from the Admin API.

```javascript
Shopware.Component.register('swag-basic-example', {
    inject: ['repositoryFactory'],

    template,

    data: function () {
        return {
            entity: undefined
        }
    },
    computed: {
        productRepository() {
            return this.repositoryFactory.create('product');
        }
    },

    created() {
        const entityId = 'some-id';

        this.productRepository
            .get(entityId, Shopware.Context.api)
            .then(entity => {
                this.entity = entity;
            });
    }
});
```

## Update an entity

The data handling contains change tracking and sends only changed properties to the Admin API endpoint. Please be aware that in order to be as transparent as possible, updating data will not be handled automatically. A manual update is mandatory.

```javascript
Shopware.Component.register('swag-basic-example', {
    inject: ['repositoryFactory'],

    template,

    data: function () {
        return {
            entityId: '1de38487abf04705810b719d4c3e8faa',
            entity: undefined
        }
    },

    computed: {
        productRepository() {
            return this.repositoryFactory.create('product');
        }
    },

    created() {
        this.productRepository
            .get(this.entityId, Shopware.Context.api)
            .then(entity => {
                this.entity = entity;
            });
    },

    methods: {
        // a function which is called over the ui
        updateTrigger() {
            this.entity.name = 'updated';

            // sends the request immediately
            this.productRepository
                .save(this.entity, Shopware.Context.api)
                .then(() => {
                    // the entity is stateless, the data has be fetched from the server, if required
                    this.productRepository
                        .get(this.entityId, Shopware.Context.api)
                        .then(entity => {
                            this.entity = entity;
                        });
                });
        }
    }
});
```

## Delete an entity

The `delete` method sends a `delete` request for a provided id. To delete multiple entities at once use the `syncDeleted` method by passing an array of `ids`.

```javascript
Shopware.Component.register('swag-basic-example', {
    inject: ['repositoryFactory'],

    template,

    computed: {
        productRepository() {
            return this.repositoryFactory.create('product');
        }
    },

    created() {
        this.productRepository.delete('1de38487abf04705810b719d4c3e8faa', Shopware.Context.api);
    }
});
```

## Create an entity

Although entities are detached from the data handling once retrieved or created they still must be set up through a repository. You can create an entity by using the `this.repositoryFactory.create()` method, fill it with data and save it as seen below:

```javascript
Shopware.Component.register('swag-basic-example', {
    inject: ['repositoryFactory'],

    template,

    data: function () {
        return {
            entity: undefined
        }
    },

    computed: {
        manufacturerRepository() {
            return this.repositoryFactory.create('product_manufacturer');
        }
    },

    created() {
        this.entity = this.manufacturerRepository.create(Shopware.Context.api);

        this.entity.name = 'test';

        this.manufacturerRepository.save(this.entity, Shopware.Context.api);
    }
});
```

## Working with associations

Each association can be accessed via normal property access:

```javascript
const { Criteria } = Shopware.Data;
Shopware.Component.register('swag-basic-example', {
    inject: ['repositoryFactory'],

    template,

    data: function () {
        return {
            product: undefined
        }
    },

    computed: {
        productRepository() {
            return this.repositoryFactory.create('product');
        },
        productCriteria() {
            return new Criteria()
                .addAssociation('manufacturer')
                .addAssociation('categories')
                .addAssociation('prices');
        }
    },

    created() {
        this.repository = this.repositoryFactory.create('product');

        const entityId = '66338d4e19f749fd90b59032134ecb74';

        this.repository
            .get(entityId, Shopware.Context.api, this.productCriteria)
            .then(product => {
                this.product = product;

                // ManyToOne: contains an entity class with the manufacturer data
                console.log(this.product.manufacturer);

                // ManyToMany: contains an entity collection with all categories.
                // contains a source property with an api route to reload this data (/product/{id}/categories)
                console.log(this.product.categories);

                // OneToMany: contains an entity collection with all prices
                // contains a source property with an api route to reload this data (/product/{id}/prices)            
                console.log(this.product.prices);
            });
    }
});
```

### Set a ManyToOne

If you have a ManyToOne association, you can write changes as seen below:

```javascript
Shopware.Component.register('swag-basic-example', {
    inject: ['repositoryFactory'],

    template,

    data: function () {
        return {
            product: undefined,
        };
    },

    computed: {

        productRepository() {
            return this.repositoryFactory.create('product');
        },
        manufacturerRepository() {
            return this.repositoryFactory.create('product_manufacturer');
        }
    },

    created() {
        this.productRepository
            .get('some-product-id', Shopware.Context.api)
            .then((product) => {
                this.product = product;

                this.product.manufacturerId = 'some-manufacturer-id'; // manually set the foreign key y

                this.productRepository.save(this.product, Shopware.Context.api);
            });
    },
});
```

### Working with lazy loaded associations

In most cases, *ToMany* associations can be loaded by adding a the association with the `.addAssociation()` method of the Criteria object.

```javascript
const { Criteria } = Shopware.Data;
Shopware.Component.register('swag-basic-example', {
    inject: ['repositoryFactory'],

    template,

    

… **Truncated.** Full document: https://developer.shopware.com/docs/v6.6/guides/plugins/plugins/administration/data-handling-processing/using-data-handling.md


---

## Using the data grid component
**Source:** [guides/plugins/plugins/administration/data-handling-processing/using-the-data-grid-component.md](https://developer.shopware.com/docs/v6.6/guides/plugins/plugins/administration/data-handling-processing/using-the-data-grid-component.md)  
# Using the data grid component

## Overview

The data grid component makes it easy to render tables with data. It also supports hiding columns or scrolling horizontally when many columns are present. This guide shows you how to use it.

## Prerequisites

All you need for this guide is a running Shopware 6 instance and full access to both the files, as well as the command line and preferably registered module. Of course you'll have to understand JavaScript, but that's a prerequisite for Shopware as a whole and will not be taught as part of this documentation.

## Creating a template for the data grid component

Let's create the simplest template we need in order to use the [`sw-data-grid`](https://github.com/shopware/shopware/blob/v6.3.4.1/src/Administration/Resources/app/administration/src/app/component/data-grid/sw-data-grid/index.js).

```html
// <plugin-root>/src/Resources/app/administration/app/src/component/swag-example/swag-example.html.twig
<div>
    <sw-data-grid :data-source="dataSource" :columns="columns">
    </sw-data-grid>
</div>
```

This template will be used in a new component. Learn how to override existing components [here](../module-component-management/customizing-components.md) .

## Declaring the data

Since this is a very basic example the following code will just statically assign data to the `dataSource` and `columns` data attribute. If you want to load data and render that instead, please consult the guide [How to use the data handling](using-data-handling.md)

```javascript
// <plugin-root>/src/Resources/app/administration/app/src/component/swag-example/index.js
import template from 'swag-example.html.twig';

Shopware.Component.register('swag-basic-example', {
    template,

    data: function () {
        return {
            dataSource: [
                { id: 'uuid1', company: 'Wordify', name: 'Portia Jobson' },
                { id: 'uuid2', company: 'Twitternation', name: 'Baxy Eardley' },
                { id: 'uuid3', company: 'Skidoo', name: 'Arturo Staker' },
                { id: 'uuid4', company: 'Meetz', name: 'Dalston Top' },
                { id: 'uuid5', company: 'Photojam', name: 'Neddy Jensen' }
            ],
            columns: [
                { property: 'name', label: 'Name' },
                { property: 'company', label: 'Company' }
            ],
        };
    }
});
```

## More interesting topics

* [Using base components](../module-component-management/using-base-components.md)

---

---

## Using Vuex Stores
**Source:** [guides/plugins/plugins/administration/data-handling-processing/using-vuex-state.md](https://developer.shopware.com/docs/v6.6/guides/plugins/plugins/administration/data-handling-processing/using-vuex-state.md)  
# Using Vuex Stores

## Overview

The Shopware 6 Administration uses [Vuex](https://vuex.vuejs.org/) stores to keep track of complex state, while just adding a wrapper around it.
Learn what Vuex is, how to use it and when to use it from their great [documentation](https://vuex.vuejs.org/).
This guide will show you how to use Vuex as you normally would, through the interfaces provided by the Shopware 6 Administration.

## Prerequisites

All you need for this guide is a running Shopware 6 instance, the files and preferably a registered module.
Of course, you'll have to understand JavaScript and have a basic familiarity with [Vue](https://vuejs.org/) the framework used in the Administration, and it's flux library [Vuex](https://vuex.vuejs.org/).

## Creating a store

Creating a store works the same way as it would in standard Vuex with the only limitation being,
that all stores have to be `namespaced` in order to prevent collisions with other third party plugins or the Shopware 6 Administration itself.

The following code snippet is the `namespaced` store we will register later through Shopware to the underlying Vuex.
It is admittedly rather short and has only one variable called `content` and a setter for it, but again this all the same as in Vuex.
Beware of the property `namespaced`, though.

::: code-group

```javascript [PLUGIN_ROOT/src/Resources/app/administration/app/src/component/store-example/store.js]

export default {
    namespaced: true,

    state() {
        return {
            // the state we want to keep track of
            content: ''
        };
    },

    mutations: {
        // a mutation to change the state
        setContent(state, content) {
            state.content = content;
        },
    }
};
```

:::

## Registering the store

The store can be registered in two scopes, on a module scope and on a per component scope.
Both ways use the same functions from the [Shopware object](./the-shopware-object.md) to register and unregister the `namespaced store modules`.

Registering in a module scope is done by simply calling the function `Shopware.State.registerModule` in the `main.js` file.

::: code-group

```javascript [ADMINISTRATION_ROOT/src/main.js]
import swagBasicState from './store';

Shopware.State.registerModule('swagBasicState', swagBasicState);
```

:::

In the component scope `Namespaced` store modules can be registered in the `beforeCreate` [Vue lifecycle hook](https://vuejs.org/v2/guide/instance.html#Lifecycle-Diagram),
with the previously mentioned `Shopware.State.registerModule` function.
But then they also need to be `unregistered` in the `beforeDestroy` Vue lifecycle hook,
in order to not leave unused stores behind after a component has been destroyed.

All of this can be seen in the following code sample:

::: code-group

```javascript [PLUGIN_ROOT/src/Resources/app/administration/app/src/component/store-example/index.js]
    beforeCreate() {
        // registering the store to vuex through the Shopware objects helper function
        // the first argument is the name the second the imported namespaced store
        Shopware.State.registerModule('swagBasicState', swagBasicState);
    },

    beforeDestroy() {
        // unregister the store before the component is destroyed
        Shopware.State.unregisterModule('swagBasicState');
    },
```

:::

Both methods make the store on the given name everywhere available, regardless of where it has been registered.

## Using the store in a component

The Shopware object also makes the native Vuex helper functions available, like [`mapState`](https://vuex.vuejs.org/guide/state.html#the-mapstate-helper), [`mapGetters`](https://vuex.vuejs.org/guide/getters.html#the-mapgetters-helper), [`mapMutations`](https://vuex.vuejs.org/guide/mutations.html#committing-mutations-in-components) and [`mapActions`](https://vuex.vuejs.org/guide/actions.html#dispatching-actions-in-components).
The `namespaced` store itself can be accessed through the `Shopware.State.get()` function.

::: code-group

```javascript [PLUGIN_ROOT/src/Resources/app/administration/app/src/component/store-example/index.js]
// import the template
import template from './store-example.html.twig';

const { Component } = Shopware;

// Access the normal Vuex helper functions through the Shopware Object
const { 
    mapState,
    mapMutations,
} = Shopware.Component.getComponentHelper();

Component.register('swag-basic-state', {
    template,

    computed: {
        // the native mapState vuex helper function 
        ...mapState('swagBasicState', [
            'content',
        ])
    },

    methods: {
        // the native mapMutations vuex helper function
        ...mapMutations('swagBasicState', [
            'setContent',
        ]),
    }
});
```

:::

## Adding a template

After we have registered our `namespaced` store, mapped state and mutations, we can now use them in our components or templates.
The component below displays the previously mapped state `content` in a `div` and a `sw-text-field`, mutating the state on the `changed` event of the `sw-text-field`.

::: code-group

```html [PLUGIN_ROOT/src/Resources/app/administration/app/src/component/store-example/store-example.html.twig]
<div>
    <h1>SW-6 State</h1>
    <sw-text-field
            :value="content"
            @update:value="value => setContent(value)">
    </sw-text-field>
    <div>
        {{ content }}
    </div>
</div>
```

:::

## More interesting topics

* [The Shopware object](./the-shopware-object.md)

---

---

## Extending services
**Source:** [guides/plugins/plugins/administration/extending-services.md](https://developer.shopware.com/docs/v6.5/guides/plugins/plugins/administration/extending-services.md)  
# Extending services

## Overview

This guide will teach you how to extend a Shopware provided service with middleware and decorators.
The Shopware 6 Administration uses [BottleJS](https://github.com/young-steveo/bottlejs) to provide the framework for services.
If you want to learn how to create your own services, look at [this guide](./add-custom-service).

## Prerequisites

All you need for this guide is a running Shopware 6 instance and full access to both the files and a running plugin. Of course you'll have to understand JavaScript, but that's a prerequisite for Shopware as a whole and will not be taught as part of this documentation.

## Reset Providers

The [`resetProviders`](https://github.com/young-steveo/bottlejs#resetprovidersnames) function is used to reset providers for the next reference to re-instantiate the provider.
You need to do this to add decorators or middleware to Shopware provided services, after they are initially instantiated in the Shopware boot-process.

```javascript
Shopware.Application.$container.resetProviders()
```

If the `names` param is passed, it will only reset the named providers.

## Adding decorators

[BottleJS decorators](https://github.com/young-steveo/bottlejs#decorators) are just simple functions that intercept a service in the provider phase after it has been created, but before it is accessed for the first time.
The function should return the service or another object to be used as the service instead.

With Shopware you have to reset the providers before extending Service.

Let's look at an example:

```javascript
Shopware.Application.$container.resetProviders(['acl']);

Shopware.Application.addServiceProviderDecorator('acl', (aclService) => {
  aclService.foo = 'bar';
  console.log(aclService);
  return aclService;
});
```

## Adding middleware

[BottleJS middleware](https://github.com/young-steveo/bottlejs#middleware) are similar to decorators, but they are executed every time a service is accessed from the container.
They are passed the service instance and a `next` function:

As mentioned before with Shopware you have to reset the providers, before extending Service.

Let's look at an Example:

```javascript
Shopware.Application.$container.resetProviders(['acl']);

Shopware.Application.addServiceProviderMiddleware('acl', (service, next) => {
    console.log('ACL service gets called');
    next();
});
```

---

---

## Extending Webpack
**Source:** [guides/plugins/plugins/administration/extending-webpack.md](https://developer.shopware.com/docs/v6.5/guides/plugins/plugins/administration/extending-webpack.md)  
# Extending Webpack

## Overview

The Shopware 6 Administration uses [Webpack](https://webpack.js.org/) as a static module bundler. Normally you don't need to change the Webpack configuration, but if you need to here is how to do it.

## Extending the Webpack configuration

The Webpack configuration can be extended by creating the file `<plugin root>/src/Resources/app/administration/build/webpack.config.js` and exporting a function from it. This will return a [webpack configuration object](https://webpack.js.org/configuration/), as seen below:

```javascript
// <plugin root>/src/Resources/app/administration/build/webpack.config.js
const path = require('path');

module.exports = () => {
    return {
        resolve: {
            alias: {
                SwagBasicExample: path.join(__dirname, '..', 'src')
            }
        }
    };
};
```

This way, the configuration is automatically loaded and then merged with the Shopware provided webpack configuration. Configurations of plugins are **not** merged into each other. Merging is done with the [webpackMerge](https://github.com/survivejs/webpack-merge) library.

---

---

## Handling media
**Source:** [guides/plugins/plugins/administration/handling-media.md](https://developer.shopware.com/docs/v6.5/guides/plugins/plugins/administration/handling-media.md)  
# Handling media

## Overview

The Shopware 6 Administration provides many components to work with, when it comes to handle media. For example, imagine you want to provide an opportunity to upload files.
This guide will show you how to use the most important of them.

## The media upload component

The Shopware 6 Administration media upload component makes it relatively easy to upload media of various kinds such as images, videos and audio files.
This is done through the `sw-media-upload-v2` component as seen below:

```html
<div>
    <sw-media-upload-v2
        uploadTag="my-upload-tag"
        :allowMultiSelect="false"
        variant="regular"
        :autoUpload="true"
        label="My image-upload">
    </sw-media-upload-v2>
</div>
```

As you can see in the code sample below, the `sw-media-upload-v2` is pretty configurable through properties.
To get an overview of all the options, here is a list:

| Property           | Function                                                                                                                        |
|--------------------|---------------------------------------------------------------------------------------------------------------------------------|
| `source`           | The source that will be used for the internal `sw-media-preview-v2` if the component is not used in the `allowMultiSelect` mode |
| `variant`          | This can be used to choose between the `regular` and the `compact` variants                                                     |
| `uploadTag`        | This is used to coordinate with the `sw-upload-listener` component                                                              |
| `allowMultiSelect` | Sets whether multiple files can be uploaded at once                                                                             |
| `label`            | The text that is displayed in the header                                                                                        |
| `defaultFolder`    | The path where the file will be put                                                                                             |
| `targetFolderId`   | The `targetFolderId` that will be used as a backup to the `defaultFolder`                                                       |
| `helpText`         | Sets the `helpText` displayed in the header of the component                                                                    |
| `fileAccept`       | Sets what the underlying , accepts standard is `image/*`                                                                 |
| `disabled`         | Disables the whole component                                                                                                    |

## Keeping track of uploads

As seen below, the `sw-upload-listener` component can be used in conjunction with an `sw-media-upload-v2` component.

```html
<div>
    <sw-media-upload-v2
        uploadTag="my-upload-tag"
        :allowMultiSelect="false"
        variant="regular"
        label="My image-upload">
    </sw-media-upload-v2>
    <sw-upload-listener
        @media-upload-finish="onUploadFinish" 
        uploadTag="my-upload-tag">
    </sw-upload-listener>
</div>
```

Notice that the `uploadTag` needs to be the same in the `sw-media-upload-v2` and the `sw-upload-listener` for them to communicate properly.
Beyond the `media-upload-finish` event there are a few more events:

| Event                 | Description                                        |
|-----------------------|----------------------------------------------------|
| `media-upload-add`    | This event is triggered when an upload is added    |
| `media-upload-finish` | This event is triggered when an upload finishes    |
| `media-upload-fail`   | This event is triggered on an upload failing       |
| `media-upload-cancel` | This event is triggered when an upload is canceled |

## Previewing Media

Media can be previewed with the `sw-media-preview-v2` component as seen below:

```html
<sw-media-preview-v2
    :source="some-id">
</sw-media-preview-v2>
```

As previously mentioned this component is already embedded within the `sw-media-upload-v2`.
However, using it as a separate component you get access to the following configuration options:

| Property         | Function                                                                      |
|------------------|-------------------------------------------------------------------------------|
| `source`         | The `id` or alternately the path to the media to be previewed                 |
| `showControls`   | Controls whether media such as videos or audio shows controls                 |
| `autoplay`       | Controls whether media such as videos or audio auto-plays                     |
| `hideTooltip`    | Hides the the filename tooltip of the media in at the bottom of the component |
| `mediaIsPrivate` | If set to true displays various lock symbols                                  |

---

---

## Injecting services
**Source:** [guides/plugins/plugins/administration/injecting-services.md](https://developer.shopware.com/docs/v6.5/guides/plugins/plugins/administration/injecting-services.md)  
# Injecting services

## Overview

This short guide will teach you how to use a service in the Shopware 6 Administration.

Along these lines, this chapter will cover the following topics:

* What is an Administration service?
* How to use a service?

## Prerequisites

All you need for this guide is a running Shopware 6 instance and full access to both the files and a running plugin.
Of course you'll have to understand JavaScript, but that's a prerequisite for Shopware as a whole and will not be taught as part of this documentation.

## Definition of an Administration service

Shopware 6 uses [bottleJS](https://github.com/young-steveo/bottlejs) to inject services.
Services are small self-contained utility classes, like the [repositoryFactory](https://github.com/shopware/shopware/blob/v6.3.4.1/src/Administration/Resources/app/administration/src/core/data-new/repository-factory.data.js), which provides a way to talk to the API.

## Injection of a service

A service is typically injected into a vue component and can simply be referenced in the `inject` property.
This service is then available via its name on the object instance.

```javascript
Shopware.Component.register('swag-basic-example', {
    // inject the service
    inject: ['repositoryFactory'],

    created() {
        // insatiate the injected repositoryFactory 
        this.productRepository = this.repositoryFactory.create('product')
    }
});
```

---

---

## Adding Mixins
**Source:** [guides/plugins/plugins/administration/mixins-directives/add-mixins.md](https://developer.shopware.com/docs/v6.6/guides/plugins/plugins/administration/mixins-directives/add-mixins.md)  
# Adding Mixins

## Overview

This documentation chapter will cover how to add a new Administration mixin for your plugin. In general, mixins behave the same as they do in Vue normally, differing only in the registration and the way mixins are included in a component. If you want an overview over the shopware provided mixins look at them here: [Using Mixins](using-mixins.md).

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

This can also be done with Shopware provided mixins, learn more about them here: [Using Mixins](using-mixins.md)

## More interesting topics

* [Adding filters](../services-utilities/add-filter.md)
* [Using utility functions](../services-utilities/using-utils.md)

---

---

## Using Directives
**Source:** [guides/plugins/plugins/administration/mixins-directives/adding-directives.md](https://developer.shopware.com/docs/v6.6/guides/plugins/plugins/administration/mixins-directives/adding-directives.md)  
# Using Directives

## Overview

Directives in the Shopware 6 Administration are essentially the same as in any other Vue application. This guide will teach you how to register your directives on a global and on a local scope.

Learn more about Vue Directives in their documentation:

## Prerequisites

All you need for this guide is a running Shopware 6 instance and full access to both the files and preferably a registered module. Of course, you'll have to understand JavaScript, but that's a prerequisite for Shopware as a whole and will not be taught as part of this documentation.

## Registering a directives globally

Directives can be registered globally via the [Shopware Objects](../data-handling-processing/the-shopware-object.md) `register` helper function as seen below:

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

## Using Mixins
**Source:** [guides/plugins/plugins/administration/mixins-directives/using-mixins.md](https://developer.shopware.com/docs/v6.6/guides/plugins/plugins/administration/mixins-directives/using-mixins.md)  
# Using Mixins

## Overview

This documentation chapter will cover how to use an existing Administration mixin in your plugin. Generally, mixins behave the same as they do in Vue normally, differing only in the registration and the way mixins are included in a component.

## Prerequisites

All you need for this guide is a running Shopware 6 instance and full access to both the files and a running plugin. Of course you'll have to understand JavaScript, but that's a prerequisite for Shopware as a whole and will not be taught as part of this documentation. As stated before mixins in Shopware are basically the same as in Vue, so you should have read their [documentation](https://vuejs.org/v2/guide/mixins.html) on them first.

## Finding a mixin

The Shopware 6 Administration comes with a few predefined [mixins](../../../../../resources/references/administration-reference/mixins.md)

If you want to learn how to create your own mixin look at this guide: [Creating mixins](add-mixins.md)

## Using the Mixin

After we've found the mixin we need, we can get it from the registry with the `Mixin.getByName` function and inject it into our component as seen below. In this example we'll use the notification mixin, which is useful for creating notifications visible to the user in the Administration.

```javascript
// <administration root>/components/swag-basic-example/index.js
const { Component, Mixin } = Shopware;

Component.register('swag-basic-example', {

    mixins: [
        Mixin.getByName('notification')
    ],

    methods: {
        greet: function () {
            this.createNotificationSuccess({ title: 'Greetings' })
        }
    }
});
```

---

---

## Modify dynamic product groups blacklist
**Source:** [guides/plugins/plugins/administration/modify-blacklist-for-dynamic-product-groups.md](https://developer.shopware.com/docs/v6.5/guides/plugins/plugins/administration/modify-blacklist-for-dynamic-product-groups.md)  
# Modify dynamic product groups blacklist

## Overview

The module "Dynamic product groups" includes a condition builder to properly configure your dynamic product groups.
You might have noticed though, that this condition builder does not show all available properties,
since some of them are blacklisted in the code, such as e.g. `createdAt`.

In this guide you'll get two quick examples on how to either add new properties to this blacklist or even remove
properties from the blacklist, so they're actually shown in the Administration and thus can be used.

## Prerequisites

This guide **will not** explain in detail how to override an existing component.
For this guide you'll have to extend the component [sw-product-stream-field-select](https://github.com/shopware/shopware/blob/v6.3.4.1/src/Administration/Resources/app/administration/src/module/sw-product-stream/component/sw-product-stream-field-select/index.js) though, since it's the one [actually checking for the properties in the computed property options](https://github.com/shopware/shopware/blob/v6.3.4.1/src/Administration/Resources/app/administration/src/module/sw-product-stream/component/sw-product-stream-field-select/index.js#L41).

An example on how to override a component can be found [here](./customizing-components).

## Adding properties to blacklist

As already mentioned in the prerequisites, the check for properties in the blacklist is done in the computed property `options`.
Therefore you'll have to make sure your modifications are done **before** the check happens.

```javascript
// <plugin-root>/src/Resources/app/administration/app/src/component/sw-product-stream-field-select/index.js
const { Component } = Shopware;

Component.override('sw-product-stream-field-select', {
    computed: {
        options() {
            this.conditionDataProviderService.addToGeneralBlacklist(['deliveryTimeId']);
            return this.$super('options');
        }
    }
});
```

This example will simply add the property `deliveryTimeId` to the blacklist, so it's not configurable using the Administration anymore.
There are also nested properties, so called 'entity properties', which are selectable once you've chosen a property such as `Categories`.
Those entity properties can also be added to the blacklist by using the method `addToEntityBlacklist` instead:

```javascript
// <plugin-root>/src/Resources/app/administration/app/src/component/sw-product-stream-field-select/index.js
const { Component } = Shopware;

Component.override('sw-product-stream-field-select', {
    computed: {
        options() {
            this.conditionDataProviderService.addToEntityBlacklist('category', ['breadcrumb']);
            return this.$super('options');
        }
    }
});
```

This example would forbid the usage of `breadcrumb` from the `category` entity.

## Removing properties from the blacklist

Most likely you'd want to do the opposite and enable properties by removing entries from the blacklist.
This can be done exactly like adding properties to the blacklist:

* Remove a property from the "general blacklist", which is the first dropdown
* Remove from the "entity blacklist" which contains the properties of the previously selected entity.

```javascript
// <plugin-root>/src/Resources/app/administration/app/src/component/sw-product-stream-field-select/index.js
const { Component } = Shopware;

Component.override('sw-product-stream-field-select', {
    computed: {
        options() {
            this.conditionDataProviderService.removeFromGeneralBlacklist(['createdAt']);
            this.conditionDataProviderService.removeFromEntityBlacklist('category', ['path']);
            return this.$super('options');
        }
    }
});
```

This example enables both the general `createdAt` property, as well as the category property `path`.

---

---

## Add custom component
**Source:** [guides/plugins/plugins/administration/module-component-management/add-custom-component.md](https://developer.shopware.com/docs/v6.6/guides/plugins/plugins/administration/module-component-management/add-custom-component.md)  
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
export default Shopware.Component.wrapComponentConfig({
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

* [More about templates](../templates-styling/writing-templates.md)
* [Add some styling to your component](../templates-styling/add-custom-styles.md)
* [Use shortcuts for your component](../advanced-configuration/add-shortcuts.md)

Furthermore, what about [customizing other components](customizing-components.md), instead of creating new ones?

---

---

## Add custom input field to existing component
**Source:** [guides/plugins/plugins/administration/module-component-management/add-custom-field.md](https://developer.shopware.com/docs/v6.6/guides/plugins/plugins/administration/module-component-management/add-custom-field.md)  
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
**Source:** [guides/plugins/plugins/administration/module-component-management/add-custom-module.md](https://developer.shopware.com/docs/v6.6/guides/plugins/plugins/administration/module-component-management/add-custom-module.md)  
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

`Shopware` is a [global object](../data-handling-processing/the-shopware-object.md) created for third party developers.
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
In our case here, let's say we use the icon `regular-shopping-bag`, which will also be used for the module.

::: danger
This is not the icon being used for a menu entry! The icon for that needs to be configured separately.
Please refer to the [Add a menu entry](../routing-navigation/add-menu-entry.md) guide for more information on this topic.
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
    icon: 'regular-shopping-bag',
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
For this purpose, create a new directory `snippet` in your module's directory and in there two new files: `de-DE.json` and `en-GB.json`.
The snippet files will be loaded automatically based on the folder structure.

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
        group: 'plugins',
        icon: 'regular-rocket',
        to: 'swag.plugin.list',
        name: 'SwagExampleMenuItemGeneral', // optional, fallback is taken from module
        id: '', // optional, fallback is taken from module
        label: '', // optional, fallback is taken from module
        iconComponent: YourCustomIconRenderingComponent, // optional, this overrides the component used to render the icon
    }]
});
```

The `group` property determines the tab, the item will be displayed in. Valid options are 'shop', 'system' and 'plugins'.

The `icon` property contains the icon name which will be displayed. Refer to the [Meteor Icon Kit documentation](https://developer.shopware.com/resources/meteor-icon-kit/) for icon names.

The `to` property must contain the name of the route. The route has to be defined in a separate routes section as described [here](../routing-navigation/add-custom-route.md). Have a look at the `Configuring the route` section in particular to find out about the name of your route.

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
    icon: 'regular-shopping-bag',

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
            path: 'detail/:id',
            meta: {
                parentPath: 'swag.example.list'
            }
        },
        create: {
            component: 'swag-example-create',
            path: 'create',
            meta: {
                parentPath: 'swag.example.list'
            }
        }
    },

    navigation: [{
        label: 'swag-example.general.mainMenuItemGeneral',
        color: '#ff3d58',
        p

… **Truncated.** Full document: https://developer.shopware.com/docs/v6.6/guides/plugins/plugins/administration/module-component-management/add-custom-module.md


---

## Customizing components
**Source:** [guides/plugins/plugins/administration/module-component-management/customizing-components.md](https://developer.shopware.com/docs/v6.6/guides/plugins/plugins/administration/module-component-management/customizing-components.md)  
*(Body truncated in this bundle; follow the link for the rest.)*

# Customizing components

The Shopware 6 Administration allows you to override and extend components to change its content and its behavior.

## Prerequisites

All you need for this guide is a running Shopware 6 instance, the files and preferably a registered module.
Of course, you will have to understand JavaScript, Vue and have a basic familiarity with TwigJS block system, and the templating engine used in the Administration. It is just used for the block extending and overriding. Every other feature of TwigJS is not used in the Administration.
However, that is a prerequisite for Shopware as a whole and will not be taught as part of this documentation.

## General

To add new functionality or change the behavior of an existing component, you can either override or extend the component.

The difference between the two methods is that with `Component.extend()` a new component is created. With `Component.override()`, on the other hand, the previous behavior of the component is simply overwritten.

## Override a component

The following example shows how you can override the template of the `sw-text-field` component.

```JS
// import the new twig-template file
import template from './sw-text-field-new.html.twig';

// override the existing component `sw-text-field` by passing the new configuration
Shopware.Component.override('sw-text-field', {
    template
});
```

## Extending a component

To create your custom text-field `sw-custom-field` based on the existing `sw-text-field` you can implement it like the following:

```JS
// import the custom twig-template file
import template from './sw-custom-field.html.twig';

// extend the existing component `sw-text-field` by passing
// a new component name and the new configuration
Shopware.Component.extend('sw-custom-field', 'sw-text-field', {
    template
});
```

Now you can render your new component `sw-custom-field` in any template like this:

```twig
    <sw-custom-field></sw-custom-field>
```

## Customize a component template

To extend a given template you can use the Twig `block` feature.

Imagine, the component you want to extend/override has the following template:

```twig
{% block card %}
    <div class="sw-card">
        {% block card_header %}
            <div class="sw-card--header">
                {{ header }}
            </div>
        {% endblock %}

        {% block card_content %}
            <div class="sw-card--content">
                {{ content }}
            </div>
        {% endblock %}
    </div>
{% endblock %}
```

Maybe you want to replace the markup of the header section and add an extra block to the content.
With the Twig `block` feature you can implement a solution like this:

```twig
{# override/replace an existing block #}
{% block card_header %}
    <h1 class="custom-header">
        {{ header }}
    </h1>
{% endblock %}

{% block card_content %}

    {# render the original block #}
    {% parent %}

    <div class="card-custom-content">
        ...
    </div>
{% endblock %}
```

Summarized with the `block` feature you will be able to replace blocks inside a template.
Additionally, you can render the original markup of a block by using `{% parent %}`

## Extending methods and computed properties

Sometimes you need to change the logic of a method or a computed property while you are extending/overriding a component.
In the following example we extend the `sw-text-field` component and change the `onInput()` method, which gets called after the value of the input field changes.

```JS
// extend the existing component `sw-text-field` by passing
// a new component name and the new configuration
Shopware.Component.extend('sw-custom-field', 'sw-text-field', {

    // override the logic of the onInput() method
    methods: {
        onInput() {
            // add your custom logic in here
            // ...
        }
    }
});
```

In the previous example, the inherited logic of `onInput()` will be replaced completely.
But sometimes, you will only be able to add additional logic to the method. You can achieve this by using `this.$super()` call.

```JS
// extend the existing component `sw-text-field` by passing
// a new component name and the new configuration
Shopware.Component.extend('sw-custom-field', 'sw-text-field', {

    // extend the logic of the onInput() method
    methods: {
        onInput() {
            // call the original implementation of `onInput()`
            const superCallResult = this.$super('onInput');

            // add your custom logic in here
            // ...
        }
    }
});
```

This technique also works for `computed` properties, for example:

```JS
// extend the existing component `sw-text-field` by passing
// a new component name and the new configuration
Shopware.Component.extend('sw-custom-field', 'sw-text-field', {

    // extend the logic of the computed property `stringRepresentation`
    computed: {
        stringRepresentation() {
            // call the original implementation of `onInput()`
            const superCallResult = this.$super('stringRepresentation');

            // add your custom logic in here
            // ...
        }
    }
});
```

## Real world example for block overriding

### Finding the block to override

In this guide we want to change the heading of the Shopware 6 dashboard to be `Welcome to a customized Administration` instead of `Welcome to Shopware 6`.
To do this, we first need to find an appropriate twig block to override.
We don't want to replace too much but also to not override too little of the Administration.
In this case, we only want to override the headline and not links or anything else on the page.
Looking at the twig markup for the dashboard [here](https://github.com/shopware/shopware/blob/trunk/src/Administration/Resources/app/administration/src/module/sw-dashboard/page/sw-dashboard-index/sw-dashboard-index.html.twig),
suggests that we only need to override the twig block with the name `sw_dashboard_index_content_intro_content_headline` to achieve our goal.

### Preparing the override

Now that we know where to place our override, we need to decide what to override it with.
In this very simple example it suffices to create a twig file, declare a block with the name we previously found and to insert our new header into the block.

```text
<!-- <plugin root>/src/Resources/app/administration/src/sw-dashboard-index-override/sw-dashboard-index.html.twig -->
{% block sw_dashboard_index_content_intro_content_headline %}
    <h1>
        Welcome to a customized component
    </h1>
{% endblock %}
```

This overrides the entire twig block with our new markup.
However, if we want to retain the original content of the twig block and just add our markup to the existing one, we can do that by including a {% parent %} somewhere in the twig block.
Learn more about the capabilities of twig.js [here](https://github.com/twigjs/twig.js/wiki).

As you might have noticed the heading we just replaced had a `{ $tc() }` [string interpolation](https://vuejs.org/v2/guide/syntax.html#Text) which is used to make it multilingual.
Learn more about internationalization in the Shopware 6 Administration and about adding your own snippets to the Administration [here](../templates-styling/adding-snippets.md).

### Applying the override

Registering the override of the Vue component is done by using the override method of our ComponentFactory.
This could be done in any `.js` file, which then has to be later imported, but we'll place it in `<plugin root>/src/Resources/app/administration/src/sw-dashboard-index-override/index.js`.

```javascript
import template from './sw-dashboard-index.html.twig';

Shopware.Component.override('sw-dashboard-index', {
    template
});
```

The first parameter matches the component to override, the second parameter has to be an object containing the actually overridden properties for example, the new twig template extension for this component.

### Loading the JavaScript File

The main entry point to customize the Administration via a plugin is the `main.js` file.
It has to be placed into the `<plugin root>/src/Resources/app/administration/src` directory in order to be automatically found by Shopware 6.

The only thing now left to just add an import for our previously created `./sw-dashboard-index-override/index.js` in the `main.js`:

```javascript
import './sw-dashboard-index-override/';
```

## Experimental: Composition API extension system

Shopware 6 is introducing a new way to extend components using the Composition API. This system is currently in an experimental state and is needed for the future migration of components from the Options API to the Composition API.

### Current status and future plans

* The existing Options API extension system remains fully supported and functional.
* The new Composition API extension system is introduced as an experimental feature.
* In future versions, components will gradually migrate from Options API to Composition API.
* Plugin developers are encouraged to familiarize themselves with the new system, but should continue using the current Component factory extension system for components written with the Options API.
* For components written with the Composition API, the new extension system should be used.
* In the long term, the Composition API extension system will become the standard way to override components. The Options API extension system will be deprecated and eventually removed when all components are migrated to the Composition API.

### How it works

The new extension system introduces two main functions:

1. `Shopware.Component.createExtendableSetup`: Used within components to make them extendable. This will mainly be used by the core team to make components extendable.
2. `Shopware.Component.overrideComponentSetup`: Used by plugins to override components.

### Using overrideComponentSetup

The `overrideComponentSetup` function is a key part of the new Composition API extension system. It allows plugin developers to override or extend the behavior of existing components without directly altering their source code.

### Basic usage

```javascript
Shopware.Component.overrideComponentSetup()('componentName', (previousState, props, context) => {
    // Your extension logic here
    return {
        // Return the new or modified properties and methods
    };
});
```

#### Parameters

1. `componentName`: A string identifying the component you want to override.
2. Callback function: This function receives three arguments:
   1. `previousState`: The current state of the component, including all its reactive properties and methods.
   2. `props`: The props passed to the component.
   3. `context`: The setup context, similar to what you would receive in a standard Vue 3 setup function.

#### Return value

The callback function should return an object containing any new or modified properties or methods you want to add or change in the component.

#### Example: Replacing a Single Property

```javascript
Shopware.Component.overrideComponentSetup()('sw-product-list', (previousState) => {
    const newPageSize = ref(50);

    return {
        pageSize: newPageSize // Override the default page size with the new ref
    };
});
```

#### Example: Adding a New Method

```javascript
Shopware.Component.overrideComponentSetup()('sw-order-list', (previousState) => {
    return {
        newCustomMethod() {
            console.log('This is a new method added to sw-order-list');
        }
    };
});
```

#### Example: Modifying existing data

```javascript
Shopware.Component.overrideComponentSetup()('sw-customer-list', (previousState) => {
    // Add a new column to the list
    previousState.columns.push({ property: 'customField', label: 'Custom Field' });
    
    return {};
});
```

#### Example: Overwriting a method

```javascript
Shopware.Component.overrideComponentSetup()('sw-customer-list', (previousState) => {
    // Overwrite the existing method
    const newIncrement = () => {

… **Truncated.** Full document: https://developer.shopware.com/docs/v6.6/guides/plugins/plugins/administration/module-component-management/customizing-components.md


---

## Customize modules
**Source:** [guides/plugins/plugins/administration/module-component-management/customizing-modules.md](https://developer.shopware.com/docs/v6.6/guides/plugins/plugins/administration/module-component-management/customizing-modules.md)  
# Customize modules

## Overview

In the `Administration` core code, each module is defined in a directory called `module`. A `module` is an encapsulated unit which implements a whole feature. For example there are modules for customers, orders, settings, etc.

## Prerequisites

All you need for this guide is a running Shopware 6 instance. Of course, you'll have to understand JavaScript and have a basic familiarity with TwigJS, the templating engine, used in the Administration. However, that's a prerequisite for Shopware as a whole and will not be taught as part of this documentation.

## Customizing a module

Module settings like `color`, `icon`, `navigation` are fixed by design and cannot be changed.

A guide for customizing components, which are already defined in existing modules, can be found here - [Customizing components](../module-component-management/customizing-components.md) ..

However, modules themselves cannot be directly overridden.

At some point you need to add or change the routes of a module. For example when you want to add a tab to the page.

This is done by creating a new module and implementing a `routeMiddleware`. You can add those changes to your `main.js` file, which could then look like this:

```javascript
// <plugin root>/src/Resources/app/administration/src/main.js
Shopware.Module.register('my-new-custom-route', {
    routeMiddleware(next, currentRoute) {
        if (currentRoute.name === 'sw.product.detail') {
            currentRoute.children.push({
                name: 'sw.product.detail.custom',
                path: '/sw/product/detail/:id/custom',
                component: 'sw-product-detail-custom',
                meta: {
                    parentPath: "sw.product.index"
                }
            });
        }
        next(currentRoute);
    }
});
```

In this example we register a new module which uses the `routeMiddleWare` to scan the routes while the `Vue router` is being set up. If we find the route `sw.product.detail` we just add another child route by pushing it to the `currentRoute.children`.

You can find a detailed example in the [Add tab to existing module](../routing-navigation/add-new-tab.md) guide.

## More interesting topics

* [Customizing components](../module-component-management/customizing-components.md)
* [Adding a route](../routing-navigation/add-custom-route.md)

---

---

## Using base components
**Source:** [guides/plugins/plugins/administration/module-component-management/using-base-components.md](https://developer.shopware.com/docs/v6.6/guides/plugins/plugins/administration/module-component-management/using-base-components.md)  
# Using base components

The Shopware 6 Administration comes with a bunch of tailored Vue components, already accessible in all of your templates via the `component registry`. This guide will show you how you can use Shopware-made components in your templates, if you want to learn more about the `component registry` and how you can register your own components to it have a look at the [corresponding guide](../module-component-management/add-custom-component.md)

## Prerequisites

All you need for this guide is a running Shopware 6 instance, the files and preferably a registered module. Of course you'll have to understand JavaScript and have a basic familiarity with [Vue](https://vuejs.org/), the framework used in the Administration. However, that's a prerequisite for Shopware as a whole and will not be taught as part of this documentation.

## Finding the base component needed

All Shopware 6 Administration components can be found in the [Component Library](https://component-library.shopware.com/). There you can see what each of the components does and looks like, it also shows you what props they can work with and which slots they have.

## Using the base component

As mentioned before in the introduction, all components used in the Shopware 6 Administration are first registered to the `component registry`. This `component registry` is just a map of all components, which then get registered to Vue during the `Administrations boot process`. Since all of the components are registered as [global `Vue` components](https://vuejs.org/v2/guide/components-registration.html#Global-Registration), they are accessible in all templates of the Administration.

Using base components in your own Administration templates is rather simple. In the example below we will use the `sw-text-field` in our template, which simply renders a `text` input tag, but also supports some fancy functionality, like inheritance, etc:

```html
// <plugin-root>/src/Resources/app/administration/app/src/component/example-component/example.html.twig
<div>
    <sw-text-field />
</div>
```

That's basically it. To continue building beautiful custom components, learn how to write templates and how to include them in your components [here](../templates-styling/writing-templates.md)

---

---

## Override existing routes
**Source:** [guides/plugins/plugins/administration/overriding-routes.md](https://developer.shopware.com/docs/v6.5/guides/plugins/plugins/administration/overriding-routes.md)  
# Override existing routes

## Overview

In the `Administration` core code, each module is defined in a directory called `module`. Modules define routes which can be extended with `routeMiddleware`. To see what else you can customize in existing modules, have a look at this [guide](customizing-modules)

A `module` is an encapsulated unit which implements a whole feature. For example there are modules for customers, orders, settings, etc.

## Prerequisites

All you need for this guide is a running Shopware 6 instance. Of course, you'll have to understand JavaScript and have a basic familiarity with [Vue](https://vuejs.org/) and the [Vue Router](https://router.vuejs.org/). However, that's a prerequisite for Shopware as a whole and will not be taught as part of this documentation. Further a basic understanding of what modules are is also required, learn more about them [here](add-custom-module)

## Applying the override

At some point you might want to override or change existing routes, for example, to change the privileges required for a route or entirely replace it with your own.

This is done by creating a new module and implementing a `routeMiddleware`. You can add those changes to your `main.js` file, which could then look like this:

```javascript
// <plugin root>/src/Resources/app/administration/src/main.js
Module.register('my-new-custom-route', {
    routeMiddleware(next, currentRoute) {
        if (currentRoute.name === 'sw.product.detail') {

            const childIndex = currentRoute.children.findIndex(child => child.name === 'sw.product.detail.base');

            currentRoute.children[childIndex] = {
                name: 'sw.product.detail.base',
                component: 'sw-product-detail-base',
                path: 'base',
                meta: {
                    parentPath: 'sw.product.index',
                    privilege: 'product.editor'
                }
            }
        }
        next(currentRoute);
    }
});
```

This `routeMiddleware` changes the required privileges for the `sw.product.detail.base` route from `product.viewer` to `product.editor`. The rest of the route configurations stays the same in this example.

If you want to learn more about ACL take a look at this [guide](add-acl-rules) and if you want to learn everything about Administration routes, head over to this [guide](add-custom-route)

---

---

