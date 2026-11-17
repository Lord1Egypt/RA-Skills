---
name: snapwidget
description: Add social media feeds (Instagram, Facebook, TikTok, X, YouTube) and reviews (Google, G2, testimonials) to a website with SnapWidget. Use when the user wants an Instagram feed, social posts, a YouTube channel, Google or G2 reviews or testimonials on their website, or wants to change or install a SnapWidget widget.
---

# SnapWidget

SnapWidget makes a widget that shows the posts of social accounts, or reviews, on a website. It updates by itself when new posts or reviews come in. You make the widget, then put its code on the site.

## How to call SnapWidget

Use the first that works:

1. **The SnapWidget MCP tools** (`get_account`, `list_widgets`, `create_widget` and the others), when the SnapWidget MCP server (`https://snapwidget.com/mcp`) is connected. The steps below name the CLI command; the MCP tool has the name in brackets.
2. **The `snapwidget` CLI**, when you have no SnapWidget MCP server. Run `snapwidget --help`. When it is not installed: `npm install -g snapwidget` (Node.js 18 or later). Every command prints JSON. `snapwidget <command> --help` shows the options of a command.

## Steps

### 1. Sign in

**With the MCP tools:** run `get_account`. When the SnapWidget MCP server is there but is not signed in, ask the user to sign in to it. Do not install the CLI for this.

- **In Claude Code:** the user runs `/mcp`, picks **snapwidget** and signs in.
- **In a Claude app:** the user opens **Settings** > **Connectors** and clicks **Connect**.

The user enters their email address, then the code from the email, and clicks **Allow**. This also makes the account of a new user.

**With the CLI:** run `snapwidget account`. When it answers "Sign in first":

- **The user has a SnapWidget account:** run `snapwidget login`. It opens the browser. The user signs in and clicks **Allow**.
- **A new account:** ask the user for their email address. Run `snapwidget signup --email <address>`. Ask the user for the 6-digit code from the email, then run `snapwidget verify --email <address> --code <code>`.

The CLI keeps the sign-in. Never ask for a password. Never show, copy or save the token yourself.

### 2. Connect the source of the posts or reviews

Run `snapwidget accounts list` (`list_accounts`) first: the account can be there already.

- **YouTube:** `snapwidget accounts connect --service youtube --channel-url <channel link>` (`connect_account`). It is ready at once.
- **Instagram, Facebook, TikTok or X:** `snapwidget accounts connect --service instagram` (or `facebook`, `tiktok`, `x`) (`connect_account`). The answer has an approval link. Give it to the user: the owner of the social account opens it, signs in to the platform and clicks Allow. The platforms require this step; you cannot do it for them. Then run `snapwidget accounts list` again.
- **Google reviews:** `snapwidget reviews find-google "<business name> <city>" --country <2-letter country code>` (`find_google_business`), then `snapwidget reviews sources add --type google --name "<name>" --place-id <place_id>` with the name and place_id from that answer (`add_review_source`).
- **G2 reviews:** `snapwidget reviews sources add --type g2 --url <G2 product page>` (`add_review_source`).
- **Testimonials:** `snapwidget reviews sources add --type manual --name <name>` (`add_review_source`), then `snapwidget reviews add <source_id> --author-name <name> --body <text>` (`add_review`) for each testimonial.

### 3. Make the widget

- `snapwidget widgets types` (`list_widget_types`) lists the layouts and their settings.
- Social posts: `snapwidget widgets create --layout grid --accounts <account_id>` (`create_widget`). More accounts: `--accounts 12,34`.
- Reviews: `snapwidget widgets create --kind review --name "<name>" --layout wall --source-ids <source_id>` (`create_widget`).
- Change settings: `snapwidget widgets update <widget_id> --settings '{"<setting>": "<value>"}'` (`update_widget`). Send only what changes. When the answer has `"embed_code_changed": true` and the widget is already on a site, the site needs the new code: run `snapwidget embed <widget_id>` and replace the old code.

### 4. Put the widget on the site

Run `snapwidget embed <widget_id> --format <format>` (`get_embed_code` gives the HTML code).

- **React:** `--format react` gives a component. Save it, for example as `components/SnapWidget.jsx`, and render it where the widget goes.
- **Next.js:** `--format next`. Save it and render it in a page.
- **React or Next.js with only the MCP tools:** make the component from the HTML code. [references/frameworks.md](references/frameworks.md) shows how.
- **Plain HTML and server templates** (PHP, Laravel Blade, Rails, Django, Jinja, Liquid, Hugo, Jekyll, Eleventy): `--format html`. Paste the code where the widget goes.
- **Vue, Nuxt, Svelte, Astro:** read [references/frameworks.md](references/frameworks.md).
- **A website builder** (WordPress, Wix, Squarespace, Shopify, Webflow and many more): `--format html`, then follow the builder's guide. [references/index.md](references/index.md) lists them, for example [references/wordpress.md](references/wordpress.md). When you cannot edit the site, give the user the code and the steps.

### 5. Check it

Open the page and look for the widget. On a live site, `snapwidget widgets get <widget_id>` (`get_widget`) shows the install status after the widget's first view.

## Rules

- Connect only accounts and reviews of the user's own business, or of a client who agrees.
- Ask the user before you delete a widget, an account or a review source.
- An error is JSON with a message. A plan error has an upgrade link: give the link to the user. Never pay and never change the plan yourself. `snapwidget upgrade-link` (`get_upgrade_link`) gives a payment link for the user.
- Help for people: https://snapwidget.com/docs
