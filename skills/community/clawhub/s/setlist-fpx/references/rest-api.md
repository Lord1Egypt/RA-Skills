# setlist.fm REST API — read endpoints for curl

Base URL: `https://api.setlist.fm/rest` · every call: `-H "x-api-key: $SETLIST_API_KEY" -H 'Accept: application/json'`.
Optional: `-H "Accept-Language: en"` (one of `en es fr de pt tr it pl`) to localize city/country names.

All 15 read endpoints below are exactly what `setlist-mcp`'s tools call — same paths, same params.

---

## Artists

### 1. Search artists

```sh
curl -s 'https://api.setlist.fm/rest/1.0/search/artists' \
  -H "x-api-key: $SETLIST_API_KEY" -H 'Accept: application/json' \
  --get --data-urlencode 'artistName=Radiohead' --data-urlencode 'sort=relevance' \
  | jq '.artist[] | {name, mbid, url}'
```
Params: `artistName`, `artistMbid`, `sort` (`sortName` default | `relevance`), `p` (page, default 1).

### 2. Get artist by mbid

```sh
curl -s "https://api.setlist.fm/rest/1.0/artist/$MBID" \
  -H "x-api-key: $SETLIST_API_KEY" -H 'Accept: application/json' | jq
```

### 3. Artist's setlists (most recent first)

```sh
curl -s "https://api.setlist.fm/rest/1.0/artist/$MBID/setlists?p=1" \
  -H "x-api-key: $SETLIST_API_KEY" -H 'Accept: application/json' \
  | jq '.setlist[] | {id, eventDate, venue: .venue.name, city: .venue.city.name, songCount, hasSongs}'
```
`songCount`/`setCount`/`hasSongs` are annotations the MCP adds by walking the
response locally (not native API fields) — derive them yourself if you need
them: `songCount = ([.sets.set[].song[]?] | length)`.

---

## Setlists

### 4. Search setlists

Provide at least one filter. `date` is `dd-MM-yyyy` (NOT ISO); `lastUpdated`
is `yyyyMMddHHmmss` UTC.

```sh
curl -s 'https://api.setlist.fm/rest/1.0/search/setlists' \
  -H "x-api-key: $SETLIST_API_KEY" -H 'Accept: application/json' \
  --get \
  --data-urlencode 'artistName=Radiohead' \
  --data-urlencode 'date=28-08-2025' \
  --data-urlencode 'cityName=Charlotte' \
  | jq '.setlist[] | {id, url, venue: .venue.name, eventDate}'
```
Other params: `artistMbid`, `venueName`, `venueId`, `cityId`, `state`,
`stateCode`, `countryCode`, `tourName`, `year`, `p`. Omit the artist and pass
`venueName`/`venueId` + `date` to list every performer at a venue that day.

### 5. Get setlist by id

```sh
curl -s "https://api.setlist.fm/rest/1.0/setlist/$SETLIST_ID" \
  -H "x-api-key: $SETLIST_API_KEY" -H 'Accept: application/json' | jq
```
Songs live in `.sets.set[].song[]`; a `set` may have `encore` (1 = first
encore) and `name` (e.g. an acoustic set). A `song` may carry `tape: true`
(pre-recorded, not performed), `cover` (original artist), `with` (guest), and
`info` (a note like "acoustic").

### 6. Get a specific historical version

```sh
curl -s "https://api.setlist.fm/rest/1.0/setlist/version/$VERSION_ID" \
  -H "x-api-key: $SETLIST_API_KEY" -H 'Accept: application/json' | jq
```

---

## Venues

### 7. Search venues

```sh
curl -s 'https://api.setlist.fm/rest/1.0/search/venues' \
  -H "x-api-key: $SETLIST_API_KEY" -H 'Accept: application/json' \
  --get --data-urlencode 'name=The Fillmore' --data-urlencode 'cityName=Charlotte' \
  | jq '.venue[] | {id, name, city: .city.name, url}'
```
Params: `name`, `cityName`, `cityId`, `state`, `stateCode`, `country`, `p`.

### 8. Get venue by id

```sh
curl -s "https://api.setlist.fm/rest/1.0/venue/$VENUE_ID" \
  -H "x-api-key: $SETLIST_API_KEY" -H 'Accept: application/json' | jq
```

### 9. Venue's setlists

```sh
curl -s "https://api.setlist.fm/rest/1.0/venue/$VENUE_ID/setlists?p=1" \
  -H "x-api-key: $SETLIST_API_KEY" -H 'Accept: application/json' \
  | jq '.setlist[] | {id, artist: .artist.name, eventDate}'
```

---

## Geo

### 10. Search cities

```sh
curl -s 'https://api.setlist.fm/rest/1.0/search/cities' \
  -H "x-api-key: $SETLIST_API_KEY" -H 'Accept: application/json' \
  --get --data-urlencode 'name=Charlotte' \
  | jq '.cities[] | {geoId: .id, name, state, country: .country.name}'
```
Params: `name`, `country`, `state`, `stateCode`, `p`. Feed `geoId` into
`cityId` on search/setlists and search/venues.

### 11. Get city by geoId

```sh
curl -s "https://api.setlist.fm/rest/1.0/city/$GEO_ID" \
  -H "x-api-key: $SETLIST_API_KEY" -H 'Accept: application/json' | jq
```

### 12. List countries

```sh
curl -s 'https://api.setlist.fm/rest/1.0/search/countries' \
  -H "x-api-key: $SETLIST_API_KEY" -H 'Accept: application/json' \
  | jq '.country[] | {code, name}'
```
Use `code` as `countryCode` in search/setlists.

---

## Users

### 13. Get user profile

```sh
curl -s "https://api.setlist.fm/rest/1.0/user/$USER_ID" \
  -H "x-api-key: $SETLIST_API_KEY" -H 'Accept: application/json' | jq
```

### 14. User's attended shows

```sh
curl -s "https://api.setlist.fm/rest/1.0/user/$USER_ID/attended?p=1" \
  -H "x-api-key: $SETLIST_API_KEY" -H 'Accept: application/json' \
  | jq '.setlist[] | {id, artist: .artist.name, eventDate}'
```

### 15. User's created/edited setlists

```sh
curl -s "https://api.setlist.fm/rest/1.0/user/$USER_ID/edited?p=1" \
  -H "x-api-key: $SETLIST_API_KEY" -H 'Accept: application/json' | jq
```

---

## Errors

- `400` — missing/invalid params (e.g. no filter on search/setlists).
- `401` — no `x-api-key` header sent at all.
- `403` — a key WAS sent but is invalid/revoked (not the same as 401 — don't
  conflate "no key" with "bad key").
- `404` — id not found.
- `429` — over the standard-tier ~2 req/sec / 1440/day limit; back off ~2s
  and retry once.
