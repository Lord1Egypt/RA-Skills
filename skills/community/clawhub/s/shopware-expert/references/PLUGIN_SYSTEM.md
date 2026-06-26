# PLUGIN SYSTEM

Compiled excerpts from the Shopware Developer Documentation snapshot. Prefer live docs at [developer.shopware.com](https://developer.shopware.com/) when in doubt.

---

## Bundle
**Source:** [guides/plugins/plugins/bundle.md](https://developer.shopware.com/docs/v6.6/guides/plugins/plugins/bundle.md)  
# Bundle

Plugins are based on the Symfony bundle concept, but offer additional features like lifecycle events and the ability to be managed in the Shopware administration.
This is maybe unwanted in some cases, like project critical customizations which should not be managed via the Shopware administration.
In this case, you can use a Symfony bundle instead of a plugin.

## Project Structure

Here's how a typical Shopware 6 project structure looks like when using bundles:

```text
project-root/
├── bin/
│   └── console
├── config/
│   ├── bundles.php
│   ├── packages/
│   └── services.yaml
├── public/
│   ├── index.php
│   └── bundles/
├── src/
│   └── YourBundleName/
│       ├── YourBundleName.php
│       ├── Migration/
│       │   └── Migration1234567890YourMigration.php
│       └── Resources/
│           ├── config/
│           │   ├── services.xml
│           │   └── routes.xml
│           ├── views/
│           │   └── storefront/
│           │       └── page/
│           └── app/
│               ├── storefront/
│               │   └── src/
│               └── administration/
│                   └── src/
├── var/
├── vendor/
├── composer.json
├── composer.lock
└── .shopware-project.yaml
```

The Bundle is typically placed in the `src/` folder of your project, which is the standard location for custom code in a Shopware project. You still will need to register the bundle in the `config/bundles.php` file of your project.

## Choosing the right Bundle class

There are two Bundle classes you can choose from:

* `Shopware\Core\Framework\Bundle`
* `Symfony\Component\HttpKernel\Bundle\Bundle`

The first one is the Shopware bundle class and the second one is the Symfony bundle class.
The Shopware bundle class extends the Symfony bundle class, but offers additional features like acting as theme, bringing JavaScript/CSS files, Migrations, etc.
If you don't need these features, you can use the Symfony bundle class instead.

## Creating a Bundle

By default, The namespace `App\` is registered to the `src` folder in any Shopware project to be used for customizations. We recommend using this namespace, if you like to change the project structure, you can change the `App\` namespace in the `composer.json` file of your project.

```php
// <project root>/src/YourBundleName.php
<?php declare(strict_types=1);

namespace App\YourBundleName;

use Shopware\Core\Framework\Bundle;

class YourBundleName extends Bundle
{
}
```

The bundle class needs to be registered in the `config/bundles.php` file of your project.

```php
// <project root>/config/bundles.php
//...
App\YourBundleName\YourBundleName::class => ['all' => true],
//...
```

## Adding services, twig templates, routes, theme, etc

You can add services, twig templates, routes, etc. to your bundle like you would do in a plugin.
Just create `Resources/config/services.xml` and `Resources/config/routes.xml` files or `Resources/views` for twig templates.
The bundle will be automatically detected and the files will be loaded.

To mark your bundle as a theme, it's enough to implement the `Shopware\Core\Framework\ThemeInterface` interface in your bundle class.
This will automatically register your bundle as a theme and make it available in the Shopware administration.
You can also add a `theme.json` file to define the theme configuration like [described here](../themes/theme-configuration.md).

## Adding migrations

Migrations are not automatically detected in bundles.
To enable migrations, you need to overwrite the `build` method in your bundle class like this:

```php
// <project root>/src/YourBundleName.php
<?php declare(strict_types=1);

namespace App\YourBundleName;

use Shopware\Core\Framework\Bundle;

class YourBundleName extends Bundle
{
    public function build(ContainerBuilder $container): void
    {
        parent::build($container);

        $this->registerMigrationPath($container);
    }
}
```

As Bundles don't have a lifecycle, the migrations are not automatically executed.
You need to execute them manually via the console command:

```bash
bin/console database:migrate <BundleName> --all
```

If you use [Deployment Helper](../../hosting/installation-updates/deployments/deployment-helper.md), you can add it to the `.shopware-project.yaml` file like this:

```yaml
deployment:
    hooks:
        pre-update: |
            bin/console database:migrate <BundleName> --all
```

## Integration into Shopware-CLI

Shopware-CLI cannot detect bundles automatically, therefore the assets of the bundles are not built automatically.
You will need to adjust the `composer.json` file of your project to specify the path to the bundle.
This is done by adding the `extra` section to the `composer.json` file:

```json
{
    "extra": {
        "shopware-bundles": {
          "src/<BundleName>": {
            "name": "<BundleName>",
          }
        }
    }
}
```

This will tell Shopware-CLI where the bundle is located and what the name of the bundle is.

---

---

## Elasticsearch
**Source:** [guides/plugins/plugins/elasticsearch.md](https://developer.shopware.com/docs/v6.6/guides/plugins/plugins/elasticsearch.md)  
# Elasticsearch

By extending fields of an entity to the Elasticsearch engine, you expand the search capabilities of Shopware, allowing users to search based on additional attributes or metadata. This enhances the overall search experience and enables more targeted and precise search results for customers.

---

---

## Adding Product Entity Extension to Elasticsearch
**Source:** [guides/plugins/plugins/elasticsearch/add-product-entity-extension-to-elasticsearch.md](https://developer.shopware.com/docs/v6.6/guides/plugins/plugins/elasticsearch/add-product-entity-extension-to-elasticsearch.md)  
*(Body truncated in this bundle; follow the link for the rest.)*

# Adding Product Entity Extension to Elasticsearch

## Overview

In this guide you'll learn how to add extended fields of the product entity to the elasticsearch engine to make it searchable.

In this example we'll assume an extension of the `ProductDefinition` with a string field `customString` like described in [Adding Complex data to existing entities](../framework/data-handling/add-complex-data-to-existing-entities#adding-a-field-without-database).

## Prerequisites

This guide is built upon the [Plugin Base Guide](../plugin-base-guide), and the entity extension described in [Adding Complex data to existing entities](../framework/data-handling/add-complex-data-to-existing-entities#adding-a-field-without-database).
We will extend the product extension with an `OneToOneAssociationField` and `OneToManyAssociationField`.

## Decorate the ElasticsearchProductDefinition

To extend the elasticsearch definition we need to extend the product definition first and add the subscriber. This is described in the above mentioned articles.
Here we show you how this could look like in the end.

The service.xml with all needed definitions.

```xml
// <plugin root>/src/Core/Content/DependencyInjection/product.xml
<?xml version="1.0" ?>

<container xmlns="http://symfony.com/schema/dic/services"
           xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
           xsi:schemaLocation="http://symfony.com/schema/dic/services http://symfony.com/schema/dic/services/services-1.0.xsd">

    <services>
        <service id="Swag\BasicExample\Extension\Content\Product\CustomExtension">
            <tag name="shopware.entity.extension"/>
        </service>

        <service id="Swag\BasicExample\Extension\Content\Product\OneToOneExampleExtensionDefinition">
            <tag name="shopware.entity.definition" entity="one_to_one_swag_example_extension" />
        </service>

        <service id="Swag\BasicExample\Extension\Content\Product\OneToManyExampleExtensionDefinition">
            <tag name="shopware.entity.definition" entity="one_to_many_swag_example_extension" />
        </service>

        <service id="Swag\BasicExample\Subscriber\ProductSubscriber">
            <tag name="kernel.event_subscriber"/>
        </service>

        <service id="Swag\BasicExample\Elasticsearch\Product\MyProductEsDecorator" decorates="Shopware\Elasticsearch\Product\ElasticsearchProductDefinition">
            <argument type="service" id="Swag\BasicExample\Elasticsearch\Product\MyProductEsDecorator.inner"/>
            <argument type="service" id="Doctrine\DBAL\Connection"/>
        </service>
    </services>
</container>
```

The product extension `CustomExtension.php` provides the extensions to the product entity.

```php
// <plugin root>/src/Extension/Content/Product/CustomExtension.php
<?php declare(strict_types=1);

namespace Swag\BasicExample\Extension\Content\Product;

use Shopware\Core\Content\Product\ProductDefinition;
use Shopware\Core\Framework\DataAbstractionLayer\EntityExtension;
use Shopware\Core\Framework\DataAbstractionLayer\Field\ObjectField;
use Shopware\Core\Framework\DataAbstractionLayer\Field\OneToManyAssociationField;
use Shopware\Core\Framework\DataAbstractionLayer\Field\OneToOneAssociationField;
use Shopware\Core\Framework\DataAbstractionLayer\FieldCollection;
use Shopware\Core\Framework\DataAbstractionLayer\Field\Flag\Runtime;

class CustomExtension extends EntityExtension
{
    public function extendFields(FieldCollection $collection): void
    {
        //Add ApiAware flag to make this field searchable
        $collection->add(
            (new OneToOneAssociationField('oneToOneExampleExtension', 'id', 'product_id', OneToOneExampleExtensionDefinition::class, true))->addFlags(new ApiAware())
        );
        //Add ApiAware flag to make this field searchable
        $collection->add(
            (new OneToManyAssociationField('oneToManyExampleExtension', OneToManyExampleExtensionDefinition::class, 'product_id'))->addFlags(new ApiAware())
        );
        //Runtime fields are not searchable
        $collection->add(
            (new ObjectField('custom_string', 'customString'))->addFlags(new Runtime())
        );
    }

    public function getDefinitionClass(): string
    {
        return ProductDefinition::class;
    }
}
```

The entity definition `OneToManyExampleExtensionDefinition.php`.

```php
// <plugin root>/src/Extension/Content/Product/OneToManyExampleExtensionDefinition.php
<?php declare(strict_types=1);

namespace Swag\BasicExample\Extension\Content\Product;

use Shopware\Core\Content\Product\ProductDefinition;
use Shopware\Core\Framework\DataAbstractionLayer\EntityDefinition;
use Shopware\Core\Framework\DataAbstractionLayer\Field\FkField;
use Shopware\Core\Framework\DataAbstractionLayer\Field\Flag\ApiAware;
use Shopware\Core\Framework\DataAbstractionLayer\Field\Flag\PrimaryKey;
use Shopware\Core\Framework\DataAbstractionLayer\Field\Flag\Required;
use Shopware\Core\Framework\DataAbstractionLayer\Field\IdField;
use Shopware\Core\Framework\DataAbstractionLayer\Field\ManyToOneAssociationField;
use Shopware\Core\Framework\DataAbstractionLayer\Field\ReferenceVersionField;
use Shopware\Core\Framework\DataAbstractionLayer\Field\StringField;
use Shopware\Core\Framework\DataAbstractionLayer\FieldCollection;
use Shopware\Core\Framework\DataAbstractionLayer\Entity;

class OneToManyExampleExtensionDefinition extends EntityDefinition
{
    public const ENTITY_NAME = 'one_to_many_swag_example_extension';

    public function getEntityName(): string
    {
        return self::ENTITY_NAME;
    }

    public function getEntityClass(): string
    {
        return Entity::class;
    }

    protected function defineFields(): FieldCollection
    {
        return new FieldCollection([
            (new IdField('id', 'id'))->addFlags(new ApiAware(), new Required(), new PrimaryKey()),
            new FkField('product_id', 'productId', ProductDefinition::class),
            (new ReferenceVersionField(ProductDefinition::class))->addFlags(new Required()),
            (new StringField('custom_string', 'customString'))->addFlags(new ApiAware()),

            new ManyToOneAssociationField('product', 'product_id', ProductDefinition::class),
        ]);
    }
}
```

The entity definition `OneToOneExampleExtensionDefinition.php`.

```php
// <plugin root>/src/Extension/Content/Product/OneToOneExampleExtensionDefinition.php
<?php declare(strict_types=1);

namespace Swag\BasicExample\Extension\Content\Product;

use Shopware\Core\Content\Product\ProductDefinition;
use Shopware\Core\Framework\DataAbstractionLayer\EntityDefinition;
use Shopware\Core\Framework\DataAbstractionLayer\Field\FkField;
use Shopware\Core\Framework\DataAbstractionLayer\Field\Flag\ApiAware;
use Shopware\Core\Framework\DataAbstractionLayer\Field\Flag\PrimaryKey;
use Shopware\Core\Framework\DataAbstractionLayer\Field\Flag\Required;
use Shopware\Core\Framework\DataAbstractionLayer\Field\IdField;
use Shopware\Core\Framework\DataAbstractionLayer\Field\OneToOneAssociationField;
use Shopware\Core\Framework\DataAbstractionLayer\Field\ReferenceVersionField;
use Shopware\Core\Framework\DataAbstractionLayer\Field\StringField;
use Shopware\Core\Framework\DataAbstractionLayer\FieldCollection;
use Shopware\Core\Framework\DataAbstractionLayer\Entity;

class OneToOneExampleExtensionDefinition extends EntityDefinition
{
    public const ENTITY_NAME = 'one_to_one_swag_example_extension';

    public function getEntityName(): string
    {
        return self::ENTITY_NAME;
    }

    public function getEntityClass(): string
    {
        return Entity::class;
    }

    protected function defineFields(): FieldCollection
    {
        return new FieldCollection([
            (new IdField('id', 'id'))->addFlags(new ApiAware(), new Required(), new PrimaryKey()),
            new FkField('product_id', 'productId', ProductDefinition::class),
            (new ReferenceVersionField(ProductDefinition::class))->addFlags(new Required()),
            (new StringField('custom_string', 'customString'))->addFlags(new ApiAware()),

            new OneToOneAssociationField('product', 'product_id', 'id', ProductDefinition::class, false)
        ]);
    }
}
```

Here is a decoration to add a new field named `customString`, an `oneToOneAssociationField` named `oneToOneExampleExtension` and an `oneToManyAssociationField` named `oneToManyExampleExtension` to the index.
For adding more information from the database you should execute a single query with all document ids `(array_column($documents, 'id'))` and map the values.

```php
// <plugin root>/src/Elasticsearch/Product/MyProductEsDecorator.php
<?php

namespace Swag\BasicExample\Elasticsearch\Product;

use Shopware\Core\Framework\Context;
use Shopware\Core\Framework\DataAbstractionLayer\EntityDefinition;
use Shopware\Elasticsearch\Framework\AbstractElasticsearchDefinition;
use Doctrine\DBAL\Connection;
use Swag\BasicExample\Subscriber\ProductSubscriber;

class MyProductEsDecorator extends AbstractElasticsearchDefinition
{
    private AbstractElasticsearchDefinition $productDefinition;
    private Connection $connection;

    public function __construct(AbstractElasticsearchDefinition $productDefinition, Connection $connection)
    {
        $this->productDefinition = $productDefinition;
        $this->connection = $connection;
    }

    public function getEntityDefinition(): EntityDefinition
    {
        return $this->productDefinition->getEntityDefinition();
    }

    public function buildTermQuery(Context $context, Criteria $criteria): BoolQuery
    {
        return $this->productDefinition->buildTermQuery($context, $criteria);
    }

    /**
     * Extend the mapping with your own changes
     * Take care to get the default mapping first by `$this->productDefinition->getMapping($context);`
     */
    public function getMapping(Context $context): array
    {
        $mapping = $this->productDefinition->getMapping($context);

        //The mapping for a simple keyword field
        $mapping['properties']['customString'] = AbstractElasticsearchDefinition::KEYWORD_FIELD;

        // Adding an association as keyword
        $mapping['properties']['oneToOneExampleExtension'] = [
                'type' => 'nested',
                'properties' => [
                    'customString' => AbstractElasticsearchDefinition::KEYWORD_FIELD,
            ],
        ];

        // Adding a nested field with id
        $mapping['properties']['oneToManyExampleExtension'] = [
            'type' => 'nested',
            'properties' => [
                'id' => AbstractElasticsearchDefinition::KEYWORD_FIELD,
            ],
        ];

        return $mapping;
    }

    public function fetch(array $ids, Context $context): array
    {
        $documents = $this->productDefinition->fetch($ids, $context);

        $associationOneToOne = $this->fetchOneToOneExample($ids);
        $associationOneToMany = $this->fetchOneToManyExample($ids);

        foreach ($documents as &$document) {
            /**
             * A field directly on the product.
             * The value should be filled with the same Runtime value which will be set by the ProductSubscriber
             */
            $document['customString'] = ProductSubscriber::getRuntimeValue($document['id'])->getValue();

            /**
             * Field with value from associated entity
             */
            if (isset($associationOneToOne[$document['id']])) {
                $document['oneToOneExampleExtension']['customString'] = $associationOneToOne[$document['id']];
            }

            /**
             * Field with multiple id entries from associated entity
             */
            if (isset($associationOneToMany[$document['id']])) {
                $document['oneToManyExampleExtension'] = array_map(function (string $id) {
                    return ['id' => $id];
                }, array_filter(explode('|', $associationOneToMany[$document['id']] ?? '')));
           

… **Truncated.** Full document: https://developer.shopware.com/docs/v6.6/guides/plugins/plugins/elasticsearch/add-product-entity-extension-to-elasticsearch.md


---

## Framework
**Source:** [guides/plugins/plugins/framework.md](https://developer.shopware.com/docs/v6.6/guides/plugins/plugins/framework.md)  
# Framework

Shopware is a flexible e-commerce framework that allows developers to extend and customize the platform according to specific business needs, creating scalable and personalized online stores. The Shopware framework offers data abstraction, custom fields, events, rules, message queues, file systems, flows, and rate limiters.

More about these features and their extensibility is mentioned in the further sections.

---

---

## Caching
**Source:** [guides/plugins/plugins/framework/caching.md](https://developer.shopware.com/docs/guides/plugins/plugins/framework/caching.md)  
*(Body truncated in this bundle; follow the link for the rest.)*

# Caching

Caching is a technique to store frequently accessed data in a temporary storage layer for faster retrieval, reducing latency and improving performance by avoiding repeated and costly data retrieval operations

While caching enhances performance, it requires careful management of data consistency, cache invalidation strategies, and storage efficiency to prevent serving outdated or incorrect data.

This guide will show you how you can modify the default caching mechanisms to suite your needs. If you are looking for information on how to add your routes to the HTTP-Cache, take a look at [this guide](../../storefront/add-caching-to-custom-controller.md).

## Cache Layers

The current cache system of Shopware is based on a multi-layer system, in which the individual layers build on each other to improve performance and scalability.
There is the [HTTP-Cache](../../../../../concepts/framework/http_cache.md) on the outer level and then multiple smaller internal "Object Caches" that are used to cache data in the application.

For information on how to configure the different cache layers, please refer to the [caching hosting guide](../../../../hosting/performance/caches.md).

### HTTP-Cache

Before jumping in and adjusting the HTTP-Caching, please familiarize yourself with the general [HTTP-Cache concept](../../../../../concepts/framework/http_cache.md) first.

#### Manipulating the cache key

There are several entry points to manipulate the cache key.

* `Shopware\Core\Framework\Adapter\Cache\Http\Extension\CacheHashRequiredExtension`: used to determine whether the cache hash should be calculated or if the request in running in the default state, and therefore no cache-hash is needed.
* `Shopware\Core\Framework\Adapter\Cache\Event\HttpCacheCookieEvent`: used to calculate the cache hash based on the application state, supports both reverse proxy caches and the default symfony HTTP-cache component.
* `Shopware\Core\Framework\Adapter\Cache\Http\Extension\ResolveCacheRelevantRuleIdsExtension`: used to determine which rule IDs are relevant for the cache hash.
* `Shopware\Core\Framework\Adapter\Cache\Event\HttpCacheKeyEvent`: used to calculate the exact cache key based on the response, only for symfony's default HTTP-cache component.

##### Modifying when the cache hash is calculated

By default, the cache hash is only calculated when the request is not in the default state, which is: no logged in customer, default currency, and an empty cart.
The reason is that the very first request to the application from a client should always be cached in the best case, the state that the application is in then is the "default state", which does not require a cache hash.
You can overwrite the default behaviour and add more conditions where the cache hash needs to be applied, e.g., when you shop needs to be more dynamic e.g. based on campaign query parameters:

```php
class RequireCacheHash implements EventSubscriberInterface
{
    public static function getSubscribedEvents(): array
    {
        return [
            CacheHashRequiredExtension::NAME . '.post' => 'onRequireCacheHash',,
        ];
    }

    public function onRequireCacheHash(CacheHashRequiredExtension $extension): void
    {
        if ($extension->request->query->has('campaignId')) {
            $extension->result = true;
        }
    }
}
```

##### Modifying the cache hash

The cache hash is used as the basis for the cache key.
It is calculated based on the application state, which includes the current user, the current language, and so on.
As the cache hash is calculated based on the application state, you have access to the resolved `SalesChannelContext` to determine the cache hash.
It is stored alongside the response as a cookie and thus also provided with all following requests, to allow differentiating the cache based on the application state.
As the cache hash will be carried over to the next request, the computed cache hash can be used inside reverse proxy caches as well as the default symfony HTTP-cache component.

:::info
The cache hash is only computed on every response as soon as the application state differs from the default state, which is: no logged in customer, default currency, and an empty cart.
:::

By default, the cache hash will consist of the following parts:

* `rule-ids`: The matched rule IDs, to reduce possible cache permutations starting with v6.8.0.0, this will only include the rule IDs in `rule areas` that are cache relevant. See the next chapter how to extend this.
* `version-id`: The context version used to load versioned DAL entities.
* `currency-id`: The currency ID of the context.
* `tax-state`: The tax state of the context (gross/net).
* `logged-in`: Whether a customer is logged in in the current state or not.

To modify the cache hash, you can subscribe to the `HttpCacheCookieEvent` event and add your own parts to the cache hash.
This allows you to add more parts to the cache hash, e.g., the current customer's group.
You can also disable the cache for certain conditions, because if that condition is met, the content is so dynamic that caching is not efficiently possible e.g., if the cart is filled.

```php
class HttpCacheCookieListener implements EventSubscriberInterface
{
    public function __construct(
        private readonly CartService $cartService
    ) {
    }
    
    public static function getSubscribedEvents(): array
    {
        return [
            HttpCacheCookieEvent::class => 'onCacheCookie',
        ];
    }

    public function onCacheCookie(HttpCacheCookieEvent $event): void
    {
        // you can add custom parts to the cache hash
        // keep in mind that every possible value will increase the number of possible cache permutations
        // and therefore directly impact cache hit rates, which in turn decreases performance
        $event->add('customer-group', $event->context->getCustomerId());

        // disable cache for filled carts
        $cart = $this->cartService->getCart($event->context->getToken(), $event->context);
        if ($cart->getLineItems()->count() > 0) {
            // you can also explicitly disable caching based on specific conditions
            $event->isCacheable = false;
        }
    }
}
```

Additionally, you can modify the cache hash from the frontend client directly by adding separate cookies with the relevant value.
You can configure custom cookies that are relevant for the cache hash in the `shopware.http_cache.cookies` option:

```yaml
shopware:
    http_cache:
        cookies:
            - 'my-custom-cookie'
```

As soon as the cookie is set, that value will be included in the cache hash.
Essentially, it saves you the effort to implement a custom cache cookie listener as shown above.
This makes it especially suited for headless projects where the frontend implementation is more decoupled from the backend.

##### Marking rule areas as cache relevant

Starting with v6.8.0.0, the cache hash will only include the rule IDs in `rule areas` that are cache relevant.
The reason is that a lot of rules are not relevant for the cache, e.g., rules that only affect pricing or shipping methods.
This greatly reduces the number of possible cache permutations, which in turn improves the cache hit rate.

By default, only the following rule areas are cache relevant:

* `RuleAreas::PRODUCT_AREA`

If you use the rule system in a way that is relevant for the cache (because the response differs based on the rules), you should add your rule area to the list of cache relevant rule areas.
To do so, you need to subscribe to the `ResolveCacheRelevantRuleIdsExtension` event.

```php
class ResolveRuleIds implements EventSubscriberInterface
{
    public static function getSubscribedEvents(): array
    {
        return [
            ResolveCacheRelevantRuleIdsExtension::NAME . '.pre' => 'onResolveRuleAreas',
        ];
    }

    public function onResolveRuleAreas(ResolveCacheRelevantRuleIdsExtension $extension): void
    {
        $extension->ruleAreas[] = RuleExtension::MY_CUSTOM_RULE_AREA;
    }
}
```

This implies that you defined the rule area in your custom entities that have an associated rule entity, by using the DAL flag `Shopware\Core\Framework\DataAbstractionLayer\Field\Flag\RuleAreas` on the rule association in the entity extension.

```php
class RuleExtension extends EntityExtension
{
    public const MY_CUSTOM_RULE_AREA = 'custom';

    public function getEntityName(): string
    {
        return RuleDefinition::ENTITY_NAME;
    }

    public function extendFields(FieldCollection $collection): void
    {
        $collection->add(
            (new ManyToManyAssociationField(
                'myPropertyName',
                MyCustomDefinition::class,
                MyMappingDefinition::class,
                RuleDefinition::ENTITY_NAME . '_id',
                MyCustomDefinition::ENTITY_NAME . '_id',
            ))->addFlags(new CascadeDelete(), new RuleAreas(self::MY_CUSTOM_RULE_AREA)),
        );
    }
}
```

For details on how to extend core definitions refer to the [DAL Guide](../../framework/data-handling/add-complex-data-to-existing-entities.md).

##### Modifying the cache keys

You can also modify the exact cache key used to store the response in the [symfony HTTP-Cache](https://symfony.com/doc/current/http_cache.html).
If possible, you should manipulate the cache hash (as already explained above) instead, as that is also used in reverse proxy caches.
You can do so by subscribing to the `HttpCacheKeyEvent` event and add your specific part to the key.

```php
class CacheKeySubscriber implements EventSubscriberInterface
{
    public static function getSubscribedEvents(): array
    {
        return [
            HttpCacheKeyEvent::class => 'addKeyPart',
        ];
    }
    
    public function addKeyPart(HttpCacheKeyEvent $event): void
    {
        $request = $event->request;
        // Perform checks to determine the key
        $key = $this->determineKey($request);
        $event->add('myCustomKey', $key);
        
        // You can also disable caching for certain conditions
        $event->isCacheable = false;
    }
}
```

:::info
The event is called on any Request; make sure that you don't use expensive operations like Database Queries.

Also, with an external reverse proxy, the cache key might be generated on the proxy and not in your application. In that case, you need to add the key part to the reverse proxy configuration.
:::

#### Adding cache tags

One problem with caching is that you not only need to retrieve the correct data, but also need to have a performant way to invalidate the cache when the data changes.
Only invalidating the caches based on the unique cache key is often not that helpful, because you don't know which cache keys are affected by the change of a specific data set.
Therefore, a tagging system is used alongside the cache keys to make cache invalidations easier and more performant. Every cache entry can be tagged with multiple tags, thus we can invalidate the cache based on the tags.
For example, all pages that contain product data are tagged with product IDs of all products they contain. So if a product is changed, we can invalidate all cache entries that are tagged with the product ID of the changed product.

To add your own cache tags to the HTTP-Cache, you can use the `CacheTagCollector` service.

```php
class MyCustomEntityExtension
{
    public function __construct(
        private readonly CacheTagCollector $cacheTagCollector,
    ) {}
    
    public function loadAdditionalData(): void
    {
        // Load the additional data you need, add it to the response, then add the correct tag to the cache entry
        $this->cacheTagCollector->addTag('my-custom-entity-' . $idOfTheLoadedData);
    }
}
```

#### Invalidating the cache

Adding custom cache tags is only useful if you also use them to invalidate the cache when the data changed.
To invalidate the cache, you need to call the `CacheInvalidator`

… **Truncated.** Full document: https://developer.shopware.com/docs/guides/plugins/plugins/framework/caching.md


---

## Custom Fields
**Source:** [guides/plugins/plugins/framework/custom-field.md](https://developer.shopware.com/docs/v6.6/guides/plugins/plugins/framework/custom-field.md)  
# Custom Fields

Custom fields in Shopware refer to additional data fields that can be added to entities such as products, customers, or orders. These fields allow businesses to store and manage extra information that may be specific to their operations.

With custom fields, you can define and store data beyond the standard attributes provided by Shopware. For example, a clothing store might add a custom field to track fabric composition, while a hardware store could add a custom field to store product dimensions.

Through the administration or via the API, users can create and manage custom fields, define their data types (such as text, number, date, etc.), and assign them to specific entities. This allows businesses the ability to extend the default data structure enabling a more tailored and personalized e-commerce experience.

---

---

## Add Custom Field
**Source:** [guides/plugins/plugins/framework/custom-field/add-custom-field.md](https://developer.shopware.com/docs/v6.6/guides/plugins/plugins/framework/custom-field/add-custom-field.md)  
*(Body truncated in this bundle; follow the link for the rest.)*

# Add Custom Field

## Overview

Shopware's custom field system allows you to extend entities, without writing a complete entity extension. This is possible by storing the additional data in a [JSON-Field](https://dev.mysql.com/doc/refman/8.0/en/json.html). Custom fields therefore can only be used to store scalar values. If you'd like to create associations between entities, you'll need to use an [Entity extension](../data-handling/add-complex-data-to-existing-entities).

This guide will cover two similar subjects:

* Supporting custom fields with your entity
* Add custom fields to an entity

## Prerequisites

This guide is built upon both the [Plugin base guide](../../plugin-base-guide) as well as the [Add custom complex data](../data-handling/add-custom-complex-data) guide. The latter explained how to create your very first entity, which is used in the following examples.

Since migrations will also be used here, it won't hurt to have a look at our guide about [Executing database queries](../../plugin-fundamentals/database-migrations).

Also, adding translatable custom fields is covered here in short as well, for which you'll need to understand how translatable entities work in general. This is covered in our guide about [Adding data translations](../data-handling/add-data-translations). This subject will **not** be covered in depth in this guide.

## Supporting custom fields with your entity

This short section will cover how to add a custom field support for your custom entity. As previously mentioned, the example from our [Add custom complex data](../data-handling/add-custom-complex-data) guide is used and extended here.

In order to support custom fields with your custom entity, there are three necessary steps :

* Add `EntityCustomFieldsTrait` trait to your `Entity`.
* Add a `CustomFields` field to your `EntityDefinition`.
* Add a column `custom_fields` to your entities' database table via migration.

Also, you may want to add translatable custom fields, which is also covered in very short here.

### Add custom field to entity

::: info
Available starting with Shopware 6.4.1.0.
:::

Let's assume you already got a working and running entity definition. If you want to support custom fields with your custom entity, you may add the `EntityCustomFieldsTrait` to your entity class, so the methods `getCustomFields()` and `setCustomFields()` can be used.

```php
// <plugin root>/src/Core/Content/Example/ExampleEntity.php
use Shopware\Core\Framework\DataAbstractionLayer\Entity;
use Shopware\Core\Framework\DataAbstractionLayer\EntityCustomFieldsTrait;
use Shopware\Core\Framework\DataAbstractionLayer\EntityIdTrait;

[...]
class ExampleEntity extends Entity
{
    use EntityIdTrait;
    use EntityCustomFieldsTrait;

    [...]

}
```

### Add custom field to entity definition

Now follows the important part. For this to work, you have to add the Data Abstraction Layer (DAL) field `CustomFields` to your entity definition.

```php
// <plugin root>/src/Core/Content/Example/ExampleDefinition.php
use Shopware\Core\Framework\DataAbstractionLayer\Field\CustomFields;                                                                    

[...]
class ExampleDefinition extends EntityDefinition
{

    [...]

    protected function defineFields(): FieldCollection
    {
        return new FieldCollection([
            (new IdField('id', 'id'))->addFlags(new Required(), new PrimaryKey()),
            (new StringField('name', 'name')),
            (new StringField('description', 'description')),
            (new BoolField('active', 'active')),

            new CustomFields()
        ]);
    }
}
```

Note the new field that was added in the `FieldCollection`. That's already it for your custom entity definition. Now go ahead and add the column to the database.

### Add column in database table

Once again, this example is built upon the [Add custom complex data](../data-handling/add-custom-complex-data) guide, which also comes with an example migration. This one will be used in this example here as well.

If you want to support custom fields now, you have to add a new column `custom_fields` of type `JSON` to your migration.

```php
// <plugin root>/src/Migration/Migration1611664789Example.php
public function update(Connection $connection): void
{
    $sql = <<<SQL
        CREATE TABLE IF NOT EXISTS `swag_example` (
        `id` BINARY(16) NOT NULL,
        `name` VARCHAR(255) COLLATE utf8mb4_unicode_ci,
        `description` VARCHAR(255) COLLATE utf8mb4_unicode_ci,
        `active` TINYINT(1) COLLATE utf8mb4_unicode_ci,

        `custom_fields` json DEFAULT NULL,

        `created_at` DATETIME(3) NOT NULL,
        `updated_at` DATETIME(3),
        PRIMARY KEY (`id`)
        )
        ENGINE = InnoDB
        DEFAULT CHARSET = utf8mb4
        COLLATE = utf8mb4_unicode_ci;
    SQL;
    $connection->executeStatement($sql);
}
```

Note the new `custom_fields` column here. It has to be a JSON field and should default to `NULL`, since it doesn't have to contain values.

### Add translatable custom field to entity definition

Make sure to understand entity translations in general first, which is explained here [Add data translations](../data-handling/add-data-translations). If you want your custom fields to be translatable, you can simply work with a `TranslatedField` here as well.

```php
// <plugin root>/src/Core/Content/Example/ExampleDefinition.php
use Shopware\Core\Framework\DataAbstractionLayer\Field\TranslatedField;                                                               

[...]

class ExampleDefinition extends EntityDefinition
{
    [...]

    protected function defineFields(): FieldCollection
    {
        return new FieldCollection([
            (new IdField('id', 'id'))->addFlags(new Required(), new PrimaryKey()),
            (new StringField('name', 'name')),
            (new StringField('description', 'description')),
            (new BoolField('active', 'active')),

            new TranslatedField('customFields'),
        ]);
    }
}
```

Just add the `TranslatedField` and apply `customFields` as a parameter.

In your translated entity definition, you then add the `CustomFields` field instead.

```php
// <plugin root>/src/Core/Content/Example/Aggregate/ExampleTranslation/ExampleTranslationDefinition.php
use Shopware\Core\Framework\DataAbstractionLayer\Field\CustomFields;                                                                    

[...]
class ExampleTranslationDefinition extends EntityTranslationDefinition
{
    [...]

    protected function defineFields(): FieldCollection
    {
        return new FieldCollection([
            (new StringField('name', 'name'))->addFlags(new Required()),

            new CustomFields()
        ]);
    }
}
```

## Add custom fields to an entity

The previous section was about adding support for custom fields in your entity, but this section will cover how to add an actual custom field to an entity and how to fill it with data.

Technically, there is no need to define a custom field set and its fields first, before actually inserting values into the `custom_fields` column of your entities' database table via the DAL. Defining a custom field set is only necessary, if you want it to be editable in the Administration or if you need validation when writing your custom field.

Because of that, we'll start with filling data to an actual entities' custom field, before actually defining it.

### Filling data into custom fields

So let's assume you've got your own `example` entity up and running and now you want to add data to its custom fields via the DAL.

For that case, you can simply use your entities' repository and start creating or updating entities with custom fields. If you don't understand what's going on here, head over to our guide about [Writing data](../data-handling/writing-data) first.

```php
$this->swagExampleRepository->upsert([[
    'id' => '<your ID here>',
    'customFields' => ['swag_example_size' => 15]
]], $context);
```

This will execute perfectly fine and you just saved a custom field with name `swag_example_size` with its value `15` to your entity. And you haven't even defined the custom field `swag_example_size` yet.

As already mentioned, you do not have to define a custom field first before saving it. That's because there is no validation happening here yet, you can write whatever valid JSON you want to that column, so the following example would also execute without any issues:

```php
$this->swagExampleRepository->upsert([[
    'id' => '<your ID here>',
    'customFields' => [ 'foo' => 'bar', 'baz' => [] ]
]], $context);
```

### Add a custom field to the Administration

You can skip this section if you don't want your new custom field to be editable in the Administration.

So now you've already filled the custom fields of one of your entity instances via code. But what if you want your user to do that, which is the more common case?

Only if you want your custom field to show up in the Administration and to be editable in there, you have to define the custom fields first in a custom field set. For this you have to use the custom fieldset repository, which can be retrieved from the dependency injection container via the `custom_field_set.repository` key and is used like any other repository.

```xml
<?xml version="1.0" ?>
<container xmlns="http://symfony.com/schema/dic/services"
           xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
           xsi:schemaLocation="http://symfony.com/schema/dic/services http://symfony.com/schema/dic/services/services-1.0.xsd">

    <services>
        <service id="Swag\BasicExample\CustomFieldClass">
          <argument type="service" id="custom_field_set.repository"/>
          ...
        </service>
    </services>
</container>
```

If you need to learn how that is done in full, head to our guide regarding [Writing data](../data-handling/writing-data).

Now use the `create` method of the repository to create a new custom field set.

```php
use Shopware\Core\System\CustomField\CustomFieldTypes;
use \Shopware\Core\Defaults;

[...]

$this->customFieldSetRepository->create([
    [
        'name' => 'swag_example_set',
        'config' => [
            'label' => [
                'en-GB' => 'English custom field set label',
                'de-DE' => 'German custom field set label',
                Defaults::LANGUAGE_SYSTEM => "Mention the fallback label here"
            ]
        ],
        'customFields' => [
            [
                'name' => 'swag_example_size',
                'type' => CustomFieldTypes::INT,
                'config' => [
                    'label' => [
                        'en-GB' => 'English custom field label',
                        'de-DE' => 'German custom field label',
                        Defaults::LANGUAGE_SYSTEM => "Mention the fallback label here"
                    ],
                    'customFieldPosition' => 1
                ]
            ]
        ]
    ]
], $context);
```

This will now create a custom field set with the name `swag_example_set` and the field, `swag_example_size`. This time we also define its type, which should be of type integer here. The type is important to mention, because the Administration will use this information to display a proper field. Also, when trying to write the custom field `swag_example_size`, the value has to be an integer.

The translated labels are added to both the field and the set, which are going to be displayed in the Administration. Also, the fallback language can be defined in case the system language is not guaranteed to be either en\_GB or de\_DE.

If you have several custom fields and want to order them within a specific order, you can do so with the `customFieldPosition` property.

::: warning
Custom field sets are deletable by the shop administrator, so you cannot rely on their existence.
:::

To update or delete a `custom_field_set`, you can use the standard repository methods lik

… **Truncated.** Full document: https://developer.shopware.com/docs/v6.6/guides/plugins/plugins/framework/custom-field/add-custom-field.md


---

## Fetching Data from "Entity Selection" Custom Field
**Source:** [guides/plugins/plugins/framework/custom-field/fetching-data-from-entity-selection.md](https://developer.shopware.com/docs/v6.6/guides/plugins/plugins/framework/custom-field/fetching-data-from-entity-selection.md)  
# Fetching Data from "Entity Selection" Custom Field

## Overview

If you set up a custom field with an entity selection in the Administration, you may need a data resolver to resolve the ID to an entity object.

## Prerequisites

This guide will not explain how to create custom field in general, so head over to the official guide about [custom field](add-custom-field) to learn this first.

## Fetching data

In this example we assume that we already set up a custom field called `custom_linked_product`, which is assigned to the products entity. The type of the custom field `custom_linked_product` is also a product.

If you now update a product in the Administration and select a value for `custom_linked_product` only the `id` of the selected product entity gets store in the custom field.

To resolve the `id` and getting access to the product we have linked here, we can create a `ProductSubscriber` which listens to the `ProductEvents::PRODUCT_LOADED_EVENT`. The event will be triggered, when the associated main product will be loaded. So we can easily resolve the id in the custom field.

Lets create a `ProductSubscriber` first which will listen to the `ProductEvents::PRODUCT_LOADED_EVENT`.

```php
// <plugin root>/src/Subscriber/ProductSubscriber.php
<?php declare(strict_types=1);

namespace Swag\BasicExample\Subscriber;

use Shopware\Core\Framework\DataAbstractionLayer\Event\EntityLoadedEvent;
use Symfony\Component\EventDispatcher\EventSubscriberInterface;
use Shopware\Core\Content\Product\ProductEvents;

class ProductSubscriber implements EventSubscriberInterface
{
    public static function getSubscribedEvents(): array
    {
        return [
            ProductEvents::PRODUCT_LOADED_EVENT => 'onProductLoaded'
        ];
    }

    public function onProductLoaded(EntityLoadedEvent $event): void
    {
    }
}
```

For this subscriber to work we need to register it in the service container via the `services.xml` file:

```xml
// <plugin root>/src/Resources/config/services.xml
<?xml version="1.0" ?>

<container xmlns="http://symfony.com/schema/dic/services"
           xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
           xsi:schemaLocation="http://symfony.com/schema/dic/services http://symfony.com/schema/dic/services/services-1.0.xsd">

    <services>
        <service id="Swag\BasicExample\Subscriber\ProductSubscriber">
            <tag name="kernel.event_subscriber"/>
        </service>
    </services>
</container>
```

Now our `ProductSubscriber` should be called every time a product is loaded, so we can resolve the custom field `custom_linked_product`.

```php
// <plugin root>/src/Subscriber/ProductSubscriber.php
<?php declare(strict_types=1);

namespace Swag\BasicExample\Subscriber;

use Shopware\Core\Framework\DataAbstractionLayer\Event\EntityLoadedEvent;
use Symfony\Component\EventDispatcher\EventSubscriberInterface;
use Shopware\Core\Content\Product\ProductEvents;

class ProductSubscriber implements EventSubscriberInterface
{
    public static function getSubscribedEvents(): array
    {
        return [
            ProductEvents::PRODUCT_LOADED_EVENT => 'onProductLoaded'
        ];
    }

    public function onProductLoaded(EntityLoadedEvent $event): void
    {

        // loop through all loaded product      
        /** @var ProductEntity $productEntity */
        foreach ($event->getEntities() as $productEntity) {
            $customFields = $productEntity->getCustomFields();

            // loop through each product's custom fields
            foreach($customFields as $name => $value) {
                if ($name !== 'custom_linked_product' || empty($value)) {
                    continue;
                }

               // resolve the $value here
            }

            $productEntity->setCustomFields($customFields);
        }
    }
}
```

Inside the `onProductLoaded` method we can get access to the loaded product entities by calling `$event->getEntities()`. Now for every product we look for our `custom_linked_product` custom field.

But, how we can load the linked product by its `id` if the custom field was set? We have to inject the product repository to achieve it.

First we update the `services.xml` and inject the product repository.

```xml
// <plugin root>/src/Resources/config/services.xml
<?xml version="1.0" ?>

<container xmlns="http://symfony.com/schema/dic/services"
           xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
           xsi:schemaLocation="http://symfony.com/schema/dic/services http://symfony.com/schema/dic/services/services-1.0.xsd">

    <services>
        <service id="Swag\BasicExample\Subscriber\ProductSubscriber">
            <argument type="service" id="product.repository"/>
            <tag name="kernel.event_subscriber"/>
        </service>
    </services>
</container>
```

Now we can use the product repository in our subscriber.

```php
// <plugin root>/src/Subscriber/ProductSubscriber.php
<?php declare(strict_types=1);

namespace Swag\BasicExample\Subscriber;

use Shopware\Core\Content\Product\ProductEntity;
use Shopware\Core\Framework\DataAbstractionLayer\EntityRepository;
use Shopware\Core\Framework\DataAbstractionLayer\Event\EntityLoadedEvent;
use Shopware\Core\Framework\DataAbstractionLayer\Search\Criteria;
use Symfony\Component\EventDispatcher\EventSubscriberInterface;
use Shopware\Core\Content\Product\ProductEvents;

class ProductSubscriber implements EventSubscriberInterface
{
    private EntityRepository $productRepository;

    public function __construct(EntityRepository $productRepository) 
    {
        $this->productRepository = $productRepository;
    }

   //...
}
```

As you can see, the product repository was injected and is now available to the `ProductRepository`. The last step is to resolve the `custom_linked_product` value inside the `onProductLoaded` method.

Let's have a look at the final implementation of the subscriber.

```php
// <plugin root>/src/Subscriber/ProductSubscriber.php
<?php declare(strict_types=1);

namespace Swag\BasicExample\Subscriber;

use Shopware\Core\Content\Product\ProductEntity;
use Shopware\Core\Framework\DataAbstractionLayer\EntityRepository;
use Shopware\Core\Framework\DataAbstractionLayer\Event\EntityLoadedEvent;
use Shopware\Core\Framework\DataAbstractionLayer\Search\Criteria;
use Symfony\Component\EventDispatcher\EventSubscriberInterface;
use Shopware\Core\Content\Product\ProductEvents;

class ProductSubscriber implements EventSubscriberInterface
{
    private EntityRepository $productRepository;

    public function __construct(EntityRepository $productRepository) 
    {
        $this->productRepository = $productRepository;
    }

    public static function getSubscribedEvents(): array
    {
        return [
            ProductEvents::PRODUCT_LOADED_EVENT => 'onProductLoaded'
        ];
    }

    public function onProductLoaded(EntityLoadedEvent $event): void
    {
        // extract all ids of our custom field
        $ids = array_map(function (ProductEntity $entity) {
            return $entity->getCustomFields()['custom_demo_test'] ?? null;
        }, $event->getEntities());

        // filter empty ids
        $ids = array_filter($ids);

        // load all products in one request instead of one request per product (big performance boost)
        $products = $this->productRepository->search(new Criteria($ids), $event->getContext());

        /** @var ProductEntity $entity */
        foreach ($event->getEntities() as $entity) {
            // check if the custom field is set
            if (!$id = $entity->getCustomFields()['custom_demo_test'] ?? null) {
                continue;
            }

            // add the product to the entity as entity extension
            $entity->addExtension('my_custom_demo_product', $products->get($id));
        }
    }
}
```

---

---

## Event
**Source:** [guides/plugins/plugins/framework/event.md](https://developer.shopware.com/docs/v6.6/guides/plugins/plugins/framework/event.md)  
# Event

Shopware events provide a flexible and powerful way to extend the functionality of the e-commerce platform. Events in Shopware are triggered at specific actions. You can extend the platform's functionality by intercepting and executing custom logic during specific system actions. By leveraging events like Storefront events, administration events, or flow builder events, to mention a few,  developers can hook into core system actions, such as order placement or product updates, and perform additional tasks, such as sending notifications, modifying data, or integrating with external services, etc. This event-driven architecture enables seamless integration of custom functionalities, making it easier to extend and customize the Shopware platform to meet specific business requirements.

---

---

## Add Custom Event
**Source:** [guides/plugins/plugins/framework/event/add-custom-event.md](https://developer.shopware.com/docs/v6.6/guides/plugins/plugins/framework/event/add-custom-event.md)  
# Add Custom Event

## Overview

In this guide, you will learn how to create your own event. You can read more about events in the [Symfony documentation](https://symfony.com/doc/current/event_dispatcher.html).

## Prerequisites

To create your own event for your plugin, you first need a plugin as base. Therefore, you can refer to the [Plugin Base Guide](../../plugin-base-guide).

::: info
Refer to this video on **[Event dispatching and handling](https://www.youtube.com/watch?v=JBpa5nBoC78)** which is a live coding example on custom events. Also available on our free online training ["Shopware 6 Backend Development"](https://academy.shopware.com/courses/shopware-6-backend-development-with-jisse-reitsma).
:::

## Event interfaces and classes

In Shopware, you have multiple interfaces and classes for different types of events, in the following you can find a list of them:

* `ShopwareEvent`: This interface is just a basic event providing a `Context` we need for almost all events.
* `ShopwareSalesChannelEvent`: This interface extends from `ShopwareEvent` and additionally provides a `SalesChannelContext`.
* `SalesChannelAware`: This interface provides the `SalesChannelId`.
* `GenericEvent`: This interface will be used if you want to give your event a specific name like the database events (e.g. `product.written.`). Otherwise, you have to reference to the event class.
* `NestedEvent`: This class will be used for events using other events, for example, the `EntityDeletedEvent` extends from the `EntityWrittenEvent`.
* `BusinessEventInterface`: This interface extends from `ShopwareEvent` and will be used for dynamic assignment and is always named.

## Create the event class

First, we create a new class for our event, which we name `ExampleEvent`. In this example we implement the `Shopware\Core\Framework\Event\ShopwareSalesChannelEvent`. As mentioned above our class already implements a method for the `SalesChannelContext` and the `Context`. Now we pass an `ExampleEntity` and the `SalesChannelContext` through the constructor and create a function which returns our `ExampleEntity`.

Therefore, this is what your event class could look like:

```php
// <plugin root>/src/Core/Content/Example/Event/ExampleEvent.php
<?php declare(strict_types=1);

namespace Swag\BasicExample\Core\Content\Example\Event;

use Shopware\Core\Framework\Context;
use Shopware\Core\Framework\Event\ShopwareSalesChannelEvent;
use Shopware\Core\System\SalesChannel\SalesChannelContext;
use Swag\BasicExample\Core\Content\Example\ExampleEntity;

class ExampleEvent implements ShopwareSalesChannelEvent
{
    protected ExampleEntity $exampleEntity;

    protected SalesChannelContext $salesChannelContext;

    public function __construct(ExampleEntity $exampleEntity, SalesChannelContext $context)
    {
        $this->exampleEntity = $exampleEntity;
        $this->salesChannelContext = $context;
    }

    public function getExample(): ExampleEntity
    {
        return $this->exampleEntity;
    }

    public function getContext(): Context
    { 
        return $this->salesChannelContext->getContext();
    }

    public function getSalesChannelContext(): SalesChannelContext
    {
        return $this->salesChannelContext;
    }
}
```

## Fire the event

After we've created our event class, we need to fire our new event. For this we need the service `event_dispatcher` which provides a method called `dispatch`. In this example we created a service `ExampleEventService` which fires our event. Below, you can find the example implementation.

```php
// <plugin root>/src/Service/ExampleEventService.php
<?php declare(strict_types=1);

namespace Swag\BasicExample\Service;

use Shopware\Core\System\SalesChannel\SalesChannelContext;
use Swag\BasicExample\Core\Content\Example\Event\ExampleEvent;
use Swag\BasicExample\Core\Content\Example\ExampleEntity;
use Symfony\Contracts\EventDispatcher\EventDispatcherInterface;

class ExampleEventService
{
    private EventDispatcherInterface $eventDispatcher;

    public function __construct(EventDispatcherInterface $eventDispatcher)
    {
        $this->eventDispatcher = $eventDispatcher;
    }

    public function fireEvent(ExampleEntity $exampleEntity, SalesChannelContext $context)
    {
        $this->eventDispatcher->dispatch(new ExampleEvent($exampleEntity, $context));
    }
}
```

## Next steps

Now that you know how to create your own event, you may want to act on it. To get a grip on this, head over to our [Listening to events](../../plugin-fundamentals/listening-to-events) guide.

---

---

## Finding Events
**Source:** [guides/plugins/plugins/framework/event/finding-events.md](https://developer.shopware.com/docs/v6.6/guides/plugins/plugins/framework/event/finding-events.md)  
*(Body truncated in this bundle; follow the link for the rest.)*

# Finding Events

## Overview

Shopware 6 is fully extensible via plugins.
Part of this extensibility is the usage of events, upon which one could react.

This guide will cover how you can find those events in the first place, in order to use them in your plugin.

## DAL Events

At first we will start with the [Data Abstraction Layer events](../data-handling/using-database-events).
They're fired whenever a [DAL entity](../data-handling/add-custom-complex-data) is read, written, created, or deleted.

There usually is no need to find them, since the pattern for them is always the same.
You can use them by following this pattern: `entity_name.event`.
For products, this could be e.g. `product.written` or `product.deleted`. For your custom entity, this then would be
`custom_entity.written` or `custom_entity.deleted`.

However, some default Shopware entities come with special "Event classes", which are basically a class, which contains all
possible kinds of events as constants.
Have a look at the [product event class](https://github.com/shopware/shopware/blob/v6.4.0.0/src/Core/Content/Product/ProductEvents.php) for example.
This way you can also find out about all the possible DAL events available in Shopware.

Finding those "event classes" can be done by searching for the term `@Event` in your project.

You can use those events in a [subscriber](../../plugin-fundamentals/listening-to-events) like the following:

```php
public static function getSubscribedEvents(): array
{
    return [
        ProductEvents::PRODUCT_LOADED_EVENT => 'onProductsLoaded',
        'custom_entity.written' => 'onCustomEntityWritten'
    ];
}
```

As you can see, you can either use the event class constants, if available, or the string itself.

You'll then have access to several event specific information, e.g. your listener method will have access to an [EntityWrittenEvent](https://github.com/shopware/shopware/blob/v6.4.0.0/src/Core/Framework/DataAbstractionLayer/Event/EntityWrittenEvent.php)
instance when subscribing to the `written` event.

```php
public function onCustomEntityWritten(EntityWrittenEvent $event): void
{
}
```

You can find all of those DAL event classes [here](https://github.com/shopware/shopware/tree/v6.4.0.0/src/Core/Framework/DataAbstractionLayer/Event).

## General PHP events

If the \[DAL events]\(#DAL events) didn't match your use case, there are a few more events built into Shopware.
These are not auto-generated events, but rather events we built in with purpose.

There are multiple ways to find them:

* By actually looking at the code, that you want to extend
* By specifically searching for them
* By having a look at the service definition of a given class

### Looking at the code

You will most likely look into our Core code quite a lot, while trying to understand what's happening and why things are happening.
On your journey looking through the code, you may stumble upon code looking like this:

```php
$someEvent = new SomeEvent($parameters, $moreParameters);
$this->eventDispatcher->dispatch($someEvent, $someEvent->getName());
```

This is an event that's being fired manually, which you can react upon.
Make sure to always have a look at the event class itself in order to find out which information it contains.

The second parameter of the `dispatch` is optional and represents the actual event's name.
If the second parameter is not applied, the class name will be used as a fallback.

When subscribing to those events, your event listener method will have access to the previously created event instance.

```php
public static function getSubscribedEvents(): array
{
    return [
        'some_event' => 'registeringToSomeEvent',
        // If there is no name applied to the event, the class name is the fallback
        SomeEvent::class => 'registeringToSomeEvent'
    ];
}

public function registeringToSomeEvent(SomeEvent $event): void
{
}
```

The \[next section]\(#Specifically searching for events) will cover how to find those events without randomly stumbling upon them.

### Specifically searching for events

If you're really looking for a fitting event for your purpose, you might want to directly search for them.
This can be done by searching through the `<shopware root>/platform/src` or the `<shopware root>/vendor/shopware/shopware/src` directory,
depending on whether you are using the [development](https://github.com/shopware/development) or the [production template](https://github.com/shopware/production).
Use one of the following search terms:

* `extends NestedEvent`: This way you will find the events themselves.
* `extends Event`: This way you will find the events themselves.
* `implements ShopwareEvent`: This way you will find the events themselves.
* `->dispatch`: Here you will find all the occurrences where the events are actually being fired.

### Looking at the service definition

Every service, that wants to fire an event sooner or later, needs access to the `event_dispatcher` in order to do so.

Hence, you can have a look at all the service definitions for the [Dependency injection container](../../plugin-fundamentals/dependency-injection)
and therefore quickly figure out, which services and classes are having access to the said `event_dispatcher`:

```xml
<?xml version="1.0" ?>

<container xmlns="http://symfony.com/schema/dic/services"
           xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
           xsi:schemaLocation="http://symfony.com/schema/dic/services http://symfony.com/schema/dic/services/services-1.0.xsd">

    <services>
        <service id="Some\Service">
            <argument type="service" id="Another/Service"/>
            <argument type="service" id="event_dispatcher"/>
        </service>
    </services>
</container>
```

Therefore, you could simply search for occurrences of the `event_dispatcher` in the respective `.xml` files.

You can also do this the other way around, by having a look at the service's constructor parameters.

```php
public function __construct(
    Some\Service $someService,
    EventDispatcherInterface $eventDispatcher
) {
    $this->someService = $someService;
    $this->eventDispatcher = $eventDispatcher;
}
```

If it's having access to the `EventDispatcherInterface`, you're most likely going to find at least one event being fired
in that service.

### Other common event types

There's a few more event "types" or classes that you may stumble upon, which are worth knowing.

#### Page Loaded Events

Usually when a [Storefront page](../../storefront/add-custom-page) is being loaded, a respective "page is being loaded" event is fired
as well.

You can find an example in the [GenericPageLoader](https://github.com/shopware/shopware/blob/v6.4.0.0/src/Storefront/Page/GenericPageLoader.php), which is kinda a "default page" to be used pretty often.
It dispatches an `GenericPageLoadedEvent` every time the page is being loaded.

This way, you can react to this and e.g. add more meta information to the said page.

You can find those events by searching for the term "PageLoadedEvent".

#### Criteria Events

You should be familiar with the `Criteria` class, at least if you've dealt with the [Data Abstraction Layer](../data-handling/).
There are many methods, that will dispatch a "criteria" event whenever a given default Shopware entity is being loaded using
a `Criteria` instance.

Let's have a look at an [example code](https://github.com/shopware/shopware/blob/v6.4.0.0/src/Core/Content/Product/SalesChannel/Listing/ResolveCriteriaProductListingRoute.php#L55-L59):

```php
#[Route(path: '/store-api/product-listing/{categoryId}', name: 'store-api.product.listing', methods: ['POST'], defaults: ['_entity' => 'product'])]
public function load(string $categoryId, Request $request, SalesChannelContext $context, Criteria $criteria): ProductListingRouteResponse
{
    $this->eventDispatcher->dispatch(
        new ProductListingCriteriaEvent($request, $criteria, $context)
    );

    return $this->getDecorated()->load($categoryId, $request, $context, $criteria);
}
```

So whenever the product listing route is being called, and therefore products are being loaded via the DAL and therefore via a
`Criteria` object, the `ProductListingCriteriaEvent` is being fired.

You can use this event to modify the `Criteria` object and therefore add or remove conditions, add or remove associations etc.
Of course, the code above is just one example excerpt and there are many more of those events for different entities.

Finding those events can be done by searching for the term `CriteriaEvent`.

::: info
Those "criteria events" are not generated automatically and therefore it is not guaranteed to exist for a given entity.
:::

#### Route Events

Symfony provides some general [kernel level routing events](https://symfony.com/doc/current/reference/events.html#kernel-events), e.g `kernel.request` or `kernel.response`.
However, those events are thrown on every route, so it's too generic when you only want to react on a specific route.
Therefore, we have added fine-grained route events that are thrown for every route:
| Event name | Scope | Event Type | Description |
|------------|-------|------------|-------------|
| `{route}.request` | Global | `Symfony\Component\HttpKernel\Event\RequestEvent` | Route specific alias for symfony's `kernel.request` event. |
| `{route}.response` | Global | `Symfony\Component\HttpKernel\Event\ResponseEvent` | Route specific alias for symfony's `kernel.response` event. For storefront routes this contains the already rendered template, for store-api routes this contains the already encoded JSON |
| `{route}.render` | Storefront | `Shopware\Storefront\Event\StorefrontRenderEvent` | Thrown before twig rendering in the storefront. |
| `{route}.encode` | Store-API | `Symfony\Component\HttpKernel\Event\ResponseEvent` | Thrown before encoding the API response to JSON, allowing easy manipulation of the returned data. **Note:** This was only introduced in 6.6.11.0 |
| `{route}.controller` | Global | `\Symfony\Component\HttpKernel\Event\ControllerEvent` | Route specific alias for symfony's `kernel.controller` event. **Note:** This was only introduced in 6.6.11.0 |

To subscribe to a specific event, replace the `{route}` placeholder with the [actual symfony route name](https://symfony.com/doc/current/routing.html), e.g. `store-api.product.listing`.

```php
public static function getSubscribedEvents(): array
{
    return [
        'store-api.product.listing.request' => 'onListingRequest',
        'store-api.product.listing.encode' => 'onListingEncode'
    ];
}

public function onListingRequest(RequestEvent $event): void
{
}

public function onListingEncode(ResponseEvent $event): void
{
}
```

#### Business events

Business events are fired everytime an important business / ecommerce action occurred, such as "A customer registered" or "An order was placed".

Therefore, you can use them to react on those events, most times there even is an event fired **before** an action happened.
Have a look at those two example events:

* [CustomerBeforeLoginEvent](https://github.com/shopware/shopware/blob/v6.4.0.0/src/Core/Checkout/Customer/SalesChannel/AccountService.php#L97-L98)
* [CustomerLoginEvent](https://github.com/shopware/shopware/blob/v6.4.0.0/src/Core/Checkout/Customer/SalesChannel/AccountService.php#L109-L110)

The kind of information they contain and which you can modify is different for each event, so you'll have to have a look at the respective
event classes to find out about it.

Those business events can be found by either searching for the term `implements BusinessEventInterface` or `implements MailActionInterface`.
The latter implement the `MailActionInterface` because they're events which will result in a mail being sent, e.g. when a customer placed an order.
Customer login however will obviously not result in a mail being sent and therefore is "only" implement the `BusinessEventInterface`.

### Using the Symfony profiler

Since Shopware 

… **Truncated.** Full document: https://developer.shopware.com/docs/v6.6/guides/plugins/plugins/framework/event/finding-events.md


---

## Extension Points
**Source:** [guides/plugins/plugins/framework/extension.md](https://developer.shopware.com/docs/guides/plugins/plugins/framework/extension.md)  
# Extension Points

Extension Points allow you to **replace core functionality** by intercepting and modifying the execution flow of system processes, unlike traditional events which are only for notifications.

---

---

## Creating Custom Extension Points
**Source:** [guides/plugins/plugins/framework/extension/creating-custom-extension.md](https://developer.shopware.com/docs/guides/plugins/plugins/framework/extension/creating-custom-extension.md)  
*(Body truncated in this bundle; follow the link for the rest.)*

# Creating Custom Extension Points

## Overview

While Shopware provides many built-in extension points, you may need to create custom extension points for your specific use cases. This guide will walk you through creating custom extension points that follow Shopware's extension system patterns.

## Extension Class Structure

### Basic Extension Class

All extension points must extend the base `Extension` class and define a typed result:

```php
<?php declare(strict_types=1);

namespace MyPlugin\Extension;

use Shopware\Core\Framework\Extensions\Extension;
use Shopware\Core\Framework\Log\Package;

/**
 * @extends Extension<MyResultType>
 */
#[Package('my-plugin')]
final class MyCustomExtension extends Extension
{
    public const NAME = 'my-plugin.custom-extension';
    
    public function __construct(
        /**
         * @public
         * @description Input data for processing
         */
        public readonly array $inputData,
        
        /**
         * @public
         * @description Context for the operation
         */
        public readonly Context $context
    ) {
    }
}
```

### Key Components

1. **Generic Type**: `@extends Extension<ResultType>` defines the return type
2. **NAME Constant**: Unique identifier for the extension
3. **Public Properties**: Input parameters marked with `@public` for API documentation
4. **Package Attribute**: Identifies the package/plugin

## Example: Custom Product Filter Extension

Let's create a custom extension point for filtering products based on custom business logic:

### 1. Define the Extension Class

```php
<?php declare(strict_types=1);

namespace MyPlugin\Extension;

use Shopware\Core\Content\Product\ProductCollection;
use Shopware\Core\Framework\Context;
use Shopware\Core\Framework\DataAbstractionLayer\Search\Criteria;
use Shopware\Core\Framework\DataAbstractionLayer\Search\EntitySearchResult;
use Shopware\Core\Framework\Extensions\Extension;
use Shopware\Core\Framework\Log\Package;
use Shopware\Core\System\SalesChannel\SalesChannelContext;

/**
 * @extends Extension<EntitySearchResult<ProductCollection>>
 */
#[Package('my-plugin')]
final class CustomProductFilterExtension extends Extension
{
    public const NAME = 'my-plugin.product-filter';
    
    public function __construct(
        /**
         * @public
         * @description The search criteria for products
         */
        public readonly Criteria $criteria,
        
        /**
         * @public
         * @description The sales channel context
         */
        public readonly SalesChannelContext $context,
        
        /**
         * @public
         * @description Custom filter parameters
         */
        public readonly array $filterParams
    ) {
    }
}
```

### 2. Create the Service that Dispatches the Extension

```php
<?php declare(strict_types=1);

namespace MyPlugin\Service;

use MyPlugin\Extension\CustomProductFilterExtension;
use Shopware\Core\Content\Product\ProductCollection;
use Shopware\Core\Framework\Context;
use Shopware\Core\Framework\DataAbstractionLayer\EntityRepository;
use Shopware\Core\Framework\DataAbstractionLayer\Search\Criteria;
use Shopware\Core\Framework\DataAbstractionLayer\Search\EntitySearchResult;
use Shopware\Core\Framework\Extensions\ExtensionDispatcher;
use Shopware\Core\Framework\Log\Package;
use Shopware\Core\System\SalesChannel\SalesChannelContext;

#[Package('my-plugin')]
class CustomProductService
{
    public function __construct(
        private readonly ExtensionDispatcher $extensionDispatcher,
        private readonly EntityRepository $productRepository
    ) {
    }
    
    public function filterProducts(
        Criteria $criteria,
        SalesChannelContext $context,
        array $filterParams = []
    ): EntitySearchResult {
        $extension = new CustomProductFilterExtension(
            $criteria,
            $context,
            $filterParams
        );
        
        return $this->extensionDispatcher->publish(
            CustomProductFilterExtension::NAME,
            $extension,
            function() use ($criteria, $context) {
                // Default implementation
                return $this->productRepository->search($criteria, $context->getContext());
            }
        );
    }
}
```

### 3. Create an Event Subscriber

```php
<?php declare(strict_types=1);

namespace MyPlugin\Subscriber;

use MyPlugin\Extension\CustomProductFilterExtension;
use Symfony\Component\EventDispatcher\EventSubscriberInterface;

class CustomProductFilterSubscriber implements EventSubscriberInterface
{
    public function __construct(
        private readonly ExternalApiService $apiService,
        private readonly ProductFilterService $filterService
    ) {
    }
    
    public static function getSubscribedEvents(): array
    {
        return [
            'my-plugin.product-filter.pre' => 'onProductFilter',
        ];
    }
    
    public function onProductFilter(CustomProductFilterExtension $event): void
    {
        // Check if we should apply custom filtering
        if (!$this->shouldApplyCustomFilter($event->filterParams)) {
            return;
        }
        
        // Get filtered product IDs from external API
        $filteredIds = $this->apiService->getFilteredProductIds(
            $event->criteria,
            $event->context,
            $event->filterParams
        );
        
        if (empty($filteredIds)) {
            // No products match the filter
            $event->result = new EntitySearchResult(
                'product',
                0,
                new ProductCollection(),
                null,
                $event->criteria,
                $event->context->getContext()
            );
            $event->stopPropagation();
            return;
        }
        
        // Create new criteria with filtered IDs
        $newCriteria = clone $event->criteria;
        $newCriteria->setIds($filteredIds);
        
        // Apply additional filtering
        $filteredProducts = $this->filterService->applyBusinessRules(
            $newCriteria,
            $event->context
        );
        
        $event->result = $filteredProducts;
        $event->stopPropagation();
    }
    
    private function shouldApplyCustomFilter(array $filterParams): bool
    {
        return isset($filterParams['custom_filter']) && $filterParams['custom_filter'] === true;
    }
}
```

### 4. Register Services

```xml
<!-- services.xml -->
<service id="MyPlugin\Service\CustomProductService">
    <argument type="service" id="Shopware\Core\Framework\Extensions\ExtensionDispatcher"/>
    <argument type="service" id="product.repository"/>
</service>

<service id="MyPlugin\Subscriber\CustomProductFilterSubscriber">
    <argument type="service" id="MyPlugin\Service\ExternalApiService"/>
    <argument type="service" id="MyPlugin\Service\ProductFilterService"/>
    <tag name="kernel.event_subscriber"/>
</service>
```

## Advanced Extension Patterns

### 1. Conditional Extension Execution

```php
public function onExtension(MyExtension $event): void
{
    // Only execute under certain conditions
    if (!$this->shouldExecute($event)) {
        return;
    }
    
    $event->result = $this->customImplementation($event);
    $event->stopPropagation();
}

private function shouldExecute(MyExtension $event): bool
{
    return $event->context->getSalesChannelId() === 'special-sales-channel';
}
```

### 2. Extension with Error Handling

```php
public function onExtension(MyExtension $event): void
{
    try {
        $event->result = $this->riskyOperation($event);
        $event->stopPropagation();
    } catch (\Exception $e) {
        // Log the error but don't stop the extension
        $this->logger->error('Custom extension failed', [
            'error' => $e->getMessage(),
            'extension' => get_class($event)
        ]);
        
        // The extension system will handle the error
        // and potentially dispatch error events
    }
}
```

### 3. Extension with Data Enrichment

```php
public function onExtension(MyExtension $event): void
{
    // Don't replace the result, just enrich it
    if ($event->result !== null) {
        $enrichedResult = $this->enrichResult($event->result, $event);
        $event->result = $enrichedResult;
    }
}

private function enrichResult($result, MyExtension $event)
{
    // Add custom data to the result
    $result->addExtension('customData', new CustomStruct([
        'processedAt' => new \DateTime(),
        'context' => $event->context->getSalesChannelId()
    ]));
    
    return $result;
}
```

### 4. Multi-Phase Extension

```php
public static function getSubscribedEvents(): array
{
    return [
        'my-extension.pre' => 'onPrePhase',
        'my-extension.post' => 'onPostPhase',
        'my-extension.error' => 'onErrorPhase',
    ];
}

public function onPrePhase(MyExtension $event): void
{
    // Prepare data before default implementation
    $event->addExtension('preparedData', $this->prepareData($event));
}

public function onPostPhase(MyExtension $event): void
{
    // Process result after default implementation
    if ($event->result !== null) {
        $event->result = $this->postProcess($event->result, $event);
    }
}

public function onErrorPhase(MyExtension $event): void
{
    // Handle errors gracefully
    if ($event->exception !== null) {
        $event->result = $this->fallbackImplementation($event);
    }
}
```

## Extension Lifecycle Management

### Pre-Phase Extensions

Use `.pre` events to:

* Validate input data
* Modify criteria or parameters
* Replace default implementation entirely

### Post-Phase Extensions

Use `.post` events to:

* Enrich results
* Log completion
* Trigger follow-up actions

### Error-Phase Extensions

Use `.error` events to:

* Provide fallback implementations
* Log errors
* Recover from failures

## Best Practices

### 1. Naming Conventions

* Use descriptive, domain-specific names
* Follow the pattern: `{plugin}.{domain}.{action}`
* Use kebab-case for event names

### 2. Type Safety

* Always define generic types for extension points
* Use proper type hints for parameters
* Validate input data in constructors

### 3. Documentation

* Document all public properties with `@public` and `@description`
* Provide clear examples in docblocks
* Include usage examples in plugin documentation

### 4. Error Handling

* Use try-catch blocks for risky operations
* Provide meaningful error messages
* Consider fallback implementations

### 5. Performance

* Avoid expensive operations in Extensions
* Cache results when appropriate
* Use lazy loading for heavy dependencies

### 6. Testing

* Write unit tests for extension point classes
* Test event subscribers thoroughly
* Mock external dependencies

## Example: Complete Plugin with Custom Extension Point

Here's a complete example of a plugin that creates and uses a custom extension point:

```php
// 1. Extension class
final class ProductRecommendationExtension extends Extension
{
    public const NAME = 'my-plugin.product-recommendation';
    
    public function __construct(
        public readonly ProductEntity $product,
        public readonly SalesChannelContext $context,
        public readonly int $limit = 5
    ) {}
}

// 2. Service that uses the extension
class ProductRecommendationService
{
    public function getRecommendations(ProductEntity $product, SalesChannelContext $context): ProductCollection
    {
        $extension = new ProductRecommendationExtension($product, $context);
        
        return $this->extensionDispatcher->publish(
            ProductRecommendationExtension::NAME,
            $extension,
            function() use ($product, $context) {
                // Default recommendation logic
                return $this->getDefaultRecommendations($product, $context);
            }
        );
    }
}

// 3. Subscriber that provides custom logic
class ProductRecommendationSubscriber implements EventSubscriberInterfac

… **Truncated.** Full document: https://developer.shopware.com/docs/guides/plugins/plugins/framework/extension/creating-custom-extension.md


---

## Extension Points vs Events
**Source:** [guides/plugins/plugins/framework/extension/extension-vs-events.md](https://developer.shopware.com/docs/guides/plugins/plugins/framework/extension/extension-vs-events.md)  
# Extension Points vs Events

## Overview

Shopware 6 provides two different mechanisms for extending functionality: **Extension Points** and **Events**. While they may seem similar, they serve different purposes and have distinct characteristics. Understanding when to use each approach is crucial for effective plugin development.

## Key Differences

### Purpose and Design Philosophy

#### Extension Points

* **Purpose**: Replace or extend core functionality
* **Design**: Result-oriented, flow-controlling
* **Philosophy**: "I want to change how this works"

#### Events

* **Purpose**: Notify about actions that occurred
* **Design**: Notification-based, fire-and-forget
* **Philosophy**: "I want to know when this happens"

### Return Values and Flow Control

#### Extension Points

```php
public function onResolveListing(ResolveListingExtension $event): void
{
    // Can return a result that replaces the default behavior
    $event->result = $this->customProductLoader->load($event->criteria, $event->context);
    
    // Can stop the default implementation
    $event->stopPropagation();
}
```

#### Events

```php
public function onProductCreated(ProductCreatedEvent $event): void
{
    // Cannot return values or control flow
    // Can only perform side effects
    $this->logger->info('Product created: ' . $event->getProduct()->getName());
    $this->notificationService->sendNotification($event->getProduct());
}
```

### Execution Timing

#### Extension Points

* **Timing**: Before or during the action
* **Purpose**: Intercept and modify the process
* **Example**: Before product prices are calculated

#### Events

* **Timing**: After the action is completed
* **Purpose**: React to completed actions
* **Example**: After a product has been created

### Error Handling

#### Extension Points

```php
// Built-in error handling with recovery
try {
    $extension->result = $function(...$extension->getParams());
} catch (\Throwable $e) {
    $extension->exception = $e;
    $extension->resetPropagation();
    
    // Dispatch error event for recovery
    $this->dispatcher->dispatch($extension, self::error($name));
    
    // If no recovery, rethrow
    if ($extension->result === null) {
        throw $e;
    }
}
```

#### Events

```php
// Basic error handling
public function onProductCreated(ProductCreatedEvent $event): void
{
    try {
        $this->performSideEffect($event);
    } catch (\Exception $e) {
        // Error handling is up to the developer
        $this->logger->error('Failed to process product creation', ['error' => $e->getMessage()]);
    }
}
```

## When to Use Extension Points

Use Extension Points when you need to:

### 1. Replace Core Functionality

```php
// Replace default product loading with custom logic
public function onResolveListing(ResolveListingExtension $event): void
{
    $event->result = $this->externalProductService->loadProducts($event->criteria);
    $event->stopPropagation();
}
```

### 2. Modify Data Before Processing

```php
// Filter products before they're displayed
public function onProductListing(ProductListingExtension $event): void
{
    $filteredProducts = $this->filterProducts($event->products, $event->context);
    $event->result = $filteredProducts;
    $event->stopPropagation();
}
```

### 3. Integrate External Systems

```php
// Use external pricing service
public function onPriceCalculation(ProductPriceCalculationExtension $event): void
{
    $prices = $this->externalPricingService->calculatePrices($event->products);
    $event->result = $prices;
    $event->stopPropagation();
}
```

### 4. Add Conditional Business Logic

```php
// Apply special pricing for VIP customers
public function onPriceCalculation(ProductPriceCalculationExtension $event): void
{
    if ($this->isVipCustomer($event->context)) {
        $event->result = $this->applyVipPricing($event->products);
        $event->stopPropagation();
    }
}
```

## When to Use Events

Use Events when you need to:

### 1. Send Notifications

```php
public function onOrderPlaced(OrderPlacedEvent $event): void
{
    $this->emailService->sendOrderConfirmation($event->getOrder());
    $this->smsService->sendOrderNotification($event->getOrder());
}
```

### 2. Log Actions

```php
public function onProductCreated(ProductCreatedEvent $event): void
{
    $this->auditLogger->log('Product created', [
        'productId' => $event->getProduct()->getId(),
        'userId' => $event->getContext()->getUserId()
    ]);
}
```

### 3. Update External Systems

```php
public function onCustomerRegistered(CustomerRegisteredEvent $event): void
{
    $this->crmService->syncCustomer($event->getCustomer());
    $this->analyticsService->trackRegistration($event->getCustomer());
}
```

### 4. Trigger Follow-up Actions

```php
public function onOrderCompleted(OrderCompletedEvent $event): void
{
    $this->inventoryService->reserveStock($event->getOrder());
    $this->shippingService->schedulePickup($event->getOrder());
}
```

## Comparison Table

| Aspect                     | Extension Points              | Events               |
|----------------------------|-------------------------------|----------------------|
| **Purpose**                | Replace/Extend functionality  | Notify about actions |
| **Return Values**          | Yes (via `result` property)   | No                   |
| **Flow Control**           | Yes (via `stopPropagation()`) | No                   |
| **Error Handling**         | Advanced with recovery        | Basic                |
| **Timing**                 | Pre/during action             | Post-action          |
| **Use Case**               | Core functionality            | Side effects         |
| **Performance Impact**     | Can be significant            | Usually minimal      |
| **Complexity**             | Higher                        | Lower                |
| **Backward Compatibility** | Easier to maintain            | More complex         |

## Real-World Examples

### E-commerce Scenarios

#### Product Pricing (Extension Point)

```php
// Replace default pricing with dynamic pricing from external API
public function onPriceCalculation(ProductPriceCalculationExtension $event): void
{
    $dynamicPrices = $this->pricingApi->getPrices($event->products, $event->context);
    $event->result = $dynamicPrices;
    $event->stopPropagation();
}
```

#### Order Notification (Event)

```php
// Send notifications after an order is placed
public function onOrderPlaced(OrderPlacedEvent $event): void
{
    $this->emailService->sendOrderConfirmation($event->getOrder());
    $this->slackService->notifyTeam($event->getOrder());
}
```

#### Product Search (Extension Point)

```php
// Replace default search with AI-powered search
public function onProductSearch(ProductSearchExtension $event): void
{
    $aiResults = $this->aiSearchService->search($event->query, $event->context);
    $event->result = $aiResults;
    $event->stopPropagation();
}
```

#### Inventory Update (Event)

```php
// Update an external inventory system after a product update
public function onProductUpdated(ProductUpdatedEvent $event): void
{
    $this->inventoryService->syncProduct($event->getProduct());
}
```

## Migration from Events to Extension Points

If you're currently using Events for functionality replacement, consider migrating to Extension Points:

### Before (Event-based)

```php
// Old approach - using events for functionality replacement
public function onProductListingCriteria(ProductListingCriteriaEvent $event): void
{
    // Modify criteria
    $event->getCriteria()->addFilter(new EqualsFilter('active', true));
}

public function onProductLoaded(ProductLoadedEvent $event): void
{
    // Post-process products
    foreach ($event->getProducts() as $product) {
        $product->addExtension('customData', $this->getCustomData($product));
    }
}
```

### After (Extension Point-based)

```php
// New approach - using extension points for functionality replacement
public function onResolveListing(ResolveListingExtension $event): void
{
    // Replace entire listing resolution
    $event->result = $this->customListingService->resolve($event->criteria, $event->context);
    $event->stopPropagation();
}
```

## Best Practices

### For Extension Points

1. **Use sparingly**: Only when you need to replace core functionality
2. **Handle errors gracefully**: Provide fallback implementations
3. **Document thoroughly**: Extension points are part of the public API
4. **Test extensively**: Extension points can break core functionality
5. **Consider performance**: Extension points can impact performance significantly

### For Events

1. **Keep side effects minimal**: Don't perform heavy operations
2. **Handle errors gracefully**: Don't let event failures break the main flow
3. **Use async processing**: For heavy operations, use message queues
4. **Document side effects**: Make it clear what the event does
5. **Test in isolation**: Events should be testable independently

---

---

## Finding Extension Points
**Source:** [guides/plugins/plugins/framework/extension/finding-extensions.md](https://developer.shopware.com/docs/guides/plugins/plugins/framework/extension/finding-extensions.md)  
# Finding Extension Points

## Overview

Shopware 6 provides a modern extension system that allows you to intercept and modify core functionality. Unlike traditional events that are primarily for notifications, Extension Points are designed for **replacing and extending** core system processes.

This guide will cover how you can find available Extension Points in the Shopware codebase to use them in your plugin.

## Extension Classes

Extension Points in Shopware extend the base `Extension` class and are typically located in domain-specific directories. They follow a consistent naming pattern and structure.

### Finding Extension Classes

You can find Extension classes by searching for the following patterns in the Shopware source code:

#### Search Terms

* `extends Extension`: Find all Extension classes
* `Extension<`: Find typed Extension Points with specific return types
* `ExtensionDispatcher`: Find where Extension Points are dispatched

#### Common Locations

Extension Points are typically located in:

* `src/Core/Content/*/Extension/`
* `src/Core/Checkout/*/Extension/`
* `src/Core/Content/Cms/Extension/`
* `src/Core/Content/Product/Extension/`

### Example Extension Classes

Here are some common Extension Point you might encounter:

#### Product Extensions

```php
// Product price calculation
src/Core/Content/Product/Extension/ProductPriceCalculationExtension.php

// Product listing resolution
src/Core/Content/Product/Extension/ResolveListingExtension.php

// Product listing criteria modification
src/Core/Content/Product/Extension/ProductListingCriteriaExtension.php
```

#### Cart Extensions

```php
// Checkout place order
src/Core/Checkout/Cart/Extension/CheckoutPlaceOrderExtension.php

// Cart rule loading
src/Core/Checkout/Cart/Extension/CheckoutCartRuleLoaderExtension.php
```

#### CMS Extensions

```php
// CMS slots data enrichment
src/Core/Content/Cms/Extension/CmsSlotsDataEnrichExtension.php

// CMS slots data resolution
src/Core/Content/Cms/Extension/CmsSlotsDataResolveExtension.php
```

## Extension Naming Convention

Extension Points follow a consistent naming pattern:

### Event Names

Extension Points use a `NAME` constant that defines the event name:

```php
final class ResolveListingExtension extends Extension
{
    public const NAME = 'listing-loader.resolve';
    
    // ...
}
```

### Event Lifecycle

Extension Points are dispatched with lifecycle suffixes:

* `{name}.pre` - Before the default implementation
* `{name}.post` - After the default implementation
* `{name}.error` - When an error occurs

## Finding Extension Usage

### In Service Definitions

Services that use Extension Points typically inject the `ExtensionDispatcher`:

```xml
<service id="Some\Service">
    <argument type="service" id="Shopware\Core\Framework\Extensions\ExtensionDispatcher"/>
</service>
```

### In Constructor Parameters

Look for services that inject the `ExtensionDispatcher`:

```php
public function __construct(
    private readonly ExtensionDispatcher $extensionDispatcher
) {
}
```

### Extension Dispatch Pattern

Extension Points are typically dispatched using this pattern:

```php
$extension = new SomeExtension($parameters);
$result = $this->extensionDispatcher->publish(
    SomeExtension::NAME,
    $extension,
    function() use ($parameters) {
        // Default implementation
        return $this->defaultImplementation($parameters);
    }
);
```

## Common Extension Types

### Product Extensions

#### ProductPriceCalculationExtension

**Purpose**: Intercept and modify product price calculations
**Event Name**: `product.calculate-prices`
**Return Type**: `void`

```php
final class ProductPriceCalculationExtension extends Extension
{
    public const NAME = 'product.calculate-prices';
    
    public function __construct(
        public readonly iterable $products,
        public readonly SalesChannelContext $context
    ) {}
}
```

#### ResolveListingExtension

**Purpose**: Replace product listing resolution logic
**Event Name**: `listing-loader.resolve`
**Return Type**: `EntitySearchResult<ProductCollection>`

```php
final class ResolveListingExtension extends Extension
{
    public const NAME = 'listing-loader.resolve';
    
    public function __construct(
        public readonly Criteria $criteria,
        public readonly SalesChannelContext $context
    ) {}
}
```

### Cart Extensions

#### CheckoutPlaceOrderExtension

**Purpose**: Intercept order placement process
**Event Name**: `checkout.place-order`
**Return Type**: `OrderPlaceResult`

```php
final class CheckoutPlaceOrderExtension extends Extension
{
    public const NAME = 'checkout.place-order';
    
    public function __construct(
        public readonly Cart $cart,
        public readonly SalesChannelContext $context
    ) {}
}
```

### CMS Extensions

#### CmsSlotsDataEnrichExtension

**Purpose**: Enrich CMS slot data before rendering
**Event Name**: `cms.slots.data-enrich`
**Return Type**: `CmsSlotCollection`

```php
final class CmsSlotsDataEnrichExtension extends Extension
{
    public const NAME = 'cms.slots.data-enrich';
    
    public function __construct(
        public readonly CmsSlotCollection $slots,
        public readonly SalesChannelContext $context
    ) {}
}
```

## Using Extensions in Your Plugin

### Event Subscriber

Create an event subscriber to listen for Extension Points:

```php
<?php declare(strict_types=1);

namespace MyPlugin\Subscriber;

use Shopware\Core\Content\Product\Extension\ResolveListingExtension;
use Symfony\Component\EventDispatcher\EventSubscriberInterface;

class ProductListingSubscriber implements EventSubscriberInterface
{
    public static function getSubscribedEvents(): array
    {
        return [
            'listing-loader.resolve.pre' => 'onResolveListing',
        ];
    }
    
    public function onResolveListing(ResolveListingExtension $event): void
    {
        // Custom logic here
        $event->result = $this->customProductLoader->load($event->criteria, $event->context);
        $event->stopPropagation();
    }
}
```

### Service Registration

Register your subscriber in the service configuration:

```xml
<service id="MyPlugin\Subscriber\ProductListingSubscriber">
    <tag name="kernel.event_subscriber"/>
</service>
```

## Extension Lifecycle

Extension Points follow a specific lifecycle:

1. **Pre-Event**: `{name}.pre` - Before default implementation
2. **Default Implementation**: Core logic (if not stopped)
3. **Post-Event**: `{name}.post` - After implementation
4. **Error-Event**: `{name}.error` - If an error occurs

### Lifecycle Example

```php
public function handleExtension(SomeExtension $event): void
{
    // This runs in the .pre phase
    if ($this->shouldReplaceDefault($event)) {
        $event->result = $this->customImplementation($event);
        $event->stopPropagation(); // Prevents default implementation
    }
}

public function handlePostExtension(SomeExtension $event): void
{
    // This runs in the .post phase
    $this->logger->info('Extension completed', ['result' => $event->result]);
}
```

## Best Practices

### 1. Use Type Hints

Always use proper type hints for Extension Point parameters:

```php
public function onResolveListing(ResolveListingExtension $event): void
{
    // Type-safe access to properties
    $criteria = $event->criteria;
    $context = $event->context;
}
```

### 2. Handle Results Properly

Check if a result has already been set:

```php
public function onExtension(SomeExtension $event): void
{
    if ($event->result !== null) {
        // Another extension already provided a result
        return;
    }
    
    $event->result = $this->myImplementation($event);
}
```

### 3. Use Stop Propagation Wisely

Only stop propagation when you're providing a complete replacement:

```php
public function onExtension(SomeExtension $event): void
{
    if ($this->shouldReplaceDefault($event)) {
        $event->result = $this->completeReplacement($event);
        $event->stopPropagation();
    }
    // If not stopped, default behavior continues
}
```

### 4. Error Handling

Extension Points have built-in error handling, but you can also handle errors gracefully:

```php
public function onExtension(SomeExtension $event): void
{
    try {
        $event->result = $this->riskyOperation($event);
    } catch (\Exception $e) {
        // Log the error but don't stop the extension
        $this->logger->error('Extension failed', ['error' => $e->getMessage()]);
        // Let the extension system handle the error
    }
}
```

## Debugging Extensions

### Using the Symfony Profiler

The Symfony profiler shows all dispatched Extension Points in the "Events" tab. Look for events with `.pre`, `.post`, or `.error` suffixes.

### Logging Extension Calls

You can log Extension Point calls to understand the flow:

```php
public function onExtension(SomeExtension $event): void
{
    $this->logger->debug('Extension called', [
        'extension' => get_class($event),
        'hasResult' => $event->result !== null,
        'stopped' => $event->isPropagationStopped()
    ]);
}
```

This comprehensive guide should help you find and use Extension Points effectively in your Shopware plugins.

---

---

## Filesystem
**Source:** [guides/plugins/plugins/framework/filesystem.md](https://developer.shopware.com/docs/v6.6/guides/plugins/plugins/framework/filesystem.md)  
# Filesystem

Plugins often need the ability to read and write files. Thanks to the [Flysystem](https://flysystem.thephpleague.com/docs/) that Shopware uses, this can be managed very easily. It does not matter whether the files are stored on the local file system or at a cloud provider. The read and write access remains the same. If you want to learn more about the configuration of the file system in Shopware, have a look at the [filesystem guide](../../../../hosting/infrastructure/filesystem). For example, you will learn how to outsource the file system to the Amazon cloud. In a plugin, we don't have to worry about the configuration and can use the advantages of the Flysystem directly.

---

---

## Filesystem - Flysystem
**Source:** [guides/plugins/plugins/framework/filesystem/filesystem.md](https://developer.shopware.com/docs/v6.6/guides/plugins/plugins/framework/filesystem/filesystem.md)  
# Filesystem - Flysystem

## Overview

Flysystem is a file storage library for PHP. It provides one interface to interact with many types of filesystems. The Flysystem file system in Shopware is flexible, allowing seamless interaction with various file storage systems. It provides a consistent interface to access, manipulate, and manage files across different storage backends.

## Prerequisites

This guide is built upon both the [Plugin base guide](../../plugin-base-guide) and the [Add custom service guide](../../plugin-fundamentals/add-custom-service).

## Flysystem overview

The Flysystem enables your plugin to read and write files through a common interface. There are several default namespaces/directories that are available, for example:

* One for private files of the shop: invoices, delivery notes
* One for public files: product pictures, media files
* One for theme files
* One for sitemap files
* One for bundle assets files

However, every plugin/bundle gets an own namespace that should be used for private or public plugin files. These are automatically generated during the plugin installation. The namespace is prefixed with the [Snake case](https://en.wikipedia.org/wiki/Snake_case) plugin name followed by `filesystem` `.` `private` or `public`. For our example plugin, this would be

* `swag_basic_example.filesystem.public` for public plugin files
* `swag_basic_example.filesystem.private` for private plugin files

## Use filesystem in a service

To make use of the filesystem, we register a new service, which helps to read and write files to the filesystem.

```php
// <plugin root>/src/Service/ExampleFilesystemService.php
<?php declare(strict_types=1);

namespace Swag\BasicExample\Service;

use League\Flysystem\FilesystemOperator;

class ExampleFilesystemService
{
    /**
     * @var FilesystemOperator
     */
    private FilesystemOperator $fileSystemPublic;
    /**
     * @var FilesystemOperator
     */
    private FilesystemOperator $fileSystemPrivate;

    /**
     * ExampleFilesystemService constructor.
     * @param FilesystemOperator $fileSystemPublic
     * @param FilesystemOperator $fileSystemPrivate
     */
    public function __construct(FilesystemOperator $fileSystemPublic, FilesystemOperator $fileSystemPrivate)
    {
        $this->fileSystemPublic = $fileSystemPublic;
        $this->fileSystemPrivate = $fileSystemPrivate;
    }

    public function readPrivateFile(string $filename) {
        return $this->fileSystemPrivate->read($filename);
    }

    public function writePrivateFile(string $filename, string $content) {
        $this->fileSystemPrivate->write($filename, $content);
    }

    public function listPublicFiles(): array {
        return $this->fileSystemPublic->listContents();
    }
}
```

This service makes use of the private und public filesystem. As you already know, this php class has to be registered as a service in the dependency injection container. This is also the place where we define which filesystem will be handed over to the constructor. To make use of the plugin private and public files, the service definition could look like this:

```xml
// <plugin root>/src/Resources/config/services.xml
<?xml version="1.0" ?>
<container xmlns="http://symfony.com/schema/dic/services"
           xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
           xsi:schemaLocation="http://symfony.com/schema/dic/services http://symfony.com/schema/dic/services/services-1.0.xsd">

    <services>
        <service id="Swag\BasicExample\Service\ExampleFilesystemService">
            <argument type="service" id="swag_basic_example.filesystem.public"/>
            <argument type="service" id="swag_basic_example.filesystem.private"/>
            <!--
            There are also predefined file system services
            <argument type="service" id="shopware.filesystem.private"/>
            <argument type="service" id="shopware.filesystem.public"/>
            -->
        </service>
    </services>
</container>
```

Now, this service can be used to read or write files to the private plugin filesystem or to list all files in the public plugin filesystem. You should visit the [Flysystem API documentation](https://flysystem.thephpleague.com/docs/usage/filesystem-api/) for more information.

---

---

## Message Queue
**Source:** [guides/plugins/plugins/framework/message-queue.md](https://developer.shopware.com/docs/v6.6/guides/plugins/plugins/framework/message-queue.md)  
# Message Queue

The Shopware message queue manages the asynchronous processing of tasks using a message handler, message queue, and middleware, ensuring reliable and efficient execution of background processes within the e-commerce platform. Possible tasks are sending emails, indexing products, or generating the sitemap.

---

---

## Add message handler
**Source:** [guides/plugins/plugins/framework/message-queue/add-message-handler.md](https://developer.shopware.com/docs/v6.6/guides/plugins/plugins/framework/message-queue/add-message-handler.md)  
# Add message handler

## Overview

::: warning
Parts of this guide refer to the `low_priority` queue, which is only available in version 6.5.7.0 and above. Configuring the messenger to consume this queue will fail if it does not exist.
:::

In this guide you'll learn how to create a message handler.

A [handler](https://symfony.com/doc/current/messenger.html#creating-a-message-handler) gets called once the message is dispatched by the `handle_messages` middleware. Handlers do the actual processing of the message.

## Prerequisites

As most guides, this guide is also built upon the [Plugin base guide](../../plugin-base-guide), but you don't necessarily need that. It will use an example message, so if you don't know how to add a custom message yet, have a look at our guide about [Adding a message to queue](add-message-to-queue). Furthermore, registering classes or services to the DI container is also not explained here, but it's covered in our guide about [Dependency injection](../../plugin-fundamentals/dependency-injection), so having this open in another tab won't hurt.

## Handling messages

First, we have to create a new class which we will name `SmsHandler` in this example. To mark the class as message handler, we use the php attribute `#[AsMessageHandler]` and implement the method `__invoke`. We can also define multiple handlers for the same message. To register a handler, we have to tag it with the `messenger.message_handler` tag.

```php
// <plugin root>/src/MessageQueue/Handler/SmsHandler.php
<?php declare(strict_types=1);

namespace Swag\BasicExample\MessageQueue\Handler;

use Symfony\Component\Messenger\Attribute\AsMessageHandler;
use Swag\BasicExample\MessageQueue\Message\SmsNotification;

#[AsMessageHandler]
class SmsHandler
{
    public function __invoke(SmsNotification $message)
    {
        // ... do some work - like sending an SMS message!
    }
}
```

## Next steps

Now that you know how to add a message handler, you may want to add a custom middleware for your bus. To do this, head over to [Add middleware](add-middleware) guide.

If you want to learn more about configuring the message queue, have a look at the [Message queue hosting guide](../../../../hosting/infrastructure/message-queue.md).

---

---

## Add message to queue
**Source:** [guides/plugins/plugins/framework/message-queue/add-message-to-queue.md](https://developer.shopware.com/docs/v6.6/guides/plugins/plugins/framework/message-queue/add-message-to-queue.md)  
# Add message to queue

## Overview

::: warning
Parts of this guide refer to the `low_priority` queue and the corresponding `LowPriorityMessageInterface`, which is only available in version 6.5.7.0 and above. Configuring the messenger to consume this queue will fail if it does not exist.
:::

In this guide you'll learn how to create a message and add it to the queue.

Shopware integrates with the [Symfony Messenger](https://symfony.com/doc/current/components/messenger.html) component and [Enqueue](https://enqueue.forma-pro.com/). This gives you the possibility to send and handle asynchronous messages.

A [message](https://symfony.com/doc/current/messenger.html#creating-a-message-handler) is a simple PHP object that you want to dispatch over the MessageQueue. It must be serializable and should contain all necessary information that your handlers need to process the message.

It will be wrapped in an [envelope](https://symfony.com/doc/current/components/messenger.html#adding-metadata-to-messages-envelopes) by the message bus that dispatches the message.

## Prerequisites

As most guides, this guide is also built upon the [Plugin base guide](../../plugin-base-guide), but you don't necessarily need that. It will use an example service, so if you don't know how to add a custom service yet, have a look at our guide about [Adding a custom service](../../plugin-fundamentals/add-custom-service). Furthermore, registering classes or services to the DI container is also not explained here, but it's covered in our guide about [Dependency injection](../../plugin-fundamentals/dependency-injection), so having this open in another tab won't hurt.

## Create a message

First, we have to create a new message class in the directory `<plugin root>/MessageQueue/Message`. In this example, we create a `SmsNotification` that contains a string with content. By default, all messages are handled synchronously. To change the behavior to asynchronously, we have to implement the `AsyncMessageInterface` interface. For messages which should also be handled asynchronously but with a lower priority, implement the `LowPriorityMessageInterface` interface.

Here's an example:

```php
// <plugin root>/src/MessageQueue/Message/SmsNotification.php
<?php declare(strict_types=1);

namespace Swag\BasicExample\MessageQueue\Message;

use Shopware\Core\Framework\MessageQueue\AsyncMessageInterface;

class SmsNotification implements AsyncMessageInterface
{
    private string $content;

    public function __construct(string $content)
    {
        $this->content = $content;
    }

    public function getContent(): string
    {
        return $this->content;
    }
}
```

## Send a message

After we've created our notification, we will create a service that will send our `SmsNotification`. We will name this service `ExampleSender`. In this service we need to inject the `Symfony\Component\Messenger\MessageBusInterface`, that is needed to send the message through the desired bus, which is called `messenger.default_bus`.

```php
// <plugin root>/src/Service/ExampleSender.php
<?php declare(strict_types=1);

namespace Swag\BasicExample\Service;

use Swag\BasicExample\MessageQueue\Message\SmsNotification;
use Symfony\Component\Messenger\MessageBusInterface;

class ExampleSender
{
    private MessageBusInterface $bus;

    public function __construct(MessageBusInterface $bus)
    {
        $this->bus = $bus;
    }

    public function sendMessage(string $message): void
    {
        $this->bus->dispatch(new SmsNotification($message));
    }
}
```

If we want to add metadata to our message, we can dispatch an `Symfony\Component\Messenger\Envelope` in our service instead with the necessary [stamps](https://symfony.com/doc/current/components/messenger.html#adding-metadata-to-messages-envelopes). In this example below, we use the `Symfony\Component\Messenger\Stamp\DelayStamp`, which tells the queue to process the message later.

```php
// <plugin root>/src/Service/ExampleSender.php
public function sendMessage(string $message): void
{
    $message = new SmsNotification($message);
    $this->bus->dispatch(
        (new Envelope($message))
            ->with(new DelayStamp(5000))
    );
}
```

## Lower the priority for specific async messages

You might consider using the new `low_priority` queue if you are dispatching messages that do not need to be handled immediately. To configure specific messages to be transported via the `low_priority` queue, you need to either adjust the routing or implement the `LowPriorityMessageInterface` as already mentioned:

```yaml
# config/packages/shopware.yaml
shopware:
    messenger:
        routing_overwrite:
            'Your\Custom\Message': low_priority
```

## Override transport for specific messages

If you explicitly configure a message to be transported via the `async` (default) queue, even though it implements the `LowPriorityMessageInterface`, which would usually be transported via the `low_priority` queue, the transport is overridden for this specific message.

Example:

```php
// <plugin root>/src/MessageQueue/Message/LowPriorityMessage.php
<?php declare(strict_types=1);

namespace Your\Custom;

use Shopware\Core\Framework\MessageQueue\LowPriorityMessageInterface;

class LowPriorityMessage implements LowPriorityMessageInterface
{
}
```

```yaml
# config/packages/shopware.yaml
shopware:
    messenger:
        routing_overwrite:
            'Shopware\Core\Framework\MessageQueue\LowPriorityMessageInterface': low_priority
            'Your\Custom\LowPriorityMessage': async
```

## Next steps

Now that you know how to create a message and add it to the queue, let's create a handler to process our message. To do this, head over to [Add message handler](add-message-handler) guide.

---

---

## Add Middleware
**Source:** [guides/plugins/plugins/framework/message-queue/add-middleware.md](https://developer.shopware.com/docs/v6.6/guides/plugins/plugins/framework/message-queue/add-middleware.md)  
# Add Middleware

## Overview

In this guide you will learn how to add a custom middleware.

A [Middleware](https://symfony.com/doc/current/messenger.html#middleware) is called when the message bus dispatches messages. The middleware defines what happens when you dispatch a message. For example the `send_message` middleware is responsible for sending your message to the configured transport and the `handle_message` middleware will actually call your handlers for the given message.

## Prerequisites

As most guides, this guide is also built upon the [Plugin base guide](../../plugin-base-guide), but you don't necessarily need that. Furthermore, registering classes or services to the DI container is also not explained here, but it's covered in our guide about [Dependency injection](../../plugin-fundamentals/dependency-injection), so having this open in another tab won't hurt.

## Create middleware

First we need to create a new service that implements the `MiddlewareInterface`. This interface comes with a method `handle`, which should always call the next middleware.

```php
// <plugin root>/src/MessageQueue/Middleware/ExampleMiddleware.php
<?php declare(strict_types=1);

namespace Swag\BasicExample\MessageQueue\Middleware;

use Symfony\Component\Messenger\Envelope;
use Symfony\Component\Messenger\Middleware\MiddlewareInterface;
use Symfony\Component\Messenger\Middleware\StackInterface;

class ExampleMiddleware implements MiddlewareInterface
{
    public function handle(Envelope $envelope, StackInterface $stack): Envelope
    {
        // do something here

        // don't forget to call the next middleware
        return $stack->next()->handle($envelope, $stack);
    }
}
```

## Configure middleware

After we've created our middleware, we have to add that middleware to the message bus through configuration.

For each defined bus in our `framework.yaml`, we can define the middleware that this bus should use. To add middleware, we simply specify our custom middleware as follows:

```yaml
// <platform root>/src/Core/Framework/Resources/config/packages/framework.yaml
framework:
    messenger:
        buses:
          messenger.bus.default:
            middleware:
              - 'Swag\BasicExample\MessageQueue\Middleware\ExampleMiddleware'
              - 'Swag\BasicExample\MessageQueue\Middleware\AnotherExampleMiddleware'
```

## More interesting topics

* [Message Queue](add-message-to-queue)
* [Message Handler](add-message-handler)

---

---

## Rate Limiter
**Source:** [guides/plugins/plugins/framework/rate-limiter.md](https://developer.shopware.com/docs/v6.6/guides/plugins/plugins/framework/rate-limiter.md)  
# Rate Limiter

A rate limiter controls the rate or frequency at which API requests can be made. It sets limits on the number of requests that can be processed within a specified time period, preventing excessive usage. Hence eliminating the chance of brute-force attacks. Rate limiters help maintain system stability, protect against misuse, and ensure fair resource allocation by enforcing predefined limits on the rate of incoming requests.

---

---

## Add Rate Limiter to API Route
**Source:** [guides/plugins/plugins/framework/rate-limiter/add-rate-limiter-to-api-route.md](https://developer.shopware.com/docs/v6.6/guides/plugins/plugins/framework/rate-limiter/add-rate-limiter-to-api-route.md)  
# Add Rate Limiter to API Route

## Overview

In this guide you'll learn how to secure API routes with a rate limit to reduce the risk against bruteforce attacks.
If you want to learn more about the configuration of the rate limiter in Shopware,
have a look at the [Rate limiter](../../../../hosting/infrastructure/rate-limiter) guide.

## Prerequisites

This guide is built upon both the [Plugin base guide](../../plugin-base-guide) as well as the [Dependency injection](../../plugin-fundamentals/dependency-injection) guide.

Furthermore you need an existing API route, to create a new one, head over to our [Add store API route](../store-api/add-store-api-route) guide.

## Creating a new rate limit

### Basic configuration for plugins

First of all, we have to create a new configuration file for our rate limit. In this example we named it `rate_limiter.yaml` located in `<plugin root>/src/Resources/config/`.
The root key of the configuration is the name which has to be a unique key. In this example we named it `example_route`.

Each rate limit configuration needs the following keys:

* `enabled`: Enables / Disables the rate limit for the specific route (default value: true).
* `policy`: Possible policies are `fixed_window`, `sliding_window`, `token_bucket`, `time_backoff`. For more information check the [Symfony documentation](https://symfony.com/doc/current/rate_limiter.html#rate-limiting-policies).

If you plan to configure the `time_backoff` policy, head over to [rate limiter](../../../../hosting/infrastructure/rate-limiter#configuring-time-backoff-policy) guide.
Otherwise, check the [Symfony documentation](https://symfony.com/doc/current/rate_limiter.html#configuration) for the other keys you need for each policy.

```yaml
// <plugin root>/src/Resources/config/rate_limiter.yaml
example_route:
    enabled: true
    policy: 'time_backoff'
```

### Extending rate limit configuration in the DI-container

In this section we will create a small compiler pass called `RateLimiterCompilerPass`. If you are not very familiar with compiler passes,
head over to the [Symfony documentation](https://symfony.com/doc/current/service_container/compiler_passes.html).

### Creating compiler pass

```php
// <plugin root>/src/CompilerPass/RateLimiterCompilerPass.php
<?php declare(strict_types=1);

namespace Swag\BasicExample\CompilerPass;

use Symfony\Component\DependencyInjection\Compiler\CompilerPassInterface;
use Symfony\Component\DependencyInjection\ContainerBuilder;
use Symfony\Component\Yaml\Yaml;

class RateLimiterCompilerPass implements CompilerPassInterface
{
    public function process(ContainerBuilder $container): void
    {
        /** @var array<string, array<string, string>> $rateLimiterConfig */
        $rateLimiterConfig = $container->getParameter('shopware.api.rate_limiter');

        $rateLimiterConfig += Yaml::parseFile(__DIR__ . '/../Resources/config/rate_limiter.yaml');

        $container->setParameter('shopware.api.rate_limiter', $rateLimiterConfig);
    }
}
```

As you can see, we're getting the current configuration of the rate limit from the DI-container and extend it by our `rate_limiter.yaml`
and reassign it with the merged configuration.

### Adding compiler pass to the container

Now, we have to add our compiler pass to the container. This will be done by overriding the `build()` method of
our `SwagBasicExample` plugin class. Important here is to use `Symfony\Component\DependencyInjection\Compiler\PassConfig::TYPE_BEFORE_OPTIMIZATION`
with a higher priority, otherwise it will be built too late.

```php
// <plugin root>/src/SwagBasicExample.php
<?php declare(strict_types=1);

namespace Swag\BasicExample;

use Swag\BasicExample\CompilerPass\RateLimiterCompilerPass;
use Shopware\Core\Framework\Plugin;
use Shopware\Core\Framework\Plugin\Context\InstallContext;
use Symfony\Component\DependencyInjection\Compiler\PassConfig;
use Symfony\Component\DependencyInjection\ContainerBuilder;

class SwagBasicExample extends Plugin
{
    public function build(ContainerBuilder $container): void
    {
        parent::build($container);

        $container->addCompilerPass(new RateLimiterCompilerPass(), PassConfig::TYPE_BEFORE_OPTIMIZATION, 500);
    }
}
```

## Implementing rate limit in API route

### Inject service

After we've configured our rate limit, we want to use it in our API route.
For this we need to inject the `Shopware\Core\Framework\RateLimiter\RateLimiter` service.

```php
// <plugin root>/src/Core/Content/Example/SalesChannel/ExampleRoute.php
<?php declare(strict_types=1);

namespace Swag\BasicExample\Core\Content\Example\SalesChannel;

use Shopware\Core\Framework\RateLimiter\RateLimiter;
...

#[Route(defaults: ['_routeScope' => ['store-api']])]
class ExampleRoute extends AbstractExampleRoute
{
    private RateLimiter $rateLimiter;

    public function __construct(RateLimiter $rateLimiter)
    {
        $this->rateLimiter = $rateLimiter;
    }

    ...
}
```

### Call the rate limiter

After we've injected the service into our API route, we can call the limiter in our route method.

To do this, we call the method `ensureAccepted` of the rate limiter which accepts the following arguments:

* `route`: Unique name of the rate limit, we defined in the configuration.
* `key`: Key we want to use to limit the request e.g., the client IP.

When calling the `ensureAccepted` method it counts the request for the key in the defined cache.
If the limit has been exceeded, it throws `Shopware\Core\Framework\RateLimiter\Exception\RateLimitExceededException`.

```php
// <plugin root>/src/Core/Content/Example/SalesChannel/ExampleRoute.php

#[Route(path: '/store-api/example', name: 'store-api.example.search', methods: ['GET','POST'])]
public function load(Request $request, SalesChannelContext $context): ExampleRouteResponse
{
    // Limit ip address
    $this->rateLimiter->ensureAccepted('example_route', $request->getClientIp());
    
    ...
}
```

### Reset the rate limit

Once we've made a successful request, we want to reset the rate limit for the client.
We just have to call the `reset` method as you can see below.

```php
// <plugin root>/src/Core/Content/Example/SalesChannel/ExampleRoute.php

#[Route(path: '/store-api/example', name: 'store-api.example.search', methods: ['GET','POST'])]
public function load(Request $request, SalesChannelContext $context): ExampleRouteResponse
{
    // Limit ip address for example
    $this->rateLimiter->ensureAccepted('example_route', $request->getClientIp());
    
    // if action was successfully, reset limit 
    if ($this->doAction() === true) {
        $this->rateLimiter->reset('example_route', $request->getClientIp());
    }
    
    ...
}
```

---

---

## Overview
**Source:** [guides/plugins/plugins/framework/system-check.md](https://developer.shopware.com/docs/v6.6/guides/plugins/plugins/framework/system-check.md)  
# Overview

In this guide, you will learn about the system health check in Shopware. System health checks are a way to monitor the health of a system and detect failures early.

You can find the core concepts well-defined in the Concepts section of the documentation [System Checks](../../../../../concepts/framework/system-check.md)

## Triggering System Checks

The system checks can be invoked either through the CLI or via an HTTP API.

* By calling the endpoint `/api/_info/system-health-check`
  * the HTTP response code only indicates the status of the request, not the status of the checks
* By calling the CLI command `system:check`
  * The command returns status `0` if all checks are healthy, `1` if any check is marked as unhealthy, and `2` if the call is invalid. See [Understanding the Check Results](#understanding-the-check-results)

> The CLI command defaults to using the `cli` execution context. You can change the execution context by passing the `--context` option. The available options are `cli`, `pre-rollout`, and `recurrent`.
> When calling the HTTP endpoint, the execution context is always `web`

### Shopware default flow

The default flow of Shopware system checks is done via: `Shopware\Core\Framework\SystemCheck\SystemChecker`

The `SystemChecker` class makes sure the system is working correctly by running all the registered system checks in a series. The following behavior is observed:

* Order of Checks: It runs checks in a specific order, grouped by types.
* Skipping Checks: Some checks are skipped if they aren’t allowed to run or if a major problem is found early on.
* Stopping Early: If a check in the `SYSTEM` type group is marked as `healthy = false`, it stops running more checks.

### Custom flow

All the system checks in Shopware are tagged with `shopware.system_check`, so you can also fetch all the checks using the Symfony service locator. and run them in your custom flow.

```php
class CustomSystemChecker
{
   public function __construct(private readonly iterable $checks)
    {
    }

    public function check(): array
    {
       # ... add your custom logic here
    }
}
```

```xml
<service id="YourNamepace\CustomSystemChecker">
    <argument type="tagged_iterator" tag="shopware.system_check"/>
</service>
```

### Custom triggers

For customized triggers, you can also inject the `Shopware\Core\Framework\SystemCheck\SystemChecker` service into your service and trigger the checks programmatically.

```php
$results = $systemChecker->check(SystemCheckExecutionContext::WEB);
# or also use any custom logic you might have...
$customChecker->check();
```

## Understanding the Check Results

The `Shopware\Core\Framework\SystemCheck\Check\Result` class represents the outcome of a system check in Shopware. Helping further diagnosis.

All the properties in the Result class, are objective in nature, so there usually is one clear interpretation. except the `healthy` flag, which is subjective.

In principle, regardless of the actual status of the check, the `healthy` flag should be set to:

* `true` if the system can still function normally
* `false` if the system cannot function normally
* `null` if it cannot be determined

---

---

## Overview
**Source:** [guides/plugins/plugins/framework/system-check/add-custom-check.md](https://developer.shopware.com/docs/v6.6/guides/plugins/plugins/framework/system-check/add-custom-check.md)  
# Overview

In this guide, we will be building a dummy example of a custom system check that verifies if the local system has enough disk space to operate normally.

## Add a new Custom Check

First, you need to add a new `LocalDiskSpaceCheck` class that extends the `Shopware\Core\Framework\SystemCheck\BaseCheck` and implement the essential categorization methods.

### Fill the categorization methods

Each check contains a set of categorization methods that help to classify the check, and determine when and where it should be executed.

```php
class LocalDiskSpaceCheck extends BaseCheck
{
    public function category(): Category
    {
        // crucial for the system to function at all. 
        return Category::SYSTEM;
    }

    public function name(): string
    {
        return 'LocalDiskSpaceCheck';
    }

    protected function allowedSystemCheckExecutionContexts(): array
    {   // a potentially long-running check, because it has an IO operation.
        return SystemCheckExecutionContext::longRunning();
    }
}
```

### Create the check logic

The next step is to implement the actual check logic. We will check if the disk space is below a certain threshold and return the appropriate result.

```php
class LocalDiskSpaceCheck extends BaseCheck
{
    public function __construct(
        private readonly string $adapterType,
        private readonly string $installationPath,
        private readonly int $warningThresholdInMb
    )
    {
    }

    public function run(): Result
    {
        if ($this->adapterType !== 'local') {
           return new Result(name: $this->name(), status: Status::SKIPPED, message: 'Disk space check is only available for local file systems.', healthy: true)
        }
        
        $availableSpaceInMb = $this->getFreeDiskSpaceInMegaBytes();
        if ($availableSpaceInMb < $this->warningThresholdInMb) {
            return new Result(name: $this->name(), status: Status::WARNING, message: sprintf('Available disk space is below the warning threshold of %s.', $this->warningThresholdInMb), healthy: true);
        }

        return new Result(name: $this->name(), status: Status::OK, message: 'Disk space is sufficient.', healthy: true);
    }

     private function getFreeDiskSpaceInMegaBytes()
     {
        $freeSpace = disk_free_space($this->installationPath);
        $totalSpace = disk_total_space($this->installationPath);
        $availableSpace = $totalSpace - $freeSpace;

        return $availableSpace / 1024 / 1024;
     }
    ...
    ...
}
```

> An important consideration is the healthy flag, which is subjective and can vary depending on the specific shop's criteria. For example, if the disk space threshold is set high, the system can still function normally, so the healthy flag could be true. Conversely, if the threshold is too low for normal operation, the healthy flag could be false.

### Register the custom check

Finally, you need to register the custom check as a service resource.

```xml
        <service id="%YourNameSpace%\LocalDiskSpaceCheck" >
            <argument>%shopware.filesystem.public.type%</argument>
            <argument>%shopware.filesystem.public.config.root%</argument>
            <argument>%warning_threshold_in_mb%</argument>
            <tag name="shopware.system_check"/>
        </service>
```

### Trigger the check

The system check is now part of the system check collection and will be executed when the system check is triggered. Refer to the [System Check](../system-check.md) guide for more information.

---

---

## In-App Purchases
**Source:** [guides/plugins/plugins/in-app-purchase.md](https://developer.shopware.com/docs/v6.6/guides/plugins/plugins/in-app-purchase.md)  
# In-App Purchases

::: info
In-App Purchase is available since Shopware version 6.6.9.0
:::

In-App Purchases are a way to lock certain features behind a paywall within the same extension.
This is useful for developers who want to offer a free version of their extension with limited features,
and then offer a paid version with more features.

## Active In-App Purchases

The `InAppPurchase` class contains a list of all In-App Purchases.
Inject this service into your class and you can check against it:

```php
class Example
{
    public function __construct(
        private readonly InAppPurchase $inAppPurchase,
    ) {}

    public function someFunction() {
        if ($this->inAppPurchase->isActive('MyExtensionName', 'my-iap-identifier')) {
            // ...
        }

        // ...
    }
}
```

If you want to check an in-app purchase in the administration:

```js
if (Shopware.InAppPurchase.isActive('MyExtensionName', 'my-iap-identifier')) {};
```

## Allow users to buy an In-App Purchase

```js
{
    computed: {
        inAppPurchaseCheckout() {
            return Shopware.Store.get('inAppPurchaseCheckout');
        }
    },

    methods: {
        onClick() {
            this.inAppPurchaseCheckout.request({ identifier: 'my-iap-identifier' }, 'MyExtensionName');
        }
    }
}
```

## Event

Apps are also able to manipulate the available In-App Purchases as described in .

Plugins can listen to the `Shopware\Core\Framework\App\InAppPurchases\Event\InAppPurchasesGatewayEvent`.
This event is dispatched after the In-App Purchases Gateway has received the app server response from a gateway
and allows plugins to manipulate the available In-App Purchases.

---

---

## In-App Purchases
**Source:** [guides/plugins/plugins/in-app-purchases.md](https://developer.shopware.com/docs/guides/plugins/plugins/in-app-purchases.md)  
# In-App Purchases

::: info
In-App Purchase is available since Shopware version 6.6.9.0
:::

In-App Purchases are a way to lock certain features behind a paywall within the same extension.
This is useful for developers who want to offer a free version of their extension with limited features,
and then offer a paid version with more features.

## Allow users to buy an In-App Purchase

In order to enable others to purchase your In-App Purchase, you must request a checkout for it via the `inAppPurchaseCheckout` store in the administration.
The checkout process itself is provided by Shopware.
As this is purely functional, it is your responsibility to provide a button and hide it if the IAP cannot be purchased more than once.

```ts
{
    computed: {
        inAppPurchaseCheckout() {
            return Shopware.Store.get('inAppPurchaseCheckout');
        },

        hideButton(): boolean {
            return Shopware.InAppPurchase.isActive('MyExtensionName', 'my-iap-identifier');
        }
    },

    methods: {
        onClick() {
            this.inAppPurchaseCheckout.request({ identifier: 'my-iap-identifier' }, 'MyExtensionName');
        }
    }
}
```

## Check active In-App Purchases

The `InAppPurchase` class contains a list of all In-App Purchases.
Inject this service into your class and you can check against it:

```php
class Example
{
    public function __construct(
        private readonly InAppPurchase $inAppPurchase,
    ) {}

    public function someFunction() {
        if ($this->inAppPurchase->isActive('MyExtensionName', 'my-iap-identifier')) {
            // ...
        }

        // ...
    }
}
```

If you want to check an in-app purchase in the administration:

```js
if (Shopware.InAppPurchase.isActive('MyExtensionName', 'my-iap-identifier')) {};
```

## Event

Apps are also able to manipulate the available In-App Purchases as described in


Plugins can listen to the `Shopware\Core\Framework\App\InAppPurchases\Event\InAppPurchasesGatewayEvent`.
This event is dispatched after the In-App Purchases Gateway has received the app server response from a gateway
and allows plugins to manipulate the available In-App Purchases.

---

---

