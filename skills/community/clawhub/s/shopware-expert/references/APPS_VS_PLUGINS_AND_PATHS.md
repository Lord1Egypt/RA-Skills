# Apps vs plugins and where code lives

Use this file for **high-level** decisions. Deep guides: `APP_SYSTEM.md`, `PLUGIN_SYSTEM.md`, `CONCEPTS_ARCHITECTURE.md` (concepts/extensions). Official overview: [developer.shopware.com](https://developer.shopware.com/docs/concepts/extensions/).

## Apps (App System)

- **Deployed separately** from the core PHP app (manifest, hosted backend, webhooks, scripting where supported).
- **Administration** often uses **iframes** / **Admin Extension SDK**; integration is **API- and event-driven** rather than shipping PHP inside Shopware's monolith.
- Good when you want **loose coupling**, **external services**, or **Store-distributed** apps without full platform bundle access.

## Plugins (plugin system)

- **PHP packages** loaded **inside** the Shopware process: services, DAL entities, subscribers, Storefront (Twig/JS), Administration (Vue), `bin/console` commands, etc.
- Installed as **Composer packages** or under the project's plugin directories (see below).
- Good when you need **deep integration** with core services, entities, checkout, or storefront rendering.

**Rule of thumb:** Prefer **apps** when Shopware documents that pattern for your use case; use **plugins** when you must extend PHP core behaviour or the classic Admin/Storefront plugin APIs.

---

## `custom/static-plugins/` vs `custom/plugins/`

Layouts differ slightly by **template** (flex, production repo, agency standards). Common **team/production** pattern:

| Location | Typical use |
| -------- | ----------- |
| **`custom/static-plugins/`** (name may vary; sometimes a single root package) | **First-party / project-owned** plugins checked into git, often wired via **Composer path repositories** in root `composer.json`. This is where **your** team's plugin source often lives so it is **not** mixed with Store downloads. |
| **`custom/plugins/`** | Often used for **third-party / Shopware Store / Composer-installed** extensions (e.g. `Swag*`, purchased plugins). Treat as **vendor-like**: do not hand-edit for fixes. |

**Always** confirm for the current project:

1. Root **`composer.json`** (`repositories`, `require` paths).
2. Whether the team uses **`static-plugins`**, a **monorepo** layout, or only **`custom/plugins/`**.

If unsure, **ask the user** or read the repo before proposing file paths.

---

## What you must not edit directly

1. **Shopware core** under **`vendor/shopware/`** (and core packages pulled by Composer). Changes are **lost on update** and are **unsupported**. Extend via **plugins/apps**, **events**, **decorators** (where documented), or configuration.

2. **Third-party plugins** under **`custom/plugins/<ThirdPartyPlugin>`** (or equivalent). **Do not** patch vendor/Store plugin code in place. Prefer: **update the extension**, **configuration**, **events**, a **small wrapping plugin** of your own, or a **fork** with a maintained Composer VCS repo - not one-off edits on disk.

3. **First-party** code in **`custom/static-plugins/`** (or your own plugin package) **may** be edited - that is the team's source of truth.

---

## Agent checklist

- [ ] Identified whether the task is **app** vs **plugin** shaped.
- [ ] Resolved **project layout** (`static-plugins` vs `custom/plugins`) from `composer.json` / user.
- [ ] No edits proposed under **`vendor/shopware/`** or **third-party** plugin trees unless the user explicitly requests a temporary diagnostic (and even then prefer read-only inspection).

See also [SAFETY.md](SAFETY.md).
