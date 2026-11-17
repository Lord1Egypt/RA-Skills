# OAuth and MCP

OAuth requires the accompanying Teleskopiq server release. A 404 at `/api/oauth/device` means that
deployment does not have OAuth; updating or republishing the skill alone cannot enable it.

## Skill login

Run `scripts/teleskopiq.py login --no-browser` using the skill's virtual environment. Give the user the
displayed verification link and code, and keep the process alive while they approve the connection.
The browser page supports sign-in and account creation. Users without a completed channel go through the full
onboarding flow (YouTube or manual setup, style review, photo, and schedule), then return to consent.
The CLI keeps waiting for up to one hour. Access is issued only after setup and explicit approval.
`--scope 'scripts:read channel:read'` requests read-only access when that is sufficient for their task.

The CLI uses the device authorization grant. Access tokens expire after 15 minutes; refresh tokens rotate
and expire after 30 days without renewal. Connections require fresh approval after 90 days.
The private token file is `~/.config/teleskopiq/oauth.json`; `TELESKOPIQ_OAUTH_FILE` overrides it.
Tokens are bound to the exact GraphQL endpoint and selected channel. Local refresh operations are locked
to avoid concurrent token reuse. If refresh is interrupted, run login again; do not retry old refresh tokens.
`auth-status` only reports local cache metadata. Run a read command to verify server access.
`logout` revokes OAuth access and removes its saved credentials; existing API keys remain separately managed.

## MCP connection

Once the server is deployed, add **https://teleskopiq.com/api/mcp** as a remote Streamable HTTP MCP server
in the user's AI app and choose OAuth authentication. The app discovers Teleskopiq's authorization server,
registers a public client, and uses authorization code with S256 PKCE. The user signs in and approves
a channel and permissions in their browser. Do not paste a GraphQL access token into MCP: the audiences differ.

Tools cover channel/style reads, script listing/search/creation/editing/deletion, comments, history/version
restoration, scheduling, metadata, thumbnail generation/references, topic ideas, and resumable AI conversations.
Only tools allowed by the connection's scopes are listed. Inputs use the same GraphQL variable shapes as
[api.md](api.md). `teleskopiq_channel` automatically uses the connected channel.

Read script/history before modifying existing content. Save a version before replacing content with `update`.
For explicit scheduling, use `update` with `scheduledFor` at noon UTC on the chosen publishing day.
Select a thumbnail using `update` with `input.thumbnails.selectedUrl` as described in `api.md`.
Generation calls can take several minutes; configure the client timeout accordingly. If an AI question is
returned, ask the user and resume `chat` with the same script ID and the returned call ID in `tool`.
After interrupted mutations, inspect existing records before retrying.

Revoke either type of connection at **Teleskopiq → Settings → Connected apps**.

Browser-based MCP clients sending an `Origin` header need their origin added to the server's
`NUXT_MCP_ALLOWED_ORIGINS` allowlist. Native clients generally omit this header. Deployment details are in
the repository's `docs/oauth-mcp.md`.
