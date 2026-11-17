# Webstudio Features (Advanced)

The bigger Webstudio feature set beyond basic page building. Source: official docs
(CMS, Data variables, Expression editor, Collection, integrations, CLI).

## CMS (backend-agnostic content)

Webstudio is backend-agnostic - connect to ANY backend with an HTTP API (CMS, CRM,
database). The building blocks:

1. **Dynamic pages** - a template page whose content changes by URL. Adding a
   dynamic parameter to a path makes it dynamic (`/post/:slug`, optional `:slug?`,
   wildcard `/*` or `/:name*`). The parameter value comes from the URL.
2. **Resources** (data variables) - fetch data from an API to use in the page.
3. **Bindings** (Expression editor) - connect/map the fetched data to components.

### Dynamic pages

- The Address Bar previews dynamic pages in the editor by entering a test parameter
  value (the static path part is already there - don't retype it).
- A Resource fetches based on the URL param, e.g. `posts(slug: system.params.slug)`.

### Handling dynamic 404s

When a dynamic URL exists but the query returns no data, return 404:
1. Page Settings > Status Code, bind an expression like `cmsData.data[0].id ? 200 : 404`.
2. Show 404 content conditionally: bind a Box's Show to `!cmsData.data[0].id`.
3. Hide regular content: bind its Show to `cmsData.data[0].id`.
Alternative: Page Settings > Redirect bound to `!cmsData.data[0].id ? "/404" : ""`.

### Compatible CMSs

Any CMS with an HTTP API. Documented: Hygraph, Sanity, Strapi, Contentful,
WordPress, Drupal, Directus, Hashnode, Payload, Airtable, Baserow, Notion, Flotiq,
Ghost, Coda, Hyvor. Rich text support varies by CMS - Webstudio supports rich text
delivered as HTML or Markdown (bind HTML to Content Embed, Markdown to Markdown
Embed). Use the Headless CMS Finder (wstd.us/cms-finder) to compare.

## Data variables

Defined on any instance (Global Root, Body, Heading) in the Settings panel. Scope:
available on the instance it's defined on and its children, NOT the parent. Define
on Global Root for site-wide access (email, social links, API endpoints, JSON for
simple CMS). To use a variable in Page Settings, define it on the Body.

Types:
- **System** - exists by default: `Params` (dynamic page URL params), `Search`
  (query params), `Origin` (current site URL), `Pathname` (current path).
- **String** - text content.
- **Number** - numeric values.
- **Boolean** - true/false (visibility toggles).
- **JSON** - structured data for Collections.
- **Resource** - value from a fetch (REST). Fields: URL, Method, Search Params,
  Cache Max Age, Headers. Pasting a cURL command auto-fills the fields. Data is
  fetched via Cloudflare Workers with caching (Cache Max Age overrides origin
  headers).
- **GraphQL** - for GraphQL APIs: URL, Query, Variables (e.g.
  `{ slug: system.params.slug }`).
- **System Resource** - internal data: Sitemap (build custom sitemaps), Current Date.

## Expression editor

Available on every field via the "+" button. Two uses:
1. **Binding** - connect external data to a field. Drill into a variable with `.`
   (e.g. `CMS Data.title`, `CMS Data.image.url`).
2. **Expressions** - a safe subset of JavaScript: ternary (`cond ? a : b`),
   template literals (backticks + `${}`), concatenation (`"a" + b`), and safe
   string/array methods (split, replace, slice, includes, join, etc.).

Examples: conditionally show content with `CMS Data.image ? true : false` bound to
Show; build JSON-LD schema with a template literal; hide the current post in a
related list with `system.params.slug === collectionItem.slug ? false : true`.

## Collections & reusable components

- **Collection** - iterate over JSON or Resource data to render lists (e.g. a
  dynamic gallery or blog list).
- **Slot** - reusable regions; can reference global variables / dynamic content.
- **Component** / reusable components - build once, reuse. Template instances.
- **Content Block** - designer-specified editable regions; the only thing editable
  in Content mode (see `ui-builder.md`).

## Forms

Form components nest the building blocks (input, textarea, checkbox, radio,
select, label, button). A **Webhook Form** posts submissions to an external
endpoint (integrates with Airtable, n8n, Zapier, etc. - see integrations).

## Integrations

Documented: Airtable (form webhook / frontend), Baserow, Flotiq, Hygraph, n8n,
Notion, Pabbly, Supabase, WordPress, Zapier. CMS integrations connect external
content (see CMS above); automation integrations handle form/webhook flows.

## Marketplace

Browse/install templates and components from the Webstudio marketplace (also
publish your own - see contributing/marketplace docs).

## Webstudio AI

There's a Webstudio AI feature (docs/university/webstudio-ai.md) for AI-assisted
building inside the platform.

## CLI / MCP / headless

- **CLI** (`npx webstudio`): export/build projects, publish, manage domains,
  inspect permissions, capture screenshots. Needs a share link with Build access.
  See `install.md`.
- **MCP** (docs/university/mcp.md): Webstudio exposes automation to tools via MCP.
- **Headless API**: authorization tokens with scoped permissions (`canClone`,
  `canCopy`, `canPublish`, `canUseApi`) - see `publishing.md` and `api.md`.

## Radix components

Webstudio ships a Radix component set (accordion, checkbox, collapsible, dialog,
label, navigation-menu, popover, radio-group, select, sheet, switch, tabs,
tooltip) for accessible UI primitives.
