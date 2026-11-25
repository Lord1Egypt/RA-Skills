# Formats: what you film for each layout

`script.py` writes `shotlist.md` with these set-ups for the formats the brief accepts. The final
video is 1080x1920; `make_video.py` does the stacking, cropping and captions.

| Layout | What you film | What `make_video.py` does |
|---|---|---|
| `talking_head` | You, to camera, in one continuous clip (`takes/creator.mp4`). Phone vertical, eye level, face in the middle third, window light in front of you | fills the frame with your take, keeps your last full try of each line, trims pauses over 0.45 s and "um"/"uh", punches in a little on every other cut, captions your own words |
| `split_screen` | The same take. The brand's supplied footage is the other half | the brand's footage in one half (the brief's `position`, top by default, muted unless `supplied_audio` is `"duck"` or `"keep"`), you in the other; captions on the line between. When the clip's sound carries it (a demo, a voiced clip), react to it: the disclosure and one or two lines of your own, with the clip ducked under your voice |
| `face_screen` | Your take, plus a screen recording of the app or site doing what the script says (`takes/screen.mp4`; the phone's own screen recorder) | the screen recording on top on a dark backdrop, you below |
| `broll_voiceover` | Your hands and the product (b-roll shots, one file per shot), and your voice reading the script (`takes/voiceover.m4a`, any phone voice memo works) | the shots in order under your voiceover. For faceless briefs only |

## One clip, retakes welcome

Film it all in one go: every hook, one after the other, then the script. Flub a line? Pause and say
it again, as often as you like. `make_video.py` reads the transcript, keeps the hook that opens this
video and the last full try of each line (at least 70% of its words), and cuts the rest. It stops
and names the line when one is missing, so nothing is dropped silently. `"assemble": false` on a
video in edit.json keeps the take as it is (check_videos.py then flags every sentence that isn't
in the script). A separate hook take still works: `"hook_take"` in edit.json opens the video with it.

Inserts: a screen recording or product shot laid over a line of a talking head or split screen
(`"inserts": [{"line": "l1", "file": "takes/screen.mp4"}]`) shows the product while you talk about
it, and counts for a brief's "product on screen by second N".

Before you film:

- Read `script.md` out loud once. The disclosure can sit anywhere in the brief's window; a short
  "<brand> is paying me to show you this" is enough.
- For each hook, do what its action says (hold the phone to camera, point at the footage): the
  first frame should show the thing before you explain it (`references/hooks.md`).
- Back camera if you can, focus and exposure locked on your face (press and hold on the phone),
  Do Not Disturb on, a clip-on mic or the phone close to you.
- Say only what is true for you. A line tagged "experience" is yours to confirm.
- Quiet room, phone on a stand, 1080p or 4K at 30 fps, no beauty filter or face effect.
- Leave a second of silence before and after each take; the edit trims it.

Then: `transcribe.py takes/creator.mp4 --out work` (your words become the captions), write
`edit.json` (references/edit-file.md) and run `make_video.py`.
