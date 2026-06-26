# DAL AND DATA

Compiled excerpts from the Shopware Developer Documentation snapshot. Prefer live docs at [developer.shopware.com](https://developer.shopware.com/) when in doubt.

---

## Data Abstraction Layer
**Source:** [concepts/framework/data-abstraction-layer.md](https://developer.shopware.com/docs/v6.6/concepts/framework/data-abstraction-layer.md)  
# Data Abstraction Layer

## Database access

### Database guide

In contrast to most Symfony applications, Shopware uses no ORM, but a thin abstraction layer called the data abstraction layer (DAL).
The DAL is implemented with the specific needs of Shopware in mind and lets developers access the database via pre-defined interfaces.
Some concepts used by the DAL, like Criteria, may sound familiar to you if you know [Doctrine](https://symfony.com/doc/current/doctrine.html) or other ORMs.
A reference to more in-depth documentation about the DAL can be found below.

Refer to [Shopware 6.6.5.0 entity relationship model](../../../assets/shopware6-erd.pdf) that depicts different tables and their relationships.

Alternatively, you can export a fresh ER model, using [MySQL Workbench](https://dev.mysql.com/doc/workbench/en/wb-reverse-engineering.html), [PHPStorm Database Tools](https://www.jetbrains.com/help/phpstorm/creating-diagrams.html), or similar tool.

::: info
Mysql Workbench → File → Import → Reverse Engineer Mysql Script → Select Db → ER diagram is created.
If you want to have it as an image: File → Export → Export as PNG
:::

### CRUD operations

An EntityRepository is used to interact with the DAL.
This is the recommended way for developers to interface with the DAL or the database in general.

### Provisioning code to use the repositories

Before using the repositories, you will need to get them from the [Dependency Injection Container (DIC)](../../guides/plugins/plugins/plugin-fundamentals/dependency-injection).
This is done with [Constructor injection](https://symfony.com/doc/current/service_container/injection_types.html#constructor-injection), so you will need to extend your services constructor by expecting an EntityRepository:

```php
// <plugin root>/src/Service/DalExampleService.php
public function __construct (EntityRepository $productRepository)
{
    $this->productRepository = $productRepository;
}
```

If you are using [Service autowiring](https://symfony.com/doc/current/service_container/autowiring.html) with the correct type and argument variable names, the repository will be injected automatically.

Alternatively, configure the `product.repository` service to be injected explicitly:

```html
// <plugin root>src/Resources/config/service.xml
<service id="Swag\ExamplePlugin\Service\DalExampleService">
    <argument type="service" id="product.repository"/>
</service>
```

You can read more about dependency injection and service registration in Shopware in the services guides:

### Translations

The DAL was designed, among other things, to enable the special requirements of Shopware's translation system.
When a record is read or searched, three language levels are searched.

1. **Current language**: The first level is the current language that is set and displayed to the user.
2. **Parent language**: the second level is an optional parent language that can be configured.
   So it is possible to translate certain dialects faster.
3. **System language**: The third and last level is the system language that is selected during the installation.
   Each entity in the system has a translation in this language.
   This serves as a final fallback to ensure only one label for the entity in the end.

The translations for a record are stored in a separate table.
The name of this table is always the same as the table for which the records are translated, with the additional suffix `_translation`.

### Versioning

Another feature that the DAL offers is versioning.
This makes it possible to store multiple versions of a single entity.
All data assigned to an entity is duplicated and made available under the new version.
Multiple entities or changes to different entities can be stored for one version.
The versioning was designed for previews, publishing, or campaign features, to prepare changes that are not yet live and to be able to view them in the store.
Currently, it is not possible (yet) to create a completely new entity with another version than the default live version.
Means, you cannot "draft" the entity first and then update it into the live version.
A live version of your entity is always required, before deriving a new version from it.

The versioning is also reflected in the database.
Entities that are versionable always have a compound foreign key: `id`, `version_id`.
Also, the foreign keys, which point to a versioned record, always consist of two columns, e.g.: `product_id` and `product_version_id`.

### Context

The context `core/Framework/Context.php` defines important configuration of the shop system and is instantiated once per request.
Depending on the passed parameters it can change the CRUD behavior of the DAL.
For example when using the currency toggle in the storefront and selecting Dollar instead of Euro, the context currency ID is changed accordingly and all operations now refer to Dollar.

### Inheritance

Another reason why the DAL was designed is to meet the requirements of the product and variant system.
For this purpose, a parent-child inheritance system was implemented in the DAL.
This allows variants to inherit records, properties, or even whole associations from the parent or container product.
For example, if a variant has not been assigned any categories or images, those of the parent product are used.

### Indexing

The DAL was designed to be optimized for use in ecommerce.
One principle has proven to be very effective so far: "The more time you put into indexing data, the faster it is possible to read it".
This is reflected in Shopware as follows:

* A product is written once every X minutes
* A product is called X times every X seconds by a customer.

This varies depending on the store, but the ratio is always the same.
Data records are read way more often than they are written.
Therefore, it is worthwhile to spend a little more time on the writing process in order to minimize the effort required for the reading process.
This is done in the DAL via the Entity Indexer pattern.
As soon as a product record is written, the corresponding Product Indexer is triggered, which pre-selects certain aggregations and writes them away optimized for the later reading process.

---

---

## Data Handling/DataAbstractionLayer
**Source:** [guides/plugins/plugins/framework/data-handling.md](https://developer.shopware.com/docs/v6.6/guides/plugins/plugins/framework/data-handling.md)  
# Data Handling/DataAbstractionLayer

The data handling, or the Data Abstraction Layer (DAL), can be an overwhelming topic. Yet, if you know the right start, it will be fairly easy to deal with.

Hence, here are some good starting topics:

Also, [listening to events](using-database-events) of the DAL will come in handy for sure.

---

---

## Adding Complex Data to Existing Entities
**Source:** [guides/plugins/plugins/framework/data-handling/add-complex-data-to-existing-entities.md](https://developer.shopware.com/docs/v6.6/guides/plugins/plugins/framework/data-handling/add-complex-data-to-existing-entities.md)  
*(Body truncated in this bundle; follow the link for the rest.)*

# Adding Complex Data to Existing Entities

## Overview

Sometimes you want to extend existing entities with some custom information. Extensions are technical and not configurable by the admin user. Also, they can deal with more complex types than scalar ones.

## Prerequisites

To create your own entity extension for your plugin, you first need a plugin as base. Please refer to the [Plugin Base Guide](../../plugin-base-guide).

Basic knowledge of [creating a custom entity](add-custom-complex-data) and [adding associations](add-data-associations) will also be helpful for this guide.

## Creating the extension

In this example, we're going to add a new string field to the `product` entity.

You can choose whether you want to save the new string field to the database or not. Therefore, you're going to see two sections, one for each way.

For both cases, you need to create a new "extension" class in the directory `<plugin root>/src/Extension/`. In this case, we want to extend the `product` entity, so we create a subdirectory `Content/Product/` since the entity location in the Core is the same. Our class needs to extend from the abstract `Shopware\Core\Framework\DataAbstractionLayer\EntityExtension` class, which forces you to implement the `getDefinitionClass` method. It has to point to the entity definition you want to extend, so `ProductDefinition` in this case.

You add new fields by overriding the method `extendFields` and add your new fields in there.

Here's an example class called `CustomExtension`:

```php
// <plugin root>/src/Extension/Content/Product/CustomExtension.php
<?php declare(strict_types=1);

namespace Swag\BasicExample\Extension\Content\Product;

use Shopware\Core\Content\Product\ProductDefinition;
use Shopware\Core\Framework\DataAbstractionLayer\EntityExtension;
use Shopware\Core\Framework\DataAbstractionLayer\FieldCollection;

class CustomExtension extends EntityExtension
{
    public function extendFields(FieldCollection $collection): void
    {
        $collection->add(
            // new fields here
        );
    }

    public function getDefinitionClass(): string
    {
        return ProductDefinition::class;
    }
}
```

Now we have to register our extension via the DI-container. If you don't know how that's done in general, head over to our guide about registering a custom service [Add a custom class / service](../../plugin-fundamentals/add-custom-service) or our guide about the [dependency injection](../../plugin-fundamentals/dependency-injection).

Here's our `services.xml`:

```xml
// <plugin root>/src/Resources/config/services.xml
<?xml version="1.0" ?>

<container xmlns="http://symfony.com/schema/dic/services"
           xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
           xsi:schemaLocation="http://symfony.com/schema/dic/services http://symfony.com/schema/dic/services/services-1.0.xsd">

    <services>
        <service id="Swag\BasicExample\Extension\Content\Product\CustomExtension">
            <tag name="shopware.entity.extension"/>
        </service>
    </services>
</container>
```

### Adding a field with a database

In this guide, you're extending the product entity in order to add a new string field to it. Since you must not extend the `product` table with a new column, you'll have to add a new table which contains the new data for the product. This new table will then be associated using a [OneToOne association](add-data-associations#One%20to%20One%20associations).

Let's start with the `CustomExtension` class by adding a new field in the `extendFields` method.

```php
// <plugin root>/src/Extension/Content/Product/CustomExtension.php
<?php declare(strict_types=1);

namespace Swag\BasicExample\Extension\Content\Product;
use Shopware\Core\Content\Product\ProductDefinition;
use Shopware\Core\Framework\DataAbstractionLayer\EntityExtension;
use Shopware\Core\Framework\DataAbstractionLayer\Field\OneToOneAssociationField;
use Shopware\Core\Framework\DataAbstractionLayer\FieldCollection;

class CustomExtension extends EntityExtension
{
    public function extendFields(FieldCollection $collection): void
    {
        $collection->add(
            new OneToOneAssociationField('exampleExtension', 'id', 'product_id', ExampleExtensionDefinition::class, true)
        );
    }

    public function getDefinitionClass(): string
    {
        return ProductDefinition::class;
    }
}
```

As you can see, we're adding a new `OneToOneAssociationField`. Its parameters are the following, in correct order:

* `propertyName`: The name of the property which should contain the associated entity of type `ExampleExtensionDefinition` in the `ProductDefinition`. Property names are usually camelCase, with the first character being lower cased.
* `storageName`: Use the `id` column here, which refers to the `id` field of your product. This will be used for the connection to your association. Storage names are always lowercase and snake\_cased.
* `referenceField`: In the `storageName` you defined one of the two connected columns, `id`. The name of the other column in the database, which you want to connect via this association, belongs into this parameter. In that case, it will be a column called `product_id`, which we will define in the `ExampleExtensionDefinition`.
* `referenceClass`: The class name of the definition that we want to connect via the association.
* `autoload`: As the name suggests, this parameter defines if this association should always be loaded by default when the product is loaded. In this case, we definitely want that.

#### Creating ExampleExtensionDefinition

You most likely noticed the new class `ExampleExtensionDefinition`, which we're going to create now. It will contain the actual string field that we wanted to add to the product.

Creating a new entity is not explained in this guide, so make sure you know [this guide](add-custom-complex-data) beforehand.

Our new entity will be located in the same directory as our extension. Let's first have a look at it before going into the explanation:

```php
// <plugin root>/src/Extension/Content/Product/ExampleExtensionDefinition.php
<?php declare(strict_types=1);

namespace Swag\BasicExample\Extension\Content\Product;

use Shopware\Core\Content\Product\ProductDefinition;
use Shopware\Core\Framework\DataAbstractionLayer\EntityDefinition;
use Shopware\Core\Framework\DataAbstractionLayer\Field\FkField;
use Shopware\Core\Framework\DataAbstractionLayer\Field\Flag\PrimaryKey;
use Shopware\Core\Framework\DataAbstractionLayer\Field\Flag\Required;
use Shopware\Core\Framework\DataAbstractionLayer\Field\IdField;
use Shopware\Core\Framework\DataAbstractionLayer\Field\OneToOneAssociationField;
use Shopware\Core\Framework\DataAbstractionLayer\Field\StringField;
use Shopware\Core\Framework\DataAbstractionLayer\FieldCollection;

class ExampleExtensionDefinition extends EntityDefinition
{
    public const ENTITY_NAME = 'swag_example_extension';

    public function getEntityName(): string
    {
        return self::ENTITY_NAME;
    }

    public function getEntityClass(): string
    {
        return ExampleExtensionEntity::class;
    }

    protected function defineFields(): FieldCollection
    {
        return new FieldCollection([
            (new IdField('id', 'id'))->addFlags(new Required(), new PrimaryKey()),
            new FkField('product_id', 'productId', ProductDefinition::class),
            (new StringField('custom_string', 'customString')),
            // ReferenceVersionField only needed on versioned entities
            new ReferenceVersionField(ProductDefinition::class, 'product_version_id'),
            new OneToOneAssociationField('product', 'product_id', 'id', ProductDefinition::class, false)
        ]);
    }
}
```

We've created a new entity definition called `ExampleExtensionDefinition`, as mentioned in the `CustomExtension` class. Its table name will be `swag_example_extension` and it will have a custom entity class called `ExampleExtensionEntity`, as you can see in the `getEntityClass` method. This will remain an example, creating the actual entity `ExampleExtensionEntity` is not part of this guide.

So let's have a look at the `defineFields` method. There's the default `IdField`, that almost every entity owns. The next field is the actual `product_id` column, which will be necessary in order to properly this entity with the product and vice versa. It has to be defined as `FkField` since that's what it is: a foreign key.

Now we're getting to the actual new data, in this example, this is just a new string field. It is called `customString` and can now be used in order to store new string data for the product in the database.

The last field is the inverse side of the `OneToOneAssociationField`. The first parameter defines the name of the property again, which will contain the `ProductEntity`. Now take a look at the second and third parameters. Those are the same as in the `ProductDefinition`, but the other way around. This order is important.

The fourth parameter is the class of the associated definition, the `ProductDefinition` in this case. The last parameter, once again, defines the autoloading. In this example, the product definition will **not** be loaded, when you're just trying to load this extension entity. Yet, the extension entity will always automatically be loaded when the product entity is loaded, just like we defined earlier.

Of course, this new definition also needs to be registered to the DI container:

```xml
// <plugin root>/src/Resources/config/services.xml
<?xml version="1.0" ?>

<container xmlns="http://symfony.com/schema/dic/services"
           xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
           xsi:schemaLocation="http://symfony.com/schema/dic/services http://symfony.com/schema/dic/services/services-1.0.xsd">

    <services>
        <service id="Swag\BasicExample\Extension\Content\Product\CustomExtension">
            <tag name="shopware.entity.extension"/>
        </service>

        <service id="Swag\BasicExample\Extension\Content\Product\ExampleExtensionDefinition">
            <tag name="shopware.entity.definition" entity="swag_example_extension" />
        </service>
    </services>
</container>
```

#### Adding the new database table

Of course, you have to add the new database table via a [Database migration](../../plugin-fundamentals/database-migrations). Look at the guide linked above to see how exactly this is done. Here's the example migration and how it could look like:

```php
<?php declare(strict_types=1);

namespace Swag\BasicExample\Migration;

use Doctrine\DBAL\Connection;
use Shopware\Core\Framework\Migration\MigrationStep;

class Migration1614903457ExampleExtension extends MigrationStep
{
    public function getCreationTimestamp(): int
    {
        return 1614903457;
    }

    public function update(Connection $connection): void
    {
    // product_version_id only needed when extending a versioned entity
        $sql = <<<SQL
CREATE TABLE IF NOT EXISTS `swag_example_extension` (
    `id` BINARY(16) NOT NULL,
    `product_id` BINARY(16) NULL,
    `product_version_id` BINARY(16) NOT NULL,
    `custom_string` VARCHAR(255) NULL,
    `created_at` DATETIME(3) NOT NULL,
    `updated_at` DATETIME(3) NULL,
    PRIMARY KEY (`id`),
    CONSTRAINT `unique.swag_example_extension.product` UNIQUE (`product_id`, `product_version_id`),
    CONSTRAINT `fk.swag_example_extension.product_id` FOREIGN KEY (`product_id`, `product_version_id`) REFERENCES `product` (`id`, `version_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
SQL;
        $connection->executeStatement($sql);
    }

    public function updateDestructive(Connection $connection): void
    {
    }
}
```

##### Foreign keys

The `AssociationFields` take care of loading the data, but it is recommended to add [foreign key constraints](https://dev.mysql.com/doc/refman/8.0/en/create-table-foreign-keys.html) to your migrati

… **Truncated.** Full document: https://developer.shopware.com/docs/v6.6/guides/plugins/plugins/framework/data-handling/add-complex-data-to-existing-entities.md


---

## Adding Custom Complex Data
**Source:** [guides/plugins/plugins/framework/data-handling/add-custom-complex-data.md](https://developer.shopware.com/docs/v6.6/guides/plugins/plugins/framework/data-handling/add-custom-complex-data.md)  
*(Body truncated in this bundle; follow the link for the rest.)*

# Adding Custom Complex Data

## Overview

Quite often, your plugin has to save data into a custom database table. Shopware 6's data abstraction layer fully supports custom entities, so you don't have to take care of the data handling at all.

## Prerequisites

This guide is built upon the [Plugin base guide](../../plugin-base-guide), but any plugin will work here. Just note that all examples are using the plugin mentioned above. In order to create a database table, you need to understand plugin migrations [Plugin migrations](../../plugin-fundamentals/database-migrations). Also, you'll have to understand how the [Dependency injection](../../plugin-fundamentals/dependency-injection) works as well.

::: info
Refer to this video on **[Creating a custom entity](https://www.youtube.com/watch?v=mTHTyof4gPk)**. Also available on our free online training ["Shopware 6 Backend Development"](https://academy.shopware.com/courses/shopware-6-backend-development-with-jisse-reitsma).
:::

## Creating the database table

We'll start with creating a new database table. Make sure to always add your individual prefix to your plugin's database tables, e.g. your manufacturer name.

In this guide we'll name our table `swag_example`, you'll find this name a few more times in here, so make sure to remember that one.

As already mentioned in the prerequisites, creating a database table is done via plugin migrations [Plugin migrations](../../plugin-fundamentals/database-migrations), head over to this guide to understand how this example works.

```php
// <plugin root>/src/Migration/Migration1611664789Example.php
<?php declare(strict_types=1);

namespace Swag\BasicExample\Migration;

use Doctrine\DBAL\Connection;
use Shopware\Core\Framework\Migration\MigrationStep;

class Migration1611664789Example extends MigrationStep
{
    public function getCreationTimestamp(): int
    {
        return 1611664789;
    }

    public function update(Connection $connection): void
    {
        $sql = <<<SQL
CREATE TABLE IF NOT EXISTS `swag_example` (
    `id` BINARY(16) NOT NULL,
    `name` VARCHAR(255) COLLATE utf8mb4_unicode_ci,
    `description` VARCHAR(255) COLLATE utf8mb4_unicode_ci,
    `active` TINYINT(1) COLLATE utf8mb4_unicode_ci,
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

    public function updateDestructive(Connection $connection): void
    {
    }
}
```

After reinstalling your plugin, you should see your new database table `swag_example`.

## Creating an entity

### EntityDefinition class

Introducing the table to Shopware 6 is done by adding a so called `EntityDefinition` for your table. As the name suggests, it defines your own entity, including its fields and name, the latter also represents the table name and therefore has to perfectly match.

Your custom entity definition should be placed inside a folder named after the domain it handles, e.g. "Checkout" if you were to include a Checkout entity. Thus, a good location for this example could be in a directory like this: `<plugin root>/src/Core/Content/Example`\
This will also be the case for the `Entity` class itself, as well as the `EntityCollection` class, but those are explained later in this guide.

Start of with creating a new file named `ExampleDefinition.php` in the directory `<plugin root>/src/Core/Content/Example/ExampleDefinition.php`. Below you can see our example definition, which is explained afterwards:

```php
// <plugin root>/src/Core/Content/Example/ExampleDefinition.php
<?php declare(strict_types=1);

namespace Swag\BasicExample\Core\Content\Example;

use Shopware\Core\Framework\DataAbstractionLayer\EntityDefinition;
use Shopware\Core\Framework\DataAbstractionLayer\FieldCollection;

class ExampleDefinition extends EntityDefinition
{
    public const ENTITY_NAME = 'swag_example';

    public function getEntityName(): string
    {
        return self::ENTITY_NAME;
    }

    protected function defineFields(): FieldCollection
    {
        return new FieldCollection([]);
    }
}
```

First of all, your own definition has to extend from the class `Shopware\Core\Framework\DataAbstractionLayer\EntityDefinition`, which enforces you to implement two methods: `getEntityName` and `defineFields`.

The method `getEntityName` returns a string equal to your table name. In this example it is `swag_example`. Keep in mind, that the return of your `getEntityName` method will be used for two cases:

* The database table name
* The repository name in the DI container (`<the-name>.repository`)

The method `defineFields` contains all the fields, that your entity or table consists of.

As you can see in your migration, your table consists of the following fields: You've got an `id` field, a `name` field, a `description` and an `active` field. Other than that, the other two columns `created_at` and `updated_at` don't have to be defined in your definition, since they're included by default. You're asked to return a `Shopware\Core\Framework\DataAbstractionLayer\FieldCollection` instance here, which then has to contain an array of your fields. There's several field classes, e.g. an `Shopware\Core\Framework\DataAbstractionLayer\Field\IdField` or a `Shopware\Core\Framework\DataAbstractionLayer\Field\StringField`, which you have to create and pass into the `FieldCollection`, so let's do that.

```php
// <plugin root>/src/Core/Content/Example/ExampleDefinition.php
<?php declare(strict_types=1);

namespace Swag\BasicExample\Core\Content\Example;

use Shopware\Core\Framework\DataAbstractionLayer\EntityDefinition;
use Shopware\Core\Framework\DataAbstractionLayer\FieldCollection;
use Shopware\Core\Framework\DataAbstractionLayer\Field\BoolField;
use Shopware\Core\Framework\DataAbstractionLayer\Field\Flag\PrimaryKey;
use Shopware\Core\Framework\DataAbstractionLayer\Field\Flag\Required;
use Shopware\Core\Framework\DataAbstractionLayer\Field\IdField;
use Shopware\Core\Framework\DataAbstractionLayer\Field\StringField;

class ExampleDefinition extends EntityDefinition
{
    public const ENTITY_NAME = 'swag_example';

    public function getEntityName(): string
    {
        return self::ENTITY_NAME;
    }

    protected function defineFields(): FieldCollection
    {
        return new FieldCollection([
            (new IdField('id', 'id'))->addFlags(new Required(), new PrimaryKey()),
            (new StringField('name', 'name')),
            (new StringField('description', 'description')),
            (new BoolField('active', 'active'))
        ]);
    }
}
```

As you can see, we've implemented an `IdField` for the `id` column, a `StringField` for the `name` and the `description`, as well as a `BoolField` for the `active` column. Most `Field` classes ask for two parameters, such as the `IdField`:

* A storage name, which represents the name of the field in the storage, e.g. the column in an SQL database.
* A property name, which defines how you can access this field later on. Make sure to remember those for the next step.

The `storageName` is written in snake\_case, while the `propertyName` must be written in lowerCamelCase.

Another thing to note is the `addFlags` call on the `IdField`. Those flags are like attributes to fields, such a required field being marked by using the `Required` flag.

If you want to know more about the flags and how to use them, head over to our guide on how to use flags [Using flags](using-flags).

All that's left to do now, is to introduce your `ExampleDefinition` to Shopware by registering your class in your `services.xml` file and by using the `shopware.entity.definition` tag, because Shopware is looking for definitions this way. If your plugin does not have a `services.xml` file yet or you don't know how that's done, head over to our guide about registering a custom service [Add a custom class / service](../../plugin-fundamentals/add-custom-service) or our guide about the [Dependency injection](../../plugin-fundamentals/dependency-injection).

Here's the `services.xml` as it should look like:

```xml
<?xml version="1.0" ?>
<container xmlns="http://symfony.com/schema/dic/services"
           xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
           xsi:schemaLocation="http://symfony.com/schema/dic/services http://symfony.com/schema/dic/services/services-1.0.xsd">

    <services>
        <service id="Swag\BasicExample\Core\Content\Example\ExampleDefinition">
            <tag name="shopware.entity.definition" entity="swag_example" />
        </service>
    </services>
</container>
```

Please note the tag for your definition and the respective `entity` attribute, which has to contain the technical name of your entity, which you provided in your entity definition. In this case this must be `swag_example`.

And basically that's it already for your definition class. Theoretically you could start using your entity now by injecting the `swag_example.repository` service to other services and start working with the repository, e.g. to [read data](reading-data) or to [write data](writing-data).

Yet, we highly recommend you to create a custom `Entity` class, as well as a custom `EntityCollection` class. This is not mandatory, but those will be replaced with generic classes otherwise.

### Entity class

The entity class itself is a simple key-value object, like a struct, which contains as many properties as fields in the definition, ignoring the ID field, which is handled by the `EntityIdTrait`.

::: warning
The properties of your entity class have to be at least `protected`, otherwise the data abstraction layer won't be able to set the values.
For the same reason `readonly` properties are not allowed. This holds true not just for `Entity` classes, but for all classes that extend the generic `Struct` class.
:::

```php
// <plugin root>/src/Core/Content/Example/ExampleEntity.php
<?php declare(strict_types=1);

namespace Swag\BasicExample\Core\Content\Example;

use Shopware\Core\Framework\DataAbstractionLayer\Entity;
use Shopware\Core\Framework\DataAbstractionLayer\EntityIdTrait;

class ExampleEntity extends Entity
{
    use EntityIdTrait;

    protected ?string $name;

    protected ?string $description;

    protected bool $active;

    public function getName(): ?string
    {
        return $this->name;
    }

    public function setName(?string $name): void
    {
        $this->name = $name;
    }

    public function getDescription(): ?string
    {
        return $this->description;
    }

    public function setDescription(?string $description): void
    {
        $this->description = $description;
    }

    public function isActive(): bool
    {
        return $this->active;
    }

    public function setActive(bool $active): void
    {
        $this->active = $active;
    }
}
```

As you can see, it only holds the properties and its respective getters and setters, for the fields mentioned in the `EntityDefinition` class.

Now you need your definition to know its custom entity class. This is done by overriding the method `getEntityClass` in your `ExampleDefinition`.

```php
// <plugin root>/src/Core/Content/Example/ExampleDefinition.php
class ExampleDefinition extends EntityDefinition
{
    [...]

    public function getEntityClass(): string
    {
        return ExampleEntity::class;
    }
}
```

That's it. Instead of generic `ArrayEntity` instances, you'll get `ExampleEntity` class instances now if you were to read your data using the repository.

### EntityCollection

Just like the `Entity` class, you do want to create your own `EntityCollection` class.

So create a `ExampleCollection` class in the same directory as your `ExampleDefinition` and `ExampleEntity`. Extending from `Shopware\Core\Framework\DataAbstractionLayer\EntityCollection`, it comes with a method called `getExpectedClass`, which once again returns the fully qualified class name o

… **Truncated.** Full document: https://developer.shopware.com/docs/v6.6/guides/plugins/plugins/framework/data-handling/add-custom-complex-data.md


---

## Adding Data Associations
**Source:** [guides/plugins/plugins/framework/data-handling/add-data-associations.md](https://developer.shopware.com/docs/v6.6/guides/plugins/plugins/framework/data-handling/add-data-associations.md)  
*(Body truncated in this bundle; follow the link for the rest.)*

# Adding Data Associations

## Overview

In this guide you will learn how to add associations to your entities. Every possible kind of association will be covered here, so "One to One", "Many to One" or "One to Many" respectively, and "Many to many" associations.

In every example we'll be working with two example entities, that we want to connect with an association: `FooEntity` and `BarEntity`.

They are **not** created in this guide though!

## Prerequisites

This guide is built upon the [Plugin Base Guide](../../plugin-base-guide), but any plugin will work here. Just note that all examples are using the plugin mentioned above.

In order to add data associations you need an existing entity, as this guide is based on the [Adding custom complex data](add-custom-complex-data) guide, you should have a look at it first.

## Associations

In the following paragraphs, there will be examples for each kind of association. Those are simplified, which means that this guide will not cover how to create entities in the first place. Head over to our guide regarding [Adding custom complex data](add-custom-complex-data).

## Example entity definitions

As already mentioned, this guide will always use the same two example entities for each type of association. They both contain only an ID field, nothing else. For the sake of clarity, here are those example entity definitions:

```php
// <plugin root>/src/Core/Content/Bar/BarDefinition.php
<?php declare(strict_types=1);

namespace Swag\BasicExample\Core\Content\Bar;

use Shopware\Core\Framework\DataAbstractionLayer\EntityDefinition;
use Shopware\Core\Framework\DataAbstractionLayer\Field\Flag\PrimaryKey;
use Shopware\Core\Framework\DataAbstractionLayer\Field\Flag\Required;
use Shopware\Core\Framework\DataAbstractionLayer\Field\IdField;
use Shopware\Core\Framework\DataAbstractionLayer\FieldCollection;

class BarDefinition extends EntityDefinition
{
    public const ENTITY_NAME = 'bar';

    public function getEntityName(): string
    {
        return self::ENTITY_NAME;
    }

    protected function defineFields(): FieldCollection
    {
        return new FieldCollection([
            (new IdField('id', 'id'))->addFlags(new Required(), new PrimaryKey()),
            // Other fields here
        ]);
    }
}
```

```php
// <plugin root>/src/Core/Content/Foo/FooDefinition.php
<?php declare(strict_types=1);

namespace Swag\BasicExample\Core\Content\Foo;

use Shopware\Core\Framework\DataAbstractionLayer\EntityDefinition;
use Shopware\Core\Framework\DataAbstractionLayer\Field\Flag\PrimaryKey;
use Shopware\Core\Framework\DataAbstractionLayer\Field\Flag\Required;
use Shopware\Core\Framework\DataAbstractionLayer\Field\IdField;
use Shopware\Core\Framework\DataAbstractionLayer\FieldCollection;

class FooDefinition extends EntityDefinition
{
    public const ENTITY_NAME = 'foo';

    public function getEntityName(): string
    {
        return self::ENTITY_NAME;
    }

    protected function defineFields(): FieldCollection
    {
        return new FieldCollection([
            (new IdField('id', 'id'))->addFlags(new Required(), new PrimaryKey()),
            // Other fields here
        ]);
    }
}
```

### One to One associations

One to One associations require you to define a foreign key for one of the two connected associations. E.g. the `bar` table has to contain a `foo_id` column, or the other way around: A `bar_id` column in the `foo` table. In this example it will be `foo_id` in the `BarDefinition`.

Let's have a look at the `defineFields` methods of both entity definitions:

```php
// <plugin root>/src/Core/Content/Bar/BarDefinition.php
protected function defineFields(): FieldCollection
{
    return new FieldCollection([
        (new IdField('id', 'id'))->addFlags(new Required(), new PrimaryKey()),
        (new FkField('foo_id', 'fooId', FooDefinition::class))->addFlags(new Required()),
        (new StringField('name', 'name'))->addFlags(new Required()),

        new OneToOneAssociationField('foo', 'foo_id', 'id', FooDefinition::class, false)
    ]);
}
```

Note the new `FkField`, which basically is the mentioned `foo_id` column. Its parameters are the name of the column in your database(snake\_case), the property name in your definition (lowerCamelCase) and the respective definition class.

Additional to that, we've got the `OneToOneAssociationField`. Here you supply the name of the property, which should contain the associated entity, in your respective definition, e.g. in this case we want the `FooDefinition` to appear in the `foo` property of our entity. Following are `foo_id`, which is the name of the column in the database, `id` as the ID column in the referenced database (`foo` in this case) and the referenced definition. The last parameter defines, if you want to automatically load this association every time you load a `bar` entity. We've set this to `false`.

::: warning
Setting autoload to \`true\` on the \`EntityExtension\` and \`EntityDefinition\` will lead to a recursion / out of memory error. If you want to get the association on every load, set autoload to \`true\` only in the \`EntityExtension\`. See also [Add complex data to existing entities](../data-handling/add-complex-data-to-existing-entities#adding-a-field-with-database).
:::

For the sake of completion, here is the respective `defineFields` method of the `FooDefinition`:

```php
// <plugin root>/src/Core/Content/Foo/FooDefinition.php
protected function defineFields(): FieldCollection
{
    return new FieldCollection([
        (new IdField('id', 'id'))->addFlags(new Required(), new PrimaryKey()),
        (new StringField('name', 'name'))->addFlags(new Required()),

        (new OneToOneAssociationField('bar', 'id', 'foo_id', BarDefinition::class, false))
    ]);
}
```

Note, that in here there is no `FkField` necessary.

### One to Many / Many to One

In "One To Many" / "Many To One" associations, you need to define a foreign key column for the "Many to One" side. E.g. your `bar` entity comes with multiple `foo`'s. Therefore, you have to add a `bar_id` column in your `foo` table. In this example it will be `bar_id` in the `FooDefinition`.

Let's have a look at the `defineFields` methods of both entity definitions:

```php
// <plugin root>/src/Core/Content/Bar/BarDefinition.php
protected function defineFields(): FieldCollection
{
    return new FieldCollection([
        (new IdField('id', 'id'))->addFlags(new Required(), new PrimaryKey()),

        new OneToManyAssociationField('foos', FooDefinition::class, 'bar_id')
    ]);
}
```

Next to the `IdField`, you only have to define the `OneToManyAssociationField` in your `BarDefinition`. Its parameters are `foos`, which is the property that will contain all `FooEntity`'s, the class name of `FooDefinition` and the name of the column in the referenced table, which points to the definition itself.

Let's have a look at the `FooDefinition` now:

```php
// <plugin root>/src/Core/Content/Foo/FooDefinition.php
protected function defineFields(): FieldCollection
{
    return new FieldCollection([
        (new IdField('id', 'id'))->addFlags(new Required(), new PrimaryKey()),
        (new FkField('bar_id', 'barId', BarDefinition::class))->addFlags(new Required()),

        new ManyToOneAssociationField('bar', 'bar_id', BarDefinition::class, 'id'),
    ]);
}
```

Next to the `IdField`, you can see a new `FkField`, which is the field for the new `bar_id` column. Its parameters are the name of the column in your database (snake\_case), the property name in your definition (lowerCamelCase) and the respective definition class.

Instead of adding a `OneToManyAssociationField` here now, we have to use the reverse side, which is `ManyToOneAssociationField`. Here you have to apply the name of the property, which will contain the single `BarDefinition` instance, the name of the column, which references to the inverse side entity (`bar_id`), the class of the referenced definition and the name of the ID column in the definition's database table itself. You could add another boolean parameter here, which would define whether or not you want this association to always automatically be added and be loaded. This defaults to `false`, since enabling this could come with performance issues.

### Many to Many associations

`ManyToMany` associations require another, third entity to be available. It will be called `FooBarMappingDefinition` and is responsible for connecting both definitions. It also needs an own database table.

#### Mapping definition

Let's create this one first:

```php
// <plugin root>/src/Core/Content/FooBarMappingDefinition.php
<?php declare(strict_types=1);

namespace Swag\BasicExample\Core\Content;

use Shopware\Core\Framework\DataAbstractionLayer\Field\CreatedAtField;
use Shopware\Core\Framework\DataAbstractionLayer\Field\FkField;
use Shopware\Core\Framework\DataAbstractionLayer\Field\Flag\PrimaryKey;
use Shopware\Core\Framework\DataAbstractionLayer\Field\Flag\Required;
use Shopware\Core\Framework\DataAbstractionLayer\Field\ManyToOneAssociationField;
use Shopware\Core\Framework\DataAbstractionLayer\FieldCollection;
use Shopware\Core\Framework\DataAbstractionLayer\MappingEntityDefinition;
use Swag\BasicExample\Core\Content\Bar\BarDefinition;
use Swag\BasicExample\Core\Content\Foo\FooDefinition;

class FooBarMappingDefinition extends MappingEntityDefinition
{
    public const ENTITY_NAME = 'foo_bar';

    public function getEntityName(): string
    {
        return self::ENTITY_NAME;
    }

    protected function defineFields(): FieldCollection
    {
        return new FieldCollection([
            (new FkField('bar_id', 'barId', BarDefinition::class))->addFlags(new PrimaryKey(), new Required()),
            (new FkField('foo_id', 'fooId', FooDefinition::class))->addFlags(new PrimaryKey(), new Required()),
            new ManyToOneAssociationField('bar', 'bar_id', BarDefinition::class, 'id'),
            new ManyToOneAssociationField('foo', 'foo_id', FooDefinition::class, 'id')
        ]);
    }
}
```

The mapping definition has to extend from the `MappingEntityDefinition`, instead of the `EntityDefinition` like in other entity definitions. The rest is quite the same: Your entity definitions needs an entity name, saved in `ENTITY_NAME`, as well as the method `defineFields`, which has to return a `FieldCollection`.

First of all there are two `FkField`'s. Its parameters are the name of the column in your database(snake\_case), the property name in your definition (lowerCamelCase) and the respective definition class.

Additional to that, you need the `ManyToOneAssociationField`'s. Here you have to supply the name of the property in your entity, which should contain the entries, again the name of the column in the database and the definition again. The last parameter is most likely `id`, which is the column name of the connected table. You could add another boolean parameter here, which would define whether or not you want this association to always automatically be added and be loaded. This defaults to `false`, since enabling this could come with performance issues.

Of course, you have to add both mentioned fields for each definition you want to connect, so two times that is.

#### Adjusting the main definitions

The last thing to do, is to add a `ManyToManyAssociationField` to each of your definitions themselves, like in the following example:

```php
// <plugin root>/src/Core/Content/Bar/BarDefinition.php
protected function defineFields(): FieldCollection
{
    return new FieldCollection([
        (new IdField('id', 'id'))->addFlags(new Required(), new PrimaryKey()),

        new ManyToManyAssociationField(
            'foos',
            FooDefinition::class,
            FooBarMappingDefinition::class,
            'bar_id',
            'foo_id'
        ),
    ]);
}
```

Its parameters are the following:

* `propertyName`: The name of the property in your entity, that will contain the associated entities.
* `referenceDefinition`: 

… **Truncated.** Full document: https://developer.shopware.com/docs/v6.6/guides/plugins/plugins/framework/data-handling/add-data-associations.md


---

## Adding Data Indexer
**Source:** [guides/plugins/plugins/framework/data-handling/add-data-indexer.md](https://developer.shopware.com/docs/v6.6/guides/plugins/plugins/framework/data-handling/add-data-indexer.md)  
*(Body truncated in this bundle; follow the link for the rest.)*

# Adding Data Indexer

## Overview

Data indexer are used to optimize the performance of recurring complex tasks. One good example to understand the benefit of data indexer would be the cheapest price calculation within Shopware. Every product has a `cheapest_price` column in the database which should contain the cheapest price a product has. The calculation of this column can be complex, because a product can have several variants with advanced pricing rules and so on. This makes the calculation more difficult and would take too much time when reading 25 products for a listing. To optimize the performance there is a data indexer that calculates the cheapest price of a product every time the product is updated by the DAL. This means that no new calculation has to be performed when a product is read, and performance during reading is significantly increased. Furthermore data indexer can make use of the [Message queue](../../../../hosting/infrastructure/message-queue) to handle the calculations asynchronously.

## Prerequisites

This guide is built upon the [Plugin base guide](../../plugin-base-guide), but any plugin will work here. Just note that all examples are using the plugin mentioned above. In order to create data indexer you should have read the [Adding custom complex data guide](./add-custom-complex-data).

## Adding an own data indexer

It is possible to add data indexer for your own entities, like the one created in the [Adding custom complex data](./add-custom-complex-data) guide or for existing entities. However, if you want to react on changes of existing entities the preferred way should be subscribing to the events if available. See the [Index data using existing events](#index-data-using-existing-events) section below. To create a new indexer, just create a new class in your plugin:

```php
// <plugin root>/src/Core/Framework/DataAbstractionLayer/Indexing/ExampleIndexer.php
<?php declare(strict_types=1);

namespace Swag\BasicExample\Core\Framework\DataAbstractionLayer\Indexing;

use Doctrine\DBAL\Connection;
use Shopware\Core\Checkout\Customer\CustomerDefinition;
use Shopware\Core\Framework\DataAbstractionLayer\Dbal\Common\IteratorFactory;
use Shopware\Core\Framework\DataAbstractionLayer\EntityRepository;
use Shopware\Core\Framework\DataAbstractionLayer\Event\EntityWrittenContainerEvent;
use Shopware\Core\Framework\DataAbstractionLayer\Indexing\EntityIndexer;
use Shopware\Core\Framework\DataAbstractionLayer\Indexing\EntityIndexingMessage;
use Shopware\Core\Framework\Uuid\Uuid;

class ExampleIndexer extends EntityIndexer
{
    private IteratorFactory $iteratorFactory;

    private EntityRepository $repository;

    private Connection $connection;

    public function __construct(
        IteratorFactory $iteratorFactory,
        EntityRepository $repository,
        Connection $connection
    ) {
        $this->iteratorFactory = $iteratorFactory;
        $this->repository = $repository;
        $this->connection = $connection;
    }

    /**
     * Returns a unique name for this indexer.
     */
    public function getName(): string
    {
        return 'swag.basic.example.indexer';
    }

    /**
     * Called when a full entity index is required. This function should generate a list of message for all records which
     * are indexed by this indexer.
     */

    public function iterate($offset): ?EntityIndexingMessage
    {
        $iterator = $this->iteratorFactory->createIterator($this->repository->getDefinition(), $offset);

        $ids = $iterator->fetch();

        if (empty($ids)) {
            return null;
        }

        return new EntityIndexingMessage(array_values($ids), $iterator->getOffset());
    }

    /**
     * Called when entities are updated over the DAL. This function should react to the provided entity written events
     * and generate a list of messages which has to be processed by the `handle` function over the message queue workers.
     */
    public function update(EntityWrittenContainerEvent $event): ?EntityIndexingMessage
    {
        $updates = $event->getPrimaryKeys(CustomerDefinition::ENTITY_NAME);

        if (empty($updates)) {
            return null;
        }

        return new EntityIndexingMessage(array_values($updates), null, $event->getContext());
    }

    /**
     * Called over the message queue workers. The messages are the generated messages
     * of the `self::iterate` or `self::update` functions.
     */
    public function handle(EntityIndexingMessage $message): void
    {
        $ids = $message->getData();

        if (!$ids) {
            return;
        }

        foreach ($ids as $id) {
            $this->writeLog($id);
        }
    }

    private function writeLog($customerId)
    {
        $this->connection->executeStatement('INSERT INTO `log_entry` (`id`, `message`, `level`, `channel`, `created_at`) VALUES (:id, :message, :level, :channel, now())', [
            'id' => Uuid::randomBytes(),
            'message' => 'Indexed customer with id: ' . $customerId,
            'level' => 1,
            'channel' => 'debug'
        ]);
    }
}
```

With the corresponding service registration:

```xml
<?xml version="1.0" ?>
<container xmlns="http://symfony.com/schema/dic/services"
           xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
           xsi:schemaLocation="http://symfony.com/schema/dic/services http://symfony.com/schema/dic/services/services-1.0.xsd">

    <services>
                <service id="Swag\BasicExample\Core\Framework\DataAbstractionLayer\Indexing\ExampleIndexer">
                    <argument type="service" id="Shopware\Core\Framework\DataAbstractionLayer\Dbal\Common\IteratorFactory"/>
                    <argument type="service" id="customer.repository"/>
                    <argument type="service" id="Doctrine\DBAL\Connection" />
                    <tag name="shopware.entity_indexer"/>
                </service>
    </services>
</container>
```

The indexer service has to be tagged as `shopware.entity_indexer` in order to work.

Let's take a closer look at the functions of the entity indexer class.

* `public function getName(): string`:
  * This function returns the name of the indexer and should be unique. It is used in the `EntityIndexerRegistry` to identify which messages should be handled by which indexer.
* `public function iterate($offset): ?EntityIndexingMessage`:
  * This function is called when a full entity indexing was requested. This is for example the case if the console command `bin/console dal:refresh:index` is used or if a user of the Administration requested an update of all indexes in the settings.
    It should generate a list of messages for all records which are indexed by this indexer. In the example documentation above, the customer entity should be indexed. Therefore, the `Shopware\Core\Framework\DataAbstractionLayer\Dbal\Common\IteratorFactory` is used to fetch customer ids. The offset is used to reduce the amount of data which is processed at once.
* `public function update(EntityWrittenContainerEvent $event): ?EntityIndexingMessage`:
  * This function is called when entities are updated over the DAL. This function should react to the provided entity written events and generate a list of messages which has to be processed by the `handle` function. In the example implementation above, we get all customer identifiers that have been updated by `$updates = $event->getPrimaryKeys(CustomerDefinition::ENTITY_NAME);`. A closer look at the `EntityWrittenContainerEvent` class is also good idea. It is for example possible to filter the updated customer by the updated column. For example if you only need to index customers with a changed firstname. It is always a good idea to filter the entities as much as possible to save performance.
  * The `update()` can also be used to update data that has always to be changed synchronously.
* `public function handle(EntityIndexingMessage $message): void`
  * The `handle()` method handles the messages which were generated in the `self::iterate` or `self::update` function. In the example above a small log entry is written to the database indicating that a customer was indexed. The preferred way to manipulate data here is using the `connection` directly and not to use the DAL. See the section \[Use DAL functionalities in the indexer]\(Use DAL functionalities in the indexer) for more information.

### Handle messages asynchronously or synchronously

By default, all messages which are returned by the `public function update()` function in the indexer are handled synchronously. That means the `handle()` function is called directly after the `update()` function. To handle the messages asynchronously over the [Message queue](../../../../hosting/infrastructure/message-queue) the `EntityIndexingMessage` can be used with different constructor parameters. A closer look at the `EntityIndexingMessage` class shows that it has a fourth parameter named `$forceQueue` which is `false` by default. This parameter can be set to `true` and then the message will be handled asynchronously by the message queue.

### Use DAL functionalities in the indexer

By default, indexing is also active while working with an indexer, which means, that entities that are written over the DAL also trigger `EntityWrittenContainerEvent` events. So the indexers are triggered again. This can lead to an infinite loop. Therefore, the connection should be used directly to alter data in the database. You can find more information about this in the corresponding ADR [when to use plain SQL or the DAL](../../../../../resources/references/adr/2021-05-14-when-to-use-plain-sql-or-dal.md). However, if you want to use the DAL for manipulation data in a data indexer, indexing can be disabled. This can be done by passing adding a flag to the context, as shown in the example below:

```php
public function update(EntityWrittenContainerEvent $event): ?EntityIndexingMessage
{
    $updates = $event->getPrimaryKeys(CustomerDefinition::ENTITY_NAME);

    if (empty($updates)) {
        return null;
    }

    $context = $event->getContext();
    $context->addState(EntityIndexerRegistry::DISABLE_INDEXING);

    return new EntityIndexingMessage(array_values($updates), null, $context);
}
```

## Index data using existing events

There are already a bunch of indexers in shopware that you can use. If you take a look at the `CustomerIndexer` or `CategoryIndexer` classes for example, you will see that they dispatch an event in the `handle` method. This should be used for indexing data of the main entities. Among others, the following indexers already exist and dispatch events that can be used for indexing data:

* `CustomerIndexer`
* `CategoryIndexer`
* `LandingPageIndexer`
* `ProductIndexer`
* `ProductStreamIndexer`
* `PromotionIndexer`
* `RuleIndexer`
* `MediaIndexer`
* `MediaFolderIndexer`
* `MediaFolderConfigurationIndexer`
* `SalesChannelIndexer`
* `BreadcrumpIndexer`

### Subscribe to an indexer event

For this we need a new subscriber. If you are not familiar with a subscriber, have a look at our [Listening to events](../../plugin-fundamentals/listening-to-events) guide. For this example, we just write a new entry to the `log_entry` database table, indicating that a customer was updated.

```php
// <plugin root>/src/Service/Subscriber.php
<?php declare(strict_types=1);

namespace Swag\BasicExample\Service;

use Doctrine\DBAL\Connection;
use Shopware\Core\Checkout\Customer\Event\CustomerIndexerEvent;
use Shopware\Core\Framework\DataAbstractionLayer\Doctrine\MultiInsertQueryQueue;
use Shopware\Core\Framework\Uuid\Uuid;
use Symfony\Component\EventDispatcher\EventSubscriberInterface;

class Subscriber implements EventSubscriberInterface
{
    /**
     * @var Connection
     */
    private Connection $connection;

    public function __construct(Connection $connection)
    {
        $this->connection = $connection;
    }

    public static function getSubscribedEvents(): array
    {


… **Truncated.** Full document: https://developer.shopware.com/docs/v6.6/guides/plugins/plugins/framework/data-handling/add-data-indexer.md


---

## Adding Data Translations
**Source:** [guides/plugins/plugins/framework/data-handling/add-data-translations.md](https://developer.shopware.com/docs/v6.6/guides/plugins/plugins/framework/data-handling/add-data-translations.md)  
# Adding Data Translations

## Overview

In this guide you'll learn how to add translations to entities.

## Prerequisites

This guide is built upon the [Plugin base guide](../../plugin-base-guide), but any plugin will work here. Just note that all examples are using the plugin mentioned above.

In order to create data translations you need an existing entity, as this guide is based on the [Adding custom complex data](add-custom-complex-data) guide, you should have a look at it first.

::: info
Refer to this video on **[Translating your entity](https://www.youtube.com/watch?v=FfqxfQl3I4w)** that deals with data translations. Also available on our free online training ["Shopware 6 Backend Development"](https://academy.shopware.com/courses/shopware-6-backend-development-with-jisse-reitsma).
:::

## Creating the migration

We'll start with creating a new database table. Make sure to use the name of your entity appending `_translation`.

In this guide we'll name our table `swag_example_translation` since our entity is named `swag_example`.

The translation table's columns should be the following:

This is how your migration could look like:

```php
// <plugin root>/src/Migration/Migration1612863838ExampleTranslation.php
<?php declare(strict_types=1);

namespace Swag\BasicExample\Migration;

use Doctrine\DBAL\Connection;
use Shopware\Core\Framework\Migration\MigrationStep;

class Migration1612863838ExampleTranslation extends MigrationStep
{
    public function getCreationTimestamp(): int
    {
        return 1612863838;
    }

    public function update(Connection $connection): void
    {
        $query = <<<SQL
CREATE TABLE IF NOT EXISTS `swag_example_translation` (
    `swag_example_id` BINARY(16) NOT NULL,
    `language_id` BINARY(16) NOT NULL,
    `name` VARCHAR(255),
    `created_at` DATETIME(3) NOT NULL,
    `updated_at` DATETIME(3) NULL,
    PRIMARY KEY (`swag_example_id`, `language_id`),
    CONSTRAINT `fk.swag_example_translation.swag_example_id` FOREIGN KEY (`swag_example_id`)
        REFERENCES `swag_example` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT `fk.swag_example_translation.language_id` FOREIGN KEY (`language_id`)
        REFERENCES `language` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
)
    ENGINE = InnoDB
    DEFAULT CHARSET = utf8mb4
    COLLATE = utf8mb4_unicode_ci;
SQL;
        $connection->executeStatement($query);
    }

    public function updateDestructive(Connection $connection): void
    {
    }
}
```

## Creating the translation entity

The translation is an aggregation to the `ExampleEntity`. Therefore, you should place it into the `<plugin root>/src/Core/Content/Example/Aggregate` directory. In this directory we create a subdirectory called `ExampleTranslation` where we create a new definition for our translation which is called `ExampleTranslation`.

### EntityDefinition class

Now we can start creating our `ExampleTranslationDefinition` which extends from `Shopware\Core\Framework\DataAbstractionLayer\EntityTranslationDefinition`. Special for entity translation is, that we have to override a method called `getParentDefinitionClass` which returns the definition class of our entity we want to translate. In this case it's `ExampleDefinition`.

```php
// <plugin root>/src/Core/Content/Example/Aggregate/ExampleTranslation/ExampleTranslationDefinition.php
<?php declare(strict_types=1);

namespace Swag\BasicExample\Core\Content\Example\Aggregate\ExampleTranslation;

use Shopware\Core\Framework\DataAbstractionLayer\EntityTranslationDefinition;
use Shopware\Core\Framework\DataAbstractionLayer\Field\Flag\Required;
use Shopware\Core\Framework\DataAbstractionLayer\Field\StringField;
use Shopware\Core\Framework\DataAbstractionLayer\FieldCollection;
use Swag\BasicExample\Core\Content\Example\ExampleDefinition;

class ExampleTranslationDefinition extends EntityTranslationDefinition
{
    public const ENTITY_NAME = 'swag_example_translation';

    public function getEntityName(): string
    {
        return self::ENTITY_NAME;
    }

    public function getParentDefinitionClass(): string
    {
        return ExampleDefinition::class;
    }

    protected function defineFields(): FieldCollection
    {
        return new FieldCollection([
            (new StringField('name', 'name'))->addFlags(new Required()),
        ]);
    }
}
```

As you can see, we've implemented a `StringField` for the `name` column, the other fields like the `language_id` will be automatically added by the `EntityTranslationDefinition` since they are base fields of it.

All that's left to do now, is to introduce your `ExampleTranslationDefinition` to Shopware by registering your class in your `services.xml` file and by using the `shopware.entity.definition` tag, because Shopware 6 is looking for definitions this way. Note, that we have to register the translation after the entity we want to translate.

Here's the `services.xml` as it should look like:

```xml
// <plugin root>/src/Resources/config/services.xml
<?xml version="1.0" ?>
<container xmlns="http://symfony.com/schema/dic/services"
           xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
           xsi:schemaLocation="http://symfony.com/schema/dic/services http://symfony.com/schema/dic/services/services-1.0.xsd">

    <services>
        <service id="Swag\BasicExample\Core\Content\Example\ExampleDefinition">
            <tag name="shopware.entity.definition" entity="swag_example" />
        </service>

        <service id="Swag\BasicExample\Core\Content\Example\Aggregate\ExampleTranslation\ExampleTranslationDefinition">
            <tag name="shopware.entity.definition" entity="swag_example_translation" />
        </service>
    </services>
</container>
```

### Entity class

So far we introduced our definition, we can create our `ExampleTranslationEntity`. Our entity has to extend from the `Shopware\Core\Framework\DataAbstractionLayer\TranslationEntity` which comes with some getters and setters for the the `language_id`. We only have to add three properties here, one for the `example_id`, one for the actual name and one for the association to the `ExampleEntity`. All of those properties need a getter and a setter again, so add those too.

Here's our `ExampleTranslationEntity`:

```php
// <plugin root>/src/Core/Content/Example/Aggregate/ExampleTranslation/ExampleTranslationEntity.php
<?php declare(strict_types=1);

namespace Swag\BasicExample\Core\Content\Example\Aggregate\ExampleTranslation;

use Shopware\Core\Framework\DataAbstractionLayer\TranslationEntity;
use Swag\BasicExample\Core\Content\Example\ExampleEntity;

class ExampleTranslationEntity extends TranslationEntity
{
    protected string $exampleId;

    protected ?string $name;

    protected ExampleEntity $example;

    public function getExampleId(): string
    {
        return $this->exampleId;
    }

    public function setExampleId(string $exampleId): void
    {
        $this->exampleId = $exampleId;
    }

    public function getName(): ?string
    {
        return $this->name;
    }

    public function setName(string $name): void
    {
        $this->name = $name;
    }

    public function getExample(): ExampleEntity
    {
        return $this->example;
    }

    public function setExample(ExampleEntity $example): void
    {
        $this->example = $example;
    }
}
```

Now we need our translation definition to know its custom entity class. This is done by overriding the method `getEntityClass` in our `ExampleTranslationDefinition`.

```php
// <plugin root>/src/Core/Content/Example/Aggregate/ExampleTranslation/ExampleTranslationDefinition.php
class ExampleTranslationDefinition extends EntityTranslationDefinition
{
    [...]

    public function getEntityClass(): string
    {
        return ExampleTranslationEntity::class;
    }
}
```

### EntityCollection

As we already know, we should create an `EntityCollection` for our `Entity` too. For entity translations it is the same way as for normal entities.

Our collection class could then look like this:

```php
// <plugin root>/src/Core/Content/Example/Aggregate/ExampleTranslation/ExampleTranslationCollection.php
<?php declare(strict_types=1);

namespace Swag\BasicExample\Core\Content\Example\Aggregate\ExampleTranslation;

use Shopware\Core\Framework\DataAbstractionLayer\EntityCollection;

/**
 * @method void                          add(ExampleTranslationEntity $entity)
 * @method void                          set(string $key, ExampleTranslationEntity $entity)
 * @method ExampleTranslationEntity[]    getIterator()
 * @method ExampleTranslationEntity[]    getElements()
 * @method ExampleTranslationEntity|null get(string $key)
 * @method ExampleTranslationEntity|null first()
 * @method ExampleTranslationEntity|null last()
 */
class ExampleTranslationCollection extends EntityCollection
{
    protected function getExpectedClass(): string
    {
        return ExampleTranslationEntity::class;
    }
}
```

### Main Entity Class

The main entity class, that is the class with the field(s) we are going to translate, must define:

* a `TranslatedField` for the “name” field
* a `TranslationsAssociationField`, with a reference to the ExampleTranslationDefinition

```php
// <plugin root>/src/Core/Content/Example/ExampleDefinition.php
<?php declare(strict_types=1);

namespace Swag\BasicExample\Core\Content\Example;

use ...

class ExampleDefinition extends EntityDefinition
{
    public const ENTITY_NAME = 'example';

    public function getEntityName(): string
    {
        return self::ENTITY_NAME;
    }

    [...]

    protected function defineFields(): FieldCollection
    {
        return new FieldCollection([
            (new IdField('id', 'id'))->addFlags(new PrimaryKey(), new ApiAware(), new Required()),
            (new StringField('not_translated_field', 'notTranslatedField'))->addFlags(new ApiAware()),
            (new TranslatedField('name'))->addFlags(new ApiAware(), new Required()),
            (new TranslationsAssociationField(
                ExampleTranslationDefinition::class,
                'swag_example_id'
            ))->addFlags(new ApiAware(), new Required())
        ]);
    }
}
```

---

---

## Removing Associated Data
**Source:** [guides/plugins/plugins/framework/data-handling/deleting-associated-data.md](https://developer.shopware.com/docs/v6.6/guides/plugins/plugins/framework/data-handling/deleting-associated-data.md)  
# Removing Associated Data

## Overview

This guide explains with some examples on how to delete associated data or most likely how to delete the association to another entity.

## Prerequisites

This example will be built upon the [Plugin base guide](../../plugin-base-guide), so having a look at it will come in handy.

Also, the same subject was already mentioned in our guide about [Replacing associated data](replacing-associated-data).

## Deleting associated data

Since the method differs from each type of association, it will be split from here.
Note, that deleting an association (as in: Removing the association without a replacement) is only possible if the association is **not** required.

E.g. you cannot just remove the `taxId` from a product, since the product always has to be associated to a tax entity.

### Deleting ToOne associations

This section will cover both `OneToOne` as well as `ManyToOne` associations, since they're basically treated the same.
In this example we'll assume that you've assigned a manufacturer to your product.
The manufacturerId is **not** required and thus the association can be removed.

```php
public function removeAssocData(Context $context): void
{
    $this->productRepository->update([
        [
            'id' => 'myProductId',
            'manufacturerId' => null
        ]
    ], $context);
}
```

We're simply setting the ID field of the respective association to `null`.
Now this product won't have a manufacturer assigned anymore.

**Note: If your product is e.g. inheriting from a parent product, the manufacturer will not be unset for the parent product as well.**

### Deleting ManyToMany associations

This section will only cover `ManyToMany` associations.
If you're looking for `OneToMany` associations, head over to the next section. But for now, let's have a look at a `ManyToMany` example.

Assuming you want to un-assign a category from a product, this is how it's done.

```php
public function removeAssocData(Context $context): void
{
    $this->productCategoryRepository->delete([
        [
            'productId' => 'myProductId',
            'categoryId' => 'myCategoryId'
        ]
    ], $context);
}
```

When using the `delete` method, you always need to provide the entities' primary keys in the data array.
Usually, this is just one `id` field, but since we're dealing with a mapping entity here, it owns two primary keys.
This piece of information can be found by looking into the respective entity definition.
Have a look at the [ProductCategoryDefinition](https://github.com/shopware/shopware/blob/v6.3.4.1/src/Core/Content/Product/Aggregate/ProductCategory/ProductCategoryDefinition.php#L37-L41) that we're dealing with here.
It owns two primary keys, `productId` and `categoryId`, and you need to provide both to precisely delete this association.

### Deleting OneToMany associations

The `OneToMany` associations deserve an own section, since they come with a special use case in Shopware 6.
They are sometimes used to create a `ManyToMany` association but with extra data in the mapping table, and sometimes they're just simple `OneToMany` associations.

You need to figure out which kind of `OneToMany` association you're facing here: A normal `OneToMany` association or a hidden `ManyToMany` association?

Let's start with the normal one. Usually, a `OneToMany` association is just the other side of a `ManyToOne` association, whose deletion was already explained in the section about deleting associated data.

Assume you're looking into the [ProductManufacturerDefinition](https://github.com/shopware/shopware/blob/trunk/src/Core/Content/Product/Aggregate/ProductManufacturer/ProductManufacturerDefinition.php), which has a `OneToMany` association to the products.
Deleting this kind of association was already explained in the section about `ToOne` associations.
Instead of working with the repository of the `ProductManufacturerDefinition`, you would be working with the repository from the `ProductDefinition` to remove this association.

```php
public function removeAssocData(Context $context): void
{
    $this->productRepository->update([
        [
            'id' => 'myProductId',
            'manufacturerId' => null
        ]
    ], $context);
}
```

Just set the `manufacturerId` to null and there we go - the `OneToMany` association was removed.
It's the very same code example again.

Unfortunately, it's not always that simple.
As explained above, sometimes `OneToMany` associations are hidden `ManyToMany` associations.
To understand what we mean, have a look at the `media` field in the [Product definition](https://github.com/shopware/shopware/blob/v6.3.4.0/src/Core/Content/Product/ProductDefinition.php#L210-L211).
Technically a product can have multiple medias, and a media can be assigned to multiple products, so this should have been a `ManyToMany` association, right?
Yet, looking at the `media` field in the `ProductDefinition`, you can see that it's a `OneToMany` association.
The second case, that we described earlier in this section, fits here: Technically a `ManyToMany` association, hidden by a `OneToMany` association for the reason mentioned above: There's more data needed for the mapping entity.

If this is the case, you have to treat it just like a `ManyToMany` association in terms of deleting it.
Get the mapping definition's repository, `product_media.repository` in this example, and execute a `delete` on that repository.
This time though, you don't have to use the `productId` and the `mediaId` to delete it, since this kind of definition has its own ID field.
And that's the one you need to use.

So figure out its ID by using the known `productId` and `mediaId` and figure out the mapping entities' ID this way.

```php
public function removeAssocData(Context $context): void
{
    $criteria = new Criteria();
    $criteria->addFilter(new EqualsFilter('productId', 'myProductId'));
    $criteria->addFilter(new EqualsFilter('mediaId', 'myMediaId'));

    $productMediaId = $this->productMediaRepository->searchIds($criteria, $context)->firstId();

    $this->productMediaRepository->delete([
        [
            'id' => $productMediaId
        ]
    ], $context);
}
```

By having a look at the [ProductMediaDefinition](https://github.com/shopware/shopware/blob/v6.3.4.1/src/Core/Content/Product/Aggregate/ProductMedia/ProductMediaDefinition.php), we know that it only has one primary key, which is `id` - and as always when using the `delete` method, this is all you need to provide in the data array.

This way the product will now lose the association to the media entity.
Note: This will **not** delete the media entity itself, just the association between the product and the media entity.

## More interesting topics

* [Replacing associated data](replacing-associated-data)

---

---

## Entities via attributes
**Source:** [guides/plugins/plugins/framework/data-handling/entities-via-attributes.md](https://developer.shopware.com/docs/v6.6/guides/plugins/plugins/framework/data-handling/entities-via-attributes.md)  
*(Body truncated in this bundle; follow the link for the rest.)*

# Entities via attributes

Since Shopware v6.6.3.0, it has been possible to register entities via PHP attributes.
This guide will demonstrate the process.

## Define the entity

First, you need to define your entity.
This is done by creating a new class extending `Entity` and adding the `Entity` attribute to it.
The `name` parameter denotes the name of the entity. It is required and must be unique.

You can also supply the entity collection class to use for this entity, by specifying the `collectionClass` parameter.
The default `EntityCollection` class is used if none is specified.
Note: this is only possible since 6.6.9.0

You have to define a primary key. The primary key is defined by adding the `PrimaryKey` attribute to a property.
In theory, the primary key can be of any type, but it is recommended to use a `UUID`.

```php
<?php declare(strict_types=1);

namespace Examples;

use Shopware\Core\Framework\DataAbstractionLayer\Entity;
use Shopware\Core\Framework\DataAbstractionLayer\Attribute\Entity as EntityAttribute;

#[EntityAttribute('example_entity', collectionClass: ExampleEntityCollection::class)]
class ExampleEntity extends Entity
{
    #[PrimaryKey]
    #[Field(type: FieldType::UUID)]
    public string $id;
}
```

This is the most basic entity definition.
You can add more properties and attributes to the entity.
For example, you can add the `Field` attribute to a property to define the type of the property.

## Register the entity

To register the entity, you have to add this class to the DI container in the `services.xml` file.
This is done by adding the `shopware.entity` tag to the service definition.

```xml
<service id="Shopware\Tests\Integration\Core\Framework\DataAbstractionLayer\fixture\ExampleEntity">
    <tag name="shopware.entity"/>
</service>
```

That's it.
Your entity is registered, and you can read and write data to it over the DAL.
Using the tag, Shopware automatically registers an `EntityDefinition` and `EntityRepository` for the entity.

## Field Types

To define more fields, you typically use the `Field` attribute.
The `Field` attribute requires the `type` parameter, which is the type of the field.
The type can be any of the `FieldType` constants.

```php
<?php declare(strict_types=1);

namespace Examples;

use Shopware\Core\Framework\DataAbstractionLayer\Entity;
use Shopware\Core\Framework\DataAbstractionLayer\Attribute\Field;
use Shopware\Core\Framework\DataAbstractionLayer\Attribute\FieldType;
use Shopware\Core\Framework\DataAbstractionLayer\Attribute\PrimaryKey;
use Shopware\Core\Framework\DataAbstractionLayer\Attribute\Entity as EntityAttribute;

#[EntityAttribute('example_entity')]
class ExampleEntity extends Entity
{
    #[PrimaryKey]
    #[Field(type: FieldType::UUID)]
    public string $id;

    #[Field(type: FieldType::STRING)]
    public string $string;

    #[Field(type: FieldType::TEXT)]
    public ?string $text = null;

    #[Field(type: FieldType::INT)]
    public ?int $int;

    // ...
}
```

All field types are defined in the [`FieldType`](https://github.com/shopware/shopware/blob/trunk/src/Core/Framework/DataAbstractionLayer/Attribute/FieldType.php) class.

### Using field class directly

It is also possible to directly define the field type with any class extending `\Shopware\Core\Framework\DataAbstractionLayer\Field\Field`.
Use the fully qualified class name reference as value for the `type` parameter.

::: note
This feature is available since Shopware 6.6.9.0.
:::

```php
<?php declare(strict_types=1);

namespace Examples;

use Shopware\Core\Framework\DataAbstractionLayer\Entity;
use Shopware\Core\Framework\DataAbstractionLayer\Attribute\Field;
use Shopware\Core\Framework\DataAbstractionLayer\Attribute\FieldType;
use Shopware\Core\Framework\DataAbstractionLayer\Attribute\PrimaryKey;
use Shopware\Core\Framework\DataAbstractionLayer\Attribute\Entity as EntityAttribute;
use Shopware\Core\Framework\DataAbstractionLayer\Field\PriceField;
use Shopware\Core\Framework\DataAbstractionLayer\Pricing\PriceCollection;

#[EntityAttribute('example_entity')]
class ExampleEntity extends Entity
{
    #[PrimaryKey]
    #[Field(type: FieldType::UUID)]
    public string $id;
    
    #[Field(type: PriceField::class)]
    public ?PriceCollection $price = null;

    // ...
}
```

### Special field types

We also provide a list of special field types, which implement a specific behavior.
They have their own PHP attribute class, for example the `AutoIncrement` or `ForeignKey` field.

```php
<?php declare(strict_types=1);

namespace Examples;

use Shopware\Core\Framework\DataAbstractionLayer\Entity;
use Shopware\Core\Framework\DataAbstractionLayer\Attribute\AutoIncrement;
use Shopware\Core\Framework\DataAbstractionLayer\Attribute\Field;
use Shopware\Core\Framework\DataAbstractionLayer\Attribute\FieldType;
use Shopware\Core\Framework\DataAbstractionLayer\Attribute\ForeignKey;
use Shopware\Core\Framework\DataAbstractionLayer\Attribute\PrimaryKey;
use Shopware\Core\Framework\DataAbstractionLayer\Attribute\Entity as EntityAttribute;

#[EntityAttribute('example_entity')]
class ExampleEntity extends Entity
{
    #[PrimaryKey]
    #[Field(type: FieldType::UUID)]
    public string $id;
    
    #[AutoIncrement]
    public int $autoIncrement;

    #[ForeignKey(entity: 'currency')]
    public ?string $foreignKey;
}
```

## JSON fields

If you want to store JSON data in a field with its own validation and serialization logic, you can use the `Serialized` attribute and define its own serializer class:

```php
<?php declare(strict_types=1);

namespace Examples;

use Shopware\Core\Framework\DataAbstractionLayer\Entity;
use Shopware\Core\Framework\DataAbstractionLayer\Attribute\Field;
use Shopware\Core\Framework\DataAbstractionLayer\Attribute\FieldType;
use Shopware\Core\Framework\DataAbstractionLayer\Attribute\PrimaryKey;
use Shopware\Core\Framework\DataAbstractionLayer\Attribute\Serialized;
use Shopware\Core\Framework\DataAbstractionLayer\Attribute\Entity as EntityAttribute;
use Shopware\Core\Framework\DataAbstractionLayer\FieldSerializer\PriceFieldSerializer;
use Shopware\Core\Framework\DataAbstractionLayer\Pricing\PriceCollection;

#[EntityAttribute('example_entity')]
class ExampleEntity extends Entity
{
    #[PrimaryKey]
    #[Field(type: FieldType::UUID)]
    public string $id;
    
    #[Serialized(serializer: PriceFieldSerializer::class)]
    public ?PriceCollection $serialized = null;
}
```

## Custom Fields

To allow custom fields, you can use the `EntityCustomFieldsTrait`.
This gives you some helper methods to easily work with custom field values out of the box.

```php
<?php declare(strict_types=1);

namespace Examples;

use Shopware\Core\Framework\DataAbstractionLayer\Entity;
use Shopware\Core\Framework\DataAbstractionLayer\Attribute\Field;
use Shopware\Core\Framework\DataAbstractionLayer\Attribute\FieldType;
use Shopware\Core\Framework\DataAbstractionLayer\Attribute\PrimaryKey;
use Shopware\Core\Framework\DataAbstractionLayer\Attribute\Entity as EntityAttribute;
use Shopware\Core\Framework\DataAbstractionLayer\EntityCustomFieldsTrait;

#[EntityAttribute('example_entity')]
class ExampleEntity extends Entity
{
    use EntityCustomFieldsTrait;
    
    #[PrimaryKey]
    #[Field(type: FieldType::UUID)]
    public string $id;
}

```

Alternatively you can use the `CustomField` attribute directly, that way you have full control over the custom fields and can add your own helpers.

```php
<?php declare(strict_types=1);

namespace Examples;

use Shopware\Core\Framework\DataAbstractionLayer\Entity;
use Shopware\Core\Framework\DataAbstractionLayer\Attribute\CustomFields;
use Shopware\Core\Framework\DataAbstractionLayer\Attribute\Field;
use Shopware\Core\Framework\DataAbstractionLayer\Attribute\FieldType;
use Shopware\Core\Framework\DataAbstractionLayer\Attribute\PrimaryKey;
use Shopware\Core\Framework\DataAbstractionLayer\Attribute\Entity as EntityAttribute;

#[EntityAttribute('example_entity')]
class ExampleEntity extends Entity
{
    #[PrimaryKey]
    #[Field(type: FieldType::UUID)]
    public string $id;
    
    /**
     * @var array<string, mixed>|null
     */
    #[CustomFields]
    public ?array $customFields = null;
}

```

## API encoding

By default, each field of an entity is not exposed in the API.
To expose a field in the API, you must set the `api` parameter of the `Field` attribute to `true` or specify one of the scopes you want to allow.

```php
<?php declare(strict_types=1);

namespace Examples;

use Shopware\Core\Framework\Api\Context\AdminApiSource;
use Shopware\Core\Framework\Api\Context\SalesChannelApiSource;
use Shopware\Core\Framework\DataAbstractionLayer\Entity;
use Shopware\Core\Framework\DataAbstractionLayer\Attribute\Field;
use Shopware\Core\Framework\DataAbstractionLayer\Attribute\FieldType;
use Shopware\Core\Framework\DataAbstractionLayer\Attribute\PrimaryKey;
use Shopware\Core\Framework\DataAbstractionLayer\Attribute\Entity as EntityAttribute;

#[EntityAttribute('example_entity')]
class ExampleEntity extends Entity
{
    #[PrimaryKey]
    #[Field(type: FieldType::UUID, api: true)]
    public string $id;

    #[Field(type: FieldType::STRING)]
    public string $notExposed;

    #[Field(type: FieldType::STRING, api: true)]
    public string $everywhere;

    #[Field(type: FieldType::STRING, api: [AdminApiSource::class])]
    public string $adminOnly;

    #[Field(type: FieldType::STRING, api: [SalesChannelApiSource::class])]
    public string $storeOnly;
```

## Translated fields

To support Shopware translations for your entity, set the `translated` property of the `Field` attribute to `true`.
This will automatically create a `TranslatedField` for the field and register an `EntityTranslationDefinition` for you.

Additionally, you can define a `Translations` attribute on a property to enable loading of all translations of the entity.
This field needs to be nullable, as by default it will not be loaded, but this allows you to add the `translations` association to the criteria to load all translations at once.

Notice: Properties with the `translated` flag must be nullable.

```php
<?php declare(strict_types=1);

namespace Examples;

use Shopware\Core\Framework\DataAbstractionLayer\Entity;
use Shopware\Core\Framework\DataAbstractionLayer\Attribute\Field;
use Shopware\Core\Framework\DataAbstractionLayer\Attribute\FieldType;
use Shopware\Core\Framework\DataAbstractionLayer\Attribute\PrimaryKey;
use Shopware\Core\Framework\DataAbstractionLayer\Attribute\Translations;
use Shopware\Core\Framework\DataAbstractionLayer\Attribute\Entity as EntityAttribute;

#[EntityAttribute('example_entity')]
class ExampleEntity extends Entity
{
    #[PrimaryKey]
    #[Field(type: FieldType::UUID)]
    public string $id;

    #[Field(type: FieldType::STRING, translated: true)]
    public ?string $string = null;

    /**
     * @var array<string, ArrayEntity>|null
     */
    #[Translations]
    public ?array $translations = null;
}
```

## Required fields

By default, any field that is not type-hinted as `null` is required.
However, you can explicitly mark a field as required by adding the `Required` attribute.
This will automatically add a validation rule to the field.
This is necessary for fields marked as `translated`, as translated fields must be nullable.

```php
<?php declare(strict_types=1);

namespace Examples;

use Shopware\Core\Framework\DataAbstractionLayer\Entity;
use Shopware\Core\Framework\DataAbstractionLayer\Attribute\Field;
use Shopware\Core\Framework\DataAbstractionLayer\Attribute\FieldType;
use Shopware\Core\Framework\DataAbstractionLayer\Attribute\PrimaryKey;
use Shopware\Core\Framework\DataAbstractionLayer\Attribute\Required;
use Shopware\Core\Framework\DataAbstractionLayer\Attribute\Entity as EntityAttribute;

#[EntityAttribute('example_entity')]
class ExampleEntity extends Entity
{
    #[PrimaryKey]
    #[Field(type: FieldType::UUID)]
    public string $id;

    #[Required]
    #[Field(type: FieldType::STRING, translated: true)]
    p

… **Truncated.** Full document: https://developer.shopware.com/docs/v6.6/guides/plugins/plugins/framework/data-handling/entities-via-attributes.md


---

## Field Inheritance
**Source:** [guides/plugins/plugins/framework/data-handling/field-inheritance.md](https://developer.shopware.com/docs/v6.6/guides/plugins/plugins/framework/data-handling/field-inheritance.md)  
# Field Inheritance

## Overview

In this guide you'll learn how to create inherited fields for your entities. Field inheritance allows you to tell Shopware which fields should inherit values from a parent entity.

## Prerequisites

This guide is built upon the [Plugin Base Guide](../../plugin-base-guide), but any plugin will work here. Just note that all examples are using the plugin mentioned above.

You also should have a look at our [Adding custom complex data](add-custom-complex-data) guide, since this guide is built upon it.

## Inherit a field

To start using inheritance, we have to update our definition and database.

1. Make inheritable fields nullable in the database
2. Add the `ParentFkField`, `ParentAssociationField`, `ChildrenAssociationField` in your definition
3. Enable inheritance by overwriting `isInheritanceAware()`
4. Flag fields as inheritable
5. Add getters and setters to the entity class

### Make fields nullable

The first thing we need to do is to make all our fields that we want to make inheritable nullable in our migration. If you lack knowledge about migrations, have a look at our [Database migrations](../../plugin-fundamentals/database-migrations) guide. We also need a 'parent\_id' field for the parent reference.

```sql
ALTER TABLE `swag_example` ADD `parent_id` BINARY(16) NULL;
ALTER TABLE `swag_example` MODIFY `description` VARCHAR(255) NULL;
```

::: code-group

```php [PLUGIN_ROOT/src/Migration/Migration1615363012MakeInheritedColumnsNullable.php]
<?php declare(strict_types=1);

namespace Swag\BasicExample\Migration;

use Doctrine\DBAL\Connection;
use Shopware\Core\Framework\Migration\MigrationStep;

class Migration1615363012MakeInheritedColumnsNullable extends MigrationStep
{
    public function getCreationTimestamp(): int
    {
        return 1615363012;
    }

    public function update(Connection $connection): void
    {
        $query = <<<SQL
            ALTER TABLE `swag_example` 
                ADD `parent_id` BINARY(16) NULL,
                MODIFY `description` VARCHAR(255) NULL;
        SQL;
        
        $connection->executeStatement($query);
    }

    public function updateDestructive(Connection $connection): void
    {
    }
}
```

:::

### Add the ParentFkField and the associations

After we've made all our fields nullable, we still need to add the following fields to our definition: `Shopware\Core\Framework\DataAbstractionLayer\Field\ParentFkField`, `Shopware\Core\Framework\DataAbstractionLayer\Field\ParentAssociationField` and `Shopware\Core\Framework\DataAbstractionLayer\Field\ChildrenAssociationField`.

* `ParentFkField`: Is the foreign key, that references the parent's id.
* `ParentAssociationField`: Field that the DAL knows where to load the parent association from.
* `ChildrenAssociationField`: Field that the DAL knows where to load the children association from.

In default, ParentFkField points to a `parent_id` column in the database. All these fields must refer to our definition by using `self::class`. The `ParentAssociationField` has as its second parameter the referenceField, which in our case is `id`. Below you can find an example of how it should then look.

::: code-group

```php [PLUGIN_ROOT/src/Core/Content/Example/ExampleDefinition.php]
protected function defineFields(): FieldCollection
{
    return new FieldCollection([
        ...

        new ParentFkField(self::class),
        new ParentAssociationField(self::class, 'id'),
        new ChildrenAssociationField(self::class),

        ...
    ]);
}
```

:::

### Allow inheritance

Now we need to enable inheritance by overriding the `isInheritanceAware` method in our definition, which must then return `true`.

::: code-group

```php [PLUGIN_ROOT/src/Core/Content/Example/ExampleDefinition.php]
public function isInheritanceAware(): bool
{
    return true;
}
```

:::

### Flag fields as inheritable

After we've enabled inheritance for our definition, we need to add the`Shopware\Core\Framework\DataAbstractionLayer\Field\Flag\Inherited` flag to all the fields in our definition that should be inherited.

::: code-group

```php [PLUGIN_ROOT/src/Core/Content/Example/ExampleDefinition.php]
protected function defineFields(): FieldCollection
{
    return new FieldCollection([
        (new IdField('id', 'id'))->addFlags(new Required(), new PrimaryKey()),

        new ParentFkField(self::class),
        new ParentAssociationField(self::class, 'id'),
        new ChildrenAssociationField(self::class),

        (new StringField('name', 'name'))->addFlags(new Inherited()),
        (new StringField('description', 'description'))->addFlags(new Inherited()),
        (new BoolField('active', 'active'))->addFlags(new Inherited()),
    ]);
}
```

:::

### Add getters and setters to the entity class

The last thing we need to do is add our new fields to our entity class.

::: code-group

```php [PLUGIN_ROOT/src/Core/Content/Example/ExampleEntity.php]
<?php declare(strict_types=1);

namespace Swag\BasicExample\Core\Content\Example;

use Shopware\Core\Framework\DataAbstractionLayer\Entity;
use Shopware\Core\Framework\DataAbstractionLayer\EntityIdTrait;

class ExampleEntity extends Entity
{
    ...

    protected ?self $parent = null;

    protected ?string $parentId;

    protected ?ExampleCollection $children = null;

    ...

    public function getParent(): ?ExampleEntity
    {
        return $this->parent;
    }

    public function setParent(ExampleEntity $parent): void
    {
        $this->parent = $parent;
    }

    public function getParentId(): ?string
    {
        return $this->parentId;
    }

    public function setParentId(?string $parentId): void
    {
        $this->parentId = $parentId;
    }

    public function getChildren(): ?ExampleCollection
    {
        return $this->children;
    }

    public function setChildren(ExampleCollection $children): void
    {
        $this->children = $children;
    }
}
```

:::

## Translations

This concept also supports translations. Given a parent/child entity with an inherited language (de-CH *inherits from* de-DE), the inheritance system will try to look up the values in following order:

1. Child (de-CH)
2. Child (de-DE)
3. Parent (de-CH)
4. Parent (de-DE)

If an inheritance is not found, the next translation in the chain above will be used.

### Enable translation inheritance

Assuming our definition is already aware of inheritance, we have to update our definition and add the `Inherited` flag to our translated fields and the translation association.

::: code-group

```php [PLUGIN_ROOT/src/Core/Content/Example/ExampleDefinition.php]
(new TranslatedField('name'))->addFlags(new Inherited()),
(new TranslationsAssociationField(ExampleTranslationDefinition::class))->addFlags(new Inherited()),
```

:::

## Association inheritance

Association inheritance allows you to inherit associations from a parent entity.
To make an association inheritable, you need to add the `Inherited` flag to the association field in your definition.

::: code-group

```php [PLUGIN_ROOT/src/Core/Content/Example/ExampleDefinition.php]
protected function defineFields(): FieldCollection
{
    return new FieldCollection([
        ...
        (new FkField('tax_id', 'taxId', TaxDefinition::class))->addFlags(new Inherited()),
        (new ManyToOneAssociationField('tax', 'tax_id', TaxDefinition::class, 'id'))->addFlags(new Inherited()),
        ...
    ]);
}
```

:::

We then need to add the foreign key column to our migration:

::: code-group

```php [PLUGIN_ROOT/src/Migration/Migration1615363013AddInheritedAssociation.php]
<?php declare(strict_types=1);

namespace Swag\BasicExample\Migration;

use Doctrine\DBAL\Connection;
use Shopware\Core\Framework\Migration\InheritanceUpdaterTrait;
use Shopware\Core\Framework\Migration\MigrationStep;

class Migration1615363013AddInheritedAssociation extends MigrationStep
{
    use InheritanceUpdaterTrait;
    
    public function getCreationTimestamp(): int
    {
        return 1615363013;
    }

    public function update(Connection $connection): void
    {
        $query = <<<SQL
            ALTER TABLE `swag_example` 
                ADD `tax_id` BINARY(16) NULL,
                ADD CONSTRAINT `fk.swag_example.tax_id` FOREIGN KEY (`tax_id`)
                    REFERENCES `tax` (`id`) ON DELETE CASCADE ON UPDATE CASCADE'
        SQL;
        
        $connection->executeStatement($query);
        
        $this->updateInheritance($connection, 'swag_example', 'tax');
    }

}
```

:::

### "Inheritance columns"

Note the use of the `updateInheritance` method in the migration.
This method is used to create "inheritance columns" in the database.
These columns are used internally by the DAL to store the inherited references.
Those columns need to be present in the database for the inheritance system to work correctly.
In those columns, the concrete reference values to perform the join on are stored.
In the case of `ToMany` associations, the ID stored in the column is the ID of the base entity (parent ID if the association is inherited, child ID if not).
For `ToOne` associations like this example, the ID stored in the column is the ID of the entity that is referenced by the association.

This additional column is needed because of two reasons:

1. To allow overriding the association in the child entity with null values, which would otherwise not be possible.
2. To improve performance by avoiding additional queries to load the parent entity when the association is inherited.

Those columns are not visible in the entity definition or entity class and cannot be accessed directly. They are only used internally by the DAL.

---

---

## Reading Data
**Source:** [guides/plugins/plugins/framework/data-handling/reading-data.md](https://developer.shopware.com/docs/v6.6/guides/plugins/plugins/framework/data-handling/reading-data.md)  
*(Body truncated in this bundle; follow the link for the rest.)*

# Reading Data

## Overview

In this guide you will learn how to properly fetch data from the database in your plugin or for core contributions. This will also cover how to add filters to only find specific data, and how to aggregate your desired data. Unlike most other Symfony applications, Shopware 6 uses no ORM but rather a thin Data Abstraction Layer. It's worth getting used to the "DAL", as you might stumble upon this term every now and then in the Shopware universe.

## Prerequisites

Since this guide is built upon the plugin base guide [Plugin base guide](../../plugin-base-guide), you might want to have a look at it. Furthermore, the guide about [Dependency injection](../../plugin-fundamentals/dependency-injection) will come in handy, since you need to know how to inject a service using the DI container.\
You also might want to have a look at the concept behind the [Data abstraction layer concept](../../../../../concepts/framework/data-abstraction-layer) first to get a better grasp of how it works.

## Reading data

Let's get started with examples on how to read data now. This example will be about reading **products**, but adjusting them for other data is easy, you'll see what we mean.

### Injecting the repository

Dealing with the Data Abstraction Layer is done by using the automatically generated repositories for each entity, such as a product. This means, that you have to inject the repository into your service first.

The repository's service name follows this pattern: `entity_name.repository`\
For products this then would be `product.repository`, so let's do this.

```xml
// SwagBasicExample/src/Resources/config/services.xml
<?xml version="1.0" ?>
<container xmlns="http://symfony.com/schema/dic/services"
           xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
           xsi:schemaLocation="http://symfony.com/schema/dic/services http://symfony.com/schema/dic/services/services-1.0.xsd">

    <services>
        <service id="Swag\BasicExample\Service\ReadingData" >
            <argument type="service" id="product.repository"/>
        </service>
    </services>
</container>
```

And here's the respective class including its constructor:

```php
// SwagBasicExample/src/Service/ReadingData.php
<?php declare(strict_types=1);

namespace Swag\BasicExample\Service;

use Shopware\Core\Framework\DataAbstractionLayer\EntityRepository;

class ReadingData
{
    private EntityRepository $productRepository;

    public function __construct(EntityRepository $productRepository)
    {
        $this->productRepository = $productRepository;
    }
}
```

So we registered a custom service called `ReadingData` and applied the repository as a constructor parameter. If you want to fetch data for another entity, just switch the `id` in the `services.xml` to whatever repository you need, e.g. `order.repository` for orders.

### Using the repository

Now that you've injected the repository into your service, you can start using it. First of all, for the following examples you'll need two more imports:

```php
use Shopware\Core\Framework\Context;
use Shopware\Core\Framework\DataAbstractionLayer\Search\Criteria;
```

Let's start with the most basic read action now:

```php
public function readData(Context $context): void
{
    $products = $this->productRepository->search(new Criteria(), $context);
}
```

This example assumes that you're using / calling a method called `readData` on your previously created service. That's it already. It will read some products without any special filtering. The result of the `search` method will be an instance of an `EntitySearchResult`, which then contains the collection of products.

The `$context` is usually passed through to your method, starting from a controller or an event.

#### Filtering

Now let's get into actually filtering your search result to get more precise results.

**Searching for IDs**

Often you have an ID from an entity and you just want to find the whole dataset related to that ID, so here you go:

```php
public function readData(Context $context): void
{
    $product = $this->productRepository->search(new Criteria([$myId]), $context)->first();
}
```

This will just find the product with the ID `$myId` or it will return `null`, if no product was found with that ID. But how does that work now?

The `Criteria` object accepts an array of IDs to search for as a constructor parameter. This means, that you could apply more than just one ID here.

The `search` method will then return a `EntitySearchResult`, which contains the according entity collection of all products. Even though just one product can be matched here, the method will always return a collection, which then contains your single product. Therefore we're calling `first()` to get the actual entity, and not the collection as a return.

**Searching for any other field**

While searching for an ID will do the trick quite often, you might want to search a product by e.g. its name instead.

In order to do this, you can apply filters to the `Criteria` object, such as an `EqualsFilter`, which accepts a field name and the value to search for. You can find the `EqualsFilter` here: `Shopware\Core\Framework\DataAbstractionLayer\Search\Filter\EqualsFilter`

```php
public function readData(Context $context): void
{
    $criteria = new Criteria();
    $criteria->addFilter(new EqualsFilter('name', 'Example name'));

    $products = $this->productRepository->search($criteria, $context);
}
```

This example will search for all products with the name `Example name` and return an `EntitySearchResult` containing all matched products. Since the `EntitySearchResult` is extending the `EntityCollection`, which is iterable, you could just iterate over the results using a `foreach`.

All available fields can be found in the entities' respective definition, `ProductDefinition` for this example.

#### Combining filters

What would you do now if you are fine with a product which has either the ID "X" OR the mentioned name "Example name"?

For this case, you can combine filters using the `OrFilter` or the `AndFilter`, or the `NandFilter`, etc.

Let's just build the example mentioned above:

```php
public function readData(Context $context): void
{
    $criteria = new Criteria();
    $criteria->addFilter(new OrFilter([
        new EqualsFilter('id', 'Your example ID'),
        new EqualsFilter('name', 'Example name')
    ]));

    $products = $this->productRepository->search($criteria, $context);
}
```

So now you'll find all products, that either have the mentioned `id` OR the mentioned `name`. The `OrFilter` can be found here: `Shopware\Core\Framework\DataAbstractionLayer\Search\Filter\OrFilter`.

You can find an example for each of the available filters in our [DAL reference about filters](../../../../../resources/references/core-reference/dal-reference/filters-reference).

#### Post filters

Later in this guide you will learn about aggregated data. Sometimes you want to filter the result returned by the DAL, but you don't want those filters to apply to the aggregation result.

E.g.: Fetch all products, whose name is `Example product`, but also return the total amount of products available.

In that case, you can just use the `addPostFilter` instead of `addFilter`:

```php
public function readData(Context $context): void
{
    $criteria = new Criteria();
    $criteria->addPostFilter(new EqualsFilter('name', 'Example name'));

    $products = $this->productRepository->search($criteria, $context);
}
```

This example does not contain any aggregation, since they're only explained later.

**Other filters**

There is more than just an `EqualsFilter`, which is the SQL equivalent of `WHERE fieldX = valueX`. You can find all other filters either on [GitHub](https://github.com/shopware/shopware/tree/trunk/src/Core/Framework/DataAbstractionLayer/Search/Filter) or in our [filters reference](../../../../../resources/references/core-reference/dal-reference/filters-reference) with explanation.

#### Associations

Of course associations to other entities are also possible in Shopware 6. If you, for example, want to load all product-reviews, which is an entity itself, related to the product you have found, you can do so by adding associations to the criteria object.

```php
public function readData(Context $context): void
{
    $criteria = new Criteria();
    $criteria->addFilter(new EqualsFilter('name', 'Example name'));
    $criteria->addAssociation('productReviews');

    $products = $this->productRepository->search($criteria, $context);
}
```

Just like the available entity fields, you can find all possible associations in the entity definition.

Also worth to mention is the fact, that you can chain the association key. E.g. a product-review has another association to the customer, who created that review. If you want access to both the review itself, as well as the customer, you can just write the association like that:

```php
public function readData(Context $context): void
{
    $criteria = new Criteria();
    $criteria->addFilter(new EqualsFilter('name', 'Example name'));
    $criteria->addAssociation('productReviews.customer');

    $products = $this->productRepository->search($criteria, $context);
}
```

**Filter associations**

Yes, this is doable. You can apply filters to an association. E.g. "Add all product reviews to the product, whose rating is above 4 stars.".

For this we can use `getAssociation` instead, which basically returns its own `Criteria` object, on which you can apply a filter.

```php
public function readData(Context $context): void
{
    $criteria = new Criteria();
    $criteria->addFilter(new EqualsFilter('name', 'Example name'));

    $criteria->getAssociation('productReviews')->addFilter(new RangeFilter('points', [
        RangeFilter::GTE => 4
    ]));

    $product = $this->productRepository->search($criteria, $context)->first();
}
```

Once again: Note, that we used `getAssociation` here now instead of `addAssociation`. Also you need the `RangeFilter`, which can be found here: `Shopware\Core\Framework\DataAbstractionLayer\Search\Filter\RangeFilter`

Another example to clarify what's going on here:

```php
public function readData(Context $context): void
{
    // This will always return the product with the given name, no matter if it has a review with 4 or more stars.
    // But only matching reviews are added to the dataset then.
    $criteria->getAssociation('productReviews')->addFilter(new RangeFilter('points', [
        RangeFilter::GTE => 4
    ]));
    $product = $this->productRepository->search($criteria, $context)->first();

    // This will only return products, whose name matches AND which have at least one rating of 4 stars or more
    $criteria->addAssociation('productReviews');
    $criteria->addFilter(new RangeFilter('productReviews.points', [
        RangeFilter::GTE => 4
    ]));
    $product = $this->productRepository->search($criteria, $context)->first();
}
```

The first will return your product, that you found anyway, and add all matching `productReview` associations. The latter will just return your product, if it has at least one matching review.

**Reading mapping entities**

Every `ManyToMany` association comes with a mapping entity, such as the `ProductCategoryDefinition`. It's important to know, that you **cannot** read those mapping entities using the `search()` method.

The following example will **not** work:

```php
public function readData(Context $context): void
{
    $criteria = new Criteria();

    // It's the product_category.repository here
    $result = $this->productCategoryRepository->search($criteria, $context);
}
```

Since mapping entities just consist of two primary keys, there is no need to search for the "full entity" via `search`. It will suffice to use `searchIds` instead, which will return the IDs - and that's all there is in a mapping entity.

#### Aggregations

Of course you can also aggregate your data. Just like filters and 

… **Truncated.** Full document: https://developer.shopware.com/docs/v6.6/guides/plugins/plugins/framework/data-handling/reading-data.md


---

## Replacing Associated Data
**Source:** [guides/plugins/plugins/framework/data-handling/replacing-associated-data.md](https://developer.shopware.com/docs/v6.6/guides/plugins/plugins/framework/data-handling/replacing-associated-data.md)  
# Replacing Associated Data

## Overview

This short guide will give you an example on how to replace associated `ToMany` data using our Data Abstraction Layer.

## Prerequisites

Having read our guide about [Writing data](writing-data) is mandatory to understand the next few steps here. Other than that, the default prerequisites apply here as well: A running Shopware 6 instance and full access to the files.

The examples mentioned here are built upon the [Plugin base guide](../../plugin-base-guide). If you don't know how to create a plugin or how to use the code examples here in the first place, the plugin base guide is a good way to start.

## Replacing data

So let's start with the main issue going on here. Let's imagine you've created a product using our previously mentioned guide about [Writing data](writing-data) and you have assigned a category to it. Unfortunately you made a mistake, since this was the wrong category to be assigned and you want another category to be assigned instead.

### A wrong example

The following example will show you how **not** to do it. It's assuming that you've previously assigned the category `Old category` with the ID `oldId` to the product.

```php
public function replaceData(Context $context): void
{
    $this->productRepository->update([
        [
            'id' => 'myProductId',
            'categories' => [
                [
                    'id' => 'newCategoryId'
                ]
            ]
        ]
    ], $context);
}
```

You're assigning an array of category arrays to the product with the ID `myProductId`. This array of category arrays does **not** contain the old category ID, only the new one. Thus, the old category association should be removed and instead the new category should be assigned, right?

Well, this is **not** how it works. Using a write operation will **not** delete data, but only add up more data. The result of the example above will be a product with two categories assigned instead.

### The right example

The right way to do it is to delete the category association first, only to then re-assign a new category. Let's take a look at the deletion part first, since this is where most people struggle.

The product categories are a `ManyToMany` association and thus come with a mapping table, and a custom entity. You can find the entity definition for the association [here](https://github.com/shopware/shopware/blob/trunk/src/Core/Content/Product/Aggregate/ProductCategory/ProductCategoryDefinition.php).

In order to delete it, we once again need its repository. The name for the entity can be found in the definition, to be precise inside of the `getEntityName` method.

So let's inject this repository into our class called `ReplacingData`:

```xml
// SwagBasicExample/src/Resources/config/services.xml
<?xml version="1.0" ?>
<container xmlns="http://symfony.com/schema/dic/services"
           xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
           xsi:schemaLocation="http://symfony.com/schema/dic/services http://symfony.com/schema/dic/services/services-1.0.xsd">

    <services>
        <service id="Swag\BasicExample\Service\ReplacingData" >
            <argument type="service" id="product.repository"/>
            <argument type="service" id="product_category.repository"/>
        </service>
    </services>
</container>
```

Afterwards, you can just use the `delete` method on the repository, just like you did before in the [Writing data](writing-data) guide.

```php
public function replaceData(Context $context): void
{
    $this->productCategoryRepository->delete([
        [
            'productId' => 'myProductId',
            'categoryId' => 'oldId'
        ]
    ], $context);
}
```

Now the association to the old category was removed and you can now use the code above to add the new category instead.

```php
public function replaceData(Context $context): void
{
    $productId = 'myProductId';

    $this->productCategoryRepository->delete([
        [
            'productId' => $productId,
            'categoryId' => 'oldCategoryId'
        ]
    ], $context);

    $this->productRepository->update([
        [
            'id' => $productId,
            'categories' => [
                [
                    'id' => 'newCategoryId'
                ]
            ]
        ]
    ], $context);
}
```

And that's it, you've successfully deleted one association and then replaced it by another. This works for both `ManyToMany`, as well as `OneToMany` associations.

### ToOne associations

Replacing `OneToOne` or `ManyToOne` associations works just like expected via an `update` call, e.g. for the tax of a product:

```php
public function replaceData(Context $context): void
{
    $this->productRepository->update([
        [
            'id' => 'myProductId',
            'taxId' => 'newTaxId'
        ]
    ], $context);
}
```

This works as expected.

## More interesting topics

* [Deleting associated data](deleting-associated-data)

---

---

## Using Database Events
**Source:** [guides/plugins/plugins/framework/data-handling/using-database-events.md](https://developer.shopware.com/docs/v6.6/guides/plugins/plugins/framework/data-handling/using-database-events.md)  
# Using Database Events

## Overview

Events are the easiest way to extend the DataAbstractionLayer. Every entity comes with a set of events which will be dispatched in various situations.

All events are nested into one container event so that your subscriber should only get called once for e.g. a search request instead of dispatching the event 30 times.

## Prerequisites

This guide is built upon the [Plugin base guide](../../plugin-base-guide), but any plugin will work here. Just note that all examples are using the plugin mentioned above.

Furthermore you should have a look at our [Listening to events](../../plugin-fundamentals/listening-to-events) guide since we are subscribing to events in this guide.

## General event overview

The events below are dispatched during certain DAL operations, they are not necessarily associated with a particular entity, rather they are triggered with batches of commands.

| Event                                                                   | Description                                                                                        |
|:------------------------------------------------------------------------|:---------------------------------------------------------------------------------------------------|
| `Shopware\Core\Framework\DataAbstractionLayer\Event\EntityWriteEvent`   | Before a batch of commands has been written to storage. Written means inserted, updated or deleted |
| `Shopware\Core\Framework\DataAbstractionLayer\Event\EntityDeleteEvent`  | Before a batch of delete commands has been executed                                                |

### `Shopware\Core\Framework\DataAbstractionLayer\Event\EntityWriteEvent`

This event allows you to hook into the process of writing an entity. This includes creating, updating, and deleting entities. You have the possibility to execute the code before and after the entity is written via the "success" and "error" callbacks. You can call the `addSuccess` or `addError` methods with any PHP callable.

You can use this event to capture state, perform actions, and sync data after an entity is written. It could be used, for example, to synchronize images to a CDN when they are written, updated, or deleted. This event is useful when you need the before state of the entity. For example, the old filename.

Below is an example subscriber listening to the generic entity write event and logging the ID's of the written entities.

```php
// <plugin root>/src/Subscriber/EntityWriteSubscriber.php
<?php declare(strict_types=1);

namespace Swag\BasicExample\Subscriber;

use Symfony\Component\EventDispatcher\EventSubscriberInterface;
use Shopware\Core\Framework\DataAbstractionLayer\Event\EntityWriteEvent;
use Shopware\Core\Content\Cms\CmsPageDefinition;
use Psr\Log\LoggerInterface;
use Shopware\Core\Framework\DataAbstractionLayer\Write\Command\WriteCommand;

class EntityWriteSubscriber implements EventSubscriberInterface
{

    public function __construct(private readonly LoggerInterface $logger)
    {
    }

    public static function getSubscribedEvents()
    {
        return [
            EntityWriteEvent::class => 'beforeWrite',
        ];
    }

    public function beforeWrite(EntityWriteEvent $event)
    {
        //get the ids of any cms entities about to be written/updated/deleted
        //this event is triggered for batches of entities, so you can use this to filter for specific entities
        $ids = $event->getIds(CmsPageDefinition::ENTITY_NAME);
        
        //get ids of all entities to be written, regardless of type
        $ids = $event->getIds();
        
        //you can also fetch the payloads (DeleteCommand's do not have payloads)
        $payloads = array_map(fn (WriteCommand $command) => $command->getPayload(), $event->getCommands());
        
        //or for a specific entity type
        $payloads = array_map(fn (WriteCommand $command) => $command->getPayload(), $event->getCommandsForEntity(CmsPageDefinition::ENTITY_NAME));
                
        
        $event->addSuccess(function () use ($ids) {
            //the entities have now been successfully written
            
            $this->logger->info(sprintf('Entities with ids: "%s" were written', implode(', ', $ids)));
        });
        
        $event->addError(function () use ($ids) {
            //the entities failed to write, you can write a log, send an e-mail, or anything else.
            $this->logger->critical(sprintf('Entities with ids: "%s" were not written', implode(', ', $ids)));
        });
    }
}
```

After creating the event subscriber, you have to register it. If you don't know how it is done, then refer to the [Listening to events](../../plugin-fundamentals/listening-to-events) guide.

### `Shopware\Core\Framework\DataAbstractionLayer\Event\EntityDeleteEvent`

This event allows you to hook into the process of removing an entity. You have the possibility to execute the code before and after the entity is removed via the "success" and "error" callbacks. You can call the `addSuccess` or `addError` methods with a closure.

You can use this event to capture state and perform actions after an entity is removed. For example, you could collect the entity name before it is deleted, then after it is deleted, use the name to remove the respective data from a third-party system via an API call.

Below is an example subscriber listening to the generic entity delete event, filtering for CMS page deletions, and then performing a different action based on whether the delete was successful or not.

```php
// <plugin root>/src/Subscriber/DeleteSubscriber.php
<?php declare(strict_types=1);

namespace Swag\BasicExample\Subscriber;

use Symfony\Component\EventDispatcher\EventSubscriberInterface;
use Shopware\Core\Framework\DataAbstractionLayer\Event\EntityDeleteEvent;
use Shopware\Core\Content\Cms\CmsPageDefinition;

class DeleteSubscriber implements EventSubscriberInterface
{
    public static function getSubscribedEvents()
    {
        return [
            EntityDeleteEvent::class => 'beforeDelete',
        ];
    }

    public function beforeDelete(EntityDeleteEvent $event)
    {
        //get the ids of any cms entities about to be deleted
        //this event is triggered for batches of entities, so you can use this to filter for specific entities
        $ids = $event->getIds(CmsPageDefinition::ENTITY_NAME);
        
        $event->addSuccess(function () use ($ids) {
            //the entities have now been successfully deleted
            
            $this->cache->purge($ids);
        });
        
        $event->addError(function () use ($ids) {
            //the entities failed to delete, you can write a log, send an e-mail, or anything else.
        });
    }
}
```

After creating the event subscriber, you have to register it. If you don't know how it is done, then refer to the [Listening to events](../../plugin-fundamentals/listening-to-events) guide.

## Entity event overview

The events below are dispatched for every entity in Shopware. The first part before the dot (.) equals your entity name. The examples are based on the `product` entity.

| Event | Description |
| :--- | :--- |
| `product.written` | After the data has been written to storage |
| `product.deleted` | After the data has been deleted in storage |
| `product.loaded` | After the data has been hydrated into objects |
| `product.search.result.loaded` | After the search returned data |
| `product.aggregation.result.loaded` | After the aggregations have been loaded |
| `product.id.search.result.loaded` | After the search for ids only has been finished |

### product.written

The written event refers to `Shopware\Core\Framework\DataAbstractionLayer\Event\EntityWrittenEvent` and provides the following information:

* The reference class of the written definition
* The data that was written
* The context the data was written with
* The list of affected primary keys
* The list of errors if there are any

### product.deleted

The deleted event refers to `Shopware\Core\Framework\DataAbstractionLayer\Event\EntityDeletedEvent` and provides the following information:

* The reference class of the deleted definition
* The context the data was deleted with
* The list of affected primary keys
* The list of errors if there are any

### product.loaded

The loaded event refers to `Shopware\Core\Framework\DataAbstractionLayer\Event\EntityLoadedEvent` and provides the following information:

* The reference class of the loaded definition
* The context the data was loaded with
* The list of hydrated entities

### product.search.result.loaded

The loaded event refers to `Shopware\Core\Framework\DataAbstractionLayer\Event\EntitySearchResultLoadedEvent` and provides the following information:

* The reference class of the loaded definition
* The context the data was loaded with
* The search result object including count, criteria and hydrated entities

### product.aggregation.result.loaded

The loaded event refers to `Shopware\Core\Framework\DataAbstractionLayer\Event\EntityAggregationResultLoadedEvent` and provides the following information:

* The results of the aggregation
* The criteria the data was searched with
* The context the data was loaded with

### product.id.search.result.loaded

The loaded event refers to `Shopware\Core\Framework\DataAbstractionLayer\Event\EntityIdSearchResultLoadedEvent` and provides the following information:

* The reference class of the loaded definition
* The context the data was loaded with
* The search result object including count, criteria, and list of ids

## Event classes

All of stock entities come with their own event class. To keep the example of the product entity, you've got the `ProductEvents` class which is a list of constants to provide auto-completion and in case we are changing event names, you are covered.

The example below shows you how to use the constants in your event subscriber:

```php
// <plugin root>/src/Subscriber/ProductSubscriber.php
<?php declare(strict_types=1);

namespace Swag\BasicExample\Subscriber;

use Shopware\Core\Content\Product\ProductEvents;
use Shopware\Core\Framework\DataAbstractionLayer\Event\EntityLoadedEvent;
use Shopware\Core\Framework\DataAbstractionLayer\Event\EntityWrittenEvent;
use Symfony\Component\EventDispatcher\EventSubscriberInterface;

class ProductSubscriber implements EventSubscriberInterface
{
    public static function getSubscribedEvents()
    {
        return [
            ProductEvents::PRODUCT_LOADED_EVENT => 'onLoad',
            ProductEvents::PRODUCT_WRITTEN_EVENT => 'afterWrite',
        ];
    }

    public function onLoad(EntityLoadedEvent $event)
    {
        ...
    }

    public function afterWrite(EntityWrittenEvent $event)
    {
        ...
    }
```

After creating the event subscriber, you have to register it. If you don't know how that's done, head over to our guide about [Listening to events](../../plugin-fundamentals/listening-to-events).

Here's our `services.xml`:

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

---

---

## Using Flags
**Source:** [guides/plugins/plugins/framework/data-handling/using-flags.md](https://developer.shopware.com/docs/v6.6/guides/plugins/plugins/framework/data-handling/using-flags.md)  
# Using Flags

## Overview

In this guide you'll learn how to use flags of the DAL but this guide will not explain all flags and its purpose.

## Prerequisites

In order to use flags in your entities for your plugin, you first need a plugin as base. Therefore, you can refer to the [Plugin Base Guide](../../plugin-base-guide).

You should also have a look at the [Flags reference](../../../../../resources/references/core-reference/dal-reference/flags-reference) to understand what each flag is used for. Furthermore you should know how entities work, therefore you can head over to our [Adding custom complex data](add-custom-complex-data) guide.

## Using flags

You have to add the flags to fields in your definition in order to use them. You can even modify the field's flags by creating entity extensions. It is also possible to use multiple flags comma separated.

### Single flag example

```php
(new IdField('id', 'id'))->addFlags(new PrimaryKey())
```

### Multiple flags example

```php
(new IdField('id', 'id'))->addFlags(new PrimaryKey(), new Required())
```

### Overwrite default flags

You can also use setFlags to overwrite the Default Flags which could be set. Be careful to not overwrite essential flags for a specific field.

```php
(new IdField('id', 'id'))->setFlags(new Required())
```

## Example entity

Below you can find an example implementation in an entity where we use flags.

```php
// <plugin root>/src/Core/Content/Example/ExampleDefinition.php
<?php declare(strict_types=1);

namespace Swag\BasicExample\Core\Content\Example;

use Shopware\Core\Framework\DataAbstractionLayer\EntityDefinition;
use Shopware\Core\Framework\DataAbstractionLayer\FieldCollection;

class ExampleDefinition extends EntityDefinition
{
    public const ENTITY_NAME = 'swag_example';

    public function getEntityName(): string
    {
        return self::ENTITY_NAME;
    }

    protected function defineFields(): FieldCollection
    {
        return new FieldCollection([
            (new IdField('id', 'id'))->addFlags(new Required(), new PrimaryKey()),
            (new StringField('name', 'name')),
            (new StringField('description', 'description')),
            (new BoolField('active', 'active'))
        ]);
    }
}
```

---

---

## Versioning Entities
**Source:** [guides/plugins/plugins/framework/data-handling/versioning-entities.md](https://developer.shopware.com/docs/v6.6/guides/plugins/plugins/framework/data-handling/versioning-entities.md)  
# Versioning Entities

## Overview

In this guide you will learn how to version your entities.
The entity versioning system in Shopware gives you the opportunity to create multiple versions of an entity, which could be used to save drafts for example.
Learn more about the versioning concept [here](../../../../../concepts/framework/data-abstraction-layer#versioning).

## Prerequisites

In order to add your own versioned entities for your plugin, you first need a plugin as base.
Therefore, you can refer to the [Plugin Base Guide](../../plugin-base-guide).

Furthermore, you should have a look at our [Adding custom complex data](add-custom-complex-data) guide, since this guide is built upon it.

## Adjust migration

First of all, we have to add a new column to our table: `version_id` which in union with the `id` field replaces the primary key.

So your SQL command could look like this:

```sql
ALTER TABLE `swag_example`
    ADD `version_id` BINARY(16) NOT NULL AFTER `id`,
    ADD PRIMARY KEY `id_version_id` (`id`, `version_id`),
    DROP INDEX `PRIMARY`;
```

## Adjust definition

After we've added the new field to our table, we also have to add it to our definition.
For this we use a `Shopware\Core\Framework\DataAbstractionLayer\Field\VersionField` which is always required, if we want to version our entity.

```php
// <plugin root>/src/Core/Content/Example/ExampleDefinition.php
protected function defineFields(): FieldCollection
{
    return new FieldCollection([
        new VersionField(),
        ...
    ]);
}
```

## Create and merge version

In this section we will create a new version of our entity which will create a new entry in the database with our updated values.
When we merge a particular version, all versions before the merged version are deleted.
In the example below, we are using a service where we injected a `swag_example.repository`.

```php
// <plugin root>/src/
public function exampleVersioning(Context $context): void
{
    $exampleId = Uuid::randomHex();

    $this->exampleRepository->create([[
        'id' => $exampleId,
        'name' => 'Example',
        'description' => 'This is an example',
        'active' => true,
    ]], $context);

    // Create new version of our entity
    $versionId = $this->exampleRepository->createVersion($exampleId, $context);

    // Update the context with our version
    $versionContext = $context->createWithVersionId($versionId);

    // Update our new entity version
    $this->exampleRepository->update([
        [
            'id' => $exampleId,
            'description' => 'This is our new description',
        ],
    ], $versionContext);

    // Our first entity will be found
    $exampleOne = $this->exampleRepository->search(new Criteria([$exampleId]), $context)->first();

    // Updated entity will be found
    $exampleTwo = $this->exampleRepository->search(new Criteria([$exampleId]), $versionContext)->first();

    $this->exampleRepository->merge($versionId, $context);

    // Our updated entity will be found now
    $exampleThree = $this->exampleRepository->search(new Criteria([$exampleId]), $context)->first();
}
```

As you can see above, we first created a new `ExampleEntity` with the description 'This is an example'.

Then we created a new version of our entity with the appropriate repository method `createVersion` and as arguments the id of our created entity and the context.
This method returns the id of our new entity version, which we have stored in a variable.

Next, we used the `createWithVersionId` method of our `Context` to create a new context with our new versionId assigned to it.
This new `Context` is used to update the `ExampleEntity`.
In our case we have updated the description to 'This is our new description'.
By using the updated context with the new `versionId`, the DAL knows that we want to update this version of our entity.

Subsequently, we searched the repository with the original context and our new versioned context.
In the first search result, using the original context, we get the first version of our entity, which we created at the beginning.
With the second search result we get the updated entity, using our new versioned context.

Lastly, we used the repository method `merge` with our versionId, which deletes all versions before this one.
The merged version is now our new live version. From now on we can find it without using a versioned context.

## Versioning with foreign keys

If you have an entity with foreign keys, your foreign keys also need to be versioned.
In this example we're using an inherited field.
If you are not familiar with inheritance, head over to our [Field inheritance](field-inheritance) guide.

### Migration

In this step we have to additionally add a foreign key constraint for your `parent_id` and `parent_version_id` referencing to our `id` and `version_id`.
The same pattern applies to other entities.

```sql
ALTER TABLE `swag_example`
    ADD `version_id` BINARY(16) NOT NULL AFTER `id`,
    ADD `parent_version_id` BINARY(16) NOT NULL,
    ADD PRIMARY KEY `id_version_id` (`id`, `version_id`),
    DROP INDEX `PRIMARY`,
    CONSTRAINT `fk.swag_example.parent_id` FOREIGN KEY (`parent_id`, `parent_version_id`)
        REFERENCES `swag_example` (`id`, `version_id`) ON DELETE CASCADE ON UPDATE CASCADE
```

### Definition

After we've added the new field to our table, we also have to add it to our definition.
For this we use a `Shopware\Core\Framework\DataAbstractionLayer\Field\ReferenceVersionField` which references to our entity by using `self::class` and the related field `parent_version_id`.

```php
// <plugin root>/src/Core/Content/Example/ExampleDefinition.php
protected function defineFields(): FieldCollection
{
    return new FieldCollection([
        new VersionField(),
        (new ReferenceVersionField(self::class, 'parent_version_id')),
        ...
    ]);
}
```

---

---

