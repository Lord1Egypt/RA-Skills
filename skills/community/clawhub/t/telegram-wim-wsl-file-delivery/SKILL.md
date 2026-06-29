---
name: telegram-wim-wsl-file-delivery
description: "Deliver local reports and artifacts through OpenClaw chat channels. Use when a generated HTML/PDF/archive/table or other local file must be sent from a local, self-hosted, or WSL OpenClaw setup where path handling and host-read policy matter."
metadata: {"openclaw":{"requires":{"bins":["openclaw","file","cp","chmod","mkdir","node","ls"]}}}
license: "MIT-0"
---

# Telegram Wim-WSL File Delivery

Use for file delivery from the local filesystem into an OpenClaw message channel.

Prefer this skill when the hard part is not Telegram itself, but the path from local disk -> OpenClaw host-read -> channel send.

## Workflow

### 1. Confirm the outbound send

Treat file delivery as an external action.

If the user did not explicitly ask to send the file, confirm:

- exact file path;
- destination channel/target;
- risk: file contents leave the machine;
- rollback: delete the sent message if supported, or send a corrected file.

If the user already asked to send it, continue.

### 2. Verify the file and use an absolute path

Never send `~`, relative paths, or guessed paths.

```json
{
  "tool": "exec",
  "command": "ls -lh /absolute/path/to/file && file /absolute/path/to/file"
}
```

Check:

- file exists;
- size is plausible for the channel/path;
- MIME/type matches the intended delivery format.

### 3. Choose the send path

Use these defaults:

- PDF / ZIP / TAR / GZIP / CSV / JSON / TXT / MD / YAML -> send directly
- HTML report -> copy to trusted OpenClaw tmp first
- image / audio / video artifacts -> send directly, add `--force-document` if compression must be avoided

### 4. Handle local HTML through trusted tmp

On some local/self-hosted OpenClaw setups, ordinary local HTML from arbitrary workspace paths is rejected by host-read policy.

Resolve or assume the trusted tmp directory, then copy HTML there before sending.

If needed, resolve the preferred tmp path:

```json
{
  "tool": "exec",
  "command": "node -e \"import('/usr/lib/node_modules/openclaw/dist/tmp-openclaw-dir-C60hWKdY.js').then(m=>console.log(m.n()))\""
}
```

Typical copy flow:

```json
{
  "tool": "exec",
  "command": "set -euo pipefail\nSRC=/absolute/path/report.html\nTMP=/tmp/openclaw\nmkdir -p \"$TMP\"\nchmod 700 \"$TMP\" || true\ncp \"$SRC\" \"$TMP/report.html\"\nchmod 600 \"$TMP/report.html\"\nls -lh \"$TMP/report.html\"\nfile \"$TMP/report.html\""
}
```

Send the tmp copy, not the original HTML.

### 5. Prefer the OpenClaw CLI when wrapper sends misbehave

If a wrapper/tool path injects bad fields or fails ambiguously, stop retrying the same path. Use the documented CLI.

Read the local CLI doc if needed:

```json
{
  "tool": "read",
  "path": "/usr/lib/node_modules/openclaw/docs/cli/message.md"
}
```

Typical Telegram sends:

```json
{
  "tool": "exec",
  "command": "openclaw message send --channel telegram --target <target> --message \"HTML report\" --media /tmp/openclaw/report.html --force-document"
}
```

```json
{
  "tool": "exec",
  "command": "openclaw message send --channel telegram --target <target> --message \"Report archive\" --media /absolute/path/to/report.tar.gz --force-document"
}
```

For other channels, keep the same shape and adjust `--channel` and `--target` according to the CLI docs.

### 6. Verify the result

Report the concrete send result or message id.

For report bundles, prefer this order:

1. primary report (`.html` / `.pdf`)
2. archive bundle (`.tar.gz` / `.zip`)
3. optional table (`.csv` / `.tsv`)

## Error handling

- `Poll fields require action "poll"`
  - Meaning: wrapper/path built the send payload incorrectly.
  - Fix: switch to `openclaw message send ...` or a truly minimal send path.

- `hostReadCapability permits only validated plain-text documents and trusted generated HTML reports for local reads`
  - Meaning: local HTML/text path was rejected by host-read policy.
  - Fix: for HTML, copy to `/tmp/openclaw` and send that copy.

- `Message: ~/path failed`
  - Meaning: path resolution or policy failed.
  - Fix: expand `~` to an absolute path; for HTML use trusted tmp.

- `Host-local media sends require buffer-verified media/document types`
  - Meaning: MIME fallback was not enough.
  - Fix: use a standard extension/type, verify with `file`, or archive the artifact.

- Telegram compresses media
  - Meaning: channel treated the file as image/video media.
  - Fix: add `--force-document`.

- Archive too large
  - Meaning: channel/gateway/path size limit.
  - Fix: split the archive, send the report first, or choose another route.

Never loop on the same failing command. Change one variable, retry once.

## Known pain points

- HTML is the most fragile class: prefer `/tmp/openclaw/...` and valid HTML document shape.
- Local `MEDIA:/...` paths may fail even when the file exists.
- `~` and relative paths are risky; use absolute paths.
- Plain-text files can fail on bad encoding, binary-ish content, or weak MIME detection.
- Safest fallback: archive the artifact as `.zip` or `.tar.gz` and send as document.

## References

- `references/debug-notes.md` - anonymized failure sequence and working commands
- `references/positioning.md` - audience and differentiation
- `references/comparison-notes.md` - what this skill adds beyond generic Telegram senders
- `examples/send-html-report.sh`
- `examples/send-archive.sh`
