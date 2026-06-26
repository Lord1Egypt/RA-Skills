---
name: shopify-manager-cli
description: Manage Shopify store — products, metafields, metaobjects, blogs & articles via Shopify Admin GraphQL API. Pure official Shopify API wrapper with no third-party plugins required; built on the same API surface as Shopify CLI, giving you full control without extra dependencies.
user_invocable: true

metadata:
  {
    "openclaw":
      {
        "emoji": "🛍️",
        "requires": { "bins": ["python3"], "env": ["SHOPIFY_STORE_URL", "SHOPIFY_ACCESS_TOKEN", "SHOPIFY_API_VERSION"] },
        "primaryEnv": "SHOPIFY_ACCESS_TOKEN",
        "install": [],
      },
  }
---

# Shopify Store Manager

You help users manage their Shopify store by running `python3 scripts/shopify_admin.py` commands.

## Prerequisites

Environment variables must be set:
- `SHOPIFY_STORE_URL` — e.g. `https://my-store.myshopify.com`
- `SHOPIFY_ACCESS_TOKEN` — Admin API access token (`shpat_…`)
- `SHOPIFY_API_VERSION` — optional, defaults to `2025-01`

If not set, remind the user to export them before proceeding.

### Required Admin API access scopes

The custom app must be granted the following scopes in the Shopify Admin under **Settings → Apps → Develop apps → Configuration**:

| Scope | Used by |
|---|---|
| `read_products` / `write_products` | product list / get / create / update / delete |
| `read_metaobject_definitions` / `write_metaobject_definitions` | metaobject define |
| `read_metaobjects` / `write_metaobjects` | metaobject list / create / update / delete |
| `read_content` / `write_content` | blog list / create; article list / create / update / delete |
| `read_files` / `write_files` | file upload; product image upload via staged-upload API |

## How to use

1. Identify the resource type (product / metafield / metaobject / blog / article / file) and action (list / get / create / update / delete / define / set / upload) from the user's message.
2. Map to the exact subcommand and flags using the command reference below. When the user omits optional arguments (e.g. `--status`, `--author`), use the documented defaults — do not prompt unless a required argument is missing.
3. When a command accepts `--image-file` or a local file path, pass the path as-is; the script reads the file from disk and uploads it via Shopify's staged-upload API — no pre-processing needed.
4. Run the command using the Bash tool.
5. Present the output in a clean, readable format (tables for lists, JSON for details).
6. **For delete operations**: always confirm with the user before executing.

## Command reference

### Product

```bash
# List products (with optional search filter)
# Output columns: id  title  [status]  vendor  productType  $price  tags
python3 scripts/shopify_admin.py product list [--filter "status:active"] [--limit 20]

# Get product details
# Output includes: id, title, status, vendor, productType, tags, variants (id/title/price/sku), metafields
python3 scripts/shopify_admin.py product get <id>

# Create a product (defaults to DRAFT status)
python3 scripts/shopify_admin.py product create "<title>" [--description "<html>"] [--vendor "<name>"] [--tags tag1 tag2] [--image-url "https://..."] [--image-file "/path/to/a.jpg"] [--image-alt "Alt text"] [--status DRAFT|ACTIVE|ARCHIVED]

# Update a product (only specify fields to change)
python3 scripts/shopify_admin.py product update <id> [--title "..."] [--description "..."] [--vendor "..."] [--tags t1 t2] [--image-url "https://..."] [--image-file "/path/to/a.jpg"] [--image-alt "Alt text"] [--status ...]

# Delete a product (⚠️ irreversible — confirm first)
python3 scripts/shopify_admin.py product delete <id>
```

### Metafield

```bash
# List metafield definitions for a resource type
python3 scripts/shopify_admin.py metafield list <owner_type> [--limit 50]

# Create a metafield definition
python3 scripts/shopify_admin.py metafield define <owner_type> <key> <type> [--name "Display Name"] [--namespace ns] [--pin]

# Set a metafield value on a resource
python3 scripts/shopify_admin.py metafield set <OwnerType> <owner_id> <key> "<value>" [--type type] [--namespace ns]
```

Owner types: `product`, `customer`, `order`, `shop`, `collection`, `productvariant`, `company`, `location`, etc.

Metafield types: `single_line_text_field`, `multi_line_text_field`, `rich_text_field`, `number_integer`, `number_decimal`, `boolean`, `color`, `date`, `date_time`, `url`, `json`, `money`, `weight`, `volume`, `dimension`, `rating`, `product_reference`, `collection_reference`, `file_reference`, `metaobject_reference`, `list.*`

### Metaobject

```bash
# Create a metaobject definition
# Field spec format: key:type[:name[:required]]
python3 scripts/shopify_admin.py metaobject define <type> <field_specs>... [--name "Display Name"] [--display-key <field_key>]

# Create/upsert a metaobject entry
# Field value format: key=value
python3 scripts/shopify_admin.py metaobject create <type> <handle> <key=value>...

# List metaobject entries
python3 scripts/shopify_admin.py metaobject list <type> [--limit 20]

# Update a metaobject entry
python3 scripts/shopify_admin.py metaobject update <id> <key=value>...

# Delete a metaobject entry (⚠️ confirm first)
python3 scripts/shopify_admin.py metaobject delete <id>
```

### Blog

```bash
# List blogs
python3 scripts/shopify_admin.py blog list [--limit 20]

# Create a blog
python3 scripts/shopify_admin.py blog create "<title>"
```

### File

```bash
# Upload a file to Shopify admin → Settings → Files
python3 scripts/shopify_admin.py file upload "/path/to/file.pdf" [--alt "Alt text"] [--filename "file.pdf"] [--content-type FILE|IMAGE|VIDEO|MODEL_3D] [--duplicate APPEND_UUID|RAISE_ERROR|REPLACE]
```

### Article

```bash
# List articles (optionally filter by blog)
python3 scripts/shopify_admin.py article list [--blog <blog_id>] [--limit 20]

# Create an article (--author defaults to "Admin" if omitted)
python3 scripts/shopify_admin.py article create --blog <blog_id> "<title>" "<body_html>" [--author "Name"] [--tags t1 t2] [--publish]

# Create an article with author info
python3 scripts/shopify_admin.py article create --blog 123 "Trail Running Guide" "<p>Tips for trail running.</p>" --author "Jane Smith" --tags running trails --publish

# Update an article's author
python3 scripts/shopify_admin.py article update <id> --author "New Author Name"

# Update an article
python3 scripts/shopify_admin.py article update <id> [--title "..."] [--body "..."] [--author "Name"] [--tags t1 t2] [--publish|--unpublish]

# Publish / unpublish (set visibility)
python3 scripts/shopify_admin.py article update <id> --publish
python3 scripts/shopify_admin.py article update <id> --unpublish

# Delete an article (⚠️ confirm first)
python3 scripts/shopify_admin.py article delete <id>
```

#### Author notes

- `--author` sets the display name shown on the article (e.g. "Jane Smith").
- Defaults to `"Admin"` when omitted.
- To show author info when listing articles, the output already includes the `by <author>` column.
- Author is stored as a plain string — it does **not** link to a Shopify staff account.

## ID format

Users can provide either:
- A numeric ID: `123`
- A full Shopify GID: `gid://shopify/Product/123`

The script handles both formats automatically.

## Natural language mapping examples

| User says | Command |
|---|---|
| "list all active products" | `product list --filter "status:active"` |
| "show me product 123" | `product get 123` |
| "create a hiking boot product by GeoStep" | `product create "Hiking Boots" --vendor GeoStep` |
| "add a care_guide text field to products" | `metafield define product care_guide single_line_text_field --name "Care Guide"` |
| "set care guide for product 123 to hand wash" | `metafield set Product 123 care_guide "Hand wash only"` |
| "define a designer metaobject with name and bio" | `metaobject define designer name:single_line_text_field:Name bio:multi_line_text_field:Bio --display-key name` |
| "create a blog called Company News" | `blog create "Company News"` |
| "write an article in blog 456 about summer hiking" | `article create --blog 456 "Summer Hiking Guide" "<p>...</p>" --publish` |
| "write an article by Jane Smith in blog 456" | `article create --blog 456 "Article Title" "<p>...</p>" --author "Jane Smith" --publish` |
| "change the author of article 789 to John Doe" | `article update 789 --author "John Doe"` |
| "list articles in blog 456 to see authors" | `article list --blog 456` |
