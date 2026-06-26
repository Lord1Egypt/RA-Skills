# YouTube to Blog Post — OpenClaw Skill

**Turn any YouTube video into a publish-ready, SEO-optimised blog post in seconds.**

Stop spending hours manually repurposing video content. Paste a URL, get a full article.

---

## What it does

Give it a YouTube URL. Get back:

- **SEO metadata** — optimised title, meta description, URL slug, primary and secondary keywords
- **Full blog post** — 600–1,800 words depending on video length, properly structured with H2/H3 headings
- **Affiliate and internal linking suggestions** — anchor text opportunities flagged throughout
- **Publish-ready formatting** — markdown output, clean and paste-ready

---

## Who it's for

- Content creators repurposing videos into written content
- Bloggers covering topics from YouTube sources
- Affiliate marketers building SEO content at scale
- Anyone running a niche site who wants to turn video research into articles fast

---

## Installation

```bash
npx clawhub@latest install tetsuakira-vk/youtube-to-blog
```

---

## Usage

```
Use youtube-to-blog with this video: https://youtube.com/watch?v=...
```

Or paste a transcript directly:

```
Use youtube-to-blog with this transcript: [paste transcript]
```

---

## Example output

**Input:** 10-minute YouTube tutorial on budget home recording setup

**Output:**
- Title: "Home Recording Setup on a Budget: Everything You Need in 2026"
- Meta description: 158 characters, includes primary keyword
- 1,100-word post with 4 H2 sections and 2 H3 subsections
- 5 affiliate linking opportunities flagged (audio interface, microphone, DAW software)
- British English, active voice throughout

---

## Features

| Feature | Detail |
|---|---|
| Transcript sources | Auto-generated captions, manual captions, or pasted text |
| Output length | Scales with video length (5 min = ~700 words, 15 min = ~1,200 words) |
| SEO optimisation | Primary keyword, secondary keywords, meta description, URL slug |
| Linking suggestions | Up to 5 affiliate/internal link anchor text suggestions |
| Language support | Detects non-English content, asks before translating |
| Formatting | Clean markdown, ready to paste into WordPress, Ghost, or any CMS |

---

## Requirements

- OpenClaw installed and running
- Any supported LLM (Claude recommended for best writing quality)
- A YouTube URL with available captions, or a pasted transcript

No API keys required for transcript-based use.

---

## Tips

- Works best with educational, tutorial, review, and explainer videos
- For videos without captions, paste the transcript manually — the output quality is identical
- Use the linking suggestions section to quickly identify affiliate opportunities before publishing
- Run multiple videos through in sequence to build out a content cluster around a topic

---

## Licence

MIT — free to use, modify, and build on.

---

## Feedback & issues

Open an issue on GitHub. Actively maintained.
