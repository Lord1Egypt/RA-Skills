---
name: zlibrary
description: "Search and download books from Z-Library. Caches login session to ~/.zlibrary-session.json. Downloads book files (EPUB/PDF) to ~/Downloads/."
version: 2.1.0
metadata:
  openclaw:
    emoji: 📚
    requires:
      env:
        - ZLIBRARY_EMAIL
        - ZLIBRARY_PASSWORD
      bins:
        - curl
      config:
        - ~/.zlibrary-session.json
---

# Z-Library

Search and download books from Z-Library using their eAPI.

## Authentication

Credentials come from environment variables `ZLIBRARY_EMAIL` and `ZLIBRARY_PASSWORD`.

Session tokens are cached at `~/.zlibrary-session.json` so login only happens once.

### Login

Before any operation, check for a cached session:

```bash
cat ~/.zlibrary-session.json 2>/dev/null
```

If the file does not exist or is empty, log in:

```bash
curl -s -X POST "https://z-lib.sk/eapi/user/login" \
  -H "User-Agent: Mozilla/5.0 (Android 12; Mobile)" \
  -d "email=$ZLIBRARY_EMAIL&password=$ZLIBRARY_PASSWORD"
```

The response contains `user.id` and `user.remix_userkey`. Save them:

```bash
echo '{"remix_userid":"<id>","remix_userkey":"<key>"}' > ~/.zlibrary-session.json
```

All subsequent requests must include these as cookies:

```
-b "remix_userid=<id>; remix_userkey=<key>"
```

## Search

```bash
curl -s -X POST "https://z-lib.sk/eapi/book/search" \
  -H "User-Agent: Mozilla/5.0 (Android 12; Mobile)" \
  -b "remix_userid=<id>; remix_userkey=<key>" \
  -d "message=<query>&limit=10"
```

Optional search parameters (append to `-d`):
- `yearFrom=YYYY` — filter by start year
- `yearTo=YYYY` — filter by end year
- `languages[]=english` — filter by language (repeatable)
- `extensions[]=epub` — filter by format (repeatable)
- `order=popular` — sort order

Response: `{ "success": 1, "books": [...] }`. Each book has `id`, `hash`, `title`, `author`, `extension`, `filesizeString`, and `dl` fields.

Present results as a numbered list showing title, author, format, and size. Ask the user which book they want before downloading.

## Get Available Formats

To see all available formats for a book:

```bash
curl -s "https://z-lib.sk/eapi/book/<id>/<hash>/formats" \
  -H "User-Agent: Mozilla/5.0 (Android 12; Mobile)" \
  -b "remix_userid=<id>; remix_userkey=<key>"
```

Response: `{ "success": 1, "books": [...] }` where each entry has `id`, `hash`, `extension`, `filesize`, and `filesizeString`.

## Download

Two-step process:

### Step 1 — Get the download link

```bash
curl -s "https://z-lib.sk/eapi/book/<id>/<hash>/file" \
  -H "User-Agent: Mozilla/5.0 (Android 12; Mobile)" \
  -b "remix_userid=<id>; remix_userkey=<key>"
```

Response: `{ "success": 1, "file": { "downloadLink": "<url>", "extension": "epub", ... } }`

### Step 2 — Download the file

```bash
curl -s -L -o ~/Downloads/<filename>.<ext> \
  -H "User-Agent: Mozilla/5.0 (Android 12; Mobile)" \
  "<downloadLink>"
```

Always download to `~/Downloads/` unless the user specifies otherwise. Use a clean filename based on the book title.

## User Profile

Check download limits and account info:

```bash
curl -s "https://z-lib.sk/eapi/user/profile" \
  -H "User-Agent: Mozilla/5.0 (Android 12; Mobile)" \
  -b "remix_userid=<id>; remix_userkey=<key>"
```

Shows `downloads_today`, `downloads_limit`, and account details.

## Error Handling

- If any request returns `{"success":0,"error":"Please login"}`, delete `~/.zlibrary-session.json` and re-authenticate.
- If login returns a validation error, tell the user their credentials are wrong and ask them to check `ZLIBRARY_EMAIL` and `ZLIBRARY_PASSWORD`.
- The free tier allows 10 downloads per day. If the user hits the limit, inform them.

## Notes

- The base domain `z-lib.sk` may change. If requests start failing, check for an updated domain.
- Always include the `User-Agent: Mozilla/5.0 (Android 12; Mobile)` header on every request.
- When downloading, prefer EPUB over PDF when both are available, unless the user asks for a specific format.
