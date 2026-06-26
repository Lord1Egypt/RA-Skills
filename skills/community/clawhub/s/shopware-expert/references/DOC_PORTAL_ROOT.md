# DOC PORTAL ROOT

Compiled excerpts from the Shopware Developer Documentation snapshot. Prefer live docs at [developer.shopware.com](https://developer.shopware.com/) when in doubt.

---

## AGENTS.md
**Source:** [AGENTS.md](https://developer.shopware.com/docs/AGENTS.md)  
# AGENTS.md

This file provides guidance to coding agents like CursorAI or Claude Code.

## Repository Overview

This is the **Shopware Developer Documentation** repository (`shopware/docs`) that contains comprehensive developer documentation for Shopware 6, served at [developer.shopware.com/docs](https://developer.shopware.com/docs/). The documentation is integrated with the main [developer portal](https://github.com/shopware/developer-portal) repository.

> **Note:**
> This documentation covers **Shopware 6** and is intended for use with the [shopware/shopware](https://github.com/shopware/shopware) open-source e-commerce framework.
>
> For contributing to or understanding Shopware core, see the [shopware/shopware GitHub repository](https://github.com/shopware/shopware) for source code and core platform issues.

## Documentation Structure

The repository follows a 4-tier hierarchical organization:

* **`/concepts/`** - High-level architectural concepts (API, commerce, extensions, framework)
* **`/guides/`** - Step-by-step tutorials (hosting, installation, integrations, plugins)
* **`/products/`** - Product-specific documentation (CLI, PaaS, extensions, Digital Sales Rooms)
* **`/resources/`** - References, guidelines, ADRs, and tooling documentation

## Common Development Commands

### Documentation Development

```bash
# Setup developer portal environment
pnpm run docs:env

# Link documentation content to developer portal
pnpm run docs:link

# Preview documentation locally
pnpm run docs:preview
```

### Quality Control

```bash
# Run spellcheck via docker
make spellcheck-local

# Run spellcheck with installed sources (aspell and pyspelling)
make spellcheck

# Auto-fix markdown issues (be aware that it can only fix certain issues)
make fix

# Sort spellcheck wordlist
LC_ALL=C sort .wordlist.txt -o .wordlist.txt
```

## Key Architecture Patterns

### Dual Repository System

* **Content Repository**: `shopware/docs` (this repo) - contains all Markdown content
* **Presentation Layer**: `shopware/developer-portal` - handles building and serving
* **Integration**: Content is linked via symlinks using `docs-cli.cjs`

### Automated Content Synchronization

Critical content auto-syncs from main `shopware/shopware` repository every 3 hours:

* `/adr/*.md` → `/resources/references/adr/*.md` (Architecture Decision Records)
* `/adr/assets/*` → `/assets/adr/*` (ADR assets)
* `/coding-guidelines/core` → `/resources/guidelines/code/core` (Coding standards)

### Extension Documentation Architecture

* **Apps**: Server-based external integrations with JWT validation, SDK integration
* **Plugins**: Internal Shopware core extensions with DAL, services, events
* **Themes**: Asset management, SCSS variables, inheritance system

## Quality Assurance Workflows

The repository has extensive automated quality control:

* **Markdown linting**: Validates formatting and style consistency
* **Spell checking**: Uses custom wordlist (`.wordlist.txt`) with pyspelling
* **Grammar checking**: Reviewdog integration for language validation
* **External link validation**: Lychee tool checks for broken links
* **Asset naming validation**: Enforces strict naming conventions
* **PageRef validation**: A custom Deno script checks internal cross-references

## Development Environment

* **Node.js**: 18.x with pnpm package manager
* **Nix**: Uses `devenv.nix` for consistent development environments
* **Build System**: VitePress managed through the developer portal
* **CI/CD**: 11+ GitHub Actions workflows for quality control and synchronization

## File Conventions

### Markdown Style

* Configuration in `markdown-style-config.yml`
* 40+ linting rules enabled
* Consistent formatting enforced via CI/CD

### Asset Management

* All assets in `/assets/` directory
* Strict naming conventions are enforced
* Images, diagrams, and media files (40,000+ characters worth)
* Extensive use of Mermaid diagrams, SVGs, and screenshots

### Code Snippets

* Reusable examples in `/snippets/` directory
* Multi-format support (PHP, JavaScript, Vue, Twig, XML, YAML, JSON)
* Configuration examples for apps, plugins, and system setup

## Cross-linking System

* Uses PageRef components for consistent internal linking
* Hierarchical navigation with clear parent-child relationships
* Context-aware references between Concepts ↔ Guides

## Version Management

* Branch-based versioning (`main`, `v6.5`, `v6.4`)
* Feature flag documentation for experimental features
* Clear deprecation notices and upgrade paths
* Automated format migration (Gitbook → VitePress)

## Redirects

`.gitbook.yaml` is used to manage redirects from old URLs to new ones, ensuring users find the correct content even after structural changes.

This can be done by the following prompt:

```shell
Check the current branch against main. There should be two files to be moved. Create a redirect in the `.gitbook.yaml` in the pattern that already exists.
```

## Do's and Don'ts for AI agents

### Do's

* **Follow repository conventions**: Adhere to the existing documentation structure, markdown style rules, and asset naming conventions.
* **Respect synced content**: When changes are needed in synced areas (`/resources/references/adr/`, `/assets/adr/`, `/resources/guidelines/code/core/`), propose edits against the `shopware/shopware` repository instead of changing them here.
* **Keep redirects consistent**: When pages are moved or removed, compare your branch against `main`, identify changed paths, and add redirects to `.gitbook.yaml` following the existing patterns.
* **Use quality checks when appropriate**: Run `make lint`, `make fix`, or the configured spellcheck tasks when you make non-trivial documentation changes, especially if CI feedback suggests issues.
* **Prefer incremental, focused changes**: Keep pull requests small and well-scoped so they are easy to review and reason about.

### Don't

* **Don't edit synced files directly**: Avoid modifying files that are automatically synchronized from `shopware/shopware`, as those changes will be overwritten.
* **Don't break existing URLs**: Avoid renaming or moving pages without adding a corresponding redirect entry in `.gitbook.yaml`.
* **Don't bypass style and spelling rules**: Do not introduce Markdown formatting that conflicts with `markdown-style-config.yml`, or ignore repeated spelling issues that should be added to `.wordlist.txt`.
* **Don't change repository tooling lightly**: Avoid editing CI workflows, configuration files, or build tooling unless explicitly requested, and always keep changes minimal and well-documented.
* **Don't mix unrelated changes**: Do not bundle large, unrelated modifications (for example, structural moves plus extensive content rewrites) into a single change set.

---

---

## apps.md
**Source:** [apps.md](https://developer.shopware.com/apps.md)  
---

---

## chat.md
**Source:** [chat.md](https://developer.shopware.com/chat.md)  
---

---

## Home
**Source:** [docs.md](https://developer.shopware.com/docs.md)  
# Home

Let us help you guide through the landscape of knowledge for Shopware 6. This documentation is organised in order to facilitate knowledge for different **products**, **topics** and **depths** of interest.

The two main sections **concepts** and **guides** assist you to navigate the documentation according to your needs.

Whereas **Concepts** convey the ideas, inner workings and architectural considerations behind our product, **Guides** provide explicit examples, step-by-step tutorials that deal with specific tasks.

These two sections are complemented by the **References**, which contain structured code references, lists of flags, commands, endpoints which are useful for development.

Visit the [academy](https://academy.shopware.com/collections?category=developer-sw6) for video content. If you have any questions left, you can always ask them on [StackOverflow](https://stackoverflow.com/questions/tagged/shopware6?tab=Newest) or join our awesome community on [Discord](https://discord.com/channels/1308047705309708348/1309107911175176217).

![Readme](assets/readme-splash.png)

---

---

## frontends.md
**Source:** [frontends.md](https://developer.shopware.com/frontends.md)  
---

---

## Extensions
**Source:** [guides/plugins.md](https://developer.shopware.com/docs/v6.6/guides/plugins.md)  
# Extensions

As a Shopware developer, your main work will be to develop extensions that enhance or modify the functionality of Shopware in a specific way. Shopware offers different types of extensions, each with its own benefits and implications. To make sure you don't get lost in all the options, take a look at the extension [overview](overview) article which compares the approaches.

Alternatively, if you want to dive straight in, take a look at our introduction guides:

These guides are essential information on how to create, configure, and extend you store with Shopware extensions.

---

---

## Overview
**Source:** [guides/plugins/overview.md](https://developer.shopware.com/docs/v6.6/guides/plugins/overview.md)  
# Overview

The variety of Shopware's extension interfaces can be overwhelming, so let us start with a simple overview comparing the three approaches **Plugins**, **Themes**, and **Apps**.

| Task | Plugin | Theme | App | Remarks |
| :--- | :--- | :--- | :--- | :--- |
| Change Storefront appearance | ✅ | ✅ | ✅ |  |
| Add admin modules | ✅ | ❌ | ✅ |  |
| Execute Webhooks | ✅ | ❌ | ✅ | Apps main functionality is to call Webhooks, but Plugins can be implemented to do that as well. |
| Add custom entities | ✅ | ❌ | ✅ |  |
| Modify database structure | ✅ | ❌ | ❌ |  |
| Integrate payment providers | ✅ | ❌ | ✅ |  |
| Publish in the Shopware Store | ✅ | ✅ | ✅ |  |
| Install in Shopware 6 Cloud Shops | ❌ | ❌ | ✅ |  |
| Install in Shopware 6 self-hosted Shops | ✅ | ✅ | ✅ | Apps can be installed and used since Shopware 6.4.0.0 |
| Add custom logic/routes/commands | ✅ | ❌ | ✅ | Apps extract functionalities/logic into separate services, so technically, they can add custom logic |
| Control order of style/template inheritance | ❌ | ✅ | ✅ |  |

## Plugins

Plugins are the most powerful extension mechanism, as they can be used to extend, overwrite and modify almost any part of the software. At the same time, they can also be the most harmful for the same reasons. You will probably need to write a plugin, if you make profound changes or complex functionalities such as:

* Custom price calculation
* Product imports
* Custom Content/Products
* Connecting 3P identity providers
* Dynamic validations
* Customer tracking

Follow our [Plugin Base Guide](plugins/plugin-base-guide) to learn how to develop a plugin. See the [Plugin Fundamentals](plugins/plugin-fundamentals/) section below for more examples.

::: info
If your extensions do not require any of the above but rather design changes, a template tweak might ideally be appropriate.
:::

## Themes

A theme lets you perform the tasks listed below.

* Template overrides
* Custom styles
* Configuration interfaces
* Control the order in which styles and templates are loaded

Technically, plugins and themes are very similar and overlap in most of their logic. However, some special aspects are handled differently, such as template and style priority or their activation. Once plugins are installed and activated, their styles and templates are applied immediately. If a theme is installed, it must first be selected in the theme manager.

::: info
Note that a plugin can also override templates.
:::

To get started with your first theme, follow our [Theme Base Guide](themes/theme-base-guide).

## Apps

Operation in cloud environments is not possible due to the aspects listed under [Plugins](overview#plugins). Therefore, a different, less intrusive pattern was introduced. Apps enable event-based integrations that communicate with external services via a synchronous API.

Most of the app's logic resides in this third-party service, so developers must ensure that they handle the details of the API and provide their service with appropriate security, protection, and reliability. While it comes with these responsibilities, you are free to choose which operating environment, framework, or programming language you wish to use as long as our [guidelines for Shopware apps](apps/app-base-guide) are followed.

Apps also provide theme support, so all the features of [Themes](overview#themes) are also available for apps. Payments are also supported by apps and the user can be forwarded to a payment provider.

---

---

## Plugins
**Source:** [guides/plugins/plugins.md](https://developer.shopware.com/docs/v6.6/guides/plugins/plugins.md)  
# Plugins

Shopware plugins are extensions that enhance the functionality and features of the Shopware e-commerce platform. Plugins are designed to extend the core capabilities of Shopware and offer additional functionalities that are not available out of the box. While apps and themes are also extensions but they differ from plugins. To better understand the differences, take a look at the [Overview](../../../guides/plugins/overview) article.

## Feature Comparison

::: tip

For customizing projects, it is recommended to use bundles instead of plugins.
As bundles are not managed via Administration and don't have a lifecycle they offer full control over the project.

:::

| Feature                                       | Plugin             | Static Plugin           | Shopware Bundle                 | Symfony Bundle                  |
| --------------------------------------------- | ------------------ | ----------------------- | ------------------------------- | ------------------------------- |
| Installation                                  | Via Shopware Admin | Via Composer            | Via Composer                    | Via Composer                    |
| Repository Location                           | `custom/plugins`   | `custom/static-plugins` | `vendor` or inside `src` folder | `vendor` or inside `src` folder |
| Lifecycle Events (install, update, uninstall) | Yes                | Yes                     | No                              | No                              |
| Can be managed in Administration              | Yes                | No                      | No                              | No                              |
| Can be a Theme                                | Yes                | Yes                     | Yes                             | No                              |
| Can modify Admin / Storefront with JS/CSS     | Yes                | Yes                     | Yes                             | No                              |

## Types of plugins

There are different types of plugins in terms of their folder structure and functionality.

### Plugins

`<shopware project root>/custom/plugins` contains all plugins from the shopware store. The plugins are installed and managed via the Shopware administration.

### Static plugins

`<shopware project root>/custom/static-plugins` contains all plugins that are project-specific and are typically committed to the git repository.

:::info
The detection of static plugins is not done via the Shopware administration. They have to be required by the project via composer to be installable.
:::

```bash
# You can find the vendor/package name in the plugin's composer.json file under "name"
composer req <vendor>/<plugin-name>
```

### Symfony Bundle / Shopware Bundle

It's also possible to use Shopware/Symfony bundles instead of plugins.
This is useful if you don't want to have the lifecycle of plugins and don't want it manageable via the Shopware administration.
The bundles are typically installed via composer and are not managed by the Shopware administration.

---

---

## integrations.md
**Source:** [integrations.md](https://developer.shopware.com/integrations.md)  
---

---

## landing/apps.md
**Source:** [landing/apps.md](https://developer.shopware.com/landing/apps.md)  
---

---

## landing/plugins.md
**Source:** [landing/plugins.md](https://developer.shopware.com/landing/plugins.md)  
---

---

## migrate-to-shopware.md
**Source:** [migrate-to-shopware.md](https://developer.shopware.com/migrate-to-shopware.md)  
---

---

## Shopware Release Policy
**Source:** [release-notes.md](https://developer.shopware.com/release-notes.md)  
# Shopware Release Policy

## Release Calendar

![Version Chart](https://shopware-platform-assets.s3.eu-central-1.amazonaws.com/release-schedule/schedule.svg)

This version chart shows which Shopware versions are currently supported in which way. You will see the following states:

* **Maintained version**: This is the latest minor version of the current major cycle and is actively supported with patch updates if necessary. Every minor version will be superseded by the next minor version.
* **[Extended support](https://www.shopware.com/en/news/shopwares-new-release-policy/)**: The last minor version of a major cycle will get extended patch updates with selective bug fixes and security updates.
* **Security fixes only**: The version is provided with security fixes only. The fixes are provided via a security plugin, but not via direct patch update.
* **End of life version**: The version isn't actively supported anymore. You should update as soon as possible.

Continue reading if you want to learn more about the different version types and release cycles.

## Release management at Shopware

Releasing new versions of Shopware is essential to stay competitive in the market and offer merchants benefits through the introduction of new features, adjustments to existing ones, or enhancements to the underlying architecture of Shopware.

Knowing that each update requires effort from the community, we are careful to minimize its impact. The following overview of our release strategy provides insight into what you can expect.

## Shopware SaaS, PaaS and Self-Hosted

Shopware is available in different distribution types and plans. There is the free Community Edition and the [Shopware Plans](https://www.shopware.com/en/pricing/). While the plans include everything from the Community Edition, they bring a variety of benefits, giving merchants and agencies the much-needed edge over the competition. As for hosting, Shopware brings, apart from self-hosting, two additional ways of hosting, each with its own benefits.

[Shopware SaaS](https://www.shopware.com/en/shopware-cloud/), hosted by Shopware, offers merchants a convenient turn-key solution with **weekly updates**. This is the easiest version of Shopware to use as you don't have to worry about hosting and your system will always automatically run on the latest version of Shopware. This means that all new features are always directly available to you.

With [Shopware PaaS](https://www.shopware.com/en/shopware-paas/), also hosted by Shopware, you are in charge of updating the system.

The same is true for the self-hosted version, where you download and host Shopware yourself or have someone else do it for you. In these versions, **minor releases** occur **monthly**.

## Types of releases

There are three release types:

* Major release
* Minor release
* Patch release

The type can be inferred from the version number that is attached to a release. Shopware is using semantic versioning, except of adding a "6" to the beginning, indicating it is a "Shopware 6" release in contrast to the predecessor, Shopware 5.

So in short, the version number is built like this: **6.Major.Minor.Patch**

As an example, 6.5.0.0 is a major release. The following 6.5.0.1 would be a patch release, 6.5.1.0 a minor release.

So just having a look if and which position of the version number contains zero tells you the type of release.

More on this can be read on [semver.org](https://semver.org/)
A complete overview of the current and past releases can be found at [GitHub](https://github.com/shopware/shopware/releases).

For questions on how to install a release please refer to the [documentation](https://docs.shopware.com/en/shopware-6-en/getting-started).

## Release cycles

* Major
  * Once a year.
* Minor
  * Every first Monday of the month.
* Patch
  * Anytime, but only on demand.

## What effects does a release have

The different types of release are in place to indicate two things: What to expect and how big the impact in terms of work on your side is.

**Major releases** are aimed at maintaining a current and cutting-edge technical foundation, introducing substantial changes that may demand significant effort. On the other hand, **minor** and **patch** updates necessitate testing but generally do not entail disruptive breaking changes.

**Breaking changes** in Shopware refer to software modifications or updates that require developers to adjust their existing code to maintain compatibility. These changes can impact the functionality or behavior of certain features, requiring developers to update their codebase to align with the latest version of Shopware.

**Deprecations**, involve signaling that a particular feature or method is no longer recommended for use in future versions of Shopware. While deprecated features are still functional in the current version, they are marked for removal in subsequent releases. Developers are encouraged to migrate to alternative solutions or updated methods to ensure long-term compatibility and avoid potential issues when upgrading to newer versions of the software. Deprecation notices serve as a proactive way for developers to stay informed about changes and plan for the necessary updates in their projects.

### Major releases

The Major release, being the least frequent type of release delivers the most significant impact in terms of updating technical foundations, and occasionally introduces new features and architectural changes that enable Shopware to maintain a competitive edge. The effort required for adaptation depends on the level of customization in your shop and the number of extensions you use.

Adapting Shopware to changes in the ecosystem requires implementing breaking changes. This involves adjusting Shopware internals to meet evolving requirements or updating underlying frameworks such as Symfony, Vue.js, and other dependencies. Remaining relevant in the ever-changing landscape of technology necessitates embracing change, and this process of adaptation may result in breaks. While efforts are made to minimize any inconvenience, we acknowledge that once a year, we take a significant stride toward the future. At least in parts.

Each Major Release is accompanied by a **Release Candidate (RC)**, which is typically made available approximately two months before the scheduled major release. This RC serves as an opportunity for the community to adapt, explore the changes, and provide valuable feedback.

Depending on the feedback the community gives us during the RC phase, it might be prolonged.

If you are an extension developer or use your private extension in a cloud shop, major releases could bring the need to update your code. These major releases in the cloud happen at the same time as the on-premise major release, to make things easier for you.

### Minor releases

Minor releases can be installed seamlessly without requiring modifications to extensions. These updates encompass all changes implemented in Shopware Cloud since the last minor release for **self-hosted**.

Minor releases primarily focus on the addition of features, improved functionality, or addressing minor and fringe bugs. Although the impact on extension developers is minimal in terms of required work, the benefits for merchants and agencies can be substantial. Despite the absence of breaking changes in this release type, it still introduces new features and significant improvements.

### Patch and security releases

Patch releases can be installed without the need for changes to extensions.

Given the broad array of scenarios Shopware is deployed in, there are some we can't predict or prepare for. If such a scenario occurs and the underlying code needs to be patched, we release the fix as soon as possible. As these releases are immediate and without notice, they only include important and urgent changes to Shopware. In rare cases there can be breaking changes, but only if any other measures would pose a risk to merchants.

A special kind of patch is a release containing a security fix. These releases are usually small and contain only the fix itself, with some exceptions. These releases must be implemented as soon as possible to keep your shop and customers save.

*Please note: if updating is not possible for whatever reason, there is the security plugin which implements all security patches. It is, however, preferable to update, since patching code through a plugin can potentially cause side effects.*

---

---

## References
**Source:** [resources/references.md](https://developer.shopware.com/docs/v6.6/resources/references.md)  
# References

The references serve as essential resources for developers, administrators, and testers, providing comprehensive details on implementation parameters. They cover every aspect of the platform, including objects, functions, classes, and more. By consulting these references, you will be able to gain a deep understanding of Shopware's capabilities and utilize its features effectively in your development, administration, and testing tasks.

---

---

## API Reference
**Source:** [resources/references/api-reference.md](https://developer.shopware.com/docs/v6.6/resources/references/api-reference.md)  
# API Reference

The API references provide detailed information about the available endpoints, methods, parameters, request and response formats, and authentication mechanisms of an API. It provides essential information on how to interact with the API, what data can be sent or received, and how to handle different API responses.

These references guide you to use the correct syntax, understand the expected input and output formats, implement the necessary authentication mechanisms and successful API requests and effectively utilize the functionality provided by the API in your applications.

There are two dedicated API reference documents for your reference:

* [Store API reference](https://shopware.stoplight.io/docs/store-api/38777d33d92dc-quick-start-guide) - Focused on customer-facing aspects, the Store API allows you to access and manipulate data related to products, customer interactions, shopping carts, and others that significantly impact the frontend user experience. It caters to both anonymous and authenticated users.

* [Admin API reference](https://shopware.stoplight.io/docs/admin-api/twpxvnspkg3yu-quick-start-guide) - Primarily for backend and administrative functions, the Admin API enables structured data exchanges, bulk operations, data synchronization, and import-export tasks, addressing the backend needs of the Shopware platform.

---

---

## Security
**Source:** [resources/references/security.md](https://developer.shopware.com/docs/v6.6/resources/references/security.md)  
# Security

## Overview

This reference presents a comprehensive compilation of all security measures implemented in Shopware 6, along with instructions on how to configure them.

:::info
If you have found a security vulnerability in Shopware, please report it to us following the instructions in our [Security Advisory Form](https://github.com/shopware/shopware/security/advisories/new).
:::

## ACL in the Administration

The Access Control List (ACL) in Shopware ensures that by default, data can only be created, read, updated, or deleted (CRUD), once the user has specific privileges for a module. [ACL in the Administration](../../concepts/framework/architecture/administration-concept#acl-in-the-administration)

## API aware field

The `ApiAware` flag allows you to control what fields of your entity are exposed to the Store API. For more information, refer to [Flags Reference](core-reference/dal-reference/flags-reference).

## Captcha

Captchas help to verify the user's humanity and prevent automated bots or scripts from gaining access. For more information, refer to [Captcha](https://docs.shopware.com/en/shopware-en/settings/basic-information#captcha) article.

## CSP

[Content Security Policies](https://developer.mozilla.org/en-US/docs/Web/HTTP/CSP) (CSPs) are used to prevent Cross-Site-Scripting (XSS) attacks, as well as data injection attacks. This policy specifies the sources from which additional content (e.g., images, scripts, etc.) can be included.

The default policies are configured over the `shopware.security.csp_templates` symfony container parameter and can be adjusted over the container configuration.

## File access

Shopware 6 stores and processes a wide variety of files. This goes from product images or videos to generated documents such as invoices or delivery notes. This data should be stored securely, and backups should be generated regularly. For more information, refer to [File system](../../guides/hosting/infrastructure/filesystem)

## GDPR compliance

General Data Protection Regulation (GDPR) is a comprehensive European Union (EU) regulation that enhances individuals' privacy rights by imposing strict rules on how organizations collect, process, and protect personal data. For more information, refer to [GDPR](https://docs.shopware.com/en/shopware-6-en/tutorials-and-faq/gdpr) guide.

## HTML sanitizer

HTML sanitizer improves security, reliability, and usability of the text editor by removing potentially unsafe or malicious HTML code. For more information, refer to [HTML Sanitizer](../../guides/hosting/configurations/shopware/html-sanitizer.md) guide.

## Rate limiter

Shopware 6 provides certain rate limits by default that reduces the risk of brute-force attacks for pages like login or password reset. For more information, refer to [Rate Limiter](../../guides/hosting/infrastructure/rate-limiter.md) guide.

## Reset sessions when changing password

As soon as a password is changed for a user or customer, the session is invalid and the user or customer must log in again. For more information, refer to:

* [User Changelog](https://github.com/shopware/shopware/commit/5ea99ee5d7a12bab3a01a64c3948eee7c4188ede)
* [Customer Changelog](https://github.com/shopware/shopware/commit/47b4b094c13f62db860be2f431138bb45c0bd0b6)

## SameSite cookie

SameSite prevents the browser from sending cookies along with cross-site requests. For more information on this, refer to [SameSite Protection](../../guides/hosting/configurations/framework/samesite-protection.md).

## Security plugin

Obtaining security fixes without version upgrades is possible through the [Security plugin](../../guides/hosting/installation-updates/cluster-setup.md#security-plugin).

## Storefront IP Whitelisting

To enable access even during maintenance mode, IP addresses can be added to [Storefront IP whitelisting](https://docs.shopware.com/en/shopware-6-en/settings/saleschannel#status).

## SQL injection

SQL injection allows an attacker to execute new or modify existing SQL statements to access information that they are not allowed to access. By mainly using our own [Data Abstraction Layer](/docs/concepts/framework/data-abstraction-layer.html), that does not expose SQL directly, most of the SQL injection attack vectors are prevented. Whenever direct SQL is being used, the [best practices from Doctrine DBAL](https://www.doctrine-project.org/projects/doctrine-dbal/en/current/reference/security.html) are followed to ensure proper escaping of user input.

---

---

## search.md
**Source:** [search.md](https://developer.shopware.com/search.md)  
---

---

## themes.md
**Source:** [themes.md](https://developer.shopware.com/themes.md)  
---

---

## Home
**Source:** [v6.4.md](https://developer.shopware.com/docs/v6.4.md)  
# Home

Let us help you guide through the landscape of knowledge for Shopware 6. This documentation is organised in order to facilitate knowledge for different **products**, **topics** and **depths** of interest.

The two main sections **concepts** and **guides** assist you to navigate the documentation according to your needs.

Whereas **Concepts** convey the ideas, inner workings and architectural considerations behind our product, **Guides** provide explicit examples, step-by-step tutorials that deal with specific tasks.

These two sections are complemented by the **References**, which contain structured code references, lists of flags, commands, endpoints which are useful for development.

Visit the [academy](https://academy.shopware.com/collections?category=developer-sw6) for video content. If you have any questions left, you can always ask them on [StackOverflow](https://stackoverflow.com/questions/tagged/shopware6?tab=Newest) or join our awesome community on [Slack](https://slack.shopware.com/).

![](.gitbook/assets/readme-splash.png)

## Need help getting started?

---

---

## Home
**Source:** [v6.5.md](https://developer.shopware.com/docs/v6.5.md)  
# Home

Let us help you guide through the landscape of knowledge for Shopware 6. This documentation is organised in order to facilitate knowledge for different **products**, **topics** and **depths** of interest.

The two main sections **concepts** and **guides** assist you to navigate the documentation according to your needs.

Whereas **Concepts** convey the ideas, inner workings and architectural considerations behind our product, **Guides** provide explicit examples, step-by-step tutorials that deal with specific tasks.

These two sections are complemented by the **References**, which contain structured code references, lists of flags, commands, endpoints which are useful for development.

Visit the [academy](https://academy.shopware.com/collections?category=developer-sw6) for video content. If you have any questions left, you can always ask them on [StackOverflow](https://stackoverflow.com/questions/tagged/shopware6?tab=Newest) or join our awesome community on [Slack](https://slack.shopware.com/).

![](assets/readme-splash.png)

---

---

## Home
**Source:** [v6.6.md](https://developer.shopware.com/docs/v6.6.md)  
# Home

Let us help you guide through the landscape of knowledge for Shopware 6. This documentation is organised in order to facilitate knowledge for different **products**, **topics** and **depths** of interest.

The two main sections **concepts** and **guides** assist you to navigate the documentation according to your needs.

Whereas **Concepts** convey the ideas, inner workings and architectural considerations behind our product, **Guides** provide explicit examples, step-by-step tutorials that deal with specific tasks.

These two sections are complemented by the **References**, which contain structured code references, lists of flags, commands, endpoints which are useful for development.

Visit the [academy](https://academy.shopware.com/collections?category=developer-sw6) for video content. If you have any questions left, you can always ask them on [StackOverflow](https://stackoverflow.com/questions/tagged/shopware6?tab=Newest) or join our awesome community on [Slack](https://slack.shopware.com/).

![Readme](assets/readme-splash.png)

---

---

## what-is-shopware.md
**Source:** [what-is-shopware.md](https://developer.shopware.com/what-is-shopware.md)  
---

---

