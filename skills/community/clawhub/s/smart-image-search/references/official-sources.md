# Official-source strengthening

When intent is `official`, do not treat generic news or gallery images as ideal unless better sources are absent.

## Prefer strongly
- official domains
- verified institution pages
- educational domains
- encyclopedia or reference pages when official pages are unavailable
- pages whose title or URL suggest logo, mascot, official poster, school identity, or institutional assets

## Penalize
- generic news articles
- entertainment news pages
- image aggregators and wallpaper galleries
- repost tool sites
- meme or emoji sites
- unrelated video thumbnails

## Practical rule
For `official` intent:
- boost: `official`, `edu`, `gov`, `baike`, `university`, `college`, `academy`, `mascot`, `logo`, `emblem`, `brand mark`
- penalize: `news`, `entertainment`, `wallpaper`, `video`, `gallery`, `meme`
- if no strong official-like result exists, fall back gracefully to the cleanest reference-style candidate rather than a random news photo
