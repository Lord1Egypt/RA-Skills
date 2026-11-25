# Short video script and storyboard

The brief and the script are free. Freeze the chosen hook before any still.

## Shot list

Four to six shots, about 30 to 45 seconds of speech. Each row has the job, what must stay visible, the 9:16 framing, the on-screen line, the spoken line, and a duration. Shot 1 is the hook and must work with the sound off. Keep type and the product out of the lower caption band.

Name the hook: a visual interruption, a question, the outcome first, or a face. One of those, not all four.

## Evidence

One lookup card, one `beatra.social.execute`. Copy `schema_hash` from the `beatra.social.tools.get` you just called. A next page is another execute.

- `social.douyin.hot_search.list`
- `social.douyin.video.search`
- `social.douyin.video.comments.list`
- `social.xiaohongshu.note.search`
- `social.xiaohongshu.note.comments.list`
- `social.tiktok.video.search`
- `social.twitter.tweet.search.recent`

Use comments when the hook should repeat a phrase people already used. Quote that phrase. Do not invent a count. Do not read WeChat, Channels, or Bilibili.

## Stills, read, bed

Upload a product photo and pass the artifact. `beatra.images.generate` is only the first still when there is no photo. Every other still is `beatra.images.transform` from the product photo or from the accepted hook still. One `beatra.images.edit` repairs a still whose product or on-screen line came back wrong, then stop.

`beatra.voices.list`, then one `beatra.speech.synthesize` of the chosen script. One instrumental `beatra.music.generate`.

## Clip

Video card, then one `beatra.videos.animate` per shot. The shot that speaks passes `driving_audio` and an admitted model. Duration is the smallest whole second at or above the real audio for that shot. Omit `aspect_ratio`. An end frame uses `beatra.videos.interpolate`.

Join with `beatra.videos.compose` after every shot succeeds. Per-shot clips stay muted. Pass the read as `narration`, the bed at `volume` 0.25, and subtitles from the spoken lines. Canvas `9:16`. At most 12 clips. If one clip is shorter than its span, deliver the parts.

## Worked clip

Subject: a folding travel kettle. Audience: people who pack a mug. Hook: the outcome first, a cup filling in a hostel kitchen. Five shots, one product photo carried by transform, one 20-second read, one bed, one 9:16 clip. The script stays in the delivery even if the clip stops.
