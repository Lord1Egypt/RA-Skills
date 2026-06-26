# Publishing Notes

This skill prepares a WeChat Official Account article and hands it off to a user-authorized publishing tool. It does not contain publishing code or credentials.

## Before handoff

Verify:

- `article.md` exists and uses Markdown image placeholders such as `![](img0.png)`.
- `cover.png` exists when the target publisher requires a cover.
- Referenced body images exist in the article folder.
- No secrets, tokens, cookies, browser profile paths, or private config values appear in the article body or frontmatter.
- The target publishing tool is installed and trusted by the user.

## Required account configuration

Actual WeChat publishing requires account access controlled by the user. Common configurations include:

- `WECHAT_APP_ID`
- `WECHAT_APP_SECRET`
- private ignored config managed by the companion publishing tool

Do not print secret values. It is safe to report only whether a required value appears to be present or missing.

## Recommended publisher

Use a vetted companion publishing skill/tool, for example `baoyu-post-to-wechat`, when it is installed and trusted in the current environment.

Before running any publisher:

1. Confirm the user asked to create or update a WeChat draft.
2. Confirm required account configuration is present.
3. Confirm the target is the draft box unless the user explicitly asks otherwise.
4. Run the smallest publisher command supported by the companion tool.
5. Verify success by checking the publisher output or draft-box evidence.

## Failure handling

| Issue | Action |
|---|---|
| Missing account config | Ask the user to configure the companion publisher or environment variables. |
| Invalid credentials | Stop and ask the user to update WeChat account settings. |
| IP allowlist / permission failure | Ask the user to update the WeChat Official Account settings. Do not bypass controls. |
| Image placeholder mismatch | Fix `article.md` placeholders and retry. |
| Publisher unavailable | Stop and explain which companion tool is needed. |

## Browser workflows

Browser-based publishing is not part of this skill. If a user explicitly chooses a browser-based publisher, use a dedicated companion skill/tool and an isolated, user-controlled browser profile.
