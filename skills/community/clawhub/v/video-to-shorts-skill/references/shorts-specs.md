# Shorts specs

What `scripts/make_shorts.py` does, and why. Platforms change these details; re-check every
quarter.

## Frame

- **1080x1920, the source frame rate (24 to 60), H.264 High, yuv420p, BT.709, AAC 48 kHz stereo, moov at the front.** One
  file that TikTok, Instagram Reels, YouTube Shorts and Facebook Reels all accept. About 4 to 9
  Mbps, so a 45-second clip is 20 to 50 MB, well under every platform's limit.
- **Framing modes:**
  - `crop`: a 9:16 window from the full source height, placed on the speaker (`focus_x`, or found
    with OpenCV), with a 1.1x punch-in. Best for one speaker. Every second segment after a cut
    punches in a little further (1.12x), so removed pauses read as edits, eyes kept level.
  - `fit`: the whole frame, scaled to the width, on a blurred and darkened copy of itself. For
    two people far apart, screen shares, slides and wide shots.
  - A source that is already vertical is just scaled.
- **Small sources:** a 720p source is enlarged about 2.7x in a crop and looks soft. Use `fit`, or
  a bigger source.

## Safe area for text

TikTok, Reels and Shorts draw buttons on the right, the caption and account name at the bottom,
and the search or tabs at the top. Text is centred on the frame and stays inside **x 180 to 900,
y 290 to 1250** (narrow enough to clear the buttons on the right while staying centred):

- Captions: centred on x = 540, at most 720 px wide, bottom of the block at y = 1230.
- Hook box: centred on x = 540, at most 720 px wide.
- Hook: just above the captions in a crop (the face fills the top), at the top in `fit`.

## Captions

- Poppins ExtraBold (bundled, SIL Open Font License), a fixed 96 px (never resized mid-clip),
  white, 8 px black outline, soft shadow.
- Up to three words at a time on one line, the spoken word in the accent colour (default
  #FFD43B). Groups break at punctuation and pauses, and never end on a small word like "the".
- The first word is capitalised when a clip starts mid-sentence.
- Drawn with Pillow and laid over the video, so any ffmpeg build works.

## Hook

- The first 3.5 seconds, 3 to 8 words, black on a white rounded box, 78 px (down to 70 to fit two
  lines). Clips over 40 seconds show it again for 2 seconds halfway.
- Lines are balanced so no word sits alone.

## Audio

- High-pass at 80 Hz, loudness normalised to -14 LUFS with a -1 dB true-peak ceiling: the level
  the platforms play at, so clips aren't turned down or sound weak.
- 10 ms fades at every cut so removed pauses don't click.

## Pauses

`"tighten": true` (the default) removes pauses over 0.45 seconds and keeps 0.12 seconds of air
around words. Transcribers often stretch a word over a silence; word lengths are capped so those
pauses go too. `"fillers": true` cuts "um", "uh", stutters and "you know,". `"cut"` removes any
range the agent lists. Typically 10 to 20% shorter, and it feels faster without sounding cut.

## Reused content rules (2026)

- **YouTube** (inauthentic content policy, July 2025): mass-produced or repetitive uploads can lose
  monetisation. Clips of your own videos are fine; clipping others needs real editing and
  permission.
- **TikTok:** reposts of other people's content with nothing new added are kept out of For You.
- **Instagram:** reposts of someone else's content are replaced by the original in
  recommendations; "materially edited" content counts as original, a watermark or speed change
  doesn't.
- **Many accounts:** posting the identical file everywhere looks like spam and gets demoted. Give
  each account its own clips or at least its own hook and caption, and stagger the times.
