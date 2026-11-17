# TikTok setup

Bring your own TikTok app. Facts checked 2026-10-24. Generated from
`docs/platforms/tiktok-setup.md`; edit it there.

## Read this first

TikTok's audit is for public apps: "Apps must not be for private or personal use", and a
tool to upload to accounts you manage is named as unacceptable. An app you own will stay
**unaudited**, which means:

- Direct posts are **private (SELF_ONLY)** and the account may need to be private.
- At most 5 users can post through the app per 24 hours.

So the default here is **draft mode**: the video is sent to your TikTok inbox and you
finish and publish it in the TikTok app.

## App

1. https://developers.tiktok.com > Manage apps > Create, platform **Desktop**.
2. Add Login Kit and Content Posting API; request scopes `user.info.basic`,
   `video.upload` (drafts) and `video.publish` (direct).
3. Redirect URI: `http://127.0.0.1:8766/callback/` (desktop apps may use 127.0.0.1).
4. In `~/.config/social-skills/env.sh`:
   ```sh
   export TIKTOK_CLIENT_KEY="..."
   export TIKTOK_CLIENT_SECRET="..."
   ```

## Sign in

`node scripts/auth.mjs --platform tiktok` (PKCE). Access tokens last 24 hours and refresh
automatically for a year.

## Rules this skill enforces (Content Sharing Guidelines)

Creator nickname shown before posting; privacy chosen by you with no default;
comments, duets and stitches off unless you turn them on; branded content cannot be
private; your explicit approval before anything is uploaded. About 15 posts per day per
account across all apps.

## Sources

- https://developers.tiktok.com/doc/content-sharing-guidelines
- https://developers.tiktok.com/doc/content-posting-api-reference-direct-post
- https://developers.tiktok.com/doc/login-kit-desktop
