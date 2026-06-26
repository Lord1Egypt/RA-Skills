# RELEASE AND UPGRADES

Compiled excerpts from the Shopware Developer Documentation snapshot. Prefer live docs at [developer.shopware.com](https://developer.shopware.com/) when in doubt.

---

## Release notes Shopware 6.7.2.0
**Source:** [release-notes/6.7/6.7.2.0.md](https://developer.shopware.com/release-notes/6.7/6.7.2.0.md)  
*(Body truncated in this bundle; follow the link for the rest.)*

# Release notes Shopware 6.7.2.0

## Abstract

Shopware 6.7.2.0 focuses on performance, developer experience, and stability. Highlights include OpenSearch query and sorting optimizations, more efficient property filter loading, dynamic sidebar category loading, and improvements to the administration search indexing. This release adds new extension points (like Cart Rule Loader and Guest Logout events), the ability to use custom route names in the Storefront, additional endpoints in the Storefront OpenAPI schema, and UI extension points for sidebar apps. It also includes numerous bug fixes and quality-of-life improvements.

## System requirements

* tested on PHP 8.2 and 8.4
* tested on MySQL 8 and MariaDB 11

## Improvements

### Performance Improvements

Multiple performance bottlenecks were resolved, mainly addressing negative performance impact with growing data sets.

#### Optimized OpenSearch Querying for product listing

The way that sorting is handled when using OpenSearch was greatly improved in cases where translated fields where used for sorting, e.g. product names.

Additionally, the queries were optimized to prevent nested queries, further improving performance. Overall, this can improve the OpenSearch query time by up to 85%.

#### Dynamic category level loading

The category tree's loading was changed so that the active levels for the sidebar navigation are loaded dynamically to always show available child categories, independently of the `navigation depth` setting in the sales channel config.

This means that the `navigation depth` setting is now mainly responsible for the header navigation depth.
In cases where that setting was increased to support deeper nesting levels in the sidebar navigation, it can be set to a lower value again, which will positively affect performance.

#### Optimized property group loading

The way in which the property groups for listing filters are loaded was improved. This mainly involved optimizing the SQL queries to avoid pagination (which gets slower with more data) and perform fewer joins.
Additionally, the sorting of the properties in the group was improved to use a more performant algorithm.
This will improve the performance of loading the property filters by up to 50%, especially with a large number of property filters.

### Efficiency Improvements

#### Lower memory footprint on data imports

Memory usage, especially when importing a lot of custom fields, could be greatly reduced by reusing dynamic field definition objects and more efficient validator constraint caching.

Additionally, a memory leak in HTMLSanitize was fixed, which increased memory usage the more sanitized fields were written in a single request.

This makes shopware more memory efficient, especially when writing bigger batches of data in a single request.

#### More efficient administration OpenSearch indexing

The indexing for the administration search indices on OpenSearch was improved to only reindex entities when search-relevant data was changed and not directly when any change happened to the entity.

### Return address in documents

The option `Display company` address in the `Company settings` section of the document configuration is now split into `Display return address` and `Display company address`.\
The former toggles the display of the return address above the customer address in the address block.\
The latter toggles the display of the company address below the header on the right-hand side of the document.

### Quality of Life Improvement: Administration forwards to the correct path after Login

When you open the administration with a deep link (e.g. to product list or order page), and you'll get redirected to the login first, you will now be forwarded to the original page you wanted to visit after sucessful login instead of always landing on the dashboard after login.

### More custom field set support in Apps

Apps can now also register custom field sets for the `Unit` and `Newsletter Recipient` entities.

### Better accessibility with ARIA labels

Slider links now include descriptive text that can be read by screen readers, making it easier for people with visual impairments to navigate your content.

### Faster loading with fetchpriority

This improves the Largest Contentful Paint (LCP), an important metric for PageSpeed and Google’s Core Web Vitals.

In Adminstration panel, a new config setting for fetchpriority to image slider and image gallery in CMS configuration was added.

### More control with configurable meta robots tags

Decide whether certain pages should be indexed by search engines or not. This gives you more flexibility and helps avoid issues like duplicate content.

It is also possible to override global settings for individual categories, landing pages etc. Open the respective entity, go to SEO tab and set the Meta robots option as needed.

### More improvements

* App user change – API requests can now be executed in the context of a specific app user.
* Storefront OpenAPI schema – extended with additional GET methods.
* Symfony profiler – cart data is now visible in the profiler.
* Cart rule loader extension event – new event for extending cart rules.
* Custom route names – custom route names for storefront routes are now possible.
* App custom fields – support for the unit and newsletter\_recipient entities.
* New commands – commands to schedule and deactivate tasks.
* Guest logout manipulation event – new event for guest logout processes.
* Sidebar apps in CMS detail pages – apps can now also be integrated into CMS detail pages.

Please checkout the [changelog](https://github.com/shopware/shopware/blob/v6.7.2.0/CHANGELOG.md) for more detailed information.

## Fixed bugs

* [#11769](https://github.com/shopware/shopware/issues/11769) Input quantity for extended prices incorrect
* [#11804](https://github.com/shopware/shopware/issues/11804) Fix display of line item taxes with tax provider
* [#11420](https://github.com/shopware/shopware/issues/11420) Fix navigation cache invalidation
* [#11654](https://github.com/shopware/shopware/issues/11654) Fixing document squished line item listing
* [#11906](https://github.com/shopware/shopware/issues/11906) Fix forwarding after login
* [#10721](https://github.com/shopware/shopware/issues/10721) Properly align logout link with icon
* [#11731](https://github.com/shopware/shopware/issues/11731) Fix login page redirect parameters
* [#11314](https://github.com/shopware/shopware/issues/11314) config endpoints cached indefinitely

::: details Click to see more fixed bugs

* [#10491](https://github.com/shopware/shopware/issues/10491) Implemented a command to download and install translation
* [#10528](https://github.com/shopware/shopware/issues/10528) Remove superfluous vat-id block from address-form.html.twig
* [#10530](https://github.com/shopware/shopware/issues/10530) Allow admininistration scripts being provided by bundles
* [#10556](https://github.com/shopware/shopware/issues/10556) min search term is now configurable
* [#10751](https://github.com/shopware/shopware/issues/10751) Add search sorting for live search
* [#10866](https://github.com/shopware/shopware/issues/10866) Allow Storefront routes without prefix
* [#10870](https://github.com/shopware/shopware/issues/10870) Improve basic captcha accessibility
* [#10878](https://github.com/shopware/shopware/issues/10878) Fix order version for determining credit notes when creating credit notes
* [#10959](https://github.com/shopware/shopware/issues/10959) Use createdAt column as default for product list sort
* [#11083](https://github.com/shopware/shopware/issues/11083) Reduce event bus usage for AddCacheTagEvent
* [#11108](https://github.com/shopware/shopware/issues/11108) AR Placement
* [#11139](https://github.com/shopware/shopware/issues/11139) refresh measurement units
* [#11167](https://github.com/shopware/shopware/issues/11167) category path does not display
* [#11188](https://github.com/shopware/shopware/issues/11188) Reset UpdatedByField for updates via API
* [#11191](https://github.com/shopware/shopware/issues/11191) Implement soft purge HTTP cache functionality
* [#11202](https://github.com/shopware/shopware/issues/11202) Change class constants to self classes
* [#11205](https://github.com/shopware/shopware/issues/11205) Deprecated EntityDefinition constructor
* [#11215](https://github.com/shopware/shopware/issues/11215) Restore ResetInterface support in long-running runtimes
* [#11222](https://github.com/shopware/shopware/issues/11222) Update DBAL to 4.3.1
* [#11223](https://github.com/shopware/shopware/issues/11223) Copy app snippets after system language change
* [#11282](https://github.com/shopware/shopware/issues/11282) add cart rule loader extension event
* [#11297](https://github.com/shopware/shopware/issues/11297) Replace AddCacheTagEvent's with CacheTagCollector addTag
* [#11327](https://github.com/shopware/shopware/issues/11327) Add missing context config setting access optional chaining
* [#11341](https://github.com/shopware/shopware/issues/11341) Correctly delete bearerAuth cookie from base path in administration
* [#11373](https://github.com/shopware/shopware/issues/11373) Fix sidebar SDK handlers in Meteor page
* [#11391](https://github.com/shopware/shopware/issues/11391) Add missing ApiAware flag to CmsBlock & CmsSection id's
* [#11409](https://github.com/shopware/shopware/issues/11409) Add missing timezone option for TimeRangeRule
* [#11410](https://github.com/shopware/shopware/issues/11410) Allow child classes for getting extension of type
* [#11417](https://github.com/shopware/shopware/issues/11417) Fix media thumbnail sizes with mediaThumbnailSizeId
* [#11466](https://github.com/shopware/shopware/issues/11466) Allow for LineItemFactoryHandler decoration
* [#11485](https://github.com/shopware/shopware/issues/11485) Skip persisting admin snippets for non-existing locales
* [#11491](https://github.com/shopware/shopware/issues/11491) Remove FK delete exception handler
* [#11492](https://github.com/shopware/shopware/issues/11492) Fix ThemeCompiler side effects
* [#11510](https://github.com/shopware/shopware/issues/11510) allow configuring the minimum search term length
* [#11515](https://github.com/shopware/shopware/issues/11515) Fix reset active apps after app deactivation
* [#11521](https://github.com/shopware/shopware/issues/11521) fix: improve check for visibility parameter check, fixes #11521 (#11565)
* [#11551](https://github.com/shopware/shopware/issues/11551) Increased minimum required version of MySQL database
* [#11551](https://github.com/shopware/shopware/issues/11551) Symfony components updated
* [#11566](https://github.com/shopware/shopware/issues/11566) Add Design Tokens to the Smart Bar
* [#11578](https://github.com/shopware/shopware/issues/11578) Add dark mode support to sidebar
* [#11582](https://github.com/shopware/shopware/issues/11582) Added dark mode support to select components
* [#11583](https://github.com/shopware/shopware/issues/11583) Fix state machine history FK constraint to integration
* [#11599](https://github.com/shopware/shopware/issues/11599) Change createdComponent back to being sync
* [#11604](https://github.com/shopware/shopware/issues/11604) Copy context rules to ESI request context
* [#11608](https://github.com/shopware/shopware/issues/11608) Add app user ID header and fix domain exception patterns
* [#11633](https://github.com/shopware/shopware/issues/11633) Fix mediaThumbnailSizeId not null in MediaThumbnailEntity
* [#11636](https://github.com/shopware/shopware/issues/11636) Fix service menu wrap
* [#11650](https://github.com/shopware/shopware/issues/11650) Fix ScriptLoader loading invalid cache paths
* [#11653](https://github.com/shopware/shopware/issues/11653) Add aria-label to image slider links
* [#11670](https://github.com/shopware/shopware/issues/11670) Add commands to schedule and disable scheduled tasks
* [#11702](https://github.com/shopware/shopware/issues/11702) 

… **Truncated.** Full document: https://developer.shopware.com/release-notes/6.7/6.7.2.0.md


---

## Release notes Shopware 6.7.2.1
**Source:** [release-notes/6.7/6.7.2.1.md](https://developer.shopware.com/release-notes/6.7/6.7.2.1.md)  
# Release notes Shopware 6.7.2.1

## Abstract

This security patch contains a XSS vulnerability fix as well as a critical bug fix. Please update immediately if possible. Otherwise please refer to the updated version of [Shopware Security Plugin](https://store.shopware.com/en/swag136939272659f/shopware-6-security-plugin.html) v4.0.0.

## System requirements

* tested on PHP 8.2 and 8.4
* tested on MySQL 8 and MariaDB 11

## Improvements

(No notable improvements in this patch release)

## Fixed bugs

* [GHSA-9v82-vcjx-m76j](https://github.com/shopware/shopware/security/advisories/GHSA-9v82-vcjx-m76j) Properly escape active route params
* [12363](https://github.com/shopware/shopware/pull/12363) fix: missing product rule filter (backport: 6.7.2.x)

## Credits

Thanks to all diligent friends for helping us make Shopware better and better with each pull request!

## More resources

* [Detailed diff on Github](https://github.com/shopware/shopware/compare/v6.7.2.0...v6.7.2.1) to the former version
* [Changelog on GitHub](https://github.com/shopware/shopware/blob/v6.7.2.1/CHANGELOG.md) for this version.
* [Installation overview](https://developer.shopware.com/docs/guides/installation/)
* [Update from a previous installation](https://developer.shopware.com/docs/guides/installation/template.html#update-shopware)

## Get in touch

Discuss about decisions, bugs you might stumble upon, etc in our [community discord](https://chat.shopware.com). See you there ;)

---

---

## Release notes Shopware 6.7.2.2
**Source:** [release-notes/6.7/6.7.2.2.md](https://developer.shopware.com/release-notes/6.7/6.7.2.2.md)  
# Release notes Shopware 6.7.2.2

## Abstract

This patch release contains three bug fixes

## System requirements

* tested on PHP 8.2 and 8.4
* tested on MySQL 8 and MariaDB 11

## Improvements

(No notable improvements in this patch release)

## Fixed bugs

* [12503](https://github.com/shopware/shopware/pull/12503) fix: disable profiler in production (backport: 6.7.2.x)
* [12434](https://github.com/shopware/shopware/issues/12434) Customer address gets stuck on non-default address when changed during checkout
* [12472](https://github.com/shopware/shopware/blob/v6.7.2.2/changelog/release-6-7-2-2/2025-09-10-fix-type-cast-system-config-validation.md) Fix type error when using named arguments in the Length validation constraint

## Credits

Thanks to all diligent friends for helping us make Shopware better and better with each pull request!

* [Grzegorz Jan Rolka](https://github.com/grzegorzrolka)

## More resources

* [Detailed diff on Github](https://github.com/shopware/shopware/compare/v6.7.2.1...v6.7.2.2) to the former version
* [Changelog on GitHub](https://github.com/shopware/shopware/blob/v6.7.2.2/CHANGELOG.md) for this version.
* [Installation overview](https://developer.shopware.com/docs/guides/installation/)
* [Update from a previous installation](https://developer.shopware.com/docs/guides/installation/template.html#update-shopware)

## Get in touch

Discuss about decisions, bugs you might stumble upon, etc in our [community discord](https://chat.shopware.com). See you there ;)

---

---

## Release notes Shopware 6.7.3.0
**Source:** [release-notes/6.7/6.7.3.0.md](https://developer.shopware.com/release-notes/6.7/6.7.3.0.md)  
*(Body truncated in this bundle; follow the link for the rest.)*

# Release notes Shopware 6.7.3.0

## Abstract

The language handling completely moved to the core, no plugin necessary from now on. Also, American English is pre-installed as one of the default languages. Additionally, this release comes with at least 161 bug fixes.

## System requirements

* tested on PHP 8.2 and 8.4
* tested on MySQL 8 and MariaDB 11

## Improvements

### Language handling

#### American English can be used in installer

American English can now be downloaded in the installer and can become the default shop language like any other language in Shopware.

#### Available languages can be managed from Shopware core

No plugin needed anymore to install languages available from the [Shopware translation platform](http://translate.shopware.com)! The entire plugin has been built into the core. Simply fetch and activate the language of your choice via the new `bin/console` commands. Later, this feature will become available in administration.

However, for any other language pack not available from the Shopware  translation platform, you will still need a plugin.

You can fetch Shopware translations from the Shopware translation platform, which are stored on [Github](https://github.com/shopware/translations/). You can even help provide translations and use them in your shop a short time later!

Please note: As these are community-provided translations, we cannot guarantee that everything is translated 100% correctly.

Good news: The Language Pack plugin will continue to be maintained under our usual [release policy](https://developer.shopware.com/release-notes/).

Please see the [ADR](https://github.com/shopware/shopware/blob/trunk/adr/2025-06-03-integrating-the-language-pack-into-platform.md) for more details.

### Country-Agnostic Language Layer

Working with language codes in Shopware, such as `en-GB` (a combination of language and country), generally works well. However, this approach can be quite maintenance-heavy: using multiple dialects, for example, British and American English, always leads to duplicated language snippets and can quickly become frustrating for translators.

To address this, we introduced an additional translation layer that reduces dialects to patch files, limiting duplication to only a small portion of the snippets.

Read the full story in this [ADR](https://github.com/shopware/shopware/blob/trunk/adr/2025-09-01-adding-a-country-agnostic-language-layer.md). You can also find a detailed [concept document](https://developer.shopware.com/docs/concepts/translations/fallback-language-selection.html) for further reference.

### CMS / Shopping Experience

#### Block type labels

See the type of blocks directly when working with it as an editor. This is especially useful if using third party plugins. Thanks to [@amenk](https://github.com/amenk)!

https://github.com/shopware/shopware/pull/12334

#### 3D/canvas switching

Slider viewers are now rendered in respect to their visibility modus. This gives us a bit of more performance. Thanks to [@ffrank913](https://github.com/ffrank913) ;)

https://github.com/shopware/shopware/pull/12642

### Performance: Faster product category loading with a new index

Thanks to this pull request, queries on `product.categories` shall run ways faster than before: See https://github.com/shopware/shopware/pull/12657 by [@vienthuong](https://github.com/vienthuong)

### Checkout & Promotions: More reliable shipping price matrix, credit notes, and promotion discount calculations

* https://github.com/shopware/shopware/pull/12560 by [@untilu29](https://github.com/untilu29) actually fixes [Shipping method cannot be applied to products below 1 EUR due to “Cart price from” default](https://github.com/shopware/shopware/issues/12430) by [@cramytech](https://github.com/cramytech).
* https://github.com/shopware/shopware/pull/12589 by [@ennasus4sun](https://github.com/ennasus4sun) fixes [Credit notes are created cumulatively](https://github.com/shopware/shopware/issues/11381) by [@swagTKA](https://github.com/swagTKA).
* https://github.com/shopware/shopware/pull/12603 by [@socrec](https://github.com/socrec) fixes [Fixed Price delivery promotions cannot be excluded](https://github.com/shopware/shopware/issues/12159) by [janobi](https://github.com/janobi)

### 3D Viewer: Improved visuals with better camera distance and model placement

* https://github.com/shopware/shopware/pull/12682 by [ffrank913](https://github.com/ffrank913) fixes [Incorrect model focus in SW6 standard CMS](https://github.com/shopware/shopware/issues/12655) by [himself](https://github.com/ffrank913)
* https://github.com/shopware/shopware/pull/12654 by [ffrank913](https://github.com/ffrank913) fixes [Incorrect frontend display of 3D glb files in SW6 standard CMS](https://github.com/shopware/shopware/issues/12632) by [MaximilianFo](https://github.com/MaximilianFo)

### More tech updates

* Framework & API: Store-API cookie groups, new route exception handling, cleaner query parsing
* Platform ops / DX: Environment variable improvements, cache directory configurability, profiler disabled by default in production
* Build tooling: Admin build target updated to ES2023 (plugin authors should check compatibility)
* Deprecations:
  * Deprecation of controllerName/controllerAction variables in templates
  * Deprecation of SalesChannelContextSwitcher
* Upgrade notes: DB migration for the new category index, admin build target upgrade, profiler defaults

Please checkout the [changelog](https://github.com/shopware/shopware/blob/v6.7.3.0/CHANGELOG.md) for more detailed information.

## Fixed bugs

* [#7780](https://github.com/shopware/shopware/issues/7780) - Limit cache permutations due to rules to improve TCO and page load performance
* [#12231](https://github.com/shopware/shopware/issues/12231) - fix: change background color on even data grid rows
* [#12234](https://github.com/shopware/shopware/issues/12234) - fix: saas related permissions missing in test (backport: 6.7.3.x)

::: details Click to see more fixed bugs

* [#12223](https://github.com/shopware/shopware/issues/12223) - fix: saas related permissions missing in test
* [#12212](https://github.com/shopware/shopware/issues/12212) - fix: Composer plugins can be removed when in custom/plugins
* [#12224](https://github.com/shopware/shopware/issues/12224) - fix: Media thumbnail generation with null media thumbnail size
* [#12208](https://github.com/shopware/shopware/issues/12208) - chore: Enable overwriteVariablesWithLoop phpstan parameter
* [#12176](https://github.com/shopware/shopware/issues/12176) - fix: Consider parent sources in api aware flag
* [#12363](https://github.com/shopware/shopware/issues/12363) - fix: missing product rule filter (backport: 6.7.2.x)
* [#12357](https://github.com/shopware/shopware/issues/12357) - chore: add missing assertions in tests of core/content integration suite
* [#12318](https://github.com/shopware/shopware/issues/12318) - fix: Zugferd invoice BasisQuantity should not be lineitem quantity
* [#12358](https://github.com/shopware/shopware/issues/12358) - chore: add missing assertions in tests of core/system integration suite
* [#12356](https://github.com/shopware/shopware/issues/12356) - chore: add missing assertions in tests of core/framework integration suite
* [#12241](https://github.com/shopware/shopware/issues/12241) - ci(deps): bump the all group across 1 directory with 7 updates
* [#12314](https://github.com/shopware/shopware/issues/12314) - feat: Add ScheduledTaskMessageInterface
* [#12311](https://github.com/shopware/shopware/issues/12311) - fix: improve tags, update config endpoint OpenAPI schema
* [#12346](https://github.com/shopware/shopware/issues/12346) - chore: Enable closureUsesThis phpstan parameter
* [#12214](https://github.com/shopware/shopware/issues/12214) - fix: intra community zugferd invoice
* [#12332](https://github.com/shopware/shopware/issues/12332) - feat: add visual test for Themes
* [#12204](https://github.com/shopware/shopware/issues/12204) - chore: Enable several phpstan strict rules
* [#12205](https://github.com/shopware/shopware/issues/12205) - chore: Enable disallowedImplicitArrayCreation phpstan parameter
* [#12249](https://github.com/shopware/shopware/issues/12249) - feat: interpret checkbox custom fields as bool in rules
* [#12266](https://github.com/shopware/shopware/issues/12266) - fix: apply sales channel specific settings for showing product reviews
* [#12263](https://github.com/shopware/shopware/issues/12263) - fix: load core snippets in Shopware 6.8.0
* [#12406](https://github.com/shopware/shopware/issues/12406) - chore: merge back into trunk 6.7.2.1 (backport: 6.7.3.x)
* [#12403](https://github.com/shopware/shopware/issues/12403) - chore: merge back into trunk 6.7.2.1
* [#12230](https://github.com/shopware/shopware/issues/12230) - feat: allow accessing vite dev server with any host
* [#12371](https://github.com/shopware/shopware/issues/12371) - fix: provide discount id to discount component card
* [#12407](https://github.com/shopware/shopware/issues/12407) - fix: contribution typo
* [#12362](https://github.com/shopware/shopware/issues/12362) - fix: apply request limit for product store-api endpoints again
* [#12228](https://github.com/shopware/shopware/issues/12228) - feat: improve languages admin ui resolves #11414
* [#12408](https://github.com/shopware/shopware/issues/12408) - feat: update tsc target version for administration to ES2023
* [#12427](https://github.com/shopware/shopware/issues/12427) - fix: Update test for seo url persister
* [#11099](https://github.com/shopware/shopware/issues/11099) - fix: Wrong customer context on login if entry from sales\_channel\_api\_context table is expired
* [#12455](https://github.com/shopware/shopware/issues/12455) - fix: Update test for seo url persister (backport: 6.7.3.x)
* [#12458](https://github.com/shopware/shopware/issues/12458) - fix: Wrong customer context on login if entry from sales\_channel\_api\_context table is expired (backport: 6.7.3.x)
* [#12319](https://github.com/shopware/shopware/issues/12319) - feat: Add handle to get router path
* [#12439](https://github.com/shopware/shopware/issues/12439) - chore: improve ThemePrepareIconsCommandTest and prevent parsing empty files in ThemePrepareIconsCommand
* [#12377](https://github.com/shopware/shopware/issues/12377) - chore: disallow risky tests for phpunit (devops, integration, unit)
* [#12444](https://github.com/shopware/shopware/issues/12444) - chore: Fix document\_base\_config migration
* [#12418](https://github.com/shopware/shopware/issues/12418) - fix: initialization of DiscountCampaignStruct, add additional properties
* [#12453](https://github.com/shopware/shopware/issues/12453) - test: use named argument for constraint in EntityNotExistsValidatorTest
* [#12435](https://github.com/shopware/shopware/issues/12435) - fix: cast XML config values for Length constraint to int to prevent type errors
* [#12390](https://github.com/shopware/shopware/issues/12390) - fix: fix email recovery in admin login
* [#12463](https://github.com/shopware/shopware/issues/12463) - fix: initialization of DiscountCampaignStruct, add additional properties (backport: 6.7.3.x)
* [#12342](https://github.com/shopware/shopware/issues/12342) - chore: Change invitation mail wording
* [#12180](https://github.com/shopware/shopware/issues/12180) - fix: revert theme field name change
* [#12472](https://github.com/shopware/shopware/issues/12472) - fix: cast XML config values for Length constraint to int to prevent type errors (backport: 6.7.2.x)
* [#12474](https://github.com/shopware/shopware/issues/12474) - fix: theme config boolean values
* [#12484](https://github.com/shopware/shopware/issues/12484) - fix: theme config boolean values (backport: 6.7.3.x)
* [#12466](https://github.com/shopware/shopware/issues/12466) - fix: deletion of active customer address
* [#12490](https://github.com/shopware/shopware/issues/12490) - fix: media search is partially broken
* [#12436]

… **Truncated.** Full document: https://developer.shopware.com/release-notes/6.7/6.7.3.0.md


---

## Release notes Shopware 6.7.3.1
**Source:** [release-notes/6.7/6.7.3.1.md](https://developer.shopware.com/release-notes/6.7/6.7.3.1.md)  
# Release notes Shopware 6.7.3.1

## Abstract

This patch release contains security and other bug fixes. Please make sure to update immediately or use the latest version of the [Shopware Security Plugin](https://store.shopware.com/en/swag136939272659f/shopware-6-security-plugin.html) if you cannot update right now.

## System requirements

* tested on PHP 8.2 and 8.4
* tested on MySQL 8 and MariaDB 11

## Improvements

(No notable improvements in this patch release)

## Fixed bugs

### Security bulletins

* [GHSA-m895-2hj3-8cg9](https://github.com/shopware/shopware/security/advisories/GHSA-m895-2hj3-8cg9) Reading media entities by aggregating fields individually bypasses MediaVisibilityRestrictionSubscriber
* [GHSA-27c9-vp3w-6ww8](https://github.com/shopware/shopware/security/advisories/GHSA-27c9-vp3w-6ww8) Exposure of sensitive user information via CSV export mapping
* [GHSA-3cpp-fv95-mpr5](https://github.com/shopware/shopware/security/advisories/GHSA-3cpp-fv95-mpr5) Server-Side Request Forgery (SSRF) – order invoice
* [GHSA-6wh5-mw9h-5c3w](https://github.com/shopware/shopware/security/advisories/GHSA-6wh5-mw9h-5c3w) Path traversal via Plugin upload
* [GHSA-r2vg-hvjm-fg38](https://github.com/shopware/shopware/security/advisories/GHSA-r2vg-hvjm-fg38) Customer Orders can be canceled, even if refunds are disabled

### Other fixed bugs

* [12884](https://github.com/shopware/shopware/issues/12884) Legacy Cookie definitions could break
* [12885](https://github.com/shopware/shopware/issues/12885) With Shopware 6.7.3, it's no longer possible to change the delivery or billing address in the checkout
* [12888](https://github.com/shopware/shopware/pull/12888) fix: api encode issue with partial entity (backport: 6.7.3.x)
* [12899](https://github.com/shopware/shopware/pull/12899) fix: address manager create form (backport: 6.7.3.x)
* [12506](https://github.com/shopware/shopware/issues/12506) CartPromotionsDataDefinition::removeCode() may fail when codes are returned as int from getAllCodes()
* [12075](https://github.com/shopware/shopware/pull/12075) fix: Admin es search for "document number" doesn't return any results
* [12363](https://github.com/shopware/shopware/pull/12363) fix: missing product rule filter
* [12472](https://github.com/shopware/shopware/pull/12472) fix: cast XML config values for Length constraint to int to prevent type errors
* [12434](https://github.com/shopware/shopware/issues/12434) Customer address gets stuck on non-default address when changed during checkout
* [12979](https://github.com/shopware/shopware/pull/12979) compatibility with OpenSearch 3.x

## Credits

Thanks to all diligent friends for helping us make Shopware better and better with each pull request!

## More resources

* [Detailed diff on Github](https://github.com/shopware/shopware/compare/v6.7.3.0...v6.7.3.1) to the former version
* [Changelog on GitHub](https://github.com/shopware/shopware/blob/v6.7.2.3/CHANGELOG.md) for this version.
* [Installation overview](https://developer.shopware.com/docs/guides/installation/)
* [Update from a previous installation](https://developer.shopware.com/docs/guides/installation/template.html#update-shopware)

## Get in touch

Discuss about decisions, bugs you might stumble upon, etc in our [community discord](https://chat.shopware.com). See you there ;)

---

---

## Release notes Shopware 6.7.4.0
**Source:** [release-notes/6.7/6.7.4.0.md](https://developer.shopware.com/release-notes/6.7/6.7.4.0.md)  
*(Body truncated in this bundle; follow the link for the rest.)*

# Release notes Shopware 6.7.4.0

## Abstract

This minor release provides some interesting improvements under the hood for more stability, performance and software robustness. Additionally, this release comes with at least 148 bug fixes.

## System requirements

* tested on PHP 8.2 and 8.4
* tested on MySQL 8 and MariaDB 11

## Improvements

### Add message queue message size limit configuration option [#13007](https://github.com/shopware/shopware/pull/13007)

Added shopware.messenger.message\_max\_kib\_size config option to define the maximum size (in KiB) of messages in the message queue. Set to 0 to disable the size check. Defaults to 1024 KiB (1 MiB).

### Add save media modal [#12146](https://github.com/shopware/shopware/pull/13007)

This implements save media modal. Save media modal can be opened by Admin SDK <https://github.com/shopware/meteor/issues/819>.

### Prevent sending multiple page change events when query parameters change [#13203](https://github.com/shopware/shopware/pull/13203)

This change stops dispatching page changed events, if only query parameters changed.

### Separate Vimeo video cookies [#13096](https://github.com/shopware/shopware/pull/13096)

Vimeo and YouTube videos shared the same cookie consent in Shopware's storefront. When a user accepts the "YouTube video" cookie, both YouTube *and* Vimeo videos are loaded, violating proper GDPR compliance. Additionally, videos required a page reload to display after accepting cookies, creating a poor user experience.

Users should have granular control over which video platforms they consent to, and videos should load immediately upon consent.

This change introduces separate cookie consent handling for Vimeo and YouTube videos.

* Videos now load immediately when cookies are accepted (via "Accept all" or cookie configuration offcanvas)
* No page reload required
* Each video type independently checks its specific cookie

### Add possibility to set fetchpriority high in images [#13070](https://github.com/shopware/shopware/pull/13070)

Formerly, there was no way to add the attribute `fetchpriority="high"` to an image, loaded by the CMS image element. As it always depends on the content this should not be done automatically, but rather configurable.

This change adds a setting to add this attribute to the image. In this case we also do not use the `loading="lazy"` option.

### Apply new screen design to installer [#13191](https://github.com/shopware/shopware/pull/13191)

This change applies a new screen design to the installer and cleans up the former behaviour.

### Remove datepicker wrapper [#12948](https://github.com/shopware/shopware/pull/12948)

Formerly, there was a wrapper around the mt-datepicker to correct styling issues with the meteor component. The component `mt-datepicker` styling has now been corrected so this wrapper could be removed.

### Make product detail review form radio keyboard accessible [#13046](https://github.com/shopware/shopware/pull/13046)

The review rating radio buttons were not focusable because they used `display: none`. We updated the radio buttons to be visually hidden using `visually-hidden()` instead, making them focusable. Additionally, I added a box-shadow to the star label when its child radio is focused, so keyboard users have a visual indicator. Also, the vertical alignment between the stars and the rating text were improved.

### Fix Vite vulnerability in admin [#13149](https://github.com/shopware/shopware/pull/13149)

Bumped and pinned vite version due to vulnerability and audit fail: [GHSA-93m4-6634-74q7](https://github.com/advisories/GHSA-93m4-6634-74q7).

This is actually not security relevant for us or Shopware users as the vulnerability is just happening at the dev-server of vite. An attacker would have to have explicit access to the network of the local dev server which is not exposed at any point.

### Add sitemap entity query events for products, landing pages, and categories [#13082](https://github.com/shopware/shopware/pull/13082)

When changing the products which are shown in the sitemap, formerly it was necessary to decorate the `ProductUrlProvider`. However, it could be much more efficient, when "modifying" the query directly. This is why we added an event to modify the query builder when fetching products, landing pages and categories.

Please checkout the [changelog](https://github.com/shopware/shopware/blob/v6.7.4.0/CHANGELOG.md) for more detailed information.

## Fixed bugs

* [12994](https://github.com/shopware/shopware/issues/12994) fix: cache cookie handling to prevent cache poisioning
* [13079](https://github.com/shopware/shopware/issues/13079) fix: session locks issue
* [12936](https://github.com/shopware/shopware/issues/12936) fix: Clearance sale (stock handling) is ignored as soon as a product is in the cart

::: details Click to see more fixed bugs

* [10486](https://github.com/shopware/shopware/issues/10486) Subscriptions: Allow single purchases and subscriptions in one cart
* [13033](https://github.com/shopware/shopware/issues/13033) fix(phpstan): Add array/iterable types to Shopware\Core\System
* [13054](https://github.com/shopware/shopware/issues/13054) fix(ADR): Revert changes and supersede ADR instead
* [13046](https://github.com/shopware/shopware/issues/13046) fix: make product detail review form radio keyboard accessible
* [12672](https://github.com/shopware/shopware/issues/12672) fix: Change error output of app loader while running in CI env
* [12790](https://github.com/shopware/shopware/issues/12790) fix: fix custom fields configuration property for select
* [12831](https://github.com/shopware/shopware/issues/12831) fix: Proper display of the administrator switch in the integration create modal
* [12808](https://github.com/shopware/shopware/issues/12808) feat: add gitignore to plugin create command
* [12764](https://github.com/shopware/shopware/issues/12764) feat: add typescript-eslint/no-misused-spread
* [12834](https://github.com/shopware/shopware/issues/12834) fix: add missing .md extension to changelog
* [12860](https://github.com/shopware/shopware/issues/12860) chore: merge back v6.7.3.0
* [12798](https://github.com/shopware/shopware/issues/12798) chore(admin-snippets): Add auth-filter for fallback (backport: 6.7.3.x)
* [12833](https://github.com/shopware/shopware/issues/12833) fix: proper display of the administrator switch in the user create
* [12835](https://github.com/shopware/shopware/issues/12835) refactor: replace the latest sw-switch-field component with a bool input
* [12864](https://github.com/shopware/shopware/issues/12864) fix: entity listing in log events
* [12837](https://github.com/shopware/shopware/issues/12837) feat: add new twig blocks for product box
* [13187](https://github.com/shopware/shopware/issues/13187) chore: Add compatibility with node 25
* [12948](https://github.com/shopware/shopware/issues/12948) feat: remove datepicker wrapper
* [12924](https://github.com/shopware/shopware/issues/12924) refactor: cleanup after-sales styles
* [13108](https://github.com/shopware/shopware/issues/13108) fix: Add check for supported types
* [12971](https://github.com/shopware/shopware/issues/12971) feat: Update PHPStan and its plugins (10-2025)
* [12820](https://github.com/shopware/shopware/issues/12820) fix: tax free config
* [13158](https://github.com/shopware/shopware/issues/13158) fix: respect errorRoute parameter in captcha failure handler
* [13037](https://github.com/shopware/shopware/issues/13037) fix: improve select result list sometimes not loading the next page when scrolling to the bottom
* [13070](https://github.com/shopware/shopware/issues/13070) feat: Add possibility to set fetchpriority high in images
* [13082](https://github.com/shopware/shopware/issues/13082) feat: Add sitemap entity query events for products, landing pages and categories
* [13076](https://github.com/shopware/shopware/issues/13076) fix: verify what phpstan is doing with its cache result
* [13032](https://github.com/shopware/shopware/issues/13032) refactor: Use lists where we know that it is a list
* [13038](https://github.com/shopware/shopware/issues/13038) fix: Hide shopware.yaml danger warning on config-schema.json change
* [12755](https://github.com/shopware/shopware/issues/12755) refactor: Do not use the Symfony validator to validate the honeypot captcha
* [13007](https://github.com/shopware/shopware/issues/13007) feat: Add message queue message size limit config option
* [13083](https://github.com/shopware/shopware/issues/13083) fix: Typos in storefront.de.json
* [12979](https://github.com/shopware/shopware/issues/12979) feat: compatibility with OpenSearch 3.x
* [13065](https://github.com/shopware/shopware/issues/13065) fix: Use bordered switches in the sw-product-deliverability-form for a consistent look
* [13109](https://github.com/shopware/shopware/issues/13109) feat: Make sure only removals are made to the PHPStan baseline
* [13091](https://github.com/shopware/shopware/issues/13091) refactor: Change to correct native return type of CmsPageLoadedEvent
* [13087](https://github.com/shopware/shopware/issues/13087) fix: IAP decoding with old OpenSSL versions
* [12923](https://github.com/shopware/shopware/issues/12923) fix: Use agnostic language layer functionality when loading snippets
* [13119](https://github.com/shopware/shopware/issues/13119) fix: change light intensity in 3D viewer
* [12742](https://github.com/shopware/shopware/issues/12742) chore: revert fix: Fix base\_url validation
* [12744](https://github.com/shopware/shopware/issues/12744) chore: revert fix: Fix base\_url validation (backport: 6.7.3.x)
* [12776](https://github.com/shopware/shopware/issues/12776) ci: enable currents for install ats
* [12779](https://github.com/shopware/shopware/issues/12779) fix: missing empty state description
* [12767](https://github.com/shopware/shopware/issues/12767) test: remove skipping for rule test (backport: 6.7.3.x)
* [12760](https://github.com/shopware/shopware/issues/12760) test: remove skipping for rule test
* [12809](https://github.com/shopware/shopware/issues/12809) feat: add Mailpit configuration and HTTPS error handling for Playwrig…
* [12822](https://github.com/shopware/shopware/issues/12822) fix: package annotation affiliate tracking
* [12796](https://github.com/shopware/shopware/issues/12796) chore(admin-snippets): Add auth-filter for fallback
* [12795](https://github.com/shopware/shopware/issues/12795) chore(ci): update acceptance test snapshots
* [12791](https://github.com/shopware/shopware/issues/12791) fix: Add specific cms state page property to watcher
* [12939](https://github.com/shopware/shopware/issues/12939) chore(ci): update acceptance test snapshots
* [12937](https://github.com/shopware/shopware/issues/12937) fix: currency name instead of isoCode
* [12928](https://github.com/shopware/shopware/issues/12928) fix: import/export profile save (backport: 6.7.3.x)
* [12908](https://github.com/shopware/shopware/issues/12908) ci: fix milestone version detection (backport: 6.7.3.x)
* [12821](https://github.com/shopware/shopware/issues/12821) fix: installer fixes
* [12931](https://github.com/shopware/shopware/issues/12931) docs: Change wording of Symfony feature ADR to make its purpose clearer
* [12865](https://github.com/shopware/shopware/issues/12865) feat: Add aria-label to CMS image link
* [12887](https://github.com/shopware/shopware/issues/12887) fix: address manager create form
* [12836](https://github.com/shopware/shopware/issues/12836) fix: SalesChannelContext::state to reset to previous state
* [12898](https://github.com/shopware/shopware/issues/12898) fix: include /Test/ directories in classmap
* [12889](https://github.com/shopware/shopware/issues/12889) ci: fix milestone version detection
* [12578](https://github.com/shopware/shopware/issues/12578) feat(product analytics): Initial commit
* [12868](https://github.com/shopware/shopware/issues/12868) chore(filename-lint): Adjustments after exploratory te

… **Truncated.** Full document: https://developer.shopware.com/release-notes/6.7/6.7.4.0.md


---

## Release notes Shopware 6.7.4.1
**Source:** [release-notes/6.7/6.7.4.1.md](https://developer.shopware.com/release-notes/6.7/6.7.4.1.md)  
# Release notes Shopware 6.7.4.1

## Abstract

This patch release contains the fix for a security issue. Please update to this patch release as soon as possible. If you cannot update immediately, it is highly recommended to use the [Security Plugin](https://store.shopware.com/en/swag136939272659f/shopware-6-security-plugin.html).

## System requirements

* tested on PHP 8.2 and 8.4
* tested on MySQL 8 and MariaDB 11

## Improvements

(No notable improvements in this patch release)

## Fixed bugs

* [#GHSA-2w46-vq8h-98vh](https://github.com/shopware/shopware/security/advisories/GHSA-2w46-vq8h-98vh) Password recovery link does not expire after email change

## Credits

Thanks to all diligent friends for helping us make Shopware better and better with each pull request!

## More resources

* [Detailed diff on Github](https://github.com/shopware/shopware/compare/v6.7.4.0...v6.7.4.1) to the former version
* [Changelog on GitHub](https://github.com/shopware/shopware/blob/v6.7.4.1/CHANGELOG.md) for this version.
* [Installation overview](https://developer.shopware.com/docs/guides/installation/)
* [Update from a previous installation](https://developer.shopware.com/docs/guides/installation/template.html#update-shopware)

## Get in touch

Discuss about decisions, bugs you might stumble upon, etc in our [community discord](https://chat.shopware.com). See you there ;)

---

---

## Release notes Shopware 6.7.4.2
**Source:** [release-notes/6.7/6.7.4.2.md](https://developer.shopware.com/release-notes/6.7/6.7.4.2.md)  
# Release notes Shopware 6.7.4.2

## Abstract

This patch release contains four bug fixes.

## System requirements

* tested on PHP 8.2 and 8.4
* tested on MySQL 8 and MariaDB 11

## Improvements

(No notable improvements in this patch release)

## Fixed bugs

* [#13305](https://github.com/shopware/shopware/issues/13305) Viewing star ratings is broken
* [#13387](https://github.com/shopware/shopware/issues/13387) Storefront bundle missing system.xml loading prevents SalesChannelAnalyticsLoader service registration
* [#13434](https://github.com/shopware/shopware/issues/13434) Block shipping method
* [#13321](https://github.com/shopware/shopware/issues/13321) Guest checkout - Change default address results in 403 Forbidden error

## Credits

Thanks to all diligent friends for helping us make Shopware better and better with each pull request!

## More resources

* [Detailed diff on Github](https://github.com/shopware/shopware/compare/v6.7.4.1...v6.7.4.2) to the former version
* [Changelog on GitHub](https://github.com/shopware/shopware/blob/v6.7.4.2/CHANGELOG.md) for this version.
* [Installation overview](https://developer.shopware.com/docs/guides/installation/)
* [Update from a previous installation](https://developer.shopware.com/docs/guides/installation/template.html#update-shopware)

## Get in touch

Discuss about decisions, bugs you might stumble upon, etc in our [community discord](https://chat.shopware.com). See you there ;)

---

---

## Release notes Shopware 6.7.5.0
**Source:** [release-notes/6.7/6.7.5.0.md](https://developer.shopware.com/release-notes/6.7/6.7.5.0.md)  
*(Body truncated in this bundle; follow the link for the rest.)*

# Release notes Shopware 6.7.5.0

## Abstract

This release delivers targeted enhancements across tax logic, SEO, API, and core infrastructure. Key improvements include corrected tax-free handling for B2B/B2C customers, extended robots.txt configurability, and a new scheduled task for cleaning corrupted media files. Developers benefit from enriched OpenAPI documentation, new JWT helpers, and PHP 8.5 polyfill support, while storefront updates refine SEO URL protection and component extensibility. Critical fixes resolve issues such as product weight precision and guest checkout behaviour, ensuring greater platform stability and accuracy.

## System requirements

* tested on PHP 8.2 and 8.4
* tested on MySQL 8 and MariaDB 11

## Improvements

#### Tax Calculation Logic

The tax-free detection logic if the cart changed to handle B2B and B2C customers separately. Previously, enabling "Tax-free for B2C" in the country settings also affected B2B customers. Now, tax rules are applied **correctly** based on the customer type.

#### Robots.txt configuration

The rendering of the `robots.txt` file has been changed to support custom `User-agent` blocks and the full `robots.txt` standard. For a detailed guide on how to use the new features and extend the functionality, please refer to our documentation guide [Extend robots.txt configuration](https://developer.shopware.com/docs/guides/plugins/plugins/content/seo/extend-robots-txt.html).

#### Scheduled Task for cleaning up corrupted media entries

A new scheduled task `media.cleanup_corrupted_media` has been introduced. It detects and removes corrupted media records, such as entries created by interrupted or failed file uploads that have no corresponding file on the filesystem.

### API

#### Add the possibility to specify indexer in context

When you want to specify which indexer should run, you can add the `EntityIndexerRegistry::EXTENSION_INDEXER_ONLY` extension to the context as follows:

```php
$context->addExtension(EntityIndexerRegistry::EXTENSION_INDEXER_ONLY,
    new ArrayEntity([
        ProductIndexer::STOCK_UPDATER // Only execute STOCK_UPDATER.
    ]),
);
```

When making a call to the Sync API, specify the required indexer in the header:

```bash
curl -X POST "http://localhost:8000/api/_action/sync" \
-H "indexing-only: product.stock" \
#...
```

### Core

#### Improved Store API OpenAPI documentation with field descriptions

The OpenAPI schema generator for Store API endpoints now includes descriptions for entity fields, making it easier for developers to understand the available fields and their purposes.

Additionally, available associations for each entity are now automatically listed in the OpenAPI operation descriptions, showing developers which relationships can be loaded.

To add descriptions to fields in your custom entity definitions, use the `setDescription()` method:

```php
(new ManyToOneAssociationField('group', 'customer_group_id',
    CustomerGroupDefinition::class, 'id', false))
    ->addFlags(new ApiAware())
    ->setDescription('Customer group determining pricing and permissions')
```

#### Allow overwriting Doctrine wrapperClass on Primary/Replica setups

It's now possible to overwrite the `wrapperClass` of the `Doctrine\DBAL\Connection` instance.
This is useful if you want to use e.g. `Doctrine MySQL Comeback` to automatically reconnect if the MySQL connection is lost.

```bash
composer require facile-it/doctrine-mysql-come-back ^3.0
```

Then specify the `wrapperClass` in the `.env` file:

```
DATABASE_URL=mysql://root:root@database/shopware?driverOptions[x_reconnect_attempts]=5&wrapperClass=Facile\DoctrineMySQLComeBack\Doctrine\DBAL\Connection
```

#### Robots.txt parsing

A new `Shopware\Storefront\Page\Robots\Parser\RobotsDirectiveParser` has been introduced to parse `robots.txt` files. This new service provides improved error tracking and adds new events for better extensibility.

As part of this change, the constructor for `Shopware\Storefront\Page\Robots\Struct\DomainRuleStruct` is now deprecated for string parameters. You should use the new parser to create a `ParsedRobots` object to pass to the constructor instead.

#### new JWT helper

Added new `Shopware\Core\Framework\JWT\SalesChannel\JWTGenerator` and `Shopware\Core\Framework\JWT\Struct\JWTStruct` to build general structure for encoding and decoding JWT.

#### Added PHP 8.5 polyfill

The new dependency `symfony/polyfill-php85` was added, to make it possible to already use PHP 8.5 features, like `array_first` and `array_last`

#### Removal of old `changelog` handling

As we changed how we process and generate changelogs the "old" changelog files are no longer needed.

Therefore, we removed all the internal code used to generate and validate them.
The whole `Shopware\Core\Framework\Changelog` namespace was removed.

The code is not needed anymore, you should adjust the `RELEASE_INFO` and `UPGRADE` files manually instead.

#### Deprecated the `\Shopware\Core\Framework\Test\TestCaseHelper\ReflectionHelper`

Refection has significantly improved in particular since PHP 8.1, therefore the `Shopware\Core\Framework\Test\TestCaseHelper\ReflectionHelper` was deprecated and will be removed in the next major release.
See below for the explicit replacements:

```diff
- $property = ReflectionHelper->getProperty(MyClass::class, 'myProperty');
+ $property = \ReflectionProperty(MyClass::class, 'myProperty');
```

```diff
- $method = ReflectionHelper->getMethod(MyClass::class, 'myMethod');
+ $method = \ReflectionMethod(MyClass::class, 'myMethod');
```

```diff
- $propertyValue = ReflectionHelper->getPropertyValue($object, 'myProperty');
+ $propertyValue = \ReflectionProperty(MyClass::class, 'myProperty')->getValue($object);
```

```diff
- $fileName = ReflectionHelper->getFileName(MyClass::class);
+ $fileName = \ReflectionClass(MyClass::class)->getFileName();
```

#### New constraint to check for existing routes

The new constraint `\Shopware\Core\Framework\Routing\Validation\Constraint\RouteNotBlocked` checks if a route is available or already taken by another part of the application.

#### Multiple payment finalize calls allowed

With the feature flag `REPEATED_PAYMENT_FINALIZE`, the `/payment-finalize` endpoint can now be called multiple times using the same payment token.

This behaviour will be the default in the next major release.
If the token has already been consumed, the user will be redirected directly to the finish page instead of triggering a PaymentException.

To support this behavior, a new `consumed` flag has been added to the payment token struct, which indicates if the token has already been processed.
Payment tokens are no longer deleted immediately after use. A new scheduled task automatically removes expired tokens to keep the `payment_token` table clean.

#### Added sanitized HTML tag support for app snippets

Added sanitized HTML tag support for app snippets. App developers can now use HTML tags for better formatting within their snippets. The sanitizing uses the `basic` set of allowed HTML tags from the `html_sanitizer` config, ensuring that security-related tags such as `script` are automatically removed.

#### App custom entity association handling

The behaviour creating associations with custom entities in apps changed.

Now an exception will be thrown if the referenced table does not exist, instead of creating a reference to the non-existing table.

To allow the schema updater to skip creating associations if the referenced table does not exist, improving flexibility and robustness during schema updates, a new optional attribute `ignore-missing-reference` was added to association types (`one-to-one`, `one-to-many`, `many-to-one`, `many-to-many`).

Example usage:

```xml
<one-to-many name="custom_entity" reference="quote_comment" ignore-missing-reference="true" store-api-aware="false" on-delete="set-null" />
```

#### Translatable product manufacturer links

The `link` property of the product manufacturer entity is now translatable.

### Administration

#### URL restrictions for product and category SEO URLs

When creating a SEO URL for a product or category, the URL is now checked for availability. Before it was possible to override existing URLs like `account` or `maintenance` with SEO URLs. Existing URLs are now blocked to be used as SEO URLs.

#### Refactor filters for the newsletter recipients list.

We now use the `<mt-select>` instead `administration/src/module/sw-newsletter-recipient/component/sw-newsletter-recipient-filter-switch`.

Because of that, we deprecate these twig blocks:

* `sw_newsletter_recipient_list_sidebar_filter_status_not_set`
* `sw_newsletter_recipient_list_sidebar_filter_status_direct`
* `sw_newsletter_recipient_list_sidebar_filter_status_opt_in`
* `sw_newsletter_recipient_list_sidebar_filter_status_opt_out`

These blocks will be removed in v6.8.0.0 without replacement. Use the parent blocks instead.

We also deprecate
`administration/src/module/sw-newsletter-recipient/component/sw-newsletter-recipient-filter-switch` which will be removed with v6.8.0.0 and
`administration/src/module/sw-newsletter-recipient/page/sw-newsletter-recipient-list/index.js` which will be private in v6.8.0.0.

### Storefront

#### Language selector twig blocks

New extensible Twig blocks `layout_header_actions_language_widget_content_inner` and `layout_header_actions_languages_widget_form_items_flag_inner` have been added to the language selector to allow custom flag implementations.

#### `context.token` is no longer available in twig rendering context

The `context.token` variable is no longer available in twig rendering context to prevent potential security vulnerabilities. If you need to access the token, consider using alternative methods that do not expose it in the rendered HTML.

Usually inside the Twig storefront there is no need to handle the context token manually, as it is handled automatically via the session handling in the Storefront.

#### Added specific `add-product-by-number` template

The `page_checkout_cart_add_product*` blocks inside `@Storefront/storefront/page/checkout/cart/index.html.twig` are deprecated and a new template `@Storefront/storefront/component/checkout/add-product-by-number.html.twig` was added.

Instead of overwriting any of the `page_checkout_cart_add_product*` blocks inside `@Storefront/storefront/page/checkout/cart/index.html.twig`,
extend the new `@Storefront/storefront/component/checkout/add-product-by-number.html.twig` file using the same blocks.

Change:

```
{% sw_extends '@Storefront/storefront/page/checkout/_page.html.twig' %}

{% block page_checkout_cart_add_product %}
    {# Your content #}
{% endblock %}
```

to:

```
{% sw_extends '@Storefront/storefront/component/checkout/add-product-by-number.html.twig' %}

{% block page_checkout_cart_add_product %}
    {# Your content #}
{% endblock %}
```

### Hosting & Configuration

#### Sales Channel Replace URL Command

A new `sales-channel:replace:url` command was added to replace the url of a sales channel.

```bash
bin/console sales-channel:replace:url <previous_url> <new_url>
```

#### Changed `CACHE_CONTEXT_HASH_RULES_OPTIMIZATION` feature flag to `CACHE_REWORK`

The `CACHE_CONTEXT_HASH_RULES_OPTIMIZATION` feature flag was renamed to `CACHE_REWORK` to better reflect its purpose, as more changes will be toggled by that flag, to enable the new cache behaviour.

To enable the new cache behaviour, set the `CACHE_REWORK` feature flag to `1` in your `.env` file:
Before:

```
CACHE_CONTEXT_HASH_RULES_OPTIMIZATION=1
```

Now:

```
CACHE_REWORK=1
```

To not break plugins that might check for the old flag unnecessarily, the old flag will be kept until the next major release, however, the flag has no effect anymore.

#### Staging configuration

The disabled delivery check in `MailSender` now checks for the Staging Mode `core.staging`, the `shopware.staging.mailing.disable_delivery` configuration and the config setting `shopware.mailing.dis

… **Truncated.** Full document: https://developer.shopware.com/release-notes/6.7/6.7.5.0.md


---

## Release notes Shopware 6.7.5.1
**Source:** [release-notes/6.7/6.7.5.1.md](https://developer.shopware.com/release-notes/6.7/6.7.5.1.md)  
# Release notes Shopware 6.7.5.1

## Abstract

This patch release contains the fix for a security issue. Please update to this patch release as soon as possible. If you cannot update immediately, it is highly recommended to use the [Security Plugin](https://store.shopware.com/en/swag136939272659f/shopware-6-security-plugin.html).

## System requirements

* tested on PHP 8.2 and 8.4
* tested on MySQL 8 and MariaDB 11

## Improvements

(No notable improvements in this patch release)

## Fixed bugs

* [GHSA-6w82-v552-wjw2](https://github.com/shopware/shopware/security/advisories/GHSA-6w82-v552-wjw2) Reflected XSS in Storefront Login Page
* [13751](https://github.com/shopware/shopware/issues/13751) Theme manager detail - tabs not visible

## Credits

Thanks to all diligent friends for helping us make Shopware better and better with each pull request!

## More resources

* [Detailed diff on Github](https://github.com/shopware/shopware/compare/v6.7.5.0...v6.7.5.1) to the former version
* [Installation overview](https://developer.shopware.com/docs/guides/installation/)
* [Update from a previous installation](https://developer.shopware.com/docs/guides/installation/template.html#update-shopware)

## Get in touch

Discuss about decisions, bugs you might stumble upon, etc in our [community discord](https://chat.shopware.com). See you there ;)

---

---

## Release notes Shopware 6.7.6.0
**Source:** [release-notes/6.7/6.7.6.0.md](https://developer.shopware.com/release-notes/6.7/6.7.6.0.md)  
*(Body truncated in this bundle; follow the link for the rest.)*

# Release notes Shopware 6.7.6.0

## Abstract

This Shopware minor release has a strong focus on performance, HTTP caching, and platform stability. The release introduces an experimental HTTP caching rework with configurable caching policies, expanded Store API cacheability, and multiple performance improvements across core indexing and API handling.

In addition, this version brings PHP 8.5 support, new API capabilities such as video cover management, enhanced administration UX, and improved Storefront validation. The App System and hosting configuration options were extended to give developers and ambicious online merchants more control over caching and search behaviour.

Alongside these improvements, approximately 150 bug fixes were delivered across Core, Administration, CMS, Storefront, and API layers — addressing issues ranging from deprecated PHP usage and CMS media uploads to editor rendering and export correctness.

## System requirements

* tested on PHP 8.2, 8.4 and 8.5
* tested on MySQL 8 and MariaDB 11

## Improvements

### HTTP caching rework

* Support for HTTP caching policies was added. It allows defining HTTP cache behavior per area (storefront, store\_api)
  and per route using configuration. The feature is experimental and can be enabled with the `CACHE_REWORK` feature flag
  together with other HTTP caching improvements.
* Selected Store API routes were marked as cacheable and now support HTTP caching with Cache-Control headers.

### Send email on customer password change

A new flow has been introduced which sends a confirmation email whenever a customer changes their password. This helps to identify any suspicious account activity more quickly.

### API

#### Video cover management `/api/_action/media/{mediaId}/video-cover`

Added endpoint to assign or remove cover images for video media files. Requires `media.editor` ACL permission.
Accepts `coverMediaId` (string or null) in request body.
Cover image reference is stored in `metaData.video.coverMediaId`.
When a cover image is deleted, all video references are automatically cleaned up via `VideoCoverCleanupSubscriber`.

#### StoreAPI HTTP caching support

HTTP caching support was added for the following Store API endpoints:

* `/store-api/breadcrumb/{id}`
* `/store-api/category`
* `/store-api/category/{navigationId}`
* `/store-api/navigation/{activeId}/{rootId}`
* `/store-api/cms/{id}`
* `/store-api/product`
* `/store-api/seo-url`
* `/store-api/country`
* `/store-api/country-state/{countryId}`
* `/store-api/currency`
* `/store-api/language`
* `/store-api/salutation`

`GET` methods and HTTP caching support were added for the following Store API endpoints:

* `/store-api/media`
* `/store-api/product/{productId}/cross-selling`
* `/store-api/product/{productId}`
* `/store-api/product/{productId}/find-variant`
* `/store-api/product-listing/{categoryId}`
* `/store-api/product/{productId}/reviews`
* `/store-api/search`
* `/store-api/search-suggest`

It's intended to work with the new HTTP caching policy system, and should increase performance for cacheable Store API requests.

#### Store API: compressed criteria parameter support

Criteria can be passed in the GET requests as single query parameter, encoded as JSON -> gzip -> base64url. This allows
sending complex criteria without hitting URL length limits. Also, ProductListingCriteria fields are supported.
Please note that this is a temporary workaround intended to be used until `QUERY` request method is standardized and supported.
Check the [ADR](adr/2025-09-15-store-api-cache-strategy.md) for more details.

#### Document download `/store-api/document/download/`

The endpoint now selects the document file type based on the `Accept` header.
When no `Accept` header is set or with `*/*`, `PDF` will be returned. (PR #12944)

### Core

#### PHP 8.5 support

Shopware is now fully compatible with PHP 8.5.

#### Deprecation of `sw-states` and `sw-currency` handling and new way to disable caching

The `sw-states` and `sw-currency` handling is deprecated, which means by default the HTTP-Cache will also be active for logged in customers or when the cart is filled in the next major version.
You can opt in to the new behaviour by activating either the `v6.8.0.0` (all upcoming breaking changes),  `PERFORMANCE_TWEAKS` (all performance related breaks) or `CACHE_REWORK` (only the HTTP-Cache related breaks) feature flag.

Due to the rework of the contained rules in the cache hash, this becomes efficiently possible. The complete caching behaviour is now controlled by the `sw-cache-hash` cookie.

You should rework you extensions to also work with enabled cache for logged in customers and when the cart is filled.
To modify the default behaviour there are several extension points you can hook into, for a detailed explanation please take a look at the [caching docs](https://developer.shopware.com/docs/guides/plugins/plugins/framework/caching/#manipulating-the-cache-key).

The following classes and constants were deprecated as they will not be used anymore:

* `\Shopware\Core\Framework\Adapter\Cache\Http\CacheStateValidator`
* `\Shopware\Core\Framework\Adapter\Cache\CacheStateSubscriber`
* `\Shopware\Core\Framework\Adapter\Cache\Http\HttpCacheKeyGenerator::SYSTEM_STATE_COOKIE`
* `\Shopware\Core\Framework\Adapter\Cache\Http\HttpCacheKeyGenerator::INVALIDATION_STATES_HEADER`
* `\Shopware\Core\Framework\Adapter\Cache\Http\HttpCacheKeyGenerator::CURRENCY_COOKIE`
* `\Shopware\Core\Framework\Adapter\Cache\CacheStateSubscriber::STATE_LOGGED_IN`
* `\Shopware\Core\Framework\Adapter\Cache\CacheStateSubscriber::STATE_CART_FILLED`

Additionally, the following configuration was deprecated:

* `shopware.cache.invalidation.http_cache`

#### HTTP Caching Policies

Added support for caching policies to define HTTP cache behavior via configuration.

You can now configure named caching policies that define how the Cache-Control header is formed. These policies can be assigned per area (`storefront`, `store_api`) and per route. The header controls how caches (browser, reverse proxy, CDN, Symfony cache layer) should cache the response.

The feature is enabled using the `CACHE_REWORK` feature flag. For more details see the [caching policies documentation](https://developer.shopware.com/docs/guides/hosting/performance/caches.html#http-caching-policies).

#### Add recursive assign method to AssignArrayTrait

A new method `assignRecursive` has been added to `Shopware\Core\Framework\Struct\AssignArrayTrait`. Along with it, the new `Shopware\Core\Framework\Struct\AssignArrayInterface` has been introduced.
To make full use of `assignRecursive`, every class using `AssignArrayTrait` must also implement the new `AssignArrayInterface`.
The `assignRecursive` method enables deeply nested, JSON-serialized data structures - for example, a fully serialized `ProductEntity` including associations such as `properties` - to be converted back into a fully populated `ProductEntity` instance, including all nested `Struct` and `Collection` objects.

Note: `assignRecursive` uses reflection and creates nested struct instances, so it is noticeably slower than the classic shallow `assign` and is intended for import/export and (re-)hydration scenarios rather than tight, performance-critical loops.

#### Performance improvements for generating category SEO-Urls

We don't synchronously fetch and generate the SEO-Urls for all child categories anymore.
Instead, we rely on the CategoryIndexer to trigger the re-index of children asynchronously.
This prevents cases where SEO-Urls were generated multiple times for the same category, and thus it considerably improves the performance of category indexing.

### Administration

#### Loading indicator for whole page

When the initial page takes more than two seconds to load, a loading indicator appears instead of a blank page.

#### Search filter for settings module

In the settings module, there is now a search bar in the top right. It can be used to filter settings based on a search term to quickly find what you need.

### Storefront

#### The email validation supports IDN email addresses

The domain part of email addresses may now contain internationalized domain names (IDN). The Storefront validation will properly check these domains. The form validation in PHP may still deny IDN emails addresses, but the default Shopware forms already allow them.

### App System

#### App Script caching control

As before, app developers can control caching via in app scripts using syntax `{% do response.cache.<directive> %}`, which map to `ResponseCacheConfiguration` methods.
Next changes were made to `ResponseCacheConfiguration` methods:

* added `sharedMaxAge(seconds)` - set shared (reverse proxy/CDN) cache TTL, equivalent to `s-maxage` cache control directive.
* added `clientMaxAge(seconds)` - set client-side (browser) cache TTL, equivalent to `max-age` cache control directive. Has effect only if `CACHE_REWORK` feature flag is enabled.
* deprecated `maxAge(seconds)` - use sharedMaxAge() instead.

Admins can override policies per script using `route_policies` with `route#hook` pattern in configuration (see HTTP caching policies description in the Core section).

### Hosting & Configuration

#### Control language analyzer usage in Elasticsearch search queries

A new environment variable `SHOPWARE_ES_USE_LANGUAGE_ANALYZER` has been added to control whether language-specific analyzers (like `sw_english_analyzer`, `sw_german_analyzer`) are used for search queries.

By default (`SHOPWARE_ES_USE_LANGUAGE_ANALYZER=1`), search queries use the same analyzer as the indexed field, which includes language-specific features like stopword filtering and stemming. This provides broader, more fuzzy search results.

When set to `0` (`SHOPWARE_ES_USE_LANGUAGE_ANALYZER=0`), search queries use `sw_whitespace_analyzer` instead, providing less fuzzy search results with fewer matches.

**Note:** This setting only affects search queries, not indexing. Indexed data continues to use language analyzers for proper tokenization.

### Possibility to disable extensions when setting up staging mode

A new config option `shopware.staging.extensions.disable` was added to allow configuring extensions that should be automatically disabled when the staging mode gets activated via `system:setup:staging` command.

```yaml
shopware:
    staging:
        extensions:
            disable: ["TheExtensionName", "AnotherExtensionName"]
```

#### Deprecated HTTP cache configuration

* `SHOPWARE_HTTP_DEFAULT_TTL` environment variable.
* `shopware.http.cache.default_ttl` parameter.
* `shopware.http_cache.stale_while_revalidate` parameter.
* `shopware.http_cache.stale_if_error` parameter.

Deprecated parameters will have no effect when `CACHE_REWORK` feature flag is enabled, and will be removed in 6.8.0.0.

## Fixed bugs

* [13952](https://github.com/shopware/shopware/pull/13952) Removed deprecated PDO constants usage
* [13927](https://github.com/shopware/shopware/pull/13927) Fixed media upload in CMS image slider
* [14090](https://github.com/shopware/shopware/pull/14090) Fixed invisible list bullets and numbering in WYSIWYG editor
* [14025](https://github.com/shopware/shopware/pull/14025) Enabled `CalculatedPrice` fields in order exports
* [14031](https://github.com/shopware/shopware/pull/14031) Added missing slot setting services

See all fixed bugs in this release: https://github.com/shopware/shopware/milestone/22?closed=1

## Credits

Thanks to all diligent friends for helping us make Shopware better and better with each pull request!

See all contributors on this page: https://github.com/shopware/shopware/releases/tag/v6.7.6.0#Contributors

## More resources

* [Detailed diff on Github](https://github.com/shopware/shopware/compare/v6.7.5.1...v6.7.6.0) to the former version
* [Changelog on GitHub](https://github.com/shopware/shopware/releases/tag/v6.7.6.0) for this version.
* [Release News corporate blog post](https://www.shopware.com/en/news/s

… **Truncated.** Full document: https://developer.shopware.com/release-notes/6.7/6.7.6.0.md


---

## Release notes Shopware 6.7.6.1
**Source:** [release-notes/6.7/6.7.6.1.md](https://developer.shopware.com/release-notes/6.7/6.7.6.1.md)  
# Release notes Shopware 6.7.6.1

## Abstract

This patch release contains the fix for a security issue. Please update to this patch release as soon as possible. If you cannot update immediately, it is highly recommended to use the [Security Plugin](https://store.shopware.com/en/swag136939272659f/shopware-6-security-plugin.html).

## System requirements

* tested on PHP 8.2, 8.4 and 8.5
* tested on MySQL 8 and MariaDB 11

## Improvements

(No notable improvements in this patch release)

## Fixed bugs

* [GHSA-7cw6-7h3h-v8pf](https://github.com/shopware/shopware/security/advisories/GHSA-7cw6-7h3h-v8pf) - fix: map in security extension for array callables

## Credits

Thanks to all diligent friends for helping us make Shopware better and better with each pull request!

## More resources

* [Detailed diff on Github](https://github.com/shopware/shopware/compare/v6.7.6.0...v6.7.6.1) to the former version
* [Installation overview](https://developer.shopware.com/docs/guides/installation/)
* [Update from a previous installation](https://developer.shopware.com/docs/guides/installation/template.html#update-shopware)

## Get in touch

Discuss about decisions, bugs you might stumble upon, etc in our [community discord](https://chat.shopware.com). See you there ;)

---

---

## Release notes Shopware 6.7.6.2
**Source:** [release-notes/6.7/6.7.6.2.md](https://developer.shopware.com/release-notes/6.7/6.7.6.2.md)  
# Release notes Shopware 6.7.6.2

## Abstract

This patch release fixes two bugs.

## System requirements

* tested on PHP 8.2, 8.4 and 8.5
* tested on MySQL 8 and MariaDB 11

## Improvements

(No notable improvements in this patch release)

## Fixed bugs

* [14396](https://github.com/shopware/shopware/pull/14396) Update i18n snippet handling to ensure reactivity on locale message changes
* [14430](https://github.com/shopware/shopware/pull/14430)TypeError when \_httpCache route attribute contains string

## Credits

Thanks to all diligent friends for helping us make Shopware better and better with each pull request!

## More resources

* [Detailed diff on Github](https://github.com/shopware/shopware/compare/v6.7.6.1...v6.7.6.2) to the former version
* [Installation overview](https://developer.shopware.com/docs/guides/installation/)
* [Update from a previous installation](https://developer.shopware.com/docs/guides/installation/template.html#update-shopware)

## Get in touch

Discuss about decisions, bugs you might stumble upon, etc in our [community discord](https://chat.shopware.com). See you there ;)

---

---

## Release notes Shopware 6.7.7.0
**Source:** [release-notes/6.7/6.7.7.0.md](https://developer.shopware.com/release-notes/6.7/6.7.7.0.md)  
*(Body truncated in this bundle; follow the link for the rest.)*

# Release notes Shopware 6.7.7.0

## Abstract

Shopware 6.7.7.0 as a minor release delivers a strong mix of performance improvements, developer-focused enhancements and stability fixes. This release upgrades the framework to Symfony 7.4, introduces significant DAL query performance optimizations, enhances cache invalidation and search indexing, and improves media handling across the platform. Administrators and storefront users benefit from usability and accessibility improvements, while developers gain new extensibility options and clearer deprecation paths.

In addition to these improvements, this version includes ~120 closed issues, covering bug fixes and other merged changes.

## System requirements

* tested on PHP 8.2, 8.4 and 8.5
* tested on MySQL 8 and MariaDB 11

## Improvements

### Symfony 7.4 update

All symfony packages have been updated to version 7.4.
Take a look at the [Symfony 7.4 release post](https://symfony.com/blog/symfony-7-4-0-released) for more information.
Especially note that Symfony now requires php-redis extension v6.1 or higher: https://github.com/symfony/symfony/blob/7.4/UPGRADE-7.4.md#cache.
If you note compatibility issues with the Redis extension please check the installed version php-redis.

### Changed maintenance mode redirect

After maintenance ends, users are now redirected back to the page they were on before maintenance.
Previously, users were always redirected to the shop homepage.

### Support of media paths with up to 2046 characters

Previously the maximum length for media paths was limited to 255 characters (due to default StringField limit) while the
database field already supported up to 2046 characters. This limitation has now been lifted and media paths can be up to
2046 characters long.

### Configurable Custom Field Searchability

Custom fields are now **not searchable by default**. To make a custom field searchable, you need to enable the "Include in search" option in the custom field detail modal when creating or updating a custom field in Settings > System > Custom fields. This change helps optimize index storage size and improve search performance, especially for stores with many custom fields.

**Important:** When enabling searchability for an existing product custom field, you must rebuild the search index or update the products manually to include the custom field data in search results.

### Media Model Viewer

From now on you are able to inspect your 3D models directly in the Media module in the Administration. Simply select a model file and you will find an interactive 3D viewer in the Preview collapsable in the item sidebar on the right. This new component is called `sw-model-viewer`.

### API

#### Improved tagged based cache invalidation

Next routes now support cache tagging, enabling automatic invalidation when relevant entities are written:

* `/store-api/breadcrumb/{id}`
* `/store-api/media`
* `/store-api/product/{productId}/find-variant`
* `/store-api/product/{productId}/cross-selling`

### Core

#### Rework of DAL query generation for nested filters groups

The DAL criteria builder has been adjusted to generate `EXISTS` subqueries instead of `LEFT JOIN`s for nested filter groups.

Previously, each level of nested filters resulted in an additional `LEFT JOIN`, even when the join was only required to check for the existence of a related entity subject to some filter.
In complex criteria trees with multiple filters on the same entity, this led to an exponential explosion of joins and significant performance degradation (e.g., the same table being joined multiple times only to evaluate existence conditions).

An example of this is a query such as "find orders that have a line item of type A and one of type B and one of type C".
According to [aadr/2020-11-19-dal-join-filter.md](adr/2020-11-19-dal-join-filter.md), this would look like:

```php
$criteria->addFilter(
    new EqualsFilter('lineItems.type', 'product'),
    new EqualsFilter('lineItems.type', 'custom'),
    new EqualsFilter('lineItems.type', 'other'),
);
```

Previously, the generated query would `LEFT JOIN` `order_line_item` multiple times onto `order`, causing the query to be extremely slow. The new `EXISTS` checks prevent this, making the query much faster.

#### Introduce Immutable DAL flag

A new `Immutable` flag is available for Data Abstraction Layer fields. Fields marked as immutable can be set during entity creation but cannot be updated later. This prevents accidental renames of technical identifiers that other subsystems rely on. Core entities now using the flag include:

* `custom_field.name`
* `custom_field.type`
* `custom_field_set.name`

Trying to update these columns now results in a `WriteConstraintViolationException` with the message `The field foo is immutable and cannot be updated.`, giving developers clear feedback when attempting to change these values.
If the value is not set in the payload, or the value won't change, no exception is thrown.

#### Performance Improvement for `ProductCategoryDenormalizer`

The SQL Query inside the `ProductCategoryDenormalizer` has been optimized to run faster, especially on large catalogues.
Previously MySql needed to perform a full table scan based on the where condition, now the result set is already limited by indexed columns.
This lead to performance improvements from up to 3s for the query down to less than 1ms on large catalogues (3000%).

### Deprecation of product states in favor of the new product type

The `product.states` field is deprecated and will be removed in the next major release.
A new field `product.type` was introduced to clearly indicate whether a product is `digital` or `physical`, or other types registered by third-party developers.

As part of this change, the following deprecations were made:

* The `order_line_item.states` field is deprecated in favor of `order_line_item.payload.product_type`.
* `\Shopware\Core\Checkout\Cart\LineItem\LineItem::$states` is deprecated in favor of `\Shopware\Core\Checkout\Cart\LineItem\LineItem::$payload['productType']`.
* The `LineItemProductStatesRule` is deprecated in favor of the new `LineItemProductTypeRule`.
* The `StatesUpdater` service and its related dispatched events (`ProductStatesBeforeChangeEvent`, `ProductStatesChangedEvent`) are deprecated.
* A new parameter `shopware.product.allowed_types` was introduced to allow third-party developers to register additional product types.
* For more details, please refer to the [2025-11-14-introduce-product-type-and-deprecate-states.md](adr%2F2025-11-14-introduce-product-type-and-deprecate-states.md)

If you are using the rule `LineItemProductStatesRule`, product stream filters, or product listing filters that rely on `product.states`, you should update them to use the new `product.type` field instead.
If you create digital products using admin api, you should explicitly set the `type` field to `digital` when creating new products instead of relying on backend handling.

#### New `RequestParamHelper`

Symfony deprecated the "magic" `Request::get()` method, which was used to retrieve parameters from the request, by checking the `attribute`, `query` or `request` parameter bags.
For easier backward compatibilty we backported the old behaviour in the new `RequestParamHelper` class, however, it should only be used in explicit cases, where the parameter could be in any of those parameter bags.
The best practice is to check the explicit parameter bag, where you expect the parameter to be.
However, as we have a lot of API routes that support being called by `GET` and `POST` methods both, the helper is handy in such cases.

Before:

```php
$parameter = $request->get($parameterName, $default);
```

After:

```php
$parameter = RequestParameterHelper::get($request, $parameterName, $default);
```

To provide full backward compatibility, the helper currently also checks the `attribute` bag for the parameter first.
However, it should be possible to strictly differentiate between request attributes (which are generally controlled and set by the application itself) and input parameters (which are provided by the client, and based on how they are passed are either part of the query bag or the request bag) in the future.
Therefore the check of the `attribute` bag is deprecated and will be removed in the next major release.
When you need to get a value from the request attributes, you should use the `Request::attributes->get()` method directly.
In case you used to set request attributes to override specific parameters, you should instead overwrite the parametes in the `query` or `request` parameter bags directly.

#### The `TranslationLoader` class is now decoratable

The `TranslationLoader` class extends from the new `AbstractTranslationLoader` class and implements the decoratable pattern. This allows third-party developers to decorate the loader to add custom logic when a translation is loaded.

#### DomainExceptions don't create \RuntimeException anymore

All factory methods for domain exceptions now return specific exception classes instead of creating a generic `\RuntimeException`.
Changing the type of the thrown exception from `\RuntimeException` to a specific domain exception is not considered a breaking change, since all Domain Exceptions extend from `\RuntimeException`.

This means code like this will stay valid:

```php
try {
    $this->someService->willThrowDomainException();
} catch (\RuntimeException $e) {
    // handle exception
}
```

Additionally, all changed factory methods were marked as deprecated, because the `\RuntimeException` return type will be removed in the next major release.
This affects the following exception factory methods:

* `DataAbstractionLayerException::cannotBuildAccessor(...)`
* `DataAbstractionLayerException::onlyStorageAwareFieldsAsTranslated(...)`
* `DataAbstractionLayerException::onlyStorageAwareFieldsInReadCondition(...)`
* `DataAbstractionLayerException::primaryKeyNotStorageAware(...)`
* `DataAbstractionLayerException::missingTranslatedStorageAwareProperty(...)`
* `DataAbstractionLayerException::noTranslationDefinition(...)`
* `DataAbstractionLayerException::missingVersionField(...)`
* `DataAbstractionLayerException::unexpectedFieldType(...)`
* `WebhookException::invalidDataMapping(...)`
* `WebhookException::unknownEventDataType(...)`

#### More fine-grained caching control in `HttpCacheCookieEvent`

A new `doNotStore` property was added to the `HttpCacheCookieEvent` to allow fine-grained control over caching behavior.
This new property allows preventing the current response from being stored in the cache.
This behaviour differs from the existing ìsCacheable\` property, which will also prevent the following requests from that session being cached.

#### Logging for invalidated cache tags

Added logging for invalidated cache tags at the info level, with the ability to enable or disable the logging via configuration for debugging and transparency.

#### Removed `CacheInvalidationSubscriber::getChangedPropertyFilterTags` due to performance issues

The `getChangedPropertyFilterTags` method has been removed from `CacheInvalidationSubscriber` due to performance issues where it could cause invalidation storms by selecting all product IDs for popular property options.

Changing a property group or option will no longer automatically invalidate product and product list caches. It's recommended to rely on TTLs for bigger shops. If you experience issues after changing a property group, a manual cache clear may be required.

### Administration

#### Deprecations in mail template components

The mail template index will be split into separate tabs for templates and headers/footers in v6.8.0.0.

The following deprecations apply to `sw-mail-template-list` and `sw-mail-header-footer-list`:

* `searchTerm` prop and watcher will be removed in v6.8.0.0
* `getList()` method: `searchTerm` variable will be replaced with `this.term` in v6.8.0.0
* `@page-change` handler will change t

… **Truncated.** Full document: https://developer.shopware.com/release-notes/6.7/6.7.7.0.md


---

## Release notes Shopware 6.7.7.1
**Source:** [release-notes/6.7/6.7.7.1.md](https://developer.shopware.com/release-notes/6.7/6.7.7.1.md)  
# Release notes Shopware 6.7.7.1

## Abstract

With this patch, three bug fixes have been delivered.

## System requirements

* tested on PHP 8.2, 8.4 and 8.5
* tested on MySQL 8 and MariaDB 11

## Improvements

(No notable improvements in this patch release)

## Fixed bugs

* [14736](https://github.com/shopware/shopware/pull/14736)`getAddress` in`AddressDetailPageLoader`
* [14725](https://github.com/shopware/shopware/pull/14725) elasticsearch requirement in core bundle
* [14746](https://github.com/shopware/shopware/pull/14746) order edit loading

## Credits

Thanks to all diligent friends for helping us make Shopware better and better with each pull request!

## More resources

* [Detailed diff on Github](https://github.com/shopware/shopware/compare/v6.7.7.0...v6.7.7.1) to the former version
* [Installation overview](https://developer.shopware.com/docs/guides/installation/)
* [Update from a previous installation](https://developer.shopware.com/docs/guides/installation/template.html#update-shopware)

## Get in touch

Discuss about decisions, bugs you might stumble upon, etc in our [community discord](https://chat.shopware.com). See you there ;)

---

---

## Release notes Shopware 6.7.7.1
**Source:** [release-notes/latest.md](https://developer.shopware.com/release-notes/latest.md)  
# Release notes Shopware 6.7.7.1

## Abstract

With this patch, three bug fixes have been delivered.

## System requirements

* tested on PHP 8.2, 8.4 and 8.5
* tested on MySQL 8 and MariaDB 11

## Improvements

(No notable improvements in this patch release)

## Fixed bugs

* [14736](https://github.com/shopware/shopware/pull/14736)`getAddress` in`AddressDetailPageLoader`
* [14725](https://github.com/shopware/shopware/pull/14725) elasticsearch requirement in core bundle
* [14746](https://github.com/shopware/shopware/pull/14746) order edit loading

## Credits

Thanks to all diligent friends for helping us make Shopware better and better with each pull request!

## More resources

* [Detailed diff on Github](https://github.com/shopware/shopware/compare/v6.7.7.0...v6.7.7.1) to the former version
* [Installation overview](https://developer.shopware.com/docs/guides/installation/)
* [Update from a previous installation](https://developer.shopware.com/docs/guides/installation/template.html#update-shopware)

## Get in touch

Discuss about decisions, bugs you might stumble upon, etc in our [community discord](https://chat.shopware.com). See you there ;)

---

---

## Upgrades
**Source:** [resources/references/upgrades.md](https://developer.shopware.com/docs/v6.6/resources/references/upgrades.md)  
# Upgrades

Software projects typically undergo changes and upgrades, for Shopware this is not different.
This section provides you with comprehensive update guides for specific technical changes.

---

---

## Administration
**Source:** [resources/references/upgrades/administration.md](https://developer.shopware.com/docs/v6.6/resources/references/upgrades/administration.md)  
# Administration

This section contains all upgrade guides related to the Shopware Administration.

---

---

## Vue 3 upgrade
**Source:** [resources/references/upgrades/administration/vue3.md](https://developer.shopware.com/docs/v6.6/resources/references/upgrades/administration/vue3.md)  
# Vue 3 upgrade

## Introduction

The Shopware administration uses Vue.js `2`, which will reach its end of life (EOL) **on December 31st 2023**. To deliver up-to-date and maintainable software, the administration will use Vue.js `3` from Shopware version `6.6` and upwards. If you are unfamiliar with the changes from Vue.js `2` to Vue.js `3`, please refer to this [official guide](https://v3-migration.vuejs.org/).

## FAQ

Let's start with some frequently asked questions. These will also help you figure out if this upgrade affects you.

### Which extensions are affected by the Vue 3 upgrade?

App-based extensions aren't affected by these changes. However, if your extension is plugin-based and contains custom administration code, you likely need to do some refactoring.

### Are there any breaking changes I should be aware of?

Yes, Vue 3 introduced breaking changes. It's crucial to review the migration guide provided by Vue.js and this document for detailed information.

### What steps should I follow to upgrade my Shopware plugin to Vue 3?

Typically, the process involves updating your project dependencies and modifying your code to adhere to Vue 3's API changes. Consult the Vue 3 documentation and this document's step-by-step instructions.

### Can one plugin version be compatible with Shopware 6.5 and 6.6?

No, your plugin requires a new version in the Store. For instance, version `1.x` is for Shopware `6.5.x`, while version `2.0` is compatible with Shopware `6.6` and newer.

### How can I check if my Shopware extension is compatible with Vue 3?

You can verify compatibility by reviewing the extension's functionality and updating test suites according to this document.

### Do I need to rewrite my extension to upgrade to Vue 3?

While some changes are required, a complete rewrite is not necessary. The amount of effort is dictated by your use of Vue's internal API.

### Are tools or libraries available to facilitate the migration to Vue 3?

Yes, there are tools and migration helpers that can automate certain aspects of the upgrade process. You could start by enabling the Vue 3 rule set of `eslint`.

### Where can I find support and community discussions about updating Shopware plugin to Vue 3?

You can participate in discussions and seek help on the Shopware community Slack. There is a dedicated channel for this topic called `#vue3-update`.

## External resources

Here is a handpicked selection of external resources. This list provides a handy reference, granting you access to all the essential materials you might need.

* [Vue 3 migration guide](https://v3-migration.vuejs.org)
* [Vue 3 breaking changes](https://v3-migration.vuejs.org/breaking-changes/)
* [Vue router migration guide](https://router.vuejs.org/guide/migration/)
* [Vue test utils migration guide](https://test-utils.vuejs.org/migration/)

## Step-by-step guide

To follow along, you should have the following:

* the latest Shopware `trunk` or an official release candidate
* installed and activated your plugin
* a running administration watcher (`composer run watch:admin`)

### Update your plugin npm dependencies

Make sure to align your `package.json` dependencies with the [administration](https://github.com/shopware/shopware/blob/trunk/src/Administration/Resources/app/administration/package.json).

### Check your templates

For your templates to work correctly, perform the following in no specific order:

* Replace all `sw-field` usages with the corresponding [components](https://github.com/shopware/shopware/blob/6.5.x/src/Administration/Resources/app/administration/src/app/component/form/sw-field/index.js#L16).
* [Check all v-models](https://v3-migration.vuejs.org/breaking-changes/v-model.html)
* [Check event listeners](https://v3-migration.vuejs.org/breaking-changes/v-model.html#_3-x-syntax)
* [Check for deprecated slot syntax](https://eslint.vuejs.org/rules/no-deprecated-slot-attribute.html)
* [Check router-view transition combinations](https://router.vuejs.org/guide/migration/#-router-view-keep-alive-and-transition-)
* [Check your key attributes](https://v3-migration.vuejs.org/breaking-changes/key-attribute.html)
* [Check for filter usages](https://v3-migration.vuejs.org/breaking-changes/filters.html)

### Check your code

Most of your code should be unaffected by the upgrade. You can start by searching for `this.$`. The usage of `this.$` is an indicator of Vue's internal API. These calls are very likely to break except for `this.$tc`.

If you have a lot of Vue internal API calls, check out the [Known issues section](#known-issues).
The best way to find errors is to test your application thoroughly, either by hand or automated.

## Known issues

### Lifecycle hooks

Lifecycle hooks such as `@hook:mounted` may be triggered multiple times if the component is loaded asynchronously. Vue 3 will emit the hook for the `AsyncComponentWrapper` and the underlying component. You can only use those hooks if your code allows to be executed multiple times.

### Using slots programmatically

It is no longer sufficient to check if `this.$slots` has a property with the slot name to see if that slot exists. Instead, you must verify if your `slotName` contains an actual `v-node`.

### this.$parent

`this.$parent` is prone to errors because Vue 3 wraps the `AsyncWrapperComponent` around asynchronous components. Leading to the virtual dom tree to differ from Vue 2 to Vue 3. Where in Vue 2, a `this.$parent` call was successful, in Vue 3, a `this.$parent.$parent` may be necessary.
Try to avoid `this.$parent` communication wherever possible as this is an anti pattern. Use services or event communication instead.

### Vue dev tools performance

Vue dev tools causes massive performance issues with huge Vue 3 applications.
There is an open [issue on Github](https://github.com/vuejs/devtools-v6/issues/1875) with next to no activity from the maintainers.

### v-model changes

`v-model` has several breaking changes. Please consider the official [guide](https://v3-migration.vuejs.org/breaking-changes/v-model.html)

### vuex reactivity

Vuex stores lose reactivity if one or more getters alter state data. For more context, see [here](https://vuejs.org/guide/essentials/reactivity-fundamentals.html#reactivity-fundamentals).

### Form field id's

Fields in the administration no longer have the previous ID almost exclusively used in tests. To fix any failing test, add the `name` attribute to your field with a unique identifier.

### Prop default

Prop default functions no longer have access to the component's `this` scope. You can no longer call `this.$tc` in default functions. Use `Shopware.Snippet.tc` instead.

### Mutating props

This is an antipattern also for Vue 2. In Vue 2, however, those mutations were not always detected. In Vue 3, this will fail with hard errors. Take a look at this [example](https://eslint.vuejs.org/rules/no-mutating-props.html) to get a basic understanding of how to avoid mutating props directly.

## Conclusion

This document emphasizes the crucial need to upgrade your Shopware extensions to Vue.js 3 as Vue.js 2 reaches its end of life on December 31st 2023. Here's a concise recap of the key points:

* **Transition to Vue 3**: Shopware will adopt Vue.js 3 from version 6.6 onwards.
* **FAQ**: Addressing frequently asked questions:
  * **Extension Compatibility**: Plugin-based extensions with custom administration code are primarily affected. App-based extensions remain unaffected.
  * **Breaking Changes**: Vue 3 introduces significant modifications, necessitating review through the Vue.js migration guide.
  * **Migration Steps**: Adapting your Shopware plugin to Vue 3 involves aligning dependencies and adhering to Vue 3's API changes, following the Vue 3 documentation.
* **Dual Compatibility**: For plugins serving both Shopware 6.5 and 6.6, separate versions are required.
* **Support**: Find support in the Shopware community Slack channel #vue3-update.

---

---

## Core upgrade and migration guides
**Source:** [resources/references/upgrades/core.md](https://developer.shopware.com/docs/resources/references/upgrades/core.md)  
# Core upgrade and migration guides

This section contains all upgrade and migration guides related to the Shopware Core.

---

---

## Update And Migration Guides For Translations In The Shopware Core
**Source:** [resources/references/upgrades/core/translation.md](https://developer.shopware.com/docs/resources/references/upgrades/core/translation.md)  
# Update And Migration Guides For Translations In The Shopware Core

This section contains all upgrade and migration guides related to translations in the Shopware Core.

---

---

## Migrating Extension Translations to the Country-Independent Snippet Layer
**Source:** [resources/references/upgrades/core/translation/extension-translation.md](https://developer.shopware.com/docs/resources/references/upgrades/core/translation/extension-translation.md)  
# Migrating Extension Translations to the Country-Independent Snippet Layer

Starting with **Shopware 6.7.3**, a new country-independent snippet layer has been introduced to reduce duplicate
translations across similar language variants (e.g., `en-GB`, `en-US`, `en-CA` can share a common "en" base layer).

This change implements a hierarchical fallback system that automatically resolves translations through multiple layers,
significantly reducing maintenance overhead for extension developers.

## How the New System Works

The snippet loading system now follows this resolution order:

1. **Country-specific layer** (e.g., `en-GB`, `de-DE`) — Highest priority
2. **Language base layer** (e.g., `en`, `de`, `es`)  **NEW fallback layer**
3. **British English fallback** (`en-GB`) - Legacy fallback to maximize compatibility
4. **Default fallback** (`en`) - Last resort

When a translation key is requested, Shopware will:

* First check the specific country variant (e.g., `es-AR`)
* If not found, check the base language (e.g., `es`)
* If not found, the legacy fallback will be checked (`en-GB`)
* Finally, fall back to `en` if still not found

**Result**: ~90% reduction in duplicate translations while maintaining full functionality.

## Migrating Your Extensions

### Automatic

Shipping with Shopware **6.7.3**, there's the command line tool `bin/console translation:lint-filenames` that can be used to
check the translation files, or use the `--fix` parameter to even automate the migration process. For more information, see [this migration article](../../../../../concepts/translations/fallback-language-selection.md#migration-and-linting-via-command).

### Manual

#### Step 1: Rename your existing files

Rename your existing files from country-specific naming to the language base layer naming.

```Generic
├── messages.en-GB.base.json ⇒ messages.en.base.json
├── messages.de-DE.base.json ⇒ messages.de.base.json
├── messages.fr-FR.base.json ⇒ messages.fr.base.json
└···
```

#### Step 2: Re-create empty country-specific files

Re-create empty files with the former names of the country-specific naming.

```Generic
├── messages.en-GB.base.json
├── messages.de-DE.base.json
├── messages.fr-FR.base.json
└···
```

#### Step 3: Remove duplicates from other country-specific files

Check for duplicate translations across country-specific files and remove them from the country-specific layer.

Here are some example locales that are a dialect to the generic base layer.

```Generic
├── messages.en-US.base.json (dialect of en-GB with the en base layer)
├── messages.en-IN.base.json (dialect of en-GB with the en base layer)
├── messages.de-AT.base.json (dialect of de-DE with the de base layer)
├── messages.de-CH.base.json (dialect of de-DE with the de base layer)
├── messages.pt-BR.base.json (dialect of pt-PT with the pt base layer)
└···
```

For more details on selecting a fallback language and structuring your snippet files, see the [Fallback Languages guide](../../../../../concepts/translations/fallback-language-selection.md).

## Testing Your Migration

After the snippet files have been renamed, changing the locale to one of the empty snippet sets should still provide
all translated strings. Changing to a country-specific locale should also provide all translated strings with just
country-specific terms being replaced.

## Best Practices

### 1. Maintain Backward Compatibility

Keep existing country-specific files during transition to ensure compatibility with older Shopware versions that don't
support the base layer.

## Troubleshooting

### Common Migration Issues

#### 1. Translations Not Found After Migration

**Symptoms**: Missing translations in frontend/backend after restructuring
**Solution**:

```bash
bin/console cache:clear
bin/console snippet:validate
```

---

---

## Migration Guide: Language Pack Plugin → Integrated Translation Handling
**Source:** [resources/references/upgrades/core/translation/language-pack-migration.md](https://developer.shopware.com/docs/resources/references/upgrades/core/translation/language-pack-migration.md)  
# Migration Guide: Language Pack Plugin → Integrated Translation Handling

Starting with Shopware **6.7.3.0**, translations are managed directly in Shopware. From **6.8.0.0**, the
[Language Pack plugin][language-pack-plugin] will no longer be compatible. Follow this guide to migrate safely.

## What changes

* **From Shopware 6.7.3.0 onward**

  * Translations can be installed via Shopware itself, the [Language Pack plugin][language-pack-plugin] is not required to fetch the
    newest [Shopware translations][shopware-translations].
  * A new CLI command is available:

```bash
  bin/console translation:install --locales it-IT
```

* The [Language Pack plugin][language-pack-plugin] still works but is not recommended.

* Languages now have an active flag which can be toggled in the Administration under `Settings → Languages`

* Languages installed/managed from other sources do not need to register their locales in the admin anymore.

* **Other translation plugins or snippets in themes are not affected and can still be used alongside the integrated handling.**

* **Shopware 6.8.0.0 and later**

  * The [Language Pack plugin][language-pack-plugin] is **not compatible**.
    * The [integrated language handling][translation-system] should be used to fetch the newest [Shopware translations][shopware-translations].
  * **Other translation plugins or snippets in themes are not affected and can still be used alongside the integrated handling.**

## Migration paths

### 1. You are **not using the Language Pack plugin**

* Nothing changes.
* To install additional languages, use the CLI command:

```bash
  bin/console translation:install --locales <locale-code>
```

Example: `bin/console translation:install --locales it-IT,fr-FR` will install Italian and French.

### 2. You are **currently using the Language Pack plugin**

1. Run the translation command and install every language you are using in your shop

   ```bash
     bin/console translation:install --locales <locale-code>,<locale-code>
   ```

2. The command uses the **same source ([translate.shopware.com][shopware-translations])** as the [Language Pack plugin][language-pack-plugin] but is
   updated more frequently. So it's essentially identical – or even more up to date!

3. Make sure that all languages you need are **active** in the Administration: `Settings → Languages`

4. Create base snippet sets for used languages
   * If you're on Shopware **6.7.7.0** or later, this is done automatically.
   * If you're on Shopware **6.7.6.0** or earlier, for each language in use, create a base snippet, e.g. `BASE en-US` for English (US).

5. Change all sales channel domains to use the base snippet sets.
   * If you're on Language Pack **5.37.1** or later, this is done automatically.
   * If you're on Language Pack **5.37.0** or earlier, open each sales channel, scroll down to the domains and change the
     snippet set from `LanguagePack` to `BASE`, e.g.: `LanguagePack en-US` to `BASE en-US`.

6. It is recommended to uninstall and remove the Language Pack plugin after `translation:install` succeeded for all locales.
   Your **custom snippets** created in the snippet module remain intact since they are saved in the database.

## New installations

* During a fresh Shopware installation, you can select desired languages directly in the installer. They will be
  downloaded and installed automatically.
* No additional language plugin is required.

## More information

* Additional details about the new translation handling are available in the [integrated language handling][translation-system] guide.

## Common problems and troubleshooting

### Can't remove Language Pack: a foreign key constraint fails (\`shopware\`.\`sales\_channel\_domain\`…

Starting with **Shopware 6.7.7.0** and **Language Pack 5.37.1**, the migration process was improved. If you encounter this issue,
please update Shopware to >= 6.7.7.0, Language Pack to >= 5.37.1, remove the translation files created from running the
command and run the command again. Or follow the updated migration guide.

[translation-system]: ../../../../../concepts/translations/built-in-translation-system.md

[language-pack-plugin]: https://store.shopware.com/en/swag338126230916f/shopware-language-pack.html

[shopware-translations]: https://translate.shopware.com

---

---

