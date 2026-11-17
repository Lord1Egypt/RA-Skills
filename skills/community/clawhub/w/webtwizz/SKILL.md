---
name: webtwizz
description: "Build, change and publish websites and web apps with WebTwizz through its MCP server. Use when the user wants a website, landing page, online store, booking site, portfolio or web app built or changed, wants a site published or put on their own domain, or asks about their WebTwizz sites, data, versions or credits."
last-updated: 2026-11-08
---

# WebTwizz

[WebTwizz](https://webtwizz.com) builds real websites and web apps from a description, hosts them and publishes them. Sites can have sign-ins, a database and file uploads built in, or use accounts the user already has, like Stripe and Supabase. Everything is saved in the user's WebTwizz account, so they can open any site in the WebTwizz editor and keep going.

The tools in this skill come from the WebTwizz MCP server at `https://app.webtwizz.com/mcp`.

## Connect first

If tools like `create-site` and `list-sites` aren't available, the server isn't connected yet. Tell the user how to connect it in their app:

- **Claude Code:** `claude mcp add --transport http webtwizz https://app.webtwizz.com/mcp`, then type `/mcp`, choose webtwizz and sign in.
- **Codex:** `codex mcp add webtwizz --url https://app.webtwizz.com/mcp`, then `codex mcp login webtwizz`.
- **Cursor:** add `{"mcpServers": {"webtwizz": {"url": "https://app.webtwizz.com/mcp"}}}` to `~/.cursor/mcp.json`, then click Login next to WebTwizz.
- **Any other MCP client:** add `https://app.webtwizz.com/mcp` as a remote HTTP server and choose OAuth if it asks how to sign in.

Signing in opens a browser. A free WebTwizz account is enough to start: the user can [sign up here](https://app.webtwizz.com/register) or during the sign-in. The account needs a verified email address before WebTwizz can build or change anything.

## How the work runs

- `create-site` and `edit-site` start the work and return at once. A build takes from a few seconds to several minutes.
- The work is done only when a result says **Finished**. Until then, check on it with `get-site`, waiting a little between checks. Don't tell the user it's done and don't describe the result before that.
- One change runs on a site at a time. If WebTwizz says the site is busy, wait for the running change to finish.
- When WebTwizz asks a question, ask the user and pass their answer with `edit-site`.
- When WebTwizz waits for an OK, for example to run a command, delete database records or change something in Stripe, ask the user plainly and pass their answer to `confirm-action`. Never approve it yourself.
- `stop-build` stops a running build. The work done so far is kept.

## Building a site

- Write the brief for `create-site` from the conversation: what the business or project is, who it's for, the pages and sections, features like a contact form, bookings, a store or sign-ins, and anything the user said about tone, colours or style.
- WebTwizz finds licensed photos itself, so describe the photos the site needs instead of looking for them. Pass the user's own logo, pictures or documents as images or files.
- To start from a ready-made design, use `list-templates`, look closer with `show-template`, then pass the template's slug to `create-site`.
- Every `site_id` also takes the site's name, so when the user names a site there's no need to list sites first. `list-sites` shows their sites when they don't.

## Changing a site and checking it

- Describe the change for `edit-site` the way the user asked for it, including the page and section when they said.
- `screenshot-site` lets you see a page, and `show-preview` gives the preview link. Look at the site before telling the user what changed.
- `list-versions` and `restore-version` undo changes. The version being replaced stays in the history.
- `duplicate-site` makes an unpublished copy to try ideas on.

## Publishing

- `publish-site` never publishes on its own. The user confirms with the Publish button in the WebTwizz card.
- Apps that can't show the WebTwizz card, like terminals and code editors, have no Publish button of their own. There, `publish-site` returns a link that opens Publish in the WebTwizz editor. Give the user that link and tell them to press **Publish**. Don't say the site is live until they have.
- `unpublish-site` takes a site offline, and it stays in WebTwizz as a draft.
- `set-site-address` changes the site's webtwizz.app address.
- `connect-domain` adds a domain the user owns and returns the DNS records to set where they bought it. `check-domain` then confirms it.
- `update-site` renames a site or sets who can see it: anyone, people with a password, or only the user's workspace.

## Data, services and code

- `list-site-data` and `get-site-data` read the records in a site's database. `add-site-data`, `update-site-data` and `delete-site-data` change them directly, with no build. Ask before deleting.
- `list-connectors` shows the services the user has connected, like Stripe, Supabase, Google Analytics or GitHub. `use-connector` gives a site one of them, and `get-connector-overview` says how it's doing, like visitors or sales.
- `get-github-status`, `push-to-github` and `pull-from-github` sync a site with its GitHub repository.
- `download-code` returns a zip link that works for 30 minutes.
- `list-env-variables` and `set-env-variable` handle a site's settings. Secret keys are never typed into the chat: `set-env-variable` returns the WebTwizz page where the user pastes them.

## Account and credits

- `get-account` shows the connected account, its plan and the credits left.
- Builds and edits use WebTwizz credits, the same as in the editor. Data, domain and preview tools don't. When credits run out, WebTwizz says so and nothing changes. [Pricing](https://webtwizz.com/pricing) explains plans and credits.
- Custom domains, private sites, GitHub and downloading the code are on paid plans.
- `search-help` answers how-to questions from the [WebTwizz docs](https://docs.webtwizz.com).
