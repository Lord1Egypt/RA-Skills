# Language Hints Guide

The Sonic Phoenix pipeline classifies tracks by language using `langdetect`, an
NLP library that analyses artist names and song titles. It works well for Latin-
script European languages but struggles with:

- **Romanised non-Latin languages** — e.g. "Arijit Singh" (Hindi) or "Kenshi
  Yonezu" (Japanese) look like English to the NLP model.
- **Multi-language artists** — e.g. an artist who sings in both Hindi and
  Punjabi may land in the wrong bucket depending on which song the model sees.
- **Short or ambiguous titles** — e.g. "Dil" could be Hindi, Turkish, or a
  brand name.

Language hint files solve this by giving the pipeline explicit overrides that
take priority over NLP guesswork.

---

## Where Hint Files Live

```
sonic-phoenix/
└── config/
    └── language_hints/
        ├── examples/          # Read-only templates shipped with the repo
        │   ├── English.json
        │   ├── Hindi.json
        │   ├── Spanish.json
        │   └── README.md
        ├── Hindi.json         # Your custom hints (create from examples)
        ├── Japanese.json
        └── artist_map.json    # Optional: artist name aliases for 03A
```

- The **filename** (minus `.json`) becomes the language folder name under
  `Sorted/`. So `Hindi.json` drives classification into `Sorted/Hindi/`.
- Create one file per language you want to hint.
- Files in `examples/` are templates — copy them up one level and customise.

---

## Schema

Each hint file is a JSON object with four optional fields:

```json
{
  "artists": ["Arijit Singh", "A.R. Rahman", "Shreya Ghoshal"],
  "dna": ["bollywood", "bhangra", "desi"],
  "keywords": ["ishq", "dil", "pyaar", "zindagi"],
  "lang_codes": ["hi", "pa"]
}
```

### `artists` (list of strings)

Exact artist names that belong to this language. Matching is case-insensitive
substring against the track's artist field.

**When to use:** When you know specific artists the NLP misclassifies.

```json
{
  "artists": [
    "Arijit Singh",
    "A.R. Rahman",
    "Shreya Ghoshal",
    "Atif Aslam",
    "Neha Kakkar",
    "Vishal-Shekhar"
  ]
}
```

### `dna` (list of strings)

Substrings to match against folder names and file paths. Useful for catching
files that passed through genre-specific directories during earlier sorting.

**When to use:** When your collection has genre-flavoured folder names.

```json
{
  "dna": ["bollywood", "bhangra", "desi", "filmi", "indi-pop"]
}
```

### `keywords` (list of strings)

Substrings to match against track titles. Catches language-specific words that
appear in romanised song names.

**When to use:** When song titles contain distinctive words the NLP misses.

```json
{
  "keywords": ["ishq", "dil", "pyaar", "zindagi", "tere", "mujhe"]
}
```

### `lang_codes` (list of strings)

ISO 639-1 language codes that `langdetect` might return for this language. When
the NLP returns one of these codes, the track is classified into this language
bucket even if the confidence is low.

**When to use:** To map NLP codes to your preferred folder name.

```json
{
  "lang_codes": ["hi", "pa", "ur"]
}
```

This maps Hindi (`hi`), Punjabi (`pa`), and Urdu (`ur`) detections all into the
same language folder (whichever file this appears in — e.g. `Hindi.json` puts
them all under `Sorted/Hindi/`).

---

## Which Scripts Consume Hints

| Script | How it uses hints |
| ------ | ----------------- |
| `absolute_zero_sort.py` | Loads all `config/language_hints/*.json` as `LanguageProfile` dataclasses. Classifies files in `Unidentified/Audit_Needed/` using `artists` then `keywords` substring matching. |
| `common_sense_sort.py` | Same logic as `absolute_zero_sort` but non-destructive (leaves Unidentified tree intact). |
| `03A_consolidate_by_artist.py` | Does not read hint files directly, but reads `artist_map.json` (see below). |

---

## Artist Map (`artist_map.json`)

A separate optional file consumed by `03A_consolidate_by_artist.py` to
normalise artist name spelling variants:

```json
{
  "AR RAHMAN": "A.R. Rahman",
  "A.R.RAHMAN": "A.R. Rahman",
  "ARIJIT SINGH": "Arijit Singh",
  "Vishal Shekhar": "Vishal-Shekhar",
  "AC_DC": "AC/DC"
}
```

Keys are variants (case-insensitive match), values are the canonical form.
This merges folders like `AR RAHMAN/` and `A.R. Rahman/` into one.

Place at: `config/language_hints/artist_map.json`

---

## Examples

### English.json (minimal)

```json
{
  "artists": [],
  "dna": [],
  "keywords": [],
  "lang_codes": ["en"]
}
```

English is usually classified correctly by NLP, so this file is mostly a
no-op. Add artists only if specific ones are being misclassified.

### Hindi.json (comprehensive)

```json
{
  "artists": [
    "Arijit Singh", "A.R. Rahman", "Shreya Ghoshal",
    "Atif Aslam", "Neha Kakkar", "Vishal-Shekhar",
    "Pritam", "Mika Singh", "Badshah", "Honey Singh",
    "Sonu Nigam", "Kumar Sanu", "Udit Narayan",
    "Alka Yagnik", "Lata Mangeshkar", "Kishore Kumar"
  ],
  "dna": ["bollywood", "bhangra", "desi", "filmi"],
  "keywords": [
    "ishq", "dil", "pyaar", "zindagi", "tere", "mujhe",
    "tum", "tera", "mohabbat", "sanam"
  ],
  "lang_codes": ["hi", "pa"]
}
```

### Japanese.json

```json
{
  "artists": [
    "Kenshi Yonezu", "YOASOBI", "Ado", "LiSA",
    "Official HIGE DANdism", "Mrs. GREEN APPLE",
    "Aimer", "King Gnu", "Vaundy"
  ],
  "dna": ["j-pop", "jpop", "anime", "vocaloid"],
  "keywords": ["koi", "yume", "hikari", "kokoro", "sekai"],
  "lang_codes": ["ja"]
}
```

### Spanish.json

```json
{
  "artists": [
    "Bad Bunny", "J Balvin", "Shakira", "Rosalia",
    "Ozuna", "Daddy Yankee", "Maluma", "Karol G"
  ],
  "dna": ["reggaeton", "latin", "bachata", "salsa"],
  "keywords": ["corazon", "amor", "vida", "fuego", "noche"],
  "lang_codes": ["es", "ca", "gl"]
}
```

---

## Tips

1. **Start small.** Add only the artists you know are misclassified. You can
   always add more after running the pipeline and checking the results.

2. **Check after sorting.** Run the pipeline, then inspect `Sorted/` to see
   which artists ended up in the wrong language folder. Add those to your
   hint file and re-run the classification scripts.

3. **One language per file.** Don't put Hindi and English artists in the same
   file — create separate files for each language.

4. **Case doesn't matter for matching** but the filename determines the folder
   name. `Hindi.json` creates `Sorted/Hindi/`, not `Sorted/hindi/`.

5. **`lang_codes` can overlap.** If you put `"pa"` (Punjabi) in both
   `Hindi.json` and `Punjabi.json`, the first file loaded wins. To avoid
   ambiguity, put each code in only one file.
