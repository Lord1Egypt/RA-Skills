# Shopware 6.7 examples: plugin bootstrap, DAL, events, migrations

Hand-curated **full listings** derived from an internal Shopware 6.7 project guide (German source). **Verify** against [developer.shopware.com](https://developer.shopware.com/) and your installed Shopware version.

Vendor/plugin names are neutralized (`Acme\ExamplePlugin`, `AcmeExamplePlugin`, `acme_example`). For deeper official coverage see `PLUGIN_SYSTEM.md`, `DAL_AND_DATA.md`.

**Architecture and API rules:** see [CODE_GUIDELINES_ESSENTIALS.md](CODE_GUIDELINES_ESSENTIALS.md) (public API, `@internal`, backward compatibility, events, DI, migrations pointers).

---

## 3. Plugin development

### 3.1 composer.json template

```json
{
    "name": "acme/example-plugin",
    "description": "Example plugin for Shopware 6.7",
    "version": "1.0.0",
    "type": "shopware-platform-plugin",
    "license": "MIT",
    "authors": [
        {
            "name": "Example Vendor",
            "homepage": "https://example.com/"
        }
    ],
    "require": {
        "shopware/core": "~6.7.0",
        "shopware/storefront": "~6.7.0",
        "shopware/administration": "~6.7.0"
    },
    "extra": {
        "shopware-plugin-class": "Acme\\ExamplePlugin\\AcmeExamplePlugin",
        "plugin-icon": "src/Resources/config/acme-shopware-plugin-icon.png",
        "label": {
            "de-DE": "Acme Example Plugin",
            "en-GB": "Acme Example Plugin"
        },
        "description": {
            "de-DE": "Beschreibung auf Deutsch",
            "en-GB": "Description in English"
        }
    },
    "autoload": {
        "psr-4": {
            "Acme\\ExamplePlugin\\": "src/"
        }
    }
}
```

### 3.2 Plugin base class

```php
<?php declare(strict_types=1);

namespace Acme\ExamplePlugin;

use Shopware\Core\Framework\Plugin;
use Shopware\Core\Framework\Plugin\Context\InstallContext;
use Shopware\Core\Framework\Plugin\Context\UninstallContext;

class AcmeExamplePlugin extends Plugin
{
    public function install(InstallContext $installContext): void
    {
        parent::install($installContext);
        // Install-Logik
    }

    public function uninstall(UninstallContext $uninstallContext): void
    {
        parent::uninstall($uninstallContext);
        
        if ($uninstallContext->keepUserData()) {
            return;
        }
        // Cleanup-Logik
    }
    
    public function getMigrationNamespace(): string
    {
        return 'Acme\ExamplePlugin\Migration';
    }
}
```

### 3.3 services.xml (DI)

```xml
<?xml version="1.0" ?>
<container xmlns="http://symfony.com/schema/dic/services"
           xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
           xsi:schemaLocation="http://symfony.com/schema/dic/services http://symfony.com/schema/dic/services/services-1.0.xsd">
    <services>
        <!-- Autowiring & Autoconfigure -->
        <defaults autowire="true" autoconfigure="true"/>

        <!-- Prototype-Registrierung für alle Services im src/ Ordner -->
        <prototype namespace="Acme\ExamplePlugin\" resource="../../" exclude="../../{Resources,Migration,*.php}"/>

        <!-- Manuelle Service-Definition (falls nötig) -->
        <service id="Acme\ExamplePlugin\Service\CustomService">
            <argument type="service" id="product.repository"/>
        </service>

        <!-- Event Subscriber -->
        <service id="Acme\ExamplePlugin\Subscriber\ProductSubscriber">
            <tag name="kernel.event_subscriber"/>
        </service>

        <!-- Console Command -->
        <service id="Acme\ExamplePlugin\Command\CustomCommand">
            <tag name="console.command"/>
        </service>

        <!-- Scheduled Task -->
        <service id="Acme\ExamplePlugin\ScheduledTask\CustomTask">
            <tag name="shopware.scheduled.task"/>
        </service>
        
        <service id="Acme\ExamplePlugin\ScheduledTask\CustomTaskHandler">
            <argument type="service" id="scheduled_task.repository"/>
            <tag name="messenger.message_handler"/>
        </service>
    </services>
</container>
```

---

## 4. DAL (Data Abstraction Layer)

### 4.1 Repository pattern

```php
<?php declare(strict_types=1);

namespace Acme\ExamplePlugin\Service;

use Shopware\Core\Content\Product\ProductEntity;
use Shopware\Core\Defaults;
use Shopware\Core\Framework\Context;
use Shopware\Core\Framework\DataAbstractionLayer\EntityRepository;
use Shopware\Core\Framework\DataAbstractionLayer\EntitySearchResult;
use Shopware\Core\Framework\DataAbstractionLayer\Search\Criteria;
use Shopware\Core\Framework\DataAbstractionLayer\Search\Filter\ContainsFilter;
use Shopware\Core\Framework\DataAbstractionLayer\Search\Filter\EqualsFilter;
use Shopware\Core\Framework\DataAbstractionLayer\Search\Filter\RangeFilter;
use Shopware\Core\Framework\DataAbstractionLayer\Search\Sorting\FieldSorting;
use Shopware\Core\Framework\Util\Uuid;

class ProductService
{
    public function __construct(
        private EntityRepository $productRepository
    ) {}

    // READ - Einzelnes Produkt
    public function getProduct(string $id, Context $context): ?ProductEntity
    {
        $criteria = new Criteria([$id]);
        $criteria->addAssociation('media');
        $criteria->addAssociation('categories');
        
        return $this->productRepository->search($criteria, $context)->first();
    }

    // READ - Suche mit Filtern
    public function findActiveProducts(Context $context): EntitySearchResult
    {
        $criteria = new Criteria();
        $criteria->addFilter(new EqualsFilter('active', true));
        $criteria->addSorting(new FieldSorting('createdAt', FieldSorting::DESCENDING));
        $criteria->setLimit(25);
        
        return $this->productRepository->search($criteria, $context);
    }

    // CREATE
    public function createProduct(array $data, Context $context): void
    {
        $this->productRepository->create([
            [
                'id' => Uuid::randomHex(),
                'name' => $data['name'],
                'productNumber' => $data['productNumber'],
                'stock' => $data['stock'],
                'taxId' => $data['taxId'],
                'price' => [
                    [
                        'currencyId' => Defaults::CURRENCY,
                        'gross' => $data['priceGross'],
                        'net' => $data['priceNet'],
                        'linked' => false
                    ]
                ],
            ]
        ], $context);
    }

    // UPDATE
    public function updateProduct(string $id, array $data, Context $context): void
    {
        $this->productRepository->update([
            ['id' => $id, 'name' => $data['name']]
        ], $context);
    }

    // UPSERT (Update oder Insert)
    public function upsertProduct(array $data, Context $context): void
    {
        $this->productRepository->upsert([$data], $context);
    }

    // DELETE
    public function deleteProduct(string $id, Context $context): void
    {
        $this->productRepository->delete([['id' => $id]], $context);
    }
}
```

### 4.2 Criteria - advanced usage (fragment)

Place inside a method; ensure `Criteria` and filter classes are imported.

```php
use Shopware\Core\Framework\DataAbstractionLayer\Search\Aggregation\Metric\AvgAggregation;
use Shopware\Core\Framework\DataAbstractionLayer\Search\Aggregation\Metric\CountAggregation;
use Shopware\Core\Framework\DataAbstractionLayer\Search\Aggregation\Metric\MaxAggregation;
use Shopware\Core\Framework\DataAbstractionLayer\Search\Criteria;
use Shopware\Core\Framework\DataAbstractionLayer\Search\Filter\AndFilter;
use Shopware\Core\Framework\DataAbstractionLayer\Search\Filter\EqualsFilter;
use Shopware\Core\Framework\DataAbstractionLayer\Search\Filter\MultiFilter;
use Shopware\Core\Framework\DataAbstractionLayer\Search\Filter\NotFilter;
use Shopware\Core\Framework\DataAbstractionLayer\Search\Filter\OrFilter;
use Shopware\Core\Framework\DataAbstractionLayer\Search\Filter\RangeFilter;
use Shopware\Core\Framework\DataAbstractionLayer\Search\Sorting\FieldSorting;

$criteria = new Criteria();

// Verschachtelte Filter
$criteria->addFilter(new AndFilter([
    new EqualsFilter('active', true),
    new OrFilter([
        new RangeFilter('stock', [RangeFilter::GT => 0]),
        new EqualsFilter('isCloseout', false)
    ])
]));

// Post-Filter (beeinflussen Aggregationen nicht)
$criteria->addPostFilter(new EqualsFilter('active', true));

// Association mit Filter
$criteria->getAssociation('reviews')
    ->addFilter(new RangeFilter('points', [RangeFilter::GTE => 4]))
    ->addSorting(new FieldSorting('createdAt', FieldSorting::DESCENDING))
    ->setLimit(5);

// Aggregationen
$criteria->addAggregation(new AvgAggregation('avg-rating', 'reviews.points'));
$criteria->addAggregation(new MaxAggregation('max-price', 'price'));
$criteria->addAggregation(new CountAggregation('review-count', 'reviews.id'));

// Full-Text Search
$criteria->setTerm('suchbegriff');

// Pagination
$criteria->setLimit(25);
$criteria->setOffset(50);
```

---

## 8. Events & Subscriber

### 8.1 Event Subscriber

```php
<?php declare(strict_types=1);

namespace Acme\ExamplePlugin\Subscriber;

use Shopware\Core\Content\Product\ProductEvents;
use Shopware\Core\Framework\DataAbstractionLayer\Event\EntityLoadedEvent;
use Shopware\Core\Framework\DataAbstractionLayer\Event\EntityWrittenEvent;
use Shopware\Core\Checkout\Order\Event\OrderPlacedEvent;
use Shopware\Core\Defaults;
use Symfony\Component\EventDispatcher\EventSubscriberInterface;

class ProductSubscriber implements EventSubscriberInterface
{
    public static function getSubscribedEvents(): array
    {
        return [
            ProductEvents::PRODUCT_LOADED_EVENT => 'onProductsLoaded',
            ProductEvents::PRODUCT_WRITTEN_EVENT => 'onProductsWritten',
            'checkout.order.placed' => 'onOrderPlaced',
        ];
    }

    public function onProductsLoaded(EntityLoadedEvent $event): void
    {
        foreach ($event->getEntities() as $product) {
            // Produkt-Logik
        }
    }

    public function onProductsWritten(EntityWrittenEvent $event): void
    {
        if ($event->getContext()->getVersionId() !== Defaults::LIVE_VERSION) {
            return;
        }
        
        foreach ($event->getIds() as $id) {
            // Verarbeitung
        }
    }

    public function onOrderPlaced(OrderPlacedEvent $event): void
    {
        $order = $event->getOrder();
        $context = $event->getContext();
        
        // Order-Logik
    }
}
```

### 8.2 Route-spezifische Events (6.6.11+)

```
{route}.request      // Vor Controller
{route}.response     // Nach Controller
{route}.render       // Vor Twig-Rendering
{route}.encode       // Vor JSON-Encoding (Store-API)
{route}.controller   // Controller-Event

Beispiele:
- store-api.product.listing.request
- frontend.checkout.cart.response
```

---

## 9. Migrations & Entities

### 9.1 Entity Definition

```php
<?php declare(strict_types=1);

namespace Acme\ExamplePlugin\Core\Content\Example;

use Shopware\Core\Framework\DataAbstractionLayer\EntityDefinition;
use Shopware\Core\Framework\DataAbstractionLayer\FieldCollection;
use Shopware\Core\Framework\DataAbstractionLayer\Field\IdField;
use Shopware\Core\Framework\DataAbstractionLayer\Field\StringField;
use Shopware\Core\Framework\DataAbstractionLayer\Field\BoolField;
use Shopware\Core\Framework\DataAbstractionLayer\Field\LongTextField;
use Shopware\Core\Framework\DataAbstractionLayer\Field\FkField;
use Shopware\Core\Framework\DataAbstractionLayer\Field\ManyToOneAssociationField;
use Shopware\Core\Framework\DataAbstractionLayer\Field\Flag\PrimaryKey;
use Shopware\Core\Framework\DataAbstractionLayer\Field\Flag\Required;
use Shopware\Core\Framework\DataAbstractionLayer\Field\Flag\ApiAware;
use Shopware\Core\Content\Media\MediaDefinition;

class ExampleDefinition extends EntityDefinition
{
    public const ENTITY_NAME = 'acme_example';

    public function getEntityName(): string
    {
        return self::ENTITY_NAME;
    }

    public function getEntityClass(): string
    {
        return ExampleEntity::class;
    }

    public function getCollectionClass(): string
    {
        return ExampleCollection::class;
    }

    protected function defineFields(): FieldCollection
    {
        return new FieldCollection([
            (new IdField('id', 'id'))
                ->addFlags(new Required(), new PrimaryKey(), new ApiAware()),
            
            (new StringField('name', 'name'))
                ->addFlags(new Required(), new ApiAware()),
            
            (new LongTextField('description', 'description'))
                ->addFlags(new ApiAware()),
            
            (new BoolField('active', 'active'))
                ->addFlags(new Required(), new ApiAware()),
            
            (new FkField('media_id', 'mediaId', MediaDefinition::class))
                ->addFlags(new ApiAware()),
            
            (new ManyToOneAssociationField('media', 'media_id', MediaDefinition::class, 'id', false))
        ]);
    }
}
```

### 9.2 Migration

```php
<?php declare(strict_types=1);

namespace Acme\ExamplePlugin\Migration;

use Doctrine\DBAL\Connection;
use Shopware\Core\Framework\Migration\MigrationStep;

class Migration1703300000CreateExampleTable extends MigrationStep
{
    public function getCreationTimestamp(): int
    {
        return 1703300000;
    }

    public function update(Connection $connection): void
    {
        $sql = <<<SQL
CREATE TABLE IF NOT EXISTS `acme_example` (
    `id` BINARY(16) NOT NULL,
    `name` VARCHAR(255) NOT NULL,
    `description` LONGTEXT NULL,
    `active` TINYINT(1) NOT NULL DEFAULT 1,
    `media_id` BINARY(16) NULL,
    `created_at` DATETIME(3) NOT NULL,
    `updated_at` DATETIME(3) NULL,
    PRIMARY KEY (`id`),
    KEY `idx.active` (`active`),
    CONSTRAINT `fk.acme_example.media_id`
        FOREIGN KEY (`media_id`) REFERENCES `media` (`id`)
        ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
SQL;
        
        $connection->executeStatement($sql);
    }

    public function updateDestructive(Connection $connection): void
    {
        // Destruktive Änderungen (DROP, etc.)
    }
}
