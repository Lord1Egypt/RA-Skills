# PRODUCT EXTENSIONS OVERVIEW

Compiled excerpts from the Shopware Developer Documentation snapshot. Prefer live docs at [developer.shopware.com](https://developer.shopware.com/) when in doubt.

---

## Concept
**Source:** [products/extensions/migration-assistant/concept.md](https://developer.shopware.com/docs/v6.6/products/extensions/migration-assistant/concept.md)  
# Concept

[Shopware Migration Assistant](https://github.com/shopware/SwagMigrationAssistant) was built with simple but powerful concepts in mind. These enable you to extend the plugin in various ways and migrate data into the Shopware 6 environment. You should have a basic understanding of how to use the migration plugin and its core features, before extending it yourself. (this documentation will not explain the usage of the plugin).

We will provide you with a basic introduction into the concepts and structure right here in this chapter. Take a look at the last headline (Extension points) to find out more about the various ways to extend this plugin.

## Profile and connections

Users of the plugin can create connections to different source systems. A connection is used to allow multiple migrations from the same source and update the right data (mapping). Connections require a specific profile, indicating the type of source system. Users can, for example, create a connection to a Shopware shop using the Shopware 5.5 profile. Developers are able to create their own profiles from scratch and connect to different source systems or just build up on and extend existing ones.

For more details have a look at [Profile and Connection](./concept/profile-and-connection).

## DataSelection and dataSet

These are the fundamental data structures for define what to migrate. Each `DataSet` represents an entity, for example a database table. Each `DataSelection` represents an orderly group of `DataSets`. For more Information take a look at [DataSelection and DataSet](./concept/dataselection-and-dataset).

## Migration context

This data structure provides all necessary data of the migration. For more details have a look at [Migration Context](./concept/migration-context).

## Premapping

Because the structure of the source system does not always match the structure of the target system, the user may need to map the old structure to the new one. For example, in Shopware 5 we have default salutations like 'mr', but the user can also create custom ones. In Shopware 6 there are also default salutations like 'mr' and the user can also create custom ones. So the salutation 'mr' from Shopware 5 must be mapped to Shopware 6 'mr'. In this default case the mapping can be achieved automatically, but customized salutations will most likely have to be mapped manually. The premapping will be written into the mapping table to associate the old identifier with the new one. For more details on this, head to [Premapping](./concept/premapping) concepts.

## Gateway and reader

Users will have to specify a gateway for the connection. The gateway defines the way of communicating with the source system. Behind the user interface we use `Reader` objects to read the data from the source system. For the `shopware55` profile we have the `api` gateway, which communicates via http/s with the source system, and the `local` gateway, which communicates directly with the source system's database. Thus both systems must be on the same server for successfully using the `local` gateway.

If you want to use the `ShopwareApiGateway` you have to download the [Shopware Migration Connector](https://github.com/shopware/SwagMigrationConnector) plugin for your Shopware 5. For more details have a look at the [Gateway and Reader](./concept/gateway-and-reader).

## Converter, mapping and deltas

Data gathered by `Reader` objects is transferred to `Converter` objects that put the data in a format Shopware 6 is able to work with. Simultaneously entries in the underlying mapping table are inserted to map the old identifiers to the new ones for future migrations (Have a look at the `MappingService` for that). The mapping is saved for the current connection. Converted data will be removed after the migration, the mapping will stay persistent. Also a checksum is saved to the mapping to identify and skip the same source data (data has not been changed since last migration). You can find out more about them in [Converter and Mapping](./concept/convert-and-mapping) section of this guide.

## Logging

During any migration, especially during the data conversion, there will possibly be errors that should be logged. The users can see these errors and these should be as helpful as possible. For more information, have a look at [Logging](./concept/logging).

## Writer

The `Writer` objects will receive the converted data and write it to Shopware 6. There is no special magic here and you don't need to worry about error handling because the migration assistant takes care of it. To learn more about them, take a look at [Writer](./concept/writer) concept.

## Media processing

During a typical migration we download the media files from the source system to Shopware 6. This is the last processing step in the migration and may be done differently for other gateways. For example the `local` gateway will copy and rename the files directly in the local filesystem. For more Details you can look at [Media Processing](./concept/media-processing).

## After migration

All fetched data will be deleted after finishing or aborting a migration run, but the mapping of the identifiers will stay.

## The migration procedure

The following bullet points will give you a general overview of what happens during a common migration.

1. The user selects / creates a connection (with a profile and gateway specified)
2. The user selects some of the available data (`DataSelections`)
3. Premapping check / execution: The user maps data from the source system to the current system (These decisions are stored with the connection.)
4. Fetch data for every `DataSet` in every selected `DataSelection` (mapping is used to store / use the identifiers from the source system.) 4.1 The corresponding `Reader` reads the data 4.2 The corresponding `Converter` converts the data
5. Write data for every `DataSet` in every selected `DataSelection` 5.1 The corresponding `Writer` writes the data
6. Process media, if necessary for example to download / copy images 6.1 Data in `swag_migration_media_file` table will be downloaded / copied 6.2 Files are assigned to media objects in Shopware 6
7. Finish migration to cleanup

These steps can be done multiple times. Each migration is called a `Run` / `MigrationRun` and will be saved to let the users know about any errors that occurred (in form of a detailed history).

## Extension points

The recommended way to migrate plugin data from a source system is to extend that profile by a new `DataSelection`. It is also possible to create a new profile, in case a migration from a different shop / source system is sought.

Take a look at the following HowTos for your scenario to get a step by step tutorial:

* [Extending a Shopware Migration Profile](./guides/extending-a-shopware-migration-profile) <- migrating your first basic plugin data (via local gateway)
* [Extending the Migration Connector](./guides/extending-the-migration-connector) <- add API support for your migration
* [Decorating a Shopware Migration Assistant Converter](./guides/decorating-a-shopware-migration-assistant-converter) <- implement a premapping and change the behavior of an existing converter
* [Creating a New Migration Profile](./guides/creating-a-new-migration-profile) <- create a new profile from scratch to support a third party source system (other than Shopware)

---

---

## Convert and Mapping
**Source:** [products/extensions/migration-assistant/concept/convert-and-mapping.md](https://developer.shopware.com/docs/v6.6/products/extensions/migration-assistant/concept/convert-and-mapping.md)  
*(Body truncated in this bundle; follow the link for the rest.)*

# Convert and Mapping

## Overview

Data gathered by `Reader` objects is transferred to `Converter` objects that put the data in a format Shopware 6 is able to work with. Simultaneously entries in the underlying mapping table are inserted to map the old identifiers to the new ones for future migrations. The mapping is saved for the current connection. After the migration, the converted data will be removed, and the mapping will stay persistent.

## Converter

All converters are registered in service container like this:

```html
<service id="SwagMigrationAssistant\Profile\Shopware\Converter\ProductConverter"
         parent="SwagMigrationAssistant\Profile\Shopware\Converter\ShopwareConverter" abstract="true">
    <argument type="service" id="SwagMigrationAssistant\Migration\Media\MediaFileService"/>
</service>
```

The converters have to extend the `ShopwareConverter` class and implement the `convert` method. This method will receive one data entry at a time. It will have to be returned in the right format to be usable for the `writer`.

```php
<?php declare(strict_types=1);

/* SwagMigrationAssistant/Profile/Shopware/Converter/ProductConverter.php */

abstract class ProductConverter extends ShopwareConverter
{
    /* ... */

    /**
     * @throws ParentEntityForChildNotFoundException
     */
    public function convert(
        array $data,
        Context $context,
        MigrationContextInterface $migrationContext
    ): ConvertStruct {
        $this->generateChecksum($data);
        $this->context = $context;
        $this->migrationContext = $migrationContext;
        $this->runId = $migrationContext->getRunUuid();
        $this->oldProductId = $data['detail']['ordernumber'];
        $this->mainProductId = $data['detail']['articleID'];
        $this->locale = $data['_locale'];

        $connection = $migrationContext->getConnection();
        $this->connectionName = '';
        $this->connectionId = '';
        if ($connection !== null) {
            $this->connectionId = $connection->getId();
            $this->connectionName = $connection->getName();
        }

        $fields = $this->checkForEmptyRequiredDataFields($data, $this->requiredDataFieldKeys);
        if (!empty($fields)) {
            $this->loggingService->addLogEntry(new EmptyNecessaryFieldRunLog(
                $this->runId,
                DefaultEntities::PRODUCT,
                $this->oldProductId,
                implode(',', $fields)
            ));

            return new ConvertStruct(null, $data);
        }

        $this->productType = (int) $data['detail']['kind'];
        unset($data['detail']['kind']);
        $isProductWithVariant = $data['configurator_set_id'] !== null;

        if ($this->productType === self::MAIN_PRODUCT_TYPE && $isProductWithVariant) {
            return $this->convertMainProduct($data);
        }

        if ($this->productType === self::VARIANT_PRODUCT_TYPE && $isProductWithVariant) {
            return $this->convertVariantProduct($data);
        }

        $converted = $this->getUuidForProduct($data);
        $converted = $this->getProductData($data, $converted);

        if (isset($data['categories'])) {
            $converted['categories'] = $this->getCategoryMapping($data['categories']);
        }
        unset($data['categories']);

        if (isset($data['shops'])) {
            $converted['visibilities'] = $this->getVisibilities($converted, $data['shops']);
        }
        unset($data['shops']);

        unset($data['detail']['id'], $data['detail']['articleID']);

        if (empty($data['detail'])) {
            unset($data['detail']);
        }

        $returnData = $data;
        if (empty($returnData)) {
            $returnData = null;
        }
        $this->updateMainMapping($migrationContext, $context);

        $mainMapping = $this->mainMapping['id'] ?? null;

        return new ConvertStruct($converted, $returnData, $mainMapping);
    }

    /* ... */
}
```

As you see above, the `convert` method gets the source system data, checks with `checkForEmptyRequiredDataFields` if the necessary data fields are filled, and returns a `ConvertStruct`. The `ConvertStruct` contains the converted value in the structure of Shopware 6 and all source system data which could not be mapped to the Shopware 6 structure. If the required fields are not filled, the convert method returns a `ConvertStruct` without a `converted` value and all of the given source system data as the `unmapped` value.

Also, every `Converter` needs to implement the `getSourceIdentifier` method like the below:

```php
/* SwagMigrationAssistant/Profile/Shopware/Converter/ProductConverter.php */

/**
 * Get the identifier of the source data, which is only known to the converter
 */
public function getSourceIdentifier(array $data): string
{
    return $data['detail']['ordernumber'];
}
```

This is the main identifier of the incoming data, and it will be used to look for already migrated data (which will be covered later in this chapter by the Deltas concept).

## Mapping

Many entities rely on other entities, so they have to be converted in a specific order. Because of this and the Shopware Migration Assistant's ability to perform multiple migrations without resetting Shopware 6, source system identifiers must be mapped to their new counterparts. Find a mapping example in the following code snippet:

```php
/* SwagMigrationAssistant/Profile/Shopware/Converter/ProductConverter.php */

private function getUuidForProduct(array &$data): array
{
    $this->mainMapping = $this->mappingService->getOrCreateMapping(
        $this->connectionId,
        DefaultEntities::PRODUCT,
        $this->oldProductId,
        $this->context,
        $this->checksum
    );

    $converted = [];
    $converted['id'] = $this->mainMapping['entityUuid'];

    $mapping = $this->mappingService->getOrCreateMapping(
        $this->connectionId,
        DefaultEntities::PRODUCT_MAIN,
        $data['detail']['articleID'],
        $this->context,
        null,
        null,
        $converted['id']
    );
    $this->mappingIds[] = $mapping['id']; // Take a look at the performance section below for details on this.

    return $converted;
}
```

The following function employs the `getOrCreateMapping` function, which is part of the mapping service to acquire a unique identifier for the product that is about to get mapped to the source system's identifier and, at the same time, creating a new mapping entry in the `swag_migration_mapping` table. If there already is a unique identifier for the product, the `getOrCreateMapping` method, instead of creating a duplicate entry, returns the existing identifier:

```php
/* SwagMigrationAssistant/Migration/Mapping/MappingService.php */

public function getOrCreateMapping(
    string $connectionId,
    string $entityName,
    string $oldIdentifier,
    Context $context,
    ?string $checksum = null,
    ?array $additionalData = null,
    ?string $uuid = null
): array {
    $mapping = $this->getMapping($connectionId, $entityName, $oldIdentifier, $context);

    if (!isset($mapping)) {
        return $this->createMapping($connectionId, $entityName, $oldIdentifier, $checksum, $additionalData, $uuid);
    }

    if ($uuid !== null) {
        $mapping['entityUuid'] = $uuid;
        $this->saveMapping($mapping);

        return $mapping;
    }

    return $mapping;
}
```

Sometimes it is not necessary to create a new identifier, and it may be enough to only get the mapping identifier. In the following example, there is an entity with a premapping and the converter simply uses the mapping service's `getMapping` method:

```php
/* SwagMigrationAssistant/Profile/Shopware/Converter/CustomerConverter.php */

protected function getDefaultPaymentMethod(array $originalData): ?string
{
    $paymentMethodMapping = $this->mappingService->getMapping(
        $this->connectionId,
        PaymentMethodReader::getMappingName(),
        $originalData['id'],
        $this->context
    );

    if ($paymentMethodMapping === null) {
        $this->loggingService->addLogEntry(new UnknownEntityLog(
            $this->runId,
            DefaultEntities::PAYMENT_METHOD,
            $originalData['id'],
            DefaultEntities::CUSTOMER,
            $this->oldCustomerId
        ));

        return null;
    }
    $this->mappingIds[] = $paymentMethodMapping['id'];

    return $paymentMethodMapping['entityUuid'];
}
```

The `getMapping` method only fetches the identifier from the database and doesn't create a new one:

```php
/* SwagMigrationAssistant/Migration/Mapping/MappingService.php */

public function getMapping(
    string $connectionId,
    string $entityName,
    string $oldIdentifier,
    Context $context
): ?array {
    if (isset($this->mappings[md5($entityName . $oldIdentifier)])) {
        return $this->mappings[md5($entityName . $oldIdentifier)];
    }

    $criteria = new Criteria();
    $criteria->addFilter(new EqualsFilter('connectionId', $connectionId));
    $criteria->addFilter(new EqualsFilter('entity', $entityName));
    $criteria->addFilter(new EqualsFilter('oldIdentifier', $oldIdentifier));
    $criteria->setLimit(1);

    $result =  $this->migrationMappingRepo->search($criteria, $context);

    if ($result->getTotal() > 0) {
        /** @var SwagMigrationMappingEntity $element */
        $element = $result->getEntities()->first();

        $mapping = [
            'id' => $element->getId(),
            'connectionId' => $element->getConnectionId(),
            'entity' => $element->getEntity(),
            'oldIdentifier' => $element->getOldIdentifier(),
            'entityUuid' => $element->getEntityUuid(),
            'checksum' => $element->getChecksum(),
            'additionalData' => $element->getAdditionalData(),
        ];
        $this->mappings[md5($entityName . $oldIdentifier)] = $mapping;

        return $mapping;
    }

    return null;
}
```

## Deltas

One of the parameters for the `getOrCreateMapping` Method is the `checksum`. It is used to identify unchanged data (source system data that has not been changed since the last migration). This will greatly improve the performance of future migrations.

To get this checksum, you can use the `generateChecksum` method of the base `Converter` class:

```php
/* SwagMigrationAssistant/Migration/Converter/Converter.php */

/**
 * Generates a unique checksum for the data array to recognize changes
 * on repeated migrations.
 */
protected function generateChecksum(array $data): void
{
    $this->checksum = md5(serialize($data));
}
```

This is used in the first line of the converter with the raw data that comes from the `Reader` object:

```php
/* SwagMigrationAssistant/Profile/Shopware/Converter/ProductConverter.php */

public function convert(
    array $data,
    Context $context,
    MigrationContextInterface $migrationContext
): ConvertStruct {
    $this->generateChecksum($data);

    /* ... */

    // This is also important, so the checksum can be saved to the right mapping!
    $this->mainMapping = $this->mappingService->getOrCreateMapping(
        $this->connectionId,
        DefaultEntities::PRODUCT,
        $this->oldProductId,
        $this->context,
        $this->checksum
    );

    /* ... */

    // Important to put the mainMapping['id'] to the ConvertStruct
    $mainMapping = $this->mainMapping['id'] ?? null;
    return new ConvertStruct($converted, $returnData, $mainMapping);

    /* ... */
}
```

For the checksum to be saved to the right mapping, make sure that you set the `mainMapping` attribute of the base `Converter` class. Internally the checksum of the main mapping of an entity will be compared to the incoming data checksum and if it is the same, it will be skipped by the converter and also by the writer (you will not receive the data with the same checksum in your converter), which increases the performance of repeated migrations massively. For more information, look at the corresponding `filterDeltas` method

… **Truncated.** Full document: https://developer.shopware.com/docs/v6.6/products/extensions/migration-assistant/concept/convert-and-mapping.md


---

## DataSelection and DataSet
**Source:** [products/extensions/migration-assistant/concept/dataselection-and-dataset.md](https://developer.shopware.com/docs/v6.6/products/extensions/migration-assistant/concept/dataselection-and-dataset.md)  
# DataSelection and DataSet

These are the fundamental data structures for defining what to migrate. Each `DataSelection` consists of one or more `DataSets`:

* ProductDataSelection (position: 100)
  * MediaFolderDataSet
  * ProductAttributeDataSet
  * ProductPriceAttributeDataSet
  * ManufacturerAttributeDataSet
  * ProductDataSet
  * PropertyGroupOptionDataSet
  * ProductOptionRelationDataSet
  * ProductPropertyRelationDataSet
  * TranslationDataSet
  * CrossSellingDataSet
* MediaDataSelection (position: 300)
  * MediaFolderDataSet
  * MediaDataSet

The order of the `DataSets` in the `DataSelection` class is important and specifies the processing order. `DataSelection` also holds a position specifying the order applied when migrating (lower numbers are migrated earlier). The `getDataSetsRequiredForCount` method returns an array of all DataSets. Its count should be displayed in the Administration.

Please take a look at the `DataSelection` example:

```php
<?php declare(strict_types=1);

namespace SwagMigrationAssistant\Profile\Shopware\DataSelection;

use SwagMigrationAssistant\Migration\DataSelection\DataSelectionInterface;
use SwagMigrationAssistant\Migration\DataSelection\DataSelectionStruct;
use SwagMigrationAssistant\Migration\MigrationContextInterface;
use SwagMigrationAssistant\Profile\Shopware\DataSelection\DataSet\CrossSellingDataSet;
use SwagMigrationAssistant\Profile\Shopware\DataSelection\DataSet\ManufacturerAttributeDataSet;
use SwagMigrationAssistant\Profile\Shopware\DataSelection\DataSet\MediaFolderDataSet;
use SwagMigrationAssistant\Profile\Shopware\DataSelection\DataSet\ProductAttributeDataSet;
use SwagMigrationAssistant\Profile\Shopware\DataSelection\DataSet\ProductDataSet;
use SwagMigrationAssistant\Profile\Shopware\DataSelection\DataSet\ProductOptionRelationDataSet;
use SwagMigrationAssistant\Profile\Shopware\DataSelection\DataSet\ProductPriceAttributeDataSet;
use SwagMigrationAssistant\Profile\Shopware\DataSelection\DataSet\ProductPropertyRelationDataSet;
use SwagMigrationAssistant\Profile\Shopware\DataSelection\DataSet\PropertyGroupOptionDataSet;
use SwagMigrationAssistant\Profile\Shopware\DataSelection\DataSet\TranslationDataSet;
use SwagMigrationAssistant\Profile\Shopware\ShopwareProfileInterface;

class ProductDataSelection implements DataSelectionInterface
{
    public const IDENTIFIER = 'products';

    public function supports(MigrationContextInterface $migrationContext): bool
    {
        return $migrationContext->getProfile() instanceof ShopwareProfileInterface;
    }

    public function getData(): DataSelectionStruct
    {
        return new DataSelectionStruct(
            self::IDENTIFIER,
            $this->getDataSets(),
            $this->getDataSetsRequiredForCount(),
            'swag-migration.index.selectDataCard.dataSelection.products', // Snippet name
            100, // The position of the dataSelection
            true, // Is process-media needed (to download / copy images for example),
            DataSelectionStruct::BASIC_DATA_TYPE, // specify the type of data (core data or plugin data)
            false // Is the selection required for every migration? (the user can't unselect this data selection)
        );
    }

    public function getDataSets(): array
    {
        return [
            // The order matters!
            new MediaFolderDataSet(),
            new ProductAttributeDataSet(),
            new ProductPriceAttributeDataSet(),
            new ManufacturerAttributeDataSet(),
            new ProductDataSet(),
            new PropertyGroupOptionDataSet(),
            new ProductOptionRelationDataSet(),
            new ProductPropertyRelationDataSet(),
            new TranslationDataSet(),
            new CrossSellingDataSet(),
        ];
    }

    public function getDataSetsRequiredForCount(): array
    {
        return [
            new ProductDataSet(),
        ];
    }
}
```

Here's a `DataSet` example:

```php
<?php declare(strict_types=1);

namespace SwagMigrationAssistant\Profile\Shopware\DataSelection\DataSet;

use SwagMigrationAssistant\Migration\DataSelection\DataSet\DataSet;
use SwagMigrationAssistant\Migration\DataSelection\DefaultEntities;
use SwagMigrationAssistant\Migration\MigrationContextInterface;
use SwagMigrationAssistant\Profile\Shopware\ShopwareProfileInterface;

class ProductDataSet extends DataSet
{
    public static function getEntity(): string
    {
        return DefaultEntities::PRODUCT;
    }

    public function supports(MigrationContextInterface $migrationContext): bool
    {
        return $migrationContext->getProfile() instanceof ShopwareProfileInterface;
    }
}
```

The `dataSelections` are registered the following way:

```html
<service id="SwagMigrationAssistant\Profile\Shopware\DataSelection\ProductDataSelection">
    <tag name="shopware.migration.data_selection"/>
</service>
```

It is also possible to specify the same `DataSets` in multiple `DataSelections` (this should only be done if no other options are available). Have a look at the `ProductReviewDataSelection`:

```php
<?php declare(strict_types=1);

namespace SwagMigrationAssistant\Profile\Shopware\DataSelection;

use SwagMigrationAssistant\Migration\DataSelection\DataSelectionInterface;
use SwagMigrationAssistant\Migration\DataSelection\DataSelectionStruct;
use SwagMigrationAssistant\Migration\MigrationContextInterface;
use SwagMigrationAssistant\Profile\Shopware\DataSelection\DataSet\CrossSellingDataSet;
use SwagMigrationAssistant\Profile\Shopware\DataSelection\DataSet\CustomerAttributeDataSet;
use SwagMigrationAssistant\Profile\Shopware\DataSelection\DataSet\CustomerDataSet;
use SwagMigrationAssistant\Profile\Shopware\DataSelection\DataSet\ManufacturerAttributeDataSet;
use SwagMigrationAssistant\Profile\Shopware\DataSelection\DataSet\MediaFolderDataSet;
use SwagMigrationAssistant\Profile\Shopware\DataSelection\DataSet\ProductAttributeDataSet;
use SwagMigrationAssistant\Profile\Shopware\DataSelection\DataSet\ProductDataSet;
use SwagMigrationAssistant\Profile\Shopware\DataSelection\DataSet\ProductOptionRelationDataSet;
use SwagMigrationAssistant\Profile\Shopware\DataSelection\DataSet\ProductPriceAttributeDataSet;
use SwagMigrationAssistant\Profile\Shopware\DataSelection\DataSet\ProductPropertyRelationDataSet;
use SwagMigrationAssistant\Profile\Shopware\DataSelection\DataSet\ProductReviewDataSet;
use SwagMigrationAssistant\Profile\Shopware\DataSelection\DataSet\PropertyGroupOptionDataSet;
use SwagMigrationAssistant\Profile\Shopware\DataSelection\DataSet\TranslationDataSet;
use SwagMigrationAssistant\Profile\Shopware\ShopwareProfileInterface;

class ProductReviewDataSelection implements DataSelectionInterface
{
    public const IDENTIFIER = 'productReviews';

    public function supports(MigrationContextInterface $migrationContext): bool
    {
        return $migrationContext->getProfile() instanceof ShopwareProfileInterface;
    }

    public function getData(): DataSelectionStruct
    {
        return new DataSelectionStruct(
            self::IDENTIFIER,
            $this->getDataSets(),
            $this->getDataSetsRequiredForCount(),
            'swag-migration.index.selectDataCard.dataSelection.productReviews',
            250,
            true
        );
    }

    /**
     * {@inheritdoc}
     */
    public function getDataSets(): array
    {
        return [
            new MediaFolderDataSet(),
            new ProductAttributeDataSet(),
            new ProductPriceAttributeDataSet(),
            new ManufacturerAttributeDataSet(),
            new ProductDataSet(),
            new PropertyGroupOptionDataSet(),
            new ProductOptionRelationDataSet(),
            new ProductPropertyRelationDataSet(),
            new TranslationDataSet(),
            new CrossSellingDataSet(),
            new CustomerAttributeDataSet(),
            new CustomerDataSet(),
            new ProductReviewDataSet(),
        ];
    }

    public function getDataSetsRequiredForCount(): array
    {
        return [
            new ProductReviewDataSet(),
        ];
    }
}
```

::: info
There are duplicate DataSets from the `ProductDataSelection`, because they are also required if the user does not select the product `DataSelection`. If the user selects both, this `DataSets` will be only migrated once (with their first occurrence).
:::

---

---

## Gateway and Reader
**Source:** [products/extensions/migration-assistant/concept/gateway-and-reader.md](https://developer.shopware.com/docs/v6.6/products/extensions/migration-assistant/concept/gateway-and-reader.md)  
# Gateway and Reader

## Overview

Users will have to specify a gateway for the connection. The gateway defines the way of communicating with the source system. Behind the user interface, we use `Reader` objects to read the data from the source system. For the `shopware55` profile, we have the `api` gateway, which communicates via http/s with the source system, and the `local` gateway, which communicates directly with the source system's database. Thus both systems must be on the same server to successfully use the `local` gateway.

## Gateway

The gateway defines how to communicate from Shopware 6 with your source system, like Shopware 5. Every profile needs to have at least one gateway. Gateways need to be defined in the corresponding service xml using the `shopware.migration.gateway` tag:

```html
<!-- Shopware Profile Gateways -->
<service id="SwagMigrationAssistant\Profile\Shopware\Gateway\Local\ShopwareLocalGateway">
    <argument type="service" id="SwagMigrationAssistant\Profile\Shopware\Gateway\Local\ReaderRegistry" />
    <argument type="service" id="SwagMigrationAssistant\Profile\Shopware\Gateway\Local\Reader\EnvironmentReader" />
    <argument type="service" id="SwagMigrationAssistant\Profile\Shopware\Gateway\Local\Reader\TableReader" />
    <argument type="service" id="SwagMigrationAssistant\Profile\Shopware\Gateway\Connection\ConnectionFactory" />
    <argument type="service" id="currency.repository"/>
    <tag name="shopware.migration.gateway" />
</service>

<service id="SwagMigrationAssistant\Profile\Shopware\Gateway\Api\ShopwareApiGateway">
    <argument type="service" id="SwagMigrationAssistant\Migration\Gateway\Reader\ReaderRegistry"/>
    <argument type="service" id="SwagMigrationAssistant\Profile\Shopware\Gateway\Api\Reader\EnvironmentReader" />
    <argument type="service" id="SwagMigrationAssistant\Profile\Shopware\Gateway\Api\Reader\TableReader" />
    <argument type="service" id="SwagMigrationAssistant\Profile\Shopware\Gateway\Api\Reader\TableCountReader" />
    <argument type="service" id="currency.repository"/>
    <tag name="shopware.migration.gateway" />
</service>
```

To use the `ShopwareApiGateway`, you must download the corresponding Shopware 5 plugin [Shopware migration connector](https://github.com/shopware/SwagMigrationConnector) first.

This tag is used by `GatwayRegistry`. This registry loads all tagged gateways and chooses a suitable gateway based on the migration's context and a unique identifier composed of a combination of profile and gateway name:

```php
<?php declare(strict_types=1);

namespace SwagMigrationAssistant\Migration\Gateway;

use SwagMigrationAssistant\Exception\MigrationContextPropertyMissingException;
use SwagMigrationAssistant\Exception\GatewayNotFoundException;
use SwagMigrationAssistant\Migration\MigrationContextInterface;

class GatewayRegistry implements GatewayRegistryInterface
{
    /**
     * @var GatewayInterface[]
     */
    private iterable $gateways;

    /**
     * @param GatewayInterface[] $gateways
    */
    public function __construct(iterable $gateways)
    {
        $this->gateways = $gateways;
    }

    /**
     * @throws GatewayNotFoundException
     *
     * @return GatewayInterface[]
     */
    public function getGateways(MigrationContextInterface $migrationContext): array
    {
        $gateways = [];
        foreach ($this->gateways as $gateway) {
            if ($gateway->supports($migrationContext)) {
                $gateways[] = $gateway;
            }
        }

        return $gateways;
    }

    /**
     * @throws GatewayNotFoundException
     */
    public function getGateway(MigrationContextInterface $migrationContext): GatewayInterface
    {
        $connection = $migrationContext->getConnection();
        if ($connection === null) {
            throw new MigrationContextPropertyMissingException('Connection');
        }

        $profileName = $connection->getProfileName();
        $gatewayName = $connection->getGatewayName();

        foreach ($this->gateways as $gateway) {
            if ($gateway->supports($migrationContext) && $gateway->getName() === $gatewayName) {
                return $gateway;
            }
        }

        throw new GatewayNotFoundException($profileName . '-' . $gatewayName);
    }
}
```

The gateway class has to implement the `GatewayInterface` to support all required methods. As you can see below, the gateway uses the right readers, which internally open a connection to the source system to receive the entity data:

```php
<?php declare(strict_types=1);

namespace SwagMigrationAssistant\Profile\Shopware\Gateway\Local;

use Shopware\Core\Defaults;
use Shopware\Core\Framework\Context;
use Shopware\Core\Framework\DataAbstractionLayer\EntityRepository;
use Shopware\Core\Framework\DataAbstractionLayer\Search\Criteria;
use Shopware\Core\System\Currency\CurrencyEntity;
use SwagMigrationAssistant\Migration\EnvironmentInformation;
use SwagMigrationAssistant\Migration\Gateway\Reader\EnvironmentReaderInterface;
use SwagMigrationAssistant\Migration\Gateway\Reader\ReaderRegistry;
use SwagMigrationAssistant\Migration\MigrationContextInterface;
use SwagMigrationAssistant\Migration\RequestStatusStruct;
use SwagMigrationAssistant\Profile\Shopware\Exception\DatabaseConnectionException;
use SwagMigrationAssistant\Profile\Shopware\Gateway\Connection\ConnectionFactoryInterface;
use SwagMigrationAssistant\Profile\Shopware\Gateway\ShopwareGatewayInterface;
use SwagMigrationAssistant\Profile\Shopware\Gateway\TableReaderInterface;
use SwagMigrationAssistant\Profile\Shopware\ShopwareProfileInterface;

class ShopwareLocalGateway implements ShopwareGatewayInterface
{
    public const GATEWAY_NAME = 'local';

    private ReaderRegistry $readerRegistry;

    private EnvironmentReaderInterface $localEnvironmentReader;

    private TableReaderInterface $localTableReader;

    private ConnectionFactoryInterface $connectionFactory;

    private EntityRepository $currencyRepository;

    public function __construct(
        ReaderRegistry $readerRegistry,
        EnvironmentReaderInterface $localEnvironmentReader,
        TableReaderInterface $localTableReader,
        ConnectionFactoryInterface $connectionFactory,
        EntityRepository $currencyRepository
    ) {
        $this->readerRegistry = $readerRegistry;
        $this->localEnvironmentReader = $localEnvironmentReader;
        $this->localTableReader = $localTableReader;
        $this->connectionFactory = $connectionFactory;
        $this->currencyRepository = $currencyRepository;
    }

    public function getName(): string
    {
        return self::GATEWAY_NAME;
    }

    public function getSnippetName(): string
    {
        return 'swag-migration.wizard.pages.connectionCreate.gateways.shopwareLocal';
    }

    public function supports(MigrationContextInterface $migrationContext): bool
    {
        return $migrationContext->getProfile() instanceof ShopwareProfileInterface;
    }

    public function read(MigrationContextInterface $migrationContext): array
    {
        $reader = $this->readerRegistry->getReader($migrationContext);

        return $reader->read($migrationContext);
    }

    public function readEnvironmentInformation(MigrationContextInterface $migrationContext, Context $context): EnvironmentInformation
    {
        $connection = $this->connectionFactory->createDatabaseConnection($migrationContext);
        $profile = $migrationContext->getProfile();

        if ($connection === null) {
            $error = new DatabaseConnectionException();

            return new EnvironmentInformation(
                $profile->getSourceSystemName(),
                $profile->getVersion(),
                '-',
                [],
                [],
                new RequestStatusStruct($error->getErrorCode(), $error->getMessage())
            );
        }

        try {
            $connection->connect();
        } catch (\Exception $e) {
            $error = new DatabaseConnectionException();

            return new EnvironmentInformation(
                $profile->getSourceSystemName(),
                $profile->getVersion(),
                '-',
                [],
                [],
                new RequestStatusStruct($error->getErrorCode(), $error->getMessage())
            );
        }
        $connection->close();
        $environmentData = $this->localEnvironmentReader->read($migrationContext);

        /** @var CurrencyEntity $targetSystemCurrency */
        $targetSystemCurrency = $this->currencyRepository->search(new Criteria([Defaults::CURRENCY]), $context)->get(Defaults::CURRENCY);
        if (!isset($environmentData['defaultCurrency'])) {
            $environmentData['defaultCurrency'] = $targetSystemCurrency->getIsoCode();
        }

        $totals = $this->readTotals($migrationContext, $context);

        return new EnvironmentInformation(
            $profile->getSourceSystemName(),
            $profile->getVersion(),
            $environmentData['host'],
            $totals,
            $environmentData['additionalData'],
            new RequestStatusStruct(),
            false,
            [],
            $targetSystemCurrency->getIsoCode(),
            $environmentData['defaultCurrency']
        );
    }

    public function readTotals(MigrationContextInterface $migrationContext, Context $context): array
    {
        $readers = $this->readerRegistry->getReaderForTotal($migrationContext);

        $totals = [];
        foreach ($readers as $reader) {
            $total = $reader->readTotal($migrationContext);

            if ($total === null) {
                continue;
            }

            $totals[$total->getEntityName()] = $total;
        }

        return $totals;
    }

    public function readTable(MigrationContextInterface $migrationContext, string $tableName, array $filter = []): array
    {
        return $this->localTableReader->read($migrationContext, $tableName, $filter);
    }
}
```

---

---

## Logging
**Source:** [products/extensions/migration-assistant/concept/logging.md](https://developer.shopware.com/docs/v6.6/products/extensions/migration-assistant/concept/logging.md)  
# Logging

Logging is essential for anyone using the Shopware Migration Assistant. In case of failure, it enables users to find out why part of their data might be missing. Most of the logging takes place in the `Converter` classes each time they detect missing required values. Also, every exception will create a log entry automatically.

We use `LogEntry` objects for our logging, so it's easier to group logs/errors of the same type and get the corresponding amount. Here is an example of how the logging works in the `CustomerConverter`:

```php
<?php declare(strict_types=1);

abstract class CustomerConverter extends ShopwareConverter
{
    /* ... */

    public function convert(
            array $data,
            Context $context,
            MigrationContextInterface $migrationContext
        ): ConvertStruct
    {
        $this->generateChecksum($data);
        $oldData = $data;
        $this->runId = $migrationContext->getRunUuid();

        $fields = $this->checkForEmptyRequiredDataFields($data, $this->requiredDataFieldKeys);

        if (!empty($fields)) {
            $this->loggingService->addLogEntry(new EmptyNecessaryFieldRunLog(
                $this->runId,
                DefaultEntities::CUSTOMER,
                $data['id'],
                implode(',', $fields)
            ));

            return new ConvertStruct(null, $oldData);
        }

        /* ... */
    }

    /* ... */
}
```

You can get the `LoggingService` from the service container. Use the `addLogEntry` method with a compatible instance of `LogEntryInterface` and save the logging later with `saveLogging`:

```php
<?php declare(strict_types=1);

interface LoggingServiceInterface
{
    public function addLogEntry(LogEntryInterface $logEntry): void;

    public function saveLogging(Context $context): void;
}
```

Look at the already existing classes, which implement the `LogEntryInterface` to find one that fits your needs, just like the `EmptyNecessaryFieldRunLog` in the `CustomerConverter` example above. All the general LogEntry classes are located under the following namespace `SwagMigrationAssistant\Migration\Logging\Log`.

To create a custom LogEntry make sure you at least implement the `LogEntryInterface` or, if your log happens during a running migration, you can also extend your LogEntry by the `BaseRunLogEntry`.

```php
<?php declare(strict_types=1);

namespace SwagMigrationAssistant\Migration\Logging\Log;

class EmptyNecessaryFieldRunLog extends BaseRunLogEntry
{
    private string $emptyField;

    public function __construct(string $runId, string $entity, string $sourceId, string $emptyField)
    {
        parent::__construct($runId, $entity, $sourceId);
        $this->emptyField = $emptyField;
    }

    public function getCode(): string
    {
        $entity = $this->getEntity();
        if ($entity === null) {
            return 'SWAG_MIGRATION_EMPTY_NECESSARY_FIELD';
        }

        return sprintf('SWAG_MIGRATION_EMPTY_NECESSARY_FIELD_%s', mb_strtoupper($entity));
    }

    public function getLevel(): string
    {
        return self::LOG_LEVEL_WARNING;
    }

    public function getTitle(): string
    {
        $entity = $this->getEntity();
        if ($entity === null) {
            return 'The entity has one or more empty necessary fields';
        }

        return sprintf('The %s entity has one or more empty necessary fields', $entity);
    }

    public function getParameters(): array
    {
        return [
            'entity' => $this->getEntity(),
            'sourceId' => $this->getSourceId(),
            'emptyField' => $this->emptyField,
        ];
    }

    public function getDescription(): string
    {
        $args = $this->getParameters();

        return sprintf(
            'The %s entity with the source id %s does not have the necessary data for the field(s): %s',
            $args['entity'],
            $args['sourceId'],
            $args['emptyField']
        );
    }

    public function getTitleSnippet(): string
    {
        return sprintf('%s.%s.title', $this->getSnippetRoot(), 'SWAG_MIGRATION__SHOPWARE_EMPTY_NECESSARY_DATA_FIELDS');
    }

    public function getDescriptionSnippet(): string
    {
        return sprintf('%s.%s.description', $this->getSnippetRoot(), 'SWAG_MIGRATION__SHOPWARE_EMPTY_NECESSARY_DATA_FIELDS');
    }
}
```

The important part here is the `getCode` method. It should not contain any details, otherwise, grouping won't work properly. Also, keep in mind to specify the English title and description in the respective `getTitle` and `getDescription` methods. Create corresponding snippets with the same content for both the `getTitleSnippet` and `getDescriptionSnippet` methods.

The English text is used in the international log file. Instead, snippets are used all over in the Administration to inform or guide the user. Parameters for the description should be returned by the `getParameters` method so the English description and snippets can both use them.

---

---

## Media Processing
**Source:** [products/extensions/migration-assistant/concept/media-processing.md](https://developer.shopware.com/docs/v6.6/products/extensions/migration-assistant/concept/media-processing.md)  
# Media Processing

Two steps are necessary to import files to Shopware 6 using the migration. First // todo10 , create a media file object  (`MediaDefinition` / `media` table, for more details, take a look at the `MediaConverter`) and create an entry in the `SwagMigrationMediaFileDefinition` / `swag_migration_media_file` table.

Every entry in the `swag_migration_media_file` table of the associated migration run will get processed by an implementation of `MediaFileProcessorInterface`. For the `api` gateway, the `HttpMediaDownloadService` is used and will download the files via HTTP.

To add a file to the table, you can do something like this in your `Converter` class (this example is from the `MediaConverter`):

```php
<?php declare(strict_types=1);

abstract class MediaConverter extends ShopwareConverter
{
    /* ... */

    public function convert(
        array $data,
        Context $context,
        MigrationContextInterface $migrationContext
    ): ConvertStruct {
        $this->generateChecksum($data);
        $this->context = $context;
        $this->locale = $data['_locale'];
        unset($data['_locale']);

        $connection = $migrationContext->getConnection();
        $this->connectionId = '';
        if ($connection !== null) {
            $this->connectionId = $connection->getId();
        }

        $converted = [];
        $this->mainMapping = $this->mappingService->getOrCreateMapping(
            $this->connectionId,
            DefaultEntities::MEDIA,
            $data['id'],
            $context,
            $this->checksum
        );
        $converted['id'] = $this->mainMapping['entityUuid'];

        if (!isset($data['name'])) {
            $data['name'] = $converted['id'];
        }

        $this->mediaFileService->saveMediaFile(
            [
                'runId' => $migrationContext->getRunUuid(),
                'entity' => MediaDataSet::getEntity(), // important to distinguish between private and public files
                'uri' => $data['uri'] ?? $data['path'],
                'fileName' => $data['name'], // uri or path to the file (because of the different implementations of the gateways)
                'fileSize' => (int) $data['file_size'],
                'mediaId' => $converted['id'], // uuid of the media object in Shopware 6
            ]
        );
        unset($data['uri'], $data['file_size']);

        $this->getMediaTranslation($converted, $data);
        $this->convertValue($converted, 'title', $data, 'name');
        $this->convertValue($converted, 'alt', $data, 'description');

        $albumMapping = $this->mappingService->getMapping(
            $this->connectionId,
            DefaultEntities::MEDIA_FOLDER,
            $data['albumID'],
            $this->context
        );

        if ($albumMapping !== null) {
            $converted['mediaFolderId'] = $albumMapping['entityUuid'];
            $this->mappingIds[] = $albumMapping['id'];
        }

        unset(
            $data['id'],
            $data['albumID'],

            // Legacy data that don't need mapping or there is no equivalent field
            $data['path'],
            $data['type'],
            $data['extension'],
            $data['file_size'],
            $data['width'],
            $data['height'],
            $data['userID'],
            $data['created']
        );

        $returnData = $data;
        if (empty($returnData)) {
            $returnData = null;
        }
        $this->updateMainMapping($migrationContext, $context);

        // The MediaWriter will write this Shopware 6 media object
        return new ConvertStruct($converted, $returnData, $this->mainMapping['id']);
    }

    /* ... */
}
```

`swag_migration_media_files` are processed by the right processor service. This service is different for documents and normal media, but it still is gateway dependent. For example, the `HttpMediaDownloadService` works like this:

```php
<?php declare(strict_types=1);

namespace SwagMigrationAssistant\Profile\Shopware55\Media;

/* ... */

class HttpMediaDownloadService implements MediaFileProcessorInterface
{
    /* ... */

    public function supports(MigrationContextInterface $migrationContext): bool
    {
        return $migrationContext->getProfile() instanceof ShopwareProfileInterface
            && $migrationContext->getGateway()->getName() === ShopwareApiGateway::GATEWAY_NAME
            && $migrationContext->getDataSet()::getEntity() === MediaDataSet::getEntity();
    }

    public function process(MigrationContextInterface $migrationContext, Context $context, array $workload, int $fileChunkByteSize): array
    {
        /* ... */

        //Fetch media from the database
        $media = $this->getMediaFiles($mediaIds, $runId, $context);

        $client = new Client([
            'verify' => false,
        ]);

        //Do download requests and store the promises
        $promises = $this->doMediaDownloadRequests($media, $mappedWorkload, $client);

        // Wait for the requests to complete, even if some of them fail
        /** @var array $results */
        $results = Promise\settle($promises)->wait();

        /* ... handle responses ... */

        $this->setProcessedFlag($runId, $context, $finishedUuids, $failureUuids);
        $this->loggingService->saveLogging($context);

        return array_values($mappedWorkload);
    }
}
```

First, the service fetches all media files associated with the given media IDs and downloads these media files from the source system. After this, it handles the response, saves the media files in a temporary folder and copies them to Shopware 6 filesystem. In the end, the service sets a `processed` status to these media files, saves all warnings that may have occurred and returns the status of the processed files.

---

---

## Migration Context
**Source:** [products/extensions/migration-assistant/concept/migration-context.md](https://developer.shopware.com/docs/v6.6/products/extensions/migration-assistant/concept/migration-context.md)  
# Migration Context

The central data structure of Shopware Migration Assistant is the migration context. The migration context contains the following information:

1. The current connection of migration which holds the credentials
2. Current Profile and Gateway instances
3. Identifier of the current run
4. Information on the current processing ([DataSet](dataselection-and-dataset))
5. Offset and limit of the current call

```php
<?php declare(strict_types=1);

namespace SwagMigrationAssistant\Migration;

use Shopware\Core\Framework\Struct\Struct;
use SwagMigrationAssistant\Migration\Connection\SwagMigrationConnectionEntity;
use SwagMigrationAssistant\Migration\DataSelection\DataSet\DataSet;
use SwagMigrationAssistant\Migration\Gateway\GatewayInterface;
use SwagMigrationAssistant\Migration\Profile\ProfileInterface;

class MigrationContext extends Struct implements MigrationContextInterface
{
    /* ... */

    public function getProfile(): ProfileInterface
    {
        return $this->profile;
    }

    public function getConnection(): ?SwagMigrationConnectionEntity
    {
        return $this->connection;
    }

    public function getRunUuid(): string
    {
        return $this->runUuid;
    }

    public function getDataSet(): ?DataSet
    {
        return $this->dataSet;
    }

    public function setDataSet(DataSet $dataSet): void
    {
        $this->dataSet = $dataSet;
    }

    public function getOffset(): int
    {
        return $this->offset;
    }

    public function getLimit(): int
    {
        return $this->limit;
    }

    public function getGateway(): GatewayInterface
    {
        return $this->gateway;
    }

    public function setGateway(GatewayInterface $gateway): void
    {
        $this->gateway = $gateway;
    }
}
```

---

---

## Premapping
**Source:** [products/extensions/migration-assistant/concept/premapping.md](https://developer.shopware.com/docs/v6.6/products/extensions/migration-assistant/concept/premapping.md)  
# Premapping

The premapping will use the normal [Mapping](convert-and-mapping#mapping) to store the old identifier with the equivalent new one. All premapping readers provide the information for the mapping choices and are registered like this:

```html
<service id="SwagMigrationAssistant\Profile\Shopware\Premapping\SalutationReader">
    <argument type="service" id="salutation.repository" />
    <argument type="service" id="SwagMigrationAssistant\Migration\Gateway\GatewayRegistry"/>
    <tag name="shopware.migration.pre_mapping_reader"/>
</service>
```

The service will return a `PremappingStruct`, which consists of:

1. Entity of the premapping
2. Choices, representing Shopware 6 equivalents
3. Mapping, representing the source system's structure, including a destination/choice

Here is an example of how the final `PremappingStruct` looks like in the `generate-premapping` json response:

```json
{
   "entity":"salutation",
   "choices":[
      {
         "uuid":"d4883ea9db2b4a5ca033873903358062",
         "description":"mr",
         "extensions":[

         ]
      },
      {
         "uuid":"7a7ef1e4a9064c46b5f85e28b4d942a9",
         "description":"mrs",
         "extensions":[

         ]
      },
      {
         "uuid":"a6fa00aef9a648d9bd012dbe16c112bf",
         "description":"not_specified",
         "extensions":[

         ]
      }
   ],
   "mapping":[
      {
         "sourceId":"mr",
         "description":"mr",
         "destinationUuid":"d4883ea9db2b4a5ca033873903358062",
         "extensions":[

         ]
      },
      {
         "sourceId":"ms",
         "description":"ms",
         "destinationUuid":"",
         "extensions":[

         ]
      }
   ]
}
```

The `destinationUuid` in the `mapping` array sets the destination for that entity. It will be saved along with the [Connection](profile-and-connection#connection), so the user does not have to make these decisions repeatedly. For more details on how the mapping process works and even more information on automatic assignment, look up more in the `SalutationReader` class.

To get the associated new identifier, you can make use of the `MappingService` similar to the `CustomerConverter`:

```php
<?php declare(strict_types=1);

/* ... */

protected function getSalutation(string $salutation): ?string
{
    $mapping = $this->mappingService->getMapping(
        $this->connectionId,
        SalutationReader::getMappingName(),
        $salutation,
        $this->context
    );

    if ($mapping === null) {
        $this->loggingService->addLogEntry(new UnknownEntityLog(
            $this->runId,
            DefaultEntities::SALUTATION,
            $salutation,
            DefaultEntities::CUSTOMER,
            $this->oldCustomerId
        ));

        return null;
    }
    $this->mappingIds[] = $mapping['id'];

    return $mapping['entityUuid'];
}

/* ... */
```

The `getMapping` method used in the mapping service looks up the `swag_migration_mapping` table for the combination of the old identifier and entity name stored in the current connection. Then it returns the mapping object containing the new Shopware 6 identifier. This identifier makes it possible to map your converted entity to your premapping choice. If `getMapping` returns null, then no valid mapping is available, and you have to log this with [LoggingService](logging). The mapping object has two keys: `id` and `entityUuid`. The `id` key is the identifier of the `swag_migration_mapping` entry and has to be inserted in the `mappingIds`, if the mapping should be preloaded. The `entityUuid` key is the UUID of the mapped entity.

---

---

## Profile and Connection
**Source:** [products/extensions/migration-assistant/concept/profile-and-connection.md](https://developer.shopware.com/docs/v6.6/products/extensions/migration-assistant/concept/profile-and-connection.md)  
# Profile and Connection

## Overview

Users of the plugin can create connections to different source systems. A connection is used to allow multiple migrations from the same source and update the right data (mapping). Connections require a specific profile indicating the type of source system. Users can, for example, create a connection to a Shopware shop using the Shopware 5.5 profile. Developers can create their own profiles from scratch, connect to different source systems, or just build and extend existing ones.

## Profile

The base of Shopware Migration Assistant is the profile, which enables you to migrate your shop system to Shopware 6. Shopware Migration Assistant comes with the default Shopware 5.5 profile and is located in the `shopware55.xml`:

```html
<!-- Shopware 5.5 Profile -->
<service id="SwagMigrationAssistant\Profile\Shopware55\Shopware55Profile">
    <tag name="shopware.migration.profile"/>
</service>
```

In order to identify itself, the profile has to implement getter functions like `getName`, which returns the unique name of the profile. The profile is used together with the [Gateway](gateway-and-reader#gateway) to check and apply the right processing during a migration run.

```php
<?php declare(strict_types=1);

namespace SwagMigrationAssistant\Profile\Shopware55;

use SwagMigrationAssistant\Profile\Shopware\ShopwareProfileInterface;

class Shopware55Profile implements ShopwareProfileInterface
{
    public const PROFILE_NAME = 'shopware55';

    public const SOURCE_SYSTEM_NAME = 'Shopware';

    public const SOURCE_SYSTEM_VERSION = '5.5';

    public const AUTHOR_NAME = 'shopware AG';

    public const ICON_PATH = '/swagmigrationassistant/static/img/migration-assistant-plugin.svg';

    public function getName(): string
    {
        return self::PROFILE_NAME;
    }

    public function getSourceSystemName(): string
    {
        return self::SOURCE_SYSTEM_NAME;
    }

    public function getVersion(): string
    {
        return self::SOURCE_SYSTEM_VERSION;
    }

    public function getAuthorName(): string
    {
        return self::AUTHOR_NAME;
    }

    public function getIconPath(): string
    {
        return self::ICON_PATH;
    }
}
```

## Connection

To connect Shopware 6 to your source system (e.g., Shopware 5), you will need a connection entity. The connection includes all the important information for your migration run. It contains the credentials for the API or database access, the actual [Premapping](premapping) and the profile, [Gateway](gateway-and-reader) combination which is used for your migration:

```php
<?php declare(strict_types=1);

namespace SwagMigrationAssistant\Migration\Connection;

/*...*/

class SwagMigrationConnectionDefinition extends EntityDefinition
{
    /*...*/

    protected function defineFields(): FieldCollection
    {
        return new FieldCollection([
             (new IdField('id', 'id'))->setFlags(new PrimaryKey(), new Required()),
             (new StringField('name', 'name'))->setFlags(new Required()),
             (new JsonField('credential_fields', 'credentialFields'))->setFlags(new WriteProtected(MigrationContext::SOURCE_CONTEXT)),
             new JsonField('premapping', 'premapping'),
             (new StringField('profile_name', 'profileName'))->setFlags(new Required()),
             (new StringField('gateway_name', 'gatewayName'))->setFlags(new Required()),
             new CreatedAtField(),
             new UpdatedAtField(),
             new OneToManyAssociationField('runs', SwagMigrationRunDefinition::class, 'connection_id'),
             new OneToManyAssociationField('mappings', SwagMigrationMappingDefinition::class, 'connection_id'),
             new OneToManyAssociationField('settings', GeneralSettingDefinition::class, 'selected_connection_id'),
        ]);
    }
}
```

---

---

## Writer
**Source:** [products/extensions/migration-assistant/concept/writer.md](https://developer.shopware.com/docs/v6.6/products/extensions/migration-assistant/concept/writer.md)  
# Writer

The `Writer` objects will get the converted data from the `swag_migration_data` table and write it to the right Shopware 6 table. Each `Writer` supports only one entity, which is most likely the target table.

When creating a writer, register it in a manner resembling the following:

```html
<service id="SwagMigrationAssistant\Migration\Writer\ProductWriter"
         parent="SwagMigrationAssistant\Migration\Writer\AbstractWriter">
    <argument type="service" id="Shopware\Core\Framework\DataAbstractionLayer\Write\EntityWriter"/>
    <argument type="service" id="Shopware\Core\Content\Product\ProductDefinition"/>
    <tag name="shopware.migration.writer"/>
</service>
```

In most cases, you should extend by the `AbstractWriter`, which does most things. You only need to specify the `supports` method.

```php
<?php declare(strict_types=1);

namespace SwagMigrationAssistant\Migration\Writer;

use SwagMigrationAssistant\Migration\DataSelection\DefaultEntities;

class ProductWriter extends AbstractWriter
{
    public function supports(): string
    {
        return DefaultEntities::PRODUCT;
    }
}
```

If you need more control over the writing, you can implement the `WriterInterface` by yourself and the class will receive the data in the `writeData` method. Received data is an array of converted values. The amount depends on the limit of the request. Error handling is already done in the overlying `MigrationDataWriter` class. If writing the entries fails with a `WriteException` from the DAL, it will try to exclude the reported failures and try again. If any other exception occurs, it will retry them one by one to minimize data loss.

---

---

## Guides
**Source:** [products/extensions/migration-assistant/guides.md](https://developer.shopware.com/docs/v6.6/products/extensions/migration-assistant/guides.md)  
# Guides

This section guides you on how to migrate from different environments by using a Migration Assistant converter, migration profile, or migration connector.

---

---

## Creating a New Migration Profile
**Source:** [products/extensions/migration-assistant/guides/creating-a-new-migration-profile.md](https://developer.shopware.com/docs/v6.6/products/extensions/migration-assistant/guides/creating-a-new-migration-profile.md)  
*(Body truncated in this bundle; follow the link for the rest.)*

# Creating a New Migration Profile

If you want to migrate your data from a different source system than Shopware, create a new migration profile for the Migration Assistant. But if you want to convert your plugin data from a Shopware system to Shopware 6, look at this article on [Extending a Shopware Migration Profile](extending-a-shopware-migration-profile).

## Setup

First, it is required that you already have installed the [Migration Assistant](https://github.com/shopware/SwagMigrationAssistant) plugin in Shopware 6 and have created a demo source system database with a `product` table. To create the table, use this SQL statement:

```sql
CREATE TABLE product
(
  id int PRIMARY KEY NOT NULL AUTO_INCREMENT,
  product_number varchar(255) NOT NULL,
  price float NOT NULL,
  stock int NOT NULL,
  product_name varchar(255) NOT NULL,
  tax float NOT NULL
);
```

This table should simulate a simple third-party source system, which should be migrated in the following steps.

## Creating a profile

In the first step, you have to create a new profile for your source system:

```php
<?php declare(strict_types=1);

namespace SwagMigrationOwnProfileExample;

use SwagMigrationAssistant\Migration\Profile\ProfileInterface;

class OwnProfile implements ProfileInterface
{
    public const PROFILE_NAME = 'ownProfile';

    public const SOURCE_SYSTEM_NAME = 'MySourceSystem';

    public const SOURCE_SYSTEM_VERSION = '1.0';

    public const AUTHOR_NAME = 'shopware AG';

    public const ICON_PATH = '/swagmigrationassistant/static/img/migration-assistant-plugin.svg';

    public function getName(): string
    {
        return self::PROFILE_NAME;
    }

    public function getSourceSystemName(): string
    {
        return self::SOURCE_SYSTEM_NAME;
    }

    public function getVersion(): string
    {
        return self::SOURCE_SYSTEM_VERSION;
    }

    public function getAuthorName(): string
    {
        return self::AUTHOR_NAME;
    }

    public function getIconPath(): string
    {
        return self::ICON_PATH;
    }
}
```

The profile itself does not contain any logic and is used to bundle the executing classes. To use this profile, you have to register and tag it in the `service.xml` with `shopware.migration.profile`:

```html
<service id="SwagMigrationOwnProfileExample\Profile\OwnProfile\OwnProfile">
    <tag name="shopware.migration.profile"/>
</service>
```

## Creating a gateway

Next, you have to create a new gateway which supports your profile:

```php
<?php declare(strict_types=1);

namespace SwagMigrationOwnProfileExample\Profile\OwnProfile\Gateway;

use Shopware\Core\Framework\Context;
use SwagMigrationAssistant\Migration\EnvironmentInformation;
use SwagMigrationAssistant\Migration\Gateway\GatewayInterface;
use SwagMigrationAssistant\Migration\Gateway\Reader\ReaderRegistry;
use SwagMigrationAssistant\Migration\MigrationContextInterface;
use SwagMigrationAssistant\Migration\RequestStatusStruct;
use SwagMigrationAssistant\Profile\Shopware\Exception\DatabaseConnectionException;
use SwagMigrationAssistant\Profile\Shopware\Gateway\Connection\ConnectionFactoryInterface;
use SwagMigrationOwnProfileExample\Profile\OwnProfile\OwnProfile;

class OwnLocaleGateway implements GatewayInterface
{
    public const GATEWAY_NAME = 'local';

    private ConnectionFactoryInterface $connectionFactory;

    private ReaderRegistry $readerRegistry;

    public function __construct(
        ReaderRegistry $readerRegistry,
        ConnectionFactoryInterface $connectionFactory
    ) {
        $this->readerRegistry = $readerRegistry;
        $this->connectionFactory = $connectionFactory;
    }

    public function getName(): string
    {
        return self::GATEWAY_NAME;
    }

    public function supports(MigrationContextInterface $migrationContext): bool
    {
        return $migrationContext->getProfile() instanceof OwnProfile;
    }

    public function getSnippetName(): string
    {
        return 'swag-migration.wizard.pages.connectionCreate.gateways.shopwareLocal';
    }

    /**
     * Reads the given entity type from via context from its connection and returns the data
     */
    public function read(MigrationContextInterface $migrationContext): array
    {
        // TODO: Implement read() method.
        return [];
    }

    public function readEnvironmentInformation(
        MigrationContextInterface $migrationContext,
        Context $context
    ): EnvironmentInformation {
        $connection = $this->connectionFactory->createDatabaseConnection($migrationContext);
        $profile = $migrationContext->getProfile();

        try {
            $connection->connect();
        } catch (\Exception $e) {
            $error = new DatabaseConnectionException();

            return new EnvironmentInformation(
                $profile->getSourceSystemName(),
                $profile->getVersion(),
                '-',
                [],
                [],
                new RequestStatusStruct($error->getErrorCode(), $error->getMessage())
            );
        }
        $connection->close();

        $totals = $this->readTotals($migrationContext, $context);

        return new EnvironmentInformation(
            $profile->getSourceSystemName(),
            $profile->getVersion(),
            'Example Host Name',
            $totals,
            [],
            new RequestStatusStruct(),
            false
        );
    }

    public function readTotals(MigrationContextInterface $migrationContext, Context $context): array
    {
        $readers = $this->readerRegistry->getReaderForTotal($migrationContext);

        $totals = [];
        foreach ($readers as $reader) {
            $total = $reader->readTotal($migrationContext);

            if ($total === null) {
                continue;
            }

            $totals[$total->getEntityName()] = $total;
        }

        return $totals;
    }
}
```

As you have seen above, the gateway uses the `ConnectionFactory` to test the connection to the source system. You can also implement your own way to check this, but using this factory is the simplest way for a gateway to connect to a local database. Like the profile, you have to register the new gateway in the `service.xml` and tag it with `shopware.migration.gateway`:

```html
<service id="SwagMigrationOwnProfileExample\Profile\OwnProfile\Gateway\OwnLocaleGateway">
    <argument type="service" id="SwagMigrationAssistant\Migration\Gateway\Reader\ReaderRegistry"/>
    <argument type="service" id="SwagMigrationAssistant\Profile\Shopware\Gateway\Connection\ConnectionFactory"/>
    <tag name="shopware.migration.gateway"/>
</service>
```

## Creating a credentials page

If you want to try your current progress in the Administration, you can select the profile and gateway in the migration wizard. If you try to go to the next page, there will be an error message because no credentials page was found. To create a new credentials page, you have to add an `index.js` for your new component into `Resources/app/administration/src/own-profile/profile`:

```javascript
import { Component } from 'src/core/shopware';
import template from './swag-migration-profile-ownProfile-local-credential-form.html.twig';

Component.register('swag-migration-profile-ownProfile-local-credential-form', {
    template,

    props: {
        credentials: {
            type: Object,
            default() {
                return {};
            }
        }
    },

    data() {
        return {
            inputCredentials: {
                dbHost: '',
                dbPort: '3306',
                dbUser: '',
                dbPassword: '',
                dbName: ''
            }
        };
    },

    watch: {
        credentials: {
            immediate: true,
            handler(newCredentials) {
                if (newCredentials === null) {
                    this.emitCredentials(this.inputCredentials);
                    return;
                }

                this.inputCredentials = newCredentials;
                this.emitOnChildRouteReadyChanged(
                    this.areCredentialsValid(this.inputCredentials)
                );
            }
        },

        inputCredentials: {
            deep: true,
            handler(newInputCredentials) {
                this.emitCredentials(newInputCredentials);
            }
        }
    },

    methods: {
        areCredentialsValid(newInputCredentials) {
            return (newInputCredentials.dbHost !== '' &&
                newInputCredentials.dbPort !== '' &&
                newInputCredentials.dbName !== '' &&
                newInputCredentials.dbUser !== '' &&
                newInputCredentials.dbPassword !== ''
            );
        },

        emitOnChildRouteReadyChanged(isReady) {
            this.$emit('onChildRouteReadyChanged', isReady);
        },

        emitCredentials(newInputCredentials) {
            this.$emit('onCredentialsChanged', newInputCredentials);
            this.emitOnChildRouteReadyChanged(
                this.areCredentialsValid(newInputCredentials)
            );
        },

        onKeyPressEnter() {
            this.$emit('onTriggerPrimaryClick');
        }
    }
});
```

As you can see above, currently, the template does not exist and you have to create this file: `swag-migration-profile-ownProfile-local-credential-form.html.twig`

```html
{% block own_profile_page_credentials %}
    <div class="swag-migration-wizard swag-migration-wizard-page-credentials"
         @keypress.enter="onKeyPressEnter">
        {% block own_profile_page_credentials_content %}
            <div class="swag-migration-wizard__content">
                {% block own_profile_page_credentials_information %}
                    <div class="swag-migration-wizard__content-information">
                        {% block own_profile_page_credentials_local_hint %}
                            {{ $tc('swag-migration.wizard.pages.credentials.shopware55.local.contentInformation') }}
                        {% endblock %}
                    </div>
                {% endblock %}

                {% block own_profile_page_credentials_credentials %}
                    <div class="swag-migration-wizard__form">
                        {% block own_profile_page_credentials_local_db_host_port_group %}
                            <sw-container columns="1fr 80px"
                                          gap="16px">
                                {% block own_profile_page_credentials_local_dbhost_field %}
                                    <sw-text-field v-autofocus
                                                   name="sw-field--dbHost"
                                                   :label="$tc('swag-migration.wizard.pages.credentials.shopware55.local.dbHostLabel')"
                                                   :placeholder="$tc('swag-migration.wizard.pages.credentials.shopware55.local.dbHostPlaceholder')"
                                                   v-model="inputCredentials.dbHost">
                                    </sw-text-field>
                                {% endblock %}

                                {% block own_profile_page_credentials_local_dbport_field %}
                                    <sw-field name="sw-field--dbPort"
                                              :label="$tc('swag-migration.wizard.pages.credentials.shopware55.local.dbPortLabel')"
                                              v-model="inputCredentials.dbPort">
                                    </sw-field>
                                {% endblock %}
                            </sw-container>
                        {% endblock %}

                        {% block own_profile_page_credentials_local_dbuser_field %}
                            <sw-field name="sw-field--dbUser"
                                      :label="$tc('swag-migration.wizard.pages.credentials.shopware55.local.dbUserLabel')"
                                      :placeholder="$tc('

… **Truncated.** Full document: https://developer.shopware.com/docs/v6.6/products/extensions/migration-assistant/guides/creating-a-new-migration-profile.md


---

## Decorating a Shopware Migration Assistant Converter
**Source:** [products/extensions/migration-assistant/guides/decorating-a-shopware-migration-assistant-converter.md](https://developer.shopware.com/docs/v6.6/products/extensions/migration-assistant/guides/decorating-a-shopware-migration-assistant-converter.md)  
*(Body truncated in this bundle; follow the link for the rest.)*

# Decorating a Shopware Migration Assistant Converter

## Overview

In this guide, you will learn how to decorate a Shopware migration converter of the [Migration Connector](https://github.com/shopware/SwagMigrationConnector) plugin. Here, the decorated converter will modify the converted products and get data out of a `premapping field`.

## Setup

It is required to have installed the [Migration Assistant](https://github.com/shopware/SwagMigrationAssistant) plugin in Shopware 6 and have a running Shopware 5 system running to connect the Migration Assistant via API or local gateway.

## Enrich existing plugin with migration features

Instead of creating a new plugin for the migration, you might want to add migration features to your existing plugin. Of course, your plugin should then also be installable without the Migration Assistant plugin. So we have an optional requirement. Have a look at this \[PLACEHOLDER-LINK: Optional requirements of a plugin] on how to inject the needed migration services only if the Migration Assistant plugin is available. You could also have a look at the example plugin to see how the conditional loading is managed in the plugin base class.

## Creating a premapping reader

In this example, the user should be able to map the manufacturer while no new manufacturer will be created. You have to create a new premapping reader to achieve this:

```php
<?php declare(strict_types=1);

namespace SwagMigrationExtendConverterExample\Profile\Shopware\Premapping;

use Shopware\Core\Content\Product\Aggregate\ProductManufacturer\ProductManufacturerEntity;
use Shopware\Core\Framework\Context;
use Shopware\Core\Framework\DataAbstractionLayer\EntityRepository;
use Shopware\Core\Framework\DataAbstractionLayer\Search\Criteria;
use Shopware\Core\Framework\DataAbstractionLayer\Search\Sorting\FieldSorting;
use SwagMigrationAssistant\Migration\Gateway\GatewayRegistryInterface;
use SwagMigrationAssistant\Migration\MigrationContextInterface;
use SwagMigrationAssistant\Migration\Premapping\AbstractPremappingReader;
use SwagMigrationAssistant\Migration\Premapping\PremappingChoiceStruct;
use SwagMigrationAssistant\Migration\Premapping\PremappingEntityStruct;
use SwagMigrationAssistant\Migration\Premapping\PremappingStruct;
use SwagMigrationAssistant\Profile\Shopware\DataSelection\ProductDataSelection;
use SwagMigrationAssistant\Profile\Shopware\Gateway\ShopwareGatewayInterface;
use SwagMigrationAssistant\Profile\Shopware\ShopwareProfileInterface;

class ManufacturerReader extends AbstractPremappingReader
{
    private const MAPPING_NAME = 'swag_manufacturer';

    private EntityRepository $manufacturerRepo;

    private GatewayRegistryInterface $gatewayRegistry;

    private array $preselectionDictionary;

    private array $preselectionSourceNameDictionary;

    public function __construct(
        EntityRepository $manufacturerRepo,
        GatewayRegistryInterface $gatewayRegistry
    ) {
        $this->manufacturerRepo = $manufacturerRepo;
        $this->gatewayRegistry = $gatewayRegistry;
    }

    public static function getMappingName(): string
    {
        return self::MAPPING_NAME;
    }

    /**
     * Checks whether or not the current profile and DataSelection is supported
     */
    public function supports(MigrationContextInterface $migrationContext, array $entityGroupNames): bool
    {
        return $migrationContext->getProfile() instanceof ShopwareProfileInterface
            && in_array(ProductDataSelection::IDENTIFIER, $entityGroupNames, true);
    }

    public function getPremapping(Context $context, MigrationContextInterface $migrationContext): PremappingStruct
    {
        $this->fillConnectionPremappingDictionary($migrationContext);
        $mapping = $this->getMapping($migrationContext);
        $choices = $this->getChoices($context);
        $this->setPreselection($mapping);

        return new PremappingStruct(self::getMappingName(), $mapping, $choices);
    }

    /**
     * Reads all manufacturers of the source system, looks into connectionPremappingDictionary if a premapping
     * is currently set and returns the filled mapping array
     *
     * @return PremappingEntityStruct[]
     */
    private function getMapping(MigrationContextInterface $migrationContext): array
    {
        /** @var ShopwareGatewayInterface $gateway */
        $gateway = $this->gatewayRegistry->getGateway($migrationContext);

        $preMappingData = $gateway->readTable($migrationContext, 's_articles_supplier');

        $entityData = [];
        foreach ($preMappingData as $data) {
            $this->preselectionSourceNameDictionary[$data['id']] = $data['name'];

            $uuid = '';
            if (isset($this->connectionPremappingDictionary[$data['id']])) {
                $uuid = $this->connectionPremappingDictionary[$data['id']]['destinationUuid'];
            }

            $entityData[] = new PremappingEntityStruct($data['id'], $data['name'], $uuid);
        }

        return $entityData;
    }

    /**
     * Returns all choices of the manufacturer repository
     *
     * @return PremappingChoiceStruct[]
     */
    private function getChoices(Context $context): array
    {
        $criteria = new Criteria();
        $criteria->addSorting(new FieldSorting('name'));

        /** @var ProductManufacturerEntity[] $manufacturers */
        $manufacturers = $this->manufacturerRepo->search($criteria, $context);

        $choices = [];
        foreach ($manufacturers as $manufacturer) {
            $this->preselectionDictionary[$manufacturer->getName()] = $manufacturer->getId();
            $choices[] = new PremappingChoiceStruct($manufacturer->getId(), $manufacturer->getName());
        }

        return $choices;
    }

    /**
     * Loops through mapping and sets preselection, if uuid is currently not set
     *
     * @param PremappingEntityStruct[] $mapping
     */
    private function setPreselection(array $mapping): void
    {
        foreach ($mapping as $item) {
            if (!isset($this->preselectionSourceNameDictionary[$item->getSourceId()]) || $item->getDestinationUuid() !== '') {
                continue;
            }

            $sourceName = $this->preselectionSourceNameDictionary[$item->getSourceId()];
            $preselectionValue = $this->getPreselectionValue($sourceName);

            if ($preselectionValue !== null) {
                $item->setDestinationUuid($preselectionValue);
            }
        }
    }

    /**
     * Only a simple example on how to implement a preselection
     */
    private function getPreselectionValue(string $sourceName): ?string
    {
        $preselectionValue = null;
        $validPreselection = 'Shopware';
        $choice = 'shopware AG';

        if ($sourceName === $validPreselection && isset($this->preselectionDictionary[$choice])) {
            $preselectionValue = $this->preselectionDictionary[$choice];
        }

        return $preselectionValue;
    }
}
```

The created premapping reader fetches all manufacturers of the source system, gets all manufacturer choices out of the Shopware 6 database, and does a simple preselection via the manufacturer name. The `getPremapping` function returns the whole premapping structure. With this structure, the Administration creates a new premapping card and creates for each source system manufacturer a selectbox with all Shopware 6 manufacturers as choices. For more details, have a look at the [Premapping concept](../concept/premapping).

## Adding snippets to premapping card

Currently, the premapping card has no snippets at all, so you have to create a new snippet file for the title:

```json
{
     "swag-migration": {
         "index": {
             "premappingCard": {
                 "group": {
                     "swag_manufacturer": "Manufacturer"
                 }
             }
         }
     }
 }
```

This file has to be located in `Resources\administration\snippet` and registered in `Resources\administration\main.js` of the plugin like this:

```javascript
import enGBSnippets from './snippet/en-GB.json';

const { Application } = Shopware;

Application.addInitializerDecorator('locale', (localeFactory) => {
    localeFactory.extend('en-GB', enGBSnippets);

     return localeFactory;
});
```

Now your new premapping card has a correct title.

## Decorate the product migration converter

After creating your premapping reader, you have a new premapping card, but this premapping is currently not in use. To map the product manufacturers of the source system to your premapping values, you have to decorate one of the Shopware product migration converters. In this example, only the `Shopware55ProductConverter` is decorated, but if you want to decorate all Shopware migration converters, you have to do the same:

```php
 <?php declare(strict_types=1);

 namespace SwagMigrationExtendConverterExample\Profile\Shopware\Converter;

 use Shopware\Core\Framework\Context;
 use SwagMigrationAssistant\Migration\Converter\ConverterInterface;
 use SwagMigrationAssistant\Migration\Converter\ConvertStruct;
 use SwagMigrationAssistant\Migration\Logging\LoggingServiceInterface;
 use SwagMigrationAssistant\Migration\Mapping\MappingServiceInterface;
 use SwagMigrationAssistant\Migration\Media\MediaFileServiceInterface;
 use SwagMigrationAssistant\Migration\MigrationContextInterface;
 use SwagMigrationAssistant\Profile\Shopware\Converter\ProductConverter;
 use SwagMigrationExtendConverterExample\Profile\Shopware\Premapping\ManufacturerReader;

 class Shopware55DecoratedProductConverter extends ProductConverter
 {
     private ConverterInterface $originalProductConverter;

     public function __construct(
         ConverterInterface $originalProductConverter,
         MappingServiceInterface $mappingService,
         LoggingServiceInterface $loggingService,
         MediaFileServiceInterface $mediaFileService
     ) {
         parent::__construct($mappingService, $loggingService, $mediaFileService);
         $this->originalProductConverter = $originalProductConverter;
     }

     public function supports(MigrationContextInterface $migrationContext): bool
     {
         return $this->originalProductConverter->supports($migrationContext);
     }

     public function getSourceIdentifier(array $data): string
     {
         return $this->originalProductConverter->getSourceIdentifier($data);
     }

     public function getMediaUuids(array $converted): ?array
     {
         return $this->originalProductConverter->getMediaUuids($converted);
     }

     public function writeMapping(Context $context): void
     {
         $this->originalProductConverter->writeMapping($context);
     }

     public function convert(
         array $data,
         Context $context,
         MigrationContextInterface $migrationContext
     ): ConvertStruct
     {
         if (!isset($data['manufacturer']['id'])) {
             return $this->originalProductConverter->convert($data, $context, $migrationContext);
         }

         $manufacturerId = $data['manufacturer']['id'];
         unset($data['manufacturer']);

         $mapping = $this->mappingService->getMapping(
             $migrationContext->getConnection()->getId(),
             ManufacturerReader::getMappingName(),
             $manufacturerId,
             $context
         );

         $convertedStruct = $this->originalProductConverter->convert($data, $context, $migrationContext);

         if ($mapping === null) {
             return $convertedStruct;
         }

         $converted = $convertedStruct->getConverted();
         $converted['manufacturerId'] = $mapping['entityUuid'];

         return new ConvertStruct($converted, $convertedStruct->getUnmapped(), $convertedStruct->getMappingUuid());
     }
 }
```

Your new decorated product migration converter checks if a manufacturer is set and searches for the premapping via the `MappingService`. If a premapping is found, the migration converter uses the converted value of the 

… **Truncated.** Full document: https://developer.shopware.com/docs/v6.6/products/extensions/migration-assistant/guides/decorating-a-shopware-migration-assistant-converter.md


---

## Extending a Shopware Migration Profile
**Source:** [products/extensions/migration-assistant/guides/extending-a-shopware-migration-profile.md](https://developer.shopware.com/docs/v6.6/products/extensions/migration-assistant/guides/extending-a-shopware-migration-profile.md)  
*(Body truncated in this bundle; follow the link for the rest.)*

# Extending a Shopware Migration Profile

## Overview

In this guide, you will see an example of how you can extend a Shopware migration profile of the [Shopware Migration Assistant](https://store.shopware.com/de/swag257162657297f/migrations-assistent.html). For this example, the Shopware 5 [SwagAdvDevBundle](https://github.com/shopwareLabs/SwagAdvDevBundle) plugin is migrated to the Shopware 6. For simplicity, only the local gateway is implemented.

## Setup

It is required to have a basic plugin running. You must have installed the [SwagAdvDevBundle](https://github.com/shopwareLabs/SwagAdvDevBundle) plugin in Shopware 5, an own [Plugin](../../../../guides/plugins/plugins/plugin-base-guide#create-your-first-plugin) and [Shopware Migration Assistant](https://store.shopware.com/de/swag257162657297f/migrations-assistent.html) in Shopware 6.

## Enrich existing plugin with migration features

Instead of creating a new plugin for the migration, you might want to add migration features to your existing plugin. Of course, your plugin should then also be installable without the Migration Assistant plugin. So we have an optional requirement. Have a look at this [section of the guide](../../../../guides/plugins/plugins/plugin-fundamentals/database-migrations) on how to inject the needed migration services only if the Migration Assistant plugin is available. You could also have a look at the example plugin to see how the conditional loading is managed in the plugin base class.

## Creating a new dataSet

First of all, you need to create a new `DataSet` for your bundle entity:

```php
<?php declare(strict_types=1);

namespace SwagMigrationBundleExample\Profile\Shopware\DataSelection\DataSet;

use SwagMigrationAssistant\Migration\DataSelection\DataSet\DataSet;
use SwagMigrationAssistant\Migration\MigrationContextInterface;
use SwagMigrationAssistant\Profile\Shopware\ShopwareProfileInterface;

class BundleDataSet extends DataSet
{
    public static function getEntity(): string
    {
        return 'swag_bundle'; // Identifier of this entity
    }

    public function supports(MigrationContextInterface $migrationContext): bool
    {
        // This way we support all Shopware profile versions
        return $migrationContext->getProfile() instanceof ShopwareProfileInterface;
    }

    public function getSnippet(): string
    {
        return 'swag-migration.index.selectDataCard.entities.' . static::getEntity();
    }
}
```

The bundle entities must be migrated after the products, because of which you have to extend the `ProductDataSelection` as follows:

```php
<?php declare(strict_types=1);

namespace SwagMigrationBundleExample\Profile\Shopware\DataSelection;

use SwagMigrationAssistant\Migration\DataSelection\DataSelectionInterface;
use SwagMigrationAssistant\Migration\DataSelection\DataSelectionStruct;
use SwagMigrationAssistant\Migration\MigrationContextInterface;
use SwagMigrationBundleExample\Profile\Shopware\DataSelection\DataSet\BundleDataSet;
use SwagMigrationOwnProfileExample\Profile\OwnProfile\DataSelection\DataSet\ProductDataSet;

class ProductDataSelection implements DataSelectionInterface
{
    private DataSelectionInterface $originalDataSelection;

    public function __construct(DataSelectionInterface $originalDataSelection)
    {
        $this->originalDataSelection = $originalDataSelection;
    }

    public function supports(MigrationContextInterface $migrationContext): bool
    {
        return $this->originalDataSelection->supports($migrationContext);
    }

    public function getData(): DataSelectionStruct
    {
        $dataSelection = $this->originalDataSelection->getData();

        // Add the modified DataSet array to a new DataSelectionStruct
        return new DataSelectionStruct(
            $dataSelection->getId(),
            $this->getDataSets(),
            $this->getDataSetsRequiredForCount(),
            $dataSelection->getSnippet(),
            $dataSelection->getPosition(),
            $dataSelection->getProcessMediaFiles(),
            DataSelectionStruct::PLUGIN_DATA_TYPE
        );
    }

    public function getDataSets(): array
    {
        $entities = $this->originalDataSelection->getDataSets();
        $entities[] = new BundleDataSet(); // Add the BundleDataSet to the DataSet array

        return $entities;
    }

    public function getDataSetsRequiredForCount(): array
    {
        return $this->originalDataSelection->getDataSetsRequiredForCount();
    }
}
```

To insert the bundle entity to this `DataSelection`, you have to add this entity to the entities array of the returning `DataSelectionStruct` of the `getData` function.

Both classes have to be registered in the `migration_assistant_extension.xml`:

```html
<service id="SwagMigrationBundleExample\Profile\Shopware\DataSelection\ProductDataSelection"
         decorates="SwagMigrationAssistant\Profile\Shopware\DataSelection\ProductDataSelection">
    <argument type="service" id="SwagMigrationBundleExample\Profile\Shopware\DataSelection\ProductDataSelection.inner"/>
</service>

<service id="SwagMigrationBundleExample\Profile\Shopware\DataSelection\DataSet\BundleDataSet">
    <tag name="shopware.migration.data_set"/>
</service>
```

All `DataSets` have to be tagged with `shopware.migration.data_set`. The `DataSetRegistry` fetches all these classes and searches for the correct `DataSet` with the `supports` method.

## Adding entity count snippets

If you check your current progress in the data selection table of Shopware Migration Assistant in the Administration, you can see that the bundle entities are automatically counted, but the description of the entity count is currently not loaded. To get a correct description of the new entity count, you have to add new snippets for this.

First of all, you create a new snippet file, e.g., `en-GB.json`:

```json
{
    "swag-migration": {
        "index": {
            "selectDataCard": {
                "entities": {
                    "swag_bundle": "Bundles:"
                }
            }
        }
    }
}
```

All count entity descriptions are located in the `swag-migration.index.selectDataCard.entities` namespace by default, so you have to create a new entry with the entity name of the new bundle entity or you could change the snippet in the `getSnippet` function of the `DataSet`.

At last, you have to create the `main.js` in the `Resources/app/administration` directory like this:

```javascript
import enGBSnippets from './snippet/en-GB.json';

const { Application } = Shopware;

Application.addInitializerDecorator('locale', (localeFactory) => {
    localeFactory.extend('en-GB', enGBSnippets);

    return localeFactory;
});
```

As you see in the code above, you register your snippet file for the `en-GB` locale. Now the count entity description should display in the Administration correctly.

## Creating a local reader

```php
<?php declare(strict_types=1);

namespace SwagMigrationBundleExample\Profile\Shopware\Gateway\Local\Reader;

use Doctrine\DBAL\Connection;
use Doctrine\DBAL\Driver\ResultStatement;
use SwagMigrationAssistant\Migration\MigrationContextInterface;
use SwagMigrationAssistant\Migration\TotalStruct;
use SwagMigrationAssistant\Profile\Shopware\Gateway\Local\Reader\AbstractReader;
use SwagMigrationAssistant\Profile\Shopware\Gateway\Local\ShopwareLocalGateway;
use SwagMigrationAssistant\Profile\Shopware\ShopwareProfileInterface;
use SwagMigrationBundleExample\Profile\Shopware\DataSelection\DataSet\BundleDataSet;

class LocalBundleReader extends AbstractReader
{
    public function supportsTotal(MigrationContextInterface $migrationContext): bool
    {
        return $migrationContext->getProfile() instanceof ShopwareProfileInterface
            && $migrationContext->getGateway()->getName() === ShopwareLocalGateway::GATEWAY_NAME;
    }

    public function readTotal(MigrationContextInterface $migrationContext): ?TotalStruct
    {
        $this->setConnection($migrationContext);

        $query = $this->connection->createQueryBuilder()
            ->select('COUNT(*)')
            ->from('s_bundles')
            ->execute();

        $total = 0;
        if ($query instanceof ResultStatement) {
            $total = (int) $query->fetchColumn();
        }

        return new TotalStruct(BundleDataSet::getEntity(), $total);
    }

    public function supports(MigrationContextInterface $migrationContext): bool
    {
        // Make sure that this reader is only called for the BundleDataSet entity
        return $migrationContext->getProfile() instanceof ShopwareProfileInterface
            && $migrationContext->getGateway()->getName() === ShopwareLocalGateway::GATEWAY_NAME
            && $migrationContext->getDataSet()::getEntity() === BundleDataSet::getEntity();
    }

    /**
     * Read all bundles with associated product data
     */
    public function read(MigrationContextInterface $migrationContext, array $params = []): array
    {
        $this->setConnection($migrationContext);

        // Fetch the ids of the given table with the given offset and limit
        $ids = $this->fetchIdentifiers('s_bundles', $migrationContext->getOffset(), $migrationContext->getLimit());

        // Strip the table prefix 'bundles' out of the bundles array 
        $bundles = $this->mapData($this->fetchBundles($ids), [], ['bundles']);
        $bundleProducts = $this->fetchBundleProducts($ids);

        foreach ($bundles as &$bundle) {
            if (isset($bundleProducts[$bundle['id']])) {
                $bundle['products'] = $bundleProducts[$bundle['id']];
            }
        }

        return $bundles;
    }

    /**
     * Fetch all bundles by given ids
     */
    private function fetchBundles(array $ids): array
    {
        $query = $this->connection->createQueryBuilder();

        $query->from('s_bundles', 'bundles');
        $this->addTableSelection($query, 's_bundles', 'bundles');

        $query->where('bundles.id IN (:ids)');
        $query->setParameter('ids', $ids, Connection::PARAM_STR_ARRAY);

        $query->addOrderBy('bundles.id');

        return $query->execute()->fetchAll();
    }

    /**
     * Fetch all bundle products by bundle ids
     */
    private function fetchBundleProducts(array $ids): array
    {
        $query = $this->connection->createQueryBuilder();

        $query->from('s_bundle_products', 'bundleProducts');
        $this->addTableSelection($query, 's_bundle_products', 'bundleProducts');

        $query->where('bundleProducts.bundle_id IN (:ids)');
        $query->setParameter('ids', $ids, Connection::PARAM_INT_ARRAY);

        return $query->execute()->fetchAll(\PDO::FETCH_GROUP | \PDO::FETCH_COLUMN);
    }
}
```

In this local reader, you fetch all bundles with associated products and return this in the `read` method. Like the `DataSelection` and `DataSet`, you must register the local reader and tag it with `shopware.migration.reader` in your `migration_assistant_extension.xml`. Also, you have to set the parent property of your local reader to `AbstractReader` to inherit from this class:

```html
<service id="SwagMigrationBundleExample\Profile\Shopware\Gateway\Local\Reader\LocalBundleReader"
         parent="SwagMigrationAssistant\Profile\Shopware\Gateway\Local\Reader\AbstractReader">
    <tag name="shopware.migration.reader"/>
</service>
```

## Creating a converter

```php
<?php declare(strict_types=1);

namespace SwagMigrationBundleExample\Profile\Shopware\Converter;

use Shopware\Core\Framework\Context;
use SwagMigrationAssistant\Migration\Converter\ConvertStruct;
use SwagMigrationAssistant\Migration\DataSelection\DefaultEntities;
use SwagMigrationAssistant\Migration\MigrationContextInterface;
use SwagMigrationAssistant\Profile\Shopware\Converter\ShopwareConverter;
use SwagMigrationAssistant\Profile\Shopware\ShopwareProfileInterface;
use SwagMigrationBundleExample\Profile\Shopware\DataSelection\DataSet\BundleDataSet;

class BundleConverter extends ShopwareConverter
{
    public function supports

… **Truncated.** Full document: https://developer.shopware.com/docs/v6.6/products/extensions/migration-assistant/guides/extending-a-shopware-migration-profile.md


---

## Extending the Migration Connector
**Source:** [products/extensions/migration-assistant/guides/extending-the-migration-connector.md](https://developer.shopware.com/docs/v6.6/products/extensions/migration-assistant/guides/extending-the-migration-connector.md)  
# Extending the Migration Connector

In this guide, you will see an example of how you can extend the [Migration connector](https://github.com/shopware/SwagMigrationConnector) plugin to migrate the Shopware 5 [SwagAdvDevBundle](https://github.com/shopwareLabs/SwagAdvDevBundle) to a Shopware 6 plugin via API.

## Setup

It is required to have a basic Shopware 5 plugin running. You must have installed the [SwagAdvDevBundle](https://github.com/shopwareLabs/SwagAdvDevBundle), the [Migration connector](https://github.com/shopware/SwagMigrationConnector) plugin in Shopware 5, and an own Shopware 6 [Plugin](../../../../guides/plugins/plugins/plugin-base-guide#create-your-first-plugin), the [Migration Assistant](https://github.com/shopware/SwagMigrationAssistant) and the [SwagMigrationBundleExample](extending-a-shopware-migration-profile) plugin in Shopware 6. If you want to know how all plugins work together, please look at the [Extending a Shopware Migration Profile](extending-a-shopware-migration-profile) guide.

With this setup, you have the bundle plugin in Shopware 5 and also the bundle plugin in Shopware 6. So you can migrate your Shopware 5 shop to Shopware 6 via local and API gateway, but your bundle data only via a local gateway.

## Creating bundle repository

To fetch your data via the Shopware 5 API, you have to create a bundle repository first:

```php
<?php

namespace SwagMigrationBundleApiExample\Repository;

use Doctrine\DBAL\Connection;
use SwagMigrationConnector\Repository\AbstractRepository;

class BundleRepository extends AbstractRepository
{
    /**
     * Fetch bundles using offset and limit
     *
     * @param int $offset
     * @param int $limit
     *
     * @return array
     */
    public function fetch($offset = 0, $limit = 250)
    {
        $ids = $this->fetchIdentifiers('s_bundles', $offset, $limit);

        $query = $this->connection->createQueryBuilder();

        $query->from('s_bundles', 'bundles');
        $this->addTableSelection($query, 's_bundles', 'bundles');

        $query->where('bundles.id IN (:ids)');
        $query->setParameter('ids', $ids, Connection::PARAM_STR_ARRAY);

        $query->addOrderBy('bundles.id');

        return $query->execute()->fetchAll();
    }

    /**
     * Fetch all bundle products by bundle ids
     *
     * @param array $ids
     *
     * @return array
     */
    public function fetchBundleProducts(array $ids)
    {
        $query = $this->connection->createQueryBuilder();

        $query->from('s_bundle_products', 'bundleProducts');
        $this->addTableSelection($query, 's_bundle_products', 'bundleProducts');

        $query->where('bundleProducts.bundle_id IN (:ids)');
        $query->setParameter('ids', $ids, Connection::PARAM_INT_ARRAY);

        return $query->execute()->fetchAll(\PDO::FETCH_GROUP | \PDO::FETCH_COLUMN);
    }
}
```

The repository has to inherit from the `AbstractRepository` of the Migration Connector. This provides helper functions like `addTableSelection`, which sets a prefix to all table columns and adds these to the query builder.

You have to register the repository in your `service.xml` with the parent property like this:

```html
<service id="swag_migration_bundle_api_example.bundle_repository"
         class="SwagMigrationBundleApiExample\Repository\BundleRepository"
         parent="SwagMigrationConnector\Repository\AbstractRepository"
         />
```

## Creating bundle service

In the next step, you create a new `BundleService`, which uses your new `BundleRepository` to fetch all bundles and products to map them to one result array:

```php
<?php
/**
 * (c) shopware AG <info@shopware.com>
 * For the full copyright and license information, please view the LICENSE
 * File that was distributed with this source code.
 */

namespace SwagMigrationBundleApiExample\Service;

use SwagMigrationBundleApiExample\Repository\BundleRepository;
use SwagMigrationConnector\Repository\ApiRepositoryInterface;
use SwagMigrationConnector\Service\AbstractApiService;

class BundleService extends AbstractApiService
{
    private BundleRepository $bundleRepository;

    /**
     * @param ApiRepositoryInterface $bundleRepository
     */
    public function __construct(ApiRepositoryInterface $bundleRepository)
    {
        $this->bundleRepository = $bundleRepository;
    }

    /**
     * @param int $offset
     * @param int $limit
     *
     * @return array
     */
    public function getBundles($offset = 0, $limit = 250)
    {
        $bundles = $this->bundleRepository->fetch($offset, $limit);
        $ids = array_column($bundles, 'bundles.id');
        $bundleProducts = $this->bundleRepository->fetchBundleProducts($ids);

        // Strip the table prefix 'bundles' out of the bundles array
        $bundles = $this->mapData($bundles, [], ['bundles']);

        foreach ($bundles as &$bundle) {
            if (isset($bundleProducts[$bundle['id']])) {
                $bundle['products'] = $bundleProducts[$bundle['id']];
            }
        }

        return $this->cleanupResultSet($bundles);
    }
}
```

You have to register the `BundleService` in your `service.xml`:

```html
<service class="SwagMigrationBundleApiExample\Service\BundleService" id="swag_migration_bundle_api_example.bundle_service">
    <argument type="service" id="swag_migration_bundle_api_example.bundle_repository"/>
</service>
```

## Create a new API controller

At last, you have to create a new API controller, which uses the `BundleService` to get your bundle data:

```php
<?php
/**
 * (c) shopware AG <info@shopware.com>
 * For the full copyright and license information, please view the LICENSE
 * File that was distributed with this source code
 */

use SwagMigrationBundleApiExample\Service\BundleService;
use SwagMigrationConnector\Service\ControllerReturnStruct;

class Shopware_Controllers_Api_SwagMigrationBundles extends Shopware_Controllers_Api_Rest
{
    public function indexAction()
    {
        $offset = (int) $this->Request()->getParam('offset', 0);
        $limit = (int) $this->Request()->getParam('limit', 250);

        /** @var BundleService $bundleService */
        $bundleService = $this->container->get('swag_migration_bundle_api_example.bundle_service');

        $bundles = $bundleService->getBundles($offset, $limit);
        $response = new ControllerReturnStruct($bundles, empty($bundles));

        $this->view->assign($response->jsonSerialize());
    }
}
```

Now you have to create the `BundleReader` in the [SwagMigrationBundleExample](extending-a-shopware-migration-profile) plugin, which only contains the Shopware 5 API route:

```php
<?php declare(strict_types=1);

namespace SwagMigrationBundleExample\Profile\Shopware\Gateway\Api\Reader;

use SwagMigrationAssistant\Migration\MigrationContextInterface;
use SwagMigrationAssistant\Profile\Shopware\Gateway\Api\Reader\ApiReader;
use SwagMigrationAssistant\Profile\Shopware\Gateway\Api\ShopwareApiGateway;
use SwagMigrationAssistant\Profile\Shopware\ShopwareProfileInterface;
use SwagMigrationBundleExample\Profile\Shopware\DataSelection\DataSet\BundleDataSet;

class BundleReader extends ApiReader
{
    public function supports(MigrationContextInterface $migrationContext): bool
    {
        return $migrationContext->getProfile() instanceof ShopwareProfileInterface
            && $migrationContext->getGateway()->getName() === ShopwareApiGateway::GATEWAY_NAME
            && $migrationContext->getDataSet()::getEntity() === BundleDataSet::getEntity();
    }

    protected function getApiRoute(): string
    {
        return 'SwagMigrationBundles'; // This defines which API route should called
    }
}
```

After this, you have to register the reader in the Symfony container:

```html
<service id="SwagMigrationBundleExample\Profile\Shopware\Gateway\Api\BundleReader"
         parent="SwagMigrationAssistant\Profile\Shopware\Gateway\Api\Reader\ApiReader">
    <tag name="shopware.migration.reader"/>
</service>
```

With that, you have implemented your first plugin migration via API.

## Source

Check out this [GitHub repository](https://github.com/shopware/swag-docs-extending-shopware-migration-connector) containing a full example source.

---

---

## Search
**Source:** [products/extensions/search.md](https://developer.shopware.com/docs/v6.4/products/extensions/search.md)  
# Search

Shopware Advanced Search (SESP in short) is an Advanced Search module based on Elasticsearch. In addition to a high performance product search, it also offers you the possibilities to customize the search experience depending on your needs. So you could also search for manufacturers and categories. The simple Administration module allows quick and easy configuration of the search.

Before continuing, you should make sure you have a basic knowledge of Elasticsearch and the Shopware implementation of it:

---

---

## Boosting
**Source:** [products/extensions/search/boosting.md](https://developer.shopware.com/docs/v6.4/products/extensions/search/boosting.md)  
# Boosting

## Overview

With the Advanced Search there are two types of boosting:

* [Field Boosting](boosting#field-boosting)
* [Explicit Boosting](boosting#explicit-boosting)

These configurations allow boosting of specific search results.

## Field boosting

With *field boosting*, it's possible to boost the values of a single field. It is easy to [configure in the Administration](https://docs.shopware.com/en/shopware-6-en/enterprise-extensions/enterprise-search#searchable-information). It is just needed to set the configuration to `Prioritized`. In the code, this option is checked. If this field is set to `prioritized`, a little [Boosting](https://www.elastic.co/guide/en/elasticsearch/reference/6.8/mapping-boost.html) of `2` will be added; otherwise, the value will be `1`.

## Explicit boosting

Like the *field boosting*, the *explicit boosting* can be configured in the Administration. With this boosting, you have more possibilities. The `BoostingQueryBuilder` assembles all queries into one [Should Query](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-bool-query.html#query-dsl-bool-query), which contains a [Constant Score Query](https://www.elastic.co/guide/en/elasticsearch/reference/6.8/query-dsl-constant-score-query.html).

---

---

## Completion
**Source:** [products/extensions/search/completion.md](https://developer.shopware.com/docs/v6.4/products/extensions/search/completion.md)  
# Completion

The Advanced Search does not use the default [Elasticsearch Completion](https://www.elastic.co/guide/en/elasticsearch/reference/7.10/search-suggesters.html#completion-suggester) because it does only support a fixed order and the storage size is high. As an alternative, Advanced Search uses aggregations to find the most important word combinations for your search input.

The `FullText` Boosted field is used to generate a list of completions. Each word is a separate completion suggestion.

## Extension for compound completions

::: warning
The default Advanced Search does not support compound completions from multiple words.
:::

To support compound completions, it is necessary to decorate the appropriate Elasticsearch definition. And add the [Service Tag](https://symfony.com/doc/current/service_container/tags.html) `swag_ses.completion_definition` to the service, like to Advanced Search default services. Make sure that the newly created decorator runs after the Advanced Search decorator; otherwise, it will override your values.

```php
// MyProductDefinitionDecorator.php
<?php declare(strict_types=1);

namespace Swag\Example\Completion;

use Shopware\Core\Framework\Context;
use Shopware\Core\Framework\DataAbstractionLayer\Entity;
use Shopware\Core\Framework\DataAbstractionLayer\EntityCollection;
use Shopware\Core\Framework\DataAbstractionLayer\EntityDefinition;
use Shopware\Core\Framework\DataAbstractionLayer\Search\Criteria;
use Shopware\Elasticsearch\Framework\AbstractElasticsearchDefinition;
use Shopware\Elasticsearch\Framework\FullText;

class MyProductDefinitionDecorator extends AbstractElasticsearchDefinition
{
    private AbstractElasticsearchDefinition $decorated;

    public function __construct(
        AbstractElasticsearchDefinition $decorated
    ) {
        $this->decorated = $decorated;
    }

    public function getMapping(Context $context): array
    {
        return $this->decorated->getMapping($context);
    }

    public function extendCriteria(Criteria $criteria): void
    {
        $this->decorated->extendCriteria($criteria);
    }

    public function buildFullText(Entity $entity): FullText
    {
        return $this->decorated->buildFullText($entity);
    }

    public function getEntityDefinition(): EntityDefinition
    {
        return $this->decorated->getEntityDefinition();
    }

    public function extendEntities(EntityCollection $collection): EntityCollection
    {
        $collection = $this->decorated->extendEntities($collection);

        foreach ($collection->getIterator() as $entity) {
            // Here, you can add your custom completions
            $completionTerms = ['blue shoes', 'green socks'];

            CompletionExtension::addCompletionExtension($entity, $completionTerms);
        }

        return $collection;
    }
}
```

---

---

## Extensibility
**Source:** [products/extensions/search/extensibility.md](https://developer.shopware.com/docs/v6.4/products/extensions/search/extensibility.md)  
# Extensibility

::: warning
This article uses many Code-References to GitLab. Please contact the Shopware Sales department to get access to the private repository.
:::

To implement the full search experience for your own entity, you have to implement multiple interfaces.

## Search/suggest gateway

You can create your own `SuggestGatewayInterface`/`SearchGatewayInterface` or use the existing SearchGateway.

The Advanced Search offers two ways to extend the search/suggest results. You can implement the following Interfaces within your services:

* [Swag\EnterpriseSearch\Suggest\SuggestGatewayInterface](https://gitlab.com/shopware/shopware/enterprise/swagenterprisesearchplatform/-/blob/release/src/Suggest/SuggestGatewayInterface.php)
* [Swag\EnterpriseSearch\Search\SearchGatewayInterface](https://gitlab.com/shopware/shopware/enterprise/swagenterprisesearchplatform/-/blob/release/src/Search/SearchGatewayInterface.php)

Or use the existing classes:

* [Swag\EnterpriseSearch\Suggest\SuggestGateway](https://gitlab.com/shopware/shopware/enterprise/swagenterprisesearchplatform/-/blob/release/src/Suggest/SuggestGateway.php)
* [Swag\EnterpriseSearch\Search\SearchGateway](https://gitlab.com/shopware/shopware/enterprise/swagenterprisesearchplatform/-/blob/release/src/Search/SearchGateway.php)

E.g., for your definition, it means the following:

```html
<service id="YourStuff" class="Swag\EnterpriseSearch\Suggest\SuggestGateway">
  <argument type="service" id="definition.repository"/>
  <argument type="service" id="Swag\EnterpriseSearch\Suggest\SuggestCriteriaBuilder"/>

  <tag name="swag_ses.suggest_gateway" key="yourDefinition"/>
</service>
```

The following tags and keys are used for registering the services in the search/suggest:

```text
swag_ses.suggest_gateway
swag_ses.search_gateway
```

The tagged services are used in the following files:

* [Swag\EnterpriseSearch\Search\MultiSearchGateway](https://gitlab.com/shopware/shopware/enterprise/swagenterprisesearchplatform/-/blob/release/src/Search/MultiSearchGateway.php)
* [Swag\EnterpriseSearch\Suggest\MultiSuggestGateway](https://gitlab.com/shopware/shopware/enterprise/swagenterprisesearchplatform/-/blob/release/src/Suggest/MultiSuggestGateway.php)

## The search template

To show the results in the search overview, you have to extend the `search/index.html.twig` and then apply the results in your desired styling.

You can take a look at an example of [Search Template](https://gitlab.com/shopware/shopware/enterprise/swagenterprisesearchplatform/-/tree/release/src/Resources/views/storefront/page/search/index.html.twig).

## The suggest gateway

To show the results in the suggest dropdown, you have to extend [`Storefront/storefront/layout/header/search-suggest.html.twig`](https://gitlab.com/shopware/shopware/enterprise/swagenterprisesearchplatform/-/blob/release/src/Resources/views/storefront/layout/header/search-suggest.html.twig) like the Advanced Search does.

## Admin boosting detail

For creating boosting based on your definition, you have to add the name to the following file.

Currently, the values are hardcoded. See here for reference of [Boosting detail modal](https://gitlab.com/shopware/shopware/enterprise/swagenterprisesearchplatform/-/blob/release/src/Resources/app/administration/src/module/swag-enterprise-search/components/swag-enterprise-search-boosting-detail-modal/swag-enterprise-search-boosting-detail-modal.html.twig#L48).

## Configuration initial value

You need a first pair of configuration entries for a first search. Therefore you have to create a migration. An example could look like this:

```php
        $salesChannels = $connection->fetchAll('SELECT `id` FROM `sales_channel`');

        foreach ($salesChannels as $salesChannel) {
            $ids = [
                'manufacturer' => Uuid::randomHex(),
                'category' => Uuid::randomHex(),
                'product' => Uuid::randomHex(),
                'salesChannel' => $salesChannel['id'],
            ];

            $defaults = "
                INSERT INTO `gateway_configuration`
                (`id`, `entity_name`, `sales_channel_id`, `max_suggest_count`, `max_search_count`, `created_at`) VALUES
                (UNHEX(:product), 'product', :salesChannel, 10, null, NOW()),
                (UNHEX(:manufacturer), 'product_manufacturer', :salesChannel, 10, 30, NOW()),
                (UNHEX(:category), 'category', :salesChannel, 10, 30, NOW())
            ";

            $connection->executeQuery($defaults, $ids);
        }
```

This can be found in the [`Swag\EnterpriseSearch\Migration\Migration1584020367CreateNewGatewayConfiguration`](https://gitlab.com/shopware/shopware/enterprise/swagenterprisesearchplatform/-/blob/release/src/Migration/Migration1584020367CreateNewGatewayConfiguration.php) file.

## Configuration entity

For adding a new configuration while creating a sales channel, you have to create your own [Swag\EnterpriseSearch\Configuration\GatewayConfigurationCreator](https://gitlab.com/shopware/shopware/enterprise/swagenterprisesearchplatform/-/blob/release/src/Configuration/GatewayConfigurationCreator.php) and override the `getEntityNames()` with your additional entity.

## Autocompletion

For adding auto-completion of your definition, you have to add a [CompletionEsDefinitionDecorator](https://gitlab.com/shopware/shopware/enterprise/swagenterprisesearchplatform/-/blob/release/src/Completion/CompletionEsDefinitionDecorator.php) to it. See this example:

```html
 <service id="swag_completion.manufacturer_es_definition"
          class="Swag\EnterpriseSearch\Completion\CompletionEsDefinitionDecorator"
          decorates="Swag\EnterpriseSearch\Manufacturer\ManufacturerEsDefinition">
      <argument type="service" id="swag_completion.manufacturer_es_definition.inner"/>

      <tag name="swag_ses.completion_definition"/>
 </service>
```

You can also change the `extendEntities()` here to apply multi-word auto-suggestions.

## Additional filtering

You may want to filter your definition. This can be done by extending the CriteriaBuilder. An example can be found in [`Swag\EnterpriseSearch\Category\SalesChannelCategorySearchCriteriaBuilder`](https://gitlab.com/shopware/shopware/enterprise/swagenterprisesearchplatform/-/blob/release/src/Category/SalesChannelCategorySearchCriteriaBuilder.php).

---

---

## Field Configuration
**Source:** [products/extensions/search/field-config.md](https://developer.shopware.com/docs/v6.4/products/extensions/search/field-config.md)  
# Field Configuration

With the [relevance](relevance), the Advanced Search offers the possibility to customize the searched fields.

Here, we want to give you brief information about the internal usage of the different Elasticsearch functionalities used for the full text search of the Advanced Search.

## Filter

The Advanced Search adds some additional filters, which will be used by the [Analyzer](field-config#analyzer).

1. **Numeric-Char-Filter (`sesNumericCharFilter`)** - The *numeric char filter* separates strings and numbers, and it normalizes the different spelling issues mostly found in shops.

With the help of this filter, a partial hit can be better found. For example:

Input: `10KG`

Output: `10 KG`

It uses the regex `(\d*)([^\d]*)` and replaces it with `$1 $2`

1. **Character Filter (`sesCharFilter`)** - The *char filter* separates strings from special characters (supported special chars: `-,.\®"/`).

When words are separated by one of these characters, the special character is removed and replaced by whitespace.

```
1. **N-Gram Filter \(`ses_ngram`\)** - This *n-gram filter* uses the elastic search default [n-gram filter](https://www.elastic.co/guide/en/elasticsearch/reference/current/analysis-ngram-tokenizer.html) with the parameters 3 for minimum and 27 for maximum value.

2. **Shingle \(`ses_shingle`\)** - This *shingle filter* uses the elastic search default [shingle](https://www.elastic.co/guide/en/elasticsearch/reference/7.10/analysis-shingle-tokenfilter.html)

The parameters for this analyzer are:

   * Minimum shingle size -&gt; 2
   * Maximum shingle size -&gt; 3
   * Output Unigrams -&gt; false

3. **Synonym \(`ses_synonym`\)** - In the Advanced Search you can define synonyms. These [synonyms](synonyms) are used by the search analyzer.
```

## Analyzer

In addition to the Shopware Elasticsearch default analyzer, the Advanced Search adds some additional analyzer. Each analyzer uses a different set of filters. Here is a list of all used custom analyzers in the Advanced Search:

1. `sesAnalyzer` -   It is the default [Analyzer](https://www.elastic.co/guide/en/elasticsearch/reference/current/analyzer.html) for the content. Filters used are: `sesCharFilter`, `sesNumericCharFilter`.

2. `sesNgramAnalyzer` -  Each string field that is indexed has an internal mapping for an extra field with the suffix `.ngram`. You can configure which field should be used in the [Administration module](https://docs.shopware.com/en/shopware-6-en/enterprise-extensions/enterprise-search?category=shopware-6-en/enterprise-extensions#Configuration). Filters used are: `ses_ngram`, `sesCharFilter`, `sesNumericCharFilter`.

3. `sesShingleAnalyzer` -  Each string field that is indexed has an internal mapping for an extra field with the suffix `.ngram`. You can configure which field should be used in the [Administration module](https://docs.shopware.com/en/shopware-6-en/enterprise-extensions/enterprise-search?category=shopware-6-en/enterprise-extensions#Configuration). Filters used are: `ses_shingle`, `sesCharFilter`, `sesNumericCharFilter`.

4. `sesSearchAnalyzer` -  It is the default [Search analyzer](https://www.elastic.co/guide/en/elasticsearch/reference/current/search-analyzer.html) for the search words. Filters used are: `synonym`.

---

---

## Installation
**Source:** [products/extensions/search/installation.md](https://developer.shopware.com/docs/v6.4/products/extensions/search/installation.md)  
# Installation

Similar to the Shopware Core production and development templates, it is possible to set up SESP as a `dependency/composer` requirement and as a development environment allowing you to contribute to the plugin on its own.

::: warning
To contribute, please get in touch with the Shopware Sales department so as to get access to the private repository.
:::

---

---

## Relevance
**Source:** [products/extensions/search/relevance.md](https://developer.shopware.com/docs/v6.4/products/extensions/search/relevance.md)  
# Relevance

The relevance is calculated per [Dis max query](https://www.elastic.co/guide/en/elasticsearch/reference/6.8/query-dsl-dis-max-query.html). The [Tie break](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-multi-match-query.html#tie-breaker) is constant and set to `0.4`, which is the recommended value by Elasticsearch.

## Indexing

In addition to the default indexing, the Advanced Search indexes every field of the Entity definition with additional [Sub-fields](field-config) to Elasticsearch by default. This is done because it is possible to [define in the Administration](https://docs.shopware.com/en/shopware-6-en/enterprise-extensions/enterprise-search) which field should be searched and how searches on that field should perform. On the one hand, indexing everything supports usability. You can make changes to the configuration and you don't need to reindex everything. But on the other hand, the created index could be huge.

## Fuzziness

Elasticsearch supports by default a [Fuzzy search](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-fuzzy-query.html). In the Advanced Search the fuzziness depends on the type of a field. The fuzziness for a numeric term is 0, and the `auto` value is taken for other terms.

---

---

## Synonyms
**Source:** [products/extensions/search/synonyms.md](https://developer.shopware.com/docs/v6.4/products/extensions/search/synonyms.md)  
# Synonyms

The Synonyms are defined in the `%PLUGIN_DIR%/Resources/config/Synonyms.php`. The path to this file is saved in the `swag_ses_synonym_dir` parameter of the container and can be overridden with the default [Dependency Injection](../../../guides/plugins/plugins/plugin-fundamentals/add-plugin-dependencies). See [how to override](synonyms#how-to-override) for more information.

::: info
The syntax in the association is the [Solr syntax](https://www.elastic.co/guide/en/elasticsearch/reference/current/analysis-synonym-tokenfilter.html#_solr_synonyms).
:::

The path parameter is later passed to the `Swag\EnterpriseSearch\Relevance\SynonymProvider` class.

## Example

```php
// Synonyms.php
<?php declare(strict_types=1);

use Swag\EnterpriseSearch\Relevance\SynonymProvider;

return [
    SynonymProvider::DEFAULT_KEY => [
        'i-pod, i pod => ipod',
        'universe, cosmos',
    ],
];
```

The `SynonymProvider` supports multi-languages and a default fallback. The language code can be added as an array key for a specific language, like the following:

```php
// Synonyms.php with multi-language support
<?php declare(strict_types=1);

use Swag\EnterpriseSearch\Relevance\SynonymProvider;

return [
    SynonymProvider::DEFAULT_KEY => [
        'i-pod, i pod => ipod',
        'universe, cosmos',
    ],
    'en-GB' => [
        'foozball, foosball',
        'sea biscuit, sea biscit => seabiscuit',
    ],
];
```

## How to override

1. Shopware configuration
   1. Shopware is based on Symfony, so it is possible to [override](https://symfony.com/doc/2.0/cookbook/bundles/override.html#services-configuration) the Service parameters in Symfony style.
   2. Parametername `swag_ses_synonym_dir`
2. Own plugin
   1. [Create a plugin](../../../guides/plugins/plugins/plugin-base-guide)
   2. Add a [Dependency Injection](../../../guides/plugins/plugins/plugin-fundamentals/dependency-injection#injecting-another-service) file
   3. Create a file with your [Synonyms](synonyms#example)
   4. [Add a parameter](https://symfony.com/doc/2.0/cookbook/bundles/override.html#services-configuration) to the Dependency Injection file.

```html
// services.xml
<parameters>
    <parameter key="swag_ses_synonym_dir">%kernel.project_dir%/MySynonyms.php</parameter>
</parameter>
```

::: warning
Make sure that the paths match.
:::

---

---

## Subscriptions
**Source:** [products/extensions/subscriptions.md](https://developer.shopware.com/docs/v6.6/products/extensions/subscriptions.md)  
# Subscriptions

To enable flexibility in product offerings, the subscription extension aims to provide a subscription-based model for products. This extension allows you to offer products on a subscription basis. The subscription model is a recurring payment model where customers can subscribe to a product and receive it at regular intervals. This model is beneficial for products that are consumed regularly, such as groceries, cosmetics, or magazines.

We suggest that you first familiarize yourself with the [subscription concepts](./concept.md) as well as the [user documentation](https://docs.shopware.com/en/shopware-6-en/settings/shop/subscriptions) before you start using the extension.

---

---

## Concepts
**Source:** [products/extensions/subscriptions/concept.md](https://developer.shopware.com/docs/v6.6/products/extensions/subscriptions/concept.md)  
# Concepts

To use subscriptions, you will need to be familiar with two core concepts in subscription models.

## Plans

A plan is a set of rules that define the subscription. This includes the billing interval and the product that the customer will receive. Multiple intervals can be assigned to a single plan. Plans can be created and managed in the Shopware administration.

## Intervals

An interval is the time between each delivery cycle. For example, a delivery can be monthly, quarterly, or annually. Billing is triggered each time a delivery cycle repeats. The interval is defined in the plan and can be set to any time frame. This is also created and managed in the Shopware administration.

Intervals can be of three different types:

### Relative

A relative interval is an interval that is determined by a previous interval. For example, if a customer subscribes to a monthly plan, the next interval will be one month after the first delivery. These intervals are determined by using PHP's `DateInterval` class.

### Absolute

An absolute interval is an interval that is determined by a fixed date. For example, if a customer subscribes to a monthly plan, the next interval will be on a fixed day like the 1st or 15th of each month. These work with cron expressions.

### Mixed

A mix of the two types above. For instance, a customer subscribes to a plan that delivers every 12 weeks, but only on a Friday. These intervals are determined by using PHP's `DateInterval` class in combination with cron expressions.

## Further reading

You can read more about the setup of plans and intervals in the [Shopware documentation](https://docs.shopware.com/en/shopware-6-en/settings/shop/subscriptions).

---

---

## Guides
**Source:** [products/extensions/subscriptions/guides.md](https://developer.shopware.com/docs/v6.6/products/extensions/subscriptions/guides.md)  
# Guides

This section will help with common topics regarding usage of subscriptions.

---

---

## B2B Employee Integration for Subscriptions
**Source:** [products/extensions/subscriptions/guides/b2b-employee-integration.md](https://developer.shopware.com/docs/products/extensions/subscriptions/guides/b2b-employee-integration.md)  
# B2B Employee Integration for Subscriptions

When using Subscriptions together with B2B Components Employee Management, subscriptions can be managed and tracked in a B2B employee context.

## Overview

The B2B Employee Integration extends subscription functionality to support employee-based workflows in B2B scenarios. This integration enables:

* **Permission-based subscription access** - Control which subscriptions employees can view based on their assigned permissions
* **Employee tracking** - Track which employee created each subscription for audit and reporting purposes
* **Organization context** - Maintain organization information in both initial and renewal subscription orders

## When to Use

This integration is relevant when you have:

* A B2B store with employee management enabled
* Subscriptions that employees should manage on behalf of their organization
* Requirements for permission-based access control to subscription data
* Need for tracking which employee initiated subscriptions

## Prerequisites

To use this integration, you need:

* Shopware 6.7 with the **Subscriptions** extension installed
* **B2B Components** with Employee Management module enabled
* Employees configured with appropriate roles and permissions

## Key Capabilities

### 1. Permission-Based Viewing

Employees can view subscriptions based on three permission levels:

* **`subscription.read.all`** - View all subscriptions in the system
* **`organization_unit.subscription.read`** - View subscriptions from their organization unit plus their own
* **No subscription permission** - View only subscriptions they personally created

### 2. Employee Context in Orders

When an employee creates a subscription:

* The **initial order** includes employee and organization data
* All **renewal orders** automatically maintain this context
* Employee information is preserved for reporting and compliance

### 3. Transparent Integration

The integration works seamlessly with existing subscription workflows:

* Works with both [separate checkout](./separate-checkout.md) and [mixed checkout](./mixed-checkout.md) flows
* No changes required to existing subscription products or plans
* Employee context is automatically added when an employee is logged in

## Technical Documentation

For detailed technical information including architecture, event flows, database schema, and developer integration points, see:

**[B2B Employee Subscription Integration Guide](../../b2b-components/employee-management/guides/subscription-integration.md)**

The technical guide covers:

* Architecture and integration patterns (decorators, event subscribers, entity extensions)
* Database schema for employee-subscription relationships
* Detailed flow diagrams for initial orders, renewals, and permission filtering
* Code examples for accessing employee data from subscriptions and orders
* Extension points for adding custom B2B logic

## Related Documentation

* [Subscription Concept](../concept.md) - Understanding subscription fundamentals
* [Mixed Checkout](./mixed-checkout.md) - Mixed cart checkout with subscriptions
* [Separate Checkout](./separate-checkout.md) - Separate subscription checkout flow
* [B2B Employee Management](../../b2b-components/employee-management/index.md) - Employee and role management basics

---

---

## Events
**Source:** [products/extensions/subscriptions/guides/events.md](https://developer.shopware.com/docs/v6.6/products/extensions/subscriptions/guides/events.md)  
# Events

Most of the events triggered within subscription checkout are prefixed with `subscription.`. These events are identical to normal checkout events. If you wish to use these events, you need to subscribe to them.

```php
// Normal Event Listener
class MyEventSubscriber implements EventSubscriberInterface
{
    public static function getSubscribedEvents(): array
    {
        return [CheckoutOrderPlacedCriteriaEvent::class => 'onOrderPlacedCriteria'];
    }

    public function onOrderPlacedCriteria(CheckoutOrderPlacedCriteriaEvent $event): void
    {
        // Your event handler logic
    }
}

// Subscription Event Listener
class MyEventSubscriber implements EventSubscriberInterface
{
    public static function getSubscribedEvents(): array
    {
        return ['subscription.' . CheckoutOrderPlacedCriteriaEvent::class => 'onOrderPlacedCriteria'];
    }

    public function onOrderPlacedCriteria(CheckoutOrderPlacedCriteriaEvent $event): void
    {
        // Your event handler logic
    }
}
```

These are the events available in the subscription checkout (subject to change):

* AfterLineItemAddedEvent
* AfterLineItemRemovedEvent
* AfterLineItemQuantityChangedEvent
* BeforeLineItemAddedEvent
* BeforeLineItemRemovedEvent
* BeforeLineItemQuantityChangedEvent
* BeforeCartMergeEvent
* CartCreatedEvent
* CartConvertedEvent
* CartDeletedEvent
* CartLoadedEvent
* CartMergedEvent
* CartSavedEvent
* CartVerifyPersistEvent
* CheckoutCartPageLoadedEvent
* CheckoutConfirmPageLoadedEvent
* CheckoutOrderPlacedCriteriaEvent
* CheckoutOrderPlacedEvent
* CheckoutRegisterPageLoadedEvent
* LineItemRemovedEvent
* SalesChannelContextCreatedEvent
* SalesChannelContextResolvedEvent
* SalesChannelContextRestoredEvent
* SalesChannelContextRestorerOrderCriteriaEvent
* OffcanvasCartPageLoadedEvent

---

---

