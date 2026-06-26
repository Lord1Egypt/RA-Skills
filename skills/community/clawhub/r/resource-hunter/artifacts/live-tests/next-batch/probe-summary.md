# Next Batch Probe Summary

## Added to runtime so far
- AnimeTosho
- DMHY
- Torlock
- DaliPan
- search-index:bing
- search-index:brave

## This wave findings

### Newly integrated this wave
- DaliPan
  - dug from Dalipan frontend bundle
  - confirmed public search API shape at `https://api.dalipan.com/api/v1/pan/search`
  - requires unverified SSL context in current environment because upstream certificate is expired
  - detail endpoint is still login-gated / incomplete for anonymous use, so runtime integration currently uses public search payload as actionable clue/direct placeholder records (`dalipan://provider/eu-token`), preserving dalipan ids/tokens in raw metadata for future follow-up

### Probed and not integrated this wave
- ZNDS: reachable, but current search entry keeps returning generic site/distribution pages instead of useful resource/forum clues.
- quark.so: homepage timed out in current environment.
- EXT.to: 403 Forbidden.
- Zooqle: returns error JSON (`{"status":"error","message":"Hatalı Deneme"}`).
- SolidTorrents: SSL EOF.
- TorrentGalaxy: SSL EOF.
- LimeTorrents: JS redirect works, redirected request currently returns 502.
- Lanzou family domains: homepages reachable, but no direct public HTML search endpoint found this wave.
- iLanzou: reachable, but JS SPA shell only.
- PanSearch: page and `_next/data` endpoint reachable. Real results appear when using `keyword=` instead of `q=`, but current runtime output is rendered content cards without stable canonical share fields, so not integrated yet.
- Dalipan detail endpoint (`/api/v1/pan/detail`) appears login-gated for anonymous access.
- Dalipan url endpoint (`/api/v1/pan/url`) currently returns `-1` for anonymous probes.

## Rule followed
- tested one by one
- only integrate sources that work end-to-end enough for current environment
- do not add login/API-key sources
