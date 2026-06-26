# ADMINISTRATION UI

Compiled excerpts from the Shopware Developer Documentation snapshot. Prefer live docs at [developer.shopware.com](https://developer.shopware.com/) when in doubt.

---

## Adding permissions
**Source:** [guides/plugins/plugins/administration/permissions-error-handling/add-acl-rules.md](https://developer.shopware.com/docs/v6.6/guides/plugins/plugins/administration/permissions-error-handling/add-acl-rules.md)  
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

![Permissions GUI](../../../../../assets/permissions-gui.png)

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

![Additional permissions GUI](../../../../../assets/additionalPermissions-gui.png)

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

## Use the

… **Truncated.** Full document: https://developer.shopware.com/docs/v6.6/guides/plugins/plugins/administration/permissions-error-handling/add-acl-rules.md


---

## Adding error handling
**Source:** [guides/plugins/plugins/administration/permissions-error-handling/add-error-handling.md](https://developer.shopware.com/docs/v6.6/guides/plugins/plugins/administration/permissions-error-handling/add-error-handling.md)  
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

## Add custom route
**Source:** [guides/plugins/plugins/administration/routing-navigation/add-custom-route.md](https://developer.shopware.com/docs/v6.6/guides/plugins/plugins/administration/routing-navigation/add-custom-route.md)  
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

Routes can be matched by name and path. This configuration results in this route's full name being `custom.module.overview` and the URL being `/custom/module/overview` relative to the Administration's default URL. The routes full name is a combination of the module's id and the name of the item inside the `routes` object. In this case the module's id is `custom-module` (Notice that all dashes are automatically replaced by dots in the final route name).

Usually you want to render your custom component here, which is explained [here](../module-component-management/add-custom-component.md). But that is not all! Routes can have parameters, to then be handed to the components being rendered and much more. Learn more about what the Vue Router can do in its official [Documentation](https://router.vuejs.org/guide/essentials/dynamic-matching.html#reacting-to-params-changes).

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

* [Adding a custom service](../services-utilities/add-custom-service.md)
* [Customizing a module](../module-component-management/customizing-modules.md)
* [Adding permissions](../permissions-error-handling/add-acl-rules.md)

---

---

## Add menu entry
**Source:** [guides/plugins/plugins/administration/routing-navigation/add-menu-entry.md](https://developer.shopware.com/docs/v6.6/guides/plugins/plugins/administration/routing-navigation/add-menu-entry.md)  
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
    parent: 'sw-catalogue',
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

## Add tab to existing module
**Source:** [guides/plugins/plugins/administration/routing-navigation/add-new-tab.md](https://developer.shopware.com/docs/v6.6/guides/plugins/plugins/administration/routing-navigation/add-new-tab.md)  
# Add tab to existing module

## Overview

You want to create a new tab in the Administration? This guide gets you covered on this subject. A realistic example would be adding a new association for an entity, which you want to configure on a separate tab on the entity detail page.

## Prerequisites

This guide requires you to already have a basic plugin running. If you don't know how to do this in the first place, have a look at our plugin base guide:

In the course of this guide, you need to create a custom route. If you want to learn on how to create a custom component, please refer to the guide on it:

Also, we will use a small, custom component to fill our custom tab. In order to get used to that, it might come in handy to read the corresponding guide first:

::: info

### Please remember

The main entry point to customize the Administration via plugin is the `main.js` file. It has to be placed into a `<plugin root>/src/Resources/app/administration/src` directory in order to be found by Shopware 6. So please use the file accordingly and refer to the [plugin base guide](../../plugin-base-guide.md) for more details.
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

The [route](../routing-navigation/add-custom-route.md) being used here has the name `sw.product.detail.custom`, this will become important again later on.

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

It then points to a component, which represents the routes actual content - so you'll have to create [a new component](../module-component-management/add-custom-component.md) in the next step. Note the new import that's already part of this example: `view/sw-product-detail-custom`

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

## Override existing routes
**Source:** [guides/plugins/plugins/administration/routing-navigation/overriding-routes.md](https://developer.shopware.com/docs/v6.6/guides/plugins/plugins/administration/routing-navigation/overriding-routes.md)  
# Override existing routes

## Overview

In the `Administration` core code, each module is defined in a directory called `module`. Modules define routes which can be extended with `routeMiddleware`. To see what else you can customize in existing modules, have a look at this [guide](../module-component-management/customizing-modules.md)

A `module` is an encapsulated unit which implements a whole feature. For example there are modules for customers, orders, settings, etc.

## Prerequisites

All you need for this guide is a running Shopware 6 instance. Of course, you'll have to understand JavaScript and have a basic familiarity with [Vue](https://vuejs.org/) and the [Vue Router](https://router.vuejs.org/). However, that's a prerequisite for Shopware as a whole and will not be taught as part of this documentation. Further a basic understanding of what modules are is also required, learn more about them [here](../module-component-management/add-custom-module.md)

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

If you want to learn more about ACL take a look at this [guide](../permissions-error-handling/add-acl-rules.md) and if you want to learn everything about Administration routes, head over to this [guide](../routing-navigation/add-custom-route.md)

---

---

## Add custom data to the search
**Source:** [guides/plugins/plugins/administration/search-custom-data.md](https://developer.shopware.com/docs/v6.5/guides/plugins/plugins/administration/search-custom-data.md)  
# Add custom data to the search

## Overview

When developing a customization that has a frequently visited entity listing you're able to make use of an interesting opportunity: You can enable the user to take a shortcut finding his desired entry using the global search.

There are two different ways how the global search works:

* Global search without type specification
* Typed global search

They only differ in the API they use and get displayed in a slightly different way.

::: warning
Think twice about adding this shortcut because if every plugin adds their own search tag it gets cluttered.
:::

## Prerequisites

For this guide, it's necessary to have a running Shopware 6 instance and full access to both the files and a running plugin. See our plugin page guide to learn how to create your own plugins.

In addition, you need a custom entity to add to the search to begin with. Head over to the following guide to learn how to achieve that:

## Support custom entity via search API

To support an entity in the untyped global search the definition in the symfony container needs the tag `shopware.composite_search.definition`. The priority of the tag defines the order in the search order.

The typed global search needs an instance of the JavaScript class `ApiService` with the key of the entity in camelcase suffixed with `Service`. E.g. The service key is `yourCustomSearchService` when requesting a service for `your_custom_search`. Every entity definition gets automatically an instance in the injection container but can be overridden so there is no additional work needed.

## Support in the Administration UI

### Add search tag

The search tag displays the entity type that is used in the typed search and is a clickable button to switch from the untyped to the typed search. In order to add the tag, a service decorator is used to add a type to the `searchTypeService`:

```javascript
const { Application } = Shopware;

Application.addServiceProviderDecorator('searchTypeService', searchTypeService => {
    searchTypeService.upsertType('foo_bar', {
        entityName: 'foo_bar',
        entityService: 'fooBarService',
        placeholderSnippet: 'foo-bar.general.placeholderSearchBar',
        listingRoute: 'foo.bar.index'
    });

    return searchTypeService;
});
```

Let's take a closer look on how this decorator is used:

* The key and `entityName` is used as the same to change also existing types.
* The `entityService` is used for the typed search.
* This service can be overridden with an own implementation for customization.
* The `placeholderSnippet` is a translation key that is shown when no search term is entered.
* The `listingRoute` is used to show a link to continue the search in the module specific listing view.

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
// <plugin root>/src/Resources/app/administration/src/app/component/structure/sw-search-bar-item/index.js
import template from './sw-search-bar-item.html.twig';

Shopware.Component.override('sw-search-bar-item', {
    template
})
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
// <plugin root>/src/Resources/app/administration/src/app/component/structure/sw-search-more-results/index.js
import template from './sw-search-more-results.html.twig';

Shopware.Component.override('sw-search-more-results', {
    template
})
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

To change the color of the tag, or the icon in the untyped global search a module has to be registered with an entity reference in the module:

```javascript
Shopware.Module.register('any-name', {
    color: '#ff0000',
    icon: 'default-basic-shape-triangle',
    entity: 'my_entity',
})
```

---

---

## Adding Services
**Source:** [guides/plugins/plugins/administration/services-utilities/add-custom-service.md](https://developer.shopware.com/docs/v6.6/guides/plugins/plugins/administration/services-utilities/add-custom-service.md)  
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

* [Creating a new administration component](../module-component-management/add-custom-component.md)
* [Extending an existing administration component](../module-component-management/customizing-components.md) .

---

---

## Add filter
**Source:** [guides/plugins/plugins/administration/services-utilities/add-filter.md](https://developer.shopware.com/docs/v6.6/guides/plugins/plugins/administration/services-utilities/add-filter.md)  
# Add filter

## Overview

In this guide you'll learn, how to create a filter for the Shopware Administration. A filter is just a little helper for formatting text. In this example, we create a filter that converts text into uppercase and adds an underscore at the beginning and end.

## Prerequisites

This guide requires you to already have a basic plugin running. If you don't know how to do this in the first place, have a look at our [Plugin base guide](../../plugin-base-guide.md).

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

Now that you know how to create a filter for the Administration, we want to use it in our code. For this head over to our [using filter](using-filter.md) guide.

---

---

## Extending services
**Source:** [guides/plugins/plugins/administration/services-utilities/extending-services.md](https://developer.shopware.com/docs/v6.6/guides/plugins/plugins/administration/services-utilities/extending-services.md)  
# Extending services

## Overview

This guide will teach you how to extend a Shopware provided service with middleware and decorators.
The Shopware 6 Administration uses [BottleJS](https://github.com/young-steveo/bottlejs) to provide the framework for services.
If you want to learn how to create your own services, look at [this guide](./add-custom-service.md).

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

## Injecting services
**Source:** [guides/plugins/plugins/administration/services-utilities/injecting-services.md](https://developer.shopware.com/docs/v6.6/guides/plugins/plugins/administration/services-utilities/injecting-services.md)  
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

## Making API Requests
**Source:** [guides/plugins/plugins/administration/services-utilities/making-api-requests.md](https://developer.shopware.com/docs/v6.6/guides/plugins/plugins/administration/services-utilities/making-api-requests.md)  
# Making API Requests

## Overview

In this guide you'll learn how to create a custom API service in your plugin's administration to make HTTP requests to the Shopware API. This is useful when you need to communicate with custom backend endpoints or extend Shopware's API functionality.

## Prerequisites

In order to add your own custom API service for your plugin, you first need a plugin as base. Therefore, you can refer to the [Plugin Base Guide](../../plugin-base-guide).

You also need to have a custom administration module or component. Refer to [Add custom module](../module-component-management/add-custom-module) to get started.

## Creating the API service

First, create a new API service class that extends Shopware's `ApiService` class. This provides you with all the necessary methods for authentication and HTTP communication.

Create the service file in your plugin's administration source directory:

```javascript
// <plugin root>/src/Resources/app/administration/src/api/my-api-service.js
const { ApiService } = Shopware.Classes;

class MyApiService extends ApiService {
    constructor(httpClient, loginService, apiEndpoint = '_action/my-plugin') {
        super(httpClient, loginService, apiEndpoint);
    }

    // GET request example
    getMyData() {
        const apiRoute = `${this.getApiBasePath()}/my-data`;
        return this.httpClient
            .get(apiRoute, {
                headers: this.getBasicHeaders(),
            })
            .then((response) => {
                return ApiService.handleResponse(response);
            });
    }

    // POST request example with data
    createMyData(data) {
        const apiRoute = `${this.getApiBasePath()}/my-data`;
        return this.httpClient
            .post(
                apiRoute,
                data,
                {
                    headers: this.getBasicHeaders(),
                }
            )
            .then((response) => {
                return ApiService.handleResponse(response);
            });
    }

    // DELETE request example
    deleteMyData(id) {
        const apiRoute = `${this.getApiBasePath()}/my-data/${id}`;
        return this.httpClient
            .delete(apiRoute, {
                headers: this.getBasicHeaders(),
            })
            .then((response) => {
                return ApiService.handleResponse(response);
            });
    }

    // GET request with query parameters
    searchMyData(searchTerm, limit = 25) {
        const apiRoute = `${this.getApiBasePath()}/my-data/search`;
        return this.httpClient
            .get(apiRoute, {
                params: {
                    term: searchTerm,
                    limit: limit,
                },
                headers: this.getBasicHeaders(),
            })
            .then((response) => {
                return ApiService.handleResponse(response);
            });
    }
}

export default MyApiService;
```

## Registering the service

To make your API service available throughout your plugin's administration, you need to register it as a service provider. Create an index file to handle the registration:

```javascript
// <plugin root>/src/Resources/app/administration/src/api/index.js
import MyApiService from './my-api-service';

const { Application } = Shopware;

Application.addServiceProvider('myApiService', (container) => {
    const initContainer = Application.getContainer('init');

    return new MyApiService(
        initContainer.httpClient,
        container.loginService
    );
});
```

Don't forget to import this file in your plugin's main administration entry point:

```javascript
// <plugin root>/src/Resources/app/administration/src/main.js
import './api';
// ... other imports
```

## Using the API service in components

Now you can inject and use your API service in any component within your plugin:

```javascript
// <plugin root>/src/Resources/app/administration/src/module/my-module/component/my-component/index.js
import template from './template.twig';

const { Component, Mixin } = Shopware;

Component.register('my-component', {
    template,
    inject: ['myApiService'],
    mixins: [Mixin.getByName('notification')],

    data() {
        return {
            myData: [],
            isLoading: false,
        };
    },

    created() {
        this.loadData();
    },

    methods: {
        async loadData() {
            this.isLoading = true;
            
            try {
                this.myData = await this.myApiService.getMyData();
                
                this.createNotificationSuccess({
                    message: 'Data loaded successfully',
                });
            } catch (error) {
                this.createNotificationError({
                    message: error.message || 'An error occurred',
                });
            } finally {
                this.isLoading = false;
            }
        },

        async saveData(data) {
            this.isLoading = true;
            
            try {
                await this.myApiService.createMyData(data);
                
                this.createNotificationSuccess({
                    message: 'Data saved successfully',
                });
                
                // Reload data after saving
                await this.loadData();
            } catch (error) {
                this.createNotificationError({
                    message: error.message || 'Failed to save data',
                });
            } finally {
                this.isLoading = false;
            }
        },

        async deleteItem(id) {
            try {
                await this.myApiService.deleteMyData(id);
                
                this.createNotificationSuccess({
                    message: 'Item deleted successfully',
                });
                
                // Reload data after deletion
                await this.loadData();
            } catch (error) {
                this.createNotificationError({
                    message: error.message || 'Failed to delete item',
                });
            }
        }
    },
});
```

## Working with authentication

The `ApiService` base class automatically handles authentication by including the necessary headers. The `getBasicHeaders()` method provides:

* Authorization token
* Content-Type headers
* API version headers

If you need custom headers, you can extend them:

```javascript
getCustomData() {
    const headers = {
        ...this.getBasicHeaders(),
        'X-Custom-Header': 'custom-value'
    };

    return this.httpClient
        .get(`${this.getApiBasePath()}/custom-endpoint`, { headers })
        .then((response) => {
            return ApiService.handleResponse(response);
        });
}
```

## Error handling

The `ApiService.handleResponse()` method automatically handles common HTTP errors. However, you should still implement proper error handling in your components:

```javascript
async performApiCall() {
    try {
        const result = await this.myApiService.getMyData();
        // Handle success
    } catch (error) {
        // Check for specific error types
        if (error.response) {
            // The request was made and the server responded with a status code
            // that falls out of the range of 2xx
            console.error('Error status:', error.response.status);
            console.error('Error data:', error.response.data);
        } else if (error.request) {
            // The request was made but no response was received
            console.error('No response received:', error.request);
        } else {
            // Something happened in setting up the request
            console.error('Error:', error.message);
        }
    }
}
```

## Advanced usage

### File uploads

For file uploads, you can use FormData:

```javascript
uploadFile(file) {
    const formData = new FormData();
    formData.append('file', file);
    
    return this.httpClient.post(
        `${this.getApiBasePath()}/upload`,
        formData,
        {
            headers: {
                ...this.getBasicHeaders(),
                'Content-Type': 'multipart/form-data',
            },
        }
    ).then((response) => {
        return ApiService.handleResponse(response);
    });
}
```

### Accessing standard Shopware APIs

You can also access Shopware's standard APIs using the repository pattern:

```javascript
Component.register('my-component', {
    inject: ['repositoryFactory'],

    computed: {
        productRepository() {
            return this.repositoryFactory.create('product');
        }
    },

    methods: {
        async loadProducts() {
            const criteria = new Shopware.Data.Criteria();
            criteria.setPage(1);
            criteria.setLimit(25);
            
            const products = await this.productRepository.search(criteria);
            // Use products...
        }
    }
});
```

## Next steps

Now that you've created your API service, you might want to:

* Create the corresponding backend API endpoints
* Add more complex API interactions
* Implement caching strategies for better performance
* Add request interceptors for global error handling

For more information on creating backend API endpoints, refer to the [API documentation](../../../api).

---

---

## The Sanitizer helper
**Source:** [guides/plugins/plugins/administration/services-utilities/the-sanitizer-helper.md](https://developer.shopware.com/docs/v6.6/guides/plugins/plugins/administration/services-utilities/the-sanitizer-helper.md)  
# The Sanitizer helper

## Overview

The Shopware 6 Sanitizer Helper is a wrapper around [`DOMPurify`](https://github.com/cure53/DOMPurify), which is used to sanitize HTML in order to prevent `XSS attacks`.

## Where is it registered?

The Sanitizer Helper is registered to the [Shopware Global Object](../data-handling-processing/the-shopware-object.md) and therefore can be accessed anywhere in your plugin.

```javascript
const sanitizer = Shopware.Helper.SanitizerHelper; 
```

It also is registered in the Vue prototype as seen [here](https://github.com/shopware/shopware/blob/trunk/src/Administration/Resources/app/administration/src/app/plugin/sanitize.plugin.js).
This means it can also be accessed in your components like this:

```javascript
const Sanitizer = this.$sanitizer;
const sanitize = this.$sanitize;
```

## Sanitizing HTML

As mentioned before the `SanitizerHelper` is registered to the [Shopware Global Object](../data-handling-processing/the-shopware-object.md) and therefore can be accessed like this everywhere:

```javascript
Shopware.Helper.SanitizerHelper.sanitize('<img src=x onerror=alert(1)//>'); // becomes <img src="x">
```

And since it is bound to the Vue prototype it can be used in all Vue components like this:

```javascript
this.$sanitizer.sanitize('<svg><g/onload=alert(2)//<p>'); // becomes <svg><g></g></svg>
this.$sanitize('<img src=x onerror=alert(1)//>'); // becomes <img src="x">
```

## How to set the config

The config can be set with the `setConfig` and cleared with the `clearConfig` function, as seen below:

```javascript
Shopware.Helper.SanitizerHelper.setConfig({
    USE_PROFILES: { html: true }
});

Shopware.Helper.SanitizerHelper.clearConfig()
```

See all of the configuration options [here](https://github.com/cure53/DOMPurify#can-i-configure-dompurify)

## How to add hooks

The aforementioned Wrapper also provides functions to add and remove hooks to DOMPurify.
Learn what DOMPurify hooks are in their [documentation](https://github.com/cure53/DOMPurify#hooks).

```javascript
Shopware.Helper.SanitizerHelper.addMiddleware('beforeSanitizeElements',  function (
        currentNode,
        hookEvent,
        config
    ) {
        // Do something with the current node and return it
        // You can also mutate hookEvent (i.e. set hookEvent.forceKeepAttr = true)
        return currentNode;
    }
);

Shopware.Helper.SanitizerHelper.removeMiddleware('beforeSanitizeElements');
```

---

---

## Using filter
**Source:** [guides/plugins/plugins/administration/services-utilities/using-filter.md](https://developer.shopware.com/docs/v6.6/guides/plugins/plugins/administration/services-utilities/using-filter.md)  
# Using filter

## Overview

In this guide you'll learn how to use filters in the Shopware Administration.

## Prerequisites

This guide requires you to already have a basic plugin running. If you don't know how to do this in the first place, have a look at our [Plugin base guide](../../plugin-base-guide.md).

Furthermore you should have a look at our [add filter](add-filter.md) guide, since this guide is built upon it.

## Using the filter

In this section we will show you, how to use our `example` filter in JavaScript code and in your Twig template files.

### Filter in components JavaScript

If we want to use the filter in our components JavaScript files, we can access it by using `this.$options.filters` and the name of our filter.

```javascript
this.$options.filters.example('firstArgument')
```

### Filter in Twig templates

If we want to use our filter in Twig templates, we can easily use it by using a pipe `|` and the name of our filter. It is also possible to use filters in `v-bind` expressions.

Below you can see two example implementations, how it could be done with single argument filters.

```twig
{% block my_custom_block %}
    <p>
       {{ $tc('swag-example.general.myCustomText')|example }}
    </p>
{% endblock %}
```

```html
<example-component :name="$tc('swag-example.general.myCustomText')|example"></example-component>
```

When using multiple arguments, we can pass them as shown below.

```twig
{% block my_custom_block %}
    <p>
       {{ $tc('swag-example.general.myCustomText')|example('secondArgument', 'thirdArgument') }}
    </p>
{% endblock %}
```

```html
<example-component :title="$tc('swag-example.general.myCustomText')|example('secondArgument', 'thirdArgument')"></example-component>
```

---

---

## Using utility functions
**Source:** [guides/plugins/plugins/administration/services-utilities/using-utils.md](https://developer.shopware.com/docs/v6.6/guides/plugins/plugins/administration/services-utilities/using-utils.md)  
# Using utility functions

Utility functions in the Shopware 6 Administration are registered to [the Shopware object](../data-handling-processing/the-shopware-object.md) and are therefore accessible everywhere in the Administration. They provide many useful [shortcuts](../../../../../resources/references/administration-reference/utils.md) for common tasks.

## Prerequisites

All you need for this guide is a running Shopware 6 instance, the files, a registered module, and a good understanding of JavaScript.

## Accessing the utility functions

Let us see how to use one of the utility functions — for example, `capitalizeString` function. As the name implies, the `capitalizeString` function capitalizes strings by calling the [`lodash capitalize`](https://lodash.com/docs/4.17.15#capitalize) function.

```javascript
// <extension root>/src/Resources/app/administration/app/src/component/swag-basic-example/index.js
const { Component, Utils } = Shopware;

Component.register('swag-basic-example', {
    data() {
        return {
            text: 'hello',
            capitalizedString: undefined,
        };
    },

    created() {
        this.capitalize();
    },

    methods: {
        capitalize() {
            this.capitalizedString = Utils.string.capitalizeString(this.string);
        },
    },
});
```

## More, interesting topics

* [Adding filters](add-filter.md)
* [Adding mixins](../mixins-directives/add-mixins.md)

---

---

## Future Development Roadmap: Upgrading to Meteor Components
**Source:** [guides/plugins/plugins/administration/system-updates/meteor-components.md](https://developer.shopware.com/docs/v6.6/guides/plugins/plugins/administration/system-updates/meteor-components.md)  
# Future Development Roadmap: Upgrading to Meteor Components

> **Note:** The information provided in this article, including timelines and specific implementations, is subject to change.
> This document serves as a general guideline for our development direction.

## Introduction

With the release of Shopware 6.7, we will replace several current administration components with components from the [Meteor Component Library](https://meteor-component-library.vercel.app/).

## Why Meteor Components?

The Meteor Component Library is Shopware's official collection of reusable components used across multiple Shopware projects and built on the Shopware Design System.

Using a shared component library offers several advantages:

* **Consistent Design**: All components follow the Shopware Design System guidelines.
* **Consistent Behavior**: All components share standardized behavior patterns and API conventions.
* **Reusability**: Components can be seamlessly integrated across different projects and apps.
* **Maintenance**: Updates and improvements to components are managed centrally and automatically propagate to all projects using the component library.

## Migration guide

For each component being replaced, we provide a detailed upgrade guide that explains the migration process from the old component to the new Meteor Component. You can find these guides in the technical upgrade documentation for the release.

## Using Codemods for migration

To simplify the plugin migration process, we provide codemods that automatically replace old components with new Meteor Components.

### Prerequisites

* A [development installation of Shopware](https://github.com/shopware/shopware) must be installed
* Your plugin must be located in the `custom/plugins` folder

### Running the Migration Tool

1. Execute the following composer command:

   ```bash
   # Main command which also outputs the help text
   composer run admin:code-mods

   ## Example with arguments
   # composer run admin:code-mods -- --plugin-name example-plugin --fix -v 6.7
   ```

2. Provide your plugin name and target Shopware version for migration

3. The tool will:
   * Automatically replace compatible components with Meteor Components
   * Add guidance comments for components that require manual migration
   * Fixes some other deprecated code where possible

## Supporting Extension Developers

To support extension developers and ensure compatibility between Shopware 6.6 and Shopware 6.7, a new prop called `deprecated` has been added to Shopware components.

* **Prop Name**: `deprecated`
* **Default Value**: `false` (uses the new Meteor Components by default)
* **Purpose**:
  * When `deprecated` is set to `true`, the component will render the old (deprecated) version instead of the new Meteor Component.
  * This allows extension developers to maintain a single codebase compatible with both Shopware 6.6 and 6.7 without being forced to immediately migrate to Meteor Components.

Example:

```html
<!-- Uses mt-button in 6.7 and sw-button-deprecated in 6.6 -->
<template>
  <sw-button />
</template>


<!-- Uses sw-button-deprecated in 6.6 and 6.7 -->
<template>
  <sw-button deprecated />
</template>
```

> **Important:** Although the old components can still be used with the `deprecated` prop, we highly recommend migrating to Meteor Components whenever possible to align with future Shopware development.

---

---

## Migration from Vuex in Shopware to Pinia
**Source:** [guides/plugins/plugins/administration/system-updates/pinia.md](https://developer.shopware.com/docs/v6.6/guides/plugins/plugins/administration/system-updates/pinia.md)  
# Migration from Vuex in Shopware to Pinia

## Introduction

With the release of Shopware 6.7, we will replace Vuex with [Pinia](https://pinia.vuejs.org/) as the state management library for the administration.

## Why Pinia?

Migrating to Pinia simplifies state management with an intuitive API, no need for mutations, better TypeScript support, and seamless integration with Vue 3 Composition API. It’s lightweight, modular, and offers modern features like devtools support, making it a more efficient alternative to Vuex.

## Migration Guide

To migrate a Vuex store to Pinia, you need to make some changes to the store definition and how you access it in components.

* First, register it with `Shopware.Store.register` and define the store with `state`, `getters`, and `actions` properties:

**Before (Vuex):**

```javascript
export default {
    namespaced: true,

    state: {
      // Initial state
      ...
    },
    mutations: {
      ...
    },
    getters: {
       ...
    },
    actions: {
       ...
    },
}
```

**After (Pinia):**

```javascript
const store = Shopware.Store.register('<storeName>', {
    state: () => ({
        // Initial state
        ...
    }),
    getters: {
       ...
    },
    actions: {
       ...
    },
});
export default store;
```

* You can also register the store with an `id` property in the definition object, for example:

```javascript
const store = Shopware.Store.register({
    id: '<storeName>',
    state: () => ({
        // Initial state
    }),
    getters: {
       // ...
    },
    actions: {
       // ...
    },
});
```

* If you register a store that already exists, it will be overwritten. You can also unregister a store:

```javascript
Shopware.Store.unregister('<storeName>');
```

* To register a store from a component or index file, simply import the store file.

**Before (Vuex):**

```javascript
import productsStore from './state/products.state';

Shopware.State.registerModule('product', productsStore);
```

**After (Pinia):**

```javascript
import './state/products.state';
```

### Key Changes

#### State

In Pinia, `state` must be a function returning the initial state instead of a static object.

```javascript
state: () => ({
    productName: '',
})
```

#### Mutations

Vuex `mutations` are no longer needed in Pinia, since you can modify state directly in actions or compute it dynamically.

```javascript
actions: {
    updateProductName(newName) {
        this.productName = newName; // Directly update state
    },
},
```

#### Getters

* There cannot be getters with the same name as a property in the state, as both are exposed at the same level in the store.
* Getters should be used to compute and return information based on state, without modifying it.

#### TypeScript

We recommend migrating JavaScript stores to TypeScript for stricter typing, better autocompletion, and fewer errors during development.

```typescript
const store = Shopware.Store.register({
  id: 'myStore',
  ...
});

export type StoreType = ReturnType<typeof store>;
```

Then, you can use this type to extend `PiniaRootState`:

```typescript
import type { StoreType } from './store/myStore';

declare global {
    interface PiniaRootState {
        myStore: StoreType;
    }
}
```

### Composables as a Store

With Pinia, you can use reactive properties inside a store and define it like a composable. Keep in mind that only variables and functions returned from the store will be tracked by Pinia in devtools.

```typescript
const store = Shopware.Store.register('<storeName>', function() {
  const count = ref(0);

  const doubled = computed(() => count.value * 2);

  function increment() {
    count.value++;
  }

  function decrement() {
    count.value--;
  }

  return { count, doubled, increment, decrement };
});
```

You can also use a composable function defined outside the store. This allows you to encapsulate and reuse logic across different stores or components, promoting better code organization and modularity:

```typescript
// composables/myComposable.ts
export function useMyComposable() {
  const count = ref(0);

  const doubled = computed(() => count.value * 2);

  function increment() {
    count.value++;
  }

  function decrement() {
    count.value--;
  }

  return { count, doubled, increment, decrement };
}
```

```typescript
// store/myStore.ts
import { useMyComposable } from '../composables/myComposable';

const store = Shopware.Store.register('myStore', useMyComposable);
```

### Accessing the Store

To access the store in Vuex, you would typically do:

```javascript
Shopware.State.get('<storeName>');
```

When migrating to Pinia, it changes to:

```javascript
Shopware.Store.get('<storeName>');
```

### Testing

To test your store, just import it so it's registered. You can use `$reset()` to reset the store before each test:

```javascript
import './store/my.store';

describe('my store', () => {
  const store = Shopware.Store.get('myStore');

  beforeEach(() => {
    store.$reset();
  });

  it('has initial state', () => {
    expect(store.count).toBe(0);
  });
});
```

When testing components that use Pinia stores, register Pinia as a plugin and reset it before each test:

```javascript
import { createPinia, setActivePinia } from 'pinia';

const pinia = createPinia();

describe('my component', () => {
  beforeEach(() => {
    setActivePinia(pinia);
  });

  it('is a component', async () => {
    const wrapper = mount(await wrapTestComponent('myComponent', { sync: true }), {
      global: {
        plugins: [pinia],
        stubs: {
          // ...
        },
      },
    });

    expect(wrapper.exists()).toBe(true);
  });
});
```

---

---

## Future Development Roadmap: Changing from Webpack to Vite
**Source:** [guides/plugins/plugins/administration/system-updates/vite.md](https://developer.shopware.com/docs/v6.6/guides/plugins/plugins/administration/system-updates/vite.md)  
# Future Development Roadmap: Changing from Webpack to Vite

> **Note:** The information provided in this article, including timelines and specific implementations, is subject to change.
> This document serves as a general guideline for our development direction.

## Introduction

We are planning substantial changes to the way we build our Vue.js application.
The current Webpack build system has been in place for quite some time now, but like everything in tech, it becomes outdated sooner than later. Additionally to Webpack being slow and outdated, we identified a security risk for the future of our application. Many Webpack maintainers have moved on to other projects. Therefore, the Webpack project no longer receives significant updates. The same applies to the Webpack loaders we currently use.

## Introducing Vite

The Vue.js ecosystem has built its own bundler: Vite. Vite is fast, easier to configure and the new standard for Vue.js applications. That's why we decided to switch to Vite with Shopware 6.7.

## Consequences for extensions

For apps there are no consequences as your build process is already decoupled from Shopware. For plugins you only need to get active if you currently extend the webpack config by providing your own `webpack.config.js` file.

### Migrate the custom webpack config to Vite

If you have a custom webpack config, you need to migrate it to Vite. You need to do the following steps:

1. Create a new config file `vite.config.mts` to your plugin in the `YourApp/src/Resources/app/administration/src` directory. Previously you had a `webpack.config.js` in the following directory: `YourApp/src/Resources/app/administration/build/`
2. Remove the old `webpack.config.js` file
3. Make sure to remove all webpack related dependencies from your `package.json` file
4. Make sure to add the Vite dependencies to your `package.json` file

A basic config migration could look like this:

```javascript
// Old Webpack config
module.exports = () => {
    return {
        resolve: {
            alias: {
                '@example': 'src/example',
            }
        }
    };
};
```

```typescript
// New Vite config
import { defineConfig } from 'vite';

export default defineConfig({
    resolve: {
        alias: {
            '@example': 'src/example',
        },
    },
});
```

Of course, this is a very basic example. The Vite config can be much more complex and powerful. You can find more information about the Vite config in the [Vite documentation](https://vitejs.dev/config/). Depending on your webpack config, the migration can be very individual.

## Implementation details

In this section we'll document the implementation details of the new Vite setup.

### Feature flag

The system is already in place and can be tested by activating the feature flag: `ADMIN_VITE`.

### Bundle information

The information about all active bundles/plugins is written to `<shopwareRoot>/var/plugins.json` by the `Shopware\Core\Framework\Plugin\Command\BundleDumpCommand`. This command can be triggered standalone by running `php bin/console bundle:dump`. It is also part of the composer commands `build:js:admin`, `build:js:storefront`, `watch:admin` and `watch:storefront`. This file is used to load all the Shopware Bundles and custom plugins.

### Building the Shopware Administration

The command responsible for building the Shopware Administration with all extensions remains `composer build:js:admin`.

### Building the core

The Vite config located under `<shopwareRoot>/src/Administration/Resources/app/administration/vite.config.mts` is only responsible for the core without extensions. Currently there are a few file duplications because Vite requires different module loading order. You can recognize these files, they look like this: `*.vite.ts`. So for example the entry file `<shopwareRoot>/src/Administration/Resources/app/administration/src/index.vite.ts`.

### Building extensions

The script responsible for building all extensions is located at `<shopwareRoot>/src/Administration/Resources/app/administration/build/plugins.vite.ts`. This script uses the JS API of Vite to build all extensions. As mentioned above, it's still part of the `composer build:js:admin` command and needs no manual execution.

The script will do the following:

1. Get all bundles/plugins from the `<shopwareRoot>/var/plugins.json`
2. Call `build` from Vite for each plugin
3. The `build` function of Vite will automatically load `vite.config` files from the path of the entry file.

### Dev mode/HMR server

The command responsible for serving the application in dev mode (HMR server) is still `composer watch:admin`. For the core it's just going to take the `vite.config.mts` again and this time the `plugins.vite.ts` script will call `createServer` for each plugin.

### Loading Vite assets

Once built the right assets need to be loaded somehow into the administration. For the core we use the `pentatrion_vite` Symfony bundle. Loading the correct file(s) based on the `entrypoints.json` file generated by its counterpart `vite-plugin-symfony`. For bundles and plugins the boot process inside the `application.ts` will load and inject the entry files based on the environment.

Production build:

* Information is taken from the `/api/_info/config` call

Dev mode/HMR server:

* Information is served by our own Vite plugin `shopware-vite-plugin-serve-multiple-static` in form of the `sw-plugin-dev.json` file requested by the `application.ts`

## Vite plugins

To accomplish all this, we created a few Vite plugins and in this section we'll take the time to explain what they do. All our Vite plugin names are prefixed with `shopware-vite-plugin-`. I'll leave this out of the headlines for better readability.

### asset-path

This plugin manipulates the chunk loading function of Vite, to prepend the `window.__sw__.assetPath` to the chunk path. This is needed for cluster setups, serving the assets from a S3 bucket.

### static-assets

Copies static admin assets from `static` to the output directory so they can get served.

### serve-multiple-static

Serves static assets in dev mode (HMR server).

### vue-globals

Replacing all Vue imports in bundles/plugins to destructure from `Shopware.Vue`. This solves the problem of having multiple Vue instances. It does this by creating a temporary file exporting the Shopware.Vue and adding an alias to point every Vue import to that temporary file. This way it will result in bundled code like this:

From this:

```vue
// From this
<script setup>
import { ref } from 'vue';
</script>

// To this
<script setup>
const { ref } = window['Shopware']['Vue'];
</script>
```

### override-component

Registering `*.override.vue` files automatically. It will search for all files matching the override pattern and automatically import them into the bundle/plugin entry file. Additionally, these imports will be registered as override components by calling `Shopware.Component.registerOverrideComponent`. This will make sure that all overrides are loaded at any time as soon as the bundle/plugin script is injected. To learn more about the new overrides take a look at the Vue native docs right next to this file.

### twigjs

Transforming all `*.html.twig` files in a way that they can be loaded by Vite.

## HMR reloading

A quick note on HMR (Hot Module Replacement). Vite is only capable of reloading `*.vue` files. This means that we can only leverage the HMR by the time we transitioned everything to SFC (Single File Components) but once we do the Vite setup will be able to distinguish between changes in a plugin or the core.

## Performance

Vite is able to build the core Administration in ~18s on my system. This is a saving of over 50% compared to Webpack. In dev mode it's similar but not directly comparable. The Vite dev server starts instantly and moves the loading time to the first request. Webpack on the other hand compiles a long time upfront until the server is ready.

---

---

## Future Development Roadmap: Removing Vue Migration Build
**Source:** [guides/plugins/plugins/administration/system-updates/vue-migration-build.md](https://developer.shopware.com/docs/v6.6/guides/plugins/plugins/administration/system-updates/vue-migration-build.md)  
# Future Development Roadmap: Removing Vue Migration Build

> **Note:** The information provided in this article, including timelines and specific implementations, is subject to change.
> This document serves as a general guideline for our development direction.

## Introduction

Prior to Shopware 6.7, we utilized the Vue migration build to facilitate the transition from Vue 2 to Vue 3 for plugin developers. This approach allowed most public APIs to behave similarly to Vue 2 while enabling gradual migration.

With the release of Shopware 6.7, the Vue migration build will be removed. All plugins must be fully migrated to Vue 3 without relying on the migration build.

## Why remove the Vue migration build?

The Vue migration build was a temporary solution to help transition from Vue 2 to Vue 3. However, maintaining it indefinitely would introduce complexity, potential performance bottlenecks, and incompatibility with future Vue versions. Removing it ensures that all plugins fully adopt Vue 3, leveraging its improved reactivity system, better TypeScript support, and performance enhancements.

## Migration guide

Shopware's administration is built using Vue 3, and all plugins should be updated accordingly. We recommend referring to the official [Vue 3 migration guide](https://v3-migration.vuejs.org/) for detailed information on breaking changes and deprecations.

Below are some of the most common changes observed in our codebase. This list is not exhaustive, so always consult the official guide for comprehensive migration steps.

### Common Migration Changes

#### `$listeners` removed

In Vue 2, `$listeners` was used to access event listeners passed to a component. In Vue 3, event listeners are now included in `$attrs`.

Before (Vue 2):

```vue
<template>
    <sw-button v-on="$listeners">Click me</sw-button>
</template>
```

After (Vue 3):

```vue
<template>
    <sw-button v-bind="$attrs">Click me</sw-button>
</template>
```

More detailed guide about [`$listeners` breaking changes](https://v3-migration.vuejs.org/breaking-changes/listeners-removed.html).

#### `$scopedSlots` removed

Previously, scoped slots were accessed using `$scopedSlots`. In Vue 3, `$slots` now unifies all slots and exposes them as functions.

Before (Vue 2):

```js
this.$scopedSlots.header
```

After (Vue 3):

```js
this.$slots.header()
```

More detailed guide about [`$slots` unification breaking changes](https://v3-migration.vuejs.org/breaking-changes/slots-unification.html).

#### `$children` removed

Vue 2 allowed access to child components using `$children`. In Vue 3, this is no longer supported, and you should use template refs instead.

Before (Vue 2):

```js
this.$children.childrenMethod();
```

After (Vue 3):

```js
// <sw-child ref="childrenRef" />

this.$refs.childrenRef.childrenMethod();
```

More detailed guide about [`$children` breaking changes](https://v3-migration.vuejs.org/breaking-changes/children).

#### Some Events API removed

The methods `$on`, `$off` and `$once` are removed in Vue 3 without a replacement. You can still use `$emit` to trigger event handlers declaratively attached by a parent component.

Alternatively you can use inject/provide to pass down event handlers using a registration pattern.

It is not possible to give a general guide for this change. You need to adjust your code based on your specific use case. Here is an example how you could adjust your code:

Before (Vue 2):

```js
created() {
  this.$parent.$on('doSomething', this.eventHandler);
},

beforeDestroy() {
  this.$parent.$off('doSomething', this.eventHandler);
}
```

After (Vue 3):

```js
// The parent component needs to provide the event handler
inject: ['registerDoSomething', 'unregisterDoSomething'],

created() {
  this.registerDoSomething(this.eventHandler);
},

beforeDestroy() {
  this.unregisterDoSomething(this.eventHandler);
}
```

More detailed guide about [Events API breaking changes](https://v3-migration.vuejs.org/breaking-changes/events-api.html).

#### `$set`, `$delete` removed

Vue 2 required `$set` and `$delete` for reactive property modifications. Vue 3’s new reactivity system, based on ES6 Proxies, removes the need for these methods.

Before (Vue 2):

```js
this.$set(this.myObject, 'key', 'value');
this.$delete(this.myObject, 'key');
```

After (Vue 3):

```js
this.myObject.key = 'value';
delete this.myObject.key;
```

## Conclusion

With Shopware 6.7, the Vue migration build will be fully removed. To ensure compatibility, all plugins must be updated to Vue 3 following the official migration guide. If you encounter challenges during migration, refer to the official Vue 3 documentation or seek assistance from the Shopware developer community.

---

---

## Future Development Roadmap: Moving Towards Vue Native
**Source:** [guides/plugins/plugins/administration/system-updates/vue-native.md](https://developer.shopware.com/docs/v6.6/guides/plugins/plugins/administration/system-updates/vue-native.md)  
# Future Development Roadmap: Moving Towards Vue Native

> **Note:** The information provided in this article, including timelines and specific implementations, is subject to change.
> This document serves as a general guideline for our development direction.

## Introduction

We are planning a significant shift in our development approach, moving towards a more native Vue.js implementation.
This document outlines the reasons for this change and provides an overview of our upgrade path.

## Current status

To better understand the changes described in this article, let's recap the current status.
The Shopware 6 Administration is built around Vue.js with several custom systems on top to allow for extensions.

### Custom component registration

```javascript
Shopware.Component.register('sw-component', {
    template,

    //...
});
```

### Custom templates with Twig.Js

```html
{% block sw-component %}
    <sw-card></sw-card>
{% endblock %}
```

## Why Go Native?

Our transition to a more native Vue.js approach is driven by several key factors:

1. **Improved Developer Experience**
   * Devtool enhancements
   * Easier maintenance

2. **Future-Proofing**
   * Aligning with Vue 3 and potential future versions
   * Preparing for upcoming industry standards

3. **Performance Optimization**
   * Leveraging native Vue.js capabilities for better performance

## Major Changes

### 1. Moving from Options API to Composition API

#### Why Make This Change?

We aim to better align with Vue's ecosystem, to minimize the amount of specifications new Developers need to learn.
The Composition API has become the new standard for Vue's documentation and projects all over Github.
Renowned libraries like `vue-i18n` are dropping support of the Options API, as seen in their [migration guide](https://vue-i18n.intlify.dev/guide/migration/vue3#summary), and we expect similar transitions from other tools in the ecosystem.
This also aligns with Vue's best practices, as highlighted in the official [Composition API FAQ](https://vuejs.org/guide/extras/composition-api-faq.html#why-composition-api).

#### What Will Change?

We will gradually transform our components from Options API to Composition API. Together with native blocks, this builds the foundation to use Single File Components (SFC).
The transformation will be stretched over multiple major versions to offer enough time for all of us to adapt. Take a look at the estimated timeline below.

#### Upgrade Path

| Shopware Version | Options API                     | Composition API              |
|:----------------:|---------------------------------|------------------------------|
|       6.7        | Standard                        | Experimental                 |
|       6.8        | Still supported for extensions\* | Standard for Core components |
|       6.9        | Removed completely              | Standard                     |

\*Extensions still can register components using the Options API; overwriting Core components needs the Composition API.

### 2. TwigJS to Native Blocks

#### Why Make This Change?

Vue has no native support for blocks like in Twig.js. Vue has slots, but slots don't work like blocks.
Recently, we accomplished the unthinkable and found a way to implement blocks with native Vue components.
This will allow us to finally use SFC and keep the extendability of Twig.js.
Lowering the learning curve, as the Twig.js syntax is especially unfamiliar to Vue developers.
Standard tooling like VSCode, ESLint, and Prettier will work out of the box.

#### What Will Change?

We will gradually transform all component templates from external `*.html.twig` files with Twig.Js into `.vue` files using the native block implementation.

#### Upgrade Path

| Shopware Version | Twig.Js                         | Native blocks                |
|:----------------:|---------------------------------|------------------------------|
|       6.7        | Standard                        | Experimental                 |
|       6.8        | Still supported for extensions\* | Standard for Core components |
|       6.9        | Removed completely              | Standard                     |

\*Extensions still can register components using Twig.Js templates; overwriting Core blocks needs the native block implementation.

### 3. Vuex to Pinia

#### Why Make This Change?

Vuex has been the default State management for Vue 2. For Vue 3 Pinia took it's place.

#### What Will Change?

We will move all core Vuex states to Pinia stores. The public API will change from `Shopware.State` to `Shopware.Store`.

#### Upgrade Path

| Shopware Version | Vuex                            | Pinia                        |
|:----------------:|---------------------------------|------------------------------|
|       6.7        | Still supported for extensions\* | Standard for Core components |
|       6.8        | Removed completely              | Standard                     |

\*Extensions still can register Vuex states; Accessing core stores is done via Pinia

## Example: Component Evolution

Now let's take a look how core and extension components will evolve.

### Shopware 6.7

First we start with the current status which is still compatible with Shopware 6.7.

#### Core component

In the core we register a component via `Shopware.Component.register`.

```javascript
Shopware.Component.register('sw-text-field', {
   template: `
     {% block sw-text-field %}
       <input type=text v-model="value" @change="onChange">
     {% endblock %}
   `,
   
   data() {
       return {
           value: null,
       }
   },
   
   methods: {
       onChange() {
           this.$emit('update:value', this.value);
       }
   },
});
```

#### Extension override

The extension overrides the component via `Shopware.Component.override`.

```javascript
Shopware.Component.override('sw-text-field', {
   template: `
     {% block sw-text-field %}
       {% parent %}
       
       {{ helpText }}
     {% endblock %}
   `,
   
   props: {
       helpText: {
           type: String,
           required: false,
       }
   }
})
```

#### Extension new component

The extension adds additional component via `Shopware.Component.register`.

```javascript
Shopware.Component.register('your-crazy-ai-field', {
   template: `
     {% block your-crazy-ai-field %}
       {# ... #}
     {% endblock %}
   `,

   // Options API implementation
})
```

### Shopware 6.8

With Shopware 6.8 the core uses single file components with the composition API.

#### Core component

The core component is added via a single file component `*.vue` file.

```vue
<template>
   {# Notice native block comonent instead of twig blocks #}
   <sw-block name="sw-text-field">
    <input type=text v-model="value" @change="onChange">
   </sw-block>
</template>

<script setup>
// Notice Composition API imports
import { ref, defineEmits } from 'vue';

// Notice new extension system Shopware.Component.createExtendableSetup
const {value, onChange, privateExample} = Shopware.Component.createExtendableSetup({
   props,
   context,
   name: 'originalComponent',
}, () => {
   const emit = defineEmits(['update:value']);

   const value = ref(null);
   const onChange = () => {
      emit('update:value', value.value)
   }

   const privateExample = ref('This is a private property');

   return {
      public: {
         value,
         onChange,
      },
      private: {
         privateExample,
      }
   };
});
</script>
```

#### Extension override

For overrides we created a new convention. They must match the `*.override.vue` pattern.
`*.override.vue` files will be loaded automatically in your main entry file.

```vue
<template>
{# Notice the native block components #}
<sw-block extends="sw-text-field">
   <sw-block-parent/>
   
   {{ helpText}}
</sw-block>
</template>

<script setup>
// Notice Composition API imports
import { defineProps } from 'vue';

// This file would also use Shopware.Component.overrideComponentSetup
// if it would change the existing public API
const props = defineProps({
   helpText: {
       type: String,
       required: false,
   },
});
</script>
```

#### Extension new component

```javascript

// For this you would also have the option to use a `*.vue` file but you don't have to
Shopware.Component.register('your-crazy-ai-field', {
   template: `
     {% block your-crazy-ai-field %}
       {# ... #}
     {% endblock %}
   `,

   // Options API implementation
})
```

### Shopware 6.9

The only difference for 6.9 is that you can no longer register new components via `Shopware.Component.register`.

## FAQ

**Will existing extensions built with Options API continue to work in Shopware 6.8?**

When you only use `Shopware.Component.register` yes. If you also use `Shopware.Component.extend/ override` you need to use the composition API extension approach for that.

**How can I prepare my development team for the transition to Composition API?**

I would recommend building a simple Vue application using the Composition API. You can do so by following [official guides](https://vuejs.org/guide/extras/composition-api-faq.html).

**What advantages does the native block implementation offer over the current Twig.js system?**

It works with native Vue.Js components, therefore is compatible with default tooling.

**Can I mix Composition API and Options API components during the transition period?**

Yes as long as you stick to the limitations from the upgrade paths.

**How will the migration from Twig.js templates to .vue files affect my existing component overrides?**

You need to migrate all your overrides with Shopware 6.8.

**What tools or resources will be available to help migrate existing components?**

We'll try to provide a code mod to transition your components into SFC. This will not work for all edge cases, so you need to manually check and transition them.

**Will there be any performance impact during the transition period when both systems are supported?**

During our tests we didn't experience any performance issues.

**How does the new `Shopware.Component.createExtendableSetup` function work with TypeScript?**

It has built in TypeScript support.

**What happens to existing extensions using Twig.js templates after version 6.9?**

They will stop working with Shopware version 6.9.

**Can I start using the native blocks and Composition API in my extensions before version 6.8?**

Yes! You can add new components using SFC and native blocks. But you can't extend core components using the old systems or vise versa.

**Which extensions are affected by these changes?**

* Apps aren't affected at all
* Plugins need to respect the discussed changes

---

---

## Add custom styles
**Source:** [guides/plugins/plugins/administration/templates-styling/add-custom-styles.md](https://developer.shopware.com/docs/v6.6/guides/plugins/plugins/administration/templates-styling/add-custom-styles.md)  
# Add custom styles

## Overview

All components contain own templates and some style. Of course, you may want to use your custom styles in your component or module. In this guide, we got you covered on how to add those custom styles to your components.

## Prerequisites

However, this guide does not explain how to create a custom component, so head over to the official guide about creating a custom component to learn this first.

In addition, you need to have a basic knowledge of CSS and SCSS in order to use custom styles. This is though considered a basic requirement and won't be taught in this guide.

### Example: Custom cms block

We will base our guide on an example: Let's use a custom component printing out "Hello world!". So first of all, create a new directory for your`sw-hello-world`. As said before, more information about that topic, such as where to create this directory, can be found in [Add a custom component](../module-component-management/add-custom-component.md).

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

* [Writing templates](../templates-styling/writing-templates.md)
* [Add shortcuts](https://github.com/shopware/docs/tree/575c2fa12ef272dc25744975e2f1e4d44721f0f1/guides/plugins/plugins/administration/add-shortcuts.md)

---

---

## Adding snippets
**Source:** [guides/plugins/plugins/administration/templates-styling/adding-snippets.md](https://developer.shopware.com/docs/v6.6/guides/plugins/plugins/administration/templates-styling/adding-snippets.md)  
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
When you do not build a module and therefore do not fit into the suggested directory structure, you can still place the translation files anywhere in `<plugin root>/src/Resources/app/administration/src/`.
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

Or use `Shopware.Snippet.tc('swag-example.general.myCustomText')` when `this` doesn't point to a component (see also [Vue3 upgrade](../../../../../resources/references/upgrades/administration/vue3.md))

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

* [Learning about the global Shopware object](../data-handling-processing/the-shopware-object.md)
* [Learning about the VueX state](https://github.com/shopware/docs/tree/575c2fa12ef272dc25744975e2f1e4d44721f0f1/guides/plugins/plugins/administration/using-vuex-state.md)

---

---

## Using assets
**Source:** [guides/plugins/plugins/administration/templates-styling/using-assets.md](https://developer.shopware.com/docs/v6.6/guides/plugins/plugins/administration/templates-styling/using-assets.md)  
# Using assets

## Overview

When working with an own plugin, the usage of own custom images or other assets is a natural requirement. So of course you can do that in Shopware as well. In this guide we will explore how you can add custom assets in your plugin in order to use them in the Administration.

## Prerequisites

In order to be able to start with this guide, you need to have an own plugin running. As to most guides, this guide is also built upon the Plugin base guide:

Needless to say, you should have your image or another asset at hand to work with.

## Add custom assets

In order to add your own custom assets, you need to save your assets in the `Resources/app/administration/static` folder.

```bash
# PluginRoot
.
├── composer.json
└── src
    ├── Resources
    │   ├── app
    │       └── administration
    │             └── static
    │                   └── your-image.png <-- Asset file here
    └── SwagBasicExample.php
```

Similar as in [using custom assets in Storefront](../../storefront/add-custom-assets.md), you need to execute the following command:

```bash
// 
bin/console assets:install
```

This way, your plugin assets are copied to the `public/bundles` folder:

```bash
# shopware-root/public/bundles
.
├── administration
├── framework
├── storefront
└── swagbasicexample
    └── your-image.png <-- Your asset is copied here
```

## Use custom assets in the Administration

After adding your assets to the `public/bundles` folder, you can start using them in the Administration. Simply utilize the `asset` filter.

:::warning
Note that [Vue filters](https://vuejs.org/v2/guide/filters.html) are no longer supported in Vue3 and therefore they will not function in Shopware versions 6.6 and above.
:::

Create a computed component to make them easy to use in your template.

```javascript
computed: {
    assetFilter() {
        return Shopware.Filter.getByName('asset');
    },
}
```

```html
<img :src="assetFilter('/<plugin root>/static/your-image.png')">
```

You're able to use this line in your `twig`/`html` files as you please and that's basically it. You successfully added your own asset to the Administration.

---

---

## Writing templates
**Source:** [guides/plugins/plugins/administration/templates-styling/writing-templates.md](https://developer.shopware.com/docs/v6.6/guides/plugins/plugins/administration/templates-styling/writing-templates.md)  
# Writing templates

## Overview

The Shopware 6 Administration uses a combination of [twig](https://twig.symfony.com/) and [Vue](https://vuejs.org/) templates in its Administration to provide easy extensibility. This guide will teach you how to use templates to extend the Administration with twig and Vue and how import them into a component.

## Prerequisites

All you need for this guide is a running Shopware 6 instance and full access to both the files and a registered module. Of course you'll have to understand JavaScript, but that's a prerequisite for Shopware as a whole and will not be taught as part of this documentation.

## Writing a template

Templates in Shopware are usually defined in a separate `.twig` file, named after the component, in the component's directory. Each module's page should start with the `sw-page` component, because it provides a search bar, a page header and a `content` slot for your content. Components in general should also include twig blocks, in order to be extendable by other plugins.

Let's look at all of this in practice, with the example of a component statically printing `'Hello World'`:

```html
{% block swag_basic_example_page %}
    <sw-page class="swag-example-list">
        <template #content>
            <h2>Hello world!</h2>
        </template>
    </sw-page>
{% endblock %}
```

## Setting the Template

Each component has a template property, which is used to set the template. To use the previously created template file, import it and assign it to the `template` property of the component.

```javascript
import template from './swag-basic-example.html.twig';

Shopware.Component.register('swag-basic-example', {
    template, // ES6 shorthand for: 'template: template'  

    metaInfo() {
        return {
            title: this.$createTitle()
        };
    },
});
```

Note: The meta info is part of [vue-meta](https://vue-meta.nuxtjs.org/) and is used to set the title of the whole page. The `this.$createTitle()` generates a title.

## Theory: Vue vs Twig

The Shopware 6 Administration mixes, as mentioned in the beginning, [twig](https://twig.symfony.com/) and [Vue](https://vuejs.org/) to provide extensibility. But for what is twig used and for what is Vue used?

Generally speaking, twig is used for **extending** from another template and adjusting it to your needs. For example overriding a twig block could provide a hook to place your own markup. But be careful overrides apply to all occurrences of this template.

Vue is used to link the data and the DOM to make them reactive. Learn about Vue and its capabilities [here](https://vuejs.org/v2/guide/index.html).

## More interesting topics

* [Add custom styling](../templates-styling/add-custom-styles.md)
* [Adding shortcuts](../advanced-configuration/add-shortcuts.md)

---

## The Sanitizer helper
**Source:** [guides/plugins/plugins/administration/the-sanitizer-helper.md](https://developer.shopware.com/docs/v6.5/guides/plugins/plugins/administration/the-sanitizer-helper.md)  
# The Sanitizer helper

## Overview

The Shopware 6 Sanitizer Helper is a wrapper around [`DOMPurify`](https://github.com/cure53/DOMPurify), which is used to sanitize HTML in order to prevent `XSS attacks`.

## Where is it registered?

The Sanitizer Helper is registered to the [Shopware Global Object](./the-shopware-object) and therefore can be accessed anywhere in your plugin.

```javascript
const sanitizer = Shopware.Helper.SanitizerHelper; 
```

It also is registered in the Vue prototype as seen [here](https://github.com/shopware/shopware/blob/trunk/src/Administration/Resources/app/administration/src/app/plugin/sanitize.plugin.js).
This means it can also be accessed in your components like this:

```javascript
const Sanitizer = this.$sanitizer;
const sanitize = this.$sanitize;
```

## Sanitizing HTML

As mentioned before the `SanitizerHelper` is registered to the [Shopware Global Object](./the-shopware-object) and therefore can be accessed like this everywhere:

```javascript
Shopware.Helper.SanitizerHelper.sanitize('<img src=x onerror=alert(1)//>'); // becomes <img src="x">
```

And since it is bound to the Vue prototype it can be used in all Vue components like this:

```javascript
this.$sanitizer.sanitize('<svg><g/onload=alert(2)//<p>'); // becomes <svg><g></g></svg>
this.$sanitize('<img src=x onerror=alert(1)//>'); // becomes <img src="x">
```

## How to set the config

The config can be set with the `setConfig` and cleared with the `clearConfig` function, as seen below:

```javascript
Shopware.Helper.SanitizerHelper.setConfig({
    USE_PROFILES: { html: true }
});

Shopware.Helper.SanitizerHelper.clearConfig()
```

See all of the configuration options [here](https://github.com/cure53/DOMPurify#can-i-configure-dompurify)

## How to add hooks

The aforementioned Wrapper also provides functions to add and remove hooks to DOMPurify.
Learn what DOMPurify hooks are in their [documentation](https://github.com/cure53/DOMPurify#hooks).

```javascript
Shopware.Helper.SanitizerHelper.addMiddleware('beforeSanitizeElements',  function (
        currentNode,
        hookEvent,
        config
    ) {
        // Do something with the current node and return it
        // You can also mutate hookEvent (i.e. set hookEvent.forceKeepAttr = true)
        return currentNode;
    }
);

Shopware.Helper.SanitizerHelper.removeMiddleware('beforeSanitizeElements');
```

---

---

## The Shopware object
**Source:** [guides/plugins/plugins/administration/the-shopware-object.md](https://developer.shopware.com/docs/v6.5/guides/plugins/plugins/administration/the-shopware-object.md)  
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

Learn more about them here: [Creating administration component](add-custom-component)

## Module

The `Module` property of the global `Shopware` contains the module registry. A `Module` is an encapsulated unit of routes and pages, which implements a whole feature. For example there are modules for customers, orders, settings, etc.

```javascript
const { Module } = Shopware;

Module.register('your-module', {});
```

Learn more about them here: [Creating administration module](add-custom-module)

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

![TypeScript declarations example](../../../../assets/typescript-declaration-shopware-module.gif)

In the example above you can see how the TypeScript declarations are helping you to register a module. It automatically marks your code and points out what is missing.

## Next steps

As you might have noticed, the `Shopware` object can be used in a lot of cases. Besides registering components and modules, here are some guides about [adding filters](add-filter), about [adding mixins](add-mixins) and about [using our utils](using-utils) - all by using the Shopware object.

---

---

## Adding responsive behavior
**Source:** [guides/plugins/plugins/administration/ui-ux/adding-responsive-behavior.md](https://developer.shopware.com/docs/v6.6/guides/plugins/plugins/administration/ui-ux/adding-responsive-behavior.md)  
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

## Using assets
**Source:** [guides/plugins/plugins/administration/using-assets.md](https://developer.shopware.com/docs/v6.5/guides/plugins/plugins/administration/using-assets.md)  
# Using assets

## Overview

When working with an own plugin, the usage of own custom images or other assets is a natural requirement. So of course you can do that in Shopware as well. In this guide we will explore how you can add custom assets in your plugin in order to use them in the Administration.

## Prerequisites

In order to be able to start with this guide, you need to have an own plugin running. As to most guides, this guide is also built upon the Plugin base guide:

Needless to say, you should have your image or another asset at hand to work with.

## Add custom assets

In order to add your own custom assets, you need to save your assets in the `Resources/app/administration/static` folder.

```bash
# PluginRoot
.
├── composer.json
└── src
    ├── Resources
    │   ├── app
    │       └── administration
    │             └── static
    │                   └── your-image.png <-- Asset file here
    └── SwagBasicExample.php
```

Similar as in [using custom assets in Storefront](../storefront/add-custom-assets), you need to execute the following command:

```bash
// 
bin/console assets:install
```

This way, your plugin assets are copied to the `public/bundles` folder:

```bash
# shopware-root/public/bundles
.
├── administration
├── framework
├── storefront
└── swagbasicexample
    └── your-image.png <-- Your asset is copied here
```

## Use custom assets in the Administration

After adding your assets to the `public/bundles` folder, you can start using your assets in the Administration. Basically, you just need to use the Vue [filter](https://vuejs.org/v2/guide/filters.html) `asset`.

```html
<img :src="'/<plugin root>/static/your-image.png' | asset">
```

You're able to use this line in your `twig`/`html` files as you please and that's basically it. You successfully added your own asset to the Administration.

---

---

## Using base components
**Source:** [guides/plugins/plugins/administration/using-base-components.md](https://developer.shopware.com/docs/v6.5/guides/plugins/plugins/administration/using-base-components.md)  
# Using base components

The Shopware 6 Administration comes with a bunch of tailored Vue components, already accessible in all of your templates via the `component registry`. This guide will show you how you can use Shopware-made components in your templates, if you want to learn more about the `component registry` and how you can register your own components to it have a look at the [corresponding guide](add-custom-component)

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

That's basically it. To continue building beautiful custom components, learn how to write templates and how to include them in your components [here](writing-templates)

---

---

## Using custom fields
**Source:** [guides/plugins/plugins/administration/using-custom-fields.md](https://developer.shopware.com/docs/v6.5/guides/plugins/plugins/administration/using-custom-fields.md)  
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

