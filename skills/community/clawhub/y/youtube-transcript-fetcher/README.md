# youtube-transcript-fetcher

`youtube-transcript-fetcher` is an OpenClaw skill and CLI for extracting full YouTube transcripts reliably.

Instead of generating a short summary first, it returns the transcript text itself. That means OpenClaw can read the full content of the video directly and decide for itself how to analyze, summarize, translate, quote, or structure it.

## Why this exists

A lot of YouTube transcript tools fail on videos where normal caption fetching breaks, or only work when the uploader has explicitly provided subtitle tracks.

`youtube-transcript-fetcher` takes a more resilient path:

watch page scrape -> `INNERTUBE_API_KEY` extraction -> InnerTube player API fallback across multiple client profiles -> caption XML download -> transcript text extraction

This makes it much better at recovering transcripts from videos where simpler libraries return `No transcript available`.

## Main selling points

It is built around three ideas.

First, it fetches the transcript itself, not just a summary. Because there is no summary layer in the middle, OpenClaw can inspect the entire spoken content and keep full context.

Second, it can often recover YouTube's automatic captions even when manually attached subtitles are not present. In practice, this is the big win. A video may look like it has no uploader-provided subtitle set, but YouTube auto-generated captions are still available through the InnerTube caption path.

Third, it outputs plain JSON with the transcript included, so it is easy to plug into other OpenClaw flows.

## What it can fetch

`youtube-transcript-fetcher` can extract transcripts from:

- a single YouTube video URL
- a recent set of videos from a channel or handle
- a batch config for repeated runs

When transcript extraction succeeds, the JSON output includes a `transcript` field containing the full extracted text.

## How transcript recovery works

The core recovery flow is:

1. Fetch the YouTube watch page HTML
2. Extract `INNERTUBE_API_KEY`
3. Call `youtubei/v1/player`
4. Try multiple client identities in order:
   - `ANDROID`
   - `WEB`
   - `TVHTML5_SIMPLY_EMBEDDED_PLAYER`
   - `IOS`
5. Read caption track metadata from the player response
6. Download the caption XML from the selected `baseUrl`
7. Parse the XML into transcript text

This fallback approach is based on the same family of techniques used to recover captions in cases where normal transcript APIs are flaky.

## Why no summary is a feature

A summary throws information away.

If the goal is to let OpenClaw understand a video well, returning only a summary is weaker than returning the transcript. With `youtube-transcript-fetcher`, OpenClaw can read the source material directly, which is better for:

- detailed analysis
- extracting exact claims or quotes
- translation
- structured output generation
- custom summaries tailored to the user's task
- reusing the transcript in other tools or agents

This is also what makes the output flexible downstream. Once you have the transcript, you can summarize it, translate it, extract quotes, or turn it into structured data later with whatever model and prompt you want.

So this project is intentionally transcript-first, not summary-first.

## Usage

Single video:

```bash
./youtube-transcript-fetcher --url "https://www.youtube.com/watch?v=VIDEO_ID"
```

It also accepts raw video IDs, `youtu.be/...`, and `youtube.com/shorts/...` URLs.

Recent videos from a channel or handle:

```bash
./youtube-transcript-fetcher --channel "@channel_handle" --hours 24
```

Batch mode with config:

```bash
./youtube-transcript-fetcher --config config/channels.example.json --daily
```

You can also write output to a specific file:

```bash
./youtube-transcript-fetcher --url "https://www.youtube.com/watch?v=VIDEO_ID" --output /tmp/youtube_transcript_fetcher.json
```

## Output format

The tool writes JSON like this:

```json
{
  "generated_at": "2026-04-09T04:00:00+00:00",
  "items": [
    {
      "video_id": "...",
      "title": "...",
      "url": "...",
      "channel": "...",
      "duration": "12:34",
      "published": "20260408",
      "has_transcript": true,
      "metadata": {
        "view_count": 12345,
        "like_count": 678
      },
      "transcript": "full transcript text here"
    }
  ],
  "stats": {
    "total_videos": 1,
    "with_transcript": 1,
    "without_transcript": 0
  }
}
```

If transcript extraction fails, `has_transcript` becomes `false` and an error message is included.

## Requirements

This project depends on:

- `python3`
- `yt-dlp`
- Python packages from `requirements.txt`

Quick setup example:

```bash
pip install -r requirements.txt
```

Install `yt-dlp` with your package manager, for example:

```bash
brew install yt-dlp
```

or:

```bash
sudo apt install yt-dlp
```

## Add it to OpenClaw

This repository is structured as an OpenClaw skill.

The simplest way is to clone or copy this repository into your OpenClaw skills directory.

Example:

```bash
cd ~/clawd/skills
git clone https://github.com/ioridev/youtube-transcript-fetcher.git
```

After that, OpenClaw can discover the skill from the `SKILL.md` metadata.

If you just want to run it directly, use the bash entrypoint:

```bash
./youtube-transcript-fetcher
```

The Python implementation lives at:

```bash
scripts/youtube_transcript_fetcher.py
```

Do not run `python youtube-transcript-fetcher`, because `youtube-transcript-fetcher` itself is a shell wrapper.

Typical OpenClaw-side use is: fetch the transcript first, then let OpenClaw read the transcript text directly for analysis, translation, extraction, or summarization.

## OpenClaw usage idea

A good pattern is:

1. run `youtube-transcript-fetcher` on the target video
2. get JSON containing `transcript`
3. pass that transcript to OpenClaw as source material

That keeps the workflow transcript-first and avoids losing information through a premature summary layer.

## Practical note on auto captions

One of the main reasons to use this project is that uploader-provided subtitles are not required.

If YouTube has generated automatic captions for the video, `youtube-transcript-fetcher` can often recover them even when ordinary transcript methods fail. That is the core value of the project.

## Security note

This project fetches caption data directly from YouTube. It does not route caption downloads through a third-party proxy.

## Git tag based ClawHub release flow

This repository is set up so Git tags can be used as the publish version.

The GitHub Actions workflow watches tags like `v0.1.1` and publishes that exact version to ClawHub.

Example:

```bash
git tag v0.1.1
git push origin v0.1.1
```

That will publish ClawHub version `0.1.1`.

Before this works, add this repository secret in GitHub:

- `CLAWDHUB_TOKEN`: your ClawHub API token used by `clawdhub login --token ...`

You can also trigger the workflow manually with `workflow_dispatch` and pass a version and changelog.

## License

See `LICENSE`.
