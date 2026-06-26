# YouTube OAuth Setup Guide

This guide walks you through creating Google OAuth credentials so the moderator can reply to and delete comments on your YouTube channel.

**Time required:** ~10 minutes
**Cost:** Free

## Step 1: Create a Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click the project dropdown (top left) → **New Project**
3. Name it something like `youtube-comment-moderator`
4. Click **Create**
5. Make sure the new project is selected in the dropdown

## Step 2: Enable the YouTube Data API

1. Go to [APIs & Services → Library](https://console.cloud.google.com/apis/library)
2. Search for **YouTube Data API v3**
3. Click it → click **Enable**

## Step 3: Configure the OAuth Consent Screen

1. Go to [APIs & Services → OAuth consent screen](https://console.cloud.google.com/apis/credentials/consent)
2. Choose **External** → click **Create**
3. Fill in:
   - **App name:** YouTube Moderator (or anything)
   - **User support email:** your email
   - **Developer contact email:** your email
4. Click **Save and Continue**
5. On the **Scopes** page, click **Add or Remove Scopes**
   - Search for `youtube.force-ssl`
   - Check the box for `YouTube Data API v3 — .../auth/youtube.force-ssl`
   - Click **Update** → **Save and Continue**
6. On the **Test users** page, click **Add Users**
   - Add the Google account email that owns your YouTube channel
   - Click **Save and Continue**
7. Click **Back to Dashboard**

> **Note:** The app stays in "Testing" mode, which is fine. Only your
> added test users can authorize. No Google review needed.

## Step 4: Create OAuth Credentials

1. Go to [APIs & Services → Credentials](https://console.cloud.google.com/apis/credentials)
2. Click **Create Credentials** → **OAuth client ID**
3. Application type: **Web application**
4. Name: `youtube-comment-moderator`
5. Under **Authorized redirect URIs**, add:
   ```
   http://127.0.0.1:8976/callback
   ```
6. Click **Create**
7. You'll see your **Client ID** and **Client Secret** — copy both

## Step 5: Get a YouTube API Key

1. Still on the [Credentials page](https://console.cloud.google.com/apis/credentials)
2. Click **Create Credentials** → **API key**
3. Copy the key
4. (Optional) Click **Restrict Key** → restrict to YouTube Data API v3

## Step 6: Set Environment Variables

Add to your `.env` file:

```bash
YOUTUBE_API_KEY=your_api_key_here
YT_MOD_CLIENT_ID=your_client_id_here
YT_MOD_CLIENT_SECRET=your_client_secret_here
```

## Step 7: Run Setup

```bash
python3 scripts/setup.py
```

The setup wizard will:
1. Detect your API key and OAuth credentials from environment
2. Ask for your YouTube channel URL or ID
3. Open a browser for OAuth authorization (or give you a URL to paste if headless)
4. Save tokens to `oauth.json`
5. Configure moderation mode, voice style, and FAQ

## Troubleshooting

**"Access blocked: This app's request is invalid" (redirect_uri_mismatch)**
→ Make sure `http://127.0.0.1:8976/callback` is in your Authorized redirect URIs (exact match, no trailing slash)

**"Access denied" or "This app is not verified"**
→ Click **Continue** (or **Advanced** → **Go to app**). This is expected for Testing mode apps.

**"The caller does not have permission" (403 on delete/reply)**
→ You must authorize with the Google account that owns the YouTube channel, not a different account.

**Token expired**
→ The moderator auto-refreshes tokens. If refresh fails, re-run `python3 scripts/setup.py` and re-authorize.
