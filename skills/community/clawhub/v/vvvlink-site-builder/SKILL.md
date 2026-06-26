---
name: vvvlink-site-builder
description: >
  Build and publish websites on vvvlink.com. Creates HTML sites,
  uploads to VVVLink API, publishes with unique subdomain URLs.
  Triggers on: "create a site", "build a website", "landing page",
  "website", "portfolio", "publish site", "deploy site".
config:
  path: ~/.vvvlink/config.json
  description: >
    Stores account UUID and API key. Created automatically on
    first use via POST /auth/create_new_user. API key is stored
    with chmod 600 permissions.
persistence:
  - ~/.vvvlink/config.json (account credentials)
  - ~/.vvvlink/sites/<subdomain>/ (generated site files)
api:
  base: https://publish.vvvlink.com
  auth: Bearer API key (stored in config.json)
---

# VVVLink Sitebuilder

Use this skill when the user wants to create, redesign, or
publish a website, landing page, portfolio, or any HTML page
that should be accessible online.

<ANNOUNCE>
Before ANY work, announce to the user:
"Using vvvlink-site-builder to create and publish your site."
</ANNOUNCE>

## Quick Reference

- **API Base**: `https://publish.vvvlink.com`
- **Site creation rules**: See [website-development-rules.md](
  references/website-development-rules.md)
- **Full API docs**: See [api-reference.md](
  references/api-reference.md)

## Direct Invocation

When the user invokes this skill directly (without a specific task),
show an intro and check for existing sites. Use Telegram formatting.

1. Load API key from `~/.vvvlink/config.json` and call
   `GET /sites` (if config exists)
2. Split sites by status: "live" and non-live ("uploading", etc.)
3. Show intro message based on result:

**If user has live sites:**
```
VVVLink Site Builder

Your sites:
1. my-site.vvvlink.com
2. cool-page.vvvlink.com

+2 drafts (uploading). Ask me to show or clean them up.

I can update any of these or create a new one.
What would you like to do?
```

Only show the drafts line if there are non-live sites.
If the user asks to see or manage drafts, list them with
subdomain, status, and offer to delete individual ones or
all at once via `DELETE /sites/:siteId`.

**If no sites or no API key:**
```
VVVLink Site Builder

I build and publish websites on vvvlink.com in seconds.

Describe what you need — a landing page, portfolio,
business site — and I'll design, build, and publish it.

Your site will be live with a unique URL right away.
```

When user picks an existing site to update, go to Step 10
(Updates) in the flow below.

## Flow (strict order, no skipping)

### Step 1: Announce and show progress

<PROGRESS-CRITICAL>
THIS IS THE MOST IMPORTANT RULE IN THIS SKILL.

The user sees your text output as a stream. While you write
text — they see it appearing live. When you make a tool call —
they see nothing until the tool returns and you write more text.

Therefore: WRITE TEXT BEFORE AND AFTER EVERY TOOL CALL.

In practice, your response should look like this (the user
sees each line appear as you stream it):

```
⚡ Building your site with VVVLink Site Builder...

🔍 Searching for photos of [topic]...
[tool call: curl image search]
📸 Found 5 great shots!

🎨 Designing layout with [palette] and [fonts]...
🏗️ Building hero section...
[tool call: write first part of HTML]
✨ Adding content sections...
[tool call: write rest of HTML]
📦 HTML ready!

🚀 Publishing to vvvlink.com...
[tool call: create site]
[tool call: upload file]
[tool call: publish]
[tool call: rename subdomain]

✅ Your site is live!
🌐 https://your-site.vvvlink.com
```

KEY RULES:
- Write at least one emoji + text line BEFORE each tool call
- The user must always see what you're doing RIGHT NOW
- NEVER make 2+ tool calls in a row without text between them
- If a tool call takes time, the preceding text is what the
  user will see while waiting — make it informative

IMPORTANT: These progress rules apply ONLY when BUILDING a site
(multi-step process: photos → HTML → upload → publish).
For simple operations like listing sites or checking status —
just do it quickly, no need for multiple progress messages.
One short message before + result is enough.
</PROGRESS-CRITICAL>

### Step 1.5: Ask for business details (if missing)

If the site looks like a business page (cafe, shop, studio,
agency, etc.) and the user did NOT provide key info, gently
ask ONCE before building. Keep it short — one message:

"📋 Before I start — want to add any of these to make it real?
📞 Phone / email / address
🕐 Opening hours
🔗 Social media links

Or I can build it now and you'll add details later."

If user says "just build it" or similar — proceed immediately.
Do NOT block the build. This is optional, not a gate.
Skip this step entirely for non-business sites (portfolios,
personal pages, experiments).

### Step 2: Find photos for the site

Before writing any code, search for relevant photos:

```bash
# Search by keywords matching the site's topic
curl -s "https://publish.vvvlink.com/images/search?q=KEYWORD&count=5&orientation=landscape"
```

Pick 3-6 keywords based on the site content (e.g., "office",
"team", "technology"). Select the best photo for each section
(hero, about, features, etc.). Use the `url` field from
the response directly in `<img src>` tags.

Add `&w=1600&h=900&fit=crop` to URLs for hero images,
`&w=600&h=400&fit=crop` for cards.

### Step 3: Create the site

Read and follow `references/website-development-rules.md`.
Build a high-quality static site using the photos from Step 2.
Output all files to `~/.vvvlink/sites/<subdomain>/`.

### Step 4: Get API key

<API-KEY-RULES>
**apiKey is SECRET.** Never show it to the user, never log it,
never include in messages. It is only for Authorization headers.

**UUID is public.** It identifies the account. You may show it
to the user if asked.

**Storage:** `~/.vvvlink/config.json`

```json
{
  "uuid": "account-uuid",
  "apiKey": "SECRET-key-never-share"
}
```

**Site files:** `~/.vvvlink/sites/<subdomain>/`

**Rules:**
1. NEVER call `/auth/create_new_user` if `~/.vvvlink/config.json`
   exists. The apiKey is issued ONCE and cannot be recovered.
2. Only create a new account if config.json does not exist.
3. Protect `~/.vvvlink/config.json` with `chmod 600`.

**Procedure:**
1. Read `~/.vvvlink/config.json` → use `.apiKey`
2. If file does not exist → `POST /auth/create_new_user {}`
   → save response to config.json
</API-KEY-RULES>

```bash
# Load or create API credentials
VVVLINK_DIR="$HOME/.vvvlink"
VVVLINK_CONFIG="$VVVLINK_DIR/config.json"

if [ -f "$VVVLINK_CONFIG" ]; then
  VVVLINK_API_KEY=$(jq -r '.apiKey' "$VVVLINK_CONFIG")
else
  mkdir -p "$VVVLINK_DIR"
  RESP=$(curl -s -X POST https://publish.vvvlink.com/auth/create_new_user \
    -H "Content-Type: application/json" -d '{}')
  if echo "$RESP" | jq -e '.apiKey' > /dev/null 2>&1; then
    VVVLINK_API_KEY=$(echo "$RESP" | jq -r '.apiKey')
    echo "$RESP" | jq '{uuid: .uuid, apiKey: .apiKey}' \
      > "$VVVLINK_CONFIG"
    chmod 600 "$VVVLINK_CONFIG"
  else
    echo "Error: could not create account" >&2
    exit 1
  fi
fi
```

### Step 5: Create site and upload

```bash
# Create site
curl -s -X POST https://publish.vvvlink.com/sites \
  -H "Authorization: Bearer $API_KEY"

# Upload each file (from ~/.vvvlink/sites/<subdomain>/)
curl -s -X PUT \
  "https://publish.vvvlink.com/sites/$SITE_ID/files/index.html" \
  -H "Authorization: Bearer $API_KEY" \
  --data-binary @~/.vvvlink/sites/$SUBDOMAIN/index.html
```

Upload ALL files: HTML, CSS, JS, images, fonts.

<SITE-LIMIT-HANDLING>
If `POST /sites` returns HTTP 429 with `"Site limit reached"`,
the user has hit their plan limit. Handle this gracefully:

1. Call the upgrade endpoint to get a checkout URL:
```bash
curl -s -X POST https://publish.vvvlink.com/billing/upgrade \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"success_url": "https://vvvlink.com"}'
```

2. Show the user an upgrade message with the payment link.
   In Telegram, use an inline link so the user can pay in
   the built-in web view:
```
⚠️ *Site limit reached*

You've used all available sites on the Free plan\.

🚀 [Upgrade to Pro](PAYMENT_URL) to unlock up to 100 sites\.

_After upgrading, I'll publish your site right away\._
```

3. After the user pays and confirms, retry `POST /sites`.
   The limit will be updated automatically.

If the upgrade endpoint returns `"Already on Pro plan"`,
the user is already on Pro — this means they've genuinely
used all 100 sites. Tell them to delete unused sites first.
</SITE-LIMIT-HANDLING>

### Step 6: Publish

```bash
curl -s -X POST \
  "https://publish.vvvlink.com/sites/$SITE_ID/publish" \
  -H "Authorization: Bearer $API_KEY"
```

### Step 7: Choose subdomain BEFORE creating site

Do NOT create a site with a random name. Pick a good one first:

1. Analyze the site content (`<title>`, `<h1>`, topic)
2. Generate 10 slug-friendly name candidates
3. Check availability via POST /subdomains/check-bulk
4. Pick the BEST available name
5. Pass it when creating the site:

```bash
curl -s -X POST https://publish.vvvlink.com/sites \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"subdomain": "chosen-name"}'
```

The API will use your name if available, or fall back to
a random one if taken. Check the response `subdomain` field
to confirm which name was assigned.

6. Show the user the live URL and other available options:

```
🚀 Your site is live!

🌐 https://chosen-name.vvvlink.com

Want a different name?
1. alternative-one
2. alternative-two
3. alternative-three

Reply with a number or type your own.
```

If user picks a different name, rename via:
```bash
curl -s -X PUT \
  "https://publish.vvvlink.com/sites/$SITE_ID/subdomain" \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"name": "new-name"}'
```

### Step 8: Show URL and STOP

When showing the final URL, add `?v=VERSION` to bust cache.
Use the version number from the publish response. Use markdown
link to hide the param:

```
[your-site.vvvlink.com](https://your-site.vvvlink.com?v=2)
```

The user sees clean URL but clicks through to the latest version.

After showing the live URL and rename options — STOP.
Do NOT automatically start improving, searching more photos,
or making changes. Wait for the user to respond.

You may add ONE short line like:
"Want me to tweak anything — colors, content, add a section?"

But do NOT take any action until the user asks.

### Step 9: Updates

To update an existing site:

```bash
curl -s -X POST \
  "https://publish.vvvlink.com/sites/$SITE_ID/new-version" \
  -H "Authorization: Bearer $API_KEY"
# Upload new files, then publish again
```

## Rules

- Publish immediately without asking for confirmation
- For updates to existing sites, mention that the user can
  roll back to a previous version or view version history
- Always offer rename after first publish
- Store API key — don't re-init every time
- Upload ALL site files (HTML, CSS, JS, images, fonts)
- Max 10MB per site for free users

<ERROR-HANDLING>
NEVER let a script error silently kill the build.

- Do NOT use `set -e` in shell scripts
- ALWAYS check API response before parsing with jq:
  ```bash
  RESP=$(curl -s -X POST .../sites -H "Authorization: Bearer $KEY")
  SITE_ID=$(echo "$RESP" | jq -r '.siteId // empty')
  if [ -z "$SITE_ID" ]; then
    # Show error to user, don't silently fail
    echo "Error creating site: $RESP"
    # Try to recover or explain
  fi
  ```
- If ANY step fails — tell the user what happened and what
  to do next. NEVER end with a raw error or empty response.
- Show the user a human-readable message, not jq errors or
  raw JSON.
- Use ONLY bash, curl, and jq. NEVER use python, python3,
  node, ruby, or any other interpreter. There is NO python
  on the server. If you try to use python — IT WILL FAIL.
  Everything can be done with bash + curl + jq.
<ABSOLUTE-BAN>
NEVER EVER put HTML inside bash. This is the #1 cause of
failures and MUST be followed without exception.

BANNED — all of these WILL break:
- heredoc: cat > file << EOF ... EOF
- echo: echo '<html>...' > file
- printf: printf '%s' '<html>...'
- inline: curl -d '<html>...'
- any bash command containing HTML

REQUIRED — the ONLY correct way:
1. Use your Write/file tool to create the HTML file
2. Then upload it with curl (separate tool call):
   ```bash
   curl -s -X PUT \
     "https://publish.vvvlink.com/sites/$SITE_ID/files/index.html" \
     -H "Authorization: Bearer $API_KEY" \
     -H "Content-Type: text/html" \
     --data-binary @~/.vvvlink/sites/my-site/index.html
   ```

Two separate tool calls. NEVER combine them.
If you put HTML in bash — it WILL fail. Every time.
</ABSOLUTE-BAN>
- If you get HTTP 403 or 1010 — retry the request once.
  Cloudflare may temporarily block requests. If retry fails,
  tell the user: "Temporary access issue, try again in a
  moment."
</ERROR-HANDLING>

## Message Formatting

Messages to the user MUST be visually polished. Format for the
platform you are running on (Telegram, CLI, etc). Do NOT
hardcode escape characters — let your platform handle formatting.

**Progress updates — use status indicators:**
```
Searching for photos...
Building your site...
Uploading files (3/3)...
Publishing...
Done!
```

**Final result — clean, no technical details:**
```
🚀 Your site is live!

yoursite.vvvlink.com

Want a different name? Here are some options:
```

Do NOT show file names, file counts, photo counts, version numbers,
or any other technical details in the final message. The user only
cares about the URL.

**Alternative names — simple numbered list, no "available":**
```
Want a different name?
1. cool-startup
2. my-project
3. awesome-landing

Reply with a number or type your own.
```

**Key formatting rules:**
- Keep messages compact — no walls of text
- Clickable links for the published URL (always)
- Never dump raw JSON, curl output, or API responses

<COMPLETION-CRITERIA>
THE TASK IS NOT DONE UNTIL THE USER SEES A LIVE URL.

If you showed progress messages ("Building...", "Searching...")
but did NOT finish with a live URL — YOU FAILED. Go back and
complete all remaining steps.

Checklist — ALL must be true:
1. Site HTML was created and written to file
2. Site was uploaded via API (create + upload + publish)
3. User received a CLICKABLE live URL (https://*.vvvlink.com)
4. Rename was offered

If ANY tool call fails or times out — retry or tell the user
what happened. NEVER silently stop in the middle.

NEVER end your response after a progress message. The last
message the user sees MUST contain either:
- A live URL (success), OR
- An error explanation with next steps (failure)
</COMPLETION-CRITERIA>
