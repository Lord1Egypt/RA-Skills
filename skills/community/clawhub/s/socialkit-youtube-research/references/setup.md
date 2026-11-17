# YouTube setup

Each user brings their own Google Cloud project and credentials. This package never
ships shared keys. Generated from `docs/platforms/youtube-setup.md`; edit it there.

## 1. Google Cloud project

1. Create a project at https://console.cloud.google.com/projectcreate
2. Open APIs & Services > Library, search "YouTube Data API v3" and enable it.

## 2. OAuth consent screen (needed for uploads)

1. Open Google Auth Platform (https://console.cloud.google.com/auth/overview) and
   configure the app: name, support email, audience "External" (or "Internal" for a
   Google Workspace organisation).
2. Add the scope `https://www.googleapis.com/auth/youtube.upload` under Data Access.
3. While the app is in "Testing", add your own Google account under Audience > Test
   users. Testing apps are limited to listed test users and their refresh tokens
   expire after 7 days, so you will need to re-run the auth script weekly.
4. For long-lived tokens, set the publishing status to "In production". Google may ask
   you to complete OAuth app verification for the requested scope; the console shows
   what is required.

## 3. OAuth client (uploads)

1. Google Auth Platform > Clients > Create client, application type **Desktop app**.
2. Download the client JSON. Store it outside any git repository, for example
   `~/.config/social-skills/youtube/oauth-client.json`, and restrict it:
   `chmod 600 ~/.config/social-skills/youtube/oauth-client.json`
3. Export the path (add to your shell profile, not to a committed file):
   `export YT_CLIENT_SECRET_PATH="$HOME/.config/social-skills/youtube/oauth-client.json"`
4. Authorise your channel from the socialkit-youtube-upload skill folder:
   `node scripts/auth.mjs`
   The token is stored at `~/.config/social-skills/youtube/token.json` (mode 0600), or
   at `YT_TOKEN_PATH` if set. The script refuses to store it inside a git repository.

## 4. API key (research only)

1. APIs & Services > Credentials > Create credentials > API key.
2. Restrict it: API restrictions > YouTube Data API v3. Add application restrictions
   where your environment allows.
3. `export YT_API_KEY=...` from your shell profile or a secret manager. Never commit it.

## 5. Quota and audit

- Default allocation (per Google Cloud project, documented 2026-10-15):
  `videos.insert` 100 calls/day and `search.list` 100 calls/day, each in its own bucket;
  all other calls share 10,000 units/day (`thumbnails.set` costs 50). Quotas reset at
  midnight Pacific Time. https://developers.google.com/youtube/v3/determine_quota_cost
- More quota requires the YouTube API Services audit and quota extension form:
  https://support.google.com/youtube/contact/yt_api_form . The audit reviews your use
  against the YouTube API Services Terms and Developer Policies.
- Older guidance said uploads from unverified API projects (created after
  2020-07-28) were locked to private. The current `videos.insert` documentation says
  unverified projects are no longer restricted to private. If YouTube still sets your
  upload to a different privacy than requested, the upload script warns you.

## 6. Account limits

- The Google account must have a YouTube channel.
- Custom thumbnails require a verified channel (https://www.youtube.com/verify).
- YouTube applies per-channel daily upload limits independent of API quota.
- Every upload must declare made-for-kids status (`madeForKids` in `metadata.json`).
- Scheduled uploads must be private until the publish time.

## 7. Revoking access

- Remove the app at https://myaccount.google.com/permissions
- Delete the token file listed above.
- Delete or rotate the OAuth client and API key in Google Cloud console.
