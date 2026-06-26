---
name: spotify-playlist-curator
description: Create and refine Spotify playlists using the Spotify Web API, with support for track search, recent and top listening lookups, queueing selected tracks, and curated playlist generation from vibes, seed tracks, and listening history. Use when a user wants a new playlist, wants tracks added to a playlist, wants songs similar to a song, artist, or mood, or wants a few selected songs queued.
---

# Spotify Playlist Curator

Use this skill for Spotify playlist creation, song selection, listening-history lookups, and lightweight queue actions.

**The tools below are means to musical understanding, not API documentation to follow.** Understand the musical goal first, translate it to data (audio features, artists, temporal filters), chain tools creatively, and explain your choices so the user understands the thinking.

## Core rules

- Prefer creating new playlists over modifying existing ones.
- Do not modify existing playlists unless the user explicitly asks.
- When revising a generated playlist, prefer versioned copies like `(v2)`, `(softer)`, or `(more dancey)`.
- Use queue only for explicit queue requests.
- Be honest that discovery is heuristic. Use it to supplement curation, not replace judgment.
- Always use `--json` mode when composing multi-step workflows. Parse JSON output; do not scrape text.
- Before your first recommendation call, run `taste show` to check the user's taste profile. Excluded artists are enforced automatically, but favorite genres and notes may inform your seed/genre choices.
- When the user expresses a taste preference ("I don't like X", "I love Y", "never include Z"), save it to the taste profile so it persists across sessions.
- If the user explicitly requests an artist that appears in the taste profile's excluded list (e.g., "make me a Taylor Swift playlist" when Taylor Swift is excluded), inform them of the conflict and ask if they'd like to make an exception for this playlist. Do not silently override the exclusion or silently produce empty/confusing results.

## Environment pre-check

Before your first CLI call, check that the environment is set up:

1. **Check for `.venv`** — if the `.venv` directory does not exist in the skill root, tell the user to run setup first:
   ```bash
   bash scripts/setup.sh
   ```
   Do not attempt to create the venv yourself or install dependencies manually. The setup script handles everything including credential prompts.

2. **Check auth** — once `.venv` exists, verify authentication:
   ```bash
   .venv/bin/python scripts/spotify_cli.py --json status
   ```
   If `authenticated` is false, tell the user to run the auth flow:
   ```bash
   .venv/bin/python scripts/spotify_auth.py
   ```

Do not attempt other commands until `status` returns `authenticated: true`.

### Common setup errors

| Error | Cause | What to tell the user |
|---|---|---|
| `invalid_client` or "client ID invalid" | The `.env` file has placeholder values or incorrect credentials | Open `.env` in the skill root, replace `your_client_id_here` / `your_client_secret_here` with real credentials from https://developer.spotify.com/dashboard, then re-run `spotify_auth.py` |
| `credentials not found` or "placeholder values" | Setup ran but user didn't edit `.env` | Same as above — they need to create a Spotify app and paste the credentials |
| `no such file or directory: .venv/bin/python` | `.venv` doesn't exist | Run `bash scripts/setup.sh` from the skill root first |
| `redirect_uri_mismatch` | Spotify app's redirect URI doesn't match | In the Spotify developer dashboard, set the redirect URI to `http://127.0.0.1:8888/callback` |

## Spotify API constraints (as of March 2026)

Before calling any CLI command, be aware of these active Spotify API regressions. They **will** cause silent failures or 403/400 errors if you ignore them.

1. **Search limit is capped at 10.** `--limit` values above 10 on `search` return `400 Invalid limit`. The CLI handles this internally, but do not expect more than 10 results from a single search call.
2. **Batch artist endpoint (`GET /artists?ids=`) returns 403.** The code falls back to individual `GET /artists/{id}` calls automatically.
3. **Playlist responses renamed `tracks` to `items` and `track` to `item`.** The code normalizes both renames automatically.
4. **`GET /playlists/{id}/items` returns 403 for some third-party playlists** (not owned by the authenticated user). User-owned playlists work normally.
5. **`GET /recommendations`, `GET /audio-features`, and `GET /artists/{id}/related-artists` are removed entirely.** The `recommend` command works around this using ReccoBeats as the primary recommendation + audio features backend, with Spotify-only fallback.
6. **Recommendations and audio features now come from ReccoBeats** (`api.reccobeats.com`). No auth required. Spotify handles playlists, search, playback, and listening history. ReccoBeats handles recommendations and audio features. If ReccoBeats is unavailable, the system falls back to Spotify-only recommendation (search + artist top tracks + genre scoring).
7. **Artist endpoints no longer return genre data.** Both batch and individual artist endpoints return `null` for genres. Genre-based filtering in `blend-dna` uses **MusicBrainz** as the primary genre source (free, no API key, cached to disk for 30 days), with Spotify genre-search membership as a fallback when MusicBrainz has no data for an artist.
8. **`GET /artists/{id}/top-tracks` returns 403.** The `artist-top-tracks` command falls back to search automatically.

See `references/implementation-notes.md` for full details on each regression and workaround.

## Quick-reference table

For simpler cases:

| Request type | Approach |
|---|---|
| "Add [specific songs] to [playlist]" | `search` → `add-to-playlist` |
| "Playlist from my recent listening" | `create-from-recent` (one command) |
| "Playlist from my top tracks" | `create-from-top` (one command) |
| "Queue [song]" | `search` if needed → `queue` |
| "What have I been listening to?" | `recent` / `top-tracks` / `top-artists` |
| "Latest song by [artist]" | `artist-releases` → `add-to-playlist` or `queue` |
| "Playlist of only X and Y" | `artist-top-tracks` + `artist-releases` → `create-playlist` + `add-to-playlist` |
| Artist-centric / vibe-based / fusion | Use the 6-step workflow below |

## Choosing the right recommendation tool

Pick the tool based on the request shape:

| Request type | Tool | Why |
|---|---|---|
| "Songs like X" / "more of this vibe" | `recommend --seed-uris` | Best for expanding from known tracks |
| "Artists like X, Y, Z" / scene-based | `recommend --artists` | Discovers collaborator network + seeds from those artists |
| "Blend of X and Y" / fusion of two aesthetics | `blend-dna` | Profiles both sides and finds the overlap zone. **Use this first for fusion requests** — don't start with `recommend` |
| Quick sonic exploration from a single track | `discover` | Lightweight wrapper: returns similar tracks without scores. Good for Ring 1+ in concentric discovery |
| Manual curation / filling gaps | `search` + `audio-features` | When you need specific tracks and want to verify they fit |

**Key distinction**: `recommend` returns scored results with reasons (useful for explaining choices). `discover` returns raw similar tracks without scores (faster, good for chaining). `blend-dna` is the only tool that profiles two distinct groups and finds the middle ground.

## Constraints and levers

Map user language to CLI flags:

| User says | Flag | Effect |
|---|---|---|
| "no X" | `--exclude-artists "X"` | Filters X out entirely |
| "blend of A and B" | `--max-per-artist 2` | Prevents one artist from dominating |
| "more emphasis on Y" | `--boost-artists "Y"` | +0.15 score boost |
| "deep cuts" / "obscure" | `--popularity-target 25` | Favors less popular tracks |
| "bangers" / "hits" | `--popularity-target 75` | Favors popular tracks |
| "energetic" / "upbeat" | Use seed tracks with high energy/danceability | Audio features steer ReccoBeats recommendations |
| "chill" / "mellow" | Use seed tracks with low energy + high acousticness | Audio features steer ReccoBeats recommendations |
| "nothing from [playlist]" | `--exclude-uris <uris...>` (`recommend` only) | Removes specific tracks from candidates. Not available on `blend-dna` — exclude manually from final track selection. |
| "like X meets Y" / "blend of X and Y" | `blend-dna --group-a <X tracks> --group-b <Y tracks>` | Finds the overlap zone between two aesthetics |
| "lean more toward X" | `blend-dna --weight-a 0.7` (or 0.3 for group B) | Shifts the blend target toward one group |
| "about an hour" / duration target | `--target-duration 60` | Trims results to fit target duration in minutes |
| "indie rock / emo / shoegaze" | `--genres "indie rock" "emo"` | Sources candidates from genre search and boosts genre-matched tracks (available on both `recommend` and `blend-dna`) |

## CLI reference

All commands go through `.venv/bin/python scripts/spotify_cli.py <command>`. Pass `--json` before the command for machine-readable output.

### Status

| Command | Arguments | Notes |
|---|---|---|
| `status` | (none) | Check auth and connection status. Returns `authenticated`, `credentials_found`, `token_exists`, `token_valid`, and `user`. |

### Taste profile

The user's musical preferences are stored in `taste_profile.json` and persist across sessions. **Excluded artists are automatically merged into `--exclude-artists` on every `recommend`, `blend-dna`, and `score-by-features` call** — the agent never needs to pass them manually.

When you learn something about the user's taste (they dislike an artist, love a genre, have a preference), save it to the taste profile so future agents benefit too.

| Command | Arguments | Notes |
|---|---|---|
| `taste show` | (none) | Show the full taste profile |
| `taste exclude` | `<artist>` | Never include this artist in playlists |
| `taste unexclude` | `<artist>` | Remove an artist from the exclusion list |
| `taste fav-genre` | `<genre>` | Record a favorite genre |
| `taste unfav-genre` | `<genre>` | Remove a favorite genre |
| `taste fav-artist` | `<artist>` | Record a favorite artist |
| `taste unfav-artist` | `<artist>` | Remove a favorite artist |
| `taste note` | `<text>` | Add a free-text note about the user's taste |
| `taste rm-note` | `<index>` | Remove a note by index |

### Search and lookup

| Command | Arguments | Notes |
|---|---|---|
| `search` | `<query>` `--limit N` | Max 10 results per call (Spotify API cap) |
| `list-playlists` | `--limit N` | Lists user's playlists |
| `list-playlist` | `<playlist_id>` `--limit N` | Lists tracks in a playlist. May return 403 for third-party playlists — if so, try `analyze-playlist` which has a fallback |
| `top-tracks` | `--time-range {short,medium,long}_term` `--limit N` | User's top tracks |
| `top-artists` | `--time-range {short,medium,long}_term` `--limit N` | User's top artists |
| `recent` | `--limit N` | Recently played tracks |
| `artist-releases` | `<artist_name>` `--limit N` `--include-groups TYPES` | Recent releases with lead track URIs. Default groups: `single,album` |
| `artist-top-tracks` | `<artist_name>` | Top tracks for an artist (~10). Complements `artist-releases` for catalog access |

### Analysis

| Command | Arguments | Returns |
|---|---|---|
| `analyze-playlist` | `<playlist_id>` `--max-tracks N` (default 200, 0=unlimited) | `track_count`, `total_duration_ms`, `avg_popularity`, `popularity_range`, `artist_distribution`, `top_artists`, `genre_clusters`, `top_genres`, `explicit_ratio`, `representative_seed_uris`, `audio_features` (avg/min/max per feature), `audio_features_sample_size`, `tracks`. Large playlists are sampled automatically — output includes `sampled`, `declared_total`, and `warning` when this happens. |
| `audio-features` | `<track_id>...` | Per-track audio features: energy, danceability, valence, acousticness, instrumentalness, speechiness, liveness, tempo, loudness. **No Spotify auth required.** JSON output includes `_not_found` array when any requested track IDs have no features available. |
| `score-by-features` | `--target-playlist ID` `--target-energy F` `--target-valence F` `--target-danceability F` `--target-acousticness F` `--target-tempo F` `--target-loudness F` `--candidate-ids ID...` `--candidate-artists NAME...` `--exclude-artists NAME...` `--limit N` (default 20) `--max-distance F` | Scores candidates by weighted audio-feature distance from a target profile. Target from playlist avg and/or explicit values. Candidates from track IDs and/or artist search. JSON output includes `distance` and per-feature `feature_deltas` (value, target, delta in natural scale). |

### Recommendations

| Command | Arguments | Notes |
|---|---|---|
| `recommend` | `--seed-uris URI...` `--seed-playlist ID` `--genres GENRE...` `--artists NAME...` `--exclude-artists NAME...` `--exclude-uris URI...` `--boost-artists NAME...` `--max-per-artist N` (default 3) `--popularity-target N` `--limit N` (default 20) `--target-duration MINUTES` `--add PLAYLIST_ID` `--create NAME` | At least one seed source required. Output includes `score` and `reasons` per track. `--target-duration` trims results to fit the specified duration. |
| `blend-dna` | `--group-a URI...` `--group-a-playlist ID` `--group-b URI...` `--group-b-playlist ID` `--label-a TEXT` `--label-b TEXT` `--weight-a W` (0.0-1.0, default 0.5) `--search-artists NAME...` `--search-queries QUERY...` `--candidate-uris URI...` `--genres GENRE...` `--exclude-artists NAME...` `--boost-artists NAME...` `--max-per-artist N` `--max-tracks-per-group N` (default 100, 0=unlimited) `--limit N` `--target-duration MINUTES` `--add PLAYLIST_ID` `--create NAME` | Blends audio DNA of two track groups. `--genres` sources candidates from genre search and boosts genre-matched tracks (penalizes unaffiliated tracks). Output includes `search_artist_misses` when specified artists don't appear in final results. `--target-duration` trims results to fit. |
| `discover` | `<seed_uris...>` `--limit N` `--add PLAYLIST_ID` | Wrapper around `recommend` without scores |

### Playlist operations

| Command | Arguments | Notes |
|---|---|---|
| `create-playlist` | `<name>` `--public` `--description TEXT` | Creates empty playlist |
| `add-to-playlist` | `<playlist_id>` `<track_uris...>` | URIs must be `spotify:track:ID` format. Validated before sending |
| `remove-from-playlist` | `<playlist_id>` `<track_uris...>` | Confirm with user first |
| `search-and-add` | `<playlist_id>` `"Artist - Title"...` | For adding specific known tracks. Format must be `"Artist - Title"`. Tracks not found are silently skipped with a warning |
| `update-playlist` | `<playlist_id>` `--name TEXT` `--description TEXT` `--public`/`--private` | Metadata changes |

### Playback and shortcuts

| Command | Arguments | Notes |
|---|---|---|
| `queue` | `<track_uri>` | Requires active Spotify device |
| `create-from-recent` | `<name>` `--limit N` `--public` `--description TEXT` | One-step playlist from recent plays |
| `create-from-top` | `<name>` `--time-range {short,medium,long}_term` `--limit N` `--public` `--description TEXT` | One-step playlist from top tracks |

## How to approach a request

For any non-trivial request (vibes, transformations, fusions, discovery), follow all six steps. For trivial cases (specific songs to add, queue a track), skip to the quick-reference table above.

### Step 1: Understand the request

Restate what the user wants, then identify:

- **Intent**: new playlist / transform existing / add tracks / queue / explore listening history
- **Specificity**: exact songs vs. vibe-based
- **Size**: "short mix" ~8-12, "playlist" ~15-25, "long session" ~30-40+, default 20. If the user specifies a duration, use `--target-duration`.
- **Constraints**: "no X", "more Y", "blend of A and B", popularity preferences

Ask at most one clarifying question if genuinely ambiguous. Do not stall with multiple rounds of clarification.

### Step 2: Gather context

Before generating recommendations, ground yourself in real data.

| Situation | First command | Why |
|---|---|---|
| Transform/extend existing playlist | `--json analyze-playlist <id>` | Get `top_artists`, `top_genres`, `representative_seed_uris`, `audio_features` |
| User names a specific song/artist | `--json search "<query>" --limit 5` | Get exact URI for seeding |
| User wants latest song by an artist | `--json artist-releases "<name>" --limit 5` | Get most recent release URIs to seed or add directly |
| Check audio profile of tracks | `--json audio-features <track_id>...` | Get energy, danceability, valence, etc. (no Spotify auth needed) |
| Playlist of only [artist] | `--json artist-top-tracks "<name>"` | Get artist's top ~10 tracks for direct playlist assembly |
| Small curated playlist (<~30 tracks) | `--json list-playlist <id>` | See every track, pick explicit seeds |
| Vibe-only, no existing playlist | `--json top-artists`, `--json top-tracks`, or `--json recent` | Ground the vibe in the user's taste |

**Key rule**: for non-trivial requests involving an existing playlist, `analyze-playlist` is almost always the right first step.

### Step 3: Draft candidates

Run `recommend` or `blend-dna` in **JSON-only mode** — no `--create`, no `--add` yet.

- Set `--limit` higher than target (e.g., 25-30 for a 20-track playlist) to give yourself room to curate
- Use seed URIs, genres, artists, and constraints derived from Step 2
- **Always pass `--genres`** when the request implies a genre/scene — this dramatically improves result quality by boosting genre-affiliated candidates and penalizing unrelated ones
- If the first pass misses the mark: adjust seeds, add/remove genres, tweak `--boost-artists` or `--exclude-artists`, and run a second pass

Do not finalize on the first pass. Draft first, inspect second.

**Understanding the JSON output:**
- `score`: 0.0-1.0 composite score. Higher = better match.
- `reasons`: array of tags explaining the score (`"genre match"`, `"boosted artist"`, `"no genre/artist affiliation (penalized)"`, etc.)
- `search_artist_misses` (blend-dna only): artists you searched for that didn't make the final results — consider adding them manually
- `_hint`: (optional) appears if there weren't enough scene-affiliated tracks. Follow its instructions.

### Step 4: Inspect and adjust

Review the JSON output from Step 3:

- **Artist balance**: Does the mix match the request? For blends/fusions, check neither artist dominates.
- **Genre affiliation**: Are tracks tagged with `"genre match"` or `"no genre/artist affiliation (penalized)"`? Penalized tracks may still be good — use your judgment.
- **Search artist misses**: If `search_artist_misses` lists artists you wanted, search for them manually and add their tracks.
- **Audio profile**: Check audio features match intent — high energy + danceability = upbeat; low energy + high acousticness = chill; high valence = happy.
- **Trim**: Cut to target count from the bottom of the score ranking.

If the results are off, go back to Step 3 with adjusted parameters.

**When recommendations fail or return off-vibe results:**

| Symptom | Likely cause | Fix |
|---|---|---|
| All results are unrelated to the seeds | ReccoBeats returned global audio matches with no scene constraint | Add `--genres` and `--artists` to constrain the scene |
| Results are too generic/mainstream | Seeds are too popular or broad | Lower `--popularity-target`, use more specific seed tracks |
| 0 results returned | Seeds not found in ReccoBeats, or all candidates filtered out | Try different seed tracks, remove `--exclude-artists`, broaden constraints |
| Fusion request returns one-sided results | `recommend` can't balance two aesthetics | Switch to `blend-dna` with explicit groups |
| Off-genre tracks scoring high | Audio features match but genre doesn't | Add `--genres` to boost genre-matched candidates and penalize unaffiliated ones |

### Step 5: Finalize

Only now commit the tracks:

- **New playlist**: `create-playlist "Name"` then `add-to-playlist <id> <uris...>`, or use `recommend ... --create "Name"` for a fresh run
- **Add to existing**: `add-to-playlist <id> <uris...>`

**Seed track inclusion:** For "inspired by" or "like X and Y" requests, include 2-4 of the strongest seed tracks as anchors in the playlist — they ground the vibe and give the listener familiar touchpoints. For "find me something new" or "discovery" requests, omit the seeds entirely. If unclear, include seeds — the user can always remove them.

### Step 6: Summarize

Tell the user:

- What seeds and constraints were used, and why
- A few anchor tracks and what makes them fit
- Any trade-offs made (e.g., "leaned more electronic because the Bjork seeds pulled that direction")

## Musical vocabulary for reasoning

Audio features are on a **0.0-1.0 scale** (except tempo in BPM and loudness in dB). Use this language when analyzing requests and making decisions:

| Concept | Audio features | Example |
|---|---|---|
| **Melancholic** | Low valence (0.0-0.3) + moderate-to-low energy (0.2-0.5) | Lana Del Rey, Bon Iver, Adrianne Lenker |
| **Upbeat / energetic** | High energy (0.6+) + high valence (0.6+) | Dance, funk, electronic uplifts |
| **Introspective** | Low energy (0.0-0.4) + low danceability (0.2-0.4) | Bedroom pop, lo-fi, indie ballads |
| **Danceable** | High danceability (0.6+) +/- energy/valence | House, pop, hip-hop grooves |
| **Acoustic / organic** | High acousticness (0.6+) | Folk, singer-songwriter, unplugged |
| **Cinematic** | Low tempo + orchestral characteristics (often detected via lower danceability, lower speechiness) | Post-rock, film scores, ambient |
| **Rhythmically complex** | High tempo + low danceability | Prog rock, math rock, jazz fusion |
| **Intimate** | Low loudness + low energy + moderate-to-high acousticness | Whisper vocals, bedroom production |

## Musical thinking framework

Before jumping to API calls, understand what you're solving:

- **"Keep it X-centered"** = find artists/tracks that match X's audio profile (energy, valence, danceability, acousticness)
- **"Add similar artists"** = search for artists in the same genre/vibe, verify with audio-features, cross-check with listening history
- **"Include recent work"** = search for artist + filter by release date or use `artist-releases`
- **"Melancholic" / "upbeat"** = low valence + low energy vs. high valence + high energy; use audio-features to verify
- **"No [artist]"** = explicit `--exclude-artists` filter or post-filter search results
- **"Based on my taste"** = analyze top-artists, recent, and target playlists to understand patterns

### Data tools for musical reasoning

| Tool | Reveals | Use for |
|---|---|---|
| `analyze-playlist` | Audio profile, top artists, genre clusters | Understanding a vibe/aesthetic |
| `audio-features` | Energy, valence, danceability, acousticness, etc. | Verifying tracks match the target profile |
| `top-artists` / `recent` | Your taste patterns across time ranges | Grounding recommendations in actual listening |
| `search` | Tracks by genre, artist, or keyword | Finding candidates that match criteria |
| `artist-releases` | Recent work with exact dates | Filtering for "last year" or "recent" |
| `artist-top-tracks` | Top ~10 tracks for an artist | Building artist-specific playlists without search guesswork |
| `discover` | Similar tracks from seeds (no scores) | Quick sonic exploration — ideal for chaining in concentric discovery |
| `recommend` | Scored candidates with reasons + scene affiliation tags | Primary recommendation tool. Uses collaborator discovery when `--artists` provided |
| `blend-dna` | Per-group profiles, overlap zone, scored candidates with per-feature distances | Fusing two distinct aesthetics. **Use this first for "X meets Y" requests**, not `recommend` |

## Improvisation and deviation

**You are not limited to the patterns above.** They are examples, not recipes.

The north star is: **understand the musical goal, then use the tools creatively to achieve it.**

Examples of valid deviations:
- Combine `analyze-playlist` on multiple playlists to find a common thread, then build from there
- Use `discover` on unexpected seed tracks to find sonic bridges between genres
- Cross-reference `top-artists` with `search` to find obscure collaborators or side projects
- Batch `audio-features` on a large search result set, then sort by multiple features simultaneously
- Use release dates from `artist-releases` to create a chronological playlist showing an artist's evolution
- Analyze two playlists, find their "intersection" (shared audio characteristics), then build outward
- Use audio features to create a "tonal journey" across a playlist (gradually increasing energy, etc.)

**If you can articulate the musical reasoning, the workflow is valid.** Test it, iterate, and explain the choices to the user.

## Setup

The quickest path is the automated setup script:

```bash
bash scripts/setup.sh
```

If you prefer to set up manually, or if the `.venv` doesn't exist yet:

```bash
# 1. Create the virtual environment
python3 -m venv .venv

# 2. Activate it and install dependencies
source .venv/bin/activate
pip install -r requirements.txt
```

Then authenticate (this opens a browser for Spotify login):

```bash
.venv/bin/python scripts/spotify_auth.py
```

After auth completes, verify with `status`:
```bash
.venv/bin/python scripts/spotify_cli.py --json status
```

## References

- `references/setup.md` — environment variables, authentication, and setup details.
- `references/implementation-notes.md` — Spotify API quirks, workarounds, and implementation details. Read this when debugging API-level issues.

---

## Appendix: Worked examples and patterns

The following examples and patterns are reference material for complex requests. You don't need to read these for typical requests — they demonstrate how to chain tools for edge cases.

### Worked example: Radiohead + Bjork blend

**Request**: "blend Radiohead's weird stuff with Bjork's electronic side"

**Step 1** — Restate: fusion playlist, experimental Radiohead + electronic Bjork, ~20 tracks, likely low popularity target.

**Step 2** — Search for specific seed tracks to get URIs:
```bash
.venv/bin/python scripts/spotify_cli.py --json search "Radiohead Everything In Its Right Place" --limit 3
.venv/bin/python scripts/spotify_cli.py --json search "Bjork All Is Full of Love" --limit 3
```

**Step 3** — Draft candidates (using URIs from Step 2):
```bash
.venv/bin/python scripts/spotify_cli.py --json recommend \
  --seed-uris spotify:track:XXXX spotify:track:YYYY \
  --genres "art rock" "electronic" "experimental" "trip hop" \
  --artists "Radiohead" "Bjork" \
  --max-per-artist 3 \
  --popularity-target 45 \
  --limit 30
```

**Step 4** — Inspect: Check Radiohead/Bjork balance, look for bridging artists (Portishead, Thom Yorke solo, Arca), verify `reasons` show genre overlap. If too Radiohead-heavy: `--boost-artists "Bjork"` and rerun. Trim to 20.

**Step 5** — Create the playlist with the curated 20 tracks.

**Step 6** — Summarize: "Seeded from Kid A and Homogenic-era tracks. The blend leans glitchy-electronic with tracks from Arca, Thom Yorke, and Portishead bridging the two."

### Improvisation patterns

**Pattern A: Artist-centric discovery**
1. `analyze-playlist` → understand target audio profile + top artists
2. `search` → find similar artists (from listening history + research)
3. `audio-features` → batch-verify candidates match the profile
4. Post-filter by release date (parse from `artist-releases` if needed)
5. `create-playlist` + `add-to-playlist` → commit to new playlist

**Pattern B: Genre blending** ("Radiohead weird stuff + Bjork electronic")
1. `search` → find seed tracks from each genre/artist
2. `audio-features` → check energy/danceability range of each seed
3. `recommend` → use both seeds with `--genres`, let scoring find bridges
4. Inspect results: do they span the emotional range you want?
5. Iterate: adjust `--genres` or `--boost-artists` if skewed

**Pattern C: Taste evolution** ("Build on my recent listening")
1. `recent` → see what you've been playing
2. `top-artists` (short_term) → find 3-4 dominant artists
3. `search` / `artist-releases` → find their recent collaborators or similar artists
4. `audio-features` → verify new artists match your recent taste
5. Blend: mix new discoveries with favorites

**Pattern D: Temporal filtering** ("Recent releases in the last year")
1. `search` for artist or genre
2. `artist-releases` → check release_date, keep recent only
3. `audio-features` → verify they match the vibe
4. `create-playlist` with curated list

**Pattern E: DNA blending** ("sinister bangers like JOAN OF ARC + the witches are angry")
Use `blend-dna` when the request describes a **fusion of two distinct aesthetics**:
1. Build two seed groups: pick 5-10 tracks each that represent each aesthetic
2. Run `blend-dna --group-a URIs... --group-b URIs... --search-artists "..." --genres "..." --limit 25`
3. Inspect the JSON: check group profiles, blend target, and per-candidate `feature_distances`
4. If results are too skewed toward one group, adjust `--weight-a`
5. Check `search_artist_misses` — manually add any important artists that were filtered out
6. Create playlist from the top-scoring candidates

**Pattern F: Concentric discovery** (scaling depth with playlist length)

When building longer playlists, expand outward in rings:

1. **Ring 0 (core):** Start with the user's seed tracks/artists. Run `recommend` with `--artists` and `--genres`. Take the affiliated results.
2. **Ring 1 (neighbors):** Pick 2-3 top-scoring tracks from Ring 0. Run `audio-features` on them, then `discover` with those as seeds.
3. **Ring 2+ (extended network):** Repeat with Ring 1 results. Stop when `audio-features` shows candidates have drifted too far from Ring 0 DNA (difference > ~0.25 across key features).

Scale rings to playlist size: 10-15 tracks = Ring 0 only; 20-30 = Rings 0+1; 40+ = Rings 0+1+2.

**Pattern G: Audio-feature scoring** (manual curation + vibe verification)

Use `score-by-features` for fine-grained control:
1. Get target profile from `analyze-playlist` or explicit feature values
2. Gather candidates via search or previous recommendations
3. Score: `score-by-features --target-playlist <ID> --candidate-artists "Artist1" "Artist2" --limit 10`
4. Inspect `distance` (lower = closer match) and `feature_deltas`

### Example: Complex request

**Request:** "Check out my playlist (lana's bangers), make a similar playlist that's mostly Lana-centered, include similar artists, keep it recent, exclude Taylor Swift, based on my listening history."

**Agent reasoning:**
```
1. analyze-playlist("lana's bangers")
   → Top artists: Lana, Ethel Cain, MARINA, Paris Paloma
   → Audio: energy=0.43, valence=0.20 (melancholic, introspective)

2. Hypothesis: "Lana-centered" means matching this audio profile + artist aesthetic

3. Search for similar artists (Phoebe Bridgers, Clairo, boygenius, etc.)
   → get_top_artists() + recent to see if user already listens to related artists

4. Batch audio-features on candidates
   → Filter: energy < 0.60 AND valence < 0.50 (match Lana's profile)

5. artist-releases on matches → Keep only recent releases

6. create-playlist("lana's bangers v2") + add verified tracks
   → Exclude Taylor Swift (already in code: --exclude-artists)
```

### Example: DNA blending

**Request:** "Make an absolutely sinister banger playlist centered on 'JOAN OF ARC' by Night Lovell."

**Why `blend-dna` over `recommend`:** The two aesthetics (dark trap + witch house) are too distant for a single recommendation call.

```
1. Build Group A (Night Lovell core): Search → pick 7 tracks
2. Build Group B (witchy core): Search "Chelsea Wolfe", "Lingua Ignota" → pick 6 tracks
3. blend-dna --group-a <URIs> --group-b <URIs>
     --search-artists "Night Lovell" "Ghostemane" "Crystal Castles" "HEALTH"
     --genres "dark trap" "witch house" "industrial"
     --max-per-artist 2 --limit 20
4. Inspect: blend zone = mid-high energy + very low valence + moderate danceability
5. Check search_artist_misses — manually add any that were filtered out
6. Create playlist from top-scoring candidates
```
