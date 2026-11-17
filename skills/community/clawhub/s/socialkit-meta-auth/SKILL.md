---
name: socialkit-meta-auth
description: Connects the user's own Meta app to their Facebook Pages, linked Instagram professional accounts and Threads profile, and stores the tokens securely. Use before the first Facebook, Instagram or Threads post, when a Meta token expired or was revoked, or to check which Pages and accounts are connected.
license: MIT
metadata:
  author: Ahmad Hussain
  platform: meta
  requires: socialkit-social-core
---

# Meta auth

Setup (app, redirect page, environment): [setup](references/setup.md).

## Steps

1. Check what is connected: `node scripts/auth.mjs --platform facebook --status` (and
   `--platform threads`). Instagram uses the facebook sign-in.
2. If not connected, run `node scripts/auth.mjs --platform <facebook|threads> --start`
   and give the user the `signInUrl`. Ask them to sign in and paste back the full URL of
   the page they land on.
3. Finish: `node scripts/auth.mjs --platform <facebook|threads> --finish --url "<pasted URL>"`
4. Report the connected Pages (with `canPost`), linked Instagram accounts, or the Threads
   user and expiry.

## Rules

- Never print or paste tokens or the app secret. The pasted redirect URL is single-use.
- A Page with `canPost: false` needs the user to get a content role on that Page.
- No Instagram listed under a Page: the Instagram account is personal or not linked.

## Failure handling

- `META_AUTH_STATE`: the URL is from an older attempt; start again.
- `META_AUTH_EXCHANGE`: the redirect URI does not exactly match the app settings, or the
  app ID/secret pair is wrong (Threads has its own pair).
- `THREADS_TOKEN_EXPIRED`: sign in again; expired tokens cannot be refreshed.
