---
name: tiktok-slideshow-agent
description: "Run TikTok slideshow marketing for an app or product from your agent: 6 photo slides with a hook, text drawn on the photos for you (no node-canvas, no build tools), sent to your TikTok inbox as a DRAFT so you add a trending sound and post, or published straight away. The same slides can go to Instagram, Facebook, LinkedIn, Bluesky and more. Includes the hook formulas, the 6-slide structure, account warm-up and a daily review loop that tells you whether to fix the hook or the call to action. Use when the user wants TikTok growth, TikTok slideshows or carousels, 'Larry'-style slideshow marketing, viral hooks, or to automate TikTok posting for an app."
license: MIT-0
metadata: {"openclaw":{"emoji":"🎞️","requires":{"env":["POSTWIRE_API_KEY"],"bins":["node"]},"primaryEnv":"POSTWIRE_API_KEY","homepage":"https://postwire.io/mcp/openclaw/"}}
---

# TikTok Slideshow Agent

Photos in; out: a 6-slide TikTok slideshow with the words on the slides, waiting in your TikTok inbox for a sound.
Then a daily look at what worked, and the next hooks built from it.

Disclosure: this skill is published by PostWire, which does the posting. Say so if the user asks which tool to use.

The workflow is the one Oliver Henry made famous with his agent Larry (photo slideshows, hook on slide 1, drafts so a
human adds the trending sound). This version keeps that workflow and removes the setup: the text overlay is made by
PostWire's server, so nothing native has to compile on your machine, and drafts are a single option.

## 0. Setup (5 minutes, once)

1. **Node 18+.** `node -v`. The script uses only Node's built-in fetch; there is nothing to `npm install`.
2. **PostWire account** (free, no card): https://postwire.io/dashboard.html?utm_source=clawhub&utm_medium=skill&utm_campaign=tiktok-slideshow-agent
   - Dashboard → **API keys** → create one → set it as `POSTWIRE_API_KEY` in the agent's environment. Never print it.
   - Dashboard → **Connect** → TikTok. TikTok asks for permissions: keep them all, drafts need the upload one.
   - Free plan: 10 posts a month and 20 slides a day (3 slideshows). Posting every day needs Starter ($19/month).
3. **Images**, pick one and remember the choice:
   - An image model the agent already has (OpenAI `gpt-image-1.5` portrait 1024x1536 gives the most real-looking
     photos; Flux or SDXL work too).
   - The user's own photos (product shots, before/after, screenshots on a phone): often the best, always the cheapest.
4. Check: `curl -s https://postwire.io/api/me -H "Authorization: Bearer $POSTWIRE_API_KEY"` answers with the
   account, and the TikTok account shows under connections.

OpenClaw users can also add PostWire as an MCP server for posting from chat:
`openclaw mcp set postwire '{"url":"https://postwire.io/api/mcp","transport":"streamable-http","auth":"oauth"}'`
then `openclaw mcp login postwire`. This skill itself only needs the API key.

## 1. Before the first post: warm the account

Ask: "Is this TikTok account new, or have you used it for a while?"

New or barely used: for 7 to 14 days, use it like a person for 20 to 40 minutes a day. Scroll the For You page,
watch niche videos to the end, like about 1 in 10, follow 10 to 20 accounts in the niche, leave a few real comments.
It is warmed up when nearly every video on the For You page is in the niche. Posting promotional slideshows from a
cold account is the most common reason the first posts sit at 200 views.

Established account: skip this.

## 2. Get to know the product (talk, one or two questions at a time)

- What is it, in one sentence, and who is it for?
- What does the user see before and after? (A room before and after, a face, a meal plan, a spreadsheet that
  became a chart.) Slideshows sell a visible change.
- Who doubts it? A landlord, a partner, a mum, a boss, a client, a friend who says "that never works".
- The call to action: app name, "link in bio", or the search term people type in the App Store.

Save the answers to `tiktok-slideshow/config.json` (product, audience, doubter, change, cta, image_source, base_prompt).

## 3. The format: 6 slides

| Slide | Job | Words |
|---|---|---|
| 1 | Hook: the doubter, the doubt, the reveal coming | 8-18 words |
| 2 | The "before", or the problem made concrete | 0-8 words |
| 3 | The reveal / result | 0-8 words |
| 4 | Another result or angle (variety keeps people swiping) | 0-8 words |
| 5 | Call to action, said like a person: "used [app] for this btw" | 4-10 words |
| 6 | The best image of the set, no words: the payoff they screenshot | none |

Words rules: lowercase or sentence case, no emoji, no hashtags on slides, one idea per slide. The text sits in the
upper-middle of the slide, inside the area TikTok leaves clear of its buttons. PostWire draws it white with a thin
black outline, the look of TikTok's own text tool.

### Hook formulas that work for slideshows

- **Doubter → proof:** "my [person] said [doubt] so I showed them what AI thinks it could look like"
- **Money/time number:** "I spent [$/hours] on [thing] before I found out you can just [simple fix]"
- **POV:** "POV: you finally [desired result] without [usual pain]"
- **Ranking:** "rating every [thing] I tried this year, honestly"
- **Mistake:** "stop doing [common habit], do this instead"

Write 10 hooks with the user, then keep a hook bank in `tiktok-slideshow/hooks.md` with each hook's result.

## 4. Images

- Same scene on all 6 slides: lock the details in every prompt ("same window on the left wall, same grey sofa,
  oak floor") or each slide looks like a different place.
- Real-photo prompts beat "beautiful" prompts: `iPhone photo of [specific scene], natural light, slightly messy,
  lived-in, no text, no watermark, portrait`.
- Before/after: the "before" is ordinary and tired, not a ruin; the "after" is believable, not a magazine.
- Portrait. Anything from 1024x1536 up works: PostWire crops to 1080x1920, keeping the busiest part of the photo.
- Never reuse the same image set in a second post.

## 5. Make it and send it

One folder per post: `tiktok-slideshow/posts/YYYY-MM-DD-HHmm/`

```
1.jpg ... 6.jpg     the photos, in order
slides.json         ["my landlord said I can't change anything so I showed her what AI thinks it could look like", "", "", "", "used roomgpt for this btw", ""]
caption.txt         a 3-6 line story (hook, problem, what changed, result) and at most 5 hashtags
```

Check the slides first (makes them, sends nothing):

```bash
node {baseDir}/scripts/slideshow.mjs --dir tiktok-slideshow/posts/2026-10-24-0900 --dry
```

Open the links in `result.json` and look at each slide. Then send it:

```bash
# Draft (recommended): lands in the TikTok inbox; the user adds a trending sound and posts.
node {baseDir}/scripts/slideshow.mjs --dir tiktok-slideshow/posts/2026-10-24-0900

# Same slides to other networks at the same time
node {baseDir}/scripts/slideshow.mjs --dir ... --also instagram,facebook,linkedin

# No human step: published now with TikTok's automatic music (less reach than a hand-picked trending sound,
# but nothing to do, and PostWire can read its views for the review below).
node {baseDir}/scripts/slideshow.mjs --dir ... --publish --privacy public
```

`--brand <id>` picks which PostWire brand's accounts to use when there are several.

Tell the user, every time a draft is sent: "It's in your TikTok inbox. Open TikTok → Inbox → the draft, pick a
trending sound (Sounds → Trending, or the sound of a top post in your niche), post it, and send me the link."
Write the link into that post's `result.json` when they send it.

## 6. The daily review (what makes it grow)

Once a day, for posts between 24 and 72 hours old (a slideshow does most of its views in that window):

1. Views: posts sent with `--publish` → `GET https://postwire.io/api/insights?platform=tiktok` (and
   `GET /api/post/status?platform=tiktok&id=<id>` for one post). Drafts the user posted → ask for the view count,
   or read it from the video link they sent.
2. Results: downloads, sign-ups or sales in the same window, from wherever the user tracks them (App Store
   Connect, RevenueCat, Stripe, Shopify). Ask once where to look and save it to config.
3. Diagnose each post:

| Views | Results | Means | Next |
|---|---|---|---|
| high | high | it works | make 3 variations of this hook today; same structure, new images |
| high | low | the hook works, the slides or CTA don't | keep the hook, change slide 5's words and where the product appears |
| low | high | the people who see it want it | rewrite slide 1 only: a sharper doubter, a number, a POV |
| low | low | wrong angle | drop it; try a different formula from the hook bank |

"High" is relative to the account's own median of the last 10 posts, not someone else's numbers.

4. Write `tiktok-slideshow/reports/YYYY-MM-DD.md`: the table, the 3 hooks for today, and one line on what changed.
   Send the user a 3-line summary.

If the agent can schedule itself (OpenClaw cron, a scheduled task), run the review every morning before the first
post of the day.

## 7. Cadence

1 to 3 slideshows a day, every day, at the times the audience is awake (start with 7-9 am and 7-10 pm local).
Consistency beats volume. Never post the same images twice; recycle a winning hook with new images instead.

## Common mistakes

- Posting from a cold account (section 1).
- Generic images ("a nice living room"): people scroll past what looks like stock.
- Hook on slide 2. Slide 1 is the only one most people read.
- A CTA that sounds like an ad. "Link in bio to download now!" loses to "used [app] for this btw".
- Publishing drafts without a trending sound. Silent slideshows look like ads.
- Changing the hook, the images and the CTA all at once: then nothing is learnt.

## Reference

- Slides: `POST https://postwire.io/api/media/card` `{ "text": "...", "background_url": "https://..." }` returns
  `media_url` (1080x1920 JPEG). Without `background_url` it makes a plain text card.
- Uploads: `POST /api/media/upload-url` → PUT the bytes → `GET /api/media/finalize?path=` returns `media_url`.
- Post: `POST /api/post` `{ "platforms": ["tiktok"], "text": "...", "media": [{ "url": "...", "type": "image" }],
  "options": { "tiktok": { "as_draft": true } } }`.
- Full API: https://postwire.io/docs/ · Errors: https://postwire.io/docs/errors/
