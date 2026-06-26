# ADMINISTRATION UI

Compiled excerpts from the Shopware Developer Documentation snapshot. Prefer live docs at [developer.shopware.com](https://developer.shopware.com/) when in doubt.

---

## Using the data handling
**Source:** [guides/plugins/plugins/administration/using-data-handling.md](https://developer.shopware.com/docs/v6.5/guides/plugins/plugins/administration/using-data-handling.md)  
*(Body truncated in this bundle; follow the link for the rest.)*

# Using the data handling

The Shopware 6 Administration allows you to fetch and write nearly everything in the database. This guide will teach you the basics of the data handling.

## Prerequisites

All you need for this guide is a running Shopware 6 instance and full access to both the files, as well as the command line and preferably registered module. Of course you'll have to understand JavaScript, but that's a prerequisite for Shopware as a whole and will not be taught as part of this documentation.

Considering that the data handling in the Administration is remotely operating the Data Abstraction Layer its highly encouraged to read the articles [Reading data with the DAL](../framework/data-handling/reading-data) and [Writing data with the DAL](../framework/data-handling/writing-data).

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

To fetch data from the server, the repository has a `search` function. Each repository function requires the API `context` and `criteria` class, which contains all functionality of the core criteria class. If you want to see all the options take a look at the file `src/Administration/Resources/app/administration/src/core/data/criteria.data.js`.

```javascript
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
Shopware.Component.register('swag-basic-example', {
    inject: ['repositoryFactory'],

    template,

    data: function () {
        return {
            product: undefined
        };
    },

    computed: {
        productRepository() {
            return this.repositoryFactory.create('product');
        },
        productCriteria() {
            const criteria = new Crit

… **Truncated.** Full document: https://developer.shopware.com/docs/v6.5/guides/plugins/plugins/administration/using-data-handling.md


---

## Using filter
**Source:** [guides/plugins/plugins/administration/using-filter.md](https://developer.shopware.com/docs/v6.5/guides/plugins/plugins/administration/using-filter.md)  
# Using filter

## Overview

In this guide you'll learn how to use filters in the Shopware Administration.

## Prerequisites

This guide requires you to already have a basic plugin running. If you don't know how to do this in the first place, have a look at our [Plugin base guide](../plugin-base-guide).

Furthermore you should have a look at our [add filter](add-filter) guide, since this guide is built upon it.

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

## Using Mixins
**Source:** [guides/plugins/plugins/administration/using-mixins.md](https://developer.shopware.com/docs/v6.5/guides/plugins/plugins/administration/using-mixins.md)  
# Using Mixins

## Overview

This documentation chapter will cover how to use an existing Administration mixin in your plugin. Generally, mixins behave the same as they do in Vue normally, differing only in the registration and the way mixins are included in a component.

## Prerequisites

All you need for this guide is a running Shopware 6 instance and full access to both the files and a running plugin. Of course you'll have to understand JavaScript, but that's a prerequisite for Shopware as a whole and will not be taught as part of this documentation. As stated before mixins in Shopware are basically the same as in Vue, so you should have read their [documentation](https://vuejs.org/v2/guide/mixins.html) on them first.

## Finding a mixin

The Shopware 6 Administration comes with a few predefined [mixins](../../../../resources/references/administration-reference/mixins.md)

If you want to learn how to create your own mixin look at this guide: [Creating mixins](add-mixins)

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

## Using the data grid component
**Source:** [guides/plugins/plugins/administration/using-the-data-grid-component.md](https://developer.shopware.com/docs/v6.5/guides/plugins/plugins/administration/using-the-data-grid-component.md)  
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

This template will be used in a new component. Learn how to override existing components [here](customizing-components) .

## Declaring the data

Since this is a very basic example the following code will just statically assign data to the `dataSource` and `columns` data attribute. If you want to load data and render that instead, please consult the guide [How to use the data handling](using-data-handling)

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

* [Using base components](using-base-components)

---

---

## Using utility functions
**Source:** [guides/plugins/plugins/administration/using-utils.md](https://developer.shopware.com/docs/v6.5/guides/plugins/plugins/administration/using-utils.md)  
# Using utility functions

Utility functions in the Shopware 6 Administration are registered to [the Shopware object](the-shopware-object) and are therefore accessible everywhere in the Administration. They provide many useful [shortcuts](../../../../resources/references/administration-reference/utils.md) for common tasks.

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

* [Adding filters](add-filter)
* [Adding mixins](add-mixins)

---

---

## Using Vuex Stores
**Source:** [guides/plugins/plugins/administration/using-vuex-state.md](https://developer.shopware.com/docs/v6.5/guides/plugins/plugins/administration/using-vuex-state.md)  
# Using Vuex Stores

## Overview

The Shopware 6 Administration uses [Vuex](https://vuex.vuejs.org/) stores to keep track of complex state, while just adding a wrapper around it.
Learn what Vuex is, how to use it and when to use it from their great [documentation](https://vuex.vuejs.org/).
This guide will show you how to use Vuex as you normally would, through the interfaces provided by the Shopware 6 Administration.

## Prerequisites

All you need for this guide is a running Shopware 6 instance, the files and preferably a registered module.
Of course you'll have to understand JavaScript and have a basic familiarity with [Vue](https://vuejs.org/) the framework used in the Administration and it's flux library [Vuex](https://vuex.vuejs.org/).

## Creating a store

Creating a store works the same way as it would in standard Vuex with the only limitation being, that all stores have to be `namespaced` in order to prevent collisions with other third party plugins or the Shopware 6 Administration itself.

The following code snippet is the `namespaced` store we will register later through Shopware to the underlying Vuex.
It is admittedly rather short and has only one variable called `content` and a setter for it, but again this all the same as in Vuex. Beware of the property `namespaced`, though.

```javascript
// <plugin-root>/src/Resources/app/administration/app/src/component/store-example/store.js
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

## Registering the store

The store can be registered in two scopes, on a module scope and on a per component scope.
Both ways use the same functions from the [Shopware object](./the-shopware-object) to register and unregister the `namespaced store modules`.

Registering in a module scope is done by simply calling the function `Shopware.State.registerModule` in the `main.js` file.

```javascript
// <administration root>/src/main.js
import swagBasicState from './store';

Shopware.State.registerModule('swagBasicState', swagBasicState);
```

In the component scope `Namespaced` store modules can be registered in the `beforeCreate` [Vue lifecycle hook](https://vuejs.org/v2/guide/instance.html#Lifecycle-Diagram),
with the previously mentioned `Shopware.State.registerModule` function.
But then they also need to be `unregistered` in the `beforeDestroy` Vue lifecycle hook,
in order to not leave unused stores behind after a component has been destroyed.

All of this can be seen in the following code sample:

```javascript
// <plugin-root>/src/Resources/app/administration/app/src/component/store-example/index.js
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

Both methods make the store on the given name everywhere available, regardless of where it has been registered.

## Using the store in a component

The Shopware object also makes the native Vuex helper functions available, like [`mapState`](https://vuex.vuejs.org/guide/state.html#the-mapstate-helper), [`mapGetters`](https://vuex.vuejs.org/guide/getters.html#the-mapgetters-helper), [`mapMutations`](https://vuex.vuejs.org/guide/mutations.html#committing-mutations-in-components) and [`mapActions`](https://vuex.vuejs.org/guide/actions.html#dispatching-actions-in-components).
The `namespaced` store itself can be accessed through the `Shopware.State.get()` function.

```javascript
// <plugin-root>/src/Resources/app/administration/app/src/component/store-example/index.js
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

## Adding a template

After we have registered our `namespaced` store, mapped state and mutations, we can now use them in our components or templates.
The component below displays the previously mapped state `content` in a `div` and a `sw-text-field`, mutating the state on the `changed` event of the `sw-text-field`.

```html
// <plugin-root>/src/Resources/app/administration/app/src/component/store-example/store-example.html.twig
<div>
    <h1>SW-6 State</h1>
    <sw-text-field @change="value => setContent(value)" :value="content">
    </sw-text-field>
    <div>
        {{ content }}
    </div>
</div>
```

## More interesting topics

* [The Shopware object](./the-shopware-object).

---

---

## Writing templates
**Source:** [guides/plugins/plugins/administration/writing-templates.md](https://developer.shopware.com/docs/v6.5/guides/plugins/plugins/administration/writing-templates.md)  
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
        <template slot="content">
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

Vue is used to link the data and the DOM in order to make them reactive. Learn about Vue and its capabilities [here](https://vuejs.org/v2/guide/index.html).

## More interesting topics

* [Add custom styling](add-custom-styles)
* [Adding shortcuts](https://github.com/shopware/docs/tree/575c2fa12ef272dc25744975e2f1e4d44721f0f1/guides/plugins/plugins/administration/add-shortcuts.md)

---

---

## resources/meteor-icon-kit.md
**Source:** [resources/meteor-icon-kit.md](https://developer.shopware.com/resources/meteor-icon-kit.md)  
---

---

