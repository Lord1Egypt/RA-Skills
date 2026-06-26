---
name: wechat-mp-draft-publisher
description: Publish WeChat Official Account draft articles through a packaged CLI executable that wraps WeChat API calls. Use when the user wants to publish or create a draft from local article content and images, especially when the required flow is getAuth -> uploadArticleImage -> uploadCoverImage -> addDraft.
---

# WeChat MP Draft Publisher

Publish draft articles by calling the bundled wrapper script, which enforces this fixed sequence:
1. `getAuth`
2. `uploadArticleImage`
3. `uploadCoverImage`
4. `addDraft`

## Requirements

- Provide executable via one of:
  - Local binary path:
    - CLI flag `--bin /absolute/path/to/mp-weixin-skill`
    - Env var `MP_WECHAT_CLI_BIN`
  - GitHub Release auto-download:
    - Env var `MP_WECHAT_RELEASE_URL=https://github.com/<owner>/<repo>/releases/download/<tag>/<asset>` (direct asset URL, supports zip or binary)
    - or:
    - Env var `MP_WECHAT_GITHUB_REPO=owner/repo`
    - Optional env `MP_WECHAT_RELEASE_TAG=latest` (default latest)
    - Optional env `MP_WECHAT_ASSET_NAME=custom-asset-name`
- Ensure local credentials file exists for `getAuth`:
  - `~/.weixin_credentials`
  - format:
    - `appid=YOUR_APP_ID`
    - `secret=YOUR_APP_SECRET`
- Prepare these files before running:
  - Article content file (`--content-file`), usually HTML
  - Inline article image (`--article-image`)
  - Cover image (`--cover-image`)

## Run

Use the wrapper script:

```bash
bash scripts/publish_draft.sh \
  --article-image /absolute/path/to/article-image.png \
  --cover-image /absolute/path/to/cover-image.png \
  --content-file /absolute/path/to/content.html \
  --title "Article Title" \
  --author "Author Name" \
  --digest "Optional digest"
```

GitHub Release mode (auto-download executable):

```bash
export MP_WECHAT_GITHUB_REPO="owner/repo"
export MP_WECHAT_RELEASE_TAG="latest"
bash scripts/publish_draft.sh \
  --cover-image /absolute/path/to/cover-image.png \
  --content-file /absolute/path/to/content.html \
  --title "Article Title"
```

Direct URL mode:

```bash
export MP_WECHAT_RELEASE_URL="https://github.com/Mesus/weixin-mp-skill/releases/download/v0.0.1/mp-weixin-skill.zip"
bash scripts/publish_draft.sh \
  --cover-image /absolute/path/to/cover-image.png \
  --content-file /absolute/path/to/content.html \
  --title "Article Title"
```

If `uploadCoverImage` response does not include usable `media_id`, pass it explicitly:

```bash
bash scripts/publish_draft.sh \
  --bin /absolute/path/to/mp-weixin-skill \
  --article-image /absolute/path/to/article-image.png \
  --cover-image /absolute/path/to/cover-image.png \
  --content-file /absolute/path/to/content.html \
  --title "Article Title" \
  --thumb-media-id "YOUR_MEDIA_ID"
```

## Output Contract

Script prints one JSON object on stdout:

- `access_token`: token returned by `getAuth`
- `article_image_url`: URL returned by `uploadArticleImage`
- `cover_upload`: raw JSON object returned by `uploadCoverImage`
- `thumb_media_id_used`: value passed to `addDraft`
- `draft`: raw JSON object returned by `addDraft`

On failure, script prints JSON error to stderr and exits non-zero.

## Resource

- CLI wrapper implementation details: `references/cli-contract.md`
