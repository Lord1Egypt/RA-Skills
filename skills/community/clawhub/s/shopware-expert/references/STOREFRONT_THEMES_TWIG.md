# STOREFRONT THEMES TWIG

Compiled excerpts from the Shopware Developer Documentation snapshot. Prefer live docs at [developer.shopware.com](https://developer.shopware.com/) when in doubt.

---

## Storefront
**Source:** [guides/plugins/plugins/storefront.md](https://developer.shopware.com/docs/v6.6/guides/plugins/plugins/storefront.md)  
# Storefront

Storefront handles the e-commerce platform's front end, including the online store's visual presentation and user interface.

You can customize and enhance the storefront by adding or modifying templates, layouts, styles, and components via plugins. It allows adding custom pages, layouts, dynamic content, filters, media, assets, and styles to create unique and engaging shopping experiences, ensuring a seamless and visually appealing interface for customers. It enables businesses to showcase their products, implement responsive designs, optimize performance, and deliver a personalized shopping journey to online visitors.

---

---

## Add Caching to Custom Controller
**Source:** [guides/plugins/plugins/storefront/add-caching-to-custom-controller.md](https://developer.shopware.com/docs/v6.6/guides/plugins/plugins/storefront/add-caching-to-custom-controller.md)  
# Add Caching to Custom Controller

## Overview

In this guide you will learn how to define a controller route as cacheable for the HTTP cache.

## Prerequisites

In order to add a cache to an own controller route, you first need a plugin with a controller. Therefore, you can refer to the [Add custom controller guide](./add-custom-controller).

## Define the controller as cacheable

To define a controller route as cacheable, the default option of the route attribute `_httpCache` must be set to `true`. Once this option is set, the core takes care of everything else. If the route is called several times in the same state, a response is generated only for the first request and the second request gets the same response as the first one. It is also possible to exclude certain states from the cache. Shopware sets two different user states to which the HTTP cache reacts:

* state: `logged-in` - means that the user is logged in.

* state: `cart-filled` - means that there are products in the shopping cart.

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

    #[Route(path: '/example', name: 'frontend.example.example', methods: ['GET'], defaults: ['_httpCache' => true])]
    public function showExample(): Response
    {
        return $this->renderStorefront('@SwagBasicExample/storefront/page/example/index.html.twig', [
            'example' => 'Hello world'
        ]);
    }
}
```

## Cache invalidation

As soon as a controller route has been defined as cacheable, and the corresponding response is written to the cache, it is tagged accordingly. For this purpose, the core uses all cache tags generated during the request or loaded from existing cache entries. The cache invalidation of the Storefront controller routes is controlled by the cache invalidation of the store API routes.

For more information about Store API cache invalidation, you can refer to the [Add Cache for Store Api Route Guide](../framework/store-api/add-caching-for-store-api-route).

This is because all data loaded in a controller route, is loaded in the core via the corresponding Store API routes and provided with corresponding cache tags. So the tags of the HTTP cache entries we have in the core consists of the sum of all store api tags generated or loaded during the request. Therefore the invalidation of a controller route that loads all data via the store API, no additional invalidation needs to be written.

---

---

## Add Cookie to Manager
**Source:** [guides/plugins/plugins/storefront/add-cookie-to-manager.md](https://developer.shopware.com/docs/v6.6/guides/plugins/plugins/storefront/add-cookie-to-manager.md)  
# Add Cookie to Manager

## Overview

Since the GDPR was introduced, every website has to be shipped with some sort of a cookie consent manager. This is also the case for Shopware 6 of course, which comes with a cookie consent manager by default. In this guide you will learn how you can add your own cookies to the cookie consent manager of Shopware 6.

## Prerequisites

This guide is built upon the [Plugin base guide](../plugin-base-guide), so have a look at that first if you're lacking a running plugin. Also you will have to know how to [create your own service](../plugin-fundamentals/add-custom-service) and [decorations](../plugin-fundamentals/adjusting-service#decorating-the-service), so you might want to have a look at those guides as well.

## Extend the cookie consent manager

Adding custom cookies basically requires you to decorate a service, the `CookieProvider` to be precise. Neither decorations, nor adding a service via a `services.xml` is explained here, so make sure to have a look at the previously mentioned guides first, if you're lacking this knowledge.

### Registering your decoration

Start with creating the `services.xml` entry and with decorating the `CookieProviderInterface`. The `CookieProvider` service was already built before we decided to use abstract classes for decorations, so don't be confused here.

```xml
// <plugin root>/src/Resources/config/services.xml
<?xml version="1.0" ?>

<container xmlns="http://symfony.com/schema/dic/services"
           xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
           xsi:schemaLocation="http://symfony.com/schema/dic/services http://symfony.com/schema/dic/services/services-1.0.xsd">

    <services>
       <service id="PluginName\Framework\Cookie\CustomCookieProvider"
                decorates="Shopware\Storefront\Framework\Cookie\CookieProviderInterface">
             <argument type="service" 
                       id="PluginName\Framework\Cookie\CustomCookieProvider.inner" />
         </service>
    </services>
</container>
```

In the next step we'll create the actual decorated class.

### Creating the decorated service

We need to create a class called `CustomCookieProvider`, which implements the `CookieProviderInterface`. Our constructor parameter is the original `CookieProviderInterface` instance, which we need to call to get all other cookies as well.

The interface mentioned above requires you to implement a method called `getCookieGroups`, which has to return an array of cookie groups and their respective cookies. You need to call the original method now, receive the default cookie groups and then merge your custom group, if there's any, and your custom cookies into it.

Let's have a look at an example:

```php
// <plugin root>/src/Framework/Cookie/CustomCookieProvider.php
<?php declare(strict_types=1);

namespace PluginName\Framework\Cookie;

use Shopware\Storefront\Framework\Cookie\CookieProviderInterface;

class CustomCookieProvider implements CookieProviderInterface {

    private CookieProviderInterface $originalService;

    public function __construct(CookieProviderInterface $service)
    {
        $this->originalService = $service;
    }

    private const singleCookie = [
        'snippet_name' => 'cookie.name',
        'snippet_description' => 'cookie.description ',
        'cookie' => 'cookie-key',
        'value' => 'cookie value',
        'expiration' => '30'
    ];

    // cookies can also be provided as a group
    private const cookieGroup = [
        'snippet_name' => 'cookie.group_name',
        'snippet_description' => 'cookie.group_description ',
        'entries' => [
            [
                'snippet_name' => 'cookie.first_child_name',
                'cookie' => 'cookie-key-1',
                'value'=> 'cookie value',
                'expiration' => '30'
            ],
            [
                'snippet_name' => 'cookie.second_child_name',
                'cookie' => 'cookie-key-2',
                'value'=> 'cookie value',
                'expiration' => '60'
            ]
        ],
    ];

    public function getCookieGroups(): array
    {
        return array_merge(
            $this->originalService->getCookieGroups(),
            [
                self::cookieGroup,
                self::singleCookie
            ]
        );
    }
}
```

As already mentioned, we're overwriting the method `getCookieGroups` and in there we're calling the original method first. We then proceed to merge our own custom group into it, as well as a custom cookie.

This will eventually lead to a new group being created, containing two new cookies, as well as a new cookie without a group.

And that's basically it already. After loading your Storefront, you should now see your new cookies and the cookie-group.

### Cookie array keys

Here's a list of attributes, that you can apply to a cookie array:

| Attribute | Data type | Required | Description |
| :--- | :--- | :--- | :--- |
| snippet\_name | String | Yes | Key of a snippet containing the display name of a cookie or cookie group. |
| snippet\_description | String | No | Key of a snippet containing a short description of a cookie or cookie group. |
| cookie | String | Yes | The internal cookie name used to save the cookie. |
| value | String | No | If unset, the cookie will not be updated (set active or inactive) by Shopware, but passed to the update event only. |
| expiration | String | No | Cookie lifetime in days. **If unset, the cookie expires with the session**. |
| entries | Array | No | An array of cookie objects. Used to create grouped cookies. Nested groups are not supported. If using this, **the group itself should not have the attributes** ***cookie*****,** ***value*** **and** ***expiration*****.**. |

## Next steps

Those changes will mainly just show your new cookies in the cookie consent manager, but without much function. Head over to our guide about [Reacting to cookie consent changes](reacting-to-cookie-consent-changes) to see how you can implement your custom logic once your cookie got accepted or declined.

---

---

## Add Custom Assets
**Source:** [guides/plugins/plugins/storefront/add-custom-assets.md](https://developer.shopware.com/docs/v6.6/guides/plugins/plugins/storefront/add-custom-assets.md)  
# Add Custom Assets

## Overview

When working with an own plugin, the usage of own custom images or other assets is a natural requirement. So of course you can do that in Shopware. In this guide we will discover together how it's possible to add and use custom assets in your Shopware plugin.

## Prerequisites

In order to be able to start with this guide, you need to have an own plugin running. As to most guides, this guide is also built upon the [Plugin base guide](../plugin-base-guide)

Needless to say, you should have your image or another asset at hand to work with.

## Adding custom assets to your plugin

In order to add custom assets to your theme, you need to create a new folder called public inside the `src/Resources` directory of your plugin. Here you're able to store your assets files, so please feel free to save your image there - we'll do the same thing in our example plugin.

```bash
# PluginRoot
.
├── composer.json
└── src
    ├── Resources
    │   ├── public
    │   │   └── your-image.png <-- Asset file here
    └── SwagBasicExample.php
```

Afterwards, you need to make sure your plugin assets are copied over to the public/bundles folder. However, don't to this by hand - the command `bin/console assets:install` will take care of it.

```text
# shopware-root/public/bundles
.
├── administration
├── framework
├── storefront
└── swagbasicexample
    └── your-image.png <-- Your asset is copied here
```

## Linking to assets

### Using custom assets in your template

Let's think about a simple example, displaying our image right in the base template of the Storefront. In there we're able to link our assets by simply using the [asset](https://symfony.com/doc/current/templates.html#linking-to-css-javascript-and-image-assets) function Symfony provides:

```twig
// <plugin root>/src/Resources/views/storefront/base.html.twig
{% sw_extends '@Storefront/storefront/base.html.twig' %}

{% block base_main %}
    <h2>Asset:</h2>

    {# Using asset function to display our custom asset #}
    <img src="{{ asset('bundles/swagbasicexample/image.png', 'asset') }}">
    {{ parent() }}
{% endblock %}
```

That's basically all you need to do to link your plugin's custom assets.

### Using custom assets in your CSS files

There's one more interesting possibility though. If you want, you can use your custom asset in your CSS files. Look at the following example:

```css
// <plugin root>/src/Resources/app/storefront/src/scss/base.scss
body {
    background-image: url("#{$sw-asset-public-url}/bundles/swagbasicexample/image.png");
}
```

You see, we can use our custom assets by using the asset path provided by the `bundle` directory.

### Adding custom assets in themes

Of course, you're able to use custom assets in themes as well. In this context there's another way on integration custom assets into your theme. Please take a look on the guide about adding assets to a theme for further detail:

## Next steps

One of the said custom assets are medias. For more information on that, refer to [Media and thumbnails](use-media-thumbnails).

---

---

## Add custom captcha
**Source:** [guides/plugins/plugins/storefront/add-custom-captcha.md](https://developer.shopware.com/docs/v6.6/guides/plugins/plugins/storefront/add-custom-captcha.md)  
# Add custom captcha

## Overview

You can add your custom captcha to the Shopware 6 core. This guide will show you how to do that.

## Prerequisites

In order to be able to start with this guide, you need to have an own plugin running. As to most guides, this guide is also built upon the [Plugin base guide](../plugin-base-guide)

## Adding custom captcha to your plugin

In order to add custom captcha to your plugin, create a new folder called `Captcha` inside the `src/Framework` directory of your plugin. This is optional, but it's a good practice to keep your plugin files organized.

Take a look at the AbstractCaptcha class. This class is the base class for all captcha types. It contains the following methods:

* `supports(string $type): bool` - This method is used to check if the captcha type is supported by the plugin.
* `isValid(string $code): bool` - This method is used to check if the captcha code is valid.
* `getName(): string` - This method is used to get the name of the captcha type.
* `shouldBreak(): bool` - This method is used to check if the captcha should break the validation.
* `getData(): array` - This method is used to get the data of the captcha type.
* `getViolations(): ConstraintViolationListInterface` - This method is used to get the violations of the captcha type.

Extend the AbstractCaptcha class and implement the methods isValid and getName. The isValid method should return true if the captcha code is valid, false otherwise. The getName method should return the name of the captcha type.

```php

<?php declare(strict_types=1);

namespace Shopware\Storefront\Framework\Captcha;

use GuzzleHttp\ClientInterface;
use Psr\Http\Client\ClientExceptionInterface;
use Shopware\Core\Framework\Log\Package;
use Symfony\Component\HttpFoundation\Request;

#[Package('storefront')]
class YourCaptcha extends AbstractCaptcha
{
    final public const CAPTCHA_NAME = 'yourCaptchaName';
    final public const CAPTCHA_REQUEST_PARAMETER = '_your_captcha_name';
    private const YOUR_CAPTCHA_ENDPOINT = 'https://www.yourcaptcha.com/verify';

    /**
     * @internal
     */
    public function __construct(private readonly ClientInterface $client)
    {
    }

    /**
     * {@inheritdoc}
     */
    public function isValid(Request $request, array $captchaConfig): bool
    {
        if (!$request->get(self::CAPTCHA_REQUEST_PARAMETER)) {
            return false;
        }
        
        try {
            $response = $this->client->request('POST', self::GOOGLE_CAPTCHA_VERIFY_ENDPOINT, [
                'form_params' => [
                    'response' => $request->get(self::CAPTCHA_REQUEST_PARAMETER),
                    'remoteip' => $request->getClientIp(),
                ],
            ]);

            $responseRaw = $response->getBody()->getContents();
            $response = json_decode($responseRaw, true);

            return $response && (bool) $response['success'];
        } catch (ClientExceptionInterface) {
            return false;
        }
    }

    /**
     * {@inheritdoc}
     */
    public function getName(): string
    {
        return self::CAPTCHA_NAME;
    }
}

```

## Google reCAPTCHA v3 example

You might want to check out the example [GoogleReCaptchaV3](https://github.com/shopware/shopware/blob/trunk/src/Storefront/Framework/Captcha/GoogleReCaptchaV3.php) class from the Shopware 6 core. It's a good example of how to implement a custom captcha type.

---

---

## Add Custom Controller
**Source:** [guides/plugins/plugins/storefront/add-custom-controller.md](https://developer.shopware.com/docs/v6.6/guides/plugins/plugins/storefront/add-custom-controller.md)  
# Add Custom Controller

## Overview

In this guide you will learn how to create a custom Storefront controller.

## Prerequisites

In order to add your own controller for your plugin, you first need a plugin as base. Therefore, you can refer to the [Plugin Base Guide](../plugin-base-guide).

::: info
Refer to this video on **[Common Storefront controller tasks](https://www.youtube.com/watch?v=5eXXNh4cQG0)** explaining the basics about Storefront controllers. Also available on our free online training ["Shopware 6 Backend Development"](https://academy.shopware.com/courses/shopware-6-backend-development-with-jisse-reitsma).
:::

## Adding custom Storefront controller

### Storefront Controller class example

First of all we have to create a new controller which extends from the `StorefrontController` class. A controller is also just a service which can be registered via the service container. Furthermore, we have to define our `Route` with `defaults` and `_routeScope` via attributes, it is used to define which domain a route is part of and **needs to be set for every route**. In our case the scope is `storefront`.

::: info
Prior to Shopware 6.4.11.0 the `_routeScope` was configured by a dedicated annotation: `@RouteScope`. This way of defining the route scope is deprecated for the 6.5 major version.
:::

Go ahead and create a new file `ExampleController.php` in the directory `<plugin root>/src/Storefront/Controller/`.

```php
// <plugin root>/src/Storefront/Controller/ExampleController.php
<?php declare(strict_types=1);

namespace Swag\BasicExample\Storefront\Controller;

use Shopware\Storefront\Controller\StorefrontController;
use Symfony\Component\Routing\Attribute\Route;

#[Route(defaults: ['_routeScope' => ['storefront']])]
class ExampleController extends StorefrontController
{
}
```

Now we can create a new example method with a `Route` attribute which has to contain our route, in this case it will be `/example`. The route defines how our new method will be accessible.

Below you can find an example implementation of a controller method including a route, where we render an `example.html.twig` template file with a template variable `example`.

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
        return $this->renderStorefront('@SwagBasicExample/storefront/page/example.html.twig', [
            'example' => 'Hello world'
        ]);
    }
}
```

The name of the method does not really matter, but it should somehow fit its purpose. More important is the `Route` attribute, that points to the route `/example`. Also note its name, which is also quite important. Make sure to use prefixes `frontend`, `widgets`, `payment`, `api` or `store-api` here, depending on what your route does. Inside the method, we're using the method `renderStorefront` to render a twig template file in addition with the template variable `example`, which contains `Hello world`. This template variable will be usable in the rendered template file. The method `renderStorefront` then returns a `Response`, as every routed controller method has to.

It is also possible to define the `_routeScope` per route.

::: info
Prior to Shopware 6.4.11.0 the `_routeScope` was configured by a dedicated annotation: `@RouteScope`. This way of defining the route-scope is deprecated for the 6.5 major version.
:::

```php
// <plugin root>/src/Storefront/Controller/ExampleController.php
<?php declare(strict_types=1);

namespace Swag\BasicExample\Storefront\Controller;

use Shopware\Storefront\Controller\StorefrontController;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\Routing\Attribute\Route;

#[Route(defaults: ['_routeScope' => ['storefront']])]
class ExampleController extends StorefrontController
{
    #[Route(path: '/example', name: 'frontend.example.example', methods: ['GET'], defaults: ['_routeScope' => ['storefront']])]
    public function showExample(): Response
    {
        ...
    }
}
```

### Services.xml example

Next, we need to register our controller in the DI-container and make it public.

```xml
// <plugin root>/src/Resources/config/services.xml
<?xml version="1.0" ?>

<container xmlns="http://symfony.com/schema/dic/services" 
           xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
           xsi:schemaLocation="http://symfony.com/schema/dic/services http://symfony.com/schema/dic/services/services-1.0.xsd">

    <services>
        <service id="Swag\BasicExample\Storefront\Controller\ExampleController" public="true">
            <call method="setContainer">
                <argument type="service" id="service_container"/>
            </call>
            <call method="setTwig">
                <argument type="service" id="twig"/>
            </call>
        </service>
    </services>
</container>
```

Please also note the `call` tag, which is necessary in order to set the DI container to the controller.

### Routes.xml example

Once we‘ve registered our new controller, we have to tell Shopware how we want it to search for new routes in our plugin. This is done with a `routes.xml` file at `<plugin root>/src/Resources/config/` location. Have a look at the official [Symfony documentation](https://symfony.com/doc/current/routing.html) about routes and how they are registered.

```xml
// <plugin root>/src/Resources/config/routes.xml
<?xml version="1.0" encoding="UTF-8" ?>
<routes xmlns="http://symfony.com/schema/routing"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:schemaLocation="http://symfony.com/schema/routing
        https://symfony.com/schema/routing/routing-1.0.xsd">

    <import resource="../../Storefront/Controller/*Controller.php" type="attribute" />
</routes>
```

### Adding template

Now we registered our controller and Shopware indexes the route, but the template file, that is supposed to be rendered, is still missing. Let's change that now.

As previously mentioned, the code will try to render an `index.html.twig` file. Thus we have to create an `index.html.twig` in the `<plugin root>/src/Resources/views/storefront/page/example` directory, as defined in our controller. Below you can find an example, where we extend from the template `base.html.twig` and override the block `base_content`. In our [Customize templates](customize-templates) guide, you can learn more about customizing templates.

```twig
// <plugin root>/src/Resources/views/storefront/page/example.html.twig
{% sw_extends '@Storefront/storefront/base.html.twig' %}

{% block base_content %}
    <h1>Our example controller!</h1>
{% endblock %}
```

### Request and Context

If necessary, we can access the `Request` and `SalesChannelContext` instances in our controller method.

Here's an example:

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
    public function showExample(Request $request, SalesChannelContext $context): Response
    {
        ...
    }
}
```

## Next steps

Since you've already created a controller now, which is also part of creating a so called "page" in Shopware, you might want to head over to our guide about [creating a page](add-custom-page).

---

---

## Add Custom Javascript
**Source:** [guides/plugins/plugins/storefront/add-custom-javascript.md](https://developer.shopware.com/docs/v6.6/guides/plugins/plugins/storefront/add-custom-javascript.md)  
*(Body truncated in this bundle; follow the link for the rest.)*

# Add Custom Javascript

## Overview

If you want to add interactivity to your Storefront you probably have to write your own JavaScript plugin. Here you will be guided through the process of writing and registering your own JavaScript plugins. You will write a plugin that simply checks if the user has scrolled to the bottom of the page and then creates an alert.

## Prerequisites

You need for this guide a running plugin and therefore a running Shopware 6 instance, with full access to all files. This also includes access to the command line to execute a command, which then builds the Storefront. A general understanding of vanilla JavaScript ES6 is also mandatory. Everything else is explained in this guide itself.

## Writing a JavaScript plugin

Storefront JavaScript plugins are vanilla JavaScript ES6 classes that extend from our Plugin base class. For more information, refer to [JavaScript classes](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Classes) section.

The directory to create custom javascript plugins should be the following, which represents the same structure like the core: `<plugin root>/src/Resources/app/storefront/src/`

In there, you create a new directory, named after your plugin. In this guide, this will be called `example-plugin`, so the full path would look like this: `<plugin root>/src/Resources/app/storefront/src/example-plugin`

Now create an actual file for your JavaScript plugin, in this example it will be called `example-plugin.plugin.js`.

Inside this file create and export an ExamplePlugin class that extends the base Plugin class:

```javascript
// <plugin root>/src/Resources/app/storefront/src/example-plugin/example-plugin.plugin.js
const { PluginBaseClass } = window;

export default class ExamplePlugin extends PluginBaseClass {
}
```

This is just a basic vanilla JavaScript ES6 class, which extends the `Plugin` class.

Each plugin has to implement the `init()` method. This method will be called when your plugin gets initialized and is the entrypoint to your custom logic. The plugin initialization runs on `DOMContentLoaded` event, so you can be sure, that the dom is already completely loaded. In your case you add a callback to the `scroll` event from the window and check if the user has scrolled to the bottom of the page. If so we display an alert. Your full plugin now looks like this:

```javascript
// <plugin root>/src/Resources/app/storefront/src/example-plugin/example-plugin.plugin.js
const { PluginBaseClass } = window;

export default class ExamplePlugin extends PluginBaseClass {
    init() {
        window.addEventListener('scroll', this.onScroll.bind(this));
    }

    onScroll() {
        if ((window.innerHeight + window.pageYOffset) >= document.body.offsetHeight) {
            alert('Seems like there\'s nothing more to see here.');
        }
    }
}
```

A short explanation what the condition is doing here: The `window.innerHeight` contains the height of the window, as you might have guessed.

This is added to `window.pageYOffset`, which contains the current scroll position on the Y-axis. It represents the **top** value of the current scroll, which basically means: If your website is 5000px high and you scroll to the very bottom, the value would **not** be 5000px, but rather `5000px - window.innerHeight`. Thus, we have to add up the `innerHeight` to actually get the bottom of the website.

Well, and then we check if this sum is bigger or equal the total size of your website, by fetching the height of your website's `body` tag. If it is higher or equal the total height of the website, you reached the end of the website.

## Registering your plugin

Next you have to tell Shopware that your plugin should be loaded and executed. Therefore you have to register your plugin in the PluginManager.

Shopware is automatically looking for a `main.js` file in a directory `<plugin root>/src/Resources/app/storefront/src`, which then will be loaded automatically. Consider this to be your main storefront JavaScript entrypoint.

Create a `main.js` file inside your `<plugin root>/src/Resources/app/storefront/src` folder and get the PluginManager from the global window object. Then register your own plugin:

```javascript
// <plugin root>/src/Resources/app/storefront/src/main.js
// Import all necessary Storefront plugins
import ExamplePlugin from './example-plugin/example-plugin.plugin';

// Register your plugin via the existing PluginManager
const PluginManager = window.PluginManager;
PluginManager.register('ExamplePlugin', ExamplePlugin);
```

Right now, your plugin will automatically be loaded once you load the website.

## Binding your plugin to the DOM

You can also bind your plugin to a DOM element by providing a css selector:

```javascript
// <plugin root>/src/Resources/app/storefront/src/main.js
// Import all necessary Storefront plugins
import ExamplePlugin from './example-plugin/example-plugin.plugin';

// Register your plugin via the existing PluginManager
const PluginManager = window.PluginManager;
PluginManager.register('ExamplePlugin', ExamplePlugin, '[data-example-plugin]');
```

In this case the plugin just gets executed if the HTML document contains at least one element with the `data-example-plugin` attribute. You can then use `this.el` inside your plugin to access the DOM element your plugin is bound to.

## Registering an async plugin

You can also register an async JS-plugin. Instead of importing a JS-plugin file at the top of your `main.js`, you can provide a dynamic import inside `PluginManager.register()`.
The import path can remain the same as the synchronous import.

```javascript
// <plugin root>/src/Resources/app/storefront/src/main.js

// Register your plugin via the existing PluginManager using a dynamic import
const PluginManager = window.PluginManager;
PluginManager.register('ExamplePlugin', () => import('./example-plugin/example-plugin.plugin'), '[data-example-plugin]');
```

If an async/dynamic import is provided, then the JS-plugin will be recognized as async by the PluginManager automatically.
This means that, the registered JS-plugin will not be included in the main bundled JavaScript (storefront.js) by default. The JS-plugin will only be downloaded on-demand if the plugin selector (`[data-example-plugin]`) is found on the current page, see [Loading your plugin](#loading-your-plugin).

Using an async JS-plugin can be helpful when the plugin is not supposed to be loaded on every page and should only be loaded when it is actually needed. This can reduce the size of the initially loaded JavaScript in the browser.
When using the "normal" import (`import ExamplePlugin from './example-plugin/example-plugin.plugin';`) in comparison, the JS-plugin will always be included in the JavaScript on all pages.

### Loading your plugin

The following will create a new template with a very short explanation. If you're looking for more information on what's going on here, head over to our guide about [Customizing templates](customize-templates).

You bound your plugin to the css selector `[data-example-plugin]`, so you have to add DOM elements with this attribute on the pages you want your plugin to be active.

Create a `<plugin root>/src/Resources/views/storefront/page/content/` folder and create a `index.html.twig` template. Inside this template, extend from the `@Storefront/storefront/page/content/index.html.twig` and overwrite the `base_main_inner` block. After the parent content of the blog, add a template tag that has the `data-example-plugin` attribute.

A lot of text, here is the respective example:

```twig
// <plugin root>/src/Resources/views/storefront/page/content/index.html.twig
{% sw_extends '@Storefront/storefront/page/content/index.html.twig' %}

{% block base_main_inner %}
    {{ parent() }}

    <template data-example-plugin></template>
{% endblock %}
```

With this template extension your plugin is active on every content page, like the homepage or category listing pages.

## Configuring your plugins

You can configure your plugins from inside the templates via data-options. First you have to define a static `options` object inside your plugin and assign your options with default values to it. In your case define a `text` option and as a default value use the text you previously directly prompted to the user. And instead of the hard coded string inside the `alert()`, use your new option value.

```javascript
// <plugin root>/src/Resources/app/storefront/src/example-plugin/example-plugin.plugin.js
const { PluginBaseClass } = window;

export default class ExamplePlugin extends PluginBaseClass {
    static options = {
        /**
         * Specifies the text that is prompted to the user
         * @type string
         */
        text: 'Seems like there\'s nothing more to see here.',
    };

    init() {
        window.addEventListener('scroll', this.onScroll.bind(this));
    }

    onScroll() {
        if ((window.innerHeight + window.pageYOffset) >= document.body.offsetHeight) {
            alert(this.options.text);
        }
    }
}
```

Now you are able to override the text that is prompted to the user from inside your templates. For this example we're going to display another message on product detail pages.

Therefore create a `product-detail` folder inside your `<plugin root>/src/Resources/views/storefront/page` folder and add an `index.html.twig` file inside that folder. In your template extend from the default `@Storefront/storefront/page/product-detail/index.html.twig` and override the block `page_product_detail_content`.

After the parent content add a template tag with the `data-example-plugin` tag to activate your plugin on product detail pages as well. Next add a `data-{your-plugin-name-in-kebab-case}-options` (in this example: `data-example-plugin-options`) attribute to the DOM element you registered your plugin on (the template tag). The value of this attribute are the options you want to override as a JSON object.

```twig
// <plugin root>/src/Resources/views/storefront/page/product-detail/index.html.twig
{% sw_extends '@Storefront/storefront/page/product-detail/index.html.twig' %}

{% set examplePluginOptions = {
    text: "Are you not interested in this product?"
} %}

{% block page_product_detail_content %}
    {{ parent() }}

    <template data-example-plugin data-example-plugin-options='{{ examplePluginOptions|json_encode }}'></template>
{% endblock %}
```

It is best practice to use a variable for the options because this is extendable from plugins.

## Modify existing options

We've just mentioned the best practice to use a template variable for setting plugin options, so other plugins can extend those options. This section will explain how to do actually achieve that.

You can use the `replace_recursive` Twig filter for this case.

Imagine the following example can be found in the core:

```twig
{% set productSliderOptions = {
    productboxMinWidth: sliderConfig.elMinWidth.value ? sliderConfig.elMinWidth.value : '',
    slider: {
        gutter: 30,
        autoplayButtonOutput: false,
        nav: false,
        mouseDrag: false,
        controls: sliderConfig.navigation.value ? true : false,
        autoplay: sliderConfig.rotate.value ? true : false
    }
} %}

{% block element_product_slider_slider %}
    <div class="base-slider"
         data-product-slider="true"
         data-product-slider-options="{{ productSliderOptions|default({})|json_encode|escape('html_attr') }}">
    </div>
{% endblock %}
```

Now you want to overwrite the value `slider.mouseDrag` with your plugin. The variable can be overwritten with `replace_recursive`:

```twig
{% block element_product_slider_slider %}
    {% set productSliderOptions = productSliderOptions|replace_recursive({
        slider: {
            mouseDrag: true
        }
    }) %}

    {{ parent() }}
{% endblock %}
```

## Plugin script path

For JavaScript you normally would have two locations where your `*.js` files are loca

… **Truncated.** Full document: https://developer.shopware.com/docs/v6.6/guides/plugins/plugins/storefront/add-custom-javascript.md


---

## Add Custom Page
**Source:** [guides/plugins/plugins/storefront/add-custom-page.md](https://developer.shopware.com/docs/v6.6/guides/plugins/plugins/storefront/add-custom-page.md)  
# Add Custom Page

## Overview

In this guide you will learn how to create custom page for your Storefront. A page in general consists of a controller, a page loader, a "page loaded" event and a page class, which is like a struct and contains most necessary data for the page.

## Prerequisites

In order to add your own custom page for your plugin, you first need a plugin as base. Therefore, you can refer to the [Plugin Base Guide](../plugin-base-guide). Since you need to load your page with a controller, you might want to have a look at our guide about [creating a controller](add-custom-controller) first. The controller created in the previously mentioned controller guide will also be used in this guide.

## Adding custom page

In the following sections, we'll create each of the necessary classes one by one. The first one will be controller, whose creation is not going to explained here again. Have a look at the guide about [creating a controller](add-custom-controller) to see why it works.

### Creating ExampleController

Let's have a look at an example controller.

```php
// <plugin root>/src/Storefront/Controller/ExampleController.php
<?php declare(strict_types=1);

namespace Swag\BasicExample\Storefront\Controller;

use Shopware\Storefront\Controller\StorefrontController;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\Routing\Attribute\Route;

#[Route(defaults: ['_routeScope' => ['storefront']])]
class ExampleController extends StorefrontController
{
    #[Route(path: '/example-page', name: 'frontend.example.page', methods: ['GET'])]
    public function examplePage(): Response
    {
    }
}
```

It has a method `examplePage`, which is accessible via the route `example-page`. This method will be responsible for loading your page later on, but we'll leave it like that for now.

Don't forget to [register your controller via the DI](add-custom-controller#services-xml-example).

### Creating the pageloader

In order to stick to Shopware's default location for the page loader, we'll have to create a new directory: `<plugin root>/src/Storefront/Page/Example`.

In there, we will proceed to create all page related classes, such as the page loader.

Go ahead and create a new file called `ExamplePageLoader.php`. It's a new service, which doesn't have to extend from any other class. You might want to implement a `ExamplePageLoaderInterface` interface, which is not explained in this guide. You can do that in order to have a decoratable page loader class.

The page loader is responsible for creating your page class instance (`ExamplePage`, will be created in the next section), filling it with data, e.g. from store api, and firing a `PageLoaded` event, so others can react to your page being loaded.
Do not use a repository directly in a page loader. Always get the data for your pages from a store api route instead.

Let's have a look at a full example `ExamplePageLoader`:

```php
// <plugin root>/src/Storefront/Page/Example/ExamplePageLoader.php
<?php declare(strict_types=1);

namespace Swag\BasicExample\Storefront\Page\Example;

use Shopware\Core\System\SalesChannel\SalesChannelContext;
use Shopware\Storefront\Page\GenericPageLoaderInterface;
use Symfony\Component\EventDispatcher\EventDispatcherInterface;
use Symfony\Component\HttpFoundation\Request;

class ExamplePageLoader
{
    private GenericPageLoaderInterface $genericPageLoader;

    private EventDispatcherInterface $eventDispatcher;

    public function __construct(GenericPageLoaderInterface $genericPageLoader, EventDispatcherInterface $eventDispatcher)
    {
        $this->genericPageLoader = $genericPageLoader;
        $this->eventDispatcher = $eventDispatcher;
    }

    public function load(Request $request, SalesChannelContext $context): ExamplePage
    {
        $page = $this->genericPageLoader->load($request, $context);
        $page = ExamplePage::createFrom($page);

        // Do additional stuff, e.g. load more data from store api and add it to page
         $page->setExampleData(...);

        $this->eventDispatcher->dispatch(
            new ExamplePageLoadedEvent($page, $context, $request)
        );

        return $page;
    }
}
```

So first of all, as already mentioned: This is a new class or service, which doesn't have to extend from any other class. The constructor is passed two arguments: The `GenericPageLoaderInterface` and the `EventDispatcherInterface`.

The first one is not necessary, but useful, since it loads all kind of default page stuff, such as a footer and a header and loads some additional helpful data. Once again, you don't have to do that, but if you want your page to have a footer etc., you should add it.

The `EventDispatcherInterface` is of course necessary in order to fire an event later on.

Every page loader should implement a `load` method, which is not mandatory, but convention. You want your page loader to work like all the other page loaders, right? It should return an instance of your example page, in this case `ExamplePage`. Don't worry, we haven't created that one yet, it will be created in the next sections. So, the first thing it does is basically creating a `Page` instance, containing all necessary basic data, such as the footer etc.

Afterwards you're creating your own page instance by using the method `createFrom`. This method is available, since your `ExamplePage` has to extend from the `Page` struct, which in return extends from the `Struct` class. The latter implements the [CreateFromTrait](https://github.com/shopware/shopware/blob/v6.3.4.1/src/Core/Framework/Struct/CreateFromTrait.php) containing this method. In short, this will create an instance of your `ExamplePage`, containing all the data from the generic `Page` object.

Afterwards, you can add more data to your page instance by using a setter. Of course, your example page class then has to have such a setter method, as well as a getter.

As already mentioned, you should also fire an event once your page was loaded. For this case, you need a custom page loaded event class, which is also created in the next sections. It will be called `ExamplePageLoadedEvent`.

The last thing to do in this method is to return your new page instance.

Remember to register your new page loader in the DI container:

```html
// <plugin root>/src/Resources/config/services.xml
<service id="Swag\BasicExample\Storefront\Page\Example\ExamplePageLoader" public="true">
    <argument type="service" id="Shopware\Storefront\Page\GenericPageLoader" />
    <argument type="service" id="event_dispatcher"/>
</service>
```

#### Adjusting the controller

Theoretically, this is all your page loader does - but it's not being used yet. Therefore, you have to inject your page loader to your custom controller and execute the `load` method.

```php
// <plugin root>/src/Storefront/Controller/ExampleController.php
<?php declare(strict_types=1);

namespace Swag\BasicExample\Storefront\Controller;

...

class ExampleController extends StorefrontController
{
    private ExamplePageLoader $examplePageLoader;

    public function __construct(ExamplePageLoader $examplePageLoader)
    {
        $this->examplePageLoader = $examplePageLoader;
    }

    #[Route(path: '/example-page', name: 'frontend.example.page', methods: ['GET'])]
    public function examplePage(Request $request, SalesChannelContext $context): Response
    {
        $page = $this->examplePageLoader->load($request, $context);

        return $this->renderStorefront('@SwagBasicExample/storefront/page/example/index.html.twig', [
            'example' => 'Hello world',
            'page' => $page
        ]);
    }
}
```

Note, that we've added the page to the template variables.

#### Adjusting the services.xml

In addition, it is necessary to pass the argument with the ID of the `ExamplePageLoader` class to the [configuration](add-custom-controller#services-xml-example) of the controller service in the `services.xml`.

```html
// <plugin root>/src/Resources/config/services.xml
<service id="Swag\BasicExample\Storefront\Controller\ExampleController" public="true">
    <argument type="service" id="Swag\BasicExample\Storefront\Page\Example\ExamplePageLoader" />
    <call method="setContainer">
        <argument type="service" id="service_container"/>
    </call>
    <call method="setTwig">
        <argument type="service" id="twig"/>
    </call>
</service>
```

### Creating the example page

So now we're going to create the example page class, that was already used in our page loader, `ExamplePage`.

It has to extend from the `Shopware\Storefront\Page\Page` class in order to contain a field for the header, the footer etc., as well as some helper methods.

Let's have a look at an example:

```php
// <plugin root>/src/Storefront/Page/Example/ExamplePage.php
<?php declare(strict_types=1);

namespace Swag\BasicExample\Storefront\Page\Example;

use Shopware\Storefront\Page\Page;
use Swag\BasicExample\Core\Content\Example\ExampleEntity;

class ExamplePage extends Page
{
    protected ExampleEntity $exampleData;

    public function getExampleData(): ExampleEntity
    {
        return $this->exampleData;
    }

    public function setExampleData(ExampleEntity $exampleData): void
    {
        $this->exampleData = $exampleData;
    }
}
```

As explained in the page loader section, your page can contain all kinds of custom data. It has to provide a getter and a setter for the custom data, so it can be applied and read. In this example, the entity from our guide about [creating custom complex data](../framework/data-handling/add-custom-complex-data#entity-class) is being used.

And that's it already. Your page is ready to go.

### Creating the page loaded event

One more class is missing, the custom event class. It has to extend from the `Shopware\Storefront\Page\PageLoadedEvent` class.

Its constructor parameter will be the `ExamplePage`, which it has to save into a property and there needs to be a getter in order to get the example page instance. Additional constructor parameters are the `Request` and the `SalesChannelContext`, which you have to pass to the parent's constructor.

Here's the example:

```php
// <plugin root>/src/Storefront/Page/Example/ExamplePageLoadedEvent.php
<?php declare(strict_types=1);

namespace Swag\BasicExample\Storefront\Page\Example;

use Shopware\Core\System\SalesChannel\SalesChannelContext;
use Shopware\Storefront\Page\PageLoadedEvent;
use Symfony\Component\HttpFoundation\Request;

class ExamplePageLoadedEvent extends PageLoadedEvent
{
    protected ExamplePage $page;

    public function __construct(ExamplePage $page, SalesChannelContext $salesChannelContext, Request $request)
    {
        $this->page = $page;
        parent::__construct($salesChannelContext, $request);
    }

    public function getPage(): ExamplePage
    {
        return $this->page;
    }
}
```

And that's it for your `ExamplePageLoadedEvent` class.

Your example page should now be fully functioning.

## Next steps

You've now successfully created a whole new page, including a custom controller, a custom template, and the necessary classes to create a new page, a loader, the page struct and the page loaded event.

In your `load` method, you've used the `GenericPageLoader`, which takes care of such a thing as the footer or the header. Those two are so called "pagelets", basically reusable fractions of a page. Learn how to [create a custom pagelet](add-custom-pagelet).

---

---

## Add Custom Pagelet
**Source:** [guides/plugins/plugins/storefront/add-custom-pagelet.md](https://developer.shopware.com/docs/v6.6/guides/plugins/plugins/storefront/add-custom-pagelet.md)  
# Add Custom Pagelet

## Overview

In this guide you will learn how to create custom pagelets for your Storefront pages.

In short: Pages are exactly that, a fully functioning page of your store with a template loaded by a route. A pagelet is an important and reusable fraction of several pages, such as a footer or the navigation.

## Prerequisites

In order to add your own custom pagelet for your plugin, you first need a plugin as base. Therefore, you can refer to the [Plugin Base Guide](../plugin-base-guide). Since a pagelet is just part of another page, we are going to use the page created in our guide about [adding a custom page](add-custom-page).

## Adding custom pagelet

Basically a pagelet is created exactly like a page: You need a pagelet loader, a pagelet struct to hold the data and a pagelet loaded event.

Since creating this kind of classes is explained in detail in our guide about [adding a custom page](add-custom-page), it is not going to be explained here in detail again. Yet, there's some differences worth mentioning:

* The struct to hold the data has to extend from the `Shopware\Storefront\Pagelet\Pagelet` class instead of `Shopware\Storefront\Page\Page`

* A pagelet doesn't have to be bound to a controller, e.g. with an extra route. It can have a route though!

* A pagelet is mostly loaded by another page or multiple pages, that's their purpose

* The `GenericPageLoaderInterface` is not used, since it is responsible to load the footer or header pagelet. You don't want to load

  a pagelet (footer or header) into your pagelet

* The pagelet instance is not created via `Pagelet::createFrom()`, but rather you just create a new instance yourself. That's because the

  `Pagelet::createFrom()` was only necessary to create a new instance of your page, which already contains the footer & header pagelets.

  Once again: You don't want that in your pagelet.

* The pagelet loaded event class extends from `Shopware\Storefront\Pagelet\PageletLoadedEvent` instead of `Shopware\Storefront\Page\PageLoadedEvent`

Let's now have a look at the example classes. The pagelet is going to be called `ExamplePagelet` in the following examples.

### The ExamplePageletLoader

```php
// <plugin root>/src/Storefront/Pagelet/Example/ExamplePageletLoader.php
<?php declare(strict_types=1);

namespace Swag\BasicExample\Storefront\Pagelet\Example;

use Shopware\Core\System\SalesChannel\SalesChannelContext;
use Shopware\Storefront\Page\GenericPageLoaderInterface;
use Symfony\Component\EventDispatcher\EventDispatcherInterface;
use Symfony\Component\HttpFoundation\Request;

class ExamplePageletLoader
{
    private EventDispatcherInterface $eventDispatcher;

    public function __construct(EventDispatcherInterface $eventDispatcher)
    {
        $this->eventDispatcher = $eventDispatcher;
    }

    public function load(Request $request, SalesChannelContext $context): ExamplePagelet
    {
        $pagelet = new ExamplePagelet();

        // Do additional stuff, e.g. load more data from store-api and add it to page
        $pagelet->setExampleData(...);

        $this->eventDispatcher->dispatch(
            new ExamplePageletLoadedEvent($pagelet, $context, $request)
        );

        return $pagelet;
    }
}
```

Note the instance creation without the `::createFrom()` call. The rest is quite equal, you can load your data, set it to the pagelet struct, you fire an event and you return the pagelet.

### The ExamplePagelet struct

```php
// <plugin root>/src/Storefront/Pagelet/Example/ExamplePagelet.php
<?php declare(strict_types=1);

namespace Swag\BasicExample\Storefront\Pagelet\Example;

use Shopware\Storefront\Pagelet\Pagelet;
use Swag\BasicExample\Core\Content\Example\ExampleEntity;

class ExamplePagelet extends Pagelet
{
    protected ExampleEntity $exampleData;

    public function getExampleData(): ExampleEntity
    {
        return $this->exampleData;
    }

    public function setExampleData(ExampleEntity $exampleData): void
    {
        $this->exampleData = $exampleData;
    }
}
```

Just like the page struct, this is basically just a class holding data. Note the different `extend` though, you're not extending from `Shopware\Storefront\Page\Page` here. It only contained helper method for the header & footer pagelets.

### The ExamplePageletLoadedEvent

```php
// <plugin root>/src/Storefront/Pagelet/Example/ExamplePageletLoadedEvent.php
<?php declare(strict_types=1);

namespace Swag\BasicExample\Storefront\Pagelet\Example;

use Shopware\Core\System\SalesChannel\SalesChannelContext;
use Shopware\Storefront\Pagelet\PageletLoadedEvent;
use Symfony\Component\HttpFoundation\Request;

class ExamplePageletLoadedEvent extends PageletLoadedEvent
{
    protected ExamplePagelet $pagelet;

    public function __construct(ExamplePagelet $pagelet, SalesChannelContext $salesChannelContext, Request $request)
    {
        $this->pagelet = $pagelet;
        parent::__construct($salesChannelContext, $request);
    }

    public function getPagelet(): ExamplePagelet
    {
        return $this->pagelet;
    }
}
```

Note the different `extends`, which uses the `PageletLoadedEvent` class instead. Also, the getter method is no longer `getPage`, but `getPagelet` instead.

## Loading the pagelet

### Loading the pagelet via another page

Most times you want to load your pagelet as part of another page. This is simply done by calling the `load` method of your pagelet in another page's `load` method.

Using the example from our [adding a custom page](add-custom-page) guide, this is what the `load` method could look like:

```php
// <plugin root>/src/Storefront/Page/Example/ExamplePageLoader.php
public function load(Request $request, SalesChannelContext $context): ExamplePage
{
    $page = $this->genericPageLoader->load($request, $context);
    $page = ExamplePage::createFrom($page);

    $page->setExamplePagelet($this->examplePageletLoader->load($request, $context));

    // Do additional stuff, e.g. load more data from store-api and add it to page
     $page->setExampleData(...);

    $this->eventDispatcher->dispatch(
        new ExamplePageletLoadedEvent($page, $context, $request)
    );

    return $page;
}
```

Of course, in this example your `ExamplePage` struct needs a method `setExamplePagelet`, as well as the respective getter method `getExamplePagelet`. And then that's it, you've loaded your pagelet as part of another page.

### Loading the pagelet via route

As already mentioned, a pagelet can be loaded via a route if you want it to. For that case, you can simply add a new route to your controller and load the pagelet via the `ExamplePageletLoader`:

```php
#[Route(path: '/example-pagelet', name: 'frontend.example.pagelet', methods: ['POST'], defaults: ['XmlHttpRequest' => 'true'])]
public function examplePagelet(Request $request, SalesChannelContext $context): Response
{
    $pagelet = $this->examplePageletLoader->load($request, $context);

    return $this->renderStorefront('@Storefront/storefront/pagelet/example/index.html.twig', [
        'pagelet' => $pagelet
    ]);
}
```

Using the part `defaults: ['XmlHttpRequest' => true]` in the attribute ensures, that this pagelet can be loaded using an XML HTTP Request.

---

---

## Add Custom Sorting for Product Listing
**Source:** [guides/plugins/plugins/storefront/add-custom-sorting-product-listing.md](https://developer.shopware.com/docs/v6.6/guides/plugins/plugins/storefront/add-custom-sorting-product-listing.md)  
# Add Custom Sorting for Product Listing

## Overview

Individual sortings are groups of sorting options which you can use to sort product listings. The sortings are available in the Storefront.

This guide will show you how to add individual sorting options using a migration (manageable) or at runtime (non-manageable).

## Prerequisites

In order to add your own custom sorting for product listings for your plugin, you first need a plugin as base. Therefore, you can refer to the [Plugin Base Guide](../plugin-base-guide).

You should also have a look at our [Database migrations](../plugin-fundamentals/database-migrations) guide, as we use one in this guide.

## Create individual sorting with migration

In order to make your sorting manageable in the Administration by the user, you will need to migrate the data to the database.

Create a new Migration in your plugin:

::: info
Note: Do not change an existing migration if your plugin is already in use by someone. In that case, create a new Migration instead! This also means, that you have to re-install or update your plugin if you adjust the migration.
:::

```php
// <plugin root>/src/Migration/Migration1615470599ExampleSorting.php
<?php declare(strict_types=1);

namespace Swag\BasicExample\Migration;

use Doctrine\DBAL\Connection;
use Shopware\Core\Content\Product\SalesChannel\Sorting\ProductSortingDefinition;
use Shopware\Core\Defaults;
use Shopware\Core\Framework\Migration\MigrationStep;
use Shopware\Core\Framework\Uuid\Uuid;

class Migration1615470599ExampleSorting extends MigrationStep
{
    public function getCreationTimestamp(): int
    {
        return 1615470599;
    }

    public function update(Connection $connection): void
    {
        $myCustomSorting = [
            'id' => Uuid::randomBytes(),
            'url_key' => 'my-custom-sort',  // shown in url - must be unique system wide
            'priority' => 5,                // the higher the priority, the further upwards it will be shown in the sortings dropdown in Storefront
            'active' => 1,                  // activate / deactivate the sorting
            'locked' => 0,                  // you can lock the sorting here to prevent it from being edited in the Administration
            'fields' => json_encode([
                [
                    'field' => 'product.name',  // field to sort by
                    'order' => 'desc',          // asc or desc
                    'priority' => 1,            // in which order the sorting is to applied (higher priority comes first)
                    'naturalSorting' => 0       // apply natural sorting logic to this field
                ],
                // ... more fields
            ]),
            'created_at' => (new \DateTime())->format(Defaults::STORAGE_DATE_TIME_FORMAT),
        ];

        // insert the product sorting
        $connection->insert(ProductSortingDefinition::ENTITY_NAME, $myCustomSorting);

        // insert the translation for the translatable label
        // if you use multiple languages, you will need to update all of them
        $connection->executeStatement(
            'REPLACE INTO product_sorting_translation
             (`language_id`, `product_sorting_id`, `label`, `created_at`)
             VALUES
             (:language_id, :product_sorting_id, :label, :created_at)',
            [
                'language_id' => Uuid::fromHexToBytes(Defaults::LANGUAGE_SYSTEM),
                'product_sorting_id' => $myCustomSorting['id'],
                'label' => 'My Custom Sorting',
                'created_at' => (new \DateTime())->format(Defaults::STORAGE_DATE_TIME_FORMAT),
            ]
        );
    }

    public function updateDestructive(Connection $connection): void
    {
    }
}
```

## Create individual sorting at runtime

You can subscribe to the `ProductListingCriteriaEvent` to add a `ProductSortingEntity` as available sorting on the fly. If you don't know how to do this, head over to our [Listening to events](../plugin-fundamentals/listening-to-events) guide.

::: info
While possible, it is not recommended adding an individual sorting at runtime. If you just wish for your individual sorting to be not editable by users in the Administration, create a migration and set the parameter `locked` to be `true`.
:::

Here's an example how your subscriber could look like:

```php
// <plugin root>/src/Subscriber/ExampleListingSubscriber.php
<?php declare(strict_types=1);

namespace Swag\BasicExample\Subscriber;

use Shopware\Core\Content\Product\Events\ProductListingCriteriaEvent;
use Shopware\Core\Content\Product\SalesChannel\Sorting\ProductSortingCollection;
use Shopware\Core\Content\Product\SalesChannel\Sorting\ProductSortingEntity;
use Shopware\Core\Framework\Uuid\Uuid;
use Symfony\Component\EventDispatcher\EventSubscriberInterface;

class ExampleListingSubscriber implements EventSubscriberInterface
{

    public static function getSubscribedEvents(): array
    {
        return [
            // be sure to subscribe with high priority to add you sorting before the default shopware logic applies
            // otherwise storefront will throw a ProductSortingNotFoundException
            ProductListingCriteriaEvent::class => ['addMyCustomSortingToStorefront', 500],
        ];
    }

    public function addMyCustomSortingToStorefront(ProductListingCriteriaEvent $event): void
    {
        /** @var ProductSortingCollection $availableSortings */
        $availableSortings = $event->getCriteria()->getExtension('sortings') ?? new ProductSortingCollection();

        $myCustomSorting = new ProductSortingEntity();
        $myCustomSorting->setId(Uuid::randomHex());
        $myCustomSorting->setActive(true);
        $myCustomSorting->setTranslated(['label' => 'My Custom Sorting at runtime']);
        $myCustomSorting->setKey('my-custom-runtime-sort');
        $myCustomSorting->setPriority(5);
        $myCustomSorting->setFields([
            [
                'field' => 'product.name',
                'order' => 'desc',
                'priority' => 1,
                'naturalSorting' => 0,
            ],
        ]);

        $availableSortings->add($myCustomSorting);

        $event->getCriteria()->addExtension('sortings', $availableSortings);
    }
}
```

## Next steps

To [add a custom filter](add-listing-filters) to your listing in the Storefront head over to the corresponding guide.

---

---

## Add Custom Styling
**Source:** [guides/plugins/plugins/storefront/add-custom-styling.md](https://developer.shopware.com/docs/v6.6/guides/plugins/plugins/storefront/add-custom-styling.md)  
# Add Custom Styling

## Overview

Quite often your plugin will have to change a few templates for the Storefront. Those might require custom styling to look neat, which will be explained in this guide.

## Prerequisites

You won't learn to create a plugin in this guide, head over to our [Plugin base guide](../plugin-base-guide) to create a plugin first, if you don't know how it is done yet. Also knowing and understanding [SCSS](https://sass-lang.com/documentation) will be quite mandatory to fully understand what is going on here.

Other than having those two requirements, nothing else is necessary for this guide.

## Adding (S)CSS files

By default, Shopware 6 is looking for a `base.scss` file in your plugin. To be precise, this file has to be inside the directory `<plugin root>/src/Resources/app/storefront/src/scss` in order to be properly found and loaded by Shopware.

So just try it out, create a `base.scss` file in the directory mentioned above.

Inside of the `.scss` file, we add some basic styles to see if it's actually working. In this example, the background of the `body` will be changed.

```css
// <plugin root>/src/Resources/app/storefront/src/scss/base.scss
body {
    background: blue;
}
```

### Adding variables

In case you want to use the same color in several places, but want to define it just one time, you can use variables for this.

Create a `abstract/variables.scss` file inside your `<plugin root>/src/Resources/app/storefront/src/scss` directory and define your background color variable.

```css
// <plugin root>/src/Resources/app/storefront/src/scss/abstract/variables.scss
// in variables.scss
$sw-storefront-assets-color-background: blue;
```

Inside your `base.scss` file you can now import your previously defined variables and use them:

```css
// <plugin root>/src/Resources/app/storefront/src/scss/base.scss
@import 'abstract/variables.scss';

body {
    background: $sw-storefront-assets-color-background;
}
```

This comes with the advantage that when you want to change this color for all occurrences, you only have to change this variable once and the hard coded values are not cluttered all over the codebase.

::: info
Refer to the theme guide **[Override Bootstrap Variables in a Theme](../../themes/override-bootstrap-variables-in-a-theme.html)** if you want to override some of the default Shopware variables.
:::

### Testing its functionality

Now you want to test if your custom styles actually apply to the Storefront. For this, you have to execute the compiling and building of the `.scss` files first. This is done by using the following command:

```bash
./bin/build-storefront.sh
```

```bash
composer run build:js:storefront
```

If you want to see all style changes made by you live, you can also use our Storefront hot-proxy for that case:

```bash
./bin/watch-storefront.sh
```

```bash
composer run watch:storefront
```

Using the hot-proxy command, you will have to access your store with the port `9998`, e.g. `domainToYourEnvironment.in:9998`.

That's it! Open the Storefront and see it turning blue due to your custom styles!

---

---

## Add Custom Twig Functions
**Source:** [guides/plugins/plugins/storefront/add-custom-twig-function.md](https://developer.shopware.com/docs/v6.6/guides/plugins/plugins/storefront/add-custom-twig-function.md)  
# Add Custom Twig Functions

## Overview

Let us consider, for instance, you want to call a PHP script from the twig template during the theme development to create a `MD5-hash`. In such a case, you can create your own twig functions. For this example, pass a string to the `TwigFunction` and return a `MD5-Hash`.

::: info
It is not recommended to use twig functions in order to retrieve data from the database. In such a case, DataResolver could come in handy.
:::

## Prerequisites

In order to create your own twig function for your plugin, you first need a plugin as base. Therefore, you can refer to the [Plugin Base Guide](../plugin-base-guide).

## Creating twig function

In the following sections, we will create and expand all necessary files for the twig function to work. There are two such files:

* PHP file with the twig functions itself and
* Services.xml

### Creating the twig function

For clarity, create a folder named `Twig` within the `src` folder. Then create a new php file with desired file name within the `Twig` folder. Refer to the below example :

```php
// <plugin root>/src/Twig/SwagCreateMd5Hash.php
<?php declare(strict_types=1);

namespace SwagBasicExample\Twig;

use Shopware\Core\Framework\Context;
use Twig\Extension\AbstractExtension;
use Twig\TwigFunction;

class SwagCreateMd5Hash extends AbstractExtension
{
    public function getFunctions()
    {
        return [
            new TwigFunction('createMd5Hash', [$this, 'createMd5Hash']),
        ];
    }

    public function createMd5Hash(string $str)
    {
        return md5($str);
    }
}
```

Of course, you can do everything in the `createMd5Hash` function that PHP can do, but the `service.xml` handles registration of the service in the DI container.

```html
// <plugin root>/src/Resources/config/services.xml
...
    <services>
        <service id="SwagBasicExample\Twig\SwagCreateMd5Hash" public="true">
            <tag name="twig.extension"/> <!--Required-->
        </service>
    </services>
...
```

Once done, you can access this `TwigFunction` within your plugin.

### Use twig function in template

The created function is now available in all your templates. You can call it like each other function.

```twig
{% sw_extends '@Storefront/storefront/layout/header/header.html.twig' %}

{% set md5Hash = createMd5Hash('Shopware is awesome') %}

{% block layout_header_logo %}
    {{ parent() }}

    {{ md5Hash }}
{% endblock %}
```

---

---

## Add Data to Storefront Page
**Source:** [guides/plugins/plugins/storefront/add-data-to-storefront-page.md](https://developer.shopware.com/docs/v6.6/guides/plugins/plugins/storefront/add-data-to-storefront-page.md)  
# Add Data to Storefront Page

## Overview

Pages or pagelets are the objects that get handed to the templates and provide all necessary information for the template to render.

If you make template changes you probably want to display some data that is currently not available in the page.
In this case you will have to listen on the page loaded event and then load the additional data and add it to the page object.
This guide will show you how to achieve this, by adding the total number of active products to the footer pagelet and displaying them in the Storefront.

## Prerequisites

This guide is built upon our [Plugin base guide](../plugin-base-guide), so keep that in mind.

Also the following knowledge is necessary, even though some of them are covered here as well:

* Knowing how to [listen to events by using a subscriber](../plugin-fundamentals/listening-to-events)
* Knowing how to [customize storefront templates](customize-templates)
* Knowing how to [read data using our data abstraction layer](../framework/data-handling/reading-data)
* Knowing how to [add a store-api route](../framework/store-api/add-store-api-route)

## Adding data to the Storefront

The workflow you need here was already described in the overview:

1. Figure out which page you want to change
2. Register to the event that this page is firing
3. Add a store-api route for your needed data
4. Add data to the page via the event
5. Display this data in the Storefront

### Subscribe to an event

So first of all, you need to know which page or pagelet you actually want to extend.
In this example, we're going to extend the [FooterPagelet](https://github.com/shopware/shopware/blob/trunk/src/Storefront/Pagelet/Footer/FooterPagelet.php).
All pages or pagelets throw `Loaded` events and this is the right event to subscribe to if you want to add data to the page or pagelet.
In our case we want to add data to the `FooterPagelet` so we need to subscribe to the `FooterPageletLoadedEvent`.

```php
// SwagBasicExample/src/Service/AddDataToPage.php
<?php declare(strict_types=1);

namespace Swag\BasicExample\Service;

use Shopware\Storefront\Pagelet\Footer\FooterPageletLoadedEvent;
use Symfony\Component\EventDispatcher\EventSubscriberInterface;

class AddDataToPage implements EventSubscriberInterface
{
    public static function getSubscribedEvents(): array
    {
        return [
            FooterPageletLoadedEvent::class => 'addActiveProductCount'
        ];
    }

    public function addActiveProductCount(FooterPageletLoadedEvent $event): void
    {

    }
}
```

The next thing we need to do is register our subscriber in the DI-Container and tag it as an event subscriber:

```xml
// Resources/config/services.xml
<?xml version="1.0" ?>
<service id="Swag\BasicExample\Service\AddDataToPage" >
    <tag name="kernel.event_subscriber" />
</service>
```

### Adding data to the page

Now that we have registered our Subscriber to the right event, we first need to fetch the additional data we need and then add it as an extension to the pagelet.

Because we are in an event of a Pagelet we should not directly call the DAL to fetch the data. Instead we should check if there is a proper store-api route to fetch our data.
If we just wanted to add specific products data we could use the ProductListRoute. But we want to fetch data that is currently not returned in a performant way with the store-api.
The ProductListRoute could return the data but it would return way to much data for our purpose. Because of that we will add a new store-api route for our data.

First you should read our guide for [adding store-api routes](../framework/store-api/add-store-api-route).

Our new Route should look like this:

```php
<?php declare(strict_types=1);

namespace Swag\BasicExample\Core\Content\Example\SalesChannel;

use Shopware\Core\Framework\DataAbstractionLayer\Search\Criteria;
use Shopware\Core\System\SalesChannel\SalesChannelContext;
use Symfony\Component\Routing\Attribute\Route;

#[Route(defaults: ['_routeScope' => ['store-api']])]
abstract class AbstractProductCountRoute
{
    abstract public function getDecorated(): AbstractProductCountRoute;

    abstract public function load(Criteria $criteria, SalesChannelContext $context): ProductCountRouteResponse;
}
```

```php
<?php declare(strict_types=1);

namespace Swag\BasicExample\Core\Content\Example\SalesChannel;

use Shopware\Core\Framework\DataAbstractionLayer\EntityRepository;
use Shopware\Core\Framework\DataAbstractionLayer\Search\Criteria;
use Shopware\Core\Framework\DataAbstractionLayer\Search\Aggregation\Metric\CountAggregation;
use Shopware\Core\Framework\DataAbstractionLayer\Search\AggregationResult\Metric\CountResult;
use Shopware\Core\Framework\Plugin\Exception\DecorationPatternException;
use Shopware\Core\System\SalesChannel\SalesChannelContext;
use Shopware\Core\Framework\DataAbstractionLayer\Search\Filter\EqualsFilter;
use Symfony\Component\Routing\Attribute\Route;

#[Route(defaults: ['_routeScope' => ['store-api']])]
class ProductCountRoute extends AbstractProductCountRoute
{
    protected EntityRepository $productRepository;

    public function __construct(EntityRepository $productRepository)
    {
        $this->productRepository = $productRepository;
    }

    public function getDecorated(): AbstractProductCountRoute
    {
        throw new DecorationPatternException(self::class);
    }

     #[Route(path: '/store-api/get-active-product-count', name: 'store-api.product-count.get', methods: ['GET', 'POST'], defaults: ['_entity' => 'product'])]
    public function load(Criteria $criteria, SalesChannelContext $context): ProductCountRouteResponse
    {
        $criteria = new Criteria();
        $criteria->addFilter(new EqualsFilter('product.active', true));
        $criteria->addAggregation(new CountAggregation('productCount', 'product.id'));

        /** @var CountResult $productCountResult */
        $productCountResult = $this->productRepository
            ->aggregate($criteria, $context->getContext())
            ->get('productCount');
            
        return new ProductCountRouteResponse($productCountResult);
    }
}
```

### Register route class

```xml
<?xml version="1.0" ?>
<container xmlns="http://symfony.com/schema/dic/services"
           xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
           xsi:schemaLocation="http://symfony.com/schema/dic/services http://symfony.com/schema/dic/services/services-1.0.xsd">

    <services>
        <service id="Swag\BasicExample\Core\Content\Example\SalesChannel\ProductCountRoute" >
            <argument type="service" id="product.repository"/>
        </service>
    </services>
</container>
```

The routes.xml according to our guide for [adding store-api routes](../framework/store-api/add-store-api-route) should look like this.

```xml
<?xml version="1.0" encoding="UTF-8" ?>
<routes xmlns="http://symfony.com/schema/routing"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:schemaLocation="http://symfony.com/schema/routing
        https://symfony.com/schema/routing/routing-1.0.xsd">

    <import resource="../../Core/**/*Route.php" type="attribute" />
</routes>
```

### ProductCountRouteResponse

The RouteResponse according to our guide for [adding store-api routes](../framework/store-api/add-store-api-route) should look like this

```php
<?php declare(strict_types=1);

namespace Swag\BasicExample\Core\Content\Example\SalesChannel;

use Shopware\Core\Framework\DataAbstractionLayer\Search\AggregationResult\Metric\CountResult;
use Shopware\Core\System\SalesChannel\StoreApiResponse;

/**
 * Class CountResult
 * @property CountResult $object
 */
class ProductCountRouteResponse extends StoreApiResponse
{
    public function __construct(CountResult $countResult)
    {
        parent::__construct($countResult);
    }

    public function getProductCount(): CountResult
    {
        return $this->object;
    }
}
```

So you should know and understand the first few lines if you have read our guide about [Reading data](../framework/data-handling/reading-data) first.
Make sure to also understand the usage of aggregations, since this is what is done here.
The only main difference you might notice is, that we're using the `aggregate()` method instead of the `search()` method.
This will not actually search for any products and return the whole products dataset, but rather just the aggregated data, nothing else.

```php
<?php declare(strict_types=1);

namespace Swag\BasicExample\Service;

use Shopware\Core\Content\Product\SalesChannel\ProductCountRoute;
use Shopware\Core\Framework\DataAbstractionLayer\Search\Criteria;
use Shopware\Storefront\Pagelet\Footer\FooterPageletLoadedEvent;
use Symfony\Component\EventDispatcher\EventSubscriberInterface;

class AddDataToPage implements EventSubscriberInterface
{
    private ProductCountRoute $productCountRoute;

    public function __construct(ProductCountRoute $productCountRoute)
    {
        $this->productCountRoute = $productCountRoute;
    }

    public static function getSubscribedEvents(): array
    {
        return [
            FooterPageletLoadedEvent::class => 'addActiveProductCount'
        ];
    }

    public function addActiveProductCount(FooterPageletLoadedEvent $event): void
    {
        $productCountResponse = $this->productCountRoute->load(new Criteria(), $event->getSalesChannelContext());

        $event->getPagelet()->addExtension('product_count', $productCountResponse->getProductCount());
    }
}
```

The first line should be nothing new as it is only the call for the store-api route, we created.
Completely new should only be the last line: `$event->getPagelet()->addExtension('product_count', $productCountResult);`

Basically what you're doing here, is to fetch the actual pagelet instance from the event and add the data to the template.
This data will then be available via the name `product_count`, but we'll get to that in the next section.

Now you only have to adjust your service definition to inject the productCountRoute:

```xml
<?xml version="1.0" ?>
<container xmlns="http://symfony.com/schema/dic/services"
           xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
           xsi:schemaLocation="http://symfony.com/schema/dic/services http://symfony.com/schema/dic/services/services-1.0.xsd">

    <services>
        <service id="Swag\BasicExample\Core\Content\Example\SalesChannel\ProductCountRoute" public="true">
            <argument type="service" id="product.repository"/>
        </service>
        
        <service id="Swag\BasicExample\Service\AddDataToPage" >
            <argument type="service" id="Swag\BasicExample\Core\Content\Example\SalesChannel\ProductCountRoute"/>
            <tag name="kernel.event_subscriber" />
        </service>
    </services>
</container>
```

### Displaying the data in the Storefront

To display the additional data we need to override the footer template and render the data.
Refer to the respective section of this guide for detailed information on how to [extend templates and override blocks](customize-templates).

For our case we extend the footer template and add a new column to the navigation block:

```twig
// Resources/views/storefront/layout/footer/footer.html.twig
{% sw_extends '@Storefront/storefront/layout/footer/footer.html.twig' %}

{% block layout_footer_navigation_columns %}
    {{ parent() }}

    {% if page.footer.extensions.product_count %}
        <div class="col-md-4 footer-column">
            <p>This shop offers you {{ page.footer.extensions.product_count.count }} products</p>
        </div>
    {% endif %}
{% endblock %}
```

Note the usage of the variable here. You're accessing the footer object, in which you can now find the path `extensions.product_count.count`.

That's it for this guide, you've successfully added data to a Storefront page(let).

---

---

## Add Dynamic Content via AJAX Calls
**Source:** [guides/plugins/plugins/storefront/add-dynamic-content-via-ajax-calls.md](https://developer.shopware.com/docs/v6.6/guides/plugins/plugins/storefront/add-dynamic-content-via-ajax-calls.md)  
# Add Dynamic Content via AJAX Calls

## Overview

This guide will show you how to add dynamic content to your Storefront. It combines and builds upon the the guides about [adding custom Javascript](add-custom-javascript) and [adding a custom controller](add-custom-controller), so you should probably read them first.

## Setting up the Controller

For this guide we will use a very simple controller that returns a timestamp wrapped in the JSON format.

::: info
Refer to this video on **[Creating a JSON controller](https://www.youtube.com/watch?v=VzREUDdpZ3E)** dealing with the creation of a controller that returns JSON data. Also available on our free online training ["Shopware 6 Backend Development"](https://academy.shopware.com/courses/shopware-6-backend-development-with-jisse-reitsma).
:::

As mentioned before this guide builds up upon the [adding a custom controller](add-custom-controller) guide. This means that this article will only cover the differences between returning a template and a `JSON` response and making it accessible to `XmlHttpRequests`.

```php
// <plugin base>/Storefront/Controller/ExampleController.php
<?php declare(strict_types=1);

namespace SwagBasicExample\Storefront\Controller;

use Shopware\Storefront\Controller\StorefrontController;
use Symfony\Component\HttpFoundation\JsonResponse;
use Symfony\Component\Routing\Attribute\Route;

#[Route(defaults: ['_routeScope' => ['storefront']])]
class ExampleController extends StorefrontController
{
    #[Route(path: '/example', name: 'frontend.example.example', methods: ['GET'], defaults: ['XmlHttpRequest' => 'true'])]
    public function showExample(): JsonResponse
    {
        return new JsonResponse(['timestamp' => (new \DateTime())->format(\DateTimeInterface::W3C)]);
    }
}
```

As you might have seen this controller isn't too different from the controller used in the article mentioned before. The route attribute has an added `defaults: ['XmlHttpRequest' => true]` to allow XmlHttpRequest and it returns a `JsonResponse` instead of a normal `Response`. Using a `JsonResponse` instead of a normal `Response` causes the data structures passed to it to be automatically turned into a `JSON` string.

The following `services.xml` and `routes.xml` are identical as in the before mentioned article, but here they are for reference anyways:

```xml
// <plugin root>/src/Resources/config/services.xml
<?xml version="1.0" ?>

<container xmlns="http://symfony.com/schema/dic/services" 
           xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
           xsi:schemaLocation="http://symfony.com/schema/dic/services http://symfony.com/schema/dic/services/services-1.0.xsd">

    <services>
        <service id="SwagBasicExample\Storefront\Controller\ExampleController" public="true">
            <call method="setContainer">
                <argument type="service" id="service_container"/>
            </call>
            <call method="setTwig">
              <argument type="service" id="twig"/>
            </call>
        </service>
    </services>
</container>
```

```xml
// <plugin root>/src/Resources/config/routes.xml
<?xml version="1.0" encoding="UTF-8" ?>
<routes xmlns="http://symfony.com/schema/routing"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:schemaLocation="http://symfony.com/schema/routing
        https://symfony.com/schema/routing/routing-1.0.xsd">

    <import resource="../../Storefront/Controller/**/*Controller.php" type="attribute" />
</routes>
```

## Preparing the Plugin

Now we have to add a `Storefront Javascript plugin` to display the timestamp we get from our controller.

Again this is built upon the [adding custom Javascript](add-custom-javascript) article, so if you don't already know what Storefront `plugins` are, hold on and read it first.

```javascript
// <plugin root>/src/Resources/app/storefront/src/example-plugin/example-plugin.plugin.js
const { PluginBaseClass } = window;

export default class AjaxLoadPlugin extends PluginBaseClass {
    init() {
        this.button = this.el.children['ajax-button'];
        this.textdiv = this.el.children['ajax-display'];

        this._registerEvents();
    }

    _registerEvents() {
        // fetch the timestamp, when the button is clicked
        this.button.onclick = this._fetch.bind(this);
    }

    async _fetch() {
        const response = await fetch('/example');
        const data = await response.json();
        this.textdiv.innerHTML = data.timestamp;
    }
}
```

and register it in the `main.js`

```javascript
import AjaxLoadPlugin from './example-plugin/example-plugin.plugin';

window.PluginManager.register('AjaxLoadPlugin', AjaxLoadPlugin, '[data-ajax-helper]');
```

## Adding the Template

The only thing that is now left, is to provide a template for the Storefront plugin to hook into:

```twig
// <plugin root>/src/Resources/views/storefront/page/content/index.html.twig
{% sw_extends '@Storefront/storefront/page/content/index.html.twig' %}

{% block cms_content %}
    <div>
        <h1>Swag AJAX Example</h1>

        <div data-ajax-helper>
            <div id="ajax-display"></div>
            <button id="ajax-button">Button</button>
        </div>
    </div>
{% endblock %}
```

## Next steps

The controller we used in this example doesn't do a lot, but this pattern of providing and using data is generally the same. Even if you use it to fetch data form the database, but in that case you probably want to learn more about the [DAL](../../../../concepts/framework/data-abstraction-layer).

---

---

## Add Custom Icons
**Source:** [guides/plugins/plugins/storefront/add-icons.md](https://developer.shopware.com/docs/v6.6/guides/plugins/plugins/storefront/add-icons.md)  
# Add Custom Icons

## Overview

In this guide you will learn how to use the icon renderer component as well as adding custom icons.

::: info
Even if this is originally a plugin guide, everything will work perfectly in a theme as well. Actually, a theme even is a kind of plugin. So don't get confused by us talking about plugins here.
:::

## Prerequisites

In order to follow this guide easily, you first need to have a functioning plugin installed. Head over to our [Plugin base guide](../plugin-base-guide) to create a plugin, if you don't know how it's done yet. Also knowing and understanding SCSS will be quite mandatory to fully understand what's going on here. Furthermore, it might be helpful to read the guide on how to [handle own assets](add-custom-assets) in your plugin before you start with this one.

## Adding icon

In order to add any icons to the Storefront, you use our `sw_icon` twig action. This way, an icon of choice is displayed in the Storefront.

Needless to say, the first step is saving your image somewhere in your plugin where Shopware can find it. The default path for icons is the following:

```text
<YourPlugin>/src/Resources/app/storefront/dist/assets/icon/default
`
```

You can also provide "solid" icons or any other custom pack names which can be configured later with the `pack` parameter. You can do that by creating a folder with the pack name:

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
When you want to see all icons available to the Storefront by default, see [here](https://github.com/shopware/shopware/tree/trunk/src/Storefront/Resources/app/storefront/dist/assets/icon). They are available as `default` and `solid` icon pack.
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
| `color` | Sets the color of the icon | --- |
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

Inside your theme, you cannot put an icon in a directory corresponding the core folder structure and expect the core one to be automatically overwritten by it, as you are used to with themes in general.

---

---

## Add JavaScript as script tag
**Source:** [guides/plugins/plugins/storefront/add-javascript-as-script-tag.md](https://developer.shopware.com/docs/v6.6/guides/plugins/plugins/storefront/add-javascript-as-script-tag.md)  
# Add JavaScript as script tag

## Overview

You often want to add your JavaScript to your main entry point `<plugin root>/src/Resources/app/storefront/src/main.js` to automatically compile it alongside the Storefront JavaScript.
Please refer to [Add custom Javascript](add-custom-javascript.md) for more information.

However, you might want to add JavaScript as a separate `<script>` tag in the HTML. For example, to load a script from an external CDN.
You will learn how to extend the template to add a `<script>` tag.

## Prerequisites

For this guide, you need a running plugin, Shopware 6 instance, and full access to all files. You also need a brief understanding of how a [template extension](customize-templates.md) works.

## Adding JavaScript as a separate script tag

You can extend the default template that includes the `<head>` section of the page: `src/Storefront/Resources/views/storefront/layout/meta.html.twig`.
While it is possible to add a `<script>` anywhere in the HTML via template extensions, it is recommended to include your script alongside the default scripts by extending the block `layout_head_javascript_hmr_mode`.

```twig
{# <plugin root>/src/Resources/views/storefront/layout/meta.html.twig #}
{% sw_extends '@Storefront/storefront/layout/meta.html.twig' %}

{% block layout_head_javascript_hmr_mode %}
    {# Renders Storefront script: <script src="https://your-shop.example/theme/747e1c6a73cf4d70f5e831b30554dd15/js/all.js?1698139296" defer></script> #}
    {{ parent() }}

    {# Your script #}
    <script src="https://unpkg.com/isotope-layout@3/dist/isotope.pkgd.min.js" defer></script>
{% endblock %}
```

This will render:

```html
<head>
    <!-- Other tags are rendered here... -->

    <script src="https://your-shop.example/theme/747e1c6a73cf4d70f5e831b30554dd15/js/all.js?1698139296" defer></script>
    <script src="https://unpkg.com/isotope-layout@3/dist/isotope.pkgd.min.js" defer></script>
</head>
```

::: danger
If you are extending the block `layout_head_javascript_hmr_mode` to add your script, you must always use the {{ parent() }} function to render the Storefront JavaScript as well.
Otherwise, the core JS functionalities of the Storefront will be overwritten and will stop working. This should only happen when you **explicitly** want this.
:::

### Conditional scripts

Instead of continually rendering your `<script>`, you can also put it behind a condition in Twig.
Then the script will only be rendered when the Twig condition is met.

```twig
{# <plugin root>/src/Resources/views/storefront/layout/meta.html.twig #}
{% sw_extends '@Storefront/storefront/layout/meta.html.twig' %}

{% block layout_head_javascript_hmr_mode %}
    {{ parent() }}

    {# Only add script when condition is met #}
    {% if someCondition %}
        <script src="https://unpkg.com/isotope-layout@3/dist/isotope.pkgd.min.js" defer></script>
    {% endif %}
{% endblock %}
```

### Script order

Should your `<script>` tag come before or after the Storefront core JavaScript?
It depends on whether you need to have access to the code added by your `<script>` within the Storefront JavaScript (added by `<plugin root>/src/Resources/app/storefront/src/main.js`).

* If you **don't** need access within the Storefronts JavaScript, you should add the `<script>` **after** the Storefront JavaScript.
* If you **do need** access, your `<script>` should come **before** the Storefront JavaScript.

::: warning
Please consider that non-async `<script src="#">` that are added before the Storefront JavaScript will postpone its execution.
Too many scripts can have a negative effect on the shop's performance.
:::

### Script loading behavior

Using the `defer` attribute is recommended to tell the browser that the script is meant to be executed after the document has been parsed.
However, if you add a library as `<script>`, please consult the library documentation. Some libraries are supposed to be loaded with `async` attribute.

::: warning
It should be avoided to add external `<script src="#">` without `defer` or `async` because it will block rendering of the site until the script is executed.
This can have a negative effect on the shop's performance.
:::

### Alternative script locations

You can also add a `<script>` near the body using block `base_body_script` in `src/Storefront/Resources/views/storefront/base.html.twig`.
It is possible to add `<script>` at every location the Twig blocks offer.

::: info
Alternative script locations should only be used when there is a technical reason.
For example, when the documentation of an external library recommends a specific script location inside the HTML.
:::

---

---

## Add Custom Listing Filters
**Source:** [guides/plugins/plugins/storefront/add-listing-filters.md](https://developer.shopware.com/docs/v6.6/guides/plugins/plugins/storefront/add-listing-filters.md)  
# Add Custom Listing Filters

## Overview

In an online shop, filters are an important feature. So you might use filters in your custom plugin. This guide will get you covered on how to implement your own, custom filters in Shopware's Storefront.

## Prerequisites

Before you start reading this guide, make sure you got an own plugin installed to work with. If you need a starting point for that, see this guide:

## Create new Filter

At first, you need to create a subscriber. In this example, we will call it `ExampleListingSubscriber`. If you are not sure on working with subscribers, please refer to the guide on working with events in Shopware:

As usual, we will start by creating this new class in the same path as you're seeing in Shopware's core - `/src/Subscriber/ExampleListingSubscriber.php`.

New listing filters, e.g. for your product listing, can be registered via the event `\Shopware\Core\Content\Product\Events\ProductListingCollectFilterEvent` This event was introduced to enable every developer to specify the metadata for a filter. The handling, meaning if and how a filter is added, is done by Shopware's core:

```php
    public static function getSubscribedEvents(): array
    {
        return [
            ProductListingCollectFilterEvent::class => 'addFilter'
        ];
    }
```

After that, you can start to actually add your custom filters. Arguably an important step is to define your filter. Therefore, you're able to use the `Filter` class, including the parameters below:

| Parameter | Description |
| :--- | :--- |
| `name` | Unique name of the filter |
| `filtered` | Set this option to `true` if this filter is active |
| `aggregations` | Defines aggregations behind a filter. Sometimes a filter contains multiple aggregations like properties |
| `filter` | Sets the DAL filter which should be added to the criteria |
| `values` | Defines the values which will be added as `currentFilter` to the result |
| `exclude` | Configure exclusions |

As a result, an example filter could look like this:

```php
$filter = new Filter(
    // name
    'manufacturer',

    // filtered
    !empty($ids),

    // aggregations
    [new EntityAggregation('manufacturer', 'product.manufacturerId', 'product_manufacturer')],

    // filter
    new EqualsAnyFilter('product.manufacturerId', $ids),

    // values
    $ids
);
```

Inside the `ProductListingCollectFilterEvent`, you get the existing filters, can define your new custom filters and merge them into the existing ones. Here is a complete example implementation, adding a filter on the product information `isCloseout`. Please note the comments for explanation:

```php
// <plugin root>/src/Subscriber/ExampleListingSubscriber.php
class ExampleListingSubscriber implements EventSubscriberInterface
{
    // register event
    public static function getSubscribedEvents(): array
    {
        return [
            ProductListingCollectFilterEvent::class => 'addFilter'
        ];
    }

    public function addFilter(ProductListingCollectFilterEvent $event): void
    {
        // fetch existing filters
        $filters = $event->getFilters();
        $request = $event->getRequest();

        $filtered = (bool) $request->get('isCloseout');

        $filter = new Filter(
            // unique name of the filter
            'isCloseout',

            // defines if this filter is active
            $filtered,

            // Defines aggregations behind a filter. A filter can contain multiple aggregations like properties
            [
                new FilterAggregation(
                    'active-filter',
                    new MaxAggregation('active', 'product.isCloseout'),
                    [new EqualsFilter('product.isCloseout', true)]
                ),
            ],

            // defines the DAL filter which should be added to the criteria   
            new EqualsFilter('product.isCloseout', true),

            // defines the values which will be added as currentFilter to the result
            $filtered
        );

        // Add your custom filter
        $filters->add($filter);
    }
}
```

## Add your filter to the Storefront UI

Well, fine - you successfully created a filter via subscriber. However, you want to enable your shop customer to use it, right? Now you need to integrate your filter in the Storefront. Let's start by searching the template file you need to extend in Shopware's Storefront. It's this one - `src/Storefront/Resources/views/storefront/component/listing/filter-panel.html.twig`.

In this template, the existing filters are contained in the block `component_filter_panel_items`. We are going to extend this block with our new filter. If you're not sure on how to customize templates in the Storefront, we got you covered with another guide:

::: info
The block `component_filter_panel_items` is available from Shopware Version 6.4.8.0
:::

Including our filter will be done as seen below, please take the comments into account:

```twig
// <plugin root>/src/Resources/views/storefront/component/listing/filter-panel.html.twig
{% sw_extends '@Storefront/storefront/component/listing/filter-panel.html.twig' %}

{% block component_filter_panel_items %}
    {{ parent() }}

    {# We'll include our filter element here #}
    {% sw_include '@Storefront/storefront/component/listing/filter/filter-boolean.html.twig' with {
        name: 'isCloseout',
        displayName: 'Closeout'
    } %}
{% endblock %}
```

As we want to filter a boolean value, we choose the `filter-boolean` component here. Sure, there are some more you can use - dependent on your filter's values:

| Name | Description |
| :--- | :--- |
| `filter-boolean` | A filter to display boolean values |
| `filter-multi-select` | Filters with multiple values |
| `filter-property-select` | A filter tailored specifically for properties |
| `filter-range` | Displays a range which can be used for filtering |
| `filter-rating-select` and `filter-rating-select-item` | Filter component for rating |

Extending  `component_filter_panel_items` as shown above puts our filter *after* the already existing ones. We could put it at the beginning by moving the `parent()` call to the end of the block.

If we instead want our filter to be placed before or after a specific filter in the middle of the list, we can instead extend the block for that filter. For example, if we want our filter to be displayed after the price filter, we would extend the block `component_filter_panel_item_price`:

```twig
// <plugin root>/src/Resources/views/storefront/component/listing/filter-panel.html.twig
{% sw_extends '@Storefront/storefront/component/listing/filter-panel.html.twig' %}

{% block component_filter_panel_item_price %}
    {{ parent() }}

    {# We'll include our filter element here #}
    {% sw_include '@Storefront/storefront/component/listing/filter/filter-boolean.html.twig' with {
        name: 'isCloseout',
        displayName: 'Closeout'
    } %}
{% endblock %}
```

## Next steps

To add [custom sorting options](add-custom-sorting-product-listing) to your listing in the Storefront, head over to the corresponding guide.

---

---

## Add SCSS Variables
**Source:** [guides/plugins/plugins/storefront/add-scss-variables-via-subscriber.md](https://developer.shopware.com/docs/v6.6/guides/plugins/plugins/storefront/add-scss-variables-via-subscriber.md)  
# Add SCSS Variables

## Overview

In order to add SCSS variables to your plugin, you can configure fields in your `config.xml` to be exposed as scss variables.

We recommend to use the declaration of [SCSS variables](./add-scss-variables) via the `config.xml` but you can still use a subscriber if you need to be more flexible as described below.

## Prerequisites

You won't learn how to create a plugin in this guide, head over to our Plugin base guide to create your first plugin:

You should also know how to listen to events:

## Setup a default value for a custom SCSS variable

Before you start adding your subscriber, you should provide a fallback value for your custom SCSS variable in your plugin `base.scss`:

```css
// <plugin root>/src/Resources/app/storefront/src/scss/base.scss
// The value will be overwritten by the subscriber when the plugin is installed and activated
$sass-plugin-header-bg-color: #ffcc00 !default;

.header-main {
    background-color: $sass-plugin-header-bg-color;
}
```

## Theme variables subscriber

You can add a new subscriber according to the [Listening to events](../plugin-fundamentals/listening-to-events) guide. In this example we name the subscriber `ThemeVariableSubscriber`. The subscriber listens to the `ThemeCompilerEnrichScssVariablesEvent`.

```php
<?php declare(strict_types=1);

namespace Swag\BasicExample\Subscriber;

use Shopware\Storefront\Theme\Event\ThemeCompilerEnrichScssVariablesEvent;
use Symfony\Component\EventDispatcher\EventSubscriberInterface;

class ThemeVariableSubscriber implements EventSubscriberInterface
{
    public static function getSubscribedEvents(): array
    {
        return [
            ThemeCompilerEnrichScssVariablesEvent::class => 'onAddVariables'
        ];
    }

    public function onAddVariables(ThemeCompilerEnrichScssVariablesEvent $event): void
    {
        // Will render: $sass-plugin-header-bg-color: "#59ccff";
        $event->addVariable('sass-plugin-header-bg-color', '#59ccff');
    }
}
```

```xml
<?xml version="1.0" ?>

<container xmlns="http://symfony.com/schema/dic/services"
           xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
           xsi:schemaLocation="http://symfony.com/schema/dic/services http://symfony.com/schema/dic/services/services-1.0.xsd">

    <services>
        <service id="Swag\BasicExample\Subscriber\ThemeVariableSubscriber">
            <tag name="kernel.event_subscriber"/>
        </service>
    </services>
</container>
```

The `ThemeCompilerEnrichScssVariablesEvent` provides the `addVariable()` method which takes the following parameters:

* `$name:` (string): The name of the SCSS variable. In your SCSS, the passed string will be used exactly as its stated here, so please be careful with special characters. We recommend using kebab-case here. The variable prefix `$` will be added automatically. We also recommend prefixing your variable name with your plugin's or company's name to prevent naming conflicts.
* `$value:` (string): The value which should be assigned to the SCSS variable.
* `$sanitize` (bool - optional): Optional parameter to remove special characters from the variables value. The parameter will also add quotes around the variables value. In most cases quotes are not needed e.g. for color hex values. However, there may be situations where you want to pass individual strings to your SCSS variable.

::: warning
Please note that plugins are not sales channel specific. Your SCSS variables are directly added in the SCSS compilation process and will be globally available throughout all themes and Storefront sales channels. If you want to change a variables value for each sales channel you should use plugin config fields and follow the next example.
:::

## Plugin config values as SCSS variables

Inside your `ThemeVariableSubscriber` you can also read values from the plugin configuration and assign those to a SCSS variable. This makes it also possible to have different values for each sales channel. Depending on the selected sales channel inside the plugin configuration in the Administration.

First, lets add a new plugin configuration field according to the [Plugin Configurations](../plugin-fundamentals/add-plugin-configuration):

```xml
// <plugin root>/src/Resources/config/config.xml
<?xml version="1.0" encoding="UTF-8"?>
<config xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:noNamespaceSchemaLocation="https://raw.githubusercontent.com/shopware/shopware/trunk/src/Core/System/SystemConfig/Schema/config.xsd">

    <card>
        <title>Example configuration</title>
        <input-field type="colorpicker">
            <name>sassPluginHeaderBgColor</name>
            <label>Header background color</label>
        </input-field>
    </card>
</config>
```

As you can see in the example, we add an input field of the type colorpicker for our plugin. In the Administration, the component 'sw-colorpicker' will later be displayed for the selection of the value. You also can set a `defaultValue` which will be pre-selected like the following:

```xml
// <plugin root>/src/Resources/config/config.xml
<?xml version="1.0" encoding="UTF-8"?>
<config xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:noNamespaceSchemaLocation="https://raw.githubusercontent.com/shopware/shopware/trunk/src/Core/System/SystemConfig/Schema/config.xsd">

    <card>
        <title>Example configuration</title>
        <input-field type="colorpicker">
            <name>sassPluginHeaderBgColor</name>
            <label>Header background color</label>
            <defaultValue>#fff</defaultValue>
        </input-field>
    </card>
</config>
```

In order to be able to read this config, you have to inject the `SystemConfigService` to your subscriber:

```php
<?php declare(strict_types=1);

namespace Swag\BasicExample\Subscriber;

use Shopware\Core\System\SystemConfig\SystemConfigService;
use Shopware\Storefront\Event\ThemeCompilerEnrichScssVariablesEvent;
use Symfony\Component\EventDispatcher\EventSubscriberInterface;

class ThemeVariableSubscriber implements EventSubscriberInterface
{
    protected SystemConfigService $systemConfig;

    // add the `SystemConfigService` to your constructor
    public function __construct(SystemConfigService $systemConfig)
    {
        $this->systemConfig = $systemConfig;
    }

    public static function getSubscribedEvents(): array
    {
        return [
            ThemeCompilerEnrichScssVariablesEvent::class => 'onAddVariables'
        ];
    }

    public function onAddVariables(ThemeCompilerEnrichScssVariablesEvent $event): void
    {
        /** @var string $configExampleField */
        $configPluginHeaderBgColor = $this->systemConfig->get('SwagBasicExample.config.sassPluginHeaderBgColor', $event->getSalesChannelId());

        if ($configPluginHeaderBgColor) {
            // pass the value from `configPluginHeaderBgColor` to `addVariable`
            $event->addVariable('sass-plugin-header-bg-color', $configPluginHeaderBgColor);
        }
    }
}
```

```xml
<?xml version="1.0" ?>

<container xmlns="http://symfony.com/schema/dic/services"
           xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
           xsi:schemaLocation="http://symfony.com/schema/dic/services http://symfony.com/schema/dic/services/services-1.0.xsd">

    <services>
        <service id="Swag\BasicExample\Subscriber\ThemeVariableSubscriber">
            <!-- add argument `SystemConfigService` -->
            <argument type="service" id="Shopware\Core\System\SystemConfig\SystemConfigService"/>
            <tag name="kernel.event_subscriber"/>
        </service>
    </services>
</container>
```

* The `SystemConfigService` provides a `get()` method where you can access the configuration structure in the first parameter with a dot notation syntax like `SwagBasicExample.config.fieldName`. The second parameter is the sales channel `id`. With this `id` the config fields can be accessed for each sales channel.
* You can get the sales channel id through the getter `getSalesChannelId()` of the `ThemeCompilerEnrichScssVariablesEvent`.
* Now your sass variables can have different values in each sales channel.

### All config fields as SCSS variables

Adding config fields via `$event->addVariable()` for every field individually may be a bit cumbersome in some cases. You could also loop over all config fields and call `addVariable()` for each one. However, this depends on your use case.

```php
// <plugin root>/src/Subscriber/ThemeVariableSubscriber.php
<?php declare(strict_types=1);

namespace Swag\BasicExample\Subscriber;

// ...
use Symfony\Component\Serializer\NameConverter\CamelCaseToSnakeCaseNameConverter;

class ThemeVariableSubscriber implements EventSubscriberInterface
{
    // ...

    public function onAddVariables(ThemeCompilerEnrichScssVariablesEvent $event): void
    {
        $configFields = $this->systemConfig->get('SwagBasicExample.config', $event->getSalesChannelId());

        foreach($configFields as $key => $value) {
            // convert `customVariableName` to `custom-variable-name`
            $kebabCased = str_replace('_', '-', (new CamelCaseToSnakeCaseNameConverter())->normalize($key));

            $event->addVariable($kebabCased, $value);
        }
    }
}
```

To avoid camelCase variable names when reading from the `config.xml`, we recommend using the `CamelCaseToSnakeCaseNameConverter` to format the variable before adding it.

---

---

## Add SCSS variables
**Source:** [guides/plugins/plugins/storefront/add-scss-variables.md](https://developer.shopware.com/docs/v6.6/guides/plugins/plugins/storefront/add-scss-variables.md)  
# Add SCSS variables

::: info
The configuration flag `css` is available from Shopware Version 6.4.13.0
:::

## Overview

In order to add SCSS variables to your plugin, you can configure fields in your `config.xml` to be exposed as scss variables.

We recommend to use the declaration of SCSS variables via the `config.xml` but you can still use a subscriber if you need to be more flexible as described [here](./add-scss-variables-via-subscriber).

## Prerequisites

You won't learn how to create a plugin in this guide, head over to our Plugin base guide to create your first plugin:

## Setup a default value for a custom SCSS variable

Before you start adding your config fields as SCSS variables, you should provide a fallback value for your custom SCSS variable in your plugin `base.scss`:

```css
// <plugin root>/src/Resources/app/storefront/src/scss/base.scss
// The value will be overwritten when the plugin is installed and activated
$sass-plugin-header-bg-color: #ffcc00 !default;

.header-main {
    background-color: $sass-plugin-header-bg-color;
}
```

## Plugin config values as SCSS variables

Now you can declare a config field in your plugin `config.xml` to be available as scss variable.
The new tag is `<css>` and takes the name of the scss variable as its value.

```xml
<input-field>
    <name>sassPluginHeaderBgColor</name>
    <label>Header backgroundcolor</label>
    <label lang="de-DE">Kopfzeile Hintergrundfarbe</label>
    <css>sass-plugin-header-bg-color</css>
    <defaultValue>#eee</defaultValue>
</input-field>
```

This value will now be exposed as SCSS variable and will have the value set in the Administration or the default value if not set. **When this value is changed you still have to recompile the theme manually for the changes to take effect.**
Plugin configurations with declared SCSS variable in its config.xml have a notice in the Administration that changes can change the theme.

---

---

## Add translations
**Source:** [guides/plugins/plugins/storefront/add-translations.md](https://developer.shopware.com/docs/v6.6/guides/plugins/plugins/storefront/add-translations.md)  
# Add translations

## Overview

In this guide, you'll learn how to add translations to the Storefront and how to use them in your twig templates.
To organize your snippets you can add them to `.json` files, so structuring and finding snippets you want to change is very easy.

## Prerequisites

To add your own custom translations for your plugin or app, you first need a base.
Refer to either the [Plugin Base Guide](../plugin-base-guide) or the [App Base Guide](../../apps/app-base-guide) to create one.

## Snippet file structure

Shopware 6 automatically loads your snippet files when a standard file structure and a naming convention are followed.
To do so, store your snippet files in the `<extension root>/src/Resources/snippet/` directory of your plugin or `<extension root>/Resources/snippet/` for your app or theme.
Also, you can use further subdirectories if you want to.
Use `<name>.<locale>` as the naming pattern for the file.
The name can be freely defined, while the locale **must** map to the ISO string of the supported locale in this snippet file - for example `example.de-DE.json`.
More precisely, the ISO string is a combination of "ISO 639-1" language codes and "ISO 3166-1 alpha-2" country codes.
Later, this will be converted to the ICU format (`de_DE`), which is also used by [Symfony](https://symfony.com/doc/current/reference/constraints/Locale.html).

In case you want to provide base translations (ship translations for a whole new language), indicate it with the suffix `.base` in your file name.
Now the filename convention to be followed looks like this `<name>.<locale>.base.json` - for example, `example.de-AT.base.json`.

So your structure could then look like this:

```text
└── SwagBasicExample
    └── src // Without `src` in apps / themes
        ├─ Resources
        │  └─ snippet
        │     ├─ example.de-DE.json
        │     └─ some-directory // optional
        │        └─ example.en-GB.json
        └─ SwagBasicExample.php
```

## Creating translations

Now that we know how the structure of snippets should be, we can create a new snippet file.
In this example we are creating a snippet file for British English called `example.en-GB.json`.
If you are using nested objects, you can access the values with `exampleOne.exampleTwo.exampleThree`.
We can also use template variables, which we can assign values later in the template.
There is no explicit syntax for variables in the Storefront.
However, it is recommended to enclose them with `%` symbols to make their purpose clear.

Here's an example of an English translation file:

```json
// <extension root>/src/Resources/snippet/en_GB/example.en-GB.json
{
  "header": {
    "example": "Our example header"
  },
  "soldProducts": "Sold about %count% products in %country%"
}
```

## Using translations in templates

Now we want to use our previously created snippet in our twig template, we can do this with the `trans` filter.
Below, you can find two examples where we use our translation with placeholders and without.

Translation without placeholders:

```twig
<div class="product-detail-headline">
    {{ 'header.example' | trans }}
</div>
```

Translation with placeholders:

```twig
<div class="product-detail-headline">
    {{ 'soldProducts' | trans({'%count%': 3, '%country%': 'Germany'}) }}
</div>
```

## Using translations in controllers

If we want to use our snippet in a controller, we can use the `trans` method,
which is available if our class is extending from `Shopware\Storefront\Controller\StorefrontController`.
Or use injection via [DI container](#using-translation-generally-in-php).

Translation without placeholders:

```php
$this->trans('header.example');
```

Translation with placeholders:

```php
$this->trans('soldProducts', ['%count%' => 3, '%country%' => 'Germany']);
```

## General usage of translations in PHP

If we need to use a snippet elsewhere in PHP,
we can use [Dependency Injection](../plugin-fundamentals/dependency-injection) to inject the `translator` service,
which implements Symfony's `Symfony\Contracts\Translation\TranslatorInterface`:

```xml
<service id="Swag\Example\Service\SwagService" public="true" >
    <argument type="service" id="translator" />
</service>
```

```php
private TranslatorInterface $translator;

public function __construct(TranslatorInterface $translator)
{
    $this->translator = $translator;
}
```

Then, call the `trans` method, which has the same parameters as the method from controllers.

```php
$this->translator->trans('soldProducts', ['%count%' => 3, '%country%' => 'Germany']);
```

---

---

## Customize Header/Footer
**Source:** [guides/plugins/plugins/storefront/customize-header-footer.md](https://developer.shopware.com/docs/guides/plugins/plugins/storefront/customize-header-footer.md)  
# Customize Header/Footer

## Overview

With the introduction of ESI loading for the header and footer, the way how to customize the header and footer has changed.
E.g. it is no longer possible to customize the header and footer depending on the current page data.
This guide will show you how to customize the header and footer in your plugin.

## Prerequisites

As most guides, this guide is built upon the [Plugin Base Guide](../plugin-base-guide), so you might want to have a look at it.
Other than that, knowing [Twig](https://twig.symfony.com/) is a big advantage for this guide, but that's not necessary.

## Customizing by bypassing the ESI loading

The ESI loading of header and footer was introduced as they are parts of the page that usually do not change that often and could therefore stay cached for a longer time.
The header and footer are now loaded with sub-requests and are therefore no longer dependent on the current page data.
It is still possible to add custom data to the header and footer directly, see ["Add data to storefront page"](add-data-to-storefront-page) guide for more information.

But if you need to customize the header or footer depending on the current page data you need to adjust the ESI loading with additional parameters.
This happens in the `Storefront/Resources/views/storefront/base.html.twig` [file](https://github.com/shopware/shopware/blob/6.7.0.0/src/Storefront/Resources/views/storefront/base.html.twig#L38).
The needed block names are `base_esi_header` and `base_esi_footer`.
Extend the `base.html.twig` in your plugin and overwrite for example the header block.

::: code-group

```twig [PLUGIN_ROOT/src/Resources/views/storefront/base.html.twig]
{% sw_extends '@Storefront/storefront/base.html.twig' %}

{% block base_esi_header %}
    {% set headerParameters = headerParameters|merge({ 'vendorPrefixPluginName': { 'activeRoute': activeRoute } }) %}
    {{ parent() }}
{% endblock %}
```

:::

The `headerParameters` are passed to the header route as query parameters and after that passed through to the header template.
With this change you are now able to access the current route in your header template:

::: code-group

```twig [PLUGIN_ROOT/src/Resources/views/storefront/layout/header.html.twig]
{% sw_extends '@Storefront/storefront/layout/header.html.twig' %}

{% block header %}
    {{ dump(headerParameters.vendorPrefixPluginName.activeRoute) }}
    {{ parent() }}
{% endblock %}
```

:::

This approach works both in plugins and apps.
In plugins, you can also use the `StorefrontRenderEvent`, to add custom data to the header and footer:

::: code-group

```php [PLUGIN_ROOT/src/StorefrontSubscriber.php]
class StorefrontSubscriber
{
    public function __invoke(StorefrontRenderEvent $event): void
    {
        if ($event->getRequest()->attributes->get('_route') !== 'frontend.header') {
            return;
        }

        $headerParameters = $event->getParameter('headerParameters') ?? [];
        $headerParameters['vendorPrefixPluginName']['salesChannelId'] = $event->getSalesChannelContext()->getSalesChannelId();

        $event->setParameter('headerParameters', $headerParameters);
    }
}
```

```twig [PLUGIN_ROOT/src/Resources/views/storefront/layout/header.html.twig]
{% sw_extends '@Storefront/storefront/layout/header.html.twig' %}

{% block header %}
    {{ dump(headerParameters.vendorPrefixPluginName.salesChannelId) }}
    {{ parent() }}
{% endblock %}
```

:::

::: warning
Please be aware, that `headerParameters` and `footerParameters` can only contain scalar values, as they are also query parameters for the ESI routes.
:::

It is also possible to load your custom header or footer templates.
This is also done in the core itself within the checkout process.
See e.g. the [checkout confirm page](https://github.com/shopware/shopware/blob/6.7.0.0/src/Storefront/Resources/views/storefront/page/checkout/confirm/index.html.twig#L3-L5).
Please be aware, that this will overwrite customizations from every other extension.
You also need to make sure, that the `header` and `footer` data is available, if your custom template extends from the original header or footer template.
See e.g. the [checkout confirm controller](https://github.com/shopware/shopware/blob/6.7.0.0/src/Storefront/Controller/CheckoutController.php#L152-L159).

---

---

## Customize Templates
**Source:** [guides/plugins/plugins/storefront/customize-templates.md](https://developer.shopware.com/docs/v6.6/guides/plugins/plugins/storefront/customize-templates.md)  
# Customize Templates

## Overview

This guide will cover customizing Storefront templates with a plugin.

## Prerequisites

As most guides, this guide is built upon the [Plugin base guide](../plugin-base-guide), so you might want to have a look at it. Other than that, knowing [Twig](https://twig.symfony.com/) is a big advantage for this guide, but that's not necessary.

## Getting started

In this guide you will see a very short example on how you can extend a storefront block. For simplicity's sake, only the logo is replaced with a 'Hello world!' text.

### Setting up your view directory

First of all you need to register your plugin's own view path, which basically represents a path in which Shopware 6 is looking for template-files. By default, Shopware 6 is looking for a directory called `views` in your plugin's `Resources` directory, so the path could look like this: `<plugin root>/src/Resources/views`

### Finding the proper template

As mentioned earlier, this guide is only trying to replace the 'demo' logo with a 'Hello world!' text. In order to find the proper template, you can simply search for the term 'logo' inside of the `<shopware root>/src/Storefront` directory. This will eventually lead you to [this file](https://github.com/shopware/shopware/blob/v6.3.4.1/src/Storefront/Resources/views/storefront/layout/header/logo.html.twig).

Overriding this file now requires you to copy the exact same directory structure starting from the `views` directory. In this case, the file `logo.html.twig` is located in a directory called `storefront/layout/header`, so make sure to remember this path.

::: info
There's a plugin out there called [FroshDevelopmentHelper](https://github.com/FriendsOfShopware/FroshDevelopmentHelper), that adds hints about template blocks and includes into the rendered HTML. This way it's easier to actually find the proper template.
:::

### Overriding the template

Now, that you've found the proper template for the logo, you can override it.

This is done by creating the very same directory structure for your custom file, which is also being used in the Storefront core. As you hopefully remember, you have to set up the following directory path in your plugin: `<plugin root>/src/Resources/views/storefront/layout/header` In there you want to create a new file called `logo.html.twig`, just like the original file. Once more to understand what's going on here: In the Storefront code, the path to the logo file looks like this: `Storefront/Resources/views/storefront/layout/header/logo.html.twig` Now have a look at the path being used in your plugin: `<plugin root>/src/Resources/views/storefront/layout/header/logo.html.twig`

Starting from the `views` directory, the path is **exactly the same**, and that's the important part for your custom template to be loaded automatically.

### Custom template content

It's time to fill your custom `logo.html.twig` file. First of all you want to extend from the original file, so you can override its blocks.

Put this line at the very beginning of your file:

```twig
{% sw_extends '@Storefront/storefront/layout/header/logo.html.twig' %}
```

This is simply extending the `logo.html.twig` file from the Storefront bundle. If you would leave the file like that, it wouldn't change anything, as you're currently just extending from the original file with no overrides.

You want to replace the logo with some custom text though, so let's have a look at the original file. In there you'll find a block called `layout_header_logo_link`. Its contents then would create an anchor tag, which is not necessary for our case anymore, so this seems to be a great block to override.

To override it now, just add the very same block into your custom file and replace its contents:

```twig
{% sw_extends '@Storefront/storefront/layout/header/logo.html.twig' %}

{% block layout_header_logo_link %}
    <h2>Hello world!</h2>
{% endblock %}
```

If you wanted to append your text to the logo instead of replacing it, you could add a line like this to your override: {{ parent() }}

And that's it already, you're done. You might have to clear the cache and refresh your storefront to see your changes in action. This can be done by using the command following command inside your command line:

```bash
./bin/console cache:clear
```

::: info
Also remember to not only activate your plugin but also to assign your theme to the correct sales channel by clicking on it in the sidebar, going to the tab Theme and selecting your theme.
:::

### Finding variables

Of course this example is very simplified and does not use any variables, even though you most likely want to do that. Using variables is exactly the same like in [Twig](https://twig.symfony.com/doc/3.x/templates.html#variables) in general, so this won't be explained here in detail. Still, this is how you use a variable: `{{ variableName }}`

But rather than that, how do you know which variables are available to use? For this case, you can just dump all available variables:

```twig
{{ dump() }}
```

This `dump()` call will print out all variables available on this page.

::: info
Once again, the plugin called [FroshDevelopmentHelper](https://github.com/FriendsOfShopware/FroshDevelopmentHelper) adds all available page data to the Twig tab in the profiler, when opening a request and its details. This might help here as well.
:::

## Next steps

You are able to customize templates now, which is a good start. However, there are a few more things you should definitely learn here:

* [Adding styles](add-custom-styling)
* [Adding translations](add-translations)
* [Using icons](add-icons)
* [Using custom assets](add-custom-assets)

---

---

## Fetching Data with Javascript
**Source:** [guides/plugins/plugins/storefront/fetching-data-with-javascript.md](https://developer.shopware.com/docs/v6.6/guides/plugins/plugins/storefront/fetching-data-with-javascript.md)  
# Fetching Data with Javascript

## Overview

When you develop your own plugin, you might want to fetch necessary data from the API. This guide explains how to achieve that.

## Prerequisites

This guide requires you to already have a basic plugin running. If you don't know how to do this in the first place, have a look at our [Plugin base guide](../plugin-base-guide).

While this is not mandatory, having read the guide about [adding custom javascript](add-custom-javascript) plugins beforehand might help you understand this guide a bit further.

## Fetching data

We will use the standard [fetch](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API) to gather additional data. The fetch API is a modern replacement for the old `XMLHttpRequest` object. It is a promise-based API that allows you to make network requests similar to XMLHttpRequest (XHR).

```javascript
// <plugin root>/src/Resources/app/storefront/src/example-plugin/example-plugin.plugin.js
const { PluginBaseClass } = window;

export default class ExamplePlugin extends PluginBaseClass {
    init() {
        this.fetchData();
    }

    // ...

    async fetchData() {
        const response = await fetch('/widgets/checkout/info');
        const data = await response.text();

        console.log(data);
    }
}
```

In this example, we fetch the data from the `/widgets/checkout/info` endpoint. The `fetch` method returns a promise that resolves to the `Response` object representing the response to the request. We then use the `text` method of the `Response` object to get the response body as text.

---

---

## Override Existing Javascript
**Source:** [guides/plugins/plugins/storefront/override-existing-javascript.md](https://developer.shopware.com/docs/v6.6/guides/plugins/plugins/storefront/override-existing-javascript.md)  
# Override Existing Javascript

## Overview

If you have to customize the logic of some core JavaScript Storefront plugins you can override them with your own implementations. You will see how this works by extending the cookie permission plugin and showing the cookie notice on every page load and asking the user if he wants to hide cookie bar via a confirm dialogue.

## Prerequisites

While this is not mandatory, having read the guide about [adding custom javascript plugins](add-custom-javascript) in the first place might help you understand this guide a bit further. Other than that, this guide just requires you to have a running plugin installed, e.g. our plugin from the [Plugin base guide](../plugin-base-guide).

## Extending an existing JavaScript plugin

As JavaScript Storefront plugins are vanilla JavaScript classes, you can simply extend them.

::: info
Each JavaScript plugin can only be overridden once. If two Shopware plugins try to override the same plugin, only the last one of them will actually work.
:::

So let's start with creating the proper directory structure. This example will be called `my-cookie-permission`, as it's extending the default `cookie-permission` plugin.

So for this example you create a `<plugin root>/src/Resources/app/storefront/src/my-cookie-permission` directory and put an empty file `my-cookie-permission.plugin.js` in there. The latter will be your main plugin class file.

Next you create a JavaScript class that extends the original CookiePermission plugin inside your previously created file:

```javascript
import CookiePermissionPlugin from 'src/plugin/cookie/cookie-permission.plugin';

export default class MyCookiePermission extends CookiePermissionPlugin {
}
```

The first line just imports the original `cookie-permission` plugin class, so you can extend from it.

If you aren't able to import the original plugin class (for example third-party plugins without an alias) you can make use of the `window.PluginManager` object to get it.

```javascript
const PluginManager = window.PluginManager
const Plugin = PluginManager.getPlugin('CookiePermission')
const PluginClass = Plugin.get('class')

export default class MyCookiePermission extends PluginClass {
}
```

Now you can override the functions from the parent class.

### Always show the cookie bar

Let's start with the function, that the cookie bar should *always* show up, no matter if the user already configured his cookie preferences or not. By having a look at the [original cookie permission plugin](https://github.com/shopware/shopware/blob/v6.3.4.0/src/Storefront/Resources/app/storefront/src/plugin/cookie/cookie-permission.plugin.js#L46-L53), we can see that it's only shown when the item `this.options.cookieName` is set in the `CookieStorage`. The latter is just a neat helper from Shopware 6 itself to simplify dealing with cookies in JavaScript.

So we'll just override the `init()` method and make sure this value is always set to an empty string, which will evaluate to `false`.

After that you call the `init()` method of the original plugin.

```javascript
import CookiePermissionPlugin from 'src/plugin/cookie/cookie-permission.plugin';
import CookieStorage from 'src/helper/storage/cookie-storage.helper';

export default class MyCookiePermission extends CookiePermissionPlugin {
    init() {
        CookieStorage.setItem(this.options.cookieName, '');
        super.init();
    }
}
```

So now the cookie will always be set to an empty string, resulting in the cookie bar always being shown after a page reload.

### Adding confirm dialogue

Upon clicking the "Accept" or "Deny" button, you want to prompt a confirm dialogue if the user wants to hide the cookie bar. Therefore you override the `_hideCookieBar()` function to show the dialogue and only call the parent implementation if the user clicks "OK" in the confirm dialogue. So your whole plugin now looks like this:

```javascript
import CookiePermissionPlugin from 'src/plugin/cookie/cookie-permission.plugin';
import CookieStorage from 'src/helper/storage/cookie-storage.helper';

export default class MyCookiePermission extends CookiePermissionPlugin {
    init() {
        CookieStorage.setItem(this.options.cookieName, '');
        super.init();
    }

    _hideCookieBar() {
        if (confirm('Do you want to hide the cookie bar?')) {
            super._hideCookieBar();
        }
    }
}
```

Of course, if the user reloads the page, the bar will be back up.

### Register your extended plugin

A few things are now missing to actually register your overridden plugin version. Currently, Shopware doesn't even know your overridden plugin, so let's introduce it to Shopware.

Create a new file called `main.js` in the directory `<plugin root>/src/Resources/app/storefront/src/`, which represents the automatically loaded entry point for javascript files in a plugin.

Next you have to register your extended plugin using the `PluginManager` from the global window object for this. But instead of using the `register()` function to register a new plugin, you use the `override()` function to indicate that you want to override an existing plugin.

```javascript
import MyCookiePermission from './my-cookie-permission/my-cookie-permission.plugin';

const PluginManager = window.PluginManager;
PluginManager.override('CookiePermission', MyCookiePermission, '[data-cookie-permission]');
```

::: info
If the plugin you want to override is an async plugin, the import of your override plugin has to be async as well. See also [Registering an async plugin](./add-custom-javascript.md#registering-an-async-plugin)
:::

```javascript
const PluginManager = window.PluginManager;

// If the plugin "CookiePermission" is registered async, you also override it with an async/dynamic import
PluginManager.override('CookiePermission', () => import('./my-cookie-permission/my-cookie-permission.plugin'), '[data-cookie-permission]');
```

### Testing your changes

To see your changes you have to build the Storefront. Use the following command and reload your Storefront.

```bash
./bin/build-storefront.sh
```

```bash
composer run build:js:storefront
```

You should see the cookie notice at the bottom of the page. If you click the "Accept" or the "Deny" button you should be prompted to confirm hiding the bar.

## Next steps

Sometimes you don't have to actually override a javascript plugin, since sometimes you can simply use an event instead. Learn how this is done in our guide about [listening to events](../reacting-to-javascript-events).

---

---

