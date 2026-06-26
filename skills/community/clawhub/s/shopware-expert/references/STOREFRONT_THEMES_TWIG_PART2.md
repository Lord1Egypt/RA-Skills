# STOREFRONT THEMES TWIG

Compiled excerpts from the Shopware Developer Documentation snapshot. Prefer live docs at [developer.shopware.com](https://developer.shopware.com/) when in doubt.

---

## Reacting to Cookie Consent Changes
**Source:** [guides/plugins/plugins/storefront/reacting-to-cookie-consent-changes.md](https://developer.shopware.com/docs/v6.6/guides/plugins/plugins/storefront/reacting-to-cookie-consent-changes.md)  
# Reacting to Cookie Consent Changes

## Overview

This small guide will bring a short example on how to react on changes for the cookie consent made by the user via JavaScript.

## Prerequisites

This guide was built upon both the [Plugin base guide](../plugin-base-guide) as well as the [Adding a cookie to the consent manager](add-cookie-to-manager) guide, so make sure to know those beforehand. Also nice to know is the guide about [Reacting to javascript events](reacting-to-javascript-events), since this will be done here, same as how to [create and load a JavaScript](add-custom-javascript) file in the first place, which can be found.

## Reacting to cookie configuration changes via JavaScript

Everytime a user saves a cookie configuration, an event is published to the document's event emitter. The event only contains the changeset for the cookie configuration as an object.

In the following example we'll check for a cookie with name `cookie-key-1`, just like we created one of the cookies in our guide about [Adding a cookie to the consent manager](add-cookie-to-manager).

You can listen for this event using the following lines:

```javascript
// <plugin root>/src/Resources/app/storefront/src/reacting-cookie/reacting-cookie.js
import { COOKIE_CONFIGURATION_UPDATE } from 'src/plugin/cookie/cookie-configuration.plugin';

document.$emitter.subscribe(COOKIE_CONFIGURATION_UPDATE, eventCallback);

function eventCallback(updatedCookies) {
    if (typeof updatedCookies.detail['cookie-key-1'] !== 'undefined') {
        // The cookie with the cookie attribute "cookie-key-1" either is set active or from active to inactive
        let cookieActive = updatedCookies.detail['cookie-key-1'];
    } else {
        // The cookie with the cookie attribute "cookie-key-1" was not updated
    }
}
```

So first of all we're registering to the event `COOKIE_CONFIGURATION_UPDATE` and apply our own custom callback here. The custom callback then checks for the updated cookies, which are stored in `updatedCookies.detail`. If your cookie is not defined in there, it wasn't changed. If you can find it, it will contain the new active state.

This way you can properly react on cookie consent changes made by the user.

### Loading the JavaScript file

Just like with every custom JavaScript file, you have to load this one as well in your plugin's main entry file, which is the `main.js`.

```javascript
// <plugin root>/src/Resources/app/storefront/src/main.js
import './reacting-cookie/reacting-cookie'
```

---

---

## Reacting to Javascript Events on Storefront
**Source:** [guides/plugins/plugins/storefront/reacting-to-javascript-events.md](https://developer.shopware.com/docs/v6.6/guides/plugins/plugins/storefront/reacting-to-javascript-events.md)  
# Reacting to Javascript Events on Storefront

## Overview

Just like in PHP, there may be useful events in our JavaScript plugins, which you can use to extend the default behavior. This guide will show you how this is done and you can find events, if there's any available for your needs.

## Prerequisites

As most guides, this one is built upon our [Plugin base guide](../plugin-base-guide), but that one is not necessary, you do need a running plugin though! Also this guide will **not** explain how to create a JavaScript plugin in general, head over to our guide [adding custom javascript](add-custom-javascript) to understand how that's done in the first place.

## JavaScript base class

As already mentioned, this guide will not explain how to create a JavaScript plugin in the first place. For this guide, we'll use the following example JavaScript plugin:

```javascript
// <plugin root>/src/Resources/app/storefront/src/events-plugin/events-plugin.plugin.js
const { PluginBaseClass } = window;

export default class EventsPlugin extends PluginBaseClass {
    init() {
    }
}
```

This one will be used from now on.

## Finding events

So before you can start reacting and listening to events, you need to find them first. Since not every plugin implements events, they can be hard to find by just looking through the code.

Instead, rather search for `this.$emitter.publish` in the directory `platform/src/Storefront/Resources/app/storefront/src` to find all occurrences of events being published. This way, you may or may not find an event useful for your needs, so you don't have to override other JavaScript plugins.

## Registering to events

Now that you possibly found your event, it's time to register to it and execute code once it is fired. For this example, we will listen to the event when the cookie bar is hidden. The respective event can be found via the name [hideCookieBar](https://github.com/shopware/shopware/blob/v6.3.4.1/src/Storefront/Resources/app/storefront/src/plugin/cookie/cookie-permission.plugin.js#L71).

```javascript
// <plugin root>/src/Resources/app/storefront/src/events-plugin/events-plugin.plugin.js
const { PluginBaseClass } = window;

export default class EventsPlugin extends PluginBaseClass {
    init() {
        const plugin = window.PluginManager.getPluginInstanceFromElement(document.querySelector('[data-cookie-permission]'), 'CookiePermission');
        plugin.$emitter.subscribe('hideCookieBar', this.onHideCookieBar);
    }

    onHideCookieBar() {
        alert("The cookie bar has been hidden!");
    }
}
```

Let's have a look at the code. There's one thing you have to understand first. When a plugin calls `this.$emitter.publish`, this event is fired on the plugin's own `$emitter` instance. This means: Every plugin has its own instance of the emitter. Therefore, you cannot just use `this.$emitter.subscribe` to listen to other plugin's events.

Rather, you have to fetch the respective plugin instance using the `PluginManager` and then you have to use `subscribe` on their `$emitter` instance: `plugin.$emitter.subscribe`

And this is done here. We're fetching the instance of the `CookiePermission` plugin by its [selector](https://github.com/shopware/shopware/blob/v6.3.4.1/src/Storefront/Resources/app/storefront/src/main.js#L103) via the `PluginManager` and using that instance to register to the event. Once the event is then fired, our own method `onHideCookieBar` is executed and the `alert` will be shown.

::: warning
This does **not** prevent the execution of the original method. Consider those events to be "notifications".
:::

## Next steps

Everytime you don't find an event to implement the changes you need, you may have to override the plugin itself. For this case, head over to our guide about [Override existing javascript](override-existing-javascript).

---

---

## Remove Javascript Plugin
**Source:** [guides/plugins/plugins/storefront/remove-unnecessary-js-plugin.md](https://developer.shopware.com/docs/v6.6/guides/plugins/plugins/storefront/remove-unnecessary-js-plugin.md)  
# Remove Javascript Plugin

## Overview

When you develop your own plugin, you might want to exclude Javascript plugins at some occasions. For example, if you don't want a Core plugin to interfere, with your own code. This guide will teach you how to remove this Javascript plugin with your own Shopware plugin.

## Prerequisites

While this is not mandatory, having read the guide about adding custom javascript plugins beforehand might help you understand this guide a bit further:

Other than that, this guide just requires you to have a running plugin installed, e.g. our plugin from the plugin base guide:

## Unregistering Javascript Plugin

Imagine we wanted to exclude the `OffCanvasCart` plugin, just to get a test case which can be inspected easily. In order to remove a Javascript plugin, you only need to add the following line to your `main.js` file:

```javascript
// <plugin root>/src/Resources/app/storefront/src/main.js
window.PluginManager.deregister('OffCanvasCart', '[data-off-canvas-cart]');
```

After building the Storefront anew, you shouldn't be able to open the offcanvas cart anymore. Another useful way of testing this is using your browser's devtools. Just open your devtool's console and type in `PluginManager.getPluginList()` in order to get a list of all registered plugins.

In our case, we shouldn't find `OffCanvasCart` in the listed plugins anymore.

## Next steps

Did you already take a look at our other storefront guides? They can give you some neat starting points on how to extend and customize Shopware's storefront.

* [Override existing Javascript in your plugin](override-existing-javascript)
* [Reacting to Javascript events](reacting-to-javascript-events)

---

---

## Use CSRF Protection
**Source:** [guides/plugins/plugins/storefront/use-csrf-protection.md](https://developer.shopware.com/docs/v6.4/guides/plugins/plugins/storefront/use-csrf-protection.md)  
# Use CSRF Protection

## Overview

One of the common security risks of your application could be a [Cross Site Request Forgery](https://owasp.org/www-community/attacks/csrf) (CSRF) attack. This short guide will teach you how to properly secure your forms in the Storefront by using Shopware's built-in tools.

## Prerequisites

Since this guide will be a general example and not a plugin-specific one, there is no need for a running plugin. However, it will assume you've got a custom `form` element in the Storefront, which you want to secure.

Knowing what exactly CSRF is and how the attack works may come in handy, so you might want to have a look at the [OWASP page regarding CSRF](https://owasp.org/www-community/attacks/csrf).

## Use CSRF protection for form

As already mentioned, this guide assumed you've already got a custom form running, which needs CSRF protection. The following will be the example form we're going to use:

```html
<form action="{{ path('some.action') }}"
    method="post"
    data-form-csrf-handler="true"
    class="some-form-class">
    <div class="some-container-class">
        <button type="submit" class="btn btn-primary btn-block">Some button</button>
        <input type="hidden" name="mayNotBeManipulated" value="sensible value">
    </div>
</form>
```

Just a basic form with a submit button and a hidden input, that must not be manipulated.

Every storefront `POST` request is checked for a valid CSRF token to prevent [Cross Site Request Forgery attacks](https://owasp.org/www-community/attacks/csrf), since by default every Storefront route is automatically looking for a CSRF token. This also means, that the simple example form mentioned above will not work, since it's missing a CSRF token. You can make the form work, by disabling the CSRF protection on your route.

Protecting it now with the built-in tools requires you to add two new lines, but let's have a look at a secure example first:

```html
<form action="{{ path('some.action') }}"
    method="post"
    data-form-csrf-handler="true"
    class="some-form-class">
    <div class="some-container-class">
        <button type="submit" class="btn btn-primary btn-block">Some button</button>
        <input type="hidden" name="mayNotBeManipulated" value="sensible value">

        {{ sw_csrf('some.action') }}
    </div>
</form>
```

Shopware 6 provides two different mechanisms for token generation:

* The default recommended method is to generate CSRF tokens server side via twig and include them in forms. In the example, this is done with the twig function `sw_csrf`, whose parameter has to match the route its protecting. This is necessary, because the javascript mechanism won't work if the user disabled javascript in his browser.
* Ajax can also be used to generate token and append them to `POST` requests. The CSRF mode has to be set so `ajax` for this to work. This method is needed while using a third party cache provider like varnish. Read more on this in the caching section below. For that case, we're registering the [FormCsrfHandler plugin](https://github.com/shopware/platform/blob/v6.3.4.1/src/Storefront/Resources/app/storefront/src/plugin/forms/form-csrf-handler.plugin.js) on your form, which will take care of generating a CSRF token via javascript.

Therefore, the two new lines are the following:

* The `sw_csrf` function is used to generate a valid CSRF token with twig and append it as a hidden input field to the form.

  It also accepts a `mode` parameter which can be set to `token` or `input`(default):

  ```text
    {{ sw_csrf('example.route', {"mode": "token"}) }}
  ```

  * Mode `token` renders only a blank token. This can be used to create an own input element or to hand over the token to a JS plugin.
  * Mode `input` renders a hidden input field with the token as value
  * Important: Note that the parameter of the `sw_csrf` function must match the route name for the action. Every token is only valid for a specific route.

* The data attribute `data-form-csrf-handler="true"` initialises the JS plugin if the `csrf` mode is set to `ajax`. This will fetch a valid token on submit and then appends it to the form.
  * The \`[FormCsrfHandler plugin](https://github.com/shopware/platform/blob/v6.3.4.1/src/Storefront/Resources/app/storefront/src/plugin/forms/form-csrf-handler.plugin.js) is only needed for native form submits.
  * `POST` requests made with the `http-client.service` are automatically protected when `csrf` mode is set to `ajax`

CSRF protection can be configured via [Symfony configuration files](https://symfony.com/doc/current/configuration.html).

```yaml
// <platform root>/src/Storefront/Resources/config/packages/storefront.yaml
storefront:
    csrf:
        enabled: true   // true/false to turn protection on/off
        mode: twig      // Valid modes are `twig` or `ajax`
```

## Exclude controller action from CSRF checks

As previously said, each Storefront route is looking for a CSRF token by default. It is possible to exclude a controller `POST` action from CSRF checks in the route annotation:

```php
/**
 * @Route("/example/route", name="example.route", defaults={"csrf_protected"=false}, methods={"POST"})
*/
public function exampleAction() {}
```

::: danger
Be aware that this is not recommended and could create a security vulnerability!
:::

## Caching and CSRF

The default configuration for the `csrf` mode is `twig` and works fine with the shopware HTTP cache. If an external cache (e.g. varnish) is used, the mode needs to be `ajax`. A valid CSRF token is then fetched and appended before a `POST` request.

---

---

## Working with Media and Thumbnails
**Source:** [guides/plugins/plugins/storefront/use-media-thumbnails.md](https://developer.shopware.com/docs/v6.6/guides/plugins/plugins/storefront/use-media-thumbnails.md)  
# Working with Media and Thumbnails

## Overview

In Shopware's Storefront, you can assign media objects to the different entities. To name an example, this is often used for products to show more information with images on the product detail page. This guide should give you a starting point on how to use media and thumbnails in your Storefront plugin.

## Prerequisites

In order to use your own media files or thumbnails of your plugin in the Storefront, of course you first need a plugin as base. To create an own plugin, you can refer to the Plugin Base Guide:

Displaying custom images is often done by using custom fields. To take full advantage of this guide, you might want to read the corresponding guide on using custom fields:

## Using searchMedia function

You should be able to store media in your shop and to maintain them in your Administration. It is not possible to display such an image in the Storefront with only its media ID though. To achieve that, the function `searchMedia` exists:

```php
public function searchMedia (array $ids, Context $context): MediaCollection { 
... 
}
```

This `searchMedia` function reads out the corresponding media objects for the given IDs in order to continue working with them afterwards. Here is an example with a custom field (`custom_sports_media_id`) on the product detail page:

```twig
{% sw_extends '@Storefront/storefront/page/product-detail/index.html.twig' %}

{% block page_product_detail_media %}
    {# simplify ID access #}
    {% set sportsMediaId = page.product.translated.customFields.custom_sports_media_id %}

    {# fetch media as batch - optimized for performance #}
    {% set mediaCollection = searchMedia([sportsMediaId], context.context) %}

    {# extract single media object #}
    {% set sportsMedia = mediaCollection.get(sportsMediaId) %}

    {{ dump (sportsMedia) }}
{% endblock %}
```

::: danger
Please note that this function performs a query against the database and should therefore not be used within a loop.
:::

The function is already structured in a way that several IDs can be passed. To read the media objects within the product listing we recommend the following procedure:

```twig
{% sw_extends '@Storefront/storefront/component/product/listing.html.twig' %}

{% block element_product_listing_col %}
    {# initial ID array #}
    {% set sportsMediaIds = [] %}

    {% for product in searchResult %}
        {# simplify ID access #}
        {% set sportsMediaId = product.translated.customFields.custom_sports_media_id %}

        {# merge IDs to a single array #}
        {% set sportsMediaIds = sportsMediaIds|merge([sportsMediaId]) %}
    {% endfor %}

    {# do a single fetch from database #}
    {% set mediaCollection = searchMedia(sportsMediaIds, context.context) %}

    {% for product in searchResult %}
        {# simplify ID access #}
        {% set sportsMediaId = product.translated.customFields.custom_sports_media_id %}

        {# get access to media of product #}
        {% set sportsMedia = mediaCollection.get(sportsMediaId) %}

        {{ dump(sportsMedia) }}
    {% endfor %}
{% endblock %}
```

## Working with sw\_thumbnail

A common issue when developing responsive web pages is resizing images properly for different screen widths. By default, Shopware generates various thumbnails for each uploaded image. Normally you would have to manually write large chunks of HTML code to render the needed images with `img` and `srcset`.

Fortunately, you do not need to define these attributes on your own - For that, Shopware introduced the `sw_thumbnails` Twig function: `sw_thumbnails` automatically generates the `img` and `srcset` code. This is the minimal configuration:

```twig
{% sw_thumbnails 'my-thumbnails' with {
    media: cover
} %}
```

As you see, `sw_thumbnail` makes use of one required parameter: `media` is required and contains the whole media entity. The string after `sw_thumbnails` is also required but does not render a CSS class. All other parameters are optional.

### Dealing with thumbnail sizes

With the `sizes` parameter you can control the `sizes` attribute of the `img` and define which of the thumbnails should be used in a media query / viewport.

You can find more information on those sizes here:

E.g. if the browser is in Bootstrap viewport `lg` (which is 992px - 1199px) use an image which is closest to 333px. If `sizes` is not set, Shopware will automatically use fallback values from global `shopware.theme.breakpoint`.

Let's think about the snippet below:

```twig
{% sw_thumbnails 'my-thumbnails' with {
    media: cover,
    sizes: {
        'xs': '501px',
        'sm': '315px',
        'md': '427px',
        'lg': '333px',
        'xl': '284px',
    }
} %}
```

This example will print out the following output:

```html
<img 
    src="http://shopware.local/media/06/f0/5c/1614258798/example-image.jpg" 
    srcset="http://shopware.local/media/06/f0/5c/1614258798/example-image.jpg 1921w, 
            http://shopware.local/thumbnail/06/f0/5c/1614258798/example-image_1920x1920.jpg 1920w, 
            http://shopware.local/thumbnail/06/f0/5c/1614258798/example-image_800x800.jpg 800w, 
            http://shopware.local/thumbnail/06/f0/5c/1614258798/example-image_400x400.jpg 400w" 
    sizes="(max-width: 1920px) and (min-width: 1200px) 284px,
           (max-width: 1199px) and (min-width: 992px) 333px, 
           (max-width: 991px) and (min-width: 768px) 427px, 
           (max-width: 767px) and (min-width: 576px) 315px, 
           (max-width: 575px) and (min-width: 0px) 501px, 100vw">
```

By giving the `default` size you can override the media queries and always refer to a single image source for all viewports. To give an example, think about always using a small thumbnail closest to 100px regardless of the current viewport:

```twig
{% sw_thumbnails 'my-thumbnails' with {
    media: cover,
    sizes: {
        'xs': '501px', {# Will be ignored #}
        'sm': '315px', {# Will be ignored #}
        'md': '427px', {# Will be ignored #}
        'lg': '333px', {# Will be ignored #}
        'xl': '284px', {# Will be ignored #}
        'default': '100px'
    }
} %}
```

This example will create the output below:

```html
<img 
    src="http://shopware.local/media/06/f0/5c/1614258798/example-image.jpg" 
    srcset="http://shopware.local/media/06/f0/5c/1614258798/example-image.jpg 1921w, 
            http://shopware.local/thumbnail/06/f0/5c/1614258798/example-image_1920x1920.jpg 1920w, 
            http://shopware.local/thumbnail/06/f0/5c/1614258798/example-image_800x800.jpg 800w, 
            http://shopware.local/thumbnail/06/f0/5c/1614258798/example-image_400x400.jpg 400w" 
    sizes="100px">
```

::: danger
Please note that those sizes only work with bootstrap viewports, like xs, sm, md, lg and xl. Custom media queries will not work.
:::

### Additional attributes

With the `attributes` param, additional attributes can be applied. Imagine the following example:

```twig
{% sw_thumbnails 'my-thumbnails' with {
    media: cover,
    attributes: {
        'class': 'my-custom-class',
        'alt': 'alt tag of image',
        'title': 'title of image'
    }
} %}
```

This will generate the output below:

```html
<img 
    src="..." 
    sizes="..." 
    class="my-custom-class" 
    alt="Image name" 
    title="My beautiful image">
```

### Native lazy loading

With the `attributes` param, it is also possible to enable native lazy loading on the thumbnail element:

```twig
{% sw_thumbnails 'my-thumbnails' with {
    media: cover,
    attributes: {
        'loading': 'lazy'
    }
} %}
```

This will generate the below output:

```html
<img 
    src="..." 
    sizes="..." 
    loading="lazy">
```

By default, lazy loading is disabled for newly added `sw_thumbnail` elements. You should consider activating it in the following scenarios:

* When multiple `sw_thumbnail` elements occur on one page while the `sw_thumbnail` s are not in the initial viewport.
* When images rendered by `sw_thumbnail` are within a container hidden by CSS via `display: none`.

## More interesting topics

* [Use custom assets in general](add-custom-assets)

---

---

## Use Nested Line Items
**Source:** [guides/plugins/plugins/storefront/use-nested-line-items.md](https://developer.shopware.com/docs/v6.6/guides/plugins/plugins/storefront/use-nested-line-items.md)  
# Use Nested Line Items

## Overview

This guide will show you how to use the nested line items in the Storefront.

## Prerequisites

As most guides, this guide is also built upon the [Plugin base guide](../plugin-base-guide), but you don't necessarily need that. This guide will only extend views and shows how the Custom Product plugin handles this.

## Make nested line item removable

If the nested line item should be removable in the cart, the `removable` property has to be set, either via view, or in an own controller action. Also, a form with an own path action has to be added:

```twig
{% block page_checkout_item_remove_icon %}
    {% do nestedLineItem.setRemovable(true) %}
    <form action="{{ path('/mycontroller/nested/remove', { 'id': nestedLineItem.id }) }}" method="post">
        {{ parent() }}
    </form>
{% endblock %}
```

## Make nested line item changeable

Most of the time, the root line item defines the nested line items, therefore there is a change button for its root line item in the cart.
In the block of the change button, the variable `isChangeable` has to be set, and the button has to be surrounded with a link to the action like this:

```twig
{% block component_offcanvas_item_children_header_content_change_button %}
    {% set isChangeable = true %}
    {% set seo = seoUrl('frontend.detail.page', {
            'productId': lineItem.children.first.referencedId,
            'swagCustomizedProductsConfigurationEdit': lineItem.extensions.customizedProductConfiguration.id
        })
    %}
    
    <a href="{{ seo }}" class="order-item-product-name" title="{{ label }}">
        {{ parent() }}
    </a>
{% endblock %}
```

## About extended functionality

Please notice: Nested line items can be implemented in various ways, so there's no telling what a **default handling** could be. Therefore, it is necessary to implement a change or remove handling by yourself.

---

---

## Using a Modal Window
**Source:** [guides/plugins/plugins/storefront/using-a-modal-window.md](https://developer.shopware.com/docs/v6.6/guides/plugins/plugins/storefront/using-a-modal-window.md)  
*(Body truncated in this bundle; follow the link for the rest.)*

# Using a Modal Window

## Overview

This guide explains how you can use a modal window in your plugin in different scenarios.

## Prerequisites

This guide requires you to already have a basic plugin running. This guide **does not** explain how to create a new plugin for Shopware 6. Head over to our Plugin base guide to learn how to create a plugin at first:

While this is not mandatory, having read the guide about adding custom JavaScript plugins beforehand might help you understand this guide a bit further:

## Create a modal manually from the DOM using Bootstrap

The simples solution to create a modal is by using Bootstrap. More info: [Modal Bootstrap](https://getbootstrap.com/docs/5.3/components/modal/#live-demo)
Here is a basic implementation as an example. We override the `base_main_inner` from the `@Storefront/storefront/page/content/index.html.twig` template to insert the modal specific DOM elements.

```twig
// <plugin root>/src/Resources/views/storefront/page/content/index.html.twig
{% sw_extends '@Storefront/storefront/page/content/index.html.twig' %}

{% block base_main_inner %}
    <!-- Button trigger modal -->
    <button type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#exampleModal">
        Launch demo modal
    </button>

    <!-- Modal -->
    <div class="modal fade" id="exampleModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title" id="exampleModalLabel">Modal title</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <!-- insert your content here -->
                    ...
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                    <button type="button" class="btn btn-primary">Save changes</button>
                </div>
            </div>
        </div>
    </div>

    {{ parent() }}
{% endblock %}
```

## Create a modal using AjaxModalPlugin

When setting `data-ajax-modal="true"` together with `data-url` shopware automatically uses the `PseudoModalUtil` and the pseudo modal template from the `base.html.twig` to render a modal:

```twig
// <plugin root>/src/Resources/views/storefront/page/content/index.html.twig
{% sw_extends '@Storefront/storefront/page/content/index.html.twig' %}

{% block base_main_inner %}
    <!-- This uses `AjaxModalPlugin` -->
    <button class="btn btn-primary"
            data-ajax-modal="true"
            data-url="https://example.org/ajax-url">
        Launch ajax modal
    </button>
    {{ parent() }}
{% endblock %}
```

::: warning
This does not work when the trigger selector is being changed via JavaScript, e.g. because of an AJAX call which replaces the content.
:::

## Advanced / manual using Pseudo Modal Utility

To create a modal window you can use the `PseudoModalUtil` in your plugin.

As explained in the guide on [adding custom javascript](./add-custom-javascript) we load our JavaScript plugin by creating `index.html.twig` template in the `<plugin root>/src/Resources/views/storefront/page/content/` folder.
Inside this template, extend from the `@Storefront/storefront/page/content/index.html.twig` and overwrite the `base_main_inner` block. After the parent content of the blog, add a template tag with the `data-example-plugin` attribute.

```twig
// <plugin root>/src/Resources/views/storefront/page/content/index.html.twig
{% sw_extends '@Storefront/storefront/page/content/index.html.twig' %}

{% block base_main_inner %}
    {{ parent() }}

    <template data-example-plugin></template>
{% endblock %}
```

Now we need to register the plugin which should create a modal in the `PluginManager`. To achieve this you can add the following code to the `main.js` file.

```javascript
// <plugin root>/src/Resources/app/storefront/src/main.js
 // Import all necessary Storefront plugins
 import ExamplePlugin from './example-plugin/example-plugin.plugin';

 // Register your plugin via the existing PluginManager
 const PluginManager = window.PluginManager;
 PluginManager.register('ExamplePlugin', ExamplePlugin, '[data-example-plugin]');
```

Now let's get started with the modal window. First we have to import the `PseudoModalUtil` class in our plugin.

```javascript
// <plugin root>/src/Resources/app/storefront/src/example-plugin/example-plugin.plugin.js
const { PluginBaseClass } = window;
import PseudoModalUtil from 'src/utility/modal-extension/pseudo-modal.util';

export default class ExamplePlugin extends PluginBaseClass {
    init() {
        // ...
    }
}
```

Now we create a new modal instance using `new PseudoModalUtil()` and assign to a property of our plugin for later usage.
We also call the method `open()` to make it visible.

```javascript
// <plugin root>/src/Resources/app/storefront/src/example-plugin/example-plugin.plugin.js
const { PluginBaseClass } = window;
import PseudoModalUtil from 'src/utility/modal-extension/pseudo-modal.util';

export default class ExamplePlugin extends PluginBaseClass {
    init() {
        this.openModal();
    }
    
    openModal() {
        // create a new modal instance
        this.modal = new PseudoModalUtil();
        
        // open the modal window and make it visible
        this.modal.open();
    }
}
```

To see your changes you have to build the storefront. Use the following command to build your storefront and reload it afterwards:

```bash
./bin/build-storefront.sh
```

```bash
composer run build:js:storefront
```

You can now see a blank modal which contains `undefined`. This is because we have not added any content to show inside the modal.

The constructor method of `PseudoModalUtil()` expects some HTML `content` to display. To keep this guide simple, we are only including sample code here.
Of course, the content can also be generated via an API and inserted via AJAX requests.

```javascript
// <plugin root>/src/Resources/app/storefront/src/example-plugin/example-plugin.plugin.js
const { PluginBaseClass } = window;
import PseudoModalUtil from 'src/utility/modal-extension/pseudo-modal.util';

export default class ExamplePlugin extends PluginBaseClass {
    init() {
        // declaring some basic content
        const content = `
            <div class="js-pseudo-modal-template">
                <div class="js-pseudo-modal-template-title-element">Modal title</div>
                <div class="js-pseudo-modal-template-content-element">Modal content</div>
            </div>
        `;
        
        this.openModal(content);
    }
    
    openModal(content) {
        // create a new modal instance
        this.modal = new PseudoModalUtil(content);
        
        // open the modal window and make it visible
        this.modal.open();
    }
}
```

## Closing the modal

The `PseudoModalUtil` class also provide a `close()` method. Same as with opening the modal by calling `this.modal.open()`, you can simply close the modal with `this.modal.close()`.

## Callback when opening a modal

The `open()` method of the `PseudoModalUtil` class supports a callback function as an argument. So if you need to perform some action when your modal opens, you can implement a callback like this:

```javascript
// <plugin root>/src/Resources/app/storefront/src/example-plugin/example-plugin.plugin.js
const { PluginBaseClass } = window;
import PseudoModalUtil from 'src/utility/modal-extension/pseudo-modal.util';

export default class ExamplePlugin extends PluginBaseClass {
    init() {
        // declaring some basic content
        const content = `
            <div class="js-pseudo-modal-template">
                <div class="js-pseudo-modal-template-title-element">Modal title</div>
                <div class="js-pseudo-modal-template-content-element">Modal content</div>
            </div>
        `;
        
        this.openModal(content);
    }
    
    openModal(content) {
        // create a new modal instance
        this.modal = new PseudoModalUtil(content);
        
        // open the modal window and fire a callback function
        this.modal.open(this.onOpenModal.bind(this));
    }
    
    onOpenModal() {
        console.log('the modal is opened');
    }
}
```

## Updating the modal content

To update the content of a modal, `PseudoModalUtil` provides a method `updateContent()` to which you can pass the updated template string. The method also accepts a callback function as a second argument, which is called after the content has been updated.
Here is an example how to use it:

```javascript
// <plugin root>/src/Resources/app/storefront/src/example-plugin/example-plugin.plugin.js
const { PluginBaseClass } = window;
import PseudoModalUtil from 'src/utility/modal-extension/pseudo-modal.util';

export default class ExamplePlugin extends PluginBaseClass {
    init() {
        // declaring some basic content
        const content = `
            <div class="js-pseudo-modal-template">
                <div class="js-pseudo-modal-template-title-element">Modal title</div>
                <div class="js-pseudo-modal-template-content-element">Modal content</div>
            </div>
        `;
        
        this.openModal(content);
        
        // ... do some stuff

        const updatedContent = `
            <div class="js-pseudo-modal-template">
                <div class="js-pseudo-modal-template-title-element">Modal title</div>
                <div class="js-pseudo-modal-template-content-element">Updated content</div>
            </div>
        `;
        
        this.modal.updateModal(updatedContent, this.onUpdateModal.bind(this));
    }
    
    openModal(content) {
        // create a new modal instance
        this.modal = new PseudoModalUtil(content);
        
        // open the modal window and fire a callback function
        this.modal.open(this.onOpenModal.bind(this));
    }
    
    onOpenModal() {
        console.log('the modal is opened');
    }

    onUpdateModal() {
        console.log('the modal was updated');
    }
    
}
```

## Customize the modal appearance

The constructor method of `PseudoModalUtil` provides optional configuration. If you don't need backdrop of the modal for example just turn it off by instantiating the modal like this

```javascript
// <plugin root>/src/Resources/app/storefront/src/example-plugin/example-plugin.plugin.js
const { PluginBaseClass } = window;
import PseudoModalUtil from 'src/utility/modal-extension/pseudo-modal.util';

export default class ExamplePlugin extends PluginBaseClass {
    init() {
        // declaring some basic content
        const content = `
            <div class="js-pseudo-modal-template">
                <div class="js-pseudo-modal-template-title-element">Modal title</div>
                <div class="js-pseudo-modal-template-content-element">Modal content</div>
            </div>
        `;
        
        this.openModal(content);
    }
    
    openModal(content) {
        // disable backdrop
        const useBackrop = false;
        
        // create a new modal instance
        this.modal = new PseudoModalUtil(content, useBackrop);
        
        // open the modal window and make it visible
        this.modal.open();
    }
}
```

As you can see in the sample code, we are using the `js-pseudo-modal-template-title-element` class to style the title text of the modal.
It also tells the `PseudoModalUtil` class that the content of the `div` holds the title text.
Furthermore there are two more css selectors `js-pseudo-modal-template` and `js-pseudo-modal-template-content-element` to define the structure of the template string.

If you want to customize your modal by using different style classes, you can do that by overridin

… **Truncated.** Full document: https://developer.shopware.com/docs/v6.6/guides/plugins/plugins/storefront/using-a-modal-window.md


---

## Add Custom Field in the Storefront
**Source:** [guides/plugins/plugins/storefront/using-custom-fields-storefront.md](https://developer.shopware.com/docs/v6.6/guides/plugins/plugins/storefront/using-custom-fields-storefront.md)  
# Add Custom Field in the Storefront

## Overview

This guide will show you how to use custom fields, e.g., labels in the Storefront.

## Prerequisites

You won't learn to create a plugin in this guide, head over to our [Plugin base guide](../plugin-base-guide) to create a plugin first, if you don't know how it's done yet.

Needless to say, you need a custom field itself to add to the Storefront via your own plugin. Head over to the guide on [adding custom fields to Shopware](../framework/custom-field/add-custom-field) to be able to prepare your own custom field.

## Use snippets of custom fields

First, if you add a custom field via API or Administration, automatically snippets for all languages are created. The naming of the snippet is like the following template: `customFields.` as prefix and then the name of the custom field. For example, if the name of the created custom field is `my_test_field`, then the created snippet name will be `customFields.my_test_field`.

::: info
In the snippet settings in the Administration you're able to edit and translate the snippet.
:::

## Storefront usage of custom fields

Adding custom fields in the Storefront is quite simple. You basically use Twig this way:

```twig
{{ "customFields.my_test_field"|trans|sw_sanitize }}: {{ page.product.translated.customFields.my_test_field }}
```

::: info
Did you notice the Twig function `sw_sanitize`? It's a Twig function we wrote, customized for Shopware's needs. It filters tags and attributes from a given string optimized for Shopware usage.
:::

Imagine you want to add a text field to the product description. If you want to use the snippet in the Storefront, you have to extend a template file first. Let's say we want to add our custom field to the product description's text. The block of this element is `page_product_detail_description_content_text`, so we'll use it in our example. As we want to add our custom field in there, we use `parent` Twig function to keep the original template:

```twig
// <plugin root>/src/Resources/views/storefront/page/product-detail/description.html.twig
{% sw_extends '@Storefront/storefront/page/product-detail/description.html.twig' %}

{% block page_product_detail_description_content_text %}
    {{ parent() }}
{% endblock %}
```

Now, we finally add our custom field as explained before:

```twig
// <plugin root>/src/Resources/views/storefront/page/product-detail/description.html.twig
{% sw_extends '@Storefront/storefront/page/product-detail/description.html.twig' %}

{% block page_product_detail_description_content_text %}
    {{ parent() }}

    {# Insert your custom field here, as seen below: #}
    {{ "customFields.my_test_field"|trans|sw_sanitize }}: {{ page.product.translated.customFields.my_test_field }}
{% endblock %}
```

## Custom fields in forms

Let's say you have a custom field for the customer entity through the administration; now, you want the customer to input data into it through a field in the customer register form. This can be done without the need for a subscriber or listener; simply add a field to the form using the correct custom field name.

```twig
// <plugin root>/src/Resources/views/storefront/component/address/address-personal.html.twig
{% sw_extends '@Storefront/storefront/component/address/address-personal.html.twig' %}

{% block component_address_personal_fields %}
    {{ parent() }}

	{# custom field #}
	<div class="form-group col-sm-6">
		<label class="form-label" for="customFields[custom_field_name]">
			{{ "customFields.custom_field_name"|trans|sw_sanitize}}*
		</label>
		<input type="text" class="form-control" name="customFields[custom_field_name]" value="{{context.customer.customFields['custom_field_name'] }}" id="customFields[custom_field_name]" required="required">
	</div>
{% endblock %}
```

---

---

## Using the Datepicker Plugin
**Source:** [guides/plugins/plugins/storefront/using-the-datepicker-plugin.md](https://developer.shopware.com/docs/v6.6/guides/plugins/plugins/storefront/using-the-datepicker-plugin.md)  
# Using the Datepicker Plugin

## Overview

To provide an input field for date and time values, you can use the datepicker plugin. This guide shows you how to use it.

The datepicker plugin uses the `flatpickr` implementation under the hood. So, check out the `flatpickr` documentation,
if you need more information about the date picker configuration itself.

## Prerequisites

You won't learn how to create a plugin in this guide, head over to our Plugin base guide to create
your first plugin:

You should also know how to customize templates:

## Setup a datepicker input field

To apply the datepicker functionality we have to add a DOM element in a template, e.g. an input field.
To keep this example simple for now we just override the `base_main_inner` block of the `storefront/page/content/index.html.twig` template.

```twig
// <plugin root>/src/Resources/views/storefront/page/content/index.html.twig
{% sw_extends '@Storefront/storefront/page/content/index.html.twig' %}

{% block base_main_inner %}
    <label>
        <input type="text"
               name="customDate"
               class="customDate"
        />
    </label>

    {{ parent() }}
{% endblock %}
```

Now you should see an empty input field if you open the storefront in your browser.
We need to add the data-attribute `data-date-picker` to activate the datepicker plugin on our input field.

```twig
// <plugin root>/src/Resources/views/storefront/page/content/index.html.twig
{% sw_extends '@Storefront/storefront/page/content/index.html.twig' %}

{% block base_main_inner %}
    <label>
        <input type="text"
               name="customDate"
               class="customDate"
               data-date-picker
        />
    </label>

    {{ parent() }}
{% endblock %}
```

If we check the change in the browser again, thus after reloading the page, we can see that the datepicker plugin is now active on this element.

## Configure the datepicker

If you select a date with the datepicker from the example above, you will see that a time is always selected and displayed in the input field. By default, the time selection is activated.

We can change this behaviour by passing more options to the datepicker plugin.

Here you can see how this is done by setting up a local Twig variable `pickerOptions`. We can assign a JSON formatted object to the variable and pass the value to the datepicker plugin through the `data-date-picker-options` attribute.

```twig
// <plugin root>/src/Resources/views/storefront/page/content/index.html.twig
{% sw_extends '@Storefront/storefront/page/content/index.html.twig' %}

{% block base_main_inner %}

    {% set pickerOptions = {
        locale: app.request.locale,
        enableTime: true
    } %}
    
    <label>
        <input type="text"
               name="customDate"
               class="customDate"
               data-date-picker
               data-date-picker-options="{{ pickerOptions|json_encode|escape('html_attr') }}"
        />
    </label>

    {{ parent() }}
{% endblock %}
```

As you can see, we also pass in the `locale` option which gets its value from `app.request.locale`. As a result,
the datepicker plugin now uses the same locale as the current storefront and the date formatting matches active
languages accordingly.

## Preselect a date

To preselect the value of the datepicker we can simply set its value in the input field which gets picked up by the datepicker plugin.

```twig
// <plugin root>/src/Resources/views/storefront/page/content/index.html.twig
{% sw_extends '@Storefront/storefront/page/content/index.html.twig' %}

{% block base_main_inner %}

    {% set pickerOptions = {
        locale: app.request.locale,
        enableTime: true
    } %}
    
    <label>
        <input type="text"
               name="customDate"
               class="customDate"
               value="2021-01-01T00:00:00+00:00"
               data-date-picker
               data-date-picker-options="{{ pickerOptions|json_encode|escape('html_attr') }}"
        />
    </label>

    {{ parent() }}
{% endblock %}
```

## Controlling the datepicker via buttons

To open or close the datepicker by trigger buttons you can pass in DOM selectors. You can also setup a selector to reset the currently selected value.
Here is an example which shows all three selectors in action.

```twig
// <plugin root>/src/Resources/views/storefront/page/content/index.html.twig
{% sw_extends '@Storefront/storefront/page/content/index.html.twig' %}

{% block base_main_inner %}

    {% set pickerProperties = {
        locale: app.request.locale,
        enableTime: true,
        selectors: {
            openButton: ".openDatePicker",
            closeButton: ".closeDatePicker",
            clearButton: ".resetDatePicker"
        }
    } %}

    <label>
        <input type="text"
               name="foo"
               class="customDate"
               value="2021-04-13T00:00:00+00:00"
               data-date-picker
               data-date-picker-options="{{ pickerProperties|json_encode|escape('html_attr') }}"
        />

        <button class="openDatePicker">Open</button>
        <button class="closeDatePicker">Close</button>
        <button class="resetDatePicker">Reset</button>
    </label>

    {{ parent() }}
{% endblock %}
```

## More options

| Option | Default | Description |
| :--- | :--- | :--- |
| `dateFormat` | 'Y-m-dTH:i:S+00:00' | Pattern for the date string representation
| `altInput` | true | Hides your original input and creates a new one.
| `altFormat` | 'j. FY, H:i' | Alternative pattern for the date string representation if `altInput` is enabled. The value of the input field gets still formatted by `dateFormat`
| `time_24hr` | true |
| `enableTime` | true |
| `noCalendar` |false |
| `weekNumbers` | true |
| `allowInput` | true |
| `minDate` | null | Specifies the minimum/earliest date (inclusively) allowed for selection
| `maxDate` | null | Specifies the maximum/latest date (inclusively) allowed for selection.

---

---

## guides/plugins/plugins/storefront/working-with-viewports-in-js.md
**Source:** [guides/plugins/plugins/storefront/working-with-viewports-in-js.md](https://developer.shopware.com/docs/v6.4/guides/plugins/plugins/storefront/working-with-viewports-in-js.md)  
---

---

## Themes
**Source:** [guides/plugins/themes.md](https://developer.shopware.com/docs/v6.6/guides/plugins/themes.md)  
# Themes

A Shopware theme plugin allows businesses to customize and modify the appearance and design of their online store. It provides the ability to change the layout, styling, and visual elements, such as fonts, colors, and images, to match your brand identity and desired user experience. Using a theme plugin, businesses can easily manage and apply their custom themes, switch between them, and ensure consistent branding across their store.

You will learn more about it in the upcoming section.

---

---

## Add Assets to a Theme
**Source:** [guides/plugins/themes/add-assets-to-theme.md](https://developer.shopware.com/docs/v6.6/guides/plugins/themes/add-assets-to-theme.md)  
# Add Assets to a Theme

## Overview

Your theme can include custom assets like images. This short guide will show you where to store your custom assets and how you can link them in Twig and SCSS.

## Prerequisites

This guide is built upon the guide on creating a first theme:

## Using custom assets

There are basically two ways of adding custom assets to your theme. The first one is using the `theme.json` to define the path to your custom assets, the second being the default way of using custom assets in plugins. We'll take a closer look at them in the following sections.

### Adding assets in theme.json file

While working with your own theme, you might have already come across the [Theme configuration](theme-configuration). In there, you have the possibility to configure your paths to your custom assets like images, fonts, etc. This way, please configure your asset path accordingly.

```javascript
// <plugin root>/src/Resources/theme.json
{
  ...
  "asset": [
     "app/storefront/src/assets"
   ]
  ...
}
```

Next, run the command `bin/console theme:compile`. The assets from the path defined in the `theme.json` file will be copied by the `theme:compile` command to `<shopware root>/public/theme/<theme-asset-uuid>` along with the compiled CSS and JS, which are stored in a separate folder.

```text
// <shopware root>/public
# 
.
└── theme
    ├── <theme-uuid>
    │   ├── css
    │   │   └── all.css
    │   └── js
    │       └── all.js
    └── <theme-asset-uuid>
        └── asset
            └── your-image.png <-- Your asset is copied here  
```

### Adding assets the plugin way

This way of adding custom assets refers to the default way of dealing with assets. For more details, please check out the article that specifically addresses this topic:

## Linking to assets

You can link to the asset with the twig [asset](https://symfony.com/doc/current/templates.html#linking-to-css-javascript-and-image-assets) function:

```html
<img src="{{ asset('/assets/your-image.png', 'theme') }}">
```

In SCSS, you can link to the asset like the following:

```css
body {
    background-image: url('#{$app-css-relative-asset-path}/your-image.png');
}
```

## Next steps

Now that you know how to use your assets in a theme, here is a list of other related topics where assets can be used.

* [Customize templates](../plugins/storefront/customize-templates)

---

---

## Add SCSS Styling and JavaScript to a Theme
**Source:** [guides/plugins/themes/add-css-js-to-theme.md](https://developer.shopware.com/docs/v6.6/guides/plugins/themes/add-css-js-to-theme.md)  
# Add SCSS Styling and JavaScript to a Theme

## Overview

This guide explains how you can add your custom styling via SCSS and add your custom JavaScript to your theme.

## Prerequisites

All you need for this guide is a running Shopware 6 instance and full access to both the files, as well as the command line. You also need to have an installed and activated theme which is assigned to a sales channel. Checkout the [Create a first theme](create-a-theme) guide if you have not yet a working theme setup.

## Adding custom SCSS

When it comes to CSS and SCSS, they are processed by a PHP SASS compiler.

The main entry point to deploy your SCSS code is defined in the `theme.json` file. By default it is the `<plugin root>/app/storefront/src/scss/base.scss` file.

```javascript
// <plugin root>/src/Resources/theme.json
 {
   ...
   "style": [
     "app/storefront/src/scss/overrides.scss",
     "@Storefront",
     "app/storefront/src/scss/base.scss"
   ],
   ...
 }
```

When the Storefront gets compiled the PHP SASS compiler will look up the files declared in the `style` section of the theme configuration. You can define the SCSS entrypoints individually if you want to.

In order to add some custom SCSS in your theme, you just need to edit the `base.scss` file which in located in `<plugin root>/src/Resources/app/storefront/src/scss` directory.

```bash
.
├── composer.json
└── src
    ├── Resources
    │   ├── app
    │   │   └── storefront
    │   │       └── src
    │   │           └── scss
    │   │               └── base.scss <-- SCSS entry
    └── SwagBasicExampleTheme.php
```

To apply your styles and test them, please use some test code:

```css
// <plugin root>/src/Resources/app/storefront/src/scss/base.scss
body {
    background-color: blue;
}
```

Afterwards, you need to compile your theme by running the `bin/console theme:compile` command in terminal.

After your theme was compiled successfully, go and check your changes by opening the Storefront in your browser.

## Adding custom JS

JavaScript cannot be compiled by PHP, so [webpack](https://webpack.js.org/) is being used for that. All Javascript in Shopware 6 is written in EcmaScript 6. Of course you can write your code in EcmaScript 5 as well.

By default your plugin is using Shopware's default webpack configuration, as you must ship your theme with the JavaScript already compiled.

Since Shopware knows where your style files are located, they are automatically compiled, compressed and loaded into the Storefront. In the case of JavaScript, you have your `main.js` as entry point which has to be located the `src/Resources/app/storefront/src/` directory:

```bash
.
├── composer.json
└── src
    ├── Resources
    │   ├── app
    │   │   └── storefront
    │   │       └── src
    │   │           └── main.js <-- JS entry
    └── SwagBasicExampleTheme.php
```

Add some test code in order to see if it works out:

```javascript
// <plugin root>/src/Resources/app/storefront/src/js/main.js
console.log('SwagBasicExampleTheme JS loaded');
```

In the end, by running the command `bin/build-storefront.sh` your custom JS plugin is loaded. By default, the compiled JavaScript file is saved as `<plugin root>/src/resources/app/storefront/dist/storefront/js/swag-basic-example-theme/swag-basic-example-theme.js`. It is detected by Shopware automatically and included in the Storefront. So you do not need to embed the JavaScript file yourself.

## Using the hot-proxy (live reload)

Of course, the theme compilation with `bin/console theme:compile` will get tedious if you change files a lot and want to check the changes in the browser. So there is a better way while you are developing your theme with the `hot-proxy` option, which will give you the live reload feature.

To activate the hot-proxy, run the following command in your terminal.

```bash
./bin/watch-storefront.sh
```

```bash
composer run watch:storefront
```

This command starts a NodeJS web server on port `9998`. If you open the Storefront of your Shopware installation on `localhost:9998`, this page will be automatically updated when you make changes to your theme.

## Next steps

Now that you know how to customize the styling via SCSS and add JavaScript, here is a list of things you can do.

* [Override Bootstrap variables in a theme](override-bootstrap-variables-in-a-theme)
* [Customize templates](../plugins/storefront/customize-templates)

---

---

## Add Custom Icons
**Source:** [guides/plugins/themes/add-icons.md](https://developer.shopware.com/docs/v6.6/guides/plugins/themes/add-icons.md)  
# Add Custom Icons

## Overview

In this guide, you will learn how to use the icon renderer component as well as adding custom icons.

::: info
Even if this is originally a plugin guide, everything will work perfectly in a theme as well. Actually, a theme even is a kind of plugin. So don't get confused by us talking about plugins here.
:::

## Prerequisites

To follow this guide easily, you first need to have a functioning plugin installed. Head over to our [Plugin base guide](../plugins/plugin-base-guide) to create a plugin, if you don't know how it's done yet. Also, knowing and understanding SCSS will be quite mandatory to fully understand what's going on here. Furthermore, it might be helpful to read the guide on how to [handle own assets](../plugins/storefront/add-custom-assets) in your plugin before you start with this one.

## Adding icon

To add any icons to the Storefront, you use our `sw_icon` twig action. This way, an icon of choice is displayed in the Storefront.

Needless to say, the first step is saving your image somewhere in your plugin where Shopware can find it. The default path for icons is the following:

```text
<YourPlugin>/src/Resources/app/storefront/dist/assets/icon/default
`
```

You can also provide "solid" icons or any other custom pack names that can be configured later with the `pack` parameter. You can do that by creating a folder with the pack name:

```text
<YourPlugin>/src/Resources/app/storefront/dist/assets/icon/<pack-name>
```

By default, Shopware looks inside the "default" folder.

```twig
{% sw_icon 'done-outline-24px' style {
    'namespace': 'TestPlugin'
} %}
```

::: info
When you want to see all icons available to the storefront by default, see [here](https://github.com/shopware/shopware/tree/trunk/src/Storefront/Resources/app/storefront/dist/assets/icon). They are available as `default` and `solid` icon pack.
:::

Imagine you want to use the default `checkmark` icon from the `solid` pack. In this case,

You surely want to add your own custom icons. In this case, the `namespace` parameter is the most important one to configure. In there, you need to set the name of the theme in which the icon is searched for by its name.

::: warning
If you configure no deviating namespace, Shopware will display the Storefront's default icons.
:::

However, these are not all of your possibilities of configuration. As you see, you're able to configure even more things. Let's take a look at the `style` object's possible parameters:

| Configuration | Description | Remarks |
| :--- | :--- | :--- |
| `size` | Sets the size of the icon | --- |
| `namespace` | Selection of the namespace of the icon, you can compare it with the source of it | Important configuration if you want to use custom icons. |
| `pack` | Selects the pack of different icons | --- |
| `color` | Sets the color of the icon | You can either use pre-defined variants similar to bootstrap (eg: primary , danger etc) or manually style the icon with any color with CSS. |
| `class` | Defines a class of the icon | --- |

A simple but fully functional example could look like below:

```twig
{% sw_extends '@Storefront/storefront/base.html.twig' %}

{% block base_body %}

    {# We want to set our own icon here #}
    <h1>Custom icon:</h1>
    {% sw_icon 'done-outline-24px' style {
        'size': 'lg',
        'namespace': 'TestPlugin',
        'pack': 'solid'
    } %}
    {{ parent() }}

{% endblock %}
```

::: danger
Icons or other custom assets are not included in the theme inheritance.
:::

Inside your theme, you cannot put an icon in a directory corresponding to the core folder structure and expect the core one to be automatically overwritten by it, as you're used to with themes in general.

## Load icons from custom locations

Since Shopware 6.4.1.0 it is possible to define custom locations of your custom icons inside your theme.json file.
You can define the name of the icon pack and the path to those icons under the `iconSets`-key:

```json
{
  /* ... */
  "iconSets": {
    "custom-icons": "app/storefront/src/assets/icon-pack/custom-icons"
  }
}
```

You can use your custom icons by specifying your icon pack:

```twig
{% sw_icon 'done-outline-24px' style {
    'pack': 'custom-icons'
} %}
```

::: warning
This setup is mandatory if you ship your Theme as an App, because otherwise your custom icons can't be loaded.
:::

---

---

## Theme with Bootstrap Styling
**Source:** [guides/plugins/themes/add-theme-inheritance-without-resources.md](https://developer.shopware.com/docs/v6.6/guides/plugins/themes/add-theme-inheritance-without-resources.md)  
# Theme with Bootstrap Styling

## Overview

The Shopware default theme is using [Bootstrap](https://getbootstrap.com/) with additional custom styling. But sometimes you want to develop a theme without the Shopware default styling.

## Theme without Shopware default styling

If you want to build your theme only upon the Bootstrap SCSS you can use the `@StorefrontBootstrap` placeholder instead of the `@Storefront` bundle in the `style` section of your `theme.json`. This gives you the ability to use the Bootstrap SCSS without the Shopware Storefront "skin". Therefore all the SCSS from `<plugin root>src/Storefront/Resources/app/storefront/src/scss/skin` will not be available in your theme.

```javascript
// <plugin root>/src/Resources/theme.json
{
  ...
  "style": [
    "@StorefrontBootstrap",
    "@Plugins",
    "app/storefront/src/scss/base.scss"
  ]
}
```

::: info

* This option can only be used in the `style` section of the `theme.json`. You must not use it in `views` or `script`.
* All theme variables like `$sw-color-brand-primary` are also available when using the Bootstrap option.
* You can only use either `@StorefrontBootstrap` or `@Storefront`. They should not be used at the same time. The `@Storefront` bundle **includes** the Bootstrap SCSS already.
* `@StorefrontBootstrap` does not include `@Plugins`, you have to add it yourself.
  :::

## Next steps

Here is a list of related topics which might be interesting for you.

* [Theme configuration](theme-configuration)
* [Add SCSS Styling and JavaScript to a theme](add-css-js-to-theme)
* [Add assets to theme](add-assets-to-theme)

---

---

## Theme Inheritance
**Source:** [guides/plugins/themes/add-theme-inheritance.md](https://developer.shopware.com/docs/v6.6/guides/plugins/themes/add-theme-inheritance.md)  
# Theme Inheritance

## Overview

This guide explains how you can extend an existing theme. What are use cases to inherit from another theme? Maybe you already use a specific theme for a sales channel and you want to use it in another sales channel for a different project with slight changes.

For example, imagine you want to use a dark version of the theme, so you have different looks for different sales channels. Or maybe you own a store-bought theme and only need to change the appearance of it without changing the code of the theme itself. Sometimes it could be useful to develop some kind of base theme and customize it for different clients.

## Prerequisites

All you need for this guide is a running Shopware 6 instance and full access to both the files, as well as the command line. You also need to have an installed and activated theme which you want to extend. Let's imagine we already have an installed and activated theme called `SwagBasicExampleTheme`.

## Extending an existing theme with a new theme

The first step is to create a new theme which will extend the existing `SwagBasicExampleTheme`. Checkout the [Create a first theme](create-a-theme) guide if you don't know how to create a new theme. In this guide we call the extending theme `SwagBasicExampleThemeExtend`. After `SwagBasicExampleTheme` was installed, activated and assigned to a sales channel we need to set up the inheritance.

## Set up the inheritance

To set up the inheritance we need to edit the theme configuration file called `theme.json` and it is located in the `<plugin root>/src/Resources` folder.

The content of the `theme.json` file looks like this:

```javascript
// <plugin root>/src/Resources/theme.json
{
  "name": "SwagBasicExampleThemeExtend",
  "author": "Shopware AG",
  "views": [
     "@Storefront",
     "@Plugins",
     "@SwagBasicExampleThemeExtend"
  ],
  "style": [
    "app/storefront/src/scss/overrides.scss",
    "@Storefront",
    "app/storefront/src/scss/base.scss"
  ],
  "script": [
    "@Storefront",
    "app/storefront/dist/storefront/js/swag-example-plugin-theme-extended/swag-example-plugin-theme-extended.js"
  ],
  "asset": [
    "@Storefront",
    "app/storefront/src/assets"
  ]
}
```

As you can see each section `views`, `style`, `script` and `asset` contains the `@Storefront` placeholder. This means that inheritance is already taking place here. Every theme inherits the default theme of Shopware called `@Storefront`.

Now it is easy to see how we can inherit from our base theme `SwagBasicExampleTheme`. We just need to add it in the inheritance chain.

Here is an example:

```javascript
// <plugin root>/src/Resources/theme.json
{
  "name": "SwagBasicExampleThemeExtend",
  "author": "Shopware AG",
  "views": [
     "@Storefront",
     "@Plugins",
     "@SwagBasicExampleTheme",
     "@SwagBasicExampleThemeExtend"
  ],
  "style": [
    "app/storefront/src/scss/overrides.scss",
    "@SwagBasicExampleTheme",
    "app/storefront/src/scss/base.scss"
  ],
  "script": [
    "@Storefront",
    "@SwagBasicExampleTheme",
    "app/storefront/dist/storefront/js/swag-example-plugin-theme-extended/swag-example-plugin-theme-extended.js"
  ],
  "asset": [
    "@Storefront",
    "@SwagBasicExampleTheme",
    "app/storefront/src/assets"
  ],
  "configInheritance": [
    "@Storefront",
    "@SwagBasicExampleTheme"
  ]
}
```

Let's walk over each section and have a closer look.

### `views` section

In the `views` section we added the placeholder `@SwagBasicExampleTheme` right before our current theme. This means that when a view gets rendered, the Storefront template is first used as the basis. The extensions of the installed plugins are applied to this. Next, the changes to the `@SwagBasicExampleTheme` theme are taken into account in the rendering process. Finally, the changes to our current theme are applied.

### `script` section

The same applies to the JavaScript `script` section. The javascript of the Storefront serves as the basis. On top of this come the extensions of the theme `@SwagBasicExampleTheme`. Finally, the JavaScript that we can implement in the current theme is applied.

### `style` section

The `style` section behaves similarly to the others. The only difference here is the `override.css` can affect SCSS variables e.g. `$border-radius`. That's why it's at the top of the list. To find out more about overriding variables check out the [Override Bootstrap variables in a theme](override-bootstrap-variables-in-a-theme) guide.

### `asset` section

If you want to use assets from the `@SwagBasicExampleTheme` you have add it to the list here as well.

### `configInheritance` section

Finally, the `configInheritance` section will use the field configuration from the given themes and defines the last of the themes, that is different from the current theme, as the parent theme. The configuration values are inherited from the themes mentioned in `configInheritance`. The Storefront theme configuration will always be inherited, even if no `configInheritance` is given. See [Theme inheritance configuration](theme-inheritance-configuration) for a more detailed example.

## Next steps

Now that you know how the theme inheritance works you can start with own customizations. Here is a list of other related topics where assets can be used.

* [Add SCSS Styling and JavaScript to a theme](add-css-js-to-theme)
* [Customize templates](../plugins/storefront/customize-templates)

---

---

## Create a First Theme
**Source:** [guides/plugins/themes/create-a-theme.md](https://developer.shopware.com/docs/v6.6/guides/plugins/themes/create-a-theme.md)  
# Create a First Theme

## Overview

This guide will show you how to create a theme from scratch. You will also learn how to install and activate your theme.

## Prerequisites

All you need for this guide is a running Shopware 6 instance and full access to both the files, as well as the command line.

## Create your first plugin theme

Let's get started with creating your plugin by finding a proper name for it.

### Name your plugin theme

First, you need to find a name for your theme. We're talking about a technical name here, so it needs to describe your theme appearance as short as possible, written in UpperCamelCase. To prevent issues with duplicated theme names, you should add a shorthand prefix for your company.\
Shopware uses "Swag" as a prefix for that case.\
For this example guide we'll use the theme name **SwagBasicExampleTheme.**

::: info
Notice: The name of a theme must begin with a capital letter too!
:::

### Create a plugin-based theme

Now that you've found your name, it's time to actually create your plugin.

Open your terminal and run the following command to create a new theme

```bash
bin/console theme:create SwagBasicExampleTheme

# you should get an output like this:

Creating theme structure under .../development/custom/plugins/SwagBasicExampleTheme
```

After your theme was created successfully Shopware has to know that it now exists. You have to refresh the plugin list by running the following command.

```bash
bin/console plugin:refresh

# you should get an output like this

[OK] Plugin list refreshed                                                                              

Shopware Plugin Service
=======================

 ----------------------- ------------------------------------ ------------- ----------------- -------- ----------- -------- ------------- 
  Plugin                  Label                                Version       Upgrade version   Author   Installed   Active   Upgradeable  
 ----------------------- ------------------------------------ ------------- ----------------- -------- ----------- -------- ------------- 
  SwagBasicExampleTheme   Theme SwagBasicExampleTheme plugin   9999999-dev                              No          No       No           
 ----------------------- ------------------------------------ ------------- ----------------- -------- ----------- -------- ------------- 

 1 plugins, 0 installed, 0 active , 0 upgradeable
```

Now Shopware recognises your plugin theme. The next step is the installation and activation of your theme. Run the following command in terminal.

```bash
# run this command to install and activate your plugin
bin/console plugin:install --activate SwagBasicExampleTheme

Shopware Plugin Lifecycle Service
=================================

 Install 1 plugin(s):
 * Theme SwagBasicExampleTheme plugin (vdev-trunk)

 Plugin "SwagBasicExampleTheme" has been installed and activated successfully.

 [OK] Installed 1 plugin(s).
```

Your theme was successfully installed and activated.

The last thing we need to do to work with the theme is to assign it to a sales channel. You can do that by running the `theme:change` command in the terminal and follow the instructions.

```bash
# run this to change the current Storefront theme
$ bin/console theme:change

# you will get an interactive prompt to change the 
# current theme of the Storefront like this

Please select a sales channel:
[0] Storefront | 64bbbe810d824c339a6c191779b2c205
[1] Headless | 98432def39fc4624b33213a56b8c944d
> 0

Please select a theme:
[0] Storefront
[1] SwagBasicExampleTheme
> 1

Set "SwagBasicExampleTheme" as new theme for sales channel "Storefront"
Compiling theme 13e0a4a46af547479b1347617926995b for sales channel SwagBasicExampleTheme
```

At first, we have to select a sales channel. The obvious choice here is the 'Storefront'. Afterwards enter the number for our theme.

Now your theme is fully installed, and you can start your customization.

### Directory structure of a theme

```bash
# structure of a plugin-based theme
├── composer.json
└── src
    ├── Resources
    │   ├── app
    │   │   └── storefront
    │   │       ├── dist
    │   │       │   └── storefront
    │   │       │       └── js
    |   |       |           └── swag-basic-example-theme  
    │   │       │               └── swag-basic-example-theme.js
    │   │       └── src
    │   │           ├── assets
    │   │           ├── main.js
    │   │           └── scss
    │   │               ├── base.scss
    │   │               └── overrides.scss
    │   └── theme.json
    └── SwagBasicExampleTheme.php
```

## Next steps

Now that you have created your own theme, the next step is to learn how to make settings and adjustments.

* [Theme configuration](theme-configuration)
* [Add SCSS Styling and JavaScript to a theme](add-css-js-to-theme)
* [Add assets to theme](add-assets-to-theme)

---

---

## Differences Plugins and Apps vs Themes
**Source:** [guides/plugins/themes/differences-plugins-and-apps-vs-themes.md](https://developer.shopware.com/docs/v6.6/guides/plugins/themes/differences-plugins-and-apps-vs-themes.md)  
# Differences Plugins and Apps vs Themes

A theme is a special type of Plugin or App, aimed at easily changing the visual appearance of the Storefront. If you want to get more information about plugins and apps you can check out the [Plugin Base Guide](../plugins/plugin-base-guide) and [App Base Guide](../apps/app-base-guide).

There are basically several ways to change the appearance of the Storefront. You can have "regular" plugins or apps whose main purpose is to add new functions and change the behavior of the shop. These plugins / apps might also contain SCSS/CSS and JavaScript to be able to embed their new features into the Storefront.

Technically, a theme is also a plugin / app, but it will be visible in the theme manger once it's activated and can be assigned to a specific sales channel, while plugins / apps are activated globally. To distinguish a theme from a "regular" plugin / app you need to implement the Interface `Shopware\Storefront\Framework\ThemeInterface`. A theme can inherit also from other themes, overwrite the default configuration (colors, fonts, media) and add new configuration options.

You do not need to write any PHP code in a theme. If you need PHP code, you should choose a plugin instead. Another important distinction to themes is this: Themes are specific for a sales channel and have to be assigned to them to take effect, the other way around plugins and apps have a global effect on the Shopware installation.

## Next steps

Now that you have learned the differences between themes, plugins and apps, you can create your first theme.

* [Create a first Shopware theme](create-a-theme)

---

---

## Override Bootstrap Variables in a Theme
**Source:** [guides/plugins/themes/override-bootstrap-variables-in-a-theme.md](https://developer.shopware.com/docs/v6.6/guides/plugins/themes/override-bootstrap-variables-in-a-theme.md)  
# Override Bootstrap Variables in a Theme

## Overview

The storefront theme is implemented as a skin on top of Bootstrap:

Sometimes it is necessary to adjust SCSS variables if you want to change the look of the Storefront for example default variables like `$border-radius` which is defined by Bootstrap. This guide will show how you can override those SCSS variables.

## Prerequisites

All you need for this guide is a running Shopware 6 instance and full access to both the files, as well as the command line. You also need to have an installed and activated theme which is assigned to a sales channel. Checkout the [Create a first theme](create-a-theme) guide if you have not yet a working theme setup.

## Override default SCSS variables

Bootstrap 4 is using the `!default` flag for it's own default variables. Variable overrides have to be declared beforehand.

More information can be found [here](https://getbootstrap.com/docs/4.0/getting-started/theming/#variable-defaults).

To be able to override Bootstrap variables there is an additional SCSS entry point defined in your `theme.json` which is declared before `@Storefront`.

This entry point is called `overrides.scss`:

```javascript
// <plugin root>/src/Resources/theme.json
{
  "name": "SwagBasicExampleTheme",
  "author": "Shopware AG",
  "views": [
        "@Storefront",
        "@Plugins"
  ],
  "style": [
    "app/storefront/src/scss/overrides.scss", <-- Variable overrides
    "@Storefront",
    "app/storefront/src/scss/base.scss"
  ],
  "script": [
    "@Storefront",
    "app/storefront/dist/storefront/js/just-another-theme/just-another-theme.js"
  ],
  "asset": [
    "@Storefront",
    "app/storefront/src/assets"
  ]
}
```

In the `<plugin root>/src/Resources/app/storefront/src/scss/overrides.scss` you can now override default variables like `$border-radius` globally and set its value to `0` to reset it in this case:

```css
// <plugin root>/src/Resources/app/storefront/src/scss/overrides.scss
/*
Override variable defaults
==================================================
This file is used to override default SCSS variables from the Shopware Storefront or Bootstrap.

Because of the !default flags, theme variable overrides have to be declared beforehand.
https://getbootstrap.com/docs/4.0/getting-started/theming/#variable-defaults
*/

$border-radius: 0;

// some other override examples
$icon-base-color: #f00;
$modal-backdrop-bg: rgba(255, 0, 0, 0.5);
$disabled-btn-bg: #f00;
$disabled-btn-border-color: #fc8;
$font-weight-semibold: 300;
```

After saving the `overrides.scss` file and running `bin/console theme:compile` go and check out the Storefront in the browser. The `border-radius` should be removed for every element.

::: warning
Please only add variable overrides in this file. You should not write CSS code like `.container { background: #f00 }` in this file.
:::

::: info
When running `composer run watch:storefront` in platform only setups or `./bin/watch-storefront.sh` in the production template, SCSS variables will be injected dynamically by webpack. When writing selectors and properties in the `overrides.scss` the code can appear multiple times in your built CSS.
:::

## Next steps

Now that you know how to override Bootstrap variables, here is a list of related topics which might be interesting for you.

* [Theme configuration](theme-configuration)
* [Add SCSS Styling and JavaScript to a theme](add-css-js-to-theme)
* [Add assets to a theme](add-assets-to-theme)

---

---

## Override responsive breakpoints in a Theme
**Source:** [guides/plugins/themes/override-theme-breakpoints.md](https://developer.shopware.com/docs/guides/plugins/themes/override-theme-breakpoints.md)  
# Override responsive breakpoints in a Theme

Shopware uses the default breakpoint configuration of Bootstrap for responsive layout adjustments. However, these breakpoints are also passed to Twig and JS. If you want to override these breakpoints with your custom configuration, you can do so by overriding the corresponding theme config fields.

## Setting custom breakpoint values

Since Shopware 6.7.8.0 you have six new theme config fields available to override specific breakpoint settings. These fields are hidden for users in the administration of Shopware and only serve as a developer feature. You can use these fields in the theme.json of your theme to set specific values for each breakpoint.

**Example:**

::: code-group

```json [PLUGIN_ROOT/src/Resources/theme.json]
{
  "name": "My custom theme",
  "config": {
    "fields": {
      "sw-breakpoint-xs": {
        "value": 0
      },
      "sw-breakpoint-sm": {
        "value": 576
      },
      "sw-breakpoint-md": {
        "value": 768
      },
      "sw-breakpoint-lg": {
        "value": 992
      },
      "sw-breakpoint-xl": {
        "value": 1200
      },
      "sw-breakpoint-xxl": {
        "value": 1400
      }
    }
  }
}
```

:::

When you override the existing fields, they will automatically replace the existing values in Twig and JS. You can also access those values in your code the same way as other theme variables. If you also want these values to be used in SCSS to override the default Bootstrap configuration, you have to do this separately.

## Overriding Bootstrap default Breakpoints

Because Shopware uses the default values of Bootstrap for breakpoints in CSS, you won't find any configuration in the default theme of Shopware. However, you can change those in your custom theme.

For detailed information about the configuration of breakpoints in Bootstrap, you can refer to the [official documentation](https://getbootstrap.com/docs/5.3/layout/breakpoints/).

The theme config values are also available in SCSS, and you can reuse them to apply the same configuration in SCSS. This way you have a single point of truth for defining the breakpoints for your theme.

::: code-group

```scss [PLUGIN_ROOT/src/Resources/app/storefront/src/scss/overrides.scss]
$grid-breakpoints: (
    xs: $sw-breakpoint-xs,
    sm: $sw-breakpoint-sm,
    md: $sw-breakpoint-md,
    lg: $sw-breakpoint-lg,
    xl: $sw-breakpoint-xl,
    xxl: $sw-breakpoint-xxl
);
```

:::

---

---

## Theme Base Guide
**Source:** [guides/plugins/themes/theme-base-guide.md](https://developer.shopware.com/docs/v6.6/guides/plugins/themes/theme-base-guide.md)  
# Theme Base Guide

A theme gives you the ability to extend/change the visual appearance of the Storefront via styling the SCSS/CSS and adjusting twig templates. You can also provide JavaScript with your theme to change how the Storefront behaves in the browser. For example, JavaScript is used in Shopware to open the offcanvas shopping-cart. Now, as you might know, Shopware comes with a default theme, to make things a bit easier. The default theme in Shopware is built on top of Bootstrap 5, style-wise. So everything you can do with Bootstrap, you can do with the Shopware Storefront as well.

Another handy capability is the theme configuration: As a theme developer you can define variables which can be configured by the shop owner in the Administration. Those variables are accessible in your theme and let you implement powerful features.

Basically a theme can be an app/plugin that aims at changing the visual appearance of the Storefront. To be better understand the difference among [Plugins and Apps vs Themes](differences-plugins-and-apps-vs-themes), refer to the corresponding article.

## Next steps

Now that you know what you can do with themes, the next steps would be to [create themes](create-a-theme).

---

---

## Theme Configuration
**Source:** [guides/plugins/themes/theme-configuration.md](https://developer.shopware.com/docs/v6.6/guides/plugins/themes/theme-configuration.md)  
*(Body truncated in this bundle; follow the link for the rest.)*

# Theme Configuration

::: info
The `configInheritance` is available from Shopware Version 6.4.8.0
:::

## Overview

This guide shows you how the theme configuration works and explains the possibilities of the settings in more depth.

## Prerequisites

This guide is built upon the guide on creating a first theme:

## Structure of theme configuration

The theme configuration for a theme is located in the `theme.json` file `<plugin root>/src/Resources` folder. Open up the `<plugin root>/src/Resources/theme.json` file with your favorite code-editor. The configuration looks like this.

```javascript
// <plugin root>/src/Resources/theme.json
{
  "name": "SwagBasicExampleTheme",
  "author": "Shopware AG",
  "description": {
    "en-GB": "My custom theme",
    "de-DE": "Mein custom thema"
  },
  "views": [
     "@Storefront",
     "@Plugins",
     "@SwagBasicExampleTheme"
  ],
  "previewMedia": "app/storefront/dist/assets/defaultThemePreview.jpg",
  "style": [
    "app/storefront/src/scss/overrides.scss",
    "@Storefront",
    "app/storefront/src/scss/base.scss"
  ],
  "script": [
    "@Storefront",
    "app/storefront/dist/storefront/js/swag-basic-example-theme/swag-basic-example-theme.js"
  ],
  "asset": [
    "@Storefront",
    "app/storefront/src/assets"
  ],
  "configInheritance": [
    "@Storefront",
    "@OtherTheme"
    ]
}
```

::: info
If you make changes or additions to the `theme.json` file, you must then execute the `theme:refresh` command to put them into effect. Run `bin/console theme:refresh` in order to update your theme.
:::

Let's have a closer look at each section.

```javascript
// <plugin root>/src/Resources/theme.json
{
  "name": "SwagBasicExampleTheme",
  "author": "Shopware AG",
  "description": {
    "en-GB": "Just another description",
    "de-DE": "Nur eine weitere Beschreibung"
  },
  ...
}
```

Here change the `name` of your theme and the `author`. The `description` section is optional and as you notice it is also translatable.

The `views` section controls the template inheritance. This will be covered in the [Theme inheritance](add-theme-inheritance) guide.

```javascript
// <plugin root>/src/Resources/theme.json
{
  ...
  "views": [
     "@Storefront",
     "@Plugins",
     "@SwagBasicExampleTheme"
  ],
  ...
}
```

The `previewMedia` field provides a path `app/storefront/dist/assets/defaultThemePreview.jpg` to an image file that is relative to the root directory of the theme. It serves as a visual preview of the theme. This preview image is typically displayed within the Shopware administration interface or theme marketplace as a thumbnail or preview of the theme's appearance to give users an idea of how the theme will appear on their storefront before they activate it.

```javascript
// <plugin root>/src/Resources/theme.json
{
  ...
  "previewMedia": "app/storefront/dist/assets/defaultThemePreview.jpg",
  ...
}
```

The `style` section determines the order of the CSS compilation. In the `<plugin root>/app/storefront/src/scss/base.scss` file you can apply your changes you want to make to the `@Storefront` standard styles or add other styles you need. The `<plugin root>/app/storefront/src/scss/overrides.scss` file is used for a special case. Maybe you need to override some defined `variables` or `functions` defined by Shopware or Bootstrap, you can implement your changes here. Checkout the [Override bootstrap variables in a theme](override-bootstrap-variables-in-a-theme) guide for further information.

```javascript
// <plugin root>/src/Resources/theme.json
{
  ...
  "style": [
    "app/storefront/src/scss/overrides.scss",
    "@Storefront",
    "app/storefront/src/scss/base.scss"
  ],
  ...
}
```

## Assets

The `asset` option you can configure your paths to your assets like images, fonts, etc. The standard location to put your assets to is the `<plugin root>/app/storefront/src/assets` folder. Checkout the [Add assets to theme](add-assets-to-theme) guide for further information.

```javascript
// <plugin root>/src/Resources/theme.json
{
  ...
  "asset": [
     "app/storefront/src/assets"
   ]
  ...
}
```

If you need the assets from the default storefront theme for your custom theme, just add `@Storefront` as asset path

```javascript
// <plugin root>/src/Resources/theme.json
{
  ...
  "asset": [
     "@Storefront",
     "app/storefront/src/assets"
   ]
  ...
}
```

## Config fields

One of the benefits of creating a theme is that you can overwrite the theme configuration of the default theme or add your own configurations.

```javascript
// <plugin root>/src/Resources/theme.json
{
  ... 
  "asset":[
    ...
  ],
  "config": {
      "fields": {
        "sw-color-brand-primary": {
          "value": "#00ff00"
        }
      }
   }
}
```

In the example above, we change the primary color to green. You always inherit from the storefront config and both configurations are merged. This also means that you only have to provide the values you actually want to change. You can find a more detailed explanation of the configuration inheritance in the section [Theme inheritance](add-theme-inheritance).

::: warning
If you overwrite variables of another theme from a third party provider and these are renamed or removed at a later time, this can lead to issues and the theme can no longer be compiled. So be aware of it.
:::

The `theme.json` contains a `config` property which contains a list of tabs, blocks, sections and fields.

The key of each config field item is also the technical name which you use to access the config option in your theme or scss files. `config` entries will show up in the Administration and can be customized by the end user (if `editable` is set to `true`, see table below).

The following parameters can be defined for a config field item:

| Name | Meaning |
| :--- | :--- |
| `label` | Array of translations with locale code as key |
| `type` | Type of the config. Possible values: color, text, number, fontFamily, media, checkbox, switch and url |
| `editable` | If set to false, the config option will not be displayed (e.g. in the Administration) |
| `tab` | Name of a tab to organize the config options |
| `block` | Name of a block to organize the config options |
| `section` | Name of a section to organize the config options |
| `custom` | The defined data will not be processed but is available via API |
| `scss` | If set to false, the config option will not be injected as a SCSS variable |
| `fullWidth` | If set to true, the Administration component width will be displayed in full width |

## Field types

You can use different field types in your theme manager:

A text field example:

```javascript
// <plugin root>/src/Resources/theme.json
{
  ...
  "config": {
    "fields": {
      "modal-padding": {
        "label": {
          "en-GB": "Modal padding",
          "de-DE": "Modal Innenabstand"
        },
        "type": "text",
        "value": "(0, 0, 0, 0)",
        "editable": true
      }
    }
  }
}
```

A number field example:

```javascript
// <plugin root>/src/Resources/theme.json
{
  ...
  "config": {
    "fields": {
      "visible-slides": {
        "label": {
          "en-GB": "Number of visible slides",
          "de-DE": "Anzahl an sichtbaren Slider Bildern"
        },
        "type": "number",
        "custom": {
          "numberType": "int",
          "min": 1,
          "max": 6
        },
        "value": 3,
        "editable": true
      }
    }
  }
}
```

Two boolean field examples:

```javascript
// <plugin root>/src/Resources/theme.json
{
  ...
  "config": {
    "fields": {
      "navigation-fixed": {
        "label": {
          "en-GB": "Fix navigation",
          "de-DE": "Navigation fixieren"
        },
        "type": "switch",
        "value": true,
        "editable": true
      }
    }
  }
}
```

or

```javascript
// <plugin root>/src/Resources/theme.json
{
  ...
  "config": {
    "fields": {
      "navigation-fixed": {
        "label": {
          "en-GB": "Fix navigation",
          "de-DE": "Navigation fixieren"
        },
        "type": "checkbox",
        "value": true,
        "editable": true
      }
    }
  }
}
```

## Examples for custom config fields

A custom single-select field example

```javascript
// <plugin root>/src/Resources/theme.json
{
  "name": "Just another theme",
  "author": "Just another author",
  "description": {
    "en-GB": "Just another description",
    "de-DE": "Nur eine weitere Beschreibung"
  },
  "views": [
    "@Storefront",
    "@Plugins",
    "@SelectExample"
  ],
  "style": [
    "app/storefront/src/scss/overrides.scss",
    "@Storefront",
    "app/storefront/src/scss/base.scss"
  ],
  "script": [
    "@Storefront",
    "app/storefront/dist/storefront/js/select-example/select-example.js"
  ],
  "asset": [
    "@Storefront",
    "app/storefront/src/assets"
  ],
  "config": {
    "blocks": {
      "exampleBlock": {
        "label": {
          "en-GB": "Example block",
          "de-DE": "Beispiel Block"
        }
      }
    },
    "sections": {
      "exampleSection": {
        "label": {
          "en-GB": "Example section",
          "de-DE": "Beispiel Sektion"
        }
      }
    },
    "fields": {
      "my-single-select-field": {
        "label": {
          "en-GB": "Select a font size",
          "de-DE": "Wähle ein Schriftgröße"
        },
        "type": "text",
        "value": "24",
        "custom": {
          "componentName": "sw-single-select",
          "options": [
            {
              "value": "16",
              "label": {
                "en-GB": "16px",
                "de-DE": "16px"
              }
            },
            {
              "value": "20",
              "label": {
                "en-GB": "20px",
                "de-DE": "20px"
              }
            },
            {
              "value": "24",
              "label": {
                "en-GB": "24px",
                "de-DE": "24px"
              }
            }
          ]
        },
        "editable": true,
        "block": "exampleBlock",
        "section": "exampleSection"
      }
    }
  }
}
```

![Example of a custom single-select field](../../../assets/example-single-select-config.png)

A custom multi-select field example

```javascript
// <plugin root>/src/Resources/theme.json
{
  "name": "Just another theme",
  "author": "Just another author",
  "description": {
    "en-GB": "Just another description",
    "de-DE": "Nur eine weitere Beschreibung"
  },
  "views": [
    "@Storefront",
    "@Plugins",
    "@SelectExample"
  ],
  "style": [
    "app/storefront/src/scss/overrides.scss",
    "@Storefront",
    "app/storefront/src/scss/base.scss"
  ],
  "script": [
    "@Storefront",
    "app/storefront/dist/storefront/js/select-example/select-example.js"
  ],
  "asset": [
    "@Storefront",
    "app/storefront/src/assets"
  ],
  "config": {
    "blocks": {
      "exampleBlock": {
        "label": {
          "en-GB": "Example block",
          "de-DE": "Beispiel Block"
        }
      }
    },
    "sections": {
      "exampleSection": {
        "label": {
          "en-GB": "Example section",
          "de-DE": "Beispiel Sektion"
        }
      }
    },
    "fields": {
      "my-multi-select-field": {
        "label": {
          "en-GB": "Select some colours",
          "de-DE": "Wähle Farben aus"
        },
        "type": "text",
        "editable": true,
        "value": [
          "green",
          "blue"
        ],
        "custom": {
          "componentName": "sw-multi-select",
          "options": [
            {
              "value": "green",
              "label": {
                "en-GB": "green",
                "de-DE": "grün"
              }
            },
            {
              "value": "red",
              "label": {
                "en-GB": "red",
                "de-DE": "rot"
              }
            },
            {
              "value": "blue",
              "label": {
                "en-GB": "blue",
                "d

… **Truncated.** Full document: https://developer.shopware.com/docs/v6.6/guides/plugins/themes/theme-configuration.md


---

## Theme Inheritance Configuration
**Source:** [guides/plugins/themes/theme-inheritance-configuration.md](https://developer.shopware.com/docs/v6.6/guides/plugins/themes/theme-inheritance-configuration.md)  
# Theme Inheritance Configuration

::: info
The `configInheritance` is available from Shopware Version 6.4.8.0
:::

## Overview

This guide explains how you can use a theme as a basic corporate design theme and create inherited themes for special purposes like holiday time or a sales week.

Imagine you have a theme that is applying your corporate design to the storefront. With your colors, your logo and other configuration fields. But on a special week in the year, you have additional requirements for a special design, like a discount counter or an advent calendar.

## Setup

### Create two themes

Create the two themes like described in [Theme inheritance](./add-theme-inheritance).

### Configure your themes

Add some configuration fields you need in your basic theme inside the `theme.json` of the `SwagBasicExampleTheme`

```javascript
// <plugin root>/src/Resources/theme.json
{
  "name": "SwagBasicExampleTheme",
  .....
  "config": {
    "blocks": {
      "colors": {
        "themeColors": {
          "en-GB": "Theme colours",
          "de-DE": "Theme Farben"
        }
      }
    },
    "sections": {
      "importantColors": {
        "label": {
          "en-GB": "Important colors",
          "de-DE": "Wichtige Farben"
        }
      }
    },
    "tabs": {
      "colors": {
          "label": {
              "en-GB": "Colours",
              "de-DE": "Farben"
          }
      } 
    },
    "fields": {
      "sw-color-brand-primary": {
        "label": {
          "en-GB": "Primary colour",
          "de-DE": "Primär"
        },
        "type": "color",
        "value": "#399",
        "editable": true,
        "tab": "colors",
        "block": "themeColors",
        "section": "importantColors"
      },
      "sw-brand-icon": {
        "label": {
            "en-GB": "Brand icon", 
            "de-DE": "Markenlogo"
        },
        "type": "url",
        "value": "/our-logo.png",
        "editable": true
      }
    }
  }
}
```

## Extending an existing theme configuration with a new theme

Add configurations to your extended theme

```javascript
// <plugin root>/src/Resources/theme.json
{
  "name": "SwagBasicExampleThemeExtend",
  .....
  "configInheritance": [
    "@Storefront",
    "@SwagBasicExampleTheme"
  ],
  "config": {
    "fields": {
      "sw-brand-icon": {
        "type": "url",
        "value": "/our-logo-holidays.png",
        "editable": true
      },
      "sw-advent-calendar-background-color": {
        "label": {
          "en-GB": "Advent calendar background color",
          "de-DE": "Adventskalender Hintergrundfarbe"
        },
        "type": "color",
        "value": "#399",
        "editable": true
      }
    }
  }
}
```

In this theme (`SwagBasicExampleThemeExtend`) all the configuration fields from the themes `Storefront` and `SwagBasicExampleTheme` will be used as inherited values. They will be shown in the Administration with an inherit anchor and will use the value of the parent themes as long as they are not set to a different value. In the `theme.json` the `sw-brand-icon` field value will be overwritten with a different default value. So this field will not be inherited regardless that it is already defined in the `SwagBasicExampleTheme`. This theme also adds a new field for the background color of the advent calendar (`sw-advent-calendar-background-color`) because this is only needed in this special theme which will only be used for 4-6 weeks a year.

## Next steps

Now that you know how the theme inheritance works you can start with own customizations. Here is a list of other related topics where assets can be used.

* [Add SCSS Styling and JavaScript to a theme](add-css-js-to-theme)
* [Customize templates](../plugins/storefront/customize-templates)

---

---

