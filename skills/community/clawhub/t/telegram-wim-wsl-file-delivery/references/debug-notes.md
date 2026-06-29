# Debug notes

Observed successful sequence during local OpenClaw testing:

1. `MEDIA:/absolute/path/to/report.html` failed.
2. `message` tool send failed because the generated tool payload carried poll fields; Gateway rejected it with `Poll fields require action "poll"`.
3. CLI send from `/absolute/path/to/report.html` reached Gateway but failed with `hostReadCapability permits only validated plain-text documents and trusted generated HTML reports for local reads`.
4. Reading `dist/web-media-*.js` showed local HTML is accepted only when `isTrustedGeneratedHostReadHtmlPath()` returns true, meaning the file must be under the preferred OpenClaw tmp dir and have valid HTML document shape.
5. Copying HTML to `/tmp/openclaw/report.html` and sending via CLI succeeded.
6. `.tar.gz` archive sent directly because archive MIME is allowed.

Successful commands:

```bash
mkdir -p /tmp/openclaw
chmod 700 /tmp/openclaw || true
cp /absolute/path/to/report.html /tmp/openclaw/report.html
chmod 600 /tmp/openclaw/report.html
openclaw message send --channel telegram --target <target> --message "HTML report" --media /tmp/openclaw/report.html --force-document
openclaw message send --channel telegram --target <target> --message "Report archive" --media /absolute/path/to/report.tar.gz --force-document
```
