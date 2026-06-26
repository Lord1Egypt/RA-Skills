# Spotify Playlist Curator

## Install

**OpenClaw:**
```bash
clawhub install spotify-playlist-curator
```

---

An [OpenClaw](https://github.com/openclaw/openclaw) skill that gives AI agents musical intuition. I built this because I was unsatisfied with Spotify’s existing music recommendation features. It allows AI agents to reason deeply about music, getting recommendations based on user requests and then critically considering which ones to include in the playlist it’s making. It gives them a framework that includes audio DNA profiling, multi-source recommendations with scored explanations, and tools for blending aesthetics across artists and genres. And since there’s so much room for thinking and personalization, it provides lots of surface area for fun emergent behavior!

## What can it do?

Describe what you want in natural language. The agent translates your intent into audio features, artist networks, and genre affinities, then builds a playlist grounded in real data.

**Some examples:**

- *"Make me a playlist that combines the sound of Lana Del Rey's 'Venice Bitch' with Mitski's 'My Love Mine All Mine', about an hour long, and don't include 'Mariner's Apartment Complex'"* — seeds from specific tracks, blends both artists' sonic profiles, trims to duration, excludes the named track
- *"Based on the songs I've been listening to lately, pick the high-energy ones and put a playlist together for my gym session. Throw in a few new ones that match the vibe"* — pulls recent listening history, filters by energy and danceability, seeds recommendations from the top matches
- *"Take my road trip playlist and make it more upbeat without losing the indie feel"* — analyzes the existing playlist's audio DNA, recommends tracks that boost energy and danceability while preserving genre affinity
- *"A playlist of only Bjork and Radiohead deep cuts"* — pulls artist catalogs directly, filters by popularity
- *"Find my 'March 2026' playlist, remove all the Drake songs, and add some more relaxed tracks that pair well with what's left"* — locates the playlist by name, removes specific artist's tracks, analyzes the remaining audio profile, recommends new tracks that match

The agent explains its reasoning at every step: which seeds it chose and why, what audio features it's targeting, and what trade-offs it made.

## How it works

The skill is built around three ideas:

### 1. Musical vocabulary

Audio features (energy, danceability, valence, acousticness, tempo, loudness) aren't just numbers — they map to musical concepts the agent uses to reason about requests. "Melancholic" means low valence + moderate energy. "Intimate" means low loudness + high acousticness. The agent speaks this language when making and explaining decisions.

### 2. Multi-source recommendation engine

A 3-tier fallback chain ensures recommendations work even as Spotify deprecates endpoints:

- **Tier 1** — [ReccoBeats](https://reccobeats.com) for similarity-based recommendations and audio feature data
- **Tier 2** — Audio-feature scoring when ReccoBeats recommendations are unavailable but feature data still is
- **Tier 3** — Spotify-only fallback using search, genre overlap, and artist proximity

Each tier produces scored results with human-readable explanations (`"genre match"`, `"audio match: energy=0.05, valence=0.03"`, `"boosted artist"`), so the agent can evaluate and adjust before committing.

### 3. DNA blending

For fusion requests ("X meets Y", "blend these two playlists"), `blend-dna` profiles two track groups independently, computes a target zone in audio-feature space, then scores candidates by how well they sit in the overlap. The output includes per-feature distances so the agent can see exactly where a track falls relative to both source aesthetics.

## Features

| Capability | Details |
|---|---|
| Natural language playlists | Describe a vibe, mood, or reference point — the agent handles seed selection, genre targeting, and audio feature alignment |
| Seed from anything | Specific tracks, artists, existing playlists, genres, or your listening history |
| Audio DNA profiling | Analyze any playlist or set of tracks for energy, danceability, valence, acousticness, tempo, loudness, and more |
| Aesthetic blending | Fuse two distinct musical identities with adjustable weighting |
| Scored recommendations | Every recommendation comes with a composite score and reasons — the agent curates, not just retrieves |
| Constraint mapping | "no X", "more Y", "deep cuts", "bangers", "about an hour" — natural language constraints map to CLI flags |
| Taste memory | Excluded artists, favorite genres, and free-text notes persist across sessions |
| Listening history | Pull from recent plays, top tracks, and top artists across time ranges |
| Playlist operations | Create, modify, analyze, queue tracks, search catalog |

## Setup

### Prerequisites

- Python 3.9+
- A [Spotify Developer](https://developer.spotify.com/dashboard) app (free)
- [OpenClaw](https://github.com/openclaw/openclaw) installed

### 1. Install and set up dependencies

```bash
clawhub install spotify-playlist-curator
cd spotify-playlist-curator
bash scripts/setup.sh
```

### 2. Configure Spotify credentials

Create an app at [developer.spotify.com/dashboard](https://developer.spotify.com/dashboard). Set the redirect URI to `http://127.0.0.1:8888/callback`.

Add your credentials to `.env`:

```
SPOTIPY_CLIENT_ID=your_client_id_here
SPOTIPY_CLIENT_SECRET=your_client_secret_here
```

### 3. Authenticate

```bash
.venv/bin/python scripts/spotify_auth.py
```

This opens a browser for Spotify OAuth consent and saves your tokens locally.

### 4. Register as an OpenClaw skill

Add the skill to your OpenClaw configuration so the agent loads it automatically for music-related requests.

### 5. Verify

Ask OpenClaw to check the connection:

```
> check my spotify connection status
```

The agent will run `status` and confirm authentication is working.

## Architecture

```
You ──→ OpenClaw ──→ SKILL.md (musical reasoning framework)
                        │
                        ├── Spotify Web API
                        │     playlists, search, playback, listening history
                        │
                        ├── ReccoBeats API
                        │     recommendations, audio features
                        │
                        └── MusicBrainz API
                              genre data (cached 30 days)
```

The skill file (`SKILL.md`) isn't just API documentation — it's a reasoning framework that teaches the agent how to think about music. It includes a musical vocabulary, a 6-step workflow for non-trivial requests, a diagnostic table for when recommendations miss the mark, and guardrails for playlist modification.

## Spotify API status (March 2026)

This project works around several Spotify Web API regressions:

| Endpoint | Status | Workaround |
|---|---|---|
| `GET /recommendations` | Removed | ReccoBeats + fallback chain |
| `GET /audio-features` | Removed | ReccoBeats audio features |
| `GET /artists/{id}/related-artists` | Removed | Collaborator discovery via ReccoBeats |
| `GET /artists/{id}/top-tracks` | 403 | Search-based fallback |
| `GET /artists?ids=` (batch) | 403 | Individual artist requests |
| `GET /search` limit | Capped at 10 | Automatic clamping |

See [`references/implementation-notes.md`](references/implementation-notes.md) for full details on each regression and workaround.

## License

MIT
