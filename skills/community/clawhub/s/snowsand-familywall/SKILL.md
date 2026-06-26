---
name: familywall
version: 1.3.0
description: >-
  Interact with the FamilyWall family organization platform. Manage calendar events,
  shopping lists, tasks, family messaging, member locations, meal plans, recipes,
  the family wall/feed, and media file downloading.
  Use when: (1) checking family calendar or creating events, (2) managing shopping lists
  or to-do items, (3) sending/reading family messages, (4) checking family member locations,
  (5) viewing the family wall/feed, (6) meal planning or recipe management,
  (7) downloading photos, audio, or other media from messages.
  Triggers: "family calendar", "family events", "shopping list", "grocery list",
  "family message", "family chat", "family location", "where is", "family wall",
  "family feed", "add to list", "family members", "familywall", "meal plan",
  "recipe", "what's for dinner", "weekly meals", "download photo",
  "download media", "family photos", "message attachment".
---

# FamilyWall Integration

FamilyWall family organization platform integration for managing calendars, lists, messaging, meal plans, recipes, and more.

## Authentication

FamilyWall uses email/password authentication with session tokens. Required environment variables:

- `FAMILYWALL_EMAIL` - FamilyWall account email
- `FAMILYWALL_PASSWORD` - FamilyWall account password

These should be set in `~/.openclaw/.env`.

Test connection:
```bash
source ~/.openclaw/.env && {baseDir}/scripts/familywall.py status
```

## Quick Reference

All operations use the `{baseDir}/scripts/familywall.py` script:

| Operation | Command |
|-----------|---------|
| **Status & Members** | |
| Account/family status | `{baseDir}/scripts/familywall.py status` |
| List family members | `{baseDir}/scripts/familywall.py members` |
| **Calendar Events** | |
| List upcoming events | `{baseDir}/scripts/familywall.py events list --days 7` |
| Create event | `{baseDir}/scripts/familywall.py events create "Title" --start "2026-03-10T14:00:00" --end "2026-03-10T15:00:00"` |
| Create all-day event | `{baseDir}/scripts/familywall.py events create "Holiday" --start "2026-03-10" --end "2026-03-11" --allday` |
| Delete event | `{baseDir}/scripts/familywall.py events delete EVENT_ID` |
| **Shopping Lists / Tasks** | |
| List all lists | `{baseDir}/scripts/familywall.py lists list` |
| View list items | `{baseDir}/scripts/familywall.py lists items LIST_ID` |
| Add item to list | `{baseDir}/scripts/familywall.py lists add LIST_ID "Milk"` |
| Add with quantity | `{baseDir}/scripts/familywall.py lists add LIST_ID "Eggs" --quantity "12"` |
| Check item (purchased) | `{baseDir}/scripts/familywall.py lists check ITEM_ID` |
| Uncheck item | `{baseDir}/scripts/familywall.py lists check ITEM_ID --uncheck` |
| Create new list | `{baseDir}/scripts/familywall.py lists create "Groceries" --type SHOPPING` |
| Create todo list | `{baseDir}/scripts/familywall.py lists create "Chores" --type TODO` |
| **Messaging** | |
| List threads | `{baseDir}/scripts/familywall.py messages threads` |
| Read messages | `{baseDir}/scripts/familywall.py messages read THREAD_ID --limit 20` |
| Send message | `{baseDir}/scripts/familywall.py messages send THREAD_ID "Hello family!"` |
| **Media** | |
| List media in thread | `{baseDir}/scripts/familywall.py media list THREAD_ID` |
| Download by URL | `{baseDir}/scripts/familywall.py media download --url "PICTURE_URL" -o file.jpg` |
| Download by media ID | `{baseDir}/scripts/familywall.py media download --media-id MEDIA_ID --thread-id THREAD_ID` |
| Download all from thread | `{baseDir}/scripts/familywall.py media download-all THREAD_ID --output-dir ./media` |
| **Meal Planner** | |
| View meal plan | `{baseDir}/scripts/familywall.py meals list --days 7` |
| Add meal to plan | `{baseDir}/scripts/familywall.py meals add "Tacos" --date 2026-05-15 --type DINNER` |
| **Recipes** | |
| Create recipe | `{baseDir}/scripts/familywall.py recipes create "Pasta" --ingredients "noodles\nsauce" --instructions "1. Boil\n2. Mix"` |
| Import recipe from URL | `{baseDir}/scripts/familywall.py recipes from-url "https://example.com/recipe"` |
| List recipe categories | `{baseDir}/scripts/familywall.py recipes categories` |
| **Location** | |
| Get member locations | `{baseDir}/scripts/familywall.py locations` |
| **Wall / Feed** | |
| Get family wall | `{baseDir}/scripts/familywall.py wall --limit 20` |

## Common Workflows

### Check upcoming family events

```bash
source ~/.openclaw/.env
{baseDir}/scripts/familywall.py events list --days 7
```

### Add items to shopping list

```bash
source ~/.openclaw/.env
# First get the list ID
{baseDir}/scripts/familywall.py lists list
# Then add items
{baseDir}/scripts/familywall.py lists add "tasklist/12345_67890" "Milk"
{baseDir}/scripts/familywall.py lists add "tasklist/12345_67890" "Bread"
{baseDir}/scripts/familywall.py lists add "tasklist/12345_67890" "Eggs" --quantity "12"
```

### Create a calendar event

```bash
source ~/.openclaw/.env
{baseDir}/scripts/familywall.py events create "Family Dinner" \
  --start "2026-05-15T18:00:00" \
  --end "2026-05-15T20:00:00" \
  --location "Home" \
  --description "Weekly family dinner"
```

### Send a family message

```bash
source ~/.openclaw/.env
# Get thread list first
{baseDir}/scripts/familywall.py messages threads
# Send message to a thread
{baseDir}/scripts/familywall.py messages send "imthread/12345_67890" "Dinner is ready!"
```

### Download media from messages

Messages can contain photos, audio, and other media files. The `medias` array in message responses includes `pictureUrl` for downloading.

```bash
source ~/.openclaw/.env
# List all media in a thread
{baseDir}/scripts/familywall.py media list "imThread/12345"

# Download a specific file by URL (from media list output)
{baseDir}/scripts/familywall.py media download --url "https://api.familywall.com/media/..." -o photo.jpg

# Download by media ID (looks up the URL automatically)
{baseDir}/scripts/familywall.py media download --media-id "media/12345_67890" --thread-id "imThread/12345"

# Download ALL media from a thread into a directory
{baseDir}/scripts/familywall.py media download-all "imThread/12345" --output-dir ./family_media

# Download media from a specific message only
{baseDir}/scripts/familywall.py media download-all "imThread/12345" --message-id "message/12345_67890" --output-dir ./media
```

### Plan meals for the week

```bash
source ~/.openclaw/.env
# View current meal plan
{baseDir}/scripts/familywall.py meals list --days 7
# Add meals
{baseDir}/scripts/familywall.py meals add "Spaghetti" --date 2026-05-13 --type DINNER
{baseDir}/scripts/familywall.py meals add "Pancakes" --date 2026-05-14 --type BREAKFAST
{baseDir}/scripts/familywall.py meals add "Grilled Chicken" --date 2026-05-14 --type DINNER
```

Meal types: `BREAKFAST`, `LUNCH`, `DINNER`, `SNACK`

### Create a recipe

```bash
source ~/.openclaw/.env
{baseDir}/scripts/familywall.py recipes create "Banana Smoothie" \
  --ingredients "2 bananas\n1 cup milk\n1 tbsp honey\nIce" \
  --instructions "1. Add all ingredients to blender\n2. Blend until smooth\n3. Serve immediately" \
  --prep-time 5 --serves 2 \
  --description "Quick healthy breakfast smoothie"
```

### Import a recipe from a website

```bash
source ~/.openclaw/.env
{baseDir}/scripts/familywall.py recipes from-url "https://www.example.com/recipe/chocolate-cake"
```

### Check family member locations

```bash
source ~/.openclaw/.env
{baseDir}/scripts/familywall.py locations
```

## API Details

The FamilyWall API is at `https://api.familywall.com/api`. Authentication is session-based:

1. Login via `log2in` endpoint with email/password
2. Receive JSESSIONID cookie and tokenCsrf
3. Include both on subsequent requests

### Key API Endpoints

| Category | Endpoint | Description |
|----------|----------|-------------|
| Auth | `log2in` | Login with email/password |
| Account | `accgetallfamily` | Get all family data |
| Family | `famlistfamily` | List user's families |
| Events | `evtlist` | List calendar events |
| Events | `evtcreate` | Create event |
| Events | `evtdelete` | Delete event |
| Lists | `tasklistlist` | List all task/shopping lists |
| Lists | `tasklistget` | Get list with items |
| Lists | `tasklistadd` | Add item to list |
| Lists | `tasklistcheck` | Check/uncheck item |
| Lists | `tasklistcreate` | Create new list |
| Messages | `imthreadlist` | List IM threads |
| Messages | `immessagelist2` | Get messages from thread (includes media) |
| Messages | `imsend` | Send message |
| Media | `/media/...` | Download media files (GET with session auth) |
| Location | `loclist` | Get member locations |
| Wall | `walllist` | Get wall/feed posts |
| Meals | `mplistinterval` | List planned meals in range |
| Meals | `mpcreate` | Add dish to meal plan |
| Meals | `mpmealput` | Create/edit a meal |
| Recipes | `mprecipeput` | Create/edit a recipe |
| Recipes | `mprecipeputbyurl` | Create recipe from URL |
| Recipes | `mpcategorylist` | List recipe categories |
| Recipes | `mpadditemtolist` | Add meal ingredients to shopping list |

### Request Format

All requests are POST with `application/x-www-form-urlencoded` body. Parameters use prefix notation:
- `a00` prefix for first call parameters
- `a01call`, `a02call`, etc. for batched calls
- `partnerScope=Family` required on all calls

### Response Format

Responses are JSON with structure:
```json
{
  "a00": {
    "r": {"r": <result_data>},  // Success
    "ex": {"ex": {"message": "..."}},  // Error
    "cn": "endpoint_name"
  }
}
```

### Media in Messages

Messages from `immessagelist2` include a `medias` array. Each media object contains:

| Field | Description |
|-------|-------------|
| `mediaId` | Unique media identifier (e.g. `media/12345_67890`) |
| `pictureUrl` | Direct download URL (requires session auth cookie) |
| `mimeType` | MIME type (`image/jpeg`, `audio/mp4`, etc.) |
| `name` | Original filename |
| `datasize` | File size in bytes |
| `resolutionX/Y` | Image dimensions (images only) |
| `durationMs` | Duration in milliseconds (audio/video only) |
| `readystate` | Processing state (`READY` = downloadable) |

To download media, send an authenticated GET request to the `pictureUrl` with the JSESSIONID cookie and tokencsrf header.

Wall/feed posts may also contain media attachments with the same structure.

## Error Handling

Common errors:
- **FizClassId 1**: Account not found
- **FizClassId 4**: Account identifier not validated
- **FizClassId 10**: API key not found
- **FizClassId 26**: Account blocked
- **FizClassId 502**: Call not registered / missing parameter
- **FizClassId 503**: Model does not exist
- **FizClassId 510**: No family context (need to select family first)

## Dependencies

- Python 3.10+ (uses stdlib `urllib` if `requests` not available)
- Optional: `requests` library for better HTTP handling

## Full API Reference

The complete FamilyWall API reference (all endpoints, parameters, return types, and exceptions) is maintained on Confluence:

**[FamilyWall — API Reference](https://snowsand.atlassian.net/wiki/spaces/SD/pages/38436865)**
