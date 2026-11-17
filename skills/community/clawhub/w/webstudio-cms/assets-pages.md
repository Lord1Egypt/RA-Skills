# Webstudio Pages, Folders & Assets

## Pages

Pages are defined in the `pages` column of the `Build` row. The page tree is a
single root folder plus a flat `pages` array:

```js
// pages structure
{
  homePageId: '<root folder id>',
  rootFolderId: 'root',
  pages: [
    { id, name, title: JSON.stringify(title), rootInstanceId, path, meta: {} },
  ],
  folders: [
    { id: 'root', name: 'Root', slug: '', children: ['<pageId>', ...] },
  ],
}
```

- `rootInstanceId` points at the page's top `body`/`Body` instance.
- Each page's path is its URL (`/`, `/about`, `/projects`).
- `folders[0].children` lists the page ids (the order shown in the builder).

When you add a page:
```js
build.pages.pages.push({ id, name, title: JSON.stringify(title), rootInstanceId, path, meta: {} })
build.pages.folders[0].children.push(id)
```

## Folders

Nested folders are allowed in the tree, but the standard setup is a single `root`
folder holding all pages. If you create subfolders, mirror the shape of `root` with
`children` arrays of page or folder ids. Keep it simple unless the site needs
organization.

## Page-level content

Page-level defaults (background, body font, text color) go on the page root
instance (`page.rootInstanceId`), not on individual elements. See `styling.md`.

## Assets (images, files)

**Assets are NOT stored in Postgres.** The bytes live in MinIO (S3-compatible, at
`:9000`); Postgres only stores metadata.

### Metadata tables

- `Asset` - `{id, projectId, name, filename, folderId, description}`
- `AssetFileMetadata` - `{projectId, assetId, revision, document(jsonb)}` (per-revision)
- `File` - `{name, format, size, meta, status(UploadStatus)}` (upload staging)
- `AssetFolder` - `{projectId, ...}`

### Storage backend

MinIO at `minio:9000`, bucket `webstudio-assets` (created by `minio-init`). The app
writes/reads asset bytes via `S3_ENDPOINT` / `S3_*` env vars. The uploads volume is
mounted at `/app/public/s/uploads`.

To add an asset programmatically you either:
1. **Upload through the builder UI** (drag/drop into the Assets panel), which writes
   the byte to MinIO and creates the `Asset` metadata row, or
2. **Write the `Asset` row + push the file to MinIO directly** (via `mc` or the S3
   API) for full control.

### Referencing an asset in a build

An image element uses a prop (e.g. `src`) pointing at the asset. The asset must be
referenced by its id/URL in the element's props. A broken `src` means the Asset row
or the MinIO object is missing - check both.

## Common gotchas

- **Assets don't survive a DB-only restore.** The bytes are in MinIO; back up the
  `uploads`/`minio-data` volumes too.
- **`MAX_ASSETS_PER_PROJECT`** (default 50) caps assets per project via env var.
- **Global root children don't publish** - see `publishing.md`. Put site-wide
  fonts/imports in a `<style>` HtmlEmbed inside each page body, not in a global root
  element.
- **Don't hardcode asset ids** across builds; resolve them from the `Asset` table by
  name/filename when you need them.
