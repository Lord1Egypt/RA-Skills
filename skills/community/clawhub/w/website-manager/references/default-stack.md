# Default Stack

Read this first. This is the opinionated default this skill should choose unless the user explicitly asks for something else.

## Default build stack

- site implementation: plain HTML, CSS, and JavaScript
- structure: reusable shell plus page templates
- CMS: Notion
- host: Netlify
- repo: optional GitHub, not required on day one
- automation: OpenClaw cron when available

## Default content model

- `Pages` database for core pages
- `Collections` database for services, resources, directories, or custom content sections
- `Blog Posts` database for editorial content
- `Site Settings` database for global values

## Default CMS provisioning rule

- use a Notion internal integration token
- require a shared parent page id
- create the CMS databases under that parent page

## Default site-type rule

- use a specialized site type only when the business clearly fits it
- otherwise use the generic type
- do not force a vertical-specific layout system onto broad or mixed-content websites

## Default route model

- `/` homepage
- `/about` about page
- `/contact` contact page
- `/blog` blog listing
- `/blog/{slug}` article template output or live CMS route
- `/{collection}` collection listing
- `/{collection}/{slug}` collection detail route

## Default listing UX

- featured items at the top when available
- category chips under the intro
- search across title, excerpt, tags, and category
- pagination at 9 items per page
- URL query params for active category and search
- empty-state message with reset control

## Default deployment model

- first deploy without Git if the user is solo and non-technical
- use the Netlify deploy helper for the first release
- add GitHub only when previews, reviews, or collaboration are needed
- persist returned non-secret runtime ids to a local JSON file and optionally mirror them into Notion Site Settings

## Default live-vs-rebuild split

Rebuild:
- homepage
- static pages
- footer and nav
- site settings
- collection landing pages

Live or semi-live CMS mode when needed:
- blog listings
- blog detail pages
- lightweight searchable collections

## Default rule

Do not ask the user to choose among five architectures.
Choose this one first, explain it briefly, and move forward.
