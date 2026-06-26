# App Authoring

Use this reference when the user is working on a source-based Graft app built with `createApp(...)`.

## Current patterns

- Start with `createApp({ name, version, description, ... })`.
- For small examples and README snippets, register tools inline with `app.tool('name', config)`.
- For modular apps and scaffolded projects, define tools in separate modules with `defineTool('name', config)` and register them with `app.tool(definedTool)`.
- Resources and prompts are still registered with object configs through `app.resource(...)`, `app.resourceTemplate(...)`, and `app.prompt(...)`.
- Use `app.route(...)` for plain HTTP-only routes and `app.webhook(...)` for HTTP-only routes that should still go through the tool pipeline.
- When demonstrating a tool, show both surfaces: the MCP `tools/call` invocation and the equivalent HTTP request.

## Tool design defaults

- Use stable, explicit names such as `orders_create` or `inventory_get_stock`.
- Write descriptions that say what the tool does, when to use it, and what it returns or changes.
- Keep input schemas simple and explicit; include examples for non-trivial tools.
- Mark mutations with `sideEffects: true`.
- Use `expose: 'both'`, `'mcp'`, or `'http'` intentionally.
- Use current auth shapes only:
  - `true`
  - `['admin']`
  - `{ roles: ['admin'] }`

## Demonstrating the dual surface

When writing docs, examples, or explaining Graft to users:

- Show the same tool accessed via MCP and HTTP side-by-side. For example:
  - MCP: `POST /mcp` with `{ "method": "tools/call", "params": { "name": "list_items", "arguments": { "q": "hello" } } }`
  - HTTP: `GET /list-items?q=hello`
- Highlight that both go through the same pipeline: authenticate → check roles → validate params → middleware → handler.
- For mutations (`sideEffects: true`), note that the HTTP method changes from GET to POST.
- For `expose: 'mcp'` or `expose: 'http'` tools, explain what is visible on each surface.
- Mention that the server auto-serves discovery and docs endpoints (`agent.json`, `mcp.json`, `openapi.json`, `/docs`, `llms.txt`, `llms-full.txt`, `/health`) when relevant to the user's task.

## Runtime and delivery surfaces

- `app.build()` returns `{ mcp, fetch }`.
- `app.toFetch()` is the cleanest integration for Bun, Deno, and worker-style runtimes.
- `app.toNodeHandler()`, `app.node()`, and `app.serve()` cover Node integration and standalone serving.
- When writing docs for end users, prefer the simplest surface that matches the target runtime.

## Documentation defaults

- Prefer one inline example plus one modular example instead of listing every registration overload.
- If the repo ships scaffolds, align docs with the scaffolded structure unless there is a strong reason not to.
- Keep MCP examples in actual JSON-RPC shape when showing request payloads.
- Always mention auto-served discovery and docs endpoints when documenting deployment or server startup.
- Reference the complete CLI command set: `serve`, `dev`, `check`, `test`, `studio`, `install`, `add-tool`.
- When documenting testing, show the `examples` property on tools and `graft test -e src/app.ts` as the smoke-test workflow.
