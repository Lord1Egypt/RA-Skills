# Shopware platform repository and contributing

## Main repositories (GitHub)

| Repository | Purpose |
| ---------- | ------- |
| [shopware/platform](https://github.com/shopware/platform) | Core platform (monorepo): `core/`, `administration/`, `storefront/`, **ADRs** under `adr/`, many composer packages |
| [shopware/shopware](https://github.com/shopware/shopware) | Product/meta repository; README links to docs and flex template |
| [shopware/frontends](https://github.com/shopware/frontends) | Headless / composable storefront packages (see `HEADLESS_FRONTENDS.md`) |

ADRs in the developer docs are mirrored from **`shopware/platform` → `adr/`** (linked from each ADR page).

## Local development (high level)

- Typical setup uses **Composer**, **Symfony**, **Vue** (Admin), **Twig** + **Storefront** assets.
- Follow the current **installation** and **development environment** guides on [developer.shopware.com](https://developer.shopware.com/docs/guides/installation/) rather than pinning a single workflow here.

## Contributing

- Read Shopware’s **contribution guidelines** on the developer portal and in **`CONTRIBUTING.md`** in the platform repository.
- For code contributions: tests, backward compatibility, and changelog expectations are defined by the project—check the version branch you target.

## For OpenClaw agents

- Treat the **git tree** as the source of truth for **internal APIs and class names** when you have a **clone in the workspace**.
- Without a clone, prefer **official API reference** and guides in this skill’s generated files and on developer.shopware.com—**do not invent** endpoints or payload shapes.
