# TeamApp Admin JSON API Map

## News

### List
- `GET /clubs/{club_id}/articles.json?_detail=v1`
- Provides item URLs for detail and edit, plus archive actions.

### Create
- Schema: `GET /clubs/{club_id}/articles/new.json?_detail=v1`
- Submit: `POST /clubs/{club_id}/articles.json?_post_response=v1`
- Observed multipart fields:
  - `article[subject]`
  - `article[body]`
  - `article[visibility]`
  - `article[comments_enabled]`
  - `article[feature]`
  - `article[html_body]`
  - `article[release_pending]`
  - `send_notifications`
  - optional `article[location_data][name|latitude|longitude]`

### Update
- Schema: `GET /clubs/{club_id}/articles/{article_id}/edit.json?_detail=v1`
- `onSubmit` indicates update endpoint, typically article `.json` with patch/put response mode.

## Events (Schedules)

### Schedule index
- `GET /clubs/{club_id}/fixtures.json?_list=v1`
- Points to events list per team (`team_id=all` or specific team).

### Events list
- `GET /clubs/{club_id}/events.json?_list=v1&team_id={team_id|all}`
- Includes per-event edit/archive URLs and top-level create URL.

### Create
- Schema: `GET /clubs/{club_id}/events/new.json?_detail=v1&team_id={team_id|all}`
- Submit: `POST /clubs/{club_id}/events.json?_post_response=v1`
- Includes two-step `multiEmbeddedForm` (details + more options) before submit.

### Update
- Schema: `GET /clubs/{club_id}/events/{event_id}/edit.json?_detail=v1&team_id={team_id|all}`
- Observed submit:
  - `PATCH /clubs/{club_id}/events/{event_id}/update_details.json?_patch_response=v1&team_id={team_id}`

## Access Groups

### List
- `GET /clubs/{club_id}/access_levels.json?_list=v1`
- Includes reorder patch, archive delete, hard delete URLs.

### Create
- Schema: `GET /clubs/{club_id}/access_levels/new.json?_detail=v1`
- Submit: `POST /clubs/{club_id}/access_levels.json?_post_response=v1`

### Update
- Schema: `GET /clubs/{club_id}/access_levels/{access_level_id}/edit.json?_detail=v1`
- Submit: `PUT /clubs/{club_id}/access_levels/{access_level_id}.json?_put_response=v1`

## Teams

### List
- `GET /clubs/{club_id}/teams.json?_list=v1`
- Includes create team URL, manage roles URL, team detail URLs, delete URLs.

### Create
- Schema: `GET /clubs/{club_id}/teams/new.json?_detail=v1`
- Submit: `POST /clubs/{club_id}/teams.json?_post_response=v1`

### Update
- Schema: `GET /clubs/{club_id}/teams/{team_id}/edit.json?_detail=v1`
- Submit: `PUT /clubs/{club_id}/teams/{team_id}.json?_patch_response=v1`

## Notes

- Most write operations are controller-driven and include response-mode query params like `_post_response=v1`, `_patch_response=v1`, `_put_response=v1`.
- Use `.../new.json` and `.../edit.json` responses as source of truth for field names and validation logic before constructing payloads.
