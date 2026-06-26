# STORE API

Compiled excerpts from the Shopware Developer Documentation snapshot. Prefer live docs at [developer.shopware.com](https://developer.shopware.com/) when in doubt.

---

## Store API
**Source:** [concepts/api/store-api.md](https://developer.shopware.com/docs/v6.6/concepts/api/store-api.md)  
# Store API

Every interaction between the store and a customer can be modeled using the Store API. It serves as a normalized layer or an interface to communicate between customer-facing applications and the Shopware Core. It can be used to build custom frontends like SPAs, native apps, or simple catalog apps. It doesn't matter what you want to build as long as you are able to consume a JSON API via HTTP.

![Data and logic flow in Shopware 6 (top to bottom and vice versa)](../../assets/concepts-api-storeApiLogic.svg)

Whenever additional logic is added to Shopware, the method of the corresponding service is exposed via a dedicated HTTP route. At the same time, it can be programmatically used to provide data to a controller or other services in the stack. This way, you can ensure that there is always common logic between the API and the Storefront and almost no redundancy. It also allows us to build core functionalities into our Storefront without compromising support for our API consumers.

## Extensibility

Using plugins, you can add custom routes to the Store API (as well as any other routes) and also register custom services. We don't force developers to provide API coverage for their functionalities. However, if you want to support headless applications, ensure that your plugin provides its functionalities through dedicated routes.

## What next?

* To start working with the Store API, check out our [Quick Start guide](https://shopware.stoplight.io/docs/store-api/38777d33d92dc-quick-start-guide) and explore all endpoints in our reference guide.

* An interesting project based on the Store API is [Composable Frontends](../../../frontends).

---

---

## Store API
**Source:** [guides/plugins/plugins/framework/store-api.md](https://developer.shopware.com/docs/v6.6/guides/plugins/plugins/framework/store-api.md)  
# Store API

The Store API plugin in Shopware enables the addition of custom endpoints to the existing Store API and the ability to override or extend the functionality of existing endpoints. This allows developers to customize the API according to their specific requirements, providing additional functionality or modifying the behavior of existing endpoints.

---

---

## Add caching for Store API route
**Source:** [guides/plugins/plugins/framework/store-api/add-caching-for-store-api-route.md](https://developer.shopware.com/docs/v6.6/guides/plugins/plugins/framework/store-api/add-caching-for-store-api-route.md)  
# Add caching for Store API route

## Overview

In this guide you will learn how to add a cache layer to your custom Store API route. In this example, we will add a cache layer for the `ExampleRoute`, which is created in the [Add Store API route](./add-store-api-route) guide. For the cache invalidation we will write a invalidation subscriber.

## Prerequisites

In order to add a cache layer for the Store API route, you first need a Store API route as base. Therefore, you can refer to the [Add Store API route](./add-store-api-route) guide.

You also should have a look at our [Adding custom complex data](../data-handling/add-custom-complex-data) guide, since this guide is built upon it.

## Add cache layer

As you might have learned already from the [Add Store API route](./add-store-api-route) guide, we use abstract classes to make our routes more decoratable.

This concept is very advantageous if we now want to include a cache layer for the route. There are of course different ways to do this - but in this guide we show how we implemented it in the core.

### Add cached route class

First, we create an abstract class called `CachedExampleRoute` which extends the `AbstractExampleRoute`.

```php
// <plugin root>/src/Core/Content/Example/SalesChannel/CachedExampleRoute.php
<?php declare(strict_types=1);

namespace Swag\BasicExample\Core\Content\Example\SalesChannel;

use Psr\Log\LoggerInterface;
use Shopware\Core\Framework\Adapter\Cache\CacheStateSubscriber;
use Shopware\Core\Framework\DataAbstractionLayer\Search\Criteria;
use Shopware\Core\System\SalesChannel\SalesChannelContext;
use Shopware\Core\Framework\Adapter\Cache\AbstractCacheTracer;
use Shopware\Core\Framework\Adapter\Cache\CacheCompressor;
use Shopware\Core\Framework\DataAbstractionLayer\Cache\EntityCacheKeyGenerator;
use Shopware\Core\Framework\Util\Json;
use Symfony\Component\Cache\Adapter\TagAwareAdapterInterface;
use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\Routing\Attribute\Route;
use Symfony\Contracts\EventDispatcher\EventDispatcherInterface;

#[Route(defaults: ['_routeScope' => ['store-api']])]
class CachedExampleRoute extends AbstractExampleRoute
{
    private AbstractExampleRoute $decorated;

    private TagAwareAdapterInterface $cache;

    private EntityCacheKeyGenerator $generator;

    private AbstractCacheTracer $tracer;

    private array $states;

    private LoggerInterface $logger;

    public function __construct(
        AbstractExampleRoute $decorated,
        TagAwareAdapterInterface $cache,
        EntityCacheKeyGenerator $generator,
        AbstractCacheTracer $tracer,
        LoggerInterface $logger
    ) {
        $this->decorated = $decorated;
        $this->cache = $cache;
        $this->generator = $generator;
        $this->tracer = $tracer;
        
        // declares that this route can not be cached if the customer is logged in
        $this->states = [CacheStateSubscriber::STATE_LOGGED_IN];
        $this->logger = $logger;
    }
    
    public function getDecorated(): AbstractExampleRoute
    {
        return $this->decorated;
    }

    #[Route(path: '/store-api/example', name: 'store-api.example.search', methods: ['GET','POST'], defaults: ['_entity' => 'swag_example'])]
    public function load(Criteria $criteria, SalesChannelContext $context): ExampleRouteResponse
    {
        // The context is provided with a state where the route cannot be cached
        if ($context->hasState(...$this->states)) {
            return $this->getDecorated()->load($criteria, $context);
        }

        // Fetch item from the cache pool
        $item = $this->cache->getItem(
            $this->generateKey($context, $criteria)
        );

        try {
            if ($item->isHit() && $item->get()) {
                // Use cache compressor to uncompress the cache value
                return CacheCompressor::uncompress($item);
            }
        } catch (\Throwable $e) {
            // Something went wrong when uncompress the cache item - we log the error and continue to overwrite the invalid cache item 
            $this->logger->error($e->getMessage());
        }

        $name = self::buildName();
        // start tracing of nested cache tags and system config keys
        $response = $this->tracer->trace($name, function () use ($criteria, $context) {
            return $this->getDecorated()->load($criteria, $context);
        });
        
        // compress cache content to reduce cache size
        $item = CacheCompressor::compress($item, $response);

        $item->tag(array_merge(
            // get traced tags and configs        
            $this->tracer->get(self::buildName()),
            [self::buildName()]
        ));

        $this->cache->save($item);

        return $response;
    }
    
    public static function buildName(): string 
    {
        return 'example-route';
    }
  
    private function generateKey(SalesChannelContext $context, Criteria $criteria): string
    {
        $parts = [
            self::buildName(),
            // generate a hash for the route criteria
            $this->generator->getCriteriaHash($criteria),
            // generate a hash for the current context 
            $this->generator->getSalesChannelContextHash($context),
        ];
          
        return md5(Json::encode($parts));
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
        <service id="Swag\BasicExample\Core\Content\Example\SalesChannel\CachedExampleRoute" decorates="Swag\BasicExample\Core\Content\Example\SalesChannel\ExampleRoute" decoration-priority="-1000">
            <argument type="service" id="Swag\BasicExample\Core\Content\Example\SalesChannel\CachedExampleRoute.inner"/>
            <argument type="service" id="cache.object"/>
            <argument type="service" id="Shopware\Core\Framework\DataAbstractionLayer\Cache\EntityCacheKeyGenerator"/>
            <argument type="service" id="Shopware\Core\Framework\Adapter\Cache\CacheTracer"/>
            <argument type="service" id="logger" />
        </service>
    </services>
</container>
```

In the new `CachedExampleRoute` some core classes are used which simplify the caching.

* `TagAwareAdapterInterface` - Used to read, write and tag cache items.

* `EntityCacheKeyGenerator` - Used to generate hashes for the context and/or criteria;

* `AbstractCacheTracer` - Traces all system config keys that were accessed. The data is needed later for cache invalidation.

* `CacheCompressor` - Provides an optimal compression of the cache entries to use as little disk space as possible.

### Add cache invalidation

Cache invalidation is much harder to implement than the actual caching. Finding the right balance between too much and too little invalidation is difficult. Therefore, there is no precise guidance or documentation on when to invalidate what. What and how to invalidate depends on what has been cached. For example, the product routes in the core are always invalidated when the product is written, but also when the product is ordered and reaches the out-of-stock status. The entire cache invalidation in Shopware is controlled via events. On the one hand there is the entity written event and on the other hand the corresponding business events like `ProductNoLongerAvailableEvent`.

```php
// <plugin root>/src/Core/Content/Example/SalesChannel/CacheInvalidationSubscriber.php
<?php declare(strict_types=1);

namespace Swag\BasicExample\Core\Content\Example\SalesChannel;

use Shopware\Core\Framework\DataAbstractionLayer\Event\EntityWrittenContainerEvent;
use Symfony\Component\EventDispatcher\EventSubscriberInterface;
use Swag\BasicExample\Core\Content\Example\ExampleDefinition;
use Shopware\Core\Framework\Adapter\Cache\CacheInvalidator;

class CacheInvalidationSubscriber implements EventSubscriberInterface
{
    private CacheInvalidator $cacheInvalidator;

    public function __construct(CacheInvalidator $cacheInvalidator) 
    {
        $this->cacheInvalidator = $cacheInvalidator;
    }
    
    public static function getSubscribedEvents()
    {
        return [
            // The EntityWrittenContainerEvent is a generic event that is always thrown when an entities are written. This contains all changed entities
            EntityWrittenContainerEvent::class => [
                ['invalidate', 2001]
            ],
        ];
    }
    
    public function invalidate(EntityWrittenContainerEvent $event): void
    {
        // check if own entity written. In some cases you want to use the primary keys for further cache invalidation
        $changes = $event->getPrimaryKeys(ExampleDefinition::ENTITY_NAME);
        
        // no example entity changed? Then the cache does not need to be invalidated
        if (empty($changes)) {
            return;
        }

        $this->cacheInvalidator->invalidate([
            CachedExampleRoute::buildName()  
        ]);
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
        <service id=" Swag\BasicExample\Core\Content\Example\SalesChannel\CacheInvalidationSubscriber">
            <argument type="service" id="Shopware\Core\Framework\Adapter\Cache\CacheInvalidator"/>
        </service>
    </services>
</container>
```

---

---

## Add Store API route
**Source:** [guides/plugins/plugins/framework/store-api/add-store-api-route.md](https://developer.shopware.com/docs/v6.6/guides/plugins/plugins/framework/store-api/add-store-api-route.md)  
*(Body truncated in this bundle; follow the link for the rest.)*

# Add Store API route

## Overview

In this guide you will learn how to add a custom store API route. In this example, we will create a new route called `ExampleRoute` that searches entities of type `swag_example`. The route will be accessible under `/store-api/example`.

## Prerequisites

In order to add your own Store API route for your plugin, you first need a plugin as base. Therefore, you can refer to the [Plugin Base Guide](../../plugin-base-guide).

You also should have a look at our [Adding custom complex data](../data-handling/add-custom-complex-data) guide, since this guide is built upon it.

## Add Store API route

As you may already know from the [Adjusting a service](../../plugin-fundamentals/adjusting-service) guide, we use abstract classes to make our routes more decoratable.

::: warning
All fields that should be available through the API require the flag `ApiAware` in the definition.
:::

### Create abstract route class

First of all, we create an abstract class called `AbstractExampleRoute`. This class has to contain a method `getDecorated` and a method `load` with a `Criteria` and `SalesChannelContext` as parameter. The `load` method has to return an instance of `ExampleRouteResponse`, which we will create later on.

```php
// <plugin root>/src/Core/Content/Example/SalesChannel/AbstractExampleRoute.php
<?php declare(strict_types=1);

namespace Swag\BasicExample\Core\Content\Example\SalesChannel;

use Shopware\Core\Framework\DataAbstractionLayer\Search\Criteria;
use Shopware\Core\System\SalesChannel\SalesChannelContext;

abstract class AbstractExampleRoute
{
    abstract public function getDecorated(): AbstractExampleRoute;

    abstract public function load(Criteria $criteria, SalesChannelContext $context): ExampleRouteResponse;
}
```

### Create route class

Now we can create a new class `ExampleRoute` which uses our previously created `AbstractExampleRoute`.

```php
// <plugin root>/src/Core/Content/Example/SalesChannel/ExampleRoute.php
<?php declare(strict_types=1);

namespace Swag\BasicExample\Core\Content\Example\SalesChannel;

use Shopware\Core\Framework\DataAbstractionLayer\EntityRepository;
use Shopware\Core\Framework\DataAbstractionLayer\Search\Criteria;
use Shopware\Core\Framework\Plugin\Exception\DecorationPatternException;
use Shopware\Core\System\SalesChannel\SalesChannelContext;
use Symfony\Component\Routing\Attribute\Route;

#[Route(defaults: ['_routeScope' => ['store-api']])]
class ExampleRoute extends AbstractExampleRoute
{
    protected EntityRepository $exampleRepository;

    public function __construct(EntityRepository $exampleRepository)
    {
        $this->exampleRepository = $exampleRepository;
    }

    public function getDecorated(): AbstractExampleRoute
    {
        throw new DecorationPatternException(self::class);
    }

    #[Route(path: '/store-api/example', name: 'store-api.example.search', methods: ['GET','POST'], defaults: ['_entity' => 'swag_example'])]
    public function load(Criteria $criteria, SalesChannelContext $context): ExampleRouteResponse
    {
        return new ExampleRouteResponse($this->exampleRepository->search($criteria, $context->getContext()));
    }
}
```

As you can see, our class has the attribute `Route` and the defined \_routeScope `store-api`.

In our class constructor we've injected our `swag_example.repository`. The method `getDecorated()` must throw a `DecorationPatternException` because it has no decoration yet and the method `load`, which fetches the data, returns a new `ExampleRouteResponse` with the respective repository search result as argument.

The `_entity` in the defaults of the `Route` attribute just marks the entity that the api will return.

### Register route class

```xml
<?xml version="1.0" ?>
<container xmlns="http://symfony.com/schema/dic/services"
           xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
           xsi:schemaLocation="http://symfony.com/schema/dic/services http://symfony.com/schema/dic/services/services-1.0.xsd">

    <services>
        <service id="Swag\BasicExample\Core\Content\Example\SalesChannel\ExampleRoute" >
            <argument type="service" id="swag_example.repository"/>
        </service>
    </services>
</container>
```

### Route response

After we have created our route, we need to create the mentioned `ExampleRouteResponse`. This class should extend from `Shopware\Core\System\SalesChannel\StoreApiResponse`, consequently inheriting a property `$object` of type `Shopware\Core\Framework\DataAbstractionLayer\Search\EntitySearchResult`. The `StoreApiResponse` parent constructor takes accepts one argument `$object` in order to set the value for the `$object` property (currently we provide this parameter our `ExampleRoute`). Finally, we add a method `getExamples` in which we return our entity collection that we got from the object.

```php
// <plugin root>/src/Core/Content/Example/SalesChannel/ExampleRouteResponse.php
<?php declare(strict_types=1);

namespace Swag\BasicExample\Core\Content\Example\SalesChannel;

use Shopware\Core\Framework\DataAbstractionLayer\Search\EntitySearchResult;
use Shopware\Core\System\SalesChannel\StoreApiResponse;
use Swag\BasicExample\Core\Content\Example\ExampleCollection;

/**
 * Class ExampleRouteResponse
 * @property EntitySearchResult<ExampleCollection> $object
 */
class ExampleRouteResponse extends StoreApiResponse
{
    public function getExamples(): ExampleCollection
    {
        return $this->object->getEntities();
    }
}
```

## Register route

The last thing we need to do now is to tell Shopware how to look for new routes in our plugin. This is done with a `routes.xml` file at `<plugin root>/src/Resources/config/` location. Have a look at the official [Symfony documentation](https://symfony.com/doc/current/routing.html) about routes and how they are registered.

```xml
// <plugin root>/src/Resources/config/routes.xml
<?xml version="1.0" encoding="UTF-8" ?>
<routes xmlns="http://symfony.com/schema/routing"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:schemaLocation="http://symfony.com/schema/routing
        https://symfony.com/schema/routing/routing-1.0.xsd">

    <import resource="../../Core/**/*Route.php" type="attribute" />
</routes>
```

## Check route via Symfony debugger

To check, if your route was registered correctly, you can use the [Symfony route debugger](https://symfony.com/doc/current/routing.html#debugging-routes).

```bash
// 
$ ./bin/console debug:router store-api.example.search
```

## Add route to Swagger

To add the route to the Swagger page, a JSON file is needed in a specific [format](https://swagger.io/specification/#paths-object). It contains information about the paths, methods, parameters, and more. You must place the JSON file in `<plugin root>/src/Resources/Schema/StoreApi/` so the shopware internal OpenApi3Generator can find it (for Admin API endpoints, use `AdminApi`).

```javascript
// <plugin root>/src/Resources/Schema/StoreApi/example.json
{
  "openapi": "3.0.0",
  "info": [],
  "paths": {
    "/example": {
      "post": {
        "tags": [
          "Example",
          "Endpoints supporting Criteria "
        ],
        "summary": "Example entity endpoint",
        "description": "Returns a list of example entities.",
        "operationId": "example",
        "requestBody": {
          "required": false,
          "content": {
            "application/json": {
              "schema": {
                "allOf": [
                  {
                    "$ref": "#/components/schemas/Criteria"
                  }
                ]
              }
            }
          }
        },
        "responses": {
          "200": {
            "description": "Returns a list of example entities.",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/Example"
                }
              }
            }
          }
        },
        "security": [
          {
            "ApiKey": []
          }
        ]
      }
    }
  }
}
```

### Check route in Swagger

To check, if your file has the correct format, you'll have to check Swagger. To do this, go to the following route: `/store-api/_info/swagger.html`.

Your generated request and response could look like this:

#### Request

```json
{
  "page": 0,
  "limit": 0,
  "term": "string",
  "filter": [
    {
      "type": "string",
      "field": "string",
      "value": "string"
    }
  ],
  "sort": [
    {
      "field": "string",
      "order": "string",
      "naturalSorting": true
    }
  ],
  "post-filter": [
    {
      "type": "string",
      "field": "string",
      "value": "string"
    }
  ],
  "associations": {},
  "aggregations": [
    {
      "name": "string",
      "type": "string",
      "field": "string"
    }
  ],
  "query": [
    {
      "score": 0,
      "query": {
        "type": "string",
        "field": "string",
        "value": "string"
      }
    }
  ],
  "grouping": [
    "string"
  ]
}
```

#### Response

```json
{
  "total": 0,
  "aggregations": {},
  "elements": [
    {
      "id": "string",
      "name": "string",
      "description": "string",
      "active": true,
      "createdAt": "2021-03-24T13:18:46.503Z",
      "updatedAt": "2021-03-24T13:18:46.503Z"
    }
  ]
}
```

## Make the route available for the Storefront

If you want to access the functionality of your route also from the Storefront you need to make it available there by adding a custom [Storefront controller](../../storefront/add-custom-controller) that will wrap your just created route.

```php
// <plugin root>/src/Storefront/Controller/ExampleController.php
<?php declare(strict_types=1);

namespace Swag\BasicExample\Storefront\Controller;

use Shopware\Core\Framework\DataAbstractionLayer\Search\Criteria;
use Shopware\Core\System\SalesChannel\SalesChannelContext;
use Shopware\Storefront\Controller\StorefrontController;
use Swag\BasicExample\Core\Content\Example\SalesChannel\AbstractExampleRoute;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\Routing\Attribute\Route;

#[Route(defaults: ['_routeScope' => ['storefront']])]
class ExampleController extends StorefrontController
{
    private AbstractExampleRoute $route;

    public function __construct(AbstractExampleRoute $route)
    {
        $this->route = $route;
    }

    #[Route(path: '/example', name: 'frontend.example.search', methods: ['GET', 'POST'], defaults: ['XmlHttpRequest' => 'true', '_entity' => 'swag_example'])]
    public function load(Criteria $criteria, SalesChannelContext $context): Response
    {
        return $this->route->load($criteria, $context);
    }
}
```

This looks very similar then what we did in the `ExampleRoute` itself. The main difference is that this route is registered for the `storefront` route scope.
Additionally, we also use the `'XmlHttpRequest' => true` config option on the route, this will enable us to request that route via AJAX-calls from the Storefronts javascript.

### Register the Controller

```xml
<?xml version="1.0" ?>
<container xmlns="http://symfony.com/schema/dic/services"
           xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
           xsi:schemaLocation="http://symfony.com/schema/dic/services http://symfony.com/schema/dic/services/services-1.0.xsd">

    <services>
        <service id="Swag\BasicExample\Core\Content\Example\SalesChannel\ExampleRoute" >
            <argument type="service" id="swag_example.repository"/>
        </service>
    
        <service id="Swag\BasicExample\Storefront\Controller\ExampleController" >
            <argument type="service" id="Swag\BasicExample\Core\Content\Example\SalesChannel\ExampleRoute"/>
            <call method="setContainer">
                <argument type="service" id="service_container"/>
            </call>
        </service>
    </services>
</container>
```

### Register Storefront api-route

We need to tell Shopware that there is a n

… **Truncated.** Full document: https://developer.shopware.com/docs/v6.6/guides/plugins/plugins/framework/store-api/add-store-api-route.md


---

## Override Existing Route
**Source:** [guides/plugins/plugins/framework/store-api/override-existing-route.md](https://developer.shopware.com/docs/v6.6/guides/plugins/plugins/framework/store-api/override-existing-route.md)  
# Override Existing Route

## Overview

In this guide you will learn how to override existing Store API routes to add additional data to it.

## Prerequisites

As most guides, this guide is also built upon the [Plugin base guide](../../plugin-base-guide), but you don't necessarily need that.

Furthermore, you should have a look at our guide about [Adding a Store API route](add-store-api-route), since this guide is built upon it.

## Decorating our route

First, we have to create a new class which extends `AbstractExampleRoute`. In this example we will name it `ExampleRouteDecorator`.

```php
// <plugin root>/src/Core/Content/Example/SalesChannel/ExampleRouteDecorator.php
<?php declare(strict_types=1);

namespace Swag\BasicExample\Core\Content\Example\SalesChannel;

use Shopware\Core\Framework\DataAbstractionLayer\EntityRepository;
use Shopware\Core\Framework\DataAbstractionLayer\Search\Criteria;
use Shopware\Core\System\SalesChannel\SalesChannelContext;
use Symfony\Component\Routing\Attribute\Route;

#[Route(defaults: ['_routeScope' => ['store-api']])]
class ExampleRouteDecorator extends AbstractExampleRoute
{
    protected EntityRepository $exampleRepository;

    private AbstractExampleRoute $decorated;

    public function __construct(EntityRepository $exampleRepository, AbstractExampleRoute $exampleRoute)
    {
        $this->exampleRepository = $exampleRepository;
        $this->decorated = $exampleRoute;
    }

    public function getDecorated(): AbstractExampleRoute
    {
        return $this->decorated;
    }
    
    #[Route(path: '/store-api/example', name: 'store-api.example.search', methods: ['GET', 'POST'], defaults: ['_entity' => 'category'])]
    public function load(Criteria $criteria, SalesChannelContext $context): ExampleRouteResponse
    {
        // We must call this function when using the decorator approach
        $exampleResponse = $this->decorated->load();
        
        // do some custom stuff
        $exampleResponse->headers->add([ 'cache-control' => "max-age=10000" ])

        return $exampleResponse;›
    }
}
```

As you can see, our decorated route has to extend from the `AbstractExampleRoute` and the constructor has to accept an instance of `AbstractExampleRoute`. Furthermore, the `getDecorated()` function has to return the decorated route passed into the constructor. Now we can add some additional data in the `load` method, which we can retrieve with the criteria.

## Registering route

Last, we have to register the decorated route to the DI-container. The `ExampleRouteDecorator` has to be registered after the `ExampleRoute` with the attribute `decorated` which points to the `ExampleRoute`. For the second argument we have to use the `ExampleRouteDecorator.inner`.

```xml
// <plugin root>/src/Resources/config/services.xml
<?xml version="1.0" ?>

<container xmlns="http://symfony.com/schema/dic/services"
           xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
           xsi:schemaLocation="http://symfony.com/schema/dic/services http://symfony.com/schema/dic/services/services-1.0.xsd">

    <services>
        ...

        <service id="Swag\BasicExample\Core\Content\Example\SalesChannel\ExampleRouteDecorator" decorates="Swag\BasicExample\Core\Content\Example\SalesChannel\ExampleRoute" public="true">
            <argument type="service" id="swag_example.repository"/>
            <argument type="service" id="Swag\BasicExample\Core\Content\Example\SalesChannel\ExampleRouteDecorator.inner"/>
        </service>
    </services>
</container>
```

---

---

## resources/api/store-api-reference.md
**Source:** [resources/api/store-api-reference.md](https://developer.shopware.com/resources/api/store-api-reference.md)  
---

---

