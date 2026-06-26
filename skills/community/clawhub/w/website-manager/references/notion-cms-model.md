# Notion CMS Model

Use this model when the website should be managed in Notion.

## Required access for automated CMS creation

If the agent is expected to create the CMS automatically, it needs:
- `NOTION_ACCESS_TOKEN` or `NOTION_TOKEN`
- `NOTION_PARENT_PAGE_ID`

Recommended default:
- create one parent page such as `Website CMS`
- share that page with the Notion integration
- create all CMS databases as children of that parent page
- use `scripts/create_notion_cms.py` to provision the default CMS layout and starter records
- persist the returned hub page id, database ids, and data source ids to `.website-manager/notion.json`
- mirror non-secret ids into Site Settings if the publishing workflow needs them there

Do not assume the integration can create top-level workspace content without the parent page being shared first.

## Principle

Notion owns:
- page content
- collection items
- SEO copy
- global settings

Code owns:
- layouts
- rendering
- interaction logic
- deployment

## Recommended databases

Default statuses across content databases:
- `Draft`
- `Ready`
- `Published`
- `Needs Update`

### Pages

For core pages such as:
- home
- about
- contact
- landing pages

Suggested properties:
- `Page Name`
- `Slug`
- `Status`
- `SEO Title`
- `SEO Description`
- `Hero Headline`
- `Hero Subtext`
- `Primary CTA Label`
- `Primary CTA URL`
- `Secondary CTA Label`
- `Secondary CTA URL`
- `Last Published`

Default slug rule:
- lowercase
- words separated with hyphens
- no leading or trailing slash
- use `home` for the homepage row and map it to `/` in the publishing layer

### Collections or Services

For service pages, directories, resources, team entries, or other structured sections.

Suggested properties:
- `Name`
- `Slug`
- `Status`
- `Category`
- `Summary`
- `Headline`
- `SEO Title`
- `SEO Description`
- `Featured`
- `Sort Order`
- `Primary CTA URL`
- `Tags`

Default collection rules:
- `Category` should be a single normalized select value
- `Tags` should be a multi-select with clean human labels
- `Sort Order` should exist whenever manual ordering matters
- `Featured` should be boolean

### Blog Posts

Suggested properties:
- `Post Title`
- `Slug`
- `Status`
- `Category`
- `Tags`
- `SEO Title`
- `SEO Description`
- `Hero Image URL`
- `Author`
- `Published Date`
- `Featured`

Default blog rules:
- every post has one primary `Category`
- tags are optional
- `Published Date` is required before publishing
- featured posts appear in the top section of the listing page

### Site Settings

Use as a key-value table for:
- business name
- address
- phone
- email
- hours
- social links
- announce bar content
- color tokens
- hosting identifiers

## Filtering and listing considerations

When a collection is driven from Notion, the website should be able to support:
- category filters
- tag filters
- search
- featured items
- pagination or load-more
- empty states

Keep filter values normalized in Notion so front-end logic stays predictable.

Default filter model:
- category is always available on listing pages
- tag filters appear only when the collection is complex enough to justify them
- search indexes title, summary, category, and tags
