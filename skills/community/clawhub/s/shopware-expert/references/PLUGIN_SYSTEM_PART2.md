# PLUGIN SYSTEM

Compiled excerpts from the Shopware Developer Documentation snapshot. Prefer live docs at [developer.shopware.com](https://developer.shopware.com/) when in doubt.

---

## Plugin Base Guide
**Source:** [guides/plugins/plugins/plugin-base-guide.md](https://developer.shopware.com/docs/v6.6/guides/plugins/plugins/plugin-base-guide.md)  
# Plugin Base Guide

## Overview

Plugins in Shopware are essentially an extension of [Symfony bundles](plugins-for-symfony-developers). Such bundles and plugins can provide their own resources like assets, controllers, services or tests, which you'll learn in the next guides.\
A plugin is the main way to extend your Shopware 6 instance programmatically.

This section guides you through the basics of creating a plugin from scratch, which can then be installed on your Shopware 6 instance. Refer to the Guide section to know how to [Install Shopware 6](../../installation/).

## Prerequisites

All you need for this guide is a running Shopware 6 instance and full access to both the files, as well as the command line.\
Of course, you'll have to understand PHP, but that's a prerequisite for Shopware as a whole and will not be taught as part of this documentation.

## Create your first plugin

Let's get started with creating your plugin by finding a proper name for it.

### Name your plugin

First, you need to find a name for your plugin. We're talking about a technical name here, so it needs to describe your plugins functionality as short as possible, written in UpperCamelCase. To prevent issues with duplicated plugin names, you should add a shorthand prefix for your company.\
Shopware uses "Swag" as a prefix for that case.\
For this example guide we'll use the plugin name **SwagBasicExample.**

::: info
Using a prefix for your plugin name is not just a convention we'd recommend, but a hard requirement if you want to publish your plugin in the [Shopware Community Store](https://store.shopware.com/en).
:::

### **Create the plugin**

Now that you've found your name, it's time to actually create your plugin.

Shopware provides a handy command that you can use to generate the plugin structure. Go to your shopware project's root directory and run the following command:

```bash
bin/console plugin:create SwagBasicExample
```

You can pass an addition flag `-c` or `--create-config` in the above command which would also create a demo configuration file in the `Resources` directory. The command will generate all the basic required files that are needed for an extension to be installed on a Shopware instance. Make sure to adjust the namespace in the files as per your need.

If you want to create the structure manually please follow the instructions below:

For this, please navigate to the directory `custom/plugins`, that you should find in your Shopware 6 installation. Inside the `plugins` directory, create a new directory named after your plugin, so it should look like this: `custom/plugins/SwagBasicExample`

By convention, you'll have another directory in there, which is called `src`. This is not required, but recommended. And that's it for the directory structure for now.

Inside your `src` directory, create a PHP class named after your plugin, `SwagBasicExample.php`.\
This new class `SwagBasicExample` has to extend from Shopware's abstract Plugin class, which is `Shopware\Core\Framework\Plugin`.

Apart from this, only the namespace is missing. You can freely define it, but we'd recommend using a combination of your manufacturer prefix and the technical name, so in this `guide` this would be: `Swag\BasicExample`

```php
// <plugin root>/src/SwagBasicExample.php
<?php declare(strict_types=1);

namespace Swag\BasicExample;

use Shopware\Core\Framework\Plugin;

class SwagBasicExample extends Plugin
{
}
```

Basically that's it for the PHP part, your basic plugin class is already done.

::: info
Refer to this video on **[Creating a plugin](https://www.youtube.com/watch?v=_Tkoq5W7woI)** that shows how to bootstrap a plugin. Also available on our free online training ["Shopware 6 Backend Development"](https://academy.shopware.com/courses/shopware-6-backend-development-with-jisse-reitsma).
:::

#### The composer.json file

You've created the necessary plugin structure and the plugin base class. The only thing missing for your plugin to be fully functional, is a `composer.json` file inside your plugin's root directory.\
`custom/plugins/SwagBasicExample/composer.json`

This file consists of basic information, that Shopware needs to know about your plugin, such as:

* The technical name
* The description
* The author
* The used license
* The current plugin version
* The required dependencies
* ... and a few more

This file can also be read by [Composer](https://getcomposer.org/), but that's not part of this guide.\
Further information you'll have to add in there: The `type` has to be `shopware-platform-plugin`, so Shopware can safely recognize your plugin as such
and the `require` field must include at least `shopware/core`, to check for compatibility.

Here's an example `composer.json` for this guide, which will do the trick:

```javascript
// <plugin root>/composer.json
{
    "name": "swag/basic-example",
    "description": "Description for the plugin SwagBasicExample",
    "version": "1.0.0",
    "type": "shopware-platform-plugin",
    "license": "MIT",
    "authors": [
        {
            "name": "Shopware"
        }
    ],
    "require": {
        "shopware/core": "~6.6.0"
    },
    "extra": {
        "shopware-plugin-class": "Swag\\BasicExample\\SwagBasicExample",
        "label": {
            "de-DE": "Der angezeigte lesbare Name für das Plugin",
            "en-GB": "The displayed readable name for the plugin"
        },
        "description": {
            "de-DE": "Beschreibung in der Administration für das Plugin",
            "en-GB": "Description in the Administration for this plugin"
        }
    },
    "autoload": {
        "psr-4": {
            "Swag\\BasicExample\\": "src/"
        }
    }
}
```

There's another two things that you need to know:

1. The `shopware-plugin-class` information. This has to point to the plugin's base PHP class. The one, that you've previously created.
2. The whole `autoload` part. This has to mention your [PSR-4](https://www.php-fig.org/psr/psr-4/) namespace. So if you'd like to have another namespace for your plugin, this is the place to go.

::: warning
The path you've configured in the configuration `autoload.psr-4`, `src/` in this case, will be referred to as `<plugin root>/src` in almost all code examples. If you're using a custom path here, e.g. just a slash `/`, then the examples would be `<plugin root>/` here instead.
:::

And that's it. The basic structure and all necessary files for your plugin to be installable are done.

::: info
Refer to this video on **[The composer.json plugin file](https://www.youtube.com/watch?v=CY3SlfwkTm8)** that explains the basic structure of the `composer.json` plugin file. Also available on our free online training ["Shopware 6 Backend Development"](https://academy.shopware.com/courses/shopware-6-backend-development-with-jisse-reitsma).
:::

## Install your plugin

You can safely install your plugin now and Shopware should easily recognize it like this.

Open up your command line terminal and navigate to your Shopware 6 directory, the one which also contains the `custom` directory.

Once inside there, you need to refresh the list of plugins, that Shopware knows yet. This is done with the following command:

```bash
php bin/console plugin:refresh
```

There might be a warning appearing regarding the `version` of the `composer.json` file, but you can safely ignore that.\
You should end up with a list like the following:

```bash
Shopware Plugin Service
=======================

 ------------------------------ -------------------------------------------- ----------- ----------------- ---------------------------- ----------- -------- -------------
  Plugin                         Label                                        Version     Upgrade version   Author                       Installed   Active   Upgradeable
 ------------------------------ -------------------------------------------- ----------- ----------------- ---------------------------- ----------- -------- -------------
  SwagBasicExample               The displayed readable name for the plugin   1.0.0                         Shopware                     No          No       No
 ------------------------------ -------------------------------------------- ----------- ----------------- ---------------------------- ----------- -------- -------------
```

This output is a **good sign**, because this means Shopware recognized your plugin successfully. But it's not installed yet, so let's do that.

```bash
php bin/console plugin:install --activate SwagBasicExample
```

This should print the following output:

```bash
Shopware Plugin Lifecycle Service
=================================

 Install 1 plugin(s):
 * The displayed readable name for the plugin (v1.0.0)

 Plugin "SwagBasicExample" has been installed and activated successfully.
```

And that's basically it.\
**You've just successfully created your Shopware 6 plugin!**

## Next steps

There's many more things to discover when creating your first plugin. Hence, here's a list of important articles, that may be of interest for you.

* [Installing data with your plugin](plugin-fundamentals/database-migrations)
* [Learn more about the plugin lifecycle methods](plugin-fundamentals/plugin-lifecycle)
* [Adding a configuration to your plugin](plugin-fundamentals/add-plugin-configuration)
* [Learning about the service container](plugin-fundamentals/dependency-injection)
* [Adding a custom service](plugin-fundamentals/add-custom-service)
* [Start listening to events](plugin-fundamentals/listening-to-events)

---

---

## Plugin Fundamentals
**Source:** [guides/plugins/plugins/plugin-fundamentals.md](https://developer.shopware.com/docs/v6.6/guides/plugins/plugins/plugin-fundamentals.md)  
# Plugin Fundamentals

Shopware plugins are PHP-based extensions that enhance the functionality of the Shopware e-commerce platform. They follow a specific directory structure and have a lifecycle for installation, activation, deactivation, and uninstallation. Plugins can utilize hooks and events to interact with core functionality, and they can have controllers, services, and models to handle specific tasks. Plugin configuration options can be defined, and integration with various parts of Shopware is possible.

You will learn more about it in depth in the following sections.

---

---

## Add Custom CLI Commands
**Source:** [guides/plugins/plugins/plugin-fundamentals/add-custom-commands.md](https://developer.shopware.com/docs/v6.6/guides/plugins/plugins/plugin-fundamentals/add-custom-commands.md)  
# Add Custom CLI Commands

To ease development tasks, Shopware contains the Symfony commands functionality. This allows (plugin-) developers to define new commands executable via the Symfony console at `bin/console`. The best thing about commands is, that they're more than just simple standalone PHP scripts - they integrate into Symfony and Shopware, so you've got access to all the functionality offered by both of them.

Creating a command for Shopware 6 via a plugin works exactly like you would add a command to Symfony. Make sure to have a look at the Symfony commands guide:

## Prerequisites

This guide **does not** explain how to create a new plugin for Shopware 6. Head over to our plugin base guide to learn how to create a plugin at first:

The main requirement here is to have a `services.xml` file loaded in your plugin. This can be achieved by placing the file into a `Resources/config` directory relative to your plugin's base class location.

::: info
Refer to this video on custom **[Creating a CLI command](https://www.youtube.com/watch?v=OL_qNVLLyaI)**. Also available on our free online training ["Shopware 6 Backend Development"](https://academy.shopware.com/courses/shopware-6-backend-development-with-jisse-reitsma).
:::

## Registering your command

From here on, everything works exactly like in Symfony itself. Commands are recognised by Shopware, once they're tagged with the `console.command` tag in the [dependency injection](dependency-injection) container. So to register a new command, just add it to your plugin's `services.xml` and specify the `console.command` tag:

```html
<services>
   <!-- ... -->

   <service id="Swag\BasicExample\Command\ExampleCommand">
       <tag name="console.command"/>
   </service>
</services>
<!-- ... -->
```

Here's a full example `services.xml` which registers your custom command:

```xml
// <plugin root>/src/Resources/config/services.xml
<?xml version="1.0" ?>

<container xmlns="http://symfony.com/schema/dic/services"
           xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
           xsi:schemaLocation="http://symfony.com/schema/dic/services http://symfony.com/schema/dic/services/services-1.0.xsd">

    <services>
        <service id="Swag\BasicExample\Command\ExampleCommand">
            <tag name="console.command"/>
        </service>
    </services>
</container>
```

Your command's class should extend from the `Symfony\Component\Console\Command\Command` class, here's an example:

```php
// <plugin root>/src/Command/ExampleCommand.php
<?php declare(strict_types=1);

namespace Swag\BasicExample\Command;

use Symfony\Component\Console\Command\Command;
use Symfony\Component\Console\Input\InputInterface;
use Symfony\Component\Console\Output\OutputInterface;
use Symfony\Component\Console\Attribute\AsCommand;

// Command name
#[AsCommand(name: 'swag-commands:example')]
class ExampleCommand extends Command
{
    // Provides a description, printed out in bin/console
    protected function configure(): void
    {
        $this->setDescription('Does something very special.');
    }

    // Actual code executed in the command
    protected function execute(InputInterface $input, OutputInterface $output): int
    {
        $output->writeln('It works!');

        return Command::SUCCESS;
    }
}
```

This command is of course only a basic example, so feel free to experiment. As stated above, you now have access to all the functionality offered by Symfony and Shopware.

::: info
For inspiration, maybe have a look at the Symfony documentation - you may for example use [tables](https://symfony.com/doc/current/components/console/helpers/table.html), [progress bars](https://symfony.com/doc/current/components/console/helpers/progressbar.html), or [custom formats](https://symfony.com/doc/current/components/console/helpers/formatterhelper.html).
:::

### Running commands

Commands are run via the `bin/console` executable. To list all available commands, run `bin/console list`:

```text
$: php bin/console list
Symfony 4.4.4 (env: dev, debug: true)

Usage:
  command [options] [arguments]

Options:
  -h, --help            Display this help message
  -q, --quiet           Do not output any message
  -V, --version         Display this application version
      --ansi            Force ANSI output
      --no-ansi         Disable ANSI output
  -n, --no-interaction  Do not ask any interactive question
  -e, --env=ENV         The Environment name. [default: "dev"]
      --no-debug        Switches off debug mode.
  -v|vv|vvv, --verbose  Increase the verbosity of messages: 1 for normal output, 2 for more verbose output and 3 for debug

Available commands:
  about                                   Displays information about the current project
  help                                    Displays help for a command
  list                                    Lists commands
 feature
  feature:dump                            Creating json file with feature config for js testing and hot reloading capabilities.
 assets
  assets:install                          
 bundle
  bundle:dump                             Creates a json file with the configuration for each active Shopware bundle.
 cache
  cache:clear                             Clears the cache
  cache:pool:clear                        Clears cache pools
  cache:pool:delete                       Deletes an item from a cache pool
  cache:pool:list                         List available cache pools
  cache:pool:prune                        Prunes cache pools
  cache:warmup                            Warms up an empty cache
 [...]
```

Each command usually has a namespace like `cache`, so to clear the cache you would execute `php bin/console cache:clear`. If you would like to learn more about commands in general, have a look at [this article](https://symfony.com/doc/current/console.html) in the Symfony documentation.

## More interesting topics

* [Adding a scheduled task](add-scheduled-task)

---

---

## Add Custom Service
**Source:** [guides/plugins/plugins/plugin-fundamentals/add-custom-service.md](https://developer.shopware.com/docs/v6.6/guides/plugins/plugins/plugin-fundamentals/add-custom-service.md)  
# Add Custom Service

## Overview

In this guide you'll learn how to create a custom service using the Symfony [DI Container](https://symfony.com/doc/current/service_container.html).

## Prerequisites

In order to add your own custom service for your plugin, you first need a plugin as base. Therefore, you can refer to the [Plugin Base Guide](../plugin-base-guide).

## Adding service

Adding a custom service requires to load a `services.xml` file with your plugin. This is done by placing a file with name `services.xml` into a directory called `src/Resources/config/`.

Here's our example `services.xml`:

```xml
// <plugin root>/src/Resources/config/services.xml
<?xml version="1.0" ?>

<container xmlns="http://symfony.com/schema/dic/services"
xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
xsi:schemaLocation="http://symfony.com/schema/dic/services http://symfony.com/schema/dic/services/services-1.0.xsd">

    <services>
        <service id="Swag\BasicExample\Service\ExampleService" />
    </services>
</container>
```

Therefore, this is how your service could then look like:

```php
// <plugin root>/src/Service/ExampleService.php
// SwagBasicExample/src/Service/ExampleService.php

<?php declare(strict_types=1);

namespace Swag\BasicExample\Service;

class ExampleService
{
    public function doSomething(): void
    {
        ...
    }
}
```

::: info
By default, all services in Shopware 6 are marked as *private*. Read more about [private and public services](https://symfony.com/doc/current/service_container.html#public-versus-private-services).
:::

## Next steps

You have now created your own custom service. In the same manner, you can create other important plugin classes, such as [commands](add-custom-commands), [scheduled tasks](add-scheduled-task) or a [subscriber to listen to events](listening-to-events).

Furthermore, we also have a guide explaining how to [customize an existing service](adjusting-service) instead.

---

---

## Add Plugin Configuration
**Source:** [guides/plugins/plugins/plugin-fundamentals/add-plugin-configuration.md](https://developer.shopware.com/docs/v6.6/guides/plugins/plugins/plugin-fundamentals/add-plugin-configuration.md)  
*(Body truncated in this bundle; follow the link for the rest.)*

# Add Plugin Configuration

The `Shopware plugin system` provides you with the option to create a configuration page for your plugin without any knowledge of templating or the `Shopware Administration`.

## Prerequisites

To build your own configuration page for your plugin, you first need a plugin as base.
Therefore, you can refer to the [Plugin Base Guide](../plugin-base-guide).

## Create your plugin configuration

::: info
This video is part of the online training ["Backend Development"](https://academy.shopware.com/courses/shopware-6-backend-development-with-jisse-reitsma) available on Shopware Academy for **free**.
:::

All you need to do is create a `config.xml` file inside a `Resources/config` directory in your plugin root.
The content of the `config.xml` will be dynamically rendered in the Administration.
Below you'll find an example structure:

```text
└── plugins
    └── SwagBasicExample
        ├── src
        │   ├── Resources
        │   │   └── config
        │   │       └── config.xml 
        │   └── SwagBasicExample.php
        └── composer.json
```

## Fill your plugin configuration with settings

As you now know how to create configurations, you can start to fill it with life using various configuration options.

### Cards in your configuration

The `config.xml` follows a simple syntax.
You can organize the content in `<card>` elements.
Every `config.xml` must contain a minimum of one `<card>` element and each `<card>` must contain one `<title>` and at least one `<input-field>`.
See the minimum `config.xml` below:

```xml
<!--<plugin root>/src/Resources/config/config.xml-->
<?xml version="1.0" encoding="UTF-8"?>
<config xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:noNamespaceSchemaLocation="https://raw.githubusercontent.com/shopware/shopware/trunk/src/Core/System/SystemConfig/Schema/config.xsd">
    <card>
        <title>Minimal configuration</title>
        <input-field>
            <name>example</name>
        </input-field>
    </card>
</config>
```

Please make sure to specify the `xsi:noNamespaceSchemaLocation` as shown above and fetch the external resource into your IDE if possible.
This enables auto-completion and suggestions for this XML file and will therefore help you to prevent issues and bugs.

### Card Titles

A `<card>` `<title>` is translatable, this is managed via the `lang` attribute.
By default, the `lang` attribute is set to `en-GB`, to change the locale of a `<title>` just add the attribute as follows:

```html
    ...
    <card>
        <title>English Title</title>
        <title lang="de-DE">German Titel</title>
    </card>
    ...
```

### Input fields

As you can see above, every `<input-field>` has to contain at least a `<name>` element.
The `<name>` element is not translatable and has to be unique, since it will be used as the technical identifier for the config element.
The field `<name>` must at least be 4 characters long and consist of only lower and upper case letters.
It can contain numbers, but not at first place - see this RegEx pattern: `[a-zA-Z][a-zA-Z0-9]*`

### The different types of input field

Your `<input-field>` can be of different types, this is managed via the `type` attribute.
Unless defined otherwise, your `<input-field>` will be a text field.
Below you'll find a list of all available `<input-field type="?">`.

| Type          | Configuration settings                                                                                                                                                              | Renders           | Default value example                   |
|:--------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:------------------|:----------------------------------------|
| text          | [copyable](add-plugin-configuration#copyable), [placeholder](add-plugin-configuration#label-placeholder-and-help-text), [length](add-plugin-configuration#text-length-restrictions) | Text field        | Some text                               |
| textarea      | [copyable](add-plugin-configuration#copyable), [placeholder](add-plugin-configuration#label-placeholder-and-help-text)                                                              | Text area         | Some more text                          |
| text-editor   | [placeholder](add-plugin-configuration#label-placeholder-and-help-text)                                                                                                             | HTML editor       | Some text with HTML `<div>`tags`</div>` |
| url           | [copyable](add-plugin-configuration#copyable), [placeholder](add-plugin-configuration#label-placeholder-and-help-text), [length](add-plugin-configuration#text-length-restrictions) | URL field         | <https://example.com>                     |
| password      | [placeholder](add-plugin-configuration#label-placeholder-and-help-text), [length](add-plugin-configuration#text-length-restrictions)                                                | Password field    | \*\*\*\*\*\*\*\*                                |
| int           | [length](add-plugin-configuration#number-length-restrictions)                                                                                                                       | Number field      | 42                                      |
| float         | [length](add-plugin-configuration#number-length-restrictions)                                                                                                                       | Number field      | 42.42                                   |
| bool          |                                                                                                                                                                                     | Switch            | `true` or `false`                       |
| checkbox      |                                                                                                                                                                                     | Checkbox          | `true` or `false`                       |
| datetime      |                                                                                                                                                                                     | Date-time picker  | 2024-04-04T12:00:00.000Z                |
| date          |                                                                                                                                                                                     | Date picker       | 2024-04-05T00:00:00                     |
| time          |                                                                                                                                                                                     | Time picker       | 11:00:00                                |
| colorpicker   |                                                                                                                                                                                     | Color picker      | #189EFF                                 |
| single-select | [options](add-plugin-configuration#options), [placeholder](add-plugin-configuration#label-placeholder-and-help-text)                                                                | Single-Select box | option\_id                               |
| multi-select  | [options](add-plugin-configuration#options), [placeholder](add-plugin-configuration#label-placeholder-and-help-text)                                                                | Multi-Select box  | \[option\_id1, option\_id2]                |

### Input field settings

These settings are used to configure your `<input-field>`.
**Every `<input-field>` has to start with the `<name>` element.**
After the `<name>` element you can configure any of the other settings mentioned above.
Beside these settings, they have the following in common:
[label](add-plugin-configuration#label-placeholder-and-help-text),
[helpText](add-plugin-configuration#label-placeholder-and-help-text),
[defaultValue](add-plugin-configuration#defaultvalue),
[disabled](add-plugin-configuration#disabled),
and [required](add-plugin-configuration#required).

#### Label, placeholder and help text

The settings `<label>`, `<placeholder>` and `<helpText>` are used to label and explain your `<input-field>` and are translatable.
You define your `<label>`, `<placeholder>` and `<helpText>` the same way as the `<card><title>`, with the `lang` attribute.
Please remember, that the `lang` attribute is set to `en-GB` per default.

#### defaultValue

Add the `defaultValue` setting to your `<input-field>` to define a default value for it.
This value will be imported into the database on installing and updating the plugin.
We use [Symfony\Component\Config\Util\XmlUtils](https://github.com/symfony/config/blob/7.1/Util/XmlUtils.php#L211) for casting the values into the correct PHP types.

Below, you'll find an example of how to use this setting.

```html
<input-field type="text">
    <name>textField</name>
    <label>Test field with default value</label>
    <defaultValue>test</defaultValue>
</input-field>
```

#### disabled

You can add the `<disabled>` setting to any of your `<input-field>` elements to disable it.

Below, you'll find an example of how to use this setting.

```html
<input-field>
    <name>email</name>
    <disabled>true</disabled>
</input-field>
```

*Please note, `<disabled>` only accepts boolean values.*

#### required

You can add the `<required>` setting to any of your `<input-field>` elements to mark it accordingly.

Below, you'll find an example of how to use this setting.

```html
<input-field>
    <name>email</name>
    <required>true</required>
</input-field>
```

*Please note, `<required>` only accepts boolean values.*

#### copyable

You can add the `<copyable>` setting to your `<input-field>` which are of type `text` or extensions of it.
This will add a button at the right, which on click copies the content of your `<input-field>` into the clipboard.

Below, you'll find an example of how to use this setting.

```html
<input-field>
    <name>email</name>
    <copyable>true</copyable>
</input-field>
```

*Please note, that `<copyable>` only accepts boolean values*

#### Text length restrictions

You can add the `<minLength>`/`<maxLength>` settings to your `<input-field>` which are of type `text`, `url` or `password`.
With those you can restrict the length of the input.

Below, you'll find an example of how to use this setting.

```html
<input-field type="password">
    <name>token</name>
    <minLength>5</minLength>
    <maxLength>20</maxLength>
</input-field>
```

#### Number length restrictions

You can add the `<min>`/`<max>` settings to your `<input-field>` which are of type `int` or `float`.
With those you can restrict the minimum and maximum value of the input.

Below, you'll find an example of how to use this setting.

```html
<input-field type="int">
    <name>token</name>
    <min>5</min>
    <max>20</max>
</input-field>
```

#### options

You can use `<options>` to add settings to a `<input-field>` of the types `single-select` and `multi-select`.
Each `<option>` represents one setting you can select.

Below you'll find an example.

```html
<input-field type="single-select">
    <name>mailMethod</name>
    <options>
        <option>
            <id>smtp</id>
            <name>English label</name>
            <name lang="de-DE">German label</name>
        </option>
        <option>
            <id>pop3</id>
            <name>English label</name>
            <name lang="de-DE">German label</name>
        </option>
    </options>
</input-field>
```

Each `<options>` element must contain at least one `<option>` element.
Each `<option>` element must contain a

… **Truncated.** Full document: https://developer.shopware.com/docs/v6.6/guides/plugins/plugins/plugin-fundamentals/add-plugin-configuration.md


---

## Add Plugin Dependencies
**Source:** [guides/plugins/plugins/plugin-fundamentals/add-plugin-dependencies.md](https://developer.shopware.com/docs/v6.6/guides/plugins/plugins/plugin-fundamentals/add-plugin-dependencies.md)  
# Add Plugin Dependencies

New in Shopware 6 is the possibility to properly require on other plugins to be in the system. This is done using the `require` feature from composer. Further information about this can be found in the [official composer documentation](https://getcomposer.org/doc/04-schema.md#package-links).

## Setup

Each plugin for Shopware 6 has to own a `composer.json` file for it to be a valid plugin. Creating a plugin is not explained here, make sure to read our [Plugin base guide](../plugin-base-guide) first.

Since every plugin has to own a `composer.json` file, you can simply refer to this plugin by its technical name and its version mentioned in the respective plugin's `composer.json`.

So, those are example lines of the `SwagBasicExample` plugin's `composer.json`:

```json
{
    "name": "swag/swag-basic-example",
    "description": "Plugin quick start plugin",
    "version": "v1.0.0",
    ...
}
```

Important to note is the `name` as well as the `version` mentioned here, the rest of the file is not important for this case here. You're going to need those two information to require them in your own plugin.

In order to require the `SwagBasicExample` plugin now, you simply have to add these two information to your own `composer.json` as a key value pair:

```javascript
// <plugin root>/composer.json
{
    "name": "swag/plugin-dependency",
    "description": "Plugin requiring other plugins",
    "version": "v1.0.0",
    "type": "shopware-platform-plugin",
    "license": "MIT",
    "authors": [
        {
            "name": "shopware AG",
            "role": "Manufacturer"
        }
    ],
    "require": {
        "shopware/core": "6.1.*",
        "swag/SwagBasicExample": "v1.0.0"
    },
    "extra": {
        "shopware-plugin-class": "Swag\\PluginDependency\\PluginDependency",
        "label": {
            "de-DE": "Plugin mit Plugin-Abhängigkeiten",
            "en-GB": "Plugin with plugin dependencies"
        },
        "description": {
            "de-DE": "Plugin mit Plugin-Abhängigkeiten",
            "en-GB": "Plugin with plugin dependencies"
        }
    },
    "autoload": {
        "psr-4": {
            "Swag\\PluginDependency\\": "src/"
        }
    }
}
```

Have a detailed look at the `require` keyword, which now requires both the Shopware 6 version, which **always** has to be mentioned in your `composer.json`, as well as the previously mentioned plugin and its version. Just as in composer itself, you can also use version wildcards, such as `v1.0.*` to only require the other plugin's minor version to be 1.1, not taking the patch version into account when it comes to find the matching plugin version.

Now your plugin isn't installable anymore, until that requirement is fulfilled.

## More interesting topics

* [Using Composer dependencies](using-composer-dependencies)
* [Using NPM dependencies](using-npm-dependencies)

---

---

## Add Scheduled Task
**Source:** [guides/plugins/plugins/plugin-fundamentals/add-scheduled-task.md](https://developer.shopware.com/docs/v6.6/guides/plugins/plugins/plugin-fundamentals/add-scheduled-task.md)  
# Add Scheduled Task

## Overview

Quite often one might want to run any type of code on a regular basis, e.g. to clean up very old entries every once in a while, automatically. Usually known as "Cronjobs", Shopware 6 supports a `ScheduledTask` for this.

## Prerequisites

This guide is built upon our [plugin base guide](../plugin-base-guide), but that one is not mandatory. Knowing how the `services.xml` file in a plugin works is also helpful, which will be taught in our guides about [Dependency Injection](dependency-injection) and [Creating a service](add-custom-service). It is shortly explained here as well though, so no worries!

::: info
Refer to this video on **[Adding scheduled tasks](https://www.youtube.com/watch?v=88S9P3x6wYE)**. Also available on our free online training ["Shopware 6 Backend Development"](https://academy.shopware.com/courses/shopware-6-backend-development-with-jisse-reitsma).
:::

## Registering scheduled task in the DI container

A `ScheduledTask` and its respective `ScheduledTaskHandler` are registered in a plugin's `services.xml`. For it to be found by Shopware 6 automatically, you need to place the `services.xml` file in a `Resources/config/` directory, relative to the location of your plugin's base class. The path could look like this: `<plugin root>/src/Resources/config/services.xml`.

Here's an example `services.xml` containing a new `ScheduledTask` as well as a new `ScheduledTaskHandler`:

```xml
// <plugin root>/src/Resources/config/services.xml
<?xml version="1.0" ?>
<container xmlns="http://symfony.com/schema/dic/services"
           xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
           xsi:schemaLocation="http://symfony.com/schema/dic/services http://symfony.com/schema/dic/services/services-1.0.xsd">
    <services>
        <service id="Swag\BasicExample\Service\ScheduledTask\ExampleTask">
            <tag name="shopware.scheduled.task" />
        </service>
        <service id="Swag\BasicExample\Service\ScheduledTask\ExampleTaskHandler">
            <argument type="service" id="scheduled_task.repository" />
            <tag name="messenger.message_handler" />
        </service>
    </services>
</container>
```

Note the tags required for both the task and its respective handler, `shopware.scheduled.task` and `messenger.message_handler`. Your custom task will now be saved into the database once your plugin is activated.

## ScheduledTask and its handler

As you might have noticed, the `services.xml` file tries to find both the task itself as well as the new task handler in a directory called `Service/ScheduledTask`. This naming is up to you, Shopware 6 decided to use this name though.

Here's the an example `ScheduledTask`:

```php
// <plugin root>/src/Service/ScheduledTask/ExampleTask.php
<?php declare(strict_types=1);

namespace Swag\BasicExample\Service\ScheduledTask;

use Shopware\Core\Framework\MessageQueue\ScheduledTask\ScheduledTask;

class ExampleTask extends ScheduledTask
{
    public static function getTaskName(): string
    {
        return 'swag.example_task';
    }

    public static function getDefaultInterval(): int
    {
        return 300; // 5 minutes
    }
}
```

Your `ExampleTask` class has to extend from the `Shopware\Core\Framework\MessageQueue\ScheduledTask\ScheduledTask` class, which will force you to implement two methods:

* `getTaskName`: The technical name of your task. Make sure to add a vendor prefix to your custom task, to prevent collisions with other plugin's scheduled tasks. In this example this is `swag`.
* `getDefaultInterval`: The interval in seconds at which your scheduled task should be executed.

And that's it for the `ExampleTask` class.

Following will be the respective task handler:

```php
// <plugin root>/src/Service/ScheduledTask/ExampleTaskHandler.php
<?php declare(strict_types=1);

namespace Swag\BasicExample\Service\ScheduledTask;

use Shopware\Core\Framework\MessageQueue\ScheduledTask\ScheduledTaskHandler;
use Symfony\Component\Messenger\Attribute\AsMessageHandler;

#[AsMessageHandler(handles: ExampleTask::class)]
class ExampleTaskHandler extends ScheduledTaskHandler
{
    public function run(): void
    {
        // ...
    }
}
```

The task handler, `ExampleTaskHandler` as defined previously in your `services.xml`, will be annotated with `AsMessageHandler` handling the `ExampleTask` class. In addition, the `ScheduledTaskHandler` has to extend from the class `Shopware\Core\Framework\MessageQueue\ScheduledTask\ScheduledTaskHandler`. This also comes with one method that you need to implement first:

* `run`: This method is executed once your scheduled task is executed. Do everything, that your task is supposed to do here. In this example, it will just create a new file.

Now every five minutes, your task will be executed and it will print an output every time now.

## Executing the scheduled task

Usually scheduled tasks are registered when installing or updating your plugin. If you don't want to reinstall your plugin in order to register your scheduled task, you can also use the following command to achieve this:
`bin/console scheduled-task:register`

In order to properly test your scheduled task, you first have to run the command `bin/console scheduled-task:run`. This will start the `ScheduledTaskRunner`, which takes care of your scheduled tasks and their respective timings. It will dispatch a message to the message bus once your scheduled task's interval is due.

Now you still need to run the command `bin/console messenger:consume` to actually execute the dispatched messages. Make sure, that the `status` of your scheduled task is set to `scheduled` in the `scheduled_task` table, otherwise it won't be executed. This is not necessary, when you're using the admin worker.

## Debugging scheduled tasks

You can directly run a single scheduled task without the queue. This is useful for debugging purposes or to have better control of when and which tasks are executed. You can use `bin/console scheduled-task:run-single <task-name>` to run a single task. Example:

```shell
bin/console scheduled-task:run-single log_entry.cleanup
```

## More interesting topics

* [Adding a custom command](add-custom-commands)

---

---

## Adjusting a Service
**Source:** [guides/plugins/plugins/plugin-fundamentals/adjusting-service.md](https://developer.shopware.com/docs/v6.6/guides/plugins/plugins/plugin-fundamentals/adjusting-service.md)  
# Adjusting a Service

## Overview

In this guide you'll learn how to adjust a service. You can read more about service decoration in the [Symfony documentation](https://symfony.com/doc/current/service_container/service_decoration.html).

## Prerequisites

In order to add your own custom service for your plugin, you first need a plugin as base. Therefore, you can refer to the [Plugin Base Guide](../plugin-base-guide).

::: info
Refer to this video on **[Decorating services](https://www.youtube.com/watch?v=Rgf4c9rd1kw)** explaining service decorations with an easy example. Also available on our free online training ["Shopware 6 Backend Development"](https://academy.shopware.com/courses/shopware-6-backend-development-with-jisse-reitsma).
:::

## Decorating the service

First of all we have to create a new service for this example which gets decorated in the next step. Then we have to add a new service to our `services.xml` with the attribute `decorates` pointing to our service we want to decorate. Next we have to add our service decorator as argument, but we append an `.inner` to the end of the service to keep the old one as reference.

Here's our example `services.xml`:

```xml
// <plugin root>/src/Resources/config/services.xml
<?xml version="1.0" ?>

<container xmlns="http://symfony.com/schema/dic/services"
xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
xsi:schemaLocation="http://symfony.com/schema/dic/services http://symfony.com/schema/dic/services/services-1.0.xsd">

    <services>
        <service id="Swag\BasicExample\Service\ExampleService" />

        <service id="Swag\BasicExample\Service\ExampleServiceDecorator" decorates="Swag\BasicExample\Service\ExampleService">
            <argument type="service" id="Swag\BasicExample\Service\ExampleServiceDecorator.inner" />
        </service>
    </services>
</container>
```

Now we have to define an abstract class because it's more beautiful and not so strict like interfaces. With an abstract class we can add new functions easier, you can read more about this at the end of this article. The abstract class has to include an abstract function called `getDecorated()` which has the return type of our instance.

::: info
To avoid misunderstandings: The abstract service class and the implementation of it is not part of the decoration process itself and most of the times comes either from the Shopware core or from a plugin you want to extend. They are added here to have an example to decorate.
:::

Therefore, this is how your abstract class could then look like:

```php
// <plugin root>/src/Service/AbstractExampleService.php
<?php declare(strict_types=1);

namespace Swag\BasicExample\Service;

abstract class AbstractExampleService
{
    abstract public function getDecorated(): AbstractExampleService; 

    abstract public function doSomething(): string;
}
```

Now we have our abstract class, but no service which uses it. So we create our `ExampleService` which extends from our `AbstractExampleService`. In our service the `getDecorated()` function has to throw an `DecorationPatternException` because it has no decoration yet.

Therefore, your service could then look like this:

```php
// <plugin root>/src/Service/ExampleService.php
<?php declare(strict_types=1);

namespace Swag\BasicExample\Service;

use Shopware\Core\Framework\Plugin\Exception\DecorationPatternException;

class ExampleService extends AbstractExampleService
{
    public function getDecorated(): AbstractExampleService
    {
        throw new DecorationPatternException(self::class);
    }

    public function doSomething(): string
    {
        return 'Did something.';
    }
}
```

The last step is creating our decorated service called `ExampleServiceDecorator` in this example. Our decorated service has to extend from the `AbstractExampleService` and the constructor has to accept an instance of `AbstractExampleService`. Furthermore, the `getDecorated()` function has to return the decorated service passed into the constructor.

Your service could then look like below:

```php
// <plugin root>/src/Service/ExampleServiceDecorator.php
<?php declare(strict_types=1);

namespace Swag\BasicExample\Service;

class ExampleServiceDecorator extends AbstractExampleService
{
    private AbstractExampleService $decoratedService;

    public function __construct(AbstractExampleService $exampleService)
    {
        $this->decoratedService = $exampleService;
    }

    public function getDecorated(): AbstractExampleService
    {
        return $this->decoratedService;
    }

    public function doSomething(): string
    {
        $originalResult = $this->decoratedService->doSomething();

        return $originalResult . ' Did something additionally.';
    }
}
```

## Adding new functions to an existing service

If you plan to add new functions to your service, it is recommended to add them as normal public functions due to backwards compatibility, if you decorate the service at several places. In this example we add a new function called `doSomethingNew()` which first calls the `getDecorated()` and then our new function `doSomethingNew()` because if our decorator does not implement it yet, it will call it from the parent. The advantage of adding it as normal public function is that you can implement it step by step into your other services without any issues. After you have implemented the function in every service decorator, you can make it abstract for the next release. If you add it directly as an abstract function, you will get errors because the function is required for every service decorator.

Here's our example abstract class:

```php
// <plugin root>/src/Service/AbstractExampleService.php
<?php declare(strict_types=1);

namespace Swag\BasicExample\Service;

abstract class AbstractExampleService
{
    abstract public function getDecorated(): AbstractExampleService; 

    abstract public function doSomething(): string;

    public function doSomethingNew(): string
    {
        return $this->getDecorated()->doSomethingNew();
    }
}
```

After we have implemented our new function in the abstract class, we implement it in our service too.

```php
// <plugin root>/src/Service/ExampleService.php
<?php declare(strict_types=1);

namespace Swag\BasicExample\Service;

use Shopware\Core\Framework\Plugin\Exception\DecorationPatternException;

class ExampleService extends AbstractExampleService
{
    public function getDecorated(): AbstractExampleService
    {
        throw new DecorationPatternException(self::class);
    }

    public function doSomething(): string
    {
        return 'Did something.';
    }

    public function doSomethingNew(): string
    {
        return 'Did something new.';
    }
}
```

---

---

## Using Custom Fields of Type Media
**Source:** [guides/plugins/plugins/plugin-fundamentals/custom-fields-of-type-media.md](https://developer.shopware.com/docs/v6.6/guides/plugins/plugins/plugin-fundamentals/custom-fields-of-type-media.md)  
# Using Custom Fields of Type Media

After you have added a custom field of type media, with the Administration or via plugin, you can assign media objects to the different entities. This is often used for products to add more images to the product detail page. If you want to learn more about custom fields you might want to take a look at this guide: [Adding custom fields](../framework/custom-field/add-custom-field).

## Overview

In the product detail page template, the key `page.product.translated.customFields.xxx` with the `xxx`, which is replaced with the corresponding custom field, contains the UUID of the media. Now the ID has just to be resolved with the function [searchMedia](https://github.com/shopware/shopware/blob/v6.3.4.1/src/Core/Framework/Adapter/Twig/Extension/MediaExtension.php#L31-L45):

```php
// platform/src/Core/Framework/Adapter/Twig/Extension/MediaExtension.php
public function searchMedia(array $ids, Context $context): MediaCollection { ... }
```

This function resolves out the corresponding media objects for the given IDs in order to continue working with them afterwards. Here is an example with a custom field (`custom_sports_media_id`) on the product detail page:

```twig
// <plugin root>/src/Resources/views/storefront/page/content/product-detail.html.twig
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

```text
//dump() output
Shopware\Core\Content\Media\MediaEntity {#5302 ▼
  #extensions: array:1 [▶]
  #_uniqueIdentifier: "f69ab8ae42d04e17b2bab5ec2ff0a93c"
  #versionId: null
  #translated: array:3 [▶]
  #createdAt: DateTimeImmutable @1691755154 {#7298 ▶}
  #updatedAt: DateTimeImmutable @1691755154 {#6848 ▶}
  -_entityName: "media"
  -_fieldVisibility: Shopware\Core\Framework\DataAbstractionLayer\FieldVisibility {#4511 ▶}
  #userId: "0189e47673a671198c21a14f15cf563e"
  #mimeType: "image/jpeg"
  #fileExtension: "jpg"
  #fileSize: 21914
  #title: null
  #metaDataRaw: null
  #mediaTypeRaw: "O:47:"Shopware\Core\Content\Media\MediaType\ImageType":3:{s:13:"\x00*\x00extensions";a:0:{}s:7:"\x00*\x00name";s:5:"IMAGE";s:8:"\x00*\x00flags";a:0:{}}"
  #metaData: array:3 [▶]
  #mediaType: Shopware\Core\Content\Media\MediaType\ImageType {#6626 ▶}
  #uploadedAt: DateTimeImmutable @1691755154 {#7376 ▶}
  #alt: null
  #url: "http://YOUR_SHOP_URL.TEST/media/f5/d3/45/1691755154/shirt_red_600x600.jpg"
  #fileName: "shirt_red_600x600"
  #user: null
  #translations: null
  #categories: null
  #productManufacturers: null
  #productMedia: null
  #avatarUsers: null
  #thumbnails: Shopware\Core\Content\Media\Aggregate\MediaThumbnail\MediaThumbnailCollection {#7086 ▶}
  #mediaFolderId: "0189e474eda5709fb8ef632219dd6fc0"
  #mediaFolder: null
  #hasFile: true
  #private: false
  #propertyGroupOptions: null
  #mailTemplateMedia: null
  #tags: null
  #thumbnailsRo: "O:77:"Shopware\Core\Content\Media\Aggregate\MediaThumbnail\MediaThumbnailCollection":2:{s:13:"\x00*\x00extensions";a:0:{}s:11:"\x00*\x00elements";a:4:{s:32:"018 ▶"
  #documentBaseConfigs: null
  #shippingMethods: null
  #paymentMethods: null
  #productConfiguratorSettings: null
  #orderLineItems: null
  #cmsBlocks: null
  #cmsSections: null
  #cmsPages: null
  #documents: null
  #appPaymentMethods: null
  #productDownloads: null
  #orderLineItemDownloads: null
  #customFields: null
  #id: "f69ab8ae42d04e17b2bab5ec2ff0a93c"
}
```

## Avoid loops

This function performs a query against the database on every invocation and should therefore not be used within a loop. To resolve multiple ID's at once just pass it an array of ID's instead.

To read the media objects within the product listing we recommend the following procedure:

```twig
// <plugin root>/src/Resources/views/storefront/component/product/listing.html.twig
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

## Display image

Use a direct html `img` tag to load the original image.

```twig
<img src="{{ sportsMedia.url }}" alt="{{ sportsMedia.alt }}">
```

You can also use the `sw_thumbnails` twig function to load viewport specific images.

```twig
{% sw_thumbnails 'my-sportsMedia-thumbnails' with {
media: sportsMedia
} %}
```

---

---

## Database Migrations
**Source:** [guides/plugins/plugins/plugin-fundamentals/database-migrations.md](https://developer.shopware.com/docs/v6.6/guides/plugins/plugins/plugin-fundamentals/database-migrations.md)  
# Database Migrations

## Overview

In this guide, you'll learn what migrations are and how to use them. Migrations are PHP classes used to manage incremental and reversible database schema changes. Shopware comes with a pre-built Migration System, to take away most of the work for you. Throughout this guide, you will find the `$` symbol representing your command line.

## Prerequisites

In order to add your own database migrations for your plugin, you first need a plugin as base. Therefore, you can refer to the [Plugin Base Guide](../plugin-base-guide).

::: info
Refer to this video on **[Database migrations](https://www.youtube.com/watch?v=__pWwaK6lxw)**. Also available on our free online training ["Shopware 6 Backend Development"](https://academy.shopware.com/courses/shopware-6-backend-development-with-jisse-reitsma).
:::

## File structure

By default, Shopware 6 is looking for migration files in a directory called `Migration` relative to your plugin's base class.

```text
└── plugins
    └── SwagBasicExample
        └── src
            ├── Migration
            │   └── Migration1546422281ExampleDescription.php
            └── SwagBasicExample.php
```

As you can see there is one file in the `<plugin root>/src/Migration` directory. Below you find a break down of what each part of its name means.

| File Name Snippet | Meaning |
| :--- | :--- |
| Migration | Each migration file has to start with Migration |
| 1546422281 | A Timestamp used to make migrations incremental |
| ExampleDescription | A descriptive name for your migration |

### Customizing the migration path / namespace

You are also able to change the migration directory. This is done by choosing another namespace for your migrations, which can be changed by overwriting your plugin's `getMigrationNamespace()` method in the plugin base class:

```php
public function getMigrationNamespace(): string
{
    return 'Swag\BasicExample\MyMigrationNamespace';
}
```

Since the path is read from the namespace, your Migration directory would have to be named `MyMigrationNamespace` now.

## Create migration

To create a new migration, you have to open your Shopware root directory in your terminal and execute the command `database:create-migration`. Below you can see the command used in this example to create the migration seen above in the file structure.

```bash
$ ./bin/console database:create-migration -p SwagBasicExample --name ExampleDescription
```

Below you'll find a break down of the command.

| Command Snippet | Meaning |
| :--- | :--- |
| ./bin/console | Calls the executable Symfony console application |
| database:create-migration | The command to create a new migration |
| -p your\_plugin\_name | -p creates a new migration for the plugin with the name provided |
| --name your\_descriptive\_name | Appends the provided string after the timestamp |

*Note: If you create a new migration yourself, the timestamp will vary.*

If you take a look at your created migration it should look similar to this:

```php
// <plugin root>/src/Migration/Migration1611740369ExampleDescription.php
<?php declare(strict_types=1);

namespace Swag\BasicExample\Migration;

use Doctrine\DBAL\Connection;
use Shopware\Core\Framework\Migration\MigrationStep;

class Migration1611740369ExampleDescription extends MigrationStep
{
    public function getCreationTimestamp(): int
    {
        return 1611740369;
    }

    public function update(Connection $connection): void
    {
        // implement update
    }

    public function updateDestructive(Connection $connection): void
    {
        // implement update destructive
    }
}
```

As you can see your migration contains 3 methods:

* getCreationTimestamp()
* update()
* updateDestructive()

There is no need to change `getCreationTimestamp()`, it returns the timestamp that's also part of the file name. In the `update()` method you implement non-destructive changes which should always be **reversible**. The `updateDestructive()` method is the follow up step, that is run after `update()` and used for **destructive none reversible changes**, like dropping columns or tables. Destructive migrations are only executed explicitly.

::: info
You do not add instructions to revert your migrations within the migration class itself. `updateDestructive` is not meant to revert instructions in `update`. Reverting changes in the database is done explicitly in plugin lifecycle method `uninstall`. Read more about [it here](./plugin-lifecycle#uninstall).
:::

Here's an example of a non-destructive migration, creating a new table:

```php
// <plugin root>/src/Migration/Migration1611740369ExampleDescription.php
<?php declare(strict_types=1);

namespace Swag\BasicExample\Migration;

use Doctrine\DBAL\Connection;
use Shopware\Core\Framework\Migration\MigrationStep;

class Migration1611740369ExampleDescription extends MigrationStep
{
    public function getCreationTimestamp(): int
    {
        return 1611740369;
    }

    public function update(Connection $connection): void
    {
        $query = <<<SQL
CREATE TABLE IF NOT EXISTS `swag_basic_example_general_settings` (
    `id`                INT             NOT NULL,
    `example_setting`   VARCHAR(255)    NOT NULL,
    PRIMARY KEY (id)
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

## SQL schema

If you want to create a migration for your new custom entity, you could execute the following command. This command selects all active entities and saves it into `platform/src/schema`.

```bash
$ ./bin/console dal:create:schema
```

*Note: Your plugin has to be activated, otherwise your custom entity definition will not be considered. The queries are outputted into /schema.*

## Execute migration

When you install your plugin, the migration directory is added to a MigrationCollection and all migrations are executed. Also, when you update a plugin via the Plugin Manager, all **new** migrations are executed. If you want to perform a migration manually as part of your development process, simply create it after installing your plugin. This way, your plugin migration directory will already be registered during the installation process and you can run any newly created migration by hand using one of the following commands.

::: warning
When updating a plugin, do not change a migration that was already executed, since every migration is only run once.
:::

| Command | Arguments | Usage |
| :--- | :--- | :--- |
| database:migrate | identifier (optional) | Calls the update() methods of unhandled migrations |
| database:migrate-destructive | identifier (optional) | Calls the updateDestructive() methods of unhandled migrations |

The identifier argument is used to decide which migrations should be executed. Per default, the identifier is set to run Shopware Core migrations. To run your plugin migrations, set the identifier argument to your plugin's bundle name, in this example `SwagBasicExample`.

```bash
$ ./bin/console database:migrate SwagBasicExample --all
```

## Advanced migration control

Once you have become familiar with the migration process and the development flow, you may want to have finer control over the migrations performed during the installation and update. In this case the `MigrationCollection` which is only filled with your specific migrations, can be accessed via the `InstallContext` and all its subclasses (UpdateContext, ActivateContext, ...). A plugin must reject the automatic execution of migrations in order to have control over the migrations that are executed.

Therefore a typical update method might look more like this:

```php
    public function update(UpdateContext $updateContext): void
    {
        $updateContext->setAutoMigrate(false); // disable auto migration execution

        $migrationCollection = $updateContext->getMigrationCollection();

        // execute all DESTRUCTIVE migrations until and including 2019-11-01T00:00:00+00:00
        $migrationCollection->migrateDestructiveInPlace(1572566400);

        // execute all UPDATE migrations until and including 2019-12-12T09:30:51+00:00
        $migrationCollection->migrateInPlace(1576143014);
    }
```

If you don't use the Shopware migration system, an empty collection (NullObject) will be in the context.

---

---

## Dependency Injection
**Source:** [guides/plugins/plugins/plugin-fundamentals/dependency-injection.md](https://developer.shopware.com/docs/v6.6/guides/plugins/plugins/plugin-fundamentals/dependency-injection.md)  
# Dependency Injection

## Overview

In this guide you'll learn how to inject services into other services. You can read more about injecting services in the [Symfony documentation](https://symfony.com/doc/current/service_container.html#injecting-services-config-into-a-service).

## Prerequisites

In order to add your own custom service for your plugin, you first need a plugin as base. Therefore, you can refer to the [Plugin Base Guide](../plugin-base-guide).

Furthermore, you need a working service. Therefore, you can refer to [Adding a custom service](add-custom-service) guide.

::: info
Refer to this video on **[Injecting services into a command](https://www.youtube.com/watch?v=Z4kyx9J1xaQ)** explaining DI based on the example of a custom CLI command. Also available on our free online training ["Shopware 6 Backend Development"](https://academy.shopware.com/courses/shopware-6-backend-development-with-jisse-reitsma).
:::

## Injecting another service

Let's get started with an example how to inject a service. This example will be about injecting the `SystemConfigService` into our `ExampleService`.

Here's our example `services.xml`:

```xml
// <plugin root>/src/Resources/config/services.xml
<?xml version="1.0" ?>

<container xmlns="http://symfony.com/schema/dic/services"
xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
xsi:schemaLocation="http://symfony.com/schema/dic/services http://symfony.com/schema/dic/services/services-1.0.xsd">

    <services>
        <service id="Swag\BasicExample\Service\ExampleService">
            <argument type="service" id="Shopware\Core\System\SystemConfig\SystemConfigService"/>
        </service>
    </services>
</container>
```

Now we have to add the injected service as argument to our service constructor.

In the following you can find our `ExampleService` where we injected the `SystemConfigService` with an example function `getShopname()` where we use it.

```php
// <plugin root>/src/Service/ExampleService.php
<?php declare(strict_types=1);

namespace Swag\BasicExample\Service;

use Shopware\Core\System\SalesChannel\SalesChannelContext;
use Shopware\Core\System\SystemConfig\SystemConfigService;

class ExampleService
{
    private SystemConfigService $systemConfigService;

    public function __construct(SystemConfigService $systemConfigService)
    {
        $this->systemConfigService = $systemConfigService;
    }

    public function getShopname(SalesChannelContext $context): string
    {
        return $this->systemConfigService->getString('core.basicInformation.shopName', $context->getSalesChannel()->getId());
    }
}
```

---

---

## Listening to Events
**Source:** [guides/plugins/plugins/plugin-fundamentals/listening-to-events.md](https://developer.shopware.com/docs/v6.6/guides/plugins/plugins/plugin-fundamentals/listening-to-events.md)  
# Listening to Events

A way to listen to events in Symfony projects is via an [event subscriber,](https://symfony.com/doc/current/event_dispatcher.html#creating-an-event-subscriber) which is a class that defines one or more methods that listen to one or various events.
It is thus the same in Shopware, so this article will guide you on how to create event subscriber in your Shopware extension.

## Prerequisites

In order to build your own subscriber for your plugin, of course you first need a plugin as base.
To create an own plugin, you can refer to the [Plugin Base Guide](../plugin-base-guide).

::: info
Refer to this video on **[Live coding example with product.loaded event.](https://www.youtube.com/watch?v=cJDaiuyjKJk)**.
Also available on our free online training ["Shopware 6 Backend Development"](https://academy.shopware.com/courses/shopware-6-backend-development-with-jisse-reitsma).
:::

## Creating your own subscriber

### Plugin base class

Registering a custom subscriber requires to load a `services.xml` file with your plugin.
This is done by either placing a file with name `services.xml` into a directory called `src/Resources/config/`.

Basically, that's it already if you're familiar with [Symfony subscribers](https://symfony.com/doc/current/event_dispatcher.html#creating-an-event-subscriber).
Don't worry, we got you covered here as well.

### Creating your new subscriber class

To start creating a subscriber, we need to create a class first implementing EventSubscriberInterface.
As mentioned above, such a subscriber for Shopware 6 looks exactly the same as in Symfony itself.

Therefore, this is how your subscriber could then look like:

```php
// <plugin root>/src/Subscriber/MySubscriber.php
<?php declare(strict_types=1);

namespace Swag\BasicExample\Subscriber;

use Shopware\Core\Content\Product\ProductEvents;
use Shopware\Core\Framework\DataAbstractionLayer\Event\EntityLoadedEvent;
use Symfony\Component\EventDispatcher\EventSubscriberInterface;

class MySubscriber implements EventSubscriberInterface
{
    public static function getSubscribedEvents(): array
    {
        // Return the events to listen to as array like this:  <event to listen to> => <method to execute>
        return [
            ProductEvents::PRODUCT_LOADED_EVENT => 'onProductsLoaded'
        ];
    }

    public function onProductsLoaded(EntityLoadedEvent $event)
    {
        // Do something
        // E.g. work with the loaded entities: $event->getEntities()
    }
}
```

In this example, the subscriber would be located in the `<plugin root>/src/Subscriber` directory.

The subscriber is now listening for the `product.loaded` event to trigger.

Some entities, like orders or products, are versioned.
This means that some events are dispatched multiple times for different versions, but they belong to the same entity.
Therefore, you can check the version of the context to make sure you're only reacting to the live version.

```php
// <plugin root>/src/Subscriber/MySubscriber.php
<?php declare(strict_types=1);

namespace Swag\BasicExample\Subscriber;

use Shopware\Core\Content\Product\ProductEvents;
use Shopware\Core\Defaults;
use Shopware\Core\Framework\DataAbstractionLayer\Event\EntityWrittenEvent;
use Symfony\Component\EventDispatcher\EventSubscriberInterface;

class MySubscriber implements EventSubscriberInterface
{
    public static function getSubscribedEvents(): array
    {
        return [
            ProductEvents::PRODUCT_WRITTEN_EVENT => 'onProductWritten'
        ];
    }

    public function onProductWritten(EntityWrittenEvent $event)
    {
        if ($event->getContext()->getVersionId() !== Defaults::LIVE_VERSION) {
            return;
        }
        // Do something
    }
}
```

Unfortunately, your subscriber is not even loaded yet - this will be done in the previously registered `services.xml` file.

### Registering your subscriber via services.xml

Registering your subscriber to Shopware 6 is also as simple as it is in Symfony.
You're simply registering your (subscriber) service by mentioning it in the `services.xml`.
The only difference to a normal service is that you need to add the `kernel.event_subscriber` tag to your subscriber for it to be recognized as such.

```php
// <plugin root>/src/Resources/config/services.xml
<?xml version="1.0" ?>

<container xmlns="http://symfony.com/schema/dic/services"
           xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
           xsi:schemaLocation="http://symfony.com/schema/dic/services http://symfony.com/schema/dic/services/services-1.0.xsd">

    <services>
        <service id="Swag\BasicExample\Subscriber\MySubscriber">
            <tag name="kernel.event_subscriber"/>
        </service>
    </services>
</container>
```

That's it, your subscriber service is now automatically loaded at runtime, and it should start listening to the mentioned events to be dispatched.

---

---

## Logging
**Source:** [guides/plugins/plugins/plugin-fundamentals/logging.md](https://developer.shopware.com/docs/v6.6/guides/plugins/plugins/plugin-fundamentals/logging.md)  
# Logging

## Overview

As a plugin developer, you may want to log certain actions or errors to a log file to aid in debugging or to simply keep a record of performed actions.

## Prerequisites

This guide is built upon our [plugin base guide](../plugin-base-guide), which explains the basics of a plugin as a whole. Make sure to have a look at it to get started on building your first plugin.

## Configuring Monolog

First, you must make sure that your plugin loads package configuration from the `/Resources/config/packages` folder:

::: code-group

```php [[plugin root]/src/SwagBasicExample.php]
<?php declare(strict_types=1);

namespace Swag\BasicExample;

use Shopware\Core\Framework\Plugin;
use Symfony\Component\Config\FileLocator;
use Symfony\Component\Config\Loader\DelegatingLoader;
use Symfony\Component\Config\Loader\LoaderResolver;
use Symfony\Component\DependencyInjection\ContainerBuilder;
use Symfony\Component\DependencyInjection\Loader\DirectoryLoader;
use Symfony\Component\DependencyInjection\Loader\GlobFileLoader;
use Symfony\Component\DependencyInjection\Loader\YamlFileLoader;

class SwagBasicExample extends Plugin
{
    public function build(ContainerBuilder $container): void
    {
        parent::build($container);

        $locator = new FileLocator('Resources/config');

        $resolver = new LoaderResolver([
            new YamlFileLoader($container, $locator),
            new GlobFileLoader($container, $locator),
            new DirectoryLoader($container, $locator),
        ]);

        $configLoader = new DelegatingLoader($resolver);

        $confDir = \rtrim($this->getPath(), '/') . '/Resources/config';

        $configLoader->load($confDir . '/{packages}/*.yaml', 'glob');
    }
}
```

:::

This is a Symfony Bundle requirement, the same can also be achieved using Bundle Extensions. Please refer to the [Symfony Documentation](https://symfony.com/doc/current/bundles/extension.html).

We will now use monolog configuration to create a channel for your log messages; the channel should be a unique name identifying your plugin. See below for an example:

::: code-group

```yaml [[plugin root]/src/Resources/config/packages/monolog.yaml]

monolog:
  channels: ['my_plugin_channel']
```

:::

Monolog automatically registers a logger service that you can inject in to your services, which is scoped to your channel. You can access the logger with the service ID: `monolog.logger.my_plugin_channel`.

With your newly created channel, you can create a handler, directing your new channel to it.

::: code-group

```yaml [[plugin root]/src/Resources/config/packages/monolog.yaml]
monolog:
  channels: ['my_plugin_channel']

  handlers:
    myPluginLogHandler:
        type: rotating_file
        path: "%kernel.logs_dir%/my_plugin_%kernel.environment%.log"
        level: error
        channels: [ "my_plugin_channel"]
```

:::

Following this approach allows project owners to redirect your channel to a different one to better suit their needs.

---

---

## Plugin Lifecycle Methods
**Source:** [guides/plugins/plugins/plugin-fundamentals/plugin-lifecycle.md](https://developer.shopware.com/docs/v6.6/guides/plugins/plugins/plugin-fundamentals/plugin-lifecycle.md)  
# Plugin Lifecycle Methods

## Overview

A Shopware plugin can be installed, activated, deactivated and then again uninstalled. Those are some plugin lifecycle methods, which will be covered a bit more in this guide.

## Prerequisites

This guide is built upon our [plugin base guide](../plugin-base-guide), which explains the basics of a plugin as a whole. Make sure to have a look at it to get started on building your first plugin.

## Lifecycle methods

Each of the followings methods are going to be part of the plugin bootstrap, in this example the file will be `<plugin root>/src/SwagBasicExample.php`, which is the bootstrap file of the previously mentioned plugin base guide.

Throughout all of the lifecycle methods, you have access to the [service container](dependency-injection) via `$this->container`.

### Install

The install method of a plugin is executed when the plugin is installed. You can use this method to install all the necessary requirements for your plugin, e.g. a new payment method.

```php
// <plugin root>/src/SwagBasicExample
public function install(InstallContext $installContext): void
{
    // Do stuff such as creating a new payment method
}
```

In your install method, you have access to the `InstallContext`, which provides information such as:

* The current plugin version
* The current Shopware version
* The `Context`, which provides a lot more of system information, e.g. the currently used language
* A collection of the [plugin migrations](database-migrations)
* If the migrations should be executed (`isAutoMigrate` or `setAutoMigrate` to prevent the execution)

::: info
You maybe don't want to create new data necessary for your plugin in the `install` method, even though it seems to be the perfect place. That's because an installed plugin is not automatically active yet - hence some data changes would have an impact on the system before the plugin is even active and therefore functioning. A good rule of thumb is: Only install new data or entities, that can be activated or deactivated themselves, such as a payment method. This way you can create a new payment method in the `install` method, but keep it inactive for now.
:::

### Uninstall

The opposite of the `install` method. It gets executed once the plugin is uninstalled. You might want to remove the data, that your plugin created upon installation.

::: warning
You can't simply remove everything that your plugin created previously. Think about a new payment method, that your plugin created and which was then used for actual orders. If you were to remove this payment method when uninstalling the plugin, all the orders that used this payment method would be broken, since the system wouldn't find the used payment method anymore. In this case, you most likely just want to deactivate the respective entity, if possible. Be careful here!
:::

```php
// <plugin root>/src/SwagBasicExample
public function uninstall(UninstallContext $uninstallContext): void
{
    // Remove or deactivate the data created by the plugin
}
```

The `uninstall` method comes with the `UninstallContext`, which offers the same information as the `install` method. There's one more very important information available with the `UninstallContext`, which is the method `keepUserData`.

#### Keeping user data upon uninstall

When uninstalling a plugin, the user is asked if he really wants to delete all the plugin data. The method `keepUserData` of the `UninstallContext` will provide the users decision. If `keepUserData` returns `true`, you should **not** remove important data of your plugin, the user wants to keep them.

```php
// <plugin root>/src/SwagBasicExample
public function uninstall(UninstallContext $uninstallContext): void
{
    parent::uninstall($uninstallContext);

    if ($uninstallContext->keepUserData()) {
        return;
    }

    // Remove or deactivate the data created by the plugin
}
```

::: info
Refer to this video on **[Uninstalling a plugin](https://www.youtube.com/watch?v=v9OXrUJzC1I)** dealing with plugin uninstall routines. Also available on our free online training ["Shopware 6 Backend Development"](https://academy.shopware.com/courses/shopware-6-backend-development-with-jisse-reitsma).
:::

### Activate

The `activate` method is executed once the plugin gets actually activated. You most likely want to do one of the following things here:

* Activate entities that you created in the install method, e.g. such as a payment method
* Create new entities or data, that you couldn't create in the install method

```php
// <plugin root>/src/SwagBasicExample
public function activate(ActivateContext $activateContext): void
{
    // Activate entities, such as a new payment method
    // Or create new entities here, because now your plugin is installed and active for sure
}
```

The `ActivateContext` provides the same information as the `InstallContext`.

### Deactivate

The opposite of the `activate` method. It is triggered once the plugin deactivates the plugin. This method should mostly do the opposite of the plugin's `activate` method:

* Deactivate entities created by the `install` method
* Maybe remove entities, that cannot be deactivated but would harm the system, if they remained in the system while the plugin is inactive

```php
// <plugin root>/src/SwagBasicExample
public function deactivate(DeactivateContext $deactivateContext): void
{
    // Deactivate entities, such as a new payment method
    // Or remove previously created entities
}
```

The `DeactivateContext` provides the same information as the `InstallContext`.

### Update

The `update` method is executed once your plugin gets updated to a new version. You do not need to update database entries here, since this should be done via [plugin migrations](database-migrations). Otherwise you'd have to check if this specific update to an entity was already done in a previous `update` method execution, mostly by using plugin version conditions.

However, of course you can still do that if necessary. Also, non-database updates can be done here.

```php
// <plugin root>/src/SwagBasicExample
public function update(UpdateContext $updateContext$context): void
{
    // Update necessary stuff, mostly non-database related
}
```

The `UpdateContext` provides the same information as the `InstallContext`, but comes with one more method. In order to get the new plugin version, you can use the method `getUpdatePluginVersion` in contrast to the `getCurrentPluginVersion`, which will return the currently installed plugin version.

### PostInstall and PostUpdate methods

There are two more lifecycle methods, that are worth mentioning: `PostUpdate` and `PostInstall`, which are executed **after** the respective process of installing or updating your plugin is fully and successfully done.

```php
// <plugin root>/src/SwagBasicExample
public function postInstall(InstallContext $installContext): void
{
}

public function postUpdate(UpdateContext $updateContext): void
{
}
```

---

---

## Use Plugin Configuration
**Source:** [guides/plugins/plugins/plugin-fundamentals/use-plugin-configuration.md](https://developer.shopware.com/docs/v6.6/guides/plugins/plugins/plugin-fundamentals/use-plugin-configuration.md)  
# Use Plugin Configuration

In our guide on how to [add a plugin configuration](add-plugin-configuration), you can learn how to provide this possibility to use configuration options in your plugins. This guide will aid you on how to then use this configuration in your plugin.

## Prerequisites

In order to add a plugin configuration, you sure need to provide your plugin first. However, you won't learn to create a plugin in this guide. Head over to our [plugin base guide](../plugin-base-guide) to create your plugin first. It is also recommended to know how to setup a [plugin configuration](add-plugin-configuration) in the first instance. In this example, the configurations will be read inside of a subscriber, so knowing the [Listening to events](listening-to-events) guide will also be helpful.

## Overview

The plugin in this example already knows a subscriber, which listens to the `product.loaded` event and therefore will be called every time a product is loaded.

```php
// <plugin root>/src/Subscriber/MySubscriber.php
<?php declare(strict_types=1);

namespace Swag\BasicExample\Subscriber;

use Shopware\Core\Framework\DataAbstractionLayer\Event\EntityLoadedEvent;
use Symfony\Component\EventDispatcher\EventSubscriberInterface;
use Shopware\Core\Content\Product\ProductEvents;

class MySubscriber implements EventSubscriberInterface
{
    public static function getSubscribedEvents(): array
    {
        return [
            ProductEvents::PRODUCT_LOADED_EVENT => 'onProductsLoaded'
        ];
    }

    public function onProductsLoaded(EntityLoadedEvent $event): void
    {
        // Do stuff with the product
    }
}
```

For this guide, a very small plugin configuration file is available as well:

```xml
// <plugin root>/src/Resources/config/config.xml
<?xml version="1.0" encoding="UTF-8"?>
<config xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:noNamespaceSchemaLocation="https://raw.githubusercontent.com/shopware/shopware/trunk/src/Core/System/SystemConfig/Schema/config.xsd">

    <card>
        <title>Minimal configuration</title>
        <input-field>
            <name>example</name>
        </input-field>
    </card>
</config>
```

Just a simple input field with the technical name `example`. This will be necessary in the next step.

## Reading the configuration

Let's get to the important part. Reading the plugin configuration is based on the `Shopware\Core\System\SystemConfig\SystemConfigService`. This service is responsible for reading all configs from Shopware 6, such as the plugin configurations.

Inject this service into your subscriber using the [DI container](https://symfony.com/doc/current/service_container.html).

```xml
// <plugin root>/src/Resources/config/services.xml
<?xml version="1.0" ?>

<container xmlns="http://symfony.com/schema/dic/services"
           xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
           xsi:schemaLocation="http://symfony.com/schema/dic/services http://symfony.com/schema/dic/services/services-1.0.xsd">

    <services>
        <service id="Swag\BasicExample\Subscriber\MySubscriber">
            <argument type="service" id="Shopware\Core\System\SystemConfig\SystemConfigService" />
            <tag name="kernel.event_subscriber"/>
        </service>
    </services>
</container>
```

Note the new `argument` being provided to your subscriber. Now create a new field in your subscriber and pass in the `SystemConfigService`:

```php
// <plugin root>/src/Subscriber/MySubscriber.php
<?php declare(strict_types=1);

namespace Swag\BasicExample\Subscriber;

...
use Shopware\Core\System\SystemConfig\SystemConfigService;

class MySubscriber implements EventSubscriberInterface
{
    private SystemConfigService $systemConfigService;

    public function __construct(SystemConfigService $systemConfigService)
    {
        $this->systemConfigService = $systemConfigService;
    }

    public static function getSubscribedEvents(): array
    {
        ...
    }
    ...
}
```

So far, so good. The `SystemConfigService` is now available in your subscriber.

This service comes with a `get` method to read the configurations. The first idea would be to simply call `$this->systemConfigService->get('example')` now, wouldn't it? Simply using the technical name you've previously set for the configuration.

But what would happen, if there were more plugins providing the same technical name for their very own configuration field? How would you access the proper field, how would you prevent plugin conflicts?

That's why the plugin configurations are always prefixed. By default, the pattern is the following: `<BundleName>.config.<configName>`. Thus, it would be `SwagBasicExample.config.example` here.

```php
// <plugin root>/src/Subscriber/MySubscriber.php
<?php declare(strict_types=1);

namespace Swag\BasicExample\Subscriber;

...

class MySubscriber implements EventSubscriberInterface
{
    ...
    public function onProductsLoaded(EntityLoadedEvent $event): void
    {
        $exampleConfig = $this->systemConfigService->get('SwagBasicExample.config.example', $salesChannelId);
    }
}
```

::: info
Set the `saleschannelId` to `null` for the plugin configuration to be used by all Sales Channels else set to the corresponding Sales Channel ID.
:::

---

---

## Adding Composer Dependencies
**Source:** [guides/plugins/plugins/plugin-fundamentals/using-composer-dependencies.md](https://developer.shopware.com/docs/v6.6/guides/plugins/plugins/plugin-fundamentals/using-composer-dependencies.md)  
# Adding Composer Dependencies

In this guide you'll learn how to add Composer dependencies to your project.

## Prerequisites

All you need for this guide is a running Shopware 6 instance and full access to both the files and a running plugin. Of course you'll have to understand PHP, but that's a prerequisite for Shopware as a whole and will not be taught as part of this documentation. Further a basic understanding of Node and NPM is required.

## Adding a Composer plugin to the `composer.json` file

In this guide we will install [`exporter`](https://github.com/sebastianbergmann/exporter), which provides the functionality to export PHP variables for visualization.

Now we can simply install the `exporter` package by adding `"sebastian/exporter": "*"` to the list in `require` section of the `composer.json` of our plugin.

Now we can simply install `exporter` by running `composer require sebastian/exporter` in your plugin directory.

After that we have to add our dependency to shopware back in.

::: warning
The `vendor` directory, where the Composer saves the dependencies, has to be included in the plugin bundle. The plugin bundle size is not allowed to exceed 5 MB.
:::

## Executing composer commands during plugin installation

In order that the additional package our plugin requires are installed as well when our plugin is installed, shopware need to execute composer commands to do so.
Therefore, we need to overwrite the `executeComposerCommands` method in our plugin base class and return true.

```php
// <plugin root>/src/SwagBasicExample.php
<?php declare(strict_types=1);

namespace Swag\BasicExample;

use Shopware\Core\Framework\Plugin;

class SwagBasicExample extends Plugin
{
    public function executeComposerCommands(): bool
    {
        return true;
    }

}
```

## Using the Composer plugin

PHP doesn't require a build system, which means that we can just add `use` statements and then use the Composer dependency directly.

The following code sample imports `SebastianBergmann\Exporter\Exporter` and logs `hello, world!` to the Symfony profiler logs whenever the `NavigationPageLoadedEvent` is fired. Learn how to [register this listener](listening-to-events).

```php
// <plugin root>/src/SwagBasicExample.php
<?php
namespace SwagBasicExample\Subscriber;

use Shopware\Core\Framework\DataAbstractionLayer\Event\EntityLoadedEvent;
use Symfony\Component\EventDispatcher\EventSubscriberInterface;
use Shopware\Storefront\Page\Navigation\NavigationPageLoadedEvent;

use Psr\Log\LoggerInterface;
use SebastianBergmann\Exporter\Exporter;

class MySubscriber implements EventSubscriberInterface
{
     private LoggerInterface $logger;

    public function __construct(
        LoggerInterface $logger
    ) {
        $this->logger = $logger;
    }

    public static function getSubscribedEvents(): array
    {
        // Return the events to listen to as array like this:  <event to listen to> => <method to execute>
        return [
            NavigationPageLoadedEvent::class => 'onNavigationPage'
        ];
    }

    public function onNavigationPage(NavigationPageLoadedEvent $event)
    {
        $exporter = new Exporter;
        $this->logger->info($exporter->export('hello, world!'));
    }
}
```

## Adding private Composer dependencies

You can bundle Composer dependencies with your plugin by adding them to the `/packages/` folder of your plugin.

Example structure:

```text
SwagBasicExample
├── packages
│   └── my-private-dependency/
│       ├── composer.json
│       └── src/
│           └── SomeCoolService.php
├── src/
│   └── SwagBasicExample.php
└── composer.json
```

You can then require them like other dependencies:

```text
"require": {
    "my-vendor-name/my-private-dependency": "^1.2.3",
}
```

## More interesting topics

* [Using NPM dependencies](using-npm-dependencies)
* [Adding plugin dependencies](add-plugin-dependencies)

---

---

## Adding NPM Dependencies
**Source:** [guides/plugins/plugins/plugin-fundamentals/using-npm-dependencies.md](https://developer.shopware.com/docs/v6.6/guides/plugins/plugins/plugin-fundamentals/using-npm-dependencies.md)  
# Adding NPM Dependencies

In this guide, you'll learn how to add NPM dependencies to your project.

## Prerequisites

All you need for this guide is a running Shopware 6 instance and full access to both the files and a running plugin. Of course, you'll have to understand JavaScript, but that's a prerequisite for Shopware as a whole and will not be taught as part of this documentation. Further, a basic understanding of Node and NPM is required.

## Video

This guide is also available as a video:

::: warning
This video shows how to resolve the NPM package name as an alias. We recommend resolving all node\_modules instead like shown in the code example below.
:::

## Adding a npm package to the Administration or the Storefront

Presuming you have `npm` installed, run `npm init -y` in the `<plugin root>src/Resources/app/administration/` folder or the `<plugin root>src/Resources/app/storefront/` folder. This command creates a `package.json` file in the respective folder, depending on the environment you're working in. To add a package to the `package.json` file simply run the `npm install` command. In this example we will be installing [`missionlog`](https://www.npmjs.com/package/missionlog).

So in order to install `missionlog`, run `npm install missionlog` in the folder you have created your `package.json` file in.

## Registering a package in the build system

Shopware's storefront as well as administration is based on the build system [Webpack](https://webpack.js.org/). Webpack is a source file bundler: In essence it bundles all the source files into a single `bundle.js` to be shipped to a browser. So in order to make Webpack aware of the new dependency, we have to register it and give it an alias/pseudonym so that the package can be bundled correctly.

To do this, we create a new folder called "build" under either `Resources/app/storefront` or `Resources/app/administration`. In this build folder we create a new file with the name `webpack.config.js`. We thereby make it possible to extend the Webpack configuration of Shopware.

```javascript
module.exports = (params) => {
    return { 
        resolve: { 
            modules: [
                `${params.basePath}/Resources/app/storefront/node_modules`,
            ],
       } 
   }; 
}
```

Let us take a closer look at the code. In the first line, we export a so-called arrow function. The build system from Shopware calls this function when either the Administration or Storefront is being built.

Now we add the `node_modules` folder from our extension. `resolve.modules` tells webpack what directories should be searched when resolving modules. By default, the shopware webpack config only considers the `node_modules` folder of the platform. By accessing `params.basePath` we get the absolute path to our extension. We then add the rest of the path to our extensions `node_modules`. Now webpack will also search for modules in our `node_modules` folder.

## Using the dependency

Once we have installed all the dependencies and registered the package in the build system, we can use the package in our own code.

```javascript
// <plugin root>/src/Resources/app/storefront/src/example.plugin.js
const { PluginBaseClass } = window;

// Import logger
import { log } from 'missionlog';

// Initializing the logger
log.init({ initializer: 'INFO' }, (level, tag, msg, params) => {
    console.log(`${level}: [${tag}] `, msg, ...params);
});

// The plugin skeleton
export default class ExamplePlugin extends PluginBaseClass {
    init() {
        console.log('init');

        // Use logger
        log.info('initializer', 'example plugin got started', this);
    }
}
```

We import the function log as well as the constants tag via `destructuring` in the specified code and register our above plugin in our main.js file, so it can be loaded by the plugin system.

```javascript
// <plugin root>/src/Resources/app/storefront/src/main.js
import ExamplePlugin from './example.plugin';

PluginManager.register(
    'ExamplePlugin',
    ExamplePlugin
);
```

The final step in this process is to build your Storefront or Administration so that your changes are processed by Webpack.

```bash
# Build the Storefront
./bin/build-storefront.sh

# Build the Administration
./bin/build-administration.sh
```

## Next steps

Now that you know how to include new `npm` dependencies you might want to create a service with them. Learn how to do that in this guide: [How to add a custom-service](../administration/add-custom-service)

If you want to add [Composer dependencies](using-composer-dependencies), or even other [plugin dependencies](add-plugin-dependencies), we've got you covered as well.

---

---

## Plugins for Symfony Developers
**Source:** [guides/plugins/plugins/plugins-for-symfony-developers.md](https://developer.shopware.com/docs/v6.6/guides/plugins/plugins/plugins-for-symfony-developers.md)  
# Plugins for Symfony Developers

## Overview

This guide serves as an entry point for developers familiar with the concepts of `Symfony bundles`.

::: info
Check out our [Shopware Toolbox PHPStorm extension](../../../resources/tooling/ide/shopware-toolbox) with useful features like autocompletion, code generation or guideline checks.
:::

## Prerequisites

This guide handles some base concepts of Shopware plugins. Therefore, you may want to have a look at [Plugin base guide](plugin-base-guide) first.

As this guide also references the functionality of Symfony bundles, you should have at least a basic knowledge of it. You may want to have a look or refresh your knowledge on Symfony's [Bundle system](https://symfony.com/doc/current/bundles.html).

## Symfony bundles

A bundle is the Symfony's preferred way to provide additional third-party features to any Symfony application. Those bundles are everywhere: Symfony even outsources many of its core features into external bundles. The template engine `Twig`, the `Security` bundle, the `WebProfiler`, as well as many other third-party bundles can be installed on demand to extend your Symfony application in any way. The Bundle System is Symfony's way of providing an extendable framework with plugin capabilities.

## Shopware plugins

Shopware is building upon the `Symfony Bundle System` to extend its functionality even more. This allows the Shopware Plugin System to function as a traditional plugin system with features like plugin lifecycles and more.

Whenever you create a Shopware plugin, you have to extend the `Shopware\Core\Framework\Plugin` class. If you investigate this class, you will see that this class extends `Shopware\Core\Framework\Bundle`, which in return extends the Symfony's `Bundle` class:

```php
// 
class YourNamespace\PluginName extends

    // plugin lifecycles
    abstract class Shopware\Core\Framework\Plugin extends

        // adds support for migrations, filesystem, events, themes
        abstract class Shopware\Core\Framework\Bundle extends

            // Symfony base bundle
            abstract class Symfony\Component\HttpKernel\Bundle
```

As you can see, any Shopware plugin is also a Symfony bundle internally as well, and will be handled as such by Symfony. A plugin adds support for some cases, specific to the Shopware environment. These include, for example, handling plugin migrations and registering Shopware business events.

### Plugin lifecycle

As mentioned before, Shopware extends the `Symfony Bundle System` with some functionality to adjust its use for the Shopware ecosystem. For you as plugin developer, the most important addition is the extended plugin lifecycle.

A Shopware plugin runs through a lifecycle. Your plugin's base class can implement the following methods to execute any sort of installation or maintenance tasks.

| Lifecycle | Description |
| :--- | :--- |
| `install()` | Executed on plugin install |
| `postInstall()` | Executed **after** successful plugin install |
| `update()` | Executed on plugin update |
| `postUpdate()` | Executed **after** successful plugin update |
| `uninstall()` | Executed on plugin uninstallation |
| `activate()` | Executed **before** plugin activation |
| `deactivate()` | Executed **before** plugin deactivation |

## Next steps

Now that you know about the differences between a Symfony bundle and a Shopware plugin, you might also want to have a look into the following Symfony-specific topics and how they are integrated in Shopware 6:

* [Dependency Injection](plugin-fundamentals/dependency-injection)
* [Listening to events](plugin-fundamentals/listening-to-events)

::: info
Here are some useful videos explaining:

* **[Bundle Methods in a plugin](https://www.youtube.com/watch?v=cUXcDwQwmPk)**
* **[Symfony services in Shopware 6](https://www.youtube.com/watch?v=l5QJ8EtilaY)**

Also available on our free online training ["Shopware 6 Backend Development"](https://academy.shopware.com/courses/shopware-6-backend-development-with-jisse-reitsma).
:::

---

---

## Redis
**Source:** [guides/plugins/plugins/redis.md](https://developer.shopware.com/docs/v6.6/guides/plugins/plugins/redis.md)  
# Redis

Starting with Shopware v6.6.8.0, Redis support has been improved, giving you more flexibility in how you use it in your projects and plugins.

## Accessing Redis connections

Once you've set up your Redis connections as explained in the  [Redis configuration](../../hosting/infrastructure/redis) guide, you can access them in your code using the following methods:

1. Inject `Shopware\Core\Framework\Adapter\Redis\RedisConnectionProvider` and retrieve connections by name:

   ```xml
   <service id="MyCustomService">
       <argument type="service" id="Shopware\Core\Framework\Adapter\Redis\RedisConnectionProvider" />
       <argument>%myservice.redis_connection_name%</argument>
   </service>
   ```

   ```php
   class MyCustomService
   { 
       public function __construct (
           private RedisConnectionProvider $redisConnectionProvider,
           string $connectionName,
       ) { }

       public function doSomething()
       {
           if ($this->redisConnectionProvider->hasConnection($this->connectionName)) {
               $connection = $this->redisConnectionProvider->getConnection($this->connectionName);
               // use connection
           }
       }
   }
   ```

2. Use `Shopware\Core\Framework\Adapter\Redis\RedisConnectionProvider` as factory to define custom services:

   ```xml
   <service id="my.custom.redis_connection" class="Redis">
       <factory service="Shopware\Core\Framework\Adapter\Redis\RedisConnectionProvider" method="getConnection" />
       <argument>%myservice.redis_connection_name%</argument>
   </service>

   <service id="MyCustomService">
       <argument type="service" id="my.custom.redis_connection" />
   </service>
   ```

   ```php
   class MyCustomService
   { 
       public function __construct (
           private object $redisConnection,
       ) { }

       public function doSomething()
       {
           // use connection
       }
   }
   ```

   This approach is especially useful when you want multiple services to share the same Redis connection.

3. Inject connection directly by name:

   ```xml
   <service id="MyCustomService">
       <argument type="service" id="shopware.redis.connection.connection_name" />
   </service>
   ```

   Be cautious with this approach! If you change the Redis connection names in your configuration, it will cause container build errors.

## Redis usage tips

### Connection types

Under the hood, connection service objects are created using the `\Symfony\Component\Cache\Adapter\RedisAdapter::createConnection` method.
Depending on the installed extensions/libraries and the provided DSN, this method may return instance of one of the following classes:
`\Redis|Relay|\RedisArray|\RedisCluster|\Predis\ClientInterface`

### Reusing connections

Connections are cached in a static variable and reused based on the provided DSN. If you use the same DSN for multiple connections, they will share the same connection object.
This means you need to be cautious when closing or modifying connection options, as it will affect all services using the same connection.

### Connection initialization

The moment actual connection is established depends on the usage model:

* When `RedisConnectionProvider::getConnection` is called.
* When the Redis connection service is requested from the container.
* When a service that depends on Redis connection is instantiated.

### Redis is optional

When developing a plugin, please keep in mind that Redis is an optional dependency in Shopware and might not be available in all installations.

---

---

