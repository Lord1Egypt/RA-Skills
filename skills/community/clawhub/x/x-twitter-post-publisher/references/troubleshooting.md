# Troubleshooting

## Post button is disabled even though text is visible

Root cause: X compose uses a Draft.js contenteditable editor. Some automation paths only change visible DOM text and do not update the internal editor state.

Use native clipboard paste:
1. `Set-Clipboard -Value $text`
2. focus the editor
3. `Control+a`
4. `Backspace`
5. `Control+v`

Then verify the button through:

```powershell
opencli browser eval "(() => { const btn = document.querySelector('[data-testid=\"tweetButtonInline\"]'); return JSON.stringify({ enabled: !!btn && !btn.disabled, ariaDisabled: btn ? btn.getAttribute('aria-disabled') : null }); })()"
```

## Content is duplicated in the composer

A stale draft was already present.

Fix:
- focus the editor
- `Control+a`
- `Backspace`
- wait a moment
- paste once

## User is logged in but automation shows logged out

You are likely using the wrong browser context.

Prefer `opencli browser` / `opencli twitter` when the user is already logged into Chrome.
Avoid isolated browser sessions for X posting unless the user explicitly wants that.

## Verification search finds nothing

Possible causes:
- search indexing delay
- wrong snippet chosen
- post failed silently

Try:
1. check the author timeline
2. search for a rarer sentence fragment
3. wait a few seconds and search again

## Post is over the limit

Do not attempt submission. Shorten first.

A practical pattern:
- remove filler lines
- compress repeated claims
- keep one proof point, one payoff, one CTA/link
