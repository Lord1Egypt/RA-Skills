# RELEASE AND UPGRADES

Compiled excerpts from the Shopware Developer Documentation snapshot. Prefer live docs at [developer.shopware.com](https://developer.shopware.com/) when in doubt.

---

## Release notes Shopware 6.6.10.8
**Source:** [release-notes/6.6/6.6.10.8.md](https://developer.shopware.com/release-notes/6.6/6.6.10.8.md)  
# Release notes Shopware 6.6.10.8

## Abstract

This patch release contains 40+ bug fixes.

## System requirements

* tested on PHP 8.2 and 8.4
* tested on MySQL 8 and MariaDB 11

## Improvements

(No notable improvements in this patch release)

## Fixed bugs

* [#11055](https://github.com/shopware/shopware/issues/11055) \<blockquote> tags in product description are not rendered as quotes in the storefront
* [#11215](https://github.com/shopware/shopware/issues/11215) Missing ResetInterface handling in Shopware Kernel (affects FrankenPHP and long‑running processes)
* [#11484](https://github.com/shopware/shopware/issues/11484) fix: don’t check for canonical SEO Urls when no path info given during SEO URL creation (backport: 6.6.x)

::: details Click to see more fixed bugs

* [#11580](https://github.com/shopware/shopware/issues/11580) feat: Add missing changelogs for Symfony update and MySQL min version increase (backport: 6.6.x)
* [#11766](https://github.com/shopware/shopware/issues/11766) Theme config fields of type ‘bool’ or ‘switch’ fall back to their default base\_config values when disabled
* [#11803](https://github.com/shopware/shopware/issues/11803) fix: advanced prices for fixed item price discount (backport: 6.6.x)
* [#11823](https://github.com/shopware/shopware/issues/11823) OOM when opening product detail page in admin with many properties
* [#11830](https://github.com/shopware/shopware/issues/11830) fix: line item tax display with tax providers (backport: 6.6.x)
* [#11838](https://github.com/shopware/shopware/issues/11838) fix: recursive usage of CartLocker (backport: 6.6.x)
* [#11839](https://github.com/shopware/shopware/issues/11839) fix: duplicate address display in sw-order-detail (backport: 6.6.x)
* [#11855](https://github.com/shopware/shopware/issues/11855) Composer plugins can not be removed from the system
* [#11967](https://github.com/shopware/shopware/issues/11967) fix: Adjust product zoom window size (backport: 6.6.x)
* [#12029](https://github.com/shopware/shopware/issues/12029) Custom field with a name from a foreign key of the entity results in write error on save
* [#12209](https://github.com/shopware/shopware/issues/12209) feat: Add docx file extension (backport: 6.6.x)
* [#12225](https://github.com/shopware/shopware/issues/12225) fix: document content wrapping (backport)
* [#12464](https://github.com/shopware/shopware/issues/12464) fix: initialization of DiscountCampaignStruct, add additional properties (backport: 6.6.x)
* [#12756](https://github.com/shopware/shopware/issues/12756) HTTP Cache Poisoning by removing or manipulating sw‑states and sw‑cache‑hash cookies
* [#7156](https://github.com/shopware/shopware/issues/7156) Proxy Store API can not be accessed due to Admin API sales channel source being blocked
* [#7238](https://github.com/shopware/shopware/issues/7238) Allow add parameters to SwitchContextEvent
* [#10707](https://github.com/shopware/shopware/issues/10707) \[ElasticSearch] Datetime format
* [#11001](https://github.com/shopware/shopware/issues/11001) Show match in search, not preview product
* [#11074](https://github.com/shopware/shopware/issues/11074) Search for “document number” doesn’t return any results if SHOPWARE\_ADMIN\_ES\_ENABLED=1 is set
* [#11097](https://github.com/shopware/shopware/issues/11097) Wrong customer context on login if entry from sales\_channel\_api\_context is expired
* [#11528](https://github.com/shopware/shopware/issues/11528) Problems patching products / Non‑backed enums have no default serialization
* [#11550](https://github.com/shopware/shopware/issues/11550) fix: inconsistent seoUrls for cross‑selling products
* [#11619](https://github.com/shopware/shopware/issues/11619) SeoUrl generate database‑error when the url changes
* [#11654](https://github.com/shopware/shopware/issues/11654) fix: document squished line item listing
* [#11800](https://github.com/shopware/shopware/issues/11800) Can not override the products assigned into a cms slider
* [#8018](https://github.com/shopware/shopware/issues/8018) Set Minimal search term length <> 3
* [#8584](https://github.com/shopware/shopware/issues/8584) Error when trying to remove “Main category” for product
* [#12979](https://github.com/shopware/shopware/issues/12979) feat: compatibility with OpenSearch 3.x

:::

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

## Release notes Shopware 6.6.10.9
**Source:** [release-notes/6.6/6.6.10.9.md](https://developer.shopware.com/release-notes/6.6/6.6.10.9.md)  
# Release notes Shopware 6.6.10.9

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

* [Detailed diff on Github](https://github.com/shopware/shopware/compare/v6.6.10.8...v6.6.10.9) to the former version
* [Changelog on GitHub](https://github.com/shopware/shopware/blob/v6.6.10.9/CHANGELOG.md) for this version.
* [Installation overview](https://developer.shopware.com/docs/guides/installation/)
* [Update from a previous installation](https://developer.shopware.com/docs/guides/installation/template.html#update-shopware)

## Get in touch

Discuss about decisions, bugs you might stumble upon, etc in our [community discord](https://chat.shopware.com). See you there ;)

---

---

## Release notes Shopware 6.6.2.0
**Source:** [release-notes/6.6/6.6.2.0.md](https://developer.shopware.com/release-notes/6.6/6.6.2.0.md)  
# Release notes Shopware 6.6.2.0

## Abstract

Besides a list of 44 bug fixes, this minor release contains some cool improvements, especially for developers, for example typescript support for extensions, automatic compiling of JS/SCSS of plugin sub-bundles, meteor component library in administration etc.

## System requirements

* tested on PHP 8.2 and 8.3
* tested on MySQL 8 and MariaDB 10.11

## Improvements

### Typescript support for webpack config in extensions

Extensions can now use typescript (.ts and .cts) files for their webpack configuration.

### JavaScript/SCSS of plugin sub-bundles now automatically compiles during the plugin activation/deactivation

* When a plugin is registering additional sub-bundles `\Shopware\Core\Framework\Plugin::getAdditionalBundles`, those bundles can also bring their own JavaScript/CSS. Previously, the JavaScript/CSS of sub-bundles was not automatically detected and re-compiled after the plugin was activated or deactivated. Now Shopware also detects JavaScript of sub-bundles and automatically executes `theme:compile` after plugin activation/deactivation.

### Added meteor component library to the administration

The [Meteor component library](https://shopware.design/meteor-components/) was added as a new dependecy to the administration. All library components are now also directly available in the administration.

### Sync option for CLI theme commands

The `theme:compile` and `theme:change ` command now accept `--sync` option to compile themes synchronously. The `--sync` option is useful for CI/CD pipelines when at runtime, themes should be compiled async, but during the build process you want sync generation.

### Improved License Key Handling and Error Reporting in Shopware

* Instead of breaking the Shop, an incorrect license domain is now logged and treated as if no license exists. This eliminates the need for manual system\_config changes and cache clearing.
* Shopware now provides a 5-minute leeway for license key issuance and expiry to accommodate system time discrepancies. If the time discrepancy exceeds 5 minutes, a proper exception is now thrown.
* Introduced a new command for showing License information: `commercial:license:info`.

### Order Approval improvements

The order approval got improved with a new UI to create approval rules. Additional the approval rules can now be extended with custom rules. Lastly, the payment authorization can now be automated with the Flow Builder.

## Fixed bugs

* [NEXT-26060](https://issues.shopware.com/issues/NEXT-26060) | PDP Image zoom modal: 'esc'-press does not close the modal (20 votes)
* [NEXT-34643](https://issues.shopware.com/issues/NEXT-34643) | Theme compile fails if theme is installed via composer (6 votes)
* [NEXT-33594](https://issues.shopware.com/issues/NEXT-33594) | Under orders in the customer account, the total amount is always displayed as gross. (5 votes)
* [NEXT-34348](https://issues.shopware.com/issues/NEXT-34348) | (SwagCommercial) Customer email validation never gets called if EMPLOYEE\_MANAGEMENT (4 votes)
* [NEXT-34338](https://issues.shopware.com/issues/NEXT-34338) | Incorrect variant display when using a product slider (shopping experience) (4 votes)
* [NEXT-33636](https://issues.shopware.com/issues/NEXT-33636) | Mailing different documents in the same flow will compound documents in later actions (4 votes)
* [NEXT-35548](https://issues.shopware.com/issues/NEXT-35548) | Wrong Rulebuilder naming for "Number of submitted reviews" (3 votes)
* [NEXT-34797](https://issues.shopware.com/issues/NEXT-34797) | Checkout Sweetner not working when it´s a subdomain (2 votes)
* [NEXT-34315](https://issues.shopware.com/issues/NEXT-34315) | Snippet generation fails with SNIPPET\_\_DUPLICATED\_FIRST\_LEVEL\_KEY if a plugin used an App first level key (2 votes)
* [NEXT-35103](https://issues.shopware.com/issues/NEXT-35103) | Image Slider preview broken in administration shopping experiences (1 votes)
* [NEXT-34914](https://issues.shopware.com/issues/NEXT-34914) | Form validation does not work with activated captcha (1 votes)
* [NEXT-34644](https://issues.shopware.com/issues/NEXT-34644) | Problem with this.$super in component override (1 votes)
* [NEXT-29590](https://issues.shopware.com/issues/NEXT-29590) | Wishlist's icon size value has no effect (1 votes)
* [NEXT-35785](https://issues.shopware.com/issues/NEXT-35785) | \[Github] NEXT-00000 - Changed media partial loaded event name (0 votes)
* [NEXT-35665](https://issues.shopware.com/issues/NEXT-35665) | \[Github] fix: Correct display of long names of child items in administration order (0 votes)
* [NEXT-35581](https://issues.shopware.com/issues/NEXT-35581) | \[Github] NEXT-00000 - Fix multicolor icons (0 votes)
* [NEXT-35577](https://issues.shopware.com/issues/NEXT-35577) | \[Github] Fix Typo in PluginBaseClassNotFoundException (0 votes)
* [NEXT-35502](https://issues.shopware.com/issues/NEXT-35502) | \[Github] NEXT-00000 - Fix migration saleschannel test (0 votes)
* [NEXT-35443](https://issues.shopware.com/issues/NEXT-35443) | \[Github] NEXT-00000 - Fix / update github pipelines (0 votes)
* [NEXT-35345](https://issues.shopware.com/issues/NEXT-35345) | Create an already existing account, results in an error page (0 votes)
* [NEXT-35318](https://issues.shopware.com/issues/NEXT-35318) | \[Github] Add heading elements for account login page to improve accessibility & SEO (0 votes)
* [NEXT-35283](https://issues.shopware.com/issues/NEXT-35283) | Deleting the custom fields when uninstalling the private APP (0 votes)
* [NEXT-35209](https://issues.shopware.com/issues/NEXT-35209) | \[ADMIN] text copyable option missused (0 votes)
* [NEXT-35126](https://issues.shopware.com/issues/NEXT-35126) | Media path update command, iterator not working (0 votes)
* [NEXT-35041](https://issues.shopware.com/issues/NEXT-35041) | \[Github] NEXT-00000 - Improve storefront webpack watch twig (0 votes)
* [NEXT-35016](https://issues.shopware.com/issues/NEXT-35016) | Umlauts in promotion code field not working (0 votes)
* [NEXT-34980](https://issues.shopware.com/issues/NEXT-34980) | \[Github] Fix Missing Document Settings Modal Template prevent creation of cust… (0 votes)
* [NEXT-34960](https://issues.shopware.com/issues/NEXT-34960) | \[Github] NEXT-34825 - Changed return value to array if object is empty (0 votes)
* [NEXT-34924](https://issues.shopware.com/issues/NEXT-34924) | \[Github]Fix installer fr translation file (0 votes)
* [NEXT-34923](https://issues.shopware.com/issues/NEXT-34923) | \[Github] Strip prefix from redis keys in redis incrementer (0 votes)
* [NEXT-34922](https://issues.shopware.com/issues/NEXT-34922) | \[Github] NEXT-00000 - Fix profiler table & icons (0 votes)
* [NEXT-34921](https://issues.shopware.com/issues/NEXT-34921) | \[Github]NEXT-34904 - chore: Add native array return type to all event subscribers getSubscribedEvents (0 votes)
* [NEXT-34826](https://issues.shopware.com/issues/NEXT-34826) | \[Github] NEXT-00000 - Add MediaHydrator & Update EntityHydrator (0 votes)
* [NEXT-34801](https://issues.shopware.com/issues/NEXT-34801) | \[Github] keep element keys when sortByPositions (0 votes)
* [NEXT-34798](https://issues.shopware.com/issues/NEXT-34798) | Missing backdrop in address modal in checkout (0 votes)
* [NEXT-34787](https://issues.shopware.com/issues/NEXT-34787) | \[Github] Update customer view and show correct saleschannel info (0 votes)
* [NEXT-34785](https://issues.shopware.com/issues/NEXT-34785) | \[Github] chore: Add `gad_source` parameter to ignored http cache parameters (0 votes)
* [NEXT-34781](https://issues.shopware.com/issues/NEXT-34781) | Flow Builder Storniert immer die Erste Rechnung anstatt die letzte erstellte (0 votes)
* [NEXT-34756](https://issues.shopware.com/issues/NEXT-34756) | \[Github] NEXT-00000 - Fix storefront webpack config entries (0 votes)
* [NEXT-34709](https://issues.shopware.com/issues/NEXT-34709) | Checkout Sweetener Availability Rule not respected in template (0 votes)
* [NEXT-34705](https://issues.shopware.com/issues/NEXT-34705) | Improve license checks in commercial (0 votes)
* [NEXT-34676](https://issues.shopware.com/issues/NEXT-34676) | \[Github] Update ProductDetailRoute.php (0 votes)
* [NEXT-34512](https://issues.shopware.com/issues/NEXT-34512) | Validation from product reviews (0 votes)
* [NEXT-34444](https://issues.shopware.com/issues/NEXT-34444) | If you create new Product comparison(feed) no sales\_channel\_language will be added. (0 votes)
* [NEXT-26889](https://issues.shopware.com/issues/NEXT-26889) | \[GitHub] fix html lang attribute (0 votes)
* [NEXT-19836](https://issues.shopware.com/issues/NEXT-19836) | Address fields are not translated in validation messages (0 votes)

## Credits

Thanks to all our contributors for helping us improve Shopware with every pull request!

* [Fabian Blechschmidt](https://github.com/Schrank)
* [Benjamin Wittwer](https://github.com/akf-bw)
* [Max](https://github.com/aragon999)
* [Joshua Behrens](https://github.com/JoshuaBehrens)
* [Stefan Richter](https://github.com/SRaromicon)
* [Justus Maier](https://github.com/justusNBB)
* [Joschka](https://github.com/tschosch51)
* [Altay Akkus](https://github.com/AltayAkkus)
* [Jesper Ingels](https://github.com/jesperingels)

## More resources

* [Detailed diff on Github](https://github.com/shopware/shopware/compare/v6.6.1.2...v6.6.2.0) to the former version
* [Changelog on GitHub](https://github.com/shopware/shopware/blob/v6.6.2.0/CHANGELOG.md) for this version.
* [Release News on corporate blog](https://www.shopware.com/en/news/shopware-6-release-news-may-2024/)
* [Installation overview](https://developer.shopware.com/docs/guides/installation/)
* [Update from a previous installation](https://developer.shopware.com/docs/guides/installation/template.html#update-shopware)

## Get in touch

Discuss about decisions, bugs you might stumble upon, etc in our [community slack](https://slack.shopware.com). See you there ;)

---

---

## Release notes Shopware 6.6.3.0
**Source:** [release-notes/6.6/6.6.3.0.md](https://developer.shopware.com/release-notes/6.6/6.6.3.0.md)  
# Release notes Shopware 6.6.3.0

## Abstract

Besides a list of 40 bug fixes, this minor release contains some cool improvements. For features, please see [Release News on corporate blog](https://www.shopware.com/en/news/shopware-6-release-news-june-2024/) which will be published in a few days.

## System requirements

* tested on PHP 8.2 and 8.3
* tested on MySQL 8 and MariaDB 10.11

## Improvements

### Entities via php attributes

Entities can now be defined using PHP attributes. This allows a more state-of-the-art and cleaner way to define entities.

* [Changes](https://github.com/shopware/shopware/commit/b0d051bebe78e64a1f889bdb432da953e987b5b1)
* [Documentation](https://github.com/shopware/docs/pull/1390)

Here a small example:

```php
<?php

#[Entity('foo')]
class Foo extends EntityStruct
{
    #[PrimaryKey]
    #[Field(type: FieldType::UUID)]
    public string $id;

    #[Field(type: FieldType::STRING)]
    public string $string;
}
```

### Typescript support for webpack config in extensions

Extensions can now use typescript (.ts and .cts) files for their webpack configuration.

### Added meteor component library to the administration

The [Meteor component library](https://shopware.design/meteor-components/) was added as a new dependency to the administration. All library components are now also directly available in the administration.

### Store theme scripts in database

Theme scripts for each theme are now stored in the database. This allows serving files directly from the DB instead of the file system.

### Order Approval improvements

The order approval got improved with inline editing of approval rules.

### Add wrapper component for sw-select-field

The old `sw-select-field` component will be removed in the next major version. Please use the new `mt-select` component instead.

### Added maximum mail body length config

Added new config option `shopware.mail.max_body_length` to set the maximum mail body length.

### Implement mt-banner code mod

The old `sw-alert` component will be removed in the next major version. Please use the new `mt-banner` component instead.

### Unify SendMailAction constants: deprecated constants

* Deprecated constants `Shopware\Core\Content\MailTemplate\Subscriber\MailSendSubscriberConfig::{ACTION_NAME,MAIL_CONFIG_EXTENSION}` use `Shopware\Core\Content\Flow\Dispatching\Action\SendMailAction::{ACTION_NAME,MAIL_CONFIG_EXTENSION}` instead
* Deprecated constant `Shopware\Core\Content\MailTemplate\MailTemplateActions::MAIL_TEMPLATE_MAIL_SEND_ACTION` use `Shopware\Core\Content\Flow\Dispatching\Action\SendMailAction::ACTION_NAME` instead
* Deprecated not needed class `Shopware\Core\Content\MailTemplate\MailTemplateActions`

### Add wrapper component for sw-textarea-field

The old `sw-textarea-field` component will be removed in the next major version. Please use the new `mt-textarea` component instead.

### Make Shopware update event hookable

Added `shopware.updated` hookable event, containing the old and new shopware version as a webhook.

### Add wrapper component for sw-datepicker

The old `sw-datepicker` component will be removed in the next major version. Please use the new `mt-datepicker` component instead.

### Add wrapper component for sw-colorpicker

The old `sw-colorpicker` component will be removed in the next major version. Please use the new `mt-colorpicker` component instead.

### Add wrapper component for sw-external-link

The old `sw-external-link` component will be removed in the next major version. Please use the new `mt-external-link` component instead.

### Add wrapper component for sw-skeleton-bar

The old `sw-skeleton-bar` component will be removed in the next major version. Please use the new `mt-skeleton-bar` component instead.

### Implement mt-email-field

The old `sw-email-field` component will be removed in the next major version. Please use the new `mt-email-field` component instead.

## Fixed bugs

* [NEXT-29683](https://issues.shopware.com/issues/NEXT-29683) | Admin: Search by document numbers does not work for orders with many documents (24 votes)
* [NEXT-35237](https://issues.shopware.com/issues/NEXT-35237) | Wrong request / Unable to find a matching sales channel for the request: "%/account/login" (12 votes)
* [NEXT-31160](https://issues.shopware.com/issues/NEXT-31160) | Media admin: all media-files are declared as "unused medium", regardless of whether and how often they are in use where (12 votes)
* [NEXT-27720](https://issues.shopware.com/issues/NEXT-27720) | Admin profile image can not be uploaded  (8 votes)
* [NEXT-35332](https://issues.shopware.com/issues/NEXT-35332) | Bad Performance in Order Module when filtering on Promotions, Affiliate-, or Campain Codes (7 votes)
* [NEXT-35509](https://issues.shopware.com/issues/NEXT-35509) | Flow Builder: Webhook Action for "Employee / Recovery / Request" not working (5 votes)
* [NEXT-36090](https://issues.shopware.com/issues/NEXT-36090) | No validation added on mandatory custom field in admin entity form. (2 votes)
* [NEXT-34736](https://issues.shopware.com/issues/NEXT-34736) | Wrong Calculation of Turnover (2 votes)
* [NEXT-32358](https://issues.shopware.com/issues/NEXT-32358) | Customer's turnover currency is wrong (2 votes)
* [NEXT-36150](https://issues.shopware.com/issues/NEXT-36150) | Touch-Event Tax Hint Product Detail Page (mobile) (1 votes)
* [NEXT-36103](https://issues.shopware.com/issues/NEXT-36103) | Wrong ReverseInherited field in CustomPriceDefinition (1 votes)
* [NEXT-36036](https://issues.shopware.com/issues/NEXT-36036) | Categories shown in suggested search results (1 votes)
* [NEXT-35996](https://issues.shopware.com/issues/NEXT-35996) | StoreApiCustomFieldMapper doesn't handle multiple selects (1 votes)
* [NEXT-35342](https://issues.shopware.com/issues/NEXT-35342) | Flow Builder - Rule 'created by administrator' can not be used for event 'order placed' (1 votes)
* [NEXT-35094](https://issues.shopware.com/issues/NEXT-35094) | Unprintable ASCII characters are still allowed in filenames when uploading media via the API (1 votes)
* [NEXT-34501](https://issues.shopware.com/issues/NEXT-34501) | Shopware Commercial can't be uninstalled without breaking (1 votes)
* [NEXT-34024](https://issues.shopware.com/issues/NEXT-34024) | Order number is no longer displayed in tab title (1 votes)
* [NEXT-33627](https://issues.shopware.com/issues/NEXT-33627) | bin/console import:entity - profile name not found (1 votes)
* [NEXT-36418](https://issues.shopware.com/issues/NEXT-36418) | \[Github] NEXT-00000 - Add missing module warn message (0 votes)
* [NEXT-36414](https://issues.shopware.com/issues/NEXT-36414) | IterateEntityMessage in messenger tasks creates errors and polutes the log (0 votes)
* [NEXT-36325](https://issues.shopware.com/issues/NEXT-36325) | \[Github] NEXT-0000 - Improve write exception message to include property, that has faulty content (0 votes)
* [NEXT-36289](https://issues.shopware.com/issues/NEXT-36289) | \[Github] NEXT-00000 - Fix changeset issues (0 votes)
* [NEXT-36288](https://issues.shopware.com/issues/NEXT-36288) | \[Github] feat: Add event to select variant on product detail page (0 votes)
* [NEXT-36275](https://issues.shopware.com/issues/NEXT-36275) | Store-api doesn't return main variant product when parent product is being retrieved (0 votes)
* [NEXT-36246](https://issues.shopware.com/issues/NEXT-36246) | Entity extension for none existing entities (0 votes)
* [NEXT-36155](https://issues.shopware.com/issues/NEXT-36155) | \[Github] Update logo.html.twig (0 votes)
* [NEXT-36151](https://issues.shopware.com/issues/NEXT-36151) | \[Github] Do not add promotion when cart price is zero (0 votes)
* [NEXT-36145](https://issues.shopware.com/issues/NEXT-36145) | \[Github] Add missing violation snippet for email at path /account/register (0 votes)
* [NEXT-36143](https://issues.shopware.com/issues/NEXT-36143) | \[Github] feat: resolve extension parameters in compiler passes (0 votes)
* [NEXT-36115](https://issues.shopware.com/issues/NEXT-36115) | \[Github] NEXT-00000: Fix AR on Meta Quest 3 (0 votes)
* [NEXT-36108](https://issues.shopware.com/issues/NEXT-36108) | \[Github] NewsletterSubscribe add salesChannelId filter (0 votes)
* [NEXT-36107](https://issues.shopware.com/issues/NEXT-36107) | \[Github] NEXT-00000 - Fix review filter (0 votes)
* [NEXT-36088](https://issues.shopware.com/issues/NEXT-36088) | \[Github] Add database profiler on CLI if "--profile" option is used. (0 votes)
* [NEXT-36082](https://issues.shopware.com/issues/NEXT-36082) | Path error when root composer.json is a plugin (0 votes)
* [NEXT-36064](https://issues.shopware.com/issues/NEXT-36064) | \[Github] feat: Add order criteria event to OrderRoute (0 votes)
* [NEXT-36025](https://issues.shopware.com/issues/NEXT-36025) | \[Github] NEXT-00000 - Add missing transactions association (0 votes)
* [NEXT-36024](https://issues.shopware.com/issues/NEXT-36024) | \[Github] Allow editing custom fields for order addresses (0 votes)
* [NEXT-36023](https://issues.shopware.com/issues/NEXT-36023) | \[Github]  Fix wrong address uses from cart address validator (0 votes)
* [NEXT-35968](https://issues.shopware.com/issues/NEXT-35968) | \[Github] NEXT-35968 - Fix OpenApi Schema validation  (0 votes)
* [NEXT-34326](https://issues.shopware.com/issues/NEXT-34326) | \[Github] NEXT-00000 - Fixes #3519 add Last-Modified header to feeds (0 votes)

## Credits

Thanks to all our contributors for helping us improve Shopware with every pull request!

* [Fabian Blechschmidt](https://github.com/Schrank)
* [Jasper Peters](https://github.com/JasperP98)
* [Alexander Menk](https://github.com/amenk)
* [tinect](https://github.com/tinect)
* [Benjamin Wittwer](https://github.com/akf-bw)
* [Tomislav Odovic](https://github.com/odovictoma)
* [Philip Standt](https://github.com/Ocarthon)
* [Benedikt Brunner](https://github.com/Benedikt-Brunner)
* [Alexander Bischko](https://github.com/divide29)
* [Yannick Van Velthoven](https://github.com/yannick-meteor)
* [Max](https://github.com/aragon999)
* [Andreas Allacher](https://github.com/AndreasA)
* [Alexander Stehlik](https://github.com/astehlik)
* [Marcus Müller](https://github.com/M-arcus)
* [Joshua Behrens](https://github.com/JoshuaBehrens)

## More resources

* [Detailed diff on Github](https://github.com/shopware/shopware/compare/v6.6.2.0...v6.6.3.0) to the former version
* [Changelog on GitHub](https://github.com/shopware/shopware/blob/v6.6.3.0/CHANGELOG.md) for this version.
* [Release News on corporate blog](https://www.shopware.com/en/news/shopware-6-release-news-june-2024/)
* [Installation overview](https://developer.shopware.com/docs/guides/installation/)
* [Update from a previous installation](https://developer.shopware.com/docs/guides/installation/template.html#update-shopware)

## Get in touch

Discuss about decisions, bugs you might stumble upon, etc in our [community slack](https://slack.shopware.com). See you there ;)

---

---

## Release notes Shopware 6.6.3.1
**Source:** [release-notes/6.6/6.6.3.1.md](https://developer.shopware.com/release-notes/6.6/6.6.3.1.md)  
# Release notes Shopware 6.6.3.1

## Abstract

This patch release contains one bug fixe.

## System requirements

* tested on PHP 8.2 and 8.3
* tested on MySQL 8 and MariaDB 10.11

## Fixed bugs

* [NEXT-36780](https://issues.shopware.com/issues/NEXT-36780) | Plugin Composer install destroys Shopware (1 vote)

## More resources

* [Detailed diff on Github](https://github.com/shopware/shopware/compare/v6.6.3.0...v6.6.3.1) to the former version
* [Changelog on GitHub](https://github.com/shopware/shopware/blob/v6.6.3.1/CHANGELOG.md) for this version.
* [Installation overview](https://developer.shopware.com/docs/guides/installation/)
* [Update from a previous installation](https://developer.shopware.com/docs/guides/installation/template.html#update-shopware)

## Get in touch

Discuss about decisions, bugs you might stumble upon, etc in our [community slack](https://slack.shopware.com). See you there ;)

---

---

## Release notes Shopware 6.6.4.0
**Source:** [release-notes/6.6/6.6.4.0.md](https://developer.shopware.com/release-notes/6.6/6.6.4.0.md)  
# Release notes Shopware 6.6.4.0

## Abstract

This release improves our payment handlers, jest runner, and state management, alongside a transition to an event-based extension system. Key bug fixes enhance overall system stability and address critical issues in Shopware.

## System requirements

* tested on PHP 8.2 and 8.3
* tested on MySQL 8 and MariaDB 10.11

## Improvements

### Improve payment handlers & general payment process

The payment handler has become quite complex over the years. It's time for a much-needed refactor to make it clearer and more maintainable.

* [More info](https://github.com/shopware/shopware/blob/930fb3445d35d999e9ed6456c52d9cbe169d6fd0/changelog/_unreleased/2024-05-13-improve-payment-handlers.md)

### Add jest runner with disabled compat mode

Currently, our component tests in Jest are running with enabled compat mode. To remove the compat mode for each
component we need to add a new Jest runner with disabled compat mode to make sure that the tests are running without
compat mode.

* [ADR](https://github.com/shopware/shopware/blob/930fb3445d35d999e9ed6456c52d9cbe169d6fd0/adr/2024-06-12-add-jest-runner-with-disabled-compat-mode.md)

### Transition from Vuex to Pinia (Administration)

Deprecated Vuex implementation and use Pinia implementation instead. All Shopware states will become Pinia Stores and will be available via Shopware.Store , `Shopware.State` related is now deprecated.

* [More info](https://github.com/shopware/shopware/blob/7c170d3fb0754ce9671bb00a0fd949a80fc74d96/changelog/_unreleased/2024-06-20-replace-vuex-with-pinia.md)

### Transition to an Event-Based Extension System (Core)

In our current Core architecture, we rely heavily on PHP decoration, Adapter, and Factory patterns to allow for extensions and customizations by third-party developers. While these patterns are effective, they present significant challenges like Backward and Forward Compatibility, Process Extension Limitations, ... .To address these challenges, we have decided to transition to an event-based extension system. This new approach will replace the existing decoration, Adapter, and Factory patterns as the primary method for extending and customizing our system.

* [ADR](https://github.com/shopware/shopware/blob/930fb3445d35d999e9ed6456c52d9cbe169d6fd0/adr/2024-06-18-extended-event-system.md)

### Improve composer executions while plugin lifecycle

Previously, when a plugin was installed, it updated all the composer packages, which was very ineffective. With the new improvement:

* Only directly affected package dependencies are updated
* Lock the version of composer/composer to not update himself
* Do not run composer commands when the Shop is in cluster mode

### Remote thumbnail generation

With these changes, we allow the possibility of disabling the filesystem thumbnail generation. You can then use an external CDN service to handle the thumbnails. As the consequence, when the remote thumbnail config is enabled, the thumbnail images and thumbnail records in the database are not generated.

* [Changes](https://github.com/shopware/shopware/commit/7c170d3fb0754ce9671bb00a0fd949a80fc74d96)
* [Detail](https://github.com/shopware/shopware/blob/7c170d3fb0754ce9671bb00a0fd949a80fc74d96/changelog/_unreleased/2024-05-21-disable-thumbnail-generation-and-use-fastly.md)

By default, the config is disabled, you can enable the remote thumbnail generation by override the `config/packages/shopware.yaml`

```yaml
remote_thumbnails:
    enable: true
    pattern: '{mediaUrl}/{mediaPath}?width={width}'
```

For example, consider a scenario where you want to generate a thumbnail with a width of 80px.
With the pattern set as `{mediaUrl}/{mediaPath}?width={width}`, the resulting URL would be `https://yourshop.example/abc/123/456.jpg?width=80`.

### Remove unwanted aria-live attributes from sliders

By default, all Storefront sliders/carousels (`GallerySliderPlugin`, `BaseSliderPlugin`, `ProductSliderPlugin`) are adding an `aria-live` region to announce slider updates to a screen reader.

In some cases this can worsen the accessibility, for example when a slider uses "auto slide" functionality. With automatic slide the slider updates can disturb the reading of other contents on the page.

You can now deactivate the `aria-live` region on the slider plugins with the new option `ariaLive` (default: `true`).

Example for `GallerySliderPlugin` (Also works for `BaseSliderPlugin` and `ProductSliderPlugin`)

```diff
{% set gallerySliderOptions = {
    slider: {
+        ariaLive: false,
        autoHeight: false,
    },
    thumbnailSlider: {
+        ariaLive: false,
        controls: true,
        responsive: {}
    }
} %}

<div data-gallery-slider-options='{{ gallerySliderOptions|json_encode }}'>
```

When `ariaLive` is `false` it will omit the `aria-live` region in the generated `tiny-slider` HTML code:

```diff
<div class="tns-outer" id="tns3-ow">
-    <div class="tns-liveregion tns-visually-hidden" aria-live="polite" aria-atomic="true">
-        slide <span class="current">2</span> of 6
-    </div>
    <div id="tns3-mw" class="tns-ovh">
        <!-- Slider contents -->
    </div>
</div>
```

## Fixed bugs

* [NEXT-35545](https://issues.shopware.com/issues/NEXT-35545) | Flow Builder - tags for entity "order" AND / OR "customer" are not set (7 votes)
* [NEXT-34393](https://issues.shopware.com/issues/NEXT-34393) | Invoice - Column name "Unit price" and "Total" always shows "incl. vat" | Rechnung - Spalten "Stückpreis" und "Gesamtpreis" zeigen immer den Zusatz "inkl. UST" an (7 votes)
* [NEXT-36545](https://issues.shopware.com/issues/NEXT-36545) | Information Disclosure via Store-API Category endpoint (6 votes)
* [NEXT-34382](https://issues.shopware.com/issues/NEXT-34382) | {{ config.companyAddress }} appearing twice on invoice and delivery note (5 votes)
* [NEXT-36808](https://issues.shopware.com/issues/NEXT-36808) | SwagCommercial Erweiterung (5 votes)
* [NEXT-36813](https://issues.shopware.com/issues/NEXT-36813) | Administration Component `<sw-select-number-field>` not working (2 votes)
* [NEXT-35563](https://issues.shopware.com/issues/NEXT-35563) | Multiple CrossSellings Backend Bug (2 votes)
* [NEXT-34217](https://issues.shopware.com/issues/NEXT-34217) | Name length isn't checked on registration (2 votes)
* [NEXT-36479](https://issues.shopware.com/issues/NEXT-36479) | Overriding messenger routing (2 votes)
* [NEXT-35701](https://issues.shopware.com/issues/NEXT-35701) | Sender e-mail address field has no function in the Cloud. (2 votes)
* [NEXT-36415](https://issues.shopware.com/issues/NEXT-36415) | we can not change the Shipping Costs after the order is submitted (2 votes)
* [NEXT-35812](https://issues.shopware.com/issues/NEXT-35812) | 400 Bad Request, when you try to complete a subscription with an already registered e-mail. (1 votes)
* [NEXT-34465](https://issues.shopware.com/issues/NEXT-34465) | AI assistant description text outside text box (1 votes)
* [NEXT-36499](https://issues.shopware.com/issues/NEXT-36499) | Cms data mapping for nested entity don't works for translations (1 votes)
* [NEXT-36477](https://issues.shopware.com/issues/NEXT-36477) | Currency dependent pricing modal is broken (1 votes)
* [NEXT-35967](https://issues.shopware.com/issues/NEXT-35967) | It is not possible to export the country state of shipping address. (1 votes)
* [NEXT-36348](https://issues.shopware.com/issues/NEXT-36348) | Unavailable variant options are not grayed out if property value display type set to "dropdown" (1 votes)
* [NEXT-36838](https://issues.shopware.com/issues/NEXT-36838) | \[Github] Add discount id check when collection promotions (0 votes)
* [NEXT-36983](https://issues.shopware.com/issues/NEXT-36983) | \[Github] Add mediaUpdatedAt to the thumbnail pattern (0 votes)
* [NEXT-36566](https://issues.shopware.com/issues/NEXT-36566) | \[Github] feat: add debug info mail header when staging mode enabled (0 votes)
* [NEXT-36555](https://issues.shopware.com/issues/NEXT-36555) | \[Github] feat: add direct admin url in staging banner (0 votes)
* [NEXT-36982](https://issues.shopware.com/issues/NEXT-36982) | \[Github] Fix media url loader with unset thumbnails (0 votes)
* [NEXT-36695](https://issues.shopware.com/issues/NEXT-36695) | \[Github] Next 0000 Trasform Scaffold generator into their own separated commands (0 votes)
* [NEXT-33234](https://issues.shopware.com/issues/NEXT-33234) | \[Github] NEXT-00000 - feat: implement product-stream custom field entity select (0 votes)
* [NEXT-36543](https://issues.shopware.com/issues/NEXT-36543) | \[Github] NEXT-00000 - Fix sw-verify-user-modal autocomplete type (0 votes)
* [NEXT-36540](https://issues.shopware.com/issues/NEXT-36540) | \[Github] NEXT-21783 - Fix admin grid headline action resize on click (0 votes)
* [NEXT-36422](https://issues.shopware.com/issues/NEXT-36422) | API Bug b2b employee management (0 votes)
* [NEXT-36428](https://issues.shopware.com/issues/NEXT-36428) | B2B QuoteManagement: Cover images are not displayed (0 votes)
* [NEXT-36563](https://issues.shopware.com/issues/NEXT-36563) | Fix Elasticsearch prefix query (0 votes)
* [NEXT-35346](https://issues.shopware.com/issues/NEXT-35346) | Fix test RulePreviewTest::testRulePreview (0 votes)
* [NEXT-34301](https://issues.shopware.com/issues/NEXT-34301) | Flow send-email-action uses wrong adress (0 votes)
* [NEXT-33049](https://issues.shopware.com/issues/NEXT-33049) | Image Import via CSV not possible (0 votes)
* [NEXT-36114](https://issues.shopware.com/issues/NEXT-36114) | import of boundSalesChannel by name is currently not possible  (0 votes)
* [NEXT-34354](https://issues.shopware.com/issues/NEXT-34354) | Import/Export: Category name leads to empty result (0 votes)
* [NEXT-35453](https://issues.shopware.com/issues/NEXT-35453) | Improve storefront watcher (0 votes)
* [NEXT-36510](https://issues.shopware.com/issues/NEXT-36510) | The condition 'Total volume of all products' in a rule of a price matrix (shipping costs) does not get evaluated correctly (0 votes)
* [NEXT-36663](https://issues.shopware.com/issues/NEXT-36663) | Variant bulk edit info box broken (0 votes)
* [NEXT-36669](https://issues.shopware.com/issues/NEXT-36669) | Wishlist icon not available on PDP when commercial plugin activated (0 votes)

## Credits

Thanks to all our contributors for helping us improve Shopware with every pull request!

* [Rafael Kraut](https://github.com/RafaelKr)
* [Joshua Behrens](https://github.com/JoshuaBehrens)
* [Benjamin Wittwer](https://github.com/akf-bw)
* [Marcus Müller](https://github.com/M-arcus)
* [Max](https://github.com/aragon999)
* [Jasper Peeters](https://github.com/JasperP98)
* [Paik Paustian](https://github.com/hype09)
* [Melvin Achterhuis](https://github.com/MelvinAchterhuis)
* [Raffaele Carelle](https://github.com/raffaelecarelle)

## More resources

* [Detailed diff on Github](https://github.com/shopware/shopware/compare/v6.6.3.1...v6.6.4.0) to the former version
* [Changelog on GitHub](https://github.com/shopware/shopware/blob/v6.6.4.0/CHANGELOG.md) for this version.
* [Release News on corporate blog](https://www.shopware.com/en/news/shopware-6-release-news-june-2024/)
* [Installation overview](https://developer.shopware.com/docs/guides/installation/)
* [Update from a previous installation](https://developer.shopware.com/docs/guides/installation/template.html#update-shopware)

## Get in touch

Discuss about decisions, bugs you might stumble upon, etc in our [community slack](https://slack.shopware.com). See you there ;)

---

---

## Release notes Shopware 6.6.4.1
**Source:** [release-notes/6.6/6.6.4.1.md](https://developer.shopware.com/release-notes/6.6/6.6.4.1.md)  
# Release notes Shopware 6.6.4.1

## Abstract

Besides other bug fixes, this release contains a security fix. Please update as soon as possible.

## System requirements

* tested on PHP 8.2 and 8.3
* tested on MySQL 8 and MariaDB 10.11

## Fixed bugs

* [NEXT-36813](https://issues.shopware.com/issues/NEXT-36813) | Administration Component `<sw-select-number-field>` not working
* [NEXT-37115](https://issues.shopware.com/issues/NEXT-37115) | Browser crashes when editing Shopping Experiences
* [NEXT-37140](https://issues.shopware.com/issues/NEXT-37140) | Search suggest route - Possible Denial of Service (DoS) entry point?
  * See explanation below

### NEXT-37140

This release contains a security update.

The potential effects of the behaviour without the patch are not critical but could lead to the database server being temporarily overloaded and the store no longer being accessible.

There is no known exploit at the time of release. The fix in NEXT-37140 is a precaution.

The fix adds a new restriction for the maximum length of search terms.

Before Shopware v6.6.4.1, the maximum length was unrestricted; this fix restricts it to 300 characters after updating. 300 is a sensible default; in most cases, the shop will not be affected by this limitation.

Setting a higher limit in a few exceptional cases may be necessary.  
In that case, the new default limit of 300 can be adjusted by adding a new entry to the file `config/packages/shopware.yaml`.

The config option is as follows:

```yaml
shopware:
  search:
    term_max_length: 300
```

Here, "300" must be replaced by a value that meets the store's requirements. This adjustment is only necessary if extensions need search terms that are longer than 300 characters.

More information on configuring your installation can be found [in the documentation](https://developer.shopware.com/docs/guides/hosting/configurations/).

## Credits

Thanks to all our contributors for helping us improve Shopware with every pull request!

## More resources

* [Detailed diff on Github](https://github.com/shopware/shopware/compare/v6.6.4.0...v6.6.4.1) to the former version
* [Changelog on GitHub](https://github.com/shopware/shopware/blob/v6.6.4.1/CHANGELOG.md) for this version.
* [Installation overview](https://developer.shopware.com/docs/guides/installation/)
* [Update from a previous installation](https://developer.shopware.com/docs/guides/installation/template.html#update-shopware)

## Get in touch

Discuss about decisions, bugs you might stumble upon, etc in our [community slack](https://slack.shopware.com). See you there ;)

---

---

## Release notes Shopware 6.6.5.0
**Source:** [release-notes/6.6/6.6.5.0.md](https://developer.shopware.com/release-notes/6.6/6.6.5.0.md)  
*(Body truncated in this bundle; follow the link for the rest.)*

# Release notes Shopware 6.6.5.0

## Abstract

This minor release contains some interesting features as well as technical improvements like impersonation (thanks to [Benjamin Wittwer](https://github.com/akf-bw)!), improved search and AR handling. Additionally, 50+ bugs could be fixed.

## System requirements

* tested on PHP 8.2 and 8.3
* tested on MySQL 8 and MariaDB 10.11

## Improvements

### Added customer impersonation feature (administration)

This release introduces the customer impersonation feature, which was one of the most requested features by the community for the Shopware 6 administration. This feature was previously part of Shopware 5, yet missing in Shopware 6. With this release, it is now fully implemented in Shopware 6; thanks to [Benjamin Wittwer](https://github.com/akf-bw) for this contribution! As a user in the administration, you can choose from the available sales channels and sales channel domains to log in as a customer. The feature can be used by users with the "api\_proxy\_imitate-customer" permission in the administration on the customer detail page. It is also fully compatible with the headless sales channel type.

* [Pull request](https://github.com/shopware/shopware/pull/3727)
* [NEXT-Ticket](https://issues.shopware.com/issues/NEXT-8593)

### Added default value for augmented-reality (plans only)

Previously, you first had to switch to the media, search for the file, and activate AR. Now, you can enable AR by default in the media settings. This way, 3D files will automatically have AR enabled when presented in the storefront.

### Added error handling to HttpClient js

For backwards compatibility, we added an errorHandling Parameter to HttpClient to handle errors internally if the plugin does not want to handle errors for every call by itself.

### Added API routes list endpoints

Added endpoints that return the list of available API routes. Use `/api/_info/routes` for the available API routes for the Admin and `/store-api/_info/routes` for the Store API.

### Changed scoring of search terms

Improved product search term scoring to provide better search results on exact matches.

### Changed Webhook Cleanup

We changed the webhook cleanup to only clean up successfully delivered or permanently failed webhook events. Thus, preventing race conditions where the cleanup task might delete webhook event entries that are still running or being retried.

### Add skip to content link to improve a11y (accessability)

This improves a11y because a keyboard or screen-reader user does not have to "skip" through all elements of the page (header, top-bar) and can jump straight to the main content if wanted. The "skip to main content" link will not be visible, unless it has focus.

### Deprecating Meteor Admin SDK public SDK

Recently, the need arose to deprecate the `Meteor Admin SDK` public API built into the Shopware Core. We need to be able to deprecate the public API, which consists of `component sections` and `data sets`.

### Deprecated automatic state change for `Shopware\Core\Checkout\Payment\Cart\PaymentHandler\DebitPayment`

The default payment method "Direct debit" will no longer automatically change the order state to "in progress". Use the flow builder instead, if you want to keep the former behaviour.

* [More info](https://github.com/shopware/shopware/blob/383f3da80181a5fa4f3f6aabcf42de4f325b88b4/changelog/_unreleased/2024-07-23-remove-state-change-for-default-payment-handlers.md)

### Default payment method removed

We deprecated a lot of routes, classes, methods, templates and blocks that are related to the default payment method of a customer. The default payment method of a customer is removed and the last used payment method will always be the one chosen during login.
This includes the remove of the rule builder condition `customerDefaultPaymentMethod`. Existing rules with this condition will be automatically migrated to the new condition paymentMethod, meaning the currently selected payment method.
Also, the trigger `checkout.customer.changed-payment-method` is removed from the flow builder, since customers do not have default payment methods anymore. Existing flows will be automatically disabled with Shopware 6.7 and removed.

* [More info](https://github.com/shopware/shopware/blob/383f3da80181a5fa4f3f6aabcf42de4f325b88b4/changelog/_unreleased/2024-07-11-remove-customer-default-payment-method.md)

## Fixed bugs

* [NEXT-8593](https://issues.shopware.com/issues/NEXT-8593) | Login as this customer (from administration)
* [NEXT-36102](https://issues.shopware.com/issues/NEXT-36102) | Productslider empty! (51 votes)
* [NEXT-16807](https://issues.shopware.com/issues/NEXT-16807) | Available Variants: Search by product number not possible (20 votes)
* [NEXT-34331](https://issues.shopware.com/issues/NEXT-34331) | Translations for custom fields (13 votes)
* [NEXT-36871](https://issues.shopware.com/issues/NEXT-36871) | CustomField Type "price" buggy in Admin-Interface (7 votes)
* [NEXT-37072](https://issues.shopware.com/issues/NEXT-37072) | Webhook event log can throw a critical exception - Webhook Event Log kann eine kritische Exception werfen (6 votes)
* [NEXT-36924](https://issues.shopware.com/issues/NEXT-36924) | StoreApiSeoResolver and auth\_required=false lead to TypeError (6 votes)
* [NEXT-33778](https://issues.shopware.com/issues/NEXT-33778) | The order is placed incorrectly when the shopping cart or a product changes (4 votes)
* [NEXT-33271](https://issues.shopware.com/issues/NEXT-33271) | ElasticsearchFieldMapper ignores customFieldMapping (4 votes)
* [NEXT-37405](https://issues.shopware.com/issues/NEXT-37405) | 'Allow payment change after checkout' feature is not working correctly (3 votes)
* [NEXT-36996](https://issues.shopware.com/issues/NEXT-36996) | WYSIWYG editor's dropdown menu won't collapse again (3 votes)
* [NEXT-36534](https://issues.shopware.com/issues/NEXT-36534) | Bulk edit with more than 25 selections broken (3 votes)
* [NEXT-34674](https://issues.shopware.com/issues/NEXT-34674) | Search for product numbers in custom fields containing "-" character (3 votes)
* [NEXT-29703](https://issues.shopware.com/issues/NEXT-29703) | Incorrect/missleading snippets for email flow action (3 votes)
* [NEXT-37121](https://issues.shopware.com/issues/NEXT-37121) | Search by product number should redirect to product detail instead of forwarding (2 votes)
* [NEXT-36807](https://issues.shopware.com/issues/NEXT-36807) | Incorrect Discounted Subtotal Calculation for Net Price Customers in Quote (2 votes)
* [NEXT-35061](https://issues.shopware.com/issues/NEXT-35061) | Own e-mail template unusable after extension was deactivated and reactivated. (2 votes)
* [NEXT-37512](https://issues.shopware.com/issues/NEXT-37512) | \[Github] Fix cms product slider offsetWidth error (1 votes)
* [NEXT-36927](https://issues.shopware.com/issues/NEXT-36927) | sw-cache-hash and sw-states cookies are deleted on 404 pages (1 votes)
* [NEXT-36917](https://issues.shopware.com/issues/NEXT-36917) | SwagCommercial Plugin Problem with PayOne Plugin (1 votes)
* [NEXT-36133](https://issues.shopware.com/issues/NEXT-36133) | Product comparison no template can be selected (1 votes)
* [NEXT-35983](https://issues.shopware.com/issues/NEXT-35983) | Component sw-category-tree-field limits 25 entities when sending data (1 votes)
* [NEXT-35576](https://issues.shopware.com/issues/NEXT-35576) | Customfield created by plugin is deaktivated in variants (1 votes)
* [NEXT-37428](https://issues.shopware.com/issues/NEXT-37428) | Payment method with Grand total >= rule not available second time (0 votes)
* [NEXT-37386](https://issues.shopware.com/issues/NEXT-37386) | \[Github] \[NEXT-00000] Add CartEvent interface (0 votes)
* [NEXT-37382](https://issues.shopware.com/issues/NEXT-37382) | Errors in Frontend when Elasticsearch stops working (0 votes)
* [NEXT-37376](https://issues.shopware.com/issues/NEXT-37376) | \[Github] NEXT-00000 - Fix performance issues in `EntityLoadedEventFactory` (0 votes)
* [NEXT-37373](https://issues.shopware.com/issues/NEXT-37373) | \[Github] fix: Added `default` node structure for the `system_config` node (0 votes)
* [NEXT-37364](https://issues.shopware.com/issues/NEXT-37364) | \[Github] feat: Add payment method name block (0 votes)
* [NEXT-37361](https://issues.shopware.com/issues/NEXT-37361) | \[Github] fix: Show all property filters when filterable properties are not restricted (0 votes)
* [NEXT-37360](https://issues.shopware.com/issues/NEXT-37360) | \[Github] fix: Linked administration price input with comma values (0 votes)
* [NEXT-37359](https://issues.shopware.com/issues/NEXT-37359) | \[Github] fix: Run unit-setup in admin:unit:watch command (0 votes)
* [NEXT-37358](https://issues.shopware.com/issues/NEXT-37358) | \[Github] NEXT-0000 Administration set limit for options in listing (0 votes)
* [NEXT-37357](https://issues.shopware.com/issues/NEXT-37357) | \[Github] NEXT-00000 - Improve admin login session (0 votes)
* [NEXT-37342](https://issues.shopware.com/issues/NEXT-37342) | \[Github] refactor: Simplify code (0 votes)
* [NEXT-37327](https://issues.shopware.com/issues/NEXT-37327) | \[Github] fix: Open section settings when clicking on "Setting" in the context menu (0 votes)
* [NEXT-37298](https://issues.shopware.com/issues/NEXT-37298) | \[Github] fix: Default layout assignments (0 votes)
* [NEXT-37237](https://issues.shopware.com/issues/NEXT-37237) | \[Github] NEXT-00000 - Fix admin customer sales channel & acl checks (0 votes)
* [NEXT-37175](https://issues.shopware.com/issues/NEXT-37175) | Assets for bundles which use `bundle` suffix can not be loaded (0 votes)
* [NEXT-37172](https://issues.shopware.com/issues/NEXT-37172) | Settings/Users & permissions: User permissions card disappears when enabling "delete" for Warehouse Groups (0 votes)
* [NEXT-37145](https://issues.shopware.com/issues/NEXT-37145) | \[Github] Added missing twig blocks to admin file order-general-info (0 votes)
* [NEXT-37141](https://issues.shopware.com/issues/NEXT-37141) | \[Github] NEXT-00000 - Add button for generation of one or more variants without deleting existing ones (0 votes)
* [NEXT-37123](https://issues.shopware.com/issues/NEXT-37123) | \[Github] ci(github): Update playwright image (0 votes)
* [NEXT-37117](https://issues.shopware.com/issues/NEXT-37117) | Enforce UTC as DB timezone (0 votes)
* [NEXT-37112](https://issues.shopware.com/issues/NEXT-37112) | \[Github] fix: Remove category criteria for editor links (0 votes)
* [NEXT-37104](https://issues.shopware.com/issues/NEXT-37104) | \[Github] NEXT-37104 - Improve wishlist user experience (0 votes)
* [NEXT-37065](https://issues.shopware.com/issues/NEXT-37065) | Cannot add a new media folder (0 votes)
* [NEXT-37041](https://issues.shopware.com/issues/NEXT-37041) | B2B Features Bulk Edit Snippets Missing (0 votes)
* [NEXT-36854](https://issues.shopware.com/issues/NEXT-36854) | \[Github] NEXT-8593 - Add customer impersonation (0 votes)
* [NEXT-36788](https://issues.shopware.com/issues/NEXT-36788) | Add parameters to the flash message in class CartException (0 votes)
* [NEXT-36774](https://issues.shopware.com/issues/NEXT-36774) | Vue.js component override leads to stack overflow (0 votes)
* [NEXT-36419](https://issues.shopware.com/issues/NEXT-36419) | \[Github] fix state-machine transition handling (0 votes)
* [NEXT-35756](https://issues.shopware.com/issues/NEXT-35756) | Javascript Error "SyntaxError: Unexpected end of JSON input"  during ajax call (0 votes)

## Credits

Thanks to all our contributors for helping us improve Shopware with every pull request!

* [Alexander Menk](https://github.com/amenk)
* [Max](https://github.com/aragon999)
* [Benjamin Wittwer](https://github.com/akf-bw)
* [Christoph Pötz](https://github.com/acris-cp)
* [Marina Egner](https://github.com/magraina)
* [Benedikt Brunner](https://github.com/Benedikt-Brunner)
* [Elias Lackner](https://github.com/lacknere)
* [tinect](https://github.com/tinect)
* [Marcel Romeike]

… **Truncated.** Full document: https://developer.shopware.com/release-notes/6.6/6.6.5.0.md


---

## Release notes Shopware 6.6.5.1
**Source:** [release-notes/6.6/6.6.5.1.md](https://developer.shopware.com/release-notes/6.6/6.6.5.1.md)  
# Release notes Shopware 6.6.5.1

## Abstract

This patch release is a security release, additionally containing three regular bug fixes. Please update as soon as possible!

## System requirements

* tested on PHP 8.1, 8.2 and 8.3
* tested on MySQL 8 and MariaDB 10.11

## Security bulletins

* [CVE-2024-42357](https://github.com/shopware/shopware/security/advisories/GHSA-p6w9-r443-r752) | Blind SQL-injection in DAL aggregations
* [CVE-2024-42356](https://github.com/shopware/shopware/security/advisories/GHSA-35jp-8cgg-p4wj) | Server Side Template Injection in Twig using Context functions
* [CVE-2024-42355](https://github.com/shopware/shopware/security/advisories/GHSA-27wp-jvhw-v4xp) | Server Side Template Injection in Twig using deprecation silence tag
* [CVE-2024-42354](https://github.com/shopware/shopware/security/advisories/GHSA-hhcq-ph6w-494g) | Improper Access Control with ManyToMany associations in store-api

## Fixed bugs

* [NEXT-37545](https://issues.shopware.com/issues/NEXT-37545) | PayPal shows all Payment Methods after Updating to 6.6.4.1 (1 vote)
* [NEXT-37555](https://issues.shopware.com/issues/NEXT-37555) | \[Github] feat: change type of class MediaUrlPlaceholderHandler (0 votes)
* [NEXT-37461](https://issues.shopware.com/issues/NEXT-37461) | Icons in front of sub-menus are visible (0 votes)

## Credits

Thanks to all our contributors for helping us improve Shopware with every pull request!

* [tinect](https://github.com/tinect)

## More resources

* [Detailed diff on Github](https://github.com/shopware/shopware/compare/v6.6.5.0...v6.6.5.1) to the former version
* [Changelog on GitHub](https://github.com/shopware/shopware/blob/v6.6.5.1/CHANGELOG.md) for this version.
* [Installation overview](https://developer.shopware.com/docs/guides/installation/)
* [Update from a previous installation](https://developer.shopware.com/docs/guides/installation/template.html#update-shopware)

## Get in touch

Discuss about decisions, bugs you might stumble upon, etc in our [community slack](https://slack.shopware.com). See you there ;)

---

---

## Release notes Shopware 6.6.6.0
**Source:** [release-notes/6.6/6.6.6.0.md](https://developer.shopware.com/release-notes/6.6/6.6.6.0.md)  
*(Body truncated in this bundle; follow the link for the rest.)*

# Release notes Shopware 6.6.6.0

## Abstract

This minor release contains 50+ bug fixes and a lot of improvements, especially concerning a11y (accessability) and improvements of the caching system.

## System requirements

* tested on PHP 8.2 and 8.3
* tested on MySQL 8.0.33, MariaDB 10.11 & 11.0

## Improvements

### IDN support for email addresses

With this version, we added support for internationalized domain names (IDN) in email addresses. This means that you can now use email addresses with special characters in the domain part of the email address.

### Cart performance improvments

Previously on any cart load, the products in the cart has been loaded always from the database and the price, cover and name has been updated to the cart line item. To speed up this process, we now compare the last updated date of the product and only if that does not match we re-fetch the product and update the line item.

Besides that, we store now a errorHash in the Cart object, which is used additonally to determine has the cart changed and needs to be persisted to the database. Previously when a cart contained a cart error, on any cart load the cart has been persisted to the database. Now we only persist the cart if the errorHash has changed.

### Caching of ESI blocks

The `Cache-Control` of ESI requests is now considered also with the internal HTTP Cache (without Varnish) and allows to cache ESI blocks for a certain time. This is useful for pages that are not cached by HTTP Cache but contain ESI blocks that should be cached.

### Removal of Locust

We removed the Locust load testing tool from the platform. The replacement is [K6 by Grafana labs](https://k6.io/), which is a more modern and powerful tool for load testing. Checkout our ready to use [K6 Shopware script](https://github.com/shopware/k6-shopware)

### General application bootstrapping improvements

We improved the performance of the application bootstrapping process by reducing the number of services to be loaded and by utilizing more lazy loading. This will result in faster bootstrapping times of the application for admin-api or store-api requests.

### PHP Opcache preload now works properly

We fixed an issue where the PHP Opcache preload was not working properly when an PDF document was generated. This has been fixed by using `setasign/tfpdf` over `tecnickcom/tcpdf`. The composer package `tecnickcom/tcpdf` will be removed with the next major version.

### Sales Channel Product associations are not added anymore to nested associations

With the last security update (6.6.5.1), we fixed a bug that the SalesChannelRepository is not called for ManyToMany assocaistion to add filters. This caused some performance issues as now all levels of product associations fetch now a cover image, prices and more.

Therefore we introduced a new method `getNestingLevel` to the Criteria object to determine the nesting level of the association. This is now used in the `SalesChannelProductDefinition` to add only the assosiations when the nesting level is 0.

This restores the behaviour before the security update, but still adds the filters required by the security update. This has been also backported to the Security plugin.

### Data Abstraction Layer improvements

* Fixed a bug where an `GROUP BY` clause was missing when a assosication has been loaded with an group field.
* Fixed a bug that it is not possible to create a many to many association to the same entity and add filters to the Criteria field.

### Property Search in Administration now allows to search for group

The property search to add new properties to an product now supports to search for the group name of the property. Additionally, the search is now correctly ranked by the relevance of the search term.

### Screenreader improvements for product listing and listing filters

With this version, we added new include parameters to our listing and filter components in the storefront. These suppose to improve accessibility when using screen readers. For example, we added the `ariaLabel` parameter to all of our filter components which can be used to add a description of the purpose of this filter for screen readers.

### Screenreader improvements for slider elements

In this version, we added new behaviour and styling to slider and gallery elements in the storefront. These changes include:

* Hiding cloned elements for screen readers
* Keeping the focused element always in view to enable navigation of the slider via tab
* Prevent the native scrolling to focused elements of the browser inside the slider to use the slider function instead

### Improved many-to-many association of entities via attributes

With these changes, entities created by attributes now support many-to-many associations with version aware entities.

Thanks to [Nicky Gerritsen](https://github.com/nickygerritsen) for this improvement!

### Added support for state machine fields

State machine state fields can now be created via attributes in your entity definitions. The attribute is taking an `machine` and `scopes` as well as the well known `api` and `column` arguments.

Thanks to [Simone Alers](https://github.com/dorxy) for this improvement!

### States / provinces are now available in flows with order data

States or provinces can now be used in Flow Builder to set rules, for example when shipping to these destinations.

### Improved CSV parsing for Quick Orders

We added support for different delimiters in CSV files you can pass in the Quick Order module. Supported delimiters next to `,` are now `;` and `|`

### Support feature flag extension in plugins

We added the possibility to enable the major feature flag in your tests using our PHPUnit extension. With this, you can run your tests with the major feature flag enabled. This can be usefull to find deprecations in your code. To enable the PHPUnit extension add it to your `phpunit.xml`:

```xml
<extensions>
    ...
    <bootstrap class="Shopware\Core\Test\PHPUnit\Extension\FeatureFlag\FeatureFlagExtension"/>
</extensions>
```

and register your test namespace in your test bootstrap file:

```php
FeatureFlagExtension::addTestNamespace('Your\\Unit\\Tests\\Namespace\\');
```

For more details see this [ADR](https://github.com/shopware/shopware/blob/trunk/adr/2024-07-31-add-more-unit-tests-namespaces-to-featureflag-extension.md)

### Added telemetry abstraction layer

By implementing a telemetry abstraction layer, we provide a unified way to integrate monitoring tools into the Shopware platform. This approach simplifies the process of adding telemetry to the application and ensures consistency across different monitoring tools.

For more information, see this [ADR](https://github.com/shopware/shopware/blob/trunk/adr/2024-07-30-add-telemetry-abstraction-layer.md) and the [README.md](https://github.com/shopware/shopware/blob/trunk/src/Core/Framework/Telemetry/README.md) of our new Telemetry namespace

### Added system health checks

By implementing system health checks, we ensure that the system is monitored and that issues are detected early. This will help to prevent system failures and improve the overall stability of the system.
Moreover, it helps detecting issues at the time of deployment and helps to prevent issues from reaching the end-users.

For more information about our new Health Check Framework see this [ADR](https://github.com/shopware/shopware/blob/trunk/adr/2024-08-02-system-health-check.md)

### Minor accessibility improvements for the storefront

We've enhanced the registration form, and improved text scalability to ensure everyone can navigate and enjoy our platform with ease.

### Restrict the message queue size

* Added `Shopware\Core\Framework\MessageQueue\Subscriber\MessageQueueSizeRestrictListener` to limit the message queue message size to 256KB. It only creates a log entry if a message is bigger than 256KB.
* Deprecated message queue message size. Messages bigger than 256KB will throw an exception with Shopware 6.7

### New `DomAccessHelper` methods to find focusable elements

The `DomAccessHelper` now supports new methods to find DOM elements that can have keyboard focus.
Optionally, an element can be provided as a parameter to only search within this given element. By default, the document body will be used.

### Deprecate cached\*route layer and use new http cache tag event for tagging

Nesting cached routes leads to complex caching, which results in complex invalidations. Additionally, the cache has become very large and should be cached more at the HTTP level.

Collecting cache tags through cache decorators is a hassle. From now on, there's an event that anyone can freely dispatch to attach a tag to the current request. This also allows us to remove those nasty cache tracers.

### Cache hash improvement

We optimized the process of determining the cache hash so that an event is dispatched where elements can be better removed in projects.

You can now also configure cookies to be included in the hash. This allows you to easily handle just one cookie (on/off) to permute the cache.

## Fixed bugs

* [NEXT-23017](https://issues.shopware.com/issues/NEXT-23017) | Time range of a rule can be set in admin user's time zone but is calculated in a different time zone (17 votes)
* [NEXT-37593](https://issues.shopware.com/issues/NEXT-37593) | Promotions are not applied anymore when a position is added to the order and the max. uses per customer is reached (8 votes)
* [NEXT-37412](https://issues.shopware.com/issues/NEXT-37412) | Trigger checkout.customer.deleted does not work (8 votes)
* [NEXT-37161](https://issues.shopware.com/issues/NEXT-37161) | Incorrect available product quantity on PDP (6 votes)
* [NEXT-35455](https://issues.shopware.com/issues/NEXT-35455) | Dropdown account menu doesn't hide when offcancas account menu is active (6 votes)
* [NEXT-34338](https://issues.shopware.com/issues/NEXT-34338) | Incorrect variant display when using a product slider (shopping experience) (4 votes)
* [NEXT-37489](https://issues.shopware.com/issues/NEXT-37489) | No shipping address available in customer group registration for companies (3 votes)
* [NEXT-38079](https://issues.shopware.com/issues/NEXT-38079) | Layout assignment CMS (3 votes)
* [NEXT-34379](https://issues.shopware.com/issues/NEXT-34379) | Unsatisfying display of emails with umlauts (3 votes)
* [NEXT-37741](https://issues.shopware.com/issues/NEXT-37741) | B2B Components / Quote Management not working (2 votes)
* [NEXT-37659](https://issues.shopware.com/issues/NEXT-37659) | Wrong set group scope discount calculation (2 votes)
* [NEXT-37559](https://issues.shopware.com/issues/NEXT-37559) | It is not possible to localize texts in Settings -> Basic Information (2 votes)
* [NEXT-37456](https://issues.shopware.com/issues/NEXT-37456) | List of individual voucher codes - pagination missing if "items per page" is set to 25 (2 votes)
* [NEXT-37289](https://issues.shopware.com/issues/NEXT-37289) | Quote  creation for custom item in admin (2 votes)
* [NEXT-37771](https://issues.shopware.com/issues/NEXT-37771) | \[Github] fix(admin): Allow (batch) deletion of categories from the category tree element (1 votes)
* [NEXT-37629](https://issues.shopware.com/issues/NEXT-37629) | Quotes are not being sent via email (1 votes)
* [NEXT-37482](https://issues.shopware.com/issues/NEXT-37482) | Not possible to right-click & copy in sw-text-editor (1 votes)
* [NEXT-37146](https://issues.shopware.com/issues/NEXT-37146) | UUID instead of domain in settings > customer group > signup form > technical url (1 votes)
* [NEXT-36782](https://issues.shopware.com/issues/NEXT-36782) | \[Github] Add storage name option to entity attributes (1 votes)
* [NEXT-33043](https://issues.shopware.com/issues/NEXT-33043) | Rule Order created by Admin in flow Builder not working (1 votes)
* [NEXT-38115](https://issues.shopware.com/issues/NEXT-38115) | \[Github] Add option to hide progress for indexing commands (0 votes)
* [NEXT-38109](htt

… **Truncated.** Full document: https://developer.shopware.com/release-notes/6.6/6.6.6.0.md


---

## Release notes Shopware 6.6.6.1
**Source:** [release-notes/6.6/6.6.6.1.md](https://developer.shopware.com/release-notes/6.6/6.6.6.1.md)  
# Release notes Shopware 6.6.6.1

## Abstract

This patch release contains

## System requirements

* tested on PHP 8.2 and 8.3
* tested on MySQL 8.0.33, MariaDB 10.11 & 11.0

## Fixed bugs

* [#4681](https://github.com/shopware/shopware/issues/4681) | EmailIdnTwigFilter present in shopware/storefront, breaks headless setups on ^v6.6.6.0
* [#4646](https://github.com/shopware/shopware/issues/4646) | By some reason CachedProductDetailRoute::load returned ProductCrossSellingRouteResponse
* [#4650](https://github.com/shopware/shopware/issues/4650) | When clicking on products in the product slider, the slider scrolls a few steps further and doesn't follow the URL
* [#4668](https://github.com/shopware/shopware/issues/4668) | base-slider plugin tries to set attribute on undefined object controlsContainer
* [NEXT-33697](https://issues.shopware.com/issues/NEXT-33697) | Focused slides in the carousel are not being moved into the visible area

## More resources

* [Detailed diff on Github](https://github.com/shopware/shopware/compare/v6.6.6.0...v6.6.6.1) to the former version
* [Changelog on GitHub](https://github.com/shopware/shopware/blob/v6.6.6.1/CHANGELOG.md) for this version.
* [Installation overview](https://developer.shopware.com/docs/guides/installation/)
* [Update from a previous installation](https://developer.shopware.com/docs/guides/installation/template.html#update-shopware)

## Get in touch

Discuss about decisions, bugs you might stumble upon, etc in our [community slack](https://slack.shopware.com). See you there ;)

---

---

## Release notes Shopware 6.6.7.0
**Source:** [release-notes/6.6/6.6.7.0.md](https://developer.shopware.com/release-notes/6.6/6.6.7.0.md)  
# Release notes Shopware 6.6.7.0

## Abstract

This minor release contains some interesting features as well as technical improvements like Accessibility improvements and OpenTelemetry enhancements.

## System requirements

* tested on PHP 8.2 and 8.3
* tested on MySQL 8 and MariaDB 10.11

## Improvements

### Sales Channel Domain Mapping missing page

Previously, when you tried to access the shop with an unknown URL, Shopware showed an exception page. Now we show a page that this domain is not configured with steps how to configure it.

### Accessibility improvements

This release contains several accessibility improvements to make Shopware more accessible for everyone like:

* Improved text formatting in the storefront
* Improved navigation in account order page using the keyboard

### Improvments to the Administration Text Editor

The text editor in the administration generates now `<p>` tags instead of `<div>` tags for better semantics. Also the editor will now wrap loose text nodes to fix rendering issues.

### Dependency Updates

We updated several dependencies to their latest versions like `opensearch-php` to fix deprecations on PHP 8.4. We still have some deprecations

### Improvments to Health check

The command `bin/console system:check` now has a new option `--format` to output the results in different formats like `json` or `table` for better processing of the results.

### Breadcrumb API for Store-API

We added a new dedicated API endpoint to fetch the breadcrumb of a product or category. This is useful if you want to display the breadcrumb of a product in a custom storefront.

To get more information about the new endpoints, please check the [changelog entry](https://github.com/shopware/shopware/blob/21da8447ae6681d1187e255efb287ae59faed061/changelog/_unreleased/2024-02-01-add-store-api-endpoints-for-product-and-category-breadcrumb.md)

### Sitemap Proxy for external stored sitemaps

It's possible to store the sitemap files in an external storage like S3. But search engines does not allow to crawl the sitemap files from an external site. To solve this problem we added a new proxy endpoint, which serves the sitemap from the same domain, but loads the file from the external storage.

## Fixed bugs

* [NEXT-38724](https://github.com/shopware/shopware/issues/4994) - \[Github] fix: Inject cmsService to properly load demo value
* [NEXT-38702](https://github.com/shopware/shopware/issues/4956) - \[Github] Added inner block for order list bulk modal slot
* [NEXT-38613](https://github.com/shopware/shopware/issues/4923) - \[Github] feat: move NavigationPageLoadedEvent
* [NEXT-38521](https://github.com/shopware/shopware/issues/4912) - \[Github] Add srsltid to ignored url parameters
* [NEXT-38519](https://github.com/shopware/shopware/issues/4910) - Overwrite SW language pack snippets with own theme snippet files don't work (only for DE and EN)
* [NEXT-38436](https://github.com/shopware/shopware/issues/4868) - Birthday is displayed incorrectly, when using a UTC - XX:XX Time
* [NEXT-38432](https://github.com/shopware/shopware/issues/4863) - \[Github] feat: add criteria events for country and country state routes
* [NEXT-38425](https://github.com/shopware/shopware/issues/4853) - \[Github] Fix newsletter optin by head request
* [NEXT-38424](https://github.com/shopware/shopware/issues/4854) - \[Github] refactor: Cleanup product media image sorting
* [NEXT-38423](https://github.com/shopware/shopware/issues/4852) - \[Github] refactor: Remove unneeded mediaFolder association
* [NEXT-38415](https://github.com/shopware/shopware/issues/4817) - Permission "system.plugin\_maintain" is not possible to assign to a role in Cloud Shops
* [NEXT-38409](https://github.com/shopware/shopware/issues/4813) - Missing translations in sw-snippet-field-edit-modal because of limitation
* [NEXT-38407](https://github.com/shopware/shopware/issues/4811) - Side crash through old review-item.html.twig
* [NEXT-38393](https://github.com/shopware/shopware/issues/4796) - Subscription order generation does not use unique ids
* [NEXT-38388](https://github.com/shopware/shopware/issues/4794) - Import/Export: Import deletes all custom fields if CSV column is empty
* [NEXT-38383](https://github.com/shopware/shopware/issues/4792) - Search option ‘Best results’ missing in Admin
* [NEXT-38358](https://github.com/shopware/shopware/issues/4768) - \[Github] NEXT-00000 - Allow admin-search to get aborted by new request
* [NEXT-38331](https://github.com/shopware/shopware/issues/4747) - Password reset breaks with non-valid mail address
* [NEXT-38326](https://github.com/shopware/shopware/issues/4593) - Shopware Commercial plugin gives SCSS compile errors when using @StorefrontBootstrap
* [NEXT-38323](https://github.com/shopware/shopware/issues/4733) - Rule "is not equal to any of" excludes non-variant products
* [NEXT-38306](https://github.com/shopware/shopware/issues/4722) - \[Github] fix deprecation warning
* [NEXT-38292](https://github.com/shopware/shopware/issues/4720) - Unnecessary and incorrect association loading in CheckoutRegisterPageLoader
* [NEXT-38273](https://github.com/shopware/shopware/issues/4712) - Import/ Export error on import "Value is not a valid UUID: en-GB"
* [NEXT-38266](https://github.com/shopware/shopware/issues/4706) - Not possible to create a notification with more than 255 characters.
* [NEXT-38243](https://github.com/shopware/shopware/issues/4691) - \[Github] fix: Shopping experience demo entity loading
* [NEXT-38241](https://github.com/shopware/shopware/issues/4690) - \[Github] \[NEXT-0000] Allow customFields on mapping on newsletter\_recipient
* [NEXT-38234](https://github.com/shopware/shopware/issues/4683) - Improve display mode options in CMS image elements
* [NEXT-38229](https://github.com/shopware/shopware/issues/4680) - Unknown field "Shopware\Core\Framework\DataAbstractionLayer\Field\DateIntervalField" in Entity Generator
* [NEXT-38226](https://github.com/shopware/shopware/issues/4677) - \[Github] refactor: Deprecate `legacy` format of `system:config:get` command
* [NEXT-38207](https://github.com/shopware/shopware/issues/4663) - Taxes are not properly rounded with multiple taxRules
* [NEXT-38137](https://github.com/shopware/shopware/issues/4626) - \[Github] NEXT-00000 - Fix product category selection unchecked
* [NEXT-38116](https://github.com/shopware/shopware/issues/4614) - Paused subscriptions do not reactivate automatically
* [NEXT-38112](https://github.com/shopware/shopware/issues/4611) - Promotion - cart discount with rule not possible in promotion-tab
* [NEXT-38063](https://github.com/shopware/shopware/issues/3575) - Wrong currency on past order view in account
* [NEXT-38056](https://github.com/shopware/shopware/issues/4570) - No page numbers in the subscription overview
* [NEXT-38053](https://github.com/shopware/shopware/issues/4567) - routerLink overrides @click function in vue block
* [NEXT-38052](https://github.com/shopware/shopware/issues/4565) - \[Github] Fix include of address actions
* [NEXT-38051](https://github.com/shopware/shopware/issues/4564) - \[Github] Fix: Add missing Twig dependency to StorefrontControllerGenerator
* [NEXT-38049](https://github.com/shopware/shopware/issues/4561) - Admin view category select; Scrolling
* [NEXT-38048](https://github.com/shopware/shopware/issues/4560) - ProductPage::getCrossSellings() TypeError
* [NEXT-38027](https://github.com/shopware/shopware/issues/4546) - Custom date fields are not saved when date is entered manual
* [NEXT-37979](https://github.com/shopware/shopware/issues/2955) - sw-number-field unexpected behavior on input and key up/down
* [NEXT-37978](https://github.com/shopware/shopware/issues/2966) - After admin logout of inactive users (NEXT-24677) various workers - e.g. notification pull are still running and produce a lot of errors - 401 for API and notification bubbles
* [NEXT-37900](https://github.com/shopware/shopware/issues/3568) - Invalid RegEx in DefinitionValidator

## Credits

* [tinect](https://github.com/tinect)
* [raffaelecarelle](https://github.com/raffaelecarelle)
* [aragon999](https://github.com/aragon999)
* [PheysX](https://github.com/PheysX)
* [niklaswolf](https://github.com/niklaswolf)
* [wannevancamp](https://github.com/wannevancamp)
* [null](https://github.com/null)
* [akf-bw](https://github.com/akf-bw)
* [raphael-homann](https://github.com/raphael-homann)
* [wexoag](https://github.com/wexoag)
* [lacknere](https://github.com/lacknere)
* [Schrank](https://github.com/Schrank)
* [iNaD](https://github.com/iNaD)
* [panakour](https://github.com/panakour)

Thanks to all diligent friends for helping us make Shopware better and better with each pull request!

## More resources

* [Detailed diff on Github](https://github.com/shopware/shopware/compare/v6.6.6.1...v6.6.7.0) to the former version
* [Changelog on GitHub](https://github.com/shopware/shopware/blob/v6.6.7.0/CHANGELOG.md) for this version
* [Release News on corporate blog](https://www.shopware.com/en/news/shopware-6-release-news-october-2024/)
* [Installation overview](https://developer.shopware.com/docs/guides/installation/)
* [Update from a previous installation](https://developer.shopware.com/docs/guides/installation/template.html#update-shopware)

## Get in touch

Discuss about decisions, bugs you might stumble upon, etc in our [community slack](https://shopwarecommunity.slack.com/). See you there ;)

---

---

## Release notes Shopware 6.6.7.1
**Source:** [release-notes/6.6/6.6.7.1.md](https://developer.shopware.com/release-notes/6.6/6.6.7.1.md)  
# Release notes Shopware 6.6.7.1

## Abstract

This patch release contains just one bug fix.

## System requirements

* tested on PHP 8.2 and 8.3
* tested on MySQL 8.0.33, MariaDB 10.11 & 11.0

## Fixed bugs

* [#5243](https://github.com/shopware/shopware/issues/5243) | \[Github] Fix WriteCommandQueue command order

## Credits

* [Benjamin Wittwer](https://github.com/akf-bw)

Thanks to all diligent friends for helping us make Shopware better and better with each pull request!

## More resources

* [Detailed diff on Github](https://github.com/shopware/shopware/compare/v6.6.7.0...v6.6.7.1) to the former version
* [Changelog on GitHub](https://github.com/shopware/shopware/blob/v6.6.7.1/CHANGELOG.md) for this version.
* [Installation overview](https://developer.shopware.com/docs/guides/installation/)
* [Update from a previous installation](https://developer.shopware.com/docs/guides/installation/template.html#update-shopware)

## Get in touch

Discuss about decisions, bugs you might stumble upon, etc in our [community slack](https://slack.shopware.com). See you there ;)

---

---

## Release notes Shopware 6.6.8.0
**Source:** [release-notes/6.6/6.6.8.0.md](https://developer.shopware.com/release-notes/6.6/6.6.8.0.md)  
# Release notes Shopware 6.6.8.0

## Abstract

This minor release contains several improvements like in redis configuration, category and product indexing as well as the introduction of pinia in admin menu. Additionally, 50+ bugs have been fixed.

## System requirements

* tested on PHP 8.2 and 8.3
* tested on MySQL 8 and MariaDB 10.11

## Improvements

### Improve Redis configuration for platform

Redis is used in different places of Shopware, like cache, increments/locks/number ranges/messenger statistics.

To make it easier to configure and to have a better overview of the configuration, we improved the Redis configuration structure. There are few breaking changes, so please check the [changelog entry](https://github.com/shopware/shopware/blob/997d9c7fbf8848d623e4eff4aaa95d4fad16e130/changelog/_unreleased/2024-10-04-improved-redis-config-structure.md) for more information.

### Improve category and product indexing for many entities at once

To prevent exceeding the message size limit when indexing many entities at once, we improved the indexing process to split the entities into smaller chunks.

### Migrate admin-menu.store to pinia

The `adminMenu` store has been migrated from Vuex to Pinia. The store is now available as a Pinia store and can be accessed via `Shopware.Store.get(‘adminMenu’)`.

### Added support for opensearch sigv4 credential provider

We added the support for authentication with AWS OpenSearch using the SigV4 credential provider

### Added interface to support copy in batches

As a manufacturer of a flysystem adapter I want to be able to use the writeBatch-possibilities with a dedicated Interface until flysystem supports it out-of-the-box.

### Added vue to shopware object

## Fixed bugs

* [NEXT-39267](https://github.com/shopware/shopware/issues/5287) - \[Github] Fix styling input groups
* [NEXT-39224](https://github.com/shopware/shopware/issues/5248) - \[Github] Remove deprecation of AppSystemTestBehaviour
* [NEXT-39183](https://github.com/shopware/shopware/issues/5221) - \[Github] Remove @internal flag from ids collection
* [NEXT-39169](https://github.com/shopware/shopware/issues/5192) - \[Github] Removed abstract declaration from StoreApiResponse class
* [NEXT-39159](https://github.com/shopware/shopware/issues/5183) - \[Github] Use constant from parent class in InstallServicesTask.php
* [NEXT-39100](https://github.com/shopware/shopware/issues/5160) - \[Github] NEXT-0000: Remove @internal state from Defaults.php
* [NEXT-39065](https://github.com/shopware/shopware/issues/5154) - \[Github] Fix wrong invalid class
* [NEXT-39044](https://github.com/shopware/shopware/issues/5148) - Last line item of order can be deleted, leading to incorrect order total
* [NEXT-38982](https://github.com/shopware/shopware/issues/5122) - \[Github] Fix watch storefront multi saleschannel with multi theme
* [NEXT-38948](https://github.com/shopware/shopware/issues/5117) - \[Github] Fix imitate customer button
* [NEXT-38884](https://github.com/shopware/shopware/issues/5094) - \[Github] Fix typo in CartCalculator
* [NEXT-38856](https://github.com/shopware/shopware/issues/5084) - \[Github] Improve context switch route. Enable cache hash event
* [NEXT-38826](https://github.com/shopware/shopware/issues/5072) - \[Github] Add new console command "cache:clear:all" using shopware CacheClearer component
* [NEXT-38816](https://github.com/shopware/shopware/issues/5058) - Pinch-To-Zoom gesture leads to lightbox bug
* [NEXT-38808](https://github.com/shopware/shopware/issues/5050) - \[Github] Dispatch Address Validation Events With Correct Name In CheckoutConfirmPageLoader
* [NEXT-38751](https://github.com/shopware/shopware/issues/5004) - \[Github] Bugfix/select all inputs
* [NEXT-38727](https://github.com/shopware/shopware/issues/4997) - \[Github] Static plugins improvement
* [NEXT-38726](https://github.com/shopware/shopware/issues/4996) - \[Github] Removed non-existent argument from pre-commit ecs-fix
* [NEXT-38725](https://github.com/shopware/shopware/issues/4995) - \[Github] chore: Add native return type to subscriber
* [NEXT-38717](https://github.com/shopware/shopware/issues/4978) - "Product" number range cannot be created
* [NEXT-38713](https://github.com/shopware/shopware/issues/4970) - \[Github] Just apply filters of the criteria builder to build the sync criteria
* [NEXT-38701](https://github.com/shopware/shopware/issues/4955) - \[Github] Fix Typo('s) in PR Template
* [NEXT-38700](https://github.com/shopware/shopware/issues/4954) - \[Github] refactor: Changed database:create-migration command to not create Package attribute
* [NEXT-38696](https://github.com/shopware/shopware/issues/4945) - Pages can show content from a logged in session
* [NEXT-38695](https://github.com/shopware/shopware/issues/4943) - Return is not changing status in the UI
* [NEXT-38653](https://github.com/shopware/shopware/issues/4928) - \[Github] Fix cms form reset on failed ajax form submission
* [NEXT-38579](https://github.com/shopware/shopware/issues/4919) - customFields of lineItem is deleted when using discount
* [NEXT-38557](https://github.com/shopware/shopware/issues/4918) - \[Github] fix: Do not fail on country change if no labels are present
* [NEXT-38556](https://github.com/shopware/shopware/issues/4917) - \[Github] Changed the JSON-LD schema links to use https instead of http
* [NEXT-38535](https://github.com/shopware/shopware/issues/4914) - Properties in product detail page are sorted randomly
* [NEXT-38504](https://github.com/shopware/shopware/issues/4896) - Missing block in Administration
* [NEXT-38427](https://github.com/shopware/shopware/issues/4855) - \[Github] NEXT-00000 - Sort sales channels in product visibility selection
* [NEXT-38411](https://github.com/shopware/shopware/issues/4815) - Create new order from customer page does not select current customer
* [NEXT-38410](https://github.com/shopware/shopware/issues/4814) - Define filter - Layouts
* [NEXT-38383](https://github.com/shopware/shopware/issues/4792) - Search option ‘Best results’ missing in Admin
* [NEXT-38382](https://github.com/shopware/shopware/issues/4791) - cmsPage association doesn't work in category list endpoint
* [NEXT-38341](https://github.com/shopware/shopware/issues/4752) - Multiple documents can be created via bulk edit
* [NEXT-38288](https://github.com/shopware/shopware/issues/4718) -  Prices, end with a € stamp, but should PLN.
* [NEXT-38259](https://github.com/shopware/shopware/issues/4702) - Base Slider display error when swipe back on Mobile (touch)
* [NEXT-38225](https://github.com/shopware/shopware/issues/4676) - Customer is created despite error
* [NEXT-38104](https://github.com/shopware/shopware/issues/4601) - LoadProductStockSubscriber gets loaded after ProductMaxPurchaseCalculator

## Credits

* [wannevancamp](https://github.com/wannevancamp)
* [null](https://github.com/null)
* [OliverSkroblin](https://github.com/OliverSkroblin)
* [tinect](https://github.com/tinect)
* [ablazejuk](https://github.com/ablazejuk)
* [jasperP98](https://github.com/jasperP98)
* [raffaelecarelle](https://github.com/raffaelecarelle)
* [akf-bw](https://github.com/akf-bw)
* [JoshuaBehrens](https://github.com/JoshuaBehrens)
* [alessandroaussems](https://github.com/alessandroaussems)
* [miljkovic5](https://github.com/miljkovic5)
* [aragon999](https://github.com/aragon999)
* [hype09](https://github.com/hype09)
* [niklaswolf](https://github.com/niklaswolf)
* [M-arcus](https://github.com/M-arcus)

Thanks to all diligent friends for helping us make Shopware better and better with each pull request!

## More resources

* [Detailed diff on Github](https://github.com/shopware/shopware/compare/v6.6.7.1...v6.6.8.0) to the former version
* [Changelog on GitHub](https://github.com/shopware/shopware/blob/v6.6.8.0/CHANGELOG.md) for this version
* [Release News on corporate blog](https://www.shopware.com/en/news/shopware-6-release-news-november-2024/)
* [Installation overview](https://developer.shopware.com/docs/guides/installation/)
* [Update from a previous installation](https://developer.shopware.com/docs/guides/installation/template.html#update-shopware)

## Get in touch

Discuss about decisions, bugs you might stumble upon, etc in our [community slack](https://shopwarecommunity.slack.com/). See you there ;)

---

---

## Release notes Shopware 6.6.8.1
**Source:** [release-notes/6.6/6.6.8.1.md](https://developer.shopware.com/release-notes/6.6/6.6.8.1.md)  
# Release notes Shopware 6.6.8.1

## Abstract

This patch release contains just one bug fix.

## System requirements

* tested on PHP 8.2 and 8.3
* tested on MySQL 8.0.33, MariaDB 10.11 & 11.0

## Fixed bugs

* [NEXT-39321](https://github.com/shopware/shopware/blob/v6.6.8.1/changelog/release-6-6-8-1/2024-10-29-fix-cookie-issue-and-follow-redirect-in-hot-reload.md) | Fix cookie issue and follow redirect in HOT reload

## More resources

* [Detailed diff on Github](https://github.com/shopware/shopware/compare/v6.6.8.0...v6.6.8.1) to the former version
* [Changelog on GitHub](https://github.com/shopware/shopware/blob/v6.6.8.1/CHANGELOG.md) for this version.
* [Installation overview](https://developer.shopware.com/docs/guides/installation/)
* [Update from a previous installation](https://developer.shopware.com/docs/guides/installation/template.html#update-shopware)

## Get in touch

Discuss about decisions, bugs you might stumble upon, etc in our [community slack](https://slack.shopware.com). See you there ;)

---

---

## Release notes Shopware 6.6.8.2
**Source:** [release-notes/6.6/6.6.8.2.md](https://developer.shopware.com/release-notes/6.6/6.6.8.2.md)  
# Release notes Shopware 6.6.8.2

## Abstract

This patch release contains several bug fixes.

## System requirements

* tested on PHP 8.2 and 8.3
* tested on MySQL 8.0.33, MariaDB 10.11 & 11.0

## Fixed bugs

* [NEXT-39484](https://github.com/shopware/shopware/issues/5423) - \[Github] NEXT-00000 - Allow activating staging mode via console with no interaction
* [NEXT-39449](https://github.com/shopware/shopware/issues/5409) - \[Github] fix: Do not use deprecated method in Twig rendering
* [NEXT-38947](https://github.com/shopware/shopware/issues/5115) - Default "not\_specified" salutation is invalid
* [NEXT-37335](https://github.com/shopware/shopware/issues/4411) - Change / suggest new password >wrong fields are filled

## Credits

* [M-arcus](https://github.com/M-arcus)
* [aragon999](https://github.com/aragon999)
* [null](https://github.com/null)

Thanks to all diligent friends for helping us make Shopware better and better with each pull request!

## More resources

* [Detailed diff on Github](https://github.com/shopware/shopware/compare/v6.6.8.1...v6.6.8.2) to the former version
* [Changelog on GitHub](https://github.com/shopware/shopware/blob/v6.6.8.2/CHANGELOG.md) for this version.
* [Installation overview](https://developer.shopware.com/docs/guides/installation/)
* [Update from a previous installation](https://developer.shopware.com/docs/guides/installation/template.html#update-shopware)

## Get in touch

Discuss about decisions, bugs you might stumble upon, etc in our [community slack](https://slack.shopware.com). See you there ;)

---

---

## Release notes Shopware 6.6.9.0
**Source:** [release-notes/6.6/6.6.9.0.md](https://developer.shopware.com/release-notes/6.6/6.6.9.0.md)  
# Release notes Shopware 6.6.9.0

## Abstract

This minor release contains some interesting features as well as technical improvements like Accessibility improvements and OpenTelemetry enhancements.

## System requirements

* tested on PHP 8.2 and 8.3
* tested on MySQL 8 and MariaDB 10.11

## Improvements

### Improve category and product indexing for many entities at once

Before the CategoryIndexer, every child of the to-be-updated categories was put into one indexing message.
This single message could stay within the message size limit if there are fewer categories.
The children and parents are now chunked and put into new messages.

### Fill the last\_usage\_at column in the integration table during the authentication process between the App/Service and the Shop.

The last\_usage\_at date is now filled when an integration is used.

### Public metrics configuration interfaces

Changed parts of the future public interface (metrics emitting view and metrics transport view) from @internal to @experimental

### Add global exports to Shopware object

Added all Vue exports to `Shopware.Vue`

### Hot Reload: Support for Multiple Themes (SCSS Variables)

Improved support for multiple themes by skipping unselected themes during Hot Reload

### Custom Field Integration in Layouts

Merchants can now use custom field data in layouts. Updates to custom fields automatically reflect across all layouts, reducing manual updates. This includes:

* Selecting entities in data mapping.
* Using custom field data as variables in text fields and entire blocks.

### Elasticsearch Search Explanation

Added the ability to view search explanations in the browser's network tab when using the preview search API, integrated with the Preview search UI.

### Exclude products from sitemap

Added the option to exclude hidden products from the sitemap.

### Accessibility improvements

A bypass mechanism was implemented to enhance site navigation by providing ARIA landmarks, internal skip links, and headlines for site areas.
Additionally, accessible names for `<iframe>` elements were added, and methods such as collapsible sections and labeled landmarks were recommended to improve usability for screen reader and keyboard-only users.

## Fixed bugs

* [NEXT-39764](https://github.com/shopware/shopware/issues/5669) - Cloud Very long loading & crash from website with many promotion codes
* [NEXT-39724](https://github.com/shopware/shopware/issues/5642) - Major Break: Theme dump command
* [NEXT-39714](https://github.com/shopware/shopware/issues/5626) - \[Github] fix(storefront): update review language property according to schema.org
* [NEXT-39678](https://github.com/shopware/shopware/issues/5524) - "Set as default billing/shipping address" in checkout is broken
* [NEXT-39646](https://github.com/shopware/shopware/issues/5509) - A11y: B2B Components lack descriptive page titles
* [NEXT-39611](https://github.com/shopware/shopware/issues/5498) - \[Github] Update `MessageQueueSizeRestrictListener` to skip on `enforceLimit = false`
* [NEXT-39609](https://github.com/shopware/shopware/issues/5496) - \[Github] Allow to specify entity collection for attributed entities
* [NEXT-39608](https://github.com/shopware/shopware/issues/5495) - \[Shopware 6.6.8.0] start-hot-reload fix destroys ddev watcher
* [NEXT-39606](https://github.com/shopware/shopware/issues/5494) - \[Github] Allow to specify custom field types for attributed entities
* [NEXT-39597](https://github.com/shopware/shopware/issues/5485) - \[Github] Update `.gitignore` to exclude the `.vscode` folder except `settings.json`
* [NEXT-39594](https://github.com/shopware/shopware/issues/5484) - \[Github] fix: correct config-schema.json to match properties of usage\_data
* [NEXT-39542](https://github.com/shopware/shopware/issues/5460) - \[Github] Fix symfony scheduler bridge
* [NEXT-39527](https://github.com/shopware/shopware/issues/5455) - \[Github] Fix - delivery address editing during order creation saving leads to Axios error
* [NEXT-39519](https://github.com/shopware/shopware/issues/5450) - \[Github] NEXT-38174 If no label set in a custom fields option, the technical name will be displayed #4641
* [NEXT-39515](https://github.com/shopware/shopware/issues/5447) - \[Github] Update UPGRADE-6.5.md
* [NEXT-39513](https://github.com/shopware/shopware/issues/5445) - \[Github] feat: removed sizes from the meta apple-touch-icon
* [NEXT-39512](https://github.com/shopware/shopware/issues/5444) - sw-string-filter: Add types `equalsAny`, `prefix` and `suffix`
* [NEXT-39495](https://github.com/shopware/shopware/issues/5429) - \[Github] Fix / Improve promotion help texts
* [NEXT-39483](https://github.com/shopware/shopware/issues/5422) - \[Github] Reuse product slider stream collect criteria
* [NEXT-39462](https://github.com/shopware/shopware/issues/5416) - \[Github] Fix administration promotion detail bugs
* [NEXT-39448](https://github.com/shopware/shopware/issues/5408) - Administration not all helpers are exposed
* [NEXT-39419](https://github.com/shopware/shopware/issues/5387) - \[Github] Remove duplicate gad\_source from ignored parameter list
* [NEXT-39418](https://github.com/shopware/shopware/issues/5386) - \[Github] NEXT-00000 - Prevent product being loaded in own cross selling product streams
* [NEXT-39417](https://github.com/shopware/shopware/issues/5385) - \[Github] Fix incorrect measures & packaging field types in product bulk edit
* [NEXT-39416](https://github.com/shopware/shopware/issues/5384) - \[Github] fix: Remove cover of product line item if media has been deleted
* [NEXT-39414](https://github.com/shopware/shopware/issues/5389) - Promotion applies even though the conditions do not apply
* [NEXT-39405](https://github.com/shopware/shopware/issues/5382) - \[Github] Added extension point for pdf renderer
* [NEXT-39387](https://github.com/shopware/shopware/issues/5371) - Cannot Modify Snippet on second modification
* [NEXT-39349](https://github.com/shopware/shopware/issues/5355) - Fixed Tax Calculation Not Applied to Shipping Method
* [NEXT-39314](https://github.com/shopware/shopware/issues/5322) - Product export from the Product comparison sales channel doesn't run

## Credits

* [Scarbous](https://github.com/Scarbous)
* [null](https://github.com/null)
* [lacknere](https://github.com/lacknere)
* [aragon999](https://github.com/aragon999)
* [sjerdo](https://github.com/sjerdo)
* [jankal](https://github.com/jankal)
* [akf-bw](https://github.com/akf-bw)
* [nickygerritsen](https://github.com/nickygerritsen)
* [tinect](https://github.com/tinect)
* [schneider-felix](https://github.com/schneider-felix)
* [LunaDotGit](https://github.com/LunaDotGit)
* [nextflex](https://github.com/nextflex)
* [wannevancamp](https://github.com/wannevancamp)
* [M-arcus](https://github.com/M-arcus)
* [timtheisinger](https://github.com/timtheisinger)
* [OliverSkroblin](https://github.com/OliverSkroblin)

Thanks to all diligent friends for helping us make Shopware better and better with each pull request!

## More resources

* [Detailed diff on Github](https://github.com/shopware/shopware/compare/v6.6.8.2...v6.6.9.0) to the former version
* [Changelog on GitHub](https://github.com/shopware/shopware/blob/v6.6.9.0/CHANGELOG.md) for this version
* [Release News on corporate blog](https://www.shopware.com/en/news/shopware-6-release-news-december-2024/)
* [Installation overview](https://developer.shopware.com/docs/guides/installation/)
* [Update from a previous installation](https://developer.shopware.com/docs/guides/installation/template.html#update-shopware)

## Get in touch

Discuss about decisions, bugs you might stumble upon, etc in our [community slack](https://shopwarecommunity.slack.com/). See you there ;)

---

---

## Release notes Shopware 6.7.0.0
**Source:** [release-notes/6.7/6.7.0.0.md](https://developer.shopware.com/release-notes/6.7/6.7.0.0.md)  
*(Body truncated in this bundle; follow the link for the rest.)*

# Release notes Shopware 6.7.0.0

## Abstract

Shopware 6.7.0.0 is a major release containing breaking changes.
Please read this document and the linked resources carefully.

This release was built with the help of the community. Thanks for supporting us with pull requests (code contributions) and during the RC phase by providing feedback and testing the release under production-like conditions.

Please note that with this release, marked as stable, the major series v6.5 will not be provided with extended maintenance and support any longer. Instead, the series v6.6 will become the new "extended support" version from now on.
[Release Policy](https://developer.shopware.com/release-notes/)

The Shopware 6.7.0.0 release is focused on core changes instead of features. It provides a foundation for adding new features throughout future minor releases.

## System requirements

* tested on PHP 8.2 and 8.4
* tested on MySQL 8 and MariaDB 11

See below for more information on the current minimum versions.

## Improvements

### Webpack to vite migration for the administration

We are switching the build system for our administration from webpack to vite. This means that when your plugins depends on a custom `webpack.config.js` file, you'll need to migrate it to a `vite.config.js` file.

Additionally, this means that you will need to distribute a separate plugin version starting for 6.7, when you extend the administration to distribute the correct build files.
For more information please take a look at the [docs](https://developer.shopware.com/docs/guides/plugins/plugins/administration/system-updates/vite.html).

### Removal of Vue 2 compatibility layer

The Vue 2 compatibility layer has been removed from the administration. This means that all components that still rely on Vue 2 features need to be updated. This ensures that our administration stays future-proof and we can make use of the most recent Vue 3 features.

For detailed explanation of what was covered by the compatibility layer and what needs to be updated, please refer to the [Vue docs](https://v3-migration.vuejs.org/migration-build.html).

### Migration from Vuex to Pinia

For Vue 3, the default state management library has become Pinia, therefore we are migrating from Vuex to Pinia, to stay as close to the default as possible. When you use default stores in your plugin you need to switch from `Shopware.State` (Vuex) to `Shopware.Store` (Pinia).
Adding your own Vuex stores is still possible, however it is recommended that you switch to Pinia as well.

### Vuex breaking change

Due to the migration from Vuex to Pinia, the Vuex helper utils have been renamed to avoid conflicts with Pinia helpers. If you are still using Vuex, please update your code accordingly:

```
    mapState -> mapVuexState
    mapMutations -> mapVuexMutations
    mapGetters -> mapVuexGetters
    mapActions -> mapVuexActions
```

For more information refer to the [docs](https://developer.shopware.com/docs/resources/references/adr/2024-06-17-replace-vuex-with-pinia.html#replace-vuex-with-pinia).

### vue-i18n v10 Update

We have updated `vue-i18n` to version 10, which introduces a significant change by removing the `tc` function. In Shopware, `$tc` remains available on Vue components, but it now internally references the `t` function from `vue-i18n`.

* While this change works for most use cases, some specific function overloads are no longer supported.
* For a comprehensive list of deprecated features and migration strategies, refer to the official [vue-i18n migration guide](https://vue-i18n.intlify.dev/guide/migration/breaking10#deprecate-tc-and-tc-for-legacy-api-mode).

Please review your existing translation calls, test components that heavily rely on translation methods and consider updating to the recommended `t` function where possible.

### Cache Rework

#### Delayed Cache Invalidation

The cache invalidation will be delayed by default. This means that the cache will be invalidated in regular intervals and not immediately. This will lead to better cache hit rates and way less (duplicated) cache invalidations, which will improve efficiency and scalability of the system. As this feature is now active by default, the previous `shopware.cache.invalidation.delay` configuration has been removed.

The default interval is 5 mins and can be changed by adjusting the run interval of the `shopware.invalidate_cache` scheduled task.

### Removal of Store-API route caching

The Store-API route caching has been removed. This means that the `Cached*Route` classes will be removed. This solves some weird states when the HTTP-Cache was invalidated separately from the route cache. Additionally, the cache hit rate for the Store-API was low, so the performance impact should be minimal, but the amount of cache items and cache invalidations will be reduced. This overall should lead to more effective cache resource usage.

### Introduction of ESI for header and footer

The header and footer are now loaded via ESI.
This allows to cache the header and footer separately from the rest of the page. Two new routes `\header` and `\footer` were added to receive the rendered header and footer.

The rendered header and footer are included into the page with the Twig function `render_esi`, which calls the previously mentioned routes.
Two new templates `src/Storefront/Resources/views/storefront/layout/header.html.twig` and `src/Storefront/Resources/views/storefront/layout/footer.html.twig` were introduced as new entry points for the header and footer.
Make sure to adjust your template extensions to be compatible with the new structure.

The block names are still the same, so it might become necessary to extend from the new templates.

### Major Library Updates

We upgraded the following libraries to their latest versions:

* [DBAL 4.x](https://github.com/doctrine/dbal/blob/4.2.5/UPGRADE.md#upgrade-to-40): When you are using DBAL directly, please check the upgrade guide.
* [PHPUnit 11.x](https://github.com/sebastianbergmann/phpunit/blob/11.0.0/ChangeLog-11.0.md#1100---2024-02-02): You need to adjust your tests to the new PHPUnit version.
* [Dompdf 3.x](https://github.com/dompdf/dompdf/releases/tag/v3.0.0): Please check your document templates, if they are still rendered as expected.
* [oauth2-server 9.x](https://oauth2.thephpleague.com/upgrade-guide/): We don't expect you are affected by this change on the code level, however the library does not support some requests that are not spec-compliant, look at the detailed [upgrade guide](#non-spec-compliant-apioauthtoken-requests-are-not-supported-anymore).

### Accessibility Compliance

In alignment with the European Accessibility Act (EAA) we made significant accessibility improvements.

* Storefront **product box** accessibility: Removed duplicate links around the product image in product cards. Affected template: `Resources/views/storefront/component/product/card/box-standard.html.twig`.
* Storefront **base font-size**: The base font-size of the storefront is updated to the browser standard of `1rem` (16px).
* Change Storefront **language and currency drop down items** to buttons: The `.top-bar-list-item` elements inside the "top-bar" dropdown menus will contain `<button>` elements instead of a hidden `<input type="radio">` elements.
* Change Storefront **order items and cart line-items** from `<div>` to `<ul>` and `<li>`: several generic `<div>` elements representing lists are changed to `<ul>` and `<li>` elements. This effects the account order overview area as well as the cart line-item templates.
* Storefront **pagination** is using anchor links instead of radio inputs
* Use `<button>` elements instead of `<a>` to **open modal windows**
* New **translation keys** with button modal triggers: Some modal triggers are inside translation texts. With 6.7 new translation keys are used that have buttons instead of links. There are also new translation parameters to avoid too much HTML and modal logic inside the translation strings.
* Storefront **icons** that are rendered via `{% sw_icon 'icon-name' %}` will apply `aria-hidden="true"` by default so they are hidden for screen readers. In most scenarios icons are of decorative nature and should therefore not be read as "graphic" by the screen reader.

More information regarding accessibility and the European Accessibility Act can be found in the [Shopware blog](https://www.shopware.com/en/news/accessible-online-store-by-2025/).

### Changed Functionality

Some functionality changed in a way that might be noticeable for merchants. Additionally, this means that changes over the administration (e.g. adjusting configured flows, mail templates) might be needed to adjust to the new behavior.

#### Vat Ids will be validated case sensitive

Vat Ids will now be checked for case sensitivity, which means that most Vat Ids will now have to be upper case, depending on their validation pattern.
For customers without a company, this check will only be done on entry, so it is still possible to checkout with an existing lower case Vat Id.
For customers with a company, this check will be done at checkout, so they will need to change their Vat Id to upper case.

#### Custom field names and field set names validation

Custom field names and field set names will be validated to not contain hyphens or dots, they must be valid [Twig variable names](https://github.com/twigphp/Twig/blob/21df1ad7824ced2abcbd33863f04c6636674481f/src/Lexer.php#L46). Existing custom fields continue to work, however the validation will be enforced on new custom fields.

#### Removal of deprecated properties of `CustomerDeletedEvent`

The deprecated properties `customerId`, `customerNumber`, `customerEmail`, `customerFirstName`, `customerLastName`, `customerCompany` and `customerSalutationId` of `CustomerDeleteEvent` have finally been removed and cannot be accessed anymore in a mail template when sending a mail via the `Checkout > Customer > Deleted` flow trigger.

#### Rule builder: Condition `customerDefaultPaymentMethod` removed

* Removed condition `customerDefaultPaymentMethod` from rule builder, since customers do not have default payment methods anymore
* Existing rules with this condition will be automatically migrated to the new condition `paymentMethod`, so the currently selected payment method

#### Flow builder: Trigger `checkout.customer.changed-payment-method` removed

* Removed trigger `checkout.customer.changed-payment-method` from flow builder, since customers do not have default payment methods anymore
* Existing flows will be automatically disabled with Shopware 6.7 and removed in a future via destructive migration.

#### Direct debit default payment: State change removed

The default payment method "Direct debit" will no longer automatically change the order state to "in progress". Use the flow builder instead, if you want the same behavior.

#### New `technicalName` property for payment and shipping methods

The `technicalName` property is now required for payment and shipping methods in the API. The `technical_name` column have been made non-nullable for the `payment_method` and `shipping_method` tables in the database.

Plugin developers now must specify a `technicalName` for their payment and shipping methods. Please note: **If no technical name is specified before the migration is run, a temporary placeholder `temporary_<method-id>` will be used instead.**

Merchants must review their custom created payment and shipping methods for the new `technicalName` property and update their methods through the administration accordingly.

### API

We made some breaks in the API, which might affect your extensions or custom integrations.

#### Non spec-compliant /api/oauth/token requests are not supported anymore

Due to an upgrade of the "league/oauth2-server" library, some requests that are not spec-compliant with the OAuth spec are not supported anymore.
Especially scopes now needed to be provided as `scope` parameter a

… **Truncated.** Full document: https://developer.shopware.com/release-notes/6.7/6.7.0.0.md


---

## Release notes Shopware 6.7.0.1
**Source:** [release-notes/6.7/6.7.0.1.md](https://developer.shopware.com/release-notes/6.7/6.7.0.1.md)  
# Release notes Shopware 6.7.0.1

## Abstract

This patch release contains ~20 bug fixes.

## System requirements

* tested on PHP 8.2 and 8.4
* tested on MySQL 8 and MariaDB 11

## Improvements

(No notable improvements listed in v6.7.0.1)

## Fixed bugs

Find lists of fixed bugs here

* https://github.com/shopware/shopware/milestone/11?closed=1
* https://github.com/shopware/shopware/blob/v6.7.0.1/CHANGELOG.md#6701

## Credits

* no community contributions in this patch release

Thanks to all diligent friends for helping us make Shopware better and better with each pull request!

## More resources

* [Detailed diff on Github](https://github.com/shopware/shopware/compare/v6.7.0.0...v6.7.0.1) to the former version
* [Changelog on GitHub](https://github.com/shopware/shopware/blob/v6.7.0.1/CHANGELOG.md) for this version.
* [Installation overview](https://developer.shopware.com/docs/guides/installation/)
* [Update from a previous installation](https://developer.shopware.com/docs/guides/installation/template.html#update-shopware)

## Get in touch

Discuss about decisions, bugs you might stumble upon, etc in our [community discord](https://chat.shopware.com). See you there ;)

---

---

## Release notes Shopware 6.7.1.0
**Source:** [release-notes/6.7/6.7.1.0.md](https://developer.shopware.com/release-notes/6.7/6.7.1.0.md)  
# Release notes Shopware 6.7.1.0

## Abstract

This minor release comes with some interesting improvements such as switch between metric and imperial measurement system. Additionally, at least 11 bugs have been fixed. Many thanks to 25+ contributors!

## System requirements

* tested on PHP 8.2, 8.3 and 8.4
* tested on MySQL 8 and MariaDB 11

## Improvements

### Switch between metric and imperial unit system per Sales Channel

With this new option, you can now configure which measurement units should be displayed per sales channel and domain. You can now maintain product values in your preferred unit, and Shopware will automatically convert them to the appropriate unit for the respective domain or sales channel.

### Theme configuration changes

* Theme configuration used during storefront rendering is now stored in a `theme_runtime_config` table and regenerated on the refresh stage of theme lifecycle.
* The `\Shopware\Storefront\Theme\CachedResolvedConfigLoader` is now deprecated and will be removed in the next major version. Please update the code that directly uses it to use the `\Shopware\Storefront\Theme\ResolvedConfigLoader` instead.
* The `\Shopware\Storefront\Theme\Exception\ThemeAssignmentException` is now deprecated and will be removed in the next major version. Please use `\Shopware\Storefront\Theme\Exception\ThemeException::themeAssignmentException`.

### Measurement system units info are now provided in the store-api

The store API now provides the measurement system units info in the response of the `context` endpoint and `product` API endpoints depending on the configured measurement system of the sales channel domain.

*Note: The product's measurement units are still stored in the database in fixed units (kg/mm) and converted to the configured measurement units of the sales channel domain when reading or writing the product's measurement units.*

We added new request headers `sw-measurement-weight-unit` and `sw-measurement-length-unit` to allow clients to specify the measurement units for length and weight when reading or writing product's measurement units.

This is useful when the user can provide measurement units in the header and get the desired product's measurement units in the response. This also goes for writing the product's measurement units in the desired measurement units without convert the units back and forth.

### A generated robots.txt with adjustments from administration panel

This minor version comes with a generated robots.txt which can be adjusted and fine tuned from the admin panel.

![Adjust robots.txt from administration panel](assets/shopware-admin-robotstxt-settings.png)

Learn the full story and how to use it: <https://www.shopware.com/en/news/hacktoberfest-2024-outcome-a-robots-txt-for-shopware/>

### New twig filter to convert measurement units

For the storefront, we added a new twig filter `sw_convert_unit` to convert measurement units in twig templates. This allows the developers to convert measurement units in the templates without writing custom logic.

It allows the developers to convert measurement units of any value, any variable in the templates without writing custom logic.

Or they can also convert between any measurement units by passing the desired measurement unit as a parameter to the filter.

### Translation labels and helpTexts for Themes

A constructed snippet key was introduced in Shopware 6.7 and will be required starting 6.8. This affects `label` and `helpText` properties in the `theme.json`, which are used in the theme manager.

To provide translations for theme configuration, [creating administration snippets as usual](https://developer.shopware.com/resources/admin-extension-sdk/faq/#how-can-i-use-snippets-to-translate-my-app) will be mandatory.

The snippet keys to be used are constructed as follows. The mentioned `themeName` implies the `technicalName` property of the theme in kebab case. Also, please notice that unnamed tabs, blocks or sections will be accessible via `default`.

### ThemeConfiguration deprecations

* The `label` and `helpText` fields in the `/api/_action/theme/{themeId}/configuration` and in the
  `/api/_action/theme/{themeId}/structured-fields` API endpoints have been deprecated. For translations you should rely on
  the `labelSnippetKey` and `helpTextSnippetKey` fields instead (present only in the structured fields endpoint).
* The `ThemeService::getThemeConfiguration` and `ThemeService::getThemeConfigurationStructuredFields` methods have been deprecated in favor of the new `ThemeConfigurationService::getPlainThemeConfiguration` and
  `ThemeConfigurationService::getThemeConfigurationFieldStructure` methods. The new methods return the same data as the old ones,
  excluding the deprecated fields.

### Vue i18n Translation Functions

* The `$tc` function is deprecated and will be removed in v6.8.0
* Use `$t` function instead for all translations
* The `$tc` function now shows a deprecation warning when used with the feature flag `V6_8_0_0` enabled

### Primary delivery ordering and read-only cart extensions

The `OrderConverter` now explicitly moves the **primary order delivery** to the front of the deliveries list. This ensures legacy compatibility for existing usages of `$deliveries->first()`.
Two new cart extensions are introduced:

* `ORIGINAL_PRIMARY_ORDER_DELIVERY` – returns the originally determined primary order delivery.
* `ORIGINAL_PRIMARY_ORDER_TRANSACTION` – returns the originally determined primary order transaction.

These extensions serve as **informational only**: modifying them does **not** change the actual primary delivery or transaction set in the order.

### Custom field set name is now unique for apps

The `name` element of the `custom-field-set` in the app manifest is now unique per app. It should not be the case for your app anyway as it caused problems. However, you should check your app manifest and ensure that the `name` of the `custom-field-set` is unique.

### Deprecated configuration of visibility in config array

The visibility of filesystems should no longer be configured in the config array. Instead, it should be set on the same level as `type`. For example, instead of:

```yaml
filesystems:
  my_filesystem:
    type: local
    config:
      visibility: public
```

You should now use:

```yaml
filesystems:
  my_filesystem:
    type: local
    visibility: public
```

For more details, please see [UPGRADE-6.7.md](https://github.com/shopware/shopware/blob/6.7.1.0/UPGRADE-6.7.md#6710).

## Fixed bugs

* Translation for English (US) not working in Default Theme [#6601](https://github.com/shopware/shopware/issues/6601)
* SEO URLs are missing in footer navigation for landing pages [#3784](https://github.com/shopware/shopware/issues/3784)

See the entire list of fixed bugs:

* <https://github.com/shopware/shopware/milestone/8?closed=1>

## Credits

* [Stefan Poensgen](https://github.com/stefanpoensgen)
* [Felix Schneider](https://github.com/schneider-felix)
* [Marvin](https://github.com/marvn-r3)
* [Oliver Skroblin](https://github.com/OliverSkroblin)
* [Max](https://github.com/aragon999)
* [Wanne Van Camp](https://github.com/wannevancamp)
* [thuong-le](https://github.com/thuong-le)
* [Benjamin Wittwer](https://github.com/gecolay)
* [Justus Geramb](https://github.com/jgeramb)
* [Elias Lackner](https://github.com/lacknere)
* [acris-lf](https://github.com/acris-lf)
* [Lukas Völler](https://github.com/LukasVoeller)
* [Marcus Müller](https://github.com/M-arcus)
* [jasperP98](https://github.com/jasperP98)
* [tinect](https://github.com/tinect)
* [Fayti1703](https://github.com/Fayti1703)
* [Sascha Heilmeier](https://github.com/Scarbous)
* [Lee Nguyen](https://github.com/nguyenquocdaile)
* [Vladislav Sultanov](https://github.com/TheBreaken)
* [Melvin Achterhuis](https://github.com/MelvinAchterhuis)
* [wbm-sbasler](https://github.com/wbm-sbasler)
* [Benedikt Schulze Baek](https://github.com/bschulzebaek)
* [Philip Standt](https://github.com/Ocarthon)
* [Stefan Reichelt](https://github.com/Songworks)
* [Hannes Wernery](https://github.com/hanneswernery)
* [Bjoern Herzke](https://github.com/wrongspot)

Thanks to all our contributors for helping us improve Shopware with every pull request!

## More resources

* [Detailed diff on Github](https://github.com/shopware/shopware/compare/v6.7.0.1...v6.7.1.0) to the former version
* [Changelog on GitHub](https://github.com/shopware/shopware/blob/v6.7.1.0/CHANGELOG.md) for this version.
* [Release News on corporate blog](https://www.shopware.com/en/news/shopware-6-release-news-july-2025/)
* [UPGRADE-6.7.md](https://github.com/shopware/shopware/blob/6.7.1.0/UPGRADE-6.7.md#6710)
* [Installation overview](https://developer.shopware.com/docs/guides/installation/)
* [Update from a previous installation](https://developer.shopware.com/docs/guides/installation/template.html#update-shopware)

## Get in touch

Discuss about decisions, bugs you might stumble upon, etc in our [community discord](https://discord.gg/ncfNP3xT). See you there ;)

---

---

## Release notes Shopware 6.7.1.1
**Source:** [release-notes/6.7/6.7.1.1.md](https://developer.shopware.com/release-notes/6.7/6.7.1.1.md)  
# Release notes Shopware 6.7.1.1

## Abstract

This patch release contains just bug fixes.

## System requirements

* tested on PHP 8.2, 8.3 and 8.4
* tested on MySQL 8 and MariaDB 11

## Improvements

(No notable improvements listed in v6.7.1.1)

## Fixed bugs

* [#11483](https://github.com/shopware/shopware/issues/11483) - Don't check for canonical SEO Urls when no path info given during SEO URL creation
* [#11513](https://github.com/shopware/shopware/issues/11513) - Fix ThemeLifecycleService refreshThemes being executed without plugin configurations
* [#11518](https://github.com/shopware/shopware/issues/11518) - Fix corruption of ThemeRuntimeConfig by theme:compile

## Credits

* [Marcus Müller](https://github.com/M-arcus)
* [Benjamin Wittwer](https://github.com/gecolay)

Thanks to all diligent friends for helping us make Shopware better and better with each pull request!

## More resources

* [Detailed diff on Github](https://github.com/shopware/shopware/compare/v6.7.1.0...v6.7.1.1) to the former version
* [Changelog on GitHub](https://github.com/shopware/shopware/blob/v6.7.1.1/CHANGELOG.md) for this version.
* [Installation overview](https://developer.shopware.com/docs/guides/installation/)
* [Update from a previous installation](https://developer.shopware.com/docs/guides/installation/template.html#update-shopware)

## Get in touch

Discuss about decisions, bugs you might stumble upon, etc in our [community discord](https://chat.shopware.com). See you there ;)

---

---

## Release notes Shopware 6.7.1.2
**Source:** [release-notes/6.7/6.7.1.2.md](https://developer.shopware.com/release-notes/6.7/6.7.1.2.md)  
# Release notes Shopware 6.7.1.2

## Abstract

This patch release contains just bug fixes.

## System requirements

* tested on PHP 8.2, 8.3 and 8.4
* tested on MySQL 8 and MariaDB 11

## Improvements

(No notable improvements listed in v6.7.1.2)

## Fixed bugs

* [#11266](https://github.com/shopware/shopware/issues/11266) - The HTML editor uses its own built-in sanitizer

::: details Click to see more fixed bugs

* [#11371](https://github.com/shopware/shopware/issues/11371) - fix sorting order when search property values
* [#11377](https://github.com/shopware/shopware/issues/11377) - Use sw-text-editor instead of mt-text-editor
* [#11515](https://github.com/shopware/shopware/issues/11515) - Fix reset active apps after app deactivation
* [#11521](https://github.com/shopware/shopware/issues/11521) - fix: improve check for visibility parameter check, fixes #11521 (backport: 6.7.1.0) (#11575)
* [#11599](https://github.com/shopware/shopware/issues/11599) - Change createdComponent back to being sync
* [#10040](https://github.com/shopware/shopware/issues/10040) - Fix backward compatibility of MediaThumbnailEntity
* [#11155](https://github.com/shopware/shopware/issues/11155) - Fix cart deserialization type error
* [#11550](https://github.com/shopware/shopware/issues/11550) - Fix inconsistent seoUrls for cross-selling products
* [#11521](https://github.com/shopware/shopware/issues/11521) - fix: improve check for visibility parameter check, fixes #11521 (backport: 6.7.1.0) (#11575)
* [#8018](https://github.com/shopware/shopware/issues/8018) - Use minimal search term length in config tables
* [#11085](https://github.com/shopware/shopware/issues/11085) - Fix primary connection is not working when replica configured

:::

## Credits

Thanks to all diligent friends for helping us make Shopware better and better with each pull request!

## More resources

* [Detailed diff on Github](https://github.com/shopware/shopware/compare/v6.7.1.1...v6.7.1.2) to the former version
* [Changelog on GitHub](https://github.com/shopware/shopware/blob/v6.7.1.2/CHANGELOG.md) for this version.
* [Installation overview](https://developer.shopware.com/docs/guides/installation/)
* [Update from a previous installation](https://developer.shopware.com/docs/guides/installation/template.html#update-shopware)

## Get in touch

Discuss about decisions, bugs you might stumble upon, etc in our [community discord](https://chat.shopware.com). See you there ;)

---

---

