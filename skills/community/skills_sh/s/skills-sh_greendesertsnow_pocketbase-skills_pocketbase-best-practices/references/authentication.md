# Authentication

**Impact: CRITICAL**

Password authentication, OAuth2 integration, token management, MFA setup, and auth collection configuration.

---

## 1. Use Impersonation for Admin Operations

**Impact: MEDIUM (Safe admin access to user data without password sharing)**

Impersonation allows superusers to generate tokens for other users, enabling admin support tasks and API key functionality without sharing passwords.

**Incorrect (sharing credentials or bypassing auth):**

```javascript
// Bad: sharing user passwords for support
async function helpUser(userId, userPassword) {
  await pb.collection('users').authWithPassword(userEmail, userPassword);
  // Support team knows user's password!
}

// Bad: directly modifying records without proper context
async function fixUserData(userId) {
  // Bypasses user's perspective and rules
  await pb.collection('posts').update(postId, { fixed: true });
}
```

**Correct (using impersonation):**

```javascript
import PocketBase from 'pocketbase';

// Admin client with superuser auth (use environment variables, never hardcode)
const adminPb = new PocketBase(process.env.PB_URL);
await adminPb.collection('_superusers').authWithPassword(
  process.env.PB_SUPERUSER_EMAIL,
  process.env.PB_SUPERUSER_PASSWORD
);

async function impersonateUser(userId) {
  // Generate impersonation token (non-renewable)
  const impersonatedClient = await adminPb
    .collection('users')
    .impersonate(userId, 3600);  // 1 hour duration

  // impersonatedClient has user's auth context
  console.log('Acting as:', impersonatedClient.authStore.record.email);

  // Operations use user's permissions
  const userPosts = await impersonatedClient.collection('posts').getList();

  return impersonatedClient;
}

// Use case: Admin viewing user's data
async function adminViewUserPosts(userId) {
  const userClient = await impersonateUser(userId);

  // See exactly what the user sees (respects API rules)
  const posts = await userClient.collection('posts').getList();

  return posts;
}

// Use case: API keys for server-to-server communication
async function createApiKey(serviceUserId) {
  // Create a service impersonation token (use short durations, rotate regularly)
  const serviceClient = await adminPb
    .collection('service_accounts')
    .impersonate(serviceUserId, 86400);  // 24 hours max, rotate via scheduled task

  // Return token for service to use
  return serviceClient.authStore.token;
}

// Using API key token in another service
async function useApiKey(apiToken) {
  const pb = new PocketBase('http://127.0.0.1:8090');

  // Manually set the token
  pb.authStore.save(apiToken, null);

  // Now requests use the service account's permissions
  const data = await pb.collection('data').getList();
  return data;
}
```

**Important considerations:**

```javascript
// Impersonation tokens are non-renewable
const client = await adminPb.collection('users').impersonate(userId, 3600);

// This will fail - can't refresh impersonation tokens
try {
  await client.collection('users').authRefresh();
} catch (error) {
  // Expected: impersonation tokens can't be refreshed
}

// For continuous access, generate new token when needed
async function getImpersonatedClient(userId) {
  // Check if existing token is still valid
  if (cachedClient?.authStore.isValid) {
    return cachedClient;
  }

  // Generate fresh token
  return await adminPb.collection('users').impersonate(userId, 3600);
}
```

**Security best practices:**
- Use short durations for support tasks
- Log all impersonation events
- Restrict impersonation to specific admin roles
- Never expose impersonation capability in client code
- Use dedicated service accounts for API keys

Reference: [PocketBase Impersonation](https://pocketbase.io/docs/authentication/#impersonate-authentication)

## 2. Implement Multi-Factor Authentication

**Impact: HIGH (Additional security layer for sensitive applications)**

MFA requires users to authenticate with two different methods. PocketBase supports OTP (One-Time Password) via email as the second factor.

**Incorrect (single-factor only for sensitive apps):**

```javascript
// Insufficient for sensitive applications
async function login(email, password) {
  const authData = await pb.collection('users').authWithPassword(email, password);
  // User immediately has full access - no second factor
  return authData;
}
```

**Correct (MFA flow with OTP):**

```javascript
import PocketBase from 'pocketbase';

const pb = new PocketBase('http://127.0.0.1:8090');

async function loginWithMFA(email, password) {
  try {
    // First factor: password
    const authData = await pb.collection('users').authWithPassword(email, password);

    // If MFA not required, auth succeeds immediately
    return { success: true, authData };

  } catch (error) {
    // MFA required - returns 401 with mfaId
    if (error.status === 401 && error.response?.mfaId) {
      return {
        success: false,
        mfaRequired: true,
        mfaId: error.response.mfaId
      };
    }
    throw error;
  }
}

async function requestOTP(email) {
  // Request OTP to be sent via email
  const result = await pb.collection('users').requestOTP(email);

  // Returns otpId - needed to verify the OTP
  // Note: Returns otpId even if email doesn't exist (prevents enumeration)
  return result.otpId;
}

async function completeMFAWithOTP(mfaId, otpId, otpCode) {
  try {
    // Second factor: OTP verification
    const authData = await pb.collection('users').authWithOTP(
      otpId,
      otpCode,
      { mfaId }  // Include mfaId from first factor
    );

    return { success: true, authData };
  } catch (error) {
    if (error.status === 400) {
      throw new Error('Invalid or expired code');
    }
    throw error;
  }
}

// Complete flow example
async function fullMFAFlow(email, password, otpCode = null) {
  // Step 1: Password authentication
  const step1 = await loginWithMFA(email, password);

  if (step1.success) {
    return step1.authData;  // MFA not required
  }

  if (step1.mfaRequired) {
    // Step 2: Request OTP
    const otpId = await requestOTP(email);

    // Step 3: UI prompts user for OTP code...
    // (In real app, wait for user input)

    if (otpCode) {
      // Step 4: Complete MFA
      const step2 = await completeMFAWithOTP(step1.mfaId, otpId, otpCode);
      return step2.authData;
    }

    return { pendingMFA: true, mfaId: step1.mfaId, otpId };
  }
}
```

**Configure MFA (Admin UI or API):**

```javascript
// Enable MFA on auth collection (superuser only)
await pb.collections.update('users', {
  mfa: {
    enabled: true,
    duration: 1800,  // MFA session duration (30 min)
    rule: ''  // When to require MFA (empty = always for all users)
    // rule: '@request.auth.role = "admin"' // Only for admins
  },
  otp: {
    enabled: true,
    duration: 300,  // OTP validity (5 min)
    length: 6,      // OTP code length
    emailTemplate: {
      subject: 'Your verification code',
      body: 'Your code is: {OTP}'
    }
  }
});
```

**MFA best practices:**
- Always enable for admin accounts
- Consider making MFA optional for regular users
- Use short OTP durations (5-10 minutes)
- Implement rate limiting on OTP requests
- Log MFA events for security auditing

Reference: [PocketBase MFA](https://pocketbase.io/docs/authentication/#mfa)

## 3. Integrate OAuth2 Providers Correctly

**Impact: CRITICAL (Secure third-party authentication with proper flow handling)**

OAuth2 integration should use the all-in-one method for simplicity and security. Manual code exchange should only be used when necessary (e.g., mobile apps with deep links).

**Incorrect (manual implementation without SDK):**

```javascript
// Don't manually handle OAuth flow
async function loginWithGoogle() {
  // Redirect user to Google manually
  window.location.href = 'https://accounts.google.com/oauth/authorize?...';
}

// Manual callback handling
async function handleCallback(code) {
  // Exchange code manually - error prone!
  const response = await fetch('/api/auth/callback', {
    method: 'POST',
    body: JSON.stringify({ code })
  });
}
```

**Correct (using SDK's all-in-one method):**

```javascript
import PocketBase from 'pocketbase';

const pb = new PocketBase('http://127.0.0.1:8090');

// All-in-one OAuth2 (recommended for web apps)
async function loginWithOAuth2(providerName) {
  try {
    const authData = await pb.collection('users').authWithOAuth2({
      provider: providerName,  // 'google', 'github', 'microsoft', etc.
      // Optional: create new user data if not exists
      createData: {
        emailVisibility: true,
        name: ''  // Will be populated from OAuth provider
      }
    });

    console.log('Logged in via', providerName);
    console.log('User:', authData.record.email);
    console.log('Is new user:', authData.meta?.isNew);

    return authData;
  } catch (error) {
    if (error.isAbort) {
      console.log('OAuth popup was closed');
      return null;
    }
    throw error;
  }
}

// Usage
document.getElementById('google-btn').onclick = () => loginWithOAuth2('google');
document.getElementById('github-btn').onclick = () => loginWithOAuth2('github');
```

**Manual code exchange (for React Native / deep links):**

```javascript
// Only use when all-in-one isn't possible
async function loginWithOAuth2Manual() {
  // Get auth methods - PocketBase provides state and codeVerifier
  const authMethods = await pb.collection('users').listAuthMethods();
  const provider = authMethods.oauth2.providers.find(p => p.name === 'google');

  // Store the provider's state and codeVerifier for callback verification
  // PocketBase generates these for you - don't create your own
  sessionStorage.setItem('oauth_state', provider.state);
  sessionStorage.setItem('oauth_code_verifier', provider.codeVerifier);

  // Build the OAuth URL using provider.authURL + redirect
  const redirectUrl = window.location.origin + '/oauth-callback';
  const authUrl = provider.authURL + encodeURIComponent(redirectUrl);

  // Redirect to OAuth provider
  window.location.href = authUrl;
}

// In your callback handler (e.g., /oauth-callback page):
async function handleOAuth2Callback() {
  const params = new URLSearchParams(window.location.search);

  // CSRF protection: verify state matches
  if (params.get('state') !== sessionStorage.getItem('oauth_state')) {
    throw new Error('State mismatch - potential CSRF attack');
  }

  const code = params.get('code');
  const codeVerifier = sessionStorage.getItem('oauth_code_verifier');
  const redirectUrl = window.location.origin + '/oauth-callback';

  // Exchange code for auth token
  const authData = await pb.collection('users').authWithOAuth2Code(
    'google',
    code,
    codeVerifier,
    redirectUrl,
    { emailVisibility: true }
  );

  // Clean up
  sessionStorage.removeItem('oauth_state');
  sessionStorage.removeItem('oauth_code_verifier');

  return authData;
}
```

**Configure OAuth2 provider (Admin UI or API):**

```javascript
// Via API (superuser only) - usually done in Admin UI
// IMPORTANT: Never hardcode client secrets. Use environment variables.
await pb.collections.update('users', {
  oauth2: {
    enabled: true,
    providers: [{
      name: 'google',
      clientId: process.env.GOOGLE_CLIENT_ID,
      clientSecret: process.env.GOOGLE_CLIENT_SECRET
    }],
    mappedFields: {
      avatarURL: 'avatar'  // Map OAuth field to collection field
    }
  }
});
```

Reference: [PocketBase OAuth2](https://pocketbase.io/docs/authentication/#oauth2-authentication)

## 4. Use authWithOTP for Email One-Time Codes, Rate-Limit requestOTP

**Impact: HIGH (OTP endpoints are unauthenticated; unthrottled requestOTP enables email bombing and enumeration)**

Auth collections can enable **OTP login** from the admin UI (Collection → Options → "Enable OTP"). The client flow is two steps: `requestOTP(email)` returns an `otpId`, then `authWithOTP(otpId, code)` exchanges the id + code for an auth token. Two things trip people up: (1) the OTP response is **the same whether the email exists or not** - do not break that by leaking a distinct error; (2) `requestOTP` sends an email, so **it must be rate-limited** or an attacker can use it to spam any address.

**Incorrect (leaks existence, custom requestOTP with no rate limit):**

```javascript
// ❌ Client-side existence check - ignore the 404 and expose it to the user
try {
    await pb.collection("users").getFirstListItem(`email="${email}"`);
} catch (e) {
    alert("No account with that email"); // ❌ account enumeration
    return;
}

// ❌ Ad-hoc route with no rate limit - attacker hammers this to spam mailboxes
routerAdd("POST", "/api/myapp/otp", (e) => {
    const body = e.requestInfo().body;
    const user = $app.findAuthRecordByEmail("users", body.email);
    // send custom email...
    return e.json(200, { ok: true });
});
```

**Correct (use the built-in flow, step 1 always returns an otpId):**

```javascript
// Step 1: request the code. Always returns { otpId } - even if the email
// does not exist, PocketBase returns a synthetic id so enumeration is
// impossible. Treat every response as success from the UI perspective.
const { otpId } = await pb.collection("users").requestOTP("user@example.com");

// Step 2: exchange otpId + the 8-digit code the user typed
const authData = await pb.collection("users").authWithOTP(
    otpId,
    "12345678",
);
// pb.authStore is now populated
```

```go
// Go side - rate-limit and log if you wrap your own endpoint
app.OnRecordRequestOTPRequest("users").BindFunc(func(e *core.RecordRequestOTPRequestEvent) error {
    // e.Collection, e.Record (may be nil - synthetic id path),
    // e.Email (always present), e.Password (unused for OTP)
    e.App.Logger().Info("otp requested",
        "email", e.Email,
        "ip",    e.RequestInfo.Headers["x_forwarded_for"])
    return e.Next() // REQUIRED
})
```

**Rules:**
- `requestOTP` **always returns 200 with an otpId**, even for non-existent emails - preserve that by never adding a pre-check or a different error path.
- Enable the built-in rate limiter (see `deploy-rate-limiting.md`) and raise the cost for the `*:requestOTP` label. Without this, an attacker can email-bomb arbitrary users.
- The OTP code is 8 digits by default, with a 3-minute TTL. Do not extend the TTL - short windows are the whole point.
- `authWithOTP` consumes the code; a successful call invalidates the `otpId`. Always show a generic "invalid or expired code" on failure.
- If you want OTP **without a password**, set the collection's `Password` option to off and `OTP` on. If both are enabled, users can use either.
- OTP emails are sent via the configured SMTP server. In dev, point SMTP at Mailpit or a console logger before testing - do **not** ship with the default "no-reply@example.com" sender.

Reference: [Auth with OTP](https://pocketbase.io/docs/authentication/#auth-with-otp) · [JS SDK - authWithOTP](https://github.com/pocketbase/js-sdk#authwithotp)

## 5. Implement Secure Password Authentication

**Impact: CRITICAL (Secure user login with proper error handling and token management)**

Password authentication should include proper error handling, avoid exposing whether emails exist, and correctly manage the auth store.

**Incorrect (exposing information and poor error handling):**

```javascript
// Dangerous: exposes whether email exists
async function login(email, password) {
  const user = await pb.collection('users').getFirstListItem(`email = "${email}"`);
  if (!user) {
    throw new Error('Email not found');  // Reveals email doesn't exist
  }

  // Manual password check - never do this!
  if (user.password !== password) {
    throw new Error('Wrong password');  // Reveals password is wrong
  }

  return user;
}
```

**Correct (secure authentication):**

```javascript
import PocketBase from 'pocketbase';

const pb = new PocketBase('http://127.0.0.1:8090');

async function login(email, password) {
  try {
    // authWithPassword handles hashing and returns token
    const authData = await pb.collection('users').authWithPassword(email, password);

    // Token is automatically stored in pb.authStore
    console.log('Logged in as:', authData.record.email);
    console.log('Token valid:', pb.authStore.isValid);

    return authData;
  } catch (error) {
    // Generic error message - don't reveal if email exists
    if (error.status === 400) {
      throw new Error('Invalid email or password');
    }
    throw error;
  }
}

// Check if user is authenticated
function isAuthenticated() {
  return pb.authStore.isValid;
}

// Get current user
function getCurrentUser() {
  return pb.authStore.record;
}

// Logout
function logout() {
  pb.authStore.clear();
}

// Listen for auth changes
pb.authStore.onChange((token, record) => {
  console.log('Auth state changed:', record?.email || 'logged out');
}, true);  // true = fire immediately with current state
```

**Auth collection configuration for password auth:**

```javascript
// When creating auth collection via API (superuser only)
await pb.collections.create({
  name: 'users',
  type: 'auth',
  fields: [
    { name: 'name', type: 'text' },
    { name: 'avatar', type: 'file', options: { maxSelect: 1 } }
  ],
  passwordAuth: {
    enabled: true,
    identityFields: ['email', 'username']  // Fields that can be used to login
  },
  // Require minimum password length
  // (configured in Admin UI under collection options)
});
```

**Security considerations:**
- Never store passwords in plain text
- Use generic error messages
- Implement rate limiting on your server
- Consider adding MFA for sensitive applications

Reference: [PocketBase Auth](https://pocketbase.io/docs/authentication/)

## 6. Manage Auth Tokens Properly

**Impact: CRITICAL (Prevents unauthorized access, handles token expiration gracefully)**

Auth tokens should be refreshed before expiration, validated on critical operations, and properly cleared on logout. The SDK's authStore handles most of this automatically.

**Incorrect (ignoring token expiration):**

```javascript
// Bad: never checking token validity
async function fetchUserData() {
  // Token might be expired!
  const records = await pb.collection('posts').getList();
  return records;
}

// Bad: manually managing tokens
let authToken = localStorage.getItem('token');
fetch('/api/posts', {
  headers: { 'Authorization': authToken }  // Token might be invalid
});
```

**Correct (proper token management):**

```javascript
import PocketBase from 'pocketbase';

const pb = new PocketBase('http://127.0.0.1:8090');

// Check token validity before operations
async function fetchSecureData() {
  // authStore.isValid is a client-side check only (JWT expiry parsing).
  // Always verify server-side with authRefresh() for critical operations.
  if (!pb.authStore.isValid) {
    throw new Error('Please log in');
  }

  return pb.collection('posts').getList();
}

// Refresh token periodically or before expiration
async function refreshAuthIfNeeded() {
  if (!pb.authStore.isValid) {
    return false;
  }

  try {
    // Verifies current token and returns fresh one
    await pb.collection('users').authRefresh();
    console.log('Token refreshed');
    return true;
  } catch (error) {
    // Token invalid - user needs to re-authenticate
    pb.authStore.clear();
    return false;
  }
}

// Auto-refresh on app initialization
async function initializeAuth() {
  if (pb.authStore.token) {
    try {
      await pb.collection('users').authRefresh();
    } catch {
      pb.authStore.clear();
    }
  }
}

// Listen for auth changes and handle expiration
pb.authStore.onChange((token, record) => {
  if (!token) {
    // User logged out or token cleared
    redirectToLogin();
  }
});

// Setup periodic refresh (e.g., every 10 minutes)
setInterval(async () => {
  if (pb.authStore.isValid) {
    try {
      await pb.collection('users').authRefresh();
    } catch {
      pb.authStore.clear();
    }
  }
}, 10 * 60 * 1000);
```

**SSR / Server-side token handling:**

```javascript
// Server-side: create fresh client per request
export async function handleRequest(request) {
  const pb = new PocketBase('http://127.0.0.1:8090');

  // Load auth from cookie
  pb.authStore.loadFromCookie(request.headers.get('cookie') || '');

  // Validate and refresh
  if (pb.authStore.isValid) {
    try {
      await pb.collection('users').authRefresh();
    } catch {
      pb.authStore.clear();
    }
  }

  // ... handle request ...

  // Send updated cookie with secure options
  const response = new Response();
  response.headers.set('set-cookie', pb.authStore.exportToCookie({
    httpOnly: true,   // Prevent XSS access to auth token
    secure: true,     // HTTPS only
    sameSite: 'Lax',  // CSRF protection
  }));
  return response;
}
```

**Token configuration (Admin UI or migration):**

```javascript
// Configure token durations (superuser only)
await pb.collections.update('users', {
  authToken: {
    duration: 1209600  // 14 days in seconds
  },
  verificationToken: {
    duration: 604800   // 7 days
  }
});
```

Reference: [PocketBase Auth Store](https://pocketbase.io/docs/authentication/)

