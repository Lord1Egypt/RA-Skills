# Verfi SDK Reference

## Installation

Add to any HTML page:

```html
<script src="https://sdk.verfi.io/v1/verfi.js" data-key="pk_YOUR_PUBLIC_KEY" async></script>
```

Place before the closing `</body>` tag.

## How It Works

1. SDK loads and scans for `<form>` elements on the page
2. Begins recording a session: mouse movements, clicks, scrolls, keystrokes, form interactions
3. Detects consent language and checkbox interactions
4. On form submission, generates a Verfi ID (`VF-xxxxxxxx`)
5. Session data is encrypted and sent to Verfi's API
6. The Verfi ID can be passed alongside lead data to buyers

## Configuration

| Attribute | Required | Description |
|-----------|----------|-------------|
| `data-key` | Yes | Public API key (`pk_...`) |
| `src` | Yes | SDK URL: `https://sdk.verfi.io/v1/verfi.js` |
| `async` | Recommended | Non-blocking load |

## What Gets Recorded

- **Mouse:** movements, clicks, hovers
- **Keyboard:** keystroke count (not content), typing patterns
- **Scroll:** scroll events and depth
- **Form:** field focus/blur, input changes, checkbox toggles
- **Consent:** consent language detection, checkbox state
- **Device:** user agent, screen resolution, platform, timezone
- **PII:** detected PII fields are SHA-256 hashed (email, phone, name, address)

## Accessing the Verfi ID

After form submission, the Verfi ID is available via:

1. **DOM:** The SDK adds a hidden `verfi-id` field to the form
2. **Event:** Listen for `verfi:session-created` event on the form element
3. **API:** Query sessions by the originating tenant's API key

## Security

- All PII is hashed client-side before transmission
- Session data is encrypted in transit (TLS) and at rest
- The SDK never stores raw PII
- Public keys (`pk_`) can only create sessions, not read them
