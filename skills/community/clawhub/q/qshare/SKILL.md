---
name: qshare
description: Share one local file through a public download URL or QR code using CNB uploads by default, with 3-day retention and immediate manual deletion, or an optional TryCloudflare tunnel.
metadata:
  openclaw:
    homepage: https://github.com/steinvenic/qshare
    requires:
      bins:
        - qshare
    install:
      - id: uv
        kind: uv
        package: qshare
        bins:
          - qshare
        label: Install qshare from PyPI (uv)
---

# qshare

Use this skill when the user asks to make one local file available through a public
download URL or QR code. qshare uploads to a CNB Release by default. Files kept in
CNB are stored for 3 days by default, and the current upload can be manually deleted
immediately at the post-upload prompt. Only the CNB channel supports deleting
uploaded files. Add `--cf` when the user chooses to serve the file from their own
machine through a temporary TryCloudflare tunnel.

## Default channel: CNB

1. Resolve the exact local file path. If the user has not identified one file,
   ask for the path instead of sharing a directory or guessing a filename.
2. Explain that the file will be uploaded to CNB, that kept uploads have a default
   3-day retention, and that the resulting public URL has no access control.
   Recommend encrypting private or sensitive files before sharing them. Honor
   existing authorization to share this file; clarify the channel if the user
   requires sharing without remote storage.
3. Run qshare with the path quoted so spaces and shell metacharacters are safe:

   ```bash
   qshare "/path/to/file.zip"
   ```

   `--cnb` explicitly selects the same default channel. The upload starts
   immediately without a pre-upload confirmation. `--ttl` and `--port` apply
   only to `--cf`; they do not change CNB retention.
4. Handle the post-upload deletion prompt according to the user's intent:
   - To leave a working download link, answer `n` to keep the file. CNB stores
     kept files for 3 days by default; qshare and the local machine can stop
     after upload without ending the download link.
   - The user can manually delete this upload immediately by pressing Enter or
     answering `y`. Enter is the default **delete** answer, not a keep answer.
     Leave the prompt open while the recipient downloads if the user wants to
     delete the file as soon as the transfer finishes. Confirm deletion only
     when requested or authorized; do not pipe a blank answer automatically.
   - Deletion affects the CNB copy, never the local source file. After successful
     deletion, the download URL and QR code are invalid, and Windows skips the
     browser QR question. Do not return a deleted upload's URL as a working link.
5. Report the line labelled `PUBLIC FILE URL` exactly as printed for a kept upload,
   along with the default 3-day retention. A QR renderer failure does not invalidate
   a successfully printed URL. Check deletion errors before claiming the remote
   file was removed; a successful process exit alone does not prove deletion.

Do not expose arbitrary local paths, directory listings, or additional files.
Do not promise permanent CNB storage or access control.

## Optional channel: TryCloudflare

Use `--cf` when the user chooses a tunnel, including requests to share without
storing the file in CNB:

```bash
qshare "/path/to/file.zip" --cf
qshare "/path/to/file.zip" --cf --ttl 30m
```

The file is served from the local machine. The tunnel's default lifetime is
2 hours; `--ttl` accepts `30m`, `90s`, `2h`, or a positive number of seconds.
Use `--port PORT` only when a fixed local port is needed. Report `PUBLIC FILE URL`
exactly as printed. The URL stops working when the TTL expires or the tunnel is
stopped. Keep the serving process running while the recipient needs access.

The `--cf` channel has no CNB upload or remote-file deletion action; stop the
tunnel to end sharing. The local source file stays intact. Do not describe CNB's
3-day retention or deletion prompt as applying to `--cf`, and do not claim that a
TryCloudflare share is persistent or access-controlled.

## Operational notes

- On Unix-like systems `--cf` may offer to detach into the background. Only
  choose that mode when the user asks for background operation; Windows remains
  in the foreground.
- On Windows, a kept CNB upload or an active `--cf` share offers a browser QR
  page after the other prompts (open by default); answer according to the user's
  preference. A deleted CNB upload must not open a QR page for an invalid link.
- `--cf` installs or uses a matching `cloudflared` binary as documented by the
  package. Do not download an unrelated binary or weaken TryCloudflare URL
  validation to work around an error.
- If qshare reports an error, show the actionable error text and do not invent a
  URL. Never print credentials or tokens from the runtime environment.
