# API Notes

## Product mapping

The WeChat Official Account backend's "发贴图" / image-first posting flow maps to **image-message drafts** created with:
- `article_type = newspic`

This is distinct from normal article drafts:
- `article_type = news`

## API flow used by this skill

1. Get access token
   - `GET /cgi-bin/token`
2. Upload each local image as a permanent image material
   - `POST /cgi-bin/material/add_material?type=image`
3. Create draft
   - `POST /cgi-bin/draft/add`
   - payload uses `article_type: newspic`

## Important payload fields

- `title`
- `content`
- `digest`
- `author`
- `image_info.image_list[].image_media_id`

## Limits / behavior

- Up to 20 images
- First image is the cover image
- Skill is intentionally draft-only
- Final publication should be done manually in the WeChat backend

## Encoding gotcha

Chinese text may become garbled if the request body is not sent explicitly as UTF-8 JSON.

Preferred pattern:
- `json.dumps(payload, ensure_ascii=False).encode('utf-8')`
- `Content-Type: application/json; charset=utf-8`

## Security / publishing hygiene

Do not publish:
- access tokens
- app ids / secrets
- output logs containing real media IDs or remote asset URLs if they are not intended for distribution
- local absolute paths from the author's private workspace
