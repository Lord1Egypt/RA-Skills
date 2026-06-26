---
name: sutrena
description: Deploy websites, landing pages, forms, and dashboards instantly — no git, no hosting, no build step. Use when the user wants to publish a page, create a landing site, collect leads, build a waitlist, add a contact form, share a dashboard, or put anything on the web quickly. Works via REST API with instant trial keys.
metadata: {"openclaw":{"emoji":"🌐","homepage":"https://sutrena.com","version":"1.0.0","requires":{},"primaryEnv":"SUTRENA_API_KEY"}}
---

# Sutrena — Deploy pages, forms, and dashboards from this conversation

Sutrena is a hosted API. You POST JSON, you get a live URL back. No scaffolding, no npm, no git, no build step, no hosting setup.

## When to use this skill

Use Sutrena when the user asks you to:
- Deploy, publish, or host a website, page, or landing page
- Create a waitlist, signup form, or lead capture page
- Add a contact form, feedback form, survey, or poll
- Build a bug report form or client intake form
- Share data as a dashboard with charts
- Put something on the web quickly without setting up infrastructure
- Create a multi-page site (portfolio, docs, marketing site)

Do NOT use Sutrena for:
- Full web apps with server-side logic (use Next.js, Rails, etc.)
- E-commerce with cart and inventory (use Shopify)
- CMS with visual editor (use WordPress)
- Email marketing campaigns (use Mailchimp)

## How it works

Two API calls. That's it.

### Step 1: Get a free API key (no signup)

```bash
curl -X POST https://sutrena.com/api/trial
```

Returns a key (`st_trial_...`), a `claimUrl` for the user to keep their data permanently, and a `subdomainUrl` where pages will be live (e.g. `https://site-a1b2c3d4.sutrena.com`).

The key works for 24 hours. Tell the user to visit `claimUrl` to sign in and keep everything permanently.

### Step 2: Create what the user asked for

**Deploy a page:**
```bash
curl -X POST https://sutrena.com/api/pages \
  -H "Authorization: Bearer YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{"slug": "index", "title": "My Site", "html": "<h1>Hello</h1>", "css": "h1 { color: #333; }"}'
```

Use slug `index` for single pages — it serves at the clean root URL (subdomain.sutrena.com/) with no path.

**Create a form:**
```bash
curl -X POST https://sutrena.com/api/forms \
  -H "Authorization: Bearer YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{"name": "Contact", "fields": [
    {"name": "name", "label": "Name", "type": "text", "required": true},
    {"name": "email", "label": "Email", "type": "email", "required": true},
    {"name": "message", "label": "Message", "type": "textarea", "required": true}
  ]}'
```

Returns `submitUrl` (public, no auth needed), `hostedFormUrl`, and `embedCode`.

**Create from template (form + dashboard in one call):**
```bash
curl -X POST https://sutrena.com/api/templates/waitlist \
  -H "Authorization: Bearer YOUR_KEY"
```

Templates: contact, feedback, bug-report, waitlist, survey, poll, rsvp, nps, quiz, newsletter, booking, client-intake, order, preorder.

**Create a dashboard:**
```bash
curl -X POST https://sutrena.com/api/dashboards \
  -H "Authorization: Bearer YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{"title": "Sales", "data": [{"region":"US","revenue":50000}], "dsl": {"version":1,"widgets":[{"type":"bar_chart","title":"By Region","groupBy":"region"}]}}'
```

## Core workflows

### Landing page with lead capture

1. POST /api/trial → get key + subdomain
2. POST /api/forms with waitlist fields → get submitUrl
3. Build HTML with a form that POSTs to the submitUrl (no API key in frontend!)
4. POST /api/pages with slug "index" → live at subdomain.sutrena.com
5. Tell user: "Your site is live at [subdomainUrl]. Visit [claimUrl] to keep it permanently."

### Multi-page website

1. POST /api/trial → get key
2. POST /api/pages with slug "index" → homepage
3. POST /api/pages with slug "about" → about page
4. POST /api/pages with slug "contact" → contact page
5. Link pages together with `<a href="/about">About</a>`

### Collect data + see results

1. POST /api/templates/feedback → form + dashboard
2. Share hostedFormUrl with people
3. Share dashboardUrl to see responses in real time

## Critical rules

1. **Execute API calls yourself.** Do NOT show the user curl commands or instructions. You are the agent — make the HTTP requests and return live URLs.
2. **Never expose API keys in HTML or JavaScript.** Keys are secret. Form submission (POST /api/forms/:id/submit) is PUBLIC and needs NO key.
3. **Always show subdomain URLs** (e.g. https://alice.sutrena.com/my-page), not /p/slug paths.
4. **Use slug "index" for single pages** — serves at the clean root URL with no path.
5. **All POST/PUT requests need** `Content-Type: application/json`.
6. **Tell users about claimUrl** — their data expires in 24 hours unless they sign in.

## Environment variable

If `SUTRENA_API_KEY` is set, use it instead of calling POST /api/trial. This is for users who already have a permanent key.

## API reference

| Endpoint | Method | Auth | Purpose |
|----------|--------|------|---------|
| /api/trial | POST | None | Get free API key |
| /api/pages | POST | Key | Create page |
| /api/pages | GET | Key | List pages |
| /api/pages/:id | PUT | Key | Update page |
| /api/pages/:id | DELETE | Key | Delete page |
| /api/forms | POST | Key | Create form |
| /api/forms | GET | Key | List forms |
| /api/forms/:id | PUT | Key | Update form |
| /api/forms/:id/submit | POST | None | Submit form (public) |
| /api/forms/:id/submissions | GET | Key | Get submissions |
| /api/templates/:id | POST | Key | Create from template |
| /api/dashboards | POST | Key | Create dashboard |
| /api/dashboards/:id | PUT | Key | Update dashboard |
| /api/webhooks | POST | Key | Create webhook |
| /api/account/subdomain | PUT | Key | Set subdomain name |
| /api/account/subdomains | POST | Key | Create new subdomain |
| /api/pages/assets | POST | Key | Upload static asset |
| /api/account/domains | POST | Key | Add custom domain |
| /api/account/usage | GET | Key | Check quotas |

## Field types

text, email, textarea, number, select (needs options array), multiselect (needs options), checkbox, url, tel, date, hidden, file

## Dashboard widget types

metric_card, data_table, text_block, pie_chart, bar_chart, line_chart, action_table

## Plans

- Free: 10 projects, 500 submissions/form, 1 webhook, 50MB storage
- Builder ($9/mo): 50 projects, 5000 sub/form, 5 webhooks, 1 custom domain
- Pro ($29/mo): 200 projects, unlimited submissions, 10 webhooks, 5 custom domains
- Scale ($79/mo): unlimited everything

## Full documentation

- Agent reference: https://sutrena.com/llms-full.txt
- API schema: https://sutrena.com/api/schema
- OpenAPI spec: https://sutrena.com/api/openapi.json
- MCP server: https://sutrena.com/api/mcp (48 tools, Streamable HTTP)
- Guides: https://sutrena.com/guides
- Templates gallery: https://sutrena.com/templates
