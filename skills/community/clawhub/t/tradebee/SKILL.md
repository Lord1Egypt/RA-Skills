---
name: tradebee
description: v26.6.26 A unified Tradebee Website Builder Open API skill that helps an agent choose the correct Tradebee data operation from a user's desired business result. Use it only when the user clearly wants to operate on Tradebee blogs, blog groups, FAQs, FAQ groups, custom pages, products, product groups, inquiries, visitors, keyword rankings, or tenant HTML rule retrieval, not for generic find/show/check/update/delete requests outside Tradebee platform data context. For all `*_update` actions, it also automatically reads the current record and writes a local JSON backup file before sending the update request.
homepage: https://open.tradew.com
metadata: {"clawdbot":{"emoji":"bee","requires":{"env":["BEE_API_KEY"]},"primaryEnv":"BEE_API_KEY"}}
---

# tradebee

> Version: 26.6.26

## Overview

This skill merges multiple Tradebee Website Builder Open API capabilities into a single publishable skill.

For all `*_update` actions, this skill does more than send a Tradebee update request:

- It reads the current record first.
- It writes a local JSON backup file under `backups/<action>/` relative to the current installed skill root.
- It returns backup metadata, the raw read response, the extracted snapshot, and a best-effort `restore_payload` on success.
- The local backup file also keeps `confirmation_summary`, `requested_update_payload`, and `restore_limitations` together with that backup data.

All future Tradebee capabilities added in this repository must be exposed through `tradebee` rather than published as separate primary skills.

This skill should be selected by the user's expected result, not only by API name.

Only route into this skill after the Tradebee data domain and object type are explicit.

- Do not trigger this skill for generic requests such as "find", "show", "check", "update", or "delete" when Tradebee platform data is not clearly the target.
- For `*_update` and `*_delete`, require one explicit Tradebee object type plus one explicit record ID or explicitly confirmed ID list before routing.
- For `*_read`, still choose the narrowest valid Tradebee filter instead of broad listing when the user already gave an exact ID, group, keyword, or IP.

When the user speaks in natural language such as "find the Tradebee product", "show Tradebee products under this category", "read one exact Tradebee blog", "open this custom page", "look at recent Tradebee inquiries", "see which Tradebee keywords are ranking in the top 100", or "delete these Tradebee products", map that request to the matching `action` below and choose the narrowest valid filter.

Supported actions:

- `languages-get`
- `rule-get`
- `blog-create`
- `blog-update`
- `blog-read`
- `blog-delete`
- `bloggroup-create`
- `bloggroup-update`
- `bloggroup-read`
- `bloggroup-delete`
- `faq-create`
- `faq-update`
- `faq-read`
- `faq-delete`
- `faqgroup-create`
- `faqgroup-update`
- `faqgroup-read`
- `faqgroup-delete`
- `custompage-create`
- `custompage-update`
- `custompage-read`
- `custompage-delete`
- `productsgroup-create`
- `productsgroup-update`
- `productsgroup-delete`
- `productsgroup-read`
- `products-read`
- `products-create`
- `products-update`
- `products-delete`
- `inquiry-read`
- `visitor-recent`
- `keywords-rank`

## HTML Fragment Rules

Before generating any HTML fragment for:

- `blog.description`
- `faq.answer`
- `products.description`
- `productsgroup.section.top`
- `productsgroup.section.bottom`
- `custompage.content`

first call `rule-get` with:

- the exact selected `language`
- the exact matching `scene`

`rule-get` call requirements:

- `language` is required
- `scene` is required
- use the exact `language` value already selected for the create or update action
- do not guess, translate, normalize, or replace the `language` value
- do not invent, shorten, translate, or rename any `scene` value
- use only the fixed scene mapping below. Do not call the current frontend website domain for this rule API.

Minimal request body:

```json
{
  "action": "rule-get",
  "language": "en",
  "scene": "products.description"
}
```

Example request pattern:

```json
{
  "action": "rule-get",
  "language": "en",
  "scene": "products.description"
}
```

Required execution order:

1. Select the exact site `language` first.
2. Select the exact fixed `scene` that matches the target HTML field.
3. Call `rule-get`.
4. Generate the HTML fragment only after `rule-get` returns successfully.

Failure rule:

- If `rule-get` fails, do not continue by guessing colors, fonts, links, layout, or other fragment rules.
- Stop and report the rule-call failure instead of generating a fragment from assumptions.

Scene mapping:

- `blog.description` -> `scene=blog.description`
- `faq.answer` -> `scene=faq.answer`
- `products.description` -> `scene=products.description`
- `productsgroup.section.top` -> `scene=productsgroup.section.top`
- `productsgroup.section.bottom` -> `scene=productsgroup.section.bottom`
- `custompage.content` -> `scene=custompage.content`

The generated fragment must follow the returned rule payload, especially:

- use the exact selected language only
- follow the full returned rule payload, not only part of it
- do not guess, replace, shorten, rename, or partially ignore returned rule fields
- do not hardcode assumptions in this skill about future rule details; the `rule-get` response is the source of truth

## Quick Routing Guide

Choose the action by the user's actual goal and the result they expect to see.

### Result-First Routing

- If the user wants to know "what exists", prefer a `*_read` action.
- If the user wants to "add new content", prefer a `*_create` action.
- If the user wants to "change existing content", prefer a `*_update` action.
- If the user wants to "remove existing content", prefer a `*_delete` action.
- If the user asks for analytics, visit history, inquiry records, or keyword performance, prefer the specialized read action instead of any content action.

### How Users Usually Ask

- "show one", "check one", "list them", "see whether it exists", "find this", "read one"
  Route these to the matching `*_read` action.
- "add new", "create", "publish", "add"
  Route these to the matching `*_create` action.
- "modify", "edit", "update", "adjust"
  Route these to the matching `*_update` action.
- "delete", "move to recycle bin", "remove"
  Route these to the matching `*_delete` action.
- "recent visits", "visitor IP", "keyword ranking", "inquiry records"
  Route these to `visitor-recent`, `keywords-rank`, or `inquiry-read` instead of blog or product actions.

### Language Selection

- Use `languages-get` when the user asks:
  - "What languages are enabled?"
  - "Show available site languages"
  - "Which language code should I use?"
- Use `rule-get` when the user asks:
  - "Read the product description HTML rules"
  - "Show the blog description rule payload"
  - "Get the product group top section rules"
  - "Check the exact Tradebee HTML generation rules for this scene"

### Blog Operations

- Use `blog-read` when the user asks:
  - "Read blogs"
  - "List blog articles"
  - "Find one exact blog"
  - "Show blogs under this blog group"
  - "help me check this blog post"
  - "show blogs under a specific category"
- Use `blog-create` when the user asks:
  - "Create a blog"
  - "Publish an article"
  - "Add a new blog post"
- Use `blog-update` when the user asks:
  - "Update blog 123"
  - "Edit blog content"
  - "Move a blog to another group"
- Use `blog-delete` when the user asks:
  - "Delete blog 123"
  - "Move these blogs to recycle bin"

### Blog Group Operations

- Use `bloggroup-read` when the user asks:
  - "List blog groups"
  - "Read one exact blog group"
  - "Show blog categories"
  - "what blog categories are there"
  - "check this blog category"
- Use `bloggroup-create` when the user asks:
  - "Create a blog group"
  - "Add a blog category"
- Use `bloggroup-update` when the user asks:
  - "Update blog group 456"
  - "Rename a blog category"
- Use `bloggroup-delete` when the user asks:
  - "Delete these blog groups"

### FAQ Operations

- Use `faq-read` when the user asks:
  - "Read FAQs"
  - "List FAQ entries"
  - "Find one exact FAQ"
  - "Show FAQs under this FAQ group"
  - "help me check this FAQ"
- Use `faq-create` when the user asks:
  - "Create an FAQ"
  - "Publish an FAQ entry"
  - "Add a FAQ item"
- Use `faq-update` when the user asks:
  - "Update FAQ 123"
  - "Edit FAQ content"
  - "Move an FAQ to another group"
- Use `faq-delete` when the user asks:
  - "Delete FAQ 123"
  - "Move these FAQs to recycle bin"

### FAQ Group Operations

- Use `faqgroup-read` when the user asks:
  - "List FAQ groups"
  - "Read one exact FAQ group"
  - "Show FAQ categories"
  - "what FAQ categories are there"
  - "check this FAQ category"
- Use `faqgroup-create` when the user asks:
  - "Create an FAQ group"
  - "Add an FAQ category"
- Use `faqgroup-update` when the user asks:
  - "Update FAQ group 456"
  - "Rename an FAQ category"
- Use `faqgroup-delete` when the user asks:
  - "Delete these FAQ groups"

### Custom Page Operations

- Use `custompage-read` when the user asks:
  - "Read custom pages"
  - "List custom pages"
  - "Find one exact custom page"
  - "show custom page details"
- Use `custompage-create` when the user asks:
  - "Create a custom page"
  - "Add a custom page"
  - "Publish a custom page"
- Use `custompage-update` when the user asks:
  - "Update custom page 123"
  - "Edit custom page content"
  - "Change custom page SEO"
- Use `custompage-delete` when the user asks:
  - "Delete custom page 123"
  - "Move these custom pages to recycle bin"

### Product Operations

- Use `products-read` when the user asks:
  - "Read products"
  - "List product data"
  - "Find one exact product"
  - "Show products under this group"
  - "help me find this product"
  - "show products under this group"
  - "read product details"
- Use `products-create` when the user asks:
  - "Create a product"
  - "Publish a new product"
  - "Add a product listing"
- Use `products-update` when the user asks:
  - "Update product 123"
  - "Modify product content"
  - "Move a product to another group"
- Use `products-delete` when the user asks:
  - "Delete product 123"
  - "Move these products to recycle bin"

### Product Group Operations

- Use `productsgroup-read` when the user asks:
  - "List product groups"
  - "Read top-level product groups"
  - "Read child groups under this parent"
  - "Find one exact product group"
  - "what product categories are there"
  - "what child categories are under this parent category"
- Use `productsgroup-create` when the user asks:
  - "Create a product group"
  - "Add a product category"
- Use `productsgroup-update` when the user asks:
  - "Update product group 456"
  - "Edit product category info"
- Use `productsgroup-delete` when the user asks:
  - "Delete these product groups"

### Inquiry, Visitor, and Ranking Operations

- Use `inquiry-read` when the user asks:
  - "Read inquiries"
  - "List leads"
  - "Show recent inquiry records"
  - "what recent inquiries are there"
  - "help me check recent customer messages"
- Use `visitor-recent` when the user asks:
  - "Check recent visitors"
  - "Find visitor by IP"
  - "Show latest visitor behavior"
  - "show recent visits"
  - "check visits from this IP"
- Use `keywords-rank` when the user asks:
  - "Check keyword ranking"
  - "Find one exact keyword ranking"
  - "Show keywords ranked within top 100"
  - "show keyword performance"
  - "check the top 100 keywords"

## Selection Principles

- Prefer `*-read` only when the user explicitly wants to read or analyze existing Tradebee records and the Tradebee object type is already clear.
- Prefer `*-create` only when the user explicitly wants to create new Tradebee content and the target Tradebee object type is already clear.
- Prefer `*-update` only when the user explicitly wants to modify one existing Tradebee record and both the Tradebee object type and target record are already explicit.
- Prefer `*-delete` only when the user explicitly wants to delete Tradebee content and both the Tradebee object type and target record ID or confirmed ID list are already explicit.
- If the user mentions one exact ID, prefer the corresponding exact-ID read filter instead of a broader group filter.
- If the user mentions "under this group", "in this category", or "belonging to this group", prefer the corresponding group filter.
- If the request needs a language and the user has not provided one exact enabled code yet, call `languages-get` first.
- If the user gives both an exact ID and a group condition, prefer the exact ID if the API requires a mutually exclusive choice.
- If the user wants "details", "that one", or "the exact record", prefer the exact-ID filter over list-style filters.
- If the user wants "all", "recent", or "latest list", avoid adding unnecessary exact-ID filters.
- If the user asks for a business result but does not name the object type clearly, infer the object from nouns:
  `product` -> `products-*`, `product group/category` -> `productsgroup-*`, `blog/article` -> `blog-*`, `blog group/category` -> `bloggroup-*`, `faq` -> `faq-*`, `faq group/category` -> `faqgroup-*`, `custom page` -> `custompage-*`.

## Preview URL Rule

For these read actions:

- `blog-read`
- `bloggroup-read`
- `faq-read`
- `faqgroup-read`
- `custompage-read`
- `products-read`
- `productsgroup-read`

when the returned result is a list, the agent must include one ID and one preview URL in the final answer so the user can decide whether to preview it.

- Do not tell the user they must preview it.
- Do not omit the preview URL when the API response already contains the corresponding URL field.
- Do not omit the ID when the API response already contains the corresponding ID field.
- If `fields` is used, include the corresponding URL field so one preview URL is available in the returned list:
  `blog_url`, `bloggroup_url`, `faq_url`, `faqgroup_url`, `custompage_url`, `products_url`, or `productsgroup_url`.
  Also include the corresponding ID field:
  `blog_id`, `bloggroup_id`, `faq_id`, `faqgroup_id`, `custompage_id`, `products_id`, or `productsgroup_id`.

## Routing by Expected Result

Use this section when a request is phrased around a business outcome instead of an API term.

- "I want to know what product data exists"
  Use `products-read`.
- "I want one exact product"
  Use `products-read` with `products_id`.
- "I want products inside one category"
  Use `products-read` with `productsgroup_id`.
- "I want all top-level product categories"
  Use `productsgroup-read` with no filter or `parent_productsgroup_id=0`.
- "I want subcategories under one parent category"
  Use `productsgroup-read` with `parent_productsgroup_id`.
- "I want one exact product category"
  Use `productsgroup-read` with `productsgroup_id`.
- "I want blog articles"
  Use `blog-read`.
- "I want one exact blog"
  Use `blog-read` with `blog_id`.
- "I want blogs inside one blog group"
  Use `blog-read` with `bloggroup_id`.
- "I want all blog groups or one exact blog group"
  Use `bloggroup-read`, optionally with `bloggroup_id`.
- "I want FAQs"
  Use `faq-read`.
- "I want one exact FAQ"
  Use `faq-read` with `faq_id`.
- "I want FAQs inside one FAQ group"
  Use `faq-read` with `faqgroup_id`.
- "I want all FAQ groups or one exact FAQ group"
  Use `faqgroup-read`, optionally with `faqgroup_id`.
- "I want custom pages"
  Use `custompage-read`.
- "I want one exact custom page"
  Use `custompage-read` with `custompage_id`.
- "I want inquiry records from recent days"
  Use `inquiry-read`, optionally with `recent_days`.
- "I want recent visitor data"
  Use `visitor-recent`.
- "I want visitor data for one IP"
  Use `visitor-recent` with `ip`.
- "I want keyword ranking for one keyword"
  Use `keywords-rank` with `keywords`.
- "I want keywords ranking within the top N"
  Use `keywords-rank` with `rank`.

## Filter Selection Rules

When multiple filters exist, choose the one that most directly matches the user's wording.

- `products-read`
  If the user names one exact product, use `products_id`.
  If the user asks for products under one group, use `productsgroup_id`.
  Do not send both together.
- `productsgroup-read`
  If the user asks for one exact group, use `productsgroup_id`.
  If the user asks for children under a parent, use `parent_productsgroup_id`.
  If the user asks for top-level groups, omit both or use `parent_productsgroup_id=0`.
- `blog-read`
  If the user names one exact blog, use `blog_id`.
  If the user asks for blogs under one group, use `bloggroup_id`.
  Do not send both together.
- `bloggroup-read`
  If the user asks for one exact blog group, use `bloggroup_id`.
  Otherwise omit it to read the list.
- `faq-read`
  If the user names one exact FAQ, use `faq_id`.
  If the user asks for FAQs under one group, use `faqgroup_id`.
  Do not send both together.
- `faqgroup-read`
  If the user asks for one exact FAQ group, use `faqgroup_id`.
  Otherwise omit it to read the list.
- `custompage-read`
  If the user asks for one exact custom page, use `custompage_id`.
  Otherwise omit it to read the list.
- `visitor-recent`
  If the user gives one IP, use `ip`.
  Otherwise omit it to read recent visitors across all IPs.
- `keywords-rank`
  If the user gives one exact keyword text, use `keywords`.
  If the user asks for "top N", use `rank`.
  Do not send both together.

## Required Parameters

Authentication uses only the configured `BEE_API_KEY` environment variable. Never provide API keys in tool inputs, prompts, examples, logs, or chat text. Tradebee requests send site and business data to the external Tradebee Website Builder API, so only send the minimum data needed for the user's stated task.

### `action` (string)

Selects which capability to execute.

Practical routing rule:

- explicit Tradebee read or analysis request with a clear object type -> usually choose a `*-read` action
- explicit Tradebee create or publish request with a clear object type -> usually choose a `*-create` action
- explicit Tradebee update request for one known record -> usually choose a `*-update` action
- explicit Tradebee delete request for one known record or one confirmed ID list -> usually choose a `*-delete` action

## Common Parameters

### `language` (string)

Used by most content operations.

- This must be the exact site language code returned by `languages-get`, such as `en` or `fr`
- Do not guess, translate, normalize, or invent the value
- First call `languages-get`, show the language list to the user, then copy one exact `language` value the user confirms

### `scene` (string)

Used by `rule-get`.

- This field is required for `rule-get`.
- Use one exact supported scene value only: `blog.description`, `faq.answer`, `products.description`, `productsgroup.section.top`, `productsgroup.section.bottom`, or `custompage.content`.
- Do not invent, shorten, translate, normalize, or rename the value.
- Choose the exact scene that matches the target HTML field before calling `rule-get`.

### `bloggroup_id` (integer)

Used by `blog-read` and `bloggroup-read`.

- Omit this field to read blogs from all groups.
- If you need blog-group filtering, use a positive blog group ID selected from `bloggroup-read` under the same language.
- For `blog-read`, do not send this field together with `blog_id`. The rule is: omit both to read all blogs, or provide exactly one of them.
- For `bloggroup-read`, omit this field to read all blog groups.
- For `bloggroup-read`, if you need one specific blog group, send one positive existing `bloggroup_id`.

### `faqgroup_id` (integer)

Used by `faq-read` and `faqgroup-read`.

- For `faq-read`, omit this field to read FAQs from all groups. If you need FAQ-group filtering, use a positive FAQ group ID selected from `faqgroup-read` under the same language.
- For `faq-read`, do not send this field together with `faq_id`. The rule is: omit both to read all FAQs, or provide exactly one of them.
- For `faqgroup-read`, omit this field to read all FAQ groups.
- For `faqgroup-read`, if you need one specific FAQ group, send one positive existing `faqgroup_id`.

### `custompage_id` (integer)

Used by `custompage-read`.

- Omit this field to read all custom pages.
- If you need one specific custom page, send one positive existing `custompage_id`.

### `blog_id` (integer)

Used by `blog-read`.

- Omit this field to avoid exact-blog filtering.
- If you need one specific blog, send one positive existing `blog_id`.
- For `blog-read`, do not send this field together with `bloggroup_id`. The rule is: omit both to read all blogs, or provide exactly one of them.

### `faq_id` (integer)

Used by `faq-read`.

- Omit this field to avoid exact-FAQ filtering.
- If you need one specific FAQ, send one positive existing `faq_id`.
- For `faq-read`, do not send this field together with `faqgroup_id`. The rule is: omit both to read all FAQs, or provide exactly one of them.

### `ip` (string)

Used by `visitor-recent`.

- Omit this field to read recent visitors for all IPs.
- If you need one specific visitor IP, send one exact IPv4 or IPv6 address.

### `keywords` (string)

Used by `keywords-rank`.

- Omit this field to read all keyword ranking records.
- If you need one specific keyword ranking record, send one exact non-empty keyword string.
- For `keywords-rank`, do not send this field together with `rank`. The rule is: omit both to read all records, or provide exactly one of them.

### `rank` (integer)

Used by `keywords-rank`.

- Omit this field to read all keyword ranking records.
- If you need keywords ranked within the top N positions, send one integer from `1` to `999`.
- `rank=100` means return keywords ranked within positions `1` through `100`, not only keywords whose rank equals `100`.
- For `keywords-rank`, do not send this field together with `keywords`. The rule is: omit both to read all records, or provide exactly one of them.

### `parent_productsgroup_id` (integer)

Used by `productsgroup-read`.

- Omit this field or set `0` to read top-level groups.
- If provided as a positive integer (`> 0`), the API returns the direct child groups under that parent group.
- This is a parent group selector, not a leaf-group validator.
- Do not send this field together with `productsgroup_id` for `productsgroup-read`. The rule is: omit both to read top-level groups, or provide exactly one of them.

### `productsgroup_id` (integer)

Used by `products-read` and `productsgroup-read`.

- For `products-read`, omit this field to read products from all groups. If you need group filtering, use a positive leaf group ID selected from `productsgroup-read` where `is_leaf === true`.
- For `products-read`, do not send this field together with `products_id`. The rule is: omit both to read all products, or provide exactly one of them.
- For `productsgroup-read`, omit this field to avoid exact-group filtering. If provided, use one positive existing `productsgroup_id`.
- For `productsgroup-read`, do not send this field together with `parent_productsgroup_id`. The rule is: omit both to read top-level groups, or provide exactly one of them.

### `products_id` (integer)

Used by `products-read`.

- Omit this field to avoid exact-product filtering.
- If you need one specific product, send one positive existing `products_id`.
- For `products-read`, do not send this field together with `productsgroup_id`. The rule is: omit both to read all products, or provide exactly one of them.

### `pagination` (object)

Used by `blog-read`, `bloggroup-read`, `faq-read`, `faqgroup-read`, `custompage-read`, `products-read`, `inquiry-read`, `visitor-recent`, and `keywords-rank`.

```json
{
  "current_page": 1,
  "page_size": 5
}
```

### `pagination.current_page` (integer)

Used inside `pagination`.

- Use a positive integer starting from `1`.
- Omit it only if the action can rely on its server-side default.

### `pagination.page_size` (integer)

Used inside `pagination`.

- Use a positive integer.
- Keep it as small as practical for the user's stated task.
- Omit it only if the action can rely on its server-side default.

### `recent_days` (integer)

Used by `inquiry-read`.

- Omit this field to use the action without recent-day filtering.
- If provided, use one positive integer to limit the inquiry read to recent days only.

### `fields` (array)

Used when a read action supports field selection, especially `productsgroup-read`.

- Omit this field to use the action's default field set.
- If the caller needs product group section HTML fragments, include `section` in this array.
- Do not guess undocumented field names.

### `products` (object)

Used by `products-create` and `products-update`.

This object contains the product payload.

- For `products-create`, send a complete new product payload
- For `products-update`, `products_id` is required and every other field is optional
- For `products-update`, omit any field that should stay unchanged
- Do not send guessed IDs or guessed field values

For `products.productsgroup_id`:

- In `products-create`, this field is required and must be a positive leaf group ID selected from `productsgroup-read` where `is_leaf === true`.
- In `products-update`, omit this field to keep the current group unchanged. If provided, it must follow the same leaf-group rule.

Field rules:

- `products.products_id`: required only for `products-update`. This is the real existing product ID to edit.
- `products.product_name`: product title. Omit it in `products-update` if the name should not change.
- `products.model`: product model. Omit it in `products-update` if the model should not change.
- `products.upload_images`: for `products-create`, provide 1 to 5 images; the first image becomes the main image. For `products-update`, omit this field if images should not change.
- `products.attributes`: optional visible attribute pairs such as material, size, or color. Omit in `products-update` if unchanged.
- `products.tags`: search keywords. For `products-create`, provide at least 1 tag and at most 6. For `products-update`, omit if unchanged.
- `products.brief_description`: short plain-text summary. Omit in `products-update` if unchanged.
- `products.description`: detailed HTML description. HTML fragment only. Do not include any `<h1>` tag, and prefer `<h2>` to `<h6>`. Allow at most 50 `<img>` tags, with each image 500 kB or smaller, and keep the 100,000-character limit after removing `<img>` tags. Follow the `rule-get` payload, including the current tenant structure rules such as one root `<section>` element and one embedded `<style>` block placed at the end of the fragment. Do not use inline style attributes as the main styling method. Omit in `products-update` if unchanged.
- `products.seo.keywords`: one comma-separated string, not an array.

### `blog` (object)

Used by `blog-create` and `blog-update`.

- `blog.blog_id`: required for `blog-update`. This is the existing blog ID to edit.
- `blog.bloggroup_id`: required blog group ID for `blog-create`. In `blog-update`, omit it if the blog should stay in the current group.
- `blog.publisher`: optional publisher name, up to 100 characters. Omit it in `blog-update` if unchanged.
- `blog.publication_date`: optional display date in `yyyy/M/d` format, for example `2026/4/24`. Omit it in `blog-update` if unchanged.
- `blog.title`: required blog title for `blog-create`, up to 500 characters. Omit it in `blog-update` if unchanged.
- `blog.cover_image`: required cover image object with `name` and `base64` for `blog-create`. In `blog-update`, omit it if the cover image should stay unchanged.
- `blog.tags`: required keyword list with 1 to 6 items for `blog-create`. Omit in `blog-update` if unchanged.
- `blog.summary`: required plain-text summary for `blog-create`, up to 500 characters. Omit in `blog-update` if unchanged.
- `blog.description`: required HTML content for `blog-create`, up to 100,000 characters after removing `<img>` tags, with at most 50 `<img>` tags. Do not include any `<h1>` tag; use `<h2>` to `<h6>` or normal block elements instead. Omit in `blog-update` if unchanged.
- `blog.seo`: optional SEO object with `title`, `description`, and `keywords`. Omit it in `blog-update` if SEO should stay unchanged.

### `faq` (object)

Used by `faq-create` and `faq-update`.

- `faq.faq_id`: required for `faq-update`. This is the existing FAQ ID to edit.
- `faq.faqgroup_id`: required FAQ group ID for `faq-create`. In `faq-update`, omit it if the FAQ should stay in the current group.
- `faq.cover_image`: optional cover image object with `name` and `base64`. Omit it in `faq-update` if the cover image should stay unchanged.
- `faq.question`: required FAQ question for `faq-create`, up to 100 characters. Omit it in `faq-update` if unchanged.
- `faq.tags`: required keyword list with 1 to 6 items for `faq-create`. Omit it in `faq-update` if unchanged.
- `faq.summary`: required plain-text summary for `faq-create`, up to 500 characters. Omit it in `faq-update` if unchanged.
- `faq.answer`: required HTML content for `faq-create`, up to 100,000 characters after removing `<img>` tags, with at most 50 `<img>` tags. Generate it only after calling `rule-get` with exact `language` and exact `scene=faq.answer`. Do not include any `<h1>` tag, and prefer `<h2>` to `<h6>`. Omit it in `faq-update` if unchanged.
- `faq.seo`: optional SEO object with `title`, `description`, and `keywords`. Omit it in `faq-update` if SEO should stay unchanged.

### `productsgroup` (object)

Used by `productsgroup-create` and `productsgroup-update`.

- `productsgroup.parent_productsgroup_id`: optional parent group ID. Omit it or set `0` for a top-level group.
- `productsgroup.productsgroup_id`: required for `productsgroup-update`. This is the existing product group ID to edit.
- `productsgroup.group_name`: required product group name, up to 200 characters.
- `productsgroup.tags`: required keyword list with 1 to 6 items. Each tag must contain 3 to 50 characters.
- `productsgroup.brief_description`: optional short plain-text description, up to 4,000 characters.
- `productsgroup.section`: optional custom HTML decoration object for the product group detail page body.
- `productsgroup.section.top`: optional product group page header decoration fragment. HTML fragment only. Do not include any `<h1>` tag, and prefer `<h2>` to `<h6>`. Maximum length: 100,000 characters after removing `<img>` tags, with at most 50 `<img>` tags. Follow the `rule-get` payload, including the current tenant structure rules such as one root `<section>` element and one embedded `<style>` block placed at the end of the fragment. Do not use inline style attributes as the main styling method. In `productsgroup-update`, omit this field or pass an empty string to keep the current top fragment unchanged.
- `productsgroup.section.bottom`: optional product group page footer decoration fragment. HTML fragment only. Do not include any `<h1>` tag, and prefer `<h2>` to `<h6>`. Maximum length: 100,000 characters after removing `<img>` tags, with at most 50 `<img>` tags. Follow the `rule-get` payload, including the current tenant structure rules such as one root `<section>` element and one embedded `<style>` block placed at the end of the fragment. Do not use inline style attributes as the main styling method. In `productsgroup-update`, omit this field or pass an empty string to keep the current bottom fragment unchanged.
- `custompage.content`: required HTML content for `custompage-create`, up to 100,000 characters after removing `<img>` tags, with at most 50 `<img>` tags. Generate it only after calling `rule-get` with exact `language` and exact `scene=custompage.content`. Follow the returned rule payload, including the current tenant structure rules such as one root `<section>` element and one embedded `<style>` block placed at the end of the fragment. Do not use inline style attributes as the main styling method. Omit it in `custompage-update` if unchanged.
- `productsgroup.seo`: optional for `productsgroup-update`. Omit it if SEO should stay unchanged.

### `bloggroup` (object)

Used by `bloggroup-create` and `bloggroup-update`.

- `bloggroup.bloggroup_id`: required for `bloggroup-update`. This is the existing blog group ID to edit.
- `bloggroup.group_name`: required blog group name for `bloggroup-create`, up to 100 characters. Omit it in `bloggroup-update` if unchanged.
- `bloggroup.tags`: required keyword list with 1 to 6 items for `bloggroup-create`. Omit it in `bloggroup-update` if unchanged.
- `bloggroup.brief_description`: optional short plain-text description, up to 300 characters. Omit it in `bloggroup-update` if unchanged.
- `bloggroup.seo`: optional SEO object with `title`, `description`, and `keywords`. Omit it in `bloggroup-update` if SEO should stay unchanged.

### `faqgroup` (object)

Used by `faqgroup-create` and `faqgroup-update`.

- `faqgroup.faqgroup_id`: required for `faqgroup-update`. This is the existing FAQ group ID to edit.
- `faqgroup.group_name`: required FAQ group name for `faqgroup-create`, up to 100 characters. Omit it in `faqgroup-update` if unchanged.
- `faqgroup.brief_description`: optional short plain-text description, up to 300 characters. Omit it in `faqgroup-update` if unchanged.
- `faqgroup.seo`: optional SEO object with `title`, `description`, and `keywords`. Omit it in `faqgroup-update` if SEO should stay unchanged.

### `custompage` (object)

Used by `custompage-create` and `custompage-update`.

- `custompage.custompage_id`: required for `custompage-update`. This is the existing custom page ID to edit.
- `custompage.title`: required title for `custompage-create`, up to 100 characters. Omit it in `custompage-update` if unchanged.
- `custompage.content`: required HTML content for `custompage-create`, up to 100,000 characters after removing `<img>` tags, with at most 50 `<img>` tags. Generate it only after calling `rule-get` with exact `language` and exact `scene=custompage.content`. Follow the returned rule payload, including the current tenant structure rules such as one root `<section>` element and one embedded `<style>` block placed at the end of the fragment. Do not use inline style attributes as the main styling method. Omit it in `custompage-update` if unchanged.
- `custompage.seo`: optional SEO object with `title`, `description`, and `keywords`. Omit it in `custompage-update` if SEO should stay unchanged.

### `id_list` (array)

Used by `blog-delete`, `bloggroup-delete`, `custompage-delete`, `faq-delete`, `faqgroup-delete`, `productsgroup-delete`, and `products-delete`.

### `confirmation` (object)

Required by `blog-create`, `blog-update`, `blog-delete`, `bloggroup-create`, `bloggroup-update`, `bloggroup-delete`, `custompage-create`, `custompage-update`, `custompage-delete`, `faq-create`, `faq-update`, `faq-delete`, `faqgroup-create`, `faqgroup-update`, `faqgroup-delete`, `productsgroup-create`, `productsgroup-update`, `productsgroup-delete`, `products-create`, `products-update`, and `products-delete`.

Before any create, update, or delete action, show the user the language and the exact payload or product IDs to be changed, then set:

```json
{
  "approved": true,
  "summary": "Confirmed by user: update product 123 in language en with the shown payload."
}
```

For every `*_update` action, this skill also enforces a pre-update backup capture and file persistence step.

- The current record must be read successfully before the update request is sent.
- The backup must be written to a local JSON file under `backups/<action>/` relative to the current installed skill root.
- That local JSON file persists `confirmation_summary`, `raw_read_response`, `snapshot`, `requested_update_payload`, `restore_payload`, and `restore_limitations`.
- That local backup file may contain sensitive business or personal data copied from the current record and requested update payload, so the user must be aware of and approve that local persistence before the update runs.
- If backup capture fails, or if the backup file cannot be written, the update must not run.
- If the update succeeds, the response includes `backup.storage.file_path`, `backup.raw_read_response`, `backup.snapshot`, and a best-effort `backup.restore_payload`.
- If the user later says the edit result is wrong, reuse that `backup.restore_payload` with the same `*_update` action to restore the previous state.
- Uploaded images are only partially restorable because the read APIs do not return the original image base64 content.

## Action Guide

### `languages-get`

Returns the list of enabled site languages.

Common user intents:

- "Show enabled languages"
- "What language codes can I use?"

### `rule-get`

Returns the tenant HTML generation rule payload for one exact `language` and one exact `scene`.

This action is the required source of truth before generating any supported HTML fragment.

Execution rules:

- `language` is required and must be one exact enabled site language.
- `scene` is required and must be one exact supported scene value.
- Call this action before generating `blog.description`, `faq.answer`, `products.description`, `productsgroup.section.top`, `productsgroup.section.bottom`, or `custompage.content`.
- If this action fails, stop and report the failure instead of guessing colors, fonts, links, layout, or any other HTML fragment rule.

Common user intents:

- "Read the product description HTML rules"
- "Show the blog description rule payload"
- "Get the product group top section rules"
- "Check the exact Tradebee HTML generation rules for this scene"

### `blog-create`

Creates and publishes a new blog under the selected language and blog group.

This action must not run unless the user has explicitly confirmed the language and exact blog payload to be created.

Common user intents:

- "Create a blog"
- "Publish an article"

### `blog-update`

Updates an existing blog under the selected language.

This action must not run unless the user has explicitly confirmed the language, target blog ID, and exact payload to be changed.

Update rules:

- `blog.blog_id` is required
- Any field other than `blog_id` should be omitted unless the user explicitly wants to change it
- Omitting a field means keep the existing value
- Do not move the blog group unless the user explicitly asks for that change
- Capture a pre-update backup snapshot first; if backup capture fails, abort the update
- Return `backup.restore_payload` on success so the same blog can be restored later if needed

Common user intents:

- "Update blog 123"
- "Edit blog information"

### `blog-read`

Returns published blog data with optional pagination, blog-group filtering, or exact blog filtering.

Common user intents:

- "Read blogs"
- "List blog articles"
- "Find blog 123"

### `blog-delete`

Moves one or more blogs to the recycle bin.

This action must not run unless the user has explicitly confirmed the language and exact blog IDs to be moved.

Common user intents:

- "Delete these blogs"
- "Move blog 123 to recycle bin"

### `bloggroup-create`

Creates and publishes a new blog group under the selected language.

This action must not run unless the user has explicitly confirmed the language and exact blog group payload to be created.

Common user intents:

- "Create a blog group"
- "Add a blog category"

### `bloggroup-update`

Updates an existing blog group under the selected language.

This action must not run unless the user has explicitly confirmed the language, target blog group ID, and exact payload to be changed.

Update rules:

- `bloggroup.bloggroup_id` is required
- Any field other than `bloggroup_id` should be omitted unless the user explicitly wants to change it
- Omitting a field means keep the existing value
- Capture a pre-update backup snapshot first; if backup capture fails, abort the update
- Return `backup.restore_payload` on success so the same blog group can be restored later if needed

Common user intents:

- "Update blog group 456"
- "Edit blog category"

### `bloggroup-read`

Returns blog group data for a selected language with optional exact group filtering, field selection, and pagination.

Common user intents:

- "List blog groups"
- "Read one exact blog group"

### `bloggroup-delete`

Deletes one or more blog groups for a selected language and returns separate success and failure ID lists.

This action must not run unless the user has explicitly confirmed the language and exact blog group IDs to delete.

Common user intents:

- "Delete these blog groups"

### `faq-create`

Creates and publishes a new FAQ under the selected language and FAQ group.

This action must not run unless the user has explicitly confirmed the language and exact FAQ payload to be created.

Common user intents:

- "Create an FAQ"
- "Publish an FAQ entry"

### `faq-update`

Updates an existing FAQ under the selected language.

This action must not run unless the user has explicitly confirmed the language, target FAQ ID, and exact payload to be changed.

Update rules:

- `faq.faq_id` is required
- Any field other than `faq_id` should be omitted unless the user explicitly wants to change it
- Omitting a field means keep the existing value
- Do not move the FAQ group unless the user explicitly asks for that change
- Capture a pre-update backup snapshot first; if backup capture fails, abort the update
- Return `backup.restore_payload` on success so the same FAQ can be restored later if needed

Common user intents:

- "Update FAQ 123"
- "Edit FAQ information"

### `faq-read`

Returns published FAQ data with optional pagination, FAQ-group filtering, or exact FAQ filtering.

Common user intents:

- "Read FAQs"
- "List FAQ entries"
- "Find FAQ 123"

### `faq-delete`

Moves one or more FAQs to the recycle bin.

This action must not run unless the user has explicitly confirmed the language and exact FAQ IDs to be moved.

Common user intents:

- "Delete these FAQs"
- "Move FAQ 123 to recycle bin"

### `faqgroup-create`

Creates and publishes a new FAQ group under the selected language.

This action must not run unless the user has explicitly confirmed the language and exact FAQ group payload to be created.

Common user intents:

- "Create an FAQ group"
- "Add an FAQ category"

### `faqgroup-update`

Updates an existing FAQ group under the selected language.

This action must not run unless the user has explicitly confirmed the language, target FAQ group ID, and exact payload to be changed.

Update rules:

- `faqgroup.faqgroup_id` is required
- Any field other than `faqgroup_id` should be omitted unless the user explicitly wants to change it
- Omitting a field means keep the existing value
- Capture a pre-update backup snapshot first; if backup capture fails, abort the update
- Return `backup.restore_payload` on success so the same FAQ group can be restored later if needed

Common user intents:

- "Update FAQ group 456"
- "Edit FAQ category"

### `faqgroup-read`

Returns FAQ group data for a selected language with optional exact group filtering, field selection, and pagination.

Common user intents:

- "List FAQ groups"
- "Read one exact FAQ group"

### `faqgroup-delete`

Deletes one or more FAQ groups for a selected language and returns separate success and failure ID lists.

This action must not run unless the user has explicitly confirmed the language and exact FAQ group IDs to delete.

Common user intents:

- "Delete these FAQ groups"

### `custompage-create`

Creates and publishes a new custom page under the selected language.

This action must not run unless the user has explicitly confirmed the language and exact custom page payload to be created.

Common user intents:

- "Create a custom page"
- "Publish a custom page"

### `custompage-update`

Updates an existing custom page under the selected language.

This action must not run unless the user has explicitly confirmed the language, target custom page ID, and exact payload to be changed.

Update rules:

- `custompage.custompage_id` is required
- Any field other than `custompage_id` should be omitted unless the user explicitly wants to change it
- Omitting a field means keep the existing value
- Capture a pre-update backup snapshot first; if backup capture fails, abort the update
- Return `backup.restore_payload` on success so the same custom page can be restored later if needed

Common user intents:

- "Update custom page 123"
- "Edit custom page information"

### `custompage-read`

Returns custom page data with optional pagination, field selection, or exact custom page filtering.

Common user intents:

- "Read custom pages"
- "List custom pages"
- "Find custom page 123"

### `custompage-delete`

Moves one or more custom pages to the recycle bin.

This action must not run unless the user has explicitly confirmed the language and exact custom page IDs to be moved.

Common user intents:

- "Delete these custom pages"
- "Move custom page 123 to recycle bin"

### `productsgroup-create`

Creates and publishes a new product group under the selected language.

This action must not run unless the user has explicitly confirmed the language and exact product group payload to be created.

Common user intents:

- "Create a product group"
- "Add a product category"

### `productsgroup-update`

Updates an existing product group under the selected language.

This action must not run unless the user has explicitly confirmed the language, target product group ID, and exact payload to be changed.

Update rules:

- `productsgroup.productsgroup_id` is required
- Any field other than `productsgroup_id` should be omitted unless the user explicitly wants to change it
- Omitting a field means keep the existing value
- If `productsgroup.section` is sent, `top` and `bottom` can be updated independently: omit one fragment or send an empty string to keep it unchanged
- Capture a pre-update backup snapshot first; if backup capture fails, abort the update
- Return `backup.restore_payload` on success so the same product group can be restored later if needed

Common user intents:

- "Update product group 456"
- "Edit product category"

### `productsgroup-delete`

Deletes one or more product groups for a selected language and returns separate success and failure ID lists.

This action must not run unless the user has explicitly confirmed the language and exact product group IDs to delete.

Common user intents:

- "Delete these product groups"

### `productsgroup-read`

Returns published product groups for a selected language.

Filter rules:

- Omit `parent_productsgroup_id` or set it to `0` to read top-level groups.
- Send `parent_productsgroup_id` to read the direct child groups under one parent group.
- Send `productsgroup_id` to read one exact product group.
- `parent_productsgroup_id` and `productsgroup_id` are mutually exclusive and must not be sent together.
- Use `fields=["section"]` or include `section` in the field list when the caller needs the custom top/bottom HTML fragments.

Common user intents:

- "List product groups"
- "Read top-level groups"
- "Read child groups under this parent"
- "Find product group 789"

### `products-read`

Returns published product data with optional pagination, product group filtering, or exact product filtering.

Filter rules:

- You may omit both `products_id` and `productsgroup_id` to read all products.
- You may send `products_id` to read one exact product.
- You may send `productsgroup_id` to read products under one leaf group.
- `products_id` and `productsgroup_id` are mutually exclusive and must not be sent together.

Common user intents:

- "Read products"
- "List products in this group"
- "Find product 123"

### `products-create`

Creates a new product under the selected language and product group.

This action must not run unless the user has explicitly confirmed the language and exact product payload to be created.

Minimum practical payload:

- `language`
- `products.productsgroup_id`
- `products.product_name`
- `products.upload_images`
- `products.tags`
- `products.brief_description`
- `products.description`
- `confirmation.approved=true`
- `confirmation.summary`

Common user intents:

- "Create a product"
- "Publish a new product"

### `products-update`

Updates an existing product under the selected language.

This action must not run unless the user has explicitly confirmed the language, target product ID, and exact payload to be changed.

Update rules:

- `products.products_id` is required
- Any field other than `products_id` should be omitted unless the user explicitly wants to change it
- Omitting a field means keep the existing value
- Do not move the product group unless the user explicitly asks for that change
- Capture a pre-update backup snapshot first; if backup capture fails, abort the update
- Return `backup.restore_payload` on success so the same product can be restored later if needed

Common user intents:

- "Update product 123"
- "Edit product information"

### `products-delete`

Moves one or more products to the recycle bin.

This action must not run unless the user has explicitly confirmed the language and exact product IDs to be moved to the recycle bin.

Common user intents:

- "Delete these products"
- "Move product 123 to recycle bin"

### `inquiry-read`

Returns inquiry records with optional language, recent-day filtering, and pagination.

Common user intents:

- "Read inquiries"
- "Show recent leads"
- "List inquiry records"

### `visitor-recent`

Returns recent visitor analytics with optional exact IP filtering and pagination.

Common user intents:

- "Check recent visitors"
- "Find visitor by IP"
- "Show latest visitor behavior"

### `keywords-rank`

Returns keyword ranking records with optional exact keyword filtering, optional top-N rank filtering, pagination, latest rank values, and rank history.

Common user intents:

- "Check keyword ranking"
- "Find one keyword ranking"
- "Show keywords ranked within top 100"

## Extension Rule

When adding a new Tradebee capability in the future:

1. Add or update the underlying implementation module.
2. Register the new action in the root `index.js` action router.
3. Add the new action to the root `skill.json` input schema.
4. Document the new action here in the root `SKILL.md`.

Changes are not complete unless the unified `tradebee` entrypoint supports the new capability end to end.

## Example

```json
{
  "action": "products-read",
  "language": "en",
  "products_id": 12345,
  "pagination": {
    "current_page": 1,
    "page_size": 5
  }
}
```

## Decision Examples

```text
User: "Help me check the product categories"
Choose: productsgroup-read
Reason: the user wants product category data, not product data
```

```text
User: "Show what products are under this category"
Choose: products-read + productsgroup_id
Reason: the user wants product records under one group
```

```text
User: "Help me find product 12345"
Choose: products-read + products_id
Reason: the user wants one exact product
```

```text
User: "Show recent visits and filter this IP"
Choose: visitor-recent + ip
Reason: this is visitor analytics, not inquiry or product content
```

```text
User: "Check the top 100 keywords"
Choose: keywords-rank + rank=100
Reason: the user wants a top-N ranking slice, not one exact keyword
```

