---
name: woocommerce-sync-pro
description: Sync WooCommerce products, orders, customers, coupons, reviews, custom post types, taxonomy terms, menus, users and custom database tables between WordPress sites with the PRO Import Export plugin abilities (rsl-ie-pro/*). Use only when the PRO plugin is active and the task goes beyond posts and pages.
license: GPL-2.0-or-later
---

# PRO sync: WooCommerce, CPT, terms, menus, users, tables (rsl-ie-pro abilities)

Requires `import-export-pro-by-rockstarlab` with an active license, on both sites, plus a working connection (see `wordpress-content-sync` steps 1–2). Check `rsl-ie-pro/get-capabilities` first; if the license is inactive, stop and tell the user.

REST: `POST /wp-json/wp-abilities/v1/abilities/rsl-ie-pro/<name>/run` `{"input":{...}}`.

## Pattern for every entity

`<entity>-browse` / `sync-search-local` → choose ids → `<entity>-push-start` or `-pull-start` with `site_id`, ids (≤50), unique `request_id` → `rsl-ie/sync-job-status` (shared status ability) → verify on target. Never use the synchronous `-push`/`-pull` for big sets.

| Entity | Start ability (push; pull is symmetric) | ids field |
|---|---|---|
| Products, CPT | `sync-push-start` (`post_type`, `woo_product_mapping`) | `post_ids` |
| Orders | `sync-woo-orders-push-start` | `order_ids` |
| Customers | `sync-woo-customers-push-start` (by email) | `customer_ids` |
| Coupons | `sync-woo-coupons-push-start` (by code) | `coupon_ids` |
| Refunds | `sync-woo-refunds-push-start` | order ids |
| Product reviews | `sync-reviews-push-start` | `comment_ids` |
| Attributes | `sync-woo-attributes-push-start` | see schema |
| Taxonomy terms | `sync-terms-push-start` (`taxonomy`) | `term_ids` |
| Menus | `sync-menus-push-start` | `menu_ids` |
| Users | `sync-users-push-start` | `user_ids` |
| Custom tables | `sync-tables-push-start` (`table_suffix`) | `table_ids` |

Order of transfer for a shop: terms and attributes → products → customers → coupons → orders → refunds → reviews. Orders, customers and coupons are matched by email/code/order key, and the result returns confirmed `*_mapping` objects to reuse in later steps.

PRO import/export of CPT, users, taxonomies, WooCommerce: `rsl-ie-pro/list-targets`, `get-content-schema`, `import-prepare|validate|start`, `export-count|preview|start`, same flow as `wordpress-import-export`. Transformations on fields: `function-*`, `snippet-*`; bulk edits of existing content: `update-count` → `update-preview` → `update-start` → `update-status`.

## Rules

- Orders, customers and users are personal data: confirm scope with the user and never display customer details in the chat beyond counts.
- Do not trigger live payment or email flows; confirm that the target store's order emails/webhooks are acceptable to fire (or disabled) before pushing orders.
- Before bulk changes, take a database backup of the target and run the `-count`/`-preview` abilities first.
- `function-create` / `function-update` store PHP code: only write code the user reviewed.
