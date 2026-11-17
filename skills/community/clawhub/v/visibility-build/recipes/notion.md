---
id: notion
kind: platform
unlocks: [notion]
source: https://developers.notion.com/guides/connections-and-tokens/public-integrations/overview, https://developers.notion.com/guides/connections-and-tokens/public-integrations/marketplace-listing, https://developers.notion.com/guides/get-started/authorization (loaded 2026-11-08)
---
## Smallest version
A public Notion connection whose one job is to write the product's existing data into a Notion database the user picks (e.g. sync new records/reports as pages), triggered from a "Connect Notion" button in the product. OAuth on the product's server; no Notion UI beyond the standard consent screen.

## Scaffold
Developer portal -> Build -> Connections -> Create new connection. No code template on the pages loaded; use the Notion JavaScript SDK or plain HTTPS.

## Fields the listings check
- Connection: name, development workspace, Redirect URI(s), installation scope **Any workspace** (only these can be listed; "cannot be changed later" is from a search summary of the docs, unconfirmed), capabilities (read / update / insert content). Client ID + secret on the Configuration tab.
- OAuth: authorize `https://api.notion.com/v1/oauth/authorize` with `owner=user`, `response_type=code`, `client_id`, `redirect_uri`; token `POST https://api.notion.com/v1/oauth/token` with HTTP Basic `CLIENT_ID:CLIENT_SECRET`, JSON `grant_type: "authorization_code"`, `code`, `redirect_uri` (when required). Response: `access_token`, `refresh_token`, `bot_id`, `workspace_id`.
- API header: `Notion-Version: 2026-03-11` on every request (unless using the JS SDK).
- Marketplace listing (Listings > Connections > Drafts): listing name and description, category and tags, listing images and logo, associated public connection. Image sizes, privacy policy/terms/support fields not stated (unconfirmed). Review: "The Notion team reviews every listing submission", 5-10 business days by email.

## Steps
claude: pick the one data flow; implement `/notion/connect` (redirect to authorize URL) and `/notion/callback` (token exchange, store tokens per user, encrypted)
claude: implement the write: search/select the target database the user shared, create pages via the API with `Notion-Version: 2026-03-11`; refresh tokens on 401
human: create the public connection (Any workspace, redirect URIs, minimal capabilities); put client ID/secret in the product's secrets
approve: deploy the Connect button and callback
human: install it in a second test workspace end to end; capture screenshots
claude: draft listing name, one-line and long description, category/tags
human: Listings > Connections: create draft with logo and images, associate the connection, Submit

## Delegate
OAuth callback + sync tests -> mattpocock-skills:tdd.

## Verify locally
Run the product locally with a dev redirect URI registered, click Connect, finish consent in a test workspace, and confirm a page appears in the chosen database.
