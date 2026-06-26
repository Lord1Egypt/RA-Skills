# INSTALLATION AND HOSTING

Compiled excerpts from the Shopware Developer Documentation snapshot. Prefer live docs at [developer.shopware.com](https://developer.shopware.com/) when in doubt.

---

## Deployment Helper
**Source:** [guides/hosting/installation-updates/deployments/deployment-helper.md](https://developer.shopware.com/docs/v6.6/guides/hosting/installation-updates/deployments/deployment-helper.md)  
# Deployment Helper

The Deployment Helper is a tool that unifies the steps executed after the Code has been uploaded to the server.
On a traditional deployment, you would run it after the files have been uploaded.
When using a Containerized environment, you would run Deployment Helper with the new source code and then switch over the traffic.

## Installing the Deployment Helper

The Deployment Helper is a composer package and can be installed via composer:

```bash
composer require shopware/deployment-helper
```

Then the helper can be executed via:

```bash
vendor/bin/shopware-deployment-helper run
```

## What does the Deployment Helper exactly do?

The Deployment Helper checks for you, if Shopware is installed and if not, it will install it for you.
It will also check if the database server is accessible, and if not, it will wait until it is.

Besides installing or updating Shopware, it also simplifies common tasks which normally are executed during the deployment like:

* Installing or updating the extensions (apps and plugins)
* Compiling the theme
* Run custom commands
* Run one time commands

## Configuration

The Deployment Helper can be configured via a `.shopware-project.yml` file in the root of your project.
The following configuration options are available:

```yaml
deployment:
  hooks:
    pre: |
      echo "Before deployment general"
    post: |
      echo "After deployment general"
    pre-install: |
      echo "Before running system:install"
    post-install: |
      echo "After running system:install"
    pre-update: |
      echo "Before running system:update"
    post-update: |
      echo "After running system:update"

  # Automatically installs and updates all extensions included in custom/plugins and custom/apps and composer
  extension-management:
    enabled: true

    # These extensions are not managed, you should use one-time-tasks to manage them
    exclude:
      - Name

    overrides:
      # the key is the extension name (app or plugin)
      MyPlugin:
        # Same as exclude
        state: ignore

      AnotherPlugin:
        # This plugin can be installed, but should be inactive
        state: inactive

      RemoveThisPlugin:
        # This plugin will be uninstalled if it is installed
        state: remove
        # should the extension data of an uninstalled extension be kept
        keepUserData: true

  one-time-tasks:
    - id: foo
      script: |
        # runs one time in deployment, then never again
        ./bin/console --version

  store:
    license-domain: 'example.com'
```

## Environment Variables

Additionally, you can configure the Shopware installation using the following environment variables:

* `INSTALL_LOCALE` - The locale to install Shopware with (default: `en-GB`)
* `INSTALL_CURRENCY` - The currency to install Shopware with (default: `EUR`)
* `INSTALL_ADMIN_USERNAME` - The username of the admin user (default: `admin`)
* `INSTALL_ADMIN_PASSWORD` - The password of the admin user (default: `shopware`)
* `SALES_CHANNEL_URL` - The URL of the Storefront sales channel (default: `http://localhost`)
* `SHOPWARE_DEPLOYMENT_TIMEOUT` - The timeout allowed for setup commands, that are executed (default: `300`)
* `SHOPWARE_STORE_ACCOUNT_EMAIL` - The email address of the Shopware account
* `SHOPWARE_STORE_ACCOUNT_PASSWORD` - The password of the Shopware account
* `SHOPWARE_STORE_LICENSE_DOMAIN` - The license domain of the Shopware Shop (default: license-domain value in YAML file)

## One Time Tasks

One time tasks are tasks that should be executed only once during the deployment, like a migration script.

You can check with `./vendor/bin/shopware-deployment-helper one-time-task:list` which tasks were executed and when.
To remove a task, use `./vendor/bin/shopware-deployment-helper one-time-task:unmark <id>`. This will cause the task to be executed again during the next update.
To manually mark a task as run you can use `./vendor/bin/shopware-deployment-helper one-time-task:mark <id>`.

## Fastly Integration

The Deployment Helper can also deploy Fastly VCL Snippets for you and keep them up to date. After installing the Deployment Helper, you can install the Fastly meta package:

```bash
composer require shopware/fastly-meta
```

After that, make sure that environment variable `FASTLY_API_KEY` and `FASTLY_SERVICE_ID` are set and the Fastly VCL Snippets will be deployed with the regular deployment process of the Deployment Helper.

The deployment helper has also two commands to manage the Fastly VCL Snippets:

* `./vendor/bin/shopware-deployment-helper fastly:snippet:list` - List all VCL snippets that are currently deployed
* `./vendor/bin/shopware-deployment-helper fastly:snippet:remove <name>` - Remove a VCL snippet by name

## Automatic Store Login

The Deployment Helper can automatically log in to the Shopware Store, so you can install Apps from the Store. For this the environment variables: `SHOPWARE_STORE_ACCOUNT_EMAIL` and `SHOPWARE_STORE_ACCOUNT_PASSWORD` need to be set, and a license domain needs to be configured in the `.shopware-project.yml` file.
The license domain can be set also by env variable `SHOPWARE_STORE_LICENSE_DOMAIN`, which will overwrite the value from the `.shopware-project.yml` file.

When you open the extension manager, you will see that you are not logged in. This is normal as the Deployment Helper does log you in only for system tasks like extension installation or updates. For the extension manager, every Administration user needs to log in manually.

## Removal of extensions

To find the name (for example `SwagPlatformDemoData`) of the extension you want to remove, use the `./bin/console plugin:list` command.

```shell
./bin/console plugin:list

Shopware Plugin Service
=======================

 ----------------------------- ------------------------------------------ ---------------------------------------------- --------- ----------------- ------------------- ----------- -------- ------------- ---------------------- 
  Plugin                        Label                                      Composer name                                  Version   Upgrade version   Author              Installed   Active   Upgradeable   Required by composer  
 ----------------------------- ------------------------------------------ ---------------------------------------------- --------- ----------------- ------------------- ----------- -------- ------------- ----------------------
  SwagPlatformDemoData          Shopware 6 Demo data                       swag/demo-data                                 2.0.1                       shopware AG         Yes         No       No            No 
 ----------------------------- ------------------------------------------ ---------------------------------------------- --------- ----------------- ------------------- ----------- -------- ------------- ----------------------
```

If you want to remove an extension, you need to do it in two steps:

1.) Set the extension to `remove` in the `.shopware-project.yml` file

```yaml
deployment:
  extension-management:
    enabled: true

    overrides:
      TheExtensionWeWantToGetRidOf:
        # This plugin will be uninstalled if it is installed
        state: remove
        # should the extension data of an uninstalled extension be kept
        keepUserData: true

```

and deploy the changes. The extension will be uninstalled and is inactive.

2.) Remove the extension from source code

After the deployment, you can remove the extension from the source code, remove the entry from the `.shopware-project.yml` file and deploy the changes again.

## Usage examples

### Container

In a Docker environment, you have a base image with a running PHP Webserver.
From that image you make a new image with your Shopware source code.
To prepare the Shopware source code, you can run [shopware-cli project ci](../../../../products/cli) to install the dependencies and build the assets.
On deployment, you spawn a second container or init a container, which runs the Deployment Helper.
The Deployment Helper sets up Shopware when it is not installed, installs the extensions and runs the one-time tasks.

### SFTP / Deployer

When using SFTP or Deployer, you clone the repository to the CI/CD server, run the [shopware-cli project ci](../../../../products/cli) command to install the dependencies and build the assets.
Then you upload the source code to the server and run the Deployment Helper on the server.
The Deployment Helper sets up Shopware when it is not installed, installs the extensions and runs the one-time tasks.

---

---

## Deployment with Deployer
**Source:** [guides/hosting/installation-updates/deployments/deployment-with-deployer.md](https://developer.shopware.com/docs/v6.6/guides/hosting/installation-updates/deployments/deployment-with-deployer.md)  
*(Body truncated in this bundle; follow the link for the rest.)*

# Deployment with Deployer

## Overview

Automated deployments shouldn't be a pain and have several advantages, like lower failure rates and reproducible builds. Also, they increase overall productivity because actual testing can get more attention.

This article explains the fundamental steps to deploy Shopware 6 to a certain infrastructure, focussing on continuous deployment using [GitLab CI](https://docs.gitlab.com/ee/ci/) or [GitHub Actions](https://github.com/features/actions) and [Deployer](https://deployer.org/) (a deployment tool written in PHP).

## Video

## Prerequisites

Please make sure you already have a working Shopware 6 instance running and that your repository is based on the [Symfony Flex template](../../../installation/template) because this article relies on some scripts to exist in your repository.

### Preparations before the first deployment

[Deployer](https://deployer.org/) has a default directory structure in which it organizes releases, shared files across releases (e.g., certificates, configuration, or media files) and the symlink to the current release.

The structure looks like this:

```text
├── .dep
├── current -> releases/1
├── releases
│   └── 1
└── shared
    ├── .env
    └── config
    └── ...
```

Suppose you haven't used such a structure yet, it is recommended to move the current document root contents to a different location because you will have to copy some existing files into the `shared` folder after your first deployment with [Deployer](https://deployer.org/).

For more information, refer to [Migrating existing instance to Deployer structure](deployment-with-deployer#migrating-existing-instance-to-deployer-structure).

### Webserver configuration

Ensure to set the document root of the domain to `/var/www/shopware/current/public`, assuming `/var/www/shopware` is the path you are uploading Shopware to, but this can, of course, differ. The most important part of this path is `current`, which is the symlink to the currently active release.

Because `current` is a symlink, please also make sure your web server is configured to resolve/follow symlinks correctly.

### Require Deployer and deployment-helper

Your project needs to have the following dependencies installed:

```bash
composer require deployer/deployer shopware/deployment-helper
```

## GitLab runner requirements

[GitLab pipelines](https://docs.gitlab.com/ee/ci/pipelines/) are processed by [runners](https://docs.gitlab.com/runner/). Once a pipeline job is created, GitLab notifies a registered runner, and the job will then be processed by that runner.

The [GitLab runner](https://docs.gitlab.com/runner/) must have the following packages installed:

* PHP (see supported versions in the [System Requirements](https://docs.shopware.com/en/shopware-6-en/first-steps/system-requirements#environment))
* [NodeJS](https://nodejs.org/en/)
* [Node Package Manager (npm)](https://www.npmjs.com/)
* OpenSSH

This example uses the docker image `shopware/shopware-cli:latest-php-8.3`. This image meets all requirements.

## Deployment steps

### 1. Cloning the repository

The very first step in the pipeline is cloning the repository into the runner's workspace. GitLab does that automatically for every started job.

### 2. Building the project

All the dependencies of your project must be installed. Shopware 6 uses [Composer](https://getcomposer.org/) for managing PHP dependencies and [Node Package Manager (NPM)](https://www.npmjs.com/) for frontend related dependencies.

We use Shopware CLI, which simplifies the installation of the dependencies and building the project assets to build a production-ready version of Shopware.

### 3. Transferring the workspace

For transferring the files to the target server, please configure at least one host in the [`deploy.php`](deployment-with-deployer#deploy-php):

```php
host('SSH-HOSTNAME')
    ->setLabels([
        'type' => 'web',
        'env'  => 'prod',
    ])
    ->setRemoteUser('www-data')
    ->set('deploy_path', '/var/www/shopware') // This is the path, where deployer will create its directory structure
    ->set('http_user', 'www-data') // Not needed, if the `user` is the same user, the webserver is running with 
    ->set('writable_mode', 'chmod');
```

This step is defined in the `deploy:update_code` job in the [`deploy.php`](deployment-with-deployer#deploy-php):

```php
task('deploy:update_code')->setCallback(static function () {
    upload('.', '{{release_path}}', [
        'options' => [
            '--exclude=.git',
            '--exclude=deploy.php',
            '--exclude=node_modules',
        ],
    ]);
});
```

### 4. Applying migrations / install or update plugins

The migrations need to be applied on the target server.

::: danger
If you are deploying to a cluster with multiple web servers, please make sure to run the migrations only on one of the servers.
:::

This step is defined in the `sw:deployment:helper` job in the [`deploy.php`](deployment-with-deployer#deploy-php), which is part of the `sw:deploy` task group:

```php
task('sw:deployment:helper', static function() {
    run('cd {{release_path}} && vendor/bin/shopware-deployment-helper run');
});
```

### 5. Creating the `install.lock` file

Before putting the new version live, ensure to create an empty file `install.lock` in the root of the build workspace. Otherwise, Shopware will redirect every request to the Shopware installer because it assumes that Shopware isn't installed yet.

This task is defined in the `sw:touch_install_lock` job in the [`deploy.php`](deployment-with-deployer#deploy-php), which is part of the `sw:deploy` task group:

```php
task('sw:touch_install_lock', static function () {
    run('cd {{release_path}} && touch install.lock');
});
```

### 6. Running System Checks (Optional)

Before putting the new version live, it is recommended to run the system checks to ensure that the new version is working correctly.

```php
task('sw:health_checks', static function () {
    run('cd {{release_path}} && bin/console system:check --context=pre_rollout');
});
```

> Before incorporating this step into your deployment process, make sure that you are well familiar with the [System Checks Concepts](../../../../concepts/framework/system-check.md) and how to use and interpret the results [Custom usage](../../../../guides/plugins/plugins/framework/system-check/index.md), and the command [error codes](../../../../guides/plugins/plugins/framework/system-check/index.md#triggering-system-checks).

### 7. Switching the document root

After all the steps are done, Deployer will switch the symlinks destination to the new release.

This task is defined in the `deploy:symlink` default job in the [`deploy.php`](deployment-with-deployer#deploy-php).

## Deployer output

This is the output of `dep deploy env=prod`:

```text
$ dep deploy env=prod               

✔ Executing task deploy:prepare
✔ Executing task deploy:lock
✔ Executing task deploy:release
✔ Executing task deploy:update_code
✔ Executing task deploy:shared
✔ Executing task sw:touch_install_lock
✔ Executing task sw:deployment:helper
✔ Executing task deploy:writable
✔ Executing task deploy:clear_paths
✔ Executing task deploy:symlink
✔ Executing task deploy:unlock
✔ Executing task cleanup
Successfully deployed!
```

## Migrating existing instance to Deployer structure

After the very first deployment with Deployer, you have to copy some files and directories from your existing Shopware instance into the directory structure, that was created by Deployer.

Let's agree on the following two paths for the examples:

1. You have copied your existing Shopware instance to `/var/www/shopware_backup`.
2. You have set the `deploy_path` in the [`deploy.php`](deployment-with-deployer#deploy-php) to `/var/www/shopware`.

Now, look at the `shared_files` and `shared_dirs` configurations in the [`deploy.php`](deployment-with-deployer#deploy-php). Simply copy all the paths into `/var/www/shopware/shared`. For the configuration of the `deploy.php` the commands would be the following:

```bash
cp /var/www/shopware_backup/.env.local /var/www/shopware/shared/.env.local
cp -R /var/www/shopware_backup/custom/plugins /var/www/shopware/shared/custom
cp -R /var/www/shopware_backup/config/jwt /var/www/shopware/shared/config
cp -R /var/www/shopware_backup/config/packages /var/www/shopware/shared/config
cp -R /var/www/shopware_backup/files /var/www/shopware/shared
cp -R /var/www/shopware_backup/var/log /var/www/shopware/shared/var
cp -R /var/www/shopware_backup/public/media /var/www/shopware/shared/public
cp -R /var/www/shopware_backup/public/thumbnail /var/www/shopware/shared/public
cp -R /var/www/shopware_backup/public/sitemap /var/www/shopware/shared/public
```

## Generating a new SSH key

To deploy your code to a server, you need to have an SSH key. If you don't have one yet, you can generate one with the following command:

```bash
ssh-keygen -t ed25519
```

It will be used in the above-mentioned GitLab CI/CD pipeline or GitHub Actions.

## Sources

Have a look at the following files. All steps are provided with helpful comments.

### .gitlab-ci.yml

```yaml
# This file defines the GitLab CI/CD pipeline.
# For more information, please visit the GitLab CI/CD docs: https://docs.gitlab.com/ee/ci/README.html
variables:
    GIT_STRATEGY: clone

# This variable holds all commands that are needed to be able to connect to the target server via SSH.
# For this you need to define two variables in the GitLab CI/CD variables:
#   - SSH_PRIVATE_KEY: The contents of the SSH private key file. The public key must be authorized on the target server.
#   - DEPLOYMENT_SERVER: Just the hostname of the target server (e.g. shopware.com, don't include schema or paths)
.configureSSHAgent: &configureSSHAgent |-
    eval $(ssh-agent -s)
    echo "$SSH_PRIVATE_KEY" | tr -d '\r' | ssh-add -
    mkdir -p ~/.ssh
    ssh-keyscan $DEPLOYMENT_SERVER >> ~/.ssh/known_hosts
    chmod 700 ~/.ssh

Deploy:
    stage: deploy
    # Tags are useful to only use runners that are safe or meet specific requirements
    image:
        name: shopware/shopware-cli:latest
        entrypoint: [ "/bin/sh", "-c" ]
    before_script:
        # First, we need to execute all commands that are defined in the `configureSSHAgent` variable.
        - *configureSSHAgent
    script:
        # This command installs all dependencies and builds the project.
        - shopware-cli project ci .
        # This command starts the workflow that is defined in the `deploy` task in the `deploy.php`.
        # `production` is the stage that was defined in the `host` in the `deploy.php`
        - vendor/bin/dep deploy
```

### .github/workflows/deploy.yml

```yaml
name: Deployment
on:
  push:
    branches: main

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Setup PHP
        uses: shivammathur/setup-php@v2
        with:
          php-version: '8.3'

      - name: Install Shopware CLI
        uses: shopware/shopware-cli-action@v1

      - name: Build
        run: shopware-cli project ci .

      - name: Deploy
        uses: deployphp/action@v1
        with:
          dep: deploy
          private-key: ${{ secrets.SSH_PRIVATE_KEY }}
```

### deploy.php

```php
<?php

namespace Deployer;

require_once 'recipe/common.php';
require_once 'contrib/cachetool.php';

set('bin/console', '{{bin/php}} {{release_or_current_path}}/bin/console');

set('cachetool', '/run/php/php-fpm.sock');
set('application', 'Shopware 6');
set('allow_anonymous_stats', false);
set('default_timeout', 3600); // Increase when tasks take longer than that.

// Hosts

host('SSH-HOSTNAME')
    ->setLabels([
        'type' => 'web',
        'env'  => 'production',
    ])
    ->setRemoteUser('www-data')
    ->set('deploy_path', '/var/www/shopware')
    ->set('http_user', 'www-data') // Not needed, if the `user` is the same user, the webserver is running with
    ->set('writable_mo

… **Truncated.** Full document: https://developer.shopware.com/docs/v6.6/guides/hosting/installation-updates/deployments/deployment-with-deployer.md


---

## Docker Image
**Source:** [guides/hosting/installation-updates/docker.md](https://developer.shopware.com/docs/v6.6/guides/hosting/installation-updates/docker.md)  
*(Body truncated in this bundle; follow the link for the rest.)*

# Docker Image

Shopware provides a Docker image to run Shopware 6 in a containerized environment for production intent. The Docker image is based on the official PHP image and includes the required PHP extensions and configurations to run Shopware 6. But it does not contain Shopware itself.
It's intended to be used together with your existing Shopware project, copy the project into the image, build it, and run it.

If you don't have yet a Shopware project, you can create a new one with:

::: info
You can create a Project with a specific Shopware version by specifying the version like: `composer create-project shopware/production:6.6.7.0 <folder>`
:::

```bash
composer create-project shopware/production <folder>
cd <folder>
composer require shopware/docker
```

The typical Dockerfile in your project would look like this:

::: info
You may want to pin the Docker image to a specific sha256 digest to ensure you always use the same image. See [Best Practices](https://docs.docker.com/build/building/best-practices/#pin-base-image-versions) for more information.
:::

```dockerfile
#syntax=docker/dockerfile:1.4

ARG PHP_VERSION=8.3
FROM ghcr.io/shopware/docker-base:$PHP_VERSION-caddy AS base-image
FROM shopware/shopware-cli:latest-php-$PHP_VERSION AS shopware-cli

FROM shopware-cli AS build

ADD . /src
WORKDIR /src

RUN --mount=type=secret,id=packages_token,env=SHOPWARE_PACKAGES_TOKEN \
    --mount=type=secret,id=composer_auth,dst=/src/auth.json \
    --mount=type=cache,target=/root/.composer \
    --mount=type=cache,target=/root/.npm \
    /usr/local/bin/entrypoint.sh shopware-cli project ci /src

FROM base-image AS final

COPY --from=build --chown=82 --link /src /var/www/html
```

The Dockerfile uses the `shopware-cli` image to build the project and then copies the built project into the `base-image` image. The `base-image` is the Shopware Docker image.

::: info
Instead of copying the Dockerfile to your project, rather run `composer req shopware/docker` to add the Dockerfile to your project. This keeps the Dockerfile up-to-date with the latest changes using Symfony Flex recipes.
:::

## Available Tags / Versioning

::: info
We recommend to use FrankenPHP over Caddy or Nginx, as it does automatic resource allocation and requires just one process to run PHP, which is better suited for containerized environments.
:::

The Docker image is versioned by the PHP Version and the PHP Patch version. The Docker Image is updated daily and contains the latest security patches.

The following tags are available with Caddy:

* `shopware/docker-base:8.3` - PHP 8.3 with Caddy
* `shopware/docker-base:8.3-caddy` - PHP 8.3 with Caddy (same as above, but more explicit)
* `shopware/docker-base:8.3.12-caddy` - PHP 8.3.12 with Caddy (same as above, but much more explicit)
* `shopware/docker-base:8.3-caddy-otel` - PHP 8.3 with Caddy and OpenTelemetry

The following tags are available with FrankenPHP:

* `shopware/docker-base:8.3-frankenphp` - PHP 8.3 with FrankenPHP
* `shopware/docker-base:8.3.12-frankenphp` - PHP 8.3.12 with FrankenPHP (same as above, but much more explicit)
* `shopware/docker-base:8.3-frankenphp-otel` - PHP 8.3 with FrankenPHP and OpenTelemetry
* `shopware/docker-base:8.3.12-frankenphp-otel` - PHP 8.3.12 with FrankenPHP and OpenTelemetry (same as above, but much more explicit)

We also have Nginx images available:

* `shopware/docker-base:8.3-nginx` - PHP 8.3 with Nginx (same as above, but more explicit)
* `shopware/docker-base:8.3.12-nginx` - PHP 8.3.12 with Nginx (same as above, but much more explicit)
* `shopware/docker-base:8.3-nginx-otel` - PHP 8.3 with Nginx and OpenTelemetry

Additionally we have also FPM only images available:

* `shopware/docker-base:8.3-fpm` - PHP 8.3 with FPM
* `shopware/docker-base:8.3.12-fpm` - PHP 8.3.12 with FPM (same as above, but much more explicit)
* `shopware/docker-base:8.3-fpm-otel` - PHP 8.3 with FPM and OpenTelemetry
* `shopware/docker-base:8.3.12-fpm-otel` - PHP 8.3.12 with FPM and OpenTelemetry (same as above, but much more explicit)

The images are available at Docker Hub and GitHub Container Registry (ghcr.io) with the same names and tags.

## Default installed PHP Extensions

The Docker image contains the following PHP extensions: `bcmath`, `gd`, `intl`, `mysqli`, `pdo_mysql`, `pcntl`, `sockets`, `bz2`, `gmp`, `soap`, `zip`, `ffi`, `opcache`, `redis`, `apcu`, `amqp` and `zstd`

## Environment Variables

| Variable                              | Default Value | Description                                                                              |
|---------------------------------------|---------------|------------------------------------------------------------------------------------------|
| `PHP_SESSION_COOKIE_LIFETIME`         | 0             | [See PHP FPM documentation](https://www.php.net/manual/en/session.configuration.php)     |
| `PHP_SESSION_GC_MAXLIFETIME`          | 1440          | [See PHP FPM documentation](https://www.php.net/manual/en/session.configuration.php)     |
| `PHP_SESSION_HANDLER`                 | files         | Set to `redis` for redis session                                                         |
| `PHP_SESSION_SAVE_PATH`               | (empty)       | Set to `tcp://redis:6379` for redis session                                              |
| `PHP_MAX_UPLOAD_SIZE`                 | 128m          | See PHP documentation                                                                    |
| `PHP_MAX_EXECUTION_TIME`              | 300           | See PHP documentation                                                                    |
| `PHP_MEMORY_LIMIT`                    | 512m          | See PHP documentation                                                                    |
| `PHP_ERROR_REPORTING`                 | E\_ALL         | See PHP documentation                                                                    |
| `PHP_DISPLAY_ERRORS`                  | 0             | See PHP documentation                                                                    |
| `PHP_OPCACHE_ENABLE_CLI`              | 1             | See PHP documentation                                                                    |
| `PHP_OPCACHE_FILE_OVERRIDE`           | 1             | See PHP documentation                                                                    |
| `PHP_OPCACHE_VALIDATE_TIMESTAMPS`     | 1             | See PHP documentation                                                                    |
| `PHP_OPCACHE_INTERNED_STRINGS_BUFFER` | 20            | See PHP documentation                                                                    |
| `PHP_OPCACHE_MAX_ACCELERATED_FILES`   | 10000         | See PHP documentation                                                                    |
| `PHP_OPCACHE_MEMORY_CONSUMPTION`      | 128           | See PHP documentation                                                                    |
| `PHP_OPCACHE_FILE_CACHE`              |               | See PHP documentation                                                                    |
| `PHP_OPCACHE_FILE_CACHE_ONLY`         | 0             | See PHP documentation                                                                    |
| `PHP_REALPATH_CACHE_TTL`              | 3600          | See PHP documentation                                                                    |
| `PHP_REALPATH_CACHE_SIZE`             | 4096k         | See PHP documentation                                                                    |
| `FPM_PM`                              | dynamic       | [See PHP FPM documentation](https://www.php.net/manual/en/install.fpm.configuration.php) |
| `FPM_PM_MAX_CHILDREN`                 | 5             | [See PHP FPM documentation](https://www.php.net/manual/en/install.fpm.configuration.php) |
| `FPM_PM_START_SERVERS`                | 2             | [See PHP FPM documentation](https://www.php.net/manual/en/install.fpm.configuration.php) |
| `FPM_PM_MIN_SPARE_SERVERS`            | 1             | [See PHP FPM documentation](https://www.php.net/manual/en/install.fpm.configuration.php) |
| `FPM_PM_MAX_SPARE_SERVERS`            | 3             | [See PHP FPM documentation](https://www.php.net/manual/en/install.fpm.configuration.php) |

This table contains only the environment variables that are specific to the Shopware Docker image. You can see all Shopware specific environment variables [here](../configurations/shopware/environment-variables.md)

Additionally, you can use also the [Deployment Helper environment variables](./deployments/deployment-helper.md#environment-variables) to specify default administration credentials, locale, currency, and sales channel URL.

## Possible Mounts

::: info
Our recommendation is to store all files in an external storage provider to not mount any volumes. Refer to [official Shopware docs for setup](https://developer.shopware.com/docs/guides/hosting/infrastructure/filesystem).
:::

In a very basic setup when all files are stored locally you need 5 volumes:

| Usage                  | Path                             |
|------------------------|----------------------------------|
| invoices/private files | `/var/www/html/files`            |
| theme files            | `/var/www/html/public/theme`     |
| images                 | `/var/www/html/public/media`     |
| image thumbnails       | `/var/www/html/public/thumbnail` |
| generated sitemap      | `/var/www/html/public/sitemap`   |

Shopware logs by default to `var/log`, but when `shopware/docker` Composer package is installed, we change it to stdout. This means you can use `docker logs` to see the logs or use logging driver to forward the logs to a logging service.

## Ideal Setup

The ideal setup requires an external storage provider like S3. In that way you don't need any mounts and can scale the instances without any problems.

Additionally, Redis is required for the session storage and the cache, so the Browser sessions are shared between all instances and cache invalidations are happening on all instances.

## Typical Setup

The docker image starts in entry point PHP-FPM / Caddy. So you will need to start a extra container to run maintenance tasks like to install Shopware, install plugins, or run the update. This can be done by installing the [Deployment Helper](./deployments/deployment-helper.md) and creating one container and running as entry point `/setup`

Here we have an example of a `compose.yaml`, how the services could look like:

::: info

This is just an example compose file to demonstrate how the services could look like. It's not a ready to use compose file. You need to adjust it to your needs.

:::

```yaml
x-environment: &shopware
  image: local
  build:
    context: .
  environment:
    DATABASE_URL: 'mysql://shopware:shopware@database/shopware'
    APP_URL: 'http://localhost:8000'
  volumes:
    - files:/var/www/html/files
    - theme:/var/www/html/public/theme
    - media:/var/www/html/public/media
    - thumbnail:/var/www/html/public/thumbnail
    - sitemap:/var/www/html/public/sitemap

services:
    database:
        image: mariadb:11.4

    init:
        <<: *shopware
        entrypoint: /setup
        depends_on:
            db:
                condition: service_started
            init-perm:
                condition: service_completed_successfully
    web:
        <<: *shopware
        depends_on:
            init:
                condition: service_completed_successfully
        ports:
            - 8000:8000

    worker:
        <<: *shopware
        depends_on:
            init:
                condition: service_completed_successfully
        entrypoint: [ "php", "bin/console", "messenger:consume", "async", "low_priority", "--time-limit=300", "--memory-limit=512M" ]
        deploy:
            replicas: 3

    scheduler:
        <<: *shopware
        depends_on:
            init:
                condition: service_completed_successfully
        ent

… **Truncated.** Full document: https://developer.shopware.com/docs/v6.6/guides/hosting/installation-updates/docker.md


---

## Extension Management
**Source:** [guides/hosting/installation-updates/extension-managment.md](https://developer.shopware.com/docs/v6.6/guides/hosting/installation-updates/extension-managment.md)  
# Extension Management

Normally all extensions installed by the Administration will be stored inside `custom/plugins` or `custom/apps`. When you want to update extensions, you have to re-upload the zip file or download the extension from the store using the Extension manager in the administration.

This way of extension management brings many problems:

* It is hard to keep track of which extensions are installed and in which version
* The extensions can be modified live in the Administration without version control
* Extension updates must be downloaded manually for each extension and installed
* Extension updates in the Administration can't be done together with Shopware updates
* Composer class loader cannot be optimized because we need to dynamically look up into `custom/plugins`

## Installing extensions with Composer

To solve these problems, it is recommended to install all extensions (plugins and apps) with Composer. This way, you can manage all extensions in one place and update them along with Shopware. To get started with Composer, first, you need to authorize your local project with the Shopware Composer Registry. Below are the steps:

* Login to [account.shopware.com](https://account.shopware.com) and go to your Shop (in Merchant or Account area)
* Click on one extension
* Click the button "Install via Composer"
* Generate a token and save it

Now you can add the Shopware Composer Registry to your project:

```bash
composer config repositories.shopware-packages '{"type": "composer", "url": "https://packages.shopware.com"}'

composer config bearer.packages.shopware.com <your-token>
```

After that, you should have a newly created file `auth.json`, in your project root. This file contains your token and is used by Composer to authenticate against the Shopware Composer Registry.

::: info
The `auth.json` should not be committed to the repository and should be ignored by default with the `.gitignore` file.
:::

Now you can install extensions with Composer:

```bash
composer require store.shopware.com/{extension-name}
```

This downloads and extracts the extension package into the `vendor` directory. To install and activate the extension in Shopware, execute the following console command:

```bash
bin/console plugin:install --activate <extension-name>
```

You can also find the Composer package name when you click "Install via Composer" in the Shopware Account.

## Migrating already installed extensions to Composer

If you already have extensions installed in your project, you can migrate them to Composer. First, you should install the extension with Composer:

```bash
composer require store.shopware.com/{extension-name}
```

And then delete the source code from `custom/plugins/{extension-name}` or `custom/apps/{extension-name}`.

After that, you must run the below command for Shopware to detect the installed extensions per Composer.

```bash
bin/console plugin:refresh
```

## Enabling Composer class map authoritative

When all extensions are installed with Composer, you can enable the Composer class map authoritative. This will improve the performance of the class loader and is recommended for production environments.
[The class map authoritative, disables the live class lookup when it cannot find the class in a dumped class map.](https://getcomposer.org/doc/articles/autoloader-optimization.md#optimization-level-2-a-authoritative-class-maps)

```diff
{
    "require": {
        "shopware/core": "....",
        // .....
    },
    "config": {
        "optimize-autoloader": true,
+       "classmap-authoritative": true
    }
}
```

And run the below command to re-generate the class loader.

```bash
composer dump-autoload
```

## Configuring Extension Manager to read-only in Admin

Since Shopware 6.6.4.0, it has been possible to disable the installation of extensions in the Administration. This is useful when you have a cluster environment or want to use proper deployments to roll out code changes.

To disable the installation of extensions in the Administration, you can set the following configuration in your `config/packages/z-shopware.yaml` file:

```yaml
shopware:
    deployment:
        runtime_extension_management: false
```

Next clear the cache once. After doing this, the Extension Manager in the Administration will become read-only, allowing access only to the extension configuration. Additionally, the First Run Wizard will no longer download extensions such as PayPal or the Shopware Store.

---

---

## Performing Shopware Updates
**Source:** [guides/hosting/installation-updates/performing-updates.md](https://developer.shopware.com/docs/v6.6/guides/hosting/installation-updates/performing-updates.md)  
# Performing Shopware Updates

## When to update

Shopware releases updates every month. It's not necessary to update every month, but you should always install the latest security patches through the [Security Plugin](https://store.shopware.com/en/swag136939272659f/shopware-6-security-plugin.html) or update Shopware itself to the latest version. To check if your Shopware version still gets security updates, you can check the [Shopware Release Cycle](https://developer.shopware.com/release-notes/). But generally speaking, the maintenance effort is the same when you wait a long period or update more regularly. So our recommendation would be to update from every major version to the next major version, and stay on a minor version for a longer period of time, if you don't need any new features or encounter issues with the used version.

## Preparations

Before any update, check if the installed extensions are compatible with the new version. The easiest way to check this is to open the Update Manager in the Administration. It lists all installed extensions and their compatibility with the new version. If an extension is not compatible, you should check with the extension developer if an update is available.

::: info
If you can't see the info in the admin, please check if [auto\_update](../installation-updates/cluster-setup#disable-auto-update) is set to false.
:::

The next step is to check when the update should be performed. You should always perform updates in a maintenance window to avoid any issues with customers. If you are using a staging environment, you can perform the update there first and then apply it to the production environment.

Before doing the actual update, you should create a backup of your database and files. This is important to ensure that you can restore your Shopware installation in case something goes wrong during the update process.

::: info
If blue-green deployment is enabled, you can rollback to the previous version without restoring the database backup. This is only recommended when you **only updated** Shopware and not any extensions together with it.
:::

Before you start the update process, you should also make sure that you have set the Sales Channels into maintenance mode. This can be done using the Administration or with `bin/console sales-channel:maintenance:enable --all` in the terminal.

### Use Composer to manage all extensions

Managing all extensions through Composer is the best way to ensure that they are compatible with the new version. It simplifies the update process as Composer automatically resolves the correct versions of the extensions.

### Use Twig Block Versioning

Twig Block Versioning is a [PHPStorm Plugin](https://plugins.jetbrains.com/plugin/17632-shopware-6-toolbox) only feature. Twig Block Versioning is a feature that allows versioning of the overwritten blocks in your theme. This helps you to show which blocks after a Shopware Update maybe have to be changed. It's recommended to enable "Shopware versioning block comment is missing" in the inspection settings. This will show you a warning if a block is missing the versioning comment. For more information, check the [Twig Block Versioning blog post](https://www.shopware.com/en/news/twig-block-versioning-in-shopware-phpstorm-plugin/).

### Use existing tools to automatically upgrade your extensions

There are tools like [Rector](https://github.com/FriendsOfShopware/shopware-rector) for PHP and [Codemods](https://github.com/shopware/shopware/blob/trunk/src/Administration/Resources/app/administration/code-mods.js) for Administration JavaScript which can help you to automatically upgrade your extensions. Both tools do the most repeating tasks for you, but you still have to check the results and adapt your code if necessary. It's recommended to use these tools, as they save you a lot of time. Make sure that your code-base is versioned with Git, so you can easily rollback the changes if necessary.

## Update types

There are two Shopware update types:

* **Minor/Patch updates**: These are updates that only contain new features, bug fixes and security patches. They are released every month for the active supported versions.
* **Major updates**: These updates are intended to clean up the codebase and introduce breaking changes. They are released once a year.

### Minor/Patch updates

Minor and patch updates are non-breaking updates. They don't require special attention if your extensions are not using internal/experimental APIs. You can find the Backwards Compatibility Promise [here](../../../resources/guidelines/code/backward-compatibility.md). Of course, there can be unexpected issues, so we recommend to test the update in a staging environment before applying it to your production environment and [reporting](https://github.com/shopware/shopware/issues) any issues you encounter.

### Major updates

Major updates are breaking updates. They require special attention, as extensions, themes or system configurations might not be compatible with the new version.

First, you should check that all extensions obtained from Shopware Store are compatible with the next version. You can find the compatibility information in the Update Manager in the Administration. Generally speaking, it's recommended to update all extensions before updating Shopware itself to their latest versions, to ensure a smooth transition. After updating Shopware, you should update all extensions again to ensure that you are using the latest versions to the new Shopware version.

For the Hosting environment, it makes sense to update the PHP version to the minimum required version for the new Shopware version before updating Shopware itself. Shopware versions always support an overlapping PHP version, so you can update the PHP version before updating Shopware itself. You can find the minimum required PHP version in the [System Requirements](../../installation/requirements.md).

For customizations, you should check the [UPGRADE.md](https://github.com/search?q=repo%3Ashopware%2Fshopware+UPGRADE-6+language%3AMarkdown+NOT+path%3A%2F%5Eadr%5C%2F%2F+NOT+path%3A%2F%5Echangelog%5C%2F%2F\&type=code\&l=Markdown), it contains all breaking changes and migration instructions. Most of the time, it's easier to update to the latest version in a local environment and take a look at what is not working anymore.

## Final Steps

Before you remove the maintenance mode, it is recommended to check the following:

* **Check the Administration**: Make sure the administration is working correctly.
* **Check the Storefront / Sales Channels**: Make sure your main processes are working correctly (e.g., adding products to the cart, checkout, etc.).
* **Check the Extensions**: Make sure that all extensions are working correctly.
* **Check the Performance**: Make sure that there is no major performance degradation.
* **Check the Logs**: Check your error logs for any issues.

After you have checked everything, you can disable the maintenance mode with `bin/console sales-channel:maintenance:disable --all`.

---

---

## Performance
**Source:** [guides/hosting/performance.md](https://developer.shopware.com/docs/v6.6/guides/hosting/performance.md)  
# Performance

By fine-tuning cache usage, optimizing session and storage management, and employing efficient locking mechanisms, you can significantly improve the overall performance of your online store. Optimizing hosting performance involves considering these factors and implementing appropriate strategies to enhance the speed, scalability, and reliability of your Shopware store.

---

---

## Cache
**Source:** [guides/hosting/performance/caches.md](https://developer.shopware.com/docs/v6.6/guides/hosting/performance/caches.md)  
# Cache

There are several caches in Shopware that can be used to optimize performance. This page gives a brief overview and shows how to configure them.

## Overview

The HTTP Cache is a *must-have* for every production system. With an enabled cache, the performance of the shop can be greatly increased.

### How to configure the HTTP cache

The HTTP cache configuration takes place completely in the `.env.local` file. The following configurations are available here:

| Name                          | Description                    |
|:------------------------------|:-------------------------------|
| `SHOPWARE_HTTP_CACHE_ENABLED` | Enables the HTTP cache         |
| `SHOPWARE_HTTP_DEFAULT_TTL`   | Defines the default cache time |

The storage used for HTTP Cache is always the [App Cache](#app-cache), see below how to configure it. If you want to move this out of the application cache, you should use an external reverse proxy cache like [Varnish](https://varnish-cache.org/) or [Fastly](https://www.fastly.com/). For more [see here](../infrastructure//reverse-http-cache.md).

## How to change the cache storage

The standard Shopware HTTP cache can be exchanged or reconfigured in several ways. The standard cache comes with an `adapter.filesystem`. This is a file-based cache that stores the cache in the `var/cache` directory. This allows Shopware to work out of the box on a single server without any additional configuration. However, this may not be the best solution for a production system, especially if you are using a load balancer or multiple servers. In this case, you should use a shared cache like [Redis](https://redis.io/).

This is a Symfony cache pool configuration and therefore supports all adapters from the [Symfony FrameworkBundle](https://symfony.com/doc/current/cache.html#configuring-cache-with-frameworkbundle).

### Using Redis

Redis is a very fast in-memory key-value store. It is a good choice for caching data that is frequently accessed and does not need to be persisted. Redis can be used as a cache adapter in Shopware. As the cached information is ephemeral and can be recreated, it is not necessary to configure Redis to store the data on disk. For maximum performance, you can configure Redis to use no persistence. Refer to the [Redis docs](https://redis.io/docs/latest/operate/oss_and_stack/management/persistence/) for details.
As key eviction policy, you should use `volatile-lru`. This policy only automatically deletes expired data, as the application explicitly manages the TTL for each cache item. For a detailed overview of Redis key eviction policies, see the [Redis docs](https://redis.io/docs/latest/develop/reference/eviction/).

For `cache.adapter.redis_tag_aware` minimum Shopware 6.5.8.3 is required. Otherwise use `cache.adapter.redis`.

```yaml
# config/packages/cache.yaml
framework:
  cache:
    app: cache.adapter.redis_tag_aware
    system: cache.adapter.redis_tag_aware
    default_redis_provider: redis://localhost
```

Make sure that you have installed the PHP Redis extension before applying this configuration.

The Redis URL can have various formats. The following are all valid:

```text
# With explicit port
redis://localhost:6379

# With authentication
redis://auth@localhost:6379

# With database
redis://localhost:6379/1

# With options
redis://localhost:6379?timeout=1

# With unix socket

redis:///var/run/redis.sock

# With unix socket and authentication
redis://auth@/var/run/redis.sock
```

For more information or other adapters checkout [Symfony FrameworkBundle](https://symfony.com/doc/current/cache.html#configuring-cache-with-frameworkbundle) documentation.

---

---

## Cart Storage
**Source:** [guides/hosting/performance/cart-storage.md](https://developer.shopware.com/docs/v6.6/guides/hosting/performance/cart-storage.md)  
# Cart Storage

By default, shopware stores the cart in the database. This can be a performance bottleneck in scenarios where high throughput is required (e.g., thousands of orders per minute), especially if a DB cluster with a read/write-split is used.
Additionally, as the content in that table can change quite quickly, it can lead to an explosion of the databases `binlog` file.

Redis is better suited in high-throughput scenarios, therefore you should use Redis as storage for the cart in such scenarios.

## Using Redis as storage

To use Redis, create a `config/packages/shopware.yml` file with the following content:

```yaml
shopware:
  cart:
    redis_url: 'redis://host:port/dbindex?persistent=1'
```

```yaml
shopware:
    redis:
        connections:
            persistent:
                dsn: 'redis://host:port/dbindex?persistent=1'
    cart:
        storage:
            type: 'redis'
            config:
                 connection: 'persistent'
```

## Migrating between storages

You can migrate the current carts from the DB to Redis by running the following CLI command:

```shell
bin/console cart:migrate {fromStorage} {redisUrl?}
```

::: info
Providing the redis URL is optional. If not provided, the value from the configuration will be used. If it is not configured in the yaml file, you need to provide the URL.
:::

For example, if you want to migrate from the default `SQL` storage to the high-performing `Redis` storage, the command is:

```shell
bin/console cart:migrate sql
```

## Redis configuration

As the information stored here is durable and should be persistent, even in the case of a Redis restart, it is recommended to configure the used Redis instance that it will not just keep the data in memory, but also store it on the disk. This can be done by using snapshots (RDB) and Append Only Files (AOF), refer to the [Redis docs](https://redis.io/docs/latest/operate/oss_and_stack/management/persistence/) for details.

As key eviction policy you should use `volatile-lru`, which only automatically deletes carts that are expired, as otherwise you might risk of losing data. For a detailed overview of Redis key eviction policies see the [Redis docs](https://redis.io/docs/latest/develop/reference/eviction/).

---

---

## Custom cache invalidation
**Source:** [guides/hosting/performance/custom-cache-invalidation.md](https://developer.shopware.com/docs/v6.6/guides/hosting/performance/custom-cache-invalidation.md)  
# Custom cache invalidation

The current cache system of Shopware is based on a multi-layer system, in which the individual layers build on each other and whose tags are passed on to the upper layer for later invalidation.

Thus, an HTTP cache entry for a product detail page is built with all cache tags that are loaded or set during the rendering of the page for the individual routes or other cache entries in the system.

These tags are determined by the Shopware core system when writing data via API and invalidated via the configured cache pool.

In the current state, almost all invalidations happen in class `Shopware\Core\Framework\Adapter\Cache\CacheInvalidationSubscriber`. This is an event listener which listens for various events in the system and determines the corresponding cache tags and sends them via `Shopware\Core\Framework\Adapter\Cache\CacheInvalidator` to the cache pool for invalidation.

However, currently, the subscriber adheres to a highly precise invalidation concept, where any data written to the product results in the invalidation of cache tags for that specific product, even if the data is not utilized in the corresponding pages. This approach is not ideal for Shopware, being a standard product, as it becomes challenging to determine precisely when and which cache entries should be deleted. Moreover, due to project-specific variations, it is not feasible to generalize the process.

Therefore, we have solved all configurations via the service definition of this subscriber, so that all events, on which the subscriber listens, can be manipulated via compiler passes.

```xml
// src/Core/Framework/DependencyInjection/cache.xml
<service id="Shopware\Core\Framework\Adapter\Cache\CacheInvalidationSubscriber">
    <tag name="kernel.event_listener" event="Shopware\Core\Content\Category\Event\CategoryIndexerEvent" method="invalidateCategoryRouteByCategoryIds" priority="2000" />

    <tag name="kernel.event_listener" event="Shopware\Core\Content\Category\Event\CategoryIndexerEvent" method="invalidateListingRouteByCategoryIds" priority="2001" />

    <tag name="kernel.event_listener" event="Shopware\Core\Content\LandingPage\Event\LandingPageIndexerEvent" method="invalidateIndexedLandingPages" priority="2000" />
    
    <!-- ... -->
</service>
```

For example, if you want to disable all cache invalidation in a project, you can simply remove the `kernel.event_listener` tag of the service definition via compiler pass and implement your own cache invalidation.

```php
<?php

namespace MyProject;

use Shopware\Core\Content\Product\Events\ProductIndexerEvent;
use Shopware\Core\Content\Product\Events\ProductNoLongerAvailableEvent;
use Shopware\Core\Framework\DependencyInjection\CompilerPass\RemoveEventListener;
use Shopware\Core\Framework\Adapter\Cache\CacheInvalidationSubscriber;

class TweakCacheInvalidation implements CompilerPassInterface
{
    public function process(ContainerBuilder $container): void
    {
        $container
            ->getDefinition(CacheInvalidationSubscriber::class)
            ->clearTag('kernel.event_listener')
    }

}
```

However, suppose only certain parts of the cache invalidation are to be adjusted, finer adjustments to the class can be made using `Shopware\Core\Framework\DependencyInjection\CompilerPass\RemoveEventListener`, in which it is possible to define which event listeners of the service are to be removed.

```php
<?php

namespace MyProject;

use Shopware\Core\Content\Product\Events\ProductIndexerEvent;
use Shopware\Core\Content\Product\Events\ProductNoLongerAvailableEvent;
use Shopware\Core\Framework\DependencyInjection\CompilerPass\RemoveEventListener;
use Shopware\Core\Framework\Adapter\Cache\CacheInvalidationSubscriber;

class TweakCacheInvalidation implements CompilerPassInterface
{
    public function process(ContainerBuilder $container): void
    {
        RemoveEventListener::remove(
            $container,
            CacheInvalidationSubscriber::class,
            [
                [ProductIndexerEvent::class, 'invalidateListings'],
                [ProductNoLongerAvailableEvent::class, 'invalidateListings'],
            ]
        );
    }
} 
```

---

---

## Increment Storage
**Source:** [guides/hosting/performance/increment.md](https://developer.shopware.com/docs/v6.6/guides/hosting/performance/increment.md)  
# Increment Storage

The increment storage is used to store status and display it in the Administration. This can include

* Status of the message queue
* Last used module of Administration users

This storage increments or decrements a given key in a transaction-safe way, which causes locks upon the storage.

Shopware uses the `increment` table to store such information by default. When multiple message consumers are running, this table can be locked very often, decreasing workers' performance. By using different storage, the performance of those updates can be improved.

## Using Redis as storage

To use Redis, create a `config/packages/shopware.yml` file with the following content

```yaml
shopware:
    increment:
        user_activity:
          type: 'redis'
          config:
            url: 'redis://host:port/dbindex'

        message_queue:
          type: 'redis'
          config:
            url: 'redis://host:port/dbindex'
```

```yaml
shopware:
    redis:
        connections:
            persistent:
                dsn: 'redis://host:port/dbindex'

    increment:
        user_activity:
            type: 'redis'
            config:
                connection: 'persistent'

        message_queue:
            type: 'redis'
            config:
                connection: 'persistent'
```

### Redis configuration

As the information stored here is durable and should be persistent, even in the case of a Redis restart, it is recommended to configure the used Redis instance that it will not just keep the data in memory, but also store it on the disk. This can be done by using snapshots (RDB) and Append Only Files (AOF), refer to the [Redis docs](https://redis.io/docs/latest/operate/oss_and_stack/management/persistence/) for details.

As key eviction policy you should use `volatile-lru`, which only automatically deletes data that is expired, as otherwise you might risk losing data. For a detailed overview of Redis key eviction policies refer to the [Redis docs](https://redis.io/docs/latest/develop/reference/eviction/).

## Disabling the increment storage

The usage of the increment storage is optional and can be disabled. When this feature is disabled, Queue Notification and Module Usage Overview will not work in the Administration.

To disable it, create a `config/packages/shopware.yml` file with the following content:

```yaml
shopware:
    increment:
        user_activity:
            type: 'array'

        message_queue:
            type: 'array'
```

---

---

## Testing Shopware Performance with K6
**Source:** [guides/hosting/performance/k6.md](https://developer.shopware.com/docs/v6.6/guides/hosting/performance/k6.md)  
# Testing Shopware Performance with K6

K6 is a modern load testing tool that makes it easy to test the performance of your Shopware store. It runs scenario's defined in JavaScript and can be used to simulate hundreds of users accessing your store at the same time, so you can see how your store performs under load.

## Prerequisites

Before you start, make sure you have the following prerequisites:

* A Shopware store
* [K6 installed locally](https://github.com/grafana/k6/releases)
* [Bun](https://bun.sh/)

## Setting up K6 to run against your Shop

1.) First we need to clone the [Shopware K6 repository](https://github.com/shopware/k6-shopware) and install the dependencies:

```bash
git clone https://github.com/shopware/k6-shopware.git
cd k6-shopware
bun install
```

2.) Next copy `.env.example` to `.env` and adjust the values to your Shopware store:

```bash
cp .env.example .env
```

3.) After setting up the credentials we need to fetch the fixtures (salutation IDs, country IDs, sales channel configuration):

```bash
bun run fetch-fixtures.ts
```

The K6 test will use the fixtures to find the correct sales channel domain and basic information to create user and orders.

## Preparations on Shopware end

Before running the tests on your Shopware store, you need to make sure that the following settings are configured:

* No captcha is active in login/register form
* Email sending has been disabled (Admin -> Settings -> System -> Mailer -> Disable email sending)

Also, make sure the Shopware Store has some products and categories, so the test can interact with the store. If you don't have any products, you can use the following command to create some test products:

```bash
APP_ENV=prod php bin/console framework:demodata
APP_ENV=prod php bin/console dal:refresh:index
```

If you need more than the default 1000 products, you can run the command again with:

```bash
APP_ENV=prod php bin/console framework:demodata --reset-defaults --products=5000
APP_ENV=prod php bin/console dal:refresh:index
```

The command `framework:demodata` can also execute multiple times in parallel, so you can create a lot of products in a short time. Just make sure that you run `dal:refresh:index` after all processes are finished.

## Running the tests

::: warning
When running against a production environment, make sure you have informed your hosting provider. Your IP may be blocked for a short time or limited to a certain number of requests, which could lead to a false positive. Grafana Cloud is generally recommended as it allows you to distribute the load across multiple locations.
:::

To run the tests, we need an scenario file. The repository comes with a example scenario file that you can use to test your store.

```javascript
// example.js
import {
  accountRegister,
  addProductToCart,
  placeOrder,
  visitCartPage,
  visitConfirmPage,
  visitNavigationPage,
  visitProductDetailPage,
  visitSearchPage,
  visitStorefront,
} from "./helpers/storefront.js";

export default function () {
  visitStorefront();
  visitSearchPage();
  visitNavigationPage();
  accountRegister();
  visitNavigationPage();
  addProductToCart(visitProductDetailPage().id);
  visitCartPage();
  visitConfirmPage();
  placeOrder();
}
```

So the test does:

* Visits home page
* Visits a search page with random term
* Visits a random navigation page
* Registers a new account
* Visits a random navigation page
* Visits a product detail page and adds the product to the cart
* Visits the cart page
* Visits the confirm page
* Places an order

and then the session ends and a new session starts and does it again.

To run the test, you can use the following command:

```bash
k6 run example.js
```

This will run the test with 1 virtual user and 1 iteration, so you can verify that the test is working correctly. To run the test with more virtual users and iterations, you can use the following command:

```bash
k6 run --vus 10 --iterations 100 example.js
```

so now the test will run with 10 virtual users and 100 iterations.

## Running multiple scenarios

You can also run multiple scenarios in the same file. To do this, you can define them in the options like so:

```javascript
// example.js
import { productChangePrice, productChangeStocks, fetchBearerToken, useCredentials, productImport } from "./helpers/api.js";
import {
  accountRegister,
  addProductToCart,
  placeOrder,
  visitNavigationPage,
  visitProductDetailPage,
  visitSearchPage,
  visitStorefront,
} from "./helpers/storefront.js";

export const options = {
  scenarios: {
    browse_only: {
      executor: 'constant-vus',
      vus: 10,
      duration: '5m',
      exec: 'browseOnly',
    },
    fast_buy: {
      executor: 'constant-vus',
      vus: 1,
      duration: '5m',
      exec: 'fastBuy',
    },
    import: {
      executor: 'constant-vus',
      vus: 1,
      duration: '5m',
      exec: 'importer',
    }
  },
};

export function browseOnly() {
  visitStorefront();
  visitSearchPage();
  visitNavigationPage();
  visitProductDetailPage();
}

export function fastBuy() {
  addProductToCart(visitProductDetailPage().id);
  accountRegister();
  placeOrder();
}

export function setup() {
  const token = fetchBearerToken();

  return { token };
}

export function importer(data) {
  useCredentials(data.token);
  productImport();
  productChangePrice();
  productChangeStocks();
}
```

and then you can run the test with the following command:

```bash
k6 run example.js
```

This will run the test with 3 scenarios, `browse_only`, `fast_buy` and `import`. When using scenarios, you cannot define the users and iterations anymore in the command-line. They need to be configured in the `options` object in your script.

There are a lot of options how the scenarios should work together, you can find more information in the [K6 documentation](https://k6.io/docs/using-k6/scenarios/).

## Enabling the K6 dashboard

K6 has an embedded dashboard that you can use to monitor the test results in real-time. To enable the dashboard, you can use the following command:

```bash
K6_WEB_DASHBOARD=true k6 run --vus 10 --duration 5m example.js
```

and then you can open <http://127.0.0.1:5665/ui/?endpoint=/> in your browser to see the dashboard.

![K6 Dashboard](../../../assets/k6-dashboard.png)

## Running the tests in the Cloud with K6 Cloud

You can also run the tests in the cloud with K6 Cloud. To do this, you need to create an account on the [K6 Cloud](https://grafana.com/products/cloud/k6/) and get an API token.
This allows you to utilize the K6 Cloud infrastructure to run the tests with a lot of more users, customize the location of the users and get more detailed reports with Grafana Dashboards.

![K6 Cloud Dashboard](../../../assets/k6-cloud.png)

---

---

## Lock store
**Source:** [guides/hosting/performance/lock-store.md](https://developer.shopware.com/docs/v6.6/guides/hosting/performance/lock-store.md)  
# Lock store

Shopware uses [Symfony's lock component](https://symfony.com/doc/5.4/lock.html) to implement locking functionality.
By default, Symfony will use a local lock store. This means in multi-machine (cluster) setups, naive file locks will break the system; therefore, it is highly recommended to use one of the [supported remote stores](https://symfony.com/doc/5.4/components/lock.html#available-stores).

## Using Redis as a lock store

As Redis can already be used for [caching](./caches), [increment store](./increment), and [session storage](./session), you can also use that Redis host as a remote lock store.
To use Redis, create a `config/packages/lock.yaml` file with the following content:

```yaml
framework:
    lock: 'redis://host:port'
```

## Other lock stores

As Shopware uses [Symfony's lock component](https://symfony.com/doc/5.4/lock.html), all lock stores supported by Symfony can be used.
Keep in mind that you should always use a remote store if you host Shopware in a cluster setup.
For a list of all available lock stores, refer to [Symfony's documentation](https://symfony.com/doc/5.4/components/lock.html#available-stores).
There is also more detailed information on the [configuration options](https://symfony.com/doc/5.4/lock.html#configuring-lock-with-frameworkbundle).

---

---

## Number Ranges
**Source:** [guides/hosting/performance/number-ranges.md](https://developer.shopware.com/docs/v6.6/guides/hosting/performance/number-ranges.md)  
# Number Ranges

Number Ranges provide a consistent way to generate a consecutive number sequence that is used for order numbers, invoice numbers, etc.
The generation of the number ranges is an **atomic** operation. This guarantees that the sequence is consecutive and that no number is generated twice.

By default, the number range states are stored in the database.
In scenarios where high throughput is required (e.g., thousands of orders per minute), the database can become a performance bottleneck because of the requirement for atomicity.
Redis offers better support for atomic increments than the database. Therefore the number ranges should be stored in Redis in such scenarios.

## Using Redis as storage

To use Redis, create a `config/packages/shopware.yml` file with the following content:

```yaml
shopware:
    number_range:
        increment_storage: "Redis"
        redis_url: 'redis://host:port/dbindex'
```

```yaml
shopware:
    redis:
        connections:
            persistent:
                dsn: 'redis://host:port/dbindex'
    number_range:
        increment_storage: 'redis'
        config:
            connection: 'persistent'
```

### Redis configuration

As the information stored here is durable and should be persistent, even in the case of a Redis restart, it is recommended to configure the used Redis instance that it will not just keep the data in memory, but also store it on the disk. This can be done by using snapshots (RDB) and Append Only Files (AOF), refer to the [Redis docs](https://redis.io/docs/latest/operate/oss_and_stack/management/persistence/) for details.

As key eviction policy you should use `volatile-lru`, which only automatically deletes data that is expired, as otherwise you might risk losing data. For a detailed overview of Redis key eviction policies refer to the [Redis docs](https://redis.io/docs/latest/develop/reference/eviction/).

## Migrating between storages

You can migrate the current state of the number ranges from your current storage to a new one by running the following CLI command:

```shell
bin/console number-range:migrate {fromStorage} {toStorage}
```

For example, if you want to migrate from the default `SQL` storage to the high-performing `Redis` storage, the command is:

```shell
bin/console number-range:migrate SQL Redis
```

::: info
If you want to migrate from or to `Redis`, ensure the `shopware.number_range.redis_url` is correctly configured, regardless if `Redis` is currently configured as the `increment_storage`.
:::

::: warning
The migration of the number ranges between different storages is **not atomic**. This means that if you migrate the number ranges and simultaneously generate new number increments, this may lead to the same number being generated twice.
Therefore, this command should normally not run during normal operations of the shop but rather during part of a deployment or maintenance.
:::

---

---

## Performance Tweaks
**Source:** [guides/hosting/performance/performance-tweaks.md](https://developer.shopware.com/docs/v6.6/guides/hosting/performance/performance-tweaks.md)  
*(Body truncated in this bundle; follow the link for the rest.)*

# Performance Tweaks

Shopware is a platform for many different projects. It needs to handle a broad range of load characteristics and environments. It means that the default configuration is optimized for the best out-of-the-box experience. However, there are many opportunities to increase the performance by fitting the configuration to your needs.

## HTTP cache

To ensure a high RPS (Requests Per Second), Shopware offers an integrated HTTP cache with a possible reverse proxy configuration. Any system that handles high user numbers should always use HTTP caching to reduce server resources.

To enable this, set `SHOPWARE_HTTP_CACHE_ENABLED=1` in the `.env`

### Reverse proxy cache

When you have many app servers, you should consider using a [reverse proxy cache](../infrastructure/reverse-http-cache) like Varnish. Shopware offers a default configuration for Varnish out-of-the-box and a [Varnish Docker image](https://github.com/shopware/varnish-shopware) for development.

### Logged-in / cart-filled

By default, Shopware can no longer deliver complete pages from a cache for a logged-in customer or if products are in the shopping cart. As soon as this happens, the user sessions differ, and the context rules could be different depending on the user. This results in different content for each customer. A good example is the [Dynamic Access](https://docs.shopware.com/en/shopware-6-en/extensions/dynamiccontent) plugin.

However, if the project does not require such functionality, pages can also be cached by the HTTP cache/reverse proxy. To disable cache invalidation in these cases:

```yaml
# config/packages/prod/shopware.yaml
shopware:
    cache:
        invalidation:
            http_cache: []
```

### Delayed invalidation

A delay for cache invalidation can be activated for systems with a high update frequency for the inventory (products, categories). Once the instruction to delete the cache entries for a specific product or category occurs, they are not deleted instantly but processed later by a background task. Thus, if two processes invalidate the cache in quick succession, the timer for the invalidation of this cache entry will only reset.
By default, the scheduled task will run every 20 seconds, but the interval can be adjusted over the `scheduled_taks` DB table, by setting the `run_interval` to the desired value (it is configured in seconds) for the entry with the name `shopware.invalidate_cache`.

::: warning
If you enable delayed cache invalidation, you must set up a worker to run [Scheduled Tasks](../infrastructure/scheduled-task), e.g., using the [Message Queue](../infrastructure/message-queue).
:::

There are two possible storages/adapters for delayed cache invalidation: Redis and MySQL. Redis is preferred since it handles retrieving and deleting keys in an atomic manner. MySQL also supports it, but it's more complicated, and at a certain load, deadlocks are inevitable. If you already use Redis, use it also for the delayed cached. The MySQL adapter should only be used when you cannot use Redis.

Redis:

```yaml
# config/packages/prod/shopware.yaml
shopware:
    cache:
        invalidation:
            delay: 1 # 0 = disabled, 1 = enabled
            delay_options:
                storage: redis
                connection: 'ephemeral' # connection name from redis configuration
```

MySQL:

```yaml
# config/packages/prod/shopware.yaml
shopware:
    cache:
        invalidation:
            delay: 1 # 0 = disabled, 1 = enabled
            delay_options:
                storage: mysql
```

## MySQL configuration

Shopware sets some MySQL configuration variables on each request to ensure it works in any environment. You can disable this behavior if you have correctly configured your MySQL server.

* Make sure that `group_concat_max_len` is by default higher or equal to `320000`
* Make sure that `sql_mode` doesn't contain `ONLY_FULL_GROUP_BY`
* Make sure that `time_zone` is set to UTC (`default-time-zone='+00:00'` in `my.cnf`)
  and then you can set `SQL_SET_DEFAULT_SESSION_VARIABLES=0` to your `.env` file

## SQL is faster than DAL

DAL(Data Abstraction Layer) has been designed suitably to provide developers with a flexible and extensible data management. However, features in such a system come at the cost of performance. Therefore, using DBAL (plain SQL) is much faster than using the DAL in many scenarios, especially when it comes to internal processes, where often only one ID of an entity is needed.

Refer to this article to know more on [when to use plain SQL and DAL](../../../resources/references/adr/2021-05-14-when-to-use-plain-sql-or-dal).

## Elasticsearch/Opensearch

Elasticsearch/Opensearch is a great tool to reduce the load of the MySQL server. Especially for systems with large product assortments, this is a must-have since MySQL simply does not cope well above a certain assortment size.

When using Elasticsearch, it is important to set the `SHOPWARE_ES_THROW_EXCEPTION=1` `.env` variable. This ensures that there is no fallback to the MySQL server if an error occurs when querying the data via Elasticsearch. In large projects, the failure of Elasticsearch leads to the MySQL server being completely overloaded otherwise.

Read more on [Elasticsearch setup](../infrastructure/elasticsearch/elasticsearch-setup)

## Prevent mail data updates

::: info
[Prevent mail updates](../../../resources/references/adr/2022-03-25-prevent-mail-updates.md) feature is available starting with Shopware 6.4.11.0.
:::

To provide auto-completion for different mail templates in the Administration UI, Shopware has a mechanism that writes an example mail into the database when sending the mail.

With the `shopware.mail.update_mail_variables_on_send` configuration, you can disable this source of database load:

```yaml
# config/packages/prod/shopware.yaml
shopware:
    mail:
        update_mail_variables_on_send: false
```

If you ever wonder why it is in `prod`, take a look into the [Symfony configuration environments](https://symfony.com/doc/current/configuration.html#configuration-environments).

## Increment storage

The [Increment storage](../performance/increment) is used to store the state and display it in the Administration.
This storage increments or decrements a given key in a transaction-safe way, which causes locks upon the storage. Therefore, we recommend moving this source of server load to a separate Redis, as described in [Increment storage Redis configuration](./increment#redis-configuration).\
If you don't need such functionality, it is highly recommended that you disable this behavior by using `array` as a type.

## Lock storage

Shopware uses [Symfony's Lock component](https://symfony.com/doc/5.4/lock.html) to implement locking functionality.
By default, Symfony will use a local file-based [lock store](../performance/lock-store), which breaks into multi-machine (cluster) setups. This is avoided using one of the [supported remote stores](https://symfony.com/doc/5.4/components/lock.html#available-stores).

```yaml
# config/packages/prod/framework.yaml
framework:
    lock: 'redis://host:port'
```

## Number ranges

[Number Ranges](../performance/number-ranges) provide a consistent way to generate a consecutive number sequence that is used for order numbers, invoice numbers, etc.
The generation of the number ranges is an **atomic** operation, which guarantees that the sequence is consecutive and no number is generated twice.

By default, the number range states are stored in the database.
In scenarios where high throughput is required (e.g., thousands of orders per minute), the database can become a performance bottleneck because of the requirement for atomicity.
Redis offers better support for atomic increments than the database. Therefore, the number ranges should be stored in Redis in such scenarios, see [Number Ranges - using Redis as a storage](./number-ranges#using-redis-as-storage).

## Sending mails with the Queue

Shopware sends the mails by default synchronously. This process can take a while when the remote SMTP server is struggling. For this purpose, it is possible to handle the mails in the message queue. To enable this, add the following config to your config:

```yaml
# config/packages/prod/framework.yaml
framework:
    mailer:
        message_bus: 'messenger.default_bus'
```

## PHP Config tweaks

```ini
; don't evaluate assert()
zend.assertions=-1

; cache file_exists,is_file
; WARNING: this will lead to thrown errors after clearing cache while it tries to access cached Shopware_Core_KernelProdDebugContainer.php
opcache.enable_file_override=1

; increase opcache string buffer as shopware has many files
opcache.interned_strings_buffer=20

; disables opcache validation for timestamp for reinvalidation of the cache
; WARNING: you need to clear on deployments the opcache by reloading php-fpm or cachetool (https://github.com/gordalina/cachetool)
opcache.validate_timestamps=0

; disable check for BOM
zend.detect_unicode=0

; increase default realpath cache
realpath_cache_ttl=3600
```

::: info
The web updater is not compatible with opcache, as updates require an opcache clear.
:::

Also, PHP PCRE Jit Target should be enabled. This can be checked using `php -i | grep 'PCRE JIT Target'` or looking into the *phpinfo* page.

For an additional 2-5% performance improvement, it is possible to provide a preload file to opcache. Preload also brings a lot of drawbacks:

* Each cache clear requires a PHP-FPM restart
* Each file change requires a PHP-FPM restart
* The Extension Manager does not work

The PHP configuration would look like:

```ini
opcache.preload=/var/www/html/var/cache/opcache-preload.php
opcache.preload_user=nginx
```

## Cache ID

The Shopware cache has a global cache ID to clear the cache faster and work in a cluster setup. This cache ID is saved in the database and will only be changed when the cache is cleared. This ensures that the new cache is used and the message queue can clean the old folder. If this functionality is not used, this cache ID can also be hardcoded `SHOPWARE_CACHE_ID=foo` in the `.env` to save one SQL query on each request.

## .env.local.php

[Symfony recommends](https://symfony.com/doc/current/configuration.html#configuring-environment-variables-in-production) that a `.env.local.php` file is used in Production instead of a `.env` file to skip parsing of the  .env file on every request.
If you are using a containerized environment, all those variables can also be set directly in the environment variables instead of dumping them into a file.

Since Shopware 6.4.15.0, you can dump the content of the `.env` file to a `.env.local.php` file by running `bin/console system:setup --dump-env` or `bin/console dotenv:dump {APP_ENV}`.

## Benchmarks

In addition to the benchmarks that Shopware regularly performs with the software, we strongly recommend integrating your benchmark tools and pipelines for larger systems. A generic benchmark of a product can rarely be adapted to individual, highly customized projects.
Tools such as [locust](https://locust.io/) or [k6](https://k6.io/) can be used for this purpose.

## Logging

Set the log level of the monolog to `error` to reduce the amount of logged events. Also, limiting the `buffer_size` of monolog prevents memory overflows for long-lived jobs:

```yaml
# config/packages/prod/monolog.yaml
monolog:
    handlers:
        main:
            level: error
            buffer_size: 30
        business_event_handler_buffer:
            level: error
```

The `business_event_handler_buffer` handler logs flow. Setting it to `error` will disable the logging of flow activities that succeed.

## Disable App URL external check

On any Administration load, Shopware tries to request itself to test that the configured `APP_URL` inside `.env` is correct.
If your `APP_URL` is correct, you can disable this behavior with an environment variable `APP_URL_CHECK_DISABLED=1`.

## Disable fine-grained caching

Shopware has

… **Truncated.** Full document: https://developer.shopware.com/docs/v6.6/guides/hosting/performance/performance-tweaks.md


---

## Shopware Session
**Source:** [guides/hosting/performance/session.md](https://developer.shopware.com/docs/v6.6/guides/hosting/performance/session.md)  
# Shopware Session

Shopware, by default, uses the session storage configured in PHP. On most installations, this is the file system. In smaller setups, you will not need to take care of sessions. However, for larger setups using clustering or with a lot of traffic, you will probably configure alternative session storage, such as Redis, to reduce the load on the database.

## Session adapters

### Configure Redis using PHP.ini

By default, Shopware uses the settings configured in PHP. You can reconfigure the Session config directly in your `php.ini`. Here is an example of configuring it directly in PHP.

```ini
session.save_handler = redis
session.save_path = "tcp://host:6379?database=0"
```

Please refer to the official [PhpRedis documentation](https://github.com/phpredis/phpredis#php-session-handler) for all possible options.

### Configure Redis using Shopware configuration

If you don't have access to the php.ini configuration, you can configure it directly in Shopware itself. For this, create a `config/packages/redis.yml` file with the following content:

```yaml
# config/packages/redis.yml
framework:
    session:
        handler_id: "redis://host:port/0"
```

### Redis configuration

As the information stored here is durable and should be persistent, even in the case of a Redis restart, it is recommended to configure the used Redis instance that it will not just keep the data in memory, but also store it on the disk. This can be done by using snapshots (RDB) and Append Only Files (AOF), refer to the [Redis docs](https://redis.io/docs/latest/operate/oss_and_stack/management/persistence/) for details.

As key eviction policy you should use `allkeys-lru`, which only automatically deletes the last recently used entries when Redis reaches max memory consumption. For a detailed overview of Redis key eviction policies see the [Redis docs](https://redis.io/docs/latest/develop/reference/eviction/).

### Other adapters

Symfony also provides PHP implementations of some adapters:

* [PdoSessionHandler](https://github.com/symfony/symfony/blob/6.3/src/Symfony/Component/HttpFoundation/Session/Storage/Handler/PdoSessionHandler.php)
* [MemcachedSessionHandler](https://github.com/symfony/symfony/blob/6.3/src/Symfony/Component/HttpFoundation/Session/Storage/Handler/MemcachedSessionHandler.php)
* [MongoDbSessionHandler](https://github.com/symfony/symfony/blob/6.3/src/Symfony/Component/HttpFoundation/Session/Storage/Handler/MongoDbSessionHandler.php)

To use one of these handlers, you must create a new service in the dependency injection and set the `handler_id` to the service id.

Example service definition:

```xml
<service id="session.db" class="Symfony\Component\HttpFoundation\Session\Storage\Handler\PdoSessionHandler">
    <argument ....></argument>
</service>
```

Example session configuration:

```yaml
# config/packages/redis.yml
framework:
    session:
        handler_id: "session.db"
```

---

---

## Installation Overview
**Source:** [guides/installation.md](https://developer.shopware.com/docs/v6.6/guides/installation.md)  
# Installation Overview

This section discusses ways to set up Shopware on local machines so you can use it as a foundation for your development.

There are a couple of ways to get Shopware running on your system, together with the most useful services for data storage and the web server.

## Template

Regardless of your choice of setup, all setup methods are based on the [Project template](./template.md). This template is a new Composer project, which requires Shopware itself. Therefore, you can further customize your installation with additional extensions, themes, or configurations.

## Setups

The following setups are available for Shopware 6:

---

---

## Community Setup
**Source:** [guides/installation/community.md](https://developer.shopware.com/docs/v6.5/guides/installation/community.md)  
# Community Setup

The community setup is the recommended installation procedure for the latest versions of Shopware. It is a streamlined installation process, providing an intuitive interface for users to set up their Shopware store via Dockware.

---

---

## Dockware
**Source:** [guides/installation/community/dockware.md](https://developer.shopware.com/docs/v6.5/guides/installation/community/dockware.md)  
# Dockware

Dockware is basically a managed Docker setup for Shopware 6. It makes it possible to start Shopware 6 very quickly using dockware.io. It comes with everything you need for a smooth development workflow. This includes all available Shopware 6 versions, MySQL, Adminer, Mailcatcher, easy PHP switching, XDebug, useful make commands, and more.

Dockware is maintained by *dasistweb GmbH*. They provide detailed [documentation](https://dockware.io/docs) as well. This way, we will cover just the basics here.

## Dockware versions

Dockware images come in several versions, so you can choose the one which fits your needs best. You can find a brief overview below, but as always, please refer to [their website](https://dockware.io/) for a detailed comparison.

| Image | Description | Basis |
| :--- | :--- | :--- |
| dockware #play | Launch Shopware in just a couple of seconds locally on your system. Test every functionality and play around while verifying your requirements. | `Production` |
| dockware #dev | This is the solution for instant coding. Run Shopware 6, prepare your IDE and immediately start with your own customizations and plugins. Provides Xdebug, watchers or more. | `Production` |
| dockware #contribute | This image supports Shopware 6 modification to contribute to the official Shopware 6 Github platform. Contains all dev tools and the already installed demo data. | `development` |
| dockware #essentials | This is a plain Dockware environment without Shopware. | --- |
| dockware #flex | This provides a flexible Apache and PHP container for all kinds of Symfony and Shopware projects. It is an image for individualization, e.g., you can manage the Shopware version on your own. | --- |

## Quickstart

First things first, install Docker on your local machine.

* If using Linux, you need to start by downloading the latest version of Docker and installing it on your system. To name a few examples, you can find the matching Docker versions for your distribution here:

  * [Docker for Ubuntu](https://docs.docker.com/install/linux/docker-ce/ubuntu/)
  * [Docker for Debian](https://docs.docker.com/install/linux/docker-ce/debian/)
  * [Docker for CentOS](https://docs.docker.com/install/linux/docker-ce/centos/)
  * [Docker for Fedora](https://docs.docker.com/install/linux/docker-ce/fedora/)

* For Windows operating system, download the latest version of [Docker desktop for Windows](https://hub.docker.com/editions/community/docker-ce-desktop-windows/).

* If using Mac, start by downloading the latest version of [Docker Desktop](https://hub.docker.com/editions/community/docker-ce-desktop-mac/) for Mac and install it.

With this, you are almost ready to start, but you just need to use the following command on your host system to get it going:

```bash
# quick run with latest PHP and Shopware
$ docker run --rm -p 80:80 dockware/dev:latest
```

::: danger
Beware that this is meant for a quick start. The parameter `--rm` will throw everything away. If the container is stopped, the whole database etc., will be gone. So if you want a persistent solution, head over to the ["Using docker-compose"](#using-docker-compose) paragraph.
:::

This command will install Dockware #dev version, which is based on `Production` template. If you want to use `development` template, you need to use #contribute version. As soon as the docker image is downloaded and Dockware is ready, you will see this text:

```bash
SUCCESS - Shopware is now ready!
-----------------------------------------------------
SHOP URL: http://localhost
ADMIN URL: http://localhost/admin
ADMINER URL: http://localhost/adminer.php
MAILCATCHER URL: http://localhost/mailcatcher
```

### Further ways to start

You can start the Dockware image with different shopware versions:

```bash
docker run --rm -p 80:80 --env PHP_VERSION=7.2 dockware/dev:latest
```

## Using docker-compose

### Create docker-compose.yml

Create a new `docker-compose.yml` in the folder where you want to start your project and use our template below.

Dockware does already come with an installed Shopware 6. You can change the Shopware version along with the PHP version in your compose file.

Here is an overview of what versions are available: <https://hub.docker.com/r/dockware/dev>

```yaml
version: "3"

services:

    shopware:
      # use either tag "latest" or any other version like "6.5.3.0", ...
      image: dockware/dev:latest
      container_name: shopware
      ports:
         - "80:80"
         - "3306:3306"
         - "22:22"
         - "8888:8888"
         - "9999:9999"
      volumes:
         - "db_volume:/var/lib/mysql"
         - "shop_volume:/var/www/html"
      networks:
         - web
      environment:
         # default = 0, recommended to be OFF for frontend devs
         - XDEBUG_ENABLED=1
         # default = latest PHP, optional = specific version
         - PHP_VERSION=8.1

volumes:
  db_volume:
    driver: local
  shop_volume:
    driver: local

networks:
  web:
    external: false
```

### Start Docker

Open the folder with your compose file in your terminal and execute this command to start your container:

```bash
docker-compose up -d
```

### Prepare development

Now download the current version of Shopware to your host into the "src" directory.

This is required to have code completion and IntelliSense right in your IDE.

```bash
mkdir -p ./src
docker cp shopware:/var/www/html/. ./src
```

### Prepare IDE

Open the "src" folder with your preferred IDE and wait until it finishes loading. Then add a new SFTP connection to your container. (we recommend Automatic-Upload if possible)

Now you are done and ready to develop your own plugins and projects.

::: info
Default credentials for Dockware can be found at <https://docs.dockware.io/use-dockware/default-credentials>
:::

## Next steps

You might want to start writing your very own plugin. Head over to ["Plugin base guide"](../../plugins/plugins/plugin-base-guide) to get a grip on that topic.

::: info
Refer to this video on **[Using Dockware](https://www.youtube.com/watch?v=b9wVfUOKqmI)** that explains the basics of Dockware. Also available on our free online training ["Shopware 6 Backend Development"](https://academy.shopware.com/courses/shopware-6-backend-development-with-jisse-reitsma).
:::

---

---

## Devenv
**Source:** [guides/installation/devenv.md](https://developer.shopware.com/docs/v6.5/guides/installation/devenv.md)  
# Devenv

## What is devenv?

Imagine [devenv](https://devenv.sh) to function as a dependency manager for the services and packages that you need to run your application for local development or even in a CI/CD context.

Similar to other package managers, devenv lets you describe what your environment should look like and locks dependencies to a specific version to help you compose a reproducible setup.

Devenv not only lets you choose from and install different versions of binaries (e.g., PHP, Node, npm), but it also allows you to configure and run services (like MySQL, Redis, OpenSearch). The binaries and states of the services are stored on a per-project level.

The main difference to other tools like Docker or a VM is that it neither uses containerization nor virtualization techniques. Instead, the services run natively on your machine.

## Installation

### Nix

As devenv is built on top of Nix, first install Nix with the following command based on your OS:

```shell
sh <(curl -L https://nixos.org/nix/install)
```

```shell
sh <(curl -L https://nixos.org/nix/install) --daemon
```

```shell
sh <(curl -L https://nixos.org/nix/install) --no-daemon
```

```shell
docker run -it nixos/nix
```

#### Using Oh My ZSH?

You probably won't be able to use the commands below. Use the following steps to continue using [oh my zsh](https://ohmyz.sh/):

* Open `/etc/zshrc` and look for the following lines (probably at the end of the file):

```bash
# Nix
if [ -e '/nix/var/nix/profiles/default/etc/profile.d/nix-daemon.sh' ]; then
   . '/nix/var/nix/profiles/default/etc/profile.d/nix-daemon.sh'
fi
# End Nix
```

* Copy these lines and delete them from this file.
* Open `~/.zshrc` and add the above-copied lines to the end of this file.
* Initiate the terminal with `source ~/.zshrc` or reboot your terminal for nix to work.

[Credits: "nixos installation issue,'command not found: nix'", StackOverflow](https://stackoverflow.com/a/70822086/982278)

### Cachix

Next, install [Cachix](https://www.cachix.org/) to speed up the installation:

```shell
nix-env -iA cachix -f https://cachix.org/api/v1/install
```

Before installing devenv, instruct Cachix to use the devenv cache:

```shell
cachix use devenv
```

::: info
The first time you run `cachix use`, you will be prompted a warning that you are not a trusted user.
:::

> This user doesn't have permission to configure binary caches.
>
> You can either:
>
> a) ...
>
> b) ...

When you encounter the above message, run:

```shell
echo "trusted-users = root ${USER}" | sudo tee -a /etc/nix/nix.conf && sudo pkill nix-daemon
```

### Devenv

Finally, install devenv:

```shell
nix-env -if https://github.com/cachix/devenv/tarball/latest
```

Before booting up your development environment, configure Cachix to use Shopware's cache:

```shell
cachix use shopware
```

You can find the whole installation guide for devenv in their official documentation:

### Shopware

Depending on whether you want to set up a fresh Shopware project or contribute to the Shopware core, you have to choose between the [Symfony Flex template](template) or the Shopware project.

```shell
cd <YOUR_SHOPWARE_FLEX_PROJECT_ROOT>
```

```shell
composer require devenv
```

This will create a basic `devenv.nix` file to enable devenv support for Shopware.


```shell
git clone git@github.com:shopware/shopware.git
```

Since the environment is described via a `devenv.nix` file committed to version control, you can now boot up the environment:

```shell
devenv up
```

::: info
If the command fails, try to update devenv `shell devenv update` once before booting up the environment.
:::

::: warning
Make sure that the ports for the services are not already in use, or else the command will fail.
:::

Check your default web services with the following commands:

```bash
netstat -p tcp -van | grep '^Proto\|LISTEN'
```

```bash
ss -tulpn | grep ':80\|:3306\|:6379'
```

Ensure to change your `.env` file to have the database connect using localhost's IP address instead of the default MySQL socket:

```txt
// <PROJECT_ROOT>/.env
DATABASE_URL="mysql://shopware:shopware@127.0.0.1:3306/shopware?sslmode=disable&charset=utf8mb4"
```

With a new terminal, go to the project directory and run the following command to launch a devenv shell.
This shell includes all needed programs (php, composer, npm, node, etc.) to initialize Shopware:

```shell
devenv shell
```

In the devenv shell, run the following command to initialize Shopware:

```shell
bin/console system:install --basic-setup --create-database --force
```

### Direnv

If you wish to switch between multiple development environments which use devenv seamlessly, we recommend installing [direnv](https://direnv.net/).

When you enter a project directory using devenv, direnv will automatically activate the environment for you.
This means you can use the binaries without having to run `devenv shell` manually, though you still have to run `devenv up` to start all services.

First, install direnv:

```bash
brew install direnv
```

```bash
apt install direnv
```

Afterward, add the following hook to your shell:

```bash
// ~/.bashrc
eval "$(direnv hook bash)"
```

```bash
// ~/.zshrc
eval "$(direnv hook zsh)"
```

```bash
// ~/.config/fish/config.fish
direnv hook fish | source
```

After you change into a project directory using devenv for the first time, you need to allow direnv to load the environment:

```bash
direnv allow
```

## Default services

Here is an overview of services Shopware provides by default and how you can access them:

| Service        | Access                                          |
|----------------|-------------------------------------------------|
| MySQL          | `mysql://shopware:shopware@127.0.0.1:3306`      |
| Mailhog (SMTP) | `smtp://127.0.0.1:1025`                         |
| Redis (TCP)    | `tcp://127.0.0.1:6379`                          |

### Caddy

Caddy is a powerful, enterprise-ready, open-source web server with automatic HTTPS written in Go.

<http://127.0.0.1:8000>

### Adminer

Adminer is a full-featured database management tool written in PHP.

<http://localhost:8010>

### Mailhog

MailHog is an email testing tool for developers.

<http://localhost:8025>

## Customize your setup

To customize the predefined services to match your needs, e.g., changing the virtual host, database name, or environment variables, you can create `devenv.local.nix` to override the service definitions.
It also allows you to add and configure additional services you might require for your local development.

::: warning
After changing `devenv.local.nix`, please [reload your environment](#manually-reloading-devenv).
:::

```nix
// <PROJECT_ROOT>/devenv.local.nix
{ pkgs, config, lib, ... }:

{
  # Disable a service
  services.adminer.enable = false;
  
  # Use a custom virtual host
  services.caddy.virtualHosts."http://shopware.swag" = {
    extraConfig = ''
      root * public
      php_fastcgi unix/${config.languages.php.fpm.pools.web.socket}
      file_server
    '';
  };
  
  # Customize nodejs version
  languages.javascript = {
    package = pkgs.nodejs-18_x;
  };

  # Override an environment variable
  env.APP_URL = "http://shopware.swag:YOUR_CADDY_PORT";
}
```

Refer to the official devenv documentation to get a complete list of all available services and their configuration possibilities:

### Enable Blackfire

```nix
// <PROJECT_ROOT>/devenv.local.nix
{ pkgs, config, lib, ... }:

{
  services.blackfire.enable = true;
  services.blackfire.server-id = "<SERVER_ID>";
  services.blackfire.server-token = "<SERVER_TOKEN>";
  services.blackfire.client-id = "<CLIENT_ID>";
  services.blackfire.client-token = "<CLIENT_TOKEN>";
}
```

### Enable XDebug

```nix
// <PROJECT_ROOT>/devenv.local.nix
{ pkgs, config, lib, ... }:

{
  # XDebug
  languages.php.extensions = [ "xdebug" ];
  languages.php.ini = ''
    xdebug.mode = debug
    xdebug.discover_client_host = 1
    xdebug.client_host = 127.0.0.1
  '';
}
```

### Use MariaDB instead of MySQL

```nix
// <PROJECT_ROOT>/devenv.local.nix
{ pkgs, config, lib, ... }:

{
  services.mysql.package = pkgs.mariadb;
}
```

### Use customized MySQL port

```nix
// <PROJECT_ROOT>/devenv.local.nix
{ pkgs, config, lib, ... }:

{
  services.mysql.settings = {
    mysqld = {
      port = 33881;
    };
  };
  
}
```

### Use customized VirtualHosts port for Caddy

```nix
// <PROJECT_ROOT>/devenv.local.nix
{ pkgs, config, lib, ... }:

{
  services.caddy.virtualHosts.":8029" = {
    extraConfig = ''
      root * public
      php_fastcgi unix/${config.languages.php.fpm.pools.web.socket}
      file_server
    '';
 };
}
```

```nix
// <PROJECT_ROOT>/devenv.local.nix
{ pkgs, config, lib, ... }:

{
  services.caddy.virtualHosts."http://shopware.swag:8029" = {
    extraConfig = ''
      root * public
      php_fastcgi unix/${config.languages.php.fpm.pools.web.socket}
      file_server
    '';
  };
```

### Use customized Adminer port

```nix
// <PROJECT_ROOT>/devenv.local.nix
{ pkgs, config, lib, ... }:

{
  services.adminer.listen = "127.0.0.1:9084";
}
```

## Known issues

### Manually reloading devenv

If you decided against using direnv, keep in mind that on every change to the `*.nix` files you need to manually reload the environment. Run `exit` to quit the current devenv shell and enter the shell again to reload:

```shell
devenv shell
```

### Direnv slow in big projects

The bigger your project directory is getting over time (e.g., cache files piling up), the slower direnv will be.
This is a known issue, and the devenv developers are working on a solution.

### Fail to start Redis with locale other than en\_US

```shell
14:04:52 redis.1           | 364812:M 07 Nov 2023 14:04:52.999 # Failed to configure LOCALE for invalid locale name.
```

You can export a different locale to your shell with the following command:

```shell
export LANG=en_US.UTF8;
```

## FAQ

### How do I clean up devenv?

Periodically run `devenv gc` to remove orphaned services, packages and processes and free-up disk space.

### How do I access the database?

The MySQL service is exposed under its default port `3306`, see [default services](#default-services).

Be aware that you cannot connect using the `localhost` socket. Instead, you must use `127.0.0.1`.

### Where is the database stored?

The database is stored in the `<PROJECT_ROOT>/.devenv/state/mysql` directory.

### Where do I find available packages?

The [NixOS package search](https://search.nixos.org/packages) is a good starting point.

### Where do I find the binaries?

The binaries can be found in the `<PROJECT_ROOT>/.devenv/profile/bin` directory.

This comes in handy if you want to configure interpreters in your IDE.

### How do I stop all processes at once?

In case you can't find and stop running devenv processes, you can use the following command to kill them:

```shell
kill $(ps -ax | grep /nix/store  | awk '{print $1}')
```

### Are you unable to access http://127.0.0.1:8000 in your Browser?

Try using http://localhost:8000 instead. This mostly applies to when using WSL2.

### Are you looking for a full test setup with demo data?

Run the below command:

```shell
composer setup && APP_ENV=prod bin/console framework:demodata && APP_ENV=prod bin/console dal:refresh:index
```

---

---

## guides/installation/legacy.md
**Source:** [guides/installation/legacy.md](https://developer.shopware.com/docs/v6.4/guides/installation/legacy.md)  
---

---

## Docker
**Source:** [guides/installation/legacy/docker.md](https://developer.shopware.com/docs/v6.4/guides/installation/legacy/docker.md)  
# Docker

::: danger
This approach is no longer recomended. It is kept here as a reference.
:::

Docker is **not** the recommended way to install Shopware 6 on a Mac when it comes to the default way, due to performance issues. You can still have a look at other possibilities below.

When using Windows, it is recommended to use [Dockware](../community/dockware) or other ways to install Shopware.

## Default way

On Linux OS, Docker installation is the easiest way to get a running Shopware 6. This way you can set up Shopware 6 with just three easy commands:

1. Build and start the containers:

```bash
./psh.phar docker:start
```

1. Access the application container:

```bash
./psh.phar docker:ssh
```

1. Execute the installer inside the docker container:

```bash
./psh.phar install
```

This may take a while since many caches need to be generated on the first execution.

To be sure the installation succeeded, just open the following URL in your browser: <http://localhost:8000/>

After exploring Shopware 6, you can terminate it with these two commands:

1. Leave the shell:

```bash
exit
```

1. Stop the containers:

```bash
./psh.phar docker:stop
```

## Possibilities to use Docker on Mac

### Using native mounting with Docker volumes and docker-sync

If you are working with Mac/OSX and are facing performance issues, you should use [docker-sync](http://docker-sync.io/) instead of the default mounting strategy.

### Preparation

Download and install `docker-sync` from <http://docker-sync.io/>, which supports OSX, Windows, Linux, and FreeBSD. `docker-sync` uses Ruby, which is pre-installed on OSX. On other operating systems, you might have to [install Ruby](https://www.ruby-lang.org/en/) separately.

* For OSX, see [OSX](https://docker-sync.readthedocs.io/en/latest/getting-started/installation.html#installation-osx).
* For Windows, see [Windows](https://docker-sync.readthedocs.io/en/latest/getting-started/installation.html#installation-windows).
* For Linux, see [Linux](https://docker-sync.readthedocs.io/en/latest/getting-started/installation.html#installation-linux).
* See the list of alternatives [here](https://docker-sync.readthedocs.io/en/latest/miscellaneous/alternatives.html)

### Enable the use of docker-sync in PSH console

By default, the usage of `docker-sync` is disabled in PSH. To use Docker Volumes with Docker Sync, you must set `DOCKER_SYNC_ENABLED` to `true` in your `.psh.yaml.override`. Create a new entry in the `const` section like so:

```yaml
const:
  #..
  DOCKER_SYNC_ENABLED: true
```

That's it. Now, continue to install Shopware 6 as usual:

1. **Build and start the containers:**

```bash
./psh.phar docker:start
```

This command creates and starts the containers, watchers, and the sync itself. Running *start* for the first time takes several minutes to complete. Subsequent starts are a lot faster since the images and volumes are reused.

1. **Access the application container:**

```bash
./psh.phar docker:ssh
```

1. **Execute the installer inside the Docker container:**

```bash
./psh.phar install
```

For more information, look at Shopware [Installation Overview](../index.md#installation-overview).

## Next steps

As the next step, you might want to start writing your very own plugin. Refer to [Plugin base guide](../../plugins/plugins/plugin-base-guide) to learn about that topic.

Would you like to explore alternative ways to install Shopware? You can install Shopware on Mac with the help of [Dockware](../community/dockware).

---

---

## Installation from Scratch
**Source:** [guides/installation/legacy/from-scratch.md](https://developer.shopware.com/docs/v6.4/guides/installation/legacy/from-scratch.md)  
# Installation from Scratch

::: danger
This approach is no longer recommended. It is kept here as a reference.
:::

If it is *impossible* to get Docker up and running on your development environment, you can install Shopware 6 locally.

::: info
Be aware that this will be a vastly more complex solution since additional system requirements then need to be managed by you. However, you may experience better control over your local setup configuration.
:::

## Prerequisites

* A Linux-based operating system (Windows installation is not covered here, but notes are provided about installing within a WSL instance).
* An [Apache2 server installation](https://httpd.apache.org/docs/2.4/install.html) within the Linux-based operating system you have selected.
* Installation of all the required packages mentioned in the [Installation overview](../index.md#installation-overview). There are two main goals you need to accomplish.

Please note that this guide is based on plugin development and contribution. If you need a template for full composer-based shop projects, refer to the [production template](https://github.com/shopware/production).

## Setting up your web server

Firstly, we need to set up Apache to locate Shopware 6. If you wish, you could configure Nginx to serve your shopware installation, but this guide explains to you about Apache2 installation.

### VHost configuration

Firstly, you must add a vhost definition to your Apache site configuration.

* Create a file with the following pattern: `/etc/apache2/sites-available/*.conf`.
  Here we will create a file called `/etc/apache2/sites-available/shopware-install.conf`

* Within the created `shopware-install.conf` file, place the following configuration:

```text
<VirtualHost *:80>
   ServerName "HOST_NAME"
   DocumentRoot _DEVELOPMENT_DIR_/public

   <Directory _DEVELOPMENT_DIR_>
      Options Indexes FollowSymLinks MultiViews
      AllowOverride All
      Order allow,deny
      allow from all
      Require all granted
   </Directory>

   ErrorLog ${APACHE_LOG_DIR}/shopware-platform.error.log
   CustomLog ${APACHE_LOG_DIR}/shopware-platform.access.log combined
   LogLevel debug
</VirtualHost>
```

* Symlink the `shopware-install.conf` file to the Apache2 `sites-enabled` directory:

```shell
sudo ln -s /etc/apache2/sites-available/shopware-install.conf /etc/apache2/sites-enabled/shopware-install.conf
```

* Restart the Apache2 service to activate your new configuration:

```shell
# Your mileage with this command may vary depending on your chosen Linux operating system
sudo service apache2 restart
```

### Domain URL naming

When making an instance within an integration like [WSL](https://docs.microsoft.com/en-us/windows/wsl/about), special attention needs to be given to how you name the URL you use for local development. In the case of Shopware setup, it is advised to enable 'localhostForwarding' (allow requests to localhost to be forwarded to open ports within your active WSL instance). An example configuration in your [.wslconfig](https://docs.microsoft.com/en-us/windows/wsl/wsl-config#wslconfig) file could be:

```text
[wsl2]
memory=8GB
localhostForwarding=true # set this setting to true to be forwarded to WSL
processors=4
```

::: info
If your WSL instance is already running after making changes to your *.wslconfig* file, you will need to restart your WSL service with `wsl --shutdown`, then `wsl` for the config settings to take effect.
:::

Once `localhostForwarding` is enabled, you should update your local development domain name in you Apache2 `sites-available` config file as follows:

```text
xxxxxx.dev.localhost
```

...where 'xxxxxx' should be replaced with a 'hyphen/underscore separated' string.

::: info
Make sure the `APP_URL` variable defined within your `[PROJECT_ROOT]/.env` file matches the `ServerName` value within your Apache2 Vhost configuration
:::

### Apache2 server configuration

Make sure the following Apache modules are enabled:

* mod\_rewrite
* mod\_headers
* mod\_negotiation

::: info
Checking if these modules are installed on Apache is possible with the command `apachectl -M | grep [module_name]`. When searching for a specific module with `grep` make sure only to use the name suffix, such as "rewrite"
:::

After a quick restart of Apache, you are done.

::: info
For Mac (OSX) operating systems:

In your Apache config, it is recommended to move the document root folder to the user's `$HOME` folder to avoid permission issues. This is the folder which Apache looks to serve a file from. By default, the document root is configured as `/usr/local/var/www`.

As this is a development machine, let's assume you want to change the document root to point to a folder in your home directory. Search for the term "DocumentRoot" in your `httpd.conf` apache configuration, and you should see the following line:
:::

```bash
DocumentRoot "/usr/local/var/www"
```

Change this to point to your user directory where your\_user is the name of your user account:

```bash
DocumentRoot /Users/your_user/Sites/sw6/public
```

You also need to change the tag reference right below the "DocumentRoot" line. This should also be changed to point to your new document root:

```text
<Directory "/Users/your_user/Sites/sw6/public">
```

Within your Apache configuration, you must set your `DocumentRoot` and `Directory` directive to the **public/** folder of your sw6 installation root. Otherwise, apache2 **will not** successfully find your `index.php` file and serve the site.

## Setting up Shopware

Before you set up Shopware, you need to clone our Shopware repositories from version control. This is explained in the "Preparatory steps" paragraph of the [Installation overview](../index.md#installation-overview).

### Starting Shopware installation

A simple CLI installation wizard can be invoked by executing the following:

```bash
bin/setup
```

Now, Shopware 6 is installed. To be sure the installation succeeded, just open the configured host URL in your favorite browser.

## Updating the repositories

It is important to keep the `platform` and the `development` repository in sync.

The following steps should always yield a positive result:

```bash
git pull
cd platform
git pull
cd ..
composer update
rm -R var/cache/*
./psh.phar install
```

::: warning
Note that this will reset your database.
:::

## Next steps

Now that you got a running Shopware installation, why not start with your first very own plugin? Refer to the [Plugin base guide](../../plugins/plugins/plugin-base-guide) for a good starting point.

---

---

## MAMP
**Source:** [guides/installation/legacy/mamp.md](https://developer.shopware.com/docs/v6.4/guides/installation/legacy/mamp.md)  
# MAMP

::: danger
This approach is no longer recomended. It is kept here as a reference.
:::

## Overview

For quick and easy installation, you can also use **MAMP** on Mac.

## Prerequisites

As a first step, make sure you installed MAMP beforehand. You can download MAMP on [this site](https://www.mamp.info/en/downloads/).

## Preparation

### Configure PHP settings

First, you have to modify the PHP settings inside MAMP, as seen in the following screenshot:

![PHP settings](../../../.gitbook/assets/10-mac-os-x-php.png)

Next, start the mysql webserver-service with the toggle buttons on the left side in the MAMP management console.

### Prepare MySQL user and database

* Open the **MySQL Tab** on the left side and click on the *PhpMyAdmin* icon. In case the icon is grayed out, check if the mysql and webserver services are running.

![Mysql settings](../../../.gitbook/assets/10-mac-os-x-mysql.png)

* Inside PhpMyAdmin, switch to the user account management on the top menu and click *add new user*.

* Choose a username (e.g., shopware) and a password and set the option *Create database with same name and grant all privileges*. Set the option *Check all* in the **Global privileges** card. Also, all checkboxes in this card should be checked.

* Finish this step by clicking *GO*.

### Global usage

Next, you must ensure MAMP php binary is used globally on your CLI. Therefore, execute the following commands:

```bash
which php
# /Applications/MAMP/bin/php/php7.2.14/bin/php &lt; should be displayed
# IF NOT
vim ~/.bash_profile
export PATH=/Applications/MAMP/bin/php/php7.2.14/bin:$PATH
# :wq to save the file
source ~/.bash_profile
```

::: info
The folder used in `PATH` (`PATH=/Applications/MAMP/bin/php/php7.2.14/bin:$PATH`) may change. Please look in the `php` folder for its current name.
:::

Then you need to make sure MAMP mysql binary is used globally on your CLI:

```bash
which mysql
# /Applications/MAMP/Library/bin/mysql &lt; should be displayed
# IF NOT
vim ~/.bash_profile
export PATH=/Applications/MAMP/Library/bin:$PATH
# :wq to save the file
source ~/.bash_profile
```

### Install `brew`

It is handy to use brew as a package manager. So we recommend you install brew. Please open the terminal application again and run the command stated below:

```bash
/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
```

### Install npm / node

The next step is installing NodeJS and NPM. Therefore you need to leave the terminal application open and use brew to install the node:

```bash
brew install node@12
```

### Install Composer

To install Composer, please open the terminal application and execute the following command:

```bash
brew install composer
```

## Checkout Shopware

Before you are able to set up Shopware, you need to checkout Shopware's repositories. This is explained in the "Preparatory steps" of the [Installation overview](../index.md#installation-overview).  guide. Nevertheless, below you see a brief summary of this process:

```bash
# Choose your own directory
cd ~/PhpstormProjects/
mkdir shopware
cd shopware
git clone https://github.com/shopware/development.git
cd development
git clone https://github.com/shopware/platform.git
```

## Shopware 6 setup in MAMP

First, add a new host in MAMP:

* Hostname = shopware
* Port = 8000
* Document Root = Browse for the public directory inside the new directory that you used before (e.g.,/PhpstormProjects/shopware/development/public)

![hosts](../../../.gitbook/assets/10-mac-os-x-net.png)

As a next step, change the installation settings:

```bash
# Inside the shopware installation directory (e.g.  /PhpstormProjects/shopware/development)
bin/setup
```

You will be prompted to enter specific information. In short:

* **Application environment**: Just hit enter to apply the default `dev`.
* **URL to your /public folder**: `http://shopware:8000`.
* **Database host**: Just hit enter to apply the default `localhost`.
* **Database port**: Just hit enter to apply the default `3306`.
* **Database name**: Enter the name of your database that you created earlier, `shopware` was suggested.
* **Database user**: Enter the name of your MySQL user that you created previously.
* **Database password**: Enter the password of the new MySQL user.

Afterwards a file called `.psh.yaml.override` is created, which contains all the information you just entered.

### Start Shopware 6 setup

```bash
# Inside the shopware installation directory (e.g. /PhpstormProjects/shopware/development) 
./psh.phar install
```

After that the setup is done. You can now access your Shopware 6 installation using the following URLs:

* **Storefront**: <http://shopware:8000>
* **Admin**: <http://shopware:8000/admin> (User: admin, password: shopware)

## Troubleshooting

There are cases when the Administration is not built correctly and has error messages similar to these:

> ERROR in foobar/vendor/shopware/storefront/Resources/app/administration/src/main.js Module Error (from ./node\_modules/eslint-loader/index.js):
>
> ✘ <https://google.com/#q=import%2Fno-unresolved> Casing of ./modules/sw-theme-manager does not match the underlying filesystem\
> foobar/vendor/shopware/storefront/Resources/app/administration/src/main.js:1:8
>
> ✘ <https://google.com/#q=import%2Fno-unresolved> Casing of ./extension/sw-sales-channel/page/sw-sales-channel-detail does not match the underlying filesystem\
> foobar/vendor/shopware/storefront/Resources/app/administration/src/main.js:3:8
>
> ✘ <https://google.com/#q=import%2Fno-unresolved> Casing of ./extension/sw-sales-channel/view/sw-sales-channel-detail-theme does not match the underlying filesystem\
> foobar/vendor/shopware/storefront/Resources/app/administration/src/main.js:4:8
>
> ✘ <https://google.com/#q=import%2Fno-unresolved> Casing of ./init/api-service.init does not match the underlying filesystem\
> foobar/vendor/shopware/storefront/Resources/app/administration/src/main.js:6:8

The underlying problem is that Mac supports case-insensitive paths but not the tools that build the administration. Therefore, make sure to execute the commands in a context where the `pwd` is written in the correct case.

✅ Ok: `/Users/shopware/Code/shopware-platform`

❌ Not ok: `/users/shopware/code/Shopware-Platform`

## Next steps

As you successfully installed Shopware, you may want to start writing your own plugin. Head over to [Plugin base guide](../../plugins/plugins/plugin-base-guide) to get a grip on that topic.

---

---

## Valet+
**Source:** [guides/installation/legacy/valet.md](https://developer.shopware.com/docs/v6.4/guides/installation/legacy/valet.md)  
# Valet+

::: danger
This approach is no longer recomended. It is kept here as a reference.
:::

## Overview

Valet+ is a fork of [laravel/valet](https://github.com/laravel/valet). It supports automatic virtual host configuration based on the folder structure.

This is a modified version of the [official Installation Guide](https://github.com/weprovide/valet-plus/wiki/Installation).

## Prerequisites

Before proceeding with this guide, have a look at [Installation overview](../index.md#installation-overview). Also, your system should be running [brew](https://brew.sh/) and [Composer](https://getcomposer.org/) already.

## If you have Valet installed

Run `composer remove laravel/valet`.

## Installing Valet-PHP

* Update Homebrew via `brew update`.
* Add the Homebrew PHP tap for Valet+ via `brew tap henkrehorst/php`.
* Install PHP 7.4 using Homebrew via `brew install valet-php@7.4`.
* Link your PHP version using the `brew link valet-php@7.4 --force` command.

## Installing Valet+

* If needed, install Composer via `brew install composer`.
* Install Valet+ via `composer global require weprovide/valet-plus`.
* Make sure `~/.composer/vendor/bin` is in your path by adding `export PATH="$PATH:$HOME/.composer/vendor/bin"` to your `bash_profile` or `.zshrc`.
* Check for the following common problem with `valet fix`.
* The above instruction will uninstall all other PHP installations. Now, run the `valet install` command. Optionally add `--with-mariadb` to use MariaDB instead of MySQL. This will configure and install Valet+ and DnsMasq.

Additionally, it registers Valet's daemon to launch when your system starts.

## Using Valet+ with Shopware 6

* Create a new empty folder, for example `~/sites`.
* Clone the development template like you normally would (dev + platform) into this folder.
* Adjust params installation editing `.psh.yaml.dist`.
* Run `./psh.phar install`.
* Move to `~/sites` and run `valet park` to register Valet for this directory. Shopware should now be accessible via the `folder-name.test`. This "folder-name" is the name of the Shopware development template in `~/sites`.
* Optional: Disable SSL via `valet unsecure` because this might cause problems with the watcher.

## Troubleshooting

### Testing your installation

* Make sure `ping something.test` responds from 127.0.0.1.
* Run `nginx -t` or `sudo nginx -t` and check for any errors. If there is a missing *elastisearch* file, follow the "Missing Elasticsearch stub fix" further below.

### Install Error: "*The process has been signaled with signal 9*"

This is due to `valet fix` uninstalling `valet-php@7.4` for some reason. You can fix it by reinstalling Valet-PHP (Step 3 and 4 of "Installing Valet-PHP"). Make sure to **NOT** run `valet fix` afterwards and just proceed with `valet install`.

### Missing Elasticsearch stub fix

```bash
sudo cp ~/.composer/vendor/weprovide/valet-plus/cli/stubs/elasticsearch.conf /usr/local/etc/nginx/valet/elasticsearch.conf
```

```bash
valet domain test
```

### Watchers not working

Try disabling SSL via `valet unsecure`.

## Next steps

Now that you have a running Shopware 6 instance, you can create your first plugin. Refer to [Plugin base guide](../../plugins/plugins/plugin-base-guide) for more information.

---

---

## Requirements
**Source:** [guides/installation/requirements.md](https://developer.shopware.com/docs/v6.6/guides/installation/requirements.md)  
# Requirements

Before installing Shopware 6, take a quick look at the requirements below to check if your local environment is capable of running it.

## Operating System

Shopware 6 is currently only supported on any Unix operating system. Windows is only supported inside WSL 2 or Docker.

## Versions

You can use these commands to check your actual environment:

::: info
On many shared hosting environments, you have multiple PHP versions installed. Make sure that you use the correct PHP binary and often CLI and FPM have different `php.ini` files. Ask your hosting provider for the correct PHP binary to use and how to change the `php.ini` file.
:::

* `php -v`: Shows CLI PHP version
* `php -m`: Shows CLI PHP modules
* `php -i | grep memory_limit`: Shows your actual CLI PHP memory limit
* `composer -V`: Shows your actual composer version
* `node -v`: Shows your actual Node version
* `npm -v`: Shows your actual NPM version

### PHP

* Compatible version: 8.2, 8.3 and 8.4
* `memory_limit` : 512M minimum
* `max_execution_time` : 30 seconds minimum
* Extensions:
  * `ext-amqp` (only required if you plan to use a message queue, which is the default on PaaS)
  * `ext-curl`
  * `ext-dom`
  * `ext-fileinfo`
  * `ext-gd`
  * `ext-iconv`
  * `ext-intl`
  * `ext-mbstring`
  * `ext-openssl`
  * `ext-pcre`
  * `ext-pdo`
  * `ext-pdo_mysql`
  * `ext-phar`
  * `ext-simplexml`
  * `ext-xml`
  * `ext-zip`
  * `ext-zlib`
* Composer recommended version: 2.2 or higher

This is how you install PHP and Composer:

Add a new software repository to your system to have the latest PHP version.

```bash
sudo add-apt-repository ppa:ondrej/php

sudo apt-get install -y php8.3-fpm php8.3-mysql php8.3-curl php8.3-gd php8.3-xml php8.3-zip php8.3-opcache php8.3-mbstring php8.3-intl php8.3-cli

sudo wget https://getcomposer.org/download/latest-stable/composer.phar -O /usr/local/bin/composer
sudo chmod +x /usr/local/bin/composer
```

Add a new software repository to your system to have the latest PHP version:

```bash
sudo apt-get install extrepo
sudo extrepo enable sury

sudo apt-get update
sudo apt-get install -y php8.3-fpm php8.3-mysql php8.3-curl php8.3-gd php8.3-xml php8.3-zip php8.3-opcache php8.3-mbstring php8.3-intl php8.3-cli

sudo wget https://getcomposer.org/download/latest-stable/composer.phar -O /usr/local/bin/composer
sudo chmod +x /usr/local/bin/composer
```

```bash
brew install php@8.3 composer
```

### SQL

* MySQL

  * Recommended version: 8.4
  * Minimum version: 8.0.22

* MariaDB

  * Recommended version: 11.4
  * Minimum version : 10.11.6 or 11.0.4

For optimal MySQL performance, it is advisable to set `max_allowed_packet` to a minimum of 32 MB.

This is how you install MariaDB:

```bash
sudo apt install -y mariadb-server
```

The easiest way is to use [Homebrew](https://brew.sh/):

```bash
brew install mariadb
```

### JavaScript

* Node.js 22.0.0 or higher

This is how you install Node.js:

```bash
curl -fsSL https://deb.nodesource.com/setup_22.x -o nodesource_setup.sh
sudo -E bash nodesource_setup.sh

sudo apt-get install -y nodejs
```

```bash
brew install node@22
```

## Redis or key/value stores

Shopware uses the Redis Protocol and, therefore, supports the following key/value stores:

* [Valkey (recommended)](https://valkey.io/)

* [Redis v7 or higher](https://redis.io)

* [Redict](https://redict.io)

* [KeyDB](https://docs.keydb.dev)

* [Dragonfly](https://www.dragonflydb.io)

* Recommended configuration `maxmemory-policy`: `volatile-lfu`

## Webserver

To run Shopware in a development context, the [Symfony CLI](https://symfony.com/doc/current/setup/symfony_server.html) will work nicely.

## Recommended stack

We recommend the following stack:

* Webserver: Caddy
* PHP: 8.4
* SQL: MariaDB 11.4
* Node: 22
* Search: OpenSearch 2.17.1
* Queue: RabbitMQ
* Cache: Valkey 8.0

Recommended PHP ini:


## Setup

Once the requirements are fulfilled, follow up with the [Template](template) guide to set up Shopware.

---

---

## Setups
**Source:** [guides/installation/setups.md](https://developer.shopware.com/docs/v6.6/guides/installation/setups.md)  
# Setups

## Set up your own environment

Head over to the [Requirements](../requirements) section to install and configure the necessary services like a database and a webserver to a Unix system like Linux, macOS, WSL, etc.

## Development setup

::: info
Technically there is no real difference between a Development Setup and a Production Setup, they only differ on performance and security optimizations.
:::

* [Docker](docker) (beginner-friendly) - This is a Docker setup for Shopware 6. It is a lightweight and easy way to get started with Shopware. It uses Docker Compose to manage the services and is suitable for local development.

* [Symfony CLI](symfony-cli) - This setup uses the Symfony CLI to run Shopware. It is the default way to run Symfony applications and is also suitable for Shopware.

* [Devenv](devenv) - This is a setup that manages all necessary services. A description file in the source code manages the versions of these services. This setup works for Linux, WSL, and macOS.

* [Dockware\*](https://dockware.io/getstarted) - This is a managed docker setup for Shopware 6 by Shopware agency [dasistweb](https://www.dasistweb.de/).

* [DDEV\*](https://notebook.vanwittlaer.de/ddev-for-shopware/less-than-5-minutes-install-with-ddev-and-symfony-flex) - Docker-based PHP development environments, works on all platforms and is generic enough to be used for any PHP project. [Project Page](https://ddev.com/)

> \* These setups are maintained by the community and not directly by Shopware. If you have any questions or issues, please open an issue in the respective repository.

## Production setup

### Managed hosting

Many hosting providers, especially Shopware certified ones, offer a fully pre-configured Hosting environment for Shopware. This is the easiest way to get started with Shopware. You can find a list of certified hosting partners on the [Shopware website](https://www.shopware.com/en/partner/hosting/). You will need to upload your [Shopware project template](./template.md) to the server and run the installation commands.

If you want to automate the installation process, consider using [Deployer](https://deployer.org/) to deploy the code changes. You can find here the [Deployer documentation](../hosting/installation-updates/deployments/deployment-with-deployer.md).

### Container-based hosting

If you are using containers for your setup, check out the dedicated [Docker guide for production](../hosting/installation-updates/docker.md). This guide will help you to set up a production ready Docker environment for Shopware 6.

If you are using Kubernetes, take a look at the [Shopware Kubernetes Operator](https://github.com/shopware/shopware-operator).

---

---

