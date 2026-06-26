---
title: Always Close the Filesystem Handle Returned by NewFilesystem
impact: HIGH
impactDescription: Leaked filesystem clients keep S3 connections and file descriptors open until the process exits
tags: filesystem, extending, files, s3, NewFilesystem, close
---

## Always Close the Filesystem Handle Returned by NewFilesystem

`app.NewFilesystem()` (Go) and `$app.newFilesystem()` (JS) return a filesystem client backed by either the local disk or S3, depending on the app settings. **The caller owns the handle** and must close it - there is no finalizer and no automatic pooling. Leaking handles leaks TCP connections to S3 and file descriptors on disk, and eventually the server will stop accepting uploads.

PocketBase also ships a second client: `app.NewBackupsFilesystem()` for the backups bucket/directory, with the same ownership rules.

**Incorrect (no close, raw bytes buffered in memory):**

```go
// ❌ Forgets to close fs - connection leaks
func downloadAvatar(app core.App, key string) ([]byte, error) {
    fs, err := app.NewFilesystem()
    if err != nil {
        return nil, err
    }
    // ❌ no defer fs.Close()

    // ❌ GetFile loads the whole file into a reader; reading it all into a
    //    byte slice defeats streaming for large files
    r, err := fs.GetFile(key)
    if err != nil {
        return nil, err
    }
    defer r.Close()
    return io.ReadAll(r)
}
```

**Correct (defer Close, stream to the HTTP response):**

```go
func serveAvatar(app core.App, key string) echo.HandlerFunc {
    return func(e *core.RequestEvent) error {
        fs, err := app.NewFilesystem()
        if err != nil {
            return e.InternalServerError("filesystem init failed", err)
        }
        defer fs.Close() // REQUIRED

        // Serve directly from the filesystem - handles ranges, content-type,
        // and the X-Accel-Redirect / X-Sendfile headers when available
        return fs.Serve(e.Response, e.Request, key, "avatar.jpg")
    }
}

// Uploading a local file to the PocketBase-managed filesystem
func importAvatar(app core.App, record *core.Record, path string) error {
    f, err := filesystem.NewFileFromPath(path)
    if err != nil {
        return err
    }
    record.Set("avatar", f) // assignment + app.Save() persist it
    return app.Save(record)
}
```

```javascript
// JSVM - file factories live on the $filesystem global
const file1 = $filesystem.fileFromPath("/tmp/import.jpg");
const file2 = $filesystem.fileFromBytes(new Uint8Array([0xff, 0xd8]), "logo.jpg");
const file3 = $filesystem.fileFromURL("https://example.com/a.jpg");

// Assigning to a record field triggers upload on save
record.set("avatar", file1);
$app.save(record);

// Low-level client - MUST be closed
const fs = $app.newFilesystem();
try {
    const list = fs.list("thumbs/");
    for (const obj of list) {
        console.log(obj.key, obj.size);
    }
} finally {
    fs.close(); // REQUIRED
}
```

**Rules:**
- `defer fs.Close()` **immediately** after a successful `NewFilesystem()` / `NewBackupsFilesystem()` call (Go). In JS, wrap in `try { ... } finally { fs.close() }`.
- Prefer the high-level record-field API (`record.Set("field", file)` + `app.Save`) over direct `fs.Upload` calls - it handles thumbs regeneration, orphan cleanup, and hook integration.
- File factory functions (`filesystem.NewFileFromPath`, `NewFileFromBytes`, `NewFileFromURL` / JS `$filesystem.fileFromPath|Bytes|URL`) capture their input; they do not stream until save.
- `fileFromURL` performs an HTTP GET and loads the body into memory - not appropriate for large files.
- Do not share a single long-lived `fs` across unrelated requests; the object is cheap to create per request.

Reference: [Go Filesystem](https://pocketbase.io/docs/go-filesystem/) · [JS Filesystem](https://pocketbase.io/docs/js-filesystem/)
