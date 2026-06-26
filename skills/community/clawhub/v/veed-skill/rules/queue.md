---
name: queue
description: Async queue submission, status polling, and result retrieval for fal.ai video generation
metadata:
  tags: queue, async, polling, status, request
---

# Queue and Polling

Video generation is asynchronous. When you POST to the queue endpoint, you get back a request ID and must poll for completion.

## Submission response

After submitting to any `https://queue.fal.run/veed/fabric-1.0*` endpoint, the response looks like:

```json
{
  "request_id": "abc123-def456",
  "response_url": "https://queue.fal.run/veed/fabric-1.0/requests/abc123-def456",
  "status_url": "https://queue.fal.run/veed/fabric-1.0/requests/abc123-def456/status",
  "cancel_url": "https://queue.fal.run/veed/fabric-1.0/requests/abc123-def456/cancel",
  "queue_position": 0
}
```

Extract the key values:
```bash
REQUEST_ID=$(echo "$RESPONSE" | jq -r '.request_id')
STATUS_URL=$(echo "$RESPONSE" | jq -r '.status_url')
RESPONSE_URL=$(echo "$RESPONSE" | jq -r '.response_url')
```

## Polling for status

Poll the status URL every 5 seconds with `?logs=1` for detailed output:

```bash
STATUS_RESPONSE=$(curl -s -H "Authorization: Key $FAL_KEY" "$STATUS_URL?logs=1")
CURRENT_STATUS=$(echo "$STATUS_RESPONSE" | jq -r '.status')
```

### Status values

| Status | Meaning | User message |
|---|---|---|
| `IN_QUEUE` | Waiting for a runner | "In queue, position {queue_position}..." |
| `IN_PROGRESS` | Actively generating | "Generating your video..." |
| `COMPLETED` | Done, result ready | Proceed to retrieval |

**MUST** report status to the user at each poll so they know the generation is progressing.

### Polling loop

```bash
while true; do
  STATUS_RESPONSE=$(curl -s -H "Authorization: Key $FAL_KEY" "$STATUS_URL?logs=1")
  CURRENT_STATUS=$(echo "$STATUS_RESPONSE" | jq -r '.status')

  if [ "$CURRENT_STATUS" = "COMPLETED" ]; then
    echo "Video generation complete!"
    break
  elif [ "$CURRENT_STATUS" = "IN_QUEUE" ]; then
    POSITION=$(echo "$STATUS_RESPONSE" | jq -r '.queue_position')
    echo "In queue, position: $POSITION"
  elif [ "$CURRENT_STATUS" = "IN_PROGRESS" ]; then
    echo "Generating video..."
  fi

  sleep 5
done
```

**MUST NOT** run this as a single bash command. Instead, poll manually — run the status check, report to the user, wait 5 seconds, repeat. This keeps the user informed.

## Retrieving the result

Once status is `COMPLETED`, fetch the full result:

```bash
RESULT=$(curl -s -H "Authorization: Key $FAL_KEY" "$RESPONSE_URL")
```

The result contains:
```json
{
  "video": {
    "url": "https://v3.fal.media/files/.../generated_video.mp4",
    "content_type": "video/mp4",
    "file_name": "generated_video.mp4",
    "file_size": 1198529
  }
}
```

Extract the video URL:
```bash
VIDEO_URL=$(echo "$RESULT" | jq -r '.video.url')
```

Proceed to [./output.md](./output.md) to download and save the video.

## Timeout

If the generation has not completed after **5 minutes** of polling, stop and tell the user:

> Generation is taking longer than expected. Your request ID is: {request_id}
> You can check the status manually or try again later.

**MUST NOT** poll indefinitely.

## Cancellation

If the user wants to cancel a running generation:

```bash
curl -s -X PUT "$CANCEL_URL" -H "Authorization: Key $FAL_KEY"
```

Returns 202 if cancelled, 400 if already completed.
