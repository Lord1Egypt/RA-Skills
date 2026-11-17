# Windows ZIP entries and CDN-aware public verification

## Windows-style ZIP entry names

Some source archives encode every entry with `\` separators (for example `Project\dist\client\assets\app.js`). On Linux, `zipfile` and common extraction tools may treat those as literal filename characters instead of directories.

Before extracting such an archive for **local inspection only**:

1. Convert `\` to `/` in every entry name in memory.
2. Reject an entry if its normalized form is absolute, contains `..`, contains a drive-qualified first segment, is a symlink, or collides with another normalized entry.
3. Extract only after all entries pass those checks.
4. Never upload the source archive itself. Build the final `site/` release from browser-consumed output only.

This is a safe path-normalization step, not permission to accept traversal or ambiguous archives.

## CDN-aware public verification

A release CDN may inject analytics markup into `text/html` (for example a Cloudflare beacon), which can legitimately change the returned HTML byte count and SHA-256 after publication.

Verification policy:

- Require the deployment service to validate the submitted manifest before release.
- On the public URL, require `200`, `text/html`, non-empty content, and an expected application marker in `index.html`.
- Treat a public HTML hash mismatch as an investigation item; identify whether the only delta is CDN injection before declaring a deployment failure.
- For every non-HTML manifest file, require public `200`, expected content type, and byte/SHA match.
- Independently request every dynamically referenced image and release-relative JS/CSS asset; URL-encode path segments when names contain spaces or reserved characters.
