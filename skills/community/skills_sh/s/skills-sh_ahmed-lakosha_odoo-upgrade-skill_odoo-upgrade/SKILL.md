---
name: odoo-upgrade
description: |
  Comprehensive Odoo ERP upgrade assistant for migrating modules between Odoo versions (14-19). Handles XML views, Python API changes, JavaScript/OWL components, theme SCSS variables, manifest updates, security implementations, and database migrations. Use when user asks to upgrade Odoo modules, fix version compatibility issues, migrate themes between versions, or resolve Odoo 17/18/19 migration errors. Specializes in frontend RPC service migrations, view XML transformations, theme variable restructuring, and portal template XPath fixes.

  <example>
  Context: User wants to upgrade an Odoo module to a newer version
  user: "Upgrade my Odoo 16 module to Odoo 17"
  assistant: "I will use the odoo-upgrade skill to analyze your module, apply XML view transformations, update Python API decorators, and fix manifest version strings for Odoo 17 compatibility."
  <commentary>Core trigger - version migration request with module in scope.</commentary>
  </example>

  <example>
  Context: User hits migration errors after an Odoo version change
  user: "My module breaks with tree views in Odoo 19 - how do I fix it?"
  assistant: "I will use the odoo-upgrade skill to convert all tree views to list views, update attrs expressions to inline invisible, and fix any other Odoo 19 breaking changes."
  <commentary>Error-driven trigger - fix specific migration breakage.</commentary>
  </example>

  <example>
  Context: User needs data migration scripts
  user: "Generate migration scripts for upgrading my module from Odoo 17 to 19"
  assistant: "I will create pre-migrate.py and post-migrate.py scripts handling field renames, data transformations, and cleanup."
  <commentary>Data migration trigger - generates migration script templates.</commentary>
  </example>
license: "MIT"
metadata:
  filePattern: "**/__manifest__.py,**/views/*.xml,**/static/src/js/*.js,**/static/src/scss/*.scss"
  bashPattern: "odoo.*upgrade|odoo.*precheck|odoo.*migrate"
---

# Odoo Upgrade Assistant v5.0

## When to Use

Activate when:
- Upgrading Odoo modules between versions (14-19)
- Fixing version compatibility errors
- Migrating themes or custom modules
- Resolving RPC service errors in frontend
- Converting XML views (tree->list, search groups)
- Updating SCSS variables for Odoo 18/19 themes
- Fixing portal view XPath inheritance errors
- Migrating JavaScript from OWL v1 to v2

## Upgrade Workflow

1. **Analyze** - Read `__manifest__.py`, identify source version, scan all files
2. **Backup** - Create timestamped backup before changes
3. **Pre-check** - Run `scripts/cli.py precheck <path> --target <version>` to identify all issues
4. **Transform** - Apply transforms in order: manifest, XML, Python, JS, SCSS
5. **Validate** - Run `scripts/cli.py validate <path>` to check syntax
6. **Test** - Install module: `python -m odoo -d DB -i MODULE --stop-after-init`

## XML/View Transformations

### Tree to List (Odoo 19)
```xml
<!-- Tags -->        <tree> -> <list>,  </tree> -> </list>
<!-- view_mode -->   tree,form -> list,form
<!-- XPath -->       //tree -> //list
<!-- Remove -->      edit="1" attribute
```

### Search Views (Odoo 19)
Remove `<group>` tags - place filters at root level. Add `<separator/>` before group_by filters.

### Kanban Templates (Odoo 19)
`t-name="kanban-box"` -> `t-name="card"`. Remove `js_class="crm_kanban"`.

### Cron Jobs (Odoo 19)
Remove `<field name="numbercall">` - field no longer exists.

### Form View Context (Odoo 19)
`active_id` -> `id` in context expressions.

### Snippet Options (Odoo 19)
Remove templates inheriting `website.snippet_options` - system redesigned.

### Attrs to Inline (Odoo 18/19)
`attrs="{'invisible': [('state','=','draft')]}"` -> `invisible="state == 'draft'"`

## Python API Migrations

### Slug/Unslug (Odoo 18+)
```python
# Old: from odoo.addons.http_routing.models.ir_http import slug
# New: use request.env['ir.http']._slug(value)
```

### URL For (Odoo 19)
```python
# Old: from odoo.addons.http_routing.models.ir_http import url_for
# New: self.env['ir.http']._url_for('/path')
```

### Controller Type (Odoo 19)
`type='json'` -> `type='jsonrpc'` in `@http.route` decorators.

### View Mode (Odoo 19)
`'view_mode': 'tree'` -> `'view_mode': 'list'` in Python dicts.

## JavaScript/OWL Migrations

### RPC Service (Odoo 19)
RPC service is NOT available in frontend/public components. Replace `useService("rpc")` with a `_jsonRpc` helper method using the fetch API with CSRF token handling.

### OWL Lifecycle Hooks (Odoo 18+)

| OWL 1.x (Odoo 14-17) | OWL 2.0 (Odoo 18+) |
|----------------------|---------------------|
| `constructor(parent, props)` | `setup()` |
| `willStart()` | `onWillStart(callback)` |
| `mounted()` | `onMounted(callback)` |
| `patched()` | `onPatched(callback)` |
| `willUnmount()` | `onWillUnmount(callback)` |
| `willUpdateProps()` | `onWillUpdateProps(callback)` |

## Theme SCSS Variables (Odoo 19)

Use `$o-theme-*` prefixed variables instead of bare Bootstrap names:
- `$headings-font-weight` -> `$o-theme-headings-font-weight`
- `$font-size-base` -> `$o-theme-font-size-base`

Color palettes must include `'menu'`, `'footer'`, `'copyright'` assignments:
```scss
$o-color-palettes: map-merge($o-color-palettes, (
    'my_theme': (
        'o-color-1': #124F81,
        'menu': 1,
        'footer': 4,
        'copyright': 5,
    ),
));
```

## Portal View XPath Migration (Odoo 19)

Sale portal templates restructured with named selectors:

**Headers**: `th[@id='product_qty_header']`, `th[@id='product_unit_price_header']`, `th[@id='product_discount_header']`, `th[@id='taxes_header']`, `th[@id='subtotal_header']`

**Body**: `tr[@name='tr_product']`, `td[@name='td_product_name']`, `td[@name='td_product_quantity']`, `td[@name='td_product_priceunit']`, `td[@name='td_product_discount']`, `td[@name='td_product_taxes']`, `td[@name='td_product_subtotal']`

## Mail Template Migration (Odoo 19)

Remove `env` parameter from format helpers:
```xml
<!-- Old --> format_datetime(env, object.date_start)
<!-- New --> format_datetime(object.date_start)
```

XML entity encoding - use numeric references:
`&copy;` -> `&#169;`, `&nbsp;` -> `&#160;`, `&mdash;` -> `&#8212;`

## Bootstrap 4 to 5 Class Migration

| Bootstrap 4 | Bootstrap 5 |
|-------------|-------------|
| `ml-*`/`mr-*` | `ms-*`/`me-*` |
| `pl-*`/`pr-*` | `ps-*`/`pe-*` |
| `text-left`/`text-right` | `text-start`/`text-end` |
| `float-left`/`float-right` | `float-start`/`float-end` |
| `sr-only` | `visually-hidden` |
| `badge-primary` | `bg-primary` |
| `font-weight-bold` | `fw-bold` |
| `no-gutters` | `g-0` |

## Data Migration Scripts

Place migration scripts under `module/migrations/VERSION/`:
- `pre-migrate.py` - Before ORM update (use raw SQL only)
- `post-migrate.py` - After ORM update (can use env/ORM)
- `end-migrate.py` - After all modules updated (cleanup)

Each must define `def migrate(cr, version):` and guard with `if not version: return`.

Common patterns:

| Pattern | Pre-Migrate | Post-Migrate |
|---------|------------|-------------|
| Field rename | `ALTER TABLE RENAME COLUMN` | Update views |
| Selection to M2O | Backup values | Map to records |
| Add required field | Nothing | Populate defaults |
| Model rename | Rename table + ir_model_data | Update foreign keys |

With `openupgradelib`: `rename_fields()`, `rename_models()`, `rename_xmlids()`, `rename_columns()`, `logged_query()`.

## Common Errors Quick Reference

| Error | Cause | Fix |
|-------|-------|-----|
| Service rpc not available | useService("rpc") in frontend | Replace with _jsonRpc helper |
| Invalid field numbercall | Field removed | Remove from cron XML |
| Invalid view definition (search) | `<group>` in search | Remove group tags |
| Missing card template | kanban-box renamed | Use t-name="card" |
| Cannot import slug | Import moved | Use compatibility wrapper |
| website.snippet_options not found | System redesigned | Remove the template |
| active_id not found | Context change | Replace with id |

## Version-Specific Notes

### Odoo 14 to 15
Bootstrap 4.x -> 5.x, `t-use-call` removed, payment provider API changes, left/right -> start/end

### Odoo 15 to 16
Bootstrap 5.1.3 standardized, web framework reorg, OWL v1 adoption begins

### Odoo 16 to 17
OWL v1 fully adopted, widget system changes, publicWidget API stabilization

### Odoo 17 to 18
OWL v1 -> v2 starts, minor XML changes, snippet group system introduced

### Odoo 18 to 19
**Major frontend overhaul**: RPC service removed, snippet system overhauled, kanban-box->card, search <group> banned, tree->list, portal templates restructured, mail template helpers changed, cron numbercall removed

## References

- [Odoo 18 to 19 Patterns](./reference/odoo18_to_19.md)
- [Error Catalog](./reference/error_catalog.md)
