# Titles and the hook clip

The topic list and the titles are free. Quote the line each title came from.

## Lookup

One card, one `beatra.social.execute`, `schema_hash` copied from the `tools.get` just read. A next page is another execute.

- `social.douyin.hot_search.list`
- `social.douyin.video.search`
- `social.douyin.video.comments.list`
- `social.xiaohongshu.note.search`
- `social.xiaohongshu.note.comments.list`
- `social.tiktok.hashtag.trends.list`
- `social.twitter.trends.list`

Prefer comments when the title should sound like a buyer. Quote that phrase. Do not invent a count. Do not substitute one platform's counts for another. Do not read WeChat or Bilibili.

## Cover and clip

Cover ratio is 3:4 for Xiaohongshu and 9:16 otherwise. Generate only when there is no photo. Transform when there is. One edit places the exact title on a clear band, large enough to read as a thumbnail.

`beatra.voices.list`, then one `beatra.speech.synthesize` of the hook, short enough for one shot.

```json
{
  "image": {"type": "artifact", "artifact_id": "art_cover"},
  "driving_audio": {"type": "artifact", "artifact_id": "art_hook"},
  "model": "<admits image plus driving_audio>",
  "prompt": "<one small motion; the title band stays put>",
  "duration": 4,
  "client_request_id": "opaque-hook-clip"
}
```

`beatra.videos.compose` with that one clip, `keep_audio` true, the title as the subtitle, canvas matching the cover. No second narration.

## Worked title

Pasted comments keep saying the thermos leaks in a backpack. Angle: the seal, not the steel. The title quotes the comment that it does not leak when laid on its side. Cover 3:4, title on a clear band, one four-second clip that speaks that line.
