# edit.json: what make_video.py edits

```json
{
  "campaign": "campaign.json",
  "script": "script.json",
  "music": {"source": "none"},
  "style": {"accent": "#FFD43B"},
  "videos": [
    {"id": "tiktok", "account": "TikTok", "layout": "split_screen", "creator": "takes/creator.mp4",
     "transcript": "work/transcript.json", "supplied": "orbit-footage.mp4", "supplied_start": 0},
    {"id": "reels", "account": "Reels", "layout": "split_screen", "creator": "takes/creator.mp4",
     "transcript": "work/transcript.json", "supplied": "orbit-footage.mp4", "supplied_start": 4},
    {"id": "shorts", "account": "Shorts", "layout": "face_screen", "creator": "takes/creator.mp4",
     "transcript": "work/transcript.json", "screen": "takes/screen.mp4"}
  ]
}
```

- `account` is the name script.json's `openings` uses: that decides which hook opens the video.
  `"accounts": ["TikTok", "Reels", "Shorts"]` sends one edit to several accounts (normal
  cross-posting); they must share the opening hook, and no platform twice.
- `creator` (or `voiceover` for `broll_voiceover`) is your take, filmed in one go; `transcript` is
  what `transcribe.py` wrote for it, and it must be of that exact file. The edit keeps the opening
  hook and the last full try of each script line; `"assemble": false` keeps the take as it is.
  `trim_silence: false` keeps the pauses. `hook_take` opens the video with a separate hook clip;
  `hook_transcript` is `transcribe.py`'s transcript of that clip (required): its words are
  captioned, timed and checked like the rest, so a hook take can say the disclosure, never deny it.
  make_video prints what the edit cut (flubbed tries, sentences not in the script).
- `supplied_audio` (split screen): `"mute"` (the default), `"duck"` (the brand clip's sound about
  18 dB under your voice, back up in the gaps) or `"keep"` (both at full level). The disclosure is
  still your own line.
- `captions` and `hook_text` (per video or for the whole edit): `false` leaves the captions or the
  hook box off. A campaign with `"burned_text": "none"` turns both off and draws no label;
  `"disclosure_only"` keeps the "Ad" label alone.
- `inserts`: `[{"line": "l1", "file": "takes/screen.mp4", "start": 0}]` lays a screen recording or
  product shot over that line; the manifest records when the product is first on screen.
- `supplied` must be a file the brief supplied (`supplied_footage.files`); `screen` is your screen
  recording; `broll` is the list of b-roll shots in script order.
- `music` is required: `{"source": "none"}`, `{"source": "licensed", "file": "track.mp3", "license":
  "<where the license is>", "volume": 0.12}` or `{"source": "brief_supplied", "file": ..., "license":
  "the brief's track"}`. When the brief supplies a track it is mixed in under your voice; a brief
  that says no music refuses any.
- Refused in edit.json: `speed`, `mirror`, `flip`, `filter`, `face_filter`, `beauty`, `avatar`,
  `voice_change`, `lip_sync`, `pitch`. The skill never changes speed, mirrors or filters a video to
  make a copy look new, and never generates or alters a face or a voice.

```bash
python3 <skill>/scripts/make_video.py edit.json --out videos            # 1080x1920
python3 <skill>/scripts/make_video.py edit.json --out videos --placeholder --width 540
                                                     # before filming: a labelled layout preview
```

`--only <id>` edits one video and keeps the others' manifest entries as they were (check_videos.py
still says which are stale). `make_video.py --frames my-edit.mp4` writes the first seconds of any
file side by side, to confirm the on-screen label of an edit made elsewhere.

It writes `videos/<id>.mp4`, a cover frame each, `contact-sheet.jpg` and `manifest.json`: each
video's fingerprint, inputs and their fingerprints, the transcript's fingerprint, hook, on-screen
disclosure, the second the disclosure is said, every sentence actually said with its time, what was
cut, when the product is first on screen, the music, and the campaign and script versions. Show the contact sheet and ask the user to
watch every video before checking. A placeholder video can never be posted.
