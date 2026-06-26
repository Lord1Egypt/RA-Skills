# PRODUCT EXTENSIONS OVERVIEW

Compiled excerpts from the Shopware Developer Documentation snapshot. Prefer live docs at [developer.shopware.com](https://developer.shopware.com/) when in doubt.

---

## Create a product with a new media
**Source:** [assets/adr/catalog-import/examples.md](https://developer.shopware.com/docs/v6.6/assets/adr/catalog-import/examples.md)  
::: info
This document represents an architecture decision record (ADR) and has been mirrored from the ADR section in our Shopware 6 repository.
You can find the original version [here](https://github.com/shopware/shopware/blob/trunk/adr/assets/catalog-import/examples.md)
:::

### Create a product with a new media

```http
POST http://localhost:8000/api/import/{{import_id}}/record
Content-Type: application/json
Accept: application/json
Authorization: Bearer {{auth_token}}

{
    "products": [
        {
            "id": "018a6b222b5a734d956fb03dda765bfa",
            "name": "My product via API",
            "productNumber": "PRODNUMAPI1",
            "tax": {
                "name": "Reduced rate 2"
            },
            "prices": [
                {
                    "currency": "EUR",
                    "gross": 10,
                    "net": 20,
                    "linked": false
                }
            ],
            "media": [
                {
                    "url": "https://images.unsplash.com/photo-1660236822651-4263beb35fa8?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1170&q=80",
                    "title": "pommes",
                    "alt": "alt",
                    "filename": "pommes.jpg"
                }
            ]
        }
    ]
}
```

### Update a product and update its media

```http
POST http://localhost:8000/api/import/{{import_id}}/record
Content-Type: application/json
Accept: application/json
Authorization: Bearer {{auth_token}}

{
    "media": [
        {
            "id": "018a6b222b5a734d956fb03dda765bfb",
            "title": "New title"
        }
    ],
    "products": [
        {
            "id": "018a6b222b5a734d956fb03dda765bfa",
            "name": "My update product"
        }
    ]
}
```

### Delete a product and media

```http
POST http://localhost:8000/api/import/{{import_id}}/record/delete
Content-Type: application/json
Accept: application/json
Authorization: Bearer {{auth_token}}
{
    "products": [
        "018a6b222b5a734d956fb03dda765bfa"
    ],
    "media": [
        "018a6b222b5a734d956fb03dda765bfb"
    ]
}
```

### Create a product with a custom entity

```http
POST http://localhost:8000/api/import/{{import_id}}/record
Content-Type: application/json
Accept: application/json
Authorization: Bearer {{auth_token}}

{
  "products": [
    {
      "id": "018a6b222b5a734d956fb03dda765bfa",
      "name": "My product via API",
      "productNumber": "PRODNUMAPI1",
      "tax": {
        "name": "Reduced rate 2"
      },
      "prices": [
        {
          "currency": "EUR",
          "gross": 10,
          "net": 20,
          "linked": false
        }
      ],
      "extensions": {
        "myCustomEntity": {
          "id": "018a6b222b5a734d956fb03dda765bf8",
          "name": "foo"
        }
      }
    }
  ]
}
```

### Update a custom entity

```http
POST http://localhost:8000/api/import/{{import_id}}/record
Content-Type: application/json
Accept: application/json
Authorization: Bearer {{auth_token}}

{
    "extensions": {
        "myCustomEntity": [
          {
            "id": "018a6b222b5a734d956fb03dda765bf8",
            "name": "bar"
          }
        ]
    },
    "products": [
        {
            "id": "018a6b222b5a734d956fb03dda765bfa",
            "name": "My update product"
        }
    ]
}
```

### Create a category and assign products to it

```http
POST http://localhost:8000/api/import/{{import_id}}/record
Content-Type: application/json
Accept: application/json
Authorization: Bearer {{auth_token}}

{
    "categories": [
        {
            "name": "Category 1",
            "parent": [
                "Home",
                "Category 2",
                "Category 3"
            ],
            "products": [
                {
                    "id": "prod1d1"
                },
                {
                    "id": "prod1d2"
                }
            ]
        }
    ]
}
```

### Un-assign a media from a product

```http
POST http://localhost:8000/api/import/{{import_id}}/record/unassign
Content-Type: application/json
Accept: application/json
Authorization: Bearer {{auth_token}}

{
    "products": {
        "id": "productId",
        "media": [
            {
                "id": "mediaId1"
            },
            {
                "filename": "pommes.jpg"
            }
        ]
    }
}
```

### Error Response: Resolving Root Entities

Scenario: Updating a product which does not exist

Request

```http
POST http://localhost:8000/api/import/{{import_id}}/record
Content-Type: application/json
Accept: application/json
Authorization: Bearer {{auth_token}}

{
    "products": [
        {
            "id": "018a6b222b5a734d956fb03dda765bfa",
            "productNumber": "PRODNUMAPI1",
        }
    ]
}
```

Response

```json
{
    "containsErrors": true,
    "records": [
        {
            "errors": [
                {
                    "message": "ID 018a6b222b5a734d956fb03dda765bfa not found",
                    "path": "products.0"
                }
            ]
        }
    ]
}
```

### Error Response: Resolving Nested Entities

Scenario: Product with ID `prod1d1` does not exist

Request

```http
POST http://localhost:8000/api/import/{{import_id}}/record
Content-Type: application/json
Accept: application/json
Authorization: Bearer {{auth_token}}

{
    "categories": [
        {
            "name": "Category 1",
            "parent": [
                "Home",
                "Category 2",
                "Category 3"
            ],
            "products": [
                {
                    "id": "prod1d1"
                },
                {
                    "id": "prod1d2"
                }
            ]
        }
    ]
}
```

Response

```json
{
    "containsErrors": true,
    "records": [
        {
            "id" : "c642f3515aff4783991e361f381e77ca",
            "errors": [
                {
                    "message": "ID prod1d1 not found",
                    "path": "categories.0.products.1"
                },
                {
                    "message": "ID prod1d2 not found",
                    "path": "categories.0.products.2"
                }
            ]
        }
    ]
}
```

### Error Response Status Root

Scenario: Create a product, productNumber is not unique

Request

```http
POST http://localhost:8000/api/import/{{import_id}}/record
Content-Type: application/json
Accept: application/json
Authorization: Bearer {{auth_token}}

{
    "products": [
        {
            "id": "018a6b222b5a734d956fb03dda765bfa",
            "name": "My product via API",
            "productNumber": "PRODNUMAPI1",
            "tax": {
                "name": "Reduced rate 2"
            },
            "prices": [
                {
                    "currency": "EUR",
                    "gross": 10,
                    "net": 20,
                    "linked": false
                }
            ],
        }
    ]
}
```

Response

```json
{
    "status": "done",
    "startTime": "25/12/2024",
    "duration": "10",
    "totals": {
        "product": 2,
        "media": 1,
        "total": 3,
        "failures": 1
    },
    "failures": [
        {
            "entity": "product",
            "path": "products.0",
            "details": [
                {
                    "severity": "error",
                    "entity": "product",
                    "path": "products.0",
                    "message": "Product number is not unique"
                }
            ]
        }
    ]
}
```

### Error Response Status Nested

Scenario: Create a product with a media, media fails to download

Request

```http
POST http://localhost:8000/api/import/{{import_id}}/record
Content-Type: application/json
Accept: application/json
Authorization: Bearer {{auth_token}}

{
    "products": [
        {
            "id": "018a6b222b5a734d956fb03dda765bfa",
            "name": "My product via API",
            "productNumber": "PRODNUMAPI1",
            "tax": {
                "name": "Reduced rate 2"
            },
            "prices": [
                {
                    "currency": "EUR",
                    "gross": 10,
                    "net": 20,
                    "linked": false
                }
            ],
            "media": [
                {
                    "url": "https://images.unsplash.com/photo-1660236822651-4263beb35fa8?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1170&q=80",
                    "title": "pommes",
                    "alt": "alt",
                    "filename": "pommes.jpg"
                }
            ]
        }
    ]
}
```

Response

```json
{
    "status": "done",
    "startTime": "25/12/2024",
    "duration": "10",
    "totals": {
        "product": 2,
        "media": 1,
        "total": 3,
        "failures": 1
    },
    "failures": [
        {
            "entity": "product",
            "path": "products.0",
            "details": [
                {
                    "severity": "error",
                    "entity": "product",
                    "path": "products.0",
                    "message": "Images could not be downloaded"
                },
                {
                    "severity": "error",
                    "entity": "media",
                    "path": "products.0.media.0",
                    "message": "Image %s could not be downloaded"
                },
                {
                    "severity": "error",
                    "entity": "media",
                    "path": "products.0.media.1",
                    "message": "Image %s could not be downloaded"
                }
            ]
        }
    ]
}
```

---

---

## Shopware CLI
**Source:** [products/cli.md](https://developer.shopware.com/docs/v6.6/products/cli.md)  
# Shopware CLI

Shopware CLI is an open-source external command-line interface for Shopware 6. It provides a set of commands to interact with your Shopware instance, build extensions, dump databases, and more. The CLI **is an extra tool** and needs to be set up separately from your Shopware instance.

The CLI consists of three command scopes:

* Project commands: Commands to interact with your Shopware project
* Extension commands: Commands to build Shopware extensions
* Store commands: Commands to publish extensions to the Shopware Store or update

If you want to use the CLI, you need to [install it first](installation.md) or take a look at each area of the CLI.

---

---

## Automatic refactoring
**Source:** [products/cli/automatic-refactoring.md](https://developer.shopware.com/docs/v6.6/products/cli/automatic-refactoring.md)  
# Automatic refactoring

Shopware-CLI comes with a built-in automatic refactoring tool for PHP, JavaScript, and Admin Twig files.

It uses the tools:

* [Rector](https://getrector.org/) for PHP
* [ESLint](https://eslint.org/) for JavaScript
* Custom rules for Admin Twig files

## Refactoring an extension

::: warning
Make sure you have a copy of your extension before running the command, as it will change your files!
:::

```shell
shopware-cli extension fix /path/to/your/extension
```

```shell
docker run --rm -v $(pwd):/ext shopware/shopware-cli extension fix /ext
```

## Refactoring an entire project

```shell
shopware-cli project fix /path/to/your/project
```

```shell
docker run --rm -v $(pwd):/ext shopware/shopware-cli project fix /project
```

This will execute Rector and ESLint to refactor your code. You should review the changes made and decide whether you want to keep them or not.

Make sure that you have adjusted the `shopware/core` requirement in the `composer.json` file of your extension to the version you want to upgrade to. It will use the lowest supported version your Composer constraint is compatible with.

## Experimental Twig upgrade using Large Language Models

The Extension Verifier also includes an experimental feature to upgrade your Twig templates using Large Language Models (LLMs). This feature is experimental and should only be executed on code that is versioned in Git or similar.
To use this feature, you can run the following command:

```shell
shopware-cli extension ai twig-upgrade /ext 6.6.0.0 6.7.0.0-rc1 --provider gemini --model gemini-2.5-pro-exp-03-25
```

```shell
docker run --rm -v $(pwd):/ext shopware/shopware-cli extension ai twig-upgrade /ext 6.6.0.0 6.7.0.0-rc1 --provider gemini --model gemini-2.5-pro-exp-03-25
```

Extension Verifier currently supports multiple providers:

* `gemini` - Google Gemini LLM (requires `GEMINI_API_KEY` environment variable)
* `openrouter` - OpenRouter API (requires `OPENROUTER_API_KEY` environment variable)
* `ollama` - Local Ollama (uses localhost by default, `OLLAMA_HOST` environment variable can be used to specify a different host)

Our recommendation is to use Google Gemini 2.5 Pro, as it provides the best results for the upgrade.

---

---

## Standalone Admin Watcher
**Source:** [products/cli/extension-commands/admin-watcher.md](https://developer.shopware.com/docs/v6.6/products/cli/extension-commands/admin-watcher.md)  
# Standalone Admin Watcher

::: info
`shopware-cli extension admin-watch` can be different to the regular Admin Watcher. You can start the regular Admin Watcher with `shopware-cli project admin-watch`
:::

Shopware CLI has an integrated Standalone Admin Watcher. This is useful if the regular Admin Watcher struggles with the number of installed extensions, and you only want to watch one single extension. The Standalone Watcher works by using the regular build Administration and injects only the changed files of the extension.

Therefore, the Watcher starts in few milliseconds and is very fast. Additionally, it can be targeted to an external Shopware 6 Instance to debug JavaScript or CSS changes with the external data.

## Starting the Standalone Admin Watcher

To start the Standalone Admin Watcher, you can use the following command:

```bash
shopware-cli extension admin-watch <path-to-extension> <url-to-shopware>
```

The first parameter is the **path to extension** you want to watch and the last parameter is the URL to the Shopware 6 instance. The URL must be reachable from the machine where the CLI is executed. You can watch also multiple extensions by providing multiple paths, but the last parameter must be the URL to the Shopware 6 instance.

You can also pass **path of a Shopware project** to the command. In this case, the CLI will automatically detect the extensions.

The listing port of the Admin Watcher can be changed with `--listen :<port>`.

## Usage behind a proxy

If you want to use the Standalone Admin Watcher behind a proxy, for example, SSL, you should set `--external-url` to the URL where the Admin Watcher will be reachable in the Browser.

---

---

## Building extensions and creating archives
**Source:** [products/cli/extension-commands/build.md](https://developer.shopware.com/docs/v6.6/products/cli/extension-commands/build.md)  
# Building extensions and creating archives

Extensions consist of PHP Changes, JavaScript and CSS. To release an extension to the Shopware Store or upload it to a Shopware 6 instance without having to rebuild Storefront and Administration, your extension needs to provide the compiled assets.

## Building an extension

Shopware CLI allows you to easily build the assets of an extension. To build an extension, you can use the following command:

```bash
shopware-cli extension build <path>
```

Shopware CLI reads the `shopware/core` requirement from `composer.json` or `manifest.xml` and builds the assets using the lowest compatible Shopware version. This ensures the extension remains usable across multiple Shopware versions. If the selected version is incorrect, you can override it using a `.shopware-extension.yml` file.

```yaml
# .shopware-extension.yml
build:
  shopwareVersionConstraint: '6.6.9.0'
```

This only affects the build process and not on the installation of the extension. For full control you can also specify the environment variable `SHOPWARE_PROJECT_ROOT` pointing to a Shopware 6 project, and it will use that Shopware to build the extension assets.

## Additional bundles

If your plugin consists of multiple bundles, usually when you have implemented `getAdditionalBundles` in your `Plugin` class, you have to provide the path to the bundle you want to build in the config:

```yaml
# .shopware-extension.yml
build:
  extraBundles:
    # Assumes the bundle name is the same as the directory name
    - path: src/Foo
    # Explicitly specify the bundle name
    - path: src/Foo
      name: Foo
```

## Extension as bundle

If your extension is not a plugin but itself a bundle, make sure your composer type is `shopware-bundle` and that you have set a `shopware-bundle-name` in the `extra` part of the composer definition like this:

```json
{
    "name": "my-vendor/my-bundle",
    "type": "shopware-bundle",
    "extra": {
        "shopware-bundle-name": "MyBundle"
    }
}
```

Now you can use `shopware-cli extension build <path>` to build the assets and distribute them together with your bundle.
Also `shopware-cli project ci` detects know automatically this bundle and builds the assets for it.

## Using esbuild for JavaScript Bundling

::: warning
Building with esbuild works completely standalone without the Shopware codebase. This means if you import files from Shopware, you have to copy it to your extension.
:::

Esbuild can be used for JavaScript bundling, offering a significantly faster alternative to the standard Shopware bundling process, as it eliminates the need to involve Shopware for asset building.

```yaml
# .shopware-extension.yml
build:
  zip:
    assets:
      # Use esbuild for Administration
      enable_es_build_for_admin: true
      # Use esbuild for Storefront
      enable_es_build_for_storefront: true
```

## Creating an archive

To create an archive of an extension, you can use the following command:

```bash
shopware-cli extension zip <path>
```

The command copies the extension to a temporary directory, builds the assets, deletes unnecessary files and creates a zip archive of the extension. The archive is placed in the current working directory.

**By default, the command picks the latest released git tag**, use the `--disable-git` flag to disable this behavior and use the current source code. Besides disabling it completely, you can also specify a specific tag or commit using `--git-commit`.

### Bundling composer dependencies

Before Shopware 6.5, bundling the composer dependencies into the zip file is required. Shopware CLI automatically runs `composer install` and removes duplicate composer dependencies to avoid conflicts.

To disable this behavior, you can adjust the configuration:

```yaml
# .shopware-extension.yml
build:
  zip:
    composer:
      enabled: false
```

This is automatically disabled for plugins targeting Shopware 6.5 and above and `executeComposerCommands` should be used instead.

### Delete files before zipping

Shopware CLI deletes a lot of known files before zipping the extension. If you want to delete more files, you can adjust the configuration:

```yaml
# .shopware-extension.yml
build:
  zip:
    pack:
      excludes:
        paths:
          - <path>
```

### JavaScript Build optimization

If you bring additional NPM packages, make sure that you added only runtime dependencies to `dependencies` inside `package.json` and tooling to `devDependencies` and enabled `npm_strict` in the configuration:

```yaml
# .shopware-extension.yml
build:
  zip:
    assets:
      npm_strict: true
```

This skips unnecessary `npm install` and `npm ci` commands and only installs the runtime dependencies.

### Release mode

If you are building an archive for distribution, you can enable the release mode with the flag `--release`. This will remove the App secret from the `manifest.xml` and generate changelog files if enabled.

The changelog generation can be enabled with the configuration:

```yaml
# .shopware-extension.yml
changelog:
  enabled: true
```

It generates the changelog by utilizing the commits between the last tag and the current commit. Additionally, it can be configured to filter commits and build the changelog differently.

```yaml
changelog:
  enabled: true
  # only the commits matching to this regex will be used
  pattern: '^NEXT-\d+'
  # variables allow extracting metadata out of the commit message
  variables:
    ticket: '^(NEXT-\d+)\s'
  # go template for the changelog, it loops over all commits
  template: |
    {{range .Commits}}- [{{ .Message }}](https://issues.shopware.com/issues/{{ .Variables.ticket }})
    {{end}}
```

This example checks that all commits in the changelog needs to start with `NEXT-` in the beginning. The `variables` section allows extracting metadata out of the commit message. The `template` is a go template which loops over all commits and generates the changelog.
With the combination of `pattern`, `variables` and `template` we link the commit message to the Shopware ticket system.

### Overwrites

Extension configuration can be overwritten during the zipping process, allowing changes to aspects such as the version and app-related settings.

Replaces the version in `composer.json` or `manifest.xml` with the given version:

```yaml
shopware-cli extension zip --overwrite-version=1.0.0 <path>
```

Replaces all external URLs in `manifest.xml` to that given URL:

```yaml
shopware-cli extension zip --overwrite-app-backend-url=https://example.com <path>
```

Replaces the App secret in `manifest.xml` with the given secret:

```yaml
shopware-cli extension zip --overwrite-app-backend-secret=MySecret <path>
```

---

---

## Configuration
**Source:** [products/cli/extension-commands/configuration.md](https://developer.shopware.com/docs/v6.6/products/cli/extension-commands/configuration.md)  
# Configuration

Many configurations can be changed using a `.shopware-extension.yml` file in the root of your extension.

Here is an example of a `.shopware-extension.yml` file:

```yaml
build:
  extraBundles:
    - path: src/Foo
    - name: OverrideName
      path: src/Override
  shopwareVersionConstraint: '~6.6.0'
  zip:
    assets:
      enabled: false
      before_hooks: []
      after_hooks: []
      disable_sass: false
      enable_es_build_for_admin: false
      enable_es_build_for_storefront: false
      npm_strict: false

changelog:
  enabled: true

store:
  automatic_bugfix_version_compatibility: true
  # ...

validation:
  ignore:
    - 'xx'
```

When you edit that file in an editor, you will get autocompletion and hints for the available options.

## Environment variables

Additionally, you can set environment variables to change the behavior of the CLI. The following environment variables are available:

| Environment Variable            | Description                                                                           |
|---------------------------------|---------------------------------------------------------------------------------------|
| CI                              | Detect CI environment                                                                 |
| SHOPWARE\_CLI\_PREVIOUS\_TAG       | Override previous Git tag detection with a previous tag used for Changelog generation |
| CI\_PROJECT\_URL                  | GitLab CI project URL used for Changelog generation                                   |
| SHOPWARE\_CLI\_NO\_SYMFONY\_CLI     | Disable Symfony CLI usage                                                             |
| APP\_ENV                         | Application environment                                                               |
| SHOPWARE\_PROJECT\_ROOT           | Use this Shopware project to build the extension instead of setting up a new project  |
| SHOPWARE\_CLI\_DISABLE\_WASM\_CACHE | Disable the WASM cache for PHP linting                                                |

---

---

## Extracting Meta Data
**Source:** [products/cli/extension-commands/extract-meta-data.md](https://developer.shopware.com/docs/v6.6/products/cli/extension-commands/extract-meta-data.md)  
# Extracting Meta Data

There are helpers in Shopware CLI to extract data of an extension. This is useful in your CI/CD pipeline to get the extension version or the changelog for the automated release.

## Extracting the version

To extract the version of an extension, you can use the following command:

```bash
shopware-cli extension get-version <path>
```

The path can be absolute or relative to the current working directory. The command will output the version of the extension.

## Extracting the changelog

To extract the changelog of an extension, you can use the following command:

```bash
shopware-cli extension get-changelog <path>
```

The path can be absolute or relative to the current working directory. The command will output the changelog of the extension.

It will output always the English changelog.

---

---

## Formatter
**Source:** [products/cli/formatter.md](https://developer.shopware.com/docs/v6.6/products/cli/formatter.md)  
# Formatter

Shopware-CLI comes with a built-in formatter for PHP, JavaScript, CSS, SCSS, and Admin Twig files.

To run the formatter, you can use the following command:

## Formatting an extension

```shell
shopware-cli extension format /path/to/your/extension
```

You can also run it in dry mode to just show the changes instead of editing the files.

```shell
shopware-cli extension format /path/to/your/extension --dry-run
```

```shell
docker run --rm -v $(pwd):/ext shopware/shopware-cli extension format /ext
```

You can also run it in dry mode to just show the changes instead of editing the files.

```shell
docker run --rm -v $(pwd):/ext shopware/shopware-cli extension format /ext --dry-run
```

## Formatting an entire project

```shell
shopware-cli project format /path/to/your/project
```

You can also run it in dry mode to just show the changes instead of editing the files.

```shell
shopware-cli project format /path/to/your/project --dry-run
```

```shell
docker run --rm -v $(pwd):/ext shopware/shopware-cli project format /ext
```

You can also run it in dry mode to just show the changes instead of editing the files.

```shell
docker run --rm -v $(pwd):/ext shopware/shopware-cli project format /ext --dry-run
```

By default, the formatting is done by Shopware Coding Standard. You can configure the formatting by creating a `.php-cs-fixer.dist.php` in your extension root or a `.prettierrc` file for JavaScript, CSS, and SCSS files.

---

---

## Installation
**Source:** [products/cli/installation.md](https://developer.shopware.com/docs/v6.6/products/cli/installation.md)  
# Installation

You can install the pre-compiled binary (in several different ways), use Docker or compile it from the source.

Below you can find the steps for each of them.

## Install the pre-compiled binary

Shopware CLI is published in various package managers. You can install it using the following commands.

### Homebrew

```bash
brew install shopware/tap/shopware-cli
```

### Debian/Ubuntu — APT based Linux

```bash
curl -1sLf \
  'https://dl.cloudsmith.io/public/friendsofshopware/stable/setup.deb.sh' \
  | sudo -E bash
sudo apt install shopware-cli
```

### Fedora/CentOS/SUSE/RedHat — YUM based Linux

```bash
curl -1sLf \
  'https://dl.cloudsmith.io/public/friendsofshopware/stable/setup.rpm.sh' \
  | sudo -E bash
sudo dnf install shopware-cli
```

### Archlinux User Repository (AUR)

```bash
yay -S shopware-cli-bin
```

### Manually: deb,rpm apt packages

Download the `.deb`, `.rpm` or `.apk` packages from the [releases](https://github.com/shopware/shopware-cli/releases/) page and install them with the appropriate tools.

```shell
sudo dpkg -i shopware-cli_0.5.2_linux_amd64.deb # for .deb
sudo rpm -i shopware-cli_0.5.2_linux_arm64.rpm # for .rpm
sudo apk add shopware-cli-0.5.2.apk # for .apk
```

### Nix

Install **Nix** package from here:

```shell
nix profile install nixpkgs#shopware-cli
```

or directly from the **FriendsOfShopware** repository (more up to date)

```shell
nix profile install github:FriendsOfShopware/nur-packages#shopware-cli
```

### Devenv

Update `devenv.yaml` with a new input:

```yaml
inputs:
  nixpkgs:
    url: github:NixOS/nixpkgs/nixpkgs-unstable
  froshpkgs:
    url: github:FriendsOfShopware/nur-packages
    inputs:
      nixpkgs:
        follows: "nixpkgs"
```

Then you can use the new input in the `devenv.nix` file. Don't forget to add the `inputs` argument, to the first line.

```nix
{ pkgs, inputs, ... }: {
  packages = [
    inputs.froshpkgs.packages.${pkgs.system}.shopware-cli
  ];
}
```

### GitHub Codespaces

```json
{
    "image": "mcr.microsoft.com/devcontainers/base:ubuntu",
    "features": {
        "ghcr.io/shyim/devcontainers-features/shopware-cli:latest": {}
    }
}
```

### GitHub Action

Using Shopware CLI Action :

```yaml
- name: Install shopware-cli
  uses: shopware/shopware-cli-action@v1
```

### Gitlab CI

```yaml
build:
  stage: build
  image:
    name: shopware/shopware-cli:latest
    entrypoint: [ "/bin/sh", "-c" ]
  script:
    - shopware-cli --version
```

### ddev

Add a file `.ddev/web-build/Dockerfile.shopware-cli`

```Dockerfile
# .ddev/web-build/Dockerfile.shopware-cli
COPY --from=shopware/shopware-cli:bin /shopware-cli /usr/local/bin/shopware-cli
```

### Docker Image

Add the following line to your docker image to copy the binary into your image.

```Dockerfile
# Dockerfile
COPY --from=shopware/shopware-cli:bin /shopware-cli /usr/local/bin/shopware-cli
```

## Add binary manually

Download the pre-compiled binaries from the [releases](https://github.com/shopware/shopware-cli/releases) page and copy them to the desired location.

## Running with Docker

You can also use it within a Docker container. To do that, you will need to execute something more or less like the examples below.

Registries:

* [shopware/shopware-cli](https://hub.docker.com/r/shopware/shopware-cli)

Example usage:

Builds assets of an extension

```bash
docker run \
    --rm \
    -v $(pwd):$(pwd) \
    -w $(pwd) \
    -u $(id -u) \
    shopware/shopware-cli \
    extension build FroshPlatformAdminer
```

## Compiling from source

If you just want to build from source for whatever reason, follow these steps:

```bash
git clone https://github.com/shopware/shopware-cli
cd shopware-cli

go mod tidy

go build -o shopware-cli .

./shopware-cli --version
```

---

---

## Autofixer
**Source:** [products/cli/project-commands/autofix.md](https://developer.shopware.com/docs/v6.6/products/cli/project-commands/autofix.md)  
# Autofixer

Shopware-CLI comes with some builtin auto fixers for project migrations.

## Migrate a Project to Symfony Flex

Prior to Shopware 6.5, Shopware didn't use Symfony Flex. This means that the project structure was different, and some configuration files were located in different places. The `shopware-cli project autofix flex` command will migrate your project to Symfony Flex and move all configuration files to the correct locations.

::: warning
Ensure that you have a backup of your project before running this command.
:::

```bash
shopware-cli project autofix flex
```

The command will delete all unnecessary configuration files. It will also update the `composer.json` file and the `bin/console` file to use the new configuration files.

## Migrate custom/plugins extensions to Composer

It's best practice to manage the store and your custom plugins via Composer. [If you want to learn more about this check out this guide](../../../guides/hosting/installation-updates/extension-managment.md). Shopware-CLI has a helper for migrating locally installed plugins to Composer through Shopware Packagist for the Shopware Store. Make sure you have a Shopware Packages Token, which can be gathered in the Shopware Account. You can find the token in the Shopware Account under "Shops" > "Licenses" > "..." of one extension and "Install via Composer.

```bash
shopware-cli project autofix composer-plugins
```

---

---

## Build a complete Project
**Source:** [products/cli/project-commands/build.md](https://developer.shopware.com/docs/v6.6/products/cli/project-commands/build.md)  
# Build a complete Project

Usually, when you want to deploy your project, you have to run `composer install` and compile the assets of the project. Shopware CLI provides a single command which does all of this for you.

::: warning
This command modifies the given directory and deletes files. Make sure you have committed all your changes before running this command.
:::

```bash
shopware-cli project ci <path>
```

## What does it do?

* It runs `composer install` (by default, only installs the production dependencies, use `--with-dev-dependencies` to install the dev dependencies as well)
* Looks for missing assets of extensions and only compiles the missing assets to speed up the build process
* Deletes unnecessary files like `node_modules` and many more to save disk space
* Deletes source code of compiled assets to save disk space
* Merges snippets of extensions to speed up Administration

## Using private Composer repositories

If you want to use `packages.shopware.com` as a private Composer repository, make sure you have set `SHOPWARE_PACKAGES_TOKEN` environment variable to your Composer token. This can be found in your Shopware Account.

For other private Composer repositories, you can use the `auth.json` file in the root of your project or set `COMPOSER_AUTH` environment variable with the content of the `auth.json` file.

For more information, see the [Composer documentation](https://getcomposer.org/doc/articles/authentication-for-private-packages.md).

## Reducing JavaScript in Storefront

Shopware's default `browserlist` still supports older browsers like Internet Explorer 11. If you want to reduce JavaScript polyfill and CSS prefixes, you can adjust the `browserlist` configuration in the `.shopware-project.yml` file.

```yaml
build:
  # Browserlist configuration for Storefront
  browserslist: 'defaults'
```

You can check [here which browsers would be affected](https://browsersl.ist/#q=defaults).

## Configuration options

You can configure the build process with a `.shopware-project.yml` file. The following options are available:

```yaml
build:
  # Browserlist configuration for Storefront
  browserslist: 'defaults'
  # Paths that should be deleted
  cleanup_paths:
    - 'node_modules'
  # At the end of the process, bin/console asset:install is executed, this can be disabled here
  disable_asset_copy: false
  # Exclude the following extensions from the build process
  exclude_extensions:
    - 'SwagExample'
  # Keep the extension Administration and Storefront source code
  keep_extension_source: false
  # Keep the source maps of the compiled assets
  keep_source_maps: false
  # Delete after bin/console asset:install all assets in the extensions, so only live in public folder.
  # This only works when the assets are served directly from the public folder.
  remove_extension_assets: false
  # Allows to force building an extension even when the assets existing. A use-case could be if you used composer patches for a specific extension.
  force_extension_build:
    - name: 'SomePlugin'
```

## Supporting bundles

Plugins and Apps are automatically detected by Shopware CLI. Custom bundles (classes that extend bundle class from Shopware) cannot be automatically detected as Shopware CLI does not execute any PHP code.
Therefore you need to add the path of the custom bundle to your project `composer.json`:

```json
{
    "extra": {
        "shopware-bundles": {
            // The key is the relative path from project root to the bundle
            "src/MyBundle": {}
        }
    }
}
```

If your bundle folder names does not match your bundle name, you can use the `name` key to map the folder to the bundle name.

```json
{
    "extra": {
        "shopware-bundles": {
            "src/MyBundle": {
                "name": "MyFancyBundle"
            }
        }
    }
}
```

### Bundle packaged in own composer package

If your bundle is a own composer package, make sure your composer type is `shopware-bundle` and that you have set a `shopware-bundle-name` in the extra part of the config like this:

```json
{
    "name": "my-vendor/my-bundle",
    "type": "shopware-bundle",
    "extra": {
        "shopware-bundle-name": "MyBundle"
    }
}
```

With this Composer type, `shopware-cli extension build` also works for your bundle, if you want to distribute compiled assets.

## Example Docker Image

This is an example Dockerfile which builds a Shopware project and copies the source code to the `/var/www/html` folder.

```dockerfile
#syntax=docker/dockerfile:1.4

# pin versions
FROM shopware/docker-base:8.3 AS base-image
FROM shopware/shopware-cli:latest-php-8.3 AS shopware-cli

# build

FROM shopware-cli AS build

ARG SHOPWARE_PACKAGES_TOKEN

ADD . /src
WORKDIR /src

RUN --mount=type=secret,id=composer_auth,dst=/src/auth.json \
    --mount=type=cache,target=/root/.composer \
    --mount=type=cache,target=/root/.npm \
    /usr/local/bin/entrypoint.sh shopware-cli project ci /src

FROM base-image

COPY --from=build --chown=82 --link /src /var/www/html
```

Besides Docker, it is also a perfect fit for any deployment variant.

---

---

## Helper Commands
**Source:** [products/cli/project-commands/helper-commands.md](https://developer.shopware.com/docs/v6.6/products/cli/project-commands/helper-commands.md)  
# Helper Commands

This is a curated list of helper commands that are useful for your daily work with Shopware CLI in your Shopware project.

## Create a new project

To create a new project, you can use the following command:

```bash
shopware-cli project create <folder-name>
```

It will ask you for the Shopware version. You can pass the version as second parameter:

```bash
shopware-cli project create <folder-name> <version>
```

The version parameter can be also `latest` for the latest stable version or `dev-trunk` for the latest development version.

## Replacements to include in shell scripts

Shopware CLI contains replacements for `bin/build-administration.sh` and `bin/build-storefront.sh`.

| Shell Script                | Shopware Command                        |
|-----------------------------|-----------------------------------------|
| bin/build-storefront.sh     | `shopware-cli project storefront-build` |
| bin/build-administration.sh | `shopware-cli project admin-build`      |
| bin/watch-storefront.sh     | `shopware-cli project storefront-watch` |
| bin/watch-administration.sh | `shopware-cli project admin-watch`      |

Additionally to the replacement, Shopware CLI allows only watching a specific set of extensions or exclude few.

To only watch specific:

```bash
shopware-cli project admin-watch --only-extensions <name>,<second>....
```

To exclude specific:

```bash
shopware-cli project admin-watch --skip-extensions <name>,<second>....
```

### Building only custom extensions

When working with a lot of 3rd party extensions, `project storefront-build` and `project admin-build` would become slow, when all extensions are built.
This is unnecessary, because store extensions are shipped together with their assets.

Use

```bash
shopware-cli project storefront-build --only-custom-static-extensions
shopware-cli project admin-build --only-custom-static-extensions
```

to build only extensions in the `custom/static-plugins` folder of your project, which are usually not shipping the assets.

## Worker

Usually you have to start the worker with `bin/console messenger:consume` in the project root directory. But if you want to have more than one worker at once, it gets a bit tricky. Shopware CLI has a helper command for that:

```bash
shopware-cli project worker <amount>
```

For production, you should let this handle **supervisord** or **systemd**. But for development, this is a quick way to start multiple workers.

## Clear cache

It is just a shortcut for `bin/console cache:clear` without having to be in the project root directory.

```bash
shopware-cli project clear-cache
```

If in the `.shopware-project.yml` a API connection is configured, it will clear the remote instance cache.

## Console

Similar to `clear-cache`, there is also a general shortcut for `bin/console`:

```bash
shopware-cli project console <command>
```

## Generate JWT secret

To generate a new JWT secret, you can use the following command:

```bash
shopware-cli project generate-jwt
```

It is similar to `bin/console system:generate-jwt-secret`, but requires no Shopware project to be present or PHP to be installed.

## Admin API

If you want to make requests against the Shopware-API using curl, you need to get a JWT token and add it as a header. Shopware CLI has a helper command for that:

```bash
shopware-cli project admin-api --output-token
```

This will output the JWT token to the console. You can also make directly API requests like:

```bash
shopware-cli project admin-api GET /_info/version
```

You can also pass more options like `-d` for data or `-H` for headers as you would do with curl.

---

---

## Image Proxy
**Source:** [products/cli/project-commands/image-proxy.md](https://developer.shopware.com/docs/v6.6/products/cli/project-commands/image-proxy.md)  
# Image Proxy

The `shopware-cli project image-proxy` command starts a local HTTP server that serves static files from your Shopware project's `public` folder. When a requested file is not found locally, it automatically proxies the request to an upstream server and caches the response for future requests.

This is particularly useful during development when you want to work with a local Shopware installation but need access to media files (images, documents, etc.) from a production or staging environment without downloading the entire media library.

## Usage

```bash
# Start the proxy server using configuration from .shopware-project.yml
shopware-cli project image-proxy

# Specify a custom upstream URL
shopware-cli project image-proxy --url https://my-shop.com

# Use a different port
shopware-cli project image-proxy --port 3000

# Clear the cache before starting
shopware-cli project image-proxy --clear

# Use external URL for reverse proxy setups
shopware-cli project image-proxy --external-url https://dev.example.com

# Skip Shopware config file creation
shopware-cli project image-proxy --skip-config
```

## Configuration

You can configure the upstream URL in your `.shopware-project.yml` file:

```yaml
# .shopware-project.yml
image_proxy:
  url: https://production.example.com
```

If no URL is provided via the `--url` flag or configuration file, the command will exit with an error.

## How It Works

The image proxy follows this request flow:

1. **Check Local Files**: First, it looks for the requested file in your local `public` folder
2. **Check Cache**: If not found locally, it checks the file cache (`var/cache/image-proxy/`)
3. **Proxy Request**: If not cached, it forwards the request to the upstream server
4. **Cache Response**: Successful responses (HTTP 200) are cached to disk for future requests

### Shopware Integration

By default, the command creates a Shopware configuration file at `config/packages/zzz-sw-cli-image-proxy.yml` that automatically configures Shopware to use the proxy server for all public filesystem operations. This file is automatically removed when the server stops.

The configuration looks like:

```yaml
shopware:
  filesystem:
    public:
      type: "local"
      url: 'http://localhost:8080'  # or your configured URL
      config:
        root: "%kernel.project_dir%/public"
```

### Cache Behavior

* Files are cached in `var/cache/image-proxy/` within your project directory
* The cache preserves the `Content-Type` header to ensure files are served with correct MIME types
* Cache files are named by replacing `/` with `_` in the request path
* There is no automatic cache expiration - files remain cached until manually cleared
* Cached responses include an `X-Cache: HIT` header when served

## Command Options

| Option           | Description                                                       | Default                   |
|------------------|-------------------------------------------------------------------|---------------------------|
| `--url`          | Upstream server URL (overrides config)                            | From config               |
| `--port`         | Port to listen on                                                 | `8080`                    |
| `--clear`        | Clear cache before starting                                       | `false`                   |
| `--external-url` | External URL for Shopware config (e.g., for reverse proxy setups) | `http://localhost:{port}` |
| `--skip-config`  | Skip creating Shopware config file                                | `false`                   |

## Example Scenarios

### Development with Production Media

When developing locally but needing access to production media files:

```bash
# Configure once
echo "image_proxy:
  url: https://production.example.com" >> .shopware-project.yml

# Start proxy
shopware-cli project image-proxy

# Access your local Shopware at http://localhost:8080
# Media files will be transparently fetched from production
```

### Testing with Fresh Cache

To ensure you're working with the latest media files:

```bash
shopware-cli project image-proxy --clear
```

### Multiple Environments

Switch between different upstream servers:

```bash
# Staging environment
shopware-cli project image-proxy --url https://staging.example.com

# Production environment
shopware-cli project image-proxy --url https://production.example.com
```

### Reverse Proxy Setup

When running behind a reverse proxy (Nginx, Apache, etc.):

```bash
# Configure external URL for Shopware
shopware-cli project image-proxy --external-url https://dev.example.com
```

### Manual Configuration

If you want to manage Shopware configuration manually:

```bash
# Run proxy without creating config file
shopware-cli project image-proxy --skip-config
```

---

---

## Generating MySQL dumps
**Source:** [products/cli/project-commands/mysql-dump.md](https://developer.shopware.com/docs/v6.6/products/cli/project-commands/mysql-dump.md)  
# Generating MySQL dumps

Shopware CLI has built-in support for generating MySQL dumps. The dump command is native implementation and does not use existing tools like `mysqldump`.

Creating a MySQL dump is as simple as running the following command:

```bash
shopware-cli project dump
```

This will create a `dump.sql` in the current directory. The dump command will use the database credentials from the `.env` file. If you want to use different credentials, you can use the following flags:

```bash
shopware-cli project dump --host 127.0.0.1 --username root --password root --database sw6
```

It is possible to use `--skip-lock-tables` to skip the lock tables command. This is useful for large databases or when the MySQL user has no rights to lock the table.

## Compressing the dump

Database dumps can be pretty large, it is possible to compress the dump using `gzip` or `zstd`. Use flag `--compression=gzip` for gzip compression or `--compression=zstd` for zstd compression.

## Table locking

By default, Shopware CLI will try to lock the table before dumping the data. This can fail if the MySQL user has no rights to lock the table. To skip the lock tables command, use the `--skip-lock-tables` flag.

## Anonymizing data

The `--anonymize` flag will anonymize known user data tables. The following tables are anonymized:

[See here for the complete list](https://github.com/shopware/shopware-cli/blob/main/cmd/project/project_dump.go#L74)

It is possible to customize the anonymization process by using the `dump.rewrite` configuration in the `shopware-cli.yml` file.

```yaml
# .shopware-project.yml
dump:
  rewrite:
    <table-name>:
      # Rewrite column content to new value
      <column-name>: "'new-value'"
      # Use go-faker to generate data
      <column-name>: "faker.Internet().Email()" # See https://github.com/jaswdr/faker for all available functions
```

## Ignoring table content

Some tables are not relevant for dumps, like log tables. To ignore some default tables, use the `--clean` flag. This will ignore the content of the following tables:

* `cart`
* `customer_recovery`
* `dead_message`
* `enqueue`
* `messenger_messages`
* `increment`
* `elasticsearch_index_task`
* `log_entry`
* `message_queue_stats`
* `notification`
* `payment_token`
* `refresh_token`
* `version`
* `version_commit`
* `version_commit_data`
* `webhook_event_log`

To ignore additional tables, use the `dump.ignore` configuration in the `shopware-project.yml` file.

```yaml
# .shopware-project.yml
dump:
  nodata:
    - <table-name>
```

## Ignoring entire tables

It is also possible to completely ignore a table **not only the content**.

```yaml
# .shopware-project.yml
dump:
  ignore:
    - <table-name>
```

## Adding a where clause

It is possible to add a where clause to the export of a table. So only rows matching the where clause will be exported.

```yaml
# .shopware-project.yml
dump:
  where:
    <table-name>: 'id > 5'
```

---

---

## Project config synchronization
**Source:** [products/cli/project-commands/project-config-sync.md](https://developer.shopware.com/docs/v6.6/products/cli/project-commands/project-config-sync.md)  
# Project config synchronization

Shopware CLI can synchronize the project configurations between different environments. This is useful, for example, to keep the configuration in the development and production environment in sync.

The Following things are possible to synchronize:

* Theme Configuration
* System Configuration (including extension configuration)
* Mail Templates
* Entity

## Setup

To synchronize the project, you need to create a `.shopware-project.yml` file in the root of your project. This file contains the configuration for the synchronization.

You can also use the command `shopware-cli project config init` to create a new `shopware-project.yml` file. Make sure that you configure the API access too as this is required for the synchronization.

## Credentials with environment variables

If you don't want to store the credentials in the `shopware-project.yml` file, you can use environment variables.

* `SHOPWARE_CLI_API_URL` - The URL to the Shopware instance
* `SHOPWARE_CLI_API_CLIENT_ID` - The client ID for the API access
* `SHOPWARE_CLI_API_CLIENT_SECRET` - The client secret for the API access
* `SHOPWARE_CLI_API_USERNAME` - The username for the API access
* `SHOPWARE_CLI_API_PASSWORD` - The password for the API access
* `SHOPWARE_CLI_API_DISABLE_SSL_CHECK` - Disable SSL check for the API access

Either you can fill `SHOPWARE_CLI_API_CLIENT_ID` and `SHOPWARE_CLI_API_CLIENT_SECRET` or `SHOPWARE_CLI_API_USERNAME` and `SHOPWARE_CLI_API_PASSWORD`.

## Initial pulling

To pull the configuration from the Shopware instance, you can use the command `shopware-cli project config pull`. This command pulls the configuration from the Shopware instance and stores it in the local `shopware-project.yml` file.

## Pushing the configuration

After you made the changes in the local `shopware-project.yml` file, you can push the changes to the Shopware instance with the command:

```bash
shopware-cli project config push
```

This shows the difference between your local and the remote configuration and asks you if you want to push the changes.

## Entity synchronization

With entity synchronization, you can synchronize any kind of entity using directly the Shopware API.

```yaml
sync:
  entity:
      - entity: tax
        payload:
          name: 'Tax'
          taxRate: 19
```

This example synchronizes a new tax entity with the name `Tax` and the tax rate `19`.

The further synchronizations will create the same entity again, you may want to fix the entity ID to avoid duplicates.

```yaml
sync:
  entity:
    - entity: tax
      # build a criteria to check that the entity already exists. when exists this will be skipped
      exists:
        - type: equals
          field: name
          value: 'Tax'
      # actual api payload to create something
      payload:
        name: 'Tax'
        taxRate: 19
```

---

---

## Remote extension management
**Source:** [products/cli/project-commands/remote-extension-managment.md](https://developer.shopware.com/docs/v6.6/products/cli/project-commands/remote-extension-managment.md)  
# Remote extension management

Shopware CLI has an extension manager to install and manage extensions in your Shopware project through the Shopware API like the Extension Manager in the Shopware 6 Administration panel, but for the CLI.

::: info
This functionality was designed for Shopware SaaS and should not be used for self-hosted installations. [The recommendation is to use the Deployment Helper and install all plugins via Composer](../../../guides/hosting/installation-updates/deployments/deployment-helper.md)
:::

To use the extension manager, you need a `.shopware-project.yml` or set environment variables. See here for more information about the [Project Configuration](./project-config-sync.md#setup).

::: warning
Make sure you log in using your username and password to the CLI. The extension API can be used **only by users**.
:::

## Commands

### List all extensions

```bash
shopware-cli project extension list
```

### Install an extension

```bash
shopware-cli project extension install <extension-name>
```

### Uninstall an extension

```bash
shopware-cli project extension uninstall <extension-name>
```

### Update an extension

```bash
shopware-cli project extension update <extension-name>
```

### Outdated extensions

Shows all extensions that have an update available.

```bash
shopware-cli project extension outdated
```

### Upload extension

Uploads an extension to the Shopware instance.

```bash
shopware-cli project extension upload <path-to-extension-zip>
```

### Delete extension

Deletes an extension from the Shopware instance.

```bash
shopware-cli project extension delete <extension-name>
```

---

---

## Authentication
**Source:** [products/cli/shopware-account-commands/authentication.md](https://developer.shopware.com/docs/v6.6/products/cli/shopware-account-commands/authentication.md)  
# Authentication

To interact with the Shopware Account API, you need to authenticate yourself.

For this, you need to log in using:

```bash
shopware-cli account login
```

and it will ask you interactively for your credentials.

For CI/CD pipelines, you should pass `SHOPWARE_CLI_ACCOUNT_EMAIL` and `SHOPWARE_CLI_ACCOUNT_PASSWORD` as environment variables and call directly the command you want to use.

::: info
For CI/CD tasks you should create a dedicated Shopware Account with limited access to the Shopware Store.
:::

## Multiple companies

A single Shopware Account can be part of multiple companies. You can only interact with one company at a time.

You can use the following commands to list all companies you have access to:

```bash
shopware-cli account company list
```

Next, select the active company with:

```bash
shopware-cli account company use <id>
```

---

---

## Configure composer repository
**Source:** [products/cli/shopware-account-commands/configure-composer-repository.md](https://developer.shopware.com/docs/v6.6/products/cli/shopware-account-commands/configure-composer-repository.md)  
# Configure composer repository

To install extensions from the Shopware Store, you need to configure the Composer repository in your `composer.json` file. Shopware CLI can configure this for you automatically.

First, make sure you have access to the given Shop in Shopware Account. You can check this with the following command:

```bash
shopware-cli account merchant shop list
```

If you don't see the shop you want to use, you need to switch to the correct company with the following command. Check the [Authentication](./authentication.md) guide for more information.

To create a `auth.json` file with the Composer repository configuration, you can use the following command:

::: info
You can also use the tab completion in the terminal to get the domains of the shops you have access to.
:::

```bash
shopware-cli account merchant shop configure-composer <domain>
```

This will create `auth.json` and append the Composer repository configuration to your `composer.json` file.

---

---

## Releasing automated extension to Shopware Store
**Source:** [products/cli/shopware-account-commands/releasing-extension-to-shopware-store.md](https://developer.shopware.com/docs/v6.6/products/cli/shopware-account-commands/releasing-extension-to-shopware-store.md)  
# Releasing automated extension to Shopware Store

## Prerequisites

* You are logged into the Shopware Store. Checkout the [Authentication](./authentication.md) guide for more information.
* You have a zip file of your extensions with all assets. Checkout the [Creating a zip](../extension-commands/build.md) guide for more information.
* The zip file contains a `CHANGELOG*.md` file with a Changelog entry for the new version. Having a German changelog is optional.
* You have validated the zip file with `shopware-cli extension validate <zip-path>`. See [Validating the zip](../extension-commands/validation.md) for more information.

## Releasing the extension

To release the extension to the Shopware Store, you need to upload the zip file to the store. This can be done with the `shopware-cli account producer extension upload` command.

```bash
shopware-cli account producer extension upload <zip-path>
```

This command will check first if an extension with the same version already exists in the store. If not, it will upload the extension to the store. For the compatibility of the extension, the command will use the Composer constraint of `composer.json` or `maniofest.xml` file.

After the upload, the command will wait for the result of the automatic validation. This can take a few minutes. If the validation fails, the command will output the error message, and you need to fix the issue and upload the extension again. You can skip this check with the `--skip-for-review-result` option.

---

---

## Updating store page of extension
**Source:** [products/cli/shopware-account-commands/updating-store-page.md](https://developer.shopware.com/docs/v6.6/products/cli/shopware-account-commands/updating-store-page.md)  
# Updating store page of extension

You can use Shopware CLI to version your Store page representation of your extension. This includes the description, images, and all other assets.

## Prerequisites

* You are logged into the Shopware Store. Checkout the [Authentication](./authentication.md) guide for more information.

## Fetching the current Store page

It is recommended to start with the current Store page and update only the parts you want to change. You can fetch the current Store page with the following command:

```bash
shopware-cli account producer extension info pull <path-to-extension-folder>
```

This will download all uploaded Store images and create a `.shopware-extension.yml` with all metadata of the extension.

This file can be checked in into the version control and will be automatically removed when you create a zip file using Shopware CLI.

## Updating the Store page

To push the changes to the Store page, you can use the following command:

```bash
shopware-cli account producer extension info push <path-to-extension-folder>
```

This will upload all images and metadata to the Store page.

## Image configuration

Images can be uploaded in two ways:

Explicitly defined in the configuration like this:

```yaml
store:
  images:
    - file: <path-to-file>
      # Priority of the image for ordering
      priority: 1
      # In which language the image should be used
      activate:
        de: false
        en: false
      # Is the image a preview image, only one image can be a preview
      preview:
        de: false
        en: false
```

or you can specify a single directory with all images:

```yaml
store:
  image_directory: <path-to-directory>
```

The images will be sorted by the file name. If you want to separate the images by language, you can create subdirectories with the language code like so:

```text
src/Resources/store/images/
├── de
│   ├── 0.png
│   ├── 1.png
│   └── 2.png (preview image)
└── en
    ├── 0.png
    ├── 1.png
    └── 2.png (preview image)
```

---

---

## Validation
**Source:** [products/cli/validation.md](https://developer.shopware.com/docs/v6.6/products/cli/validation.md)  
## Validation

Shopware CLI has built-in validation for extensions. This is useful in your CI/CD pipeline to validate the extension before you release it.

## Validating an extension

To validate an extension, you can use the following command:

```shell
shopware-cli extension validate /path/to/your/extension
```

```shell
docker run --rm -v $(pwd):/ext shopware/shopware-cli extension validate /ext
```

The path can be absolute or relative to the directory containing the extension or the zip file. The command exits with a non-zero exit code if the validation fails with an error-level message.

## What is validated in basic mode?

* The `composer.json` has a `shopware/core` requirement and the constraint is parsable
* The extension metadata is filled with:
  * `name`
  * `label` (German and English)
  * `description` (German and English) and longer than 150 characters and shorter than 185 characters
* PHP can be correctly linted with the minimum PHP version
* The `theme.json` can be parsed and included assets can be found
* All snippet files contain the same set of translation keys

## Supported PHP versions for linting

The following PHP versions are supported for linting:

* 7.3
* 7.4
* 8.1
* 8.2

These versions don't need to be installed locally; they are downloaded on demand and executed using WebAssembly without any dependencies.

## Running all validation tools

By default, only a few tools are run, but you can run all tools by using the `--full` option. This will run all available tools and check your extension against the latest Shopware version.

```shell
shopware-cli extension validate --full /path/to/your/extension
```

```shell
docker run --rm -v $(pwd):/ext shopware/shopware-cli extension validate --full /ext
```

By default, it will check against the latest allowed Shopware version according to your constraints in `composer.json`. It's recommended to run the check against the lowest and highest allowed version, so you can be sure that your extension is compatible with all versions. You can do this by using the `--check-against` option:

```shell
shopware-cli extension validate --full /ext --check-against lowest
shopware-cli extension validate --full /ext --check-against highest
```

```shell
docker run --rm -v $(pwd):/ext shopware/shopware-cli extension validate --full /ext --check-against lowest
docker run --rm -v $(pwd):/ext shopware/shopware-cli extension validate --full /ext --check-against highest
```

The check command has multiple reporting options, you can use `--reporter` to specify the output format. The following formats are supported:

| Format     | Description                             |
|------------|-----------------------------------------|
| `summary`  | default list of all errors and warnings |
| `json`     | json output                             |
| `junit`    | junit output                            |
| `github`   | GitHub Actions output                   |
| `markdown` | markdown output                         |

## Running Specific Tools

Instead of running all tools, you can choose to run specific tools using the `--only` flag. The following tools are available:

| Tool           | Description                    |
|----------------|--------------------------------|
| `phpstan`      | PHP static analysis            |
| `sw-cli`       | Shopware CLI validation checks |
| `stylelint`    | CSS/SCSS linting               |
| `admin-twig`   | Admin Twig template checks     |
| `php-cs-fixer` | PHP code style fixing          |
| `prettier`     | Code formatting                |
| `eslint`       | JavaScript/TypeScript linting  |
| `rector`       | PHP code refactoring           |

You can run a single tool:

```shell
shopware-cli extension validate --full /ext --only phpstan
```

Or run multiple tools by separating them with commas:

```shell
shopware-cli extension validate --full /ext --only "phpstan,eslint,stylelint"
```

```shell
docker run --rm -v $(pwd):/ext shopware/shopware-cli extension validate --full /ext --only phpstan
```

Or run multiple tools by separating them with commas:

```shell
docker run --rm -v $(pwd):/ext shopware/shopware-cli extension validate --full /ext --only "phpstan,eslint,stylelint"
```

This is particularly useful when:

* You want to focus on specific aspects of your code
* You want to run only the relevant tools for the files you've changed
* You want to fix issues one tool at a time

## Validation ignores

If you want to ignore errors or warnings, you can create a `.shopware-extension.yaml` file in your extension root with the following content:

```yaml
validation:
  ignore:
    # Ignore all errors by identifier
    - identifier: 'Shopware.XXXXXX'
    # Ignore all errors by identifier and path
    - identifier: 'Shopware.XXXXXX'
      path: 'path/to/file.php'
    # Ignore all errors by message and path
    - message: 'Some error message'
      path: 'path/to/file.php'
    # Ignore all errors by message
    - message: 'Some error message'
```

## Scanning a project

It's possible to scan an entire project instead of just a single extension. This is useful if you want to check all extensions in your project at once. You can do this by passing the path to the project root instead of the extension path.

All config files like `phpstan.neon` and `.php-cs-fixer.dist.php` should be placed in the project root for proper configuration or to override the default settings. The Verifier will automatically detect the config files and use them for the checks.

Ignoring errors works similarly to extensions; in that case, you can create a `.shopware-project.yaml` file in your project root with the same syntax.

## Common issues

### Fixer does nothing for Shopware 6.7

The fixers are enabled by the supported Shopware Version in the plugins `composer.json` file. For 6.7, you should change the composer constraint to this:

```json
{
    "minimum-stability": "dev",
    "require": {
        "shopware/core": "~6.7.0"
    }
}
```

### Missing classes in Storefront/Elasticsearch bundle

Your plugin typically requires only `shopware/core`, but when you use classes from Storefront or the Elasticsearch Bundle and they are required, you have to add `shopware/storefront` or `shopware/elasticsearch` also to the `require` in the composer.json. If those features are optional with `class_exists` checks, you want to add them into `require-dev`, so the dependencies are installed only for development and PHPStan can recognize the files.

---

---

## Community Edition
**Source:** [products/community-edition.md](https://developer.shopware.com/docs/v6.6/products/community-edition.md)  
# Community Edition

## Overview

The Community Edition is an open-source, basic variant of Shopware, free for everyone to use. All other Shopware offerings, such as  [PaaS](paas/) and [SaaS](saas) are based upon the Community Edition.

## Running Shopware

In general, there are several options to run Shopware, as explained in the [Installation](../guides/installation/) section. Also, find the [system requirements](../guides/installation/requirements) needed for running Shopware as a PHP application built upon Symfony.

## Platform components

The Shopware Platform itself is a Symfony application which consists of several components developed as Symfony bundles. Each of these components is mirrored to a dedicated repository and also included in the Shopware Platform mono repository. For the time being, there is the Core component, which includes the framework and business logic, as well as the APIs. The [Storefront](../guides/plugins/plugins/storefront/) component is a default frontend for your Storefront built upon the Bootstrap toolkit and Twig templates. A Vue.js SPA [Administration](../concepts/framework/architecture/administration-concept) component wrapped inside a Symfony bundle is a default Administration panel for all back-office tasks and communicates via the [Admin API](../concepts/api/admin-api) with the Core component. Last but not least, the Elasticsearch component gives you the opportunity to improve the indexing of entities and also contains an adapter for the entity search.

With these components stored inside many repositories, one can also enable Shopware to be used for headless scenarios. With the help of the [Production repository](https://github.com/shopware/production), you do have the opportunity to only require the repositories you really want to have in your project through the `composer.json` file (e.g. only require `shopware/core`).

## Features

Rather than listing all features from a user perspective below, we would like to mention a few key features that are also worth looking at in a more technical way. As Shopware 6 is built with the API first approach, your first technical feature touch points might be our different APIs built in our Core component.

The **Admin API** is used to work on all Administration tasks and is connected to our Administration component (Vue.js SPA). This Admin API gives you the opportunity to interact with every single entity resource of Shopware and it also ships with another endpoint, the **Sync API**. Its main purpose is to perform bulk write and delete operations within one single request via `UPSERT/DELETE`. Further conceptual information to our Admin API can be found [here](../concepts/api/admin-api). Now that you already know our Admin API, it is also interesting to learn about our [Store API](../concepts/api/store-api), which was built for a different use case. The **Store API** should be used when developing customer-facing clients. Within these endpoints, you do have the opportunity to cover the complete customer journey - starting from a product listing, showing product information and, of course, placing an order through the checkout. Not only our [Storefront](../guides/plugins/plugins/storefront/) components use these routes, but also [Composable Frontends](/../../frontends), which offer platform-independent packages to build your own custom frontend with Vue, React or something else.

Another feature worth mentioning is our CMS integration called *Shopping experiences*, which lets you build custom pages for different page types like listing, shop pages, landing pages and product detail pages. As this *Shopping Experiences* feature is also a built-in feature available through the Administration panel, you can easily drag and drop predefined (and even custom) blocks to your page layout. From a technical perspective, it is also important to know that this translatable content is stored in a generic way and is also available throughout the Store API. There is also a [conceptual article](../concepts/commerce/content/shopping-experiences-cms.md) covering this topic more specifically.

Shopware also has a custom built-in **ORM**, called [Data Abstraction Layer](../concepts/framework/data-abstraction-layer), which offers several features, like e.g., API endpoint generation for your entities. Our rule engine, called [Rule builder](../concepts/framework/rules), is a big feature that lets you create global rules with several conditions, which can be used and applied in several modules to e.g. configure the availability of promotion codes, shipping methods, payment methods or even product prices.

Last but not least, there is a most important technical feature, which gives you the power to create your custom ideas without touching the Shopware core. Every single feature above can be extended and customized with the help of **Extensions**. Throughout this [Extension system](../concepts/extensions/) one is able to create own [Plugins](../concepts/extensions/plugins-concept), [Themes](../guides/plugins/themes/), or even [Apps](../concepts/extensions/apps-concept), for your Shopware project.

## Repository structure

Shopware 6 consists of multiple repositories bundled inside a [Mono repository](https://www.atlassian.com/git/tutorials/monorepos) called [shopware/shopware](https://github.com/shopware/shopware). This is where the Shopware core is developed. You need it as a dependency in your projects and this is where you can participate in the development of Shopware through pull requests. It is split into multiple repositories for production setups. All of them are read-only and include Core, Storefront, Administration, and Elasticsearch. Besides that, there is also a `Recovery` directory, which provides the opportunity to interactively update, install and maintain Shopware throughout the browser. To start developing with Shopware 6, refer to the [Installation](../guides/installation/) section for an overview of the supported development environments.

::: info
This video is part of our online training, the [Backend Development](https://academy.shopware.com/courses/shopware-6-backend-development-with-jisse-reitsma) available on Shopware Academy for **free**.
:::

## Contribution

Shopware 6 is a community-driven platform with a lot of contributions, and we really appreciate your support. To ensure the quality of our code, our products and our documentation, we have created a small guideline for contributing [Code](../resources/guidelines/code/contribution) and contributing to the [Docs](../resources/guidelines/documentation-guidelines/) we all should endorse to. It helps you and us to collaborate with our software. Following these guidelines will help us to integrate your changes in our daily workflow.

---

---

## Digital Sales Rooms Overview
**Source:** [products/digital-sales-rooms.md](https://developer.shopware.com/docs/v6.6/products/digital-sales-rooms.md)  
# Digital Sales Rooms Overview

*Digital Sales Rooms* is a state-of-the-art new feature that seamlessly integrates into your Shopware system landscape and co-operates with your existing e-commerce infrastructure.

You can create interactive live video events for your customers straight from your Shopware website without having to switch between a presentation tool, video conferencing system, and store system. It is one sophisticated solution to highlight your products, engage your customers, and reinforce brand loyalty.

![ ](../../assets/products-digitalSalesRooms.png)

::: warning
*Digital Sales Rooms* is a license extension and is not available as open source.
:::

::: warning
*Digital Sales Rooms* application does not belong to *the default Storefront*. It's a standalone Frontend app running with Nuxt instance. This template will be hosted in a separate instance with a new domain, which will be different from the Storefront domain.
:::

To use the Digital Sales Rooms plugin, you must perform **installation** & **3rd parties setup** & **plugin configuration**.

## Prerequisites

Review the below minimum operating requirements before you install the *Digital Sales Rooms* feature:

* [node](https://nodejs.org/en) >= v18
* [pnpm](https://pnpm.io/installation) >= 8
* [Shopware Frontends framework](https://frontends.shopware.com/) based on Nuxt 3.
* Instance of [Shopware 6](../../guides/installation) (version 6.6.0 and above).
  * Recommend installing with [devenv](../../guides/installation/devenv)
* Third party services:
  * [Daily.co](https://daily.co/) - Refer to setup instructions for [realtime video call](./setup-3rd-party/realtime-video-dailyco.md)
  * [Mercure](https://mercure.rocks/)- Refer to setup instructions for [realtime Mercure service](./setup-3rd-party/realtime-service-mercure.md)

---

---

## products/digital-sales-rooms/best-practices.md
**Source:** [products/digital-sales-rooms/best-practices.md](https://developer.shopware.com/docs/v6.6/products/digital-sales-rooms/best-practices.md)  
---

---

## Frontend App Deployment
**Source:** [products/digital-sales-rooms/best-practices/app-deployment.md](https://developer.shopware.com/docs/v6.6/products/digital-sales-rooms/best-practices/app-deployment.md)  
# Frontend App Deployment

According to [Shopware Frontends deployment document](https://frontends.shopware.com/best-practices/deployment.html), all the templates which were generated by Shopware Frontends can be deployed in multiple ways, depending on the setup you are using. Most likely you will be using either a static hosting service or a server with a Node.js runtime.

You may find the different approaches are described in [Nuxt instruction](https://nuxt.com/deploy).

Alternatively, we will show some best practices of *Digital Sales Room* frontend app deployment.

---

---

## Deploy with AWS Amplify
**Source:** [products/digital-sales-rooms/best-practices/app-deployment/aws.md](https://developer.shopware.com/docs/v6.6/products/digital-sales-rooms/best-practices/app-deployment/aws.md)  
# Deploy with AWS Amplify

In this chapter, you will learn how to deploy the frontend source code to [AWS Amplify](https://aws.amazon.com/amplify/).

## Prerequisites

* Register an AWS account.
* Clone the frontend source code and push it to your GitHub repository.
  * Download the plugin zip. After extracting it, you will find it inside `/templates/dsr-frontends`.
* Push source code to your Git repository.

## Deploy

* Login to the AWS Amplify Hosting Console.
* Create a new app in AWS Amplify.
* Select and authorize access to your Git repository provider and select the main branch (it will auto deploy when there are some changes in the main branch).
* Choose a name for your app and make sure build settings are auto-detected.
* Set Environment variables under the Advanced Settings section.
  * Add `SHOPWARE_STORE_API`, `SHOPWARE_ADMIN_API`, `SHOPWARE_STORE_API_ACCESS_TOKEN`, `SHOPWARE_STOREFRONT_URL`, `ORIGIN` variables with appropriate values.
* Confirm the configuration and click on "Save and Deploy".

## Custom domain

After deploying your code to AWS Amplify, you may wish to point custom domains (or subdomains) to your site. AWS has an [instruction](https://docs.aws.amazon.com/amplify/latest/userguide/custom-domains.html).

## Configure sales channel domain

Your website is ready, and you should have a frontend app domain. Please use the current domain to configure [sales channel domain](../../configuration/domain-config.md).

---

---

## Deploy with Cloudflare
**Source:** [products/digital-sales-rooms/best-practices/app-deployment/cloudflare.md](https://developer.shopware.com/docs/v6.6/products/digital-sales-rooms/best-practices/app-deployment/cloudflare.md)  
# Deploy with Cloudflare

In this chapter you will learn how to deploy the frontend source code to [Cloudflare Pages](https://pages.cloudflare.com/).

## Prerequisites

* Register a Cloudflare account.
* Clone the frontend source code and push to your GitHub repository.
  * Download the plugin zip. After extracting, you can find it inside `/templates/dsr-frontends`.

## Deploy from local machine

* Due to this [issue](https://github.com/nuxt/nuxt/issues/28248), just make sure your `.npmrc` file has

```bash
shamefully-hoist=true
strict-peer-dependencies=false
```

* Install Wrangler

```bash
pnpm install wrangler --save-dev
```

* Make sure the Frontend app has already [generated .env file](../../installation/app-installation.md#generate-env-file)
* Build your project for Cloudflare Pages:

```bash
npx nuxi build --preset=cloudflare_pages
```

* Then deploy. However, for the first time, it will ask you to create a project:

```bash
wrangler pages deploy dist/
```

## Automation with GitHub Actions

### Setup GitHub Secrets & variables

* In GitHub Secrets, add `CLOUDFLARE_API_TOKEN` with API token value.
  * [Create an API token](https://developers.cloudflare.com/fundamentals/api/get-started/create-token/) in the Cloudflare dashboard with the "Cloudflare Pages — Edit" permission.
* In GitHub environment variables, create new environment named `production`. Add `SHOPWARE_STORE_API`, `SHOPWARE_ADMIN_API`, `SHOPWARE_STORE_API_ACCESS_TOKEN`, `SHOPWARE_STOREFRONT_URL`, `ORIGIN` variables with appropriate values.
  * Besides `production`, we can add new values for the same variable names in multiple environments such as `development`, `staging`.

### Setup pipeline

To trigger the deployment automatically, we can attach the GitHub Actions.

* Create a `.github/workflows/publish.yml` file in your repository with below sample content.

::: warning
Please note that this pipeline is just a sample. There are some points need to update for specific purpose
:::

```yml
on:
  push:
   # Specify the pipeline trigger
   branches:
      - main

jobs:
  publish:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      deployments: write
    name: Cloudflare Pages Deployment
    # Specify the environment name
    environment: production
    steps:
      - name: Checkout
        uses: actions/checkout@v3

      - uses: pnpm/action-setup@v4
        name: Install pnpm
        with:
          version: 8
          run_install: false

      - name: Install dependencies
        run: |
          pnpm install

      - name: Build env file
        run: |
          touch .env
          # echo ALLOW_ANONYMOUS_MERCURE=${{ vars.ALLOW_ANONYMOUS_MERCURE }} >> .env
          echo SHOPWARE_STORE_API=${{ vars.SHOPWARE_STORE_API }} >> .env
          echo SHOPWARE_ADMIN_API=${{ vars.SHOPWARE_ADMIN_API }} >> .env
          echo SHOPWARE_STORE_API_ACCESS_TOKEN=${{ vars.SHOPWARE_STORE_API_ACCESS_TOKEN }} >> .env
          echo SHOPWARE_STOREFRONT_URL=${{ vars.SHOPWARE_STOREFRONT_URL }} >> .env
          echo ORIGIN=${{ vars.ORIGIN }} >> .env
          cat .env

      - name: Build code
        run: |
          npx nuxi build --preset=cloudflare_pages

      - name: Publish to Cloudflare Pages
        uses: cloudflare/pages-action@v1.5.0
        with:
          apiToken: ${{ secrets.CLOUDFLARE_API_TOKEN }}
          accountId: YOUR_ACCOUNT_ID
          projectName: YOUR_PROJECT_NAME
          directory: dist
          wranglerVersion: '3'
```

* Replace `YOUR_ACCOUNT_ID` with your account ID. Get it from the dashboard URL. E.g: `https://dash.cloudflare.com/<ACCOUNT_ID>/pages`.
* Replace `YOUR_PROJECT_NAME` with the appropriate value.

## Custom domain

When deploying your Pages project, you may wish to point custom domains (or subdomains) to your site. Cloudflare has an [instruction](https://developers.cloudflare.com/pages/configuration/custom-domains/).

## Configure sales channel domain

Your website is ready, you should have a frontend app domain. Please use the current domain to configure [sales channel domain](../../configuration/domain-config.md).

---

---

## Hosting a Frontend App on an Ubuntu Server with PM2
**Source:** [products/digital-sales-rooms/best-practices/app-deployment/hosted-with-ubuntu-server.md](https://developer.shopware.com/docs/v6.6/products/digital-sales-rooms/best-practices/app-deployment/hosted-with-ubuntu-server.md)  
# Hosting a Frontend App on an Ubuntu Server with PM2

This guide will walk you through the steps to deploy DSR frontend web application to an Ubuntu server using [PM2](https://nuxt.com/docs/getting-started/deployment#pm2), a process manager for Node.js applications. PM2 will help you keep your app running in the background, restart it automatically when it crashes, and manage logs for easier troubleshooting.

## Prerequisites

* Ubuntu Server: This guide assumes you have an Ubuntu server running, and you can access it via SSH.
* Node.js & npm: Make sure Node.js and npm (Node package manager) are installed on your server.
* PM2: PM2 should be installed globally.

```bash
npm install -g pm2
```

* pnpm

```bash
npm install -g pnpm
```

* Frontend Application: Clone the frontend source code and push to your GitHub repository.
  * Download the plugin zip. After extracting, you can find it inside `/templates/dsr-frontends`.

## Build code

* After clone the source code into Ubuntu server, please follow the guide to [build env](../../installation/app-installation.md#generate-env-file) & [build code for production](../../installation/app-installation.md#for-production)

## Start the Application with PM2

Now that your app is built, create a file named `ecosystem.config.cjs` in the root of your project with the following content. Ensure that the script path points to your app's build output directory (e.g., `.output/server/index.mjs` for Nuxt 3)

```js
module.exports = {
  apps: [
    {
      name: 'DSRNuxtApp',
      port: '3000',
      exec_mode: 'cluster',
      instances: 'max',
      script: './.output/server/index.mjs'
    }
  ]
}
```

Once saved, you can start the app with:

```bash
pm2 start ecosystem.config.cjs
```

---

---

## Digital Sales Rooms with SaaS
**Source:** [products/digital-sales-rooms/best-practices/saas.md](https://developer.shopware.com/docs/v6.6/products/digital-sales-rooms/best-practices/saas.md)  
# Digital Sales Rooms with SaaS

If you are a Beyond merchant and are using SaaS, the *Digital Sales Rooms* plugin is installed in your SaaS instance. So, you should see the *Digital Sales Rooms* section in the Marketing menu item.
However, there are some steps that need to be completed to ensure the DSR functions fully with SaaS:

* [Deploy the frontend app](../app-deployment/index.md)

* [3rd parties](../../setup-3rd-party/index.md)

* [Configuration](../../configuration/index.md)

---

---

## Digital Sales Rooms Configuration
**Source:** [products/digital-sales-rooms/configuration.md](https://developer.shopware.com/docs/v6.6/products/digital-sales-rooms/configuration.md)  
# Digital Sales Rooms Configuration

This section will show how to configure *Digital Sales Rooms* plugin. The Following sections will give you a detailed procedure of configuration.

---

---

## Configuration with CLI
**Source:** [products/digital-sales-rooms/configuration/config-with-cli.md](https://developer.shopware.com/docs/products/digital-sales-rooms/configuration/config-with-cli.md)  
## Configuration with CLI

Using the CLI for configuration is significantly faster than performing each setup manually. By executing the below command, you streamline the entire process, ensuring that all necessary configurations are applied efficiently and correctly in one go.

Make sure you are in the root folder of the plugin, run:

```bash
composer dsr:config
```

This command will automatically execute the following setup commands (If you prefer, you can also execute each setup command separately to configure specific parts individually):

1. **Domain Setup**
   * `composer dsr:domain-setup`
   * This command sets up the necessary domain configurations for **Digital Sales Rooms**.

2. **Daily.co Setup**
   * `composer dsr:daily-setup`
   * This command sets up Daily.co, which is essential for real-time video/audio calling within **Digital Sales Rooms**.

3. **Mercure Setup**
   * `composer dsr:mercure-setup`
   * This command sets up the Mercure hub, which is essential for real-time updates and notifications within **Digital Sales Rooms**.

---

---

## Domain Configuration for frontend app
**Source:** [products/digital-sales-rooms/configuration/domain-config.md](https://developer.shopware.com/docs/v6.6/products/digital-sales-rooms/configuration/domain-config.md)  
::: warning
Based on the business use case, the merchant can decide to add *Digital Sales Rooms* to their existing sales channel or new sales channel.
When you run the frontend app server, you will always have a specific domain (eg: `https://dsr.shopware.io`)
:::

# Domain Configuration for frontend app

This section will show you how to add these domains to a sales channel.

## Setup domains for Digital Sales Rooms

::: warning
Please redeploy or rerun your frontend app to apply the domain changes into it.
:::

* After specifying the sales channel, head to the *Domains section* and add appropriate *Digital Sales Rooms* domains with appropriate languages. *Digital Sales Rooms* can switch languages by the path, you can choose your domain path represents for a language. Here is our recommendation:

```text
https://dsr.shopware.io - English
https://dsr.shopware.io/de-DE - Deutsch
https://dsr.shopware.io/en-US - English (US)
```

![ ](../../../assets/setup-domain-for-sales-channel-DSR.png)

* These *Digital Sales Rooms* domains should be selected as *Available domains* in [Configuration Page - Appointments](./plugin-config.md#appointments)

![ ](../../../assets/fill-domain-into-configuration.png)

---

---

## Plugin Configuration
**Source:** [products/digital-sales-rooms/configuration/plugin-config.md](https://developer.shopware.com/docs/v6.6/products/digital-sales-rooms/configuration/plugin-config.md)  
# Plugin Configuration

There are a lot of settings on the configuration page, but most of them are already filled by default. However, there are some settings that need to be set up.

## Navigate to the configuration page

Open Shopware CMS, select **Marketing** > **Digital Sales Rooms** > **Configuration**

![ ](../../../assets/products-digitalSalesRooms-configuration.png)

## Fill the settings

### Appointments

* *Available domains* - This select box shows the list of domains of all sales channels. You should choose the *Digital Sales Rooms* domains from [this section](./domain-config.md)

### Video and Audio

* *API base url* - use value `https://api.daily.co/v1/`
* *API key* - get the value from [this section](../setup-3rd-party/realtime-video-dailyco.md#get-the-api-key)

### Realtime service

* *Hub url* - get the value from [this section](../setup-3rd-party/realtime-service-mercure.md#attach-mercure-information-into-digital-sales-rooms)
* *Hub public url* - get the value from [this section](../setup-3rd-party/realtime-service-mercure.md#attach-mercure-information-into-digital-sales-rooms)
* *Hub subscriber secret* - get the value from [this section](../setup-3rd-party/realtime-service-mercure.md#attach-mercure-information-into-digital-sales-rooms)
* *Hub publisher secret* - get the value from [this section](../setup-3rd-party/realtime-service-mercure.md#attach-mercure-information-into-digital-sales-rooms)

---

---

## Digital Sales Rooms Customization
**Source:** [products/digital-sales-rooms/customization.md](https://developer.shopware.com/docs/v6.6/products/digital-sales-rooms/customization.md)  
# Digital Sales Rooms Customization

This section explains how to customize the **Digital Sales Rooms** frontend template. The DSR frontend is built with Nuxt 3 and leverages the [Nuxt Layer concept](https://nuxt.com/docs/getting-started/layers), allowing you to override file content with your own Nuxt layer for easy customization.

## Create a new Nuxt layer

If you look into the `dsr-frontends` template, you'll find the default Nuxt layer named `dsr`. This layer should remain untouched. To apply customizations, you should create a new Nuxt layer and import it in `nuxt.config.ts`. For more details, refer to the [composition guide](https://nuxt.com/docs/guide/going-further/layers). Besides, we’ve also created a customization layer named `example` within the frontend source code. You can rename this layer and modify its contents to suit your needs.

---

---

## Branding Customization
**Source:** [products/digital-sales-rooms/customization/branding.md](https://developer.shopware.com/docs/v6.6/products/digital-sales-rooms/customization/branding.md)  
::: warning
All customization instructions will refer to changes made within your customization layer folder.
:::

# Branding Customization

## Favicon

* Create `public` folder inside your layer (if missing).

* Place your favicon inside the `public` folder and ensure it is named `favicon.ico`.

## Web application title

* Create `nuxt.config.ts` inside your layer (if missing).

* Replace "Your app name" with your app's name and add the following code:

```js
app: {
  head: {
    title: 'Your app name'
  }
}
```

## Theme color

* Create `uno.config.ts` inside your layer (if missing).

* E.g. to change the primary color to `#000000`, add the following code:

```js
theme: {
  colors: {
    primary: {
      DEFAULT: '#000000'
    }
  }
}
```

* Refer to the `uno.config.ts` file in the dsr layer to understand the key structure for overriding colors.

---

---

## Component Customization
**Source:** [products/digital-sales-rooms/customization/component.md](https://developer.shopware.com/docs/v6.6/products/digital-sales-rooms/customization/component.md)  
::: warning
All customization instructions will refer to changes made within your customization layer folder.
:::

# Component Customization

In this document, we will demonstrate how to customize a component (specifically, the "Wishlist" button) in the DSR frontend template using the Nuxt layer concept. This guide will help you understand the process of extending or modifying the default components in your frontend without altering the core files.

## Understand the component structure of the default layer

Before customizing any components, it's essential to understand the structure of the default layer. Navigate to the `dsr/components` directory to view all available components.

In this case, look for the `SwWishlistButton.vue` component inside `dsr/components/shared/molecules/`.

## Create the component in the custom layer

Now, inside your custom layer, paste the copied `SwWishlistButton.vue` file. You should now have the same default component in your custom-layer directory, ready for modification.
Once you have copied the component to your custom layer, modify the part of the component that you want to change. For instance, you may want to change the style, add new functionality, or update the template.
At this point, the frontend app will ignore the `SwWishlistButton` from the default layer and only use the `SwWishlistButton` from the custom layer.

---

---

## I18n Customization
**Source:** [products/digital-sales-rooms/customization/i18n.md](https://developer.shopware.com/docs/v6.6/products/digital-sales-rooms/customization/i18n.md)  
::: warning
All customization instructions will refer to changes made within your customization layer folder.
:::

# I18n Customization

This guide will walk you through the process of customizing the internationalization (i18n) setup in your Nuxt 3 project using the Nuxt layer concept. By using this method, you can extend and override the default i18n functionality to meet your specific requirements without modifying the core files.

## Configure i18n

Configure the i18n settings in your `nuxt.config.ts` file. This configuration defines the language directory and any specific language configurations you want to override.

Add the following configuration to `nuxt.config.ts`:

```js
modules: [
  "@nuxtjs/i18n",
],
i18n: {
  langDir: "./i18n/src/langs/",
  ...i18nConfig,
},
```

## Create the i18n Folder in the custom layer

To customize the i18n functionality, we need to create a new folder structure in your custom layer. You will mirror the default layer's structure, but only create the files you need to override.

Take a look on `example` layer to understand the structure.

---

---

## Digital Sales Rooms Installation
**Source:** [products/digital-sales-rooms/installation.md](https://developer.shopware.com/docs/v6.6/products/digital-sales-rooms/installation.md)  
# Digital Sales Rooms Installation

::: warning
This section will show how to install **Digital Sales Rooms** plugin into the existing Shopware platform. It will not explain a Shopware platform installation.
:::

::: info
Before we start, let assume Shopware platform is running at `https://shopware.store` & frontend app will run in `https://dsr.shopware.io`.
:::

This includes installation at admin and at template.

---

---

## Admin Installation
**Source:** [products/digital-sales-rooms/installation/admin-installation.md](https://developer.shopware.com/docs/v6.5/products/digital-sales-rooms/installation/admin-installation.md)  
# Admin Installation

::: warning
To access the *Digital Sales Rooms* source code, please create a support ticket in your Shopware Account and share your GitLab (not GitHub) username. You will then be granted access to the private repository.
:::

## Get the plugin

1. Clone or download the [SwagDigitalSalesRooms repository 6.6.x](https://gitlab.com/shopware/shopware/shopware-6/services/swagdigitalsalesrooms/-/tree/6.6.x).
2. Extract the plugin, including the outer folder `SwagDigitalSalesRooms`, to `platform/custom/plugins` directory of the Shopware repository.
3. Ensure the plugin has a PHP package structure containing `composer.json` file, `src/` folder, and so on.
4. Prepare a zip file containing the plugin as in the following structure:

```bash
# SwagDigitalSalesRooms.zip

**SwagDigitalSalesRooms**/
├── bin
├── composer.json
├── composer.lock
├── makefile
├── phpstan.neon
├── phpunit.xml
├── README.md
├── src
└── tests
```

## Install & activate the plugin in Admin Extension

To install and use the *Digital Sales Rooms* feature, place and extract the above zip file in this location `<shopware-root-dir>/custom/plugins` directory. Once it is done, you can either refer the guide to [install plugin](../../../guides/plugins/plugins/plugin-base-guide.html#install-your-plugin) or you can run the below Symfony commands:

```bash
# refresh the list of available plugins
bin/console plugin:refresh
# find the plugin **name** (first column on the list). In this case, it is "**SwagDigitalSalesRooms"**
bin/console plugin:install **SwagDigitalSalesRooms** --activate
# clear the cache afterward
bin/console cache:clear

# Now it is ready to use
```

---

---

## Admin Side Installation
**Source:** [products/digital-sales-rooms/installation/admin-side-installation.md](https://developer.shopware.com/docs/v6.6/products/digital-sales-rooms/installation/admin-side-installation.md)  
# Admin Side Installation

::: info
Digital Sales Rooms plugin is a licensed plugin. If you already know how to install a licensed plugin, you can skip this part.
:::

::: warning
As part of the Shopware Beyond plan, the **Digital Sales Rooms** is available to you as an extension.
Same with other plugins, you have multiple ways to install the plugin via composer, direct download or through your Shopware Account.
:::

In this part, we will learn how to get and install the **Digital Sales Rooms** plugin into local Shopware instance.

## Get the plugin

If you are a merchant with Shopware Beyond, you can access account.shopware.com and create a wildcard environment with attached plugins. Refer to [guideline](https://docs.shopware.com/en/account-en/extension-partner/wildcard-environments) for more info.

![ ](../../../assets/products-digitalSalesRooms-wildcard.png)

By this way, you can get the plugin quickly into Shopware instance via multiple ways (via composer, direct download or through your Shopware Account).

### Via download

To install a plugin via download, follow these steps:

* From wildcard environment detail page, click on the plugin and then click on the “Download” button.
* Save the zip file to your computer.
* In your Shopware 6 instance source code, go to the `custom/plugins` directory.
* Extract the zip file into the `custom/plugins` directory with name `SwagDigitalSalesRooms`.

### Via composer

To install a plugin via composer, follow these steps:

* From wildcard environment detail page, click on the plugin and then click on the "Install via composer" button.
* A modal will appear and contain all command lines to install.

## Install & activate the plugin

Once you fetch the plugin, you can run the Symfony commands below for activating the plugin:

```bash
# refresh the list of available plugins
bin/console plugin:refresh
# find the plugin **name** (first column on the list). In this case, it is "**SwagDigitalSalesRooms"**
bin/console plugin:install **SwagDigitalSalesRooms** --activate
# clear the cache afterward
bin/console cache:clear

# Now it is ready to use
```

---

---

## Frontend App Installation
**Source:** [products/digital-sales-rooms/installation/app-installation.md](https://developer.shopware.com/docs/v6.6/products/digital-sales-rooms/installation/app-installation.md)  
# Frontend App Installation

::: warning
After finishing the installation of the plugin in Shopware, we will run and connect the frontend template with Shopware.
The frontend template is built based on the Shopware Frontends framework, so it inherits from Shopware Frontends & Nuxt 3 concepts.
:::

## Get the frontend template

* From the **Digital Sales Rooms** plugin, you can find the dsr-frontends folder by:

```shell
cd ./templates/dsr-frontends
```

* This folder contains all the source code for the frontend template. You can copy the entire source code and push it to your own private repository for easy customization in the future.

## How to run?

### Generate env file

```shell
cp .env.template .env
```

| Key | Required? | Description                     |
|-----|-----------| --------------------------------|
| ORIGIN | Yes | This is current frontend app domain. E.g: `https://dsr.shopware.io` |
| SHOPWARE\_STOREFRONT\_URL | Yes | This is default Shopware storefront domain. E.g: `https://shopware.store` |
| SHOPWARE\_ADMIN\_API | Yes | This is Shopware admin-api domain server. E.g: `https://shopware.store/admin-api` |
| SHOPWARE\_STORE\_API | Yes | This is the Shopware store-api domain server. E.g: `https://shopware.store/store-api` |
| SHOPWARE\_STORE\_API\_ACCESS\_TOKEN | Yes | This is the Shopware Access Token to connect to Shopware API. Head to sales channel you assign the *Digital Sales Rooms* domain, find the `API access` section, and copy the `API access key` |
| ALLOW\_ANONYMOUS\_MERCURE | No | This is the flag for development only. When the value = 1, it means your app is running with unsecured Mercure. |

Example .env:

```shell
ORIGIN=https://dsr.shopware.io
SHOPWARE_STOREFRONT_URL=https://shopware.store
SHOPWARE_ADMIN_API=https://shopware.store/admin-api
SHOPWARE_STORE_API=https://shopware.store/store-api
SHOPWARE_STORE_API_ACCESS_TOKEN=XXXXXXXXXXX
```

### For development

* Install pnpm with global scope

```shell
npm install -g pnpm
```

* Install dependencies

```shell
pnpm install
```

* Run dev server

```shell
pnpm dev
```

Usually, port `3000` is the default port so that you can access the domain of the Frontend App `http://localhost:3000/`

### For production

* Install pnpm with global scope

```shell
npm install -g pnpm
```

* Install dependencies

```shell
pnpm install
```

* Build

```shell
pnpm build
```

After build code, please read [here](../best-practices/app-deployment/index.md) for how to make the deployment.

The Following section guides you to 3rd party setup procedures.

---

---

## Realtime Service - Mercure
**Source:** [products/digital-sales-rooms/installation/realtime-service-mercure.md](https://developer.shopware.com/docs/v6.5/products/digital-sales-rooms/installation/realtime-service-mercure.md)  
# Realtime Service - Mercure

::: info
Symfony provides a straightforward component, built on top of the [Mercure](https://symfony.com/doc/current/mercure.html) protocol, specifically designed for this class of use cases.
[Mercure](https://mercure.rocks/docs/getting-started) is an open protocol designed from the ground up to publish updates from server to client. It is a modern and efficient alternative to timer-based polling and to WebSocket.
:::

## Mercure general settings

Detailed below is the minimum configuration needed for a working stack apart from project-specific CMS configurations.

* *Set up CORS allowed origins* - In our case, it would be the domain where the Shopware Frontends is hosted and available. For instance: https://dsr-frontends.com (frontend).
* *Set up publish allowed origins* - The domains that request the Mercure service must be added to publish allowed origins or else it gets rejected. For instance (HTTP protocol must not be included): shopware-pwa-gs.herokuapp.com (frontend) and pwa-demo-api.shopware.com(backend - API).
* *Set up the publisher (JWT) key* - Set whatever you want.
* *Set up the subscriber (JWT) key* - Set whatever you want.

There are 4 main pieces of information from Mercure Hub you have to get:

* *Hub url* - The hub URL.
* *Hub public url* - The hub public URL, normally it's the same as the hub URL.
* *Hub subscriber secret* - The JWT key used for authenticating subscribers
* *Hub publisher secret* - The JWT key used for authenticating publishers

## Setup

There are different ways to set up Mercure as listed below:

### Setup via Stackhero (Recommended)

::: info
💡 We tested the service provided by [StackHero](https://www.stackhero.io/en/services/Mercure-Hub/pricing). Depending on the expected traffic, you can easily switch between the plans. For a small demo among a few people at the same time, the “Hobby” plan is sufficient.
:::

* Create the Stackhero account.
* Access the dashboard.
* In the **Stacks** menu item, create a new stack with the **Mercure Hub** service.
* When creating a stack successfully, tap into the Configure button.
* On this page, it's easy to find the [Mercure general settings](#mercure-general-settings), copy all the necessary information, and paste it into [the proper inputs of the configuration page](../configuration.md#realtime-service).

![Mercure configuration](../../../assets/products-digitalSalesRooms-mercureConfig.png)

![ ](../../../assets/products-digitalSalesRooms-mercureConfigExample.png)

### Setup via Docker

The docker image can be found at [dunglas/mercure](https://hub.docker.com/r/dunglas/mercure). It allows you to use the following *env* variables to configure Mercure.

::: warning
Use different publisher and subscriber keys for security reasons.
:::

```txt
- MERCURE_PUBLISHER_JWT_KEY: your-256-bit-publisher-key
- MERCURE_SUBSCRIBER_JWT_KEY: your-256-bit-subscriber-key
- MERCURE_EXTRA_DIRECTIVES: |-  
   cors_origins "https://my-pwa-shop.com https://en.my-pwa-shop.com"  
   anonymous 0  
   ui 1
```

You can also configure it like the self-installed version via the Caddyfile.

```txt
// Sample Caddyfile
{
    # Debug mode (disable it in production!)
    debug
    # HTTP/3 support
}
:80
log
route {
    redir / /.well-known/mercure/ui/
    encode gzip
    mercure {
        # Enable the demo endpoint (disable it in production!)
        demo
        # Publisher JWT key
        publisher_jwt MySecret
        # Subscriber JWT key
        subscriber_jwt MySecret
        # CORS
        cors_origins http://localhost:3000 http://localhost:8080 http://shopware.test http://7779-91-90-160-158.ngrok.io
        publish_origins localhost:3000 localhost:8080 shopware.test 7779-91-90-160-158.ngrok.io
        # Allow anonymous subscribers (double-check that it's what you want)
        anonymous
        # Enable the subscription API (double-check that it's what you want)
        subscriptions
    }
    respond "Not Found" 404
}
```

### Self-host setup

The [installation guide](https://mercure.rocks/docs/hub/install) explains all the steps that are required for installing the Mercure.

```txt
mercure {
...  
publisher_jwt my-publisher-key HS256  
subscriber_jwt my-subscriber-key HS256  
cors_origins "https://my-pwa-shop.com https://en.my-pwa-shop.com"  
demo 0  
ui 0  
...
}
```

---

---

## Realtime Video Call - Daily.co
**Source:** [products/digital-sales-rooms/installation/realtime-video-dailyco.md](https://developer.shopware.com/docs/v6.5/products/digital-sales-rooms/installation/realtime-video-dailyco.md)  
# Realtime Video Call - Daily.co

The service is responsible for streaming a video between the attendees.

## Login Daily.co dashboard

* Go to the dashboard at: https://dashboard.daily.co/
* Login or register with the Daily.co account.

## Get the API key

* Visit the “developers” section on the left
* Copy the *API KEY* and paste it [here](../configuration.md#video-and-audio)

![ ](../../../assets/products-digitalSalesRooms-videoConfig.png)

---

---

## Setup 3rd parties
**Source:** [products/digital-sales-rooms/setup-3rd-party.md](https://developer.shopware.com/docs/v6.6/products/digital-sales-rooms/setup-3rd-party.md)  
# Setup 3rd parties

This section will show you how to set up 3rd parties of *Digital Sales Rooms*.

* [Daily.co](https://daily.co/) - Refer to setup instructions for [realtime video call](./setup-3rd-party/realtime-video-dailyco.md)
* [Mercure](https://mercure.rocks/)- Refer to setup instructions for [realtime Mercure service](./setup-3rd-party/realtime-service-mercure.md)

The Following sections give you a detailed procedure for setup.

---

---

## Realtime Service - Mercure
**Source:** [products/digital-sales-rooms/setup-3rd-party/realtime-service-mercure.md](https://developer.shopware.com/docs/v6.6/products/digital-sales-rooms/setup-3rd-party/realtime-service-mercure.md)  
# Realtime Service - Mercure

::: info
Symfony provides a straightforward component, built on top of the [Mercure](https://symfony.com/doc/current/mercure.html) protocol, specifically designed for this class of use cases.
[Mercure](https://mercure.rocks/docs/getting-started) is an open protocol designed from the ground up to publish updates from server to client. It is a modern and efficient alternative to timer-based polling and to WebSocket.
:::

## Setup hub

There are different ways to set up Mercure; we choose the quickest and easiest for you below:

### Setup via Stackhero (Recommended)

::: info
💡 We tested the service provided by [StackHero](https://www.stackhero.io/en/services/Mercure-Hub/pricing). Depending on the expected traffic, you can easily switch between the plans. For a small demo among a few people at the same time, the “Hobby” plan is sufficient.
:::

* Create the Stackhero account.
* Access the dashboard.
* In the **Stacks** menu item, create a new stack with the **Mercure Hub** service.
* When creating a stack successfully, tap into the Configure button.
* On this page, it's easy to find the [Mercure general settings](#attach-mercure-information-into-digital-sales-rooms), copy all the necessary information, and paste it into [the proper inputs of the configuration page](../configuration/plugin-config.md#realtime-service).

![Mercure configuration](../../../assets/products-digitalSalesRooms-mercureConfig.png)

![ ](../../../assets/products-digitalSalesRooms-mercureConfigExample.png)

### Setup via Docker

::: warning
For security reasons, use different publisher and subscriber keys in production mode.
:::

You can clone our [local-mercure-sample](https://github.com/shopware/local-mercure-sample) and run it with docker-compose.

## Config Mercure hub

After init mercure hub, let's make it more secure with your information:

* *Set up CORS allowed origins* - In our case, it would be the domain where the Shopware Frontends is hosted and available. For instance: `https://dsr.shopware.io` (frontend domain).
* *Set up publish allowed origins* - The domains that request the Mercure service must be added to publish allowed origins or else it gets rejected. For instance (HTTP protocol must not be included): `https://dsr.shopware.io` (frontend domain) and `https://shopware.store` (backend API domain).
* *Set up the publisher (JWT) key* - Set whatever you want.
* *Set up the subscriber (JWT) key* - Set whatever you want.

## Attach Mercure information into Digital Sales Rooms

From your Mercure hub, it's easy to get the proper information:

* *Hub url* - The hub URL.
* *Hub public url* - The hub public URL, normally it's the same as the hub URL.
* *Hub subscriber secret* - The JWT key used for authenticating subscribers
* *Hub publisher secret* - The JWT key used for authenticating publishers

Then, fill them in [Configuration Page - Realtime service](../configuration/plugin-config.md#realtime-service)

---

---

## Realtime Video Call - Daily.co
**Source:** [products/digital-sales-rooms/setup-3rd-party/realtime-video-dailyco.md](https://developer.shopware.com/docs/v6.6/products/digital-sales-rooms/setup-3rd-party/realtime-video-dailyco.md)  
# Realtime Video Call - Daily.co

The service is responsible for streaming a video between the attendees.

## Login Daily.co dashboard

* Go to the dashboard at: <https://dashboard.daily.co/>
* Login or register with the Daily.co account.

## Get the API key

* Visit the “developers” section on the left
* Copy the *API KEY* and paste it [here](../configuration/plugin-config.md#video-and-audio)

![DailyAPIConfig](../../../assets/products-digitalSalesRooms-videoConfig.png)

---

---

## Extensions
**Source:** [products/extensions.md](https://developer.shopware.com/docs/v6.6/products/extensions.md)  
# Extensions

Shopware provides some unique extensions:

* Migration Assistant - An extension that connects the source shop and the target shop to migrate data.
* B2B Suite - The B2B Suite extension equips your store with the most important B2B functions. These include workflows, order lists, budgets, and quick orders.
* B2B Components - B2B components enable you to enhance your shop with essential B2B functionalities.
* Advanced Search - This offers the possibility to customize the search fields.
* Subscriptions - Subscription extension allows you to offer products on a subscription basis.

---

---

## Advanced Search
**Source:** [products/extensions/advanced-search.md](https://developer.shopware.com/docs/v6.6/products/extensions/advanced-search.md)  
# Advanced Search

::: info
Advanced Search is available starting with Commercial 5.5.0
:::

Shopware Advanced Search is a part of the Commercial plugin available along with the Evolve and Beyond plan.

Advanced search module is based on Elasticsearch. In addition to a high performance product search, it also offers you the possibilities to customize the search experience depending on your needs. So you could also search for manufacturers and categories. The simple Administration module allows quick and easy configuration of the search.

Before continuing, you should make sure you have a basic knowledge of [Elasticsearch](https://www.elastic.co/guide/en/elasticsearch/reference/7.10/index.html) and the Shopware implementation of it.

---

---

## Cross Search
**Source:** [products/extensions/advanced-search/Cross-search.md](https://developer.shopware.com/docs/v6.6/products/extensions/advanced-search/Cross-search.md)  
# Cross Search

@Refer: `\Shopware\Commercial\AdvancedSearch\Domain\CrossSearch\CrossSearchLogic`

At times, the need arises to search for categories using product names. To enable Elasticsearch with this capability, it becomes essential to index associated data across different indexes. However, it's important to note that this operation leads to a notable increase in the overall size of the index.

To solve this problem, an **experimental** feature called Cross Search has been introduced. You can configure which associations could be cross-searched:

```yaml
# config/packages/advanced_search.yaml
advanced_search:
    # When searching for `manufacturer.product.name`, if `product_manufacturer.product` cross_search is enabled, the `product` index will be used for search field `name`
    cross_search:
        product.product_manufacturer: false
        product.category: false
        category.product: true
        product_manufacturer.product: true
```

By default, only `category - product` and `product_manufacturer - product` associations are enabled, but you can change this behavior in the parameter. This way, we don't need to index product's data inside category and manufacturer indexes.

You can add your own Cross Search mapping to the parameter. If the mapping is not defined or is false, you need to index the associated data accordingly.

Be aware that this comes with a downside: when Cross Search is enabled, we need an extra aggregated Elasticsearch query to accomplish the desired search behavior.

---

---

## Add / Modify language analyzers, stopwords, stemmer
**Source:** [products/extensions/advanced-search/How-to-add-modify-language-analyzers-stopwords-stemmer.md](https://developer.shopware.com/docs/v6.6/products/extensions/advanced-search/How-to-add-modify-language-analyzers-stopwords-stemmer.md)  
# Add / Modify language analyzers, stopwords, stemmer

With the introduction of the multi-language index, support for built-in [Elasticsearch language analyzers](https://www.elastic.co/guide/en/elasticsearch/reference/current/analysis-lang-analyzer.html) was also introduced.

This would help language-based fields have different analyzers for each language's specific features, like stopwords, stemmers, and normalization, out of the box.

You can also add more or customize the language analyzer by overriding the analyzer parameter in `custom/plugins/SwagCommercial/src/AdvancedSearch/Resources/config/packages/advanced_search.yaml`

For example:

```yaml
advanced_search:
    analysis:
        analyzer:
            sw_your_custom_language_analyzer:
                type: custom
                tokenizer: standard
                filter: ['lowercase', 'my_stopwords_filter', 'my_stemmer_filter']
    filter:
        my_stopwords_filter:
            type: 'stop'
            stopwords: ['foo', 'bar']
        my_stemmer_filter:
            type: 'stemmer'
            language: 'english'
    # It's important to map your analyzer with the language iso code
    language_analyzer_mapping:
        custom_iso: sw_your_custom_language_analyzer
```

---

---

## Add more Fields to Product Search
**Source:** [products/extensions/advanced-search/How-to-add-more-fields-to-product-search.md](https://developer.shopware.com/docs/v6.6/products/extensions/advanced-search/How-to-add-more-fields-to-product-search.md)  
# Add more Fields to Product Search

You can add more searchable fields into your product or any Elasticsearch definition.

In this example, we create a field called `productNumberPrefix` to make it searchable. This requires 3 steps:

**1. Decorate the ElasticsearchDefinition**

```xml
<service id="YourPluginNameSpace\ElasticsearchProductDefinitionDecorator" decorates="Shopware\Elasticsearch\Product\ElasticsearchProductDefinition">
    <argument type="service" id=".inner"/>
    <argument type="service" id="Shopware\Commercial\AdvancedSearch\Domain\Search\SearchLogic"/>
</service>
```

```php
<?php declare(strict_types=1);

namespace YourPluginNameSpace;

use OpenSearchDSL\Query\Compound\BoolQuery;
use Shopware\Core\Framework\Context;
use Shopware\Core\Framework\DataAbstractionLayer\EntityDefinition;
use Shopware\Core\Framework\DataAbstractionLayer\Search\Criteria;
use Shopware\Elasticsearch\Framework\AbstractElasticsearchDefinition;

class ElasticsearchProductDefinitionDecorator extends AbstractElasticsearchDefinition
{
    public function __construct(
        private readonly AbstractElasticsearchDefinition $decorated
    ) {
    }

    public function getEntityDefinition(): EntityDefinition
    {
        return $this->decorated->getEntityDefinition();
    }

    public function buildTermQuery(Context $context, Criteria $criteria): BoolQuery
    {
        return $this->decorated->buildTermQuery($context, $criteria);
    }

    public function getMapping(Context $context): array
    {
        $mappings = $this->decorated->getMapping($context);

        $additionalMappings = [
            // define your new field's type
            'prefixProductNumber' => self::KEYWORD_FIELD,
            // other additional fields
        ];

        $mappings['properties'] = array_merge($mappings['properties'], $additionalMappings);

        return $mappings;
    }

    public function fetch(array $ids, Context $context): array
    {
        $data = $this->decorated->fetch($ids, $context);

        $documents = [];

        foreach ($data as $id => $document) {
            $document = array_merge($document, [
                // get first 5 characters from productNumber to index it
                'prefixProductNumber' => substr($document['productNumber'], 0, 5),
            ]);

            $documents[$id] = $document;
        }

        return $documents;
    }
}
```

**2. Run the commands:**

We need to update these data mapping to the Opensearch's server to make the change effective:

```bash
// Update the Elasticsearch indices mapping, introduce since 6.5.4.0
bin/console es:mapping:update

// Assume the new field data are already set in products, otherwise you don't need to reindex
bin/console es:index --no-queue
```

**3. Insert new fields to advanced\_search\_config\_field of the search entity**

So now the data is mapped and indexed, we need to make it searchable by adding the new field into the search config. Create a new migration and make sure it is run by reinstalling or updating the plugin:

```bash
bin/console database:create-migration --name AddNewPrefixProductNumberFieldIntoProductAdvancedSearch --plugin YourPlugin
```

```php
<?php declare(strict_types=1);

namespace YourPluginNameSpace\Migration;

use Doctrine\DBAL\Connection;
use Shopware\Commercial\AdvancedSearch\Entity\AdvancedSearchConfig\Aggregate\AdvancedSearchConfigFieldDefinition;
use Shopware\Core\Content\Product\ProductDefinition;
use Shopware\Core\Defaults;
use Shopware\Core\Framework\Migration\MigrationStep;
use Shopware\Core\Framework\Uuid\Uuid;

class Migration1692954529AddNewPrefixProductNumberFieldIntoProductAdvancedSearch extends MigrationStep
{
    public function getCreationTimestamp(): int
    {
        return 1692954529;
    }

    public function update(Connection $connection): void
    {
        $configSalesChannelIds = $connection->fetchFirstColumn('SELECT id FROM advanced_search_config');

        $createdAt = (new \DateTime())->format(Defaults::STORAGE_DATE_TIME_FORMAT);

        foreach ($configSalesChannelIds as $configSalesChannelId) {
            $connection->insert(AdvancedSearchConfigFieldDefinition::ENTITY_NAME, [
                'id' => Uuid::randomBytes(),
                'field' => 'prefixProductNumber',
                'config_id' => $configSalesChannelId,
                'entity' => ProductDefinition::ENTITY_NAME,
                'tokenize' => 1,
                'searchable' => 1,
                'ranking' => 500,
                'created_at' => $createdAt,
            ]);
        }
    }
}
```

---

---

## Configure Searchable Fields
**Source:** [products/extensions/advanced-search/How-to-configure-searchable-fields.md](https://developer.shopware.com/docs/v6.6/products/extensions/advanced-search/How-to-configure-searchable-fields.md)  
# Configure Searchable Fields

Search entities and their searchable fields are stored in `advanced_search_config` and `advanced_search_config_field` table respectively.

These configured fields help to build the search query when a search/suggest request is sent from the client.

This approach is very similar to how `product_search_config` and `product_search_config_field` work in the platform. The main difference is you can configure the configuration by sales channel instead of by language (each sales channel now has its own search config).

@Refer:

`\Shopware\Commercial\AdvancedSearch\Entity\AdvancedSearchConfig\AdvancedSearchConfigDefinition`
`\Shopware\Commercial\AdvancedSearch\Entity\AdvancedSearchConfig\Aggregate\AdvancedSearchConfigFieldDefinition`

To have the custom search configuration, you need to add a migration to insert the configuration into the database. In the below example, we add default search configuration for product, manufacturer, and category entities

@Refer: `\Shopware\Commercial\Migration\Migration1680751315SWAGAdvancedSearch_AddAdvancedSearchConfigurationDefaults`

And you might want to add the configuration for newly created saleschannel as well:
@Refer: `\Shopware\Commercial\AdvancedSearch\Subscriber\SalesChannelCreatedSubscriber`

---

---

## Define a custom Elasticsearch Definition
**Source:** [products/extensions/advanced-search/How-to-define-your-custom-Elasticsearch-definition.md](https://developer.shopware.com/docs/v6.6/products/extensions/advanced-search/How-to-define-your-custom-Elasticsearch-definition.md)  
# Define a custom Elasticsearch Definition

In the previous implementation, the Elasticsearch index was language-based, meaning each system's language would be indexed in a separate index. With the introduction of the multilingual index:

Each index will contain multiple language-based fields; refer to the [ADR](/docs/resources/references/adr/2023-04-11-new-language-inheritance-mechanism-for-opensearch) and adjust your custom Elasticsearch definition's configuration mapping to adapt to the new mapping structure.

For instance, to define your custom Elasticsearch definition (this definition will be used for later examples).

```php
<?php declare(strict_types=1);

namespace YourPluginNameSpace;

use Doctrine\DBAL\ArrayParameterType;
use Doctrine\DBAL\Connection;
use OpenSearchDSL\Query\Compound\BoolQuery;
use Shopware\Commercial\AdvancedSearch\Domain\Search\AbstractSearchLogic;
use Shopware\Core\Framework\Context;
use Shopware\Core\Framework\DataAbstractionLayer\EntityDefinition;
use Shopware\Core\Framework\DataAbstractionLayer\Search\Criteria;
use Shopware\Core\Framework\Uuid\Uuid;
use Shopware\Elasticsearch\Framework\AbstractElasticsearchDefinition;

class YourCustomElasticsearchDefinition extends AbstractElasticsearchDefinition
{
    public function __construct(
        private readonly EntityDefinition $definition,
        private readonly Connection $connection,
        private readonly AbstractSearchLogic $searchLogic
    ) {
    }

    /**
     * Define your ES definition's mapping
     */
    public function getMapping(Context $context): array
    {
        $languages = $this->connection->fetchAllKeyValue(
            'SELECT LOWER(HEX(language.`id`)) as id, locale.code
             FROM language
             INNER JOIN locale ON locale_id = locale.id'
        );

        $languageFields = [];

        foreach ($languages as $languageId => $code) {
            $parts = explode('-', $code);
            $locale = $parts[0];

            $languageFields[$languageId] = self::getTextFieldConfig();
            if (\array_key_exists($locale, $this->languageAnalyzerMapping)) {
                $fields = $languageFields[$languageId]['fields'];
                $fields['search']['analyzer'] = $this->languageAnalyzerMapping[$locale];
                $languageFields[$languageId]['fields'] = $fields;
            }
        }

        $properties = [
            'name' => [
                'properties' => $languageFields,
            ],
            'description' => [
                'properties' => $languageFields,
            ],
        ];

        return [
            '_source' => ['includes' => ['id']],
            'properties' => $properties,
        ];
    }

    /**
     * Build a bool query when searching your custom ES definition, by default we use the Shopware\Commercial\AdvancedSearch\Domain\Search\SearchLogic  
     */
    public function buildTermQuery(Context $context, Criteria $criteria): BoolQuery
    {
        return $this->searchLogic->build($this->definition, $criteria, $context);
    }

    /**
    * fetch data from storage to push to elasticsearch cluster when indexing data 
    */
    public function fetch(array $ids, Context $context): array
    {
        $data = $this->fetchData($ids, $context);

        $documents = [];

        foreach ($data as $id => $item) {
            $translations = (array) json_decode($item['translation'] ?? '[]', true, 512, \JSON_THROW_ON_ERROR);

            $document = [
                'id' => $id,
                'name' => $this->mapTranslatedField('name', true, ...$translations),
                'description' => $this->mapTranslatedField('description', true, ...$translations),
            ];

            $documents[$id] = $document;
        }

        return $documents;
    }

    public function getEntityDefinition(): EntityDefinition
    {
        return $this->definition;
    }

    private function fetchData(array $ids, Context $context): array
    {
        $sql = <<<'SQL'
SELECT
    LOWER(HEX(custom_entity.id)) AS id,
    CONCAT(
        '[',
            GROUP_CONCAT(DISTINCT
                JSON_OBJECT(
                    'description', your_custom_entity_translation.description,
                    'name', your_custom_entity_translation.name,
                    'languageId', LOWER(HEX(your_custom_entity_translation.language_id))
                )
            ),
        ']'
    ) as translation
FROM your_custom_entity custom_entity
    LEFT JOIN your_custom_entity_translation ON your_custom_entity_translation.your_custom_entity_id = custom_entity.id
WHERE custom_entity.id IN (:ids)
GROUP BY custom_entity.id
SQL;

        $result = $this->connection->fetchAllAssociativeIndexed(
            $sql,
            [
                'ids' => $ids,
            ],
            [
                'ids' => ArrayParameterType::STRING,
            ]
        );

        return $result;    }
}
```

And register it in the container with tag `shopware.es.definition` and `advanced_search.supported_definition`

```xml
# YourPluginNameSpace should be changed to your respectively ElasticsearchDefinition and Definition classes
<service id="YourPluginNameSpace\YourCustomElasticsearchDefinition">
    <argument type="service" id="YourPluginNameSpace\YourCustomDefinition"/>
    <argument type="service" id="Doctrine\DBAL\Connection"/>
    <argument type="service" id="Shopware\Commercial\AdvancedSearch\Domain\Search\SearchLogic"/>

    <tag name="shopware.es.definition"/>
    <tag name="advanced_search.supported_definition"/>
</service>
```

---

---

## Extend Search Template
**Source:** [products/extensions/advanced-search/How-to-extend-the-search-and-suggest-template.md](https://developer.shopware.com/docs/v6.6/products/extensions/advanced-search/How-to-extend-the-search-and-suggest-template.md)  
# Extend Search Template

To show the results in the search overview, you have to extend the `search/index.html.twig` and then apply the results in your desired styling.
You can take a look at an example of `custom/plugins/SwagCommercial/src/AdvancedSearch/Resources/views/storefront/page/search/index.html.twig`.

The manufacturers and categories or your custom search result could be realized in the template as:

```twig
{% set searchResult = page.listing.extensions.multiSearchResult %}
{% set products = page.listing %}
{% set manufacturers = searchResult.getResult('product_manufacturer') %}
{% set categories = searchResult.getResult('category') %}
{% set customEntities = searchResult.getResult('custom_entity') %}
```

## How to extend the suggest template

To show the results in the suggest dropdown, you have to extend `Storefront/storefront/layout/header/search-suggest.html.twig` like the Advanced Search does in `custom/plugins/SwagCommercial/src/AdvancedSearch/Resources/views/storefront/layout/header/search-suggest.html.twig`.

The completion, manufacturers and categories or your custom search result could be realized in the template as:

```twig
{% set suggestResult = page.searchResult.extensions.multiSuggestResult %}
{% set products = page.searchResult %}
{% set completions = page.searchResult.extensions.completionResult %}
{% set manufacturers = suggestResult.getResult('product_manufacturer') %}
{% set categories = suggestResult.getResult('category') %}
{% set customEntities = suggestResult.getResult('custom_entity') %}
```

---

---

## Add / Modify Completion
**Source:** [products/extensions/advanced-search/How-to-modify-completion.md](https://developer.shopware.com/docs/v6.6/products/extensions/advanced-search/How-to-modify-completion.md)  
# Add / Modify Completion

The Advanced Search does not use the default Elasticsearch completion because it only supports a fixed order and the storage size is high. As an alternative, Advanced Search uses aggregations to find the most important word combinations for your search input.

## Adding completion to your definition mapping

To index our own completion keywords, we need to inject `Shopware\Commercial\AdvancedSearch\Domain\Completion\CompletionDefinitionEnrichment` into your ES definition and call enrich methods in `getMapping` and `fetch` as following example:

Example:

*The definition is from the [previous example](./How-to-define-your-custom-Elasticsearch-definition):*

```php
<?php declare(strict_types=1);

class YourCustomElasticsearchDefinition extends AbstractElasticsearchDefinition
{
    public function __construct(
        private readonly EntityDefinition $definition,
        private readonly Connection $connection,
        private readonly AbstractSearchLogic $searchLogic,
        private readonly CompletionDefinitionEnrichment $completionDefinitionEnrichment,
        private readonly array $languageAnalyzerMapping
    ) {
    }

    public function getMapping(Context $context): array
    {
        // ...
        
        return [
            '_source' => ['includes' => ['id']],
            // to add the mapping of completion field in your definition
            'properties' => array_merge($properties, $this->completionDefinitionEnrichment->enrichMapping()),
        ];
    }

    public function fetch(array $ids, Context $context): array
    {
        // ...

        // to add the completion keywords to the existing data
        return $this->completionDefinitionEnrichment->enrichData($this->getEntityDefinition(), $documents);
    }
}
```

## Add/modify completion keywords

By default, each of Shopware's ES definitions has a set of `string` fields to be considered as completion keywords. This configuration is realized via the parameter `%advanced_search.completion%`, if the configured fields for your definition are not set, all StringFields of the definition will be used as completion keywords.

For example, you can add or modify this configuration in `config/packages/advanced_search.yaml`:

```yaml
advanced_search:
    completion:
        your_custom_entity:
            - email
            - company
```

If you want to have more control over the completion, such as using static texts from files or parsing a field from another data source as completion keywords, you might want to decorate the service `\Shopware\Commercial\AdvancedSearch\Domain\Completion\CompletionDefinitionEnrichment::enrichData` instead.

---

---

## Modify Search Logic
**Source:** [products/extensions/advanced-search/How-to-modify-search-logic.md](https://developer.shopware.com/docs/v6.6/products/extensions/advanced-search/How-to-modify-search-logic.md)  
# Modify Search Logic

@Refer: `\Shopware\Commercial\AdvancedSearch\Domain\Search\SearchLogic`

This class is the central place to build the Elasticsearch query:

* Load all searchable fields of the wanted search entity and the current context's sales channel.
* The search term will be tokenized and filtered into a list of "token". For e.g., `The 2 QUICK Brown-Foxes jumped over the lazy dog's bone` will be tokenized to `[ The, 2, QUICK, Brown, Foxes, jumped, over, the, lazy, dog's, bone ]`.
* Each search token will form a bool query to check whether the token matches any of the loaded searchable fields. This step is when `\Shopware\Commercial\AdvancedSearch\Domain\Search\TokenQueryBuilder::build` takes place, it will help to build a `token query`.
* These built queries will be combined into a single query by `AND` or `OR` operators, depending on the search behavior configured at the first step.
* This query will be used by `\Shopware\Elasticsearch\Framework\DataAbstractionLayer\ElasticsearchEntitySearcher` to search.

To modify the search logic, you can decorate the search logic class and add your own logic into it:

```xml
<service id="YourPluginNameSpace\Domain\Search\SearchLogicDecorator" decorates="Shopware\Commercial\AdvancedSearch\Domain\Search\SearchLogic">
    <argument type="service" id=".inner"/>
    <argument type="service" id="Shopware\Commercial\AdvancedSearch\Domain\Configuration\ConfigurationLoader"/>
</service>
```

```php
<?php declare(strict_types=1);

namespace YourPluginNameSpace;

use OpenSearchDSL\Query\Compound\BoolQuery;
use Shopware\Commercial\AdvancedSearch\Domain\Configuration\ConfigurationLoader;
use Shopware\Commercial\AdvancedSearch\Domain\Search\AbstractSearchLogic;
use Shopware\Core\Framework\Api\Context\SalesChannelApiSource;
use Shopware\Core\Framework\Context;
use Shopware\Core\Framework\DataAbstractionLayer\EntityDefinition;
use Shopware\Core\Framework\DataAbstractionLayer\Search\Criteria;

class SearchLogicDecorator extends AbstractSearchLogic
{
    public function __construct(
        private readonly AbstractSearchLogic $decorated,
        private readonly ConfigurationLoader $configurationLoader
    ) {
    }

    public function build(EntityDefinition $definition, Criteria $criteria, Context $context): BoolQuery
    {
        if (!$context->getSource() instanceof SalesChannelApiSource) {
            return new BoolQuery();
        }

        $salesChannelId = $context->getSource()->getSalesChannelId();
        // you probably want get the search configs of the context's sales channel but it's optional
        $searchConfig = $this->configurationLoader->load($salesChannelId);

        // you probably want to add extra logic into existing logic but it's optional
        $bool = $this->getDecorated()->build($definition, $criteria, $context);

        // Add your own logic
        return $bool;
    }

    public function getDecorated(): AbstractSearchLogic
    {
        return $this->decorated;
    }
}
```

---

---

## Search and Suggest Routes
**Source:** [products/extensions/advanced-search/Search-and-suggest-routes.md](https://developer.shopware.com/docs/v6.6/products/extensions/advanced-search/Search-and-suggest-routes.md)  
# Search and Suggest Routes

@Refer: `\Shopware\Commercial\AdvancedSearch\Domain\Search\ProductSearchRouteDecorator`

`ProductSearchRoute` is decorated, so when searching for products from the Storefront, a `multiSearchResult` extension is added to the search product listing result. This extension includes all the search results for each Elasticsearch definition with the tag `advanced_search.supported_definition` with the given search term.

The same approach applies to `ProductSuggestRoute`. The only difference is that we added the completion search result as another extension `completionResult` to the search product listing result.

@Refer: `\Shopware\Commercial\AdvancedSearch\Domain\Suggest\ProductSuggestRouteDecorator`

You can also subscribe to the event `\Shopware\Commercial\AdvancedSearch\Event\MultiContentSearchCriteriaEvent` or `\Shopware\Commercial\AdvancedSearch\Event\MultiContentSuggestCriteriaEvent` to adjust the search criteria.

This decoration approach comes with the benefit that the caching mechanism already works for the decorated search routes.

---

---

