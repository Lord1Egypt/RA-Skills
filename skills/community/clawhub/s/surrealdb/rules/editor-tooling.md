# SurrealQL Editor Tooling

> **v1.7.0 status note:** this rule was shrunk in v1.4.1 after the v1.4.0
> editor section was caught documenting a `surrealql.toml` schema, a
> `lint --format github` CI subcommand, a `--socket` flag, and a VS Code
> command palette that did not exist upstream. v1.6.6 keeps per-editor
> detail grounded in the actual upstream source for each extension at a
> pinned tag (`surrealdb/surrealql-language-server v0.1.3`,
> `surrealdb/surrealql-vsx v0.3.0`, `surrealdb/surrealql-zed v0.1.0`,
> `surrealdb/surrealql-jetbrains` head, `surrealdb/surrealql-tree-sitter`
> head). v1.6.6 also adds the official CodeMirror packages
> (`@surrealdb/codemirror`, `@surrealdb/lezer` v1.0.5). Anything in this file
> is from inspected source; anything beyond it is out-of-scope until a future
> verify pass.

This rule covers the editor-side toolchain for SurrealQL: the language
server, the tree-sitter grammar, and the per-editor extensions. Pair
this with `rules/surrealmcp.md` for the agent-facing layer -- LSP serves
human authoring; MCP serves agent execution.

---

## Canonical Components (verified 2026-06-17)

| Component | Verified release | Notes |
|---|---|---|
| `surrealql-language-server` | **v0.1.6** (crates.io) | First-party LSP baseline |
| `@surrealdb/codemirror` / `@surrealdb/lezer` | **v1.0.6** (npm) | Async DEFINE EVENT support in v1.0.6 |
| SurrealQL VS Code extension (`surrealql-vsx`) | **v0.4.2** | Marketplace + OpenVSX |
| SurrealQL JetBrains plugin | **v0.2.3** | JetBrains Marketplace |
| `surql-lsp` (community) | v0.1.1 | Separate community crate — not first-party |

| Component | Repo | Pinned tag | Wire name on disk |
|-----------|------|------------|-------------------|
| Language server | `surrealdb/surrealql-language-server` | `v0.1.6` (2026-05-28) | `surrealql-language-server` (Cargo `[package].name`; no `[[bin]]` override) |
| Tree-sitter grammar | `surrealdb/surrealql-tree-sitter` | head (sibling checkout required by the LSP build) | -- |
| VS Code grammar+snippets | `surrealdb/surrealql-vsx` | `v0.4.2` (2026-06-09) | `surrealdb.surrealql` (Marketplace publisher.name) |
| JetBrains plugin | `surrealdb/surrealql-jetbrains` | `v0.2.3` (2026-06-09) | `com.surrealdb.surql-jetbrains` (Marketplace id `31397`) |
| Zed extension | `surrealdb/surrealql-zed` | `v0.1.0` | `surrealdb-surrealql` (Zed extension id) |
| CodeMirror package | `surrealdb/codemirror` | `v1.0.6` (2026-05-19) | `@surrealdb/codemirror`, `@surrealdb/lezer` |

There is also an older crate `surql-lsp` on crates.io. **The canonical
LSP for first-party extensions is `surrealql-language-server`** -- the
Zed and JetBrains extensions both shell out to that binary by name.
Treat `surql-lsp` as a separate community LSP and do not mix the two in
one editor wiring.

---

## Language Server: `surrealql-language-server` v0.1.6

v0.1.6 continues the v0.1.3 migration to `tower-lsp-server` with parser and
diagnostic improvements. It depends on a pinned `surrealdb` crate for parsing;
check the tag's `Cargo.toml` for the exact server version when debugging
syntax mismatches.

### Communication + invocation

The server speaks LSP over **stdio only**. `src/main.rs` constructs
`tokio::io::stdin()` / `stdout()`, hands them to `tower-lsp`, and serves;
there is no `--socket`, `--port`, `--http`, `--stdio`, `lint`, or
subcommand of any kind. Editors launch the binary with no arguments:

```bash
surrealql-language-server
```

If you want `--socket`/`--lint`/CI integration, treat it as not-yet-shipped.

### Server capabilities (reported on `initialize`)

From `src/backend.rs`:

| LSP capability | Provided |
|----------------|----------|
| `completionProvider` | yes (no `resolveProvider`) |
| `hoverProvider` | yes |
| `definitionProvider` | yes |
| `referencesProvider` | yes |
| `renameProvider` | yes (with `prepareProvider`) |
| `signatureHelpProvider` | yes |
| `codeActionProvider` | yes |
| `documentHighlightProvider` | yes |
| `callHierarchyProvider` | yes |
| `documentSymbolProvider` | yes |
| `workspaceSymbolProvider` | yes |
| `executeCommandProvider` | **no** |

Because `executeCommandProvider` is not advertised, there are **no
LSP-exposed commands** for "Run Selection", "Open Schema Browser",
"Connect", etc. Any such command in an editor extension is the
extension's own contribution, not the LSP's.

### Workspace settings (`surrealql.*`)

The server reads its config from `initializationOptions` first and from
`workspace/configuration` second, deserialised by `src/config.rs`.
Camel-case is canonical; snake-case aliases are accepted on a few
fields. The full schema:

```jsonc
{
  "surrealql": {
    "connection": {
      "endpoint": "ws://127.0.0.1:8000/rpc",  // or http://, file:, mem:
      "namespace": "myns",
      "database": "mydb",
      "username": "root",
      "password": "root",
      "token":    "<jwt>",
      "access":   "<access-method-name>"
    },
    "metadata": {
      "mode":               "workspace+db",   // default
      "enableLiveMetadata": true,             // default
      "refreshOnSave":      true              // default
    },
    "analysis": {
      "enablePermissionAnalysis":         true,  // default
      "enableAggressiveSchemaInference":  true,  // default
      "enableCodeActions":                true   // default
    },
    "authContexts": [
      {
        "name":       "viewer",
        "roles":      ["viewer"],
        "authRecord": null,
        "claims":     {},
        "session":    {},
        "variables":  {}
      }
    ],
    "activeAuthContext": "viewer"  // must match an entry in authContexts
  }
}
```

Defaults if no settings are sent: a single `"viewer"` auth context is
synthesised, all `analysis.*` and `metadata.enableLiveMetadata` /
`metadata.refreshOnSave` flags are `true`, and `metadata.mode` is
`"workspace+db"`.

### Environment-variable fallback

If a `connection.*` field is unset, the server falls back to these env
vars (defined in `ServerSettings::merge_with_env`):

| Setting | Env var |
|---------|---------|
| `connection.endpoint` | `SURREALDB_ENDPOINT` |
| `connection.namespace` | `SURREALDB_NAMESPACE` |
| `connection.database` | `SURREALDB_DATABASE` |
| `connection.username` | `SURREALDB_USERNAME` |
| `connection.password` | `SURREALDB_PASSWORD` |
| `connection.token` | `SURREALDB_TOKEN` |

There is **no** env-var fallback for `connection.access`, `metadata.*`,
`analysis.*`, or the auth contexts.

### Building from source

```bash
git clone https://github.com/surrealdb/surrealql-language-server
cd surrealql-language-server

# The build requires a sibling checkout of the tree-sitter grammar.
bash scripts/setup-grammar.sh
# OR: TREE_SITTER_SURREALQL_DIR=/path/to/surrealql-tree-sitter cargo build

cargo build --release
# binary: target/release/surrealql-language-server
```

Pinned dependency: `surrealdb = "3.0.5"` (HTTP + WS + rustls features only).

---

## VS Code (`surrealdb.surrealql` v0.3.0)

The official VS Code extension (`surrealdb/surrealql-vsx`) is **a grammar
and snippets extension only**. From its `package.json`:

| Contribution | Provided | Detail |
|--------------|----------|--------|
| `languages` | yes | id `surrealql`, file extensions `.surql` + `.surrealql` |
| `grammars` | yes | TextMate grammar `source.surrealql`, plus injection grammars for JS/TS template literals (`inline.surrealql-js-literal`) and Markdown code fences (`markdown.surrealql.codeblock`) |
| `snippets` | yes | `./snippets.json` |
| `commands` | **no** | none contributed |
| `configuration` (settings) | **no** | none contributed |
| `languageServer` integration | **no** | the extension does not start a language server |

Required VS Code engine: `^1.77.0`.

```bash
# VS Code Marketplace
code --install-extension surrealdb.surrealql

# OpenVSX (VSCodium, code-server, Cursor, Windsurf)
codium --install-extension surrealdb.surrealql
```

To get diagnostics/hover/completion in VS Code today, install the
extension above for syntax + run the LSP through a generic LSP-client
extension that lets you bind a binary to a `languageId`. There is no
first-party VS Code LSP extension at the v1.6.6 cut.

---

## JetBrains (`com.surrealdb.surql-jetbrains`)

The official JetBrains plugin (`surrealdb/surrealql-jetbrains`,
Marketplace id `31397`) supports IntelliJ IDEA, PyCharm, WebStorm,
GoLand, RustRover, DataGrip, and other IntelliJ-platform IDEs. From
`plugin.xml`:

| Contribution | Detail |
|--------------|--------|
| Plugin id | `com.surrealdb.surql-jetbrains` |
| Required platform plugins | `org.jetbrains.plugins.textmate`, `com.redhat.devtools.lsp4ij` |
| Syntax | TextMate bundle (provided by the plugin) |
| File icon | `.surql` / `.surrealql` |
| LSP integration | LSP4IJ server `surrealqlLanguageServer`, factory `com.surrealdb.surql.lsp.SurQLLanguageServerFactory` |
| File pattern → server mapping | `*.surql;*.surrealql → surrealqlLanguageServer` |
| Notification group | `SurrealQL` (BALLOON) |
| Settings page | **Settings → Tools → SurrealQL** (configurable id `com.surrealdb.surql.settings`) |
| Persistent settings service | `com.surrealdb.surql.settings.SurQLSettings` |

The plugin auto-downloads the `surrealql-language-server` binary from
GitHub Releases on first launch and caches it locally. From the
plugin's own description: *"You can pin a release or override the
binary path under Settings → Tools → SurrealQL."*

A `postStartupActivity` warms the LSP binary cache so the first
`.surql` open does not pay GitHub-download latency.

---

## Zed (`surrealdb-surrealql` v0.1.0)

The official Zed extension (`surrealdb/surrealql-zed`) wires the LSP
into Zed's extension API.

From `extension.toml`:

| Field | Value |
|-------|-------|
| `id` | `surrealdb-surrealql` |
| `name` | `SurrealQL` |
| `version` | `0.1.0` |
| `schema_version` | `1` |
| `repository` | `https://github.com/surrealdb/surrealql-zed` |
| `[grammars.surrealql].repository` | `https://github.com/surrealdb/surrealql-tree-sitter` |
| `[grammars.surrealql].commit` | `bf420b6dbe1f31da5d6609ce090d19d2a549f538` |
| `[language_servers.surrealql-lsp].name` | `SurrealQL Language Server` |
| `[language_servers.surrealql-lsp].languages` | `["Surreal Query Language"]` |

From `languages/surql/config.toml`:

| Field | Value |
|-------|-------|
| `name` | `Surreal Query Language` |
| `grammar` | `surrealql` |
| `language_servers` | `["surrealql-lsp"]` |
| `path_suffixes` | `["surql"]` |
| `line_comments` | `["-- "]` |
| `hard_tabs` | `true` |

From `src/lib.rs`: the extension binary discovery prefers a
locally-installed `surrealql-language-server` on `$PATH`
(`worktree.which(BINARY_NAME)`) and otherwise downloads a release asset
from `surrealdb/surrealql-language-server` matching one of:

```
surrealql-language-server-macos-arm64
surrealql-language-server-linux-amd64
surrealql-language-server-linux-arm64
surrealql-language-server-windows-amd64.exe
```

If none are available the extension fails with an installer hint:
*"Install it manually with: `cargo install --git
https://github.com/surrealdb/surrealql-language-server`."*

---

## CodeMirror (`@surrealdb/codemirror` v1.0.5)

The official CodeMirror package lives in `surrealdb/codemirror` and publishes
two npm packages:

| Package | Purpose |
|---------|---------|
| `@surrealdb/codemirror` | CodeMirror extension with highlighting, folding, indentation, comment toggling, embedded JavaScript highlighting, and version-aware linting |
| `@surrealdb/lezer` | Low-level Lezer grammar used by the CodeMirror extension |

Install:

```bash
npm install @surrealdb/codemirror
```

Use:

```typescript
import { surrealql, surrealqlVersionLinter } from "@surrealdb/codemirror";

const state = EditorState.create({
  doc: "SELECT * FROM table",
  extensions: [
    surrealql(),
    surrealqlVersionLinter("2.0.0"),
  ],
});
```

`@surrealdb/codemirror` is editor-embedded syntax tooling. It is not an LSP
client, does not connect to a SurrealDB instance, and should not be treated as
a replacement for `surrealql-language-server` when you need schema-aware
workspace diagnostics.

---

## Other editors (community / wire-it-yourself)

The SurrealDB GitHub org now publishes small first-party extension repos for
Neovim, Helix, and Emacs (`surrealql-neovim`, `surrealql-helix`,
`surrealql-emacs`), but they are source-only at the v1.6.6 cut and have no
release tags. For those editors, install `surrealql-language-server` on
`$PATH` and configure the editor's LSP client to point at it.

### Neovim (`nvim-lspconfig`)

```lua
-- requires surrealql-language-server on $PATH
require("lspconfig").util.default_config = require("lspconfig").util.default_config
local configs = require("lspconfig.configs")
if not configs.surrealql then
  configs.surrealql = {
    default_config = {
      cmd = { "surrealql-language-server" },
      filetypes = { "surrealql", "surql" },
      root_dir = require("lspconfig.util").root_pattern(".git"),
      settings = {
        surrealql = {
          connection = { endpoint = "ws://127.0.0.1:8000/rpc" },
          activeAuthContext = "viewer",
        },
      },
    },
  }
end
require("lspconfig").surrealql.setup({})
```

Use the upstream `surrealdb/surrealql-neovim` repo as the first place to check
for current Neovim wiring. The inline snippet above remains a portable fallback
when you only have `nvim-lspconfig`.

### Helix (`languages.toml`)

```toml
[[language]]
name = "surrealql"
scope = "source.surrealql"
file-types = ["surql", "surrealql"]
language-servers = ["surrealql-language-server"]
comment-token = "--"

[language-server.surrealql-language-server]
command = "surrealql-language-server"
config = { surrealql = { activeAuthContext = "viewer" } }
```

### Sublime Text

No first-party Sublime package exists at the v1.6.6 cut. Wire the LSP
through the `LSP` package (sublimelsp.github.io/LSP) and bring your
own SurrealQL syntax (the TextMate grammar in `surrealdb/surrealql-vsx`
is loadable). Treat anything more specific than "use the LSP package
plus a TextMate grammar" as out of scope.

### Emacs

Use the upstream `surrealdb/surrealql-emacs` repo for current Emacs packaging.
`eglot` or `lsp-mode` can drive `surrealql-language-server` over stdio; bring
tree-sitter grammar support if you need richer local highlighting.

---

## Choosing Between LSP, MCP, and Surrealist

These three surfaces overlap but optimize for different audiences:

| Audience | Primary surface | Why |
|----------|-----------------|-----|
| Developer authoring SurrealQL in their editor | LSP + extension | Inline diagnostics, completion, formatting -- editor-native |
| Coding agent (Claude, Cursor, Copilot, Codex) | SurrealMCP | Stable tool catalog, structured introspection, no UI |
| Operator running ad-hoc queries / debugging | Surrealist | Visual schema designer, query history, graph visualizer |

A typical setup runs all three: VS Code or Zed with the LSP for human
work, the MCP server registered in your AI host config for agent loops,
and Surrealist on the side for ops.

---

## Cross-References

- `rules/surrealql.md` -- the language the LSP and grammar parse
- `rules/surrealmcp.md` -- agent-facing equivalent (full tool catalog)
- `rules/surrealist.md` -- standalone GUI / IDE
- `rules/surrealkit.md` -- desired-state schema files the LSP would lint
- `references/surrealql_cheatsheet.md` -- quick syntax reference
- `surrealql-language-server` on crates.io: `https://crates.io/crates/surrealql-language-server`
- `surql-lsp` on crates.io: `https://crates.io/crates/surql-lsp` (older / community LSP, not what first-party extensions wire to)
- VS Code grammar repo: `https://github.com/surrealdb/surrealql-vsx`
- JetBrains plugin repo: `https://github.com/surrealdb/surrealql-jetbrains`
- Zed extension repo: `https://github.com/surrealdb/surrealql-zed`
- CodeMirror repo: `https://github.com/surrealdb/codemirror`
- Tree-sitter grammar: `https://github.com/surrealdb/surrealql-tree-sitter`
