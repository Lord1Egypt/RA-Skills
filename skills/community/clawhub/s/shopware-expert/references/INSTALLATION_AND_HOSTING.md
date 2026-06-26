# INSTALLATION AND HOSTING

Compiled excerpts from the Shopware Developer Documentation snapshot. Prefer live docs at [developer.shopware.com](https://developer.shopware.com/) when in doubt.

---

## Hosting
**Source:** [guides/hosting.md](https://developer.shopware.com/docs/v6.6/guides/hosting.md)  
# Hosting

Setting up an operating environment for Shopware can be hard, but it doesn't have to be if you follow some general guidelines in the subsequent sections.

---

---

## Configurations
**Source:** [guides/hosting/configurations.md](https://developer.shopware.com/docs/v6.6/guides/hosting/configurations.md)  
# Configurations

## Overview

When running Shopware 6 there are various configuration options you can use to customize your installation.

## Configuration

The configuration for Shopware 6 resides in the general bundle configuration:

```text
<project root>
└── config
   └── packages
      └── shopware.yaml
```

If you want to aim at a specific environment, you can create a configuration file for that as follows:

```text
<project root>
└── config
   └── packages
      └── dev
         └── mailer.yaml
```

```text
<project root>
└── config
   └── packages
      └── prod
         └── mailer.yaml
```

For more information on environment-specific configurations, check out the [Symfony Configuration Environments](https://symfony.com/doc/current/configuration.html#configuration-environments) section.

---

---

## Framework configurations
**Source:** [guides/hosting/configurations/framework.md](https://developer.shopware.com/docs/v6.6/guides/hosting/configurations/framework.md)  
# Framework configurations

## Overview

Framework configurations are originated in the [Symfony FrameworkBundle](https://symfony.com/doc/current/reference/configuration/framework.html) and are partially documented in this guide.

---

---

## Custom routes
**Source:** [guides/hosting/configurations/framework/routes.md](https://developer.shopware.com/docs/v6.6/guides/hosting/configurations/framework/routes.md)  
# Custom routes

## Overview

Your default routes in Shopware 6 are defined in the controllers of the core or your plugins. An example could be the wishlist route:

```php
<?php declare(strict_types=1);

#[Route(path: '/wishlist', name: 'frontend.wishlist.page', options: ['seo' => false], defaults: ['_noStore' => true], methods: ['GET'])]
public function index(Request $request, SalesChannelContext $context): Response
{
    $customer = $context->getCustomer();

    if ($customer !== null && $customer->getGuest() === false) {
        $page = $this->wishlistPageLoader->load($request, $context, $customer);
        $this->hook(new WishlistPageLoadedHook($page, $context));
    } else {
        $page = $this->guestPageLoader->load($request, $context);
        $this->hook(new GuestWishlistPageLoadedHook($page, $context));
    }

    return $this->renderStorefront('@Storefront/storefront/page/wishlist/index.html.twig', ['page' => $page]);
}
```

It defines that your wishlist page is available at `/wishlist`. This is fine for an English-only shop, but for a multilingual shop, you might want to have a different route for each language.

For example, you could have `/wishlist` for English and `/merkliste` for German.

## Configuration

To easily configure those routes, you can use the `routes.yaml` file in ROOT/config/routes/routes.yaml. Symfony loads this file, which allows you to define your custom `paths`, in our case, for the wishlist index page.

```yaml
frontend.wishlist.page:
  path:
    en-GB: '/wishlist'
    de-DE: '/merkliste'
  controller: 'Shopware\Storefront\Controller\WishlistController::index'
  methods: ['GET']
  defaults:
    _noStore: true
    _routeScope: ['storefront']
  options:
    seo: false
```

You can configure the `path` with the **locales** (for example, `de-DE`) your shop uses.

If you want to learn more about routes in Symfony, check out the [Symfony documentation](https://symfony.com/doc/current/routing.html#creating-routes-as-attributes).

---

---

## SameSite protection
**Source:** [guides/hosting/configurations/framework/samesite-protection.md](https://developer.shopware.com/docs/v6.6/guides/hosting/configurations/framework/samesite-protection.md)  
# SameSite protection

::: info
This feature has been introduced with Shopware version 6.4.3.1
:::

## Overview

The [SameSite configuration](https://symfony.com/doc/current/reference/configuration/framework.html#cookie-samesite) comes with the Symfony FrameworkBundle and supersedes the removed `sw_csrf` Twig function.
It is widely [available](https://caniuse.com/same-site-cookie-attribute) in modern browsers and is set to `lax` per default.

For more information, refer to [SameSite cookies site](https://web.dev/articles/samesite-cookies-explained?hl=en)

## Configuration

Changes to the `cookie_samesite` attribute can be applied to your `framework.yaml`. The `cookie_secure` ensures that cookies are sent via HTTP or HTTPS, depending on the request's origin.

```yaml

framework:
  session:
    cookie_secure: 'auto'
    cookie_samesite: lax
```

If you want to deactivate the SameSite protection despite security risks, change the value from `lax` to `null`. For detailed configuration options, check the official [Symfony Docs](https://symfony.com/doc/current/reference/configuration/framework.html#cookie-samesite).

---

---

## Logging
**Source:** [guides/hosting/configurations/observability/logging.md](https://developer.shopware.com/docs/v6.6/guides/hosting/configurations/observability/logging.md)  
# Logging

## Overview

Monolog is the logging library for PHP. It is used by Shopware to log errors and debug information. The log files are located in the `var/log` directory of your Shopware installation.

## Configuration

Configuration of Monolog is done in the `config/packages/prod/monolog.yaml` file. The following example shows the default configuration:

```yaml
monolog:
  handlers:
    main:
      type: fingers_crossed
      action_level: error
      handler: nested
      excluded_http_codes: [404, 405]
      buffer_size: 30 # How many messages should be saved? Prevent memory leaks
    business_event_handler_buffer:
      level: error
    nested:
      type: rotating_file
      path: "%kernel.logs_dir%/%kernel.environment%.log"
      level: error
    console:
      type: console
      process_psr_3_messages: false
      channels: ["!event", "!doctrine"]

```

## Log levels

Monolog supports the following log levels:

* `DEBUG`: Detailed debug information.
* `INFO`: Interesting events. Examples: User logs in, SQL logs.
* `NOTICE`: Normal but significant events.
* `WARNING`: Exceptional occurrences that are not errors. Examples: Use of deprecated APIs, poor use of an API, undesirable things that are not necessarily wrong.
* `ERROR`: Runtime errors that do not require immediate action but should typically be logged and monitored.
* `CRITICAL`: Critical conditions. Example: Application component unavailable, unexpected exception.
* `ALERT`: Action must be taken immediately. Example: Entire website down, database unavailable, etc. This should trigger the SMS alerts and wake you up.
* `EMERGENCY`: Emergency: system is unusable.

## Log sent e-mails and other flow events

To monitor all sent e-mails and other flow events set the `business_event_handler_buffer` to `info` level:

```yaml
monolog:
  handlers:
    business_event_handler_buffer:
      level: info
```

::: info
Be aware that this will cost you some performance.
:::

---

---

## OpenTelemetry
**Source:** [guides/hosting/configurations/observability/opentelemetry.md](https://developer.shopware.com/docs/v6.6/guides/hosting/configurations/observability/opentelemetry.md)  
# OpenTelemetry

OpenTelemetry is a standard to collect distributed traces, metrics and logs from the application. It is similar to tools like NewRelic, Datadog, Blackfire Monitoring and Tideways, but it is completely open source and vendor neutral. That means you can use OpenTelemetry to collect the data and push it to one of the vendors mentioned earlier, or you can use it to collect the data and push it to your own infrastructure with tools like Grafana Stack (Tempo, Loki, Prometheus, Grafana) or other tools.

## Requirements

To use OpenTelemetry with Shopware, you need to have the following requirements met:

* `ext-opentelemetry` [PHP extension](https://github.com/open-telemetry/opentelemetry-php-instrumentation)
* `ext-grpc` (optional, required when the transport method is gRPC)

## Installation

To install the OpenTelemetry Shopware extension, you need to run the following command:

```bash
composer require shopware/opentelemetry
```

This will install the OpenTelemetry Shopware bundle and create new configuration file `config/packages/prod/opentelemetry.yaml` with Symfony Flex plugin.

This configuration file enables the Shopware Profiler integration with OpenTelemetry in a production environment. Additionally, it specifies that the Monolog output will be directed to OpenTelemetry.

## Configuration

After the installation, you will need to set some environment variables to configure both, the OpenTelemetry and its exporter.

### Basic configuration

The following configuration enables the OpenTelemetry auto-instrumentation and sets the service name.

```text
OTEL_PHP_AUTOLOAD_ENABLED=true
OTEL_SERVICE_NAME=shopware
```

Refer to all possible [environment variables](https://opentelemetry.io/docs/instrumentation/php/sdk/#configuration) for better understanding.

### Exporter configuration

The OpenTelemetry extension needs to be configured to export the data to your collector. Here is an example configuration for the OpenTelemetry Collector using gRPC:

```text
OTEL_TRACES_EXPORTER=otlp
OTEL_LOGS_EXPORTER=otlp
OTEL_METRICS_EXPORTER=otlp
OTEL_EXPORTER_OTLP_PROTOCOL=grpc
OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317
```

If you use gRPC with OpenTelemetry Protocol (OTLP) , you will need to install `open-telemetry/transport-grpc open-telemetry/exporter-otlp` as composer packages.

Refer to this doc for more information about the [exporters](https://opentelemetry.io/docs/instrumentation/php/exporters/).

## Available instrumentation

The OpenTelemetry instrumentation collects following traces:

* Controller
* Symfony HTTP Client
* MySQL Queries

![Example Trace in Grafana](../../../../assets/otel-grafana-trace.png)

## Example Grafana Stack

You can find an example [Stack](https://github.com/shopwareLabs/opentelemetry/tree/main/docker) with:

* Grafana (Dashboard)
* Loki (Log storage)
* Prometheus (Metrics storage)
* Tempo (Trace storage)
* OpenTelemetry Collector (Collector for all data and batches it to the storage)

You will need to have the following environment variables in Shopware:

```text
OTEL_PHP_AUTOLOAD_ENABLED=true
OTEL_SERVICE_NAME=shopware
OTEL_TRACES_EXPORTER=otlp
OTEL_LOGS_EXPORTER=otlp
OTEL_METRICS_EXPORTER=otlp
OTEL_EXPORTER_OTLP_PROTOCOL=grpc
OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317
```

And following two composer packages installed: `open-telemetry/transport-grpc open-telemetry/exporter-otlp`.

The example Grafana is pre-configured to use the data sources, and it is enabled to go from logs to traces and from traces to the logs.

![Explore](../../../../assets/otel-grafana-explore.png)
![Trace](../../../../assets/otel-grafana-trace.png)

---

---

## Profiling
**Source:** [guides/hosting/configurations/observability/profiling.md](https://developer.shopware.com/docs/v6.6/guides/hosting/configurations/observability/profiling.md)  
# Profiling

Shopware provides a built-in profiler abstraction to measure the performance of code parts and publish this data to a profiler backend.

## Enabling the profiler backends

By default, only the Stopwatch profiler (Symfony Profiler Bar) is enabled. To enable the other profiler backends, you have to add the following configuration to your `config/packages/shopware.yaml` file:

```yaml
shopware:
    profiler:
        integrations:
            - Symfony
            # Requires the dd-trace PHP extension
            - Datadog
            # Requires the tideways PHP extension
            - Tideways
            # Requires the opentelemetry PHP extension
            - OpenTelemetry
```

::: info
The OpenTelemetry profiler is not installed by default. Checkout the [OpenTelemetry Integration](./opentelemetry.md) to learn how to install it.
:::

## Adding custom spans

To add custom spans to the profiler, you can use the `Shopware\Core\Profiling\Profiler::trace` method:

```php
use Shopware\Core\Profiling\Profiler;

$value = Profiler::trace('my-example-trace', function () {
    return $myFunction();
});
```

And then you can see the trace in the configured profiler backends.

## Adding a custom profiler backend

To add a custom profiler backend, you need to implement the `Shopware\Core\Profiling\Integration\ProfilerInterface` interface and register it as a service with the tag `shopware.profiler`.

The following example shows a custom profiler backend that logs the traces to the console:

```php

namespace App\Profiler;

use Shopware\Core\Profiling\Integration\ProfilerInterface;

class ConsoleProfiler implements ProfilerInterface
{
    public function start(string $title, string $category, array $tags): void
    {
        echo "Start $name\n";
    }

    public function stop(string $title): void
    {
        echo "Stop $name\n";
    }
}
```

```XML
<service id="App\Profiler">
    <tag name="shopware.profiler" integration="Console"/>
</service>
```

The attribute `integration` is used to identify the profiler backend in the configuration.

---

---

## Shopware configurations
**Source:** [guides/hosting/configurations/shopware.md](https://developer.shopware.com/docs/v6.6/guides/hosting/configurations/shopware.md)  
# Shopware configurations

## Overview

The following section guides you on the security, performance or structural configurations specific to Shopware 6.

---

---

## Environment Variables
**Source:** [guides/hosting/configurations/shopware/environment-variables.md](https://developer.shopware.com/docs/v6.6/guides/hosting/configurations/shopware/environment-variables.md)  
# Environment Variables

This page lists all environment variables that can be used to configure Shopware.

| Variable                               | Default Value             | Description                                                                                                          |
|----------------------------------------|---------------------------|----------------------------------------------------------------------------------------------------------------------|
| `APP_ENV`                              | `prod`                    | Environment                                                                                                          |
| `APP_SECRET`                           | (empty)                   | Can be generated with `openssl rand -hex 32`                                                                         |
| `APP_CACHE_DIR`                        | `{projectRoot}/var/cache` | Path to a directory to store caches (since 6.6.8.0)                                                                  |
| `APP_BUILD_DIR`                        | `{projectRoot}/var/cache` | Path to a temporary directory to create cache folder (since 6.6.8.0)                                                 |
| `APP_LOG_DIR`                          | `{projectRoot}/var/log`   | Path to a directory to store logs (since 6.6.8.0)                                                                    |
| `INSTANCE_ID`                          | (empty)                   | Unique Identifier for the Store: Can be generated with `openssl rand -hex 32`                                        |
| `JWT_PRIVATE_KEY`                      | (empty)                   | Can be generated with `shopware-cli project generate-jwt --env`                                                      |
| `JWT_PUBLIC_KEY`                       | (empty)                   | Can be generated with `shopware-cli project generate-jwt --env`                                                      |
| `LOCK_DSN`                             | `flock`                   | DSN for Symfony locking                                                                                              |
| `APP_URL`                              | (empty)                   | Where Shopware will be accessible                                                                                    |
| `BLUE_GREEN_DEPLOYMENT`                | `0`                       | This needs super privilege to create trigger                                                                         |
| `DATABASE_URL`                         | (empty)                   | MySQL credentials as DSN                                                                                             |
| `DATABASE_SSL_CA`                      | (empty)                   | Path to SSL CA file                                                                                                  |
| `DATABASE_SSL_CERT`                    | (empty)                   | Path to SSL Cert file                                                                                                |
| `DATABASE_SSL_KEY`                     | (empty)                   | Path to SSL Key file                                                                                                 |
| `DATABASE_SSL_DONT_VERIFY_SERVER_CERT` | (empty)                   | Disables verification of the server certificate (1 disables it)                                                      |
| `MAILER_DSN`                           | `null://localhost`        | Mailer DSN (Admin Configuration overwrites this)                                                                     |
| `ENABLE_SERVICES`                      | `auto`                    | Determines if services are enabled, auto detects that based on `APP_ENV`, other possible values are `true` & `false` |
| `OPENSEARCH_URL`                       | (empty)                   | Open Search Hosts                                                                                                    |
| `SHOPWARE_ES_ENABLED`                  | `0`                       | Open Search Support Enabled?                                                                                         |
| `SHOPWARE_ES_INDEXING_ENABLED`         | `0`                       | Open Search Indexing Enabled?                                                                                        |
| `SHOPWARE_ES_INDEX_PREFIX`             | (empty)                   | Open Search Index Prefix                                                                                             |
| `COMPOSER_HOME`                        | `/tmp/composer`           | Caching for the Plugin Manager                                                                                       |
| `SHOPWARE_HTTP_CACHE_ENABLED`          | `1`                       | Is HTTP Cache enabled?                                                                                               |
| `SHOPWARE_HTTP_DEFAULT_TTL`            | `7200`                    | Default TTL for HTTP Cache                                                                                           |
| `MESSENGER_TRANSPORT_DSN`              | (empty)                   | DSN for default async queue (example: `amqp://guest:guest@localhost:5672/%2f/default`)                               |
| `MESSENGER_TRANSPORT_LOW_PRIORITY_DSN` | (empty)                   | DSN for low priority queue (example: `amqp://guest:guest@localhost:5672/%2f/low_prio`)                               |
| `MESSENGER_TRANSPORT_FAILURE_DSN`      | (empty)                   | DSN for failed messages queue (example: `amqp://guest:guest@localhost:5672/%2f/failure`)                             |

---

---

## HTML Sanitizer
**Source:** [guides/hosting/configurations/shopware/html-sanitizer.md](https://developer.shopware.com/docs/v6.6/guides/hosting/configurations/shopware/html-sanitizer.md)  
# HTML Sanitizer

::: info
This feature has been introduced with Shopware version 6.5. This is exclusively intended for self-hosted shops. However, it's important to note that the implementation is currently not available for cloud stores.
:::

## Overview

HTML sanitizer improves security, reliability and usability of the text editor by removing potentially unsafe or malicious HTML code. It also sanitizes styles and attributes for consistent and correct code rendering regardless of platform and browser. For example, if the `<img>` tag is added, it is automatically removed by the editor after a few seconds and an additional notice appears that some of your inputs have been sanitized.

## Configuration

Through a workaround or an adjustment of the `z-shopware.yaml` file, it is possible to add the `<img>` tag to the allowed code.

The `z-shopware.yaml` is located below `config/packages/` on the server where Shopware is installed. By default, this file does not exist. A simple copy of the `shopware.yaml` in the same directory solves this obstacle.

In the copied `shopware.yaml` file (z-shopware.yaml), you should include an additional key called `html_sanitizer:` inside the `shopware:` section. This key will contain all the other values and wildcards required for whitelisting.

In this example, the `<img>` tag, as well as the CSS attributes `src`, `alt` and `style` are added to the whitelist:

```yaml
shopware:
  html_sanitizer:
    sets:
      -   name: basic
          tags: [ "img" ]
          attributes: [ "src", "alt", "style" ]
          options:
            - key: HTML.Trusted
              value: true
            - key: CSS.Trusted
              value: true

```

If you want to deactivate the sanitizer despite security risks, you can also do this in the `z-shopware.yaml` using the following code:

```yaml
shopware:
  html_sanitizer:
    enabled: false

```

::: warning
Disabling the HTML sanitizer will allow potentially unsafe or malicious HTML code to be inserted.
:::

---

---

## Staging
**Source:** [guides/hosting/configurations/shopware/staging.md](https://developer.shopware.com/docs/v6.6/guides/hosting/configurations/shopware/staging.md)  
# Staging

Since Shopware 6.6.1.0, Shopware has an integrated staging mode. This mode prepares the shop to be used in a staging environment. This means the shop is prepared to be used in a test environment, where changes can be made without affecting the live shop.

## The workflow

The staging mode is designed to modify data only inside the Shopware instance. This means the staging mode does not duplicate the current installation, copy the database, or copy the files. It only changes the data inside the Shopware instance.

So, the real-world use case would be something like this:

### Creating the second Shopware instance

The recommended way to create a second Shopware instance would be to deploy from your Git repository to the new environment. This way, you ensure the codebase is equal to the live environment.

An alternative way would be to copy the files from the live environment to the staging environment.

### Copying the database

::: info
Ensure that the `mysqldump` and `mysql` binary are from the same major version and vendor. If you use `mysqldump` from MariaDB, you should also use `mysql` from MariaDB. The same applies to MySQL.
:::

To have the staging environment similar to the live environment, it's recommended that the database be duplicated. You can use the `mysqldump` command to export the database and import it into the staging environment.

::: info
`shopware-cli` is a separate Go command line application that contains a lot of useful commands for Shopware. [Checkout the docs](../../../../products/cli/installation) to learn how to install it.
:::

We recommend using `shopware-cli project dump` to create a dump of the database and import it with the regular mysql command. Shopware cli also has a flag to anonymize the data, so you can be sure that no personal data is in the staging environment.

```bash
# creating a regular dump, the clean parameter will not dump the data of cart table
shopware-cli project dump --clean --host localhost --username db_user --password db_pass --output shop.sql shopware

# create a dump with anonymize data
shopware-cli project dump --clean --anonymize --host localhost --username db_user --password db_pass --output shop.sql shopware
```

You can configure the dump command with a `.shopware-project.yml`. This file allows you to specify tables that should be skipped, define additional fields for anonymization, and more. Check out the [CLI](../../../../products/cli/project-commands/mysql-dump) for more information.

### Configuration

::: info
It is not recommended to share resources like MySQL, Redis, ElasticSearch/OpenSearch between the live and staging environments. This could lead to data corruption when the configuration is not done correctly. Also, the performance of the live environment could be affected by the staging environment.
:::

After importing the database, you should modify the `.env` to use the staging database. If you use ElasticSearch/OpenSearch, you should set a `SHOPWARE_ES_INDEX_PREFIX` to avoid conflicts with the live environment.

### Activate the staging mode

After the database is imported and the configuration is done, you can activate the staging mode. This can be done using:

```bash
./bin/console system:setup:staging
```

This command will modify the database to be used in a staging environment. You can pass `--no-interaction` to the command to avoid the interactive questions.

### Protecting the staging environment

The staging environment should be protected from unauthorized access. It is advisable to employ protective measures like password protection, IP restriction, or OAuth authentication.

The simplest way to protect the staging environment is utilizing `.htaccess` for  Apache or `auth_basic` for Nginx. You can also use a firewall to restrict access to the staging environment based on IP addresses.

Example configuration for Apache:

```apache
# <project-root>/public/.htaccess
SetEnvIf Request_URI /api noauth=1
<RequireAny>
Require env noauth
Require env REDIRECT_noauth
Require valid-user
</RequireAny>
```

An alternative way could be to use an Application Proxy before the staging environment like:

* [Cloudflare Access](https://www.cloudflare.com/teams/access/)
* [Azure Application Gateway](https://azure.microsoft.com/en-us/services/application-gateway/)
* [Generic oauth2 proxy](https://oauth2-proxy.github.io/oauth2-proxy/)

## Staging mode

The staging mode is designed to be used in a test environment. This means the shop is prepared to be used in a test environment, where changes can be made without affecting the live shop.

### What staging mode does?

* Deletes all apps that have an active connection to an external service and the integrations in Shopware.
* Resets the instance ID used for registration of apps.
* It turns off the sending of emails.
* Rewrites the URLs to the staging domain (if configured).
* Checks that the ElasticSearch/OpenSearch indices do not exist yet.
* Shows a banner in the administration and storefront to indicate that the shop is in staging mode.

### What staging mode does not?

* Doesn't duplicate the current installation.
* Doesn't copy database or files.
* Doesn't modify the live environment.

### Configuration

The staging mode is fully configurable with `config/packages/staging.yaml`. You can configure the following options:

```yaml
# <shopware-root>/config/packages/staging.yaml
shopware:
    staging:
        mailing:
            # Disables the sending of mails (default: true)
            disable_delivery: true
        storefront:
            # Shows a banner in the storefront when staging mode is active (default: true)
            show_banner: true
        administration:
            # Shows a banner in the administration when staging mode is active (default: true)
            show_banner: true
        sales_channel:
            domain_rewrite:
                # See below for more information
        elasticsearch:
            # Checks that no indices are existing yet (default: true)
            check_for_existence: true
```

One of the most important options is the `domain_rewrite`. This option allows you to rewrite the URLs to the staging domain. This allows multiple ways to rewrite the URLs:

* Using direct match (`equal`)

```yaml
# <shopware-root>/config/packages/staging.yaml
shopware:
    staging:
        sales_channel:
            domain_rewrite:
                - type: equal
                  match: https://my-live-store.com
                  replace: https://my-staging-store.com
                - # ... second rule
```

This compares the Sales Channel URLs. When it's equal to `https://my-live-store.com`, it will be replaced with `https://my-staging-store.com`.

* Replace using prefix (`prefix`)

```yaml
# <shopware-root>/config/packages/staging.yaml
shopware:
    staging:
        sales_channel:
            domain_rewrite:
                - type: prefix
                  match: https://my-live-store.com
                  replace: https://my-staging-store.com
                - # ... second rule
```

The difference here to the `equal` type is that it will only replace the URL when it starts with `https://my-live-store.com`, so all paths to that beginning will be replaced. For example, `https://my-live-store.com/en` will be replaced with `https://my-staging-store.com/en`

* Replace using regex (`regex`)

```yaml
# <shopware-root>/config/packages/staging.yaml
shopware:
    staging:
        sales_channel:
            domain_rewrite:
                - type: regex
                  match: '/https?:\/\/(\w+)\.(\w+)$/m'
                  replace: 'http://$1-$2.local'
                - # ... second rule
```

This will use the regex to replace the URL. The match and replace are regular expressions. In this example, `https://my-live-store.com` will be replaced with `http://my-live-store.local`.

### Usage of apps

The staging command will delete all apps that have an active connection to an external service. This will be done to avoid data corruption or leaks in the live environment, as the staging environment is a copy of the live environment, so they keep a connection. After executing the command, you can install the app again, creating a new instance ID, so the app will think it's an entirely different shop. In this way, the app installation is completely isolated from the live environment.

## Integration into plugins

The `system:setup:staging` is dispatching an Event which all plugins can subscribe to `Shopware\Core\Maintenance\Staging\Event\SetupStagingEvent` and modify the database for them to be in staging mode.

Example of a subscriber for a payment provider to turn on the test mode:

```php
<?php

namespace Swag\PaymentProvider\Subscriber;

use Shopware\Core\Maintenance\Staging\Event\SetupStagingEvent;

class StagingSubscriber implements EventSubscriberInterface
{
    public static function getSubscribedEvents(): array
    {
        return [
            SetupStagingEvent::class => 'onSetupStaging'
        ];
    }

    public function onSetupStaging(SetupStagingEvent $event): void
    {
        // modify the database to turn on the test mode
    }
}
```

---

---

## Static System Configuration
**Source:** [guides/hosting/configurations/shopware/static-system-config.md](https://developer.shopware.com/docs/v6.6/guides/hosting/configurations/shopware/static-system-config.md)  
# Static System Configuration

::: note
This feature is available since Shopware 6.6.4.0
:::

The static system configuration is a feature that allows you to configure system configurations inside the `config/packages` directory and **overwrite** the configuration set in the database. This is useful for setting up configurations that should not be changed by the user, or properly configuring the system for different environments without the need to change the database.

## How it works

The statically set configuration is an overlay of the database loaded configuration. This means that the configuration in the database is loaded first, and then the configuration set in the `config/packages` directory is loaded. If a configuration key is set in both places, the value from the `config/packages` directory will be used. Additionally, when the configuration is overwritten, the user is not able to change the configuration in the administration anymore.

## Why to use?

* When the configuration should be fixed and should not be changed by the user
* When you want to have the configuration versioned in the repository
* When you want to have different configurations for different environments (e.g., development, staging, production)

## Usage

To use this feature, you will need to create a new file at `config/packages/<name>.yaml`

The file should contain the configuration in the following format:

```yaml
shopware:
  system_config:
    default:
      core.listing.allowBuyInListing: true
    # Disable it for the specific sales channel
    0188da12724970b9b4a708298259b171:
      core.listing.allowBuyInListing: false
```

In this example, the `core.listing.allowBuyInListing` configuration is set to `true` by default. However, for the sales channel with the ID `0188da12724970b9b4a708298259b171`, the configuration is set to `false`.

You can also use regular Symfony Configuration processors like the usage of environment variables:

```yaml
shopware:
  system_config:
    default:
      core.listing.allowBuyInListing: '%env(bool:ALLOW_BUY_IN_LISTING)%'
```

and then set the environment variable in your `.env` file:

```dotenv
# .env.local
ALLOW_BUY_IN_LISTING=true
```

---

---

## Stock Configuration
**Source:** [guides/hosting/configurations/shopware/stock.md](https://developer.shopware.com/docs/v6.6/guides/hosting/configurations/shopware/stock.md)  
# Stock Configuration

When running Shopware 6 there are various configuration options you can use to customize your installation. These configurations reside in the general [bundle configuration](../../../../guides/hosting/configurations/).

Some features of Shopware are only activated when the corresponding feature flag is enabled. Feature flags can be enabled in your project's `.env` file:

```sh
// <project root>/.env
STOCK_HANDLING=1

```

## Enable stock management system

As of Shopware 6.5.5, the stock management system has been rewritten. The `product.stock` field is now the primary source for real-time product stock values.

The new system is not enabled by default. To enable it, set the `STOCK_HANDLING` feature flag to `1`.

```sh
// <project root>/.env
STOCK_HANDLING=1

```

In the next major version of Shopware, the new stock management system will become the default.

## Disable stock management system

Please note this only applies if you have the `STOCK_HANDLING` feature flag enabled.

You can completely disable Shopware's default stock management system. When disabled, none of the event subscribers for order transitions will be executed. In practice, this means that none of the subscribers in `Shopware\Core\Content\Product\Stock\OrderStockSubscriber` will be executed.

To disable, set `shopware.stock.enable_stock_management` to `false`:

```yaml
# <project root>/config/packages/shopware.yaml
shopware:
  stock:
    enable_stock_management: false

```

For more detailed implementation refer to [Stock](../../../../guides/plugins/plugins/content/stock/) guide section.

---

---

## Infrastructure
**Source:** [guides/hosting/infrastructure.md](https://developer.shopware.com/docs/v6.6/guides/hosting/infrastructure.md)  
# Infrastructure

The Hosting infrastructure for Shopware includes Elasticsearch for advanced search, a database cluster for data storage, a filesystem for media files, a message queue for asynchronous communication, a rate limiter for request management, and a reverse HTTPS proxy for secure communication.

More detailed information is described in the following sections.

---

---

## Database Cluster
**Source:** [guides/hosting/infrastructure/database-cluster.md](https://developer.shopware.com/docs/v6.6/guides/hosting/infrastructure/database-cluster.md)  
# Database Cluster

::: info
This functionality is available starting with Shopware 6.4.12.0.
:::

To scale Shopware even further, we recommend using a database cluster. A database cluster consists of multiple read-only servers managed by a single primary instance.

Shopware already splits read and write SQL queries by default. When a write  [`INSERT`/`UPDATE`/`DELETE`/...](https://github.com/shopware/shopware/blob/v6.4.11.1/src/Core/Profiling/Doctrine/DebugStack.php#L48) query is executed, the query is delegated to the primary server, and the current connection uses only the primary node for subsequent calls. This is ensured by the `executeStatement` method in the [DebugStack decoration](https://github.com/shopware/shopware/blob/v6.4.11.1/src/Core/Profiling/Doctrine/DebugStack.php#L48).
That way, Shopware can ensure read-write consistency for records within the same request. However, it doesn't take into account that read-only child nodes might not be in sync with the primary node. This is left to the database replication process.

## Preparing Shopware

We suggest following the steps below to make the splitting the most effective.

### Using the optimal MySQL configuration

By default, Shopware does not set specific MySQL configurations that make sure the database is optimized for Shopware usage.
These variables are set in cluster mode only on the read-only server. To make sure that Shopware works flawlessly, these configurations must be configured directly on the MySQL server so these variables are set on any server.

The following options should be set:

* Make sure that `group_concat_max_len` is by default higher or equal to `320000`
* Make sure that `sql_mode` doesn't contain `ONLY_FULL_GROUP_BY`

After this change, you can set also `SQL_SET_DEFAULT_SESSION_VARIABLES=0` in the `.env` file so Shopware does not check for those variables at runtime.

### Cart in Redis

As we learned in the beginning, Shopware queries a read-only MySQL server until the first write attempt. To maximize this behavior, it is highly recommended to outsource as many write operations as possible from the database. One of the easiest solutions is to use the Redis as storage for store carts.
To use Redis, add the following snippet to `config/packages/cart.yml`

```yaml
shopware:
    cart:
        redis_url: 'redis://localhost:6379/0?persistent=1'
```

It is recommended to use a persistent Redis connection to avoid connection issues in high-load scenarios. There is also a `cart:migrate` command to migrate the existing carts between MySQL and Redis, so the migration does not influence end-user experience.

For a detailed explanation refer to the cart storage docs:


## Configure the database cluster

To use the MySQL cluster, you have to configure the following in the `.env` file:

* `DATABASE_URL` is the connection string for the MySQL primary.
* `DATABASE_REPLICA_x_URL` (e.g `DATABASE_REPLICA_0_URL`, `DATABASE_REPLICA_1_URL`) - is the connection string for the MySQL read-only server.

---

---

## Elasticsearch
**Source:** [guides/hosting/infrastructure/elasticsearch.md](https://developer.shopware.com/docs/v6.6/guides/hosting/infrastructure/elasticsearch.md)  
# Elasticsearch

Elasticsearch is a robust search engine that can be integrated into Shopware to provide advanced search capabilities. It also supports AND/OR operations.

The following sections will help you to set up, configure, debug, resolve indexing issues, and optimize performance. By following these steps, you can leverage Elasticsearch to enhance search functionality in your Shopware store.

---

---

## Debugging Elasticsearch
**Source:** [guides/hosting/infrastructure/elasticsearch/elasticsearch-debugging.md](https://developer.shopware.com/docs/v6.6/guides/hosting/infrastructure/elasticsearch/elasticsearch-debugging.md)  
# Debugging Elasticsearch

## Overview

This article shows you how to debug the status and indexing process of your Elasticsearch environment. Ensure that the [Debug-Mode](./elasticsearch-debugging) is activated in your *.env* file.

## Shopware 6 CLI commands

### Cache clear

`cache:clear` clears the cache

```bash
bin/console cache:clear
```

**> Output:**

```bash
// Clearing the cache for the dev environment with debug
// true
[OK] Cache for the "dev" environment (debug=true) was successfully cleared.
```

### ES index

`es:index` creates only the index for ES

```bash
bin/console es:index // Creates only the index for ES
```

**> No Output**

### ES create alias

`es:create:alias`  will create an alias linking to the index after `es:index` is done. Normally this is done automatically. In the older version, this has to be done.

```bash
bin/console es:create:alias 
```

**> No Output**

### DAL refresh index

`dal:refresh:index --use-queue` creates a complete reindex from the Shopware DAL (ES/SEO/Media/Sitemap...) **ALWAYS** "`--use-queue`" since big request can outperform the server!

```bash
bin/console dal:refresh:index --use-queue
```

**> Output:**

```bash
[landing_page.indexer]
1/1 [============================] 100% < 1 sec/< 1 sec 38.5 MiB

[product.indexer]
22/22 [============================] 100% < 1 sec/< 1 sec 40.5 MiB

[customer.indexer]
2/2 [============================] 100% < 1 sec/< 1 sec 40.5 MiB

[sales_channel.indexer]
2/2 [============================] 100% < 1 sec/< 1 sec 40.5 MiB

[category.indexer]
9/9 [============================] 100% < 1 sec/< 1 sec 40.5 MiB

[...]
```

### Messenger consume

`messenger:consume -vv` starts a message consumer working on all tasks. This could be started *X* times. When using more than 3 message consumers, you will need something like RabbitMq to handle the data.

```bash
bin/console messenger:consume -vv
```

**> Output:**

```bash
[OK] Consuming messages from transports "default".

// The worker will automatically exit once it has received a stop signal via the messenger:stop-workers command.

// Quit the worker with CONTROL-C.

09:47:28 INFO      [messenger] Received message Shopware\Elasticsearch\Framework\Indexing\ElasticsearchIndexingMessage ["message" => Shopware\Elasticsearch\Framework\Indexing\ElasticsearchIndexingMessage^ { …},"class" => "Shopware\Elasticsearch\Framework\Indexing\ElasticsearchIndexingMessage"]

[...]
```

### Index cleanup

`es:index:cleanup` to remove unused indices, because each indexing will generate a new Elasticsearch index.

```bash
bin/console es:index:cleanup
```

## Helpful Elasticsearch REST APIs

```bash
curl -XGET 'http://elasticsearch:9200/?pretty'
```

**> Output:**

```bash
{
  "name" : "TZzynG6",
  "cluster_name" : "docker-cluster",
  "cluster_uuid" : "tHklOFWPSwm-j8Yn-8PRoQ",
  "version" : {
    "number" : "6.8.1",
    "build_flavor" : "default",
    "build_type" : "docker",
    "build_hash" : "1fad4e1",
    "build_date" : "2019-06-18T13:16:52.517138Z",
    "build_snapshot" : false,
    "lucene_version" : "7.7.0",
    "minimum_wire_compatibility_version" : "5.6.0",
    "minimum_index_compatibility_version" : "5.0.0"
  },
  "tagline" : "You Know, for Search"
}
```

### API for cluster health

Returns the health status of a cluster:

```bash
curl -XGET 'http://elasticsearch:9200/_cluster/health?pretty'
```

**> Output:**

```bash
{
  "cluster_name" : "docker-cluster",
  "status" : "yellow",
  "timed_out" : false,
  "number_of_nodes" : 1,
  "number_of_data_nodes" : 1,
  "active_primary_shards" : 1210,
  "active_shards" : 1210,
  "relocating_shards" : 0,
  "initializing_shards" : 0,
  "unassigned_shards" : 1210,
  "delayed_unassigned_shards" : 0,
  "number_of_pending_tasks" : 0,
  "number_of_in_flight_fetch" : 0,
  "task_max_waiting_in_queue_millis" : 0,
  "active_shards_percent_as_number" : 50.0
}
```

### API for cat indices

Returns high-level information about indices in a cluster, including backing indices for data streams:

```bash
curl -XGET 'http://elasticsearch:9200/_cat/indices/?pretty'
```

**> Output:**

```bash
yellow open sw1_manufacturer_20210906113224 AYKMT4NJS7eZgU29ww7z6Q 5 1  3 0  33.2kb  33.2kb
yellow open sw1_emotion_20210903165112      he19OP_UR3mMIAKI7ry2mg 5 1  1 0  11.6kb  11.6kb
yellow open sw1_emotion_20210903171353      jBzApKujRPu73CkKA79F7w 5 1  1 0  11.6kb  11.6kb
yellow open sw1_synonym_20210903175037      EexqHsXyTK202XsalUednQ 5 1  1 0     6kb     6kb
yellow open sw1_synonym_20210903170128      NRjlZZ3AQ0Wat1ILB_9L8Q 5 1  0 0   1.2kb   1.2kb

[...]
```

### API to delete the index

With `_all` it will delete all indices.

```bash
curl -X DELETE 'elasticsearch:9200/_all'
```

**> Output:**

```bash
{"acknowledged":true}
```

## Show the indexing status in the database

Returns the status of your indexing:

```sql
select * from message_queue_stats mqs ; 
select count(*) from enqueue e ; 
select count(*) from dead_message dm ; 
```

The number of entries in the enqueue should match the sum of the size values in the `message_queue_stats`. As long as there are entries in your `enqueue`, the indexing is in process and your message consumer has to work those messages.

## Reset the indexing in the database

Sometimes you want to reset the indexing in your database because your indexing is stuck or you run into an error.
If the database queue is used, third-party services will differ. You can do so with the following queries.

```sql
truncate enqueue ; 
truncate dead_message ;
truncate message_queue_stats ;
update scheduled_task set status = 'scheduled' where status = 'queued';
```

## Completely reset your Elasticsearch and reindex

This is mainly for debugging purposes and is only meant for testing and staging environments.
First, execute the database reset (only working for the database queue):

```sql
truncate enqueue ; 
truncate dead_message ;
truncate message_queue_stats ;
update scheduled_task set status = 'scheduled' where status = 'queued';
```

Now delete the old Elasticsearch index, clear your cache, reindex and ensure that the indexing process is finished:

```bash
curl -X DELETE 'elasticsearch:9200/_all'
bin/console cache:clear
bin/console es:index
bin/console messenger:consume -vv
```

After the last message has been processed, your index should be found in your Storefront else execute:

```bash
bin/console es:create:alias
```

## Logfiles and tipps

You can usually find the Elasticsearch logfiles at [`/var/log/elasticsearch`](https://www.elastic.co/guide/en/elasticsearch/reference/master/settings.html#_config_file_format) to check for any issues when indexing.
Also, tools like [Kibana](https://www.elastic.co/kibana) or [Cerebro](https://wissen.profihost.com/wissen/artikel/cerebro/) can help you better understand what is happening in your Elasticsearch.

---

---

## Set up Elasticsearch
**Source:** [guides/hosting/infrastructure/elasticsearch/elasticsearch-setup.md](https://developer.shopware.com/docs/v6.6/guides/hosting/infrastructure/elasticsearch/elasticsearch-setup.md)  
*(Body truncated in this bundle; follow the link for the rest.)*

# Set up Elasticsearch

## Overview

As soon as several thousand data sets are used in a project, it makes sense to deal with Elasticsearch. The Elasticsearch integration for Shopware is in the [shopware/elasticsearch](https://github.com/shopware/elasticsearch) bundle. If this is not available in your project, you can simply add it via `composer require shopware/elasticsearch`. In this documentation, we will provide you with a short overview of the functionalities of Elasticsearch on your server and the configuration, activation, and indexing process in Shopware for live and test environments.

::: info
Currently, the implementation for Elasticsearch/Opensearch works in the same way.
:::

## Requirements

* Opensearch >= 2.0 or Elasticsearch >= 7.8
* [Running message queue workers in background](../message-queue)

## Server basics

Elasticsearch installation and configuration greatly depend on your operating system and hosting provider. You will find extensive documentation online regarding the installation and configuration of Elasticsearch on most common Linux distributions. Some hosting providers might also provide specific documentation regarding this subject. Installation on Mac OS or Windows is also possible but not officially supported.

The current Shopware 6 integration is designed to work with the out-of-the-box configuration of Elasticsearch. This does not mean, of course, that these are the best settings for a production environment. Although they will affect performance and security, the settings you choose to use on your Elasticsearch setup will be mostly transparent to your Shopware installation. The best setting constellation for your shop will greatly depend on your server setup, the number, and structure of products, and replication requirements, to name a few. In this document, we can't give you specific examples for your setup, but provide you with hints and basics you might need to choose your perfect setup. More detailed information can be found on the official [Elasticsearch](https://www.elastic.co/guide/index.html)  documentation page.

### Elasticsearch server setup

Elasticsearch is meant to be used as a cluster setup so it can scale properly and provide you with reliability.
In this cluster, you can choose how many nodes you want to use and which different type each node in the cluster shall have.
A one node cluster is only meant for development or test environments because it can't scale at all and does not give you any more reliability.
Reliability is given when you have at least 3 nodes because of the process of election of the master node. This is further explained in more detail in the [Master Node](#master-node) section.
From our experience, the best way is to have a cluster with 5 nodes. You can have the 3 needed master-eligible nodes and 2 nodes which are data nodes and do not proceed in the election process.
Which cluster is really needed in your setup and fits your needs best is up to you.

Most configurations of the Elasticsearch cluster can be done in the elasticsearch.yml file you find in the [config folder](https://www.elastic.co/guide/en/elasticsearch/reference/master/settings.html#config-files-location).
This file configures, for example, the name of your cluster (`cluster.name`), the name of your node (`node.name`), nodes that know each other (`discovery.seed_hosts`), the type of the node (`node.master`, `node.data`, `node.ingest`), the host (`network.host`) and the port (`network.host`).
Sometimes it makes sense to configure your [JVM](https://www.elastic.co/guide/en/elasticsearch/reference/master/advanced-configuration.html#set-jvm-options) as well. You should only make changes here if you know exactly what you do. Most hosting partners will provide you with a fitting setup that will not require many changes here.
The data files of the index will be found in the data directory later on. Another important folder is the logs folder. If not configured differently, you will find the different logfiles for your cluster here in case you ever need to check an error or slowlog.

### Nodes

Every instance of Elasticsearch starts a node. A collection of connected nodes are called a cluster. All nodes can handle HTTP and transport traffic.
Depending on your setup, the needed performance, and reliability, you might want to have dedicated nodes of the following types in your cluster.

#### Master nodes

Master nodes are in charge of the cluster-wide settings and changes like CRUD operations of indices, including mappings and settings of those, adding nodes, removing nodes and allocating the [shards](#shards) to the nodes.
A productive cluster of Elasticsearch should always contain 3 nodes that are all master-eligible nodes set by the `node.master` property in the elasticsearch.yml file. The master node is chosen by an election process of which only the master-eligible nodes are part. In an election process, you have to mind a quorum of master-eligible nodes, so you get a specific result of the election, so you should have N/2+1 master-eligible nodes. 3 is the minimum number for this because then the currently elected master node fails, you can still have a correct election process for a new master. The setting "cluster.initial\_master\_nodes: \["masternode1","masternode2","masternode3"]" should be provided on each of those master-eligible nodes on start.

#### Ingest nodes

Ingest nodes provide the ability to pre-process a document before it gets indexed.
The ingest node intercepts bulk and index requests applies transformations and then passes the documents back to the index or bulk APIs.
All nodes are Ingest nodes by default which can be changed by the `node.ingest` property in the elasticsearch.yml file.

#### Data nodes

Data nodes have two main features. They hold the [shards](#shards) that contain the documents/elements you have indexed and execute data related operations like CRUD, search and aggregations.
By default, all nodes are Data nodes, which can be changed using the `node.data` property in the elasticsearch.yml file.
Data nodes are very resource intensive, so you definitely want to monitor the resources and add more data nodes if they are overloaded.

### Shards

A shard is a worker unit that holds the data of the index and can be assigned to a node. There are two types of shards:

* **Primary**: A primary shard contains the original data.
* **Replica**: A replica is a copy of a primary shard.

The number of replica shards is up to you and the reliability you need in your cluster. The more replica shards you have, the more nodes can fail before the data in the shard becomes unavailable.
But reliability is not the only usage of a replica shard. Queries like search can be performed on a primary or replica. So if you have replicas of your shards you can better scale your data and cluster resources.
A replica is only created when there are enough nodes because a replica can never be created in the same node as its primary or another replica of its primary.
The master node determines where the shard is distributed.
Normally a shard in Elasticsearch can hold at least tens of gigabytes, so you might want to keep this in mind when setting your number of shards and replicas.

## Prepare Shopware for Elasticsearch

### Variables in your *.env*

| Variable | Possible values | Description |
| ---------|-----------------|-------------|
| `APP_ENV`| `prod` / `dev` | This variable is important if you want to activate the debug mode and see possible errors of Elasticsearch. You have to set the variable to dev for debug mode and prod if you want to use Elasticsearch in a productive system.|
| `OPENSEARCH_URL`| `localhost:9200` | A comma separated list of Elasticsearch hosts. You can find the possible formats [here](https://www.elastic.co/guide/en/elasticsearch/client/php-api/current/host-config.html#inline-host-config)|
| `SHOPWARE_ES_INDEXING_ENABLED`| `0` / `1` |  This variable activates the indexing to Elasticsearch|
| `SHOPWARE_ES_ENABLED`| `0` / `1` | This variable activates the usage of Elasticsearch for your shop|
| `SHOPWARE_ES_INDEX_PREFIX`| `sw_myshop` | This variable defines the prefix for the Elasticsearch indices|
| `SHOPWARE_ES_THROW_EXCEPTION`| `0` / `1` | This variable activates the debug mode for Elasticsearch. Without this variable as = 0 you will get a fallback to mysql without any error message if Elasticsearch is not working|

### Example file for productive environments

```bash
APP_ENV=prod
APP_SECRET=1
INSTANCE_ID=1
DATABASE_URL=mysql://mysqluser:mysqlpassword@localhost:3306/shopwaredatabasename
APP_URL=http://localhost
MAILER_URL=smtp://localhost:1025
COMPOSER_HOME=/var/www/html/var/cache/composer

OPENSEARCH_URL="elasticsearchhostname:9200"
SHOPWARE_ES_ENABLED="1"
SHOPWARE_ES_INDEXING_ENABLED="1"
SHOPWARE_ES_INDEX_PREFIX="sw"
SHOPWARE_ES_THROW_EXCEPTION=1
```

### Example file for debug configuration

```bash
APP_ENV=dev
APP_SECRET=1
INSTANCE_ID=1
DATABASE_URL=mysql://mysqluser:mysqlpassword@localhost:3306/shopwaredatabasename
APP_URL=http://localhost
MAILER_URL=smtp://localhost:1025
COMPOSER_HOME=/var/www/html/var/cache/composer

OPENSEARCH_URL="elasticsearchhostname:9200"
SHOPWARE_ES_ENABLED="1"
SHOPWARE_ES_INDEXING_ENABLED="1"
SHOPWARE_ES_INDEX_PREFIX="sw"
SHOPWARE_ES_THROW_EXCEPTION=1
```

### Example for changing index configuration

Shopware will use by default 3 shards and 3 replicas for the created index. This configuration can be overwritten with a new config file in `config/packages/elasticsearch.yml`

::: info
This configuration is available since Shopware version 6.4.12.0
:::

```yaml
elasticsearch:
  index_settings:
    number_of_shards: 1
    number_of_replicas: 0
```

## Indexing

Before indexing, you might want to clear your cache with `bin/console cache:clear` so the changes from your *.env* can be processed.

### Basic Elasticsearch indexing

Normally, you can index by executing the command `bin/console es:index`.

### Indexing the whole shop

Sometimes you want to reindex your whole shop, including Elasticsearch, SEO-URLs, product index, and more.
For a reindex of the whole shop, you can use the command `bin/console dal:refresh:index --use-queue`. Use the `--use-queue` option because you will have too many products to index without the [message queue](/docs/guides/hosting/infrastructure/message-queue) involved.

### Alias creation

Some systems require you to manually execute `bin/console es:create:alias` after the indexing is processed completely.
Try that command if your index was created fully without errors and you still don't see products in your Storefront.

### What happens when indexing

When you are indexing, the data is written in bulks to the message queue and the respective table enqueue.
If a messenger process is active, the entries of that table are processed one by one.
In case a message runs into an error, it is written into the `dead_messages` table and will be processed again after a specific time frame.

You can start multiple messenger consumer processes by using the command `bin/console messenger:consume` and also add output to the processed messages by adding the parameter `bin/console messenger:consume -vv`.
In a production environment, you want to deactivate the admin messenger which is started automatically when opening a session in your Administration view by following this [documentation](/docs/guides/plugins/plugins/framework/message-queue/add-message-handler#the-admin-worker).

Our experience has shown that up to 3 worker processes are normal and useful for a production environment.
If you want more than that, a tool like [RabbitMq](/docs/guides/hosting/infrastructure/message-queue#transport-rabbitmq-example) to handle the queue is needed so your database will not become a bottleneck.

## Configuration

Keep in mind that the search configuration of Shopware has no effect when using Elasticsearch.
To configure which fields and elements are searchable when using Elasti

… **Truncated.** Full document: https://developer.shopware.com/docs/v6.6/guides/hosting/infrastructure/elasticsearch/elasticsearch-setup.md


---

## Filesystem
**Source:** [guides/hosting/infrastructure/filesystem.md](https://developer.shopware.com/docs/v6.6/guides/hosting/infrastructure/filesystem.md)  
# Filesystem

## Overview

Shopware 6 stores and processes a wide variety of files. This goes from product images or videos to generated documents such as invoices or delivery notes. This data should be stored securely, and backups should be generated regularly. Therefore, it is advisable to set up storage service, which scales with the size of the data, performs backups, and ensures data redundancy. In addition, for cluster setups with multiple setups, it is **necessary** to share the files via external storage so that each app server can access the corresponding data.

## Flysystem overview

Shopware 6 can be used with several cloud storage providers. It uses [Flysystem](https://flysystem.thephpleague.com/docs/) to provide a common interface between different providers as well as the local file system. This enables your shops to read and write files through a common interface.

The file system can be divided into multiple adapters. Each adapter can handle one or more of the following directories: media, sitemaps, and more. Of course, you can also use the same configuration for:

* private files: invoices, delivery notes, plugin files, etc.
* public files: product pictures, media files, plugin files in general
* theme files
* sitemap files
* bundle assets files

## Configuration

The configuration for file storage of Shopware 6 resides in the general bundle configuration:

```text
<project root>
└── config
   └── packages
      └── shopware.yml
```

To set up a non-default filesystem for your shop, you need to add the `filesystem:` map to the `shopware.yml`. Under this key, you can separately define your storage for the public, private, theme, sitemap, and asset (bundle assets).

::: info
You can also change the URL of the file systems. This is useful if you want to use a different domain for your files. For example, you can use a CDN for your public files.
:::

```yaml
shopware:
  filesystem:
    public:
      url: "{url-to-your-public-files}"
      # The Adapter Configuration
    private:
      visibility: "private"
      # The Adapter Configuration
    theme:
      url: "{url-to-your-theme-files}"
      # The Adapter Configuration
    asset:
      url: "{url-to-your-asset-files}"
      # The Adapter Configuration
    sitemap:
      url: "{url-to-your-sitemap-files}"
      # The Adapter Configuration

```

### Fallback adapter configuration

By default, the configuration for the theme, asset and sitemap filesystem will use the configuration from the `public` filesystem if they are not specifically configured.
This means when you want to change the configuration used for the public filesystem, but the others should use the old configuration you have to set them explicitly.

E.g. before you had the following configuration:

```yaml
shopware:
  filesystem:
    public:
      type: "local"
      url: "https://your.domain/public"
      config:
        root: "%kernel.project_dir%/public"

```

Now you want to change the public filesystem to use an S3 adapter, but the theme, asset and sitemap filesystem should still use the local adapter. You have to set them explicitly:

```yaml
shopware:
  filesystem:
    public:
      url: "{{S3_URL}}"
      type: "amazon-s3"
      config:
        bucket: "{{AWS_BUCKET}}"
        region: "{{AWS_REGION}}"
        endpoint: "{{AWS_ENDPOINT}}"
        visibility: "public"
        credentials:
          key: "{{AWS_ACCESS_KEY_ID}}"
          secret: "{{AWS_SECRET_ACCESS_KEY}}"
    theme:
      type: "local"
      url: "https://your.domain/public"
      config:
        root: "%kernel.project_dir%/public"
    asset:
      type: "local"
      url: "https://your.domain/public"
      config:
        root: "%kernel.project_dir%/public"
    sitemap:
      type: "local"
      url: "https://your.domain/public"
      config:
        root: "%kernel.project_dir%/public"
```

### Additional configuration

If you want to regulate the uploaded file types, then you could add the keys `allowed_extensions`for the public filesystem or `private_local_download_strategy` for the private filesystem.
With the `private_local_download_strategy` key you could choose the download strategy for private files (e.g., the downloadable products):

```yaml
shopware:
  filesystem:
    public:
      # The Adapter Configuration
    private:
      # The Adapter Configuration
    allowed_extensions: # Array with allowed file extensions for public filesystem
    private_allowed_extensions: # Array with allowed file extensions for private filesystem
    private_local_download_strategy: # Name of the download strategy: php, x-sendfile or x-accel
```

The following download strategies are valid:

* `php` (default): A streamed response of content type `application/octet-stream` with binary data
* `x-sendfile` (Apache only): X-Sendfile allows you to use PHP to instruct the server to send a file to a user, without having to load that file into PHP. You must have the [`mod_xsendfile`](https://github.com/nmaier/mod_xsendfile) Apache module installed.
* `x-accel` (Nginx only): X-accel allows for internal redirection to a location determined by a header returned from a backend. See the [example configuration](https://www.nginx.com/resources/wiki/start/topics/examples/x-accel/).

## CDN configuration

If your public files are available on a CDN, you can use the following config to serve images and other assets via that CDN.

```yaml
# <project root>/config/packages/prod/shopware.yml
shopware:
  filesystem:
    public:
      url: "YOUR_CDN_URL"
      type: "local"
      config:
        root: "%kernel.project_dir%/public"
```

::: info
Be aware of the **prod** in the config path. CDNs are typically for production environments, but you can also set them for all environments in `config/packages/shopware.yml`.
:::

## Supported adapter configurations

### Local

```yaml
shopware:
    filesystem:
      {ADAPTER_NAME}:
        type: "local"
        config:
          root: "%kernel.project_dir%/public"
```

### Amazon S3

In order to use the S3 adapter you need to install the `league/flysystem-async-aws-s3` package.

```bash
composer require league/flysystem-async-aws-s3
```

Example configuration:

```yaml
shopware:
    filesystem:
      {ADAPTER_NAME}:
        type: "amazon-s3"
        url: "https://your-cloudfront-url"
        visibility: "private" # Default is "public", can be set only on shopware.filesystem.private
        config:
            bucket: "{your-public-bucket-name}"
            region: "{your-bucket-region}"
            endpoint: "{your-s3-provider-endpoint}"
            root: "{your-root-folder}"
            # Optional, otherwise will be automatically discovered with AWS content discovery
            credentials:
              key: '{your-access-key}'
              secret: '{your-secret-key}'
```

If your S3 provider does not use buckets as subdomain like Minio in default configuration, you need to set `use_path_style_endpoint` to `true` inside `config`.

### Google Cloud Platform

In order to use the Google Cloud Platform adapter you need to install the `league/flysystem-google-cloud-storage` package.

```bash
composer require league/flysystem-google-cloud-storage
```

Example configuration:

```yaml
shopware:
    filesystem:
      {ADAPTER_NAME}:
        type: "google-storage"
        url: "https://storage.googleapis.com/{your-public-bucket-name}"
        visibility: "private" # Default is "public", can be set only on shopware.filesystem.private
        config:
            bucket: "{your-public-bucket-name}"
            projectId: "{your-project-id}"
            keyFilePath: "{path-to-your-keyfile}"
```

The bucket needs to use the "Fine-grained" [ACL mode](https://cloud.google.com/storage/docs/access-control#choose_between_uniform_and_fine-grained_access). This is required so that Shopware can manage the ACL of the objects.

## Add your own adapter

To create your own adapter, check out the [official Flysystem guide](https://flysystem.thephpleague.com/v1/docs/advanced/creating-an-adapter/).

To make your adapter available in Shopware, you will need to create an AdapterFactory for your Flysystem provided adapter. An example of that could look like this:

```php
<?php

use Shopware\Core\Framework\Adapter\Filesystem\Adapter\AdapterFactoryInterface;
use League\Flysystem\AdapterInterface;

class MyFlysystemAdapterFactory implements AdapterFactoryInterface
{
    public function getType(): string
    {
        return 'my-adapter-prefix'; // This must match with the type in the yaml file
    }

    public function create(array $config): AdapterInterface
    {
        // $config contains the given config from the yaml
        return new MyFlysystemAdapter($config);
    }
}
```

This new class needs to be registered in the DI with the tag `shopware.filesystem.factory` to be usable.

---

---

## Message Queue
**Source:** [guides/hosting/infrastructure/message-queue.md](https://developer.shopware.com/docs/v6.6/guides/hosting/infrastructure/message-queue.md)  
# Message Queue

## Overview

Shopware uses the Symfony Messenger component and Enqueue to handle asynchronous messages. This allows tasks to be processed in the background. Thus, tasks can be processed independently of timeouts or system crashes. By default, tasks in Shopware are stored in the database and processed via the browser as long as you are logged into the Administration. This is a simple and fast method for the development process, but not recommended for production systems. With multiple users logged into the Administration, this can lead to a high CPU load and interfere with the smooth execution of PHP FPM.

## Message queue on production systems

On a production system, the message queue should be processed via the CLI instead of the browser in the Administration ([Admin worker](#admin-worker)). This way, tasks are also completed when no one is logged into the Administration and high CPU load due to multiple users in the admin is also avoided. Furthermore, you can change the transport to another system like [RabbitMQ](https://www.rabbitmq.com/). This would, relieve the database and, on the other hand, use a much more specialized service for handling message queues. The following are examples of the steps needed.\
It is recommended to run one or more `messenger:consume` workers. To automatically start the processes again after they stopped because of exceeding the given limits you can use a process control system like [systemd](https://www.freedesktop.org/wiki/Software/systemd/) or [supervisor](http://supervisord.org/running.html).
Alternatively, you can configure a cron job that runs the command periodically.

::: info
Using cron jobs won't take care of maximum running worker, like supervisor can do. They don't wait for another worker to stop. So there is a risk of starting an unwanted amount of workers when you have messages running longer than the set time limit. If the time limit has been exceeded worker will wait for the current message to be finished.
:::

Find here the docs of Symfony: <https://symfony.com/doc/current/messenger.html#deploying-to-production>

::: info
It is recommended to use a third-party message queue to support multiple consumers and/or a greater amount of data to index.
:::

## Execution methods

### CLI worker

::: info
The CLI worker is the recommended way to consume messages.
:::

You can configure the command just to run a certain amount of time and to stop if it exceeds a certain memory limit like:

```bash
bin/console messenger:consume async --time-limit=60 --memory-limit=128M
```

You can also configure the command to consume messages from multiple transports to prioritize them to your needs, as it is recommended by the [Symfony documentation](https://symfony.com/doc/current/messenger.html#prioritized-transports):

```bash
bin/console messenger:consume async low_priority
```

For more information about the command and its configuration, use the -h option:

```bash
bin/console messenger:consume -h
```

If you have configured the cli-worker, you should turn off the admin worker in the Shopware configuration file. Therefore, create or edit the configuration `shopware.yaml`.

```yaml
# config/packages/shopware.yaml
shopware:
    admin_worker:
        enable_admin_worker: false
```

::: warning
Make sure to set up the CLI worker also for the failed queue. Otherwise, failed messages will not be processed.
:::

#### systemd example

We assume the services to be called `shopware_consumer`.

Create a new file `/etc/systemd/system/shopware_consumer@.service`

```bash
[Unit]
Description=Shopware Message Queue Consumer, instance %i
PartOf=shopware_consumer.target

[Service]
Type=simple
User=www-data # Change this to webserver's user name
Restart=always
# Change the path to your shop path
WorkingDirectory=/var/www/html
ExecStart=php /var/www/html/bin/console messenger:consume --time-limit=60 --memory-limit=512M async low_priority

[Install]
WantedBy=shopware_consumer.target
```

Create a new file `/etc/systemd/system/shopware_consumer.target`

```bash
[Install]
WantedBy=multi-user.target

[Unit]
Description=shopware_consumer service
```

Enable multiple instances. Example for three instances:
`systemctl enable shopware_consumer@{1..3}.service`

Enable the dummy target:
`systemctl enable shopware_consumer.target`

At the end start the services:
`systemctl start shopware_consumer.target`

#### supervisord example

Please refer to the [Symfony documentation](https://symfony.com/doc/current/messenger.html#supervisor-configuration) for the setup.

### Admin worker

The admin worker, if used, can be configured in the general `shopware.yml` configuration. If you want to use the admin worker, you have to specify each transport that was previously configured. The poll interval is the time in seconds that the admin worker polls messages from the queue. After the poll interval is over, the request terminates, and the Administration initiates a new request.

```yaml
# config/packages/shopware.yaml
shopware:
    admin_worker:
        enable_admin_worker: true
        poll_interval: 30
        transports: ["async", "low_priority"]
```

## Sending mails over the message queue

By default, Shopware sends the mails synchronously. Since this can affect the page speed, you can switch it to use the Message Queue with a small configuration change.

```yaml
# config/packages/framework.yaml
framework:
    mailer:
        message_bus: 'messenger.default_bus'
```

## Failed messages

If a message fails, it will be moved to the failed transport. The failed transport is configured using the `MESSENGER_TRANSPORT_FAILURE_DSN` env. The default is the Doctrine transport. The messages are retried automatically 3 times. If the message fails again, it will be deleted. You can learn more about the failed transport and how you can configure it in the Symfony Messenger documentation: <https://symfony.com/doc/current/messenger.html#retries-failures>

## Changing the transport

By default, Shopware uses the Doctrine transport. This is simple transport that stores the messages in the database. This is a good choice for development, but not recommended for production systems. You can change the transport to another system like [RabbitMQ](https://www.rabbitmq.com/). This would, relieve the database and, on the other hand, use a much more specialized service for handling message queues. The following are examples of the steps needed.

You can find all available transport options in the Symfony Messenger documentation: <https://symfony.com/doc/current/messenger.html#transport-configuration>

Following environment variables are in use out of the box:

* `MESSENGER_TRANSPORT_DSN` - The DSN to the transport to use (e.g. `doctrine://default`).
* `MESSENGER_TRANSPORT_LOW_PRIORITY_DSN` - The DSN to the transport to use for low priority messages (e.g. `doctrine://default?queue_name=low_priority`).
* `MESSENGER_TRANSPORT_FAILURE_DSN` - The DSN to the transport to use for failed messages (e.g. `doctrine://default?queue_name=failed`).

## Worker count for efficient message processing

The number of workers depends on the number of messages queued and the type of messages they are. Product indexing messages are usually slow, while other messages are processed very fast. Therefore, it is difficult to give a general recommendation. You should be able to monitor the queue and adjust the number of workers accordingly.
Sometimes, it also makes sense to route messages to a different transport to limit the number of workers for a specific type of message to avoid database locks or prioritize messages like sending emails.

## Configuration

### Message bus

The message bus is used to dispatch your messages to your registered handlers. While dispatching your message, it loops through the configured middleware for that bus. The message bus used inside Shopware can be found under the service tag `messenger.bus.default`. It is mandatory to use this message bus if your messages should be handled inside Shopware. However, if you want to send messages to external systems, you can define your custom message bus for that.

You can configure an array of buses and define one default bus in your `framework.yaml`.

```yaml
// <platform root>/src/Core/Framework/Resources/config/packages/framework.yaml
framework:
    messenger:
        default_bus: my.messenger.bus
        buses:
            my.messenger.bus:
```

For more information on this check the [Symfony docs](https://symfony.com/doc/current/messenger/multiple_buses.html).

### Transport

A [transport](https://symfony.com/doc/current/messenger.html#transports-async-queued-messages) is responsible for communicating with your 3rd party message broker. You can configure multiple transports and route messages to multiple or different transports. Supported are all transports that are either supported by [Symfony](https://symfony.com/doc/current/messenger.html#transport-configuration) itself. If you don't configure a transport, messages will be processed synchronously like in the Symfony event system.

You can configure an amqp transport directly in your `framework.yaml` and simply tell Symfony to use your  transports.

In a simple setup you only need to set the transport to a valid DSN like:

```yaml
// <platform root>/src/Core/Framework/Resources/config/packages/queue.yaml
framework:
  messenger:
    transports:
      my_transport:
        dsn: "%env(MESSENGER_TRANSPORT_DSN)%"
```

For more information on this check the [symfony docs](https://symfony.com/doc/current/messenger.html#transport-configuration).

### Routing

You can route messages to different transports. For that, just configure your routing in the `framework.yaml`.

```yaml
// <plugin root>/src/
framework:
    messenger:
      transports:
        async: "%env(MESSENGER_TRANSPORT_DSN)%"
        another_transport: "%env(MESSENGER_TRANSPORT_ANOTHER_DSN)%"
      routing: 
        'Swag\BasicExample\MessageQueue\Message\SmsNotification': another_transport
        'Swag\BasicExample\MessageQueue\Message\AnotherExampleNotification': [async, another_transport]
        '*': async
```

You can route messages by their classname and use the asterisk as a fallback for all other messages. If you specify a list of transports the messages will be routed to all of them. For more information on this check the [Symfony docs](https://symfony.com/doc/current/messenger.html#routing-messages-to-a-transport).

#### Routing overwrites

By default, all messages that implement the `AsyncMessageInterface` will be routed to the `async` transport. The default symfony config detailed above will only let you add additional routing to those messages, however if you need to overwrite the additional routing you can do so by adding the following to your `shopware.yaml`:

```yaml
shopware:
  messenger:
    routing_overwrite:
      'Shopware\Core\Framework\DataAbstractionLayer\Indexing\EntityIndexingMessage': entity_indexing
```

The `shopware.messenger.routing_overwrite` config option accepts the same format as the `framework.messenger.routing` option, but it will overwrite the routing for the given message class instead of adding to it.
This is especially useful if there is a default routing already configured based on a message interface, but you need to change the routing for a specific message.

::: info
This configuration option was added in Shopware 6.6.4.0 and 6.5.12.0.
:::

---

---

## Rate Limiter
**Source:** [guides/hosting/infrastructure/rate-limiter.md](https://developer.shopware.com/docs/v6.6/guides/hosting/infrastructure/rate-limiter.md)  
# Rate Limiter

::: info
This functionality is available starting with Shopware 6.4.6.0.
:::

## Overview

Shopware 6 provides certain rate limits by default that reduces the risk of brute-force attacks for pages like login or password reset.

## Configuration

The configuration for the rate limiter of Shopware 6 resides in the general bundle configuration:

```text
<shop root>
└── config
   └── packages
      └── shopware.yml
```

To configure the default rate limiters for your shop, you need to add the `shopware.api.rate_limiter` map to the `shopware.yml`. Under this key, you can separately define the rate limiters.

In the following, you can find a list of the default limiters:

* `login`: Storefront / Store-API customer authentication.
* `guest_login`: Storefront / Store-API after order guest authentication.
* `oauth`: API oauth authentication / Administration login.
* `reset_password`: Storefront / Store-API customer password reset.
* `user_recovery`: Administration user password recovery.
* `contact_form`: Storefront / Store-API contact form.

```yaml
// <shop root>/config/packages/shopware.yaml
shopware:
  api:
    rate_limiter:
      login:
        enabled: false
      oauth:
        enabled: true
        policy: 'time_backoff'
        reset: '24 hours'
        limits:
          - limit: 3
            interval: '10 seconds'
          - limit: 5
            interval: '60 seconds'
```

### Configuring time backoff policy

The `time_backoff` policy is built by Shopware itself. It enables you to throttle the request in multiple steps with different waiting times.
Below you can find an example which throttles the request for 10 seconds after 3 requests and starting from 5 requests it always
throttles for 60 seconds. If there are no more requests, it will be reset after 24 hours.

```yaml
// <plugin root>/src/Resources/config/rate_limiter.yaml
example_route:
    enabled: true
    policy: 'time_backoff'
    reset: '24 hours'
    limits:
        - limit: 3
          interval: '10 seconds'
        - limit: 5
          interval: '60 seconds'
```

---

---

## Redis
**Source:** [guides/hosting/infrastructure/redis.md](https://developer.shopware.com/docs/v6.6/guides/hosting/infrastructure/redis.md)  
# Redis

[Redis](https://redis.io/docs/latest/get-started/) is an in-memory data storage, that offers high performance and can be used as a cache, message broker, and database. It is a key-value store that supports various data structures like strings, hashes, lists, sets, and sorted sets.
Especially in high-performance and high-throughput scenarios it can give better results, than relying on a traditional relational database.
Therefore, multiple adapter exists in shopware, to offload some tasks from the DB to Redis.

However, as the data that is stored in Redis differs and also the access patterns to this data differ, it makes sense to use different Redis instances with different configurations for different tasks.

The data stored in Redis can be roughly classified into those three categories:

1. Ephemeral data: This data is not critical and can be easily recreated when lost, e.g., caches.
2. Durable, but "aging" data: This data is important and cannot easily be recreated, but the relevance of the data decreases over time, e.g. sessions.
3. Durable and critical data: This data is important and cannot easily be recreated, e.g. carts, number ranges.

Please note that in current Redis versions, it is not possible to use different eviction policies for different databases in the same Redis instance. Therefore, it is recommended to use separate Redis instances for different types of data.

## Ephemeral data

As ephemeral data can easily be restored and is most often used in cases where high performance matters, this data can be stored with no durable persistence.
This means the data is only stored in memory and is lost when the Redis instance is restarted.

For key eviction policy you should use `volatile-lru`, which only automatically deletes data that is expired, as the application explicitly manages the TTL for each cache item.

The caching data (HTTP-Cache & Object cache) is what should be stored in this instance.

## Durable, but "aging" data

As the data stored here is durable and should be persistent, even in the case of a Redis restart, it is recommended to configure the used Redis instance that it will not just keep the data in memory, but also store it on the disk. This can be done by using snapshots (RDB) and Append Only Files (AOF), refer to the [Redis docs](https://redis.io/docs/latest/operate/oss_and_stack/management/persistence/) for details.

`allkeys-lru` should be used as key eviction policy here, as by default more recent data is more important than older data, therefore the oldest values should be discarded, when Redis reach the max memory.

The session data is what should be stored in this instance.

## Durable and critical data

Again this is durable data, that can not easily be recreated, therefore it should be persisted as well.

As the data is critical, it is important to use a key eviction policy that will not delete data that is not expired, therefore `volatile-lru` should be used.

The cart, number range, lock store and increment data is what should be stored in this instance.

## Configuration

Starting with v6.6.8.0 Shopware supports configuring different reusable Redis connections in the`config/packages/shopware.yaml` file under the `shopware` section:

```yaml
shopware:
    # ...
    redis:
        connections:
            ephemeral:
                dsn: 'redis://host1:port/dbindex'
            persistent:
                dsn: 'redis://host2:port/dbindex'
```

Connection names should reflect the actual connection purpose/type and be unique. Also, the names are used as part of the service names in the container, so they should follow the service naming conventions. After defining connections, you can reference them by name in the configuration of different subsystems.

It's possible to use environment variables in the DSN string, e.g. if `REDIS_EPHEMERAL` is set to `redis://host1:port`, the configuration could look like this:

```yaml
shopware:
    # ...
    redis:
        connections:
            ephemeral_1:
                dsn: '%env(REDIS_EPHEMERAL)%/1' # using database 1
            ephemeral_2:
                dsn: '%env(REDIS_EPHEMERAL)%/2' # using database 2
```

### Connection pooling

In high-load scenarios, it is recommended to use persistent connections to avoid the overhead of establishing a new connection for each request. This can be achieved by setting the `persistent` flag in DSN to `1`:

```yaml
shopware:
    redis:
        connections:
            ephemeral:
                dsn: 'redis://host:port/dbindex?persistent=1'
```

Please note that the persistent flag influences connection pooling, not persistent storage of data.

---

---

## Reverse HTTP Cache
**Source:** [guides/hosting/infrastructure/reverse-http-cache.md](https://developer.shopware.com/docs/v6.6/guides/hosting/infrastructure/reverse-http-cache.md)  
# Reverse HTTP Cache

## Overview

A reverse HTTP cache is a cache server placed before the web shop. If you are not familiar with HTTP caching, please refer to the [HTTP cache](../../../concepts/framework/http_cache) concept. The reverse http cache needs the following capabilities to function with Shopware fully:

* Able to differentiate the request with multiple cookies
* Allow clearing the cache using a web request for a specific site or with `/` for all pages

::: info
In this guide, we will use Varnish as an example for HTTP cache.
:::

### The example Setup with Varnish

::: warning
This setup is compatible with Shopware version 6.4 and higher
:::

![Http cache](../../../assets/hosting-infrastructure-reverseHttpCache.svg)

### Shopware Varnish Docker image

Feel free to check out the [Shopware Varnish Docker image](https://github.com/shopware/varnish-shopware) for a quick start. It contains the Shopware default VCL. The containing VCL is for the usage with xkeys.

### Configure Shopware

:::warning
From version v6.6.x onwards, this method is deprecated and will be removed in v6.7.0. Utilising Varnish with Redis involves LUA scripts to determine URLs for the BAN request. This can cause problems depending on the setup or network. Furthermore, Redis clusters are not supported. Therefore, it is advisable to opt for the [Varnish with XKey](#configure-varnish) integration instead.
:::

First, we need to activate the reverse proxy support in Shopware. To enable it, we need to create a new file in `config/packages/storefront.yaml`:

```yaml
# Be aware that the configuration key changed from storefront.reverse_proxy to shopware.http_cache.reverse_proxy starting with Shopware 6.6
shopware:
    http_cache:
        reverse_proxy:
            enabled: true
            ban_method: "BAN"
            # This needs to point to your varnish hosts
            hosts: [ "http://varnish" ]
            # Max parallel invalidations at the same time for a single worker
            max_parallel_invalidations: 3
            use_varnish_xkey: true
```

Also set `SHOPWARE_HTTP_CACHE_ENABLED=1` in your `.env` file.

::: info
The configuration key changed from `storefront.reverse_proxy` up to Shopware 6.5.x to `shopware.http_cache.reverse_proxy` starting with Shopware 6.6.0.0.
So you will need to adjust your config while upgrading.
If you look for the old documentation and examples, you can find it [here](https://developer.shopware.com/docs/v6.5/guides/hosting/infrastructure/reverse-http-cache.html)
:::

#### Trusted proxies

::: info
Since Shopware 6.6, the `TRUSTED_PROXIES` environment variable is no longer taken into account out of the box. Make sure to create a Symfony configuration to make it configurable again [like here](https://github.com/shopware/recipes/blob/main/shopware/docker/0.1/config/packages/trusted_env.yaml).
:::

For the most part, using Symfony and Varnish doesn't cause any problem. But, when a request passes through a proxy, certain request information is sent using either the standard Forwarded header or *X-Forwarded* headers. For example, instead of reading the *REMOTE\_ADDR* header (which will now be the IP address of your reverse proxy), the user's true IP will be stored in a standard Forwarded: for="..." header or an *X-Forwarded-For* header.

If you don't configure Symfony to look for these headers, you will get incorrect information about the client's IP address. Whether or not the client connects via https, the client's port and the hostname are requested.

Go through [Proxies](https://symfony.com/doc/current/deployment/proxies.html) section for more information.

### Varnish Docker Image

Shopware offers a Varnish Docker image that is pre-configured to work with Shopware. You can find the image [here](https://github.com/shopware/varnish-shopware). The image is based on the official Varnish image and contains the Shopware default VCL with few configurations as environment variables.

### Configure Varnish

Varnish XKey is a cache key module that allows you to use Varnish with surrogate keys. It is a module not included in the default Varnish installation. It is available for Varnish 6.0 or higher.

Checkout the official Varnish installation guide [here](https://github.com/varnish/varnish-modules#installation).

And also needs to be enabled in the `config/packages/varnish.yaml` file:

```yaml
# Be aware that the configuration key changed from storefront.reverse_proxy to shopware.http_cache.reverse_proxy starting with Shopware 6.6
shopware:
  # Cache tagging must be disabled with xkey config
  cache:
    tagging:
      each_config: false
      each_snippet: false
      each_theme_config: false

  http_cache:
      reverse_proxy:
        enabled: true
        use_varnish_xkey: true
        hosts:
          - 'varnish-host'
```

Make sure to replace the `__XXX__` placeholders with your actual values.

### Soft Purge vs Hard Purge

The default configuration Varnish uses Hard purges, so when you update a product, the page will be removed from the cache and the next request takes longer because the cache is empty. To avoid this, you can use Soft purges.
Soft purge keeps the old page in case and serves it still to the clients and refreshes the cache in the background. This way the client gets **always** a cached page and the cache is updated in the background.

To enable soft purge, you need to change the varnish configuration.

```diff
-set req.http.n-gone = xkey.purge(req.http.xkey);
+set req.http.n-gone = xkey.softpurge(req.http.xkey);
```

### Debugging

The default configuration removes all headers except the `Age` header, which is used to determine the cache age. If you see only `0` as the `Age` header, it means that the cache is not working.

This problem is mostly caused as the application didn't set `Cache-Control: public` header. To check this you can use `curl` against the upstream server:

```bash
curl -vvv -H 'Host: <sales-channel-domain>' <app-server-ip> 1> /dev/null
```

and you should get a response like:

```text
< HTTP/1.1 200 OK
< Cache-Control: public, s-maxage=7200
< Content-Type: text/html; charset=UTF-8
< Xkey: theme.sw-logo-desktop, ...
```

If you don't see the `Cache-Control: public` header or the `Xkey` header, you need to check the application configuration that you really have enabled the reverse proxy mode.

For more details, please refer to the [Varnish documentation](https://www.varnish-software.com/developers/tutorials/logging-cache-hits-misses-varnish/) on logging cache hits and misses.

## Configure Fastly

Fastly is supported since Shopware 6.4.11.0 is out-of-the-box with some configurations. To enable it, we need to create a new file in `config/packages/storefront.yaml`

```yaml
# Be aware that the configuration key changed from storefront.reverse_proxy to shopware.http_cache.reverse_proxy starting with Shopware 6.6
shopware:
  http_cache:
    reverse_proxy:
        enabled: true
        fastly:
          enabled: true
          api_key: '<personal-token-from-fastly>'
          service_id: '<service-id>'
```

### Fastly soft-purge

::: warning
This feature has been introduced with Shopware version 6.4.15.0
:::

By default, the cache will be immediately purged and the next requesting user will get a slow response as the cache has been deleted. On soft purge, the user still gets the cached response after the purge, but in the configured time interval, the cache will be refreshed. This makes sure that the client gets the fastest response possible.

```yaml
# Be aware that the configuration key changed from storefront.reverse_proxy to shopware.http_cache.reverse_proxy starting with Shopware 6.6
shopware:
  http_cache:
    # Allow to serve the out-dated cache for 300 seconds
    stale_while_revalidate: 300
    # Allow to serve the out-dated cache for an hour if the origin server is offline
    stale_if_error: 3600
    reverse_proxy:
        enabled: true
        fastly:
          enabled: true
          api_key: '<personal-token-from-fastly>'
          service_id: '<service-id>'
          soft_purge: '1'
```

### Fastly VCL Snippets

You can use the [Deployment Helper to automatically deploy Fastly VCL Snippets and keep them up to date](../installation-updates//deployments/deployment-helper.md).

For manual deployment, you can find the VCL Snippets here:

### Cache Invalidations

The Reverse Proxy Cache shares the same invalidation mechanism as the Object Cache and has the same tags. So, when a product is invalidated, the object cache and the HTTP cache will also be invalidated.

::: warning
`bin/console cache:clear` will also clear the HTTP cache. If this is not intended, you should manually delete the `var/cache` folder. The object cache can be cleared with `bin/console cache:pool:clear --all` explicitly.
:::

---

---

## Scheduled task
**Source:** [guides/hosting/infrastructure/scheduled-task.md](https://developer.shopware.com/docs/v6.6/guides/hosting/infrastructure/scheduled-task.md)  
# Scheduled task

## What are scheduled tasks?

Scheduled tasks are a way to schedule messages to the queue on time.
Shopware uses it to run cleanup tasks, update tasks, and other non-time critical tasks in the background.

## Default scheduled tasks

These tasks are registered by default:

| Name                                | Run interval (seconds) |
|-------------------------------------|------------------------|
| log\_entry.cleanup                   | 86400                  |
| shopware.invalidate\_cache           | 20                     |
| app\_update                          | 86400                  |
| app\_delete                          | 86400                  |
| version.cleanup                     | 86400                  |
| webhook\_event\_log.cleanup           | 86400                  |
| sales\_channel\_context.cleanup       | 86400                  |
| product\_keyword\_dictionary.cleanup  | 604800                 |
| product\_download.media.cleanup      | 2628000                |
| delete\_newsletter\_recipient\_task    | 86400                  |
| product\_stream.mapping.update       | 86400                  |
| product\_export\_generate\_task        | 60                     |
| import\_export\_file.cleanup          | 86400                  |
| shopware.sitemap\_generate           | 86400                  |
| cart.cleanup                        | 86400                  |
| shopware.elasticsearch.create.alias | 300                    |

::: info
Some tasks like `shopware.elasticsearch.create.alias` and `shopware.invalidate_cache` are only running when necessary. Elasticsearch task only runs when an Elasticsearch server is configured and enabled.
:::

## Creating a scheduled task

::: info
The following commands or flags (--no-wait) are available starting with Shopware 6.5.5.0.
:::

## List all scheduled tasks

You can list all scheduled tasks with `bin/console scheduled-task:list` command.

## Running scheduled tasks

To run the scheduled tasks, you must set up a background worker like the [Message Queue](message-queue.md) and run the command `bin/console scheduled-task:run`. The command schedules all tasks to the queue and waits until a task needs to be scheduled. It consumes little CPU time or memory.

You can use the flag `--no-wait` and run the command from an operating system scheduler like cron. Check your scheduled task interval to determine the best interval to trigger the command. Example:

```bash
*/5 * * * * /usr/bin/php /var/www/html/bin/console scheduled-task:run --no-wait
```

## Using the symfony scheduler to run tasks

::: info
Running tasks with the symfony scheduler is available starting with Shopware 6.6
:::

::: warning
This feature is experimental.
:::

You can run scheduled tasks as part of your queue workers with the help of the symfony scheduler component.

```bash
bin/console messenger:consume scheduler_shopware
```

On startup of this command reads the `scheduled_task` database table and applies the stored intervals, an entry in this table is optional.  In the event that these intervals are modified in the database, it is necessary to restart the command for the updated intervals to take effect.
To deactivate tasks, set status to `Shopware\Core\Framework\MessageQueue\ScheduledTask\ScheduledTaskDefinition::STATUS_INACTIVE` in this table, and restart the `consume` command.

## Debugging scheduled tasks

You can directly run a single scheduled task without the queue. This is useful for debugging purposes or to have better control of when and which tasks are executed. You can use `bin/console scheduled-task:run-single <task-name>` to run a single task. Example:

```shell
bin/console scheduled-task:run-single log_entry.cleanup
```

---

---

## Installation and Updates
**Source:** [guides/hosting/installation-updates.md](https://developer.shopware.com/docs/v6.6/guides/hosting/installation-updates.md)  
# Installation and Updates

This section will brief you on cluster setup for custom stores, Shopware 6 production template, and deployment to an infrastructure.

---

---

## Cluster Setup
**Source:** [guides/hosting/installation-updates/cluster-setup.md](https://developer.shopware.com/docs/v6.6/guides/hosting/installation-updates/cluster-setup.md)  
# Cluster Setup

The setup of high-scaling systems differs from a normal installation of Shopware. They are completely customized stores with individual templates and extensions.

This guide contains information for everyone who intends to start with such a project.

## Shopware configuration

::: info
This configuration is available starting with Shopware version 6.5.6.0
:::

To configure Shopware for a cluster setup, you have to set the following configuration in your shopware.yaml file:

```yaml
shopware:
    deployment:
        cluster_setup: true
```

This option prevents shopware from running operations locally (meaning only on one node in a cluster), that potentially can corrupt the state of the cluster by having the state of the nodes diverge from each other, e.g. clearing symfony cache files at runtime.

## Symfony Flex template

Use the [Symfony Flex template](../../installation/template) and pin the Shopware versions in the `composer.json` file. This prevents unwanted updates when deploying (without a composer.lock).

## Sources

The following folders are available in the production template:

* **/src**: Here, the project specific bundles and sources can be stored.
* **/config**: Here are the .yaml config files and other possible configurations (routing, admin configs, etc).
* **/config/bundles.php**: In this file, all Symfony bundles are defined, which should be included in the project.

## Third-party sources

Most big-scale projects have a development team assigned. It is responsible for the stability and performance of the system. The integration of external sources via apps or plugins can be useful but should always be viewed with a critical eye. By including those sources, the development team relinquishes control over parts of the system. We recommend including necessary plugins as Composer packages instead of user-managed plugins.

## Redis

We recommend setting up at least five Redis servers for the following resources:

1. [Session](../performance/session) + [cart](../infrastructure/database-cluster#cart-in-redis)
2. [cache.object](../performance/caches#example-replace-some-cache-with-redis)
3. [Lock](../performance/lock-store) + [Increment storage](../performance/increment)
4. [Number Ranges](../performance/number-ranges)
5. [Message Queue](../infrastructure/message-queue#transport-redis-example)\
   Instead of setting up a Redis server for `messenger`, you can also work directly with [RabbitMQ](../infrastructure/message-queue#transport-rabbitmq-example)

The PHP Redis extension provides persistent Redis connections. Persistent connections can help in high load scenarios as each request doesn't have to open and close connections. Using non-persistent Redis connections can also hit the system's maximum open sockets. Because of these limitations, the Redis extension is preferred over Predis.

When a Redis cluster is in usage, the `php.ini` setting `redis.clusters.cache_slots=1` should be set to skip the cluster node lookup on each connection.

## Database cluster

We have compiled some best practices and configurations to allow you to operate Shopware in a clustered database environment. Please refer to the guide below.

## Filesystem

In a multi-app-server system, manage specific directories over a shared filesystem. This includes assets, theme files, and private as well as public filesystems. The recommendation is to use an S3 compatible bucket.

For more information, refer to the [filesystems](../infrastructure/filesystem) section of this guide.

### Shared directories

Besides the S3 bucket, it is also necessary to create certain directories for the app servers as shared filesystem.

## Shopware updates + security

To update your project, we always recommend using a staging environment. However, updates for a project should only be obtained if there are critical problems with the system or if essential features have been provided by Shopware.
Updates of such systems require a certain amount of effort, as issues often arise during deployments to production systems.

### Security plugin

For obtaining security fixes, without version upgrades, we provide a dedicated [Security plugin](https://store.shopware.com/swag136939272659f/shopware-6-sicherheits-plugin.html). This is compatible with all Shopware versions and corresponding hot fixes are only included in versions that are affected.

### Update of composer dependencies

To ensure the security of your Shopware installation, it's essential to be vigilant about third-party dependencies that might be affected by security vulnerabilities. In that case, a new Shopware version will be released with updated dependencies. If an update to the latest Shopware version in a timely manner is not possible, it is recommended to update the affected dependency manually. This can be done by using the following command:

```bash
 composer update <dependency-name>
```

To identify any potential security risk in your current dependencies, it's a good practice to regularly run the [`composer audit`](https://getcomposer.org/doc/03-cli.md#audit) command. This command scans your dependencies and alerts you if there are any known vulnerabilities that need to be addressed.

### Disable auto-update

Shopware's integrated auto-update functionality should be disabled to prevent unwanted updates. Also, this feature is not multi-app server compatible and should be controlled via deployment.

```yaml
shopware:
    auto_update:
        enabled: false
```

## Message queue

On a productive system, the [message queue](../infrastructure/message-queue) should be processed via CLI processes instead of the [Admin worker](../infrastructure/message-queue#admin-worker). This way, messages are completed regardless of logged-in Administration users and CPU load, as messages can be regulated through the amount of worker processes. Furthermore, you can change the transport to another system like [RabbitMQ](https://www.rabbitmq.com/).

It is recommended to run multiple `messenger:consume` workers. To automatically start the processes again after they stopped because of exceeding the given limits you can use a process control system like [systemd](https://www.freedesktop.org/wiki/Software/systemd/) or [supervisor](http://supervisord.org/running.html).

### Own queue

It is also recommended to define your own message queue in addition to the standard message queue. This gives you more control over the load distribution and allows you to prioritize your own processes higher than the data indexing of Shopware.

## Monitoring

Likewise, we recommend setting up an appropriate monitoring dashboard with well-known software such as:

* [Blackfire](https://www.blackfire.io/)
* [Tideways](https://tideways.com/)
* [Datadog](https://www.datadoghq.com/)
* [Elastic](https://www.elastic.co/)

## Local machines

It is important to keep the local development environments of the developers similar to the live environments. A development environment without Redis or Elasticsearch is always too far away from reality and often leads to complications after deployment. Therefore, it is advisable to maintain internal documentation on how to deploy the server structure and how to set up local machines.

## Theme compiling

The [theme compilation](deployments/build-w-o-db#compiling-the-storefront-without-database) in Shopware by default depends on the settings in the database. However, since a connection to the database is usually not guaranteed during deployment, we recommend configuring static theme compilation.

## Strong CPU

For the server setup, pay special attention to CPU speed. This applies to all servers (app, SQL, Elasticsearch, Redis). Usually, it is more optimal to choose a slightly stronger CPU. This has to be determined more precisely depending on the project and load. Experience has shown that systems with powerful CPUs finish processes faster and can release resources sooner.

## Health Check

::: info
This feature is available starting with Shopware version 6.5.5.0
:::

Use the Shopware-provided Health Check API (`/api/_info/health-check`) to monitor the health of your Shopware app server. It responds with HTTP status `200` when the Shopware Application is working and `50x` when it is not.
For docker, you can use: `HEALTHCHECK CMD curl --fail http://localhost/api/_info/health-check || exit 1`

## Performance tweaks

When setting up big-scale projects, there are some settings and conditions that should be taken into account with regard to performance.

Read more on [performance tweaks](../performance/performance-tweaks).

---

---

## Versioning and Dependencies
**Source:** [guides/hosting/installation-updates/composer.md](https://developer.shopware.com/docs/v6.4/guides/hosting/installation-updates/composer.md)  
# Versioning and Dependencies

::: danger
This setup is no longer the recomended way to manage a Shopware installation. Please refer to our [Flex-guide](../../installation/template.md#how-do-i-migrate-from-production-template-to-symfony-flex) on how to migrate to a symfony flex based setup.
:::

## Overview

### Shopware 6 production template

The Shopware 6 production template enables you to build, package and deploy Shopware 6 to production shops. This template is also used to build the official packages distributed by [shopware](https://www.shopware.com/en/download).

The template is optimized for production usage and contains basic development tooling. It is intended as a basis for project customizations, which are usually done by agencies.

### Branches and stability

In each commit, a `composer.lock` is contained to ensure that the version being deployed is the version that was tested in our CI. We currently provide the following branches:

* `6.3`: stable minor and patch releases (`v6.3.0.0-rc2`, `v6.3.0.1`, `v6.3.1.0`, `v6.1.*`, but not `v6.4.0.0`)
* `trunk`: stable major, minor, and patch releases (`v6.3.0.0`, `v6.3.1.0`, `v6.4.0.0`, `v6.5.0.0`...)

The `6.3` branch contains all the 6.3 releases. It is stable now and only gets non-breaking changes. (security issues are an exception).

The `trunk` branch contains the newest stable release, including major releases. That may result in plugins being incompatible, so be careful.

Starting with `6.3.0.0`, we use a slightly modified version of SemVer. The pattern looks like this: 6.MAJOR.MINOR.PATCH. Examples:

* 6.3.2.5 - Major=3, Minor=2, Patch=5
* 6.4.1.0 - Major=4, Minor=1, Patch=0

See also:

### Requirements

To get an overview of the requirements, refer to the following:

NPM and Node are only required during the build process and for development. If you don't have javascript customizations, it is not required at all because the Storefront and Admin are pre-build.

If you are using a separate build server, consider having NPM and Node as build-only requirements. Your operating application server doesn't require any of these to run Shopware 6.

### Setup and install

To set up the environment and install it with a basic setup, run the following commands:

```bash
# clone newest 6.4 patch version from github 
git clone --branch=6.4 https://github.com/shopware/production shopware
cd shopware

# install shopware and dependencies according to the composer.lock 
composer install

# setup the environment
bin/console system:setup
# or create .env yourself, if you need more control
# create jwt secret: bin/console system:generate-jwt-secret
# create app secret: APP_SECRET=$(bin/console system:generate-app-secret)
# create .env

# create database with a basic setup (admin user and Storefront sales channel)
bin/console system:install --create-database --basic-setup

# or use the interactive installer in the browser: /recovery/install/index.php
```

### Update

To update Shopware 6, just run this:

```bash
# pull newest changes from origin
git pull origin

# the (pre|post)-(install|update)-cmd will execute all steps automatically
composer install
```

## Customization

This project is called [production template](https://github.com/shopware/production) because it can be used to create project specific configurations. The template provides a basic setup that is equivalent to the official distribution. If you need customization, the workflow could look like this:

* Fork template
* Make customization
* Add dependencies
* Add project specific plugins
* Update var/plugins.json (bin/console bundle:dump, paths need to be relative to the project root)
* Build Administration or Storefront
* Update composer.json and composer.lock
* Commit changes

### Development

#### Command overview

The following commands and scripts are available:

**Setup/Install/Deployment**

| Command | Description |
| :--- | :--- |
| `bin/console system:setup` | Configure and create .env and optionally create jwt secret |
| `bin/console system:generate-jwt-secret` | Generates a new jwt secret |
| `bin/console system:generate-app-secret` | Outputs a new app secret. This does not update your .env! |
| `bin/console system:install` | Setup database and optional install some basic data |
| `bin/console system:update:prepare` | Run update preparations before the update. Do not update if this fails |
| `bin/console system:update:finish` | Executes the migrations and finishes the update |
| `bin/console theme:change` | Assign theme to a sales channel |

**Build**

::: info
Bash is required for the shell scripts.
:::

| Command | Description |
| :--- | :--- |
| `bin/console theme:compile` | Compile all assigned themes |
| `bin/build.sh` | Complete build including composer install |
| `bin/build-js.sh` | Build Administration and Storefront, including all plugins in `var/plugins.json`. |
| `bin/build-administration.sh` | Just build the Administration. |
| `bin/build-storefront.sh` | Just build the Storefront. You need to have built the Administration once. |

**Dev**

Run `bin/build-js.sh` once to install the npm dependencies.

::: info
Bash is required for the shell scripts.
:::

| Command | Description |
| :--- | :--- |
| `bin/console theme:refresh` | Reload theme.json of active themes |
| `bin/watch-administration.sh` | Watcher for Administration changes, recompile and reload page if required |
| `bin/watch-storefront.sh` | Watcher for Storefront changes, recompile and reload page if required |

### Configuration

See the `README.md` in the `config` folder of the production template.

#### Template overview

This directory tree should give an overview of the template structure.

```text
├── bin/                  # binaries to setup, build and run Symfony console commands 
├── composer.json         # defines dependencies and setups autoloading
├── composer.lock         # pins all dependencies to allow for reproducible installs
├── config                # contains application configuration
│   ├── bundles.php       # defines static Symfony bundles - use plugins for dynamic bundles
│   ├── etc/              # contains the configuration of the docker image
│   ├── jwt/              # secrets for generating jwt tokens - DO NOT COMMIT these secrets
│   ├── packages/         # configure packages - see: config/README.md
│   ├── secrets/          # symfony secrets store - DO NOT COMMIT these secrets
│   ├── services/         # contains some default overrides
│   ├── services.xml      # just imports the default overrides - this file should not change
│   └── services_test.xml # just imports the default overrides for tests
├── custom                # contains custom files
│   ├── plugins           # store plugins
│   ├── static-plugins    # static project specific plugins
├── docker-compose.yml    # example docker-compose
├── Dockerfile            # minimal docker image
├── phpunit.xml.dist      # phpunit config
├── public                # should be the web root
│   ├── index.php         # main entry point for the web application
├── README.md             # this file
├── src
│   ├── Command/*
│   ├── Kernel.php        # our kernel extension
│   └── TestBootstrap.php # required to run unit tests
└── var
    ├── log/              # log dir
    |── cache/            # cache directory for Symfony
    └── plugins.json      # javascript build configuration
```

### Managing Dependencies

#### Composer

You only need to require the things you want. If you only want to run shopware 6 in headless mode, your composer.json could look like this:

```json
{
    "name": "acme/shopware-production",
    "type": "project",
    "license": "MIT",
    "config": {
        "optimize-autoloader": true
    },
    "prefer-stable": true,
    "minimum-stability": "stable",
    "autoload": {
        "psr-4": {
            "Shopware\\Production\\": "src/"
        }
    },
    "require": {
        "php": "~7.4.3",
        "shopware/core": "~v6.4.0"
    }
}
```

#### Require project plugins

If you have project specific plugins, place them under `custom/static-plugins/{YourPlugin}` and require them in your `composer.json`.

::: info
The plugins needs a (stable) version to work with the default stability `stable`.
:::

```bash
composer require "exampleorg/myplugin"
```

External plugins in private repositories can also be required by adding the repository to your `composer.json`. To learn more about the usage of private repositories, see here:

#### Update Shopware packages

Run the following command to update all shopware dependencies:

```bash
composer update "shopware/*"
```

## Deployment

### Docker

The `DOCKERFILE` and docker-compose.yml service definitions should work but are still experimental.

### Storage and caches

The following directories should be shared by all app servers:

```text
.
├── config
│   ├── jwt # ro - should be written on first deployment
│   ├── secrets # rw shared - see, if you want to use it: https://symfony.com/blog/new-in-symfony-4-4-encrypted-secrets-management 
├── public
│   ├── bundles # rw shared - Written by `assets:install` / `theme:compile`, can also be initiated by the Administration
│   ├── media # rw shared
│   ├── theme # rw shared - generated themes by `theme:compile/change`
│   └── thumbnail # rw shared - media thumbnails
│   └── sitemap # rw shared - generated sitemaps
├── var
│   ├── cache # rw local - contains the containers, which contains additional cache directories (twig, translations, etc)
│   ├── log # a - append only, can be change in the monlog config

ro - Readonly after deployment
rw shared - read and write access, it should be shared across the app servers
rw local - locale read and write access
```

Some of these directories, like `public`, can also be changed to a different [Flysystem](../infrastructure/filesystem#flysystem-overview) to host the files on S3.

---

---

## Deployments
**Source:** [guides/hosting/installation-updates/deployments.md](https://developer.shopware.com/docs/v6.6/guides/hosting/installation-updates/deployments.md)  
# Deployments

The following guide explains the fundamental steps to deploy Shopware 6 to a specific infrastructure and how to build assets for Shopware's Administration and Storefront without a database.

---

---

## Building assets of Administration and Storefront without a Database
**Source:** [guides/hosting/installation-updates/deployments/build-w-o-db.md](https://developer.shopware.com/docs/v6.6/guides/hosting/installation-updates/deployments/build-w-o-db.md)  
*(Body truncated in this bundle; follow the link for the rest.)*

# Building assets of Administration and Storefront without a Database

It is common to prebuild assets in professional deployments to deploy the build artifact assets to the production environment. This task is mostly done by a CI job that doesn't have access to the production database. Shopware needs access to the database to look up the installed extensions/load the configured theme variables. To be able to build the assets without a database, we can use static dumped files. All extensions need to be required by Composer to be able to be loaded by the `ComposerPluginLoader`.

::: warning
This guide requires Shopware 6.4.4.0 or higher.
:::

## Compiling the Administration without database

By default, Shopware builds the Administration without extensions if there is no database connection. To include the extensions without a database, you will need to use the `ComposerPluginLoader`. This determines the used plugins by looking up the installed project dependencies. To get this working, the plugin needs to be required in the system using `composer req [package/name]`.

There is a file `bin/ci` which uses the `ComposerPluginLoader` and can be used instead of `bin/console`.
Using this, you can dump the plugins for the Administration with the new file without a database using the command `bin/ci bundle:dump`. It is recommended to call `bin/ci` instead of `bin/console` in the `bin/*.js` scripts, which can be achieved by setting the environment variable `CI=1`.

## Compiling the Storefront without database

To compile the Storefront theme, you will need the theme variables from the database. To allow compiling it without a database, it is possible to dump the variables to the private file system of Shopware. This file system interacts with the local folder `files/theme-config` by default, but for it to be compiled, it should be shared such that settings are shared across deployments. This can be achieved, for example, by using a [storage adapter like s3](../../infrastructure/filesystem). The configuration can be dumped using the command `bin/console theme:dump`, or it happens automatically when changing theme settings or assigning a new theme.

This means that you still **need a dumped configuration from a system with a working database setup**. You then need to copy these files to your setup without a database and follow the steps below.

By default, Shopware still tries to load configurations from the database. In the next step, you will need to change the loader to `StaticFileConfigLoader`. To change that, you will need to create a new file, `config/packages/storefront.yaml` with the following content:

```yaml
storefront:
   theme:
       config_loader_id: Shopware\Storefront\Theme\ConfigLoader\StaticFileConfigLoader
       available_theme_provider: Shopware\Storefront\Theme\ConfigLoader\StaticFileAvailableThemeProvider
       theme_path_builder_id: Shopware\Storefront\Theme\MD5ThemePathBuilder
```

This will force the theme compiler to use the static dumped file instead of looking into the database.

::: info
Warnings about Database errors can still occur but will be caught and should be ignored in this case.
:::

The dumped files should be found in the directory `files/theme-config`

### Example

directory (files/theme-config):

```text
a729322c1f4e4b4e851137c807b4f363.json
index.json
```

index.json

```json
{"99ef1e95716d43d7be78e9d9921c7163":"a729322c1f4e4b4e851137c807b4f363"}
```

```json
{
  "extensions": [],
  "themeConfig": {
    "blocks": {
      "themeColors": {
        "label": {
          "en-GB": "Theme colours",
          "de-DE": "Theme-Farben"
        }
      },
      "typography": {
        "label": {
          "en-GB": "Typography",
          "de-DE": "Typografie"
        }
      },
      "eCommerce": {
        "label": {
          "en-GB": "E-Commerce",
          "de-DE": "E-Commerce"
        }
      },
      "statusColors": {
        "label": {
          "en-GB": "Status messages",
          "de-DE": "Status-Ausgaben"
        }
      },
      "media": {
        "label": {
          "en-GB": "Media",
          "de-DE": "Medien"
        }
      },
      "unordered": {
        "label": {
          "en-GB": "Misc",
          "de-DE": "Sonstige"
        }
      }
    },
    "fields": {
      "sw-color-brand-primary": {
        "label": {
          "en-GB": "Primary colour",
          "de-DE": "Prim\u00e4rfarbe"
        },
        "type": "color",
        "value": "#ff0000",
        "editable": true,
        "block": "themeColors",
        "order": 100
      },
      "sw-color-brand-secondary": {
        "label": {
          "en-GB": "Secondary colour",
          "de-DE": "Sekund\u00e4rfarbe"
        },
        "type": "color",
        "value": "#3d444d",
        "editable": true,
        "block": "themeColors",
        "order": 200
      },
      "sw-border-color": {
        "label": {
          "en-GB": "Border",
          "de-DE": "Rahmen"
        },
        "type": "color",
        "value": "#798490",
        "editable": true,
        "block": "themeColors",
        "order": 300
      },
      "sw-background-color": {
        "label": {
          "en-GB": "Background",
          "de-DE": "Hintergrund"
        },
        "type": "color",
        "value": "#fff",
        "editable": true,
        "block": "themeColors",
        "order": 400
      },
      "sw-color-success": {
        "label": {
          "en-GB": "Success",
          "de-DE": "Erfolg"
        },
        "type": "color",
        "value": "#3cc261",
        "editable": true,
        "block": "statusColors",
        "order": 100
      },
      "sw-color-info": {
        "label": {
          "en-GB": "Information",
          "de-DE": "Information"
        },
        "type": "color",
        "value": "#26b6cf",
        "editable": true,
        "block": "statusColors",
        "order": 200
      },
      "sw-color-warning": {
        "label": {
          "en-GB": "Notice",
          "de-DE": "Hinweis"
        },
        "type": "color",
        "value": "#ffbd5d",
        "editable": true,
        "block": "statusColors",
        "order": 300
      },
      "sw-color-danger": {
        "label": {
          "en-GB": "Error",
          "de-DE": "Fehler"
        },
        "type": "color",
        "value": "#e52427",
        "editable": true,
        "block": "statusColors",
        "order": 400
      },
      "sw-font-family-base": {
        "label": {
          "en-GB": "Fonttype text",
          "de-DE": "Schriftart Text"
        },
        "type": "fontFamily",
        "value": "'Inter', sans-serif",
        "editable": true,
        "block": "typography",
        "order": 100
      },
      "sw-text-color": {
        "label": {
          "en-GB": "Text colour",
          "de-DE": "Textfarbe"
        },
        "type": "color",
        "value": "#2b3136",
        "editable": true,
        "block": "typography",
        "order": 200
      },
      "sw-font-family-headline": {
        "label": {
          "en-GB": "Fonttype headline",
          "de-DE": "Schriftart \u00dcberschrift"
        },
        "type": "fontFamily",
        "value": "'Inter', sans-serif",
        "editable": true,
        "block": "typography",
        "order": 300
      },
      "sw-headline-color": {
        "label": {
          "en-GB": "Headline colour",
          "de-DE": "\u00dcberschriftfarbe"
        },
        "type": "color",
        "value": "#2b3136",
        "editable": true,
        "block": "typography",
        "order": 400
      },
      "sw-color-price": {
        "label": {
          "en-GB": "Price",
          "de-DE": "Preis"
        },
        "type": "color",
        "value": "#2b3136",
        "editable": true,
        "block": "eCommerce",
        "order": 100
      },
      "sw-color-buy-button": {
        "label": {
          "en-GB": "Buy button",
          "de-DE": "Kaufen-Button"
        },
        "type": "color",
        "value": "#0b539b",
        "editable": true,
        "block": "eCommerce",
        "order": 200
      },
      "sw-color-buy-button-text": {
        "label": {
          "en-GB": "Buy button text",
          "de-DE": "Kaufen-Button Text"
        },
        "type": "color",
        "value": "#fff",
        "editable": true,
        "block": "eCommerce",
        "order": 300
      },
      "sw-logo-desktop": {
        "label": {
          "en-GB": "Desktop",
          "de-DE": "Desktop"
        },
        "helpText": {
          "en-GB": "Displayed on viewport sizes above 991px and as a fallback on smaller viewports, if no other logo is set.",
          "de-DE": "Wird bei Ansichten \u00fcber 991px angezeigt und als Alternative bei kleineren Aufl\u00f6sungen, f\u00fcr die kein anderes Logo eingestellt ist."
        },
        "type": "media",
        "value": "http:\/\/shopware.local\/media\/64\/17\/g0\/1678462492\/demostore-logo.png",
        "editable": true,
        "block": "media",
        "order": 100,
        "fullWidth": true
      },
      "sw-logo-tablet": {
        "label": {
          "en-GB": "Tablet",
          "de-DE": "Tablet"
        },
        "helpText": {
          "en-GB": "Displayed between a viewport of 767px to 991px",
          "de-DE": "Wird zwischen einem viewport von 767px bis 991px angezeigt"
        },
        "type": "media",
        "value": "http:\/\/shopware.local\/media\/64\/17\/g0\/1678462492\/demostore-logo.png",
        "editable": true,
        "block": "media",
        "order": 200,
        "fullWidth": true
      },
      "sw-logo-mobile": {
        "label": {
          "en-GB": "Mobile",
          "de-DE": "Mobil"
        },
        "helpText": {
          "en-GB": "Displayed up to a viewport of 767px",
          "de-DE": "Wird bis zu einem Viewport von 767px angezeigt"
        },
        "type": "media",
        "value": "http:\/\/shopware.local\/media\/64\/17\/g0\/1678462492\/demostore-logo.png",
        "editable": true,
        "block": "media",
        "order": 300,
        "fullWidth": true
      },
      "sw-logo-share": {
        "label": {
          "en-GB": "App & share icon",
          "de-DE": "App- & Share-Icon"
        },
        "type": "media",
        "value": "",
        "editable": true,
        "block": "media",
        "order": 400
      },
      "sw-logo-favicon": {
        "label": {
          "en-GB": "Favicon",
          "de-DE": "Favicon"
        },
        "type": "media",
        "value": "http:\/\/shopware.local\/media\/d3\/f5\/b7\/1678462492\/favicon.png",
        "editable": true,
        "block": "media",
        "order": 500
      }
    },
    "sw-color-brand-primary": {
      "extensions": [],
      "name": "sw-color-brand-primary",
      "label": {
        "en-GB": "Primary colour",
        "de-DE": "Prim\u00e4rfarbe"
      },
      "helpText": null,
      "type": "color",
      "value": "#0b539b",
      "editable": true,
      "block": "themeColors",
      "section": null,
      "tab": null,
      "order": 100,
      "sectionOrder": null,
      "blockOrder": null,
      "tabOrder": null,
      "custom": null,
      "scss": null,
      "fullWidth": null
    },
    "sw-color-brand-secondary": {
      "extensions": [],
      "name": "sw-color-brand-secondary",
      "label": {
        "en-GB": "Secondary colour",
        "de-DE": "Sekund\u00e4rfarbe"
      },
      "helpText": null,
      "type": "color",
      "value": "#3d444d",
      "editable": true,
      "block": "themeColors",
      "section": null,
      "tab": null,
      "order": 200,
      "sectionOrder": null,
      "blockOrder": null,
      "tabOrder": null,
      "custom": null,
      "scss": null,
      "fullWidth": null
    },
    "sw-border-color": {
      "extensions": [],
      "name": "sw-border-color",
      "label": {
        "en-GB": "Border",
        "de-DE": "Rahmen"
      },
      "helpText": null,
      "type": "color",
      "value": "#798490",
      "editable": true,
      "block": "themeColors",
      "section": null,
  

… **Truncated.** Full document: https://developer.shopware.com/docs/v6.6/guides/hosting/installation-updates/deployments/build-w-o-db.md


---

