# Templates and current CLI coverage gaps

This file covers the template lifecycle and the most important “do not promise this too early”
behaviour for agents.

## Template lifecycle

The CLI clearly supports the hosted template workflow:

- `templates create`
- `templates get`
- `templates list`
- `templates update`
- `templates publish`
- `templates duplicate`
- `templates delete`

Typical sequence:

1. create a draft template
2. update as needed
3. publish it
4. re-publish after later edits

## `templates create`

Useful options include:

- `--name`
- `--html` or `--html-file`
- `--subject`
- `--text`
- `--from`
- `--reply-to`
- `--alias`
- `--var KEY:type` or `--var KEY:type:fallback`

Template variables use triple-brace syntax:

```html
<h1>Hello {{{NAME}}}</h1>
<p>Total: {{{PRICE}}}</p>
```

## `templates publish`

Publishing promotes the draft to live use. After editing a published template, publish again to make
the new draft current.

## Important current caveat: direct template sends

The template command group says published templates can be used in emails via `template_id`.

However, the current `emails send` command implementation does **not** expose a direct
`--template-id` / template-variable flag surface.

### How to handle this safely

If the user asks to **manage** hosted templates:

- stay in the CLI
- use the `templates *` commands

If the user asks to **send** using a hosted template:

1. say that the hosted template lifecycle exists in the CLI,
2. note that direct send-by-template is not clearly exposed in the current `emails send` flags,
3. offer one of these paths:
   - render the content to local HTML and use `emails send --html-file`
   - fall back to MCP/API for true hosted-template sending
   - inspect local `resend emails send --help` in case the installed CLI has advanced beyond this snapshot

Do **not** pretend the flag definitely exists unless local help proves it.

## Other important gaps and ambiguities

### Domain receiving toggle ambiguity

Inbound help text references enabling receiving via `domains update`, but the current
`domains update` implementation does not expose that option. Plan receiving at `domains create`
time or fall back if needed.

### JSON error channel discrepancy

The README promises JSON-to-stdout for machine mode, but the current implementation writes JSON
errors to stderr. Wrappers must parse both.

### Transactional natural-language scheduling

Broadcast commands explicitly support natural-language scheduling. Transactional `emails send` /
`emails update` help documents ISO examples. For agents, prefer ISO on transactional sends even if
the underlying API is more permissive.

## Practical template advice for agents

- Do not promise a pure CLI hosted-template send flow unless local help confirms it.
- Do not mix “hosted template lifecycle” and “raw HTML file send” as if they were the same thing.
- If the user mainly needs hosted-template sends in production automation, MCP/API may currently be
  the cleaner path.
