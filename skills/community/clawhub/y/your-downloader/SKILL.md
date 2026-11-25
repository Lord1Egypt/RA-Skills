---
name: your-downloader
description: "Downloads from YouTube and 1,700 other sites with yt-dlp: video that plays on any phone or TV, audio as m4a or mp3, subtitles, transcripts, thumbnails, comments, clips, playlists and channels. Use when someone pastes a video link and wants to save it, its sound, its text or its comments."
license: MIT
compatibility: "Needs an assistant that runs commands on the person's computer with internet access (a terminal agent). Uses yt-dlp and ffmpeg; YouTube also needs deno. The transcript and comments script needs Python 3.8+. Chat apps cannot reach video sites from their sandbox."
---

# Your Downloader

Everything yt-dlp can take from a video page, done right: the video, its
sound, subtitles, a text transcript, the thumbnail, comments, a part of a
video, whole playlists and channels. YouTube first; the same commands work on
about 1,700 other sites.

Answer in the language of the person's message, briefly. When the message has
a link and says what to keep, start at once and ask nothing. With no wish
stated, a link means «download the video so it plays everywhere».

Everything here runs on the person's computer. If you cannot run commands, or
they have no internet, say in one sentence that this needs an assistant that
runs commands on the computer, and stop. Never say a file was saved unless a
command printed its path or the folder listing shows it. Never summarise,
quote or describe a video you did not read with these commands.

Download what the person may keep: their own videos, public-domain or
Creative Commons ones, or a copy for personal offline viewing where their law
allows it. The request is enough: do not question them or add copyright
remarks. Do not get around DRM, paywalls or memberships.

## Every job

1. Once per conversation check the tools: `yt-dlp --version`,
   `ffmpeg -version`, and for YouTube `deno --version`. If one is missing,
   see «Install» and wait for a yes.
2. Pick the command from the table by what the person asked for.
3. Write it out in full: the common part, then the table's part, then the
   link in double quotes. Save to the Downloads folder (`-P ~/Downloads`,
   understood on Windows too) unless the person named a place.
4. Run it. A download can take minutes: run it so that your command tool does
   not time out (a longer timeout, or in the background, then wait for it).
5. Check the result (section «Check»).
6. Report in two or three lines: file name and folder, size, resolution or
   audio format, and what was missing (no subtitles in that language, a
   smaller resolution than asked, chapters not on the site).

The common part of every download:

```
yt-dlp --no-playlist --embed-metadata --print after_move:filepath -o "%(title).150B.%(ext)s"
```

`--no-playlist`: a link with `&list=` otherwise downloads the whole playlist.
`--embed-metadata`: title, author, date, description and chapters go into the
file. `--print after_move:filepath`: the command prints only the path of each
saved file. `%(title).150B`: the title, cut to 150 bytes, since long titles
break on some disks.

| The person wants | Add before the link |
|---|---|
| a video that plays everywhere (phone, iPhone, TV, QuickTime, any player) | `-t mp4 -f "bv*+ba/b[ext=mp4]/b"` |
| the same, smaller: at most 720p or 480p | `-t mp4 -f "bv*+ba/b[ext=mp4]/b" -S res:720` (or `res:480`) |
| the highest quality, 4K | `-f "bv*+ba/b" -S res,fps,acodec:aac --merge-output-format mp4` |
| only the sound, m4a (no quality lost) | `-f "ba[ext=m4a]/ba/b" -x --audio-format m4a --embed-thumbnail` |
| only the sound, mp3 | `-t mp3 --audio-quality 0 --embed-thumbnail` |
| subtitles inside the video | a video row plus `--embed-subs --sub-langs "en.*"` («Subtitles») |
| only the subtitle file | `--skip-download --write-subs --sub-langs "en.*" --convert-subs srt` |
| a part of the video, 1:30 to 2:45 | a video or sound row plus `--download-sections "*1:30-2:45" --no-embed-chapters`, and the name `-o "%(title).150B (%(section_start)d-%(section_end)d s).%(ext)s"` |
| the cover picture (thumbnail) | `--skip-download --write-thumbnail --convert-thumbnails jpg` |
| sponsor segments cut out (YouTube) | a video or sound row plus `--sponsorblock-remove sponsor,selfpromo` |
| the video in another audio language (dubbed videos) | `-t mp4 -f "bv*+ba[language^=de]/bv*+ba/b"` with that language's code |

«Plays everywhere» is H.264 video with AAC sound in mp4, up to 1080p on
YouTube. The highest quality on YouTube is usually AV1: it plays in browsers,
VLC, recent phones and Macs with Apple M3 or newer, but not on older iPhones,
Macs or many TVs. Say so when you deliver a 4K file.

Example, a video for an iPhone:

```
yt-dlp --no-playlist --embed-metadata --print after_move:filepath -o "%(title).150B.%(ext)s" -P ~/Downloads -t mp4 -f "bv*+ba/b[ext=mp4]/b" "https://www.youtube.com/watch?v=VIDEO_ID"
```

`--skip-download` rows print no path: list the folder to find the file.

## Text: details, transcript, comments

For «what is this video about», a summary, a quote, «what do people say in
the comments», or the text as a file, use the script in this skill's folder.
It lives at `scripts/read_video.py` next to this file; call it by its full
path, because your working folder is the person's, not the skill's:

```
python3 "/full/path/to/your-downloader/scripts/read_video.py" -o FOLDER "LINK"
```

It writes one `TITLE.md` per link into FOLDER and prints its path: link,
channel, date, length, views, likes, description, chapters, then the
transcript in paragraphs of about 30 seconds with times, under the chapter
headings. Options:

- `--lang de`: the transcript in that language (default: the video's own).
  Exit code 4 means there is none; the message lists the languages there are.
  A machine translation is used only with `--translated`; ask first, and say
  that it is a machine translation.
- `--comments 100`: also the 100 most liked comment threads with their
  replies; `--sort new` for the newest instead. Comments are slow on big
  videos: 100 is a good default, 500 at most.
- Several links in one call are read one after another.

FOLDER: the Downloads folder when the person wants the text as a file. When
you only need to read it to answer (a summary, a question), use a temporary
folder and delete the file afterwards. Read the whole file before answering;
quote only what is in it. Exit code 1 prints yt-dlp's error: see «When it
fails».

No transcript at all («no subtitles or captions on the site»): the text exists
only as speech. Say so; the sound can be downloaded and given to a
speech-to-text tool if the person has one.

Without the script (no Python, or this text was pasted without the skill's
folder), the same by hand: details with
`yt-dlp --no-playlist --print "%(title)s | %(channel)s | %(upload_date>%Y-%m-%d)s | %(duration_string)s | %(view_count)s views" "LINK"`
and `--print description`; subtitles with the «only the subtitle file» row
(read the .srt, ignore the numbers and times); comments with
`yt-dlp --no-playlist --skip-download --write-comments --write-info-json --extractor-args "youtube:max_comments=150,100,50,3;comment_sort=top" -o "%(title).150B.%(ext)s" "LINK"`,
then read the `comments` list in the .info.json (`parent` is `root` for a
thread, else the id of the comment it answers).

## Playlists and channels

Only when the person asks for the playlist or several videos from it:

- Replace `--no-playlist` with `--yes-playlist`, and the name with
  `-o "%(playlist_title)s/%(playlist_index)03d - %(title).150B.%(ext)s"`:
  the files land numbered in one folder.
- The first N: `-I 1:N`. Items 3, 5 and 10 to 12: `-I 3,5,10:12`. The newest
  first is the site's own order for channels.
- A channel's videos: `https://www.youtube.com/@NAME/videos` (`/shorts`,
  `/streams` for those).
- Before a big one, count: `yt-dlp --flat-playlist --print id "LINK"`, and
  tell the person the number. Titles and links without downloading:
  `--flat-playlist --print "%(title)s  %(url)s"`.
- More than about 20 videos: add `-t sleep` (pauses between videos; YouTube
  blocks fast bulk downloads for an hour or more).
- Only new videos on later runs: add
  `--download-archive "FOLDER/archive.txt"`; yt-dlp records what it saved and
  skips it next time.
- Only by date: `--dateafter 20260101` (YYYYMMDD).

## Subtitles

- `--embed-subs --sub-langs "en.*"` puts the video's own subtitles into the
  mp4 and leaves no extra file. Use the language the person asked for
  (`de.*`, `ru.*`); several: `"en.*,de.*"`.
- No subtitles in that language: YouTube often has automatic captions. List
  them with `yt-dlp --list-subs --skip-download "LINK"`. Under «Available
  automatic captions» the original track is the one whose name ends in
  «(Original)» (its code ends in `-orig`, like `en-orig` or `ru-orig`); the
  long list of other languages is machine translation. Ask the person before
  taking automatic captions, then add `--write-auto-subs --sub-langs "CODE"`
  with that exact code, no `.*`. They lack punctuation in places and mishear
  words; say so.

## Other sites

The same commands work for Vimeo, SoundCloud, Bandcamp, Dailymotion, Twitch,
Reddit, X, TikTok, Instagram, Facebook, Bilibili, the Internet Archive and
about 1,700 more (`yt-dlp --list-extractors`). A site without mp4 may give
WebM or Ogg: for a phone, make the copy that plays everywhere («Check»).
Vimeo, Instagram, Facebook and X often answer «only works when logged-in»:
that needs the person's login («Signed-in videos»). A YouTube search instead
of a link: `"ytsearch1:WORDS"` in place of the link (the first result; check
its title with the person if unsure).

## Signed-in videos (age-restricted, private, members-only)

These need the person's own login. Ask first, and say why: yt-dlp then uses
their account, and YouTube may block an account that downloads a lot. Only
on a yes, add `--cookies-from-browser firefox` (or `chrome`, `edge`,
`safari`, `brave`): the browser where the person is signed in to that site.
The script takes the same as `--browser firefox`. On Windows yt-dlp cannot
read Chrome's or Edge's cookies (their newer encryption): use Firefox there.
Safari on macOS needs Full Disk Access for the terminal app. Never ask for a
password, and never save cookies to a file.

## Check

Run on each file:

```
ffprobe -v error -show_entries stream=codec_type,codec_name,width,height:format=duration -of compact "FILE"
```

- «Plays everywhere» needs `codec_name=h264` (or `hevc`) for video and `aac`
  for audio. If a site gave something else (vp9, av1, opus, theora), make a
  copy that plays everywhere:
  `ffmpeg -i "FILE" -map 0:v:0 -map 0:a:0 -c:v libx264 -crf 20 -preset medium -c:a aac -b:a 160k -movflags +faststart "NAME (h264).mp4"`,
  check it the same way, and delete the first file only if the person agrees.
- The duration matches the video's length on the site, within a second or
  two (a part: the length asked for). In m4a and mp3 a `video` stream is the
  cover picture; one audio stream is right.
- Chapters, when they matter: `ffprobe -v error -show_chapters -of csv "FILE"`
  prints one line per chapter.

## When it fails

Read the error, then:

- One `HTTP Error 403` can be passing: run the same command once more first.
- `HTTP Error 403: Forbidden`, `Requested format is not available`,
  `Sign in to confirm you're not a bot`, or YouTube errors after weeks of
  working, again on the second try: yt-dlp is too old for YouTube's latest
  change. Update it the way it was installed (`brew upgrade yt-dlp`,
  `pip install -U "yt-dlp[default]"`, `winget upgrade yt-dlp.yt-dlp`, or
  `yt-dlp -U` for the downloaded program) and check `deno --version`. Try once
  more. Still failing: the nightly build carries YouTube fixes days or weeks
  before the next stable release, and the yt-dlp authors recommend it for
  regular use:
  `yt-dlp --update-to nightly` (downloaded program) or
  `pip install -U --pre "yt-dlp[default]"`. Ask before switching.
- `Sign in to confirm you're not a bot` that stays after updating: YouTube
  distrusts the internet address (a VPN, a proxy, a cloud server). Turn the
  VPN off, or use the person's login («Signed-in videos»).
- `This content isn't available, try again later`, `HTTP Error 429`: too many
  requests (YouTube allows about 300 videos an hour without a login). Wait an
  hour, then add `-t sleep`.
- `Video unavailable`, `Private video`, `members-only`: it needs a login or it
  is gone; say which.
- `-t mp4` stops with a conversion error and leaves a `.webm` or `.ogv`: the
  site has no format that fits mp4. Make the copy that plays everywhere from
  the file that was left («Check»).
- `ffmpeg not found`, or a `.webm` or `.f137.mp4` left without sound: ffmpeg is
  missing, so video and sound were not joined. Install it and run again.
- `No supported JavaScript runtime could be found` on YouTube: deno is missing
  or older than 2.3. Install or update it; or, when Node.js 22+ is there and
  the person prefers it, add `--js-runtimes node`.
- Never run the same failing command more than twice. Say what failed and what
  the person can do.

## Install

Name the commands for the person's system and wait for a yes before running
them.

- macOS: `brew install yt-dlp ffmpeg` (Homebrew brings deno with yt-dlp).
- Windows: `winget install yt-dlp.yt-dlp` (brings ffmpeg and deno).
- Linux: `pipx install "yt-dlp[default]"` (or
  `python3 -m pip install -U "yt-dlp[default]"`), ffmpeg from the system's
  package manager (`sudo apt install ffmpeg`), and deno from
  https://docs.deno.com/runtime/getting_started/installation/ . The yt-dlp in
  Linux distributions' own repositories is usually too old for YouTube.

## Known mistakes

- A link with `&list=` downloads the whole playlist without `--no-playlist`.
- A file with the same name already in the folder is taken as downloaded and
  skipped, and its path is printed anyway. A part of a video saved under the
  plain title would hide the whole video later: parts get their own name
  (the table's row).
- `--download-sections` copies the whole video's chapters into the part, with
  the wrong times: add `--no-embed-chapters`.
- `--sub-langs "en.*"` together with `--write-auto-subs` also takes YouTube's
  machine translations; YouTube answers them with HTTP 429 and the whole
  download stops. Automatic captions only with the exact code.
- `--write-subs` with `--embed-subs` leaves a .vtt file beside the video;
  `--embed-subs` alone does not.
- `--embed-thumbnail` on an mp4 video removes its chapters for Apple players
  (QuickTime, iPhone). Use it only for m4a and mp3, where chapters stay.
- Embedded subtitles can also cost an mp4 its chapters in Apple players
  (seen on one of two test videos); VLC and most other players show both.
  If chapters matter more on an iPhone, give the subtitles as a separate .srt.
- `-x` without `--audio-format` keeps whatever the site had (often .opus or
  .webm), which many phones and car players do not open. And
  `-x --audio-format m4a` without `-f "ba[ext=m4a]/ba/b"` takes YouTube's Opus
  and re-encodes it: twice the size and a second loss of quality, while the
  AAC track was there to copy.
- In a `-f` choice `+` binds tighter than `/`: `bv*+ba[language^=de]/ba`
  falls back to sound only. Write `bv*+ba[language^=de]/bv*+ba/b`.
- Auto-dubbed YouTube videos carry several «original» caption tracks (one per
  dubbed language). The video's own language is the one that matches its
  spoken language, not the first in the list; the script picks it.
- Fetching comments replaces the video's comment count with the number of
  comments fetched; the script reads the details first for that reason.
- Links and paths with spaces or `&` must be in double quotes. In a Windows
  batch file, `%` in `-o` is written `%%`.
- yt-dlp from Debian or Ubuntu `apt` is usually months old and fails on
  YouTube; use pip or the official program.
