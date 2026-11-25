# Platforms: limits and the rules that matter for UGC creators

`ugclib.py` holds the same numbers `check_videos.py` uses. Platforms change them; when a platform
rejects something these say is fine, trust the platform and tell the user.

## The file

| | TikTok | Instagram Reels | YouTube Shorts |
|---|---|---|---|
| Length | 3 s up to the account's own limit (read it per account) | 3 s to 15 min | up to 3 min, or it becomes a normal video |
| Size | 4 GB | 300 MB | 256 GB |
| Frame rate | 23 to 60 | 23 to 60 | not restricted |
| Video | H.264 | H.264 or HEVC, standard colour, up to 25 Mbps | not restricted |
| Sound | not restricted | AAC, up to 48 kHz | not restricted |
| File | MP4 | MP4 or MOV with its index at the start | MP4 |

`make_video.py` writes one file that passes all three: 1080x1920 (or `--width`), H.264 High,
yuv420p, BT.709, AAC 48 kHz stereo, index at the start, -14 LUFS.

## Text

| | TikTok | Instagram Reels | YouTube Shorts |
|---|---|---|---|
| Title | none | none | required, 100 characters |
| Caption | 2,200 (most emoji count 2) | 2,200, at most 5 hashtags | description, 5,000 bytes |
| Links | not clickable | not clickable | not clickable in Shorts |

A link the brief requires in the caption goes in anyway (the campaign checks for it); the bio link
is the one viewers can tap.

## Paid content settings

| | Through WoopSocial | By hand |
|---|---|---|
| TikTok | `isBrandedContent: true` on every campaign post (TikTok's "Paid partnership" label). A branded post can't be "only you". | nothing |
| Instagram | WoopSocial can't set it | turn on the paid partnership label in the app, inside the 30 minutes |
| YouTube | WoopSocial can't set it (YouTube's own API has the field; WoopSocial doesn't send it) | tick "includes paid promotion" in YouTube Studio, inside the 30 minutes |


TikTok tells a creator when it detects undisclosed branded content and gives 24 hours before the
video loses For You eligibility. Content Rewards requires the platform's paid-partnership setting
where it exists, and "#Ad" at the top of the caption.

## Reused content and many accounts (2026)

The platforms act on the same content spread across accounts:

- **TikTok** keeps reposts with nothing new added out of For You, and limits reused material.
- **Instagram** (since 30 April 2026) stops recommending accounts that mostly repost, and shows the
  original of identical copies. A watermark or a speed change doesn't count as original.
- **YouTube** names networks of channels posting the same content in its spam policy.

These are about reposting and networks of accounts on one platform. Your own edit on your TikTok,
your Reels and your Shorts is normal cross-posting, and the skill allows it. What
`check_videos.py` blocks: the same file or the same take on two accounts of one platform (two
TikTok accounts), and any file, or a re-cut of the same take, already used for another campaign. A
different hook per platform is an optional test (the ledger shows which did better), unless the
brief asks for it. The skill never speeds up, mirrors, crops differently or filters a video to
dodge duplicate detection: the platforms don't treat that as new.

## Music

Music is declared, never guessed: `"music"` in edit.json is `{"source": "none"}`, a track you have a
license for (`"licensed"`, with the file and where the license is), or the brief's own track
(`"brief_supplied"`). `autoAddMusic` is always false. Trending sounds from an app's library can't be
added through any posting API and can't be added after posting; if a brief requires one, that post
goes out by hand with the sound added in the app before posting.

## Safe area

The apps draw their own buttons over the video: TikTok's tabs at the top, the like and share rail
on the right, the caption and account name at the bottom. `make_video.py` puts the on-screen
disclosure as a compact label in the top-left corner below the top tabs (from y 300 of 1920), the hook from y 420, and the captions on the
line between the two halves of a split screen (y 960) or just above the face in face plus screen
(y 1152), clear of the caption area at the bottom. Film with your face in the middle of the frame
and nothing you need seen in the bottom fifth.
