# Notion file upload flow for image-backed archive items

Use this reference when the target backend is Notion and the library schema includes a `files` property such as `Image`.

## Goal

Attach the original image to the Notion record without relying on ad-hoc public hosting.

## Principles

- Prefer Notion-native file upload over third-party or public temporary hosting.
- Do not upload user images to random public file hosts unless the user explicitly asks for that behavior.
- If native file upload fails, keep the metadata record and report image attachment as pending or unsupported.

## Recommended flow

1. Create the page record first with metadata.
2. Create a Notion file upload object.
3. Upload the local image file to the provided send endpoint using multipart form data.
4. Confirm the upload status is usable rather than `pending`.
5. Patch the page `files` property with the uploaded file object.
6. Return success only when both metadata and file attachment are complete; otherwise report partial success.

## API checkpoints

Typical sequence:

1. `POST /v1/file_uploads`
2. `POST /v1/file_uploads/{id}/send`
3. `GET /v1/file_uploads/{id}` to confirm status
4. `PATCH /v1/pages/{page_id}` with the `files` property referencing the uploaded file

## Confirmed request shape

For the `send` step, use:
- `Authorization: Bearer <NOTION_API_KEY>`
- `Notion-Version: 2025-09-03`
- multipart form field named `file`

A working curl shape is:

```bash
curl -X POST "$UPLOAD_URL" \
  -H "Authorization: Bearer $NOTION_KEY" \
  -H "Notion-Version: 2025-09-03" \
  -F "file=@/path/to/image.jpg"
```

After upload, confirm the file upload object reports `status: uploaded` before attaching it to the page.

When patching the page `files` property, reference the uploaded object by `file_upload.id`.

## Validation rule

Do not claim the image is attached until the file upload object is no longer pending and the page property reflects the uploaded file.

## Fallback behavior

If file upload is not supported or fails:
- preserve the metadata record,
- mark the result as partial success,
- state clearly that the image itself was not attached,
- avoid silently substituting a temporary public URL.
