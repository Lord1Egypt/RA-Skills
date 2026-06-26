# CSRF Protection Reference

## Token-Based Protection

### Synchronizer Token Pattern

Generate unique per-session tokens and validate on state-changing requests:

```javascript
// Server-side token generation (Node.js)
const crypto = require('crypto');

function generateCSRFToken(session) {
  const token = crypto.randomBytes(32).toString('hex');
  session.csrfToken = token;
  return token;
}

// Middleware validation
function validateCSRF(req, res, next) {
  const token = req.headers['x-csrf-token'] || req.body._csrf;
  if (!token || token !== req.session.csrfToken) {
    return res.status(403).json({ error: 'Invalid CSRF token' });
  }
  next();
}
```

### Double Submit Cookie Pattern

```javascript
// Set CSRF cookie
res.cookie('csrf_token', token, {
  httpOnly: false,  // Must be readable by JavaScript
  secure: true,
  sameSite: 'Strict'
});

// Client sends token in header
fetch('/api/action', {
  method: 'POST',
  headers: {
    'X-CSRF-Token': getCookie('csrf_token')
  }
});

// Server validates cookie matches header
function validateDoubleSubmit(req) {
  const cookieToken = req.cookies.csrf_token;
  const headerToken = req.headers['x-csrf-token'];
  return cookieToken && cookieToken === headerToken;
}
```

## SameSite Cookie Attribute

```javascript
// Strict - never sent cross-site
res.cookie('session', value, { sameSite: 'Strict', secure: true, httpOnly: true });

// Lax - sent for top-level GET navigations (default in modern browsers)
res.cookie('session', value, { sameSite: 'Lax', secure: true, httpOnly: true });

// None - requires Secure flag, sent cross-site
res.cookie('session', value, { sameSite: 'None', secure: true, httpOnly: true });
```

**Recommendation**: Use `SameSite=Strict` for session cookies when possible, `Lax` as minimum.

## Fetch Metadata Headers

Validate request origin using Sec-Fetch-* headers:

```javascript
function validateFetchMetadata(req, res, next) {
  const site = req.headers['sec-fetch-site'];
  const mode = req.headers['sec-fetch-mode'];
  const dest = req.headers['sec-fetch-dest'];

  // Allow same-origin requests
  if (site === 'same-origin') return next();

  // Allow browser navigation requests
  if (site === 'none') return next();

  // Block cross-origin requests to sensitive endpoints
  if (site === 'cross-site') {
    return res.status(403).json({ error: 'Cross-site request blocked' });
  }

  // Allow same-site requests for non-sensitive operations
  if (site === 'same-site' && mode === 'navigate') return next();

  next();
}
```

## Framework Integration

### Express.js with csurf

```javascript
const csrf = require('csurf');
const csrfProtection = csrf({ cookie: true });

app.use(csrfProtection);

app.get('/form', (req, res) => {
  res.render('form', { csrfToken: req.csrfToken() });
});
```

### React Forms

```jsx
function Form({ csrfToken }) {
  const handleSubmit = async (e) => {
    e.preventDefault();
    await fetch('/api/submit', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRF-Token': csrfToken
      },
      body: JSON.stringify(formData)
    });
  };

  return (
    <form onSubmit={handleSubmit}>
      <input type="hidden" name="_csrf" value={csrfToken} />
      {/* form fields */}
    </form>
  );
}
```

### Twig Forms

```twig
<form method="post" action="/submit">
  <input type="hidden" name="_csrf_token" value="{{ csrf_token('form_name') }}">
  <!-- form fields -->
</form>
```

## Client-Side CSRF (AJAX)

Protect against CSRF in single-page applications:

```javascript
// Set up axios defaults
import axios from 'axios';

axios.defaults.xsrfCookieName = 'csrf_token';
axios.defaults.xsrfHeaderName = 'X-CSRF-Token';
axios.defaults.withCredentials = true;

// Or with fetch
async function secureFetch(url, options = {}) {
  const csrfToken = document.querySelector('meta[name="csrf-token"]')?.content;

  return fetch(url, {
    ...options,
    credentials: 'same-origin',
    headers: {
      ...options.headers,
      'X-CSRF-Token': csrfToken
    }
  });
}
```

## Verification Checklist

- [ ] All state-changing endpoints require CSRF tokens
- [ ] Tokens are cryptographically random (≥128 bits)
- [ ] Tokens are tied to user session
- [ ] Tokens validated server-side before processing
- [ ] SameSite cookie attribute set appropriately
- [ ] Fetch Metadata headers validated for sensitive endpoints
- [ ] GET requests are idempotent (no state changes)

OWASP Reference: https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html
