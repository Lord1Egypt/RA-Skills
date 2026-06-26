# CLI Contract

Wrapper script: `scripts/publish_draft.sh`

## Fixed Execution Order

1. `getAuth`
2. `uploadArticleImage --token <access_token> --path <article_image>`
3. `uploadCoverImage --token <access_token> --path <cover_image>`
4. `addDraft --token <access_token> --title ... --author ... --content-file ... --digest ... --thumb-media-id ...`

## getAuth Prerequisite

- Local file `~/.weixin_credentials` must exist
- File content format:
  - `appid=YOUR_APP_ID`
  - `secret=YOUR_APP_SECRET`

## Wrapper Args

- `--bin`: executable path (optional if auto-download is configured)
- `--repo`: GitHub repo `owner/repo` for auto-download (or env `MP_WECHAT_GITHUB_REPO`)
- `--tag`: release tag (or env `MP_WECHAT_RELEASE_TAG`, default `latest`)
- `--asset`: release asset name override (or env `MP_WECHAT_ASSET_NAME`)
- `--url`: direct release asset URL (or env `MP_WECHAT_RELEASE_URL`, supports zip or binary)
- `--article-image`: local image path for article image upload
- `--cover-image`: local image path for cover upload
- `--content-file`: local article content file path
- `--title`: draft title
- `--author`: optional author
- `--digest`: optional digest
- `--thumb-media-id`: optional override value used in `addDraft`

## Thumb Media Fallback Rule

If `--thumb-media-id` is not provided, wrapper tries:

1. `uploadCoverImage` response `media_id` or `mediaId`
2. `uploadCoverImage` response `url`

If neither exists, wrapper fails with clear error.

## Error Handling

- Any subcommand non-zero exit causes immediate failure.
- Non-JSON stdout is tolerated if the final line is JSON.
- Final wrapper error is emitted as JSON to stderr:
  - `{"error": "..."}`

## GitHub Release Download

If local binary is missing and `--repo` or `MP_WECHAT_GITHUB_REPO` is provided, wrapper calls:

- `scripts/install_mp_weixin_skill.sh`

and installs executable to:

- `<skill>/bin/mp-weixin-skill`

It can download from:
- direct URL (`--url` / `MP_WECHAT_RELEASE_URL`)
- GitHub release API (`--repo` + optional `--tag/--asset`)
