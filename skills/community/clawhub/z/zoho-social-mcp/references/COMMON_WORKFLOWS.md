# Verified Zoho Social MCP Workflows

Step-by-step procedures for frequent Social tasks. All operations assume `mcporter` and a configured `ZOHO_SOCIAL_MCP_URL`. Inspect the live tool schema with `mcporter list` before the first write.

Portal IDs, brand IDs, channel IDs, and media file IDs are opaque. Never invent them. Resolve them through lookup tools first.

An empty portal list or `USER_INACTIVE_IN_PORTAL` means the authenticated Zoho user has no Social workspace access. Stop. Do not guess IDs and do not switch to another customer's MCP endpoint.

## 1. Resolve portal, brand, and channels

```text
getSocialPortals -> getSocialBrands -> getSocialChannels
```

1. List portals with `getSocialPortals`. Use the portal `id`.
2. List brands with `getSocialBrands` and header `portal_id`.
3. List channels with `getSocialChannels` and headers `portal_id` plus `brand_id`.
4. Confirm the target network and channel IDs with the user before writing.

```bash
python3 scripts/list_portals.py
python3 scripts/list_brands.py --portal-id <portal_id>
python3 scripts/list_channels.py --portal-id <portal_id> --brand-id <brand_id>
```

## 2. Upload an image, then confirm it

```text
uploadSocialMedia / uploadSocialMediaFromUrl -> getSocialMediaLibrary
```

Local files: read bytes with `scripts/upload_media.py --file`. The helper encodes a complete `data:image/...;base64,...` payload. Do not paste base64 into chat.

Remote images: `scripts/upload_media.py --image-url https://...`

Then re-list:

```bash
python3 scripts/list_media.py --portal-id <portal_id> --brand-id <brand_id>
```

Treat empty `file_path` as failure even when `status` is `success`. The live upload ID arrives in `file_path`. Re-list the library, then use that ID in `media_input` when creating a draft or schedule.

`uploadSocialMedia` also documents a multipart/form-data mode. The JSON/base64 mode is the one MCP actually carries. Live evidence: a real PNG returns `file_path` and appears in the library; a degenerate 1x1 PNG returns empty fields and never appears. File a GitHub issue immediately if a later live upload reports success with empty `file_path`. Do not add a GitHub wrapper script.

[zoho-attachment-bridge](https://github.com/sprintberlin/zoho-attachment-bridge) remains the companion for Zoho apps whose MCP upload tools drop binary parameters. Social images stay in this skill.

## 3. Draft a post

```text
getSocialChannels -> upload media if needed -> validateSocialPost -> createSocialDraft -> getSocialDraft
```

1. Resolve channels.
2. Upload media first when the post includes images.
3. Call `validateSocialPost` with the exact post body. Do not create the draft if validation reports errors.
4. Create the draft with `createSocialDraft` (`type=6`).
5. Read it back with `getSocialDraft` or `scripts/inspect_post.py <id> --kind draft`.

Never publish as a side effect of drafting.

## 4. Schedule or publish

```text
validateSocialPost -> createSocialSchedule / publishSocialPost -> getSocialSchedule / getPublishStatus
```

1. Validate the exact post body again.
2. Schedule with `createSocialSchedule` or publish immediately with `publishSocialPost`.
3. Read the result back. For a live publish, check `getPublishStatus`.
4. List the queue with `scripts/list_schedules.py`.

Keep `deleteSocialSchedule` disabled unless the task explicitly requires it.

## 5. Inspect published content

```text
getSocialPublishedPosts -> getSocialPublishedPostDetail -> getSocialPostActivities
```

```bash
python3 scripts/list_published.py --portal-id <portal_id> --brand-id <brand_id> --network linkedin
python3 scripts/inspect_post.py <post_id> --kind published --network linkedin --portal-id <portal_id> --brand-id <brand_id>
```
