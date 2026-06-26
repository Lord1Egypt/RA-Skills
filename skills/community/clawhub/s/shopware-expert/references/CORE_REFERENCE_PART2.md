# CORE REFERENCE

Compiled excerpts from the Shopware Developer Documentation snapshot. Prefer live docs at [developer.shopware.com](https://developer.shopware.com/) when in doubt.

---

## Commands Reference
**Source:** [resources/references/core-reference/commands-reference.md](https://developer.shopware.com/docs/v6.6/resources/references/core-reference/commands-reference.md)  
*(Body truncated in this bundle; follow the link for the rest.)*

# Commands Reference

These commands can be executed using the Shopware command line interface (CLI), located within your Shopware project.

```bash
$ bin/console [command] [parameters]
```

## Commands

### General

| Command | Description |
| :--- | :--- |
| `about` | Displays information about the current project |
| `help` | Displays help for a command |
| `list` | Lists commands |

### Administration

| Command | Description |
| :--- | :--- |
| `administration:delete-files-after-build` | Deletes all unnecessary files of the administration after the build process |

### App

| Command | Description |
| :--- | :--- |
| `app:activate` | Activates the app in the folder with the given name |
| `app:create` | Creates an app skeleton |
| `app:deactivate` | Deactivates the app in the folder with the given name |
| `app:install` | Installs the app in the folder with the given name |
| `app:refresh` | \[app:update] Refreshes the installed apps |
| `app:uninstall` | Uninstalls the app |
| `app:url-change:resolve` | Resolves changes in the app URL and how the app system should handle it. |
| `app:validate` | Checks manifests for errors |

### Assets

| Command | Description |
| :--- | :--- |
| `assets:install` |  |

### Bundle

| Command | Description |
| :--- | :--- |
| `bundle:dump` | \[administration:dump:plugins|administration:dump:bundles] Creates a JSON file with the configuration for each active Shopware bundle. |

### Cache

| Command | Description |
| :--- | :--- |
| `cache:clear` | Clears the cache |
| `cache:pool:clear` | Clears cache pools |
| `cache:pool:delete` | Deletes an item from a cache pool |
| `cache:pool:list` | Lists available cache pools |
| `cache:pool:prune` | Prunes cache pools |
| `cache:warmup` | Warms up an empty cache |

### Cart

| Command | Description |
| :--- | :--- |
| `cart:migrate` | Migrates carts from redis to database |

### Changelog

| Command | Description |
| :--- | :--- |
| `changelog:change` | Returns all changes made in a specific / unreleased version. |
| `changelog:check` | Checks the validation of a given changelog file or of all files in the "changelog/\_unreleased" folder |
| `changelog:create` | Creates a changelog markdown file in `/changelog/_unreleased` |
| `changelog:release` | Creates or updates the final changelog for a new release |

### Config

| Command | Description |
| :--- | :--- |
| `config:dump-reference` | Dumps the default configuration for an extension |

### Customer

| Command | Description |
| :--- | :--- |
| `customer:delete-unused-guests` | Deletes unused guest customers |

### Dal

| Command | Description |
| :--- | :--- |
| `dal:create:entities` | Creates the entity classes |
| `dal:create:hydrators` | Creates the hydrator classes |
| `dal:create:schema` | Creates the database schema |
| `dal:refresh:index` | Refreshes the index for a given entity |
| `dal:validate` | Validates the DAL definitions |

### Database

| Command | Description |
| :--- | :--- |
| `database:clean-personal-data` | Cleans personal data from the database |
| `database:create-migration` | Creates a new migration file |
| `database:migrate` | Executes all migrations |
| `database:migrate-destructive` | Executes all migrations |
| `database:refresh-migration` | Refreshes the migration state |

### Debug

| Command | Description |
| :--- | :--- |
| `debug:autowiring` | Lists classes/interfaces you can use for autowiring |
| `debug:business-events` | Dumps all business events |
| `debug:config` | Dumps the current configuration for an extension |
| `debug:container` | Displays current services for an application |
| `debug:event-dispatcher` | Displays configured listeners for an application |
| `debug:messenger` | Lists messages you can dispatch using the message buses |
| `debug:router` | Displays current routes for an application |
| `debug:translation` | Displays translation messages information |
| `debug:twig` | Shows a list of twig functions, filters, globals and tests |

### Es

| Command | Description |
| :--- | :--- |
| `es:admin:index` | Indexes the elasticsearch for the admin search |
| `es:admin:reset` | Reset Admin Elasticsearch indexing |
| `es:admin:test` | Allows you to test the admin search index |
| `es:create:alias` | Creates the elasticsearch alias |
| `es:index` | Reindexes all entities to elasticsearch |
| `es:index:cleanup` | Cleans outdated indices |
| `es:reset` | Resets the elasticsearch index |
| `es:status` | Shows the status of the elasticsearch index |
| `es:test:analyzer` | Allows to test an elasticsearch analyzer |

### Feature

| Command | Description |
| :--- | :--- |
| `feature:dump` | \[administration:dump:features] Creates a JSON file with feature config for JS testing and hot reloading capabilities |

### Framework

| Command | Description |
| :--- | :--- |
| `framework:demodata` | Generates demo data |
| `framework:dump:class:schema` | Dumps the schema of the given entity |
| `framework:schema` | Dumps the api definition to a json file. |

### Http

| Command | Description |
| :--- | :--- |
| `http:cache:warm:up` | Warms up the HTTP cache |

### Import

| Command | Description |
| :--- | :--- |
| `import:entity` | Imports entities from a CSV file |

### Import-export

| Command | Description |
| :--- | :--- |
| `import-export:delete-expired` | Deletes all expired import/export files |

### Lint

| Command | Description |
| :--- | :--- |
| `lint:container` | Ensures that arguments injected into services match type declarations |
| `lint:twig` | Lints a Twig template and outputs encountered errors |
| `lint:xliff` | Lints a XLIFF file and outputs encountered errors |
| `lint:yaml` | Lints a YAML file and outputs encountered errors |

### Mailer

| Command | Description |
| :--- | :--- |
| `mailer:test` | Tests Mailer transports by sending an email |

### Media

| Command                      | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
|:-----------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `media:delete-unused`        |  Deletes all media files that are never used. Use the `--dry-run` flag to see a paginated list of files that will be deleted, without actually deleting them. Use the `--grace-period-days=10` to set a grace period for unused media, meaning only media uploaded before the current date and time minus 10 days will be considered for deletion. The default is 20 and therefore any media uploaded in the previous 20 days will not be considered for deletion even if it is unused. Use the `--folder-entity` flag to target only a specific folder (e.g. `--folder-entity=PRODUCT` to purge all product images) |
| `media:generate-media-types` | Generates the media types for all media entities                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| `media:generate-thumbnails`  | Generates the thumbnails for all media entities                                                                                                                                                                                                                                                                                                                                                                                                                                                 |

### Messenger

| Command | Description |
| :--- | :--- |
| `messenger:consume` | Consumes messages |
| `messenger:failed:remove` | Removes given messages from the failure transport |
| `messenger:failed:retry` | Retries one or more messages from the failure transport |
| `messenger:failed:show` | Shows one or more messages from the failure transport |
| `messenger:setup-transports` | Prepares the required infrastructure for the transport |
| `messenger:stats` | Shows the message count for one or more transports |
| `messenger:stop-workers` | Stops workers after their current message |

### Number-range

| Command | Description |
| :--- | :--- |
| `number-range:migrate` | Migrates the increment storage of a number range |

### Plugin

| Command | Description |
| :--- | :--- |
| `plugin:activate` | Activates given plugins |
| `plugin:create` | Creates a plugin skeleton |
| `plugin:deactivate` | Deactivates given plugins |
| `plugin:install` | Installs given plugins |
| `plugin:list` | Lists all plugins |
| `plugin:refresh` | Refreshes the plugins list in the storage from the file system |
| `plugin:uninstall` | Uninstalls given plugins |
| `plugin:update` | Updates given plugins |
| `plugin:zip-import` | Imports a plugin from a zip file |

### Product-export

| Command | Description |
| :--- | :--- |
| `product-export:generate` | Generates a product export file |

### Router

| Command | Description |
| :--- | :--- |
| `router:match` | Helps debug routes by simulating a path info match |

### S3

| Command | Description |
| :--- | :--- |
| `s3:set-visibility` | Sets the visibility of all files in the s3 filesystem to public |

### Sales-channel

| Command | Description |
| :--- | :--- |
| `sales-channel:create` | Creates a new sales channel |
| `sales-channel:create:storefront` | Creates a new storefront sales channel |
| `sales-channel:list` | Lists all sales channels |
| `sales-channel:maintenance:disable` | Disables maintenance mode for a sales channel |
| `sales-channel:maintenance:enable` | Enables maintenance mode for a sales channel |
| `sales-channel:update:domain` | Updates a sales channel domain |

### Scheduled-task

| Command | Description | Version |
| :--- | :--- | :--- |
| `scheduled-task:register` | Registers all scheduled tasks |
| `scheduled-task:run` | Runs scheduled tasks |
| `scheduled-task:run-single` | Runs single scheduled tasks | 6.5.5.0 |
| `scheduled-task:list` | Lists all scheduled tasks | 6.5.5.0 |

### Secrets

| Command | Description |
| :--- | :--- |
| `secrets:decrypt-to-local` | Decrypts all secrets and stores them in the local vault |
| `secrets:encrypt-from-local` | Encrypts all local secrets to the vault |
| `secrets:generate-keys` | Generates new encryption keys |
| `secrets:list` | Lists all secrets |
| `secrets:remove` | Removes a secret from the vault |
| `secrets:set` | Sets a secret in the vault |

### Sitemap

| Command | Description |
| :--- | :--- |
| `sitemap:generate` | Generates sitemaps for a given shop (or all active ones) |

### Snippets

| Command | Description |
| :--- | :--- |
| `snippets:validate` | Validates snippets |

### State-machine

| Command | Description |
| :--- | :--- |
| `state-machine:dump` | Dumps a state machine to a graphviz file |

### Store

| Command | Description |
| :--- | :--- |
| `store:download` | Downloads a plugin from the store |
| `store:login` | Login for the store |

### System

| Command | Description |
| :--- | :--- |
| `sys

… **Truncated.** Full document: https://developer.shopware.com/docs/v6.6/resources/references/core-reference/commands-reference.md


---

## Composer Commands Reference
**Source:** [resources/references/core-reference/composer-commands-reference.md](https://developer.shopware.com/docs/v6.6/resources/references/core-reference/composer-commands-reference.md)  
# Composer Commands Reference

::: info
These commands are only available inside `shopware/shopware` GitHub repository, so when you contribute to Shopware. For regular projects, use `./bin/*.sh` scripts.
:::

These composer commands can be executed using composer with your Shopware project.

```bash
$ composer [command] [parameters]
```

## Commands

### Setup & build

| Command                      | Description                                                                                                                   |
|------------------------------|-------------------------------------------------------------------------------------------------------------------------------|
| `setup`                      | Resets and re-installs this Shopware instance - Database will be purged!                                                      |
| `build:js`                   | Builds Administration & Storefront - Combination of `build:js:admin` & `build:js:storefront`                                  |
| `build:js:admin`             | Builds the Administration - Includes `bundle:dump`, `feature:dump`, `admin:generate-entity-schema-types` and `assets:install` |
| `build:js:component-library` | Builds the component library                                                                                                  |
| `watch:admin`                | Build administration with hot module reloading                                                                                |
| `build:js:storefront`        | Builds the Storefront's JavaScript - Includes `bundle:dump`, `feature:dump` and `theme:compile`                               |
| `check:license`              | Check third-party dependency licenses for composer dependencies                                                               |
| `reset`                      | Resets this Shopware instance, without composer and npm install. (Faster reset if no dependencies changed)                    |

### Administration

| Command                              | Description                                                                   |
|:-------------------------------------|:------------------------------------------------------------------------------|
| `admin:create:test`                  | Generate a test boilerplate                                                   |
| `admin:generate-entity-schema-types` | Convert entity schemas to data types                                          |
| `admin:unit`                         | Launches the jest unit test-suite for the Admin                               |
| `admin:unit:watch`                   | Launches the interactive jest unit test-suite watcher for the Admin           |
| `admin:unit:prepare-vue3`            | Prepares the jest unit test-suite for the Admin with Vue3                     |
| `admin:unit:vue3`                    | Launches the jest unit test-suite for the Admin with Vue3                     |
| `admin:unit:watch:vue3`              | Launches the interactive jest unit test-suite watcher for the Admin with Vue3 |
| `npm:admin:check-license`            | Check third-party dependency licenses for administration                      |
| `watch:admin`                        | Build administration with hot module reloading                                |

### Storefront

| Command                        | Description                                                                                     |
|:-------------------------------|:------------------------------------------------------------------------------------------------|
| `build:js:storefront`          | Builds the Storefront's JavaScript - Includes `bundle:dump`, `feature:dump` and `theme:compile` |
| `npm:storefront:check-license` | Check third-party dependency licenses for storefront                                            |
| `watch:storefront`             | Build storefront with hot module reloading                                                      |

### Testsuite & Development

| Command                 | Description                                                                                           |
|:------------------------|:------------------------------------------------------------------------------------------------------|
| `bc-check`              | Checks for backwards compatibility breaks in the current branch                                       |
| `e2e:setup`             | Installs a clean shopware instance for E2E environment and launches `e2e:prepare`                     |
| `e2e:open`              | Launches the Cypress E2E test-suite UI                                                                |
| `e2e:prepare`           | Installs the Admin Extension SDK test plugin with fixtures and dumps the database                     |
| `ecs`                   | Checks all files regarding the Easy Coding Standard                                                   |
| `ecs-fix`               | Checks all files regarding the Easy Coding Standard and fixes them if possible                        |
| `eslint`                | Codestyle checks all (Administration/Storefront/E2E) JS/TS files                                      |
| `eslint:admin`          | Codestyle checks Administration JS/TS files                                                           |
| `eslint:admin:fix`      | Codestyle checks Administration JS/TS files and fixes them if possible                                |
| `eslint:e2e`            | Codestyle checks all E2E JS/TS files                                                                  |
| `eslint:e2e:fix`        | Codestyle checks all E2E JS/TS files and fixes them if possible                                       |
| `eslint:storefront`     | Codestyle checks all Storefront JS/TS files                                                           |
| `init:testdb`           | Initializes the test database                                                                         |
| `lint`                  | Shorthand for the composer commands `stylelint`, `eslint`, `ecs`, `lint:changlog` and `lint:snippets` |
| `lint:changelog`        | Validates changelogs                                                                                  |
| `lint:snippets`         | Validates existence of snippets in all core-supported languages                                       |
| `phpstan`               | runs the PHP static analysis tool                                                                     |
| `phpunit`               | Launches the PHP unit test-suit                                                                       |
| `phpunit:quarantined`   | Launches the PHP unit test-suite for quarantined tests                                                |
| `storefront:unit`       | Launches the jest unit test-suite for the Storefront                                                  |
| `storefront:unit:watch` | Launches the interactive jest unit test-suite watcher for the Storefront                              |

---

---

## DAL Reference
**Source:** [resources/references/core-reference/dal-reference.md](https://developer.shopware.com/docs/v6.6/resources/references/core-reference/dal-reference.md)  
# DAL Reference

The DAL reference documents fields, flags, filters, and aggregations for effective data management and querying within the platform.

---

---

## Aggregations Reference
**Source:** [resources/references/core-reference/dal-reference/aggregations-reference.md](https://developer.shopware.com/docs/v6.6/resources/references/core-reference/dal-reference/aggregations-reference.md)  
*(Body truncated in this bundle; follow the link for the rest.)*

# Aggregations Reference

Aggregations allow you to determine further information about the overall result in addition to the actual search results. These include totals, unique values, or the average of a field.

The DAL knows two types of aggregations:

* `metric` aggregation - This type of aggregation applies a mathematical formula to a field. A metric aggregation always has a calculated result. These are aggregations to calculate sums or maximum values.
* `bucket` aggregation - With this type of aggregation, a list of keys is determined. Further aggregations can then be determined for each key.

| Name | Type | Description |
| :--- | :--- | :--- |
| avg | metric | Average of all numeric values for the specified field |
| count | metric | Number of records for the specified field |
| max | metric | Maximum value for the specified field |
| min | metric | Minimal value for the specified field |
| stats | metric | Stats overall numeric values for the specified field |
| sum | metric | Sum of all numeric values for the specified field |
| entity | bucket | Groups the result for each value of the provided field and fetches the entities for this field |
| filter | bucket | Allows to filter the aggregation result |
| terms | bucket | Groups the result for each value of the provided field and fetches the count of affected documents |
| histogram | bucket | Groups the result for each value of the provided field and fetches the count of affected documents. Although allows to provide date interval (day, month, ...) |
| range | bucket | Groups the result for each defined set of ranges into each bucket - bucket of numerical data and a count of items/documents for each bucket |

## Avg aggregation

The `Avg` aggregation makes it possible to calculate the average value for a field. The following SQL statement is executed in the background: `AVG(price)`.

```php
$criteria = new Criteria();
$criteria->setLimit(1);

$criteria->addAggregation(
    new AvgAggregation('avg-price', 'price')
);

$result = $repository->search($criteria, $context);

/** @var AvgResult $aggregation */
$aggregation = $result->getAggregations()->get('avg-price');

$aggregation->getAvg();
```

```json
{
    "limit": 1,
    "includes": {
        "product": ["id", "name"]
    },
    "aggregations": [
        {  
            "name": "avg-price",
            "type": "avg",
            "field": "price"
        }
    ]
}
```

Response

```json
{
    "total": 1,
    "data": [
        {
            "name": "Gorgeous Cotton Magellanic Penguin",
            "id": "0402ca6a746b41458fd000124c308cc8",
            "apiAlias": "product"
        }
    ],
    "aggregations": {
        "avg-price": {
            "avg": 505.73333333333335,
            "extensions": []
        }
    }
}
```

## Count aggregation

The `count` aggregation makes it possible to determine the number of entries for a field that are filled with a value. The following SQL statement is executed in the background: `COUNT(DISTINCT(manufacturerId))`.

```php
$criteria = new Criteria();
$criteria->setLimit(1);

$criteria->addAggregation(
    new CountAggregation('count-manufacturers', 'manufacturerId')
);

$result = $repository->search($criteria, $context);

/** @var CountResult $aggregation */
$aggregation = $result->getAggregations()->get('count-manufacturers');

$aggregation->getCount();
```

```json
{
    "limit": 1,
    "includes": {
        "product": ["id", "name"]
    },
    "aggregations": [
        {  
            "name": "count-manufacturers",
            "type": "count",
            "field": "manufacturerId"
        }
    ]
}
```

Response

```json
{
    "total": 1,
    "data": [
        {
            "name": "Gorgeous Cotton Magellanic Penguin",
            "id": "0402ca6a746b41458fd000124c308cc8",
            "apiAlias": "product"
        }
    ],
    "aggregations": {
        "count-manufacturers": {
            "count": 44,
            "extensions": []
        }
    }
}
```

## Max aggregation

The `max` aggregation allows you to determine the maximum value of a field. The following SQL statement is executed in the background: `MAX(price)`.

```php
$criteria = new Criteria();
$criteria->setLimit(1);

$criteria->addAggregation(
    new MaxAggregation('max-price', 'price')
);

$result = $repository->search($criteria, $context);

/** @var MaxResult $aggregation */
$aggregation = $result->getAggregations()->get('max-price');

$aggregation->getMax();
```

```json
{
    "limit": 1,
    "includes": {
        "product": ["id", "name"]
    },
    "aggregations": [
        {  
            "name": "max-price",
            "type": "max",
            "field": "price"
        }
    ]
}
```

Response

```json
{
    "total": 1,
    "data": [
        {
            "name": "Gorgeous Cotton Magellanic Penguin",
            "id": "0402ca6a746b41458fd000124c308cc8",
            "apiAlias": "product"
        }
    ],
    "aggregations": {
        "max-price": {
            "max": "979",
            "extensions": []
        }
    }
}
```

## Min aggregation

The `min` aggregation makes it possible to determine the minimum value of a field. The following SQL statement is executed in the background: `MIN(price)`

```php
$criteria = new Criteria();
$criteria->setLimit(1);

$criteria->addAggregation(
    new MinAggregation('min-price', 'price')
);

$result = $repository->search($criteria, $context);

/** @var MinResult $aggregation */
$aggregation = $result->getAggregations()->get('min-price');

$aggregation->getMin();
```

```json
{
    "limit": 1,
    "includes": {
        "product": ["id", "name"]
    },
    "aggregations": [
        {  
            "name": "min-price",
            "type": "min",
            "field": "price"
        }
    ]
}
```

Response

```json
{
    "total": 1,
    "data": [
        {
            "name": "Gorgeous Cotton Magellanic Penguin",
            "id": "0402ca6a746b41458fd000124c308cc8",
            "apiAlias": "product"
        }
    ],
    "aggregations": {
        "min-price": {
            "min": "5",
            "extensions": []
        }
    }
}
```

## Sum aggregation

The `sum` aggregation makes it possible to determine the total of a field. The following SQL statement is executed in the background: `SUM(price)`.[PHP](https://docs.shopware.com/en/shopware-platform-dev-en/references-internals/core/dal?category=shopware-platform-dev-en/references-internals/core#)[API](https://docs.shopware.com/en/shopware-platform-dev-en/references-internals/core/dal?category=shopware-platform-dev-en/references-internals/core#)

```php
$criteria = new Criteria();
$criteria->setLimit(1);

$criteria->addAggregation(
    new SumAggregation('sum-price', 'price')
);

$result = $repository->search($criteria, $context);

/** @var SumResult $aggregation */
$aggregation = $result->getAggregations()->get('sum-price');

$aggregation->getSum();
```

```json
{
    "limit": 1,
    "includes": {
        "product": ["id", "name"]
    },
    "aggregations": [
        {  
            "name": "sum-price",
            "type": "sum",
            "field": "price"
        }
    ]
}
```

Response

```json
{
    "total": 1,
    "data": [
        {
            "name": "Gorgeous Cotton Magellanic Penguin",
            "id": "0402ca6a746b41458fd000124c308cc8",
            "apiAlias": "product"
        }
    ],
    "aggregations": {
        "sum-price": {
            "sum": 30344,
            "extensions": []
        }
    }
}
```

## Stats aggregation

The `stats` aggregation makes it possible to calculate several values at once for a field. This includes the previous `max`, `min`, `avg` and `sum` aggregation. The following SQL statement is executed in the background: `SELECT MAX(price), MIN(price), AVG(price), SUM(price)`.

```php
$criteria = new Criteria();
$criteria->setLimit(1);

$criteria->addAggregation(
    new StatsAggregation('stats-price', 'price')
);

$result = $repository->search($criteria, $context);

/** @var StatsResult $aggregation */
$aggregation = $result->getAggregations()->get('stats-price');

$aggregation->getSum();
$aggregation->getMax();
$aggregation->getAvg();
$aggregation->getMin();
```

```json
{
    "limit": 1,
    "includes": {
        "product": ["id", "name"]
    },
    "aggregations": [
        {  
            "name": "stats-price",
            "type": "stats",
            "field": "price"
        }
    ]
}
```

Response

```json
{
    "total": 1,
    "data": [
        {
            "name": "Gorgeous Cotton Magellanic Penguin",
            "id": "0402ca6a746b41458fd000124c308cc8",
            "apiAlias": "product"
        }
    ],
    "aggregations": {
        "stats-price": {
            "min": "5",
            "max": "979",
            "avg": 505.73333333333335,
            "sum": 30344,
            "extensions": []
        }
    }
}
```

## Terms aggregation

The `terms` aggregation belongs to the bucket aggregations. This allows you to determine the values of a field. The result contains each value once and how often this value occurs in the result. The `terms` aggregation also supports the following parameters:

* `limit` - Defines a maximum number of entries to be returned (default: zero)
* `sort` - Defines the order of the entries. By default, the following is not sorted
* `aggregation` - Enables you to calculate further aggregations for each key

The following SQL statement is executed in the background: `SELECT DISTINCT(manufacturerId) as key, COUNT(manufacturerId) as count`

```php
$criteria = new Criteria();
$criteria->setLimit(1);

$criteria->addAggregation(
    new TermsAggregation(
        'manufacturer-ids',
        'manufacturerId',
        10,
        new FieldSorting('manufacturer.name', FieldSorting::DESCENDING)
    )
);

$result = $repository->search($criteria, $context);

/** @var TermsResult $aggregation */
$aggregation = $result->getAggregations()->get('manufacturer-ids');

foreach ($aggregation->getBuckets() as $bucket) {
    $bucket->getKey();
    $bucket->getCount();
}
```

```json
{
    "limit": 1,
    "includes": {
        "product": ["id", "name"]
    },
    "aggregations": [
        {
            "name": "manufacturer-ids",
            "type": "terms",
            "limit": 3,
            "sort": { "field": "manufacturer.name", "order": "DESC" },
            "field": "manufacturerId"
        }
    ]
}
```

Response

```json
{
    "total": 1,
    "data": [
        {
            "name": "Gorgeous Cotton Magellanic Penguin",
            "id": "0402ca6a746b41458fd000124c308cc8",
            "apiAlias": "product"
        }
    ],
    "aggregations": {
        "manufacturer-ids": {
            "buckets": [
                {
                    "key": "7af1534f96604744a4bc16e713550107",
                    "count": 1,
                    "extensions": []
                },
                {
                    "key": "32d5c55f960b409ab209fe25c88a6676",
                    "count": 1,
                    "extensions": []
                },
                {
                    "key": "935ceec182714a8da48227d4772628a4",
                    "count": 1,
                    "extensions": []
                }
            ],
            "extensions": []
        }
    }
}
```

## Filter aggregation

The `filter` aggregation belongs to the bucket aggregations. Unlike all other aggregations, this aggregation does not determine any result. It can't be used alone. It is only used to further restrict the result of an aggregation in a criterion. Filters defined inside the `filter` property of this aggregation type are only used when calculating this aggregation. The filters have no effect on other aggregations or on the result of the search.

```php
$criteria = new Criteria();
$criteria->setLimit(1);

$criteria->addAggregation(
    new FilterAggregation(
        'active-price-avg',
        new AvgAggregation('avg-price', 'price'),
        [
            new EqualsFilter('active', true)
        ]
    )
);

$result = $repository->search($crit

… **Truncated.** Full document: https://developer.shopware.com/docs/v6.6/resources/references/core-reference/dal-reference/aggregations-reference.md


---

## Fields Reference
**Source:** [resources/references/core-reference/dal-reference/fields-reference.md](https://developer.shopware.com/docs/v6.6/resources/references/core-reference/dal-reference/fields-reference.md)  
# Fields Reference

| Name                         | Description                  | Extends                   | StorageAware |
|:-----------------------------|:-----------------------------|:--------------------------|:-------------|
| AssociationField             | Stores a association value   | Field                     |              |
| AutoIncrementField           | Stores an integer value      | IntField                  |              |
| BlobField                    | Stores a blob value          | Field                     | x            |
| BoolField                    | Stores a bool value          | Field                     | x            |
| BreadcrumbField              | Stores a JSON value          | JsonField                 |              |
| CalculatedPriceField         | Stores a JSON value          | JsonField                 |              |
| CartPriceField               | Stores a JSON value          | JsonField                 |              |
| CashRoundingConfigField      | Stores a JSON value          | JsonField                 |              |
| ChildCountField              | Stores an integer value      | IntField                  |              |
| ChildrenAssociationField     | Stores a association value   | OneToManyAssociationField |              |
| ConfigJsonField              | Stores a JSON value          | JsonField                 |              |
| CreatedAtField               | Stores a DateTime value      | DateTimeField             |              |
| CreatedByField               | Stores a foreign key value   | FkField                   |              |
| CronIntervalField            | Stores a croninterval value  | Field                     | x            |
| DateField                    | Stores a date value          | Field                     | x            |
| DateIntervalField            | Stores a dateinterval value  | Field                     | x            |
| DateTimeField                | Stores a datetime value      | Field                     | x            |
| EmailField                   | Stores a string value        | StringField               |              |
| [EnumField](enum-field)      | Stores a enum value          | Field                     | x            |
| Field                        | Stores a  value              | Struct                    |              |
| FkField                      | Stores a fk value            | Field                     | x            |
| FloatField                   | Stores a float value         | Field                     | x            |
| IdField                      | Stores a id value            | Field                     | x            |
| IntField                     | Stores a int value           | Field                     | x            |
| JsonField                    | Stores a json value          | Field                     | x            |
| ListField                    | Stores a JSON value          | JsonField                 |              |
| LockedField                  | Stores a boolean value       | BoolField                 |              |
| LongTextField                | Stores a longtext value      | Field                     | x            |
| ManyToManyAssociationField   | Stores a association value   | AssociationField          |              |
| ManyToManyIdField            | Stores a manytomanyid value  | ListField                 |              |
| ManyToOneAssociationField    | Stores a association value   | AssociationField          |              |
| ObjectField                  | Stores a JSON value          | JsonField                 |              |
| OneToManyAssociationField    | Stores a association value   | AssociationField          |              |
| OneToOneAssociationField     | Stores a association value   | AssociationField          |              |
| ParentAssociationField       | Stores a association value   | ManyToOneAssociationField |              |
| ParentFkField                | Stores a foreign key value   | FkField                   |              |
| PasswordField                | Stores a password value      | Field                     | x            |
| PriceDefinitionField         | Stores a JSON value          | JsonField                 |              |
| PriceField                   | Stores a JSON value          | JsonField                 |              |
| ReferenceVersionField        | Stores a foreign key value   | FkField                   |              |
| RemoteAddressField           | Stores a remoteaddress value | Field                     | x            |
| SerializedField              | Stores a serialized value    | Field                     | x            |
| StateMachineStateField       | Stores a foreign key value   | FkField                   |              |
| StringField                  | Stores a string value        | Field                     | x            |
| TaxFreeConfigField           | Stores a JSON value          | JsonField                 |              |
| TimeZoneField                | Stores a string value        | StringField               |              |
| TranslatedField              | Stores a translated value    | Field                     |              |
| TranslationsAssociationField | Stores a association value   | OneToManyAssociationField |              |
| TreeBreadcrumbField          | Stores a JSON value          | JsonField                 |              |
| TreeLevelField               | Stores an integer value      | IntField                  |              |
| TreePathField                | Stores a treepath value      | LongTextField             |              |
| UpdatedAtField               | Stores a DateTime value      | DateTimeField             |              |
| UpdatedByField               | Stores a foreign key value   | FkField                   |              |
| VariantListingConfigField    | Stores a JSON value          | JsonField                 |              |
| VersionDataPayloadField      | Stores a JSON value          | JsonField                 |              |
| VersionField                 | Stores a foreign key value   | FkField                   |              |

---

---

## EnumField reference
**Source:** [resources/references/core-reference/dal-reference/fields-reference/enum-field.md](https://developer.shopware.com/docs/v6.6/resources/references/core-reference/dal-reference/fields-reference/enum-field.md)  
# EnumField reference

## Usage

The `EnumField` can be used to restrict  `string` or `int` values to a fixed set.

Define a `\BackedEnum` class, use them in an Entity and restrict the values in your RDBMS.

```php
<?php

enum PaymentMethod : string {
    case PAYPAL = 'paypal';
    case CREDIT_CARD = 'credit_card';
    case INVOICE = 'invoice';
}
```

```php
<?php

enum BatchOrderSize: int {
    case DOZEN = 12;
    case SCORE = 20;
    case SMALL_GROSS = 120;
    case GROSS = 144;
    case GRAND = 1000;
}
```

```php
<?php

class BatchOrderEntity extends Entity {

    #[Field(type: FieldType::ENUM, column: 'payment_method')]
    protected PaymentMethod $paymentMethod;

    #[Field(type: FieldType::ENUM, column: 'amount')]
    protected BatchOrderSize $amount;
    
   public function getPaymentMethod(): PaymentMethod
    {
        return $this->paymentMethod;
    }
    
    public function setPaymentMethod(PaymentMethod $paymentMethod): void
    {
        $this->paymentMethod = $paymentMethod;
    }
    
    public function getAmount(): BatchOrderSize
    {
        return $this->amount;
    }
    
    public function setAmount(BatchOrderSize $amount): void
    {
        $this->amount = $amount;
    }
```

```sql
CREATE TABLE `batch_order` (
    `id` BINARY(16) NOT NULL,
    `payment_method` ENUM('paypal', 'credit_card', 'invoice') NOT NULL,
    `amount` INT NOT NULL,
    PRIMARY KEY (`id`)
);
```

It's not advisable to use `ENUM` types for integer values, as most RDBMS only support string values and use integers
internally. Using a regular `INT` column is recommended in this case. The `BackedEnum` will restrict the possible
values, unless the database is modified manually.

## Examples

### Example 1: Creating an input field from an enum

```twig
<select name="payment_method">
    {% for method in PaymentMethod::cases() %}
        <option value="{{ method.value }}">{{ method.name }}</option>
    {% endfor %}
</select>
```

### Example 2: Setting an Entity value

```php
<?php

$batchOrder = new BatchOrderEntity();
$batchOrder->setPaymentMethod(PaymentMethod::PAYPAL);
```

### Example 3: Check if a value is valid

```php
<?php

$validPaymentMethod = PaymentMethod::tryFrom($userProvidedInput);

// Either check for null
if (is_null($validPaymentMethod)) {
    // The input was not a valid payment method
}

// Or check for the class
if($validPaymentMethod instanceof PaymentMethod) {
    // The input was a valid payment method
}

```

---

---

## Filters Reference
**Source:** [resources/references/core-reference/dal-reference/filters-reference.md](https://developer.shopware.com/docs/v6.6/resources/references/core-reference/dal-reference/filters-reference.md)  
# Filters Reference

| Name | Notes |
| :--- | :--- |
| equals | Exact match for the given value |
| equalsAny | At least one exact match for a value of the given list |
| contains | Before and after wildcard search for the given value |
| range | For range compatible fields like numbers or dates |
| not | Allows to negate a filter |
| multi | Allows to combine different filters |
| prefix | Before wildcard search for the given value |
| suffix | After wildcard search for the given value |

## Equals

The `Equals` filter allows you to check fields for an exact value. The following SQL statement is executed in the background: `WHERE stock = 10`.

```php
$criteria = new Criteria();
$criteria->addFilter(new EqualsFilter('stock', 10));
```

```javascript
 {
    "filter": [
        { 
            "type": "equals", 
            "field": "stock", 
            "value": 10
        }    
    ]
}
```

## EqualsAny

The `EqualsAny` filter allows you to filter a field where at least one of the defined values matches exactly. The following SQL statement is executed in the background: `WHERE productNumber IN ('3fed029475fa4d4585f3a119886e0eb1', '77d26d011d914c3aa2c197c81241a45b')`.

```php
$criteria = new Criteria();
$criteria->addFilter(
    new EqualsAnyFilter('productNumber', ['3fed029475fa4d4585f3a119886e0eb1', '77d26d011d914c3aa2c197c81241a45b'])
);
```

```json
{
    "filter": [
        { 
            "type": "equalsAny", 
            "field": "productNumber", 
            "value": [
                "3fed029475fa4d4585f3a119886e0eb1", 
                "77d26d011d914c3aa2c197c81241a45b"
            ] 
        }    
    ]
}
```

## Contains

The `Contains` Filter allows you to filter a field to an approximate value, where the passed value must be contained as a full value. The following SQL statement is executed in the background: `WHERE name LIKE '%Lightweight%'`.

```php
$criteria = new Criteria();
$criteria->addFilter(new ContainsFilter('name', 'Lightweight'));
```

```json
{
    "filter": [
        { 
            "type": "contains", 
            "field": "name", 
            "value": "Lightweight"
        }    
    ]
}
```

## Range

The `Range` filter allows you to filter a field to a value space. This can work with date or numerical values. Within the `parameter` property the following values are possible:

* `gte` => Greater than equals
* `lte` => Less than equals
* `gt` => Greater than
* `lt` => Less than

The following SQL statement is executed in the background: `WHERE stock >= 20 AND stock <= 30`.

```php
$criteria = new Criteria();
$criteria->addFilter(
    new RangeFilter('stock', [
        RangeFilter::GTE => 20,
        RangeFilter::LTE => 30
    ])
);
```

```json
{
    "filter": [
        { 
            "type": "range", 
            "field": "stock", 
            "parameters": {
                "gte": 20,      
                "lte": 30
            }
        }    
    ]
}
```

## Not

The `Not` Filter is a container which allows to negate any kind of filter. The `operator` allows you to define the combination of queries within the NOT filter (`OR` and `AND`). The following SQL statement is executed in the background: `WHERE !(stock = 1 OR availableStock = 1) AND active = 1`:

```php
$criteria = new Criteria();
$criteria->addFilter(new EqualsFilter('active', true));

$criteria->addFilter(
    new NotFilter(
        NotFilter::CONNECTION_OR,
        [
            new EqualsFilter('stock', 1),
            new EqualsFilter('availableStock', 10)
        ]
    )
);
```

```json
{
    "filter": [
        { 
            "type": "not", 
            "operator": "or",
            "queries": [
                {
                    "type": "equals",
                    "field": "stock",
                    "value": 1
                },
                {
                    "type": "equals",
                    "field": "availableStock",
                    "value": 1
                }    
            ]
        },
        {
            "type": "equals",
            "field": "active",
            "value": true
        }
    ]
}
```

## Multi

The `Multi` Filter is a container, which allows to set logical links between filters. The `operator` allows you to define the links between the queries within the `Multi` filter (`OR` and `AND`). The following SQL statement is executed in the background: `WHERE (stock = 1 OR availableStock = 1) AND active = 1`.

```php
$criteria = new Criteria();
$criteria->addFilter(
    new MultiFilter(
        MultiFilter::CONNECTION_OR,
        [
            new EqualsFilter('stock', 1),
            new EqualsFilter('availableStock', 10)
        ]
    )
);
$criteria->addFilter(
    new EqualsFilter('active', true)
);
```

```javascript
 {
    "filter": [
        { 
            "type": "multi",   
            "operator": "or",
            "queries": [
                {
                    "type": "equals",
                    "field": "stock",
                    "value": 1
                },
                {
                    "type": "equals",
                    "field": "availableStock",
                    "value": 1
                } 
            ]
        },
        {
            "type": "equals",
            "field": "active",
            "value": true
        }
    ]
}
```

## Prefix

The `Prefix` Filter allows you to filter a field to an approximate value, where the passed value must be the start of a full value. The following SQL statement is executed in the background: `WHERE name LIKE 'Lightweight%'`.

```php
$criteria = new Criteria();
$criteria->addFilter(new PrefixFilter('name', 'Lightweight'));
```

```json
{
    "filter": [
        {
            "type": "prefix",
            "field": "name",
            "value": "Lightweight"
        }
    ]
}
```

## Suffix

The `Suffix` Filter allows you to filter a field to an approximate value, where the passed value must be the end of a full value. The following SQL statement is executed in the background: `WHERE name LIKE '%Lightweight'`.

```php
$criteria = new Criteria();
$criteria->addFilter(new SuffixFilter('name', 'Lightweight'));
```

```json
{
    "filter": [
        {
            "type": "suffix",
            "field": "name",
            "value": "Lightweight"
        }
    ]
}
```

In general, the storage systems are **case-insensitive**, meaning that when filtering values to search for a string, the casing of the filter values doesn't affect their handling.

---

---

## Flags Reference
**Source:** [resources/references/core-reference/dal-reference/flags-reference.md](https://developer.shopware.com/docs/v6.6/resources/references/core-reference/dal-reference/flags-reference.md)  
# Flags Reference

| Classname | Description                                                                                                                                                                                                                                                                                                                                     |
| :--- |:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| AllowEmptyString | Flag a text column that an empty string should not be considered as null                                                                                                                                                                                                                                                                        |
| AllowHtml | In case a column is allowed to contain HTML-escaped data. Beware of injection possibilities                                                                                                                                                                                                                                                    |
| ApiAware | Makes a field available in the Store or Admin API. If no parameter is passed for the flag, the field will be exposed in the both Store and Admin API. By default, all fields are enabled for the Admin API, as the flag is added in the base Field class. However, the scope can be restricted to `AdminApiSource` and `SalesChannelApiSource`. |
| CascadeDelete | In case the referenced association data will be deleted, the related data will be deleted too                                                                                                                                                                                                                                                   |
| Computed | The value is computed by indexer or external systems and cannot be written using the DAL.                                                                                                                                                                                                                                                       |
| Deprecated | This flag is used to mark the field that has been deprecated and will be removed with the next major version.                                                                                                                                                                                                                                   |
| Extension | Defines that the data of this field is stored in an Entity::$extension and are not part of the struct itself.                                                                                                                                                                                                                                   |
| Inherited | Defines that the data of this field can be inherited by the parent record                                                                                                                                                                                                                                                                       |
| PrimaryKey | The PrimaryKey flag defines the field as part of the entity's primary key. Usually, this should be the ID field.                                                                                                                                                                                                                                |
| Required | Fields marked as "Required" must be specified during the create request of an entity. This configuration is only taken into account during the write process.                                                                                                                                                                                   |
| RestrictDelete | Associated data with this flag, restricts the delete of the entity in case that a record with the primary key exists.                                                                                                                                                                                                                           |
| ReverseInherited | Flags "ReverseInherited"                                                                                                                                                                                                                                                                                                                        |
| Runtime | Defines that the data of the field will be loaded at runtime by an event subscriber or other class. Used in entity extensions for plugins or not directly fetchable associations.                                                                                                                                                               |
| SearchRanking | Defines the weight for a search query on the entity for this field                                                                                                                                                                                                                                                                              |
| SetNullOnDelete | In case the referenced association data will be deleted, the related data will be set to null and an Written event will be thrown                                                                                                                                                                                                               |
| Since | The "Since" flag defines since which Shopware version the field is available.                                                                                                                                                                                                                                                                   |
| WriteProtected | By setting the "WriteProtected" flag, write access via API can be restricted. This flag is mostly used to protect indexed data from direct writing via API.                                                                                                                                                                                     |

---

---

## Flow Reference
**Source:** [resources/references/core-reference/flow-reference.md](https://developer.shopware.com/docs/v6.6/resources/references/core-reference/flow-reference.md)  
*(Body truncated in this bundle; follow the link for the rest.)*

# Flow Reference

::: info
This functionality is available starting with Shopware 6.4.6.0
:::

| Event                                                  | Description                                                                                       | Actions                                                        |
|--------------------------------------------------------|---------------------------------------------------------------------------------------------------|----------------------------------------------------------------|
| checkout.customer.before.login                         | Triggers as soon as a customer logs in                                                            | No action                                                      |
| checkout.customer.login                                | Triggers as soon as a customer logs in                                                            | Add/remove tag                                                 |
| checkout.customer.logout                               | Triggers when a customer logs out                                                                 | Add/remove tag                                                 |
| checkout.customer.deleted                              | Triggers if a customer gets deleted                                                               | Add/remove tag, send mail                                      |
| user.recovery.request                                  | Triggers when a user created a password recovery request at admin                                 | Send mail                                                      |
| checkout.customer.changed-payment-method               | Triggers when a customer changes his payment method in the checkout process                       | Add/remove tag                                                 |
| checkout.order.placed                                  | Triggers when an order is placed                                                                  | Add/remove tag, send mail, generate document, set order status |
| checkout.order.payment\_method.changed                  | Triggers when a user changed payment method during checkout process                               | No action                                                      |
| customer.recovery.request                              | Triggers when a customer recovers his password                                                    | Add/remove tag, send mail                                      |
| checkout.customer.double\_opt\_in\_registration           | Triggers when a customer commits to his registration via double opt in                            | Add/remove tag, send mail                                      |
| customer.group.registration.accepted                   | Triggers when admin accepted a user who register to join a customer group                         | Add/remove tag, send mail                                      |
| customer.group.registration.declined<                  | Triggers when admin declined a user who register to join a customer group                         | Add/remove tag, send mail                                      |
| checkout.customer.register                             | Triggers when a new customer was registered                                                       | Add/remove tag, send mail                                      |
| checkout.customer.double\_opt\_in\_guest\_order            | Triggers as soon as double opt-in is accepted in a guest order                                    | Add/remove tag, send mail                                      |
| checkout.customer.guest\_register                       | Triggers when a new guest customer was registered                                                 | Add/remove tag, send mail                                      |
| contact\_form.send                                      | Triggers when a contact form is send                                                              | Send mail                                                      |
| mail.after.create.message                              | Triggers when a mail message/ content is created                                                  | No action                                                      |
| mail.before.send                                       | Triggers before a mail is send                                                                    | No action                                                      |
| mail.sent                                              | Triggers when a mail is send from Shopware                                                        | No action                                                      |
| newsletter.confirm                                     | Triggers when newsletter was confirmed by a user                                                  | Send mail                                                      |
| newsletter.register                                    | Triggers when user registered to subscribe to a sales channel newsletter                          | Send mail                                                      |
| newsletter.unsubscribe                                 | Triggers when user unsubscribe from a sales channel newsletter                                    | Send mail                                                      |
| newsletter.update                                      | Deprecated in 6.5.0                                                                               | Send mail                                                      |
| product\_export.log                                     | Triggers when product export is executed                                                          | No action                                                      |
| state\_enter.order\_transaction.state.open               | Triggers when an order payment enters status "Open"                                               | Add/remove tag, send mail, generate document, set order status |
| state\_leave.order\_transaction.state.open               | Triggers when an order payment leaves status "Open"                                               | Add/remove tag, send mail, generate document, set order status |
| state\_enter.order\_transaction.state.paid               | Triggers when an order payment enters status "Paid"                                               | Add/remove tag, send mail, generate document, set order status |
| state\_leave.order\_transaction.state.paid               | Triggers when an order payment leaves status "Paid"                                               | Add/remove tag, send mail, generate document, set order status |
| state\_enter.order\_transaction.state.refunded\_partially | Triggers when an order payment enters status "Refunded partially"                                 | Add/remove tag, send mail, generate document, set order status |
| state\_leave.order\_transaction.state.refunded\_partially | Triggers when an order payment leaves status "Refund partially"                                   | Add/remove tag, send mail, generate document, set order status |
| state\_enter.order\_transaction.state.chargeback         | Triggers when an order payment enters status "Chargeback"                                        | Add/remove tag, send mail, generate document, set order status |
| state\_leave.order\_transaction.state.chargeback         | Triggers when an order payment leaves status "Chargeback"                                         | Add/remove tag, send mail, generate document, set order status |
| state\_enter.order\_transaction.state.paid\_partially     | Triggers when an order payment enters status "Paid partially"                                     | Add/remove tag, send mail, generate document, set order status |
| state\_leave.order\_transaction.state.paid\_partially     | Triggers when an order payment leaves status "Paid partially"                                     |                                                                |
| state\_enter.order\_transaction.state.failed             | Triggers when an order payment enters status "Failed"                                             | Add/remove tag, send mail, generate document, set order status |
| state\_leave.order\_transaction.state.failed             | Triggers when an order payment leaves status "Failed"                                             | Add/remove tag, send mail, generate document, set order status |
| state\_enter.order\_transaction.state.reminded           | Triggers when an order payment enters status "Reminded"                                           | Add/remove tag, send mail, generate document, set order status |
| state\_leave.order\_transaction.state.reminded<          | Triggers when an order payment leaves status "Reminded"                                           | Add/remove tag, send mail, generate document, set order status |
| state\_enter.order\_transaction.state.authorized         | Triggers when an order payment enters status "Authorized"                                         | Add/remove tag, send mail, generate document, set order status |
| state\_leave.order\_transaction.state.authorized         | Triggers when an order payment leaves status "Authorized"                                         | Add/remove tag, send mail, generate document, set order status |
| state\_enter.order\_transaction.state.cancelled          | Triggers when an order payment enters status "Cancelled"                                          | Add/remove tag, send mail, generate document, set order status |
| state\_leave.order\_transaction.state.cancelled          | Triggers when an order payment leaves status "Cancelled"                                          | Add/remove tag, send mail, generate document, set order status |
| state\_enter.order\_transaction.state.refunded           | Triggers when an order payment enters status "Refunded"                                           | Add/remove tag, send mail, generate document, set order status |
| state\_leave.order\_transaction.state.refunded           | Triggers when an order payment leaves status "Refunded"                                           | Add/remove tag, send mail, generate document, set order status |
| state\_enter.order\_transaction.state.in\_progress        | Triggers when an order payment enters status "In progress"                                        | Add/remove tag, send mail, generate document, set order status |
| state\_leave.order\_transaction.state.in\_progress        | Triggers when an order payment leaves status "In progress"                                        | Add/remove tag, send mail, generate document, set order status |
| state\_enter.order\_delivery.state.returned\_partially    | Triggers when an order delivery enters status "Return partially"                                  | Add/remove tag, send mail, generate document, set order status |
| state\_leave.order\_delivery.state.returned\_partially    | Triggers when an order delivery leaves status "Return partially"                                  | Add/remove tag, send mail, generate document, set order status |
| state\_enter.order\_delivery.state.returned              | Triggers when an order delivery enters status "Returned"                                          | Add/remove tag, send mail, generate document, set order status |
| state\_leave.order\_delivery.state.returned              | Triggers when an order delivery leaves status "Returned"                                          | Add/remove tag, send mail, generate document, set order status |
| state\_enter.order\_delivery.state.cancelled             | Triggers when an order delivery enters status "Cancelled"                                         | Add/remove tag, send mail,

… **Truncated.** Full document: https://developer.shopware.com/docs/v6.6/resources/references/core-reference/flow-reference.md


---

## Rules Reference
**Source:** [resources/references/core-reference/rules-reference.md](https://developer.shopware.com/docs/v6.6/resources/references/core-reference/rules-reference.md)  
*(Body truncated in this bundle; follow the link for the rest.)*

# Rules Reference

List of all rule classes across Shopware 6.

## Checkout

| Class                                                                                                                                                                       | Description |
|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------| :--- |
| [Shopware\Core\Checkout\Cart\Rule\AlwaysValidRule](https://github.com/shopware/shopware/blob/trunk/src/Core/Checkout/Cart/Rule/AlwaysValidRule.php)                         | Matches always |
| [Shopware\Core\Checkout\Cart\Rule\CartAmountRule](https://github.com/shopware/shopware/blob/trunk/src/Core/Checkout/Cart/Rule/CartAmountRule.php)                           | Matches a specific number to the carts total price. |
| [Shopware\Core\Checkout\Cart\Rule\CartHasDeliveryFreeItemRule](https://github.com/shopware/shopware/blob/trunk/src/Core/Checkout/Cart/Rule/CartHasDeliveryFreeItemRule.php) | Matches if the cart has a free delivery item. |
| [Shopware\Core\Checkout\Cart\Rule\CartWeightRule](https://github.com/shopware/shopware/blob/trunk/src/Core/Checkout/Cart/Rule/CartWeightRule.php)                           | Matches a specific number to the current cart's total weight. |
| [Shopware\Core\Checkout\Cart\Rule\GoodsCountRule](https://github.com/shopware/shopware/blob/trunk/src/Core/Checkout/Cart/Rule/GoodsCountRule.php)                           | Matches a number to the current cart's line item goods count. |
| [Shopware\Core\Checkout\Cart\Rule\GoodsPriceRule](https://github.com/shopware/shopware/blob/trunk/src/Core/Checkout/Cart/Rule/GoodsPriceRule.php)                           | Matches a specific number to the carts goods price. |
| [Shopware\Core\Checkout\Cart\Rule\LineItemClearanceSaleRule](https://github.com/shopware/shopware/blob/trunk/src/Core/Checkout/Cart/Rule/LineItemClearanceSaleRule.php)     | Matches a specific line item which is on clearance sale |
| [Shopware\Core\Checkout\Cart\Rule\LineItemCreationDateRule](https://github.com/shopware/shopware/blob/trunk/src/Core/Checkout/Cart/Rule/LineItemCreationDateRule.php)       | Matches if a line item has a specific creation date. |
| [Shopware\Core\Checkout\Cart\Rule\LineItemCustomFieldRule](https://github.com/shopware/shopware/blob/trunk/src/Core/Checkout/Cart/Rule/LineItemCustomFieldRule.php)         | Matches if a line item has a specific custom field. |
| [Shopware\Core\Checkout\Cart\Rule\LineItemDimensionHeightRule](https://github.com/shopware/shopware/blob/trunk/src/Core/Checkout/Cart/Rule/LineItemDimensionHeightRule.php) | Matches a specific line item's height. |
| [Shopware\Core\Checkout\Cart\Rule\LineItemDimensionLengthRule](https://github.com/shopware/shopware/blob/trunk/src/Core/Checkout/Cart/Rule/LineItemDimensionLengthRule.php) | Matches a specific line item's length. |
| [Shopware\Core\Checkout\Cart\Rule\LineItemDimensionWeightRule](https://github.com/shopware/shopware/blob/trunk/src/Core/Checkout/Cart/Rule/LineItemDimensionWeightRule.php) | Matches a specific line item's weight. |
| [Shopware\Core\Checkout\Cart\Rule\LineItemDimensionWidthRule](https://github.com/shopware/shopware/blob/trunk/src/Core/Checkout/Cart/Rule/LineItemDimensionWidthRule.php)   | Matches a specific line item's width. |
| [Shopware\Core\Checkout\Cart\Rule\LineItemGroupRule](https://github.com/shopware/shopware/blob/trunk/src/Core/Checkout/Cart/Rule/LineItemGroupRule.php)                     | Matches if a line item has a specific group. |
| [Shopware\Core\Checkout\Cart\Rule\LineItemInCategoryRule](https://github.com/shopware/shopware/blob/trunk/src/Core/Checkout/Cart/Rule/LineItemInCategoryRule.php)           | Matches if a line item is in a specific category. |
| [Shopware\Core\Checkout\Cart\Rule\LineItemIsNewRule](https://github.com/shopware/shopware/blob/trunk/src/Core/Checkout/Cart/Rule/LineItemIsNewRule.php)                     | Matches if a line item is marked as new. |
| [Shopware\Core\Checkout\Cart\Rule\LineItemListPriceRule](https://github.com/shopware/shopware/blob/trunk/src/Core/Checkout/Cart/Rule/LineItemListPriceRule.php)             | Matches a specific line item has a specific list price. |
| [Shopware\Core\Checkout\Cart\Rule\LineItemOfManufacturerRule](https://github.com/shopware/shopware/blob/trunk/src/Core/Checkout/Cart/Rule/LineItemOfManufacturerRule.php)   | Matches a specific line item has a specific manufacturer. |
| [Shopware\Core\Checkout\Cart\Rule\LineItemOfTypeRule](https://github.com/shopware/shopware/blob/trunk/src/Core/Checkout/Cart/Rule/LineItemOfTypeRule.php)                   | Matches a specific type name to the line item's type. |
| [Shopware\Core\Checkout\Cart\Rule\LineItemPromotedRule](https://github.com/shopware/shopware/blob/trunk/src/Core/Checkout/Cart/Rule/LineItemPromotedRule.php)               | Matches if a line item is promoted. |
| [Shopware\Core\Checkout\Cart\Rule\LineItemPropertyRule](https://github.com/shopware/shopware/blob/trunk/src/Core/Checkout/Cart/Rule/LineItemPropertyRule.php)               | Matches if a line item has a specific property. |
| [Shopware\Core\Checkout\Cart\Rule\LineItemPurchasePriceRule](https://github.com/shopware/shopware/blob/trunk/src/Core/Checkout/Cart/Rule/LineItemPurchasePriceRule.php)     | Matches if a line item has a specific purchase price. |
| [Shopware\Core\Checkout\Cart\Rule\LineItemReleaseDateRule](https://github.com/shopware/shopware/blob/trunk/src/Core/Checkout/Cart/Rule/LineItemReleaseDateRule.php)         | Matches a specific line item's release date. |
| [Shopware\Core\Checkout\Cart\Rule\LineItemRule](https://github.com/shopware/shopware/blob/trunk/src/Core/Checkout/Cart/Rule/LineItemRule.php)                               | Matches multiple identifiers to a line item's keys. True if one identifier matches. |
| [Shopware\Core\Checkout\Cart\Rule\LineItemTagRule](https://github.com/shopware/shopware/blob/trunk/src/Core/Checkout/Cart/Rule/LineItemTagRule.php)                         | Matches multiple tags to a line item's tag. True if one tag matches. |
| [Shopware\Core\Checkout\Cart\Rule\LineItemTaxationRule](https://github.com/shopware/shopware/blob/trunk/src/Core/Checkout/Cart/Rule/LineItemTaxationRule.php)               | Matches if a line item has a specific tax. |
| [Shopware\Core\Checkout\Cart\Rule\LineItemTotalPriceRule](https://github.com/shopware/shopware/blob/trunk/src/Core/Checkout/Cart/Rule/LineItemTotalPriceRule.php)           | Matches a number to the current cart's line item total price. |
| [Shopware\Core\Checkout\Cart\Rule\LineItemUnitPriceRule](https://github.com/shopware/shopware/blob/trunk/src/Core/Checkout/Cart/Rule/LineItemUnitPriceRule.php)             | Matches a specific number to a line item's price. |
| [Shopware\Core\Checkout\Cart\Rule\LineItemWithQuantityRule](https://github.com/shopware/shopware/blob/trunk/src/Core/Checkout/Cart/Rule/LineItemWithQuantityRule.php)       | Matches a specific line item's quantity to the current line item's quantity. |
| [Shopware\Core\Checkout\Cart\Rule\LineItemWrapperRule](https://github.com/shopware/shopware/blob/trunk/src/Core/Checkout/Cart/Rule/LineItemWrapperRule.php)                 | Internally handled scope changes. |
| [Shopware\Core\Checkout\Cart\Rule\LineItemsInCartCountRule](https://github.com/shopware/shopware/blob/trunk/src/Core/Checkout/Cart/Rule/LineItemsInCartCountRule.php)       | Matches a number to the current cart's line item count. |
| [Shopware\Core\Checkout\Cart\Rule\LineItemsInCartCountRule](https://github.com/shopware/shopware/blob/trunk/src/Core/Checkout/Cart/Rule/LineItemsInCartCountRule.php)                | Matches multiple identifiers to a carts line item's identifier. True if one identifier matches. |
| [Shopware\Core\Checkout\Cart\Rule\PaymentMethodRule](https://github.com/shopware/shopware/blob/trunk/src/Core/Checkout/Cart/Rule/PaymentMethodRule.php)                     | Matches if a specific payment method is used |
| [Shopware\Core\Checkout\Cart\Rule\ShippingMethodRule](https://github.com/shopware/shopware/blob/trunk/src/Core/Checkout/Cart/Rule/ShippingMethodRule.php)                   | Matches if a specific shipping method is used |
| [Shopware\Core\Checkout\Customer\Rule\BillingCountryRule](https://github.com/shopware/shopware/blob/trunk/src/Core/Checkout/Customer/Rule/BillingCountryRule.php)           | Matches multiple countries to the customer's active billing address country. |
| [Shopware\Core\Checkout\Customer\Rule\BillingStreetRule](https://github.com/shopware/shopware/blob/trunk/src/Core/Checkout/Customer/Rule/BillingStreetRule.php)             | Matches multiple street names to the customer's active billing address street name. |
| [Shopware\Core\Checkout\Customer\Rule\BillingZipCodeRule](https://github.com/shopware/shopware/blob/trunk/src/Core/Checkout/Customer/Rule/BillingZipCodeRule.php)           | Matches multiple zip codes to the customer's active billing address zip code. |
| [Shopware\Core\Checkout\Customer\Rule\CustomerGroupRule](https://github.com/shopware/shopware/blob/trunk/src/Core/Checkout/Customer/Rule/CustomerGroupRule.php)             | Matches multiple customer groups to the current customers group. True if one customer group matches. |
| [Shopware\Core\Checkout\Customer\Rule\CustomerNumberRule](https://github.com/shopware/shopware/blob/trunk/src/Core/Checkout/Customer/Rule/CustomerNumberRule.php)           | Matches multiple numbers to the active customers number. |
| [Shopware\Core\Checkout\Customer\Rule\CustomerTagRule](https://github.com/shopware/shopware/blob/trunk/src/Core/Checkout/Customer/Rule/CustomerTagRule.php)                 | Matches a tag set to customers |
| [Shopware\Core\Checkout\Customer\Rule\DaysSinceLastOrderRule](https://github.com/shopware/shopware/blob/trunk/src/Core/Checkout/Customer/Rule/DaysSinceLastOrderRule.php)   | Matches a specific number of days to the last order creation date. |
| [Shopware\Core\Checkout\Customer\Rule\DifferentAddressesRule](https://github.com/shopware/shopware/blob/trunk/src/Core/Checkout/Customer/Rule/DifferentAddressesRule.php)   | Matches if active billing address is not the default. |
| [Shopware\Core\Checkout\Customer\Rule\IsCompanyRule](https://github.com/shopware/shopware/blob/trunk/src/Core/Checkout/Customer/Rule/IsCompanyRule.php)                     | Matches if the customer is a company |
| [Shopware\Core\Checkout\Customer\Rule\IsNewCustomerRule](https://github.com/shopware/shopware/blob/trunk/src/Core/Checkout/Customer/Rule/IsNewCustomerRule.php)             | Matches if a customer is new, by matching the `firstLogin` property with today. |
| [Shopware\Core\Checkout\Customer\Rule\LastNameRule](https://github.com/shopware/shopware/blob/trunk/src/Core/Checkout/Customer/Rule/LastNameRule.php)                       | Exactly matches a string to the customer's last name. |
| [Shopware\Core\Checkout\Customer\Rule\OrderCountRule](https://github.com/shopware/shopware/blob/trunk/src/Core/Checkout/Customer/Rule/OrderCountRule.php)                   | Matches a specific number to the number of orders of the current customer. |
| [Shopware\Core\Checkout\Customer\Rule\ShippingCountryRule](https://github.com/shopware/shopware/blob/trunk/src/Core/Checkout/Customer/Rule/ShippingCountryRule.php)         | Matches multiple countries to the customer's active shipping address country. True if one country matches. |
| [Shopware\Core\Checkout\Customer\Rule\ShippingStreetRule](https://github.com/shopware/shopware/blob/trunk/src/Core/Checkout/Customer/Rule/ShippingStreetRule.php)           | Matches multiple street names to the customer's active shipping address street name. True if one street name matches. |
| [Shopware\Core\Checkout\Customer\Rule\ShippingZipCodeRule](https://github.com/shopware/shopware/blob/trunk/src/Core/Checkout/Customer/Rule/ShippingZipCodeRule.php)         | Matches multiple zip codes to the customer's ac

… **Truncated.** Full document: https://developer.shopware.com/docs/v6.6/resources/references/core-reference/rules-reference.md


---

## Storefront Reference
**Source:** [resources/references/storefront-reference.md](https://developer.shopware.com/docs/v6.6/resources/references/storefront-reference.md)  
# Storefront Reference

The storefront reference documents functions, filters, and extensions that are available for customizing storefronts. It helps you understand how to use these features to enhance the functionality and appearance of your storefront.

---

---

## Storefront plugins and helper
**Source:** [resources/references/storefront-reference/plugin-reference.md](https://developer.shopware.com/docs/v6.6/resources/references/storefront-reference/plugin-reference.md)  
*(Body truncated in this bundle; follow the link for the rest.)*

# Storefront plugins and helper

This is a list of available javascript plugins and helpers that can be used and extended.

## Plugins

| Plugin                                 | Description                                                                                                                                                                                       | Notes                            |
|:---------------------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:---------------------------------|
| `AccountGuestAbortButtonPlugin`        | Used on the logout button to fire a `guest-logout` event after logging out from a guest session.                                                                                                  | ---                              |
| `AddToCartPlugin`                      | Submits the form that adds a product to the cart and opens the OffCanvasCart. E.g., used on product buy buttons.                                                                                   | ---                              |
| `AddToWishlistPlugin`                  | Adds or removes a product from the wishlist and toggles the indicator (heart icon) that displays if the current product is on the wishlist. Also updates the wishlist counter in the main header. | ---                              |
| `AddressEditorPlugin`                  | Opens a modal to edit the billing or shipping address.                                                                                                                                            | ---                              |
| `AjaxModalPlugin`                      | This class extends the Bootstrap modal functionality by adding an event listener to modal triggers that contain a special "data-url" attribute which is needed to load the modal content by AJAX. | ---                              |
| `BaseSliderPlugin`                     | Provides basic slider functionality to a container with sliding elements. Uses the "tiny-slider" framework in the background.                                                                     | ---                              |
| `BaseWishlistStoragePlugin`            | Provides basic storage logic to add, remove and get products from the wishlist. Used by the local storage wishlist (if user is guest) and the persisted wishlist (if used is logged in).            | ---                              |
| `BasicCaptchaPlugin`                   | Provides the JS functionality for the basic captcha that can be activated in storefront sales channel. Only works with a corresponding form.                                                    | ---                              |
| `BuyBoxPlugin`                         | Refreshes the buy box area on the product detail page after switching to a different product variant. Re-initializes the tax info modal.                                                          | ---                              |
| `CartWidgetPlugin`                     | Controls the cart widget in the main header that displays the total cart amount. Updates automatically if a product is added to the cart.                                                         | ---                              |
| `ClearInputPlugin`                     | Adds clear functionality to input fields.                                                                                                                                                         | ---                              |
| `CmsGdprVideoElement`                  | Shows a consent overlay before rendering an external CMS video element, e.g. from YouTube. Only when the user provides consent, the actual video will be loaded.                                           | ---                              |
| `CollapseCheckoutConfirmMethodsPlugin` | Displays a "show more" button when too many shipping or payment methods are shown. Used on the checkout page.                                                                                     | ---                              |
| `CollapseFooterColumnsPlugin`          | Enables collapsing containers (accordion) on mobile viewports for the columns in the page footer.                                                                                                 | ---                              |
| `CookieConfiguration`                  | Controls the detailed cookie configuration (displayed in an OffCanvas). Displays the available cookies with checkboxes and saves the selected user preference.                                    | ---                              |
| `CookiePermissionPlugin`               | Controls the cookie banner at the bottom of the page when no cookie preference is set. Can either save a preference directly via button or open the cookie configuration OffCanvas.               | ---                              |
| `CountryStateSelectPlugin`             | Renders an additional select box with country states (e.g. "North-Rhine-Westphalia") if a country was selected. E.g., used in the registration form.                                               | ---                              |
| `CrossSellingPlugin`                   | Used to re-initialize the product sliders when toggling between different cross-selling tabs that contain product sliders.                                                                        | ---                              |
| `DateFormat`                           | This plugin formats a date and converts it to the local timezone if the data attribute date-format is set.                                                                                        | ---                              |
| `DatePickerPlugin`                     | Controls the date picker component. Shows a datepicker UI when applied to an input field.                                                                                                         | ---                              |
| `EllipsisPlugin`                       | Used to expand or shrink a text.                                                                                                                                                                  | Deprecated and removed in v6.6.0 |
| `FadingPlugin`                         | Collapses or expands a Bootstrap collapse container with additional "more" or "less" links.                                                                                                       | Deprecated and removed in v6.6.0 |
| `FilterBasePlugin`                     | Provides basic functionality for a product listing filter. Communicates with the `ListingPlugin`. Other filters like "multi select" extend from this plugin class.                                | ---                              |
| `FlyoutMenuPlugin`                     | This Plugin handles the subcategory display of the main navigation.                                                                                                                               | ---                              |
| `FormAddHistoryPlugin`                 | Provides an API to push items into the browser history after a form was submitted. Only works on a `<form>` element.                                                                              | ---                              |
| `FormAjaxSubmitPlugin`                 | This plugin submits a form with ajax without reloading the page, instead of performing a regular form submit.                                                                                     | ---                              |
| `FormAutoSubmitPlugin`                 | This plugin automatically submits a form, when the element or the form itself has changed.                                                                                                        | ---                              |
| `FormCmsHandler`                       | Sends forms from the CMS (e.g. contact form) via ajax and renders additional error/success messages.                                                                                              | ---                              |
| `FormFieldTogglePlugin`                | Provides functionality to display or hide additional form fields without reloading the page. E.g., used in the registration form when shipping and billing addresses are different.                  | ---                              |
| `FormPreserverPlugin`                  | This plugin preserves a form, if the element or the form itself has changed. After a reload of the page the form is filled up with the stored values.                                             | ---                              |
| `FormScrollToInvalidFieldPlugin`       | This plugin scrolls to invalid form fields when the form is submitted.                                                                                                                            | ---                              |
| `FormSubmitLoaderPlugin`               | This plugin shows a loading indicator on the form submit button when the form is submitted.                                                                                                       | ---                              |
| `FormValidation`                       | This plugin validates fields of a form. Also styles the field elements with the bootstrap style if enabled.                                                                                       | ---                              |
| `GoogleAnalyticsPlugin`                | Adds all events for Google Analytics and configures the `gtag`. Only used when "Analytics" is activated in the sales channel.                                                                     | ---                              |
| `GoogleReCaptchaBasePlugin`            | Provides basic functionality to apply a Google reCAPTCHA to a `<form>` element. The JS-plugins for reCAPTCHA v2 and v3 extend this plugin.                                                        | ---                              |
| `GuestWishlistPagePlugin`              | Used on the `/wishlist` page/route to display the products currently on the wishlist. Displays wishlist items from local storage if the user is a guest.                                          | ---                              |
| `ImageZoomPlugin`                      | Enables functionality to zoom into an image, e.g. using the mouse wheel. Used inside the image zoom modal on the product detail page. Works together with `ZoomModalPlugin`.                      | ---                              |
| `ListingPlugin`                        | Provides the filter functionality of the product listing. Gets the current values of each filter, current sorting and pagination. Generates the requests and displays the new results.            | ---                              |
| `MagnifierPlugin`                      | Handles the magnifier lens functionality on the detail page.                                                                                                                                      | ---                              |
| `OffCanvasAccountMenu`                 | Opens the account dropdown menu ("user avatar" icon in header) inside an OffCanvas on mobile viewports.                                                                                           | ---                              |
| `OffCanvasCartPlugin`                  | Opens the shopping cart in an OffCanvas. Used on the shopping cart display in the main header.                                                                                                    | ---                              |
| `OffCanvasFilter`                      | Opens the listing filters

… **Truncated.** Full document: https://developer.shopware.com/docs/v6.6/resources/references/storefront-reference/plugin-reference.md


---

## Shopware's twig functions
**Source:** [resources/references/storefront-reference/twig-function-reference.md](https://developer.shopware.com/docs/v6.6/resources/references/storefront-reference/twig-function-reference.md)  
# Shopware's twig functions

In Shopware, we extend Twig's functionality by custom ones. See our own actions below.

::: warning

## No official support for the twig {% use %} tag

Try to avoid importing blocks from the core templates with the {% use %} tag for horizontal reuse in twig. [Twig documentation - use tag](https://twig.symfony.com/doc/3.x/tags/use.html).

The {% use %} tag does not consider the template inheritance similar to {% sw\_extends %}\`.

Furthermore, templates which are imported via {% use %} are not allowed to have additional twig statements outside of twig blocks. Therefore, changes in core templates which are imported via {% use %} might break your app or plugin.
:::

### Functions

| Function | Description | Notes |
| :--- | :--- | :--- |
| `sw_extends` | Inherits from another file with support for multi inheritance. The API is the same like in twigs default `extends` | --- |
| `sw_include` | Includes template partials with support for multi inheritance. The API is the same like in twigs default `include` | --- |
| `sw_icon` | Displays an icon from a given icon set | See [Add custom icon](../../../guides/plugins/plugins/storefront/add-icons#adding-icon) guide for details. |
| `sw_thumbnails` | Renders a  tag with correctly configured “srcset” and “sizes” attributes based on the provided parameters | See [Add thumbnail](../../../guides/plugins/plugins/storefront/use-media-thumbnails) guide for more information. |
| `config` | Gets a value from the system config (used by plugins and global settings) for the given sales channel |  See [Reading the configuration values](../../../guides/plugins/apps/configuration) |
| `theme_config` | Gets a value from the current theme |  See [Theme configuration](../../../guides/plugins/themes/theme-configuration) |

### Filter

| Filter | Description | Notes |
| :--- | :--- | :--- |
| `replace_recursive` | Enables recursive replacement in addition to twig's default `replace` filter | To see an example, see the guide on [add custom JavaScript](../../../guides/plugins/plugins/storefront/add-custom-javascript) |
| `currency` | Adopts currency formatting: The currency symbol and the comma setting. | --- |
| `sw_sanitize` | Filters tags and attributes from a given string. By default, twig's auto escaping is on, so this filter explicitly allows basic HTML tags like \<i%gt;, \<b>,... | --- |

### Extensions

| Extension | Description | Notes |
| :--- | :--- | :--- |
| `sw_breadcrumb_full()` | Returns all categories defined in the breadcrumb as an array | Contains functionalities of `sw_breadcrumb_types` and `sw_breadcrumb_build_types` |
| `sw_breadcrumb()` | Returns the category tree as array. Entry points of the SalesChannel ( e.g. footer, navigation) are filtered out. | Deprecated in 6.5.0 |
| `sw_breadcrumb_types()` | Yields the types of the categories within the breadcrumb | Deprecated in 6.5.0 |
| `sw_breadcrumb_build_types()` | returns the same as sw\_breadcrumb\_types, only without another repository call | Deprecated in 6.5.0 |
| `seoUrl()` | Returns seo URL of given route | --- |
| `searchMedia()` | Resolves media ids to media objects | See [Add media](../../../guides/plugins/plugins/storefront/use-media-thumbnails) guide for details. |
| `rawUrl()` | Returns full URL | --- |

---

---

## Testing Reference
**Source:** [resources/references/testing-reference.md](https://developer.shopware.com/docs/v6.6/resources/references/testing-reference.md)  
# Testing Reference

In this reference, all Shopware commands provided by [E2E-testsuite-platform](https://github.com/shopware/e2e-testsuite-platform) or [Shopware Platform](https://github.com/shopware/shopware) are listed here.

---

---

## E2E Commands
**Source:** [resources/references/testing-reference/e2e-commands.md](https://developer.shopware.com/docs/v6.6/resources/references/testing-reference/e2e-commands.md)  
# E2E Commands

| Command                               | Description                                                      |
|:--------------------------------------|:-----------------------------------------------------------------|
| `bin/console e2e:restore-db`          | Sets Shopware back to state of the backup                        |
| `APP_ENV=e2e bin/console e2e:dump-db` | Creates a backup of Shopware's database                          |
| `composer run e2e:setup`              | Prepares Shopware installation and environment for Cypress usage |
| `composer run e2e:open`               | Opens Cypress' e2e tests runner                                  |
| `composer run e2e:prepare`            | Install dependencies and prepare database for Cypress usage      |
| `composer e2e:cypress -- run --spec="cypress/e2e/administration/**/*.cy.js"`          | Runs Cypress' admin e2e tests in CLI                             |
| `composer e2e:cypress -- run --spec="cypress/e2e/storefront/**/*.cy.js"`     | Runs Cypress' storefront e2e tests in CLI                        |

---

---

## Custom E2E Commands
**Source:** [resources/references/testing-reference/e2e-custom-commands.md](https://developer.shopware.com/docs/v6.6/resources/references/testing-reference/e2e-custom-commands.md)  
# Custom E2E Commands

## General commands

| Command | Parameter | Description |
| :--- | :--- | :--- |
| setLocaleToEnGb | - | Switches administration UI locale to EN\_GB |
| login | `(userType)` | Logs in to the Administration manually |
| typeAndCheck | `(textToType)` | Types in an input element and checks if the content was correctly typed |
| clearTypeAndCheck | `(textToType)` | Clears field, types in an input element and checks if the content was correctly typed |
| typeMultiSelectAndCheck | `(textToType, { searchTerm: searchTerm })` | Types in a sw-select field and checks if the content was correctly typed (multi select) |
| typeSingleSelect | `(textToType, selector)` | Types in an sw-select field (single select) |
| typeSingleSelectAndCheck | `(textToType, selector)` | Types in an sw-select field and checks if the content was correctly typed (single select) |
| typeLegacySelectAndCheck | `(textToType, { searchTerm: searchTerm })` | Types in an legacy swSelect field and checks if the content was correctly typed |
| typeAndCheckSearchField | `(searchTerm)` | Types in the global search field and verify search terms in url |
| awaitAndCheckNotification | `(message)` | Wait for a notification to appear and check its message |
| clickContextMenuItem | `(actionInMenuSelector, openMenuSelector, scope = '')` | Click context menu in order to cause a desired action |
| clickMainMenuItem | `({ targetPath, mainMenuId, subMenuId })` | Navigate to module by clicking the corresponding main menu item |
| openUserActionMenu | `({ targetPath, mainMenuId, subMenuId })` | Click user menu to open it up |
| dragTo | `(target)` | Drags the previous subject element to a target, performing a drag and drop operation |
| onlyOnFeature | `(feature)` | Only run the test (skip otherwise) if the feature is activated |
| skipOnFeature | `(feature)` | Skip the test if the feature is activated |

## Storefront-related / Sales Channel API commands

| Command | Parameter | Description |
| :--- | :--- | :--- |
| getSalesChannelId | - | Get the sales channel Id via Admin API |
| storefrontApiRequest | `(method, endpoint, header = {}, body = {})` | Performs Storefront API Requests |
| getRandomProductInformationForCheckout | - | Returns random product with id, name and url to view product |

## System Commands

| Command | Parameter | Description |
| :--- | :--- | :--- |
| activateShopwareTheme | - | Activates Shopware theme for Cypress test runner |
| cleanUpPreviousState | - | Cleans up any previous state by restoring database and clearing caches |
| openInitialPage | - | Opens up the administration initially and waits for the "me" call to be successful |

## API commands

| Command | Parameter | Description |
| :--- | :--- | :--- |
| authenticate | - | Authenticate towards the Shopware API |
| loginViaApi | - | Logs in silently using Shopware API |
| searchViaAdminApi | `(data)` | Search for an existing entity using Shopware API at the given endpoint |
| requestAdminApi | `(method, url, requestData)` | Handling API requests |
| updateViaAdminApi | `(endpoint, id, data)` | Updates an existing entity using Shopware API at the given endpoint |

## Fixture commands

| Command | Parameter | Description |
| :--- | :--- | :--- |
| setToInitialState | - | Sets Shopware back to its initial state if using platform E2E backup routine |
| createDefaultFixture | `(endpoint, data = {}, jsonPath)` | Create entity using Shopware API via given endpoint |
| createProductFixture | `(userData = {})` | Create product fixture using Shopware API via given endpoint |
| createCategoryFixture | `(userData = {})` | Create category fixture using Shopware API via given endpoint |
| createSalesChannelFixture | `(userData = {}` | Create sales channel fixture using Shopware API via given endpoint |
| setSalesChannelDomain | `(salesChannelName = 'Storefront')` | Create sales channel domain using Shopware API at the given endpoint |
| createCustomerFixture | `(userData = {})` | Create customer fixture using Shopware API via given endpoint |
| createCmsFixture | `(userData = {})` | Create cms fixture using Shopware API at the given endpoint |
| createPropertyFixture | `(options, userData)` | Create property fixture using Shopware API at the given endpoint |
| createLanguageFixture | - | Create language fixture using Shopware API at the given endpoint |
| createShippingFixture | `(userData)` | Create shipping fixture using Shopware API at the given endpoint |
| createSnippetFixture | - | Create snippet fixture using Shopware API at the given endpoint |
| createGuestOrder | `productId, userData)` | Create guest order fixture |
| setProductFixtureVisibility | `(productName, categoryName)` | Sets category and visibility for a product in order to set it visible in the Storefront |

---

---

## PSH E2E Commands
**Source:** [resources/references/testing-reference/e2e-psh-commands.md](https://developer.shopware.com/docs/v6.4/resources/references/testing-reference/e2e-psh-commands.md)  
# PSH E2E Commands

| Command | Description |
| :--- | :--- |
| `./psh.phar e2e:cleanup` | Sets Shopware back to state of the backup |
| `./psh.phar e2e:dump-db` | Creates a backup of Shopware's database |
| `./psh.phar e2e:init` | Prepares Shopware installation and environment for Cypress usage |
| `./psh.phar e2e:open` | Opens Cypress' e2e tests runner |
| `./psh.phar e2e:prepare-environment` | Install dependencies and prepare database for Cypress usage |
| `./psh.phar e2e:prepare-shopware` | Prepare shopware installation for Cypress usage |
| `./psh.phar e2e:restore-db` | Restores shopware backup |
| `./psh.phar e2e:run` | Runs Cypress' e2e tests in CLI |

---

---

