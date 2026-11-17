---
id: mcp-server
kind: asset
unlocks: [mcp-registry, mcp-directories, cursor-directory, claudemarketplaces, buildwithclaude, docker-mcp, gemini-cli-ext]
source: https://raw.githubusercontent.com/modelcontextprotocol/registry/main/docs/modelcontextprotocol-io/quickstart.mdx, https://raw.githubusercontent.com/modelcontextprotocol/registry/main/docs/reference/server-json/generic-server-json.md, https://raw.githubusercontent.com/modelcontextprotocol/registry/main/docs/modelcontextprotocol-io/authentication.mdx, https://vercel.com/docs/mcp/deploy-mcp-servers-to-vercel (inspector command) (loaded 2026-11-08)
---
## Smallest version
A stdio (or remote) MCP server whose tools are thin wrappers over the 2-5 API endpoints customers already call most, reading the user's key from an env var. No new backend logic. Published as an npm/PyPI package (or a remote URL) plus a `server.json` so the Official MCP Registry, and the aggregators that ingest it, can list it.

## Scaffold
- Server code: delegate (below); TypeScript or Python MCP SDK.
- Registry metadata: `brew install mcp-publisher` (Homebrew installs the current formula and cannot pin it: run `brew info mcp-publisher` first and compare with 1.8.9, the version checked 2026-11-12), then `mcp-publisher init` ("Create a server.json file template").

## Fields the listings check
- `server.json` `$schema`: `https://static.modelcontextprotocol.io/schemas/2025-12-11/server.schema.json`
- Top level: `name` (reverse-DNS, e.g. `io.github.<user>/<server>`), `description`, `title`, `websiteUrl`, `repository`, `version`, `packages`, `remotes`, `_meta`. Which are required is not stated on the reference page; check the schema file (unconfirmed).
- `packages[]`: `registryType`, `registryBaseUrl`, `identifier`, `version`, `transport`, `environmentVariables`, `packageArguments`, `runtimeArguments`, `runtimeHint`, `fileSha256`
- `remotes[]`: `type`, `url`, `headers`, `variables`
- Package ownership marker: npm `package.json` `"mcpName": "io.github.<user>/<server>"`; PyPI/NuGet: a line `mcp-name: <server-name>` (or HTML comment) in the package README.
- Namespace auth: `io.github.<user>/*` via GitHub login; `com.<domain>/*` via DNS TXT `v=MCPv1; k=ed25519; p=<PUBLIC_KEY>` at the domain apex, or HTTP.

## Steps
claude: pick the 2-5 endpoints from the API docs/OpenAPI and build the server (delegate) with the key read from an env var
claude: add `mcpName` to package.json (or `mcp-name:` to the PyPI README) matching the server.json `name`
claude: run `mcp-publisher init`, fill `description`, `version` (same as the package), `packages[]` with `transport` stdio and the API-key `environmentVariables`, or `remotes[]` for a hosted URL
claude: run `mcp-publisher validate`
approve: publish the package (npm publish / PyPI upload) at that exact version
human: `brew install mcp-publisher` (compare `brew info mcp-publisher` with 1.8.9 first); `mcp-publisher login github` (personal namespace only; org namespaces need a PAT with read:org as an org Owner, or GitHub Actions OIDC)
human: for a `com.<domain>/*` name instead: add the TXT record at the domain apex, then `mcp-publisher login dns --domain <domain> --private-key <YOUR_PRIVATE_KEY>`
approve: `mcp-publisher publish` (registry versions are immutable)
claude: `mcp-publisher status` to confirm the entry

## Delegate
Server code -> mcp-server-dev:build-mcp-server or anthropic-skills:mcp-builder. Tool tests -> mattpocock-skills:tdd.

## Verify locally
`npx @modelcontextprotocol/inspector@2.15.0` (connect to the server's start command or URL) lists tools and calls one against a test key; then `mcp-publisher validate` passes.
