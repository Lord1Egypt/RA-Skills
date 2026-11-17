---
id: linear
kind: platform
unlocks: [linear]
source: https://linear.app/docs/integration-directory, https://linear.app/developers/oauth-2-0-authentication (loaded 2026-11-08)
---
## Smallest version
A Linear OAuth app that does one job for the product's users: e.g. create a Linear issue (with a link back) from an item in the product, or post a comment when something happens in the product. Plus a docs page on the product's docs site explaining how to connect. Linear "generally doesn't accept scripts or low-effort or hobbyist apps", so it must be a real in-product flow.

## Scaffold
Create the app at https://linear.app/settings/api/applications/new in a separate workspace owned by the company (Linear recommends this so all admins get access). No code template on the pages loaded; Linear GraphQL API over HTTPS.

## Fields the listings check
- OAuth: authorize `GET https://linear.app/oauth/authorize`, token `POST https://api.linear.app/oauth/token`; callback URLs configured on the app; `scope` comma-separated: `read` (always), `write`, `issues:create`, `comments:create`, `admin` (avoid), `timeSchedule:write`; `actor=app` creates resources as the application; PKCE supported (`code_challenge`, `code_challenge_method` `plain`|`S256`). Other app form fields (name, developer URL, webhooks, public toggle) not described on the page (unconfirmed).
- Directory submission: Google Form (https://docs.google.com/forms/d/e/1FAIpQLSdYKtml_JsVv-sXuP4_eiT-l-8K6IaoEQrxdAP_7w-mb1-hSQ/viewform) with a sample page for copy style/length.
- Assets: color icon 320x320 (.svg, .jpeg or .png); monochrome (white) icon 320x320; 1-3 showcase images 1600x1000; Figma template https://www.figma.com/community/file/1111754695287344546. Send to integrations@linear.app or link in the form.
- A docs page for connecting is not an explicit requirement on the page (catalog asks for it; unconfirmed).

## Steps
claude: implement connect (authorize with the narrowest scope, e.g. `issues:create`, PKCE S256) and callback (token exchange, store per workspace)
claude: implement the one action via the GraphQL API (e.g. `issueCreate`; mutation name unconfirmed on the pages loaded) and a disconnect
claude: write the docs page "Connect Linear" with the install link and screenshots
human: create the separate workspace and the OAuth app; register callback URLs; store client secret
approve: deploy the integration and docs page
human: make the icons and showcase images from the Figma template
claude: draft the form answers in the sample page's style
human: submit the form and email assets to integrations@linear.app

## Verify locally
Local run with a dev callback URL registered: connect a test Linear workspace and confirm the issue/comment appears.
