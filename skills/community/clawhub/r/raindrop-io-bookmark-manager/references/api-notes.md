# API notes

## Base URL

- `https://api.raindrop.io/rest/v1`

## Auth

- Send `Authorization: Bearer <token>`
- Send JSON payloads with `Content-Type: application/json`
- For local desktop use, a Raindrop **test token** is enough for working with the owner account

## OAuth endpoints

- `GET https://raindrop.io/oauth/authorize`
- `POST https://raindrop.io/oauth/access_token`

Authorization request params:
- `client_id`
- `redirect_uri`
- `response_type=code`

Token exchange / refresh response fields commonly include:
- `access_token`
- `refresh_token`
- `expires_in`
- `expires` (deprecated)
- `token_type`

Typical local callback:
- `http://127.0.0.1:8765/callback`

## Core endpoints used by this skill

### User
- `GET /user` — authenticated user profile

### Collections
- `GET /collections` — root collections
- `GET /collections/childrens` — nested collections
- `GET /collection/{id}` — one collection
- `POST /collection` — create collection
- `PUT /collection/{id}` — update collection
- `DELETE /collection/{id}` — delete collection

Common collection fields:
- `title`
- `view` = `list|simple|grid|masonry`
- `sort`
- `public`
- `parent.$id`
- `cover`
- `expanded`

System collection ids:
- `-1` = Unsorted
- `-99` = Trash

### Raindrops / bookmarks
- `GET /raindrops/{collectionId}` — list/search bookmarks in a collection
- `GET /raindrop/{id}` — fetch one bookmark
- `POST /raindrop` — create one bookmark
- `PUT /raindrop/{id}` — update one bookmark
- `DELETE /raindrop/{id}` — delete one bookmark

Common bookmark fields:
- `link`
- `title`
- `excerpt`
- `note`
- `tags`
- `cover`
- `collection.$id`
- `important`
- `pleaseParse`

Common list query params:
- `page`
- `perpage`
- `sort`
- `search`
