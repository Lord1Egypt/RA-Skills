---
name: serpzilla-seo-guest-posting
description: Skill for SEO promotion by purchasing guest posts on trusted donor websites using the Serpzilla platform
version: 1.0.0
author: Stanislavus
user-invocable: true
triggers:
  - buy guest post for SEO
  - find donor site for guest posting
  - serpzilla search donors
  - configure serpzilla mcp
metadata:
  {
    "openclaw":
      {
        "emoji": "🦖",
        "requires":
          {
            "bins": ["mcporter"],
            "env": ["SERPZILLA_LOGIN", "SERPZILLA_API_TOKEN"],
          },
        "primaryEnv": "SERPZILLA_API_TOKEN",
      },
  }
---

# Serpzilla SEO Guest Posting

## Description

This skill is designed for SEO specialists and webmasters who want to improve their website's backlink profile.
It allows you to automate the search and purchase of guest posts (article placements on donor sites 
that pass link equity to your promoted resource) through OpenClaw. Interaction with the platform is done 
via the Serpzilla MCP server, managed by the `mcporter` tool.

## Prerequisites

The following components must be installed and configured on the server where OpenClaw runs:

1. **Docker** – to run the Serpzilla MCP server in an isolated container.
2. **Node.js and npm** – to install and run `mcporter`.
3. **OpenClaw** – the agent runtime environment.

Before using any Serpzilla commands, verify the MCP server is already registered with `npx mcporter list serpzilla`.

## Preliminary Setup

To fully use this skill, you need to register and configure the connection to the Serpzilla API.

### 1. Registration and API token

1. Register as an advertiser on [Serpzilla.com](https://serpzilla.com/).
2. Go to the security section at [https://passport.serpzilla.com/security/token/](https://passport.serpzilla.com/security/token/).
3. Copy your **API token** and remember your **login** (email) used for registration.

### 2. Install mcporter and add the Serpzilla MCP server

`mcporter` is a CLI tool for managing MCP servers. OpenClaw uses it to communicate with external services.

**Install mcporter globally:**
```bash
npm install -g mcporter
```

Add the Serpzilla MCP server:

It is necessary to request the user to provide values for the environment variables SERPZILLA_LOGIN
(the user's chosen login for registering with serpzilla.com, usually an email address)
and SERPZILLA_API_TOKEN (the API token received by the user).
Run the following command, replacing XXX and YYY with user's values:

```bash
npx mcporter config add serpzilla --stdio "docker run -i --rm --env SERPZILLA_LOGIN=XXX --env SERPZILLA_API_TOKEN=YYY stanislavusbest/serpzilla-mcp-stdio-server:v1.0.8"
```

### 3. Verify the configuration

Check that the MCP server was added successfully:

```bash
npx mcporter list serpzilla
```

## Using the skill

After completing the preliminary setup, the skill is ready to use. The typical workflow for purchasing
a guest post is described below.

The main entities in the Serpzilla domain for purchasing Guest Posts are:

- *Project* - a container for the entities listed below. To begin posting, you must create a project. A project is 
  created for a specific domain, but there are no restrictions on promoting other domains within the project.
- *URL* - the address of the page being promoted for SEO. Guest Post placements will be purchased to promote this 
  page. The URL is linked to the project.
- *Article* - the article to be posted on donor sites. It can be uploaded to the Serpzilla system for use when 
  purchasing placements. After uploading to Serpzilla, articles are reviewed by moderators. For this reason, Articles have statuses. Articles are linked to the project.
- *Text* - the anchor for the link being posted on the donor page/site. If the user uploads an Article, the Text and 
  URL for the promotion are determined automatically. Text is linked to the project.
- *Content* - a general entity for Article and Content. It also has its own system for transitioning between statuses.
- *Placement* - the Guest Post placement being purchased. Placement has a workflow that is reflected in the status 
  transition. Placement is linked to Text and URL.

Description of placement types:

| Format    | Type                              | Content Provided By          | Required Fields When Buying | Notes                                                                                                 |
|-----------|-----------------------------------|------------------------------|-----------------------------|-------------------------------------------------------------------------------------------------------|
| `news`    | Advertiser’s Article (Guest Post) | Advertiser (client)          | `article_id`, `url_id`      | `text_id` not required. The article is fully provided by the client.                                  |
| `review`  | Publisher’s Article (Guest Post)  | Publisher (webmaster)        | `url_id`, `text_id`         | The webmaster writes a review article. This placement is **more expensive**.                          |
| `link`    | In The News (Link Insertion)      | Publisher (webmaster)        | `url_id`, `text_id`         | The webmaster writes an article — not a review, but a link naturally embedded into a site news piece. |
| `archive` | In The Archive (Link Insertion)   | N/A (article already exists) | `url_id`, `text_id`         | Placement occurs in an already existing article on the site.                                          |


To get current user information including account balance:

```bash
npx mcporter call serpzilla.get_user_info
```

To top up user's balance, refer user to visit: https://passport.serpzilla.com/deposit/

### Step 1: Create a project for your promoted website

Create a project inside Serpzilla for your domain. Replace **YOUR_SITE.COM** with your actual website URL
(without `https://`):

```bash
npx mcporter call serpzilla.create_project domain=YOUR_SITE.COM
```

*Important:* Save the returned **PROJECT_ID** (ID field) – you will need it later.

When a project is created, Serpzilla automatically generates:

- One **URL** entity with the `domain` as the URL (e.g., https://YOUR_SITE.COM)
- One **Text** entity with the domain name as the default anchor

You can later add more URLs and Texts for specific landing pages and anchors.

To view all your existing projects:

```bash
npx mcporter call serpzilla.list_projects
```

### Step 2. Content preparation

You must upload an article **before** purchasing a placement. The article will be reviewed by Serpzilla moderators.
Only `approved` articles can be used for placements.

**Add an article:**

```bash
npx mcporter call serpzilla.add_article project_id=PROJECT_ID url='FULL_URL' title='ARTICLE_TITLE' \
meta_title="ARTICLE_META_TITLE" body='ARTICLE_BODY'
```

Parameters:

- `url` – the full promotion URL (including `https://`), e.g., https://yoursite.com/product
- `title` – internal title of the article (visible only in Serpzilla UI)
- `meta_title` – meta title used by the publisher when posting
- `body` – HTML content of the article, with your backlink(s) already inserted

**Article moderation:**

- After upload, the article status will be `pending`.
- Moderation usually takes 1–2 business days.
- If approved, status changes to `approved`; you can then use it in purchases.
- If rejected, check the reason and re-upload a corrected version.

Check article status:

```bash
npx mcporter call serpzilla.get_project_content_list project_id=PROJECT_ID
```

**For `review`, `link`, `archive` formats**

No article upload is needed. Serpzilla will use the `text_id` (anchor) and `url_id` (promoted page).
The webmaster writes the content according to the format.

### Step 3: Search for donor sites

With your **PROJECT_ID**, you can search for available donor sites that accept your desired placement type.

**Basic search command:**

```bash
npx mcporter call serpzilla.search_sites project_id=PROJECT_ID link_type=link
```

Valid link_type values: `news`, `review`, `link`, `archive`.

**See all available filters (language, price range, DR, etc.):**

```bash
npx mcporter list serpzilla --schema --json
```

**Get detailed information about a specific donor site:**

```bash
npx mcporter call serpzilla.get_site_info site_id=SITE_ID
```

This returns metrics (DR, traffic, language), status, price, placement examples, and more.

### Step 4. Buying Guest Posts

**IMPORTANT — User confirmation required before any purchase.**

Before executing a purchase, the agent MUST:

1. Call `get_user_info` to retrieve the current account balance.
2. Call `get_site_info site_id=SITE_ID` to retrieve the price for the selected donor site.
3. Present the following information to the user:
   - Site URL and price
   - Current account balance
   - Remaining balance after purchase (balance - price)
4. Ask the user for **explicit confirmation** to proceed with the purchase.
5. Only execute `purchase_placement` after receiving the user's confirmation.

If the user does not confirm, do NOT proceed with the purchase.

Once you have:
- `PROJECT_ID`
- `SITE_ID` (from search results)
- For `news`: `article_id` (approved) and `url_id`
- For `review`, `link`, `archive`: `url_id` and `text_id`

**Important:** The `search_history_id` parameter must always be set to an empty string `""` when buying.

#### Examples for each format:

**4.1 Purchase a `news` placement (Advertiser’s Article)**

```bash
npx mcporter call serpzilla.purchase_placement project_id=PROJECT_ID link_type=news \
  site_id=SITE_ID article_id=ARTICLE_ID url_id=URL_ID search_history_id=""
```

Optional: `is_content_need_approval=true` – if set, the placement will wait for your approval before the publisher starts.
Useful if you want to review the final context.

**4.2 Purchase a `review` placement (Publisher’s Article)**

```bash
npx mcporter call serpzilla.purchase_placement project_id=PROJECT_ID link_type=review \
  site_id=SITE_ID url_id=URL_ID text_id=TEXT_ID search_history_id=""
```

**4.3 Purchase a `link` placement (In The News – Link Insertion)**

```bash
npx mcporter call serpzilla.purchase_placement project_id=PROJECT_ID link_type=link \
  site_id=SITE_ID url_id=URL_ID text_id=TEXT_ID search_history_id=""
```

**4.4 Purchase an `archive` placement (In The Archive – Link Insertion)**

```bash
npx mcporter call serpzilla.purchase_placement project_id=PROJECT_ID link_type=archive \
  site_id=SITE_ID url_id=URL_ID text_id=TEXT_ID search_history_id=""
```
To view purchased placements use:

```bash
npx mcporter call serpzilla.get_project_placements project_id=PROJECT_ID
```

### Step 5. Managing Purchased Placements

**IMPORTANT — User confirmation required before any placement action.**

Many placement actions have financial implications:
- `approve_seo` / `approve_content_seo` — releases funds to the publisher
- `cancel_seo` / `cancel_from_*` — may trigger refunds or forfeiture
- `terminate_seo` — permanently removes an approved backlink
- `approve_from_arbitration_seo` — resolves a dispute in your favour

Before executing any `perform_placement_action`, the agent MUST:

1. Inform the user about the action being taken and its financial impact.
2. Ask the user for **explicit confirmation** to proceed.
3. Only execute the action after receiving the user's confirmation.

If the user does not confirm, do NOT proceed with the action.

After you purchase a placement, its lifecycle is managed through a set of statuses and transitions. 
You can perform specific actions to influence the placement's progress, request changes, cancel orders, 
or handle edge cases like billing or failed purchases.

All actions are executed using the MCP tool:

```bash
npx mcporter call serpzilla.perform_placement_action placement_ids=PLACEMENT_ID action=ACTION_NAME
```

The [table by link](references/placement_actions.md) lists every SEO‑available action. 
For each action we describe its purpose, the source status(es), the target status, and any relevant notes.


## Additional resources

* [Serpzilla API Documentation](https://serpzilla.com/api/)
