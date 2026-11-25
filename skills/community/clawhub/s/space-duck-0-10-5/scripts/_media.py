#!/usr/bin/env python3
"""
Space Duck — peck media attachments helper (skill 0.10.0).

INTENT: Move image/file bytes out-of-band (Telegram/WhatsApp pointer model,
        docs/spec/PECK-MEDIA-ATTACHMENTS.md v0.2). The peck envelope carries
        only signature-neutral `attachments[]` refs; the signed proof of the
        media is the 📎[media:<id>:<sha256>:<filename>] manifest line the
        sender appends to the message text (covered by message_hash), which
        doubles as the graceful-degradation fallback old ducks render as text.
CALLS:  POST <api>/beak/media/upload-url and GET <api>/beak/media/<id> —
        Space Duck's own backend; plus the presigned S3 URLs those routes
        return (https://spaceduck-peck-media-<acct>.s3.amazonaws.com/…,
        AWS S3 only). No other third-party hosts are ever contacted.
AUTH:   Beak Key from ~/.space-duck/config.json identifies this duck. The
        server gates every download on the per-media grants set (sender +
        recipients stamped at delivery/approval) — a presigned GET is minted
        only for a granted caller and expires in minutes.
"""
import hashlib, json, re, sys, urllib.error, urllib.request
from pathlib import Path

MEDIA_DIR = Path.home() / '.space-duck' / 'media'
MAX_ATTACHMENTS = 10          # mirrors server MEDIA_MAX_ATTACHMENTS
MAX_BYTES = 26214400          # mirrors server MEDIA_MAX_BYTES (25 MB)
_MEDIA_ID_RE = re.compile(r'^[A-Za-z0-9_-]{8,64}$')
_SHA256_RE = re.compile(r'^[0-9a-f]{64}$')

# Mirror of the server MIME allowlist (lambda MEDIA_MIME_ALLOWLIST) keyed by
# extension so --attach fails locally with a clear message instead of a 400.
_EXT_MIME = {
    '.png': 'image/png', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg',
    '.gif': 'image/gif', '.webp': 'image/webp', '.pdf': 'application/pdf',
    '.txt': 'text/plain', '.md': 'text/markdown', '.markdown': 'text/markdown',
}


def guess_mime(path):
    """Extension→MIME per the server allowlist; '' when unsupported."""
    return _EXT_MIME.get(Path(path).suffix.lower(), '')


def manifest_line(ref):
    """The signed + fallback form of one attachment (spec §3.3). Appended to
    the message text BEFORE hashing, so the v2/v3 signature covers it and a
    pre-0.10 duck still sees an honest text rendering."""
    return (f"\U0001F4CE[media:{ref['media_id']}:{ref['sha256']}:"
            f"{ref.get('filename', '')}]")


PRICING_URL = 'https://spaceduckling.com/pricing.html'   # static fallback


def quota_exceeded_message(name, payload=None):
    """[MEDIA-QUOTA-UPSELL] Owner-facing text for a 429 media_quota_exceeded.
    Uses the server's cap/used/tier/upgrade_url when present (Lambda with the
    upsell fields); older servers get the static fallback wording + URL."""
    p = payload if isinstance(payload, dict) else {}
    cap, used = p.get('cap', p.get('daily_cap')), p.get('used', p.get('used_today'))
    url = p.get('upgrade_url')
    url = url if isinstance(url, str) and url.startswith('https://') else PRICING_URL
    tier = p.get('tier') if isinstance(p.get('tier'), str) else ''
    if isinstance(cap, int) and not isinstance(cap, bool) and cap > 0:
        u = used if isinstance(used, int) and not isinstance(used, bool) and used >= 0 else cap
        detail = f'{u}/{cap} files today' + (f', {tier} tier' if tier else '')
        return (f'--attach {name}: daily media upload quota reached ({detail}) '
                f'— resets midnight UTC. More files/day: {url}')
    return (f'--attach {name}: daily media upload quota reached for this '
            f'duck\'s tier — resets midnight UTC. More files/day: {url}')


def _http_error_payload(e):
    """Parse an HTTPError body as JSON; {} on anything unexpected."""
    try:
        d = json.loads(e.read())
        return d if isinstance(d, dict) else {}
    except Exception:
        return {}


def _api_headers(cfg):
    return {'Content-Type': 'application/json',
            'X-Beak-Key': cfg.get('beak_key', ''),
            'X-Spaceduck-ID': cfg.get('spaceduck_id', '')}


def upload_attachment(cfg, path, target_sdid=''):
    """Upload one local file: mint a presigned PUT via /beak/media/upload-url,
    PUT the bytes, return the attachments[] ref dict. Raises RuntimeError with
    an operator-readable message on any failure — callers treat an attachment
    that cannot ship as a send-stopping error (never silently drop media)."""
    api = cfg.get('api_base', 'https://beak.spaceduckling.com')
    p = Path(path).expanduser()
    if not p.is_file():
        raise RuntimeError(f'--attach {path}: file not found')
    data = p.read_bytes()
    if not data:
        raise RuntimeError(f'--attach {path}: file is empty')
    if len(data) > MAX_BYTES:
        raise RuntimeError(f'--attach {path}: {len(data)} bytes exceeds the '
                           f'{MAX_BYTES} byte (25 MB) rail cap')
    mime = guess_mime(p)
    if not mime:
        raise RuntimeError(
            f'--attach {path}: unsupported type "{p.suffix}". Allowed: '
            + ', '.join(sorted(set(_EXT_MIME))))
    sha = hashlib.sha256(data).hexdigest()
    body = {'mime': mime, 'bytes': len(data), 'sha256': sha,
            'filename': p.name}
    if target_sdid:
        body['target_spaceduck_id'] = target_sdid
    req = urllib.request.Request(f'{api}/beak/media/upload-url',
                                 data=json.dumps(body).encode(),
                                 headers=_api_headers(cfg), method='POST')
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            minted = json.loads(r.read())
    except urllib.error.HTTPError as e:
        _payload = _http_error_payload(e)
        err = _payload.get('error', '') if isinstance(_payload.get('error', ''), str) else ''
        if err == 'media_blocked_by_connection':
            raise RuntimeError(f'--attach {p.name}: this connection has media '
                               'disabled (allow_media=false in Mission Control)')
        if err == 'media_quota_exceeded':
            raise RuntimeError(quota_exceeded_message(p.name, _payload))
        raise RuntimeError(f'--attach {p.name}: upload-url HTTP {e.code} {err}')
    put = urllib.request.Request(minted['put_url'], data=data,
                                 headers={'Content-Type': mime}, method='PUT')
    try:
        with urllib.request.urlopen(put, timeout=120) as r:
            if r.status not in (200, 204):
                raise RuntimeError(f'S3 PUT HTTP {r.status}')
    except Exception as e:
        raise RuntimeError(f'--attach {p.name}: byte upload failed: {e}')
    return {'media_id': minted['media_id'], 'sha256': sha, 'mime': mime,
            'bytes': len(data), 'filename': p.name}


def fetch_attachments(cfg, attachments, peck_id=''):
    """Download every ref in an inbound peck's attachments[] to
    ~/.space-duck/media/, verifying sha256. Best-effort per item — returns
    {'saved': [paths], 'errors': [msgs]} and never raises (receipt of the
    peck must not depend on media)."""
    out = {'saved': [], 'errors': []}
    if not isinstance(attachments, list):
        return out
    api = cfg.get('api_base', 'https://beak.spaceduckling.com')
    for a in attachments[:MAX_ATTACHMENTS]:
        if not isinstance(a, dict):
            continue
        mid = str(a.get('media_id', ''))
        sha = str(a.get('sha256', '')).lower()
        if not _MEDIA_ID_RE.match(mid) or not _SHA256_RE.match(sha):
            out['errors'].append(f'{mid or "?"}: malformed ref')
            continue
        # filename from the ref is untrusted — keep the basename only and
        # prefix the media_id so two pecks can never collide or traverse.
        safe_name = str(a.get('filename', '')).replace('\\', '/').split('/')[-1][:255]
        dest = MEDIA_DIR / (f'{mid}_{safe_name}' if safe_name else mid)
        if dest.exists() and hashlib.sha256(dest.read_bytes()).hexdigest() == sha:
            out['saved'].append(str(dest))   # already fetched (re-delivery)
            continue
        try:
            req = urllib.request.Request(f'{api}/beak/media/{mid}',
                                         headers=_api_headers(cfg))
            with urllib.request.urlopen(req, timeout=20) as r:
                meta = json.loads(r.read())
            with urllib.request.urlopen(meta['get_url'], timeout=120) as r:
                blob = r.read(MAX_BYTES + 1)
            if len(blob) > MAX_BYTES:
                raise RuntimeError('object exceeds rail cap')
            if hashlib.sha256(blob).hexdigest() != sha:
                raise RuntimeError('sha256 mismatch — refusing to keep bytes')
            MEDIA_DIR.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(blob)
            try:
                dest.chmod(0o600)
            except Exception:
                pass
            out['saved'].append(str(dest))
        except urllib.error.HTTPError as e:
            try:
                err = json.loads(e.read()).get('error', '')
            except Exception:
                err = ''
            out['errors'].append(f'{mid}: HTTP {e.code} {err}'.strip())
        except Exception as e:
            out['errors'].append(f'{mid}: {e}')
    if out['errors'] and peck_id:
        print(f'   warn: media fetch for {peck_id}: ' + '; '.join(out['errors']),
              file=sys.stderr)
    return out
