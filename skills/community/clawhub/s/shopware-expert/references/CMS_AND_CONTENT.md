# CMS AND CONTENT

Compiled excerpts from the Shopware Developer Documentation snapshot. Prefer live docs at [developer.shopware.com](https://developer.shopware.com/) when in doubt.

---

## Content
**Source:** [guides/plugins/plugins/content.md](https://developer.shopware.com/docs/v6.6/guides/plugins/plugins/content.md)  
# Content

Content feature in Shopware encompasses the essential capabilities related to managing and enhancing content within the e-commerce platform, including content management, email management, SEO optimization, sitemap generation, and media management. These functions enhance website content, facilitate effective communication, improve search engine visibility, and streamline media organization within the e-commerce platform. While these functions are typically available within the core Shopware system, plugins offer the flexibility to extend or customize them based on specific business needs and content strategies.

---

---

## CMS
**Source:** [guides/plugins/plugins/content/cms.md](https://developer.shopware.com/docs/v6.6/guides/plugins/plugins/content/cms.md)  
# CMS

In general, Shopware CMS creates and manages content using blocks and elements.

The CMS plugin allows you to easily add and organize these CMS blocks, which are reusable sections of content that can be placed on multiple pages. You can customize the appearance and layout of these blocks. To create engaging and visually appealing pages within these blocks, you can add and configure various content elements such as text, images, videos, sliders, and more. Additionally, the CMS plugin enables you to add data to their content elements, such as product information, categories, or dynamic content from APIs.

Furthermore, the CMS feature core functions can be accessed and managed through the Shopware Admin SDK. This provides developers with tools and APIs to interact with the CMS functionality, allowing for more advanced customization.

Overall, the plugin facilitates you to create, customize, and manage engaging content on your website. Through blocks, elements, and the flexibility the Admin SDK provides, businesses can create visually appealing pages with dynamic and relevant content to enhance the user experience.

---

---

## Add CMS Block
**Source:** [guides/plugins/plugins/content/cms/add-cms-block.md](https://developer.shopware.com/docs/v6.6/guides/plugins/plugins/content/cms/add-cms-block.md)  
*(Body truncated in this bundle; follow the link for the rest.)*

# Add CMS Block

## Overview

This guide will teach you how to create your very own CMS block with your plugin.

## Prerequisites

This plugin is built upon our plugin from the [Plugin base guide](../../plugin-base-guide), but the examples mentioned here are applicable to every valid Shopware 6 plugin. Also, you should know how to handle the "Shopping Experiences" module in the Administration first. Furthermore, you definitely need to know how to create a custom component in the Administration, which is covered here [Creating a component](../../administration/add-custom-component).

## Custom block in the Administration

Let's get started with adding your first custom block. By default, Shopware 6 comes with several blocks, such as a block called `image_text`. It renders an image element on the left side and a simple text element on the right side. In this guide, you're going to create a new block to swap those two elements, so the text is on the left side and the image on the right side.

All blocks can be found in the directory [/src/Administration/Resources/app/administration/src/module/sw-cms/blocks](https://github.com/shopware/shopware/tree/v6.3.4.1/src/Administration/Resources/app/administration/src/module/sw-cms/blocks). In there, they are divided into the categories `commerce`, `form`, `image`, `sidebar`, `text-image`, `text` and `video`.

`commerce` : Blocks using a special template can be found here, e.g. a product slider block.

`form` : A single block displaying a form, mainly the `contact` or the `newsletter` form.

`image` : Only image elements are used by these blocks.

`sidebar` : Blocks for the sidebar, such as the listing filters or the category navigation.

`text-image` : Blocks, that are making use of both, text and images, belong here.

`text` : Blocks only using text elements are located here.

`video` : Our blocks for youtube and vimeo videos reside here.

### Injecting into the Administration

The main entry point to customize the Administration via plugin is the `main.js` file. It has to be placed into a `<plugin root>/src/Resources/app/administration/src` directory in order to be automatically found by Shopware 6.

Create this `main.js` file for now, it will be used later.

### Registering a new block

Your plugin's structure should always match the core's structure. When thinking about creating a new block, you should recreate the directory structure of core blocks in your plugin. The block, which you're going to create, consists of an `image` and a `text` element, so it belongs to the category `text-image`. Thus, create the directory `<plugin root>/src/Resources/app/administration/src/module/sw-cms/blocks/text-image`.

In there, you have to create a new directory for each block you want to create, the directory's name representing the block's name. For this example, the name `my-image-text-reversed` is going to be used, so create this directory in there.

Now create a new file `index.js` inside the `my-image-text-reversed` directory, since it will be automatically loaded when importing this block in your `main.js`. Speaking of that, right after having created the `index.js` file, you can actually import your new block directory in the `main.js` file already:

```javascript
// <plugin root>/src/Resources/app/administration/src/main.js
import './module/sw-cms/blocks/text-image/my-image-text-reversed';
```

Back to your `index.js`, which is still empty. In order to register a new block, you have to call the `registerCmsBlock` method of the [cmsService](https://github.com/shopware/shopware/blob/v6.3.4.1/src/Administration/Resources/app/administration/src/module/sw-cms/service/cms.service.js). Since it's available in the Dependency Injection Container, you can fetch it from there.

First of all, access our `Application` wrapper, which will grant you access to the DI container. This `Application` wrapper has access to the DI container, so go ahead and fetch the `cmsService` from it and call the mentioned `registerCmsBlock` method.

```javascript
// <plugin root>/src/Resources/app/administration/src/module/sw-cms/blocks/text-image/my-image-text-reversed/index.js
Shopware.Service('cmsService').registerCmsBlock();
```

#### The configuration object

The method `registerCmsBlock` takes a configuration object, containing the following necessary data:

`name` : The technical name of your block. Will be used for the template and component loading later on.

`label` : A name to be shown for your block in the User Interface.

`category` : The category this block belongs to.

`component` : The Vue component to be used when rendering your actual block in the Administration sidebar.

`previewComponent` : The Vue component to be used in the "list of available blocks". Just shows a tiny preview of what your block would look like if it was used.

`defaultConfig` : A default configuration to be applied to this block. Must be an object containing those default values.

`slots` : Key-value pair to configure which element to be shown in which slot. Will be explained in the next few steps when creating a template for this block.

Go ahead and create this configuration object yourself. Here's what it should look like after having set all of those options:

```javascript
// <plugin root>/src/Resources/app/administration/src/module/sw-cms/blocks/text-image/my-image-text-reversed/index.js
Shopware.Service('cmsService').registerCmsBlock({
    name: 'my-image-text-reversed',
    category: 'text-image',
    label: 'My Image Text Block!',
    component: 'sw-cms-block-my-image-text-reversed',
    previewComponent: 'sw-cms-preview-my-image-text-reversed',
    defaultConfig: {
        marginBottom: '20px',
        marginTop: '20px',
        marginLeft: '20px',
        marginRight: '20px',
        sizingMode: 'boxed'
    },
    slots: {
        left: 'text',
        right: 'image'
    }
});
```

The `component` and `previewComponent` do not exist yet, but they are created later in this guide. The `defaultConfig` just gets some minor margins and the sizing mode 'boxed', which will result in a CSS class [is--boxed](https://github.com/shopware/shopware/blob/v6.3.4.1/src/Administration/Resources/app/administration/src/module/sw-cms/component/sw-cms-block/sw-cms-block.scss) being applied to that block later. The slots are defined by an object, where the key represents the slot's name and the value being the technical name of the element to be used in this slot. This will be easier to understand when having a look at the respective template in a few minutes. Also you might want to have a look at the [Vue documentation regarding slots](https://vuejs.org/v2/guide/components-slots.html).

### Rendering the block

You've set the `name` of the component to be used when rendering your block to be 'sw-cms-block-my-image-text-reversed'. This component does not exist yet, so let's create this one real quick. As already mentioned, creating a component is not explained by this guide in detail, so you might want to head over to our guide about [Creating a component](../../administration/add-custom-component) first.

First of all, create a new directory `component` in your block's directory. In there, create a new `index.js` file and register your custom component `sw-cms-block-my-image-text-reversed`.

**Keep in mind: The component name consists of `sw-cms-block-` and the `name` property mentioned in your `index.js`, while registering your cms block component via `registerCmsBlock()`!**

```javascript
// <plugin root>/src/Resources/app/administration/src/module/sw-cms/blocks/text-image/my-image-text-reversed/component/index.js
import template from './sw-cms-block-my-image-text-reversed.html.twig';
import './sw-cms-block-my-image-text-reversed.scss';

Shopware.Component.register('sw-cms-block-my-image-text-reversed', {
    template
});
```

Just like most components, it has a custom template and also some styles. Focus on the template first, create a new file `sw-cms-block-my-image-text-reversed.html.twig`.

This template now has to define the basic structure of your custom block. In this simple case, you only need a parent container and two sub-elements, whatever those are. That's also were the slots come into play: You've used two slots in your block's configuration, `left` and `right`. Make sure to create those slots in the template as well now.

```twig
// <plugin root>/src/Resources/app/administration/src/module/sw-cms/blocks/text-image/my-image-text-reversed/component/sw-cms-block-my-image-text-reversed.html.twig
{% block sw_cms_block_my_image_text_reversed %}
    <div class="sw-cms-block-my-image-text-reversed">
        <slot name="left">{% block sw_cms_block_my_image_text_reversed_slot_left %}{% endblock %}</slot>
        <slot name="right">{% block sw_cms_block_my_image_text_reversed_slot_right %}{% endblock %}</slot>
    </div>
{% endblock %}
```

You've got a parent `div` containing the two required [slots](https://vuejs.org/v2/guide/components-slots.html). If you were to rename the first slot `left` to something else, you'd have to adjust this in your block's configuration as well.

Those slots would be rendered from top to bottom now, instead of from left to right. That's why your block comes with a custom `.scss` file, create it now by adding the file `sw-cms-block-my-image-text-reversed.scss` to your `component` directory.

In there, use a grid to display your elements next to each other. You've set a CSS class for your block, which is the same as its name.

```css
// <plugin root>/src/Resources/app/administration/src/module/sw-cms/blocks/text-image/my-image-text-reversed/component/sw-cms-block-my-image-text-reversed.scss
.sw-cms-block-my-image-text-reversed {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    grid-gap: 40px;
}
```

That's it for this component! Make sure to import your `component` directory in your `index.js` file, so your new component actually gets loaded.

```javascript
// <plugin root>/src/Resources/app/administration/src/module/sw-cms/blocks/text-image/my-image-text-reversed/index.js
import './component'; // <- Right here!

Shopware.Service('cmsService').registerCmsBlock({
    ...
});
```

Your block can now be rendered in the designer. Let's continue with the preview component.

### Block preview

You've also set a property `previewComponent` containing the value `sw-cms-preview-my-image-text-reversed`. Time to create this component as well. For this purpose, stick to the core structure again and create a new directory `preview`. In there, again, create an `index.js` file, register your component by its name and load a template and a `.scss` file.

```javascript
// <plugin root>/src/Resources/app/administration/src/module/sw-cms/blocks/text-image/my-image-text-reversed/preview/index.js
import template from './sw-cms-preview-my-image-text-reversed.html.twig';
import './sw-cms-preview-my-image-text-reversed.scss';

Shopware.Component.register('sw-cms-preview-my-image-text-reversed', {
    template
});
```

The preview element doesn't have to deal with mobile viewports or anything alike, it's just a simplified preview of your block. Thus, create a template containing a text and an image and use the styles to place them next to each other. Create a `sw-cms-preview-my-image-text-reversed.html.twig` file in your `preview` directory with the following content.

```twig
// <plugin root>/src/Resources/app/administration/src/module/sw-cms/blocks/text-image/my-image-text-reversed/preview/sw-cms-preview-my-image-text-reversed.html.twig
{% block sw_cms_block_my_image_text_reversed_preview %}
    <div class="sw-cms-preview-my-image-text-reversed">
        <div>
            <h2>Lorem ipsum dolor</h2>
            <p>Lorem ipsum dolor sit amet, consetetur sadipscing elitr.</p>
        </div>
        <img :src="assetFilter('/administration/static/img/cms/preview_mountain_small.jpg')">
    </div>
{% endblock %}
```

Also, you need to create a

… **Truncated.** Full document: https://developer.shopware.com/docs/v6.6/guides/plugins/plugins/content/cms/add-cms-block.md


---

## Add CMS Element via Admin Extension SDK
**Source:** [guides/plugins/plugins/content/cms/add-cms-element-via-admin-sdk.md](https://developer.shopware.com/docs/v6.4/guides/plugins/plugins/content/cms/add-cms-element-via-admin-sdk.md)  
*(Body truncated in this bundle; follow the link for the rest.)*

# Add CMS Element via Admin Extension SDK

## Overview

This article will teach you how to create a new CMS element via the Admin Extension SDK. The plugin in this example will be named `SwagBasicAppCmsElementExample`, similar to the other guides.

## Prerequisites

* Knowledge on the creation of [Plugins](/docs/guides/plugins/plugins/plugin-base-guide) or [Apps](/docs/guides/plugins/apps/app-base-guide)
* Knowledge on the [creation of custom admin components](/docs/guides/plugins/plugins/administration/add-custom-component#creating-a-custom-component)
* Understanding the [Admin Extension SDK](https://shopware.github.io/admin-extension-sdk/docs/guide/getting-started/installation)

::: info
This example uses TypeScript, which is recommended, but not required for developing Shopware.
:::

## Creating your custom element

Similar to [Creating a new custom element via plugin](/docs/guides/plugins/plugins/content/cms/add-cms-element#creating-your-custom-element), this article describes creating a new custom element via app.
Creating a new element requires Admin Extension SDK.

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

```js
import 'regenerator-runtime/runtime';
import { location } from '@shopware-ag/admin-extension-sdk';

// Only execute extensionSDK commands when
// it is inside a iFrame (only needed for plugins)
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

This is the main file, which is executed first and functions as the entry point.

Start with `if(location.isIframe())` to make sure only content used inside iFrames is loaded. While the SDK is used in apps and plugins, this check ensures the code is executed in the right place.

Next you need `if(location.is(location.MAIN_HIDDEN))` to **load the main commands**, which are defined in the `mainCommands.ts` file. This will only be used to load logic, but not templates into the Administration.

Lastly, the `else` case will be responsible for specific loading of views via `viewRenderer.ts`. This is where the view templates will be loaded.

### Loading all required templates

Now, create the `viewRenderer.ts` file, which includes the three mandatory files needed for a CMS element as below:

* `swag-dailymotion-config.ts`, which will handle the content of the CMS element configuration
* `swag-dailymotion-element.ts`, which represents the actual target element in the CMS
* `swag-dailymotion-preview.ts`, which is responsible for the preview, when selecting the CMS element in its selection screen

Observe that every file is named according to the component and prefixed with `swag-dailymotion`, (vendor prefix) to ensure no other developer accidentally chooses the same name.

Let us see how the component loading via `viewRenderer.ts` looks like:

```js
import Vue from 'vue';
import { location } from '@shopware-ag/admin-extension-sdk';

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

What's especially interesting here is the use of the `location` object. This is a main concept of the Admin Extension SDK, where Shopware provides dedicated `locationIds` to offer you places to inject your templates into. For further information on that, it is recommend to have a look at the documentation of the [Admin Extension SDK](https://shopware.github.io/admin-extension-sdk/docs/guide/concepts/locations) to learn more about its concepts.

In your case, we will get your own **auto-generated** `locationIds`, depending on the name of your CMS element and suffixes, such as `-element`, `-config`, and `-preview`.

Those will be available after **registering the component**, which we will do in the following chapter.

## Registering a new element

For this topic we head to `mainCommands.ts`, since the registration of CMS elements is something to be done in a global scope.

```js
import { cms } from '@shopware-ag/admin-extension-sdk';

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

At first, you import the Admin Extension SDK's cms object, used for `cms.registerCmsElement` to register a new element.

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

```js
import Vue from 'vue'
import { data } from "@shopware-ag/admin-extension-sdk";
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

* Import `data` from the Admin Extension SDK, which is required for data handling between this app and Shopware
* The `element` variable contains the typical CMS element object and is also used to manage the element configuration you want to edit
* The `publishingKey` is used to tell the Admin Extension SDK in Shopware what piece of information you want to fetch. In this case, you need the `element` data

So, now you need a simple input field to get a `dailyUrl` for the Dailymotion video to be displayed. For that, first fetch the element via `data.get()` as seen in `createdComponent` and then link it to the computed property `dailyUrl` with getters and setters to mutate it. Using `data.update({ id, data })` you provide the publishing key `id` as a target and `data` for the data you want to save in Shopware.

With these small additions to typical CMS element behavior, you have already done with the config modal.

![Dailymotion config modal](../../../../../.gitbook/assets/add-cms-element-via-admin-sdk-config.png)

### The element file

Now let's have a look at the result of `swag-dailymotion-element.ts`:

```js
import Vue from 'vue'
import { data } from "@shopware-ag/admin-extension-sdk";
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

It initally fetches the `element` data, as you've already seen it in the config file. After that, using `data.subscribe(id, method)` it subscribes to the publishing key, which will update the element data automatically if something changes. It doesn't matter if the changes originate from our config modal outside Shopware or from somewhere else inside Shopware.

![Dailymotion CMS element](../../../../../.gitbook/assets/add-cms-element-via-admin-sdk-element.png)

### The preview f

… **Truncated.** Full document: https://developer.shopware.com/docs/v6.4/guides/plugins/plugins/content/cms/add-cms-element-via-admin-sdk.md


---

## Add CMS Element
**Source:** [guides/plugins/plugins/content/cms/add-cms-element.md](https://developer.shopware.com/docs/v6.6/guides/plugins/plugins/content/cms/add-cms-element.md)  
*(Body truncated in this bundle; follow the link for the rest.)*

# Add CMS Element

## Overview

This article will teach you how to create a new CMS element via plugin.
The plugin in this example will be named `SwagBasicExample`, similar to the other guides.

## Prerequisites

You won't learn how to create a plugin in this guide, head over to our Plugin base guide to create your first plugin.

This guide will also not explain how a custom component can be created in general, so head over to the official guide about creating a custom component to learn this first.

## Creating your custom element

Imagine you want to create a new element to display a Dailymotion video.
The shop managers can configure the link of the video to be shown. That's exactly what you're going to build in this guide.

Creating a new element requires you to extend the Administration.

### Injecting into the Administration

The main entry point to customize the Administration via plugin is the `main.js` file.
It has to be placed into a `<plugin root>/src/Resources/app/administration/src` directory in order to be automatically found by the Shopware platform.

## Registering a new element

Your plugin's structure should always match the core's structure.
When thinking about creating a new element, it's a recommendation to recreate the file tree like in the core for your plugin.
Thus, recreate this structure in your plugin: `<plugin root>/src/Resources/app/administration/src/module/sw-cms/elements`

In there, you create a directory for each new element you want to create. In this example a directory `dailymotion` is created.

Now create a new file `index.js` inside the `dailymotion` directory, since it will be loaded when importing this element in your `main.js`.
Speaking of that, right after having created the `index.js` file, you can actually import your new element's directory in the `main.js` file already:

```javascript
// <plugin root>/src/Resources/app/administration/src/main.js
import './module/sw-cms/elements/dailymotion';
```

Now open up your empty `dailymotion/index.js` file.
In order to register a new element to the system, you have to call the method `registerCmsElement` of the [cmsService](https://github.com/shopware/shopware/blob/v6.3.4.1/src/Administration/Resources/app/administration/src/module/sw-cms/service/cms.service.js).
Since it's available in the Dependency Injection Container, you can fetch it from there.

First of all, access our `Application` wrapper, which will grant you access to the DI container.
So go ahead and fetch the `cmsService` from it and call the mentioned `registerCmsElement` method.

```javascript
// <plugin root>/src/Resources/app/administration/src/module/sw-cms/elements/dailymotion/index.js
Shopware.Service('cmsService').registerCmsElement();
```

The method `registerCmsElement` takes a configuration object, containing the following necessary data:

| Key                  | Description                                                                                                                                                     |
|:---------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------|
| name                 | The technical name of your element. Will be used for the template loading later on.                                                                             |
| label                | A name to be shown for your element in the User Interface. Preferably as a snippet key.                                                                         |
| component            | The Vue component to be used when rendering your actual element in the Administration.                                                                          |
| configComponent      | The Vue component defining the "configuration detail" page of your element.                                                                                     |
| previewComponent     | The Vue component to be used in the "list of available elements". Just shows a tiny preview of what your element would look like if it was used.                |
| defaultConfig        | A default configuration to be applied to this element. Must be an object containing properties matching the used variable names, containing the default values. |
| hidden (optional)    | Hides the element in the replace element modal.                                                                                                                 |
| removable (optional) | Removes the replace element icon.                                                                                                                               |

Go ahead and create this configuration object yourself.
Here's what it should look like after having set all of those options:

```javascript
// <plugin root>/src/Resources/app/administration/src/module/sw-cms/elements/dailymotion/index.js
Shopware.Service('cmsService').registerCmsElement({
    name: 'dailymotion',
    label: 'sw-cms.elements.customDailymotionElement.label',
    component: 'sw-cms-el-dailymotion',
    configComponent: 'sw-cms-el-config-dailymotion',
    previewComponent: 'sw-cms-el-preview-dailymotion',
    defaultConfig: {
        dailyUrl: {
            source: 'static',
            value: ''
        }
    }
});
```

The property name does not require further explanation.
However, you need to create a snippet file in your plugin directory for the label property.

To do this, create a folder with the name snippet in your `sw-cms` folder.
After that, create the files for the languages, e.g. `de-DE.json` and `en-GB.json`.
The content of your snippet file should look something like this:

```json
{
  "sw-cms": {
    "elements": {
      "customDailymotionElement": {
        "label": "Dailymotion video"
      }
    }
  }
}
```

To learn more about adding own snippets, please refer to [Add snippets to Administration](../../administration/adding-snippets) for more information.

For all three fields `component`, `configComponent` and `previewComponent`, components that do not *yet* exist were applied.
Those will be created in the next few steps as well. The `defaultConfig` defines the default values for the element's configuration.
There will be a text field to enter a Dailymotion video ID called `dailyUrl`.

Now you have to create the three missing components, let's start with the preview component.

## Building the preview

Create a new directory preview in your element's directory dailymotion. In there, create a new file `index.js`, just like for all components.
Then register your component, using the `Shopware.Component` wrapper:

```javascript
// <plugin root>/src/Resources/app/administration/src/module/sw-cms/elements/dailymotion/preview/index.js
import template from './sw-cms-el-preview-dailymotion.html.twig';
import './sw-cms-el-preview-dailymotion.scss';

Shopware.Component.register('sw-cms-el-preview-dailymotion', {
    template
});
```

Just like most components, it has a custom template and some styles.
Focus on the template first, create a new file `sw-cms-el-preview-dailymotion.html.twig`.

So, for instance, if you want to show the default 'mountain' preview image as an example, then copy it from `<Shopware root>/public/bundles/administration/static/img/cms/preview_mountain_small.jpg` to your static folder.
You can also replace it with something of your own. Additionally, you can place icons `multicolor-action-play`.
Head over to [icon library](https://component-library.shopware.com/icons/) to access them.

That means: You'll need a container to contain both the image and the icon.
In there, you create an `img` tag and use the [sw-icon component](https://github.com/shopware/shopware/blob/v6.3.4.1/src/Administration/Resources/app/administration/src/app/component/base/sw-icon/index.js) to display the icon.

```twig
// <plugin root>/src/Resources/app/administration/src/module/sw-cms/elements/dailymotion/preview/sw-cms-el-preview-dailymotion.html.twig
{% block sw_cms_element_dailymotion_preview %}
    <div class="sw-cms-el-preview-dailymotion">
        <img class="sw-cms-el-preview-dailymotion-img"
             :src="'customcmselement/static/img/background_dailymotion_preview.jpg' | asset">

        <sw-icon class="sw-cms-el-preview-dailymotion-icon"
                 name="multicolor-action-play"></sw-icon>
    </div>
{% endblock %}
```

The icon would now be displayed beneath the image, so let's add some styles for this by creating the file `sw-cms-el-preview-dailymotion.scss`.

The container needs to have a `position: relative;` style.
This is necessary, so the child can be positioned absolutely and will do so relative to the container's position.
Thus, the icon receives a `position: absolute;` style, plus some top and left values to center it.

```css
// <plugin root>/src/Resources/app/administration/src/module/sw-cms/elements/dailymotion/preview/sw-cms-el-preview-dailymotion.scss
.sw-cms-el-preview-dailymotion {
    position: relative;

    .sw-cms-el-preview-dailymotion-img {
        display: block;
        max-width: 100%;
    }

    .sw-cms-el-preview-dailymotion-icon {
        $icon-height: 50px;
        $icon-width: $icon-height;
        position: absolute;
        height: $icon-height;
        width: $icon-width;

        left: calc(50% - #{$icon-width/2});
        top: calc(50% - #{$icon-height/2});
    }
}
```

The centered positioning will be done by translating the elements by 50% via `top` and `left` properties.
Since that would be 50% from the upper left corner of the icon, this wouldn't really center the icon yet.
Subtract the half of the icon's width and height and then you're fine.

One last thing: Import your preview component in your element's `index.js` file, so it's loaded.

## Rendering the component

The next would be the main component `sw-cms-el-dailymotion`, the one to be rendered when the shop managers actually decided to use your element by clicking on the preview.
Now, you want to show the actually configured video here now.
Start with the basic again, create a new directory `component`, in there a new file `index.js` and then register your component `sw-cms-el-dailymotion`.

```javascript
// <plugin root>/src/Resources/app/administration/src/module/sw-cms/elements/dailymotion/component/index.js
import template from './sw-cms-el-dailymotion.html.twig';
import './sw-cms-el-dailymotion.scss';

Shopware.Component.register('sw-cms-el-dailymotion', {
    template
});
```

In addition, create the template file `sw-cms-el-dailymotion.html.twig` and the `.scss` file `sw-cms-el-dailymotion.scss`.

The template doesn't have to include a lot.
Having a look at how Dailymotion video embedding works, you just have to add an `iframe` with a src attribute pointing to the video.

```twig
// <plugin root>/src/Resources/app/administration/src/module/sw-cms/elements/dailymotion/component/sw-cms-el-dailymotion.html.twig
{% block sw_cms_element_dailymotion %}
    <div class="sw-cms-el-dailymotion">
        <div class="sw-cms-el-dailymotion-iframe-wrapper">
            <iframe frameborder="0"
                    type="text/html"
                    width="100%"
                    height="100%"
                    :src="dailyUrl">
            </iframe>
        </div>
    </div>
{% endblock %}
```

You can't just use a static `src` here, since the shop managers want to configure the video they want to show.
Thus, we're fetching that link via Vue.js now.

Let's add the code to provide the src for the iframe. For this case you're going to use a [computed property](https://vuejs.org/v2/guide/computed.html).

```javascript
// <plugin root>/src/Resources/app/administration/src/module/sw-cms/elements/dailymotion/component/index.js
import template from './sw-cms-el-dailymotion.html.twig';
import './sw-cms-el-dailymotion.scss';

Shopware.Component.register('sw-cms-el-dailymotion', {
    template,

    computed: {
        da

… **Truncated.** Full document: https://developer.shopware.com/docs/v6.6/guides/plugins/plugins/content/cms/add-cms-element.md


---

## Add Data to CMS Element
**Source:** [guides/plugins/plugins/content/cms/add-data-to-cms-elements.md](https://developer.shopware.com/docs/v6.6/guides/plugins/plugins/content/cms/add-data-to-cms-elements.md)  
# Add Data to CMS Element

## Overview

When creating custom CMS elements, you sometimes want to use more complex data types than text or boolean values, e.g. other entities such as media or products. In those cases you can implement a custom `CmsElementResolver` to resolve the configuration data.

## Prerequisites

This guide will not explain how to create custom CMS elements in general, so head over to the official guide about [Adding a custom CMS element](add-cms-element) to learn this first.

## Create a data resolver

To manipulate the data of these elements during the loading of the configuration, we create a `DailyMotionCmsElementResolver` resolver in our plugin.

```php
// <plugin root>/src/DataResolver/DailyMotionCmsElementResolver.php
<?php declare(strict_types=1);

namespace Swag\BasicExample\DataResolver;

use Shopware\Core\Content\Cms\Aggregate\CmsSlot\CmsSlotEntity;
use Shopware\Core\Content\Cms\DataResolver\Element\AbstractCmsElementResolver;
use Shopware\Core\Content\Cms\DataResolver\Element\ElementDataCollection;
use Shopware\Core\Content\Cms\DataResolver\ResolverContext\ResolverContext;
use Shopware\Core\Content\Cms\DataResolver\CriteriaCollection;

class DailyMotionCmsElementResolver extends AbstractCmsElementResolver
{
    public function getType(): string
    {
        return 'dailymotion';
    }

    public function collect(CmsSlotEntity $slot, ResolverContext $resolverContext): ?CriteriaCollection
    {
        return null;
    }

    public function enrich(CmsSlotEntity $slot, ResolverContext $resolverContext, ElementDataCollection $result): void
    {

    }
}
```

Our custom resolver extends from the `AbstractCmsElementResolver` which forces us to implement the methods `getType`, `collect` and `enrich`.

In the previous [example](add-cms-element) we added a cms element with the name `dailymotion`. As you can see the `getType` method of our custom resolver reflects that name by returning the `dailymotion` string. This resolver is called every time for an element of the type `dailymotion`.

To register our custom resolver to the service container we have to register it in the `services.xml` file in our plugin.

```xml
// <plugin root>/src/Resources/config/services.xml
<?xml version="1.0" ?>

<container xmlns="http://symfony.com/schema/dic/services"
           xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
           xsi:schemaLocation="http://symfony.com/schema/dic/services http://symfony.com/schema/dic/services/services-1.0.xsd">

    <services>
        <service id="Swag\BasicExample\DataResolver\DailyMotionCmsElementResolver">
            <tag name="shopware.cms.data_resolver" />
        </service>
    </services>
</container>
```

### Collect data

The `collect` method prepares the criteria object. This is useful if, for example, you have a media entity `ID` stored in your configuration. As in the following example, you can retrieve the configuration for the current cms element with the call `$slot->getFieldConfig()` and then have access to the individual fields. In this case we read out `myCustomMedia` field which may contain a mediaId. If a `mediaId` exists, we create a new `CriteriaCollection` for it. Now we are able to use this media-object later on.

```php
// <plugin root>/src/DataResolver/DailyMotionCmsElementResolver.php
<?php declare(strict_types=1);

// ...
use Shopware\Core\Content\Media\MediaDefinition;
use Shopware\Core\Content\Media\MediaEntity;
// ...

    public function collect(CmsSlotEntity $slot, ResolverContext $resolverContext): ?CriteriaCollection
    {
        $config = $slot->getFieldConfig();
        $myCustomMedia = $config->get('myCustomMedia');

        if (!$myCustomMedia) {
            return null;
        }

        $mediaId = $myCustomMedia->getValue();

        $criteria = new Criteria([$mediaId]);

        $criteriaCollection = new CriteriaCollection();
        $criteriaCollection->add('media_' . $slot->getUniqueIdentifier(), MediaDefinition::class, $criteria);

        return $criteriaCollection;
    }

// ...
```

### Enrich data

Inside the `enrich` you can perform additional logic on the data that has been resolved. Like in the `collect` method, we have access to our configuration fields and their values. Imagine you have stored some information in the element configuration and want to perform an external `Api` call to fetch some additional data. After that you can add the response information to the current slot data by calling `$slot->setData()`.

This could be a possible solution for that:

```php
// <plugin root>/src/DataResolver/DailyMotionCmsElementResolver.php
<?php declare(strict_types=1);
// ...

    public function enrich(CmsSlotEntity $slot, ResolverContext $resolverContext, ElementDataCollection $result): void
    {
        $config = $slot->getFieldConfig();
        $myCustomApiPayload = $config->get('myCustomApiPayload');

        // perform some external api call with the payload `myCustomApiPayload`
        $myCustomAPI = new MyCustomAPI();

        $response = $myCustomAPI->query($myCustomApiPayload);

        if ($response) {
            $slot->setData($response);
        }
    }

// ...
```

---

---

## Mail
**Source:** [guides/plugins/plugins/content/mail.md](https://developer.shopware.com/docs/v6.6/guides/plugins/plugins/content/mail.md)  
# Mail

Shopware Mail offers the ability to add mail data and configure mail templates for various email communications within the e-commerce platform.	 You can add relevant mail data such as transactional emails, order notifications, customer communication, marketing campaigns, or newsletters. These emails can be tailored to specific events or triggers, ensuring timely and personalized communication with customers.

The plugin provides the functionality to create and customize these mail templates. Users can design and format the content of their emails, including text, images, logos, and dynamic variables, to personalize the messages. This allows for consistent branding and a professional appearance across all outgoing emails.

By utilizing this plugin, businesses can effectively engage with their customers and keep them informed about order updates, promotions, or other relevant information.

---

---

## Add Data to Mails
**Source:** [guides/plugins/plugins/content/mail/add-data-to-mails.md](https://developer.shopware.com/docs/v6.6/guides/plugins/plugins/content/mail/add-data-to-mails.md)  
# Add Data to Mails

## Overview

The mail templates in Shopware have access to a given set of data, e.g. the customer data, the order data, etc. Sometimes you want add your custom entity to that data set though, so you can use this data in your mail templates as well.

This guide will teach you how to add new data to the mail templates using your plugin.

## Prerequisites

This guide is built upon our [plugin base guide](../../plugin-base-guide), whose namespace is going to be used in the examples of this guide. However, you can use those examples with any plugin, you'll just have to adjust the namespace and the directory the files are located in.

Furthermore, you should know how to [decorate a service](../../plugin-fundamentals/adjusting-service).

## Adding data via decorator

In order to add new data to the mail templates, you'll have to decorate the [MailService](https://github.com/shopware/shopware/blob/trunk/src/Core/Content/Mail/Service/MailService.php).

To be precise, you have to extend the `send` method, whose last parameter is the `$templateData`, that we want to enrich.

So let's do that, here's an example of a decorated mail service:

```php
// <plugin root>/src/Service/AddDataToMails.php
<?php declare(strict_types=1);

namespace Swag\BasicExample\Service;

use Shopware\Core\Content\Mail\Service\AbstractMailService;
use Shopware\Core\Framework\Context;
use Symfony\Component\Mime\Email;

class AddDataToMails extends AbstractMailService
{
    /**
     * @var AbstractMailService
     */
    private AbstractMailService $mailService;

    public function __construct(AbstractMailService $mailService)
    {
        $this->mailService = $mailService;
    }

    public function getDecorated(): AbstractMailService
    {
        return $this->mailService;
    }

    public function send(array $data, Context $context, array $templateData = []): ?Email
    {
        $templateData['myCustomData'] = 'Example data';

        return $this->mailService->send($data, $context, $templateData);
    }
}
```

If you don't recognise the decoration pattern used here, make sure to have a look at our guide about [decorations](../../plugin-fundamentals/adjusting-service).

As always, we're passing in the original `MailService` as a constructor parameter, so we can return it in the `getDecorated` method, as well as use the original `send` method after having adjusted the `$templateData`.

In this example, we're adding `myCustomData` to the `$templateData`, so that one should be available then.

If we add `{{ myCustomData }}` to any mail template, it should then print "Example data". You can use any kind of data here, e.g. an array of data.

### Register your decorator

Of course you still have to register the decoration to the service container. Beware of the `decorates` attribute of our service.

Here's the respective example `services.xml`:

```xml
// <plugin root>/src/Resources/config/services.xml
<?xml version="1.0" ?>
<container xmlns="http://symfony.com/schema/dic/services"
           xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
           xsi:schemaLocation="http://symfony.com/schema/dic/services http://symfony.com/schema/dic/services/services-1.0.xsd">

    <services>
        <service id="Swag\BasicExample\Service\AddDataToMails" decorates="Shopware\Core\Content\Mail\Service\MailService">
            <argument type="service" id="Swag\BasicExample\Service\AddDataToMails.inner" />
        </service>
    </services>
</container>
```

---

---

## Add Mail Templates
**Source:** [guides/plugins/plugins/content/mail/add-mail-template.md](https://developer.shopware.com/docs/v6.6/guides/plugins/plugins/content/mail/add-mail-template.md)  
*(Body truncated in this bundle; follow the link for the rest.)*

# Add Mail Templates

## Overview

You can add new mail templates to Shopware by using the Administration. However, you might want to ship a mail template with your plugin, so using the Administration is no option.

This guide will cover how to add a custom mail template with your plugin.

## Prerequisites

The namespaces used in the examples of this guide are the same as the namespace from our [Plugin base guide](../../plugin-base-guide), so you might want to have a look at it first.

Furthermore, this guide will use [Database migrations](../../plugin-fundamentals/database-migrations) in order to add a custom mail template, which is not explained in depth here. Make sure to understand those first!

## Adding a mail template via migration

As already mentioned, adding a mail template is done by using a plugin database migration. To be precise, those are the steps necessary:

* Create a new mail template type or fetch an existing mail template type ID
* Add an entry to `mail_template` using the said template type ID
* Add an entry to `mail_template_translation` for each language you want to support

The following example will create a new template of type "contact form", which is already available. There will be an example to create a custom mail template type though.

Let's have a look at an example, which will:

* Use the "contact form" type
* Add a mail template entry
* Add a mail template translation for en\_GB and de\_DE

```php
// <plugin root>/src/Migration/Migration1616418675AddMailTemplate.php
<?php declare(strict_types=1);

namespace Swag\BasicExample\Migration;

use DateTime;
use Doctrine\DBAL\Connection;
use Shopware\Core\Framework\Migration\MigrationStep;
use Shopware\Core\Defaults;
use Shopware\Core\Framework\Uuid\Uuid;

class Migration1616418675AddMailTemplate extends MigrationStep
{
    public function getCreationTimestamp(): int
    {
        return 1616418675;
    }

    public function update(Connection $connection): void
    {
        $mailTemplateTypeId = $this->getMailTemplateTypeId($connection);

        $this->createMailTemplate($connection, $mailTemplateTypeId);
    }

    public function updateDestructive(Connection $connection): void
    {
    }

    private function getMailTemplateTypeId(Connection $connection): string
    {
        $sql = <<<SQL
            SELECT id
            FROM mail_template_type
            WHERE technical_name = "contact_form"
        SQL;

        return Uuid::fromBytesToHex($connection->fetchOne($sql));
    }

    private function getLanguageIdByLocale(Connection $connection, string $locale): ?string
    {
        $sql = <<<SQL
        SELECT `language`.`id`
        FROM `language`
        INNER JOIN `locale` ON `locale`.`id` = `language`.`locale_id`
        WHERE `locale`.`code` = :code
        SQL;

        $languageId = $connection->executeQuery($sql, ['code' => $locale])->fetchOne();

        if (empty($languageId)) {
            return null;
        }

        return $languageId;
    }

    private function createMailTemplate(Connection $connection, string $mailTemplateTypeId): void
    {
        $mailTemplateId = Uuid::randomHex();

        $enGbLangId = $this->getLanguageIdByLocale($connection, 'en-GB');
        $deDeLangId = $this->getLanguageIdByLocale($connection, 'de-DE');

        $connection->executeStatement("
        INSERT IGNORE INTO `mail_template`
            (id, mail_template_type_id, system_default, created_at)
        VALUES
            (:id, :mailTemplateTypeId, :systemDefault, :createdAt)
        ",[
            'id' => Uuid::fromHexToBytes($mailTemplateId),
            'mailTemplateTypeId' => Uuid::fromHexToBytes($mailTemplateTypeId),
            'systemDefault' => 0,
            'createdAt' => (new DateTime())->format(Defaults::STORAGE_DATE_TIME_FORMAT),
        ]);

        if (!empty($enGbLangId)) {
            $connection->executeStatement("
            INSERT IGNORE INTO `mail_template_translation`
                (mail_template_id, language_id, sender_name, subject, description, content_html, content_plain, created_at)
            VALUES
                (:mailTemplateId, :languageId, :senderName, :subject, :description, :contentHtml, :contentPlain, :createdAt)
            ",[
                'mailTemplateId' => Uuid::fromHexToBytes($mailTemplateId),
                'languageId' => $enGbLangId,
                'senderName' => '{{ salesChannel.name }}',
                'subject' => 'Example mail template subject',
                'description' => 'Example mail template description',
                'contentHtml' => $this->getContentHtmlEn(),
                'contentPlain' => $this->getContentPlainEn(),
                'createdAt' => (new DateTime())->format(Defaults::STORAGE_DATE_TIME_FORMAT),
            ]);
        }

        if (!empty($deDeLangId)) {            
            $connection->executeStatement("
            INSERT IGNORE INTO `mail_template_translation`
                (mail_template_id, language_id, sender_name, subject, description, content_html, content_plain, created_at)
            VALUES
                (:mailTemplateId, :languageId, :senderName, :subject, :description, :contentHtml, :contentPlain, :createdAt)
            ",[
                'mailTemplateId' => Uuid::fromHexToBytes($mailTemplateId),
                'languageId' => $deDeLangId,
                'senderName' => '{{ salesChannel.name }}',
                'subject' => 'Beispiel E-Mail Template Titel',
                'description' => 'Beispiel E-Mail Template Beschreibung',
                'contentHtml' => $this->getContentHtmlDe(),
                'contentPlain' => $this->getContentPlainDe(),
                'createdAt' => (new DateTime())->format(Defaults::STORAGE_DATE_TIME_FORMAT),
            ]);
        }

    }

    private function getContentHtmlEn(): string
    {
        return <<<MAIL
        <div style="font-family:arial; font-size:12px;">
            <p>
                Example HTML content!
            </p>
        </div>
        MAIL;
    }

    private function getContentPlainEn(): string
    {
        return <<<MAIL
        Example plain content!
        MAIL;
    }

    private function getContentHtmlDe(): string
    {
        return <<<MAIL
        <div style="font-family:arial; font-size:12px;">
            <p>
                Beispiel HTML Inhalt!
            </p>
        </div>
        MAIL;
    }

    private function getContentPlainDe(): string
    {
        return <<<MAIL
        Beispiel Plain Inhalt!
        MAIL;
    }
}
```

First of all, let's have a look at the small `update` method. It's mainly just fetching the mail template type ID using a short SQL statement and afterwards it executes the method `createMailTemplate`, which will cover all the other steps.

Now on to the `createMailTemplate` method, which looks big, but isn't that scary. First of all, we're fetching the language IDs for both `en-GB` and `de-DE`.

We then create the entry for the `mail_template` table. Make sure to set `system_default` to 0 here!

Afterwards we're inserting the entries into the `mail_template_translation` table. For compatibility reasons we have to check whether the languages exist in the database so we can insert our translations for these languages. The same principle applies to other ISO languages.

The variables for the English and the German subject and description, may be changed to fit your needs.

Each of those calls uses a little helper method `getContentHtml` or `getContentPlain` respectively, where you can use your template.

And that's it, once your plugin is installed, the mail template will be added to Shopware.

::: warning
Do not remove e-mail templates in your plugin, e.g. when it is uninstalled. This may lead to data inconsistency, since those templates can be associated to other entities. Beware to use `IGNORE` before `INTO` Statements so no exception will be thrown upon uninstallation and reinstallation of your plugin.
:::

### Creating a custom mail type

In order to not only use an existing mail template type, but to create a custom one, you have to adjust the `update` method and create a new method.

Let's have a look:

```php
// <plugin root>/src/Migration/Migration1616418675AddMailTemplate.php
<?php declare(strict_types=1);

namespace Swag\BasicExample\Migration;

use DateTime;
use Doctrine\DBAL\Connection;
use Shopware\Core\Framework\Migration\MigrationStep;
use Shopware\Core\Defaults;
use Shopware\Core\Framework\Uuid\Uuid;

class Migration1616418675AddMailTemplate extends MigrationStep
{
    public function getCreationTimestamp(): int
    {
        return 1616418675;
    }

    public function update(Connection $connection): void
    {
        $mailTemplateTypeId = $this->createMailTemplateType($connection);

        $this->createMailTemplate($connection, $mailTemplateTypeId);
    }

    private function createMailTemplateType(Connection $connection): string
    {
        $mailTemplateTypeId = Uuid::randomHex();

        $enGbLangId = $this->getLanguageIdByLocale($connection, 'en-GB');
        $deDeLangId = $this->getLanguageIdByLocale($connection, 'de-DE');

        $englishName = 'Example mail template type name';
        $germanName = 'Beispiel E-Mail Template Name';

        $connection->executeStatement("
            INSERT IGNORE INTO `mail_template_type`
                (id, technical_name, available_entities, created_at)
            VALUES
                (:id, :technicalName, :availableEntities, :createdAt)
        ",[
            'id' => Uuid::fromHexToBytes($mailTemplateTypeId),
            'technicalName' => 'custom_mail_template_type',
            'availableEntities' => json_encode(['product' => 'product']),
            'createdAt' => (new DateTime())->format(Defaults::STORAGE_DATE_TIME_FORMAT),
        ]);

        if (!empty($enGbLangId)) {
            $connection->executeStatement("
            INSERT IGNORE INTO `mail_template_type_translation`
                (mail_template_type_id, language_id, name, created_at)
            VALUES
                (:mailTemplateTypeId, :languageId, :name, :createdAt)
            ",[
                'mailTemplateTypeId' => Uuid::fromHexToBytes($mailTemplateTypeId),
                'languageId' => $enGbLangId,
                'name' => $englishName,
                'createdAt' => (new DateTime())->format(Defaults::STORAGE_DATE_TIME_FORMAT),
            ]);
        }

        if (!empty($deDeLangId)) {
            $connection->executeStatement("
            INSERT IGNORE INTO `mail_template_type_translation`
                (mail_template_type_id, language_id, name, created_at)
            VALUES
                (:mailTemplateTypeId, :languageId, :name, :createdAt)
            ",[
                'mailTemplateTypeId' => Uuid::fromHexToBytes($mailTemplateTypeId),
                'languageId' => $deDeLangId,
                'name' => $germanName,
                'createdAt' => (new DateTime())->format(Defaults::STORAGE_DATE_TIME_FORMAT),
            ]);
        }

        return $mailTemplateTypeId;
    }

    // ...
}
```

First of all we changed the `getMailTemplateTypeId` method call to `createMailTemplateType`, a new method which we will create afterwards. Again, this method then has to return the ID of the newly created mail template ID.

So having a look at the `createMailTemplateType` method, you will see some similarities:

* First of all we're fetching the language IDs for `en-GB` and `de-DE`
* Then we define the translated names for the mail template type
* And then the respective `mail_template_type` entry, as well as the translated `mail_template_type_translation` entries are created

Note the `available_entities` column when creating the mail template type itself though. In here, you define which entities should be available for the respective mail template, in this example we'll just provide the `ProductEntity`.

## Next steps

Now that you know how to add custom mail templates, you might wonder how you ca

… **Truncated.** Full document: https://developer.shopware.com/docs/v6.6/guides/plugins/plugins/content/mail/add-mail-template.md


---

## Media
**Source:** [guides/plugins/plugins/content/media.md](https://developer.shopware.com/docs/v6.6/guides/plugins/plugins/content/media.md)  
# Media

Shopware Media offers the ability to add media file extensions and prevent the deletion of media files within the e-commerce platform.

With the Media plugin, users can specify and configure new media file extensions. This allows businesses to define different types of media files, such as images, videos, or documents, that can be uploaded and used within the Shopware platform.

Furthermore, the plugin helps prevent the deletion of media files that are not used in your application.

---

---

## Add Custom Media File Extension
**Source:** [guides/plugins/plugins/content/media/add-custom-file-extension.md](https://developer.shopware.com/docs/v6.6/guides/plugins/plugins/content/media/add-custom-file-extension.md)  
# Add Custom Media File Extension

## Overview

You might have come across the fact, that you cannot just upload any type of media to Shopware by using the Media
module in the Administration.
If that's the case for you, this guide will be the solution.
It will provide an explanation on how you can add new allowed file extensions to Shopware using a plugin.

## Prerequisites

As most of our plugin guides, this guide was also built upon our [Plugin base guide](../../plugin-base-guide).
Furthermore, you'll have to know about adding classes to the [Dependency injection](../../plugin-fundamentals/dependency-injection) container
and about using a subscriber in order to [Listen to events](../../plugin-fundamentals/listening-to-events).

## Adding a custom extension

In this section, we're going to take care of allowing a new extension to Shopware first, without letting Shopware know
exactly what kind of file this new extension represents (Images, videos, documents, ...).

For this to work, all you have to do is to register to the `MediaFileExtensionWhitelistEvent` event, which can be found
[here](https://github.com/shopware/shopware/blob/v6.4.0.0/src/Core/Content/Media/File/FileSaver.php#L397-L398).
This is of course done via a [subscriber](../../plugin-fundamentals/listening-to-events).

Have a look at the following code example:

```php
// <plugin root>/src/Service/Subscriber.php
<?php declare(strict_types=1);

namespace Swag\BasicExample\Service;

use Shopware\Core\Content\Media\Event\MediaFileExtensionWhitelistEvent;
use Symfony\Component\EventDispatcher\EventSubscriberInterface;

class Subscriber implements EventSubscriberInterface
{
    public static function getSubscribedEvents(): array
    {
        return [
            MediaFileExtensionWhitelistEvent::class => 'addEntryToFileExtensionWhitelist'
        ];
    }

    public function addEntryToFileExtensionWhitelist(MediaFileExtensionWhitelistEvent $event): void
    {
        $whiteList = $event->getWhitelist();
        $whiteList[] = 'img';

        $event->setWhitelist($whiteList);
    }
}
```

You can use the method `getWhitelist` of the `$event` variable to get the current whitelist, which is just a plain array of extensions.
Therefore you can add new array entries and then set the array back to the `$event` instance by using the respective setter method
`setWhitelist`.

And that's it already! Shopware will now allow uploading files with the extension `.img`.

## Recognising the new extension

There is another thing you most likely want to do here.
While you can add new extensions like mentioned above, Shopware does not automatically recognise which kind of extension it is dealing with.
Is it a new image extension and should be displayed as such? Is it a video file extension? Maybe a new kind of document?

In order to let Shopware know which kind of type we're dealing with, you can add a new `TypeDetector` class
to let Shopware know about your new extension.

In the following example we'll imagine that we've added a new **image** extension called `img`, like we did above, and we're going to let Shopware know
about it.

What we'll be doing now, is to add a custom `TypeDetector` class which returns an `ImageType` if the extension of the file to be checked matches our type detector.
Have a look at the following example:

```php
// <plugin root>/src/Core/Content/Media/TypeDetector/CustomImageTypeDetector.php
<?php declare(strict_types=1);

namespace Swag\BasicExample\Core\Content\Media\TypeDetector;

use Shopware\Core\Content\Media\File\MediaFile;
use Shopware\Core\Content\Media\MediaType\ImageType;
use Shopware\Core\Content\Media\MediaType\MediaType;
use Shopware\Core\Content\Media\TypeDetector\TypeDetectorInterface;

class CustomImageTypeDetector implements TypeDetectorInterface
{
    protected const SUPPORTED_FILE_EXTENSIONS = [
        'img' => [ImageType::TRANSPARENT],
    ];

    public function detect(MediaFile $mediaFile, ?MediaType $previouslyDetectedType): ?MediaType
    {
        $fileExtension = mb_strtolower($mediaFile->getFileExtension());
        if (!\array_key_exists($fileExtension, self::SUPPORTED_FILE_EXTENSIONS)) {
            return $previouslyDetectedType;
        }

        if ($previouslyDetectedType === null) {
            $previouslyDetectedType = new ImageType();
        }

        $previouslyDetectedType->addFlags(self::SUPPORTED_FILE_EXTENSIONS[$fileExtension]);

        return $previouslyDetectedType;
    }
}
```

```xml
// <plugin root>/src/Resources/config/services.xml
<?xml version="1.0" ?>
<container xmlns="http://symfony.com/schema/dic/services"
           xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
           xsi:schemaLocation="http://symfony.com/schema/dic/services http://symfony.com/schema/dic/services/services-1.0.xsd">

    <services>
        <service id="Swag\BasicExample\Core\Content\Media\TypeDetector\CustomImageTypeDetector">
            <tag name="shopware.media_type.detector" priority="10"/>
        </service>
    </services>
</container>
```

You will have to create a new class which implements from the interface `TypeDetectorInterface`.
This will come with the requirement of having a `detect` method, which will return the respective media type.

Inside of the `detect` method, we're first checking if the file extension matches our allowed extensions, in this case only
`img`.
If that's not the case, just return the `$previouslyDetectedType`, which most likely comes from the `DefaultTypeDetector` and which
tried to detect the type already by analysing the file's MIME-type.

If the extension does indeed match, we're for sure going to return `ImageType` here.
Make sure to add flags to your media type, e.g. the `transparent` flag, or if it's an animated image.

You can find all available flags in their respective media type classes,
e.g. [here](https://github.com/shopware/shopware/blob/v6.4.0.0/src/Core/Content/Media/MediaType/ImageType.php#L7-L10) for the image media type.

Make sure to register your new type detector to the [Dependency injection container](../../plugin-fundamentals/dependency-injection)
by using the tag `shopware.media_type.detector`.

Shopware will now recognise your new image extension and handle your new file like an image.

---

---

## Prevent Deletion of Media Files Referenced in your Plugins
**Source:** [guides/plugins/plugins/content/media/prevent-deletion-of-media-files-referenced-in-your-plugins.md](https://developer.shopware.com/docs/v6.6/guides/plugins/plugins/content/media/prevent-deletion-of-media-files-referenced-in-your-plugins.md)  
# Prevent Deletion of Media Files Referenced in your Plugins

::: info
The ability to prevent Media entities from being deleted is available since Shopware 6.5.1.0.
:::

## Overview

The Shopware CLI application provides a `media:delete-unused` command which deletes all media entities and their corresponding files which are not used in your application.
Not used means that it is not referenced by any other entity. This works well in the simple case that all your entity definitions store references to Media entities with correct foreign keys.

However, this does not cover all the possible cases, even for many internal Shopware features. For example the CMS entities store their configuration as JSON blobs with references to Media IDs stored in a nested data structure.

In order to fix the case of Media references that cannot be resolved without knowledge of the specific entity and its features, an extension point is provided via an event.

If you are developing an extension which references Media entities, and you cannot use foreign keys, this guide will detail how to prevent shopware deleting the Media entities your extension references.

## Prerequisites

As most of our plugin guides, this guide was also built upon our [Plugin base guide](../../plugin-base-guide).
Furthermore, you'll have to know about adding classes to the [Dependency injection](../../plugin-fundamentals/dependency-injection) container
and about using a subscriber in order to [Listen to events](../../plugin-fundamentals/listening-to-events).

## The deletion process

The `\Shopware\Core\Content\Media\UnusedMediaPurger` service first searches for Media entities that are not referenced by any other entities in the system via foreign keys. Then it dispatches an event containing the Media IDs it believes are unused.

The event is an instance of `\Shopware\Core\Content\Media\Event\UnusedMediaSearchEvent`. A subscriber can then cross-reference the Media IDs scheduled to be deleted and mark any of them as *used*.

The remaining Media IDs will then be deleted by the `\Shopware\Core\Content\Media\UnusedMediaPurger` service.

Please note that this process is completed in small batches to maintain stability, so the event may be dispatched multiple times when an installation has many unused Media entities.

## Adding a subscriber

In this section, we're going to register a subscriber for the `\Shopware\Core\Content\Media\Event\UnusedMediaSearchEvent` event.

Have a look at the following code example:

```php
// <plugin root>/src/Subscriber/UnusedMediaSubscriber.php
<?php declare(strict_types=1);

namespace Swag\BasicExample\Subscriber;

use Shopware\Core\Content\Media\Event\UnusedMediaSearchEvent;
use Symfony\Component\EventDispatcher\EventSubscriberInterface;

class UnusedMediaSubscriber implements EventSubscriberInterface
{
    public static function getSubscribedEvents(): array
    {
        return [
            UnusedMediaSearchEvent::class => 'removeUsedMedia',
        ];
    }

    public function removeUsedMedia(UnusedMediaSearchEvent $event): void
    {
        $idsToBeDeleted = $event->getUnusedIds();
    
        $doNotDeleteTheseIds = $this->getUsedMediaIds($idsToBeDeleted);
    
        $event->markAsUsed($doNotDeleteTheseIds);
    }
    
    private function getUsedMediaIds(array $idsToBeDeleted): array
    {
        // do something to get the IDs that are used
        return [];
    }
}
```

You can use the method `getUnusedIds` of the `$event` variable to get the current an array of Media IDs scheduled for removal.

You can use these IDs to query whatever storage your plugin uses to store references to Media entities, to check if they are currently used.

If any of the IDs are used by your plugin, you can use the method `markAsUsed` of the `$event` variable to prevent the Media entities from being deleted. `markAsUsed` accepts an array of string IDs.

If your storage is a relational database such as MySQL you should, when possible, use direct database queries to check for references. This saves memory and CPU cycles by not loading unnecessary data.

Imagine an extension which provides an image slider feature. An implementation of `getUsedMediaIds` might look something like the following:

```php
// <plugin root>/src/Subscriber/UnusedMediaSubscriber.php
private function getUsedMediaIds(array $idsToBeDeleted): array
{
    $sql = <<<SQL
    SELECT JSON_EXTRACT(slider_config, "$.images") as mediaIds FROM my_slider_table
    WHERE JSON_OVERLAPS(
        JSON_EXTRACT(slider_config, "$.images"),
        JSON_ARRAY(?)
    );
    SQL;

    $usedMediaIds = $this->connection->fetchFirstColumn(
        $sql,
        [$event->getUnusedIds()],
        [ArrayParameterType::STRING]
    );

    return array_map(fn (string $ids) => json_decode($ids, true, \JSON_THROW_ON_ERROR), $usedMediaIds);
}
```

In the above example, `$this->connection` is an instance of `\Doctrine\DBAL\Connection` which can be injected in to your subscriber.
We use the MySQL JSON functions to query the table `my_slider_table`.
We check if there are any references to the Media IDs from the event, in the `slider_config` column which is a JSON blob. The `JSON_EXTRACT` function looks into the `images` key of the data. We use the where condition in combination with the `JSON_OVERLAPS` function to only query rows that have references to the Media IDs we are interested in.

Finally, we return all the IDs of Media which are used in the slider config so that they are not deleted.

Make sure to register your event subscriber to the [Dependency injection container](../../plugin-fundamentals/dependency-injection)
by using the tag `kernel.event_subscriber`.

```xml
// <plugin root>/src/Resources/config/services.xml
<?xml version="1.0" ?>
<container xmlns="http://symfony.com/schema/dic/services"
           xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
           xsi:schemaLocation="http://symfony.com/schema/dic/services http://symfony.com/schema/dic/services/services-1.0.xsd">

    <services>
        <service id="Swag\BasicExample\Subscriber\UnusedMediaSubscriber">
            <tag name="kernel.event_subscriber"/>
        </service>
    </services>
</container>
```

---

---

## Remote Thumbnail Generation
**Source:** [guides/plugins/plugins/content/media/remote-thumbnail-generation.md](https://developer.shopware.com/docs/v6.6/guides/plugins/plugins/content/media/remote-thumbnail-generation.md)  
# Remote Thumbnail Generation

::: info
This feature is available starting with Shopware version 6.6.4.0
:::

In certain scenarios, you might want to disable the filesystem thumbnail generation in Shopware and use an external CDN service to handle the thumbnails.
This can be beneficial for performance and scalability reasons.
When the remote thumbnail configuration is enabled, the thumbnail images and thumbnail records in the database are not generated by Shopware, but by the external service.

## Configuration

To use remote thumbnails, you need to adjust the following parameters in your `config/packages/shopware.yaml`:

```yaml
shopware:
  media:
    remote_thumbnails:
      enable: true
      pattern: '{mediaUrl}/{mediaPath}?width={width}&ts={mediaUpdatedAt}'
```

1. `shopware.media.remote_thumbnails.enable`: Set this parameter to `true` to enable remote thumbnails.

2. `shopware.media.remote_thumbnails.pattern`: This parameter defines the URL pattern for your remote thumbnails. Replace it with your actual URL pattern.

The pattern supports the following variables:

* `mediaUrl`: The base URL of the media file.
* `mediaPath`: The media file path relative to the `mediaUrl`.
* `width`: The width of the thumbnail.
* `height`: The height of the thumbnail.
* `mediaUpdatedAt`: The timestamp of the last media change.

For example, by default, the pattern was set as `{mediaUrl}/{mediaPath}?width={width}&ts={mediaUpdatedAt}`, the thumbnail URL would be generated as `https://yourshop.example/abc/123/456.jpg?width=80&ts=1718954838`.

## Usage

Once the configuration is set, Shopware will automatically use the defined pattern to generate thumbnail URLs.
These URLs will point to the external CDN service, which should handle generating and delivering the thumbnail images.

Please note that the external service needs to be able to handle the URL pattern and generate the appropriate thumbnails based on the provided parameters.

## Conclusion

By using remote thumbnails, you can offload the task of thumbnail generation to an external service, potentially improving the performance and scalability of your Shopware installation.

---

---

## SEO
**Source:** [guides/plugins/plugins/content/seo.md](https://developer.shopware.com/docs/v6.6/guides/plugins/plugins/content/seo.md)  
# SEO

The Shopware SEO feature offers the ability to add custom SEO URLs to optimize the search engine visibility of the e-commerce platform.

With the SEO plugin, you can create custom SEO URLs for product pages, categories, content pages, and other relevant sections of the website. The plugin allows businesses to customize meta tags for each page, including meta titles, descriptions, and keywords. This enables users to optimize the on-page SEO elements, providing search engines with relevant information about the content of the page.

---

---

## Add custom SEO URLs
**Source:** [guides/plugins/plugins/content/seo/add-custom-seo-url.md](https://developer.shopware.com/docs/v6.6/guides/plugins/plugins/content/seo/add-custom-seo-url.md)  
*(Body truncated in this bundle; follow the link for the rest.)*

# Add custom SEO URLs

## Overview

Every good website had to deal with it at some point: SEO URLs. Of course Shopware supports the usage of SEO URLs, e.g. for products or categories.

This guide however will cover the question on how you can define your own SEO URLs, e.g. for your own custom entities. This will include both static SEO URLs, as well as dynamic SEO URLs.

## Prerequisites

As every almost every guide in the plugins section, this guide as well is built upon the plugin base guide.

Furthermore, we're going to use a [Custom storefront controller](../../storefront/add-custom-controller) for the static SEO URL example, as well as [Custom entities](../../framework/data-handling/add-custom-complex-data) for the dynamic SEO URLs. Make sure you know and understand those two as well before diving deeper into this guide. Those come with two different solutions:

* Using [plugin migrations](../../plugin-fundamentals/database-migrations) for static SEO URLs
* Using [DAL events](../../framework/data-handling/using-database-events) to react on entity changes and therefore generating a dynamic SEO URL

## Custom SEO URLs

As already mentioned in the overview, this guide will be divided into two parts: Static and dynamic SEO URLs.

### Static SEO URLs

A static SEO URL doesn't have to change every now and then. Imagine a custom controller, which is accessible via the link `yourShop.com/example`.

Now if you want this URL to be translatable, you'll have to add a custom SEO URL to your controller route, so it is accessible using both `Example-Page` in English, as well as e.g. `Beispiel-Seite` in German.

#### Example controller

For this example, the controller from the [Add custom controller guide](../../storefront/add-custom-controller) is being used. It creates a controller with a route like the example mentioned above: `/example`

Let's now have a look at our example controller:

```php
// <plugin root>/src/Storefront/Controller/ExampleController.php
<?php declare(strict_types=1);

namespace Swag\BasicExample\Storefront\Controller;

use Shopware\Core\System\SalesChannel\SalesChannelContext;
use Shopware\Storefront\Controller\StorefrontController;
use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\Routing\Attribute\Route;

#[Route(defaults: ['_routeScope' => ['storefront']])]
class ExampleController extends StorefrontController
{
    #[Route(path: '/example', name: 'frontend.example.example', methods: ['GET'])]
    public function showExample(): Response
    {
        return $this->renderStorefront('@SwagBasicExample/storefront/page/example/index.html.twig', [
            'example' => 'Hello world'
        ]);
    }
}
```

The important information you'll need here is the route name, `frontend.example.example`, as well as the route itself: `/example`. Make sure to remember those for the next step.

#### Example migration

Creating a SEO URL in this scenario can be achieved by creating a [plugin migration](../../plugin-fundamentals/database-migrations).

The migration has to insert an entry for each sales channel and language into the `seo_url` table. For this case, we're making use of the `ImportTranslationsTrait`, which comes with a helper method `importTranslation`.

Don't be confused here, we'll just treat the `seo_url` table like a translation table, since it also needs a `language_id` and respective translated SEO URLs. You'll have to pass a German and an English array into an instance of the `Translations` class, which is then the second parameter for the `importTranslation` method.

Let's have a look at an example:

```php
// <plugin root>/src/Migration/Migration1619094740AddStaticSeoUrl.php
<?php declare(strict_types=1);

namespace Swag\BasicExample\Migration;

use Doctrine\DBAL\Connection;
use Shopware\Core\Defaults;
use Shopware\Core\Framework\Migration\MigrationStep;
use Shopware\Core\Framework\Uuid\Uuid;
use Shopware\Core\Migration\Traits\ImportTranslationsTrait;
use Shopware\Core\Migration\Traits\Translations;

class Migration1619094740AddStaticSeoUrl extends MigrationStep
{
    use ImportTranslationsTrait;

    public function getCreationTimestamp(): int
    {
        return 1619094740;
    }

    public function update(Connection $connection): void
    {
        $this->importTranslation('seo_url', new Translations(
            // German array
            array_merge($this->getSeoMetaArray($connection), ['seo_path_info' => 'Beispiel-Seite']),
            // English array
            array_merge($this->getSeoMetaArray($connection), ['seo_path_info' => 'Example-Page']),

        ), $connection);
    }

    public function updateDestructive(Connection $connection): void
    {
    }

    private function getSeoMetaArray(Connection $connection): array
    {
        return [
            'id' => Uuid::randomBytes(),
            'sales_channel_id' => $this->getStorefrontSalesChannelId($connection),
            'foreign_key' => Uuid::randomBytes(),
            'route_name' => 'frontend.example.example',
            'path_info' => '/example',
            'is_canonical' => 1,
            'is_modified' => 0,
            'is_deleted' => 0,
        ];
    }

    private function getStorefrontSalesChannelId(Connection $connection): ?string
    {
        $sql = <<<SQL
            SELECT id
            FROM sales_channel
            WHERE type_id = :typeId
SQL;
        $salesChannelId = $connection->fetchOne($sql, [
            ':typeId' => Uuid::fromHexToBytes(Defaults::SALES_CHANNEL_TYPE_STOREFRONT)
        ]);

        if (!$salesChannelId) {
            return null;
        }

        return $salesChannelId;
    }
}
```

You might want to have a look at the `getSeoMetaArray` method, that we implemented here. Most important for you are the columns `route_name` and `path_info` here, which represent the values you've defined in your controller's route attributes.

By using the default PHP method `array_merge`, we're then also adding our translated SEO URL to the column `seo_path_info`.

And that's it! After installing our plugin, you should now be able to access your controller's route with the given SEO URLs.

::: info
You can only access the German SEO URL if you've configured a German domain in your respective sales channel first.
:::

### Dynamic SEO URLs

Dynamic SEO URLs are URLs, that have to change every now and then. Yet, there's another separation necessary.

If you're going to generate custom SEO URLs for your custom entities, you'll have to follow the section about [Dynamic SEO URLs for entities](add-custom-seo-url#dynamic-seo-urls-for-entities). For all other kinds of dynamic content, that are not DAL entities, the section about [Dynamic SEO URLs for other content](add-custom-seo-url#dynamic-seo-urls-for-custom-content) is your way to go.

#### Dynamic SEO URLs for entities

This scenario will be about a custom entity, to be specific we're going to use the entity from our guide about [adding custom complex data](../../framework/data-handling/add-custom-complex-data), which then would have a custom Storefront route for each entity.

Each entity comes with a name, which eventually should be the SEO URL. Thus, your entity named `Foo` should be accessible using the route `yourShop.com/Foo` or `yourShop.com/Entities/Foo` or whatever you'd like. Now, everytime you create a new entity, a SEO URL has to be automatically created as well. When you update your entities' name, guess what, you'll have to change the SEO URL as well.

For this scenario, you can make use of the Shopware built-in `SeoUrlRoute` classes, which hold all necessary information about your dynamic route and will then create the respective `seo_url` entries automatically.

Let's first have a look at such an example class:

```php
// <plugin root>/src/Storefront/Framework/Seo/SeoUrlRoute/ExamplePageSeoUrlRoute.php
<?php declare(strict_types=1);

namespace Swag\BasicExample\Storefront\Framework\Seo\SeoUrlRoute;

use Shopware\Core\Content\Seo\SeoUrlRoute\SeoUrlMapping;
use Shopware\Core\Content\Seo\SeoUrlRoute\SeoUrlRouteConfig;
use Shopware\Core\Content\Seo\SeoUrlRoute\SeoUrlRouteInterface;
use Shopware\Core\Framework\DataAbstractionLayer\Entity;
use Shopware\Core\Framework\DataAbstractionLayer\Search\Criteria;
use Shopware\Core\System\SalesChannel\SalesChannelEntity;
use Swag\BasicExample\Core\Content\Example\ExampleDefinition;
use Swag\BasicExample\Core\Content\Example\ExampleEntity;

class ExamplePageSeoUrlRoute implements SeoUrlRouteInterface
{
    public const ROUTE_NAME = 'frontend.example.example';
    public const DEFAULT_TEMPLATE = '{{ example.name }}';

    private ExampleDefinition $exampleDefinition;

    public function __construct(ExampleDefinition $exampleDefinition)
    {
        $this->exampleDefinition = $exampleDefinition;
    }

    public function getConfig(): SeoUrlRouteConfig
    {
        return new SeoUrlRouteConfig(
            $this->exampleDefinition,
            self::ROUTE_NAME,
            self::DEFAULT_TEMPLATE,
            true
        );
    }

    public function prepareCriteria(Criteria $criteria): void
    {
    }

    public function getMapping(Entity $example, ?SalesChannelEntity $salesChannel): SeoUrlMapping
    {
        if (!$example instanceof ExampleEntity) {
            throw new \InvalidArgumentException('Expected ExampleEntity');
        }

        $exampleJson = $example->jsonSerialize();

        return new SeoUrlMapping(
            $example,
            ['exampleId' => $example->getId()],
            [
                'example' => $exampleJson,
            ]
        );
    }
}
```

```xml
// <plugin root>/src/Resources/config/services.xml
<?xml version="1.0" ?>
<container xmlns="http://symfony.com/schema/dic/services"
           xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
           xsi:schemaLocation="http://symfony.com/schema/dic/services http://symfony.com/schema/dic/services/services-1.0.xsd">

    <services>
        <service id="Swag\BasicExample\Storefront\Framework\Seo\SeoUrlRoute\ExamplePageSeoUrlRoute">
            <argument type="service" id="Swag\BasicExample\Core\Content\Example\ExampleDefinition"/>

            <tag name="shopware.seo_url.route"/>
        </service>
    </services>
</container>
```

Okay, so let's look through this step by step.

Your custom "SeoUrlRoute" class has to implement the `SeoUrlRouteInterface`, which comes with three necessary methods:

* `getConfig`: Here you have to return an instance of `SeoUrlRouteConfig`, containing your entity's definition,

  the technical name of the route to be used, and the desired SEO path.

* `prepareCriteria`: Here you can adjust the criteria instance, which will be used to fetch your entities.

  Here you can e.g. narrow down which entities may be used for the SEO URL generation. For example you could add a filter

  on an `active` field and therefore only generate SEO URLs for active entities. Also you can add associations here,

  which will then be available with the entity provided in the `getMapping` method.

* `getMapping`: In this method you have to return an instance of `SeoUrlMapping`. It has to contain the actually

  available data for the SEO URL template. If you're using a variable `example.name` in the SEO URL template, you have to

  provide the data for the key `example` here.

Make sure to check which kind of entity has been applied to the `getMapping` method, since you don't want to provide mappings for other entities than your custom one.

It then has to be registered to the container using the tag `shopware.seo_url.route`.

Now that you've set up this class, there are two more things to be done, which are covered in the next sections.

**Example subscriber**

Every time your entity is written now, you have to let Shopware know, that you want to generate the SEO URLs for those entities now. This is done by reacting to the [DAL events](../../framework/data-handling/using-database-events) of 

… **Truncated.** Full document: https://developer.shopware.com/docs/v6.6/guides/plugins/plugins/content/seo/add-custom-seo-url.md


---

## Extend robots.txt configuration
**Source:** [guides/plugins/plugins/content/seo/extend-robots-txt.md](https://developer.shopware.com/docs/guides/plugins/plugins/content/seo/extend-robots-txt.md)  
# Extend robots.txt configuration

## Overview

Since Shopware 6.7.1, the platform provides full `robots.txt` support with all standard directives and user-agent blocks.
This feature was developed as an open-source contribution during Hacktober 2024 ([learn more](https://www.shopware.com/en/news/hacktoberfest-2024-outcome-a-robots-txt-for-shopware/)).
For general configuration, refer to the [user documentation](https://docs.shopware.com/en/shopware-6-en/tutorials-and-faq/creation-of-robots-txt).

::: info
The events and features described in this guide are available since Shopware 6.7.5.
:::

You can extend the `robots.txt` functionality through events to:

* Add custom validation rules during parsing
* Modify or generate directives dynamically
* Support custom or vendor-specific directives
* Prevent warnings for known non-standard directives

## Prerequisites

This guide requires you to have a basic plugin running. If you don't know how to create a plugin, head over to the plugin base guide:

You should also be familiar with [Event listeners](../../plugin-fundamentals/listening-to-events).

::: info
This guide uses EventListeners since each example listens to a single event. If you need to subscribe to multiple events in the same class, consider using an [EventSubscriber](../../plugin-fundamentals/listening-to-events#listening-to-events-via-subscriber) instead.
:::

## Modifying parsed directives

The `RobotsDirectiveParsingEvent` is dispatched after `robots.txt` content is parsed. You can modify the parsed result, add validation, or inject dynamic directives.

This example shows how to dynamically add restrictions for AI crawlers:

```PHP
<?php declare(strict_types=1);

namespace Swag\Example\Listener;

use Psr\Log\LoggerInterface;
use Shopware\Core\Framework\Log\Package;
use Shopware\Storefront\Page\Robots\Event\RobotsDirectiveParsingEvent;
use Shopware\Storefront\Page\Robots\ValueObject\RobotsDirective;
use Shopware\Storefront\Page\Robots\ValueObject\RobotsDirectiveType;
use Shopware\Storefront\Page\Robots\ValueObject\RobotsUserAgentBlock;

#[Package('storefront')]
class RobotsExtensionListener
{
    public function __construct(
        private readonly LoggerInterface $logger,
    ) {
    }

    public function __invoke(RobotsDirectiveParsingEvent $event): void
    {
        $parsedRobots = $event->getParsedRobots();

        // Add restrictions for AI crawlers
        $aiCrawlers = ['GPTBot', 'ChatGPT-User', 'CCBot', 'anthropic-ai'];

        $aiBlock = new RobotsUserAgentBlock(
            userAgents: $aiCrawlers,
            directives: [
                new RobotsDirective(
                    type: RobotsDirectiveType::DISALLOW,
                    value: '/checkout/',
                ),
            ],
        );

        $parsedRobots->addUserAgentBlock($aiBlock);

        $this->logger->info('Extended robots.txt with AI crawler rules');
    }
}
```

```XML
<?xml version="1.0" ?>
<container xmlns="http://symfony.com/schema/dic/services"
           xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
           xsi:schemaLocation="http://symfony.com/schema/dic/services http://symfony.com/schema/dic/services/services-1.0.xsd">

    <services>
        <service id="Swag\Example\Listener\RobotsExtensionListener">
            <argument type="service" id="logger"/>
            <tag name="kernel.event_listener" event="Shopware\Storefront\Page\Robots\Event\RobotsDirectiveParsingEvent"/>
        </service>
    </services>
</container>
```

## Handling custom directives

The `RobotsUnknownDirectiveEvent` is dispatched when an unknown directive is encountered. Use this to support vendor-specific directives or prevent warnings for known non-standard directives:

```PHP
<?php declare(strict_types=1);

namespace Swag\Example\Listener;

use Shopware\Core\Framework\Log\Package;
use Shopware\Storefront\Page\Robots\Event\RobotsUnknownDirectiveEvent;

#[Package('storefront')]
class CustomDirectiveListener
{
    public function __invoke(RobotsUnknownDirectiveEvent $event): void
    {
        // Support Google and Yandex specific directives
        $knownCustomDirectives = ['noimageindex', 'noarchive', 'clean-param'];

        if (in_array(strtolower($event->getDirectiveName()), $knownCustomDirectives, true)) {
            $event->setHandled(true); // Prevent "unknown directive" warning
        }
    }
}
```

```XML
<?xml version="1.0" ?>
<container xmlns="http://symfony.com/schema/dic/services"
           xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
           xsi:schemaLocation="http://symfony.com/schema/dic/services http://symfony.com/schema/dic/services/services-1.0.xsd">

    <services>
        <service id="Swag\Example\Listener\CustomDirectiveListener">
            <tag name="kernel.event_listener" event="Shopware\Storefront\Page\Robots\Event\RobotsUnknownDirectiveEvent"/>
        </service>
    </services>
</container>
```

## Validation and parse issues

You can add validation warnings or errors during parsing using the `ParseIssue` class. This example shows common validation scenarios:

```PHP
<?php declare(strict_types=1);

namespace Swag\Example\Listener;

use Shopware\Core\Framework\Log\Package;
use Shopware\Storefront\Page\Robots\Event\RobotsDirectiveParsingEvent;
use Shopware\Storefront\Page\Robots\Parser\ParseIssue;
use Shopware\Storefront\Page\Robots\Parser\ParseIssueSeverity;
use Shopware\Storefront\Page\Robots\ValueObject\RobotsDirectiveType;

#[Package('storefront')]
class RobotsValidationListener
{
    public function __invoke(RobotsDirectiveParsingEvent $event): void
    {
        $parsedRobots = $event->getParsedRobots();

        // Validate crawl-delay values
        foreach ($parsedRobots->getUserAgentBlocks() as $block) {
            foreach ($block->getDirectives() as $directive) {
                if ($directive->getType() === RobotsDirectiveType::CRAWL_DELAY) {
                    $value = (int) $directive->getValue();

                    if ($value <= 0) {
                        $event->addIssue(new ParseIssue(
                            severity: ParseIssueSeverity::ERROR,
                            message: 'Invalid crawl-delay value: must be a positive integer',
                            lineNumber: null,
                        ));
                    }

                    if ($value > 10) {
                        $event->addIssue(new ParseIssue(
                            severity: ParseIssueSeverity::WARNING,
                            message: 'Crawl-delay value is very high. This may significantly slow down indexing.',
                            lineNumber: null,
                        ));
                    }
                }
            }
        }

        // Check for conflicting Allow/Disallow directives
        foreach ($parsedRobots->getUserAgentBlocks() as $block) {
            $disallowed = [];
            $allowed = [];

            foreach ($block->getDirectives() as $directive) {
                if ($directive->getType() === RobotsDirectiveType::DISALLOW) {
                    $disallowed[] = $directive->getValue();
                } elseif ($directive->getType() === RobotsDirectiveType::ALLOW) {
                    $allowed[] = $directive->getValue();
                }
            }

            foreach ($allowed as $allowPath) {
                foreach ($disallowed as $disallowPath) {
                    if ($allowPath === $disallowPath) {
                        $event->addIssue(new ParseIssue(
                            severity: ParseIssueSeverity::WARNING,
                            message: sprintf('Conflicting directives: Path "%s" is both allowed and disallowed', $allowPath),
                            lineNumber: null,
                        ));
                    }
                }
            }
        }
    }
}
```

```XML
<?xml version="1.0" ?>
<container xmlns="http://symfony.com/schema/dic/services"
           xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
           xsi:schemaLocation="http://symfony.com/schema/dic/services http://symfony.com/schema/dic/services/services-1.0.xsd">

    <services>
        <service id="Swag\Example\Listener\RobotsValidationListener">
            <tag name="kernel.event_listener" event="Shopware\Storefront\Page\Robots\Event\RobotsDirectiveParsingEvent"/>
        </service>
    </services>
</container>
```

Issues are automatically logged when the `robots.txt` configuration is saved in the Administration. Use `WARNING` for recommendations and `ERROR` for critical problems that prevent proper generation.

---

---

## Sitemap
**Source:** [guides/plugins/plugins/content/sitemap.md](https://developer.shopware.com/docs/v6.6/guides/plugins/plugins/content/sitemap.md)  
# Sitemap

Shopware Sitemap offers the ability to add sitemaps and modify sitemap entries within the e-commerce platform.

With the Sitemap plugin, you can create custom sitemaps to provide search engines with a structured overview of the website's content. These sitemaps can be tailored to specific requirements, allowing businesses to include relevant pages, categories, products, or other content sections based on their needs.

Additionally, the plugin enables users to modify sitemap entries. This means they can customize the information included in the sitemap, such as URLs change or overriding SEO URLs.

With this flexibility, businesses can ensure their website's content is efficiently crawled and indexed by search engines. Custom sitemaps and modified sitemap entries help improve the visibility and discoverability of the website, leading to better search engine rankings and increased traffic.

---

---

## Add Custom Sitemap Entries
**Source:** [guides/plugins/plugins/content/sitemap/add-custom-sitemap-entries.md](https://developer.shopware.com/docs/v6.6/guides/plugins/plugins/content/sitemap/add-custom-sitemap-entries.md)  
# Add Custom Sitemap Entries

## Overview

Of course Shopware comes with a sitemap generation feature, including products and categories, as well as some more URLs.
This guide however will cover how you can add your own custom URLs to the sitemap.

## By using the configuration

To add a custom URL to the sitemap, use the configuration setting `shopware.sitemap.custom_urls`

```yaml
shopware:
    sitemap:
        custom_urls:
            -   url: 'custom-url'
                salesChannelId: '98432def39fc4624b33213a56b8c944d'
                changeFreq: 'weekly'
                priority: 0.5
                lastMod: '2024-09-19 12:19:00'
            -   url: 'custom-url-2'
                salesChannelId: '98432def39fc4624b33213a56b8c944d'
                changeFreq: 'weekly'
                priority: 0.5
                lastMod: '2024-09-18 12:18:00'
```

The `salesChannelId` is the ID of the sales channel you want to add the URL to.

## By adding a URL provider

This part of the guide is mainly built upon the guide about \[Adding a custom SEO URL]\(../seo/add-custom-seo-url#Dynamic SEO URLs for entities),
so you might want to have a look at that.
The said guide comes with a custom entity, a controller with a technical route to display each entity, and a custom SEO URL.
All of this will be needed for this guide, as we're going to add the custom entity SEO URLs to the sitemap here.

So let's get started.
Adding custom URLs to the sitemap is done by adding a so-called "URL provider" to the system.

This is done by adding a new class, which is extending from `Shopware\Core\Content\Sitemap\Provider\AbstractUrlProvider`.
It then has to be registered to the [service container](../../plugin-fundamentals/dependency-injection) using the tag
`shopware.sitemap_url_provider`.

It has to provide three methods:

* `getDecorated`: Just throw an exception of type `DecorationPatternException` here. This is done for the sake of extending
  a class via decoration. Learn more about this [here](../../plugin-fundamentals/adjusting-service).
* `getName`: A technical name for your custom URLs
* `getUrls`: The main method to take care of. It has to return an instance of `Shopware\Core\Content\Sitemap\Struct\UrlResult`,
  containing an array of all URLs to be added.

Let's have a look at the example class:

```php
// <plugin root>/src/Core/Content/Sitemap/Provider/CustomUrlProvider.php
<?php declare(strict_types=1);

namespace Swag\BasicExample\Core\Content\Sitemap\Provider;

use Doctrine\DBAL\Connection;
use Shopware\Core\Content\Sitemap\Provider\AbstractUrlProvider;
use Shopware\Core\Content\Sitemap\Struct\Url;
use Shopware\Core\Content\Sitemap\Struct\UrlResult;
use Shopware\Core\Framework\DataAbstractionLayer\Doctrine\FetchModeHelper;
use Shopware\Core\Framework\DataAbstractionLayer\EntityRepository;
use Shopware\Core\Framework\DataAbstractionLayer\Search\Criteria;
use Shopware\Core\Framework\Plugin\Exception\DecorationPatternException;
use Shopware\Core\System\SalesChannel\SalesChannelContext;
use Swag\BasicExample\Core\Content\Example\ExampleEntity;
use Symfony\Component\Routing\Generator\UrlGeneratorInterface;
use Symfony\Component\Routing\RouterInterface;

class CustomUrlProvider extends AbstractUrlProvider
{
    public const CHANGE_FREQ = 'daily';
    public const PRIORITY = 1.0;

    private EntityRepository $exampleRepository;

    private Connection $connection;

    private RouterInterface $router;

    public function __construct(
        EntityRepository $exampleRepository,
        Connection $connection,
        RouterInterface $router
    ) {
        $this->exampleRepository = $exampleRepository;
        $this->connection = $connection;
        $this->router = $router;
    }

    public function getDecorated(): AbstractUrlProvider
    {
        throw new DecorationPatternException(self::class);
    }

    public function getName(): string
    {
        return 'custom';
    }

    /**
     * {@inheritdoc}
     */
    public function getUrls(SalesChannelContext $context, int $limit, ?int $offset = null): UrlResult
    {
        $criteria = new Criteria();
        $criteria->setLimit($limit);
        $criteria->setOffset($offset);

        $exampleEntities = $this->exampleRepository->search($criteria, $context->getContext());

        if ($exampleEntities->count() === 0) {
            return new UrlResult([], null);
        }

        $seoUrls = $this->getSeoUrls($exampleEntities->getIds(), 'frontend.example.example', $context, $this->connection);
        $seoUrls = FetchModeHelper::groupUnique($seoUrls);

        $urls = [];

        /** @var ExampleEntity $exampleEntity */
        foreach ($exampleEntities as $exampleEntity) {
            $exampleUrl = new Url();
            $exampleUrl->setLastmod($exampleEntity->getUpdatedAt() ?? new \DateTime());
            $exampleUrl->setChangefreq(self::CHANGE_FREQ);
            $exampleUrl->setPriority(self::PRIORITY);
            $exampleUrl->setResource(ExampleEntity::class);
            $exampleUrl->setIdentifier($exampleEntity->getId());

            if (isset($seoUrls[$exampleEntity->getId()])) {
                $exampleUrl->setLoc($seoUrls[$exampleEntity->getId()]['seo_path_info']);
            } else {
                $exampleUrl->setLoc(
                    $this->router->generate(
                        'frontend.example.example',
                        ['exampleId' => $exampleEntity->getId()],
                        UrlGeneratorInterface::ABSOLUTE_PATH
                    )
                );
            }

            $urls[] = $exampleUrl;
        }

        return new UrlResult($urls, null);
    }
}
```

```xml
// <plugin root>/src/Resources/config/services.xml
<?xml version="1.0" ?>
<container xmlns="http://symfony.com/schema/dic/services"
           xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
           xsi:schemaLocation="http://symfony.com/schema/dic/services http://symfony.com/schema/dic/services/services-1.0.xsd">

    <services>
        <service id="Swag\BasicExample\Core\Content\Sitemap\Provider\CustomUrlProvider" >
            <argument type="service" id="swag_example.repository" />
            <argument type="service" id="Doctrine\DBAL\Connection"/>
            <argument type="service" id="router"/>

            <tag name="shopware.sitemap_url_provider" />
        </service>
    </services>
</container>
```

Let's go through this step by step.
First of all we created a new class `CustomUrlProvider`, which is extending from the `AbstractUrlProvider`.
Following are the constants `CHANGE_FREQ` and `priority` - you don't have to add those values as constants of course.
They're going to be used later in the generation of the sitemap URLs.

Passed into the constructor are the repository for our [custom entity](../../framework/data-handling/add-custom-complex-data),
the DBAL connection used for actually fetching SEO URLs from the database, and the Symfony router in order to generate SEO URLs
that have not yet been written to the database.

Now let's get to the main method `getUrls`.
Here we start of with fetching all custom entities, using the provided `$limit` and `$offset` values.
Make sure to always use those values, as the sitemap support "paging" and therefore you do not want to simply fetch all
of your entities.
If there aren't any entities to be fetched, there is nothing more to be done here.

Afterwards we fetch all already existing SEO URLs for our custom entities. Once again, have a look at our guide about
\[adding a custom SEO URL]\(../seo/add-custom-seo-url#Dynamic SEO URLs for entities) if you don't know how to add custom
SEO URLs in the first place.

We're then iterating over all of our fetched entities and we create an instance of `Shopware\Core\Content\Sitemap\Struct\Url`
for each iteration.
This struct requests each of the typical sitemap information:

* `lastMod`: The last time this entry was modified. Just use the `updatedAt` value here, if available
* `changeFreq`: How often will the entry most likely change?
  Possible values are `always`, `hourly`, `daily`, `weekly`, `monthly`, `yearly` and `never`
* `priority`: Has to have a value between 0 and 1. URLs with higher priority are considered to be "more important" by common
  search engines.
* `resource`: Just a name for your entry, in this example we're just using the entity class name
* `identifier`: The ID of the entry, if available

The most important entry is set afterwards, which is the `location`: The actual SEO URL to be indexed.
We're setting this value by checking if the SEO URL for the given entity was already generated, and if not, we're generating it on the fly.

All of those instances are then stored in array, which in return is passed to the `UrlResult`.
And that's it already!

---

---

## Modify Sitemap Entries
**Source:** [guides/plugins/plugins/content/sitemap/modify-sitemap-entries.md](https://developer.shopware.com/docs/v6.6/guides/plugins/plugins/content/sitemap/modify-sitemap-entries.md)  
# Modify Sitemap Entries

## Overview

You might have had a look at our guide about [adding custom sitemap entries](add-custom-sitemap-entries),
e.g. for a custom entity.
However, you might not want to add new URLs, but rather modify already existing ones.
This guide will cover modifying e.g. the product URLs for the sitemap.

## Prerequisites

This guide is built upon the [Plugin base guide](../../plugin-base-guide), like most guides.

Modifying the sitemap entries is done via decoration, so should know how that's done as well.
Also, knowing how the URL providers work, like it's explained in our guide about [adding custom sitemap entries](add-custom-sitemap-entries),
will come in handy.

## Modifying the sitemap

There's two ways of actually modifying the sitemap entries, but both ways are done by decorating
the respective `UrlProvider`, e.g. the `Shopware\Core\Content\Sitemap\Provider\ProductUrlProvider` for products.

Hence, let's start with creating the basic decorated class for the `ProductUrlProvider`. We'll call
this class `DecoratedProductUrlProvider`:

```php
// <plugin root>/src/Core/Content/Sitemap/Provider/DecoratedProductUrlProvider.php
<?php declare(strict_types=1);

namespace Swag\BasicExample\Core\Content\Sitemap\Provider;

use Doctrine\DBAL\Connection;
use Shopware\Core\Content\Sitemap\Provider\AbstractUrlProvider;
use Shopware\Core\Content\Sitemap\Struct\UrlResult;
use Shopware\Core\Framework\Uuid\Uuid;
use Shopware\Core\System\SalesChannel\SalesChannelContext;

class DecoratedProductUrlProvider extends AbstractUrlProvider
{
    private AbstractUrlProvider $decoratedUrlProvider;

    public function __construct(AbstractUrlProvider $abstractUrlProvider)
    {
        $this->decoratedUrlProvider = $abstractUrlProvider;
    }

    public function getDecorated(): AbstractUrlProvider
    {
        return $this->decoratedUrlProvider;
    }

    public function getName(): string
    {
        return $this->getDecorated()->getName();
    }

    public function getUrls(SalesChannelContext $context, int $limit, ?int $offset = null): UrlResult
    {
        return $this->getDecorated()->getUrls($context, $limit, $offset);
    }
}
```

```xml
// <plugin root>/src/Resources/config/services.xml
<?xml version="1.0" ?>
<container xmlns="http://symfony.com/schema/dic/services"
           xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
           xsi:schemaLocation="http://symfony.com/schema/dic/services http://symfony.com/schema/dic/services/services-1.0.xsd">

    <services>
        <service id="Swag\BasicExample\Core\Content\Sitemap\Provider\DecoratedProductUrlProvider" decorates="Shopware\Core\Content\Sitemap\Provider\ProductUrlProvider">
            <argument type="service" id="Swag\BasicExample\Core\Content\Sitemap\Provider\DecoratedProductUrlProvider.inner" />
        </service>
    </services>
</container>
```

Now let's get on to the two possible ways and its benefits.

### Adjusting the getUrls method

By adjusting the `getUrls` method, you can execute the parent's `getUrls` method and modify its return value, which
is an instance of the `UrlResult`.
On this instance, you can use the method `getUrls` to actually get the `Url` instances and make adjustments to them - or even remove them.

```php
// <plugin root>/src/Core/Content/Sitemap/Provider/DecoratedProductUrlProvider.php
public function getUrls(SalesChannelContext $context, int $limit, ?int $offset = null): UrlResult
{
    $urlResult = $this->getDecorated()->getUrls($context, $limit, $offset);
    $urls = $urlResult->getUrls();

    /* Change $urls, e.g. removing entries or updating them by iterating over them. */

    return new UrlResult($urls, $urlResult->getNextOffset());
}
```

You could iterate over the `$urls` array and modify each entry - or even create a new array with less entries,
if you want to fully remove some.

There is one main downside to this way:
You don't have access to a lot of information about the entity itself, that was used for this `Url` instance.
E.g. if you'd like to filter all products with a given name, you can't do that here, since the name itself isn't available.
The only reliable information you have here, is the ID of the entity by using the method `getIdentifier` on the `Url` instance.

Also, it's not the best way in terms of performance to read all SEO URLs from the database, only to filter them afterwards.

### Overriding the getSeoUrls method

The available SEO URLs are read in the protected method `getSeoUrls` of the `AbstractUrlProvider`.
Since it's a protected method, you can override it and create a custom SQL in order to only read the data you really want.

For this you'll most likely want to copy the original method's code and paste it into your overridden method.
You can then add new lines to the SQL statement in order to do the necessary filtering or customising.

```php
// <plugin root>/src/Core/Content/Sitemap/Provider/DecoratedProductUrlProvider.php
protected function getSeoUrls(array $ids, string $routeName, SalesChannelContext $context, Connection $connection): array
{
    /* Make adjustments to this SQL */
    $sql = 'SELECT LOWER(HEX(foreign_key)) as foreign_key, seo_path_info
                FROM seo_url WHERE foreign_key IN (:ids)
                 AND `seo_url`.`route_name` =:routeName
                 AND `seo_url`.`is_canonical` = 1
                 AND `seo_url`.`is_deleted` = 0
                 AND `seo_url`.`language_id` =:languageId
                 AND (`seo_url`.`sales_channel_id` =:salesChannelId OR seo_url.sales_channel_id IS NULL)';

    return $connection->fetchAll(
        $sql,
        [
            'routeName' => $routeName,
            'languageId' => Uuid::fromHexToBytes($context->getSalesChannel()->getLanguageId()),
            'salesChannelId' => Uuid::fromHexToBytes($context->getSalesChannelId()),
            'ids' => Uuid::fromHexToBytesList(array_values($ids)),
        ],
        [
            'ids' => Connection::PARAM_STR_ARRAY,
        ]
    );
}
```

Now you could adjust the SQL statement to fit your needs, e.g. by adding a `JOIN` to the respective entities' table.

However, there is a downside here as well:
Overriding the method like this is not really update-compatible. If the original method is changed in a future
update, those changes will not apply for your modification, hence you might not receive a performance update or a bugfix
for those few lines of code.

---

---

## Remove Sitemap Entries
**Source:** [guides/plugins/plugins/content/sitemap/remove-sitemap-entries.md](https://developer.shopware.com/docs/v6.6/guides/plugins/plugins/content/sitemap/remove-sitemap-entries.md)  
# Remove Sitemap Entries

## Overview

This guide covers how to remove URLs from the sitemap.

## By using the configuration

To remove a URL from the sitemap, use the configuration setting `shopware.sitemap.excluded_urls`

```yaml
shopware:
    sitemap:
        excluded_urls:
            -   salesChannelId: '98432def39fc4624b33213a56b8c944d'
                resource: 'Shopware\Core\Content\Product\ProductEntity'
                identifier: 'd20e4d60e35e4afdb795c767eee08fec'
```

The `salesChannelId` is the ID of the sales channel from which you want to exclude the URL.
The `resource` is the full class name of the entity from which you want to exclude the URL, for example, `Shopware\Core\Content\Product\ProductEntity`.
The `identifier` is the entity's ID for which you want to exclude the URL.

---

---

## Stock
**Source:** [guides/plugins/plugins/content/stock.md](https://developer.shopware.com/docs/v6.6/guides/plugins/plugins/content/stock.md)  
# Stock

::: info
The stock management system is available from Shopware 6.5.5.0. It is only enabled if the shop owner has enabled the `\STOCK_HANDLING\` feature flag.
:::

The stock management system allows the allocation of stocks to products. Stock is incremented and decremented as orders are placed, modified, canceled, and refunded.

In order to accommodate for the various use cases, the stock management system has been kept as simple as possible. The shop owner can deactivate it entirely if not required.

To enable or disable this feature, refer to [stock configuration](../../../../../guides/hosting/configurations/shopware/stock) section.

---

---

## Implementing your own stock storage
**Source:** [guides/plugins/plugins/content/stock/implementing-your-own-stock-storage.md](https://developer.shopware.com/docs/v6.6/guides/plugins/plugins/content/stock/implementing-your-own-stock-storage.md)  
# Implementing your own stock storage

## Overview

Shopware stores stock as simple integer values in the `product` table. If you need a more advanced stock management system or would like to write the stock alterations to a different system, you can implement your own stock storage.

## Prerequisites

Here you will be decorating a service; therefore, it will be helpful to familiarise yourself with the [Adjusting a Service](../../../../../guides/plugins/plugins/plugin-fundamentals/adjusting-service) guide.

## Add a decorator to load the stock

First, to communicate stock alterations to a third-party service, you will have to decorate `\Shopware\Core\Content\Product\Stock\AbstractStockStorage` and implement the `alter` method. This method is triggered with an array of `StockAlteration`'s, which contains:

* the Product and Line Item IDs,
* the old quantity and
* the new quantity.

```php
// <plugin root>/src/Swag/Example/Service/StockStorageDecorator.php
<?php declare(strict_types=1);

namespace Swag\Example\Service;

use Shopware\Core\Content\Product\Stock\AbstractStockStorage;
use Shopware\Core\Content\Product\Stock\StockData;
use Shopware\Core\Content\Product\Stock\StockDataCollection;
use Shopware\Core\Content\Product\Stock\StockLoadRequest;
use Shopware\Core\Framework\Context;
use Shopware\Core\System\SalesChannel\SalesChannelContext;
use Shopware\Core\Content\Product\Stock\StockAlteration;

class StockStorageDecorator extends AbstractStockStorage
{
    public function __construct(private AbstractStockStorage $decorated, private MyStockApi $stockApi)
    {
    }

    public function getDecorated(): AbstractStockStorage
    {
        return $this->decorated;
    }

    public function load(StockLoadRequest $stockRequest, SalesChannelContext $context): StockDataCollection
    {
        return $this->decorated->load($stockRequest, $context);
    }

    /**
     * @param list<StockAlteration> $changes  
     */
    public function alter(array $changes, Context $context): void
    {
        foreach ($changes as $alteration) {
            $this->stockApi->updateStock($alteration->productId, $alteration->newQuantity);
        }
        
        $this->decorated->alter($changes, $context);
    }

    public function index(array $productIds, Context $context): void
    {
        $this->decorated->index($productIds, $context);
    }
}
```

```xml
// <plugin root>/src/Resources/config/services.xml
<?xml version="1.0" ?>
<container xmlns="http://symfony.com/schema/dic/services"
           xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
           xsi:schemaLocation="http://symfony.com/schema/dic/services http://symfony.com/schema/dic/services/services-1.0.xsd">

    <services>
        <service id="Swag\Example\Service\StockStorageDecorator" decorates="Shopware\Core\Content\Product\Stock\StockStorage">
            <argument type="service" id="Swag\Example\Service\StockStorageDecorator.inner" />
        </service>
    </services>
</container>
```

The alter method will be called when the stock of a product should be updated. The `$changes` array contains a list of `StockAlteration` instances. These objects contain the following properties/methods:

| Property/Method | Type   | Description                                             |
|-----------------|--------|---------------------------------------------------------|
| lineItemId      | string | The ID of the line item that triggered the stock update |
| productId       | string | The ID of the product that should be updated            |
| quantityBefore  | int    | The old product stock level                             |
| newQuantity     | int    | The new product stock level                             |
| quantityDelta() | int    | The difference between the old and new stock level      |

## Stock changing scenarios

The following list contains all the scenarios that trigger stock alterations. All implementations of `AbstractStockStorage` should be able to handle these scenarios.

* Order placed
* Order canceled
* Order deleted
* Cancelled order, reopened
* Line item added to the order
* Line item removed from an order
* Line item updated (Product qty increased)
* Line item updated (Product qty decreased)
* Line item updated (Product sku changed)

All of these scenarios are handled by the event subscriber `Shopware\Core\Content\Product\Stock\OrderStockSubscriber`.

## Further extension points for advanced customization

1. If you need to listen to more events to trigger stock alterations, you can create an event subscriber for the required events and call the `\Shopware\Core\Content\Product\Stock\AbstractStockStorage::alter` method with a `StockAlteration` instance representative of the alteration.
2. If you don't want to use Shopware's default events and stock storage, you can implement your own system and recommend that the project owner disables the Shopware stock management system. Refer them to [Configuration guide](../../../../../guides/hosting/configurations/shopware/stock).

---

---

## Loading Stock Information from a Different Source
**Source:** [guides/plugins/plugins/content/stock/loading-stock-information-from-different-source.md](https://developer.shopware.com/docs/v6.6/guides/plugins/plugins/content/stock/loading-stock-information-from-different-source.md)  
# Loading Stock Information from a Different Source

## Overview

If Shopware is not the source of truth for your stock data, you can customize the stock loading process and provide your data from a third-party source.

## Prerequisites

Here again, you will be decorating a service; therefore, it will be helpful to familiarise yourself with the [Adjusting a Service](../../../../../guides/plugins/plugins/plugin-fundamentals/adjusting-service) guide.

## Add a decorator to load the stock

For example, to load stock from a third-party API, you need to decorate `\Shopware\Core\Content\Product\Stock\AbstractStockStorage` and implement the `load` method. When products are loaded in Shopware the `load` method will be invoked with the loaded product IDs.

```php
// <plugin root>/src/Swag/Example/Service/StockStorageDecorator.php
<?php declare(strict_types=1);

namespace Swag\Example\Service;

use Shopware\Core\Content\Product\Stock\AbstractStockStorage;
use Shopware\Core\Content\Product\Stock\StockData;
use Shopware\Core\Content\Product\Stock\StockDataCollection;
use Shopware\Core\Content\Product\Stock\StockLoadRequest;
use Shopware\Core\Framework\Context;
use Shopware\Core\System\SalesChannel\SalesChannelContext;

class StockStorageDecorator extends AbstractStockStorage
{
    public function __construct(private AbstractStockStorage $decorated)
    {
    }

    public function getDecorated(): AbstractStockStorage
    {
        return $this->decorated;
    }

    public function load(StockLoadRequest $stockRequest, SalesChannelContext $context): StockDataCollection
    {
        $productsIds = $stockRequest->productIds;

        //use $productIds to make an API request to get stock data
        //$result would come from the api response
        $result = ['product-1' => 5, 'product-2' => 10];

        return new StockDataCollection(
            array_map(function (string $productId, int $stock) {
                return new StockData($productId, $stock, true);
            }, array_keys($result), $result)
        );
    }

    public function alter(array $changes, Context $context): void
    {
        $this->decorated->alter($changes, $context);
    }

    public function index(array $productIds, Context $context): void
    {
        $this->decorated->index($productIds, $context);
    }
}
```

```xml
// <plugin root>/src/Resources/config/services.xml
<?xml version="1.0" ?>
<container xmlns="http://symfony.com/schema/dic/services"
           xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
           xsi:schemaLocation="http://symfony.com/schema/dic/services http://symfony.com/schema/dic/services/services-1.0.xsd">

    <services>
        <service id="Swag\Example\Service\StockStorageDecorator" decorates="Shopware\Core\Content\Product\Stock\StockStorage">
            <argument type="service" id="Swag\Example\Service\StockStorageDecorator.inner" />
        </service>
    </services>
</container>
```

In your `load` method, you can access the product IDs from the `StockLoadRequest` instance and perform a request to your system to retrieve the data.

You then construct and return a `StockDataCollection` full of `StockData` instances. Each `StockData` instance represents a product.

You can use the static method `Shopware\Core\Content\Product\Stock::fromArray()` to construct an instance, passing in an array of the stock attributes.

There are several required values and some optional values.

| Attribute   | Type    | Description                                                     | Optional/Required |
|-------------|---------|-----------------------------------------------------------------|-------------------|
| productId   | string  | The product ID                                                  | Required          |
| stock       | int     | The stock amount                                                | Required          |
| available   | boolean | Whether the product is considered available                     | Required          |
| minPurchase | int     | The minimum purchase value for this product                     | Optional          |
| maxPurchase | int     | The maximum purchase value for this product                     | Optional          |
| isCloseout  | boolean | Whether the product can be ordered if there is not enough stock | Optional          |

For example:

```php
$stockData = \Shopware\Core\Content\Product\Stock\StockData::fromArray([
    'productId' => 'product-1',
    'stock' => 5,
    'available' => true,
    'minPurchase' => 1,
    'maxPurchase' => 10,
    'isCloseout' => false,
]);
```

It is also possible to provide arbitrary data via extensions:

```php
$stockData = \Shopware\Core\Content\Product\Stock\StockData::fromArray([
    'productId' => 'product-1',
    'stock' => 5,
    'available' => true,
]);

$stockData->addArrayExtension('extraData', ['foo' => 'bar']);
```

The values in the `StockData` instance will be used to update the loaded product instance. Furthermore, fetching the `StockData` instance from the product via the `stock_data` extension is possible. For example:

```php
$stockData = $product->getExtension('stock_data');
```

---

---

## Reading and Writing Stock
**Source:** [guides/plugins/plugins/content/stock/reading-writing-stock.md](https://developer.shopware.com/docs/v6.6/guides/plugins/plugins/content/stock/reading-writing-stock.md)  
# Reading and Writing Stock

## Overview

Shopware stores the current stock level alongside the product, this guide will help you when you want to read and write that value.

## Reading Stock

The `product.stock` field should be used to read the current stock level. When building extensions that need to query a product's stock, use this field. It is always a real-time calculated value of the available product stock.

```php
// <plugin root>/src/Swag/Example/ServiceReadingData.php
<?php declare(strict_types=1);

namespace Swag\Example\Service;

use Shopware\Core\Framework\DataAbstractionLayer\EntityRepository;
use Shopware\Core\Framework\Context;
use Shopware\Core\Framework\DataAbstractionLayer\Search\Criteria;

class ReadingStock
{
    private EntityRepository $productRepository;

    public function __construct(EntityRepository $productRepository)
    {
        $this->productRepository = $productRepository;
    }
    
    public function read(Context $context): void
    {
        $product = $this->productRepository
            ->search(new Criteria([$productId]), $context)
            ->first();
            
        $stock = $product->getStock();
    }
}
```

## Writing Stock

The `product.stock` field should be used to write the current stock level.

```php
// <plugin root>/src/Swag/Example/ServiceReadingData.php
<?php declare(strict_types=1);

namespace Swag\Example\Service;

use Shopware\Core\Framework\DataAbstractionLayer\EntityRepository;
use Shopware\Core\Framework\Context;
use Shopware\Core\Framework\DataAbstractionLayer\Search\Criteria;

class WritingStock
{
    private EntityRepository $productRepository;

    public function __construct(EntityRepository $productRepository)
    {
        $this->productRepository = $productRepository;
    }
    
    public function write(string $productId, int $stock, Context $context): void
    {
        $this->productRepository->update(
            [
                [
                    'id' => $productId,
                    'stock' => $stock
                ]
            ],
            $context
        );
    }
}
```

---

---

