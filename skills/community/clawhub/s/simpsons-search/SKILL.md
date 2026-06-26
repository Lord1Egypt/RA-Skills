---
name: simpsons-search
description: Search and reference Simpsons episode scripts using Springfield! Springfield! as the source, with an optional local episode index for faster lookups. Use when a user asks for Simpsons quotes, wants to identify an episode by line or scene, compare recurring jokes or characters, or find short script excerpts and source links.
---

# Simpsons Search

Use this skill to find Simpsons quotes and episode scripts without stuffing a giant corpus into context.

## Source

Primary source:
- `https://www.springfieldspringfield.co.uk/episode_scripts.php?tv-show=the-simpsons`

Preferred approach:
- keep a local episode index with titles + URLs
- optionally build a local searchable corpus cache for better quote accuracy
- fetch individual script pages when needed or while building the corpus
- return short excerpts plus the source link

Default to the index first. Build the corpus when the user wants stronger quote/scene search quality.

## Workflow

1. Read the local index at `references/simpsons-episodes.json` if it exists.
2. If the index is missing or stale, refresh it with `scripts/build_index.py`.
3. Search the index by episode title when the user asks for a known episode.
4. Search the website or fetched script text when the user asks for:
   - a quote fragment
   - a scene description
   - a character/topic pattern
5. When the user wants a character voice or impression, read `references/simpsons-characters.json` or use the helper scripts first.
6. Return:
   - episode title or character name
   - script URL when relevant
   - a short excerpt, summary, or character brief
   - note when the match is approximate

## Files

- `references/simpsons-episodes.json` — local metadata index of episode titles and URLs
- `references/cache/` — cached fetched script pages
- `references/simpsons-corpus.json` — optional local searchable corpus cache
- `references/simpsons-characters.json` — grounded character briefs for impressions and style matching
- `references/simpsons-character-evidence.json` — script-derived evidence lines and episode presence for seeded characters
- `references/simpsons-character-dossiers.json` — richer auto-built dossiers with top terms, related characters, and candidate catchphrases
- `scripts/build_index.py` — rebuild the episode index from the source page
- `scripts/build_corpus.py` — fetch/cache scripts and build a local searchable corpus
- `scripts/build_search_index.py` — build a lightweight inverted index for faster quote lookups
- `scripts/build_character_dossiers.py` — synthesize richer character dossiers from the corpus
- `scripts/find_episode.py` — fuzzy local search over the index
- `scripts/find_quote.py` — quote/topic search using the search index + local corpus when available, otherwise cached fetched pages
- `scripts/find_character.py` — fuzzy character lookup over the local character briefs
- `scripts/character_brief.py` — human-readable character brief and imitation prompt
- `scripts/extract_character_evidence.py` — derive character evidence snippets from the local script corpus
- `scripts/rewrite_as_character.py` — build a rewrite/imitation prompt package for a target character
- `scripts/speak_as_character.py` — assemble a direct style guide package for replying as a chosen character

## Common tasks

### Find by title

Run:

```bash
python3 scripts/find_episode.py "steamed hams"
```

Then fetch the matched page if needed.

### Find by quote fragment or topic

Run:

```bash
python3 scripts/find_quote.py "steamed hams"
```

Behavior:
1. Prefer the local corpus if `references/simpsons-corpus.json` exists.
2. Otherwise use the local index to shortlist candidates and fetch/cache likely script pages.
3. Rank matches by phrase hit, term coverage, and term frequency.
4. Return short excerpts with source links.

To build the stronger corpus cache:

```bash
python3 scripts/build_corpus.py
python3 scripts/build_search_index.py
```

### Find a character voice

Run:

```bash
python3 scripts/find_character.py "mr burns"
python3 scripts/character_brief.py "mr burns"
```

Use the returned brief before writing in-character text. Base the imitation on role, traits, rhythm, themes, and recurring attitudes.

To ground the brief with script evidence:

```bash
python3 scripts/extract_character_evidence.py
```

To generate a rewrite prompt package:

```bash
python3 scripts/rewrite_as_character.py "moe" "i can't believe this meeting is still going"
```

To build richer dossiers:

```bash
python3 scripts/build_character_dossiers.py
```

To get a direct speaking-style package:

```bash
python3 scripts/speak_as_character.py "mr burns" "complain about modern coffee shops"
```

## Notes

- The local index is for discovery, not full-text script storage.
- The corpus improves quote accuracy but still depends on script-source quality.
- Character briefs are grounded style guides, not a claim of perfect canon simulation.
- If a quote search needs broader coverage, search the web first, then fetch the specific script page.
- Be explicit when the source appears user-maintained or imperfect.
- Keep excerpts short and useful.
