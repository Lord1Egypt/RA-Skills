# Command Patterns

## PowerShell invocation

Use the checked-out toolkit directly:

```powershell
& 'D:\silmairl cdp\silmaril.cmd' openbrowser --json
& 'D:\silmairl cdp\silmaril.cmd' openUrl 'https://example.com' --json
```

If the checkout is not present at that path, resolve `silmaril.cmd` from `PATH` or the local workspace before proceeding.

## Read patterns

- Single assertion: `get-text '#title' --json`
- Presence check: `exists '[data-test="submit"]' --json`
- Structured extraction: `query 'a[href]' --fields 'text,href,attr:data-test' --limit 20 --json`
- Debug markup: `get-dom '#main' --json`

Prefer `query` when later steps need rows or machine-readable fields.

## Action patterns

- Click: `click '#submit' --yes --json`
- Type: `type '#search' 'hello world' --yes --json`
- Replace text: `set-text '#status' 'Done' --yes --json`
- Replace HTML: `set-html '#box' '<h3>Updated</h3>' --yes --json`

Validate the selector first with `exists`, `get-text`, or `query`.

## Wait patterns

- Show element: `wait-for '#result' --json`
- Wait for any outcome: `wait-for-any '.result-list' '.empty-state' --counts --json`
- Spinner disappears: `wait-for-gone '.spinner' --json`
- JS condition: `wait-until-js "document.querySelectorAll('.item').length > 0" --json`
- Mutation watch: `wait-for-mutation '#app' --details --json`

Use one explicit wait after each action instead of sleeping.

## JavaScript patterns

Prefer inline `eval-js` only for short expressions:

```powershell
& 'D:\silmairl cdp\silmaril.cmd' eval-js "document.title" --allow-unsafe-js --yes --json
```

Prefer file mode for longer logic:

```powershell
Set-Content -LiteralPath 'C:\Users\hangx\silmaril-expr.js' -Encoding UTF8 -Value "JSON.stringify(Array.from(document.querySelectorAll('a[href]')).map(a => a.href))"
& 'D:\silmairl cdp\silmaril.cmd' eval-js --file 'C:\Users\hangx\silmaril-expr.js' --allow-unsafe-js --yes --json
```

High-risk rule:

- `eval-js` requires `--allow-unsafe-js` unless `SILMARIL_ALLOW_UNSAFE_JS=1` is already set for a trusted local session.
- Proxy commands require `--allow-mitm` unless `SILMARIL_ALLOW_MITM=1` is already set for a trusted local session.
- Proxy listeners stay loopback-only unless `--allow-nonlocal-bind` is explicitly requested.

## Targeting rules

- Use `--target-id` when a specific CDP page target is already known.
- Use `--url-match` when selecting a page by URL pattern is simpler.
- Never pass both flags in the same call.

## Source files

For deeper details, consult the local toolkit docs in `D:\silmairl cdp\COMMAND_GUIDE.md` and the command implementations under `D:\silmairl cdp\commands\`.
