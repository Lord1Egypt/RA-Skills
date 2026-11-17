# Worked examples — ZARZOOM Skill conversations

These are illustrative transcripts showing what a user prompt looks
like, what API calls the Skill makes, and what natural-language
output the user receives. Replace placeholder UUIDs / URLs with the
real values from your test runs.

---

## Example 1 — Submit an article with one image

**User prompt:**
> Post an article titled "Morning coffee ritual" — first paragraph:
> "Every morning starts with a slow pour-over. The grind, the bloom,
> the patience." Add this picture I just took. Hit Facebook and LinkedIn.

**Skill action plan:**

1. Call `POST /api/v1/uploads/presign`
   ```json
   { "content_type": "image", "mime_type": "image/jpeg", "file_size_bytes": 1247829 }
   ```
   Returns `{ "data": { "upload_key": "uploads/abc-123/img-xyz.jpg", "upload_url": "https://...", "expires_at": "..." }, "meta": { ... } }`

2. PUT the image bytes to `data.upload_url` with `Content-Type: image/jpeg`.

3. Call `POST /api/v1/content/articles`
   ```json
   {
     "title": "Morning coffee ritual",
     "body": "<p>Every morning starts with a slow pour-over. The grind, the bloom, the patience.</p>",
     "image_keys": ["uploads/abc-123/img-xyz.jpg"],
     "selected_platforms": ["facebook", "linkedin"]
   }
   ```

4. Receives 202:
   ```json
   {
     "data": {
       "submission_id": "sub-456",
       "status": "pending",
       "per_platform_status": [
         { "platform": "facebook", "eligible": true },
         { "platform": "linkedin", "eligible": true }
       ]
     },
     "meta": { "api_version": "1.0", "request_id": "..." }
   }
   ```

**Skill output to user:**

> Submitted! "Morning coffee ritual" is now in compliance review (id
> `sub-456`).
>
> Will post to: **Facebook**, **LinkedIn**
>
> You can track approval at https://zarzoom.com/dashboard/my-submissions.

---

## Example 2 — Submit a short with platforms that don't all fit

**User prompt:**
> Write a short about how I just hit 1,000 subscribers — exuberant,
> 50 words or so. Post everywhere I'm connected.

**Skill action plan:**

1. Call `GET /api/v1/capabilities/platforms` to find connected platforms.
2. Compose the text (~50 words).
3. Call `POST /api/v1/content/shorts`
   ```json
   {
     "text": "Just hit 1,000 subscribers...[50 words]",
     "selected_platforms": ["facebook","linkedin","x","threads","bluesky","instagram"]
   }
   ```

4. Receives 202 with `per_platform_status` that flags Pinterest as
   ineligible (no image — Pinterest requires one).

**Skill output to user:**

> Submitted (id `sub-789`)!
>
> Will post to: Facebook, LinkedIn, X, Threads, Bluesky, Instagram
>
> Skipping **Pinterest** — it needs an image, and this one's text-only.

---

## Example 3 — Check status after admin approval

**User prompt:**
> What's the status of my morning coffee submission?

**Skill action plan:**

1. (If the user hasn't given an id) — call `GET /api/v1/submissions?limit=5`
   to find the most recent.
2. Call `GET /api/v1/submissions/sub-456`.

Returns:
```json
{
  "data": {
    "submission_id": "sub-456",
    "status": "approved",
    "reviewed_at": "2026-05-25T11:32:14Z",
    "per_platform_status": [
      { "platform": "facebook", "eligible": true, "posted_at": "2026-05-25T11:34:01Z", "post_url": "https://facebook.com/.../posts/123" },
      { "platform": "linkedin", "eligible": true, "posted_at": null, "post_url": null }
    ]
  },
  "meta": { "api_version": "1.0", "request_id": "..." }
}
```

**Skill output to user:**

> "Morning coffee ritual" was approved 2 hours ago.
>
> ✓ **Facebook** — posted: https://facebook.com/.../posts/123
>
> ⏳ **LinkedIn** — engine is about to post; check back in a minute or two.

---

## Example 4 — Submission rejected

**User prompt:**
> Did my last submission post?

**Skill action plan:**

1. `GET /api/v1/submissions?limit=1`.

Returns:
```json
{
  "data": [{
    "submission_id": "sub-bad",
    "status": "rejected",
    "rejection_reason_category": "community_standards",
    "rejection_notes": "References a competitor's brand name; please remove or paraphrase before resubmitting."
  }],
  "meta": { "api_version": "1.0", "request_id": "...", "next_cursor": null }
}
```

**Skill output to user:**

> Your last submission was **rejected** during compliance review.
>
> **Reason — community standards:**
> "References a competitor's brand name; please remove or paraphrase
> before resubmitting."
>
> You can revise and resubmit from the dashboard:
> https://zarzoom.com/dashboard/my-submissions

---

## Example 5 — Analytics summary

**User prompt:**
> How did my posts do this month?

**Skill action plan:**

1. `GET /api/v1/me/stats/overview?days=30`
2. `GET /api/v1/me/stats/top?days=30&limit=3`
3. `GET /api/v1/me/stats/by-platform?days=30`

**Skill output to user:**

> Last 30 days at a glance:
>
> - **24 posts published** across all platforms.
> - **3,847 total engagements** (likes + comments + shares).
> - **+312 followers** net across all connected accounts.
>
> **Top performers:**
> 1. "Morning coffee ritual" — 487 engagements (Facebook + LinkedIn)
> 2. "Best podcast episodes" — 312 engagements (Twitter / X)
> 3. "Home office setup" — 290 engagements (Pinterest + Instagram)
>
> **Strongest platform:** LinkedIn (1,247 engagements, up 18% vs prior 30 days).
> **Weakest:** Bluesky (43 engagements; consider posting more frequently).

---

## Example 6 — Rate-limit hit

**User prompt:**
> Submit this video.

**Skill action plan:**

1. Presign + PUT + `POST /api/v1/content/videos`.

Receives 429:
```json
{
  "error": {
    "code": "rate_limit_exceeded",
    "message": "Daily write limit of 40 reached for this workspace.",
    "details": {
      "limit": 40,
      "used": 40,
      "reset_at": "2026-05-26T00:00:00Z",
      "retry_after_seconds": 27384
    },
    "request_id": "..."
  }
}
```

**Skill output to user:**

> ZARZOOM's daily-write limit kicked in — your workspace has used all
> 40 submissions for today.
>
> The cap resets at **midnight UTC** (about 7 hours from now). Try
> again then, or upgrade your plan from the dashboard if you need
> more headroom.
>
> Your image upload was successful (no extra charge on retry); the
> only thing not yet stored is the article body itself.

---

These transcripts are illustrative. Real OpenClaw output will vary
based on the user's prompt, conversational style, and model
temperature, but the API call sequence and the structural information
shown to the user should match these patterns.
