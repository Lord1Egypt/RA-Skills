# Independent Browser Publish Path

## Canonical browser profile

Use:

```bash
~/.openclaw/browser/xhs-independent-user-data
```

Do not reuse:
- the user's daily browser profile
- OpenClaw's built-in browser profile for other tasks

## Start browser

```bash
node scripts/xhs_independent_browser.js
```

This opens Xiaohongshu publish page in the dedicated profile.

## First login

If Xiaohongshu is not logged in, ask the user to log in once in that browser.

## Publish flow

```bash
node scripts/xhs_independent_publish.js
```

This should:
1. open publish page
2. upload images
3. fill title
4. fill body
5. click the verified publish button selector

## Verified final publish selector

```js
#web > div > div > div.publish-page-container > div.publish-page-publish-btn > button.d-button.d-button-default.d-button-with-content.--color-static.bold.--color-bg-fill.--color-text-paragraph.custom-button.bg-red
```

## Operational note

If the profile is already open and Playwright cannot relaunch it because of a profile lock, close the existing independent browser instance first, then rerun.
