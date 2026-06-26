# Official whitelist and directed search

When intent is `official`, add domain-aware preferences and directed search queries.

## Preferred domain classes

Strong prefer:
- official brand or organization domains
- educational domains
- government or institution domains
- verified reference pages when official pages are missing
- official social or profile pages when clearly branded

## Soft whitelist tokens
Use these tokens to boost candidates:
- `official`
- `logo`
- `emblem`
- `crest`
- `mascot`
- `brand`
- `institution`
- `university`
- `college`
- `academy`
- `edu`
- `gov`
- `baike`

## Blacklist / strong penalties
Apply strong penalties to these in official mode:
- generic entertainment news pages
- generic image aggregation pages
- meme or emoji sites
- wallpaper galleries
- unrelated video pages

## Directed search strategy
For `official` intent, try additional query variants built from the cleaned core query:
- `<core> official`
- `<core> logo`
- `<core> emblem`
- `<core> mascot`
- `<core> site:edu`
- `<core> site:gov`

Subtype-aware additions:
- `emblem`: `<core> crest` / `<core> brand mark` / `<core> visual identity`
- `mascot`: `<core> official character` / `<core> brand character` / `<core> IP character`
- `campus`: `<core> campus` / `<core> gate`

Merge candidates from these directed queries into the same ranking pool.
