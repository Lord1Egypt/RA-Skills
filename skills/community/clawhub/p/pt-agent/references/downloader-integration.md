# Downloader Integration Reference

Use this reference when adding downloader configuration, torrent handoff, downloader health checks, status queries, or queue control.

## Supported Client Pattern

Start with qBittorrent and Transmission because they expose stable HTTP/RPC APIs.

Downloader config should contain:

- `id`, `type`, `baseUrl`, and optional proxy binding.
- Secret references for username/password/token, not raw secret values.
- Default category or label.
- Default save path.
- Add mode: start immediately, add paused, or follow downloader default.
- Duplicate handling: skip, reannounce, or let client decide.

## Configuration Flow

1. Validate `type`, `baseUrl`, credential reference, default category/label, save path, tags, and add-paused policy.
2. Normalize endpoint URLs without logging usernames, passwords, or tokens.
3. Keep TLS certificate and hostname verification enabled for HTTPS endpoints, then run a health check before saving as enabled.
4. Store detected version and supported features as cacheable non-secret metadata.
5. Keep credentials in a secret store or environment-variable reference.

## Add Torrent Flow

1. When the user selects a result, immediately run `download-torrent --start` against the default downloader. Do not ask for confirmation and do not require a dry-run gate for ordinary single-result downloads.
2. Use `--paused` only when the user explicitly asks to queue without starting.
3. Resolve the tracker result into a `.torrent` download URL or magnet.
4. Fetch using the authenticated tracker session or browser profile.
5. Keep the torrent bytes in memory or a temporary ignored path.
6. Submit to downloader with category, save path, start-by-default (or paused when requested), and tags.
7. Delete temporary torrent files after successful handoff.
8. Treat `status=already_present` as success: report current progress/state and do not re-add.
9. If a selected download is already present but paused and the user asked to start, the runtime should resume it and return `status=resumed`.
10. If add fails as `downloader_add_failed`, report the runtime error directly; do not invent ad hoc qBittorrent scripts.
11. If the user later asks to start a paused torrent by hash/name, call `resume-torrents` instead of re-fetching the torrent.
12. Record a run history entry without cookies, passkeys, torrent bytes, or private URLs.

## Status Flow

Return a normalized status object:

```ts
type DownloaderStatus = {
  downloaderId: string;
  healthy: boolean;
  type: "qbittorrent" | "transmission";
  version?: string;
  freeSpaceBytes?: number;
  downloadRateBytesPerSec?: number;
  uploadRateBytesPerSec?: number;
  counts: {
    active?: number;
    downloading?: number;
    uploading?: number;
    paused?: number;
    checking?: number;
    errored?: number;
    completed?: number;
  };
  lastCheckedAt: string;
  error?: { code: string; message: string };
};
```

Handle unreachable, unauthorized, unsupported version, and malformed response as separate error codes. Cache status briefly if the UI polls frequently.

## qBittorrent Notes

- Use `/api/v2/auth/login` for session auth when needed.
- Use `/api/v2/torrents/add` with multipart form data for `.torrent` files.
- Use `/api/v2/app/version`, `/api/v2/sync/maindata`, `/api/v2/torrents/info`, and `/api/v2/transfer/info` for status where available.
- Validate category and save path before adding when the app maintains a known mapping.
- Treat HTTP 200 with text responses carefully; qBittorrent may return textual errors.

## Transmission Notes

- Use the RPC endpoint and handle `X-Transmission-Session-Id` negotiation.
- Use base64 torrent metainfo for `.torrent` bytes or `filename` for magnet/URL.
- Set `paused`, `download-dir`, and labels if supported by the target version.
- Use `session-get` and `torrent-get` for version, speed, free-space support, and queue counts.

## Safety Checks

- Never log full add URLs for private tracker downloads.
- Redact passkey-like query parameters before persistence.
- Confirm the downloader endpoint is local or explicitly trusted.
- Provide dry-run mode for filter rules and bulk add workflows.
