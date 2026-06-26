# Feishu Document Creation — Recipe Guide

Step-by-step API calls for creating a weekly menu Feishu document with images.

## 1. Get Tenant Access Token

```bash
curl -s -X POST "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal" \
  -H "Content-Type: application/json" \
  -d '{"app_id":"<APP_ID>","app_secret":"<APP_SECRET>"}'
```

Read `app_id` and `app_secret` from `~/.openclaw/openclaw.json` → `channels.feishu.accounts.default`.

## 2. Create Document

```bash
curl -s -X POST "https://open.feishu.cn/open-apis/docx/v1/documents" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title":"🍽️ YYYY-MM-DD 推荐菜单","folder_token":"<RECEIPTS_FOLDER>"}'
```

Receipts folder token: check MEMORY.md for `receipts 文件夹 token`.

## 3. Grant User Permission

```bash
curl -s -X POST "https://open.feishu.cn/open-apis/drive/v1/permissions/<DOC_TOKEN>/members?type=docx" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"member_type":"openid","member_id":"<USER_OPEN_ID>","perm":"full_access"}'
```

## 4. Insert Text Blocks

POST to `/docx/v1/documents/<DOC>/blocks/<DOC>/children?document_revision_id=-1`

Block types:
- `2` — text: `{"block_type":2,"text":{"elements":[{"text_run":{"content":"...","text_element_style":{}}}],"style":{}}}`
- `4` — heading2: `{"block_type":4,"heading2":{"elements":[...],"style":{}}}`
- `5` — heading3: `{"block_type":5,"heading3":{"elements":[...],"style":{}}}`
- `17` — todo: `{"block_type":17,"todo":{"elements":[...],"style":{"done":false}}}`
- `22` — divider: `{"block_type":22,"divider":{}}`
- `27` — image (empty): `{"block_type":27,"image":{}}`

**Max 50 blocks per request.** Split into batches if needed.

### Link element

```json
{"text_run":{"content":"link text","text_element_style":{"link":{"url":"https://..."}}}}
```

### Bold element

```json
{"text_run":{"content":"bold text","text_element_style":{"bold":true}}}
```

## 5. Insert Images (3-step process)

### Step A: Create empty image block

Include `{"block_type": 27, "image": {}}` in the children batch. Note the returned `block_id`.

### Step B: Upload image to drive

```bash
curl -s -X POST "https://open.feishu.cn/open-apis/drive/v1/medias/upload_all" \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@<LOCAL_PATH>" \
  -F "file_name=<FILENAME>" \
  -F "parent_type=docx_image" \
  -F "parent_node=<IMAGE_BLOCK_ID>" \
  -F "size=<FILE_SIZE_BYTES>"
```

Returns `file_token`.

### Step C: Patch image block

```bash
curl -s -X PATCH "https://open.feishu.cn/open-apis/docx/v1/documents/<DOC>/blocks/<BLOCK_ID>?document_revision_id=-1" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"replace_image":{"token":"<FILE_TOKEN>"}}'
```

**Rate limit:** sleep 0.4s between each edit operation. Max 3 edits/second per document.

## 6. Delete a Document

```bash
curl -s -X DELETE "https://open.feishu.cn/open-apis/drive/v1/files/<DOC_TOKEN>?type=docx" \
  -H "Authorization: Bearer $TOKEN"
```

## 7. Move a Document

```bash
curl -s -X POST "https://open.feishu.cn/open-apis/drive/v1/files/<DOC_TOKEN>/move" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"type":"docx","folder_token":"<TARGET_FOLDER>"}'
```

## Common Gotchas

- Document title (page block type 1) **cannot be renamed via API** after creation — get it right at create time
- Image blocks **cannot** be created with a token — must create empty then patch
- XiaoHongShu CDN images return 403 if downloaded directly — use alternative image sources
- `heading2`/`heading3` keys must match block_type (4→heading2, 5→heading3), NOT `text`
