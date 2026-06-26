# RELEASE AND UPGRADES

Compiled excerpts from the Shopware Developer Documentation snapshot. Prefer live docs at [developer.shopware.com](https://developer.shopware.com/) when in doubt.

---

## Release notes Shopware 6.5.7.0
**Source:** [release-notes/6.5/6.5.7.0.md](https://developer.shopware.com/release-notes/6.5/6.5.7.0.md)  
*(Body truncated in this bundle; follow the link for the rest.)*

# Release notes Shopware 6.5.7.0

## Abstract

Besides new features which will be announced later this week, this minor release contains a lot of improvements and changes for developers as well as 69 bug fixes. We could merge pull requests from 18 community developers, thanks for that!

## System requirements

* tested on PHP 8.1 and 8.2
* tested on MySQL 8.0.33, MariaDB 10.4. 10.5, 10.11 & 11.0

## Improvements

### Deprecated SEO URLs for Headless Sales Channels

With this release, we deprecated the SEO URLs for headless sales channels. This will be removed in 6.6. If you need SEO URLs in a headless environment, please use the Storefront Sales Channel type or a custom sales channel type using a custom plugin.

[PR](https://github.com/shopware/shopware/commit/9d6d58b075898dc181a2626ae0c0eefd0f342cb6)

### Disabled Doctrine Database Profiler in CLI

When the Symfony Profiler was installed, it collected database queries in the CLI, even in production mode. We disabled it now completely in CLI regardless of the current environment Shopware is running.

### Support for Maintenance mode in Store-API

The maintenance configuration of Sales Channels is now respected in headless store-api requests. When the maintenance mode is active, you will get a 503 http error as response.

[PR](https://github.com/shopware/shopware/commit/df8833a46a1c370d52234f2190d848b148e981ca)

### Media Path refactoring

We refactored the media path handling to persist the media paths instead of recalculating in any request. This allows the media entity to be queried only with the path. Previously, the complete media entity needed to be loaded to generate the path.

```http
POST /api/search/product

{
    "fields": [
        "name",
        "cover.path"
    ]
}
```

### Improvements to logging

As in the previous releases, we continued to improve the logging of Shopware. Hence, we added more logging or down-ranked non-relevant errors to noises to keep the logs clean for important messages.

### Deprecated LoggerFactory

We deprecated the LoggerFactory for plugins for 6.6 as this does not consider the project configuration of logging. Our suggested replacement is to use Monolog Channels, which works in any Shopware 6 version. Please also see the PayPal plugin as an example of our implementation:

* https://github.com/shopware/SwagPayPal/blob/7.3.0/src/Resources/config/packages/monolog.yaml
* https://github.com/shopware/SwagPayPal/blob/7.3.0/src/SwagPayPal.php#L200-L217

### New low\_priority queue

We introduced a new queue, `low_priority`, in addition to the already existing `async` queue. This queue can be used by plugins, to queue up messages which are not important in a short manner.

The existing `messenger:consume` or admin watcher will consume the new queue without configuration changes. With Shopware 6.6, it becomes required to setup an additional `messenger:consume` or just append the queue additionally to the existing one `messenger:consume async low_priority`

### Improved plugin:create

The `plugin:create` command now can generate:

* console command
* scheduled task
* event subscriber
* storefront controller
* store-api route

We are working right now also on a `dal:migration:create` to generate migration files automatically by comparing your entity definition with the current database schema. So stay tuned!

### Soft delete of custom entities on App uninstall

Custom Entities created by Apps will now be soft deleted, so that you can preserve the app data on uninstallation.

### System update now uses the regular kernel

The commands `system:update:prepare` and `system:update:finish` now use the regular kernel while updating Shopware. This fixes a lot of issues when plugins extend root components like Symfony Configuration or created themes.

### MySQL 8.2 support

We fixed some internal queries of DAL to be able to support MySQL 8.2.

### And many more things

* Paginated pages in listing are now HTTP cached
* Improved performance *order\_line\_item* migration
* Removed *ManyToManyIdFieldUpdater* in *LandingPageIndexer*
* Optimized SEO lookup queries

## Fixed bugs

* [NEXT-29188](https://issues.shopware.com/issues/NEXT-29188) | Wrong error message in Flow Builder (64 votes)
* [NEXT-29496](https://issues.shopware.com/issues/NEXT-29496) | Dynamic product groups with properties - Filters not shown (36 votes)
* [NEXT-30650](https://issues.shopware.com/issues/NEXT-30650) | Cannot create Rule for customer custom fields (29 votes)
* [NEXT-30866](https://issues.shopware.com/issues/NEXT-30866) | SwagCommercial 5.6.0 can't be installed if B2B Suite was installed before (25 votes)
* [NEXT-23795](https://issues.shopware.com/issues/NEXT-23795) | Sendmail insert a dot into a url (22 votes)
* [NEXT-31145](https://issues.shopware.com/issues/NEXT-31145) | Inheritance issues with new languages wich inherit from another language (19 votes)
* [NEXT-31296](https://issues.shopware.com/issues/NEXT-31296) | Rule builder does not take effect when changing payment type (16 votes)
* [NEXT-26311](https://issues.shopware.com/issues/NEXT-26311) | import/export of advanced prices with rule names (16 votes)
* [NEXT-28809](https://issues.shopware.com/issues/NEXT-28809) | HTML Filter removes important parameters from text snippets in Shopware 6.5.2.1 (14 votes)
* [NEXT-29142](https://issues.shopware.com/issues/NEXT-29142) | Order delivery address foreign key missing / wrongly defined (13 votes)
* [NEXT-30680](https://issues.shopware.com/issues/NEXT-30680) | Can't select an item picking mode (11 votes)
* [NEXT-30652](https://issues.shopware.com/issues/NEXT-30652) | TagEntity does not contain Name or the ID in store-api (6 votes)
* [NEXT-31256](https://issues.shopware.com/issues/NEXT-31256) | No order confirmation is sent in combination with an invoice document (5 votes)
* [NEXT-25425](https://issues.shopware.com/issues/NEXT-25425) | Sorting of payment methods does not work (5 votes)
* [NEXT-30879](https://issues.shopware.com/issues/NEXT-30879) | Sorting of product cross sellings with dynamic product group by price with Elasticsearch (3 votes)
* [NEXT-31486](https://issues.shopware.com/issues/NEXT-31486) | SaaS: Dashboard not loading when time zone is not UTC (3 votes)
* [NEXT-30895](https://issues.shopware.com/issues/NEXT-30895) | Shopware Commercial 5.6.0 don't work with 6.5.6.0 (2 votes)
* [NEXT-30315](https://issues.shopware.com/issues/NEXT-30315) | Properties disappear after the search (1 votes)
* [NEXT-30810](https://issues.shopware.com/issues/NEXT-30810) | Backend JS-Error on batch-update product - price (1 votes)
* [NEXT-30878](https://issues.shopware.com/issues/NEXT-30878) | Watch-administration.sh issue (1 votes)
* [NEXT-30974](https://issues.shopware.com/issues/NEXT-30974) | View guest order in frontend (1 votes)
* [NEXT-31427](https://issues.shopware.com/issues/NEXT-31427) | Installation deadlock after trying to create a not valid admin password (1 votes)
* [NEXT-31519](https://issues.shopware.com/issues/NEXT-31519) | Cart-Rules do not use very recent product attributes (1 votes)
* [NEXT-31087](https://issues.shopware.com/issues/NEXT-31087) | Apparent wrong naming of twig block component\_line\_item\_type\_product\_order\_number (1 votes)
* [NEXT-31275](https://issues.shopware.com/issues/NEXT-31275) | Cross Selling Criteria Id's change will be ignored (1 votes)
* [NEXT-31466](https://issues.shopware.com/issues/NEXT-31466) | Wishlist Double-Optin route frontend.wishlist.add.after.login misses productId parameter (1 votes)
* [NEXT-29060](https://issues.shopware.com/issues/NEXT-29060) | Generating documents very slow once a reasonable number of documents exists (1 votes)
* [NEXT-31086](https://issues.shopware.com/issues/NEXT-31086) | \[Github] - Skip creation of category links in SeoUrlGenerator (Revert NEXT-10719) (1 votes)
* [NEXT-30394](https://issues.shopware.com/issues/NEXT-30394) | Re-installuing commercial plugins results in a bug with returns and number ranges (0 votes)
* [NEXT-30987](https://issues.shopware.com/issues/NEXT-30987) | Custom Fields of type "price" can't be edited in Admin (0 votes)
* [NEXT-31303](https://issues.shopware.com/issues/NEXT-31303) | remove from cart event (0 votes)
* [NEXT-25584](https://issues.shopware.com/issues/NEXT-25584) | \[GitHub] feat: change behaviour of getting path name to not generate it on every request (0 votes)
* [NEXT-29751](https://issues.shopware.com/issues/NEXT-29751) | Document - at shipping address for countries is not taken the translated name (0 votes)
* [NEXT-30455](https://issues.shopware.com/issues/NEXT-30455) | \[GitHub] fix: add missing closing div (0 votes)
* [NEXT-30468](https://issues.shopware.com/issues/NEXT-30468) | \[Github] #3025 - Support active flag and maintenace mode in store api routes.. (0 votes)
* [NEXT-30604](https://issues.shopware.com/issues/NEXT-30604) | Avoid creating SEO URLs for headless sales channels (0 votes)
* [NEXT-30765](https://issues.shopware.com/issues/NEXT-30765) | \[GitHub] Fix: Using designer in Category sends us back to the wrong page (0 votes)
* [NEXT-30809](https://issues.shopware.com/issues/NEXT-30809) | Rules with App conditions can't be saved (0 votes)
* [NEXT-30824](https://issues.shopware.com/issues/NEXT-30824) | \[Github] fix: change argument type to UrlGeneratorInterface in BCStrategy to allow decorations (0 votes)
* [NEXT-30825](https://issues.shopware.com/issues/NEXT-30825) | \[GitHub] Fix accept all cookies button styling (0 votes)
* [NEXT-30828](https://issues.shopware.com/issues/NEXT-30828) | \[GitHub] Return error on preview with invalid SEO URL template (0 votes)
* [NEXT-30829](https://issues.shopware.com/issues/NEXT-30829) | \[GitHub] Use displayed SEO URL template value for validation hints (0 votes)
* [NEXT-30834](https://issues.shopware.com/issues/NEXT-30834) | \[Github] Pagination http cache (0 votes)
* [NEXT-30838](https://issues.shopware.com/issues/NEXT-30838) | \[Github] refactor: Remove AFTER statement for order\_line\_item table (0 votes)
* [NEXT-30848](https://issues.shopware.com/issues/NEXT-30848) | \[GitHub] feat: change title for wishlist toggle (0 votes)
* [NEXT-30850](https://issues.shopware.com/issues/NEXT-30850) | \[GitHub] refactor: Deprecate CartEvents (0 votes)
* [NEXT-30852](https://issues.shopware.com/issues/NEXT-30852) | \[GitHub] Transition state machine exception fix (0 votes)
* [NEXT-30854](https://issues.shopware.com/issues/NEXT-30854) | \[GitHub] fix(administration): promotion v2 date-picker prop usage so time-pickers are displayed again (0 votes)
* [NEXT-30929](https://issues.shopware.com/issues/NEXT-30929) | \[Github] Nested query version\_id field check (0 votes)
* [NEXT-30930](https://issues.shopware.com/issues/NEXT-30930) | \[Github] feat: correct class AbstractMediaUrlGenerator to namespace Shopware\Core\Content\Media\Core\Application\ (0 votes)
* [NEXT-30963](https://issues.shopware.com/issues/NEXT-30963) | \[Github] Fixed typo from "langugage" to "language" (0 votes)
* [NEXT-30984](https://issues.shopware.com/issues/NEXT-30984) | \[Github] feat: Add local apps folder (0 votes)
* [NEXT-31036](https://issues.shopware.com/issues/NEXT-31036) | \[Github] NEXT-29904 - Fix Change sorting of availability for best variant calculation (0 votes)
* [NEXT-31046](https://issues.shopware.com/issues/NEXT-31046) | Admin dashboard currency factor fix (0 votes)
* [NEXT-31064](https://issues.shopware.com/issues/NEXT-31064) | \[Github] Fix typo error (0 votes)
* [NEXT-31262](https://issues.shopware.com/issues/NEXT-31262) | \[Github] NEXT-00000 - Remove internal hint from PartialEntity to communicate the use of public API (0 votes)
* [NEXT-31263](https://issues.shopware.com/issues/NEXT-31263) | \[Github] NEXT-00000 - Allow elasticsearch to be better drop in for normal search (0 votes)
* [NEXT-31264](https://issues.shopware.com/issues/NEXT-31264) | \[Github] NEXT-00000 - Add retry loop and deletion limit to scheduled task handler (0 votes)
* [NEXT-31265](https://issues.shopware.com/issues/N

… **Truncated.** Full document: https://developer.shopware.com/release-notes/6.5/6.5.7.0.md


---

## Release notes Shopware 6.5.7.1
**Source:** [release-notes/6.5/6.5.7.1.md](https://developer.shopware.com/release-notes/6.5/6.5.7.1.md)  
# Release notes Shopware 6.5.7.1

## Abstract

This patch release contains just one bug fix (see below)

## System requirements

* tested on PHP 8.1 and 8.2
* tested on MySQL 8.0.33, MariaDB 10.4. 10.5, 10.11 & 11.0

## Fixed bugs

* [NEXT-31845](https://issues.shopware.com/issues/NEXT-31845) | Kernel cannot be booted without tests  (0 votes)

## More resources

* [Detailed diff on Github](https://github.com/shopware/shopware/compare/v6.5.7.0...v6.5.7.1) to the former version
* [Changelog on GitHub](https://github.com/shopware/shopware/blob/v6.5.7.1/CHANGELOG.md) for this version.
* [Installation overview](https://developer.shopware.com/docs/guides/installation/)
* [Update from a previous installation](https://developer.shopware.com/docs/guides/installation/template.html#update-shopware)

## Get in touch

Discuss about decisions, bugs you might stumble upon, etc in our [community slack](https://slack.shopware.com). See you there ;)

---

---

## Release notes Shopware 6.5.7.2
**Source:** [release-notes/6.5/6.5.7.2.md](https://developer.shopware.com/release-notes/6.5/6.5.7.2.md)  
# Release notes Shopware 6.5.7.2

## Abstract

Shopware patch v6.5.7.2 contains only one change which fixes a missing injection in admin panel. This missing injection lead to an error with the Paypal integration.

## System requirements

* tested on PHP 8.1 and 8.2
* tested on MySQL 8.0.33, MariaDB 10.4. 10.5, 10.11 & 11.0

## Fixed bugs

* [PPI-836](https://issues.shopware.com/issues/PPI-836) | Entering paypal credentials not possible  (5 votes)

## More resources

* [Detailed diff on Github](https://github.com/shopware/shopware/compare/v6.5.7.1...v6.5.7.2) to the former version
* [Changelog on GitHub](https://github.com/shopware/shopware/blob/v6.5.7.2/CHANGELOG.md) for this version.
* [Installation overview](https://developer.shopware.com/docs/guides/installation/)
* [Update from a previous installation](https://developer.shopware.com/docs/guides/installation/template.html#update-shopware)

## Get in touch

Discuss about decisions, bugs you might stumble upon, etc in our [community slack](https://slack.shopware.com). See you there ;)

---

---

## Release notes Shopware 6.5.7.3
**Source:** [release-notes/6.5/6.5.7.3.md](https://developer.shopware.com/release-notes/6.5/6.5.7.3.md)  
# Release notes Shopware 6.5.7.3

## Abstract

Shopware patch v6.5.7.3 contains only one change which adds migration to fix address\_format column type back to `JSON` in `country_translation` table.

## System requirements

* tested on PHP 8.1 and 8.2
* tested on MySQL 8.0.33, MariaDB 10.4. 10.5, 10.11 & 11.0

## Fixed bugs

* [NEXT-32042](https://issues.shopware.com/issues/NEXT-32042) | address\_format column is too short (0 votes)

## More resources

* [Detailed diff on Github](https://github.com/shopware/shopware/compare/v6.5.7.2...v6.5.7.3) to the former version
* [Changelog on GitHub](https://github.com/shopware/shopware/blob/v6.5.7.3/CHANGELOG.md) for this version.
* [Installation overview](https://developer.shopware.com/docs/guides/installation/)
* [Update from a previous installation](https://developer.shopware.com/docs/guides/installation/template.html#update-shopware)

## Get in touch

Discuss about decisions, bugs you might stumble upon, etc in our [community slack](https://slack.shopware.com). See you there ;)

---

---

## Release notes Shopware 6.5.7.4
**Source:** [release-notes/6.5/6.5.7.4.md](https://developer.shopware.com/release-notes/6.5/6.5.7.4.md)  
# Release notes Shopware 6.5.7.4

## Abstract

Shopware patch v6.5.7.4 fixes the following security issues:

* [CVE-2024-22406](https://github.com/shopware/shopware/security/advisories/GHSA-qmp9-2xwj-m6m9) - Blind SQL-injection in DAL aggregations (CVSS = 9.3)
* [CVE-2024-22408](https://github.com/shopware/shopware/security/advisories/GHSA-3535-m8vh-vrmw) - Server-Side Request Forgery (SSRF) in Flow Builder (CVSS = 7.6)
* [CVE-2024-22407](https://github.com/shopware/shopware/security/advisories/GHSA-3867-jc5c-66qf) - Broken Access Control order API (CVSS = 4.9)
* [DomPDF security issue in Commercial plugin < 2.0.3](https://github.com/dompdf/dompdf/security/advisories/GHSA-3qx2-6f78-w2j2) - Resource exhaustion caused by infinite recursion when validating SVG images (CVSS = 5.3)

The Flow Builder Issue appears only in Commercial Plugin or in prior versions of the SwagFlowBuilder (Flow Builder Professional) plugin.

**Security page:**
<https://docs.shopware.com/en/shopware-6-en/security-updates/security-update-01-2024>

Please update immediately to the [latest Shopware version](https://www.shopware.com/de/changelog/#release-6-5-7-4) or install the [Security Plugin](https://store.shopware.com/en/swag136939272659f/shopware-6-security-plugin.html) if you cannot update swiftly.

## System requirements

* tested on PHP 8.1 and 8.2
* tested on MySQL 8.0.33, MariaDB 10.4. 10.5, 10.11 & 11.0

## Fixed bugs

* [NEXT-32388](https://github.com/shopware/shopware/blob/v6.5.7.4/changelog/release-6-5-7-4/2023-12-14-update-dompdf-to-2-0-4.md) | Update dompdf/dompdf to 2.0.4
* [NEXT-32201](https://github.com/shopware/shopware/blob/v6.5.7.4/changelog/release-6-5-7-4/2023-14-12-add-new-innovation-area.md) | Add 'innovation' as package title
* [NEXT-32889](https://github.com/shopware/shopware/blob/v6.5.7.4/changelog/release-6-5-7-4/2024-01-05-fix-privileges-for-state-machine.md) | Fix privileges for state machine

## More resources

* [Detailed diff on Github](https://github.com/shopware/shopware/compare/v6.5.7.3...v6.5.7.4) to the former version
* [Changelog on GitHub](https://github.com/shopware/shopware/blob/v6.5.7.4/CHANGELOG.md) for this version.
* [Installation overview](https://developer.shopware.com/docs/guides/installation/)
* [Update from a previous installation](https://developer.shopware.com/docs/guides/installation/template.html#update-shopware)

## Get in touch

Discuss about decisions, bugs you might stumble upon, etc in our [community slack](https://slack.shopware.com). See you there ;)

---

---

## Release notes Shopware 6.5.8.0
**Source:** [release-notes/6.5/6.5.8.0.md](https://developer.shopware.com/release-notes/6.5/6.5.8.0.md)  
# Release notes Shopware 6.5.8.0

## Abstract

This minor release comes with a bunch of new features and improvements like a 3D/AR model viewer, PHP 8.3 support, performance improvements and more, and we could also fix a lot of bugs. Thanks for your code contributions once again!

## System requirements

* tested on PHP 8.1, 8.2 and 8.3
* tested on MySQL 8.0.33, MariaDB 10.4. 10.5, 10.11 & 11.0

## Improvements

### Spatial Commerce (3D/AR Model Viewer)

It is now possible to upload 3D Model files as product picture and they are visible in a 3D Model Viewer or as Augmented Reality in the Product Detail Page.

### Performance Improvments

* Symfony Inline class loader is now disabled by default and generates smaller PHP Container in cache.
* Shopware Storefront NPM packages can be now installed with `npm install --production` to install only build relevant tools
* Improved SQL search config performance in order module. Searching in 30k orders
* Optimized the variant listing in Administration to do less API calls
* Added new enviroment variable `SHOPWARE_ADMIN_SKIP_SOURCEMAP_GENERATION` to skip source map generation while building the Administration to build faster

### PHP 8.3 support

Shopware 6.5.8.0 is fully PHP 8.3 compatible.

### Dependency Updates

We updated the dependencies of the Storefront to the newest version, also we upgraded Symfony from `6.3` to `6.4`. The Symfony `7.0` upgrade is planned for Shopware 6.6.

### 404 Page Language handling

The 404 page, does now consider again the user's language when the 404 page is cached.

### Admin Request Tracing

All API calls from the Administration now add a header `shopware-admin-active-route` to be able to trace API errors occures back to single Administration modules.

### Elasticsearch/OpenSearch scripts are not stored anymore inside the Server

To simplify the OpenSearch/Elasticsearch upgrades, we don't store scripts anymore inside the server. Shopware now sends the scripts with the search queries.

### Preparations for Shopware 6.6

We deprecated the old Shopware Kernel Wrapper (`Shopware\Core\HttpKernel`) and implemented the new improved Shopware Kernel for Edge Side Includes behind new `KernelFactory` factory. If you depend on the Kernel Wrapper besides `public/index.php`, `bin/console` and `bin/ci`, make sure to update your Code to the new `KernelFactory`. The changes to the files above mentioned will be automatically done with Symfony Flex when you are upgrading to Shopware 6.6 later.

### And many more things

* Webhooks are not triggered anymore for inactive apps
* The Symfony annotation cache is now explictly cleared to fix bugs after Plugin updates
* Shopware Redis Decorator bug has been fixed when the RedisTagAware adapter was used
* Belgian VAT ID validation is now fixed
* Improved webhook error handling when the response is not a json object
* The `ScoreQuery` is now correctly serialized and so recognized by the caching system

## Fixed bugs

* [NEXT-30550](https://issues.shopware.com/issues/NEXT-30550) | 404 Page has wrong language snippets and not considering the sales channel language  (42 votes)
* [NEXT-29439](https://issues.shopware.com/issues/NEXT-29439) | In the frontend, the products are displayed twice on several pages with the standard sorting "Topseller" (26 votes)
* [NEXT-28255](https://issues.shopware.com/issues/NEXT-28255) | "@RouteScope annotation is deprecated" error, although it was removed from the code already (24 votes)
* [NEXT-29293](https://issues.shopware.com/issues/NEXT-29293) | Failed to load resource Inter-roman.latin.var.woff2 (15 votes)
* [NEXT-31459](https://issues.shopware.com/issues/NEXT-31459) | New order versions are created but never deleted (13 votes)
* [NEXT-31855](https://issues.shopware.com/issues/NEXT-31855) | Deactivating an app doesn't deactivate related webhooks (8 votes)
* [NEXT-32768](https://issues.shopware.com/issues/NEXT-32768) | DAL Filter of Admin API produces incorrect results (6 votes)
* [NEXT-32159](https://issues.shopware.com/issues/NEXT-32159) | Shopware Commercial throws EmployeeManagementException despite Feature being disabled (2 votes)
* [NEXT-31213](https://issues.shopware.com/issues/NEXT-31213) | customer variables in E-Mail-Templates do not work (1 votes)
* [NEXT-31897](https://issues.shopware.com/issues/NEXT-31897) | Create a shipping method will be displayed a white window (1 votes)
* [NEXT-32972](https://issues.shopware.com/issues/NEXT-32972) | \[Commercial] Installing without German language not possible (1 votes)
* [NEXT-31146](https://issues.shopware.com/issues/NEXT-31146) | If individual variants are assigned to a category, this is not shown in the category configuration under product assignment. (0 votes)
* [NEXT-32671](https://issues.shopware.com/issues/NEXT-32671) | Kernel cache hash when using multiple database urls (0 votes)
* [NEXT-32898](https://issues.shopware.com/issues/NEXT-32898) | New Belgian tax ID format does not work (0 votes)

## Credits

Thanks to all diligent friends for helping us make Shopware better and better with each pull request!

* [Joshua Behrens](https://github.com/JoshuaBehrens)
* [Jan Emig](https://github.com/Xnaff)
* [Elias Lackner](https://github.com/lacknere)

## More resources

* [Detailed diff on Github](https://github.com/shopware/shopware/compare/v6.5.7.3...v6.5.8.0) to the former version
* [Changelog on GitHub](https://github.com/shopware/shopware/blob/v6.5.8.0/CHANGELOG.md) for this version.
* [Marketing blog post](https://www.shopware.com/en/news/shopware-6-release-news-january-2024/)
* [Installation overview](https://developer.shopware.com/docs/guides/installation/)
* [Update from a previous installation](https://developer.shopware.com/docs/guides/installation/template.html#update-shopware)

## Get in touch

Discuss about decisions, bugs you might stumble upon, etc in our [community slack](https://slack.shopware.com). See you there ;)

---

---

## Release notes Shopware 6.5.8.1
**Source:** [release-notes/6.5/6.5.8.1.md](https://developer.shopware.com/release-notes/6.5/6.5.8.1.md)  
# Release notes Shopware 6.5.8.1

## Abstract

This patch release contains two bug fixes as shown below.

## System requirements

* tested on PHP 8.1, 8.2 and 8.3
* tested on MySQL 8.0.33, MariaDB 10.4. 10.5, 10.11 & 11.0

## Fixed bugs

* [NEXT-30261](https://issues.shopware.com/issues/NEXT-30261) | Fixed redirect loop on seo url pages
* [NEXT-31872](https://issues.shopware.com/issues/NEXT-31872) | Fixed config.xsd to be compliant with libxml2 2.12.0

## More resources

* [Detailed diff on Github](https://github.com/shopware/shopware/compare/v6.5.8.0...v6.5.8.1) to the former version
* [Changelog on GitHub](https://github.com/shopware/shopware/blob/v6.5.8.1/CHANGELOG.md) for this version.
* [Installation overview](https://developer.shopware.com/docs/guides/installation/)
* [Update from a previous installation](https://developer.shopware.com/docs/guides/installation/template.html#update-shopware)

## Get in touch

Discuss about decisions, bugs you might stumble upon, etc in our [community slack](https://slack.shopware.com). See you there ;)

---

---

## Release notes Shopware 6.5.8.10
**Source:** [release-notes/6.5/6.5.8.10.md](https://developer.shopware.com/release-notes/6.5/6.5.8.10.md)  
# Release notes Shopware 6.5.8.10

## Abstract

This patch release comes with four fixed bugs.

## System requirements

* tested on PHP 8.1, 8.2 and 8.3
* tested on MySQL 8.0.33, MariaDB 10.4. 10.5, 10.11 & 11.0

## Fixed bugs

* [NEXT-30575](https://issues.shopware.com/issues/NEXT-30575) | HTML sanitizer on mail template header & footer (42 votes)
* [NEXT-35094](https://issues.shopware.com/issues/NEXT-35094) | Unprintable ASCII characters are still allowed in filenames when uploading media via the API (1 votes)
* [NEXT-35318](https://issues.shopware.com/issues/NEXT-35318) | Add heading elements for account login page to improve accessibility & SEO (0 votes)
* [NEXT-33694](https://issues.shopware.com/issues/NEXT-33694) | "Shipping Germany" function is not accessible with the keyboard (0 votes)

## Credits

Thanks to all diligent friends for helping us make Shopware better and better with each pull request!

* [Marcus Müller](https://github.com/M-arcus)
* [Jesper Ingels](https://github.com/jesperingels)

## More resources

* [Detailed diff on Github](https://github.com/shopware/shopware/compare/v6.5.8.9...v6.5.8.10) to the former version
* [Changelog on GitHub](https://github.com/shopware/shopware/blob/v6.5.8.10/CHANGELOG.md) for this version.
* [Installation overview](https://developer.shopware.com/docs/guides/installation/)
* [Update from a previous installation](https://developer.shopware.com/docs/guides/installation/template.html#update-shopware)

## Get in touch

Discuss about decisions, bugs you might stumble upon, etc in our [community slack](https://slack.shopware.com). See you there ;)

---

---

## Release notes Shopware 6.5.8.11
**Source:** [release-notes/6.5/6.5.8.11.md](https://developer.shopware.com/release-notes/6.5/6.5.8.11.md)  
# Release notes Shopware 6.5.8.11

## Abstract

This patch release contains 13 bug fixes.

## System requirements

* tested on PHP 8.1, 8.2 and 8.3
* tested on MySQL 8.0.33, MariaDB 10.4. 10.5, 10.11 & 11.0

## Fixed bugs

* [NEXT-29683](https://issues.shopware.com/issues/NEXT-29683) | Admin: Search by document numbers does not work for orders with many (24 votes)
* [NEXT-29167](https://issues.shopware.com/issues/NEXT-29167) | API: Single CustomFields cannot be output  (13 votes)
* [NEXT-31160](https://issues.shopware.com/issues/NEXT-31160) | Media admin: all media-files are declared as "unused medium", regardless of whether and how often they are in use where (12 votes)
* [NEXT-36026](https://issues.shopware.com/issues/NEXT-36026) | B2B quick order cannot be uploaded (2 votes)
* [NEXT-36507](https://issues.shopware.com/issues/NEXT-36507) | Gutscheincodes nicht als eingelöst markiert bei mehreren Rabattaktionen (1 vote)
* [NEXT-36428](https://issues.shopware.com/issues/NEXT-36428) | B2B QuoteManagement: Cover images are not displayed (0 votes)
* [NEXT-36414](https://issues.shopware.com/issues/NEXT-36414) | IterateEntityMessage in messenger tasks creates errors and polutes the log (0 votes)
* [NEXT-36288](https://issues.shopware.com/issues/NEXT-36288) | \[Github] feat: Add event to select variant on product detail page (0 votes)
* [NEXT-36279](https://issues.shopware.com/issues/NEXT-36279) | Broken initial pagination of property values in the administration (0 votes)
* [NEXT-36275](https://issues.shopware.com/issues/NEXT-36275) | Store-api doesn't return main variant product when parent product is being (0 votes)
* [NEXT-36143](https://issues.shopware.com/issues/NEXT-36143) | \[Github] feat: resolve extension parameters in compiler passes (0 votes)
* [NEXT-36088](https://issues.shopware.com/issues/NEXT-36088) | \[Github] Add database profiler on CLI if "--profile" option is used.  (0 votes)
* [NEXT-34676](https://issues.shopware.com/issues/NEXT-34676) | \[Github] Update ProductDetailRoute.php (0 votes)

## Credits

Thanks to all diligent friends for helping us make Shopware better and better with each pull request!

* [Wolfgang Kreminger](https://github.com/r4pt0s)
* [Philip Standt](https://github.com/Ocarthon)
* [Andreas Allacher](https://github.com/AndreasA)
* [Max](https://github.com/aragon999)

## More resources

* [Detailed diff on Github](https://github.com/shopware/shopware/compare/v6.5.8.10...v6.5.8.11) to the former version
* [Changelog on GitHub](https://github.com/shopware/shopware/blob/v6.5.8.11/CHANGELOG.md) for this version.
* [Installation overview](https://developer.shopware.com/docs/guides/installation/)
* [Update from a previous installation](https://developer.shopware.com/docs/guides/installation/template.html#update-shopware)

## Get in touch

Discuss about decisions, bugs you might stumble upon, etc in our [community slack](https://slack.shopware.com). See you there ;)

---

---

## Release notes Shopware 6.5.8.12
**Source:** [release-notes/6.5/6.5.8.12.md](https://developer.shopware.com/release-notes/6.5/6.5.8.12.md)  
# Release notes Shopware 6.5.8.12

## Abstract

This patch release contains at least seven bug fixes.

## System requirements

* tested on PHP 8.1, 8.2 and 8.3
* tested on MySQL 8.0.33, MariaDB 10.4. 10.5, 10.11 & 11.0

## Fixed bugs

* [NEXT-16551](https://issues.shopware.com/issues/NEXT-16551) | Searching by order number in administration is very inefficient (12 votes)
* [NEXT-37072](https://issues.shopware.com/issues/NEXT-37072) | Webhook event log can throw a critical exception (6 votes)
* [NEXT-28322](https://issues.shopware.com/issues/NEXT-28322) | Serialization failure while generating product variants (5 votes)
* [NEXT-36534](https://issues.shopware.com/issues/NEXT-36534) | Bulk edit with more than 25 selections broken (3 votes)
* [NEXT-36479](https://issues.shopware.com/issues/NEXT-36479) | Overriding messenger routing (2 votes)
* [NEXT-36927](https://issues.shopware.com/issues/NEXT-36927) | sw-cache-hash and sw-states cookies are deleted on 404 pages (1 vote)
* [NEXT-37140](https://issues.shopware.com/issues/NEXT-37140) | Search suggest route - Possible Denial of Service (DoS) entry point? (0 votes)

## Credits

Thanks to all diligent friends for helping us make Shopware better and better with each pull request!

* [Lily Berkow](https://github.com/TheAnimeGuru)
* [Pascal Thesing](https://github.com/PascalThesing)

## More resources

* [Detailed diff on Github](https://github.com/shopware/shopware/compare/v6.5.8.11...v6.5.8.12) to the former version
* [Changelog on GitHub](https://github.com/shopware/shopware/blob/v6.5.8.12/CHANGELOG.md) for this version.
* [Installation overview](https://developer.shopware.com/docs/guides/installation/)
* [Update from a previous installation](https://developer.shopware.com/docs/guides/installation/template.html#update-shopware)

## Get in touch

Discuss about decisions, bugs you might stumble upon, etc in our [community slack](https://slack.shopware.com). See you there ;)

---

---

## Release notes Shopware 6.5.8.13
**Source:** [release-notes/6.5/6.5.8.13.md](https://developer.shopware.com/release-notes/6.5/6.5.8.13.md)  
# Release notes Shopware 6.5.8.13

## Abstract

This patch release is a security release, additionally containing nine regular bug fixes. Please update as soon as possible!

## System requirements

* tested on PHP 8.1, 8.2 and 8.3
* tested on MySQL 8.0.33, MariaDB 10.4. 10.5, 10.11 & 11.0

## Security bulletins

* [CVE-2024-42357](https://github.com/shopware/shopware/security/advisories/GHSA-p6w9-r443-r752) | Blind SQL-injection in DAL aggregations
* [CVE-2024-42356](https://github.com/shopware/shopware/security/advisories/GHSA-35jp-8cgg-p4wj) | Server Side Template Injection in Twig using Context functions
* [CVE-2024-42355](https://github.com/shopware/shopware/security/advisories/GHSA-27wp-jvhw-v4xp) | Server Side Template Injection in Twig using deprecation silence tag
* [CVE-2024-42354](https://github.com/shopware/shopware/security/advisories/GHSA-hhcq-ph6w-494g) | Improper Access Control with ManyToMany associations in store-api

## Fixed bugs

* [NEXT-36445](https://issues.shopware.com/issues/NEXT-36445) | when creating a new customer in admin, salutation of the shipping address is saved incorrectly (8 votes)
* [NEXT-34301](https://issues.shopware.com/issues/NEXT-34301) | Flow send-email-action uses wrong adress (6 votes)
* [NEXT-36924](https://issues.shopware.com/issues/NEXT-36924) | StoreApiSeoResolver and auth\_required=false lead to TypeError (6 votes)
* [NEXT-37348](https://issues.shopware.com/issues/NEXT-37348) | change shipping address in order details doesnt work (3 votes)
* [NEXT-37525](https://issues.shopware.com/issues/NEXT-37525) | Tax provider processor does not allow empty tax provider results  (0 votes)
* [NEXT-34410](https://issues.shopware.com/issues/NEXT-34410) | \[Github] fix: Allow Twig array filters to accept null (0 votes)
* [NEXT-35343](https://issues.shopware.com/issues/NEXT-35343) | The selected order language is not saved for a manually created orders (0 votes)
* [NEXT-37034](https://issues.shopware.com/issues/NEXT-37034) | Automatisch hinzugefügte Rabatte nicht abwählbar (0 votes)
* [NEXT-37175](https://issues.shopware.com/issues/NEXT-37175) | Assets for bundles which use `bundle` suffix can not be loaded (0 votes)

## Credits

Thanks to all diligent friends for helping us make Shopware better and better with each pull request!

* [Max](https://github.com/aragon999)
* [Marcel Romeike](https://github.com/mromeike)

## More resources

* [Detailed diff on Github](https://github.com/shopware/shopware/compare/v6.5.8.12...v6.5.8.13) to the former version
* [Changelog on GitHub](https://github.com/shopware/shopware/blob/v6.5.8.13/CHANGELOG.md) for this version.
* [Installation overview](https://developer.shopware.com/docs/guides/installation/)
* [Update from a previous installation](https://developer.shopware.com/docs/guides/installation/template.html#update-shopware)

## Get in touch

Discuss about decisions, bugs you might stumble upon, etc in our [community slack](https://slack.shopware.com). See you there ;)

---

---

## Release notes Shopware 6.5.8.14
**Source:** [release-notes/6.5/6.5.8.14.md](https://developer.shopware.com/release-notes/6.5/6.5.8.14.md)  
# Release notes Shopware 6.5.8.14

## Abstract

This patch release contains ~15 bug fixes

## System requirements

* tested on PHP 8.2 and 8.3
* tested on MySQL 8.0.33, MariaDB 10.4. 10.5, 10.11 & 11.0

## Fixed bugs

* [NEXT-37593](https://issues.shopware.com/issues/NEXT-37593) | Promotions are not applied anymore when a position is added to the order and the max. uses per customer is reached (8 votes)
* [NEXT-37456](https://issues.shopware.com/issues/NEXT-37456) | List of individual voucher codes - pagination missing if "items per page" is set to 25 (2 votes)
* [NEXT-37571](https://issues.shopware.com/issues/NEXT-37571) | Validate VAT Reg.No. format does not work correct (1 vote)
* [NEXT-34155](https://issues.shopware.com/issues/NEXT-34155) | custom/plugins path hardcoded in TestBootstrapper.php (1 vote)
* [NEXT-38050](https://issues.shopware.com/issues/NEXT-38050) | ORDER BY contains aggregate function and applies to the result of a non-aggregated query (0 votes)
* [NEXT-38080](https://issues.shopware.com/issues/NEXT-38080) | Don't add automatic associations to child associations (0 votes)
* [NEXT-37991](https://issues.shopware.com/issues/NEXT-37991) | ManyToMany association loading with filters does not work to same table (0 votes)
* [NEXT-38012](https://issues.shopware.com/issues/NEXT-38012) | Update to 6.6 regenerates all Media Paths, potentially leading to wrong paths (0 votes)
* [NEXT-37684](https://issues.shopware.com/issues/NEXT-37684) | \[Github] Fix updating thumbnails in strict mode (0 votes)
* [NEXT-37480](https://issues.shopware.com/issues/NEXT-37480) | Promotions with rules cannot apply (0 votes)

## Credits

Thanks to all diligent friends for helping us make Shopware better and better with each pull request!

* [Philipp Zabel](https://github.com/phizab)

## More resources

* [Detailed diff on Github](https://github.com/shopware/shopware/compare/v6.5.8.13...v6.5.8.14) to the former version
* [Changelog on GitHub](https://github.com/shopware/shopware/blob/v6.5.8.14/CHANGELOG.md) for this version.
* [Installation overview](https://developer.shopware.com/docs/guides/installation/)
* [Update from a previous installation](https://developer.shopware.com/docs/guides/installation/template.html#update-shopware)

## Get in touch

Discuss about decisions, bugs you might stumble upon, etc in our [community slack](https://slack.shopware.com). See you there ;)

---

---

## Release notes Shopware 6.5.8.15
**Source:** [release-notes/6.5/6.5.8.15.md](https://developer.shopware.com/release-notes/6.5/6.5.8.15.md)  
# Release notes Shopware 6.5.8.15

## Abstract

This patch release contains ~20 bug fixes

## System requirements

* tested on PHP 8.2 and 8.3
* tested on MySQL 8.0.33, MariaDB 10.4. 10.5, 10.11 & 11.0

## Fixed bugs

* [NEXT-39044](https://github.com/shopware/shopware/issues/5148) - Last line item of order can be deleted, leading to incorrect order total
* [NEXT-38579](https://github.com/shopware/shopware/issues/4919) - customFields of lineItem is deleted when using discount
* [NEXT-38495](https://github.com/shopware/shopware/issues/4892) - My account change password / email accordion collapse (Missing Bootstrap 5 compatibility)
* [NEXT-38436](https://github.com/shopware/shopware/issues/4868) - Birthday is displayed incorrectly, when using a UTC - XX:XX Time
* [NEXT-38393](https://github.com/shopware/shopware/issues/4796) - Subscription order generation does not use unique ids
* [NEXT-38375](https://github.com/shopware/shopware/issues/4781) - Address not reloaded when searching for a customer while already on a administration customer detail page
* [NEXT-38326](https://github.com/shopware/shopware/issues/4593) - Shopware Commercial plugin gives SCSS compile errors when using @StorefrontBootstrap
* [NEXT-38292](https://github.com/shopware/shopware/issues/4720) - Unnecessary and incorrect association loading in CheckoutRegisterPageLoader
* [NEXT-38112](https://github.com/shopware/shopware/issues/4611) - Promotion - cart discount with rule not possible in promotion-tab
* [NEXT-38056](https://github.com/shopware/shopware/issues/4570) - No page numbers in the subscription overview
* [NEXT-37823](https://github.com/shopware/shopware/issues/3248) - Shopware watch-administration.sh not working after remove shopware/storefront package
* [NEXT-37571](https://github.com/shopware/shopware/issues/4444) - Validate VAT Reg.No. format does not work correct
* [NEXT-37518](https://github.com/shopware/shopware/issues/4440) - Advanced Search 2.0 - Search for product numbers with special characters
* [NEXT-36925](https://github.com/shopware/shopware/issues/4382) - Release promo code after cancelation
* [NEXT-34142](https://github.com/shopware/shopware/issues/4198) - Invoice creation via bulk edit
* [NEXT-33825](https://github.com/shopware/shopware/issues/4222) - Postal code not required by default anymore
* [NEXT-32922](https://github.com/shopware/shopware/issues/4283) - Postal code not mandatory in alternative delivery address / PLZ kein Pflichtfeld in abweichender Lieferadresse
* [NEXT-32770](https://github.com/shopware/shopware/issues/4638) - Discount calculation in existing order - Rabattkalkulation in bestehender Bestellung
* [NEXT-32218](https://github.com/shopware/shopware/issues/4071) - Promotion: It is not possible to change the tax of a promotion in an order.

## More resources

* [Detailed diff on Github](https://github.com/shopware/shopware/compare/v6.5.8.14...v6.5.8.15) to the former version
* [Changelog on GitHub](https://github.com/shopware/shopware/blob/v6.5.8.15/CHANGELOG.md) for this version.
* [Installation overview](https://developer.shopware.com/docs/guides/installation/)
* [Update from a previous installation](https://developer.shopware.com/docs/guides/installation/template.html#update-shopware)

## Get in touch

Discuss about decisions, bugs you might stumble upon, etc in our [community slack](https://slack.shopware.com). See you there ;)

---

---

## Release notes Shopware 6.5.8.16
**Source:** [release-notes/6.5/6.5.8.16.md](https://developer.shopware.com/release-notes/6.5/6.5.8.16.md)  
# Release notes Shopware 6.5.8.16

## Abstract

This patch release contains 20+ bug fixes

## System requirements

* tested on PHP 8.2 and 8.3
* tested on MySQL 8.0.33, MariaDB 10.4. 10.5, 10.11 & 11.0

## Fixed bugs & Credits

See the [UPGRADE.md](https://github.com/shopware/shopware/blob/trunk/UPGRADE-6.5.md) for all important technical changes.

* [#3476 - NEXT-33504 - fix: Allow `association_fields` of `media_default_folder` to be nullable](https://github.com/shopware/shopware/issues/3476) ([@aragon999](https://github.com/aragon999))
* [#3486 - NEXT-32844 - fix(elasticsearch): Add separator to admin ES search indexer queries](https://github.com/shopware/shopware/issues/3486) ([@M-arcus](https://github.com/M-arcus))
* [#3494 - NEXT-30575 - fix(core): Remove HTML sanitization from mail header and footer fields](https://github.com/shopware/shopware/issues/3494) ([@M-arcus](https://github.com/M-arcus))
* [#3518 - NEXT-33235 - perf: Only use `searchIds` for import id resolving](https://github.com/shopware/shopware/issues/3518) ([@aragon999](https://github.com/aragon999))
* [#3567 - NEXT-34491 - NEXT-14691 - Add pseudo modal twig blocks](https://github.com/shopware/shopware/issues/3567) ([@lacknere](https://github.com/lacknere))
* [#3579 - NEXT-34070 - Improved seo url replacer](https://github.com/shopware/shopware/issues/3579) ([@akf-bw](https://github.com/akf-bw))
* [#3580 - NEXT-34102 - Add new block in analytics template](https://github.com/shopware/shopware/issues/3580) ([@wannevancamp](https://github.com/wannevancamp))
* [#3605 - NEXT-34399 - Update action.html.twig to include css class for detail button](https://github.com/shopware/shopware/issues/3605) ([@choeft](https://github.com/choeft))
* [#3611 - NEXT-34676 - Update ProductDetailRoute.php](https://github.com/shopware/shopware/issues/3611) ([@aneufeld23](https://github.com/aneufeld23))
* [#3684 - NEXT-36143 - feat: resolve extension parameters in compiler passes](https://github.com/shopware/shopware/issues/3684) ([@Ocarthon](https://github.com/Ocarthon))
* [#3718 - NEXT-36288 - feat: Add event to select variant on product detail page](https://github.com/shopware/shopware/issues/3718) ([@aragon999](https://github.com/aragon999))
* [#3779 - NEXT-36924 - Add missing check for context object in request attributes for StoreApiSeoResolver](https://github.com/shopware/shopware/issues/3779) ([@mromeike](https://github.com/mromeike))
* [#3833 - NEXT-37557 - Update Bootstrap Docs Link](https://github.com/shopware/shopware/issues/3833) ([@levin192](https://github.com/levin192))
* [#3836 - NEXT-37684 - Fix updating thumbnails in strict mode](https://github.com/shopware/shopware/issues/3836) ([@phizab](https://github.com/phizab))
* [#5759 - Fixed Elasticsearch Filter parsing of translated fields in product-related entities](https://github.com/shopware/shopware/blob/55b4515ccb12eb02ca08cbe0e7d3e1ad65c07465/changelog/release-6-6-10-0/2024-12-03-fixed-elasticsearch-filter-parsing-of-translated-fields-in-product-related-entities.md?plain=1#L4) ([Martin Bens](https://github.com/spigandromeda))
* [NEXT-32135 - Set-Group promotions cause a timeout if too many products are in cart](https://github.com/shopware/shopware/blob/v6.5.8.16/changelog/release-6-5-8-16/2024-11-05-set-group-promotions-cause-a-timeout-if-too-many-products-are-in-cart.md)
* [NEXT-38535 - Adding the sort when searching the properties](https://github.com/shopware/shopware/blob/v6.5.8.16/changelog/release-6-5-8-16/2024-11-26-adding-the-sort-when-searching-the-properties.md)
* [NEXT-38579 - Changed to cleanup custom fields before save to DB](https://github.com/shopware/shopware/blob/v6.5.8.16/changelog/release-6-5-8-16/2024-10-24-changed-to-cleanup-custom-fields-before-save-to-db.md)
* [NEXT-39044 - Fix order can not recalculate when line items are empty](https://github.com/shopware/shopware/blob/v6.5.8.16/changelog/release-6-5-8-16/2024-10-21-fix-order-can-not-recalculate-when-line-items-are-empty.md)
* [NEXT-39215 - Fixed Belgian VAT ID pattern](https://github.com/shopware/shopware/blob/v6.5.8.16/changelog/release-6-5-8-16/2024-10-25-fixed-belgian-vat-id-pattern.md)
* [NEXT-39245 - Fix address handling does not work properly](https://github.com/shopware/shopware/blob/v6.5.8.16/changelog/release-6-5-8-16/2024-10-28-fix-address-handling-does-not-work-properly.md)
* [NEXT-39299 - Fixed price field collection serialization](https://github.com/shopware/shopware/blob/v6.5.8.16/changelog/release-6-5-8-16/2024-11-11-fixed-price-field-collection-serialization.md)
* [NEXT-39349 - Fixed shipping method fixed tax recalculation](https://github.com/shopware/shopware/blob/v6.5.8.16/changelog/release-6-5-8-16/2024-11-11-fixed-shipping-method-fixed-tax-recalculation.md)
* [NEXT-39414 - Fix issue delivery promotion not apply](https://github.com/shopware/shopware/blob/v6.5.8.16/changelog/release-6-5-8-16/2024-11-20-fix-issue-delivery-promotion-not-apply.md)

## More resources

* [Detailed diff on Github](https://github.com/shopware/shopware/compare/v6.5.8.15...v6.5.8.16) to the former version
* [Changelog on GitHub](https://github.com/shopware/shopware/blob/v6.5.8.16/CHANGELOG.md) for this version.
* [Installation overview](https://developer.shopware.com/docs/guides/installation/)
* [Update from a previous installation](https://developer.shopware.com/docs/guides/installation/template.html#update-shopware)

## Get in touch

Discuss about decisions, bugs you might stumble upon, etc in our [community slack](https://slack.shopware.com). See you there ;)

---

---

## Release notes Shopware 6.5.8.17
**Source:** [release-notes/6.5/6.5.8.17.md](https://developer.shopware.com/release-notes/6.5/6.5.8.17.md)  
# Release notes Shopware 6.5.8.17

## Abstract

This patch release contains **security fixes**. It is recommended to update your system as soon as possible!

## System requirements

* tested on PHP 8.2 and 8.3
* tested on MySQL 8.0.33, MariaDB 10.4. 10.5, 10.11 & 11.0

## Fixed bugs

* [Blind SQL-injection in DAL aggregations](https://github.com/shopware/shopware/security/advisories/GHSA-8g35-7rmw-7f59)
* [Broken ACL on Document retrieval to access other customers documents](https://github.com/shopware/shopware/security/advisories/GHSA-68wv-g3fw-pq7q)
* [Denial Of Service via password length](https://github.com/shopware/shopware/security/advisories/GHSA-cgfj-hj93-rmh2)
* [Check for registered accounts through the store-api](https://github.com/shopware/shopware/security/advisories/GHSA-hh7j-6x3q-f52h)
* [Default newsletter opt-in settings allow for mass sign-up abuse](https://github.com/shopware/shopware/security/advisories/GHSA-4h9w-7vfp-px8m)

## More resources

* [Detailed diff on Github](https://github.com/shopware/shopware/compare/v6.5.8.16...v6.5.8.17) to the former version
* [Changelog on GitHub](https://github.com/shopware/shopware/blob/v6.5.8.17/CHANGELOG.md) for this version.
* [Installation overview](https://developer.shopware.com/docs/guides/installation/)
* [Update from a previous installation](https://developer.shopware.com/docs/guides/installation/template.html#update-shopware)

## Get in touch

Discuss about decisions, bugs you might stumble upon, etc in our [community slack](https://slack.shopware.com). See you there ;)

---

---

## Release notes Shopware 6.5.8.18
**Source:** [release-notes/6.5/6.5.8.18.md](https://developer.shopware.com/release-notes/6.5/6.5.8.18.md)  
# Release notes Shopware 6.5.8.18

## Abstract

This patch release contains **security fixes**. It is recommended to update your system as soon as possible!

This is going to be the last patch for 6.5 series. Please make sure you have the [security plugin](https://store.shopware.com/en/swag136939272659f/shopware-6-security-plugin.html) installed and keep it updated.

## System requirements

* tested on PHP 8.2 and 8.4
* tested on MySQL 8, MariaDB 11

## Fixed bugs

Our backporting process failed for these two security issues:

* [6.5.8.17 - Does probably not fix the blind SQL aggregation security issue and check for registered accounts through store-api](https://github.com/shopware/shopware/security/advisories/GHSA-q5qc-g5xc-2p8f)
* [Check for registered accounts through the store-api](https://github.com/shopware/shopware/security/advisories/GHSA-hh7j-6x3q-f52h)

## Credits

* [niklaswolf](https://github.com/niklaswolf)
* [MelvinAchterhuis](https://github.com/MelvinAchterhuis)
* [AndreasA](https://github.com/AndreasA)

Thanks to all diligent friends for helping us make Shopware better and better with each pull request!

## More resources

* [Detailed diff on Github](https://github.com/shopware/shopware/compare/v6.5.8.17...v6.5.8.18) to the former version
* [Changelog on GitHub](https://github.com/shopware/shopware/blob/v6.5.8.18/CHANGELOG.md) for this version.
* [Installation overview](https://developer.shopware.com/docs/guides/installation/)
* [Update from a previous installation](https://developer.shopware.com/docs/guides/installation/template.html#update-shopware)

## Get in touch

Discuss about decisions, bugs you might stumble upon, etc in our [community slack](https://slack.shopware.com). See you there ;)

---

---

## Release notes Shopware 6.5.8.2
**Source:** [release-notes/6.5/6.5.8.2.md](https://developer.shopware.com/release-notes/6.5/6.5.8.2.md)  
# Release notes Shopware 6.5.8.2

## Abstract

This patch release contains a version roll back that prevents from braking themes when utilizing the new bootstrap version.

## System requirements

* tested on PHP 8.1, 8.2 and 8.3
* tested on MySQL 8.0.33, MariaDB 10.4. 10.5, 10.11 & 11.0

## Fixed bugs

* [NEXT-31820](https://github.com/shopware/shopware/blob/v6.5.8.2/changelog/release-6-5-8-2/2024-01-19-revert-update-npm-packages.md) | Revert update NPM packages

## More resources

* [Detailed diff on Github](https://github.com/shopware/shopware/compare/v6.5.8.1...v6.5.8.2) to the former version
* [Changelog on GitHub](https://github.com/shopware/shopware/blob/v6.5.8.2/CHANGELOG.md) for this version.
* [Installation overview](https://developer.shopware.com/docs/guides/installation/)
* [Update from a previous installation](https://developer.shopware.com/docs/guides/installation/template.html#update-shopware)

## Get in touch

Discuss about decisions, bugs you might stumble upon, etc in our [community slack](https://slack.shopware.com). See you there ;)

---

---

## Release notes Shopware 6.5.8.3
**Source:** [release-notes/6.5/6.5.8.3.md](https://developer.shopware.com/release-notes/6.5/6.5.8.3.md)  
# Release notes Shopware 6.5.8.3

## Abstract

This patch release contains 20+ bug fixes.

## System requirements

* tested on PHP 8.1, 8.2 and 8.3
* tested on MySQL 8.0.33, MariaDB 10.4. 10.5, 10.11 & 11.0

## Fixed bugs

* [NEXT-26217](https://issues.shopware.com/issues/NEXT-26217) | Copying a Variant Product does not replace main variant id (23 votes)
* [NEXT-30573](https://issues.shopware.com/issues/NEXT-30573) | SearchSuggest zeigt 24 statt 10 Produkte an (12 votes)
* [NEXT-29560](https://issues.shopware.com/issues/NEXT-29560) | Custom fields in cart line item payload are not translated (9 votes)
* [NEXT-31030](https://issues.shopware.com/issues/NEXT-31030) | Shopware Commercial throws error when password recovery detects inactive user (9 votes)
* [NEXT-33403](https://issues.shopware.com/issues/NEXT-33403) | Debug Messages are being logged in elasticsearch\_prod log (5 votes)
* [NEXT-31377](https://issues.shopware.com/issues/NEXT-31377) | AI Copilot outputs message too long (5 votes)
* [NEXT-29424](https://issues.shopware.com/issues/NEXT-29424) | Wishlist vs. Line-Items: ReferenceId kann leer sein (5 votes)
* [NEXT-33038](https://issues.shopware.com/issues/NEXT-33038) | Removed payment methods cause problems when loading an order (4 votes)
* [NEXT-32904](https://issues.shopware.com/issues/NEXT-32904) | Date filter in the orders does not work as expected (4 votes)
* [NEXT-31763](https://issues.shopware.com/issues/NEXT-31763) | More or less than three characters (currency -> "short name") creates an error in orders (4 votes)
* [NEXT-33146](https://issues.shopware.com/issues/NEXT-33146) | No full screen on YouTube Player (3 votes)
* [NEXT-33457](https://issues.shopware.com/issues/NEXT-33457) | Can not add some products to quote (2 votes)
* [NEXT-33360](https://issues.shopware.com/issues/NEXT-33360) | Save discount for set groups not possible (2 votes)
* [NEXT-32989](https://issues.shopware.com/issues/NEXT-32989) | HTML entities in the SEO fields (2 votes)
* [NEXT-32776](https://issues.shopware.com/issues/NEXT-32776) | (EN/DE) Admin order - Number of entries in selection field "Delivery address" / "Billing address" limited to 25 (2 votes)
* [NEXT-32920](https://issues.shopware.com/issues/NEXT-32920) | first- and lastname fields in the newsletter subscription form no required fields (1 vote)
* [NEXT-31770](https://issues.shopware.com/issues/NEXT-31770) | Product comparison Scheduled Export Image URLs APP\_URL used instead of assigned SalesChannel URL (1 votes)
* [NEXT-33292](https://issues.shopware.com/issues/NEXT-33292) | The search function doesn't work with dots in the search term (0 votes)
* [NEXT-33235](https://issues.shopware.com/issues/NEXT-33235) | Perf: Only use `searchIds` for import id resolving (0 votes)
* [NEXT-31225](https://issues.shopware.com/issues/NEXT-31225) | When "elements are missing" notice is displayed, saving Layout results in empty content (0 votes)
* [NEXT-30059](https://issues.shopware.com/issues/NEXT-30059) | Delete Sales Channel Domain wrong cascade delete of product\_export (0 votes)

## Credits

Thanks to all diligent friends for helping us make Shopware better and better with each pull request!

* [Max](https://github.com/aragon999)
* [Marcus Müller](https://github.com/M-arcus)

## More resources

* [Detailed diff on Github](https://github.com/shopware/shopware/compare/v6.5.8.2...v6.5.8.3) to the former version
* [Changelog on GitHub](https://github.com/shopware/shopware/blob/v6.5.8.3/CHANGELOG.md) for this version.
* [Installation overview](https://developer.shopware.com/docs/guides/installation/)
* [Update from a previous installation](https://developer.shopware.com/docs/guides/installation/template.html#update-shopware)

## Get in touch

Discuss about decisions, bugs you might stumble upon, etc in our [community slack](https://slack.shopware.com). See you there ;)

---

---

## Release notes Shopware 6.5.8.4
**Source:** [release-notes/6.5/6.5.8.4.md](https://developer.shopware.com/release-notes/6.5/6.5.8.4.md)  
# Release notes Shopware 6.5.8.4

## Abstract

This patch release contains one bug fix which caused an unusual bloating of the log files on the server.

## System requirements

* tested on PHP 8.1, 8.2 and 8.3
* tested on MySQL 8.0.33, MariaDB 10.4. 10.5, 10.11 & 11.0

## Fixed bugs

* [NEXT-33403](https://issues.shopware.com/issues/NEXT-33403) | Debug Messages are being logged in elasticsearch\_prod log (5 votes)

## More resources

* [Detailed diff on Github](https://github.com/shopware/shopware/compare/v6.5.8.3...v6.5.8.4) to the former version
* [Changelog on GitHub](https://github.com/shopware/shopware/blob/v6.5.8.4/CHANGELOG.md) for this version.
* [Installation overview](https://developer.shopware.com/docs/guides/installation/)
* [Update from a previous installation](https://developer.shopware.com/docs/guides/installation/template.html#update-shopware)

## Get in touch

Discuss about decisions, bugs you might stumble upon, etc in our [community slack](https://slack.shopware.com). See you there ;)

---

---

## Release notes Shopware 6.5.8.5
**Source:** [release-notes/6.5/6.5.8.5.md](https://developer.shopware.com/release-notes/6.5/6.5.8.5.md)  
# Release notes Shopware 6.5.8.5

## Abstract

This patch release contains several bug fixes.

## System requirements

* tested on PHP 8.1, 8.2 and 8.3
* tested on MySQL 8.0.33, MariaDB 10.4. 10.5, 10.11 & 11.0

## Fixed bugs

* [NEXT-33629](https://issues.shopware.com/issues/NEXT-33629) | Commercial: Missing `$super` calls in Administration overrides break other plugin's overrides (10 votes)
* [NEXT-33403](https://issues.shopware.com/issues/NEXT-33403) | Debug Messages are being logged in elasticsearch\_prod log (5 votes)
* [NEXT-33724](https://issues.shopware.com/issues/NEXT-33724) | Wrong currency in the order (3 votes)
* [NEXT-33642](https://issues.shopware.com/issues/NEXT-33642) | Product export - CDN URL replaced with saleschannel domain URL for product images (3 votes)
* [NEXT-33411](https://issues.shopware.com/issues/NEXT-33411) | Compile Error in 6.5.8.2 because of Async JS (0 votes)
* [NEXT-33699](https://issues.shopware.com/issues/NEXT-33699) | Static asset compilation broken when no DB available (0 votes)

## More resources

* [Detailed diff on Github](https://github.com/shopware/shopware/compare/v6.5.8.4...v6.5.8.5) to the former version
* [Changelog on GitHub](https://github.com/shopware/shopware/blob/v6.5.8.5/CHANGELOG.md) for this version.
* [Installation overview](https://developer.shopware.com/docs/guides/installation/)
* [Update from a previous installation](https://developer.shopware.com/docs/guides/installation/template.html#update-shopware)

## Get in touch

Discuss about decisions, bugs you might stumble upon, etc in our [community slack](https://slack.shopware.com). See you there ;)

---

---

## Release notes Shopware 6.5.8.6
**Source:** [release-notes/6.5/6.5.8.6.md](https://developer.shopware.com/release-notes/6.5/6.5.8.6.md)  
# Release notes Shopware 6.5.8.6

## Abstract

This patch release contains several bug fixes.

It also contains a housekeeping issue which adds support for "Google Consent Mode v2".

The decision to include this issue in a patch release was made due to the short time remaining until using v2 becomes mandatory, by March 2024.
This is not a feature, it is an adjustment to the way Shopware communicates with Google's APIs.

## System requirements

* tested on PHP 8.1, 8.2 and 8.3
* tested on MySQL 8.0.33, MariaDB 10.4. 10.5, 10.11 & 11.0

## Fixed bugs

* [NEXT-32925](https://issues.shopware.com/issues/NEXT-32925) | Support for "Google Consent Mode v2" (18 votes)
* [NEXT-31342](https://issues.shopware.com/issues/NEXT-31342) | SEO indexer doesn't consider Sales Channel context (14 votes)
* [NEXT-32024](https://issues.shopware.com/issues/NEXT-32024) | Language resets to default language for customer after login (1 vote)
* NEXT-33423 | When unsubscribing from a newsletter, an error could occur if the e-mail parameter was not valid
* NEXT-33701 | Variant names are not visible in dynamic product groups

## More resources

* [Detailed diff on Github](https://github.com/shopware/shopware/compare/v6.5.8.5...v6.5.8.6) to the former version
* [Changelog on GitHub](https://github.com/shopware/shopware/blob/v6.5.8.6/CHANGELOG.md) for this version.
* [Installation overview](https://developer.shopware.com/docs/guides/installation/)
* [Update from a previous installation](https://developer.shopware.com/docs/guides/installation/template.html#update-shopware)

## Get in touch

Discuss about decisions, bugs you might stumble upon, etc in our [community slack](https://slack.shopware.com). See you there ;)

---

---

## Release notes Shopware 6.5.8.7
**Source:** [release-notes/6.5/6.5.8.7.md](https://developer.shopware.com/release-notes/6.5/6.5.8.7.md)  
# Release notes Shopware 6.5.8.7

## Abstract

Shopware v6.5.8.7 is a **security release** to fix a bug where the 404 page cache might contain session IDs. The cookie will be only persist to caching when the browser had no cookie before. Hence, it is not possible to obtain the session of an authenticated customer.
This issue is only relevant from Shopware >= 6.5.8.0, for older versions a fix is not required.

## System requirements

* tested on PHP 8.1, 8.2 and 8.3
* tested on MySQL 8.0.33, MariaDB 10.4. 10.5, 10.11 & 11.0

## Fixed bugs

* [Session is persistent in Cache for 404 pages (GHSA-c2f9-4jmm-v45m)](https://github.com/shopware/shopware/security/advisories/GHSA-c2f9-4jmm-v45m)
* [NEXT-34113 - Clear cookies on 404 pages](https://github.com/shopware/shopware/blob/v6.5.8.7/changelog/release-6-5-8-7/2024-03-04-clear-cookies-on-404-pages.md)

## More resources

* [Detailed diff on Github](https://github.com/shopware/shopware/compare/v6.5.8.6...v6.5.8.7) to the former version
* [Changelog on GitHub](https://github.com/shopware/shopware/blob/v6.5.8.7/CHANGELOG.md) for this version.
* [Installation overview](https://developer.shopware.com/docs/guides/installation/)
* [Update from a previous installation](https://developer.shopware.com/docs/guides/installation/template.html#update-shopware)

## Get in touch

Discuss about decisions, bugs you might stumble upon, etc in our [community slack](https://slack.shopware.com). See you there ;)

---

---

## Release notes Shopware 6.5.8.8
**Source:** [release-notes/6.5/6.5.8.8.md](https://developer.shopware.com/release-notes/6.5/6.5.8.8.md)  
# Release notes Shopware 6.5.8.8

## Abstract

Shopware v6.5.8.8 is a **security release** to fix improper session handling in store api account logout. Additionally, 18+ bugs have been fixed.

## System requirements

* tested on PHP 8.1, 8.2 and 8.3
* tested on MySQL 8.0.33, MariaDB 10.4. 10.5, 10.11 & 11.0

## Fixed bugs

* [NEXT-23962](https://issues.shopware.com/issues/NEXT-23962) | Contact form - page cannot be used without reloading the modal (42 votes)
* [NEXT-14691](https://issues.shopware.com/issues/NEXT-14691) | Add pseudo modal twig blocks (Elias Lackner) (33 votes)
* [NEXT-34012](https://issues.shopware.com/issues/NEXT-34012) | Wrong URL in product-export Feed for Google Merchant Center (16 votes)
* [NEXT-11827](https://issues.shopware.com/issues/NEXT-11827) | MediaService creates temporary files that are never cleaned up (14 votes)
* [NEXT-33846](https://issues.shopware.com/issues/NEXT-33846) | Missing Indexer in setDeletedNewsletterRecipients causes Dead Messeges spam (5 votes)
* [NEXT-31922](https://issues.shopware.com/issues/NEXT-31922) | Order details shipping and billing address select does not work correctly (5 votes)
* [NEXT-31040](https://issues.shopware.com/issues/NEXT-31040) | CustomField Type "Media" - missing pagination in media selection / search results (4 votes)
* [NEXT-34027](https://issues.shopware.com/issues/NEXT-34027) | Indexing results in an exception, when a inherting language is used (4 votes)
* [NEXT-34323](https://issues.shopware.com/issues/NEXT-34323) | Broken product slider in backend with assignment to a deleted product (3 votes)
* [NEXT-31710](https://issues.shopware.com/issues/NEXT-31710) | UnusedMediaSubscriber uses method JSON\_OVERLAPS that does not exist in "supported" MariaDB versions (3 votes)
* [NEXT-34113](https://issues.shopware.com/issues/NEXT-34113) | Session Hijacking (2 votes)
* [NEXT-34102](https://issues.shopware.com/issues/NEXT-34102) | Add new block in analytics template (Wanne Van Camp) (1 vote)
* [NEXT-32339](https://issues.shopware.com/issues/NEXT-32339) | Possible to delete connected media\_thumbnail\_size (0 votes)
* [NEXT-33748](https://issues.shopware.com/issues/NEXT-33748) | (Github) Update sw-media-modal-v2.html.twig (0 votes)
* [NEXT-34023](https://issues.shopware.com/issues/NEXT-34023) | Slow query for product search via term (0 votes)
* [NEXT-34181](https://issues.shopware.com/issues/NEXT-34181) | Partial Criteria | ManyToManyAssociationField Error (0 votes)
* [NEXT-34165](https://issues.shopware.com/issues/NEXT-34165) | review backdrop opens twice on mobile view (0 votes)
* [NEXT-34478](https://issues.shopware.com/issues/NEXT-34478) | No cache force for snippets (0 votes)
* [NEXT-34608](https://github.com/shopware/shopware/security/advisories/GHSA-5297-wrrp-rcj7) | Improper Session Handling in store-api account logout (0 votes)

## Credits

Thanks to all diligent friends for helping us make Shopware better and better with each pull request!

* [Wanne Van Camp](https://github.com/wannevancamp)
* [Elias Lackner](https://github.com/lacknere)

## More resources

* [Detailed diff on Github](https://github.com/shopware/shopware/compare/v6.5.8.7...v6.5.8.8) to the former version
* [Changelog on GitHub](https://github.com/shopware/shopware/blob/v6.5.8.8/CHANGELOG.md) for this version.
* [Installation overview](https://developer.shopware.com/docs/guides/installation/)
* [Update from a previous installation](https://developer.shopware.com/docs/guides/installation/template.html#update-shopware)

## Get in touch

Discuss about decisions, bugs you might stumble upon, etc in our [community slack](https://slack.shopware.com). See you there ;)

---

---

## Release notes Shopware 6.5.8.9
**Source:** [release-notes/6.5/6.5.8.9.md](https://developer.shopware.com/release-notes/6.5/6.5.8.9.md)  
# Release notes Shopware 6.5.8.9

## Abstract

This patch release belongs to the extended support for Shopware 6.5 series and contains a few bug fixes.

## System requirements

* tested on PHP 8.1, 8.2 and 8.3
* tested on MySQL 8.0.33, MariaDB 10.4. 10.5, 10.11 & 11.0

## Fixed bugs

* [NEXT-32927](https://issues.shopware.com/issues/NEXT-32927) | Switch edit modes to html doesn't save new content (13 votes)
* [NEXT-34914](https://issues.shopware.com/issues/NEXT-34914) | Form validation does not work with activated captcha (1 votes)
* [NEXT-35111](https://issues.shopware.com/issues/NEXT-35111) | After logging out customer\_id is now set to NULL in the sales\_channel\_api\_context (1 votes)
* [NEXT-31926](https://issues.shopware.com/issues/NEXT-31926) | ban()/banAll() function for Varnish uses PURGE (0 votes)

## More resources

* [Detailed diff on Github](https://github.com/shopware/shopware/compare/v6.5.8.8...v6.5.8.9) to the former version
* [Changelog on GitHub](https://github.com/shopware/shopware/blob/v6.5.8.9/CHANGELOG.md) for this version.
* [Installation overview](https://developer.shopware.com/docs/guides/installation/)
* [Update from a previous installation](https://developer.shopware.com/docs/guides/installation/template.html#update-shopware)

## Get in touch

Discuss about decisions, bugs you might stumble upon, etc in our [community slack](https://slack.shopware.com). See you there ;)

---

---

## Release notes Shopware 6.6.0.0
**Source:** [release-notes/6.6/6.6.0.0.md](https://developer.shopware.com/release-notes/6.6/6.6.0.0.md)  
*(Body truncated in this bundle; follow the link for the rest.)*

# Release notes Shopware 6.6.0.0

## Abstract

Shopware 6.6.0.0 is a major release containing breaking changes.
Please read this document and the linked resources carefully. The system requirements have changed, and third-party dependencies have been updated, as explained below.

This release was built with the help of the community. Thank you for supporting us during the twelve-week RC phase by providing feedback and testing the release under production-like conditions, and thank you for 34 code contributors with 64 merged pull requests in this release.

With this release, we are also officially introducing a new release policy that provides up to two years of support for major versions, starting with Shopware 6.5. A detailed explanation can be found in our blog: [Shopware's new Release Policy](https://www.shopware.com/en/news/shopwares-new-release-policy/)

The Shopware 6.6.0.0 release is focused on core changes instead of features. It provides a foundation for adding new features throughout future minor releases.

## System requirements

* tested on PHP 8.2 and 8.3
* tested on MySQL 8 and MariaDB 10.11

See below for more information on the current minimum versions.

## Improvements

### Removal of deprecations

All code marked as deprecated for 6.6 was removed. This potentially breaks extensions and other customizations. Please see the  [UPGRADE.md](https://github.com/shopware/shopware/blob/trunk/UPGRADE-6.6.md) for detailed information on what has changed.

### Removal of feature flags

Some specific features have already been released and marked with a feature flag. These features are now active by default, introducing breaking changes and requiring code updates:

* New media path behaviour
* Stock Handling
* Change ElasticSearch mapping data to support multi-languages in one index
* Vuejs 3
* Asynchronous theme compilation via message queue
* Async JS plugin loading
* Caching layer improvements

See [details on Github](https://github.com/search?q=repo%3Ashopware%2Fshopware++Feature%3A%3AisActive\('v6.6.0.0'\)\&type=code)

### Removal of experimental state

The experimental annotation has been removed from features.

* AsyncThemeCompilation
* QuoteManagement
* Async JS plugin loading

These and a few more features are now stable and can be used in production.

### Vue.js update

[Vue.js 2 is no longer supported](https://endoflife.date/vue) since the end of 2023. We updated the administration component to the latest version of Vue.js, ensuring our customers receive up-to-date and compliant software. A tutorial on how to adapt your plugin-system-based extension to Vue.js 3 is available in the [documentation](https://developer.shopware.com/docs/resources/references/upgrades/administration/vue3.html).

### Webpack update

We updated [Webpack](https://webpack.js.org/) to version 5. The new version and switching from Babel zu [SWC](https://swc.rs/) makes building the administration three times faster. Plugin-system-based extensions with a custom webpack configuration must be migrated to the webpack 5 API.

### Node 20 as the minimum version

As [discussed](https://github.com/shopware/shopware/discussions/3359), the minimum version requirement for Node was changed from 18 to 20. Version 20 is the current LTS version with active support until the end of 2024 and maintenance support until mid-2026.

### Configurable auto logout

The administration login form now has the option to stay signed in, keeping the user logged in for 14 days instead of the previous 30 minutes.

![](assets/shopware6_admin_login.png)

### Symfony upgrade

Shopware 6.6.0.0 upgraded Symfony to the current stable major version 7, as previously announced on [GitHub discussions](https://github.com/shopware/shopware/discussions/3354). More about breaking changes in this Symfony upgrade can be found in [Symfony's upgrade guide](https://github.com/symfony/symfony/blob/7.0/UPGRADE-7.0.md).

### PHP 8.2 as the minimum requirement

With the upgrade to Symfony 7, PHP 8.2 will become the new minimum required version. Refer to the [release information by Symfony](https://symfony.com/releases/7.0) and **check compatibility with your hosting provider**.

### Maria DB 10.11 minimum requirement

The minimum version requirement for Maria DB now is the latest LTS version, v10.11. This version supports the `JSON_OVERLAPS` function, which the "delete unused media" feature needs. MySQL was previously changed to a minimum version of 8.0.

### Redis 7.0 minimum requirement

The minimum version requirement for Redis now is v7.0. It comes with performance improvements and allows using the new [redis function feature](https://redis.io/docs/interact/programmability/functions-intro/).

### Upgrading third-party composer dependencies

We upgraded some third-party composer dependencies, such as `lcobucci/jwt` to v5 or higher and `async-aws/simple-s3` to v2 or higher.

### Stock API changes

We simplified the way Shopware stores stock data and made the system more extendable for developers. It became easier to supplement the stock information with user-defined data and to send it to third-party systems. It is also possible to turn off Shopware's stock management altogether. The new Stock API was introduced in Shopware 6.5.5 behind the `STOCK_HANDLING` feature flag; it is now the default method in Shopware 6.6.

To keep the impact as low as possible, we kept the backwards compatibility for reading the stock. Please note that the feature *multi-inventory* has yet to be compatible. Find more details in the [discussions](https://github.com/shopware/shopware/discussions/3172), the [changelog](https://github.com/shopware/shopware/blob/trunk/changelog/release-6-5-5-0/2023-06-21-stock-refactoring.md), and in our [docs for extending the API](https://developer.shopware.com/docs/guides/plugins/plugins/content/stock/).

### Persistent media path storage

The path to media is now stored in the database instead of being generated on the fly. Please read more about this topic in [discussions](https://github.com/shopware/shopware/discussions/3174).

### Improving the caching layer

Improvements on the caching layer were previously available behind a feature flag. They are now active and available by default. Read [discussion #3299](https://github.com/shopware/shopware/discussions/3299) and [discussion #3171](https://github.com/shopware/shopware/discussions/3171) for more information.

### Availability of symfony/scheduler

Symfony recently added a scheduler component, and we want to use as many official Symfony components as possible. Starting with Shopware 6.6, the Symfony scheduler can be used to execute scheduled tasks instead of the custom Shopware scheduler. For details on how to set it up, take a look at the [documentation](https://developer.shopware.com/docs/v6.6rc/guides/hosting/infrastructure/scheduled-task.html#using-the-symfony-scheduler-to-run-tasks).

### Multilingual ElasticSearch index

The ElasticSearch index is no longer split by language. Translated fields are mapped as object fields. This change in indexing brings performance improvements. Please be aware of this when providing custom properties in ElasticSearch. For more details, please read our [architecture decision record](https://github.com/shopware/shopware/blob/trunk/adr/2023-04-11-new-language-inheritance-mechanism-for-opensearch.md).

### Async JavaScript loading

By introducing asynchronous JS loading and allowing dynamic imports, we could [increase the storefront performance](https://www.shopware.com/en/news/storefront-performance-improvements-with-shopware-6-6/) and smoothen the JS handling. Read the [discussions](https://github.com/shopware/shopware/discussions/3310) and the [documentation](https://developer.shopware.com/docs/v6.6rc/guides/plugins/plugins/storefront/add-custom-javascript.html#registering-an-async-plugin) for more details.

### Removal of SCSS code

Custom SCSS code was removed from Shopware if it already existed in Bootstrap. Please read more about this in our [architecture decision record](https://github.com/shopware/shopware/blob/trunk/adr/2023-10-19-bootstrap-css-utils.md).

### Low-priority Queue

Before Shopware 6.6.0.0, workers automatically consumed the low-priority queue. Workers for the low-priority queue now have to be started separately. For more details, take a look at the [upgrade guide](https://github.com/shopware/shopware/blob/v6.6.0.0-rc6/UPGRADE-6.6.md#configure-queue-workers-to-consume-low_priority-queue).

## Fixed bugs

* [NEXT-30575](https://issues.shopware.com/issues/NEXT-30575) | HTML sanitizer on mail template header & footer (42 votes)
* [NEXT-15942](https://issues.shopware.com/issues/NEXT-15942) | \[github] Compiled storefront JS with modules can't be executed in prod env (41 votes)
* [NEXT-22217](https://issues.shopware.com/issues/NEXT-22217) | Misleading Replace / Rename function in Contents>Media (33 votes)
* [NEXT-26321](https://issues.shopware.com/issues/NEXT-26321) | payment status isn't fully changed (32 votes)
* [NEXT-28671](https://issues.shopware.com/issues/NEXT-28671) | COMMERCIAL: admin is no longer accessible when Commercial is activated. (30 votes)
* [NEXT-29439](https://issues.shopware.com/issues/NEXT-29439) | In the frontend, the products are displayed twice on several pages with the standard sorting "Topseller" (26 votes)
* [NEXT-30489](https://issues.shopware.com/issues/NEXT-30489) | Sanitize: Making shopware's own snippets unusable (24 votes)
* [NEXT-23962](https://issues.shopware.com/issues/NEXT-23962) | Contact form - page cannot be used without reloading the modal (23 votes)
* [NEXT-32925](https://issues.shopware.com/issues/NEXT-32925) | Support for "Google Consent Mode v2" (18 votes)
* [NEXT-30785](https://issues.shopware.com/issues/NEXT-30785) | Country/region is defined as a mandatory field, but is not requested in the checkout (17 votes)
* [NEXT-30672](https://issues.shopware.com/issues/NEXT-30672) | \[Github] Fix for distorted Thumbnails (17 votes)
* [NEXT-17301](https://issues.shopware.com/issues/NEXT-17301) | Error when trying to add properties to variants, if the main product does not have any properties assigned (17 votes)
* [NEXT-34012](https://issues.shopware.com/issues/NEXT-34012) | Wrong URL in product-export Feed for Google Merchant Center (16 votes)
* [NEXT-19420](https://issues.shopware.com/issues/NEXT-19420) | Internal linking to a landingpage doesn't work properly, even with sitemap (16 votes)
* [NEXT-18778](https://issues.shopware.com/issues/NEXT-18778) | Test mails do not contain mail header and footer in correct language (15 votes)
* [NEXT-23783](https://issues.shopware.com/issues/NEXT-23783) | Affiliate Code / Campaign Code Tracking not working when you initiale enter the shop with tracking URL (14 votes)
* [NEXT-22973](https://issues.shopware.com/issues/NEXT-22973) | Snippet renaming leads to vanishing of it | Snippet-Umbenennung führt zum Verschwinden des Snippets (14 votes)
* [NEXT-11827](https://issues.shopware.com/issues/NEXT-11827) | MediaService creates temporary files that are never cleaned up (14 votes)
* [NEXT-33881](https://issues.shopware.com/issues/NEXT-33881) | Cannot request 'user-verified' scope for client\_credentials (13 votes)
* [NEXT-24580](https://issues.shopware.com/issues/NEXT-24580) | Versandstatus in Bestellübersicht stimmt nicht mit Versandstatus in Bestell-Detailansicht überein (13 votes)
* [NEXT-24159](https://issues.shopware.com/issues/NEXT-24159) | Problem loading snippets from parent of parent theme (13 votes)
* [NEXT-32276](https://issues.shopware.com/issues/NEXT-32276) | Custom sort in Category listing leads to 404 (12 votes)
* [NEXT-29601](https://issues.shopware.com/issues/NEXT-29601) | Storno PDF wird aus aktuellen Daten generiert. (12 votes)
* [NEXT-32133](https://issues.shopware.com/issues/NEXT-32133) | Order: Can not change order status (11 votes)
* [NEXT-31769](https://issues.shopware.com/issues/NEXT-31769) | ES admin search is broken with t

… **Truncated.** Full document: https://developer.shopware.com/release-notes/6.6/6.6.0.0.md


---

## Release notes Shopware 6.6.0.1
**Source:** [release-notes/6.6/6.6.0.1.md](https://developer.shopware.com/release-notes/6.6/6.6.0.1.md)  
# Release notes Shopware 6.6.0.1

## Abstract

This patch release contains just one bug, fixing a problem that the storefront was not available after an update as a specific change in a database column was expected. This change didn't take effect if a destructive migration has not been run for a long time (< v6.5) and just the `system:update:finish` command was used.

## System requirements

* tested on PHP 8.2 and 8.3
* tested on MySQL 8 and MariaDB 10.11

## Fixed bugs

* [NEXT-34524](https://issues.shopware.com/issues/NEXT-34524) | Missing migration for payload column in cart table (0 votes)

## More resources

* [Detailed diff on Github](https://github.com/shopware/shopware/compare/v6.6.0.0...v6.6.0.1) to the former version
* [Changelog on GitHub](https://github.com/shopware/shopware/blob/v6.6.0.1/CHANGELOG.md) for this version.
* [Installation overview](https://developer.shopware.com/docs/guides/installation/)
* [Update from a previous installation](https://developer.shopware.com/docs/guides/installation/template.html#update-shopware)

## Get in touch

Discuss about decisions, bugs you might stumble upon, etc in our [community slack](https://slack.shopware.com). See you there ;)

---

---

## Release notes Shopware 6.6.0.2
**Source:** [release-notes/6.6/6.6.0.2.md](https://developer.shopware.com/release-notes/6.6/6.6.0.2.md)  
# Release notes Shopware 6.6.0.2

## Abstract

This patch release fixes a bug where (in dependency of CMS options taken) the default order on listing pages have been influenced. As a result, some listings have not been displayed on these pages. This is why we added a migration to change the sorting key accordingly in CMS slots to fix potential problems with the loading of listings.

## System requirements

* tested on PHP 8.2 and 8.3
* tested on MySQL 8 and MariaDB 10.11

## Fixed bugs

* [NEXT-34640](https://issues.shopware.com/issues/NEXT-34640) | Some Categories are not working (4 votes)

## More resources

* [Detailed diff on Github](https://github.com/shopware/shopware/compare/v6.6.0.1...v6.6.0.2) to the former version
* [Changelog on GitHub](https://github.com/shopware/shopware/blob/v6.6.0.2/CHANGELOG.md) for this version.
* [Installation overview](https://developer.shopware.com/docs/guides/installation/)
* [Update from a previous installation](https://developer.shopware.com/docs/guides/installation/template.html#update-shopware)

## Get in touch

Discuss about decisions, bugs you might stumble upon, etc in our [community slack](https://slack.shopware.com). See you there ;)

---

---

## Release notes Shopware 6.6.0.3
**Source:** [release-notes/6.6/6.6.0.3.md](https://developer.shopware.com/release-notes/6.6/6.6.0.3.md)  
# Release notes Shopware 6.6.0.3

## Abstract

This patch release fixes a bug where snippets (language keys) have not been resolved, depending on which sales channel the cache was built. Additionally, we could optimize the caching mechanism.

## System requirements

* tested on PHP 8.2 and 8.3
* tested on MySQL 8 and MariaDB 10.11

## Fixed bugs

* [NEXT-34783](https://issues.shopware.com/issues/NEXT-34783) | Snippets display technical name (4 votes)
* [NEXT-30065](https://github.com/shopware/shopware/blob/v6.6.0.3/changelog/release-6-6-0-3/2024-04-04-next-30065.md) | Fix session access in AffiliateTrackingListener (Optimized caching mechanism, 0 votes)

## More resources

* [Detailed diff on Github](https://github.com/shopware/shopware/compare/v6.6.0.2...v6.6.0.3) to the former version
* [Changelog on GitHub](https://github.com/shopware/shopware/blob/v6.6.0.3/CHANGELOG.md) for this version.
* [Installation overview](https://developer.shopware.com/docs/guides/installation/)
* [Update from a previous installation](https://developer.shopware.com/docs/guides/installation/template.html#update-shopware)

## Get in touch

Discuss about decisions, bugs you might stumble upon, etc in our [community slack](https://slack.shopware.com). See you there ;)

---

---

## Release notes Shopware 6.6.1.0
**Source:** [release-notes/6.6/6.6.1.0.md](https://developer.shopware.com/release-notes/6.6/6.6.1.0.md)  
*(Body truncated in this bundle; follow the link for the rest.)*

# Release notes Shopware 6.6.1.0

## Abstract

This minor release comes with a lot of improvements, such as staging mode, a new HTML element in CMS, media cleanup as well as S3 speed improvements. Additionally, ~80 bugs were fixed.

## System requirements

* tested on PHP 8.2 and 8.3
* tested on MySQL 8 and MariaDB 10.11

## Improvements

### Staging Mode

We added a staging mode to Shopware, which helps you to mark an instance as a staging environment. This is useful for development and testing purposes. It allows to change the sales channel domain url, shows a banner in the Administration or Storefront and much more. For more information, check out the [docs for staging mode](https://developer.shopware.com/docs/guides/hosting/configurations/shopware/staging.html).

### HTML code element

The HTML code element is a new element in Shopping Experiences. This element allows you to add custom HTML code to Shopping Experience without conflicting with the HTML sanitization.

### Improved Elasticsearch/Opensearch logging

We changed the log\_level to `error` for Elasticsearch/Opensearch logging. This will reduce the amount of log entries in the log file in production mode.

### HTML sanitization optimization

The mail header and footer are not sanitized anymore. This allows you now to use any HTML tags in the mail header and footer.

The HTML sanitization now also supports all HTML5 tags and attributes.

### user:list command

We added a new command `user:list` to the CLI. This command lists all users in the system. This command have also a `--json` flag to interact with external tools like jq.

### Deprecation of dal:create:schema

The command `dal:create:schema` is deprecated and will be removed in the next major release. Please use as replacement the `dal:migration:create` command, this diffes your DAL schema to the current database and creates a migration file.

### Various OpenAPI schema improvements

We improved the OpenAPI schema in various places. We added missing properties, fixed wrong types and added missing descriptions.

### MediaService cleanups now the temporary created files

The MediaService now cleans up the temporary created files after the media has been processed.

### Store-api route to fetch media elements

Sometimes in custom fields or other fields are the media id stored, But you need in the Storefront the media url. We added a new route to fetch the media elements by media id.

```http
POST /store-api/media
Accept: application/json
sw-access-key: YOUR_ACCESS_KEY
Content-Type: application/json

{
    "ids" : [
        "018d8922df51736c98bec29c2d1f813f",
        "018d8923a32879cfadf561fb02c479e0"
    ]
}
```

### HMAC based JWT

Using private/public keys (asymmetric encryption) for JWT is now deprecated and will be removed with the next major release. Replacement for this is the HMAC based JWT, this allows us to use the existing `APP_SECRET` environment file and get rid of `config/jwt` folder. This makes hosting Shopware in a containerized environment a lot easier, as you don't need to mount the `config/jwt` folder anymore.

### Improved search on Product search in the administration

The search in the product listing in the administration is not considereing anymore category names and tag names attached to the products. This improves the search performance with MySQL a lot.

### Context::createDefaultContext is now internal

The method `Context::createDefaultContext` is now marked internal. With this decision we want to prevent that developers for wrong usage. In HTTP requests the context is created automatically and attached to the Request object. The only place where the Context is unknown is the `console` context. In this case you should use the `Context::createCLIContext` method.

### Spotlight Elements will replace Swagger UI

We deprecated the Swagger UI (`/api/_info/swagger.html`) and will replace it with the Spotlight Elements. The Spotlight Elements are a more modern and user-friendly way to interact with the API. The Spotlight Elements are available under `/api/_info/swagger.html`. This solves also the problem that the payload can't be shown in the Swagger UI.

### Improved s3 copy-speed

We improved the CopyBatch plugin to copy multiple files asynchronously. This improves the speed of the s3 copy operation a lot. This benefits `bin/console theme:compile` or `bin/console assets:install`

#### Before

| Command                | Local | AWS S3  | Cloudflare R2 |
|------------------------|-------|---------|---------------|
| theme:compile          | 1.09s | 24.72s  | 91.30s        |
| asset:install --force\* | 1.09s | 192.05s | 892.11s       |

#### After

| Command                | Local | AWS S3  | Cloudflare R2 |
|------------------------|-------|---------|---------------|
| theme:compile          | 1.09s | 6.5s    | 17.91s        |
| asset:install --force\* | 1.09s | 41.12s  | 141.38        |

* * the `asset:install` command uses a manifest file to only upload the changed files to the s3 bucket. The `--force` flag disables this feature and uploads all files, to have a better comparison.

## Fixed bugs

* [NEXT-17867](https://issues.shopware.com/issues/NEXT-17867) | Strrev does not support utf8 properly (23 votes)
* [NEXT-28620](https://issues.shopware.com/issues/NEXT-28620) | Delete Payment methods (17 votes)
* [NEXT-33431](https://issues.shopware.com/issues/NEXT-33431) | Async component factory breaks on second call to function that extends parent method (16 votes)
* [NEXT-32133](https://issues.shopware.com/issues/NEXT-32133) | Order: Can not change order status (11 votes)
* [NEXT-21544](https://issues.shopware.com/issues/NEXT-21544) | Order status cannot be exported (10 votes)
* [NEXT-31030](https://issues.shopware.com/issues/NEXT-31030) | Shopware Commercial throws error when password recovery detects inactive user (9 votes)
* [NEXT-32942](https://issues.shopware.com/issues/NEXT-32942) | Email Header/Footer wird nicht angehängt (8 votes)
* [NEXT-24683](https://issues.shopware.com/issues/NEXT-24683) | Image slider breaks when deleting media files (8 votes)
* [NEXT-31749](https://issues.shopware.com/issues/NEXT-31749) | Losing page content in the administration when switching from a selected category to a landing page (6 votes)
* [NEXT-30360](https://issues.shopware.com/issues/NEXT-30360) | order\_count/orders\_per\_customer\_count wrong for promotions with individual codes (6 votes)
* [NEXT-32365](https://issues.shopware.com/issues/NEXT-32365) | "Discount promotions" field greyed out for non-admin users despite rights to orders (5 votes)
* [NEXT-31922](https://issues.shopware.com/issues/NEXT-31922) | Order details shipping and billing address select does not work correctly (5 votes)
* [NEXT-31729](https://issues.shopware.com/issues/NEXT-31729) | Conversion of the volume in the Rule Builder is not accurate (5 votes)
* [NEXT-34027](https://issues.shopware.com/issues/NEXT-34027) | Indexing results in an exception, when a inherting language is used (4 votes)
* [NEXT-33913](https://issues.shopware.com/issues/NEXT-33913) | Wording Issue in the Flow Builder (German only) (4 votes)
* [NEXT-33867](https://issues.shopware.com/issues/NEXT-33867) | sw-settings-loggin-list calls this.$options.components (4 votes)
* [NEXT-29093](https://issues.shopware.com/issues/NEXT-29093) | "label" attribute inheritance of theme variables does not work anymore (4 votes)
* [NEXT-34312](https://issues.shopware.com/issues/NEXT-34312) | Aktive commecial plugin: Error messages on Checkout Confirm page are not displayed (3 votes)
* [NEXT-34068](https://issues.shopware.com/issues/NEXT-34068) | The "Send email" action is missing in Flow Builder Delayed Actions (3 votes)
* [NEXT-33503](https://issues.shopware.com/issues/NEXT-33503) | Video cms element loaded when saving cookie settings - even if the video cookie was not accepted (3 votes)
* [NEXT-33146](https://issues.shopware.com/issues/NEXT-33146) | No full screen on YouTube Player (3 votes)
* [NEXT-32770](https://issues.shopware.com/issues/NEXT-32770) | Discount calculation in existing order - Rabattkalkulation in bestehender Bestellung (3 votes)
* [NEXT-33028](https://issues.shopware.com/issues/NEXT-33028) | Store API change default address route not allowed for guest users (2 votes)
* [NEXT-32989](https://issues.shopware.com/issues/NEXT-32989) | HTML entities in the SEO fields (2 votes)
* [NEXT-32254](https://issues.shopware.com/issues/NEXT-32254) | Manuelle aktivierung der Benutzer nicht möglich. (2 votes)
* [NEXT-30892](https://issues.shopware.com/issues/NEXT-30892) | Custom Fields for Media: View of the custom field content in the Admin not updating correctly (2 votes)
* [NEXT-30769](https://issues.shopware.com/issues/NEXT-30769) | Preview Mode Rule Builder wrong results (2 votes)
* [NEXT-34155](https://issues.shopware.com/issues/NEXT-34155) | custom/plugins path hardcoded in TestBootstrapper.php (1 votes)
* [NEXT-33484](https://issues.shopware.com/issues/NEXT-33484) | Displaying the order overview in the backend makes shop unavailable (because of promotion code filter) (1 votes)
* [NEXT-33359](https://issues.shopware.com/issues/NEXT-33359) | Incorrect label in the selection field for the e-mail template when sending a document (1 votes)
* [NEXT-32920](https://issues.shopware.com/issues/NEXT-32920) | first- and lastname fields in the newsletter subscription form no required fields (1 votes)
* [NEXT-28908](https://issues.shopware.com/issues/NEXT-28908) | Chrome memory and display bug in 6.4.20.2 (1 votes)
* [NEXT-28055](https://issues.shopware.com/issues/NEXT-28055) | Ace editor only accepts new value on blur (1 votes)
* [NEXT-34665](https://issues.shopware.com/issues/NEXT-34665) | Disable PHPBench (0 votes)
* [NEXT-34654](https://issues.shopware.com/issues/NEXT-34654) | \[Github] chore: Add sales channel context getter to CustomerDoubleOptInRegistrationEvent (0 votes)
* [NEXT-34653](https://issues.shopware.com/issues/NEXT-34653) | \[Github] NEXT-0000 - Check invalid rules with DAL before fetching (0 votes)
* [NEXT-34650](https://issues.shopware.com/issues/NEXT-34650) | \[Github] NEXT-00000 - Add options argument to recalculate order (0 votes)
* [NEXT-34649](https://issues.shopware.com/issues/NEXT-34649) | \[Github] NEXT-00000 - Add customer data to CustomerDeletedEvent (0 votes)
* [NEXT-34616](https://issues.shopware.com/issues/NEXT-34616) | \[Github] Add sanitize field name for cms text (0 votes)
* [NEXT-34525](https://issues.shopware.com/issues/NEXT-34525) | \[Github] NEXT-00000 - Support webpack config ts (0 votes)
* [NEXT-34503](https://issues.shopware.com/issues/NEXT-34503) | \[Github] Add column assigned pages to CMS list (0 votes)
* [NEXT-34491](https://issues.shopware.com/issues/NEXT-34491) | \[Github] NEXT-14691 - Add pseudo modal twig blocks (0 votes)
* [NEXT-34478](https://issues.shopware.com/issues/NEXT-34478) | No cache force for snippets. (0 votes)
* [NEXT-34455](https://issues.shopware.com/issues/NEXT-34455) | Filtering order with non default languages throws a JS error (0 votes)
* [NEXT-34435](https://issues.shopware.com/issues/NEXT-34435) | Fixed Playwright documentation link (0 votes)
* [NEXT-34415](https://issues.shopware.com/issues/NEXT-34415) | \[Github] refactor: Product card action template (0 votes)
* [NEXT-34411](https://issues.shopware.com/issues/NEXT-34411) | \[Github] NEXT-29093 - Fix theme config label inheritance (0 votes)
* [NEXT-34410](https://issues.shopware.com/issues/NEXT-34410) | \[Github] fix: Allow Twig array filters to accept null (0 votes)
* [NEXT-34399](https://issues.shopware.com/issues/NEXT-34399) | \[Github] NEXT-0000 - Update action.html.twig to include css class for detail button (0 votes)
* [NEXT-34381](https://issues.shopware.com/issues/NEXT-34381) | media components needs to refresh when replacing an image (0 votes)
* [NEXT-34361](https://issues.shopware.com/issues/NEXT-34361) | ThemeCompiler cannot be decorated in async CompileThemeHandler (0 votes)
* [NEXT-34330](htt

… **Truncated.** Full document: https://developer.shopware.com/release-notes/6.6/6.6.1.0.md


---

## Release notes Shopware 6.6.1.1
**Source:** [release-notes/6.6/6.6.1.1.md](https://developer.shopware.com/release-notes/6.6/6.6.1.1.md)  
# Release notes Shopware 6.6.1.1

## Abstract

This patch release contains two bug fixes.

## System requirements

* tested on PHP 8.2 and 8.3
* tested on MySQL 8 and MariaDB 10.11

## Fixed bugs

* [NEXT-31926](https://issues.shopware.com/issues/NEXT-31926) | ban()/banAll() function for Varnish uses PURGE (0 votes)
* [NEXT-35121](https://github.com/shopware/shopware/blob/v6.6.1.1/changelog/release-6-6-1-1/2024-04-16-recompile-on-plugins-with-additional-bundles.md) | Recompile theme on plugin with additional bundles (0 votes)

## More resources

* [Detailed diff on Github](https://github.com/shopware/shopware/compare/v6.6.1.0...v6.6.1.1) to the former version
* [Changelog on GitHub](https://github.com/shopware/shopware/blob/v6.6.1.1/CHANGELOG.md) for this version.
* [Installation overview](https://developer.shopware.com/docs/guides/installation/)
* [Update from a previous installation](https://developer.shopware.com/docs/guides/installation/template.html#update-shopware)

## Get in touch

Discuss about decisions, bugs you might stumble upon, etc in our [community slack](https://slack.shopware.com). See you there ;)

---

---

## Release notes Shopware 6.6.1.2
**Source:** [release-notes/6.6/6.6.1.2.md](https://developer.shopware.com/release-notes/6.6/6.6.1.2.md)  
# Release notes Shopware 6.6.1.2

## Abstract

This patch release contains two bug fixes.

## System requirements

* tested on PHP 8.2 and 8.3
* tested on MySQL 8 and MariaDB 10.11

## Fixed bugs

* [NEXT-35585](https://issues.shopware.com/issues/NEXT-35585) | Shipping price matrixes only accept rules instead of property conditions (1 votes)
* [NEXT-35571](https://issues.shopware.com/issues/NEXT-35571) | Block Twig 3.9 update (0 votes)

## More resources

* [Detailed diff on Github](https://github.com/shopware/shopware/compare/v6.6.1.1...v6.6.1.2) to the former version
* [Changelog on GitHub](https://github.com/shopware/shopware/blob/v6.6.1.2/CHANGELOG.md) for this version.
* [Installation overview](https://developer.shopware.com/docs/guides/installation/)
* [Update from a previous installation](https://developer.shopware.com/docs/guides/installation/template.html#update-shopware)

## Get in touch

Discuss about decisions, bugs you might stumble upon, etc in our [community slack](https://slack.shopware.com). See you there ;)

---

---

## Release notes Shopware 6.6.10.0
**Source:** [release-notes/6.6/6.6.10.0.md](https://developer.shopware.com/release-notes/6.6/6.6.10.0.md)  
# Release notes Shopware 6.6.10.0

## Abstract

This minor release contains improvements like MySQL invalidator storage, external media URLs via API, even more A11y improvents and more. Additionally, 10+ bugs had been fixed.

## System requirements

* tested on PHP 8.2 and 8.3
* tested on MySQL 8 and MariaDB 10.11

## Improvements

### Upgrade to Symfony 7.2

* Changed `symfony/*` dependencies to `^7.2`

### Addition of MySQLInvalidatorStorage

* Introduced `/Shopware/Core/Framework/Adapter/Cache/InvalidatorStorage/MySQLInvalidatorStorage` to collect and handle cache invalidations in MySQL as an atomic operation.
* This new storage option allows delayed cache invalidation without requiring Redis (although Redis remains the recommended solution).
* To switch to MySQL for delayed cache invalidation, update your configuration as follows:

```yaml
shopware:
    cache:
        invalidation:
            delay: 1
            delay_options:
                storage: mysql
```

### \[A11y-HTML] Offer HTML alternative to our pdf standard documents

* Besides the existing PDF document which is based on DOMPDF, we added our standard document as HTML documents for fulfilling the A11y criteria.

### Introduce global template data for language and navigation

Some of the data for the Twig template in the storefront, like the current currency or navigation ID, should not depend on the current page object; instead, the should be available globally and independently. The following changes facilitate the introduction of those global template data:

* Added new Twig function `sw_breadcrumb_full_by_id` to get the full breadcrumb for a category ID.
* Added /Shopware/Storefront/Framework/Twig/NavigationInfo to the global shopware Twig variable, to provide the ID of the main navigation and the current navigation path as ID list.
* Added `minSearchLength` to the global Shopware Twig variable, which defines the minimum search term length.
* Added `showStagingBanner` to the global shopware Twig variable, which defines if the staging banner should be shown.
* Deprecated the global `showStagingBanner` Twig variable. Use `shopware.showStagingBanner` instead.
* Deprecated the usage of the header and footer properties of page Twig objects outside the dedicated header and footer templates. Use the following alternatives instead:
  * `context.currency` instead of `page.header.activeCurrency`
  * `shopware.navigation.id` instead of `page.header.navigation.active.id`
  * `shopware.navigation.pathIdList` instead of `page.header.navigation.active.path`
  * `context.saleschannel.languages.first` instead of `page.header.activeLanguage`
* Added new optional parameter `serviceMenu` of type /Shopware/Core/Content/Category/CategoryCollection to /Shopware/Storefront/Pagelet/Footer/FooterPagelet. It will be required in the next major version.

### Introduce Edge Side Includes (ESI) for header and footer

With the next major version, the header and footer will be loaded via ESI. Due to this change, many things were deprecated and will be removed with the next major version, as they are not needed anymore (Please refer to the [changelog](https://github.com/shopware/shopware/blob/v6.6.10.0/CHANGELOG.md) for a detailed list of associated deprecations).

* This changes are currently behind the `cache_rework` flag.
* The header and footer are now loaded via ESI. This allows to cache the header and footer separately from the rest of the page.
* Two new routes `/header` and `/footer` were added to receive the rendered header and footer.
* The rendered header and footer are included into the page with the Twig function `render_esi`, which calls the previously mentioned routes.
* Two new templates `src/Storefront/Resources/views/storefront/layout/header.html.twig` and `src/Storefront/Resources/views/storefront/layout/footer.html.twig` were introduced as new entry points for the header and footer.
* Make sure to adjust your template extensions to be compatible with the new structure. The block names are still the same, so it just should be necessary to extend from the new templates.

### Removal of the asterisk next to every price

* When activating the `ACCESSIBILITY_TWEAKS` feature flag the price asterisk \* are no longer displayed next to every price. A text link for tax and shipping information is displayed instead.

### Bulk entity extension

* Deprecated EntityExtension::getDefinitionClass. It will be replaced by `EntityExtension::getEntityName`, which needs to return the entity name.

Before:

```php
<?php

namespace Examples\Extension;

use Shopware\Core\Content\Product\ProductDefinition;
use Shopware\Core\Framework\DataAbstractionLayer\EntityExtension;

class MyEntityExtension extends EntityExtension
{
    public function getDefinitionClass(): string
    { 
        return ProductDefinition::class;
    }
}
```

After:

```php
<?php

namespace Examples\Extension;

use Shopware\Core\Content\Product\ProductDefinition;
use Shopware\Core\Framework\DataAbstractionLayer\EntityExtension;

class MyEntityExtension extends EntityExtension
{
    public function getEntityName() : string
    {
        return ProductDefinition::ENTITY_NAME;
    }
}
```

### Using external URL for media's path without storing physical files

* You can now store media paths as external URLs using the admin API. This allows more flexible media management without the need to store physical files on the server.

**Example Request:**

```http
POST http://sw.test/api/media
Content-Type: application/json

{
    "id": "01934e0015bd7174b35838bbb30dc927",
    "mediaFolderId": "01934ebfc0da735d841f38e8e54fda09",
    "path": "https://test.com/photo/2024/11/30/sunflowers.jpg",
    "fileName": "sunflower",
    "mimeType": "image/jpeg"
}
```

### Add aggregate admin api

* Added generic `/api/aggregate/{entityName}` API. It is similar to already existing `/api/search/${entityName}`, but without loading entities

### Updated Menu Structure in Settings Page

* The settings page has been reorganized into groups for better usability.\
  Extension developers which extend or customize the settings menu  has to make sure that their changes are compatible with the new structure.\
  The old menu structure in the settings page is deprecated and will be removed in `v6.7.0.0`.\
  (Please refer to the [changelog](https://github.com/shopware/shopware/blob/v6.6.10.0/CHANGELOG.md) for a detailed list of associated deprecations).

## Fixed bugs

* [NEXT-40478](https://github.com/shopware/shopware/issues/6484) - Elasticsearch indexing for orders for administration is really slow
* [NEXT-40385](https://github.com/shopware/shopware/issues/6359) - No optional config fields in Shopware 6.6.9.0 in theme.json
* [NEXT-40210](https://github.com/shopware/shopware/issues/6055) - admin watcher ignores HOST & PORT env
* [NEXT-40100](https://github.com/shopware/shopware/issues/5904) - Struct clone behaviour causes errors with readonly properties
* [NEXT-40084](https://github.com/shopware/shopware/issues/5890) - item in warehouse not available when stock 0
* [NEXT-40053](https://github.com/shopware/shopware/issues/5825) - Promotion action buttons have initialization issues and send incorrect entity IDs
* [NEXT-39764](https://github.com/shopware/shopware/issues/5669) - Cloud Very long loading & crash from website with many promotion codes
* [NEXT-39718](https://github.com/shopware/shopware/issues/5629) - Restoring currency inheritance breaks advanced pricing
* [NEXT-39645](https://github.com/shopware/shopware/issues/5508) - A11y: Subscriptions - lacking descriptive page titles
* [NEXT-39643](https://github.com/shopware/shopware/issues/5506) - A11y: Employee Management - error handling on detail pages for VO

## Credits

* [null](https://github.com/null)
* [ROBJkE](https://github.com/ROBJkE)
* [Schrank](https://github.com/Schrank)
* [g-volker](https://github.com/g-volker)
* [amenk](https://github.com/amenk)
* [lacknere](https://github.com/lacknere)
* [akf-bw](https://github.com/akf-bw)
* [SpiGAndromeda](https://github.com/SpiGAndromeda)
* [aragon999](https://github.com/aragon999)
* [niklaswolf](https://github.com/niklaswolf)
* [patzick](https://github.com/patzick)
* [OliverSkroblin](https://github.com/OliverSkroblin)

Thanks to all diligent friends for helping us make Shopware better and better with each pull request!

## More resources

* [Detailed diff on Github](https://github.com/shopware/shopware/compare/v6.6.9.0...v6.6.10.0) to the former version
* [Changelog on GitHub](https://github.com/shopware/shopware/blob/v6.6.10.0/CHANGELOG.md) for this version
* [Release News on corporate blog](https://www.shopware.com/en/news/shopware-6-release-news-february-2025/)
* [Installation overview](https://developer.shopware.com/docs/guides/installation/)
* [Update from a previous installation](https://developer.shopware.com/docs/guides/installation/template.html#update-shopware)

## Get in touch

Discuss about decisions, bugs you might stumble upon, etc in our [community slack](https://shopwarecommunity.slack.com/). See you there ;)

---

---

## Release notes Shopware 6.6.10.1
**Source:** [release-notes/6.6/6.6.10.1.md](https://developer.shopware.com/release-notes/6.6/6.6.10.1.md)  
# Release notes Shopware 6.6.10.1

## Abstract

This minor release contains bug fixes two possible bugs that were discovered by the community and can affect you under certain circumstances.

## System requirements

* tested on PHP 8.2 and 8.3
* tested on MySQL 8 and MariaDB 10.11

## Fixed bugs

There are two main fixes that are the reason for this release:

* [NEXT-36780](https://issues.shopware.com/issues/NEXT-36780) | Plugin Composer install destroys Shopware (1 vote)
* [#6911](https://github.com/shopware/shopware/blob/v6.6.10.1/changelog/release-6-6-10-1/2025-02-19-fix-messenger-middleware-compiler-path.md) - Fix: MessengerMiddlewareCompilerPass

These additional bug fixes are included in the release as well:

* [#6919](https://github.com/shopware/shopware/blob/v6.6.10.1/changelog/release-6-6-10-1/2025-02-19-fix-commercial-update.md) - Fix: Commercial Update
* [#6912](https://github.com/shopware/shopware/issues/6912) - Fix: require with minimum-stability stable
* [#6936](https://github.com/shopware/shopware/issues/6936) - Fix: Class SwTwigFunction not found exception
* [#6949](https://github.com/shopware/shopware/issues/6949) - Fix: Bulk edit for variants

## More resources

* [Detailed diff on Github](https://github.com/shopware/shopware/compare/v6.6.10.0...v6.6.10.1) to the former version
* [Changelog on GitHub](https://github.com/shopware/shopware/blob/v6.6.10.1/CHANGELOG.md) for this version.
* [Installation overview](https://developer.shopware.com/docs/guides/installation/)
* [Update from a previous installation](https://developer.shopware.com/docs/guides/installation/template.html#update-shopware)

## Get in touch

Discuss about decisions, bugs you might stumble upon, etc in our [community slack](https://slack.shopware.com). See you there ;)

---

---

## Release notes Shopware 6.6.10.10
**Source:** [release-notes/6.6/6.6.10.10.md](https://developer.shopware.com/release-notes/6.6/6.6.10.10.md)  
# Release notes Shopware 6.6.10.10

## Abstract

This patch release contains the fix for a security issue. Please update to this patch release as soon as possible. If you cannot update immediately, it is highly recommended to use the [Security Plugin](https://store.shopware.com/en/swag136939272659f/shopware-6-security-plugin.html).

## System requirements

* tested on PHP 8.2 and 8.4
* tested on MySQL 8 and MariaDB 11

## Improvements

(No notable improvements in this patch release)

## Fixed bugs

* [GHSA-6w82-v552-wjw2](https://github.com/shopware/shopware/security/advisories/GHSA-6w82-v552-wjw2) Reflected XSS in Storefront Login Page

## Credits

Thanks to all diligent friends for helping us make Shopware better and better with each pull request!

## More resources

* [Detailed diff on Github](https://github.com/shopware/shopware/compare/v6.6.10.9...v6.6.10.10) to the former version
* [Installation overview](https://developer.shopware.com/docs/guides/installation/)
* [Update from a previous installation](https://developer.shopware.com/docs/guides/installation/template.html#update-shopware)

## Get in touch

Discuss about decisions, bugs you might stumble upon, etc in our [community discord](https://chat.shopware.com). See you there ;)

---

---

## Release notes Shopware 6.6.10.11
**Source:** [release-notes/6.6/6.6.10.11.md](https://developer.shopware.com/release-notes/6.6/6.6.10.11.md)  
# Release notes Shopware 6.6.10.11

## Abstract

This is a maintenance patch for Shopware 6.6. It primarily delivers several bug fixes and introduces a small number of new features to improve stability and developer experience.

## System requirements

* tested on PHP 8.2 and 8.4
* tested on MySQL 8 and MariaDB 11

## Improvements

(No notable improvements in this patch release)

## Fixed bugs

* [#14332 - Performance improvement for category denormalizer](./changelog/release-6-6-10-11/2026-01-14-category-denormalizer-performance-improvement.md)
* [#6912 - fix: require with minimum-stability stable (fixes: #6912) (#6914)](https://github.com/shopware/shopware/issues/6912)
* [#6960 - ci: skip downstreams in case of no write perms (fixes: #6960) (#6985)](https://github.com/shopware/shopware/issues/6960)
* [#9031 - ci: reenable 6.6.0.0 update (fixes #9031)\[6.6.x\]  (#9248)](https://github.com/shopware/shopware/issues/9031)
* [#9851 - feat: implement event on Sitemap Generation, closes #9851 \[6.6.x\]  (#9968)](https://github.com/shopware/shopware/issues/9851)
* [#12859 - Fix captcha validation to respect errorRoute parameter](./changelog/release-6-6-10-11/2025-10-23-fix-captcha-error-route-parameter.md)
* [#13179 - Slash and backslash are now working correctly in search if configured as preserved characters](./changelog/release-6-6-10-11/2025-10-26-special-characters-in-search-not-working-even-when-added-as-preserved-characters-in-config-file.md)
* [#13707 - Generate EXISTS conditions instead of left joins for nested filter groups in DAL criteria builder](./changelog/release-6-6-10-11/2026-01-14-multi-join-exists.md)
* [#8577 - Cheapest price of variant product applies across sales channels](./changelog/release-6-6-10-11/2025-10-27-cheapest-price-of-variant-product-applies-across-sales-channels.md)

## Credits

Thanks to all diligent friends for helping us make Shopware better and better with each pull request!

## More resources

* [Detailed diff on Github](https://github.com/shopware/shopware/compare/v6.6.10.10...v6.6.10.11) to the former version
* [Installation overview](https://developer.shopware.com/docs/guides/installation/)
* [Update from a previous installation](https://developer.shopware.com/docs/guides/installation/template.html#update-shopware)

## Get in touch

Discuss about decisions, bugs you might stumble upon, etc in our [community discord](https://chat.shopware.com). See you there ;)

---

---

## Release notes Shopware 6.6.10.12
**Source:** [release-notes/6.6/6.6.10.12.md](https://developer.shopware.com/release-notes/6.6/6.6.10.12.md)  
# Release notes Shopware 6.6.10.12

## Abstract

This is a maintenance patch for Shopware 6.6. It primarily delivers several bug fixes.

## System requirements

* tested on PHP 8.2 and 8.4
* tested on MySQL 8 and MariaDB 11

## Improvements

(No notable improvements in this patch release)

## Fixed bugs

* [#14353 - fix: Remove usage of deprecated PDO constants (backport: 6.6.x) (#14353)](https://github.com/shopware/shopware/pull/14353)
* [#14451 - Fix IAP decoding with old OpenSSL versions](./changelog/release-6-6-10-12/2025-10-20-fix-iap-decoding-with-old-openssl-versions.md)
* [#14413 - fix: keep mail attachments across flow actions (backport: 6.6.x) (#14443)](https://github.com/shopware/shopware/issues/14413)
* [#14058 - fix: Never load unfiltered many-to-many (backport: 6.6.x) (#14438)](https://github.com/shopware/shopware/issues/14058)
* [#14475 - fix: attribute entities missing with auto configuration (backport: 6.6.x) (#14475)](https://github.com/shopware/shopware/pull/14475)
* [#14482 - feat: Update PHPStan and its Symfony plugin (#14482)](https://github.com/shopware/shopware/pull/14482)
* [#13968 - Symfony 7.4 Update](./changelog/release-6-6-10-12/2026-01-23-symfony-7-4.md)
* [#14289 - fix: allow bulk edit stock with negative value (backport: 6.6.x) (#14392)](https://github.com/shopware/shopware/issues/14289)
* [#14485 - fix: ProductListingLoader shows random product variant instead of the main variant - backport 6.6.x (#14485)](https://github.com/shopware/shopware/pull/14485)
* [#11733 - fix: Error when inserting tables in custom field (backport: 6.6.x) (#14537)](https://github.com/shopware/shopware/issues/11733)
* [#14633 - fix: document footer placement (backport: 6.6.x) (#14633)](https://github.com/shopware/shopware/pull/14633)

## Credits

Thanks to all diligent friends for helping us make Shopware better and better with each pull request!

## More resources

* [Detailed diff on Github](https://github.com/shopware/shopware/compare/v6.6.10.11...v6.6.10.12) to the former version
* [Installation overview](https://developer.shopware.com/docs/guides/installation/)
* [Update from a previous installation](https://developer.shopware.com/docs/guides/installation/template.html#update-shopware)

## Get in touch

Discuss about decisions, bugs you might stumble upon, etc in our [community discord](https://chat.shopware.com). See you there ;)

---

---

## Release notes Shopware 6.6.10.13
**Source:** [release-notes/6.6/6.6.10.13.md](https://developer.shopware.com/release-notes/6.6/6.6.10.13.md)  
# Release notes Shopware 6.6.10.13

## Abstract

This is a maintenance patch for Shopware 6.6. It fixes two bugs.

## System requirements

* tested on PHP 8.2 and 8.4
* tested on MySQL 8 and MariaDB 11

## Improvements

(No notable improvements in this patch release)

## Fixed bugs

* [#14738 - fix: `getAddress` in`AddressDetailPageLoader` (backport: 6.6.x) (#14738)](https://github.com/shopware/shopware/pull/14738)
* [#14735 - fix: order edit loading (backport: 6.6.x) (#14747)](https://github.com/shopware/shopware/issues/14735)

## Credits

Thanks to all diligent friends for helping us make Shopware better and better with each pull request!

## More resources

* [Detailed diff on Github](https://github.com/shopware/shopware/compare/v6.6.10.12...v6.6.10.13) to the former version
* [Installation overview](https://developer.shopware.com/docs/guides/installation/)
* [Update from a previous installation](https://developer.shopware.com/docs/guides/installation/template.html#update-shopware)

## Get in touch

Discuss about decisions, bugs you might stumble upon, etc in our [community discord](https://chat.shopware.com). See you there ;)

---

---

## Release notes Shopware 6.6.10.2
**Source:** [release-notes/6.6/6.6.10.2.md](https://developer.shopware.com/release-notes/6.6/6.6.10.2.md)  
# Release notes Shopware 6.6.10.2

## Abstract

This minor release contains bug fixes.

## System requirements

* tested on PHP 8.2 and 8.3
* tested on MySQL 8 and MariaDB 10.11

## Fixed bugs

* [PR-7132:](https://github.com/shopware/shopware/pull/7132) With https://github.com/symfony/symfony/pull/59781, the definition *mailer.default\_transport* was removed and set as a simple alias. Therefore it could not be accessed anymore in a compiler pass. But this should also be not necessary anymore.
* [PR-7121:](https://github.com/shopware/shopware/pull/7121) In languages, which use Apostrophes a lot (like French), the storefront broke because escaping was missing.
* [PR-7222](https://github.com/shopware/shopware/pull/7222) Show update button for plugins located in "custom/plugins" directory, which make use of the composer installation functionality
* [PR-7158](https://github.com/shopware/shopware/pull/7158) Double form submit from reCaptcha plugin
* [PR-7257](https://github.com/shopware/shopware/pull/7257) Only use button modal triggers behind accessibility flag

## More resources

* [Detailed diff on Github](https://github.com/shopware/shopware/compare/v6.6.10.1...v6.6.10.2) to the former version
* [Changelog on GitHub](https://github.com/shopware/shopware/blob/v6.6.10.2/CHANGELOG.md) for this version.
* [Installation overview](https://developer.shopware.com/docs/guides/installation/)
* [Update from a previous installation](https://developer.shopware.com/docs/guides/installation/template.html#update-shopware)

## Get in touch

Discuss about decisions, bugs you might stumble upon, etc in our [community slack](https://slack.shopware.com). See you there ;)

---

---

## Release notes Shopware 6.6.10.3
**Source:** [release-notes/6.6/6.6.10.3.md](https://developer.shopware.com/release-notes/6.6/6.6.10.3.md)  
# Release notes Shopware 6.6.10.3

## Abstract

This patch release contains **security fixes**. It is recommended to update your system as soon as possible!

## System requirements

* tested on PHP 8.2 and 8.3
* tested on MySQL 8 and MariaDB 10.11

## Fixed bugs

* [Blind SQL-injection in DAL aggregations](https://github.com/shopware/shopware/security/advisories/GHSA-8g35-7rmw-7f59)
* [Broken ACL on Document retrieval to access other customers documents](https://github.com/shopware/shopware/security/advisories/GHSA-68wv-g3fw-pq7q)
* [Denial Of Service via password length](https://github.com/shopware/shopware/security/advisories/GHSA-cgfj-hj93-rmh2)
* [Check for registered accounts through the store-api](https://github.com/shopware/shopware/security/advisories/GHSA-hh7j-6x3q-f52h)
* [Default newsletter opt-in settings allow for mass sign-up abuse](https://github.com/shopware/shopware/security/advisories/GHSA-4h9w-7vfp-px8m)

## More resources

* [Detailed diff on Github](https://github.com/shopware/shopware/compare/v6.6.10.2...v6.6.10.3) to the former version
* [Changelog on GitHub](https://github.com/shopware/shopware/blob/v6.6.10.3/CHANGELOG.md) for this version.
* [Installation overview](https://developer.shopware.com/docs/guides/installation/)
* [Update from a previous installation](https://developer.shopware.com/docs/guides/installation/template.html#update-shopware)

## Get in touch

Discuss about decisions, bugs you might stumble upon, etc in our [community slack](https://slack.shopware.com). See you there ;)

---

---

## Release notes Shopware 6.6.10.4
**Source:** [release-notes/6.6/6.6.10.4.md](https://developer.shopware.com/release-notes/6.6/6.6.10.4.md)  
# Release notes Shopware 6.6.10.4

## Abstract

This patch release contains quite a list of different improvements plus 12 bug fixes.

## System requirements

* tested on PHP 8.2 and 8.4
* tested on MySQL 8 and MariaDB 11

## Improvements

### Possibility to create private or internal custom fields

We introduce a new value for the custom\_field entity, which will allow a developer/shop owner to exclude a custom field from the API. This is useful for custom fields that are only used internally and should not be exposed to the API.

### Confirmation modal to save changes in the order administration

When managing an order and make changes (such as adding a tracking code) and update the order's status without saving, a confirmation pop-up will now ask if you'd like to save your changes first. This ensures that your updates are applied correctly before moving forward, preventing issues with outdated information being used.

### Orders edited in Admin now use the correct customer address for recalculation

When editing customer addresses for orders, the system chose the customer's default instead of the one the order was placed with. This has now been resolved, ensuring that the system always uses the correct customer address during order recalculations.

### Improved Card Component Identification in Order Details

The card component in the order details page has been improved to ensure that it is correctly identified. This enhancement is particularly beneficial for third-party developers who rely on accurate identification of components for their integrations and customizations.

### Improved Email Previews for order data

Email previews now use real order data instead of sample data when displaying order information. For shop owners, this means you will see accurate, live order details in email previews, making it easier to verify the content before sending emails to customers.

### New Possibilities for Extension Developers: Configurable Response Headers

This feature allows developers to modify response headers through app scripts to e.g. change CSP or XFramOptions headers.

### Enhanced Search Widget Accessibility for Better User Experience

The search widget in the storefront has been improved to be more accessible. This includes better keyboard navigation and screen reader support, ensuring that all users can easily interact with the search functionality.

### Improved promotion management for orders

Since the introduction of the ability to edit promotions after an order has been placed, promotions are always re-evaluated when an order is recalculated (e.g. by edit a line item). Now, when a recalculation is triggered, a modal shows all changes resulting from the recalculation. You can decide whether these changes should be adopted or not.

## Fixed bugs

* [#4450](https://github.com/shopware/shopware/issues/4450) – OffCanvasSingleton does not remove hard-coded offcanvas from DOM
* [#4654](https://github.com/shopware/shopware/issues/4654) – Fix HTML quirks mode in the Storefront
* [#6675](https://github.com/shopware/shopware/issues/8207) – Fix elasticsearch indexing performance for orders in administration
* [#7131](https://github.com/shopware/shopware/issues/7131) – Fixed bulk edit custom fields
* [#7624](https://github.com/shopware/shopware/issues/7624) – Improve cookie settings accessibility
* [#7697](https://github.com/shopware/shopware/issues/7697) – Fix double triggering of switch field update:value
* [#8234](https://github.com/shopware/shopware/issues/8875) – Fix loading of to-one associations with partial data loading
* [#8333](https://github.com/shopware/shopware/issues/8333) – Fixed calls to update extensions
* [#5328](https://github.com/shopware/shopware/issues/5328) – Fix DAL inherited to-many field reads with limits
* [#7858](https://github.com/shopware/shopware/issues/7858) – Fix webhook dispatching for not versioned events
* [#7228](https://github.com/shopware/shopware/issues/7228) – Added missing rule filter for shipping price matrix
* [#7350](https://github.com/shopware/shopware/issues/7350) – Show new customer address after saving admin modal

## Credits

* [niklaswolf](https://github.com/niklaswolf)
* [akf-bw](https://github.com/akf-bw)
* [jmatthiesen81](https://github.com/jmatthiesen81)
* [lacknere](https://github.com/lacknere)
* [aragon999](https://github.com/aragon999)
* [nguyenquocdaile](https://github.com/nguyenquocdaile)
* [pascalniklaspaul](https://github.com/pascalniklaspaul)
* [MelvinAchterhuis](https://github.com/MelvinAchterhuis)
* [Fayti1703](https://github.com/Fayti1703)
* [schneider-felix](https://github.com/schneider-felix)

Thanks to all diligent friends for helping us make Shopware better and better with each pull request!

## More resources

* [Detailed diff on Github](https://github.com/shopware/shopware/compare/v6.6.10.3...v6.6.10.4) to the former version
* [Changelog on GitHub](https://github.com/shopware/shopware/blob/v6.6.10.4/CHANGELOG.md) for this version.
* [Installation overview](https://developer.shopware.com/docs/guides/installation/)
* [Update from a previous installation](https://developer.shopware.com/docs/guides/installation/template.html#update-shopware)

## Get in touch

Discuss about decisions, bugs you might stumble upon, etc in our [community slack](https://slack.shopware.com). See you there ;)

---

---

## Release notes Shopware 6.6.10.5
**Source:** [release-notes/6.6/6.6.10.5.md](https://developer.shopware.com/release-notes/6.6/6.6.10.5.md)  
# Release notes Shopware 6.6.10.5

## Abstract

This patch release contains different bug fixes.

## System requirements

* tested on PHP 8.2 and 8.4
* tested on MySQL 8 and MariaDB 11

## Improvements

(No notable improvements listed in v6.6.10.5)

## Fixed bugs

* Fixed an issue where the Shopware\Core\Framework\DataAbstractionLayer\Search\Criteria could cause incorrect SQL queries under certain conditions.
* Resolved a bug in the administration UI where custom entity listings would not properly refresh after updates.
* Fixed a caching issue that could lead to stale data being displayed in storefront product listings.
* Addressed a rare race condition in order processing that could lead to duplicate order numbers.
* Fixed a bug where certain plugin migrations would fail when executed in bulk.

## Credits

* [@OliverSkroblin](https://github.com/OliverSkroblin)
* [@akf-bw](https://github.com/akf-bw)
* [@MelvinAchterhuis](https://github.com/MelvinAchterhuis)
* [raffaelecarelle](https://github.com/raffaelecarelle)
* [aragon999](https://github.com/aragon999)
* [amenk](https://github.com/amenk)
* [wrongspot](https://github.com/wrongspot)

Thanks to all diligent friends for helping us make Shopware better and better with each pull request!

## More resources

* [Detailed diff on Github](https://github.com/shopware/shopware/compare/v6.6.10.4...v6.6.10.5) to the former version
* [Changelog on GitHub](https://github.com/shopware/shopware/blob/v6.6.10.5/CHANGELOG.md) for this version.
* [Installation overview](https://developer.shopware.com/docs/guides/installation/)
* [Update from a previous installation](https://developer.shopware.com/docs/guides/installation/template.html#update-shopware)

## Get in touch

Discuss about decisions, bugs you might stumble upon, etc in our [community slack](https://slack.shopware.com). See you there ;)

---

---

## Release notes Shopware 6.6.10.6
**Source:** [release-notes/6.6/6.6.10.6.md](https://developer.shopware.com/release-notes/6.6/6.6.10.6.md)  
# Release notes Shopware 6.6.10.6

## Abstract

This patch release contains several bug fixes.

## System requirements

* tested on PHP 8.2, 8.3 and 8.4
* tested on MySQL 8 and MariaDB 11

## Improvements

(No notable improvements listed in v6.6.10.6)

## Fixed bugs

* [#8724](https://github.com/shopware/shopware/issues/8724) - Added locking to cart mutating routes
* [#10763](https://github.com/shopware/shopware/issues/10763) - fix: remove 6.8.0.0 feature flag
* [#10146](https://github.com/shopware/shopware/issues/10146) - Filter cart success error messages

::: details Click to see more fixed bugs

* [#10457](https://github.com/shopware/shopware/issues/10457) - Improve ES search scoring for numeric tokens
* [#10518](https://github.com/shopware/shopware/issues/10518) - Press ESC key in the modal will go back listing page
* [#10682](https://github.com/shopware/shopware/issues/10682) - Live search page broken if the data is empty
* [#10696](https://github.com/shopware/shopware/issues/10696) - Respect missing shipping method currency prices
* [#10738](https://github.com/shopware/shopware/issues/10738) - Fix apps with duplicated custom field sets
* [#10774](https://github.com/shopware/shopware/issues/10774) - Multiple promotions order count fix
* [#10853](https://github.com/shopware/shopware/issues/10853) - Skip In-App Purchases update task on missing authentication headers
* [#10900](https://github.com/shopware/shopware/issues/10900) - Add new data id to set off-canvas aria-labelledby
* [#10919](https://github.com/shopware/shopware/issues/10919) - Delete correct expired store session
* [#11016](https://github.com/shopware/shopware/issues/11016) - Change URL generation for ESI includes to avoid HTTPS issues with Varnish @stefanpoensgen
* [#11092](https://github.com/shopware/shopware/issues/11092) - Fix variant listing config when cloning products or deleting variants @schneider-felix
* [#8228](https://github.com/shopware/shopware/issues/8228) - Allow empty alt with sw\_thumbnails
* [#8591](https://github.com/shopware/shopware/issues/8591) - Fixed theme config inheritance for database child themes
* [#9229](https://github.com/shopware/shopware/issues/9229) - Fix the reading of the cart widget by screen readers
* [#9310](https://github.com/shopware/shopware/issues/9310) - E-invoice vertical tax calculation
* [#10513](https://github.com/shopware/shopware/issues/10513) - Fix issue SEO url not generating anymore
* [#10906](https://github.com/shopware/shopware/issues/10906) - Change path of header and footer routes
* [#8471](https://github.com/shopware/shopware/issues/8471) - ES should work correctly with ScoreQuery
* [#9367](https://github.com/shopware/shopware/issues/9367) - Fix alignment logo manufacturer media field not correct
* [#11106](https://github.com/shopware/shopware/issues/11106) - Fix Quote counts up the order number range

:::

## Credits

* [Stefan Poensgen](https://github.com/stefanpoensgen)
* [Felix Schneider](https://github.com/schneider-felix)

Thanks to all diligent friends for helping us make Shopware better and better with each pull request!

## More resources

* [Detailed diff on Github](https://github.com/shopware/shopware/compare/v6.6.10.5...v6.6.10.6) to the former version
* [Changelog on GitHub](https://github.com/shopware/shopware/blob/v6.6.10.6/CHANGELOG.md) for this version.
* [Installation overview](https://developer.shopware.com/docs/guides/installation/)
* [Update from a previous installation](https://developer.shopware.com/docs/guides/installation/template.html#update-shopware)

## Get in touch

Discuss about decisions, bugs you might stumble upon, etc in our [community discord](https://chat.shopware.com). See you there ;)

---

---

## Release notes Shopware 6.6.10.7
**Source:** [release-notes/6.6/6.6.10.7.md](https://developer.shopware.com/release-notes/6.6/6.6.10.7.md)  
# Release notes Shopware 6.6.10.7

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

* [6912](https://github.com/shopware/shopware/issues/6912) `composer require shopware/platform:6.6.10.0` requires minimum-stability dev
* [6960](https://github.com/shopware/shopware/issues/6960) Skip downstreams for external contributors
* [9031](https://github.com/shopware/shopware/issues/9031) Fix 6.6.0.0 ATS update test
* [9851](https://github.com/shopware/shopware/issues/9851) Missing Event to exclude Domains from Sitemap Generation

## Credits

Thanks to all diligent friends for helping us make Shopware better and better with each pull request!

## More resources

* [Detailed diff on Github](https://github.com/shopware/shopware/compare/v6.6.10.6...v6.6.10.7) to the former version
* [Changelog on GitHub](https://github.com/shopware/shopware/blob/v6.6.10.7/CHANGELOG.md) for this version.
* [Installation overview](https://developer.shopware.com/docs/guides/installation/)
* [Update from a previous installation](https://developer.shopware.com/docs/guides/installation/template.html#update-shopware)

## Get in touch

Discuss about decisions, bugs you might stumble upon, etc in our [community discord](https://chat.shopware.com). See you there ;)

---

---

