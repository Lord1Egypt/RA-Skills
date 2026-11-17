# SnapDub REST API, the parts this skill uses

Base URL `https://snapdub.ai/api/v1`, every request with `Authorization: Bearer $SNAPDUB_API_KEY`.
Full reference and OpenAPI file: https://snapdub.ai/developers/api and https://snapdub.ai/api/v1/openapi.json.

```bash
# who am I, credits left
curl -s https://snapdub.ai/api/v1/me -H "Authorization: Bearer $SNAPDUB_API_KEY"

# what a job would cost
curl -s -X POST https://snapdub.ai/api/v1/estimate -H "Authorization: Bearer $SNAPDUB_API_KEY" \
  -H "Content-Type: application/json" -d '{"url":"https://www.youtube.com/watch?v=VIDEO","clips":5}'

# start a job
curl -s -X POST https://snapdub.ai/api/v1/videos -H "Authorization: Bearer $SNAPDUB_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"url":"https://www.youtube.com/watch?v=VIDEO","clips":5,"clip_length_seconds":45,"captions":true}'

# progress (check about once a minute)
curl -s https://snapdub.ai/api/v1/videos/VIDEO_ID -H "Authorization: Bearer $SNAPDUB_API_KEY"

# finished clips, best first
curl -s https://snapdub.ai/api/v1/videos/VIDEO_ID/clips -H "Authorization: Bearer $SNAPDUB_API_KEY"

# live paid clipping campaigns
curl -s https://snapdub.ai/api/v1/campaigns -H "Authorization: Bearer $SNAPDUB_API_KEY"

# connected social accounts, then schedule one clip (only with the person's go-ahead)
curl -s https://snapdub.ai/api/v1/social_accounts -H "Authorization: Bearer $SNAPDUB_API_KEY"
curl -s -X POST https://snapdub.ai/api/v1/posts -H "Authorization: Bearer $SNAPDUB_API_KEY" \
  -H "Content-Type: application/json" -d '{"clip_id":"CLIP_ID","platforms":["tiktok","youtube"],"post_at":"2026-11-06T18:00"}'
# post_at without a UTC offset is read in the account's own time zone; leave it out to post now
```

Errors come back as JSON with an `error` field and a 4xx status; pass the message on to the person as is.
Rate limit: 120 requests a minute per key.
