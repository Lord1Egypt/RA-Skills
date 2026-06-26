# Shopware Expert – reference index

Skill id **`shopware-expert`**. Use **progressive disclosure**: load this file first, then open the smallest reference that matches the task. Several topics are split across **`_PART2.md`**, **`_PART3.md`**, … when the bundle would exceed a safe file size—read parts in order.

| File | Content |
| ---- | ------- |
| [SOURCES_AND_VERSIONS.md](SOURCES_AND_VERSIONS.md) | Official URLs; **6.7-oriented** bundle (gaps OK); versioning; attribution; regeneration note |
| [MERCHANT_USER_DOCS.md](MERCHANT_USER_DOCS.md) | End-user / Administration help on **docs.shopware.com** (DE/EN) |
| [PLATFORM_REPO_AND_CONTRIBUTING.md](PLATFORM_REPO_AND_CONTRIBUTING.md) | **GitHub** repos (`platform`, `shopware`, `frontends`), ADRs, contributing |
| [CONNECTING.md](CONNECTING.md) | OpenClaw ↔ Shopware topologies (HTTP-only vs code+HTTP) |
| [AUTH.md](AUTH.md) | OAuth / Admin API / Store API secrets and env vars |
| [TOOLING.md](TOOLING.md) | curl, `bin/console`, browser, workspace editing |
| [OPENCLAW_INTEGRATION.md](OPENCLAW_INTEGRATION.md) | Tool allowlists, sandbox, `skills.entries` |
| [SAFETY.md](SAFETY.md) | Destructive actions, API safety, third-party extensions |
| [APPS_VS_PLUGINS_AND_PATHS.md](APPS_VS_PLUGINS_AND_PATHS.md) | **Apps vs plugins**; `custom/static-plugins/` vs `custom/plugins/`; **never edit core or third-party plugins** |
| [WORKFLOWS.md](WORKFLOWS.md) | **Pre-flight checklist** (version, env names, sales channel, verify via official links); Read → Plan → Write → Verify |
| [CODE_GUIDELINES_ESSENTIALS.md](CODE_GUIDELINES_ESSENTIALS.md) | Official **code** guidelines digest: `@final` / `@internal`, public API, backward-compat annotations, platform domains, Storefront controller, Store API, routing (6.7 note); links to full docs |
| [SHOPWARE_67_EXAMPLES_PLUGIN_DAL.md](SHOPWARE_67_EXAMPLES_PLUGIN_DAL.md) | **Hand-curated 6.7** full examples: plugin `composer.json`, base class, `services.xml`, DAL service, Criteria fragment, event subscriber, entity + migration |
| [SHOPWARE_67_EXAMPLES_STOREFRONT_ADMIN_CMS.md](SHOPWARE_67_EXAMPLES_STOREFRONT_ADMIN_CMS.md) | **Hand-curated 6.7** full examples: Storefront controller/routes/Twig/JS, Administration module (incl. `mt-*`), CMS element registration + storefront Twig |
| [SHOPWARE_67_PRACTICAL_NOTES.md](SHOPWARE_67_PRACTICAL_NOTES.md) | **Hand-curated 6.7** requirements table, breaking changes, commands, links, **storefront asset build** (`theme:compile` vs plugin JS), Composer path notes, CMS/debug learnings |

### Generated from developer documentation (excerpts + links)

| File | Content |
| ---- | ------- |
| [DOC_PORTAL_ROOT.md](DOC_PORTAL_ROOT.md) | Portal landing pages, plugin overview stubs |
| [CONCEPTS_ARCHITECTURE.md](CONCEPTS_ARCHITECTURE.md) | Framework, commerce, extensions, translations, API overview |
| [CATALOG_AND_SALES_CHANNEL.md](CATALOG_AND_SALES_CHANNEL.md) | Catalog and sales channels (concepts) |
| [CHECKOUT_CART_PAYMENTS.md](CHECKOUT_CART_PAYMENTS.md) | Checkout, cart, payments (guides + concepts) |
| [DAL_AND_DATA.md](DAL_AND_DATA.md) + parts | Data Abstraction Layer, data handling guides |
| [RULES_FLOWS_AUTOMATION.md](RULES_FLOWS_AUTOMATION.md) | Rules, Flow Builder, automation |
| [PLUGIN_SYSTEM.md](PLUGIN_SYSTEM.md) + parts | Plugin fundamentals, framework topics, Elasticsearch, Redis, bundles |
| [APP_SYSTEM.md](APP_SYSTEM.md) + parts | App system, webhooks, gateways, SDKs, local dev |
| [ADMINISTRATION_UI.md](ADMINISTRATION_UI.md) + parts | Extending the Vue Administration |
| [ADMIN_EXTENSION_SDK.md](ADMIN_EXTENSION_SDK.md) | Admin Extension SDK reference |
| [STOREFRONT_THEMES_TWIG.md](STOREFRONT_THEMES_TWIG.md) + parts | Storefront, themes, Twig, caching |
| [HEADLESS_FRONTENDS.md](HEADLESS_FRONTENDS.md) + parts | Composable frontends, Nuxt, composables |
| [CMS_AND_CONTENT.md](CMS_AND_CONTENT.md) | CMS blocks, elements, content guides |
| [ADMIN_API.md](ADMIN_API.md) | Admin API guides and concept |
| [STORE_API.md](STORE_API.md) | Store API guides and concept |
| [INTEGRATIONS_AND_SYNC.md](INTEGRATIONS_AND_SYNC.md) | Integrations API |
| [CORE_REFERENCE.md](CORE_REFERENCE.md) + parts | Core / app / config / administration / storefront / testing reference |
| [INSTALLATION_AND_HOSTING.md](INSTALLATION_AND_HOSTING.md) + parts | Install, hosting, infrastructure, deployments |
| [RELEASE_AND_UPGRADES.md](RELEASE_AND_UPGRADES.md) + parts | Release notes, upgrade references |
| [TESTING_AND_QUALITY.md](TESTING_AND_QUALITY.md) + parts | Guidelines, testing, tooling, accessibility |
| [PRODUCT_EXTENSIONS_OVERVIEW.md](PRODUCT_EXTENSIONS_OVERVIEW.md) + parts | Commercial extensions, PaaS, B2B, etc. |
| [ADR_OVERVIEW.md](ADR_OVERVIEW.md) | **Index** of Architecture Decision Records (links to official pages) |

**Maintainer-only** (not in ClawHub bundle): regeneration scripts, taxonomy, and coverage manifest live in the **source repository** under `docs/openclaw-shopware/`—see that README.
