# Upload Images, Templates & Send via the SendPulse API

> Read this to upload images to the File Manager, save templates, and create/send campaigns over
> the REST API when MCP isn't used. Also covers image resize/convert tips. Docs:
> sendpulse.com/integrations/api (auth), .../bulk-email (templates & campaigns),
> .../file-manager (images). All requests are HTTPS to `https://api.sendpulse.com`.

## Table of Contents
1. Authentication (OAuth client credentials)
2. File Manager — upload images
3. Image resize & conversion tips
4. Templates — create/edit
5. Address books & campaigns — send
6. Recommended end-to-end flow

---

## 1. Authentication

SendPulse offers two methods. **Recommend the Single API Key — it is the preferred, simpler option.**

### A. Single API Key (preferred)

A **long-lived bearer token generated manually** in **Settings → API → API keys** (click *Generate*;
you can create up to 5 independent keys for different integrations). It stays valid until you revoke
it — no token-refresh logic, ideal for most integrations.

```
Authorization: Bearer <YOUR_API_KEY>
```

Just add that header to every request to `https://api.sendpulse.com`. That's it — no token call.
**Never hardcode or commit the key** — read it from env/config, and revoke it in the UI if leaked.

### B. OAuth client credentials (alternative)

Use only when you specifically need short-lived tokens. Get `client_id` / `client_secret` from
**Settings → API → Client credentials**, then:

```
POST https://api.sendpulse.com/oauth/access_token
Content-Type: application/json

{ "grant_type": "client_credentials", "client_id": "YOUR_ID", "client_secret": "YOUR_SECRET" }
```

Response: `access_token` (JWT bearer), `token_type: "Bearer"`, `expires_in: 3600` (1 hour).
Use it the same way (`Authorization: Bearer <access_token>`) but you must request a new token after
each expiry (cache it ~1h) and implement refresh logic — which is why the Single API Key is simpler.

## 2. File Manager — upload assets (verified endpoint)

> ⚠️ **Two important, field-verified facts:**
> 1. The working File Manager endpoint is on **`https://api.sendpulse.com/fm/public/v1`** (the same
>    host + Bearer token as the rest of the API). The `login.sendpulse.com/api/file-manager-service`
>    path does **not** work for API uploads.
> 2. **File Manager is NOT the store for email `<img>` images.** Generic-FM files (used for CRM
>    products, chatbots, pop-ups, sites) do **not** resolve to a public image URL — fetching them on
>    the account's public domain returns SendPulse's "technical domain" stub page, and the
>    authenticated FM endpoint can't be used in an email. **Email images are served from the email
>    editor's `userfiles` store** (`https://s<ACCOUNT_ID>.sendpul.se/files/emailservice/userfiles/<hash>/…`),
>    populated by the email editor's image picker. See §2b for what to actually do for email images.

**File Manager API (for CRM/store/chatbot assets), base `https://api.sendpulse.com/fm/public/v1`:**
- **Upload:** `POST /file` — multipart fields: `content[]` (binary file; repeatable) and
  `pathToStore` (an **existing** directory, no leading slash, e.g. `jewelry` or `test/skyeng`).
  Returns an array of `{path, name, stream, thumb, extension, size, date}`. The target directory
  must already exist — upload does **not** auto-create it.
- **Create directory:** `POST /directory` — multipart fields `pathToStore` (existing parent) +
  `name`. Root-level creation is unreliable; create under an existing folder (e.g. parent `test`,
  name `skyeng` → `/test/skyeng/`).
- **List:** `GET /directory//<path>` (note the double slash) — items with `path`, `name`,
  `isFolder`, `size`, `stream`, `thumb`.
- **Delete:** `DELETE /file` — JSON `{ "path": "/dir/file.ext" }`.

### 2a-bis. Easiest manual path WITH images — upload a ZIP (no API, verified working)

If the user isn't using the API/MCP and just wants images bundled with the template, SendPulse's
**New template → Upload a file** accepts a `.zip` (also `.rar`, `.7z`, or a lone `.html`), up to 5MB:

- Put the **HTML file + all image files in the archive ROOT** — no subfolders.
- In the HTML, reference images by **bare filename** (`src="hero.jpg"`), not a path or URL.
- On upload, tick **"Upload images to the server SendPulse"** — SendPulse hosts the images in your
  account and rewrites each relative `src` to a permanent SendPulse URL automatically.
- Remote URLs (a CDN, `placehold.co`, an existing File Manager URL) are left untouched, so archived
  and remote images can coexist in the same template.

This avoids needing the File Manager API or the public-URL format below — the simplest option for
non-technical users who have local images. (Tested: HTML + 5 JPEGs in a flat zip → all images loaded.)

### 2b. Building the public URL for EMAIL images (verified working)

FM files **are** servable for email — but only via the email-service `userfiles` path, not by the
bare FM path. The public URL pattern is:

```
https://s<ACCOUNT_ID>.sendpul.se/files/emailservice/userfiles/<USERFILES_HASH>/<FM_PATH>
```

- `<ACCOUNT_ID>` — your numeric account id (from `GET /user/info` → `id`).
- `<USERFILES_HASH>` — a per-account hash that **ends with your account id** (e.g.
  `9ff1097dc04ccfbdd451a7ff24ae5ff0` + `7824090`). Get it once: in the SendPulse email editor insert
  any image, then copy the generated `src` — it contains this hash. It's stable per account; store
  it in `brand-profile.md` for reuse.
- `<FM_PATH>` — the File Manager path returned by the upload, **without the leading slash**
  (e.g. `jewelry/en-01.jpg`, `test/skyeng/skyeng-logo.png`).

**Full verified flow for email images:**
1. `POST /fm/public/v1/file` to upload (create the dir first if needed — §2).
2. Take the returned `path` (e.g. `/jewelry/logo.png`), drop the leading slash.
3. Compose: `https://s<id>.sendpul.se/files/emailservice/userfiles/<hash>/jewelry/logo.png`.
4. Use that URL in the template's `<img src>`. (Verified: returns `200 image/*` and renders.)

Alternatively, you can host images on **any public HTTPS URL** (your own CDN, S3, etc.) — email
`<img>` accepts any public URL, it doesn't have to be on SendPulse. During drafting, `placehold.co`
URLs are public and render fine; swap them for real URLs before the real send.

> The bare FM path on the account domain (e.g. `s<id>.sendpul.se/jewelry/en-01.jpg`) returns the
> "technical domain" stub — you MUST include the `/files/emailservice/userfiles/<hash>/` prefix.

## 3. Image resize & conversion tips

Prepare images before upload for fast, crisp, lightweight emails:
- **Width:** export hero/content images at **2× the display width** for retina (e.g. a 600px-wide
  hero → 1200px source), then set the `width`/`height` attributes to the display size in HTML.
- **Max display width 600px** (template width); product cards ~280px, feature icons ≤80px.
- **Format:** JPEG for photos, PNG for logos/transparency/flat graphics, **GIF** for simple
  animation. Avoid WebP/AVIF — inconsistent email-client support (see dark-mode-accessibility.md).
- **Compress:** target < ~200KB per image; keep total email weight reasonable (Gmail clips > 102KB
  of HTML, separate from images, but heavy emails still hurt load & deliverability).
- **Always set `width` and `height`** attributes so layout doesn't jump before images load.
- **Alt text** on every image (accessibility + shown when images are blocked).
- **Dark mode:** pad transparent PNG logos with a safe background so they don't vanish on dark.
- Tools: any image editor / CLI (e.g. ImageMagick `convert in.png -resize 1200x out.jpg`) — do the
  resize/convert locally, then upload the optimized file via §2.

## 4. Templates — create/edit

The bulk-email API stores the **HTML Base64-encoded**:
- **Create:** `POST https://api.sendpulse.com/template` — `body` (Base64 HTML, required),
  `name` (optional), `lang` (optional). Returns the new template `id`.
- **Edit:** `POST https://api.sendpulse.com/template/edit/{id}` — `body` (Base64 HTML), `id`.
- **List:** `GET https://api.sendpulse.com/templates?owner=me`
- **Get one:** `GET https://api.sendpulse.com/template/{id}`

Base64-encode the fragment before sending, e.g.:
```bash
B64=$(base64 -w0 template.html)   # then POST {"body":"'$B64'","name":"Spring Sale"}
```

## 5. Address books & campaigns — send

- **Create list:** `POST https://api.sendpulse.com/addressbooks` — `bookName`.
- **Get lists:** `GET https://api.sendpulse.com/addressbooks` (`limit`, `offset`).
- **Add emails:** `POST https://api.sendpulse.com/addressbooks/{id}/emails` — `emails` array
  (with `variables` for personalization), optional `tags`.
- **Create campaign:** `POST https://api.sendpulse.com/campaigns` — `sender_name`, `sender_email`
  (must be a verified sender), `subject`, `body` (Base64 HTML) **or** `template_id`, `list_id`.
  Optional `send_date` (schedule), `segment_id`, `attachments`.
- **Campaign info/list:** `GET /campaigns/{id}`, `GET /campaigns` (`status`, `planed`, `limit`).

> **Sending is outward-facing and hard to reverse.** Confirm sender, subject, and recipient list
> with the user before calling `POST /campaigns` without a future `send_date`. Enable open/click
> tracking and add UTM (see variables-analytics.md) before sending.

## 6. Recommended end-to-end flow

1. Auth → get token (§1).
2. Upload images to File Manager → collect URLs (§2–3).
3. Generate the HTML fragment with those real URLs + variables + UTM.
4. Base64-encode → create template (§4) — or upload via MCP ([sendpulse-mcp.md](sendpulse-mcp.md)).
5. Ensure the address book exists / contacts added (§5).
6. Create the campaign with `template_id`; schedule or confirm-then-send (§5).
7. After send, review analytics; iterate with an A/B test (variables-analytics.md).
