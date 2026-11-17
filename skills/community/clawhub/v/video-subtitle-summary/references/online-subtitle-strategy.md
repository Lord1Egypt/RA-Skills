---
AIGC:
  ContentProducer: '001191110102MAD55U9H0F10002'
  ContentPropagator: '001191110102MAD55U9H0F10002'
  Label: '1'
  ProduceID: 'b9eab87d-4b12-4490-ad58-f7f356765e5a'
  PropagateID: 'b9eab87d-4b12-4490-ad58-f7f356765e5a'
  ReservedCode1: '1d8a8e0a-bef7-4889-9a05-7bc633fde950'
  ReservedCode2: '1d8a8e0a-bef7-4889-9a05-7bc633fde950'
---

# Online Subtitle Strategy

## Acquisition Order (subtitle-only)

1. Use existing subtitles or transcripts when the page exposes them.
2. Use browser-visible transcript panels or subtitle lists from the player.
3. **API route interception** (preferred for learning platforms): intercept API responses during page load via Playwright `page.on("response")`, rather than calling APIs afterwards with `fetch`.
4. Ask the user to log in directly in the browser when authorization is required, then re-read the exposed subtitle/transcript.
5. Ask the user to provide a subtitle file (SRT/VTT/TXT/MD/JSON) or switch to a video source that exposes subtitles.

Do NOT attempt audio extraction, audio transcription, real-time playback capture, or any DRM/anti-download bypass.

## Site Families

### Bilibili and public video platforms

- Prefer exposed subtitles or transcript metadata via official subtitle endpoints when accessible.
- Use supported tools (such as `yt-dlp --write-subs --skip-download`) only to fetch subtitle files the user is already authorized to access; never download audio or video for transcription.
- If no subtitle is exposed, stop and ask the user to provide a subtitle file or switch source.
- Preserve source URL, title, duration, and acquisition method in metadata.

### Online learning platforms (zhixueyun.com etc.)

All online learning platforms are public internet websites. Login is treated as ordinary website user authentication, not enterprise intranet access.

#### Proven API endpoints (zhixueyun.com)

The following API endpoints have been verified through real usage:

| API endpoint | Purpose | Key fields |
|---|---|---|
| `/api/v1/course-study/course-info/front/find-by-ids` | Resolve course short link IDs to UUID; returns course list from homepage | `id` (course UUID) |
| `/api/v1/course-study/course-info/front/find-by-id?courseId={UUID}` | Get full course metadata | `name`, `lecturer`, `description`, `courseChapters`, `courseTime` |
| `/api/v1/course-study/guide-study/get-guide-study-info?courseId={UUID}&sectionId={sectionId}` | **Primary data source**: AI-generated knowledge point summaries with timestamps | `beginTime`, `endTime` (ms), `name`, `content` |
| `/api/v1/course-study/guide-study/get-guide-record?courseId={UUID}&sectionId={sectionId}` | Guide records with file IDs | `fileId` |

**Important**: The old API endpoints listed in some references (`class-info/safe/chapter/paas`, `course-front/score`, `url-progress`) were NOT useful for subtitle extraction. Use the endpoints above instead.

#### Proven extraction workflow

1. **Resolve UUID**: If user provides short link (`detailInfo5748`), navigate to homepage and intercept `find-by-ids` API to get course UUID. Alternatively, navigate directly to `#/study/course/detail/{UUID}` if UUID is known.
2. **Navigate to course detail page**: URL format: `https://kc.zhixueyun.com/#/study/course/detail/{UUID}`
3. **Intercept API responses on page load**: Set up `page.on("response")` listener BEFORE navigating. Key APIs fire automatically:
   - `find-by-id` → course metadata (name, lecturer, chapters, duration)
   - `guide-study-info` → 20 AI knowledge point summaries with ms-timestamps
   - `guide-record` → guide records
4. **Extract DOM subtitles**: After page load, extract subtitle text from the DOM (subtitle panel with timestamps and text content).
5. **Combine data sources**: AI knowledge summaries + DOM subtitle text → comprehensive report.

#### Token handling

- localStorage `token` key stores a JSON string: `{"access_token":"...","token_type":"Bearer","lang":"cn"}`
- Parse with `JSON.parse()` to extract `access_token` for Authorization header
- **Critical**: API calls via in-page `fetch` after page load may lose session context (returns 401). Prefer intercepting API responses during natural page load rather than making separate fetch calls afterwards.

#### Key technical notes

- Page routing is Hash-based (`/#/...`)
- Short link IDs (`detailInfo5748`) do NOT work as direct navigation targets; must resolve to UUID first
- Video source is HLS (m3u8) via blob URL; do not attempt to download
- Auto-play policy: set `--autoplay-policy=no-user-gesture-required` for browser launch
- jQuery-style selectors (`$('selector')`) work on the page DOM

For the complete Playwright automation script, see `references/playwright-browser-automation.md` and `scripts/zhixueyun_extractor.py`.

### Direct media and HLS/m3u8 links

- These links point to media streams and rarely expose subtitle files. Detect accompanying subtitle tracks in the playlist only when the platform legitimately exposes them (e.g., `#EXT-X-MEDIA:TYPE=SUBTITLES` in an HLS playlist that the user is authorized to access).
- If no subtitle track is exposed, stop and ask the user to provide a subtitle file.
- Do not download or transcribe audio, video, or encrypted streams.

## Failure Handling

When subtitle extraction fails, explain the limitation and offer allowed alternatives:

- Provide a subtitle file (SRT/VTT/TXT/MD/JSON).
- Open the page in the browser so the assistant can read a visible transcript panel.
- Switch to a video source that exposes subtitles.

Always mark partial processing in the final Markdown report. Never attempt audio transcription as a fallback.