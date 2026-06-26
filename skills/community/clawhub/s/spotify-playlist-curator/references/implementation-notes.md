# Implementation Notes

## Deprecated Spotify endpoints

The following endpoints have been removed or deprecated by Spotify and are **not available**:

- `GET /recommendations` — removed entirely
- `GET /audio-features` — removed entirely
- `GET /artists/{id}/related-artists` — removed entirely
- `GET /artists/{id}/top-tracks` — returns 403 as of March 2026

The recommendation engine works around these gaps using what still works: search (with genre/artist filters), artist info, album tracks, and user listening data. Artist top tracks uses a search-based fallback since the native endpoint is broken.

## Recommendation engine

### Architecture (3-tier fallback chain)

```
Spotify  ──── playlists, playback, search, listening history, seed resolution
ReccoBeats ── recommendations, audio features, scoring data
Bridge: Spotify track ID → GET /v1/track?ids= → ReccoBeats UUID
```

The `recommend()` method resolves seeds, then uses a 3-tier fallback chain:

```
Tier 1: ReccoBeats recs (_recommend_via_reccobeats)
  ↓ empty results or exception
Tier 2: Audio-feature fallback (_recommend_audio_fallback) — playlist-seeded only
  ↓ no playlist features, empty results, or exception
Tier 3: Spotify-only fallback (_recommend_spotify_fallback) — genre overlap, no audio data
```

Tier 2 is only attempted when `playlist_audio_features` is non-empty (i.e., the request was seeded from a playlist). It uses ReccoBeats `get_audio_features` (a different endpoint than recommendations), so it works even when the recommendation endpoint is broken. If ReccoBeats is completely down, it catches the exception and falls through to Tier 3.

### ReccoBeats path (`_recommend_via_reccobeats`)

1. **Seed resolution** — normalize inputs into `seed_track_ids` (concrete Spotify track IDs):
   - From `--seed-uris`: extract track ID from URI
   - From `--seed-playlist`: take `representative_seed_uris` from `analyze_playlist()`
   - From `--artists`: search Spotify for artist, take top track or search result
   - From `--genres`: search Spotify for genre tracks (`genre:"trip hop"` → tracks)
   - Capped at 10 seed tracks

2. **ID bridging** — `resolve_track_ids(seed_track_ids)` → ReccoBeats UUIDs

3. **Candidate generation** — `get_recommendations(seed_uuids, size=limit*2)` → relevance-ordered tracks

4. **Scoring** — each candidate scored with:
   - Position score (40%): earlier in ReccoBeats results = more similar
   - Audio feature alignment (25%): Euclidean distance from seed avg (energy, danceability, valence)
   - Popularity match (20%): distance from target
   - Boost: +0.15 for boosted artists
   - If audio features unavailable: position (55%) + popularity (30%)

5. **Filtering** — max-per-artist cap, sort by score, return top N

### Audio-feature fallback path (`_recommend_audio_fallback`)

Uses the playlist's audio profile as a target and scores candidates by weighted audio-feature distance. Only available for playlist-seeded recommendations.

1. **Target extraction** — takes `avg` values from `playlist_audio_features` for each feature in `_BLEND_FEATURES`
2. **Candidate sourcing** — same as ReccoBeats path: search for seed artist names + collaborator discovery from co-artists
3. **Scoring** — delegates to `score_candidates_by_audio_features()`, then converts to recommend output format:
   - `audio_score = max(0, 1.0 - distance)` (inverted so higher = better)
   - `final_score = audio_score * 0.70 + pop_score * 0.30`
   - `reasons` include natural-scale deltas: `"audio match: Δenergy=0.05, Δvalence=0.03, Δtempo=3.2 BPM"`
4. **Filtering** — max-per-artist cap, boost (+0.15), sort by score desc, return top N

### `score_candidates_by_audio_features()` helper

Reusable scoring primitive that computes weighted audio-feature distance from a target profile. Used by:
- `_recommend_audio_fallback()` — automatic fallback in the recommend chain
- `score-by-features` CLI command — standalone scoring for manual curation

Takes a target profile (feature→value in natural scale), candidate track IDs, and optional pre-fetched metadata. Returns candidates sorted by ascending distance with per-feature `feature_deltas` showing value, target, and delta in natural scale.

Reuses `_BLEND_FEATURES`, `_BLEND_WEIGHTS`, and `_normalize_feature()` from the DNA blending system.

### Spotify fallback path (`_recommend_spotify_fallback`)

The original recommendation engine, preserved as Tier 3 fallback:

1. **Candidate generation** — multi-source funnel (~20-30 Spotify API calls): artist name search (fallback for broken top-tracks endpoint), genre search, cross-genre discovery
2. **Scoring** — genre overlap (35%) + artist proximity (30%) + popularity (20%) + freshness (15%)
3. **Filtering** — same as ReccoBeats path

### API budget comparison

| Path | Typical API calls | Latency |
|---|---|---|
| ReccoBeats | 2-4 ReccoBeats + 1-3 Spotify (seed resolution) | ~2-4s |
| Spotify fallback | 20-30 Spotify calls | ~15-30s |

### ReccoBeats API notes

- **No auth required** — standalone calls work without Spotify tokens
- **Accepts Spotify track IDs** via `/v1/track?ids=` — the ID bridge
- **Max 5 seeds for recommendations** — `/v1/track/recommendation` returns 400 (`"size must be between 1 and 5"`) if `seeds` contains more than 5 UUIDs. The client caps at 5 automatically. Previously caused noisy 400 errors when playlist-seeded recommendations resolved 6+ seed tracks.
- **No genre concept** — genres are converted to seed tracks via Spotify search
- **No track search** — must resolve through Spotify first
- **Rate limits undisclosed** — no issues observed in testing (~300ms response times)
- **`size` not `limit`** — recommendation endpoint uses `size` parameter
- **Audio feature filters silently return empty** — don't use them; fetch features separately

### `_get_artist_top_tracks` / `get_artist_top_tracks`

`_get_artist_top_tracks(artist_id)` calls `GET /artists/{id}/top-tracks` directly via `_api_request`. This endpoint returns **403 Forbidden** as of March 2026 (confirmed across multiple artists and auth methods, including with `market` parameter).

The public `get_artist_top_tracks(artist_name)` method resolves the artist name via search, tries the native endpoint first, then falls back to `search_track(f'artist:"{name}"', limit=10)` filtered by artist ID. Results are capped at 10 (Spotify search limit) and are relevance-ordered rather than popularity-ordered, but overlap heavily with what the native endpoint used to return.

## Discovery

The `discover` command is now a thin wrapper around `recommend()`, stripping score/reasons fields for backward compatibility.

### `GET /artists?ids=` returns 403 — URL encoding bug (fixed) + Spotify regression (ongoing)

The batch artist endpoint was returning **403 Forbidden** for two compounding reasons:

1. **Our URL encoding bug (fixed)**: code passed `params={"ids": "a,b,c"}` to `requests.request()`, which percent-encodes commas as `%2C`. Spotify's batch endpoint requires raw commas as delimiters. Fix: IDs are now embedded directly in the URL string (`f"artists?ids={','.join(batch)}"`).
2. **Spotify-side regression (ongoing)**: even with correctly-formatted URLs (raw commas), the batch endpoint still returns 403 as of March 2026.

**Impact**: The individual-artist fallback remains the actual working path. The encoding fix is correct code hygiene and will work automatically once Spotify fixes the endpoint.

**Status**: Spotify-side issue. Re-test periodically.

### Known regression: search API limit capped at 10 (as of March 2026)

`GET /search` returns **400 Invalid limit** for any `limit` value above 10. Previously supported up to 50.

**Workaround**: `search_track` clamps `limit` to `min(limit, 10)`. The `recommend` engine's artist name search now uses `limit=10` (previously 15, which was silently clamped anyway).

**Status**: Spotify-side change (possibly permanent). No action needed unless they raise the cap again.

## URL encoding and `_api_request`

Python's `requests` library percent-encodes values in the `params` dict. This breaks Spotify endpoints that expect raw commas (batch IDs), dots (field selectors like `tracks.total`), or colons (`spotify:track:` URIs). When calling `_api_request` with special characters in query params, embed them directly in the URL string instead of using `params={}`.

Affected endpoints (fixed):
- `GET /artists?ids=` — commas between IDs
- `GET /playlists/{id}?fields=` — commas and dots in field selectors
- `POST /me/player/queue?uri=` — colons in Spotify URIs

### Playlist response key renames (as of March 2026)

Spotify made two key renames in playlist responses:

1. **`tracks` → `items`** at the top level of `GET /playlists/{id}`. The pagination wrapper (containing `total`, `items`, `next`, etc.) moved from `data["tracks"]` to `data["items"]`. `get_playlist_info` normalizes this so callers can continue using `data["tracks"]["total"]`.

2. **`track` → `item`** inside individual playlist item objects. Each entry in the items array now uses `{"item": {...}}` instead of `{"track": {...}}`. Both `_fetch_items_endpoint` and `_fetch_tracks_via_playlist_object` check both keys.

These renames caused what appeared to be a widespread Spotify regression (all playlists returning 0 tracks). The data was always there — our code was reading the old keys.

## API quirks

- `list_playlist_tracks` fetches full track objects (no `fields` param) to avoid silent data loss with local files, podcasts, or edge-case response formats.
- Some playlist operations use direct Web API requests rather than Spotipy helpers.

### Known regression: /playlists/{id}/items returns 403 for some third-party playlists

Spotify's `GET /playlists/{playlist_id}/items` endpoint returns **403 Forbidden** for some playlists not owned by the authenticated user. The full playlist object (`GET /playlists/{id}`) also omits track data for these playlists.

**Known affected**: `1MkKWo8Ggs8TpD6dJi1JSp` ("the witches are angry", owned by "mars") — 403 on `/items`, no track data in full object.

**Previously misdiagnosed**: Most "empty results" were caused by Spotify renaming the `track` key to `item` in playlist item objects (see "Playlist response key renames" above). After fixing the key lookup, all user-owned playlists return tracks normally.

**Community thread**: https://community.spotify.com/t5/Spotify-for-Developers/403-Forbidden-on-all-playlist-track-requests-even-with-new-app/td-p/7367439

**Workaround**: `list_playlist_tracks` falls back to `GET /playlists/{id}` (with embedded tracks) when `/items` returns 403. For the genuinely affected playlists where even this fails, there is no workaround.

**Status**: Spotify-side issue for a small number of third-party playlists. Re-test periodically.

## DNA blending

### Algorithm

`blend_dna()` fuses the audio DNA of two track groups:

1. **Profile extraction** — fetch audio features for both groups, compute per-feature mean/std/min/max
2. **Blend target** — for each feature, compute a "target zone":
   - Center = weighted average of two group means (default 50/50, adjustable via `weight_a`)
   - Tolerance = half the gap between means + average std, floored at 0.08
   - Zone = [center - tolerance, center + tolerance]
3. **Candidate sourcing** — multiple strategies:
   - ReccoBeats recommendations from combined seeds (may 400 for some seed combos)
   - Search by artist names (`--search-artists`)
   - Search by free-text queries (`--search-queries`)
   - Explicit candidate URIs (`--candidate-uris`)
4. **Scoring** — for each candidate, compute weighted distance from blend center across 8 features:
   - energy (20%), valence (20%), danceability (15%), acousticness (15%)
   - loudness (10%), tempo (10%), instrumentalness (5%), speechiness (5%)
   - Score = 1.0 at center, decays to 0.0 at 2× tolerance
5. **Filtering** — max-per-artist cap, sort by score, return top N

### Feature normalization

Loudness and tempo are normalized to 0-1 for distance computation:
- Loudness: `(value + 60) / 60` (maps -60 dB → 0.0, 0 dB → 1.0)
- Tempo: `(value - 50) / 150` (maps 50 BPM → 0.0, 200 BPM → 1.0)

### JSON output structure

The output is designed for agent reasoning:
- `group_a.profile` / `group_b.profile` — per-feature stats (mean, std, min, max)
- `blend_target` — per-feature center and zone boundaries
- `candidates[].feature_distances` — per-feature value, target, and `in_zone` boolean
- `candidates[].reasons` — human-readable explanation ("8/8 features in blend zone", "energy=0.70 (target 0.54)")

### When to use blend-dna vs recommend

| Situation | Use |
|---|---|
| Simple single-vibe request | `recommend` |
| Two distinct aesthetics to fuse | `blend-dna` |
| `recommend` returns 400 or off-vibe results | `blend-dna` |
| Need to explain *why* tracks fit | `blend-dna` (per-feature distances) |
| Quick discovery from seeds | `recommend` or `discover` |

## Output style

Prefer stable, concise CLI output that is easy for an agent to parse and summarize.

All methods return enriched track dicts with: name, artists, artist_ids, uri, id, popularity, duration_ms, explicit, release_date, album. Existing text output only displays name/artists/uri; new fields are visible in `--json` mode.

## Large playlist handling

Both `analyze_playlist()` and `blend_dna()` can hang or get killed on very large playlists (500+ tracks) due to unbounded API calls. Guardrails:

### `analyze_playlist()`

- `max_tracks` param (default 200): caps `list_playlist_tracks()` to avoid fetching 900+ tracks. Output includes `sampled: true`, `declared_total`, and a warning when sampling occurs.
- Artist info capped at 100 unique artists: the batch `GET /artists?ids=` endpoint returns 403, so the individual-artist fallback runs N requests. Capping at 100 prevents 300+ sequential API calls.
- Audio features already sampled at 30 tracks (via ReccoBeats).

### `blend_dna()`

- `max_tracks_per_group` param (default 100): caps tracks loaded per group.
- Audio features sampled at 50 tracks per group for profiling.
- Output includes `features_sampled` count and `sampling_note` when sampling occurs.

### CLI flags

- `analyze-playlist --max-tracks N` (default 200, 0 = unlimited)
- `blend-dna --max-tracks-per-group N` (default 100, 0 = unlimited)

Defaults are tuned so commands complete in under 15 seconds for any playlist size.

## Artist name normalization

All artist name comparisons (exclude filters, boost filters, seed deduplication, `search_artist_misses`) use `_normalize_name()`, which lowercases and strips diacritics via NFD decomposition. This ensures `"Touche Amore"` matches `"Touché Amoré"`, `"Beyonce"` matches `"Beyoncé"`, etc.

Without this, `--exclude-artists` and `--boost-artists` silently fail for any artist with accented characters — the user types the ASCII version but Spotify returns the accented form.

## Exclude-artists safety net

The `recommend()` method applies a `_final_exclude_filter()` to the return value of all three tiers in the fallback chain. This is defense-in-depth: each tier has its own per-candidate exclude check during scoring, but edge cases (seed artist resolution, collaborator discovery, featured appearances) can leak excluded artists into results. The final filter guarantees no leaks regardless of which tier produced the results.

## Audio-features `_not_found` reporting

When `audio-features` is called with `--json`, the output includes a `_not_found` array listing any track IDs that ReccoBeats couldn't resolve. This lets the agent know which tracks have no feature data and adjust its candidate pool accordingly. The underscore prefix avoids collision with track ID keys. When all tracks are found, output is unchanged (no breaking change).

## Safety

- Do not modify existing playlists unless explicitly asked.
- Prefer creating new playlists for experiments and iterations.
- Avoid dumping stack traces to the user when setup or auth fails.
