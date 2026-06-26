# TESTING AND QUALITY

Compiled excerpts from the Shopware Developer Documentation snapshot. Prefer live docs at [developer.shopware.com](https://developer.shopware.com/) when in doubt.

---

## Accessibility in the Storefront
**Source:** [resources/accessibility/storefront-accessibility.md](https://developer.shopware.com/docs/resources/accessibility/storefront-accessibility.md)  
*(Body truncated in this bundle; follow the link for the rest.)*

# Accessibility in the Storefront

At Shopware, we are committed to creating inclusive and barrier-free shopping experiences for our merchants and their customers.

## What shopware does to ensure accessibility?

* Shopware is committed to fulfill the [WCAG 2.1 AA](https://www.w3.org/TR/WCAG21/) accessibility guidelines and Barrier-Free Information Technology Regulation (BITV 2.0) in the Storefront.
  * You can find more information on [shopware.design](https://shopware.design/foundations/accessibility.html) and [in our blog post](https://www.shopware.com/en/news/accessible-online-store-by-2025/).
* The Storefront is using [Bootstrap components](https://getbootstrap.com/docs/5.3/getting-started/accessibility/) that already consider good accessibility practices, for example, using aria roles.
* Much of the HTML structure and CSS styling already fulfill accessibility guidelines. However, there are still [open accessibility issues](#Overview-of-known-accessibility-issues) that will be addressed.
* Automated [E2E testing with playwright](https://github.com/shopware/shopware/tree/trunk/tests/acceptance) and axe reporter are used to ensure future accessibility.

## How are core accessibility improvements released?

Starting from **Shopware 6.6+,** accessibility improvements have been introduced, and **6.7+** includes further enhancements. Accessibility improvements are rolled out in regular minor releases, similar to other improvements or bug-fixes.
There is no large "accessibility release" planned that ships all accessibility improvements at once.

## How to deal with breaking accessibility changes?

Ensuring an accessible shop page can require changes in the HTML/Twig structure or the CSS. This can cause unintended behavior for an extension that is modifying an area that is being changed to improve accessibility.

Because of this, breaking accessibility changes are not enabled by default. All accessibility changes that include breaking changes are implemented behind a feature flag:

```env
ACCESSIBILITY_TWEAKS=1
```

However, breaking accessibility changes are still released regularly inside minor releases. They are just not active by default to not cause a breaking change.

The feature flag `ACCESSIBILITY_TWEAKS` can be activated inside your `.env`, similar to the major feature flags like `V6_7_0_0`. When the feature flag is enabled, all available accessibility improvements are activated.
This allows you to check if your project or extension is effected by the change and already prepare an adaptation to the change if it is necessary.

::: warning
With the major version v6.7.0 all accessibility improvements will become the default.
:::

### Example of a breaking accessibility change

Let's say, for example, that a list is not using a proper markup, and it is changed to improve accessibility.

This is what a suboptimal HTML structure could look like:

```twig
<div class="sidebar-list">
    {% block component_list_items %}
        <div class="list-item"><a href="#">Item</a></div>
        <div class="list-item"><a href="#">Item</a></div>
        <div class="list-item"><a href="#">Item</a></div>
    {% endblock %}
</div>
```

Let's assume it should be changed to a proper list. Instead of implementing this right away, it is implemented behind the `ACCESSIBILITY_TWEAKS` flag, including instructions how it should be changed:

```twig
{# @deprecated tag:v6.7.0 - The list will be changed to `<ul>` and `<li>` to improve accessibility #}
{% if feature('ACCESSIBILITY_TWEAKS') %}
    <ul class="sidebar-list">
        {% block component_list_items_inner %}
            <li class="list-item"><a href="#">Item</a></li>
            <li class="list-item"><a href="#">Item</a></li>
            <li class="list-item"><a href="#">Item</a></li>
        {% endblock %}
    </ul>
{% else %}
    <div class="sidebar-list">
        {# @deprecated tag:v6.7.0 - Use `component_list_items_inner` instead with `<li>` #}
        {% block component_list_items %}
            <div class="list-item"><a href="#">Item</a></div>
            <div class="list-item"><a href="#">Item</a></div>
            <div class="list-item"><a href="#">Item</a></div>
        {% endblock %}
    </div>
{% endif %}
```

If the block `component_list_items` is being extended, the new accessibility change can already be considered. If the change was rolled out without a feature flag, the extension still assumes a `<div class="list-item">` which would likely result in incorrect HTML:

```twig
{% sw_extends '@Storefront/storefront/component/list.html.twig' %}

{# Consider the new structure already #}
{% block component_list_items_inner %}
    {{ parent() }}
    <li class="list-item"><a href="#">My item</a></li>
{% endblock %}

{# This can be removed after v6.7.0 #}
{% block component_list_items %}
    {{ parent() }}
    <div class="list-item"><a href="#">My item</a></div>
{% endblock %}
```

## Overview of accessibility issues for iteration 1

::: info
With accessibility iteration 1 we have addressed the most critical accessibility problems and implemented multiple improvements.
:::

### Continuous efforts to ensure accessibility

We are continuously testing our core Storefront to meet accessibility requirements. This includes screen reader usage, keyboard-operation or color contrast analyzes.
We are using the [WCAG 2.1 Level AA](https://www.w3.org/TR/WCAG21/) standard and do our best to solve all issues to meet the WCAG 2.1 requirements.

### Overview of released accessibility improvements

* Below, you find a list of recent accessibility improvements. The list includes a changelog and the release versions for each improvement.
* Enable the feature flag `ACCESSIBILITY_TWEAKS` to activate all breaking accessibility changes.

| Topic                                                                                           | Breaking changes | Changelog                                                                                                                                                 | Release versions                                                                                 |
|-------------------------------------------------------------------------------------------------|------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------|
| Missing semantic markup of form address headings                                                | No               | [Changelog](https://github.com/shopware/shopware/blob/v6.6.6.0/changelog/release-6-6-6-0/2024-08-13-registration-form-fieldset-improvement.md)            | [v6.6.6.0](https://github.com/shopware/shopware/releases/tag/v6.6.6.0)                           |
| Product image zoom modal keyboard accessibility                                                 | No               | [Changelog](https://github.com/shopware/shopware/blob/v6.6.6.0/changelog/release-6-6-6-0/2024-08-08-improve-image-zoom-modal-accessibility.md)            | [v6.6.6.0](https://github.com/shopware/shopware/releases/tag/v6.6.6.0)                           |
| Focused slides in the carousel are not being moved into the visible area                        | Yes              | [Changelog](https://github.com/shopware/shopware/blob/v6.6.6.0/changelog/release-6-6-6-0/2024-08-05-improve-slider-element-accessibility.md)              | [v6.6.6.0](https://github.com/shopware/shopware/releases/tag/v6.6.6.0)                           |
| Focus jumps to the top of the page after closing a modal                                        | No               | [Changelog](https://github.com/shopware/shopware/blob/v6.6.6.0/changelog/release-6-6-6-0/2024-08-01-add-focus-handling-to-storefront.md)                  | [v6.6.6.0](https://github.com/shopware/shopware/releases/tag/v6.6.6.0)                           |
| Ensure that resizing content up to 200% does not cause breaks                                   | Yes              | [Changelog](https://github.com/shopware/shopware/blob/v6.6.6.0/changelog/release-6-6-6-0/2024-08-13-Improved-storefront-text-scaling.md)                  | [v6.6.6.0](https://github.com/shopware/shopware/releases/tag/v6.6.6.0)                           |
| Language of each Storefront passage or phrase in the content can be programmatically determined | No               | [Changelog](https://github.com/shopware/shopware/blob/v6.6.6.0/changelog/release-6-6-6-0/2024-08-05-add-language-to-reviews.md)                           | [v6.6.6.0](https://github.com/shopware/shopware/releases/tag/v6.6.6.0)                           |
| Check Lighthouse Accessibility Score                                                            | No               | [Changelog](https://github.com/shopware/shopware/blob/v6.6.6.0/changelog/release-6-6-6-0/2024-08-21-fix-scroll-up-button-accessibility.md)                | [v6.6.6.0](https://github.com/shopware/shopware/releases/tag/v6.6.6.0)                           |
| Pagination does not have links                                                                  | Yes              | [Changelog](https://github.com/shopware/shopware/blob/v6.6.6.0/changelog/release-6-6-6-0/2023-08-31-pagination-with-links.md)                             | [v6.6.6.0](https://github.com/shopware/shopware/releases/tag/v6.6.6.0)                           |
| Non-informative document title                                                                  | No               | [Changelog](https://github.com/shopware/shopware/blob/v6.6.1.0/changelog/release-6-6-1-0/2024-03-12-distinctive-document-titles.md)                       | [v6.6.6.0](https://github.com/shopware/shopware/releases/tag/v6.6.1.0)                           |
| The form element quantity selector is not labeled                                               | No               | [Changelog](https://github.com/shopware/shopware/blob/v6.6.5.0/changelog/release-6-6-5-0/2024-07-15-the-form-element-quantity-selector-is-not-labeled.md) | [v6.6.5.0](https://github.com/shopware/shopware/releases/tag/v6.6.5.0)                           |
| Slider reports confusing status changes to screen readers                                       | No               | [Changelog](https://github.com/shopware/shopware/blob/v6.6.4.0/changelog/release-6-6-4-0/2024-05-31-remove-unwanted-aria-live-attributes-from-sliders.md) | [v6.6.4.0](https://github.com/shopware/shopware/releases/tag/v6.6.4.0)                           |
| The user needs to be able to close triggered, additional content                                | No               | [Changelog](https://github.com/shopware/shopware/blob/trunk/changelog/release-6-6-3-0/2024-05-03-esc-key-for-nav-flyout-close.md)                         | [v6.6.3.0](https://github.com/shopware/shopware/releases/tag/v6.6.3.0)                           |
| Improve "Remove Product" button labeling in checkout                                            | No               | [Changelog](https://github.com/shopware/shopware/blob/v6.6.3.0/changelog/release-6-6-3-0/2024-05-03-improve-line-item-labels-and-alt-texts.md)            | [v6.6.3.0](https://github.com/shopware/shopware/releases/tag/v6.6.3.0)                           |
| Missing alternative text for product images in the shopping cart                                | No               | [Changelog](https://github.com/shopware/shopware/blob/v6.6.3.0/changelog/release-6-6-3-0/2024-05-03-improve-line-item-labels-and-alt-texts.md)            | [v6.6.3.0](https://github.com/shopware/shopware/releases/tag/v6.6.3.0)                           |
| A closing mechanism for the navigation                                                          | No               | [Changelog](https://github.com/shopware/shopware/blob/trunk/changelog/release-6-6-3-0/2024-05-03-esc-key-for-nav-flyout-close.md)        

… **Truncated.** Full document: https://developer.shopware.com/docs/resources/accessibility/storefront-accessibility.md


---

## Accessibility in the Storefront
**Source:** [resources/accessibility/storefront.md](https://developer.shopware.com/docs/v6.6/resources/accessibility/storefront.md)  
*(Body truncated in this bundle; follow the link for the rest.)*

# Accessibility in the Storefront

At Shopware, we are committed to creating inclusive and barrier-free shopping experiences for our merchants and their customers.

## What shopware does to ensure accessibility

* Shopware is committed to fulfill the [WCAG 2.1 AA](https://www.w3.org/TR/WCAG21/) accessibility guidelines and Barrier-Free Information Technology Regulation (BITV 2.0) in the Storefront.
  * You can find more information on [shopware.design](https://shopware.design/foundations/accessibility.html) and [in our blog post](https://www.shopware.com/en/news/accessible-online-store-by-2025/).
* The Storefront is using [Bootstrap components](https://getbootstrap.com/docs/5.3/getting-started/accessibility/) that already consider good accessibility practices, for example, using aria roles.
* Much of the HTML structure and CSS styling already fulfill accessibility guidelines. However, there are still [open accessibility issues](#Overview-of-known-accessibility-issues) that will be addressed.
* Automated [E2E testing with playwright](https://github.com/shopware/shopware/tree/trunk/tests/acceptance) and axe reporter are used to ensure future accessibility.

## How core accessibility improvements are released

Accessibility improvements are rolled out in regular minor releases, similar to other improvements or bug-fixes. We implement all accessibility improvements in the current major version `6.6.x` and its minor versions.
There is no large "accessibility release" planned that ships all accessibility improvements at once.

## How to deal with breaking accessibility changes

Ensuring an accessible shop page can require changes in the HTML/Twig structure or the CSS. This can cause unintended behavior for an extension that is modifying an area that is being changed to improve accessibility.

Because of this, breaking accessibility changes are not enabled by default. All accessibility changes that include breaking changes are implemented behind a feature flag:

```env
ACCESSIBILITY_TWEAKS
```

However, breaking accessibility changes are still released regularly inside minor releases. They are just not active by default to not cause a breaking change.

The feature flag `ACCESSIBILITY_TWEAKS` can be activated inside your `.env`, similar to the major feature flags like `V6_7_0_0`. When the feature flag is enabled, all available accessibility improvements are activated.
This allows you to check if your project or extension is effected by the change and already prepare an adaptation to the change if it is necessary.

::: warning
With the major version v6.7.0 all accessibility improvements will become the default.
:::

### Example of a breaking accessibility change

Let's say, for example, that a list is not using a proper markup, and it is changed to improve accessibility.

This is what a suboptimal HTML structure could look like:

```twig
<div class="sidebar-list">
    {% block component_list_items %}
        <div class="list-item"><a href="#">Item</a></div>
        <div class="list-item"><a href="#">Item</a></div>
        <div class="list-item"><a href="#">Item</a></div>
    {% endblock %}
</div>
```

Let's assume it should be changed to a proper list. Instead of implementing this right away, it is implemented behind the `ACCESSIBILITY_TWEAKS` flag, including instructions how it should be changed:

```twig
{# @deprecated tag:v6.7.0 - The list will be changed to `<ul>` and `<li>` to improve accessibility #}
{% if feature('ACCESSIBILITY_TWEAKS') %}
    <ul class="sidebar-list">
        {% block component_list_items_inner %}
            <li class="list-item"><a href="#">Item</a></li>
            <li class="list-item"><a href="#">Item</a></li>
            <li class="list-item"><a href="#">Item</a></li>
        {% endblock %}
    </ul>
{% else %}
    <div class="sidebar-list">
        {# @deprecated tag:v6.7.0 - Use `component_list_items_inner` instead with `<li>` #}
        {% block component_list_items %}
            <div class="list-item"><a href="#">Item</a></div>
            <div class="list-item"><a href="#">Item</a></div>
            <div class="list-item"><a href="#">Item</a></div>
        {% endblock %}
    </div>
{% endif %}
```

If the block `component_list_items` is being extended, the new accessibility change can already be considered. If the change was rolled out without a feature flag, the extension still assumes a `<div class="list-item">` which would likely result in incorrect HTML:

```twig
{% sw_extends '@Storefront/storefront/component/list.html.twig' %}

{# Consider the new structure already #}
{% block component_list_items_inner %}
    {{ parent() }}
    <li class="list-item"><a href="#">My item</a></li>
{% endblock %}

{# This can be removed after v6.7.0 #}
{% block component_list_items %}
    {{ parent() }}
    <div class="list-item"><a href="#">My item</a></div>
{% endblock %}
```

## Overview of accessibility issues for iteration 1

::: info
With accessibility iteration 1 we have addressed the most critical accessibility problems and implemented multiple improvements.
You can find an overview of the accessibility iteration 1 epic in the following ticket: [NEXT-37039](https://issues.shopware.com/issues/NEXT-37039)
:::

### Continuous efforts to ensure accessibility

We are continuously testing our core Storefront to meet accessibility requirements. This includes screen reader usage, keyboard-operation or color contrast analyzes.
We are using the [WCAG 2.1 Level AA](https://www.w3.org/TR/WCAG21/) standard and do our best to solve all issues to meet the WCAG 2.1 requirements.

### Overview of released accessibility improvements

* Below, you find a list of recent accessibility improvements. The list includes a changelog and the release versions for each improvement.
* Enable the feature flag `ACCESSIBILITY_TWEAKS` to activate all breaking accessibility changes.

| Topic                                                                                           | Breaking changes | Changelog                                                                                                                                                 | Release versions                                                                                 |
|-------------------------------------------------------------------------------------------------|------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------|
| Missing semantic markup of form address headings                                                | No               | [Changelog](https://github.com/shopware/shopware/blob/v6.6.6.0/changelog/release-6-6-6-0/2024-08-13-registration-form-fieldset-improvement.md)            | [v6.6.6.0](https://github.com/shopware/shopware/releases/tag/v6.6.6.0)                           |
| Product image zoom modal keyboard accessibility                                                 | No               | [Changelog](https://github.com/shopware/shopware/blob/v6.6.6.0/changelog/release-6-6-6-0/2024-08-08-improve-image-zoom-modal-accessibility.md)            | [v6.6.6.0](https://github.com/shopware/shopware/releases/tag/v6.6.6.0)                           |
| Focused slides in the carousel are not being moved into the visible area                        | Yes              | [Changelog](https://github.com/shopware/shopware/blob/v6.6.6.0/changelog/release-6-6-6-0/2024-08-05-improve-slider-element-accessibility.md)              | [v6.6.6.0](https://github.com/shopware/shopware/releases/tag/v6.6.6.0)                           |
| Focus jumps to the top of the page after closing a modal                                        | No               | [Changelog](https://github.com/shopware/shopware/blob/v6.6.6.0/changelog/release-6-6-6-0/2024-08-01-add-focus-handling-to-storefront.md)                  | [v6.6.6.0](https://github.com/shopware/shopware/releases/tag/v6.6.6.0)                           |
| Ensure that resizing content up to 200% does not cause breaks                                   | Yes              | [Changelog](https://github.com/shopware/shopware/blob/v6.6.6.0/changelog/release-6-6-6-0/2024-08-13-Improved-storefront-text-scaling.md)                  | [v6.6.6.0](https://github.com/shopware/shopware/releases/tag/v6.6.6.0)                           |
| Language of each Storefront passage or phrase in the content can be programmatically determined | No               | [Changelog](https://github.com/shopware/shopware/blob/v6.6.6.0/changelog/release-6-6-6-0/2024-08-05-add-language-to-reviews.md)                           | [v6.6.6.0](https://github.com/shopware/shopware/releases/tag/v6.6.6.0)                           |
| Check Lighthouse Accessibility Score                                                            | No               | [Changelog](https://github.com/shopware/shopware/blob/v6.6.6.0/changelog/release-6-6-6-0/2024-08-21-fix-scroll-up-button-accessibility.md)                | [v6.6.6.0](https://github.com/shopware/shopware/releases/tag/v6.6.6.0)                           |
| Pagination does not have links                                                                  | Yes              | [Changelog](https://github.com/shopware/shopware/blob/v6.6.6.0/changelog/release-6-6-6-0/2023-08-31-pagination-with-links.md)                             | [v6.6.6.0](https://github.com/shopware/shopware/releases/tag/v6.6.6.0)                           |
| Non-informative document title                                                                  | No               | [Changelog](https://github.com/shopware/shopware/blob/v6.6.1.0/changelog/release-6-6-1-0/2024-03-12-distinctive-document-titles.md)                       | [v6.6.6.0](https://github.com/shopware/shopware/releases/tag/v6.6.1.0)                           |
| The form element quantity selector is not labeled                                               | No               | [Changelog](https://github.com/shopware/shopware/blob/v6.6.5.0/changelog/release-6-6-5-0/2024-07-15-the-form-element-quantity-selector-is-not-labeled.md) | [v6.6.5.0](https://github.com/shopware/shopware/releases/tag/v6.6.5.0)                           |
| Slider reports confusing status changes to screen readers                                       | No               | [Changelog](https://github.com/shopware/shopware/blob/v6.6.4.0/changelog/release-6-6-4-0/2024-05-31-remove-unwanted-aria-live-attributes-from-sliders.md) | [v6.6.4.0](https://github.com/shopware/shopware/releases/tag/v6.6.4.0)                           |
| The user needs to be able to close triggered, additional content                                | No               | [Changelog](https://github.com/shopware/shopware/blob/trunk/changelog/release-6-6-3-0/2024-05-03-esc-key-for-nav-flyout-close.md)                         | [v6.6.3.0](https://github.com/shopware/shopware/releases/tag/v6.6.3.0)                           |
| Improve "Remove Product" button labeling in checkout                                            | No               | [Changelog](https://github.com/shopware/shopware/blob/v6.6.3.0/changelog/release-6-6-3-0/2024-05-03-improve-line-item-labels-and-alt-texts.md)            | [v6.6.3.0](https://github.com/shopware/shopware/releases/tag/v6.6.3.0)                           |
| Missing alternative text for product images in the shopping cart                                | No               | [Changelog](https://github.com/shopware/shopware/blob/v6.6.3.0/changelog/release-6-6-3-0/2024-05-03-improve-line-item-labels-and-alt-texts.md)            | [v6.6.3.0](https://github.com/shopware/shopware/releases/tag/v6.6.3.0)                           |
| A closing mechanism for the navigation                                                          | No               | [Changelog](htt

… **Truncated.** Full document: https://developer.shopware.com/docs/v6.6/resources/accessibility/storefront.md


---

## Guidelines
**Source:** [resources/guidelines.md](https://developer.shopware.com/docs/v6.6/resources/guidelines.md)  
# Guidelines

This document is intended for all readers and contributors. We have defined coding, documentation, and testing guidelines.

The code section lays out the coding standards. This helps anyone understand and modify the code at any point while keeping the code consistent.

The test section briefs you about best practices for writing end-to-end tests.

The document section details you on the language style, grammar, markdown syntax, and documentation process.

this document serves as a comprehensive resource for both readers and contributors, offering essential coding, testing, and documentation guidelines to maintain consistency, promote best practices, and facilitate effective collaboration.

---

---

## Code
**Source:** [resources/guidelines/code.md](https://developer.shopware.com/docs/v6.6/resources/guidelines/code.md)  
# Code

Code guidelines is a comprehensive developer handbook that includes dos and don'ts and a clear description of how the code functions, blocks, class, method, argument, return value, and files may be used. It enhances code readability, reproducibility, and usability.

Refer to the following different sections to know more about it.

---

---

## Backward Compatibility
**Source:** [resources/guidelines/code/backward-compatibility.md](https://developer.shopware.com/docs/v6.6/resources/guidelines/code/backward-compatibility.md)  
*(Body truncated in this bundle; follow the link for the rest.)*

# Backward Compatibility

## Introduction

Shopware is a standard ecommerce solution used by many customers worldwide and is the technical foundation of their online business. As developers of Shopware, it is our highest goal to guarantee the reliability of the software for our customers. Always remember that every change you make can have a big impact on the life of our customers, either in a good way or in a bad way.

For the release strategy, Shopware uses a semantic [versioning](https://www.shopware.com/en/news/shopware-6-versioning-strategy/) and therefore has to be always backward compatible for minor and patch updates. This brings additional challenges when changing the code of Shopware. The following guide aims to provide you with the necessary workflows and techniques to do your changes in a backward compatible way and what to do if it is not possible.

## Annotations

During the development, different cases occur where you want to replace old code with new ones or even remove some obsolete code. As Shopware must always be backward compatible on minor and patch updates, old code should only be removed with a major release. Until the next major release, you want to mark the code with a corresponding annotation to inform other developers of the planned change. This overview shows the most important annotations and in which situation they must be used.

### @deprecated

```php
/**
 * @deprecated tag:v6.5.0 - Use NewFunction() instead
 */
```

The `@deprecated` annotation is used for obsolete public code, which will be removed with the next major release. The annotation always needs the specific major version tag, in which the code should be removed. Always add a meaningful comment with information about the corresponding replacement and how the deprecated code can be removed.

### @feature-deprecated

```php
/**
 * @feature-deprecated (flag:FEATURE_NEXT_11111)
 */
```

The `@feature-deprecated` annotation is used for obsolete code during the development of a feature when the code is still hidden behind a feature flag. This is important so that code that is not public will not trigger deprecation warnings. This annotation has to be changed to the correct `@deprecated` annotation when the feature is released, and the corresponding feature flag is removed. Always add the name of the corresponding feature flag to the annotation so that it will not be forgotten when the flag is removed.

### @major-deprecated

```php
/**
 * @major-deprecated (flag:FEATURE_NEXT_22222)
 */
```

The `@major-deprecated` annotation is used for breaking code which has to stay behind a specific major feature flag until the next major release. Always add the name of the corresponding feature flag to the annotation so that it will not be forgotten when the flag is removed.

### @internal

```php
/**
 * @internal (flag:FEATURE_NEXT_11111)
 */
```

In combination with a feature flag, like shown above, the `@internal` annotation is used for newly introduced code, which is not yet released. This ensures that it will not be treated as a public API until the corresponding feature is released and makes it possible to change the code in any way until the final release. Always add the name of the corresponding feature flag to the annotation so that it will not be forgotten when the corresponding feature is released.

## Workflows

### Backward compatible features

When developing new features, the goal should always be to do this in a backward compatible way. This ensures that the feature can be shipped with a minor release to provide value for customers as soon as possible. The following table should help you to use the correct approach for each type of change.

| Case                    | During development                                                                                                                                                                                                                                                                                                                                       | On feature release                                                                                                                                       | Next major release                          |
| ---                     | ---                                                                                                                                                                                                                                                                                                                                                      | ---                                                                                                                                                      | ---                                         |
| 🚩 **Feature Flag**     | Hide code behind normal [feature flag](../../references/adr/2020-08-10-feature-flag-system.md).                                                                                                                                                                                                                                                                                            | Remove the feature flag.                                                                                                                                     |                                             |
| ➕ **New code**         | Add `@internal annotation` for new public API.                                                                                                                                                                                                                                                                                                           | Remove `@internal` annotation.                                                                                                                           |                                             |
| ⚪ **Obsolete code**    | Add `@feature-deprecated` annotation.                                                                                                                                                                                                                                                                                                                    | Replace @feature-deprecated with normal `@deprecated` annotation.                                                                                        | Remove old code.                            |
| 🔴 **Breaking change**  | Add `@major-deprecated` annotation. Hide breaking code behind additional major [feature flag](../../references/adr/2020-08-10-feature-flag-system.md). Also, create a separate [changelog](../../references/adr/2020-08-03-implement-new-changelog.md) for the change with the major flag. |                                                                                                                                                          | Remove old code. Remove the major feature flag. |
| 🔍 **Tests**            | Add new tests behind a feature flag.                                                                                                                                                                                                                                                                                                                       | Remove feature flags from new tests. Declare old tests as [legacy](https://symfony.com/doc/current/components/phpunit_bridge.html#mark-tests-as-legacy). | Remove legacy tests.                        |

You can also find more detailed information and code examples in the corresponding **[ADR](https://github.com/shopware/shopware/blob/trunk/adr/)** for the deprecation strategy.

### Breaking Changes / Features

The first goal should always be to make your changes backward compatible. But there might be some special cases where it isn't possible in any way. In this case, the change can only be released with a major version. As we develop all changes in the same code base, the `trunk` branch, the changes have to stay behind a special feature flag, which is especially marked as a major feature flag.

| Case                    | During development                                                                                                                                           | Next major release (feature release) |
| ---                     | ---                                                                                                                                                          | ---                                  |
| 🚩 **Feature Flag**     | Hide code behind a major feature flag.                                                                                                                         | Remove major feature flag.           |
| ➕ **New code**         | Add `@internal` annotation for new public API.                                                                                                               | Remove `@internal` annotation.       |
| ⚪ **Obsolete code**    | Add `@major-deprecated` annotation.                                                                                                                          | Remove old code.                     |
| 🔴 **Breaking change**  | Add `@major-deprecated` annotation.                                                                                                                          | Remove old code.                     |
| 🔍 **Tests**            | Add new tests behind a major feature flag. Declare old tests as [legacy](https://symfony.com/doc/current/components/phpunit_bridge.html#mark-tests-as-legacy). | Remove legacy tests.                 |

## Compatibility sheet

To ensure backward compatibility, it is important to know what you are allowed to do and what not. The following sheet should give you an orientation on common changes and how they could affect the backward compatibility. Although a lot of effort went into this list, it is not guaranteed to be 100% complete. Always keep the persona of third-party developers in mind and challenge your changes against external needs.

### PHP

As Shopware is based on the PHP framework Symfony, we also have to make sure to use the rules which the framework follows. Besides the list below, always keep in mind the backward compatibility promise and implement your changes in a way the promise is kept.

**[Symfony Backward Compatibility Promise](https://symfony.com/doc/current/contributing/code/bc.html)**

| Use Case                                                                                                      | Allowed?   | Notes / Alternatives                                                                                                                                                                                                           |
| ---                                                                                                           | ---        | ---                                                                                                                                                                                                                            |
| Change the typehint of a class, interface or trait.                                                           | 🔴 NO      | Add the new typehint as an abstract class. Code Example: [Extend class with abstract class](#extend-class-with-abstract-class)                                                                                             |
| Change the constructor of a service.                                                                          | ✅ YES     | Services have to be instantiated over the container, so the changes should not break anything.                

… **Truncated.** Full document: https://developer.shopware.com/docs/v6.6/resources/guidelines/code/backward-compatibility.md


---

## Cart Process
**Source:** [resources/guidelines/code/cart-process.md](https://developer.shopware.com/docs/v6.6/resources/guidelines/code/cart-process.md)  
# Cart Process

* Within `\Shopware\Core\Checkout\Cart\CartProcessorInterface::process`, no queries may be executed because this method is executed several times in a row to resolve the dependencies of the elements in the shopping cart.
* The `\Shopware\Core\Checkout\Cart\CartDataCollectorInterface::collect` method must always check if the required data has already been loaded. This is to avoid having to execute unnecessarily many queries on the database. The loaded data will be appended to the passed *CartDataCollection*.
* The creation of line items must always take place via a `LineItemFactoryHandler` class.
* All price calculations must take place via an appropriate `PriceCalculator`. All price calculators are stored inside the `Shopware\Core\Checkout\Cart\Price` class.
* All shopping cart functions must be mapped via a corresponding store API route. The routes are located in the `Shopware\Core\Checkout\Cart\SalesChannel` namespace.

---

---

## Context Rules and Rule Systems
**Source:** [resources/guidelines/code/context-rules-rule-systems.md](https://developer.shopware.com/docs/v6.6/resources/guidelines/code/context-rules-rule-systems.md)  
# Context Rules and Rule Systems

* In a rule, there must never be a query against the database because all configured rules are validated in a request.
* Rules that check for the cart must always support the `\Shopware\Core\Checkout\Cart\Rule\CartRuleScope` class and the `\Shopware\Core\Checkout\Cart\Rule\LineItemScopeclass`.
* Rules may only access data provided in the appropriate scopes.

---

---

## Contribution Guidelines
**Source:** [resources/guidelines/code/contribution.md](https://developer.shopware.com/docs/v6.6/resources/guidelines/code/contribution.md)  
# Contribution Guidelines

## Introduction

First of all, thank you! :)
You have decided to contribute code to our software and become a member of the large Shopware community.
We appreciate your hard work and want to handle it with the most possible respect.

To ensure the quality of our code and our products, we have created a list of guidelines for you.
It helps you and us to collaborate with our software.
Following these guidelines will help us integrate your changes into our daily workflow.

## Requirements for a successful pull request

To avoid your pull request getting rejected, you should always check that you provided all the necessary information so that we can easily integrate your changes.
Here is a checklist of requirements you should always consider when committing new changes:

* A pull request to the Shopware core always has to be made to the [main shopware](https://github.com/shopware/shopware) repository.
* Fill out the [pull request info template](https://github.com/shopware/shopware/blob/trunk/.github/PULL_REQUEST_TEMPLATE.md) as detailed as possible.
* Create a changelog file with documentation of your changes.
  Refer to [Changelog](https://github.com/shopware/shopware/blob/master/adr/2020-08-03-implement-new-changelog.md) section for more detailed information about writing changelog.
* Check if your pull request addresses the correct Shopware branch.
  It should always target the `trunk` branch.
  If you would like to have your changes in the previous major version, we have the possibility to do a backport quite easily.
  Let us know about this in the pull request description.
* Check if your implementation is missing some important parts - For example, translations, backwards compatibility, deprecations, etc.
* Provide tests for your implementation.
* Check if there is already an existing pull request tackling the same issue.
* Write your commit messages in English. The individual commit messages in the PR are not critical since the PR will be squashed on merge.
  However, ensure your **pull request title** follows the [Conventional Commits](https://www.conventionalcommits.org/) format, as this will become the final commit message.
  * Example PR titles:
    * `feat: Add new product import API`
    * `fix: Resolve cart calculation issue`
    * `docs: Update installation instructions`

::: danger
Pull requests which do not fulfill these requirements will most likely not be accepted by our team.
To avoid your changes going through unnecessary workflow cycles, make sure to check this list with every pull request.
:::

## The developing workflow on GitHub

When you create a new pull request on GitHub, please ensure:

1. Your PR title follows the **conventional commits** format as it will become the squashed commit message
2. You've provided all necessary information in the PR description
3. Your changes are complete and tested

You are responsible for maintaining and updating your pull request. This includes:

* Responding to review comments in a timely manner
* Updating the code according to review feedback
* Keeping the PR up to date with the target branch if conflicts arise
* Making sure that all pipeline checks succeed on your PR

::: tip
Once your PR is public, avoid rebasing or force-pushing to the branch.
Adding new commits makes it easier for reviewers to track changes and see what was updated in response to feedback.
The PR will be automatically squashed when merged.
:::

::: tip
Allow us to make changes to your PR.
This will help merge the PR faster, as we can fix minor issues ourselves.
Refer to the [GitHub Docs](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/working-with-forks/allowing-changes-to-a-pull-request-branch-created-from-a-fork) on how to do it.
:::

::: warning
Pull requests that become stale (no activity from the author for two weeks after a review or request for changes) will be closed.
You can always reopen the pull request when you're ready to continue working on it.
:::

## What happens after a pull request has been created

Everyday weekdays, we assign the pull request to a domain (team) which is responsible for the specific part of the Shopware software.
The area will then review your pull request and decide what to do next.
The team can either accept your pull request, decline it, or ask you to update it with more information or changes.

## Why a pull request gets declined

So the worst thing happened; Your pull request was declined.
No reason to be upset.
We know that it can sometimes be hard to understand why your pull request was rejected.
We want to be as transparent as possible, but sometimes it can also rely on internal decisions.

Here is a list of common reasons why we reject a pull request:

* The pull request does not fulfill the requirements of the list above.
* You did not update your pull request with the necessary info after a specific label was added.
* The change you made is already a part of a current change by Shopware and is handled internally.
* The benefit of your change is not relevant to the whole product but only to your intent.
* Your change implements a feature that does not fit our roadmap or our company values.

To avoid a decline of the PR beforehand, create a new issue or discussion in the Shopware repository.
Especially if you want to implement a new feature or change the behavior of an existing one.

---

---

## resources/guidelines/code/core.md
**Source:** [resources/guidelines/code/core.md](https://developer.shopware.com/docs/v6.6/resources/guidelines/code/core.md)  
---

---

## 2023-05-16 - PHP 8.1 & Symfony 6.1 new features
**Source:** [resources/guidelines/code/core/6.5-new-php-language-features.md](https://developer.shopware.com/docs/v6.6/resources/guidelines/code/core/6.5-new-php-language-features.md)  
*(Body truncated in this bundle; follow the link for the rest.)*

::: info
This document represents core guidelines and has been mirrored from the core in our Shopware 6 repository.
You can find the original version [here](https://github.com/shopware/shopware/blob/trunk/coding-guidelines/core/6.5-new-php-language-features.md)
:::

# 2023-05-16 - PHP 8.1 & Symfony 6.1 new features

## Context

As of Shopware 6.5 the minimum version of PHP is 8.1 and the minimum version of Symfony is 6.1. We would like to *promote* the usage of the newly available features.

Many of the new features allow us to reduce boilerplate, make it easier to prevent common mistakes, improve refactoring support, increase legibility, perform faster and so on.

By using the latest features we allow the reader and writer of code to focus on the domain rather than the language.

## PHP 8.0 & 8.1 new features

### Promoted Properties

* [PHP Docs](https://www.php.net/manual/en/language.oop5.decon.php#language.oop5.decon.constructor.promotion)
* [PHP Watch](https://php.watch/versions/8.0/constructor-property-promotion)

*We have automatically refactored all existing code to use Promoted Properties using Rector.*

Promoted properties allow us to reduce the boilerplate when defining classes, by removing the need to type the property name four times and the type twice.

Class properties, with their visibility and flags can now be specified entirely in the constructor.

From:

```php
class Point {
    private int $x;
    private int $y;
    public function __construct(int $x, int $y)
    {
        $this->x = $x;
        $this->y = $y;
    }
}
```

To:

```php
class Point {
    public function __construct(private int $x, private int $y)
    {
    }
}
```

Note: It is still possible to use normal property definitions/assignments with promoted properties. For example, if you need to manipulate some dependencies.

Advantages:

* Less code, less duplication.
* Better refactoring.

#### Backwards Compatibility / Migration Strategy

Migrating to promoted properties does not represent a breaking change.

### New in initializers

* [PHP Docs](https://www.php.net/manual/en/language.oop5.decon.php#language.oop5.decon.constructor.new)

It is now possible to specify an object as a default parameter value in a function/method. Previously it was only possible to specify scalar values.

From:

```php
class PasswordHasher
{
    private Hasher $hasher;
    public function __construct(private Hasher $hasher = null)
    {
        $this->hasher = $hasher ?? new Bcrypt();
    }
}
```

To:

```php
class PasswordHasher
{
    public function __construct(private Hasher $hasher = new Bcrypt())
    {}
}
```

Advantages:

* Less code
* More consistent

#### Backwards Compatibility / Migration Strategy

Migrating to inline object default parameters does not represent a breaking change.

### Match

* [PHP Docs](https://www.php.net/manual/en/control-structures.match.php)
* [PHP Watch](https://php.watch/versions/8.0/match-expression)

*We have automatically refactored all existing code to use match instead of switch using Rector.*

In most cases, `switch` statements can be replaced with `match` statements:

* Match uses strict equality unlike switch which uses weak comparison and can lead to subtle bugs.
* Each match arm does not fall through without a break statement, unlike switch.
* Match expressions must be exhaustive, if there is no default arm specified, and no arm matches the given value, an `UnhandledMatchError` is thrown.
* Match is an expression and thus returns a value, reducing unnecessary variables and reducing the risk of accessing undefined variables.

From:

```php
switch ($statusCode) {
    case 200:
    case 300:
        $message = null;
        break;
    case 400:
        $message = 'not found';
        break;
    case 500:
        $message = 'server error';
        break;
    default:
        $message = 'unknown status code';
        break;
}
```

To:

```php
$message = match ($statusCode) {
    200, 300 => null,
    400 => 'not found',
    500 => 'server error',
    default => 'unknown status code',
};
```

Note: Conditions can be combined in a much simpler fashion.

#### Backwards Compatibility / Migration Strategy

There are cases where migrating from a switch to a match could case a BC break. For example switch performs lose type checks and throws an exception for unhandled values.

When migrating code, be sure to check that values are the correct types and that all cases are handled.

### New string functions

* `str_contains`
* `str_starts_with`
* `str_ends_with`

Advantages:

* Simpler and more concise.
* Saner return types.
* It is harder to get their usage wrong, for example checking for 0 vs false with `strpos`.
* The functions are faster, being implemented in C.
* The operations require less function calls, for example no usages of strlen are required.

### Named arguments

* [PHP Docs](https://www.php.net/manual/en/functions.arguments.php)
* [PHP Watch](https://php.watch/versions/8.0/named-parameters)

Named arguments are useful when calling code with bad and/or large API's. For example, many of PHP's global functions.

In terms of calling bad PHP API's, the following advantages apply:

* It is possible to skip defaults in between the arguments you want to change.
* The code is better documented since the argument label is specified with the value, very useful for boolean flags.

From:

```php
htmlspecialchars($string, ENT_COMPAT | ENT_HTML, 'UTF-8', false);
```

To:

```php
htmlspecialchars($string, double_encode: false);
```

Note: The second argument is not changed, but in the first example we must provide the default value, in order to change the double encode flag.

#### Backwards Compatibility / Migration Strategy

We do not want to use named parameters when calling Shopware API's as parameter names are not a part of the Backwards compatability promise.

Named parameters should only be used when calling PHP API's.

### Type improvements

* [PHP Docs](https://www.php.net/manual/en/language.types.type-system.php)
* [PHP Watch - Union Types](https://php.watch/versions/8.0/union-types)
* [PHP Watch - Mixed Type](https://php.watch/versions/8.0/mixed-type)
* [PHP Watch - Intersection Types](https://php.watch/versions/8.1/intersection-types)

**It will now only be necessary to reach for @var & @param annotations when defining array shapes, generics and more specific types such as `class-string`, `positive-int` etc. Everything else should be natively typed.**

When a type can really be any value, this can now be expressed as `mixed`.

When a type can be multiple, but not all, this can now be expressed as a union type, eg: `int|string`.

When a type must be an intersection of multiple types, this can now be expressed as an intersection type, eg: `MyService&MockObject`.

These improvements come with various advantages:

* The types are enforced by PHP, so TypeError's will be thrown when attempting to pass non-valid types.
* It allows us to move more type information from phpdoc into function signatures.
* It prevents incorrect function information. phpdocs can often become stale when they are not updated with the function itself.

### Enums

* [PHP Docs](https://www.php.net/manual/en/language.types.enumerations.php)
* [PHP Watch](https://php.watch/versions/8.1/enums)

PHP finally has native support for enumerations, with various advantages over common userland packages and using const's.

Enums are useful where we have a predefined list of constant values. It's now not necessary to provide values as constants, and it's not necessary to create arrays of the constants to check validity.

From:

```php
class Indexer
{
    public const PARTIAL = 'partial';
    public const FULL = 'full';

    public function product(int $id, string $method): void
    {
        if (!in_array($method, [self::PARTIAL, self::FULL], true)) {
            throw new \InvalidArgumentException();
        }
    
        match ($method) {
            self::PARTIAL => $this->partial($id),
            self::FULL => $this->full($id)
        };
    }
}
```

To:

```php
enum IndexMethod
{
    case PARTIAL;
    case FULL;
}

class Indexer
{
    public function product(int $id, IndexMethod $method): void
    {
        match ($method) {
            IndexMethod::PARTIAL => $this->partial($id),
            IndexMethod::FULL => $this->full($id)
        };
    }
}
```

Advantages:

* Works great with `match` - an `UnhandledMatchError` exception will be thrown if there is no match arm for a given enum case.
* Can type hint on an enum.
* No need to validate a case.
* Can provide backed values and serialize/unserialize with `MyEnum::from()` && `MyEnum::tryFrom()`.
* Enums can provide methods and implement interfaces.
* Better comparison features, e.g. Enums are singletons.

#### Backwards Compatibility / Migration Strategy

See the [Use PHP 8.1 Enums](../../../references/adr/2023-05-16-php-enums) ADR for the decision and migration strategy.

### Readonly properties

* [PHP Docs](https://www.php.net/manual/en/language.oop5.properties.php#language.oop5.properties.readonly-properties)
* [PHP Watch](https://php.watch/versions/8.1/readonly)

Readonly properties are very useful when building DTOs. When you want to communicate a payload to a system or service, `readonly` properties allow us to create immutable data structures with a lot less code.

In conjunction with promoted properties, we can reduce the boilerplate of a class significantly. Consider a product reindex command:

From:

```php
class ProductReindexCommand
{
    private int $productId;
    
    private bool $includeStock:
    
    public function __construct(int $productId, bool $includeStock)
    {
        $this->productId = $productId;
        $this->includeStock = $includeStock;
    }
    
    public function getProductId(): int
    {
        return $this->productId;
    }
    
    public function includeStock(): bool
    {
        return $this->includeStock;
    }
}
```

To:

```php
class ProductReindexCommand
{
    public function __construct(public readonly int $productId, public readonly bool $includeStock)
    {
    }
}
```

In the first example, we use private properties to prohibit updates and public getters to allow access to the data. In the second we change the properties to `public` to allow access to the data without getters, but use `readonly` to prohibit updates. We also use promoted properties to make it even more succinct.

Advantages:

* Reduced boilerplate.
* Make the intent of code clearer.

#### Backwards Compatibility / Migration Strategy

All private properties, which are not written to after instantiation can successfully be migrated to `readonly` without BC breaks.

New code can use `readonly` on public and protected properties, but for existing code, that would be a BC break.

### First-class callable syntax

* [PHP Docs](https://www.php.net/manual/en/functions.first_class_callable_syntax.php)
* [PHP Watch](https://php.watch/versions/8.1/first-class-callable-syntax)

This is a new method of referencing callables with strings and arrays. It allows for improved refactoring support, better static analysis and fixes some subtle bugs with scope.

Consider an operation to find the longest string in an array, you might use `strlen` within an `array_map`:

From:

```php
$longest = max(array_map('strlen', $strings));
```

To:

```php
$longest = max(array_map(strlen(...), $strings));
```

Instead of using an arbitrary string as a reference to a function, we can now use the `(...)` syntax to create a callable.

It can also be used with object methods, instance or static, e.g.:

```php
$callable = $object->doCoolStuff(...);
$callable = \My\Object::doCoolStuff(...);
```

Advantages:

* Refactoring support.
* Better static analyses.
* Fixes scope issues.

### Attributes

* [PHP Docs](https://www.php.net/manual/en/language.attributes.overview.php)
* [PHP Watch](https://php.watch/versions/8.0/attributes)

*We have automatically refactored all existing cod

… **Truncated.** Full document: https://developer.shopware.com/docs/v6.6/resources/guidelines/code/core/6.5-new-php-language-features.md


---

## ADR
**Source:** [resources/guidelines/code/core/adr.md](https://developer.shopware.com/docs/v6.6/resources/guidelines/code/core/adr.md)  
::: info
This document represents core guidelines and has been mirrored from the core in our Shopware 6 repository.
You can find the original version [here](https://github.com/shopware/shopware/blob/trunk/coding-guidelines/core/adr.md)
:::

# ADR

This guideline describes what we expect from our ADRs and how you can write some.

Joel Parker Henderson has done a lot of work on this topic, collected excellent ideas, tips, templates, and examples, and published them on [github](https://github.com/joelparkerhenderson/architecture-decision-record).

The ADRs examples published there are good.

Expectations for an ADR:

* Write a complete description of the requirements
* List all technical domains that are affected by the ADR
* List all affected logic in the system that are affected
* Write some pseudo code for your new logic to visualize what you want to realize
* Define all public APIs that are to be created or changed with your new logic
* Define how developers can extend the new APIs and logic and what possible business cases you see
* Define the reason why you made the decision. It often helps to understand why you made a specific architectural change in the future.
* Define all consequences of the decision and how they impact a developer who has used the code/product.

Everyone takes a different approach to create ADRs and meeting the expectations above. One possible approach is the following:

* Create a list of domains you want to touch (Store-API, admin process, indexing, ...)
* Create a headline for each domain
* Describe the domains. After each headline, write in 2 sentences why this domain is relevant for this ADR
* Describe the "problems" of each domain... write in each domain which logic has to be touched... not how you want to change them, only why
  * e.G. indexing: "We have to extend the product indexing process because calculating the new product data is too expensive, and we want to calculate the values in a background job."
* Describe the "solution" of each domain... write in each domain how you want to extend the above logic to solve your "problems."
* Add a new section about extendability and write down how developers should be able to extend your system and which business cases you see
* Last, add some pseudocode at the end to visualize your solutions and ideas.

---

---

## Benchmarks
**Source:** [resources/guidelines/code/core/benchmarks.md](https://developer.shopware.com/docs/v6.5/resources/guidelines/code/core/benchmarks.md)  
::: info
This document represents core guidelines and has been mirrored from the core in our Shopware 6 repository.
You can find the original version [here](https://github.com/shopware/shopware/blob/trunk/coding-guidelines/core/benchmarks.md)
:::

# Benchmarks

Since the 6.4.11 version, we have run continuous performance benchmarks via [locust.io](https://locust.io/). We want to extend these benchmarks continuously. You can find the sources in the [src/Core/Devops/Locust](https://github.com/shopware/shopware/tree/trunk/src/Core/DevOps/Locust) folder. You can find all the information on setting up and running these tests in the [README.md](https://github.com/shopware/shopware/blob/trunk/src/Core/DevOps/Locust/README.md).

If you develop a new feature that impacts the store (storefront and/or store API), this functionality must be performance tested. It is not enough to rest on the fact that performance tests already exist and hope they will test it somehow. New functionality usually also needs a configuration which is not inside the existing mysqldump.

## Extend `setup.php`

The [`setup.php`](https://github.com/shopware/shopware/blob/trunk/src/Core/DevOps/Locust/setup.php) exports a fixture set which you can use inside the locust python files. Getting the data on demand via API would also be possible, but this would put additional load on the server and possibly falsify the results.

So if you need additional data to test your feature, you can write other .json files here. These will then be parsed in the [Context](https://github.com/shopware/shopware/blob/trunk/src/Core/DevOps/Locust/common/context.py) class and made available globally.

## Extend the scenarios

We have defined several [scenarios](https://github.com/shopware/shopware/tree/trunk/src/Core/DevOps/Locust/scenarios) in locust.

You have to customize the following scenarios under the following conditions:

* API-benchmark.py > Here, we test the performance of our API for ERP imports.
  * API Write / Sync processes extended
  * Indexing process of products or categories
* integration-benchmark.py > In this scenario, we test everything
  * Always
* Nvidia-benchmark.py > In this scenario, we test many orders per second
  * Changes to the order process
  * Changes to `available_stock`
  * Changes to the product detail page
* store-API-benchmark.py > In this scenario, we test our store API routes
  * If you have added a new store API route
  * If you have added a function to an existing store API
* storefront-benchmark.py > Here, we test only storefront routes without a shopping cart
  * If you have added new functions to the storefront

## Extend mysqldump

If the new feature needs new data, the mysqldump of the demo-data environment must be adjusted. For example, if you implement a new CMS element, it is essential, that this element is used somewhere. Otherwise, this element will never be considered when running the performance tests.

Since the mysqldump is static and defined as a snapshot on our servers, it is not easy to manipulate it.

Therefore, you should build a script that can manipulate an existing system to add the necessary data for you.
Let's take product ratings as an example. In the script, you would simply add ten ratings to each product, which are randomly generated.

Test the script locally and build your locust scenarios based on the results. Once you have met all criteria for a merge, create a merge request and add the @ct-core team as reviewers. You should put the script to adjust the dump in the merge request description.

@ct-core will do a review of your script and your performance tests. Once the review is successful, please contact @ct-core team to spawn the mysql server. Afterwards you can manipulate the dump and @ct-core create a new snapshot.

Since we also test other dumps, you must program the locust scenarios so that the results are not affected if your data (fixtures) does not exist.

---

---

## Introduction
**Source:** [resources/guidelines/code/core/database-migations.md](https://developer.shopware.com/docs/resources/guidelines/code/core/database-migations.md)  
## Introduction

Changing the database structure of Shopware is an important and sensitive topic, because it can effect the installation of customers and their data in many ways.
Therefore, it is important for every developer to understand the core principles of database migrations, also in the case of backward compatibility.

Migrations in Shopware are grouped by major versions.
This allows for a sane execution of destructive migrations on customer systems.
Database changes in minor or patch releases should always be non-destructive.
See [backward compatibility](#backward-compatibility) for more information.

## Create a migration

Use `bin/console database:create-migration` to create a new migration in the current major namespace.

Make sure to always test your migration against the defined rule set -> [Important Rules](#important-rules)

## The migration class

Migrations are created in their own major version namespace.
As an example, migrations which should not run before the `v6.5.0.0` are located in the `Core\Migration\V6_5` namespace.

The migration consists of two separated steps: `update` and `updateDestructive`.

## Backward compatibility

As every other change, also your database changes should always be [backward compatible](/docs/resources/guidelines/code/backward-compatibility.html) for minor and patch releases and support blue-green deployment.
A common technique is the [expand and contract](https://www.tim-wellhausen.de/papers/ExpandAndContract/ExpandAndContract.html) pattern, which will help you to implement your changes in a backward compatible way.

* **Expand**: Instead of renaming an existing column, create a new column with the updated name. (non-destructive)
* **Migrate**: Move the data from the old column to the new column.
* **Contract**: Once you verify that your code is functioning correctly with the new column, then delete the old column and make it non-existent.
  This must only be done in the `updateDestructive` method.

### Mode for executing destructive changes

There are different `version-selection-modes` for customers to choose from when executing migrations.

> **NOTE:** The default mode is `mode=safe`.

## Migration execution order

Migrations are executed in following order.

1. migrations from v6\_3 namespace
2. migrations from v6\_4 namespace
3. migrations from v6\_5 namespace\
   ...
4. core 'legacy' migrations

> **HINT:** You can run migrations specific to a major version with `bin/console database:migrate --all core.V6_7` where `core.V6_7` represents the major version you want to execute.

***

## Important Rules

**To ensure the stability of updates and the software itself, it is imperative that the following rules are always followed when creating new migrations.**

***

::: info
This document represents core guidelines and has been mirrored from the core in our Shopware 6 repository.
You can find the original version [here](https://github.com/shopware/shopware/blob/trunk/coding-guidelines/core/database-migations.md)
:::

### 1. NEVER change an executed migration

You cannot alter an executed, or already released, migration.
If the migration was not yet part of a public release, you can still change it.
For example, the current major is 6.6, so you can still change migrations in the 6.7 migrations folder.
If the migration was executed already, you need to write a new migration to do the changes.
Otherwise, an existing system will not have the same structure after an update as a new installation.
The only exception is when a migration was incorrectly created and causes errors.

### 2. Migrations must be able to be executed more than once

If a migration fails, make sure that it can be executed again.
A failure can happen for various reasons, such as a timeout, a connection error, or a syntax error.
A migration should check whether structures have already been created to avoid creating duplicates.

You can easily achieve this by adding the `IF [NOT] EXISTS` condition to commands like `CREATE TABLE` or `DROP TABLE`.
There are also helper methods available to check for the existence of a table or column. E.g.:

* `\Shopware\Core\Framework\Migration\MigrationStep::dropTableIfExists`
* `\Shopware\Core\Framework\Migration\MigrationStep::dropColumnIfExists`
* `\Shopware\Core\Framework\Migration\AddColumnTrait::columnExists`

> **NOTE:** Commands like `ALTER TABLE` however do not have a conditional `IF EXISTS` check. You **must** query the table for its columns manually.

### 3. Do not trust any identifier

Identifiers on a customer system can always be different from those on a development environment.
A database query for the identifier should be initiated in advance.

### 4. Do not trust data of customer environments

The data of production environments sometimes produce very confusing data constructs.
Therefore, never rely on the existence of data or structures.
Always program migrations very defensively with exact queries on the situation.

### 5. Don't hurt customized data

There is data that is often individualized by customers.
Under no circumstances may a migration overwrite individualized customer data.
Always check this in your migration.

This can easily be done by checking, whether the `updated_at` field is `null`:

```mysql
UPDATE `product` SET name = 'foobar' WHERE updated_at IS NULL;
```

### 6. Performance / Duration

A migration must never take longer than 10 seconds on your local system.
We do not know the timeout values of the customers, so this value should never be exceeded.
Customer systems may be slower than developer systems, and contain a lot of data.
Make sure to test your migration with big data sets.

### 7. There are no default languages

The customers can select any language as their default.
Don't rely on any language as given, neither English nor German.

Use the `ImportTranslationsTrait` to your advantage:

```php
// src/Core/Migration/V6_3/Migration1595422169AddProductSorting.php

...
use Shopware\Core\Migration\Traits\ImportTranslationsTrait;
...

public function createDefaultSortingsWithTranslations(Connection $connection): void
{
    // hard-coded default data coming with the release of product-sortings
    foreach ($this->getDefaultSortings() as $sorting) {
        $connection->insert(ProductSortingDefinition::ENTITY_NAME, $sorting);

        $translations = new Translations(
            ['product_sorting_id' => $sorting['id'], 'label' => $sorting['translations']['de-DE']],
            ['product_sorting_id' => $sorting['id'], 'label' => $sorting['translations']['en-GB']]
        );

        $this->importTranslation('product_sorting_translation', $translations, $connection);
    }
}
```

### 8. Migration Tests

For each migration you write you need to write a test, that verifies that the migration works as expected and adheres to the guidelines stated above.
Place your migration test inside the `tests/Migration/V6_*` folder.
To make those tests fast to run and easier to understand you should not use any of the "legacy test behaviours" like `IntegrationTestBehaviour` or `KernelTestBehaviour`.
You should also especially not rely on the kernel being booted and the service container being available.
To test your migration you can get a database connection via `KernelLifecycleManager::getConnection()`.
Besides obviously relying on the database, the migration tests should behave like unit tests and rely on nothing else external.

**Be careful with implicit commits**

If data is updated in a migration, a test must be written for this migration.
You can use database transactions in your migration tests to keep the database tidy after each test.
For that use the `MigrationTestTrait` trait, which encapsulates your migration test in a database transaction.

Unfortunately, database transactions won't work with DDL commands.
DDL commands will fire an implicit commit and end an active transaction.

> https://dev.mysql.com/doc/refman/8.0/en/implicit-commit.html

All DDL commands **must** be done outside of transactions.
Therefore, you **must** undo your DDL commands manually after the test and it is best to handle the transaction start and rollback manually in your test and not rely on the `MigrationTestTrait`.

**Obsolete migration tests**

Migrations run in a specified order, therefore they may rely on a specific state (columns present, triggers active etc.) in the DB.
However, you can not expect a specific state inside your migration tests, as all migrations are already executed when the migration tests are run.
The destructive part of the migration you are testing may already be run or not, also a new migration may have altered the current state of the DB in the meantime etc.
If your test relies on a specific state, you should create that state explicitly in your test.
Do to that you could do:

1. Rename the table your migration relies on to temporary name
2. Recreate the table manually with the state (columns present, triggers active etc.) your test needs
3. Run your migration test
4. Drop your newly created table and rename the temporary table back to the original name

### 9. Database Table Naming

When naming database tables, it's essential to steer clear of prefixes like 'swag\_' that were historically used for plugins.
This practice is crucial for maintaining database consistency.
Additionally, ensure you assign suitable names to the tables that accurately represent their content and purpose.

Dos:
For instance, when creating a database table that stores customer information, a suitable name could be 'customer\_data' or just 'customer'.
This follows the practice of using descriptive, singular, snake case names that align with the table's purpose.

Don'ts:
On the other hand, avoid using prefixes such as 'swag\_' as seen in past plugins.
For example, refraining from naming a table 'swag\_order\_history' ensures better scalability, clarity, and uniformity within the database schema.

---

---

## Decorator pattern
**Source:** [resources/guidelines/code/core/decorator-pattern.md](https://developer.shopware.com/docs/v6.6/resources/guidelines/code/core/decorator-pattern.md)  
::: info
This document represents core guidelines and has been mirrored from the core in our Shopware 6 repository.
You can find the original version [here](https://github.com/shopware/shopware/blob/trunk/coding-guidelines/core/decorator-pattern.md)
:::

# Decorator pattern

The decorator pattern is a design pattern that allows behavior to be added to an individual object, either statically or dynamically, without affecting the behavior of other objects from the same class.

## When to use the decorator pattern

You should choose the decorator pattern, when you want that other developers can extend your functionality. The most common use case is that other developers should be allowed to decorate or rewrite your DI container services.

https://symfony.com/doc/current/service\_container/service\_decoration.html

## How to use the decorator pattern

Instead of interfaces, we use abstract classes to define the base functionality of a service. This allows us to add more functions without breaking existing code. This decision was made in this [ADR](https://github.com/shopware/shopware/blob/trunk/adr/2020-11-25-decoration-pattern.md).

## Rules for the decorator pattern

When defining a service, which should be decorated, you have to follow these rules:

* The abstract class has to implement a `getDecorated()` function which returns the abstract class.
* The core service has to throw a `DecorationPatternException` if the `getDecorated()` function is called.
* The abstract class **can not** be marked as `@internal` or `@final`
* An implementation of the abstract class **can not** provide any other public functions than the ones defined in the abstract class.
* Implementations of the abstract class **can not** act as an event subscriber, symfony event system **can not** handle this correctly.

These rules are enforced by the `\Shopware\Core\DevOps\StaticAnalyze\PHPStan\Rules\DecorationPatternRule` class.

## Example

```php
abstract class AbstractRuleLoader
{
    abstract public function getDecorated(): AbstractRuleLoader;

    abstract public function load(Context $context): RuleCollection;
}

class CoreRuleLoader
{
    public function getDecorated(): AbstractRuleLoader {
        throw new DecorationPatternException(self::class);
    }
    
    public function load(Context $context): RuleCollection {
        // do some stuff 
    }
}

class SomePlugin extends AbstractRuleLoader
{
    public function __construct(private AbstractRuleLoader $inner) {}
    
    public function getDecorated(): AbstractRuleLoader {
        return $this->inner;
    }
    
    public function load(Context $context): RuleCollection {
        $rules = $this->inner->load($context);
        // add some data or execute some logic
        return $rules;
    }
}
```

When you add a new functionality to such a service, you have to add it to the abstract class but not as abstract function. This allows you to add new functions without breaking existing code.

```php
abstract class AbstractRuleLoader
{
    abstract public function getDecorated(): AbstractRuleLoader;

    abstract public function load(Context $context): RuleCollection;

    // introduced with shopware/shopware v6.6
    public function create(Context $context): RuleCollection 
    {
        return $this->getDecorated()->create($context);
    }
}
```

## Alternative

Sometimes you want to decorate your own service but don't want to allow other developers to do it.

This can be the case when you "just" want to implement a logging or cache layer around your service or when you have to adjust something in our cloud product.

In this case, you should not use the decorator pattern described above and only inject the inner service and delegate the calls to it.

In this case you should mark the service as follows:

* if this is private api and should not be used by other developers, mark all classes as `@internal`
* if you want that developers can call public functions of your service but should not extend it, mark all classes as `@final`

```php
abstract class AbstractRuleLoader
{
    abstract public function load(Context $context): RuleCollection;
}

/**
 * @final - if you want that developers can use your service
 */
class CachedLoader extends AbstractRuleLoader
{
    public function __construct(
        private readonly AbstractRuleLoader $decorated,
        private readonly CacheInterface $cache
    ) {
    }

    public function load(Context $context): RuleCollection {
        return $this->cache->get(
            self::CACHE_KEY, 
            fn (): RuleCollection => $this->decorated->load($context)
        );
    }
}
```

---

---

## Domain exceptions
**Source:** [resources/guidelines/code/core/domain-exceptions.md](https://developer.shopware.com/docs/v6.6/resources/guidelines/code/core/domain-exceptions.md)  
::: info
This document represents core guidelines and has been mirrored from the core in our Shopware 6 repository.
You can find the original version [here](https://github.com/shopware/shopware/blob/trunk/coding-guidelines/core/domain-exceptions.md)
:::

# Domain exceptions

To ensure a consistent exception handling, we introduced domain exceptions. These domain exceptions are a separate exception class for each domain within shopware. These classes are used as a factory for all exceptions within the domain. The \_\_construct of the DomainException is set to `private`, so that only the factory methods can create an instance.

Each domain exception class extends the `Shopware\Core\Framework\HttpException` class, which ensure a unique error code and http handling. Error codes of each domain exception class are unique within the domain. The error codes are defined within the corresponding domain exception.

Domain exception are always stored directly inside the top level domain in each area. Top level domains are:

* `Checkout\Cart`
* `Checkout\Customer`
* `Content\Category`
* `Content\Product`
* ...

This decision was made in this [ADR](https://github.com/shopware/shopware/blob/71ef1dffc97a131069cd4649f71ba35d04771e24/adr/2022-02-24-domain-exceptions.md).

## Example

```php
<?php declare(strict_types=1);

namespace Shopware\Core\Checkout\Customer;

#[Package('customer-order')]
class CustomerException extends HttpException
{
    public const CUSTOMER_GROUP_NOT_FOUND = 'CHECKOUT__CUSTOMER_GROUP_NOT_FOUND';

    public static function customerGroupNotFound(string $id): self
    {
        return new self(
            Response::HTTP_BAD_REQUEST,
            self::CUSTOMER_GROUP_NOT_FOUND,
            'Customer group with id "{{ id }}" not found',
            ['id' => $id]
        );
    }
}
```

## Exceptions which should be catchable

However, the DomainExceptions are not (necessarily) made to be caught and handled in a try-catch. Therefore, we will continue to implement own exception classes, for exceptions that we want to catch ourselves in the system via a try-catch, which extends the DomainException. These exceptions are then stored in an exception sub folder:

```php
<?php declare(strict_types=1);

namespace Shopware\Core\Checkout\Customer;

#[Package('customer-order')]
class CustomerException extends HttpException
{
    public const CUSTOMER_GROUP_NOT_FOUND = 'CHECKOUT__CUSTOMER_GROUP_NOT_FOUND';

    public static function notFound(string $id): self
    {
        return new CustomerNotFoundException(
            Response::HTTP_BAD_REQUEST,
            self::CUSTOMER_GROUP_NOT_FOUND,
            'Customer group with id "{{ id }}" not found',
            ['id' => $id]
        );
    }
}

<?php declare(strict_types=1);

namespace Shopware\Core\Checkout\Customer\Exception;

use Shopware\Core\Checkout\Customer\CustomerException;

class CustomerNotFoundException extends CustomerException
{
}
```

## Http status code

Each specific type of domain exceptions should provide a specific http status code. Please use the following official http status defined by [https://developer.mozilla.org](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status)

---

---

## Extendability
**Source:** [resources/guidelines/code/core/extendability.md](https://developer.shopware.com/docs/v6.6/resources/guidelines/code/core/extendability.md)  
::: info
This document represents core guidelines and has been mirrored from the core in our Shopware 6 repository.
You can find the original version [here](https://github.com/shopware/shopware/blob/trunk/coding-guidelines/core/extendability.md)
:::

# Extendability

The Extendability of our software and its features is an essential part of development. Enabling external companies, but also ourselves, to customize our software so that it can be adapted to different business cases is the foundation for the success of our software.

Regarding software extendability, different business cases and requirements must be considered, according to which we must also build the architecture of the software.

The requirements are divided into technical requirements and business requirements.

## Technical requirements

When talking about technical requirements, we talk about how we have to design our software for different extension use cases. These use cases include:

* Functional extensibility
  * It should be possible to extend the feature with additional features.
  * Ex: Extend the enterprise search by a suggestion feature
* Functional modifiability
  * You can rewrite the feature in certain areas to modify the functionality.
  * Ex: Implementing tax calculation for America via tax providers
* Functional differentiation
  * The feature should be able to be extended in such a way that certain parts of the software are liable to pay costs.
  * Ex: With the XXX software version, you should be able to unlock another feature.
* Functional exchange market
  * The feature is to be replaced entirely by an external solution
  * Ex: An external newsletter system should be connected

## Business requirements

When talking about business requirements, we talk about how the above technical requirements are used in different business cases. These business cases include:

* Marketplace extensions
  * We should build the software so everyone can easily provide new features in certain areas.
  * Ex: There should be a plugin to integrate a CMS Page publishing system
* Adaptive technologies
  * We must build certain technical areas so flexibly that we can use different technologies for this area.
  * Ex: Our listings should be able to be read via Elasticsearch for large systems.
* Environment specifications
  * We must program features so that they can resist different loads depending on the setup.
  * Ex: Assets should be able to be loaded via CDN as there are several App Servers.

## Approaches

These business cases are realized with the following three conceptual approaches:

* Project templates
  * Large customers have their deployments in which they deploy a fork of our production template.
  * In project templates, local customizations are not implemented as a plugin but as a bundle.
  * We have a SaaS product that has special configurations for cloud compatibility
* Apps
  * Apps provide minor extensions for our system
  * The app technology is designed for use in cloud products
* Plugins
  * Plugins can provide larger extensions to the system
  * Plugin technology is designed to replace all areas in Shopware

## Patterns

All the above requirements and approaches are based on different design patterns within our architecture. To realize the extensibility, we use the following patterns, which allow the third-party developer to extend our software:

* Decoration
* Factory
* Visitor
* Mediator
* Adapter

### Decoration

With the Decoration pattern, we make it possible to replace or extend certain areas in Shopware completely. We often use this pattern for our Store API routes to provide more functionality in the Store API. Another use case is the **functional replacement market** case, where we can completely replace features with other technologies or external libraries.

An example Store API route is the CategoryRoute. For this route, there is an [Abstract class](https://github.com/shopware/shopware/blob/v6.4.12.0/src/Core/Content/Category/SalesChannel/AbstractCategoryRoute.php) to which we type behind a [Concrete implementation](https://github.com/shopware/shopware/blob/v6.4.12.0/src/Core/Content/Category/SalesChannel/CategoryRoute.php) and a [Cache decorator](https://github.com/shopware/shopware/blob/v6.4.12.0/src/Core/Content/Category/SalesChannel/CachedCategoryRoute.php)

### Factory

The factory pattern is often used when we have to interpret user input and validate or enrich this input before it is passed to the application.
One use case for the factory pattern is the **Functional extensibility**, to allow third-party developers to add new factories, which allow other user input.

A good example is the [line item factory registry](https://github.com/shopware/shopware/blob/v6.4.12.0/src/Core/Checkout/Cart/LineItemFactoryRegistry.php). This registry is used when an item is to be added to the shopping cart via store-API. [The corresponding handler](https://github.com/shopware/shopware/blob/v6.4.12.0/src/Core/Checkout/Cart/LineItemFactoryHandler/ProductLineItemFactory.php) is responsible for the instantiation of the line item and enriches it with necessary data.

### Visitor

The visitor pattern is often used when we process some objects within our application. This pattern is often used to fit the **Functional extensibility** and **Functional modifiability** requirements. In theory, after or before the core visitors are executed, the third party visitors are executed, and they can visit the objects and manipulate or extend the processed data beforehand or afterward to manipulate the result.

A good example of the visitor pattern is the [cart processor](https://github.com/shopware/shopware/blob/v6.4.12.0/src/Core/Checkout/Cart/Processor.php). The processor calls all line item processors, like the [product cart process](https://github.com/shopware/shopware/blob/v6.4.12.0/src/Core/Content/Product/Cart/ProductCartProcessor.php), to modify the provided cart object and transport the line items from the previous cart to the calculated.

### Mediator

We often use this pattern to realize **functional extensibility** and **functional modifiability** to manipulate data or extend it with additional data sources. The best-known example of this pattern in our application is Events. We use events to create different entry points for developers to trigger specific processes.

The best-known example is the [`checkout.order.placed`](https://github.com/shopware/shopware/blob/v6.4.12.0/src/Core/Checkout/Cart/Event/CheckoutOrderPlacedEvent.php) event. This event is [dispatched](https://github.com/shopware/shopware/blob/v6.4.12.0/src/Core/Checkout/Cart/SalesChannel/CartOrderRoute.php#L151) as soon as an order is created in the system. However, over time, it has been shown that it is best practice not to pass objects or entities around in events, but only a corresponding primary key so that the connected listeners can determine the data for themselves. Furthermore, possible asynchronous processing of the underlying processes is easier to realize this way. An optimized variant of this event would not contain the `private OrderEntity $order;` but only the primary key for the order `private string $orderId;`.

#### Hooks

Hooks are another good example of the observer pattern. Hooks are entry points for apps in which the so-called [**App scripts**](/docs/guides/plugins/apps/app-scripts/) is enabled. Since apps do not have the permission to execute code on the server directly, hooks are a way to execute more complex business logic within the request without having to address the own app server via HTTP. Hooks are the equivalent of **events**.

One of the best-known hooks is the [`product page loaded hook`](https://github.com/shopware/shopware/blob/v6.4.12.0/src/Storefront/Page/Product/ProductPageLoadedHook.php). This hook allows apps to load additional data on the product detail page. The hook is instantiated and dispatched [at controller level](https://github.com/shopware/shopware/blob/v6.4.12.0/src/Storefront/Controller/ProductController.php#L100). Each app script, which is registered to the hook, is executed.

### Adapter

The adapter pattern is perfectly designed for **Functional exchange market**. We often realize this by allowing the user to do some configuration and select a corresponding adapter. These adapters are usually registered inside a registry, and third-party developers can easily add new adapters via events or via tagged services.

A good example is the captcha implementation. The store owner can configure a [captcha type](https://docs.shopware.com/en/shopware-en/settings/basic-information#captcha), and we then use the [corresponding adapter](https://github.com/shopware/shopware/blob/v6.4.12.0/src/Storefront/Framework/Captcha/HoneypotCaptcha.php#L11) in the code for the configured captcha.

---

---

## Introduction
**Source:** [resources/guidelines/code/core/feature-flags.md](https://developer.shopware.com/docs/resources/guidelines/code/core/feature-flags.md)  
::: info
This document represents core guidelines and has been mirrored from the core in our Shopware 6 repository.
You can find the original version [here](https://github.com/shopware/shopware/blob/trunk/coding-guidelines/core/feature-flags.md)
:::

## Introduction

Feature flags enable the developer to create new code which is hidden behind the flag and merge it into the trunk branch, even when the code is not finalized.
We use this functionality to merge breaks into the trunk early, without them already being switched active. To learn more about breaking changes and backward compability take a look to our [Backward Compatibility Guide](/docs/resources/guidelines/code/backward-compatibility.html)

### Activating the flag

To switch flags on and off you can use the ***.env*** to configure each feature flag. Using dots inside an env variable are not allowed, so we use underscore instead:

```
V6_5_0_0=1
```

## Using flags in PHP

The feature flag can be used in PHP to make specific code parts only executable when the flag is active.

### Using flags in methods

When there is no option via the container you can use additional helper functions:

```php
use Shopware\Core\Framework\Feature;
 
class ApiController
{

  public function indexAction(Request $request)
  {
    // some old stuff
    Feature::ifActiveCall('v6.5.0.0', $this, 'handleNewFeature', $request);
    // some old stuff
  }

  private function handleNewFeature(Request $request)
  {
    // awesome new stuff
  }
}
```

You can also do it in a callback:

```php
use Shopware\Core\Framework\Feature;
 
class ApiController
{
  public function indexAction(Request $request)
  {
    // some old stuff
    Feature::ifActive('v6.5.0.0', function() use ($request) {
      // awesome stuff
    });
    // some old stuff
  }
}
```

And you can use it for conditions:

```php
use Shopware\Core\Framework\Feature;
 
class ApiController
{
  public function indexAction(Request $request)
  {
    // some old stuff
    if (!Feature::isActive('v6.5.0.0')) {
      //some old stuff
      return;
    }
    // awesome new stuff
  }
}
```

Putting the old behaviuor inside the if block makes it easier to remove the feature flag later on.

And you can use it simply to throw exceptions:

```php
use Shopware\Core\Framework\Feature;
 
/**
 * @deprecated tag:v6.5.0 - Class is deprecated, use ... instead
 */
class ApiController
{
  public function indexAction(Request $request)
  {
     Feature::triggerDeprecationOrThrow('v6.5.0.0', 'Class is deprecated, use ... instead');
  }
}
```

### Using flags in tests

You can flag a test by using the corresponding helper function. This can also be used in the `setUp()` method.

```php
use Shopware\Core\Framework\Feature;
 
class ProductTest
{
  public function testNewFeature() 
  {
     Feature::skipTestIfActive('v6.5.0.0', $this);

     // test code
  }
}
```

## Using flags in the administration

Also in the JavaScript code of the administration the flags can be used in various ways.

### Using flags for modules

You can also hide complete admin modules behind a flag:

```javascript
 
Module.register('sw-awesome', {
    flag: 'v6.5.0.0',
    ...
});
```

### Using flags in JavaScript

To use a flag in a VueJS component you can inject the feature service and use it.

```
inject: ['feature'],
...
featureIsActive(flag) {
    return this.feature.isActive(flag);
},
```

### Using flags in templates

When you want to toggle different parts of the template you can use the flag in a VueJs condition if you injected the service in the module:

```html
<sw-field type="text" v-if="feature.isActive('v6.5.0.0')"></sw-field>
```

### Using flags in config.xml

When you want to toggle config input fields in config.xml like [basicInformatation.xml](https://gitlab.shopware.com/shopware/6/product/platform/-/blob/trunk/src/Core/System/Resources/config/basicInformation.xml), you can add a `flag` element like this:

```xml
<input-field type="bool" flag="v6.5.0.0">
  <name>showTitleField</name>
  <label>Show title</label>
  <label lang="de-DE">Titel anzeigen</label>
  <flag>v6.5.0.0</flag>
</input-field>
```

## Using flags in the storefront

In the Storefront it works nearly similar to the admin.

### Using flags in storefront JavaScript

```
import Feature from 'src/helper/feature.helper';
...
data() {
   if (Feature.isActive('v6.5.0.0')) {
        console.log('v6.5.0.0 is active')
   }
 };
```

### Using flags in storefront templates

```
{% if feature('v6.5.0.0') %}
    <span>Feature is active</span>
{% endif %}
```

## Using flags in plugins

Feature flags can also be used in plugins. Among other things, by adding your own flags, but also the use of the major feature flag is an intended use case.

### Major feature flag

As mentioned before, we use the major feature flags (`v6.5.0.0`, `v6.6.0.0`) to signal breaks within the code ahead of time. This is an incredible help in the preparation of the next major release, as otherwise all breaks would have to be made within a short period of time.

This procedure can also be applied to plugins, which also use this flag and internally query it to either prepare the plugin for the next major or to support multiple Shopware major versions with one plugin version. Since each major feature flag remains after the corresponding release, they can be used as an alternative version switch to the php equivalent `version_compare`.

### Own plugin flags

This is internal only and we may break this behaviour at any time!

When you need to implement a feature flag for a plugin you can't edit the feature.yaml or provide an override for it,
so you have to register the new flag "on the fly".

```php
    private const FEATURE_FLAGS = [
        'paypal:v1.0.0.0'
    ];
...
    public function boot(): void
    {
        Feature::setRegisteredFeatures(
            array_merge(array_keys(Feature::getAll()), self::FEATURE_FLAGS),
            $this->container->getParameter('kernel.cache_dir') . '/shopware_features.php'
        );
...
```

Now your own feature flag can be handled like every core flag.

---

---

## Final and internal annotation
**Source:** [resources/guidelines/code/core/final-and-internal.md](https://developer.shopware.com/docs/v6.6/resources/guidelines/code/core/final-and-internal.md)  
::: info
This document represents core guidelines and has been mirrored from the core in our Shopware 6 repository.
You can find the original version [here](https://github.com/shopware/shopware/blob/trunk/coding-guidelines/core/final-and-internal.md)
:::

# Final and internal annotation

We use `@final` and `@internal` annotations to mark classes as final or internal. This allows us to mark services and classes as public or private API and to define which breaking changes can be expected.

## Final

We mark classes as `@final` when developers can use the class but should not extend it.

Following changes of the class are allowed:

* Adding new public methods/properties/constants
* Adding new optional parameters to public methods
* Protected and private methods/properties/constants can be changed without any restrictions.
* Widening the type of public method params

Following changes of the class are not allowed:

* Removing public methods/properties/constants
* Removing public methods parameters
* Narrowing the type of public methods/properties/constants

Due to the fact that we "only" mark the classes as `@final` via doc annotation, it is possible for developers to extend the base class and replace the service in the DI container. This is not recommended and should be avoided. But it is possible and without any guarantees.

## Internal

We mark classes as `@internal` when the class is private API and should not be used or extended by other developers.

This means that we can change the class without any restrictions and we also can remove the class without any deprecation.

Due to the fact that we "only" mark the class as `@internal` via doc annotation, it is possible for developers to use the class or replace the service. This is not recommended and should be avoided. But it is possible and without any guarantees.

---

---

## Internal
**Source:** [resources/guidelines/code/core/internal.md](https://developer.shopware.com/docs/v6.6/resources/guidelines/code/core/internal.md)  
::: info
This document represents core guidelines and has been mirrored from the core in our Shopware 6 repository.
You can find the original version [here](https://github.com/shopware/shopware/blob/trunk/coding-guidelines/core/internal.md)
:::

# Internal

All classes and elements (methods, properties, constants) that are defined as protected or public are initially Public API for third party developers.

The Shopware Public API must be kept compatible with each release. This means that the following must not change for third party developers in a minor release:

* The developer uses a service to use certain functions.
* The developer decorates a service to extend its functionality.
* The developer uses DTO to get or pass data.

There are various other use-cases for third party developers, but the above reflect the standards.

However, if all classes and properties had to be considered public api by us, we would be very limited in our work.

Therefore, we mark the elements that we do not consider to be public API. To do this, we have the following tools at our disposal.

## Decoration pattern

Classes that are intended for **service decoration** are provided with an abstract class. This class is then provided with a `getDecorated` function to pass unimplemented functions directly to the core classes. [Read more](https://github.com/shopware/shopware/blob/trunk/adr/2020-11-25-decoration-pattern.md)

## Final classes

Tendentiously, just about all classes in Shopware should be declared as `final`. We do this for the following reasons:

* We declare a DI container service as `final` so that it will not be extended. All services that can be exchanged via DI-Container have an `abstract class` implementation. Per `extends` from core services is not intended.
* We declare **DTO classes** as `final` to indicate that we do not intend third party developers to derive from these classes. To append more data to DTO's we use the base `Struct` class which allows **Extensions**.
* We declare **Event Subscriber** as `final` as we do not foresee deriving from them in order to leverage the events or extend their functionality.

Classes that we declare as `final` are still Public API, because **Third Party Developers are consumers** of these classes. That means they access the public methods and functions of the classes.

## Internal annotation

Classes where we want to reserve a complete **refactoring** or where we only implemented them to not implement "a big master class" in a domain, we mark them with the doc block `@internal`.

Classes with this annotation may change completely with each release and are therefore not intended for use by third party developers.

## Internal interfaces

We declare interfaces as `@internal` when we want to implement multiple implementations of a feature or adapter, but do not want third party developers to interfere in this area of the software. A good example of this is the Data Abstraction layer and the Field and FieldSerializer classes. In such areas of the domain we want to reserve optimizations and breaks within minor versions but still be able to work with interfaces and abstract classes.

---

---

## Unit tests
**Source:** [resources/guidelines/code/core/unit-tests.md](https://developer.shopware.com/docs/v6.6/resources/guidelines/code/core/unit-tests.md)  
::: info
This document represents core guidelines and has been mirrored from the core in our Shopware 6 repository.
You can find the original version [here](https://github.com/shopware/shopware/blob/trunk/coding-guidelines/core/unit-tests.md)
:::

# Unit tests

Unit tests are an essential part of our software. The Shopware product grows and grows, the release cycles become shorter and shorter, more and more developers work with the software.

**Therefore it is important that all functionalities and services are fully unit tested.**

When writing unit tests, the following is important:

* **"100% coverage "** - This does not mean that simply a high code coverage should be generated, but that all use cases of each individual service is tested.
* **Performance** - As we grow more and more it is advisable to pay attention to the speed of the tests.
* **Mocking** - Don't be lazy but deal with mock objects to optimize for example database access. So you don't have to persist every storage case before but you can describe it as a Mock.
* **Readable** - You are not the only one who maintains the code. Therefore, it is important that others can quickly and easily understand your unit tests and extend them with additional cases.
* **Extensibility** - It is important that when more cases are added or certain cases are not tested that it is easy to extend your unit tests with another case without extending dozens of lines of code.
* **Modularity** - Your test should not fail just because another test left artifacts (files, storage records, ...).
* **Cleanup** - It is also important that you clean up your artifacts. If you register an event listener dynamically, make sure that it is removed again on `teardown`. If you write data to the database or change the schema, make sure it is rolled back.
* **Failure** - Don't just test the happy case or success case, test the failure of your services and objects.
* **Unit** - Write unit tests (not integration tests), don't always test the whole request or service stack, you can also just instantiate services yourself and mock dependencies to make testing faster and easier.
* **Para-test** - Your tests should be compatible with our para-test setup so that any developer can quickly run the tests locally.

## Examples

Here are some good examples of shopware unit tests:

* [CriteriaTest](https://github.com/shopware/shopware/blob/trunk/tests/unit/Core/Framework/DataAbstractionLayer/Search/CriteriaTest.php)
  * Good example for simple DTO tests
* [CashRounding](https://github.com/shopware/shopware/blob/trunk/tests/unit/Core/Checkout/Cart/Price/CashRoundingTest.php)
  * Nice test matrix for single service coverage
* [AddCustomerTagActionTest](https://github.com/shopware/shopware/blob/trunk/tests/unit/Core/Content/Flow/Dispatching/Action/AddCustomerTagActionTest.php)
  * A good example of how to test flow actions and use mocks for repositories

Here are some good examples of integration tests:

* [ProductCartTest](https://github.com/shopware/shopware/blob/trunk/src/Core/Content/Test/Product/Cart/ProductCartTest.php)
  * Slim product cart test with good helper function integrations
* [CachedProductListingRouteTest](https://github.com/shopware/shopware/blob/trunk/src/Core/Content/Test/Product/SalesChannel/Listing/CachedProductListingRouteTest.php)
  * This test is a little complex, but has a very good test case matrix with good descriptions and reusable test code.

# Mocks and its influence on software design

When speaking about unit testing, one automatically also speaks about `mocks` and the need to mock away dependencies.
It seems to be quite a common attitude towards mocks along the lines of "Mock every external dependency of the class under test" and this attitude can be quite dangerous.
Therefore, here are some words of caution.

## Mocks are hard to refactor

Be cautious when utilizing mocks extensively because it can be hard to automatically refactor classes. This is because IDEs do not provide robust support for refactoring classes that are heavily mocked, and tools like *PHPStan* may not effectively detect these mock-related issues.

More broadly speaking, it is hard to guarantee that the mock behaves in the same/or intended manner as the real implementation (especially when the underlying implementation changes).

Use mocks only where you need to because:

1. creating the objects is hard as you need tons of nested dependencies to create the object.
   or
2. the class produces some side effects that you don't want in unit tests (e.g., DB writes).

For all other cases, use real implementations and rely as minimally as possible on the magic of phpunit's mocking framework.

## Focus on behavior, not implementation: Effective unit testing principles

Relying heavily on mocks creates a bad pattern in unit tests of testing `how` something is implemented and not `what` the implementation actually does. If tests are implemented in a mock-heavy way, they are tightly coupled to the implementation, meaning they rely on implementation details and may fail more often when the implementation details change than when the actual behavior of the class under test changes. Consider these two example changes to some classes:
Before:

```php
$id = $this->repository->search($criteria, $context)->first()?->getId();
```

After:

```php
$id = $this->repository->searchIds($criteria, $context)->firstId();
```

Before

```php
$values = $this->connection->fetchAllAssociative('SELECT first, second FROM foo ...');

$values = $this->mapToKeyValue($values);
```

After:

```php
$values = $this->connection->fetchKeyValue('SELECT first, second FROM foo ...');
```

By definition, both changes are a pure example of refactoring::

> Refactoring is a disciplined technique for restructuring an existing body of code, altering its internal structure without changing its external behavior.
> -> [Martin Fowler](https://refactoring.com/)

But when the unit test mocked the `repository` or `connection` dependencies the unit tests will fail after the change, even though the external behaviour (that's what a test should really test) was not changed.

Using mocks is ok in some cases, but not all.
Probably the examples from above are ones that are totally valid (as the mocked classes rely on a DB), which can be commonly encountered in real life.
Furthermore, the intention of this document is to keep you aware of the downsides that come with using mocks.

## Mocks might indicate your class is not well-designed

In a well-designed and testable system, it is relatively easy to isolate individual classes or modules and distinguish them between the components that contain the core business logic, which should be extensively unit tested, and the portions responsible for interfacing with the external environment and generating side effects. These side-effect-prone elements should be substituted in the unit tests. In fact, it is advisable to perform integration testing since their primary purpose is to abstract and facilitate the replacement of side effects in tests.

This kind of abstraction follows when you apply the principles of [Domain Driven Design](https://martinfowler.com/bliki/DomainDrivenDesign.html) and [Hexagonal Architecture](https://alistair.cockburn.us/hexagonal-architecture/) (aka Ports & Adapters)

The absence of such abstraction in the existing `shopware/shopware` codebase is one of the reasons why it is so hard to write "good" unit tests for shopware, but that does not mean that we should keep designing our code as we used and keep writing "bad" (meaning unit tests tightly coupled to the implementation) unit tests.
However, it's the opposite; we start designing our code in a way that makes it easy to write "good" unit test that does not rely that much on a "magic" mock framework.

So, a heavy reliance on mocks when writing unit tests can indicate a potential issue with the software design, suggesting insufficient encapsulation. Hence designing code to promote better encapsulation and reduce the need for extensive mocking is advisable. This can lead to improved testability and overall software quality.

## Better options than mocks

There are better options but that depends on the use cases. Here are a few alternatives:

1. Use the real implementation (this means the real thing is easy to create and does not produce side effects)
2. Use a hand-crafted dummy implementation of the real thing, that is easy to configure and behaves like a stub in that use case (this means that the real thing probably needs to be designed in a way to be easy to replace, examples of this in our test suite are the `StaticEntityRepository`  or `StaticSystemConfigService`)
3. Fallback to using phpunit's mocking framework (when the real thing is not designed to be replaced easily)

The way you design your codebase directly impacts whether you can rely on option 1 or option 2 without resorting to heavy mocking.

# Conclusion: Write tests first!

When you write tests first, most of the points described above should come out of the box!
Nobody who starts with a test would start with configuring a mock.

While we provide insights on this, it is essential to validate the information. So we encourage you to explore the following references to gain a deeper understanding and form your own opinion.

## References

Frank De Jonge on the exact same topic (with more examples in PHP): https://blog.frankdejonge.nl/testing-without-mocking-frameworks/

Martin Fowler on the differences between mocks (option 3) and stubs (option 2): https://martinfowler.com/articles/mocksArentStubs.html

Presentation by Mathias Noback on testing hexagonal architectures: https://matthiasnoback.nl/talk/a-testing-strategy-for-hexagonal-applications/

Some good real life examples on unit tests in php: https://github.com/sarven/unit-testing-tips

A great write up on testing in general: https://dannorth.net/2021/07/26/we-need-to-talk-about-testing/

Quite old (1997!) paper on how **not** to use code coverage: http://www.exampler.com/testing-com/writings/coverage.pdf

Great blog post series on how to avoid mocks: https://philippe.bourgau.net/categories/#how-to-avoid-mocks-series

---

---

## Writing code for static analysis
**Source:** [resources/guidelines/code/core/writing-code-for-static-analysis.md](https://developer.shopware.com/docs/v6.6/resources/guidelines/code/core/writing-code-for-static-analysis.md)  
::: info
This document represents core guidelines and has been mirrored from the core in our Shopware 6 repository.
You can find the original version [here](https://github.com/shopware/shopware/blob/trunk/coding-guidelines/core/writing-code-for-static-analysis.md)
:::

# Writing code for static analysis

We rely heavily on static analysis (read PHPStan) to ensure the quality of our code and enforce coding guidelines and best practices.
For static analysis to work properly, it is important that the code is written in a way that is understandable by static analysis tools, this mostly means that the code uses static types where possible, to catch a bunch of possible errors.

A main challenge is to narrow down the types when part of the code is implemented in a generic way and uses the dynamics that PHP offers.
This document will explain some of the approaches that can be used in those cases. They are presented in the order in which they should be used, the first one being the preferred one.

So this document mainly deals with issues on how to fix common PHPStan errors like:
`Can not call method getFoo() on Foo\\Bar|null.`
`Method Foo\\Bar::getFoo() expected first parameter to be string, but string|int|null given.`

## 1. Ensure the types at runtime with explicit checks

To ensure the types at runtime, the most common approach is to use an explicit type or null checks on the variable's values that we want to check.
**Examples:**

```php
$foo = $bar->getFoo(); // $foo is Foo|null, but we expect only Foo

if ($foo === null) {
    // handle the error case
    throw new \InvalidArgumentException('Foo must not be null');
}
```

or

```php
$foo = $bar->getFoo(); // $foo is mixed, but we expect only string

if (!is_string($foo)) {
    // handle the error case
    throw new \InvalidArgumentException('$foo must not be string');  
}
```

or

```php
$foo = $bar->getFoo(); // $foo is object, but we expect it to be Foo instance

if (!$foo instanceof Foo) {
    // handle the error case
    throw new \InvalidArgumentException('$foo must be instance of Foo');  
}
```

This approach catches type mismatches at runtime and ensures that the code is executed in a way that is expected to. It allows handling the error case explicitly as well, by throwing an error or returning a default value or something else entirely based on the specific case.

Runtime checks should be preferred as with them it is impossible to have type mismatches further down in the code.
The downside is that the error case has to be handled explicitly, which is a lot of overhead in cases where type mismatches may happen in theory (because technically the type hints allow mismatches), but for all practical reasons will never happen in reality.

### 1.1 Caution when using type casts

Type casts can be used as well to ensure types at runtime. However, this should not be the goto-solution, as PHP internally does a lot of [magic when casting](https://www.php.net/manual/en/language.types.type-juggling.php#language.types.typecasting) from one type to another.
Thus, it is possible that type cast may lead to unexpected results, e.g. casting null to an empty string where null was not expected in the first place. This makes catching those types of errors even harder, as type casts might hide the root cause of an error, that then only pops up later it in the code, where it is not obvious what caused the error.
Additionally, unexpected type casts cannot be caught by static analysis tools, so the effect of the cast has to be explicitly tested for.

This means you should only use type casts when you are sure what the possible inputs are and the result of the cast is actually what we would expect.

**Examples:**

```php
$foo = $bar->getFoo(); // $foo is mixed, but we expect only string

$foo = (string) $foo; // this might hide unexpected conversions from non-string values to string
```

### 1.2 Ensuring types in unit tests

In unit tests, the type ensuring asserts from PhpUnit can be used to ensure that the types are correct. Those are also evaluated at (test) runtime, thus they guarantee have full type safety.
This is especially useful as the error case in unit tests does not have to be handled manually, as the error will simply lead to a test failure when a type is encountered that was not expected.
**Examples:**

```php
$foo = $bar->getFoo(); // $foo is Foo|null, but we expect only Foo

static::assertNotNull($foo);
```

or

```php
$foo = $bar->getFoo(); // $foo is mixed, but we expect only string

static::assertIsString($foo);
```

or

```php
$foo = $bar->getFoo(); // $foo is object, but we expect it to be Foo instance

static::assertInstanceOf(Foo::class, $foo);
```

For unit tests, this approach should be preferred and there is basically no case where the other approaches further down this list should be used.

## 2. Ensure types during development and test with `assert()`

Instead of making the type checks explicitly and then having to handle the error case manually, [PHP's built in `assert()`](https://www.php.net/manual/en/function.assert.php) function can be used to ensure the types.
Those `asserts` work similar to explicit if-checks, the main difference is that assert checks can be turned off completely by configuration (which is the recommended setting for production setups).
This means that the `asserts` will only be evaluated in development and test environments (e.g. during local development and unit test execution), with the consequence that `asserts` don't guarantee full type safety as it might happen that in a prod environment unexpected things might happen, that where not encountered previously where the asserts where evaluated.
The upside of using `asserts` is that they will throw a generic `AssertionError` when the type is not as expected, which is a lot easier to handle than having to handle the error case manually.

**Examples:**

```php
$foo = $bar->getFoo(); // $foo is Foo|null, but we expect only Foo

assert($foo !== null);
```

or

```php
$foo = $bar->getFoo(); // $foo is mixed, but we expect only string

assert(is_string($foo));
```

or

```php
$foo = $bar->getFoo(); // $foo is object, but we expect it to be Foo instance

assert($foo instanceof Foo);
```

## 3. Narrow types during static analysis with `@var` annotations

Lastly it is possible to use `@var` annotations to narrow down types during static analysis.
Those annotations are evaluated by static analysis tools, but are ignored at runtime, which means that they offer no real type safety at runtime.
With the [latest PHPStan version](https://phpstan.org/blog/phpstan-1-10-comes-with-lie-detector) it is now able to detect cases where the `@var` annotations contradict with the real types specified on language level, but beside that there are no checks that the type we expect and specify as `@var` annotations are actually the correct types we get at runtime.
Which also means that wrong `@var` annotations can actively hide type mismatches that would otherwise be detected by static analysis tools.

Thus `@var` annotations should only be used when the other approaches are not possible or not feasible as a last resort.
**Examples:**

```php
/** @var Foo $foo */
$foo = $bar->getFoo(); // $foo is Foo|null, but we expect only Foo
```

or

```php
/** @var string $foo */
$foo = $bar->getFoo(); // $foo is mixed, but we expect only string
```

or

```php
/** @var Foo $foo */
$foo = $bar->getFoo(); // $foo is object, but we expect it to be Foo instance
```

## On `@var`, `@param` and `@return` annotations

`@var`, `@param` and `@return` annotations should only be used when they cover cases that you could not accomplish using language features alone.
This mainly includes:

* [Generics](https://phpstan.org/blog/generics-in-php-using-phpdocs)
* [Array shapes](https://phpstan.org/writing-php-code/phpdoc-types#array-shapes)
* special PHPStan types e.g. [class-string](https://phpstan.org/writing-php-code/phpdoc-types#class-string), [integer ranges](https://phpstan.org/writing-php-code/phpdoc-types#integer-ranges), etc

Note that `Intersection & Union Types` are not covered here, as they are now a native language feature and the language feature should be used instead.

---

---

## Dependency Injection and Dependency Handling
**Source:** [resources/guidelines/code/dependency-injection-dependency-handling.md](https://developer.shopware.com/docs/v6.6/resources/guidelines/code/dependency-injection-dependency-handling.md)  
# Dependency Injection and Dependency Handling

Within the Core domain, it is not allowed to access the PHP session. There is only one PHP session if it is a storefront request. The appropriate implementation and consideration of session data must be handled in the Storefront domain.

---

---

## Document Code
**Source:** [resources/guidelines/code/document-code.md](https://developer.shopware.com/docs/v6.6/resources/guidelines/code/document-code.md)  
# Document Code

* Methods of interfaces or abstract classes should always have a doc block describing what the function is used for and what is to be observed in the function. This should serve to clarify what an implementation has to take into account.
* Unnecessary doc block lines should always be avoided. This includes the `@param` and `@return` annotations as long as this is already defined by type hints.
* In a doc block, all exceptions thrown directly by the function should be documented via `@throws` annotation.
* Exceptions that could be thrown by a library are not included in the doc blocks.

---

---

## Events
**Source:** [resources/guidelines/code/events.md](https://developer.shopware.com/docs/v6.6/resources/guidelines/code/events.md)  
# Events

* An event must always implement the `\Shopware\Core\Framework\Event\ShopwareEvent` interface.
* Events thrown in the context of a sales channel must always implement the interfaces `ShopwareSalesChannelEvent` and `Shopware\Core\Framework\Event\SalesChannelAware`.
* Events are mostly used to allow developers to load more data. They should, as a rule, not interfere with the program flow. The decoration pattern is intended for influencing the program flow.

---

---

## Page Loader
**Source:** [resources/guidelines/code/pageloader.md](https://developer.shopware.com/docs/v6.6/resources/guidelines/code/pageloader.md)  
# Page Loader

* Pageloaders must be divided into appropriate domains that represent the different sections of the Storefront - "products", "account", etc.
* Each page loader must have an abstract class from which it derives ( See [decoration pattern](../../references/adr/2020-11-25-decoration-pattern.md)). This pattern can be used to completely replace the page loader in a project.
* Each page loader has a page object to return, in which all the necessary information for the page is present.
* At the end of each pageloader, an individual `PageLoaded` event is thrown. This event can be used to provide further data by third-party developers.
* Page loaders are not allowed to work directly with repositories but are only allowed to load data via the Store API. This is to ensure that all storefront functionalities can also be accessed via the Store API.
* A Page object must always extend from the base `\Shopware\Storefront\Page\Page` class.

---

---

## Platform Domains
**Source:** [resources/guidelines/code/platform-domains.md](https://developer.shopware.com/docs/v6.6/resources/guidelines/code/platform-domains.md)  
# Platform Domains

* The `Core` domain must not have any dependency on any of the other domains. This means that neither classes nor assets from `Storefront`, `Administration` or `Elasticsearch` may be used within the `Core` domain.
* The `Administration` domain may have dependencies on the `Core` domain but not on the `Storefront` or `Elasticsearch` domain.
* The `Elasticsearch` domain may have dependencies on the `Core` domain but not on the `Storefront` or `Administration` domain.
* The `Storefront` domain may have dependencies on the `Core` domain, but not on the `Administration` or `Elasticsearch` domain.

---

---

## Public APIs
**Source:** [resources/guidelines/code/public-apis.md](https://developer.shopware.com/docs/v6.6/resources/guidelines/code/public-apis.md)  
# Public APIs

* Services not intended for decoration or direct use must be marked with `@internal` and have an appropriate comment in the docblock why they should not be used or decorated directly.
* Classes marked with `@internal` need not be kept compatible for third-party developers. Here the public API can change at any time.
* `__construct` methods of services instantiated via DI container are not public API and can be changed at any time.
* `__construct` functions of Data Transfer Objects (DTO), which the developer himself could therefore instantiate (e.g. `CalculatedPrice`, `QuantityPriceDefinition`), are public API and must be kept backward compatible.

---

---

## Routing
**Source:** [resources/guidelines/code/routing.md](https://developer.shopware.com/docs/v6.6/resources/guidelines/code/routing.md)  
# Routing

* Storefront routes must always have the prefix `frontend` in the name.
* Every route must have the `Shopware\Core\Framework\Routing\Annotation\Since` annotation.
* Each core route must have a schema defined under `src/Core/Framework/Api/ApiDefinition/Generator/Schema`.

---

---

## Session and State
**Source:** [resources/guidelines/code/session-and-state.md](https://developer.shopware.com/docs/v6.6/resources/guidelines/code/session-and-state.md)  
# Session and State

Within the `Core` domain, it is not allowed to access the PHP session. There is only one PHP session if it is a Storefront request. The appropriate implementation and consideration of session data must be handled in the Storefront domain.

---

---

## Store API
**Source:** [resources/guidelines/code/store-api.md](https://developer.shopware.com/docs/v6.6/resources/guidelines/code/store-api.md)  
# Store API

## Routes

* Stop implementing the Sales Channel API. It will be deprecated in the 6.4 major release. Define API Controllers (Routes) as services. Use named Routes internally.
* The class or each API method requires the attribute: `#[Route(defaults: ['_routeScope' => ['store-api']])]`.
* Decorator of response extends on `StoreApiResponse`.

## Page Loader

* Routes represent a single functionality.
* Controller/Pageloader only works with routes.
* Controller/Pageloader can call multiple routes.
* A route has to return a StoreApiResponse, to convert to JSON.
* A route response can only contain one object.
* The Storefront controller should never work with the repository again. It should be injected inside a route.

---

---

## Storefront Controller
**Source:** [resources/guidelines/code/storefront-controller.md](https://developer.shopware.com/docs/v6.6/resources/guidelines/code/storefront-controller.md)  
# Storefront Controller

## Controller

* Each controller action requires a `#Route` attribute.
* The name of the route should start with "frontend".
* Each route should define the corresponding HTTP Method (GET, POST, DELETE, PATCH).
* The function name should be concise.
* Each function should define a return type hint.
* A route should have a single purpose.
* Use Symfony flash bags for error reporting.
* Each storefront functionality has to be available inside the Store API too.
* A Storefront controller should never contain business logic.
* The class requires the attribute: `#[Route(defaults: ['_routeScope' => ['storefront']])]`.
* Depending services have to be injected over the class constructor.
* Depending services have to be defined in the DI-Container service definition.
* Depending services have to be assigned to a private class property.
* A Storefront controller has to extend the `\Shopware\Storefront\Controller\StorefrontController`.

## Read operations inside Storefront controllers

* A Storefront controller should never use a repository directly. The data should be fetched over a route or page loader.
* Routes that load a full Storefront page should use a page loader class to load all corresponding data.
* Pages that contain data that are the same for all customers should have the `_httpCache` attribute.

## Write operations inside Storefront controllers

* Write operations should create their response with the `createActionResponse` function to allow different forwards and redirects.
* Each write operation has to call a corresponding Store API route.

---

---

## Documentation Guidelines
**Source:** [resources/guidelines/documentation-guidelines.md](https://developer.shopware.com/docs/v6.6/resources/guidelines/documentation-guidelines.md)  
# Documentation Guidelines

As a contributor, you should refer to this section on how to write articles, the language usage, font and formats to be followed, etc. This section also details the step-by-step documentation process.

---

---

## Documentation Guidelines
**Source:** [resources/guidelines/documentation-guidelines/01-general.md](https://developer.shopware.com/docs/v6.6/resources/guidelines/documentation-guidelines/01-general.md)  
# Documentation Guidelines

Your style, your words, and your tone define you. Correspondingly, this style guide lays out standard editorial instructions that define Shopware documentation.

We recommend that every contributor follows the defined writing standards to maintain uniformity of the documentation. Refer to different sections of this guide to know more.

## Audience

It is important to consider the background of the potential audience reading your writing. This helps you to adapt your writing to meet their needs and interests.

| Who is the audience? | What are their roles? |
| :--- | :--- |
| Fullstack developer | Plugin developmentTemplatesRoutes/ Controllers|
| Frontend developer | AdminThemesPWA  |
| Backend developer | DI/ Service architectureMessage queuesDALAction event systemElasticSearch |
| API developer  | How to consume the APICreate a product/ category importHow to extend the APIAPI paradigmProper API referencesRequest collection |
| DevOps  | Hosting setupDeploymentPerformance tests |
| Project/ Solution architect | HostingArchitectureModules/ Extension systemParadigms/ PatternsCommonalities app system/ Plugin system |
| Designer | Component libraryDesign system |
| Product owner/ Manager | Responsibilities pertaining to the product life cycle |
| Tech writers | Document all product details |

## Applicable documents: style guide coverage

* [Developer docs](https://developer.shopware.com/docs/)
* [API Reference Guide](https://shopware.stoplight.io/)
* [Composable Frontends docs](https://frontends.shopware.com/)
* [Component library](https://component-library.shopware.com/)

## Word list

Choose ecommerce and technical terms from the pre-defined list of terminologies:

* [Shopware terminologies](https://shopware.atlassian.net/wiki/spaces/pr/pages/19249037615/Shopware+terminology)
* [General terms and abbreviations](https://shopware.atlassian.net/wiki/spaces/BGE/pages/735426953/Our+corporate+communications)

::: info
These are internal resources visible to Shopware employees only.
:::

## Use of third-party sources

Third-party sources include websites, books, blogs, videos, images, and more. Ensure to reference these external sources in the documentation only if they are trustworthy. Avoid copying any content directly from other sources like websites, encyclopedias, and Wikipedia.

## Markdown rules

Adhere to the [Markdown cheat sheet](https://www.markdownguide.org/cheat-sheet/) while creating the document.

Refer to [Vitepress syntax](https://vitepress.dev/guide/markdown) for features like hint block, emoji, API blocks, etc.

Symbols in Markdown sometimes serve multi-purpose. For example, `*` or `-` can be used to create bulleted lists. However, follow a single pattern to maintain uniformity throughout. Further sections describe the usage of these patterns and let us comply with them.

Also, user-defined rules govern the content quality, such as removing trailing spaces, code fence style, and more. You may refer to these rules in the [Markdown style of Shopware docs](https://github.com/shopware/docs/blob/master/markdown-style-config.yml).

The following section details the conceptual outline structure of our documentation.

---

---

## Conceptual Outline
**Source:** [resources/guidelines/documentation-guidelines/02-conceptual-structure.md](https://developer.shopware.com/docs/v6.6/resources/guidelines/documentation-guidelines/02-conceptual-structure.md)  
# Conceptual Outline

Our documentation is categorized into the following sections - Concepts, Products, Guides, and Resources. This structure provides different levels of detail, abstraction, and focus.

To give our readers a good experience, we have established writing guidelines for these sections.

## Concepts

This section articulates the core concepts of Shopware. It is an entry point to learn about how the platform is organized. This section rather **explains** than **shows** how things work

## Products

This section deals with topics specific to a single product of Shopware. Every product shares at least some aspect and serves as an entry point to other sections. For example, the *catalog* used within our Community Edition and in all commercial plans is technically the same.

## Guides

This section of the document is home to all the *how-to's*, *examples, cookbooks*, and *tutorials*. In contrast to articles within the *Concepts section*, *Guides* show code, give concrete examples, and provide step-by-step instructions.

It is essential to refer back to the concepts section for related topics from the Guides. For example, *"How to create a custom cart processor"* might contain terms and concepts explained within the "Concepts > Commerce > Checkout > Cart" section and also relate to topics dealt within the "Concepts > Framework > Rules" section. A clear structure allows you to create these cross-references and make the documentation more readable.

## Resources

Resources contain structured documentation for API references, code references, testing references, tooling, links, SDKs, libraries, etc. It also includes guidelines for contribution and publishing.

Now that you have understood the documentation structure, the following section describes the command over language one needs to use for documentation.

---

---

