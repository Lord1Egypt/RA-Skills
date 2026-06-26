#!/usr/bin/env python3
import argparse
import asyncio
import json
import os
import random
import string
import sys
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
SKILL_DIR = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG = ROOT / '.openclaw' / 'yandex-music-control' / 'config.json'
DEFAULT_CONFIG.parent.mkdir(parents=True, exist_ok=True)


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def redact_token(token: str | None):
    if not token:
        return None
    if len(token) <= 8:
        return '*' * len(token)
    return f'{token[:4]}…{token[-4:]}'


def load_client(token: str):
    try:
        from yandex_music import Client
        from yandex_music.exceptions import UnauthorizedError
    except Exception:
        eprint('yandex-music python package is missing.')
        eprint(f'Create venv and install: python3 -m venv {SKILL_DIR / ".venv"} && {SKILL_DIR / ".venv/bin/pip"} install yandex-music')
        raise SystemExit(2)

    try:
        client = Client(token).init()
    except UnauthorizedError:
        raise SystemExit('Token was rejected by Yandex Music (Unauthorized). Save a fresh token with auth-set or pass --token.')
    return client


def config_path(custom: str | None):
    return Path(custom).expanduser() if custom else DEFAULT_CONFIG


def read_config(path: Path):
    if not path.exists():
        return {}
    return json.loads(path.read_text())


def write_config(path: Path, data: dict):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2))
    os.chmod(path, 0o600)


def token_source(args):
    if getattr(args, 'token', None):
        return 'arg', args.token
    env = os.getenv('YM_TOKEN')
    if env:
        return 'env', env
    cfg = read_config(config_path(getattr(args, 'config', None)))
    token = cfg.get('token')
    if token:
        return 'config', token
    return None, None


def get_token(args):
    _source, token = token_source(args)
    if token:
        return token
    raise SystemExit('No token found. Use auth-set, --token, or YM_TOKEN.')


def fmt_track(track):
    artists = ', '.join(a.name for a in (track.artists or [])) or 'Unknown artist'
    title = getattr(track, 'title', 'Unknown title')
    album = getattr(getattr(track, 'albums', [None])[0], 'title', None) if getattr(track, 'albums', None) else None
    year = getattr(getattr(track, 'albums', [None])[0], 'year', None) if getattr(track, 'albums', None) else None
    suffix = []
    if album:
        suffix.append(album)
    if year:
        suffix.append(str(year))
    extra = f" ({' · '.join(suffix)})" if suffix else ''
    duration_ms = getattr(track, 'duration_ms', None)
    if duration_ms:
        mins, secs = divmod(duration_ms // 1000, 60)
        extra += f' [{mins}:{secs:02d}]'
    return f'{track.id}: {artists} — {title}{extra}'


def fmt_artist(artist):
    counts = []
    if getattr(artist, 'counts', None):
        tracks = artist.counts.get('tracks')
        albums = artist.counts.get('albums')
        if tracks is not None:
            counts.append(f'{tracks} tracks')
        if albums is not None:
            counts.append(f'{albums} albums')
    extra = f" ({', '.join(counts)})" if counts else ''
    return f'{artist.id}: {artist.name}{extra}'


def fmt_album(album):
    year = getattr(album, 'year', None)
    artists = ', '.join(a.name for a in (getattr(album, 'artists', None) or []))
    suffix = []
    if artists:
        suffix.append(artists)
    if year:
        suffix.append(str(year))
    extra = f" ({' · '.join(suffix)})" if suffix else ''
    return f'{album.id}: {album.title}{extra}'


def fmt_playlist(playlist):
    owner = getattr(getattr(playlist, 'owner', None), 'name', None) or getattr(getattr(playlist, 'owner', None), 'login', None)
    track_count = getattr(playlist, 'track_count', None)
    suffix = []
    if owner:
        suffix.append(owner)
    if track_count is not None:
        suffix.append(f'{track_count} tracks')
    extra = f" ({' · '.join(suffix)})" if suffix else ''
    return f'{playlist.kind}: {playlist.title}{extra}'


def resolve_track_id(client, query: str):
    if query.isdigit():
        tracks = client.tracks([query])
        if tracks and tracks[0]:
            return tracks[0]
    result = client.search(query, type_='track')
    if not result or not result.tracks or not result.tracks.results:
        raise SystemExit(f'No track found for query: {query}')
    return result.tracks.results[0]


def generate_device_id(length: int = 16) -> str:
    return ''.join(random.choices(string.ascii_lowercase, k=length))


async def ynison_shadow_probe(session, token: str):
    device_id = generate_device_id()
    ws_proto = {
        'Ynison-Device-Id': device_id,
        'Ynison-Device-Info': json.dumps({'app_name': 'Chrome', 'type': 1}),
    }
    async with session.ws_connect(
        'wss://ynison.music.yandex.ru/redirector.YnisonRedirectService/GetRedirectToYnison',
        headers={
            'Sec-WebSocket-Protocol': f'Bearer, v2, {json.dumps(ws_proto)}',
            'Origin': 'http://music.yandex.ru',
            'Authorization': f'OAuth {token}',
        },
    ) as ws:
        data = json.loads((await ws.receive()).data)

    ws_proto['Ynison-Redirect-Ticket'] = data['redirect_ticket']
    payload = {
        'update_full_state': {
            'player_state': {
                'player_queue': {
                    'current_playable_index': -1,
                    'entity_id': '',
                    'entity_type': 'VARIOUS',
                    'playable_list': [],
                    'options': {'repeat_mode': 'NONE'},
                    'entity_context': 'BASED_ON_ENTITY_BY_DEFAULT',
                    'version': {'device_id': device_id, 'version': 9021243204784341000, 'timestamp_ms': 0},
                    'from_optional': '',
                },
                'status': {
                    'duration_ms': 0,
                    'paused': True,
                    'playback_speed': 1,
                    'progress_ms': 0,
                    'version': {'device_id': device_id, 'version': 8321822175199937000, 'timestamp_ms': 0},
                },
            },
            'device': {
                'capabilities': {'can_be_player': True, 'can_be_remote_controller': False, 'volume_granularity': 16},
                'info': {'device_id': device_id, 'type': 'WEB', 'title': 'Chrome Browser', 'app_name': 'Chrome'},
                'volume_info': {'volume': 0},
                'is_shadow': True,
            },
            'is_currently_active': False,
        },
        'rid': str(uuid.uuid4()),
        'player_action_timestamp_ms': 0,
        'activity_interception_type': 'DO_NOT_INTERCEPT_BY_DEFAULT',
    }
    async with session.ws_connect(
        f"wss://{data['host']}/ynison_state.YnisonStateService/PutYnisonState",
        headers={
            'Sec-WebSocket-Protocol': f'Bearer, v2, {json.dumps(ws_proto)}',
            'Origin': 'http://music.yandex.ru',
            'Authorization': f'OAuth {token}',
        },
    ) as ws:
        await ws.send_str(json.dumps(payload))
        ynison = json.loads((await ws.receive()).data)
    return ynison


async def ynison_current_state(token: str):
    try:
        import aiohttp
        from yandex_music import ClientAsync
    except Exception:
        raise SystemExit('aiohttp/yandex-music async support is missing in the skill venv.')

    client = await ClientAsync(token).init()
    async with aiohttp.ClientSession() as session:
        ynison = await ynison_shadow_probe(session, token)

    queue = ynison.get('player_state', {}).get('player_queue', {})
    status = ynison.get('player_state', {}).get('status', {})
    devices = ynison.get('devices') or []
    active_device_id = ynison.get('active_device_id_optional') or queue.get('version', {}).get('device_id') or status.get('version', {}).get('device_id')
    active_device = next((d for d in devices if d.get('info', {}).get('device_id') == active_device_id), None)

    idx = queue.get('current_playable_index', -1)
    playable_list = queue.get('playable_list') or []
    if idx < 0 or idx >= len(playable_list):
        raise RuntimeError('Ynison returned no active playable item.')

    playable = playable_list[idx]
    track_id = playable.get('playable_id')
    if not track_id:
        raise RuntimeError('Ynison active item has no playable_id.')

    track = (await client.tracks([track_id]))[0]
    info = active_device.get('info', {}) if active_device else {}
    session_info = active_device.get('session', {}) if active_device else {}

    return {
        'source': 'ynison',
        'device_id': active_device_id,
        'device_title': info.get('title'),
        'device_type': info.get('type'),
        'device_is_offline': active_device.get('is_offline') if active_device else None,
        'device_session_id': session_info.get('id'),
        'paused': status.get('paused'),
        'duration_ms': status.get('duration_ms'),
        'progress_ms': status.get('progress_ms'),
        'entity_id': queue.get('entity_id'),
        'entity_type': queue.get('entity_type'),
        'current_index': idx,
        'track_count': len(playable_list),
        'queue_version': queue.get('version'),
        'status_version': status.get('version'),
        'navigation_id_optional': queue.get('navigation_id_optional') or playable.get('navigation_id_optional'),
        'playback_action_id_optional': queue.get('playback_action_id_optional') or playable.get('playback_action_id_optional'),
        'track': {
            'id': track.id,
            'title': track.title,
            'artists': [a.name for a in (track.artists or [])],
            'album': track.albums[0].title if getattr(track, 'albums', None) else None,
            'duration_ms': track.duration_ms,
        },
    }


def cmd_auth_set(args):
    path = config_path(args.config)
    cfg = read_config(path)
    cfg['token'] = args.token.strip()
    write_config(path, cfg)
    print(f'Token saved to {path}')


def cmd_auth_clear(args):
    path = config_path(args.config)
    cfg = read_config(path)
    if 'token' in cfg:
        del cfg['token']
    write_config(path, cfg)
    print(f'Token removed from {path}')


def cmd_auth_where(args):
    source, token = token_source(args)
    print(json.dumps({
        'config_path': str(config_path(args.config)),
        'token_source': source,
        'token_present': bool(token),
        'token_preview': redact_token(token),
    }, ensure_ascii=False, indent=2))


def cmd_auth_check(args):
    source, token = token_source(args)
    if not token:
        raise SystemExit('No token found. Use auth-set, --token, or YM_TOKEN.')
    client = load_client(token)
    status = client.account_status()
    account = getattr(status, 'account', None)
    result = {
        'ok': True,
        'token_source': source,
        'token_preview': redact_token(token),
        'uid': getattr(account, 'uid', None),
        'login': getattr(account, 'login', None),
        'display_name': getattr(account, 'display_name', None),
        'plus': bool(getattr(status, 'plus', None)),
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_search(args):
    client = load_client(get_token(args))
    result = client.search(args.query, type_=args.type, page=0)
    if not result:
        raise SystemExit('Empty search result.')

    if args.type == 'track':
        items = (result.tracks.results if result and result.tracks else [])[: args.limit]
        for idx, item in enumerate(items, 1):
            print(f'{idx}. {fmt_track(item)}')
        return
    if args.type == 'artist':
        items = (result.artists.results if result and result.artists else [])[: args.limit]
        for idx, item in enumerate(items, 1):
            print(f'{idx}. {fmt_artist(item)}')
        return
    if args.type == 'album':
        items = (result.albums.results if result and result.albums else [])[: args.limit]
        for idx, item in enumerate(items, 1):
            print(f'{idx}. {fmt_album(item)}')
        return
    if args.type == 'playlist':
        items = (result.playlists.results if result and result.playlists else [])[: args.limit]
        for idx, item in enumerate(items, 1):
            print(f'{idx}. {fmt_playlist(item)}')
        return

    payload = {
        'best': result.best.to_dict() if getattr(result, 'best', None) else None,
        'tracks': [t.to_dict() for t in (result.tracks.results if getattr(result, 'tracks', None) else [])[: args.limit]],
        'artists': [a.to_dict() for a in (result.artists.results if getattr(result, 'artists', None) else [])[: args.limit]],
        'albums': [a.to_dict() for a in (result.albums.results if getattr(result, 'albums', None) else [])[: args.limit]],
        'playlists': [p.to_dict() for p in (result.playlists.results if getattr(result, 'playlists', None) else [])[: args.limit]],
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))


def cmd_now_playing(args):
    token = get_token(args)
    payload = asyncio.run(ynison_current_state(token))
    print(json.dumps(payload, ensure_ascii=False, indent=2))


def cmd_like(args):
    client = load_client(get_token(args))
    track = resolve_track_id(client, args.query)
    ok = client.users_likes_tracks_add(track.id)
    print(json.dumps({'ok': bool(ok), 'track': fmt_track(track)}, ensure_ascii=False, indent=2))


def cmd_unlike(args):
    client = load_client(get_token(args))
    track = resolve_track_id(client, args.query)
    ok = client.users_likes_tracks_remove(track.id)
    print(json.dumps({'ok': bool(ok), 'track': fmt_track(track)}, ensure_ascii=False, indent=2))


def cmd_likes(args):
    client = load_client(get_token(args))
    liked = client.users_likes_tracks()
    tracks = liked.fetch_tracks()[: args.limit]
    for idx, track in enumerate(tracks, 1):
        print(f'{idx}. {fmt_track(track)}')


def cmd_playlists(args):
    client = load_client(get_token(args))
    playlists = client.users_playlists_list()
    for idx, pl in enumerate(playlists[: args.limit], 1):
        print(f'{idx}. {fmt_playlist(pl)}')


def build():
    p = argparse.ArgumentParser(description='Read/search helper for Yandex Music')
    p.add_argument('--config', help='Path to config JSON')
    sub = p.add_subparsers(dest='cmd', required=True)

    a = sub.add_parser('auth-set', help='Save token to config')
    a.add_argument('token')
    a.set_defaults(func=cmd_auth_set)

    a = sub.add_parser('auth-clear', help='Remove token from config file')
    a.set_defaults(func=cmd_auth_clear)

    a = sub.add_parser('auth-where', help='Show where token config is coming from without leaking secrets')
    a.add_argument('--token')
    a.set_defaults(func=cmd_auth_where)

    a = sub.add_parser('auth-check', help='Validate token and print account info')
    a.add_argument('--token')
    a.set_defaults(func=cmd_auth_check)

    a = sub.add_parser('search', help='Search in Yandex Music')
    a.add_argument('query')
    a.add_argument('--type', default='track', choices=['all', 'track', 'artist', 'album', 'playlist'])
    a.add_argument('--limit', type=int, default=5)
    a.add_argument('--token')
    a.set_defaults(func=cmd_search)

    a = sub.add_parser('now-playing', help='Show current track via Ynison probe')
    a.add_argument('--token')
    a.set_defaults(func=cmd_now_playing)

    a = sub.add_parser('like', help='Like track by id or search query')
    a.add_argument('query')
    a.add_argument('--token')
    a.set_defaults(func=cmd_like)

    a = sub.add_parser('unlike', help='Remove like from track by id or search query')
    a.add_argument('query')
    a.add_argument('--token')
    a.set_defaults(func=cmd_unlike)

    a = sub.add_parser('likes', help='List liked tracks')
    a.add_argument('--limit', type=int, default=10)
    a.add_argument('--token')
    a.set_defaults(func=cmd_likes)

    a = sub.add_parser('playlists', help='List playlists')
    a.add_argument('--limit', type=int, default=20)
    a.add_argument('--token')
    a.set_defaults(func=cmd_playlists)
    return p


if __name__ == '__main__':
    parser = build()
    args = parser.parse_args()
    args.func(args)
