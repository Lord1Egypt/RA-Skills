# Daily Auto-Publish Automation Template

This file contains ready-to-use automation prompts for setting up daily publishing.

## Architecture

Two automations work together:

1. **Draft Generation** (e.g., 15:00 daily) — generates article content and pushes to draft box
2. **Draft Publishing** (e.g., 20:00 daily) — publishes the day's draft via `freepublish/submit`

The draft generation automation is content-specific (you write the prompt for your content style).
The draft publishing automation is generic — use the template below.

---

## Publishing Automation Prompt

Copy this as the `prompt` field when creating an automation via `automation_update`:

```
You are a WeChat Official Account publishing assistant. Your job is to publish today's draft at the scheduled time.

## Execution Steps

### Step 1: Get today's date
Run `date +%Y-%m-%d` to get today's date.

### Step 2: Check today's draft
Read the draft status file at {DRAFT_STATUS_PATH}/YYYY-MM-DD.json
- If the file does not exist: notify the user "No draft found for today, skipping publish" and stop.
- If the file exists: read the `media_id` field.

### Step 3: Load credentials
Read the .env file at {ENV_FILE_PATH} for WECHAT_APPID and WECHAT_SECRET.

### Step 4: Publish the draft
1. Get access_token:
   curl -s "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=APPID&secret=SECRET"
2. If errcode=40164 (IP whitelist): get server IP with `curl -s https://api.ipify.org` and notify the user to add it to the whitelist.
3. Call publish API:
   curl -X POST "https://api.weixin.qq.com/cgi-bin/freepublish/submit?access_token=TOKEN" \
     -H "Content-Type: application/json" \
     -d '{"media_id":"MEDIA_ID"}'
4. Check result:
   - errcode=0: Success — notify the user with the article title and publish_id.
   - errcode=48001: API permission not active — notify the user to publish manually from mp.weixin.qq.com draft box.
   - errcode=40007: media_id invalid — notify the user the draft may have been published or deleted.
   - errcode=-1: System error — retry 2-3 times with fresh token; if persistent, notify user to publish manually.
   - Other errors: notify the user of the failure reason.

### Step 5: Notify the user
- On success: "Today's article has been auto-published. Title: XXX"
- On 48001: "API permission syncing. Please open mp.weixin.qq.com → Draft Box → click Publish manually. Title: XXX"
- On other failure: report the error and suggest manual publishing.

## Notes
- Publishing is irreversible. Always verify the media_id is correct.
- If the user said "skip today" or "don't publish today" before the scheduled time, skip this run.
- Update the draft status file with the publish result.
```

---

## How to Create the Automation

Use the `automation_update` tool with these parameters:

```
mode: "create"
name: "Daily WeChat Publish (20:00)"
scheduleType: "recurring"
rrule: "FREQ=DAILY;BYHOUR=20;BYMINUTE=0"
cwds: "/path/to/your/workspace"
prompt: <the template above, with placeholders filled in>
```

### Placeholders to replace

| Placeholder | Description | Example |
|-------------|-------------|---------|
| `{DRAFT_STATUS_PATH}` | Directory where daily draft JSON files are stored | `/Users/friend/articles/drafts` |
| `{ENV_FILE_PATH}` | Path to the .env credential file | `/Users/friend/.wechat-mp.env` |

---

## Draft Status JSON Format

The publishing automation expects a JSON file at `{DRAFT_STATUS_PATH}/YYYY-MM-DD.json`:

```json
{
  "date": "2026-07-18",
  "title": "Article Title",
  "digest": "Article summary",
  "media_id": "DRAFT_MEDIA_ID_FROM_PUSH",
  "status": "draft_pushed",
  "push_time": "2026-07-18T15:00:00+08:00"
}
```

After publishing, update the `status` field:
- `"published"` — on success
- `"publish_failed"` — on failure (include error details in a `publish_attempts` array)

---

## Alternative: Use the Publish Script Directly

Instead of the automation prompt calling curl inline, the automation can call the script:

```
Run this command to publish today's draft:
python3 {SKILL_PATH}/scripts/publish_draft.py --env {ENV_FILE_PATH} --media-id MEDIA_ID
```

This approach is simpler but less flexible for error-specific notifications.
