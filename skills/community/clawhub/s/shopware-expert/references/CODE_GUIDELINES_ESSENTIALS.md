# Shopware code guidelines (essentials)

Curated **short** summary of official Shopware **code** guidelines for extension and integration work. **Always verify** against the live docs and your Shopware version.

- **Hub:** [Guidelines](https://developer.shopware.com/docs/resources/guidelines/)
- **More in this skill bundle:** longer excerpts live under `TESTING_AND_QUALITY.md` and especially `TESTING_AND_QUALITY_PART2.md` (search for `resources/guidelines`).

---

## @final and @internal

**Source:** [Final and internal annotation](https://developer.shopware.com/docs/resources/guidelines/code/core/final-and-internal/) (mirrored from [shopware/platform coding-guidelines](https://github.com/shopware/shopware/blob/trunk/coding-guidelines/core/final-and-internal.md))

Shopware uses `@final` and `@internal` in docblocks to separate **public** vs **private** API and set expectations for breaking changes.

### @final

Classes are `@final` when developers **may use** the class but **should not extend** it.

**Allowed changes:**

- Adding new public methods, properties, or constants
- Adding new **optional** parameters to public methods
- Changing protected/private members without restriction
- Widening types of public method parameters

**Not allowed:**

- Removing public methods, properties, or constants
- Removing parameters from public methods
- Narrowing types of public methods, properties, or constants

Because this is only a docblock (not the PHP `final` keyword), extending and replacing the service in DI is technically possible but **unsupported and without guarantees**.

### @internal

Classes are `@internal` when they are **private API**: not for third-party use or extension. Shopware may change or remove them **without deprecation**.

Using or replacing such services is possible in PHP but **not recommended** and **without guarantees**.

---

## Public APIs

**Source:** [Public APIs](https://developer.shopware.com/docs/resources/guidelines/code/public-apis/)

- Services not meant for decoration or direct use must be marked `@internal` with a docblock explaining why.
- `@internal` classes need **not** stay compatible for third parties; the API may change anytime.
- `__construct` of services built by the **DI container** is **not** public API and may change anytime.
- `__construct` of **DTOs** that developers may instantiate themselves (e.g. `CalculatedPrice`, `QuantityPriceDefinition`) **is** public API and must stay backward compatible.

---

## Backward compatibility

**Source:** [Backward compatibility](https://developer.shopware.com/docs/resources/guidelines/code/backward-compatibility/) | [Symfony backward compatibility](https://symfony.com/doc/current/contributing/code/bc.html)

Shopware follows **semantic versioning**; **minor and patch** releases must stay backward compatible for public APIs. Full **compatibility matrices** (PHP, Twig, Storefront JS, Administration Vue, etc.) are only in the official guide; use the link above before you change APIs, templates, or events.

### Annotations (overview)

**Obsolete public code** (remove in next major):

```php
/**
 * @deprecated tag:v6.8.0 - Use NewFunction() instead
 */
```

**New, not yet stable API** (treat like internal until stable):

```php
/**
 * @experimental feature:FEATURE_FLAG stableVersion:v6.8.0
 */
```

Workflow tables (feature flags, `@internal` on new API, deprecations, major breaks) are in the official document.

---

## Platform domains

**Source:** [Platform domains](https://developer.shopware.com/docs/resources/guidelines/code/platform-domains/)

- **Core** must not depend on `Storefront`, `Administration`, or `Elasticsearch` (no classes or assets from those domains).
- **Administration** may depend on **Core** only (not Storefront or Elasticsearch).
- **Elasticsearch** may depend on **Core** only (not Storefront or Administration).
- **Storefront** may depend on **Core** only (not Administration or Elasticsearch).

---

## Storefront controller

**Source:** [Storefront controller](https://developer.shopware.com/docs/resources/guidelines/code/storefront-controller/)

### Controller

- Each action uses a `#[Route]` **attribute** (PHP 8).
- Route **name** should start with `frontend`.
- Each route declares the HTTP method (GET, POST, DELETE, PATCH).
- Function names should be concise; each function has a **return type**.
- One route, one purpose.
- Use Symfony **flash bags** for errors.
- Storefront features should also be available via **Store API** where applicable.
- **No business logic** in the Storefront controller.
- Class attribute: `#[Route(defaults: ['_routeScope' => ['storefront']])]` (or equivalent `PlatformRequest` / scope constants used in your Shopware version).
- Inject dependencies via **constructor**; register services in DI; keep dependencies in **private** properties.
- Extend `\Shopware\Storefront\Controller\StorefrontController`.

### Read operations

- Do **not** use repositories directly in the controller; load data via **routes** or **page loaders**.
- Full pages should use a **page loader** for related data.
- Pages with the same data for all customers may use the **`_httpCache`** attribute where appropriate.

### Write operations

- Use **`createActionResponse`** for responses that may forward or redirect.
- Each write should go through the corresponding **Store API** route pattern where applicable.

---

## Store API

**Source:** [Store API](https://developer.shopware.com/docs/resources/guidelines/code/store-api/)

### Routes

- Prefer defined API controllers (routes) as services; use **named routes** internally.
- Class or method needs route scope for Store API, e.g. `#[Route(defaults: ['_routeScope' => ['store-api']])]` (confirm attribute keys for your version).
- Response decorators extend `StoreApiResponse`.

### Page loader

- Routes map to a **single** responsibility.
- Controller/page loader composes work via routes; may call multiple routes.
- A route returns a **StoreApiResponse** for JSON.
- One route response: **one** top-level object.
- Storefront controller should not use the repository directly; repositories belong behind routes.

**Plugins:** Treat this as **architectural guidance**. Route names, scopes, and internal core layout may differ from your plugin; align with official Store API / routing docs when you expose HTTP APIs.

---

## Routing (core conventions)

**Source:** [Routing](https://developer.shopware.com/docs/resources/guidelines/code/routing/)

- Storefront route names use the **`frontend`** prefix.
- Core documentation also references a **`Since` annotation** for core routes and OpenAPI schema paths under core; those targets are **core-repo** specific.

**Shopware 6.7 plugins:** Use **PHP 8 `Route` attributes** and the route scope pattern documented for your edition (see [SHOPWARE_67_EXAMPLES_STOREFRONT_ADMIN_CMS.md](SHOPWARE_67_EXAMPLES_STOREFRONT_ADMIN_CMS.md)). Do not rely on legacy annotation-only examples without checking the current doc.

---

## Session and state

**Source:** [Session and state](https://developer.shopware.com/docs/resources/guidelines/code/session-and-state/)

Within **Core**, **do not** use the PHP session. There is a single PHP session for Storefront requests; session-related behavior belongs in the **Storefront** domain.

---

## Further reading (official)

Short pointers only; full text is on developer.shopware.com.

| Topic | Why open it |
| ----- | ----------- |
| [Decorator pattern](https://developer.shopware.com/docs/resources/guidelines/code/core/decorator-pattern/) | Safe extension of services without breaking core. |
| [Domain exceptions](https://developer.shopware.com/docs/resources/guidelines/code/core/domain-exceptions/) | Consistent error handling in the domain layer. |
| [Events](https://developer.shopware.com/docs/resources/guidelines/code/events/) | Prefer events and extension points where documented. |
| [Dependency injection](https://developer.shopware.com/docs/resources/guidelines/code/dependency-injection-dependency-handling/) | How Shopware expects services and decoration to work. |
| [Database migrations](https://developer.shopware.com/docs/resources/guidelines/code/core/database-migations/) | BC-safe schema changes and blue/green considerations for core; mirror discipline in plugins. |
