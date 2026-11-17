# Meta setup (Facebook Pages, Instagram, Threads)

Each user brings their own Meta app; this package never ships shared keys. Your own
app works on accounts you own or manage without Meta App Review ("Standard Access"):
anyone with a role on the app can authorise it. Generated from
`docs/platforms/meta-setup.md`; edit it there. Facts checked 2026-10-24.

## Account requirements

- **Facebook:** Pages only. The API cannot post to personal profiles. You need a role on
  the Page that allows creating content.
- **Instagram:** a Business or Creator account **linked to a Facebook Page**. Personal
  Instagram accounts are not supported by the API.
- **Threads:** any Threads profile, added as a Threads Tester on your app.

## 1. Redirect page (all three)

Meta sends you back to a redirect URL after sign-in, and Threads requires HTTPS (no
localhost). Use any HTTPS page on a domain you control; it only has to load. For example
a GitHub Pages site: `https://<your-github-user>.github.io/oauth/`. You copy the URL you
land on and give it to the auth script. The code in it is single-use, expires in an hour
and is useless without your app secret.

## 2. Facebook and Instagram app

1. https://developers.facebook.com/apps > Create app > type **Business**.
2. Add **Facebook Login for Business**. Under its settings add your redirect URL to
   **Valid OAuth Redirect URIs** (exact match, Strict Mode on).
3. Optional but recommended: create a Login configuration (User access token) with the
   permissions below, and set its ID as `META_LOGIN_CONFIG_ID`. Without it the auth script
   requests the permissions by scope.
4. Permissions used: `pages_show_list`, `pages_read_engagement`, `pages_manage_posts`,
   `instagram_basic`, `instagram_content_publish`.
5. App settings > Basic: copy the **App ID** and **App secret**.

## 3. Threads app

1. Create an app with the use case **Access the Threads API**. It has its own Threads
   app ID and secret; use those, not the Facebook pair.
2. Add permissions `threads_basic` and `threads_content_publish`.
3. Add your redirect URL under the Threads use case settings, plus a Deauthorize callback
   and Data Deletion Request URL (any HTTPS page you control).
4. App roles > Roles > Add People > **Threads Tester**: invite your Threads account, then
   accept it in Threads > Settings > Account > Website permissions.

## 4. Environment

Store in `~/.config/social-skills/env.sh` (mode 600), never in a repository:

```sh
export META_APP_ID="..."
export META_APP_SECRET="..."
export META_REDIRECT_URI="https://<your-domain>/oauth/"
# export META_LOGIN_CONFIG_ID="..."
export THREADS_APP_ID="..."
export THREADS_APP_SECRET="..."
export THREADS_REDIRECT_URI="https://<your-domain>/oauth/"
```

## 5. Sign in

From the socialkit-meta-auth skill folder:

```sh
node scripts/auth.mjs --platform facebook --start     # prints a sign-in URL
node scripts/auth.mjs --platform facebook --finish --url "<URL you landed on>"
node scripts/auth.mjs --platform threads --start
node scripts/auth.mjs --platform threads --finish --url "<URL you landed on>"
```

Tokens go to `~/.config/social-skills/meta/` with mode 0600. Facebook Page tokens do not
expire; Threads tokens last 60 days and are refreshed automatically when you publish.
A permission unused for 90 days must be granted again.

## 6. Limits

| | Limit |
| - | - |
| Instagram | publishing quota per 24 h read from the API at publish time (docs say 50 or 100); caption 2,200 chars, 30 hashtags, 20 mentions; images JPEG only, from a public URL; carousel 2-10; no API scheduling |
| Facebook | scheduling 10 minutes to 30 days ahead (video up to 6 months); photos up to 10 MB |
| Threads | 250 posts per 24 h; 500 characters; 5 links; media from a public URL; carousel 2-20; no API scheduling |

## 7. Sources

- Instagram publishing: https://developers.facebook.com/docs/instagram-platform/content-publishing
- Instagram errors: https://developers.facebook.com/docs/instagram-platform/instagram-graph-api/reference/error-codes
- Page posts: https://developers.facebook.com/docs/pages-api/posts
- Page photos: https://developers.facebook.com/docs/graph-api/reference/page/photos/
- Facebook Login for Business: https://developers.facebook.com/docs/facebook-login/facebook-login-for-business/
- Long-lived tokens: https://developers.facebook.com/docs/facebook-login/guides/access-tokens/get-long-lived
- Threads: https://developers.facebook.com/documentation/threads/get-started
- Access levels: https://developers.facebook.com/docs/graph-api/overview/access-levels
