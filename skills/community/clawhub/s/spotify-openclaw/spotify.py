#!/usr/bin/env python3
"""
Spotify CLI helper для OpenClaw агента.
Избегает проблем с кавычками в bash — всё через Python.
Читает CLIENT_ID/SECRET из Keychain автоматически.

Использование:
  python3 /Users/mixx/.openclaw/scripts/spotify.py top-tracks [short|medium|long] [limit]
  python3 /Users/mixx/.openclaw/scripts/spotify.py top-artists [short|medium|long] [limit]
  python3 /Users/mixx/.openclaw/scripts/spotify.py recent [limit]
  python3 /Users/mixx/.openclaw/scripts/spotify.py liked [limit]
  python3 /Users/mixx/.openclaw/scripts/spotify.py playlists
  python3 /Users/mixx/.openclaw/scripts/spotify.py create-playlist "Название" ["Описание"]
  python3 /Users/mixx/.openclaw/scripts/spotify.py add-to-playlist PLAYLIST_ID TRACK_URI [TRACK_URI ...]
  python3 /Users/mixx/.openclaw/scripts/spotify.py search "query" [track|artist|album] [limit]
  python3 /Users/mixx/.openclaw/scripts/spotify.py genres [short|medium|long]
  python3 /Users/mixx/.openclaw/scripts/spotify.py now
  python3 /Users/mixx/.openclaw/scripts/spotify.py track-info TRACK_URI [TRACK_URI ...]
  python3 /Users/mixx/.openclaw/scripts/spotify.py related-artists ARTIST_NAME_OR_ID [limit]
  python3 /Users/mixx/.openclaw/scripts/spotify.py artist-top-tracks ARTIST_NAME_OR_ID [limit]
  python3 /Users/mixx/.openclaw/scripts/spotify.py make-playlist "Название" [short|medium|long] [limit]
  python3 /Users/mixx/.openclaw/scripts/spotify.py discover ARTIST_NAME [depth] [tracks_per_artist]
  python3 /Users/mixx/.openclaw/scripts/spotify.py liked-all
  python3 /Users/mixx/.openclaw/scripts/spotify.py liked-by-artist "Artist Name"

Playback (Spotify Premium):
  python3 /Users/mixx/.openclaw/scripts/spotify.py play
  python3 /Users/mixx/.openclaw/scripts/spotify.py play "название трека"
  python3 /Users/mixx/.openclaw/scripts/spotify.py play spotify:track:URI
  python3 /Users/mixx/.openclaw/scripts/spotify.py play playlist PLAYLIST_ID
  python3 /Users/mixx/.openclaw/scripts/spotify.py pause
  python3 /Users/mixx/.openclaw/scripts/spotify.py next
  python3 /Users/mixx/.openclaw/scripts/spotify.py prev
  python3 /Users/mixx/.openclaw/scripts/spotify.py volume 70
  python3 /Users/mixx/.openclaw/scripts/spotify.py volume up/down
  python3 /Users/mixx/.openclaw/scripts/spotify.py devices
  python3 /Users/mixx/.openclaw/scripts/spotify.py queue "название трека"
  python3 /Users/mixx/.openclaw/scripts/spotify.py shuffle on/off
"""

import sys
import os
import subprocess
import json
import time
from collections import Counter
from pathlib import Path

CACHE_PATH = str(Path.home() / ".openclaw" / ".spotify_cache")
_ME_CACHE = {}  # lazy cache for user id


def get_my_user_id(sp):
    """Получает user ID текущего пользователя через API (с кэшированием)."""
    if "id" not in _ME_CACHE:
        _ME_CACHE["id"] = sp.me()["id"]
    return _ME_CACHE["id"]


def _keychain_get(service):
    """Читает значение из macOS Keychain."""
    result = subprocess.run(
        ["security", "find-generic-password", "-a", "openclaw", "-s", service, "-w"],
        capture_output=True, text=True
    )
    if result.returncode == 0:
        return result.stdout.strip()
    return None


def _setup_env():
    """Устанавливает SPOTIPY_* переменные из Keychain если не заданы."""
    if not os.environ.get("SPOTIPY_CLIENT_ID"):
        val = _keychain_get("openclaw.spotify.client_id")
        if val:
            os.environ["SPOTIPY_CLIENT_ID"] = val
    if not os.environ.get("SPOTIPY_CLIENT_SECRET"):
        val = _keychain_get("openclaw.spotify.client_secret")
        if val:
            os.environ["SPOTIPY_CLIENT_SECRET"] = val
    os.environ.setdefault("SPOTIPY_REDIRECT_URI", "http://127.0.0.1:8888/callback")
    os.environ.setdefault("SPOTIPY_CACHE_PATH", CACHE_PATH)


_setup_env()

try:
    import spotipy
    from spotipy.oauth2 import SpotifyOAuth
except ImportError:
    print("ERROR: spotipy not installed. Run: pip3 install spotipy --break-system-packages")
    sys.exit(1)


SCOPES = " ".join([
    "user-read-private",
    "user-read-email",
    "user-top-read",
    "user-read-recently-played",
    "user-library-read",
    "user-library-modify",
    "playlist-read-private",
    "playlist-modify-private",
    "playlist-modify-public",
    # Playback (Premium)
    "user-read-playback-state",
    "user-modify-playback-state",
    "user-read-currently-playing",
])


def get_sp():
    return spotipy.Spotify(auth_manager=SpotifyOAuth(
        cache_path=CACHE_PATH,
        scope=SCOPES,
    ))


PERIOD_MAP = {"short": "short_term", "medium": "medium_term", "long": "long_term"}


def normalize_period(p):
    return PERIOD_MAP.get(p, p if p in ("short_term", "medium_term", "long_term") else "medium_term")


def normalize_uri(uri):
    if uri.startswith("spotify:track:"):
        return uri
    elif uri.startswith("https://open.spotify.com/track/"):
        return "spotify:track:" + uri.split("/track/")[1].split("?")[0]
    else:
        return "spotify:track:" + uri


def find_artist_id(sp, name_or_id):
    """По имени артиста или ID получает artist_id."""
    # Если выглядит как ID (22 символа base62) — используем напрямую
    if len(name_or_id) == 22 and name_or_id.replace("_", "").replace("-", "").isalnum():
        return name_or_id
    results = sp.search(q=f"artist:{name_or_id}", type="artist", limit=1)
    items = results["artists"]["items"]
    if not items:
        return None
    return items[0]["id"]


# ─── команды ────────────────────────────────────────────────────────────────

def cmd_top_tracks(args):
    period = normalize_period(args[0] if args else "medium")
    limit = int(args[1]) if len(args) > 1 else 10
    sp = get_sp()
    tracks = sp.current_user_top_tracks(limit=limit, time_range=period)["items"]
    print(f"Топ {limit} треков ({period}):")
    for i, t in enumerate(tracks, 1):
        artists = ", ".join(a["name"] for a in t["artists"])
        print(f"  {i}. {t['name']} — {artists}")
        print(f"     URI: {t['uri']}")


def cmd_top_artists(args):
    period = normalize_period(args[0] if args else "medium")
    limit = int(args[1]) if len(args) > 1 else 10
    sp = get_sp()
    artists = sp.current_user_top_artists(limit=limit, time_range=period)["items"]
    print(f"Топ {limit} артистов ({period}):")
    for i, a in enumerate(artists, 1):
        genres = ", ".join(a["genres"][:3]) if a["genres"] else "—"
        print(f"  {i}. {a['name']} | {a['id']} | {genres}")


def cmd_recent(args):
    limit = int(args[0]) if args else 20
    sp = get_sp()
    items = sp.current_user_recently_played(limit=limit)["items"]
    print(f"Последние {len(items)} треков:")
    for r in items:
        t = r["track"]
        artists = ", ".join(a["name"] for a in t["artists"])
        played = r["played_at"][:16].replace("T", " ")
        print(f"  {played} — {t['name']} ({artists})")
        print(f"     URI: {t['uri']}")


def cmd_liked(args):
    limit = int(args[0]) if args else 50
    sp = get_sp()
    items = sp.current_user_saved_tracks(limit=min(limit, 50))["items"]
    print(f"Сохранённые треки (первые {len(items)}):")
    for item in items:
        t = item["track"]
        artists = ", ".join(a["name"] for a in t["artists"])
        print(f"  {t['name']} — {artists}")
        print(f"     URI: {t['uri']}")


def cmd_liked_all(args):
    """Все лайкнутые треки с пагинацией."""
    sp = get_sp()
    liked = []
    offset = 0
    while True:
        batch = sp.current_user_saved_tracks(limit=50, offset=offset)["items"]
        if not batch:
            break
        liked.extend(batch)
        offset += 50
        if len(batch) < 50:
            break
    print(f"Всего лайкнутых треков: {len(liked)}")
    for item in liked:
        t = item["track"]
        artists = ", ".join(a["name"] for a in t["artists"])
        print(f"  {t['name']} — {artists} | URI: {t['uri']}")


def cmd_liked_by_artist(args):
    """Все лайкнутые треки конкретного артиста."""
    if not args:
        print("ERROR: укажи имя артиста")
        sys.exit(1)
    target = args[0].lower()
    sp = get_sp()
    liked = []
    offset = 0
    while True:
        batch = sp.current_user_saved_tracks(limit=50, offset=offset)["items"]
        if not batch:
            break
        liked.extend(batch)
        offset += 50
        if len(batch) < 50:
            break
    found = []
    for item in liked:
        t = item["track"]
        for a in t["artists"]:
            if target in a["name"].lower():
                found.append(t)
                break
    print(f"Лайкнутые треки '{args[0]}' ({len(found)}):")
    for t in found:
        artists = ", ".join(a["name"] for a in t["artists"])
        print(f"  {t['name']} — {artists} | URI: {t['uri']}")


def cmd_playlists(args):
    sp = get_sp()
    items = sp.current_user_playlists(limit=50)["items"]
    print(f"Плейлисты ({len(items)}):")
    for p in items:
        print(f"  [{p['id']}] {p['name']} — {p['tracks']['total']} треков")


def cmd_create_playlist(args):
    if not args:
        print("ERROR: укажи название плейлиста")
        sys.exit(1)
    name = args[0]
    description = args[1] if len(args) > 1 else ""
    sp = get_sp()
    pl = sp.user_playlist_create(
        user=get_my_user_id(sp),
        name=name,
        public=False,
        description=description
    )
    print(f"Создан плейлист: {pl['name']}")
    print(f"ID: {pl['id']}")
    print(f"URI: {pl['uri']}")
    print(f"URL: {pl['external_urls']['spotify']}")


def cmd_add_to_playlist(args):
    if len(args) < 2:
        print("ERROR: укажи PLAYLIST_ID и TRACK_URI")
        sys.exit(1)
    playlist_id = args[0]
    track_uris = [normalize_uri(u) for u in args[1:]]
    sp = get_sp()
    # Добавляем по 100 (лимит API)
    for i in range(0, len(track_uris), 100):
        sp.playlist_add_items(playlist_id=playlist_id, items=track_uris[i:i+100])
    print(f"Добавлено {len(track_uris)} треков в плейлист {playlist_id}")


def cmd_search(args):
    if not args:
        print("ERROR: укажи поисковый запрос")
        sys.exit(1)
    query = args[0]
    search_type = args[1] if len(args) > 1 else "track"
    limit = int(args[2]) if len(args) > 2 else 10
    sp = get_sp()
    results = sp.search(q=query, type=search_type, limit=limit)
    if search_type == "track":
        items = results["tracks"]["items"]
        print(f"Треки по запросу '{query}' ({len(items)}):")
        for t in items:
            artists = ", ".join(a["name"] for a in t["artists"])
            print(f"  {t['name']} — {artists} | pop:{t['popularity']}")
            print(f"     URI: {t['uri']}")
    elif search_type == "artist":
        items = results["artists"]["items"]
        print(f"Артисты по запросу '{query}':")
        for a in items:
            genres = ", ".join(a["genres"][:3]) if a["genres"] else "—"
            print(f"  {a['name']} | ID: {a['id']} | {genres}")
    elif search_type == "album":
        items = results["albums"]["items"]
        print(f"Альбомы по запросу '{query}':")
        for al in items:
            artists = ", ".join(a["name"] for a in al["artists"])
            print(f"  {al['name']} — {artists} ({al['release_date'][:4]})")


def cmd_genres(args):
    period = normalize_period(args[0] if args else "medium")
    sp = get_sp()
    artists = sp.current_user_top_artists(limit=50, time_range=period)["items"]
    genres = []
    for a in artists:
        genres.extend(a["genres"])
    top = Counter(genres).most_common(15)
    print(f"Топ жанры ({period}):")
    for genre, count in top:
        bar = "█" * count
        print(f"  {genre:<30} {bar} ({count})")


def cmd_now(args):
    sp = get_sp()
    current = sp.current_playback()
    if not current or not current.get("is_playing"):
        print("Сейчас ничего не играет")
        return
    t = current["item"]
    artists = ", ".join(a["name"] for a in t["artists"])
    progress = current["progress_ms"] // 1000
    duration = t["duration_ms"] // 1000
    print(f"Сейчас играет: {t['name']} — {artists}")
    print(f"  Прогресс: {progress//60}:{progress%60:02d} / {duration//60}:{duration%60:02d}")
    print(f"  URI: {t['uri']}")
    print(f"  Устройство: {current.get('device', {}).get('name', '—')}")


def cmd_track_info(args):
    if not args:
        print("ERROR: укажи TRACK_URI или TRACK_ID")
        sys.exit(1)
    sp = get_sp()
    for uri in args:
        if uri.startswith("spotify:track:"):
            track_id = uri.split(":")[-1]
        elif uri.startswith("https://open.spotify.com/track/"):
            track_id = uri.split("/track/")[1].split("?")[0]
        else:
            track_id = uri
        t = sp.track(track_id)
        artists = ", ".join(a["name"] for a in t["artists"])
        print(f"{t['name']} — {artists}")
        print(f"  Альбом: {t['album']['name']} ({t['album']['release_date'][:4]})")
        print(f"  Популярность: {t['popularity']}/100")
        duration = t["duration_ms"] // 1000
        print(f"  Длительность: {duration//60}:{duration%60:02d}")
        print(f"  URI: {t['uri']}")


def cmd_related_artists(args):
    """Похожие артисты через поиск по жанрам (related-artists API недоступен для новых приложений)."""
    if not args:
        print("ERROR: укажи имя артиста или ID")
        sys.exit(1)
    sp = get_sp()
    limit = int(args[1]) if len(args) > 1 else 10
    artist_id = find_artist_id(sp, args[0])
    if not artist_id:
        print(f"ERROR: артист '{args[0]}' не найден")
        sys.exit(1)
    artist = sp.artist(artist_id)
    genres = artist.get("genres", [])
    if not genres:
        print(f"У {artist['name']} нет жанров в Spotify — ищем по имени")
        results = sp.search(q=f"artist:{artist['name']}", type="artist", limit=limit+1)
        found = [a for a in results["artists"]["items"] if a["id"] != artist_id][:limit]
    else:
        # Ищем по главному жанру (без genre: — работает лучше)
        found = []
        seen = {artist_id}
        for genre in genres[:3]:
            results = sp.search(q=genre, type="artist", limit=20)
            for a in results["artists"]["items"]:
                if a["id"] not in seen:
                    seen.add(a["id"])
                    found.append(a)
            if len(found) >= limit:
                break
        found = found[:limit]
    print(f"Похожие на {artist['name']} (по жанрам: {', '.join(genres[:2]) or '—'}):")
    for a in found:
        a_genres = ", ".join(a["genres"][:3]) if a["genres"] else "—"
        print(f"  {a['name']} | ID: {a['id']} | pop:{a['popularity']} | {a_genres}")


def cmd_artist_top_tracks(args):
    """Топ треки артиста."""
    if not args:
        print("ERROR: укажи имя артиста или ID")
        sys.exit(1)
    sp = get_sp()
    limit = int(args[1]) if len(args) > 1 else 10
    artist_id = find_artist_id(sp, args[0])
    if not artist_id:
        print(f"ERROR: артист '{args[0]}' не найден")
        sys.exit(1)
    artist = sp.artist(artist_id)
    tracks = sp.artist_top_tracks(artist_id)["tracks"][:limit]
    print(f"Топ треки {artist['name']} ({len(tracks)}):")
    for i, t in enumerate(tracks, 1):
        duration = t["duration_ms"] // 1000
        print(f"  {i}. {t['name']} | pop:{t['popularity']} | {duration//60}:{duration%60:02d}")
        print(f"     URI: {t['uri']}")


def cmd_make_playlist(args):
    """Создаёт плейлист из топ-треков пользователя.

    Использование: make-playlist "Название" [short|medium|long] [limit]
    """
    if not args:
        print("ERROR: укажи название плейлиста")
        sys.exit(1)
    name = args[0]
    period = normalize_period(args[1] if len(args) > 1 else "short")
    limit = int(args[2]) if len(args) > 2 else 20
    sp = get_sp()

    # Собираем топ треки
    tracks = sp.current_user_top_tracks(limit=limit, time_range=period)["items"]
    uris = [t["uri"] for t in tracks]

    # Создаём плейлист
    from datetime import datetime
    month = datetime.now().strftime("%B %Y")
    pl = sp.user_playlist_create(
        user=get_my_user_id(sp),
        name=name,
        public=False,
        description=f"Создан TupacAI | {month} | {period}"
    )
    sp.playlist_add_items(playlist_id=pl["id"], items=uris)
    print(f"Плейлист создан: {pl['name']}")
    print(f"ID: {pl['id']}")
    print(f"URL: {pl['external_urls']['spotify']}")
    print(f"Добавлено треков: {len(uris)}")
    for i, t in enumerate(tracks, 1):
        artists = ", ".join(a["name"] for a in t["artists"])
        print(f"  {i}. {t['name']} — {artists}")


def cmd_discover(args):
    """Находит новую музыку по жанрам профиля пользователя.

    related-artists API недоступен — используем жанровый поиск.
    Берёт топ-жанры пользователя → ищет артистов по каждому жанру
    → берёт их топ треки → фильтрует уже известных артистов.

    Использование:
      discover                     — по топ-жанрам пользователя
      discover ARTIST_NAME         — по жанрам конкретного артиста
      discover ARTIST_NAME 5 3     — глубина=5, треков=3
    """
    sp = get_sp()
    tracks_per = 3
    limit_artists = 5

    # Собираем уже известных артистов (из топа пользователя)
    known_artists = set()
    known_names = set()
    for period in ["short_term", "medium_term", "long_term"]:
        for a in sp.current_user_top_artists(limit=50, time_range=period)["items"]:
            known_artists.add(a["id"])
            known_names.add(a["name"].lower())

    if args and not args[0].isdigit():
        # Режим: конкретный артист — берём его жанры
        seed_name = args[0]
        limit_artists = int(args[1]) if len(args) > 1 else 5
        tracks_per = int(args[2]) if len(args) > 2 else 3
        artist_id = find_artist_id(sp, seed_name)
        if not artist_id:
            print(f"ERROR: артист '{seed_name}' не найден")
            sys.exit(1)
        seed_artist = sp.artist(artist_id)
        seed_genres = seed_artist.get("genres", [])
        if not seed_genres:
            print(f"У {seed_artist['name']} нет жанров. Пробуем поиск по имени...")
            seed_genres = [seed_artist["name"]]
        print(f"Ищем похожих на {seed_artist['name']} по жанрам: {', '.join(seed_genres[:3])}")
    else:
        # Режим: жанры из профиля пользователя
        limit_artists = int(args[0]) if args else 5
        tracks_per = int(args[1]) if len(args) > 1 else 3
        top_artists = sp.current_user_top_artists(limit=50, time_range="medium_term")["items"]
        genre_counter = Counter()
        for a in top_artists:
            genre_counter.update(a["genres"])
        seed_genres = [g for g, _ in genre_counter.most_common(5)]
        print(f"Твои топ-жанры: {', '.join(seed_genres)}")

    discoveries = []
    seen_track_ids = set()
    seen_artist_ids = set(known_artists)

    for genre in seed_genres[:5]:
        print(f"\n  Жанр: {genre}")
        try:
            # Ищем без 'genre:' — работает лучше для нишевых жанров
            results = sp.search(q=genre, type="artist", limit=20)
            artists = results["artists"]["items"]
        except Exception as e:
            print(f"    Ошибка поиска: {e}")
            continue

        new_artists = [a for a in artists if a["id"] not in seen_artist_ids][:limit_artists]

        for rel in new_artists:
            seen_artist_ids.add(rel["id"])
            a_genres = ", ".join(rel["genres"][:2]) if rel["genres"] else "—"
            print(f"    ★ {rel['name']} | pop:{rel['popularity']} | {a_genres}")

            try:
                top_tracks = sp.artist_top_tracks(rel["id"])["tracks"][:tracks_per]
            except Exception:
                continue

            for t in top_tracks:
                if t["id"] not in seen_track_ids:
                    seen_track_ids.add(t["id"])
                    discoveries.append({
                        "track": t,
                        "genre": genre,
                        "artist": rel,
                    })

    print(f"\n{'═'*55}")
    print(f"Открытия — {len(discoveries)} треков от {len(seen_artist_ids - known_artists)} новых артистов:")
    discoveries.sort(key=lambda x: -x["artist"]["popularity"])
    for d in discoveries:
        t = d["track"]
        artists = ", ".join(a["name"] for a in t["artists"])
        print(f"  {t['name']} — {artists}")
        print(f"     жанр: {d['genre']} | pop:{t['popularity']} | URI: {t['uri']}")


def ensure_active_device(sp, retries=3, wait=2.5):
    """Проверяет устройство. Если нет — запускает Spotify. Возвращает device_id или None."""
    devices = sp.devices().get("devices", [])
    if devices:
        # Вернуть активное, иначе первое доступное
        for d in devices:
            if d.get("is_active"):
                return d["id"]
        return devices[0]["id"]
    # Нет устройства — запускаем Spotify
    print("⚡ Spotify не запущен — открываю...")
    os.system("open -a Spotify")
    for i in range(retries):
        time.sleep(wait)
        devices = sp.devices().get("devices", [])
        if devices:
            print(f"✅ Spotify запущен ({devices[0]['name']})")
            time.sleep(2)  # доп. пауза — ждём полной инициализации
            for d in devices:
                if d.get("is_active"):
                    return d["id"]
            return devices[0]["id"]
    print("⚠️  Не удалось запустить Spotify — открой вручную")
    return None


def cmd_play(args):
    """Воспроизведение.
    play                        — продолжить/возобновить
    play TRACK_URI              — включить конкретный трек
    play "название трека"       — найти и включить трек
    play playlist PLAYLIST_ID   — включить плейлист
    """
    sp = get_sp()
    device_id = ensure_active_device(sp)

    if not args:
        # Просто resume
        try:
            sp.start_playback(device_id=device_id)
            print("▶ Воспроизведение возобновлено")
        except Exception as e:
            print(f"ERROR: {e}")
            print("  Убедись что Spotify открыт на этом ноуте")
        return

    query = args[0]

    # play spotify:playlist:xxx или playlist PLAYLIST_ID
    if query.startswith("spotify:playlist:"):
        try:
            sp.start_playback(context_uri=query, device_id=device_id)
            print(f"▶ Играет плейлист")
        except Exception as e:
            print(f"ERROR: {e}")
        return

    if query.lower() == "playlist" and len(args) > 1:
        playlist_id = args[1]
        if not playlist_id.startswith("spotify:"):
            playlist_id = "spotify:playlist:" + playlist_id
        try:
            sp.start_playback(context_uri=playlist_id, device_id=device_id)
            print(f"▶ Играет плейлист {playlist_id}")
        except Exception as e:
            print(f"ERROR: {e}")
        return

    # play spotify:track:xxx
    if query.startswith("spotify:track:") or (len(query) == 22 and query.replace("_","").replace("-","").isalnum()):
        uri = normalize_uri(query)
        try:
            sp.start_playback(uris=[uri], device_id=device_id)
            info = sp.track(uri)
            artists = ", ".join(a["name"] for a in info["artists"])
            print(f"▶ {info['name']} — {artists}")
        except Exception as e:
            print(f"ERROR: {e}")
        return

    # play "название" — ищем трек
    search_q = " ".join(args)
    results = sp.search(q=search_q, type="track", limit=1)
    items = results["tracks"]["items"]
    if not items:
        print(f"ERROR: трек '{search_q}' не найден")
        return
    track = items[0]
    artists = ", ".join(a["name"] for a in track["artists"])
    try:
        sp.start_playback(uris=[track["uri"]], device_id=device_id)
        print(f"▶ {track['name']} — {artists}")
        print(f"  URI: {track['uri']}")
    except Exception as e:
        print(f"ERROR: {e}")
        print("  Убедись что Spotify открыт на этом ноуте")


def cmd_pause(args):
    """Пауза."""
    sp = get_sp()
    device_id = ensure_active_device(sp)
    try:
        sp.pause_playback(device_id=device_id)
        print("⏸ Пауза")
    except Exception as e:
        print(f"ERROR: {e}")


def cmd_next(args):
    """Следующий трек."""
    sp = get_sp()
    device_id = ensure_active_device(sp)
    try:
        sp.next_track(device_id=device_id)
        time.sleep(0.5)
        cur = sp.current_playback()
        if cur and cur.get("item"):
            t = cur["item"]
            artists = ", ".join(a["name"] for a in t["artists"])
            print(f"⏭ {t['name']} — {artists}")
        else:
            print("⏭ Следующий трек")
    except Exception as e:
        print(f"ERROR: {e}")


def cmd_prev(args):
    """Предыдущий трек."""
    sp = get_sp()
    device_id = ensure_active_device(sp)
    try:
        sp.previous_track(device_id=device_id)
        time.sleep(0.5)
        cur = sp.current_playback()
        if cur and cur.get("item"):
            t = cur["item"]
            artists = ", ".join(a["name"] for a in t["artists"])
            print(f"⏮ {t['name']} — {artists}")
        else:
            print("⏮ Предыдущий трек")
    except Exception as e:
        print(f"ERROR: {e}")


def cmd_volume(args):
    """Громкость.
    volume 70      — установить 70%
    volume up      — +10%
    volume down    — -10%
    """
    sp = get_sp()
    device_id = ensure_active_device(sp)
    if not args:
        cur = sp.current_playback()
        if cur and cur.get("device"):
            print(f"🔊 Громкость: {cur['device']['volume_percent']}%")
        else:
            print("ERROR: нет активного устройства")
        return

    query = args[0].lower()
    if query in ("up", "down"):
        cur = sp.current_playback()
        cur_vol = cur["device"]["volume_percent"] if cur and cur.get("device") else 50
        vol = min(100, cur_vol + 10) if query == "up" else max(0, cur_vol - 10)
    else:
        try:
            vol = int(query)
        except ValueError:
            print(f"ERROR: непонятное значение '{query}'. Используй: volume 70 / volume up / volume down")
            return

    try:
        sp.volume(vol, device_id=device_id)
        print(f"🔊 Громкость: {vol}%")
    except Exception as e:
        print(f"ERROR: {e}")


def cmd_devices(args):
    """Список активных Spotify устройств."""
    sp = get_sp()
    devices = sp.devices().get("devices", [])
    if not devices:
        print("Нет активных устройств. Открой Spotify на ноуте.")
        return
    print(f"Устройства ({len(devices)}):")
    for d in devices:
        active = "← активное" if d["is_active"] else ""
        print(f"  {d['name']} ({d['type']}) | {d['id']} {active}")
        print(f"  vol:{d['volume_percent']}%")


def cmd_queue(args):
    """Добавить трек в очередь воспроизведения.
    queue TRACK_URI
    queue "название трека"
    """
    if not args:
        print("ERROR: укажи трек URI или название")
        sys.exit(1)
    sp = get_sp()
    device_id = ensure_active_device(sp)
    query = " ".join(args)

    if query.startswith("spotify:track:"):
        uri = query
    else:
        results = sp.search(q=query, type="track", limit=1)
        items = results["tracks"]["items"]
        if not items:
            print(f"ERROR: трек '{query}' не найден")
            return
        track = items[0]
        uri = track["uri"]
        artists = ", ".join(a["name"] for a in track["artists"])
        print(f"Найден: {track['name']} — {artists}")

    try:
        sp.add_to_queue(uri, device_id=device_id)
        print(f"✅ Добавлен в очередь: {uri}")
    except Exception as e:
        print(f"ERROR: {e}")


def cmd_shuffle(args):
    """Перемешать / выключить перемешивание.
    shuffle on / shuffle off / shuffle (переключить)
    """
    sp = get_sp()
    device_id = ensure_active_device(sp)
    if not args:
        cur = sp.current_playback()
        state = cur.get("shuffle_state", False) if cur else False
        new_state = not state
    else:
        new_state = args[0].lower() in ("on", "true", "1", "вкл")

    try:
        sp.shuffle(new_state, device_id=device_id)
        print(f"🔀 Shuffle: {'вкл' if new_state else 'выкл'}")
    except Exception as e:
        print(f"ERROR: {e}")


COMMANDS = {
    "top-tracks": cmd_top_tracks,
    "top-artists": cmd_top_artists,
    "recent": cmd_recent,
    "liked": cmd_liked,
    "liked-all": cmd_liked_all,
    "liked-by-artist": cmd_liked_by_artist,
    "playlists": cmd_playlists,
    "create-playlist": cmd_create_playlist,
    "add-to-playlist": cmd_add_to_playlist,
    "search": cmd_search,
    "genres": cmd_genres,
    "now": cmd_now,
    "track-info": cmd_track_info,
    "related-artists": cmd_related_artists,
    "artist-top-tracks": cmd_artist_top_tracks,
    "make-playlist": cmd_make_playlist,
    "discover": cmd_discover,
    # Playback (Premium)
    "play": cmd_play,
    "pause": cmd_pause,
    "next": cmd_next,
    "prev": cmd_prev,
    "volume": cmd_volume,
    "devices": cmd_devices,
    "queue": cmd_queue,
    "shuffle": cmd_shuffle,
}

if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] not in COMMANDS:
        print("Доступные команды:")
        for cmd in sorted(COMMANDS):
            print(f"  python3 /Users/mixx/.openclaw/scripts/spotify.py {cmd}")
        sys.exit(1)

    cmd = sys.argv[1]
    args = sys.argv[2:]
    COMMANDS[cmd](args)
