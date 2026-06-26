---
name: qshell-copilot
description: >
  Manage files on Qiniu Cloud Storage (Kodo) via the qshell CLI tool: upload, download, list, delete, copy, move files,
  CDN refresh/prefetch, and bucket management. Use this skill whenever the user mentions Qiniu, qiniu, qshell, Kodo,
  uploading to cloud storage, CDN operations, object storage buckets, or managing remote files on Qiniu's platform.
  Also trigger when the user asks to transfer local files to a Chinese cloud storage provider, fetch remote URLs into
  a storage bucket, generate private download links, or batch-upload a directory. Even if the user simply says
  "upload this to my bucket" or "list my cloud files" in a context where Qiniu is the configured provider, use this skill.
---

# Qiniu Cloud Storage Management (qshell)

This skill wraps the `qshell` CLI to let you manage Qiniu Kodo storage through natural language. It handles prerequisite checks, command selection, and result formatting automatically.

## Pre-flight Checks

Before executing any storage operation, run these checks in order. The reason for checking every time is that qshell state can change between sessions (uninstalled, credentials expired), and failing silently leads to confusing errors.

### 1. Installation Check

```bash
qshell --version
```

If this fails, the user doesn't have qshell installed. Stop and guide them through installation (see `references/install-guide.md`).

### 2. Authentication Check

```bash
qshell user ls
```

If the output is empty or shows an error, the user needs to configure credentials:
```bash
qshell account <AccessKey> <SecretKey> <Name>
```
Direct them to [Qiniu Key Management](https://portal.qiniu.com/user/key) to get their AK/SK.

### 3. Proceed with the Request

Once both checks pass, execute the user's request using the command reference below.

## Command Reference

### Uploading Files

Choose the upload method based on what the user provides:

- **Single file, under 100MB**: `qshell fput [--overwrite] <Bucket> <Key> <LocalFile>`
- **Single file, 100MB or larger**: `qshell rput [--overwrite] <Bucket> <Key> <LocalFile>` — rput uses resumable upload, so if it fails partway through, re-running the same command resumes from where it left off rather than starting over.
- **Entire directory**: `qshell qupload2 --src-dir=<Dir> --bucket=<Bucket> [--overwrite] [--key-prefix=<Prefix>] [--thread-count=<N>]` — if some files fail during batch upload, qupload2 logs failures to a local file. Re-running the same command retries only the failed files.

To decide which to use: check the file size first (`ls -lh <file>`). If the user points to a directory rather than a file, use `qupload2`.

**Key (remote path) inference**: When the user doesn't specify a remote path, use the local filename as the Key. If they mention a remote directory like `images/`, concatenate it as `images/filename.ext`.

**After a successful upload**: Run `qshell domains <Bucket>` to get the bound domain, then show the user the full access URL: `http(s)://<Domain>/<Key>`. Prefer CDN domains when multiple domains are available.

### Downloading Files

- **Single file**: `qshell get <Bucket> <Key> [-o <SaveAs>]`
- **Batch download**: Requires a config file. See `references/batch-download.md` for the JSON format.

### File Operations

| Operation | Command |
|-----------|---------|
| List files | `qshell listbucket2 <Bucket> [--prefix <P>] [--limit <N>] [--marker <M>]` |
| File info | `qshell stat <Bucket> <Key>` |
| Delete file | `qshell delete <Bucket> <Key>` |
| Copy file | `qshell copy <SrcBucket> <SrcKey> <DstBucket> [-k <DstKey>]` |
| Move/rename | `qshell move <SrcBucket> <SrcKey> <DstBucket> [-k <DstKey>]` |

When listing files, use `--limit 20` by default to keep output manageable. However, if the user explicitly asks for "all" files or a large number, omit the limit or set a high value to respect their intent.

**Before deleting**: Always run `qshell stat` first and show the file details to the user. Wait for explicit confirmation before executing `qshell delete`. This prevents accidental data loss — deleted files in Kodo cannot be recovered without versioning enabled.

### Bucket Management

| Operation | Command |
|-----------|---------|
| List buckets | `qshell buckets` |
| Bucket domains | `qshell domains <Bucket>` |
| Create bucket | `qshell mkbucket <Bucket> --region <Region>` |

Region values: `z0` (East China), `z1` (North China), `z2` (South China), `na0` (North America), `as0` (Southeast Asia), `cn-east-2` (East China - Zhejiang 2)

### CDN and Network

| Operation | Command |
|-----------|---------|
| Fetch URL to bucket | `qshell fetch <URL> <Bucket> <Key>` |
| CDN refresh URLs | `qshell cdnrefresh -i <file>` |
| CDN refresh dirs | `qshell cdnrefresh -r -i <file>` |
| CDN prefetch | `qshell cdnprefetch -i <file>` |
| Private download URL | `qshell privateurl <PublicUrl> [--deadline <timestamp>]` |

## Error Recovery

When a command fails, diagnose and guide the user rather than just showing the raw error:

| Error pattern | What happened | What to do |
|---------------|---------------|------------|
| `no such file or directory` | Local file path is wrong | Help the user verify the path exists |
| `invalid account` / `no auth` | Credentials missing or expired | Re-run `qshell account` |
| `no such bucket` | Bucket name doesn't exist | Run `qshell buckets` to show available ones |
| `file exists` | Remote file already exists | Ask if they want to add `--overwrite` |
| `key doesn't exist` | Remote key not found | Use `qshell listbucket2` to find the correct key |
| `bad token` / `expired token` | Auth token expired | Re-run `qshell account` |
| Network timeout | Connectivity issue | Suggest checking network and retrying |

## Reference Files

- `references/install-guide.md` — Platform-specific installation instructions (Windows, macOS, Linux)
- `references/batch-download.md` — JSON config format for `qdownload` batch downloads

## Examples

**Example 1:**
Input: "Upload ./logo.png to my-bucket"
Steps: Check file size -> `qshell fput my-bucket logo.png ./logo.png` -> `qshell domains my-bucket` -> Return URL

**Example 2:**
Input: "List all jpg files in my-bucket"
Steps: `qshell listbucket2 my-bucket --limit 100` -> Filter results for `.jpg` suffix -> Display

**Example 3:**
Input: "Delete old-file.txt from my-bucket"
Steps: `qshell stat my-bucket old-file.txt` -> Show file info -> Wait for user confirmation -> `qshell delete my-bucket old-file.txt`
