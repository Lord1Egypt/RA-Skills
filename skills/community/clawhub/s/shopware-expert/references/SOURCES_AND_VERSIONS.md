# Official sources and Shopware versions

Use this skill together with the **live** Shopware documentation. Bundled `references/` are **excerpts and indexes** from a point-in-time export; they are **not** a substitute for the official sites.

## Target: Shopware 6.7 (with gaps)

- The maintainer export **prefers newer versioned doc paths** (including **6.7**) when deduplicating. Treat the bundle as **6.7-oriented**, **not** a complete mirror of Shopware 6.7 or every patch release.
- **New changelog items**, edge cases, or last-week doc updates may be **missing** or **truncated** (see per-section links and truncation notes in generated files).
- **Always** reconcile with the **customer’s real Shopware version** and current **[developer.shopware.com](https://developer.shopware.com/)** (and **[shopware/platform](https://github.com/shopware/platform)** / ADRs for internals)—especially before breaking API or deployment advice.

## Primary URLs

| Audience | Site | Role |
| -------- | ---- | ---- |
| Developers | [developer.shopware.com](https://developer.shopware.com/) | APIs, plugins, apps, hosting, concepts, ADRs |
| Merchants / admin users | [docs.shopware.com](https://docs.shopware.com/) (DE/EN) | Operating the administration, day-to-day shop tasks |

## Versioning in this bundle

- Export paths may include **`/docs/v6.4/`**, **`/docs/v6.5/`**, **`/docs/v6.6/`**, **`/docs/v6.7/`**, or **unversioned** `/docs/guides/...`.
- When deduplicating the source dump, **newer versioned paths are preferred** (see maintainer script `parse_shopware_dump.py`).
- Always confirm behaviour against the **Shopware version** of the target installation.

## License / attribution

- Text and structure originate from **Shopware** documentation and ADRs.
- Prefer linking users to the official pages above for the canonical, up-to-date text.

## Regenerating bundled references

Maintainers: see `docs/openclaw-shopware/README.md` in the **skill source repository** (not shipped on ClawHub) for the dump path and `generate_shopware_references.py`.
