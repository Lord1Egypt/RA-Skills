---
title: Integrate OAuth2 Providers Correctly
impact: CRITICAL
impactDescription: Secure third-party authentication with proper flow handling
tags: authentication, oauth2, google, github, social-login
---

## Integrate OAuth2 Providers Correctly

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
